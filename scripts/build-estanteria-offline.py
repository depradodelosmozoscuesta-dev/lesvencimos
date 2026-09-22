#!/usr/bin/env python3
"""Rebuild downloads/estanteria-offline.zip (flat layout for Android file://)."""
from __future__ import annotations
import re, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "offline-estanteria"
OUT = ROOT / "downloads" / "estanteria-offline.zip"
STAGING = ROOT / "downloads" / ".estanteria-staging"

# Flat short names (same folder as estanteria.html). Avoids nested modulos/
# and reduces MediaStore truncation pain if someone opens via content://.
MODULE_MAP = {
    "calculadora.html": "calc.html",
    "gimnasio.html": "gym.html",
    "informatica.html": "info.html",
    "medicacion.html": "medica.html",
    "primeros-auxilios.html": "auxilios.html",
    "tinta-escritura.html": "escritura.html",
    "tinta-estudio.html": "dibujo.html",
}


def ungate_alarma(text: str) -> str:
    text = text.replace('class="lv-locked"', "", 1)
    text = re.sub(
        r"if\(sessionStorage\.getItem\('lv-gate-v1'\)==='ok'\)document\.documentElement\.classList\.remove\('lv-locked'\);",
        "document.documentElement.classList.remove('lv-locked');",
        text,
        count=1,
    )
    if "lv-offline-ungate" not in text:
        text = text.replace(
            "</head>",
            """
  <style id="lv-offline-ungate">
    html.lv-locked #lv-protected { display: block !important; }
    #lv-gate { display: none !important; }
  </style>
</head>""",
            1,
        )
    text = re.sub(r'\s*<script src="/brand/gate\.js"></script>\s*', "\n", text)
    return text


def main() -> None:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)

    est = (SRC / "estanteria.html").read_text(encoding="utf-8")
    for pat in ("lv-locked", "lv-gate", "gate.js", "/brand/"):
        if pat in est:
            raise SystemExit(f"offline estanteria.html still contains {pat!r}")
    if "modulos/" in est and ("href: 'modulos/" in est or 'href: "modulos/' in est or "href: '/modulos/" in est):
        raise SystemExit("offline estanteria.html still has nested modulos/ hrefs")
    for need in ("gym.html", "profe.html", "calc.html", "file://"):
        if need not in est:
            raise SystemExit(f"offline estanteria.html missing expected {need!r}")

    (STAGING / "estanteria.html").write_text(est, encoding="utf-8")
    (STAGING / "ABRE-AQUI.html").write_text(est, encoding="utf-8")
    shutil.copy2(SRC / "LEEME.txt", STAGING / "LEEME.txt")

    if (ROOT / "profesor.html").exists():
        shutil.copy2(ROOT / "profesor.html", STAGING / "profe.html")
    elif (ROOT / "downloads" / "Profesor.html").exists():
        shutil.copy2(ROOT / "downloads" / "Profesor.html", STAGING / "profe.html")
    else:
        raise SystemExit("profesor.html not found")

    alarma = ungate_alarma((ROOT / "alarma-cuba.html").read_text(encoding="utf-8"))
    (STAGING / "alarma.html").write_text(alarma, encoding="utf-8")

    mods_src = ROOT / "modulos"
    for src_name, dest_name in sorted(MODULE_MAP.items()):
        src = mods_src / src_name
        if not src.exists():
            raise SystemExit(f"missing module {src}")
        shutil.copy2(src, STAGING / dest_name)

    if OUT.exists():
        OUT.unlink()

    order = [
        "LEEME.txt",
        "ABRE-AQUI.html",
        "estanteria.html",
        "profe.html",
        "alarma.html",
        "gym.html",
        "calc.html",
        "info.html",
        "auxilios.html",
        "escritura.html",
        "dibujo.html",
        "medica.html",
    ]
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name in order:
            z.write(STAGING / name, arcname=name)

    shutil.copy2(SRC / "LEEME.txt", ROOT / "downloads" / "LEEME-estanteria.txt")
    shutil.rmtree(STAGING)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    with zipfile.ZipFile(OUT) as z:
        print("Contents:", ", ".join(z.namelist()))


if __name__ == "__main__":
    main()
