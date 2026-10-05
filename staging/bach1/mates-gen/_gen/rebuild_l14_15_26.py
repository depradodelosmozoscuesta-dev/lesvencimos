# -*- coding: utf-8 -*-
"""L15–L26 al listón L14. No toca L01–L04 ni L14 (el lab L14 es un hermano aparte)."""
import math, sys
sys.path.insert(0, '/workspace/lesvencimos/staging/bach1/mates-gen/_gen')
from rebuild_l14_common import *

SNAP = snapshot()

# ---------- L15 ----------
write_lab(15, 'Grados de un grafo dirigido', '''
<div class="panel">
<p>Grafo dirigido del ejemplo: arcos A→B, B→C, C→A y A→C. Pulsa para ver grados de salida y de entrada.</p>
<button id="go" type="button">Calcular grados</button>
<div class="out" id="out"></div>
<canvas id="c" width="640" height="220"></canvas>
</div>
<script>
function dib(){
  var cv=document.getElementById('c'), ctx=cv.getContext('2d');
  ctx.fillStyle='#12100e'; ctx.fillRect(0,0,640,220);
  var P={A:[120,110],B:[320,40],C:[320,180]};
  var E=[['A','B'],['B','C'],['C','A'],['A','C']];
  ctx.strokeStyle='#C4A15A'; ctx.lineWidth=2;
  E.forEach(function(e){var a=P[e[0]], b=P[e[1]]; ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]); ctx.stroke();});
  ctx.fillStyle='#E6E1D6'; ctx.font='16px sans-serif';
  Object.keys(P).forEach(function(k){ctx.beginPath(); ctx.arc(P[k][0],P[k][1],16,0,6.3); ctx.fillStyle='#1C1A16'; ctx.fill(); ctx.stroke(); ctx.fillStyle='#E6E1D6'; ctx.fillText(k,P[k][0]-5,P[k][1]+5);});
}
document.getElementById('go').onclick=function(){
  document.getElementById('out').textContent='Salida: A=2, B=1, C=1. Entrada: A=1, B=1, C=2. En un dirigido no coinciden.';
};
dib();
</script>
''')

fig15 = '''
<line x1="120" y1="150" x2="300" y2="60" stroke="#C4A15A" stroke-width="2.5"/>
<line x1="300" y1="60" x2="300" y2="230" stroke="#C4A15A" stroke-width="2.5"/>
<line x1="300" y1="230" x2="120" y2="150" stroke="#C4A15A" stroke-width="2.5"/>
<line x1="120" y1="150" x2="300" y2="230" stroke="#8F9A72" stroke-width="2"/>
<polygon points="292,68 278,52 286,78" fill="#C4A15A"/>
<polygon points="308,210 292,198 312,190" fill="#C4A15A"/>
<polygon points="140,158 128,140 150,142" fill="#C4A15A"/>
<polygon points="270,214 250,200 258,222" fill="#8F9A72"/>
<circle cx="120" cy="150" r="16" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="300" cy="60" r="16" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="300" cy="230" r="16" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<text x="120" y="155" text-anchor="middle" fill="#E6E1D6">A</text>
<text x="300" y="65" text-anchor="middle" fill="#E6E1D6">B</text>
<text x="300" y="235" text-anchor="middle" fill="#E6E1D6">C</text>
<text x="40" y="28" fill="#C4A15A" font-size="14">dirigido: A→B, B→C, C→A y A→C</text>
<line x1="460" y1="40" x2="560" y2="110" stroke="#C4A15A" stroke-width="2"/>
<line x1="560" y1="110" x2="640" y2="40" stroke="#C4A15A" stroke-width="2"/>
<line x1="560" y1="110" x2="560" y2="210" stroke="#C4A15A" stroke-width="2"/>
<circle cx="460" cy="40" r="14" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="560" cy="110" r="14" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="640" cy="40" r="14" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="560" cy="210" r="14" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<text x="430" y="250" fill="#9A9488" font-size="14">árbol: 4 vértices, 3 aristas, sin ciclo</text>
'''
build(
15, 'Grafos: tipos y <em>representación</em>', 'C.1 Grafos dirigidos, planos, ponderados y árboles',
'Flechas que no se pueden dar la vuelta',
'CyL distingue grafos dirigidos, planos, ponderados y árboles. A la izquierda, el ejemplo dirigido: arcos A→B, B→C, C→A y A→C. A la derecha, un árbol de cuatro vértices, sin ciclo y con una arista menos que vértices.',
['Leer un grafo dirigido y separar grado de salida y de entrada.','Reconocer un árbol: conexo, sin ciclos, E = V − 1.','Decir qué añade un peso o una flecha respecto de un grafo simple.'],
'''<h2>El mismo dibujo no significa siempre lo mismo</h2>
<p>Un grafo es un conjunto de vértices y un conjunto de relaciones entre ellos. Si la relación tiene dirección, hablamos de grafo dirigido y dibujamos flechas: el arco A→B no es el arco B→A. Si la relación no tiene dirección, una sola arista vale para los dos extremos.</p>
<p><span class="glosa">grado de salida = flechas que salen · grado de entrada = flechas que llegan · árbol = grafo conexo y sin ciclos · en un árbol E = V − 1 · ponderado = cada arista lleva un número (distancia, tiempo, coste) · plano = se puede dibujar sin cruces; el cruce de dos trazos no es un vértice</span></p>
<p>En el ejemplo de la izquierda hay 3 vértices y 4 arcos. De A salen dos flechas (a B y a C), así que su grado de salida es 2. A C llegan dos (desde B y desde A), grado de entrada 2. Esa cuenta no se puede hacer en el árbol de la derecha, porque allí no hay flechas: cada arista suma 1 al grado de sus dos extremos y no hay «salida» distinta de la «entrada».</p>
<p>El árbol tiene V = 4 y E = 3. Es conexo (se puede ir de cualquier vértice a cualquier otro) y no contiene un ciclo: si quitas una arista, dejas de poder conectar los dos lados. Un ciclo, como el triángulo A→B→C→A de la izquierda, es justo lo que un árbol prohíbe.</p>
<table class="datos"><thead><tr><th></th><th>Grafo dirigido del ejemplo</th><th>Árbol de la derecha</th></tr></thead>
<tbody>
<tr><td>Vértices</td><td>3 (A, B, C)</td><td>4</td></tr>
<tr><td>Aristas o arcos</td><td>4 arcos</td><td>3 aristas</td></tr>
<tr><td>¿Ciclo?</td><td>sí, A-B-C-A</td><td>no</td></tr>
<tr><td>Relación E y V</td><td>E = 4, V − 1 = 2</td><td>E = V − 1</td></tr>
</tbody></table>''',
'Grafo dirigido A→B, B→C, C→A, A→C junto a un árbol de 4 vértices y 3 aristas', fig15,
[
('Grados con flecha',
 'En el grafo dirigido del gráfico, calcula el grado de salida y el de entrada de A, B y C.',
 [
  ('Arcos: A→B, B→C, C→A y A→C. Léelos en las flechas, no inventes B→A.',
   'Glosa: la flecha verde A→C es un arco más, no la misma relación que C→A.'),
  ('Salida: A manda a B y a C (2); B solo a C (1); C solo a A (1).',
   'Glosa: el grado de salida cuenta arcos cuyo origen es ese vértice.'),
  ('Entrada: a A solo llega C (1); a B solo llega A (1); a C llegan B y A (2).',
   'Glosa: entrada y salida no tienen por qué coincidir. En A, 2 de salida y 1 de entrada.'),
  ('Comprueba la suma: salidas 2+1+1 = 4 y entradas 1+1+2 = 4. Las dos sumas valen el número de arcos.',
   'Glosa: cada arco aporta 1 a una salida y 1 a una entrada. Si no cuadra, falta una flecha.'),
 ]),
('El árbol no es un detalle',
 'Comprueba que la figura de la derecha es un árbol y que le sobra o le falta algo si añades una arista entre las dos hojas superiores.',
 [
  ('V = 4, E = 3 y E = V − 1. Está conectado: desde el vértice central se llega a los otros tres.',
   'Glosa: E = V − 1 es necesario en un grafo conexo, y junto con la conexión evita ciclos.'),
  ('No hay ciclo: no puedes volver al punto de partida sin repetir una arista.',
   'Glosa: un ciclo necesitaría al menos tres vértices unidos en redondo, y aquí no se cierra.'),
  ('Si unes las dos hojas de arriba, añades una arista: E = 4 y V − 1 = 3. Aparece un triángulo y deja de ser árbol.',
   'Glosa: esa arista de más crea exactamente un ciclo y rompe la igualdad E = V − 1.'),
  ('Sigue siendo conexo, pero ya no es árbol. Conexo y árbol no son sinónimos.',
   'Glosa: el ciclo dirigido de la izquierda también es conexo en su sentido, y tampoco es un árbol.'),
 ]),
('Qué falta para otros tipos',
 'Di qué habría que añadir al árbol para que fuera ponderado y qué habría que exigir para llamarlo plano. ¿El dirigido de la izquierda es plano?',
 [
  ('Ponderado: un número en cada arista (por ejemplo minutos). El dibujo actual no trae números, luego no está ponderado.',
   'Glosa: el peso no es el grado. El grado se calcula; el peso se declara.'),
  ('Plano: que exista un dibujo sin cruces. El árbol de la derecha ya está dibujado sin cruces, así que es plano.',
   'Glosa: plano no significa «dibujado en horizontal»; significa «sin cruces forzados».'),
  ('El dirigido también está dibujado sin que las flechas se crucen en un punto que no sea vértice. Es plano.',
   'Glosa: que A→C y el lado B-C se toquen en C no es un cruce: C es un vértice.'),
  ('Un cruce de verdad aparecería si dos arcos se cortaran por el medio y ese corte no fuera un vértice del grafo. Aquí no ocurre.',
   'Glosa: en la lección siguiente un grafo no plano no se puede salvar cambiando el dibujo.'),
 ]),
],
[
(1, 'Suma de arcos',
 'Un dirigido tiene suma de grados de salida 7. ¿Cuántos arcos tiene? ¿Cuánto suma la entrada?',
 'Cada arco cuenta una vez en la salida de su origen, así que hay 7 arcos. La suma de los grados de entrada también es 7, porque ese mismo arco cuenta una vez en el destino. El paso es no dividir entre 2: esa división era del grafo no dirigido, donde cada arista suma a dos grados indistintos. Aquí entrada y salida ya separan los dos papeles, y cada suma, por sí sola, vale E. Si te dieran solo grados sin decir si son de salida, no podrías aplicar esta lectura.',
 'e15a'),
(2, '¿Árbol?',
 'V = 6 y E = 5, conexo y sin ciclos. ¿Es un árbol? ¿Y si te dicen que tiene un ciclo?',
 'E = V − 1 = 5 y, además, conexo y sin ciclos: es un árbol. Las tres condiciones van juntas en la definición que usamos; la igualdad E = V − 1 en un grafo conexo ya impide el ciclo. Si te dicen que tiene un ciclo, entonces no es árbol, y además no puede cumplir a la vez ser conexo y E = V − 1: un ciclo obliga a tener al menos una arista de más. El paso es no quedarte solo con el dibujo «parece un árbol» si el enunciado trae un ciclo.',
 'e15b'),
(3, 'Flecha inversa',
 'En el ejemplo, ¿está el arco B→A? ¿Qué grado de salida de B cambiaría si lo añadieras?',
 'No está: la flecha entre A y B apunta a B, no a A. Añadir B→A sería un arco nuevo. El grado de salida de B pasaría de 1 a 2, y el de entrada de A pasaría de 1 a 2. El paso es mirar la punta de la flecha, no el segmento. En un no dirigido esa pregunta no existiría: una sola arista AB serviría para los dos. Por eso el dirigido de la izquierda y un triángulo sin flechas no guardan la misma información aunque el «dibujo de líneas» se parezca.',
 'e15c'),
],
[
('¿Cuántos arcos salen de A en el gráfico?',
 'Dos: A→B y A→C. Por qué: se ven dos flechas con origen en A. El arco C→A llega a A, así que cuenta como entrada, no como salida. Mezclarlas daría grado 3 y la suma de salidas dejaría de valer 4.'),
('¿Por qué el de la derecha es un árbol?',
 'Porque es conexo, no tiene ciclos y E = V − 1 (3 = 4 − 1). Por qué: con esas condiciones no sobra ni falta ninguna arista para unir los vértices. Si faltara una, quedaría desconectado; si sobrara una, aparecería un ciclo.'),
('¿Un grafo ponderado es lo mismo que un grafo con grados?',
 'No. Por qué: el peso es un dato escrito en la arista (distancia, coste). El grado es un recuento de aristas incidentes. El árbol del gráfico tiene grados pero no tiene pesos: no es ponderado hasta que alguien asigne números a las aristas.'),
],
'Un mapa con flechas',
'Dibuja en el lienzo tres lugares de tu barrio y flechas de «puedo ir andando en ese sentido». Anota grados de salida.',
['Izquierda: cuatro flechas A→B, B→C, C→A y A→C. Derecha: árbol de 4 vértices y 3 aristas.',
 'La salida de A es 2 y su entrada es 1. No son el mismo número.',
 'Ejemplo 1: las sumas de salidas y de entradas valen 4, el número de arcos.',
 'Ejemplo 2: si cierras las dos hojas del árbol, dejas de tener E = V − 1.',
 'Ejemplo 3: sin números en las aristas no hay ponderación; sin cruces, lo dibujado es plano.',
 'En el laboratorio contrasta entrada y salida.',
 'No des la vuelta a una flecha si el arco no existe.']
, lab_title='Grados de un grafo dirigido')

print('L15 ok parcial')

# ---------- L16 K5 ----------
_verts = []
for _k in range(5):
    _a = -math.pi/2 + _k*2*math.pi/5
    _verts.append((210+120*math.cos(_a), 168+120*math.sin(_a)))
fig16 = ''
for _i in range(5):
    for _j in range(_i+1, 5):
        x1,y1=_verts[_i]; x2,y2=_verts[_j]
        fig16 += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#C4A15A" stroke-width="1.7"/>'
for _i,(x,y) in enumerate(_verts):
    fig16 += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>'
    fig16 += f'<text x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle" fill="#E6E1D6" font-size="14">{_i+1}</text>'
