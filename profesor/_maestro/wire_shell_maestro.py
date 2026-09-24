#!/usr/bin/env python3
"""Wire a leccion-NN-*.html shell for modo maestro (idempotent).
Adds runtime CSS/JS, data-maestro-json, atajo, and maestro-* ids on key blocks.
Does NOT invent guion content — only DOM hooks.
"""
from __future__ import annotations
import re, json, sys
from pathlib import Path

CSS = '<link rel="stylesheet" href="../../_maestro/maestro-puntero.css"/>'
JS = '<script src="../../_maestro/maestro-runtime.js" defer></script>'

def wire(shell: Path, nn: int, curso: str, titulo: str, pasos: list) -> dict:
    t = shell.read_text(encoding='utf-8')
    orig = t
    # head assets
    if '_maestro/maestro-puntero.css' not in t:
        planted = False
        for css_href in (
            '<link rel="stylesheet" href="../../_plantilla-leccion/leccion-shell.css"/>',
            '<link rel="stylesheet" href="leccion-shell.css"/>',
        ):
            if css_href in t:
                t = t.replace(css_href, css_href + '\n' + CSS, 1)
                planted = True
                break
        if not planted:
            t = t.replace('</head>', CSS + '\n</head>', 1)
    if '_maestro/maestro-runtime.js' not in t:
        # Prefer inserting after plantilla nav script (online) or any nav script (offline flat).
        planted = False
        for nav in (
            '<script src="../../_plantilla-leccion/leccion-shell-nav.js" defer></script>',
            '<script src="leccion-shell-nav.js" defer></script>',
        ):
            if nav in t:
                t = t.replace(nav, nav + '\n' + JS, 1)
                planted = True
                break
        if not planted:
            t = t.replace('</head>', JS + '\n</head>', 1)
    # body attr
    json_name = f'maestro-{nn:02d}.json'
    if 'data-maestro-json=' not in t:
        t = re.sub(
            r'<body([^>]*)>',
            lambda m: f'<body{m.group(1)} data-maestro-json="{json_name}">'
            if 'data-maestro-json' not in m.group(1)
            else m.group(0),
            t,
            count=1,
        )
    else:
        t = re.sub(r'data-maestro-json="[^"]*"', f'data-maestro-json="{json_name}"', t, count=1)
    # atajo in progresion bar if present
    if 'atajo-maestro' not in t:
        # after progreso-texto or inside leccion-progreso
        if 'leccion-progreso' in t:
            t = re.sub(
                r'(<div class="leccion-progreso"[^>]*>)',
                r'\1\n      <a class="atajo atajo-maestro" href="?maestro=1">Modo maestro</a>',
                t,
                count=1,
            )
        elif 'leccion-barra' in t:
            t = re.sub(
                r'(<nav class="leccion-barra"[^>]*>)',
                r'\1\n    <a class="atajo atajo-maestro" href="?maestro=1">Modo maestro</a>',
                t,
                count=1,
            )
        else:
            # inject near top of wrap
            t = re.sub(
                r'(<div class="leccion-wrap">)',
                r'\1\n  <p class="maestro-atajo-wrap"><a class="atajo atajo-maestro" href="?maestro=1">Modo maestro</a></p>',
                t,
                count=1,
            )

    def ensure_id(html: str, pattern: str, mid: str, data: str) -> str:
        # If pattern matches a tag without id=maestro-*, add id and data-maestro
        def repl(m):
            tag = m.group(0)
            if f'id="{mid}"' in tag or f"id='{mid}'" in tag:
                return tag
            # insert after first word of opening tag
            return re.sub(
                r'^<(\w+)',
                rf'<\1 id="{mid}" data-maestro="{data}"',
                tag,
                count=1,
            )
        return re.sub(pattern, repl, html, count=1, flags=re.I)

    # Title block
    if 'id="maestro-titulo"' not in t:
        if re.search(r'<header[^>]*class="[^"]*bloque-titulo', t):
            t = ensure_id(t, r'<header[^>]*class="[^"]*bloque-titulo[^"]*"[^>]*>', 'maestro-titulo', 'titulo')
        elif re.search(r'<h1[^>]*>', t):
            # wrap or tag the first h1's parent section — tag h1 itself + a section
            t = re.sub(
                r'(<h1)([^>]*>)',
                r'<header class="bloque-titulo" id="maestro-titulo" data-maestro="titulo">\n    \1\2',
                t,
                count=1,
            )
            # close header after h1 block roughly: after first </h1> and maybe following p
            t = re.sub(r'(</h1>\s*(?:<p[^>]*>.*?</p>\s*)?)', r'\1\n  </header>', t, count=1, flags=re.S)

    # Map common h2 texts to anchors
    h2_map = [
        (r'Objetivos', 'maestro-objetivos', 'objetivos'),
        (r'Explicaci[oó]n', 'maestro-explicacion', 'explicacion'),
        (r'Ejemplos?', 'maestro-ejemplos', 'ejemplos'),
        (r'Pr[aá]ctica', 'maestro-practica', 'practica'),
        (r'Glosario', 'maestro-glosario', 'glosario'),
        (r'Mini cierre|Cierre|Recuerda', 'maestro-cierre', 'cierre'),
        (r'Reto', 'maestro-reto', 'reto'),
        (r'Comprueba|Mini-?quiz|Quiz', 'maestro-quiz', 'quiz'),
    ]
    for pat, mid, data in h2_map:
        if f'id="{mid}"' in t:
            continue
        # find <h2>...</h2> matching
        m = re.search(rf'(<h2[^>]*>)([^<]*{pat}[^<]*)(</h2>)', t, flags=re.I)
        if not m:
            continue
        # Prefer id on surrounding section if exists just before
        # Put id on the h2
        t = t[: m.start()] + f'<h2 id="{mid}" data-maestro="{data}">' + m.group(2) + m.group(3) + t[m.end() :]

    # First iframe / interactivo / tinta block
    if 'id="maestro-interactivo"' not in t:
        m = re.search(
            r'(<(?:section|div)[^>]*(?:interactivo|marco-interactivo|widget|tinta)[^>]*>)',
            t,
            flags=re.I,
        )
        if m:
            tag = m.group(1)
            if 'id=' not in tag:
                newt = re.sub(r'^<(\w+)', r'<\1 id="maestro-interactivo" data-maestro="interactivo"', tag, count=1)
                t = t[: m.start()] + newt + t[m.end() :]
        else:
            m2 = re.search(r'(<iframe\b[^>]*>)', t, flags=re.I)
            if m2:
                # wrap iframe with section
                start = m2.start()
                end = t.find('</iframe>', m2.end())
                if end > 0:
                    end += len('</iframe>')
                    block = t[start:end]
                    wrapped = f'<section class="bloque-interactivo" id="maestro-interactivo" data-maestro="interactivo">{block}</section>'
                    t = t[:start] + wrapped + t[end:]

    # Curiosidad / vida / aside
    if 'id="maestro-curiosidad"' not in t:
        m = re.search(r'(<aside[^>]*class="[^"]*curiosidad[^"]*"[^>]*>)', t, flags=re.I)
        if m and 'id=' not in m.group(1):
            newt = re.sub(r'^<aside', '<aside id="maestro-curiosidad" data-maestro="curiosidad"', m.group(1), count=1)
            t = t[: m.start()] + newt + t[m.end() :]

    # Embed guion JSON for file:// fallback
    guion = {
        'curso': curso,
        'leccion': nn,
        'titulo': titulo,
        'url': shell.name,
        'musica': False,
        'pasos': pasos,
    }
    guion_tag = (
        '<script type="application/json" data-maestro="guion">\n'
        + json.dumps(guion, ensure_ascii=False, indent=2)
        + '\n</script>\n'
    )
    if 'data-maestro="guion"' in t:
        t = re.sub(
            r'<script type="application/json" data-maestro="guion">.*?</script>\s*',
            guion_tag,
            t,
            count=1,
            flags=re.S,
        )
    else:
        t = t.replace('</body>', guion_tag + '</body>', 1)

    changed = t != orig
    if changed:
        shell.write_text(t, encoding='utf-8')
    return {'changed': changed, 'path': str(shell), 'json': json_name}

if __name__ == '__main__':
    print('helper module — import wire() from subject scripts')
