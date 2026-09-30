#!/usr/bin/env python3
"""Build Pack Casa — installable ZIP for thin APK shell (modules/pack-casa/).

Output:
  downloads/pack-casa-offline.zip
  downloads/pack-casa-offline-v20261001a.zip
  downloads/LEEME-pack-casa.txt

NO estanteria.html. NO tabaco/caja/privado/radio/cuba/ESO.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "downloads"
MODULOS = ROOT / "modulos"
BUILD = DL / "_build-pack-casa"
OUT = DL / "pack-casa-offline.zip"
VERSION = "20261001"
SNAPSHOT = DL / f"pack-casa-offline-v{VERSION}a.zip"
MODULE_ID = "pack-casa"
NOMBRE = "Pack Casa"
ENTRADA = "index.html"

# (folder_or_file id, título, blurb, source kind)
# kind: "html" → modulos/<id>.html as modulos/<id>.html
#       "musica" → unpack musica-offline.zip into modulos/musica/
MODULES = [
    ("hogar", "Hogar", "Casa, listas y mantenimiento", "html"),
    ("cocina-maestro", "Cocina maestro", "Recetas, láminas, voz y reloj", "html"),
    ("moda", "Moda", "Estilo y armario", "html"),
    ("teatro-marionetas", "Teatro de marionetas", "Títeres y escena", "html"),
    ("musica", "Música", "Hub + instrumentos offline", "musica"),
    ("jardin", "Jardín", "Plantas y huerto", "html"),
    ("conservacion", "Conservación", "Guardar y aprovechas comida", "html"),
    ("economia", "Economía", "Presupuesto y casa", "html"),
    ("clima", "Clima", "Tiempo y estación (offline)", "html"),
    ("mascotas", "Mascotas", "Cuidado básico", "html"),
    ("bricolaje", "Bricolaje", "Reparaciones ligeras", "html"),
    ("electricidad", "Electricidad", "Seguridad y casa", "html"),
    ("electronica", "Electrónica", "Taller doméstico", "html"),
    ("fontaneria", "Fontanería", "Agua y desagües", "html"),
    ("gas", "Gas", "Avisos y seguridad", "html"),
    ("higiene", "Higiene", "Limpieza y hábitos", "html"),
    ("salud", "Salud", "Consultas básicas", "html"),
    ("gimnasio", "Gimnasio", "Ejercicio en casa", "html"),
    ("meditacion", "Meditación", "Calma y respiración", "html"),
    ("medicacion", "Medicación", "Recordatorios offline", "html"),
    ("primeros-auxilios", "Primeros auxilios", "Qué hacer mientras llega ayuda", "html"),
    ("supervivencia", "Supervivencia", "Apagones y emergencias", "html"),
    ("legal-casa", "Legal casa", "Papeles y vivienda", "html"),
    ("protocolo", "Protocolo", "Formas y visitas", "html"),
    ("ideas", "Ideas", "Notas y proyectos", "html"),
]

FORBIDDEN_BASENAMES = {
    "estanteria.html",
    "tabaco.html",
    "tabaco-pipa.html",
    "caja-fuerte.html",
    "caja.html",
    "radio.html",
    "puros.html",
}
FORBIDDEN_SEGMENTS = {
    "tabaco",
    "tabaco-pipa",
    "prostata",
    "próstata",
    "caja-fuerte",
    "caja_fuerte",
    "intimidad",
    "privado-jorge",
    "pack-1eso",
    "1eso-matematicas",
}


def hub_html() -> str:
    cards = []
    for mid, title, blurb, kind in MODULES:
        if kind == "musica":
            href = "modulos/musica/musica.html"
        else:
            href = f"modulos/{mid}.html"
        cards.append(
            f'    <a class="card" href="{href}">'
            f"<strong>{title}</strong>"
            f"<span>{blurb}</span></a>"
        )
    cards_html = "\n".join(cards)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#0E0E0C">
  <title>Pack Casa — Les vencimos</title>
  <style>
    :root {{
      --bg: #0E0E0C; --fg: #E6E1D6; --muted: #9A9388;
      --gold: #C4A15A; --card: #1A1916; --line: #2A2824;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{
      margin: 0; min-height: 100%;
      background: var(--bg); color: var(--fg);
      font: 1rem/1.45 system-ui, -apple-system, "Segoe UI", sans-serif;
    }}
    header {{
      padding: 1.25rem 1.25rem 0.75rem;
      border-bottom: 1px solid var(--line);
    }}
    header h1 {{ margin: 0; font-size: 1.35rem; letter-spacing: 0.02em; }}
    header h1 span {{ color: var(--gold); }}
    header p {{ margin: 0.4rem 0 0; color: var(--muted); font-size: 0.92rem; }}
    main {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(15.5rem, 1fr));
      gap: 0.75rem;
      padding: 1rem 1.25rem 2rem;
      max-width: 56rem;
    }}
    .card {{
      display: flex; flex-direction: column; gap: 0.35rem;
      padding: 1rem 1.05rem;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 12px;
      color: inherit; text-decoration: none;
      transition: border-color 0.15s, transform 0.15s;
    }}
    .card:hover, .card:focus-visible {{
      border-color: var(--gold); outline: none;
      transform: translateY(-1px);
    }}
    .card strong {{ font-size: 1.02rem; }}
    .card span {{ color: var(--muted); font-size: 0.86rem; }}
    footer {{
      padding: 0 1.25rem 1.5rem;
      color: var(--muted); font-size: 0.8rem;
      max-width: 56rem;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Pack <span>Casa</span></h1>
    <p>Hogar, cocina, moda, música, teatro y mantenimiento · offline</p>
  </header>
  <main>
{cards_html}
  </main>
  <footer>
    Les vencimos · {MODULE_ID} · v{VERSION} · modules/{MODULE_ID}/
  </footer>
</body>
</html>
"""


