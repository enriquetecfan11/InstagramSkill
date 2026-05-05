#!/usr/bin/env python3
"""
Render a carousel HTML file into individual PNG slides using local Google Chrome headless.

Designed for fixed-size slides (e.g., 1080x1080 or 1080x1350) where each slide is a
<section class="slide ..."> element.

Best input: an inlined HTML where assets are embedded (data URIs), e.g. carousel.inlined.html.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import tempfile
from pathlib import Path


SLIDE_RE = re.compile(
    r'(<section\s+class="slide\b[^"]*".*?</section>)',
    re.IGNORECASE | re.DOTALL,
)

HEAD_RE = re.compile(r"<head\b[^>]*>(.*?)</head>", re.IGNORECASE | re.DOTALL)


def find_chrome_binary() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for c in candidates:
        if os.path.exists(c) and os.access(c, os.X_OK):
            return c
    raise SystemExit(
        "Google Chrome binary not found. Expected at "
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )


def extract_head(html: str) -> str:
    m = HEAD_RE.search(html)
    if not m:
        return "<head><meta charset='utf-8'></head>"
    head_inner = m.group(1)
    # Ensure charset exists for consistent rendering.
    if "charset" not in head_inner.lower():
        head_inner = "<meta charset='utf-8'>\n" + head_inner
    return f"<head>\n{head_inner}\n</head>"


def extract_slides(html: str) -> list[str]:
    slides = [m.group(1) for m in SLIDE_RE.finditer(html)]
    if not slides:
        raise SystemExit('No slides found. Expected <section class="slide ..."> blocks.')
    return slides


def build_single_slide_html(head: str, slide_html: str) -> str:
    # Force zero margins and lock viewport background.
    return (
        "<!doctype html>\n"
        "<html lang='en'>\n"
        f"{head}\n"
        "<body style='margin:0;background:#000;overflow:hidden;'>\n"
        f"{slide_html}\n"
        "</body>\n"
        "</html>\n"
    )


def render_slide(
    chrome_bin: str,
    html_path: Path,
    out_path: Path,
    width: int,
    height: int,
    budget_ms: int,
    user_data_dir: Path,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--user-data-dir={str(user_data_dir)}",
        f"--window-size={width},{height}",
        f"--virtual-time-budget={budget_ms}",
        f"--screenshot={str(out_path)}",
        str(html_path.as_uri()),
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        stderr = (p.stderr or "").strip()
        raise RuntimeError(
            "Chrome headless failed (this often happens when headless is blocked by OS/App sandbox).\n"
            f"HTML: {html_path}\n"
            f"OUT: {out_path}\n"
            f"Exit: {p.returncode}\n"
            + (f"STDERR:\n{stderr}\n" if stderr else "")
            + "Fallback: open the per-slide HTML in Chrome and use DevTools → Capture node screenshot.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render carousel HTML into per-slide PNGs (Chrome headless)."
    )
    parser.add_argument(
        "html",
        type=Path,
        help="Path to carousel HTML (preferably inlined).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output directory for rendered PNGs.",
    )
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument(
        "--budget-ms",
        type=int,
        default=800,
        help="Virtual time budget for Chrome to finish rendering.",
    )
    args = parser.parse_args()

    html_text = args.html.read_text(encoding="utf-8")
    head = extract_head(html_text)
    slides = extract_slides(html_text)
    chrome_bin = find_chrome_binary()

    with tempfile.TemporaryDirectory(prefix="carousel-render-") as td:
        td_path = Path(td)
        user_data_dir = td_path / "chrome-profile"
        user_data_dir.mkdir(parents=True, exist_ok=True)
        for idx, slide in enumerate(slides, start=1):
            single = build_single_slide_html(head, slide)
            tmp_html = td_path / f"slide-{idx:02d}.html"
            tmp_html.write_text(single, encoding="utf-8")
            out_png = args.out / f"slide-{idx:02d}.png"
            render_slide(
                chrome_bin=chrome_bin,
                html_path=tmp_html,
                out_path=out_png,
                width=args.width,
                height=args.height,
                budget_ms=args.budget_ms,
                user_data_dir=user_data_dir,
            )

    print(str(args.out))


if __name__ == "__main__":
    main()
