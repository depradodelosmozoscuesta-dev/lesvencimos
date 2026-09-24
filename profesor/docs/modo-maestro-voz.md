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

### Otros interactivos

Cada bot de asignatura documenta aquí los `type` que acepte su widget. Hasta entonces, pasos sin `iframeCmd` solo desplazan y señalan el marco.

## Música / ritmo

- Norma de producto: si una lección **ya** enlaza música o ritmo, los pasos del maestro pueden mencionarlo.
- **L01 piloto: sin música** (`"musica": false`). No inventar canciones ni pistas.
- Ganchos naturales futuros en Mate (cuando el contenido/QA lo lleve):
  - **L16–L18** fracciones (pizza / recta / suma) — ritmo de partes iguales.
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