fig16 += '''
<text x="400" y="70" fill="#E6E1D6" font-size="16">K5: V = 5, E = 10</text>
<text x="400" y="110" fill="#C4A15A" font-size="16">3V − 6 = 9</text>
<text x="400" y="150" fill="#E6E1D6" font-size="16">10 &gt; 9</text>
<text x="400" y="200" fill="#9A9488" font-size="14">Si fuera plano, E ≤ 3V − 6.</text>
<text x="400" y="224" fill="#9A9488" font-size="14">Como 10 &gt; 9, K5 no es plano.</text>
'''
build(
16, 'Euler y grafos <em>planos</em>', 'C.1 Fórmula de Euler y grafos planos',
'Diez aristas donde solo cabían nueve',
'Un grafo plano y conexo cumple V − E + F = 2, contando la cara exterior. De ahí sale, para un grafo simple con V ≥ 3, la cota E ≤ 3V − 6. K5 tiene V = 5 y E = 10, y 10 > 9 = 3·5 − 6, así que no es plano.',
['Contar V, E y F en un grafo plano pequeño y contrastar Euler.','Aplicar la cota E ≤ 3V − 6.','Concluir que K5 no es plano porque 10 > 9.'],
'''<h2>Planar no es «me ha salido un cruce»: es que todo dibujo se cruza</h2>
<p>Un grafo es plano si existe algún dibujo en el papel en el que las aristas solo se encuentren en los vértices. Que un dibujo concreto tenga un cruce no demuestra que el grafo sea no plano: a lo mejor otro dibujo lo evita. Hace falta un argumento que valga para todos los dibujos.</p>
<p><span class="glosa">V = vértices · E = aristas · F = caras, incluida la cara infinita de fuera · K5 = cinco vértices, todos unidos con todos · 3V − 6 = cota superior de aristas de un grafo simple, conexo y plano con V ≥ 3</span></p>
<p>En un grafo simple plano cada cara queda limitada por al menos 3 aristas y cada arista separa a lo sumo 2 caras, así que 2E ≥ 3F. Con Euler, V − E + F = 2, se despeja F = E − V + 2 y al sustituir sale E ≤ 3V − 6. Es una condición necesaria: si un grafo simple tiene más aristas, no puede ser plano.</p>
<p>K5, dibujado al lado, une cada pareja de entre 5 vértices. El número de aristas es C(5, 2) = 10. La cota permite como mucho 3·5 − 6 = 9. Como 10 > 9, ningún reordenado de los vértices eliminará todos los cruces. El dibujo enseña uno de esos cruces inevitables; la desigualdad demuestra que no es un descuido.</p>
<table class="datos"><thead><tr><th>Grafo</th><th>V</th><th>E</th><th>3V − 6</th><th>¿Puede ser plano?</th></tr></thead>
<tbody>
<tr><td>Triángulo</td><td>3</td><td>3</td><td>3</td><td>sí, 3 ≤ 3, y se dibuja sin cruces</td></tr>
<tr><td>K5</td><td>5</td><td>10</td><td>9</td><td>no, porque 10 > 9</td></tr>
</tbody></table>''',
'K5 con 5 vértices y las 10 aristas; la desigualdad 10 > 9', fig16,
[
('Contar K5',
 'Cuenta vértices y aristas de K5 y comprueba que las aristas son todas las parejas.',
 [
  ('Hay 5 vértices, uno por cada círculo numerado del gráfico.',
   'Glosa: V = 5 es el primer dato de la cota; no cuentes un cruce como vértice.'),
  ('Cada vértice se une a los otros 4, pero así contarías cada arista dos veces: (5·4)/2 = 10.',
   'Glosa: la división entre 2 es el mismo doble conteo de siempre. C(5, 2) = 10.'),
  ('También puedes enumerar: desde 1 salen 4 aristas nuevas, desde 2 salen 3 que no repiten la anterior, luego 2 y luego 1. Suma 4+3+2+1 = 10.',
   'Glosa: ese recuento ordenado evita contar dos veces la arista 1-2.'),
  ('E = 10 y V = 5. Esos son los números que entran en la desigualdad, no el número de cruces que veas en este dibujo.',
   'Glosa: los cruces dependen del dibujo; V y E, no.'),
 ]),
('La cota que no cumple',
 'Aplica E ≤ 3V − 6 a K5 y redacta la contradicción con la planaridad.',
 [
  ('Sustituye V = 5: 3·5 − 6 = 15 − 6 = 9. Un grafo simple plano con 5 vértices tiene como mucho 9 aristas.',
   'Glosa: la cota no dice que 9 aristas garanticen que es plano; dice que más de 9 lo impiden.'),
  ('K5 tiene 10 aristas. Compara: 10 > 9.',
   'Glosa: el exceso es una sola arista, y con eso basta para la contradicción.'),
  ('Si K5 fuera plano, cumpliría la cota. No la cumple. Luego no es plano.',
   'Glosa: es una prueba por contradicción, no una impresión sobre este dibujo concreto.'),
  ('Por tanto no existe ningún dibujo de K5 sin cruces. Mover los círculos puede cambiar qué aristas se cruzan, no el hecho de que alguna se cruce.',
   'Glosa: por eso el SVG puede enseñar un cruce y la desigualdad cierra el argumento.'),
 ]),
('Euler en un plano que sí lo es',
 'Un triángulo tiene V = 3, E = 3 y dos caras (interior y exterior). Comprueba V − E + F = 2 y la cota.',
 [
  ('F = 2: la región de dentro del triángulo y la región infinita de fuera.',
   'Glosa: olvidar la cara exterior es el error típico; sin ella, 3 − 3 + 1 = 1, que no es 2.'),
  ('V − E + F = 3 − 3 + 2 = 2. Euler se cumple.',
   'Glosa: el 2 es de un grafo conexo plano, contando la cara de fuera.'),
  ('Cota: 3V − 6 = 3. Y E = 3, así que 3 ≤ 3. La cota no prohíbe este grafo.',
   'Glosa: estar en la frontera de la cota es compatible con ser plano, y el triángulo lo es.'),
  ('Contraste: el triángulo satura la cota y es plano; K5 se pasa en una arista y no lo es.',
   'Glosa: la misma fórmula, dos conclusiones distintas según los números.'),
 ]),
],
[
(1, 'Un cruce no basta',
 'Dibujas un cuadrado con las dos diagonales y las diagonales se cruzan en el papel. ¿Has demostrado que ese grafo no es plano?',
 'No. Has demostrado que ese dibujo tiene un cruce, no que todos los dibujos lo tengan. El paso que falta es intentar otro dibujo: saca un vértice fuera y traza una diagonal por el exterior; el grafo del cuadrado con diagonales (K4) sí es plano. V = 4, E = 6 y 3V − 6 = 6, así que la cota no lo prohíbe. Con K5 la cota sí prohíbe cualquier intento: 10 > 9. No confundas «este dibujo se cruza» con «el grafo no es plano».',
 'e16a'),
(2, 'Cara exterior',
 'En el triángulo, alguien dice F = 1 porque «solo se ve un hueco». ¿Qué le hace Euler?',
 'Le descuadra la fórmula: 3 − 3 + 1 = 1, que no es 2. El hueco interior es una cara y el resto del plano es otra. El paso es contar la cara no acotada. Cuando se añade, F = 2 y 3 − 3 + 2 = 2. Este cuidado importa antes de usar 2E ≥ 3F para llegar a la cota, porque F entra en la demostración. En K5 ni siquiera llegamos a contar caras de un dibujo plano, porque ese dibujo no existe.',
 'e16b'),
(3, 'Otra cota numérica',
 'Un grafo simple tiene V = 6. ¿Cuántas aristas puede tener, como máximo, si es plano? ¿Puede ser K6?',
 '3V − 6 = 18 − 6 = 12. Si es plano y simple, E ≤ 12. K6 une todas las parejas: C(6, 2) = 15, y 15 > 12, luego K6 tampoco es plano. El paso es calcular la cota antes de discutir el dibujo. K5 ya no lo era con 10 > 9; K6 se pasa todavía más. Que la cota falle prueba que no es plano. Que la cota se cumpla, en cambio, no prueba que lo sea: es necesaria, no suficiente.',
 'e16c'),
],
[
('¿Cuántas aristas tiene K5 y cuántas le permitiría ser plano?',
 'Tiene 10 y la cota permite como mucho 9. Por qué: C(5, 2) = 10 y 3·5 − 6 = 9. La comparación 10 > 9 es la prueba. No hace falta contar los cruces del dibujo para concluir.'),
('¿Por qué no contamos el cruce del dibujo como un sexto vértice?',
 'Porque no es un vértice del grafo: es un accidente del dibujo. Por qué: K5 tiene solo los cinco vértices que elegimos, todos unidos entre sí. Si convirtieras el cruce en vértice estarías mirando otro grafo, con más vértices y aristas partidas.'),
('En el triángulo, ¿cuánto da V − E + F?',
 'Da 2: 3 − 3 + 2. Por qué: hay que contar la cara exterior. Sin ella la fórmula no cierra y tampoco se sostiene la deducción de E ≤ 3V − 6, que parte de Euler.'),
],
'Dibuja y contradice',
'Dibuja K5 en el lienzo intentando evitar cruces. Escribe al lado V = 5, E = 10, 3V − 6 = 9 y la frase «10 > 9, no es plano».',
['El SVG es K5: cinco círculos y las diez aristas, con la cuenta 10 > 9 al lado.',
 'Los cruces del dibujo ilustran; la prueba es la cota.',
 'Ejemplo 1: (5·4)/2 = 10 aristas.',
 'Ejemplo 2: si fuera plano, E ≤ 9. No lo es.',
 'Ejemplo 3: el triángulo sí cumple Euler, 3 − 3 + 2 = 2, y satura la cota con E = 3.',
 'No declares no plano un grafo solo porque tu primer dibujo se cruce.',
 'K5 queda fuera por una arista de más sobre la cota.']
)

# ---------- L17 ----------
fig17 = '''
<line x1="80" y1="60" x2="230" y2="60" stroke="#C4A15A" stroke-width="3"/>
<line x1="230" y1="60" x2="230" y2="210" stroke="#C4A15A" stroke-width="3"/>
<line x1="230" y1="210" x2="80" y2="210" stroke="#C4A15A" stroke-width="3"/>
<line x1="80" y1="210" x2="80" y2="60" stroke="#C4A15A" stroke-width="3"/>
<circle cx="80" cy="60" r="16" fill="#C4A15A" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="230" cy="60" r="16" fill="#8F9A72" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="230" cy="210" r="16" fill="#C4A15A" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="80" cy="210" r="16" fill="#8F9A72" stroke="#E6E1D6" stroke-width="2"/>
<text x="40" y="40" fill="#C4A15A" font-size="14">circuito A-B-C-D-A · grados 2</text>
<text x="70" y="250" fill="#9A9488" font-size="13">2 colores bastan en el ciclo par</text>
<polygon points="430,200 520,50 640,170" fill="none" stroke="#C4A15A" stroke-width="3"/>
<circle cx="430" cy="200" r="16" fill="#C4A15A" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="520" cy="50" r="16" fill="#8F9A72" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="640" cy="170" r="16" fill="#E6E1D6" stroke="#C4A15A" stroke-width="2"/>
<text x="400" y="30" fill="#E6E1D6" font-size="14">triángulo: 3 colores · circuito</text>
<text x="400" y="250" fill="#9A9488" font-size="13">ciclo impar: no bastan 2 colores</text>
'''
build(
17, 'Eulerianos, hamiltonianos y <em>coloración</em>', 'C.1 Circuitos eulerianos, hamiltonianos y coloración',
'Recorrer aristas o vértices, y pintar sin choques',
'A la izquierda, un ciclo de 4: todos los grados valen 2, así que el propio ciclo es un circuito euleriano, y dos colores bastan. A la derecha, un triángulo: también es circuito euleriano, pero es un ciclo impar y necesita tres colores.',
['Decidir si hay circuito euleriano mirando los grados.','Distinguir ese recorrido de un ciclo hamiltoniano.','Colorear vértices adyacentes de distinto color y ver por qué un ciclo impar pide tres.'],
'''<h2>Dos recorridos y una pintura</h2>
<p>Un circuito euleriano recorre cada arista exactamente una vez y vuelve al inicio. Existe en un grafo conexo si y solo si todos los grados son pares. Un ciclo hamiltoniano recorre cada vértice exactamente una vez y vuelve al inicio: le importan los vértices, no cubrir las aristas.</p>
<p><span class="glosa">grado par = 0, 2, 4… · ciclo par = número par de vértices · ciclo impar = número impar · coloración propia = vértices unidos por una arista llevan colores distintos · número cromático = mínimo de colores que lo consiguen</span></p>
<p>El cuadrado de la izquierda tiene cuatro vértices de grado 2. El circuito A-B-C-D-A usa las cuatro aristas, una vez cada una, y es a la vez hamiltoniano porque también visita cada vértice una vez. Se colorea alternando ámbar y verde: los adyacentes quedan distintos y hacen falta 2 colores.</p>
<p>El triángulo de la derecha tiene grados 2, luego también admite circuito euleriano (y hamiltoniano): la vuelta al triángulo. Pero es un ciclo impar. Si intentas dos colores, el tercer vértice está unido a los otros dos, que ya llevan colores distintos, y no le queda ninguno. Hacen falta 3, como en el dibujo: ámbar, verde y claro.</p>
<table class="datos"><thead><tr><th></th><th>Ciclo de 4</th><th>Triángulo</th></tr></thead>
<tbody>
<tr><td>Grados</td><td>2, 2, 2, 2</td><td>2, 2, 2</td></tr>
<tr><td>¿Circuito euleriano?</td><td>sí</td><td>sí</td></tr>
<tr><td>¿Ciclo hamiltoniano?</td><td>sí, el mismo</td><td>sí, el mismo</td></tr>
<tr><td>Colores mínimos</td><td>2</td><td>3</td></tr>
</tbody></table>''',
'Ciclo de 4 coloreado con 2 colores y triángulo coloreado con 3, ambos con circuito', fig17,
[
('El cuadrado es euleriano',
 'Comprueba los grados del ciclo de 4 y escribe un circuito euleriano.',
 [
  ('Cada vértice del cuadrado incide en dos lados. Grados: 2, 2, 2 y 2, todos pares, y el grafo es conexo.',
   'Glosa: grado 2 es par. No hace falta que todos valgan lo mismo, solo que ninguno sea impar.'),
  ('Un circuito: A-B-C-D-A, siguiendo el trazo ámbar. Usa las 4 aristas y no repite ninguna.',
   'Glosa: volver al inicio es lo que lo hace circuito; si paras en otro vértice sería un camino euleriano, que aquí no pedimos.'),
  ('También es hamiltoniano: A, B, C y D aparecen una sola vez antes de cerrar.',
   'Glosa: en un ciclo simple las dos nociones coinciden. No coincidirán cuando haya aristas extra.'),
  ('Comprueba que no queda ninguna arista fuera del recorrido. Si sobrara un lado, no sería euleriano.',
   'Glosa: euleriano habla de aristas; si olvidas una, el circuito no sirve.'),
 ]),
('El triángulo pide tres colores',
 'Intenta colorear el triángulo con dos colores y explica dónde se rompe. Da después una coloración con tres.',
 [
  ('Pinta el primer vértice de ámbar y el segundo, que es adyacente, de verde.',
   'Glosa: dos unidos no pueden compartir color. El segundo queda forzado si solo hay dos colores.'),
  ('El tercero está unido al primero y al segundo. Ámbar y verde están prohibidos. Con solo dos colores no hay salida.',
   'Glosa: el conflicto es local en ese vértice, pero demuestra que todo el grafo necesita otro color.'),
  ('Con un tercer color (el claro del gráfico) el tercero se pinta y los tres pares de vecinos quedan distintos.',
   'Glosa: tres colores bastan. No hacen falta más, porque solo hay tres vértices.'),
  ('El número cromático del triángulo es 3. Es el ciclo impar más pequeño; todo ciclo impar necesita 3.',
   'Glosa: el ciclo de 4, par, sí se pudo hacer con 2. La paridad cambia la coloración.'),
 ]),
('Cuando euleriano y hamiltoniano se separan',
 'Añade al cuadrado una diagonal. ¿Siguen siendo pares los grados? ¿Sigue habiendo ciclo hamiltoniano?',
 [
  ('La diagonal suma 1 al grado de dos vértices opuestos. Esos pasan de 2 a 3, que es impar. Los otros dos siguen en 2.',
   'Glosa: una arista nueva cambia dos grados, no uno.'),
  ('Hay grados impares, luego ya no existe circuito euleriano. No intentes recorrerlo: alguna arista se repetirá o alguna quedará fuera.',
   'Glosa: la condición de los grados es necesaria. Si falla, se acabó el circuito euleriano.'),
  ('Sigue habiendo ciclos hamiltonianos: el borde A-B-C-D-A visita cada vértice una vez. La diagonal no es obligatoria en ese recorrido.',
   'Glosa: hamiltoniano puede ignorar aristas; euleriano no.'),
  ('Conclusión: al añadir la diagonal se pierde el circuito euleriano y se conserva un ciclo hamiltoniano. Son propiedades distintas.',
   'Glosa: el cuadrado original las tenía las dos; el nuevo grafo solo conserva una.'),
 ]),
],
[
(1, 'Un grado impar',
 'Un grafo conexo tiene grados 2, 2, 2 y 3. ¿Hay circuito euleriano?',
 'No, porque el vértice de grado 3 tiene grado impar. La condición exige que todos sean pares, no que «la mayoría» lo sean. El paso es revisar la lista completa antes de buscar el recorrido: si hay un impar, puedes dejar de dibujar caminos. Con un solo impar el enunciado además sería imposible por el lema de los grados (la suma sería impar), así que en un grafo real los impares van de dos en dos; con uno o más impares el circuito euleriano ya está descartado.',
 'e17a'),
(2, 'Colores del ciclo de 5',
 'Un ciclo de 5 vértices, sin diagonales. ¿Cuántos colores hacen falta como mínimo?',
 'Es un ciclo impar, como el triángulo pero con cinco vértices. Con dos colores, al alternar, el quinto queda al lado del primero y ambos recibirían el mismo color si cierras el ciclo. Ese choque obliga a un tercer color. Tres bastan: repites una pauta ámbar, verde, ámbar, verde y el quinto en claro, cuidando sus dos vecinos. El paso es no fiarte de que «es un ciclo, como el cuadrado»: el cuadrado es par y con dos colores cierra; el de 5 no.',
 'e17b'),
(3, 'Hamiltoniano que no cubre aristas',
 'En el cuadrado con una diagonal, da un ciclo hamiltoniano y señala una arista que ese ciclo no usa.',
 'El borde A-B-C-D-A es un ciclo hamiltoniano: entra cada vértice una vez y vuelve. La diagonal no forma parte de ese ciclo, luego hay una arista sin recorrer. Por eso el ciclo es hamiltoniano pero el recorrido no es euleriano, cosa que ya sabíamos porque hay grados 3. El paso es separar las dos listas: vértices visitados y aristas usadas. Que la primera esté completa no dice nada de la segunda.',
 'e17c'),
],
[
('¿Por qué el cuadrado del gráfico tiene circuito euleriano?',
 'Porque es conexo y los cuatro grados valen 2, que es par. Por qué: esa es la condición. El circuito es el propio borde, y usa cada lado una vez. No depende de los colores, que responden a otra pregunta.'),
('¿Por qué el triángulo no se colorea con dos colores?',
 'Porque es un ciclo impar: el tercer vértice toca a los otros dos. Por qué: esos dos ya necesitan colores distintos, y al tercero no le queda ninguno de los dos. Con tres colores, como en el SVG, sí se puede.'),
('¿Todo circuito euleriano es hamiltoniano?',
 'No. Por qué: el euleriano controla aristas y el hamiltoniano, vértices. En el cuadrado simple coinciden. Si un vértice tuviera grado 4, un circuito euleriano pasaría por ese vértice más de una vez y dejaría de ser un ciclo hamiltoniano, aunque cubriera las aristas.'),
],
'Pinta el circuito',
'Dibuja en el lienzo el cuadrado, escribe el circuito A-B-C-D-A y coloréalo con dos colores. Al lado, un triángulo con tres colores.',
['Izquierda: ciclo par, dos colores, circuito por el borde. Derecha: triángulo, tres colores.',
 'Grados 2 en todos los vértices de las dos figuras: las dos son eulerianas.',
 'Ejemplo 1: A-B-C-D-A no deja ningún lado fuera.',
 'Ejemplo 2: el tercer vértice del triángulo no cabe en dos colores.',
 'Ejemplo 3: una diagonal crea dos grados impares y mata el circuito euleriano, no el hamiltoniano del borde.',
 'No uses el color para decidir si el recorrido es euleriano.',
 'Ciclo par, 2 colores; ciclo impar, 3.']
)
print('L16 L17 en fuente')

