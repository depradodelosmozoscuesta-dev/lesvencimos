#!/usr/bin/env python3
"""Localize 1º Bach Modo Maestro for offline/APK (ESO _maestro pattern). Idempotent."""
from __future__ import annotations
import re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDU = ROOT / "educacion"
MAESTRO_SRC = ROOT / "profesor" / "_maestro"
PLANTILLA_SRC = ROOT / "profesor" / "_plantilla-leccion"
MAESTRO_FILES = ("maestro-runtime.js", "maestro-puntero.css", "maestro-demo.html", "README.md")
PLANTILLA_FILES = ("leccion-shell.css", "leccion-shell-nav.js")
COURSES = [
    "mates-i", "bgca", "griego", "ingles", "mates-gen", "fyq", "edfisica",
]

def rel_prefix(html: Path, course: Path) -> str:
    rel = html.parent.relative_to(course)
    depth = len(rel.parts) if rel.parts != (".",) else 0
    return "../" * depth if depth else ""

def ensure_assets(course: Path) -> None:
    dst = course / "_maestro"
    dst.mkdir(parents=True, exist_ok=True)
    for fname in MAESTRO_FILES:
        src = MAESTRO_SRC / fname
        if src.is_file():
            shutil.copy2(src, dst / fname)
    for fname in PLANTILLA_FILES:
        src = PLANTILLA_SRC / fname
        if src.is_file() and not (course / fname).is_file():
            shutil.copy2(src, course / fname)

def inject_maestro_head(html: str, prefix: str) -> str:
    css = f'<link rel="stylesheet" href="{prefix}_maestro/maestro-puntero.css"/>'
    js = f'<script src="{prefix}_maestro/maestro-runtime.js" defer></script>'
    if "_maestro/maestro-puntero.css" not in html and "maestro-puntero.css" not in html:
        m = re.search(r'<link rel="stylesheet" href="[^"]*leccion-shell\.css"[^>]*>', html)
        if m:
            html = html[: m.end()] + "\n" + css + html[m.end() :]
        else:
            html = html.replace("</head>", css + "\n</head>", 1)
    if "_maestro/maestro-runtime.js" not in html and "maestro-runtime.js" not in html:
        m = re.search(r'<script src="[^"]*leccion-shell-nav\.js"[^>]*></script>', html)
        if m:
            html = html[: m.end()] + "\n" + js + html[m.end() :]
        else:
            html = html.replace("</head>", js + "\n</head>", 1)
    return html

def inject_atajo(html: str) -> str:
    if "atajo-maestro" in html:
        return html
    atajo = '<a class="atajo atajo-maestro" href="?maestro=1">Modo maestro</a>'
    if "leccion-progreso" in html:
        html = re.sub(r'(<div class="leccion-progreso"[^>]*>)', r"\1\n      " + atajo, html, count=1)
    elif "leccion-atajos" in html:
        html = re.sub(r'(<div class="leccion-atajos"[^>]*>)', r"\1\n    " + atajo, html, count=1)
    elif "leccion-barra" in html:
        html = re.sub(r'(<nav class="leccion-barra"[^>]*>)', r"\1\n    " + atajo, html, count=1)
    elif "leccion-wrap" in html:
        html = re.sub(r'(<div class="leccion-wrap"[^>]*>)', r'\1\n  <p class="maestro-atajo-wrap">' + atajo + "</p>", html, count=1)
    else:
        html = re.sub(r"(<body[^>]*>)", r"\1\n" + atajo, html, count=1)
    return html

def ensure_data_maestro_json(html: str, html_path: Path) -> str:
    if "data-maestro-json=" in html:
        return html
    m = re.search(r"(?:leccion|l|maestro)[-_]?(\d{1,2})", html_path.name, re.I)
    if not m:
        return html
    nn = int(m.group(1))
    json_name = f"maestro-{nn:02d}.json"
    if not (html_path.parent / json_name).is_file():
        return html
    html = re.sub(
        r"<body([^>]*)>",
        lambda mm: f'<body{mm.group(1)} data-maestro-json="{json_name}">'
        if "data-maestro-json" not in mm.group(1)
        else mm.group(0),
        html,
        count=1,
    )
    return html

def rewrite_paths(html: str, prefix: str) -> str:
    html = re.sub(r"(?:(?:\.\./)+)?profesor/_maestro/", f"{prefix}_maestro/", html)
    html = html.replace("/profesor/_maestro/", f"{prefix}_maestro/")
    html = re.sub(
        r"(?:(?:\.\./)+)?profesor/_plantilla-leccion/leccion-shell\.css",
        f"{prefix}leccion-shell.css",
        html,
    )
    html = re.sub(
        r"(?:(?:\.\./)+)?profesor/_plantilla-leccion/leccion-shell-nav\.js",
        f"{prefix}leccion-shell-nav.js",
        html,
    )
    return html

def patch_file(html_path: Path, course: Path) -> bool:
    orig = html_path.read_text(encoding="utf-8")
    prefix = rel_prefix(html_path, course)
    text = rewrite_paths(orig, prefix)
    has_json_nearby = bool(list(html_path.parent.glob("maestro-*.json"))) or bool(
        list(course.glob("maestro-*.json"))
    )
    is_lesson = bool(re.search(r"leccion-|l\d{2}-", html_path.name, re.I)) and html_path.name != "index.html"
    if is_lesson and has_json_nearby:
        text = inject_maestro_head(text, prefix)
        text = ensure_data_maestro_json(text, html_path)
        text = inject_atajo(text)
    if text != orig:
        html_path.write_text(text, encoding="utf-8")
        return True
    return False

def main() -> None:
    for name in COURSES:
        course = EDU / name
        if not course.is_dir():
            print("SKIP", name)
            continue
        ensure_assets(course)
        changed = sum(1 for h in course.rglob("*.html") if patch_file(h, course))
        n_atajo = sum(
            1
            for p in course.rglob("*.html")
            if "atajo-maestro" in p.read_text(encoding="utf-8", errors="ignore")
        )
        n_prof = sum(
            1
            for p in course.rglob("*.html")
            if "profesor/_maestro" in p.read_text(encoding="utf-8", errors="ignore")
        )
        print(f"{name}: changed={changed} atajo={n_atajo} prof_left={n_prof} _maestro={(course/'_maestro'/'maestro-runtime.js').is_file()}")

if __name__ == "__main__":
    main()
