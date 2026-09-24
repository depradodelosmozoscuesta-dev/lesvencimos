# QA bloque L11–L31 · 1º ESO EPVA (Plástica Visual) · Re-revisión

**Fecha:** 2026-09-24 (Europe/Madrid, CEST / UTC+2)  
**Revisor:** Revisor ESO  
**Canónico:** `/workspace/lesvencimos/profesor/1eso-plastica-visual/`  
**Prohibido:** `lesultimos` / `lescircimos`  
**Alcance:** md + shells HTML + widgets Tinta L11–L31 (L01–L10 no reabiertos salvo regresión hub).  
**No se reescribió temario** (solo ficha QA).

---

## Criterios comprobados

| # | Criterio | Estado |
|---|---|---|
| 1 | Rutas Tinta desde `lecciones/` = `../../../modulos/tinta-estudio.html` (no `../../`) | ✅ 0 malas / 72 buenas; resuelve a `modulos/tinta-estudio.html` |
| 2 | L11,12,13,15,20,21,22,23,25,27,28,31 con CTA + widgets usables | ✅ shells con `#practica-tinta` + iframe widget + CTA; widgets con consignas + iframe/CTA Tinta |
| 3 | L31 proyecto: etapas C1 + exposición D5 + Tinta | ✅ meta C1,D5; seis etapas en hoja 2; ficha D5 en entrega; widget + Tinta |
| 4 | Quizzes: correcta no siempre 1.ª opción | ✅ posiciones A×2 / B×11 / C×7 / D×1 (L11–31); sync md↔html 0 mismatches |
| 5 | Sin relleno (curiosidad solo histórica real; vida real solo evidente) | ✅ 0 bloques «curiosidad/vida real/¿sabías?/TODO» |
| 6 | Nada incorrecto / sin sentido; glosas; ritmo | ⚠️ contenido muestreado OK; **glosas a menudo sin definición** (mejora) |
| 7 | Hub lista L01–31 **disponibles** | ❌ **CRÍTICO** — L11–31 = `hub-pronto` / «Próximamente» **sin** `href` |

---

## Inventario L11–L31 (en disco canónico)

| L | Título (shell) | MD | Shell | Alias | Widget Tinta |
|---|---|---|---|---|---|
| 11 | Transformaciones gráfico-plásticas | `11.md` | `leccion-11-transformaciones-grafico-plasticas.html` | `leccion-11.html` | `l11-transformaciones.html` |
| 12 | Composición I: formato, encuadre y estructuras | `12.md` | `leccion-12-composicion-i-formato-encuadre-y-estructuras.html` | `leccion-12.html` | `l12-composicion-formato.html` |
| 13 | Composición II: equilibrio, proporción y ritmo | `13.md` | `leccion-13-composicion-ii-equilibrio-proporcion-y-ritmo.html` | `leccion-13.html` | `l13-composicion-equilibrio.html` |
| 14 | El proceso creativo: seis etapas | `14.md` | `leccion-14-el-proceso-creativo-seis-etapas.html` | `leccion-14.html` | — (C1; Tinta opcional) |
| 15 | Operaciones plásticas… | `15.md` | `leccion-15-operaciones-plasticas-….html` | `leccion-15.html` | `l15-operaciones-plasticas.html` |
| 16 | Instrumentos y materiales de dibujo técnico | `16.md` | `leccion-16-….html` | `leccion-16.html` | — |
| 17 | Geometría plana: lugares y trazados básicos | `17.md` | `leccion-17-….html` | `leccion-17.html` | — |
| 18 | Figuras planas y polígonos… | `18.md` | `leccion-18-….html` | `leccion-18.html` | — |
| 19 | Proporcionalidad, Tales, igualdad, semejanza y escalas | `19.md` | `leccion-19-….html` | `leccion-19.html` | — |
| 20 | Movimientos en el plano: simetrías y traslaciones | `20.md` | `leccion-20-….html` | `leccion-20.html` | `l20-simetrias-traslaciones.html` |
| 21 | Técnicas secas en dos dimensiones | `21.md` | `leccion-21-….html` | `leccion-21.html` | `l21-tecnicas-secas.html` |
| 22 | Técnicas húmedas en dos dimensiones | `22.md` | `leccion-22-….html` | `leccion-22.html` | `l22-tecnicas-humedas.html` |
| 23 | Soportes físicos y digitales | `23.md` | `leccion-23-….html` | `leccion-23.html` | `l23-soportes.html` |
| 24 | Comunicación visual… | `24.md` | `leccion-24-….html` | `leccion-24.html` | — |
| 25 | Realismo, figuración y abstracción | `25.md` | `leccion-25-….html` | `leccion-25.html` | `l25-realismo-abstraccion.html` |
| 26 | Lenguaje visual en prensa, publicidad, TV… | `26.md` | `leccion-26-….html` | `leccion-26.html` | — |
| 27 | Fotografía: imagen fija | `27.md` | `leccion-27-….html` | `leccion-27.html` | `l27-fotografia.html` |
| 28 | Cómic: características y práctica | `28.md` | `leccion-28-….html` | `leccion-28.html` | `l28-comic.html` |
| 29 | Cine, animación y formatos digitales | `29.md` | `leccion-29-….html` | `leccion-29.html` | — |
| 30 | Técnicas expositivas básicas… | `30.md` | `leccion-30-….html` | `leccion-30.html` | — |
| 31 | Proyecto de curso: del boceto a la exposición | `31.md` | `leccion-31-proyecto-de-curso-del-boceto-a-la-exposicion.html` | `leccion-31.html` | `l31-proyecto-curso.html` |