# ---------- L18 ----------
write_lab(18, 'Tres caminos y sus longitudes', '''
<div class="panel">
<p>Grafo del ejemplo. Pesos: A-B 4, A-C 2, C-B 1, B-D 3, C-D 5. Compara los tres caminos de A a D.</p>
<button type="button" id="b1">A-B-D</button>
<button type="button" id="b2">A-C-D</button>
<button type="button" id="b3">A-C-B-D</button>
<div class="out" id="out"></div>
<canvas id="c" width="640" height="220"></canvas>
</div>
<script>
var P={A:[70,110],B:[250,40],C:[250,180],D:[480,110]};
var E=[['A','B',4],['A','C',2],['C','B',1],['B','D',3],['C','D',5]];
function dib(resalta){
  var cv=document.getElementById('c'), ctx=cv.getContext('2d');
  ctx.fillStyle='#12100e'; ctx.fillRect(0,0,640,220);
  ctx.font='14px sans-serif'; ctx.lineWidth=2;
  E.forEach(function(e){
    var a=P[e[0]], b=P[e[1]];
    var on=resalta.indexOf(e[0]+e[1])>=0 || resalta.indexOf(e[1]+e[0])>=0;
    ctx.strokeStyle=on?'#E6E1D6':'#C4A15A';
    ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]); ctx.stroke();
    ctx.fillStyle='#9A9488'; ctx.fillText(String(e[2]), (a[0]+b[0])/2+4, (a[1]+b[1])/2);
  });
  Object.keys(P).forEach(function(k){
    ctx.beginPath(); ctx.arc(P[k][0],P[k][1],15,0,6.3);
    ctx.fillStyle='#1C1A16'; ctx.fill(); ctx.strokeStyle='#E6E1D6'; ctx.stroke();
    ctx.fillStyle='#E6E1D6'; ctx.fillText(k,P[k][0]-4,P[k][1]+4);
  });
}
document.getElementById('b1').onclick=function(){dib(['AB','BD']); document.getElementById('out').textContent='A-B-D = 4+3 = 7';};
document.getElementById('b2').onclick=function(){dib(['AC','CD']); document.getElementById('out').textContent='A-C-D = 2+5 = 7';};
document.getElementById('b3').onclick=function(){dib(['AC','CB','BD']); document.getElementById('out').textContent='A-C-B-D = 2+1+3 = 6, el mínimo';};
dib(['AC','CB','BD']);
document.getElementById('out').textContent='Camino mínimo resaltado: A-C-B-D = 6';
</script>
''')
fig18 = '''
<line x1="80" y1="160" x2="260" y2="70" stroke="#9A9488" stroke-width="2"/>
<line x1="80" y1="160" x2="260" y2="250" stroke="#C4A15A" stroke-width="3"/>
<line x1="260" y1="250" x2="260" y2="70" stroke="#C4A15A" stroke-width="3"/>
<line x1="260" y1="70" x2="520" y2="160" stroke="#C4A15A" stroke-width="3"/>
<line x1="260" y1="250" x2="520" y2="160" stroke="#9A9488" stroke-width="2"/>
<circle cx="80" cy="160" r="18" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="260" cy="70" r="18" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="260" cy="250" r="18" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="520" cy="160" r="18" fill="#1C1A16" stroke="#C4A15A" stroke-width="3"/>
<text x="80" y="165" text-anchor="middle" fill="#E6E1D6">A</text>
<text x="260" y="75" text-anchor="middle" fill="#E6E1D6">B</text>
<text x="260" y="255" text-anchor="middle" fill="#E6E1D6">C</text>
<text x="520" y="165" text-anchor="middle" fill="#E6E1D6">D</text>
<text x="150" y="100" fill="#9A9488" font-size="14">4</text>
<text x="140" y="220" fill="#C4A15A" font-size="14">2</text>
<text x="268" y="160" fill="#C4A15A" font-size="14">1</text>
<text x="380" y="100" fill="#C4A15A" font-size="14">3</text>
<text x="400" y="230" fill="#9A9488" font-size="14">5</text>
<text x="80" y="30" fill="#E6E1D6" font-size="15">mínimo A-C-B-D = 2+1+3 = 6</text>
'''
build(18, 'Camino <em>mínimo</em>', 'C.1 Problema del camino mínimo',
'Seis kilómetros, no siete',
'En el grafo ponderado, A-B pesa 4, A-C pesa 2, C-B pesa 1, B-D pesa 3 y C-D pesa 5. El camino más corto de A a D no es el de menos aristas: es A-C-B-D, con longitud 6. Los otros dos caminos conocidos valen 7.',
['Sumar los pesos de un camino, no contar aristas.','Comparar todos los caminos simples de A a D.','Elegir el mínimo y explicar por qué un atajo visual puede ser más largo.'],
'''<h2>El peso manda, no el número de saltos</h2>
<p>En un grafo ponderado cada arista lleva un número: minutos, euros o kilómetros. La longitud de un camino es la suma de esos pesos. El camino mínimo entre dos vértices es el de menor suma. No tiene por qué ser el que tiene menos aristas.</p>
<p><span class="glosa">peso = número de la arista · longitud de un camino = suma de pesos · camino simple = no repite vértices · en el dibujo el trazo ámbar es A-C-B-D y el gris son las aristas que no entran en ese mínimo</span></p>
<p>De A a D hay tres caminos simples. A-B-D suma 4+3 = 7. A-C-D suma 2+5 = 7. A-C-B-D suma 2+1+3 = 6. El tercero usa tres aristas y aun así es más corto que los de dos, porque C-B pesa solo 1 y evita la arista C-D, que pesa 5.</p>
<p>No hace falta un algoritmo con nombre para un grafo de cuatro vértices: se enumeran los caminos simples y se comparan. En un grafo grande esa enumeración se sustituye por un método ordenado (como el de Dijkstra si los pesos son positivos). La idea no cambia: no te detienes en el primer camino que llega.</p>
<table class="datos"><thead><tr><th>Camino</th><th>Suma</th><th>¿Mínimo?</th></tr></thead>
<tbody>
<tr><td>A-B-D</td><td>4+3 = 7</td><td>no</td></tr>
<tr><td>A-C-D</td><td>2+5 = 7</td><td>no</td></tr>
<tr><td>A-C-B-D</td><td>2+1+3 = 6</td><td>sí</td></tr>
</tbody></table>''',
'Grafo ponderado con el camino mínimo A-C-B-D de longitud 6 resaltado', fig18,
[
('Las tres sumas',
 'Con los pesos del gráfico, calcula la longitud de A-B-D, de A-C-D y de A-C-B-D.',
 [
  ('A-B-D usa las aristas de peso 4 y 3. Longitud 4+3 = 7.',
   'Glosa: no cuentes «dos aristas» como longitud 2; 2 sería un recuento, no una suma de pesos.'),
  ('A-C-D usa 2 y 5. Longitud 2+5 = 7. Llega en dos saltos, igual que el anterior, y cuesta lo mismo.',
   'Glosa: empate en 7 no significa que sean el mismo camino; solo que la suma coincide.'),
  ('A-C-B-D usa 2, 1 y 3. Longitud 2+1+3 = 6. Es el trazo ámbar del SVG.',
   'Glosa: tres aristas pueden sumar menos que dos si una de las cortas evita un peso grande.'),
  ('El mínimo de 7, 7 y 6 es 6. Cualquier otro recorrido que repita un vértice solo añadiría peso positivo y no mejoraría.',
   'Glosa: con pesos positivos, un rodeo no acorta. Por eso basta mirar caminos simples.'),
 ]),
('Por qué C-D no es un atajo',
 'Explica, con la resta de los números, por qué ir de C a D directo es peor que C-B-D.',
 [
  ('De C a D directo: peso 5.',
   'Glosa: es la arista gris inferior derecha.'),
  ('De C a D por B: C-B pesa 1 y B-D pesa 3, suma 4.',
   'Glosa: 1+3 = 4, que ya es menor que 5 antes de mirar el resto del viaje.'),
  ('Diferencia: 5 − 4 = 1. El rodeo por B ahorra 1 respecto del directo.',
   'Glosa: por eso el camino completo que usa C-D queda en 7 y el que usa C-B-D queda en 6.'),
  ('Conclusión local: entre C y D, con estos pesos, el mínimo no es la arista directa. Hay que comprobar los desvíos.',
   'Glosa: «directo» en el dibujo no es «mínimo» en la suma.'),
 ]),
('Cambia un peso',
 'Si el peso de C-B pasa de 1 a 4 y el resto no cambia, ¿cuál es el nuevo mínimo de A a D?',
 [
  ('A-B-D no usa C-B: sigue en 4+3 = 7.',
   'Glosa: un peso que no está en el camino no lo altera.'),
  ('A-C-D tampoco usa C-B: sigue en 2+5 = 7.',
   'Glosa: el empate anterior se mantiene.'),
  ('A-C-B-D pasa a 2+4+3 = 9, que ya es peor que 7.',
   'Glosa: el antiguo mínimo se rompe porque su arista barata ha dejado de serlo.'),
  ('El nuevo mínimo es 7, compartido por A-B-D y A-C-D. Ya no hay un único camino mínimo.',
   'Glosa: di los dos. Quedarte con el ámbar del gráfico, sin rehacer la suma, es el error.'),
 ]),
],
[
(1, 'Un cuarto camino que no ayuda',
 'Alguien propone A-B-C-D. Con los pesos originales, ¿qué longitud tiene y por qué no mejora el 6?',
 'A-B pesa 4, B-C es la misma arista que C-B y pesa 1, C-D pesa 5. Suma 4+1+5 = 10. Es mayor que 6 y también mayor que 7. El paso es sumar las tres aristas de verdad, no reutilizar el 6 del camino ámbar. Además A-B-C-D baja a C para luego pagar el 5 de C-D, justo la arista cara que el mínimo evitaba. Con pesos positivos, meter un vértice de más solo compensa si sustituye una arista cara por varias baratas; aquí no ocurre.',
 'e18a'),
(2, 'Menos aristas no basta',
 'Sin calcular, ¿puedes afirmar que A-C-D es mínimo porque solo tiene dos aristas? Justifica con los números.',
 'No. A-C-D suma 7 y A-C-B-D suma 6 teniendo una arista más. El criterio «menos aristas» sería válido si todos los pesos fueran 1. Aquí no lo son: C-D pesa 5 ella sola, más que C-B y B-D juntas (1+3 = 4). El paso es sustituir el recuento de aristas por la suma de pesos antes de declarar un mínimo. El gráfico lo separa con el color: el camino de tres tramos ámbar es el corto.',
 'e18b'),
(3, 'Peso nuevo en A-B',
 'El peso de A-B baja a 1 y los demás siguen igual. Recalcula el mínimo de A a D.',
 'A-B-D pasa a 1+3 = 4. A-C-D sigue en 7. A-C-B-D sigue en 6. El mínimo nuevo es 4, por A-B-D. El paso es no conservar el 6 como respuesta solo porque antes ganaba: ha cambiado una arista del camino que iba segundo. Comprueba que 4 es menor que 6 y que 7. El laboratorio sirve para ensayar el caso original; este cambio lo haces a mano y anotas las tres sumas otra vez.',
 'e18c'),
],
[
('¿Cuál es la longitud mínima de A a D en el gráfico?',
 '6, por A-C-B-D. Por qué: las otras dos sumas simples valen 7 (4+3 y 2+5). 2+1+3 = 6 es la menor. No es el camino con menos aristas: tiene tres tramos y aun así gana, porque los pesos no valen 1.'),
('¿Por qué C-D, que se ve directa, no forma parte del mínimo?',
 'Porque pesa 5, y C-B-D pesa 4. Por qué: 5 es mayor que 1+3. Meter esa arista en el viaje desde A produce 2+5 = 7, un kilómetro más que el ámbar.'),
('Si todos los pesos fueran 1, ¿cambiaría el criterio?',
 'Sí: entonces la longitud coincidiría con el número de aristas y ganaría un camino de dos aristas. Por qué: hoy los pesos no son iguales, así que la suma y el recuento ordenan los caminos de forma distinta. El 6 actual depende de que C-B pese 1.'),
],
'Otro destino',
'En el lienzo copia el grafo con sus pesos y marca el camino mínimo de A a D. Escribe las tres sumas al lado.',
['El ámbar del SVG es A-C-B-D y suma 6. Las aristas grises son las que quedan fuera de ese mínimo.',
 'A-B-D = 7 y A-C-D = 7. Ninguno bate al 6.',
 'Ejemplo 1: se comparan las tres sumas, no el número de saltos.',
 'Ejemplo 2: C-D pesa 5 y C-B-D pesa 4, por eso el directo no es atajo.',
 'Ejemplo 3: si C-B pasa a valer 4, el mínimo sube a 7 y hay empate.',
 'En el laboratorio resalta cada camino antes de creerte el color.',
 'Con pesos positivos no mejores un camino repitiendo vértices.'],
lab_title='Tres caminos y sus longitudes')

