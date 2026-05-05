#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def python_for_images() -> str:
    configured = os.environ.get("INSTAGRAMSKILL_PYTHON")
    if configured:
        path = Path(configured).expanduser()
        if not path.exists():
            raise SystemExit(f"INSTAGRAMSKILL_PYTHON no existe: {path}")
        return str(path)
    codex_runtime = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "python"
        / "bin"
        / "python3"
    )
    if codex_runtime.exists():
        return str(codex_runtime)
    return sys.executable


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise SystemExit(message)
    return result.stdout.strip()


def read_slug(json_path: Path) -> str:
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    slug = data.get("slug")
    if not slug:
        raise SystemExit("El JSON necesita un campo 'slug'.")
    return str(slug)


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera un carrusel desde un JSON.")
    parser.add_argument(
        "json",
        nargs="?",
        default="examples/chatbots-vs-agentes.json",
        help="Ruta del JSON. Si no pones nada, usa examples/chatbots-vs-agentes.json.",
    )
    args = parser.parse_args()

    json_path = (ROOT / args.json).resolve() if not Path(args.json).is_absolute() else Path(args.json)
    if not json_path.exists():
        raise SystemExit(f"No existe el JSON: {json_path}")

    slug = read_slug(json_path)
    carousel_html = run([
        sys.executable,
        "tools/scripts/create_slides_from_json.py",
        str(json_path),
    ])

    out_dir = ROOT / "outputs" / "carousels" / slug / "slides_html"
    run([
        sys.executable,
        "tools/scripts/split_carousel_html.py",
        carousel_html,
        "--out",
        str(out_dir),
    ])

    jpg_dir = run([
        python_for_images(),
        "tools/scripts/export_jpg_from_json.py",
        str(json_path),
    ])

    print("Carrusel generado:")
    print(carousel_html)
    print("")
    print("Slides individuales:")
    print(out_dir)
    print("")
    print("JPG:")
    print(jpg_dir)


if __name__ == "__main__":
    main()
