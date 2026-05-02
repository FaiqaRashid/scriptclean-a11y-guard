from flask import Flask, request, jsonify, send_from_directory, redirect, abort
from flask_cors import CORS
from pathlib import Path
import os
import json
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for client communication

# ============================================================
# CROSS-PLATFORM PATH CONFIGURATION
# ============================================================
# Use pathlib for cross-platform compatibility (Windows/Mac/Linux)
BASE_DIR = Path(__file__).parent.parent.resolve()
CLIENT_DIR = BASE_DIR / "client"
SAMPLES_DIR = BASE_DIR / "text_samples"
UPLOADS_DIR = BASE_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "reports"

# Avoid Windows/Services conflict on port 5000 (e.g. AirPlay); override with A11Y_GUARD_PORT
SERVER_PORT = int(os.environ.get("A11Y_GUARD_PORT", "5050"))

# Create directories if they don't exist
UPLOADS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# ============================================================
# ACCESSIBILITY SCANNING ENGINE
# ============================================================
class A11yScanner:
    """
    Core accessibility scanner that analyzes HTML/PHP/JS files
    for WCAG 2.1 violations using regex patterns and context analysis.
    """
    
    def __init__(self):
        self.issues = []
        self.stats = {
            'critical': 0,
            'warning': 0,
            'info': 0,
            'files_scanned': 0
        }
    
    def scan_content(self, content, filename):
        """Scan file content for accessibility issues"""
        self.issues = []
        lines = content.split('\n')
        
        # Check for missing alt attributes on images
        self._check_missing_alt(lines, filename)
        
        # Check for missing ARIA labels on buttons/inputs
        self._check_missing_aria_labels(lines, filename)
        
        # Check for role and structure issues
        self._check_role_structure(lines, filename)
        
        # Check for heading hierarchy
        self._check_heading_hierarchy(lines, filename)
        
        # Check for form labels
        self._check_form_labels(lines, filename)
        
        self.stats['files_scanned'] += 1
        return self.issues
    
    def _check_missing_alt(self, lines, filename):
        """Check for images without alt attributes"""
        img_pattern = re.compile(r'<img\s+[^>]*?>', re.IGNORECASE)
        alt_pattern = re.compile(r'\balt\s*=', re.IGNORECASE)
        
        for i, line in enumerate(lines, 1):
            for match in img_pattern.finditer(line):
                img_tag = match.group(0)
                if not alt_pattern.search(img_tag):
                    # Extract src for context
                    src_match = re.search(r'src\s*=\s*["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
                    src = src_match.group(1) if src_match else 'unknown'
                    
                    self.issues.append({
                        'id': len(self.issues) + 1,
                        'severity': 'critical',
                        'type': 'Missing Alt Text',
                        'file': filename,
                        'line': i,
                        'desc': f'Image "{src}" has no alt attribute. Screen readers cannot convey this content to visually impaired users.',
                        'broken': img_tag.strip(),
                        'fix': self._generate_alt_fix(img_tag, src),
                        'wcag': 'WCAG 1.1.1',
                        'applied': False
                    })
                    self.stats['critical'] += 1
    
    def _generate_alt_fix(self, img_tag, src):
        """Generate contextual alt text fix"""
        # Smart alt text based on filename
        filename = Path(src).stem
        alt_text = filename.replace('-', ' ').replace('_', ' ').title()
        
        # Insert alt attribute before closing >
        return img_tag[:-1] + f' alt="{alt_text}">'
    
    def _check_missing_aria_labels(self, lines, filename):
        """Check for buttons/inputs without accessible labels"""
        button_pattern = re.compile(r'<button[^>]*?>.*?</button>', re.IGNORECASE | re.DOTALL)
        aria_pattern = re.compile(r'\baria-label\s*=', re.IGNORECASE)
        
        for i, line in enumerate(lines, 1):
            # Check buttons with only icons (SVG)
            for match in button_pattern.finditer(line):
                button = match.group(0)
                if '<svg' in button and not aria_pattern.search(button):
                    # Extract onclick for context
                    onclick_match = re.search(r'onclick\s*=\s*["\']([^"\']+)["\']', button)
                    context = onclick_match.group(1) if onclick_match else 'action'
                    
                    self.issues.append({
                        'id': len(self.issues) + 1,
                        'severity': 'critical',
                        'type': 'Missing ARIA Label',
                        'file': filename,
                        'line': i,
                        'desc': f'Button with icon has no aria-label. Screen reader users cannot determine its purpose.',
                        'broken': button[:80] + '...' if len(button) > 80 else button,
                        'fix': self._generate_aria_fix(button, context),
                        'wcag': 'WCAG 4.1.2',
                        'applied': False
                    })
                    self.stats['critical'] += 1
    
    def _generate_aria_fix(self, element, context):
        """Generate aria-label fix"""
        label = context.replace('()', '').replace('open', 'Open').replace('close', 'Close')
        return element.replace('<button', f'<button aria-label="{label}"', 1)
    
    def _check_role_structure(self, lines, filename):
        """Check for proper landmark roles"""
        content = '\n'.join(lines)
        
        # Check for main landmark
        if '<main' not in content.lower() and 'role="main"' not in content.lower():
            if '<div class="main' in content.lower() or '<div class="container' in content.lower():
                self.issues.append({
                    'id': len(self.issues) + 1,
                    'severity': 'warning',
                    'type': 'Role & Structure',
                    'file': filename,
                    'line': 1,
                    'desc': 'No <main> landmark found. Screen readers use landmarks to navigate page sections.',
                    'broken': '<div class="main-content">',
                    'fix': '<main class="main-content" role="main">',
                    'wcag': 'WCAG 1.3.1',
                    'applied': False
                })
                self.stats['warning'] += 1
    
    def _check_heading_hierarchy(self, lines, filename):
        """Check for proper heading hierarchy"""
        headings = []
        for i, line in enumerate(lines, 1):
            for level in range(1, 7):
                if f'<h{level}' in line.lower():
                    headings.append((level, i))
        
        # Check for skipped levels
        for i in range(len(headings) - 1):
            current_level, current_line = headings[i]
            next_level, next_line = headings[i + 1]
            if next_level > current_level + 1:
                self.issues.append({
                    'id': len(self.issues) + 1,
                    'severity': 'warning',
                    'type': 'Role & Structure',
                    'file': filename,
                    'line': next_line,
                    'desc': f'Heading hierarchy jumps from H{current_level} to H{next_level}, skipping levels.',
                    'broken': f'<h{next_level}>',
                    'fix': f'<h{current_level + 1}>',
                    'wcag': 'WCAG 2.4.6',
                    'applied': False
                })
                self.stats['warning'] += 1
                break
    
    def _check_form_labels(self, lines, filename):
        """Check for form inputs without labels"""
        input_pattern = re.compile(r'<input[^>]*?>', re.IGNORECASE)
        
        for i, line in enumerate(lines, 1):
            for match in input_pattern.finditer(line):
                input_tag = match.group(0)
                # Check if input has id but no aria-label
                if 'id=' in input_tag and 'aria-label' not in input_tag:
                    # Check if there's a label in previous or same line
                    context = '\n'.join(lines[max(0, i-2):i+1])
                    if '<label' not in context.lower():
                        input_type = re.search(r'type\s*=\s*["\']([^"\']+)["\']', input_tag)
                        type_val = input_type.group(1) if input_type else 'text'
                        
                        self.issues.append({
                            'id': len(self.issues) + 1,
                            'severity': 'critical',
                            'type': 'Missing ARIA Label',
                            'file': filename,
                            'line': i,
                            'desc': f'Input field ({type_val}) has no associated label or aria-label.',
                            'broken': input_tag.strip(),
                            'fix': input_tag.replace('<input', f'<input aria-label="{type_val.title()} input"', 1),
                            'wcag': 'WCAG 4.1.2',
                            'applied': False
                        })
                        self.stats['critical'] += 1

# ============================================================
# API ENDPOINTS
# ============================================================

@app.route('/api/scan', methods=['POST'])
def scan_code():
    """
    Main scanning endpoint - receives code and returns accessibility issues
    Integrates with IBM Bob for enhanced reporting
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Invalid JSON data'
            }), 400
        
        code = data.get('code', '')
        filename = data.get('filename', 'uploaded_file.html')
        
        if not code:
            return jsonify({
                'status': 'error',
                'message': 'No code provided'
            }), 400
        
        # Initialize scanner
        scanner = A11yScanner()
        issues = scanner.scan_content(code, filename)
        
        # Generate IBM Bob report
        bob_report = generate_bob_report(issues, scanner.stats, filename)
        
        return jsonify({
            'status': 'success',
            'issues': issues,
            'stats': scanner.stats,
            'bob_report': bob_report,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        # IBM Bob error reporting integration
        return jsonify({
            'status': 'error',
            'message': str(e),
            'bob_report': {
                'error': True,
                'details': f'Scan failed: {str(e)}'
            }
        }), 500

@app.route('/api/scan-file', methods=['POST'])
def scan_file():
    """
    Scan a file from the test_samples directory or custom path
    Cross-platform path handling with dynamic file selection
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Invalid JSON data'
            }), 400
        
        filename = data.get('filename', '')
        
        if not filename:
            return jsonify({
                'status': 'error',
                'message': 'No filename provided'
            }), 400
        
        # Check if it's a full path or just a filename
        file_path = Path(filename)
        
        # If it's just a filename (no directory separators), look in test-samples
        if file_path.name == filename:
            # Secure path handling - prevent directory traversal
            safe_filename = file_path.name
            file_path = SAMPLES_DIR / safe_filename
        else:
            # It's a path - resolve it; only allow files inside the project tree
            try:
                base_resolved = BASE_DIR.resolve()
                if not file_path.is_absolute():
                    file_path = (base_resolved / file_path).resolve()
                else:
                    file_path = file_path.resolve()
                file_path.relative_to(base_resolved)
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': 'Access denied: Path outside project directory'
                }), 403
            except Exception:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid file path'
                }), 400
        
        if not file_path.exists():
            # Try to find the file in test_samples
            alt_path = SAMPLES_DIR / Path(filename).name
            if alt_path.exists():
                file_path = alt_path
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'File not found: {filename}',
                    'hint': f'Available files in test_samples: {[f.name for f in SAMPLES_DIR.glob("*.*") if f.is_file()]}'
                }), 404
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Scan the content
        scanner = A11yScanner()
        issues = scanner.scan_content(code, file_path.name)
        
        # Generate IBM Bob report
        bob_report = generate_bob_report(issues, scanner.stats, file_path.name)
        
        return jsonify({
            'status': 'success',
            'issues': issues,
            'stats': scanner.stats,
            'bob_report': bob_report,
            'filename': file_path.name,
            'full_path': str(file_path),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'bob_report': {
                'error': True,
                'details': f'File scan failed: {str(e)}'
            }
        }), 500

