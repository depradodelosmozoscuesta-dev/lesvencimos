#!/usr/bin/env python3
"""Build flat offline pack + site wiring for 1º ESO Educación Física (32/32).

Does NOT rewrite pedagogical lesson bodies. Packages existing shells, ships
modo maestro runtime + maestro-NN.json, and wires descargas listings.
"""
from __future__ import annotations

import html
import pathlib
import re
import shutil
import zipfile

REPO = pathlib.Path("/workspace/lesvencimos")
COURSE_DIR = REPO / "profesor/1eso-educacion-fisica"
LEC = COURSE_DIR / "lecciones"
PLANTILLA = REPO / "profesor/_plantilla-leccion"
MAESTRO_SRC = REPO / "profesor/_maestro"
HUB = COURSE_DIR / "1eso-educacion-fisica.html"
DESCARGAS = REPO / "descargas.html"
DESCARGAS_PROF = REPO / "descargas-profesor.html"
INDEX = REPO / "index.html"
INV = REPO / "docs/inventario-curriculo-cyl-lomloe.md"
PACK_DIR = REPO / "downloads/_build-1eso-educacion-fisica-flat"
ZIP_PATH = REPO / "downloads/1eso-educacion-fisica-offline.zip"
BRAND_ICONS = REPO / "brand/favicon"
CALC = REPO / "modulos/calculadora.html"

TOTAL = 32
AVAILABLE = 32
COURSE_NAME = "1º ESO Educación Física"
COURSE_SHORT = "1º ESO Educación Física"
ZIP_FOLDER = "1eso-educacion-fisica-offline"
HUB_BASENAME = "1eso-educacion-fisica.html"
ZIP_BASENAME = "1eso-educacion-fisica-offline.zip"
ARTICLE_NUM = "08f"

TEMARIO = [
    'Actividad física diaria y semanal',
    'Alimentación saludable y hábitos',
    'Postura, respiración y musculatura del core',
    'Calentamiento autónomo y dolor muscular retardado',
    'Aparatos y sistemas del cuerpo en el movimiento',
    'Salud social: malos hábitos y estereotipos',
    'Salud mental: disfrute, prejuicios y aceptación',
    'Elegir la práctica: competición con lógica y respeto',
    'Autoconstrucción de materiales y consumo responsable',
    'Higiene en la actividad física',
    'Planificar un proyecto motor y autoevaluarse',
    'Herramientas digitales con criterio',
    'Prevención de accidentes: ropa, calzado, material, instalaciones',
    'Primeros auxilios básicos: PAS, SVB y 112',
    'Esquema corporal y capacidades perceptivo-motrices',
    'Capacidades físicas básicas (condicionales)',
    'Decisiones en juegos individuales y cooperativos',
    'Oposición y colaboración-oposición: rival y móvil',
    'Técnica y habilidades motrices específicas',
    'Creatividad motriz: retos originales seguros',
    'Accesibilidad universal y movilidad activa',
    'Emociones en el juego: esfuerzo, frustración y superación',
    'Cooperar, roles y conductas prosociales',
    'Reglas y arbitraje como integración social',
    'Rechazar violencia y discriminación en el deporte',
    'Juegos y danzas: herencia cultural e interculturalidad',
    'El cuerpo que habla: expresión de emociones',
    'Ritmo y música en el movimiento',
    'Deporte y perspectiva de género: referentes',
    'Andar, pedalar, circular: normas viales y bicicleta',
    'Espacios urbanos y naturales: prácticas, riesgo y seguridad',
    'Cuidar el entorno mientras nos movemos',
]

