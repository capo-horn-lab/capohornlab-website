from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / 'research-detail.html', ROOT / 'pages' / 'research-detail.html']
IDS = [
    '01_equity_curve', '02_drawdown', '03_trade_distribution',
    '04_monthly_heatmap', '05_long_vs_short', '06_performance_table',
    '07_is_vs_oos',
]
array_re = re.compile(r'("chart_descriptions"\s*:\s*\[)(.*?)(\])', re.S)
id_re = re.compile(r'("id"\s*:\s*")[^"]+(")')
for file in FILES:
    text = file.read_text(encoding='utf-8')
    count = 0
    def normalize(match):
        nonlocal_count = [0]
        def replace_id(id_match):
            idx = nonlocal_count[0]
            nonlocal_count[0] += 1
            if idx >= len(IDS):
                raise ValueError(f'{file}: chart list exceeds {len(IDS)}')
            return id_match.group(1) + IDS[idx] + id_match.group(2)
        body = id_re.sub(replace_id, match.group(2))
        if nonlocal_count[0] != len(IDS):
            raise ValueError(f'{file}: expected {len(IDS)} chart ids, got {nonlocal_count[0]}')
        return match.group(1) + body + match.group(3)
    new, count = array_re.subn(normalize, text)
    if count != 13:
        raise ValueError(f'{file}: expected 13 chart arrays, got {count}')
    file.write_text(new, encoding='utf-8')
    print(f'NORMALIZED {file.name}: {count} chart arrays')
