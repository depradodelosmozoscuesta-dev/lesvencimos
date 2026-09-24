# Modo maestro — runtime offline (piloto Mate L01)

Para **Web / Voz aparte**: cablear el cromado de voz al pack Profesor sin CDN.

## Qué hay aquí

| Archivo | Rol |
|---------|-----|
| `maestro-runtime.js` | Cola de pasos: hablar → fin de voz → `scrollIntoView` → `.maestro-focus` → puntero → `postMessage` al iframe |
| `maestro-puntero.css` | Puntero fijo (mano SVG) + anillo de foco + barra flotante |
| `maestro-demo.html` | Demo Preguntar \| Modo maestro + enlace a L01 |
| `../docs/modo-maestro-voz.md` | Contrato `maestro.json`, normas, música, API iframe |

Guion piloto: `../1eso-matematicas/lecciones/maestro-01.json`  
Lección parcheada: `../1eso-matematicas/lecciones/leccion-01-que-es-pensar-matematicamente.html`

## Qué debe cablear Web en Voz aparte

1. **Toggle** ya esbozado en el share «Voz aparte»: **Preguntar | Modo maestro**.
2. **Descargar / Cargar lecciones** del pack `1eso-matematicas` (y otras asignaturas) al almacenamiento local del núcleo.
3. Voces por asignatura (Mate / Geografía…): el runtime usa `speechSynthesis` del aparato; Web puede sustituir el motor si el asistente ya habla.
4. Al oír «modo maestro» / «enséñame la lección 1»:
   - Abrir la HTML de la lección del pack **con** `?maestro=1`.
   - Eso muestra la barra Empezar / Siguiente / Repite / Para e inyecta puntero.
5. Sin `?maestro=1` la lección se lee como siempre (sin barra ni voz guiada).
6. Comandos de voz (mismo contrato que la barra):
   - `siguiente` → `LesVencimosMaestro.command('siguiente')`
   - `repite` → `…('repite')`
   - `para` → `…('para')`
   - `pregunta` → sale del guion y dispara `maestro:preguntar` (vuelve al modo Preguntar sin cerrar la lección).

## postMessage hacia interactivos

El runtime reenvía `paso.iframeCmd` a **todos** los `iframe` de la lección (`targetOrigin: '*'` por `file://`).

Piloto bus (`l01-autobus-plazas.html`):

- `maestro:reset` — ejemplo 55 / 38 / 3×6
- `maestro:highlight` — resalta veredicto / pasos
- `maestro:setPreview` — `{ cap, hay, grupos, tam }`
- `maestro:anim` — «Ver cómo suben»
- Al cargar, el iframe puede emitir `{ type: 'maestro:ready' }` (el padre puede ignorarlo)

## Música

- Norma: solo mencionar ritmo/música si la lección **ya** la enlaza.
- **L01: sin música** — no inventar canciones en el guion.
- Futuros ganchos naturales (Mate): L16–L18 fracciones; L23–L24 proporciones (ver doc).

## Cómo probar (file://)

1. Abrir  
   `profesor/1eso-matematicas/lecciones/leccion-01-que-es-pensar-matematicamente.html?maestro=1`  
   en Chromium / Firefox / Safari.
2. Pulsar **Empezar** (hace falta gesto de usuario para voz en casi todos los navegadores).
3. Comprobar puntero, anillo azul y avance por anclas `#maestro-*`.
4. Alternativa: `_maestro/maestro-demo.html` → Modo maestro → «Abrir L01» (más fiable que el iframe bajo `file://`).

## Limitaciones conocidas

- Voces `es-ES` dependen del SO; si no hay, usa la primera voz disponible o solo texto en la barra.
- Autoplay de voz: no arranca solo al cargar; siempre **Empezar**.
- `fetch` de JSON bajo `file://` falla en algunos navegadores: el runtime cae a XHR; si ambos fallan, incrustar el guion en `<script type="application/json" data-maestro="guion">`.
- `postMessage` al iframe hermano suele funcionar en `file://` mismo directorio; si el SO lo aísla, abrir el interactivo en pestaña no recibe comandos del padre.

## No tocar desde Web

- No reescribir el temario en prompts: el guion sale de `maestro-NN.json` alineado al `NN.md` QA.
- No pedir fichas, red ni 112 más allá de la norma 04.
