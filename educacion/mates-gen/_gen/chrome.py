# -*- coding: utf-8 -*-
from pathlib import Path
import json, html as H, hashlib

ROOT = Path('/workspace/lesvencimos/staging/bach1/mates-gen')
LEC = ROOT / 'lecciones'
SLUGS = [
'que-son-matematicas-generales','conteo-principios-basicos','palomar-e-inclusion-exclusion','arboles-y-combinatoria','documentos-numericos-cotidianos',
'potencias-raices-logaritmos','matrices-clasificacion-operaciones','matrices-tablas-y-grafos','razones-proporciones-porcentajes','educacion-financiera',
'probabilidad-como-medida','variacion-absoluta-y-media','limite-idea-de-cambio','derivada-concepto-e-interpretacion','grafos-tipos-y-representacion',
'euler-y-grafos-planos','eulerianos-hamiltonianos-coloracion','camino-minimo','patrones-y-generalizacion','funciones-afines',
'funciones-cuadraticas','racionales-trozos-periodicas','exponenciales-y-logaritmicas','sistemas-de-ecuaciones','inecuaciones-y-sistemas',
'programacion-lineal','pensamiento-computacional','estadistica-interpretacion','variables-bidimensionales','regresion-correlacion-causalidad',
'coeficientes-prediccion','probabilidad-compuesta-condicionada','probabilidad-total-y-bayes','uniforme-binomial-normal','muestreo-e-inferencia',
'emociones-error-y-equipo','inclusion-historia-matematicas','proyecto-integrador-cierre']
BLOQUES = [''] + [
'F · Socioafectivo','A · Numérico','A · Numérico','A · Numérico','A · Numérico','A · Numérico','A · Numérico','A · Numérico','A · Numérico','A · Numérico',
'B · Medida','B · Medida','B · Medida','B · Medida','C · Espacial','C · Espacial','C · Espacial','C · Espacial','D · Algebraico','D · Algebraico',
'D · Algebraico','D · Algebraico','D · Algebraico','D · Algebraico','D · Algebraico','D · Algebraico','D · Algebraico','E · Estocástico','E · Estocástico','E · Estocástico',
'E · Estocástico','E · Estocástico','E · Estocástico','E · Estocástico','E · Estocástico','F · Socioafectivo','F · Socioafectivo','A–F · Cierre']

STYLE = r'''
.pasos{list-style:none;margin:0 0 1rem;padding:0;counter-reset:paso}
.pasos li{position:relative;margin:0 0 .7rem;padding:.7rem .8rem .7rem 3.1rem;background:var(--lv-panel);border:1px solid var(--lv-linea);border-radius:10px}
.pasos li::before{counter-increment:paso;content:counter(paso);position:absolute;left:.65rem;top:.7rem;width:1.7rem;height:1.7rem;border-radius:50%;background:#C4A15A;color:#1A160E;font-weight:700;font-size:.9rem;display:flex;align-items:center;justify-content:center}
.figura-svg{background:#161512;border:1px solid var(--lv-linea);border-radius:10px;padding:.5rem;margin:.5rem 0 1.1rem}
.figura-svg svg{width:100%;height:auto;display:block}
.ej{margin:0 0 1rem;padding:.85rem .95rem;background:var(--lv-panel);border:1px solid var(--lv-linea);border-left:3px solid #C4A15A;border-radius:10px}
.ej h3{margin:0 0 .35rem;font-family:var(--lv-serif);font-size:1.05rem;color:var(--lv-titulo)}
.editor,textarea.editor{width:100%;min-height:5.5rem;font-family:ui-monospace,monospace;font-size:.95rem;line-height:1.45;padding:.55rem .65rem;border:1px solid rgba(196,161,90,.45);border-radius:8px;background:#161512;color:#E6E1D6;resize:vertical}
.lienzo{display:block;width:100%;height:280px;background:#161512;border:1px solid #C4A15A;border-radius:8px;touch-action:none;cursor:crosshair}
.fila{display:flex;flex-wrap:wrap;gap:.4rem;margin:.45rem 0}
.boton{font:inherit;font-weight:700;font-size:.85rem;padding:.4rem .8rem;border-radius:999px;border:1px solid #C4A15A;background:transparent;color:#E6E1D6;cursor:pointer}
.porque{margin-top:.55rem;padding:.65rem .75rem;background:#1a2218;border-radius:8px;color:#E6E1D6}
.dato{font-size:.95rem;color:var(--lv-suave)}
.glosa{display:block;font-size:.9rem;color:#9A9488;margin:.25rem 0 .5rem;line-height:1.4}
.lab-box{margin:1rem 0;padding:.85rem;border:1px dashed rgba(196,161,90,.5);border-radius:10px;background:#141210}
.lab-box iframe{width:100%;min-height:320px;border:1px solid #C4A15A;border-radius:8px;background:#0E0E0C}
table.datos{width:100%;border-collapse:collapse;margin:.45rem 0 1rem;font-size:.98rem}
table.datos th,table.datos td{border:1px solid var(--lv-linea);padding:.4rem .55rem;text-align:left}
table.datos th{background:#161512;color:#C4A15A}
'''

