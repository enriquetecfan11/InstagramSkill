# Parametros del JSON

Este archivo documenta el JSON que se puede pasar a `generar.py` para crear un carrusel de Instagram.

Ejemplo de uso:

```bash
python generar.py examples/chatbots-vs-agentes.json
```

## Estructura minima

```json
{
  "slug": "chatbots-vs-agentes",
  "tema": "ChatBots vs Agentes de IA",
  "angulo": "La diferencia real entre una IA que responde y una IA que ejecuta",
  "num_slides": 5,
  "cta": "Comenta AGENTES",
  "avatar": {
    "ruta": "assets/avatar-upload/imagen_1.png"
  },
  "visual": {
    "estilo": "tech premium oscuro editorial",
    "acento": "cyan",
    "motivo": "HUD UI",
    "formato": "1080x1080",
    "templates": "A/B alternado"
  }
}
```

Con esta estructura el sistema genera el contenido de las slides automaticamente.

## Estructura completa recomendada

```json
{
  "slug": "ia-automatizacion-ventas",
  "tema": "IA para automatizar ventas",
  "angulo": "Errores que hacen que tus automatizaciones no conviertan",
  "idioma": "ES",
  "num_slides": 7,
  "cta": "Comenta AUTOMATIZAR",
  "avatar": {
    "ruta": "assets/avatar-upload/imagen_1.png",
    "usar_pack": true,
    "regla": "obligatorio en todas las slides; template A avatar derecha, template B avatar izquierda"
  },
  "visual": {
    "estilo": "tech premium oscuro editorial",
    "acento": "cyan",
    "motivo": "HUD UI",
    "formato": "1080x1080",
    "margen_seguro": 64,
    "templates": "A/B alternado"
  },
  "brand": {
    "show": true,
    "text": "Tu marca"
  },
  "hud": {
    "show": true,
    "top_left": "Automatizacion IA",
    "eyebrow": "SISTEMAS",
    "show_slide_number": true
  },
  "slides": [
    {
      "titular": "Tu automatizacion no falla por la IA",
      "subtitulo": "Falla porque no tiene sistema.",
      "puntos": ["Demasiadas excepciones", "Datos sin limpiar"],
      "frase": "Primero sistema. Luego IA."
    },
    {
      "titular": "Error 1: automatizar caos",
      "subtitulo": "Si el proceso manual es confuso, la IA solo lo escala.",
      "puntos": ["Define entrada", "Define criterio"],
      "frase": "No automatices lo que aun no entiendes."
    }
  ]
}
```

## Campos principales

| Campo | Obligatorio | Tipo | Descripcion |
| --- | --- | --- | --- |
| `slug` | Si | string | Nombre corto para crear la carpeta de salida. Ejemplo: `chatbots-vs-agentes`. |
| `tema` | Recomendado | string | Tema general del carrusel. Se usa para generar slides si no las defines manualmente. |
| `angulo` | Recomendado | string | Enfoque editorial del post. Ejemplo: diferencia, errores, checklist, tutorial. |
| `idioma` | No | string | Idioma del contenido. Normalmente `ES` o `EN`. |
| `num_slides` | No | number | Numero de slides a generar si no pasas `slides`. Rango recomendado: 5 a 10. |
| `slides_count` | No | number | Alias de `num_slides`. |
| `cta` | No | string | Llamada a la accion final. Ejemplo: `Comenta SISTEMA`. |
| `avatar` | Si | object | Configuracion del avatar. Debe incluir `ruta`. |
| `visual` | No | object | Direccion visual general del carrusel. |
| `brand` | No | object | Marca inferior opcional. |
| `hud` | No | object | Textos decorativos superiores y numeracion. |
| `slides` | No | array | Slides escritas manualmente. Si falta, se generan automaticamente. |

## `avatar`

```json
{
  "avatar": {
    "ruta": "assets/avatar-upload/imagen_1.png",
    "usar_pack": true,
    "regla": "obligatorio en todas las slides"
  }
}
```

| Campo | Obligatorio | Tipo | Descripcion |
| --- | --- | --- | --- |
| `ruta` | Si | string | Ruta del avatar o carpeta de avatares. Puede ser relativa al repo o absoluta. |
| `usar_pack` | No | boolean | Si es `true`, usa varias poses del pack cuando la ruta esta en `assets/avatar-upload/`. Por defecto se comporta como activado. |
| `regla` | No | string | Nota editorial para documentar como debe usarse el avatar. |

