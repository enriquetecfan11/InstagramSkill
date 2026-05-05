#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "ig-tech-avatar-posts"
SKILL_PATH = ROOT / "ig-tech-avatar-posts" / "SKILL.md"
SPEC_PATH = ROOT / "tools" / "scripts" / "create_slides_from_json.py"
EXAMPLES_DIR = ROOT / "examples"

FORBIDDEN_EXPORT_STRINGS = [
    "ig-tech-avatar-posts",
    "Template A",
    "Template B",
    "placeholder",
    "marca de agua",
]


def fail(message: str) -> None:
    raise SystemExit(f"[ERROR] {message}")


def load_spec_module():
    spec = importlib.util.spec_from_file_location("create_slides_from_json", SPEC_PATH)
    if spec is None or spec.loader is None:
        fail(f"No se pudo cargar {SPEC_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_skill_frontmatter(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(?P<body>.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{path} necesita frontmatter YAML delimitado por ---")
    frontmatter = match.group("body")
    for key in ("name:", "description:"):
        if key not in frontmatter:
            fail(f"{path} necesita {key}")
    name_match = re.search(r"^name:\s*(?P<name>[A-Za-z0-9_-]+)\s*$", frontmatter, re.MULTILINE)
    if not name_match:
        fail(f"{path} necesita un name simple en frontmatter")
    if name_match.group("name") != SKILL_DIR.name:
        fail(f"{path} name debe coincidir con el directorio: {SKILL_DIR.name}")
    if len(text.splitlines()) > 500:
        fail(f"{path} supera 500 lineas; mueve detalle a references/")


def validate_skill_layout() -> None:
    if (ROOT / "SKILL.md").exists():
        fail("No debe existir SKILL.md en la raiz; usa ig-tech-avatar-posts/SKILL.md")
    root_agents = ROOT / "agents"
    if root_agents.exists() and any(root_agents.iterdir()):
        fail("No debe existir agents/ en la raiz sin SKILL.md raiz")
    for required in (
        SKILL_DIR / "agents" / "openai.yaml",
        SKILL_DIR / "references",
        SKILL_DIR / "scripts",
    ):
        if not required.exists():
            fail(f"Falta recurso requerido de la skill: {required}")


def validate_json_files() -> list[Path]:
    files = sorted(EXAMPLES_DIR.glob("*.json"))
    if not files:
        fail("No hay ejemplos JSON")
    for path in files:
        try:
            with path.open("r", encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as exc:
            fail(f"JSON invalido en {path}: {exc}")
    return files


def validate_render_contract(example_files: list[Path]) -> None:
    spec = load_spec_module()
    renderable = [p for p in example_files if p.name != "brand-hud-template.json"]
    if not renderable:
        fail("No hay ejemplos renderizables")
    for path in renderable:
        data = spec.read_request(path)
        if not data.get("avatar", {}).get("ruta"):
            fail(f"{path} necesita avatar.ruta")
        avatars = spec.select_avatars(spec.resolve_avatar_pack(data), len(data["slides"]))
        avatar_rels = [f"assets/{avatar.name}" for avatar in avatars]
        html = spec.build_html(data, avatar_rels)
        lowered = html.lower()
        for forbidden in FORBIDDEN_EXPORT_STRINGS:
            if forbidden.lower() in lowered:
                fail(f"{path} exporta texto interno prohibido: {forbidden}")


def main() -> None:
    validate_skill_layout()
    validate_skill_frontmatter(SKILL_PATH)
    example_files = validate_json_files()
    validate_render_contract(example_files)
    print("OK: skill, ejemplos y contrato de render validados.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        raise SystemExit(1)
