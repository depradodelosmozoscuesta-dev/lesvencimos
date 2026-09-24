# QA Revisor ESO — Modo maestro Lengua Castellana 1º ESO L01–L40

**Fecha:** 2026-09-24 · Europe/Madrid (UTC+2)  
**Agente:** Revisor ESO  
**Canónico:** `/workspace/lesvencimos`  
**Ámbito:** modo maestro (`maestro-01.json`…`maestro-40.json` + shells largos + runtime)  
**Mapa consultado (no copiado como veredicto):** `profesor/1eso-lengua-castellana/_auto-revision-maestro-01-40.md`  
**Diseño de voz:** `profesor/docs/modo-maestro-voz.md`

---

## Veredicto

**OK** — **0 críticos** / **1 mejora**

El modo maestro L01–L40 está cableado, las anclas del JSON existen en los shells largos, `curso` es correcto, embed ≡ JSON, intros «modo maestro de Lengua», diálogos multi-voz coherentes, y `?maestro=1` es usable. Norma ≤3 frases/paso: 0 incumplimientos. Una mejora de cobertura: bloques `#maestro-vida` presentes en 8 shells no visitados por el guion.

| Métrica | Resultado |
|---|---|
| Guiones `maestro-01.json`…`maestro-40.json` | **40/40** |
| Shells largos CSS + JS + `data-maestro-json` | **40/40** |
| Anclas JSON → ids HTML (sistemático) | **0 rotas** |
| Ids `maestro-*` duplicados en shell | **0** |
| Embed `data-maestro="guion"` vs JSON externo | **0 drift** |
| Campo `curso` = `1eso-lengua-castellana` | **40/40** |
| Hub CTA «Probar modo maestro» → L01 `?maestro=1` | **sí** (+ listado L01–L40) |
| Runtime JS (`node --check`) | **OK** |
| Frases >3 en `decir` / réplicas | **0** |
| Críticos | **0** |
| Mejoras | **1** |

---

## Método

1. Inventario: 40 JSON, 40 shells `leccion-NN-*.html`, runtime en `profesor/_maestro/`.
2. Script sistemático Python: wiring, parse JSON, conteo de frases (split español `.!?…`), cruce anclas ↔ `id=`, ids duplicados, sync embed↔JSON normalizado, `curso`, rutas relativas, CDN, intros, `iframeCmd`, muletillas.
3. Muestreo profundo JSON + shell (+ md): **L01, L08, L13, L26, L31, L32, L38, L40** (+ L09 por hit de escáner «curiosidad»).
4. Hub: `profesor/1eso-lengua-castellana/1eso-lengua-castellana.html`.
5. `node --check` sobre `profesor/_maestro/maestro-runtime.js`.
6. Auto-mapa usado solo como focos; hallazgos re-verificados.

---

## 1. Guiones (voz maestro)

- Norma **≤3 frases** por paso (`decir` y réplicas de `dialogo`): **0 incumplimientos** (298 pasos; 82 con exactamente 3).
- Intros: las 40 abren con «soy el modo maestro de **Lengua**».
- Diálogos multi-voz (con tiento): L08, L13, L26, L32, L34, L38 — réplicas ≤3 frases; roles alumno/alumna/narrador.
- L09 `localismo`: «Curiosidad, no burla.» — **no es relleno**: es actitud pedagógica alineada con el md (localismos sin burla). No crítico.
- Muestreo: mnemónicos y ejemplos coinciden con `NN.md` (Tres Abrigos; S-C-Y-V; DI-EX; VP; NaLiTe; CoMeP-HA; SA-PD-V+APCI; OrDiVu-P). Sin currículo inventado.

---

## 2. Anclas JSON ↔ shell

- Cruce automático en las **40** lecciones: **ninguna ancla ausente**.
- Todas las anclas son `#maestro-*`.
- Muestreo L01/L08/L13/L26/L31/L32/L38/L40: ids presentes; sin duplicados `maestro-*`.
- **Nota (mejora M1):** 8 shells tienen `#maestro-vida` (contenido CyL real del md) pero el guion **no** apunta a esa ancla: L01, L05, L08, L17, L23, L28, L32, L40. No es ancla rota (el JSON no la cita); es cobertura incompleta del bloque «En la vida real».

---

## 3. Cableado y runtime

| Pieza | Ruta canónica | Uso en shells |
|---|---|---|
| CSS | `profesor/_maestro/maestro-puntero.css` | `../../_maestro/maestro-puntero.css` · **40/40** |
| JS | `profesor/_maestro/maestro-runtime.js` | `../../_maestro/maestro-runtime.js` · **40/40** |
| Guion | `lecciones/maestro-NN.json` | `data-maestro-json="maestro-NN.json"` · **40/40** |

- Embed `data-maestro="guion"` presente y **alineado** con el JSON externo (40/40).
- Sin CDN en shells ni en widgets `lNN-*.html`.
- `musica: false` en todas.
- Sin `iframeCmd` (no hay iframes Tinta en este pack): OK.

