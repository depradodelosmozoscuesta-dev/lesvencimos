# QA bloque L34–L36 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)
**Ruta primaria (interactivos):** `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`
**Pack canónico:** HTML/PNG/md en `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `34.md` | Lección congruencia/semejanza/escalas + glosario + interactivo | ~6.5 KB |
| `35.md` | Lección Tales + criterios AA/LAL/LLL + glosario + interactivo | ~7.0 KB |
| `36.md` | Lección relación pitagórica + glosario + interactivo | ~6.3 KB |
| `l34-semejanza-escalas.html` | Interactivo offline (file://) | ~21 KB |
| `l34-semejanza-escalas-preview.png` | Preview Chrome headless (3-4-5 → 6-8-10, k=2) | ~192 KB |
| `l35-tales-semejanza.html` | Interactivo offline | ~28 KB |
| `l35-tales-semejanza-preview.png` | Preview (haz + 2 paralelas, t=0.35/0.72) | ~204 KB |
| `l36-pitagoras.html` | Interactivo offline | ~24 KB |
| `l36-pitagoras-preview.png` | Preview (3-4-5 con cuadrados a²/b²/c²) | ~221 KB |
| `_qa-bloque-34-36.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://…?preview=1` (sin red) para L34, L35, L36.
- [x] Preview L34 inspeccionado: **Dos triángulos** a=3 · b=4 · c=5 · k=2 → imagen 6-8-10; marcas de ángulos iguales + ticks homólogos; áreas 6→24 (×k²=4).
- [x] Preview L35 inspeccionado: **Tales (paralelas)**; haz desde O + dos ∥ rojas; OA/OC ≈ OB/OD ≈ AB/CD ≈ 0,49; controles t1/t2/aperturas independientes.
- [x] Preview L36 inspeccionado: **Cuadrados en los lados** 3-4-5; cuadrados azul/verde/rojo con a²=9, b²=16, c²=25; ecuación 3²+4²=5²; ternas clicables.

### Matemáticas
- [x] L34: semejanza k=2 en 3-4-5; congruencia = k=1; escala 1:n → real = plano×n (misma unidad); áreas ×k².
- [x] L35: Tales OA/OC = OB/OD = AB/CD; paralela en triángulo → AA; sombra h = h_pers × s_edif/s_pers (1,7×6,8/0,85=13,6).
- [x] L36: a²+b²=c² con áreas visibles; cateto √(c²−b²); recíproco escolar; ternas 3-4-5 / 5-12-13 / 6-8-10…

### Calidad Jorge (barra L01)
- [x] **Dibujos = lo que nombran:** triángulos semejantes con marcas (L34); haz + paralelas cortando rayos (L35); rectángulo con cuadrados sobre los lados (L36) — no blobs.
- [x] **Controles independientes:** L34 a/b/c/k; L35 t1/t2/aperturas; L36 catetos a y b (c calculado).
- [x] **Glosario en español primero:** a/b/c/k/escala/homólogos; ∥/haz/AA/LAL/LLL; catetos/hipotenusa/terna — en HTML + md.
- [x] Mnemónicos visibles en los 3 interactivos.
- [x] Notas históricas **honestas**: Tales (versión escolar moderna; atribución tradicional); Pitágoras (ternas babilónicas previas; escuela pitagórica).
- [x] Tono ~12 años; UD11 Semejanza, Tales y Pitágoras.
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Sin inventar currículo: UD11 L34–L36 · Decreto 39/2022 C.1.

### Markdown
- [x] `34.md` / `35.md` / `36.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones/reto.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lescircimos` y `lesvencimos`.

---

## Límites conocidos

1. **L34 triángulo libre:** desigualdad triangular bloquea dibujo si a+b≤c; umbral visual de marcas fijo.
2. **L34 escala:** la barra gráfica es ilustrativa (80 px ≈ conversión didáctica); no es un mapa geodésico.
3. **L34 áreas:** Herón para el área mostrada; redondeo a 2 decimales.
4. **L35 Tales:** las dos transversales son rayos desde O; las ∥ se dibujan por los puntos a parámetro t (no arrastre libre tipo GeoGebra).
5. **L35 sombras:** rayos solares ≈ paralelos (modelo escolar); el edificio se comprime visualmente si la altura es enorme para caber en el SVG.
6. **L35 AA:** construye dos triángulos con los mismos ángulos A y B; el tercero = 180°−A−B.
7. **L36 cuadrados:** orientación «hacia fuera» del triángulo; con catetos muy desiguales algún cuadrado puede rozar el borde del viewBox.
8. **L36 cateto:** exige c > b; si no, mensaje de error didáctico.
9. **L36 ¿es rectángulo?:** tolerancia |a²+b²−c²| < 0,05 (controles con paso 0,1).
10. **Preview estática** del estado `?preview=1` (L34 k=2 3-4-5; L35 Tales t=0,35/0,72; L36 3-4-5 con cuadrados).
11. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l34-semejanza-escalas.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l35-tales-semejanza.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l36-pitagoras.html"
```

---

## Veredicto

**OK para bloque 34–36.** Interactivos visibles y correctos; glosarios con a/b/c/k, catetos/hipotenusa y ∥/AA; visuals de triángulos semejantes / Tales con paralelas / cuadrados pitagóricos alineados al concepto (barra L01); controles independientes; notas históricas honestas; previews alineados con la UI; sync en ambos árboles.
