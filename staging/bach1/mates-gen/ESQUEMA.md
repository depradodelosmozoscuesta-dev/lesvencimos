# Matemáticas Generales · 1º Bachillerato · Modalidad General · CyL Decreto 40/2022

Curso offline Les vencimos. **Staging only — NO publicar.**
Path: `/workspace/lesvencimos/staging/bach1/mates-gen/`
Fuente: Decreto 40/2022 Anexo III, Matemáticas Generales (BOCyL 30/09/2022, extracto págs. ~50126–50128). Contenidos A–F CyL (incluye matrices, combinatoria, límite introductorio, Bayes).
**Sin modalidad Artes.** Cadena: Revisor Bach `a8d723de-f137-42a9-a5c8-4937cf349386` → Web `52533bd5-ab62-4c04-9175-ece191bf23f7`.
Entrega objetivo: domingo 4 oct 2026, 10:00 Europe/Madrid.
Listón: densidad máxima tipo 1º ESO Mate (lección completa + laboratorio + Comprueba×3 con «Por qué:» + gráficos SVG/canvas + ejemplos paso a paso).

## Marca y shell

- Carbón + ámbar local: `leccion-shell.css` en esta carpeta (`#0E0E0C` / `#C4A15A` / tinta `#E6E1D6`). file://, sin CDN, sin Google Fonts.
- Anatomía: nav sticky, marca, título con `<em>`, objetivos, explicación, glosas, ejemplos resueltos, vida real CyL si encaja, laboratorio (iframe hermano **o** widget embebido), editor/canvas en página, Comprueba (3× `<details>` con Por qué), mini cierre, reto, guion maestro JSON incrustado.
- Meta: `1º Bachillerato Matemáticas Generales`.
- Eyebrow: `Lección NN · A|B|C|D|E|F · <nombre bloque>`.
- `reto_id: bach1-mates-gen-LNN`. `data-total="38"`.

## UX Jorge (obligatorio)

- **Escribir** = `<textarea>` / editor embebido en la misma lección.
- **Dibujar** = `<canvas>` en la misma página (grafos, rectas, regiones PL, etc.).
- **NUNCA** saltar a otro módulo para escribir o dibujar. La calculadora de la barra nav sí puede quedar como atajo (no sustituye el trabajo de la lección).

## Archivos por lección NN

En `lecciones/`:

- `leccion-NN-slug.html` — shell
- `lNN-slug.html` — laboratorio a pantalla completa (cuando el interactivo sea complejo; si cabe en página, embeber y omitir iframe)
- `maestro-NN.json` — mismo guion que el `<script type="application/json" data-maestro="guion">`

L01 anterior → `../index.html`. L38 siguiente → `../index.html`.

## Rutas desde `lecciones/`

- CSS: `../leccion-shell.css` (carbón+ámbar de este pack)
- Nav: `../leccion-shell-nav.js` (copia de plantilla)
- Puntero/runtime maestro: `../../../../profesor/_maestro/maestro-puntero.css` + `maestro-runtime.js`
- Figuras: `../../../../profesor/_plantilla-leccion/figuras/…` o SVG inline
- Marca: `../../../../index.html`
- Calculadora (atajo barra): `../../../../modulos/calculadora.html`
- Iconos: `../icons/…`
- Manifest: `../manifest.webmanifest`

## Temario (38 lecciones) — cobertura 100 % saberes CyL

