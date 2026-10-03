# TIC I · 1º Bachillerato · CyL Decreto 40/2022

Curso offline Les vencimos. **NO publicar.** Staging: `/workspace/lesvencimos/staging/bach1/tic/`.
Fuente: BOCyL 30/09/2022 (BOCYL-D-30092022-4), Anexo III, Tecnologías de la Información y la Comunicación, **primer curso** (págs. 50261–50269). Sin inventar currículo. Sin modalidad Artes aparte.
Marca carbón+ámbar. HTML `file://`, sin CDN, sin nube real.

## Offline vs «Cloud» del decreto
El currículo nombra CMS, Cloud Computing y alojamiento web. Aquí se **explican** esos conceptos con rigor, y se **practican** con editores/canvas/simulación **embebidos en la misma página**.  
**UX Jorge Bach:** escribir = editor embebido; dibujar = canvas en la misma página. **NUNCA** saltar a otro módulo.

## Tres bloques oficiales (contenidos A–C)

| Bloque | Nombre oficial |
|--------|----------------|
| A | Proyecto TIC. Publicación y difusión de contenidos |
| B | Digitalización del entorno personal de aprendizaje |
| C | Programación |

Tres competencias específicas (por nombre, en prosa en la meta): (1) generar contenido multimedia / diseño web e interactivos; (2) configurar el entorno personal de aprendizaje; (3) diseñar e implementar programas.

## Archivos por lección NN

En `lecciones/`:
- `leccion-NN-slug.html` — shell completo
- `lNN-slug.html` — laboratorio a pantalla completa (iframe + abrible solo) cuando haya práctica densa
- `maestro-NN.json` — guion maestro alineado

También: `index.html`, `manifest.webmanifest`, `icons/`, `figuras/`, `leccion-shell.css`, `leccion-shell-nav.js`, este `ESQUEMA.md`.

Rutas desde `lecciones/` (como Inglés Bach):
- CSS/nav: `../leccion-shell.css` y `../leccion-shell-nav.js` (copiados en staging)
- Marca: `../../../../index.html` (si existe) o relativo seguro
- Iconos: `../icons/…`

## Listón de calidad (= 1º ESO al máximo)
Cada lección: explicación densa, glosas de lo que hace falta **en esa lección**, diagramas SVG, ejemplos resueltos, vida real CyL cuando encaje, laboratorio embebido (editor o canvas), sección **Comprueba** con 3 preguntas en `<details>` (respuesta + párrafo «Por qué:»), mini cierre, reto, guion maestro. Densidad alta; sin relleno.

## Orden de lecciones (32)

### A · Proyecto TIC (01–12)
01 html-y-estructura-de-una-pagina — HTML semántico; estructura; file://
02 css-basico-y-experiencia-de-usuario — CSS; tipografía; contraste; UX
03 cms-concepto-y-editor-de-pagina — Qué es un CMS; editor embebido tipo página
04 sitio-web-multimedia-offline — Integrar texto+imagen+audio en una página
05 presentaciones-estructura-y-narrativa — Guion, diapositivas, jerarquía (editor embebido)
06 presentaciones-multimedia-offline — Imagen, audio, notas; simulación «nube» local
07 maquetacion-folleto-e-infografia — Folleto/tarjeta/infografía en editor+canvas
08 tipografia-rejilla-y-jerarquia-visual — Rejilla, tipografía, contraste accesible
09 audio-digital-formatos-y-edicion — WAV/MP3/OGG; pistas; editor de timeline simple
10 video-digital-formatos-y-montaje — Contenedores; storyboard; montaje conceptual offline
11 alojamiento-servidores-y-publicacion — Servidor, hosting, DNS (concepto); exportar ZIP local
12 proyecto-tic-integrado — Mini proyecto A: página+presentación+audio (todo embebido)

### B · Entorno personal de aprendizaje (13–22)
13 imagen-bitmap-vs-vectorial — Raster vs vector; cuándo usar cada uno
14 trazos-rellenos-nodos-y-capas — Herramientas 2D; canvas de dibujo vectorial simplificado
15 logotipo-y-marca — Brief; variantes; canvas logotipo
16 alineacion-distribucion-y-filtros — Composición; alineación; capas
17 graficos-3D-conceptos — Ejes, extrusión, texturas (diagrama + canvas isométrico)
18 modelado-basico-y-espacios — Plantillas; componentes; espacio de trabajo 3D conceptual
19 paseo-virtual-y-visualizacion — Cámara, recorrido; storyboard de paseo
20 micromecenazgo-digital — Crowdfunding: fases, recompensas, ética (sin plataforma real)
21 licencias-y-derechos-de-autor — Creative Commons, dominio público, atribución
22 epa-portfolio-offline — Montar EPA: carpetas, portfolio HTML local

### C · Programación (23–32)
23 pensamiento-computacional-y-algoritmos — Entrada/proceso/salida; descomposición
24 diagramas-de-flujo-y-pseudocodigo — Símbolos; canvas de flujo; pseudocódigo en editor
25 variables-tipos-y-operadores — JS embebido seguro; tipos; operadores
26 estructuras-de-control — if/else, while, for; trazas
27 vectores-arrays-y-funciones — Arrays; funciones; parámetros
28 objetos-e-imagenes-multimedia — Objetos literales; canvas/imagen
29 depuracion-y-buenas-practicas — Errores típicos; consola simulada; licencias de código
30 aplicacion-interactiva-ludica — Mini juego/app visual (canvas + JS en página)
31 proyecto-programacion — Proyecto C: app que resuelve un problema definido
32 cierre-portfolio-y-criterios — Repaso A–C; portfolio; autoevaluación criterios 1.x–3.1

L01 anterior → `../index.html`. L32 siguiente → `../index.html`.
Barra: `data-actual="N"` `data-total="32"`. Progreso = round(N/32*100)%.

## Criterios de evaluación (1º) a cubrir
1.1 webs multimedia (CMS/HTML) · 1.2 presentaciones · 1.3 maquetación · 1.4 audio/vídeo  
2.1 logotipos 2D · 2.2 espacios 3D · 2.3 micromecenazgo  
3.1 programas con sintaxis, depuración, multimedia e interactividad (propósito lúdico)

## Cadena
Profesor TIC → Revisor Bach `a8d723de-f137-42a9-a5c8-4937cf349386` → Web `52533bd5-ab62-4c04-9175-ece191bf23f7`.  
Avisos a Web al **50%** y al **cierre** (path + MD5). Staging only.

## Hardware embebido (Jorge 2026-10-03)
En lecciones de E/S digital y programación: ejemplos **Arduino / Raspberry Pi** (GPIO, sensores, sketches) con **toggle ON/OFF embebido** en la misma página (simulación LED/pin HIGH-LOW). No es un bloque curricular inventado: son ejemplos prácticos dentro de A/C. Nunca saltar a otro módulo.
