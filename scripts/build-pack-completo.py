#!/usr/bin/env python3
"""Build Pack Completo offline: Estantería (56 embeds) + Educación (10 ESO + Profesor + Linux).

Output:
  downloads/pack-completo-offline.zip
  downloads/pack-completo-offline-vYYYYMMDDx.zip
  downloads/LEEME-pack-completo.txt

Does NOT touch privado-jorge. Does NOT promote lesvencimos-completo.zip (legacy).
Radio / Cuba / Vitaink stay out (novedades vía Añadir).
"""
from __future__ import annotations

import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "downloads"
SHELL_SRC = ROOT / "offline-estanteria" / "estanteria.shell.html"
STAGING = ROOT / "offline-pack-completo"
OUT = DL / "pack-completo-offline.zip"
VERSION = "v20261001k6"
SNAPSHOT = DL / f"pack-completo-offline-{VERSION}.zip"

# Reuse embed map from the Estantería builder (single source of truth).
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "build_estanteria_offline", ROOT / "scripts" / "build-estanteria-offline.py"
)
_est = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_est)
EMBED_SOURCES = _est.EMBED_SOURCES
inject_embedded = _est.inject_embedded
build_embedded = _est.build_embedded

# catalog id -> relative pack path (under educacion/)
SCHOOL_PACKS = [
    {
        "id": "profesor",
        "titulo": "Profesor",
        "icon": "profesor",
        "href": "educacion/Profesor.html",
        "blurb": "Hub · en el pack",
        "shape": "billboard",
        "color": "#E8B84A",
    },
    {
        "id": "mate-1eso",
        "titulo": "Mates",
        "icon": "mates",
        "href": "educacion/1eso-matematicas/index.html",
        "blurb": "1º ESO · en el pack",
        "shape": "wide",
        "color": "#2B7FFF",
        "zip": "1eso-matematicas-offline.zip",
        "dest": "1eso-matematicas",
    },
    {
        "id": "lengua-1eso",
        "titulo": "Lengua",
        "icon": "lengua",
        "href": "educacion/1eso-lengua-castellana/index.html",
        "blurb": "1º ESO · en el pack",
        "shape": "wide",
        "color": "#9B59D0",
        "zip": "1eso-lengua-castellana-offline.zip",
        "dest": "1eso-lengua-castellana",
    },
    {
        "id": "byg-1eso",
        "titulo": "Biología",
        "icon": "bio",
        "href": "educacion/1eso-biologia-geologia/index.html",
        "blurb": "ByG 1º ESO · en el pack",
        "shape": "wide",
        "color": "#3CB371",
        "zip": "1eso-biologia-geologia-offline.zip",
        "dest": "1eso-biologia-geologia",
    },
    {
        "id": "geo-1eso",
        "titulo": "Geo e Historia",
        "icon": "geo",
        "href": "educacion/1eso-geografia-historia/index.html",
        "blurb": "1º ESO · en el pack",
        "shape": "wide",
        "color": "#E8763A",
        "zip": "1eso-geografia-historia-offline.zip",
        "dest": "1eso-geografia-historia",
    },
    {
        "id": "plastica-1eso",
        "titulo": "Plástica",
        "icon": "plastica",
        "href": "educacion/1eso-plastica-visual/index.html",
        "blurb": "1º ESO · en el pack",
        "shape": "soft",
        "color": "#FF6B6B",
        "zip": "1eso-plastica-visual-offline.zip",
        "dest": "1eso-plastica-visual",
    },
    {
        "id": "ingles-1eso",
        "titulo": "Inglés",
        "icon": "lengua",
        "href": "educacion/1eso-ingles/index.html",
        "blurb": "1º ESO · en el pack",
        "shape": "wide",
        "color": "#4A90D9",
        "zip": "1eso-ingles-offline.zip",
        "dest": "1eso-ingles",
        "new": True,
    },
    {
        "id": "frances-1eso",
        "titulo": "Francés",
        "icon": "lengua",
        "href": "educacion/1eso-frances/index.html",
        "blurb": "1º ESO · en el pack",
        "shape": "wide",
        "color": "#5B8DEF",
        "zip": "1eso-frances-offline.zip",
        "dest": "1eso-frances",
        "new": True,
    },
    {
        "id": "edfis-1eso",
        "titulo": "Ed. Física",
        "icon": "gimnasio",
        "href": "educacion/1eso-educacion-fisica/index.html",
        "blurb": "1º ESO · en el pack",
        "shape": "soft",
        "color": "#2ECC71",
        "zip": "1eso-educacion-fisica-offline.zip",
        "dest": "1eso-educacion-fisica",
        "new": True,
    },
    {
        "id": "religion-1eso",
        "titulo": "Religión",
        "icon": "profesor",
        "href": "educacion/1eso-religion/index.html",
        "blurb": "1º ESO · en el pack",
        "shape": "soft",
        "color": "#C4A15A",
        "zip": "1eso-religion-offline.zip",
        "dest": "1eso-religion",
        "new": True,
    },
    {
        "id": "altrelig-1eso",
        "titulo": "Alt. Religión",
        "icon": "profesor",
        "href": "educacion/1eso-alternativa-religion/index.html",
        "blurb": "1º ESO · en el pack",
        "shape": "soft",
        "color": "#A0896A",
        "zip": "1eso-alternativa-religion-offline.zip",
        "dest": "1eso-alternativa-religion",
        "new": True,
    },
    {
        "id": "linux-essentials",
        "titulo": "Linux",
        "icon": "linux",
        "href": "educacion/linux-essentials/linux-essentials.html",
        "blurb": "Essentials · en el pack",
        "shape": "soft",
        "color": "#F0B429",
    },
]

