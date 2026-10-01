# body-detail — Jorge adult character kit overlays

Adult, **modest**, non-sexualized alpha body-detail layers for Les vencimos tinta-estudio / paperdoll.

## Canvas
- **512×768 RGBA**, transparent background
- Aligned to VitaInk body-shapes: bust ellipse center ~`(256, 235)`; hips band `y ~ 330–560`

## Style
- Soft painterly blobs / soft ellipses / gentle hatching — anatomical **suggestion** only
- Colors: muted skin-shadow browns/taupes (`rgba ~140,100,80` low alpha) so Web can tint
- No genitals, no explicit erotic posing, no underage content
- Level **0** = fully transparent empty PNG (same size)
- Procedural Pillow generation (no Mari face assets, no clothed photo copies)

## Layout
```
body-detail/
  catalog.json
  README.md
  PARAMS.md
  front/
    nipples/nipples-0.png .. nipples-3.png
    body-hair/body-hair-0.png .. body-hair-3.png
    armpit/armpit-0.png .. armpit-2.png
  rear/
    silhouette-rear.png
    butt/butt-0.png .. butt-3.png
  side/
    butt-side-0.png .. butt-side-3.png
```

## Draw order
- **Front:** silhouette / bust+hips → nipples → bodyHair → armpit → cloth
- **Rear:** silhouette-rear → butt → cloth
- **Side:** side body → buttSide → cloth

## Params (see PARAMS.md)
| param | range | folder |
|-------|-------|--------|
| nipples | 0..3 | front/nipples/ |
| bodyHair | 0..3 | front/body-hair/ |
| armpit | 0..2 | front/armpit/ |
| butt | 0..3 | rear/butt/ |
| buttSide | 0..3 | side/ |
| showRear | bool | swaps to rear silhouette + butt |

## Regenerate
```bash
/tmp/pilvenv/bin/python /workspace/vitaink-sprites-mari/body-detail/_gen_body_detail.py
```
