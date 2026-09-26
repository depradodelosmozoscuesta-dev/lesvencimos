# Solapes entre módulos — evidencia actual

Fecha: 26 sep 2026 · Europe/Madrid (UTC+2)  
Criterio: se marca solape solo con **nombres de sección / claves LS / lecciones** presentes en el HTML de hoy, no por intuición.

---

## Top solapes (prioridad clúster)

### 1. Hogar `super` ↔ Economía `compra` — LISTA DE LA COMPRA (datos)

| | Hogar | Economía |
|--|-------|----------|
| Sección | tab `super` «Súper» | tab `compra` «Compra» |
| Clave canónica | `lv-lista-compra-v1` | `lv-lista-compra-v1` |
| Legado | `lv-hogar-compra-v1` | `lv-economia-lista-v1` |
| Flag | `lv-lista-compra-migrated-v1` | igual |

Ambos ejecutan `migrateListaCompra()` y fusionan legados → canónica.  
**Frontera:** un solo dato (la lista). Dueño de escritura: cualquiera de los dos UI, misma clave. Tips de trucos de compra (≥35) viven solo en Economía (`lv-economia-compra-tips-v1`). Menú 2 semanas = Economía. Nevera/alimentos/recetas = Hogar.

### 2. Salud `pastillas` ↔ Medicación — MEDICINAS (datos)

| | Salud | Medicación |
|--|-------|------------|
| UI | tab Pastillas (sección completa) | módulo simple + modo letras grandes |
| Canónica | escribe/lee `lv-medicacion-v1` | `lv-medicacion-v1` |
| Legacy | `lv-salud-meds-v1` + migrate → canónica | — |
| Checks día | `lv-salud-check-YYYY-MM-DD` | `lv-med-check-YYYY-MM-DD` |

**Frontera:** ficha medicina (nombre/dosis/horas) = canónica compartida. Médicos, informes, historial, consejos = solo Salud. UI simple / `lv-med-simple` = solo Medicación. Los checks diarios **aún no unificados** (dos prefijos).

### 3. Hogar `lavado` ↔ Moda `cuidado`/`lavar`/`manchas`/`plancha-guardar` — PROCEDIMIENTO ROPA

| Tema | Hogar Lavado (20 fichas) | Moda |
|------|--------------------------|------|
| Separar colores | «Separar colores y tejidos» | lección `lavar` |
| Manchas en ropa | fichas Casa→Manchas + «Tratar manchas antes…» | lección `manchas` (grasa, café/vino, sudor, sangre) |
| Plancha / vapor | 4+ fichas plancha/vapor/arrugas | `plancha-guardar` |
| Símbolos etiqueta | (no dedicado) | `simbolos` — **dueño claro Moda** |
| Estilo / silueta / costura | no | Moda exclusivo |

**Frontera:** procedimiento doméstico de colada/plancha → **Hogar**. Lectura de etiquetas, tejidos-con-estilo, cuándo tintorería, estética → **Moda**. Manchas de casa (encimera, juntas) → Hogar Casa; manchas de prenda con criterio moda → Moda puede enlazar a Hogar.

### 4. Clima ↔ Economía `luz` — ENERGÍA / CONFORT

| | Clima | Economía Luz y agua |
|--|-------|---------------------|
| Enfoque | confort, humedad, moho, CO, aislamiento práctico | factura, tips ahorro, calculadora, hábitos (`lv-economia-energia-habits-v1`, `…-suministros-v1`) |
| Termostato / calefacción | lecciones `calefaccion`, `frio`, `calor` | mención ahorro en tab `luz` |
| Humedad / moho / CO | lecciones propias | casi ausente |

**Frontera:** *cómo vivir con confort y seguridad* → Clima. *cuánto cuesta / cómo medir y ahorrar* → Economía. No duplicar guías de moho/CO en Economía.

### 5. Apagón ↔ Electricidad ↔ Supervivencia — CORTE DE SUMINISTRO

| Módulo | Sección relevante |
|--------|-------------------|
| Apagón | «Se fue la luz ahora», nevera, pilas, vecinos, preparar |
| Electricidad | lección «Cuando se va la luz» (+ enchufes/clavijas DIY) |
| Supervivencia | Agua, botiquín, comunicación, frío/calor, mochila |

**Frontera:** procedimiento inmediato corte → Apagón. DIY eléctrico seguro → Electricidad. Resiliencia civil stock/plan → Supervivencia. Apagón ya declara enlace ligero a Electricidad.

---

## Otros solapes menores (con frontera)

| A | B | Qué se pisa | Frontera |
|---|---|-------------|----------|
| Hogar `manten` | Bricolaje / Electricidad | bisagras, tiradores vs taladro/enchufe | Mantén = usuario ligero; Bricolaje = aprender DIY; Electricidad = solo eléctrico con SVG |
| Hogar Casa `olores`/`manchas` moho | Clima `moho`/`humedad` | moho superficial vs diagnóstico confort | Hogar = limpiar junta leve; Clima = causa, ventilación, cuándo profesional |
| Economía `menu` | Hogar `recetas`/`nevera` | planificar comidas vs cocinar | Menú económico → Eco; ejecutar plato/nevera → Hogar |
| Legal-casa impuestos vivienda | Economía `patrimonio` vivienda | valor/tributos | Legal = normas/cifras Va 2026; Eco = inventario patrimonial orientativo |
| Primeros auxilios | Salud / Medicación | salud general | PA = RCP/urgencia educativa; Salud = agenda personal |
| Campo | Supervivencia | agua/fuego | Campo = outdoor; Supervivencia = casa |
| Jardín toxicidad mascotas | Mascotas | aviso breve | Jardín = planta; Mascotas = convivencia/vet |
| Informática Central Cuba | `_aparte-cuba` | Cuba | Aparte = alarma/central packs; Informática = lección cultural |
| Guías viaje | Mapas | España | Guías = texto turismo piloto; Mapas = GPS + tiles packs |
| Gimnasio | Salud | cuerpo | Gym ≠ consejo médico (aviso explícito) |
| Radio | Apagón | info en corte | Radio lista emisoras; Apagón recomienda radio |

---

## Qué NO es solape de datos

- Aliases HTML idénticos (biblioteca/biblio, etc.) → keep ambos nombres.
- Biblioteca libros JSON vs Informática lecciones → dominios distintos.
- LEEME-vida anuncios futuros (fontanería…) → huecos, no solapes.

*Fin solapes*
