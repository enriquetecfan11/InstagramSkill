---
name: ig-tech-avatar-posts
description: Diseñar carruseles completos de Instagram (5–10 slides) con identidad visual totalmente consistente (paleta, tipografía, composición, iluminación, fondos tech premium) y storytelling editorial optimizado para retención, branding y viralidad, usando un avatar/“muñeco” como ancla de marca en toda la secuencia. Usar cuando el usuario pida carruseles cohesionados (no posts sueltos), guiones slide-a-slide, dirección de arte unificada, copy corto integrado en la composición, y prompts listos para generar/editar todas las slides como una campaña reconocible.
---

# Ig Tech Avatar Posts

## Reglas visibles de exportacion

- Nunca exportar textos internos, placeholders, nombres de template, nombres de la skill ni marcas de agua no solicitadas.
- La marca inferior solo puede salir de `brand.text` cuando `brand.show` sea `true`.
- Los textos decorativos superiores solo pueden salir de `hud.top_left` y `hud.eyebrow`.
- La numeracion de slide solo depende de `hud.show_slide_number`.
- El avatar debe renderizarse limpio, sin aura azul, glow, halo, silueta luminosa ni `drop-shadow` decorativo.
- Antes de entregar una exportacion, validar el HTML final contra textos internos conocidos.
- Si se trabaja dentro del repositorio de la skill, ejecutar `python3 tools/scripts/validate_repo.py` antes de considerar lista una entrega versionable.

## Workflow

Producir un “carousel spec” repetible (story + dirección de arte + copy + prompts) con consistencia de marca y variedad controlada, priorizando claridad, espacio negativo, jerarquía y un look futurista profesional.

### 1) Intake (preguntar y fijar constraints)

- Pedir el **avatar** (ideal: PNG con fondo transparente) y su “rol” visual:
  - “Serio/autoridad”, “curioso/innovación”, “builder/acción”.
  - Si el usuario no aporta archivo, pedir **ruta local** o que lo adjunte; si no, trabajar con un “avatar placeholder” y dejar claro qué falta.
  - Si el usuario quiere dejarlo fijo, guardar el archivo como `assets/avatar.png` dentro de la skill.
- Pedir la **longitud del carrusel** (recomendado 7 slides; rango 5–10).
- Pedir el **tema** y el **ángulo** (1 frase): IA, automatización, devtools, SaaS, programación, producto, carrera.
- Pedir el **objetivo**: autoridad, lead, engagement, viralidad, hiring, lanzamiento.
- Pedir el **idioma** (ES/EN) y “energía” del copy (minimal / directo / audaz).
- Pedir el **CTA** deseado (comentar palabra, guardar, descargar plantilla, visitar link, DM).

### 2) Mantener constantes de identidad (no negociables)

- **Avatar protagonista**: punto focal principal; nunca “decorativo”.
- **Composición limpia**: 1 idea por pieza; máximo 2 niveles de mensaje (titular + soporte).
- **Espacio negativo**: dejar respirar; evitar “ruido” UI excesivo.
- **Fondo premium oscuro**: negros/grises profundos con detalle sutil (grids, partículas, UI glow).
- **Motivo firma** (elegir 1 por post y rotar): grid técnico, HUD UI, código, dashboards, nodos/flows, blueprint, scanner lines.
- **Sistema tipográfico**: 1 familia headline + 1 familia cuerpo + 2 pesos; siempre con la misma jerarquía.
- **Tokens de marca**: fijar paleta + acento + radio + grosor de línea + estilo de sombras (ver `references/brand-tokens.md`).
- **Textos decorativos configurables**: no imprimir nombres internos de la skill, nombres de template, marcas de agua, placeholders ni textos demo. Todo texto decorativo debe venir de `brand` o `hud` en el JSON.

### 3) Sistema de templates maestras (composicion principal)

- Para carruseles cuadrados 1080 x 1080, usar como base estructural `references/master-composition-templates.md`.
- Alternar **Template A - Avatar Derecha** y **Template B - Avatar Izquierda** para crear ritmo editorial sin romper identidad.
- Elegir la template por rol de slide:
  - A: hook, introduccion, comparativa, claim dominante.
  - B: desarrollo, reflexion, cierre o CTA.
- Mantener constantes el margen seguro, posicion de categoria/contador, branding, jerarquia del titular y ausencia de cajas pesadas.
- Declarar en cada prompt por slide la template elegida y los porcentajes texto/avatar.

#### Regla obligatoria de `avatar_box`

Cada slide debe dividirse en 2 zonas visuales invisibles:

- Zona texto: 55% del ancho.
- Zona avatar: 45% del ancho.
- El avatar siempre se renderiza dentro de una `avatar_box` fija, centrada dentro de su zona asignada y con `object-fit: contain`.
- En layout `texto / avatar`, el texto queda en la zona izquierda y la `avatar_box` en la zona derecha.
- En layout `avatar / texto`, la `avatar_box` queda en la zona izquierda y el texto en la zona derecha.
- El avatar no puede tocar bordes: margen lateral minimo 80px y margen inferior minimo 50px.
- El avatar debe quedar completo, sin cortar cabeza, brazos, piernas, silla ni accesorios.
- La altura visual objetivo del avatar es 55% a 70% del alto total, ajustando el escalado dentro de la caja sin romper los margenes.
- Esta prohibido colocar el avatar debajo del texto principal, superponer avatar y texto, o usar offsets libres negativos para posicionarlo.
- Esta prohibido añadir aura azul, glow, halo o silueta luminosa al avatar en HTML, JPG o PNG final.

Cuando el JSON incluya `visual.composicion`, respetar estos campos como contrato de render:

