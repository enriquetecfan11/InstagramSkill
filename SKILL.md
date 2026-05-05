---
name: ig-tech-avatar-posts
description: Diseñar carruseles completos de Instagram (5–10 slides) con identidad visual totalmente consistente (paleta, tipografía, composición, iluminación, fondos tech premium) y storytelling editorial optimizado para retención, branding y viralidad, usando un avatar/“muñeco” como ancla de marca en toda la secuencia. Usar cuando el usuario pida carruseles cohesionados (no posts sueltos), guiones slide-a-slide, dirección de arte unificada, copy corto integrado en la composición, y prompts listos para generar/editar todas las slides como una campaña reconocible.
---

# Ig Tech Avatar Posts

Este archivo es el entrypoint instalable del repositorio.

La fuente canónica de la skill vive en:

`skill/ig-tech-avatar-posts/SKILL.md`

Cuando esta skill se active, sigue ese archivo canónico y usa sus recursos:

- `skill/ig-tech-avatar-posts/references/`
- `skill/ig-tech-avatar-posts/scripts/`
- `skill/ig-tech-avatar-posts/agents/openai.yaml`

## Reglas críticas

- Nunca exportar textos internos, placeholders, nombres de template, nombres de la skill ni marcas de agua no solicitadas.
- La marca inferior solo puede salir de `brand.text` cuando `brand.show` sea `true`.
- Los textos decorativos superiores solo pueden salir de `hud.top_left` y `hud.eyebrow`.
- La numeracion de slide solo depende de `hud.show_slide_number`.
- El avatar debe renderizarse limpio, sin aura azul, glow, halo, silueta luminosa ni `drop-shadow` decorativo.
- Si se trabaja dentro de este repositorio, ejecutar `python3 tools/scripts/validate_repo.py` antes de considerar lista una entrega versionable.

## Uso local del repositorio

Para generar un carrusel desde JSON:

`python3 generar.py examples/chatbots-vs-agentes.json`

Para validar el repositorio:

`python3 tools/scripts/validate_repo.py`
