from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'research-detail.html').read_text(encoding='utf-8')
pairs = re.findall(r'"charts_slug"\s*:\s*"([^"]+)".*?"chart_descriptions"\s*:\s*\[(.*?)\]', text, re.S)
checks = []
for directory, body in pairs:
    for chart_id in re.findall(r'"id"\s*:\s*"([^"]+)"', body):
        file = ROOT / 'research' / 'charts' / directory / f'{chart_id}.png'
        checks.append(file)
missing = [str(x.relative_to(ROOT)) for x in checks if not x.is_file() or x.stat().st_size == 0]
print(f'charts={len(checks)} present={len(checks)-len(missing)} missing={len(missing)}')
for item in missing: print(item)
raise SystemExit(1 if missing or len(checks) != 91 else 0)
