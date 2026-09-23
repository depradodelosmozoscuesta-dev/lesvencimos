# Plantilla visual de lección (shell Les vencimos)

Chrome compartido para presentaciones HTML offline. Los bots de Mate siguen creando los **interactivos**; este shell solo enmarca el contenido.

**Colores:** charcoal `#0E0E0C` · acento `#C4A15A` · crema `#F2EDE3`  
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
| `leccion-shell.css` | Estilos reutilizables |
| `demo-bloques.html` / `leccion-shell.html` | Catálogo visual de bloques |
| `figuras/*.svg` | Mini-gráficos de ejemplo (fuego, olla, mapa, ticket) |
| `README.md` | Esta guía |

## Cómo estructurar cada lección HTML (Mate bots)

Orden recomendado dentro de `<body class="leccion-shell">` → `.leccion-wrap`:

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
| Título | `.bloque-titulo` | No uses un H1 suelto sin esta envoltura |
| Curiosidad histórica | `.bloque-curiosidad` | Panel featured |
| Vida real / apps | `.bloque-vida-real` | Gráfico en `.figura` |
| Interactivo | `.bloque-interactivo` | iframe dentro de `.marco-interactivo` |
| Reto web | `.bloque-reto` | Callout dorado |

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

Ajusta la ruta al CSS según la profundidad del HTML de la lección
(`lecciones/` → `../../_plantilla-leccion/leccion-shell.css`).

## Figuras de ejemplo

Copiar o enlazar desde `figuras/`:

- `fuego.svg` — hoguera / medir el fuego  
- `olla.svg` — cocina  
- `mapa.svg` — camino / mapa  
- `ticket.svg` — importe en €  

Son SVG inline-friendly (palette charcoal/oro/crema). Se pueden pegar dentro de `.figura` o `.ilustracion-slot`.

## Qué no hacer

- No reescribir los 47 `.md` desde aquí; el shell es para **presentación HTML**.
- No tocar la lógica de los interactivos Mate; solo enmarcarlos.
- No añadir fuentes remotas ni assets de CDN.
- Nunca versionar ni commitear `DNS.txt` desde este trabajo.
