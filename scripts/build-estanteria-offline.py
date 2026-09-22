#!/usr/bin/env python3
"""Rebuild downloads/estanteria-offline.zip (offline desktop, no cultural gate)."""
from __future__ import annotations
import re, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "offline-estanteria"
OUT = ROOT / "downloads" / "estanteria-offline.zip"
STAGING = ROOT / "downloads" / ".estanteria-staging"


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
    (STAGING / "estanteria.html").write_text(est, encoding="utf-8")
    (STAGING / "ABRE-AQUI.html").write_text(est, encoding="utf-8")
    shutil.copy2(SRC / "LEEME.txt", STAGING / "LEEME.txt")
    shutil.copy2(ROOT / "downloads" / "Profesor.html", STAGING / "profesor.html")
    # Prefer root profesor.html if downloads one missing size; already copied
    if (ROOT / "profesor.html").exists():
        shutil.copy2(ROOT / "profesor.html", STAGING / "profesor.html")

    alarma = ungate_alarma((ROOT / "alarma-cuba.html").read_text(encoding="utf-8"))
    (STAGING / "alarma-cuba.html").write_text(alarma, encoding="utf-8")

    mods = STAGING / "modulos"
    mods.mkdir()
    for p in sorted((ROOT / "modulos").glob("*.html")):
        shutil.copy2(p, mods / p.name)

    if OUT.exists():
        OUT.unlink()
    order = [
        "LEEME.txt",
        "ABRE-AQUI.html",
        "estanteria.html",
        "profesor.html",
        "alarma-cuba.html",
    ]
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name in order:
            z.write(STAGING / name, arcname=name)
        for p in sorted(mods.glob("*.html")):
            z.write(p, arcname=f"modulos/{p.name}")

    shutil.copy2(SRC / "LEEME.txt", ROOT / "downloads" / "LEEME-estanteria.txt")
    shutil.rmtree(STAGING)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