### Hub

`1eso-lengua-castellana/1eso-lengua-castellana.html`: CTA **Probar modo maestro (L01) →** + texto «Modo maestro» + listado L01–L40 con `?maestro=1`.

---

## 4. Glosas (Jorge)

No aplica glosa tipo S/A/L de Mate. Mnemónicos del md (S-C-Y-V, NaLiTe, etc.) se pronuncian tal cual; sin inventar etiquetas nuevas. L38 etiqueta Det+Sust+Verbo sobre «La niña lee un cuento» — coherente con el ejemplo del md.

---

## 5. `?maestro=1`

- Runtime: autoarranque con `?maestro=1`; JSON + fallback embed.
- `node --check` `maestro-runtime.js`: **sin error de sintaxis**.
- Sin errores de JSON ni de cableado que impidan arrancar.

---

## Críticos / mejoras

### Críticos — **0**

Ningún blocker de ancla, cableado, drift, `curso`, frases >3, CDN, intro o contenido inventado.

### Mejoras — **1**

| ID | Ruta | Hallazgo | Acción sugerida |
|---|---|---|---|
| M1 | `lecciones/maestro-01.json`, `05`, `08`, `17`, `23`, `28`, `32`, `40` (+ embeds) | Shell con `#maestro-vida` (bloque «En la vida real» del md) sin paso que lo ancle. | Añadir 1 paso corto `ancla: "#maestro-vida"` con 1–2 frases reales del md (CyL). **No reescrito** en esta QA. |

---

## Notas de muestreo

| Lección | Pasos | Notas |
|---|---:|---|
| L01 | 8 | Tres Abrigos; ejemplos León/Soria; interactivo laboratorio. Vida en shell sin visitar (M1). |
| L08 | 9 | Diálogo seseo + voseo/yeísmo; respeto + norma escolar CyL. |
| L09 | 8 | «CyL no es un bloque»; «Curiosidad, no burla» = actitud, no ficha inventada. |
| L13 | 8 | Diálogo alumno/alumna vs exposición narrador (DI-EX). |
| L26 | 8 | Diálogo coma «Vamos a comer[,] niños»; coherencia verbal. |
| L31 | 8 | NaLiTe; fragmentos narrativa/lírica. |
| L32 | 7 | Diálogo metáfora/personificación + efecto (CoMeP-HA). |
| L38 | 8 | SA-PD-V+APCI; truco «empieza por el verbo». |
| L40 | 8 | OrDiVu-P; *haiga→haya*; hay/ay/ahí; cierre portfolio. Vida sin visitar (M1). |

---

## Checklist de éxito

- [x] Guiones L01–L40 presentes y válidos
- [x] Shells largos cablean CSS + JS + `data-maestro-json`; rutas runtime resuelven
- [x] Anclas del JSON existen en el shell; sin ids `maestro-*` duplicados
- [x] Intro «modo maestro de Lengua»
- [x] Hub con Probar modo maestro → L01 `?maestro=1`
- [x] Embed ≡ JSON; `curso` correcto; sin CDN
- [x] `?maestro=1` usable (runtime + JSON)
- [x] Ficha escrita en esta ruta
- [x] Sin reescritura de temario ni guiones; sin publicar

---

**Firmado:** Revisor ESO · 2026-09-24 Europe/Madrid


---

## Re-OK M1 (2026-09-24) — pasos `#maestro-vida`

**Alcance:** L01, L05, L08, L17, L23, L28, L32, L40 tras corrección Mate.

| Lección | id paso | ancla | frases (reales) | embed sync | id en shell |
|--------:|---------|-------|----------------:|:----------:|:-----------:|
| 01 | `vida-burgos-zamora` | `#maestro-vida` | 2 | OK | OK |
| 05 | `vida-lenguas-signos` | `#maestro-vida` | 2 | OK | OK |
| 08 | `vida-escucha-escritura` | `#maestro-vida` | 2 | OK | OK |
| 17 | `vida-redes-cyl` | `#maestro-vida` | 2 | OK | OK |
| 23 | `vida-avisos-aula` | `#maestro-vida` | 2 | OK | OK |
| 28 | `vida-bibliotecas` | `#maestro-vida` | 2 | OK | OK |
| 32 | `vida-recursos-avila` | `#maestro-vida` | 2 | OK | OK |
| 40 | `vida-portfolio-cyl` | `#maestro-vida` | 2 | OK | OK |

Nota L28: el texto usa `…` dentro de «Leí… / Quiero leer… / Me gusta cuando…»; no son fines de frase (conteo real = 2).

**Veredicto re-OK M1:** **OK** — **0 críticos**. M1 cerrado. ByG/Geo listeners siguen como menor aceptado (fuera de este re-OK).

**¿OK Lengua modo maestro tras M1?** **SÍ**
