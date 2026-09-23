#!/usr/bin/env python3
"""Build online shell + flat offline pack for 1º ESO Biología y Geología (L01 only)."""
from __future__ import annotations

import html
import json
import pathlib
import re
import shutil
import zipfile

REPO = pathlib.Path("/workspace/lesvencimos")
COURSE_DIR = REPO / "profesor/1eso-biologia-geologia"
LEC = COURSE_DIR / "lecciones"
PLANTILLA = REPO / "profesor/_plantilla-leccion"
HUB = COURSE_DIR / "1eso-biologia-geologia.html"
DESCARGAS = REPO / "descargas.html"
INDEX = REPO / "index.html"
PACK_DIR = REPO / "downloads/_build-1eso-byg-flat"
ZIP_PATH = REPO / "downloads/1eso-biologia-geologia-offline.zip"
COURSE_ICONS = COURSE_DIR / "icons"
BRAND_ICONS = REPO / "brand/favicon"
TOTAL = 40
AVAILABLE = 1

# Full temario titles (L02–L40 shown as próximamente on hub)
TEMARIO = [
    "El método científico en experimentos sencillos",
    "Fuentes veraces frente a bulos y pseudociencia",
    "Laboratorio: instrumentos, espacios y normas de seguridad",
    "Observar, tomar datos, modelar y presentar resultados",
    "Científicas y científicos que cambiaron la biología y la geología",
    "Rocas y minerales: qué son y en qué se diferencian",
    "Clasificar rocas: sedimentarias, metamórficas e ígneas",
    "El ciclo de las rocas",
    "Rocas y minerales relevantes (con foco en Castilla y León)",
    "Extracción minera: aplicaciones, economía y sociedad en CyL",
    "Estructura de la geosfera y movimientos de la Tierra",
    "Atmósfera: composición y estructura",
    "Contaminación, efecto invernadero, ozono y Agenda 2030",
    "Hidrosfera y el ciclo del agua",
    "Mares, aguas continentales, contaminación y uso sostenible",
    "Por qué atmósfera e hidrosfera hacen posible la vida",
    "La célula: unidad estructural y funcional",
    "Célula procariota y sus partes",
    "Célula eucariota animal y sus partes",
    "Célula eucariota vegetal y sus partes",
    "Observar y comparar células al microscopio",
    "Funciones vitales: nutrición, relación y reproducción",
    "Clasificación, nomenclatura binomial y especies de CyL",
    "De los antiguos reinos a los dominios actuales",
    "Hongos: características y micología en Castilla y León",
    "Plantas: grupos, flor, fruto y semilla",
    "Animales invertebrados: anatomía y fisiología básicas",
    "Animales vertebrados y animales como seres sintientes",
    "Identificar especies del entorno (guías y claves)",
    "Ecosistemas del entorno y sus elementos",
    "Relaciones intraespecíficas e interespecíficas",
    "Cadenas, redes y pirámides tróficas",
    "Conservar ecosistemas, biodiversidad y desarrollo sostenible",
    "Especies amenazadas y figuras de protección ambiental",
    "Atmósfera, hidrosfera, geosfera y biosfera: suelo y relieve",
    "Cambio climático y consecuencias en los ecosistemas",
    "Hábitos sostenibles (consumo, residuos, respeto al medio)",
    "One Health: salud ambiental, humana y de otros seres vivos",
    "Proyecto integrador del curso (ciencia + entorno CyL)",
    "Autoevaluación, portfolio y hábitos de trabajo científico",
]

