"""Offline static QA for public Capo Horn Lab HTML pages; emits evidence JSON."""
from __future__ import annotations
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', '.venv', 'design', 'node_modules', '__pycache__'}
# Generated Plotly fragments are chart assets embedded by the canonical research
# page, not standalone site pages. Their document shell is intentionally absent.
HTML = sorted(
    p for p in ROOT.rglob('*.html')
    if not any(part in EXCLUDED for part in p.parts)
    and not p.as_posix().startswith((ROOT / 'research' / 'charts').as_posix())
    and not p.as_posix().startswith((ROOT / 'research' / 'runs').as_posix())
)
ATTR = re.compile(r'''(?:href|src)\s*=\s*["']([^"']+)["']''', re.I)
ID = re.compile(r'''\bid\s*=\s*["']([^"']+)["']''', re.I)
findings = []
references = 0
for page in HTML:
    text = page.read_text(encoding='utf-8', errors='replace')
    rel = page.relative_to(ROOT).as_posix()
    for label, required in [('doctype', '<!doctype html'), ('title', '<title'), ('viewport', 'name="viewport"')]:
        if required not in text.lower():
            findings.append({'page': rel, 'kind': 'html', 'detail': f'missing {label}'})
    ids = set(ID.findall(text))
    for raw in ATTR.findall(text):
        raw = raw.strip()
        references += 1
        if raw in ('', '#'):
            findings.append({'page': rel, 'kind': 'reference', 'detail': f'dead reference {raw!r}'})
            continue
        parts = urlsplit(raw)
        if parts.scheme in ('http', 'https', 'mailto', 'tel', 'data', 'javascript'):
            continue
        target = unquote(parts.path)
        if not target:
            if parts.fragment and parts.fragment not in ids:
                findings.append({'page': rel, 'kind': 'anchor', 'detail': f'missing #{parts.fragment}'})
            continue
        resolved = (page.parent / target).resolve()
        if not resolved.exists():
            findings.append({'page': rel, 'kind': 'reference', 'detail': f'missing {raw}'})
        if parts.fragment and resolved == page.resolve() and parts.fragment not in ids:
            findings.append({'page': rel, 'kind': 'anchor', 'detail': f'missing #{parts.fragment}'})
result = {'pages': len(HTML), 'references': references, 'findings': findings, 'passed': not findings}
out = ROOT / 'reports' / 'qa-current-cycle.json'
out.write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
raise SystemExit(0 if not findings else 1)
