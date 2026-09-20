# VitaInk World / Terrain — LOTE 1 (Calles)

**ES** · Pack de tiles PNG-alpha para el mapa open-world Calles (capa civic Valladolid + aventura tipo Zelda BOTW).

**EN** · PNG-alpha tile/overlay pack for the Calles open-world map (Valladolid civic + BOTW-like adventure layer).

## Biomes

| Biome   | Contents                                      |
|---------|-----------------------------------------------|
| pradera | Grass tiles + flower accents                  |
| bosque  | Canopy / trees                                |
| roca    | Rock / mountain cliffs + lichen               |
| rio     | Water + shore / orilla + foam                 |
| urbana  | Stylized Valladolid (plaza caliza, tejas, ocre) |
| cielo   | Day sky + sunset / atardecer + cloud strip    |

## Layout

```
world/
  palette.json
  catalog.json
  inventory.json
  COPY-TO-RCV.sh
  <biome>/{top,front,overlays}/*.png
```

- **top/** — orthographic / high-angle map tiles (~128px source; display ~64px)
- **front/** — elevated / side billboards or horizon strips (sky 16:9)
- **overlays/** — soft edge blends, foam, lichen, clouds

## Style

Painted adventure art, clear silhouettes, transparent backgrounds (sky plates may be opaque gradients with soft alpha edges). No characters, no UI text. Colors from `palette.json`.

## Copy to RCV

```bash
bash /workspace/vitaink-sprites-mari/world/COPY-TO-RCV.sh
```

Target: `/workspace/nuevo-internet/red-ciudadano-valladolid/web/vitaink/sprites/world/`

## Catalog

See `catalog.json` for every asset `id`, `biome`, `view`, relative `path`, `tags`, and `palette_ref`.