LESSONS = [
    {
        "n": 1,
        "slug": "el-metodo-cientifico-en-experimentos-sencillos",
        "eyebrow": "Lección 01 · UD A · Proyecto científico",
        "title_html": "El <em>método científico</em> en experimentos sencillos",
        "title_plain": "El método científico en experimentos sencillos",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque A",
        "curiosidad_t": "Probar antes de creer",
        "curiosidad": (
            "Hace casi mil años, Ibn al-Haytham (Alhazén) insistió en comprobar "
            "las ideas sobre la luz con experimentos, no solo con argumentos. "
            "Ese hábito —observar, preguntar y poner a prueba— es el germen del "
            "método científico que usas en el laboratorio de Biología y Geología."
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            "Nombrar y ordenar los pasos del <strong>método científico</strong> en un experimento sencillo.",
            "Distinguir <strong>observación</strong>, <strong>pregunta</strong>, <strong>hipótesis</strong>, <strong>experimento</strong>, <strong>datos</strong> y <strong>conclusión</strong>.",
            "Reconocer qué es una <strong>hipótesis comprobable</strong> y qué no lo es.",
            "Identificar la <strong>variable</strong> que cambias y lo que dejas igual (<strong>control</strong>).",
            "Aplicar el método a una escena real: un <strong>cubito de hielo</strong> que se derrite.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>La ciencia no es «adivinar a ciegas». Es un <strong>camino ordenado</strong> para entender la naturaleza con pruebas. Ese camino se llama <strong>método científico</strong>.</p>
    <div class="tarjeta">
      <p style="margin:0">En un colegio de <strong>Valladolid</strong>, Lucía deja un <strong>cubito de hielo</strong> en un vaso. Al rato es más pequeño y hay más agua. Marcos dice: «¡Se ha evaporado!». Lucía: «No lo sé todavía… vamos a <strong>investigarlo</strong> como científicos».</p>
    </div>
    <h2>Los 6 pasos</h2>
    <ol>
      <li><strong>Observar</strong> — mirar con atención y anotar lo que ves (sin inventar aún la causa).</li>
      <li><strong>Preguntar</strong> — convertir la curiosidad en una pregunta investigable.</li>
      <li><strong>Hipotetizar</strong> — proponer una hipótesis: explicación <strong>comprobable</strong>.</li>
      <li><strong>Experimentar</strong> — prueba justa (cambiar una cosa, controlar el resto).</li>
      <li><strong>Tomar datos</strong> — medir y anotar (números, dibujos, tablas).</li>
      <li><strong>Concluir</strong> — decidir si los datos apoyan o no la hipótesis.</li>
    </ol>
    <div class="tarjeta">
      <p style="margin:0 0 0.5rem"><strong>Mnemónico:</strong> «Oso Pequeño Hace Experimentos De Ciencia»</p>
      <p style="margin:0"><strong>O</strong>bservar · <strong>P</strong>reguntar · <strong>H</strong>ipotetizar · <strong>E</strong>xperimentar · <strong>D</strong>atos · <strong>C</strong>oncluir</p>
    </div>
    <p><strong>Variable</strong> = lo que cambias a propósito. <strong>Control</strong> = lo que dejas igual para que la comparación sea justa.</p>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "En invierno en <strong>Burgos</strong> o <strong>León</strong>, el hielo del patio se derrite cuando sale el sol: misma pregunta que Lucía.",
            "En casa: ¿el chocolate se ablanda más cerca del radiador? Método científico casero.",
            "En el huerto escolar: ¿las plantas del alféizar crecen distinto a las de la sombra? (hoy practicamos el <strong>método</strong>).",
            "Un meteorólogo de CyL también observa → pregunta → mide → concluye sobre el tiempo.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Laboratorio · método científico · cubito", "l01-metodo-cientifico.html"),
        ],
        "reto_t": "Mi mini-experimento",
        "reto": (
            "Describe en 4–6 líneas un experimento <strong>sencillo</strong> que podrías hacer "
            "en casa o en el patio (agua, temperatura, plantas de alféizar, hielo…). "
            "Marca con claridad: observación, pregunta, hipótesis y qué medirías."
        ),
        "reto_id": "1eso-byg-L01",
        "cierre": (
            "<strong>Oso Pequeño Hace Experimentos De Ciencia.</strong> "
            "Observas → preguntas → hipotetizas → experimentas → tomas datos → concluyes. "
            "Una hipótesis no es un deseo: es una idea que se puede <strong>poner a prueba</strong>."
        ),
    },
]


def lesson_filename(n: int) -> str:
    lesson = next(item for item in LESSONS if item["n"] == n)
    return f"leccion-{n:02d}-{lesson['slug']}.html"


