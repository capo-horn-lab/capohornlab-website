from pathlib import Path

root = Path(r"D:/CapoHornLab/projects/capohornlab-website")

def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"Expected unique source not found in {path.name}: {old[:70]}")
    if text.count(old) != 1:
        raise RuntimeError(f"Source not unique in {path.name}: {text.count(old)} matches")
    path.write_text(text.replace(old, new), encoding="utf-8")

# Dashboard: no account may be rendered with simulated holdings or client-only subscription state.
dashboard = root / "dashboard.html"
replace_once(dashboard,
'''          <div class="summary-card animate-up-d5" style="border-color:var(--ch-amber-300);background:linear-gradient(135deg,var(--ch-white),#fffbeb);">
            <div class="label">Data Portfolio</div>
            <div class="value" style="font-size:var(--ch-text-base);color:var(--ch-amber-600);">1 dataset</div>
            <div class="sub">NQ 1-Min Tick · 1 Year</div>
          </div>''',
'''          <div class="summary-card animate-up-d5" id="portfolioSummaryCard">
            <div class="label">Data Portfolio</div>
            <div class="value" style="font-size:var(--ch-text-base);">0 datasets</div>
            <div class="sub">No completed purchases recorded</div>
          </div>''')
replace_once(dashboard,
'''            <span class="count">3</span>''',
'''            <span class="count">0</span>''')
replace_once(dashboard,
'''                <button class="btn btn-secondary btn-sm" onclick="this.textContent='✓ Subscribed!'; this.disabled=true; setTimeout(()=>{this.textContent='Subscribed'; this.disabled=false}, 3000);">Subscribed</button>''',
'''                <span class="field-value">Newsletter preferences are confirmed through the double-opt-in email flow.</span>''')
replace_once(dashboard,
'''    function loadRequests() {
      window.CHLAccount.listRequests().then(function(payload) {
        var rows = document.querySelector('#requestsTable tbody');
        var count = document.querySelector('.section-title .count');
        var items = payload.items || [];
        if (count) count.textContent = String(payload.total || items.length);''',
'''    function loadRequests() {
      window.CHLAccount.listRequests().then(function(payload) {
        var rows = document.querySelector('#requestsTable tbody');
        var count = document.querySelector('.section-title .count');
        var items = payload.items || [];
        renderRequestSummary(items, payload.total || items.length);
        if (count) count.textContent = String(payload.total || items.length);''')
replace_once(dashboard,
'''    /* ---- Tab Switching ---- */''',
'''    function renderRequestSummary(items, total) {
      var cards = document.querySelectorAll('#summaryCards .summary-card .value');
      if (cards.length < 4) return;
      var latest = items[0];
      var inProgress = items.filter(function(item) { return ['inviata', 'info_mancanti', 'in_valutazione', 'in_lavorazione'].indexOf(item.status) !== -1; }).length;
      var completed = items.filter(function(item) { return item.status === 'completata'; }).length;
      cards[0].textContent = String(total);
      cards[1].textContent = latest && (latest.strategy_name || '—') || '—';
      cards[2].textContent = String(inProgress);
      cards[3].textContent = String(completed);
    }

    /* ---- Tab Switching ---- */''')

# Strategy intake: promotions cannot be made up from browser localStorage; confirmation has no fictitious request id.
strategy = root / "test-strategy.html"
replace_once(strategy,
'''                 <div style="display:flex;gap:var(--ch-space-2);align-items:center;flex-wrap:wrap;">
                   <input class="input-field" id="discountInput" type="text" placeholder="Enter code" style="flex:1;min-width:150px;padding:var(--ch-space-2) var(--ch-space-3);text-transform:uppercase;">
                   <button class="btn btn-secondary btn-sm" onclick="applyDiscountCode()" type="button">Apply</button>
                   <span id="discountMsg" style="font-size:var(--ch-text-xs);min-height:1.2em;"></span>
                 </div>''',
'''                 <p style="font-size:var(--ch-text-xs);color:var(--ch-gray-400);">Promotions are applied only after server-side validation during checkout.</p>''')
replace_once(strategy,
'''              <div class="submission-id">Request ID: CH-2026-XXXX</div>''',
'''              <div class="submission-id">A request ID is issued only after the authenticated submission succeeds.</div>''')
start = '''    // ---- Discount Code ----
    function applyDiscountCode() {'''
text = strategy.read_text(encoding="utf-8")
i = text.find(start)
end = text.find('    // ---- Submit ----', i)
if i < 0 or end < 0:
    raise RuntimeError('Discount-code script boundaries not found')
strategy.write_text(text[:i] + '    // Promotions are deliberately server-side only.\n\n' + text[end:], encoding="utf-8")

for p in (dashboard, strategy):
    tail = p.read_text(encoding="utf-8").rstrip()
    if not tail.endswith("</html>"):
        raise RuntimeError(f"HTML tail invalid: {p}")
print("Updated dashboard.html and test-strategy.html")
