# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'/workspace/lesvencimos/staging/bach1/mates-gen/_gen')
from chrome import write_dense, ej

def S(title, inner):
    return f'<div class="figura-svg"><svg viewBox="0 0 720 240" role="img"><title>{title}</title><rect width="720" height="240" fill="#161512"/>{inner}</svg></div>'

write_dense(11,'Probabilidad como <em>medida</em>','B.1 Probabilidad','Del «creo» al número entre 0 y 1',
'CyL introduce la probabilidad como medida de la incertidumbre: asignar un número coherente a sucesos.',
['Asignar P(A) entre 0 y 1.','Usar regla de Laplace cuando hay equiprobabilidad.','Interpretar frecuencia relativa como aproximación empírica.'],
f'''<section class="bloque-cuerpo">
<h2>Qué mide la probabilidad</h2>
<p>P(A) ∈ [0,1]. P(∅)=0, P(Ω)=1. Si A y B son incompatibles (A∩B=∅), P(A∪B)=P(A)+P(B).</p>
<p><strong>Laplace</strong> (casos favorables / posibles) solo si todos los resultados elementales son equiprobables. Si no, usa frecuencias o un modelo distinto.</p>
<span class="glosa">Ω = espacio muestral · A ⊂ Ω · P = medida de incertidumbre</span>
{S('Dados','''
<text x="40" y="50" fill="#E6E1D6" font-size="16">Dado justo: P(par)=3/6=1/2</text>
<text x="40" y="100" fill="#9A9488" font-size="14">Favorables: 2,4,6 · Posibles: 6</text>
<rect x="80" y="140" width="80" height="50" fill="#1C1A16" stroke="#C4A15A"/><text x="120" y="170" text-anchor="middle" fill="#C4A15A">1/2</text>
<text x="200" y="170" fill="#9A9488">no «50 % porque sí»: hay modelo</text>
''')}
<h2>Ejemplo 1 — monedas</h2>
<ol class="pasos">
<li>Moneda justa: Ω={{C,X}}, P(C)=P(X)=1/2.</li>
<li>Dos lanzamientos independientes: Ω tiene 4 pares; P(dos caras)=1/4.</li>
<li>P(al menos una cara)=1−P(XX)=3/4.</li>
</ol>
<h2>Ejemplo 2 — urna</h2>
<ol class="pasos">
<li>3 rojas, 2 azules. Una bola al azar: P(roja)=3/5.</li>
<li>Si no hay reposición y sacas dos: cuenta orden o usa combinaciones con cuidado.</li>
</ol>
<h2>Ejemplo 3 — frecuencia</h2>
<ol class="pasos">
<li>En 200 lanzamientos salen 108 caras → frecuencia 0,54.</li>
<li>No «demuestra» que P≠1/2; con n pequeño hay fluctuación.</li>
</ol>
{ej(1,'Laplace','Dado justo: P(múltiplo de 3).','Favorables 3 y 6 → 2/6=1/3. Equiprobabilidad justificada por «dado justo».','e11a')}
{ej(2,'Complementario','P(A)=0,35. ¿P(no A)?','0,65. P(Aᶜ)=1−P(A) siempre que A esté en Ω.','e11b')}
{ej(3,'Incompatibles','P(A)=0,2, P(B)=0,3, A∩B=∅. P(A∪B).','0,5. Suma porque no se solapan.','e11c')}
{ej(4,'Trampa','Baraja: ¿P(as)=1/4 porque hay 4 palos?','No. Hay 4 ases entre 52 cartas → 4/52=1/13. Los palos no son el espacio elemental aquí.','e11d')}
<canvas id="lienzo11" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo11">Borrar</button></div>
</section>''',
[('P(Ω)','1'),('Laplace exige','equiprobabilidad'),('P(A)=0,4 → P(Aᶜ)','0,6')],
'Experimento','Diseña un experimento con 6 resultados no equiprobables; justifica por qué Laplace no aplica.')