def manifest_text(*, offline: bool = False) -> str:
    # Online hub lives in course dir; offline pack uses flat icons/
    icons_prefix = "icons/" if offline else "icons/"
    return json.dumps({
        "name": "1º ESO Biología y Geología · Les vencimos",
        "short_name": "1º ESO ByG",
        "start_url": "./index.html" if offline else "./1eso-biologia-geologia.html",
        "scope": "./",
        "display": "standalone",
        "theme_color": "#FAF7F0",
        "background_color": "#FAF7F0",
        "accent_color": "#C4A15A",
        "icons": [
            {"src": f"{icons_prefix}favicon.svg", "sizes": "any", "type": "image/svg+xml"},
            {"src": f"{icons_prefix}favicon-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": f"{icons_prefix}apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
            {"src": f"{icons_prefix}app-icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, ensure_ascii=False, indent=2) + "\n"


def ensure_course_branding() -> None:
    COURSE_ICONS.mkdir(parents=True, exist_ok=True)
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "app-icon-512.png"):
        shutil.copy2(BRAND_ICONS / name, COURSE_ICONS / name)
    (COURSE_DIR / "manifest.webmanifest").write_text(
        manifest_text(offline=False), encoding="utf-8"
    )


def progress_pct(n: int) -> str:
    return f"{(n / TOTAL) * 100:.2f}".rstrip("0").rstrip(".")


def nav_html(n: int, *, offline: bool) -> str:
    calc = "calculadora.html" if offline else "../../../modulos/calculadora.html"
    hub = "index.html" if offline else "../1eso-biologia-geologia.html"
    if n <= 1:
        prev = (
            '<span class="atajo atajo-prev is-disabled" aria-disabled="true" '
            'title="Primera lección">← Anterior</span>'
        )
    else:
        prev = (
            f'<a class="atajo atajo-prev" href="{lesson_filename(n - 1)}" '
            f'title="Lección {n-1:02d}">← Anterior</a>'
        )
    if n >= TOTAL:
        nxt = f'<a class="atajo atajo-next" href="{hub}" title="Volver al índice">Fin del curso</a>'
    elif n >= AVAILABLE:
        nxt = (
            f'<a class="atajo atajo-next" href="{hub}" '
            f'title="Más lecciones próximamente">Índice · próximamente →</a>'
        )
    else:
        nxt = (
            f'<a class="atajo atajo-next" href="{lesson_filename(n + 1)}" '
            f'title="Lección {n+1:02d}">Siguiente →</a>'
        )
    return f"""  <nav class="leccion-barra" aria-label="Navegación de lección"
       data-actual="{n}" data-total="{TOTAL}">
    <div class="leccion-progreso" role="status">
      <span class="progreso-texto"><strong>{n}</strong> de <strong>{TOTAL}</strong></span>
      <div class="progreso-pista" aria-hidden="true"><div class="progreso-lleno" style="width:{progress_pct(n)}%"></div></div>
    </div>
    <div class="leccion-atajos">
      <a class="atajo atajo-calc" href="{calc}" title="Calculadora offline">Calculadora</a>
      {prev}
      {nxt}
    </div>
  </nav>"""


def srcdoc_escape(doc: str) -> str:
    return (
        doc.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
    )


def load_widget_html(fname: str) -> str:
    path = LEC / fname
    if not path.exists():
        raise SystemExit(f"missing widget {fname}")
    return path.read_text(encoding="utf-8")


_EXTERNAL_URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.I)
_EXTERNAL_OK = ("w3.org", "www.w3.org", "xmlns", "schema.org", "schemas.xmlsoap")


def assert_widget_offline_safe(fname: str, doc: str) -> None:
    bad = []
    for url in sorted(set(_EXTERNAL_URL_RE.findall(doc))):
        if any(ok in url for ok in _EXTERNAL_OK):
            continue
        bad.append(url)
    if bad:
        raise SystemExit(
            f"widget {fname} has network URL(s) that break offline: {', '.join(bad[:8])}"
        )


def widget_block(
    label: str,
    fname: str,
    *,
    offline: bool = False,
    widget_html: str | None = None,
) -> str:
    title = html.escape(label, quote=True)
    if offline and widget_html is not None:
        onload = (
            "try{var d=this.contentDocument||this.contentWindow.document;"
            "if(d){var h=Math.max("
            "(d.documentElement&&d.documentElement.scrollHeight)||0,"
            "(d.body&&d.body.scrollHeight)||0,560);"
            "this.style.height=h+'px';this.parentElement.style.minHeight=h+'px';}}"
            "catch(e){}}"
        )
        iframe = (
            f'<iframe title="{title}" class="widget-srcdoc" '
            f'srcdoc="{srcdoc_escape(widget_html)}" '
            f'onload="{html.escape(onload, quote=True)}"></iframe>'
        )
        fallback = (
            f'Si el marco embebido no responde, abre el widget suelto: '
            f'<a href="{fname}">{fname}</a>.'
        )
    else:
        iframe = f'<iframe title="{title}" src="{fname}" loading="lazy"></iframe>'
        fallback = (
            f'Si el marco no carga (<code>file://</code>), abre '
            f'<a href="{fname}">{fname}</a>.'
        )
    marco_extra = " marco-offline-embed" if offline else ""
    return f"""  <section class="bloque-interactivo">
    <div class="marco-interactivo-cabecera">
      <span class="etiqueta-interactivo">{label}</span>
      <a class="enlace-abrir" href="{fname}">Abrir en pestaña →</a>
    </div>
    <div class="marco-interactivo{marco_extra}">
      {iframe}
    </div>
    <p class="fallback-enlace">{fallback}</p>
  </section>"""


def render_lesson(lesson: dict, *, offline: bool) -> str:
    n = lesson["n"]
    css = "leccion-shell.css" if offline else "../../_plantilla-leccion/leccion-shell.css"
    js = "leccion-shell-nav.js" if offline else "../../_plantilla-leccion/leccion-shell-nav.js"
    fig = (lambda f: f"figuras/{f}" if offline else f"../../_plantilla-leccion/figuras/{f}")
    home = "index.html" if offline else "../../../index.html"
    marca_meta = "1º ESO Biología y Geología · offline" if offline else "1º ESO Biología y Geología"
    icon_root = "icons" if offline else "../icons"
    # Online icons live under course; brand path also works — prefer course icons
    if not offline:
        icon_root = "../icons"
    manifest_href = "manifest.webmanifest" if offline else "../manifest.webmanifest"
    body_class = "leccion-shell offline-embed" if offline else "leccion-shell"

    objs = "".join(f"      <li>{o}</li>\n" for o in lesson["objetivos"])
    vida_lis = "".join(f"        <li>{v}</li>\n" for v in lesson["vida"])

    w_parts = []
    for lab, fn in lesson["widgets"]:
        wh = None
        if offline:
            wh = load_widget_html(fn)
            assert_widget_offline_safe(fn, wh)
        w_parts.append(widget_block(lab, fn, offline=offline, widget_html=wh))
    w_html = "\n".join(w_parts)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#FAF7F0"/>
<title>Lección {n:02d} · {lesson['title_plain']} · Les vencimos</title>
<link rel="icon" href="{icon_root}/favicon.svg" type="image/svg+xml"/>
<link rel="icon" href="{icon_root}/favicon-32.png" sizes="32x32" type="image/png"/>
<link rel="apple-touch-icon" href="{icon_root}/apple-touch-icon.png"/>
<link rel="manifest" href="{manifest_href}"/>
<link rel="stylesheet" href="{css}"/>
<script src="{js}" defer></script>
</head>
<body class="{body_class}">
<div class="leccion-wrap">

{nav_html(n, offline=offline)}

  <header class="leccion-top">
    <a class="leccion-marca" href="{home}">Les <span>vencimos</span></a>
    <p class="leccion-meta-top">{marca_meta}</p>
  </header>

  <header class="bloque-titulo">
    <span class="eyebrow">{lesson['eyebrow']}</span>
    <h1 class="titulo-leccion">{lesson['title_html']}</h1>
    <p class="meta-leccion">{lesson['meta']}</p>
  </header>

  <aside class="bloque-curiosidad">
    <p class="etiqueta-bloque">Curiosidad histórica</p>
    <h2 class="titulo-curiosidad">{lesson['curiosidad_t']}</h2>
    <p class="texto-curiosidad">{lesson['curiosidad']}</p>
    <div class="ilustracion-slot">
      <img src="{fig(lesson['curiosidad_fig'])}" width="96" height="96" alt=""/>
    </div>
  </aside>

  <section class="bloque-cuerpo">
    <h2>Objetivos</h2>
    <ol>
{objs}    </ol>
{lesson['cuerpo']}  </section>

  <section class="bloque-vida-real con-figura">
    <div class="figura" aria-hidden="true">
      <img src="{fig(lesson['vida_fig'])}" width="96" height="96" alt=""/>
    </div>
    <div class="contenido-vida">
      <p class="etiqueta-bloque">En la vida real</p>
      <h2 class="titulo-vida">{lesson['vida_t']}</h2>
      <ul>
{vida_lis}      </ul>
    </div>
  </section>

{w_html}

  <section class="bloque-cuerpo">
    <h2>Mini cierre</h2>
    <p>{lesson['cierre']}</p>
  </section>

  <section class="bloque-reto">
    <span class="etiqueta-reto">Reto Profesor</span>
    <h2 class="titulo-reto">{lesson['reto_t']}</h2>
    <p>{lesson['reto']}</p>
    <ul>
      <li>Usar los pasos del método (aunque sea en corto).</li>
      <li>Medir algo concreto (tiempo, temperatura, altura…).</li>
      <li>Conectar con tu entorno (CyL, casa, cole).</li>
    </ul>
    <p class="reto-id">reto_id: {lesson['reto_id']}</p>
  </section>

  <footer class="leccion-pie">
    <strong>Les vencimos</strong> · L{n:02d} de {TOTAL} · shell HTML · offline / file:// · sin instalar
  </footer>
</div>
</body>
</html>
"""


def write_redirect(path: pathlib.Path, target: str, label: str) -> None:
    path.write_text(f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta http-equiv="refresh" content="0; url={target}"/>
<link rel="canonical" href="{target}"/>
<title>{label} · redirige · Les vencimos</title>
<style>
  body{{font-family:system-ui,sans-serif;max-width:36rem;margin:2rem auto;padding:0 1rem;line-height:1.5;color:#2A2620;background:#FAF7F0}}
  a{{color:#2F5D7A}}
</style>
</head>
<body>
  <h1>{label}</h1>
  <p>Esta página se ha movido a <a href="{target}"><strong>{target}</strong></a>.</p>
  <p>Si no redirige sola, usa el enlace.</p>
</body>
</html>
""", encoding="utf-8")


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
    color: var(--lv-tinta);
    font-size: 0.95rem;
  }
  .hub-estado {
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--lv-suave);
    white-space: nowrap;
  }
  .hub-disponible .hub-estado {
    color: var(--lv-verde);
  }
  .hub-pie-nota {
    margin-top: 1.5rem;
    padding: 0.9rem 1rem;
    font-size: 0.88rem;
    color: var(--lv-suave);
    background: var(--lv-fondo-2);
    border: 1px dashed var(--lv-linea);
    border-radius: var(--lv-radio);
  }
