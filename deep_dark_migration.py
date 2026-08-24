# -*- coding: utf-8 -*-
"""Deep dark-mode migration: convert light sections + blue text to Observatory dark/red."""
import os, re

BASE = "D:/CapoHornLab/projects/capohornlab-website"
PAGES = ["about.html", "contact.html", "dashboard.html", "documentation.html",
         "faq.html", "login.html", "method.html", "pricing.html", "research.html",
         "research-detail.html", "signup.html", "test-strategy.html"]

# Light backgrounds -> dark surfaces
BG_SUBS = [
    (r"background\s*:\s*var\(--ch-white\)", "background:#0c1420"),
    (r"background\s*:\s*var\(--ch-off-white\)", "background:#0c1420"),
    (r"background\s*:\s*var\(--ch-gray-50\)", "background:#0c1420"),
    (r"background\s*:\s*var\(--ch-gray-100\)", "background:#102438"),
    (r"background\s*:\s*var\(--ch-gray-200\)", "background:#12253c"),
    (r"background\s*:\s*var\(--ch-blue-50\)", "background:rgba(227,59,47,0.06)"),
    (r"background\s*:\s*var\(--ch-blue-100\)", "background:rgba(227,59,47,0.08)"),
    (r"background-color\s*:\s*var\(--ch-white\)", "background-color:#0c1420"),
    (r"background-color\s*:\s*var\(--ch-off-white\)", "background-color:#0c1420"),
]

# Dark text (was on light bg) -> light text
TEXT_SUBS = [
    (r"color\s*:\s*var\(--ch-navy-900\)", "color:#f2e7e3"),
    (r"color\s*:\s*var\(--ch-gray-900\)", "color:#f2e7e3"),
    (r"color\s*:\s*var\(--ch-gray-800\)", "color:#f2e7e3"),
    (r"color\s*:\s*var\(--ch-gray-700\)", "color:#cfb6ae"),
    (r"color\s*:\s*var\(--ch-gray-600\)", "color:#cfb6ae"),
    (r"color\s*:\s*var\(--ch-gray-500\)", "color:#9d746d"),
    (r"color\s*:\s*var\(--ch-navy-800\)", "color:#cfb6ae"),
    (r"color\s*:\s*var\(--ch-navy-700\)", "color:#cfb6ae"),
]

# Residual blue-ish hex values -> warm neutrals
HEX_SUBS = [
    ("#45719a", "#cfb6ae"),
    ("#7da3c4", "#f2e7e3"),
    ("#cfe0ee", "#9d746d"),
]

def migrate(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    orig = c
    n = 0
    for pat, rep in BG_SUBS:
        c, k = re.subn(pat, rep, c)
        n += k
    for pat, rep in TEXT_SUBS:
        c, k = re.subn(pat, rep, c)
        n += k
    for old, new in HEX_SUBS:
        k = c.count(old)
        c = c.replace(old, new)
        n += k
    if c != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
    return n

for p in PAGES:
    path = os.path.join(BASE, p)
    if os.path.exists(path):
        n = migrate(path)
        print(f"{p}: {n} substitutions")
    else:
        print(f"MISSING {p}")
print("\nDone")
