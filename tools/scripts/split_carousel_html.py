#!/usr/bin/env python3
"""
Split a carousel HTML file into per-slide standalone HTML files.

This is useful as a fallback when automated PNG export is blocked:
open each generated HTML in Chrome and use DevTools → Capture node screenshot.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SLIDE_RE = re.compile(
    r'(<section\s+class="slide\b[^"]*".*?</section>)',
    re.IGNORECASE | re.DOTALL,
)

HEAD_RE = re.compile(r"<head\b[^>]*>(.*?)</head>", re.IGNORECASE | re.DOTALL)


def extract_head(html: str) -> str:
    m = HEAD_RE.search(html)
    if not m:
        return "<head><meta charset='utf-8'></head>"
    head_inner = m.group(1)
    if "charset" not in head_inner.lower():
        head_inner = "<meta charset='utf-8'>\n" + head_inner
    return f"<head>\n{head_inner}\n</head>"


def extract_slides(html: str) -> list[str]:
    slides = [m.group(1) for m in SLIDE_RE.finditer(html)]
    if not slides:
        raise SystemExit('No slides found. Expected <section class="slide ..."> blocks.')
    return slides


def build_single_slide_html(head: str, slide_html: str) -> str:
    return (
        "<!doctype html>\n"
        "<html lang='en'>\n"
        f"{head}\n"
        "<body style='margin:0;background:#000;overflow:hidden;'>\n"
        f"{slide_html}\n"
        "</body>\n"
        "</html>\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Split carousel HTML into per-slide HTML files.")
    parser.add_argument("html", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    html_text = args.html.read_text(encoding="utf-8")
    head = extract_head(html_text)
    slides = extract_slides(html_text)

    args.out.mkdir(parents=True, exist_ok=True)
    for idx, slide in enumerate(slides, start=1):
        single = build_single_slide_html(head, slide)
        out_path = args.out / f"slide-{idx:02d}.html"
        out_path.write_text(single, encoding="utf-8")

    print(str(args.out))


if __name__ == "__main__":
    main()

