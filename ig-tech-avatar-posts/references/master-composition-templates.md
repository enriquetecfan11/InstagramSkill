# Master Composition Templates (Avatar Izquierda / Derecha)

Usar estas plantillas como sistema visual principal para carruseles cuadrados de Instagram con avatar. Son templates maestras de composición: deben guiar la estructura de cada slide antes de elegir fondos, motivos firma, micro-elementos UI o variaciones de pose.

## Formato base

- Tamano: 1080 x 1080 px.
- Estilo: tecnologico premium, editorial, moderno.
- Fondo: oscuro (navy / negro) con glow sutil azul o violeta.
- Margen seguro: 64 px minimo.
- Avatar: protagonista visual integrado.
- Texto: limpio, llamativo, sin cajas, sin bloques pesados.
- Diseno: impacto visual + lectura rapida + miniatura potente.

## Regla de secuencia

- Slide 1: hook fuerte.
- Slides intermedias: desarrollo claro.
- Ultima slide: cierre o CTA.
- Alternar A / B / A / B para dinamismo cuando el carrusel lo permita.
- El avatar debe parecer parte de la direccion de arte, no un elemento pegado encima.
- Cada slide debe funcionar sola como miniatura potente.

## Template A - Avatar Derecha

### Uso recomendado

Para slides donde el mensaje principal domina y el avatar refuerza visualmente desde la derecha. Ideal para hooks, introducciones y comparativas.

### Estructura visual

- Avatar grande en lado derecho.
- Titular potente en lado izquierdo.
- Subtitulo o frase de apoyo debajo.
- Texto secundario en formato simple: lineas, bullets o frases cortas.
- Numero de slide arriba derecha.
- Categoria pequena arriba izquierda.
- Frase clave o cierre abajo izquierda.

### Distribucion

- Texto principal: 40-45% izquierda.
- Avatar: 55-60% derecha.
- Titular ocupa zona alta-media.
- Avatar puede recortarse parcialmente abajo o lateral.
- Mucho espacio negativo.

### Reglas

- El titular manda visualmente.
- El avatar nunca invade la lectura.
- Nada de cajas pesadas.
- El texto debe respirar.
- Diseno tipo portada/editorial premium.

### Guia visual

```text
┌──────────────────────────────────────────────────────────────┐
│ CATEGORIA                                            [00/00] │
│                                                              │
│ TEXTO PRINCIPAL GRANDE                                       │
│ Hook potente y muy visual                                    │
│                                                              │
│ Subtitulo o frase secundaria                                 │
│                                                              │
│ - Punto clave                                                │
│ - Punto clave                                                │
│ - Punto clave                                                │
│                                                              │
│ Frase final / insight                                        │
│                                              ████████████    │
│                                           ████████████████   │
│                                         █████ AVATAR █████   │
│                                         █████ GRANDE █████   │
│                                         █████████████████    │
│                                           █████████████      │
│                                                              │
│ [Branding / Firma]                                           │
└──────────────────────────────────────────────────────────────┘
```

## Template B - Avatar Izquierda

### Uso recomendado

Para romper ritmo visual y alternar composicion manteniendo coherencia. Ideal para desarrollo, reflexion y cierre.

### Estructura visual

- Avatar grande en lado izquierdo.
- Titular potente en lado derecho.
- Subtitulo debajo.
- Texto secundario limpio y ordenado.
- Numero de slide arriba derecha.
- Categoria arriba izquierda.
- Frase clave o CTA abajo derecha.

### Distribucion

- Avatar: 55-60% izquierda.
- Texto principal: 55-60% derecha.
- Titular dominante.
- Avatar orientado visualmente hacia el contenido.
- Composicion espejada respecto al Template A.

### Reglas

- Mantener misma identidad visual.
- Sin cajas pesadas.
- Priorizar legibilidad inmediata.
- El avatar suma protagonismo, no ruido.
- Sensacion de carrusel premium y dinamico.

### Guia visual

```text
┌──────────────────────────────────────────────────────────────┐
│ CATEGORIA                                            [00/00] │
│                                                              │
│    █████████████                                             │
│  ████████████████                                            │
│ █████ AVATAR █████                                           │
│ █████ GRANDE █████      TEXTO PRINCIPAL GRANDE               │
│ █████████████████      Hook potente y muy visual             │
│   █████████████                                              │
│                                                              │
│                          Subtitulo o frase secundaria        │
│                                                              │
│                          - Punto clave                       │
│                          - Punto clave                       │
│                          - Punto clave                       │
│                                                              │
│                          Frase final / CTA                   │
│                                                              │
│                                           [Branding / Firma] │
└──────────────────────────────────────────────────────────────┘
```

## Aplicacion en prompts

Cuando se generen prompts por slide, declarar siempre:

- `Template A - Avatar Derecha` o `Template B - Avatar Izquierda`.
- Posicion del titular, subtitulo, numero de slide, categoria, frase final y branding.
- Porcentaje aproximado de ocupacion texto/avatar.
- Restriccion explicita: texto integrado sin cajas pesadas, margen seguro de 64 px, alta legibilidad movil.

## Control de consistencia

- Mantener tokens de `brand-tokens.md` en todas las slides.
- Usar los roles editoriales de `carousel-structure.md` para decidir el contenido.
- Usar `prompt-blocks.md` para estilo, fondo, tipografia y negativos.
- Alternar templates sin alterar paleta, tipografia, iluminacion ni motivo firma del carrusel.
