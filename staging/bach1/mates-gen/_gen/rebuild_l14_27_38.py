# -*- coding: utf-8 -*-
"""L27–L38 al listón L14. No toca L01–L26. Staging, sin publicar."""
import math, sys
sys.path.insert(0, '/workspace/lesvencimos/staging/bach1/mates-gen/_gen')
from rebuild_l14_common import *

SNAP = snapshot()

# ---------- laboratorios (hermanos file://, carbón y ámbar, sin CDN) ----------
write_lab(27, 'Euclides paso a paso', '''
<div class="panel">
<p>Algoritmo de Euclides, el del ejemplo: mientras el segundo número no sea 0, se sustituye el par por (divisor, resto). Prueba 48 y 18, y después otro par.</p>
<label>a <input id="a" type="number" value="48" min="1" max="9999"/></label>
<label>b <input id="b" type="number" value="18" min="0" max="9999"/></label>
<button id="go" type="button">Calcular restos</button>
<div class="out" id="out"></div>
<canvas id="c" width="640" height="200"></canvas>
</div>
<script>
function pintar(pares){
  var cv=document.getElementById('c'), ctx=cv.getContext('2d');
  ctx.fillStyle='#12100e'; ctx.fillRect(0,0,640,200);
  ctx.strokeStyle='#9A9488'; ctx.beginPath(); ctx.moveTo(40,170); ctx.lineTo(600,170); ctx.stroke();
  var n=Math.max(1, pares.length);
  pares.forEach(function(p,i){
    var x=60+i*(520/n);
    var h=Math.min(130, p[0]);
    ctx.fillStyle='#C4A15A'; ctx.fillRect(x,170-h,18,h);
    ctx.fillStyle='#8F9A72'; ctx.fillRect(x+22,170-Math.min(130,p[1]),18,Math.min(130,p[1]));
    ctx.fillStyle='#E6E1D6'; ctx.font='12px sans-serif';
    ctx.fillText(p[0]+','+p[1], x, 188);
  });
}
document.getElementById('go').onclick=function(){
  var a=parseInt(document.getElementById('a').value,10);
  var b=parseInt(document.getElementById('b').value,10);
  if(!(a>0) || b<0){ document.getElementById('out').textContent='a debe ser positivo y b no negativo.'; return; }
  var pares=[[a,b]], lineas=[];
  var guard=0;
  while(b!==0 && guard<30){
    var q=Math.floor(a/b), r=a%b;
    lineas.push(a+' = '+q+' · '+b+' + '+r);
    a=b; b=r; pares.push([a,b]); guard++;
  }
  document.getElementById('out').textContent=lineas.join('  →  ')+'  →  mcd = '+a;
  pintar(pares);
};
document.getElementById('go').onclick();
</script>
''')

write_lab(30, 'Recta, predicción y causa', '''
<div class="panel">
<p>Datos del ejemplo: horas 1, 2, 3, 4, 5 y notas 2, 4, 5, 6, 8. Recta ŷ = 0,8 + 1,4x. Mueve x. Si sales de 1 a 5, la cifra es una extrapolación, no un hecho. La recta no demuestra que estudiar cause la nota.</p>
<label>x (horas) <input id="x" type="range" min="0" max="7" step="0.5" value="3"/></label>
<div class="out" id="out"></div>
<canvas id="c" width="640" height="220"></canvas>
</div>
<script>
function pintar(){
  var x=parseFloat(document.getElementById('x').value);
  var yhat=0.8+1.4*x;
  var aviso = (x<1 || x>5) ? ' Extrapolación: x no está entre 1 y 5. No es una causa demostrada.' : ' Interpolación dentro del rango. Sigue sin ser una causa: solo asociación.';
  document.getElementById('out').textContent='x = '+String(x).replace('.',',')+' · ŷ = '+yhat.toFixed(2).replace('.',',')+'.'+aviso;
  var cv=document.getElementById('c'), ctx=cv.getContext('2d');
  ctx.fillStyle='#12100e'; ctx.fillRect(0,0,640,220);
  function X(v){return 50+(v)*70;} function Y(v){return 190-v*16;}
  ctx.strokeStyle='#9A9488'; ctx.beginPath(); ctx.moveTo(40,190); ctx.lineTo(600,190); ctx.moveTo(50,200); ctx.lineTo(50,20); ctx.stroke();
  var pts=[[1,2],[2,4],[3,5],[4,6],[5,8]];
  ctx.strokeStyle='#C4A15A'; ctx.beginPath(); ctx.moveTo(X(1),Y(2.2)); ctx.lineTo(X(5),Y(7.8)); ctx.stroke();
  ctx.fillStyle='#E6E1D6';
  pts.forEach(function(p){ctx.beginPath(); ctx.arc(X(p[0]),Y(p[1]),4,0,6.3); ctx.fill();});
  ctx.strokeStyle='#8F9A72'; ctx.beginPath(); ctx.arc(X(x),Y(yhat),6,0,6.3); ctx.stroke();
}
document.getElementById('x').oninput=pintar; pintar();
</script>
''')

write_lab(32, 'Árbol con y sin reemplazo', '''
<div class="panel">
<p>Urna del ejemplo: 5 rojas y 3 azules, total 8. Se extraen dos. Compara la condicionada de la segunda roja según haya o no reemplazo.</p>
<button id="sin" type="button">Sin reemplazo</button>
<button id="con" type="button">Con reemplazo</button>
<div class="out" id="out"></div>
<canvas id="c" width="640" height="200"></canvas>
</div>
<script>
function dib(con){
  var cv=document.getElementById('c'), ctx=cv.getContext('2d');
  ctx.fillStyle='#12100e'; ctx.fillRect(0,0,640,200);
  ctx.strokeStyle='#C4A15A'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.moveTo(80,100); ctx.lineTo(240,40); ctx.moveTo(80,100); ctx.lineTo(240,160); ctx.stroke();
  ctx.strokeStyle='#8F9A72';
  ctx.beginPath(); ctx.moveTo(240,40); ctx.lineTo(420,20); ctx.moveTo(240,40); ctx.lineTo(420,70);
  ctx.moveTo(240,160); ctx.lineTo(420,130); ctx.moveTo(240,160); ctx.lineTo(420,180); ctx.stroke();
  ctx.fillStyle='#E6E1D6'; ctx.font='13px sans-serif';
  ctx.fillText('1ª', 70, 92);
  ctx.fillText('R', 230, 34); ctx.fillText('A', 230, 176);
  ctx.fillText(con?'R 5/8':'R 4/7', 430, 24);
  ctx.fillText(con?'A 3/8':'A 3/7', 430, 74);
}
document.getElementById('sin').onclick=function(){
  document.getElementById('out').textContent='Sin reemplazo: P(R2|R1)=4/7, distinta de P(R1)=5/8. No son independientes. P(RR)=20/56. P(colores distintos)=30/56.';
  dib(false);
};
document.getElementById('con').onclick=function(){
  document.getElementById('out').textContent='Con reemplazo: P(R2|R1)=5/8 = P(R1). Sí son independientes. P(RR)=25/64.';
  dib(true);
};
document.getElementById('sin').onclick();
</script>
''')

write_lab(33, 'Bayes con mil personas', '''
<div class="panel">
<p>Base de 1000 personas, como en el ejemplo. Cambia prevalencia, sensibilidad y especificidad (en %). El resultado es verdaderos positivos partido de todos los positivos, no la sensibilidad sola.</p>
<label>Prevalencia % <input id="pr" type="number" value="10" min="1" max="99"/></label>
<label>Sensibilidad % <input id="se" type="number" value="90" min="1" max="99"/></label>
<label>Especificidad % <input id="sp" type="number" value="80" min="1" max="99"/></label>
<button id="go" type="button">Reconstruir la tabla</button>
<div class="out" id="out"></div>
</div>
<script>
document.getElementById('go').onclick=function(){
  var pr=+document.getElementById('pr').value/100;
  var se=+document.getElementById('se').value/100;
  var sp=+document.getElementById('sp').value/100;
  var enf=1000*pr, san=1000-enf;
  var tp=enf*se, fn=enf-tp, tn=san*sp, fp=san-tn;
  var pos=tp+fp;
  var post=pos>0? tp/pos : 0;
  document.getElementById('out').textContent=
    'Enfermas '+enf.toFixed(0)+' (VP '+tp.toFixed(0)+', FN '+fn.toFixed(0)+'). Sanas '+san.toFixed(0)+' (FP '+fp.toFixed(0)+', VN '+tn.toFixed(0)+'). Positivos '+pos.toFixed(0)+'. P(enferma | positivo) = '+tp.toFixed(0)+' / '+pos.toFixed(0)+' = '+post.toFixed(3).replace('.',',')+'.';
};
document.getElementById('go').onclick();
</script>
''')

write_lab(34, 'Binomial n=4 y la barra del ejemplo', '''
<div class="panel">
<p>Cuatro pruebas justas, como el ejemplo. P(X=k) = C(4,k) / 16. El caso marcado en la lección es k=3.</p>
<label>k
<select id="k"><option>0</option><option>1</option><option>2</option><option selected>3</option><option>4</option></select>
</label>
<div class="out" id="out"></div>
<canvas id="c" width="640" height="200"></canvas>
</div>
<script>
function C(n,k){var r=1; for(var i=0;i<k;i++) r=r*(n-i)/(i+1); return r;}
function pintar(){
  var k=+document.getElementById('k').value;
  var probs=[1,4,6,4,1];
  document.getElementById('out').textContent='C(4,'+k+') = '+C(4,k)+' · P(X='+k+') = '+probs[k]+'/16 = '+(probs[k]/16).toFixed(4).replace('.',',')+'. La barra ámbar es la que has elegido.';
  var cv=document.getElementById('c'), ctx=cv.getContext('2d');
  ctx.fillStyle='#12100e'; ctx.fillRect(0,0,640,200);
  ctx.strokeStyle='#9A9488'; ctx.beginPath(); ctx.moveTo(40,170); ctx.lineTo(600,170); ctx.stroke();
  for(var i=0;i<5;i++){
    var h=probs[i]*18;
    ctx.fillStyle = (i===k) ? '#C4A15A' : '#3a3428';
    ctx.fillRect(70+i*90, 170-h, 50, h);
    ctx.fillStyle='#E6E1D6'; ctx.font='13px sans-serif';
    ctx.fillText(String(i), 90+i*90, 188);
  }
}
document.getElementById('k').onchange=pintar; pintar();
</script>
''')

# ---------- L27 ----------
fig27 = '''
<circle cx="130" cy="34" r="16" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<line x1="130" y1="50" x2="130" y2="68" stroke="#C4A15A" stroke-width="2"/>
<polygon points="40,68 220,68 220,112 40,112" fill="#1C1A16" stroke="#E6E1D6" stroke-width="1.6"/>
<line x1="130" y1="112" x2="130" y2="136" stroke="#C4A15A" stroke-width="2"/>
<polygon points="130,134 230,184 130,234 30,184" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<line x1="30" y1="184" x2="30" y2="262" stroke="#8F9A72" stroke-width="2"/>
<line x1="30" y1="262" x2="130" y2="262" stroke="#8F9A72" stroke-width="2"/>
<polygon points="122,254 138,254 130,270" fill="#8F9A72"/>
<polygon points="40,248 220,248 220,302 40,302" fill="#1C1A16" stroke="#8F9A72" stroke-width="1.6"/>
<line x1="230" y1="184" x2="300" y2="184" stroke="#C4A15A" stroke-width="2"/>
<circle cx="348" cy="184" r="32" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<circle cx="520" cy="48" r="8" fill="#C4A15A"/>
<circle cx="520" cy="108" r="8" fill="#C4A15A"/>
<circle cx="520" cy="168" r="8" fill="#C4A15A"/>
<circle cx="520" cy="228" r="8" fill="#8F9A72"/>
<line x1="520" y1="56" x2="520" y2="100" stroke="#C4A15A" stroke-width="2"/>
<line x1="520" y1="116" x2="520" y2="160" stroke="#C4A15A" stroke-width="2"/>
<line x1="520" y1="176" x2="520" y2="220" stroke="#C4A15A" stroke-width="2"/>
<text x="130" y="38" text-anchor="middle" fill="#E6E1D6" font-size="11">inicio</text>
<text x="130" y="94" text-anchor="middle" fill="#E6E1D6" font-size="13">a = 48 , b = 18</text>
<text x="130" y="180" text-anchor="middle" fill="#C4A15A" font-size="13">¿b = 0?</text>
<text x="44" y="176" fill="#8F9A72" font-size="12">no</text>
<text x="236" y="176" fill="#C4A15A" font-size="12">sí</text>
<text x="130" y="278" text-anchor="middle" fill="#E6E1D6" font-size="12">a, b ← b, a mod b</text>
<text x="348" y="180" text-anchor="middle" fill="#E6E1D6" font-size="12">mcd</text>
<text x="348" y="196" text-anchor="middle" fill="#C4A15A" font-size="14">6</text>
<text x="540" y="52" fill="#E6E1D6" font-size="13">48 , 18  resto 12</text>
<text x="540" y="112" fill="#E6E1D6" font-size="13">18 , 12  resto 6</text>
<text x="540" y="172" fill="#E6E1D6" font-size="13">12 , 6   resto 0</text>
<text x="540" y="232" fill="#8F9A72" font-size="13">6 , 0    parar</text>
<text x="430" y="28" fill="#C4A15A" font-size="14">traza del ejemplo 1</text>
'''
build(
27, 'Pensamiento <em>computacional</em>', 'D.5 Algoritmos, programas y herramientas offline',
'Un procedimiento que se puede seguir sin adivinar',
'El Decreto pide descomponer problemas, escribir algoritmos y usar herramientas. Aquí la herramienta es el papel: un diagrama de flujo y el algoritmo de Euclides ejecutado con 48 y 18, resto a resto, hasta que el divisor se hace cero.',
['Leer un diagrama de flujo y distinguir secuencia, decisión y bucle.',
 'Ejecutar el algoritmo de Euclides con números concretos y justificar el último resto no nulo.',
 'Detectar un algoritmo que no termina o que falla al iniciar el acumulador.'],
'''<h2>Preciso, finito y escrito en pasos</h2>
<p>Un algoritmo es una lista de instrucciones tan cerrada que otra persona, sin conocer el problema, llega al mismo resultado. No vale «haz la cuenta» ni «busca el máximo si se ve». Hacen falta una entrada, un proceso con operaciones permitidas y una salida, y hace falta que el proceso se detenga.</p>
<p><span class="glosa">secuencia = pasos uno detrás de otro · decisión = una pregunta con dos salidas (sí / no) · bucle = volver atrás mientras una condición siga siendo verdadera · resto = lo que sobra en la división entera, a módulo b · mcd = mayor entero que divide a los dos números</span></p>
<p>El diagrama de la izquierda es el de Euclides para el par del ejemplo. El rombo pregunta si b ya es 0. Si no lo es, la caja verde sustituye el par: el divisor pasa a ser el nuevo a, y el resto pasa a ser el nuevo b. La flecha vuelve al rombo. Si b es 0, se sale y la respuesta es el a que queda. A la derecha está la traza concreta, no un esquema vacío: (48, 18), (18, 12), (12, 6) y (6, 0).</p>
<p>Esa misma disciplina sirve para un bucle que suma o para uno que busca un máximo. El fallo típico no es «no se me dan los algoritmos»: o falta la actualización que acerca el proceso al final, o el valor inicial no pertenece al conjunto de datos. Las dos cosas se ven al ejecutar tres vueltas con números, que es lo que pide esta lección.</p>
<table class="datos"><thead><tr><th>Pieza</th><th>En el ejemplo</th><th>Si falta</th></tr></thead>
<tbody>
<tr><td>Entrada</td><td>a = 48, b = 18</td><td>No hay caso que ejecutar</td></tr>
<tr><td>Condición</td><td>¿b = 0?</td><td>No se sabe cuándo salir</td></tr>
<tr><td>Actualización</td><td>(a, b) ← (b, a mod b)</td><td>El rombo no cambia nunca</td></tr>
<tr><td>Salida</td><td>6</td><td>El proceso no devuelve el mcd</td></tr>
</tbody></table>''',
'Diagrama de Euclides con el par 48 y 18 y la traza de restos 12, 6 y 0', fig27,
[
('Euclides con 48 y 18',
 'Ejecuta el algoritmo de la figura con a = 48 y b = 18. Escribe cada división, el par nuevo y el motivo para parar. Comprueba que 6 divide a los dos.',
 [
  ('Primera vuelta: 48 = 2 · 18 + 12. El cociente es 2 y el resto es 12, así que el par pasa a ser (18, 12).',
   'Glosa: 2 · 18 = 36 y 48 − 36 = 12. El resto tiene que ser menor que el divisor.'),
  ('Segunda vuelta: 18 = 1 · 12 + 6. El par pasa a ser (12, 6). El mcd todavía no es 12: el resto no es cero.',
   'Glosa: se para solo cuando el resto es 0, no cuando el resto «ya es pequeño».'),
  ('Tercera vuelta: 12 = 2 · 6 + 0. El par pasa a ser (6, 0). La condición del rombo ya es sí, y la salida es 6.',
   'Glosa: el último divisor no nulo, que ahora está en a, es el máximo común divisor.'),
  ('Comprobación: 48 = 6 · 8 y 18 = 6 · 3. No hay un entero mayor que divida a los dos, porque el algoritmo agota los restos.',
   'Glosa: 8 y 3 son coprimos; si hubiera un divisor común mayor que 6, también dividiría al resto 0 de forma contradictoria con los pasos.'),
 ]),
('Suma de 1 a 5, bucle y atajo',
 'Un algoritmo hace s = 0 y, para i desde 1 hasta 5, s = s + i. Ejecútalo vuelta a vuelta y compáralo con la fórmula n(n+1)/2.',
 [
  ('Estado inicial: s = 0 e i = 1. La primera suma deja s = 1. No se empieza en el resultado.',
   'Glosa: el acumulador tiene que nacer en el elemento neutro de la suma, que es 0.'),
  ('Siguientes vueltas: i = 2 deja s = 3; i = 3 deja s = 6; i = 4 deja s = 10; i = 5 deja s = 15. Ahí el bucle corta.',
   'Glosa: el límite superior es 5 inclusive. Parar en 4 olvidaría el último sumando.'),
  ('La fórmula con n = 5 da 5 · 6 / 2 = 15. Coincide con el bucle, así que el atajo no cambia el problema.',
   'Glosa: la fórmula es otro algoritmo para la misma salida; si no coincidiera, habría un límite mal puesto.'),
  ('Si el bucle llegara hasta 6, saldría 21, y la fórmula de n = 5 seguiría diciendo 15. El desajuste delata el error de límite, no «que la fórmula falle».',
   'Glosa: se depura comparando dos procedimientos sobre el mismo n, no discutiendo en abstracto.'),
 ]),
('El máximo no puede nacer en cero',
 'Lista: −3, −1, −8. Algoritmo A inicia m en el primer dato. Algoritmo B inicia m en 0 y solo actualiza si el dato es mayor. Ejecuta los dos.',
 [
  ('Algoritmo A: m = −3. El −1 es mayor, así que m = −1. El −8 no lo supera. Salida −1, que sí está en la lista.',
   'Glosa: empezar en el primer dato garantiza que m siempre es uno de los valores leídos.'),
  ('Algoritmo B: m = 0. Ningún dato es mayor que 0, así que m no se mueve. La salida es 0, y 0 no está en la lista.',
   'Glosa: el fallo es la inicialización, no la comparación. Con números positivos el mismo B habría parecido correcto.'),
  ('La decisión «dato mayor que m» está bien escrita en los dos. Lo que cambia el resultado es el valor de entrada del acumulador.',
   'Glosa: un ejemplo con negativos es una prueba de escritorio: busca el caso que rompe el algoritmo, no el caso cómodo.'),
  ('Corrección de B: o se inicia m con el primer elemento, o se declara que la lista es de números no negativos. Sin esa hipótesis, B es incorrecto.',
   'Glosa: un algoritmo correcto necesita decir para qué entradas promete funcionar.'),
 ]),
],
[
(1, 'Euclides con 30 y 21',
 'Calcula mcd(30, 21) con el mismo algoritmo. Escribe los tres restos y di por qué la salida no es el último cociente.',
 'El paso que hay que escribir es la división entera, no un «se ve que es 3». 30 = 1 · 21 + 9, así que el par pasa a (21, 9). Después 21 = 2 · 9 + 3 y el par pasa a (9, 3). Después 9 = 3 · 3 + 0 y se para: el mcd es 3, el último resto no nulo. El último cociente es también 3, pero eso es casualidad de este ejemplo; en 48 y 18 el último cociente era 2 y el mcd era 6. Por eso la regla es leer a cuando b llega a 0, no leer el cociente. Comprobación: 30 = 3 · 10 y 21 = 3 · 7.',
 'e27a'),
(2, 'Un mientras que no se mueve',
 'Pseudocódigo: x = 3; mientras x sea mayor que 0, escribir x. No hay ninguna otra línea. ¿Qué ocurre en las tres primeras vueltas y qué propiedad del algoritmo falta?',
 'El paso ausente es la actualización de x. Primera vuelta: x = 3, la condición es verdadera y se escribe 3. Segunda vuelta: x sigue siendo 3, porque nadie lo ha restado, y se vuelve a escribir 3. La tercera es idéntica. La condición no se acerca a ser falsa, así que el algoritmo no termina. En la definición que usamos en esta lección, terminar forma parte del algoritmo: un bucle solo es válido si cada vuelta cambia el estado hacia la salida, como el resto de Euclides, que es siempre menor que el divisor anterior y no puede bajar indefinidamente en los enteros no negativos.',
 'e27b'),
(3, 'Contar aprobados',
 'Notas 4, 7, 5, 3, 9. Escribe un algoritmo que cuente cuántas son mayores o iguales que 5 y ejecútalo. Di qué pasa si la condición se escribe mal como «mayor que 5».',
 'El paso es un contador que nace en 0 y solo suma 1 cuando la condición es verdadera, no sumar la propia nota. Con el umbral bien puesto: 4 no; 7 sí (c = 1); 5 sí (c = 2); 3 no; 9 sí (c = 3). Salida 3. Si la condición se cambia a «mayor que 5», el 5 deja de contarse y la salida es 2. El algoritmo no está «casi bien»: el borde del aprobado, que el Decreto y la evaluación colocan en 5, hay que copiarlo con el igual. Por eso se prueba el caso frontera, no solo un 9 y un 3.',
 'e27c'),
],
[
('¿Por qué en la figura se para al llegar al par (6, 0)?',
 'Porque b ya es 0 y el rombo sale hacia el círculo de la respuesta. Por qué: el resto 0 significa que 6 divide exactamente a 12, y los restos anteriores garantizan que 6 también divide a 18 y a 48. Seguir no tiene sentido: el módulo con divisor 0 no está definido.'),
('¿Qué dato de la lista −3, −1, −8 delata al algoritmo que empieza en 0?',
 'Que la salida 0 no pertenece a la lista. Por qué: un máximo de la lista tiene que ser uno de sus elementos. Si todas las pruebas se hacen con números positivos, el 0 inicial se sustituye enseguida y el error queda escondido. El caso negativo es el que obliga a corregir el inicio.'),
('¿La fórmula n(n+1)/2 sustituye al bucle o lo comprueba?',
 'Lo comprueba y, cuando ya se sabe que coinciden, también lo abrevia. Por qué: con n = 5 los dos dan 15. Si en otro n no dieran lo mismo, no se «elige el que guste»: se revisa el límite del bucle o el uso de la fórmula. Dos algoritmos de la misma función tienen que devolver la misma salida.'),
],
'Euclides en tu libreta',
'Elige dos enteros positivos menores que 100, dibuja en el lienzo el rombo y tres cajas con tus restos reales, y escribe al lado el mcd. No copies 48 y 18.',
['El rombo pregunta si b es 0. Con 48 y 18 la respuesta tarda tres restos: 12, 6 y 0.',
 'La columna de la derecha es la traza, no un adorno: cada círculo es un par.',
 'Ejemplo 1: el mcd es 6, y 6 no es el último cociente, que era 2.',
 'Ejemplo 2: el bucle de la suma acaba en 15, igual que 5·6/2.',
 'Ejemplo 3: iniciar el máximo en 0 falla en cuanto aparecen negativos.',
 'En el laboratorio cambia el par y mira cómo encogen las barras.',
 'Un algoritmo que no cambia su variable de control no es un algoritmo: no termina.'],
lab_title='Euclides paso a paso')

