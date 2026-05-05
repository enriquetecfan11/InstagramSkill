#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "tools" / "scripts" / "create_slides_from_json.py"
FONT_REGULAR_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_BOLD_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
TEXT_ZONE_W = 594
AVATAR_BOX_W = 430
AVATAR_BOX_H = 700
AVATAR_SIDE_MARGIN = 80
AVATAR_BOTTOM_MARGIN = 50


def load_spec_module():
    spec = importlib.util.spec_from_file_location("create_slides_from_json", SPEC_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit("No se pudo cargar create_slides_from_json.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def resolve_font(candidates: list[str]) -> str:
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    raise SystemExit("No se encontro una fuente TrueType compatible para exportar JPG.")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = FONT_BOLD_CANDIDATES if bold else FONT_REGULAR_CANDIDATES
    return ImageFont.truetype(resolve_font(candidates), size)


def accent_color(name: str) -> tuple[int, int, int]:
    colors = {
        "cyan": (35, 213, 255),
        "electric blue": (58, 134, 255),
        "violet": (139, 92, 246),
        "magenta": (255, 79, 216),
    }
    return colors.get(str(name).lower(), colors["cyan"])


def is_enabled(config: dict, default: bool = False) -> bool:
    value = config.get("show")
    if value is None:
        return default
    return bool(value)


def text_width(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = str(text or "").split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = word if not current else f"{current} {word}"
        if text_width(draw, test, fnt) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    max_width: int,
    line_gap: int,
) -> int:
    x, y = xy
    for line in wrap_text(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        box = draw.textbbox((x, y), line, font=fnt)
        y += (box[3] - box[1]) + line_gap
    return y


def make_background(accent: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (1080, 1080), (7, 11, 17))
    pix = img.load()
    for y in range(1080):
        for x in range(1080):
            base = 8 + int(9 * y / 1080)
            glow_r = math.hypot((x - 830) / 520, (y - 360) / 450)
            glow = max(0, 1 - glow_r) ** 2
            violet_r = math.hypot((x - 250) / 620, (y - 930) / 380)
            violet = max(0, 1 - violet_r) ** 2
            r = base + int(accent[0] * glow * 0.12) + int(60 * violet * 0.16)
            g = base + 4 + int(accent[1] * glow * 0.14) + int(40 * violet * 0.08)
            b = base + 10 + int(accent[2] * glow * 0.16) + int(120 * violet * 0.16)
            pix[x, y] = (min(r, 255), min(g, 255), min(b, 255))

    overlay = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for v in range(64, 1080, 72):
        d.line((v, 64, v, 1016), fill=(255, 255, 255, 12), width=1)
        d.line((64, v, 1016, v), fill=(255, 255, 255, 12), width=1)
    d.rectangle((64, 64, 1016, 1016), outline=(*accent, 52), width=1)
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def trim_alpha(img: Image.Image) -> Image.Image:
    bbox = img.getchannel("A").getbbox()
    if not bbox:
        return img
    return img.crop(bbox)


def paste_avatar(canvas: Image.Image, avatar_path: Path, template: str) -> None:
    avatar = Image.open(avatar_path).convert("RGBA")
    avatar = trim_alpha(avatar)
    avatar.thumbnail((AVATAR_BOX_W, AVATAR_BOX_H), Image.Resampling.LANCZOS)

    box_x = 1080 - AVATAR_SIDE_MARGIN - AVATAR_BOX_W if template == "A" else AVATAR_SIDE_MARGIN
    box_y = 1080 - AVATAR_BOTTOM_MARGIN - AVATAR_BOX_H
    x = box_x + (AVATAR_BOX_W - avatar.width) // 2
    y = box_y + AVATAR_BOX_H - avatar.height
    canvas.alpha_composite(avatar, (x, y))


def draw_slide(slide: dict, avatar_path: Path, index: int, total: int, data: dict, out_path: Path) -> None:
    visual = data.get("visual", {})
    hud = data.get("hud", {})
    brand_cfg = data.get("brand", {})
    layout = str(slide.get("layout", "")).lower()
    if "avatar / texto" in layout:
        template = "B"
    elif "texto / avatar" in layout:
        template = "A"
    else:
        template = "A" if index % 2 == 1 else "B"
    accent = accent_color(visual.get("acento", "cyan"))
    img = make_background(accent)
    paste_avatar(img, avatar_path, template)

    draw = ImageDraw.Draw(img)
    muted = (155, 176, 198)
    white = (231, 238, 247)
    show_hud = is_enabled(hud)
    show_slide_number = bool(hud.get("show_slide_number", show_hud))
    top_left = str(hud.get("top_left") or "").strip()
    eyebrow = str(hud.get("eyebrow") or "").strip()

    if show_hud and top_left:
        draw.text((64, 66), top_left, font=font(24), fill=muted)
    if show_slide_number:
        counter = f"{index:02d}/{total:02d}"
        draw.text((1016 - text_width(draw, counter, font(24)), 66), counter, font=font(24), fill=muted)

    x = 64 if template == "A" else TEXT_ZONE_W
    y = 190
    max_w = 466 if template == "A" else 422

    if show_hud and eyebrow:
        draw.text((x, y), eyebrow, font=font(22, True), fill=accent)
        y += 58
    y = draw_wrapped(draw, slide.get("titular", ""), (x, y), font(84, True), white, max_w, 2)
    y += 26
    y = draw_wrapped(draw, slide.get("subtitulo", ""), (x, y), font(36), muted, max_w, 6)

    points = list(slide.get("puntos", []))[:2]
    if points:
        y += 28
        for point in points:
            draw.ellipse((x, y + 15, x + 10, y + 25), fill=accent)
            draw.text((x + 26, y), str(point), font=font(31, True), fill=white)
            y += 46

    frase = slide.get("frase")
    if frase:
        y += 28
        draw_wrapped(draw, frase, (x, y), font(31, True), white, max_w, 4)

    brand = str(brand_cfg.get("text") or "").strip()
    if is_enabled(brand_cfg) and brand:
        bx = 64 if template == "A" else 1016 - text_width(draw, brand, font(24))
        draw.text((bx, 986), brand, font=font(24), fill=muted)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out_path, "JPEG", quality=95, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Exporta JPG 1080x1080 directamente desde un JSON.")
    parser.add_argument("json", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    spec = load_spec_module()
    data = spec.read_request(args.json)
    slug = spec.slugify(data.get("slug") or data.get("tema") or args.json.stem)
    out_dir = args.out or (ROOT / "outputs" / "carousels" / slug / "jpg")
    avatars = spec.select_avatars(spec.resolve_avatar_pack(data), len(data["slides"]))
    for idx, slide in enumerate(data["slides"], start=1):
        draw_slide(slide, avatars[idx - 1], idx, len(data["slides"]), data, out_dir / f"slide-{idx:02d}.jpg")
    print(out_dir)


if __name__ == "__main__":
    main()
