# QA bloque L37–L39 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta primaria (interactivos):** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`  
**Sync:** mismos HTML/PNG/md copiados a `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`  
*(El usuario escribió «lescircimos» dos veces; el espejo real es **lesvencimos**.)*

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `37.md` | Lección coordenadas + glosario abscisa/ordenada + interactivo | ~6.2 KB |
| `38.md` | Lección modelización + glosario + interactivo CyL | ~6.5 KB |
| `39.md` | Lección patrones + glosario aₙ + interactivo | ~6.0 KB |
| `l37-coordenadas-plano.html` | Interactivo offline (file://) | ~23 KB |
| `l37-coordenadas-plano-preview.png` | Preview Chrome headless · P(3,−2) cuadrante IV | ~176 KB |
| `l38-modelizacion-plano.html` | Interactivo offline | ~25 KB |
| `l38-modelizacion-plano-preview.png` | Preview calles ⊥ VA · 60-80 → atajo 100 | ~198 KB |
| `l39-patrones-regla.html` | Interactivo offline | ~24 KB |
| `l39-patrones-regla-preview.png` | Preview fósforos n=3 → 10 · aₙ=3n+1 | ~169 KB |
| `_qa-bloque-37-39.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://…?preview=1` (sin red) para L37, L38, L39.
- [x] Preview L37 inspeccionado: **Colocar un punto** P(3,−2); cuadrantes coloreados I–IV; mapa (fuente, banco, árbol, porterías, kiosco); abscisa/ordenada en leyenda y sliders; guías a los ejes; veredicto cuadrante IV.
- [x] Preview L38 inspeccionado: **Calles ⊥ (Valladolid)** E=60 · N=80; croquis Casa→Esquina→Cole; atajo √=100 m; ruido (tiendas/farolas); pasos 1–5; fórmulas en mapa.
- [x] Preview L39 inspeccionado: **Fósforos (cuadrados)** n=3 → 10 fósforos; regla 3n+1; fichas 4,7,10; check n=1→4 · n=2→7.

### Matemáticas
- [x] L37: (x,y) pareja ordenada; cuadrantes por signos; distancia √(Δx²+Δy²) y casos alineados |Δx|/|Δy|; simetría (x,y)→(−x,−y).
- [x] L38: rectángulo P=2(L+A), A=L·A; Pitágoras calles ⊥; aula rodapié P−1; patio L = L·A − r² (P=2(L+A)).
- [x] L39: aritmética aₙ=a₁+(n−1)d; fósforos 3n+1; L baldosas 2n−1; tabla n→aₙ con predicción.

### Calidad Jorge (barra L01)
- [x] **Dibujos = lo que nombran:** plano-mapa con hitos (L37); mini-mapas CyL con calles/huerto/aula/L (L38); fósforos y baldosas en L contables (L39) — no blobs.
- [x] **Controles independientes:** L37 x/y (y x₂/y₂); L38 L/A o E/N o L/A/r; L39 a₁/d/n (y k en tabla).
- [x] **Glosario en español primero:** abscisa/ordenada/(x,y)/cuadrantes; modelo/croquis/ruido/validar; n/aₙ/d — en HTML + md.
- [x] Mnemónicos visibles en los 3 interactivos.
- [x] Notas históricas / contexto **honestas**: Descartes + GPS ≠ plano escolar; mini-mapas CyL croquis (no planos oficiales); puente al álgebra / arte mudéjar.
- [x] Tono ~12 años; UD12 L37–L38 · UD13 L39.
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Sin inventar currículo: UD12/UD13 · Decreto 39/2022 C.2, C.3, D.1.

### Markdown
- [x] `37.md` / `38.md` / `39.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones/reto.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lescircimos` y `lesvencimos`.

---

## Límites conocidos

1. **L37 rango:** cuadrícula ±6; puntos fuera no se permiten por el slider.
2. **L37 mapa:** hitos fijos (fuente 4,3…); decorativos didácticos, no un plano real del recreo.
3. **L37 distancia:** muestra √ con 2 decimales; enteros exactos (3-4-5) salen limpios.
4. **L38 calles:** el atajo asume que existe un camino diagonal (el veredicto pregunta si lo hay).
5. **L38 patio L:** el recorte r se acota a r < L y r < A; perímetro del L = 2(L+A) (corte que añade y quita 2r).
6. **L38 aula:** puerta fija ≈ 1 m restado del rodapié (simplificación escolar).
7. **L39 fósforos:** cuadrados en fila compartiendo lados → 3n+1 (no 4n).
8. **L39 L baldosas:** muestra hasta 5 pasos a la vez aunque n=6.
9. **L39 tabla:** predicción k hasta 20; filas visibles ≤ 8.
10. **Preview estática** del estado `?preview=1` (L37 P(3,−2); L38 calles 60-80; L39 fósforos n=3).
11. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l37-coordenadas-plano.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l38-modelizacion-plano.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l39-patrones-regla.html"
```

---

## Veredicto

**OK para bloque 37–39.** Interactivos visibles y correctos; glosarios con abscisa/ordenada, modelo/croquis y n/aₙ/d; visuals de plano-mapa / mini-mapas CyL / fósforos-baldosas alineados al concepto (barra L01); controles independientes; previews alineados con la UI; sync en ambos árboles.
