#!/usr/bin/env python3
"""Build Completo EMBED pack for monolithic App APK.

App contract (2026-10-01):
  assets/embed/completo-offline.zip
  = Estantería shell (parade k5 Completo) + full content of 7 thematic packs
  Layout: root ABRE-AQUI.html / estanteria.html + educacion/ + brand/
          + modulos/*.html (flat shelf) + guias-viaje/
          + modules/pack-1eso|casa|biblioteca|estudio|utiles|ocio|midia/
  Soft warn if ZIP > ~70 MB. Target APK < 80–100 MB.

Primary output:
  downloads/completo-offline.zip
Alias (same bytes):
  downloads/pack-completo-offline.zip
Snapshot:
  downloads/completo-offline-vYYYYMMDDx.zip

Excludes: radio, vitaink, cuba, privado-jorge (not in source packs).
Does NOT touch privado-jorge. Disk only — no web publish.

Embed shell strip: EMBED_NO_ADD removes Añadir / file picker / download-pack UI
(keeps parade k5 WebView fixes + Módulos show/hide). Soft warn if ZIP > ~70 MB.

Base shell: pack-completo-offline-v20261001k6.zip (parade k5) preferred;
falls back to k3/k4 thin snapshots or thin pack-completo-offline.zip.
Use --rebuild-shell to regenerate thin via build-pack-completo.py first.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "downloads"
STAGING = ROOT / "offline-pack-completo-embed"
VERSION = "v20261006embed-2.0.22"
SOFT_WARN_BYTES = 70 * 1024 * 1024

PRIMARY = DL / "completo-offline.zip"
ALIAS = DL / "pack-completo-offline.zip"
SNAPSHOT = DL / f"completo-offline-{VERSION}.zip"
# Prefer thin Completo shell snapshot (no modules/) so re-runs stay clean.
SHELL_CANDIDATES = [
    # Prefer previous fat Completo embed as base (keeps educacion/arduino/clarity max set)
    DL / "completo-offline-v20261005embed-claridad.zip",
    DL / "completo-offline.zip",
    DL / "pack-completo-offline-v20261001k6.zip",
    DL / "pack-completo-offline-v20261001k5.zip",
    DL / "pack-completo-offline-v20261001k3.zip",
    DL / "pack-completo-offline-v20261001k4.zip",
    DL / "pack-completo-offline-v20261001k2.zip",
    DL / "pack-completo-offline-v20261001k.zip",
]

# Thematic packs → modules/<id>/
THEMATIC = [
    {
        "id": "pack-1eso",
        "zip": "pack-1eso-offline.zip",
        "nombre": "Pack 1º ESO",
        "entrada": "index.html",
        "defaultVisible": True,
        "nota": "limpio v20261001b · 10 ESO + Profesor · sin sexualidad",
    },
    {
        "id": "pack-casa",
        "zip": "pack-casa-offline.zip",
        "nombre": "Pack Casa",
        "entrada": "index.html",
        "defaultVisible": True,
        "nota": "hogar / cocina / música / gym / …",
    },
    {
        "id": "pack-biblioteca",
        "zip": "pack-biblioteca-offline.zip",
        "nombre": "Pack Biblioteca",
        "entrada": "index.html",
        "defaultVisible": True,
        "nota": "~12 MB libros · INSIDE embed",
    },
    {
        "id": "pack-estudio",
        "zip": "pack-estudio-offline.zip",
        "nombre": "Pack Estudio",
        "entrada": "index.html",
        "defaultVisible": True,
        "nota": "tinta / informática / alto rendimiento",
    },
    {
        "id": "pack-utiles",
        "zip": "pack-utiles-offline.zip",
        "nombre": "Pack Útiles",
        "entrada": "index.html",
        "defaultVisible": True,
        "nota": "qr / calc / mapas / guías / reproductor",
    },
    {
        "id": "pack-ocio",
        "zip": "pack-ocio-offline.zip",
        "nombre": "Pack Ocio",
        "entrada": "index.html",
        "defaultVisible": True,
        "nota": "arte / tanteo",
    },
    {
        "id": "pack-midia",
        "zip": "pack-midia-offline.zip",
        "nombre": "Pack Mi día",
        "entrada": "index.html",
        "defaultVisible": True,
        "nota": "mi-dia",
    },
]

FORBIDDEN_NAME_PARTS = (
    "radio",
    "vitaink",
    "privado-jorge",
    "central-cuba",
    "alarma-cuba",
    "sexualidad",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_clean_zip(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            low = name.lower().replace("\\", "/")
            for part in FORBIDDEN_NAME_PARTS:
                if part in low.split("/"):
                    raise SystemExit(f"forbidden path in {zip_path.name}: {name}")


def extract_zip_to(zip_path: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest)


def unpack_pack_into_modules(zip_path: Path, dest: Path) -> None:
    """Extract thematic pack flat into modules/<id>/ (strip single top folder if any)."""
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as zf:
        names = [n for n in zf.namelist() if n and not n.endswith("/")]
        tops = {n.split("/")[0] for n in names}
        # Thematic packs are already flat (ABRE-AQUI, index, module.json, …)
        # Only strip if EVERY file lives under one folder and that folder is not a known root file.
        strip = None
        if len(tops) == 1:
            top = next(iter(tops))
            if top not in {"ABRE-AQUI.html", "index.html", "module.json", "LEEME.txt", "modulos", "educacion"}:
                strip = top + "/"
        for info in zf.infolist():
            name = info.filename
            if name.endswith("/"):
                continue
            if strip:
                if not name.startswith(strip):
                    continue
                rel = name[len(strip) :]
            else:
                rel = name
            if not rel:
                continue
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, open(out, "wb") as dst:
                shutil.copyfileobj(src, dst)




def flatten_shelf_modulos(staging: Path) -> int:
    """Materialize top-level modulos/<id>.html (+ assets) next to estanteria.html.

    Estantería moduleWebPath returns /modulos/<id>.html (absolute). On App
    WebView that hits appassets …/modulos/… which PackExtractor serves from
    contentRoot/modulos/ (or index). Nested modules/pack-*/modulos/** alone
    left top-level count at 0 → ERR_NAME_NOT_RESOLVED.

    Source of truth: repo modulos/ (same tree PWA Completo / EMBED_SOURCES).
    Keeps modules/pack-* for catalogo-embed toggles.
    """
    src = ROOT / "modulos"
    if not src.is_dir():
        raise SystemExit(f"missing shelf modulos source: {src}")
    dest = staging / "modulos"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    # Embed key → file map (canonical shelf set)
    # Prefer importing sibling script
    est_path = ROOT / "scripts" / "build-estanteria-offline.py"
    embed_paths: list[Path] = []
    if est_path.is_file():
        import importlib.util
        spec = importlib.util.spec_from_file_location("_est_embed", est_path)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        embed_paths = list(mod.EMBED_SOURCES.values())
    else:
        embed_paths = sorted(src.glob("*.html"))

    n = 0
    seen: set[str] = set()
    for p in embed_paths:
        p = Path(p)
        if not p.is_file():
            # fallback same name under src
            alt = src / p.name
            if alt.is_file():
                p = alt
            else:
                raise SystemExit(f"shelf module missing: {p}")
        low = p.name.lower()
        if any(part in low for part in FORBIDDEN_NAME_PARTS):
            continue
        out = dest / p.name
        shutil.copy2(p, out)
        seen.add(p.name)
        n += 1

    # biblioteca-libros (relative assets for biblioteca.html)
    books_src = src / "biblioteca-libros"
    if books_src.is_dir():
        books_dest = dest / "biblioteca-libros"
        shutil.copytree(books_src, books_dest, dirs_exist_ok=True)
        n += sum(1 for f in books_dest.rglob("*") if f.is_file())

    # guias-viaje at ZIP root (moduleWebPath special → /guias-viaje/)
    guias_src = ROOT / "guias-viaje"
    if guias_src.is_dir():
        guias_dest = staging / "guias-viaje"
        if guias_dest.exists():
            shutil.rmtree(guias_dest)
        shutil.copytree(guias_src, guias_dest)
        n += sum(1 for f in guias_dest.rglob("*") if f.is_file())

    # Extra published shelf HTML not in EMBED_SOURCES (Completo max set)
    EXTRA_HTML = [
        "aliados.html",
        "apagon.html",
        "caligrafia.html",
        "conducir.html",
        "newpipe.html",
        "oposiciones.html",
    ]
    for name in EXTRA_HTML:
        p = src / name
        if p.is_file() and name not in seen:
            low = name.lower()
            if any(part in low for part in FORBIDDEN_NAME_PARTS):
                continue
            shutil.copy2(p, dest / name)
            seen.add(name)
            n += 1

    # Asset / course directories beside flat HTML (packLocal hrefs)
    EXTRA_DIRS = [
        "arduino",
        "raspberry",
        "robot",
        "conducir",
        "oposiciones",
        "nomenclator",
        "espana-offline",
        "valladolid-offline",
        "podcast",
    ]
    for dname in EXTRA_DIRS:
        dsrc = src / dname
        if not dsrc.is_dir():
            continue
        # never ship QA fixtures
        def _ignore(dirpath, names):
            skip = set()
            if Path(dirpath).name == dname or Path(dirpath).name in {"podcast"}:
                if "_qa" in names:
                    skip.add("_qa")
            for nm in names:
                low = nm.lower()
                if low.endswith((".wav", ".png")) and "_qa" in Path(dirpath).parts:
                    skip.add(nm)
            return skip
        ddest = dest / dname
        if ddest.exists():
            shutil.rmtree(ddest)
        shutil.copytree(dsrc, ddest, ignore=_ignore)
        n += sum(1 for f in ddest.rglob("*") if f.is_file())

    # LEEME-*.txt next to modules (optional docs)
    for p in sorted(src.glob("LEEME-*.txt")):
        low = p.name.lower()
        if any(part in low for part in FORBIDDEN_NAME_PARTS):
            continue
        shutil.copy2(p, dest / p.name)
        n += 1

    # Sanity: bajo + guitarra must exist at flat path
    for must in ("bajo.html", "guitarra.html", "hogar.html"):
        if not (dest / must).is_file():
            raise SystemExit(f"flatten_shelf_modulos: missing {must}")
    if not (dest / "podcast" / "estudio.html").is_file():
        raise SystemExit("flatten_shelf_modulos: missing podcast/estudio.html")
    print(f"  flat modulos/ → {len(seen)} html (+ assets); bajo/guitarra/podcast OK")
    return n



def strip_embed_no_add(html: str) -> str:
    """Remove download/Añadir UI from Completo shell for monolithic embed.

    Keeps parade k5 logic, Módulos/Widgets show-hide, splash, LvBridge TTS.
    Sets EMBED_NO_ADD=1 and EST_BUILD k6 (parade+j scroll+anti-rayas+splash h).
    """
    import re

    # Toolbar: Añadir label + HTML file picker (exact Completo shell)
    html = html.replace(
        '          <label class="file-btn" for="local-file" '
        'title="Abre un módulo HTML descargado de lesvencimos.com">Añadir</label>\n'
        '          <input id="local-file" type="file" accept=".html,.htm,text/html" '
        'aria-label="Añadir módulo HTML descargado de lesvencimos.com">\n',
        '',
    )
    html = html.replace(
        '<label class="file-btn" for="local-file" '
        'title="Abre un módulo HTML descargado de lesvencimos.com">Añadir</label>',
        '',
    )
    html = html.replace(
        '<input id="local-file" type="file" accept=".html,.htm,text/html" '
        'aria-label="Añadir módulo HTML descargado de lesvencimos.com">',
        '',
    )
    # Panel hint: no «Añadir» for novedades
    html = html.replace(
        'También «Añadir» para novedades.',
        'Todo el contenido va en este pack (sin descargas).',
    )
    # Missing-module tip
    html = html.replace(
        "'<p>Si ves esto, abre <strong>ABRE-AQUI.html</strong> del Pack Completo o usa «Añadir».</p>';",
        "'<p>Si ves esto, abre <strong>ABRE-AQUI.html</strong> del Pack Completo embebido.</p>';",
    )
    # Listener → remove leftover nodes if any
    html = html.replace(
        "document.getElementById('local-file').addEventListener('change', onFile);",
        "/* EMBED_NO_ADD */ (function(){ var _lf=document.getElementById('local-file'); "
        "if(_lf) _lf.remove(); var _fe=document.getElementById('file-err'); if(_fe) _fe.remove(); })();",
    )
    # EST_BUILD + flag (keep k5 parade lineage in name)
    html2, n = re.subn(
        r"var EST_BUILD = '[^']+';",
        "var EST_BUILD = 'v20261001k6';\n"
        "    var EMBED_NO_ADD = 1; /* monolithic: no Añadir / file picker / pack download */",
        html,
        count=1,
    )
    if n != 1:
        raise SystemExit('EST_BUILD not found for EMBED_NO_ADD inject')
    html = html2
    # Belt: onFile early-return
    needle = "    function onFile(e) {\n      var err = document.getElementById('file-err');"
    repl = (
        "    function onFile(e) {\n"
        "      if (typeof EMBED_NO_ADD !== 'undefined' && EMBED_NO_ADD) return;\n"
        "      var err = document.getElementById('file-err');"
    )
    if needle in html:
        html = html.replace(needle, repl, 1)
    # Hide any residual file-btn / file input in toolbar CSS
    old_css = (
        "  .desk-toolbar input[type=file] {\n"
        "    position: absolute; width: 1px; height: 1px; opacity: 0; overflow: hidden;\n"
        "  }"
    )
    new_css = (
        "  /* EMBED_NO_ADD: no pack download / HTML file picker */\n"
        "  .desk-toolbar input[type=file],\n"
        "  .desk-toolbar label.file-btn,\n"
        "  #local-file,\n"
        "  #file-err { display: none !important; }"
    )
    if old_css in html:
        html = html.replace(old_css, new_css, 1)
    html = html.replace(
        '/* Pin Añadir bar to top while sheet is open — never buried under the list */',
        '/* Pin toolbar to top while sheet is open — never buried under the list */',
    )
    # Chip tooltips: show/hide wording (not download)
    html = html.replace(
        "b.title = 'Añadir al escritorio · ' + mod.titulo;",
        "b.title = 'Mostrar · ' + mod.titulo;",
        1,
    )
    html = html.replace(
        "b.title = (typeof EMBED_NO_ADD !== 'undefined' && EMBED_NO_ADD "
        "? ('Mostrar · ' + mod.titulo) : ('Añadir al escritorio · ' + mod.titulo));",
        "b.title = 'Mostrar · ' + mod.titulo;",
    )
    html = html.replace(
        '/* layoutRev 42: Añadir + starters offline-safe + splash relative · v20261001a */',
        '/* layoutRev 42: starters offline-safe + splash relative · v20261001a */',
    )
    # Sanity: Añadir button label must be gone
    if '>Añadir</label>' in html or 'id="local-file"' in html:
        raise SystemExit('strip_embed_no_add: Añadir/local-file still present')
    if 'EMBED_NO_ADD' not in html:
        raise SystemExit('strip_embed_no_add: EMBED_NO_ADD flag missing')
    # Flat modulos next to estanteria: use relative URLs so appassets
    # resolves under /completo/modulos/… (not host-root /modulos/ → ERR_NAME_NOT_RESOLVED)
    old_wp = "return '/modulos/' + id + '.html';"
    new_wp = "return 'modulos/' + id + '.html'; /* EMBED flat relative */"
    if old_wp not in html:
        raise SystemExit('strip_embed_no_add: moduleWebPath /modulos/ return not found')
    html = html.replace(old_wp, new_wp, 1)
    # specials that were site-root absolute
    html = html.replace("'alarma-cuba': '/alarma-cuba.html'", "'alarma-cuba': 'alarma-cuba.html'", 1)
    html = html.replace("'guias-viaje': '/guias-viaje/'", "'guias-viaje': 'guias-viaje/'", 1)
    return html


def sync_apk_assets(primary: Path):
    """Copy completo-offline.zip into fat APK assets/embed when present."""
    dest = (
        ROOT
        / "android-cascaron"
        / "app"
        / "src"
        / "main"
        / "assets"
        / "embed"
        / "completo-offline.zip"
    )
    if not dest.parent.is_dir():
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(primary, dest)
    return dest



def write_catalog(modules_meta: list[dict], n_files: int, size_hint: int) -> dict:
    return {
        "id": "completo-offline",
        "nombre": "Completo offline (embed APK)",
        "version": VERSION,
        "entry": "estanteria.html",
        "abre": "ABRE-AQUI.html",
        "apkAssetPath": "assets/embed/completo-offline.zip",
        "layout": "shell+modules",
        "excludes": ["radio", "vitaink", "cuba", "privado-jorge", "download-flow"],
        "modules": modules_meta,
        "files": n_files,
        "bytesHint": size_hint,
        "nota": (
            "Monolithic embed: Estantería Completo (parade) + 7 packs under modules/. "
            "App shows/hides modules via this catalog; no download flow."
        ),
    }


def write_leeme(size_bytes: int, n_files: int, module_ids: list[str]) -> str:
    mb = size_bytes / (1024 * 1024)
    mods = "\n".join(f"  · modules/{mid}/" for mid in module_ids)
    warn = ""
    if size_bytes > SOFT_WARN_BYTES:
        warn = (
            f"\n⚠ SOFT WARN: ZIP ~{mb:.1f} MB > 70 MB. "
            "Target APK sigue < 80–100 MB; revisar con App.\n"
        )
    return f"""═══════════════════════════════════════
  COMPLETO OFFLINE — EMBED APK
  Build {VERSION}
  Shell Completo + 7 packs thematic
═══════════════════════════════════════

Canónico para App APK:
  assets/embed/completo-offline.zip
  (= downloads/completo-offline.zip)

También alias:
  downloads/pack-completo-offline.zip

Entrada WebView (tras descomprimir en filesDir / assets):
  ABRE-AQUI.html  →  estanteria.html
  (parade Completo / Estantería k5 + educación)

Contiene:
  · estanteria.html     → shell Completo (56 embeds + Educación packLocal)
  · educacion/          → Profesor + 10×1º ESO limpio + Linux
  · brand/splash/       → vídeo + sonido
  · modulos/<id>.html   → flat shelf modules (App /modulos/ + relative)
  · guias-viaje/        → special shelf path
  · modules/<id>/       → packs thematic completos (App toggle)
{mods}
  · catalogo-embed.json → ids para UI show/hide
  · LEEME.txt

Biblioteca (~12 MB) VA DENTRO (modules/pack-biblioteca/).

EXCLUIDO: radio, vitaink, cuba, privado-jorge, UI de descarga/Añadir/file picker.
Shell: EMBED_NO_ADD=1 · EST_BUILD k6 (parade k5 + j scroll + anti-rayas + splash h + flat modulos/).

Archivos en el ZIP: {n_files}
Tamaño comprimido: ~{mb:.1f} MB
{warn}
─── App APK ───

1) Embebe downloads/completo-offline.zip en assets/embed/completo-offline.zip
2) Al primer arranque: descomprime a filesDir (o sirve desde assets)
3) WebView entry: estanteria.html (o ABRE-AQUI.html)
4) Lee catalogo-embed.json para toggles de visibilidad de modules/*
5) Sin red. Sin flujo «Descargar pack» / «Añadir» / file picker.
6) catalogo-embed.json solo para show/hide de icons (no install-from-url).

No es el ZIP legado lesvencimos-completo.zip.
lesvencimos.com
"""



def sync_live_educacion_bach(staging: Path) -> None:
    """Overlay live educacion Bach (+ shared assets) so Maestro/_maestro is in the ZIP.

    Base fat shells keep stale Bach HTML pointing at ../../../../profesor/_maestro
    (missing inside APK). Source of truth: repo educacion/<curso>/ with local _maestro/.
    """
    src_root = ROOT / "educacion"
    dst_root = staging / "educacion"
    if not src_root.is_dir() or not dst_root.is_dir():
        raise SystemExit("sync_live_educacion_bach: missing educacion/")
    courses = [
        "mates-i", "bgca", "griego", "ingles", "mates-gen", "fyq", "edfisica",
        "mates-ccs", "dibujo-tec", "economia", "tic",
    ]
    for name in courses:
        src = src_root / name
        if not src.is_dir():
            print(f"  WARN skip missing educacion/{name}")
            continue
        dst = dst_root / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "_gen"))
        print(f"  synced educacion/{name}/")
    # Profesor hub if present live
    for hub in ("Profesor.html",):
        sp = src_root / hub
        if sp.is_file():
            shutil.copy2(sp, dst_root / hub)


