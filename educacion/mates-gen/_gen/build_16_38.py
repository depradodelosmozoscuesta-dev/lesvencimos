#!/usr/bin/env python3
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
BLOQUES = ['']+[
'F · Socioafectivo','A · Numérico','A · Numérico','A · Numérico','A · Numérico','A · Numérico','A · Numérico','A · Numérico','A · Numérico','A · Numérico',
'B · Medida','B · Medida','B · Medida','B · Medida','C · Espacial','C · Espacial','C · Espacial','C · Espacial','D · Algebraico','D · Algebraico',
'D · Algebraico','D · Algebraico','D · Algebraico','D · Algebraico','D · Algebraico','D · Algebraico','D · Algebraico','E · Estocástico','E · Estocástico','E · Estocástico',
'E · Estocástico','E · Estocástico','E · Estocástico','E · Estocástico','E · Estocástico','F · Socioafectivo','F · Socioafectivo','A–F · Cierre']
TITLES = {
16:'Euler y grafos <em>planos</em>',17:'Eulerianos, hamiltonianos y <em>coloración</em>',18:'El problema del camino <em>mínimo</em>',19:'Patrones y <em>generalización</em>',
20:'Funciones <em>afines</em>',21:'Funciones <em>cuadráticas</em>',22:'Racionales, a trozos y <em>periódicas</em>',23:'Exponenciales y <em>logarítmicas</em>',
24:'Sistemas de <em>ecuaciones</em>',25:'Inecuaciones y <em>sistemas</em>',26:'Programación <em>lineal</em>',27:'Pensamiento <em>computacional</em>',
28:'Estadística: <em>interpretación</em>',29:'Variables <em>bidimensionales</em>',30:'Regresión, correlación y <em>causalidad</em>',31:'Coeficientes y <em>predicción</em>',
32:'Probabilidad compuesta y <em>condicionada</em>',33:'Probabilidad total y <em>Bayes</em>',34:'Uniforme, binomial y <em>normal</em>',35:'Muestreo e <em>inferencia</em>',
36:'Emociones, error y <em>equipo</em>',37:'Inclusión e <em>historia</em> de las matemáticas',38:'Proyecto <em>integrador</em> y cierre',
}
NAMES = {
1:'Qué son las Matemáticas Generales',2:'Conteo: principios básicos',3:'Palomar e inclusión-exclusión',4:'Árboles y combinatoria',5:'Documentos numéricos cotidianos',
6:'Potencias, raíces y logaritmos',7:'Matrices: clasificación y operaciones',8:'Matrices en tablas y grafos',9:'Razones, proporciones y porcentajes',10:'Educación financiera',
11:'Probabilidad como medida',12:'Variación absoluta y media',13:'Límite: idea de cambio',14:'Derivada: concepto e interpretación',15:'Grafos: tipos y representación',
16:'Euler y grafos planos',17:'Eulerianos, hamiltonianos y coloración',18:'El problema del camino mínimo',19:'Patrones y generalización',20:'Funciones afines',
21:'Funciones cuadráticas',22:'Racionales, a trozos y periódicas',23:'Exponenciales y logarítmicas',24:'Sistemas de ecuaciones',25:'Inecuaciones y sistemas',
26:'Programación lineal',27:'Pensamiento computacional',28:'Estadística: interpretación',29:'Variables bidimensionales',30:'Regresión, correlación y causalidad',
31:'Coeficientes y predicción',32:'Probabilidad compuesta y condicionada',33:'Probabilidad total y Bayes',34:'Uniforme, binomial y normal',35:'Muestreo e inferencia',
36:'Emociones, error y equipo',37:'Inclusión e historia de las matemáticas',38:'Proyecto integrador y cierre',
}
STYLE = Path(__file__).with_name('style.css')
# inline
STYLE_TXT = r'''
.pasos{list-style:none;margin:0 0 1rem;padding:0;counter-reset:paso}
.pasos li{position:relative;margin:0 0 .7rem;padding:.7rem .8rem .7rem 3.1rem;background:var(--lv-panel);border:1px solid var(--lv-linea);border-radius:10px}
.pasos li::before{counter-increment:paso;content:counter(paso);position:absolute;left:.65rem;top:.7rem;width:1.7rem;height:1.7rem;border-radius:50%;background:#C4A15A;color:#1A160E;font-weight:700;font-size:.9rem;display:flex;align-items:center;justify-content:center}
.ej{margin:0 0 1rem;padding:.85rem .95rem;background:var(--lv-panel);border:1px solid var(--lv-linea);border-left:3px solid #C4A15A;border-radius:10px}
.ej h3{margin:0 0 .35rem;font-family:var(--lv-serif);font-size:1.05rem}
.editor,textarea.editor{width:100%;min-height:5rem;font-family:ui-monospace,monospace;font-size:.95rem;padding:.55rem .65rem;border:1px solid rgba(196,161,90,.45);border-radius:8px;background:#161512;color:#E6E1D6;resize:vertical}
.lienzo{display:block;width:100%;height:240px;background:#161512;border:1px solid #C4A15A;border-radius:8px;touch-action:none;cursor:crosshair}
.fila{display:flex;gap:.4rem;margin:.45rem 0;flex-wrap:wrap}
.boton{font:inherit;font-weight:700;font-size:.85rem;padding:.35rem .75rem;border-radius:999px;border:1px solid #C4A15A;background:transparent;color:#E6E1D6;cursor:pointer}
.porque{margin-top:.5rem;padding:.6rem .7rem;background:#1a2218;border-radius:8px}
.dato{font-size:.95rem;color:var(--lv-suave)}
.glosa{display:block;font-size:.9rem;color:#9A9488;margin:.15rem 0 .4rem}
.hub-lista{list-style:none;margin:0;padding:0;display:grid;gap:.4rem}
.hub-item{display:grid;grid-template-columns:2.5rem 1fr auto;gap:.65rem;padding:.65rem .85rem;background:var(--lv-panel);border:1px solid var(--lv-linea);border-radius:8px}
.hub-item a{color:inherit;text-decoration:none;display:contents}
.hub-num{color:#C4A15A;font-weight:700}
.hub-hero{margin:0 0 1.5rem;padding:1.4rem;background:var(--lv-panel);border:1px solid var(--lv-linea);border-left:3px solid #C4A15A;border-radius:10px}
'''
JS = r'''(function(){function liga(c){var ctx=c.getContext('2d');function fondo(){ctx.fillStyle='#161512';ctx.fillRect(0,0,c.width,c.height);ctx.strokeStyle='#C4A15A';ctx.strokeRect(.5,.5,c.width-1,c.height-1);}function fit(){var r=c.getBoundingClientRect();var w=Math.max(300,Math.floor(r.width));if(c.width!==w){c.width=w;c.height=240;fondo();}}var dib=false,last=null;function pos(ev){var r=c.getBoundingClientRect();var s=ev.touches?ev.touches[0]:ev;return{x:(s.clientX-r.left)*c.width/r.width,y:(s.clientY-r.top)*c.height/r.height};}c.addEventListener('pointerdown',function(ev){dib=true;last=pos(ev);ev.preventDefault();});c.addEventListener('pointermove',function(ev){if(!dib)return;var p=pos(ev);ctx.strokeStyle='#E6E1D6';ctx.lineWidth=2.2;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(last.x,last.y);ctx.lineTo(p.x,p.y);ctx.stroke();last=p;ev.preventDefault();});function up(){dib=false;}c.addEventListener('pointerup',up);c.addEventListener('pointerleave',up);var b=document.querySelector('[data-clear="'+c.id+'"]');if(b)b.addEventListener('click',fondo);fit();window.addEventListener('resize',fit);}document.querySelectorAll('canvas.lienzo').forEach(liga);})();'''