JS = r'''(function(){function liga(c){var ctx=c.getContext('2d');function fondo(){ctx.fillStyle='#161512';ctx.fillRect(0,0,c.width,c.height);ctx.strokeStyle='#C4A15A';ctx.strokeRect(.5,.5,c.width-1,c.height-1);}function fit(){var r=c.getBoundingClientRect();var w=Math.max(320,Math.floor(r.width));if(c.width!==w){c.width=w;c.height=280;fondo();}}var dib=false,last=null;function pos(ev){var r=c.getBoundingClientRect();var s=ev.touches?ev.touches[0]:ev;return{x:(s.clientX-r.left)*c.width/r.width,y:(s.clientY-r.top)*c.height/r.height};}c.addEventListener('pointerdown',function(ev){dib=true;last=pos(ev);ev.preventDefault();});c.addEventListener('pointermove',function(ev){if(!dib)return;var p=pos(ev);ctx.strokeStyle='#E6E1D6';ctx.lineWidth=2.2;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(last.x,last.y);ctx.lineTo(p.x,p.y);ctx.stroke();last=p;ev.preventDefault();});function up(){dib=false;}c.addEventListener('pointerup',up);c.addEventListener('pointerleave',up);var b=document.querySelector('[data-clear="'+c.id+'"]');if(b)b.addEventListener('click',fondo);fit();window.addEventListener('resize',fit);}document.querySelectorAll('canvas.lienzo').forEach(liga);})();'''

def href(n):
    return f'leccion-{n:02d}-{SLUGS[n-1]}.html'

def lab_href(n):
    return f'l{n:02d}-{SLUGS[n-1]}.html'

def svg(title, inner, h=300):
    return (
        f'<div class="figura-svg"><svg viewBox="0 0 720 {h}" role="img" aria-label="{H.escape(title)}">'
        f'<title>{H.escape(title)}</title><rect width="720" height="{h}" fill="#161512"/>{inner}</svg></div>'
    )

def ejes(ox=80, oy=240, x2=680, y2=40):
    return (
        f'<line x1="{ox}" y1="{oy}" x2="{x2}" y2="{oy}" stroke="#9A9488" stroke-width="1.5"/>'
        f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{y2}" stroke="#9A9488" stroke-width="1.5"/>'
    )

def ej(num, titulo, enunciado, porque, eid):
    if len(porque) < 160:
        raise ValueError(f'porque demasiado corto en ej {eid}: {porque!r}')
    return (
        f'<article class="ej"><h3>{num}. {titulo}</h3><p>{enunciado}</p>'
        f'<label for="{eid}">Tu resolución</label><textarea class="editor" id="{eid}" placeholder="Escribe aquí el razonamiento completo…"></textarea>'
        f'<details class="porque"><summary>Por qué (abre cuando hayas escrito)</summary><p>{porque}</p></details></article>'
    )

def comprueba(items):
    bits = []
    for q, a in items:
        if len(a) < 140:
            raise ValueError(f'Comprueba demasiado corto: {q!r} → {a!r}')
        bits.append(f'<details class="porque"><summary>{q}</summary><p>{a}</p></details>')
    return '\n'.join(bits)

def pasos_ol(items):
    """items: list of (texto_paso, glosa)"""
    out = ['<ol class="pasos">']
    for t, g in items:
        out.append(f'<li>{t}<span class="glosa">{g}</span></li>')
    out.append('</ol>')
    return '\n'.join(out)

def canvas_block(cid):
    return (
        f'<canvas id="{cid}" class="lienzo" width="900" height="280"></canvas>'
        f'<div class="fila"><button type="button" class="boton" data-clear="{cid}">Borrar lienzo</button></div>'
    )

