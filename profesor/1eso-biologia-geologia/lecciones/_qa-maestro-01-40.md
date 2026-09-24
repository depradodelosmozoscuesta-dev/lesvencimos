# QA Revisor ESO — Modo maestro ByG 1º ESO L01–L40

**Fecha:** 2026-09-24 · Europe/Madrid (UTC+2)  
**Agente:** Revisor ESO  
**Canónico:** `/workspace/lesvencimos`  
**Ámbito:** modo maestro (`maestro-01.json`…`maestro-40.json` + shells largos + runtime)  
**Mapa consultado (no copiado como veredicto):** `profesor/1eso-biologia-geologia/_auto-revision-maestro-01-40.md`

---

## Veredicto

**OK** — **0 críticos** / **1 mejora**

El modo maestro L01–L40 está cableado, las anclas del JSON existen en los shells largos, intro «modo maestro de Biología y Geología» en las 40, glosas (VERAZ, CE-FU, Nu-Re-Re, INTRA/INTER, PRO-CON-DES, SÉ·GUARDO·MEJORO, One Health / tres saludes) alineadas con cada `NN.md`, embed ↔ JSON sin drift, y `?maestro=1` usable. Sin inventar currículo ni música. La única mejora es listeners `maestro:*` en widgets (no bloquea: el runtime reenvía `postMessage`).

| Métrica | Resultado |
|---|---|
| Guiones `maestro-01.json`…`maestro-40.json` | **40/40** |
| Shells largos CSS + JS + `data-maestro-json` | **40/40** |
| Anclas JSON → ids HTML (sistemático) | **0 rotas** |
| Ids duplicados en shells | **0** |
| Embed `data-maestro="guion"` vs JSON externo | **0 drift** |
| `curso` = `1eso-biologia-geologia` | **40/40** |
| Intro «modo maestro de Biología y Geología» | **40/40** |
| `decir` / réplicas `dialogo` ≤3 frases | **0 incumplimientos** |
| Hub CTA → L01 `?maestro=1` | **OK** |
| Runtime JS (`node --check`) | **OK** |
| Críticos | **0** |
| Mejoras | **1** |

---

## Método

1. Inventario: 40 JSON, 40 shells `leccion-NN-*.html` (alias corto fuera de alcance), runtime en `profesor/_maestro/`.
2. Script sistemático: wiring (`../../_maestro/maestro-puntero.css` + `maestro-runtime.js` + `data-maestro-json`), parse JSON, conteo de frases, cruce anclas ↔ `id=`, dups, sync embed↔JSON, `curso`/`url`/`musica`, intro, CDN, `iframeCmd`.
3. Muestreo profundo JSON+shell: **L01, L02, L08, L14, L17, L22, L31, L32, L38, L40** (+ barrido de frases/anclas en las 40).
4. Hub pack: `1eso-biologia-geologia/1eso-biologia-geologia.html` (no raíz `profesor/`).
5. `node --check` sobre `profesor/_maestro/maestro-runtime.js`.
6. Auto-mapa ByG usado solo como focos; hallazgos re-verificados.

---

## 1. Guiones (voz maestro)

- Norma **≤3 frases** por paso (`decir` y réplicas de `dialogo`): **0 incumplimientos** (máximo observado = 3).
- Sin relleno detectado (muletillas / música inventada / meta).
- Intro oral fija en paso `intro` de las **40**: «modo maestro de Biología y Geología».
- `musica: false` en las 40; pasos por lección **7–10** (media ≈7,4).
- Diálogos multi-voz muestreados: **L01** (hipótesis Lucía/Marcos), **L31** (INTRA vs INTER) — réplicas ≤3; `decir` del paso + `dialogo` válidos.
- Muestreo L01/L02/L08/L14/L17/L22/L31/L32/L38/L40: tono oral corto, coherente con bloque anclado y con `NN.md` (método, VERAZ, ciclo de rocas, hidrosfera, CE-FU, Nu-Re-Re, relaciones, PRO-CON-DES, One Health, SÉ·GUARDO·MEJORO).
- Curiosidad Alhazén (L01): **no inventada** — figura en el aside `#maestro-curiosidad` del shell y en el guion.

