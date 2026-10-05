# NOTAS-REVISION · Educación Física 1º Bachillerato

Revisión del listón Bachillerato (SVG ≥2, ≥2 ejemplos con ≥4 pasos, 4 ítems de comprobación con porqué real, textarea + localStorage `bach1-ef-LNN`, canvas solo si la lección pide dibujar, `data-total=32` / `data-actual` coherente, nav anterior/siguiente a archivo largo, JSON `curso=bach1-educacion-fisica` y `leccion=N`).

Fecha de revisión: 2026-10-03 (Europe/Madrid).

## Resultado global

Las **32 lecciones largas** cumplen el listón. **No se reescribió ninguna** (no había hueco real que fallara).

## Criterio por criterio

| Criterio | Estado |
|----------|--------|
| ≥2 SVG de enseñanza | OK en L01–L32 (2 SVG cada una). `xmlns` w3.org no cuenta como enlace externo. |
| ≥2 ejemplos resueltos con ≥4 pasos | OK: cada lección tiene al menos 2 `<ol>` con ≥4 `<li>` en la zona de ejemplos. |
| 4 ítems de comprobación con porqué real | OK. L01–L16: `.quiz-feedback` con «Porqué.» argumentado. L17–L32: `data-why` con texto largo; el JS lo muestra al responder. Ningún porqué del tipo «solución: B». |
| textarea + localStorage `bach1-ef-LNN` | OK en las 32. Sin enlace a tinta/dibujo/estantería u otro módulo. |
| canvas solo si pide dibujar | OK. L28 sin canvas (solo editor), a propósito. L05, L14, L16–L27, L29–L32 llevan lienzo porque la propia lección pide dibujar en página. L01–L04, L06–L13, L15 sin canvas. |
| data-total 32 / data-actual / nav | OK. L01 sin anterior (disabled). L32 sin siguiente (disabled). Resto encadenadas al archivo largo. |
| JSON maestro | OK: 32 ficheros válidos, `curso=bach1-educacion-fisica`, `leccion` = N. |

## Seguridad (spot check, sin rebajar)

- **L08:** vigorexia, anorexia y bulimia definidas; sin métodos de restricción, purga u ocultación; ayuda = familia u orientador; malestar grave → 024.
- **L12:** protocolo escolar, no certifica, 112, PAS; RCP 30/2 o solo compresiones; DEA encender y obedecer; Heimlich escolar consciente; ictus cara-brazo-habla-tiempo; botiquín sin fármacos; no mover herido grave salvo peligro inminente.
- **Contacto / lucha leonesa (L17):** respeto y parar a la señal; sin técnicas de daño; solo con docente.
- **Exterior (L29–L32):** cuándo no ir solo; sin manual de escalada ni parkour.

## Hub creado en esta pasada

- `index.html` — índice local, CSS `leccion-shell.css`, iconos locales, sin CDN ni enlaces a otros módulos.
- `ABRE-AQUI.html` — meta refresh + `location.replace` + enlace visible a `index.html`; CSS local (no ruta `../../../profesor/`).
- `INDICE.md` — 32 líneas número / título / archivo largo / bloque.

## Lecciones corregidas

Ninguna.

## Quedó sin corregir

Nada pendiente del listón de esta tarea. No se creó LEEME ni se calcularon MD5 (fuera de alcance).
