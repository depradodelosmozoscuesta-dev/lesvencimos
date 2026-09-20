# Re-anclaje puppet/side (2026-09-19)

Cloth day `viajero-pradera` sigue válido en anclas skel (puente KeyO).

Sección `puppet` en `placement.json` mapea a `mari/puppet/side/`:
- `torso.png` → `chest` (+ `abdomen` follow)
- `sleeves_R.png` → `upperarm` (lado near; facing right)
- `pants_R.png` → `thigh` (+ `hips` opcional)
- `boots_R.png` → `foot` (+ `calf` opcional)
- `cape.png` omitido (usar `acc_cape_short`)

`scale_ref_px` puppet = **1056**. PNGs cloth aún en escala ~512×768; Motor escala por pieza.


## front (2026-09-19)

`placement.json` → `puppet.views.front` (scale_ref **1056**):
- `torso.png` → chest (+ abdomen)
- `sleeves_L/R.png` → upperarm L/R
- `pants_L/R.png` → thigh L/R (+ hips opc.)
- `boots_L/R.png` → foot L/R (+ calf opc.)

Compat: `puppet.layers` sigue siendo **side**.


## q3 (2026-09-19)

`placement.json` → `puppet.views.q3` (facing **qleft**, scale_ref **1056**):
mismas capas L+R que front; pack `/assets/mari/puppet/q3/`.
Trío side+front+q3 cerrado en placement.
