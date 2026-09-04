#!/usr/bin/env python3
"""Render privacy.html and terms.html from ../docs/domain.md.

**The legal text is authored in the container, not here.** This script renders
it; it does not write it. A policy edited on the website and not in the contract
is a policy the app's own disclosures no longer match — which is the exact
discrepancy an App Review rejection is written about.

    ./render-legal.py            write the pages
    ./render-legal.py --check    fail if a page is out of date

Run it from this directory, with the container checked out around it.
"""

from __future__ import annotations

import html
import io
import re
import sys
from pathlib import Path

DOMAIN = Path(__file__).resolve().parent.parent / "docs" / "domain.md"

NAV = """    <nav>
        <a href="index.html">Due This Week</a>
        <a href="privacy.html">Privacy</a>
        <a href="terms.html">Terms</a>
        <a href="support.html">Support</a>
    </nav>
    <footer>Due This Week is made by Patryk Grabowski.</footer>"""

GENERATED = (
    "<!-- GENERATED from ../docs/domain.md by ./render-legal.py. "
    "Edit the contract, then run the script. Changes made here are lost. -->"
)


def section(domain: str, heading: str) -> str:
    start = domain.index(f"### {heading}\n")
    rest = domain[start + len(heading) + 5 :]
    end = rest.index("\n### ") if "\n### " in rest else rest.index("\n**The legal pages")
    return rest[:end]


BOLD = re.compile(r"\*\*(.+?)\*\*")


def to_html(block: str) -> str:
    """Only the blockquote is the policy; the prose around it is instructions."""
    lines = [
        line[2:] if line.startswith("> ") else ("" if line.strip() == ">" else None)
        for line in block.split("\n")
    ]
    text = "\n".join(line for line in lines if line is not None)
    paragraphs = [" ".join(p.split()) for p in text.split("\n\n") if p.strip()]
    rendered = [BOLD.sub(r"<strong>\1</strong>", html.escape(p)) for p in paragraphs]
    return "\n".join("    <p>" + p + "</p>" for p in rendered)


def effective(block: str) -> str:
    match = re.search(r"\*\*Effective ([^*]+)\.\*\*", block)
    return match.group(1) if match else ""


def page(title: str, description: str, heading: str, block: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
{GENERATED}
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="page">
    <header>
        <h1>{heading}</h1>
        <p class="effective">Effective {effective(block)}</p>
    </header>

{to_html(block)}

{NAV}
</div>
</body>
</html>
"""


def main() -> int:
    domain = DOMAIN.read_text(encoding="utf-8")
    pages = {
        "privacy.html": page(
            "Privacy — Due This Week",
            "Due This Week does not collect your data. No account, no server, and documents are read on your phone.",
            "Privacy",
            section(domain, "The privacy policy"),
        ),
        "terms.html": page(
            "Terms — Due This Week",
            "The terms for using Due This Week.",
            "Terms",
            section(domain, "The terms"),
        ),
    }

    stale = []
    for name, contents in pages.items():
        path = Path(name)
        if "--check" in sys.argv:
            if not path.exists() or path.read_text(encoding="utf-8") != contents:
                stale.append(name)
        else:
            path.write_text(contents, encoding="utf-8")
            print(f"wrote {name}")

    for name in stale:
        print(f"error: {name} is out of date — run ./render-legal.py")
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
