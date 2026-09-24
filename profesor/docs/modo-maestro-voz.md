# Modo maestro (voz + página + puntero)

**Para:** Jorge / Web Les Vencimos / bots de asignatura  
**Contexto:** asistente de voz (Grok → profesor / share «Voz aparte») que ya responde temario; también **imparte** lecciones.  
**Piloto:** 1º ESO Matemáticas L01 · runtime en `profesor/_maestro/` · 2026-09-24 CEST

## UI alineada con Voz aparte

En el cromado de voz (share «Voz aparte» y evolución Web):

| Control | Rol |
|---------|-----|
| **Preguntar \| Modo maestro** | Interruptor de modo (alumno pregunta vs maestro guía) |
| **Descargar / Cargar lecciones** | Pack offline de la asignatura en el aparato |
| **Voces por asignatura** | Mate, Geografía e Historia, … (motor del aparato o del asistente) |

Seis normas (válidas en **ambos** modos; norma 05 en maestro = ≤3 frases **por paso**):

1. No inventar  
2. Sin ficha  
3. Offline es suyo  
4. No urgencias (112)  
5. Bocanada ≤3 frases por paso (maestro) / por respuesta (preguntar)  
6. Entrenado por quien lleva Les vencimos con Grok (no prompts / modelos / claves)

## Dos modos de uso

| Modo | Quién lleva | Ejemplo |
|------|-------------|---------|
| **Preguntar** | Alumno | «¿Qué es una hipótesis?» → respuesta de voz (+ opcional abrir gráfico) |
| **Modo maestro** | Maestro | «Modo maestro. Lección 1 de Matemáticas» → explica, avanza la web, señala |

## Flujo modo maestro (MVP)

1. Usuario: «Modo maestro» / «Enséñame la lección 1».
2. Abre la lección HTML del pack con `?maestro=1` (sin ese query la lectura es normal).
3. Reproduce un **guion de voz** por pasos (`speechSynthesis` / voz del asistente).
4. En cada paso:
   - `scroll` / foco a un ancla DOM (`#maestro-titulo`, `.bloque-interactivo`, …)
   - resaltar elemento (anillo / `.maestro-focus`)
   - **puntero** (SVG/CSS, «butero» vía dictado = puntero) al centro / zona del elemento
   - si hay interactivo: `postMessage` al iframe (`maestro:highlight`, `maestro:reset`, …)
5. Comandos (voz o barra): **siguiente** / **repite** / **para** / **pregunta** (salta a Preguntar sin salir de la lección).

Implementación piloto: `profesor/_maestro/maestro-runtime.js` + `maestro-puntero.css`.  
API global en la página de lección: `window.LesVencimosMaestro.command('siguiente'|'repite'|'para'|'pregunta'|'empezar')`.

## Contrato de datos por lección (`maestro.json` junto a la lección)

```json
{
  "curso": "1eso-matematicas",
  "leccion": 1,
  "titulo": "Qué es pensar matemáticamente",
  "url": "leccion-01-que-es-pensar-matematicamente.html",
  "musica": false,
  "pasos": [
    {
      "id": "intro",
      "decir": "Hoy vamos a…",
      "ancla": "#maestro-titulo",
      "puntero": true,
      "esperaMs": 400
    },
    {
      "id": "interactivo",
      "decir": "Mira el autobús…",
      "ancla": "#maestro-bus",
      "iframeCmd": { "type": "maestro:reset" },
      "puntero": ".marco-interactivo"
    }
  ]
}
```

- Textos de voz en castellano claro (~12 años).
- Sin inventar currículo: el guion sigue el `NN.md` / saberes del decreto.
- Offline `file://`: sin CDN; voz del navegador o del motor del asistente.
- `decir`: máximo **3 frases cortas** por paso (norma 05).
- `puntero`: `true` (centro del ancla), selector CSS relativo/absoluto, o `false`.
- `iframeCmd`: objeto enviado con `postMessage` a los iframes de la lección.

Piloto: `1eso-matematicas/lecciones/maestro-01.json`.


## Diálogos y voces

El runtime habla con `speechSynthesis` del aparato (offline / `file://`). Por defecto cada paso usa el rol **narrador**. Se pueden cambiar voces por paso o montar un **diálogo** de varias réplicas.

### Roles (pitch / rate relativos)

