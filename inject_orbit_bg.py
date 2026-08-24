# -*- coding: utf-8 -*-
"""Inject orbit-background.js into all pages, before </body>."""
import os

BASE = "D:/CapoHornLab/projects/capohornlab-website"
PAGES = ["index.html", "about.html", "contact.html", "dashboard.html", "documentation.html",
         "faq.html", "login.html", "method.html", "pricing.html", "research.html",
         "research-detail.html", "signup.html", "test-strategy.html"]

SCRIPT_TAG = '<script src="assets/js/orbit-background.js"></script>'

for p in PAGES:
    path = os.path.join(BASE, p)
    if not os.path.exists(path):
        print(f"MISSING {p}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    if "orbit-background.js" in c:
        print(f"SKIP {p}: already has orbit bg")
        continue

    if "</body>" in c:
        c = c.replace("</body>", "  " + SCRIPT_TAG + "\n</body>", 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"OK {p}: orbit bg injected")
    else:
        print(f"WARN {p}: no </body>")

print("\nDone")
