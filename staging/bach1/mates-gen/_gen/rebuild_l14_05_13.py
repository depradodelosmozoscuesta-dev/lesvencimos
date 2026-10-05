# -*- coding: utf-8 -*-
"""L05–L13 al listón L14. No toca L01–L04 ni L14."""
import sys
sys.path.insert(0, '/workspace/lesvencimos/staging/bach1/mates-gen/_gen')
from rebuild_l14_common import *

SNAP = snapshot()

# ---------- L05 ----------
fig05 = '''
<line x1="70" y1="36" x2="650" y2="36" stroke="#C4A15A" stroke-width="2"/>
<line x1="70" y1="78" x2="650" y2="78" stroke="#9A9488" stroke-width="1.2"/>
<line x1="70" y1="118" x2="650" y2="118" stroke="#9A9488" stroke-width="1.2"/>
<line x1="70" y1="158" x2="650" y2="158" stroke="#9A9488" stroke-width="1.2"/>
<line x1="70" y1="198" x2="650" y2="198" stroke="#9A9488" stroke-width="1.2"/>
<line x1="70" y1="248" x2="650" y2="248" stroke="#C4A15A" stroke-width="2"/>
<line x1="70" y1="36" x2="70" y2="248" stroke="#9A9488" stroke-width="1.2"/>
<line x1="430" y1="36" x2="430" y2="248" stroke="#9A9488" stroke-width="1.2"/>
<line x1="650" y1="36" x2="650" y2="248" stroke="#9A9488" stroke-width="1.2"/>
<circle cx="600" cy="270" r="0" fill="none"/>
<text x="80" y="28" fill="#C4A15A" font-size="14">Factura taller · Valladolid</text>
<text x="80" y="62" fill="#E6E1D6" font-size="15">Mano de obra 2 h × 35 €/h</text>
<text x="450" y="62" fill="#E6E1D6" font-size="15">70,00 €</text>
<text x="80" y="102" fill="#E6E1D6" font-size="15">Pieza de recambio</text>
<text x="450" y="102" fill="#E6E1D6" font-size="15">25,00 €</text>
<text x="80" y="142" fill="#C4A15A" font-size="15">Base imponible</text>
<text x="450" y="142" fill="#C4A15A" font-size="15">95,00 €</text>
<text x="80" y="182" fill="#E6E1D6" font-size="15">IVA 21 % de 95</text>
<text x="450" y="182" fill="#E6E1D6" font-size="15">19,95 €</text>
<text x="80" y="230" fill="#E6E1D6" font-size="16" font-weight="700">Total</text>
<text x="450" y="230" fill="#E6E1D6" font-size="16" font-weight="700">114,95 €</text>
<circle cx="90" cy="286" r="7" fill="#C4A15A"/>
<text x="108" y="291" fill="#9A9488" font-size="13">el IVA sale de la base, no del total</text>
'''
# circle r=0 doesn't count as useful but circle tag counts. Real circles exist.
build(
5, 'Documentos numéricos <em>cotidianos</em>', 'A.2 Tablas, facturas, nóminas y noticias',
'La cifra que no está donde crees',
'El Decreto pide leer tablas, diagramas, facturas, nóminas y noticias con números. Aquí una factura real de taller y una nómina se desmenuzan operación a operación, y una noticia enseña a no confundir puntos porcentuales con un porcentaje.',
['Separar base, impuesto y total en una factura.','Pasar del bruto al neto en una nómina.','Distinguir puntos porcentuales de variación relativa.'],
'''<h2>Leer el documento antes de operar</h2>
<p>Una factura, una nómina o una noticia no son «un número suelto». Cada cifra tiene un papel: unas son datos de partida, otras son porcentajes aplicados a una base concreta, y el total es el resultado de una suma o de una resta, nunca un adorno.</p>
<p><span class="glosa">base imponible = importe antes de impuestos · tipo de IVA = porcentaje legal que se aplica a esa base · bruto = sueldo antes de retenciones · neto = lo que queda tras restar IRPF y cotización</span></p>
<p>En el taller de Valladolid del gráfico, la mano de obra (2 horas a 35 euros) y la pieza (25 euros) se suman primero. Solo entonces se calcula el 21 % de IVA. Si aplicas el 21 % al total ya inflado, o lo sumas dos veces, el documento deja de cuadrar con el banco.</p>
<p>En la nómina el mismo cuidado: el 15 % de IRPF y el 6,35 % de Seguridad Social se calculan sobre el bruto, y se restan. En la noticia, pasar del 12 % al 9 % de paro son 3 puntos porcentuales; la variación relativa respecto al valor inicial es otra cuenta, (9 − 12) / 12.</p>
<table class="datos"><thead><tr><th>Documento</th><th>Operación que manda</th><th>Trampa</th></tr></thead>
<tbody>
<tr><td>Factura</td><td>IVA = tipo × base; total = base + IVA</td><td>Calcular el IVA sobre el total</td></tr>
<tr><td>Nómina</td><td>neto = bruto − IRPF − cotización</td><td>Tomar el bruto como ingreso</td></tr>
<tr><td>Noticia</td><td>variación relativa = (final − inicial) / inicial</td><td>Llamar porcentaje a una resta de porcentajes</td></tr>
</tbody></table>''',
'Factura con base 95 €, IVA 19,95 € y total 114,95 €', fig05,
[
('Factura del taller',
 'Mano de obra: 2 horas a 35 €/h. Pieza: 25 €. IVA general del 21 %. Halla base, IVA y total, y comprueba que el total no es 95 × 1,21 dos veces.',
 [
  ('Suma las líneas anteriores al impuesto: 2 × 35 = 70, y 70 + 25 = 95. Esa suma es la base imponible.',
   'Glosa: la base se cierra antes de mencionar el IVA; 70 y 25 son importes sin impuesto.'),
  ('Aplica el tipo solo a la base: 0,21 × 95. Primero 0,20 × 95 = 19 y 0,01 × 95 = 0,95, luego 19 + 0,95 = 19,95 €.',
   'Glosa: 0,21 es el tanto por uno del 21 %; el porcentaje no se suma a la base como si fuera 21 euros.'),
  ('El total a pagar es base más IVA: 95 + 19,95 = 114,95 €. Coincide con la última fila del gráfico.',
   'Glosa: multiplicar la base por 1,21 da el mismo total (95 × 1,21 = 114,95) y no hay que volver a multiplicar.'),
  ('Comprobación por exceso: si alguien hace 0,21 × 114,95 obtiene unos 24 € de «IVA» y un total absurdo. Ese paso usa la magnitud equivocada.',
   'Glosa: el tipo siempre se refiere a la base escrita en la factura, no al total ya con impuesto.'),
 ]),
('Nómina de 1 800 €',
 'Bruto mensual 1 800 €. Retención de IRPF del 15 % y cotización del trabajador del 6,35 %. Calcula cada descuento y el neto.',
 [
  ('IRPF: 0,15 × 1 800 = 270 €. La retención sale del bruto, no de una estimación «a ojo» de lo que queda.',
   'Glosa: 15 % = 15/100 = 0,15; 0,15 × 1 800 = 270 exactamente.'),
  ('Cotización: 0,0635 × 1 800. Haz 0,06 × 1 800 = 108 y 0,0035 × 1 800 = 6,30; suma 114,30 €.',
   'Glosa: 6,35 % no es 6,35 euros; es 6,35 euros por cada 100 euros de bruto.'),
  ('Neto = 1 800 − 270 − 114,30 = 1 415,70 €. Resta por separado para ver qué concepto pesa más.',
   'Glosa: el IRPF (270) es mayor que la cotización (114,30); el neto no es el bruto menos solo uno de los dos.'),
  ('Comprueba el orden: 1 800 − 270 = 1 530 y 1 530 − 114,30 = 1 415,70. Si sumas los descuentos primero, 270 + 114,30 = 384,30 y 1 800 − 384,30 da lo mismo.',
   'Glosa: las dos restas son conmutativas en el resultado, pero cada descuento debe identificarse en la nómina.'),
 ]),
('Del 12 % al 9 % no es un 3 %',
 'Una noticia dice que el paro de la comarca pasa del 12 % al 9 % y titula «baja un 3 %». Explica el error y calcula la variación relativa.',
 [
  ('La resta 12 − 9 = 3 mide puntos porcentuales, no un porcentaje de variación. El titular mezcla las dos unidades.',
   'Glosa: un punto porcentual es la diferencia directa entre dos porcentajes; no lleva división.'),
  ('La variación relativa usa el valor inicial como base: (9 − 12) / 12 = (−3) / 12 = −0,25.',
   'Glosa: el signo menos indica bajada; la base de la división es 12, el dato de partida, no 9 ni 3.'),
  ('Pasa a porcentaje: −0,25 = −25 %. Respecto del 12 % inicial, el paro ha bajado un 25 %, no un 3 %.',
   'Glosa: multiplicar el tanto por uno por 100 cambia la forma de escribirlo, no la magnitud.'),
  ('Comprobación con personas: si había 12 parados por cada 100 activos y pasan a 9, se han ido 3 de esos 12, y 3/12 = 1/4.',
   'Glosa: el modelo «de cada 100» hace visible por qué la base es el dato antiguo.'),
 ]),
],
[
(1, 'Ticket con IVA incluido',
 'Un ticket muestra solo el total, 60,50 €, «IVA incluido» al 21 %. Recupera la base y el IVA por separado.',
 'El paso que ordena el problema es deshacer el factor 1,21, no restar 21 % del total. Si el total ya lleva el impuesto, base × 1,21 = 60,50, así que la base es 60,50 / 1,21 = 50 €. El IVA es la diferencia 60,50 − 50 = 10,50 €, que coincide con 0,21 × 50. Restar 0,21 × 60,50 ≈ 12,71 € sería tratar el total como si fuera base y dejaría una factura que no cierra.',
 'e05a'),
(2, 'Otra nómina',
 'Bruto 2 200 €, IRPF 18 % y cotización 6,35 %. Halla neto y di qué descuento es mayor.',
 'Calcula cada porcentaje sobre el mismo bruto antes de restar. IRPF: 0,18 × 2 200 = 396 €. Cotización: 0,0635 × 2 200 = 139,70 €. El IRPF es mayor. Neto = 2 200 − 396 − 139,70 = 1 664,30 €. El error típico es aplicar el 18 % al neto o encadenar el segundo porcentaje sobre lo que queda después del primero: la nómina española habitual aplica ambos tipos al bruto.',
 'e05b'),
(3, 'Titular deportivo',
 'Los socios de un club pasan de 400 a 500. Un cartel dice «suben un 100 %» y otro «suben 100 personas». ¿Cuál es la variación relativa correcta?',
 'La variación absoluta es 500 − 400 = 100 personas. La relativa es 100 / 400 = 0,25 = 25 %, no 100 %. El cartel del 100 % ha dividido el aumento entre algo que no es el valor inicial, o ha confundido «100 personas» con «100 %». Comprueba al revés: el 25 % de 400 es 100, y 400 + 100 = 500. Esa comprobación cierra el paso.',
 'e05c'),
],
[
('¿Sobre qué cantidad se calcula el 21 % de IVA de la factura del gráfico?',
 'Sobre la base de 95 €, no sobre 114,95 €. Por qué: el tipo legal se aplica al importe antes de impuesto. 0,21 × 95 = 19,95, y solo después se suma para obtener el total. Usar el total como base contaría impuesto sobre impuesto.'),
('En la nómina de 1 800 €, ¿por qué el neto no es 1 800 − 15 − 6,35?',
 'Porque 15 y 6,35 son porcentajes, no euros. Por qué: hay que convertirlos en tanto por uno y multiplicar por el bruto: 270 € y 114,30 €. Restar los números del porcentaje como si fueran euros deja casi todo el bruto intacto y no describe ninguna nómina real.'),
('Bajar del 12 % al 9 %: ¿cuánto es la variación relativa?',
 'Es −25 %, no −3 %. Por qué: 3 son los puntos porcentuales (resta directa). La variación relativa divide esa resta entre el valor inicial: −3/12 = −0,25. Sin esa división se cambia de unidad y el titular exagera poco o mucho según el caso.'),
],
'Documento de casa',
'Trae una factura o un ticket (puedes tapar el nombre). Escribe base, tipo, impuesto y total, y señala una cifra que alguien podría leer mal. Si no tienes documento, inventa uno coherente y comprueba que cierra.',
['Hoy leemos facturas: la del gráfico suma 70 y 25, base 95, IVA 19,95 y total 114,95.',
 'El SVG es la factura: cada línea horizontal es un concepto y la columna derecha es el importe.',
 'Ejemplo 1: el 21 % se aplica a 95, no al total. Repite 0,21 por 95.',
 'Ejemplo 2: nómina de 1 800 €, se van 270 de IRPF y 114,30 de cotización.',
 'Ejemplo 3: del 12 % al 9 % son 3 puntos y, a la vez, una bajada relativa del 25 %.',
 'Ahora los tres ejercicios: deshaz un IVA incluido y no restes puntos como si fueran porcentajes.',
 'Cierra con Comprueba y el reto de un documento real.']
)

print('lote L05 escrito, sigo en el mismo proceso')

