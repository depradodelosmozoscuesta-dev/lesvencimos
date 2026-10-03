# -*- coding: utf-8 -*-
"""Helpers for dense Matemáticas Generales lessons."""
from chrome import write_dense, ej

def figura(titulo, inner, h=300):
    return (
        f'<div class="figura-svg"><svg viewBox="0 0 720 {h}" role="img" aria-label="{titulo}">'
        f'<title>{titulo}</title><rect width="720" height="{h}" fill="#161512"/>{inner}</svg></div>'
    )

def tabla(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    body = []
    for r in rows:
        body.append('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>')
    return '<table class="datos"><thead><tr>' + th + '</tr></thead><tbody>' + ''.join(body) + '</tbody></table>'

def pasos(items):
    lis = ''.join(f'<li>{it}</li>' for it in items)
    return f'<ol class="pasos">{lis}</ol>'

def canvas(n, titulo, texto):
    nn = f'{n:02d}'
    return (
        f'<h2>{titulo}</h2><p>{texto}</p>'
        f'<canvas id="lienzo{nn}" class="lienzo" width="900" height="260" aria-label="Lienzo de la lección {nn}"></canvas>'
        f'<div class="fila"><button type="button" class="boton" data-clear="lienzo{nn}">Borrar lienzo</button></div>'
    )

def seccion(chunks):
    return '<section class="bloque-cuerpo">' + ''.join(chunks) + '</section>'

def publicar(n, titulo, saber, ct, cu, objs, chunks, comps, rt, rp):
    sz = write_dense(n, titulo, saber, ct, cu, objs, seccion(chunks), comps, rt, rp)
    print(f'L{n:02d} {sz}')
    return sz
