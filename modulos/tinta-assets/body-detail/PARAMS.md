# PARAMS — body-detail (Web / Les Vencimos tinta-estudio)

One-pager for wiring Jorge adult body-detail overlays into the paperdoll stack.

## Canvas
`512 × 768` RGBA. All paths relative to `vitaink-sprites-mari/`.

## Param API

| Param | Type | Range | Default | Path pattern | Notes |
|-------|------|-------|---------|--------------|-------|
| `nipples` | int | 0–3 | 0 | `body-detail/front/nipples/nipples-{n}.png` | Soft chest tones; 0 = empty |
| `bodyHair` | int | 0–3 | 0 | `body-detail/front/body-hair/body-hair-{n}.png` | Arms/legs/midline strokes |
| `armpit` | int | 0–2 | 0 | `body-detail/front/armpit/armpit-{n}.png` | Underarm shadow / light hair |
| `butt` | int | 0–3 | 0 | `body-detail/rear/butt/butt-{n}.png` | Rear view only |
| `buttSide` | int | 0–3 | 0 | `body-detail/side/butt-side-{n}.png` | Profile facing **left** (rear on right) |
| `showRear` | bool | — | `false` | — | If true: use `silhouette-rear` + `butt` instead of front stack |

## Draw order

### Front (`showRear === false`)
1. Existing body-shapes (bust + hips) / base silhouette  
2. `nipples`  
3. `bodyHair`  
4. `armpit`  
5. Cloth / outfit layers  

### Rear (`showRear === true`)
1. `body-detail/rear/silhouette-rear.png`  
2. `butt`  
3. Cloth  

### Side / ¾
1. Side body / silhouette  
2. `buttSide`  
3. Cloth  

## Tint
Overlays use muted taupe/brown at low alpha. Apply Web CSS / canvas `multiply` or `overlay` with the active skin tone so they read as skin-shadow, not fixed paint.

## Alignment anchors
- Bust center: `(256, 235)`  
- Nipples: `(220, 230)` and `(292, 230)`  
- Armpits: `(155, 188)` and `(355, 188)`  
- Rear butt CY: `420`  
- Side butt HX: `~310` (facing left)

## Level 0
Every series includes a fully transparent empty PNG at level 0 — safe no-op when the param is off.

## Catalog
Machine-readable: `body-detail/catalog.json` (`version`, `canvas`, `params`, `paths`, `drawOrder`).