@app.route('/api/samples', methods=['GET'])
def list_samples():
    """
    List available test sample files
    Cross-platform directory listing
    """
    try:
        samples = []
        if SAMPLES_DIR.exists():
            for file_path in SAMPLES_DIR.iterdir():
                if file_path.is_file() and file_path.suffix in ['.html', '.php', '.js']:
                    samples.append({
                        'name': file_path.name,
                        'size': file_path.stat().st_size,
                        'extension': file_path.suffix
                    })
        
        return jsonify({
            'status': 'success',
            'samples': samples,
            'count': len(samples)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/export-report', methods=['POST'])
def export_report():
    """
    Export IBM Bob accessibility report as JSON
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Invalid JSON data'
            }), 400
        
        report_data = data.get('report', {})
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f'a11y_report_{timestamp}.json'
        report_path = REPORTS_DIR / report_filename
        
        # Save report
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
        
        return jsonify({
            'status': 'success',
            'filename': report_filename,
            'path': str(report_path)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ============================================================
# IBM BOB REPORTING INTEGRATION
# ============================================================

def generate_bob_report(issues, stats, filename):
    """
    Generate comprehensive IBM Bob accessibility report
    This integrates Bob's AI-powered insights into the error handling
    """
    report = {
        'tool': 'ScriptClean A11y Guard',
        'powered_by': 'IBM Bob',
        'scan_date': datetime.now().isoformat(),
        'file_analyzed': filename,
        'summary': {
            'total_issues': len(issues),
            'critical': stats['critical'],
            'warning': stats['warning'],
            'info': stats['info'],
            'files_scanned': stats['files_scanned']
        },
        'wcag_compliance': {
            'level_a': calculate_wcag_compliance(issues, 'A'),
            'level_aa': calculate_wcag_compliance(issues, 'AA'),
            'level_aaa': calculate_wcag_compliance(issues, 'AAA')
        },
        'issues': issues,
        'recommendations': generate_recommendations(issues),
        'bob_insights': {
            'priority_fix': get_priority_fix(issues),
            'estimated_fix_time': estimate_fix_time(issues),
            'impact_score': calculate_impact_score(stats)
        }
    }
    
    return report

def calculate_wcag_compliance(issues, level):
    """Calculate WCAG compliance percentage"""
    # Simplified calculation - in production, this would be more sophisticated
    total_checks = 20  # Total WCAG criteria checked
    failed_checks = len([i for i in issues if level in i.get('wcag', '')])
    compliance = ((total_checks - failed_checks) / total_checks) * 100
    return round(compliance, 1)

def generate_recommendations(issues):
    """Generate prioritized recommendations"""
    recommendations = []
    
    critical_count = len([i for i in issues if i['severity'] == 'critical'])
    if critical_count > 0:
        recommendations.append({
            'priority': 'HIGH',
            'action': f'Fix {critical_count} critical accessibility issues immediately',
            'impact': 'These issues prevent users with disabilities from accessing content'
        })
    
    warning_count = len([i for i in issues if i['severity'] == 'warning'])
    if warning_count > 0:
        recommendations.append({
            'priority': 'MEDIUM',
            'action': f'Address {warning_count} warning-level issues',
            'impact': 'These issues create barriers but have workarounds'
        })
    
    return recommendations

def get_priority_fix(issues):
    """Identify the most critical fix to apply first (fallback to any issue)."""
    if not issues:
        return None
    critical_issues = [i for i in issues if i['severity'] == 'critical']
    top = critical_issues[0] if critical_issues else issues[0]
    return {
        'issue_id': top['id'],
        'issue': top['type'],
        'file': top['file'],
        'line': top['line'],
        'reason': (
            'This critical issue has the highest impact on accessibility'
            if top['severity'] == 'critical'
            else 'No critical findings — address this warning first for best results'
        )
    }

def estimate_fix_time(issues):
    """Estimate time to fix all issues"""
    # Rough estimate: 5 min per critical, 3 min per warning, 1 min per info
    time_map = {'critical': 5, 'warning': 3, 'info': 1}
    total_minutes = sum(time_map.get(i['severity'], 1) for i in issues)
    return f"{total_minutes} minutes"

def calculate_impact_score(stats):
    """Calculate overall accessibility impact score (0-100)"""
    # Higher score = worse accessibility
    score = (stats['critical'] * 10) + (stats['warning'] * 5) + (stats['info'] * 1)
    return min(score, 100)

# ============================================================
# HEALTH CHECK & STATIC FILES
# ============================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'ScriptClean A11y Guard API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/app')
def app_redirect():
    """Use trailing slash so relative asset URLs (style.css, script.js) resolve correctly."""
    return redirect('/app/', code=302)


@app.route('/app/')
@app.route('/app/index.html')
def serve_web_app():
    """Serve the ScriptClean UI from the same origin as the API."""
    if not CLIENT_DIR.is_dir():
        abort(500, description='Client directory missing')
    index_path = CLIENT_DIR / 'index.html'
    if not index_path.is_file():
        abort(404, description='client/index.html not found')
    return send_from_directory(CLIENT_DIR, 'index.html')


@app.route('/app/style.css')
def serve_app_css():
    return send_from_directory(CLIENT_DIR, 'style.css')


@app.route('/app/script.js')
def serve_app_js():
    return send_from_directory(CLIENT_DIR, 'script.js')


@app.route('/')
def index():
    """Serve API documentation"""
    return jsonify({
        'service': 'ScriptClean A11y Guard API',
        'version': '1.0.0',
        'endpoints': {
            '/api/scan': 'POST - Scan code for accessibility issues',
            '/api/scan-file': 'POST - Scan a file from test_samples',
            '/api/samples': 'GET - List available test samples',
            '/api/export-report': 'POST - Export accessibility report',
            '/health': 'GET - Health check'
        },
        'powered_by': 'IBM Bob',
        'web_ui': f'http://127.0.0.1:{SERVER_PORT}/app/'
    })

# ============================================================
# SERVER STARTUP
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("ScriptClean A11y Guard Server")
    print("Powered by IBM Bob")
    print("=" * 60)
    print(f"Base Directory: {BASE_DIR}")
    print(f"Samples Directory: {SAMPLES_DIR}")
    print(f"Uploads Directory: {UPLOADS_DIR}")
    print(f"Reports Directory: {REPORTS_DIR}")
    print("=" * 60)
    idx = CLIENT_DIR / 'index.html'
    if not idx.is_file():
        print(f"WARNING: Web UI missing — expected {idx}")
    print(f"Server port: {SERVER_PORT} (set A11Y_GUARD_PORT to change)")
    print(f"Open the web app: http://127.0.0.1:{SERVER_PORT}/app/")
    print(f"If /app/ is 404 in the browser but this log appeared, port {SERVER_PORT} may be used by another app — try a different A11Y_GUARD_PORT.")
    print("=" * 60)
    
    app.run(debug=True, port=SERVER_PORT, host='0.0.0.0')

# Made with Bob
