# QA bloque L10–L12 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta primaria:** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`  
**Sync:** mismos HTML/PNG/md copiados a `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `10.md` | Lección + enlace + glosario (currículo CyL UD3) | ~6 KB |
| `11.md` | Lección primos/factorización + enlace | ~5.5 KB |
| `12.md` | Lección mcd/mcm + enlace | ~5.8 KB |
| `l10-bloques-divisibilidad.html` | Interactivo offline (file://) | ~24 KB |
| `l10-bloques-divisibilidad-preview.png` | Preview Chrome headless | ~348 KB |
| `l11-criba-factorizacion.html` | Interactivo offline | ~23 KB |
| `l11-criba-factorizacion-preview.png` | Preview | ~384 KB |
| `l12-barras-mcd-mcm.html` | Interactivo offline | ~24 KB |
| `l12-barras-mcd-mcm-preview.png` | Preview | ~450 KB |
| `_qa-bloque-10-12.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://` (sin red) para L10, L11, L12.
- [x] Preview L10 inspeccionado: mesa de caramelos n=24 con 4 rectángulos (1×24, 2×12, 3×8, 4×6), lista de divisores, chips de criterios ÷2…÷10, tira de múltiplos de b=8, glosario visible.
- [x] Preview L11 inspeccionado: criba N=30 con pasos 2 y 3 aplicados (verdes/tachados), ladrillos de 84 = 2×2×3×7, árbol de divisiones, clasificación «Compuesto».
- [x] Preview L12 inspeccionado: a=18 b=24 → mcd=6 mcm=72, varillas segmentadas en g, timeline con marca común en 72, Venn de factores, problema de packs, relación 6×72=18×24.

### Matemáticas
- [x] Divisores de 24: 1,2,3,4,6,8,12,24 (script de comprobación).
- [x] Criterios: lógica de unidades / suma de cifras / últimas dos cifras / 2∧3 para el 6 (UI aplica al mismo n).
- [x] Factorización 84→[2,2,3,7], 60→[2,2,3,5], 100→[2,2,5,5]; 1 ni primo ni compuesto; 97 primo (botón ejemplo).
- [x] mcd(18,24)=6, mcm=72; mcd(20,28)=4, mcm=140; mcd(7,15)=1, mcm=105; relación mcd×mcm=a×b.
- [x] Criba: tachado desde 2p; parada cuando p²>N; el 1 permanece especial (gris).

### Calidad Jorge (barra)
- [x] Cada letra/símbolo de UI explicado en español (n,d,k,b,N,p,a,b,g,mcd,mcm,×,÷,=,aⁿ).
- [x] Glosario en cada HTML + glosario en cada `.md`.
- [x] Mnemónicos en las tres lecciones.
- [x] Controles independientes (sin reescalado cruzado n↔d, N↔n, a↔b) — buscado patrón de asignación cruzada: ninguno.
- [x] Escenas que **se parecen** al concepto: rectángulos de bloques; criba + ladrillos de colores; varillas solapadas + timeline + Venn de factores.
- [x] Criptograma/juego de letras: **omitido a propósito** (L07 ya lo tiene; no forzarlo en este bloque).
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Sin inventar currículo: títulos y saberes alineados a hub CyL UD3 / Decreto 39/2022 A.4.

### Markdown
- [x] `10.md` / `11.md` / `12.md` parchados con sección interactivo + glosario + mnemónico + checklist, conservando objetivos/práctica/soluciones del pack.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lesvencimos` y `lescircimos`.

---

## Límites conocidos

1. **Rangos acotados a propósito:** L10 n=4–60 (rectángulos legibles); L11 criba N=20–50 y factorización n=2–120; L12 a,b=4–48 (varillas y timeline visibles; mcm puede llegar a 48×47/g pero con tope 48 el mcm máximo es manejable).
2. **Criba pedagógica:** tacha desde 2p (no solo desde p²) para que se vean todos los múltiplos; al terminar p²>N declara primos el resto.
3. **Venn L12:** muestra factores «solo a / solo b» como *exceso de exponente* tras el centro común (no duplica el centro en los laterales). El caption explica mcd/mcm completos.
4. **Preview es captura estática:** el botón «Comprobar» de L10 aparece en estado idle en el PNG (esperado); la criba L11 se capturó tras 2 pasos automáticos al cargar.
5. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.
6. **Criterio del 11:** solo en el md como ampliación opcional; no hay chip en el HTML (no obligatorio en todos los centros).
7. **Euclides:** explicado en el md; el interactivo usa gcd por restos internamente y enfatiza varillas/factores (visuales del concepto).

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l10-bloques-divisibilidad.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l11-criba-factorizacion.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l12-barras-mcd-mcm.html"
```

---

## Veredicto

**OK para bloque 10–12.** Interactivos visibles y correctos, glosarios completos, visuals alineados al concepto (bloques / criba-ladrillos / varillas-Venn), previews alineados con la UI, sync en ambos árboles.