| Rol | pitch | rate | Notas |
|-----|-------|------|-------|
| `narrador` | 1 | 1 | Voz por defecto |
| `chico` | ≈0.88 | ≈1.02 | Prefiere voces con pistas de nombre masculino |
| `chica` | ≈1.22 | ≈1.05 | Prefiere voces con pistas de nombre femenino |
| `mayor` | ≈0.72 | ≈0.82 | Más grave y pausado (vendedor / persona mayor) |
| `perro` | ≈1.75 | ≈1.35 | Juguetón; el texto debe ser corto tipo «¡Guau guau!» (TTS, **no** un ladrido real ni archivo de audio) |
| `timbre` | ≈1.4 | ≈1.15 | Imitación divertida / «otra voz» |

### Alias de guion → rol

| Clave en JSON | Rol de voz | Etiqueta en barra |
|---------------|------------|-------------------|
| `vendedor` | `mayor` | Vendedor |
| `alumna` | `chica` | Alumna |
| `alumno` | `chico` | Alumno |
| `narrador` / `chico` / `chica` / `mayor` / `perro` / `timbre` | el mismo | Capitalizado |

La barra muestra `Nombre: texto` y un chip de color (`.maestro-voz-chip`).

### API en el paso (`maestro.json`)

Línea única con voz:

```json
{
  "id": "ejemplo-chica",
  "voz": "chica",
  "decir": "Redondeo a decenas y ya veo el hinchazón.",
  "ancla": "#maestro-regateo"
}
```

Diálogo (réplicas en secuencia; `stop` / `siguiente` cancelan la cadena; entre líneas **no** se cancela a medias):

```json
{
  "id": "regateo-dialogo",
  "ancla": "#maestro-regateo",
  "puntero": true,
  "iframeCmd": { "type": "maestro:setPreview", "fair": 24, "offer": 38, "cat": "timo" },
  "dialogo": [
    { "voz": "vendedor", "decir": "¡Solo treinta y ocho euros!" },
    { "voz": "alumna", "decir": "Justo unos veinte. Oferta unos cuarenta: parece un timo." },
    { "voz": "perro", "decir": "¡Guau guau!" },
    { "voz": "narrador", "decir": "Estimar con redondeo detecta el hinchazón a ojo." }
  ]
}
```

Normas:

- ≤3 frases cortas **por réplica** (norma 05).
- Sin `voz` ni `dialogo` → narrador (guiones viejos siguen igual).
- `speak(texto, { voz })` acepta opciones; la cancelación brusca solo ocurre en **Para** / **Siguiente** / **Empezar** / **Repite**, no entre réplicas del mismo diálogo.
- `pickVoice('male'|'female'|'any')` elige entre voces `es-*` del aparato cuando existen pistas de género en el nombre.

### Límites del aparato

- Las voces instaladas dependen del SO / navegador: a veces solo hay una `es-ES`, o ninguna y cae a la primera voz del sistema.
- Pitch/rate ayudan a distinguir roles aunque la voz sea la misma.
- El «perro» es TTS exagerado (`¡Guau guau!`), no un fichero WAV/MP3 (MVP sin audio externo). Un beep WebAudio opcional puede llegar después.
- Piloto de diálogo: Mate L05 paso `regateo-dialogo` (mercadillo).


## Roles de voz y diálogo (runtime)

El runtime (`profesor/_maestro/maestro-runtime.js`) acepta:

- `voz`: rol o alias (`narrador`, `chico`, `chica`, `mayor`, `perro`, `timbre`; alias `alumno`→chico, `alumna`→chica, `vendedor`→mayor).
- `dialogo`: array de `{ voz, decir }` en un paso (multi-réplica; chip de rol en la barra).
- Sin `dialogo`, el paso usa `decir` con `voz` opcional (default `narrador`).

Norma 05: ≤3 frases por réplica / por `decir`.

## Puntero

- Capa fija sobre la lección: mano/flecha semitransparente (`#maestro-puntero`).
- Animación suave hacia `getBoundingClientRect()` del ancla.
- Visible solo en modo maestro; ocultar al salir / al **para**.

## postMessage API (interactivos)

El runtime reenvía `paso.iframeCmd` a cada `iframe` (`postMessage(cmd, '*')` por compatibilidad `file://`).

### L01 autobús (`l01-autobus-plazas.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | Vuelve al ejemplo 55 / 38 / 3 grupos × 6 |
| `maestro:highlight` | Resalta breve el panel de pasos / veredicto |
| `maestro:setPreview` | Opcional `{ cap, hay, grupos, tam }` en los sliders |
| `maestro:anim` | Dispara «Ver cómo suben» si no está animando |
| `maestro:ready` | (respuesta del iframe al cargar; el padre puede ignorarla) |

No romper controles existentes: el listener solo añade; no sustituye `onclick` de reset/anim.