print('L27 escrito')

# ---------- L28 ----------
_bars = []
_bars.append('<line x1="70" y1="270" x2="680" y2="270" stroke="#9A9488" stroke-width="1.6"/>')
_bars.append('<line x1="70" y1="270" x2="70" y2="36" stroke="#9A9488" stroke-width="1.6"/>')
for _v in (0, 2, 4, 6, 8):
    _y = 270 - _v * 26
    _bars.append(f'<line x1="70" y1="{_y}" x2="660" y2="{_y}" stroke="#3a3428" stroke-width="1"/>')
    _bars.append(f'<text x="40" y="{_y+4}" fill="#9A9488" font-size="12">{_v}</text>')
_fx = [130, 240, 350, 460, 570]
_ff = [2, 5, 7, 4, 2]
for _i, _f in enumerate(_ff):
    _h = _f * 26
    _yt = 270 - _h
    _col = '#E6E1D6' if _i == 2 else '#C4A15A'
    _bars.append(barra(_fx[_i], _yt, 70, _h, _col))
    _bars.append(f'<text x="{_fx[_i]+35}" y="{_yt-8}" text-anchor="middle" fill="#C4A15A" font-size="14">{_f}</text>')
    _bars.append(f'<text x="{_fx[_i]+35}" y="292" text-anchor="middle" fill="#E6E1D6" font-size="14">{_i}</text>')
_bars.append('<text x="90" y="24" fill="#C4A15A" font-size="14">20 alumnos · libros en el trimestre · la barra clara es la moda</text>')
fig28 = '\n'.join(_bars)
build(
28, 'Estadística: leer <em>sin deformar</em>', 'E.1 Interpretación y análisis de información estadística',
'La barra mide personas, no un adorno',
'En un grupo de 20 alumnos se ha contado cuántos libros leyó cada uno en el trimestre: 0, 1, 2, 3 o 4. Las frecuencias son 2, 5, 7, 4 y 2. El gráfico pone escala desde cero para que la altura sea proporcional a esas frecuencias.',
['Calcular media, mediana y moda de una distribución concreta y no confundirlas.',
 'Comparar dos grupos por la media y no por el total, cuando los tamaños son distintos.',
 'Explicar por qué un eje que no nace en cero deforma la comparación de barras.'],
'''<h2>Frecuencia, promedio y escala</h2>
<p>Interpretar estadística no es repetir el número que destaca el titular. Hay que saber qué se ha contado, cuántos individuos hay y qué operación resume la distribución. En el gráfico cada barra es un número de alumnos, no un «nivel de lectura» inventado.</p>
<p><span class="glosa">frecuencia = cuántos individuos caen en ese valor · media = suma de todos los valores dividida entre el número de individuos · mediana = valor central de la lista ordenada · moda = valor de mayor frecuencia · el eje vertical de un diagrama de barras de frecuencias empieza en 0</span></p>
<p>Los 20 datos suman 0·2 + 1·5 + 2·7 + 3·4 + 4·2 = 39 libros. La media es 39/20 = 1,95. La lista ordenada tiene 20 puestos: los puestos 10 y 11 caen los dos en el valor 2 (la barra de 2 ocupa desde el puesto 8 hasta el 14), así que la mediana es 2. La moda también es 2, porque su frecuencia, 7, es la mayor. Media, mediana y moda no tienen por qué coincidir; aquí la media queda un poco por debajo porque los ceros tiran hacia abajo.</p>
<p>Un segundo grupo de 10 alumnos suma 30 libros. Su total es menor (30 frente a 39), pero su media es 30/10 = 3, mayor que 1,95. Quien compare totales dirá que el primer grupo lee más; quien compare medias dirá que el alumno típico del segundo grupo lee más. Las dos frases hablan de cosas distintas y solo la segunda compara individuos.</p>
<table class="datos"><thead><tr><th>Libros</th><th>Alumnos</th><th>Libros · alumnos</th><th>Acumulada</th></tr></thead>
<tbody>
<tr><td>0</td><td>2</td><td>0</td><td>2</td></tr>
<tr><td>1</td><td>5</td><td>5</td><td>7</td></tr>
<tr><td>2</td><td>7</td><td>14</td><td>14</td></tr>
<tr><td>3</td><td>4</td><td>12</td><td>18</td></tr>
<tr><td>4</td><td>2</td><td>8</td><td>20</td></tr>
</tbody></table>''',
'Barras de frecuencias 2, 5, 7, 4 y 2 con escala de 0 a 8', fig28,
[
('Media, mediana y moda del gráfico',
 'Con las frecuencias de la figura, calcula la media, explica por qué la mediana es 2 y señala la moda. Redondea la media a dos decimales.',
 [
  ('La suma de libros es 0·2 + 1·5 + 2·7 + 3·4 + 4·2 = 5 + 14 + 12 + 8 = 39. Hay 20 alumnos, no 5 valores distintos.',
   'Glosa: el denominador de la media es el número de individuos, la suma de las frecuencias.'),
  ('Media = 39/20 = 1,95 libros por alumno. No se divide entre 4, que es solo el valor más alto de la tabla.',
   'Glosa: dividir entre el número de categorías es un error distinto de dividir entre n − 1.'),
  ('Ordenados, los puestos 10 y 11 están dentro de la acumulada 14, que corresponde al valor 2. Mediana = 2.',
   'Glosa: con n par se miran los dos puestos centrales; aquí los dos valen 2 y no hay que promediar valores distintos.'),
  ('La moda es 2 porque la frecuencia 7 es mayor que 5, 4 y 2. En la figura es la barra clara, y la escala permite ver que 7 no es el doble de 5.',
   'Glosa: 7/5 = 1,4. La barra de 7 es 1,4 veces la de 5, no «muchísimo mayor».'),
 ]),
('Dos grupos, dos preguntas',
 'El grupo A es el de la figura: 20 alumnos y 39 libros. El grupo B tiene 10 alumnos y 30 libros. ¿Qué grupo ha leído más libros en total? ¿En qué grupo lee más un alumno típico?',
 [
  ('Total de A: 39. Total de B: 30. En conjunto, A ha leído más libros. Esa frase no habla del alumno típico.',
   'Glosa: el total crece con el tamaño del grupo aunque cada persona lea poco.'),
  ('Media de A: 39/20 = 1,95. Media de B: 30/10 = 3. El alumno típico de B lee más.',
   'Glosa: para comparar individuos hay que usar el mismo tipo de promedio, aquí la media aritmética.'),
  ('Si alguien dice «A lee más porque 39 es mayor que 30», ha cambiado la pregunta sin avisar. El paso es escribir la pregunta antes de elegir el número.',
   'Glosa: total y media responden a decisiones distintas: comprar libros para el grupo, o describir un hábito individual.'),
  ('Comprobación de B: 3 · 10 = 30, cierra. No hace falta la lista de B para esta comparación, pero sí su tamaño. Sin el 10, el 30 no se interpreta.',
   'Glosa: un total sin n no permite calcular la media. Pedir n forma parte de leer la estadística.'),
 ]),
('El eje que empieza en 4',
 'Alguien redibuja las frecuencias 5 y 7 (un libro y dos libros) con el eje vertical empezando en 4. Las alturas visibles pasan a ser 1 y 3. Explica la deformación.',
 [
  ('Con el eje en cero, las alturas están en razón 7:5 = 1,4. La diferencia real es de 2 alumnos.',
   'Glosa: la proporción de las barras copia la proporción de las frecuencias solo si el cero está en el eje.'),
  ('Si el eje nace en 4, se ha borrado la misma cantidad en las dos barras. Queda 7 − 4 = 3 frente a 5 − 4 = 1. La razón visible es 3, más del doble.',
   'Glosa: restar 4 a los dos datos no conserva el cociente. Por eso el recorte del eje exagera.'),
  ('El gráfico recortado sirve para ver una diferencia pequeña en una escala fina, pero entonces hay que decirlo. Si se presenta como retrato de las frecuencias, engaña.',
   'Glosa: en esta lección el diagrama de barras de frecuencias lleva el cero. La figura del ejemplo lo cumple.'),
  ('La moda seguiría siendo 2, porque 7 sigue siendo mayor que 5, pero un lector que solo mira «cuánto más alta» sacaría una conclusión inflada. Interpretar incluye mirar el eje.',
   'Glosa: el título de la barra no basta; la unidad del eje es parte del dato.'),
 ]),
],
[
(1, 'Otro recuento pequeño',
 'Cuatro datos: 3, 5, 5 y 7. Calcula media, mediana y moda, y di por qué el denominador es 4.',
 'El paso es sumar los cuatro datos y dividir entre cuatro, porque cada dato es un individuo y no hay frecuencias agrupadas que recontar. La suma es 3 + 5 + 5 + 7 = 20 y la media es 20/4 = 5. Ordenados ya están 3, 5, 5, 7; con n = 4 los puestos centrales son el 2.º y el 3.º, los dos valen 5, y la mediana es 5. La moda es 5 porque se repite y los otros valores no. Dividir entre 3, que es la cantidad de números distintos, daría 20/3 y describiría otra cosa: no es la media de estos cuatro alumnos.',
 'e28a'),
(2, 'Porcentaje sobre las barras',
 'En el gráfico, ¿qué porcentaje del grupo leyó al menos 2 libros? Explica qué frecuencias entran y cuál es el denominador.',
 'El paso es sumar las frecuencias que cumplen la condición y dividir entre 20, no entre 5 categorías. Entran las barras de 2, 3 y 4 libros: 7 + 4 + 2 = 13 alumnos. El porcentaje es 13/20 = 0,65, es decir el 65 %. Dejar fuera la barra de 2 sería leer «más de 2» cuando el enunciado dice «al menos 2». El denominador no es 13: 13 es el numerador, los que cumplen. Si se usa como denominador la frecuencia de la moda, 7, se obtiene un cociente mayor que 1 y deja de ser una proporción del grupo.',
 'e28b'),
(3, 'Titular con el total',
 'Un titular dice: «El grupo A lee más que el B» usando solo 39 y 30. Escribe la frase correcta según se hable del total o de la media, con los tamaños 20 y 10.',
 'El paso es no aceptar un verbo («lee más») mientras no esté dicho el sujeto: el grupo entero o el alumno típico. Con los totales, A suma 39 libros y B suma 30, así que el grupo A, en conjunto, ha leído más. Con las medias, 39/20 = 1,95 y 30/10 = 3, así que un alumno de B lee más por término medio. Las dos frases pueden ser verdaderas a la vez porque comparan magnitudes distintas. El error del titular es presentar una de ellas como si fuera la otra, sin escribir n. En cuanto se recuperan los tamaños, la ambigüedad se deshace con una división.',
 'e28c'),
],
[
('¿Cuánto vale la media del gráfico y por qué el denominador es 20?',
 'Vale 1,95 porque 39/20 = 1,95. Por qué: 39 es la suma de libros de todos los alumnos y 20 es el número de alumnos, no el número de barras. Hay cinco barras, pero las frecuencias 2, 5, 7, 4 y 2 ya dicen cuántas personas hay detrás de cada una.'),
('¿Por qué la mediana no es 1,95?',
 'Porque la mediana no usa la suma: usa el centro de la lista ordenada. Por qué: los puestos 10 y 11, de 20, caen en el valor 2. La media se desplaza a 1,95 porque los dos ceros pesan en la suma y en la mediana solo ocupan los primeros puestos, lejos del centro.'),
('¿Qué le pasa a la comparación entre las frecuencias 5 y 7 si el eje empieza en 4?',
 'La razón de alturas pasa de 7/5 = 1,4 a 3/1 = 3, y la diferencia parece mucho mayor de lo que es. Por qué: se ha restado el mismo 4 a las dos frecuencias y el cociente no se conserva. El diagrama del ejemplo evita eso porque la escala nace en 0 y cada unidad vertical es un mismo número de alumnos.'),
],
'Tu diagrama con cero',
'Dibuja en el lienzo cinco barras con frecuencias distintas, escribe la escala desde 0 y calcula al lado la moda. No recortes el eje.',
['Escala vertical de 0 a 8. Frecuencias escritas encima: 2, 5, 7, 4 y 2.',
 'La barra clara es la de 2 libros, frecuencia 7, la moda.',
 'Ejemplo 1: suma 39, media 1,95, mediana 2, moda 2.',
 'Ejemplo 2: el total 39 no se compara con el total 30 sin dividir entre 20 y entre 10.',
 'Ejemplo 3: recortar el eje en 4 cambia la razón 7:5 en la razón 3:1.',
 'El porcentaje de quien leyó al menos 2 libros usa el denominador 20.',
 'Leer una barra incluye leer el cero del eje.'],
)

print('L28 escrito')