def sync_1eso_shell_chrome(staging: Path) -> None:
    """Apply lv-chrome-2026 plantilla shell to all 1º ESO flat packs in the embed.

    Flat 1ESO packs historically kept an older leccion-shell.css with
    color: var(--lv-azul) on links/h3/etiquetas (cheap hyperlink look).
    Source of truth: profesor/_plantilla-leccion/leccion-shell.css (carbón/ámbar).
    """
    src = ROOT / "profesor" / "_plantilla-leccion" / "leccion-shell.css"
    if not src.is_file():
        raise SystemExit(f"sync_1eso_shell_chrome: missing {src}")
    targets: list[Path] = []
    edu = staging / "educacion"
    if edu.is_dir():
        targets.extend(sorted(edu.glob("1eso-*/leccion-shell.css")))
    pack = staging / "modules" / "pack-1eso" / "educacion"
    if pack.is_dir():
        targets.extend(sorted(pack.glob("1eso-*/leccion-shell.css")))
    if not targets:
        raise SystemExit("sync_1eso_shell_chrome: no 1eso leccion-shell.css targets")
    data = src.read_bytes()
    if b"lv-chrome-2026" not in data:
        raise SystemExit("sync_1eso_shell_chrome: plantilla missing lv-chrome-2026")
    for dst in targets:
        dst.write_bytes(data)
    print(f"  synced lv-chrome shell → {len(targets)} 1eso leccion-shell.css")


