#!/usr/bin/env python3
import argparse
import hashlib
import json
from dataclasses import dataclass, asdict


LAYOUTS = [
    "L1 Hero + Title Stack",
    "L2 Split (Avatar / UI)",
    "L3 Side Hero + Big Type",
    "L4 Center Hero + Frame",
]

CAROUSEL_ROLES = [
    "cover_hook",
    "pain",
    "reframe",
    "mechanism",
    "application",
    "example",
    "closing_cta",
]

BACKGROUND_FAMILIES = [
    "dark gradient + subtle particles",
    "volumetric smoke + neon rim",
    "glass blur UI layers + depth",
    "blueprint background + wireframe",
    "abstract terminal/code texture (clean, not cluttered)",
]

ACCENTS = ["cyan", "electric blue", "violet", "magenta"]

MOTIFS = [
    "technical grid overlay (thin lines)",
    "minimal HUD frame (corner marks, scanning line)",
    "automation flow nodes + connectors (clean diagram)",
    "minimal dashboard cards + charts (subtle glass)",
    "abstract code pattern (hinted, not dense)",
]

AVATAR_ROLES = ["authority", "think", "point", "builder", "confirm", "cta", "neutral"]


def pick(items, seed_int, offset=0):
    if not items:
        return None
    return items[(seed_int + offset) % len(items)]


def stable_seed(*parts: str) -> int:
    raw = "|".join([p.strip() for p in parts if p is not None]).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    return int(digest[:8], 16)


@dataclass
class PostSpec:
    topic: str
    angle: str
    goal: str
    language: str
    format: str
    layout: str
    background_family: str
    accent_color: str
    signature_motif: str
    headline: str
    microcopy: str
    prompt_final: str
    negatives: str
    caption: str
    cta: str


def build_prompt_base(background_family: str, accent_color: str, signature_motif: str) -> str:
    identity_block = (
        "premium futuristic tech, minimal, dark theme, high-end product visual; "
        "matte black + subtle glass UI + thin neon accents; "
        "controlled studio lighting, soft rim light, subtle volumetric haze; "
        "ultra clean, crisp edges, high contrast, negative space"
    )
    avatar_block = (
        "Main subject: my personal brand avatar/character; "
        "avatar must be the focal point (or a consistent recurring element), sharp, high detail; "
        "compose using the provided avatar image, do not redesign the character"
    )
    typography_block = (
        "bold sans headline, tight tracking, high legibility on mobile; "
        "microcopy smaller and lighter, aligned to a clean grid; "
        "text integrated into the composition"
    )
    return (
        f"{identity_block}. {avatar_block}. "
        f"Background family: {background_family}. "
        f"Signature motif: {signature_motif}. Accent color: {accent_color}. "
        f"{typography_block}."
    )


def build_negatives() -> str:
    return (
        "no messy clutter, no extra characters, no cheap neon, no cartoonish, "
        "no watermark, no illegible dense text blocks, no oversaturated colors"
    )


def slide_copy(language: str, idx: int, role: str, topic: str, angle: str):
    # Short, generic defaults (user typically overrides later).
    if language == "ES":
        defaults = {
            "cover_hook": ("No es magia. Es sistema.", "Automatiza lo repetible. Decide lo importante."),
            "pain": ("Te está costando horas", "La fricción invisible te roba foco."),
            "reframe": ("Tool ≠ sistema", "La diferencia es el flujo, no la app."),
            "mechanism": ("El flujo en 3 capas", "Entrada → Lógica → Salida."),
            "application": ("Hazlo hoy", "1 regla. 1 trigger. 1 output."),
            "example": ("Ejemplo rápido", "De tarea manual a flujo automático."),
            "closing_cta": ("Guárdalo", "Comenta “SISTEMA” y te paso plantilla."),
        }
    else:
        defaults = {
            "cover_hook": ("Not magic. Just a system.", "Automate the repeatable. Decide what matters."),
            "pain": ("It’s costing you hours", "Invisible friction kills momentum."),
            "reframe": ("Tool ≠ system", "It’s the workflow, not the app."),
            "mechanism": ("The 3-layer flow", "Input → Logic → Output."),
            "application": ("Do it today", "1 rule. 1 trigger. 1 output."),
            "example": ("Quick example", "From manual task to workflow."),
            "closing_cta": ("Save this", "Comment “SYSTEM” and I’ll share a template."),
        }

    headline, micro = defaults.get(role, defaults["application"])
    return headline, micro