def abre_aqui_html() -> str:
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="0; url=index.html">
  <title>Pack Casa — Abrir</title>
  <style>
    html,body{margin:0;min-height:100%;background:#0E0E0C;color:#E6E1D6;
      font:1rem/1.45 system-ui,sans-serif;display:flex;align-items:center;justify-content:center}
    a{color:#C4A15A;font-weight:700}
  </style>
  <script>location.replace("index.html");</script>
</head>
<body>
  <p>Abriendo Pack Casa… <a href="index.html">Entrar</a></p>
</body>
</html>
"""


def leeme_txt(n_files: int, zip_bytes: int, sha: str) -> str:
    mb = zip_bytes / (1024 * 1024)
    lines = []
    for mid, title, _blurb, kind in MODULES:
        if kind == "musica":
            lines.append(f"  · {title} → modulos/musica/")
        else:
            lines.append(f"  · {title} → modulos/{mid}.html")
    listing = "\n".join(lines)
    return f"""═══════════════════════════════════════
  PACK CASA — Les vencimos
  Id: {MODULE_ID} · versión {VERSION}
═══════════════════════════════════════

Pack de contenido para el cascarón APK (shell fino).
NO incluye estanteria.html, radio, tabaco, caja fuerte ni ESO.

─── Contenido ───

  module.json          → contrato del módulo
  index.html           → hub (enlaces relativos)
  ABRE-AQUI.html       → atajo al hub
  modulos/             → un HTML (o carpeta) por módulo
{listing}
  LEEME.txt

Archivos en el ZIP: {n_files}
Tamaño comprimido: ~{mb:.1f} MB
sha256 (catálogo / LEEME-pack-casa.txt): {sha}

─── App APK (cascarón) ───

1) Catálogo → Descargar e instalar «Pack Casa»
   URL: https://lesvencimos.com/downloads/pack-casa-offline.zip
2) Descomprime en modules/{MODULE_ID}/
3) Abre entrada: index.html
4) Sin red tras instalar. publico=casa, red=false

Hogar enlaza a Cocina maestro como hermano en modulos/.
Música trae el hub + salas de instrumentos en modulos/musica/.

