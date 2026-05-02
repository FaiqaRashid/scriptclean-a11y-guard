**User:**

<task>
check why server not working ?
</task>
<environment_details>
# VSCode Visible Files
server\app.py

# VSCode Open Tabs
test_client.html,client/style.css,server/requirements.txt,README.md,server/app.py,client/script.js,client/index.html

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T10:06:53.300Z
User time zone: Asia/Karachi, UTC+5:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (d:/scriptclean_a11y_guard) Files
BUTTON_FIX_DOCUMENTATION.md
FIXES_APPLIED.md
PRIORITY_FIX_DOCUMENTATION.md
README.md
TESTING_GUIDE.md
client/
client/index.html
client/script.js
client/style.css
reports/
reports/a11y_report_20260501_222724.json
reports/a11y_report_20260501_222805.json
reports/a11y_report_20260501_223342.json
reports/a11y_report_20260501_224801.json
reports/a11y_report_20260502_114750.json
reports/a11y_report_20260502_120042.json
reports/a11y_report_20260502_125032.json
reports/a11y_report_20260502_130719.json
reports/a11y_report_20260502_131956.json
server/
server/app.py
server/requirements.txt
text_samples/
text_samples/bad_images.php
text_samples/broken_nav.html
text_samples/Contact_form.html
text_samples/dashboard_header.html
text_samples/new_card.php
text_samples/travello.html
uploads/
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll help you diagnose why the server is not working. Let me start by examining the server code and related files.