def href(n):
    return f'leccion-{n:02d}-{SLUGS[n-1]}.html'

def ej(num, t, e, p, eid):
    return (
        f'<article class="ej"><h3>{num}. {t}</h3><p>{e}</p>'
        f'<label for="{eid}">Tu resolución</label><textarea class="editor" id="{eid}"></textarea>'
        f'<details class="porque"><summary>Por qué</summary><p>{p}</p></details></article>'
    )

def comprueba(items):
    return '\n'.join(
        f'<details class="porque"><summary>{q}</summary><p>{a}</p></details>' for q, a in items
    )

def write(n, saber, objetivos, ct, c, expl, comps, rt, rp):
    nn = f'{n:02d}'
    titulo = TITLES[n]
    plain = titulo.replace('<em>', '').replace('</em>', '')
    objs = ''.join(f'<li>{o}</li>' for o in objetivos)
    prev_h = (
        '<span class="atajo atajo-prev is-disabled" aria-disabled="true">← Anterior</span>'
        if n == 1
        else f'<a class="atajo atajo-prev" href="{href(n-1)}">← Anterior</a>'
    )
    nxt = '../index.html' if n == 38 else href(n + 1)
    w = round(n / 38 * 100, 2)
    w = int(w) if w == int(w) else w
    maestro = {
        'curso': 'bach1-mates-gen',
        'leccion': n,
        'titulo': plain,
        'url': href(n),
        'musica': False,
        'pasos': [
            {'id': 'a', 'dicho': ct, 'hacer': 'Leer'},
            {'id': 'b', 'dicho': 'Practica en editores y lienzo.', 'hacer': 'Resolver'},
            {'id': 'c', 'dicho': 'Comprueba.', 'hacer': 'Cerrar'},
        ],
    }
    (LEC / f'maestro-{nn}.json').write_text(json.dumps(maestro, ensure_ascii=False, indent=2), encoding='utf-8')
    html = f'''<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#0E0E0C"/>
<title>Lección {nn} · {H.escape(plain)} · Les vencimos</title>
<link rel="icon" href="../icons/favicon.svg" type="image/svg+xml"/>
<link rel="manifest" href="../manifest.webmanifest"/>
<link rel="stylesheet" href="../leccion-shell.css"/>
<style>{STYLE_TXT}</style>
<script src="../leccion-shell-nav.js" defer></script>
</head>
<body class="leccion-shell" data-maestro-json="maestro-{nn}.json">
<div class="leccion-wrap">
<nav class="leccion-barra" aria-label="Navegación" data-actual="{n}" data-total="38">
<div class="leccion-progreso" role="status"><span class="progreso-texto"><strong>{n}</strong> de <strong>38</strong></span>
<div class="progreso-pista" aria-hidden="true"><div class="progreso-lleno" style="width:{w}%"></div></div></div>
<div class="leccion-atajos"><a class="atajo atajo-calc" href="../../../../modulos/calculadora.html">Calculadora</a>
{prev_h}<a class="atajo atajo-next" href="{nxt}">Siguiente →</a></div></nav>
<header class="leccion-top"><a class="leccion-marca" href="../../../../index.html">Les <span>vencimos</span></a>
<p class="leccion-meta-top">Matemáticas Generales · 1º Bachillerato</p></header>
<header class="bloque-titulo"><span class="eyebrow">Lección {nn} · {BLOQUES[n]}</span>
<h1 class="titulo-leccion">{titulo}</h1>
<p class="meta-leccion">CyL Decreto 40/2022 · {saber}</p></header>
<aside class="bloque-curiosidad"><p class="etiqueta-bloque">Para situarte</p>
<h2 class="titulo-curiosidad">{ct}</h2><p class="texto-curiosidad">{c}</p></aside>
<section class="bloque-cuerpo"><h2>Objetivos</h2><ul>{objs}</ul></section>
<section class="bloque-cuerpo">{expl}
<h2>Dibuja en esta página</h2>
<canvas id="lienzo{nn}" class="lienzo" width="900" height="240"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo{nn}">Borrar lienzo</button></div>
</section>
<section class="bloque-cuerpo"><h2>Comprueba</h2>{comprueba(comps)}</section>
<section class="bloque-reto"><span class="etiqueta-reto">Reto Profesor</span>
<h2 class="titulo-reto">{rt}</h2><p>{rp}</p>
<p class="reto-id">reto_id: bach1-mates-gen-L{nn}</p></section>
<footer class="leccion-pie"><strong>Les vencimos</strong> · L{nn}/38 · staging</footer>
</div>
<script type="application/json" data-maestro="guion">{json.dumps(maestro, ensure_ascii=False)}</script>
<script>{JS}</script>
</body></html>'''
    (LEC / href(n)).write_text(html, encoding='utf-8')
    print('OK', n, (LEC / href(n)).stat().st_size)