**Presencia:** 21/21 md · 21 shells largos · 21 aliases redirect · 12/12 widgets esperados.  
**Git:** L11–31 aparecen como **untracked** tras commit `acc598b` (solo publicó L01–L10 + hub parcial). Archivos **sí** están en el FS canónico.

---

## Checks técnicos

### Rutas Tinta (crítico si falla)
- Desde `lecciones/`: **solo** `../../../modulos/tinta-estudio.html` en md, shells y widgets del bloque.
- `../../modulos/…` → `/workspace/lesvencimos/profesor/modulos/` (**no existe**): **0 hits**.
- Assets shell: `../../_plantilla-leccion/leccion-shell.css|.js`, brand, calculadora, index → OK.

### Hub (`1eso-plastica-visual.html`)
- L01–L10: `hub-disponible` + enlaces OK (sin regresión de hrefs L01–10).
- L11–L31: clase `hub-pronto`, texto «Próximamente», **sin** `<a href="lecciones/leccion-NN-…">`.
- Hero: «Lecciones 01–10 disponibles» / «10/31» / «L11–L31 aún en producción».
- Pie: Tinta solo L06–L10 (no menciona widgets L11+).
- Contradice `TEMARIO.md` § Estado: «L11–L31 … hub marca L01–L31 disponibles».

### L31 (C1 + D5 + Tinta)
| Pieza | ¿OK? |
|---|---|
| Viñetas C1, D5 en meta md/html | Sí |
| Seis etapas nombradas (inv→plan→des→rea→dif→eva) | Sí (hoja 2; eco L14) |
| Exposición / ficha D5 en entrega mínima | Sí |
| Widget `l31-proyecto-curso.html` + CTA Tinta | Sí |
| Quiz correcta = proceso C1 + exposición D5 | Sí (B) |

### Quizzes (posición de la correcta)
L11 B · L12 C · L13 D · L14 B · L15 C · L16 B · L17 C · L18 C · L19 A · L20 C · L21 B · L22 B · L23 C · L24 B · L25 B · L26 B · L27 B · L28 A · L29 B · L30 B · L31 B.  
No hay sesgo «siempre A».

### Nav prev/next L11–31
Cadena de shells largos íntegra; L31 next disabled.

---

## Hallazgos

### Críticos (bloquean OK)

| ID | Hallazgo | Rutas / evidencia |
|---|---|---|
| **C1** | Hub **no** lista L11–L31 como disponibles (check 7). Lecciones existen en disco pero el índice las marca «Próximamente» sin enlace. | `/workspace/lesvencimos/profesor/1eso-plastica-visual/1eso-plastica-visual.html` (líneas hero ~132–139; ítems `hub-pronto` 11–31). Mirror: `downloads/1eso-plastica-visual.html`. |
| **C2** | `TEMARIO.md` afirma publicación L11–L31 + hub L01–31 disponibles; el hub committed (`acc598b`) dice lo contrario. | `/workspace/lesvencimos/profesor/1eso-plastica-visual/TEMARIO.md` § «Estado de producción» (fila L11–L31). |

### Mejoras (no bloquean por sí solas)

