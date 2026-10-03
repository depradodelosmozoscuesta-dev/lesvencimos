# Inglés I · 1º Bachillerato · CyL Decreto 40/2022

Curso offline Les vencimos. No publicar. No es la materia de Artes.
Nivel: primero de Bachillerato (aprox. B1). No repitas el curso de 1º ESO (saludos, have got, this/that como lección entera).
Explicaciones en español de España. Ejemplos en inglés, correctos. Si un dato (PIB, población, fecha menor) no lo tienes seguro, no lo pongas.

## Saberes (anexo Lengua Extranjera, Decreto 40/2022)

Tres bloques: A Comunicación, B Plurilingüismo, C Interculturalidad.
No inventes criterios numerados (1.1, 1.2). En la meta de la lección cita el bloque y el saber en prosa.
Las seis competencias de la materia, por nombre y sin numerar criterios: comprender; producir; interactuar; mediar; repertorio plurilingüe; diversidad intercultural.

## Archivos por lección NN

En `lecciones/`:

- `leccion-NN-slug.html` — shell de la lección
- `lNN-slug.html` — laboratorio a pantalla completa (iframe y también abrible solo)
- `maestro-NN.json` — el mismo guion que va incrustado en la lección

Slugs y orden (anterior/siguiente usan estos nombres exactos):

01 estrategias-de-comprension-y-produccion
02 autoconfianza-asertividad-y-autorreparacion
03 mediacion-resumir-y-transmitir
04 describir-fenomenos-y-acontecimientos
05 instrucciones-y-consejos
06 narrar-el-pasado
07 presente-futuro-y-predicciones
08 emociones-y-deseos
09 opinion-posibilidad-y-obligacion
10 argumentar
11 reformular-citar-y-resumir
12 generos-discursivos
13 coherencia-cohesion-y-adecuacion
14 entidad-y-propiedades
15 cantidad-y-cualidad
16 espacio-y-relaciones-espaciales
17 tiempo-y-relaciones-temporales
18 afirmacion-negacion-pregunta-y-exclamacion
19 relaciones-logicas
20 lexico-tiempo-espacio-y-procesos
21 lexico-relaciones-educacion-y-trabajo
22 lexico-ciencia-tecnologia-historia-y-cultura
23 enriquecimiento-lexico
24 sonidos-acento-ritmo-y-entonacion
25 alfabeto-fonetico-basico
26 ortografia-y-elementos-graficos
27 conversacion-turnos-aclaraciones-e-ironia
28 colaborar-debatir-y-negociar
29 comunicar-pese-al-nivel
30 comparar-lenguas-para-aprender
31 autoevaluacion-y-coevaluacion
32 metalenguaje
33 origen-y-parentescos-del-ingles
34 ingles-comunicacion-internacional
35 intercambios-con-hablantes
36 cortesia-registros-y-lenguaje-no-verbal
37 diversidad-y-lenguaje-discriminatorio
38 variedades-y-aspectos-socioculturales
39 geopolitica-y-economia-anglofona
40 proyecto-portfolio-y-cierre

L01 anterior → `../index.html`. L40 siguiente → `../index.html`.
Barra: `data-actual="N" data-total="40"`. Ancho de progreso = N/40 en porcentaje entero.

## Rutas desde `lecciones/` (no las cambies)

- CSS: `../../../../profesor/_plantilla-leccion/leccion-shell.css`
- Nav: `../../../../profesor/_plantilla-leccion/leccion-shell-nav.js`
- Puntero: `../../../../profesor/_maestro/maestro-puntero.css`
- Runtime: `../../../../profesor/_maestro/maestro-runtime.js`
- Figura: `../../../../profesor/_plantilla-leccion/figuras/mapa.svg`
- Marca: `../../../../index.html`
- Calculadora: `../../../../modulos/calculadora.html`
- Iconos: `../icons/…` (ya copiados)
- Manifest: `../manifest.webmanifest`

Lee antes de escribir, y copia la estructura (no el contenido de ESO):

- `/workspace/lesvencimos/profesor/1eso-ingles/lecciones/leccion-04-saludar-despedirse-presentar-y-presentarse.html`
- `/workspace/lesvencimos/profesor/1eso-ingles/lecciones/l04-saludar-despedirse-presentar-y-presentarse.html`

No modifiques nada fuera de `staging/bach1/ingles/`.

## Shell

Misma anatomía que la lección 04 de 1º ESO: nav, marca, título, objetivos, explicación, glosas, ejemplos resueltos, vida real en Castilla y León, laboratorio iframe, mini cierre, reto, guion maestro incrustado en `<script type="application/json" data-maestro="guion">`.

Añade, antes del mini cierre, una sección Comprueba con exactamente 3 preguntas. Cada una en un `<details>`: la pregunta visible, y dentro la respuesta y un párrafo que empiece por «Por qué:». Sin red, sin CDN.