# ---------- L19 ----------
fig19 = '''
<line x1="60" y1="200" x2="680" y2="200" stroke="#9A9488" stroke-width="2"/>
<line x1="120" y1="200" x2="120" y2="150" stroke="#C4A15A" stroke-width="3"/>
<line x1="260" y1="200" x2="260" y2="110" stroke="#C4A15A" stroke-width="3"/>
<line x1="400" y1="200" x2="400" y2="70" stroke="#C4A15A" stroke-width="3"/>
<line x1="540" y1="200" x2="540" y2="30" stroke="#C4A15A" stroke-width="3"/>
<circle cx="120" cy="150" r="8" fill="#E6E1D6"/>
<circle cx="260" cy="110" r="8" fill="#E6E1D6"/>
<circle cx="400" cy="70" r="8" fill="#E6E1D6"/>
<circle cx="540" cy="30" r="8" fill="#E6E1D6"/>
<text x="120" y="230" text-anchor="middle" fill="#E6E1D6" font-size="14">n=1 · 3</text>
<text x="260" y="230" text-anchor="middle" fill="#E6E1D6" font-size="14">n=2 · 7</text>
<text x="400" y="230" text-anchor="middle" fill="#E6E1D6" font-size="14">n=3 · 11</text>
<text x="540" y="230" text-anchor="middle" fill="#E6E1D6" font-size="14">n=4 · 15</text>
<text x="60" y="28" fill="#C4A15A" font-size="15">a(n) = 4n − 1. De un término al siguiente se suman 4.</text>
'''
build(19, 'Patrones y <em>generalización</em>', 'D.1 Generalización de patrones',
'Tres comprobaciones antes de la fórmula',
'La sucesión 3, 7, 11, 15 sube de 4 en 4. La fórmula candidata es a(n) = 4n − 1. No se acepta hasta comprobar n = 1, n = 2 y n = 3, que son los tres primeros círculos del gráfico.',
['Describir el patrón con una frase de cómo se pasa de un término al siguiente.','Proponer una fórmula y comprobarla en n = 1, 2 y 3.','Calcular un término lejano con la fórmula, no recorriendo toda la lista.'],
'''<h2>Del salto constante a la fórmula, con red de seguridad</h2>
<p>Un patrón numérico se generaliza cuando puedes decir el término que ocupa el lugar n sin haber escrito todos los anteriores. En una sucesión aritmética el salto entre términos consecutivos es siempre el mismo. Ese salto es la diferencia, y entra en la fórmula como coeficiente de n.</p>
<p><span class="glosa">a(n) = término que ocupa el lugar n, empezando en n = 1 · diferencia d = 4 en este ejemplo · a(n) = 4n − 1 · comprobar n = 1, 2 y 3 significa sustituir y ver si salen 3, 7 y 11, no mirar solo el dibujo</span></p>
<p>Si el primero es 3 y cada vez se suman 4, el término n ha sufrido (n − 1) saltos. Entonces a(n) = 3 + (n − 1)·4 = 3 + 4n − 4 = 4n − 1. Las dos escrituras dicen lo mismo. El gráfico enseña los cuatro primeros: alturas 3, 7, 11 y 15, separadas por el mismo salto visual.</p>
<p>Una fórmula que solo acierta el primer término no sirve. Por eso la comprobación pide tres valores, no uno. Si falla en n = 2 o en n = 3, se descarta aunque «se parezca» al principio.</p>
<table class="datos"><thead><tr><th>n</th><th>4n − 1</th><th>Término de la lista</th><th>¿Cuadra?</th></tr></thead>
<tbody>
<tr><td>1</td><td>4·1 − 1 = 3</td><td>3</td><td>sí</td></tr>
<tr><td>2</td><td>4·2 − 1 = 7</td><td>7</td><td>sí</td></tr>
<tr><td>3</td><td>4·3 − 1 = 11</td><td>11</td><td>sí</td></tr>
<tr><td>4</td><td>4·4 − 1 = 15</td><td>15</td><td>sí, predicción ya vista</td></tr>
</tbody></table>''',
'Cuatro puntos de la sucesión 3, 7, 11, 15 con la fórmula 4n − 1', fig19,
[
('Comprobar n = 1, 2 y 3',
 'La lista empieza 3, 7, 11. Alguien propone a(n) = 4n − 1. Sustituye n = 1, n = 2 y n = 3.',
 [
  ('n = 1: 4·1 − 1 = 3. Coincide con el primer círculo.',
   'Glosa: el primer término no es 4n; hay que restar 1. Sin esa resta saldría 4.'),
  ('n = 2: 4·2 − 1 = 7. Coincide con el segundo.',
   'Glosa: aquí se ve el salto: de 3 a 7 hay +4, que es el coeficiente.'),
  ('n = 3: 4·3 − 1 = 11. Coincide con el tercero.',
   'Glosa: tres aciertos seguidos no son una casualidad del primero. La fórmula supera la red.'),
  ('Como las tres comprobaciones cierran, se acepta a(n) = 4n − 1 para esta sucesión, y el cuarto término 15 queda predicho: 4·4 − 1 = 15.',
   'Glosa: predecir el cuarto ya no exige sumar 4 al 11, aunque esa suma sirve de comprobación extra.'),
 ]),
('De dónde sale el −1',
 'Escribe a(n) como «el primero más los saltos» y llega a 4n − 1.',
 [
  ('El primer término es 3 y cada salto suma 4.',
   'Glosa: 3 es a(1), no la diferencia. La diferencia es 4.'),
  ('Para llegar al lugar n haces (n − 1) saltos, no n. Del 1 al 2 hay un salto, no dos.',
   'Glosa: contar n saltos es el error que desplaza toda la fórmula.'),
  ('a(n) = 3 + (n − 1)·4 = 3 + 4n − 4 = 4n − 1.',
   'Glosa: el −1 es lo que queda de 3 − 4, no un ajuste misterioso.'),
  ('Comprueba de nuevo n = 1 en esta forma: 3 + (1 − 1)·4 = 3. Cero saltos, te quedas en el primero.',
   'Glosa: si en n = 1 no recuperas el primer término, has contado mal los saltos.'),
 ]),
('Un término lejano y una fórmula falsa',
 'Calcula a(20) con la fórmula buena. Después prueba b(n) = 4n + 3 y di en qué comprobación muere.',
 [
  ('a(20) = 4·20 − 1 = 80 − 1 = 79. No hace falta escribir los 19 términos intermedios.',
   'Glosa: para eso se generaliza: el lugar 20 está a 19 saltos de 4 desde el 3, y 3+76 = 79.'),
  ('b(1) = 4·1 + 3 = 7, que ya no es 3. Falla en la primera comprobación.',
   'Glosa: ni siquiera hace falta mirar n = 2. Una fórmula que no da el primer término está descartada.'),
  ('Aunque alguien dijera «también sube de 4 en 4», el nivel de partida es otro: 7, 11, 15… no es nuestra lista.',
   'Glosa: la diferencia no determina la sucesión sola; falta el primer término.'),
  ('Por eso pedimos tres comprobaciones cuando la fórmula es candidata seria, y basta una en contra para rechazarla.',
   'Glosa: n = 1, 2 y 3 son el mínimo de esta lección antes de fiarte de a(20).'),
 ]),
],
[
(1, 'El término 10',
 'Con a(n) = 4n − 1, calcula a(10) y comprueba sumando saltos desde a(3) = 11.',
 'Por la fórmula, a(10) = 40 − 1 = 39. Desde n = 3 hasta n = 10 hay 7 saltos de 4: 11 + 7·4 = 11 + 28 = 39. Las dos cuentas coinciden. El paso útil es no sumar de uno en uno los diez términos: o usas la fórmula cerrada o cuentas solo los saltos que faltan. Si te sale 40, te has dejado el −1 o has hecho 10·4 sin restar.',
 'e19a'),
(2, 'Otra diferencia',
 'La lista 5, 8, 11, 14 tiene diferencia 3 y primer término 5. Escribe la fórmula y comprueba n = 1, 2 y 3.',
 'a(n) = 5 + (n − 1)·3 = 3n + 2. Comprobación: n = 1 da 5; n = 2 da 8; n = 3 da 11. El paso delicado es el (n − 1): si escribes 5 + 3n, en n = 1 sale 8 y ya no es la lista. Desarrollar 5 + 3n − 3 = 3n + 2 permite comprobar más rápido, pero la forma con saltos explica de dónde sale. Las tres sustituciones son obligatorias antes de usar la fórmula para un n grande.',
 'e19b'),
(3, 'Patrón que no es de salto constante',
 'Miras 2, 4, 8, 16. ¿Sirve una fórmula del tipo an + b? ¿Qué compruebas?',
 'No es aritmética: los saltos son +2, +4 y +8, no son constantes. Una fórmula an + b produce saltos iguales, así que no puede generar esta lista. Se ve al comprobar: si fuerzas el primer salto, de 2 a 4, la diferencia sería 2 y el tercero tendría que ser 6, pero la lista dice 8. El paso es mirar si la diferencia se repite antes de copiar el método de 4n − 1. Aquí el patrón es multiplicar por 2: a(n) = 2ⁿ, y se comprueba 2¹ = 2, 2² = 4, 2³ = 8.',
 'e19c'),
],
[
('¿Qué da a(n) = 4n − 1 en n = 1, n = 2 y n = 3?',
 'Da 3, 7 y 11. Por qué: 4·1 − 1 = 3, 4·2 − 1 = 7 y 4·3 − 1 = 11, que son los tres primeros términos dibujados. Sin esas tres sustituciones la fórmula es solo una sospecha.'),
('¿Por qué el número de saltos hasta el lugar n es n − 1?',
 'Porque el primer término ya está puesto y no cuenta como salto. Por qué: del lugar 1 al lugar n hay n − 1 huecos. En n = 1 hay 0 saltos y la fórmula devuelve 3. Contar n saltos sumaría un 4 de más.'),
('¿Por qué b(n) = 4n + 3 no sirve para 3, 7, 11?',
 'Porque en n = 1 da 7, no 3. Por qué: comparte la diferencia 4, pero arranca en otro sitio. Una sola comprobación fallida basta para rechazarla; no se «arregla» mirando solo el dibujo del salto.'),
],
'Tu sucesión',
'Inventa una sucesión aritmética de cuatro términos, escribe la fórmula y comprueba n = 1, 2 y 3 en el editor. Dibuja los puntos en el lienzo.',
['Los círculos marcan 3, 7, 11 y 15. El salto vertical entre ellos es el +4.',
 'La fórmula 4n − 1 sale de 3 + (n − 1)·4.',
 'Ejemplo 1: n = 1, 2 y 3 devuelven exactamente 3, 7 y 11.',
 'Ejemplo 2: el −1 es 3 − 4, el ajuste de contar n − 1 saltos.',
 'Ejemplo 3: a(20) = 79, y 4n + 3 muere ya en n = 1.',
 'No des por buena una fórmula que solo acierta el primer término.',
 'Si los saltos no son constantes, no uses este modelo.'],
None)

print('append L18 L19 escrito en este bloque')

# ---------- L20 ----------
write_lab(20, 'Recta y = mx + n', '''
<div class="panel">
<p>La recta de la lección es y = 2x + 1. Cambia m o n y mira los puntos.</p>
<label>m <input id="m" type="number" value="2" step="0.5"/></label>
<label>n <input id="n" type="number" value="1" step="0.5"/></label>
<button id="go" type="button">Dibujar</button>
<div class="out" id="out"></div>
<canvas id="c" width="640" height="220"></canvas>
</div>
<script>
function dib(){
  var m=parseFloat(document.getElementById('m').value), n=parseFloat(document.getElementById('n').value);
  var cv=document.getElementById('c'), ctx=cv.getContext('2d');
  ctx.fillStyle='#12100e'; ctx.fillRect(0,0,640,220);
  ctx.strokeStyle='#9A9488'; ctx.beginPath(); ctx.moveTo(40,180); ctx.lineTo(600,180); ctx.moveTo(80,20); ctx.lineTo(80,200); ctx.stroke();
  ctx.strokeStyle='#C4A15A'; ctx.beginPath();
  for(var x=0;x<=5.01;x+=0.1){var px=80+x*80, py=180-(m*x+n)*18; if(x===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);} ctx.stroke();
  ctx.fillStyle='#E6E1D6';
  [0,1,2].forEach(function(x){var y=m*x+n; ctx.beginPath(); ctx.arc(80+x*80,180-y*18,4,0,6.3); ctx.fill();});
  document.getElementById('out').textContent='Puntos: (0, '+n+'), (1, '+(m+n)+'), (2, '+(2*m+n)+')';
}
document.getElementById('go').onclick=dib; dib();
</script>
''')
fig20 = ejes(70, 280, 660, 30) + '''
<line x1="70" y1="250" x2="430" y2="70" stroke="#C4A15A" stroke-width="3"/>
<circle cx="70" cy="250" r="6" fill="#E6E1D6"/>
<circle cx="190" cy="190" r="6" fill="#E6E1D6"/>
<circle cx="310" cy="130" r="6" fill="#E6E1D6"/>
<line x1="70" y1="250" x2="190" y2="250" stroke="#8F9A72" stroke-width="2"/>
<line x1="190" y1="250" x2="190" y2="190" stroke="#8F9A72" stroke-width="2"/>
<text x="100" y="270" fill="#E6E1D6" font-size="14">(0, 1)</text>
<text x="200" y="185" fill="#E6E1D6" font-size="14">(1, 3)</text>
<text x="320" y="120" fill="#E6E1D6" font-size="14">(2, 5)</text>
<text x="450" y="80" fill="#C4A15A" font-size="16">y = 2x + 1</text>
<text x="450" y="120" fill="#8F9A72" font-size="14">sube 2 cuando x avanza 1</text>
'''
build(20, 'Funciones <em>afines</em>', 'D.2 Funciones afines',
'Pendiente 2, corte en 1',
'La recta del ejemplo es y = 2x + 1. Corta al eje en (0, 1) y pasa por (1, 3) y (2, 5). El triángulo verde del gráfico mide el salto: una unidad a la derecha y dos hacia arriba.',
['Identificar pendiente y ordenada en el origen.','Construir la tabla de valores y situar los puntos.','Leer crecimiento y un valor concreto sobre la recta.'],
'''<h2>Una recta queda fijada por dos números</h2>
<p>Una función afín tiene la forma y = mx + n. El número m es la pendiente: lo que cambia y cuando x aumenta una unidad. El número n es el valor de y cuando x vale 0, el corte con el eje vertical.</p>
<p><span class="glosa">m = 2 en el ejemplo · n = 1 · punto de la recta = par (x, 2x+1) · creciente porque m es positivo · si m fuera negativo la recta bajaría</span></p>
<p>Sustituir es obligatorio antes de dibujar. Para x = 0, y = 1. Para x = 1, y = 2·1 + 1 = 3. Para x = 2, y = 4 + 1 = 5. Esos tres puntos son los círculos del SVG, y la recta ámbar pasa por los tres. No hace falta un cuarto punto para trazarla, pero sirve de comprobación: x = 3 da y = 7, y el extremo derecho del segmento va hacia esa zona.</p>
<p>El escalón verde entre (0, 1) y (1, 3) separa el avance horizontal, que es 1, del vertical, que es 2. El cociente 2/1 es la pendiente. Si alguien dice que la pendiente es 1 porque «empieza en 1», está leyendo n en lugar de m.</p>
<table class="datos"><thead><tr><th>x</th><th>2x + 1</th><th>Punto</th></tr></thead>
<tbody>
<tr><td>0</td><td>1</td><td>(0, 1)</td></tr>
<tr><td>1</td><td>3</td><td>(1, 3)</td></tr>
<tr><td>2</td><td>5</td><td>(2, 5)</td></tr>
<tr><td>3</td><td>7</td><td>comprobación, fuera de los tres círculos</td></tr>
</tbody></table>''',
'Recta y = 2x + 1 con los puntos (0, 1), (1, 3) y (2, 5) marcados', fig20,
[
('La tabla del gráfico',
 'Calcula y = 2x + 1 en x = 0, x = 1 y x = 2, y di qué es cada número de la fórmula.',
 [
  ('En x = 0 queda solo n: y = 1. El círculo de la izquierda está sobre el eje, a altura 1.',
   'Glosa: n no es la pendiente. Es el punto de arranque.'),
  ('En x = 1: 2·1 + 1 = 3. Has sumado la pendiente una vez.',
   'Glosa: de (0, 1) a (1, 3) el vertical es +2, que es m.'),
  ('En x = 2: 2·2 + 1 = 5. Segundo círculo a la derecha del centro del tramo.',
   'Glosa: otro paso de +2. La tabla 1, 3, 5 es aritmética de diferencia 2.'),
  ('Comprobación x = 3: 2·3 + 1 = 7. Si tu recta no puede pasar por (3, 7), la pendiente está mal copiada.',
   'Glosa: tres puntos alineados no se discuten; el cuarto caza un error de cuentas.'),
 ]),
('Pendiente como cociente',
 'Entre (1, 3) y (2, 5), calcula el cociente de incrementos y relaciónalo con m.',
 [
  ('Δx = 2 − 1 = 1. Δy = 5 − 3 = 2.',
   'Glosa: final menos inicial en cada coordenada, como en la variación media.'),
  ('Cociente Δy/Δx = 2/1 = 2.',
   'Glosa: ese 2 es m. En una recta el cociente no depende de qué puntos elijas.'),
  ('Prueba con (0, 1) y (2, 5): Δx = 2, Δy = 4, cociente 4/2 = 2. La misma pendiente.',
   'Glosa: si te saliera otro número, los puntos no estarían en la misma recta.'),
  ('Por eso la función es creciente: al avanzar x, y sube. Un m negativo invertiría el escalón verde.',
   'Glosa: el signo de m se lee en el dibujo sin calcular, y el cálculo lo confirma.'),
 ]),
('Hallar x conocido y',
 '¿Para qué x la recta vale 11? Comprueba sustituyendo.',
 [
  ('Plantea 2x + 1 = 11.',
   'Glosa: 11 es una ordenada, no un valor de x. Despeja, no lo coloques en la tabla como si fuera x.'),
  ('Resta 1: 2x = 10. Divide entre 2: x = 5.',
   'Glosa: la pendiente está multiplicando, así que al final se divide, no se resta.'),
  ('Comprobación: 2·5 + 1 = 11. Vuelve a la fórmula.',
   'Glosa: si no recuperas 11, el despeje está mal.'),
  ('En el gráfico, x = 5 cae a la derecha de los círculos, pero en la misma recta. No hace falta que el punto esté dibujado para que exista.',
   'Glosa: el SVG enseña el patrón; la fórmula vale fuera del recuadro.'),
 ]),
],
[
(1, 'Otra pendiente',
 'Dibuja mentalmente y = −x + 4. Calcula los valores en x = 0, x = 1 y x = 2 y di si crece.',
 'En x = 0, y = 4. En x = 1, y = 3. En x = 2, y = 2. Baja una unidad cada vez porque m = −1. No es creciente. El paso es leer el signo antes de unir los puntos: la ordenada en el origen es 4, distinta de la del ejemplo, y la pendiente es negativa, así que el escalón baja en vez de subir. Comprueba el cociente entre (0, 4) y (2, 2): Δy/Δx = −2/2 = −1, que es m.',
 'e20a'),
(2, 'Ecuación de la recta de dos puntos',
 'Pasa por (0, 1) y (1, 3), que ya conoces. Escribe la ecuación y explica qué dato te da cada punto.',
 '(0, 1) fija n = 1, porque cuando x es 0 la fórmula se reduce a n. Entre los dos puntos, Δy/Δx = (3−1)/(1−0) = 2, así que m = 2. La ecuación es y = 2x + 1, la del gráfico. El paso que no se salta es usar el punto del eje para n y un cociente para m, no inventar la pendiente mirando solo una coordenada. Si el primer punto no tuviera x = 0, n no se leería directamente y habría que sustituir después de conocer m.',
 'e20b'),
(3, 'Error de lectura',
 'Alguien dice que y = 2x + 1 en x = 4 vale 6 porque «2+4». ¿Qué ha confundido?',
 'Ha sumado la pendiente con la abscisa y se ha dejado el producto y el término n. Lo correcto es 2·4 + 1 = 9. El paso es respetar la estructura mx + n: m multiplica a x. Sumar 2+4 trata la pendiente como si fuera otro sumando suelto. Comprueba con el patrón de la tabla: desde (2, 5) hasta x = 4 hay dos pasos de +2, así que y = 5+4 = 9, el mismo resultado. El 6 no aparece en esta recta para un x entero pequeño.',
 'e20c'),
],
[
('¿Qué puntos del gráfico confirman y = 2x + 1?',
 '(0, 1), (1, 3) y (2, 5). Por qué: al sustituir esos x se obtienen exactamente esas y, y el escalón verde mide la pendiente 2 entre los dos primeros. Tres puntos alineados con esa tabla fijan la recta del ejemplo.'),
('¿Qué número es la pendiente y cuál el corte?',
 'La pendiente es 2 y el corte es 1. Por qué: en y = mx + n, m multiplica a x y n es y cuando x = 0. Confundirlos hace que la recta arranque en 2 o que suba solo 1.'),
('Si m pasa a ser 0, ¿qué queda?',
 'La recta horizontal y = 1. Por qué: 0·x + 1 = 1 para todo x. No hay escalón vertical. Sigue siendo afín, pero ya no es creciente ni decreciente: es constante.'),
],
'Marca la tuya',
'Elige otra m y otra n en el laboratorio, copia tres puntos en el lienzo y escribe la pendiente como cociente.',
['La recta ámbar pasa por (0, 1), (1, 3) y (2, 5). El escalón verde es +1 en x y +2 en y.',
 'm = 2 es el cociente. n = 1 es la altura en el eje.',
 'Ejemplo 1: la tabla 1, 3, 5 y la comprobación 7.',
 'Ejemplo 2: entre cualquier par de esos puntos el cociente vuelve a ser 2.',
 'Ejemplo 3: y = 11 obliga x = 5, porque 2·5 + 1 = 11.',
 'No sumes m y x. Multiplica.',
 'En el laboratorio mueve n y verás que la recta sube o baja sin cambiar de inclinación.'],
lab_title='Recta y = mx + n')

