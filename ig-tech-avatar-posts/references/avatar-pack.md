# Avatar Pack (poses como sistema)

Objetivo: usar un pack de poses como “biblioteca” para asignar un rol por slide y mantener consistencia.

## Carpeta recomendada

- Guardar poses en `assets/avatars/` (PNG/JPG).
- Mantener nombres estables; si se renombra, usar un índice.

## Etiquetas (rápidas)

Asignar 1–2 tags por pose:
- `authority` (brazos cruzados, seguro)
- `think` (mano en barbilla, mirada arriba)
- `point` (señala al texto/UI)
- `confirm` (thumbs up, ok)
- `cta` (gesto enérgico, “let’s go”)
- `builder` (laptop, escribir, móvil)
- `neutral` (sonrisa simple, mirada al frente)

## Asignación por slide (regla simple)

- Si hay pack disponible, usar una pose distinta por slide siempre que el número de poses sea suficiente.
- No repetir el mismo avatar en todo un carrusel de varias slides salvo que el usuario lo pida explicitamente.
- Slide 1 (Hook): `authority` o `point`
- Slides 2–3 (Problema/Reframe): `think` o `neutral`
- Slides 4–6 (Mecanismo/Pasos): `point` o `builder`
- Slide final (CTA): `cta` o `confirm`

## Consistencia visual del avatar

- Evitar re-ilustrar al avatar: preferir composición/edición.
- Mantener tamaño relativo consistente (hero vs recurrente).
- Si el carrusel es dark premium, aplicar glow/rim light constante (fino).