`body` con `class="leccion-shell"` y `data-maestro-json="maestro-NN.json"`.
Meta: `1º Bachillerato Lengua Extranjera · Inglés I`.
Eyebrow: `Lección NN · A|B|C · Comunicación|Plurilingüismo|Interculturalidad`.
Título con un `<em>` en la palabra clave, como el modelo.
`reto_id: bach1-ingles-LNN`.

## Qué enseñar (no relleno)

Cada lección enseña UNA cosa usable. Varios `h3`, ejemplos correctos, un error típico de hablantes de español marcado como incorrecto, glosa de cada término que el alumno necesita en ESA lección (no un glosario genérico copiado). Vida real con lugares de Castilla y León (Soria, Burgos, Valladolid, León, Salamanca, Segovia, Ávila, Palencia, Zamora) solo cuando encaje, sin forzarlo en las cuarenta.

Gramática por lección (no la adelantes entera en otra):

01 Planificar antes de leer o escribir: propósito, predicción, subrayar, revisar. Sin gramática nueva.
02 Autorreparación: I mean, sorry, what I meant was; mirar el propio error. Asertividad cortés.
03 Mediación: contar en inglés lo que dijo otra persona en una frase, y al revés en español. Sin estilo indirecto completo (eso es la 11): aquí, transmitir la idea con tus palabras.
04 Presente simple y continuo para describir; there is/are; who/which/that en frases cortas.
05 Imperativo; should/shouldn't; had better; la fórmula If I were you (sin explicar todo el condicional).
06 Past simple y past continuous; used to para hábitos pasados. When/while. No will.
07 Be going to, will para predicciones, presente continuo para planes ya cerrados. En oraciones temporales (when, as soon as) el presente, no will.
08 Feel + adjetivo; would like to; wish + pasado simple para un deseo sobre el presente (I wish I had more time). No mezcles con condicional 3.
09 Can/could/be able to; may/might; must/have to/mustn't frente a don't have to; should. I think / in my opinion.
10 Although, however, on the other hand, because, so. Párrafo: idea, razón, ejemplo.
11 Say/tell con un paso atrás en el tiempo (said that she was). According to. In other words. Resumir un texto corto. No reported questions.
12 Correo informal y correo formal (saludo, cierre, contracciones sí/no). Artículo breve. Reseña de pocas líneas. Registro.
13 Frase temática, referencia (this, they), conectores, adecuar el tono al lector.
14 A/an/the y artículo cero en usos claros de Bach (the + instrumento de música no hace falta). Orden básico del adjetivo. Comparativo y superlativo, incluyendo irregular good/bad/far.
15 Much/many/a lot of/(a) few/(a) little; some/any; too/enough.
16 Preposiciones de lugar y de movimiento. Where en una frase relativa corta.
17 Elegir tiempo según el marcador. When/while/until/as soon as.
18 Negación, preguntas, question tags con el caso fácil (is/are/do/did/can). What a… / How + adjetivo.
19 Because, so, so that, in order to, although, despite + sustantivo.
20 Léxico y colocaciones de tiempo, espacio, estados, acontecimientos y procesos. Poco gramática: solo la que sujeta el vocabulario.
21 Educación, trabajo, emprendimiento. Frases de un correo o de un CV corto. Sin datos laborales inventados de España.
22 Ciencia, tecnología, historia y cultura como VOCABULARIO para hablar de un invento, un hecho o una película. No es un curso de Artes ni de Historia.
23 Prefijos y sufijos frecuentes, compuestos, familias, sinónimos, antónimos, una polisemia clara (run, light, o la que elijas y expliques bien).
24 Acento de palabra, schwa, terminación -ed /t/ /d/ /ɪd/, entonación de pregunta sí/no frente a pregunta con partícula. Sin audio de red: describe y contrasta con ejemplos escritos.
25 Símbolos que un alumno de primero confunde: /iː/ e /ɪ/, /æ/ y /ʌ/, /θ/ y /ð/, /ʃ/ y /tʃ/. Sheep/ship y think/this. No un cuadro IPA vacío.
26 Ortografía útil: mayúsculas, coma y punto, apóstrofo de contracción frente a posesivo, duplicar consonante en stopped. Elementos gráficos: título, párrafo, lista.
27 Abrir, mantener y cerrar; pedir la palabra; Could you say that again?; ironía fácil (Yeah, right) frente a lectura literal. No jerga.
28 Agreeing and disagreeing con cortesía; negociar un significado; frases de un proyecto en común, también por escrito (foro o aula virtual descritos, sin herramientas online).
29 Circunlocución: definir la palabra que no sabes. What do you call…? It's a thing you use to…
30 Cognados y falsos amigos seguros: actually, eventually, library, sensible, embarrassed, constipated si lo usas con cuidado y claro. Orden de palabras ES/EN en una frase simple.
31 Lista de «sé hacer» de este curso, diario de errores, frases para comentar el texto de un compañero sin humillar.
32 Metalenguaje mínimo: noun, verb, adjective, tense, clause, collocation, register, false friend. Sirve para hablar de cómo aprendes, no para analizar oraciones largas.
33 Núcleo germánico (house, water, strong) frente a préstamos latinos o franceses (university, information, government). Por qué a veces el inglés se parece al español y a veces no. Sin etimologías dudosas: si dudas, no la pongas.
34 El inglés como lengua franca, no solo Reino Unido y Estados Unidos. Participar sin corregir el acento de otros.
35 Escribir un mensaje de intercambio: presentarse a este nivel, preguntar, no estereotipar.
36 Could you… frente a un imperativo seco; registros formal e informal; gestos y temas que no viajan igual (edad, dinero, cola). Sin anécdotas inventadas como si fueran datos.
37 Detectar un estereotipo o un uso excluyente en un texto corto original tuyo, y proponer otra formulación. Valores democráticos y ecosociales en una viñeta, sin sermón.
38 Diferencias que importan en uso: flat/apartment, holiday/vacation, have got/have, colour/color, -our/-or. Costumbres e instituciones en términos de libro de texto, sin cifras.
39 Países donde el inglés es lengua oficial o vehicular (Reino Unido, Irlanda, Estados Unidos, Canadá, Australia, y el hecho de que también lo es en la India o Nigeria, sin reducirlos a una capital). Economía y geopolítica en prosa general. Cero cifras que no puedas sostener: mejor ninguna.
40 Proyecto: un dosier corto que junte un correo, un párrafo de opinión y un resumen de lo que dijo otra persona. Portfolio: qué sabe hacer el alumno al final, sin nota falsa ni «aprobado».