# ---------- L21 ----------
write_lab(21, 'Parábola con raíces 1 y 3', '''
<div class="panel">
<p>f(x) = (x − 1)(x − 3). El vértice está en x = 2. Pulsa para leer f(1), f(2) y f(3).</p>
<button id="go" type="button">Calcular</button>
<div class="out" id="out"></div>
<canvas id="c" width="640" height="220"></canvas>
</div>
<script>
function fy(x){return (x-1)*(x-3);} 
function dib(){
  var cv=document.getElementById('c'), ctx=cv.getContext('2d');
  ctx.fillStyle='#12100e'; ctx.fillRect(0,0,640,220);
  ctx.strokeStyle='#9A9488'; ctx.beginPath(); ctx.moveTo(40,140); ctx.lineTo(600,140); ctx.moveTo(40,140); ctx.lineTo(40,20); ctx.stroke();
  ctx.strokeStyle='#C4A15A'; ctx.beginPath();
  for(var x=0;x<=4.01;x+=0.05){var px=40+x*120, py=140-fy(x)*30; if(x===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);} ctx.stroke();
  ctx.fillStyle='#E6E1D6';
  [[1,0],[2,-1],[3,0]].forEach(function(p){ctx.beginPath(); ctx.arc(40+p[0]*120,140-p[1]*30,5,0,6.3); ctx.fill();});
  document.getElementById('out').textContent='f(1)=0, f(2)=−1, f(3)=0. Vértice (2, −1).';
}
document.getElementById('go').onclick=dib; dib();
</script>
''')
fig21 = ejes(50, 250, 680, 24)
fig21 += path_fn(lambda x: (x-1)*(x-3), 0, 4, 40, lambda x: 60+x*140, lambda y: 200 - y*55)
fig21 += '''
<circle cx="200" cy="200" r="6" fill="#E6E1D6"/>
<circle cx="480" cy="200" r="6" fill="#E6E1D6"/>
<circle cx="340" cy="255" r="6" fill="#C4A15A"/>
<line x1="340" y1="255" x2="340" y2="200" stroke="#8F9A72" stroke-width="1.5" stroke-dasharray="4 3"/>
<text x="168" y="188" fill="#E6E1D6" font-size="14">(1, 0)</text>
<text x="490" y="188" fill="#E6E1D6" font-size="14">(3, 0)</text>
<text x="350" y="270" fill="#C4A15A" font-size="14">vértice (2, −1)</text>
<text x="60" y="22" fill="#C4A15A" font-size="15">f(x) = (x − 1)(x − 3) = x² − 4x + 3</text>
'''
build(21, 'Funciones <em>cuadráticas</em>', 'D.2 Funciones cuadráticas',
'Raíces en 1 y en 3, vértice en medio',
'La parábola f(x) = (x − 1)(x − 3) corta al eje horizontal en x = 1 y en x = 3. El vértice, punto más bajo, está en la mitad, x = 2, y vale f(2) = −1. Esos tres puntos están marcados en el gráfico.',
['Leer las raíces en la forma factorizada.','Calcular el vértice como punto medio de las raíces y evaluar.','Pasar a la forma x² − 4x + 3 y comprobar un punto.'],
'''<h2>Dónde corta y dónde gira</h2>
<p>Una cuadrática de la forma (x − r)(x − s) vale 0 justo cuando x = r o x = s. Esas son las raíces, los cortes con el eje horizontal. La parábola es simétrica respecto de la vertical que pasa por el punto medio de las raíces. Ese punto es el vértice.</p>
<p><span class="glosa">raíces 1 y 3 · eje de simetría x = (1+3)/2 = 2 · f(2) = −1 · abre hacia arriba porque el coeficiente de x² es positivo · f(x) = x² − 4x + 3 es la misma función desarrollada</span></p>
<p>En el gráfico los círculos claros están en (1, 0) y (3, 0), sobre el eje. El círculo ámbar está más abajo, en (2, −1): entre las dos raíces la función es negativa, porque los factores (x−1) y (x−3) tienen signos distintos. Fuera del intervalo, por ejemplo en x = 0 o en x = 4, la función vale 3 y la curva está por encima del eje.</p>
<p>Desarrollar no cambia la parábola: (x−1)(x−3) = x² − 3x − x + 3 = x² − 4x + 3. Sustituir x = 1 en el polinomio da 1 − 4 + 3 = 0, la misma raíz. El vértice no se lee en el término independiente; el 3 es f(0), otro punto.</p>
<table class="datos"><thead><tr><th>x</th><th>f(x)</th><th>Qué es</th></tr></thead>
<tbody>
<tr><td>1</td><td>0</td><td>raíz</td></tr>
<tr><td>2</td><td>−1</td><td>vértice, mínimo</td></tr>
<tr><td>3</td><td>0</td><td>raíz</td></tr>
<tr><td>0</td><td>3</td><td>corte con el eje vertical</td></tr>
</tbody></table>''',
'Parábola con raíces en x = 1 y x = 3 y vértice en (2, −1)', fig21,
[
('Raíces y vértice',
 'Para f(x) = (x − 1)(x − 3), halla los cortes con el eje horizontal y el vértice.',
 [
  ('f(x) = 0 cuando x − 1 = 0 o x − 3 = 0. Raíces x = 1 y x = 3. Son los círculos claros.',
   'Glosa: no sumes 1+3 para obtener una raíz. Cada factor aporta la suya.'),
  ('El eje de simetría es la media: (1+3)/2 = 2.',
   'Glosa: en una parábola con dos raíces, el vértice cae justo en medio.'),
  ('f(2) = (2−1)(2−3) = (1)(−1) = −1. Vértice (2, −1), el círculo ámbar.',
   'Glosa: hay que evaluar. Saber la x del vértice no da la y.'),
  ('Como el mínimo es −1, negativo, la curva cruza el eje, baja y vuelve a cruzar. El gráfico lo enseña.',
   'Glosa: si el vértice hubiera sido positivo y el coeficiente de x² positivo, no habría raíces reales. Aquí sí las hay.'),
 ]),
('Desarrollar y comprobar',
 'Escribe f como polinomio y comprueba f(1), f(3) y f(0).',
 [
  ('(x−1)(x−3) = x² − 4x + 3.',
   'Glosa: −3x − x = −4x, y (−1)(−3) = +3.'),
  ('f(1) = 1 − 4 + 3 = 0. f(3) = 9 − 12 + 3 = 0.',
   'Glosa: las raíces sobreviven al desarrollo. Si no dan 0, te has equivocado al expandir.'),
  ('f(0) = 3, el término independiente. Es el corte vertical, no el vértice.',
   'Glosa: el vértice está en x = 2, no en x = 0.'),
  ('f(4) = 16 − 16 + 3 = 3, igual que f(0). La simetría respecto de x = 2 lo explica: 0 y 4 están a la misma distancia del eje.',
   'Glosa: 2−0 = 2 y 4−2 = 2. Por eso las alturas coinciden.'),
 ]),
('Ecuación y signo',
 'Resuelve x² − 4x + 3 = 0 y di el signo de f en el intervalo (1, 3).',
 [
  ('Ya está factorizada: (x−1)(x−3) = 0, soluciones 1 y 3.',
   'Glosa: puedes usar la fórmula general, pero aquí sobra: las raíces se ven.'),
  ('Prueba un punto de dentro, x = 2: f(2) = −1, negativo.',
   'Glosa: un solo punto interior basta para el signo en todo (1, 3), porque la parábola no corta el eje por medio.'),
  ('Fuera, x = 0: f(0) = 3, positivo. A la derecha de 3 también, por simetría o por x = 4.',
   'Glosa: el signo cambia en cada raíz simple.'),
  ('Lectura: la parábola está por debajo del eje solo entre las dos raíces, que es lo que muestra el vértice bajo el eje.',
   'Glosa: no digas que es negativa «porque abre hacia abajo». Abre hacia arriba y aun así tiene un tramo negativo.'),
 ]),
],
[
(1, 'Mueve las raíces',
 'g(x) = (x − 0)(x − 4) = x(x − 4). Halla raíces y vértice.',
 'Raíces 0 y 4. El vértice está en x = 2, la media. g(2) = 2·(2−4) = 2·(−2) = −4. Vértice (2, −4). El paso es el mismo que en el ejemplo: media de las raíces y sustitución. No reutilices el −1 de f; esa altura era de otras raíces, más juntas. Aquí la parábola baja más. Comprueba g(0) = 0 y g(4) = 0.',
 'e21a'),
(2, 'Coeficiente que no es 1',
 'h(x) = 2(x − 1)(x − 3). ¿Cambian las raíces? ¿Y la y del vértice?',
 'Las raíces siguen en 1 y 3, porque el factor 2 no se anula. El eje sigue en x = 2. Pero h(2) = 2·(−1) = −2, no −1. El vértice baja a (2, −2). El paso es no creer que un coeficiente positivo delante solo «estrecha» sin tocar la altura: multiplica todos los valores, también el del vértice. Las raíces se salvan precisamente porque lo que se multiplica es cero.',
 'e21b'),
(3, 'Sin raíces reales',
 'p(x) = x² + 1. ¿Dónde está el vértice y por qué no corta al eje horizontal?',
 'p(x) = x² + 1 es siempre al menos 1. El mínimo está en x = 0, p(0) = 1, vértice (0, 1), por encima del eje. No hay raíces reales: x² = −1 no tiene solución real. El paso es mirar el vértice antes de forzar una factorización que no existe. A diferencia del ejemplo, aquí no hay dos cortes que promediar; la simetría se lee porque no hay término en x, así que el eje es x = 0.',
 'e21c'),
],
[
('¿Cuáles son las raíces y el vértice de la parábola dibujada?',
 'Raíces x = 1 y x = 3, vértice (2, −1). Por qué: la forma (x−1)(x−3) se anula en 1 y en 3, el medio es 2 y f(2) = −1. Los tres puntos están marcados; el ámbar es el más bajo.'),
('¿Por qué f vale 3 en x = 0 y también en x = 4?',
 'Por la simetría respecto de x = 2. Por qué: 0 y 4 equidistan del eje, y al desarrollar f(0) = 3 y f(4) = 3. No es casualidad del término independiente solo: el 3 de f(0) se refleja al otro lado.'),
('¿Abrir hacia arriba implica que la función es positiva?',
 'No. Por qué: el coeficiente de x² es positivo, así que hay un mínimo, pero ese mínimo es −1, por debajo del eje. Entre las raíces la función es negativa. Positiva lo es fuera de [1, 3].'),
],
'Marca las tres',
'En el lienzo dibuja la parábola, señala (1, 0), (3, 0) y (2, −1) y escribe el signo entre las raíces.',
['Los cortes están en 1 y en 3. El vértice ámbar está en (2, −1), debajo del eje.',
 'La curva abre hacia arriba: el mínimo es el vértice, no un máximo.',
 'Ejemplo 1: la media de las raíces da la x, y hay que evaluar para la y.',
 'Ejemplo 2: x² − 4x + 3 coincide y f(0) = f(4) = 3.',
 'Ejemplo 3: dentro de (1, 3) el signo es negativo; no hace falta otra raíz.',
 'Un coeficiente 2 delante no mueve las raíces y sí la altura del vértice.',
 'En el laboratorio lee f(1), f(2) y f(3) antes de cambiar nada.'],
lab_title='Parábola con raíces 1 y 3')

print('L20 L21 en append')

