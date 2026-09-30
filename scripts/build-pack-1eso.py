#!/usr/bin/env python3
"""Build Pack 1º ESO — installable ZIP for thin APK shell (modules/pack-1eso/).

Output:
  downloads/pack-1eso-offline.zip
  downloads/pack-1eso-offline-v20261001a.zip
  downloads/LEEME-pack-1eso.txt

NO estanteria.html. NO tabaco/caja/privado. Solo 10 asignaturas + Profesor.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "downloads"
STAGING_SRC = ROOT / "offline-pack-completo" / "educacion"
BUILD = ROOT / "downloads" / "_build-pack-1eso"
OUT = DL / "pack-1eso-offline.zip"
VERSION = "20261001"
SNAPSHOT = DL / f"pack-1eso-offline-v{VERSION}a.zip"
MODULE_ID = "pack-1eso"
NOMBRE = "Pack 1º ESO"
ENTRADA = "index.html"

SUBJECTS = [
    ("1eso-matematicas", "Matemáticas", "Números, cálculo y problemas"),
    ("1eso-lengua-castellana", "Lengua castellana", "Lectura, escritura y comunicación"),
    ("1eso-biologia-geologia", "Biología y Geología", "Vida, Tierra y laboratorio"),
    ("1eso-geografia-historia", "Geografía e Historia", "Mapas, sociedades y tiempo"),
    ("1eso-ingles", "Inglés", "English · vocabulary & skills"),
    ("1eso-frances", "Francés", "Français · bases et pratique"),
    ("1eso-plastica-visual", "Plástica y visual", "Dibujo, color y composición"),
    ("1eso-educacion-fisica", "Educación Física", "Cuerpo, deporte y salud"),
    ("1eso-religion", "Religión", "Cultura religiosa y valores"),
    ("1eso-alternativa-religion", "Alt. Religión", "Valores, ética y ciudadanía"),
]

# Exact basenames or path-segment tokens (not substrings like "redondeo")
FORBIDDEN_BASENAMES = {
    "estanteria.html",
    "tabaco.html",
    "tabaco-pipa.html",
    "caja-fuerte.html",
    "caja.html",
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
}


def hub_html() -> str:
    cards = []
    cards.append(
        '    <a class="card maestro" href="educacion/Profesor.html">'
        "<strong>Profesor</strong>"
        "<span>Maestro · hub de lecciones</span></a>"
    )
    for folder, title, blurb in SUBJECTS:
        cards.append(
            f'    <a class="card" href="educacion/{folder}/index.html">'
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
  <title>Pack 1º ESO — Les vencimos</title>
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
    header h1 {{
      margin: 0; font-size: 1.35rem; letter-spacing: 0.02em;
    }}
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
    .card.maestro {{ border-color: #5a4a28; background: #1f1a12; }}
    .card.maestro strong {{ color: var(--gold); }}
    footer {{
      padding: 0 1.25rem 1.5rem;
      color: var(--muted); font-size: 0.8rem;
      max-width: 56rem;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Pack <span>1º ESO</span></h1>
    <p>Diez asignaturas + Profesor · offline · sin red</p>
  </header>
  <main>
{cards_html}
  </main>
  <footer>
    Les vencimos · {MODULE_ID} · v{VERSION} · instálalo en la app (cascarón) → modules/{MODULE_ID}/
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
  <title>Pack 1º ESO — Abrir</title>
  <style>
    html,body{margin:0;min-height:100%;background:#0E0E0C;color:#E6E1D6;
      font:1rem/1.45 system-ui,sans-serif;display:flex;align-items:center;justify-content:center}
    a{color:#C4A15A;font-weight:700}
  </style>
  <script>location.replace("index.html");</script>
</head>
<body>
  <p>Abriendo Pack 1º ESO… <a href="index.html">Entrar</a></p>
</body>
</html>
"""


