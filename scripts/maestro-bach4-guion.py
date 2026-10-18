#!/usr/bin/env python3
"""Cablea modo Maestro (runtime local _maestro + guion incrustado) en 4 materias de 1º Bach.
Guion derivado SOLO del texto de cada lección: título (h1) y apartados (h2) con su primera frase."""
import re, json, html, shutil, sys
from pathlib import Path
REPO = Path('/workspace/lv-repo')
EDU = REPO/'educacion'
SRC = EDU/'fyq'/'_maestro'
SETS = [  # (curso_id, raíz de materia con _maestro, carpeta de lecciones, patrón)
  ('bach1-dibujo-tec', EDU/'dibujo-tec', EDU/'dibujo-tec'/'lecciones', 'leccion-*.html'),
  ('bach1-tic',        EDU/'tic',        EDU/'tic'/'lecciones',        'leccion-*.html'),
  ('bach1-mates-ccs',  EDU/'mates-ccs',  EDU/'mates-ccs'/'lecciones',  'leccion-*.html'),
  ('bach1-economia',   EDU/'economia',   EDU/'economia'/'economia',    'leccion-*.html'),
  ('bach1-eeae',       EDU/'economia',   EDU/'economia'/'eeae',        'leccion-*.html'),
]
TAG = re.compile(r'<[^>]+>')
def txt(s):
    s = re.sub(r'<(svg|math|script|style|button|select)\b.*?</\1>', ' ', s, flags=re.S | re.I)
    s = TAG.sub(' ', s); s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()
def frase(s, lim=230):
    s = s.strip()
    if not s: return ''
    parts = re.split(r'(?<=[.!?…])\s+(?=[A-ZÁÉÍÓÚÑ¿¡0-9«])', s)
    out = parts[0]
    if len(out) < 70 and len(parts) > 1 and len(out) + len(parts[1]) < lim: out += ' ' + parts[1]
    if len(out) > lim:
        cut = out[:lim].rsplit(' ', 1)[0].rstrip(',;:')
        out = cut + '…'
    return out
def masked(s):
    """Devuelve copia con <script>/<style>/<template>/comentarios en blanco (mismas posiciones)."""
    m = list(s)
    for rx in (r'<script\b.*?</script>', r'<style\b.*?</style>', r'<template\b.*?</template>', r'<!--.*?-->'):
        for x in re.finditer(rx, s, re.S | re.I):
            for i in range(x.start(), x.end()): m[i] = ' '
    return ''.join(m)
def procesa(curso, root, f):
    s = f.read_text(encoding='utf-8')
    if 'maestro-runtime.js' in s: return 'ya'
    # Plantillas vacías previas (guion sin pasos): se sustituyen por el guion derivado
    s = re.sub(r'<script type="application/json" data-maestro="guion">(?:(?!</script>).)*</script>\n?',
               lambda m: '' if '"pasos"' not in m.group(0) else m.group(0), s, flags=re.S)
    ms = masked(s)
    heads = [x for x in re.finditer(r'<(h1|h2)\b([^>]*)>(.*?)</\1>', ms, re.S | re.I)]
    if not heads: return 'sin-titulos'
    pasos, edits = [], []
    for k, h in enumerate(heads[:14]):
        tag, attrs = h.group(1), h.group(2)
        titulo = txt(s[h.start(3):h.end(3)])
        if not titulo: continue
        fin = heads[k+1].start() if k+1 < len(heads) else len(ms)
        trozo = ms[h.end():fin]
        cuerpo = ''
        for p in re.finditer(r'<p\b[^>]*>(.*?)</p>', trozo, re.S | re.I):
            c = txt(s[h.end()+p.start(1):h.end()+p.end(1)])
            if not c or (len(c) < 40 and '.' not in c) or (len(c) < 140 and re.search(r'Decreto|·|Criterio \d', c)): continue
            cuerpo = frase(c); break
        idm = re.search(r'\bid\s*=\s*"([^"]+)"', attrs)
        if idm: aid = idm.group(1)
        else:
            aid = 'maestro-p%d' % (len(pasos)+1)
            edits.append((h.start()+1+len(tag), ' id="%s"' % aid))
        t = titulo.rstrip('.:')
        decir = (t + '. ' + cuerpo) if cuerpo else t + '.'
        pasos.append({'id': 'p%d' % (len(pasos)+1), 'decir': decir, 'ancla': '#' + aid,
                      'puntero': True, 'esperaMs': 400 if not pasos else 300})
    if not pasos: return 'sin-pasos'
    for pos, ins in sorted(edits, reverse=True): s = s[:pos] + ins + s[pos:]
    num = re.search(r'(\d+)', f.name); num = int(num.group(1)) if num else 0
    rel = '../' * (len(f.parent.relative_to(root).parts)) + '_maestro/'
    guion = {'curso': curso, 'leccion': num, 'titulo': pasos[0]['decir'].split('. ')[0],
             'url': f.name, 'musica': False, 'origen': 'derivado del texto de la lección (h1/h2 + primera frase)',
             'pasos': pasos}
    js = json.dumps(guion, ensure_ascii=False, indent=1).replace('</', '<\\/')
    headins = '<link rel="stylesheet" href="%smaestro-puntero.css"/>\n<script src="%smaestro-runtime.js" defer></script>\n' % (rel, rel)
    m2 = masked(s).lower()
    i = m2.find('</head>'); s = s[:i] + headins + s[i:]
    b = re.search(r'<body\b[^>]*>', masked(s), re.I)
    b = re.match(r'<body\b[^>]*>', s[b.start():], re.I) and type('B', (), {'start': lambda self, o=b.start(): o, 'end': lambda self, o=b.start(), L=len(re.match(r'<body\b[^>]*>', s[b.start():], re.I).group(0)): o + L, 'group': lambda self, k=0, t=re.match(r'<body\b[^>]*>', s[b.start():], re.I).group(0): t})()
    bt = b.group(0)
    nb = bt[:-1] + (' data-maestro-json="maestro-%02d.json">' % num)
    s = s[:b.start()] + nb + s[b.end():]
    i = masked(s).lower().rfind('</body>')
    s = s[:i] + '<script type="application/json" data-maestro="guion">\n' + js + '\n</script>\n' + s[i:]
    f.write_text(s, encoding='utf-8')
    return len(pasos)
def main():
    res = {}
    for curso, root, d, pat in SETS:
        dst = root/'_maestro'; dst.mkdir(exist_ok=True)
        for n in ('maestro-runtime.js', 'maestro-puntero.css', 'README.md'):
            shutil.copy2(SRC/n, dst/n)
        r = {}
        for f in sorted(d.glob(pat)): r[f.name] = procesa(curso, root, f)
        res[curso] = r
    json.dump(res, open('/workspace/lv-tools/maestro_bach4_resultado.json', 'w'), ensure_ascii=False, indent=1)
    for c, r in res.items():
        ok = [v for v in r.values() if isinstance(v, int)]
        print(c, 'lecciones', len(r), 'con guion', len(ok), 'pasos min/max', (min(ok), max(ok)) if ok else '-', 'otros', {k: v for k, v in r.items() if not isinstance(v, int)})
main()
