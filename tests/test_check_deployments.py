import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.check_deployments import check


class DeploymentHealthTests(unittest.TestCase):
    def run_check(self, targets, responses):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config, report = root / "deployments.json", root / "report.json"
            config.write_text(json.dumps(targets), encoding="utf-8")
            with patch("scripts.check_deployments.probe", side_effect=responses):
                healthy = check(config, report)
            return healthy, json.loads(report.read_text(encoding="utf-8"))

    def test_accepts_public_and_protected_contracts(self):
        targets = [
            {"name": "public", "url": "https://public.example", "expected_status": [200]},
            {"name": "protected", "url": "https://protected.example", "expected_status": [401]},
        ]
        healthy, report = self.run_check(targets, [
            (200, None, "", {}, "https://public.example"),
            (401, None, "", {}, "https://protected.example"),
        ])
        self.assertTrue(healthy)
        self.assertTrue(report["healthy"])

    def test_fails_on_unexpected_status(self):
        targets = [{"name": "public", "url": "https://public.example", "expected_status": [200]}]
        healthy, report = self.run_check(
            targets, [(503, None, "", {}, "https://public.example")]
        )
        self.assertFalse(healthy)
        self.assertFalse(report["results"][0]["ok"])

    def test_rejects_non_https_target(self):
        targets = [{"name": "bad", "url": "http://example.com", "expected_status": [200]}]
        with self.assertRaises(ValueError):
            self.run_check(targets, [(200, None, "", {}, "http://example.com")])

    def test_fails_when_expected_application_marker_is_missing(self):
        targets = [{
            "name": "public",
            "url": "https://public.example",
            "expected_status": [200],
            "required_text": ["Expected application"],
        }]
        healthy, report = self.run_check(targets, [
            (200, None, "Wrong application", {}, "https://public.example")
        ])
        self.assertFalse(healthy)
        self.assertEqual(report["results"][0]["missing_text"], ["Expected application"])

    def test_accepts_expected_application_marker(self):
        targets = [{
            "name": "public",
            "url": "https://public.example",
            "expected_status": [200],
            "required_text": ["Expected application"],
        }]
        healthy, report = self.run_check(targets, [
            (200, None, "Expected application is live", {}, "https://public.example")
        ])
        self.assertTrue(healthy)
        self.assertEqual(report["results"][0]["missing_text"], [])

    def test_requires_security_header_value(self):
        targets = [{
            "name": "public",
            "url": "https://public.example",
            "expected_status": [200],
            "required_headers": {"Strict-Transport-Security": "max-age="},
        }]
        healthy, report = self.run_check(targets, [
            (200, None, "", {"strict-transport-security": "max-age=31536000"},
             "https://public.example")
        ])
        self.assertTrue(healthy)
        self.assertEqual(report["results"][0]["header_mismatches"], {})

    def test_fails_when_security_header_is_missing(self):
        targets = [{
            "name": "public",
            "url": "https://public.example",
            "expected_status": [200],
            "required_headers": {"Strict-Transport-Security": "max-age="},
        }]
        healthy, report = self.run_check(targets, [
            (200, None, "", {}, "https://public.example")
        ])
        self.assertFalse(healthy)
        self.assertIn("strict-transport-security", report["results"][0]["header_mismatches"])

    def test_fails_on_cross_host_redirect(self):
        targets = [{
            "name": "public",
            "url": "https://public.example",
            "expected_status": [200],
        }]
        healthy, report = self.run_check(targets, [
            (200, None, "", {}, "https://unexpected.example/login")
        ])
        self.assertFalse(healthy)
        self.assertTrue(report["results"][0]["unexpected_final_host"])


if __name__ == "__main__":
    unittest.main()
