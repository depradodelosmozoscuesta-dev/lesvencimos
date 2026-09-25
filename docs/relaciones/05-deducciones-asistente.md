# Deducciones para el futuro asistente personal

Contexto: asistente offline = corazón; módulos = opcionales; privacidad en el aparato.  
**No mezclar** con Ruleta/patente ni red ciudadana/juego (fuera de alcance).

---

## Modos sugeridos (núcleo)

| Modo | Módulos que enciende | Datos locales que lee |
|---|---|---|
| **Hogar** | Hogar, Economía (compra/menú), Clima, Jardín (opcional), Moda lavado | `lv-hogar-*`, lista compra unificada, hábitos energía |
| **Salud** | Medicación (fuente), Salud (vista), Primeros auxilios (emergencia), Gimnasio/Meditación (opcional) | medicinas Hoy; no diagnosticar |
| **Agenda** | *(hueco: no hay módulo)* — nacer en núcleo | eventos propios del asistente; deep-link Listas Hogar / Prioridades Economía |
| **Resiliencia** | Apagón, Supervivencia, Campo, Electricidad, Radio, Mapas | checklists; 112 siempre visible |
| **Casa legal/€** | Economía, Legal-casa, Hogar mantén. | presupuesto, patrimonio, avisos derrama |
| **Cultura** | Biblioteca, Guitarra, Tinta×2, Guías, Informática | progreso lecciones Informática; no mezclar con Profesor cole |

## Reglas de diseño

1. El asistente **no copia** el HTML del módulo: deep-link + resumen de 1–2 datos.
2. Una sola fuente de verdad por dominio (compra; medicación).
3. Tonos: educativo / prudente / 112 — nunca consejo médico/legal/fiscal vinculante.
4. Packs pesados: el asistente detecta «módulo no instalado» → CTA Añadir módulo / ZIP.
5. Cuba: no sugerir Alarma/Central en home; Informática puede mencionar Central como lección.
6. Perfiles especiales (`asistente-alzheimer.html`, `asistente-negocios.html`) viven aparte; este mapa es el asistente general doméstico.

## Señales situacionales (ejemplos)

- Sin luz / usuario dice apagón → modo Resiliencia (Apagón primero).
- Ola calor → Clima + Economía luz + Hogar nevera.
- «Lista de la compra» → lista unificada.
- «Pastilla» → Medicación Hoy.
- «Viaje a Salamanca» → Guías + Mapas pack.
- «Ruido vecino» → Legal convivencia (divulgativo).

*Fin deducciones.*
