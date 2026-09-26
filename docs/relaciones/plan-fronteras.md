# Plan de fronteras — dueños de datos (claves REALES)

Fecha: 26 sep 2026 · Europe/Madrid (UTC+2)  
Solo claves y tabs verificados en el HTML actual de `/workspace/lesvencimos/modulos/`.

---

## Principio

> Un concepto de dato → **una clave canónica**.  
> Varios UI pueden leer/escribir esa clave.  
> El contenido educativo tiene **un dueño**; los demás enlazan.

---

## 1. Clúster Hogar ↔ Economía ↔ Clima

### 1.1 Lista de la compra

| Campo | Valor |
|-------|-------|
| Clave canónica | `lv-lista-compra-v1` |
| Dueño dato | **compartido** Hogar + Economía |
| UI Hogar | tab `super` |
| UI Economía | tab `compra` (lista; trucos aparte) |
| Legado (solo migrate) | `lv-hogar-compra-v1`, `lv-economia-lista-v1` |
| Flag | `lv-lista-compra-migrated-v1` |
| Dueño trucos compra | Economía `lv-economia-compra-tips-v1` |
| Dueño menú 2 semanas | Economía (tab `menu`) |

### 1.2 Datos solo Hogar

| Clave | Tab / uso |
|-------|-----------|
| `lv-hogar-nevera-v1` | `nevera` |
| `lv-hogar-listas-v1` | `listas` (checklist diario/semanal/viaje/visita) |
| `lv-hogar-reloj-v1` | `reloj` |

Contenido sin LS (dueño Hogar): `recetas`, `fichas` (alimentos), `casa` (zonas/materiales/manchas/olores/orden), `lavado`, `manten`, `tips`.

### 1.3 Datos solo Economía

| Clave | Tab |
|-------|-----|
| `lv-economia-presupuesto-v1` | `presupuesto` |
| `lv-economia-gastos-v1` | `gastos` |
| `lv-economia-ahorro-v1` | `ahorro` |
| `lv-economia-suministros-v1` | `luz` (lecturas/plan) |
| `lv-economia-energia-habits-v1` | `luz` / hábitos energía |
| `lv-economia-habitos-v1` | `habitos` |
| `lv-economia-prioridades-v1` | `prioridades` |
| `lv-economia-millon-v1` | `millon` |
| `lv-economia-patrimonio-v1` | `patrimonio` |
| `lv-economia-asesor-v1` | `asesor` |
| `lv-economia-compra-tips-v1` | `compra` (checks trucos) |

### 1.4 Clima

| | |
|--|--|
| LS | **ninguna** |
| Dueño contenido | lecciones `bases`…`viviendas` (confort, humedad, moho, CO, aislamiento) |
| No dueño | factura, lista compra, DIY gas |

**Frontera Clima vs Economía `luz`:**  
- Clima → percepción térmica, ventilación, riesgos.  
- Economía → euros, suministros, hábitos medibles (`energia-habits`, `suministros`).

**Frontera Clima vs Hogar Casa:**  
- Clima → por qué hay moho/humedad.  
- Hogar → limpieza superficial de junta / olor a cerrado.

---

## 2. Clúster Salud ↔ Medicación

| Clave | Dueño | Notas |
|-------|-------|-------|
| `lv-medicacion-v1` | **canónica compartida** | Salud Pastillas + módulo Medicación |
| `lv-salud-meds-v1` | legacy Salud | solo origen de `migrateSaludMedsToMedicacion` |
| `lv-salud-meds-migrated-v1` | flag | |
| `lv-med-simple` | Medicación | preferencia UI |
| `lv-med-check-YYYY-MM-DD` | **canónico** (Medicación + Salud Hoy) | checklist día |
| `lv-salud-check-YYYY-MM-DD` | legacy Salud | solo origen migrate → `lv-med-check-*` (`lv-salud-checks-migrated-v1`) |
| `lv-salud-docs-v1` | Salud | |
| `lv-salud-reports-v1` | Salud | informes |
| `lv-salud-hist-v1` | Salud | historial |

Tabs Salud dueñas: `medicos`, `informes`, `historial`, `consejos`.  
Medicación dueña: modo sencillo / letras grandes.

---

## 3. Hogar Lavado ↔ Moda

Sin claves LS compartidas (Moda sin persistencia de inventario).

| Concepto | Dueño contenido | IDs evidencia |
|----------|-----------------|---------------|
| Procedimiento colada/secado/plancha casa | **Hogar** | tab `lavado` (20 fichas) |
| Manchas domésticas (tela + casa) | **Hogar** | Casa `manchas` + ficha lavado «Tratar manchas…» |
| Símbolos de etiquetas | **Moda** | `simbolos` |
| Criterio prenda / tintorería / elastano | **Moda** | `lavar`, `manchas`, `tejidos` |
| Estilo, combinar, costura, probador SVG | **Moda** | `combinar`, `probador`, `costura`, … |
| Armario orden temporada | **Hogar** | Casa `orden` «Armario de ropa: temporada» |

---

## 4. Otras fronteras con claves

| Módulo | Claves | Frontera |
|--------|--------|----------|
| Apagón | `lv-apagon-links` | no pisa Electricidad |
| Gimnasio | `lv-gym-figura`, `lv-gym-filtros` | no salud clínica |
| Meditación | `lv-medita-v2`, `lv-arbol-v1` | no terapia |
| Informática | avance en LS propio del HTML | ≠ Profesor escolar |

Módulos sin LS de usuario relevante para fronteras de datos: clima, moda, jardín, mascotas, legal-casa, bricolaje, campo, supervivencia, electricidad, radio, qr, calculadora, guías, primeros-auxilios, tinta-*, mapas núcleo.

---

## 5. Matriz rápida dueño

```
Lista compra .......... lv-lista-compra-v1 .......... Hogar super + Eco compra
Nevera / listas hogar . lv-hogar-* .................. Hogar
Dinero / energía € .... lv-economia-* ............... Economía
Confort / CO / moho ... (contenido) ................. Clima
Medicinas ............. lv-medicacion-v1 ............ Salud + Medicación
Agenda sanitaria ...... lv-salud-docs/reports/hist .. Salud
Colada procedimiento .. (contenido lavado) .......... Hogar
Etiquetas / estilo .... (contenido moda) ............ Moda
```

*Fin plan-fronteras*
