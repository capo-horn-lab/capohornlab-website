"""Local end-to-end smoke test for the authenticated strategy-request flow."""
from __future__ import annotations

import json
import mimetypes
import os
import secrets
import urllib.error
import urllib.request
from pathlib import Path

BASE = os.getenv("CHL_E2E_BASE", "http://127.0.0.1:8010/api/v1")
EMAIL = f"e2e-{secrets.token_hex(5)}@example.com"
PASSWORD = "S3cure-Test-Only!9"


def request(path: str, method: str = "GET", body: bytes | None = None, headers: dict | None = None):
    req = urllib.request.Request(BASE + path, data=body, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, dict(response.headers), response.read()
    except urllib.error.HTTPError as exc:
        raise AssertionError(f"{method} {path} -> {exc.code}: {exc.read().decode()}") from exc


def json_request(path: str, method: str, payload: dict, headers: dict | None = None):
    request_headers = {"Content-Type": "application/json"}
    request_headers.update(headers or {})
    status, response_headers, content = request(path, method, json.dumps(payload).encode(), request_headers)
    return status, response_headers, json.loads(content)


def multipart(field: str, filename: str, content: bytes):
    boundary = "----chl" + secrets.token_hex(12)
    mime = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode() + content + f"\r\n--{boundary}--\r\n".encode()
    return body, {"Content-Type": f"multipart/form-data; boundary={boundary}"}


signup = {"name": "Local E2E Client", "email": EMAIL, "password": PASSWORD}
try:
    status, _, registered = json_request("/auth/signup", "POST", signup)
    signup_delivery = "sent"
    assert status == 201, registered
except AssertionError as exc:
    # The local runtime deliberately fail-closes when Resend cannot deliver.
    # The account is persisted before dispatch so the remaining authenticated
    # browser/API path can still be verified independently.
    assert "Account created, but verification email delivery is unavailable" in str(exc), exc
    signup_delivery = "unavailable"

status, _, login = json_request("/auth/login", "POST", {"email": EMAIL, "password": PASSWORD})
assert status == 200 and login["access_token"], login
headers = {"Authorization": "Bearer " + login["access_token"]}

status, _, me = request("/auth/me", headers=headers)
assert status == 200 and json.loads(me)["email"] == EMAIL

payload = {
    "strategy_name": "Local API E2E strategy",
    "description": "Verified browser-contract payload.",
    "instrument": "NQ",
    "timeframe": "5m",
    "historical_period": "2024-01-01 → 2024-12-31",
    "session_times": "09:30-16:00 ET",
    "entry_rules_long": "Breakout rule",
    "entry_rules_short": "Breakdown rule",
    "exit_rules": "Defined stop and target",
    "stop_loss": "20 ticks",
    "take_profit": "40 ticks",
    "trailing_stop": "None",
    "break_even": "At +20 ticks",
    "indicators_params": {"data_mode": "owned"},
    "contracts": 1,
    "commission_slippage": "2.50 / 1 tick",
    "additional_notes": "Created by local e2e smoke test.",
}
status, _, created = json_request("/requests", "POST", payload, headers)
assert status == 201 and created["id"], created

body, multipart_headers = multipart("file", "strategy-notes.txt", b"local e2e attachment\n")
multipart_headers.update(headers)
status, _, uploaded = request(f"/requests/{created['id']}/attachments", "POST", body, multipart_headers)
assert status == 201 and json.loads(uploaded)["original_name"] == "strategy-notes.txt"

status, _, listed = request("/requests", headers=headers)
items = json.loads(listed)["items"]
assert status == 200 and any(item["id"] == created["id"] for item in items), items

status, _, detail = request(f"/requests/{created['id']}", headers=headers)
detail_json = json.loads(detail)
assert status == 200 and len(detail_json["attachments"]) == 1, detail_json

print(json.dumps({"status": "passed", "signup_delivery": signup_delivery, "email": EMAIL, "request_id": created["id"], "attachment_count": len(detail_json["attachments"])}, indent=2))
