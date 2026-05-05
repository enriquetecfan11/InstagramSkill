#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "carousel"


def read_request(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    avatar = data.get("avatar", {}).get("ruta")
    if not avatar:
        raise SystemExit("El JSON necesita avatar.ruta. El avatar es obligatorio.")
    if "slides" not in data or not data["slides"]:
        data["slides"] = generate_slides(data)
    return data


def generate_slides(data: dict) -> list[dict]:
    topic = data.get("tema", "tu sistema")
    angle = data.get("angulo", "lo que necesitas ordenar")
    cta = data.get("cta", "Guarda este carrusel")
    requested = int(data.get("num_slides") or data.get("slides_count") or 7)
    total = max(5, min(10, requested))

    topic_l = topic.lower()
    if "chatbot" in topic_l and "agente" in topic_l:
        base = [
            {
                "titular": "ChatBot responde",
                "subtitulo": "Un agente ejecuta.",
                "puntos": [],
                "frase": "Responder no es ejecutar.",
            },
            {
                "titular": "ChatBot",
                "subtitulo": "Espera tu mensaje.",
                "puntos": ["Pregunta", "Respuesta"],
                "frase": "Conversacion.",
            },
            {
                "titular": "Agente IA",
                "subtitulo": "Toma una tarea.",
                "puntos": ["Plan", "Accion"],
                "frase": "Ejecucion.",
            },
            {
                "titular": "La diferencia",
                "subtitulo": "No es hablar. Es hacer.",
                "puntos": ["Herramientas", "Memoria"],
                "frase": "Ahi cambia todo.",
            },
            {
                "titular": "Usa agentes",
                "subtitulo": "Cuando haya proceso.",
                "puntos": [],
                "frase": cta,
            },
        ]
        return base[:total]

    base = [
        {
            "titular": "Menos herramientas",
            "subtitulo": f"Mas sistema para {topic}.",
            "puntos": [],
            "frase": "Claridad antes que velocidad.",
        },
        {
            "titular": "El error",
            "subtitulo": "Automatizar caos.",
            "puntos": ["Entrada", "Salida"],
            "frase": "Primero claridad.",
        },
        {
            "titular": "La regla",
            "subtitulo": "Repetible. Medible. Reversible.",
            "puntos": [],
            "frase": "Ese es el filtro.",
        },
        {
            "titular": "Flujo minimo",
            "subtitulo": "Entrada -> criterio -> accion.",
            "puntos": ["Trigger", "Revision"],
            "frase": "Menos piezas.",
        },
        {
            "titular": "Donde entra IA",
            "subtitulo": "Acelera lo definido.",
            "puntos": ["Clasifica", "Propone"],
            "frase": "No sustituye criterio.",
        },
        {
            "titular": "Mide impacto",
            "subtitulo": "Si no mejora, estorba.",
            "puntos": ["Tiempo", "Errores"],
            "frase": "Mide antes/despues.",
        },
        {
            "titular": "Guarda esto",
            "subtitulo": "Antes de automatizar.",
            "puntos": [],
            "frase": cta,
        },
        {
            "titular": "Checklist",
            "subtitulo": "Si falla, no automatices.",
            "puntos": ["Entrada", "Regla"],
            "frase": "Proceso primero.",
        },
        {
            "titular": "Hazlo pequeno",
            "subtitulo": "Un flujo util gana.",
            "puntos": ["Un caso", "Una regla"],
            "frase": "Luego escala.",
        },
        {
            "titular": "Siguiente paso",
            "subtitulo": "Convierte proceso en flujo.",
            "puntos": [],
            "frase": cta,
        },
    ]
    if total <= 7:
        return base[:total]
    return base[: total - 1] + [base[-1]]


def resolve_asset(path_value: str) -> Path:
    path = Path(path_value)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists() and not path.name.startswith("no_bg_"):
        no_bg = path.with_name(f"no_bg_{path.name}")
        if no_bg.exists():
            path = no_bg
    if not path.exists():
        raise SystemExit(f"No existe el archivo de avatar: {path}")
    return path


def natural_key(path: Path) -> list[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


def resolve_avatar_pack(data: dict) -> list[Path]:
    avatar_cfg = data.get("avatar", {})
    src = resolve_asset(avatar_cfg["ruta"])
    use_pack = avatar_cfg.get("usar_pack", True)
    if src.is_dir():
        candidates = [p for p in src.iterdir() if p.suffix.lower() in IMAGE_EXTS]
    elif use_pack and src.parent.name == "avatar-upload":
        candidates = [p for p in src.parent.iterdir() if p.suffix.lower() in IMAGE_EXTS]
    else:
        candidates = [src]
    candidates = sorted(candidates, key=natural_key)
    if not candidates:
        raise SystemExit("No hay avatares disponibles para usar.")
    return candidates


def select_avatars(avatars: list[Path], total: int) -> list[Path]:
    if len(avatars) <= total:
        return avatars[:total]
    # Reparte poses por todo el pack para evitar usar siempre imagenes consecutivas.
    step = max(1, len(avatars) // total)
    selected = []
    used = set()
    for idx in range(total):
        candidate = avatars[(idx * step) % len(avatars)]
        while candidate in used:
            candidate = avatars[(avatars.index(candidate) + 1) % len(avatars)]
        selected.append(candidate)
        used.add(candidate)
    return selected


def copy_avatar(src: Path, out_dir: Path) -> Path:
    asset_dir = out_dir / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    dst = asset_dir / src.name
    if src.resolve() != dst.resolve():
        shutil.copy2(src, dst)
    return dst


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def is_enabled(config: dict, default: bool = False) -> bool:
    value = config.get("show")
    if value is None:
        return default
    return bool(value)


def render_chrome(index: int, total: int, hud: dict) -> str:
    show_hud = is_enabled(hud)
    show_slide_number = bool(hud.get("show_slide_number", show_hud))
    top_left = str(hud.get("top_left") or "").strip()
    parts = []
    if show_hud and top_left:
        parts.append(f'<div class="chrome top-left">{esc(top_left)}</div>')
    if show_slide_number:
        parts.append(f'<div class="chrome top-right">{index:02d}/{total:02d}</div>')
    return "\n      ".join(parts)


def render_eyebrow(hud: dict) -> str:
    if not is_enabled(hud):
        return ""
    eyebrow = str(hud.get("eyebrow") or "").strip()
    if not eyebrow:
        return ""
    return f'<p class="eyebrow">{esc(eyebrow)}</p>'


def render_brand(brand: dict) -> str:
    if not is_enabled(brand):
        return ""
    text = str(brand.get("text") or "").strip()
    if not text:
        return ""
    return f'<div class="brand">{esc(text)}</div>'


def render_points(points: list[str]) -> str:
    if not points:
        return ""
    items = "\n".join(f"<li>{esc(point)}</li>" for point in points[:2])
    return f"<ul>{items}</ul>"


def slide_template(slide: dict, index: int, total: int, avatar_src: str, data: dict) -> str:
    visual = data.get("visual", {})
    hud = data.get("hud", {})
    brand = data.get("brand", {})
    layout = str(slide.get("layout", "")).lower()
    if "avatar / texto" in layout:
        template = "B"
    elif "texto / avatar" in layout:
        template = "A"
    else:
        template = "A" if index % 2 == 1 else "B"
    side_class = "avatar-right" if template == "A" else "avatar-left"
    points = render_points(slide.get("puntos", []))
    chrome = render_chrome(index, total, hud)
    eyebrow = render_eyebrow(hud)
    brand_html = render_brand(brand)

    return f"""
    <section class="slide {side_class}">
      <div class="ambient ambient-{template.lower()}"></div>
      {chrome}
      <div class="copy">
        {eyebrow}
        <h1>{esc(slide.get("titular"))}</h1>
        <p class="subtitle">{esc(slide.get("subtitulo"))}</p>
        {points}
        <p class="closing">{esc(slide.get("frase"))}</p>
      </div>
      <figure class="avatar-box">
        <img src="{esc(avatar_src)}" alt="Avatar protagonista" />
      </figure>
      {brand_html}
    </section>
    """


def build_html(data: dict, avatar_rels: list[str]) -> str:
    visual = data.get("visual", {})
    slides = data["slides"]
    total = len(slides)
    rendered = "\n".join(
        slide_template(slide, idx, total, avatar_rels[(idx - 1) % len(avatar_rels)], data)
        for idx, slide in enumerate(slides, start=1)
    )
    topic = esc(data.get("tema", "Carousel"))
    accent = str(visual.get("acento", "cyan")).lower()
    accent_color = {
        "cyan": "#23d5ff",
        "electric blue": "#3a86ff",
        "violet": "#8b5cf6",
        "magenta": "#ff4fd8",
    }.get(accent, "#23d5ff")

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{topic}</title>
  <style>
    :root {{
      --bg: #080d14;
      --panel: rgba(15, 22, 32, 0.64);
      --text: #e7eef7;
      --muted: #9bb0c6;
      --accent: {accent_color};
      --safe: 64px;
      --text-zone: 55%;
      --avatar-zone: 45%;
      --avatar-box-width: 430px;
      --avatar-box-height: 700px;
      --avatar-side-margin: 80px;
      --avatar-bottom-margin: 50px;
    }}

    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: #05080d;
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    .slide {{
      position: relative;
      width: 1080px;
      height: 1080px;
      overflow: hidden;
      background:
        radial-gradient(circle at 72% 34%, color-mix(in srgb, var(--accent) 34%, transparent), transparent 30%),
        radial-gradient(circle at 18% 78%, rgba(139, 92, 246, 0.20), transparent 26%),
        linear-gradient(135deg, #070b11 0%, #0b121c 48%, #05070b 100%);
      border: 1px solid rgba(255,255,255,0.04);
      isolation: isolate;
    }}

    .slide::before {{
      content: "";
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px);
      background-size: 72px 72px;
      mask-image: radial-gradient(circle at center, black, transparent 78%);
      opacity: 0.34;
      z-index: -2;
    }}

    .ambient {{
      position: absolute;
      inset: var(--safe);
      border: 1px solid color-mix(in srgb, var(--accent) 24%, transparent);
      box-shadow: inset 0 0 40px rgba(255,255,255,0.025);
      opacity: 0.82;
      z-index: -1;
    }}

    .chrome {{
      position: absolute;
      top: var(--safe);
      font-size: 22px;
      line-height: 1;
      color: var(--muted);
      letter-spacing: 0;
      text-transform: uppercase;
    }}
    .top-left {{ left: var(--safe); }}
    .top-right {{ right: var(--safe); font-variant-numeric: tabular-nums; }}
    .brand {{
      position: absolute;
      bottom: var(--safe);
      font-size: 24px;
      color: var(--muted);
    }}
    .avatar-right .brand {{ left: var(--safe); }}
    .avatar-left .brand {{ right: var(--safe); }}

    .copy {{
      position: absolute;
      top: 186px;
      z-index: 3;
    }}
    .avatar-right .copy {{
      left: var(--safe);
      width: calc(var(--text-zone) - (var(--safe) * 2));
    }}
    .avatar-left .copy {{
      left: var(--text-zone);
      width: calc(100% - var(--text-zone) - var(--safe));
    }}

    .eyebrow {{
      margin: 0 0 18px;
      color: var(--accent);
      font-size: 20px;
      font-weight: 700;
      text-transform: uppercase;
    }}
    h1 {{
      margin: 0;
      font-size: 84px;
      line-height: 0.9;
      letter-spacing: 0;
      max-width: 9ch;
    }}
    .subtitle {{
      margin: 26px 0 0;
      color: var(--muted);
      font-size: 34px;
      line-height: 1.08;
      max-width: 13ch;
    }}
    ul {{
      list-style: none;
      margin: 34px 0 0;
      padding: 0;
      display: grid;
      gap: 12px;
      color: #d9e5f2;
      font-size: 30px;
      line-height: 1.05;
    }}
    li::before {{
      content: "";
      display: inline-block;
      width: 10px;
      height: 10px;
      margin-right: 14px;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 18px var(--accent);
      vertical-align: 4px;
    }}
    .closing {{
      margin: 40px 0 0;
      color: var(--text);
      font-size: 30px;
      font-weight: 800;
      line-height: 1.06;
      max-width: 13ch;
    }}

    .avatar-box {{
      position: absolute;
      bottom: var(--avatar-bottom-margin);
      width: var(--avatar-box-width);
      height: var(--avatar-box-height);
      margin: 0;
      display: flex;
      align-items: flex-end;
      justify-content: center;
      z-index: 2;
    }}
    .avatar-right .avatar-box {{
      right: var(--avatar-side-margin);
    }}
    .avatar-left .avatar-box {{
      left: var(--avatar-side-margin);
    }}
    .avatar-box img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      object-position: center bottom;
    }}
  </style>
</head>
<body>
{rendered}
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Crear slides HTML desde un JSON de carrusel.")
    parser.add_argument("json", type=Path, help="Ruta del JSON de entrada.")
    parser.add_argument("--out", type=Path, default=None, help="Carpeta de salida.")
    args = parser.parse_args()

    data = read_request(args.json)
    slug = slugify(data.get("slug") or data.get("tema") or args.json.stem)
    out_dir = args.out or (ROOT / "outputs" / "carousels" / slug)
    out_dir.mkdir(parents=True, exist_ok=True)

    avatars = select_avatars(resolve_avatar_pack(data), len(data["slides"]))
    avatar_rels = []
    for avatar_src in avatars:
        avatar_dst = copy_avatar(avatar_src, out_dir)
        avatar_rels.append(avatar_dst.relative_to(out_dir).as_posix())

    html_text = build_html(data, avatar_rels)
    out_html = out_dir / "carousel.html"
    out_html.write_text(html_text, encoding="utf-8")
    print(out_html)


if __name__ == "__main__":
    main()