<read_file>
<args>
<file>
<path>server/app.py</path>
</file>
<file>
<path>server/requirements.txt</path>
</file>
<file>
<path>README.md</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'server/app.py', 'server/requirements.txt', 'README.md'] Result:
<files>
<file><path>server/app.py</path>
<content lines="1-581">
  1 | from flask import Flask, request, jsonify, send_from_directory
  2 | from flask_cors import CORS
  3 | import os
  4 | from pathlib import Path
  5 | import json
  6 | import re
  7 | from datetime import datetime
  8 | 
  9 | app = Flask(__name__)
 10 | CORS(app)  # Enable CORS for client communication
 11 | 
 12 | # ============================================================
 13 | # CROSS-PLATFORM PATH CONFIGURATION
 14 | # ============================================================
 15 | # Use pathlib for cross-platform compatibility (Windows/Mac/Linux)
 16 | BASE_DIR = Path(__file__).parent.parent.resolve()
 17 | SAMPLES_DIR = BASE_DIR / "text_samples"
 18 | UPLOADS_DIR = BASE_DIR / "uploads"
 19 | REPORTS_DIR = BASE_DIR / "reports"
 20 | 
 21 | # Create directories if they don't exist
 22 | UPLOADS_DIR.mkdir(exist_ok=True)
 23 | REPORTS_DIR.mkdir(exist_ok=True)
 24 | 
 25 | # ============================================================
 26 | # ACCESSIBILITY SCANNING ENGINE
 27 | # ============================================================
 28 | class A11yScanner:
 29 |     """
 30 |     Core accessibility scanner that analyzes HTML/PHP/JS files
 31 |     for WCAG 2.1 violations using regex patterns and context analysis.
 32 |     """
 33 |     
 34 |     def __init__(self):
 35 |         self.issues = []
 36 |         self.stats = {
 37 |             'critical': 0,
 38 |             'warning': 0,
 39 |             'info': 0,
 40 |             'files_scanned': 0
 41 |         }
 42 |     
 43 |     def scan_content(self, content, filename):
 44 |         """Scan file content for accessibility issues"""
 45 |         self.issues = []
 46 |         lines = content.split('\n')
 47 |         
 48 |         # Check for missing alt attributes on images
 49 |         self._check_missing_alt(lines, filename)
 50 |         
 51 |         # Check for missing ARIA labels on buttons/inputs
 52 |         self._check_missing_aria_labels(lines, filename)
 53 |         
 54 |         # Check for role and structure issues
 55 |         self._check_role_structure(lines, filename)
 56 |         
 57 |         # Check for heading hierarchy
 58 |         self._check_heading_hierarchy(lines, filename)
 59 |         
 60 |         # Check for form labels
 61 |         self._check_form_labels(lines, filename)
 62 |         
 63 |         self.stats['files_scanned'] += 1
 64 |         return self.issues
 65 |     
 66 |     def _check_missing_alt(self, lines, filename):
 67 |         """Check for images without alt attributes"""
 68 |         img_pattern = re.compile(r'<img\s+[^>]*?>', re.IGNORECASE)
 69 |         alt_pattern = re.compile(r'\balt\s*=', re.IGNORECASE)
 70 |         
 71 |         for i, line in enumerate(lines, 1):
 72 |             for match in img_pattern.finditer(line):
 73 |                 img_tag = match.group(0)
 74 |                 if not alt_pattern.search(img_tag):
 75 |                     # Extract src for context
 76 |                     src_match = re.search(r'src\s*=\s*["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
 77 |                     src = src_match.group(1) if src_match else 'unknown'
 78 |                     
 79 |                     self.issues.append({
 80 |                         'id': len(self.issues) + 1,
 81 |                         'severity': 'critical',
 82 |                         'type': 'Missing Alt Text',
 83 |                         'file': filename,
 84 |                         'line': i,
 85 |                         'desc': f'Image "{src}" has no alt attribute. Screen readers cannot convey this content to visually impaired users.',
 86 |                         'broken': img_tag.strip(),
 87 |                         'fix': self._generate_alt_fix(img_tag, src),
 88 |                         'wcag': 'WCAG 1.1.1',
 89 |                         'applied': False
 90 |                     })
 91 |                     self.stats['critical'] += 1
 92 |     
 93 |     def _generate_alt_fix(self, img_tag, src):
 94 |         """Generate contextual alt text fix"""
 95 |         # Smart alt text based on filename
 96 |         filename = Path(src).stem
 97 |         alt_text = filename.replace('-', ' ').replace('_', ' ').title()
 98 |         
 99 |         # Insert alt attribute before closing >
100 |         return img_tag[:-1] + f' alt="{alt_text}">'
101 |     
102 |     def _check_missing_aria_labels(self, lines, filename):
103 |         """Check for buttons/inputs without accessible labels"""
104 |         button_pattern = re.compile(r'<button[^>]*?>.*?</button>', re.IGNORECASE | re.DOTALL)
105 |         aria_pattern = re.compile(r'\baria-label\s*=', re.IGNORECASE)
106 |         
107 |         for i, line in enumerate(lines, 1):
108 |             # Check buttons with only icons (SVG)
109 |             for match in button_pattern.finditer(line):
110 |                 button = match.group(0)
111 |                 if '<svg' in button and not aria_pattern.search(button):
112 |                     # Extract onclick for context
113 |                     onclick_match = re.search(r'onclick\s*=\s*["\']([^"\']+)["\']', button)
114 |                     context = onclick_match.group(1) if onclick_match else 'action'
115 |                     
116 |                     self.issues.append({
117 |                         'id': len(self.issues) + 1,
118 |                         'severity': 'critical',
119 |                         'type': 'Missing ARIA Label',
120 |                         'file': filename,
121 |                         'line': i,
122 |                         'desc': f'Button with icon has no aria-label. Screen reader users cannot determine its purpose.',
123 |                         'broken': button[:80] + '...' if len(button) > 80 else button,
124 |                         'fix': self._generate_aria_fix(button, context),
125 |                         'wcag': 'WCAG 4.1.2',
126 |                         'applied': False
127 |                     })
128 |                     self.stats['critical'] += 1
129 |     
130 |     def _generate_aria_fix(self, element, context):
131 |         """Generate aria-label fix"""
132 |         label = context.replace('()', '').replace('open', 'Open').replace('close', 'Close')
133 |         return element.replace('<button', f'<button aria-label="{label}"', 1)
134 |     
135 |     def _check_role_structure(self, lines, filename):
136 |         """Check for proper landmark roles"""
137 |         content = '\n'.join(lines)
138 |         
139 |         # Check for main landmark
140 |         if '<main' not in content.lower() and 'role="main"' not in content.lower():
141 |             if '<div class="main' in content.lower() or '<div class="container' in content.lower():
142 |                 self.issues.append({
143 |                     'id': len(self.issues) + 1,
144 |                     'severity': 'warning',
145 |                     'type': 'Role & Structure',
146 |                     'file': filename,
147 |                     'line': 1,
148 |                     'desc': 'No <main> landmark found. Screen readers use landmarks to navigate page sections.',
149 |                     'broken': '<div class="main-content">',
150 |                     'fix': '<main class="main-content" role="main">',
151 |                     'wcag': 'WCAG 1.3.1',
152 |                     'applied': False
153 |                 })
154 |                 self.stats['warning'] += 1
155 |     
156 |     def _check_heading_hierarchy(self, lines, filename):
157 |         """Check for proper heading hierarchy"""
158 |         headings = []
159 |         for i, line in enumerate(lines, 1):
160 |             for level in range(1, 7):
161 |                 if f'<h{level}' in line.lower():
162 |                     headings.append((level, i))
163 |         
164 |         # Check for skipped levels
165 |         for i in range(len(headings) - 1):
166 |             current_level, current_line = headings[i]
167 |             next_level, next_line = headings[i + 1]
168 |             if next_level > current_level + 1:
169 |                 self.issues.append({
170 |                     'id': len(self.issues) + 1,
171 |                     'severity': 'warning',
172 |                     'type': 'Role & Structure',
173 |                     'file': filename,
174 |                     'line': next_line,
175 |                     'desc': f'Heading hierarchy jumps from H{current_level} to H{next_level}, skipping levels.',
176 |                     'broken': f'<h{next_level}>',
177 |                     'fix': f'<h{current_level + 1}>',
178 |                     'wcag': 'WCAG 2.4.6',
179 |                     'applied': False
180 |                 })
181 |                 self.stats['warning'] += 1
182 |                 break
183 |     
184 |     def _check_form_labels(self, lines, filename):
185 |         """Check for form inputs without labels"""
186 |         input_pattern = re.compile(r'<input[^>]*?>', re.IGNORECASE)
187 |         
188 |         for i, line in enumerate(lines, 1):
189 |             for match in input_pattern.finditer(line):
190 |                 input_tag = match.group(0)
191 |                 # Check if input has id but no aria-label
192 |                 if 'id=' in input_tag and 'aria-label' not in input_tag:
193 |                     # Check if there's a label in previous or same line
194 |                     context = '\n'.join(lines[max(0, i-2):i+1])
195 |                     if '<label' not in context.lower():
196 |                         input_type = re.search(r'type\s*=\s*["\']([^"\']+)["\']', input_tag)
197 |                         type_val = input_type.group(1) if input_type else 'text'
198 |                         
199 |                         self.issues.append({
200 |                             'id': len(self.issues) + 1,
201 |                             'severity': 'critical',
202 |                             'type': 'Missing ARIA Label',
203 |                             'file': filename,
204 |                             'line': i,
205 |                             'desc': f'Input field ({type_val}) has no associated label or aria-label.',
206 |                             'broken': input_tag.strip(),
207 |                             'fix': input_tag.replace('<input', f'<input aria-label="{type_val.title()} input"', 1),
208 |                             'wcag': 'WCAG 4.1.2',
209 |                             'applied': False
210 |                         })
211 |                         self.stats['critical'] += 1
212 | 
213 | # ============================================================
214 | # API ENDPOINTS
215 | # ============================================================
216 | 
217 | @app.route('/api/scan', methods=['POST'])
218 | def scan_code():
219 |     """
220 |     Main scanning endpoint - receives code and returns accessibility issues
221 |     Integrates with IBM Bob for enhanced reporting
222 |     """
223 |     try:
224 |         data = request.get_json()
225 |         if not data:
226 |             return jsonify({
227 |                 'status': 'error',
228 |                 'message': 'Invalid JSON data'
229 |             }), 400
230 |         
231 |         code = data.get('code', '')
232 |         filename = data.get('filename', 'uploaded_file.html')
233 |         
234 |         if not code:
235 |             return jsonify({
236 |                 'status': 'error',
237 |                 'message': 'No code provided'
238 |             }), 400
239 |         
240 |         # Initialize scanner
241 |         scanner = A11yScanner()
242 |         issues = scanner.scan_content(code, filename)
243 |         
244 |         # Generate IBM Bob report
245 |         bob_report = generate_bob_report(issues, scanner.stats, filename)
246 |         
247 |         return jsonify({
248 |             'status': 'success',
249 |             'issues': issues,
250 |             'stats': scanner.stats,
251 |             'bob_report': bob_report,
252 |             'timestamp': datetime.now().isoformat()
253 |         })
254 |         
255 |     except Exception as e:
256 |         # IBM Bob error reporting integration
257 |         return jsonify({
258 |             'status': 'error',
259 |             'message': str(e),
260 |             'bob_report': {
261 |                 'error': True,
262 |                 'details': f'Scan failed: {str(e)}'
263 |             }
264 |         }), 500
265 | 
266 | @app.route('/api/scan-file', methods=['POST'])
267 | def scan_file():
268 |     """
269 |     Scan a file from the test_samples directory or custom path
270 |     Cross-platform path handling with dynamic file selection
271 |     """
272 |     try:
273 |         data = request.get_json()
274 |         if not data:
275 |             return jsonify({
276 |                 'status': 'error',
277 |                 'message': 'Invalid JSON data'
278 |             }), 400
279 |         
280 |         filename = data.get('filename', '')
281 |         
282 |         if not filename:
283 |             return jsonify({
284 |                 'status': 'error',
285 |                 'message': 'No filename provided'
286 |             }), 400
287 |         
288 |         # Check if it's a full path or just a filename
289 |         file_path = Path(filename)
290 |         
291 |         # If it's just a filename (no directory separators), look in test-samples
292 |         if file_path.name == filename:
293 |             # Secure path handling - prevent directory traversal
294 |             safe_filename = file_path.name
295 |             file_path = SAMPLES_DIR / safe_filename
296 |         else:
297 |             # It's a path - resolve it relative to base directory
298 |             # Security: Only allow paths within the project directory
299 |             try:
300 |                 file_path = file_path.resolve()
301 |                 # Check if path is within allowed directories
302 |                 if not (str(file_path).startswith(str(BASE_DIR)) or
303 |                         str(file_path).startswith(str(SAMPLES_DIR))):
304 |                     return jsonify({
305 |                         'status': 'error',
306 |                         'message': 'Access denied: Path outside project directory'
307 |                     }), 403
308 |             except Exception:
309 |                 return jsonify({
310 |                     'status': 'error',
311 |                     'message': 'Invalid file path'
312 |                 }), 400
313 |         
314 |         if not file_path.exists():
315 |             # Try to find the file in test_samples
316 |             alt_path = SAMPLES_DIR / Path(filename).name
317 |             if alt_path.exists():
318 |                 file_path = alt_path
319 |             else:
320 |                 return jsonify({
321 |                     'status': 'error',
322 |                     'message': f'File not found: {filename}',
323 |                     'hint': f'Available files in test_samples: {[f.name for f in SAMPLES_DIR.glob("*.*") if f.is_file()]}'
324 |                 }), 404
325 |         
326 |         # Read file content
327 |         with open(file_path, 'r', encoding='utf-8') as f:
328 |             code = f.read()
329 |         
330 |         # Scan the content
331 |         scanner = A11yScanner()
332 |         issues = scanner.scan_content(code, file_path.name)
333 |         
334 |         # Generate IBM Bob report
335 |         bob_report = generate_bob_report(issues, scanner.stats, file_path.name)
336 |         
337 |         return jsonify({
338 |             'status': 'success',
339 |             'issues': issues,
340 |             'stats': scanner.stats,
341 |             'bob_report': bob_report,
342 |             'filename': file_path.name,
343 |             'full_path': str(file_path),
344 |             'timestamp': datetime.now().isoformat()
345 |         })
346 |         
347 |     except Exception as e:
348 |         return jsonify({
349 |             'status': 'error',
350 |             'message': str(e),
351 |             'bob_report': {
352 |                 'error': True,
353 |                 'details': f'File scan failed: {str(e)}'
354 |             }
355 |         }), 500
356 | 
357 | @app.route('/api/samples', methods=['GET'])
358 | def list_samples():
359 |     """
360 |     List available test sample files
361 |     Cross-platform directory listing
362 |     """
363 |     try:
364 |         samples = []
365 |         if SAMPLES_DIR.exists():
366 |             for file_path in SAMPLES_DIR.iterdir():
367 |                 if file_path.is_file() and file_path.suffix in ['.html', '.php', '.js']:
368 |                     samples.append({
369 |                         'name': file_path.name,
370 |                         'size': file_path.stat().st_size,
371 |                         'extension': file_path.suffix
372 |                     })
373 |         
374 |         return jsonify({
375 |             'status': 'success',
376 |             'samples': samples,
377 |             'count': len(samples)
378 |         })
379 |         
380 |     except Exception as e:
381 |         return jsonify({
382 |             'status': 'error',
383 |             'message': str(e)
384 |         }), 500
385 | 
386 | @app.route('/api/export-report', methods=['POST'])
387 | def export_report():
388 |     """
389 |     Export IBM Bob accessibility report as JSON
390 |     """
391 |     try:
392 |         data = request.get_json()
393 |         if not data:
394 |             return jsonify({
395 |                 'status': 'error',
396 |                 'message': 'Invalid JSON data'
397 |             }), 400
398 |         
399 |         report_data = data.get('report', {})
400 |         
401 |         # Generate unique filename
402 |         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
403 |         report_filename = f'a11y_report_{timestamp}.json'
404 |         report_path = REPORTS_DIR / report_filename
405 |         
406 |         # Save report
407 |         with open(report_path, 'w', encoding='utf-8') as f:
408 |             json.dump(report_data, f, indent=2)
409 |         
410 |         return jsonify({
411 |             'status': 'success',
412 |             'filename': report_filename,
413 |             'path': str(report_path)
414 |         })
415 |         
416 |     except Exception as e:
417 |         return jsonify({
418 |             'status': 'error',
419 |             'message': str(e)
420 |         }), 500
421 | 
422 | # ============================================================
423 | # IBM BOB REPORTING INTEGRATION
424 | # ============================================================
425 | 
426 | def generate_bob_report(issues, stats, filename):
427 |     """
428 |     Generate comprehensive IBM Bob accessibility report
429 |     This integrates Bob's AI-powered insights into the error handling
430 |     """
431 |     report = {
432 |         'tool': 'ScriptClean A11y Guard',
433 |         'powered_by': 'IBM Bob',
434 |         'scan_date': datetime.now().isoformat(),
435 |         'file_analyzed': filename,
436 |         'summary': {
437 |             'total_issues': len(issues),
438 |             'critical': stats['critical'],
439 |             'warning': stats['warning'],
440 |             'info': stats['info'],
441 |             'files_scanned': stats['files_scanned']
442 |         },
443 |         'wcag_compliance': {
444 |             'level_a': calculate_wcag_compliance(issues, 'A'),
445 |             'level_aa': calculate_wcag_compliance(issues, 'AA'),
446 |             'level_aaa': calculate_wcag_compliance(issues, 'AAA')
447 |         },
448 |         'issues': issues,
449 |         'recommendations': generate_recommendations(issues),
450 |         'bob_insights': {
451 |             'priority_fix': get_priority_fix(issues),
452 |             'reason': get_priority_reason(issues),
453 |             'impact_score': calculate_impact_score(stats),
454 |             'estimated_fix_time': estimate_fix_time(issues)
455 |         }
456 |     }
457 |     
458 |     return report
459 | 
460 | def calculate_wcag_compliance(issues, level):
461 |     """Calculate WCAG compliance percentage"""
462 |     # Simplified calculation - in production, this would be more sophisticated
463 |     total_checks = 20  # Total WCAG criteria checked
464 |     failed_checks = len([i for i in issues if level in i.get('wcag', '')])
465 |     compliance = ((total_checks - failed_checks) / total_checks) * 100
466 |     return round(compliance, 1)
467 | 
468 | def generate_recommendations(issues):
469 |     """Generate prioritized recommendations"""
470 |     recommendations = []
471 |     
472 |     critical_count = len([i for i in issues if i['severity'] == 'critical'])
473 |     if critical_count > 0:
474 |         recommendations.append({
475 |             'priority': 'HIGH',
476 |             'action': f'Fix {critical_count} critical accessibility issues immediately',
477 |             'impact': 'These issues prevent users with disabilities from accessing content'
478 |         })
479 |     
480 |     warning_count = len([i for i in issues if i['severity'] == 'warning'])
481 |     if warning_count > 0:
482 |         recommendations.append({
483 |             'priority': 'MEDIUM',
484 |             'action': f'Address {warning_count} warning-level issues',
485 |             'impact': 'These issues create barriers but have workarounds'
486 |         })
487 |     
488 |     return recommendations
489 | 
490 | def get_priority_fix(issues):
491 |     """Identify the most critical fix to apply first"""
492 |     critical_issues = [i for i in issues if i['severity'] == 'critical']
493 |     if critical_issues:
494 |         # Return the full priority issue object with all details
495 |         priority_issue = critical_issues[0]
496 |         return {
497 |             'issue': priority_issue['type'],
498 |             'file': priority_issue['file'],
499 |             'line': priority_issue['line'],
500 |             'wcag': priority_issue['wcag'],
501 |             'description': priority_issue['desc'],
502 |             'broken': priority_issue['broken'],
503 |             'fix': priority_issue['fix']
504 |         }
505 |     return None
506 | 
507 | def get_priority_reason(issues):
508 |     """Get the reason why this is the priority fix"""
509 |     critical_issues = [i for i in issues if i['severity'] == 'critical']
510 |     if critical_issues:
511 |         return 'This issue has the highest impact on accessibility and prevents users with disabilities from accessing content.'
512 |     return None
513 | 
514 | def estimate_fix_time(issues):
515 |     """Estimate time to fix all issues"""
516 |     # Rough estimate: 5 min per critical, 3 min per warning, 1 min per info
517 |     time_map = {'critical': 5, 'warning': 3, 'info': 1}
518 |     total_minutes = sum(time_map.get(i['severity'], 1) for i in issues)
519 |     
520 |     if total_minutes < 60:
521 |         return f"{total_minutes} minutes"
522 |     else:
523 |         hours = total_minutes / 60
524 |         return f"{hours:.1f} hours saved"
525 | 
526 | def calculate_impact_score(stats):
527 |     """Calculate overall accessibility impact score (0-100)"""
528 |     # Higher score = worse accessibility
529 |     score = (stats['critical'] * 10) + (stats['warning'] * 5) + (stats['info'] * 1)
530 |     return min(score, 100)
531 | 
532 | # ============================================================
533 | # HEALTH CHECK & STATIC FILES
534 | # ============================================================
535 | 
536 | @app.route('/health', methods=['GET'])
537 | def health_check():
538 |     """Health check endpoint for monitoring"""
539 |     return jsonify({
540 |         'status': 'healthy',
541 |         'service': 'ScriptClean A11y Guard API',
542 |         'version': '1.0.0',
543 |         'timestamp': datetime.now().isoformat()
544 |     })
545 | 
546 | @app.route('/')
547 | def index():
548 |     """Serve API documentation"""
549 |     return jsonify({
550 |         'service': 'ScriptClean A11y Guard API',
551 |         'version': '1.0.0',
552 |         'endpoints': {
553 |             '/api/scan': 'POST - Scan code for accessibility issues',
554 |             '/api/scan-file': 'POST - Scan a file from test_samples',
555 |             '/api/samples': 'GET - List available test samples',
556 |             '/api/export-report': 'POST - Export accessibility report',
557 |             '/health': 'GET - Health check'
558 |         },
559 |         'powered_by': 'IBM Bob'
560 |     })
561 | 
562 | # ============================================================
563 | # SERVER STARTUP
564 | # ============================================================
565 | 
566 | if __name__ == '__main__':
567 |     print("=" * 60)
568 |     print("ScriptClean A11y Guard Server")
569 |     print("Powered by IBM Bob")
570 |     print("=" * 60)
571 |     print(f"Base Directory: {BASE_DIR}")
572 |     print(f"Samples Directory: {SAMPLES_DIR}")
573 |     print(f"Uploads Directory: {UPLOADS_DIR}")
574 |     print(f"Reports Directory: {REPORTS_DIR}")
575 |     print("=" * 60)
576 |     print("Server starting on http://localhost:5000")
577 |     print("=" * 60)
578 |     
579 |     app.run(debug=True, port=5000, host='0.0.0.0')
580 | 
581 | # Made with Bob
</content>
</file>
<file><path>server/requirements.txt</path>
<content lines="1-16">
 1 | # ScriptClean A11y Guard - Python Dependencies
 2 | # Install with: pip install -r requirements.txt
 3 | 
 4 | # Core Web Framework
 5 | Flask==3.1.3
 6 | flask-cors==6.0.2
 7 | 
 8 | # WSGI Server (for production deployment)
 9 | Werkzeug==3.1.3
10 | 
11 | # Additional utilities (already included with Flask but listed for clarity)
12 | click>=8.1.3
13 | itsdangerous>=2.2.0
14 | Jinja2>=3.1.2
15 | MarkupSafe>=2.1.5
16 | blinker>=1.9.0
</content>
</file>
<file><path>README.md</path>
<content lines="1-646">
  1 | # ScriptClean: A11y Guard ♿
  2 | 
  3 | > **Bridging the Digital Divide with AI-Driven Inclusive Design.**  
  4 | > **Saving developers 15+ hours per project while making the web accessible to 1.3 billion people with disabilities.**
  5 | 
  6 | [![IBM Bob](https://img.shields.io/badge/Powered%20by-IBM%20Bob-0f62fe?style=flat-square)](https://www.ibm.com/)
  7 | [![WCAG 2.1](https://img.shields.io/badge/Standard-WCAG%202.1-198038?style=flat-square)](https://www.w3.org/WAI/WCAG21/quickref/)
  8 | [![License](https://img.shields.io/badge/License-MIT-e0e0e0?style=flat-square)](LICENSE)
  9 | [![Hackathon](https://img.shields.io/badge/IBM%20Bob-Hackathon%202026-da1e28?style=flat-square)](https://watsonx-challenge.ibm.com/)
 10 | 
 11 | ---
 12 | 
 13 | ## 🎯 The Impact
 14 | 
 15 | **ScriptClean transforms accessibility from a 40-hour manual audit into a 2-hour automated fix.**
 16 | 
 17 | ### By the Numbers
 18 | 
 19 | | Metric | Manual Audit | ScriptClean | Time Saved |
 20 | |--------|--------------|-------------|------------|
 21 | | Initial scan | 8-12 hours | 2 minutes | **99.7%** |
 22 | | Issue identification | 6-8 hours | Instant | **100%** |
 23 | | Fix generation | 12-16 hours | Automated | **95%** |
 24 | | Documentation | 4-6 hours | 1-click export | **98%** |
 25 | | **Total per project** | **30-42 hours** | **2-3 hours** | **~15-20 hours** |
 26 | 
 27 | **Business Value:** At $75/hour developer rate, ScriptClean saves **$1,125-$1,500 per project**.
 28 | 
 29 | **Global Impact:** With 1.3 billion people living with disabilities (WHO, 2023), every website made accessible through ScriptClean potentially serves 16% more users — translating to real revenue growth and legal compliance.
 30 | 
 31 | ---
 32 | 
 33 | ## 💡 What is ScriptClean?
 34 | 
 35 | ScriptClean: A11y Guard is an **AI-powered Accessibility (A11y) Auditor** built on IBM Bob that scans web source code — HTML, PHP, and JavaScript — and automatically identifies barriers that prevent people with visual, auditory, motor, and cognitive impairments from using the web.
 36 | 
 37 | **The difference?** ScriptClean doesn't just flag issues — it **understands context** and generates **meaningful, human-readable fixes** that developers can apply with one click.
 38 | 
 39 | ### 🚨 The Problem (Quantified)
 40 | 
 41 | - **96.3%** of the top 1 million websites have detectable WCAG failures *(WebAIM Million, 2024)*
 42 | - The average homepage has **56 distinct accessibility errors** *(WebAIM, 2024)*
 43 | - **71%** of users with disabilities leave a website immediately if it's not accessible *(Click-Away Pound Survey, 2019)*
 44 | - Missing `alt` text (58.2%) and absent ARIA labels (50.1%) are the **#1 and #2** most common violations
 45 | - **$6.9 billion** in legal settlements paid by companies for ADA violations in 2023 *(UsableNet, 2024)*
 46 | 
 47 | **Developer Pain Points:**
 48 | - Existing tools flag issues without explaining *why* or *how* to fix them
 49 | - Manual audits require specialist knowledge (WCAG 2.1 has 78 success criteria)
 50 | - Generic fixes like `alt="image"` fail accessibility standards
 51 | - No integration with development workflow
 52 | 
 53 | ### ✅ The Solution (How ScriptClean Solves It)
 54 | 
 55 | ScriptClean uses IBM Bob's repository-wide context engine to:
 56 | 
 57 | 1. **Understand** what the element actually does (not just what tag it is)
 58 | 2. **Suggest** descriptive, context-aware fixes (`alt="Company logo linking to homepage"` — not `alt="image"`)
 59 | 3. **Prioritize** issues by impact (Critical → Warning → Info) with WCAG criterion mapping
 60 | 4. **Apply** fixes with one click, directly in the interface
 61 | 5. **Report** full WCAG 2.1 compliance coverage for teams, clients, and legal documentation
 62 | 
 63 | **Result:** Developers without accessibility expertise can achieve WCAG 2.1 Level AA compliance in hours, not weeks.
 64 | 
 65 | ---
 66 | 
 67 | ## 🎬 See It In Action
 68 | 
 69 | **Suggested GIF Placements:**
 70 | 1. **Hero GIF** (right after this section): Show drag-and-drop → scan → issues appear → one-click fix applied
 71 | 2. **Bob Priority Modal GIF** (in Features section): Show clicking "Ask Bob for priority" → modal appears with metrics
 72 | 3. **Side-by-Side Diff GIF** (in How It Works section): Show broken code transforming into Bob's fix
 73 | 
 74 | ---
 75 | 
 76 | ## ✨ Features
 77 | 
 78 | ### Core Capabilities
 79 | - **🎯 Drag-and-drop file upload** — scan HTML, PHP, JS, JSX, and TS files instantly
 80 | - **🤖 IBM Bob AI analysis** — full repository context, not regex pattern matching
 81 | - **📊 Severity classification** — Critical / Warning / Info, mapped to WCAG 2.1 criteria
 82 | - **🔍 Side-by-side diff view** — broken code vs. Bob's suggested fix with syntax highlighting
 83 | - **⚡ One-click Apply** — fix issues without leaving the dashboard (saves 12+ hours per project)
 84 | - **📋 WCAG 2.1 coverage** — criteria 1.1.1, 1.3.1, 2.1.1, 2.4.6, 4.1.2 (Level A & AA)
 85 | - **📄 Export report** — shareable JSON compliance report for clients, auditors, or legal teams
 86 | - **🎯 Bob Priority Recommendation** — AI-powered prioritization shows which issue to fix first and why
 87 | 
 88 | ### 🎯 How to Use "Ask Bob for Priority" Button
 89 | 
 90 | The **"Ask Bob for priority"** button helps you decide which accessibility issue to fix first:
 91 | 
 92 | **Steps:**
 93 | 1. Run a scan on your code files
 94 | 2. Wait for results to appear in the **Report** tab
 95 | 3. Scroll down and click **"Ask Bob for priority ↗"** button
 96 | 4. A modal will appear showing:
 97 |    - **Priority Fix**: The most critical issue to address
 98 |    - **File & Line**: Exact location of the issue
 99 |    - **Reason**: Why this issue should be fixed first
100 |    - **Estimated Fix Time**: Total time to fix all issues
101 |    - **Impact Score**: Severity rating (0-100)
102 |    - **WCAG Compliance**: Current compliance percentages
103 | 
104 | **Example:**
105 | ```
106 | 🤖 Bob's Priority Recommendation
107 | Fix this issue first for maximum impact
108 | 
109 | PRIORITY FIX: Missing Alt Text
110 | 📄 bad_images.php : Line 45
111 | Reason: This issue has the highest impact on accessibility
112 | 
113 | ESTIMATED FIX TIME: 35 minutes
114 | IMPACT SCORE: 75/100
115 | 
116 | WCAG COMPLIANCE
117 | Level A: 65% • Level AA: 70% • Level AAA: 80%
118 | ```
119 | 
120 | 5. Click **"Got it, let's fix this!"** to close the modal
121 | 6. The page will scroll to the priority issue automatically
122 | 7. Expand the issue card and click **"Apply Fix"**
123 | 
124 | **Note:** The button only works after running a scan. If you see a warning message, make sure you've completed a scan first.
125 | 
126 | ### What Makes ScriptClean Different
127 | 
128 | | Feature | Traditional Tools | ScriptClean |
129 | |---------|------------------|-------------|
130 | | Context awareness | ❌ Pattern matching only | ✅ Full codebase understanding |
131 | | Fix quality | ❌ Generic placeholders | ✅ Meaningful, descriptive fixes |
132 | | Developer experience | ❌ Copy-paste from report | ✅ One-click apply in UI |
133 | | Learning curve | ❌ Requires WCAG expertise | ✅ Plain-English explanations |
134 | | Time to compliance | ❌ 30-40 hours | ✅ 2-3 hours |
135 | | Cost per project | ❌ $2,250-$3,000 | ✅ $150-$225 |
136 | 
137 | ---
138 | 
139 | ## 🏗️ Tech Stack
140 | 
141 | | Layer | Technology | Why We Chose It |
142 | |---|---|---|
143 | | Frontend | HTML5 · CSS3 · Vanilla JS | Zero dependencies, instant load time |
144 | | Backend | Python 3.11 · Flask | Lightweight, perfect for AI integration |
145 | | AI Engine | IBM Bob (watsonx) | Repository-wide context understanding |
146 | | Design | IBM Carbon Design System | Accessible by design, professional UI |
147 | | Methodology | Double Diamond (HCI) | User-centered design process |
148 | 
149 | ---
150 | 
151 | ## 📁 Project Structure
152 | 
153 | ```
154 | scriptclean-a11y-guard/
155 | ├── client/
156 | │   ├── index.html          # Main dashboard UI (162 lines)
157 | │   ├── style.css           # IBM Carbon-inspired styles (290 lines)
158 | │   └── script.js           # Frontend logic & API calls (475 lines)
159 | ├── server/
160 | │   ├── app.py              # Flask server + IBM Bob integration (540 lines)
161 | │   └── requirements.txt    # Python dependencies
162 | ├── text_samples/           # Demo files with intentional violations
163 | │   ├── broken_nav.html     # Missing alt text & ARIA on navigation
164 | │   ├── bad_images.php      # Inaccessible images & buttons (323 lines)
165 | │   └── travello.html       # Travel site with contrast issues
166 | ├── reports/                # Auto-generated compliance reports
167 | ├── uploads/                # User-uploaded files (temporary storage)
168 | └── README.md
169 | ```
170 | 
171 | **Total Lines of Code:** ~1,790 (excluding test samples)
172 | 
173 | ---
174 | 
175 | ## 🚀 Getting Started
176 | 
177 | ### Prerequisites
178 | 
179 | - Python 3.9+
180 | - Modern web browser (Chrome, Firefox, Safari, Edge)
181 | - IBM Bob API credentials (provided during hackathon)
182 | 
183 | ### 1. Clone the repository
184 | 
185 | ```bash
186 | git clone https://github.com/YOUR_USERNAME/scriptclean-a11y-guard.git
187 | cd scriptclean-a11y-guard
188 | ```
189 | 
190 | ### 2. Set up the backend
191 | 
192 | ```bash
193 | cd server
194 | pip install -r requirements.txt
195 | ```
196 | 
197 | Create a `.env` file in `/server`:
198 | 
199 | ```env
200 | IBM_BOB_API_KEY=your_api_key_here
201 | IBM_BOB_PROJECT_ID=your_project_id_here
202 | IBM_BOB_BASE_URL=https://your-bob-instance.ibm.com
203 | ```
204 | 
205 | ### 3. Run the server
206 | 
207 | ```bash
208 | python app.py
209 | ```
210 | 
211 | The server starts at `http://localhost:5000`.
212 | 
213 | ### 4. Open the frontend
214 | 
215 | Open `client/index.html` directly in your browser, or serve it:
216 | 
217 | ```bash
218 | cd client
219 | python -m http.server 8080
220 | # then visit http://localhost:8080
221 | ```
222 | 
223 | ### 5. Test with sample files
224 | 
225 | Drop the files from `text_samples/` into the dashboard to see ScriptClean in action. These files contain **intentional** accessibility violations for demonstration purposes.
226 | 
227 | **Try this workflow:**
228 | 1. Drag `bad_images.php` into the upload zone
229 | 2. Watch Bob analyze 323 lines of code in ~2 seconds
230 | 3. See 11 issues identified (7 critical, 4 warnings)
231 | 4. Click "Ask Bob for priority" to see AI-powered prioritization
232 | 5. Expand an issue to see side-by-side diff
233 | 6. Click "Apply Fix" to resolve the issue
234 | 7. Export the compliance report
235 | 
236 | ---
237 | 
238 | ## 🤖 How IBM Bob Powers This
239 | 
240 | When you upload a file, ScriptClean sends it to IBM Bob with a carefully engineered prompt that leverages Bob's **repository-wide context understanding**:
241 | 
242 | ```
243 | You are a Senior Accessibility Engineer and WCAG 2.1 expert.
244 | 
245 | Analyze the following source code and identify ALL accessibility violations.
246 | For each violation, return a JSON object with:
247 |   - line: line number of the violation
248 |   - severity: "critical" | "warning" | "info"
249 |   - type: "Missing Alt Text" | "Missing ARIA Label" | "Role & Structure"
250 |   - wcag: the WCAG criterion (e.g. "WCAG 1.1.1")
251 |   - description: a plain-English explanation of WHY this is a barrier
252 |   - broken_code: the exact broken snippet
253 |   - fixed_code: a corrected version with a MEANINGFUL, context-aware fix
254 | 
255 | CRITICAL: Do not use placeholder values like alt="image". Read the surrounding
256 | code to understand context and generate a descriptive, human-readable fix.
257 | 
258 | Example:
259 | - BAD: alt="image"
260 | - GOOD: alt="Company logo linking to homepage"
261 | 
262 | SOURCE CODE:
263 | [file contents here]
264 | ```
265 | 
266 | **Why This Works:**
267 | 
268 | 1. **Context Awareness:** Bob reads the entire file, not just the problematic line
269 | 2. **Semantic Understanding:** Bob understands what a "logo" or "navigation menu" is
270 | 3. **Human-Readable Output:** Fixes are written for developers, not machines
271 | 4. **WCAG Mapping:** Every issue is tied to a specific WCAG 2.1 success criterion
272 | 
273 | Bob's response is parsed into structured issue cards and rendered in the dashboard — complete with the broken code, the fix, and a one-click apply button.
274 | 
275 | ---
276 | 
277 | ## 📊 WCAG 2.1 Coverage
278 | 
279 | ScriptClean checks for the **5 most common accessibility violations** that account for **78% of all WCAG failures**:
280 | 
281 | | Criterion | Level | What ScriptClean checks | Failure Rate* |
282 | |---|---|---|---|
283 | | 1.1.1 Non-text Content | A | All images have meaningful alt attributes | 58.2% |
284 | | 4.1.2 Name, Role, Value | A | ARIA labels on all controls and widgets | 50.1% |
285 | | 1.3.1 Info & Relationships | A | Semantic structure and landmark roles | 47.6% |
286 | | 2.4.6 Headings & Labels | AA | Heading hierarchy and label accuracy | 38.4% |
287 | | 2.1.1 Keyboard Accessible | A | Interactive elements are keyboard-focusable | 28.7% |
288 | 
289 | *Source: WebAIM Million Report, 2024
290 | 
291 | **Compliance Guarantee:** Projects scanned and fixed with ScriptClean achieve **WCAG 2.1 Level AA compliance** for the covered criteria.
292 | 
293 | ---
294 | 
295 | ## 🎨 Design Philosophy: The Double Diamond
296 | 
297 | ScriptClean was designed using the **Double Diamond** framework (British Design Council) — a human-centered design process that ensures we're solving the *right* problem in the *right* way.
298 | 
299 | ### 💎 Diamond 1: Discover & Define
300 | 
301 | #### Discover Phase (Problem Space)
302 | We conducted research with 15 web developers and 8 accessibility specialists to understand the current state of accessibility auditing:
303 | 
304 | **Key Findings:**
305 | - 87% of developers skip accessibility checks due to time constraints
306 | - 73% find existing tools "too technical" or "unhelpful"
307 | - 92% want fixes, not just error reports
308 | - Average time to manually audit a 10-page site: **32 hours**
309 | - Most common complaint: *"Tools tell me what's broken, never how to fix it meaningfully"*
310 | 
311 | **User Pain Points Identified:**
312 | 1. **Cognitive Load:** WCAG 2.1 has 78 success criteria — too much to memorize
313 | 2. **Generic Fixes:** Tools suggest `alt="image"` which fails accessibility standards
314 | 3. **No Context:** Developers don't understand *why* something is a barrier
315 | 4. **Workflow Friction:** Copy-pasting fixes from reports is tedious
316 | 5. **No Prioritization:** Which issue should I fix first?
317 | 
318 | #### Define Phase (Problem Statement)
319 | After synthesizing our research, we defined the core problem:
320 | 
321 | > **"Developers want to build accessible websites, but existing tools create more friction than they remove. They need a solution that understands context, explains the 'why,' and makes fixing issues as easy as clicking a button."**
322 | 
323 | **Design Principles Established:**
324 | 1. **Zero Learning Curve:** No WCAG expertise required
325 | 2. **Context is King:** Fixes must be meaningful, not generic
326 | 3. **One-Click Everything:** Minimize steps to resolution
327 | 4. **Explain the Why:** Every issue includes plain-English reasoning
328 | 5. **Prioritize by Impact:** Show what matters most
329 | 
330 | ### 💎 Diamond 2: Develop & Deliver
331 | 
332 | #### Develop Phase (Solution Space)
333 | Based on our defined problem, we prototyped three key features:
334 | 
335 | **1. One-Click Apply Feature**
336 | - **Why:** Developers cited "copy-paste friction" as the #1 reason they abandon fixes
337 | - **How:** IBM Bob generates the fix → ScriptClean displays it in a diff view → One button applies it
338 | - **Impact:** Reduces fix application time from 5-10 minutes per issue to **5 seconds**
339 | 
340 | **2. Bob Priority Recommendation**
341 | - **Why:** Developers asked "Which issue should I fix first?"
342 | - **How:** Bob analyzes impact score, WCAG level, and user experience to recommend priority
343 | - **Impact:** Eliminates decision paralysis, focuses effort on high-impact fixes
344 | 
345 | **3. Side-by-Side Diff View**
346 | - **Why:** Developers need to see *what changed* before applying a fix
347 | - **How:** Broken code (left) vs. Bob's fix (right) with syntax highlighting
348 | - **Impact:** Builds trust, enables learning, reduces errors
349 | 
350 | #### Deliver Phase (Validation)
351 | We tested ScriptClean with 5 developers (3 junior, 2 senior) on real projects:
352 | 
353 | **Results:**
354 | - **100%** successfully achieved WCAG 2.1 Level AA compliance
355 | - **Average time to fix 10 issues:** 12 minutes (vs. 2-3 hours manually)
356 | - **User satisfaction:** 4.8/5.0
357 | - **Most common feedback:** *"I finally understand why accessibility matters"*
358 | 
359 | **Key Insight:** The "One-Click Apply" feature wasn't just about speed — it was about **removing the psychological barrier** to fixing accessibility issues. When fixes are instant, developers are more likely to care about accessibility.
360 | 
361 | ---
362 | 
363 | ## 🔮 Future Vision: Scaling Impact
364 | 
365 | ### Phase 1: Developer Workflow Integration (Q3 2026)
366 | 
367 | **GitHub Action**
368 | ```yaml
369 | name: ScriptClean A11y Check
370 | on: [push, pull_request]
371 | jobs:
372 |   accessibility:
373 |     runs-on: ubuntu-latest
374 |     steps:
375 |       - uses: actions/checkout@v2
376 |       - uses: scriptclean/a11y-action@v1
377 |         with:
378 |           fail-on: critical
379 |           auto-fix: true
380 | ```
381 | 
382 | **Impact:** Catch accessibility issues *before* they reach production. Estimated to prevent **90% of WCAG violations** from being deployed.
383 | 
384 | **VS Code Extension**
385 | - Real-time accessibility linting as you type
386 | - Inline fix suggestions with Cmd+. quick actions
387 | - WCAG criterion tooltips on hover
388 | - Accessibility score in status bar
389 | 
390 | **Impact:** Shift accessibility "left" in the development process. Developers fix issues in **seconds**, not hours.
391 | 
392 | ### Phase 2: Mobile & Framework Support (Q4 2026)
393 | 
394 | **React Native & Flutter Support**
395 | - Scan mobile app code for accessibility barriers
396 | - Check for proper screen reader labels
397 | - Validate touch target sizes (minimum 44x44pt)
398 | - Test color contrast ratios
399 | 
400 | **Impact:** Extend accessibility to the **6.8 billion smartphone users** worldwide.
401 | 
402 | **Framework-Specific Fixes**
403 | - React: Generate accessible component patterns
404 | - Vue: Suggest v-bind:aria-label directives
405 | - Angular: Recommend Material Design a11y components
406 | 
407 | **Impact:** Reduce framework-specific accessibility learning curve by **80%**.
408 | 
409 | ### Phase 3: Compliance Automation (Q1 2027)
410 | 
411 | **Auto-Generated Accessibility Statements**
412 | ```
413 | ScriptClean analyzed your website and generated a WCAG 2.1 Level AA
414 | Accessibility Statement compliant with EU Directive 2016/2102.
415 | 
416 | Download: accessibility-statement.pdf
417 | ```
418 | 
419 | **Impact:** Save legal teams **10-15 hours** per compliance report. Reduce legal risk.
420 | 
421 | **Continuous Monitoring Dashboard**
422 | - Track accessibility score over time
423 | - Alert on new violations introduced
424 | - Benchmark against industry standards
425 | - Generate executive reports
426 | 
427 | **Impact:** Transform accessibility from a one-time audit to an **ongoing practice**.
428 | 
429 | ---
430 | 
431 | ## 🚀 Scalability & Deployment
432 | 
433 | ### Deployment Options
434 | 
435 | #### 1. **GitHub Action** (Recommended for CI/CD)
436 | ```yaml
437 | # .github/workflows/accessibility.yml
438 | name: Accessibility Check
439 | on: [push, pull_request]
440 | jobs:
441 |   a11y:
442 |     runs-on: ubuntu-latest
443 |     steps:
444 |       - uses: actions/checkout@v2
445 |       - uses: scriptclean/a11y-action@v1
446 |         with:
447 |           files: 'src/**/*.{html,jsx,tsx}'
448 |           fail-on: critical
449 |           auto-fix: true
450 |           report: true
451 | ```
452 | 
453 | **Benefits:**
454 | - Runs on every commit
455 | - Blocks PRs with critical violations
456 | - Auto-generates compliance reports
457 | - Zero manual intervention
458 | 
459 | **Estimated Impact:** Prevents 90% of accessibility violations from reaching production.
460 | 
461 | #### 2. **VS Code Extension**
462 | ```json
463 | // settings.json
464 | {
465 |   "scriptclean.enableLinting": true,
466 |   "scriptclean.autoFix": true,
467 |   "scriptclean.showWCAGTooltips": true
468 | }
469 | ```
470 | 
471 | **Benefits:**
472 | - Real-time feedback as you type
473 | - Inline fix suggestions (Cmd+.)
474 | - WCAG criterion documentation on hover
475 | - Accessibility score in status bar
476 | 
477 | **Estimated Impact:** Reduces time-to-fix from hours to seconds.
478 | 
479 | #### 3. **Docker Container** (For Enterprise)
480 | ```bash
481 | docker run -p 5000:5000 \
482 |   -e IBM_BOB_API_KEY=$BOB_KEY \
483 |   scriptclean/a11y-guard:latest
484 | ```
485 | 
486 | **Benefits:**
487 | - Self-hosted for security compliance
488 | - Scales horizontally with Kubernetes
489 | - Integrates with existing CI/CD pipelines
490 | - No data leaves your infrastructure
491 | 
492 | **Estimated Impact:** Enterprise-ready deployment in under 5 minutes.
493 | 
494 | #### 4. **Cloud Service** (SaaS Model)
495 | ```bash
496 | curl -X POST https://api.scriptclean.io/scan \
497 |   -H "Authorization: Bearer $API_KEY" \
498 |   -F "file=@index.html"
499 | ```
500 | 
501 | **Benefits:**
502 | - Zero infrastructure management
503 | - Pay-per-scan pricing model
504 | - Global CDN for low latency
505 | - Automatic updates
506 | 
507 | **Estimated Impact:** Democratizes accessibility for small teams without DevOps resources.
508 | 
509 | ### Scalability Metrics
510 | 
511 | | Deployment | Concurrent Users | Scans/Hour | Cost/Month |
512 | |------------|------------------|------------|------------|
513 | | Local | 1 | 60 | $0 |
514 | | Docker | 10-50 | 600 | $50-200 |
515 | | Kubernetes | 100-1000 | 6,000 | $500-2,000 |
516 | | Cloud SaaS | Unlimited | Unlimited | $0.10/scan |
517 | 
518 | **Infrastructure:** ScriptClean is designed to scale horizontally. Each Flask instance is stateless, making it perfect for containerization and auto-scaling.
519 | 
520 | ---
521 | 
522 | ## 🎥 Visual Guide: Where to Place Media
523 | 
524 | ### 1. **Hero GIF** (Top of README, after badges)
525 | **What to show:** 
526 | - Drag file into upload zone
527 | - Progress bar with "Bob is analyzing..."
528 | - Results appear with issue count
529 | - Click "Apply Fix" on one issue
530 | - Counter updates
531 | 
532 | **Why here:** First impression. Judges see the core value proposition in 10 seconds.
533 | 
534 | **Recommended tool:** LICEcap or ScreenToGif (keep under 5MB)
535 | 
536 | ### 2. **Bob Priority Modal GIF** (In Features section)
537 | **What to show:**
538 | - Click "Ask Bob for priority" button
539 | - Modal slides in with animation
540 | - Highlight the metrics (fix time, impact score)
541 | - Show WCAG compliance percentages
542 | - Click "Got it, let's fix this!"
543 | 
544 | **Why here:** Demonstrates AI-powered intelligence and professional UI.
545 | 
546 | ### 3. **Side-by-Side Diff GIF** (In "How It Works" section)
547 | **What to show:**
548 | - Expand an issue card
549 | - Highlight broken code (left) and Bob's fix (right)
550 | - Show the green "Apply Fix" button
551 | - Issue card grays out after applying
552 | 
553 | **Why here:** Shows the quality of Bob's fixes and the one-click workflow.
554 | 
555 | ### 4. **Demo Video** (Linked at top, embedded in middle)
556 | **What to include:**
557 | - 30-second intro: The problem (96.3% of sites fail WCAG)
558 | - 60 seconds: Live demo of scanning a file
559 | - 30 seconds: Show Bob's priority recommendation
560 | - 30 seconds: Apply fixes and export report
561 | - 30 seconds: Show time saved (30 hours → 2 hours)
562 | 
563 | **Why here:** Comprehensive walkthrough for judges who want details.
564 | 
565 | **Recommended tool:** Loom or OBS Studio
566 | 
567 | ### 5. **Architecture Diagram** (In Tech Stack section)
568 | **What to show:**
569 | ```
570 | [Browser] → [Flask API] → [IBM Bob] → [WCAG Engine]
571 |     ↓           ↓              ↓            ↓
572 | [Upload]   [Parse]      [Analyze]     [Generate Fixes]
573 | ```
574 | 
575 | **Why here:** Shows technical sophistication and integration with IBM Bob.
576 | 
577 | ---
578 | 
579 | ## ♿ Accessibility Note
580 | 
581 | ScriptClean itself follows **WCAG 2.1 Level AA** standards. We eat our own cooking.
582 | 
583 | **Accessibility Features:**
584 | - ✅ Keyboard navigation (Tab, Enter, Escape)
585 | - ✅ Screen reader support (ARIA labels, semantic HTML)
586 | - ✅ Color contrast ratios meet AA standards (4.5:1 minimum)
587 | - ✅ Focus indicators on all interactive elements
588 | - ✅ Skip-to-content link for keyboard users
589 | 
590 | **Tested with:**
591 | - NVDA (Windows)
592 | - JAWS (Windows)
593 | - VoiceOver (macOS/iOS)
594 | - TalkBack (Android)
595 | 
596 | ---
597 | 
598 | ## 🏆 Hackathon Submission
599 | 
600 | Built for the **IBM Bob Hackathon — May 2026** under the theme *"Turn Idea Into Impact Faster."*
601 | 
602 | **Why ScriptClean Embodies This Theme:**
603 | - **Idea:** Make accessibility auditing instant and actionable
604 | - **Impact:** Save developers 15+ hours per project, make the web accessible to 1.3 billion people
605 | - **Faster:** 30-hour manual audit → 2-hour automated fix (93% time reduction)
606 | 
607 | **Measurable Outcomes:**
608 | - **Developer Time Saved:** 15-20 hours per project
609 | - **Cost Savings:** $1,125-$1,500 per project (at $75/hr rate)
610 | - **Accessibility Coverage:** 78% of all WCAG violations detected
611 | - **User Impact:** 16% more users can access fixed websites (1.3B people with disabilities)
612 | - **Legal Risk Reduction:** Compliance reports reduce ADA lawsuit exposure
613 | 
614 | ---
615 | 
616 | ## 📄 License
617 | 
618 | MIT License — see [LICENSE](LICENSE) for details.
619 | 
620 | ---
621 | 
622 | ## 🙏 Acknowledgments
623 | 
624 | - **IBM Bob Team** for the incredible AI platform
625 | - **WebAIM** for accessibility research and data
626 | - **W3C WAI** for WCAG 2.1 standards
627 | - **British Design Council** for the Double Diamond framework
628 | 
629 | ---
630 | 
631 | ## 📞 Contact
632 | 
633 | **Project Lead:** [Your Name]  
634 | **Email:** your.email@example.com  
635 | **GitHub:** [@yourusername](https://github.com/yourusername)  
636 | **Demo:** [https://scriptclean-demo.com](https://scriptclean-demo.com)
637 | 
638 | ---
639 | 
640 | <div align="center">
641 | 
642 | **Made with ❤️ and ♿ for a more accessible web**
643 | 
644 | [⭐ Star this repo](https://github.com/yourusername/scriptclean-a11y-guard) | [🐛 Report Bug](https://github.com/yourusername/scriptclean-a11y-guard/issues) | [💡 Request Feature](https://github.com/yourusername/scriptclean-a11y-guard/issues)
645 | 
646 | </div>
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
server\app.py

# VSCode Open Tabs
test_client.html,client/style.css,server/requirements.txt,README.md,server/app.py,client/script.js,client/index.html

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T10:07:00.811Z
User time zone: Asia/Karachi, UTC+5:00

# Current Cost
$0.01

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll check why the server is not working by examining the setup and testing it. Let me create a todo list and start diagnosing the issue.

<update_todo_list>
<todos>
[ ] Check if Python dependencies are installed
[ ] Test if the server can start
[ ] Verify directory structure and paths
[ ] Check for any runtime errors
[ ] Test API endpoints
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
server\app.py

# VSCode Open Tabs
test_client.html,client/style.css,server/requirements.txt,README.md,server/app.py,client/script.js,client/index.html

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T10:07:07.667Z
User time zone: Asia/Karachi, UTC+5:00

# Current Cost
$0.06

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check if Python dependencies are installed | Pending |
| 2 | Test if the server can start | Pending |
| 3 | Verify directory structure and paths | Pending |
| 4 | Check for any runtime errors | Pending |
| 5 | Test API endpoints | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let me check if the Python dependencies are installed and try to start the server.

<execute_command>
<command>cd server && pip list | findstr -i "flask"</command>
</execute_command>

---

**User:**

[execute_command for 'cd server && pip list | findstr -i "flask"'] Result:
Command executed in terminal  within working directory 'd:/scriptclean_a11y_guard'. Command execution was not successful, inspect the cause and adjust as needed.
Exit code: 1
Output:
At line:1 char:11
+ cd server && pip list | findstr -i "flask"
+           ~~
The token '&&' is not a valid statement separator in this version.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : InvalidEndOfLine
 

<environment_details>
# VSCode Visible Files
server\app.py

# VSCode Open Tabs
test_client.html,client/style.css,server/requirements.txt,README.md,server/app.py,client/script.js,client/index.html

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T10:07:23.055Z
User time zone: Asia/Karachi, UTC+5:00

# Current Cost
$0.11

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check if Python dependencies are installed | Pending |
| 2 | Test if the server can start | Pending |
| 3 | Verify directory structure and paths | Pending |
| 4 | Check for any runtime errors | Pending |
| 5 | Test API endpoints | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

I see, PowerShell doesn't use `&&`. Let me use the correct PowerShell syntax.

<execute_command>
<command>cd server; pip list | Select-String -Pattern "flask"</command>
</execute_command>

---

**User:**

[execute_command for 'cd server; pip list | Select-String -Pattern "flask"'] Result:
Command executed in terminal  within working directory 'd:/scriptclean_a11y_guard'. Exit code: 0
Output:

Flask                     3.1.3
flask-cors                6.0.2



<environment_details>
# VSCode Visible Files
server\app.py

# VSCode Open Tabs
test_client.html,client/style.css,server/requirements.txt,README.md,server/app.py,client/script.js,client/index.html

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T10:07:40.237Z
User time zone: Asia/Karachi, UTC+5:00

# Current Cost
$0.17

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check if Python dependencies are installed | Pending |
| 2 | Test if the server can start | Pending |
| 3 | Verify directory structure and paths | Pending |
| 4 | Check for any runtime errors | Pending |
| 5 | Test API endpoints | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Good! Flask and flask-cors are installed. Now let me try to start the server and see what happens.

<execute_command>
<command>cd server; python app.py</command>
</execute_command>

---

**User:**

[execute_command for 'cd server; python app.py'] Result:
Command is still running in terminal  from 'd:/scriptclean_a11y_guard'.


You will be updated on the terminal status and new output in the future.
<environment_details>
# VSCode Visible Files
server\app.py

# VSCode Open Tabs
test_client.html,client/style.css,server/requirements.txt,README.md,server/app.py,client/script.js,client/index.html

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `d:\scriptclean_a11y_guard`
### Original command: `cd server; python app.py`
### New Output
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.8:5000
Press CTRL+C to quit
 * Restarting with watchdog (windowsapi)
 * Debugger is active!
 * Debugger PIN: 128-078-010


# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T10:07:53.081Z
User time zone: Asia/Karachi, UTC+5:00

# Current Cost
$0.22

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check if Python dependencies are installed | Pending |
| 2 | Test if the server can start | Pending |
| 3 | Verify directory structure and paths | Pending |
| 4 | Check for any runtime errors | Pending |
| 5 | Test API endpoints | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Excellent! The server is actually **working perfectly**! It has started successfully and is running on:
- `http://127.0.0.1:5000` (localhost)
- `http://192.168.1.8:5000` (local network)

The server shows:
- ✅ Flask is running
- ✅ Debug mode is active
- ✅ Auto-reloader (watchdog) is working
- ✅ No errors in startup

Let me update the todo list and test the API endpoints to confirm everything is functioning correctly.

<update_todo_list>
<todos>
[x] Check if Python dependencies are installed
[x] Test if the server can start
[-] Verify directory structure and paths
[-] Test API endpoints
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
server\app.py

# VSCode Open Tabs
test_client.html,client/style.css,server/requirements.txt,README.md,server/app.py,client/script.js,client/index.html

# Actively Running Terminals
## Terminal 1 (Active)
### Working Directory: `d:\scriptclean_a11y_guard`
### Original command: `cd server; python app.py`

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T10:08:00.607Z
User time zone: Asia/Karachi, UTC+5:00

# Current Cost
$0.28

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check if Python dependencies are installed | Completed |
| 2 | Test if the server can start | Completed |
| 3 | Verify directory structure and paths | In Progress |
| 4 | Test API endpoints | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let me test the API endpoints to verify they're responding correctly. I'll open a new terminal to test the health check endpoint.

<execute_command>
<command>curl http://localhost:5000/health</command>
</execute_command>

