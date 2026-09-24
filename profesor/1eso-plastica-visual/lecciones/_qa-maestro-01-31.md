# QA Revisor ESO — Modo maestro Plástica 1º ESO L01–L31

**Fecha:** 2026-09-24 · Europe/Madrid (UTC+2)  
**Agente:** Revisor ESO  
**Canónico:** `/workspace/lesvencimos`  
**Ámbito:** modo maestro (`maestro-01.json`…`maestro-31.json` + shells largos + runtime)  
**Mapa consultado (no copiado como veredicto):** `profesor/1eso-plastica-visual/_auto-revision-maestro-01-31.md`  
**Diseño de voz:** `profesor/docs/modo-maestro-voz.md`

---

## Veredicto

**OK** — **0 críticos** / **0 mejoras**

El modo maestro L01–L31 está cableado, las anclas del JSON existen en los shells largos, `curso` es correcto, embed ≡ JSON, intros «modo maestro de Plástica», y `?maestro=1` es usable. Muestreo profundo sin hechos inventados ni relleno. Norma ≤3 frases/paso: 0 incumplimientos.

| Métrica | Resultado |
|---|---|
| Guiones `maestro-01.json`…`maestro-31.json` | **31/31** |
| Shells largos CSS + JS + `data-maestro-json` | **31/31** |
| Anclas JSON → ids HTML (sistemático) | **0 rotas** |
| Ids `maestro-*` duplicados en shell | **0** |
| Embed `data-maestro="guion"` vs JSON externo | **0 drift** |
| Campo `curso` = `1eso-plastica-visual` | **31/31** |
| Hub CTA «Probar modo maestro» → L01 `?maestro=1` | **sí** |
| Runtime JS (`node --check`) | **OK** |
| Frases >3 en `decir` / réplicas | **0** |
| Críticos | **0** |
| Mejoras | **0** |

---

## Método

1. Inventario: 31 JSON, 31 shells `leccion-NN-*.html`, runtime en `profesor/_maestro/`.
2. Script sistemático Python: wiring, parse JSON, conteo de frases (split español `.!?…`), cruce anclas ↔ `id=`, ids duplicados, sync embed↔JSON normalizado, `curso`, rutas relativas, CDN, intros, `iframeCmd`.
3. Muestreo profundo JSON + shell (+ md): **L01, L03, L10, L17, L24, L31**.
4. Hub: `profesor/1eso-plastica-visual/1eso-plastica-visual.html`.
5. `node --check` sobre `profesor/_maestro/maestro-runtime.js`.
6. Auto-mapa usado solo como focos; hallazgos re-verificados.

---

## 1. Guiones (voz maestro)

- Norma **≤3 frases** por paso (`decir` y réplicas): **0 incumplimientos** (267 pasos; 97 con exactamente 3).
- Intros: las 31 abren con «soy el modo maestro de **Plástica**».
- Sin relleno detectado (escaneo de muletillas / curiosidad inventada).
- Sin `dialogo` multi-voz (coherente con el auto-mapa; no aporta en esta asignatura).
- Muestreo L01/L03/L10/L17/L24/L31: tono oral corto, alineado con `NN.md` / saberes (patrimonio material-inmaterial; formal/contexto CyL; percepción/luz; mediatriz-bisectriz; finalidades D1; proyecto seis etapas). Sin currículo inventado.

---

## 2. Anclas JSON ↔ shell

- Cruce automático en las **31** lecciones: **ninguna ancla ausente**.
- Todas las anclas son `#maestro-*` (sin selectores raros).
- Muestreo manual L01/L03/L10/L17/L24/L31: ids presentes; sin duplicados `maestro-*`.

---

## 3. Cableado y runtime

| Pieza | Ruta canónica | Uso en shells |
|---|---|---|
| CSS | `profesor/_maestro/maestro-puntero.css` | `../../_maestro/maestro-puntero.css` · **31/31** |
| JS | `profesor/_maestro/maestro-runtime.js` | `../../_maestro/maestro-runtime.js` · **31/31** |
| Guion | `lecciones/maestro-NN.json` | `data-maestro-json="maestro-NN.json"` · **31/31** |

- Embed `<script type="application/json" data-maestro="guion">` presente y **alineado** con el JSON externo (31/31; fallback `file://`).
- Sin CDN en shells ni en widgets `lNN-*.html`.
- `musica: false` en todas.
- Alias cortos `leccion-NN.html`: fuera de alcance (brief = shells largos).

### Hub

`1eso-plastica-visual/1eso-plastica-visual.html`: CTA **Probar modo maestro** → `lecciones/leccion-01-patrimonio-proteger-y-conservar-el-legado.html?maestro=1`.

---

## 4. `iframeCmd` (Tinta)

17 pasos `interactivo` en L06–L13, L15, L20–L23, L25, L27–L28, L31: `{"type":"maestro:reset"}` solo donde el shell tiene iframe Tinta. OK con tiento (el widget puede ignorar).

---

## 5. `?maestro=1`

- Runtime: autoarranque con `?maestro=1`; carga JSON + fallback embed.
- `node --check` `maestro-runtime.js`: **sin error de sintaxis**.
- Sin errores de JSON ni de cableado que impidan arrancar.

---

## 6. Glosas (Jorge)

No aplica glosa tipo S/A/L de Mate. Vocabulario de cada lección (patrimonio, formal/contexto, mediatriz, finalidades, etc.) se glosa solo lo que el `NN.md` pide. Sin inventar.

---

## Críticos / mejoras

### Críticos — **0**

Ningún blocker de ancla, cableado, drift, `curso`, frases >3, CDN, intro o contenido inventado.

### Mejoras — **0**

Nada bloqueante ni de voz que merezca reescritura en esta pasada.

---

## Notas de muestreo

| Lección | Pasos | Notas |
|---|---:|---|
| L01 | 11 | Patrimonio material/inmaterial; ejemplos retablo/bordado/muro; alineado con `01.md`. |
| L03 | 9 | Formal + contexto CyL; sin lista inventada de obras. |
| L10 | 10 | Luz/sombra/profundidad + Tinta `iframeCmd`; perspectiva «se entiende; trazado después» coherente con el md. |
| L17 | 8 | Lugar geométrico, mediatriz, bisectriz, perpendicular/paralela — quiz md C. |
| L24 | 8 | Finalidades + elementos del acto comunicativo (D1). |
| L31 | 9 | Seis etapas + Tinta + evidencias/portfolio; cierre de curso. |

---

## Checklist de éxito

- [x] Guiones L01–L31 presentes y válidos
- [x] Shells largos cablean CSS + JS + `data-maestro-json`; rutas runtime resuelven
- [x] Anclas del JSON existen en el shell; sin ids `maestro-*` duplicados
- [x] Intro «modo maestro de Plástica»
- [x] Hub con Probar modo maestro → L01 `?maestro=1`
- [x] Embed ≡ JSON; `curso` correcto; sin CDN
- [x] `?maestro=1` usable (runtime + JSON)
- [x] Ficha escrita en esta ruta
- [x] Sin reescritura de temario ni guiones; sin publicar

---

**Firmado:** Revisor ESO · 2026-09-24 Europe/Madrid
