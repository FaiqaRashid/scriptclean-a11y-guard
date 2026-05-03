# ScriptClean: A11y Guard
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)
[![IBM Bob Hackathon 2026](https://img.shields.io/badge/Hackathon-IBM%20Bob%202026-ff69b4)](https://developer.ibm.com/hackathons/)
[![Powered by IBM Bob](https://img.shields.io/badge/AI-IBM%20Bob-00ced1)](https://www.ibm.com/)
[![WCAG 2.1](https://img.shields.io/badge/Standard-WCAG%202.1-ff8c00)](https://www.w3.org/WAI/WCAG21/quickref/)

---

**AI-Powered Accessibility Auditor Built on IBM Bob**

ScriptClean is an intelligent accessibility auditing tool that scans HTML, PHP, and JavaScript files to identify and fix WCAG violations. Powered by IBM watsonx.ai text generation (via your IBM Cloud API key and project), it can refine heuristic fixes using repository context—not just generic placeholders.

---

## The Impact

**Turn a 40-hour manual audit into a 2-hour automated fix.**

Traditional accessibility audits are time-consuming and error-prone. ScriptClean combines fast local scanning with optional watsonx refinement to analyze your code, surface barriers, and suggest context-aware fixes.

---

## Features

### One-Click Apply
Apply accessibility fixes from the UI. Selected issues are merged back into file content via `/api/apply-fixes` so you can copy or save the patched source.

### Side-by-Side Diff View
Compare broken snippets with suggested fixes before applying.

### Batch upload
Drag-and-drop multiple files; the client calls `/api/scan-batch` so everything is analyzed in one round trip.

### Bob / watsonx refinement (optional)
With `IBM_BOB_API_KEY` and `WATSONX_PROJECT_ID` set in `server/.env`, scan results are passed through watsonx to improve fix strings. Without those variables, the tool still runs using local heuristics only.

### Priority and reporting
Reports include priority hints, estimated fix time, impact-style scoring, and WCAG level summaries. Export saves structured JSON under `reports/` on the server.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.x with Flask |
| **Frontend** | Vanilla JavaScript (no frameworks) |
| **Design System** | IBM Carbon Design System |
| **Methodology** | Double Diamond (HCI) |
| **AI refinement** | IBM watsonx.ai (Granite instruct model by default) |

### Why These Choices?

- **Python/Flask**: Lightweight, cross-platform server with minimal dependencies
- **Vanilla JS**: Zero build tools, instant deployment, maximum compatibility
- **Double Diamond**: Human-centered design process ensuring the tool solves real accessibility challenges through discovery, definition, development, and delivery phases

---

## How IBM Bob / watsonx Powers This

The scanner first detects issues with regex and structure rules. When watsonx is configured, `server/watsonx_bob.py` sends constrained prompts so the model can **refine** fix text (for example, richer `alt` descriptions) using the file’s context.

### Example: Context-Aware Alt Text

**Generic Tool Output:**
```html
<img src="logo.png" alt="image">
```

**ScriptClean (with refinement):**
```html
<img src="logo.png" alt="Company logo showcasing brand identity">
```

The pipeline considers filename, surrounding lines, and WCAG-oriented instructions baked into the scanner and prompts.

---

## WCAG 2.1 Coverage

ScriptClean’s local checks map to areas such as:

| Criterion | Level | What ScriptClean Checks |
|-----------|-------|------------------------|
| **1.1.1** Non-text Content | A | Images missing meaningful `alt` |
| **4.1.2** Name, Role, Value | A | Interactive elements missing labels / ARIA where applicable |
| **1.3.1** Info & Relationships | A | Landmark / role structure |
| **2.4.6** Headings & Labels | AA | Heading hierarchy (skipped levels, etc.) |
| **3.3.2** Labels or Instructions | A | Form inputs without labels or `aria-label` |

**Scanner check IDs** (optional `checks` array in API bodies): `missing_alt`, `missing_aria`, `role_structure`, `heading_hierarchy`, `form_labels`. If omitted, all of the above run.

### Compliance Scoring

Each report includes simplified **Level A / AA / AAA** percentages derived from the current issue set, plus an overall **score** (higher is better—fewer detected issues).

---

## Quick Start

### Prerequisites

- Python 3.10+ recommended (3.8+ should work)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/scriptclean-a11y-guard.git
   cd scriptclean-a11y-guard
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r server/requirements.txt
   ```

4. **Configure environment (optional but needed for watsonx refinement)**
   ```bash
   copy server\.env.example server\.env
   # macOS/Linux: cp server/.env.example server/.env
   ```
   Edit `server/.env` and set at least `IBM_BOB_API_KEY` and `WATSONX_PROJECT_ID`. Never commit `.env` (it is gitignored).

5. **Start the server**
   ```bash
   python server/app.py
   ```

   The server listens on **`http://127.0.0.1:5050`** by default (`0.0.0.0` bind). On first run it creates **`uploads/`** and **`reports/`** if they are missing.

6. **Open the web interface**

   Use the same origin as the API (so asset URLs resolve correctly):

   **`http://127.0.0.1:5050/app/`**

   Avoid opening `client/index.html` as `file://` unless you use the default port **5050**; the client falls back to `http://127.0.0.1:5050` for API calls in that mode.

### Custom Port Configuration

Port **5000** is avoided by default (e.g. macOS AirPlay). Override with:

```powershell
# Windows PowerShell
$env:A11Y_GUARD_PORT="8080"
python server/app.py
```

```bash
# macOS/Linux
export A11Y_GUARD_PORT=8080
python server/app.py
```

If you change the port and use `file://` for the UI, update `DEFAULT_DEV_PORT` in `client/script.js` or always use `/app/` on the server.

---

## Usage

### 1. Upload Source Files

Drag and drop files into the upload zone, or type a **project-relative path** (see below).

**Typical extensions:** `.html`, `.php`, `.js` (samples list uses these; batch upload sends raw text for any dropped file).

### 2. Configure Scan Options

Toggle checks in the UI (they map to the `checks` IDs above).

### 3. Run the Scan

- **With uploaded files:** the client posts to **`/api/scan-batch`**.
- **With path only:** the client posts to **`/api/scan-file`** with `filename` (e.g. `bad_images.php` resolves under `text_samples/`, or use a path **inside the repo**).

### 4. Review Results

Use the **Report** tab for severity breakdown, issues, and Bob report metadata.

### 5. Apply Fixes

Use the UI actions to apply fixes; the client can request patched content via **`/api/apply-fixes`**.

### 6. Export Reports

**Export JSON Report** calls **`/api/export-report`**. The server writes `a11y_report_YYYYMMDD_HHMMSS.json` under **`reports/`** and returns JSON with `filename` and `path`. There is no PDF export in this repo—the deliverable is JSON.

### 7. Priority and “Ask Bob”

Use in-app actions that read `bob_report` / insights (priority fix, estimates, scores) from the last scan response.

---

## Project Structure

```
scriptclean-a11y-guard/
├── client/
│   ├── index.html          # Web interface
│   ├── script.js           # Client-side logic (API_BASE, batch vs path scan)
│   └── style.css           # IBM Carbon-oriented styles
├── server/
│   ├── app.py              # Flask API + scanner + static /app routes
│   ├── watsonx_bob.py      # watsonx IAM + text generation for fix refinement
│   ├── requirements.txt
│   ├── .env.example        # Template for keys (commit this)
│   └── .env                # Your secrets (gitignored — do not commit)
├── text_samples/           # Built-in sample files for demos
├── reports/                # Exported JSON reports (created at runtime)
├── uploads/                # Reserved for uploads (created at runtime)
└── README.md
```

---

## API Reference

### Root

```http
GET /
```

Returns JSON describing the service and endpoint map (same information as in `app.py`).

### Health Check

```http
GET /health
```

Example fields: `status`, `service`, `version`, `timestamp`, `ibm_bob_api_configured` (non-empty API key), `watsonx_ready` (key **and** `WATSONX_PROJECT_ID` set).

### Scan Code

```http
POST /api/scan
Content-Type: application/json

{
  "code": "<html>...</html>",
  "filename": "index.html",
  "checks": ["missing_alt", "missing_aria"]
}
```

`checks` is optional; omit to run all checks.

### Scan File (sample name or repo-relative path)

```http
POST /api/scan-file
Content-Type: application/json

{
  "filename": "bad_images.php",
  "checks": []
}
```

- Bare filename → resolved under **`text_samples/`**.
- Path → must stay inside the project root (directory traversal blocked).

### Scan Batch

```http
POST /api/scan-batch
Content-Type: application/json

{
  "files": [
    { "filename": "a.html", "code": "<html>...</html>" },
    { "filename": "b.php", "code": "<?php ..." }
  ],
  "checks": ["form_labels"]
}
```

### Apply Fixes

```http
POST /api/apply-fixes
Content-Type: application/json

{
  "files": [
    {
      "filename": "page.html",
      "content": "<html>...</html>",
      "issues": [ { "broken_full": "...", "fix": "..." } ]
    }
  ]
}
```

Returns `patched_files` with updated `content` and `applied_count`.

### List Samples

```http
GET /api/samples
```

Lists `.html`, `.php`, `.js` files in `text_samples/`.

### Export Report

```http
POST /api/export-report
Content-Type: application/json

{
  "report": { }
}
```

Persists JSON to **`reports/a11y_report_<timestamp>.json`** and returns `status`, `filename`, and server `path`.

---

## Testing with Sample Files

| File | Issues Demonstrated |
|------|-------------------|
| `bad_images.php` | Missing `alt` on images |
| `broken_nav.html` | Navigation / ARIA patterns |
| `Contact_form.html` | Form labeling |
| `dashboard_header.html` | Heading structure |
| `new_card.php`, `travello.html` | Additional demo content |

1. Start the server  
2. Open `http://127.0.0.1:5050/app/`  
3. Run a scan with default path (defaults to **`bad_images.php`**) or pick a sample name from **`GET /api/samples`**

---

## Design Philosophy: Double Diamond

ScriptClean was built using the **Double Diamond** methodology from Human-Computer Interaction (HCI):

### Diamond 1: Discover & Define
- **Research**: Developer and accessibility workflows  
- **Problem**: Manual audits are slow and generic fixes help little  
- **Insight**: Combine fast rules with optional LLM refinement for better fix text  

### Diamond 2: Develop & Deliver
- **Prototype**: Scanner + Flask API + Carbon-styled UI  
- **Test**: Sample corpus under `text_samples/`  
- **Iterate**: Batch scans, apply-fix pipeline, watsonx integration  
- **Launch**: Single-command local run for hackathon demos  

---

## Contributing

Contributions are welcome! Please open issues or pull requests.

### Development Setup

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/amazing-feature`)  
3. Make your changes  
4. Test with `python server/app.py` and `http://127.0.0.1:5050/app/`  
5. Commit and push  
6. Open a Pull Request  

---

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026 ScriptClean Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**Made with care for a more accessible web**

</div>