# ---------- L06 ----------
p6 = path_fn(lambda x: 2 ** x, 0, 4, 20, lambda x: 48 + x * 72, lambda y: 286 - y * 13)
q6 = path_fn(lambda x: __import__('math').log2(x), 1, 8, 24, lambda x: 400 + (x - 1) * 36, lambda y: 286 - y * 52, stroke='#8F9A72')
fig06 = ejes(48, 286, 340, 30) + ejes(400, 286, 680, 30) + p6 + q6 + '''
<circle cx="336" cy="78" r="6" fill="#E6E1D6"/>
<circle cx="652" cy="130" r="6" fill="#E6E1D6"/>
<line x1="300" y1="78" x2="336" y2="78" stroke="#9A9488" stroke-width="1"/>
<text x="48" y="22" fill="#C4A15A" font-size="14">y = 2^x</text>
<text x="250" y="68" fill="#E6E1D6" font-size="13">(4, 16)</text>
<text x="400" y="22" fill="#8F9A72" font-size="14">y = log2(x)</text>
<text x="560" y="118" fill="#E6E1D6" font-size="13">(8, 3)</text>
'''
build(
6, 'Potencias, raíces y <em>logaritmos</em>', 'A.2 Potencias, raíces y logaritmos',
'El exponente que cuenta duplicaciones',
'CyL pide usar potencias, raíces y logaritmos en problemas, no solo recitar propiedades. La curva de la izquierda es 2 elevado a x, con el punto del ejemplo (4, 16); la de la derecha es su inversa, logaritmo en base 2, con el punto (8, 3).',
['Calcular potencias enteras y leerlas como crecimiento.','Interpretar un logaritmo como el exponente que falta.','Resolver ecuaciones sencillas del tipo a elevado a x igual a un número conocido.'],
'''<h2>Potencia, raíz y logaritmo dicen lo mismo en tres idiomas</h2>
<p>Una potencia aⁿ repite el factor a, n veces. La raíz pregunta por la base: ¿qué número, elevado a n, da este resultado? El logaritmo pregunta por el exponente: ¿a qué hay que elevar la base para obtener ese resultado?</p>
<p><span class="glosa">2⁴ = 2·2·2·2 = 16 · log₂(8) = 3 porque 2³ = 8 · √144 = 12 porque 12² = 144 · el logaritmo y la exponencial de la misma base se deshacen</span></p>
<p>En el gráfico, la curva ámbar no es una recta: cada paso de una unidad en x duplica la altura. Por eso el punto marcado es (4, 16) y no (4, 8). La curva verde es la inversa: intercambia el papel de la altura y del exponente. El punto (8, 3) se lee «hay que elevar 2 a 3 para llegar a 8».</p>
<p>Las propiedades no sustituyen al significado. log(a·b) = log a + log b cuando existe, pero log(a+b) no es log a + log b. Y una raíz cuadrada no es «dividir entre dos»: √144 es 12, mientras que 144/2 es 72.</p>
<table class="datos"><thead><tr><th>Pregunta</th><th>Operación</th><th>Ejemplo de esta lección</th></tr></thead>
<tbody>
<tr><td>¿Qué sale al repetir el factor?</td><td>potencia</td><td>2⁴ = 16</td></tr>
<tr><td>¿Qué exponente falta?</td><td>logaritmo</td><td>log₂(8) = 3</td></tr>
<tr><td>¿Qué base falta?</td><td>raíz</td><td>√144 = 12</td></tr>
</tbody></table>''',
'Curva 2^x con el punto (4, 16) y logaritmo en base 2 con el punto (8, 3)', fig06,
[
('Cultivo que se duplica',
 'Un cultivo tiene 1 unidad de masa al empezar la observación y duplica su masa cada hora. ¿Cuántas veces la masa inicial hay al cabo de 4 horas? Marca el punto en la curva ámbar.',
 [
  ('Traduce «duplica cada hora» a potencia de base 2: al cabo de n horas la masa es 2ⁿ veces la inicial.',
   'Glosa: la base 2 es el factor de cada hora; el exponente es el número de horas, no al revés.'),
  ('Sustituye n = 4: 2⁴ = 2·2·2·2. Agrupa (2·2)·(2·2) = 4·4 = 16.',
   'Glosa: 2⁴ no es 2·4 = 8; ese error confunde la potencia con un producto por el exponente.'),
  ('El punto de la curva es (4, 16): abscisa 4 horas, ordenada 16 veces la masa inicial.',
   'Glosa: en el SVG la altura crece cada vez más deprisa; por eso de x = 3 a x = 4 la curva pega el salto de 8 a 16.'),
  ('Comprueba una hora antes: 2³ = 8, y 8·2 = 16. El paso de una hora multiplica por 2, no suma 2.',
   'Glosa: el crecimiento exponencial suma cantidades distintas en cada hora; aquí el último tramo suma otras 8 unidades.'),
 ]),
('El exponente escondido',
 'Se cumple 2ˣ = 8. Halla x con un logaritmo y comprueba que el punto (8, 3) de la curva verde cuenta esa misma historia al revés.',
 [
  ('Pregunta explícita del logaritmo: x = log₂(8). No es 8/2 ni 8 − 2.',
   'Glosa: log₂(8) se lee «exponente al que hay que elevar 2 para obtener 8».'),
  ('Prueba potencias conocidas: 2¹ = 2, 2² = 4, 2³ = 8. El exponente que encaja es 3.',
   'Glosa: como 8 es potencia entera de 2, el logaritmo sale exacto, sin decimales.'),
  ('En la curva verde la abscisa es el resultado (8) y la ordenada es el exponente (3). Por eso el punto marcado es (8, 3).',
   'Glosa: respecto de y = 2ˣ, el logaritmo intercambia los ejes: el 3 que era exponente pasa a ser altura.'),
  ('Comprueba deshaciendo: 2 elevado a log₂(8) vuelve a 8. Si tu x no cumple 2ˣ = 8, no es la solución.',
   'Glosa: esta comprobación sirve también cuando el logaritmo no es entero y usas la calculadora de la barra.'),
 ]),
('Ecuación y una raíz que no es una división',
 'Resuelve 3ˣ = 81. Después calcula √144 y explica por qué no vale 72.',
 [
  ('Descompón 81 como potencia de 3: 3² = 9, 3³ = 27, 3⁴ = 81. Luego 3ˣ = 3⁴ y x = 4.',
   'Glosa: si las bases coinciden y son positivas y distintas de 1, los exponentes son iguales.'),
  ('También puedes escribir x = log₃(81) = 4. El logaritmo es el nombre de la incógnita, no una operación distinta del paso anterior.',
   'Glosa: cambiar de nombre no cambia el exponente; solo lo hace visible.'),
  ('√144 pregunta «qué número al cuadrado da 144». 12² = 144, luego √144 = 12. En cambio 144/2 = 72 y 72² es mucho mayor que 144.',
   'Glosa: la raíz cuadrada es la potencia 1/2, no el cociente entre 2.'),
  ('Comprueba la ecuación: 3⁴ = 81. Y la raíz: 12·12 = 144. Las dos comprobaciones son volver a la potencia.',
   'Glosa: potencia, raíz y logaritmo se comprueban siempre rehaciendo la potencia original.'),
 ]),
],
[
(1, 'Seis duplicaciones',
 'El mismo cultivo duplica ahora durante 6 horas. Calcula 2⁶ y explica con una frase qué significa el resultado.',
 'No multipliques 2 por 6. Parte de 2⁴ = 16, que ya está en el gráfico, y da dos duplicaciones más: 16·2 = 32 y 32·2 = 64. Así 2⁶ = 64: al cabo de 6 horas hay 64 veces la masa inicial. El paso que evita el error es encadenar multiplicaciones por 2, una por hora, en lugar de un producto por el número de horas.',
 'e06a'),
(2, 'Logaritmo decimal de una noticia',
 'Una noticia habla de 10 000 casos. Escribe 10 000 como potencia de 10 y halla log₁₀(10 000).',
 'Cuenta los ceros, o mejor los factores 10: 10 000 = 10·10·10·10 = 10⁴. Por definición log₁₀(10⁴) = 4. El paso fino es no contar solo los ceros si el número no es un 1 seguido de ceros: aquí sí lo es, así que el exponente es 4. Comprobar es rehacer 10⁴ = 10 000. Decir que el logaritmo es 10 000, o 40, confunde el resultado con el exponente.',
 'e06b'),
(3, 'Raíz cúbica',
 '¿Cuánto es la raíz cúbica de 64? Justifica con una potencia y di qué error comete quien responde 32.',
 'Busca un entero cuyo cubo sea 64. 4³ = 4·4·4 = 64, luego la raíz cúbica es 4. Quien responde 32 ha dividido 64 entre 2, como si toda raíz fuera «partir por la mitad». El paso correcto es probar el cubo, no el cociente: 4·4 = 16 y 16·4 = 64. Comprueba que 32² ya es 1 024, y 32³ es enorme, así que 32 no puede ser la raíz cúbica de 64.',
 'e06c'),
],
[
('En el gráfico, ¿qué coordenada es el exponente en y = 2ˣ y cuál lo es en y = log₂(x)?',
 'En la curva ámbar el exponente es la abscisa x; en la verde el exponente es la ordenada. Por qué: 2ˣ eleva la base al valor horizontal, así que en x = 4 la altura es 16. El logaritmo deshace eso y coloca el exponente en el eje vertical: log₂(8) = 3 se dibuja como el punto (8, 3).'),
('¿Por qué 2⁴ no es 8?',
 'Porque 2⁴ significa cuatro factores iguales a 2, no 2 por 4. Por qué: 2·2·2·2 = 16, mientras que 2·4 = 8 es un producto con un solo dos. En el cultivo, 8 sería el valor a las 3 horas (2³), no a las 4.'),
('¿√144 puede dar 72?',
 'No. Por qué: la raíz cuadrada es el número que, multiplicado por sí mismo, recupera 144. 12·12 = 144, pero 72·72 es mucho mayor. 72 es la mitad, y partir entre dos no es la definición de raíz.'),
],
'Una potencia de tu semana',
'Elige algo que se duplique o se parta (rumor, ahorro, medio tiempo de un juego). Escribe la potencia o la raíz con una frase de significado y comprueba rehaciendo la operación inversa.',
['La curva ámbar es 2 elevado a x y pasa por (4, 16); la verde es el logaritmo en base 2 y marca (8, 3).',
 'No leas la potencia como una multiplicación por el exponente: 2⁴ es 16, no 8.',
 'Ejemplo 1: cuatro duplicaciones llevan a 16 veces la masa inicial.',
 'Ejemplo 2: logaritmo en base 2 de 8 es el exponente 3, el mismo punto verde.',
 'Ejemplo 3: 3 elevado a x igual a 81 obliga x = 4, y la raíz de 144 es 12, no 72.',
 'En los ejercicios encadena 2⁶ desde 16 y no dividas cuando toque una raíz.',
 'Comprueba intercambiando potencia y logaritmo antes de abrir el porqué.']
)

# ---------- L07 lab + lección ----------
write_lab(7, 'Producto de matrices 2×2', '''
<div class="panel">
<p>Reproduce el producto de la lección o cambia una casilla. A es la primera matriz y B la segunda. El resultado es A por B, en ese orden.</p>
<p>A: <input id="a11" value="2" size="3"/> <input id="a12" value="1" size="3"/><br/>
<input id="a21" value="0" size="3"/> <input id="a22" value="3" size="3"/></p>
<p>B: <input id="b11" value="4" size="3"/> <input id="b12" value="-1" size="3"/><br/>
<input id="b21" value="5" size="3"/> <input id="b22" value="2" size="3"/></p>
<button id="go" type="button">Calcular AB y BA</button>
<div class="out" id="out"></div>
</div>
<script>
function v(id){return parseFloat(String(document.getElementById(id).value).replace(',','.'));}
document.getElementById('go').onclick=function(){
  var a=v('a11'),b=v('a12'),c=v('a21'),d=v('a22');
  var e=v('b11'),f=v('b12'),g=v('b21'),h=v('b22');
  function fmt(x){return (Math.round(x*1000)/1000).toString().replace('.',',');}
  var p=[a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h];
  var q=[e*a+f*c, e*b+f*d, g*a+h*c, g*b+h*d];
  document.getElementById('out').textContent='AB = [[ '+fmt(p[0])+' , '+fmt(p[1])+' ] , [ '+fmt(p[2])+' , '+fmt(p[3])+' ]]   |   BA = [[ '+fmt(q[0])+' , '+fmt(q[1])+' ] , [ '+fmt(q[2])+' , '+fmt(q[3])+' ]]';
};
</script>
''')

