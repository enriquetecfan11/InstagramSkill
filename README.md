# InstagramSkill

Repositorio para mantener una skill de Codex que diseña y genera carruseles de Instagram (estilo tech premium) con un avatar consistente.

La fuente canónica editable de la skill vive en `ig-tech-avatar-posts/`.

## Qué incluye

- `ig-tech-avatar-posts/`: skill principal con `SKILL.md`, referencias y scripts internos.
- `examples/`: entradas JSON listas para generar carruseles.
- `assets/avatar-upload/`: pack base de avatares con fondo transparente.
- `tools/scripts/`: utilidades internas (render, export, validación).
- `generar.py`: entrypoint de generación (ver guía de herramientas).

Las carpetas `outputs/`, `analysis/`, `diagnostics/` y `archive/` se tratan como artefactos locales y no se versionan.

## Tooling (opcional)

Si quieres generar/exportar carruseles localmente, consulta `TOOLS.md`.

## Uso como skill

Instalar apuntando al directorio del skill:

`enriquetecfan11/InstagramSkill/ig-tech-avatar-posts`

## Contrato de `brand` y `hud`

La exportación final no debe incluir marcas internas, nombres de la skill, nombres de template, placeholders, textos demo ni marcas de agua no solicitadas.

Todo texto decorativo debe venir del JSON:

```json
{
  "brand": {
    "show": true,
    "text": "Nombre o marca del usuario"
  },
  "hud": {
    "show": true,
    "top_left": "Categoría del post",
    "eyebrow": "Etiqueta temática",
    "show_slide_number": true
  }
}
```

- Si `brand.show` es `false` o `brand.text` está vacío, no se muestra marca inferior.
- Si `hud.show` es `false`, no se muestran textos decorativos superiores.
- La numeración se muestra cuando `hud.show_slide_number` es `true`.

## Contrato de avatar

El avatar debe exportarse limpio, sin aura azul, glow, halo, silueta luminosa ni sombras decorativas pegadas al contorno.

La composición puede usar fondo, grid o iluminación ambiental, pero los efectos no deben contaminar el avatar.

## Contribuir

Consulta `CONTRIBUTING.md`.
