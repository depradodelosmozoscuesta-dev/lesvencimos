# QA bloque L22–L24 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)<br>
**Ruta primaria (interactivos):** `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `22.md` | Lección + glosario + interactivo (fracción–decimal–%) | ~6.3 KB |
| `23.md` | Lección razones/proporciones + interactivo | ~6.1 KB |
| `24.md` | Lección proporcionalidad directa + interactivo | ~6.8 KB |
| `l22-fraccion-decimal-porcentaje.html` | Interactivo offline (file://) | ~19 KB |
| `l22-fraccion-decimal-porcentaje-preview.png` | Preview Chrome headless | ~236 KB |
| `l23-razones-proporciones.html` | Interactivo offline | ~20 KB |
| `l23-razones-proporciones-preview.png` | Preview (recta doble) | ~285 KB |
| `l24-proporcionalidad-directa.html` | Interactivo offline | ~20 KB |
| `l24-proporcionalidad-directa-preview.png` | Preview (unidad 1-2-3) | ~276 KB |
| `_qa-bloque-22-24.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://` (sin red) para L22, L23, L24.
- [x] Preview L22 inspeccionado: modo fracción 1/4 → triad 1/4 · 0,25 · 25 %; rejilla 10×10 con 25 casillas rojas; barra 25 %; glosario `%` «por ciento».
- [x] Preview L23 inspeccionado: 3:4 = 9:12; recta numérica doble (a=3,c=9 / b=4,d=12); productos cruzados 36=36; razón simplificada 3:4.
- [x] Preview L24 inspeccionado: 4 cuadernos = 12 € → unidad 3 → 7 = 21; pasos 1-2-3; barras cantidad/total; mnemónico visible.

### Matemáticas
- [x] L22: 1/4=0,25=25 %; 3/5=0,6=60 %; 0,08→8 %=2/25; 45 %=0,45=9/20; 2/8=25 %.
- [x] L23: 3×12=4×9=36; 2×15=5×6=30; 5/8=20/x → x=32; 9/x=3/5 → x=15; 12:18→2:3.
- [x] L24: 4→12 ⇒ 7→21; 3→24 ⇒ 5→40; 6→9 ⇒ 10→15; 5 kg→12,50 ⇒ 3 kg→7,50; receta 4→600 ⇒ 6→900; taxi y/x no constante.

### Calidad Jorge (barra)
- [x] Glosario: L22 `%` «por ciento» / fracción / coma; L23 `a:b` / `=` de razones / productos cruzados; L24 unidad / k / igualdad de razones / NO directa — en HTML + md.
- [x] Visuales alineados al concepto: rejilla 100 (L22), recta doble + receta/mapa (L23), pasos a la unidad + tabla k + taxi (L24).
- [x] Controles independientes (modo de entrada L22; a,b,c,d L23; n₁,y₁,n₂ L24 — no se reescalan juntos).
- [x] Mnemónicos visibles en los 3 interactivos.
- [x] Tono ~12 años; contextos CyL (Burgos, León, Valladolid, Salamanca, recetas, descuentos).
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Sin inventar currículo: títulos/saberes alineados a hub CyL UD6/UD7 / Decreto 39/2022 A.2–A.5.

### Markdown
- [x] `22.md` / `23.md` / `24.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones.
- [x] Enlaces relativos a HTML + PNG.
- [x] Archivos comprobados en el árbol `lesvencimos`.

---

## Límites conocidos

1. **Rangos acotados:** L22 numerador/denominador hasta 200 y % hasta 200 (rejilla visual capada a 100 casillas); L23 valores numéricos libres pero la recta doble escala al máximo de cada magnitud; L24 n₁>0.
2. **L22 periódicos:** 1/3 se muestra ≈33,3 % con aviso de periódico; la rejilla usa sombreado parcial en la última casilla.
3. **L23 «Hallar x»:** deshabilita el término elegido; si el divisor necesario es 0, muestra aviso.
4. **L24 taxi:** contraejemplo didáctico (bajada + €/km); no es un tarifario real de una ciudad.
5. **Preview estática** del estado elegido (L22 1/4; L23 3:4=9:12; L24 unidad 4→12→7).
6. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.
7. **Coma vs punto:** inputs decimales aceptan ambos; la UI muestra coma española.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lesvencimos/profesor/1eso-matematicas/lecciones/l22-fraccion-decimal-porcentaje.html"
google-chrome "file:///workspace/lesvencimos/profesor/1eso-matematicas/lecciones/l23-razones-proporciones.html"
google-chrome "file:///workspace/lesvencimos/profesor/1eso-matematicas/lecciones/l24-proporcionalidad-directa.html"
```

---

## Veredicto

**OK para bloque 22–24.** Interactivos visibles y correctos, glosarios completos (`%` «por ciento», `a:b`, `=` de razones), visuals de rejilla-100 / recta doble / unidad alineados al concepto, previews alineados con la UI, sync en ambos árboles.