SCHOOL_IDS = [p["id"] for p in SCHOOL_PACKS]


def catalog_object(p: dict) -> str:
    return (
        "{ id: '%(id)s', titulo: '%(titulo)s', icon: '%(icon)s', embed: null, "
        "external: false, packLocal: true, href: '%(href)s', "
        "blurb: '%(blurb)s', shelf: 'varios', shape: '%(shape)s', color: '%(color)s' }"
        % p
    )


def patch_shell(shell: str) -> str:
    """Make Educación packs open from relative paths inside the Completo ZIP."""

    # 1) Replace existing school catalog entries
    for p in SCHOOL_PACKS:
        if p.get("new"):
            continue
        pat = re.compile(r"\{ id: '" + re.escape(p["id"]) + r"'[^}]+\}")
        ms = list(pat.finditer(shell))
        if not ms:
            raise SystemExit(f"catalog entry missing: {p['id']}")
        # Replace only the main CATALOG object (first match with titulo)
        replaced = 0
        for m in ms:
            chunk = m.group(0)
            if "titulo:" in chunk or "href:" in chunk:
                shell = shell[: m.start()] + catalog_object(p) + shell[m.end() :]
                replaced += 1
                break
        if not replaced:
            raise SystemExit(f"could not patch catalog for {p['id']}")

    # 2) Insert new subject entries after plastica-1eso in CATALOG
    new_objs = [catalog_object(p) for p in SCHOOL_PACKS if p.get("new")]
    insert_block = ",\n      ".join(new_objs)
    marker = catalog_object(next(p for p in SCHOOL_PACKS if p["id"] == "plastica-1eso"))
    # After patching, plastica line is the new object; find it and insert after
    plastica_new = catalog_object(next(p for p in SCHOOL_PACKS if p["id"] == "plastica-1eso"))
    if plastica_new not in shell:
        raise SystemExit("plastica catalog patch missing before insert")
    # Avoid double-insert on re-run
    if "ingles-1eso" not in shell:
        shell = shell.replace(plastica_new, plastica_new + ",\n      " + insert_block, 1)

    # 3) SCHOOL_IDS (both declarations)
    school_list = "[" + ", ".join(f"'{i}'" for i in SCHOOL_IDS) + "]"
    shell = re.sub(
        r"var SCHOOL_IDS = \[[^\]]+\];",
        f"var SCHOOL_IDS = {school_list};",
        shell,
        count=1,
    )
    shell = re.sub(
        r"var schoolIds = \[[^\]]+\]",
        f"var schoolIds = {school_list}",
        shell,
    )

    # 4) PRESETS.educacion + estudio get new subjects
    edu_ids = SCHOOL_IDS + ["calculadora", "tinta-escritura", "tinta-estudio"]
    edu_list = "[" + ", ".join(f"'{i}'" for i in edu_ids) + "]"
    shell = re.sub(
        r"educacion:\s*\[[^\]]+\]",
        f"educacion: {edu_list}",
        shell,
        count=1,
    )
    # estudio: keep core + add ingles
    shell = re.sub(
        r"estudio:\s*\[[^\]]+\]",
        "estudio: ['tinta-escritura', 'ideas', 'tinta-estudio', 'profesor', "
        "'mate-1eso', 'lengua-1eso', 'ingles-1eso', 'calculadora', 'informatica', "
        "'biblioteca', 'qr']",
        shell,
        count=1,
    )

    # 5) isOfflineEmbed: include packLocal siblings
    old_iso = """function isOfflineEmbed(mod) {
      if (!mod || !mod.embed) return false;
      if (mod.openNative || mod.external) return false;
      try {
        if (typeof EMBEDDED === 'undefined' || !EMBEDDED) return !!mod.embed;
        return !!EMBEDDED[mod.embed];
      } catch (e) { return !!mod.embed; }
    }"""
    new_iso = """function isOfflineEmbed(mod) {
      if (!mod) return false;
      if (mod.openNative || mod.external) return false;
      /* Pack Completo: Educación / Profesor viven como HTML hermanos */
      if (mod.packLocal && mod.href) return true;
      if (!mod.embed) return false;
      try {
        if (typeof EMBEDDED === 'undefined' || !EMBEDDED) return !!mod.embed;
        return !!EMBEDDED[mod.embed];
      } catch (e) { return !!mod.embed; }
    }"""
    if old_iso not in shell:
        raise SystemExit("isOfflineEmbed block not found for patch")
    shell = shell.replace(old_iso, new_iso, 1)

    # 6) openModule: open packLocal relative href before external tip
    old_open = """      /* Online hub URL (Educación packs, Profesor…) — before ZIP tip */
      if (href && isHttp) {
        showModuleViewerUrl(title, href, embedKey);
        return;
      }

      if (cat.external || it.external) {
        var tip = '<h2>' + escapeHtml(title) + '</h2>' +
          '<p>Este módulo es grande y va en un ZIP aparte (no cabe cómodo en el HTML único).</p>' +
          '<p>Descárgalo desde <strong>lesvencimos.com/descargas.html</strong> → Profesor / Educación según corresponda, ' +
          'descomprime y ábrelos con «Añadir» arriba, uno cada vez.</p>' +
          '<p>Los demás módulos (Gimnasio, Guitarra, Caja fuerte, Calculadora…) ya están <strong>dentro de este mismo archivo</strong>.</p>';
        if (location.protocol === 'content:') {
          tip += '<p><strong>Tip:</strong> aunque estés en content://, los módulos embebidos sí abren aquí. ' +
            'Para Profesor aparte, mejor file:// desde Archivos.</p>';
        }
        showModuleViewer(title, null, tip);
        return;
      }"""
    new_open = """      /* Pack Completo: Educación / Profesor como rutas relativas (file:// o http local) */
      if ((cat.packLocal || it.packLocal) && href) {
        showModuleViewerUrl(title, href, embedKey);
        return;
      }

      /* Online hub URL */
      if (href && isHttp) {
        showModuleViewerUrl(title, href, embedKey);
        return;
      }

      if (cat.external || it.external) {
        var tip = '<h2>' + escapeHtml(title) + '</h2>' +
          '<p>Este módulo no está en este pack. En Pack Completo ya van Profesor y 1º ESO dentro.</p>' +
          '<p>Si ves esto, abre <strong>ABRE-AQUI.html</strong> del Pack Completo o usa «Añadir».</p>';
        showModuleViewer(title, null, tip);
        return;
      }"""
    if old_open not in shell:
        raise SystemExit("openModule educación block not found for patch")
    shell = shell.replace(old_open, new_open, 1)

    # 7) Soften UI copy that says Profesor is separate download
    shell = shell.replace(
        "Profesor es descarga aparte. También «Añadir» (HTML de lesvencimos.com).",
        "Profesor y 1º ESO van en este Pack Completo (carpeta Educación). También «Añadir» para novedades.",
    )
    shell = shell.replace(
        'title="Disposición Completo: solo módulos embebidos offline"',
        'title="Disposición Completo: embebidos + Educación del pack"',
    )

    # 8) When pushing school items, copy packLocal flag
    shell = shell.replace(
        "external: mod.external || null,\n                openNative: mod.openNative || null,",
        "external: mod.external || null,\n                packLocal: mod.packLocal || null,\n                openNative: mod.openNative || null,",
    )
    # fillDesktop / applyPreset push paths (slightly different indent)
    shell = shell.replace(
        "external: mod.external || null,\n          openNative: mod.openNative || null,",
        "external: mod.external || null,\n          packLocal: mod.packLocal || null,\n          openNative: mod.openNative || null,",
    )

    if "packLocal: true" not in shell:
        raise SystemExit("packLocal flag missing after patch")
    if "ingles-1eso" not in shell:
        raise SystemExit("ingles-1eso not inserted")
    if "Descárgalo desde <strong>lesvencimos.com/descargas.html</strong> → Profesor" in shell:
        raise SystemExit("old download tip still present in openModule")

    return shell