LESSON_FILES = {
    1: "leccion-01-actividad-fisica-diaria-y-semanal.html",
    2: "leccion-02-alimentacion-saludable-y-habitos.html",
    3: "leccion-03-postura-respiracion-y-core.html",
    4: "leccion-04-calentamiento-autonomo-y-dolor-muscular.html",
    5: "leccion-05-aparatos-y-sistemas-en-el-movimiento.html",
    6: "leccion-06-salud-social-malos-habitos-y-estereotipos.html",
    7: "leccion-07-salud-mental-disfrute-prejuicios-aceptacion.html",
    8: "leccion-08-elegir-la-practica-competicion-con-respeto.html",
    9: "leccion-09-autoconstruccion-materiales-consumo-responsable.html",
    10: "leccion-10-higiene-en-la-actividad-fisica.html",
    11: "leccion-11-planificar-proyecto-motor-y-autoevaluarse.html",
    12: "leccion-12-herramientas-digitales-con-criterio.html",
    13: "leccion-13-prevencion-de-accidentes-ropa-calzado-material-instalaciones.html",
    14: "leccion-14-primeros-auxilios-basicos-pas-svb-y-112.html",
    15: "leccion-15-esquema-corporal-y-capacidades-perceptivo-motrices.html",
    16: "leccion-16-capacidades-fisicas-basicas-condicionales.html",
    17: "leccion-17-decisiones-en-juegos-individuales-y-cooperativos.html",
    18: "leccion-18-oposicion-y-colaboracion-oposicion-rival-y-movil.html",
    19: "leccion-19-tecnica-y-habilidades-motrices-especificas.html",
    20: "leccion-20-creatividad-motriz-retos-originales-seguros.html",
    21: "leccion-21-accesibilidad-universal-y-movilidad-activa.html",
    22: "leccion-22-emociones-en-el-juego-esfuerzo-frustracion-y-superacion.html",
    23: "leccion-23-cooperar-roles-y-conductas-prosociales.html",
    24: "leccion-24-reglas-y-arbitraje-como-integracion-social.html",
    25: "leccion-25-rechazar-violencia-y-discriminacion-en-el-deporte.html",
    26: "leccion-26-juegos-y-danzas-herencia-cultural-e-interculturalidad.html",
    27: "leccion-27-el-cuerpo-que-habla-expresion-de-emociones.html",
    28: "leccion-28-ritmo-y-musica-en-el-movimiento.html",
    29: "leccion-29-deporte-y-perspectiva-de-genero-referentes.html",
    30: "leccion-30-andar-pedalar-circular-normas-viales-y-bicicleta.html",
    31: "leccion-31-espacios-urbanos-y-naturales-practicas-riesgo-y-seguridad.html",
    32: "leccion-32-cuidar-el-entorno-mientras-nos-movemos.html",
}


def lesson_filename(n: int) -> str:
    return LESSON_FILES[n]