# ---------- L22 ----------
fig22 = ejes(36, 270, 340, 30) + ejes(380, 270, 690, 30)
fig22 += path_fn(lambda x: 1/x, 0.45, 5, 30, lambda x: 50+x*52, lambda y: 250-y*70, stroke='#C4A15A')
fig22 += path_fn(lambda x: x+1, -1, 2, 12, lambda x: 430+(x+1)*48, lambda y: 250-y*36, stroke='#C4A15A')
fig22 += path_fn(lambda x: 5-x, 2, 5, 12, lambda x: 430+(x+1)*48, lambda y: 250-y*36, stroke='#8F9A72')
fig22 += '''
<circle cx="154" cy="215" r="6" fill="#E6E1D6"/>
<text x="160" y="205" fill="#E6E1D6" font-size="13">(2, 1/2)</text>
<circle cx="258" cy="232" r="5" fill="#E6E1D6"/>
<text x="200" y="224" fill="#E6E1D6" font-size="13">(4, 1/4)</text>
<circle cx="574" cy="142" r="6" fill="#C4A15A"/>
<text x="500" y="40" fill="#C4A15A" font-size="14">trozos: x+1 y 5−x</text>
<text x="50" y="24" fill="#C4A15A" font-size="14">y = 1/x</text>
<text x="520" y="160" fill="#E6E1D6" font-size="13">une en (2, 3)</text>
'''
build(22, 'Racionales, a trozos y <em>periódicas</em>', 'D.2 Racionales, a trozos y periódicas',
'1/x se dispara, y el trozo cambia de regla',
'A la izquierda, y = 1/x con los puntos (2, 1/2) y (4, 1/4): al doblar x, la altura se parte. A la derecha, una función a trozos que vale x+1 si x es menor que 2 y vale 5−x si x es mayor o igual que 2. En x = 2 las dos reglas dan 3 y la gráfica se une.',
['Evaluar 1/x y reconocer la asíntota en x = 0.','Aplicar la pieza correcta de una función a trozos.','Reconocer un periodo en un ejemplo numérico sencillo.'],
'''<h2>Tres maneras de no ser una recta</h2>
<p>Una racional sencilla como 1/x no está definida en 0: no se puede dividir entre cero. Cuando x se acerca a 0 por la derecha, 1/x se hace muy grande. Cuando x crece, 1/x se acerca a 0 sin llegar a tocar el eje. Eso es lo que hace la curva ámbar de la izquierda, con los dos puntos del ejemplo marcados.</p>
<p><span class="glosa">1/2 = 0,5 y 1/4 = 0,25 · asíntota vertical en x = 0 · función a trozos = regla distinta según el intervalo · en este ejemplo el cambio de regla está en x = 2 · periodo = longitud que se repite, como en y = sen, aquí lo vemos con una lista</span></p>
<p>La función a trozos de la derecha no es 1/x. Hay que leer la condición antes de sustituir. Si x = 0, como 0 es menor que 2, se usa x+1 y sale 1. Si x = 4, como 4 no es menor que 2, se usa 5−x y sale 1. Si x = 2, la segunda pieza incluye el igual y da 5−2 = 3; la primera, llegada por la izquierda, da 2+1 = 3. Coinciden, así que no hay salto.</p>
<p>Una función periódica repite valores cada cierto intervalo. La lista 1, 0, −1, 0 y otra vez 1, 0, −1, 0 tiene periodo 4: el término 5 coincide con el 1. No hace falta la fórmula del seno para ver el patrón y comprobarlo en tres posiciones.</p>
<table class="datos"><thead><tr><th>x</th><th>1/x</th><th>trozo</th></tr></thead>
<tbody>
<tr><td>2</td><td>1/2</td><td>3, por la pieza 5−x</td></tr>
<tr><td>4</td><td>1/4</td><td>1, por 5−4</td></tr>
<tr><td>0</td><td>no existe</td><td>1, por 0+1</td></tr>
<tr><td>1</td><td>1</td><td>2, por 1+1</td></tr>
</tbody></table>''',
'Curva 1/x con (2, 1/2) y (4, 1/4), y función a trozos que se une en (2, 3)', fig22,
[
('Dos puntos de 1/x',
 'Calcula 1/2 y 1/4 y explica qué pasa si intentas 1/0.',
 [
  ('1/2 = 0,5. Es el primer círculo de la curva izquierda, x = 2.',
   'Glosa: la altura es menor que 1 porque el denominador es mayor que 1.'),
  ('1/4 = 0,25. Al doblar x de 2 a 4, la altura pasa de 1/2 a la mitad.',
   'Glosa: es la propiedad 1/(2a) = (1/a)/2, visible en los dos círculos.'),
  ('1/0 no es un número. La función no tiene punto en x = 0; la curva se va hacia arriba al acercarse al eje.',
   'Glosa: no pongas infinito como si fuera un valor de la función. Di que no está definida.'),
  ('Comprueba un tercer punto, x = 1: 1/1 = 1, más alto que 0,5, como corresponde a estar más cerca del eje.',
   'Glosa: el orden de las alturas 1 > 1/2 > 1/4 sigue al orden inverso de los denominadores.'),
 ]),
('Elegir el trozo',
 'Para g(x) = x+1 si x es menor que 2, y g(x) = 5−x si x es mayor o igual que 2, calcula g(0), g(2) y g(4).',
 [
  ('x = 0 es menor que 2: g(0) = 0+1 = 1. No uses 5−0.',
   'Glosa: la condición se mira antes de la fórmula. Elegir la pieza equivocada es el error típico.'),
  ('x = 2 cumple el igual de la segunda pieza: g(2) = 5−2 = 3. El círculo ámbar de la derecha está ahí.',
   'Glosa: la primera pieza no incluye el 2. Aun así, por la izquierda también saldría 3.'),
  ('x = 4 usa 5−x: g(4) = 1. La rama verde baja desde (2, 3) hacia la derecha.',
   'Glosa: de 2 a 4 la expresión 5−x baja 2 unidades, de 3 a 1.'),
  ('Comprueba la unión: límite por la izquierda en 2 es 3, y el valor es 3. No hay salto que dibujar.',
   'Glosa: si las dos piezas no coincidieran, habría un círculo relleno y otro hueco. Aquí no.'),
 ]),
('Periodo 4',
 'La lista de una señal repite 1, 0, −1, 0. Comprueba que el lugar 5, el 6 y el 7 coinciden con el 1, el 2 y el 3.',
 [
  ('Lugares: 1→1, 2→0, 3→−1, 4→0, y el 5 vuelve a 1.',
   'Glosa: periodo 4 significa que avanzas 4 posiciones y el valor se repite.'),
  ('Lugar 6 = lugar 2 = 0. Lugar 7 = lugar 3 = −1.',
   'Glosa: restar el periodo las veces que haga falta: 6−4 = 2 y 7−4 = 3.'),
  ('Lugar 8 = lugar 4 = 0, y el 9 otra vez 1. El bloque 1, 0, −1, 0 se copia.',
   'Glosa: no es una sucesión aritmética; el salto no es constante y no debes usar 4n−1.'),
  ('Comprobación de tres sitios, como pide el hábito de la lección anterior: 5, 6 y 7 casan con 1, 2 y 3.',
   'Glosa: si el lugar 6 no hubiera sido 0, el periodo no sería 4.'),
 ]),
],
[
(1, 'Otro punto de la hipérbola',
 'Calcula 1/x en x = 5 y en x = −2. Di qué cambia con el signo.',
 '1/5 = 0,2, más pequeña que 1/4, así que la rama derecha sigue bajando hacia el eje. 1/(−2) = −0,5: el signo del resultado es el signo de x, porque el numerador es positivo. El punto (−2, −0,5) está en la otra rama, la que el gráfico de la izquierda no ha dibujado para no mezclarla con los trozos. El paso es no aplicar una pieza de g a la pregunta sobre 1/x: son funciones distintas, separadas en el SVG.',
 'e22a'),
(2, 'Trozo mal elegido',
 'Alguien calcula g(1) = 5−1 = 4. ¿Qué condición ha ignorado y cuál es el valor?',
 'x = 1 es menor que 2, luego toca la primera pieza: g(1) = 1+1 = 2, no 4. Ha usado 5−x fuera de su intervalo. El paso es subrayar la condición y tachar la otra fórmula antes de operar. En el gráfico, x = 1 cae en el tramo ámbar de la derecha, que sube hacia (2, 3), y la altura 2 está en esa subida. El 4 ni siquiera está en la imagen de los puntos que hemos calculado (1, 3 y 1).',
 'e22b'),
(3, '¿Hay salto si cambio el igual?',
 'Define h igual que g pero con la segunda pieza solo cuando x es mayor que 2, y en x = 2 pon h(2) = 0. ¿Sigue siendo continua la gráfica?',
 'Ahora h(2) = 0, mientras que al acercarte por la izquierda con x+1 llegas a 3, y por la derecha con 5−x también llegas a 3. El valor 0 queda aislado: hay un salto, o mejor un punto descolgado, en x = 2. El paso es comparar el valor que impones con el de las dos piezas vecinas. En g coincidían y el círculo ámbar está pegado a las dos ramas; en h habría que dibujar el punto (2, 0) separado. La continuidad no es automática por escribir dos fórmulas: depende de que en la frontera den lo mismo.',
 'e22c'),
],
[
('¿Cuánto vale 1/x en x = 2 y en x = 4?',
 '1/2 y 1/4. Por qué: son los dos círculos de la curva izquierda. Doblar el denominador parte la altura. En x = 0 la expresión no tiene valor, porque no se divide entre cero.'),
('¿Qué pieza se usa en x = 4 para la función de la derecha?',
 'La segunda, 5−x, y da 1. Por qué: 4 no es menor que 2, así que la regla x+1 no se aplica. En x = 2, que es la frontera, la pieza con el igual da 3 y coincide con llegar por la izquierda.'),
('¿Qué significa periodo 4 en la lista 1, 0, −1, 0?',
 'Que cada 4 lugares el valor se repite. Por qué: el lugar 5 vale lo mismo que el 1, el 6 lo mismo que el 2 y el 7 lo mismo que el 3. No es un salto constante, así que no se modela con una afín.'),
],
'Dos reglas',
'Inventa una función a trozos con cambio en x = 1, calcúlala en −1, 1 y 3, y dibújala en el lienzo junto a un esquema de 1/x.',
['Izquierda: 1/x pasa por (2, 1/2) y (4, 1/4). Derecha: dos trozos que se encuentran en (2, 3).',
 'No evalúes 1/0. No uses la pieza de la derecha para un x menor que 2.',
 'Ejemplo 1: 1/2 y 1/4, y el tercer punto 1/1 = 1.',
 'Ejemplo 2: g(0) = 1, g(2) = 3, g(4) = 1.',
 'Ejemplo 3: la lista de periodo 4 se comprueba en los lugares 5, 6 y 7.',
 'Si en la frontera las dos reglas no coinciden, el gráfico no se une.',
 'Racional, trozos y periodo son tres lecturas distintas.'],
None)

# ---------- L23 ----------
fig23 = ejes(40, 280, 340, 28) + ejes(390, 280, 700, 28)
fig23 += path_fn(lambda x: 2**x, 0, 4, 24, lambda x: 40+x*70, lambda y: 280-y*14)
fig23 += path_fn(lambda x: math.log2(x), 0.5, 8, 24, lambda x: 400+(x-1)*31, lambda y: 250-y*40, stroke='#8F9A72')
fig23 += '''
<circle cx="250" cy="168" r="6" fill="#E6E1D6"/>
<text x="200" y="155" fill="#E6E1D6" font-size="14">(3, 8)</text>
<circle cx="617" cy="130" r="6" fill="#E6E1D6"/>
<text x="500" y="110" fill="#E6E1D6" font-size="14">log2(8) = 3</text>
<text x="40" y="22" fill="#C4A15A" font-size="14">y = 2^x</text>
<text x="400" y="22" fill="#8F9A72" font-size="14">y = log2(x)</text>
'''
build(23, 'Exponenciales y <em>logarítmicas</em>', 'D.2 Exponenciales y logarítmicas',
'El 8 que es 2³, y el 3 que es su logaritmo',
'La curva ámbar es y = 2^x y pasa por (3, 8), porque 2³ = 8. La verde es el logaritmo en base 2: log2(8) = 3, el exponente que devuelve el 8 a la altura. Son inversas: cada una deshace a la otra.',
['Calcular potencias de 2 y situarlas en la exponencial.','Leer un logaritmo como exponente.','Usar que el logaritmo de un producto es la suma, con números concretos.'],
'''<h2>Crecer multiplicando, y la pregunta inversa</h2>
<p>La función exponencial y = 2^x multiplica por 2 cada vez que x aumenta una unidad. Pasa por (0, 1), porque 2⁰ = 1, y por (3, 8), el punto marcado. No es una recta: de x = 2 a x = 3 la altura pasa de 4 a 8, un salto mayor que el anterior.</p>
<p><span class="glosa">2³ = 8 · log₂(8) = 3 porque 2³ = 8 · log₂(2^x) = x · 2 elevado a log₂(8) vuelve a 8 · log₂(4·2) = log₂(4) + log₂(2)</span></p>
<p>El logaritmo en base 2 pregunta por el exponente. log₂(8) no es 8/2. Es 3, y por eso en la curva verde el punto que corresponde al resultado 8 tiene altura 3. Las dos gráficas cuentan la misma frase en orden contrario: «2 elevado a 3 es 8» y «el exponente que lleva de 2 a 8 es 3».</p>
<p>La propiedad útil no es decorativa. log₂(4·2) = log₂(8) = 3, y también log₂(4) + log₂(2) = 2 + 1 = 3. El logaritmo convierte el producto en suma. No convierte la suma en producto: log₂(4+2) = log₂(6) no es 2+1.</p>
<table class="datos"><thead><tr><th>x</th><th>2^x</th><th>lectura logarítmica</th></tr></thead>
<tbody>
<tr><td>0</td><td>1</td><td>log₂(1) = 0</td></tr>
<tr><td>2</td><td>4</td><td>log₂(4) = 2</td></tr>
<tr><td>3</td><td>8</td><td>log₂(8) = 3, el punto de las dos curvas</td></tr>
<tr><td>4</td><td>16</td><td>log₂(16) = 4</td></tr>
</tbody></table>''',
'Exponencial 2^x con el punto (3, 8) y logaritmo en base 2 de 8, que vale 3', fig23,
[
('El punto (3, 8)',
 'Comprueba que 2³ = 8 y sitúa el punto en la exponencial.',
 [
  ('2³ = 2·2·2 = 8. No es 2·3 = 6.',
   'Glosa: el exponente cuenta factores, no se multiplica por la base una sola vez.'),
  ('El punto es (3, 8): abscisa el exponente, ordenada el resultado. Es el círculo de la curva ámbar.',
   'Glosa: en y = 2^x la altura crece cada vez más deprisa; de 4 a 8 es el último tramo entero del dibujo.'),
  ('Un paso antes: 2² = 4. Un paso después: 2⁴ = 16, que ya se sale por arriba del recuadro con esta escala, pero la regla es la misma.',
   'Glosa: cada unidad de x duplica la altura anterior.'),
  ('Comprobación inversa: si la altura es 8, el exponente es 3. Esa frase es el logaritmo.',
   'Glosa: no cambies de curva todavía; primero cierra la potencia.'),
 ]),
('El mismo 8 en la otra curva',
 'Calcula log₂(8) y explica por qué el punto no es (3, 8) en la curva verde.',
 [
  ('log₂(8) es el exponente que da 8 con base 2. Como 2³ = 8, el logaritmo vale 3.',
   'Glosa: se lee «a qué hay que elevar 2», no «2 entre 8».'),
  ('En la curva verde la abscisa es el resultado (8) y la ordenada es el exponente (3).',
   'Glosa: por eso el círculo verde no está en las mismas coordenadas que el ámbar.'),
  ('Deshacer: 2 elevado a log₂(8) es 8, y log₂(2³) es 3.',
   'Glosa: son inversas. Cada una deshace el viaje de la otra.'),
  ('log₂(16) = 4 y log₂(4) = 2. La tabla de la lección se lee en las dos direcciones.',
   'Glosa: si tu logaritmo no cumple la potencia, está mal.'),
 ]),
('Producto que se vuelve suma',
 'Comprueba log₂(4·2) de las dos maneras.',
 [
  ('Dentro: 4·2 = 8 y log₂(8) = 3.',
   'Glosa: primero el producto, luego el logaritmo. Es la vía directa.'),
  ('Por la propiedad: log₂(4) + log₂(2) = 2 + 1 = 3.',
   'Glosa: el producto de dentro pasa a suma de logaritmos. Los factores 4 y 2 son potencias de la misma base.'),
  ('Las dos vías dan 3. La propiedad no ha cambiado el número; lo ha escrito de otra forma.',
   'Glosa: sirve cuando los factores son más cómodos que el producto, por ejemplo potencias de 10 en otra base.'),
  ('Contraste: log₂(4+2) = log₂(6), que no es 3. La propiedad no se aplica a las sumas.',
   'Glosa: el error clásico es repartir el logaritmo sobre una suma. Aquí se ve con números pequeños.'),
 ]),
],
[
(1, 'De 8 a 32',
 '¿Cuánto es 2⁵ y log₂(32)?',
 '2⁵ = 2³·2² = 8·4 = 32. El logaritmo en base 2 de 32 es el exponente 5. El paso es no multiplicar 2·5. Puedes encadenar desde el punto del gráfico: 8·2 = 16 y 16·2 = 32, dos duplicaciones más allá de x = 3. Comprueba al revés: 2⁵ = 32. En la curva exponencial el punto sería (5, 32), más alto que el recuadro; en la logarítmica, (32, 5).',
 'e23a'),
(2, 'Ecuación',
 'Resuelve 2^x = 16 y escribe la solución como logaritmo.',
 '16 = 2⁴, así que x = 4. También x = log₂(16). Las dos escrituras son la misma solución. El paso es igualar exponentes cuando las bases ya coinciden, o nombrar el logaritmo si todavía no has reconocido la potencia. Comprueba sustituyendo: 2⁴ = 16, que está en la tabla. No sirve x = 16/2 = 8, porque 2⁸ es 256, no 16.',
 'e23b'),
(3, 'Propiedad a ciegas',
 '¿Es verdad que log₂(6) = log₂(2) + log₂(4)? ¿Y log₂(8) = log₂(3) + log₂(5)?',
 'La primera es falsa: 2+4 = 6, pero la propiedad exige un producto, no una suma. log₂(2)+log₂(4) = 1+2 = 3 = log₂(8), no log₂(6). La segunda también es falsa: 3·5 = 15, no 8, así que log₂(3)+log₂(5) = log₂(15), distinto de log₂(8) = 3. El paso es mirar si lo de dentro es un producto de los argumentos que vas a sumar. En el ejemplo bueno, 4·2 sí era 8. Aquí ni la suma 2+4 ni el producto 3·5 reconstruyen el argumento que alguien ha puesto.',
 'e23c'),
],
[
('¿Qué punto de la exponencial corresponde a 2³?',
 '(3, 8). Por qué: el exponente 3 va en el eje horizontal y el resultado 8 en el vertical. 2·2·2 = 8, no 6. El círculo ámbar es ese punto, y un paso antes la altura es 4, no una recta.'),
('¿Por qué log₂(8) = 3 y no 4?',
 'Porque 2³ = 8, no porque 8 tenga un 4 escondido en 2⁴ = 16. Por qué: el logaritmo es el exponente exacto. 2⁴ ya se pasa a 16. En la curva verde, 8 está en el eje horizontal y la altura es 3.'),
('¿log₂(4·2) se puede separar?',
 'Sí, en log₂(4) + log₂(2) = 2+1 = 3, que es log₂(8). Por qué: el logaritmo de un producto es la suma de logaritmos. No hagas lo mismo con 4+2, porque eso no es el producto y log₂(6) no vale 3.'),
],
'Una potencia de tu fórmula',
'Escribe 2 elevado a un entero entre 1 y 6, el logaritmo inverso y una comprobación de la propiedad del producto. Dibújalo en el lienzo si te ayuda el esquema de las dos curvas.',
['Ámbar: 2^x pasa por (3, 8). Verde: log₂(8) = 3, con los ejes intercambiados en el significado.',
 'Son inversas. Cada comprobación vuelve a la potencia.',
 'Ejemplo 1: 2³ = 8, no 6.',
 'Ejemplo 2: el punto verde no tiene las mismas coordenadas que el ámbar.',
 'Ejemplo 3: log₂(4·2) = 2+1 = 3, y la suma 4+2 no entra en la propiedad.',
 'Para resolver 2^x = 16, x = 4.',
 'No repartas un logaritmo sobre una suma.'],
None)

