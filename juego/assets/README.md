# Assets públicos (VitaInk Juego)

Estructura consumida por el motor (`/assets/...`).

| Carpeta | Contenido |
|---------|-----------|
| `mari/` | Paper-doll / skel / faces / body-shapes (mirror Assets) |
| `props/` | Props open-world day/night |
| `world/` | Biomas / tiles |
| `fauna/` | Fauna |
| `hud/` | HUD |

**Motor base** espera al menos `mari/skel/*.png` y `props/day/prop_{chest_closed,campfire_day,grass_cuttable}.png`.

El equipo **Motor / Assets** mantiene el mirror completo. No reestructurar carpetas sin actualizar `docs/ANCLAJES.md`.