# ---------- L29 ----------
fig29 = '''
<line x1="40" y1="40" x2="680" y2="40" stroke="#C4A15A" stroke-width="1.6"/>
<line x1="40" y1="90" x2="680" y2="90" stroke="#9A9488" stroke-width="1.2"/>
<line x1="40" y1="150" x2="680" y2="150" stroke="#9A9488" stroke-width="1.2"/>
<line x1="40" y1="210" x2="680" y2="210" stroke="#9A9488" stroke-width="1.2"/>
<line x1="40" y1="270" x2="680" y2="270" stroke="#C4A15A" stroke-width="1.6"/>
<line x1="40" y1="40" x2="40" y2="270" stroke="#9A9488" stroke-width="1.2"/>
<line x1="220" y1="40" x2="220" y2="270" stroke="#9A9488" stroke-width="1.2"/>
<line x1="380" y1="40" x2="380" y2="270" stroke="#9A9488" stroke-width="1.2"/>
<line x1="530" y1="40" x2="530" y2="270" stroke="#C4A15A" stroke-width="1.6"/>
<line x1="680" y1="40" x2="680" y2="270" stroke="#9A9488" stroke-width="1.2"/>
<circle cx="300" cy="120" r="16" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<circle cx="455" cy="180" r="16" fill="#1C1A16" stroke="#8F9A72" stroke-width="2"/>
<text x="70" y="72" fill="#9A9488" font-size="14">método</text>
<text x="270" y="72" fill="#C4A15A" font-size="14">aprueba</text>
<text x="420" y="72" fill="#E6E1D6" font-size="14">suspende</text>
<text x="570" y="72" fill="#C4A15A" font-size="14">total</text>
<text x="70" y="126" fill="#E6E1D6" font-size="15">apuntes</text>
<text x="292" y="126" fill="#E6E1D6" font-size="16">8</text>
<text x="445" y="126" fill="#E6E1D6" font-size="16">10</text>
<text x="590" y="126" fill="#C4A15A" font-size="16">18</text>
<text x="70" y="186" fill="#E6E1D6" font-size="15">ejercicios</text>
<text x="284" y="186" fill="#E6E1D6" font-size="16">16</text>
<text x="448" y="186" fill="#E6E1D6" font-size="16">6</text>
<text x="590" y="186" fill="#C4A15A" font-size="16">22</text>
<text x="70" y="248" fill="#C4A15A" font-size="15">total</text>
<text x="284" y="248" fill="#C4A15A" font-size="16">24</text>
<text x="445" y="248" fill="#C4A15A" font-size="16">16</text>
<text x="590" y="248" fill="#C4A15A" font-size="16">40</text>
<text x="300" y="124" text-anchor="middle" fill="#C4A15A" font-size="12">8</text>
'''
build(
29, 'Variables <em>bidimensionales</em>', 'E.1 Conjunta, marginales, condicionadas y dependencia',
'El denominador cambia cuando se condiciona',
'Cuarenta alumnos eligieron estudiar con apuntes o con ejercicios, y luego aprobaron o suspendieron. La tabla de la figura es la distribución conjunta. La columna de totales es la marginal del método; la fila de totales es la marginal del resultado. Una condicionada cambia el denominador: ya no son los 40.',
['Leer una tabla de contingencia y localizar conjunta, marginal y condicionada.',
 'Calcular una probabilidad condicionada restringiendo el denominador a la fila o a la columna indicada.',
 'Decidir dependencia comparando la condicionada con la marginal, no con una impresión visual.'],
'''<h2>Conjunta, marginal y condicionada</h2>
<p>Dos variables categóricas sobre las mismas personas se cruzan en una tabla. Cada celda interior es una frecuencia conjunta: las dos cosas a la vez. Sumar una fila o una columna borra una de las variables y deja la marginal. Condicionar es negarse a hacer esa suma y usar como total solo el grupo que ya cumple la condición.</p>
<p><span class="glosa">conjunta = frecuencia de una celda interior · marginal = suma de una fila o de una columna · condicionada = celda dividida entre el total de su fila o de su columna, no entre el total de la tabla · dependencia = alguna condicionada distinta de la marginal correspondiente</span></p>
<p>En el ejemplo hay 40 alumnos. Aprueban 24, así que la marginal de aprobar es 24/40 = 0,60. Entre quienes hicieron ejercicios hay 22 personas y aprueban 16, así que la condicionada es 16/22 = 8/11 ≈ 0,727. No es el mismo número: saber el método cambia la probabilidad de aprobar. Entre quienes usaron apuntes, 8/18 = 4/9 ≈ 0,444. Las dos condicionadas se separan de la marginal, una por arriba y otra por abajo.</p>
<p>Eso no dice que los ejercicios causen el aprobado. La tabla mide asociación en este grupo: puede haber motivación previa, horario u otra variable no recogida. Lo que sí queda cerrado con estas cifras es que las variables no son independientes, porque independencia exigiría que aprobar tuviera la misma proporción en cada fila y, por tanto, la misma que en el total.</p>
<table class="datos"><thead><tr><th></th><th>Aprueba</th><th>Suspende</th><th>Total</th></tr></thead>
<tbody>
<tr><td>Apuntes</td><td>8</td><td>10</td><td>18</td></tr>
<tr><td>Ejercicios</td><td>16</td><td>6</td><td>22</td></tr>
<tr><td>Total</td><td>24</td><td>16</td><td>40</td></tr>
</tbody></table>''',
'Tabla de contingencia 8, 10, 16 y 6 con marginales 18, 22, 24, 16 y total 40', fig29,
[
('Marginal y condicionada de aprobar',
 'Con la tabla de la figura, calcula la probabilidad marginal de aprobar y la condicionada a haber elegido ejercicios. Explica el cambio de denominador.',
 [
  ('Marginal: se usa la fila de totales, no una celda suelta. Aprueban 24 de 40, luego 24/40 = 3/5 = 0,60.',
   'Glosa: 24 es 8 + 16. Si se olvida una celda, la marginal ya no cuadra con el total 40.'),
  ('Condicionada a ejercicios: el grupo ya no son los 40, son los 22 de esa fila. Aprueban 16, luego 16/22 = 8/11 ≈ 0,727.',
   'Glosa: condicionar es cambiar el universo. El 16 sigue siendo la celda conjunta; lo que cambia es el denominador.'),
  ('Comparación: 0,727 es mayor que 0,60. En este grupo, la fila de ejercicios aprueba en una proporción más alta que el conjunto.',
   'Glosa: la diferencia no es pequeña ni un redondeo: 8/11 − 3/5 = 40/55 − 33/55 = 7/55 ≈ 0,127.'),
  ('La otra fila comprueba el desequilibrio: apuntes, 8/18 ≈ 0,444, por debajo de 0,60. Las dos filas no copian la marginal.',
   'Glosa: si las dos condicionadas valieran 0,60, las celdas serían 0,60·18 y 0,60·22, y no son 8 y 16.'),
 ]),
('La conjunta no es la condicionada',
 'Calcula la probabilidad conjunta de «ejercicios y aprueba» y compárala con la condicionada 16/22. ¿Por qué la conjunta es más pequeña?',
 [
  ('Conjunta: la celda 16 sobre el total de la tabla, 16/40 = 0,40. El denominador vuelve a ser todo el grupo.',
   'Glosa: «y» pide la intersección dentro de los 40, no dentro de los 22.'),
  ('Condicionada: 16/22 ≈ 0,727, ya calculada. Es mayor porque se han quitado del denominador los 18 de apuntes.',
   'Glosa: al quitar gente del denominador sin quitar los 16 del numerador, el cociente sube.'),
  ('Relación: condicionada = conjunta / marginal de la condición. 0,40 / (22/40) = 0,40 / 0,55 = 16/22. Cuadra.',
   'Glosa: 22/40 = 0,55 es la marginal de elegir ejercicios. No hace falta memorizar la fórmula si se ve el recorte del denominador.'),
  ('Error típico: decir que la conjunta es 16/22 porque «son los que hacen ejercicios y aprueban». Esa frase describe la celda, pero el «de cuántos» sigue siendo una decisión aparte.',
   'Glosa: la celda no trae el denominador escrito. Lo elige la pregunta.'),
 ]),
('¿Independientes?',
 'Comprueba si «aprobar» y «elegir ejercicios» son independientes comparando la conjunta con el producto de las marginales.',
 [
  ('Marginal de aprobar: 24/40 = 0,60. Marginal de ejercicios: 22/40 = 0,55. Producto: 0,60 · 0,55 = 0,33.',
   'Glosa: independencia significa que la conjunta factoriza en el producto de las marginales.'),
  ('Conjunta real: 16/40 = 0,40. Como 0,40 no es 0,33, en esta tabla las variables no son independientes.',
   'Glosa: 0,40 − 0,33 = 0,07. No es un error de redondeo de la celda 16.'),
  ('La misma conclusión salía al comparar 16/22 con 24/40. Son dos escrituras del mismo hecho: la fila no reproduce la proporción global.',
   'Glosa: si hubiera independencia, 16 tendría que ser aproximadamente 0,33 · 40 = 13,2, no 16.'),
  ('Independencia no se decide porque las dos variables «hablen de cosas distintas». Se decide con esta igualdad, y aquí falla.',
   'Glosa: método y resultado podrían haber sido independientes; los datos dicen que en este grupo no lo son.'),
 ]),
],
[
(1, 'Condicionada al otro método',
 'Calcula la probabilidad de suspender condicionada a haber estudiado con apuntes. No uses el total 40 como denominador.',
 'El paso es encerrarse en la fila de apuntes, cuyo total es 18, y leer la celda de suspende, que es 10. La condicionada es 10/18 = 5/9 ≈ 0,556. Si se divide 10 entre 40 se obtiene la conjunta 0,25, que responde a «¿qué fracción del grupo entero usó apuntes y suspendió?», no a «entre quienes usaron apuntes, ¿qué fracción suspendió?». El 16 del margen de suspende tampoco sirve: mezcla los 10 de apuntes con los 6 de ejercicios. La fila de la condición es el único denominador correcto, y 10 + 8 = 18 comprueba que la fila está completa.',
 'e29a'),
(2, 'Marginal del método',
 '¿Qué probabilidad hay de que un alumno del grupo hubiera elegido ejercicios, sin mirar si aprobó? ¿Por qué no vale usar solo la columna de aprobados?',
 'El paso es sumar la fila entera de ejercicios, aprobados y suspensos, y dividir entre 40. La fila suma 16 + 6 = 22, luego 22/40 = 0,55. La columna de aprobados tiene 16 ejercicios frente a 8 apuntes, y 16/24 ≈ 0,667 es otra probabilidad: la de haber elegido ejercicios condicionada a haber aprobado. Quien solo mira a los que aprueban está condicionando por el resultado y ya no describe el método en el grupo completo. Las dos cifras, 0,55 y 0,667, se parecen en el tema y no son intercambiables, porque una divide entre 40 y la otra entre 24.',
 'e29b'),
(3, 'Dependencia en una frase',
 'Escribe la comparación numérica que demuestra que aprobar depende del método en esta tabla, y una frase que no convierta esa dependencia en causa.',
 'El paso es poner una condicionada al lado de la marginal: 16/22 ≈ 0,727 frente a 24/40 = 0,60. Como no coinciden, la proporción de aprobados cambia al saber el método, y eso es dependencia en la tabla. La frase causal que no está justificada sería «los ejercicios hacen aprobar». La tabla no dice qué pasaría si los de apuntes pasaran a ejercicios: no es un experimento, es un cruce de lo que ya eligieron. Se puede afirmar la diferencia de proporciones y hay que parar antes de la causa. La fila de apuntes, 8/18 ≈ 0,444, refuerza que el método y el resultado van juntos en estos 40 alumnos, sin identificar el mecanismo.',
 'e29c'),
],
[
('¿Cuál es el denominador de «aprueba dado ejercicios»?',
 '22, el total de la fila de ejercicios. Por qué: la condición fija el grupo antes de mirar el resultado. Los 40 incluyen a quienes usaron apuntes, y esos no entran en esta pregunta. El numerador es la celda 16, así que el cociente es 16/22.'),
('¿Por qué 16/40 y 16/22 no son la misma probabilidad?',
 'Porque 16/40 es conjunta y 16/22 es condicionada. Por qué: las dos usan la misma celda y cambian el «de cuántos». 16/40 cuenta sobre todo el grupo; 16/22 cuenta solo sobre la fila de la condición. Numéricamente 0,40 frente a aproximadamente 0,727.'),
('¿Qué igualdad fallaría si las variables fueran independientes?',
 'La conjunta 16/40 = 0,40 tendría que igualar al producto de marginales 0,60 · 0,55 = 0,33. Por qué: independencia significa que saber el método no cambia la proporción de aprobados, y entonces la celda se predice multiplicando. Aquí 0,40 no es 0,33, así que hay dependencia en la tabla, que no es lo mismo que haber demostrado una causa.'),
],
'La fila y el total',
'Copia en el lienzo la tabla de 40 alumnos, rodea la fila que usarías como denominador para condicionar a ejercicios y escribe al lado las dos fracciones 24/40 y 16/22.',
['La cuadrícula es la tabla del ejemplo: celdas 8, 10, 16 y 6, y el 40 en la esquina.',
 'El círculo ámbar marca la celda 16, la que entra en la condicionada a ejercicios.',
 'Ejemplo 1: 24/40 = 0,60 y 16/22 ≈ 0,727. El denominador cambia.',
 'Ejemplo 2: la conjunta 16/40 = 0,40 no es la condicionada.',
 'Ejemplo 3: 0,40 no coincide con 0,60 · 0,55 = 0,33, luego no hay independencia.',
 'Suspender entre los de apuntes usa el 18, no el 40.',
 'Dependencia en la tabla no es, por sí sola, una causa.'],
)

print('L29 escrito')

# ---------- L30 ----------
def _X30(x):
    return 80 + x * 90
def _Y30(y):
    return 280 - y * 24
_line30 = path_fn(lambda x: 0.8 + 1.4 * x, 1, 5, 8, _X30, _Y30)
_pts30 = []
for _x, _y in ((1, 2), (2, 4), (3, 5), (4, 6), (5, 8)):
    _pts30.append(f'<circle cx="{_X30(_x):.0f}" cy="{_Y30(_y):.0f}" r="6" fill="#E6E1D6" stroke="#C4A15A" stroke-width="1.5"/>')
    _pts30.append(f'<text x="{_X30(_x)+10}" y="{_Y30(_y)-8}" fill="#9A9488" font-size="12">({_x}, {_y})</text>')
fig30 = f'''
<line x1="70" y1="280" x2="660" y2="280" stroke="#9A9488" stroke-width="1.6"/>
<line x1="80" y1="290" x2="80" y2="30" stroke="#9A9488" stroke-width="1.6"/>
<line x1="80" y1="{_Y30(2):.0f}" x2="90" y2="{_Y30(2):.0f}" stroke="#9A9488" stroke-width="1.2"/>
<line x1="80" y1="{_Y30(5):.0f}" x2="90" y2="{_Y30(5):.0f}" stroke="#9A9488" stroke-width="1.2"/>
<line x1="80" y1="{_Y30(8):.0f}" x2="90" y2="{_Y30(8):.0f}" stroke="#9A9488" stroke-width="1.2"/>
{_line30}
{''.join(_pts30)}
<text x="100" y="24" fill="#C4A15A" font-size="14">horas de estudio y nota · recta 0,8 + 1,4x · cinco puntos del ejemplo</text>
<text x="400" y="300" fill="#9A9488" font-size="13">x horas</text>
<text x="24" y="160" fill="#9A9488" font-size="13">nota</text>
'''
build(
30, 'Regresión, correlación y <em>causalidad</em>', 'E.1 Recta de regresión; correlación no es causa',
'La nube se alinea y aun así no manda',
'Cinco alumnos: 1, 2, 3, 4 y 5 horas de estudio, con notas 2, 4, 5, 6 y 8. La recta de mínimos cuadrados es ŷ = 0,8 + 1,4x y la correlación sale altísima. El ejemplo siguiente, con datos esquemáticos de helados y ahogamientos, enseña que una asociación igual de clara puede venir de una tercera variable.',
['Calcular la pendiente y la ordenada de una recta de mínimos cuadrados con cinco puntos.',
 'Leer la correlación como fuerza de la asociación lineal, no como permiso para intervenir.',
 'Separar, con un caso numérico, correlación y causalidad cuando hay una variable intermedia.'],
'''<h2>Ajuste lineal y la pregunta que el ajuste no responde</h2>
<p>La recta de regresión resume una nube por la recta que menos se separa de los puntos en vertical. Sirve para describir y, con cuidado, para predecir dentro del rango de las x. No dice qué pasaría si alguien forzara la x a cambiar: eso sería una causa, y la causa no sale de la misma cuenta.</p>
<p><span class="glosa">x̄, ȳ = medias · Sxx = suma de (x − x̄)² · Syy = suma de (y − ȳ)² · Sxy = suma de (x − x̄)(y − ȳ) · pendiente b = Sxy / Sxx · ordenada a = ȳ − b x̄ · r = Sxy / √(Sxx Syy)</span></p>
<p>En el ejemplo, x̄ = 3 y ȳ = 5. Las desviaciones de x son −2, −1, 0, 1, 2 y Sxx = 10. Las de y son −3, −1, 0, 1, 3 y Syy = 20. Los productos suman 14, así que b = 14/10 = 1,4 y a = 5 − 1,4·3 = 0,8. La recta dibujada es ŷ = 0,8 + 1,4x. Además r = 14/√200 ≈ 0,99: la asociación lineal es fortísima. Aun así, las horas y la nota pueden subir juntas porque quien ya domina la materia estudia más y también rinde más. El coeficiente no separa esas historias.</p>
<p>El contraste está en el segundo ejemplo: helados y ahogamientos suben a la vez en el esquema de junio frente a enero, y la variable que empuja a las dos es el calor, no el helado. Cerrar la heladería no vacía la piscina. Correlación describe; causalidad exige un mecanismo y, casi siempre, un diseño que no es esta nube.</p>
<table class="datos"><thead><tr><th>x horas</th><th>y nota</th><th>x − 3</th><th>y − 5</th><th>producto</th></tr></thead>
<tbody>
<tr><td>1</td><td>2</td><td>−2</td><td>−3</td><td>6</td></tr>
<tr><td>2</td><td>4</td><td>−1</td><td>−1</td><td>1</td></tr>
<tr><td>3</td><td>5</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>4</td><td>6</td><td>1</td><td>1</td><td>1</td></tr>
<tr><td>5</td><td>8</td><td>2</td><td>3</td><td>6</td></tr>
</tbody></table>''',
'Cinco puntos (1,2), (2,4), (3,5), (4,6), (5,8) y la recta 0,8 + 1,4x', fig30,
[
('La recta de las cinco horas',
 'Con los cinco puntos de la figura, obtén b y a, y escribe la recta. Comprueba Sxy = 14 y Sxx = 10.',
 [
  ('Medias: (1+2+3+4+5)/5 = 3 y (2+4+5+6+8)/5 = 25/5 = 5. Los productos de desviaciones son 6, 1, 0, 1 y 6.',
   'Glosa: 6 + 1 + 1 + 6 = 14. El producto del punto medio es 0 y no aporta.'),
  ('Sxx = (−2)² + (−1)² + 0 + 1² + 2² = 4 + 1 + 1 + 4 = 10. Pendiente b = 14/10 = 1,4.',
   'Glosa: la pendiente son puntos de nota asociados a una hora más, dentro de esta muestra.'),
  ('Ordenada: a = 5 − 1,4 · 3 = 5 − 4,2 = 0,8. La recta es ŷ = 0,8 + 1,4x, la de la figura.',
   'Glosa: a es el valor de la recta cuando x = 0, aunque x = 0 no esté en los datos.'),
  ('Correlación: r = 14/√(10·20) = 14/√200 ≈ 0,99. Casi 1, y ni así la cuenta demuestra que añadir una hora cause 1,4 puntos.',
   'Glosa: r mide alineación. La causa exigiría saber qué se ha mantenido constante al variar las horas.'),
 ]),
('Helados y ahogamientos, esquema',
 'Esquema de un municipio, no una estadística oficial: en enero, 4 ºC, 40 helados y 0 ahogamientos; en junio, 28 ºC, 800 helados y 6 ahogamientos. Hay asociación positiva. ¿Se evita el ahogamiento cerrando la heladería?',
 [
  ('Entre enero y junio suben a la vez la temperatura, los helados y los ahogamientos. El signo de la asociación helados–ahogamientos es positivo.',
   'Glosa: positivo significa que se mueven en el mismo sentido, no que uno produzca al otro.'),
  ('La variable que empuja a las dos series es el calor: más baños y, por separado, más helados. El helado está en medio del calendario, no en la cadena causal del ahogado.',
   'Glosa: una tercera variable correlacionada con las dos se llama factor de confusión.'),
  ('Cerrar la heladería bajaría la segunda cifra y dejaría intactos el calor y los baños. La predicción «menos helados, menos ahogamientos» copia la correlación y se salta el mecanismo.',
   'Glosa: intervenir sobre x solo cambia y si x es una causa de y, y aquí no lo es.'),
  ('La frase correcta separa las dos cosas: en el esquema, helados y ahogamientos están correlacionados; la causa plausible de los ahogamientos es la exposición al agua, no el postre.',
   'Glosa: correlación describe el esquema; la decisión de cerrar la heladería no se deduce de él.'),
 ]),
('Misma recta, sin palanca',
 'En los cinco alumnos, b = 1,4. Explica qué está permitido decir y qué no cuando alguien propone «obligar una hora más para ganar 1,4 puntos».',
 [
  ('Permitido: dentro de estos datos, a una hora más le acompañan, en la recta, 1,4 puntos más de nota. Es la pendiente del ajuste.',
   'Glosa: «acompañan» describe la nube. No dice qué ocurriría al empujar a un alumno concreto.'),
  ('No permitido: tratar 1,4 como el efecto de una hora impuesta. Quien estudia 5 horas puede ser quien ya iba mejor antes de abrir el libro.',
   'Glosa: la x observada no es una x asignada. Regresión sobre lo observado no es un experimento.'),
  ('El punto (4, 6) ni siquiera está en la recta: ŷ = 0,8 + 1,4·4 = 6,4, y la nota real es 6. La asociación no es una regla persona a persona.',
   'Glosa: el residuo 6 − 6,4 = −0,4 es la parte que la recta no captura. Se detalla en la lección siguiente.'),
  ('Aunque r ≈ 0,99, la frase causal sigue sin estar justificada. Una correlación casi perfecta puede ser espuria, como la del helado, o puede ser real: la cifra sola no distingue.',
   'Glosa: el tamaño de r no sustituye al diseño. Hace falta saber cómo se generó la x.'),
 ]),
],
[
(1, 'Tres puntos en línea',
 'Puntos (1, 2), (2, 4) y (3, 6). Halla la recta de mínimos cuadrados y di por qué, aun siendo perfecta, no demuestra una causa.',
 'El paso es calcular medias y cociente de sumas, no «ver» la pendiente sin cuentas. La media de x es 2 y la de y es 4. Las desviaciones de x son −1, 0, 1 y Sxx = 2. Las de y son −2, 0, 2 y los productos suman 2 + 0 + 2 = 4. Entonces b = 4/2 = 2 y a = 4 − 2·2 = 0, así que ŷ = 2x. Los tres puntos cumplen la recta y r = 1. Esa perfección solo dice que, en la muestra, y es exactamente el doble de x. No dice que manipular x vaya a fabricar y: podría ser que una tercera variable, el tiempo de clase por ejemplo, empuje a las dos. La recta describe estos tres pares; la causa necesitaría un argumento que la cuenta no trae.',
 'e30a'),
(2, 'Leer b sin pasarse',
 'En el ejemplo de las horas, ¿cuántos puntos de nota asocia la recta a pasar de 2 horas a 3? ¿Por qué esa respuesta no es «el efecto de estudiar la tercera hora»?',
 'El paso es multiplicar la pendiente por el incremento de x, no buscar el punto en la nube y restar notas reales. De x = 2 a x = 3, Δx = 1 y la recta sube b·1 = 1,4 puntos: de ŷ = 3,6 a ŷ = 5. Las notas reales de esos dos alumnos son 4 y 5, y su diferencia es 1, no 1,4: la pendiente es del ajuste, no de cada pareja de personas. Llamar a 1,4 «efecto» supondría que la hora extra es la única cosa que cambia. En los datos, quien estudió 3 horas puede diferir en atención, descanso o nivel previo. La recta no ha mantenido nada de eso fijo, así que 1,4 es asociación media en la muestra.',
 'e30b'),
(3, 'Elegir la frase',
 'De estas dos frases, di cuál describe correlación y cuál afirma una causa, usando el esquema del helado: «en junio hay más helados y más ahogamientos» y «los helados provocan los ahogamientos».',
 'El paso es mirar si la frase solo dice que las dos cifras se mueven juntas o si dice que intervenir en una cambiaría la otra. La primera frase es correlación: compara enero y junio y constata que helados y ahogamientos van en el mismo sentido. La segunda es causal y no se sostiene con el esquema, porque la variable que cambia entre los dos meses y empuja a las dos series es la temperatura y, con ella, el baño. Si los helados fueran la causa, quitarlos en junio debería bajar los ahogamientos aunque el calor y las piscinas siguieran igual, y el esquema no aporta esa prueba. Correlación y causa no se distinguen por lo convencida que suene la frase, sino por si hay mecanismo y diseño.',
 'e30c'),
],
[
('¿Cuánto valen b y a en los cinco puntos del gráfico?',
 'b = 1,4 y a = 0,8, luego ŷ = 0,8 + 1,4x. Por qué: Sxy = 14, Sxx = 10 y b es su cociente. La ordenada se obtiene de a = ȳ − b x̄ = 5 − 1,4·3 = 0,8. La recta de la figura es exactamente esa.'),
('¿Un r de aproximadamente 0,99 demuestra que estudiar causa la nota?',
 'No. Por qué: r = 14/√200 solo mide lo alineados que están los cinco puntos. Quien estudia más puede ser quien ya partía de un nivel más alto, y entonces las dos variables suben juntas sin que la hora sea la causa. Hace falta un diseño, no un coeficiente más bonito.'),
('En el esquema de enero y junio, ¿qué variable estorba la lectura causal?',
 'La temperatura. Por qué: pasa de 4 ºC a 28 ºC y empuja a la vez a los helados (de 40 a 800) y a los ahogamientos (de 0 a 6). La asociación helados–ahogamientos es real en el esquema y la intervención «cerrar la heladería» no toca esa causa. Correlación no es permiso para actuar sobre la variable que esté más a mano.'),
],
'Asociación no es palanca',
'En el lienzo marca los cinco puntos del ejemplo, traza a mano una recta creciente y escribe debajo una frase que diga asociación y otra que se niegue a decir causa.',
['Cinco puntos y la recta 0,8 + 1,4x entre x = 1 y x = 5.',
 'Sxy = 14 y Sxx = 10 fijan la pendiente 1,4. No es una recta puesta a ojo.',
 'Ejemplo 1: r ≈ 0,99 y, aun así, la causa no está demostrada.',
 'Ejemplo 2: helados y ahogamientos suben con el calor. Cerrar la heladería no es la intervención.',
 'Ejemplo 3: 1,4 puntos por hora es la pendiente del ajuste, no el efecto de obligar una hora.',
 'El laboratorio predice un x y avisa si te sales del intervalo 1 a 5.',
 'Una nube describe. No manda sobre lo que nadie ha manipulado.'],
lab_title='Recta, predicción y causa')

print('L30 escrito')

# ---------- L31 ----------
_line31 = path_fn(lambda x: 0.8 + 1.4 * x, 1, 5, 8, _X30, _Y30)
_pts31 = []
for _x, _y in ((1, 2), (2, 4), (3, 5), (4, 6), (5, 8)):
    _pts31.append(f'<circle cx="{_X30(_x):.0f}" cy="{_Y30(_y):.0f}" r="6" fill="#E6E1D6"/>')
