#!/usr/bin/env python3
"""Build Completo EMBED pack for monolithic App APK.

App contract (2026-10-01):
  assets/embed/completo-offline.zip
  = Estantería shell (parade k3 Completo) + full content of 7 thematic packs
  Layout: root ABRE-AQUI.html / estanteria.html + educacion/ + brand/
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

Base shell: existing downloads/pack-completo-offline.zip (or rebuild with
--rebuild-shell which runs build-pack-completo.py first).
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
VERSION = "v20261001embed"
SOFT_WARN_BYTES = 70 * 1024 * 1024

PRIMARY = DL / "completo-offline.zip"
ALIAS = DL / "pack-completo-offline.zip"
SNAPSHOT = DL / f"completo-offline-{VERSION}.zip"
# Prefer thin Completo shell snapshot (no modules/) so re-runs stay clean.
SHELL_CANDIDATES = [
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
  (parade Completo / Estantería k3 + educación)

Contiene:
  · estanteria.html     → shell Completo (56 embeds + Educación packLocal)
  · educacion/          → Profesor + 10×1º ESO limpio + Linux
  · brand/splash/       → vídeo + sonido
  · modules/<id>/       → packs thematic completos (App toggle)
{mods}
  · catalogo-embed.json → ids para UI show/hide
  · LEEME.txt

Biblioteca (~12 MB) VA DENTRO (modules/pack-biblioteca/).

EXCLUIDO: radio, vitaink, cuba, privado-jorge, UI de descarga.

Archivos en el ZIP: {n_files}
Tamaño comprimido: ~{mb:.1f} MB
{warn}
─── App APK ───

1) Embebe downloads/completo-offline.zip en assets/embed/completo-offline.zip
2) Al primer arranque: descomprime a filesDir (o sirve desde assets)
3) WebView entry: estanteria.html (o ABRE-AQUI.html)
4) Lee catalogo-embed.json para toggles de visibilidad de modules/*
5) Sin red. Sin flujo «Descargar pack».

No es el ZIP legado lesvencimos-completo.zip.
lesvencimos.com
"""


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

    modules_dir = STAGING / "modules"
    modules_dir.mkdir(parents=True, exist_ok=True)

    modules_meta: list[dict] = []
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
    ]
    name_set = set(names)
    for m in must:
        if m not in name_set:
            raise SystemExit(f"ZIP missing required entry: {m}")

    # Soft warn
    if size > SOFT_WARN_BYTES:
        print(f"SOFT WARN: ZIP {size} bytes ({size/1024/1024:.1f} MB) > 70 MB")

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
    print("OK")


if __name__ == "__main__":
    main()
