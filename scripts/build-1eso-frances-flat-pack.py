#!/usr/bin/env python3
"""Build flat offline pack + site wiring for 1º ESO Francés / Segunda Lengua Extranjera (40/40).

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
COURSE_DIR = REPO / "profesor/1eso-frances"
LEC = COURSE_DIR / "lecciones"
PLANTILLA = REPO / "profesor/_plantilla-leccion"
MAESTRO_SRC = REPO / "profesor/_maestro"
HUB = COURSE_DIR / "1eso-frances.html"
DESCARGAS = REPO / "descargas.html"
DESCARGAS_PROF = REPO / "descargas-profesor.html"
INDEX = REPO / "index.html"
INV = REPO / "docs/inventario-curriculo-cyl-lomloe.md"
PACK_DIR = REPO / "downloads/_build-1eso-frances-flat"
ZIP_PATH = REPO / "downloads/1eso-frances-offline.zip"
BRAND_ICONS = COURSE_DIR / "icons"
CALC = REPO / "modulos/calculadora.html"

TOTAL = 40
AVAILABLE = 40
COURSE_NAME = "1º ESO Francés"
COURSE_SHORT = "1º ESO Francés"
ZIP_FOLDER = "1eso-frances-offline"
HUB_BASENAME = "1eso-frances.html"
ZIP_BASENAME = "1eso-frances-offline.zip"
ARTICLE_NUM = "08j"


def discover_course_index() -> tuple[dict[int, str], list[str]]:
    """Discover shells and titles from the Francés (2.ª LE) course.

    Shells are leccion-NN.html (exact two-digit, no trailing slug).
    """
    files = {}
    for path in sorted(LEC.glob("leccion-[0-9][0-9].html")):
        m = re.match(r"leccion-(\d{2})\.html$", path.name)
        if m:
            files[int(m.group(1))] = path.name
    if len(files) != TOTAL or set(files) != set(range(1, TOTAL + 1)):
        raise SystemExit(f"frances: expected {TOTAL} named shells, found {len(files)}")
    hub = HUB.read_text(encoding="utf-8")
    titles = {}
    for m in re.finditer(
        r'href="lecciones/(leccion-(\d{2})\.html)"[^>]*>.*?<span class="hub-titulo">(.*?)</span>',
        hub,
        re.S,
    ):
        titles[int(m.group(2))] = html.unescape(re.sub(r"<[^>]+>", "", m.group(3)).strip())
    for n in range(1, TOTAL + 1):
        if n not in titles:
            raw = (LEC / files[n]).read_text(encoding="utf-8")
            hm = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
            titles[n] = (
                html.unescape(re.sub(r"<[^>]+>", "", hm.group(1)).strip())
                if hm
                else files[n]
            )
    temario = [titles.get(n, pathlib.Path(files[n]).stem) for n in range(1, TOTAL + 1)]
    return files, temario


LESSON_FILES, TEMARIO = discover_course_index()


def lesson_filename(n: int) -> str:
    return LESSON_FILES[n]


def pack_ud_blurb(*, short: bool = False) -> str:
    if short:
        return "currículo CyL Decreto 39/2022 LOMLOE · 2.ª LE francés"
    return (
        "Segunda Lengua Extranjera (Francés) 1º ESO: currículo de Castilla y León "
        "(Decreto 39/2022, LOMLOE); comunicación, plurilingüismo e interculturalidad; "
        "no es Inglés ni 1.ª lengua extranjera"
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
  "icons": [
    {{"src": "icons/favicon.svg", "sizes": "any", "type": "image/svg+xml"}},
    {{"src": "icons/favicon-32.png", "sizes": "32x32", "type": "image/png"}},
    {{"src": "icons/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}},
    {{"src": "icons/app-icon-512.png", "sizes": "512x512", "type": "image/png"}}
  ]
}}
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
    doc = doc.replace("../icons/", "icons/")
    doc = doc.replace("../manifest.webmanifest", "manifest.webmanifest")
    doc = doc.replace("../../_plantilla-leccion/figuras/", "figuras/")
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
    link_re = r'href="lecciones/leccion-\d{2}\.html"'
    n_before = len(re.findall(link_re, text))
    new_status_inner = (
        f"      <strong>Pack completo L01–L{AVAILABLE:02d}/{TOTAL}</strong> "
        "(Segunda Lengua Extranjera · Francés · Decreto 39/2022 CyL LOMLOE, 100&nbsp;%).\n"
        "      No es Inglés ni 1.ª lengua extranjera. Curso cerrado · Revisor Dios <strong>CONFIRMA</strong> (0 críticos).\n"
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
    new_pie = (
        '<p class="hub-pie-nota">Material educativo de Segunda Lengua Extranjera (Francés) 1º ESO. '
        "Basado en el currículo de Castilla y León (Decreto 39/2022, LOMLOE). "
        "No es Inglés ni sustituye al criterio del centro o del profesorado. "
        "Curso cerrado · Revisor Dios CONFIRMA (0 críticos).</p>"
    )
    if re.search(r'<p class="hub-pie-nota">', text2):
        text2, n = re.subn(r'<p class="hub-pie-nota">.*?</p>', new_pie, text2, count=1, flags=re.S)
        if not n:
            raise SystemExit("hub: hub-pie-nota replace failed")
    else:
        if ".hub-pie-nota" not in text2:
            text2 = text2.replace(
                "  .hub-item.hub-disponible .hub-estado { color: var(--lv-acento); }\n</style>",
                "  .hub-item.hub-disponible .hub-estado { color: var(--lv-acento); }\n"
                "  .hub-pie-nota { margin: 1.5rem 0 0; font-size: 0.88rem; color: var(--lv-suave); "
                "line-height: 1.5; }\n</style>",
                1,
            )
        if re.search(r'<footer class="leccion-pie"', text2):
            text2, n = re.subn(
                r'(\s*<footer class="leccion-pie")',
                "\n  " + new_pie + r"\1",
                text2,
                count=1,
            )
            if not n:
                raise SystemExit("hub: footer not found to insert hub-pie-nota")
        else:
            text2, n = re.subn(
                r"(</ol>\s*)(</div>\s*</body>)",
                r"\1  " + new_pie + r"\n\2",
                text2,
                count=1,
            )
            if not n:
                raise SystemExit("hub: </ol> not found to insert hub-pie-nota")
    n_after = len(re.findall(link_re, text2))
    if n_after != n_before or n_after < TOTAL:
        raise SystemExit(f"hub refresh destroyed links: before={n_before} after={n_after}")
    HUB.write_text(text2, encoding="utf-8")
    print(f"hub: refreshed footnote; {n_after} links preserved")


def write_downloads_mirror() -> None:
    raw = HUB.read_text(encoding="utf-8")
    doc = raw
    doc = doc.replace('href="../../brand/favicon/', 'href="../brand/favicon/')
    doc = doc.replace('href="icons/', 'href="../profesor/1eso-frances/icons/')
    doc = doc.replace(
        'href="manifest.webmanifest"',
        'href="../profesor/1eso-frances/manifest.webmanifest"',
    )
    doc = doc.replace('href="../_plantilla-leccion/', 'href="../profesor/_plantilla-leccion/')
    doc = doc.replace('href="lecciones/', 'href="../profesor/1eso-frances/lecciones/')
    doc = doc.replace('href="../../descargas.html"', 'href="../descargas.html"')
    doc = doc.replace('href="../../index.html"', 'href="../index.html"')
    (REPO / "downloads/1eso-frances.html").write_text(doc, encoding="utf-8")
    print("Wrote downloads/1eso-frances.html mirror")


def update_descargas() -> None:
    text = DESCARGAS.read_text(encoding="utf-8")
    lead_new = (
        "Currículo oficial Castilla y León (LOMLOE). 1º ESO Matemáticas, Biología y Geología, "
        "Geografía e Historia, Lengua Castellana y Literatura, Educación Plástica, Visual y Audiovisual "
        "(EPVA pack completo L01–L31/31), Educación Física (pack completo L01–L32/32), "
        "Alternativa laica a la Religión (pack completo L01–L28/28), Religión Católica "
        "(pack completo L01–L30/30), Inglés / Lengua Extranjera (pack completo L01–L40/40) y "
        f"Francés / 2.ª Lengua Extranjera (pack completo L01–L{AVAILABLE:02d}/{TOTAL}). "
        "Religión Católica conforme al marco confesional "
        "BOE-A-2022-10452 / Decreto 39/2022: no es Alternativa laica. "
        "Inglés conforme al Decreto 39/2022 (LOMLOE): no es Francés. "
        "Francés conforme al Decreto 39/2022 (LOMLOE) Segunda Lengua Extranjera: no es Inglés. "
        "<strong>No es el pack Profesor</strong> (ese es otro: muchas materias, más sencillo)."
    )
    m = re.search(
        r'<p class="lead-mini">Currículo oficial Castilla y León \(LOMLOE\).*?</p>',
        text,
        re.S,
    )
    if not m:
        raise SystemExit("descargas.html: lead-mini not found")
    text = text[: m.start()] + f'<p class="lead-mini">{lead_new}</p>' + text[m.end() :]
    article = f"""        <article class="item">
          <div class="num">{ARTICLE_NUM}</div>
          <div>
            <h2>{COURSE_NAME}</h2>
            <p class="kicker">Oficial CyL · Decreto 39/2022 LOMLOE · pack completo ({TOTAL} lecciones)</p>
            <p><strong>No se instala.</strong> Descomprime y abre <code>ABRE-AQUI.html</code> / <code>index.html</code>.
            Pack completo L01–L{AVAILABLE:02d}/{TOTAL} ({pack_ud_blurb()}). Revisor Dios CONFIRMA (0 críticos).
            Segunda Lengua Extranjera (Francés); <strong>no es Inglés</strong>. Modo maestro en cada lección. Sin nube ni servidor. Distinto del pack Profesor.</p>
            <div class="actions">
              <a class="btn-download" href="/downloads/{ZIP_BASENAME}" download="{ZIP_BASENAME}">Descargar ZIP</a>
              <a class="textlink" href="/profesor/1eso-frances/lecciones/{lesson_filename(1)}">Abrir lección 01</a>
              <a class="textlink" href="/profesor/1eso-frances/{HUB_BASENAME}">Índice del curso</a>
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
        else:
            raise SystemExit("descargas.html: existing frances article not replaced")
    else:
        anchor = 'href="/downloads/1eso-ingles-offline.zip"'
        idx = text.find(anchor)
        if idx < 0:
            raise SystemExit("descargas.html: ingles download anchor not found")
        end = text.find("</article>", idx) + len("</article>")
        text = text[:end] + "\n" + article + text[end:]
    DESCARGAS.write_text(text, encoding="utf-8")
    print("descargas.html: frances article", ARTICLE_NUM)


