#!/usr/bin/env python3
"""Build cream hub + flat offline pack for 1º ESO EPVA (Plástica) curso completo 31/31.

Does NOT rewrite pedagogical lesson bodies. Packages existing shells, embeds
Tinta practice widgets via srcdoc for Android file://, and wires site listings.
"""
from __future__ import annotations

import html
import pathlib
import re
import shutil
import zipfile

REPO = pathlib.Path("/workspace/lesvencimos")
COURSE_DIR = REPO / "profesor/1eso-plastica-visual"
LEC = COURSE_DIR / "lecciones"
PLANTILLA = REPO / "profesor/_plantilla-leccion"
HUB = COURSE_DIR / "1eso-plastica-visual.html"
DESCARGAS = REPO / "descargas.html"
DESCARGAS_PROF = REPO / "descargas-profesor.html"
INDEX = REPO / "index.html"
PACK_DIR = REPO / "downloads/_build-1eso-plastica-flat"
ZIP_PATH = REPO / "downloads/1eso-plastica-visual-offline.zip"
BRAND_ICONS = REPO / "brand/favicon"
COURSE_ICONS = COURSE_DIR / "icons"
TINTA = REPO / "modulos/tinta-estudio.html"
CALC = REPO / "modulos/calculadora.html"

TOTAL = 31
AVAILABLE = 31

COURSE_NAME = "1º ESO Educación Plástica, Visual y Audiovisual"
COURSE_SHORT = "1º ESO Plástica"
ZIP_FOLDER = "1eso-plastica-visual-offline"
HUB_BASENAME = "1eso-plastica-visual.html"
ZIP_BASENAME = "1eso-plastica-visual-offline.zip"
ARTICLE_NUM = "08e"

TEMARIO = [
    "Patrimonio: proteger y conservar el legado",
    "Géneros y estilos artísticos",
    "Manifestaciones artísticas y patrimonio de Castilla y León",
    "Formas geométricas en el arte, el entorno y el patrimonio arquitectónico",
    "El lenguaje visual como comunicación",
    "Punto, línea y plano",
    "La forma: tipos y relaciones en el plano y en el espacio",
    "Color: conceptos y posibilidades expresivas",
    "Textura: conceptos y posibilidades expresivas",
    "Percepción visual, espacio, luz y sombras",
    "Transformaciones gráfico-plásticas",
    "Composición I: formato, encuadre y estructuras",
    "Composición II: equilibrio, proporción y ritmo",
    "El proceso creativo: seis etapas",
    "Operaciones plásticas: reproducir, aislar, transformar, asociar",
    "Instrumentos y materiales de dibujo técnico",
    "Geometría plana: lugares y trazados básicos",
    "Figuras planas y polígonos: clasificación y construcción",
    "Proporcionalidad, Tales, igualdad, semejanza y escalas",
    "Movimientos en el plano: simetrías y traslaciones",
    "Técnicas secas en dos dimensiones",
    "Técnicas húmedas en dos dimensiones",
    "Soportes físicos y digitales",
    "Comunicación visual: finalidades, elementos, contextos y funciones",
    "Realismo, figuración y abstracción",
    "Lenguaje visual en prensa, publicidad, TV, diseño y TIC",
    "Fotografía: imagen fija",
    "Cómic: características y práctica",
    "Cine, animación y formatos digitales",
    "Técnicas expositivas básicas (presenciales y virtuales)",
    "Proyecto de curso: del boceto a la exposición",
]

LESSON_FILES = {
    1: "leccion-01-patrimonio-proteger-y-conservar-el-legado.html",
    2: "leccion-02-generos-y-estilos-artisticos.html",
    3: "leccion-03-manifestaciones-artisticas-y-patrimonio-de-castilla-y-leon.html",
    4: "leccion-04-formas-geometricas-en-el-arte-el-entorno-y-el-patrimonio-arquitectonico.html",
    5: "leccion-05-el-lenguaje-visual-como-comunicacion.html",
    6: "leccion-06-punto-linea-y-plano.html",
    7: "leccion-07-la-forma-tipos-y-relaciones.html",
    8: "leccion-08-color-conceptos-y-posibilidades-expresivas.html",
    9: "leccion-09-textura-conceptos-y-posibilidades-expresivas.html",
    10: "leccion-10-percepcion-visual-espacio-luz-y-sombras.html",
    11: "leccion-11-transformaciones-grafico-plasticas.html",
    12: "leccion-12-composicion-i-formato-encuadre-y-estructuras.html",
    13: "leccion-13-composicion-ii-equilibrio-proporcion-y-ritmo.html",
    14: "leccion-14-el-proceso-creativo-seis-etapas.html",
    15: "leccion-15-operaciones-plasticas-reproducir-aislar-transformar-asociar.html",
    16: "leccion-16-instrumentos-y-materiales-de-dibujo-tecnico.html",
    17: "leccion-17-geometria-plana-lugares-y-trazados-basicos.html",
    18: "leccion-18-figuras-planas-y-poligonos-clasificacion-y-construccion.html",
    19: "leccion-19-proporcionalidad-tales-igualdad-semejanza-y-escalas.html",
    20: "leccion-20-movimientos-en-el-plano-simetrias-y-traslaciones.html",
    21: "leccion-21-tecnicas-secas-en-dos-dimensiones.html",
    22: "leccion-22-tecnicas-humedas-en-dos-dimensiones.html",
    23: "leccion-23-soportes-fisicos-y-digitales.html",
    24: "leccion-24-comunicacion-visual-finalidades-elementos-contextos-y-funciones.html",
    25: "leccion-25-realismo-figuracion-y-abstraccion.html",
    26: "leccion-26-lenguaje-visual-en-prensa-publicidad-tv-diseno-y-tic.html",
    27: "leccion-27-fotografia-imagen-fija.html",
    28: "leccion-28-comic-caracteristicas-y-practica.html",
    29: "leccion-29-cine-animacion-y-formatos-digitales.html",
    30: "leccion-30-tecnicas-expositivas-basicas-presenciales-y-virtuales.html",
    31: "leccion-31-proyecto-de-curso-del-boceto-a-la-exposicion.html",
}