```json
{
  "grid": "2 columnas invisibles",
  "zona_texto": "55%",
  "zona_avatar": "45%",
  "avatar_safe_area": true,
  "avatar_centrado_en_su_zona": true,
  "avatar_altura": "55-70%",
  "margen_minimo_lateral": "80px",
  "margen_minimo_inferior": "50px",
  "evitar_cortes": true,
  "evitar_superposicion_texto": true
}
```

#### Regla obligatoria de `brand` y `hud`

El render final no debe contener textos internos, marcas de prueba, nombres de la skill, nombres del template, placeholders ni marcas de agua no solicitadas.

Todo texto decorativo debe salir de estas secciones del JSON:

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

- Si `brand.show` es `false` o `brand.text` esta vacio, no mostrar marca inferior.
- Si `hud.show` es `false`, no mostrar `top_left` ni `eyebrow`.
- La numeracion puede mostrarse aunque `hud.show` sea `false` si `hud.show_slide_number` es `true`.
- Antes de entregar, validar el HTML exportado contra textos internos conocidos.

### 4) Sistema de variedad (para no repetirse sin perder coherencia)

- Variar **layout** (ver `references/layouts.md`).
- Variar **familia de fondo** (1 por post):
  - “Neón suave + humo/volumen”, “UI glass + blur”, “Blueprint + líneas finas”, “Data particles”, “Terminal/código abstracto”.
- Variar **acento de color** (máx 1–2 acentos): cyan, electric blue, violet, magenta.
- Variar **elemento secundario** (máx 1): micro-dashboard, snippet, gráfico minimal, iconos outline.

### 5) Diseñar el carrusel como secuencia editorial (no slides sueltas)

Construir el carrusel como una **historia con propósito por slide**. Usar la estructura recomendada de `references/carousel-structure.md` y adaptar al tema.

Reglas de continuidad:
- Definir un **“Master Slide Style”** (tokens + grid + iluminación + motivo firma) y NO cambiarlo dentro del carrusel.
- Cambiar solo **deltas controlados** por slide (gesto del avatar, micro-elemento UI, 1 icono, 1 mini-gráfico).
- Mantener **posiciones consistentes**: titular, soporte, marca, motivo firma, avatar (con variaciones pequeñas).

### 6) Avatar como ancla recurrente (consistencia y estrategia)

- El avatar debe aparecer en todas las slides, pero **no siempre igual**:
  - Slides clave (1, 4/5, final): avatar **hero**.
  - Slides intermedias: avatar **recurrente** (más pequeño o lateral) para sostener reconocimiento sin robar lectura.
- Rotar “roles” del avatar (mirar al texto, señalar, pensar, confirmar, acción) para guiar la lectura.
- Si hay pack de poses: guardarlo en `assets/avatars/` y referenciar por nombre (ver `references/avatar-pack.md`).

### 7) Construir prompts (consistentes a nivel carrusel)

- Usar un **prompt base único** para el carrusel (estilo, tokens, motivo firma, tipografía, iluminación).
- Para cada slide, añadir solo:
  - **Rol del slide** (hook, problema, mecanismo, pasos, ejemplo, cierre).
  - **Template maestra** (A derecha / B izquierda) desde `references/master-composition-templates.md`.
  - **Texto exacto** (titular + microcopy).
  - **Gesto/pose del avatar** (y accesorio si aplica: laptop, café, móvil).
  - **Elemento visual** (1): mini-chart, snippet, flow, dashboard card.
- Si hay avatar en archivo:
  - Preferir **composición/edición** sobre “recrear” el avatar desde cero.
  - Pedir confirmación si se necesita recortar o recolor. No añadir glow, aura o halo al avatar.

### 8) Checklist de calidad (retención + lectura + unidad)

- ¿Portada “stop scroll” en 1 segundo (hook + avatar + contraste)?
- ¿Cada slide responde “¿y qué?” y empuja a la siguiente (transición natural)?
- ¿Se lee el titular en móvil sin zoom y con 2 niveles de texto máximo?
- ¿El master style se siente igual en todas las slides (paleta/tipo/luz/fondo)?
- ¿El avatar se repite con intención (guía visual, no ruido)?
- ¿Cierre con CTA o reflexión final clara?

## Output Format (si el usuario no especifica; carrusel completo)

Entregar un carrusel con:

1) **Master Slide Style** (tokens + grid + reglas de composición)
2) **Tabla slide-a-slide** (1..N): propósito, titular, microcopy, layout, avatar pose/rol, elemento visual, transición a la siguiente
3) **Prompts**:
   - Prompt base (constante)
   - Prompt por slide (solo deltas)
   - Negativos (constantes)
4) **Caption** (2–4 líneas) + **CTA** (1 línea) + 3 hashtags opcionales (máx)

## Resources

### `references/layouts.md`
Elegir layouts repetibles y variaciones seguras (feed y carrusel).

### `references/master-composition-templates.md`
Templates maestras 1080 x 1080 para carruseles con avatar a derecha/izquierda; usar como sistema visual principal de composicion.

### `references/carousel-structure.md`
Estructuras editoriales para carruseles (retención + narrativa) y roles por slide.

### `references/brand-tokens.md`
Tokens de identidad visual: paleta, tipografía, grid, líneas, sombras, glow, consistencia.

### `references/avatar-pack.md`
Cómo organizar un pack de poses, etiquetarlas, y asignarlas a roles de slide.

### `references/prompt-blocks.md`
Bloques de prompt para mantener coherencia estética y variar sin romper la identidad.

### `references/copy-formulas.md`
Fórmulas de copy corto, potente y estratégico (ES/EN) para titular + microcopy + caption.

### `scripts/make_post_spec.py` (opcional)
Generar un “post/carousel spec” en JSON con estructura fija (útil para iterar y versionar).