# ---------- L24 ----------
fig24 = ejes(60, 260, 680, 30) + '''
<line x1="170" y1="78" x2="470" y2="234" stroke="#C4A15A" stroke-width="3"/>
<line x1="170" y1="234" x2="570" y2="130" stroke="#8F9A72" stroke-width="3"/>
<circle cx="370" cy="182" r="7" fill="#E6E1D6"/>
<text x="380" y="170" fill="#E6E1D6" font-size="15">(3, 2)</text>
<text x="300" y="70" fill="#C4A15A" font-size="14">2x + y = 8</text>
<text x="480" y="110" fill="#8F9A72" font-size="14">x − y = 1</text>
'''
build(24, 'Sistemas de <em>ecuaciones</em>', 'D.3 Sistemas de ecuaciones',
'Las dos rectas se cortan en (3, 2)',
'El sistema 2x + y = 8 y x − y = 1 tiene una sola solución: x = 3, y = 2. En el gráfico la recta ámbar es la primera y la verde la segunda. El círculo es el corte, el único punto que cumple las dos a la vez.',
['Resolver un sistema 2×2 por suma o por sustitución.','Comprobar la pareja en las dos ecuaciones.','Leer en el dibujo qué significa una solución, ninguna o infinitas.'],
'''<h2>Una pareja que tiene que servir para las dos rectas</h2>
<p>Cada ecuación del sistema es una recta. Una solución del sistema es un punto que está en las dos. Si las rectas se cortan en un solo punto, hay una solución. Si son paralelas distintas, ninguna. Si son la misma recta, infinitas.</p>
<p><span class="glosa">2x + y = 8 es la ámbar · x − y = 1 es la verde · sumarlas elimina y porque +y y −y se cancelan · la solución (3, 2) hay que meterla en las dos ecuaciones, no solo en la que acabas de despejar</span></p>
<p>Suma: (2x + y) + (x − y) = 8 + 1, es decir 3x = 9, luego x = 3. De la segunda, 3 − y = 1, así que y = 2. Sustituir en la primera: 2·3 + 2 = 8, que cierra. El punto (3, 2) es el círculo del gráfico, donde se cruzan los dos trazos.</p>
<p>No basta con que el punto cumpla una. (4, 0) está en la ámbar porque 8+0 = 8, pero en la verde 4 − 0 = 4, que no es 1. Por eso (4, 0) no es solución del sistema aunque sea un corte con el eje de la primera recta.</p>
<table class="datos"><thead><tr><th>Punto</th><th>¿Cumple 2x + y = 8?</th><th>¿Cumple x − y = 1?</th></tr></thead>
<tbody>
<tr><td>(3, 2)</td><td>6+2 = 8, sí</td><td>3−2 = 1, sí</td></tr>
<tr><td>(4, 0)</td><td>8+0 = 8, sí</td><td>4−0 = 4, no</td></tr>
<tr><td>(1, 0)</td><td>2+0 = 2, no</td><td>1−0 = 1, sí</td></tr>
</tbody></table>''',
'Corte de las rectas 2x + y = 8 y x − y = 1 en el punto (3, 2)', fig24,
[
('Suma que elimina y',
 'Resuelve el sistema del gráfico por suma y comprueba en las dos ecuaciones.',
 [
  ('Suma miembro a miembro: 2x + y + x − y = 8 + 1. Queda 3x = 9.',
   'Glosa: +y y −y se anulan. Por eso se elige la suma y no un apaño.'),
  ('x = 3. Sustituye en x − y = 1: 3 − y = 1, luego y = 2.',
   'Glosa: puedes usar cualquiera de las dos ecuaciones; la segunda es más corta.'),
  ('Comprueba en la primera: 2·3 + 2 = 8. Y en la segunda: 3 − 2 = 1.',
   'Glosa: las dos tienen que cerrar. Si solo miras una, puedes arrastrar un fallo de la otra.'),
  ('El punto (3, 2) es el círculo donde la ámbar y la verde se cortan. No hay otro corte.',
   'Glosa: dos rectas no paralelas se cortan una sola vez.'),
 ]),
('Sustitución, el mismo punto',
 'Despeja y en la segunda ecuación y sustituye en la primera.',
 [
  ('De x − y = 1 sale y = x − 1.',
   'Glosa: al pasar −y, el 1 cambia de lado con x. y no es 1 − x.'),
  ('Mete y en la primera: 2x + (x − 1) = 8. Entonces 3x − 1 = 8, 3x = 9, x = 3.',
   'Glosa: el mismo 3x = 9 de antes. Los dos métodos coinciden.'),
  ('y = 3 − 1 = 2. Otra vez (3, 2).',
   'Glosa: si el despeje hubiera sido y = 1 − x, en x = 3 saldría y = −2 y la primera ecuación no cerraría.'),
  ('Sustituir no es un método distinto en el resultado: es otra forma de obligar a que el punto esté en las dos rectas.',
   'Glosa: el gráfico no cambia porque cambies de método.'),
 ]),
('Un punto que solo está en una',
 'Muestra con números que (4, 0) no es solución, y di en qué recta sí está.',
 [
  ('Primera ecuación: 2·4 + 0 = 8. Sí está en la ámbar. Es su corte con el eje horizontal, porque y = 8 − 2x da y = 0 cuando x = 4.',
   'Glosa: cumplir una ecuación significa estar en esa recta, no en el sistema.'),
  ('Segunda: 4 − 0 = 4, y 4 no es 1. No está en la verde.',
   'Glosa: por eso no es el círculo del cruce.'),
  ('(1, 0) hace lo contrario: 1 − 0 = 1, está en la verde, pero 2·1 + 0 = 2 no es 8.',
   'Glosa: cada eje puede cortar una recta en un punto que la otra no quiere.'),
  ('La solución del sistema es la intersección, no un corte con el eje. Aquí solo (3, 2).',
   'Glosa: en otros sistemas la solución puede caer sobre un eje, pero se comprueba igual, en las dos ecuaciones.'),
 ]),
],
[
(1, 'Cambia el término',
 'Resuelve 2x + y = 8 y x − y = 4. Compara con (3, 2).',
 'Al sumar, 3x = 12 y x = 4. Entonces 4 − y = 4, así que y = 0. La solución es (4, 0). El paso es rehacer la suma: el 1 de la segunda ecuación ha pasado a ser 4, y 8+4 = 12, no 9. Justo (4, 0) era el punto que en el sistema original estaba en la ámbar y no en la verde. Al cambiar la verde para que pida x − y = 4, ese punto entra y (3, 2) sale: 3−2 = 1, que ya no es 4. Comprueba 2·4 + 0 = 8.',
 'e24a'),
(2, 'Paralelas',
 '¿Qué ocurre con 2x + y = 8 y 2x + y = 3?',
 'Restando, 0 = 5, que es imposible. No hay ningún (x, y) que cumpla las dos, porque la misma expresión 2x + y no puede valer 8 y 3 a la vez. Son rectas paralelas: misma pendiente (de y = −2x + 8 y y = −2x + 3) y distinta ordenada en el origen. El paso es reconocer 0 = número distinto de cero como «ninguna solución», no como x = 0. En el gráfico del ejemplo las pendientes no coinciden (una baja con pendiente −2 y la otra sube con pendiente 1), por eso sí se cortan.',
 'e24b'),
(3, 'Sustituye al revés',
 'Comprueba (3, 2) en el orden inverso: primero la segunda ecuación y después la primera, escribiendo las operaciones.',
 'Segunda: 3 − 2 = 1, que es el término independiente. Primera: 2·3 = 6 y 6+2 = 8. El orden de la comprobación no importa; importa no saltarse ninguna. El paso evita el error de dar por bueno x = 3 solo porque 3x = 9, sin haber recuperado y. Si y hubiera salido 1 por un despiste, la segunda daría 3−1 = 2, que no es 1, y la primera 6+1 = 7, que no es 8. Las dos fallarían o, según el despiste, fallaría una. Por eso se miran las dos.',
 'e24c'),
],
[
('¿Dónde se cortan las dos rectas del gráfico?',
 'En (3, 2). Por qué: al sumar las ecuaciones, 3x = 9 y x = 3; de x − y = 1 sale y = 2. Ese punto cumple 6+2 = 8 y 3−2 = 1. Es el único corte porque las rectas no son paralelas.'),
('¿Por qué (4, 0) no vale?',
 'Cumple la primera ecuación y no la segunda: 4 − 0 = 4, no 1. Por qué: estar en una recta no es estar en el sistema. El sistema pide las dos condiciones a la vez.'),
('¿Qué señalaría una resta que da 0 = 5?',
 'Que no hay solución. Por qué: las dos ecuaciones se contradicen. En el ejemplo eso no pasa: la suma da 3x = 9, que sí tiene solución. 0 = 5 aparecería si las rectas fueran paralelas distintas, como 2x + y = 8 y 2x + y = 3.'),
],
'Otro cruce',
'Escribe un sistema propio de dos rectas, resuélvelo y marca el corte en el lienzo. Comprueba el punto en las dos ecuaciones.',
['Ámbar: 2x + y = 8. Verde: x − y = 1. El círculo es (3, 2).',
 'Sumar cancela y y deja 3x = 9.',
 'Ejemplo 1: x = 3, y = 2, y las dos ecuaciones cierran.',
 'Ejemplo 2: despejar y = x − 1 lleva al mismo punto.',
 'Ejemplo 3: (4, 0) está solo en la ámbar.',
 'Si al operar sale 0 = 5, no inventes una solución.',
 'La comprobación entra en las dos rectas, no en una.'],
None)

# ---------- L25 ----------
fig25 = ejes(80, 280, 660, 24) + '''
<polygon points="100,270 420,270 100,70" fill="#3a3424" stroke="#C4A15A" stroke-width="3"/>
<circle cx="180" cy="220" r="6" fill="#E6E1D6"/>
<circle cx="340" cy="120" r="6" fill="#8F9A72"/>
<line x1="100" y1="70" x2="420" y2="270" stroke="#C4A15A" stroke-width="2"/>
<text x="150" y="240" fill="#E6E1D6" font-size="14">(1, 1) dentro</text>
<text x="350" y="110" fill="#8F9A72" font-size="14">(3, 3) fuera</text>
<text x="430" y="80" fill="#C4A15A" font-size="15">x + y = 4</text>
<text x="430" y="120" fill="#9A9488" font-size="14">región: x ≥ 0, y ≥ 0, x + y ≤ 4</text>
'''
build(25, 'Inecuaciones y <em>sistemas</em>', 'D.3 Inecuaciones y sistemas de inecuaciones',
'El triángulo de lo que sí cumple',
'El sistema x ≥ 0, y ≥ 0 y x + y ≤ 4 es el triángulo del gráfico, de vértices (0, 0), (4, 0) y (0, 4). El punto (1, 1) suma 2 y está dentro. El punto (3, 3) suma 6 y se queda fuera, al otro lado de la frontera x + y = 4.',
['Representar una inecuación como semiplano.','Cortar varios semiplanos y quedarte con la región común.','Probar un punto de dentro y un punto de fuera con los números.'],
'''<h2>La frontera es una recta; la solución es una región</h2>
<p>Una ecuación como x + y = 4 es la recta frontera. La inecuación x + y ≤ 4 se queda con un lado de esa recta, el semiplano, incluidos los puntos de la propia recta porque el signo es ≤ y no &lt; estricto. Añadir x ≥ 0 e y ≥ 0 recorta el primer cuadrante.</p>
<p><span class="glosa">semiplano = una de las dos mitades en que la recta parte el papel · la región solución es la intersección de los semiplanos · (1, 1) es un testigo interior · (3, 3) es un testigo exterior · los vértices del triángulo son (0, 0), (4, 0) y (0, 4)</span></p>
<p>El triángulo sombreado es exactamente esa intersección. Su lado inclinado es la frontera ámbar. Cualquier punto de dentro cumple las tres desigualdades a la vez. Cualquier punto al otro lado de la frontera incumple x + y ≤ 4, aunque tenga coordenadas positivas.</p>
<p>Para decidir el lado sin dibujar, se prueba un punto que no esté en la frontera. El origen (0, 0): 0+0 ≤ 4 es verdad, y el origen está en la región (es un vértice). El punto (3, 3): 6 ≤ 4 es falso, y el círculo verde queda fuera. Esa prueba es la que manda si el dibujo duda.</p>
<table class="datos"><thead><tr><th>Punto</th><th>x ≥ 0</th><th>y ≥ 0</th><th>x + y ≤ 4</th><th>¿Región?</th></tr></thead>
<tbody>
<tr><td>(1, 1)</td><td>sí</td><td>sí</td><td>2 ≤ 4, sí</td><td>dentro</td></tr>
<tr><td>(4, 0)</td><td>sí</td><td>sí</td><td>4 ≤ 4, sí</td><td>vértice, en la frontera</td></tr>
<tr><td>(3, 3)</td><td>sí</td><td>sí</td><td>6 ≤ 4, no</td><td>fuera</td></tr>
<tr><td>(−1, 1)</td><td>no</td><td>sí</td><td>0 ≤ 4, sí</td><td>fuera</td></tr>
</tbody></table>''',
'Semiplano x + y ≤ 4 en el primer cuadrante: (1, 1) dentro y (3, 3) fuera', fig25,
[
('El triángulo',
 'Describe la región x ≥ 0, y ≥ 0, x + y ≤ 4 y nombra sus vértices.',
 [
  ('x ≥ 0 es el semiplano a la derecha del eje vertical. y ≥ 0 es el de encima del eje horizontal. Juntos, el primer cuadrante.',
   'Glosa: incluir el igual significa que los ejes forman parte de la región, no solo el interior.'),
  ('x + y ≤ 4 se queda con el lado del origen, porque 0+0 ≤ 4. La frontera es la recta que une (4, 0) y (0, 4).',
   'Glosa: el test del origen elige el lado. Sin ese test, el sombreado puede caer al revés.'),
  ('La intersección es el triángulo de vértices (0, 0), (4, 0) y (0, 4), el polígono del gráfico.',
   'Glosa: cada vértice es el cruce de dos fronteras y cumple la tercera.'),
  ('(4, 0): 4+0 = 4, cumple el igual. Está incluido. Un punto como (4,1) ya suma 5 y se sale.',
   'Glosa: la frontera entra; lo que queda más allá, no.'),
 ]),
('Dos testigos',
 'Comprueba (1, 1) y (3, 3) en las tres inecuaciones.',
 [
  ('(1, 1): 1 ≥ 0, 1 ≥ 0 y 1+1 = 2 ≤ 4. Las tres sí. Es el círculo claro, dentro del triángulo.',
   'Glosa: hay que mirar las tres. Con solo la suma no sabrías si estás en el primer cuadrante.'),
  ('(3, 3): las coordenadas son positivas, pero 3+3 = 6, y 6 ≤ 4 es falso.',
   'Glosa: una sola desigualdad fallida saca el punto de la región.'),
  ('Por eso el círculo verde está al otro lado de la recta, aunque el dibujo lo deje cerca.',
   'Glosa: cerca no cuenta. La frontera es nítida: suma 4.'),
  ('Un punto de la frontera, (2, 2): 2+2 = 4 ≤ 4, sí entra. El signo es ≤, no &lt;.',
   'Glosa: si el enunciado dijera &lt;, (2, 2) quedaría fuera y la frontera se dibujaría discontinua.'),
 ]),
('Añadir otra condición',
 'Añade y ≤ 1 al sistema. ¿Sigue (1, 1) dentro? ¿Qué le pasa al triángulo?',
 [
  ('(1, 1): y = 1 cumple y ≤ 1, y ya cumplía el resto. Sigue dentro, ahora en la nueva frontera.',
   'Glosa: añadir una condición no echa a quien ya la cumple; recorta a los demás.'),
  ('(0, 4) tiene y = 4, que no es ≤ 1. Ese vértice se pierde.',
   'Glosa: el triángulo original queda cortado por la horizontal y = 1.'),
  ('La nueva región es un cuadrilátero (o un triángulo más bajo, según cuentes) con cima y = 1, desde x = 0 hasta x = 3, porque x + 1 ≤ 4 implica x ≤ 3.',
   'Glosa: en y = 1 la frontera inclinada corta en x = 3.'),
  ('(3, 3) sigue fuera. Una condición nueva no puede hacer verdadero un 6 ≤ 4.',
   'Glosa: las condiciones se acumulan; no se elige la que más convenga.'),
 ]),
],
[
(1, 'Punto en el eje',
 '¿Está (0, 4) en la región del gráfico? ¿Y (0, 5)?',
 '(0, 4) cumple x = 0, y = 4 ≥ 0 y 0+4 = 4 ≤ 4. Es un vértice, así que está, en la frontera. (0, 5) cumple los ejes pero 5 ≤ 4 es falso: está en el eje vertical, justo por encima del triángulo, fuera. El paso es no dar por bueno todo el eje por el hecho de que x sea 0. La suma también limita. Comprueba cada desigualdad por separado y exige que todas sean verdaderas.',
 'e25a'),
(2, 'Cambia el sentido',
 'Describe, sin dibujar primero, el semiplano x + y ≥ 4. ¿Contiene al origen?',
 'La frontera es la misma recta. El sentido ≥ se queda con el otro lado, el que no contiene al origen, porque 0+0 ≥ 4 es falso. (3, 3) sí entra, porque 6 ≥ 4. El paso es repetir el test del punto y no dar la vuelta al sombreado «a ojo». Si además pides x ≥ 0 e y ≥ 0, la región ya no es el triángulo acotado: es infinita, todo el primer cuadrante que queda por encima de la recta. El triángulo del gráfico corresponde al ≤, no al ≥.',
 'e25b'),
(3, 'Estricto',
 'Si la condición fuera x + y &lt; 4, ¿el punto (4, 0) seguiría en la región?',
 'No. 4 no es estrictamente menor que 4. (4, 0) está en la frontera y el signo &lt; la excluye. (1, 1) sigue dentro, porque 2 &lt; 4. El paso es leer el igual del símbolo antes de incluir vértices. En el dibujo, la frontera pasaría a ser una línea discontinua y los vértices (4, 0) y (0, 4) se vaciarían; (0, 0) se quedaría porque 0 &lt; 4. El gráfico de la lección usa ≤, así que esos vértices están pintados como parte de la solución.',
 'e25c'),
],
[
('¿Qué desigualdades describe el triángulo del gráfico?',
 'x ≥ 0, y ≥ 0 y x + y ≤ 4. Por qué: es el primer cuadrante recortado por la recta que une (4, 0) y (0, 4), del lado del origen. Los vértices son esos dos y el (0, 0).'),
('¿Por qué (1, 1) está dentro y (3, 3) no?',
 '(1, 1) suma 2, que es ≤ 4, y las coordenadas son positivas. (3, 3) suma 6, que ya no es ≤ 4. Por qué: basta una desigualdad falsa para salir de la intersección. El color del punto en el SVG lo separa, pero la decisión es la cuenta.'),
('¿El origen sirve para elegir el semiplano?',
 'Sí, si no está sobre la frontera. Por qué: 0+0 ≤ 4 es verdadero, luego el semiplano de x + y ≤ 4 es el que contiene al origen. Si la recta pasara por el origen, habría que probar otro punto.'),
],
'Recorta',
'Dibuja en el lienzo el triángulo del ejemplo, marca (1, 1) y (3, 3) y escribe al lado qué desigualdad falla en el segundo.',
['El polígono es x ≥ 0, y ≥ 0, x + y ≤ 4. Dentro, (1, 1). Fuera, (3, 3).',
 'La frontera inclinada entra porque el signo es menor o igual.',
 'Ejemplo 1: los vértices son (0, 0), (4, 0) y (0, 4).',
 'Ejemplo 2: 2 ≤ 4 pasa y 6 ≤ 4 no pasa.',
 'Ejemplo 3: añadir y ≤ 1 recorta el vértice (0, 4) y deja a (1, 1).',
 'No des por buena una sola desigualdad.',
 'Si el símbolo pierde el igual, la frontera deja de ser solución.'],
None)