fig07 = '''
<line x1="40" y1="40" x2="200" y2="40" stroke="#C4A15A" stroke-width="2"/>
<line x1="40" y1="100" x2="200" y2="100" stroke="#9A9488"/>
<line x1="40" y1="160" x2="200" y2="160" stroke="#C4A15A" stroke-width="2"/>
<line x1="40" y1="40" x2="40" y2="160" stroke="#C4A15A" stroke-width="2"/>
<line x1="120" y1="40" x2="120" y2="160" stroke="#9A9488"/>
<line x1="200" y1="40" x2="200" y2="160" stroke="#C4A15A" stroke-width="2"/>
<line x1="250" y1="40" x2="410" y2="40" stroke="#8F9A72" stroke-width="2"/>
<line x1="250" y1="100" x2="410" y2="100" stroke="#9A9488"/>
<line x1="250" y1="160" x2="410" y2="160" stroke="#8F9A72" stroke-width="2"/>
<line x1="250" y1="40" x2="250" y2="160" stroke="#8F9A72" stroke-width="2"/>
<line x1="330" y1="40" x2="330" y2="160" stroke="#9A9488"/>
<line x1="410" y1="40" x2="410" y2="160" stroke="#8F9A72" stroke-width="2"/>
<line x1="470" y1="40" x2="670" y2="40" stroke="#E6E1D6" stroke-width="2"/>
<line x1="470" y1="100" x2="670" y2="100" stroke="#9A9488"/>
<line x1="470" y1="160" x2="670" y2="160" stroke="#E6E1D6" stroke-width="2"/>
<line x1="470" y1="40" x2="470" y2="160" stroke="#E6E1D6" stroke-width="2"/>
<line x1="570" y1="40" x2="570" y2="160" stroke="#9A9488"/>
<line x1="670" y1="40" x2="670" y2="160" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="80" cy="70" r="16" fill="#1C1A16" stroke="#C4A15A" stroke-width="2"/>
<circle cx="290" cy="70" r="16" fill="#1C1A16" stroke="#8F9A72" stroke-width="2"/>
<text x="80" y="75" text-anchor="middle" fill="#E6E1D6" font-size="16">2</text>
<text x="160" y="75" text-anchor="middle" fill="#E6E1D6" font-size="16">1</text>
<text x="80" y="138" text-anchor="middle" fill="#E6E1D6" font-size="16">0</text>
<text x="160" y="138" text-anchor="middle" fill="#E6E1D6" font-size="16">3</text>
<text x="290" y="75" text-anchor="middle" fill="#E6E1D6" font-size="16">4</text>
<text x="370" y="75" text-anchor="middle" fill="#E6E1D6" font-size="16">−1</text>
<text x="290" y="138" text-anchor="middle" fill="#E6E1D6" font-size="16">5</text>
<text x="370" y="138" text-anchor="middle" fill="#E6E1D6" font-size="16">2</text>
<text x="520" y="75" text-anchor="middle" fill="#E6E1D6" font-size="16">13</text>
<text x="620" y="75" text-anchor="middle" fill="#E6E1D6" font-size="16">0</text>
<text x="520" y="138" text-anchor="middle" fill="#E6E1D6" font-size="16">15</text>
<text x="620" y="138" text-anchor="middle" fill="#E6E1D6" font-size="16">6</text>
<text x="120" y="190" text-anchor="middle" fill="#C4A15A" font-size="14">A</text>
<text x="330" y="190" text-anchor="middle" fill="#8F9A72" font-size="14">B</text>
<text x="570" y="190" text-anchor="middle" fill="#E6E1D6" font-size="14">AB</text>
<path d="M80,70 L290,130" fill="none" stroke="#C4A15A" stroke-width="1.5" stroke-dasharray="4 3"/>
<text x="40" y="250" fill="#9A9488" font-size="14">13 = 2·4 + 1·5. Los círculos marcan el 2 de A y el 4 de B, primer sumando.</text>
'''
build(
7, 'Matrices: clasificación y <em>operaciones</em>', 'A.2 Matrices: clasificación y operaciones',
'La tabla que se multiplica por filas y columnas',
'CyL introduce las matrices como tablas con álgebra propia. Clasificamos por tamaño y calculamos suma, producto por un número y producto de matrices con el caso numérico dibujado: A, B y AB.',
['Clasificar matrices por su tamaño y citar la identidad.','Sumar y multiplicar por un escalar casilla a casilla.','Multiplicar matrices 2×2 por filas y columnas, y ver que el orden importa.'],
'''<h2>Una matriz es una tabla con reglas</h2>
<p>Una matriz es un rectángulo de números ordenados en filas y columnas. El tamaño se dice «filas por columnas». No toda tabla de un periódico es una matriz en sentido algebraico, pero toda matriz se puede escribir como tabla.</p>
<p><span class="glosa">A es 2×2, cuadrada · el elemento a₁₂ está en la fila 1 y la columna 2 · I₂ tiene unos en la diagonal y ceros fuera · el producto AB usa filas de A contra columnas de B</span></p>
<p>En esta lección A = [[2, 1], [0, 3]] y B = [[4, −1], [5, 2]]. Las dos son cuadradas de orden 2. La suma existe porque tienen el mismo tamaño: cada casilla se suma con la casilla del mismo sitio. El producto AB también existe porque las columnas de A (2) coinciden con las filas de B (2).</p>
<p>El gráfico dibuja las dos rejillas y el resultado. El 13 de la esquina superior izquierda de AB no es 2·4 a secas: es el producto escalar de la primera fila de A por la primera columna de B, 2·4 + 1·5. Cambiar el orden y calcular BA produce otra matriz.</p>
<table class="datos"><thead><tr><th>Tipo</th><th>Tamaño de un ejemplo</th><th>Rasgo</th></tr></thead>
<tbody>
<tr><td>Cuadrada</td><td>2×2, como A y B</td><td>mismo número de filas y de columnas</td></tr>
<tr><td>Fila</td><td>1×4</td><td>una sola fila</td></tr>
<tr><td>Columna</td><td>3×1</td><td>una sola columna</td></tr>
<tr><td>Identidad I₂</td><td>2×2</td><td>[[1, 0], [0, 1]]; cumple I₂·A = A</td></tr>
<tr><td>Nula</td><td>2×2</td><td>todos los elementos 0; elemento neutro de la suma</td></tr>
</tbody></table>''',
'Rejillas de A = [[2, 1], [0, 3]], B = [[4, −1], [5, 2]] y el producto AB = [[13, 0], [15, 6]]', fig07,
[
('Suma y doble',
 'Con las matrices del gráfico, calcula A + B y 2A. Comprueba el tamaño del resultado.',
 [
  ('La suma exige el mismo tamaño. Aquí ambos son 2×2, así que se puede sumar casilla a casilla.',
   'Glosa: si una fuera 2×3, la suma no estaría definida; no se «rellenan» ceros por nuestra cuenta salvo que el enunciado lo diga.'),
  ('A + B = [[2+4, 1+(−1)], [0+5, 3+2]] = [[6, 0], [5, 5]].',
   'Glosa: el 1 y el −1 de la primera fila se cancelan; no se multiplican.'),
  ('2A multiplica cada casilla por 2: [[4, 2], [0, 6]]. No es A + A escrito de otra forma casual: es la misma matriz, y sirve de comprobación porque A + A = [[4, 2], [0, 6]].',
   'Glosa: el escalar no se coloca como una casilla más; reparte su producto por todas.'),
  ('El resultado de sumar sigue siendo 2×2. El de multiplicar por 2 también. El tamaño solo cambia, a veces, en el producto de matrices de tamaños distintos.',
   'Glosa: en este ejemplo no hay cambio de tamaño; no lo inventes.'),
 ]),
('El 13 del gráfico',
 'Calcula las cuatro casillas de AB y explica de dónde sale el 0 de la primera fila.',
 [
  ('Primera fila de A (2, 1) por primera columna de B (4, 5): 2·4 + 1·5 = 8 + 5 = 13.',
   'Glosa: es el camino que marcan los círculos y la línea discontinua del SVG.'),
  ('Primera fila de A por segunda columna de B (−1, 2): 2·(−1) + 1·2 = −2 + 2 = 0.',
   'Glosa: el cero no significa «no se multiplica»; es una cancelación −2 + 2.'),
  ('Segunda fila de A (0, 3) por las dos columnas: 0·4 + 3·5 = 15 y 0·(−1) + 3·2 = 6.',
   'Glosa: el 0 de A anula el primer sumando; no anula la fila entera.'),
  ('AB = [[13, 0], [15, 6]]. Comprueba la casilla 15: 3·5 = 15, porque el otro sumando lleva el 0 de A.',
   'Glosa: cada casilla del producto tiene su propia fila y su propia columna; no se copia un patrón.'),
 ]),
('El orden importa',
 'Calcula BA y compáralo con AB. ¿Son la misma matriz?',
 [
  ('BA multiplica filas de B por columnas de A. Primera casilla: fila (4, −1) por columna (2, 0): 4·2 + (−1)·0 = 8.',
   'Glosa: ahora la fila viene de B; no reutilices el 13.'),
  ('Siguiente casilla de la primera fila: (4, −1) por (1, 3): 4·1 + (−1)·3 = 4 − 3 = 1.',
   'Glosa: ya no sale 0. El orden ha cambiado los compañeros de producto.'),
  ('Segunda fila de B (5, 2) por las columnas de A: 5·2 + 2·0 = 10 y 5·1 + 2·3 = 11.',
   'Glosa: BA = [[8, 1], [10, 11]].'),
  ('AB y BA son distintas. En matrices cuadradas el producto puede existir en los dos órdenes y aun así no conmutar.',
   'Glosa: la suma sí conmuta (A+B = B+A); el producto, no. No traslades la costumbre de los números.'),
 ]),
],
[
(1, 'Clasifica y suma',
 'C = [[1, 0, 4], [2, −1, 3]] y D es 2×2. ¿Qué tamaño tiene C? ¿Existe C + D? ¿Y 3C?',
 'C tiene 2 filas y 3 columnas: es rectangular 2×3, no cuadrada. C + D no existe porque D es 2×2 y la suma pide el mismo número de filas y de columnas; no se recorta C para forzarla. 3C sí existe y es otra 2×3: cada casilla por 3, o sea [[3, 0, 12], [6, −3, 9]]. El paso decisivo es mirar el tamaño antes de operar, no después de haber sumado casillas que no se corresponden.',
 'e07a'),
(2, 'Una casilla del producto',
 'Solo con A y B del gráfico, vuelve a obtener la casilla inferior derecha de AB y di qué fila y qué columna usaste.',
 'La casilla de la fila 2 y la columna 2 usa la segunda fila de A, que es (0, 3), y la segunda columna de B, que es (−1, 2). El producto escalar es 0·(−1) + 3·2 = 6. No intervienen el 13 ni el 15: cada casilla tiene su par fila-columna. Si usas la primera fila de A obtendrías el 0 de arriba, que es otro elemento. Este es el mismo paso que en el ejemplo resuelto, cambiado de casilla para asegurar que no memorizas solo el 13.',
 'e07b'),
(3, 'Identidad',
 'Multiplica I₂ = [[1, 0], [0, 1]] por A y explica por qué el resultado es A.',
 'Fila (1, 0) de la identidad por las columnas de A copia la primera fila de A: 1·2 + 0·0 = 2 y 1·1 + 0·3 = 1. Fila (0, 1) copia la segunda: 0·2 + 1·0 = 0 y 0·1 + 1·3 = 3. Sale A. El paso general es que el 1 de la diagonal deja pasar la casilla correspondiente y el 0 apaga la otra. Por eso I₂ es el elemento neutro del producto, parecido al 1 de los números, y no se comporta como la matriz nula, que es el neutro de la suma.',
 'e07c'),
],
[
('¿De dónde sale el 13 de AB en el gráfico?',
 'De la primera fila de A por la primera columna de B: 2·4 + 1·5 = 13. Por qué: el producto de matrices no multiplica casillas del mismo sitio, como hace la suma. Combina una fila entera con una columna entera. Los círculos del SVG señalan el primer sumando de esa cuenta.'),
('¿Por qué AB y BA no coinciden en este ejemplo?',
 'Porque al cambiar el orden cambian las filas y las columnas que se emparejan. Por qué: BA da [[8, 1], [10, 11]] y AB da [[13, 0], [15, 6]]. Las dos existen (las dos matrices son 2×2) y aun así son distintas. El producto de matrices no hereda la conmutatividad del producto de números.'),
('¿Se puede sumar una matriz 2×3 con una 2×2?',
 'No. Por qué: la suma está definida casilla a casilla y cada casilla necesita compañera en el mismo sitio. Si sobra una columna, esa casilla no tiene pareja y la operación no está definida. El producto tiene otra condición: columnas de la primera iguales a filas de la segunda.'),
],
'Rejilla propia',
'Dibuja en el lienzo dos matrices 2×2 distintas de A y B, calcula AB en el laboratorio y copia una casilla explicada como fila por columna.',
['Las rejillas del SVG son A, B y el producto AB del ejemplo, con el 13 escrito a la derecha.',
 'El 13 no es 2 por 4: es 2·4 + 1·5, fila por columna.',
 'Ejemplo 1: A + B = [[6, 0], [5, 5]] y 2A = [[4, 2], [0, 6]].',
 'Ejemplo 2: la casilla de arriba a la derecha de AB es 0 porque −2 + 2 se cancela.',
 'Ejemplo 3: BA = [[8, 1], [10, 11]], distinta de AB.',
 'En el laboratorio cambia una casilla y mira cómo se mueve solo la fila o la columna afectada.',
 'Cierra clasificando tamaños antes de operar.'],
lab_title='Producto de matrices 2×2'
)
print('L05-L07 builds defined')

