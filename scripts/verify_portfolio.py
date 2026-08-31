"""Fail CI when the public portfolio regresses to local-only demos or broken links."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CANONICAL_REPOS = {
    "remote-gig-desk-vercel",
    "ruozhu-deploy-doctor",
    "distributed-job-runner",
    "ai-freelance-workbench",
    "multilingual-support-copilot",
    "marketplace-payment-loop",
}


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        key = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if key and values.get(key):
            self.values.append(values[key] or "")


def main() -> None:
    source = INDEX.read_text(encoding="utf-8")
    lowered = source.lower()
    forbidden = ("open demo · 打开演示", "stores sample activity locally", "six bilingual product demos")
    for phrase in forbidden:
        assert phrase not in lowered, f"browser-only demo claim returned: {phrase}"

    parser = Links()
    parser.feed(source)
    github_repos: set[str] = set()
    for link in parser.values:
        parsed = urlparse(link)
        if parsed.scheme in {"http", "https", "mailto"} or link.startswith("#"):
            if parsed.netloc == "github.com" and parsed.path.startswith("/crz0614/"):
                github_repos.add(parsed.path.strip("/").split("/")[1])
            continue
        target = ROOT / link.split("#", 1)[0].split("?", 1)[0]
        assert target.exists(), f"broken local link: {link}"

    missing = CANONICAL_REPOS - github_repos
    assert not missing, f"missing canonical repository links: {sorted(missing)}"
    print(f"verified {len(parser.values)} links and {len(github_repos)} project repositories")


if __name__ == "__main__":
    main()