# Lessons 16-38
write(16, 'C.1 Fórmula de Euler',
['Aplicar V−E+F=2 en grafos planos conexos.', 'Contar vértices, aristas y caras.', 'Detectar si un dibujo es plano.'],
'La cuenta que no miente',
'Euler: en un grafo plano conexo V−E+F=2 (contando la cara infinita exterior).',
'<h2>Fórmula</h2><p>V−E+F=2. <span class="glosa">V=vértices · E=aristas · F=caras (incluida la exterior)</span></p>'
'<ol class="pasos"><li>Triángulo: V=3, E=3, F=2 → 3−3+2=2.</li></ol>'
+ ej(1, 'Cuadrado', 'V=4, E=4. ¿F? Comprueba Euler.', 'F=2 → 4−4+2=2.', 'e16a')
+ ej(2, 'Dos triángulos', 'Comparten una arista. Cuenta V, E, F.', 'Típico: V=4, E=5, F=3 → 4−5+3=2.', 'e16b')
+ ej(3, 'K5', '¿Es plano el K5 completo?', 'No. Euler solo aplica a dibujos planos.', 'e16c'),
[('Euler', 'V−E+F=2'), ('F incluye', 'cara exterior'), ('Triángulo F', '2')],
'Dibuja plano', 'Dibuja un grafo plano, conta V,E,F y escribe Euler en el editor.')