def update_descargas_profesor() -> None:
    text = DESCARGAS_PROF.read_text(encoding="utf-8")
    text = text.replace(
        "1º ESO CyL (Mate, ByG, GeoHistoria, Lengua, Plástica, Educación Física, Alternativa laica, Religión Católica, Inglés)",
        "1º ESO CyL (Mate, ByG, GeoHistoria, Lengua, Plástica, Educación Física, Alternativa laica, Religión Católica, Inglés, Francés)",
    )
    article = f"""      <article class="item">
        <div class="num">{ARTICLE_NUM}</div>
        <div>
          <h2>{COURSE_NAME}</h2>
          <p class="kicker">Oficial CyL · pack completo {AVAILABLE}/{TOTAL} · 2.ª lengua extranjera</p>
          <div class="actions">
            <a class="btn-download" href="/downloads/{ZIP_BASENAME}" download="{ZIP_BASENAME}">Descargar ZIP</a>
            <a class="textlink" href="/profesor/1eso-frances/{HUB_BASENAME}">Índice del curso</a>
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
    else:
        anchor = 'href="/downloads/1eso-ingles-offline.zip"'
        idx = text.find(anchor)
        if idx < 0:
            raise SystemExit("descargas-profesor: ingles download anchor not found")
        end = text.find("</article>", idx) + len("</article>")
        text = text[:end] + "\n" + article + text[end:]
    DESCARGAS_PROF.write_text(text, encoding="utf-8")
    print("descargas-profesor: frances article", ARTICLE_NUM)


def update_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    block = f"""              <li>
                <span class="lv-pack-name">{COURSE_NAME} <em>(pack completo {AVAILABLE}/{TOTAL} · 2.ª lengua extranjera)</em></span>
                <span class="lv-cta-row lv-cta-inline">
                  <a class="lv-square lv-square-secondary" href="/profesor/1eso-frances/{HUB_BASENAME}">Ver</a>
                  <a class="lv-square lv-square-secondary" href="/downloads/{ZIP_BASENAME}" download="{ZIP_BASENAME}">Descargar</a>
                </span>
              </li>
