"""Fetch official BLS release dates (CPI + Employment Situation) 2020-2024.

Source: Wayback Machine snapshots of the official BLS news-release calendar ICS
(https://www.bls.gov/schedule/news_release/bls.ics). BLS blocks live bot access
to www pages; the public API (api.bls.gov) is used separately for values.
"""
import json
import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "bls_release_dates.json"
CDX = "http://web.archive.org/cdx/search/cdx?url=bls.gov/schedule/news_release/bls.ics&from={}&to={}&output=json&limit=50&filter=statuscode:200"


def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "CapoHornLab-research/1.0 (research study; single pass)"})
    return urllib.request.urlopen(req, timeout=timeout).read()


def snapshot_for_year(year: int) -> str | None:
    """Find an ICS snapshot covering the release calendar of `year`."""
    # Schedule for year Y is published ~Dec Y-1; search Dec 1 Y-1 .. Mar 1 Y.
    from_ts = f"{year-1}1201"
    to_ts = f"{year}0401"
    try:
        raw = fetch(CDX.format(from_ts, to_ts))
        rows = json.loads(raw)
    except Exception as exc:  # noqa: BLE001
        print(f"  cdx error {year}: {exc}")
        return None
    if len(rows) < 2:
        return None
    # rows[0] is the header; pick the EARLIEST snapshot in the window
    snap = rows[1][1]
    return snap


def parse_ics(data: bytes) -> list[dict]:
    text = data.decode("utf-8", errors="replace")
    events = []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.S):
        dtstart = re.search(r"DTSTART[^:\r\n]*:(\d{8})", block)
        summary = re.search(r"SUMMARY[^:\r\n]*:(.*?)[\r\n]", block)
        if not dtstart or not summary:
            continue
        date = dtstart.group(1)
        name = summary.group(1).strip()
        if any(k in name for k in ("Consumer Price Index", "Employment Situation")):
            events.append({"date": date, "release": name})
    return events


def main() -> None:
    all_events: dict[str, list[dict]] = {str(y): [] for y in range(2020, 2025)}
    # All snapshots of the ICS between late 2019 and early 2025.
    try:
        raw = fetch(CDX.format("20191101", "20250301"))
        rows = json.loads(raw)[1:]
    except Exception as exc:  # noqa: BLE001
        print("cdx error:", exc)
        return
    seen_digests = set()
    fetched = 0
    for row in rows:
        ts, digest = row[1], row[5]
        if digest in seen_digests:
            continue
        seen_digests.add(digest)
        url = f"https://web.archive.org/web/{ts}id_/https://www.bls.gov/schedule/news_release/bls.ics"
        try:
            data = fetch(url)
            events = parse_ics(data)
            for ev in events:
                y = ev["date"][:4]
                if y in all_events:
                    all_events[y].append(ev)
            fetched += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  snapshot {ts}: error {exc}")
    # Dedupe per year by date+release
    for y in all_events:
        seen = set()
        uniq = []
        for ev in sorted(all_events[y], key=lambda e: e["date"]):
            key = (ev["date"], ev["release"])
            if key not in seen:
                seen.add(key)
                uniq.append(ev)
        all_events[y] = uniq
        print(f"{y}: {len(all_events[y])} events (from {fetched} snapshots)")

    OUT.write_text(json.dumps(all_events, indent=2) + "\n", encoding="utf-8")
    print("saved:", OUT)


if __name__ == "__main__":
    main()
