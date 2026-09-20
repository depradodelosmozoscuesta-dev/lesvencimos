# Mirror de assets VitaInk

**Fecha:** 2026-09-20 02:45 CEST (Europe/Madrid)
**Pipeline:** Motor Assets — mirror gráfico de VitaInk. Las fuentes no se borran.

## Mapa de rutas

| Origen principal | Destino |
|---|---|
| `/workspace/vitaink-sprites-mari/{faces,body-shapes,base,masters,paperdoll,from-mari-gym,skel}` | `public/assets/mari/` |
| `/workspace/vitaink-sprites-mari/world/{bosque,cielo,pradera,rio,roca,urbana}` | `public/assets/world/` |
| `/workspace/vitaink-art-props/{day,night}` | `public/assets/props/` |
| `/workspace/vitaink-art-fauna/{bird,deer,boar,fish,bat}` | `public/assets/fauna/` |
| `/workspace/vitaink-art-hud/{png,svg}` | `public/assets/hud/` |
| `/workspace/vitaink-art-ropa/day/<outfit>/` | `public/assets/ropa/day/<outfit>/` (cloth canónico) |
| `/workspace/vitaink-art-ropa/accessories/<outfit>/` | `public/assets/ropa/<outfit>/` (acc_*) |

Se copiaron también los metadatos/documentación solicitados (`README.md`, `manifest.json`, `catalog.json`, `inventory.json` y, en world, `palette.json`). Los huecos se rellenaron desde `/workspace/nuevo-internet/red-ciudadano-valladolid/web/vitaink/sprites/{mari,world,props,fauna,hud}/`, sin sustituir archivos del pack principal.

## Conteos del mirror

| Carpeta | Archivos totales | PNG | SVG | JSON |
|---|---:|---:|---:|---:|
| `mari/` | 874 | 859 | 0 | 11 |
| `world/` | 80 | 72 | 0 | 5 |
| `props/` | 14 | 11 | 0 | 2 |
| `fauna/` | 37 | 34 | 0 | 2 |
| `hud/` | 31 | 18 | 9 | 3 |
| `ropa/` | 78 | 69 | 0 | 6 |

`ropa/viajero-pradera/` catalog `2.4.1` — 111 PNG + placement.puppet (scale_ref 1056). Cloth day también con `puppet.layers`.

Se excluyeron los artefactos de generación y entornos de desarrollo (`_gen/`, `raw/`, `_raw/`, `_docs/` y `.venv*`) según el mapa del pack.


**World:** inventory `1.3.0-lote1-oleo-lapiz` (Arte Mundos v1.3 óleo+lápiz) — re-copiado 2026-09-18 02:33 desde `vitaink-sprites-mari/world/` (25 PNG, 6 biomas, mismos IDs).
**Side-persp:** inventory `3.1.0-collage-capas-all-biomes` — 5 biomas a 2048 (near/mid/far) + compat-1024. 32 PNG en `world/side-persp/` (sin `_gen` ni backups). Validado 2026-09-19 03:01.
**Skel-skin:** remirror 2026-09-19 03:18 — `head.png` + `torso.png` + `head-placement.json` + `previews/` (+ fallback camisole HQ).
**Puppet:** trío `mari/puppet/{side,front,q3}/` a scale_ref **1056** — mirrored. Cloth+acc `viajero-pradera` con `puppet.views.*`.
**Fullbody:** recomendado default Virginia `/assets/mari/fullbody/idle-clothed-side.png` (512×768, traveler clothed side-R). Alias de `side-persp/side-R/idle-clothed.png`. Pendiente remirror a juego-offline cuando Anclajes cambie default.
**Nota:** Este mirror pertenece al pipeline Motor Assets. No borrar ni modificar las fuentes.
