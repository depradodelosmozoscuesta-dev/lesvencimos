# Puentes útiles — para un asistente futuro

Fecha: 26 sep 2026 · Europe/Madrid (UTC+2)  
Un **puente** = cruce que el asistente puede sugerir sin mezclar dueños de datos.

---

## Clúster Hogar ↔ Economía ↔ Clima

| Situación del usuario | Puente | Qué abrir | Qué no mezclar |
|----------------------|--------|-----------|----------------|
| «Se me acaba la comida / voy a comprar» | Lista compartida | Hogar `super` **o** Economía `compra` (misma `lv-lista-compra-v1`) | No crear segunda lista |
| «Quiero gastar menos en súper» | Tips + lista | Economía `compra` (trucos) + Hogar nevera/recetas para aprovechar | No mover trucos a Hogar |
| «Pagar menos luz sin pasar frío» | Confort → dinero | Clima (`calefaccion`/`frio`) luego Economía `luz` | No meter CO/moho en Eco |
| «Huele a humedad / mancha negra» | Causa vs limpieza | Clima `humedad`/`moho` → si leve, Hogar Casa manchas/olores | Si extenso → profesional / 112 |
| «Menú barato 15 días» | Plan → cocina | Economía `menu` → Hogar `recetas`/`nevera` | Menú no sustituye nevera |
| «Valorar piso + IBI/basura Va» | Patrimonio + legal | Economía `patrimonio` + Legal-casa bloque E | Legal no es tasador |

## Clúster Salud ↔ Medicación

| Situación | Puente | Abrir |
|-----------|--------|-------|
| «¿A qué hora la pastilla?» | Checklist | Medicación (simple) o Salud Pastillas (misma `lv-medicacion-v1`) |
| «Teléfono del centro de salud» | Agenda | Solo Salud `medicos` |
| «Guardar analítica» | Docs | Solo Salud `informes` |
| «Se fue la luz y tengo nevera de insulina» | Crisis | Apagón (nevera/meds) + Medicación (qué tomar) — sin consejo clínico |

## Clúster Hogar Lavado ↔ Moda

| Situación | Puente | Abrir |
|-----------|--------|-------|
| «¿Cómo lavo esta camisa?» | Procedimiento | Hogar `lavado` |
| «¿Qué dice el símbolo del triángulo?» | Etiqueta | Moda `simbolos` |
| «Mancha de vino en la blusa» | Mancha prenda | Hogar Casa `manchas` (vino tinto) + Moda `manchas` si pide criterio de prenda cara/tintorería |
| «Combinar look + plancha» | Estilo → plancha | Moda `combinar`/`probador` → Hogar plancha si arrugas |

## Resiliencia / vida práctica

| Situación | Cadena de puentes |
|-----------|-------------------|
| Se va la luz | Apagón → Electricidad «se va la luz» → Radio (si hay red) → Supervivencia mochila |
| Quiero aprender enchufe | Electricidad (no Hogar mantén) |
| Outdoor fin de semana | Campo (no Supervivencia casa) |
| Planta tóxica y perro | Jardín ficha → Mascotas urgencias |
| Viaje Castilla y León | Guías-viaje (piloto) + Mapas pack Valladolid |

## Puentes de bienestar (sin solapar datos)

- Gimnasio ↔ Meditación: cuerpo / mente; sin LS compartido.
- Primeros auxilios ↔ Salud: urgencia educativa vs agenda personal.
- Tinta escritura ↔ Meditación cuaderno: creativo vs práctica; no unificar.

## Reglas para el asistente

1. Si hay **clave canónica compartida**, ofrecer el módulo según UI deseada (simple vs rica), no duplicar el dato.
2. Si hay **solape de contenido** (lavado/moda, clima/luz), enlazar al dueño de frontera (`plan-fronteras.md`).
3. Nunca inventar módulos anunciados en LEEME-vida (fontanería/gas/pintura) como si existieran.
4. Cuba: respetar `_aparte-cuba.md` (fuera del Escritorio home).

*Fin puentes*