"""
    frances_row = r'\s*<li>\s*<span class="lv-pack-name">1º ESO Francés.*?</li>\n?'
    text = re.sub(frances_row, "", text, count=1, flags=re.S)
    ing = re.search(
        r'<li>\s*<span class="lv-pack-name">1º ESO Inglés.*?</li>',
        text,
        re.S,
    )
    if not ing:
        raise SystemExit("index.html: ingles row not found")
    text = text[: ing.end()] + "\n" + block + text[ing.end() :]
    text = re.sub(
        r'(</span>) +(?=</li>\s*<li>\s*<span class="lv-pack-name">1º ESO Francés)',
        r"\1\n              ",
        text,
        count=1,
    )
    INDEX.write_text(text, encoding="utf-8")
    print("index.html: frances pillar row")


def update_inventory_light() -> None:
    if not INV.exists():
        return
    text = INV.read_text(encoding="utf-8")
    bullet = (
        f"- **1º ESO Francés / Segunda Lengua Extranjera**: pack completo L01–L{AVAILABLE:02d}/{TOTAL} "
        "(hub + ZIP offline, Decreto 39/2022 CyL LOMLOE). Revisor Dios CONFIRMA (0 críticos). "
        "No es Inglés.\n"
    )
    marker = "### Publicación completa (Les vencimos)"
    if marker in text:
        m = re.search(
            r"(### Publicación completa \(Les vencimos\)\n)(.*?)(?=\n### |\Z)",
            text,
            re.S,
        )
        if m:
            body = m.group(2)
            if "1º ESO Francés" in body:
                body2, n = re.subn(
                    r"- \*\*1º ESO Francés[^*]*\*\*:.*?\n", bullet, body, count=1
                )
                body = body2 if n else body
            else:
                body = bullet + body
            text = text[: m.start(2)] + body + text[m.end(2) :]
    else:
        text = text.rstrip() + "\n\n" + marker + "\n" + bullet
    INV.write_text(text, encoding="utf-8")
    print("inventory: frances publication bullet")


def build_offline_pack() -> None:
    if PACK_DIR.exists():
        shutil.rmtree(PACK_DIR)
    root = PACK_DIR / ZIP_FOLDER
    root.mkdir(parents=True)

    (root / "LEEME.md").write_text(
        f"""# {COURSE_NAME} — pack offline