"""


def render_hub(*, for_downloads: bool = False) -> str:
    """Online hub (or downloads/ mirror with adjusted relative paths)."""
    if for_downloads:
        css = "../profesor/_plantilla-leccion/leccion-shell.css"
        home = "../index.html"
        descargas = "../descargas.html"
        brand = "../brand/favicon/"
        manifest = "../profesor/1eso-biologia-geologia/manifest.webmanifest"
        lec_prefix = "../profesor/1eso-biologia-geologia/lecciones/"
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
            items.append(
                f'''      <li class="hub-item hub-disponible">
        <a href="{lec_prefix}{fn}">
          <span class="hub-num">{i:02d}</span>
          <span class="hub-titulo">{html.escape(title)}</span>
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
<title>1º ESO Biología y Geología · Les vencimos</title>
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
    <h1 id="hub-titulo">1º ESO Biología y Geología</h1>
    <p class="hub-status">
      <strong>Lección 01 disponible</strong> (método científico) en shell HTML.
      El curso está <strong>en construcción</strong> (40 lecciones previstas).
      <strong>ZIP offline</strong> (sin instalar: descomprime y abre <code>ABRE-AQUI.html</code>) en <a href="{descargas}">Descargas</a>.
    </p>
    <a class="hub-cta" href="{lec_prefix}{l01}">Abrir lección 01 →</a>
  </section>

  <p class="hub-nota">Índice del temario (40 lecciones previstas). Solo L01 como <code>leccion-01-….html</code> (alias <code>leccion-01.html</code>). L02–L40: próximamente.</p>

  <ol class="hub-lista">
{chr(10).join(items)}
  </ol>

  <p class="hub-pie-nota">
    Educación obligatoria · currículo oficial CyL (Decreto 39/2022). Distinto del pack Profesor (multi-materia).
    Interactivo L01: laboratorio del cubito de hielo.
  </p>

  <footer class="leccion-pie">
    <strong>Les vencimos</strong> · 1º ESO Biología y Geología · L01 de {TOTAL} · en construcción
  </footer>
</div>
</body>
</html>
"""


