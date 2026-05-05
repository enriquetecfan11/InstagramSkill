#!/usr/bin/env python3
"""
One-command carousel exporter.

Flow:
1) Read carousel HTML.
2) Inline local <img src="./..."> assets as data URIs.
3) Split into per-slide standalone HTML files.
4) Try headless Chrome export to PNG.
5) If headless fails, keep split HTML files for manual Chrome capture.

This script is designed to be easy to run and predictable.
"""

from __future__ import annotations

import argparse
import base64
import mimetypes
import os
import re
import subprocess
import tempfile
from pathlib import Path
from shlex import quote
from datetime import datetime
from glob import glob


IMG_SRC_RE = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)(")', re.IGNORECASE)
SLIDE_RE = re.compile(
    r'(<section\s+class="slide\b[^"]*".*?</section>)',
    re.IGNORECASE | re.DOTALL,
)
HEAD_RE = re.compile(r"<head\b[^>]*>(.*?)</head>", re.IGNORECASE | re.DOTALL)


def log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def find_chrome_binary(user_override: str | None) -> str:
    candidates = []
    if user_override:
        candidates.append(user_override)
    candidates.extend(
        [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        ]
    )
    for c in candidates:
        if c and os.path.exists(c) and os.access(c, os.X_OK):
            return c
    raise FileNotFoundError("Chrome binary not found.")


def chrome_app_path_from_binary(chrome_bin: str) -> str:
    # /Applications/Google Chrome.app/Contents/MacOS/Google Chrome -> /Applications/Google Chrome.app
    marker = "/Contents/MacOS/"
    if marker in chrome_bin:
        return chrome_bin.split(marker, 1)[0]
    # Fallback to app name for unusual installs.
    return "Google Chrome"


def open_file_in_chrome(chrome_bin: str, file_path: str) -> bool:
    """
    Prefer launching via Chrome executable directly; fallback to `open -a`.
    """
    # Primary path: direct binary invocation.
    p1 = subprocess.run([chrome_bin, file_path], check=False)
    if p1.returncode == 0:
        return True
    # Fallback: LaunchServices by app name.
    p2 = subprocess.run(["open", "-a", "Google Chrome", file_path], check=False)
    return p2.returncode == 0


def to_data_uri(file_path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(file_path))
    if not mime:
        mime = "application/octet-stream"
    data = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def inline_local_images(html: str, base_dir: Path) -> str:
    inlined_count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal inlined_count
        before, src, after = match.groups()
        # Keep existing external/data URLs untouched.
        if src.startswith(("http://", "https://", "data:")):
            return match.group(0)
        asset = (base_dir / src).resolve()
        if not asset.exists():
            log(f"WARN asset not found, keeping src as-is: {src}")
            return match.group(0)
        inlined_count += 1
        return f'{before}{to_data_uri(asset)}{after}'

    out = IMG_SRC_RE.sub(repl, html)
    log(f"Assets inlined: {inlined_count}")
    return out


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
        raise ValueError('No slides found. Expected <section class="slide ..."> blocks.')
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


def render_png(
    chrome_bin: str,
    html_path: Path,
    out_png: Path,
    width: int,
    height: int,
    budget_ms: int,
    user_data_dir: Path,
    timeout_sec: int,
) -> tuple[bool, str]:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome_bin,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--user-data-dir={str(user_data_dir)}",
        f"--window-size={width},{height}",
        f"--virtual-time-budget={budget_ms}",
        f"--screenshot={str(out_png)}",
        str(html_path.as_uri()),
    ]
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout_sec}s"
    except KeyboardInterrupt:
        # Let caller handle graceful cancellation summary.
        raise
    ok = proc.returncode == 0 and out_png.exists()
    return ok, (proc.stderr or "").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Export carousel HTML to per-slide PNGs.")
    parser.add_argument("html", type=Path, help="Input carousel HTML path.")
    parser.add_argument("--out", type=Path, default=None, help="Output directory (default: sibling folder).")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--budget-ms", type=int, default=1200)
    parser.add_argument(
        "--render-timeout-sec",
        type=int,
        default=20,
        help="Per-slide timeout for headless Chrome render.",
    )
    parser.add_argument("--chrome-path", type=str, default=None)
    parser.add_argument(
        "--open-chrome",
        action="store_true",
        help="Open generated slide HTML files in Chrome when headless export fails.",
    )
    parser.add_argument(
        "--manual-only",
        action="store_true",
        help="Skip headless export and only prepare/open per-slide HTML files.",
    )
    args = parser.parse_args()

    html_path = args.html.resolve()
    if not html_path.exists():
        raise SystemExit(f"Input not found: {html_path}")
    log(f"Input HTML: {html_path}")

    out_root = args.out.resolve() if args.out else (html_path.parent / "export")
    split_dir = out_root / "slides_html"
    png_dir = out_root / "png"
    out_root.mkdir(parents=True, exist_ok=True)
    split_dir.mkdir(parents=True, exist_ok=True)
    png_dir.mkdir(parents=True, exist_ok=True)
    log(f"Output root: {out_root}")
    log(f"Target size: {args.width}x{args.height}")

    log("Reading HTML...")
    html_text = html_path.read_text(encoding="utf-8")
    log("Inlining local images...")
    html_inlined = inline_local_images(html_text, html_path.parent)
    inlined_path = out_root / "carousel.inlined.html"
    inlined_path.write_text(html_inlined, encoding="utf-8")
    log(f"Wrote inlined HTML: {inlined_path}")

    head = extract_head(html_inlined)
    slides = extract_slides(html_inlined)
    log(f"Slides detected: {len(slides)}")

    log("Writing per-slide HTML files...")
    for idx, slide in enumerate(slides, start=1):
        single = build_single_slide_html(head, slide)
        (split_dir / f"slide-{idx:02d}.html").write_text(single, encoding="utf-8")
    log(f"Per-slide HTML dir: {split_dir}")

    try:
        chrome_bin = find_chrome_binary(args.chrome_path)
        chrome_app = chrome_app_path_from_binary(chrome_bin)
        log(f"Chrome binary: {chrome_bin}")
    except FileNotFoundError:
        log("WARN Chrome binary not found. Generated split HTML files only.")
        log(f"OUT_HTML: {split_dir}")
        return

    if args.manual_only:
        log("Manual-only mode: skipping headless export.")
        fallback_cmd = f'open -a "Google Chrome" {quote(str(split_dir))}/slide-*.html'
        log("Fallback command (copy/paste):")
        print(fallback_cmd)
        if args.open_chrome:
            slide_files = sorted(glob(str(split_dir / "slide-*.html")))
            if not slide_files:
                log("WARN no slide HTML files found to open.")
                return
            opened = 0
            for slide_file in slide_files:
                if open_file_in_chrome(chrome_bin, slide_file):
                    opened += 1
            if opened == len(slide_files):
                log(f"Opened {opened} slide files in Chrome.")
            else:
                log(f"WARN opened {opened}/{len(slide_files)} slide files in Chrome.")
        return

    failed = []
    completed = 0
    log("Starting headless PNG export...")
    try:
        with tempfile.TemporaryDirectory(prefix="carousel-export-") as td:
            user_data_dir = Path(td) / "chrome-profile"
            user_data_dir.mkdir(parents=True, exist_ok=True)
            for idx in range(1, len(slides) + 1):
                src = split_dir / f"slide-{idx:02d}.html"
                dst = png_dir / f"slide-{idx:02d}.png"
                log(f"Render slide {idx:02d} -> {dst.name}")
                ok, err = render_png(
                    chrome_bin=chrome_bin,
                    html_path=src,
                    out_png=dst,
                    width=args.width,
                    height=args.height,
                    budget_ms=args.budget_ms,
                    user_data_dir=user_data_dir,
                    timeout_sec=args.render_timeout_sec,
                )
                if not ok:
                    failed.append((idx, err))
                    log(f"WARN render failed: slide {idx:02d}")
                else:
                    completed += 1
                    log(f"OK render done: slide {idx:02d}")
    except KeyboardInterrupt:
        log("CANCELLED by user (Ctrl+C).")
        log(f"Completed PNGs before cancel: {completed}")
        log(f"OUT_PNG (partial): {png_dir}")
        log(f"OUT_HTML: {split_dir}")
        return

    if not failed:
        log(f"DONE exported {len(slides)} PNG files")
        log(f"OUT_PNG: {png_dir}")
        log(f"INLINED_HTML: {inlined_path}")
        return

    log("WARN headless export failed for one or more slides.")
    log(f"OUT_HTML: {split_dir}")
    log(f"INLINED_HTML: {inlined_path}")
    log("Fallback command (copy/paste):")
    fallback_cmd = f'open -a "Google Chrome" {quote(str(split_dir))}/slide-*.html'
    print(fallback_cmd)
    log("Then in each tab: DevTools -> select <section class='slide'> -> Capture node screenshot")
    # Print only first error to keep output readable.
    first_idx, first_err = failed[0]
    if first_err:
        log(f"First error (slide {first_idx:02d}): {first_err}")
    if args.open_chrome:
        slide_files = sorted(glob(str(split_dir / "slide-*.html")))
        if not slide_files:
            log("WARN no slide HTML files found to open.")
            return
        opened = 0
        for slide_file in slide_files:
            if open_file_in_chrome(chrome_bin, slide_file):
                opened += 1
        if opened == len(slide_files):
            log(f"Opened {opened} slide files in Chrome.")
        else:
            log(f"WARN opened {opened}/{len(slide_files)} slide files in Chrome.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Final guard: avoid traceback on Ctrl+C.
        print("\nInterrupted by user.")