write_dense(12,'Variación absoluta y <em>media</em>','B.2 Variación','Cuánto cambia, y a qué ritmo',
'CyL: variación absoluta y variación media como puente hacia el límite y la derivada.',
['Calcular Δy = f(b)−f(a).','Calcular variación media (f(b)−f(a))/(b−a).','Interpretar la pendiente de la secante.'],
f'''<section class="bloque-cuerpo">
<h2>Dos números del cambio</h2>
<p>Variación absoluta: Δy = f(b)−f(a). Solo dice «cuánto subió o bajó», no a qué ritmo.</p>
<p>Variación media en [a,b]: m = (f(b)−f(a))/(b−a). Es la pendiente de la <strong>secante</strong> que une (a,f(a)) y (b,f(b)).</p>
<span class="glosa">Δy / Δx = ritmo medio · unidades: (unidad de y)/(unidad de x)</span>
{S('Secante','''
<path d="M 80 180 Q 200 40 400 100 T 640 60" fill="none" stroke="#8F9A72" stroke-width="2"/>
<line x1="160" y1="120" x2="480" y2="80" stroke="#C4A15A" stroke-width="2"/>
<circle cx="160" cy="120" r="5" fill="#E6E1D6"/><circle cx="480" cy="80" r="5" fill="#E6E1D6"/>
<text x="160" y="210" fill="#9A9488" font-size="13">secante = variación media</text>
''')}
<h2>Ejemplo 1 — lineal</h2>
<ol class="pasos">
<li>f(x)=2x+1. En [1,4]: f(1)=3, f(4)=9.</li>
<li>Δy=6; m=6/3=2. Coincide con la pendiente de la recta.</li>
</ol>
<h2>Ejemplo 2 — cuadrática</h2>
<ol class="pasos">
<li>f(x)=x² en [1,3]: f(1)=1, f(3)=9 → m=(9−1)/(3−1)=4.</li>
<li>No es la pendiente en un solo punto; es el ritmo medio del intervalo.</li>
</ol>
<h2>Ejemplo 3 — unidades</h2>
<ol class="pasos">
<li>Posición s en metros, t en segundos: m en m/s (velocidad media).</li>
</ol>
{ej(1,'Media','f(x)=x²−x en [2,5]. Variación media.','f(2)=2, f(5)=20 → (20−2)/(5−2)=6.','e12a')}
{ej(2,'Absoluta','Misma f: Δy en [2,5].','18. Solo el numerador.','e12b')}
{ej(3,'Signo','Si m&lt;0 en [a,b], ¿qué pasó?','En media, la función descendió: f(b)&lt;f(a).','e12c')}
{ej(4,'Comparar','f(x)=x²: media en [0,2] vs [2,4].','[0,2]: 2; [2,4]: 6. El ritmo medio crece.','e12d')}
<canvas id="lienzo12" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo12">Borrar</button></div>
</section>''',
[('Δy = f(b)−f(a)','variación absoluta'),('m=(f(b)−f(a))/(b−a)','variación media / pendiente secante'),('Unidades de m si y en € y x en meses','€/mes')],
'Secante','Dibuja y=x², marca dos puntos y la secante; anota m en el editor.')

write_dense(13,'Límite: idea de <em>cambio</em>','B.2 Límite','Cuando el intervalo se encoge',
'CyL introduce el límite desde la variación media, como paso hacia la derivada.',
['Entender el límite como valor al que se acerca una expresión.','Acercar b→a en la variación media.','Relacionar con la pendiente de la tangente (idea).'],
f'''<section class="bloque-cuerpo">
<h2>De la secante a la idea de tangente</h2>
<p>Fija a y deja que h→0 en (f(a+h)−f(a))/h. Si ese cociente se acerca a un número L, ese L es el candidato a f′(a).</p>
<p>No hace falta la definición ε-δ aquí: sí hace falta una tabla de valores y un gráfico que muestre el acercamiento.</p>
<span class="glosa">h = incremento · cociente incremental · L = límite del cociente</span>
{S('Acercamiento','''
<text x="40" y="40" fill="#E6E1D6" font-size="14">f(x)=x² en a=1 · cociente ( (1+h)²−1 )/h = 2+h</text>
<text x="40" y="90" fill="#8F9A72">h=0,1 → 2,1</text>
<text x="40" y="130" fill="#8F9A72">h=0,01 → 2,01</text>
<text x="40" y="170" fill="#C4A15A" font-weight="700">h→0 → 2</text>
''')}
<h2>Ejemplo 1 — x² en 1</h2>
<ol class="pasos">
<li>(f(1+h)−f(1))/h = ((1+2h+h²)−1)/h = 2+h.</li>
<li>Si h→0, el cociente → 2.</li>
<li>Interpretación: cerca de x=1, la curva se comporta como una recta de pendiente 2.</li>
</ol>
<h2>Ejemplo 2 — tabla</h2>
<ol class="pasos">
<li>h=0,1 → 2,1; h=0,01 → 2,01; h=−0,01 → 1,99.</li>
<li>Por ambos lados se acerca a 2.</li>
</ol>
<h2>Ejemplo 3 — constante</h2>
<ol class="pasos">
<li>f(x)=5: el cociente es 0 para todo h≠0 → límite 0 (no cambia).</li>
</ol>
{ej(1,'Algebra','f(x)=3x en a=2: simplifica el cociente y pasa al límite.','(3(2+h)−6)/h=3 → límite 3.','e13a')}
{ej(2,'Tabla','f(x)=x² en a=0: valores del cociente para h=0,1 y 0,01.','h y h: 0,1 y 0,01 → límite 0.','e13b')}
{ej(3,'Idea','¿Por qué no sustituir h=0 directamente en el cociente sin simplificar?','Queda 0/0. Hay que simplificar o tabular antes de «pasar al límite».','e13c')}
{ej(4,'Unidades','Si f es posición (m) y x tiempo (s), ¿qué unidades tiene el límite del cociente?','m/s: velocidad instantánea (idea).','e13d')}
<canvas id="lienzo13" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo13">Borrar</button></div>
</section>''',
[('Cociente de x² en 1','2+h → 2'),('h→0 por ambos lados a 2','límite 2'),('Constante: límite del cociente','0')],
'Tangente mental','Dibuja y=x² y varias secantes hacia x=1; anota en el editor la tabla de h.')

