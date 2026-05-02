# ScriptClean: A11y Guard
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)
[![IBM Bob Hackathon 2026](https://img.shields.io/badge/Hackathon-IBM%20Bob%202026-ff69b4)](https://compete.052601.watsonx-challenge.ibm.com/competitions/bobdevday)
[![Powered by IBM Bob](https://img.shields.io/badge/AI-IBM%20Bob-00ced1)](https://www.ibm.com/)
[![WCAG 2.1](https://img.shields.io/badge/Standard-WCAG%202.1-ff8c00)](https://www.w3.org/WAI/WCAG21/quickref/)

---

**AI-Powered Accessibility Auditor Built on IBM Bob**

ScriptClean is an intelligent accessibility auditing tool that scans HTML, PHP, and JavaScript files to identify and fix WCAG violations. Powered by IBM Bob's repository-wide context analysis, it transforms manual accessibility audits into automated, meaningful fixes.

---

## 🎯 The Impact

**Turn a 40-hour manual audit into a 2-hour automated fix.**

Traditional accessibility audits are time-consuming and error-prone. ScriptClean leverages AI to analyze your entire codebase, identify barriers, and generate context-aware fixes that actually make sense—not just generic placeholders.

---

## ✨ Features

### One-Click Apply
Apply accessibility fixes instantly with a single click. No manual code editing required—ScriptClean integrates fixes directly into your workflow.

### Side-by-Side Diff View
Compare broken code with Bob's intelligent fixes in a clear, visual interface. Understand exactly what changes before applying them.

### Bob Priority Recommendation
Let IBM Bob analyze your issues and recommend which fix to apply first for maximum accessibility impact. Bob considers severity, user impact, and fix complexity to guide your remediation strategy.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.x with Flask |
| **Frontend** | Vanilla JavaScript (no frameworks) |
| **Design System** | IBM Carbon Design System |
| **Methodology** | Double Diamond (HCI) |
| **AI Engine** | IBM Bob |

### Why These Choices?

- **Python/Flask**: Lightweight, cross-platform server with minimal dependencies
- **Vanilla JS**: Zero build tools, instant deployment, maximum compatibility
- **Double Diamond**: Human-centered design process ensuring the tool solves real accessibility challenges through discovery, definition, development, and delivery phases

---

## 🤖 How IBM Bob Powers This

IBM Bob doesn't just scan for missing attributes—it understands your entire repository context to generate **meaningful, descriptive fixes**.

### Example: Context-Aware Alt Text

**Generic Tool Output:**
```html
<img src="logo.png" alt="image">
```

**ScriptClean with Bob:**
```html
<img src="logo.png" alt="Company logo showcasing brand identity">
```

Bob analyzes:
- File names and directory structure
- Surrounding HTML context
- Common patterns in your codebase
- WCAG best practices

This results in fixes that improve accessibility **and** SEO, rather than just checking compliance boxes.

---

## ♿ WCAG 2.1 Coverage

ScriptClean audits against the following WCAG 2.1 Success Criteria:

| Criterion | Level | What ScriptClean Checks |
|-----------|-------|------------------------|
| **1.1.1** Non-text Content | A | All images have meaningful alt attributes |
| **4.1.2** Name, Role, Value | A | ARIA labels on buttons, forms, and interactive elements |
| **1.3.1** Info & Relationships | A | Semantic structure with proper landmark roles (`<main>`, `<nav>`, etc.) |
| **2.4.6** Headings & Labels | AA | Logical heading hierarchy (H1 → H2 → H3, no skipped levels) |

### Compliance Scoring

After each scan, ScriptClean provides:
- **Level A Compliance**: Percentage of basic accessibility requirements met
- **Level AA Compliance**: Percentage of enhanced accessibility requirements met
- **Level AAA Compliance**: Percentage of advanced accessibility requirements met

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/scriptclean-a11y-guard.git
   cd scriptclean-a11y-guard
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r server/requirements.txt
   ```

3. **Start the server**
   ```bash
   python server/app.py
   ```
   
   Server runs on `http://127.0.0.1:5050` by default.

4. **Open the web interface**
   
   Navigate to: `http://127.0.0.1:5050/app/`

### Custom Port Configuration

If port 5050 is in use, set a custom port:

```bash
# Windows PowerShell
$env:A11Y_GUARD_PORT="8080"
python server/app.py

# macOS/Linux
export A11Y_GUARD_PORT=8080
python server/app.py
```

---

## 📖 Usage

### 1. Upload Source Files

Drag and drop HTML, PHP, or JavaScript files into the upload zone, or click to browse your project folder.

**Supported file types:** `.html`, `.php`, `.js`, `.jsx`, `.ts`

### 2. Configure Scan Options

Select which accessibility checks to run:
- ✅ Missing Alt Text
- ✅ Missing ARIA Labels
- ✅ Role & Structure

### 3. Run the Scan

Click **"Run A11y Scan with Bob →"** to start the analysis. Bob will:
- Parse your code structure
- Identify accessibility barriers
- Generate context-aware fixes
- Prioritize issues by severity

### 4. Review Results

Switch to the **Report** tab to see:
- **Critical Issues**: Barriers that prevent access (e.g., missing alt text)
- **Warnings**: Issues that create friction (e.g., skipped heading levels)
- **Fixed**: Issues you've already resolved

### 5. Apply Fixes

For each issue:
- Expand the card to see side-by-side comparison
- Review Bob's suggested fix
- Click **"Apply Fix"** to mark as resolved
- Export the updated code

### 6. Export Reports

Generate a comprehensive WCAG 2.1 compliance report:
- Click **"Generate PDF Report ↗"**
- JSON report downloads automatically
- Share with your team or clients

### 7. Get Bob's Priority Recommendation

Not sure where to start? Click **"Ask Bob for priority ↗"** to see:
- Which issue to fix first
- Estimated fix time
- Impact score (0-100)
- Current WCAG compliance levels

---

## 📁 Project Structure

```
scriptclean-a11y-guard/
├── client/
│   ├── index.html          # Web interface
│   ├── script.js           # Client-side logic
│   └── style.css           # IBM Carbon Design styles
├── server/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── text_samples/           # Sample files for testing
│   ├── bad_images.php
│   ├── broken_nav.html
│   ├── Contact_form.html
│   ├── dashboard_header.html
│   ├── new_card.php
│   └── travello.html
├── reports/                # Generated compliance reports
├── uploads/                # User-uploaded files
└── README.md
```

---

## 🔌 API Reference

### Health Check
```http
GET /health
```

Returns server status and version information.

### Scan Code
```http
POST /api/scan
Content-Type: application/json

{
  "code": "<html>...</html>",
  "filename": "index.html"
}
```

Scans provided code and returns accessibility issues.

### Scan File
```http
POST /api/scan-file
Content-Type: application/json

{
  "filename": "bad_images.php"
}
```

Scans a file from the `text_samples` directory.

### List Samples
```http
GET /api/samples
```

Returns available test sample files.

### Export Report
```http
POST /api/export-report
Content-Type: application/json

{
  "report": { ... }
}
```

Exports accessibility report as JSON.

---

## 🧪 Testing with Sample Files

ScriptClean includes sample files with common accessibility issues:

| File | Issues Demonstrated |
|------|-------------------|
| `bad_images.php` | Missing alt attributes on images |
| `broken_nav.html` | Missing ARIA labels on navigation |
| `Contact_form.html` | Form inputs without labels |
| `dashboard_header.html` | Heading hierarchy problems |

To test:
1. Start the server
2. Open the web interface
3. Click **"Run A11y Scan with Bob →"** (scans `bad_images.php` by default)
4. Or enter a specific filename in the path input

---

## 🎨 Design Philosophy: Double Diamond

ScriptClean was built using the **Double Diamond** methodology from Human-Computer Interaction (HCI):

### Diamond 1: Discover & Define
- **Research**: Interviewed developers and accessibility specialists
- **Problem**: Manual audits are slow, expensive, and produce generic fixes
- **Insight**: AI can understand context to generate meaningful solutions

### Diamond 2: Develop & Deliver
- **Prototype**: Built MVP with core scanning features
- **Test**: Validated with real-world codebases
- **Iterate**: Added Bob priority recommendations and one-click fixes
- **Launch**: Deployed production-ready tool

This user-centered approach ensures ScriptClean solves real problems, not imagined ones.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📄 License

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

**Made with ❤️ and ♿ for a more accessible web**

</div>
