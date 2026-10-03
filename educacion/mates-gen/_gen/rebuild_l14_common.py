# -*- coding: utf-8 -*-
"""Utilidades del listón L14. No escribe lecciones por sí solo."""
import hashlib, re, sys
from pathlib import Path
sys.path.insert(0, '/workspace/lesvencimos/staging/bach1/mates-gen/_gen')
from chrome import *

PROTECT = tuple(range(1, 14))  # L01–L13 ya al listón; L14 ya no está protegida
TAGS = ('<line', '<path', '<circle', '<polygon')

def _md5(n):
    files = list(LEC.glob(f'leccion-{n:02d}-*.html'))
    if len(files) != 1:
        raise SystemExit(f'esperado 1 html para L{n:02d}, hay {files}')
    return files[0], hashlib.md5(files[0].read_bytes()).hexdigest()

def snapshot():
    return {n: _md5(n) for n in PROTECT}

def assert_untouched(snap):
    for n, (path, dig) in snap.items():
        now = hashlib.md5(path.read_bytes()).hexdigest()
        if now != dig:
            raise SystemExit(f'PROTEGIDA MODIFICADA L{n:02d}')

def nstrokes(s):
    return sum(s.count(t) for t in TAGS)

def path_fn(fn, x0, x1, n, X, Y, stroke='#C4A15A', width='2.5'):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append(f'{X(x):.1f},{Y(fn(x)):.1f}')
    return f'<path d="M {" L ".join(pts)}" fill="none" stroke="{stroke}" stroke-width="{width}"/>'

def barra(x, y_top, w, h, fill='#C4A15A'):
    yb = y_top + h
    return (f'<polygon points="{x},{yb} {x+w},{yb} {x+w},{y_top} {x},{y_top}" '
            f'fill="{fill}" stroke="#E6E1D6" stroke-width="1"/>')

def narrar(frases):
    if len(frases) < 6:
        raise ValueError('maestro corto')
    ids = ['abrir', 'figura', 'ej1', 'ej2', 'ej3', 'practica', 'cierre']
    hacer = [
        'Leer en voz alta el apartado Para situarte y los objetivos.',
        'Mirar el SVG y decir qué dato numérico marca cada trazo.',
        'Rehacer el ejemplo 1, glosa a glosa, sin mirar el resultado final.',
        'Rehacer el ejemplo 2 y contrastarlo con el 1.',
        'Rehacer el ejemplo 3 y anotar la comprobación.',
        'Escribir el razonamiento de al menos dos ejercicios y usar el lienzo.',
        'Contestar Comprueba antes de abrir y dejar el reto por escrito.',
    ]
    return [{'id': i, 'dicho': d, 'hacer': h} for i, d, h in zip(ids, frases, hacer)]

def build(n, titulo_html, saber, cur_t, cur, objetivos, explicacion, fig_title, fig_inner,
          ejemplos, ejercicios, comps, reto_t, reto_p, frases, lab_title=None):
    if n in PROTECT:
        raise RuntimeError(f'build rechaza L{n}')
    if nstrokes(fig_inner) < 3:
        raise RuntimeError(f'L{n:02d} SVG con pocos trazos: {nstrokes(fig_inner)}')
    if len(ejemplos) < 3 or len(ejercicios) < 3 or len(comps) != 3:
        raise RuntimeError(f'L{n:02d} recuento ejemplos/ejercicios/comprueba')
    parts = ['<section class="bloque-cuerpo">', explicacion,
             '<h2>Gráfico del ejemplo</h2>',
             '<p class="dato">La figura no es decoración: los trazos corresponden a los números del ejemplo 1.</p>',
             svg(fig_title, fig_inner, h=320)]
    for i, (tit, enun, pasos) in enumerate(ejemplos, 1):
        if not 3 <= len(pasos) <= 4:
            raise RuntimeError(f'L{n:02d} ejemplo {i} tiene {len(pasos)} pasos')
        for tx, gl in pasos:
            if len(gl) < 25:
                raise RuntimeError(f'L{n:02d} glosa corta en ejemplo {i}: {gl!r}')
        block = f'<h2>Ejemplo resuelto {i} — {tit}</h2><p>{enun}</p>{pasos_ol(pasos)}'
        plain = re.sub(r'<[^>]+>', '', block)
        if len(plain) < 250:
            raise RuntimeError(f'L{n:02d} ejemplo {i} corto ({len(plain)}): {plain[:120]}')
        parts.append(block)
    parts.append('<h2>Ejercicios</h2>')
    parts.append('<p class="dato">Escribe el razonamiento completo en el editor, no solo la cifra. Si el enunciado pide figura, dibújala en el lienzo de esta misma página.</p>')
    for num, tit, enun, porque, eid in ejercicios:
        if len(porque) < 160:
            raise RuntimeError(f'porque corto {eid} ({len(porque)})')
        parts.append(ej(num, tit, enun, porque, eid))
    parts.append('<h2>Dibuja en el lienzo</h2>')
    parts.append('<p>Reproduce a mano el gráfico del ejemplo: ejes o nodos, los datos numéricos y una frase con la conclusión. El botón borra el lienzo sin salir de la lección.</p>')
    parts.append(canvas_block(f'lienzo{n:02d}'))
    parts.append('</section>')
    body = '\n'.join(parts)
    for bad in ('Ussar', 'Impossible', 'Compueba', 'Ejemplo resuelto extra'):
        if bad in body or bad in cur or bad in reto_p:
            raise RuntimeError(f'cadena prohibida {bad} en L{n:02d}')
    size = write_dense(
        n, titulo_html, saber, cur_t, cur, objetivos, body, comps, reto_t, reto_p,
        pasos=narrar(frases), lab_title=lab_title,
    )
    print(f'L{n:02d} {size} B')
    return size
