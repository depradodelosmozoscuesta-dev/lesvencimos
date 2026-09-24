# QA Revisor ESO — Modo maestro GeoHistoria 1º ESO L01–L36

**Fecha:** 2026-09-24 · Europe/Madrid (UTC+2)  
**Agente:** Revisor ESO  
**Canónico:** `/workspace/lesvencimos`  
**Ámbito:** modo maestro (`maestro-01.json`…`maestro-36.json` + shells largos + runtime)  
**Mapa consultado (no copiado como veredicto):** `profesor/1eso-geografia-historia/_auto-revision-maestro-01-36.md`

---

## Veredicto

**OK** — **0 críticos** / **1 mejora**

El modo maestro L01–L36 está cableado, anclas del JSON resueltas en shells largos, intro «modo maestro de Geografía e Historia» en las 36, glosas (MAPA, MAB, POLIS-ALEX, ROMA-CyL, SE-POR-HAB / Sé-por-hab) alineadas con cada `NN.md`, embed ↔ JSON sin drift, hub CTA → L01 `?maestro=1`, y runtime OK. Sin inventar currículo ni música. Mejora abierta: listeners `maestro:*` en widgets (no bloquea).

| Métrica | Resultado |
|---|---|
| Guiones `maestro-01.json`…`maestro-36.json` | **36/36** |
| Shells largos CSS + JS + `data-maestro-json` | **36/36** |
| Anclas JSON → ids HTML (sistemático) | **0 rotas** |
| Ids duplicados en shells | **0** |
| Embed `data-maestro="guion"` vs JSON externo | **0 drift** |
| `curso` = `1eso-geografia-historia` | **36/36** |
| Intro «modo maestro de Geografía e Historia» | **36/36** |
| `decir` / réplicas `dialogo` ≤3 frases | **0 incumplimientos** |
| Hub CTA → L01 `?maestro=1` | **OK** |
| Runtime JS (`node --check`) | **OK** |
| Críticos | **0** |
| Mejoras | **1** |

---

## Método

1. Inventario: 36 JSON, 36 shells `leccion-NN-*.html` (alias corto fuera de alcance), runtime en `profesor/_maestro/`.
2. Script sistemático: wiring, parse JSON, frases, anclas ↔ `id=`, dups, embed↔JSON, `curso`/`url`/`musica`, intro, CDN, `iframeCmd`.
3. Muestreo profundo JSON+shell: **L01, L05, L12, L18, L24, L31, L36** (+ barrido frases/anclas en las 36).
4. Hub pack: `1eso-geografia-historia/1eso-geografia-historia.html` (no raíz `profesor/`).
5. `node --check` sobre `profesor/_maestro/maestro-runtime.js`.
6. Auto-mapa GeoHist usado solo como focos; hallazgos re-verificados.

---

## 1. Guiones (voz maestro)

- Norma **≤3 frases** por paso: **0 incumplimientos** (máximo = 3).
- Sin relleno / música inventada / meta detectados.
- Intro oral fija en `intro` de las **36**: «modo maestro de Geografía e Historia».
- `musica: false` en las 36; pasos **6–8** (media ≈6,7).
- Muestreo L01/L05/L12/L18/L24/L31/L36: MAPA + escala + TIG; tiempo≠clima / climograma / CyL continental; MAB + Simancas / Atapuerca; polis + Alejandro; romanización CyL (Segovia, Médulas…); mirar–parar–cruzar / espacio público; autoeval + portfolio + hábitos — fiel a `NN.md`, sin inventar saberes.

---

## 2. Anclas JSON ↔ shell

- Cruce automático en las **36**: **ninguna ancla ausente**.
- `#maestro-titulo` + objetivos / explicación / interactivo / cierre / reto; `#maestro-curiosidad`, `#maestro-vida`, `#maestro-ejemplos` cuando el JSON las cita (presentes en el DOM).
- `.marco-interactivo` OK donde se usa.
- Sin `id=` duplicados.

---

## 3. Cableado y runtime

| Pieza | Ruta canónica | Uso en shells |
|---|---|---|
| CSS | `profesor/_maestro/maestro-puntero.css` | `../../_maestro/maestro-puntero.css` · **36/36** |
| JS | `profesor/_maestro/maestro-runtime.js` | `../../_maestro/maestro-runtime.js` · **36/36** |
| Guion | `lecciones/maestro-NN.json` | `data-maestro-json="maestro-NN.json"` · **36/36** |

- Embed `data-maestro="guion"` **alineado** con JSON externo en las 36.
- Atajo `atajo-maestro` → `?maestro=1`: **36/36**.
- Sin CDN / HTTP externo en shells largos.
- `iframeCmd` con tiento: **1 comando por lección** (36 total) — mezcla `maestro:reset` (26) y `maestro:highlight` (10); tipos `maestro:*` válidos.

---

## 4. Glosas (solo lo que pide cada lección)

| Lección | Glosa / mnemónico en guion | En `NN.md` | Veredicto |
|---|---|---|---|
| L01 | MAPA (mide / norte / leyenda / TIG) | sí | **OK** |
| L12 | MAB (museo / archivo / biblioteca) | sí | **OK** |
| L18 | Polis-Alex / POLIS-ALEX | sí | **OK** |
| L24 | Roma-CyL / ROMA-CyL | sí | **OK** |
| L31 | mirar, parar, cruzar | sí (curiosidad / cierre de lección) | **OK** |
| L36 | Sé-por-hab (oral de SE-POR-HAB) | sí (`SE-POR-HAB — SÉ… PORtfolio… HABitos`) | **OK** |

Sin glosas de otras lecciones ni inventadas.

---

## 5. Hub + `?maestro=1`

- Hub: `profesor/1eso-geografia-historia/1eso-geografia-historia.html`.
- CTA **«Modo maestro →»** (`.hub-cta-maestro`) → `lecciones/leccion-01-orientarse-en-el-espacio-mapas-escalas-y-tig.html?maestro=1`.
- Runtime: autoarranque con `?maestro=1`; `node --check` **OK**.

---

## Críticos / mejoras

### Críticos — **0**

Ningún blocker de contenido/voz, frases, anclas, dups, cableado, `curso`, intro, embed drift, CDN u `iframeCmd`.

### Mejoras — **1**

| ID | Ruta | Hallazgo | Acción sugerida |
|---|---|---|---|
| M1 | Widgets `lecciones/lNN-*.html` (GeoHist) | Guion envía `maestro:reset` / `highlight` (1× por lección); iframes pueden ignorarlo aún. | Al tocar mapas/interactivos, añadir listeners `maestro:reset` / `maestro:highlight`. **No reescrito** en esta QA. |

---

## Checklist de éxito

- [x] Guiones L01–L36 presentes y válidos
- [x] Shells largos cablean CSS + JS + `data-maestro-json`
- [x] Anclas del JSON existen; sin ids duplicados
- [x] Intro «modo maestro de Geografía e Historia»; `curso` correcto
- [x] Embed ↔ JSON sin drift; ≤3 frases/paso
- [x] Hub CTA Modo maestro → L01 `?maestro=1`
- [x] `?maestro=1` usable (runtime + JSON)
- [x] Glosas solo las de cada lección
- [x] Ficha escrita en esta ruta
- [x] Sin reescritura de temario ni guiones; sin publish; Mate no reabierto

---

**Firmado:** Revisor ESO · 2026-09-24 Europe/Madrid
