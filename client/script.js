// ============================================================
// SCRIPTCLEAN A11Y GUARD - CLIENT SCRIPT
// Powered by IBM Bob
// ============================================================

// Same host as the UI when served from /app/; file:// fallback must match server A11Y_GUARD_PORT (default 5050)
const DEFAULT_DEV_PORT = '5050';
const API_BASE =
  window.location.protocol === 'file:' || !window.location.host
    ? `http://127.0.0.1:${DEFAULT_DEV_PORT}`
    : window.location.origin;

// Global state
let currentIssues = [];
let currentBobReport = null;
let currentFilter = 'all';
let fixedCount = 0;
let scanDone = false;
let queuedFiles = [];

// ============================================================
// TAB NAVIGATION
// ============================================================

function switchTab(tab, el) {
  document.querySelectorAll('.sc-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.sc-panel').forEach(p => p.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('panel-' + tab).classList.add('active');
}

function toggleOpt(el) {
  el.classList.toggle('checked');
}

// ============================================================
// FILE HANDLING
// ============================================================

function handleDrag(e) {
  e.preventDefault();
  document.getElementById('dropzone').classList.add('drag');
}

function handleDragLeave() {
  document.getElementById('dropzone').classList.remove('drag');
}

function handleDrop(e) {
  e.preventDefault();
  document.getElementById('dropzone').classList.remove('drag');
  handleFiles(e.dataTransfer.files);
}

function handleFiles(files) {
  queuedFiles = [...files];
  const el = document.getElementById('files-queued');
  if (queuedFiles.length) {
    el.style.display = 'block';
    el.innerHTML = queuedFiles.map(f => 
      `<span style="font-family:var(--mono);font-size:11px;background:rgba(15,98,254,.1);padding:2px 8px;margin-right:6px;color:var(--ibm-blue)">${f.name}</span>`
    ).join('') + `<span style="font-size:11px;color:var(--ibm-gray-60);margin-left:4px">${queuedFiles.length} file${queuedFiles.length > 1 ? 's' : ''} ready</span>`;
  }
}

function addPath() {
  const v = document.getElementById('path-input').value.trim();
  if (!v) return;
  const el = document.getElementById('files-queued');
  el.style.display = 'block';
  el.innerHTML = `<span style="font-family:var(--mono);font-size:11px;background:rgba(15,98,254,.1);padding:2px 8px;color:var(--ibm-blue)">${v}</span><span style="font-size:11px;color:var(--ibm-gray-60);margin-left:6px">Path queued</span>`;
}

// ============================================================
// SCANNING LOGIC - CONNECTED TO NEW API
// ============================================================

async function startScan() {
  // Switch to report tab
  document.querySelectorAll('.sc-tab')[1].click();
  document.getElementById('empty-report').style.display = 'none';
  document.getElementById('results-section').style.display = 'none';
  
  const prog = document.getElementById('progress-section');
  prog.style.display = 'block';
  
  const fill = document.getElementById('progress-fill');
  const pct = document.getElementById('progress-pct');
  const status = document.getElementById('progress-status');
  
  const steps = [
    'Initializing IBM Bob engine...',
    'Reading repository context...',
    'Parsing HTML structure...',
    'Checking alt attributes on img tags...',
    'Auditing ARIA labels on interactive elements...',
    'Validating landmark roles...',
    'Verifying heading hierarchy...',
    'Generating contextual fix suggestions...',
    'Compiling accessibility report...'
  ];
  
  let p = 0;
  let si = 0;
  
  // Animate progress bar
  const iv = setInterval(() => {
    p += Math.random() * 14;
    if (p > 100) p = 100;
    fill.style.width = Math.round(p) + '%';
    pct.textContent = Math.round(p) + '%';
    if (si < steps.length - 1 && p > si * 12) {
      status.textContent = steps[si];
      si++;
    }
    if (p >= 100) {
      clearInterval(iv);
      setTimeout(() => performActualScan(), 400);
    }
  }, 300);
}

async function performActualScan() {
  try {
    let response;
    
    // Check if we have queued files
    if (queuedFiles.length > 0) {
      // Read first file and scan it
      const file = queuedFiles[0];
      const content = await file.text();
      
      response = await fetch(`${API_BASE}/api/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code: content,
          filename: file.name
        })
      });
    } else {
      // Check if user entered a path
      const pathInput = document.getElementById('path-input').value.trim();
      const filename = pathInput || 'bad_images.php';
      
      // Scan file from test_samples or custom path
      response = await fetch(`${API_BASE}/api/scan-file`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          filename: filename
        })
      });
    }
    
    if (!response.ok) {
      throw new Error(`Scan failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    // Store results globally
    currentIssues = data.issues || [];
    currentBobReport = data.bob_report || null;
    
    // Update stats from server response
    if (data.stats) {
      document.getElementById('stat-critical').textContent = data.stats.critical;
      document.getElementById('stat-warning').textContent = data.stats.warning;
      document.getElementById('stat-files').textContent = data.stats.files_scanned;
    }
    
    showResults();
    
  } catch (error) {
    console.error('Scan error:', error);
    document.getElementById('progress-section').style.display = 'none';
    document.getElementById('empty-report').style.display = 'block';
    document.getElementById('empty-report').innerHTML = `
      <div style="padding:2rem;text-align:center;color:var(--ibm-red)">
        <div style="font-size:14px;margin-bottom:6px">Scan failed</div>
        <div style="font-size:12px">${error.message}</div>
        <div style="font-size:11px;margin-top:8px;color:var(--ibm-gray-60)">Check that the server is running (default port ${DEFAULT_DEV_PORT}) and you opened this app from /app/ on the same host.</div>
      </div>
    `;
  }
}

function showResults() {
  document.getElementById('progress-section').style.display = 'none';
  document.getElementById('results-section').style.display = 'block';
  scanDone = true;
  
  updateStats();
  renderIssues();
  
  const badge = document.getElementById('issue-count-badge');
  badge.style.display = 'inline';
  badge.textContent = currentIssues.length;
}

// ============================================================
// ISSUE DISPLAY & FILTERING
// ============================================================

function updateStats() {
  const crit = currentIssues.filter(i => i.severity === 'critical' && !i.applied).length;
  const warn = currentIssues.filter(i => i.severity === 'warning' && !i.applied).length;
  document.getElementById('stat-critical').textContent = crit;
  document.getElementById('stat-warning').textContent = warn;
  document.getElementById('stat-fixed').textContent = fixedCount;
}

function filterIssues(f, btn) {
  currentFilter = f;
  document.querySelectorAll('.sc-filter-btn').forEach(b => {
    b.classList.remove('active', 'critical', 'warning-f');
  });
  if (f === 'critical') btn.classList.add('critical');
  else if (f === 'warning') btn.classList.add('warning-f');
  else btn.classList.add('active');
  renderIssues();
}

function renderIssues() {
  const list = document.getElementById('issue-list');
  const filtered = currentFilter === 'all' 
    ? currentIssues 
    : currentIssues.filter(i => i.severity === currentFilter);
  
  list.innerHTML = filtered.map(issue => `
    <div class="sc-issue-card ${issue.applied ? 'applied' : ''}" id="card-${issue.id}" style="${issue.applied ? 'opacity:.5' : ''}">
      <div class="sc-issue-header" onclick="toggleIssue(${issue.id})">
        <span class="sc-severity ${issue.severity}">${issue.severity}</span>
        <span class="sc-issue-file">${issue.file}<span style="color:var(--ibm-gray-30);margin:0 4px">:</span><span style="color:var(--ibm-gray-60)">L${issue.line}</span></span>
        <span class="sc-issue-type">${issue.type}</span>
        <span class="sc-wcag">${issue.wcag}</span>
        <span class="sc-chevron" id="chev-${issue.id}">▾</span>
      </div>
      <div class="sc-issue-body" id="body-${issue.id}">
        <div class="sc-issue-desc">${issue.desc}</div>
        <div class="sc-issue-row">
          <div style="flex:1">
            <div class="sc-code-label">Current code</div>
            <div class="sc-code-block">${escHtml(issue.broken)}</div>
          </div>
          <div style="flex:1">
            <div class="sc-code-label" style="color:var(--ibm-green)">Bob's fix</div>
            <div class="sc-code-block fix">${escHtml(issue.fix)}</div>
          </div>
        </div>
        <div class="sc-apply-row">
          <span class="sc-applied-tag ${issue.applied ? 'show' : ''}" id="applied-${issue.id}">✓ Fix applied</span>
          ${issue.applied ? '' : `
            <button class="sc-btn sc-btn-ghost sc-btn-sm" onclick="dismissIssue(${issue.id})">Dismiss</button>
            <button class="sc-btn sc-btn-success sc-btn-sm" onclick="applyFix(${issue.id})">Apply Fix</button>
          `}
        </div>
      </div>
    </div>
  `).join('');
}

function toggleIssue(id) {
  const body = document.getElementById('body-' + id);
  const chev = document.getElementById('chev-' + id);
  const open = body.classList.toggle('open');
  chev.classList.toggle('open', open);
}

function applyFix(id) {
  const issue = currentIssues.find(i => i.id === id);
  if (!issue) return;
  issue.applied = true;
  fixedCount++;
  updateStats();
  renderIssues();
  
  // Show success notification
  showNotification(`✓ Fix applied for ${issue.type} on line ${issue.line}`, 'success');
}

function dismissIssue(id) {
  const idx = currentIssues.findIndex(i => i.id === id);
  if (idx > -1) currentIssues.splice(idx, 1);
  updateStats();
  renderIssues();
}

// ============================================================
// IBM BOB INTEGRATION - EXPORT & PRIORITY
// ============================================================

async function exportBobReport() {
  if (!currentBobReport) {
    showNotification('⚠ No scan results to export. Run a scan first.', 'warning');
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/api/export-report`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        report: currentBobReport
      })
    });
    
    if (!response.ok) {
      throw new Error('Export failed');
    }
    
    const data = await response.json();
    
    // Download the report as JSON
    const blob = new Blob([JSON.stringify(currentBobReport, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = data.filename || 'a11y_report.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification(`✓ Report exported: ${data.filename}`, 'success');
    
  } catch (error) {
    console.error('Export error:', error);
    showNotification('⚠ Export failed. Check console for details.', 'error');
  }
}

function resolvePriorityIssueId(priority) {
  if (priority.issue_id != null) return Number(priority.issue_id);
  if (!currentIssues.length) return null;
  const line = Number(priority.line);
  const byFileLine = currentIssues.find(
    i => i.file === priority.file && Number(i.line) === line
  );
  if (byFileLine) return byFileLine.id;
  const byType = currentIssues.find(i => i.type === priority.issue);
  return byType ? byType.id : null;
}

function jumpToIssue(issueId) {
  document.querySelectorAll('.sc-modal-overlay').forEach(el => el.remove());

  if (issueId == null || issueId === '') {
    showNotification('Could not match Bob’s priority to an issue card.', 'warning');
    return;
  }

  const id = Number(issueId);
  const reportTab = document.querySelectorAll('.sc-tab')[1];
  if (reportTab && !reportTab.classList.contains('active')) {
    reportTab.click();
  }

  const filterRow = document.querySelector('.sc-filter-row');
  if (filterRow && currentFilter !== 'all') {
    const allBtn = filterRow.querySelector('.sc-filter-btn');
    if (allBtn) filterIssues('all', allBtn);
  }

  const card = document.getElementById('card-' + id);
  if (!card) {
    showNotification('That issue isn’t on the page — open the Report tab and try “All” filters.', 'warning');
    return;
  }

  const body = document.getElementById('body-' + id);
  if (body && !body.classList.contains('open')) {
    toggleIssue(id);
  }

  requestAnimationFrame(() => {
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.classList.remove('sc-priority-highlight');
    void card.offsetWidth;
    card.classList.add('sc-priority-highlight');
    setTimeout(() => card.classList.remove('sc-priority-highlight'), 2200);
  });
}

function showBobPriority() {
  if (!currentBobReport || !currentBobReport.bob_insights) {
    showNotification('⚠ No Bob insights available. Run a scan first.', 'warning');
    return;
  }
  
  const insights = currentBobReport.bob_insights;
  const priority = insights.priority_fix;
  
  if (!priority) {
    showNotification('No issues in this scan to prioritize.', 'info');
    return;
  }

  const priorityIssueId = resolvePriorityIssueId(priority);
  
  // Create modal to show Bob's priority recommendation
  const modal = document.createElement('div');
  modal.className = 'sc-modal-overlay';
  modal.onclick = (e) => {
    if (e.target === modal) modal.remove();
  };
  
  modal.innerHTML = `
    <div class="sc-modal">
      <div class="sc-modal-header">
        <div>
          <div class="sc-modal-title">🤖 Bob's Priority Recommendation</div>
          <div class="sc-modal-subtitle">Fix this issue first for maximum impact</div>
        </div>
        <button type="button" class="sc-modal-close" onclick="this.closest('.sc-modal-overlay').remove()" aria-label="Close modal">&times;</button>
      </div>
      
      <div class="sc-modal-body">
        <div class="sc-priority-box">
          <div class="sc-priority-label">PRIORITY FIX</div>
          <div class="sc-priority-issue">${escHtml(priority.issue)}</div>
          <div class="sc-priority-location">📄 ${escHtml(priority.file)} : Line ${escHtml(priority.line)}</div>
          <div class="sc-priority-reason">${escHtml(priority.reason)}</div>
        </div>
        
        <div class="sc-metrics-grid">
          <div class="sc-metric-box">
            <div class="sc-metric-label">ESTIMATED FIX TIME</div>
            <div class="sc-metric-value">${escHtml(insights.estimated_fix_time)}</div>
          </div>
          <div class="sc-metric-box">
            <div class="sc-metric-label">IMPACT SCORE</div>
            <div class="sc-metric-value" style="color:${insights.impact_score > 50 ? 'var(--ibm-red)' : '#b45309'}">
              ${insights.impact_score}/100
            </div>
          </div>
        </div>
        
        <div class="sc-compliance-box">
          <div class="sc-compliance-label">WCAG COMPLIANCE</div>
          <div class="sc-compliance-text">
            Level A: ${currentBobReport.wcag_compliance.level_a}% •
            Level AA: ${currentBobReport.wcag_compliance.level_aa}% •
            Level AAA: ${currentBobReport.wcag_compliance.level_aaa}%
          </div>
        </div>
        
        <button type="button" class="sc-btn sc-btn-primary sc-priority-gotit" style="width:100%">Got it, let's fix this!</button>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);

  const gotIt = modal.querySelector('.sc-priority-gotit');
  if (gotIt) {
    gotIt.addEventListener('click', () => jumpToIssue(priorityIssueId));
  }
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function escHtml(s) {
  if (s == null) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${type === 'success' ? '#24a148' : type === 'error' ? '#da1e28' : '#0f62fe'};
    color: white;
    padding: 12px 20px;
    border-radius: 4px;
    font-size: 13px;
    z-index: 10000;
    box-shadow: 0 4px 12px rgba(0,0,0,.15);
    animation: slideIn 0.3s ease;
  `;
  notification.textContent = message;
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(400px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(400px); opacity: 0; }
  }
  .sc-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    animation: fadeIn 0.2s ease;
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  .sc-issue-card.sc-priority-highlight {
    animation: scPriorityPulse 1.1s ease-out 2;
    box-shadow: 0 0 0 3px rgba(234, 179, 8, 0.95), 0 8px 24px rgba(0,0,0,.12);
    border-radius: 8px;
  }
  @keyframes scPriorityPulse {
    0% { box-shadow: 0 0 0 0 rgba(234, 179, 8, 0.7); }
    40% { box-shadow: 0 0 0 10px rgba(234, 179, 8, 0.25); }
    100% { box-shadow: 0 0 0 3px rgba(234, 179, 8, 0.95), 0 8px 24px rgba(0,0,0,.12); }
  }
`;
document.head.appendChild(style);

// ============================================================
// BUTTON CLICK HANDLERS (called from HTML)
// ============================================================

function sendPrompt(prompt) {
  if (prompt.includes('Generate PDF Report') || prompt.includes('Generate a WCAG')) {
    exportBobReport();
  } else if (
    prompt.includes('priority') ||
    prompt.includes('Ask Bob') ||
    prompt.includes('most critical accessibility fix')
  ) {
    showBobPriority();
  } else {
    showNotification('Unknown action.', 'info');
  }
}

// ============================================================
// INITIALIZE ON PAGE LOAD
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  console.log('ScriptClean A11y Guard initialized');
  console.log('API Base:', API_BASE);
  
  fetch(`${API_BASE}/health`)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then(data => {
      console.log('✓ Server connected:', data);
      showNotification('Connected to IBM Bob server', 'success');
    })
    .catch(err => {
      console.warn('Server not responding:', err);
      showNotification(
        `Server not reachable. Run: python server/app.py — then open http://127.0.0.1:${DEFAULT_DEV_PORT}/app/`,
        'warning'
      );
    });
});

// Made with Bob