write_dense(15,'Grafos: tipos y <em>representación</em>','C.1 Grafos','Puntos y flechas con significado',
'CyL: grafos dirigidos, no dirigidos, planos, ponderados y árboles.',
['Distinguir dirigido / no dirigido / ponderado.','Representar con diagrama y con matriz.','Reconocer un árbol.'],
f'''<section class="bloque-cuerpo">
<h2>Vocabulario mínimo</h2>
<p><strong>Vértices</strong> (nodos) y <strong>aristas</strong> (o arcos si hay sentido). Ponderado: cada arista lleva un peso (km, coste, tiempo).</p>
<p>Un <strong>árbol</strong> es un grafo conexo sin ciclos. Un grafo <strong>plano</strong> se puede dibujar sin cruces de aristas.</p>
{S('Tipos','''
<circle cx="120" cy="100" r="18" fill="#1C1A16" stroke="#C4A15A"/><text x="120" y="105" text-anchor="middle" fill="#E6E1D6">A</text>
<circle cx="280" cy="100" r="18" fill="#1C1A16" stroke="#C4A15A"/><text x="280" y="105" text-anchor="middle" fill="#E6E1D6">B</text>
<line x1="138" y1="100" x2="262" y2="100" stroke="#C4A15A" stroke-width="2"/>
<text x="180" y="85" fill="#8F9A72" font-size="12">3</text>
<text x="100" y="180" fill="#9A9488" font-size="13">ponderado no dirigido</text>
<circle cx="480" cy="80" r="16" fill="#1C1A16" stroke="#C4A15A"/><text x="480" y="85" text-anchor="middle" fill="#E6E1D6">A</text>
<circle cx="600" cy="140" r="16" fill="#1C1A16" stroke="#C4A15A"/><text x="600" y="145" text-anchor="middle" fill="#E6E1D6">B</text>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#C4A15A"/></marker></defs>
<line x1="494" y1="90" x2="586" y2="130" stroke="#C4A15A" stroke-width="2" marker-end="url(#arrow)"/>
<text x="500" y="200" fill="#9A9488" font-size="13">dirigido A→B</text>
''')}
<h2>Ejemplo 1 — ciudad</h2>
<ol class="pasos">
<li>Calles de doble sentido: no dirigido. Sentido único: dirigido.</li>
<li>Minutos de trayecto: pesos en las aristas.</li>
</ol>
<h2>Ejemplo 2 — árbol genealógico simplificado</h2>
<ol class="pasos">
<li>Conexo y sin ciclos → árbol. n vértices ⇒ n−1 aristas.</li>
</ol>
<h2>Ejemplo 3 — matriz</h2>
<ol class="pasos">
<li>Grafo A—B—C: adyacencia simétrica con 1 en AB y BC.</li>
</ol>
{ej(1,'Árbol','Un conexo con 5 vértices y 5 aristas: ¿es árbol?','No: un árbol con 5 vértices tiene exactamente 4 aristas. Aquí hay ciclo.','e15a')}
{ej(2,'Dirigido','Solo arco A→B. ¿a_BA en la matriz de adyacencia?','0. El sentido importa.','e15b')}
{ej(3,'Peso','Dos rutas A→B de 4 y 7 minutos. ¿Qué guarda el grafo ponderado?','Dos aristas (o la de menor peso si modelas «mejor»); el peso es el dato de cada arista.','e15c')}
{ej(4,'Plano','K5 ¿es siempre dibujable sin cruces?','No: K5 no es plano. CyL pide reconocer la idea de planaridad.','e15d')}
<canvas id="lienzo15" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo15">Borrar</button></div>
</section>''',
[('Árbol con n vértices','n−1 aristas'),('Arista con minutos','grafo ponderado'),('Solo A→B','dirigido')],
'Red local','Dibuja 5 lugares de tu entorno, aristas con tiempos, y escribe si es dirigido o no.')

