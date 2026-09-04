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

    def test_transport_error_is_unverified_not_missing_headers(self):
        targets = [{"name": "protected", "url": "https://protected.example",
                    "expected_status": [401], "required_text": ["Restricted"],
                    "required_headers": {"www-authenticate": "Basic"}}]
        for error in ["URLError: Tunnel connection failed: 403 Forbidden",
                      "TimeoutError: timed out", "URLError: certificate verify failed"]:
            with self.subTest(error=error):
                healthy, report = self.run_check(targets, [
                    (None, error, "", {}, "https://protected.example")])
                result = report["results"][0]
                self.assertFalse(healthy)
                self.assertFalse(result["ok"])
                self.assertFalse(result["response_received"])
                self.assertEqual(result["verification_state"], "unverified")
                self.assertEqual(result["header_mismatches"], {})
                self.assertEqual(result["missing_text"], [])
                self.assertEqual(result["error"], error)

    def test_received_403_is_contract_failure_not_transport_block(self):
        targets = [{"name": "public", "url": "https://public.example",
                    "expected_status": [200], "required_headers": {"x-frame-options": "DENY"}}]
        healthy, report = self.run_check(targets, [(403, None, "", {}, "https://public.example")])
        result = report["results"][0]
        self.assertFalse(healthy)
        self.assertTrue(result["response_received"])
        self.assertEqual(result["verification_state"], "failed")
        self.assertIn("x-frame-options", result["header_mismatches"])

    def test_invalid_expected_status_cannot_accept_transport_failure(self):
        for expected in [[], [None], [True], [99], [600], ["200"]]:
            with self.subTest(expected=expected), self.assertRaises(ValueError):
                self.run_check([{"name": "bad", "url": "https://example.com",
                                 "expected_status": expected}], [])

    def test_commerce_console_exposes_bilingual_filtered_csv_export(self):
        root = Path(__file__).parents[1]
        console = (root / "commerce-ops" / "index.html").read_text(encoding="utf-8")
        homepage = (root / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="exportOrders"', console)
        self.assertIn("export:'导出 CSV'", console)
        self.assertIn("export:'Export CSV'", console)
        self.assertIn("p.set('format','csv')", console)
        self.assertIn("authorization:'Bearer '+token", console)
        self.assertIn('id="orderCanonical"', console)
        self.assertIn("allCanonical:'全部标准状态'", console)
        self.assertIn("allCanonical:'All canonical statuses'", console)
        self.assertIn("p.set('canonical_status',canonical)", console)
        self.assertIn("canonicalLabels[lang][x.canonical_status]", console)
        self.assertIn('/api/commerce/summary', console)
        self.assertIn('id="refreshSummary"', console)
        self.assertIn("summary:'运营概览'", console)
        self.assertIn("summary:'Operations summary'", console)
        self.assertIn('不受 200 条账本上限影响', console)
        self.assertIn('beyond the 200-row ledger limit', console)
        self.assertIn('Number(x.amount_minor)/100', console)
        self.assertIn('id="inventoryForm"', console)
        self.assertIn('id="lowStockOnly"', console)
        self.assertIn("inventoryTitle:'库存与低库存预警'", console)
        self.assertIn("inventoryTitle:'Inventory and low-stock alerts'", console)
        self.assertIn("/api/commerce/inventory", console)
        self.assertIn("p.set('low_stock','true')", console)
        self.assertIn('id="refreshInventorySummary"', console)
        self.assertIn("inventorySummary:'跨店铺 SKU 汇总'", console)
        self.assertIn("inventorySummary:'Cross-shop SKU summary'", console)
        self.assertIn('/api/commerce/inventory-summary', console)
        self.assertIn('x.low_stock_shop_count', console)
        self.assertIn('id="exportLowStock"', console)
        self.assertIn("exportLowStock:'导出低库存 CSV'", console)
        self.assertIn("exportLowStock:'Export low-stock CSV'", console)
        self.assertIn("a.download='vesper-commerce-low-stock.csv'", console)
        self.assertIn('id="refreshInventoryExceptions"', console)
        self.assertIn("inventoryExceptions:'订单—库存对账异常'", console)
        self.assertIn("inventoryExceptions:'Order–inventory reconciliation exceptions'", console)
        self.assertIn('/api/commerce/inventory-exceptions', console)
        self.assertIn('x.order_line_count', console)
        self.assertIn('x.ordered_quantity', console)
        self.assertIn("marketplace-payment-loop/pull/33", homepage)


if __name__ == "__main__":
    unittest.main()