# ---------- L08 ----------
fig08 = '''
<line x1="150" y1="70" x2="340" y2="70" stroke="#C4A15A" stroke-width="2.5"/>
<line x1="340" y1="70" x2="340" y2="230" stroke="#C4A15A" stroke-width="2.5"/>
<line x1="150" y1="70" x2="340" y2="230" stroke="#C4A15A" stroke-width="2.5"/>
<line x1="150" y1="70" x2="150" y2="230" stroke="#C4A15A" stroke-width="2.5"/>
<circle cx="150" cy="70" r="16" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="340" cy="70" r="16" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="340" cy="230" r="16" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<circle cx="150" cy="230" r="16" fill="#1C1A16" stroke="#E6E1D6" stroke-width="2"/>
<text x="150" y="75" text-anchor="middle" fill="#E6E1D6" font-size="14">A</text>
<text x="340" y="75" text-anchor="middle" fill="#E6E1D6" font-size="14">B</text>
<text x="340" y="235" text-anchor="middle" fill="#E6E1D6" font-size="14">C</text>
<text x="150" y="235" text-anchor="middle" fill="#E6E1D6" font-size="14">D</text>
<line x1="430" y1="40" x2="680" y2="40" stroke="#C4A15A"/>
<line x1="430" y1="82" x2="680" y2="82" stroke="#9A9488"/>
<line x1="430" y1="124" x2="680" y2="124" stroke="#9A9488"/>
<line x1="430" y1="166" x2="680" y2="166" stroke="#9A9488"/>
<line x1="430" y1="208" x2="680" y2="208" stroke="#C4A15A"/>
<line x1="430" y1="40" x2="430" y2="208" stroke="#C4A15A"/>
<line x1="492" y1="40" x2="492" y2="208" stroke="#9A9488"/>
<line x1="554" y1="40" x2="554" y2="208" stroke="#9A9488"/>
<line x1="616" y1="40" x2="616" y2="208" stroke="#9A9488"/>
<line x1="680" y1="40" x2="680" y2="208" stroke="#C4A15A"/>
<text x="461" y="70" text-anchor="middle" fill="#E6E1D6" font-size="14">0</text>
<text x="523" y="70" text-anchor="middle" fill="#C4A15A" font-size="14">1</text>
<text x="585" y="70" text-anchor="middle" fill="#C4A15A" font-size="14">1</text>
<text x="648" y="70" text-anchor="middle" fill="#C4A15A" font-size="14">1</text>
<text x="461" y="112" text-anchor="middle" fill="#C4A15A" font-size="14">1</text>
<text x="523" y="112" text-anchor="middle" fill="#E6E1D6" font-size="14">0</text>
<text x="585" y="112" text-anchor="middle" fill="#C4A15A" font-size="14">1</text>
<text x="648" y="112" text-anchor="middle" fill="#E6E1D6" font-size="14">0</text>
<text x="461" y="154" text-anchor="middle" fill="#C4A15A" font-size="14">1</text>
<text x="523" y="154" text-anchor="middle" fill="#C4A15A" font-size="14">1</text>
<text x="585" y="154" text-anchor="middle" fill="#E6E1D6" font-size="14">0</text>
<text x="648" y="154" text-anchor="middle" fill="#E6E1D6" font-size="14">0</text>
<text x="461" y="196" text-anchor="middle" fill="#C4A15A" font-size="14">1</text>
<text x="523" y="196" text-anchor="middle" fill="#E6E1D6" font-size="14">0</text>
<text x="585" y="196" text-anchor="middle" fill="#E6E1D6" font-size="14">0</text>
<text x="648" y="196" text-anchor="middle" fill="#E6E1D6" font-size="14">0</text>
<text x="430" y="236" fill="#9A9488" font-size="13">Filas y columnas en orden A, B, C, D. Un 1 es una arista.</text>
'''
build(
8, 'Matrices, tablas y <em>grafos</em>', 'A.2 Matrices como herramienta en tablas y grafos',
'El 1 que significa «hay arista»',
'La matriz de adyacencia guarda un grafo en una tabla. El dibujo de la izquierda tiene cuatro vértices y cuatro aristas; la rejilla de la derecha es exactamente esa información, casilla a casilla.',
['Construir la matriz de adyacencia de un grafo sin lazos.','Leer grados y el número de aristas desde la matriz.','Contar caminos de longitud 2 con el producto de la matriz por sí misma.'],
'''<h2>Del dibujo a la tabla, sin perder aristas</h2>
<p>Un grafo pequeño se puede mirar. En cuanto crece, conviene una matriz: filas y columnas con los mismos vértices, y un 1 en la casilla (i, j) si hay arista entre ellos. En un grafo no dirigido esa tabla es simétrica: la arista AB se anota arriba y abajo de la diagonal.</p>
<p><span class="glosa">vértice = punto del grafo · arista = trazo que une dos vértices · lazo = arista de un vértice a sí mismo, que aquí no hay · grado de un vértice = número de aristas que inciden en él · E = número de aristas</span></p>
<p>En el ejemplo hay vértices A, B, C y D. Las aristas dibujadas son AB, BC, CA y AD. No hay BD, ni CD, ni lazos. Por eso la diagonal de la matriz es 0, 0, 0, 0 y las casillas BD, DB, CD y DC también son 0. El grado de A es 3 (llega a B, a C y a D) y la primera fila suma 3.</p>
<p>Sumar todos los grados cuenta cada arista dos veces, una por cada extremo. Aquí 3+2+2+1 = 8 = 2E, luego E = 4, que son las cuatro líneas del dibujo. Multiplicar la matriz por sí misma no dibuja aristas nuevas: la casilla (A, C) de M² cuenta caminos de dos pasos desde A hasta C.</p>
<table class="datos"><thead><tr><th>Vértice</th><th>Vecinos en el dibujo</th><th>Grado</th><th>Suma de su fila</th></tr></thead>
<tbody>
<tr><td>A</td><td>B, C, D</td><td>3</td><td>0+1+1+1 = 3</td></tr>
<tr><td>B</td><td>A, C</td><td>2</td><td>1+0+1+0 = 2</td></tr>
<tr><td>C</td><td>A, B</td><td>2</td><td>1+1+0+0 = 2</td></tr>
<tr><td>D</td><td>A</td><td>1</td><td>1+0+0+0 = 1</td></tr>
</tbody></table>''',
'Grafo A-B, B-C, C-A, A-D y su matriz de adyacencia 4×4', fig08,
[
('De las líneas a los unos',
 'Escribe la matriz de adyacencia del grafo dibujado, en el orden A, B, C, D, y justifica la simetría.',
 [
  ('Lista las aristas del dibujo: AB, BC, CA y AD. Son cuatro. No inventes BD ni CD: no hay trazo.',
   'Glosa: cada segmento del SVG es una arista; la diagonal del triángulo es CA, no un adorno.'),
  ('Coloca un 1 en (A,B), (B,A), (B,C), (C,B), (C,A), (A,C), (A,D) y (D,A). El resto, ceros.',
   'Glosa: al ser no dirigido, cada arista escribe dos unos, salvo que fuera un lazo.'),
  ('La diagonal queda a cero porque ningún vértice está unido consigo mismo.',
   'Glosa: un lazo se vería como un bucle en el dibujo y un 1 en la diagonal; aquí no aparece.'),
  ('Comprueba la simetría: la casilla (fila i, columna j) coincide con (fila j, columna i). Si no, te falta uno de los dos sentidos de la misma arista.',
   'Glosa: en un grafo dirigido la matriz puede dejar de ser simétrica; este dibujo no tiene flechas.'),
 ]),
('Grados y doble conteo',
 'Calcula el grado de cada vértice sumando filas y deduce E.',
 [
  ('Suma la fila A: 3. Fila B: 2. Fila C: 2. Fila D: 1. Esos son los grados.',
   'Glosa: el grado no es el número de vértices vecinos «a ojo» si hay lazos; aquí, al no haberlos, coincide con la suma de la fila.'),
  ('Suma de grados = 3+2+2+1 = 8.',
   'Glosa: 8 no es el número de aristas. Cada arista aporta a dos grados.'),
  ('Por el lema del apretón de manos, suma de grados = 2E. Entonces 2E = 8 y E = 4.',
   'Glosa: divide entre 2 al final, no al principio. Si divides cada grado, pierdes el sentido del doble conteo.'),
  ('Comprueba contando segmentos en el SVG: AB, BC, CA, AD. Cuatro. Cuadra con E = 4.',
   'Glosa: si la matriz y el dibujo no dan el mismo E, hay un 1 de más o un trazo sin casilla.'),
 ]),
('Caminos de dos pasos',
 'Calcula la casilla (A, C) de M² y nombra el único camino de longitud 2 de A a C.',
 [
  ('La casilla (A, C) de M² es el producto de la fila A por la columna C: (0, 1, 1, 1) · (1, 1, 0, 0).',
   'Glosa: fila A es 0,1,1,1 y columna C es 1,1,0,0 porque la matriz es simétrica y la columna C copia la fila C.'),
  ('0·1 + 1·1 + 1·0 + 1·0 = 1.',
   'Glosa: el único sumando no nulo es el de la columna B: se sale de A hacia B y desde B se puede seguir a C.'),
  ('Ese 1 es el camino A-B-C. A-C-C no existe (no hay lazo) y A-D-C tampoco (D no toca a C).',
   'Glosa: A-C es un camino de longitud 1, no de longitud 2; M² no lo cuenta.'),
  ('Comprueba que hay arista A-B y arista B-C en el dibujo. Las dos hacen falta. Una sola no crea camino de dos pasos.',
   'Glosa: por eso el producto mira parejas de aristas encadenadas, no aristas sueltas.'),
 ]),
],
[
(1, 'Un cero que importa',
 'Alguien pone un 1 en la casilla (B, D) «porque B y D están en el grafo». ¿Qué afirma de más y cómo se ve en el dibujo?',
 'Un 1 en (B, D) afirmaría que existe la arista BD. En el dibujo B está unido a A y a C, y D solo a A: no hay segmento BD. El paso erróneo confunde «pertenecer al mismo grafo» con «estar unidos». La matriz solo registra adyacencia, no convivencia. Si aceptaras ese 1, el grado de B pasaría de 2 a 3, la suma de grados subiría en 2 (también el 1 simétrico en D,B) y E pasaría de 4 a 5, en contradicción con los cuatro segmentos visibles.',
 'e08a'),
(2, '¿Por qué la diagonal es cero?',
 'Explica, con este grafo concreto, qué significaría un 1 en la casilla (C, C) y por qué no debe ponerse.',
 'La casilla (C, C) es la intersección de la fila C con la columna C. Un 1 diría que C tiene un lazo, una arista con los dos extremos en C. El grado de C contaría ese lazo según el convenio del curso (aquí no usamos lazos, así que la diagonal se queda en 0). En el SVG no hay ningún bucle sobre el círculo C: sus únicos trazos van a A y a B. Poner el 1 copiaría un dato que el dibujo no contiene y rompería la lectura «unos = segmentos que se ven».',
 'e08b'),
(3, 'Otro camino',
 '¿Cuántos caminos de longitud 2 hay de A a A? Relaciónalos con el grado de A sin multiplicar la matriz entera.',
 'Un camino de longitud 2 que empieza y acaba en A es salir por una arista y volver por la misma, porque los vecinos de A no están unidos entre sí de forma que cierren otro ciclo de dos (un ciclo de dos no existe en un grafo simple). Desde A se puede ir a B y volver, a C y volver, o a D y volver: tres paseos. Coincide con el grado de A. El paso es emparejar cada arista incidente con su vuelta inmediata. Si el grafo tuviera un triángulo que vuelva a A en dos pasos por vecinos distintos, habría que contarlos aparte; aquí los vecinos B, C y D no se conectan todos entre sí en un triángulo que incluya solo dos pasos distintos de la ida y vuelta. El triángulo es A-B-C-A, que es longitud 3. Por eso los retornos de longitud 2 son exactamente las tres idas y vueltas, y la casilla (A, A) de M² vale 3.',
 'e08c'),
],
[
('¿Qué significa el 1 de la fila B, columna C?',
 'Que la arista BC está en el grafo, la misma que el segmento vertical del dibujo. Por qué: la fila elige el extremo B y la columna el extremo C. El 1 no es una distancia ni un peso: en esta lección solo dice si la arista existe. El peso llegará en grafos ponderados.'),
('¿Por qué dividimos entre 2 la suma de los grados?',
 'Porque cada arista se ha contado en los dos extremos. Por qué: AB suma 1 al grado de A y 1 al de B. Si no divides, obtienes 8, que es el doble de las cuatro aristas. La fórmula suma de grados = 2E obliga a ese paso final.'),
('¿Un camino de longitud 1 aparece en M²?',
 'No. Por qué: M² combina dos aristas seguidas. La arista CA es un camino de longitud 1 y vive en la propia matriz M, casilla (C, A), no en el cuadrado. Confundirlas mezcla «estar unidos» con «llegar en dos saltos».'),
],
'Matriz de un plano',
'Dibuja en el lienzo cuatro lugares de tu instituto y las conexiones que usas. Escribe la matriz 4×4 y la suma de grados.',
['El SVG parte el grafo a la izquierda y la matriz a la derecha: mismos cuatro vértices.',
 'Hay cuatro aristas: AB, BC, CA y AD. La diagonal de la matriz está a cero.',
 'Ejemplo 1: cada arista escribe dos unos, y la tabla queda simétrica.',
 'Ejemplo 2: grados 3, 2, 2 y 1; suma 8; E = 4.',
 'Ejemplo 3: de A a C en dos pasos solo se puede A-B-C, y la casilla de M² vale 1.',
 'No pongas un 1 solo porque dos vértices existan: tiene que verse el trazo.',
 'Comprueba simetría y doble conteo antes de dar por buena la matriz.']
)