### L02 sistemas (`l02-sistemas-numeracion.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | Ejemplo XLII → 42 |
| `maestro:highlight` | Resalta los tres paneles (decimal / romano / egipcio) |
| `maestro:setPreview` | Opcional `{ n }` (1–99) en el deslizador |
| `maestro:ready` | widget: `l02-sistemas-numeracion` |

### L02 monedas (`l02-monedas-cambio.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | Pestaña Roma + 100 € / 200 sestercios |
| `maestro:highlight` | Resalta la ecuación del panel activo |
| `maestro:setPreview` | Opcional `{ mode, euros, qty }` |
| `maestro:setMode` | `{ mode: 'roma' / 'sal' / 'divisas' }` |
| `maestro:ready` | widget: `l02-monedas-cambio` |

### L03 valor posicional (`l03-valor-posicional.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | Carga el ejemplo 5 082 |
| `maestro:highlight` | Resalta la tarjeta / forma desarrollada |
| `maestro:setPreview` | `{ n }` (0–99999) en las casitas |
| `maestro:ready` | widget: `l03-valor-posicional` |

### L04 recta numérica (`l04-recta-numerica.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | Ejemplo «colocar» 5 / 22 / 39 en 0–40 |
| `maestro:highlight` | Resalta la caja de comparación |
| `maestro:setExample` | `{ example: 'compare' / 'place' / 'between' }` |
| `maestro:setPreview` | Acepta `{ example }` (alias de setExample) |
| `maestro:ready` | widget: `l04-recta-numerica` |

### L05 redondeo (`l05-redondeo.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | Ejemplo 3 746 a centenas → 3 700 |
| `maestro:highlight` | Resalta frase / número redondeado / regla activa |
| `maestro:setPreview` | `{ n, order }` — `order` 10/100/1000 (decenas/centenas/millares) |
| `maestro:setDomain` | Alias: `{ domain: 'decenas'/'centenas'/'millares' }` o `order` |
| `maestro:ready` | widget: `l05-redondeo` |

### L05 regateo (`l05-regateo.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | Nueva partida de 6 puestos (ofertas aleatorias, a menudo hinchadas) |
| `maestro:highlight` | Resalta el precio ofertado |
| `maestro:setPreview` | `{ fair, offer, cat, name?, emoji? }` — demo de timo/ganga/justo (ignora payloads sin `fair`/`offer`) |
| `maestro:ready` | widget: `l05-regateo` |

### L06 suma/resta (`l06-suma-resta.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | Caja del mercadillo: 48 + 27, modo suma, sin demo |
| `maestro:highlight` | Resalta demo de propiedad o pantalla de la caja |
| `maestro:setDemo` | `{ demo: 'comm' / 'assoc' / null }` (alias `maestro:setExample`) |
| `maestro:setPreview` | `{ a, b, c?, mode: 'sum'/'diff', demo? }` |
| `maestro:setMode` / `maestro:setDomain` | `{ mode: 'sum'/'diff' }` |
| `maestro:ready` | widget: `l06-suma-resta` |

### L07 cajas de zumo (`l07-cajas-zumo.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | 3×4 botellas, modo ×, sin demo |
| `maestro:highlight` | Resalta el criptograma (o la demo si está abierta) |
| `maestro:setDemo` | `{ demo: 'comm' / 'assoc' / 'dist' / null }` (alias `maestro:setExample`) |
| `maestro:setPreview` | `{ a, b, c?, mode: 'mul'/'div', demo? }` |
| `maestro:setMode` / `maestro:setDomain` | `{ mode: 'mul'/'div' }` |
| `maestro:ready` | widget: `l07-cajas-zumo` |


### L08 torres y baldosas (`l08-torres-potencias.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | Modo potencia, a=2, n=3 (y s=4 en raíz) |
| `maestro:highlight` | Resalta la lista de cuadrados perfectos / escenario |
| `maestro:setDemo` / `setExample` | `{ demo: '23'/'34'/'52'/'sqrt81' }` (alias `2^3`, `root9`…) |
| `maestro:setPreview` | `{ mode: 'pow'/'root', a, n, s }` |
| `maestro:setMode` / `setDomain` | `{ mode: 'pow'/'root' }` (alias `raiz`, `baldosas`, `√`) |
| `maestro:ready` | widget: `l08-torres-potencias` |