def write_leeme(size_bytes: int, n_files: int) -> str:
    mb = size_bytes / (1024 * 1024)
    return f"""═══════════════════════════════════════
  PACK COMPLETO — Les vencimos
  Build {VERSION}
  Estantería + Educación offline
═══════════════════════════════════════

Este ZIP es la aplicación base CON TODO lo ya hecho:
  · Estantería / Escritorio (56 módulos embebidos)
  · Profesor (hub)
  · 1º ESO: Mate, Lengua, ByG, Geo, Inglés, Francés,
    Plástica, Ed. Física, Religión, Alt. Religión
  · Linux essentials

NO hace falta red después de descomprimir.
Las NOVEDADES futuras se añaden aparte con «Añadir»
(Radio, Alarma Cuba, Vitaink, etc. NO van en este pack).

─── Contenido ───

  ABRE-AQUI.html     → abre esto (redirige a la Estantería)
  estanteria.html    → Escritorio con módulos dentro
  brand/splash/      → vídeo + sonido de entrada
  educacion/         → Profesor + packs 1º ESO + Linux
  LEEME.txt          → este archivo

Archivos en el ZIP: {n_files}
Tamaño comprimido: ~{mb:.1f} MB

─── Android ───

1) Descomprime con Mis archivos / Archivos.
2) Entra en la carpeta del pack.
3) Toca ABRE-AQUI.html → Chrome / Samsung Internet.
4) Debe verse Offline · file://
5) Carpeta Educación (balda Varios): packs escolares.
6) Novedades: «Añadir» arriba.

La app es Estantería / Completo (este ZIP). Embebe o copia
downloads/pack-completo-offline.zip como contenido base;
las novedades siguen el canal «Añadir». No es un cascarón vacío.

No es el ZIP legado lesvencimos-completo.zip.
lesvencimos.com
"""