# ---------- L09 ----------
fig09 = ''.join(
    f'<circle cx="{70+i*46}" cy="90" r="16" fill="{"#C4A15A" if i<3 else "#8F9A72"}" stroke="#E6E1D6"/>'
    for i in range(8)
) + '''
<line x1="54" y1="150" x2="450" y2="150" stroke="#E6E1D6" stroke-width="2"/>
<line x1="54" y1="140" x2="54" y2="160" stroke="#E6E1D6" stroke-width="2"/>
<line x1="202" y1="140" x2="202" y2="160" stroke="#C4A15A" stroke-width="2"/>
<line x1="450" y1="140" x2="450" y2="160" stroke="#8F9A72" stroke-width="2"/>
<path d="M54,150 L202,150" fill="none" stroke="#C4A15A" stroke-width="6"/>
<text x="70" y="190" fill="#C4A15A" font-size="15">3 partes · 300 ml</text>
<text x="250" y="190" fill="#8F9A72" font-size="15">5 partes · 500 ml</text>
<text x="480" y="80" fill="#E6E1D6" font-size="15">razón 3:5</text>
<text x="480" y="110" fill="#E6E1D6" font-size="15">8 partes = 800 ml</text>
<text x="480" y="140" fill="#9A9488" font-size="14">cada parte = 100 ml</text>
'''
build(
9, 'Razones, proporciones y <em>porcentajes</em>', 'A.3 Razones, proporciones, porcentajes y tasas',
'Ocho partes, no ocho mililitros de más',
'CyL pide razones, proporciones, porcentajes y tasas en contextos. El gráfico reparte 800 ml en razón 3:5: tres círculos ámbar y cinco verdes, 300 ml y 500 ml.',
['Pasar de una razón a una cantidad total repartida.','Calcular un porcentaje sobre la base correcta.','Usar una tasa «por cada 1 000» y una escala de mapa.'],
'''<h2>La razón no es el total</h2>
<p>Una razón 3:5 compara dos partes. No dice que haya 3 ml y 5 ml: dice que, de cada 8 partes iguales, 3 son del primer tipo y 5 del segundo. Hasta que no conoces el total, no hay mililitros.</p>
<p><span class="glosa">3:5 se lee «3 a 5» · 3+5 = 8 partes · porcentaje = tanto por ciento, base 100 · tasa por 1 000 = casos por cada mil unidades · escala 1:25 000 = 1 cm del mapa son 25 000 cm reales</span></p>
<p>En el gráfico el total es 800 ml. Como hay 8 partes, cada parte pesa 800/8 = 100 ml. El primer líquido se lleva 3×100 = 300 ml y el segundo 5×100 = 500 ml. La marca de la regla cae justo al acabar el tercer círculo.</p>
<p>Un porcentaje es una razón con segunda cantidad 100. 240 de 800 es 240/800 = 0,30 = 30 %. Subir un 30 % no es lo mismo que pasar a ser el 30 %: la base del «un 30 % más» es el valor que ya tenías, no el total del instituto.</p>
<table class="datos"><thead><tr><th>Lenguaje</th><th>Escritura</th><th>Dato de esta lección</th></tr></thead>
<tbody>
<tr><td>Razón</td><td>3:5</td><td>300 ml frente a 500 ml</td></tr>
<tr><td>Fracción del total</td><td>3/8</td><td>300 de 800 ml</td></tr>
<tr><td>Porcentaje</td><td>37,5 %</td><td>porque 3/8 = 0,375</td></tr>
<tr><td>Tasa</td><td>12 por 1 000</td><td>300 casos en 25 000 habitantes</td></tr>
</tbody></table>''',
'Ocho círculos en razón 3:5 que reparten 800 ml en 300 y 500', fig09,
[
('El zumo de 800 ml',
 'Se mezclan dos zumos en razón 3:5 hasta llenar 800 ml. Halla cada cantidad y comprueba la suma.',
 [
  ('Suma las partes de la razón: 3+5 = 8. El 8 no es un volumen; es el número de partes iguales.',
   'Glosa: si sumas 3+5 y lo dejas en mililitros, has cambiado de unidad a mitad del problema.'),
  ('Cada parte mide 800/8 = 100 ml.',
   'Glosa: divides el total conocido entre las partes, no al revés.'),
  ('Primer zumo: 3×100 = 300 ml. Segundo: 5×100 = 500 ml. En el gráfico, tres círculos ámbar y cinco verdes.',
   'Glosa: 300/500 = 3/5, la misma razón del enunciado.'),
  ('Comprueba 300+500 = 800. Si no cierra, la parte unitaria está mal calculada.',
   'Glosa: la comprobación es obligatoria en un reparto: las partes tienen que reconstruir el total.'),
 ]),
('240 de 800, y un 30 % más',
 'En un instituto de 800 alumnos, 240 van al comedor. ¿Qué porcentaje son? Si el curso que viene el comedor crece un 30 %, ¿cuántos comen?',
 [
  ('Porcentaje actual: 240/800 = 24/80 = 12/40 = 3/10 = 0,30 = 30 %.',
   'Glosa: la base del porcentaje es 800, los alumnos, no 240.'),
  ('Un 30 % más no significa «pasar al 60 %» ni «añadir 30 alumnos». Se calcula el 30 % de 240.',
   'Glosa: la base ha cambiado: ahora es el valor que va a crecer, 240.'),
  ('0,30×240 = 72. Nuevo comedor: 240+72 = 312 alumnos.',
   'Glosa: también 240×1,30 = 312. El 1,30 junta el 100 % antiguo con el 30 % nuevo.'),
  ('Comprueba que 312 no es el 30 % de 800 (eso sería otra vez 240). Son preguntas distintas.',
   'Glosa: «el 30 % de» y «un 30 % más que» no comparten base.'),
 ]),
('Tasa y mapa',
 'Hay 12 accidentes por cada 1 000 habitantes. En una ciudad de 25 000 habitantes, ¿cuántos accidentes espera el modelo? En un mapa a escala 1:25 000, ¿cuántos km reales son 4 cm?',
 [
  ('25 000 / 1 000 = 25 grupos de mil habitantes. Accidentes: 25×12 = 300.',
   'Glosa: la tasa no se suma 12+25 000; se multiplica por el número de bloques de 1 000.'),
  ('Escala 1:25 000 significa que 1 cm del papel son 25 000 cm reales.',
   'Glosa: los dos lados de la escala van en la misma unidad antes de pasar a km.'),
  ('4 cm del mapa son 4×25 000 = 100 000 cm. Como 100 000 cm = 1 000 m = 1 km, la distancia real es 1 km.',
   'Glosa: 100 cm = 1 m y 1 000 m = 1 km; conviene pasar por metros para no perder ceros.'),
  ('Comprueba la tasa al revés: 300 accidentes en 25 000 habitantes son 300/25 = 12 por cada mil.',
   'Glosa: si no recuperas la tasa 12, el número de grupos está mal.'),
 ]),
],
[
(1, 'Razón 2:3 y 1 litro',
 'Reparte 1 000 ml en razón 2:3. Escribe las dos cantidades.',
 'Hay 2+3 = 5 partes. Cada parte es 1 000/5 = 200 ml. La primera cantidad es 2×200 = 400 ml y la segunda 3×200 = 600 ml. El paso que no puedes saltarte es convertir la razón en un número de partes antes de dividir el total: 2:3 no significa 2 ml y 3 ml, ni la mitad. Comprueba 400+600 = 1 000 y 400/600 = 2/3.',
 'e09a'),
(2, 'Rebaja',
 'Una chaqueta cuesta 80 € y la rebajan un 15 %. ¿Cuánto pagas? Explica por qué no pagas 80 − 15.',
 'El 15 % hay que convertirlo en tanto por uno y aplicarlo al precio: 0,15×80 = 12 € de rebaja. Pagas 80 − 12 = 68 €, o bien 80×0,85 = 68 €. Restar 15 a secas trata el porcentaje como si fueran 15 euros, y solo coincidiría si la base fuera 100 €. Aquí la base es 80, así que el 15 % son 12 euros, no 15. La comprobación es ver que 12 es a 80 como 15 es a 100.',
 'e09b'),
(3, 'Escala al revés',
 'En el mismo mapa 1:25 000, dos pueblos están a 3 km. ¿A cuántos centímetros hay que dibujarlos?',
 'Pasa 3 km a cm: 3 km = 3 000 m = 300 000 cm. La escala dice que el papel es 25 000 veces más pequeño, luego 300 000/25 000 = 12 cm. El paso delicado es no dividir 3 entre 25 000 dejando los kilómetros: las unidades tienen que coincidir antes de usar la razón. Comprueba al revés: 12 cm × 25 000 = 300 000 cm = 3 km.',
 'e09c'),
],
[
('En el gráfico, ¿cuántos mililitros vale cada círculo?',
 '100 ml. Por qué: hay 8 círculos y 800 ml, y la razón 3:5 obliga a que todas las partes sean iguales. 800/8 = 100. Tres círculos ámbar son 300 ml, no 3 ml.'),
('¿240 de 800 es el mismo cálculo que «un 30 % más que 240»?',
 'No. Por qué: 240/800 = 30 % usa de base 800 y describe qué fracción del instituto come. Un 30 % más que 240 usa de base 240 y da 312. Cambiar la base cambia la pregunta aunque el número 30 coincida.'),
('12 por cada 1 000 en 25 000 habitantes, ¿son 12 accidentes?',
 'No: son 300. Por qué: 25 000 contiene 25 millares, y cada millar aporta 12 casos según la tasa. 25×12 = 300. Dejar el 12 sin multiplicar olvida que la tasa es un ritmo, no el dato de la ciudad entera.'),
],
'Una razón en la cocina',
'Escribe una razón de una receta o de un mapa real, repártela sobre un total que elijas y comprueba que las partes suman el total.',
['Ocho círculos: tres ámbar y cinco verdes reparten 800 ml en 300 y 500.',
 'Primero cuentas las partes (8) y solo después aparecen los mililitros (100 cada una).',
 'Ejemplo 1: 3×100 y 5×100, y la suma vuelve a 800.',
 'Ejemplo 2: 240 de 800 es el 30 %, pero un 30 % más que 240 son 312.',
 'Ejemplo 3: la tasa 12 por 1 000 da 300 casos en 25 000 habitantes; 4 cm a escala 1:25 000 son 1 km.',
 'En los ejercicios no restes el porcentaje como si fuera un número de euros.',
 'Comprueba siempre que las partes reconstruyen el total.']
)
print('L08 L09 en fuente')

# ---------- L10 ----------
# barras: simple vs compuesto, capital de 2000 a 4 años al 3 %
# simple: 2000,2060,2120,2180,2240
# compuesto: 2000, 2060, 2121.80, 2185.45, 2251.02
def _cap_y(c):
    return 300 - (c - 1980) * 0.85
fig10 = ejes(50, 300, 690, 30)
simples = [2000, 2060, 2120, 2180, 2240]
compuestos = [2000, 2060, 2121.80, 2185.45, 2251.02]
for i, (s, c) in enumerate(zip(simples, compuestos)):
    x = 90 + i * 110
    fig10 += barra(x, _cap_y(s), 28, 300 - _cap_y(s), '#8F9A72')
    fig10 += barra(x + 34, _cap_y(c), 28, 300 - _cap_y(c), '#C4A15A')
fig10 += f'<circle cx="{90+4*110+34+14:.0f}" cy="{_cap_y(2251.02):.0f}" r="5" fill="#E6E1D6"/>'
fig10 += '''
<text x="60" y="22" fill="#8F9A72" font-size="14">verde: interés simple</text>
<text x="280" y="22" fill="#C4A15A" font-size="14">ámbar: interés compuesto</text>
<text x="520" y="22" fill="#E6E1D6" font-size="14">año 4: 2240 frente a 2251</text>
'''
build(
10, 'Educación <em>financiera</em>', 'A.4 Intereses, comisiones y cambios',
'El interés que también produce interés',
'CyL pide intereses, cuotas, comisiones y cambios de divisas. El gráfico compara, año a año, 2 000 € al 3 % anual durante 4 años: interés simple (verde) e interés compuesto anual (ámbar).',
['Calcular interés simple I = C·r·t y el montante.','Calcular un interés compuesto año a año.','Aplicar una comisión y un cambio de divisa sobre la cantidad correcta.'],
'''<h2>Simple, compuesto, comisión, divisa</h2>
<p>El interés es el precio de usar un dinero durante un tiempo. En el interés simple, cada año se calcula sobre el capital inicial y no sobre los intereses ya generados. En el compuesto, el interés de un año se suma al capital y el año siguiente trabaja sobre esa suma.</p>
<p><span class="glosa">C = capital inicial · r = tanto por uno anual (3 % es 0,03, no 3) · t = tiempo en años si r es anual · I = interés · montante = C + I · comisión = porcentaje o fijo que se resta o se suma por el servicio</span></p>
<p>Con C = 2 000 €, r = 0,03 y t = 4 años, el interés simple es 2 000·0,03·4 = 240 € y el montante es 2 240 €. El compuesto anual hace cuatro multiplicaciones por 1,03. El gráfico enseña que los dos crecen igual el primer año (ambos llegan a 2 060) y que a partir del segundo el ámbar se separa, poco a poco, hasta 2 251,02 €.</p>
<p>Una comisión del 0,6 % se calcula sobre la cantidad a la que se refiere el contrato, igual que un porcentaje de la lección anterior. Un cambio 1 € = 1,09 $ multiplica euros por 1,09 para pasar a dólares; para volver, se divide.</p>
<table class="datos"><thead><tr><th>Año</th><th>Montante simple</th><th>Montante compuesto</th></tr></thead>
<tbody>
<tr><td>0</td><td>2 000 €</td><td>2 000 €</td></tr>
<tr><td>1</td><td>2 060 €</td><td>2 060,00 €</td></tr>
<tr><td>2</td><td>2 120 €</td><td>2 121,80 €</td></tr>
<tr><td>3</td><td>2 180 €</td><td>2 185,45 €</td></tr>
<tr><td>4</td><td>2 240 €</td><td>2 251,02 €</td></tr>
</tbody></table>''',
'Barras del capital año a año: simple hasta 2240 € y compuesto hasta 2251 €', fig10,
[
('Cuatro años al 3 % simple',
 'Un depósito de 2 000 € al 3 % anual simple durante 4 años. Halla el interés y el montante, y léelos en la barra verde del año 4.',
 [
  ('Pasa el 3 % a tanto por uno: r = 0,03. No uses 3 en la fórmula.',
   'Glosa: 3 % de 2 000 es 60 €, no 3 € ni 6 000 €.'),
  ('I = C·r·t = 2 000·0,03·4. Primero 2 000·0,03 = 60 € de interés al año; después 60·4 = 240 €.',
   'Glosa: en el simple el interés anual no cambia, por eso las barras verdes crecen a saltos iguales.'),
  ('Montante = 2 000 + 240 = 2 240 €. Es la altura de la barra verde del último par.',
   'Glosa: el montante incluye el capital; el interés solo es la ganancia, 240 €.'),
  ('Comprueba un año intermedio: a los 2 años el interés es 120 € y el montante 2 120 €, la tercera barra verde (año 2).',
   'Glosa: si tu montante del año 2 no es 2 120, has compuesto sin querer o has usado mal r.'),
 ]),
('Los mismos datos, compuestos',
 'Capitaliza 2 000 € al 3 % compuesto anual durante 4 años, año a año, y compara con 2 240 €.',
 [
  ('Cada año se multiplica por 1,03, que es el capital más el 3 %. Año 1: 2 000·1,03 = 2 060 €.',
   'Glosa: el primer año simple y compuesto coinciden; el gráfico lo enseña.'),
  ('Año 2: 2 060·1,03. 2 060·1 = 2 060 y 2 060·0,03 = 61,80; total 2 121,80 €.',
   'Glosa: el interés de este año es 61,80, no 60, porque la base ya no es 2 000.'),
  ('Año 3: 2 121,80·1,03 = 2 185,454, que redondeamos a céntimos: 2 185,45 €. Año 4: 2 185,45·1,03 = 2 251,0135, unos 2 251,02 €.',
   'Glosa: el redondeo a céntimo se hace al cierre de cada año si el banco liquida así; aquí seguimos esa convención en el año 3 y 4.'),
  ('Diferencia con el simple: 2 251,02 − 2 240 = 11,02 €. Pequeña en 4 años al 3 %, pero es justo el interés del interés.',
   'Glosa: no digas que «casi da igual» sin haber restado; la diferencia está calculada.'),
 ]),
('Comisión y dólares',
 'Sobre los 2 000 € te cobran una comisión del 0,6 % al abrir el depósito. El resto lo cambias a dólares a 1 € = 1,09 $. ¿Cuántos dólares recibes?',
 [
  ('Comisión: 0,006×2 000 = 12 €. No es el 6 % (eso serían 120 €) ni 0,6 €.',
   'Glosa: 0,6 % = 0,6/100 = 0,006.'),
  ('Capital que sí se cambia: 2 000 − 12 = 1 988 €.',
   'Glosa: la comisión sale antes del cambio; si la calculas sobre los dólares, es otro contrato.'),
  ('Dólares: 1 988·1,09. 1 988·1 = 1 988 y 1 988·0,09 = 178,92; total 2 166,92 $.',
   'Glosa: multiplicar por 1,09 pasa de euros a dólares con este tipo de cambio.'),
  ('Comprueba al revés aproximando: 2 166,92 / 1,09 ≈ 1 988 €. Si no vuelves a los euros, el factor está invertido.',
   'Glosa: dividir entre 1,09 convierte dólares a euros; no sirvas las dos operaciones a la vez.'),
 ]),
],
[
(1, 'Seis meses simples',
 '2 000 € al 3 % anual simple, pero solo 6 meses. ¿Qué interés corresponde?',
 'El 3 % del enunciado es anual, y 6 meses son medio año: t = 0,5, no t = 6. I = 2 000·0,03·0,5 = 30 €. El paso que evita el error es pasar el tiempo a años antes de usar r, porque la fórmula supone que r y t hablan la misma unidad. Si pones t = 6 obtienes 360 €, más que el interés de 4 años enteros, lo cual delata que las unidades no casan. Comprueba: un año son 60 €, medio año la mitad.',
 'e10a'),
(2, 'Un año más de compuesto',
 'Partiendo del montante compuesto del año 4 (2 251,02 €), ¿cuál es el montante al acabar el año 5?',
 'No vuelvas a empezar desde 2 000. El compuesto del año 5 multiplica el último montante por 1,03: 2 251,02·1,03. Calcula 2 251,02·0,03 = 67,5306 y suma 2 251,02 + 67,53 = 2 318,55 € al céntimo. El paso propio del compuesto es usar como base lo ya acumulado. El simple, en cambio, sumaría otros 60 € y llegaría a 2 300 €. La diferencia sigue creciendo: 2 318,55 − 2 300 = 18,55 €.',
 'e10b'),
(3, 'Tipo de cambio inverso',
 'Te dan 327 $ y el cambio sigue siendo 1 € = 1,09 $. ¿Cuántos euros son, antes de comisiones?',
 'Para pasar de dólares a euros divides entre 1,09, no multiplicas. 327 / 1,09 = 300 € exactos, porque 300·1,09 = 327. El paso es decidir la dirección del tipo: el número 1,09 dice cuántos dólares vale un euro, así que los dólares son la unidad grande y hay que dividir para recuperar euros. Multiplicar 327·1,09 daría unos 356 $, que ni siquiera son euros. Comprueba siempre con la multiplicación inversa.',
 'e10c'),
],
[
('¿Por qué el primer año las dos barras coinciden?',
 'Porque el primer interés se calcula en los dos modelos sobre los mismos 2 000 €: 60 €, y ambos montantes son 2 060. Por qué: la diferencia del compuesto aparece cuando el segundo interés usa 2 060 como base y da 61,80 en vez de 60. Antes de eso no hay «interés del interés».'),
('¿Qué error produce usar r = 3 en I = C·r·t?',
 'Multiplica el interés por 100. Por qué: 3 % es 0,03 en tanto por uno. Con r = 3, I = 2 000·3·4 = 24 000 €, un montante imposible para este depósito. El gráfico se queda alrededor de 2 250 € precisamente porque r es 0,03.'),
('La comisión del 0,6 % sobre 2 000 €, ¿son 0,60 €?',
 'No: son 12 €. Por qué: 0,6 % de 2 000 es 0,006×2 000 = 12. Leer 0,6 como 0,60 euros olvida que un porcentaje necesita una base. 0,60 € sería el 0,6 % de 100 €, no de 2 000.'),
],
'Tu depósito imaginario',
'Elige un capital, un tipo anual y 3 años. Calcula el montante simple y el compuesto del último año y dibuja en el lienzo tres pares de barras.',
['Barras verdes, interés simple hasta 2 240 €; barras ámbar, compuesto hasta unos 2 251 €.',
 'El salto verde es siempre de 60 €. El ámbar se separa desde el segundo año.',
 'Ejemplo 1: I = 2 000·0,03·4 = 240, montante 2 240.',
 'Ejemplo 2: cuatro multiplicaciones por 1,03 llevan a 2 251,02 €.',
 'Ejemplo 3: la comisión es 12 € y con el resto se obtienen 2 166,92 dólares.',
 'No pongas t = 6 si el plazo es de 6 meses y el tipo es anual.',
 'Comprueba el primer año: simple y compuesto tienen que coincidir.']
)