write(17, 'C.1 Eulerianos, hamiltonianos, coloración',
['Distinguir recorrido euleriano y ciclo hamiltoniano.', 'Usar grados para euleriano.', 'Colorear vértices.'],
'Recorrer sin repetir',
'Euleriano: todas las aristas. Hamiltoniano: todos los vértices. Coloración: adyacentes con distinto color.',
'<h2>Criterios</h2><p>Grafo conexo: hay ciclo euleriano si todos los grados son pares. Hamiltoniano no tiene criterio simple general.</p>'
+ ej(1, 'Ciclo', 'Todos grado 2. ¿Euleriano?', 'Sí.', 'e17a')
+ ej(2, 'C4', '¿Colores mínimos para C4?', '2.', 'e17b')
+ ej(3, 'Camino', 'Camino de 3 vértices: ¿ciclo hamiltoniano?', 'No. Sí hay camino hamiltoniano.', 'e17c'),
[('Euleriano mira', 'aristas'), ('Hamiltoniano mira', 'vértices'), ('Grado impar y ciclo euleriano', 'imposible')],
'Colorea', 'Dibuja un grafo y colorea vértices en el lienzo.')

write(18, 'C.1 Camino mínimo',
['Formular camino mínimo.', 'Resolver ejemplos pequeños.', 'Interpretar el peso.'],
'El atajo con peso',
'CyL: resolución del camino mínimo en distintos contextos.',
'<h2>Idea</h2><p>Cadena de aristas de menor suma de pesos.</p><ol class="pasos"><li>A–B 4, A–C 2, C–B 1 → A–C–B = 3 &lt; 4.</li></ol>'
+ ej(1, 'Elige', 'A–B=5, A–D=2, D–B=2. Mínimo A→B', '4 por A–D–B.', 'e18a')
+ ej(2, 'Unidades', 'Peso en minutos: el mínimo es…', 'el trayecto más rápido.', 'e18b')
+ ej(3, 'Dijkstra', 'Pesos en Dijkstra clásico', 'no negativos.', 'e18c'),
[('Optimiza', 'suma de pesos'), ('3 vs 4', 'elige 3'), ('Contextos', 'transporte, redes')],
'Mapa', 'Dibuja 5 nodos con pesos y marca el mínimo.')

write(19, 'D.1 Patrones',
['Detectar patrones.', 'Escribir la regla.', 'Comprobar con términos nuevos.'],
'De lo particular a la regla',
'CyL: generalización de patrones en situaciones sencillas.',
'<h2>Método</h2><p>Observa → conjetura → prueba → escribe a<sub>n</sub>.</p><ol class="pasos"><li>2,5,8,11… → a<sub>n</sub>=3n−1 (n≥1).</li></ol>'
+ ej(1, 'Sigue', '1,4,9,16… siguiente', '25 (cuadrados).', 'e19a')
+ ej(2, 'Regla', '3,6,12,24…', 'Se duplica: a_n=3·2^(n-1).', 'e19b')
+ ej(3, 'Visual', 'Explica un patrón de puntos en el borde de un cuadrado.', 'Por ejemplo 4(n−1) para n≥2; justifica.', 'e19c'),
[('Generalizar', 'pasar a regla'), ('Pares', '+2'), ('Comprobar', 'nuevo n')],
'Patrón', 'Dibuja un patrón y escribe a_n.')

write(20, 'D.2/D.4 Funciones afines',
['Reconocer y=mx+n.', 'Interpretar m y n.', 'Modelizar.'],
'La recta que modela', 'Funciones afines: modelización y propiedades.',
'<h2>Forma</h2><p>y=mx+n. <span class="glosa">m=pendiente · n=ordenada en origen</span></p>'
+ ej(1, 'Pendiente', 'y=2x−3 → m', '2', 'e20a')
+ ej(2, 'Taxi', '2 € + 1,2 €/km. Fórmula', 'y=1,2x+2', 'e20b')
+ ej(3, 'Paralelas', 'misma m', 'sí', 'e20c'),
[('n es', 'corte con y'), ('m=0', 'horizontal'), ('afín', 'recta')],
'Ajusta', 'Dibuja una recta y escribe m, n.')

