"""Contract checks for non-operational account and billing controls."""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_login_does_not_offer_console_only_social_sign_in() -> None:
    login = read("login.html")
    assert "GitHub SSO — pending backend" not in login
    assert "Google SSO — pending backend" not in login
    assert login.count('class="btn-social"') == 2
    assert login.count('aria-disabled="true"') >= 2


def test_dashboard_disables_unimplemented_payment_actions() -> None:
    dashboard = read("dashboard.html")
    assert "Stripe checkout pending" not in dashboard
    assert "Add Card — Stripe pending" not in dashboard
    assert dashboard.count('disabled aria-disabled="true"') >= 3