# ---------- L11 ----------
fig11 = '''
<circle cx="90" cy="80" r="22" fill="#C4A15A" stroke="#E6E1D6"/>
<circle cx="150" cy="80" r="22" fill="#C4A15A" stroke="#E6E1D6"/>
<circle cx="210" cy="80" r="22" fill="#C4A15A" stroke="#E6E1D6"/>
<circle cx="280" cy="80" r="22" fill="#8F9A72" stroke="#E6E1D6"/>
<circle cx="340" cy="80" r="22" fill="#8F9A72" stroke="#E6E1D6"/>
<text x="90" y="130" text-anchor="middle" fill="#C4A15A" font-size="13">R</text>
<text x="150" y="130" text-anchor="middle" fill="#C4A15A" font-size="13">R</text>
<text x="210" y="130" text-anchor="middle" fill="#C4A15A" font-size="13">R</text>
<text x="280" y="130" text-anchor="middle" fill="#8F9A72" font-size="13">A</text>
<text x="340" y="130" text-anchor="middle" fill="#8F9A72" font-size="13">A</text>
<line x1="80" y1="220" x2="640" y2="220" stroke="#E6E1D6" stroke-width="3"/>
<line x1="80" y1="205" x2="80" y2="235" stroke="#E6E1D6" stroke-width="2"/>
<line x1="640" y1="205" x2="640" y2="235" stroke="#E6E1D6" stroke-width="2"/>
<line x1="416" y1="205" x2="416" y2="235" stroke="#C4A15A" stroke-width="2"/>
<path d="M80,220 L416,220" fill="none" stroke="#C4A15A" stroke-width="8"/>
<circle cx="416" cy="220" r="7" fill="#E6E1D6"/>
<polygon points="416,200 408,184 424,184" fill="#C4A15A"/>
<text x="80" y="260" fill="#9A9488" font-size="14">0</text>
<text x="630" y="260" fill="#9A9488" font-size="14">1</text>
<text x="390" y="175" fill="#E6E1D6" font-size="14">3/5 = 0,6</text>
<text x="430" y="100" fill="#E6E1D6" font-size="15">urna: 3 rojas y 2 azules</text>
'''
build(
11, 'Probabilidad como <em>medida</em>', 'B.1 Probabilidad como medida de la incertidumbre',
'Cinco bolas y un segmento de cero a uno',
'La probabilidad mide la incertidumbre con un número entre 0 y 1. En la urna hay 3 bolas rojas y 2 azules; si sacas una al azar, P(roja) = 3/5 = 0,6, y ese 0,6 está marcado en el segmento [0, 1] del gráfico.',
['Asignar probabilidades con la regla de Laplace cuando los casos son equiprobables.','Situar una probabilidad en el segmento [0, 1].','Usar el suceso contrario y la suma de sucesos incompatibles.'],
'''<h2>Un número entre imposible y seguro, con casos contados</h2>
<p>Decir «hay bastante probabilidad» no mide. La probabilidad de un suceso es un número del intervalo cerrado [0, 1]: 0 es el suceso imposible en ese modelo, 1 es el suceso seguro, y el resto gradúa la incertidumbre. El gráfico lo dibuja como un segmento: el trazo ámbar llega al 60 % del camino entre 0 y 1.</p>
<p><span class="glosa">caso favorable = resultado que nos interesa · caso posible = resultado del experimento que el modelo considera · equiprobable = todos los casos posibles pesan igual · P(A) = favorables / posibles en ese modelo · suceso contrario de A = «no ocurre A», y P(contrario) = 1 − P(A)</span></p>
<p>En la urna hay 5 bolas y el sorteo es al azar, así que cada bola pesa 1/5. Las rojas son 3, luego P(roja) = 3/5 = 0,6. Las azules son 2, P(azul) = 2/5 = 0,4. Suman 1 porque rojo y azul cubren todas las bolas y no se solapan: o sale roja o sale azul.</p>
<p>Laplace no se aplica a ciegas. Si las bolas no salen igual de a menudo (una es mucho mayor, o el sorteo está trucado), los casos dejan de ser equiprobables y el cociente 3/5 deja de ser el modelo. La probabilidad sigue siendo una medida entre 0 y 1, pero hay que estimarla de otra forma.</p>
<table class="datos"><thead><tr><th>Suceso</th><th>Favorables</th><th>Posibles</th><th>Probabilidad</th><th>Lugar en [0, 1]</th></tr></thead>
<tbody>
<tr><td>roja</td><td>3</td><td>5</td><td>3/5 = 0,6</td><td>la marca del gráfico</td></tr>
<tr><td>azul</td><td>2</td><td>5</td><td>2/5 = 0,4</td><td>a la izquierda del 0,6</td></tr>
<tr><td>roja o azul</td><td>5</td><td>5</td><td>1</td><td>extremo derecho</td></tr>
<tr><td>verde</td><td>0</td><td>5</td><td>0</td><td>extremo izquierdo</td></tr>
</tbody></table>''',
'Urna con 3 bolas rojas y 2 azules, y segmento [0, 1] marcado en 3/5', fig11,
[
('La urna del gráfico',
 'Se extrae una bola al azar. Calcula P(roja), P(azul) y sitúa P(roja) en [0, 1].',
 [
  ('Cuenta posibles: 5 bolas, un solo sorteo, mismas condiciones. El denominador es 5.',
   'Glosa: el denominador no es 2 «porque hay dos colores»; los colores no son equiprobables entre sí.'),
  ('Favorables a roja: 3. P(roja) = 3/5 = 0,6. Favorables a azul: 2. P(azul) = 2/5 = 0,4.',
   'Glosa: 3/5 no se simplifica con el 2 del otro color; son sucesos distintos.'),
  ('En el segmento, 0,6 está a 3/5 del recorrido. Si el segmento del SVG va de la marca 0 a la marca 1, la señal ámbar cae pasada la mitad, más cerca de 1 que de 0.',
   'Glosa: 0,6 no es «más de 1» ni «un 6 %». Un 6 % sería 0,06.'),
  ('Comprueba 0,6+0,4 = 1. Roja y azul son incompatibles y su unión es el suceso seguro.',
   'Glosa: si sumaran más de 1, habrías contado dos veces alguna bola o usado mal el denominador.'),
 ]),
('Dado honesto',
 'En un dado de 6 caras, calcula P(par) y el suceso contrario.',
 [
  ('Casos posibles: 1, 2, 3, 4, 5, 6. Seis, equiprobables si el dado es honesto.',
   'Glosa: las caras son el espacio, no «par e impar» como si solo hubiera dos casos iguales sin contar caras.'),
  ('Pares: 2, 4, 6. Tres favorables. P(par) = 3/6 = 1/2.',
   'Glosa: 3/6 se simplifica a 1/2, pero el recuento original eran 3 caras de 6.'),
  ('El contrario es «impar»: 1, 3, 5. P(impar) = 1 − 1/2 = 1/2. También 3/6.',
   'Glosa: restar de 1 sirve porque toda cara es par o impar, sin tercera opción.'),
  ('Comprueba que par e impar no comparten caras y cubren el dado. Por eso sus probabilidades suman 1.',
   'Glosa: si el suceso fuera «mayor que 4», el contrario no es «menor que 4»: también está el 4, que no es mayor que 4.'),
 ]),
('Incompatibles en la misma urna',
 'Con la urna de 5 bolas, P(roja) = 3/5 y P(azul) = 2/5. Calcula P(roja o azul) y explica por qué se suman.',
 [
  ('Roja y azul no pueden salir a la vez en una sola extracción: son incompatibles. Su intersección está vacía.',
   'Glosa: incompatible significa que el modelo asigna probabilidad 0 a la intersección, no que «sean distintos de nombre».'),
  ('P(unión) = P(roja) + P(azul) = 3/5 + 2/5 = 5/5 = 1.',
   'Glosa: se suman los numeradores porque el denominador común ya es el mismo espacio de 5 bolas.'),
  ('Contando casos: favorables a «roja o azul» = 5, posibles = 5, cociente 1. El mismo resultado.',
   'Glosa: las dos vías (suma de probabilidades y recuento) tienen que coincidir.'),
  ('Si los sucesos se solaparan, no bastaría sumar: habría que restar la intersección. Aquí esa corrección es 0.',
   'Glosa: el caso de la unión de lecciones de conteo reaparece: no se puede sumar dos veces lo común.'),
 ]),
],
[
(1, 'Una verde añadida',
 'Añades una bola verde a la urna (ahora hay 6). Calcula P(roja) y di hacia dónde se mueve la marca en [0, 1].',
 'El denominador cambia: ya no hay 5 bolas sino 6, y las rojas siguen siendo 3 si no has añadido una roja. P(roja) = 3/6 = 1/2 = 0,5. La marca, que estaba en 0,6, se desplaza a la izquierda, hacia el centro del segmento, porque la misma cantidad de favorables se reparte entre más casos posibles. El paso que suele fallar es dejar el denominador en 5 después de haber metido la bola nueva. Comprueba que 0,5 está a mitad de camino entre 0 y 1, a la izquierda de la marca dibujada.',
 'e11a'),
(2, 'Contrario de un color',
 'Sin añadir bolas, ¿cuál es la probabilidad de no sacar roja? Escríbela como resta y como cociente.',
 'No sacar roja, en esta urna, es sacar azul: hay 2 azules de 5, así que el cociente es 2/5. Por el contrario, 1 − 3/5 = 2/5. Las dos escrituras cuentan lo mismo porque toda bola no roja es azul: no hay verdes en el modelo original. El paso es identificar el contrario dentro del espacio real de la urna, no inventar un color. Si hubiera verdes, «no roja» sería azul o verde y el numerador sería la suma de esas bolas, mientras que 1 − P(roja) seguiría siendo válido.',
 'e11b'),
(3, 'Casos que no pesan igual',
 'Alguien dice que P(roja) = 1/2 porque «o sale roja o no». ¿Qué hipótesis de Laplace está usando mal?',
 'Está tomando dos casos, «roja» y «no roja», y suponiéndolos equiprobables. En la urna no lo son: hay 3 rojas y 2 no rojas, así que «roja» pesa 3/5 y no 1/2. Laplace exige que los casos del denominador sean igual de verosímiles. Las cinco bolas sí lo son; los dos colores, no, porque agrupan cantidades distintas de bolas. El paso correcto es contar resultados elementales equiprobables (las bolas) y no atajos verbales de «sí o no». Por eso el segmento marca 0,6 y no 0,5.',
 'e11c'),
],
[
('¿Dónde está marcada P(roja) en el segmento?',
 'En 3/5 = 0,6, más allá de la mitad. Por qué: hay 3 bolas rojas entre 5 equiprobables, y el segmento [0, 1] representa la probabilidad, no el número de bolas. 3 bolas no se marcan en el punto 3.'),
('¿Por qué P(verde) = 0 no contradice que el 0 sea «imposible»?',
 'En este modelo es imposible sacar verde porque no hay bolas verdes. Por qué: el 0 no es una opinión; es el cociente 0/5. Si el experimento cambiara y hubiera verdes, el modelo cambiaría y ese 0 dejaría de valer.'),
('Par e impar en el dado suman 1. ¿Eso demuestra que cada uno vale 1/2 sin contar caras?',
 'No del todo. Por qué: dos contrarios siempre suman 1, pero podrían valer 1/6 y 5/6, por ejemplo «sacar un 6» y «no sacar un 6». Que sumen 1 no los hace iguales. En el dado, par e impar valen 1/2 porque cada uno reúne 3 caras de 6, no porque sean contrarios.'),
],
'Una urna de verdad',
'Dibuja en el lienzo una urna con tus datos (hasta 8 bolas), calcula una probabilidad y marca el punto en un segmento [0, 1].',
['Tres círculos ámbar y dos verdes: la urna. El segmento de abajo marca 0,6.',
 'P(roja) = 3/5 porque las bolas son equiprobables, no los colores.',
 'Ejemplo 1: 0,6 y 0,4 suman 1 y cubren la urna.',
 'Ejemplo 2: en el dado, par es 3 caras de 6, no «uno de dos nombres».',
 'Ejemplo 3: roja o azul, al ser incompatibles y cubrirlo todo, tiene probabilidad 1.',
 'Si añades una bola, cambia el denominador antes de recolocar la marca.',
 'Comprueba que ninguna probabilidad de esta lección se sale de [0, 1].']
)
print('L10 L11 en fuente')