| ID | Hallazgo | Evidencia / acción |
|---|---|---|
| M1 | Glosario: muchos `<li><strong>Término</strong></li>` **sin** glosa (L11,13,14,17–31 en distinto grado; p. ej. L20/L24/L25/L27/L29–31 todos vacíos). | Completar «— definición» alineada a la hoja 2 de **esa** lección. |
| M2 | Densidad shell baja (~190–260 palabras visibles; md ~140–170). Mismo patrón OK’d en L01–10; valorar ampliar explicación/ejemplos sin relleno. | Sobre todo L16–19, L24, L26, L29–30. |
| M3 | Widget L31: 5 consignas (fusiona desarrollo+realización) vs 6 etapas del shell. | Alinear lista del widget a las seis etapas. |
| M4 | L11–L31 **untracked** en git tras commit parcial L01–L10. | Añadir a repo cuando se reactive el hub; no mezclar con ZIP «10/31» sin actualizar pack. |
| M5 | Pie del hub / copy «curso en construcción» desactualizados respecto a archivos ya generados. | Misma reparación que C1. |

### No hallados
- Rutas Tinta rotas `../../modulos`.
- Widgets faltantes del set esperado.
- Fallo L31 C1/D5/Tinta de contenido.
- Quizzes con correcta siempre 1.ª.
- Relleno tipo curiosidad/vida real decorativa.
- Errores de concepto graves en muestreo (mediatriz, semejanza, traslación, lavado, jerarquía, secuencia cómic, animación vs cine).
- Rotura de enlaces L01–L10 en hub.
- md↔html desync de respuesta de quiz.

---

## DUDA (prompt copiable)

Si el padre deliberó **no** publicar L11–L31 en hub aún (ZIP solo 10/31), entonces C1/C2 son coherentes con el commit `acc598b` y el veredicto de este bloque sigue siendo **NO OK para “hub lista L01–31”** hasta que se active. Prompt:

```
Plástica 1º ESO — activar hub L11–L31 en canónico /workspace/lesvencimos

1) En profesor/1eso-plastica-visual/1eso-plastica-visual.html:
   - Pasar ítems 11–31 de hub-pronto → hub-disponible con <a href="lecciones/leccion-NN-….html">
   - Actualizar hero: «31 lecciones disponibles (L01–L31)» (quitar «10/31» / «aún en producción»)
   - Pie: mencionar Tinta también en L11,12,13,15,20–23,25,27,28,31
2) Sync downloads/1eso-plastica-visual.html
3) Alinear TEMARIO.md § Estado con el hub real
4) git add lecciones/{11..31}.md + shells + aliases + widgets l11/l12/…/l31
5) No tocar L01–L10 salvo copy del hub
```

---

## Veredicto

**NO OK** — **2 críticos** / **5 mejoras**.  
OK solo con **0 críticos**. Blocker principal: hub no expone L11–L31. Contenido md/shells/widgets del bloque, rutas Tinta y L31 C1+D5 están en buen estado técnico en disco.

**Firmado:** Revisor ESO · 2026-09-24 Europe/Madrid


---

## Re-revisión hub/TEMARIO (2026-09-24 · Revisor ESO)

**C1 cerrado:** hub `1eso-plastica-visual.html` — 31/31 `hub-disponible` con `href` a shells reales; 0 ítems `hub-pronto` en lista; mirror `downloads/` alineado.  
**C2 cerrado:** `TEMARIO.md` § Estado: L01–L31 publicados y hub enlaza las 31.

**Veredicto tras re-revisión:** **OK** — **0 críticos** abiertos en L11–L31 + hub.

Firmado: Revisor ESO · Europe/Madrid


---

## Re-OK tras D1–D3 Dios (2026-09-24 · Revisor ESO)

**Contexto:** Revisor Dios REABRIÓ sello curso (D1 ficha L01–10; D2 TEMARIO; D3 glosas vacías). Autor cerró D2/D3; D1 ya tenía ficha ESO.

| Id | Comprobación | Estado |
|---|---|---|
| D1 | `lecciones/_qa-bloque-01-10.md` presente, OK L01–10 · 0 críticos | ✅ trazable |
| D2 | `TEMARIO.md` § Estado: sin «pendiente…»; marca sello impugnado hasta CONFIRMA Dios | ✅ |
| D3 | Glosarios L13 + L17–L31: **0 vacías** (rescaneado; 60 entradas con definición) | ✅ |

Muestreo calidad glosas L17/L20/L24/L31: definiciones reales (no solo término).

**Veredicto re-OK tramos tocados (L13 + L17–L31 + D1/D2):** **OK — 0 críticos.**

Cadena siguiente: Revisor final (nuevo sello curso) → Revisor Dios (2.ª pasada).  
**No** se declara OK curso vigente desde Revisor ESO.

Firmado: Revisor ESO · Europe/Madrid