def write_hub() -> None:
    HUB.write_text(render_hub(for_downloads=False), encoding="utf-8")
    (REPO / "downloads/1eso-biologia-geologia.html").write_text(
        render_hub(for_downloads=True), encoding="utf-8"
    )
    print("Wrote hub (+ downloads mirror)")


def update_descargas() -> None:
    text = DESCARGAS.read_text(encoding="utf-8")
    if "1eso-biologia-geologia-offline.zip" in text:
        print("descargas already has ByG entry")
        return

    # Soften Mate-only lead
    text = text.replace(
        "Empieza por 1º ESO Matemáticas. <strong>No es el pack Profesor</strong>",
        "1º ESO Matemáticas y Biología y Geología (L01). <strong>No es el pack Profesor</strong>",
    )

    byg_article = f"""        <article class="item">
          <div class="num">08b</div>
          <div>
            <h2>1º ESO Biología y Geología</h2>
            <p class="kicker">Oficial CyL · Decreto 39/2022 · en construcción (40 lecciones)</p>
            <p><strong>No se instala.</strong> Descomprime y abre <code>ABRE-AQUI.html</code> / <code>index.html</code>.
            L01 disponible (método científico); curso en construcción (40 lecciones previstas). Sin nube ni servidor.
            Distinto del pack Profesor.</p>
            <div class="actions">
              <a class="btn-download" href="/downloads/1eso-biologia-geologia-offline.zip" download="1eso-biologia-geologia-offline.zip">Descargar ZIP</a>
              <a class="textlink" href="/profesor/1eso-biologia-geologia/lecciones/{lesson_filename(1)}">Abrir lección 01</a>
              <a class="textlink" href="/profesor/1eso-biologia-geologia/1eso-biologia-geologia.html">Índice del curso</a>
            </div>
          </div>
        </article>
"""

    # Insert after Mate article (before closing </div> of that catalog)
    needle = """              <a class="textlink" href="/profesor/1eso-matematicas/1eso-matematicas.html">Índice del curso</a>
            </div>
          </div>
        </article>
      </div>

      <div class="section-modulos">
        <h2>Aprender para el cole</h2>"""
    if needle not in text:
        raise SystemExit("descargas.html Mate block not found for ByG insert")
    replacement = f"""              <a class="textlink" href="/profesor/1eso-matematicas/1eso-matematicas.html">Índice del curso</a>
            </div>
          </div>
        </article>
{byg_article}      </div>

      <div class="section-modulos">
        <h2>Aprender para el cole</h2>"""
    text = text.replace(needle, replacement, 1)
    DESCARGAS.write_text(text, encoding="utf-8")
    print("Updated descargas.html")


