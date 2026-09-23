# QA bloque L25–L27 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)
**Ruta primaria (interactivos):** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`
**Sync:** mismos HTML/PNG/md copiados a `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`
*(Ambos árboles existen. El usuario escribió «lescircimos» dos veces; el espejo real es lesvencimos.)*

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `25.md` | Lección + glosario + interactivo (porcentajes) | ~6.3 KB |
| `26.md` | Lección tickets/ofertas/presupuesto + [E] + interactivo | ~7.3 KB |
| `27.md` | Lección calidad-precio / valor + [E] + interactivo | ~7.4 KB |
| `l25-porcentajes-descuentos.html` | Interactivo offline (file://) | ~24 KB |
| `l25-porcentajes-descuentos-preview.png` | Preview Chrome headless | ~276 KB |
| `l26-ticket-ofertas.html` | Interactivo offline | ~26 KB |
| `l26-ticket-ofertas-preview.png` | Preview (ticket térmico) | ~315 KB |
| `l27-calidad-precio.html` | Interactivo offline | ~26 KB |
| `l27-calidad-precio-preview.png` | Preview (estantería €/kg) | ~292 KB |
| `_qa-bloque-25-27.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://` (sin red) para L25, L26, L27.
- [x] Preview L25 inspeccionado: modo **Descuento**; sudadera 80 € −25 % → etiqueta Valladolid con badge −25 %, tachado 80 €, final **60,00 €**, pizarra ×0,75, ahorro 20 €; glosario `%` «por ciento».
- [x] Preview L26 inspeccionado: ticket **SUPER MERINO · Segovia** con 3 líneas (pan, leche, manzanas); total **5,80 €**; cambio de 10 € = **4,20 €**; unitario manzanas 1,80 €/kg; momento [E] visible.
- [x] Preview L27 inspeccionado: estantería arroz A 1,80 €/1 kg vs B 2,40 €/1,5 kg → B gana con **1,60 €/kg** (badge MEJOR kg); mnemónico + momento [E].

### Matemáticas
- [x] L25: 25 % de 80 = 20; final dto = 60; aumento 4 % de 1000 = 1040 (modo); encadenados 50×0,8×0,9 = 36 ≠ 50×0,7 = 35.
- [x] L26: 1×1,20 + 2×0,95 + 1,5×1,80 = 5,80; cambio 4,20; packs 2,40/0,5 = 4,80 €/kg vs 3,30/0,75 = 4,40 €/kg; 2ª al 50 %: 20+10 = 30.
- [x] L27: 2,40/1,5 = 1,60 €/kg; 15/4 = 3,75 €/mes vs 36/18 = 2 €/mes; desperdicio 2,00/0,9 ≈ 2,22 > 2,20.

### Calidad Jorge (barra)
- [x] Glosario: L25 `%` «por ciento» / p% de N / base; L26 `€/kg` / 2×1 / 2ª al 50 % / «hasta −70 %»; L27 precio / calidad-precio / valor / €/mes — en HTML + md.
- [x] Visuales reales alineados: **etiqueta de rebajas** (L25), **ticket térmico** (L26), **dos productos en estantería €/kg** (L27).
- [x] Controles independientes (N, p, p₂; 3 líneas ticket; packs A/B; precios/meses A/B — no se reescalan juntos).
- [x] Mnemónicos visibles en los 3 interactivos.
- [x] Tono ~12 años; contextos CyL (Valladolid, Segovia, Burgos, Salamanca, Ávila, Pucela).
- [x] Socioafectivo ligero [E] en L26 (privacidad del dinero) y L27 (ataca el argumento, no a la persona).
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Sin inventar currículo: UD7 L25 / UD8 L26–L27 · Decreto 39/2022 A.5–A.6 + E.

### Markdown
- [x] `25.md` / `26.md` / `27.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lescircimos` y `lesvencimos`.

---

## Límites conocidos

1. **Rangos acotados:** L25 % hasta 200 / descuentos 0–100; L26 cantidades y precios libres pero ticket fijo a 3 líneas; L27 calidad/valor en escala 1–5.
2. **L26 IVA:** desglose ~10 % incluido es **modelo didáctico**, no un tipo real de un súper concreto.
3. **L26 «Hasta −70 %»:** muestra el caso *si* el artículo estuviera al −70 %, con aviso explícito de letra pequeña.
4. **L27 rúbrica valor:** suma orientativa (precio invertido + calidad + valor); no es un juicio objetivo — el callout lo dice.
5. **Preview estática** del estado elegido (L25 dto 80→60; L26 ticket 5,80; L27 arroz B 1,60 €/kg).
6. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.
7. **Coma vs punto:** inputs decimales aceptan ambos; la UI muestra coma española; `euro()` fija 2 decimales.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l25-porcentajes-descuentos.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l26-ticket-ofertas.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l27-calidad-precio.html"
```

---

## Veredicto

**OK para bloque 25–27.** Interactivos visibles y correctos, glosarios con `%` «por ciento», visuals de etiqueta de rebajas / ticket térmico / estantería €/kg alineados al concepto, toque [E] en 26–27, previews alineados con la UI, sync en ambos árboles.