WIDGET_FILES = {
    6: "l06-punto-linea-plano.html",
    7: "l07-formas-y-relaciones.html",
    8: "l08-color.html",
    9: "l09-textura.html",
    10: "l10-luz-sombra-profundidad.html",
    11: "l11-transformaciones.html",
    12: "l12-composicion-formato.html",
    13: "l13-composicion-equilibrio.html",
    15: "l15-operaciones-plasticas.html",
    20: "l20-simetrias-traslaciones.html",
    21: "l21-tecnicas-secas.html",
    22: "l22-tecnicas-humedas.html",
    23: "l23-soportes.html",
    25: "l25-realismo-abstraccion.html",
    27: "l27-fotografia.html",
    28: "l28-comic.html",
    31: "l31-proyecto-curso.html",
}

HUB_STYLES = """
  .hub-hero {
    margin: 0 0 1.75rem;
    padding: 1.5rem 1.35rem 1.6rem;
    background:
      linear-gradient(135deg, rgba(196, 161, 90, 0.12), transparent 55%),
      var(--lv-panel);
    border: 1px solid var(--lv-linea);
    border-left: 3px solid var(--lv-acento);
    border-radius: var(--lv-radio-card);
    box-shadow: var(--lv-sombra);
  }
  .hub-hero h1 {
    margin: 0 0 0.55rem;
    font-family: var(--lv-serif);
    font-size: clamp(1.55rem, 4vw, 2.1rem);
    font-weight: 600;
    color: var(--lv-titulo);
    line-height: 1.2;
  }
  .hub-hero .hub-status {
    margin: 0 0 1.1rem;
    color: var(--lv-suave);
    font-size: 1rem;
    max-width: 40rem;
  }
  .hub-cta {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1.15rem;
    font-size: 1.02rem;
    font-weight: 650;
    text-decoration: none;
    color: var(--lv-acento-texto);
    background: var(--lv-acento);
    border: 1px solid #b08d45;
    border-radius: var(--lv-radio);
    box-shadow: var(--lv-sombra);
  }
  .hub-cta:hover {
    color: var(--lv-acento-texto);
    filter: brightness(1.05);
  }

  .hub-cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
    align-items: center;
  }
  .hub-cta-maestro {
    background: transparent;
    color: var(--lv-titulo);
    border: 1px solid var(--lv-acento);
  }
  .hub-cta-maestro:hover {
    background: rgba(196, 161, 90, 0.12);
    color: var(--lv-titulo);
    filter: none;
  }
  .hub-nota {
    margin: 1.25rem 0 0.5rem;
    font-size: 0.92rem;
    color: var(--lv-suave);
  }
  .hub-lista {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    gap: 0.45rem;
  }
  .hub-item {
    display: grid;
    grid-template-columns: 2.5rem 1fr auto;
    gap: 0.65rem 0.85rem;
    align-items: baseline;
    padding: 0.65rem 0.85rem;
    background: var(--lv-panel);
    border: 1px solid var(--lv-linea);
    border-radius: var(--lv-radio);
  }
  .hub-item a {
    display: contents;
    text-decoration: none;
    color: inherit;
  }
  .hub-item.hub-disponible {
    border-color: rgba(196, 161, 90, 0.45);
    background: var(--lv-panel-soft);
  }
  .hub-item.hub-disponible:hover {
    border-color: var(--lv-acento);
  }
  .hub-item.hub-pronto {
    opacity: 0.78;
  }
  .hub-num {
    font-weight: 700;
    color: var(--lv-acento);
    font-variant-numeric: tabular-nums;
  }
  .hub-titulo {
    color: var(--lv-texto);
  }
  .hub-estado {
    font-size: 0.82rem;
    color: var(--lv-suave);
    justify-self: end;
  }
  .hub-item.hub-disponible .hub-estado {
    color: #2f6b4f;
    font-weight: 600;
  }
  .hub-pie-nota {
    margin: 1.5rem 0 0;
    font-size: 0.88rem;
    color: var(--lv-suave);
  }
"""


def lesson_filename(n: int) -> str:
    return LESSON_FILES[n]


def pack_ud_blurb(*, short: bool = False) -> str:
    if short:
        return "curso completo EPVA 1º CyL"
    return "temario completo EPVA 1º CyL (patrimonio, lenguaje visual, geometría, técnicas, medios)"


def pack_interactivos_blurb() -> str:
    return (
        "Tinta Estudio en L06–L13, L15, L20–L23, L25, L27, L28 y L31; "
        "resto de lecciones sin widget Tinta (enlace opcional donde aplique)"
    )


def is_complete() -> bool:
    return AVAILABLE >= TOTAL


def srcdoc_escape(doc: str) -> str:
    return (
        doc.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
    )


_EXTERNAL_URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.I)
_EXTERNAL_OK = ("w3.org", "www.w3.org", "xmlns", "schema.org", "schemas.xmlsoap")


