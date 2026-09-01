"""Verify that every published deployment matches its documented access contract."""

from __future__ import annotations

import argparse
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / ".github" / "deployments.json"
DEFAULT_REPORT = ROOT / "deployment-health.json"


def probe(
    url: str, timeout: float = 20.0, attempts: int = 2
) -> tuple[int | None, str | None, str, dict[str, str], str]:
    request = Request(url, headers={"User-Agent": "ruozhu-portfolio-health/1.0"})
    last_error: str | None = None
    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                body = response.read(512 * 1024).decode(charset, errors="replace")
                headers = {key.lower(): value for key, value in response.headers.items()}
                return response.status, None, body, headers, response.geturl()
        except HTTPError as exc:
            with exc:
                headers = {key.lower(): value for key, value in exc.headers.items()}
                return exc.code, None, "", headers, exc.geturl()
        except (URLError, TimeoutError, OSError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt + 1 < attempts:
                time.sleep(1.0)
    return None, last_error, "", {}, url


def check(config_path: Path, report_path: Path) -> bool:
    targets = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(targets, list) or not targets:
        raise ValueError("deployment configuration must be a non-empty list")
    results = []
    healthy = True
    for target in targets:
        name, url, expected = target["name"], target["url"], target["expected_status"]
        required_text = target.get("required_text", [])
        required_headers = target.get("required_headers", {})
        if not url.startswith("https://"):
            raise ValueError(f"{name}: deployment URL must use HTTPS")
        if not isinstance(expected, list) or not expected or not all(
            type(value) is int and 100 <= value <= 599 for value in expected
        ):
            raise ValueError(f"{name}: expected_status must be a non-empty list of HTTP status codes")
        if not isinstance(required_text, list) or not all(
            isinstance(value, str) and value for value in required_text
        ):
            raise ValueError(f"{name}: required_text must be a list of non-empty strings")
        if not isinstance(required_headers, dict) or not all(
            isinstance(key, str) and key
            and isinstance(value, str) and value
            for key, value in required_headers.items()
        ):
            raise ValueError(f"{name}: required_headers must map names to required substrings")
        status, error, body, headers, final_url = probe(url)
        response_received = status is not None
        missing_text = [value for value in required_text if value not in body] if response_received else []
        header_mismatches = {
            key.lower(): {"required": value, "observed": headers.get(key.lower())}
            for key, value in required_headers.items()
            if value.lower() not in headers.get(key.lower(), "").lower()
        } if response_received else {}
        expected_host = urlparse(url).hostname
        final_host = urlparse(final_url).hostname
        unexpected_final_host = final_host != expected_host
        ok = (
            response_received
            and error is None
            and status in expected
            and not missing_text
            and not header_mismatches
            and not unexpected_final_host
        )
        healthy = healthy and ok
        # A transport error says nothing about the application's response headers.
        # Keep CI fail-closed, but do not describe unobserved headers as absent.
        verification_state = "passed" if ok else ("failed" if response_received else "unverified")
        results.append({"name": name, "url": url, "expected_status": expected,
                        "required_text": required_text, "missing_text": missing_text,
                        "required_headers": required_headers,
                        "header_mismatches": header_mismatches,
                        "observed_status": status, "final_url": final_url,
                        "unexpected_final_host": unexpected_final_host,
                        "ok": ok, "error": error,
                        "response_received": response_received,
                        "verification_state": verification_state})
        detail = f" missing_text={missing_text}" if missing_text else ""
        detail += f" header_mismatches={header_mismatches}" if header_mismatches else ""
        detail += f" final_url={final_url}" if unexpected_final_host else ""
        detail += f" transport_error={error}" if not response_received else ""
        label = {"passed": "PASS", "failed": "FAIL", "unverified": "UNVERIFIED"}[verification_state]
        print(f"{label} {name}: observed={status} expected={expected}{detail}")
    report = {"checked_at": datetime.now(UTC).isoformat(), "healthy": healthy, "results": results}
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return healthy


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    raise SystemExit(0 if check(args.config, args.report) else 1)


if __name__ == "__main__":
    main()