def update_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    old = "1º ESO Matemáticas (oficial CyL). L01 lista — descarga ZIP offline en Descargas."
    new = (
        "1º ESO Matemáticas + Biología y Geología L01 (oficial CyL). "
        "Descarga ZIP offline en Descargas."
    )
    if new in text:
        print("index already updated")
        return
    if old not in text:
        # try partial
        if "Biología y Geología" in text and "Educación obligatoria" in text:
            print("index already mentions ByG")
            return
        raise SystemExit("index.html Educación obligatoria card text not found")
    INDEX.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("Updated index.html")


def build_offline_pack() -> None:
    if PACK_DIR.exists():
        shutil.rmtree(PACK_DIR)
    root = PACK_DIR / "1eso-biologia-geologia-offline"
    root.mkdir(parents=True)

    (root / "LEEME.md").write_text(
        f"""# 1º ESO Biología y Geología — pack offline

No hay que instalar nada. Descomprime y abre **ABRE-AQUI.html** (o index.html).

**Qué es:** lecciones de **Educación obligatoria** (currículo oficial Castilla y León, Decreto 39/2022).
Este pack trae la lección **01** (método científico) en HTML plano (shell + interactivo embebido).
Curso en construcción: **40** lecciones previstas.

**Cómo abrir (Android / PC) — 4 pasos**

1. Descarga el ZIP.
2. Abre **Archivos / Mis archivos** (NO la lista Descargas del navegador).
3. Descomprime y entra en la carpeta `1eso-biologia-geologia-offline`.
4. Toca **`ABRE-AQUI.html`** o **`index.html`** → Chrome / Samsung Internet.

Todo funciona **offline**, sin nube ni servidor (`file://`). Sin instalación, sin app store, sin «setup».

**Importante en Android:** abre siempre desde la **carpeta descomprimida** (`file://`).
**Nunca** abras el HTML desde la lista Descargas del navegador (`content://`): ahí fallan
imágenes, CSS e interactivos/animaciones.
En Chrome/Android: menú → **Añadir a pantalla de inicio**.

Los interactivos van **embebidos** en cada lección (funcionan sin cargar iframes hermanos).
Si hace falta, cada lección sigue teniendo el enlace «Abrir en pestaña →» al widget suelto.

**Contenido:** `ABRE-AQUI.html`, `index.html`, `LEEME.md`, `leccion-01-….html`,
alias `leccion-01.html`, widget `l01-metodo-cientifico.html`, calculadora, CSS/JS,
`figuras/*.svg` e iconos — todo en la misma carpeta.
""",
        encoding="utf-8",
    )

    items = [
        f'    <li class="ok"><a href="{lesson_filename(1)}"><strong>L01</strong> — {TEMARIO[0]}</a></li>'
    ]
    for n in range(2, min(7, TOTAL + 1)):
        items.append(f'    <li class="soon"><span><strong>L{n:02d}</strong> — {html.escape(TEMARIO[n-1])} · próximamente</span></li>')
    items.append(f'    <li class="soon"><span>… hasta L{TOTAL} — próximamente</span></li>')

    hub_flat = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#FAF7F0"/>
