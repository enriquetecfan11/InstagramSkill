# Layouts Premium para Carruseles Instagram con Avatar

Sistema visual repetible para crear carruseles cuadrados de Instagram con estética tecnológica premium, manteniendo consistencia de marca y evitando composiciones improvisadas.

---

## 1. Principio general

Cada carrusel debe construirse a partir de **dos templates maestros**:

- **Template A — Texto / Avatar**
- **Template B — Avatar / Texto**

La idea es alternarlos para crear dinamismo visual sin perder coherencia.

```text
Template A:  TEXTO  / AVATAR
Template B:  AVATAR / TEXTO
```

El avatar debe ser un elemento protagonista de marca, pero nunca debe bloquear, invadir ni competir con el texto principal.

---

## 2. Formato base

### Instagram cuadrado

- Tamaño: **1080 x 1080 px**
- Formato: **1:1**
- Uso principal: carruseles, miniaturas de feed y branding visual
- Margen seguro recomendado: **64–80 px**
- Fondo: oscuro, tecnológico, premium
- Estética: SaaS, IA, automatización, developer tools, HUD UI
- Avatar: grande, integrado y con presencia clara
- Texto: normal, limpio, grande, llamativo y sin cajas pesadas

---

## 3. Identidad visual

### Fondo

Usar una base oscura con profundidad:

- Navy oscuro
- Negro azulado
- Gradientes sutiles
- Glow azul/cyan/violeta muy controlado
- Grid fino o líneas HUD
- Elementos tecnológicos mínimos

Evitar:

- Fondos planos sin intención
- Exceso de glow
- Ruido visual
- Elementos que resten protagonismo al texto o avatar

---

## 4. Tipografía y texto

### Reglas de texto y Tamaños (Referencia)

- **Titular (Headline)**: `72px`, interlineado `1`, tracking `-1.5px`. Margen inferior de `38-42px`.
- **Subtítulo / Puntos clave**: `36px`, interlineado `1.15`. Separación vertical de `14px`.
- **Número de slide y Branding**: `20px`.
- Máximo 2 niveles principales:
  - Titular
  - Subtítulo / apoyo
- Máximo 2–3 bullets si son necesarios
- Frases cortas y memorables
- Sin cajas pesadas
- Sin párrafos largos
- Buena legibilidad en miniatura

### Jerarquía recomendada

```text
[CATEGORÍA PEQUEÑA]

TITULAR GRANDE
EN 2–4 LÍNEAS

Subtítulo corto con idea de apoyo.

• Punto clave
• Punto clave

Frase final / CTA
```

---

# 5. Template A — Texto / Avatar

## Uso

Ideal para:

- Portadas
- Hooks
- Claims fuertes
- Introducciones
- Comparativas simples
- Slides donde el mensaje debe liderar

## Composición

> **[IMPORTANTE]** Ya no se utiliza el antiguo diseño a ojo o manual. Para la composición visual del **Template A (Avatar a la Derecha)**, utiliza SIEMPRE el archivo base estructural:
> 
> 👉 **[`layout-left.html`](./layout-left.html)**
> 
> Este archivo proporciona el código fuente real con las proporciones, capas (`z-index`) y contenedores exactos que debes seguir.

## Distribución (Basado en layout-left.html)

- **Texto (Contenido)**: Lado izquierdo, ocupa el **48% del ancho**. Posicionado a `185px` desde arriba y `62px` desde la izquierda.
- **Avatar**: Lado derecho, ocupa el **56% del ancho**. Posicionado pegado a la derecha (`right: 0`) y abajo (`bottom: 0`).
- **Número de slide**: Arriba a la izquierda (`top: 48px; left: 48px;`).
- **Branding**: Abajo a la izquierda (`bottom: 42px; left: 48px;`).
- El avatar tiene `height: 100%` con `object-fit: contain` anclado a la base (`bottom center`).
- Avatar puede ir recortado por abajo o lateral derecho.
- El rostro debe tener presencia clara.

## Reglas

- El titular manda la lectura.
- El avatar acompaña y refuerza.
- El avatar puede mirar o señalar hacia el texto.
- No colocar texto detrás de cabeza, manos, portátil, taza u otros objetos.
- Dejar separación visual clara entre texto y avatar.
- El avatar debe parecer integrado, no pegado.

---

# 6. Template B — Avatar / Texto

## Uso

Ideal para:

- Desarrollo del carrusel
- Reflexiones
- Contrastes
- Slides de explicación
- Cierres
- CTAs

## Composición

> **[IMPORTANTE]** Ya no se utiliza el antiguo diseño a ojo o manual. Para la composición visual del **Template B (Avatar a la Izquierda)**, utiliza SIEMPRE el archivo base estructural:
> 
> 👉 **[`layout-right.html`](./layout-right.html)**
> 
> Este archivo proporciona el código fuente real con las proporciones, capas (`z-index`) y contenedores exactos que debes seguir.

## Distribución (Basado en layout-right.html)