El avatar es obligatorio. Si la ruta apunta a `imagen_1.png` y existe `no_bg_imagen_1.png`, el sistema puede usar la version limpia con fondo transparente.

Para carruseles con varias slides, la regla recomendada es usar `usar_pack: true` y apuntar a un archivo dentro de `assets/avatar-upload/`. El render debe seleccionar una pose diferente por slide siempre que haya suficientes avatares disponibles; no se debe repetir el mismo avatar en todo el carrusel.

## `visual`

```json
{
  "visual": {
    "estilo": "tech premium oscuro editorial",
    "acento": "cyan",
    "motivo": "HUD UI",
    "formato": "1080x1080",
    "margen_seguro": 64,
    "templates": "A/B alternado"
  }
}
```

| Campo | Obligatorio | Tipo | Descripcion |
| --- | --- | --- | --- |
| `estilo` | No | string | Direccion visual general. |
| `acento` | No | string | Color principal. Valores utiles: `cyan`, `electric blue`, `violet`, `magenta`. |
| `motivo` | No | string | Motivo visual: `HUD UI`, grid tecnico, nodos, dashboard, codigo, etc. |
| `formato` | No | string | Formato esperado. Actualmente recomendado: `1080x1080`. |
| `margen_seguro` | No | number | Margen interno de seguridad. Recomendado: `64`. |
| `templates` | No | string | Regla de composicion. Recomendado: `A/B alternado`. |

## `brand`

Controla si aparece una marca en la parte inferior.

```json
{
  "brand": {
    "show": true,
    "text": "Tu marca"
  }
}
```

| Campo | Obligatorio | Tipo | Descripcion |
| --- | --- | --- | --- |
| `show` | No | boolean | Muestra u oculta la marca. |
| `text` | No | string | Texto de marca. Si esta vacio, no se muestra. |

## `hud`

Controla los textos superiores y la numeracion.

```json
{
  "hud": {
    "show": true,
    "top_left": "Categoria del post",
    "eyebrow": "Etiqueta tematica",
    "show_slide_number": true
  }
}
```

| Campo | Obligatorio | Tipo | Descripcion |
| --- | --- | --- | --- |
| `show` | No | boolean | Muestra u oculta el HUD. |
| `top_left` | No | string | Texto superior izquierdo. |
| `eyebrow` | No | string | Etiqueta pequena encima del titular. |
| `show_slide_number` | No | boolean | Muestra numeracion tipo `01/07`. |

## `slides`

Si defines `slides`, el sistema usa tu contenido manual. Cada slide acepta:

```json
{
  "titular": "Error 1: automatizar caos",
  "subtitulo": "Si el proceso manual es confuso, la IA solo lo escala.",
  "puntos": ["Define entrada", "Define criterio"],
  "frase": "No automatices lo que aun no entiendes.",
  "layout": "left"
}
```

| Campo | Obligatorio | Tipo | Descripcion |
| --- | --- | --- | --- |
| `titular` | Si | string | Texto principal grande. Debe ser corto. |
| `subtitulo` | No | string | Texto de apoyo. |
| `puntos` | No | array | Lista de puntos. Se usan como maximo 2 en el render actual. |
| `frase` | No | string | Cierre corto o remate de la slide. |
| `layout` | No | string | Forzar orientacion visual. Valores utiles: `left`, `right`, `avatar-left`, `avatar-right`. |

## Reglas practicas de copy

- Usa titulares de 3 a 8 palabras.
- Evita parrafos largos dentro de `subtitulo`.
- Usa maximo 2 puntos por slide.
- Deja la slide final para CTA o guardado.
- Mantén una sola idea por slide.

## Ejemplo ultra corto

```json
{
  "slug": "mi-carrusel",
  "tema": "Agentes de IA",
  "angulo": "Como detectar cuando necesitas un agente y no un chatbot",
  "num_slides": 5,
  "cta": "Comenta AGENTE",
  "avatar": {
    "ruta": "assets/avatar-upload/imagen_1.png"
  }
}
```