# residual at x=2: observed 4, predicted 3.6
_rx, _ry, _yhat = _X30(2), _Y30(4), _Y30(3.6)
fig31 = f'''
<line x1="70" y1="280" x2="660" y2="280" stroke="#9A9488" stroke-width="1.6"/>
<line x1="80" y1="290" x2="80" y2="30" stroke="#9A9488" stroke-width="1.6"/>
{_line31}
<line x1="{_rx:.0f}" y1="{_yhat:.0f}" x2="{_rx:.0f}" y2="{_ry:.0f}" stroke="#8F9A72" stroke-width="3"/>
<circle cx="{_rx:.0f}" cy="{_ry:.0f}" r="6" fill="#8F9A72"/>
<circle cx="{_rx:.0f}" cy="{_yhat:.0f}" r="5" fill="none" stroke="#C4A15A" stroke-width="2"/>
{''.join(_pts31)}
<text x="210" y="{(_ry+_yhat)/2:.0f}" fill="#8F9A72" font-size="13">residuo +0,4</text>
<text x="100" y="24" fill="#C4A15A" font-size="14">mismos datos · segmento verde = nota real menos predicción en x = 2</text>
'''
build(
31, 'Coeficientes y <em>predicción</em>', 'E.1 r, R², residuo y fiabilidad de la predicción',
'Lo que la recta no acierta también se mide',
'Seguimos con las horas y las notas de la lección anterior: ŷ = 0,8 + 1,4x. En x = 2 la recta predice 3,6 y la nota real es 4, así que el residuo vertical es +0,4. R² vale 0,98. Predecir en x = 6 ya es salirse de los datos.',
['Calcular un residuo como valor observado menos predicción, con su signo.',
 'Interpretar R² como fracción de la suma de cuadrados, no como probabilidad de acertar.',
 'Distinguir una predicción dentro del rango de una extrapolación.'],
'''<h2>Residuo, R² y el borde de los datos</h2>
<p>La pendiente dice cuánto sube la recta. El residuo dice cuánto falla en un punto concreto: es vertical, porque la regresión minimiza errores en y, no distancias perpendiculares a la recta. R² dice qué parte de la variación de las notas queda recogida por esa recta. Ninguno de los tres convierte la predicción en un hecho cuando x se sale del intervalo observado.</p>
<p><span class="glosa">ŷ = a + bx · residuo e = y − ŷ · signo positivo = el punto queda por encima de la recta · SCres = suma de e² · SCtot = Syy · R² = 1 − SCres/SCtot = r² en el ajuste lineal simple</span></p>
<p>Con estos cinco puntos los residuos son −0,2, +0,4, 0, −0,4 y +0,2. Suman cero, como tiene que ocurrir en una recta con ordenada calculada a partir de las medias. Sus cuadrados suman 0,04 + 0,16 + 0 + 0,16 + 0,04 = 0,40. La suma de cuadrados de las notas respecto de su media es Syy = 20. Entonces R² = 1 − 0,40/20 = 0,98. También 196/200 = 0,98, porque R² = Sxy² / (Sxx Syy). El 2 % que falta es exactamente esos residuos: no es «un 2 % de probabilidad de equivocarse».</p>
<p>Dentro del intervalo, x = 3,5 da ŷ = 0,8 + 1,4·3,5 = 5,7, una interpolación. En x = 6, fuera de 1 a 5, la fórmula da 9,2, pero ningún alumno de la muestra estudió 6 horas y la nota no puede leerse como si el modelo siguiera igual de fiable. Extrapolación es usar la recta donde no la hemos visto funcionar.</p>''',
'Recta 0,8 + 1,4x, puntos del ejemplo y residuo vertical +0,4 en x = 2', fig31,
[
('El residuo de dos horas',
 'Para el alumno de 2 horas y nota 4, calcula la predicción y el residuo. Di qué significa el signo.',
 [
  ('Predicción: ŷ = 0,8 + 1,4 · 2 = 0,8 + 2,8 = 3,6. Es el punto de la recta, no la nota real.',
   'Glosa: 1,4 · 2 se calcula antes de sumar la ordenada 0,8.'),
  ('Residuo: e = 4 − 3,6 = +0,4. Primero el observado, después la predicción. El orden cambia el signo.',
   'Glosa: si se resta al revés sale −0,4 y se invierte quién está encima.'),
  ('El signo positivo significa que la nota real queda 0,4 puntos por encima de la recta. En la figura es el segmento verde.',
   'Glosa: el segmento es vertical, a x constante. No es la distancia perpendicular a la recta.'),
  ('No es un error de redondeo ni un fallo del alumno. Es la parte de la nota que estas cinco x no recogen con una recta.',
   'Glosa: residuo pequeño no significa causa. Solo significa que el punto está cerca de la recta.'),
 ]),
('De los residuos a R²',
 'Comprueba que los cinco residuos cuadrados suman 0,40 y que R² = 0,98. Explica qué no significa ese 0,98.',
 [
  ('Residuos: en x = 1, 2 − 2,2 = −0,2; en x = 2, +0,4; en x = 3, 5 − 5 = 0; en x = 4, 6 − 6,4 = −0,4; en x = 5, 8 − 7,8 = +0,2.',
   'Glosa: 0,8 + 1,4·4 = 6,4 y 0,8 + 1,4·5 = 7,8. Conviene escribir ŷ antes de restar.'),
  ('Cuadrados: 0,04 + 0,16 + 0 + 0,16 + 0,04 = 0,40. Syy = 20. R² = 1 − 0,40/20 = 0,98.',
   'Glosa: se dividen sumas de cuadrados, no los residuos crudos. El signo desaparece al cuadrar.'),
  ('Atajo: Sxy² / (Sxx Syy) = 196 / 200 = 0,98. Las dos cuentas tienen que coincidir en la recta simple.',
   'Glosa: 14² = 196, Sxx = 10 y Syy = 20. Si no coincidiera, habría un residuo mal restado.'),
  ('0,98 no es la probabilidad de que la próxima nota sea la predicha. Es la fracción de la variación de y que la recta acompaña. Queda un 2 % en los residuos.',
   'Glosa: una predicción concreta sigue teniendo residuo. R² no lo anula en cada persona.'),
 ]),
('Dentro y fuera del intervalo',
 'Predice la nota para 3,5 horas y para 6 horas. Di cuál de las dos es una extrapolación y por qué es menos de fiar.',
 [
  ('x = 3,5 está entre 1 y 5. ŷ = 0,8 + 1,4 · 3,5 = 0,8 + 4,9 = 5,7. Es interpolación.',
   'Glosa: 1,4 · 3,5 = 1,4 · 3 + 1,4 · 0,5 = 4,2 + 0,7 = 4,9.'),
  ('x = 6 está fuera. La misma fórmula da 0,8 + 1,4 · 6 = 0,8 + 8,4 = 9,2. La aritmética funciona; la garantía, no.',
   'Glosa: no hay ningún punto de la muestra a la derecha de x = 5. La recta allí es una hipótesis.'),
  ('La fiabilidad se apoya en haber visto la nube en esa zona. En 3,5 hay puntos a los dos lados. En 6 no hay ninguno.',
   'Glosa: R² = 0,98 describe el ajuste donde están los datos, no un permiso para alargar la recta.'),
  ('Además la nota del centro, si el máximo es 10, aún cabría 9,2, pero ese techo no lo ha informado la muestra. Extrapolación suma riesgo de forma y riesgo de contexto.',
   'Glosa: salirse del rango de x es el criterio. No hace falta que la predicción sea absurda para desconfiar.'),
 ]),
],
[
(1, 'Residuo en cinco horas',
 'El alumno de 5 horas sacó un 8. Calcula ŷ y el residuo, y explica el signo con una frase.',
 'El paso es evaluar la recta en ese x y restar después, en el orden observado menos predicción. ŷ = 0,8 + 1,4·5 = 7,8. El residuo es 8 − 7,8 = +0,2. El signo positivo dice que la nota quedó dos décimas por encima de la recta, no que la recta «se haya pasado». Si alguien calcula 7,8 − 8 = −0,2 y lo llama residuo del mismo convenio, ha cambiado el criterio y ya no podrá sumar los residuos de la muestra y obtener cero. El segmento es vertical: se compara la nota con la altura de la recta en la misma hora, no con el punto de otro alumno.',
 'e31a'),
(2, 'Qué no es R²',
 'Un compañero dice: «R² = 0,98, así que hay un 98 % de probabilidad de acertar la nota». Corrige la frase usando SCres = 0,40 y SCtot = 20.',
 'El paso es recordar que R² es un cociente de sumas de cuadrados, no una probabilidad sobre la próxima persona. 0,40/20 = 0,02 y 1 − 0,02 = 0,98: el 98 % de la suma de cuadrados de las notas, respecto de su media, queda recogido por la recta, y el 2 % restante es la suma de los residuos al cuadrado. Ningún alumno tiene probabilidad 0,98 de obtener exactamente ŷ, porque el residuo de varios de ellos no es cero: en x = 2 vale +0,4. La frase del compañero convierte una medida de ajuste global en una garantía individual. Se corrige diciendo «la recta acompaña el 98 % de la variación cuadrática de estas cinco notas».',
 'e31b'),
(3, 'Una x nueva',
 '¿La predicción en x = 4,5 es más defendible que la predicción en x = 0? Calcula las dos y justifica la diferencia.',
 'El paso es situar cada x respecto del intervalo observado, que va de 1 a 5, antes de fiarse del número. En x = 4,5, ŷ = 0,8 + 1,4·4,5 = 0,8 + 6,3 = 7,1, y 4,5 cae entre dos horas que sí están en la muestra: es interpolación. En x = 0, ŷ = 0,8, pero nadie de los cinco tiene 0 horas y la ordenada es solo el cruce de la recta con el eje, no una nota vista. Las dos cuentas usan la misma fórmula y no tienen la misma fiabilidad. R² alto no arregla la segunda: el coeficiente resume el tramo donde había puntos. Predecir en el borde interior es razonable; predecir en cero es extrapolación.',
 'e31c'),
],
[
('¿Cuánto vale el residuo del punto (2, 4) y por qué es positivo?',
 'Vale +0,4 porque 4 − 3,6 = 0,4. Por qué: la recta en x = 2 da 0,8 + 2,8 = 3,6 y el residuo resta esa predicción de la nota real. Positivo significa que el punto queda por encima de la recta, que es el segmento verde de la figura.'),
('¿Qué cuenta produce R² = 0,98?',
 '1 − 0,40/20, o bien 196/200. Por qué: los residuos cuadrados suman 0,40 y la variación de las notas suma 20. No es una probabilidad de acierto. El 0,02 que falta está en los residuos, no en una moneda que se lanza a cada predicción.'),
('¿Por qué ŷ = 9,2 en x = 6 es menos de fiar que ŷ = 5,7 en x = 3,5?',
 'Porque 6 está fuera del intervalo de horas de la muestra y 3,5 está dentro. Por qué: la recta se estimó con x desde 1 hasta 5. Interpolación se apoya en puntos vecinos; extrapolación supone que la misma pendiente sigue valiendo donde no hemos visto a nadie. R² = 0,98 no se traslada solo al tramo nuevo.'),
],
'El segmento que falta',
'Dibuja en el lienzo la recta y el punto (2, 4), marca el residuo vertical y escribe si tu x elegida para una predicción nueva cae dentro o fuera de 1 a 5.',
['La recta es la de siempre: 0,8 + 1,4x. El segmento verde mide +0,4 en x = 2.',
 'Ese residuo es nota real menos predicción, no al revés.',
 'Ejemplo 1: 3,6 de predicción y residuo positivo porque 4 está por encima.',
 'Ejemplo 2: los cuadrados suman 0,40 y R² = 1 − 0,40/20 = 0,98.',
 'Ejemplo 3: 5,7 es interpolación; 9,2 en x = 6 es extrapolación.',
 'R² alto no es la probabilidad de acertar la nota de una persona.',
 'Fuera del rango de x, la fórmula sigue y la garantía no.'],
)

print('L31 escrito')

# ---------- L32 ----------
fig32 = '''
<circle cx="70" cy="160" r="16" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<line x1="86" y1="150" x2="210" y2="70" stroke="#C4A15A" stroke-width="2"/>
<line x1="86" y1="170" x2="210" y2="250" stroke="#C4A15A" stroke-width="2"/>
<circle cx="226" cy="64" r="16" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<circle cx="226" cy="256" r="16" fill="#1C1A16" stroke="#8F9A72" stroke-width="2"/>
<line x1="242" y1="56" x2="390" y2="28" stroke="#C4A15A" stroke-width="2"/>
<line x1="242" y1="74" x2="390" y2="110" stroke="#8F9A72" stroke-width="2"/>
<line x1="242" y1="248" x2="390" y2="200" stroke="#C4A15A" stroke-width="2"/>
<line x1="242" y1="266" x2="390" y2="292" stroke="#8F9A72" stroke-width="2"/>
<circle cx="408" cy="28" r="8" fill="#C4A15A"/>
<circle cx="408" cy="112" r="8" fill="#8F9A72"/>
<circle cx="408" cy="198" r="8" fill="#C4A15A"/>
<circle cx="408" cy="292" r="8" fill="#8F9A72"/>
<text x="70" y="164" text-anchor="middle" fill="#E6E1D6" font-size="12">8</text>
<text x="226" y="68" text-anchor="middle" fill="#E6E1D6" font-size="12">R</text>
<text x="226" y="260" text-anchor="middle" fill="#E6E1D6" font-size="12">A</text>
<text x="130" y="100" fill="#C4A15A" font-size="13">5/8</text>
<text x="130" y="230" fill="#8F9A72" font-size="13">3/8</text>
<text x="300" y="36" fill="#C4A15A" font-size="13">4/7</text>
<text x="300" y="100" fill="#8F9A72" font-size="13">3/7</text>
<text x="300" y="230" fill="#C4A15A" font-size="13">5/7</text>
<text x="300" y="286" fill="#8F9A72" font-size="13">2/7</text>
<text x="430" y="32" fill="#E6E1D6" font-size="14">RR = 20/56</text>
<text x="430" y="116" fill="#E6E1D6" font-size="14">RA = 15/56</text>
<text x="430" y="202" fill="#E6E1D6" font-size="14">AR = 15/56</text>
<text x="430" y="296" fill="#E6E1D6" font-size="14">AA = 6/56</text>
<text x="40" y="24" fill="#C4A15A" font-size="14">sin reemplazo · 5 rojas y 3 azules</text>
'''
build(
32, 'Compuesta y <em>condicionada</em>', 'E.2 Compuestos, condicionada, independencia y árbol',
'La segunda bola no ve la misma urna',
'Urna con 5 bolas rojas y 3 azules, ocho en total. Se extraen dos sin devolver la primera. El árbol de la figura cambia el denominador en la segunda rama: de 8 pasa a 7, y el color que ya salió cambia el numerador.',
['Multiplicar a lo largo de una rama usando la probabilidad condicionada de la segunda extracción.',
 'Sumar ramas cuando el suceso es una unión de caminos distintos.',
 'Reconocer independencia solo cuando la condicionada coincide con la marginal, como al reemplazar.'],
'''<h2>El árbol guarda el orden y el denominador</h2>
<p>Una probabilidad compuesta es la de un camino entero: primera extracción y segunda. En el árbol se multiplica la probabilidad de la rama de salida por la de la rama que sale de ella. Sin reemplazo, la segunda no se copia de la primera: queda una bola menos, y del color que ya salió queda una menos todavía.</p>
<p><span class="glosa">P(R) = 5/8 · P(A) = 3/8 · sin reemplazo, tras roja: 4 rojas y 3 azules entre 7 · P(RR) = (5/8)·(4/7) = 20/56 · ramas que se suman = caminos distintos del mismo suceso · independencia = la condicionada no cambia al saber la primera</span></p>
<p>Las cuatro hojas suman 20/56 + 15/56 + 15/56 + 6/56 = 56/56 = 1. Esa comprobación delata una rama mal contada. Colores distintos son dos caminos, RA y AR, no uno: 15/56 + 15/56 = 30/56 = 15/28. Dos rojas son un solo camino, 20/56 = 5/14.</p>
<p>Con reemplazo la urna no cambia y P(segunda roja | primera roja) sigue siendo 5/8, igual que la marginal: ahí sí hay independencia. Sin reemplazo, 4/7 no es 5/8. El laboratorio pone las dos situaciones una al lado de la otra para que el denominador no se copie por costumbre.</p>''',
'Árbol sin reemplazo: ramas 5/8 y 3/8, segundas 4/7, 3/7, 5/7 y 2/7', fig32,
[
('Dos colores distintos',
 'Con el árbol de la figura, calcula la probabilidad de sacar una roja y una azul, en cualquier orden.',
 [
  ('Camino roja luego azul: (5/8)·(3/7) = 15/56. Tras la roja quedan 3 azules de 7 bolas.',
   'Glosa: el 3 del numerador son las azules, que no han cambiado; el denominador sí, de 8 a 7.'),
  ('Camino azul luego roja: (3/8)·(5/7) = 15/56. Ahora se han quitado una azul y quedan las 5 rojas entre 7.',
   'Glosa: el orden cambia qué condicionada se usa, aunque el producto numérico coincida.'),
  ('El suceso «una de cada» es la unión de esos dos caminos, que no se solapan. Se suman: 15/56 + 15/56 = 30/56 = 15/28.',
   'Glosa: multiplicar solo un camino olvidaría la mitad de las formas de conseguir colores distintos.'),
  ('Comprobación: los cuatro caminos suman 56/56. Los que no son mixtos son 20/56 + 6/56 = 26/56, y 1 − 26/56 = 30/56.',
   'Glosa: restar del total es lícito porque las cuatro hojas forman todo el espacio.'),
 ]),
('Con devolución el denominador no baja',
 'Se devuelve la primera bola. Calcula P(dos rojas) y compara P(segunda roja | primera roja) con 5/8.',
 [
  ('Con reemplazo, la segunda roja sigue teniendo probabilidad 5/8 aunque la primera haya sido roja. Hay independencia.',
   'Glosa: devolver restaura las 5 rojas y las 3 azules. El 7 no aparece.'),
  ('P(RR) = (5/8)·(5/8) = 25/64. Ya no es 20/56. El numerador de la segunda rama no baja de 5 a 4.',
   'Glosa: 25/64 ≈ 0,391 y 20/56 ≈ 0,357. Sacar dos rojas es un poco más fácil si se devuelve la primera.'),
  ('La condicionada coincide con la marginal: 5/8 = 5/8. Esa igualdad es la definición de independencia en este experimento.',
   'Glosa: sin reemplazo la misma comparación era 4/7 frente a 5/8, y no se cumplía.'),
  ('No basta con que las extracciones «se parezcan». Hay que mirar si la información de la primera cambia el número de la segunda.',
   'Glosa: el árbol con reemplazo repite las fracciones; el de la figura no las repite.'),
 ]),
('La segunda roja, sin saber la primera',
 'Sin reemplazo, calcula la probabilidad de que la segunda bola sea roja, sumando los dos caminos que acaban en roja.',
 [
  ('Caminan a segunda roja: RR, que vale 20/56, y AR, que vale 15/56.',
   'Glosa: RA acaba en azul y AA acaba en azul. No entran en este suceso.'),
  ('Suma: 20/56 + 15/56 = 35/56 = 5/8. La segunda bola, a ciegas, tiene la misma probabilidad de ser roja que la primera.',
   'Glosa: 35/56 = 5/8 porque 35 ÷ 7 = 5 y 56 ÷ 7 = 8.'),
  ('No contradice la dependencia. 4/7 es la probabilidad si ya se vio una roja. 5/8 es la probabilidad si no se vio nada.',
   'Glosa: marginal de la segunda y condicionada de la segunda son preguntas distintas.'),
  ('Por simetría, cualquiera de las ocho bolas es igual de probable en la segunda posición si no hay información. Por eso reaparece 5/8.',
   'Glosa: el árbol no «olvida» el sin reemplazo; al sumar los dos caminos, la información se cancela.'),
 ]),
],
[
(1, 'Dos azules',
 'Sin reemplazo, calcula P(dos azules) y explica por qué la segunda fracción es 2/7 y no 3/8.',
 'El paso es actualizar la urna después de la primera azul, no copiar 3/8 en la segunda rama. La primera azul sale con probabilidad 3/8. Quedan entonces 2 azules y 5 rojas, siete bolas, así que la segunda azul tiene probabilidad 2/7. El producto es (3/8)·(2/7) = 6/56 = 3/28, que es la hoja AA de la figura. Usar otra vez 3/8 sería devolver la bola sin decirlo y daría (3/8)·(3/8) = 9/64, un experimento distinto. El 2 del numerador es «una azul menos» y el 7 es «una bola menos»: las dos rebajas van juntas.',
 'e32a'),
(2, '¿Dónde está la independencia?',
 'Explica con las fracciones 4/7 y 5/8 si las dos extracciones sin reemplazo son independientes, y qué habría que cambiar en la urna para que lo fueran.',
 'El paso es comparar la condicionada con la marginal del mismo color, no juzgar por el aspecto del árbol. Sin reemplazo, P(segunda roja | primera roja) = 4/7, y la marginal de roja en la primera es 5/8. Como 4/7 ≠ 5/8, saber que la primera fue roja cambia la probabilidad de la segunda, y no hay independencia. Para que la hubiera, la segunda fracción tendría que seguir siendo 5/8, y eso ocurre si la bola se devuelve: la urna queda otra vez en 5 rojas y 3 azules. Independencia aquí no es una opinión sobre si los colores «tienen que ver»; es esa igualdad numérica.',
 'e32b'),
(3, 'Un solo camino no basta',
 'Alguien calcula «roja y azul» solo como 15/56. ¿Qué suceso ha calculado en realidad y cuál es el que pedía cualquier orden?',
 'El paso es listar los caminos del suceso antes de multiplicar una sola rama. 15/56 es únicamente roja seguida de azul, la hoja RA. El suceso «una de cada color», sin fijar el orden, incluye también azul seguida de roja, otros 15/56. La unión suma 30/56 porque los dos caminos no pueden ocurrir a la vez. Quedarse en 15/56 responde a una pregunta más estrecha, con el orden escrito. En cuanto el enunciado dice «en cualquier orden» o «una de cada», hay que recorrer las dos ramas del árbol y sumarlas. La comprobación con el complementario, 1 − 20/56 − 6/56 = 30/56, evita olvidar AR.',
 'e32c'),
],
[
('¿Cuánto suma la probabilidad de una roja y una azul, en cualquier orden?',
 '30/56, es decir 15/28. Por qué: son dos caminos, (5/8)·(3/7) = 15/56 y (3/8)·(5/7) = 15/56, y se suman porque el orden no está fijado. Un solo camino dejaría fuera la mitad del suceso.'),
('¿Por qué sin reemplazo no hay independencia?',
 'Porque 4/7 no es igual a 5/8. Por qué: si la primera fue roja, quedan 4 rojas de 7, no 5 de 8. La información de la primera extracción cambia la segunda. Con devolución las dos fracciones serían 5/8 y ahí sí serían independientes.'),
('Si no se mira la primera bola, ¿qué probabilidad tiene la segunda de ser roja?',
 '5/8, la misma que la primera. Por qué: se suman RR y AR, 20/56 + 15/56 = 35/56 = 5/8. No es la condicionada 4/7, porque esa exige haber visto una roja. Sin información, cualquiera de las ocho bolas puede ocupar el segundo lugar.'),
],
'Numera las ramas',
'En el lienzo dibuja el árbol de la urna, escribe 5/8, 3/8 y las cuatro segundas fracciones con denominador 7, y rodea las dos hojas que se suman para colores distintos.',
['Cuatro hojas: 20/56, 15/56, 15/56 y 6/56. Su suma es 1.',
 'Tras una roja el denominador es 7 y las rojas que quedan son 4.',
 'Ejemplo 1: colores distintos suman 30/56, los dos caminos.',
 'Ejemplo 2: con reemplazo, P(RR) = 25/64 y la condicionada no cambia.',
 'Ejemplo 3: la segunda roja, a ciegas, vuelve a valer 5/8.',
 'El laboratorio contrasta el 4/7 del sin reemplazo con el 5/8 del con reemplazo.',
 'Multiplicar una rama y sumar las ramas del mismo suceso.'],
lab_title='Árbol con y sin reemplazo')

