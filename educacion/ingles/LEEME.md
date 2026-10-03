# Inglés I · 1º Bachillerato

**Qué es.** Curso offline de Lengua Extranjera, **Inglés I**, de primero de Bachillerato, según el currículo de Castilla y León (**Decreto 40/2022**). Trae las lecciones **01–40**. **No es Francés. No es Artes.**

**Cómo abrirlo.** Descomprime el ZIP si llega comprimido. Entra en la **carpeta descomprimida** (Archivos o el explorador de archivos, no la lista de Descargas del navegador). Abre `ABRE-AQUI.html` o `index.html`.

La dirección tiene que ser `file://`. **No** abras el HTML desde la lista de Descargas: esa ruta es `content://` y entonces fallan el estilo, los iconos y las lecciones.

No hace falta instalar nada ni tener red. No publiques esta carpeta: es material de trabajo en local.

**Contenido.** `index.html` enlaza las cuarenta lecciones en `lecciones/leccion-01-….html` … `leccion-40-….html`, con su laboratorio y su guion de maestro. Identidad: Inglés I, no Francés ni Artes.

SELLO: 2026-10-03 01:24 CEST
MD5: 96874172c737f2f3e65268801de016fe
Ese MD5 es el de los contenidos, no el de la lista de nombres. Desde esta carpeta, sin incluir este LEEME ni ESQUEMA.md:
find . -type f ! -name LEEME.md ! -name ESQUEMA.md -print0 | sort -z | xargs -0 md5sum | md5sum