def force_sync_jardin(staging: Path) -> None:
    """Always take live modulos/jardin.html (195KB+) — never keep stale embed ~111KB."""
    src = ROOT / "modulos" / "jardin.html"
    if not src.is_file():
        raise SystemExit(f"force_sync_jardin: missing {src}")
    size = src.stat().st_size
    if size < 150_000:
        raise SystemExit(f"force_sync_jardin: live jardin too small ({size} bytes) — expected ~195KB")
    targets = [
        staging / "modulos" / "jardin.html",
        staging / "modules" / "pack-casa" / "modulos" / "jardin.html",
    ]
    for t in targets:
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, t)
        print(f"  forced jardin.html → {t.relative_to(staging)} ({t.stat().st_size} bytes)")
    # LEEME if present
    leeme = ROOT / "modulos" / "LEEME-jardin.txt"
    if leeme.is_file():
        for t in [
            staging / "modulos" / "LEEME-jardin.txt",
            staging / "modules" / "pack-casa" / "modulos" / "LEEME-jardin.txt",
        ]:
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(leeme, t)
    # offline zip into downloads path inside pack if we keep downloads/ copies elsewhere — shelf uses html
    zip_src = ROOT / "downloads" / "jardin-offline.zip"
    if zip_src.is_file():
        # optional: not required inside embed APK for WebView shelf
        pass


