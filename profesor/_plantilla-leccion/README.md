# Plantilla visual de lección (shell Les vencimos)

Chrome compartido para presentaciones HTML offline. Los bots de Mate siguen creando los **interactivos**; este shell solo enmarca el contenido.

**Colores (tema luminoso):** fondo `#FAF7F0` · panel `#FFFFFF` · tinta `#2A2620` · título `#0E0E0C` · suave `#5C564C` · acento `#C4A15A` · verde `#3D6B4F` · azul `#2F5D7A`  
**Restricciones:** sin Google Fonts, sin CDN, tipografía de sistema, `file://` seguro.

## Abrir la demo

1. Abre en el navegador (doble clic o arrastrar):
   - `profesor/_plantilla-leccion/demo-bloques.html`
   - o `profesor/_plantilla-leccion/leccion-shell.html` (mismo demo)
2. Mock de lección 01 con iframes reales:
   - `profesor/1eso-matematicas/lecciones/01-presentacion.html`

Rutas relativas: funciona desde disco o desde el sitio estático.

## Archivos

| Archivo | Uso |
|---|---|
| `leccion-shell.css` | Estilos reutilizables (columna ~60rem, barra sticky) |
| `leccion-shell-nav.js` | Opcional: sincroniza progreso desde `data-actual` / `data-total` |
| `demo-bloques.html` / `leccion-shell.html` | Catálogo visual de bloques |
| `figuras/*.svg` | Mini-gráficos de ejemplo (fuego, olla, mapa, ticket) |
| `README.md` | Esta guía |

## Cómo estructurar cada lección HTML (Mate bots)

Orden recomendado dentro de `<body class="leccion-shell">` → `.leccion-wrap`
(la columna de lectura usa `max-width: ~60rem`; padding horizontal reducido en tablet/desktop):

0. **Barra de navegación (siempre visible):** `.leccion-barra` — sticky arriba
1. **Cabecera** (opcional): `.leccion-top`
2. **Título de lección:** `.bloque-titulo`
   - `.eyebrow` — «Lección 01 · UD0»
   - `h1.titulo-leccion` — titular con carácter (serif); `em` para acento dorado
   - `.meta-leccion` — curso / saberes
3. **Curiosidad histórica** (si hay): `.bloque-curiosidad`
   - `.etiqueta-bloque` → texto «Curiosidad histórica»
   - `.titulo-curiosidad` + `.texto-curiosidad`
   - `.ilustracion-slot` — SVG/img opcional
4. **Cuerpo** (objetivos, explicación, práctica…): `.bloque-cuerpo` (+ `.tarjeta` si hace falta)
5. **En la vida real / aplicaciones:** `.bloque-vida-real.con-figura`
   - `.figura` — gráfico pequeño (SVG inline o `figuras/…`)
   - `.contenido-vida` — título + lista/párrafos
6. **Problema / Interactivo:** `.bloque-interactivo`
   - Cabecera con `.etiqueta-interactivo` y enlace «Abrir en pestaña»
   - `.marco-interactivo` → `<iframe src="l01-….html">` (o embed del widget)
7. **Reto Profesor:** `.bloque-reto`
   - `.etiqueta-reto`, `.titulo-reto`, cuerpo, `.reto-id`
8. **Pie:** `.leccion-pie`

### Clases clave (contrato Mate ↔ Web)

| Bloque | Clase contenedor | Notas |
|---|---|---|
| Barra nav | `.leccion-barra` | Sticky; `data-actual` / `data-total`; calc + prev/next |
| Título | `.bloque-titulo` | No uses un H1 suelto sin esta envoltura |
| Curiosidad histórica | `.bloque-curiosidad` | Panel featured |
| Vida real / apps | `.bloque-vida-real` | Gráfico en `.figura` |
| Interactivo | `.bloque-interactivo` | iframe dentro de `.marco-interactivo` |
| Reto web | `.bloque-reto` | Callout dorado |


### Barra sticky · progreso / calculadora / prev–next

Contrato obligatorio en cada presentación HTML:

