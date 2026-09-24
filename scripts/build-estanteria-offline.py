#!/usr/bin/env python3
"""Rebuild single-file Estantería offline zip + Caja fuerte zip."""
from __future__ import annotations
import json, re, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "offline-estanteria"
OUT = ROOT / "downloads" / "estanteria-offline.zip"
CAJA_OUT = ROOT / "downloads" / "caja-fuerte-offline.zip"
STAGING = ROOT / "downloads" / ".estanteria-staging"

# embed key -> source file
EMBED_SOURCES = {
    "hogar": ROOT / "modulos" / "hogar.html",
    "salud": ROOT / "modulos" / "salud.html",
    "radio": ROOT / "modulos" / "radio.html",
    "qr": ROOT / "modulos" / "qr.html",
    "electro": ROOT / "modulos" / "electricidad.html",
    "brico": ROOT / "modulos" / "bricolaje.html",
    "jardin": ROOT / "modulos" / "jardin.html",
    "supervive": ROOT / "modulos" / "supervivencia.html",
    "apagon": ROOT / "modulos" / "apagon.html",
    "caja": ROOT / "modulos" / "caja-fuerte.html",
    "calc": ROOT / "modulos" / "calculadora.html",
    "gym": ROOT / "modulos" / "gimnasio.html",
    "guitarra": ROOT / "modulos" / "guitarra.html",
    "medica": ROOT / "modulos" / "medicacion.html",
    "medita": ROOT / "modulos" / "meditacion.html",
    "auxilios": ROOT / "modulos" / "primeros-auxilios.html",
    "escritura": ROOT / "modulos" / "tinta-escritura.html",
    "dibujo": ROOT / "modulos" / "tinta-estudio.html",
    "info": ROOT / "modulos" / "informatica.html",
    "guias": ROOT / "modulos" / "guias-viaje.html",
    "mapas": ROOT / "modulos" / "mapas.html",
    "alarma": ROOT / "alarma-cuba.html",
    "biblio": ROOT / "modulos" / "biblioteca.html",
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


def build_embedded() -> dict[str, str]:
    out: dict[str, str] = {}
    for key, path in EMBED_SOURCES.items():
        if not path.exists():
            raise SystemExit(f"missing embed source {path}")
        html = path.read_text(encoding="utf-8")
        if key == "alarma":
            html = ungate_alarma(html)
        out[key] = html
    return out


def inject_embedded(shell: str, embedded: dict[str, str]) -> str:
    # Plain str.replace — do NOT use re.sub (it eats JSON backslash escapes).
    # CRITICAL: escape "<" so embedded HTML "</script>" cannot close the outer
    # <script> tag (HTML parser ignores JS string context). Without this,
    # togglePanel / click handlers never run → Módulos/Widgets panels stay dead.
    payload = json.dumps(embedded, ensure_ascii=False).replace("<", "\\u003c")
    needle = "var EMBEDDED = {/*__EMBEDDED_MODULES__*/};"
    if needle not in shell:
        raise SystemExit("EMBEDDED placeholder missing in shell")
    shell2 = shell.replace(needle, "var EMBEDDED = " + payload + ";", 1)
    if "__EMBEDDED_MODULES__" in shell2:
        raise SystemExit("placeholder still present")
    # Verify EMBEDDED region has no raw script closer before CATALOG
    try:
        emb_body = shell2.split("var EMBEDDED = ", 1)[1].split("var CATALOG", 1)[0]
    except IndexError:
        emb_body = ""
    if "</script>" in emb_body:
        raise SystemExit("EMBEDDED payload still contains raw </script>")
    return shell2


def write_leeme() -> str:
    return """═══════════════════════════════════════
  ESCRITORIO / ESTANTERÍA — Les vencimos
  Build v20260924q
  UN SOLO HTML (módulos dentro)
═══════════════════════════════════════

Este ZIP lleva esencialmente UN archivo:
  ABRE-AQUI.html  (= estanteria.html)
  estanteria.html
  LEEME.txt

Baldas deslizables por tema (Escritura, Ocio,
Casa/Hogar, Salud, Varios): una sola línea,
desliza en horizontal. Primer icono de cada balda
más grande: Teléfono, WhatsApp, Navegador, Fotos
(atajos nativos). El resto se ordena por uso.
Packs escolares en Varios (no hay balda Educación
ni Rápido). Barra Ajustes compacta arriba (no es
una balda). Iconos de color vivos.
Hora y fecha fijas arriba a la derecha; papelera
ahí (elige app · otra vez para confirmar).
Disposición: Completo / Casa / Estudio / Educación / Mínimo.
Calendario opcional como mosaico (sin cortar la
balda). Sin ficha libre ni redimensionar a mano.
Al abrir ya viene llena. Sin Radio ni Alarma Cuba.

Los módulos (Hogar, Salud, QR, Electricidad,
Bricolaje, Jardín, Resiliencia, Apagón, Calculadora,
Gimnasio, Guitarra, Caja fuerte, Medicación, Meditación,
Auxilios, Escritura, Dibujo, Informática, Guías de viaje, Mapas, Biblioteca…)
van EMBEBIDOS dentro del HTML.
Al tocar un icono se abren en la misma página
(← Escritorio para volver).

Profesor (cole) es grande: descarga aparte en
lesvencimos.com/descargas.html (o «Archivo local…»).

─── Android — pasos ───

1) Descarga el ZIP.
2) Abre Mis archivos / Archivos (NO la lista
   Descargas del navegador).
3) Descomprime y entra en la carpeta.
4) Toca ABRE-AQUI.html → Chrome / Samsung Internet.
5) Debe verse «Modo offline · file://».
6) Lanzadera llena al abrir. Widgets para añadir;
   Módulos / Restaurar todo si quitaste algo.

Con content:// los embebidos también abren, pero
file:// desde Archivos es lo más fiable.

Sin pestillo cultural. Sin internet.
lesvencimos.com
"""


def build_caja_zip() -> None:
    staging = ROOT / "downloads" / ".caja-staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    src = ROOT / "modulos" / "caja-fuerte.html"
    shutil.copy2(src, staging / "caja-fuerte.html")
    shutil.copy2(src, staging / "caja.html")
    (staging / "LEEME.txt").write_text(
        "Caja fuerte — Les vencimos\n"
        "Offline en este aparato. Cifrado Web Crypto (PBKDF2 + AES-GCM).\n"
        "PIN olvidado = datos irrecuperables. No es banco ni nube.\n"
        "Abre caja.html o caja-fuerte.html desde Archivos (file://).\n",
        encoding="utf-8",
    )
    if CAJA_OUT.exists():
        CAJA_OUT.unlink()
    with zipfile.ZipFile(CAJA_OUT, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name in ("LEEME.txt", "caja.html", "caja-fuerte.html"):
            z.write(staging / name, arcname=name)
    shutil.rmtree(staging)
    print(f"Wrote {CAJA_OUT} ({CAJA_OUT.stat().st_size} bytes)")


def main() -> None:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)

    shell_tpl = SRC / "estanteria.shell.html"
    if shell_tpl.exists():
        shell = shell_tpl.read_text(encoding="utf-8")
    else:
        shell = (SRC / "estanteria.html").read_text(encoding="utf-8")
    for pat in ("lv-locked", "lv-gate", "gate.js", "/brand/"):
        if pat in shell:
            raise SystemExit(f"offline shell still contains {pat!r}")
    if "/*__EMBEDDED_MODULES__*/" not in shell:
        raise SystemExit("shell missing EMBEDDED placeholder (need estanteria.shell.html)")

    embedded = build_embedded()
    for need in ("hogar", "salud", "radio", "qr", "electro", "brico", "jardin", "supervive", "apagon", "caja", "gym", "guitarra", "calc", "medica", "medita", "auxilios", "escritura", "dibujo", "info", "guias", "mapas", "alarma", "biblio"):
        if need not in embedded:
            raise SystemExit(f"missing embed {need}")

    final = inject_embedded(shell, embedded)

    # Keep/update shell template with placeholder
    if "/*__EMBEDDED_MODULES__*/" in shell:
        (SRC / "estanteria.shell.html").write_text(shell, encoding="utf-8")

    # Verify no required sibling hrefs for gym/caja
    if re.search(r"href:\s*['\"]gym\.html['\"]", final):
        raise SystemExit("built file still has gym.html href")
    if re.search(r"href:\s*['\"]caja", final):
        raise SystemExit("built file still has caja href")
    if "location.assign(it.href)" in final and "EMBEDDED" not in final:
        raise SystemExit("unexpected")
    # openModule must prefer EMBEDDED
    if "showModuleViewer" not in final:
        raise SystemExit("missing in-page viewer")
    if "EMBEDDED[embedKey]" not in final and "EMBEDDED[embedKey]" not in final:
        # check alternate
        if "EMBEDDED && EMBEDDED[embedKey]" not in final:
            raise SystemExit("openModule does not use EMBEDDED")

    (SRC / "estanteria.html").write_text(final, encoding="utf-8")
    # Live web shell at site root (same single-file build)
    (ROOT / "estanteria.html").write_text(final, encoding="utf-8")
    leeme = write_leeme()
    (SRC / "LEEME.txt").write_text(leeme, encoding="utf-8")

    (STAGING / "estanteria.html").write_text(final, encoding="utf-8")
    (STAGING / "ABRE-AQUI.html").write_text(final, encoding="utf-8")
    (STAGING / "LEEME.txt").write_text(leeme, encoding="utf-8")

    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name in ("LEEME.txt", "ABRE-AQUI.html", "estanteria.html"):
            z.write(STAGING / name, arcname=name)

    shutil.copy2(STAGING / "LEEME.txt", ROOT / "downloads" / "LEEME-estanteria.txt")
    shutil.rmtree(STAGING)

    # Also keep last lettered snapshot name pointing at same bytes (bookmarks).
    snapshot = ROOT / "downloads" / "estanteria-offline-v20260924q.zip"
    shutil.copy2(OUT, snapshot)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"Snapshot {snapshot}")
    print(f"Built HTML size: {(SRC / 'estanteria.html').stat().st_size} bytes")
    with zipfile.ZipFile(OUT) as z:
        print("Estantería contents:", ", ".join(z.namelist()))

    # sizes of embeds
    for k, v in embedded.items():
        print(f"  embed {k}: {len(v)} chars")

    build_caja_zip()
    with zipfile.ZipFile(CAJA_OUT) as z:
        print("Caja contents:", ", ".join(z.namelist()))


if __name__ == "__main__":
    main()
