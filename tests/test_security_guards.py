"""Security regression guards for the web application's production surface."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def source(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class SecurityGuardsTests(unittest.TestCase):
    def test_auth_responses_never_expose_verification_or_reset_codes(self):
        auth = source("app/api/v1/auth.py")
        self.assertNotIn("(dev: {code})", auth)
        self.assertIn("If the address is eligible", auth)

    def test_production_configuration_rejects_placeholder_signing_secrets(self):
        config = source("app/core/config.py")
        self.assertIn("model_validator", config)
        self.assertIn("production settings require non-placeholder", config)

    def test_refresh_tokens_are_not_exposed_to_browser_javascript(self):
        auth = source("app/api/v1/auth.py")
        client = source("assets/js/account-client.js")
        schema = source("app/schemas/auth.py")
        self.assertIn("httponly=True", auth)
        self.assertNotIn("refresh_token=refresh_token", auth)
        self.assertNotIn("REFRESH_KEY", client)
        self.assertNotIn("refresh_token: str", schema)

    def test_data_services_bind_only_to_loopback(self):
        compose = source("docker-compose.yml")
        self.assertIn('"127.0.0.1:5432:5432"', compose)
        self.assertIn('"127.0.0.1:6379:6379"', compose)

    def test_docker_build_excludes_local_credentials_and_heavy_artifacts(self):
        ignore = source(".dockerignore")
        for entry in (".env", ".venv/", ".git/", "reports/"):
            self.assertIn(entry, ignore)


if __name__ == "__main__":
    unittest.main()
