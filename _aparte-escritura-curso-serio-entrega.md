# Entrega Web — Curso de dibujo SERIO (aparte Escritura)

Fecha: 2026-10-02 Europe/Madrid (UTC+2). **NO publicado. NO git push. NO deploy.**

Jorge rechazó la versión corta de 8 lecciones. Reconstruido como itinerario de atelier.

## Resumen
| Campo | Valor |
|---|---|
| Lecciones | **54** numeradas |
| Bloques | **12** |
| Archivo | `modulos/curso-dibujo.html` ≈ **92 KB** |
| Versión sugerida | `20261002b` |
| Offline | file://, CSP como antes, SVG inline, sin red |
| Progreso | TOC por bloques; `localStorage` última lección |

## Bloques (conteo de lecciones)
1. Materiales, postura y ver como artista — **4** (L01–L04)
2. Trazo, ritmo y calentamiento (gesto) — **4** (L05–L08)
3. Formas básicas y construcción — **4** (L09–L12)
4. Volumen: caja, cilindro, esfera, cono — **5** (L13–L17)
5. Perspectiva: profundidad creíble — **5** (L18–L22)
6. Luz y sombra — **5** (L23–L27)
7. Color: energía y luz (rueda, temperatura, complementarios, sombra de color, pincelada tipo Van Gogh) — **5** (L28–L32)
8. Composición — **4** (L33–L36)
9. Paisaje — **5** (L37–L41)
10. Bodegón — **4** (L42–L45)
11. Cabeza / retrato básico + figura vestida / gesto + manos — **5** (L46–L50)
12. Proyectos guiados (paisaje color vivo; bodegón tonal; serie de gestos; estudio de luz) — **4** (L51–L54)

Cada lección: prosa de oficio, 2–4 pasos, ejercicio con tiempo/materiales, enlace a Tinta Estudio, y quiz o autocrítica.

## Rutas tocadas (caja `/workspace/lesvencimos`)
| Ruta | Acción |
|---|---|
| `modulos/curso-dibujo.html` | Reescrito (54 lecciones) |
| `modulos/LEEME-curso-dibujo.txt` | Actualizado (itinerario serio) |
| `offline-pack-completo-embed/modulos/curso-dibujo.html` | Espejo |
| `offline-pack-completo-embed/modulos/LEEME-curso-dibujo.txt` | Espejo |
| `modulos/tinta-estudio.html` | Enlace: «Curso de dibujo · itinerario» + copy «itinerario serio (54 lecciones)» |
| `offline-pack-completo-embed/modulos/tinta-estudio.html` | Igual |
| `_aparte-escritura-curso-serio-entrega.md` | Este informe |

## Qué debe registrar Web (cuando autorice publicar)
1. **Catálogo** (`catalogo.json` + `app/catalogo.json`) — propuesto, **no aplicado** aquí:

```json
{
  "id": "curso-dibujo",
  "nombre": "Curso de dibujo",
  "version": "20261002b",
  "publico": "infantil",
  "red": false,
  "bytes": null,
  "sha256": null,
  "url": "https://lesvencimos.com/downloads/curso-dibujo-offline.zip",
  "entrada": "curso-dibujo.html",
  "permisos": []
}
```

Recalcular `bytes` / `sha256` tras empaquetar el ZIP (HTML + LEEME; el curso ya no es ~25 KB).

2. Preset `infantil`: `curso-dibujo` junto a `tinta-estudio` y `arte`. Opcional en `estudios`.
3. Empaquetar `downloads/curso-dibujo-offline.zip` y actualizar tarjeta en `descargas.html`.
4. **No** regenerar a mano los ~21 MB de `estanteria.html` salvo pipeline habitual.
5. Actualizar copy de catálogo/descargas: **itinerario / curso serio**, no «curso corto» ni «ocho lecciones».

## Qué NO se hizo
- Publicar, push, deploy, firmar ZIP.
- Editar `catalogo.json` / `estanteria.html` / ZIPs.
- Lecciones o SVG de anatomía íntima; no cablear `tinta-assets` body-detail / bust.
- Biografía de Van Gogh (solo oficio: gesto, color, luz, paisaje, bodegón, figura vestida).

## Relación producto
`curso-dibujo` = itinerario de estudio → práctica en `tinta-estudio`. `arte` = museos/estilos. `tinta-escritura` = editor de texto.
