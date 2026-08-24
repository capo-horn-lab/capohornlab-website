# -*- coding: utf-8 -*-
"""Fix: (1) corrupted var(--ch-ink):/var(--ch-abyss): property names,
        (2) duplicate/leaked --ch-font-serif token declarations."""
import glob, os, re

BASE = "D:/CapoHornLab/projects/capohornlab-website"

TARGET_SERIF = "--ch-font-serif: 'Playfair Display', Georgia, 'Times New Roman', serif;"

def fix_page(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    orig = c

    # 1. Fix corrupted property names
    c = c.replace("var(--ch-ink):", "--ch-ink:")
    c = c.replace("var(--ch-abyss):", "--ch-abyss:")

    # 2. Remove duplicate --ch-font-serif token lines (keep only the :root one)
    if c.count(TARGET_SERIF) > 1:
        lines = c.split("\n")
        out = []
        kept = False
        for line in lines:
            if line.strip() == TARGET_SERIF:
                if not kept:
                    kept = True
                    out.append(line)   # keep the :root definition
                # else: drop duplicate
            else:
                out.append(line)
        c = "\n".join(out)

    if c != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        return True
    return False

changed = []
for path in sorted(glob.glob(os.path.join(BASE, "*.html"))):
    if fix_page(path):
        changed.append(os.path.basename(path))

print("Fixed %d pages:" % len(changed))
for n in changed:
    print("  +", n)

# ── Verify no remaining corruption/leaks ──
print("\n=== post-fix verification ===")
for path in sorted(glob.glob(os.path.join(BASE, "*.html"))):
    name = os.path.basename(path)
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    issues = []
    if "var(--ch-ink):" in c or "var(--ch-abyss):" in c:
        issues.append("var(--ch-*): corruption")
    if c.count(TARGET_SERIF) > 1:
        issues.append("serif token x%d" % c.count(TARGET_SERIF))
    # body leak check
    body_idx = c.find("<body")
    if body_idx != -1 and TARGET_SERIF in c[body_idx:]:
        issues.append("serif token LEAKED in body")
    if issues:
        print("  %-26s %s" % (name, ", ".join(issues)))
print("\n(done — empty above = all clean)")