print('L32 escrito')

# ---------- L33 ----------
fig33 = '''
<circle cx="60" cy="160" r="14" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<line x1="74" y1="150" x2="180" y2="70" stroke="#C4A15A" stroke-width="2.2"/>
<line x1="74" y1="170" x2="180" y2="250" stroke="#9A9488" stroke-width="2.2"/>
<circle cx="196" cy="64" r="14" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<circle cx="196" cy="256" r="14" fill="#1C1A16" stroke="#9A9488" stroke-width="2"/>
<line x1="210" y1="56" x2="340" y2="30" stroke="#C4A15A" stroke-width="2"/>
<line x1="210" y1="74" x2="340" y2="110" stroke="#8F9A72" stroke-width="2"/>
<line x1="210" y1="246" x2="340" y2="210" stroke="#C4A15A" stroke-width="2"/>
<line x1="210" y1="266" x2="340" y2="300" stroke="#8F9A72" stroke-width="2"/>
<circle cx="356" cy="28" r="7" fill="#C4A15A"/>
<circle cx="356" cy="112" r="7" fill="#8F9A72"/>
<circle cx="356" cy="208" r="7" fill="#C4A15A"/>
<circle cx="356" cy="300" r="7" fill="#8F9A72"/>
<text x="100" y="100" fill="#C4A15A" font-size="13">100 con déficit</text>
<text x="100" y="230" fill="#9A9488" font-size="13">900 sin déficit</text>
<text x="250" y="40" fill="#C4A15A" font-size="12">90 %</text>
<text x="250" y="100" fill="#8F9A72" font-size="12">10 %</text>
<text x="250" y="230" fill="#C4A15A" font-size="12">20 %</text>
<text x="250" y="292" fill="#8F9A72" font-size="12">80 %</text>
<text x="376" y="32" fill="#E6E1D6" font-size="14">VP 90</text>
<text x="376" y="116" fill="#E6E1D6" font-size="14">FN 10</text>
<text x="376" y="212" fill="#E6E1D6" font-size="14">FP 180</text>
<text x="376" y="304" fill="#E6E1D6" font-size="14">VN 720</text>
<text x="500" y="120" fill="#C4A15A" font-size="15">positivos</text>
<text x="500" y="144" fill="#E6E1D6" font-size="15">90 + 180 = 270</text>
<line x1="470" y1="28" x2="490" y2="120" stroke="#C4A15A" stroke-width="1.6"/>
<line x1="470" y1="208" x2="490" y2="140" stroke="#C4A15A" stroke-width="1.6"/>
<text x="500" y="180" fill="#C4A15A" font-size="16">90 / 270 = 1/3</text>
'''
build(
33, 'Probabilidad total y <em>Bayes</em>', 'E.2 Teorema de la probabilidad total y teorema de Bayes',
'El positivo no es la sensibilidad',
'Sobre 1000 alumnos, un déficit vitamínico afecta a 100. La prueba detecta al 90 % de quienes lo tienen y da positivo falso al 20 % de quienes no. Los positivos no son 90: son 90 verdaderos más 180 falsos. Bayes es la fracción 90/270.',
['Reconstruir verdaderos positivos y falsos positivos a partir de la prevalencia y de las tasas de la prueba.',
 'Calcular la probabilidad total de dar positivo sumando los dos caminos.',
 'Aplicar Bayes como el peso del camino buscado dentro de todos los positivos, y ver cómo cambia si cambia la prevalencia.'],
'''<h2>Primero las cuatro casillas, después el cociente</h2>
<p>La probabilidad total descompone un suceso según una partición. Aquí la partición es «tiene el déficit» o «no lo tiene». Dar positivo puede ocurrir por los dos lados, y Bayes pregunta, ya visto el positivo, qué parte de esos positivos venía del lado del déficit. La sensibilidad no contesta esa pregunta: la sensibilidad solo mira a quienes sí tienen el déficit.</p>
<p><span class="glosa">prevalencia = 100/1000 = 0,10 · sensibilidad = verdaderos positivos / enfermos = 90/100 · especificidad = verdaderos negativos / sanos = 720/900 · P(positivo) = 90/1000 + 180/1000 = 0,27 · P(déficit | positivo) = 90/270</span></p>
<p>Con mil personas las cuentas se ven sin decimales escondidos. Enfermos: 100. La prueba acierta en el 90 %, luego 90 verdaderos positivos y 10 falsos negativos. Sanos: 900. Especificidad del 80 %, luego 720 verdaderos negativos y 180 falsos positivos. Positivos totales: 90 + 180 = 270. De ellos, solo 90 tienen el déficit: 90/270 = 1/3. Quien oiga «la prueba acierta el 90 %» y crea que un positivo significa un 90 % de déficit está leyendo la rama equivocada del árbol.</p>
<p>La fórmula compacta dice lo mismo: P(D|+) = (0,90·0,10) / 0,27 = 0,09/0,27 = 1/3. El numerador 0,09 es el camino de los verdaderos positivos sobre las mil personas; el denominador es la probabilidad total de positivo. El segundo ejemplo cambia de contexto, a dos líneas de producción, y el tercero cambia solo la prevalencia para ver que el mismo test no arrastra el mismo posterior.</p>''',
'Árbol de 1000 alumnos: 90 verdaderos positivos, 180 falsos positivos y cociente 90/270', fig33,
[
('Del árbol al tercio',
 'Con 1000 alumnos, prevalencia 10 %, sensibilidad 90 % y especificidad 80 %, calcula cuántos positivos hay y qué fracción de ellos tiene el déficit.',
 [
  ('Partición: 0,10 · 1000 = 100 con déficit y 900 sin él. Esta fila se escribe antes de tocar la prueba.',
   'Glosa: la prevalencia manda el tamaño de cada rama. Sin ella no hay falsos positivos que contar.'),
  ('En los 100, el 90 % da positivo: 90 verdaderos positivos y 10 falsos negativos. En los 900, el 20 % da positivo falso: 180. Los otros 720 son negativos verdaderos.',
   'Glosa: 0,20 · 900 = 180. La especificidad es el 80 % complementario, no un adorno.'),
  ('Probabilidad total de positivo, en personas: 90 + 180 = 270, es decir 270/1000 = 0,27. Son dos caminos, no uno.',
   'Glosa: olvidar los 180 deja el denominador en 90 y la probabilidad condicionada en 1, absurda.'),
  ('Bayes: 90/270 = 1/3 ≈ 0,333. Un positivo, en este grupo, deja el déficit en un tercio, no en el 90 % de la sensibilidad.',
   'Glosa: 90/270 = 1/3 exactamente. No hace falta redondear a 0,33 para verlo.'),
 ]),
('La pieza defectuosa y la línea',
 'La línea A fabrica el 60 % de las piezas y el 2 % de las suyas salen defectuosas. La línea B fabrica el 40 % y el 5 % de las suyas salen defectuosas. Una pieza es defectuosa: ¿qué probabilidad hay de que venga de B?',
 [
  ('Caminos hacia el defecto, en tanto por uno: A aporta 0,60 · 0,02 = 0,012. B aporta 0,40 · 0,05 = 0,020.',
   'Glosa: cada producto es producción por tasa. La tasa sola, 0,05, no es la probabilidad de venir de B.'),
  ('Probabilidad total de defecto: 0,012 + 0,020 = 0,032. El defecto es más frecuente por la rama B aunque A fabrique más piezas.',
   'Glosa: 0,020 es mayor que 0,012 porque la tasa de B compensa, y sobrepasa, su menor producción.'),
  ('Bayes hacia B: 0,020 / 0,032 = 20/32 = 5/8 = 0,625. Hacia A queda 0,012/0,032 = 3/8 = 0,375.',
   'Glosa: las dos posteriores suman 1. Si no sumaran, se habría perdido un camino.'),
  ('No vale quedarse en «B tiene más porcentaje de fallos, luego es B». Sin el 40 % de producción, el peso 0,020 no existiría. Las dos cifras de cada línea entran en el producto.',
   'Glosa: 0,05 / (0,05 + 0,02) = 5/7 ≈ 0,71 olvidaría cuánto fabrica cada línea y no es Bayes.'),
 ]),
('La misma prueba, otra prevalencia',
 'El mismo test (sensibilidad 90 %, falsos positivos 20 %) se usa en un grupo donde la mitad tiene el déficit, 500 de 1000. Recalcula P(déficit | positivo).',
 [
  ('Nuevas casillas de enfermos: 500. Verdaderos positivos: 0,90 · 500 = 450. Falsos negativos: 50.',
   'Glosa: se rehace la partición. No se reutiliza el 100 del ejemplo primero.'),
  ('Sanos: 500. Falsos positivos: 0,20 · 500 = 100. Verdaderos negativos: 400.',
   'Glosa: al haber menos sanos, los falsos positivos bajan de 180 a 100 aunque la tasa sea la misma.'),
  ('Positivos: 450 + 100 = 550. Bayes: 450/550 = 45/55 = 9/11 ≈ 0,818.',
   'Glosa: 450 ÷ 50 = 9 y 550 ÷ 50 = 11. El posterior ahora sí es alto, porque el déficit ya era frecuente.'),
  ('La sensibilidad no se ha movido del 90 % y el posterior ha pasado de 1/3 a 9/11. Bayes depende de la prevalencia. Memorizar el resultado del primer grupo y pegarlo en el segundo es el error.',
   'Glosa: un test no trae su posterior puesto. Lo fabrica junto con la frecuencia de partida.'),
 ]),
],
[
(1, 'Sube la especificidad',
 'En el grupo de 1000 con 100 afectados, la sensibilidad sigue en el 90 % pero la especificidad pasa al 90 % (solo un 10 % de falsos positivos). Recalcula P(déficit | positivo).',
 'El paso es volver a contar los falsos positivos desde los 900 sanos, no retocar el 180 a ojo. Con especificidad del 90 %, el falso positivo es el 10 % de 900, o sea 90. Los verdaderos positivos no cambian: siguen siendo 90. Los positivos totales pasan a 90 + 90 = 180. Bayes da 90/180 = 1/2. Antes, con 180 falsos, el posterior era 1/3; al reducir los falsos a la mitad, el positivo pesa más y el posterior sube a un medio. No sube hasta el 90 %, porque todavía hay tantos falsos positivos como verdaderos. La sensibilidad sola seguiría engañando.',
 'e33a'),
(2, 'No olvides la producción',
 'En las líneas A y B del ejemplo, alguien dice que una defectuosa viene de B con probabilidad 0,05 / (0,05 + 0,02). Explica qué dato ha tirado y cuál es el posterior correcto.',
 'El paso que falta es multiplicar cada tasa por la fracción de producción antes de comparar. 0,05 y 0,02 son probabilidades condicionadas a la línea, no pesos de las líneas. A fabrica el 60 % y B el 40 %, así que los caminos son 0,60·0,02 = 0,012 y 0,40·0,05 = 0,020. El posterior de B es 0,020/0,032 = 5/8 = 0,625, no 0,05/0,07 ≈ 0,714. La cuenta sin producción trataría a las dos líneas como si fabricaran lo mismo, y no es el caso. Bayes de una causa entre dos exige el producto de la previa por la verosimilitud, las dos cosas, y luego normalizar por la suma.',
 'e33b'),
(3, 'Negativo no es imposible',
 'En el primer cribado, ¿qué probabilidad hay de tener el déficit habiendo dado negativo? Usa los 10 y los 720.',
 'El paso es aplicar la misma lógica de Bayes al suceso «negativo», no concluir cero porque la prueba haya dicho que no. Los negativos son los 10 falsos negativos más los 720 verdaderos negativos: 730. De ellos, 10 sí tienen el déficit. El posterior es 10/730 = 1/73 ≈ 0,0137. Es pequeño, mucho menor que el tercio de un positivo, y no es cero: la sensibilidad del 90 % deja escapar a 10 personas de las 100. Decir «si sale negativo, seguro que no lo tiene» convierte un 10 % de fallos entre los enfermos en una imposibilidad. La probabilidad total de negativo es 730/1000 = 0,73, y Bayes se queda con la parte 10/730.',
 'e33c'),
],
[
('¿Por qué un positivo no significa un 90 % de déficit en el primer cribado?',
 'Porque el 90 % es la sensibilidad, calculada solo entre los 100 que sí tienen el déficit. Por qué: entre los positivos hay 90 verdaderos y 180 falsos, 270 en total, y 90/270 = 1/3. La mayoría de los positivos, en este grupo poco afectado, son falsos. El árbol lo separa antes de dividir.'),
('En las dos líneas, ¿por qué el posterior de B es 5/8 y no «la tasa más alta»?',
 'Porque hay que ponderar el 5 % por el 40 % de producción. Por qué: el camino de B es 0,020 y el total de defecto es 0,032, y 0,020/0,032 = 5/8. La tasa 0,05 sin el peso de la línea no es una probabilidad sobre las piezas defectuosas.'),
('¿Qué le pasa al posterior del déficit si la prevalencia pasa del 10 % al 50 %, con el mismo test?',
 'Sube de 1/3 a 9/11, unos 0,818. Por qué: ahora hay 450 verdaderos positivos y solo 100 falsos, 450/550 = 9/11. La sensibilidad sigue en el 90 %. Cambia el posterior porque cambia cuánta gente parte con el déficit, no porque la prueba se haya vuelto otra.'),
],
'Las cuatro casillas primero',
'En el lienzo dibuja el árbol con 100 y 900, escribe 90 y 180 en las hojas positivas y la división 90/270 al lado. No pongas 0,90 como respuesta final.',
['El árbol parte 1000 en 100 y 900. Las hojas positivas son 90 y 180.',
 '270 es la suma de los dos caminos, la probabilidad total en personas.',
 'Ejemplo 1: Bayes da 90/270 = 1/3, no la sensibilidad 0,90.',
 'Ejemplo 2: las líneas dan caminos 0,012 y 0,020, y B queda en 5/8.',
 'Ejemplo 3: con prevalencia 50 % el mismo test da 450/550 = 9/11.',
 'El laboratorio rehace las cuatro casillas si cambias los porcentajes.',
 'Sin prevalencia no hay posterior. La prueba sola no lo trae.'],
lab_title='Bayes con mil personas')

print('L33 escrito')

# ---------- L34 ----------
_b34 = []
_b34.append('<line x1="40" y1="250" x2="430" y2="250" stroke="#9A9488" stroke-width="1.6"/>')
_b34.append('<line x1="50" y1="250" x2="50" y2="40" stroke="#9A9488" stroke-width="1.6"/>')
_probs = [1, 4, 6, 4, 1]
for _k, _p in enumerate(_probs):
    _h = _p * 24
    _x = 70 + _k * 70
    _col = '#E6E1D6' if _k == 3 else '#C4A15A'
    _b34.append(barra(_x, 250 - _h, 46, _h, _col))
    _b34.append(f'<text x="{_x+23}" y="268" text-anchor="middle" fill="#E6E1D6" font-size="13">{_k}</text>')
    _b34.append(f'<text x="{_x+23}" y="{242-_h}" text-anchor="middle" fill="#C4A15A" font-size="12">{_p}/16</text>')
_b34.append('<circle cx="303" cy="70" r="14" fill="none" stroke="#E6E1D6" stroke-width="2"/>')
_gpts = []
for _i in range(33):
    _z = -3 + 6 * _i / 32
    _px = 610 + _z * 28
    _py = 200 - math.exp(-0.5 * _z * _z) * 110
    _gpts.append(f'{_px:.1f},{_py:.1f}')
