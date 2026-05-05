## Tooling local

Este repo incluye scripts para renderizar carruseles a HTML y exportar imágenes a partir de JSONs en `examples/`.

### Requisitos

- Python **3.10+**

### Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Generar un carrusel

Con el ejemplo por defecto (usa `examples/`):

```bash
python3 generar.py
```

Con un JSON concreto:

```bash
python3 generar.py examples/chatbots-vs-agentes.json
```

Salida por cada carrusel:

- `outputs/carousels/<slug>/carousel.html`
- `outputs/carousels/<slug>/slides_html/`
- `outputs/carousels/<slug>/jpg/`

### Scripts útiles

```bash
python3 tools/scripts/create_slides_from_json.py <input.json>
python3 tools/scripts/export_jpg_from_json.py <input.json>
python3 tools/scripts/export_carousel_images.py <slug_o_dir>
python3 tools/scripts/render_carousel_pngs.py <slug_o_dir>
python3 tools/scripts/split_carousel_html.py outputs/carousels/<slug>/carousel.html
```

### Validar antes de commitear

```bash
python3 tools/scripts/validate_repo.py
```

La validación comprueba:

- frontmatter básico de la skill;
- JSON válido en `examples/`;
- que los ejemplos renderizables tengan avatar;
- que el HTML generado no filtre textos internos conocidos.