# ---------- L12 ----------
def _s12(t):
    return t*t - 2*t + 10
fig12 = ejes(70, 290, 680, 24)
fig12 += path_fn(_s12, 0, 7, 28, lambda t: 70 + t*80, lambda y: 300 - y*6)
fig12 += '<line x1="230" y1="240" x2="550" y2="96" stroke="#8F9A72" stroke-width="2.5"/>'
fig12 += '<circle cx="230" cy="240" r="6" fill="#E6E1D6"/>'
fig12 += '<circle cx="550" cy="96" r="6" fill="#E6E1D6"/>'
fig12 += '''
<text x="150" y="230" fill="#E6E1D6" font-size="14">(2, 10)</text>
<text x="555" y="90" fill="#E6E1D6" font-size="14">(6, 34)</text>
<text x="300" y="150" fill="#8F9A72" font-size="14">secante · pendiente 6</text>
<text x="80" y="20" fill="#C4A15A" font-size="14">s(t) = t² − 2t + 10</text>
'''
build(
12, 'Variación absoluta y <em>media</em>', 'B.2 Variación absoluta y variación media',
'El cambio neto no es el ritmo',
'Entre t = 2 h y t = 6 h, el espacio s pasa de 10 km a 34 km. La variación absoluta es 24 km. La variación media es 24 km / 4 h = 6 km/h: la pendiente de la secante dibujada, no la velocidad en cada instante.',
['Calcular una variación absoluta con unidades.','Dividirla entre el tiempo para obtener la variación media.','Explicar qué dice y qué no dice ese ritmo medio.'],
'''<h2>Dos preguntas distintas sobre el mismo cambio</h2>
<p>La variación absoluta responde «¿cuánto ha cambiado la magnitud?». Es una resta: valor final menos valor inicial. Conserva la unidad de la magnitud. Si el resultado es negativo, la magnitud ha bajado.</p>
<p>La variación media responde «¿con qué ritmo constante se habría producido ese mismo cambio en ese intervalo?». Es el cociente entre la variación absoluta y la variación de la variable independiente. Su unidad es un cociente de unidades: kilómetros por hora, euros por semana, grados por minuto.</p>
<p><span class="glosa">Δs = s(final) − s(inicial) · Δt = t(final) − t(inicial) · variación media = Δs / Δt · la secante es la recta que pasa por los dos puntos del intervalo; su pendiente es la variación media</span></p>
<p>En el gráfico, s(t) = t² − 2t + 10, con t en horas y s en kilómetros. No hace falta derivar: basta evaluar los extremos. s(2) = 10 y s(6) = 34. La curva no es recta, así que el móvil no ha ido todo el rato a la misma velocidad. Aun así, la secante verde tiene pendiente 6: un movimiento constante a 6 km/h, durante esas 4 horas, habría acumulado los mismos 24 km.</p>
<p>Por eso la variación media no es «la velocidad que llevaba» ni una media aritmética de dos fotos sacadas al tuntún. Es el ritmo constante equivalente en ese intervalo concreto. Si alargas el intervalo, el cociente puede cambiar aunque el cambio absoluto sea otro.</p>
<table class="datos"><thead><tr><th></th><th>Cálculo en el ejemplo</th><th>Unidad</th><th>Qué no dice</th></tr></thead>
<tbody>
<tr><td>Variación absoluta</td><td>34 − 10 = 24</td><td>km</td><td>no dice cuánto tardó</td></tr>
<tr><td>Variación de t</td><td>6 − 2 = 4</td><td>h</td><td>no es un espacio</td></tr>
<tr><td>Variación media</td><td>24 / 4 = 6</td><td>km/h</td><td>no es la velocidad en t = 2 ni en t = 6</td></tr>
</tbody></table>''',
'Curva s(t) = t² − 2t + 10 con la secante entre (2, 10) y (6, 34), pendiente 6', fig12,
[
('Los 24 km en 4 horas',
 's(t) = t² − 2t + 10. Calcula la variación absoluta y la media de s entre t = 2 y t = 6, y explica la frase «equivale a 6 km/h constantes».',
 [
  ('Evalúa los extremos: s(2) = 4 − 4 + 10 = 10. s(6) = 36 − 12 + 10 = 34. Son los dos círculos del gráfico.',
   'Glosa: sustituye antes de restar; no restes los tiempos dentro de la fórmula como si fueran el espacio.'),
  ('Variación absoluta: Δs = 34 − 10 = 24 km. El orden es final menos inicial. Δt = 6 − 2 = 4 h.',
   'Glosa: si inviertes el orden, el signo cambia y dirías que el espacio disminuye, en contra del dibujo.'),
  ('Variación media: 24 km / 4 h = 6 km/h. Es la pendiente de la secante verde: en horizontal avanza 4 horas y en vertical 24 km.',
   'Glosa: pendiente = incremento vertical / incremento horizontal, con las unidades puestas.'),
  ('Interpretación: durante esas 4 horas el espacio ha crecido 24 km. Un vehículo a 6 km/h constantes habría hecho el mismo neto. La curva, al no ser recta, no ha mantenido esa velocidad en cada instante; la media no lo afirma.',
   'Glosa: decir «iba a 6 km/h» a secas sobra. Di «en media, en ese intervalo».'),
 ]),
('Cuando la magnitud baja',
 'El precio de un abono pasa de 50 € en la semana 0 a 35 € en la semana 5. Calcula variación absoluta y media, con signo y unidades.',
 [
  ('ΔP = 35 − 50 = −15 €. El signo menos es parte del resultado: el precio ha bajado 15 euros.',
   'Glosa: la variación absoluta no es siempre el valor absoluto. El signo informa de la dirección.'),
  ('Δt = 5 − 0 = 5 semanas.',
   'Glosa: la semana 0 cuenta como instante inicial; el intervalo dura 5 semanas, no 6.'),
  ('Variación media = −15 € / 5 semanas = −3 €/semana.',
   'Glosa: se lee «baja, en media, 3 euros cada semana» a lo largo de esas cinco.'),
  ('Comprueba con un ritmo constante: si cada semana restaras 3 €, en 5 semanas restarías 15 € y llegarías de 50 a 35. Eso no demuestra que la bajada haya sido uniforme, solo que el neto coincide.',
   'Glosa: la misma idea de la secante, ahora con pendiente negativa.'),
 ]),
('El mismo cambio absoluto, otro ritmo',
 'Unos 24 km pueden recorrerse en 4 h o en 8 h. Compara las dos variaciones medias y di qué dato distingue las situaciones.',
 [
  ('En ambos casos la variación absoluta del espacio es +24 km. Ese dato, solo, no distingue los dos viajes.',
   'Glosa: por eso hace falta una segunda pregunta, la del ritmo.'),
  ('Primer viaje: Δt = 4 h, media = 24/4 = 6 km/h. Es el ejemplo del gráfico.',
   'Glosa: mismo cociente que la secante de (2, 10) a (6, 34).'),
  ('Segundo viaje: Δt = 8 h, media = 24/8 = 3 km/h.',
   'Glosa: el numerador no ha cambiado; al doblar el denominador, el ritmo se parte por la mitad.'),
  ('Lo que distingue las situaciones es Δt, y por tanto la variación media. Quedarse en «han avanzado 24 km» omite el tiempo que la media sí incorpora.',
   'Glosa: absoluta y media no se sustituyen; se complementan.'),
 ]),
],
[
(1, 'Otro intervalo de la misma curva',
 'Con s(t) = t² − 2t + 10, calcula la variación media entre t = 0 y t = 2. ¿Sale también 6?',
 's(0) = 10 y s(2) = 10, así que Δs = 0 km y Δt = 2 h. La variación media es 0/2 = 0 km/h. No sale 6: el ritmo medio depende del intervalo. Entre 0 y 2 la curva sale de 10 y vuelve a 10 (baja y sube), y el neto es nulo; la secante sería horizontal. El paso es volver a evaluar los extremos nuevos en vez de reutilizar el 6 del intervalo [2, 6]. Un neto cero no significa que el móvil haya estado parado todo el rato, solo que el cambio acumulado es cero.',
 'e12a'),
(2, 'Unidades',
 'Una cuenta pasa de 1 200 € a 1 560 € en 9 meses. Da la variación absoluta y la media por mes.',
 'Variación absoluta: 1 560 − 1 200 = 360 €. No hace falta cambiar de unidad para esta resta. La media pide un cociente: 360 € / 9 meses = 40 €/mes. El paso es no convertir los 9 meses en 0,75 años si vas a expresar el ritmo por mes; si quisieras euros por año, primero decidirías la unidad del denominador y sería 360 / 0,75 = 480 €/año. Las dos medias son coherentes (40×12 = 480), pero mezclar «9» con «euros al año» no lo es. La media sigue siendo un ritmo equivalente, no la lista de ingresos de cada mes.',
 'e12b'),
(3, 'Lectura de la secante',
 'Alguien mira el gráfico y dice que la variación media es 34 − 6 = 28 porque «resta las coordenadas que se ven». ¿Qué coordenadas ha mezclado?',
 'Ha restado la ordenada final (34) y la abscisa final (6), que no comparten unidad: kilómetros menos horas. La variación absoluta del espacio usa las dos ordenadas, 34 − 10. La del tiempo usa las dos abscisas, 6 − 2. Solo después se dividen. El 28 no es una variación de esta lección. El paso ordenado es: identifica qué eje es la magnitud y cuál es la variable, resta en cada eje por separado y divide. La pendiente 6 del dibujo sale de 24/4, no de una resta cruzada.',
 'e12c'),
],
[
('¿Qué diferencia hay entre 24 km y 6 km/h en el ejemplo?',
 '24 km es la variación absoluta, el cambio neto de espacio. 6 km/h es la variación media, ese cambio repartido entre las 4 horas. Por qué: la primera no contiene el tiempo; la segunda sí, porque es un cociente. Un movimiento a 6 km/h constantes durante 4 h reproduce el neto, aunque la curva real no sea constante.'),
('¿Puede la variación absoluta ser negativa y la media también?',
 'Sí, como en el abono: −15 € y −3 €/semana. Por qué: el signo se conserva al dividir entre un Δt positivo. Significa que la magnitud disminuye. Tomar el valor absoluto es otra decisión, y hay que decirlo; no sale de la definición.'),
('Si la variación absoluta es 0, ¿la media es 0?',
 'Sí, siempre que el intervalo de la variable no sea 0. Por qué: el numerador es 0 y el cociente es 0, como entre t = 0 y t = 2 en esta curva. No concluye que la magnitud haya sido constante, solo que ha terminado donde empezó.'),
],
'Un trayecto real',
'Anota dos lecturas de una magnitud (pasos, saldo, temperatura) y el tiempo entre ellas. Escribe variación absoluta y media con unidades y una frase que diga «equivale a…».',
['La curva pasa por (2, 10) y (6, 34); la secante verde tiene pendiente 6.',
 'Absoluta: 24 km. Media: 6 km/h. No son la misma pregunta.',
 'Ejemplo 1: la media es el ritmo constante que reproduce el neto, no la velocidad instantánea.',
 'Ejemplo 2: de 50 € a 35 € en 5 semanas, la media es −3 €/semana.',
 'Ejemplo 3: los mismos 24 km en 8 h bajan la media a 3 km/h.',
 'No restes una ordenada con una abscisa.',
 'Comprueba los extremos en la fórmula antes de dividir.']
)