def main():
    parser = argparse.ArgumentParser(description="Generate a structured IG tech post spec (JSON).")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--angle", required=True)
    parser.add_argument("--goal", default="authority")
    parser.add_argument("--language", default="ES", choices=["ES", "EN"])
    parser.add_argument("--format", default="carousel", choices=["feed-4x5", "carousel", "cover"])
    parser.add_argument("--slides", type=int, default=7, help="Carousel length (5-10 recommended). Used when format=carousel.")
    args = parser.parse_args()

    seed_int = stable_seed(args.topic, args.angle, args.goal, args.language, args.format)

    layout = pick(LAYOUTS, seed_int, 0)
    background_family = pick(BACKGROUND_FAMILIES, seed_int, 1)
    accent_color = pick(ACCENTS, seed_int, 2)
    signature_motif = pick(MOTIFS, seed_int, 3)

    negatives = build_negatives()
    prompt_base = build_prompt_base(background_family, accent_color, signature_motif)

    if args.language == "ES":
        caption = (
            "La estética atrae, pero el sistema sostiene.\n"
            "Aquí tienes el flujo para pasar de herramienta a sistema."
        )
        cta = "Comenta “SISTEMA” y te paso la plantilla."
    else:
        caption = (
            "Aesthetics stop the scroll. Systems keep the output.\n"
            "Here’s the flow to move from tool to system."
        )
        cta = "Comment “SYSTEM” and I’ll share the template."

    # Carousel mode: output a full slide-by-slide spec (plus a master style).
    if args.format == "carousel":
        slide_count = max(5, min(10, int(args.slides)))
        roles = (CAROUSEL_ROLES * ((slide_count // len(CAROUSEL_ROLES)) + 1))[:slide_count]
        slides = []
        for i, role in enumerate(roles, start=1):
            h, m = slide_copy(args.language, i, role, args.topic, args.angle)
            avatar_role = pick(AVATAR_ROLES, seed_int, i)  # stable per slide
            # Keep layout mostly consistent; allow small controlled variation.
            slide_layout = layout if i in (1, slide_count, 4) else pick(LAYOUTS, seed_int, i) or layout
            delta = (
                f"Slide role: {role}. Layout: {slide_layout}. "
                f"Avatar role/pose tag: {avatar_role}. "
                f"Headline text: {h}. Microcopy text: {m}. "
                "Add one supporting UI element (mini dashboard card OR flow node OR code snippet), keep it minimal."
            )
            slides.append(
                {
                    "index": i,
                    "role": role,
                    "headline": h,
                    "microcopy": m,
                    "layout": slide_layout,
                    "avatar_pose_tag": avatar_role,
                    "prompt": f"{prompt_base} {delta} Negative prompt: {negatives}.",
                    "transition_hint": "Puente corto hacia la siguiente slide.",
                }
            )

        out = {
            "topic": args.topic,
            "angle": args.angle,
            "goal": args.goal,
            "language": args.language,
            "format": args.format,
            "master_style": {
                "background_family": background_family,
                "accent_color": accent_color,
                "signature_motif": signature_motif,
                "base_layout": layout,
                "prompt_base": prompt_base,
                "negatives": negatives,
            },
            "slides": slides,
            "caption": caption,
            "cta": cta,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    # Single-image modes (kept for compatibility)
    headline, microcopy = slide_copy(args.language, 1, "cover_hook", args.topic, args.angle)
    prompt_final = (
        f"{prompt_base} Layout: {layout}. Headline text: {headline}. Microcopy text: {microcopy}. "
        f"Negative prompt: {negatives}."
    )
    spec = PostSpec(
        topic=args.topic,
        angle=args.angle,
        goal=args.goal,
        language=args.language,
        format=args.format,
        layout=layout,
        background_family=background_family,
        accent_color=accent_color,
        signature_motif=signature_motif,
        headline=headline,
        microcopy=microcopy,
        prompt_final=prompt_final,
        negatives=negatives,
        caption=caption,
        cta=cta,
    )
    print(json.dumps(asdict(spec), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