write(21, 'D.2/D.4 Funciones cuadráticas',
['Identificar ax²+bx+c.', 'Vértice y apertura.', 'Modelizar.'],
'La parábola cotidiana', 'Cuadráticas: modelización y propiedades.',
'<h2>Claves</h2><p>a&gt;0 abre arriba. Vértice x=−b/(2a).</p>'
+ ej(1, 'Vértice', 'y=x²−4x+1 → x_v', '2', 'e21a')
+ ej(2, 'Raíces', 'x²−5x+6=0', '2 y 3', 'e21b')
+ ej(3, 'a&lt;0', 'máximo en el vértice', 'sí', 'e21c'),
[('Vértice x', '−b/(2a)'), ('a&gt;0', 'mínimo'), ('grado', '2')],
'Parábola', 'Bosqueja y=x²−4x marcando vértice.')

write(22, 'D.2/D.4 Racionales, a trozos, periódicas',
['Asíntotas simples.', 'Funciones a trozos.', 'Periodicidad.'],
'Tres formas flexibles', 'Racionales sencillas, a trozos y periódicas.',
'<h2>Piezas</h2><p>Racional = cociente. A trozos = por intervalos. Periódica: f(x+T)=f(x).</p>'
+ ej(1, '1/x', 'asíntota vertical', 'x=0', 'e22a')
+ ej(2, '|x|', 'definición a trozos', 'x si x≥0; −x si x&lt;0', 'e22b')
+ ej(3, 'seno', 'periodo', '2π', 'e22c'),
[('Periodo', 'f(x+T)=f(x)'), ('A trozos', 'varias fórmulas'), ('Ejemplo racional', '1/x')],
'Trozos', 'Define f a trozos y dibújala.')

write(23, 'D.2/D.4 Exponenciales y logarítmicas',
['Modelizar crecimiento.', 'Log como inversa.', 'Comparar modelos.'],
'Multiplicar en el tiempo', 'Exponenciales y logarítmicas.',
'<h2>Par</h2><p>y=a·b<sup>x</sup>. log_b inversa de b^x.</p>'
+ ej(1, 'Duplicar', 'Parte 5, ×2 cada año, año 3', '40', 'e23a')
+ ej(2, 'log', 'log2 8', '3', 'e23b')
+ ej(3, '0&lt;b&lt;1', 'la función', 'decrece', 'e23c'),
[('Inversa de exp', 'log'), ('b&gt;1', 'crece'), ('b=1', 'constante')],
'Serie', 'Escribe 3 términos ×1,05 y márcalos.')

write(24, 'D.3 Sistemas de ecuaciones',
['Resolver 2×2.', 'Interpretar rectas.', 'Modelizar.'],
'Dos condiciones a la vez', 'Sistemas de ecuaciones en contextos.',
'<h2>Ejemplo</h2><ol class="pasos"><li>x+y=10; x−y=2 → x=6, y=4.</li></ol>'
+ ej(1, 'Suma', 'x+y=5; 2x−y=4', 'x=3, y=2', 'e24a')
+ ej(2, 'Paralelas', 'y=2x+1; y=2x−3', 'sin solución', 'e24b')
+ ej(3, 'Coincidentes', 'infinitas soluciones si', 'son la misma recta', 'e24c'),
[('Secantes', '1 solución'), ('Paralelas', '0'), ('Coincidentes', 'infinitas')],
'Plantea', 'Traduce un enunciado a sistema 2×2.')

write(25, 'D.3 Inecuaciones y sistemas',
['Inecuaciones lineales.', 'Semiplanos.', 'Sistemas de desigualdades.'],
'Regiones que cumplen', 'Inecuaciones y sistemas de inecuaciones.',
'<h2>Idea</h2><p>x+2&gt;5 → x&gt;3. En el plano, y≤2x+1 es un semiplano.</p>'
+ ej(1, 'Lineal', '2x−4≤0', 'x≤2', 'e25a')
+ ej(2, 'Signo', 'Al ×(−1) la desigualdad', 'se invierte', 'e25b')
+ ej(3, 'Sistema', 'x≥0, y≥0, x+y≤1', 'triángulo en el 1er cuadrante', 'e25c'),
[('Semiplano', 'una desigualdad lineal'), ('Invertir', '× negativo'), ('x&gt;3', 'rayo abierto')],
'Región', 'Dibuja x≥0, y≥0, x+y≤4.')

