# QA bloque L19–L21 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)<br>
**Ruta primaria (interactivos):** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`<br>
**Sync:** mismos HTML/PNG/md copiados a `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`<br>
*(Ambos árboles existen.)*

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `19.md` | Lección + glosario + interactivo (×/÷ fracciones) | ~7.0 KB |
| `20.md` | Lección problemas + interactivo CyL | ~7.1 KB |
| `21.md` | Lección decimales + interactivo €/rejilla | ~6.6 KB |
| `l19-fracciones-producto.html` | Interactivo offline (file://) | ~22 KB |
| `l19-fracciones-producto-preview.png` | Preview Chrome headless | ~288 KB |
| `l20-problemas-fracciones.html` | Interactivo offline | ~25 KB |
| `l20-problemas-fracciones-preview.png` | Preview (libro Salamanca, pasos) | ~361 KB |
| `l21-decimales-euro.html` | Interactivo offline | ~28 KB |
| `l21-decimales-euro-preview.png` | Preview (dinero € / cambio) | ~296 KB |
| `_qa-bloque-19-21.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://` (sin red) para L19, L20, L21.
- [x] Preview L19 inspeccionado: modo × con modelo de área (2/5×3/4 → celdas verdes 6/20 → 3/10); modo ÷ verificado aparte (`?op=div`): panel «DAR LA VUELTA AL 2.º» 3/4÷1/8 → ×8/1 → 6.
- [x] Preview L20 inspeccionado: problema libro Salamanca «de lo que queda», cinta coloreada, 4 pasos visibles, respuesta con unidades.
- [x] Preview L21 inspeccionado: modo Dinero € (5,14 €), rejilla posicional con coma, billetes/monedas, cambio de 10 € = 4,86 €.

### Matemáticas
- [x] Producto: 2/5×3/4 = 6/20 = 3/10; 1/2×3/4 = 3/8; cancelación 4/9×3/8 = 1/6.
- [x] División: 3/4÷1/8 = 3/4×8/1 = 6; 2/3÷4/5 = 2/3×5/4 = 5/6; aviso c=0.
- [x] Problemas: bus 3/5 de 240 = 144; libro 1/4 luego 1/3 del resto → 60; oferta 1/5 de 40 = 32 €.
- [x] Decimales: 2,45+0,8=3,25; 5−1,28=3,72; 1,2×0,3=0,36; 7,5÷0,5=15; 3,07<3,7; redondeo a céntimo.

### Calidad Jorge (barra)
- [x] Glosario: L19 `×`/`÷`/`=`/inversa/«de»/mcd; L20 todo/resto/`×+−÷`/cinta; L21 coma/décima/€/`<>/=` — en HTML + md.
- [x] Visuales alineados al concepto: área (×), «dar la vuelta al segundo» (÷), cinta CyL (problemas), rejilla + billetes/monedas €.
- [x] Controles independientes (a↔b, c↔d, N/fracciones, A↔B; modos no reescalan el otro número).
- [x] Mnemónicos visibles en los 3 interactivos.
- [x] Tono ~12 años; contextos CyL (Valladolid, León, Burgos, Salamanca, Ávila, Segovia).
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Sin inventar currículo: títulos/saberes alineados a hub CyL UD5/UD6 / Decreto 39/2022 A.2–A.3.

### Markdown
- [x] `19.md` / `20.md` / `21.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lescircimos` y `lesvencimos`.

---

## Límites conocidos

1. **Rangos acotados:** L19 a,c=0…12 y b,d=1…10 (rejilla de área legible); L20 totales y fracciones por problema; L21 rejilla hasta 999,999.
2. **Área L19:** filas=denominador 1.º, columnas=denominador 2.º; numeradores > denominadores se recortan visualmente en el sombreado.
3. **L20 «de lo que queda»:** un solo escenario de dos pasos encadenados (libro); otros son un paso o suma de fracciones del mismo total.
4. **L21 dinero:** desglose en billetes/monedas es visual (no caja registradora exacta de todas las combinaciones mínimas).
5. **Preview estática** del estado elegido (L19 producto 2/5×3/4; L20 libro pasos abiertos; L21 5,14 € con cambio de 10).
6. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.
7. **Coma vs punto:** el input acepta ambos; la UI muestra coma española.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l19-fracciones-producto.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l20-problemas-fracciones.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l21-decimales-euro.html"
```

---

## Veredicto

**OK para bloque 19–21.** Interactivos visibles y correctos, glosarios completos, visuals de área / inversa / cinta CyL / rejilla+€ alineados al concepto, previews alineados con la UI, sync en ambos árboles.