### L09 excursión CyL (`l09-excursion-problemas.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | Problema autobús con a=4, b=5, c=6 |
| `maestro:highlight` | Resalta plan de pasos / expresión / escena |
| `maestro:setDemo` / `setExample` | `{ demo/problem: 'bus'/'shop'/'snack' }` (+ opcional a,b,c) |
| `maestro:setPreview` | `{ problem, a, b, c }` |
| `maestro:setMode` / `setDomain` | Alias de `problem` |
| `maestro:ready` | widget: `l09-excursion-problemas` |

### L10 bloques y criterios (`l10-bloques-divisibilidad.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | n=24, d=6, b=8, criterio ÷2 |
| `maestro:highlight` | Resalta la mesa de rectángulos / criterio |
| `maestro:setDemo` / `setExample` | `{ crit: 2/3/4/5/6/9/10 }` (o demo/example numérico) |
| `maestro:setPreview` | `{ n, d, b, m, crit }` — si viene `d`, prueba n÷d y resalta el rectángulo |
| `maestro:setMode` / `setDomain` | Alias de `crit` |
| `maestro:ready` | widget: `l10-bloques-divisibilidad` |


### L11 criba y factorización (`l11-criba-factorizacion.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | N=30, n=84, reinicia criba (+2 pasos) y factoriza |
| `maestro:highlight` | Resalta ladrillos / criba |
| `maestro:setDemo` / `setExample` | `{ n }` (o demo/example) → factoriza ese n |
| `maestro:setPreview` | `{ N, n, sieve: 'reset'/'step'/'all' }` — N y n independientes |
| `maestro:setMode` / `setDomain` | Alias de `sieve` o `{ n }` |
| `maestro:ready` | widget: `l11-criba-factorizacion` |

### L12 barras mcd/mcm (`l12-barras-mcd-mcm.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | a=18, b=24, problema mcd |
| `maestro:highlight` | Resalta varillas / Venn |
| `maestro:setDemo` / `setExample` | `{ a, b, prob: 'mcd'/'mcm' }` |
| `maestro:setPreview` | `{ a, b, prob }` |
| `maestro:setMode` / `setDomain` | Alias de `prob` (`mcd` / `mcm`) |
| `maestro:ready` | widget: `l12-barras-mcd-mcm` |

Diálogo opcional en el guion (rol `alumno` → chico, `narrador`): buses y «¿cada cuánto coinciden?» → mcm.

### L13 enteros en la recta (`l13-enteros-recta.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | a=−5, b=3, vista `line` |
| `maestro:highlight` | Resalta la escena activa (recta / termómetro / ascensor / fichas) |
| `maestro:setDemo` / `setExample` | `{ a, b, view: 'line'/'thermo'/'elev'/'chips' }` |
| `maestro:setPreview` | `{ a, b, view }` |
| `maestro:setMode` / `setDomain` | Alias de `view` |
| `maestro:ready` | widget: `l13-enteros-recta` |

### L14 operaciones con enteros (`l14-enteros-operaciones.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | a=−3, b=5, op `+` |
| `maestro:highlight` | Resalta salto (recta) o regla de signos según op |
| `maestro:setDemo` / `setExample` | `{ a, b, op: '+'/'/'*//' }` |
| `maestro:setPreview` | `{ a, b, op }` |
| `maestro:setMode` / `setDomain` | Alias de `op` |
| `maestro:ready` | widget: `l14-enteros-operaciones` |

Diálogo opcional: alumno↔narrador en resta de negativo (4−(−9)).

### L15 enteros en contextos (`l15-enteros-contextos.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | historia `debt` (paga) con preset de la lección |
| `maestro:highlight` | Resalta el escenario activo |
| `maestro:setDemo` / `setExample` | `{ story: 'debt'/'temp'/'elev', s0?, d1?, d2?, d3? }` |
| `maestro:setPreview` | `{ story, s0?, d1?, d2?, d3? }` (sin s0… usa preset) |
| `maestro:setMode` / `setDomain` | Alias de `story` |
| `maestro:ready` | widget: `l15-enteros-contextos` |

Diálogo opcional alumno↔narrador: corrige el paso ([E]), no a la persona.

### L16 fracciones pizza (`l16-fracciones-pizza.html`)

| type | Efecto |
|------|--------|
| `maestro:reset` | a=2, b=4, k=1, vista `pizza` |
| `maestro:highlight` | Resalta escena; `{ target: 'music' }` → panel negra/corchea |
| `maestro:setDemo` / `setExample` | `{ a|num, b|den, k, view: 'pizza'/'barra'/'rect'/'ambas', simplify? }` |
| `maestro:setPreview` | igual; `simplify: true` divide por mcd |
| `maestro:setMode` / `setDomain` | Alias de `view` |
| `maestro:ready` | widget: `l16-fracciones-pizza` |

