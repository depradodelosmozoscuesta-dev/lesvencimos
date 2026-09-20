# VitaInk Art HUD — Lote 3 (v3.1 pintura aventura)

Iconos HUD de aventura para VitaInk (móvil / touch), estilo **pintura aventura** (óleo suave + volumen), vibe BOTW + Arte Mundos.

**Arte ORIGINAL de VitaInk** — no son copias de assets de Zelda/Nintendo.

**Versión:** `3.1.0-lote3` · actualizado 2026-09-19 03:10 Europe/Madrid (UTC+2)

## ES — Qué incluye

### Estilo v3
- Volumen suave, textura de pincel sutil, highlights cálidos
- Contorno grueso legible a 48–64 px
- Fondo transparente (alpha)
- Sin personajes ni escenas; solo chrome/iconos HUD
- Sin texto dentro de los iconos

### Iconos base (day) + night + disabled
| Icono | Estados | Notas |
|-------|---------|-------|
| `heart` | full, empty | Rojo cálido con sheen |
| `stamina` | full, half, empty | **ANILLO DE ENERGÍA** verde (nunca manecillas de reloj) |
| `coin` | idle | Gema hexagonal cristal-hoja teal+oro |
| `quest` | idle | Pin ámbar con diamante |
| `tower_eye` | idle | Ojo pizarra azul frío |
| `inventory` | idle | Alforja de cuero con solapa + broche |
| `minimap-frame` | idle (+ night) | Marco circular vacío (centro transparente) |

- v3.1: quest pintada con letra **M**; corazón full mejorado y derivados hollow/night/disabled actualizados
- SVG: `svg/` (siluetas; stamina corregido sin manecillas)
- PNG: `png/128/`, `png/256/` (iconos); `png/256/` + `png/512/` (minimapa)
- Masters: `masters/` (512)
- Metadatos: `catalog.json`, `inventory.json`, `manifest.json` — **lote: 3**, style `pintura aventura`

**Tamaños recomendados:** HUD 48–64 px; hit-area táctil 64–72 px.

## EN — Brief

Adventure oil-paint HUD icon set (lote 3 / v3.1). Soft volume, brush texture, thick outlines, alpha backgrounds. Stamina is a **green energy ring/gauge** — clock-hands bug from v2 is fixed. Original VitaInk art.

## Destinos / Copy

1. Master: `/workspace/vitaink-art-hud/`
2. Game: `nuevo-internet/vitaink-juego/public/assets/hud/`
3. RCV: `nuevo-internet/red-ciudadano-valladolid/web/vitaink/sprites/hud/`

```bash
./COPY-TO-RCV.sh
# also rsync to vitaink-juego (see script notes / sync below)
```

## Regenerar

```bash
.venv/bin/python _gen/paint_hud_v3.py
```

GenerateImage was not available in the agent toolset; masters are procedural Pillow paint matching Arte Mundos volume/brush language.
