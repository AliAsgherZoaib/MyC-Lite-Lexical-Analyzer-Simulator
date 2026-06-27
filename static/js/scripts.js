// Tab Controller Switcher Mechanics
function switchTab(tabId) {
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Clear Interface Workspace Fields
function clearEditor() {
    document.getElementById('codeEditor').value = '';
    location.reload(); 
}

// Local Document File Upload Parsing Reader Handler
document.getElementById('fileUpload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(evt) {
        document.getElementById('codeEditor').value = evt.target.result;
    };
    reader.readAsText(file);
});

// UI Pipeline Step Control Highlight Engine Animation
function cyclePipelineHighlight() {
    const steps = ['step-source', 'step-scanner', 'step-lexeme', 'step-tokens', 'step-symtab', 'step-errors'];
    steps.forEach((step, idx) => {
        setTimeout(() => {
            document.querySelectorAll('.flow-step').forEach(el => el.classList.remove('active'));
            document.getElementById(step).classList.add('active');
        }, idx * 150);
    });
}

// Primary Core Processing Pipeline via AJAX Request Routing Execution
function processAnalysis() {
    const rawCode = document.getElementById('codeEditor').value;
    cyclePipelineHighlight();

    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: rawCode })
    })
    .then(res => res.json())
    .then(data => {
        updateStatsDashboard(data.stats);
        renderTokens(data.tokens);
        renderSymbolTable(data.symbol_table);
        renderErrorsAndWarnings(data.errors, data.warnings);
        renderExecutionTrace(data.trace);
    })
    .catch(err => console.error("Communication channel exception failure encountered:", err));
}

function updateStatsDashboard(stats) {
    const container = document.getElementById('statsContainer');
    container.innerHTML = `
        <div class="card"><h3>${stats.total_tokens}</h3><p>Total Tokens</p></div>
        <div class="card" style="border-color:#10b981"><h3>${stats.keywords}</h3><p>Keywords</p></div>
        <div class="card" style="border-color:#38bdf8"><h3>${stats.identifiers}</h3><p>Identifiers</p></div>
        <div class="card" style="border-color:#a855f7"><h3>${stats.constants}</h3><p>Constants</p></div>
        <div class="card" style="border-color:#ef4444"><h3>${stats.errors}</h3><p>Errors</p></div>
    `;
}

function renderTokens(tokens) {
    const tbody = document.getElementById('tokenTableBody');
    if(tokens.length === 0) {
        tbody.innerHTML = `<tr><td colspan="3" class="placeholder">No valid operational tokens derived.</td></tr>`;
        return;
    }
    tbody.innerHTML = tokens.map(t => `
        <tr>
            <td><strong>${escapeHtml(t.lexeme)}</strong></td>
            <td><span class="badge">${t.type}</span></td>
            <td>${t.line}</td>
        </tr>
    `).join('');
}

function renderSymbolTable(symtab) {
    const tbody = document.getElementById('symbolTableBody');
    if(symtab.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="placeholder">Symbol Table completely empty.</td></tr>`;
        return;
    }
    tbody.innerHTML = symtab.map(s => `
        <tr>
            <td><code>${escapeHtml(s.name)}</code></td>
            <td>${s.type}</td>
            <td>${s.scope}</td>
            <td>0x${s.address.toString(16).toUpperCase()}</td>
            <td>${s.line}</td>
            <td style="font-size:0.85rem; color:#94a3b8">${s.reason}</td>
        </tr>
    `).join('');
}

function renderErrorsAndWarnings(errors, warnings) {
    const container = document.getElementById('errorWarningContent');
    if(errors.length === 0 && warnings.length === 0) {
        container.innerHTML = `<p class="placeholder" style="color:#10b981">✓ Lexical validation passed without issues!</p>`;
        return;
    }
    
    let html = '';
    errors.forEach(e => {
        html += `
            <div class="alert-box error">
                <strong>[LINE ${e.line}] LEXICAL ERROR: ${e.error_type}</strong><br>
                <span style="color:#f8fafc">${escapeHtml(e.message)}</span><br>
                <small style="color:#fca5a5">💡 Suggested Resolution: ${escapeHtml(e.suggested_fix)}</small>
            </div>`;
    });
    
    warnings.forEach(w => {
        html += `
            <div class="alert-box warning">
                <strong>[LINE ${w.line}] STATIC ANALYSIS WARNING:</strong><br>
                <span style="color:#f8fafc">${escapeHtml(w.message)} (Lexeme: '<code>${escapeHtml(w.lexeme)}</code>')</span>
            </div>`;
    });
    
    container.innerHTML = html;
}

function renderExecutionTrace(trace) {
    const consoleLog = document.getElementById('traceConsoleLog');
    if(trace.length === 0) {
        consoleLog.innerText = "Trace empty.";
        return;
    }
    consoleLog.innerText = trace.join('\n');
}

function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
