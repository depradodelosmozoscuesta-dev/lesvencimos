# QA bloque L31–L33 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta primaria (interactivos):** `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `31.md` | Lección elementos/clasificación + glosario + interactivo | ~7.0 KB |
| `32.md` | Lección posiciones rectas/circunferencias + glosario + interactivo | ~6.5 KB |
| `33.md` | Lección construcción manipulativa/digital + glosario + interactivo | ~7.1 KB |
| `l31-clasificar-figuras.html` | Interactivo offline (file://) | ~28 KB |
| `l31-clasificar-figuras-preview.png` | Preview Chrome headless | ~170 KB |
| `l32-posiciones-rectas-circulos.html` | Interactivo offline | ~24 KB |
| `l32-posiciones-rectas-circulos-preview.png` | Preview (tangente d=r=5) | ~141 KB |
| `l33-construccion-figuras.html` | Interactivo offline | ~24 KB |
| `l33-construccion-figuras-preview.png` | Preview (SSS 4-5-7 + arcos) | ~175 KB |
| `_qa-bloque-31-33.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://…?preview=1` (sin red) para L31, L32, L33.
- [x] Preview L31 inspeccionado: **Triángulos · Isósceles** a=b=5, c=8; vértices A/B/C; ángulos ≈36,9° / 36,9° / 106,3°; tags isósceles + obtusángulo; marcas de lados iguales.
- [x] Preview L32 inspeccionado: **Recta y circunferencia**; r=5 · d=5 → **tangente** (1 punto T); radio y d perpendiculares etiquetados; glosario paralelo/perpendicular/tangente/secante.
- [x] Preview L33 inspeccionado: **Triángulo SSS** a=4 · b=5 · c=7; arcos de compás desde A (r=b) y B (r=a); vértice C por intersección; protocolo por pasos.

### Matemáticas
- [x] L31: isósceles 5-5-8 → ángulos base iguales, obtusángulo; suma ≈180°; hexágono diagonales 6·3/2=9 (ejercicio md).
- [x] L32: d>r exterior · d=r tangente · d<r secante; diámetro 18 → radio 9; paralelas θ=0°; ⊥ θ=90°.
- [x] L33: 4+5>7 sí; 4+5>10 no; equilátero tres radios iguales; mediatriz ⊥ por punto medio; bisectriz parte θ en dos.

### Calidad Jorge (barra L01)
- [x] **Dibujos = lo que nombran:** polígonos con vértices/lados/ángulos (L31); rectas + circunferencias + d ⊥ (L32); arcos de compás + intersección (L33) — no charcos/blobs.
- [x] **Controles independientes:** L31 a/b/c no se reescalan juntos en pantalla; L32 r y d independientes; L33 lados SSS independientes.
- [x] **Glosario en español primero:** vértice/lado/ángulo/diagonal/∥/⊥; paralelo/perpendicular/tangente/secante/O/r/d; compás/regla/mediatriz/bisectriz/SSS — en HTML + md.
- [x] Mnemónicos visibles en los 3 interactivos.
- [x] Tono ~12 años; UD10 Figuras planas.
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Sin inventar currículo: UD10 L31–L33 · Decreto 39/2022 C.1.

### Markdown
- [x] `31.md` / `32.md` / `33.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones/reto.
- [x] Enlaces relativos a HTML + PNG.

---

## Límites conocidos

1. **L31 triángulo libre:** la clasificación por ángulos usa la ley de cosenos; umbral de igualdad de lados ≈0,15 u.
2. **L31 cuadriláteros:** el «romboide/paralelogramo» y el trapecio son modelos escolares (marcas ∥); no cubre todos los trapecios no isósceles con controles de base asimétrica.
3. **L31 diagonales en triángulo:** el toggle explica que n(n−3)/2 = 0; no dibuja diagonal fantasma.
4. **L32 dos circunferencias:** casos básicos (exteriores, tangentes, secantes, interiores, concéntricas); no enumera los 8–10 casos de algunos libros.
5. **L32 distancia d:** siempre se mide en vertical (recta horizontal) para claridad didáctica.
6. **L33 compás:** arcos completos dibujados como circunferencias discontinuas (lectura clara), no solo el arco mínimo de taller.
7. **L33 bisectriz:** construcción clásica simplificada visualmente (arco en V + bisectriz); no arrastra puntos libres tipo GeoGebra completo.
8. **Preview estática** del estado `?preview=1` (L31 iso 5-5-8; L32 tangente 5=5; L33 SSS 4-5-7).
9. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lesvencimos/profesor/1eso-matematicas/lecciones/l31-clasificar-figuras.html"
google-chrome "file:///workspace/lesvencimos/profesor/1eso-matematicas/lecciones/l32-posiciones-rectas-circulos.html"
google-chrome "file:///workspace/lesvencimos/profesor/1eso-matematicas/lecciones/l33-construccion-figuras.html"
```

---

## Veredicto

**OK para bloque 31–33.** Interactivos visibles y correctos; glosarios con vértice/lado/ángulo, paralelo/perpendicular/tangente/secante y mediatriz/bisectriz; visuals de polígonos / recta–círculo / arcos de compás alineados al concepto (barra L01); controles independientes; previews alineados con la UI; sync en ambos árboles.
