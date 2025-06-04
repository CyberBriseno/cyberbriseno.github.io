#!/usr/bin/env python3
"""Check that relative links in index.html point to existing files."""

from html.parser import HTMLParser
from html import unescape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        for attr, value in attrs:
            if attr in ("href", "src") and value:
                if (value.startswith("http://") or value.startswith("https://") or
                    value.startswith("mailto:") or value.startswith("#") or
                    value.startswith("data:") or value.startswith("//")):
                    continue
                val = unescape(value).split("#", 1)[0].split("?", 1)[0]
                self.links.append(val)

def check_links():
    html = INDEX.read_text(encoding="utf-8")
    parser = LinkCollector()
    parser.feed(html)

    missing = []
    for link in parser.links:
        path = (ROOT / link.lstrip("./").lstrip("/"))
        if not path.exists():
            missing.append(link)

    if missing:
        print("Missing files referenced in index.html:")
        for link in missing:
            print(f" - {link}")
        return 1

    print("All referenced files exist.")
    return 0

if __name__ == "__main__":
    sys.exit(check_links())
