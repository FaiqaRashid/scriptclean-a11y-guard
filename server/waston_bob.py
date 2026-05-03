"""
IBM watsonx.ai text generation — refines heuristic accessibility fixes using the API key.

Requires:
  IBM_BOB_API_KEY       — IBM Cloud IAM API key
  WATSONX_PROJECT_ID    — watsonx project GUID (IBM Cloud)

Optional:
  WATSONX_URL           — default https://us-south.ml.cloud.ibm.com
  WATSONX_MODEL_ID      — default ibm/granite-3-8b-instruct
  WATSONX_API_VERSION   — default 2024-05-31
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

IAM_URL = "https://iam.cloud.ibm.com/identity/token"
DEFAULT_ML_URL = "https://us-south.ml.cloud.ibm.com"


def watsonx_configured() -> bool:
    return bool(
        os.environ.get("IBM_BOB_API_KEY", "").strip()
        and os.environ.get("WATSONX_PROJECT_ID", "").strip()
    )


def get_iam_token(api_key: str) -> str | None:
    data = urllib.parse.urlencode(
        {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": api_key,
        }
    ).encode()
    req = urllib.request.Request(
        IAM_URL,
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.load(resp)
        tok = body.get("access_token")
        return str(tok) if tok else None
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def call_text_generation(
    access_token: str,
    project_id: str,
    model_id: str,
    prompt: str,
    ml_url: str,
    api_version: str,
) -> tuple[str | None, str | None]:
    url = f"{ml_url.rstrip('/')}/ml/v1/text/generation?version={urllib.parse.quote(api_version)}"
    body = {
        "input": prompt,
        "model_id": model_id,
        "project_id": project_id,
        "parameters": {
            "max_new_tokens": 1600,
            "min_new_tokens": 1,
        },
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            out = json.load(resp)
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace") if e.fp else str(e)
        return None, err[:500]
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        return None, str(e)[:500]

    results = out.get("results") or []
    if not results:
        return None, "empty_results"
    text = (results[0] or {}).get("generated_text")
    return (str(text) if text else None), None


def parse_first_json_value(text: str) -> Any | None:
    """Extract first JSON object or array from model output (handles markdown fences)."""
    if not text:
        return None
    s = text.strip()
    if "```" in s:
        chunks = re.split(r"```(?:json)?", s, flags=re.IGNORECASE)
        for chunk in chunks:
            chunk = chunk.strip()
            if chunk.startswith("{") or chunk.startswith("["):
                s = chunk
                break
    decoder = json.JSONDecoder()
    for i, c in enumerate(s):
        if c in "{[":
            try:
                obj, _ = decoder.raw_decode(s[i:])
                return obj
            except json.JSONDecodeError:
                continue
    return None


def normalize_fix_mapping(obj: Any) -> dict[str, str]:
    """Turn model JSON into {issue_id: fix_html}."""
    out: dict[str, str] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            if v is not None and isinstance(v, str) and str(v).strip():
                out[str(k)] = str(v).strip()
        return out
    if isinstance(obj, list):
        for item in obj:
            if not isinstance(item, dict):
                continue
            iid = item.get("id")
            fix = item.get("fix")
            if iid is not None and isinstance(fix, str) and fix.strip():
                out[str(iid)] = fix.strip()
        return out
    return out


def enhance_issues_with_watsonx(
    issues: list[dict[str, Any]],
    full_code: str,
    filename: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    One watsonx call to refine `fix` fields. On failure, returns issues unchanged
    with fix_source=heuristic only.
    """
    meta: dict[str, Any] = {
        "watsonx_available": watsonx_configured(),
        "watsonx_used": False,
        "watsonx_error": None,
        "watsonx_fixes_applied": 0,
    }

    for issue in issues:
        issue.setdefault("fix_source", "heuristic")

    if not issues or not watsonx_configured():
        return issues, meta

    api_key = os.environ["IBM_BOB_API_KEY"].strip()
    project_id = os.environ["WATSONX_PROJECT_ID"].strip()
    ml_url = (os.environ.get("WATSONX_URL") or DEFAULT_ML_URL).strip() or DEFAULT_ML_URL
    model_id = (
        os.environ.get("WATSONX_MODEL_ID") or "ibm/granite-3-8b-instruct"
    ).strip()
    api_version = (os.environ.get("WATSONX_API_VERSION") or "2024-05-31").strip()

    token = get_iam_token(api_key)
    if not token:
        meta["watsonx_error"] = "iam_token_failed"
        return issues, meta

    slim = []
    for iss in issues:
        broken = iss.get("broken_full") or iss.get("broken") or ""
        slim.append(
            {
                "id": iss["id"],
                "type": iss["type"],
                "wcag": iss.get("wcag", ""),
                "line": iss["line"],
                "broken": broken[:600],
                "heuristic_fix": (iss.get("fix") or "")[:900],
            }
        )

    code_trim = full_code if len(full_code) <= 16000 else full_code[:16000]

    prompt = f"""You are an expert web accessibility engineer (WCAG 2.1 Level A and AA).
Improve each accessibility fix for file "{filename}". Use the source code for context.

Output exactly one JSON value (an object OR an array) and nothing else:
- Preferred: an object whose keys are issue ids as strings and values are full HTML replacement strings.
  Example: {{"1": "<img src=\\"a.png\\" alt=\\"Company home\\">", "2": "<button type=\\"button\\" aria-label=\\"Open menu\\">"}}
- Alternative: array of objects: [{{"id": 1, "fix": "..."}}, {{"id": 2, "fix": "..."}}]

Rules:
- Each fix must replace the entire broken fragment (same tag type / role as heuristic_fix).
- Alt text: short, meaningful for screen reader users; never raw filenames like "logo-final-v3".
- Icon buttons: short aria-label describing the action.

Issues:
{json.dumps(slim, indent=2)}

Source code:
{code_trim}
"""

    raw, gen_err = call_text_generation(
        token, project_id, model_id, prompt, ml_url, api_version
    )
    if gen_err:
        meta["watsonx_error"] = gen_err
    if not raw:
        if not meta["watsonx_error"]:
            meta["watsonx_error"] = "generation_failed"
        return issues, meta

    parsed = parse_first_json_value(raw)
    mapping = normalize_fix_mapping(parsed)
    if not mapping:
        meta["watsonx_error"] = (meta.get("watsonx_error") or "parse_json_failed")
        return issues, meta

    applied = 0
    for issue in issues:
        iid = str(issue["id"])
        new_fix = mapping.get(iid)
        if not new_fix or not isinstance(new_fix, str):
            continue
        new_fix = new_fix.strip()
        if not new_fix:
            continue
        issue["fix_heuristic"] = issue.get("fix")
        issue["fix"] = new_fix
        issue["fix_source"] = "watsonx"
        applied += 1

    meta["watsonx_used"] = applied > 0
    meta["watsonx_fixes_applied"] = applied
    if applied == 0:
        meta["watsonx_error"] = meta.get("watsonx_error") or "no_matching_issue_ids"
    return issues, meta
