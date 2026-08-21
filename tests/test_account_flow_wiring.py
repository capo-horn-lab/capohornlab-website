"""Contract tests for the browser-to-API account and payment readiness flow."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class AccountFlowWiringTests(unittest.TestCase):
    def test_shared_client_uses_real_auth_endpoints(self) -> None:
        client = read("assets/js/account-client.js")
        self.assertIn("https://capohornlab-website.onrender.com/api/v1", client)
        self.assertIn("'/auth/signup'", client)
        self.assertIn("'/auth/login'", client)
        self.assertIn("Authorization", client)
        self.assertNotIn("mock", client.lower())

    def test_signup_submits_to_api_instead_of_redirect_mock(self) -> None:
        page = read("signup.html")
        self.assertIn("account-client.js", page)
        self.assertIn("window.CHLAccount.signup", page)
        self.assertNotIn("Mock signup", page)

    def test_login_persists_a_real_session_before_dashboard_redirect(self) -> None:
        page = read("login.html")
        self.assertIn("account-client.js", page)
        self.assertIn("window.CHLAccount.login", page)
        self.assertIn("dashboard.html", page)
        self.assertNotIn("setTimeout(function() {\n        window.location.href = 'dashboard.html'", page)

    def test_dashboard_requires_and_displays_authenticated_account(self) -> None:
        page = read("dashboard.html")
        self.assertIn("account-client.js", page)
        self.assertIn("window.CHLAccount.requireSession", page)
        self.assertIn("window.CHLAccount.getMe", page)
        self.assertNotIn("user@example.com", page)

    def test_checkout_never_simulates_a_successful_payment(self) -> None:
        page = read("checkout.html")
        self.assertNotIn("function mockPayment", page)
        self.assertNotIn("simulates payment", page)
        self.assertIn("Payment provider is not configured", page)


    def test_static_frontend_defaults_to_live_render_api(self) -> None:
        api = "https://capohornlab-website.onrender.com/api/v1"
        self.assertIn(api, read("assets/js/account-client.js"))
        self.assertIn(api, read("assets/js/newsletter-client.js"))
        self.assertIn(api, read("contact.html"))
        # Legacy /pages route must delegate to, rather than duplicate, the canonical real-API page.
        legacy_contact = read("pages/contact.html")
        self.assertIn("../contact.html", legacy_contact)
        self.assertIn("window.location.replace", legacy_contact)

    def test_account_client_includes_cross_origin_credentials(self) -> None:
        client = read("assets/js/account-client.js")
        self.assertIn("options.credentials = options.credentials || 'include';", client)


if __name__ == "__main__":
    unittest.main()
