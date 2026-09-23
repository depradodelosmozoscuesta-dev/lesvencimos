# QA Bloque L01–L10 · 1º ESO Lengua Castellana y Literatura (CyL Decreto 39/2022)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta canónica:** `/workspace/lesvencimos/profesor/1eso-lengua-castellana/lecciones/`  
**No escrito en:** `/workspace/lescircimos/` (espejo prohibido)

---

## Criterios comprobados

| Criterio | Estado |
|---|---|
| Offline `file://` (sin CDN / sin imágenes externas) | ✅ SVG/CSS/JS inline |
| Tema crema `#FAF7F0` | ✅ |
| Tonos ~12 años; español primero; CyL cuando el decreto lo nombra | ✅ |
| MD densas (objetivos, explicación, vida real, ejemplos, práctica, soluciones+porqués, glosario, mnemónico, link interactivo, reto) | ✅ |
| Mapas lenguas de España cuando aplica (L05; esquema didáctico) | ✅ |
| Lenguaje inclusivo respetuoso; sin burlas a acentos/signos | ✅ |
| Marco legal: parafraseo Constitución art. 3 + Estatuto CyL art. 5 (sin citas inventadas) | ✅ L02 |
| Preview PNG Chrome `?preview=1` (1200×1100) | ✅ L01–L10 |
| Solo viñetas del decreto tocadas por cada lección | ✅ ver mapa abajo |
| Respuesta correcta repartida (no sesgo a la 1ª) | ✅ 1ª×2 · 2ª×3 · 3ª×3 · 4ª×2 |

---

## Mapa decreto (Bloque A + inicio B) → lección

| Viñeta decreto (1º curso) | Lección |
|---|---|
| Variantes territoriales. Lenguas, dialectos y hablas | **L01** |
| Marco legal Constitución + Estatuto CyL | **L02** |
| Biografía lingüística + diversidad centro/localidad/CyL | **L03** |
| Familias lingüísticas y lenguas del mundo | **L04** |
| Lenguas de España: origen, distribución; aproximación lengua de signos | **L05** |
| Diferencias plurilingüismo / diversidad dialectal | **L06** |
| Pluralidad como enriquecimiento; prejuicios/estereotipos; lenguaje inclusivo | **L07** |
| Fenómenos: seseo, ceceo, yeísmo, voseo (ejemplos sencillos) | **L08** |
| Variedades del español con especial atención a CyL | **L09** |
| B.1 Hecho comunicativo: elementos; intención; canal *(no verbales → L11)* | **L10** |

---

## Inventario L01–L10

| L | Título | MD | HTML | Preview | Quiz OK en |
|---|---|---|---|---|---|
| 01 | Lenguas, dialectos y hablas | `01.md` | `l01-lenguas-dialectos-hablas.html` | `…-preview.png` | **2ª** |
| 02 | Constitución y Estatuto CyL | `02.md` | `l02-constitucion-estatuto-cyl-marco-linguistico.html` | `…-preview.png` | **3ª** |
| 03 | Biografía lingüística y diversidad CyL | `03.md` | `l03-biografia-linguistica-diversidad-cyl.html` | `…-preview.png` | **1ª** |
| 04 | Familias lingüísticas y lenguas del mundo | `04.md` | `l04-familias-linguisticas-lenguas-mundo.html` | `…-preview.png` | **4ª** |
| 05 | Lenguas de España + signos | `05.md` | `l05-lenguas-espana-origen-mapa-signos.html` | `…-preview.png` | **2ª** |
| 06 | Plurilingüismo vs diversidad dialectal | `06.md` | `l06-plurilinguismo-diversidad-dialectal.html` | `…-preview.png` | **3ª** |
| 07 | Prejuicios y lenguaje inclusivo | `07.md` | `l07-prejuicios-lenguaje-inclusivo.html` | `…-preview.png` | **4ª** |
| 08 | Seseo, ceceo, yeísmo, voseo | `08.md` | `l08-seseo-ceceo-yeismo-voseo.html` | `…-preview.png` | **1ª** |
| 09 | Variedades del español (foco CyL) | `09.md` | `l09-variedades-espanol-castilla-leon.html` | `…-preview.png` | **3ª** |
| 10 | Hecho comunicativo | `10.md` | `l10-hecho-comunicativo-elementos-intencion-canal.html` | `…-preview.png` | **2ª** |

---

## Checks técnicos rápidos

- [x] `google-chrome --headless --window-size=1200,1100 --screenshot` con `file://…?preview=1` (L01–L10).
- [x] Sin `cdn` / `googleapis` / `unpkg` / `jsdelivr`.
- [x] `body.preview-mode` oculta story/quiz/footer según CSS compartido.
- [x] Nada escrito bajo `lescircimos`.

---

## Veredicto

**APTO** — Bloque L01–L10 listo para revisión de Jorge.
