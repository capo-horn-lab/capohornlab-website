"""Extract FOMC meeting dates and rate actions 2020-2024 from Wikipedia.

Source: https://en.wikipedia.org/wiki/History_of_Federal_Open_Market_Committee_actions
Each row links to the official Federal Reserve statement. Colors: #FFE153=easing,
#C5FAA0=no change, #CCEEFF=tightening, #FFB6B6=inter-meeting action.
Cross-check: dates are validated against the Federal Reserve's own FOMC calendar
in the study script.
"""
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

OUT = Path(__file__).resolve().parent / "fomc_events.json"
URL = (
    "https://en.wikipedia.org/w/api.php?action=parse"
    "&page=History_of_Federal_Open_Market_Committee_actions"
    "&prop=wikitext&format=json&formatversion=2"
)
COLOR_ACTION = {
    "#FFE153": "easing",
    "#C5FAA0": "no_change",
    "#CCEEFF": "tightening",
    "#FFB6B6": "inter_meeting",
}


def main() -> None:
    req = urllib.request.Request(URL, headers={"User-Agent": "CapoHornLab-research/1.0 (citation study)"})
    wt = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())["parse"]["wikitext"]

    idx = wt.find("Historical actions")
    # Parse ONLY the FOMC Federal Funds Rate table (not the Key legend or other tables).
    table_start = wt.find("|+ FOMC Federal Funds Rate History", idx)
    table_end = wt.find("|}", table_start)
    table = wt[table_start:table_end]
    rows = table.split("|-")
    events = []
    for row in rows:
        text = "\n".join(c.strip() for c in row.split("\n") if c.strip())
        if "! Date" in text or "Fed. Funds Rate" in text:
            continue
        # Date cell: "|Date" or styled "|style="..." |Date"; ranges "Month DD–DD, YYYY" -> first day
        m_date = re.search(r"^\|\s*(?:style=\"([^\"]*)\"\s*)?\|?\s*([A-Z][a-z]+) (\d{1,2})(?:–\d{1,2})?, (\d{4})", text)
        if not m_date:
            continue
        try:
            dt = datetime.strptime(f"{m_date.group(2)} {m_date.group(3)}, {m_date.group(4)}", "%B %d, %Y")
        except ValueError:
            continue
        if not (2020 <= dt.year <= 2024):
            continue
        m_rate = re.search(r"background:(#[0-9A-Fa-f]{6})\"\s*\|\s*([\d.]+%?–[\d.]+%?)", text)
        m_votes = re.search(r"\|\s*(\d+–\d+)\s*\|", text)
        if not m_rate:
            continue
        date_cell_color = (m_date.group(1) or "").upper()
        action = COLOR_ACTION.get(date_cell_color) or COLOR_ACTION.get(m_rate.group(1).upper(), "unknown")
        events.append(
            {
                "date": dt.strftime("%Y-%m-%d"),
                "rate_after": m_rate.group(2),
                "action": action,
                "votes": m_votes.group(1) if m_votes else None,
            }
        )

    events.sort(key=lambda e: e["date"])
    # Supplement: the January 28-29, 2020 meeting (held at 1.50-1.75%) is omitted from
    # the Wikipedia table but is a real FOMC meeting. Source: Federal Reserve statement
    # https://www.federalreserve.gov/newsevents/pressreleases/monetary20200129a.htm
    if not any(e["date"] == "2020-01-29" for e in events):
        events.insert(
            0,
            {
                "date": "2020-01-29",
                "rate_after": "1.50%–1.75%",
                "action": "no_change",
                "votes": "10–0",
                "source_note": "Supplemented from Federal Reserve statement monetary20200129a.htm (row absent from Wikipedia table)",
            },
        )
    OUT.write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")
    print(f"FOMC events 2020-2024: {len(events)}")
    for e in events:
        print(f"  {e['date']}  {e['action']:<16} {e['rate_after']}")


if __name__ == "__main__":
    main()