```html
<nav class="leccion-barra" aria-label="Navegación de lección"
     data-actual="1" data-total="47">
  <div class="leccion-progreso" role="status">
    <span class="progreso-texto"><strong>1</strong> de <strong>47</strong></span>
    <div class="progreso-pista" aria-hidden="true"><div class="progreso-lleno" style="width:2.13%"></div></div>
  </div>
  <div class="leccion-atajos">
    <a class="atajo atajo-calc" href="../../../modulos/calculadora.html" title="Calculadora">Calculadora</a>
    <a class="atajo atajo-prev" href="…">← Anterior</a>
    <a class="atajo atajo-next" href="…">Siguiente →</a>
  </div>
</nav>
```

Reglas para bots Mate:

| Campo | Quién lo rellena | Notas |
|---|---|---|
| `data-actual` / `data-total` | Mate | Nº de lección y total del curso (p. ej. 1 y 47). |
| `.progreso-lleno` width | Mate o JS | `actual/total × 100%`. Si incluyes `leccion-shell-nav.js`, el script lo calcula solo. |
| `atajo-calc` href | Mate | Ruta relativa a `modulos/calculadora.html`. Desde `…/lecciones/` → `../../../modulos/calculadora.html`. (También existe `calculadora.html` en la raíz del sitio; preferir el módulo.) |
| `atajo-prev` / `atajo-next` | Mate | Hrefs reales a HTML hermano. **No** inventar URLs en el JS. |
| Primera lección | Mate | «Anterior» deshabilitado: `<span class="atajo atajo-prev is-disabled" aria-disabled="true">` (sin enlace muerto). |
| Última lección | Mate | «Siguiente» igual, deshabilitado. |
| Lección aún sin HTML | Mate | Siguiente deshabilitado con `title="Próximamente"`, o stub mínimo «en construcción» con el mismo shell. |

Incluir el script opcional (sin CDN):

```html
<script src="../../_plantilla-leccion/leccion-shell-nav.js" defer></script>
```

(ajusta la profundidad). El JS **solo** lee `data-actual`/`data-total` y actualiza texto + barra; los hrefs prev/next permanecen en el HTML.

### Snippet mínimo

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Lección NN · …</title>
  <link rel="stylesheet" href="../../_plantilla-leccion/leccion-shell.css"/>
</head>
<body class="leccion-shell">
<div class="leccion-wrap">
  <nav class="leccion-barra" aria-label="Navegación de lección"
       data-actual="N" data-total="47">…</nav>
  <header class="bloque-titulo">…</header>
  <aside class="bloque-curiosidad">…</aside>
  <section class="bloque-cuerpo">…</section>
  <section class="bloque-vida-real con-figura">
    <div class="figura">…</div>
    <div class="contenido-vida">…</div>
  </section>
  <section class="bloque-interactivo">
    <div class="marco-interactivo-cabecera">…</div>
    <div class="marco-interactivo">
      <iframe title="…" src="lNN-widget.html" loading="lazy"></iframe>
    </div>
  </section>
  <section class="bloque-reto">…</section>
</div>
</body>
</html>
```

Ajusta la ruta al CSS (y al JS de la barra) según la profundidad del HTML de la lección
(`lecciones/` → `../../_plantilla-leccion/leccion-shell.css` y `leccion-shell-nav.js`).
Columna de lectura: `--lv-max: 60rem` (antes ~46rem); menos padding lateral en tablet/desktop.

## Figuras de ejemplo

Copiar o enlazar desde `figuras/`:

- `fuego.svg` — hoguera / medir el fuego  
- `olla.svg` — cocina  
- `mapa.svg` — camino / mapa  
- `ticket.svg` — importe en €  

Son SVG inline-friendly (fondo crema `#FAF7F0` + oro `#C4A15A`). Se pueden pegar dentro de `.figura` o `.ilustracion-slot`.

## Qué no hacer

- No reescribir los 47 `.md` desde aquí; el shell es para **presentación HTML**.
- No tocar la lógica de los interactivos Mate; solo enmarcarlos.
- No añadir fuentes remotas ni assets de CDN.
- Nunca versionar ni commitear `DNS.txt` desde este trabajo.