_gpath = '<path d="M ' + ' L '.join(_gpts) + '" fill="none" stroke="#C4A15A" stroke-width="2.2"/>'
fig34 = '\n'.join(_b34) + f'''
<text x="40" y="24" fill="#C4A15A" font-size="14">binomial n=4, p=1/2 · barra clara: ejemplo P(X=3)=4/16</text>
<line x1="470" y1="200" x2="700" y2="200" stroke="#9A9488" stroke-width="1.4"/>
{_gpath}
<line x1="582" y1="200" x2="582" y2="133" stroke="#8F9A72" stroke-width="2"/>
<line x1="638" y1="200" x2="638" y2="133" stroke="#8F9A72" stroke-width="2"/>
<text x="560" y="220" fill="#8F9A72" font-size="12">164</text>
<text x="626" y="220" fill="#8F9A72" font-size="12">176</text>
<text x="590" y="248" fill="#9A9488" font-size="12">normal 170, σ=6</text>
'''
build(
34, 'Uniforme, binomial y <em>normal</em>', 'E.3 Uniforme discreta y continua, binomial y normal',
'El modelo se elige antes de echar la cuenta',
'Cuatro preguntas de verdadero o falso respondidas al azar siguen una binomial de n = 4 y p = 1/2. La barra clara es el ejemplo: tres aciertos, probabilidad 4/16. Al lado, una normal de media 170 cm y desviación 6 marca el intervalo de una desviación típica. El dado y la espera del autobús cubren las dos uniformes.',
['Calcular probabilidades binomiales con n pequeño a partir del número de caminos.',
 'Usar la longitud del intervalo en una uniforme continua y el recuento de caras en una discreta.',
 'Tipificar antes de aplicar la regla empírica de la normal.'],
'''<h2>Tres modelos, tres maneras de contar</h2>
<p>No toda probabilidad sale de listar el espacio a mano. Cuando los resultados son equiprobables y finitos, basta la uniforme discreta. Cuando lo equiprobable es un continuo, la probabilidad es longitud a favor entre longitud total. Cuando se repite n veces, en las mismas condiciones e independientes, un éxito de probabilidad p, aparece la binomial. La normal entra cuando los datos se acumulan en campana alrededor de una media, y entonces se trabaja en desviaciones típicas, no en centímetros crudos.</p>
<p><span class="glosa">uniforme discreta: P = 1/n en cada caso · uniforme continua en [0, L]: P(a ≤ X ≤ b) = (b − a)/L · binomial: P(X = k) = C(n, k) p^k (1 − p)^(n − k) · en la normal, z = (x − μ) / σ · regla empírica aproximada: unos 68 % a menos de una σ, unos 95 % a menos de dos</span></p>
<p>En la binomial del gráfico, p = 1/2 y (1/2)^4 = 1/16, así que cada secuencia concreta de cuatro respuestas vale 1/16. Tres aciertos son las secuencias con exactamente tres sí: hay C(4, 3) = 4, luego P(X = 3) = 4/16 = 1/4. Esa es la barra clara. La barra central, seis dieciseisavos, es el caso de dos aciertos, el más frecuente, y no hay que confundirlo con el ejemplo solo porque sea más alta.</p>
<p>La campana de la derecha no está en la misma escala: es otra variable, la estatura, con μ = 170 y σ = 6. Las rectas verdes marcan 164 y 176, es decir μ ± σ. La regla empírica dice que alrededor del 68 % de una normal cae entre ellas. No es una barra de la binomial ni un porcentaje leído del eje de los aciertos.</p>''',
'Barras binomiales 1, 4, 6, 4 y 1 sobre 16, con P(X=3) marcada, y campana normal entre 164 y 176', fig34,
[
('Tres aciertos al azar',
 'En cuatro preguntas justo al azar, calcula P(X = 3) y explica de dónde sale el 4 del numerador.',
 [
  ('Cada secuencia de cuatro respuestas tiene probabilidad (1/2)^4 = 1/16. Acertar o fallar una concreta no cambia el peso de las demás.',
   'Glosa: p = 1 − p = 1/2, así que no hace falta separar p^k y (1 − p)^(n − k): todo es 1/16.'),
  ('Las secuencias con exactamente tres aciertos son cuatro: falla solo la primera, o solo la segunda, o solo la tercera, o solo la cuarta.',
   'Glosa: C(4, 3) = 4. También C(4, 1) = 4, porque elegir qué pregunta se falla es lo mismo.'),
  ('P(X = 3) = 4/16 = 1/4. En la figura es la barra clara, no la más alta.',
   'Glosa: la más alta es k = 2, con 6/16. El ejemplo pide tres aciertos, no «el caso típico».'),
  ('Comprobación de todo el modelo: 1 + 4 + 6 + 4 + 1 = 16, y 16/16 = 1. Si la barra del 3 se leyera como 3/16, la suma ya no cerraría.',
   'Glosa: el numerador es el número de caminos, no el valor k.'),
 ]),
('Dos uniformes distintas',
 'Un dado justo: probabilidad de sacar 1 o 2. Una espera al autobús, uniforme entre 0 y 30 minutos: probabilidad de esperar menos de 10. Compara las dos cuentas.',
 [
  ('Dado: seis caras equiprobables, P(cada cara) = 1/6. Sacar 1 o 2 son dos caras, 2/6 = 1/3.',
   'Glosa: uniforme discreta cuenta casos favorables entre casos posibles. El 6 es el número de caras, no un minuto.'),
  ('Autobús: cualquier instante entre 0 y 30 es igual de plausible. La probabilidad es longitud, 10/30 = 1/3.',
   'Glosa: uniforme continua no tiene «caras». El 30 es la longitud del intervalo total.'),
  ('Los dos resultados valen 1/3 y no son el mismo modelo. Uno cuenta 2 de 6; el otro mide 10 de 30.',
   'Glosa: que el número coincida es casual. La unidad de la cuenta es lo que distingue los modelos.'),
  ('Si el autobús solo pudiera llegar en el minuto 0, 10, 20 o 30, ya no sería continua. El enunciado de «en cualquier momento» es lo que autoriza a dividir longitudes.',
   'Glosa: elegir el modelo es leer cómo se genera el azar, antes de operar.'),
 ]),
('Estatura a dos desviaciones',
 'Estaturas normales de media 170 cm y desviación típica 6 cm. Un alumno mide 182 cm. Tipifica y sitúalo con la regla empírica.',
 [
  ('Puntuación z: (182 − 170) / 6 = 12/6 = 2. Está exactamente dos desviaciones típicas por encima de la media.',
   'Glosa: sin dividir entre σ, 12 cm no se sabe si es mucho. Con σ = 6, 12 cm son dos unidades estándar.'),
  ('La regla empírica coloca alrededor del 95 % entre μ − 2σ y μ + 2σ, esto es entre 158 y 182.',
   'Glosa: 170 − 12 = 158 y 170 + 12 = 182. El 182 es el borde superior de ese intervalo.'),
  ('Por encima de dos desviaciones, en un solo lado, queda alrededor de la mitad del 5 % exterior, cerca del 2,5 %.',
   'Glosa: la campana es simétrica. El 5 % de fuera se reparte en dos colas de unos 2,5 %.'),
  ('No se dice «182 está cerca de 170 porque solo hay 12 cm». Doce centímetros son muchos cuando σ vale 6. La figura marca solo ±1σ, de 164 a 176; 182 cae fuera de esas dos rectas verdes.',
   'Glosa: primero z, después la regla. El centímetro crudo no es la unidad del modelo.'),
 ]),
],
[
(1, 'Al menos tres aciertos',
 'Con la misma binomial de la figura, calcula P(X ≥ 3). Explica por qué no basta la barra clara.',
 'El paso es sumar las barras que cumplen la desigualdad, no leer solo la que el ejemplo había marcado. X ≥ 3 incluye k = 3 y k = 4, con numeradores 4 y 1. La probabilidad es 4/16 + 1/16 = 5/16. La barra clara, 4/16, es exactamente tres aciertos; dejar fuera el 1/16 sería contestar P(X = 3) a un enunciado que dice «al menos». Las barras de 0, 1 y 2 no entran. Comprobación por el complementario: P(X ≤ 2) = (1 + 4 + 6)/16 = 11/16, y 1 − 11/16 = 5/16. El valor k no se suma: se suman las probabilidades de los k favorables.',
 'e34a'),
(2, 'Espera entre 10 y 20',
 'El autobús llega al azar uniforme entre el minuto 0 y el 30. ¿Qué probabilidad hay de esperar entre 10 y 20 minutos, incluidos?',
 'El paso es restar los extremos del tramo favorable y dividir entre la longitud total, no contar minutos como si fueran caras de un dado discreto mal definido. El tramo mide 20 − 10 = 10 minutos y el total mide 30, luego 10/30 = 1/3. Incluir o no los extremos no cambia la probabilidad en una continua, porque un instante suelto tiene longitud cero. No es 11/31 ni un conteo de enteros: el modelo del enunciado es la uniforme continua, la misma en la que esperar menos de 10 ya valía 10/30. Dos tramos de la misma longitud tienen la misma probabilidad, y por eso este tercio coincide con el de los diez primeros minutos.',
 'e34b'),
(3, 'Dentro de una desviación',
 'Con media 170 y σ = 6, ¿entre qué estaturas cae, aproximadamente, el 68 % central? ¿182 entra en ese intervalo?',
 'El paso es sumar y restar una sola desviación típica a la media, no dos, porque el 68 % de la regla empírica es el intervalo μ ± σ. 170 − 6 = 164 y 170 + 6 = 176. Esas son las rectas verdes de la figura. El 182 está en z = 2, fuera de ese intervalo: entra en el del 95 %, que llega hasta 182, y no en el del 68 %. Confundir «una desviación» con «dos» cambiaría las marcas a 158 y 182 y metería al alumno dentro del porcentaje equivocado. La regla es aproximada y solo se aplica cuando el enunciado sostiene que la variable es normal; no es una propiedad de cualquier lista de estaturas.',
 'e34c'),
],
[
('¿Cuánto vale P(X = 3) en la binomial de la figura y por qué el numerador es 4?',
 'Vale 4/16 = 1/4. Por qué: cada una de las 16 secuencias pesa lo mismo y hay exactamente 4 con tres aciertos, una por cada pregunta que se falla. La barra clara marca ese caso. No es 3/16: el 3 es el número de aciertos, no el número de caminos.'),
('¿Por qué 2/6 en el dado y 10/30 en el autobús pueden coincidir y no ser el mismo modelo?',
 'Porque uno cuenta caras y el otro mide minutos. Por qué: los dos cocientes valen 1/3, pero la uniforme discreta parte de 6 resultados y la continua parte de un intervalo de longitud 30. Elegir mal la unidad cambia el denominador en el siguiente problema.'),
('¿Dónde está 182 cm si μ = 170 y σ = 6?',
 'En z = 2, el borde del intervalo del 95 % aproximado, y fuera del intervalo 164 a 176. Por qué: (182 − 170)/6 = 2. La figura marca solo una desviación típica. Doce centímetros no se interpretan sin dividir entre σ.'),
],
'Marca la barra del tres',
'Copia en el lienzo las cinco barras con sus numeradores 1, 4, 6, 4 y 1, destaca la de tres aciertos y anota 4/16. Al lado, marca 164 y 176 alrededor de 170.',
['La barra clara es k = 3, numerador 4, no la barra más alta.',
 'Los cinco numeradores suman 16. El modelo cierra.',
 'Ejemplo 1: P(X = 3) = 4/16 porque hay cuatro secuencias.',
 'Ejemplo 2: el dado da 2/6 y el autobús da 10/30. Misma cifra, distinta unidad.',
 'Ejemplo 3: 182 cm está a z = 2. La campana verde marca solo ±1σ.',
 'El laboratorio cambia k y repinta la barra ámbar de la binomial.',
 'Primero el modelo, después la cuenta. No al revés.'],
lab_title='Binomial n=4 y la barra del ejemplo')

print('L34 escrito')

# ---------- L35 ----------
fig35 = '''
<line x1="60" y1="260" x2="680" y2="260" stroke="#9A9488" stroke-width="1.6"/>
<line x1="60" y1="260" x2="60" y2="30" stroke="#9A9488" stroke-width="1.6"/>
<polygon points="110,260 210,260 210,92 110,92" fill="#2a261c" stroke="#9A9488" stroke-width="1.4"/>
<polygon points="110,260 210,260 210,232 110,232" fill="#C4A15A" stroke="#E6E1D6" stroke-width="1.2"/>
<polygon points="280,260 380,260 380,159 280,159" fill="#2a261c" stroke="#9A9488" stroke-width="1.4"/>
<polygon points="280,260 380,260 380,243 280,243" fill="#C4A15A" stroke="#E6E1D6" stroke-width="1.2"/>
<polygon points="450,260 550,260 550,193 450,193" fill="#2a261c" stroke="#9A9488" stroke-width="1.4"/>
<polygon points="450,260 550,260 550,249 450,249" fill="#C4A15A" stroke="#E6E1D6" stroke-width="1.2"/>
<circle cx="160" cy="246" r="6" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<circle cx="330" cy="251" r="6" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<circle cx="500" cy="254" r="6" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<line x1="60" y1="92" x2="70" y2="92" stroke="#9A9488" stroke-width="1.2"/>
<line x1="60" y1="176" x2="70" y2="176" stroke="#9A9488" stroke-width="1.2"/>
<text x="28" y="96" fill="#9A9488" font-size="12">120</text>
<text x="36" y="180" fill="#9A9488" font-size="12">60</text>
<text x="145" y="282" fill="#E6E1D6" font-size="13">Ciencias</text>
<text x="300" y="282" fill="#E6E1D6" font-size="13">Humanidades</text>
<text x="475" y="282" fill="#E6E1D6" font-size="13">General</text>
<text x="118" y="84" fill="#E6E1D6" font-size="13">120</text>
<text x="292" y="150" fill="#E6E1D6" font-size="13">72</text>
<text x="468" y="184" fill="#E6E1D6" font-size="13">48</text>
<text x="118" y="226" fill="#1C1A16" font-size="13">muestra 20</text>
<text x="288" y="238" fill="#1C1A16" font-size="12">12</text>
<text x="462" y="246" fill="#1C1A16" font-size="11">8</text>
<text x="80" y="24" fill="#C4A15A" font-size="14">240 alumnos · muestra proporcional 40 · fracción 1/6 en ámbar</text>
'''
build(
35, 'Muestreo e <em>inferencia</em>', 'E.4 Muestras, representatividad, validez y diseño',
'A quién preguntas forma parte del resultado',
'Un instituto de 240 alumnos de Bachillerato: 120 de Ciencias, 72 de Humanidades y 48 de General. Se quiere una muestra de 40. El diseño proporcional reparte 20, 12 y 8, la misma fracción 1/6 en cada modalidad. Preguntar solo en la biblioteca no se arregla preguntando a más voluntarios.',
['Diseñar una muestra estratificada proporcional y comprobar que los cupos suman el tamaño previsto.',
 'Distinguir un sesgo de marco (a quién se puede llegar) de un problema de tamaño.',
 'Juzgar si la pregunta mide el constructo que se dice estudiar.'],
'''<h2>Marco, azar y la pregunta que de verdad se hace</h2>
<p>Inferir del instituto entero a partir de unos pocos exige que esos pocos puedan estar en el lugar de cualquiera. Hace falta un marco (la lista de los 240), un procedimiento de azar dentro de ese marco y una pregunta que signifique lo que el estudio dice querer saber. El tamaño importa, pero un marco torcido no se cura añadiendo gente del mismo sitio equivocado.</p>
<p><span class="glosa">población = 240 · estrato = modalidad · fracción de muestreo = 40/240 = 1/6 · cupo = fracción por tamaño del estrato · sesgo de selección = la muestra no puede representar a quien el marco nunca incluye · validez = la pregunta corresponde al constructo</span></p>
<p>Ciencias recibe 120 · (1/6) = 20; Humanidades, 72 · (1/6) = 12; General, 48 · (1/6) = 8. Los cupos suman 40. En la figura, la altura entera es la población del estrato y el tramo ámbar es la muestra: en los tres la altura ámbar es un sexto de la barra. Dentro de cada estrato los 20, los 12 o los 8 se eligen al azar sobre el censo, no entre quienes levantan la mano.</p>
<p>Una muestra voluntaria de 25 personas en la biblioteca, aunque 20 digan que estudian tres horas o más (20/25 = 0,80), describe a quien estaba allí. Ampliarla a 50 voluntarios repite el mismo marco. Y una pregunta distinta de la que se cree hacer —«¿estudias lo suficiente?» frente a las horas de una semana— puede ser válida como opinión e inválida como medida del hábito.</p>''',
'Estratos 120, 72 y 48 con la muestra proporcional 20, 12 y 8 marcada en ámbar', fig35,
[
('Los tres cupos',
 'Reparte una muestra de 40 sobre 120, 72 y 48 de modo proporcional. Comprueba la suma y la fracción común.',
 [
  ('Fracción: 40/240 = 1/6. Se usa la misma en los tres estratos precisamente porque el diseño es proporcional, no porque los estratos sean iguales.',
   'Glosa: 120 + 72 + 48 = 240. Si la población estuviera mal sumada, la fracción ya no sería 1/6.'),
  ('Cupos: 120/6 = 20, 72/6 = 12 y 48/6 = 8. En la figura son las alturas ámbar.',
   'Glosa: 72 no es divisible entre 10, pero sí entre 6. El tamaño 40 está elegido para que los cupos salgan enteros.'),
  ('Suma: 20 + 12 + 8 = 40. Si saliera 39 o 41, sobraría o faltaría una persona y el redondeo habría que decidirlo a propósito, no dejarlo caer.',
   'Glosa: en este diseño no hay resto. La comprobación es inmediata.'),
  ('Dentro de cada cupo el azar actúa sobre el censo del estrato. El número 20 no dice todavía qué personas: dice cuántas.',
   'Glosa: proporcional fija el tamaño; el sorteo fija los nombres. Las dos piezas son el diseño.'),
 ]),
('Cincuenta voluntarios siguen sesgados',
 'En la biblioteca, 20 de 25 voluntarios dicen estudiar al menos tres horas. Alguien propone preguntar a otros 25 voluntarios del mismo sitio para «corregir el sesgo». ¿Qué se corrige y qué no?',
 [
  ('La proporción observada es 20/25 = 0,80. Describe a esos 25, no a los 240. El marco es «quien está en la biblioteca y acepta», no el censo.',
   'Glosa: el denominador 25 no es una muestra aleatoria de 240. No se le aplica la lectura de los cupos.'),
  ('Otros 25 voluntarios del mismo sitio agrandan el mismo marco. Si el hábito de la biblioteca no es el del instituto, el error se estima con más precisión y no desaparece.',
   'Glosa: el sesgo de selección no es varianza. Más datos del mismo sesgo aprietan alrededor del valor equivocado.'),
  ('Para representar a Ciencias, Humanidades y General haría falta volver a la lista de 240 y sortear, por ejemplo, los cupos 20, 12 y 8.',
   'Glosa: cambiar de marco es cambiar de diseño. No es un ajuste del porcentaje 0,80.'),
  ('El 0,80 puede ser verdad dentro de la biblioteca y ser inútil para el claustro si la decisión afecta a quien no pisa esa sala. La frase del estudio tiene que nombrar la población.',
   'Glosa: inferir es decir a quién se extiende el número. Sin esa frase, el número no sale del pasillo.'),
 ]),
('La pregunta y el hábito',
 'Se quiere el hábito de estudio. Un alumno declara 0 horas ayer. Su semana fue 0, 2, 1, 0, 5, 1 y 0. Compara las dos medidas y di cuál se acerca al constructo.',
 [
  ('Ayer: 0 horas. Como retrato de un día, puede ser exacto. Como retrato del hábito, usa un solo día que además fue un cero.',
   'Glosa: un día es una observación. El hábito es una regularidad, y una observación no la fija.'),
  ('Semana: 0 + 2 + 1 + 0 + 5 + 1 + 0 = 9 horas en 7 días. Media diaria 9/7 ≈ 1,29 horas, no 0.',
   'Glosa: el 5 del quinto día tira de la media. Un único cero la habría dejado en el suelo.'),
  ('«¿Estudias lo suficiente?» ni siquiera produce estas cifras: produce un juicio. Puede ser válida como opinión y no mide el hábito en horas.',
   'Glosa: validez es ajuste entre la pregunta y el constructo declarado, no entre la pregunta y lo que sea fácil de responder.'),
  ('Un buen diseño de este estudio une las tres piezas: marco de 240, cupos proporcionales y una pregunta de horas en varios días. Fallar una de las tres no se compensa adornando las otras.',
   'Glosa: muestreo sin validez mide con precisión otra cosa. Validez sin marco mide bien a quien no es la población.'),
 ]),
],
[
(1, 'Otra población, la misma fracción',
 'Población de 180 alumnos en tres grupos de 90, 60 y 30. Diseña una muestra proporcional de 30. Escribe los cupos y su suma.',
 'El paso es calcular la fracción 30/180 = 1/6 y multiplicarla por cada grupo, no repartir 10, 10 y 10 como si los grupos fueran iguales. Los cupos son 90/6 = 15, 60/6 = 10 y 30/6 = 5. Suman 30, que es el tamaño pedido, y cada grupo aporta la misma fracción que en el instituto de 240. Un reparto igualitario de 10 por grupo sobrerrepresentaría al de 30 (10/30) y infrarrepresentaría al de 90 (10/90). Solo sería correcto si el diseño, dicho de antemano, fuera de cupos iguales y no proporcional. Aquí el enunciado pide proporcionalidad, así que el tamaño del estrato entra en la multiplicación.',
 'e35a'),
(2, 'Precisión no es ausencia de sesgo',
 'Explica, con el ejemplo de la biblioteca, la diferencia entre ampliar la muestra voluntaria y cambiar el marco a los 240 del censo.',
 'El paso es separar el error de quién puede entrar en la muestra del error de cuántos entran. Los 25 voluntarios, y también 50, solo incluyen a quien está en la biblioteca y acepta hablar. Si esa gente estudia más que el instituto, todas las estimaciones quedan desplazadas hacia arriba, y ampliar el número aprieta el resultado alrededor de ese valor desplazado: baja la oscilación y no baja el sesgo. Pasar al censo de 240, con un sorteo dentro de los estratos, cambia quién puede ser elegido. Esa es la corrección del marco. Mientras el procedimiento siga siendo «quien pasa por delante», el tamaño es un detalle y el sesgo es la estructura.',
 'e35b'),
(3, 'Redactar la pregunta',
 'El claustro quiere saber el hábito de estudio, no la opinión sobre uno mismo. Escribe una pregunta más válida que «¿estudias lo suficiente?» y di qué dato de la semana de 9 horas en 7 días usarías.',
 'El paso es pedir un comportamiento contable en un periodo, no un adjetivo. Una redacción válida sería: «¿cuántas horas estudiaste cada uno de los últimos siete días, sin contar el tiempo en el instituto?». El dato que resume el hábito en el ejemplo es la media 9/7 ≈ 1,29 horas al día, no el 0 de ayer ni la palabra «suficiente», que cada alumno corta en un sitio distinto. Hace falta, además, hacer esa pregunta sobre la muestra diseñada, no solo sobre un alumno. Validez de la pregunta y representatividad de la muestra se exigen juntas: una semana bien medida en la biblioteca seguiría sin describir a los 240.',
 'e35c'),
],
[
('¿Qué cupos corresponden a 120, 72 y 48 si la muestra es de 40?',
 '20, 12 y 8. Por qué: la fracción es 40/240 = 1/6, y 120/6 = 20, 72/6 = 12, 48/6 = 8. Suman 40. En la figura el ámbar es ese sexto de cada barra, no una altura caprichosa.'),
('¿Por qué otros 25 voluntarios de la biblioteca no quitan el sesgo?',
 'Porque siguen dejando fuera a quien no está allí. Por qué: el marco no es el censo de 240. Más voluntarios del mismo sitio estiman mejor el comportamiento de la biblioteca y siguen sin estimar el del instituto. El sesgo de selección no se promedia al subir n.'),
('¿Qué medida se acerca más al hábito, el 0 de ayer o la semana?',
 'La media de la semana, 9/7 ≈ 1,29 horas. Por qué: el hábito es una regularidad de varios días y ayer fue un cero suelto. La pregunta «¿estudias lo suficiente?» ni siquiera da horas: da un juicio, y no es válida para el constructo «horas de estudio».'),
],
'Cupos antes que opiniones',
'Dibuja en el lienzo tres barras con los tamaños 120, 72 y 48, marca el sexto de cada una y escribe 20, 12 y 8. Añade una frase con la población a la que sí se podría extender el resultado.',
['Tres estratos, alturas 120, 72 y 48. El ámbar es la muestra: 20, 12 y 8.',
 'La fracción común es 1/6 porque 40/240 = 1/6.',
 'Ejemplo 1: los cupos suman 40 y el sorteo todavía tiene que elegir los nombres.',
 'Ejemplo 2: 20/25 = 0,80 en la biblioteca no se cura con más voluntarios.',
 'Ejemplo 3: la semana suma 9 horas y la media es 9/7, no el cero de ayer.',
 'Marco, azar y pregunta son las tres piezas. Falta una y el estudio cojea.',
 'El tamaño afina. El marco equivocado desplaza.'],
)

print('L35 escrito')

