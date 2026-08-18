"""Regression guards for real contact/email wiring."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContactFlowWiringTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_contact_frontends_call_real_api(self):
        for path in ("contact.html", "pages/contact.html"):
            page = self.read(path)
            self.assertIn("https://capohornlab-website.onrender.com/api/v1", page)
            self.assertIn("+ '/contact'", page)
            self.assertNotIn("Simulate submission", page)

    def test_email_service_fails_closed_without_provider(self):
        service = self.read("app/services/email.py")
        self.assertIn("return False", service)
        self.assertIn("api.resend.com/emails", service)
        self.assertNotIn("EMAIL STUB", service)

    def test_contact_route_persists_and_notifies(self):
        route = self.read("app/api/v1/contact.py")
        self.assertIn("ContactMessage", route)
        self.assertIn("send_contact_notification", route)
        self.assertIn("check_rate_limit", route)
        self.assertIn("503", route)

    def test_newsletter_forms_use_shared_client(self):
        page = self.read("index.html")
        self.assertIn("CHLNewsletter.subscribe(event)", page)
        self.assertIn("assets/js/newsletter-client.js", page)
        newsletter = self.read("assets/js/newsletter-client.js")
        self.assertIn("https://capohornlab-website.onrender.com/api/v1", newsletter)
        self.assertIn("API_BASE + '/newsletter/subscribe'", newsletter)


if __name__ == "__main__":
    unittest.main()