write(26, 'D.2 Programación lineal',
['Función objetivo y restricciones.', 'Región factible.', 'Óptimo en vértices.'],
'Optimizar con restricciones', 'Programación lineal gráfica.',
'<h2>Método</h2><ol class="pasos"><li>Max z=3x+2y; x≥0,y≥0,x+y≤4.</li><li>Vértices (0,0),(4,0),(0,4) → z=0,12,8 → óptimo (4,0).</li></ol>'
+ ej(1, 'Objetivo', 'Qué se optimiza', 'la función z', 'e26a')
+ ej(2, 'Factible', 'cumple todas las restricciones', 'sí', 'e26b')
+ ej(3, 'Óptimo 2D', 'típicamente en', 'un vértice', 'e26c'),
[('PL', 'objetivo + restricciones'), ('Evaluar z en', 'vértices'), ('Gráfico', '2 variables')],
'PL', 'Inventa restricciones + z; dibuja y marca el óptimo.')

write(27, 'D.5 Pensamiento computacional',
['Descomponer.', 'Pseudocódigo.', 'Bucles y condiciones.'],
'Instrucciones claras', 'Algoritmos offline en el editor.',
'<h2>Algoritmo</h2><p>Entrada → proceso finito → salida. SI / MIENTRAS / PARA.</p>'
+ ej(1, 'Máximo', 'Idea', 'recorrer guardando el mayor', 'e27a')
+ ej(2, 'Bucle', 'qué hace', 'repite mientras valga la condición', 'e27b')
+ ej(3, 'Traza', 'x=1; mientras x&lt;4: x=x+1. Final', '4', 'e27c'),
[('Algoritmo', 'pasos finitos'), ('Pseudocódigo', 'intermedio'), ('Depurar', 'seguir valores')],
'Código', 'Algoritmo del máximo de 3 números en el editor.')

write(28, 'E.1 Interpretación estadística',
['Leer gráficos.', 'Media, mediana, moda.', 'Detectar sesgos.'],
'Datos con intención', 'Interpretación de información estadística.',
'<h2>Alertas</h2><p>Escala recortada, outliers, muestra opaca.</p>'
+ ej(1, 'Media', '2,4,6', '4', 'e28a')
+ ej(2, 'Mediana', '1,2,100', '2', 'e28b')
+ ej(3, 'Moda', '2,2,3,5', '2', 'e28c'),
[('Outlier afecta', 'más a la media'), ('Mediana', 'central'), ('Lee', 'ejes y fuente')],
'Critica', 'Describe un gráfico engañoso y su corrección.')

write(29, 'E.1 Variables bidimensionales',
['Tabla doble.', 'Marginales.', 'Dependencia.'],
'Dos variables a la vez', 'Conjunta, marginales, condicionadas.',
'<h2>Tabla</h2><p>Filas X, columnas Y. Marginal = suma de fila/columna.</p>'
+ ej(1, 'Marginal', 'suma de una fila', 'total de ese valor de X', 'e29a')
+ ej(2, 'Celda', 'frecuencia conjunta', 'P(X=x,Y=y) o conteo', 'e29b')
+ ej(3, 'Independencia', 'conjunta ≈ producto marginales', 'sí (idea)', 'e29c'),
[('Marginal', 'suma'), ('Condicionada', 'renorma'), ('Bidimensional', 'dos variables')],
'Encuesta', 'Tabla 2×2 inventada + marginales.')

write(30, 'E.1 Regresión y causalidad',
['Nube de puntos.', 'Correlación ≠ causalidad.', 'Valorar el ajuste.'],
'Nubes, rectas y trampas', 'Regresión lineal/cuadrática; causalidad.',
'<h2>Aviso</h2><p>Correlación no implica causalidad.</p>'
+ ej(1, 'Nube ↑', 'correlación', 'positiva', 'e30a')
+ ej(2, '¿Causalidad automática?', 'No', 'No', 'e30b')
+ ej(3, 'Nube curva + recta', 'puede ser mal ajuste', 'sí', 'e30c'),
[('Correlación', 'asociación'), ('Causalidad', 'causa-efecto'), ('Primero', 'el gráfico')],
'Nube', 'Dibuja 8 puntos y una recta a ojo.')

write(31, 'E.1 Coeficientes y predicción',
['Interpretar r.', 'Idea de R².', 'Predecir con cuidado.'],
'Cuánto de recta hay', 'r, R², predicción y fiabilidad.',
'<h2>r y R²</h2><p>r∈[−1,1]. R² alto: el modelo explica mucha varianza (idea).</p>'
+ ej(1, 'r≈0', 'poca relación lineal', 'sí', 'e31a')
+ ej(2, 'r=−0,9', 'fuerte inversa', 'sí', 'e31b')
+ ej(3, 'Extrapolación', 'fuera del rango', 'arriesgada', 'e31c'),
[('r=1', 'perfecto creciente'), ('R²', 'calidad de ajuste'), ('Fuera de rango', 'cuidado')],
'Predice', 'Con una recta inventada, predice y limita el engaño.')

