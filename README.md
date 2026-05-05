# InstagramSkill

Repositorio para mantener una skill de Codex que diseña y genera carruseles de Instagram de estilo tech premium con avatar consistente.

La fuente principal vive en `skill/ig-tech-avatar-posts/`. Los scripts del repositorio permiten crear HTML y JPG desde JSONs versionables en `examples/`.

## Que incluye

- `skill/ig-tech-avatar-posts/`: skill principal con `SKILL.md`, referencias, metadata y scripts internos.
- `examples/`: entradas JSON listas para generar carruseles.
- `assets/avatar-upload/`: pack base de avatares con fondo transparente.
- `tools/scripts/`: utilidades para crear HTML, dividir slides, exportar JPG/PNG y validar el repositorio.
- `generar.py`: comando principal para generar un carrusel desde un JSON.

Las carpetas `outputs/`, `analysis/`, `diagnostics/` y `archive/` se tratan como artefactos locales y no se versionan.

## Instalacion local

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Generar un carrusel

Con el ejemplo por defecto:

```bash
python3 generar.py
```

Con un JSON concreto:

```bash
python3 generar.py examples/chatbots-vs-agentes.json
```

El comando genera:

- `outputs/carousels/<slug>/carousel.html`
- `outputs/carousels/<slug>/slides_html/`
- `outputs/carousels/<slug>/jpg/`

## Validar antes de commitear

```bash
python3 tools/scripts/validate_repo.py
```

La validacion comprueba:

- frontmatter basico de la skill;
- JSON valido en `examples/`;
- que los ejemplos renderizables tengan avatar;
- que el HTML generado no filtre textos internos conocidos.

## Contrato de `brand` y `hud`

La exportacion final no debe incluir marcas internas, nombres de la skill, nombres de template, placeholders, textos demo ni marcas de agua no solicitadas.

Todo texto decorativo debe venir del JSON:

```json
{
  "brand": {
    "show": true,
    "text": "Nombre o marca del usuario"
  },
  "hud": {
    "show": true,
    "top_left": "Categoria del post",
    "eyebrow": "Etiqueta tematica",
    "show_slide_number": true
  }
}
```

- Si `brand.show` es `false` o `brand.text` esta vacio, no se muestra marca inferior.
- Si `hud.show` es `false`, no se muestran textos decorativos superiores.
- La numeracion se muestra cuando `hud.show_slide_number` es `true`.

## Contrato de avatar

El avatar debe exportarse limpio, sin aura azul, glow, halo, silueta luminosa ni sombras decorativas pegadas al contorno.

La composicion puede usar fondo, grid o iluminacion ambiental, pero los efectos no deben contaminar el avatar.

## Versionado recomendado

```bash
git init
git add .
git commit -m "Initial InstagramSkill repository"
```

Antes de subirlo a GitHub, decide si quieres publicar el repositorio como privado o anadir una licencia open source.
