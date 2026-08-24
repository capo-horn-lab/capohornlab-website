# -*- coding: utf-8 -*-
"""Migrate all Capo Horn Lab pages from navy/blue to Observatory signal-red design system.
Keeps variable names, swaps values. Preserves layout + content."""
import os, re

BASE = "D:/CapoHornLab/projects/capohornlab-website"
PAGES = [
    "about.html", "contact.html", "dashboard.html", "login.html", "method.html",
    "pricing.html", "research.html", "research-detail.html", "test-strategy.html",
    "signup.html", "faq.html", "documentation.html",
]

# (old -> new) exact value swaps. Variable NAMES unchanged.
COLOR_MAP = [
    # Navy (dark surfaces) -> observatory ocean ink
    ("#0a1628", "#070b12"),
    ("#0f1e36", "#0c1420"),
    ("#152a45", "#102438"),
    ("#1c3a5c", "#12253c"),
    ("#254e77", "#17304a"),
    ("#3b6fa0", "#1e3d5e"),
    ("#5e93c2", "#2d5577"),
    ("#8fb8da", "#45719a"),
    ("#c1d6ec", "#7da3c4"),
    ("#e8f0f8", "#cfe0ee"),
    # Blue (accent) -> signal red
    ("#1e40af", "#a8231b"),
    ("#1d4ed8", "#c8322a"),
    ("#2563eb", "#e33b2f"),
    ("#3b82f6", "#ff5c47"),
    ("#60a5fa", "#ff7a66"),
    ("#93c5fd", "#ffa08f"),
    ("#dbeafe", "#ffd0c7"),
    ("#eff6ff", "#fff0ed"),
    # Amber -> warm orange
    ("#f59e0b", "#ff9b64"),
    ("#fbbf24", "#ffab78"),
    ("#fcd34d", "#ffc092"),
    ("#fde68a", "#ffd4ae"),
    ("#fef3c7", "#ffe7d4"),
    ("#fffbeb", "#fff3ec"),
    # Semantic
    ("#10b981", "#5cb8a5"),
    ("#ef4444", "#ff7067"),
    ("#059669", "#4a9d8c"),
    # rgba blue -> rgba signal red
    ("rgba(37,99,235,", "rgba(227,59,47,"),
    ("rgba(59,130,246,", "rgba(255,92,71,"),
    ("rgba(30,64,175,", "rgba(168,35,27,"),
    ("rgba(29,78,216,", "rgba(200,50,42,"),
    ("rgba(16,185,129,", "rgba(92,184,165,"),
]

# Font link replacement (regex)
FONT_LINK_RE = re.compile(
    r"family=Inter[^&]*&family=JetBrains\+Mono:[^&'\"&]*"
)
NEW_FONT_LINK = (
    "family=DM+Mono:wght@400;500&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700"
    "&family=Playfair+Display:ital,wght@0,600;0,700;1,600"
)

# Font token replacements
FONT_TOKENS = [
    (
        "--ch-font-sans:   'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;",
        "--ch-font-sans:   'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;"
    ),
    (
        "--ch-font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;",
        "--ch-font-sans: 'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;"
    ),
    (
        "--ch-font-mono:   'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace;",
        "--ch-font-mono:   'DM Mono', 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;"
    ),
    (
        "--ch-font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace;",
        "--ch-font-mono: 'DM Mono', 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;"
    ),
]

# Serif token to inject after --ch-font-mono line
SERIF_TOKEN = "      --ch-font-serif: 'Playfair Display', Georgia, 'Times New Roman', serif;\n"

# Serif heading override to inject before </head>
SERIF_HEAD_CSS = """
    /* Observatory red — serif display headings */
    h1, h2, .display, .hero h1, .section-header h2 { font-family: var(--ch-font-serif), Georgia, serif !important; letter-spacing: -0.035em; }
"""

def migrate(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    orig = c

    # 1. Font link
    c = FONT_LINK_RE.sub(lambda m: NEW_FONT_LINK, c)

    # 2. Font tokens
    for old, new in FONT_TOKENS:
        c = c.replace(old, new)

    # 3. Inject serif token after font-mono declaration
    if "--ch-font-serif" not in c and "--ch-font-mono" in c:
        # find the --ch-font-mono line and append serif after it
        lines = c.split("\n")
        out = []
        for ln in lines:
            out.append(ln)
            if "--ch-font-mono" in ln and "--ch-font-serif" not in ln and ":" in ln:
                out.append(SERIF_TOKEN.rstrip("\n"))
        c = "\n".join(out)

    # 4. Color swaps
    for old, new in COLOR_MAP:
        c = c.replace(old, new)

    # 5. Serif heading override before </head>
    if "</head>" in c and "serif display headings" not in c:
        c = c.replace("</head>", SERIF_HEAD_CSS + "\n</head>", 1)

    if c != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        return True
    return False

if __name__ == "__main__":
    for p in PAGES:
        path = os.path.join(BASE, p)
        if os.path.exists(path):
            changed = migrate(path)
            print(f"{'OK' if changed else 'SKIP'}: {p}")
        else:
            print(f"MISSING: {p}")
    print("\nDone.")
