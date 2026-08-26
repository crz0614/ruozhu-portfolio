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
        healthy, report = self.run_check(targets, [(200, None), (401, None)])
        self.assertTrue(healthy)
        self.assertTrue(report["healthy"])

    def test_fails_on_unexpected_status(self):
        targets = [{"name": "public", "url": "https://public.example", "expected_status": [200]}]
        healthy, report = self.run_check(targets, [(503, None)])
        self.assertFalse(healthy)
        self.assertFalse(report["results"][0]["ok"])

    def test_rejects_non_https_target(self):
        targets = [{"name": "bad", "url": "http://example.com", "expected_status": [200]}]
        with self.assertRaises(ValueError):
            self.run_check(targets, [(200, None)])


if __name__ == "__main__":
    unittest.main()
