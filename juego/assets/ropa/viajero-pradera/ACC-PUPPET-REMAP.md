# Accesorios → puppet (2026-09-19)

Pack `viajero-pradera` acc — sección `puppet` en `placement.json`.

## Trío (scale_ref_px **1056**)
| view | facing | pack | notes |
|------|--------|------|-------|
| `side` (default `puppet.layers`) | right | `/assets/mari/puppet/side/` | L limbs far/optional |
| `front` → `puppet.views.front` | front | `/assets/mari/puppet/front/` | L+R limbs |
| `q3` → `puppet.views.q3` | qleft | `/assets/mari/puppet/q3/` | near bias L |

## Anclas
- hip props → `hips` (+ abdomen follow)
- hand props → `hand` (+ forearm opt.)
- `acc_cape_short` → `chest` (+ abdomen drape) — **no** day cape
- head jewelry → `head`

Puente skel `slots` intacto. @Motor Anclajes: tras cloth, consumir `puppet.layers` (side) o `puppet.views.<view>.layers`.