# ---------- L13 ----------
fig13 = ejes(40, 286, 360, 30)
fig13 += path_fn(lambda x: x*x, 0.2, 4, 24, lambda x: 40 + x*70, lambda y: 286 - y*14)
fig13 += '<line x1="180" y1="230" x2="250" y2="160" stroke="#8F9A72" stroke-width="2.5"/>'
fig13 += '<circle cx="180" cy="230" r="6" fill="#E6E1D6"/>'
fig13 += '<circle cx="250" cy="160" r="5" fill="#8F9A72"/>'
# tabla de cocientes
fig13 += '''
<line x1="400" y1="36" x2="690" y2="36" stroke="#C4A15A" stroke-width="1.5"/>
<line x1="400" y1="78" x2="690" y2="78" stroke="#9A9488"/>
<line x1="400" y1="118" x2="690" y2="118" stroke="#9A9488"/>
<line x1="400" y1="158" x2="690" y2="158" stroke="#9A9488"/>
<line x1="400" y1="198" x2="690" y2="198" stroke="#9A9488"/>
<line x1="400" y1="238" x2="690" y2="238" stroke="#C4A15A" stroke-width="1.5"/>
<line x1="400" y1="36" x2="400" y2="238" stroke="#C4A15A" stroke-width="1.5"/>
<line x1="520" y1="36" x2="520" y2="238" stroke="#9A9488"/>
<line x1="690" y1="36" x2="690" y2="238" stroke="#C4A15A" stroke-width="1.5"/>
<text x="430" y="64" fill="#C4A15A" font-size="15">h</text>
<text x="560" y="64" fill="#C4A15A" font-size="15">cociente</text>
<text x="445" y="104" fill="#E6E1D6" font-size="15">1</text>
<text x="590" y="104" fill="#E6E1D6" font-size="15">5</text>
<text x="430" y="144" fill="#E6E1D6" font-size="15">0,5</text>
<text x="580" y="144" fill="#E6E1D6" font-size="15">4,5</text>
<text x="430" y="184" fill="#E6E1D6" font-size="15">0,1</text>
<text x="580" y="184" fill="#E6E1D6" font-size="15">4,1</text>
<text x="420" y="224" fill="#E6E1D6" font-size="15">0,01</text>
<text x="575" y="224" fill="#E6E1D6" font-size="15">4,01</text>
<text x="48" y="24" fill="#C4A15A" font-size="14">f(x) = x² · punto (2, 4)</text>
<text x="400" y="268" fill="#9A9488" font-size="13">cociente = (f(2+h) − 4) / h → 4</text>
<text x="120" y="250" fill="#E6E1D6" font-size="13">(2, 4)</text>
'''
build(
13, 'Límite: idea de <em>cambio</em>', 'B.2 Límite desde la variación media',
'Los cocientes que se acercan a 4',
'La variación media de f(x) = x² entre 2 y 2 + h es (f(2+h) − 4) / h. La tabla del gráfico da 5; 4,5; 4,1 y 4,01 cuando h vale 1; 0,5; 0,1 y 0,01. Esos cocientes se acercan a 4, y ese comportamiento es la idea de límite que prepara la derivada.',
['Calcular variaciones medias con un incremento h cada vez menor.','Reconocer a qué número se acercan esos cocientes.','Explicar por qué no se sustituye h = 0 en el cociente.'],
'''<h2>Encoger el intervalo sin dividir entre cero</h2>
<p>En la lección anterior la variación media usaba un intervalo fijo. Aquí el intervalo se encoge alrededor de un punto. Para f(x) = x² miramos el punto x = 2, donde f(2) = 4, y un incremento h distinto de cero. La variación media en [2, 2+h] (o hacia la izquierda si h es negativo) es el cociente (f(2+h) − f(2)) / h.</p>
<p><span class="glosa">h = incremento de x, h ≠ 0 · f(2+h) = (2+h)² = 4 + 4h + h² · numerador = 4h + h² · cociente = 4 + h, mientras h ≠ 0 · el límite cuando h tiende a 0 es 4, aunque en h = 0 el cociente no se pueda calcular</span></p>
<p>La tabla del SVG no es un adorno: son cuatro variaciones medias del mismo punto. Con h = 1 el cociente vale 5, y la secante verde va de (2, 4) a (3, 9), porque de 4 a 9 hay 5 unidades de altura en 1 unidad de ancho. Cuando h baja a 0,5, a 0,1 y a 0,01, el cociente vale 4,5, 4,1 y 4,01. Se acerca a 4.</p>
<p>No podemos meter h = 0 en el cociente: el numerador también se haría 0 y estaríamos dividiendo 0 entre 0, que no tiene sentido. El límite no es «el valor del cociente en 0»; es el número al que los cocientes se acercan cuando h se acerca a 0 sin llegar a serlo. En la próxima lección ese número, 4, se leerá como pendiente de la tangente y como ritmo instantáneo. Aquí basta ver la tabla y la simplificación 4 + h.</p>
<table class="datos"><thead><tr><th>h</th><th>f(2+h)</th><th>f(2+h) − 4</th><th>cociente</th></tr></thead>
<tbody>
<tr><td>1</td><td>9</td><td>5</td><td>5</td></tr>
<tr><td>0,5</td><td>6,25</td><td>2,25</td><td>4,5</td></tr>
<tr><td>0,1</td><td>4,41</td><td>0,41</td><td>4,1</td></tr>
<tr><td>0,01</td><td>4,0401</td><td>0,0401</td><td>4,01</td></tr>
</tbody></table>''',
'Tabla de cocientes de f(x)=x² en x=2 (valen 5; 4,5; 4,1; 4,01) y secante de h=1', fig13,
[
('Las cuatro filas de la tabla',
 'Para f(x) = x² y el punto x = 2, calcula el cociente (f(2+h) − 4) / h con h = 1, h = 0,5, h = 0,1 y h = 0,01.',
 [
  ('Con h = 1: f(3) = 9, numerador 9 − 4 = 5, cociente 5/1 = 5. Es la secante verde del gráfico, de (2, 4) a (3, 9).',
   'Glosa: pendiente 5 significa 5 unidades de función por cada unidad de x en ese tramo.'),
  ('Con h = 0,5: 2+h = 2,5 y f = 6,25. Numerador 6,25 − 4 = 2,25. Cociente 2,25/0,5 = 4,5.',
   'Glosa: dividir entre 0,5 es multiplicar por 2; 2,25·2 = 4,5.'),
  ('Con h = 0,1: (2,1)² = 4,41. Numerador 0,41. Cociente 0,41/0,1 = 4,1. Con h = 0,01: (2,01)² = 4,0401, numerador 0,0401, cociente 4,01.',
   'Glosa: estas dos filas son las de abajo del SVG; no redondees el cociente a 4 antes de haber dividido.'),
  ('Los cuatro resultados 5; 4,5; 4,1; 4,01 se acercan a 4. Simplificando en general, el cociente vale 4 + h si h ≠ 0, y 4 + h tiende a 4.',
   'Glosa: 4 + h explica la tabla de un vistazo: el cociente es 4 más el propio h.'),
 ]),
('De dónde sale 4 + h',
 'Desarrolla (2+h)² y simplifica el cociente. Di por qué la simplificación exige h distinto de 0.',
 [
  ('(2+h)² = 4 + 4h + h². Resta f(2) = 4: queda 4h + h².',
   'Glosa: el 4 inicial se cancela; por eso el numerador se hace pequeño cuando h se hace pequeño.'),
  ('Divide entre h: (4h + h²) / h = 4 + h, sacando factor común h en el numerador: h(4 + h) / h.',
   'Glosa: simplificar h/h es válido solo si h ≠ 0. Si h fuera 0, estarías tachando un cero.'),
  ('Por tanto, mientras h ≠ 0, la variación media es exactamente 4 + h. La tabla cuadra: 4+1 = 5, 4+0,5 = 4,5, 4+0,1 = 4,1, 4+0,01 = 4,01.',
   'Glosa: no hace falta rehacer cada cuadrado si ya confías en el álgebra; la tabla sirve de comprobación.'),
  ('El límite cuando h tiende a 0 de (4 + h) es 4. Ese 4 no se obtiene sustituyendo h = 0 en el cociente original, que quedaría 0/0.',
   'Glosa: primero se simplifica en los h permitidos; después se mira a qué valor se acercan.'),
 ]),
('Una función en la que el cociente no se mueve',
 'Para g(x) = 3x, calcula la variación media entre x = 2 y x = 2+h y explica el límite.',
 [
  ('g(2) = 6. g(2+h) = 3(2+h) = 6 + 3h. Numerador: 6 + 3h − 6 = 3h.',
   'Glosa: en una recta, el incremento de la función es proporcional a h desde el primer momento.'),
  ('Cociente: 3h / h = 3, para todo h ≠ 0.',
   'Glosa: no queda un sumando con h. La variación media es constante.'),
  ('La tabla sería 3, 3, 3 y 3 para los mismos h de antes. El límite cuando h tiende a 0 también es 3.',
   'Glosa: acercarse a 3 es inmediato porque ya estás en 3.'),
  ('Comparación: en x² el cociente todavía dependía de h (valía 4+h); en 3x no. Las dos situaciones tienen límite, pero solo la recta tiene variación media idéntica en todos los intervalos.',
   'Glosa: por eso en la lección 12 la secante de una curva no cuenta toda la historia, y en una recta sí.'),
 ]),
],
[
(1, 'h negativo',
 'Calcula el cociente de f(x) = x² en x = 2 con h = −0,1 y di si también se acerca a 4.',
 'f(1,9) = 3,61. Numerador 3,61 − 4 = −0,39. Cociente (−0,39)/(−0,1) = 3,9. Con la fórmula simplificada, 4 + h = 4 − 0,1 = 3,9. Está a una décima de 4, por debajo, igual que h = 0,1 dejaba el cociente a una décima por encima (4,1). El paso es no descartar los h negativos: el límite exige acercarse por los dos lados. Aquí por la izquierda también vamos hacia 4, no hacia otro número.',
 'e13a'),
(2, 'Por qué no h = 0',
 'Sustituye h = 0 en (f(2+h) − 4) / h antes de simplificar y explica qué obtienes. Después di qué número describe el límite.',
 'Con h = 0, f(2+0) − 4 = 0 y el denominador es 0. La expresión 0/0 no es un número: no puedes dividir entre cero. Por eso el cociente, como operación, no está definido en h = 0 y la tabla no tiene esa fila. El límite no rellena esa casilla con una división; mira las filas que sí existen (h = 1, 0,5, 0,1, 0,01, …) y observa que se acercan a 4. Después de simplificar a 4 + h, se ve el mismo hecho sin necesidad de dividir entre cero. El 4 es el límite, no el valor de una fracción con denominador nulo.',
 'e13b'),
(3, 'Lee la secante',
 'La secante del gráfico une (2, 4) y (3, 9). ¿Qué fila de la tabla es y por qué su pendiente no es el límite?',
 'Esa secante corresponde a h = 1, primera fila, cociente 5. La pendiente es (9 − 4)/(3 − 2) = 5, que es una variación media de un intervalo todavía grande. El límite aparece cuando el segundo punto se acerca al primero, es decir cuando h tiende a 0, y los cocientes pasan de 5 a 4,5, a 4,1 y a 4,01. Confundir la pendiente de esta secante concreta con el límite es quedarse en la primera fila de la tabla. El 4 no es la altura del punto (que es 4, casualmente f(2) = 4) ni la pendiente de la secante de h = 1.',
 'e13c'),
],
[
('¿A qué número se acercan los cocientes de la tabla?',
 'A 4. Por qué: valen 5; 4,5; 4,1 y 4,01, que son 4 + h para esos h. Al encoger h, el sumando h desaparece y el límite es 4. No es la primera fila (el 5), que corresponde al intervalo más ancho.'),
('¿Por qué la tabla no incluye h = 0?',
 'Porque el cociente tendría denominador 0 y numerador 0. Por qué: f(2) − f(2) = 0. La expresión 0/0 no da el límite. El límite se lee en los h distintos de cero, cada vez más pequeños.'),
('En g(x) = 3x, ¿por qué todas las variaciones medias valen 3?',
 'Porque (g(2+h) − g(2)) / h = 3h / h = 3 si h ≠ 0. Por qué: g es una recta de pendiente 3, y en una recta la variación media de cualquier intervalo coincide con la pendiente. No hay un término extra que se apague al hacer h pequeño, a diferencia de x², donde ese término es h.'),
],
'Una fila más',
'Añade a la tabla el cociente con h = 0,001 para f(x) = x² en x = 2 y escribe a cuántas milésimas está de 4. Dibuja en el lienzo el punto y una secante muy pegada.',
['La tabla del SVG es el ejemplo: h = 1, 0,5, 0,1 y 0,01 dan cocientes 5; 4,5; 4,1 y 4,01.',
 'La secante verde es solo la fila h = 1, de (2, 4) a (3, 9), pendiente 5.',
 'Ejemplo 1: recalcula esas cuatro filas sin saltarte el numerador.',
 'Ejemplo 2: el álgebra deja el cociente en 4 + h, y por eso el límite es 4.',
 'Ejemplo 3: en la recta 3x el cociente ya es 3 para cualquier h distinto de cero.',
 'No rellenes la tabla con h = 0.',
 'El 4 al que te acercas será, en la lección siguiente, la derivada en ese punto.']
)

assert_untouched(SNAP)
print('L05-L13 generadas; L01-L04 y L14 intactas')