No hay que instalar nada. Descomprime y abre **ABRE-AQUI.html** (o index.html).

**Qué es:** pack de **Segunda Lengua Extranjera (Francés)** de 1º ESO (currículo de Castilla y León, Decreto 39/2022, LOMLOE). **No es Inglés.**
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

**Identidad:** material educativo de **Segunda Lengua Extranjera (Francés)**. Se basa en Decreto 39/2022 (LOMLOE). **No es Inglés.** No sustituye al criterio del centro ni del profesorado.

**Contenido:** `ABRE-AQUI.html`, `index.html`, `LEEME.md`, `leccion-01.html`…`leccion-{AVAILABLE:02d}.html`,
`maestro-NN.json`, carpeta `_maestro/`, calculadora, CSS/JS e iconos — todo en la misma carpeta.
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
  .hub-lista-flat{{list-style:none;padding:0;margin:1.25rem 0 0;display:grid;gap:0.55rem}}
  .hub-lista-flat li{{background:#fff;border:1px solid #E8E0D0;border-radius:12px;padding:0.85rem 1rem}}
  .hub-lista-flat li.ok a{{color:#2F5D7A;text-decoration:none;font-weight:600}}
  .hub-lista-flat li.ok a:hover{{text-decoration:underline}}
  .big-cta{{display:inline-block;margin-top:1rem;padding:0.85rem 1.35rem;background:#C4A15A;color:#0E0E0C;border-radius:999px;font-weight:700;text-decoration:none}}
  .no-install{{background:#EAF3EC;border:1px solid #B7D0BE;border-radius:12px;padding:0.9rem 1rem;margin:1rem 0}}
  .aviso-salud{{background:#F8F1E3;border:1px solid #E0D3B8;border-radius:12px;padding:0.9rem 1rem;margin:1rem 0;font-size:0.95rem}}
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
    <strong>Identidad:</strong> Segunda Lengua Extranjera (Francés) · <strong>no</strong> es Inglés.
    Material educativo. No sustituye al criterio del centro ni del profesorado. Lee <code>LEEME.md</code>.
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
        # Shells already named leccion-NN.html — skip self-redirects that would overwrite.
        alias = f"leccion-{n:02d}.html"
        if lesson_filename(n) != alias:
            write_redirect(root / alias, lesson_filename(n), f"Lección {n:02d}")

    for short in sorted(LEC.glob("l??-*.html")):
        shutil.copy2(short, root / short.name)
    figures_dst = root / "figuras"
    figures_dst.mkdir()
    for figure in sorted((PLANTILLA / "figuras").glob("*")):
        if figure.is_file():
            shutil.copy2(figure, figures_dst / figure.name)
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
