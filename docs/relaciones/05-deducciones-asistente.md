# 05 — Deducciones del asistente (modos)

Fecha: 26 sep 2026 · Europe/Madrid (UTC+2)  
Cómo debe razonar un asistente futuro sobre este catálogo **sin** inventar módulos ni duplicar datos.

---

## Modos de asistencia

### Modo A — Enrutado (router)
Entrada: frase del usuario. Salida: 1 módulo + tab/lección sugerida + aviso de frontera.

Ejemplos:
- «lista de la compra» → Hogar `super` *o* Economía `compra` (misma clave).
- «símbolo de lavado» → Moda `simbolos`.
- «se fue la luz» → Apagón primero; Electricidad si pregunta por el cuadro/enchufe.
- «pastilla de las 8» → Medicación (simple) / Salud Pastillas.

### Modo B — Puente (bridge)
Cuando la necesidad cruza dos dueños: ofrecer **secuencia**, no fusión.

Ejemplo: «pasar menos frío gastando menos» → Clima `calefaccion`/`frio` **luego** Economía `luz`.

### Modo C — Dueño de dato (data-owner)
Antes de proponer «guardar», consultar `plan-fronteras.md`:
- ¿Existe clave canónica? usarla.
- ¿Legacy? no escribir; solo migrate.
- ¿Checks duales meds? preferir la clave del módulo cuya UI está abierta; no crear tercera.

### Modo D — Hueco consciente (gap)
Si piden fontanería / gas DIY / pintura / CCAA de guías no escritas:
- Decir que **no hay módulo** (o es piloto).
- Ofrecer el satélite más cercano (Hogar `manten`, Clima riesgos, Guías ciudades existentes).
- No improvisar temario largo.

### Modo E — Seguridad (safety)
Forzar freno en: gas, cuadro eléctrico, plagas/moho extenso, medicación clínica, veterinaria, legal personal.
Texto tipo: «Esto no sustituye a profesional · 112 en emergencia».

### Modo F — Densidad (depth)
Elegir módulo según profundidad pedida:
- Denso (Hogar/Eco/Jardín/Gym…) para «enséñame a fondo».
- Fino (Apagón/Campo…) para checklist corta.
- Esqueleto (Guías piloto, Calculadora) — no prometer más de lo que hay.

---

## Heurísticas rápidas

| Señal en el mensaje | Preferir |
|---------------------|----------|
| €, factura, ahorro, millón, patrimonio | Economía |
| nevera, receta, fregar, colada, mancha sofá | Hogar |
| humedad, CO, termostato confort, moho pared | Clima |
| look, etiqueta lavado, costura, silueta | Moda |
| dosis, horario pastilla | Medicación / Salud pastillas |
| médico, analítica, historial | Salud |
| RCP, atragantamiento | Primeros auxilios |
| enchufe, clavija | Electricidad |
| corte luz ahora | Apagón |
| mochila casa, botiquín stock | Supervivencia |
| monte, fuego outdoor | Campo |

## Anti-patrones

1. Crear segunda lista de compra «para economía».
2. Copiar guía de moho dentro de Economía.
3. Tratar aliases como módulos distintos.
4. Incluir Cuba en Escritorio home (aparte).
5. Hablar de Ruleta/patente (fuera de alcance Relaciones).

*Fin deducciones*