---

## 2. Anclas JSON ↔ shell

- Cruce automático en las **40** lecciones: **ninguna ancla ausente**.
- `#maestro-titulo`, `#maestro-objetivos`, `#maestro-explicacion`, `#maestro-interactivo`, `#maestro-cierre`, `#maestro-reto` presentes donde el JSON las cita; `#maestro-curiosidad` solo si hay aside (coherente).
- Selector `.marco-interactivo` resuelve en todos los pasos que lo usan.
- Sin `id=` duplicados en ningún shell largo.

---

## 3. Cableado y runtime

| Pieza | Ruta canónica | Uso en shells |
|---|---|---|
| CSS | `profesor/_maestro/maestro-puntero.css` | `../../_maestro/maestro-puntero.css` · **40/40** |
| JS | `profesor/_maestro/maestro-runtime.js` | `../../_maestro/maestro-runtime.js` · **40/40** |
| Guion | `lecciones/maestro-NN.json` | `data-maestro-json="maestro-NN.json"` · **40/40** |

- Embed `<script type="application/json" data-maestro="guion">` presente y **alineado** con el JSON externo en las 40 (fallback `file://`).
- Atajo `atajo-maestro` → `?maestro=1`: **40/40**.
- Sin CDN / HTTP externo en shells largos (offline OK para assets de lección).
- `iframeCmd` con tiento: **40**× `maestro:reset` + **1**× `maestro:highlight` (L01); tipos `maestro:*` válidos.

---

## 4. Glosas (solo lo que pide cada lección)

| Lección | Glosa / mnemónico en guion | En `NN.md` | Veredicto |
|---|---|---|---|
| L02 | VERAZ | sí | **OK** |
| L17 | CE-FU (+ pro/eu) | sí | **OK** |
| L22 | Nu-Re-Re | sí | **OK** |
| L31 | INTRA / INTER | sí | **OK** |
| L32 | PRO-CON-DES | sí | **OK** |
| L38 | One Health / tres saludes | sí (decreto F) | **OK** |
| L40 | SÉ · GUARDO · MEJORO | sí | **OK** |
| L01 | Oso Pequeño… / O-P-H-E-D-C | sí | **OK** |

Sin glosas inventadas fuera del temario de cada lección.

---

## 5. Hub + `?maestro=1`

- Hub: `profesor/1eso-biologia-geologia/1eso-biologia-geologia.html`.
- CTA **«Probar modo maestro»** → `lecciones/leccion-01-el-metodo-cientifico-en-experimentos-sencillos.html?maestro=1`.
- Runtime: autoarranque con `?maestro=1`; `node --check` **sin error de sintaxis**.

---

## Críticos / mejoras

### Críticos — **0**

Ningún blocker de contenido/voz, frases, anclas, dups, cableado, `curso`, intro, embed drift, CDN u `iframeCmd`.

### Mejoras — **1**

| ID | Ruta | Hallazgo | Acción sugerida |
|---|---|---|---|
| M1 | Widgets `lecciones/lNN-*.html` (ByG) | El guion envía `maestro:reset` / `highlight` con tiento; los iframes aún pueden ignorarlo (no documentados de forma uniforme en `docs/modo-maestro-voz.md`). | En lote posterior, añadir listeners `maestro:reset` / `maestro:highlight` por interactivo (como Mate L01–L19). **No reescrito** en esta QA. |

---

## Checklist de éxito

- [x] Guiones L01–L40 presentes y válidos
- [x] Shells largos cablean CSS + JS + `data-maestro-json`; rutas runtime resuelven
- [x] Anclas del JSON existen en el shell; sin ids duplicados
- [x] Intro «modo maestro de Biología y Geología»; `curso` correcto
- [x] Embed ↔ JSON sin drift; ≤3 frases/paso
- [x] Hub CTA Modo maestro → L01 `?maestro=1`
- [x] `?maestro=1` usable (runtime + JSON)
- [x] Glosas solo las de cada lección
- [x] Ficha escrita en esta ruta
- [x] Sin reescritura de temario ni guiones; sin publish; Mate no reabierto

---

**Firmado:** Revisor ESO · 2026-09-24 Europe/Madrid