def lab_embed(n, titulo_lab):
    return (
        f'<div class="lab-box"><p><strong>Laboratorio</strong> — {titulo_lab}. '
        f'Si el marco no carga, abre el hermano: '
        f'<a href="{lab_href(n)}">{lab_href(n)}</a>.</p>'
        f'<iframe src="{lab_href(n)}" title="{H.escape(titulo_lab)}" loading="lazy"></iframe></div>'
    )

def write_lab(n, titulo, body_inner):
    """Hermano lNN-slug.html autocontenido carbón+ámbar."""
    nn = f'{n:02d}'
    slug = SLUGS[n-1]
    html = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Lab L{nn} · {H.escape(titulo)}</title>
<link rel="stylesheet" href="../leccion-shell.css"/>
<style>body{{margin:0;padding:1rem;background:#0E0E0C;color:#E6E1D6;font-family:system-ui,sans-serif}}
h1{{font-size:1.15rem;color:#C4A15A}} .panel{{background:#161512;border:1px solid #C4A15A;border-radius:10px;padding:.8rem;margin:.6rem 0}}
button{{font:inherit;font-weight:700;padding:.35rem .75rem;border-radius:999px;border:1px solid #C4A15A;background:transparent;color:#E6E1D6;cursor:pointer;margin:.2rem}}
canvas{{display:block;width:100%;max-width:640px;background:#12100e;border:1px solid #9A9488;border-radius:8px}}
input,select{{background:#161512;color:#E6E1D6;border:1px solid #C4A15A;border-radius:6px;padding:.3rem .5rem}}
.out{{min-height:2rem;color:#8F9A72;margin-top:.5rem}}</style></head>
<body>
<p><a href="{href(n)}" style="color:#C4A15A">← Volver a la lección {nn}</a></p>
<h1>Laboratorio · L{nn} · {H.escape(titulo)}</h1>
{body_inner}
</body></html>'''
    (LEC / f'l{nn}-{slug}.html').write_text(html, encoding='utf-8')

def default_pasos(n, plain, curiosidad_t, sabers_hint):
    return [
        {'id': 'abrir', 'dicho': f'Lección {n:02d}: {plain}. {curiosidad_t}.', 'hacer': 'Leer situarte y los objetivos en voz alta.'},
        {'id': 'idea', 'dicho': f'Hoy trabajamos: {sabers_hint}. Mira el gráfico SVG antes de los números.', 'hacer': 'Observar la figura y nombrar qué representa cada símbolo.'},
        {'id': 'ej1', 'dicho': 'Primer ejemplo resuelto: sigue cada paso y la glosa debajo.', 'hacer': 'Recalcular el ejemplo 1 en papel o en el editor.'},
        {'id': 'ej2', 'dicho': 'Segundo ejemplo: cambia el contexto pero no la herramienta.', 'hacer': 'Recalcular el ejemplo 2 y comparar con el 1.'},
        {'id': 'practica', 'dicho': 'Ahora los ejercicios: escribe el razonamiento completo, no solo el número.', 'hacer': 'Resolver al menos dos ejercicios; dibujar en el lienzo si pide figura.'},
        {'id': 'lab', 'dicho': 'Si hay laboratorio, ábrelo y prueba un caso distinto al del texto.', 'hacer': 'Usar el lab o el iframe embebido.'},
        {'id': 'comprueba', 'dicho': 'Comprueba: responde mentalmente antes de abrir el porqué.', 'hacer': 'Hacer las tres preguntas del bloque Comprueba.'},
        {'id': 'reto', 'dicho': 'Cierra con el reto Profesor: deja constancia escrita.', 'hacer': 'Escribir el reto en el editor o en el portfolio.'},
    ]

def write_dense(n, titulo_html, saber, curiosidad_t, curiosidad, objetivos, body_html, comps, reto_t, reto_p, pasos=None, lab_title=None):
    if n < 5:
        raise RuntimeError(f'write_dense bloqueado para L{n:02d}: no se toca L01–L04')
    nn = f'{n:02d}'
    plain = titulo_html.replace('<em>', '').replace('</em>', '')
    objs = ''.join(f'<li>{o}</li>' for o in objetivos)
    prev_h = (
        f'<a class="atajo atajo-prev" href="../index.html">← Anterior</a>' if n == 1
        else f'<a class="atajo atajo-prev" href="{href(n-1)}">← Anterior</a>'
    )
    nxt = '../index.html' if n == 38 else href(n + 1)
    w = round(n / 38 * 100, 2)
    w = int(w) if w == int(w) else w
    if pasos is None:
        pasos = default_pasos(n, plain, curiosidad_t, saber)
    # validate comps
    comp_html = comprueba(comps)
    maestro = {'curso': 'bach1-mates-gen', 'leccion': n, 'titulo': plain, 'url': href(n), 'musica': False, 'pasos': pasos}
    (LEC / f'maestro-{nn}.json').write_text(json.dumps(maestro, ensure_ascii=False, indent=2), encoding='utf-8')
    lab_note = ''
    if lab_title:
        lab_note = lab_embed(n, lab_title)
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#0E0E0C"/>
<title>Lección {nn} · {H.escape(plain)} · Les vencimos</title>
<link rel="icon" href="../icons/favicon.svg" type="image/svg+xml"/>
<link rel="manifest" href="../manifest.webmanifest"/>
<link rel="stylesheet" href="../leccion-shell.css"/>
<style>{STYLE}</style>
<script src="../leccion-shell-nav.js" defer></script>
</head>
<body class="leccion-shell" data-maestro-json="maestro-{nn}.json">
<div class="leccion-wrap">
<nav class="leccion-barra" aria-label="Navegación de lección" data-actual="{n}" data-total="38">
  <div class="leccion-progreso" role="status">
    <span class="progreso-texto"><strong>{n}</strong> de <strong>38</strong></span>
    <div class="progreso-pista" aria-hidden="true"><div class="progreso-lleno" style="width:{w}%"></div></div>
  </div>
  <div class="leccion-atajos">
    <a class="atajo atajo-calc" href="../../../../modulos/calculadora.html" title="Calculadora offline">Calculadora</a>
    {prev_h}
    <a class="atajo atajo-next" href="{nxt}">Siguiente →</a>
  </div>
</nav>
<header class="leccion-top">
  <a class="leccion-marca" href="../../../../index.html">Les <span>vencimos</span></a>
  <p class="leccion-meta-top">Matemáticas Generales · 1º Bachillerato</p>
</header>
<header class="bloque-titulo">
  <span class="eyebrow">Lección {nn} · {BLOQUES[n]}</span>
  <h1 class="titulo-leccion">{titulo_html}</h1>
  <p class="meta-leccion">1º Bach Matemáticas Generales · CyL Decreto 40/2022 · {saber}</p>
</header>
<aside class="bloque-curiosidad" aria-label="Para situarte">
  <p class="etiqueta-bloque">Para situarte</p>
  <h2 class="titulo-curiosidad">{curiosidad_t}</h2>
  <p class="texto-curiosidad">{curiosidad}</p>
</aside>
<section class="bloque-cuerpo">
  <h2>Objetivos</h2>
  <ul>{objs}</ul>
</section>
{body_html}
{lab_note}
<section class="bloque-cuerpo">
  <h2>Comprueba</h2>
  <p class="dato">Tres preguntas. Responde mentalmente antes de abrir el porqué.</p>
  {comp_html}
</section>
<section class="bloque-reto">
  <span class="etiqueta-reto">Reto Profesor</span>
  <h2 class="titulo-reto">{reto_t}</h2>
  <p>{reto_p}</p>
  <p class="reto-id">reto_id: bach1-mates-gen-L{nn}</p>
</section>
<footer class="leccion-pie"><strong>Les vencimos</strong> · L{nn} de 38 · Matemáticas Generales · staging · file:// · sin publicar</footer>
</div>
<script type="application/json" data-maestro="guion">{json.dumps(maestro, ensure_ascii=False)}</script>
<script>{JS}</script>
</body>
</html>'''
    path = LEC / href(n)
    path.write_text(html, encoding='utf-8')
    return path.stat().st_size

def md5_pack():
    """MD5 documentado: concatena nombre+bytes de cada leccion-*.html ordenado por nombre."""
    files = sorted(LEC.glob('leccion-*.html'))
    h = hashlib.md5()
    for f in files:
        h.update(f.name.encode()); h.update(b'\0'); h.update(f.read_bytes())
    return len(files), h.hexdigest()

def md5_explain():
    n, digest = md5_pack()
    return (
        f'Receta MD5: para cada archivo `lecciones/leccion-*.html` ordenado por nombre, '
        f'se concatena `nombre + NUL + contenido` y se hace MD5 del flujo. '
        f'No incluye index.html ni maestro-*.json ni labs. Archivos={n}. Digest={digest}.'
    )
