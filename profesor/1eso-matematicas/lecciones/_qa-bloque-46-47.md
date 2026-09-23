# QA bloque L46–L47 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta primaria (interactivos):** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`  
**Sync:** mismos HTML/PNG/md copiados a `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`  
*(El usuario escribió «lescircimos» dos veces; el espejo real es **lesvencimos**.)*

**Cierre del track de calidad de las 47 lecciones.**

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `46.md` | Lección proyecto integrador + glosario + interactivo | ~7 KB |
| `47.md` | Lección portfolio/hábitos + glosario + socioafectivo + interactivo | ~7.5 KB |
| `l46-proyecto-patio.html` | Interactivo offline (file://) · mini-proyecto patio VA | ~26 KB |
| `l46-proyecto-patio-preview.png` | Preview Chrome · checkpoint 3 Área/P · L=35 A=20 | ~232 KB |
| `l47-portfolio-habitos.html` | Interactivo offline · portfolio + hábitos + logros | ~25 KB |
| `l47-portfolio-habitos-preview.png` | Preview · Mis logros · 6/8 evidencias · estrellas | ~210 KB |
| `_qa-bloque-46-47.md` | Este checklist | — |

**md5 sync lescircimos ↔ lesvencimos:** idénticos en los 6 artefactos + este QA.

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://…?preview=1` (sin red) para L46 y L47.
- [x] Preview L46 inspeccionado: patio IES Valladolid · pista de baloncesto (líneas + canastas) · árboles · valla · **Largo L=35 m · Ancho A=20 m** · fórmulas Área S=700 m² · Perímetro P=110 m · checkpoint 3 activo.
- [x] Preview L47 inspeccionado: carpeta portfolio con hojas · panel **Mis logros** (Números 3★, Medida 3★, Geometría 4★, Álgebra 2★, Actitud 3★) · badge 6/8 piezas · socioafectivo suave ON.

### Matemáticas / metacognición
- [x] L46: estimar → escala 1:n → área/perímetro → ecuación botes (C·n ≥ S, techo) → presupuesto valla con % dto. Integra A–D.
- [x] L47: checklist 8 evidencias · 6 hábitos · rúbrica 1–4 en 5 sentidos · 3 prompts de reflexión · localStorage opcional.

### Calidad Jorge (barra L01)
- [x] **Dibujos = lo que nombran:** patio con pista/valla/árboles/edificio (L46); carpeta con hojas + estrellas (L47) — no blobs.
- [x] **Controles independientes:** L46 Largo/Ancho/escala/cobertura/precio/%; L47 cada casilla/hábito/estrella aparte.
- [x] **Glosario en español primero:** Largo (L), Ancho (A), Área (S), Perímetro (P), Escala 1:n, Cobertura (C) · Portfolio, Evidencia, Autoevaluación, Metacognición, Hábito, Logro — en HTML + md.
- [x] Mnemónicos visibles en los 2 interactivos y en los 2.md.
- [x] Historia CyL: IES Valladolid (patio); cierre hacia 2º ESO / Decreto 39/2022 sentido E.
- [x] Tono ~12 años; UD15 L46–L47.
- [x] Single-file HTML, `file://`, sin red. Tema crema (#FAF7F0).
- [x] Sin inventar currículo: A–D integrados + E (metacognición / socioafectivo).
- [x] L47 socioafectivo **ligero**: evidencia concreta vs «se me dan mal» / «¿me miras el paso 2?» — no sermón.

### Markdown
- [x] `46.md` / `47.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones/reto.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lescircimos` y `lesvencimos`.

---

## Límites conocidos

1. **L46 patio:** croquis escolar tipado (no plano oficial del IES); pista simplificada (rectángulo + círculo + canastas).
2. **L46 estimar:** 3 opciones de banco (baja / justa / alta) ligadas a L·A actual.
3. **L46 escala:** conversión plano cm ↔ real m con 1:n; no imprime PDF a escala real.
4. **L46 botes:** redondeo hacia arriba; asume cobertura constante por bote.
5. **L46 presupuesto:** un solo tramo de valla = perímetro completo (sin puertas/restos).
6. **L47 portfolio:** 8 ítems fijos de ejemplo (no importa archivos del alumno).
7. **L47 localStorage:** solo en el mismo navegador/dispositivo; no sincroniza entre PCs.
8. **L47 estrellas:** autoevaluación subjetiva 1–4 (no calificación oficial).
9. **Preview estática** del estado `?preview=1` (L46 área 35×20; L47 logros con ejemplo del libro).
10. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l46-proyecto-patio.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l47-portfolio-habitos.html"
```

---

## Veredicto

**OK para bloque 46–47 (cierre de curso).** Interactivos de situación-problema (patio CyL multipaso) y de portfolio/hábitos/logros; glosarios con nombres en español primero; visuals alineados al concepto (barra L01); controles independientes; socioafectivo ligero en L47; previews alineados con la UI; sync en ambos árboles.

**Track de calidad 47/47 lecciones: cerrado.**
