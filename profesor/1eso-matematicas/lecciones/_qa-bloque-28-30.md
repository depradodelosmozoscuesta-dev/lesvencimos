# QA bloque L28–L30 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)
**Ruta primaria (interactivos):** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`
**Sync:** mismos HTML/PNG/md copiados a `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`
*(El usuario escribió «lescircimos» dos veces; el espejo real es **lesvencimos**.)*

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `28.md` | Lección magnitudes/unidades + glosario + interactivo | ~6.4 KB |
| `29.md` | Lección medir / precisión / estimación + [interactivo] | ~6.7 KB |
| `30.md` | Lección áreas elementales (deducción) + interactivo | ~6.3 KB |
| `l28-magnitudes-unidades.html` | Interactivo offline (file://) | ~31 KB |
| `l28-magnitudes-unidades-preview.png` | Preview Chrome headless | ~253 KB |
| `l29-regla-transportador.html` | Interactivo offline | ~24 KB |
| `l29-regla-transportador-preview.png` | Preview (regla + error) | ~249 KB |
| `l30-areas-figuras.html` | Interactivo offline | ~27 KB |
| `l30-areas-figuras-preview.png` | Preview (triángulo + fantasma) | ~278 KB |
| `_qa-bloque-28-30.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://…?preview=1` (sin red) para L28, L29, L30.
- [x] Preview L28 inspeccionado: modo **Longitud** · objeto **Lápiz**; regla real cm/mm; lápiz alineado 0→18 cm; convertidor 18 cm → 180 mm (×10); glosario magnitud/unidad/cantidad; mnemónico 10 000.
- [x] Preview L29 inspeccionado: **Regla**; objeto «lápiz del estuche»; E=14,0 cm · M=14,6 cm · error **0,6 cm**; feedback «Bien: estás cerca»; marcas mm; aviso del 0 y parallax; glosario E/M.
- [x] Preview L30 inspeccionado: **Triángulo** b=10 cm · h=6 cm → **A=30 cm²**; rectángulo fantasma + «otra mitad»; h ⊥ base; glosario A/b/h; perímetro ≠ área.

### Matemáticas
- [x] L28: 18 cm = 180 mm; 2,3 m = 230 cm; 3 m² = 30 000 cm²; 50 cm² = 0,005 m².
- [x] L29: \|14,0 − 14,6\| = 0,6 cm; clasificación agudo/recto/obtuso/llano en modo ángulo.
- [x] L30: triángulo ½×10×6=30; cuadrado 9²=81; rectángulo 12×4,5=54; paralelogramo 11×3=33; trapecio ½(10+6)×4=32; L: 6×4+3×2=30.

### Calidad Jorge (barra L01)
- [x] **Dibujos = lo que nombran:** regla con marcas cm/mm (L28/L29); transportador semicircular con grados (L28/L29); áreas con cuadrícula / rectángulo fantasma / despiece L (L30) — no charcos/blobs.
- [x] **Controles independientes:** L29 E y M no se reescalan juntos; L30 scaleX/scaleY fijos por unidad (mover b no encoge h en pantalla).
- [x] **Glosario de letras en español primero:** magnitud/unidad/cantidad; E/M; A, b, h, L, B, P — en HTML + md.
- [x] Mnemónicos visibles en los 3 interactivos.
- [x] Tono ~12 años; contextos CyL (Segovia, Valladolid, León–Astorga, Salamanca…).
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Sin inventar currículo: UD9 L28–L30 · Decreto 39/2022 B.1–B.3.

### Markdown
- [x] `28.md` / `29.md` / `30.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones/reto.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lescircimos` y `lesvencimos`.

---

## Límites conocidos

1. **L28 objetos:** cantidades «típicas» orientativas (lápiz ≈ 18 cm, León–Astorga ≈ 48 km), no medidas de campo.
2. **L28 área km²:** factor incluido para completar el convertidor; en 1º se usa poco.
3. **L29 transportador:** escala 0°–180° en semicírculo superior (modelo escolar); no simula corona doble interior/exterior completa.
4. **L29 parallax:** se explica en texto; no hay cámara 3D.
5. **L30 altura exterior (obtusángulo):** mencionada en el md; el interactivo dibuja triángulo rectángulo/agudo apoyado en la base para la deducción ½.
6. **L30 compuesta (L):** el segundo rectángulo está fijado a 3×2 (ejemplo de la lección); solo b×h del bloque grande es variable.
7. **Preview estática** del estado `?preview=1` (L28 lápiz 18 cm→mm; L29 E=14/M=14,6; L30 tri 10×6=30).
8. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.
9. **Coma vs punto:** inputs aceptan ambos en cantidad L28; la UI muestra coma española en lecturas.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l28-magnitudes-unidades.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l29-regla-transportador.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l30-areas-figuras.html"
```

---

## Veredicto

**OK para bloque 28–30.** Interactivos visibles y correctos; glosarios con magnitud/unidad/cantidad, E/M y A/b/h/L/B; visuals de regla / transportador / rectángulo fantasma alineados al concepto (barra L01); controles independientes b↔h; previews alineados con la UI; sync en ambos árboles.