| L | Archivo | Bloque | Contenido oficial que cubre |
|---|---------|--------|------------------------------|
| 01 | leccion-01-que-son-matematicas-generales.html | F/A | Presentación materia; mapa de sentidos; error como aprendizaje |
| 02 | leccion-02-conteo-principios-basicos.html | A.1 | Comparación, adición, multiplicación y división para cardinales |
| 03 | leccion-03-palomar-e-inclusion-exclusion.html | A.1 | Principio del palomar; inclusión-exclusión |
| 04 | leccion-04-arboles-y-combinatoria.html | A.1 | Diagramas de árbol; técnicas de combinatoria |
| 05 | leccion-05-documentos-numericos-cotidianos.html | A.2 | Tablas, diagramas, facturas, nóminas, noticias |
| 06 | leccion-06-potencias-raices-logaritmos.html | A.2 | Potencias, raíces y logaritmos en problemas |
| 07 | leccion-07-matrices-clasificacion-operaciones.html | A.2 | Matrices: clasificación y operaciones |
| 08 | leccion-08-matrices-tablas-y-grafos.html | A.2 | Matrices como herramienta en tablas y grafos |
| 09 | leccion-09-razones-proporciones-porcentajes.html | A.3 | Razones, proporciones, porcentajes y tasas |
| 10 | leccion-10-educacion-financiera.html | A.4 | Intereses, cuotas, comisiones, cambios de divisas |
| 11 | leccion-11-probabilidad-como-medida.html | B.1 | Probabilidad como medida de incertidumbre |
| 12 | leccion-12-variacion-absoluta-y-media.html | B.2 | Variación absoluta y variación media |
| 13 | leccion-13-limite-idea-de-cambio.html | B.2 | Límite desde la variación media (intro a derivada) |
| 14 | leccion-14-derivada-concepto-e-interpretacion.html | B.2 | Concepto de derivada; análisis e interpretación |
| 15 | leccion-15-grafos-tipos-y-representacion.html | C.1 | Grafos dirigidos, planos, ponderados, árboles |
| 16 | leccion-16-euler-y-grafos-planos.html | C.1 | Fórmula de Euler; grafos planos |
| 17 | leccion-17-eulerianos-hamiltonianos-coloracion.html | C.1 | Caminos/circuitos eulerianos y hamiltonianos; coloración |
| 18 | leccion-18-camino-minimo.html | C.1 | Problema del camino mínimo en contextos |
| 19 | leccion-19-patrones-y-generalizacion.html | D.1 | Generalización de patrones |
| 20 | leccion-20-funciones-afines.html | D.2/D.4 | Funciones afines; modelización; propiedades |
| 21 | leccion-21-funciones-cuadraticas.html | D.2/D.4 | Funciones cuadráticas; modelización; propiedades |
| 22 | leccion-22-racionales-trozos-periodicas.html | D.2/D.4 | Racionales sencillas, a trozos y periódicas |
| 23 | leccion-23-exponenciales-y-logaritmicas.html | D.2/D.4 | Exponenciales y logarítmicas; propiedades |
| 24 | leccion-24-sistemas-de-ecuaciones.html | D.3 | Sistemas de ecuaciones en contextos |
| 25 | leccion-25-inecuaciones-y-sistemas.html | D.3 | Inecuaciones y sistemas de inecuaciones |
| 26 | leccion-26-programacion-lineal.html | D.2 | Programación lineal: modelización y resolución |
| 27 | leccion-27-pensamiento-computacional.html | D.5 | Algoritmos, programas y herramientas (offline) |
| 28 | leccion-28-estadistica-interpretacion.html | E.1 | Interpretación y análisis de información estadística |
| 29 | leccion-29-variables-bidimensionales.html | E.1 | Distribución conjunta, marginales, condicionadas; dependencia |
| 30 | leccion-30-regresion-correlacion-causalidad.html | E.1 | Regresión lineal/cuadrática; correlación ≠ causalidad |
| 31 | leccion-31-coeficientes-prediccion.html | E.1 | r y R²; predicción y fiabilidad |
| 32 | leccion-32-probabilidad-compuesta-condicionada.html | E.2 | Simples/compuestos; condicionada; independencia; árbol; contingencia |
| 33 | leccion-33-probabilidad-total-y-bayes.html | E.2 | Teorema de la probabilidad total; Bayes |
| 34 | leccion-34-uniforme-binomial-normal.html | E.3 | Uniforme (disc./cont.), binomial y normal |
| 35 | leccion-35-muestreo-e-inferencia.html | E.4 | Muestras, muestreo, validez, diseño de estudios |
| 36 | leccion-36-emociones-error-y-equipo.html | F.1/F.2 | Autoconciencia, error, decisiones, trabajo en equipo |
| 37 | leccion-37-inclusion-historia-matematicas.html | F.3 | Comunicación efectiva; aportación histórica |
| 38 | leccion-38-proyecto-integrador-cierre.html | A–F | Proyecto integrador + portfolio de cierre |

## Densidad por lección (no escatimar)

1. Objetivos claros (3–5).
2. Explicación lenta con glosas de **cada** símbolo/dato de esa lección.
3. ≥2 ejemplos resueltos paso a paso (castellano bajo cada operación).
4. Gráfico SVG o canvas cuando el saber lo pida (grafos, funciones, regiones, rectas de regresión…).
5. Laboratorio usable offline (iframe hermano o embebido).
6. Editor o canvas en página si la tarea es escribir/dibujar.
7. Comprueba: 3 preguntas en `<details>` con respuesta + párrafo «Por qué:…».
8. Mini cierre + Reto Profesor concreto.
9. Guion maestro ≤3 frases/paso, multi-voz si aporta.

## Hitos

- 50 %: L01–L19 listas + hub `index.html` → avisar Web (path + MD5 parcial).
- 100 %: L01–L38 + labs + maestros + manifest → auto-revisar, ampliar, mejorar → avisar Web (path + MD5) → pasar a Revisor Bach.