def assert_offline_safe(fname: str, doc: str) -> None:
    bad = []
    for url in sorted(set(_EXTERNAL_URL_RE.findall(doc))):
        if any(ok in url for ok in _EXTERNAL_OK):
            continue
        bad.append(url)
    if bad:
        raise SystemExit(
            f"{fname} has network URL(s) that break offline: {', '.join(bad[:8])}"
        )


def write_redirect(path: pathlib.Path, target: str, label: str) -> None:
    path.write_text(
        f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta http-equiv="refresh" content="0; url={html.escape(target, quote=True)}"/>
<title>{html.escape(label)} · redirección</title>
<link rel="canonical" href="{html.escape(target, quote=True)}"/>
</head>
<body>
<p><a href="{html.escape(target, quote=True)}">Abrir {html.escape(label)} →</a></p>
</body>
</html>
""",
        encoding="utf-8",
    )


def manifest_text(*, offline: bool = False) -> str:
    start = "./index.html" if offline else f"./{HUB_BASENAME}"
    return f"""{{
  "name": "{COURSE_NAME} · Les vencimos",
  "short_name": "{COURSE_SHORT}",
  "start_url": "{start}",
  "scope": "./",
  "display": "standalone",
  "theme_color": "#FAF7F0",
  "background_color": "#FAF7F0",
  "accent_color": "#C4A15A",
  "icons": [
    {{"src": "icons/favicon.svg", "sizes": "any", "type": "image/svg+xml"}},
    {{"src": "icons/favicon-32.png", "sizes": "32x32", "type": "image/png"}},
    {{"src": "icons/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}},
    {{"src": "icons/app-icon-512.png", "sizes": "512x512", "type": "image/png"}}
  ]
}}
"""


def ensure_course_branding() -> None:
    COURSE_ICONS.mkdir(parents=True, exist_ok=True)
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "app-icon-512.png"):
        src = BRAND_ICONS / name
        dst = COURSE_ICONS / name
        if src.exists() and (not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime):
            shutil.copy2(src, dst)
    (COURSE_DIR / "manifest.webmanifest").write_text(
        manifest_text(offline=False), encoding="utf-8"
    )


def transform_widget_offline(fname: str, raw: str, *, tinta_html: str) -> str:
    """Sibling tinta path + srcdoc-embed Tinta so nested iframe works in lesson srcdoc."""
    doc = raw.replace("../../../modulos/tinta-estudio.html", "tinta-estudio.html")
    # CTA stays as sibling link; embed Tinta inside the practice marco for srcdoc hosts
    onload = (
        "try{var d=this.contentDocument||this.contentWindow.document;"
        "if(d){var h=Math.max("
        "(d.documentElement&&d.documentElement.scrollHeight)||0,"
        "(d.body&&d.body.scrollHeight)||0,560);"
        "this.style.height=h+'px';}}"
        "catch(e){}"
    )
    iframe_srcdoc = (
        f'<iframe title="Tinta Estudio" class="widget-srcdoc" '
        f'srcdoc="{srcdoc_escape(tinta_html)}" '
        f'onload="{html.escape(onload, quote=True)}" '
        f'style="display:block;width:100%;height:75vh;min-height:28rem;border:0"></iframe>'
    )
    doc2, n = re.subn(
        r'<iframe\s+title="Tinta Estudio"\s+src="tinta-estudio\.html"[^>]*>\s*</iframe>',
        iframe_srcdoc,
        doc,
        count=1,
        flags=re.I,
    )
    if n != 1:
        # fallback: any tinta iframe
        doc2, n = re.subn(
            r'<iframe[^>]+src="tinta-estudio\.html"[^>]*>\s*</iframe>',
            iframe_srcdoc,
            doc,
            count=1,
            flags=re.I,
        )
    if n != 1:
        raise SystemExit(f"could not srcdoc-embed tinta in widget {fname}")
    assert_offline_safe(fname, doc2.replace(srcdoc_escape(tinta_html), ""))
    return doc2


def widget_srcdoc_block(label: str, fname: str, widget_html: str) -> str:
    title = html.escape(label, quote=True)
    onload = (
        "try{var d=this.contentDocument||this.contentWindow.document;"
        "if(d){var h=Math.max("
        "(d.documentElement&&d.documentElement.scrollHeight)||0,"
        "(d.body&&d.body.scrollHeight)||0,560);"
        "this.style.height=h+'px';this.parentElement.style.minHeight=h+'px';}}"
        "catch(e){}"
    )
    iframe = (
        f'<iframe title="{title}" class="widget-srcdoc" '
        f'srcdoc="{srcdoc_escape(widget_html)}" '
        f'onload="{html.escape(onload, quote=True)}" '
        f'style="height:36rem;max-height:80vh"></iframe>'
    )
    return f"""  <section class="bloque-interactivo" id="practica-tinta">
    <div class="marco-interactivo-cabecera">
      <span class="etiqueta-interactivo">{html.escape(label)}</span>
      <a class="enlace-abrir" href="{fname}">Abrir a pantalla completa →</a>
    </div>
    <div class="marco-interactivo marco-offline-embed" style="min-height:32rem">
      {iframe}
    </div>
    <p class="fallback-enlace">Si el marco embebido no responde, abre
      <a href="{fname}">{fname}</a>
      o <a href="tinta-estudio.html">Tinta Estudio</a>.</p>
  </section>"""



def ship_maestro_into_pack(root: pathlib.Path) -> None:
    """Copy shared _maestro runtime + all lecciones/maestro-*.json into flat pack root."""
    maestro_src = REPO / "profesor/_maestro"
    if maestro_src.is_dir():
        dst = root / "_maestro"
        dst.mkdir(exist_ok=True)
        for fname in ("maestro-runtime.js", "maestro-puntero.css", "maestro-demo.html", "README.md"):
            src = maestro_src / fname
            if src.exists():
                shutil.copy2(src, dst / fname)
                print("Shipped", f"_maestro/{fname}")
    n_json = 0
    for mj in sorted(LEC.glob("maestro-*.json")):
        shutil.copy2(mj, root / mj.name)
        n_json += 1
    print(f"Shipped {n_json} maestro-*.json from lecciones/")


def rewrite_maestro_paths_offline(doc: str) -> str:
    """Flat-pack path rewrite for modo maestro assets (sibling _maestro/)."""
    doc = doc.replace("../../_maestro/maestro-puntero.css", "_maestro/maestro-puntero.css")
    doc = doc.replace("../../_maestro/maestro-runtime.js", "_maestro/maestro-runtime.js")
    return doc


def ensure_offline_embed_class(doc: str) -> str:
    """Add offline-embed to body.leccion-shell without stripping attributes (e.g. data-maestro-json)."""
    def repl(m: re.Match) -> str:
        attrs = m.group(1) or ""
        if re.search(r'\bclass="', attrs):
            def class_repl(cm: re.Match) -> str:
                classes = cm.group(1)
                if re.search(r'(?<![\w-])offline-embed(?![\w-])', classes):
                    return cm.group(0)
                return f'class="{classes} offline-embed"'
            attrs2 = re.sub(r'\bclass="([^"]*)"', class_repl, attrs, count=1)
            return f"<body{attrs2}>"
        return f'<body{attrs} class="leccion-shell offline-embed">'
    return re.sub(r"<body([^>]*)>", repl, doc, count=1, flags=re.I)


def transform_lesson_offline(n: int, raw: str, *, tinta_html: str) -> str:
    doc = raw
    doc = doc.replace("../../_plantilla-leccion/leccion-shell.css", "leccion-shell.css")
    doc = doc.replace("../../_plantilla-leccion/leccion-shell-nav.js", "leccion-shell-nav.js")
    doc = doc.replace("../../../brand/favicon/", "icons/")
    doc = doc.replace('href="../../../index.html"', 'href="index.html"')
    doc = doc.replace("../../../modulos/calculadora.html", "calculadora.html")
    doc = doc.replace("../../../modulos/tinta-estudio.html", "tinta-estudio.html")
    doc = ensure_offline_embed_class(doc)
    doc = rewrite_maestro_paths_offline(doc)

    # Harden last available lesson next (complete pack → fin de curso)
    if n == AVAILABLE:
        next_title = (
            "Última lección"
            if is_complete()
            else f"L{AVAILABLE + 1:02d} próximamente"
        )
        doc = re.sub(
            r'<a class="atajo atajo-next"[^>]*>Siguiente →</a>',
            '<span class="atajo atajo-next is-disabled" aria-disabled="true" '
            f'title="{next_title}">Siguiente →</span>',
            doc,
            count=1,
        )

    wf = WIDGET_FILES.get(n)
    if wf:
        widget_raw = (LEC / wf).read_text(encoding="utf-8")
        widget_off = transform_widget_offline(wf, widget_raw, tinta_html=tinta_html)
        # pull label from existing cabecera if present
        mlab = re.search(
            r'<span class="etiqueta-interactivo">([^<]+)</span>',
            doc,
        )
        label = mlab.group(1) if mlab else f"Tinta · L{n:02d}"
        block = widget_srcdoc_block(label, wf, widget_off)
        doc2, nsub = re.subn(
            r'<section class="bloque-interactivo"[^>]*>.*?</section>',
            block,
            doc,
            count=1,
            flags=re.S,
        )
        if nsub != 1:
            raise SystemExit(f"L{n:02d}: could not replace bloque-interactivo")
        doc = doc2

    # Fix any leftover catch(e){}} typos
    doc = doc.replace("catch(e){}}", "catch(e){}")
    return doc


def render_hub(*, for_downloads: bool = False) -> str:
    if for_downloads:
        css = "../profesor/_plantilla-leccion/leccion-shell.css"
        home = "../index.html"
        descargas = "../descargas.html"
        brand = "../brand/favicon/"
        manifest = "../profesor/1eso-plastica-visual/manifest.webmanifest"
        lec_prefix = "../profesor/1eso-plastica-visual/lecciones/"
    else:
        css = "../_plantilla-leccion/leccion-shell.css"
        home = "../../index.html"
        descargas = "../../descargas.html"
        brand = "../../brand/favicon/"
        manifest = "manifest.webmanifest"
        lec_prefix = "lecciones/"

    items = []
    for i, title in enumerate(TEMARIO, start=1):
        if i <= AVAILABLE:
            fn = lesson_filename(i)
            tint = " · Tinta" if i in WIDGET_FILES else ""
            items.append(
                f'''      <li class="hub-item hub-disponible">
        <a href="{lec_prefix}{fn}">
          <span class="hub-num">{i:02d}</span>
          <span class="hub-titulo">{html.escape(title)}{html.escape(tint)}</span>
          <span class="hub-estado">Disponible</span>
        </a>
      </li>'''
            )
        else:
            items.append(
                f'''      <li class="hub-item hub-pronto">
        <span class="hub-num">{i:02d}</span>
        <span class="hub-titulo">{html.escape(title)}</span>
        <span class="hub-estado">Próximamente</span>
      </li>'''
            )

    l01 = lesson_filename(1)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{COURSE_NAME} · Les vencimos</title>
<meta name="theme-color" content="#FAF7F0"/>
<link rel="icon" href="{brand}favicon.svg" type="image/svg+xml"/>
<link rel="icon" href="{brand}favicon-32.png" sizes="32x32" type="image/png"/>
<link rel="apple-touch-icon" href="{brand}apple-touch-icon.png"/>
<link rel="manifest" href="{manifest}"/>
<link rel="stylesheet" href="{css}"/>
<style>
{HUB_STYLES}
</style>
</head>
<body class="leccion-shell">
<div class="leccion-wrap">

  <header class="leccion-top">
    <a class="leccion-marca" href="{home}">Les <span>vencimos</span></a>
    <p class="leccion-meta-top">Curso · shell</p>
  </header>

  <section class="hub-hero" aria-labelledby="hub-titulo">
    <p class="eyebrow" style="display:block;font-size:0.72rem;letter-spacing:0.16em;text-transform:uppercase;color:var(--lv-acento);font-weight:600;margin:0 0 0.55rem">Decreto 39/2022 · Castilla y León</p>
    <h1 id="hub-titulo">{COURSE_NAME}</h1>
    <p class="hub-status">
      <strong>Pack completo L01–L{AVAILABLE:02d}/{TOTAL}</strong> ({pack_ud_blurb()}) en shell HTML.
      Curso cerrado · Revisor Dios <strong>CONFIRMA</strong> (0 críticos).
      <strong>ZIP offline</strong> (sin instalar: descomprime y abre <code>ABRE-AQUI.html</code>) en <a href="{descargas}">Descargas</a>.
    </p>
    <div class="hub-cta-row">
    <a class="hub-cta" href="{lec_prefix}{l01}">Abrir lección 01 →</a>
    <a class="hub-cta hub-cta-maestro" href="{lec_prefix}{l01}?maestro=1">Probar modo maestro</a>
    </div>
  </section>

  <p class="hub-nota">Índice del temario completo ({TOTAL} lecciones). Todas disponibles como <code>leccion-NN-….html</code> (alias <code>leccion-NN.html</code>).</p>

  <ol class="hub-lista">
{chr(10).join(items)}
  </ol>

  <p class="hub-pie-nota">
    Educación obligatoria · currículo oficial CyL (Decreto 39/2022). Misma familia que Mate, ByG, GeoHistoria y Lengua; distinto del pack Profesor (multi-materia).
    Interactivos: {pack_interactivos_blurb()}.
  </p>

  <footer class="leccion-pie">
    <strong>Les vencimos</strong> · {COURSE_NAME} · pack completo L01–L{AVAILABLE:02d}/{TOTAL} · Revisor Dios CONFIRMA
  </footer>
</div>
</body>
</html>
"""


def write_hub() -> None:
    HUB.write_text(render_hub(for_downloads=False), encoding="utf-8")
    (REPO / "downloads/1eso-plastica-visual.html").write_text(
        render_hub(for_downloads=True), encoding="utf-8"
    )
    print("Wrote hub (+ downloads mirror)")


def update_descargas() -> None:
    text = DESCARGAS.read_text(encoding="utf-8")
    lead_new = (
        "Currículo oficial Castilla y León (LOMLOE). 1º ESO Matemáticas, Biología y Geología, "
        "Geografía e Historia, Lengua Castellana y Literatura y Educación Plástica, Visual y Audiovisual "
        f"(EPVA pack completo L01–L{AVAILABLE:02d}/{TOTAL}). "
        "<strong>No es el pack Profesor</strong> (ese es otro: muchas materias, más sencillo)."
    )
    text2, n = re.subn(
        r"Currículo oficial Castilla y León \(LOMLOE\)\. 1º ESO Matemáticas, Biología y Geología, "
        r"Geografía e Historia y Lengua Castellana y Literatura \(L01–L\d+ de \d+\)\. "
        r"<strong>No es el pack Profesor</strong> \(ese es otro: muchas materias, más sencillo\)\.",
        lead_new,
        text,
        count=1,
    )
    if n:
        text = text2
    else:
        text2, n = re.subn(
            r"Currículo oficial Castilla y León \(LOMLOE\)\. 1º ESO Matemáticas.*?No es el pack Profesor</strong> \(ese es otro: muchas materias, más sencillo\)\.",
            lead_new,
            text,
            count=1,
        )
        if n:
            text = text2

    article = f"""        <article class="item">
          <div class="num">{ARTICLE_NUM}</div>
          <div>
            <h2>{COURSE_NAME}</h2>
            <p class="kicker">Oficial CyL · Decreto 39/2022 · pack completo ({TOTAL} lecciones)</p>
            <p><strong>No se instala.</strong> Descomprime y abre <code>ABRE-AQUI.html</code> / <code>index.html</code>.
            Pack completo L01–L{AVAILABLE:02d}/{TOTAL} ({pack_ud_blurb()}). Revisor Dios CONFIRMA (0 críticos).
            Con Tinta Estudio en las lecciones con widget. Sin nube ni servidor.
            Distinto del pack Profesor.</p>
            <div class="actions">
              <a class="btn-download" href="/downloads/{ZIP_BASENAME}" download="{ZIP_BASENAME}">Descargar ZIP</a>
              <a class="textlink" href="/profesor/1eso-plastica-visual/lecciones/{lesson_filename(1)}">Abrir lección 01</a>
              <a class="textlink" href="/profesor/1eso-plastica-visual/{HUB_BASENAME}">Índice del curso</a>
            </div>
          </div>
        </article>
"""
    if ZIP_BASENAME in text:
        text2, n = re.subn(
            rf'\s*<article class="item">\s*<div class="num">{ARTICLE_NUM}</div>.*?</article>\n',
            "\n" + article,
            text,
            count=1,
            flags=re.S,
        )
        if n:
            text = text2
            print("descargas.html: replaced existing Plástica article")
        else:
            print("descargas.html: ZIP already mentioned; article pattern not replaced")
    else:
        # insert after Lengua article (08d)
        needle = 'href="/profesor/1eso-lengua-castellana/1eso-lengua-castellana.html">Índice del curso</a>'
        idx = text.find(needle)
        if idx < 0:
            raise SystemExit("descargas.html: could not find Lengua index link to insert after")
        end = text.find("</article>", idx)
        if end < 0:
            raise SystemExit("descargas.html: no </article> after Lengua")
        end = end + len("</article>")
        text = text[:end] + "\n" + article + text[end:]
        print("descargas.html: inserted Plástica article")

    DESCARGAS.write_text(text, encoding="utf-8")


def update_descargas_profesor() -> None:
    text = DESCARGAS_PROF.read_text(encoding="utf-8")
    text = text.replace(
        "Descargas educación Les vencimos: 1º ESO CyL (Mate, ByG, GeoHistoria, Lengua) y pack Profesor cole.",
        "Descargas educación Les vencimos: 1º ESO CyL (Mate, ByG, GeoHistoria, Lengua, Plástica) y pack Profesor cole.",
    )
    article = f"""      <article class="item">
        <div class="num">05</div>
        <div>
          <h2>{COURSE_NAME}</h2>
          <p class="kicker">Oficial CyL · pack completo {AVAILABLE}/{TOTAL}</p>
          <div class="actions">
            <a class="btn-download" href="/downloads/{ZIP_BASENAME}" download="{ZIP_BASENAME}">Descargar ZIP</a>
            <a class="textlink" href="/profesor/1eso-plastica-visual/{HUB_BASENAME}">Índice del curso</a>
          </div>
        </div>
      </article>
"""
    # renumber Profesor pack to 06 if we insert as 05
    if ZIP_BASENAME in text:
        text2, n = re.subn(
            rf'\s*<article class="item">\s*<div class="num">05</div>\s*<div>\s*<h2>{re.escape(COURSE_NAME)}</h2>.*?</article>\n',
            "\n" + article,
            text,
            count=1,
            flags=re.S,
        )
        if n:
            text = text2
        print("descargas-profesor: Plástica already present / refreshed")
    else:
        # Insert before Pack Profesor; renumber Profesor from 05 → 06
        text = text.replace(
            """      <article class="item primary">
        <div class="num">05</div>
        <div>
          <h2>Profesor</h2>""",
            article
            + """      <article class="item primary">
        <div class="num">06</div>
        <div>
          <h2>Profesor</h2>""",
            1,
        )
        print("descargas-profesor: inserted Plástica")
    DESCARGAS_PROF.write_text(text, encoding="utf-8")


def update_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    block = f"""              <li>
                <span class="lv-pack-name">1º ESO Plástica <em>(pack completo 31/31)</em></span>
                <span class="lv-cta-row lv-cta-inline">
                  <a class="lv-square lv-square-secondary" href="/profesor/1eso-plastica-visual/{HUB_BASENAME}">Ver</a>
                  <a class="lv-square lv-square-secondary" href="/downloads/{ZIP_BASENAME}" download="{ZIP_BASENAME}">Descargar</a>
                </span>
              </li>
"""
    if "1eso-plastica-visual" in text:
        text2, n = re.subn(
            r'\s*<li>\s*<span class="lv-pack-name">1º ESO Plástica.*?</li>\n',
            "\n" + block,
            text,
            count=1,
            flags=re.S,
        )
        if n:
            text = text2
            print("index.html: refreshed Plástica pillar row")
        else:
            print("index.html: plastica mentioned but row not replaced")
    else:
        needle = """              <li>
                <span class="lv-pack-name">Pack Profesor cole"""
        if needle not in text:
            raise SystemExit("index.html: Pack Profesor row not found")
        text = text.replace(needle, block + needle, 1)
        print("index.html: inserted Plástica pillar row")
    INDEX.write_text(text, encoding="utf-8")


def update_inventory_light() -> None:
    inv = REPO / "docs/inventario-curriculo-cyl-lomloe.md"
    if not inv.exists():
        return
    text = inv.read_text(encoding="utf-8")
    note = (
        "\n\n### Publicación completa (Les vencimos)\n\n"
        f"- **1º ESO Educación Plástica, Visual y Audiovisual**: pack completo L01–L{AVAILABLE:02d}/{TOTAL} "
        "(hub + ZIP offline). Revisor Dios CONFIRMA (0 críticos).\n"
    )
    if re.search(r"### Publicación (?:parcial|completa) \(Les vencimos\)", text):
        # refresh block (parcial → completa or refresh completa)
        text2, n = re.subn(
            r"### Publicación (?:parcial|completa) \(Les vencimos\).*?(?=\n## |\n### |\Z)",
            note.strip() + "\n",
            text,
            count=1,
            flags=re.S,
        )
        if n:
            text = text2
    else:
        # append near EPVA mention / end of section 3
        anchor = "Siguiente oleada 1º ESO: Lengua Extranjera (Inglés), Educación Física, Educación Plástica Visual y Audiovisual;"
        if anchor in text:
            text = text.replace(
                anchor,
                anchor
                + f" **EPVA pack completo L01–L{AVAILABLE:02d}/{TOTAL}** (Revisor Dios CONFIRMA).",
                1,
            )
        text = text.rstrip() + note
    # Scrub leftover parcial EPVA inline notes from earlier partial publish
    text = re.sub(
        r"\*\*EPVA L01–L\d+/\d+ ya publicadas\*\* \(parcial; resto en curso\)\.?\s*",
        f"**EPVA pack completo L01–L{AVAILABLE:02d}/{TOTAL}** (Revisor Dios CONFIRMA). ",
        text,
        count=1,
    )
    text = re.sub(
        r"\*\*EPVA pack completo L01–L\d+/\d+\*\* \(Revisor Dios CONFIRMA\)\.?\s*",
        f"**EPVA pack completo L01–L{AVAILABLE:02d}/{TOTAL}** (Revisor Dios CONFIRMA). ",
        text,
        count=1,
    )
    inv.write_text(text, encoding="utf-8")
    print("inventory: light touch")


def build_offline_pack() -> None:
    if PACK_DIR.exists():
        shutil.rmtree(PACK_DIR)
    root = PACK_DIR / ZIP_FOLDER
    root.mkdir(parents=True)

    tinta_html = TINTA.read_text(encoding="utf-8")
    assert_offline_safe("tinta-estudio.html", tinta_html)

    (root / "LEEME.md").write_text(
        f"""# {COURSE_NAME} — pack offline

No hay que instalar nada. Descomprime y abre **ABRE-AQUI.html** (o index.html).

**Qué es:** lecciones de **Educación obligatoria** (currículo oficial Castilla y León, Decreto 39/2022 · EPVA).
Este pack trae el **curso completo** (lecciones **01–{AVAILABLE:02d}/{TOTAL}**) ({pack_ud_blurb()}) en HTML plano (shell + práctica Tinta embebida donde hay widget).
Revisor Dios **CONFIRMA** OK curso (0 críticos).

**Cómo abrir (Android / PC) — 4 pasos**

1. Descarga el ZIP.
2. Abre **Archivos / Mis archivos** (NO la lista Descargas del navegador).
3. Descomprime y entra en la carpeta `{ZIP_FOLDER}`.
4. Toca **`ABRE-AQUI.html`** o **`index.html`** → Chrome / Samsung Internet.

Todo funciona **offline**, sin nube ni servidor (`file://`). Sin instalación, sin app store, sin «setup».

**Importante en Android:** abre siempre desde la **carpeta descomprimida** (`file://`).
**Nunca** abras el HTML desde la lista Descargas del navegador (`content://`): ahí fallan
imágenes, CSS e interactivos.

En Chrome/Android: menú → **Añadir a pantalla de inicio**.

La práctica **Tinta Estudio** va **embebida** en las lecciones con widget (y también suelta como `tinta-estudio.html`).
Si hace falta, cada lección con práctica tiene «Abrir a pantalla completa →».

**Contenido:** `ABRE-AQUI.html`, `index.html`, `LEEME.md`, `leccion-01`…`leccion-{AVAILABLE:02d}-….html`,
alias `leccion-NN.html`, widgets Tinta, `tinta-estudio.html`, calculadora, CSS/JS e iconos — todo en la misma carpeta.
""",
        encoding="utf-8",
    )

    items = []
    for n in range(1, AVAILABLE + 1):
        items.append(
            f'    <li class="ok"><a href="{lesson_filename(n)}"><strong>L{n:02d}</strong> — {html.escape(TEMARIO[n-1])}</a></li>'
        )
    if not is_complete():
        for n in range(AVAILABLE + 1, min(AVAILABLE + 6, TOTAL + 1)):
            items.append(
                f'    <li class="soon"><span><strong>L{n:02d}</strong> — {html.escape(TEMARIO[n-1])} · próximamente</span></li>'
            )
        items.append(f'    <li class="soon"><span>… hasta L{TOTAL} — próximamente</span></li>')

    hub_flat = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#FAF7F0"/>
<title>{COURSE_NAME} · offline · Les vencimos</title>
<link rel="icon" href="icons/favicon.svg" type="image/svg+xml"/>
<link rel="icon" href="icons/favicon-32.png" sizes="32x32" type="image/png"/>
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png"/>
<link rel="manifest" href="manifest.webmanifest"/>
<link rel="stylesheet" href="leccion-shell.css"/>
<style>
  .hub-lista-flat{{list-style:none;padding:0;margin:1.25rem 0 0;display:grid;gap:0.55rem}}
  .hub-lista-flat li{{background:#fff;border:1px solid #E8E0D0;border-radius:12px;padding:0.85rem 1rem}}
  .hub-lista-flat li.ok a{{color:#2F5D7A;text-decoration:none;font-weight:600}}
  .hub-lista-flat li.ok a:hover{{text-decoration:underline}}
  .hub-lista-flat li.soon{{color:#5C564C;opacity:0.85}}
  .big-cta{{display:inline-block;margin-top:1rem;padding:0.85rem 1.35rem;background:#C4A15A;color:#0E0E0C;border-radius:999px;font-weight:700;text-decoration:none}}
  .no-install{{background:#EAF3EC;border:1px solid #B7D0BE;border-radius:12px;padding:0.9rem 1rem;margin:1rem 0}}
</style>
</head>
<body class="leccion-shell">
<div class="leccion-wrap">
  <header class="leccion-top">
    <a class="leccion-marca" href="index.html">Les <span>vencimos</span></a>
    <p class="leccion-meta-top">Pack offline</p>
  </header>
  <header class="bloque-titulo">
    <span class="eyebrow">Educación obligatoria · CyL</span>
    <h1 class="titulo-leccion">{COURSE_NAME}</h1>
    <p class="meta-leccion">Pack completo L01–L{AVAILABLE:02d}/{TOTAL} · {pack_ud_blurb(short=True)} · Revisor Dios CONFIRMA</p>
  </header>
  <div class="no-install">
    <strong>No hay que instalar nada.</strong> Abre <code>ABRE-AQUI.html</code> o <code>index.html</code> desde esta carpeta
    (Archivos / Mis archivos → carpeta descomprimida → <code>file://</code>).
    Tinta va embebida en las lecciones con widget.
    En Chrome/Android: menú → <strong>Añadir a pantalla de inicio</strong>.
    <strong>Nunca</strong> abras desde la lista Descargas del navegador (<code>content://</code>).
  </div>
  <p><a class="big-cta" href="{lesson_filename(1)}">Abrir lección 01 →</a>
     &nbsp; <a class="big-cta hub-cta-maestro" href="{lesson_filename(1)}?maestro=1" style="background:transparent;color:#0E0E0C;border:2px solid #C4A15A;box-shadow:none">Probar modo maestro</a>
     &nbsp; <a href="tinta-estudio.html">Tinta Estudio</a>
     &nbsp; <a href="calculadora.html">Calculadora</a></p>
  <p class="hub-nota">Curso completo L01–L{AVAILABLE:02d}/{TOTAL}. Usa siempre este índice.</p>
  <section class="bloque-cuerpo">
    <h2>Lecciones</h2>
    <ol class="hub-lista-flat">
{chr(10).join(items)}
    </ol>
  </section>
  <footer class="leccion-pie"><strong>Les vencimos</strong> · pack plano · sin instalar · lee LEEME.md</footer>
</div>
</body>
</html>
"""
    (root / "index.html").write_text(hub_flat, encoding="utf-8")
    (root / "ABRE-AQUI.html").write_text(hub_flat, encoding="utf-8")

    shutil.copy2(PLANTILLA / "leccion-shell.css", root / "leccion-shell.css")
    shutil.copy2(PLANTILLA / "leccion-shell-nav.js", root / "leccion-shell-nav.js")
    shutil.copy2(CALC, root / "calculadora.html")
    shutil.copy2(TINTA, root / "tinta-estudio.html")

    icons_dst = root / "icons"
    icons_dst.mkdir()
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "app-icon-512.png"):
        shutil.copy2(BRAND_ICONS / name, icons_dst / name)
    (root / "manifest.webmanifest").write_text(manifest_text(offline=True), encoding="utf-8")

    for n in range(1, AVAILABLE + 1):
        src = LEC / lesson_filename(n)
        if not src.exists():
            raise SystemExit(f"missing lesson {src}")
        offline_html = transform_lesson_offline(
            n, src.read_text(encoding="utf-8"), tinta_html=tinta_html
        )
        (root / lesson_filename(n)).write_text(offline_html, encoding="utf-8")
        write_redirect(
            root / f"leccion-{n:02d}.html",
            lesson_filename(n),
            f"Lección {n:02d}",
        )
        wf = WIDGET_FILES.get(n)
        if wf:
            wraw = (LEC / wf).read_text(encoding="utf-8")
            # standalone widget in pack: sibling tinta (iframe src), good for "open in tab"
            wstand = wraw.replace("../../../modulos/tinta-estudio.html", "tinta-estudio.html")
            wstand = wstand.replace("catch(e){}}", "catch(e){}")
            assert_offline_safe(wf, wstand)
            (root / wf).write_text(wstand, encoding="utf-8")

    ship_maestro_into_pack(root)

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(PACK_DIR).as_posix())
    size = ZIP_PATH.stat().st_size
    print(f"Wrote {ZIP_PATH} ({size} bytes)")
    shutil.rmtree(PACK_DIR)


def audit_online_shells() -> None:
    """Quick sanity: tinta paths, progress, no catch(e){}}."""
    for n, fn in LESSON_FILES.items():
        p = LEC / fn
        t = p.read_text(encoding="utf-8")
        if "catch(e){}}" in t:
            raise SystemExit(fn + ": bad catch(e){}}")
        if f'data-total="31"' not in t:
            raise SystemExit(f"{fn}: data-total != 31")
        if f"L{n:02d} de 31" not in t and f"L{n:02d} de <" not in t:
            if f"· L{n:02d} de 31 ·" not in t:
                raise SystemExit(f"{fn}: missing Lxx de 31 footer")
        if n in WIDGET_FILES and "../../../modulos/tinta-estudio.html" not in t:
            raise SystemExit(f"{fn}: missing tinta path")
        if n == AVAILABLE and not is_complete():
            nxt = AVAILABLE + 1
            if re.search(rf'atajo-next"[^>]*href="leccion-{nxt:02d}', t):
                raise SystemExit(f"{fn}: still links to missing L{nxt:02d}")
        if n == TOTAL:
            if re.search(r'atajo-next"[^>]*href="leccion-3[2-9]', t) or re.search(
                r'atajo-next"[^>]*href="leccion-[4-9]', t
            ):
                raise SystemExit(f"{fn}: L31 must not link to a next lesson")
    for wf in WIDGET_FILES.values():
        t = (LEC / wf).read_text(encoding="utf-8")
        if "../../../modulos/tinta-estudio.html" not in t:
            raise SystemExit(f"{wf}: bad tinta path")
        if "catch(e){}}" in t:
            raise SystemExit(wf + ": bad catch brace")
    print("audit_online_shells: OK")


def main() -> None:
    audit_online_shells()
    ensure_course_branding()
    write_hub()
    update_descargas()
    update_descargas_profesor()
    update_index()
    update_inventory_light()
    build_offline_pack()
    print("DONE available=", AVAILABLE, "total=", TOTAL)


if __name__ == "__main__":
    main()
