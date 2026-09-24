# Informe revisor final — EPVA 1º ESO · lote L01–L10

**Fecha:** 2026-09-24 (Europe/Madrid)  
**Ámbito:** pasada de **lote publicable** (coherencia L01–10, decreto del tramo, glosas, relleno, decisión B en L10). No re-QA píxel a píxel (Revisor ESO ya OK lección a lección).  
**Base:** `/workspace/lesvencimos/profesor/1eso-plastica-visual/`  
**Entrada:** Revisor ESO + Jorge — prioridad cerrar Mate + Plástica; empezar por Plástica L01–10.

---

## 1. Resumen ejecutivo

**¿OK lote L01–L10 / publicable?** **SÍ.**

- 0 críticos de lote.
- Hub `1eso-plastica-visual.html` enlaza L01–10.
- Cobertura del tramo: viñetas **A1–A4** y **B1–B5** (B3 repartida L07–09; B4 = L10). Coherente con `COBERTURA-DECRETO.md` / `TEMARIO.md`.
- L06–L10: práctica Tinta + ruta `../../../modulos/tinta-estudio.html` (resuelve a `modulos/tinta-estudio.html`).
- **L10 cumple decisión Revisor ESO B:** perspectiva como concepto 1–2 fugas; sin cónica/oblicua; profundidad por tamaño / solape / sombra.
- Glosas alineadas en el muestreo (género/estilo; solape L07→L10; luz/sombra).
- Sin relleno tipo «curiosidad / vida real» decorativa (0 hits en md L01–10).
- Quizzes: respuesta correcta repartida (A/B/C/D), no sesgo a la 1.ª.

**Alcance explícito:** esto **no** es sello del curso EPVA completo (31 lecciones). Quedan fuera B6–B7 y bloques C–D (L11–31). No se tratan como hueco del lote L01–10.

---

## 2. Hallazgos

### Críticos

Ninguno.

### Importantes

| ID | Hallazgo | Evidencia / acción |
|---|---|---|
| I1 | Lecciones md muy cortas (~220–330 palabras L01–05) | Revisor ESO ya OK lección a lección. No bloquea lote; valorar en L11+ si el ritmo corto se mantiene sin práctica Tinta. |
| I2 | DUDA-2 y DUDA-3 abiertas en `COBERTURA-DECRETO.md` | A4 wording exacto; grafía «grafico-plásticas». No bloquean publicar L01–10; prompts abajo. |

### Menores

| ID | Hallazgo | Evidencia |
|---|---|---|
| M1 | Alias `leccion-NN.html` = redirect al shell largo | Funciona (p. ej. L10). Ruido de mantenimiento. |
| M2 | NORMAS.md cita path de ejemplo distinto al canónico real | Canónico real: `profesor/1eso-plastica-visual/`. Cosmético. |
| M3 | L01–05 sin widget Tinta | Acorde a temario (Tinta desde L06). OK. |

### No hallados

- Rotura de rutas Tinta / shells / hub.
- Perspectiva cónica o tipologías de 3º coladas en L10.
- Repetición absurda L04 (geometría en patrimonio) vs L07 (forma como elemento visual): roles distintos.
- Glosa contradictoria solape / profundidad entre L07 y L10.
- Relleno sistemático.

---

## 3. Decreto (alcance L01–10)

| Viñeta | Lección | ¿Cubierta en lote? |
|---|---|---|
| A1–A4 | L01–L04 | Sí |
| B1 | L05 | Sí |
| B2 | L06 | Sí |
| B3 | L07–L09 | Sí |
| B5 | L07 | Sí |
| B4 | L10 | Sí (+ apartado perspectiva concepto, decisión B) |
| B6–B7, C*, D* | L11–31 | **Fuera de alcance** del lote |

---

## 4. L10 — checklist decisión B

| Criterio | ¿OK? |
|---|---|
| Perspectiva = concepto (representar profundidad en un plano) | Sí |
| Idea 1–2 puntos de fuga, sin trazado | Sí |
| Sin cónica / oblicua / proyección de 3º | Sí (explícito «cursos posteriores») |
| Práctica profundidad: tamaño, solape, sombra | Sí (md + `l10-luz-sombra-profundidad.html`) |

---

## 5. Dudas con prompts (Jorge → Grok/Claude)

### D1 — DUDA-2 cobertura A4

```
Curso: EPVA 1º ESO CyL. Archivo: COBERTURA-DECRETO.md DUDA-2.
Hecho: en PDF de 1º la viñeta A4 aparece como «Las formas geométricas en el arte y en el entorno. Patrimonio arquitectónico».
Pregunta: ¿Confirmamos que A4 de 1º termina ahí, sin añadir «de Castilla y León» u otra frase no presente en BOCyL de 1º?
Opciones: (A) Sí, citar literal. (B) Añadir CyL en didáctica sin presentarlo como cita del decreto.
```

### D2 — DUDA-3 grafía «grafico-plásticas»

```
BOCyL escribe «Transformaciones grafico-plásticas» (sin tilde en gráfico) en la viñeta.
¿En lecciones: (A) cita literal del decreto + «gráfico-plásticas» en prosa didáctica, o (B) unificar siempre a «gráfico-plásticas»?
```

---

## 6. Veredicto

**OK lote L01–L10 — publicable.**  
No OK curso EPVA completo (faltan L11–31).  
Pendientes no bloqueantes: I1 (densidad), I2/D1/D2 (dudas cobertura).

