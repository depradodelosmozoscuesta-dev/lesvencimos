#!/usr/bin/env python3
"""Rebuild biblioteca BOOKS embed + catalog + offline zip from biblioteca-libros/."""
from __future__ import annotations
import json, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "modulos" / "biblioteca-libros"
HTML = ROOT / "modulos" / "biblioteca.html"
BIBLIO = ROOT / "modulos" / "biblio.html"
CATALOG = LIB / "catalog.json"
ZIP_OUT = ROOT / "downloads" / "biblioteca-offline.zip"
INLINE_CAP = 45000  # keep zip/html lean; huge texts still load via src


def load_books():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    books = []
    for meta in catalog:
        bid = meta["id"]
        entry = {
            "id": bid,
            "titulo": meta["titulo"],
            "autor": meta["autor"],
            "nota": meta.get("nota", ""),
            "categoria": meta.get("categoria", "narrativa"),
        }
        path = LIB / f"{bid}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            texto = data.get("texto") or ""
            entry["src"] = f"biblioteca-libros/{bid}.json"
            entry["inline"] = True
            if len(texto) > INLINE_CAP:
                entry["texto"] = texto[:INLINE_CAP]
                entry["chars"] = len(texto)
            else:
                entry["texto"] = texto
                entry["chars"] = len(texto)
            for k in ("titulo", "autor", "nota", "categoria"):
                if data.get(k):
                    entry[k] = data[k]
        else:
            entry["inline"] = False
            entry["texto"] = meta.get("texto", "")
            entry["chars"] = len(entry["texto"])
        books.append(entry)
    return books


def inject_books(html: str, books: list) -> str:
    payload = json.dumps(books, ensure_ascii=False, separators=(",", ":"))
    # Escape </script> breakouts (HTML parser ignores JS string context)
    payload = payload.replace("<", "\\u003c")
    m = re.search(r"var BOOKS = \[.*?\];\n", html, flags=re.S)
    if not m:
        raise SystemExit("BOOKS inject failed (n=0)")
    return html[: m.start()] + "var BOOKS = " + payload + ";\n" + html[m.end() :]


def build_zip():
    if ZIP_OUT.exists():
        ZIP_OUT.unlink()
    with zipfile.ZipFile(ZIP_OUT, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(HTML, "biblioteca.html")
        z.write(BIBLIO, "biblio.html")
        leeme = ROOT / "downloads" / "LEEME-biblioteca.txt"
        if leeme.exists():
            z.write(leeme, "LEEME.txt")
        for p in sorted(LIB.glob("*.json")):
            z.write(p, f"biblioteca-libros/{p.name}")
    return ZIP_OUT.stat().st_size


def main():
    books = load_books()
    html = HTML.read_text(encoding="utf-8")
    html = inject_books(html, books)
    HTML.write_text(html, encoding="utf-8")
    BIBLIO.write_text(html, encoding="utf-8")
    size = build_zip()
    print(f"books={len(books)} html={HTML.stat().st_size} zip={size}")


if __name__ == "__main__":
    main()
