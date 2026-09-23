# QA — Posición de la respuesta correcta (Geografía e Historia · 1º ESO)

**Fecha:** 2026-09-23 (Europe/Madrid)  
**Ámbito:** solo `lesvencimos/profesor/1eso-geografia-historia` (no `lescircimos`; no Mate/ByG)  
**Ruta:** `lecciones/l*.html` (canónicos `lNN-*.html`) + chequeo `NN.md`  
**Objetivo:** eliminar el sesgo «la correcta suele ser la 1ª opción» en quizzes / mini-checks, sin cambiar la corrección curricular (solo el orden de opciones). Feedback/porqués siguen ligados al contenido (por `data-ok`, no por índice).

## Resumen

| Pack | HTML `lNN-*` escaneados | Con MCQ (`data-ok`) | Corregidos (reorden) | Ya en posición objetivo / sin MCQ |
|------|-------------------------|---------------------|----------------------|-----------------------------------|
| 1eso-geografia-historia | 24 | 23 | 15 | 8 ya OK + 1 sin MCQ (`l09`) |

## Distribución (posición del correcto)

### Antes
- **1ª:** 19 · **2ª:** 4  
- Total MCQ: **23**  
- Sesgo claro hacia la **1ª** opción; **0** en 3ª.

### Después
- **1ª:** 8 · **2ª:** 8 · **3ª:** 7  
- Total MCQ: **23**  
- Criterio: posición objetivo = `(N−1) mod 3` (todos los quizzes tienen 3 opciones).

## Archivos corregidos (15)

| Archivo | Antes | Después | Correcta (contenido) |
|---------|-------|---------|----------------------|
| `l01-orientarse-mapas-escalas-tig.html` | **2ª** | **1ª** | 1 cm en el mapa = 100 000 cm = 1 km en la realidad |
| `l03-europa-espana-cyl-relieve-rios.html` | **2ª** | **3ª** | Duero |
| `l05-clima-elementos-factores-graficos.html` | **1ª** | **2ª** | Temperatura y precipitación |
| `l06-emergencia-climatica-riesgos-resiliencia.html` | **2ª** | **3ª** | Prepararse, resistir y recuperarse mejor |
| `l08-ecosistemas-patrimonio-huella-humana.html` | **1ª** | **2ª** | cómo nuestras actividades lo alteran |
| `l11-pensar-geografo-historiador.html` | **1ª** | **2ª** | pregunta de geógrafo (lugar y conexiones), enlazable con historia |
| `l12-fuentes-museos-archivos-bibliotecas.html` | **1ª** | **3ª** | documentos históricos |
| `l14-paleolitico-supervivencia-culturas.html` | **1ª** | **2ª** | nómadas o semimóviles, siguiendo recursos |
| `l15-neolitico-edad-metales.html` | **1ª** | **3ª** | cobre → bronce → hierro |
| `l17-arte-cultura-patrimonio-civilizaciones.html` | **1ª** | **2ª** | es una herencia común que estudiar y cuidar |
| `l18-grecia-polis-alejandro.html` | **1ª** | **3ª** | una ciudad-Estado con su territorio e instituciones |
| `l20-religion-poder-identidades-antiguedad.html` | **1ª** | **2ª** | creer en muchos dioses |
| `l21-invisibilizados-mujeres-esclavos-extranjeros.html` | **1ª** | **3ª** | dejar fuera del relato a grupos enteros |
| `l23-pueblos-prerromanos-hispania-romana.html` | **1ª** | **2ª** | fue un proceso largo y desigual |
| `l24-romanizacion-patrimonio-cyl.html` | **1ª** | **3ª** | un paisaje de minería aurífera romana (UNESCO) |

## Ya en objetivo — sin cambio de orden (8)

| Archivo | Posición | Correcta (contenido) |
|---------|----------|----------------------|
| `l02-continentes-oceanos-mares-rios.html` | **2ª** (ya objetivo) | un mar (conectado al Atlántico por Gibraltar) |
| `l04-fondos-marinos-formas-relieve.html` | **1ª** (ya objetivo) | plataforma continental |
| `l07-zonas-bioclimaticas-biodiversidad.html` | **1ª** (ya objetivo) | la variedad de seres vivos y ecosistemas |
| `l10-ciencias-sociales-objetivos-terminos.html` | **1ª** (ya objetivo) | organizar, compartir y elaborar conocimiento con normas de uso seguro |
| `l13-origen-humano-migraciones.html` | **1ª** (ya objetivo) | África |
| `l16-civilizaciones-rutas-comerciales.html` | **1ª** (ya objetivo) | intercambiar productos y conectar territorios |
| `l19-roma-monarquia-republica-imperio.html` | **1ª** (ya objetivo) | el Mediterráneo controlado por Roma |
| `l22-prehistoria-peninsula-atapuerca.html` | **1ª** (ya objetivo) | Burgos (Castilla y León) |

## Sin MCQ de opciones fijas

- `l09-tic-redes-seguras-lectura-critica.html` — sin botones `data-ok` / lista de opciones.

## `leccion-*.html` (48 archivos)

- `leccion-NN.html` = redirect/alias.  
- `leccion-NN-….html` embebe el laboratorio `lNN-*.html` (iframe).  
- Sin `data-ok` propio → el arreglo en `lNN-*` cubre el interactivo.

## MD (`01.md`–`24.md`)

- Escaneados: **sin** bloques a)/b)/c)/d) con solución siempre a).  
- Práctica = preguntas abiertas + «Soluciones y porqués» numeradas → **sin cambios**.

## Preview PNG

- Opciones con `hide-preview` → **no** se regeneraron PNG.

## Norma

`NORMAS.md` en este pack:

> Respuesta correcta repartida; nunca sesgo a la 1ª opción.