def zip_tree(src: Path, out: Path) -> list[str]:
    if out.exists():
        out.unlink()
    names: list[str] = []
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(src.rglob("*")):
            if path.is_file():
                arc = path.relative_to(src).as_posix()
                zf.write(path, arcname=arc)
                names.append(arc)
    return names


def maybe_rebuild_shell() -> None:
    script = ROOT / "scripts" / "build-pack-completo.py"
    print("== Rebuilding shell via build-pack-completo.py ==")
    subprocess.check_call([sys.executable, str(script)], cwd=str(ROOT))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--rebuild-shell",
        action="store_true",
        help="Run build-pack-completo.py before assembling embed ZIP",
    )
    args = ap.parse_args()

    if args.rebuild_shell:
        maybe_rebuild_shell()

    shell_zip = None
    for cand in SHELL_CANDIDATES:
        if cand.exists():
            shell_zip = cand
            break
    if shell_zip is None:
        # Fall back to alias only if it is still a thin shell (no modules/)
        alias = DL / "pack-completo-offline.zip"
        if alias.exists():
            with zipfile.ZipFile(alias) as zf:
                names = zf.namelist()
            if any(n.startswith("modules/") for n in names):
                raise SystemExit(
                    "pack-completo-offline.zip already has modules/ and no thin "
                    "k3 snapshot found — pass --rebuild-shell or restore "
                    "pack-completo-offline-v20261001k4.zip"
                )
            shell_zip = alias
    if shell_zip is None or not shell_zip.exists():
        raise SystemExit(
            "missing shell base — run scripts/build-pack-completo.py "
            "or pass --rebuild-shell"
        )

    print(f"== Base shell ZIP: {shell_zip.name} ({shell_zip.stat().st_size} bytes) ==")
    assert_clean_zip(shell_zip)

    if STAGING.exists():
        shutil.rmtree(STAGING)
    print("== Extract shell Completo ==")
    extract_zip_to(shell_zip, STAGING)

    # Required shell entry
    if not (STAGING / "estanteria.html").is_file():
        raise SystemExit("shell ZIP missing estanteria.html")
    if not (STAGING / "ABRE-AQUI.html").is_file():
        raise SystemExit("shell ZIP missing ABRE-AQUI.html")
    if not (STAGING / "educacion").is_dir():
        raise SystemExit("shell ZIP missing educacion/")

    # Prefer LIVE repo estanteria (layoutRev / new shelf icons), then strip embed UI
    live_est = ROOT / "estanteria.html"
    est_path = STAGING / "estanteria.html"
    if live_est.is_file():
        print("== Overlay live estanteria.html ==")
        est_html = live_est.read_text(encoding="utf-8")
    else:
        est_html = est_path.read_text(encoding="utf-8")
    print("== Strip EMBED_NO_ADD (Añadir / file picker) ==")
    est_path.write_text(strip_embed_no_add(est_html), encoding="utf-8")

    modules_dir = STAGING / "modules"
    modules_dir.mkdir(parents=True, exist_ok=True)

    modules_meta: list[dict] = []
    base_has_modules = any(modules_dir.glob("pack-*"))
    if base_has_modules:
        print("== Base already has modules/ (previous fat embed) — keep + refresh meta ==")
        for spec in THEMATIC:
            dest = modules_dir / spec["id"]
            if not dest.is_dir():
                print(f"  WARN missing modules/{spec['id']}/ — will unpack")
                base_has_modules = False
                break
            meta = {
                "id": spec["id"],
                "nombre": spec["nombre"],
                "path": f"modules/{spec['id']}/",
                "entrada": spec["entrada"],
                "defaultVisible": spec["defaultVisible"],
                "nota": spec["nota"],
                "bytes": sum(p.stat().st_size for p in dest.rglob("*") if p.is_file()),
            }
            modules_meta.append(meta)

    if not base_has_modules:
        modules_meta = []
        print("== Unpack 7 thematic packs → modules/<id>/ ==")
        for spec in THEMATIC:
            zpath = DL / spec["zip"]
            if not zpath.exists():
                raise SystemExit(f"missing thematic pack: {zpath}")
            assert_clean_zip(zpath)
            dest = modules_dir / spec["id"]
            print(f"  {spec['zip']} → modules/{spec['id']}/")
            unpack_pack_into_modules(zpath, dest)
            entrada = dest / spec["entrada"]
            if not entrada.is_file():
                # fallback ABRE-AQUI
                if (dest / "ABRE-AQUI.html").is_file():
                    spec = {**spec, "entrada": "ABRE-AQUI.html"}
                else:
                    raise SystemExit(f"no entry HTML in modules/{spec['id']}/")
            # strip download-flow wording from pack LEEME is optional; keep as-is
            meta = {
                "id": spec["id"],
                "nombre": spec["nombre"],
                "path": f"modules/{spec['id']}/",
                "entrada": spec["entrada"],
                "defaultVisible": spec["defaultVisible"],
                "nota": spec["nota"],
                "bytes": sum(p.stat().st_size for p in dest.rglob("*") if p.is_file()),
            }
            # refresh module.json sha placeholder if present
            mj = dest / "module.json"
            if mj.is_file():
                try:
                    data = json.loads(mj.read_text(encoding="utf-8"))
                    data["embed"] = True
                    data["path"] = meta["path"]
                    mj.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                except json.JSONDecodeError:
                    pass
            modules_meta.append(meta)

    print("== Flatten shelf modulos/ at ZIP root (estantería paths) ==")
    flatten_shelf_modulos(STAGING)

    # Keep mi-dia from pack-midia at flat path (not in repo modulos/)
    midia_src = STAGING / "modules" / "pack-midia" / "modulos" / "mi-dia.html"
    if midia_src.is_file():
        shutil.copy2(midia_src, STAGING / "modulos" / "mi-dia.html")
        print("  copied mi-dia.html from pack-midia")

    # Sync biblioteca-libros (Celestina completa, etc.) into thematic pack copy
    books_src = ROOT / "modulos" / "biblioteca-libros"
    biblio_html = ROOT / "modulos" / "biblioteca.html"
    for pack_books in [
        STAGING / "modules" / "pack-biblioteca" / "modulos" / "biblioteca-libros",
        STAGING / "modulos" / "biblioteca-libros",
    ]:
        if books_src.is_dir():
            if pack_books.exists():
                shutil.rmtree(pack_books)
            pack_books.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(books_src, pack_books)
            print(f"  synced biblioteca-libros → {pack_books.relative_to(STAGING)}")
    for pack_html in [
        STAGING / "modules" / "pack-biblioteca" / "modulos" / "biblioteca.html",
        STAGING / "modulos" / "biblioteca.html",
    ]:
        if biblio_html.is_file():
            pack_html.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(biblio_html, pack_html)

    print("== Sync live educacion Bach (Maestro local _maestro) ==")
    sync_live_educacion_bach(STAGING)
    print("== Sync 1eso shell chrome (no blue link headers) ==")
    sync_1eso_shell_chrome(STAGING)
    print("== Force sync jardin.html from live modulos/ ==")
    force_sync_jardin(STAGING)

    # Count files before catalog/LEEME finalize
    files = [p for p in STAGING.rglob("*") if p.is_file()]
    # provisional catalog
    catalog = write_catalog(modules_meta, len(files) + 2, 0)
    (STAGING / "catalogo-embed.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    module_ids = [m["id"] for m in modules_meta]
    (STAGING / "LEEME.txt").write_text(
        write_leeme(0, len(files) + 1, module_ids), encoding="utf-8"
    )

    print("== Zip completo-offline.zip ==")
    names = zip_tree(STAGING, PRIMARY)
    size = PRIMARY.stat().st_size

    # Rewrite LEEME + catalog with real size
    catalog = write_catalog(modules_meta, len(names), size)
    catalog_json = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
    leeme = write_leeme(size, len(names), module_ids)
    (STAGING / "catalogo-embed.json").write_text(catalog_json, encoding="utf-8")
    (STAGING / "LEEME.txt").write_text(leeme, encoding="utf-8")
    (DL / "LEEME-completo-embed.txt").write_text(leeme, encoding="utf-8")
    (DL / "LEEME-pack-completo.txt").write_text(leeme, encoding="utf-8")

    # Re-zip with final LEEME/catalog
    names = zip_tree(STAGING, PRIMARY)
    size = PRIMARY.stat().st_size
    shutil.copy2(PRIMARY, SNAPSHOT)
    shutil.copy2(PRIMARY, ALIAS)

    apk_asset = sync_apk_assets(PRIMARY)
    pe = ROOT / "android-cascaron" / "app" / "src" / "main" / "java" / "com" / "lesvencimos" / "cascaron" / "PackExtractor.java"
    if pe.is_file():
        pe_txt = pe.read_text(encoding="utf-8")
        import re as _re
        pe_new, n_pe = _re.subn(
            r'(\?\s*"v20261001k6"\s*:\s*")([^"]+)(")',
            rf'\g<1>{VERSION}\3',
            pe_txt,
            count=1,
        )
        if n_pe != 1:
            pe_new, n_pe = _re.subn(
                r'public static final String EXPECTED_VERSION = "[^"]+";',
                f'public static final String EXPECTED_VERSION = "{VERSION}";',
                pe_txt,
                count=1,
            )
        if n_pe == 1 and pe_new != pe_txt:
            pe.write_text(pe_new, encoding="utf-8")
            print(f"== PackExtractor.EXPECTED_VERSION → {VERSION} ==")
        elif n_pe != 1:
            print("WARN: PackExtractor.EXPECTED_VERSION not updated")

    digest_sha = sha256_file(PRIMARY)
    digest_md5 = md5_file(PRIMARY)

    # Presence checks
    must = [
        "estanteria.html",
        "ABRE-AQUI.html",
        "catalogo-embed.json",
        "educacion/Profesor.html",
        "educacion/1eso-matematicas/index.html",
        "modules/pack-1eso/index.html",
        "modules/pack-casa/index.html",
        "modules/pack-biblioteca/index.html",
        "modules/pack-biblioteca/modulos/biblioteca-libros/catalog.json",
        "modules/pack-estudio/index.html",
        "modules/pack-utiles/index.html",
        "modules/pack-ocio/index.html",
        "modules/pack-midia/index.html",
        "modules/pack-midia/modulos/mi-dia.html",
        "modulos/bajo.html",
        "modulos/guitarra.html",
        "modulos/hogar.html",
        "modulos/biblioteca.html",
        "modulos/biblioteca-libros/catalog.json",
        "modulos/biblioteca-libros/celestina-1.json",
        "modulos/biblioteca-libros/celestina-11.json",
        "modulos/podcast/estudio.html",
        "modulos/podcast/efectos.js",
        "modulos/podcast/sonido/lv-podcast-audio.js",
        "modulos/conducir.html",
        "modulos/oposiciones.html",
        "modulos/aliados.html",
        "modulos/grabadora.html",
        "modulos/jardin.html",
        "educacion/mates-i/index.html",
        "educacion/mates-i/_maestro/maestro-runtime.js",
        "educacion/mates-i/lecciones/leccion-02-logaritmos.html",
        "educacion/fyq/_maestro/maestro-runtime.js",
        "educacion/bgca/_maestro/maestro-runtime.js",
        "educacion/mates-gen/_maestro/maestro-runtime.js",
        "educacion/edfisica/_maestro/maestro-runtime.js",
    ]
    name_set = set(names)
    for m in must:
        if m not in name_set:
            raise SystemExit(f"ZIP missing required entry: {m}")

    # Soft warn
    if size > SOFT_WARN_BYTES:
        print(f"SOFT WARN: ZIP {size} bytes ({size/1024/1024:.1f} MB) > 70 MB")


    # Maestro Bach + jardin content gates (APK WebView)
    with zipfile.ZipFile(PRIMARY) as zf:
        sample = zf.read("educacion/mates-i/lecciones/leccion-02-logaritmos.html").decode("utf-8", "replace")
        if "atajo-maestro" not in sample or "_maestro/maestro-runtime.js" not in sample:
            raise SystemExit("ZIP mates-i L02 missing Maestro markers")
        if "profesor/_maestro" in sample:
            raise SystemExit("ZIP mates-i L02 still points at profesor/_maestro")
        jardin_info = zf.getinfo("modulos/jardin.html")
        if jardin_info.file_size < 150_000:
            raise SystemExit(f"ZIP jardin.html too small: {jardin_info.file_size}")
        # count maestro runtimes under educacion Bach
        bach_rt = [n for n in zf.namelist() if n.startswith("educacion/") and n.endswith("/_maestro/maestro-runtime.js")]
        if len(bach_rt) < 5:
            raise SystemExit(f"ZIP expected >=5 Bach _maestro runtimes, got {len(bach_rt)}: {bach_rt}")
        print(f"MAESTRO_BACH_RUNTIMES {len(bach_rt)}")
        print(f"JARDIN_BYTES {jardin_info.file_size}")
        eso_shell = zf.read("educacion/1eso-matematicas/leccion-shell.css")
        if b"lv-chrome-2026" not in eso_shell:
            raise SystemExit("ZIP 1eso-matematicas leccion-shell.css missing lv-chrome-2026")
        if b"color: var(--lv-azul)" in eso_shell.split(b"lv-chrome-2026")[0]:
            # azul before chrome block on .leccion-shell a is the old bug
            head = eso_shell.split(b"lv-chrome-2026")[0]
            if b".leccion-shell a" in head and b"color: var(--lv-azul)" in head:
                raise SystemExit("ZIP 1eso shell still has azul link color before chrome block")


    print("---")
    print(f"PRIMARY  {PRIMARY}")
    print(f"ALIAS    {ALIAS}")
    print(f"SNAPSHOT {SNAPSHOT}")
    print(f"VERSION  {VERSION}")
    print(f"BYTES    {size}")
    print(f"MB       {size/1024/1024:.2f}")
    print(f"FILES    {len(names)}")
    print(f"SHA256   {digest_sha}")
    print(f"MD5      {digest_md5}")
    print(f"ENTRY    estanteria.html (ABRE-AQUI.html → redirect)")
    print(f"MODULES  {', '.join(module_ids)}")
    print(f"BIBLIOTECA_INCLUDED  yes (~12MB pack inside modules/pack-biblioteca/)")
    print(f"EMBED_NO_ADD  yes (Añadir/file picker stripped; parade k6)")
    print(f"FLAT_MODULOS  yes (modulos/bajo.html + shelf at ZIP root; relative moduleWebPath)")
    if apk_asset:
        print(f"APK_ASSET {apk_asset} ({apk_asset.stat().st_size} bytes)")
    print("OK")


if __name__ == "__main__":
    main()