lesvencimos.com
"""


def assert_clean(path: Path) -> None:
    parts = Path(str(path).replace("\\", "/")).parts
    low_parts = [p.lower() for p in parts]
    base = low_parts[-1] if low_parts else ""
    if base in FORBIDDEN_BASENAMES:
        raise SystemExit(f"contenido prohibido en pack: {path}")
    for seg in low_parts:
        name = seg[:-1] if seg.endswith("/") else seg
        if name in FORBIDDEN_SEGMENTS:
            raise SystemExit(f"contenido prohibido en pack: {path}")


def patch_musica_brand(html: str) -> str:
    """musica/* sits two levels under pack root → brand must go ../../index.html."""
    html = html.replace('href="../index.html"', 'href="../../index.html"')
    return html


def stage() -> Path:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)
    dest_mod = BUILD / "modulos"
    dest_mod.mkdir()

    for mid, _title, _blurb, kind in MODULES:
        if kind == "html":
            src = MODULOS / f"{mid}.html"
            if not src.is_file():
                # try from offline zip
                zpath = DL / f"{mid}-offline.zip"
                if not zpath.is_file():
                    raise SystemExit(f"falta módulo: {mid}")
                with zipfile.ZipFile(zpath) as z:
                    # find the main html
                    names = [n for n in z.namelist() if n.lower().endswith(".html")]
                    pick = next((n for n in names if Path(n).name == f"{mid}.html"), None)
                    if not pick:
                        pick = names[0] if names else None
                    if not pick:
                        raise SystemExit(f"sin HTML en {zpath.name}")
                    data = z.read(pick)
                (dest_mod / f"{mid}.html").write_bytes(data)
            else:
                shutil.copy2(src, dest_mod / f"{mid}.html")
            assert_clean(dest_mod / f"{mid}.html")
        elif kind == "musica":
            zpath = DL / "musica-offline.zip"
            if not zpath.is_file():
                raise SystemExit("falta musica-offline.zip")
            tmp = BUILD / "_tmp_musica"
            if tmp.exists():
                shutil.rmtree(tmp)
            tmp.mkdir()
            with zipfile.ZipFile(zpath) as z:
                z.extractall(tmp)
            # Prefer tmp/musica/ folder
            inner = tmp / "musica"
            if not inner.is_dir():
                # maybe files at root
                inner = tmp
            out_m = dest_mod / "musica"
            if out_m.exists():
                shutil.rmtree(out_m)
            out_m.mkdir()
            for path in inner.rglob("*"):
                if not path.is_file():
                    continue
                if path.name.startswith("."):
                    continue
                rel = path.relative_to(inner)
                target = out_m / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if path.suffix.lower() in {".html", ".htm"}:
                    text = path.read_text(encoding="utf-8", errors="replace")
                    target.write_text(patch_musica_brand(text), encoding="utf-8")
                else:
                    shutil.copy2(path, target)
                assert_clean(target)
            if not (out_m / "musica.html").is_file():
                raise SystemExit("musica hub missing after unpack")
            shutil.rmtree(tmp)
        else:
            raise SystemExit(f"kind desconocido: {kind}")

    # Cross-link check: hogar → cocina-maestro sibling
    hogar = (dest_mod / "hogar.html").read_text(encoding="utf-8", errors="replace")
    if "cocina-maestro.html" not in hogar:
        print("WARN: hogar no referencia cocina-maestro.html")

    (BUILD / "index.html").write_text(hub_html(), encoding="utf-8")
    (BUILD / "ABRE-AQUI.html").write_text(abre_aqui_html(), encoding="utf-8")
    (BUILD / "LEEME.txt").write_text("Pack Casa\n", encoding="utf-8")

    meta = {
        "id": MODULE_ID,
        "nombre": NOMBRE,
        "version": VERSION,
        "publico": "casa",
        "red": False,
        "entrada": ENTRADA,
        "permisos": [],
        "sha256": None,
        "bytes": None,
    }
    (BUILD / "module.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return BUILD


def zip_dir(src: Path, dest: Path) -> tuple[int, int]:
    if dest.exists():
        dest.unlink()
    n = 0
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in sorted(src.rglob("*")):
            if not path.is_file():
                continue
            if path.name.startswith("."):
                continue
            rel = path.relative_to(src).as_posix()
            assert_clean(Path(rel))
            if "estanteria.html" in rel.lower():
                raise SystemExit("estanteria.html no debe entrar")
            z.write(path, rel)
            n += 1
    return n, dest.stat().st_size


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def finalize_meta(zip_path: Path, n_files: int) -> dict:
    """module.json keeps sha256/bytes null (hash is of whole ZIP).
    LEEME inside ZIP omits digest; catalog + LEEME-pack-casa.txt get real sha256/bytes.
    """
    meta_path = BUILD / "module.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["sha256"] = None
    meta["bytes"] = None
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Stable LEEME without self-hash
    (BUILD / "LEEME.txt").write_text(
        leeme_txt(n_files, zip_path.stat().st_size, "(ver catálogo)"),
        encoding="utf-8",
    )
    n2, size2 = zip_dir(BUILD, zip_path)
    # Fix file count label once
    (BUILD / "LEEME.txt").write_text(
        leeme_txt(n2, size2, "(ver catálogo)"),
        encoding="utf-8",
    )
    n3, size3 = zip_dir(BUILD, zip_path)
    if n3 != n2:
        n2, size2 = n3, size3
        (BUILD / "LEEME.txt").write_text(
            leeme_txt(n2, size2, "(ver catálogo)"),
            encoding="utf-8",
        )
        n2, size2 = zip_dir(BUILD, zip_path)
    else:
        n2, size2 = n3, size3
    sha = sha256_file(zip_path)
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return {"files": n2, "bytes": size2, "sha256": sha, "meta": meta}


def update_catalogos(zip_bytes: int, sha: str) -> None:
    entry = {
        "id": MODULE_ID,
        "nombre": NOMBRE,
        "version": VERSION,
        "publico": "casa",
        "red": False,
        "bytes": zip_bytes,
        "sha256": sha,
        "url": "https://lesvencimos.com/downloads/pack-casa-offline.zip",
        "entrada": ENTRADA,
        "permisos": [],
        "nota": "Agrupa hogar, cocina, moda, teatro, música (+instrumentos), jardín, mantenimiento y salud básica. Sin radio/tabaco/caja/ESO.",
    }
    for cat_path in (ROOT / "catalogo.json", ROOT / "app" / "catalogo.json"):
        data = json.loads(cat_path.read_text(encoding="utf-8"))
        data["actualizado"] = "2026-10-01"
        presets = data.setdefault("presets", {})
        casa = list(presets.get("casa") or [])
        if MODULE_ID not in casa:
            casa.insert(0, MODULE_ID)
            presets["casa"] = casa
        mods = data.setdefault("modulos", [])
        idx = next((i for i, m in enumerate(mods) if m.get("id") == MODULE_ID), None)
        if idx is not None:
            mods[idx] = entry
        else:
            # insert near hogar / after pack-1eso if present
            insert_at = next(
                (i + 1 for i, m in enumerate(mods) if m.get("id") == "pack-1eso"),
                next((i for i, m in enumerate(mods) if m.get("id") == "hogar"), len(mods)),
            )
            mods.insert(insert_at, entry)
        data["modulos"] = mods
        nota = data.get("nota") or ""
        if "pack-casa" not in nota:
            data["nota"] = (
                nota.rstrip() + " Pack pack-casa agrupa módulos de casa; los sueltos siguen."
            ).strip()
        cat_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_leeme_download(n_files: int, zip_bytes: int, sha: str) -> None:
    (DL / "LEEME-pack-casa.txt").write_text(leeme_txt(n_files, zip_bytes, sha), encoding="utf-8")


def verify(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        meta = json.loads(z.read("module.json"))
    for name in names:
        assert_clean(Path(name))
    need = ["module.json", "index.html", "ABRE-AQUI.html", "LEEME.txt", "modulos/hogar.html",
            "modulos/cocina-maestro.html", "modulos/moda.html", "modulos/teatro-marionetas.html",
            "modulos/musica/musica.html"]
    for n in need:
        if n not in names:
            raise SystemExit(f"VERIFY FAIL: falta {n}")
    for req in ("id", "nombre", "version", "entrada"):
        if req not in meta:
            raise SystemExit(f"VERIFY FAIL: module.json sin {req}")
    if meta["id"] != MODULE_ID or meta.get("publico") != "casa" or meta.get("red") is not False:
        raise SystemExit("VERIFY FAIL: id/publico/red")
    if any("estanteria" in n.lower() for n in names):
        raise SystemExit("VERIFY FAIL: estanteria")
    sha = sha256_file(zip_path)
    # module.json keeps sha256 null (hash is of whole ZIP); catalog holds the real digest
    if meta.get("sha256") not in (None, sha):
        raise SystemExit(f"VERIFY FAIL: sha256 mismatch meta={meta['sha256']} file={sha}")
    print(f"OK verify: {len(names)} entries, id={meta['id']}, sha256={sha[:16]}…")


def main() -> None:
    print("Staging pack-casa…")
    stage()
    print("Zipping…")
    n, _size = zip_dir(BUILD, OUT)
    info = finalize_meta(OUT, n)
    n, size, sha = info["files"], info["bytes"], info["sha256"]
    shutil.copy2(OUT, SNAPSHOT)
    write_leeme_download(n, size, sha)
    update_catalogos(size, sha)
    verify(OUT)
    print(f"OUT: {OUT}")
    print(f"SNAPSHOT: {SNAPSHOT}")
    print(f"files={n} bytes={size} ({size/1024/1024:.2f} MiB)")
    print(f"sha256={sha}")
    print(json.dumps(info["meta"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
