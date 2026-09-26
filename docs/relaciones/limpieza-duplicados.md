# Limpieza de duplicados — keep / merge / cut

Fecha: 26 sep 2026 · Europe/Madrid (UTC+2)  
Reglas: **aliases OK**; **datos duplicados NO**; Hogar hub se limpia por fronteras; Moda↔Lavado es **parcial**.

---

## Aliases — KEEP

| Acción | Par | Motivo |
|--------|-----|--------|
| KEEP | `biblioteca.html` ↔ `biblio.html` | idénticos MD5 |
| KEEP | `caja-fuerte.html` ↔ `caja.html` | idénticos |
| KEEP | `guitarra.html` ↔ `guitar.html` | idénticos |
| KEEP | `gimnasio.html` ↔ `gym.html` | idénticos |
| KEEP | `meditacion.html` ↔ `medita.html` | idénticos (Android corto) |

No borrar aliases: Android/rutas cortas los usan (LEEME meditacion lo dice).

---

## Datos — MERGE ya hecho / vigilar

### Lista compra (P1 doc)
| Acción | Detalle |
|--------|---------|
| KEEP canónica | `lv-lista-compra-v1` |
| MERGE runtime | `migrateListaCompra()` en Hogar y Economía ya fusiona `lv-hogar-compra-v1` + `lv-economia-lista-v1` |
| CUT en docs | **Hecho (P1.1 docs):** LEEME-hogar + HOGAR-INDICE + LEEME-economia → `lv-lista-compra-v1` |
| KEEP legado solo lectura | Las claves viejas pueden quedar para migración one-shot |

### Medicinas (P1 código/doc)
| Acción | Detalle |
|--------|---------|
| KEEP canónica | `lv-medicacion-v1` |
| MERGE | `migrateSaludMedsToMedicacion()` desde `lv-salud-meds-v1` |
| CUT escritura | Salud no debe volver a persistir medicinas en `lv-salud-meds-v1` (solo migrate) — verificar en futuros edits |
| MERGE checks | **Hecho (P1.3):** canónico `lv-med-check-*`; migrate one-shot desde `lv-salud-check-*` (`lv-salud-checks-migrated-v1`) |

---

## Contenido — CUT / SLIM parcial

### Hogar hub (P1)
| Acción | Qué |
|--------|-----|
| KEEP hub | Inicio + Casa + Lavado + Mantén + cocina |
| CUT tentación | No reintroducir tips de factura luz/agua (dueño Economía `luz`) |
| CUT tentación | No expandir DIY gas/cuadro eléctrico (límites ya en HOGAR-INDICE) |
| KEEP enlace | Mantén «cuándo llamar profesional» → puente Electricidad/Bricolaje/Clima |

### Moda ↔ Hogar Lavado (P1 parcial)
| Acción | Dueño | Qué hacer |
|--------|-------|-----------|
| KEEP | Hogar | 20 fichas procedimiento colada/plancha/secado |
| KEEP | Moda | `simbolos`, estilos, combinar, costura, probador |
| SLIM | Moda `lavar` / `plancha-guardar` / `manchas` | Acortar pasos genéricos que copian Hogar; dejar criterio moda (tintorería, elastano, prenda cara) + enlace conceptual a Hogar Lavado |
| KEEP overlap mínimo | Manchas | OK si Moda remite «pasos caseros» y Hogar tiene ficha detallada |

### Clima ↔ Economía luz
| Acción | Detalle |
|--------|---------|
| KEEP | Clima = confort/seguridad; Eco = €/hábitos |
| CUT | Evitar en Economía lecciones de moho/CO/ventilación |
| CUT | Evitar en Clima calculadoras de factura / kWh |

### Apagón ↔ Electricidad
| Acción | Detalle |
|--------|---------|
| KEEP ambos | scopes distintos |
| KEEP | Enlace ligero ya declarado en LEEME-apagon |
| CUT | No duplicar SVG de enchufes dentro de Apagón |

---

## No tocar (falsos duplicados)

- Jardín «supervivencia germinados» ≠ Campo outdoor ≠ Supervivencia casa.
- Primeros auxilios ≠ Salud agenda.
- Informática Cuba ≠ packs `_aparte-cuba`.
- Biblioteca 4.2M ≠ Tinta escritura.

---

## Checklist limpiezas P1

1. **Docs claves compra:** **hecho** — LEEME-hogar + HOGAR-INDICE + LEEME-economia → `lv-lista-compra-v1`.
2. **Moda ↔ Hogar Lavado:** frontera + CTAs ligeras (P1.2); SLIM de lecciones Moda sigue parcial.
3. **Checks medicación:** **hecho** — canónico `lv-med-check-*` + migrate desde `lv-salud-check-*`.

*Fin limpieza*
