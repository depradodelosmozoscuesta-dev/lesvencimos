# QA Bloque L25–L36 · 1º ESO Geografía e Historia (CyL Decreto 39/2022)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta canónica:** `/workspace/lesvencimos/profesor/1eso-geografia-historia/lecciones/`  
**No escrito en:** `/workspace/lescircimos/` (espejo / typo prohibido)

---

## Criterios comprobados

| Criterio | Estado |
|---|---|
| Offline `file://` (sin CDN / sin imágenes externas) | ✅ SVG/CSS/JS inline |
| Tema crema `#FAF7F0` | ✅ |
| Tonos ~12 años; español primero; CyL cuando el decreto lo pide | ✅ |
| Lecciones densas (~2 pág.): objetivos / explicación / vida / ejemplos / práctica / soluciones / errores / glosario / cierre / reto | ✅ |
| Mapas/líneas/infografías estilo QVALD (sin copiar arte) | ✅ 3R-planeta, alteridad, CDN 1989, igualdad, democracia, antes/ahora, vial, timeline, atlas, fuentes, proyecto, portfolio |
| Honestidad (ONU 1989; 753 a.C. = tradición; SVG didácticos; sin inventar artículos CDN ni listas cerradas de parques) | ✅ |
| **Jorge rule:** respuesta correcta NO siempre 1ª opción | ✅ Posiciones 1ª/2ª/3ª/4ª repartidas (solo 3/12 en 1ª) |
| Feedback quiz alineado tras reordenar | ✅ `ok_msg`/`bad_msg` coherentes |
| Preview PNG Chrome `?preview=1` (1200×1100) | ✅ L25–L36 |
| Path solo `lesvencimos` | ✅ |

---

## Mapa decreto (Bloque C + cierre) → lección

| Viñeta decreto (1º curso, C. Compromiso cívico) / cierre | Lección |
|---|---|
| Conciencia ambiental; cuidado seres vivos y planeta | **L25** |
| Alteridad; no discriminación / no segregación | **L26** |
| Dignidad humana; Convención Derechos del Niño | **L27** |
| Igualdad de género; conductas no sexistas | **L28** |
| Convivencia cívica / democracia; proyectos comunitarios | **L29** |
| Ciclos vitales; tiempo libre; hábitos de consumo (antes/ahora) | **L30** |
| Seguridad vial; movilidad sostenible; espacio público | **L31** |
| Síntesis cronológica Prehistoria→Roma (+ CyL) | **L32** |
| Repaso geográfico multi-escala CyL–España–Europa–mundo | **L33** |
| Mini-investigación con fuentes (guiada) | **L34** |
| Proyecto integrador paisaje local + historia cercana | **L35** |
| Autoevaluación, portfolio, hábitos de ciudadanía | **L36** |

---

## Inventario L25–L36

| L | Título | MD | HTML | Preview | Correcta (quiz) |
|---|---|---|---|---|---|
| 25 | Conciencia ambiental: cuidar el planeta y los seres vivos | `25.md` | `l25-conciencia-ambiental-planeta-seres-vivos.html` | `l25-conciencia-ambiental-planeta-seres-vivos-preview.png` | **2ª** |
| 26 | Alteridad: respeto y rechazo a la discriminación | `26.md` | `l26-alteridad-respeto-no-discriminacion.html` | `l26-alteridad-respeto-no-discriminacion-preview.png` | **3ª** |
| 27 | Dignidad humana y derechos del niño | `27.md` | `l27-dignidad-humana-derechos-nino.html` | `l27-dignidad-humana-derechos-nino-preview.png` | **4ª** |
| 28 | Igualdad de género: conductas no sexistas | `28.md` | `l28-igualdad-genero-conductas-no-sexistas.html` | `l28-igualdad-genero-conductas-no-sexistas-preview.png` | **1ª** |
| 29 | Convivencia democrática y participación ciudadana | `29.md` | `l29-convivencia-democratica-participacion.html` | `l29-convivencia-democratica-participacion-preview.png` | **3ª** |
| 30 | Ciclos vitales, tiempo libre y hábitos de consumo | `30.md` | `l30-ciclos-vitales-tiempo-libre-consumo.html` | `l30-ciclos-vitales-tiempo-libre-consumo-preview.png` | **2ª** |
| 31 | Seguridad vial y espacio público sostenible | `31.md` | `l31-seguridad-vial-espacio-publico.html` | `l31-seguridad-vial-espacio-publico-preview.png` | **4ª** |
| 32 | Línea del tiempo: Prehistoria → Roma (síntesis) | `32.md` | `l32-linea-tiempo-prehistoria-roma.html` | `l32-linea-tiempo-prehistoria-roma-preview.png` | **1ª** |
| 33 | Atlas CyL–España–Europa–mundo | `33.md` | `l33-atlas-interactivo-cyl-espana-europa-mundo.html` | `l33-atlas-interactivo-cyl-espana-europa-mundo-preview.png` | **2ª** |
| 34 | Mini-investigación con fuentes | `34.md` | `l34-mini-investigacion-fuentes.html` | `l34-mini-investigacion-fuentes-preview.png` | **4ª** |
| 35 | Proyecto integrador: paisaje + historia cercana | `35.md` | `l35-proyecto-integrador-paisaje-historia.html` | `l35-proyecto-integrador-paisaje-historia-preview.png` | **3ª** |
| 36 | Autoevaluación, portfolio y hábitos de ciudadanía | `36.md` | `l36-autoevaluacion-portfolio-ciudadania.html` | `l36-autoevaluacion-portfolio-ciudadania-preview.png` | **1ª** |

---

## Checks técnicos rápidos

- [x] `google-chrome --headless --window-size=1200,1100 --screenshot` con `file://…?preview=1` (L25–L36).
- [x] `body.preview-mode` / `.hide-preview` oculta story/quiz/glossary.
- [x] SVG offline; sin fetch externo.
- [x] Quiz: `data-ok` distribuido; feedback JSON coincide con la opción marcada.

---

## Muestreo de honestidad

| Tema | Tratamiento |
|---|---|
| Convención Derechos del Niño | ONU **1989**; pilares didácticos; sin inventar nº de artículo |
| 753 a.C. Roma | **Tradición**, no laboratorio (L32) |
| Atlas / mapas | Esquemas didácticos, no carta oficial |
| Espacios naturales CyL | Se nombra la existencia; listas/normas → fuente oficial |
| Consumo antes/ahora | Sin idealizar el pasado (trabajo infantil, desigualdades) |

---

## Veredicto

**APTO** bloque L25–L36 (12/12 entregadas: MD + HTML offline + preview + glosario + mnemónico; Jorge rule OK).  

**Curso cerrado: 36/36.**