Gancho ritmo ya en el md/widget (negra=1, corchea=1/2). `musica: false` (sin pista de audio).

### Otros interactivos

Cada bot de asignatura documenta aquí los `type` que acepte su widget. Hasta entonces, pasos sin `iframeCmd` solo desplazan y señalan el marco.

**Lote L02–L04 (2026-09-24):** guiones `maestro-02.json` … `maestro-04.json` + shells cableados; `musica: false`.

**Lote L05–L07 (2026-09-24):** guiones `maestro-05.json` … `maestro-07.json` + shells cableados; `musica: false`. L05 trae dos iframes (redondeo + regateo): cada widget ignora el payload que no le corresponde.

**Lote L08–L10 (2026-09-24):** guiones `maestro-08.json` … `maestro-10.json` + shells cableados; `musica: false`. Un iframe por lección (torres / excursión / bloques).

**Lote L11–L13 (2026-09-24):** guiones `maestro-11.json` … `maestro-13.json` + shells cableados; `musica: false`. Un iframe por lección (criba / barras / enteros). L12 incluye un diálogo corto alumno↔narrador (buses → mcm).

**Lote L14–L16 (2026-09-24):** guiones `maestro-14.json` … `maestro-16.json` + shells cableados; `musica: false`. Un iframe por lección (operaciones / contextos / pizza). L14 y L15 traen diálogo corto opcional; L16 menciona el panel de ritmo (sin audio).

## Música / ritmo

- Norma de producto: si una lección **ya** enlaza música o ritmo, los pasos del maestro pueden mencionarlo.
- **L01 piloto: sin música** (`"musica": false`). No inventar canciones ni pistas.
- Ganchos naturales futuros en Mate (cuando el contenido/QA lo lleve):
  - **L16–L18** fracciones (pizza / recta / suma) — ritmo de partes iguales. L16 ya tiene panel negra/corchea en el widget; el guion lo señala con `highlight`/`target: music` y `musica: false`.
  - **L23–L24** razones y proporcionalidad directa — tempo / “al doble, al triple”.
- Hasta que esas lecciones declaren audio en el shell o en el `maestro.json`, el runtime no reproduce nada.

## Qué hace cada bot de asignatura

1. Añadir `id` / `data-maestro` estables en secciones clave del shell y widgets.
2. Generar `maestro.json` (o embebido) por lección a partir del contenido ya QA.
3. Documentar comandos `postMessage` que acepta cada interactivo.
4. Enlazar `../../_maestro/maestro-puntero.css` + `maestro-runtime.js` y `data-maestro-json`.

## Qué hace el núcleo (asistente / Web)

1. UI: interruptor **Preguntar | Modo maestro** + Descargar/Cargar lecciones + voces por asignatura.
2. Orquestador: cola de pasos (hablar → esperar fin de voz → siguiente) — o delegar en `LesVencimosMaestro` inyectado en la lección.
3. Navegación entre lecciones del pack descargado con `?maestro=1` cuando toque guiar.
4. Integración con reconocimiento de voz ya existente (`siguiente` / `repite` / `para` / `pregunta`).
5. Detalle de cableado: `profesor/_maestro/README.md`.

## Rutas del piloto (Mate L01)

| Pieza | Ruta |
|-------|------|
| Design doc | `profesor/docs/modo-maestro-voz.md` |
| Runtime | `profesor/_maestro/maestro-runtime.js` |
| CSS puntero | `profesor/_maestro/maestro-puntero.css` |
| Demo cromado | `profesor/_maestro/maestro-demo.html` |
| README Web | `profesor/_maestro/README.md` |
| Guion | `profesor/1eso-matematicas/lecciones/maestro-01.json` |
| Shell L01 | `…/leccion-01-que-es-pensar-matematicamente.html` |
| Bus iframe | `…/l01-autobus-plazas.html` |
| Perímetro iframe | `…/l01-rectangulo-perimetro.html` |
| Fuente currículo | `…/01.md` |

**Probar:** abrir el shell L01 con `?maestro=1` vía `file://` → pulsar Empezar → puntero y voz. Sin query: comportamiento anterior.

## Norma Jorge (2026-09-24) — obligatorio

Tras el piloto L01 Mate, Jorge pidió **modo maestro en todo** lo que hagamos (Mate y demás asignaturas ESO), con el mismo mimo y calidad. No precipitar: lotes de ~3 lecciones, QA, publicar URLs `?maestro=1`.

Orden práctico: Mate L02→L47; luego ByG, GeoHistoria, Lengua. Skill: `lecci-n-eso-con-criterio-jorge`.
