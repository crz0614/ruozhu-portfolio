"""Verify that every published deployment matches its documented access contract."""

from __future__ import annotations

import argparse
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / ".github" / "deployments.json"
DEFAULT_REPORT = ROOT / "deployment-health.json"


def probe(
    url: str, timeout: float = 20.0, attempts: int = 2
) -> tuple[int | None, str | None, str]:
    request = Request(url, headers={"User-Agent": "ruozhu-portfolio-health/1.0"})
    last_error: str | None = None
    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                body = response.read(512 * 1024).decode(charset, errors="replace")
                return response.status, None, body
        except HTTPError as exc:
            return exc.code, None, ""
        except (URLError, TimeoutError, OSError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt + 1 < attempts:
                time.sleep(1.0)
    return None, last_error, ""


def check(config_path: Path, report_path: Path) -> bool:
    targets = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(targets, list) or not targets:
        raise ValueError("deployment configuration must be a non-empty list")
    results = []
    healthy = True
    for target in targets:
        name, url, expected = target["name"], target["url"], target["expected_status"]
        required_text = target.get("required_text", [])
        if not url.startswith("https://"):
            raise ValueError(f"{name}: deployment URL must use HTTPS")
        if not isinstance(expected, list) or not all(isinstance(value, int) for value in expected):
            raise ValueError(f"{name}: expected_status must be a list of integers")
        if not isinstance(required_text, list) or not all(
            isinstance(value, str) and value for value in required_text
        ):
            raise ValueError(f"{name}: required_text must be a list of non-empty strings")
        status, error, body = probe(url)
        missing_text = [value for value in required_text if value not in body]
        ok = status in expected and not missing_text
        healthy = healthy and ok
        results.append({"name": name, "url": url, "expected_status": expected,
                        "required_text": required_text, "missing_text": missing_text,
                        "observed_status": status, "ok": ok, "error": error})
        detail = f" missing_text={missing_text}" if missing_text else ""
        print(f"{'PASS' if ok else 'FAIL'} {name}: observed={status} expected={expected}{detail}")
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