# ---------- L36 ----------
_dots = []
for _i in range(20):
    _cx = 48 + (_i % 10) * 28
    _cy = 46 + (_i // 10) * 28
    _dots.append(f'<circle cx="{_cx}" cy="{_cy}" r="8" fill="#1C1A16" stroke="#C4A15A" stroke-width="1.6"/>')
fig36 = '\n'.join(_dots) + '''
<text x="40" y="110" fill="#9A9488" font-size="13">20 alumnos · suma de libros = 39</text>
<line x1="360" y1="70" x2="470" y2="70" stroke="#C4A15A" stroke-width="2"/>
<text x="400" y="58" text-anchor="middle" fill="#E6E1D6" font-size="18">39</text>
<text x="400" y="96" text-anchor="middle" fill="#E6E1D6" font-size="18">20</text>
<line x1="560" y1="70" x2="670" y2="70" stroke="#9A9488" stroke-width="2"/>
<text x="600" y="58" text-anchor="middle" fill="#9A9488" font-size="18">39</text>
<text x="600" y="96" text-anchor="middle" fill="#9A9488" font-size="18">19</text>
<line x1="545" y1="40" x2="685" y2="110" stroke="#C4A15A" stroke-width="2.4"/>
<text x="360" y="140" fill="#C4A15A" font-size="14">denominador n = 20</text>
<text x="520" y="140" fill="#9A9488" font-size="14">n − 1 no es la media</text>
<text x="40" y="180" fill="#E6E1D6" font-size="15">El fallo está en la raya de la división, no en la persona que la escribió.</text>
<line x1="40" y1="200" x2="660" y2="200" stroke="#3a3428" stroke-width="1.2"/>
<polygon points="40,230 200,230 200,280 40,280" fill="#1C1A16" stroke="#C4A15A" stroke-width="1.5"/>
<polygon points="240,230 460,230 460,280 240,280" fill="#1C1A16" stroke="#8F9A72" stroke-width="1.5"/>
<polygon points="500,230 680,230 680,280 500,280" fill="#1C1A16" stroke="#E6E1D6" stroke-width="1.5"/>
<text x="120" y="260" text-anchor="middle" fill="#E6E1D6" font-size="13">1. señalar el paso</text>
<text x="350" y="260" text-anchor="middle" fill="#E6E1D6" font-size="13">2. rehacer esa línea</text>
<text x="590" y="260" text-anchor="middle" fill="#E6E1D6" font-size="13">3. seguir en equipo</text>
'''
build(
36, 'Emociones, error y <em>equipo</em>', 'F.1 y F.2 Autoconciencia, error, decisiones y trabajo en equipo',
'El error tiene sitio en la página, no en la identidad',
'Un equipo calcula la media de los 20 alumnos y 39 libros de la lección de estadística. Alguien divide entre 19, obtiene cerca de 2,05 y dice «es que no valgo». El denominador se señala, se rehace y el equipo sigue. La persona no era el dato equivocado.',
['Localizar el paso concreto de un error de cálculo y separarlo del juicio sobre la persona.',
 'Tratar un desacuerdo numérico como información: dos resultados distintos obligan a revisar, no a subir la voz.',
 'Acordar una regla de decisión antes de mirar quién defiende cada cifra.'],
'''<h2>Señalar la línea, no a quien la escribió</h2>
<p>El sentido socioafectivo de Matemáticas Generales no es un añadido blando al margen de las cuentas. El error forma parte del trabajo, y la manera de tratarlo cambia lo que el equipo vuelve a intentar. Insultar el resultado, o insultarse, esconde el paso. Nombrar el paso lo deja a la vista y se puede rehacer.</p>
<p><span class="glosa">error localizado = una línea concreta (un denominador, un signo, una operación) · atribución global = «no valgo», que no dice qué rehacer · revisión en paralelo = dos personas calculan lo mismo sin copiarse · regla de decisión = el criterio escrito antes de saber a quién favorece</span></p>
<p>En el caso de la media, la suma 39 puede estar bien y fallar solo la raya de abajo. La media de los 20 datos usa denominador 20: 39/20 = 1,95. El 19 aparece en otras fórmulas, por ejemplo al estimar una varianza con n − 1, y aquí nadie ha pedido esa varianza. Quien escribió 19 no «es de letras»: ha mezclado dos denominadores que este curso sí distingue. El arreglo es una frase del tipo «en esta línea el denominador es n», dicha sobre el papel.</p>
<p>Lo mismo ocurre con un porcentaje mal convertido o con tres predicciones distintas en un grupo. El volumen de la voz no es un criterio matemático. Sí lo es volver a hacer la operación en paralelo, o haber escrito antes cómo se va a elegir la cifra cuando no coincidan. El lienzo de esta lección sirve para dibujar el paso, no para dibujar una cara.</p>''',
'Veinte alumnos, la fracción 39/20 frente a 39/19 tachada, y tres pasos de revisión', fig36,
[
('La raya que sobra un alumno',
 'El equipo tiene suma 39 y n = 20. Un miembro hace 39/19 ≈ 2,05 y aparta el cuaderno. Reconstruye la corrección matemática y la frase que corresponde decir.',
 [
  ('La media pedida es 39/20 = 1,95. El denominador es el número de alumnos, que está dibujado: son 20 círculos.',
   'Glosa: 39 ÷ 20 = 1,95 exactamente, porque 20 · 1,95 = 39.'),
  ('39/19 ≈ 2,053 no es «casi la media». Es la misma suma partida en un grupo que no existe. El 19 sería otro estadístico, no este.',
   'Glosa: cambiar el denominador en una unidad, de 20 a 19, mueve el resultado en más de una décima. No es un redondeo.'),
  ('La frase útil nombra la línea: «el denominador de esta media es 20, no 19». La frase inútil nombra a la persona: «no vales para esto».',
   'Glosa: la primera frase se puede comprobar en el papel. La segunda no dice qué número cambiar.'),
  ('Después de corregir, el cuaderno sigue en la mesa. Apartarlo convierte un denominador en una identidad, y el equipo pierde a quien ya había hecho bien la suma.',
   'Glosa: la suma 39 no había que rehacerla. Localizar ahorra trabajo y ahorra humillación.'),
 ]),
('Quince por ciento escrito como quince veces',
 'Hay que calcular el 15 % de 80 euros. Una persona obtiene 12 y otra obtiene 1200, y la segunda se calla. ¿Dónde está el paso y cómo se revisa sin dejarla fuera?',
 [
  ('El 15 % es 15/100 = 0,15. Entonces 0,15 · 80 = 12. La cifra 12 es la cuota correcta.',
   'Glosa: 0,15 · 80 = 15 · 0,8 = 12. También 15 · 80 / 100 = 1200/100 = 12.'),
  ('1200 es 15 · 80 sin dividir entre 100. El fallo es un paso, la conversión del porcentaje, no el desconocimiento de la multiplicación.',
   'Glosa: quien obtuvo 1200 sabe multiplicar. Le falta la centésima. Decirle que «no multiplica» es falso y no ayuda.'),
  ('La revisión en equipo pone las dos operaciones en la misma hoja y se pregunta en qué línea divergen. Divergen al no escribir /100.',
   'Glosa: comparar líneas es más preciso que votar la cifra de quien habla más alto.'),
  ('Callarse para no molestar esconde el 1200, que era la pista. Un equipo que agradece el resultado distinto encuentra antes el paso.',
   'Glosa: el desacuerdo, escrito, es dato. El silencio no comprueba nada.'),
 ]),
('Cuatro estimaciones y una regla',
 'Antes de abrir las notas, el equipo acuerda: «la predicción del grupo será la media de las cuatro estimaciones, salvo que una no explique su cuenta». Las estimaciones son 4, 6, 8 y 14. La de 14 era un 1,4 leído como 14. Aplica la regla.',
 [
  ('Regla escrita antes de conocer las cifras: se promedia solo lo que trae una cuenta explicada. La regla no se cambia al ver el 14.',
   'Glosa: decidir el criterio después permite empujar el resultado hacia la cifra que a alguien le conviene.'),
  ('El 14 no trae una cuenta de horas o de notas: es un error de coma al leer 1,4. Según la regla, no entra en la media.',
   'Glosa: excluirlo no es excluir a la persona. Es no usar un número que ella misma reconoce como mal leído.'),
  ('Media de las tres restantes: (4 + 6 + 8) / 3 = 18/3 = 6. Si se hubiera promediado todo a ciegas, (4+6+8+14)/4 = 8, arrastrando la coma.',
   'Glosa: 8 no es «más democrático». Es la media de un dato que no significa lo que el equipo cree.'),
  ('Quien leyó 1,4 sigue en el equipo y ahora sabe qué tipo de error vigilar. La regla ha hecho de filtro sin necesidad de una discusión de voces.',
   'Glosa: el criterio previo convierte el conflicto en una comprobación. Eso es una decisión matemática en grupo.'),
 ]),
],
[
(1, 'Qué frase repara',
 'Tu compañera ha dividido 39 entre 19 y dice «soy un desastre en mates». Escribe la respuesta que localiza el paso y la que conviene no decir.',
 'El paso que hay que nombrar es el denominador: la media de los 20 alumnos es 39/20 = 1,95, y el 19 no corresponde a este cálculo. Una respuesta que repara sería: «la suma 39 está bien; en la raya de abajo tiene que ir 20, porque hay 20 datos, y sale 1,95». Una respuesta que no repara es «tranquila, a mí tampoco se me dan» o «es que eres un desastre», porque ninguna de las dos cambia el 19 por el 20 ni invita a rehacer la línea. El error queda pegado a la identidad y el equipo no aprende a distinguir la media de otras fórmulas que sí usan n − 1. Señalar la línea devuelve el cuaderno a la mesa.',
 'e36a'),
(2, 'Dos resultados, una multiplicación',
 'En paralelo, una persona obtiene 12 euros y otra 1200 al calcular el 15 % de 80. Describe el protocolo de revisión, no el veredicto sobre quién es mejor.',
 'El protocolo es poner las dos cadenas de operaciones una bajo la otra y marcar la primera línea en la que ya no coinciden, sin votar todavía. Las dos habrán escrito 15 y 80. La que llega a 12 ha dividido entre 100 o ha usado 0,15; la que llega a 1200 ha multiplicado 15 · 80 y se ha quedado ahí. El paso ausente es /100, y 1200/100 = 12 cierra la discrepancia. No hace falta declarar ganadora a la persona del 12: hace falta que las dos vean la centésima. Trabajar en paralelo, sin copiarse, es lo que ha producido dos cifras y, con ellas, la posibilidad de encontrar el salto. Si una sola persona calcula y las demás asienten, el 1200 puede quedar de resultado oficial.',
 'e36b'),
(3, 'La regla antes del número',
 'El equipo aún no ha oído las estimaciones. Propón en una frase la regla que usaríais para resumirlas y aplícala luego a 4, 6, 8 y 14 sabiendo que 14 era un 1,4 mal leído.',
 'Una regla previa posible es: «promediaremos solo las estimaciones cuya cuenta se pueda explicar, y no cambiaremos la regla al ver los números». Aplicada a estos datos, el 14 se reconoce como una coma corrida al leer 1,4, así que no entra, y la media es (4 + 6 + 8) / 3 = 6. Si la regla se improvisa después, alguien puede defender el 8 de la media ingenua porque le favorece, y la discusión ya no es sobre la coma sino sobre el peso de cada voz. Escribir el criterio primero convierte la revisión en un procedimiento, que es lo que esta lección pide al trabajo en equipo: una decisión repetible, no una negociación de ánimos. Quien se equivocó al leer sigue dentro y corrige la lectura.',
 'e36c'),
],
[
('¿Por qué 39/19 no es la media de los 20 alumnos?',
 'Porque el denominador de esa media es 20, el número de datos, y 39/20 = 1,95. Por qué: el 19 no cuenta a ningún alumno que falte; es una unidad menos puesta por confusión con otras fórmulas. El dibujo tiene 20 círculos. Cambiar la raya de abajo cambia el resultado en más de una décima y no es un redondeo.'),
('Al calcular el 15 % de 80, ¿qué paso separa 12 de 1200?',
 'Dividir entre 100, o multiplicar por 0,15 en vez de por 15. Por qué: 15 · 80 = 1200 y 1200/100 = 12. Quien obtiene 1200 no ha fallado la multiplicación; ha dejado el porcentaje sin convertir. La revisión compara líneas, no personas.'),
('¿Por qué la regla de decisión se escribe antes de oír las estimaciones?',
 'Porque si se elige después, el criterio se puede torcer hacia la cifra que a alguien le conviene. Por qué: con 4, 6, 8 y un 14 que en realidad era 1,4, una regla previa de «solo lo que tenga cuenta» da media 6. Improvisar permite colar el 14 y obtener 8 sin discutir la coma. El equipo necesita un procedimiento, no la voz más fuerte.'),
],
'La línea, en voz baja y clara',
'En el lienzo escribe una operación con un error que hayas cometido de verdad este curso, rodéalo y al lado anota la frase que señala el paso, no a la persona.',
['Veinte círculos y la fracción 39/20. La fracción 39/19 está tachada.',
 'Debajo, el protocolo: señalar el paso, rehacer esa línea, seguir en equipo.',
 'Ejemplo 1: la media es 1,95. La frase útil nombra el denominador.',
 'Ejemplo 2: 0,15 · 80 = 12. El 1200 es la misma multiplicación sin la centésima.',
 'Ejemplo 3: la regla previa deja fuera el 14 mal leído y la media queda en 6.',
 'Un desacuerdo escrito es una pista. Un silencio no comprueba.',
 'El error se queda en la página. No se convierte en identidad.'],
)

print('L36 escrito')

# ---------- L37 ----------
fig37 = '''
<polygon points="80,70 230,70 230,220 80,220" fill="#1C1A16" stroke="#E6E1D6" stroke-width="1.5"/>
<polygon points="230,70 310,70 310,220 230,220" fill="#241c12" stroke="#C4A15A" stroke-width="1.6"/>
<polygon points="80,220 230,220 230,290 80,290" fill="#241c12" stroke="#C4A15A" stroke-width="1.6"/>
<polygon points="230,220 310,220 310,290 230,290" fill="#3a2e16" stroke="#C4A15A" stroke-width="2"/>
<line x1="80" y1="70" x2="310" y2="70" stroke="#C4A15A" stroke-width="2"/>
<line x1="310" y1="70" x2="310" y2="290" stroke="#C4A15A" stroke-width="2"/>
<line x1="310" y1="290" x2="80" y2="290" stroke="#C4A15A" stroke-width="2"/>
<line x1="80" y1="290" x2="80" y2="70" stroke="#C4A15A" stroke-width="2"/>
<line x1="230" y1="70" x2="230" y2="290" stroke="#9A9488" stroke-width="1.4"/>
<line x1="80" y1="220" x2="310" y2="220" stroke="#9A9488" stroke-width="1.4"/>
<text x="140" y="150" fill="#E6E1D6" font-size="18">x²</text>
<text x="255" y="150" fill="#C4A15A" font-size="16">5x</text>
<text x="140" y="260" fill="#C4A15A" font-size="16">5x</text>
<text x="258" y="262" fill="#E6E1D6" font-size="16">25</text>
<text x="140" y="54" fill="#9A9488" font-size="14">lado x</text>
<text x="330" y="150" fill="#C4A15A" font-size="14">5</text>
<text x="80" y="312" fill="#E6E1D6" font-size="14">(x + 5)² = x² + 10x + 25 = 64</text>
<polygon points="470,40 680,40 680,100 470,100" fill="#C4A15A"/>
<polygon points="470,110 620,110 620,160 470,160" fill="#8F9A72"/>
<polygon points="470,170 530,170 530,210 470,210" fill="#9A9488"/>
<text x="490" y="78" fill="#1C1A16" font-size="14">enfermedad 72</text>
<text x="490" y="142" fill="#1C1A16" font-size="14">heridas 18</text>
<text x="490" y="196" fill="#1C1A16" font-size="13">otras 10</text>
<text x="470" y="240" fill="#9A9488" font-size="12">esquema didáctico, no cifra de archivo</text>
'''
build(
37, 'Inclusión e historia de las <em>matemáticas</em>', 'F.3 Comunicación y aportación histórica',
'El razonamiento viaja; el acceso, no siempre',
'Al-Juarismi completa el cuadrado de x² + 10x = 39 y obtiene x = 3 con una figura, no con una cita. Sophie Germain demuestra que 29 y 59 son primos escribiendo bajo un nombre que la escuela le exigía. El esquema de la derecha recuerda de qué iba el argumento de Nightingale: mirar qué muertes pesaban más.',
['Completar el cuadrado en un caso numérico y comprobar la raíz en la ecuación original.',
 'Verificar un primo de Germain comprobando divisores, y nombrar la barrera de acceso junto al teorema.',
 'Comparar partes de un recuento antes de decidir una intervención, como en el argumento sanitario del esquema.'],
'''<h2>Una idea se estudia cuando se puede rehacer</h2>
<p>La aportación histórica, en este curso, no es una lámina de nombres. Es un razonamiento que todavía se puede ejecutar, más la pregunta de quién pudo firmarlo, estudiarlo o ser creído. Inclusión es decir las dos cosas: la cuenta y la puerta que estaba cerrada.</p>
<p><span class="glosa">completar el cuadrado = sumar el cuadrado de la mitad del coeficiente de x · Al-Juarismi, Bagdad, siglo IX, da nombre a la palabra algoritmo · primo de Germain = p primo tal que 2p + 1 también es primo · el esquema de barras no es un dato de archivo: imita la estructura del argumento de Florence Nightingale, no una cita literal</span></p>
<p>En el cuadrado de la izquierda el lado desconocido es x y la franja añadida mide 5, la mitad de 10. El cuadrado grande mide (x + 5)². Como x² + 10x vale 39, al sumar la esquina 25 se obtiene 64, que es 8². De ahí x + 5 = 8 y x = 3, en la tradición de soluciones positivas con la que él trabajaba. La comprobación no es la biografía: 9 + 30 = 39.</p>
<p>Germain, ya en el París de entresiglos, no podía entrar en la École Polytechnique. Estudió y escribió como M. Le Blanc. Eso no es una anécdota de carácter: es una condición de acceso. El teorema que lleva su nombre se puede comprobar con divisores, y se dice con su nombre. Nightingale, por su parte, tuvo que volver visible un recuento para que la administración mirara las infecciones y no solo las heridas. El esquema de la derecha, con 72, 18 y 10 sobre 100 muertes de aula, es didáctico: sirve para rehacer la comparación, y no hay que presentarlo como si fuera una tabla transcrita del hospital de Escútari.</p>''',
'Completar el cuadrado de x² + 10x: franjas 5x y esquina 25. A la derecha, esquema 72, 18 y 10', fig37,
[
('Completar x² + 10x = 39',
 'Resuelve x² + 10x = 39 completando el cuadrado, como en la figura, y comprueba la solución en la ecuación.',
 [
  ('La mitad del coeficiente de x es 5, y 5² = 25. Se suma 25 a los dos lados: x² + 10x + 25 = 39 + 25.',
   'Glosa: la esquina de la figura es ese 25. Sin ella el lado no es x + 5 en los dos sentidos.'),
  ('El miembro izquierdo es (x + 5)² y el derecho es 64. Entonces x + 5 = 8, tomando la raíz positiva que encaja con el cuadrado dibujado.',
   'Glosa: 8² = 64. La raíz negativa, −8, daría x = −13, que este texto geométrico del siglo IX no buscaba.'),
  ('x = 8 − 5 = 3. Es la longitud que hace coherente la figura: el cuadrado interior de lado 3 y las franjas de anchura 5.',
   'Glosa: (x + 5) vale 8, que es el lado del cuadrado grande cuya área es 64.'),
  ('Comprobación en la ecuación, no en la biografía: 3² + 10·3 = 9 + 30 = 39. La identidad cierra.',
   'Glosa: si la comprobación fallara, el error estaría en la mitad del coeficiente o en la raíz, y se podría localizar.'),
 ]),
('29 es primo de Germain',
 'Comprueba que 29 es primo y que 2·29 + 1 = 59 también lo es. Di qué barrera de acceso no queda demostrada con esa cuenta.',
 [
  ('29 es primo si no lo dividen los primos hasta √29 ≈ 5,4, o sea 2, 3 y 5. 29 es impar, 2+9 = 11 no es múltiplo de 3, y no acaba en 0 ni en 5.',
   'Glosa: basta llegar a la raíz. Probar divisores hasta 28 es correcto y es trabajo de más.'),
  ('2·29 + 1 = 59. √59 ≈ 7,7, así que se prueba hasta 7: impar, 5+9 = 14 no es múltiplo de 3, no acaba en 5, y 59/7 ≈ 8,4 no es entero.',
   'Glosa: 7·8 = 56, luego 59 − 56 = 3. No es múltiplo de 7.'),
  ('Los dos son primos, así que 29 es un primo de Germain. La cuenta es el contenido matemático y se puede rehacer sin la biografía.',
   'Glosa: el nombre del concepto recuerda a quien lo trabajó. La definición es la pareja de primos.'),
  ('La cuenta no demuestra que pudiera matricularse. La École Polytechnique no admitía mujeres y ella correspondió como M. Le Blanc. Nombrar el pseudónimo es parte de la historia del resultado, no un adorno.',
   'Glosa: inclusión es no separar el teorema de la puerta cerrada que condicionó cómo se firmó.'),
 ]),
('Dónde pesar la intervención',
 'En el esquema didáctico de la derecha, de cada 100 muertes 72 son por enfermedad, 18 por heridas y 10 por otras causas. ¿Qué parte es la mayor y qué error sería atender solo la más llamativa?',
 [
  ('72 + 18 + 10 = 100. Las tres barras agotan el esquema. La mayor es la enfermedad: 72/100 = 0,72.',
   'Glosa: 72 es el cuádruple de 18, porque 18·4 = 72. La barra ámbar es cuatro veces la verde en este dibujo.'),
  ('Atender solo las heridas, que son el relato más visible del combate, dejaría sin tocar 72 de cada 100 muertes del esquema.',
   'Glosa: la parte llamativa no es la parte grande. Hay que comparar antes de elegir.'),
  ('Nightingale usó diagramas para que esa comparación se viera. Este gráfico no reproduce sus cifras de archivo: imita la estructura del argumento, enfermedad frente a herida.',
   'Glosa: no se cita un 72 como si estuviera en el parte de Escútari. Se dice que es un esquema de aula.'),
  ('La decisión, dentro del esquema, pone los recursos en la causa de mayor peso. Comunicar la matemática incluye elegir la comparación que la administración no quería mirar.',
   'Glosa: el diagrama es un acto de comunicación, no una decoración de un texto que ya hubiera convencido.'),
 ]),
],
[
(1, 'Otro cuadrado',
 'Resuelve x² + 6x = 40 completando el cuadrado. Comprueba la solución positiva.',
 'El paso es sumar el cuadrado de la mitad de 6, no el cuadrado de 6. La mitad es 3 y 3² = 9, así que x² + 6x + 9 = 40 + 9 = 49. Entonces (x + 3)² = 49 y x + 3 = 7, luego x = 4. Comprobación: 16 + 6·4 = 16 + 24 = 40. Si se hubiera sumado 36, el miembro izquierdo no sería un cuadrado perfecto de (x + 3) y la raíz no correspondería a la ecuación. El mismo dibujo de la lección sirve, con franjas de anchura 3 y esquina 9 en vez de 5 y 25. La raíz negativa de 49 daría x = −10, que también satisface el álgebra moderna y que el método geométrico positivo de Al-Juarismi no estaba buscando.',
 'e37a'),
(2, '¿Y el 4? ¿Y el 3?',
 'Di si 4 es un primo de Germain. Después comprueba el caso p = 3.',
 'El paso es exigir las dos cosas: que p sea primo y que 2p + 1 lo sea. 4 no es primo, porque 4 = 2·2, así que ya no puede ser un primo de Germain; además 2·4 + 1 = 9 = 3·3, tampoco primo. Con p = 3: 3 es primo y 2·3 + 1 = 7, que es primo (no lo dividen 2 ni 3). Luego 3 sí es un primo de Germain. No basta con que 2p + 1 salga primo si p no lo es, ni al revés. La definición es una pareja. Comprobarla es el mismo trabajo de divisores que con 29 y 59, en pequeño, y se puede hacer entero en el cuaderno sin apelar a la autoridad del nombre.',
 'e37b'),
(3, 'No cites: compara',
 'Usando solo el esquema 72, 18 y 10, escribe el razonamiento por el que una medida centrada en las heridas deja fuera a la mayoría, sin atribuir el 72 a un archivo.',
 'El paso es comparar las tres partes del propio esquema y decir que es un esquema. Enfermedad 72, heridas 18, otras 10, suma 100. Una medida que solo alcance a las heridas se dirige a 18 de cada 100 muertes dibujadas y deja fuera las 72 de enfermedad, que son la mayoría y el cuádruple. Eso es el razonamiento. Lo que no se puede añadir es «Nightingale midió exactamente 72»: esta lección no ha mostrado ese parte, ha mostrado la estructura de su idea, que las causas no visibles pueden pesar más que las llamativas y que un diagrama obliga a mirarlas. Citar una cifra no hecha es peor comunicación científica que rehacer la comparación con datos declarados como de aula.',
 'e37c'),
],
[
('¿Qué número se suma al completar x² + 10x = 39 y qué solución positiva sale?',
 'Se suma 25, el cuadrado de 5, y sale x = 3. Por qué: (x + 5)² = 39 + 25 = 64, así que x + 5 = 8 y x = 3. La comprobación es 9 + 30 = 39. La esquina de la figura es precisamente ese 25; sin ella el lado grande no cuadra.'),
('¿Qué hay que comprobar para decir que 29 es primo de Germain, además de la biografía?',
 'Que 29 es primo y que 59 = 2·29 + 1 también lo es, mirando divisores hasta la raíz. Por qué: la definición es esa pareja, no el relato. El relato añade otra cosa que la cuenta no demuestra: que la École Polytechnique no la admitía y que publicó como M. Le Blanc. Las dos frases hacen falta y no se sustituyen.'),
('En el esquema de 100 muertes, ¿por qué no se atiende primero la causa más llamativa?',
 'Porque las heridas son 18 y la enfermedad es 72. Por qué: 72 es la mayor parte y el cuádruple de 18. El esquema es didáctico, no un parte de archivo, y aun así el razonamiento se puede rehacer: una medida solo sobre las heridas deja fuera a la mayoría dibujada. Comparar precede a elegir.'),
],
'La figura se puede rehacer',
'En el lienzo dibuja el cuadrado de x² + 6x = 40 con su esquina de 9, escribe x = 4 y, al lado, una frase que diga qué puerta se le cerró a Germain sin reducirla a una anécdota.',
['El cuadrado grande completa x² + 10x con la esquina 25 y el área pasa de 39 a 64.',
 'De 64 sale lado 8, y x = 3. La comprobación 9 + 30 = 39 cierra.',
 'Ejemplo 1: la mitad de 10 es 5. No se suma 10².',
 'Ejemplo 2: 29 y 59 son primos. El pseudónimo nombra una exclusión, no un capricho.',
 'Ejemplo 3: en el esquema, 72 frente a 18. No es una cita de archivo.',
 'Rehacer el razonamiento es la forma de estudiarlo. Copiar el nombre no lo es.',
 'Inclusión es contar la idea y contar la puerta.'],
)

print('L37 escrito')

# ---------- L38 un solo problema, de la inscripción al pasillo y a la lluvia ----------
fig38 = '''
<line x1="30" y1="200" x2="300" y2="200" stroke="#9A9488" stroke-width="1.5"/>
<polygon points="40,200 100,200 100,20 40,20" fill="#C4A15A" stroke="#E6E1D6" stroke-width="1"/>
<polygon points="120,200 180,200 180,65 120,65" fill="#8F9A72" stroke="#E6E1D6" stroke-width="1"/>
<polygon points="200,200 260,200 260,155 200,155" fill="#E6E1D6" stroke="#C4A15A" stroke-width="1"/>
<text x="70" y="16" text-anchor="middle" fill="#C4A15A" font-size="12">960</text>
<text x="150" y="58" text-anchor="middle" fill="#E6E1D6" font-size="12">720</text>
<text x="230" y="148" text-anchor="middle" fill="#1C1A16" font-size="12">240</text>
<text x="70" y="218" text-anchor="middle" fill="#9A9488" font-size="12">ingreso</text>
<text x="150" y="218" text-anchor="middle" fill="#9A9488" font-size="12">coste</text>
<text x="230" y="218" text-anchor="middle" fill="#9A9488" font-size="12">beneficio</text>
<circle cx="430" cy="50" r="16" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<circle cx="620" cy="50" r="16" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<circle cx="430" cy="190" r="16" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<circle cx="620" cy="190" r="16" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<line x1="446" y1="50" x2="604" y2="50" stroke="#C4A15A" stroke-width="2"/>
<line x1="430" y1="66" x2="430" y2="174" stroke="#C4A15A" stroke-width="2"/>
<line x1="620" y1="66" x2="620" y2="174" stroke="#C4A15A" stroke-width="2"/>
<line x1="444" y1="62" x2="606" y2="178" stroke="#8F9A72" stroke-width="2"/>
<line x1="444" y1="178" x2="606" y2="62" stroke="#8F9A72" stroke-width="2"/>
<line x1="446" y1="190" x2="604" y2="190" stroke="#C4A15A" stroke-width="2"/>
<text x="430" y="55" text-anchor="middle" fill="#E6E1D6" font-size="14">A</text>
<text x="620" y="55" text-anchor="middle" fill="#E6E1D6" font-size="14">B</text>
<text x="430" y="195" text-anchor="middle" fill="#E6E1D6" font-size="14">C</text>
<text x="620" y="195" text-anchor="middle" fill="#E6E1D6" font-size="14">D</text>
<text x="400" y="24" fill="#C4A15A" font-size="13">4 talleres, las 6 parejas</text>
<text x="30" y="250" fill="#E6E1D6" font-size="14">80 inscritos · 12 € · coste 400 + 4·80 = 720 · beneficio 240</text>
<text x="30" y="278" fill="#9A9488" font-size="13">el mismo problema sigue en el pasillo y en la lluvia: no son tres enunciados sueltos</text>
'''
build(
38, 'Proyecto integrador de <em>cierre</em>', 'A–F Un problema con varios bloques del curso',
'De la inscripción al pasillo, sin cambiar de historia',
'Un solo caso: el IES de Soria abre las puertas. Hay 80 alumnos inscritos, cuatro talleres y cada alumno elige dos. La entrada son 12 euros, el alquiler 400 y el material 4 euros por persona. Los tres ejemplos recorren esa misma jornada: primero el dinero y el conteo, después el plano y la función de beneficio, al final la lluvia y la asistencia.',
['Modelar el beneficio de la jornada como función afín y localizar el umbral de asistencia.',
 'Leer el plano de pasillos como grafo ponderado y elegir el camino mínimo con las duraciones sumadas.',
 'Incorporar la probabilidad de lluvia y la asistencia esperada sin confundir la media con el peor caso.'],
'''<h2>Una jornada, tres herramientas</h2>
<p>El cierre no abre tres problemas pequeños. Abre uno y no lo suelta. El instituto tiene 80 alumnos inscritos en la jornada de puertas abiertas. Hay cuatro talleres, A, B, C y D. Cada alumno elige dos, sin que el orden importe. La entrada cuesta 12 euros. El alquiler de la mañana son 400 euros, se paguen o no se llenen las salas, y el material son 4 euros por alumno que asiste. En el edificio, la entrada E comunica con el hall H en 3 minutos, el hall con los talleres T en 5 y con el salón S en 7, los talleres con el salón en 4, y hay un patio directo de E a T de 9 minutos. La previsión de lluvia es 1/4. En jornadas anteriores ha asistido el 90 % de quienes se inscribieron.</p>
<p><span class="glosa">itinerarios = C(4, 2) = 6 · ingreso I(x) = 12x · coste C(x) = 400 + 4x · beneficio B(x) = 8x − 400 · umbral: B(x) = 0 cuando x = 50 · camino mínimo E–H–S = 10 min · asistencia esperada = 0,90 · 80 = 72 · B(72) = 176</span></p>
<p>Con los 80 inscritos, si vienen todos, el ingreso es 960 euros y el coste 720, así que el beneficio es 240. La función B(x) = 8x − 400 dice que cada persona de más, por encima del alquiler ya pagado, aporta 8 euros: los 12 de la entrada menos los 4 del material. Hacen falta 50 asistentes para no perder dinero. El grafo no cambia esas cifras: cambia cuánto se tarda en ir de la puerta al salón, y la lluvia no cambia el alquiler: cambia cuánta gente cabe y cuánta se espera.</p>
<p>Nada de esto pide un bloque nuevo. Pide no abandonar los números al cambiar de herramienta. El conteo de parejas, la recta del beneficio, la arista del pasillo y el 0,25 de lluvia hablan de la misma mañana. Si un resultado intermedio no se reutiliza en el ejemplo siguiente, se ha roto el proyecto.</p>
<table class="datos"><thead><tr><th>Pieza</th><th>Cifra de la jornada</th><th>Bloque</th></tr></thead>
<tbody>
<tr><td>Parejas de talleres</td><td>C(4, 2) = 6</td><td>conteo</td></tr>
<tr><td>Beneficio si vienen 80</td><td>240 €</td><td>finanzas y función afín</td></tr>
<tr><td>Puerta al salón</td><td>10 min</td><td>grafos</td></tr>
<tr><td>Asistencia esperada</td><td>72 personas, beneficio 176 €</td><td>probabilidad</td></tr>
</tbody></table>''',
'Barras 960, 720 y 240 de la jornada, y los cuatro talleres con las seis parejas posibles', fig38,
[
('Dinero y parejas de la misma lista',
 'Con 80 inscritos que vienen todos, cuatro talleres y entrada de 12 euros, halla el beneficio y el número de parejas de talleres. Deja escrita B(x).',
 [
  ('Parejas: C(4, 2) = 4·3/2 = 6. Son AB, AC, AD, BC, BD y CD, las seis aristas del grafo de la derecha. El orden no crea un itinerario nuevo.',
   'Glosa: si el orden importara serían 4·3 = 12. El enunciado dice que no importa.'),
  ('Ingreso: 80 · 12 = 960 euros. Coste: 400 + 80 · 4 = 400 + 320 = 720. Beneficio: 960 − 720 = 240 euros. Son las tres barras.',
   'Glosa: el 400 no se multiplica por 80. Es alquiler fijo de la mañana.'),
  ('En función del número que asiste, I(x) = 12x y C(x) = 400 + 4x, luego B(x) = 8x − 400. Con x = 80, 640 − 400 = 240, la misma barra.',
   'Glosa: 12 − 4 = 8 es lo que aporta cada asistente una vez pagado el alquiler.'),
  ('Umbral: 8x − 400 = 0 da x = 50. Por debajo se pierde dinero aunque la entrada sea de 12 euros, porque el alquiler no se encoge.',
   'Glosa: 8 · 50 = 400. Faltan 30 personas respecto de los 80 inscritos para estar justo en cero, no para el beneficio 240.'),
 ]),
('El plano no cambia el beneficio; cambia el minuto',
 'En el mismo edificio, ¿cuánto se tarda de la entrada E al salón S? Usa los pesos 3, 5, 7, 4 y 9, y relaciona la pendiente de B con los 8 euros.',
 [
  ('Tres caminos: E–H–S = 3 + 7 = 10; E–H–T–S = 3 + 5 + 4 = 12; E–T–S = 9 + 4 = 13. El mínimo es 10 minutos, por el hall.',
   'Glosa: se suman minutos de aristas, no se cuenta el número de pasillos. El camino de tres tramos dura más que el de dos.'),
  ('La matriz de pesos, con orden E, H, T, S, guarda los mismos números: la casilla H–S es 7, la E–T es 9 y no hay casilla directa E–S. El plano y la matriz son el mismo grafo.',
   'Glosa: un hueco en la matriz no es un cero de minutos. Es una arista que no existe.'),
  ('Nada de esto modifica los 240 euros. El beneficio depende de cuánta gente entra, no de si tarda 10 o 13 minutos, salvo que el retraso vaciara la sala, cosa que el enunciado no dice.',
   'Glosa: cambiar de bloque no es permiso para tirar la cifra anterior. Aquí simplemente no se usa.'),
  ('La pendiente de B es 8 euros por persona: es constante, como la derivada de una afín. Una persona más, si ya se ha superado el alquiler, no cambia el 400 y sí suma 8.',
   'Glosa: B(51) − B(50) = 8. Ese incremento es la pendiente, no un beneficio nuevo calculado desde cero.'),
 ]),
('Lluvia y asistencia, sobre el mismo B(x)',
 'Asiste, en media, el 90 % de los 80. La lluvia tiene probabilidad 1/4. Si llueve, 20 alumnos de huerto exterior pasan a un salón donde ya hay 40 y solo caben 50. Calcula el beneficio esperado y el peor caso de asientos.',
 [
  ('Asistencia esperada: 0,90 · 80 = 72 personas. No son los 80 de la barra, ni un sorteo que haya que simular para obtener la media.',
   'Glosa: 10 % de 80 son 8 ausencias. 80 − 8 = 72.'),
  ('Beneficio con esa media: B(72) = 8 · 72 − 400 = 576 − 400 = 176 euros. Son 64 euros menos que 240, y 64 = 8 · 8: las ocho ausencias valen ocho euros cada una.',
   'Glosa: se reutiliza B(x). No se reconstruye el alquiler desde el principio, aunque hacerlo daría lo mismo: 12·72 − (400 + 4·72) = 864 − 688 = 176.'),
  ('Si llueve, que ocurre con probabilidad 1/4, el salón recibe 40 + 20 = 60 personas y caben 50. Faltan 10 asientos. Si no llueve, el huerto no se mueve y esos 10 no faltan.',
   'Glosa: 60 − 50 = 10. El déficit es condicional a la lluvia, no un hecho seguro.'),
  ('La media de asistentes, 72, no evita el peor caso de la sala. 176 euros es una esperanza de beneficio, no una promesa, y los 10 asientos faltan precisamente cuando llueve, aunque la asistencia media quepa en otras cuentas.',
   'Glosa: esperanza y peor caso responden a preguntas distintas. El proyecto las deja escritas las dos.'),
 ]),
],
[
(1, 'Vienen 60, no 80',
 'En la misma jornada, asisten 60 personas. Calcula el beneficio con B(x) = 8x − 400 y comprueba rehaciendo ingreso y coste. No cambies el alquiler.',
 'El paso es evaluar la función ya obtenida, y usar la cuenta larga solo como comprobación, sin olvidar el fijo. B(60) = 8·60 − 400 = 480 − 400 = 80 euros. Por la definición: ingreso 12·60 = 720, coste 400 + 4·60 = 640, beneficio 720 − 640 = 80. Si alguien resta solo el material, 720 − 240 = 480, ha perdido el alquiler y presenta como beneficio un número que todavía debe 400 euros. El umbral seguía en 50: con 60 se está 10 personas por encima, y 10·8 = 80 cierra otra vez. Es la misma jornada; solo ha cambiado x.',
 'e38a'),
(2, 'Cierran el patio',
 'El patio E–T de 9 minutos está cerrado. ¿Cuál es ahora el camino mínimo de E a S con los pesos que quedan? No uses el beneficio para contestar minutos.',
 'El paso es tachar la arista que ya no existe y volver a sumar los caminos que quedan, no quedarse con el 13 que usaba el patio ni con el 10 sin mirar. Sin E–T desaparece el camino E–T–S de 13 minutos. Siguen E–H–S = 3 + 7 = 10 y E–H–T–S = 3 + 5 + 4 = 12. El mínimo continúa siendo 10, por el hall: cerrar el patio elimina un camino que ya era peor, no el mejor. Contar aristas en vez de minutos habría preferido cualquier camino de dos tramos sin sumar 3 y 7. El beneficio de 240 euros no entra en la respuesta: la pregunta es de tiempo. Mezclar las unidades es romper el proyecto, no enriquecerlo.',
 'e38b'),
(3, 'Llueve más a menudo',
 'La probabilidad de lluvia pasa a 0,40 y siguen siendo 20 los del huerto. ¿Cuántos alumnos de huerto se espera que acaben en el salón? ¿Por qué esa esperanza no garantiza que quepan los 50 asientos el día que llueve?',
 'El paso es multiplicar la probabilidad por los 20, y no usar ese producto como si fuera el aforo del día de lluvia. Esperanza de desplazados: 0,40 · 20 = 8. Sumados a los 40 de la charla dan 48, que en media caben en 50. El día que sí llueve, sin embargo, no se desplazan 8: se desplazan los 20, y 40 + 20 = 60, diez asientos por encima del aforo. La esperanza promedia los días de lluvia y los despejados; el aforo se sufre en un día concreto. Confundir 8 con 20 es tratar la media como si fuera el suceso condicionado. La probabilidad 0,40 cambia la previsión media respecto del 0,25 del ejemplo y no cambia la aritmética del peor caso, que sigue siendo 60 frente a 50.',
 'e38c'),
],
[
('Si vienen los 80, ¿cuánto beneficio queda y cuántas parejas de talleres hay?',
 'Beneficio 240 euros y 6 parejas. Por qué: ingreso 80·12 = 960, coste 400 + 320 = 720, diferencia 240. Las parejas son C(4, 2) = 6, las aristas del dibujo. El beneficio también es B(80) = 8·80 − 400 = 240. El alquiler no se multiplica por el número de talleres.'),
('¿Cuál es el camino mínimo de la entrada al salón y por qué no es el de tres tramos?',
 '10 minutos, E–H–S. Por qué: 3 + 7 = 10, mientras E–H–T–S suma 12 y E–T–S suma 13. Se suman los minutos de las aristas. El camino con más pasillos no es el más corto. No hay puerta directa de E a S: esa casilla no está en la matriz.'),
('Con un 90 % de asistencia, ¿qué beneficio se espera y qué no dice esa cifra sobre los asientos si llueve?',
 'Se esperan 72 personas y B(72) = 176 euros. Por qué: 0,90·80 = 72 y 8·72 − 400 = 176, sesenta y cuatro euros menos que si vinieran todos, justo 8 euros por cada una de las 8 ausencias. Si llueve, el salón junta 40 + 20 = 60 y caben 50: faltan 10 asientos. La esperanza no es el peor caso.'),
],
'La misma mañana, en el lienzo',
'Dibuja las tres barras 960, 720 y 240, el camino E–H–S de 10 minutos y escribe B(72) = 176. Tiene que reconocerse una sola jornada.',
['Una sola historia: 80 inscritos, cuatro talleres, 12 euros, alquiler 400 y material 4.',
 'Las barras son 960, 720 y 240. Las seis líneas de la derecha son las parejas de talleres.',
 'Ejemplo 1: B(x) = 8x − 400 y el umbral está en 50 asistentes.',
 'Ejemplo 2: el salón se alcanza en 10 minutos por el hall. La pendiente del beneficio es 8 euros.',
 'Ejemplo 3: asistencia esperada 72, beneficio 176. Si llueve, faltan 10 asientos.',
 'Cada cifra se reutiliza. Cambiar de bloque no borra el anterior.',
 'Esperanza y peor caso se escriben los dos, porque no son la misma pregunta.'],
)

print('L38 escrito')

assert_untouched(SNAP)
print('PROTECT 01-14 intacto')