def leeme_txt(n_files: int, zip_bytes: int) -> str:
    mb = zip_bytes / (1024 * 1024)
    subjects = "\n".join(f"  · {title} → educacion/{folder}/" for folder, title, _ in SUBJECTS)
    return f"""═══════════════════════════════════════
  PACK 1º ESO — Les vencimos
  Id: {MODULE_ID} · versión {VERSION}
═══════════════════════════════════════

Pack de contenido para el cascarón APK (shell fino).
NO incluye estanteria.html ni módulos de adulto/privado.

─── Contenido ───

  module.json          → contrato del módulo
  index.html           → hub (10 asignaturas + Profesor)
  ABRE-AQUI.html       → atajo al hub
  educacion/Profesor.html
{subjects}
  LEEME.txt

Archivos en el ZIP: {n_files}
Tamaño comprimido: ~{mb:.1f} MB

─── App APK (cascarón) ───

1) Desde el catálogo: Descargar e instalar «Pack 1º ESO»
   URL: https://lesvencimos.com/downloads/pack-1eso-offline.zip
2) El cascarón descomprime en modules/{MODULE_ID}/
3) Abre entrada: index.html (o ABRE-AQUI.html)
4) Sin red tras instalar. publico=estudios, red=false

También puedes instalar el ZIP a mano (Instalar ZIP / Añadir)
manteniendo el id {MODULE_ID}.

Los módulos sueltos 1eso-* siguen en el catálogo;
este pack los agrupa + maestro en un solo ZIP.

lesvencimos.com
"""


def assert_clean(path: Path) -> None:
    parts = Path(str(path).replace("\\", "/")).parts
    low_parts = [p.lower() for p in parts]
    base = low_parts[-1] if low_parts else ""
    if base in FORBIDDEN_BASENAMES:
        raise SystemExit(f"contenido prohibido en pack: {path}")
    for seg in low_parts:
        # strip trailing slash-style empties already handled by parts
        name = seg[:-1] if seg.endswith("/") else seg
        if name in FORBIDDEN_SEGMENTS:
            raise SystemExit(f"contenido prohibido en pack: {path}")


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, symlinks=False)
    for p in dst.rglob("*"):
        if p.is_file():
            assert_clean(p)


def stage() -> Path:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    edu = BUILD / "educacion"
    edu.mkdir()

    # Subjects from offline-pack-completo (already flattened, no -offline suffix)
    for folder, _title, _blurb in SUBJECTS:
        src = STAGING_SRC / folder
        if not src.is_dir():
            # Fallback: unpack downloads ZIP and flatten *-offline
            zpath = DL / f"{folder}-offline.zip"
            if not zpath.is_file():
                raise SystemExit(f"falta asignatura: {folder}")
            tmp = BUILD / f"_tmp_{folder}"
            tmp.mkdir()
            with zipfile.ZipFile(zpath) as z:
                z.extractall(tmp)
            # find single wrapper *-offline
            kids = [c for c in tmp.iterdir() if not c.name.startswith(".")]
            if len(kids) == 1 and kids[0].is_dir():
                inner = kids[0]
            else:
                inner = tmp
            copy_tree(inner, edu / folder)
            shutil.rmtree(tmp)
        else:
            copy_tree(src, edu / folder)
        if not (edu / folder / "index.html").is_file():
            raise SystemExit(f"sin index.html: {folder}")

    # Profesor
    prof_src = STAGING_SRC / "Profesor.html"
    if not prof_src.is_file():
        prof_src = DL / "Profesor.html"
    if not prof_src.is_file():
        raise SystemExit("falta Profesor.html")
    shutil.copy2(prof_src, edu / "Profesor.html")

    # Hub + abre-aqui + module.json (bytes/sha filled after zip)
    (BUILD / "index.html").write_text(hub_html(), encoding="utf-8")
    (BUILD / "ABRE-AQUI.html").write_text(abre_aqui_html(), encoding="utf-8")
    (BUILD / "LEEME.txt").write_text(
        leeme_txt(0, 0).replace("Archivos en el ZIP: 0\nTamaño comprimido: ~0.0 MB\n", ""),
        encoding="utf-8",
    )

    meta = {
        "id": MODULE_ID,
        "nombre": NOMBRE,
        "version": VERSION,
        "publico": "estudios",
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
    """ZIP with module contents at root (module.json at ZIP root)."""
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
            if rel == "estanteria.html" or rel.endswith("/estanteria.html"):
                raise SystemExit("estanteria.html no debe entrar en pack-1eso")
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
    """Rewrite module.json bytes + LEEME and re-zip until size stabilizes."""
    meta_path = BUILD / "module.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["sha256"] = None
    n2, size2 = n_files, zip_path.stat().st_size
    for _ in range(4):
        meta["bytes"] = size2
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (BUILD / "LEEME.txt").write_text(leeme_txt(n2, size2), encoding="utf-8")
        n3, size3 = zip_dir(BUILD, zip_path)
        if size3 == size2 and n3 == n2:
            break
        n2, size2 = n3, size3
    meta["bytes"] = size2
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"files": n2, "bytes": size2, "meta": meta}