def pack_ud_blurb(*, short: bool = False) -> str:
    if short:
        return "contenidos A–F · Decreto 39/2022"
    return (
        "temario completo EF 1º CyL "
        "(vida activa, organización, motricidad, emociones, cultura motriz, entorno)"
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
    return f"""{
  "name": "{COURSE_NAME} · Les vencimos",
  "short_name": "{COURSE_SHORT}",
  "start_url": "{start}",
  "scope": "./",
  "display": "standalone",
  "theme_color": "#FAF7F0",
  "background_color": "#FAF7F0",
  "icons": [
    {"src": "icons/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
    {"src": "icons/favicon-32.png", "sizes": "32x32", "type": "image/png"},
    {"src": "icons/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
    {"src": "icons/app-icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}
"""


def ship_maestro_into_pack(root: pathlib.Path) -> None:
    dst = root / "_maestro"
    dst.mkdir(exist_ok=True)
    for fname in (
        "maestro-runtime.js",
        "maestro-puntero.css",
        "maestro-demo.html",
        "README.md",
    ):
        src = MAESTRO_SRC / fname
        if src.exists():
            shutil.copy2(src, dst / fname)
            print("Shipped", f"_maestro/{fname}")
    n_json = 0
    for mj in sorted(LEC.glob("maestro-*.json")):
        shutil.copy2(mj, root / mj.name)
        n_json += 1
    print(f"Shipped {n_json} maestro-*.json from lecciones/")


def rewrite_maestro_paths_offline(doc: str) -> str:
    doc = doc.replace("../../_maestro/maestro-puntero.css", "_maestro/maestro-puntero.css")
    doc = doc.replace("../../_maestro/maestro-runtime.js", "_maestro/maestro-runtime.js")
    return doc


def ensure_offline_embed_class(doc: str) -> str:
    def repl(m: re.Match) -> str:
        attrs = m.group(1) or ""
        if re.search(r'\bclass="', attrs):
            def class_repl(cm: re.Match) -> str:
                classes = cm.group(1)
                if re.search(r"(?<![\w-])offline-embed(?![\w-])", classes):
                    return cm.group(0)
                return f'class="{classes} offline-embed"'

            attrs2 = re.sub(r'\bclass="([^"]*)"', class_repl, attrs, count=1)
            return f"<body{attrs2}>"
        return f'<body{attrs} class="leccion-shell offline-embed">'

    return re.sub(r"<body([^>]*)>", repl, doc, count=1, flags=re.I)


def transform_lesson_offline(n: int, raw: str) -> str:
    """Path rewrites only — no pedagogy changes."""
    doc = raw
    doc = doc.replace("../../_plantilla-leccion/leccion-shell.css", "leccion-shell.css")
    doc = doc.replace("../../_plantilla-leccion/leccion-shell-nav.js", "leccion-shell-nav.js")
    doc = doc.replace("../../../brand/favicon/", "icons/")
    doc = doc.replace('href="../../../index.html"', 'href="index.html"')
    doc = doc.replace("../../../modulos/calculadora.html", "calculadora.html")
    doc = ensure_offline_embed_class(doc)
    doc = rewrite_maestro_paths_offline(doc)
    assert_offline_safe(lesson_filename(n), doc)
    leftovers = re.findall(r'(?:href|src)="([^"]*\.\./[^"]*)"', doc)
    if leftovers:
        raise SystemExit(f"L{n:02d}: leftover ../ paths: {leftovers[:5]}")
    return doc


def refresh_hub_footnote() -> None:
    text = HUB.read_text(encoding="utf-8")
    n_before = len(re.findall(r'href="lecciones/leccion-\d{2}-[^"]+\.html"', text))

    new_status_inner = (
        f"      <strong>Pack completo L01–L{AVAILABLE:02d}/{TOTAL}</strong> "
        "(contenidos A–F del Decreto 39/2022 CyL, 100&nbsp;%).\n"
        "      Curso cerrado · Revisor Dios <strong>CONFIRMA</strong> (0 críticos).\n"
        "      <strong>ZIP offline</strong> (sin instalar: descomprime y abre "
        '<code>ABRE-AQUI.html</code>) en <a href="../../descargas.html">Descargas</a>.'
    )
    text2, n = re.subn(
        r'(<p class="hub-status">).*?(</p>)',
        r"\1\n" + new_status_inner + r"\n    \2",
        text,
        count=1,
        flags=re.S,
    )
    if not n:
        raise SystemExit("hub: hub-status not found")
    text = text2

    new_pie = (
        '<p class="hub-pie-nota">Material educativo. No sustituye al profesorado de '
        "Educación Física ni a consejo médico. Prácticas pensadas para casa, patio o parque. "
        "Ante dolor, mareo o lesión: parar y consultar. En urgencia: <strong>112</strong>. "
        "Curso cerrado · Revisor Dios CONFIRMA (0 críticos).</p>"
    )
    text2, n = re.subn(
        r'<p class="hub-pie-nota">.*?</p>',
        new_pie,
        text,
        count=1,
        flags=re.S,
    )
    if not n:
        raise SystemExit("hub: hub-pie-nota not found")
    text = text2

    n_after = len(re.findall(r'href="lecciones/leccion-\d{2}-[^"]+\.html"', text))
    if n_after != n_before or n_after < TOTAL:
        raise SystemExit(f"hub refresh destroyed links: before={n_before} after={n_after}")
    HUB.write_text(text, encoding="utf-8")
    print(f"hub: refreshed footnote; {n_after} links preserved")


def write_downloads_mirror() -> None:
    raw = HUB.read_text(encoding="utf-8")
    doc = raw
    doc = doc.replace('href="../../brand/favicon/', 'href="../brand/favicon/')
    doc = doc.replace(
        'href="../_plantilla-leccion/',
        'href="../profesor/_plantilla-leccion/',
    )
    doc = doc.replace(
        'href="lecciones/',
        'href="../profesor/1eso-educacion-fisica/lecciones/',
    )
    doc = doc.replace('href="../../descargas.html"', 'href="../descargas.html"')
    doc = doc.replace('href="../../index.html"', 'href="../index.html"')
    (REPO / "downloads/1eso-educacion-fisica.html").write_text(doc, encoding="utf-8")
    print("Wrote downloads/1eso-educacion-fisica.html mirror")


def update_descargas() -> None:
    text = DESCARGAS.read_text(encoding="utf-8")
    lead_new = (
        "Currículo oficial Castilla y León (LOMLOE). 1º ESO Matemáticas, Biología y Geología, "
        "Geografía e Historia, Lengua Castellana y Literatura, Educación Plástica, Visual y Audiovisual "
        f"(EPVA pack completo L01–L31/31) y Educación Física (pack completo L01–L{AVAILABLE:02d}/{TOTAL}). "
        "<strong>No es el pack Profesor</strong> (ese es otro: muchas materias, más sencillo)."
    )
    text2, n = re.subn(
        r'<p class="lead-mini">Currículo oficial Castilla y León \(LOMLOE\).*?</p>',
        f'<p class="lead-mini">{lead_new}</p>',
        text,
        count=1,
        flags=re.S,
    )
    if n:
        text = text2
        print("descargas.html: refreshed lead-mini")
    else:
        print("descargas.html: WARN lead-mini not updated")

    l01 = lesson_filename(1)
    article = f"""        <article class="item">
          <div class="num">{ARTICLE_NUM}</div>
          <div>
            <h2>{COURSE_NAME}</h2>
            <p class="kicker">Oficial CyL · Decreto 39/2022 · pack completo ({TOTAL} lecciones)</p>
            <p><strong>No se instala.</strong> Descomprime y abre <code>ABRE-AQUI.html</code> / <code>index.html</code>.
            Pack completo L01–L{AVAILABLE:02d}/{TOTAL} ({pack_ud_blurb()}). Revisor Dios CONFIRMA (0 críticos).
            Modo maestro en cada lección. Sin nube ni servidor.
            Material educativo: no es consejo médico; en urgencia llama al <strong>112</strong>.
            Distinto del pack Profesor.</p>
            <div class="actions">
              <a class="btn-download" href="/downloads/{ZIP_BASENAME}" download="{ZIP_BASENAME}">Descargar ZIP</a>
              <a class="textlink" href="/profesor/1eso-educacion-fisica/lecciones/{l01}">Abrir lección 01</a>
              <a class="textlink" href="/profesor/1eso-educacion-fisica/{HUB_BASENAME}">Índice del curso</a>
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
            print("descargas.html: replaced existing EF article")
        else:
            print("descargas.html: ZIP mentioned; article pattern not replaced")
    else:
        needle = 'href="/profesor/1eso-plastica-visual/1eso-plastica-visual.html">Índice del curso</a>'
        idx = text.find(needle)
        if idx < 0:
            raise SystemExit("descargas.html: Plástica index link not found")
        end = text.find("</article>", idx) + len("</article>")
        text = text[:end] + "\n" + article + text[end:]
        print("descargas.html: inserted EF article as", ARTICLE_NUM)

    DESCARGAS.write_text(text, encoding="utf-8")


def update_descargas_profesor() -> None:
    text = DESCARGAS_PROF.read_text(encoding="utf-8")
    text = text.replace(
        "Descargas educación Les vencimos: 1º ESO CyL, pack Profesor cole y Linux Essentials (piloto + PDFs LPI).",
        "Descargas educación Les vencimos: 1º ESO CyL (Mate, ByG, GeoHistoria, Lengua, Plástica, Educación Física), pack Profesor cole y Linux Essentials (piloto + PDFs LPI).",
    )
    article = f"""      <article class="item">
        <div class="num">06</div>
        <div>
          <h2>{COURSE_NAME}</h2>
          <p class="kicker">Oficial CyL · pack completo {AVAILABLE}/{TOTAL}</p>
          <div class="actions">
            <a class="btn-download" href="/downloads/{ZIP_BASENAME}" download="{ZIP_BASENAME}">Descargar ZIP</a>
            <a class="textlink" href="/profesor/1eso-educacion-fisica/{HUB_BASENAME}">Índice del curso</a>
          </div>
        </div>
      </article>
"""
    if ZIP_BASENAME in text:
        text2, n = re.subn(
            rf'\s*<article class="item">\s*<div class="num">06</div>\s*<div>\s*<h2>{re.escape(COURSE_NAME)}</h2>.*?</article>\n',
            "\n" + article,
            text,
            count=1,
            flags=re.S,
        )
        if n:
            text = text2
        print("descargas-profesor: EF already present / refreshed")
    else:
        old_prof = """      <article class="item primary">
        <div class="num">06</div>
        <div>
          <h2>Profesor</h2>"""
        new_prof = """      <article class="item primary">
        <div class="num">07</div>
        <div>
          <h2>Profesor</h2>"""
        if old_prof not in text:
            raise SystemExit("descargas-profesor: Profesor article 06 not found")
        text = text.replace(old_prof, article + new_prof, 1)
        print("descargas-profesor: inserted EF as 06; Profesor → 07")
    DESCARGAS_PROF.write_text(text, encoding="utf-8")


def update_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    block = f"""              <li>
                <span class="lv-pack-name">1º ESO Educación Física <em>(pack completo 32/32)</em></span>
                <span class="lv-cta-row lv-cta-inline">
                  <a class="lv-square lv-square-secondary" href="/profesor/1eso-educacion-fisica/{HUB_BASENAME}">Ver</a>
                  <a class="lv-square lv-square-secondary" href="/downloads/{ZIP_BASENAME}" download="{ZIP_BASENAME}">Descargar</a>
                </span>
              </li>
"""
    if "1eso-educacion-fisica" in text:
        text2, n = re.subn(
            r'\s*<li>\s*<span class="lv-pack-name">1º ESO Educación Física.*?</li>\n',
            "\n" + block,
            text,
            count=1,
            flags=re.S,
        )
        if n:
            text = text2
            print("index.html: refreshed EF pillar row")
        else:
            print("index.html: educacion-fisica mentioned but row not replaced")
    else:
        needle = """              <li>
                <span class="lv-pack-name">Linux Essentials <em>(piloto)</em></span>"""
        if needle not in text:
            needle = """              <li>
                <span class="lv-pack-name">Pack Profesor cole"""
        if needle not in text:
            raise SystemExit("index.html: insert anchor not found")
        text = text.replace(needle, block + needle, 1)
        print("index.html: inserted EF pillar row")
    INDEX.write_text(text, encoding="utf-8")


def update_inventory_light() -> None:
    if not INV.exists():
        return
    text = INV.read_text(encoding="utf-8")
    # oleada line: append EF note once
    oleada_add = (
        f" **Educación Física pack completo L01–L{AVAILABLE:02d}/{TOTAL}** "
        "(Revisor Dios CONFIRMA)."
    )
    if "Educación Física pack completo L01–L32/32" not in text:
        anchor = "**EPVA pack completo L01–L31/31** (Revisor Dios CONFIRMA)."
        if anchor in text:
            text = text.replace(anchor, anchor + oleada_add, 1)
            print("inventory: oleada note added")
    bullet = (
        f"- **1º ESO Educación Física**: pack completo L01–L{AVAILABLE:02d}/{TOTAL} "
        "(hub + ZIP offline). Revisor Dios CONFIRMA (0 críticos).\n"
    )
    if "### Publicación completa (Les vencimos)" in text:
        # section body until next ### at line start
        m = re.search(
            r"(### Publicación completa \(Les vencimos\)\n)(.*?)(?=\n### |\Z)",
            text,
            flags=re.S,
        )
        if m:
            body = m.group(2)
            if "1º ESO Educación Física" not in body:
                text = text[: m.end(1)] + bullet + body + text[m.end() :]
                print("inventory: added EF bullet")
            else:
                text2, n = re.subn(
                    r"- \*\*1º ESO Educación Física\*\*:.*?\n",
                    bullet,
                    text,
                    count=1,
                )
                if n:
                    text = text2
                print("inventory: refreshed EF bullet")
    else:
        text = text.rstrip() + "\n\n### Publicación completa (Les vencimos)\n\n" + bullet
        print("inventory: created publicación section")
    INV.write_text(text, encoding="utf-8")


def build_offline_pack() -> None:
    if PACK_DIR.exists():
        shutil.rmtree(PACK_DIR)
    root = PACK_DIR / ZIP_FOLDER
    root.mkdir(parents=True)

    (root / "LEEME.md").write_text(
        f"""# {COURSE_NAME} — pack offline

No hay que instalar nada. Descomprime y abre **ABRE-AQUI.html** (o index.html).

**Qué es:** lecciones de **Educación obligatoria** (currículo oficial Castilla y León, Decreto 39/2022 · Educación Física).
Este pack trae el **curso completo** (lecciones **01–{AVAILABLE:02d}/{TOTAL}**) ({pack_ud_blurb()}) en HTML plano (shell + modo maestro).
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

**Salud y seguridad:** este material es **educativo**. **No** es consejo médico ni sustituye al profesorado de Educación Física o a un profesional sanitario. Prácticas pensadas para casa, patio o parque. Ante dolor, mareo o lesión: **parar** y consultar. En una emergencia: llama al **112**. La lección de primeros auxilios (L14) explica el marco PAS/SVB/112; **no** es un tutorial de RCP.

**Contenido:** `ABRE-AQUI.html`, `index.html`, `LEEME.md`, `leccion-01`…`leccion-{AVAILABLE:02d}-….html`,
alias `leccion-NN.html`, `maestro-NN.json`, carpeta `_maestro/`, calculadora, CSS/JS e iconos — todo en la misma carpeta.
""",
        encoding="utf-8",
    )

    items = []
    for n in range(1, AVAILABLE + 1):
        items.append(
            f'    <li class="ok"><a href="{lesson_filename(n)}"><strong>L{n:02d}</strong> — {html.escape(TEMARIO[n - 1])}</a></li>'
        )

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
  .hub-lista-flat{list-style:none;padding:0;margin:1.25rem 0 0;display:grid;gap:0.55rem}
  .hub-lista-flat li{background:#fff;border:1px solid #E8E0D0;border-radius:12px;padding:0.85rem 1rem}
  .hub-lista-flat li.ok a{color:#2F5D7A;text-decoration:none;font-weight:600}
  .hub-lista-flat li.ok a:hover{text-decoration:underline}
  .big-cta{display:inline-block;margin-top:1rem;padding:0.85rem 1.35rem;background:#C4A15A;color:#0E0E0C;border-radius:999px;font-weight:700;text-decoration:none}
  .no-install{background:#EAF3EC;border:1px solid #B7D0BE;border-radius:12px;padding:0.9rem 1rem;margin:1rem 0}
  .aviso-salud{background:#F8F1E3;border:1px solid #E0D3B8;border-radius:12px;padding:0.9rem 1rem;margin:1rem 0;font-size:0.95rem}
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
    En Chrome/Android: menú → <strong>Añadir a pantalla de inicio</strong>.
    <strong>Nunca</strong> abras desde la lista Descargas del navegador (<code>content://</code>).
  </div>
  <div class="aviso-salud">
    <strong>Salud:</strong> material educativo · <strong>no</strong> es consejo médico.
    Ante dolor, mareo o lesión: parar y consultar. Urgencia: <strong>112</strong>. Lee <code>LEEME.md</code>.
  </div>
  <p><a class="big-cta" href="{lesson_filename(1)}">Abrir lección 01 →</a>
     &nbsp; <a class="big-cta" href="{lesson_filename(1)}?maestro=1" style="background:transparent;color:#0E0E0C;border:2px solid #C4A15A;box-shadow:none">Probar modo maestro</a>
     &nbsp; <a href="calculadora.html">Calculadora</a></p>
  <p class="hub-nota">Curso completo L01–L{AVAILABLE:02d}/{TOTAL}. Usa siempre este índice.</p>
  <section class="bloque-cuerpo">
    <h2>Lecciones</h2>
    <ol class="hub-lista-flat">
{chr(10).join(items)}
    </ol>
  </section>
  <footer class="leccion-pie"><strong>Les vencimos</strong> · pack plano · sin instalar · lee LEEME.md · Dios CONFIRMA</footer>
</div>
</body>
</html>
"""
    (root / "index.html").write_text(hub_flat, encoding="utf-8")
    (root / "ABRE-AQUI.html").write_text(hub_flat, encoding="utf-8")

    shutil.copy2(PLANTILLA / "leccion-shell.css", root / "leccion-shell.css")
    shutil.copy2(PLANTILLA / "leccion-shell-nav.js", root / "leccion-shell-nav.js")
    shutil.copy2(CALC, root / "calculadora.html")

    icons_dst = root / "icons"
    icons_dst.mkdir()
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "app-icon-512.png"):
        shutil.copy2(BRAND_ICONS / name, icons_dst / name)
    (root / "manifest.webmanifest").write_text(manifest_text(offline=True), encoding="utf-8")

    for n in range(1, AVAILABLE + 1):
        src = LEC / lesson_filename(n)
        offline_html = transform_lesson_offline(n, src.read_text(encoding="utf-8"))
        (root / lesson_filename(n)).write_text(offline_html, encoding="utf-8")
        write_redirect(
            root / f"leccion-{n:02d}.html",
            lesson_filename(n),
            f"Lección {n:02d}",
        )

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


def audit_source() -> None:
    for n, fn in LESSON_FILES.items():
        p = LEC / fn
        t = p.read_text(encoding="utf-8")
        if "googleapis" in t or re.search(r"cdn\.", t, re.I):
            raise SystemExit(f"{fn}: CDN reference")
        if "data-maestro-json=" not in t:
            raise SystemExit(f"{fn}: missing data-maestro-json")
        if "maestro-runtime.js" not in t:
            raise SystemExit(f"{fn}: missing maestro-runtime.js")
    print("audit_source: OK", AVAILABLE, "/", TOTAL)


def main() -> None:
    audit_source()
    refresh_hub_footnote()
    write_downloads_mirror()
    update_descargas()
    update_descargas_profesor()
    update_index()
    update_inventory_light()
    build_offline_pack()
    print("DONE available=", AVAILABLE, "total=", TOTAL, "article=", ARTICLE_NUM)


if __name__ == "__main__":
    main()