write_dense(16,'Euler y grafos <em>planos</em>','C.1 Euler','Caras, aristas, vértices',
'CyL: fórmula de Euler y grafos planos.',
['Enunciar V−E+F=2 para grafos planos conexos.','Contar caras incluyendo el exterior.','Relacionar planaridad con el dibujo.'],
f'''<section class="bloque-cuerpo">
<h2>Fórmula de Euler</h2>
<p>Para un grafo <strong>conexo plano</strong> dibujado sin cruces: V − E + F = 2, donde F cuenta también la cara infinita exterior.</p>
{S('Tetraedro plano','''
<text x="40" y="40" fill="#E6E1D6">Ejemplo: triangulación simple</text>
<text x="40" y="90" fill="#8F9A72">V=4, E=6, F=4 → 4−6+4=2</text>
<polygon points="360,40 280,180 440,180" fill="none" stroke="#C4A15A" stroke-width="2"/>
<line x1="360" y1="40" x2="360" y2="180" stroke="#C4A15A"/>
<line x1="280" y1="180" x2="400" y2="100" stroke="#C4A15A"/>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos">
<li>Cuadrado con una diagonal: V=4, E=5, caras=3 (2 interiores + exterior) → 4−5+3=2.</li>
</ol>
<h2>Ejemplo 2</h2>
<ol class="pasos">
<li>Árbol con 6 vértices: E=5, F=1 (solo exterior) → 6−5+1=2.</li>
</ol>
<h2>Ejemplo 3</h2>
<ol class="pasos">
<li>Si al dibujar necesitas cruces inevitables, no es plano: Euler en esa forma no aplica.</li>
</ol>
{ej(1,'Cuenta','Grafo plano: V=6, E=9. ¿F?','F=2−V+E=5. Incluye el exterior.','e16a')}
{ej(2,'Árbol','V=8 árbol. E y F.','E=7; F=1; 8−7+1=2.','e16b')}
{ej(3,'Olvido','¿Por qué fallan cuentas que olvidan la cara exterior?','F queda corto y V−E+F≠2.','e16c')}
{ej(4,'Plano','¿Todo grafo con V−E+F=2 es plano?','La fórmula se usa en grafos ya dibujados planos conexos; no es un test mágico aislado.','e16d')}
<canvas id="lienzo16" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo16">Borrar</button></div>
</section>''',
[('V−E+F','2 (plano conexo)'),('Árbol: F','1'),('Incluir','cara exterior')],
'Mapa','Dibuja un grafo plano, numera V,E,F y comprueba Euler en el editor.')

write_dense(17,'Eulerianos, hamiltonianos y <em>coloración</em>','C.1 Recorridos','Pasar por aristas o por vértices',
'CyL: caminos/circuitos eulerianos y hamiltonianos; coloración de grafos.',
['Distinguir euleriano (aristas) y hamiltoniano (vértices).','Usar grados pares para circuitos eulerianos.','Explicar coloración propia.'],
f'''<section class="bloque-cuerpo">
<h2>Dos problemas clásicos</h2>
<p><strong>Euleriano:</strong> recorrer cada arista exactamente una vez. Circuito euleriano: además vuelves al inicio. Condición útil: todos los grados pares (grafo conexo).</p>
<p><strong>Hamiltoniano:</strong> visitar cada vértice exactamente una vez. No hay criterio tan simple: a menudo se explora o se argumenta con ejemplos.</p>
<p><strong>Coloración:</strong> asignar colores a vértices para que adyacentes no compartan color. El número cromático es el mínimo de colores.</p>
{S('Grados','''
<text x="40" y="60" fill="#E6E1D6">Circuito euleriano ↔ grados pares (conexo)</text>
<text x="40" y="110" fill="#9A9488">Camino euleriano (no circuito): exactamente 0 o 2 vértices de grado impar</text>
''')}
<h2>Ejemplo 1 — cuadrado</h2>
<ol class="pasos">
<li>Ciclo C4: todos grado 2 → circuito euleriano existe.</li>
<li>También es hamiltoniano (el propio ciclo).</li>
</ol>
<h2>Ejemplo 2 — puentes</h2>
<ol class="pasos">
<li>Si hay más de dos vértices de grado impar, no hay camino euleriano.</li>
</ol>
<h2>Ejemplo 3 — coloración</h2>
<ol class="pasos">
<li>Grafo bipartito: 2 colores bastan. Triángulo: necesita 3.</li>
</ol>
{ej(1,'Grados','Conexo con grados 2,2,2,2,2. ¿Circuito euleriano?','Sí: todos pares.','e17a')}
{ej(2,'Impar','Grados 3,3,2,2. ¿Camino euleriano?','Sí: exactamente dos impares. Empieza en un impar.','e17b')}
{ej(3,'Hamilton','¿Todo euleriano es hamiltoniano?','No. Recorrer aristas ≠ visitar vértices una sola vez.','e17c')}
{ej(4,'Colores','K3 (triángulo): número cromático.','3. Cada par está unido.','e17d')}
<canvas id="lienzo17" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo17">Borrar</button></div>
</section>''',
[('Circuito euleriano','grados pares'),('Dos impares','camino euleriano'),('Triángulo cromático','3')],
'Mapa de calles','Dibuja un barrio pequeño; marca grados; decide si hay ruta del cartero (euleriana).')

write_dense(18,'El problema del camino <em>mínimo</em>','C.1 Camino mínimo','La ruta más barata',
'CyL: camino mínimo en contextos (distancia, tiempo, coste).',
['Modelar un mapa como grafo ponderado.','Comparar rutas sumando pesos.','Explicar la idea de algoritmo voraz/etiquetas (nivel Bach).'],
f'''<section class="bloque-cuerpo">
<h2>Modelo</h2>
<p>Vértices = lugares; aristas = tramos con peso (km, min, €). Un camino mínimo entre s y t minimiza la suma de pesos.</p>
<p>En grafos pequeños puedes enumerar. En mayores, la idea de <strong>Dijkstra</strong>: ir etiquetando la distancia mínima provisional desde el origen.</p>
{S('Rutas','''
<text x="40" y="40" fill="#E6E1D6">A—4—B—2—C  vs  A—7—C</text>
<text x="40" y="100" fill="#8F9A72">A→B→C suma 6 &lt; 7</text>
<text x="40" y="160" fill="#C4A15A">mínimo A→C = 6</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos">
<li>A-B 4, B-C 2, A-C 7. Mínimo A→C: por B, coste 6.</li>
</ol>
<h2>Ejemplo 2</h2>
<ol class="pasos">
<li>Si aparece un atajo A-C 5, el mínimo pasa a 5 (directo).</li>
</ol>
<h2>Ejemplo 3 — idea etiquetas</h2>
<ol class="pasos">
<li>Desde A: etiqueta A=0, vecinos con su peso.</li>
<li>Elige la etiqueta más pequeña no fijada; actualiza vecinos. Repite.</li>
</ol>
{ej(1,'Suma','Ruta 3+5+2. Coste.','10. Suma de pesos del camino.','e18a')}
{ej(2,'Comparar','Caminos 12 y 9 y 15. Mínimo.','9.','e18b')}
{ej(3,'Negativos','¿Por qué en Bach evitamos pesos negativos con Dijkstra básico?','Las actualizaciones voraces pueden fallar con negativos; otro marco (Bellman-Ford) hace falta.','e18c')}
{ej(4,'Contexto','Autobús vs a pie: ¿mismo grafo?','Puedes usar el mismo mapa con pesos distintos (tiempo) o capas (multigrafo). El peso define el criterio.','e18d')}
<canvas id="lienzo18" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo18">Borrar</button></div>
</section>''',
[('Camino mínimo','suma de pesos mínima'),('A-B4 B-C2 A-C7 → A a C','6'),('Peso típico','km, min, €')],
'Tu barrio','5 nodos con tiempos; calcula a mano el mínimo entre dos extremos.')

print('L11-13,15-18 written')
for i in [11,12,13,15,16,17,18]:
    from pathlib import Path
    p=list(Path('/workspace/lesvencimos/staging/bach1/mates-gen/lecciones').glob(f'leccion-{i:02d}-*.html'))[0]
    print(i, p.stat().st_size)