<title>1º ESO Biología y Geología · offline · Les vencimos</title>
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
    <h1 class="titulo-leccion">1º ESO Biología y Geología</h1>
    <p class="meta-leccion">L01 lista · curso en construcción (40 lecciones previstas)</p>
  </header>
  <div class="no-install">
    <strong>No hay que instalar nada.</strong> Abre <code>ABRE-AQUI.html</code> o <code>index.html</code> desde esta carpeta
    (Archivos / Mis archivos → carpeta descomprimida → <code>file://</code>).
    El interactivo va embebido en la lección.
    En Chrome/Android: menú → <strong>Añadir a pantalla de inicio</strong>.
    <strong>Nunca</strong> abras desde la lista Descargas del navegador (<code>content://</code>).
  </div>
  <p><a class="big-cta" href="{lesson_filename(1)}">Abrir lección 01 →</a>
     &nbsp; <a href="calculadora.html">Calculadora</a></p>
  <p class="hub-nota">L02–L40 próximamente. Usa siempre este índice.</p>
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
    shutil.copy2(REPO / "modulos/calculadora.html", root / "calculadora.html")
    icons_dst = root / "icons"
    icons_dst.mkdir()
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "app-icon-512.png"):
        shutil.copy2(BRAND_ICONS / name, icons_dst / name)
    (root / "manifest.webmanifest").write_text(manifest_text(offline=True), encoding="utf-8")

    fig_dst = root / "figuras"
    fig_dst.mkdir()
    for svg in (PLANTILLA / "figuras").glob("*.svg"):
        shutil.copy2(svg, fig_dst / svg.name)

    for L in LESSONS:
        (root / lesson_filename(L["n"])).write_text(
            render_lesson(L, offline=True), encoding="utf-8"
        )
        write_redirect(
            root / f"leccion-{L['n']:02d}.html",
            lesson_filename(L["n"]),
            f"Lección {L['n']:02d}",
        )
        for _, wf in L["widgets"]:
            src = LEC / wf
            if not src.exists():
                raise SystemExit(f"missing widget {wf}")
            wh = src.read_text(encoding="utf-8")
            assert_widget_offline_safe(wf, wh)
            shutil.copy2(src, root / wf)

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                arc = path.relative_to(PACK_DIR).as_posix()
                zf.write(path, arc)
    size = ZIP_PATH.stat().st_size
    print(f"Wrote {ZIP_PATH} ({size} bytes)")
    shutil.rmtree(PACK_DIR)


def main() -> None:
    ensure_course_branding()
    for L in LESSONS:
        out = LEC / lesson_filename(L["n"])
        out.write_text(render_lesson(L, offline=False), encoding="utf-8")
        write_redirect(
            LEC / f"leccion-{L['n']:02d}.html",
            out.name,
            f"Lección {L['n']:02d} (alias)",
        )
        print("Wrote", out.name)

    write_hub()
    update_descargas()
    update_index()
    build_offline_pack()
    print("DONE available=", AVAILABLE, "total=", TOTAL)


if __name__ == "__main__":
    main()
