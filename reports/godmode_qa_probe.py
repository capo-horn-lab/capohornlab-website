from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

BASE = "https://www.capohornlab.com/"
ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "/", "/index.html", "/about.html", "/method.html", "/research.html",
    "/research-detail.html", "/test-strategy.html", "/contact.html", "/login.html",
    "/signup.html", "/dashboard.html", "/checkout.html", "/faq.html", "/documentation.html",
    "/privacy-policy.html", "/terms-of-service.html", "/cookie-policy.html", "/disclaimer.html",
    "/refund-policy.html", "/investors.html",
] + ["/pages/" + p.name for p in sorted((ROOT / "pages").glob("*.html"))]


def get(url: str):
    req = Request(url, headers={"User-Agent": "CapoHornLab-QA/1.0"})
    try:
        with urlopen(req, timeout=25) as r:
            raw = r.read()
            return {"status": r.status, "bytes": len(raw), "text": raw.decode("utf-8", "replace"), "url": r.url}
    except Exception as exc:
        return {"status": 0, "bytes": 0, "text": "", "error": str(exc)}

live = {}
for path in PAGES:
    live[path] = get(BASE.rstrip("/") + path + "?v=godmodeqa20260819")

local_files = sorted(list(ROOT.glob("*.html")) + list((ROOT / "pages").glob("*.html")))
source = {}
for file in local_files:
    text = file.read_text(encoding="utf-8", errors="replace")
    source[str(file.relative_to(ROOT)).replace("\\", "/")] = {
        "bytes": len(text.encode()),
        "todo": len(re.findall(r"\bTODO\b", text, re.I)),
        "lorem": len(re.findall(r"lorem ipsum", text, re.I)),
        "dead_href": len(re.findall(r"href\s*=\s*(['\"])#\1", text, re.I)),
        "title": bool(re.search(r"<title>\s*[^<]+", text, re.I)),
        "viewport": bool(re.search(r"name\s*=\s*(['\"])viewport\1", text, re.I)),
    }

for slug in ["nq-rth-directional-screen", "news-event-long-horizon-es"]:
    for path in ["/research.html", "/research-detail.html"]:
        live[path]["slug_" + slug] = live[path]["text"].count(slug)

result = {"base": BASE, "pages": {k: {x: v for x, v in d.items() if x != "text"} for k, d in live.items()}, "source": source}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