write(32, 'E.2 Probabilidad condicionada',
['P(A|B).', 'Árboles y contingencia.', 'Independencia.'],
'Si ya pasó B…', 'Condicionada, independencia, árboles, contingencia.',
'<h2>Fórmula</h2><p>P(A|B)=P(A∩B)/P(B) si P(B)&gt;0.</p>'
+ ej(1, 'Dado', 'P(6|par)', '1/3', 'e32a')
+ ej(2, 'Independencia', 'P(A∩B)=P(A)P(B)', 'sí', 'e32b')
+ ej(3, 'Árbol', 'en una rama', 'se multiplican las P', 'e32c'),
[('Condicionada', 'renorma'), ('Árbol', 'ramas'), ('Tabla', 'contingencia')],
'Árbol', 'Dibuja un árbol de 2 etapas.')

write(33, 'E.2 Probabilidad total y Bayes',
['Probabilidad total.', 'Bayes.', 'Falsos positivos (idea).'],
'Actualizar creencias', 'Total y Bayes (CyL).',
'<h2>Bayes</h2><p>P(A|B)=P(B|A)P(A)/P(B); P(B) a menudo por total.</p>'
+ ej(1, 'Total', 'con partición Bi', 'P(A)=Σ P(A|Bi)P(Bi)', 'e33a')
+ ej(2, 'Bayes', 'invierte el condicionamiento', 'sí', 'e33b')
+ ej(3, 'A priori', 'importa P(A)', 'sí', 'e33c'),
[('Bayes', 'P(A|B) vía P(B|A)'), ('Total', 'desglosa'), ('Árbol', 'ayuda')],
'Bayes', 'Calcula un test con prevalencia baja paso a paso.')

write(34, 'E.3 Uniforme, binomial, normal',
['Uniforme.', 'Binomial sencilla.', 'Normal (idea).'],
'Tres familias', 'Uniforme, binomial y normal en casos sencillos.',
'<h2>Fichas</h2><p>Uniforme: misma probabilidad/densidad. Binomial: éxitos en n ensayos. Normal: campana.</p>'
+ ej(1, 'Dado', 'uniforme en 1..6', 'sí', 'e34a')
+ ej(2, 'Binom', 'n=3,p=1/2, P(3)', '1/8', 'e34b')
+ ej(3, 'Normal', 'parámetros típicos', 'media y desviación', 'e34c'),
[('Binomial', 'cuenta éxitos'), ('Uniforme [0,1]', 'densidad 1'), ('Normal', 'continua')],
'Elige', 'Justifica qué familia encaja en un enunciado tuyo.')

write(35, 'E.4 Muestreo e inferencia',
['Población vs muestra.', 'Muestreo simple.', 'Representatividad.'],
'De la parte al todo', 'Muestreo, validez, diseño.',
'<h2>Claves</h2><p>Muestra representativa; el sesgo no se arregla solo con más tamaño.</p>'
+ ej(1, 'Aleatorio', 'igual probabilidad', 'sí', 'e35a')
+ ej(2, 'Voluntarios web', 'sesgo', 'alto riesgo', 'e35b')
+ ej(3, 'Inferencia', 'generalizar con incertidumbre', 'sí', 'e35c'),
[('Población', 'total'), ('Muestra', 'subconjunto'), ('Representativa', 'refleja')],
'Diseña', 'Mini-estudio: pregunta, población, muestreo.')

write(36, 'F.1/F.2 Emociones, error, equipo',
['Nombrar emociones.', 'Error como pista.', 'Roles de equipo.'],
'Mates con sistema nervioso', 'Autoconciencia, error, equipo.',
'<h2>Protocolo</h2><ol class="pasos"><li>Para 60 s.</li><li>Escribe qué no entiendes.</li><li>Ejemplo mínimo.</li><li>Pide ayuda concreta.</li></ol>'
+ ej(1, 'Error', '0,5 vs 50 %', 'aclara la base (1 vs 100)', 'e36a')
+ ej(2, 'Rol', 'uno útil', 'reloj / escriba / escéptico', 'e36b')
+ ej(3, 'Decisión', 'cómo', 'pros/contras matemáticos', 'e36c'),
[('Error', 'dato'), ('Ayuda', 'específica'), ('Equipo', 'diverso')],
'Contrato', 'Tu protocolo de bloqueo en el editor.')

