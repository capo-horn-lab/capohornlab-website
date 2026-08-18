"""Safe, dependency-free parsing and local storage for approved web-page results."""
from __future__ import annotations

import json
import sqlite3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class _VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=""; self.description=""; self.heading=""; self._ignore=0; self._tag=""; self.parts=[]
    def handle_starttag(self, tag, attrs):
        self._tag=tag
        if tag in {"script","style","noscript","template"}: self._ignore+=1
        if tag=="meta":
            values=dict(attrs)
            if values.get("name", "").lower()=="description": self.description=values.get("content", "")
    def handle_endtag(self, tag):
        if tag in {"script","style","noscript","template"} and self._ignore: self._ignore-=1
        self._tag=""
    def handle_data(self, data):
        value=" ".join(data.split())
        if not value or self._ignore: return
        if self._tag=="title": self.title=value
        elif self._tag=="h1" and not self.heading: self.heading=value
        else: self.parts.append(value)


def extract_content(url: str, html: str) -> dict[str, str]:
    parser=_VisibleText(); parser.feed(html)
    return {"url":url,"title":parser.title,"description":parser.description,"heading":parser.heading,"text":" ".join(parser.parts)}


def validate_record(record: dict[str, str], max_text_length: int = 1_000_000) -> dict[str, str]:
    parsed=urlparse(record.get("url", ""))
    if parsed.scheme not in {"http","https"} or not parsed.netloc: raise ValueError("record requires an http(s) URL")
    if not record.get("text", "").strip(): raise ValueError("record requires readable text")
    if len(record["text"]) > max_text_length: raise ValueError("record text exceeds size limit")
    return record


class ResultStore:
    def __init__(self, json_path: Path, sqlite_path: Path): self.json_path=Path(json_path); self.sqlite_path=Path(sqlite_path)
    def save(self, records: list[dict[str, str]]) -> None:
        checked=[validate_record(item) for item in records]
        self.json_path.parent.mkdir(parents=True,exist_ok=True); self.sqlite_path.parent.mkdir(parents=True,exist_ok=True)
        self.json_path.write_text(json.dumps(checked,ensure_ascii=False),encoding="utf-8")
        con = sqlite3.connect(self.sqlite_path)
        try:
            con.execute("CREATE TABLE IF NOT EXISTS scraped_pages (url TEXT, title TEXT, description TEXT, heading TEXT, text TEXT)")
            con.execute("DELETE FROM scraped_pages")
            con.executemany("INSERT INTO scraped_pages (url,title,description,heading,text) VALUES (:url,:title,:description,:heading,:text)", checked)
            con.commit()
        finally:
            # Close explicitly: SQLite context managers commit/rollback but keep a Windows file handle open.
            con.close()
