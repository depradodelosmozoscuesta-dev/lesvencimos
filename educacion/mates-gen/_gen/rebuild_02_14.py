# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'/workspace/lesvencimos/staging/bach1/mates-gen/_gen')
from chrome import *

def build():
  # L02
  write_dense(2,'Conteo: principios <em>básicos</em>','A.1 Conteo',
  'Contar sin perder ni duplicar',
  'CyL pide comparación, adición, multiplicación y división para cardinales: el producto cuando las elecciones son independientes; la suma cuando son excluyentes.',
  ['Aplicar la regla del producto.','Usar la suma en casos excluyentes.','Detectar doble conteo.'],
  f'''<section class="bloque-cuerpo">
  <h2>Reglas</h2>
  <p>Si un proceso tiene k etapas con n₁, n₂, … opciones independientes, el total es el <strong>producto</strong> n₁·n₂·…·n_k. Si puedes llegar al mismo resultado por caminos excluyentes, <strong>sumas</strong> esos caminos.</p>
  {svg('Rejilla 3×4 del producto','''
  '''+ejes(60,250,660,30)+'''
  <g stroke="#C4A15A" stroke-width="1.5" fill="none">
  '''+''.join(f'<line x1="{80+i*50}" y1="60" x2="{80+i*50}" y2="220"/>' for i in range(5))+'''
  '''+''.join(f'<line x1="80" y1="{60+j*40}" x2="280" y2="{60+j*40}"/>' for j in range(5))+'''
  </g>
  <text x="400" y="120" fill="#E6E1D6" font-size="16">3 filas × 4 columnas = 12</text>
  <text x="400" y="160" fill="#9A9488" font-size="14">cada celda = un par (fila, columna)</text>
  ''',280)}
  <h2>Ejemplo resuelto 1 — menú</h2>
  {pasos_ol([
  ('2 primeros, 3 segundos, 2 postres; eliges uno de cada.','Glosa: tres etapas independientes.'),
  ('Total = 2·3·2 = 12 menús.','Glosa: producto, no suma: 2+3+2=7 sería otro problema.'),
  ('Comprueba listando mentalmente: para cada primero hay 3·2=6 segundos+postre.','Glosa: 2·6=12 cierra el círculo.'),
  ])}
  <h2>Ejemplo resuelto 2 — cromos</h2>
  {pasos_ol([
  ('24 cromos en 4 sobres iguales.','Glosa: reparto equitativo → división.'),
  ('24÷4 = 6 cromos por sobre.','Glosa: la división responde «¿cuántos en cada parte?».'),
  ('Si sobraran cromos, el cociente entero no bastaría: habría resto.','Glosa: en conteo exacto, el resto importa.'),
  ])}
  <h2>Ejemplo resuelto 3 — doble conteo</h2>
  {pasos_ol([
  ('|A|=10, |B|=7, |A∩B|=3. Si sumas 10+7…','Glosa: la intersección se ha contado dos veces.'),
  ('|A∪B| = 10+7−3 = 14.','Glosa: inclusión-exclusión en su forma más simple.'),
  ])}
  <h2>Ejercicios</h2>
  {ej(1,'Producto','Camisetas: 4 tallas y 5 colores. ¿Cuántas variantes?',
  '4·5=20. Cada talla se combina con cada color; las elecciones son independientes, así que aplica la regla del producto. Sumar 4+5=9 describiría otro enunciado (elegir talla O color, no ambos).',
  'e2a')}
  {ej(2,'Suma excluyente','Camino A con 3 rutas o camino B con 2 rutas, sin compartir. ¿Total?',
  '3+2=5. Son opciones excluyentes: tomas A o B, no ambos a la vez. Por eso sumas. Si pudieras encadenar A y luego B, sería producto.',
  'e2b')}
  {ej(3,'Trampa','Sumas |A|+|B| con intersección no vacía. ¿Qué falla y cómo se corrige?',
  'Cuentas dos veces los elementos de la intersección. Se corrige restando |A∩B| (inclusión-exclusión). Sin ese resto, el cardinal de la unión queda hinchado.',
  'e2c')}
  <h2>Dibuja</h2>
  <p>Rejilla o árbol de un producto 2×3 en el lienzo.</p>
  {canvas_block('lienzo02')}
  </section>''',
  [
  ('3×4 looks: ¿cuántos?',
  '12. Cada celda de la rejilla es un par ordenado (fila, columna). El producto 3·4 cuenta exactamente esos pares sin omitir ni repetir.'),
  ('Si no restas la intersección al unir A y B…',
  'Cometes doble conteo: los elementos de A∩B aparecen en |A| y otra vez en |B|. La unión real es |A|+|B|−|A∩B|.'),
  ('12 cromos en 3 sobres iguales: ¿cuántos por sobre?',
  '4. La división modela el reparto equitativo. 12÷3=4; si el enunciado no garantiza igualdad, no puedes usar solo esa división.'),
  ],
  'Inventario','Elige un armario real (ropa/comida) y escribe un producto de 2 o 3 factores; dibuja la rejilla.')

  # L03
  write_dense(3,'Palomar e inclusión-<em>exclusión</em>','A.1 Palomar',
  'Cuando sobran palomas',
  'CyL: principio del palomar e inclusión-exclusión para conteos correctos cuando hay forzamientos o solapes.',
  ['Enunciar el palomar.','Aplicarlo a un caso numérico.','Usar inclusión-exclusión con dos o tres conjuntos.'],
  f'''<section class="bloque-cuerpo">
  <h2>Palomar</h2>
  <p>Si n+1 objetos se ponen en n cajas, <strong>alguna caja tiene al menos 2</strong>. Más general: si hay más de k·n objetos en n cajas, alguna tiene al menos k+1.</p>
  {svg('Palomar 3 nidos, 4 palomas','''
  <rect x="80" y="160" width="120" height="80" rx="8" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
  <rect x="260" y="160" width="120" height="80" rx="8" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
  <rect x="440" y="160" width="120" height="80" rx="8" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
  <circle cx="110" cy="120" r="14" fill="#C4A15A"/><circle cx="150" cy="120" r="14" fill="#C4A15A"/>
  <circle cx="320" cy="120" r="14" fill="#8F9A72"/>
  <circle cx="500" cy="120" r="14" fill="#E6E1D6"/>
  <text x="360" y="50" text-anchor="middle" fill="#E6E1D6" font-size="15">4 palomas · 3 nidos → algún nido con ≥2</text>
  ''',280)}
  <h2>Ejemplo 1 — cumpleaños</h2>
  {pasos_ol([
  ('13 personas, 12 meses.','Glosa: 13 > 12 → palomar con n=12.'),
  ('Algún mes contiene al menos dos cumpleaños.','Glosa: no dice cuál; solo garantiza existencia.'),
  ])}
  <h2>Ejemplo 2 — inclusión-exclusión</h2>
  {pasos_ol([
  ('|A|=20, |B|=15, |A∩B|=6 → |A∪B|=20+15−6=29.','Glosa: restar la intersección una vez.'),
  ('Con tres conjuntos: suma individuales, resta dobles, suma el triple.','Glosa: + − + en el diagrama de Venn.'),
  ])}
  <h2>Ejemplo 3 — forzamiento</h2>
  {pasos_ol([
  ('10 calcetines, 3 colores. ¿Cuántos sacar para garantizar 3 del mismo?',
  'Glosa: peor caso: 2 de cada color = 6; el siguiente (7º) fuerza 3 de un color.'),
  ('Respuesta: 7.','Glosa: palomar con k=2, n=3 → k·n+1.'),
  ])}
  <h2>Ejercicios</h2>
  {ej(1,'Palomar','En una clase de 25, ¿se puede asegurar que al menos 3 nacieron el mismo día de la semana?',
  'Hay 7 días. 2·7=14; con 15 ya se fuerza 3 en un día. Como 25>14, sí: al menos un día tiene ≥3. El principio garantiza existencia, no identifica el día.',
  'e3a')}
  {ej(2,'Unión','|A|=12, |B|=9, |A∩B|=4. Calcula |A∪B| y explica cada término.',
  '|A∪B|=12+9−4=17. Sumas los dos cardinales y restas la intersección porque esos 4 se habían contado dos veces. Sin restar obtendrías 21, que hincha la unión.',
  'e3b')}
  {ej(3,'Venn','Dibuja A,B,C con números en cada región (elige datos coherentes) y comprueba la fórmula de tres conjuntos.',
  'Tras asignar las 7 regiones interiores + exterior, verifica: suma de individuales − suma de intersecciones dobles + |A∩B∩C| = unión. Si no cierra, revisa una región.',
  'e3c')}
  {canvas_block('lienzo03')}
  </section>''',
  [
  ('¿El palomar dice qué caja?',
  'No. Solo garantiza que existe al menos una caja con el mínimo anunciado. La prueba es por contradicción: si todas tuvieran menos, el total no alcanzaría.'),
  ('¿Por qué restar la intersección?',
  'Porque al sumar |A|+|B| cada elemento de A∩B se ha contado dos veces. Restar |A∩B| una vez deja cada elemento de la unión contado exactamente una vez.'),
  ('Calcetines: 4 colores, garantizar 3 iguales. ¿Cuántos?',
  'Peor caso: 2 de cada color = 8; el 9º fuerza un tercer calcetín de algún color. Fórmula: k·n+1 con k=2, n=4.'),
  ],
  'Palomar cotidiano','Inventa un palomar con cajas reales (ascensor, taquillas) y escribe el argumento.')

  print('L02-03 ok')

  # L04 + lab
  write_lab(4,'Árbol de posibilidades','''
  <div class="panel"><p>Elige opciones por nivel y calcula el producto.</p>
  <label>Nivel 1 <input id="n1" type="number" value="2" min="1" max="9"/></label>
  <label>Nivel 2 <input id="n2" type="number" value="3" min="1" max="9"/></label>
  <label>Nivel 3 <input id="n3" type="number" value="2" min="1" max="9"/></label>
  <button id="go">Calcular</button>
  <div class="out" id="out"></div>
  <canvas id="c" width="600" height="220"></canvas></div>
  <script>
  function dibuja(a,b,c){var cv=document.getElementById('c');var ctx=cv.getContext('2d');ctx.fillStyle='#12100e';ctx.fillRect(0,0,600,220);ctx.strokeStyle='#C4A15A';ctx.fillStyle='#E6E1D6';
  ctx.beginPath();ctx.arc(300,30,10,0,6.28);ctx.stroke();
  var y=100;for(var i=0;i<a;i++){var x=100+i*(400/(a||1));ctx.beginPath();ctx.moveTo(300,40);ctx.lineTo(x,y);ctx.stroke();ctx.beginPath();ctx.arc(x,y,8,0,6.28);ctx.stroke();}
  document.getElementById('out').textContent='Total de ramas (producto)= '+(a*b*c);}
  document.getElementById('go').onclick=function(){dibuja(+n1.value,+n2.value,+n3.value);};dibuja(2,3,2);
  </script>''')

  write_dense(4,'Árboles y <em>combinatoria</em>','A.1 Árboles y combinatoria',
  'El árbol ordena el conteo',
  'CyL pide diagramas de árbol y técnicas de combinatoria: variaciones si el orden importa; combinaciones si no.',
  ['Dibujar un árbol y leer el producto.','Calcular V(n,k) y C(n,k).','Justificar el cociente k!.'],
  f'''<section class="bloque-cuerpo">
  <h2>Árbol, variaciones, combinaciones</h2>
  <p>Cada nivel del árbol es una decisión. <strong>Variaciones</strong> V(n,k)=n·(n−1)·…·(n−k+1) cuando el orden importa. <strong>Combinaciones</strong> C(n,k)=V(n,k)/k! cuando no importa: cada grupo se había contado k! veces.</p>
  {svg('Árbol binario de profundidad 2','''
  <circle cx="360" cy="40" r="14" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
  <line x1="360" y1="54" x2="200" y2="110" stroke="#C4A15A" stroke-width="2"/>
  <line x1="360" y1="54" x2="520" y2="110" stroke="#C4A15A" stroke-width="2"/>
  <circle cx="200" cy="120" r="14" fill="#1C1A16" stroke="#8F9A72" stroke-width="2"/><text x="200" y="125" text-anchor="middle" fill="#E6E1D6" font-size="12">C</text>
  <circle cx="520" cy="120" r="14" fill="#1C1A16" stroke="#8F9A72" stroke-width="2"/><text x="520" y="125" text-anchor="middle" fill="#E6E1D6" font-size="12">X</text>
  <line x1="200" y1="134" x2="120" y2="190" stroke="#C4A15A"/><line x1="200" y1="134" x2="280" y2="190" stroke="#C4A15A"/>
  <line x1="520" y1="134" x2="440" y2="190" stroke="#C4A15A"/><line x1="520" y1="134" x2="600" y2="190" stroke="#C4A15A"/>
  <circle cx="120" cy="200" r="10" fill="#C4A15A"/><circle cx="280" cy="200" r="10" fill="#C4A15A"/>
  <circle cx="440" cy="200" r="10" fill="#C4A15A"/><circle cx="600" cy="200" r="10" fill="#C4A15A"/>
  <text x="360" y="250" text-anchor="middle" fill="#9A9488" font-size="14">2×2=4 secuencias de longitud 2</text>
  ''',280)}
  <h2>Ejemplo 1 — monedas</h2>
  {pasos_ol([
  ('3 lanzamientos: árbol binario profundidad 3.','Glosa: cada nivel multiplica por 2.'),
  ('2³=8 secuencias equiprobables si la moneda es justa.','Glosa: el árbol lista secuencias, no agregados.'),
  ('Agregar por «nº de caras» rompe la equiprobabilidad (hay 3 formas de 2 caras).','Glosa: C(3,2)=3.'),
  ])}
  <h2>Ejemplo 2 — PIN</h2>
  {pasos_ol([
  ('4 dígitos, primero ≠0, repetición permitida.','Glosa: 9·10·10·10.'),
  ('Total 9000.','Glosa: producto por posiciones independientes con repetición.'),
  ])}
  <h2>Ejemplo 3 — comité vs podio</h2>
  {pasos_ol([
  ('De 6 personas, comité de 2 sin cargos: C(6,2)=15.','Glosa: 6·5/2!; el /2 evita contar AB y BA.'),
  ('Podio oro-plata-bronce: V(6,3)=120.','Glosa: el orden importa.'),
  ('120/15=8=3!? No: 3!=6. Relación: C(6,3)·3!=V(6,3).','Glosa: para k=3, C·k!=V.'),
  ])}
  <h2>Ejercicios</h2>
  {ej(1,'C(5,2)','Calcula C(5,2) y explica el /2 con una frase.',
  'C(5,2)=5·4/2=10. Dividimos por 2! porque el par {{A,B}} es el mismo que {{B,A}}: en combinaciones el orden no crea un objeto nuevo. Si no dividieras, contarías cada comité dos veces.',
  'e4a')}
  {ej(2,'Matrícula','3 letras (26) y 4 dígitos, con repetición. Escribe el producto y justifica.',
  '26³·10⁴. Cada posición elige con independencia y puede repetir símbolo; la regla del producto multiplica las opciones de cada casilla. Usar variaciones sin repetición sería otro enunciado.',
  'e4b')}
  {ej(3,'Error típico','Usas V cuando el problema pedía C. ¿Qué hinchas y cómo lo corriges?',
  'Hinchas el conteo exactamente k! veces: cada grupo se cuenta una vez por cada permutación interna. Se corrige dividiendo por k! (pasar de variaciones a combinaciones). Lee si el enunciado distingue cargos u orden.',
  'e4c')}
  {canvas_block('lienzo04')}
  </section>''',
  [
  ('2³ secuencias de moneda justa',
  'Hay 8 secuencias distintas (CCC…XXX). El exponente 3 es la profundidad del árbol; la base 2 es el número de ramas por nodo. Si la moneda es justa, cada hoja pesa 1/8.'),
  ('¿Orden en un comité sin cargos?',
  'No importa: usas combinaciones. Distinto del podio, donde oro y plata son roles distintos y entonces usas variaciones. La clave está en si el enunciado distingue posiciones.'),
  ('Relación C y V',
  'V(n,k)=C(n,k)·k!. Las variaciones ordenan cada combinación de k elementos de k! formas. Por eso, si calculas V y el orden no importa, divides por k!.'),
  ],
  'Árbol del día','Dibuja un árbol de 2–3 decisiones reales y calcula el producto.',
  lab_title='Árbol de posibilidades')

  print('L04', list(__import__('pathlib').Path('/workspace/lesvencimos/staging/bach1/mates-gen/lecciones').glob('leccion-04*'))[0].stat().st_size)

if __name__=='__main__':
  build()