def thin_abre_aqui() -> str:
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="0; url=estanteria.html">
  <title>Les vencimos — Pack Completo</title>
  <style>
    html,body{margin:0;min-height:100%;background:#0E0E0C;color:#E6E1D6;
      font:1rem/1.45 system-ui,sans-serif;display:flex;align-items:center;justify-content:center}
    a{color:#C4A15A;font-weight:700}
  </style>
  <script>location.replace("estanteria.html");</script>
</head>
<body>
  <p>Abriendo Pack Completo… <a href="estanteria.html">Entrar</a></p>
</body>
</html>
"""


def unzip_flat_to(zip_path: Path, dest_dir: Path) -> None:
    """Extract flat pack; strip top-level *-offline/ folder into dest_dir."""
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        # detect single top folder
        tops = {n.split("/")[0] for n in names if n and not n.endswith("/")}
        tops |= {n.rstrip("/").split("/")[0] for n in names if n.endswith("/") and n.count("/") == 1}
        tops = {t for t in tops if t}
        if len(tops) == 1:
            top = next(iter(tops))
            prefix = top + "/"
            for info in zf.infolist():
                name = info.filename
                if name.endswith("/") or name == top or name == prefix:
                    continue
                if not name.startswith(prefix):
                    continue
                rel = name[len(prefix) :]
                out = dest_dir / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(info) as src, open(out, "wb") as dst:
                    shutil.copyfileobj(src, dst)
        else:
            zf.extractall(dest_dir)


def stage_educacion(edu: Path) -> None:
    edu.mkdir(parents=True, exist_ok=True)

    # Profesor hub (offline zip or downloads/Profesor.html)
    prof_zip = DL / "profesor-offline.zip"
    if prof_zip.exists():
        with zipfile.ZipFile(prof_zip) as zf:
            data = None
            for name in zf.namelist():
                if name.lower().endswith("profesor.html"):
                    data = zf.read(name)
                    break
            if data is None:
                raise SystemExit("Profesor.html missing inside profesor-offline.zip")
            (edu / "Profesor.html").write_bytes(data)
    else:
        src = DL / "Profesor.html"
        if not src.exists():
            src = ROOT / "profesor.html"
        shutil.copy2(src, edu / "Profesor.html")

    # 10 ESO flat packs
    for p in SCHOOL_PACKS:
        zname = p.get("zip")
        if not zname:
            continue
        zpath = DL / zname
        if not zpath.exists():
            raise SystemExit(f"missing ESO zip: {zpath}")
        dest = edu / p["dest"]
        print(f"  unpack {zname} → educacion/{p['dest']}/")
        unzip_flat_to(zpath, dest)
        # ensure index.html exists
        if not (dest / "index.html").exists():
            abre = dest / "ABRE-AQUI.html"
            if abre.exists():
                shutil.copy2(abre, dest / "index.html")
            else:
                raise SystemExit(f"no index.html in {dest}")

    # Linux essentials tree
    linux_src = ROOT / "profesor" / "linux-essentials"
    if linux_src.is_dir():
        linux_dst = edu / "linux-essentials"
        if linux_dst.exists():
            shutil.rmtree(linux_dst)
        shutil.copytree(
            linux_src,
            linux_dst,
            ignore=shutil.ignore_patterns("*.pdf", ".git", "__pycache__"),
        )
        print("  copied linux-essentials/")
    else:
        print("  WARN: linux-essentials missing — skip")


def main() -> None:
    if not SHELL_SRC.exists():
        raise SystemExit(f"missing shell {SHELL_SRC}")

    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    edu = STAGING / "educacion"

    print("== Staging educación ==")
    stage_educacion(edu)

    print("== Patch shell + embed modules ==")
    shell = SHELL_SRC.read_text(encoding="utf-8")
    if "/*__EMBEDDED_MODULES__*/" not in shell:
        raise SystemExit("shell missing EMBEDDED placeholder")
    patched = patch_shell(shell)
    embedded = build_embedded()
    need = [
        "hogar", "salud", "qr", "electro", "brico", "fontaneria", "jardin",
        "conservacion", "economia", "clima", "moda", "legal", "mascotas",
        "campo", "supervive", "caja", "gym", "guitarra", "piano", "armonica",
        "saxofon", "bajo", "canto-solfeo", "historia-musica", "grabadora",
        "calc", "medica", "medita", "auxilios", "escritura", "dibujo", "info",
        "guias", "mapas", "biblio", "teatro", "tanteo", "higiene", "arte",
        "protocolo", "ideas", "tabaco", "comunicacion", "gas",
        "alto-rendimiento", "cocina-maestro", "musica", "bateria", "clasica",
        "dj", "electronica", "grupo", "teoria-musical", "cuidado-instrumentos",
        "reproductor",
    ]
    for k in need:
        if k not in embedded:
            raise SystemExit(f"missing embed {k}")
    final = inject_embedded(patched, embedded)

    # Spot-check: school packs must not be external:true tip-to-web
    for sid in SCHOOL_IDS:
        m = re.search(r"\{ id: '" + re.escape(sid) + r"'[^}]+\}", final)
        if not m:
            raise SystemExit(f"built HTML missing catalog {sid}")
        chunk = m.group(0)
        if "external: true" in chunk:
            raise SystemExit(f"{sid} still external:true → {chunk}")
        if "packLocal: true" not in chunk:
            raise SystemExit(f"{sid} missing packLocal → {chunk}")

    (STAGING / "estanteria.html").write_text(final, encoding="utf-8")
    (STAGING / "ABRE-AQUI.html").write_text(thin_abre_aqui(), encoding="utf-8")

    # Splash vídeo + sonido (misma ruta relativa que la Estantería offline)
    splash_src = ROOT / "brand" / "splash"
    splash_dst = STAGING / "brand" / "splash"
    splash_dst.mkdir(parents=True, exist_ok=True)
    for splash_name in ("entrada.mp4", "entrada-sonido.m4a"):
        src = splash_src / splash_name
        if src.is_file():
            shutil.copy2(src, splash_dst / splash_name)
        else:
            print(f"  WARN: missing {src}")
    voz_src = splash_src / "voz"
    if voz_src.is_dir():
        voz_dst = splash_dst / "voz"
        voz_dst.mkdir(parents=True, exist_ok=True)
        for clip in sorted(voz_src.glob("*")):
            if clip.is_file():
                shutil.copy2(clip, voz_dst / clip.name)

    # Count files before LEEME
    files = [p for p in STAGING.rglob("*") if p.is_file()]
    # Write LEEME with placeholder size; rewrite after zip
    leeme = write_leeme(0, len(files) + 1)
    (STAGING / "LEEME.txt").write_text(leeme, encoding="utf-8")

    print("== Zip ==")
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(STAGING.rglob("*")):
            if path.is_file():
                arc = path.relative_to(STAGING).as_posix()
                zf.write(path, arcname=arc)

    shutil.copy2(OUT, SNAPSHOT)
    size = OUT.stat().st_size
    with zipfile.ZipFile(OUT) as zf:
        names = zf.namelist()
    leeme = write_leeme(size, len(names))
    (STAGING / "LEEME.txt").write_text(leeme, encoding="utf-8")
    (DL / "LEEME-pack-completo.txt").write_text(leeme, encoding="utf-8")
    # Update LEEME inside both zips
    for target in (OUT, SNAPSHOT):
        with zipfile.ZipFile(target, "a") as zf:
            # ZipFile append may leave old LEEME; rewrite whole zip cleanly
            pass
    # Clean rewrite LEEME entry
    for target in (OUT, SNAPSHOT):
        tmp = target.with_suffix(".tmp.zip")
        with zipfile.ZipFile(target, "r") as zin, zipfile.ZipFile(
            tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
        ) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "LEEME.txt":
                    data = leeme.encode("utf-8")
                zout.writestr(item, data)
        tmp.replace(target)

    print(f"Wrote {OUT} ({size} bytes)")
    print(f"Snapshot {SNAPSHOT}")
    print(f"Files: {len(names)}")
    # required presence checks
    must = [
        "estanteria.html",
        "ABRE-AQUI.html",
        "educacion/Profesor.html",
        "educacion/1eso-matematicas/index.html",
        "educacion/1eso-lengua-castellana/index.html",
        "educacion/1eso-ingles/index.html",
    ]
    for m in must:
        if m not in names:
            raise SystemExit(f"ZIP missing required entry: {m}")
    eso = [n for n in names if n.startswith("educacion/1eso-") and n.endswith("/index.html")]
    print(f"ESO index.html count: {len(eso)}")
    for e in sorted(eso):
        print(f"  {e}")
    print("OK")


if __name__ == "__main__":
    main()
