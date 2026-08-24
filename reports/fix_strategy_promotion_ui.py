from pathlib import Path

p = Path(r"D:/CapoHornLab/projects/capohornlab-website/test-strategy.html")
text = p.read_text(encoding="utf-8")
old = '''              <!-- Discount Code -->
              <div class="review-card" style="margin-top:var(--ch-space-4);">
                <div class="review-card-title">Discount Code</div>
                <div style="display:flex;gap:var(--ch-space-3);align-items:center;margin-top:var(--ch-space-3);flex-wrap:wrap;">
                  <input class="input-field" id="discountInput" type="text" placeholder="Enter code" style="flex:1;min-width:150px;padding:var(--ch-space-2) var(--ch-space-3);text-transform:uppercase;">
                  <button class="btn btn-secondary btn-sm" onclick="applyDiscountCode()" type="button">Apply</button>
                  <span id="discountMsg" style="font-size:var(--ch-text-xs);min-height:1.2em;"></span>
                </div>
              </div>'''
new = '''              <div class="review-card" style="margin-top:var(--ch-space-4);">
                <div class="review-card-title">Promotions</div>
                <p style="font-size:var(--ch-text-xs);color:var(--ch-gray-400);">Promotions are applied only after server-side validation during checkout.</p>
              </div>'''
if text.count(old) != 1:
    raise RuntimeError(f"Promotion markup occurrences: {text.count(old)}")
text = text.replace(old, new)
old_id = '<div class="submission-id">Request ID: CH-2026-XXXX</div>'
new_id = '<div class="submission-id">A request ID is issued only after the authenticated submission succeeds.</div>'
if text.count(old_id) != 1:
    raise RuntimeError(f"Mock request id occurrences: {text.count(old_id)}")
text = text.replace(old_id, new_id)
start = text.find('    // ---- Discount Code ----\n    function applyDiscountCode() {')
end = text.find('    // ---- Submit ----', start)
if start < 0 or end < 0:
    raise RuntimeError('Promotion script boundaries not found')
text = text[:start] + '    // Promotions are deliberately server-side only.\n\n' + text[end:]
if not text.rstrip().endswith('</html>'):
    raise RuntimeError('HTML tail invalid')
p.write_text(text, encoding='utf-8')
print('Updated test-strategy.html')