## Laboratorio

Una página HTML autónoma, en español la interfaz y en inglés los ítems. Unos 6 u 8 ítems de la lección, corrección al momento, botones, funciona en iframe y a pantalla completa, sin red y sin librerías. Lee el laboratorio de la lección 04 de ESO y quédate con la idea, no con sus frases de primero de ESO.

## Maestro

JSON con curso `bach1-ingles`, número de lección, titulo, url del shell, musica false, y pasos que recorren titulo, objetivos, explicacion, glosas, ejemplos, vida, interactivo, comprueba, cierre y reto. Cada `decir` es una frase hablada en español, concreta, no un resumen vago. incrusta el mismo JSON en la lección.

## Prohibido

Inventario de relleno, copiar párrafos de un libro, CDN, formularios que envían a internet, publicar, tocar `profesor/1eso-ingles`, y una lección titulada Artes.

## Listón (pedido 2026-10-03, entrega domingo 4 oct 10:00 Madrid)

Igual que el laboratorio de 1º ESO Inglés en su versión completa, no una ficha corta.

Lee de verdad el laboratorio modelo (CSS, escena SVG, rondas con why, mini-check):
`/workspace/lesvencimos/profesor/1eso-ingles/lecciones/l04-saludar-despedirse-presentar-y-presentarse.html`
y, para ver más escenas SVG, las funciones `drawVisual` de
`/workspace/lesvencimos/profesor/1eso-ingles/lecciones/l06-comparar-personas-y-objetos.html` o la que tengas a mano en esa carpeta.

Cada `lNN-….html`:
- CSS propio carbón `#0E0E0C` / `#2A2620` y ámbar `#C4A15A`, fondo `#FAF7F0`. Sin CDN.
- Escena `.stage` con SVG inline que cambia según el ítem (no un único dibujo decorativo).
- Avatar o viñeta SVG en la historia.
- Rondas (6–8) con 4 opciones y `why` en español que explica el fallo, no solo «incorrecto».
- Mini-check aparte (4 preguntas) también con porqué.
- Glosario de la lección al pie.

Cada `leccion-NN-….html`, más densa que una ficha:
- En Ejemplos resueltos, al menos 2 ejemplos desarrollados paso a paso (paso 1, paso 2, paso 3), no una frase suelta.
- Una figura SVG inline en la explicación o en la vida real, hecha para ESA lección (línea de tiempos, contraste, esquema de párrafo, mapa mudo sin cifras inventadas). `aria` con texto. Sin imágenes de red.
- Las 3 preguntas de Comprueba llevan porqué real.
- Decreto 40/2022: no atribuyas al decreto una frase que no esté en el saber de ESQUEMA.md. No numeres criterios.

Si ya escribiste una lección por debajo de esto, reescríbela antes de dar por terminado. No escatimes.

## UX Bach (regla Jorge, aplicar ya)

Escribir se hace en un editor embebido en la propia lección (textarea o zona editable, en la misma página). Dibujar se hace en un `<canvas>` de la misma página. Nunca un enlace a Tinta, Dibujo ni a otro módulo (tampoco a la calculadora ni a `modulos/`). El reto de escribir o dibujar se resuelve ahí mismo, sin salir. Lo que el alumno escriba puede quedarse en la página (o en localStorage de esa lección); no se envía a ninguna red. No copies el atajo «Calculadora» del shell de 1º ESO.
