# -*- coding: utf-8 -*-
"""Migrate legal pages to Observatory dark/red (palette + dark + orbit + logo)."""
import os, re

BASE = "D:/CapoHornLab/projects/capohornlab-website"
PAGES = ["cookie-policy.html", "disclaimer.html", "investors.html", "privacy-policy.html",
         "refund-policy.html", "terms-of-service.html", "checkout.html"]

# 1. Palette hex map (navy/blue -> observatory)
COLOR_MAP = [
    ("#0a1628", "#070b12"), ("#0f1e36", "#0c1420"), ("#152a45", "#102438"),
    ("#1c3a5c", "#12253c"), ("#254e77", "#17304a"), ("#3b6fa0", "#1e3d5e"),
    ("#5e93c2", "#2d5577"), ("#8fb8da", "#cfb6ae"), ("#c1d6ec", "#f2e7e3"),
    ("#e8f0f8", "#9d746d"),
    ("#1e40af", "#a8231b"), ("#1d4ed8", "#c8322a"), ("#2563eb", "#e33b2f"),
    ("#3b82f6", "#ff5c47"), ("#60a5fa", "#ff7a66"), ("#93c5fd", "#ffa08f"),
    ("#dbeafe", "#ffd0c7"), ("#eff6ff", "#fff0ed"),
    ("#f59e0b", "#ff9b64"), ("#fbbf24", "#ffab78"), ("#fcd34d", "#ffc092"),
    ("#fde68a", "#ffd4ae"), ("#fef3c7", "#ffe7d4"), ("#fffbeb", "#fff3ec"),
    ("#10b981", "#5cb8a5"), ("#ef4444", "#ff7067"), ("#059669", "#4a9d8c"),
    ("rgba(37,99,235,", "rgba(227,59,47,"), ("rgba(59,130,246,", "rgba(255,92,71,"),
    ("rgba(30,64,175,", "rgba(168,35,27,"), ("rgba(29,78,216,", "rgba(200,50,42,"),
    ("rgba(16,185,129,", "rgba(92,184,165,"),
]

# 2. Font tokens
FONT_LINK_RE = re.compile(r"family=Inter[^&]*&family=JetBrains\+Mono:[^&\"'&]*")
NEW_FONT_LINK = ("family=DM+Mono:wght@400;500&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700"
                 "&family=Playfair+Display:ital,wght@0,600;0,700;1,600")

# 3. Dark migration: light bg -> dark, dark text -> light
BG_SUBS = [
    (r"background\s*:\s*var\(--ch-white\)", "background:#0c1420"),
    (r"background\s*:\s*var\(--ch-off-white\)", "background:#0c1420"),
    (r"background\s*:\s*var\(--ch-gray-50\)", "background:#0c1420"),
    (r"background\s*:\s*var\(--ch-gray-100\)", "background:#102438"),
    (r"background\s*:\s*var\(--ch-gray-200\)", "background:#12253c"),
    (r"background-color\s*:\s*var\(--ch-white\)", "background-color:#0c1420"),
]
TEXT_SUBS = [
    (r"color\s*:\s*var\(--ch-navy-900\)", "color:#f2e7e3"),
    (r"color\s*:\s*var\(--ch-gray-900\)", "color:#f2e7e3"),
    (r"color\s*:\s*var\(--ch-gray-800\)", "color:#f2e7e3"),
    (r"color\s*:\s*var\(--ch-gray-700\)", "color:#cfb6ae"),
    (r"color\s*:\s*var\(--ch-gray-600\)", "color:#cfb6ae"),
    (r"color\s*:\s*var\(--ch-navy-800\)", "color:#cfb6ae"),
    (r"color\s*:\s*var\(--ch-navy-700\)", "color:#cfb6ae"),
]

ORBIT_SCRIPT = '<script src="assets/js/orbit-background.js"></script>'

def migrate(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    orig = c

    # Font link
    c = FONT_LINK_RE.sub(lambda m: NEW_FONT_LINK, c)

    # Font tokens
    c = c.replace("'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;",
                  "'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;")
    c = c.replace("'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace;",
                  "'DM Mono', 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;")

    # Color map
    for old, new in COLOR_MAP:
        c = c.replace(old, new)

    # Dark migration
    for pat, rep in BG_SUBS + TEXT_SUBS:
        c = re.sub(pat, rep, c)

    # Logo PNG -> orbit SVG
    c = c.replace("assets/logo/capo-horn-lab-logo.png", "assets/capo-horn-lab-orbit-mark.svg")

    # Github link
    c = c.replace("github.com/capohornlab", "github.com/capo-horn-lab")

    # Orbit background script
    if "orbit-background.js" not in c and "</body>" in c:
        c = c.replace("</body>", "  " + ORBIT_SCRIPT + "\n</body>", 1)

    if c != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        return True
    return False

for p in PAGES:
    path = os.path.join(BASE, p)
    if os.path.exists(path):
        print(f"{'OK' if migrate(path) else 'SKIP'}: {p}")
    else:
        print(f"MISSING {p}")
print("\nDone")