# ---------- L26 ----------
write_lab(26, 'z en los vértices', '''
<div class="panel">
<p>Región del ejemplo. z = 3x + 2y. Pulsa un vértice.</p>
<button type="button" data-x="0" data-y="0"> (0, 0) </button>
<button type="button" data-x="4" data-y="0"> (4, 0) </button>
<button type="button" data-x="4" data-y="2"> (4, 2) </button>
<button type="button" data-x="1" data-y="5"> (1, 5) </button>
<button type="button" data-x="0" data-y="5"> (0, 5) </button>
<div class="out" id="out"></div>
<canvas id="c" width="640" height="240"></canvas>
</div>
<script>
function dib(mx,my){
  var cv=document.getElementById('c'), ctx=cv.getContext('2d');
  ctx.fillStyle='#12100e'; ctx.fillRect(0,0,640,240);
  var pts=[[0,0],[4,0],[4,2],[1,5],[0,5]];
  function X(x){return 80+x*70;} function Y(y){return 210-y*32;}
  ctx.beginPath(); pts.forEach(function(p,i){ if(i===0) ctx.moveTo(X(p[0]),Y(p[1])); else ctx.lineTo(X(p[0]),Y(p[1])); }); ctx.closePath();
  ctx.fillStyle='#3a3424'; ctx.fill(); ctx.strokeStyle='#C4A15A'; ctx.stroke();
  pts.forEach(function(p){
    ctx.beginPath(); ctx.arc(X(p[0]),Y(p[1]),5,0,6.3);
    ctx.fillStyle=(p[0]===mx&&p[1]===my)?'#E6E1D6':'#C4A15A'; ctx.fill();
  });
  document.getElementById('out').textContent='En ('+mx+', '+my+'), z = '+(3*mx+2*my);
}
document.querySelectorAll('button[data-x]').forEach(function(b){
  b.onclick=function(){dib(+b.getAttribute('data-x'), +b.getAttribute('data-y'));};
});
dib(4,2);
</script>
''')
fig26 = '''
<polygon points="90,280 410,280 410,200 170,80 90,80" fill="#3a3424" stroke="#C4A15A" stroke-width="3"/>
<circle cx="90" cy="280" r="6" fill="#E6E1D6"/>
<circle cx="410" cy="280" r="6" fill="#E6E1D6"/>
<circle cx="410" cy="200" r="8" fill="#C4A15A"/>
<circle cx="170" cy="80" r="6" fill="#E6E1D6"/>
<circle cx="90" cy="80" r="6" fill="#E6E1D6"/>
<line x1="70" y1="300" x2="480" y2="300" stroke="#9A9488" stroke-width="1.5"/>
<line x1="70" y1="300" x2="70" y2="40" stroke="#9A9488" stroke-width="1.5"/>
<text x="20" y="284" fill="#E6E1D6" font-size="13">z=0</text>
<text x="420" y="284" fill="#E6E1D6" font-size="13">(4,0) z=12</text>
<text x="420" y="190" fill="#C4A15A" font-size="14">(4,2) z=16</text>
<text x="180" y="74" fill="#E6E1D6" font-size="13">(1,5) z=13</text>
<text x="20" y="74" fill="#E6E1D6" font-size="13">(0,5) z=10</text>
<text x="460" y="120" fill="#C4A15A" font-size="15">óptimo z = 16</text>
'''
build(26, 'Programación <em>lineal</em>', 'D.2 Programación lineal',
'El máximo no está en el centro',
'Se maximiza z = 3x + 2y con x ≥ 0, y ≥ 0, x ≤ 4, y ≤ 5 y x + y ≤ 6. La región es el polígono de vértices (0, 0), (4, 0), (4, 2), (1, 5) y (0, 5). El máximo de z en una región poligonal se alcanza en un vértice: aquí (4, 2), con z = 16.',
['Traducir las restricciones a una región.','Hallar los vértices como cortes de las fronteras.','Evaluar z en cada vértice y elegir el óptimo.'],
'''<h2>Evaluar en las esquinas</h2>
<p>En un problema lineal la función objetivo z = 3x + 2y es un plano inclinado, y la región factible es un polígono. El mayor valor no se esconde en el interior: está en algún vértice. Por eso se listan las esquinas, se calcula z en cada una y se compara.</p>
<p><span class="glosa">factible = cumple todas las restricciones · vértice = corte de dos fronteras que además cumple las demás · z(4, 2) = 3·4 + 2·2 = 16 · las otras esquinas dan 0, 12, 13 y 10</span></p>
<p>Las restricciones x ≤ 4 y x + y ≤ 6 se cortan cuando x = 4 e y = 2, porque 4 + y = 6. Ese punto cumple y ≤ 5 e y ≥ 0. Es el círculo ámbar. y = 5 y x + y = 6 se cortan en (1, 5), que cumple x ≤ 4. El resto de esquinas son los cortes con los ejes y con y = 5 o x = 0: (0, 0), (4, 0) y (0, 5).</p>
<p>z premia más a x (coeficiente 3) que a y (coeficiente 2). Por eso el óptimo se va hacia la derecha, a x = 4, y sube en y solo hasta donde la suma lo permite, y = 2. Subir hasta y = 5 obliga a bajar x a 1 y z baja a 13.</p>
<table class="datos"><thead><tr><th>Vértice</th><th>z = 3x + 2y</th></tr></thead>
<tbody>
<tr><td>(0, 0)</td><td>0</td></tr>
<tr><td>(4, 0)</td><td>12</td></tr>
<tr><td>(4, 2)</td><td>16, máximo</td></tr>
<tr><td>(1, 5)</td><td>13</td></tr>
<tr><td>(0, 5)</td><td>10</td></tr>
</tbody></table>''',
'Polígono factible con vértices etiquetados y óptimo z = 16 en (4, 2)', fig26,
[
('Los cinco vértices',
 'Justifica cada esquina del polígono con las restricciones x ≥ 0, y ≥ 0, x ≤ 4, y ≤ 5, x + y ≤ 6.',
 [
  ('(0, 0) es el origen, corte de x = 0 e y = 0. Cumple el resto: 0 ≤ 4, 0 ≤ 5 y 0 ≤ 6.',
   'Glosa: un corte de dos fronteras solo es vértice factible si no se sale de las otras.'),
  ('(4, 0): x = 4 e y = 0. Suma 4 ≤ 6, y = 0 ≤ 5.',
   'Glosa: está en la base del polígono, a la derecha.'),
  ('(4, 2): x = 4 y x + y = 6, luego y = 2. Además 2 ≤ 5. Es el ámbar.',
   'Glosa: si y saliera mayor que 5, este corte no valdría y habría que mirar x = 4 con y = 5.'),
  ('(1, 5): y = 5 y x + y = 6, luego x = 1, y 1 ≤ 4. (0, 5): x = 0 e y = 5, suma 5 ≤ 6.',
   'Glosa: cinco esquinas, no cuatro. Olvidar (4, 2) o (1, 5) cambia el óptimo.'),
 ]),
('Evaluar z',
 'Calcula z = 3x + 2y en los cinco vértices y señala el máximo.',
 [
  ('(0, 0): 0. (4, 0): 3·4 + 0 = 12. (0, 5): 0 + 2·5 = 10.',
   'Glosa: en los ejes se anula uno de los dos sumandos.'),
  ('(4, 2): 3·4 + 2·2 = 12 + 4 = 16.',
   'Glosa: es el mayor de la tabla del SVG.'),
  ('(1, 5): 3·1 + 2·5 = 3 + 10 = 13, menor que 16.',
   'Glosa: más coordenada y no compensa el coeficiente 3 de la x que se pierde.'),
  ('Máximo 16 en (4, 2). Mínimo 0 en (0, 0), por si el enunciado pidiera minimizar: también está en un vértice.',
   'Glosa: el método de los vértices vale para el máximo y para el mínimo.'),
 ]),
('Por qué no el centro',
 'Calcula z en un punto interior, por ejemplo (2, 2), y compáralo con 16.',
 [
  ('(2, 2) cumple x ≤ 4, y ≤ 5 y 2+2 ≤ 6. Es factible.',
   'Glosa: interior no significa óptimo. Solo significa permitido.'),
  ('z(2, 2) = 6 + 4 = 10, por debajo de 16 y también de 12 y de 13.',
   'Glosa: quedarse en medio desaprovecha el coeficiente de x.'),
  ('Moverse desde (2, 2) hacia la derecha aumenta z en 3 por cada unidad de x, hasta chocar con x = 4 o con la suma.',
   'Glosa: el gradiente empuja al borde. Por eso se buscan esquinas, no el centro del polígono.'),
  ('En el borde x = 4, entre y = 0 (z = 12) e y = 2 (z = 16), z sube con y. El mejor de ese lado es la esquina alta, (4, 2).',
   'Glosa: dentro de un lado, el óptimo de una función lineal está en un extremo del lado.'),
 ]),
],
[
(1, 'Minimizar',
 'Con la misma región y z = 3x + 2y, ¿dónde está el mínimo?',
 'En la tabla, el menor valor es 0, en (0, 0). No hace falta otra cuenta: los cinco vértices ya están evaluados y 0 es el más pequeño. El paso es no cambiar de región al cambiar de pregunta. Minimizar y maximizar comparten esquinas; cambia cuál eliges. Si la función fuera z = −3x − 2y, los signos darían la vuelta y el mínimo de aquella sería el máximo de esta, pero aquí z es la del enunciado y el mínimo es el origen.',
 'e26a'),
(2, 'Otra objetivo',
 'Maximiza w = x + 4y en la misma región, evaluando vértices.',
 'w(0,0) = 0, w(4,0) = 4, w(4,2) = 4+8 = 12, w(1,5) = 1+20 = 21, w(0,5) = 20. El máximo pasa a (1, 5), con w = 21. El paso es no reutilizar (4, 2) solo porque ganaba con z. El coeficiente de y ahora es 4, mayor que el de x, y el óptimo se va al vértice más alto. Comprueba que (1, 5) sigue siendo factible: lo era antes y la región no ha cambiado.',
 'e26b'),
(3, 'Vértice falso',
 '¿Es (4, 5) un vértice factible? Calcula la suma y di qué restricción falla.',
 'x = 4 e y = 5 cumplen las cotas sueltas, pero x + y = 9, y 9 ≤ 6 es falso. No está en el polígono. El paso es contrastar todas las restricciones, no solo las que definen «la esquina visual» de las cotas. Si lo metieras en la tabla, z valdría 12+10 = 22, mayor que 16, y estarías maximizando fuera de la región, que no es una solución del problema. El ámbar (4, 2) es precisamente hasta dónde deja subir y cuando x ya vale 4.',
 'e26c'),
],
[
('¿Dónde se alcanza el máximo de z = 3x + 2y?',
 'En (4, 2), con z = 16. Por qué: es el mayor valor entre los cinco vértices factibles (0, 12, 16, 13 y 10). En una región poligonal con objetivo lineal el óptimo está en un vértice, así que no hace falta mirar el interior.'),
('¿Por qué (4, 5) no vale, si x = 4 e y = 5 están permitidos por separado?',
 'Porque juntos suman 9 y la restricción x + y ≤ 6 no se cumple. Por qué: todas las desigualdades son obligatorias a la vez. El polígono se corta en (4, 2) y en (1, 5), no en (4, 5).'),
('Si el objetivo pasa a ser x + 4y, ¿se mantiene el óptimo?',
 'No: pasa a (1, 5). Por qué: hay que reevaluar. w(1, 5) = 21 y w(4, 2) = 12. El vértice ganador depende de los coeficientes, no solo de la forma del polígono.'),
],
'Cambia el premio',
'Copia el polígono en el lienzo, anota z en cada vértice y marca (4, 2). Después prueba en el laboratorio el vértice (1, 5).',
['Cinco esquinas. El ámbar (4, 2) da z = 16, por encima de 12, 13, 10 y 0.',
 'z = 3x + 2y premia más cada unidad de x.',
 'Ejemplo 1: (4, 2) nace de x = 4 y x + y = 6; (1, 5) nace de y = 5 y la suma.',
 'Ejemplo 2: la tabla ordena el máximo en 16 y el mínimo en 0.',
 'Ejemplo 3: un interior como (2, 2) solo llega a z = 10.',
 'No evalúes (4, 5): suma 9 y no es factible.',
 'Si cambias la función, repite la tabla; no heredes el vértice.'],
lab_title='z en los vértices')

assert_untouched(SNAP)
print('L15-L26 hechas; protegidas intactas')