- **Avatar**: Lado izquierdo, ocupa el **54% del ancho**. Posicionado pegado a la izquierda (`left: 0`) y abajo (`bottom: 0`).
- **Texto (Contenido)**: Lado derecho, ocupa el **46% del ancho**. Posicionado a `180px` desde arriba y `74px` desde la derecha.
- **Número de slide**: Arriba a la izquierda (`top: 48px; left: 48px;`), con `z-index: 3`.
- **Branding**: Abajo a la derecha (`bottom: 42px; right: 48px;`), con `z-index: 3`.
- El avatar tiene `height: 100%` con `object-fit: contain` anclado a la base (`bottom center`).
- Avatar puede ir recortado por abajo o lateral izquierdo.
- El avatar debe dirigir la atención hacia el texto.

## Reglas

- No debe ser una copia exacta invertida del Template A.
- Mantiene la misma marca, pero cambia el ritmo visual.
- El avatar puede ser más cercano, sentado, señalando, pensando o trabajando.
- El texto debe quedar en una columna limpia.
- La composición debe sentirse intencionada, no automática.

---

## 7. Uso del avatar

El avatar debe tener suficiente protagonismo para reforzar marca personal.

### Tamaño recomendado

- En portada: **60–75% del alto visual**
- En slides de desarrollo: **50–65% del alto visual**
- En cierre/CTA: **55–70% del alto visual**

### Buenas poses

Usar poses con intención:

- Pensando: para reflexión o duda
- Señalando: para destacar una idea
- Cruzado de brazos: para autoridad
- Con portátil: para trabajo, automatización o ejecución
- Con móvil: para herramientas, apps o interacción
- Saludando: para introducción o cierre
- Sentado: para slides más calmadas o conceptuales

### Reglas de integración

- Glow sutil, no exagerado
- Sombra suave de contacto
- Recorte limpio
- El avatar debe respetar el espacio de lectura
- No poner elementos importantes debajo del avatar
- Evitar que parezca un sticker pegado

---

## 8. Ritmo recomendado para carrusel

Para carruseles de 5 slides:

```text
Slide 1 — Template A
Hook fuerte + avatar hero

Slide 2 — Template B
Idea principal o primer concepto

Slide 3 — Template A
Desarrollo o contraste

Slide 4 — Template B
Ejemplo, error común o reflexión

Slide 5 — Template A o B
Cierre + CTA
```

Para carruseles de 7 slides:

```text
A / B / A / B / A / B / Cierre
```

La alternancia no debe ser rígida si el contenido pide otra cosa, pero sí debe mantenerse una sensación de sistema.

---

## 9. Estructura narrativa del carrusel

### Slide 1 — Portada

Objetivo: detener el scroll.

Debe tener:

- Hook muy claro
- Avatar protagonista
- Pocos elementos
- Alta legibilidad
- Máximo impacto en miniatura

### Slides intermedias

Objetivo: explicar una idea por slide.

Cada slide debe tener:

- Una sola idea
- Un titular claro
- Un apoyo corto
- Avatar integrado con intención
- Continuidad visual con el resto

### Slide final

Objetivo: cerrar y activar respuesta.

Puede incluir:

- CTA
- Pregunta
- Frase final contundente
- Invitación a comentar
- Resumen de la idea principal

---

## 10. Safe zones

### Margen general y posicionamiento

Según las referencias de los layouts, los márgenes operativos exactos son:
- **Superior/Inferior (Número y Branding)**: `48px` (superior) y `42px` (inferior).
- **Lateral (Contenido)**: `62px` (layout izquierdo) o `74px` (layout derecho).
- Mantener un respiro general y no salirse de estas coordenadas para mantener consistencia visual.

### Zonas críticas

Nunca colocar texto importante:

- Pegado al borde inferior
- Bajo el avatar
- Detrás del avatar
- En zonas de glow intenso
- En esquinas demasiado cargadas

### Regla de legibilidad

Si el diseño se ve pequeño en el grid de Instagram y no se entiende el titular en 1 segundo, el slide no es válido.

---

## 11. Qué evitar

Evitar siempre:

- Cajas grandes innecesarias
- Tablas visuales pesadas
- Demasiados bullets
- Texto largo
- Avatar pequeño sin protagonismo
- Avatar tapando texto
- Glow excesivo alrededor del avatar
- Slides demasiado vacías
- Composiciones idénticas en todo el carrusel
- CTA pegado al borde
- Fondos que parezcan genéricos

---

## 12. Checklist antes de aprobar una slide

Antes de dar una slide por válida, revisar:

- ¿El titular se lee rápido?
- ¿El avatar tiene protagonismo?
- ¿El avatar no tapa nada importante?
- ¿Hay suficiente margen?
- ¿El diseño se siente premium?
- ¿La slide funciona como miniatura?
- ¿Encaja con el resto del carrusel?
- ¿Hay una sola idea principal?
- ¿El espacio negativo parece intencionado?
- ¿La composición usa correctamente Template A o B?

---

# 13. Resumen operativo

Usar siempre este sistema:

```text
Formato: 1080 x 1080
Estilo: tech premium oscuro
Sistema: Template A + Template B
Texto: grande, claro, sin cajas pesadas
Avatar: protagonista, integrado y dinámico
Carrusel: coherente, alternado y editorial
Objetivo: miniaturas potentes + marca reconocible
```

El resultado debe parecer una campaña visual de marca personal sobre IA, automatización y tecnología, no una colección de slides sueltas.