def update_catalogos(zip_bytes: int) -> None:
    entry = {
        "id": MODULE_ID,
        "nombre": NOMBRE,
        "version": VERSION,
        "publico": "estudios",
        "red": False,
        "bytes": zip_bytes,
        "sha256": None,
        "url": "https://lesvencimos.com/downloads/pack-1eso-offline.zip",
        "entrada": ENTRADA,
        "permisos": [],
        "nota": "Agrupa las diez asignaturas 1º ESO + Profesor (maestro). Los 1eso-* sueltos siguen disponibles.",
    }
    for cat_path in (ROOT / "catalogo.json", ROOT / "app" / "catalogo.json"):
        data = json.loads(cat_path.read_text(encoding="utf-8"))
        data["actualizado"] = "2026-10-01"
        # bump catalog version if numeric
        if isinstance(data.get("version"), int):
            data["version"] = max(int(data["version"]), 1)
        # Prefer pack in estudios preset (front)
        presets = data.setdefault("presets", {})
        estudios = list(presets.get("estudios") or [])
        if MODULE_ID not in estudios:
            estudios.insert(0, MODULE_ID)
            presets["estudios"] = estudios
        mods = data.setdefault("modulos", [])
        # Replace or insert after last 1eso-* / before gimnasio
        idx = next((i for i, m in enumerate(mods) if m.get("id") == MODULE_ID), None)
        if idx is not None:
            # preserve any extra keys? replace cleanly
            mods[idx] = entry
        else:
            # insert after 1eso-alternativa-religion if present
            insert_at = next(
                (i + 1 for i, m in enumerate(mods) if m.get("id") == "1eso-alternativa-religion"),
                0,
            )
            mods.insert(insert_at, entry)
        data["modulos"] = mods
        # Short note in top-level nota if missing pack mention
        nota = data.get("nota") or ""
        if "pack-1eso" not in nota:
            data["nota"] = (
                nota.rstrip()
                + " Pack pack-1eso agrupa los diez 1º ESO + maestro; los sueltos siguen."
            ).strip()
        cat_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_leeme_download(n_files: int, zip_bytes: int) -> None:
    (DL / "LEEME-pack-1eso.txt").write_text(leeme_txt(n_files, zip_bytes), encoding="utf-8")


def verify(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
    joined = "\n".join(names)
    for name in names:
        assert_clean(Path(name))
    need = ["module.json", "index.html", "ABRE-AQUI.html", "educacion/Profesor.html", "LEEME.txt"]
    for folder, _, _ in SUBJECTS:
        need.append(f"educacion/{folder}/index.html")
    for n in need:
        if n not in names:
            raise SystemExit(f"VERIFY FAIL: falta {n}")
    # module.json fields
    with zipfile.ZipFile(zip_path) as z:
        meta = json.loads(z.read("module.json"))
    for req in ("id", "nombre", "version", "entrada"):
        if req not in meta:
            raise SystemExit(f"VERIFY FAIL: module.json sin {req}")
    if meta["id"] != MODULE_ID:
        raise SystemExit(f"VERIFY FAIL: id={meta['id']}")
    if meta.get("publico") != "estudios" or meta.get("red") is not False:
        raise SystemExit("VERIFY FAIL: publico/red")
    print(f"OK verify: {len(names)} entries, id={meta['id']}, entrada={meta['entrada']}")


def main() -> None:
    print("Staging pack-1eso…")
    stage()
    print("Zipping…")
    n, size = zip_dir(BUILD, OUT)
    info = finalize_meta(OUT, n)
    n, size = info["files"], info["bytes"]
    shutil.copy2(OUT, SNAPSHOT)
    write_leeme_download(n, size)
    update_catalogos(size)
    verify(OUT)
    print(f"OUT: {OUT}")
    print(f"SNAPSHOT: {SNAPSHOT}")
    print(f"files={n} bytes={size} ({size/1024/1024:.2f} MiB)")
    print(json.dumps(info["meta"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