write(37, 'F.3 Inclusión e historia',
['Pregunta clara.', 'Aportación histórica.', 'Respeto en el aula.'],
'Personas detrás de las ideas', 'Comunicación; historia de las matemáticas.',
'<h2>Ejemplos</h2><p>Al-Juarismi (álgebra); Euler (grafos); Bayes (condicionada). Sin inventar fechas dudosas.</p>'
+ ej(1, 'Pregunta', 'forma buena', '«¿En qué paso…?»', 'e37a')
+ ej(2, 'Escucha', 'técnica', 'parafrasear', 'e37b')
+ ej(3, 'Euler', 'aporte', 'caminos / grafos', 'e37c'),
[('Inclusión', 'participación'), ('Historia', 'contexto'), ('Pregunta', 'concreta')],
'Bio', '5 líneas verificables sobre una figura; esquema en el lienzo.')

write(38, 'A–F Proyecto integrador',
['Problema real con ≥2 sentidos.', 'Documentar límites.', 'Conclusión clara.'],
'Todo el curso en un problema', 'Proyecto + portfolio de cierre.',
'<h2>Encargo</h2><p>Tema real (transporte, tarifa, deporte…). Mínimo dos bloques A–E y reflexión F.</p>'
'<label for="port38">Portfolio</label>'
'<textarea class="editor" id="port38" style="min-height:12rem" placeholder="Título · datos · modelo · cálculos · límites · error…"></textarea>'
+ ej(1, 'Checklist', '¿Datos + modelo + límite?', 'Escríbelos explícitos.', 'e38a')
+ ej(2, 'Sentidos', 'lista bloques', 'mínimo 2 + F', 'e38b')
+ ej(3, 'Cierre', '3 frases para no matemático', 'sí', 'e38c'),
[('Proyecto', 'problema acotado'), ('Límites', 'qué no afirma'), ('Portfolio', 'evidencia')],
'Cierra', 'Completa el portfolio y dibuja el esquema del modelo.')

# Hub
items = []
for i in range(1, 39):
    items.append(
        f'<li class="hub-item hub-disponible"><a href="lecciones/{href(i)}">'
        f'<span class="hub-num">{i:02d}</span><span>{NAMES[i]}</span><span>OK</span></a></li>'
    )
index = f'''<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#0E0E0C"/>
<title>Matemáticas Generales · 1º Bach · Les vencimos</title>
<link rel="stylesheet" href="leccion-shell.css"/>
<link rel="icon" href="icons/favicon.svg" type="image/svg+xml"/>
<link rel="manifest" href="manifest.webmanifest"/>
<style>{STYLE_TXT}</style>
</head>
<body class="leccion-shell"><div class="leccion-wrap">
<header class="leccion-top"><a class="leccion-marca" href="../../index.html">Les <span>vencimos</span></a>
<p class="leccion-meta-top">Staging · no publicado</p></header>
<div class="hub-hero">
<h1 style="font-family:var(--lv-serif);margin:0 0 .5rem;color:var(--lv-titulo)">Matemáticas Generales · 1º Bachillerato</h1>
<p class="dato">Modalidad General · CyL Decreto 40/2022 · 38 lecciones · carbón+ámbar · file://</p>
<p><a style="display:inline-block;padding:.6rem 1rem;background:#C4A15A;color:#1A160E;border-radius:8px;text-decoration:none;font-weight:700" href="lecciones/{href(1)}">Empezar L01 →</a></p>
</div>
<ul class="hub-lista">{''.join(items)}</ul>
<footer class="leccion-pie">Les vencimos · staging/bach1/mates-gen · sin publicar</footer>
</div></body></html>'''
(ROOT / 'index.html').write_text(index, encoding='utf-8')

files = sorted(LEC.glob('leccion-*.html'))
h = hashlib.md5()
for f in files:
    h.update(f.name.encode())
    h.update(f.read_bytes())
print('TOTAL', len(files))
print('MD5', h.hexdigest())
(ROOT / 'PROGRESS.md').write_text(
    f'# Progreso mates-gen\n\nLecciones: {len(files)}/38\nMD5 (nombre+contenido ordenado): `{h.hexdigest()}`\nPath: `/workspace/lesvencimos/staging/bach1/mates-gen/`\n',
    encoding='utf-8',
)
(ROOT / 'CIERRE.md').write_text(
    f'# Cierre staging Matemáticas Generales\n\n'
    f'- Path: `/workspace/lesvencimos/staging/bach1/mates-gen/`\n'
    f'- Lecciones: {len(files)}/38\n'
    f'- MD5 pack lecciones: `{h.hexdigest()}`\n'
    f'- ESQUEMA.md MD5: `{hashlib.md5((ROOT/"ESQUEMA.md").read_bytes()).hexdigest()}`\n'
    f'- NO publicado. Cadena: Revisor Bach → Web LV.\n',
    encoding='utf-8',
)
