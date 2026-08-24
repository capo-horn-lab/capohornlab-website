# -*- coding: utf-8 -*-
"""Fix navy backgrounds + inject unified left sidebar into all public pages.
Excludes admin.html and legacy crypto-* standalone pages."""
import os, re, glob

BASE = "D:/CapoHornLab/projects/capohornlab-website"

EXCLUDE = {"admin.html", "crypto-cards.html", "crypto-price-cards.html", "crypto-prices.html"}

LINK = '<link rel="stylesheet" href="assets/css/sidebar.css">'
SCRIPT = '<script src="assets/js/sidebar.js"></script>'

def fix_page(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    orig = c

    # 1. Fix opaque navy body background -> ink token
    c = re.sub(r'background\s*:\s*#0c1420\s*;?', 'background:var(--ch-ink);', c)

    # 2. Fix broken double-var
    c = c.replace('background: var(var(--ch-ink));', 'background: var(--ch-ink);')

    # 3. Fix navy page-hero / section backgrounds -> transparent (let orbit show)
    c = re.sub(r'background\s*:\s*var\(--ch-navy-\d+\)\s*;?', 'background:transparent;', c)

    # 4. Inject sidebar CSS link before </head>
    if 'assets/css/sidebar.css' not in c:
        c = c.replace('</head>', LINK + '\n</head>', 1)

    # 5. Inject sidebar JS before </body>
    if 'assets/js/sidebar.js' not in c:
        c = c.replace('</body>', SCRIPT + '\n</body>', 1)

    if c != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        return True
    return False

changed = []
skipped = []
for path in sorted(glob.glob(os.path.join(BASE, "*.html"))):
    name = os.path.basename(path)
    if name in EXCLUDE:
        skipped.append(name)
        continue
    if fix_page(path):
        changed.append(name)

print("CHANGED (%d):" % len(changed))
for n in changed:
    print("  +", n)
print("\nSKIPPED (excluded):", skipped)
