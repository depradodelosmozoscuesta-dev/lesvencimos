# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'/workspace/lesvencimos/staging/bach1/mates-gen/_gen')
from chrome import write_dense, ej

def S(title, inner):
    return f'<div class="figura-svg"><svg viewBox="0 0 720 240" role="img"><title>{title}</title><rect width="720" height="240" fill="#161512"/>{inner}</svg></div>'

write_dense(19,'Patrones y <em>generalización</em>','D.1 Patrones','De lo concreto a la fórmula',
'CyL: generalización de patrones numéricos y geométricos hacia expresiones algebraicas.',
['Describir un patrón en palabras y en tabla.','Proponer una fórmula para el término n-ésimo.','Comprobar la fórmula en varios valores.'],
f'''<section class="bloque-cuerpo">
<h2>Método</h2>
<p>1) Observa. 2) Tabla (n | a_n). 3) Hipótesis (lineal, cuadrática…). 4) Comprueba con un término no usado. 5) Explica por qué encaja.</p>
{S('Triángulos','''
<text x="40" y="50" fill="#E6E1D6">Puntos: 1, 3, 6, 10… → a_n = n(n+1)/2</text>
<text x="40" y="120" fill="#9A9488">Diferencias: +2,+3,+4 → sugiere cuadrático</text>
''')}
<h2>Ejemplo 1 — aritmética</h2>
<ol class="pasos"><li>2,5,8,11… diferencia +3 → a_n=2+3(n−1)=3n−1.</li><li>Comprueba n=4: 11.</li></ol>
<h2>Ejemplo 2 — cuadrados</h2>
<ol class="pasos"><li>1,4,9,16 → a_n=n².</li></ol>
<h2>Ejemplo 3 — bordes</h2>
<ol class="pasos"><li>Cuadrícula n×n: perímetro de celdas exteriores 4(n−1) si n≥2.</li></ol>
{ej(1,'Fórmula','7,10,13,16… término general.','a_n=7+3(n−1)=3n+4. Comprueba n=1 → 7.','e19a')}
{ej(2,'Triangular','10.º triangular.','10·11/2=55.','e19b')}
{ej(3,'Trampa','¿Basta ver 3 términos para afirmar n²?','No: conviene comprobar más y justificar la estructura.','e19c')}
{ej(4,'Geométrico','2,6,18,54… razón.','×3; a_n=2·3^{{n−1}}.','e19d')}
<canvas id="lienzo19" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo19">Borrar</button></div>
</section>''',
[('2,5,8,11','3n−1'),('1,4,9,16','n²'),('Comprobar','con un n nuevo')],
'Patrón tuyo','Inventa 5 términos; escribe a_n; dibuja la figura que lo motiva.')

