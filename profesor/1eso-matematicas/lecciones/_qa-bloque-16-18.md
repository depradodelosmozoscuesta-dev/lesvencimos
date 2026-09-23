# QA bloque L16–L18 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta primaria (interactivos):** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`  
**Sync:** mismos HTML/PNG/md copiados a `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`  
*(Ambos árboles existen.)*

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `16.md` | Lección + glosario + interactivo (CyL UD5 significado/equivalencia/simplificar) | ~6.5 KB |
| `17.md` | Lección comparación + recta + interactivo | ~6.5 KB |
| `18.md` | Lección suma/resta + interactivo | ~6.1 KB |
| `l16-fracciones-pizza.html` | Interactivo offline (file://) | ~23 KB |
| `l16-fracciones-pizza-preview.png` | Preview Chrome headless | ~327 KB |
| `l17-fracciones-recta.html` | Interactivo offline | ~22 KB |
| `l17-fracciones-recta-preview.png` | Preview | ~214 KB |
| `l18-fracciones-suma.html` | Interactivo offline | ~21 KB |
| `l18-fracciones-suma-preview.png` | Preview | ~243 KB |
| `_qa-bloque-16-18.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://` (sin red) para L16, L17, L18.
- [x] Preview L16 inspeccionado: pizza 2/4 (2 trozos rojos / 2 amarillos), presets, amplificar k, simplificar → 1/2, vistas Pizza/Barra/Rectángulo/Equivalentes, panel música negra/corchea, mnemónico visible.
- [x] Preview L17 inspeccionado: 2/5 < 1/2, recta 0…1 con anclas 0·1/2·1, barras+pizzas A/B, mcm=10 → 4/10 vs 5/10.
- [x] Preview L18 inspeccionado: 1/4+1/6=5/12, pasos barras original→mcm 12→resultado 5/12, mnemónico del denominador.

### Matemáticas
- [x] Equivalencia: 2/4 = 1/2; amplificar ×k deja mismo valor; mcd(2,4)=2.
- [x] Comparación: 2/5 < 1/2; 3/7 < 5/7 (igual den.); 3/8 < 3/5 (igual num.); 3/4 < 5/6 (mcm 12).
- [x] Suma: 1/4+1/6 → mcm 12 → 3/12+2/12=5/12. Resta igual den.: 5/8−2/8=3/8. 1−3/5=2/5.
- [x] Error típico bloqueado en copy: 1/2+1/3 ≠ 2/5.

### Calidad Jorge (barra)
- [x] Glosario numerador/denominador/barra/`=`/`≠`/`<`/`>`/`+`/`−`/mcd/mcm en español (HTML + md).
- [x] Visuales tipo fracción: pizza con crust+pepperoni, barras de longitud fija, rectángulo partido, recta 0–1(+).
- [x] Controles independientes (a↔b, a/b↔c/d, k no reescala UI ajena).
- [x] Mnemónicos: L16 «mismo tamaño, más trozos…»; L17 mismo numerador; L18 no sumar denominador.
- [x] Panel música L16 (negra=1, corchea=1/2) — un panel corto, natural y claro.
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Sin inventar currículo: títulos/saberes alineados a hub CyL UD5 / Decreto 39/2022 A.2–A.3.

### Markdown
- [x] `16.md` / `17.md` / `18.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lescircimos` y `lesvencimos`.

---

## Límites conocidos

1. **Rangos acotados:** L16 a=0…24, b=1…16, k=1…6; L17 a,c=0…20 y b,d=1…12; L18 igual + resta negativa avisada (no modelamos negativos aquí).
2. **Barras L18 con mcm grande:** si mcm>36 la barra es esquemática (celdas proporcionales).
3. **Pizza impropia:** sombrea como máximo un todo y avisa «+N trozos de otra pizza».
4. **Preview estática** del estado inicial (L16 pizza 2/4; L17 2/5 vs 1/2; L18 1/4+1/6).
5. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.
6. **Música L16:** panel conceptual (sin audio); no es un editor de partituras.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l16-fracciones-pizza.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l17-fracciones-recta.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l18-fracciones-suma.html"
```

---

## Veredicto

**OK para bloque 16–18.** Interactivos visibles y correctos, glosarios completos, visuals de pizza/barra/recta alineados al concepto, panel música breve en L16, previews alineados con la UI, sync en ambos árboles.
