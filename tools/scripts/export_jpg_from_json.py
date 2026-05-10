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
AVATAR_BOTTOM_MARGIN = 0
AVATAR_HEIGHT_RATIO = 0.88


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


def visual_palette(name: str) -> dict[str, tuple[int, int, int]]:
    palettes = {
        "cyan": {
            "accent": (35, 213, 255),
            "secondary": (57, 255, 136),
            "danger": (255, 59, 79),
        },
        "electric blue": {
            "accent": (58, 134, 255),
            "secondary": (57, 255, 136),
            "danger": (255, 59, 79),
        },
        "violet": {
            "accent": (139, 92, 246),
            "secondary": (35, 213, 255),
            "danger": (255, 59, 79),
        },
        "magenta": {
            "accent": (255, 79, 216),
            "secondary": (35, 213, 255),
            "danger": (255, 59, 79),
        },
        "hacker-red": {
            "accent": (57, 255, 136),
            "secondary": (35, 213, 255),
            "danger": (255, 52, 72),
        },
    }
    return palettes.get(str(name).lower(), palettes["cyan"])


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


def fit_font_size(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_lines: int,
    start: int,
    minimum: int,
) -> int:
    for size in range(start, minimum - 1, -2):
        fnt = font(size, True)
        lines = wrap_text(draw, text, fnt, max_width)
        if len(lines) <= max_lines and all(text_width(draw, line, fnt) <= max_width for line in lines):
            return size
    return minimum


def make_background(palette: dict[str, tuple[int, int, int]]) -> Image.Image:
    accent = palette["accent"]
    secondary = palette["secondary"]
    danger = palette["danger"]
    img = Image.new("RGB", (1080, 1080), (7, 11, 17))
    pix = img.load()
    for y in range(1080):
        for x in range(1080):
            base = 8 + int(9 * y / 1080)
            glow_r = math.hypot((x - 830) / 520, (y - 360) / 450)
            glow = max(0, 1 - glow_r) ** 2
            cool_r = math.hypot((x - 245) / 620, (y - 890) / 390)
            cool = max(0, 1 - cool_r) ** 2
            threat_r = math.hypot((x - 925) / 420, (y - 890) / 360)
            threat = max(0, 1 - threat_r) ** 2
            r = base + int(accent[0] * glow * 0.08) + int(secondary[0] * cool * 0.06) + int(danger[0] * threat * 0.07)
            g = base + 4 + int(accent[1] * glow * 0.10) + int(secondary[1] * cool * 0.07) + int(danger[1] * threat * 0.03)
            b = base + 10 + int(accent[2] * glow * 0.08) + int(secondary[2] * cool * 0.08) + int(danger[2] * threat * 0.03)
            pix[x, y] = (min(r, 255), min(g, 255), min(b, 255))

    overlay = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for v in range(64, 1080, 72):
        d.line((v, 64, v, 1016), fill=(255, 255, 255, 12), width=1)
        d.line((64, v, 1016, v), fill=(255, 255, 255, 12), width=1)
    for y in range(120, 930, 86):
        d.text((720, y), "LOGS  METRICS  TRACES  SPANS", font=font(18), fill=(255, 255, 255, 34))
    for y in range(166, 910, 144):
        d.line((720, y, 1016, y), fill=(*danger, 32), width=1)
    d.rectangle((64, 64, 1016, 1016), outline=(*accent, 44), width=1)
    d.line((64, 64, 164, 64), fill=(*accent, 92), width=2)
    d.line((916, 1016, 1016, 1016), fill=(*secondary, 92), width=2)
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def trim_alpha(img: Image.Image) -> Image.Image:
    bbox = img.getchannel("A").getbbox()
    if not bbox:
        return img
    return img.crop(bbox)


def paste_avatar(canvas: Image.Image, avatar_path: Path, template: str) -> None:
    avatar = Image.open(avatar_path).convert("RGBA")
    avatar = trim_alpha(avatar)
    if template == "A":
        box_x, box_w = 1080 - int(1080 * 0.56), int(1080 * 0.56)
    else:
        box_x, box_w = 0, int(1080 * 0.54)
    box_h = 1080
    target_h = int(box_h * AVATAR_HEIGHT_RATIO)
    target_w = round(avatar.width * (target_h / avatar.height))
    avatar = avatar.resize((target_w, target_h), Image.Resampling.LANCZOS)

    box_y = 1080 - AVATAR_BOTTOM_MARGIN - box_h
    x = box_x + (box_w - avatar.width) // 2
    y = box_y + box_h - avatar.height
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
    palette = visual_palette(visual.get("acento", "cyan"))
    accent = palette["accent"]
    secondary = palette["secondary"]
    danger = palette["danger"]
    img = make_background(palette)
    paste_avatar(img, avatar_path, template)

    draw = ImageDraw.Draw(img)
    white = (242, 247, 252)
    muted = white
    show_hud = is_enabled(hud)
    show_slide_number = bool(hud.get("show_slide_number", show_hud))
    top_left = str(hud.get("top_left") or "").strip()
    eyebrow = str(hud.get("eyebrow") or "").strip()

    if show_hud and top_left:
        draw.text((48, 48), top_left, font=font(20), fill=muted)
    if show_slide_number:
        counter = f"{index:02d}/{total:02d}"
        draw.text((1032 - text_width(draw, counter, font(20)), 48), counter, font=font(20), fill=muted)

    x = 48 if template == "A" else 1080 - 48 - int(1080 * 0.42)
    y = 185 if template == "A" else 180
    max_w = int(1080 * 0.40) if template == "A" else int(1080 * 0.42)

    if show_hud and eyebrow:
        draw.text((x, y), eyebrow, font=font(20, True), fill=white)
        y += 58
    title_size = fit_font_size(draw, slide.get("titular", ""), max_w, 4, 72, 32)
    y = draw_wrapped(draw, slide.get("titular", ""), (x, y), font(title_size, True), white, max_w, 2)
    y += 38
    indented_x = x + 32
    indented_w = max_w - 32
    y = draw_wrapped(draw, slide.get("subtitulo", ""), (indented_x, y), font(36), white, indented_w, 6)

    points = list(slide.get("puntos", []))[:2]
    if points:
        y += 28
        for point in points:
            draw.ellipse((indented_x, y + 15, indented_x + 10, y + 25), fill=accent)
            draw.text((indented_x + 26, y), str(point), font=font(31, True), fill=white)
            y += 46

    frase = slide.get("frase")
    if frase:
        y += 28
        draw_wrapped(draw, frase, (x, y), font(31, True), white, max_w, 4)

    brand = str(brand_cfg.get("text") or "").strip()
    if is_enabled(brand_cfg) and brand:
        bx = 48 if template == "A" else 1032 - text_width(draw, brand, font(20))
        draw.text((bx, 1018), brand, font=font(20), fill=muted)

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
        draw_slide(slide, avatars[(idx - 1) % len(avatars)], idx, len(data["slides"]), data, out_dir / f"slide-{idx:02d}.jpg")
    print(out_dir)


if __name__ == "__main__":
    main()