write_dense(20,'Funciones <em>afines</em>','D.2/D.4 Afines','Rectas que modelan',
'CyL: funciones afines; modelización y propiedades.',
['Identificar f(x)=mx+n.','Interpretar m y n.','Modelar un contexto lineal.'],
f'''<section class="bloque-cuerpo">
<h2>Forma y gráfico</h2>
<p>f(x)=mx+n: m = pendiente (variación media constante), n = ordenada en el origen f(0).</p>
{S('Recta','''
<line x1="60" y1="200" x2="660" y2="200" stroke="#9A9488"/><line x1="120" y1="20" x2="120" y2="220" stroke="#9A9488"/>
<line x1="120" y1="160" x2="520" y2="40" stroke="#C4A15A" stroke-width="2"/>
<text x="400" y="100" fill="#C4A15A">m&gt;0</text>
<text x="140" y="150" fill="#8F9A72" font-size="13">n=f(0)</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>f(x)=2x−3: m=2, n=−3. Pasa por (0,−3) y (2,1).</li></ol>
<h2>Ejemplo 2 — tarifa</h2>
<ol class="pasos"><li>12 € fijos + 0,8 €/km → C(x)=0,8x+12.</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>Por (1,4) y (3,10): m=(10−4)/(3−1)=3; n=4−3·1=1 → y=3x+1.</li></ol>
{ej(1,'Lectura','f(x)=−0,5x+4. ¿Crece o decrece? Intersección con ejes.','Decrece (m&lt;0). Eje Y: 4. Eje X: −0,5x+4=0 → x=8.','e20a')}
{ej(2,'Modelo','Entrada 5 € + 2 €/hora. Coste 3 h.','C=5+2·3=11 €.','e20b')}
{ej(3,'Pendiente','Por (0,2) y (4,2). m y ecuación.','m=0; y=2 (constante).','e20c')}
{ej(4,'Paralelas','y=2x+1 y y=2x−5. ¿Relación?','Misma m → paralelas; distintos n.','e20d')}
<canvas id="lienzo20" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo20">Borrar</button></div>
</section>''',
[('m en mx+n','pendiente'),('n','f(0)'),('Tarifa fija+variable','afin')],
'Tarifa','Inventa una tarifa afin; grafica en el lienzo; tabla en el editor.')

write_dense(21,'Funciones <em>cuadráticas</em>','D.2/D.4 Cuadráticas','Parábolas con significado',
'CyL: funciones cuadráticas; vértices, raíces y modelización.',
['Reconocer f(x)=ax²+bx+c.','Hallar vértice y raíces cuando existan.','Interpretar el signo de a.'],
f'''<section class="bloque-cuerpo">
<h2>Forma</h2>
<p>a&gt;0 abre hacia arriba (mínimo); a&lt;0 hacia abajo (máximo). Vértice en x=−b/(2a). Discriminante Δ=b²−4ac decide el número de raíces reales.</p>
{S('Parábola','''
<path d="M 80 40 Q 360 220 640 40" fill="none" stroke="#C4A15A" stroke-width="2"/>
<circle cx="360" cy="200" r="5" fill="#E6E1D6"/>
<text x="370" y="195" fill="#8F9A72">vértice</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>f(x)=x²−4x+3. a=1&gt;0. Vértice x=2, f(2)=−1.</li><li>Δ=16−12=4 → raíces 1 y 3.</li></ol>
<h2>Ejemplo 2 — altura</h2>
<ol class="pasos"><li>h(t)=−5t²+20t: máximo en t=2, h=20 (unidades del modelo).</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>x²+1=0: Δ&lt;0, sin raíces reales; siempre positiva.</li></ol>
{ej(1,'Vértice','f(x)=2x²−8x+1. x del vértice.','x=8/(4)=2. f(2)=2·4−16+1=−7.','e21a')}
{ej(2,'Δ','x²−2x+1. Raíces.','Δ=0 → raíz doble x=1.','e21b')}
{ej(3,'Signo a','a&lt;0: ¿máx o mín?','Máximo en el vértice.','e21c')}
{ej(4,'Modelo','Área de rectángulo de perímetro 20: x·(10−x). ¿Máximo?','A=10x−x²; vértice x=5 → cuadrado área 25.','e21d')}
<canvas id="lienzo21" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo21">Borrar</button></div>
</section>''',
[('x vértice','−b/(2a)'),('Δ&gt;0','dos raíces'),('a&gt;0','mínimo')],
'Parábola','Dibuja y=x²−4x+3; marca raíces y vértice.')

write_dense(22,'Racionales, a trozos y <em>periódicas</em>','D.2/D.4 Otras','Más allá de la parábola',
'CyL: racionales sencillas, definidas a trozos y periódicas.',
['Identificar asíntotas verticales simples en p(x)/q(x).','Leer una función a trozos.','Reconocer periodo en un gráfico.'],
f'''<section class="bloque-cuerpo">
<h2>Tres familias</h2>
<p><strong>Racional sencilla:</strong> f(x)=1/x tiene asíntota vertical x=0 y horizontal y=0.</p>
<p><strong>A trozos:</strong> varias fórmulas según el intervalo; mira el extremo (cerrado/abierto).</p>
<p><strong>Periódica:</strong> f(x+T)=f(x); T periodo.</p>
{S('1/x y trozos','''
<text x="40" y="50" fill="#E6E1D6">f(x)=1/x · asíntota x=0</text>
<text x="40" y="120" fill="#8F9A72">g(x)=x si x&lt;0; 2 si x≥0</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>f(x)=(x−1)/(x−2): no definida en 2; asíntota vertical x=2.</li></ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>h(x)=−x si x&lt;0, x si x≥0 (valor absoluto). Continua; pico en 0.</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>Señal que se repite cada 4 s: periodo T=4.</li></ol>
{ej(1,'Dominio','(x+1)/(x−3). ¿Dónde no está definida?','x=3. Denominador cero.','e22a')}
{ej(2,'Trozos','f(x)=2x (x&lt;1), 5 (x≥1). f(1) y f(0).','f(1)=5; f(0)=0.','e22b')}
{ej(3,'Periodo','Si T=2 y f(0)=3, ¿f(4)?','3. 4=2·2.','e22c')}
{ej(4,'Asíntota','¿Por qué 1/x no corta x=0?','Denominador nulo: no hay imagen.','e22d')}
<canvas id="lienzo22" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo22">Borrar</button></div>
</section>''',
[('1/x asíntota vertical','x=0'),('A trozos','elige fórmula por intervalo'),('f(x+T)=f(x)','periodo T')],
'Trozos','Define una función a trozos con 2 piezas; grafícala.')

write_dense(23,'Exponenciales y <em>logarítmicas</em>','D.2/D.4 Exp-log','Crecer multiplicando',
'CyL: exponenciales y logarítmicas; propiedades y modelización.',
['Reconocer y=a·b^x.','Usar el logaritmo para despejar el exponente.','Comparar crecimiento lineal vs exponencial.'],
f'''<section class="bloque-cuerpo">
<h2>Par inversas</h2>
<p>Si b&gt;0, b≠1: y=b^x y y=log_b x son inversas. Dom log: x&gt;0.</p>
{S('Exp','''
<path d="M 80 200 Q 200 180 320 100 T 560 20" fill="none" stroke="#C4A15A" stroke-width="2"/>
<text x="400" y="80" fill="#C4A15A">b^x crece si b&gt;1</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>Población P=100·1,05^t. A 3 años: 100·1,05³≈115,76.</li></ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>2^x=32 → x=5. O x=log₂32.</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>Lineal 10+2t vs exp 10·1,2^t: a largo plazo gana la exp si la base &gt;1.</li></ol>
{ej(1,'Valor','50·2^4.','800. Duplicar 4 veces.','e23a')}
{ej(2,'Log','log₁₀ 1000.','3.','e23b')}
{ej(3,'Despeje','1,1^t=2. Idea.','t=log(2)/log(1,1). No hace falta el valor decimal aquí: deja escrito el log.','e23c')}
{ej(4,'Dominio','log(x−2): dominio.','x&gt;2.','e23d')}
<canvas id="lienzo23" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo23">Borrar</button></div>
</section>''',
[('2^5','32'),('Inversa de b^x','log_b'),('Dominio log','x&gt;0')],
'Ahorro','Compara interés simple y compuesto en tabla; gráfica aproximada.')

write_dense(24,'Sistemas de <em>ecuaciones</em>','D.3 Sistemas','Varias condiciones a la vez',
'CyL: sistemas de ecuaciones en contextos.',
['Resolver 2×2 por sustitución o igualación.','Interpretar la intersección de rectas.','Detectar incompatible o indeterminado.'],
f'''<section class="bloque-cuerpo">
<h2>Geometría</h2>
<p>Cada ecuación lineal es una recta. Una solución = un punto de corte. Paralelas sin corte: incompatible. Misma recta: infinitas.</p>
{S('Corte','''
<line x1="80" y1="180" x2="600" y2="40" stroke="#C4A15A" stroke-width="2"/>
<line x1="80" y1="40" x2="600" y2="180" stroke="#8F9A72" stroke-width="2"/>
<circle cx="340" cy="110" r="6" fill="#E6E1D6"/>
<text x="360" y="105" fill="#E6E1D6">solución</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>x+y=5; x−y=1 → sumando 2x=6 → x=3, y=2.</li></ol>
<h2>Ejemplo 2 — contexto</h2>
<ol class="pasos"><li>2 cafés + 1 té = 5 €; 1 café + 2 tés = 5,5 €. Resuelve.</li><li>2c+t=5; c+2t=5,5 → c=1,5; t=2.</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>x+y=1; 2x+2y=3 incompatible (paralelas).</li></ol>
{ej(1,'Suma','x+2y=7; x−2y=1.','Suma: 2x=8 → x=4; y=1,5.','e24a')}
{ej(2,'Sustitución','y=2x; x+y=9.','x+2x=9 → x=3, y=6.','e24b')}
{ej(3,'Tipo','x−y=2; 2x−2y=4.','Infinitas: segunda = 2·primera.','e24c')}
{ej(4,'Contexto','Entradas: 3 adultos + 2 niños = 44; 1A+3N=28. Precios.','3a+2n=44; a+3n=28 → a=8, n=20/3≈6,67 (o exacto 20/3).','e24d')}
<canvas id="lienzo24" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo24">Borrar</button></div>
</section>''',
[('Corte de dos rectas','una solución'),('Paralelas distintas','incompatible'),('x+y=5,x−y=1','(3,2)')],
'Rectas','Dibuja dos rectas que se cortan; escribe el sistema y la solución.')

write_dense(25,'Inecuaciones y <em>sistemas</em>','D.3 Inecuaciones','Regiones, no solo puntos',
'CyL: inecuaciones y sistemas de inecuaciones.',
['Resolver inecuaciones lineales.','Representar semipianos.','Intersecar regiones.'],
f'''<section class="bloque-cuerpo">
<h2>De la igualdad a la región</h2>
<p>ax+by ≤ c define un semipiano. La frontera es la recta ax+by=c. Un sistema es la intersección de regiones.</p>
{S('Semipiano','''
<line x1="100" y1="200" x2="600" y2="40" stroke="#C4A15A" stroke-width="2"/>
<text x="200" y="160" fill="#8F9A72">región sombreada = soluciones</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>2x−4&gt;0 → x&gt;2. Intervalo (2,+∞).</li></ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>x+y≤4, x≥0, y≥0: triángulo con vértices (0,0),(4,0),(0,4).</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>Al multiplicar por −1 una inecuación, se invierte el sentido.</li></ol>
{ej(1,'Intervalo','−3x≥6.','x≤−2 (al dividir por −3 se invierte).','e25a')}
{ej(2,'Punto','¿(1,1) cumple x+y≤3 y x≥0?','Sí: 2≤3 y 1≥0.','e25b')}
{ej(3,'Frontera','En ≤, ¿la frontera cuenta?','Sí. En &lt;, no.','e25c')}
{ej(4,'Sistema','x≥0,y≥0,x+y≤2: vértices.','(0,0),(2,0),(0,2).','e25d')}
<canvas id="lienzo25" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo25">Borrar</button></div>
</section>''',
[('Invertir al ·(−1)','sí'),('≤ incluye','frontera'),('x+y≤2, x,y≥0 vértices','(0,0)(2,0)(0,2)')],
'Región','Sombrea x≥0, y≥0, x+2y≤6 en el lienzo; lista vértices.')

write_dense(26,'Programación <em>lineal</em>','D.2 PL','Optimizar en un polígono',
'CyL: programación lineal — modelización y resolución en el plano.',
['Escribir función objetivo y restricciones.','Hallar la región factible.','Evaluar la objetivo en vértices.'],
f'''<section class="bloque-cuerpo">
<h2>Método en 2 variables</h2>
<p>1) Variables. 2) Restricciones → región. 3) Objetivo z=ax+by. 4) En PL lineal, el óptimo está en un vértice (si existe).</p>
{S('Factible','''
<polygon points="120,200 320,200 280,80 120,120" fill="rgba(196,161,90,.15)" stroke="#C4A15A" stroke-width="2"/>
<text x="160" y="160" fill="#E6E1D6">vértices</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos">
<li>Max z=3x+2y s.a. x+y≤4, x≥0,y≥0.</li>
<li>Vértices (0,0),(4,0),(0,4). z: 0,12,8 → máximo 12 en (4,0).</li>
</ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>Misma región, min z=x+5y → óptimo en (4,0) con z=4 (comparar vértices).</li></ol>
<h2>Ejemplo 3 — fábrica</h2>
<ol class="pasos"><li>Productos A,B con límites de horas y material: traduce a inecuaciones antes de dibujar.</li></ol>
{ej(1,'Vértice','Región (0,0),(5,0),(0,3). Max z=2x+y.','En (5,0): z=10; (0,3):3; (0,0):0 → 10.','e26a')}
{ej(2,'Modelo','x mesas, y sillas; x+y≤10, x≤6. Escribe restricciones completas con x,y≥0.','x+y≤10, x≤6, x≥0,y≥0.','e26b')}
{ej(3,'¿Interior?','¿Puede el máximo de z lineal estar estrictamente dentro?','No, en región poligonal cerrada el extremo está en vértice.','e26c')}
{ej(4,'Vacía','Si las restricciones no se cortan, ¿qué pasa?','Región vacía: no hay programa factible.','e26d')}
<canvas id="lienzo26" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo26">Borrar</button></div>
</section>''',
[('Óptimo PL 2D','en un vértice'),('z=3x+2y en (4,0)','12'),('Paso previo','región factible')],
'Fábrica','Inventa 2 productos, 2 recursos; dibuja región y elige óptimo.')

write_dense(27,'Pensamiento <em>computacional</em>','D.5 Computacional','Algoritmos sin magia',
'CyL: pensamiento computacional — algoritmos, programas y herramientas (aquí offline).',
['Descomponer un problema en pasos.','Escribir un algoritmo en pseudocódigo.','Detectar bucles y condiciones.'],
f'''<section class="bloque-cuerpo">
<h2>Ideas clave</h2>
<p>Entrada → proceso → salida. Secuencia, selección (si), iteración (mientras/para). Un algoritmo debe terminar y ser preciso.</p>
{S('Flujo','''
<rect x="280" y="30" width="160" height="40" fill="#1C1A16" stroke="#C4A15A"/><text x="360" y="55" text-anchor="middle" fill="#E6E1D6">entrada</text>
<rect x="280" y="100" width="160" height="40" fill="#1C1A16" stroke="#8F9A72"/><text x="360" y="125" text-anchor="middle" fill="#8F9A72">proceso</text>
<rect x="280" y="170" width="160" height="40" fill="#1C1A16" stroke="#C4A15A"/><text x="360" y="195" text-anchor="middle" fill="#E6E1D6">salida</text>
''')}
<h2>Ejemplo 1 — máximo de una lista</h2>
<ol class="pasos"><li>m ← primer elemento. Para cada siguiente: si es &gt; m, m ← ese. Salida m.</li></ol>
<h2>Ejemplo 2 — Euclides (mcd)</h2>
<ol class="pasos"><li>Mientras b≠0: (a,b)←(b, a mod b). Salida a.</li></ol>
<h2>Ejemplo 3 — conteo</h2>
<ol class="pasos"><li>Contador c=0; para cada ítem si cumple, c←c+1.</li></ol>
{ej(1,'Pseudo','Algoritmo: suma de 1 a n.','s←0; para i=1..n: s←s+i; salida s. (O fórmula n(n+1)/2.)','e27a')}
{ej(2,'Bug','Bucle mientras x&gt;0 pero x nunca baja. ¿Problema?','No termina. Falta actualizar x.','e27b')}
{ej(3,'Descomponer','Calcular media de 5 notas: pasos.','Leer 5; sumar; dividir por 5; mostrar.','e27c')}
{ej(4,'Condición','Clasificar aprobado si nota≥5.','Si nota≥5 entonces «apto» si no «no apto».','e27d')}
<canvas id="lienzo27" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo27">Borrar</button></div>
</section>''',
[('Tres estructuras','secuencia, si, bucle'),('Euclides','mcd'),('Algoritmo debe','terminar y ser preciso')],
'Algoritmo','Escribe pseudocódigo para el mínimo de una lista; diagrama de flujo en el lienzo.')

write_dense(28,'Estadística: <em>interpretación</em>','E.1 Estadística','Leer sin engañarse',
'CyL: interpretación y análisis de información estadística.',
['Leer tablas y gráficos con unidades.','Calcular media, mediana y rango en series cortas.','Detectar sesgos de presentación.'],
f'''<section class="bloque-cuerpo">
<h2>Resúmenes</h2>
<p>Media: promedio. Mediana: valor central ordenado. Rango: máx−mín. Un gráfico puede manipular el eje Y para exagerar diferencias.</p>
{S('Barras','''
<rect x="120" y="100" width="60" height="100" fill="#C4A15A"/><rect x="220" y="60" width="60" height="140" fill="#8F9A72"/>
<text x="120" y="220" fill="#9A9488" font-size="12">lee la escala</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>Datos 2,4,4,5,10. Media=5; mediana=4; rango=8.</li></ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>El 10 tira la media arriba; la mediana resiste mejor el extremo.</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>Eje Y que empieza en 90 en vez de 0: diferencias se ven enormes.</li></ol>
{ej(1,'Media','3,5,7.','5.','e28a')}
{ej(2,'Mediana','1,2,8,9,10.','8.','e28b')}
{ej(3,'Sesgo','¿Por qué preguntar la escala del eje?','Sin escala, el gráfico puede exagerar o minimizar.','e28c')}
{ej(4,'Muestra','Encuesta solo en un grupo de WhatsApp: ¿problema?','Sesgo de selección: no representa a toda la población.','e28d')}
<canvas id="lienzo28" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo28">Borrar</button></div>
</section>''',
[('Media de 2,4,6','4'),('Mediana vs outlier','mediana más robusta'),('Eje manipulado','sesgo visual')],
'Noticia','Inventa un gráfico engañoso y uno honesto del mismo dato; explícalo.')

print('19-28 done')
from pathlib import Path
for i in range(19,29):
    p=list(Path('/workspace/lesvencimos/staging/bach1/mates-gen/lecciones').glob(f'leccion-{i:02d}-*.html'))[0]
    print(i, p.stat().st_size)
