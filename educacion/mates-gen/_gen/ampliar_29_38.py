# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'/workspace/lesvencimos/staging/bach1/mates-gen/_gen')
from chrome import write_dense, ej, md5_pack
from pathlib import Path

def S(title, inner):
    return f'<div class="figura-svg"><svg viewBox="0 0 720 240" role="img"><title>{title}</title><rect width="720" height="240" fill="#161512"/>{inner}</svg></div>'

write_dense(29,'Variables <em>bidimensionales</em>','E.1 Bidimensional','Dos variables a la vez',
'CyL: distribución conjunta, marginales, condicionadas; dependencia e independencia.',
['Leer una tabla de contingencia.','Calcular marginales.','Calcular una probabilidad condicionada desde la tabla.'],
f'''<section class="bloque-cuerpo">
<h2>Tabla conjunta</h2>
<p>Filas = valores de X, columnas = Y. Cada celda es n(X=x,Y=y). Marginales: sumas de filas/columnas. Condicionada: restringe a una fila o columna y renormaliza.</p>
{S('Contingencia','''
<text x="40" y="40" fill="#E6E1D6" font-size="14">   | Y=0 | Y=1 | total</text>
<text x="40" y="80" fill="#8F9A72">X=0|  10 |  20 |  30</text>
<text x="40" y="120" fill="#8F9A72">X=1|  15 |  5  |  20</text>
<text x="40" y="160" fill="#C4A15A">tot |  25 |  25 |  50</text>
''')}
<h2>Ejemplo 1 — marginal</h2>
<ol class="pasos"><li>P(X=0)=30/50=0,6. P(Y=1)=25/50=0,5.</li></ol>
<h2>Ejemplo 2 — conjunta</h2>
<ol class="pasos"><li>P(X=1,Y=0)=15/50=0,3.</li></ol>
<h2>Ejemplo 3 — condicionada</h2>
<ol class="pasos"><li>P(Y=1|X=0)=20/30≈0,667 (solo fila X=0).</li><li>Si P(Y=1|X) ≠ P(Y=1), hay dependencia.</li></ol>
{ej(1,'Marginal','Con la tabla: P(X=1).','20/50=0,4.','e29a')}
{ej(2,'Cond','P(X=0|Y=1).','20/25=0,8. Columna Y=1.','e29b')}
{ej(3,'Indep','Si P(X,Y)=P(X)P(Y) en todas las celdas…','Independencia. Si falla en una, hay dependencia.','e29c')}
{ej(4,'Trampa','¿P(X=0,Y=1) es lo mismo que P(X=0|Y=1)?','No. Conjunta 20/50; condicionada 20/25.','e29d')}
<canvas id="lienzo29" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo29">Borrar</button></div>
</section>''',
[('Marginal','suma fila/columna'),('Condicionada','renormaliza en la fila/col'),('P conjunta vs cond','distintas')],
'Encuesta','Inventa tabla 2×2 de 40 personas; calcula una condicionada.')

write_dense(30,'Regresión, correlación y <em>causalidad</em>','E.1 Regresión','Ajustar sin confundir causas',
'CyL: regresión lineal/cuadrática; correlación ≠ causalidad.',
['Interpretar una nube de puntos.','Distinguir correlación y causalidad.','Leer la idea de recta de ajuste.'],
f'''<section class="bloque-cuerpo">
<h2>Nube y recta</h2>
<p>La recta de regresión resume una tendencia lineal. r mide fuerza y sentido de la relación lineal (−1 a 1). Correlación fuerte no prueba que X cause Y (tercera variable, causalidad inversa, azar).</p>
{S('Nube','''
<circle cx="160" cy="160" r="4" fill="#C4A15A"/><circle cx="220" cy="140" r="4" fill="#C4A15A"/>
<circle cx="300" cy="120" r="4" fill="#C4A15A"/><circle cx="380" cy="90" r="4" fill="#C4A15A"/>
<circle cx="460" cy="70" r="4" fill="#C4A15A"/>
<line x1="120" y1="180" x2="520" y2="40" stroke="#8F9A72" stroke-width="2"/>
<text x="400" y="200" fill="#9A9488" font-size="13">tendencia creciente · no implica causa</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>Horas de estudio vs nota: correlación positiva plausible; aún así hay otros factores.</li></ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>Helados y ahogamientos correlacionan en verano: temperatura es confusora.</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>|r|≈0: poca relación lineal (puede haber otra forma: curva).</li></ol>
{ej(1,'r','r=−0,8: interpreta.','Fuerte y decreciente (lineal). No prueba causa.','e30a')}
{ej(2,'Causalidad','¿r alto implica causa?','No. Hace falta diseño/teoría, no solo r.','e30b')}
{ej(3,'Ajuste','Puntos cerca de una recta creciente: ¿r?','Cercano a +1.','e30c')}
{ej(4,'Cuadrática','Nube en forma de U: ¿basta r lineal?','No: r puede ser bajo aunque haya patrón cuadrático.','e30d')}
<canvas id="lienzo30" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo30">Borrar</button></div>
</section>''',
[('r ∈','[−1,1]'),('Correlación ≠','causalidad'),('Confusora','tercera variable')],
'Contrafáctico','Dibuja una nube con r alto pero causa dudosa; escribe la confusora.')

write_dense(31,'Coeficientes y <em>predicción</em>','E.1 Coeficientes','¿Qué tan fiable es predecir?',
'CyL: coeficientes r y R²; predicción y fiabilidad.',
['Interpretar R² como proporción de varianza explicada (idea).','Usar la recta para predecir dentro del rango.','Desconfiar de extrapolaciones lejanas.'],
f'''<section class="bloque-cuerpo">
<h2>Predicción</h2>
<p>Si ŷ = a + bx, predices y para un x del rango observado. R² cercano a 1: el modelo lineal explica mucho de la variabilidad de y (idea Bach). Extrapolación lejos de los datos: frágil.</p>
{S('Rango','''
<text x="40" y="80" fill="#E6E1D6">Datos x ∈ [1,10] · predecir x=9: OK razonable</text>
<text x="40" y="140" fill="#C4A15A">predecir x=100: extrapolación peligrosa</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>ŷ=2+0,5x. Para x=8 → ŷ=6.</li></ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>R²=0,81: el modelo lineal explica el 81 % de la varianza de y (lectura habitual).</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>Residuo = y − ŷ. Residuos grandes → mala predicción en ese punto.</li></ol>
{ej(1,'Pred','ŷ=10−x. x=3 → ŷ.','7.','e31a')}
{ej(2,'R²','R²=0,25: interpreta con cautela.','Solo ~25 % explicado por la recta; mucha dispersión.','e31b')}
{ej(3,'Extra','Datos de edades 12–18: ¿predecir a los 80?','Extrapolación: no fiable.','e31c')}
{ej(4,'Residuo','y=10, ŷ=8. Residuo.','2. Observado menos predicho.','e31d')}
<canvas id="lienzo31" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo31">Borrar</button></div>
</section>''',
[('ŷ=a+bx','predicción lineal'),('R² alto','mejor ajuste lineal'),('Extrapolación','riesgo')],
'Recta','Ajusta a ojo 5 puntos; predice un x interior y uno exterior; comenta.')

write_dense(32,'Probabilidad compuesta y <em>condicionada</em>','E.2 Condicionada','Árboles y «sabiendo que»',
'CyL: sucesos compuestos; condicionada; independencia; árbol; contingencia.',
['Calcular P(A∩B) con producto cuando hay independencia o con P(A)P(B|A).','Leer P(A|B)=P(A∩B)/P(B).','Construir un árbol de dos etapas.'],
f'''<section class="bloque-cuerpo">
<h2>Reglas</h2>
<p>P(A∩B)=P(A)·P(B|A). Si independientes, P(B|A)=P(B) y el producto se simplifica. Árbol: primera rama P; segunda rama condicionadas; hoja = producto.</p>
{S('Árbol','''
<text x="40" y="50" fill="#E6E1D6">Urna: 2R, 3A · sin reposición</text>
<text x="40" y="110" fill="#8F9A72">P(R1)=2/5 · luego P(R2|R1)=1/4</text>
<text x="40" y="160" fill="#C4A15A">P(R1∩R2)=(2/5)·(1/4)=1/10</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>Monedas independientes: P(CC)=(1/2)·(1/2)=1/4.</li></ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>Sin reposición: P(dos rojas)= (2/5)·(1/4)=1/10.</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>P(A)=0,4, P(A∩B)=0,1 → P(B|A)=0,1/0,4=0,25.</li></ol>
{ej(1,'Indep','P(A)=0,5, P(B)=0,2 indep. P(A∩B).','0,1.','e32a')}
{ej(2,'Cond','P(A∩B)=0,12, P(B)=0,4. P(A|B).','0,3.','e32b')}
{ej(3,'Árbol','Con reposición 2R3A: P(dos rojas).','(2/5)·(2/5)=4/25.','e32c')}
{ej(4,'Indep test','Si P(A|B)=P(A), ¿qué concluimos?','A y B independientes (en ese sentido).','e32d')}
<canvas id="lienzo32" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo32">Borrar</button></div>
</section>''',
[('P(A∩B)','P(A)P(B|A)'),('Independientes','producto P(A)P(B)'),('Árbol hoja','producto de ramas')],
'Urna','Dibuja árbol con y sin reposición; calcula P(dos del mismo color).')

write_dense(33,'Probabilidad total y <em>Bayes</em>','E.2 Bayes','Actualizar creencias',
'CyL: teorema de la probabilidad total y de Bayes.',
['Partir Ω en causas A_i.','Aplicar probabilidad total.','Aplicar Bayes para P(causa|dato).'],
f'''<section class="bloque-cuerpo">
<h2>Fórmulas</h2>
<p>Total: P(B)=Σ P(A_i)P(B|A_i) si los A_i particionan Ω.</p>
<p>Bayes: P(A_j|B)= P(A_j)P(B|A_j) / P(B).</p>
{S('Bayes','''
<text x="40" y="60" fill="#E6E1D6">Test: P(E)=0,01 · P(+|E)=0,99 · P(+|no E)=0,05</text>
<text x="40" y="120" fill="#8F9A72">P(+)≈0,01·0,99+0,99·0,05≈0,0594</text>
<text x="40" y="170" fill="#C4A15A">P(E|+)≈0,0099/0,0594≈0,167</text>
''')}
<h2>Ejemplo 1 — total</h2>
<ol class="pasos"><li>Dos urnas: elige urna 1 con 1/2. P(roja)=… suma productos.</li></ol>
<h2>Ejemplo 2 — Bayes numérico</h2>
<ol class="pasos">
<li>P(E)=0,01; P(+|E)=0,99; P(+|¬E)=0,05.</li>
<li>P(+)=0,01·0,99+0,99·0,05=0,0594.</li>
<li>P(E|+)=0,0099/0,0594≈0,167 (no 0,99).</li>
</ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>La intuición «test bueno ⇒ casi seguro enfermo» falla si la enfermedad es rara.</li></ol>
{ej(1,'Total','P(A)=0,3, P(B|A)=0,5, P(B|Aᶜ)=0,1. P(B).','0,3·0,5+0,7·0,1=0,22.','e33a')}
{ej(2,'Bayes','Con esos datos, P(A|B).','(0,3·0,5)/0,22≈0,682.','e33b')}
{ej(3,'Idea','¿Qué actualiza Bayes?','La probabilidad de la causa dado el dato observado.','e33c')}
{ej(4,'Rareza','¿Por qué baja P(E|+)?','Muchos falsos positivos en la masa de sanos.','e33d')}
<canvas id="lienzo33" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo33">Borrar</button></div>
</section>''',
[('Total','suma P(A_i)P(B|A_i)'),('Bayes','P(causa|dato)'),('Test raro','P(E|+) puede ser moderada')],
'Test','Cambia P(E) a 0,1 y recalcula P(E|+); comenta.')

write_dense(34,'Uniforme, binomial y <em>normal</em>','E.3 Distribuciones','Tres modelos estrella',
'CyL: uniforme (disc./cont.), binomial y normal.',
['Reconocer uniforme.','Calcular binomial en n pequeño.','Usar la campana normal de forma cualitativa (μ, σ).'],
f'''<section class="bloque-cuerpo">
<h2>Modelos</h2>
<p><strong>Uniforme discreto</strong> en 1…n: cada uno 1/n. <strong>Uniforme continuo</strong> en [a,b]: densidad constante 1/(b−a).</p>
<p><strong>Binomial</strong> B(n,p): n ensayos Bernoulli independientes; P(X=k)=C(n,k)p^k(1−p)^{{n−k}}.</p>
<p><strong>Normal</strong>: campana centrada en μ, anchura σ; simétrica.</p>
{S('Campana','''
<path d="M 80 200 Q 200 200 300 80 T 520 200 T 640 200" fill="none" stroke="#C4A15A" stroke-width="2"/>
<line x1="360" y1="40" x2="360" y2="210" stroke="#8F9A72" stroke-dasharray="4"/>
<text x="370" y="60" fill="#8F9A72">μ</text>
''')}
<h2>Ejemplo 1 — uniforme</h2>
<ol class="pasos"><li>Dado justo: P(5)=1/6.</li></ol>
<h2>Ejemplo 2 — binomial</h2>
<ol class="pasos"><li>B(3,1/2): P(X=2)=C(3,2)(1/2)³=3/8.</li></ol>
<h2>Ejemplo 3 — normal</h2>
<ol class="pasos"><li>μ=100, σ=15: valores cerca de 100 son más probables; ±2σ cubre la mayor parte de la masa (idea).</li></ol>
{ej(1,'Unif','[0,10] continuo: P(X≤2).','2/10=0,2. Longitud del intervalo.','e34a')}
{ej(2,'Bin','B(4,0,5): P(X=0).','(1/2)^4=1/16.','e34b')}
{ej(3,'Normal','Si σ crece, ¿la campana?','Se ensancha (más dispersión).','e34c')}
{ej(4,'Modelo','10 lanzamientos moneda: ¿qué distribución?','Binomial n=10 p=1/2 (si justa e indep.).','e34d')}
<canvas id="lienzo34" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo34">Borrar</button></div>
</section>''',
[('B(3,1/2) P(X=2)','3/8'),('Uniforme [a,b]','densidad 1/(b−a)'),('μ normal','centro')],
'Campana','Dibuja dos normales misma μ distinta σ; etiqueta.')

write_dense(35,'Muestreo e <em>inferencia</em>','E.4 Muestreo','De la muestra a la población',
'CyL: muestras, muestreo, validez y diseño de estudios.',
['Distinguir población y muestra.','Reconocer muestreo aleatorio vs sesgado.','Hablar de validez con cautela.'],
f'''<section class="bloque-cuerpo">
<h2>Ideas</h2>
<p>Población: conjunto objetivo. Muestra: subconjunto observado. Inferencia: generalizar con incertidumbre. Muestra aleatoria simple reduce sesgos de selección; voluntarios o «solo mis amigos» no.</p>
{S('Muestreo','''
<text x="40" y="80" fill="#E6E1D6">Población ○○○○○○○○○○</text>
<text x="40" y="140" fill="#C4A15A">Muestra marcada · aleatoria preferible</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>Encuesta del instituto preguntando solo en un recreo de 2º: posible sesgo de edad/horario.</li></ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>n grande ayuda precisión, pero no arregla un sesgo de diseño.</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>Estudio observacional vs experimento controlado: la causalidad es más defendible en el segundo.</li></ol>
{ej(1,'Vocab','¿Muestra o población? «Todas las personas de CyL».','Población (si ese es el objetivo).','e35a')}
{ej(2,'Sesgo','Encuesta online voluntaria sobre «horas de móvil».','Sesgo: quien más usa móvil puede responder más.','e35b')}
{ej(3,'n','¿n=1000 sesgado es mejor que n=100 aleatorio?','No necesariamente: el sesgo no se cura solo con n.','e35c')}
{ej(4,'Validez','Una conclusión válida requiere…','Diseño adecuado + datos + límite de lo que se puede afirmar.','e35d')}
<canvas id="lienzo35" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo35">Borrar</button></div>
</section>''',
[('Población','objetivo completo'),('Muestra aleatoria','reduce sesgo de selección'),('n grande ≠','diseño bueno')],
'Diseño','Propón cómo muestrear opinión del centro con menos sesgo; diagrama.')

write_dense(36,'Emociones, error y <em>equipo</em>','F.1/F.2 Socioafectivo','El error también enseña',
'CyL: autoconciencia, gestión del error, decisiones y trabajo en equipo en matemáticas.',
['Nombrar emociones ante un problema difícil.','Convertir un error en pista.','Acordar roles en un equipo breve.'],
f'''<section class="bloque-cuerpo">
<h2>Práctica</h2>
<p>Bloqueo ≠ incapacidad. Protocolo: 1) ¿Qué entiendo? 2) ¿Qué no? 3) Ejemplo numérico mínimo. 4) Pedir una pista concreta al equipo. El error documentado evita repetirlo.</p>
{S('Ciclo','''
<text x="80" y="80" fill="#E6E1D6">intentar → revisar → ajustar → reintentar</text>
<text x="80" y="140" fill="#8F9A72">el equipo reparte: quien escribe / quien comprueba / quien explica</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>Te sales en un signo: en vez de borrar todo, localiza la línea del cambio.</li></ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>En PL, uno dibuja la región y otro evalúa vértices: menos carga cognitiva.</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>«No sé» + señalar el paso exacto es más útil que silencio.</li></ol>
{ej(1,'Error','Escribes 3·0=3. ¿Qué haces?','Corriges la propiedad; anotas la trampa; rehacés solo desde ahí.','e36a')}
{ej(2,'Equipo','Tres roles útiles en un problema de grafos.','Dibuja / cuenta grados / escribe conclusión.','e36b')}
{ej(3,'Emoción','Ansiedad ante el examen: un gesto útil.','Respirar y empezar por el ítem más claro para recuperar control.','e36c')}
{ej(4,'Decisión','Dos métodos posibles: ¿cómo elegir en equipo?','Probar el más corto 2 min; si atasca, cambiar sin culpa.','e36d')}
<canvas id="lienzo36" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo36">Borrar</button></div>
</section>''',
[('Error útil','si se documenta'),('Roles','reducen carga'),('Pista concreta','mejor que «no sé» vacío')],
'Diario','Escribe un error tuyo reciente y la regla que evitará repetirlo; icono en el lienzo.')

write_dense(37,'Inclusión e <em>historia</em> de las matemáticas','F.3 Inclusión','Voces y contextos',
'CyL: comunicación efectiva; aportación de las matemáticas a lo largo de la historia.',
['Citar un hito histórico con su idea matemática.','Explicar una idea a alguien que no la vio.','Reconocer diversidad de aportaciones.'],
f'''<section class="bloque-cuerpo">
<h2>Historia útil, no decorativa</h2>
<p>Los grafos eulerianos nacen del problema de Königsberg. El álgebra de Al-Juarismi nombra el algoritmo. Hipatia, Kovalevskaya y muchas otras muestran que el talento no tiene un solo perfil. Comunicar matemáticas = elegir el ejemplo adecuado al oyente.</p>
{S('Puentes','''
<text x="40" y="100" fill="#E6E1D6">Königsberg → Euler → grados impares</text>
<text x="40" y="160" fill="#9A9488">La historia explica por qué importa el teorema</text>
''')}
<h2>Ejemplo 1</h2>
<ol class="pasos"><li>Explica combinatoria con menús de un comedor, no solo con fórmulas.</li></ol>
<h2>Ejemplo 2</h2>
<ol class="pasos"><li>Bayes y los tests médicos: historia moderna de actualizar creencias.</li></ol>
<h2>Ejemplo 3</h2>
<ol class="pasos"><li>Una explicación inclusiva evita «esto es obvio» y prefiere «miramos este caso».</li></ol>
{ej(1,'Hito','Nombra la idea de Euler con grafos.','Recorrer aristas y la paridad de grados.','e37a')}
{ej(2,'Comunicar','Explica pendiente a alguien de otra clase en una frase.','Ritmo de cambio: cuánto sube y por cada unidad horizontal.','e37b')}
{ej(3,'Inclusión','¿Por qué evitar «obvio»?','Cierra la puerta a quien aún no lo ve; mejor mostrar el paso.','e37c')}
{ej(4,'Diversidad','Una razón para citar autoras/autores diversos.','El currículo refleja más voces; el alumnado se reconoce.','e37d')}
<canvas id="lienzo37" class="lienzo" width="900" height="280"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo37">Borrar</button></div>
</section>''',
[('Königsberg','origen grafos eulerianos'),('Comunicar','ejemplo adaptado'),('«Obvio»','puede excluir')],
'Minicharla','Prepara 6 líneas para explicar Bayes a un compañero de otra materia.')

write_dense(38,'Proyecto <em>integrador</em> y cierre','A–F Cierre','Todo el curso en un caso',
'Cierre del pack: proyecto que mezcla al menos tres bloques CyL (A–F) en un problema realista offline.',
['Elegir un contexto (viaje, taller, encuesta, red).','Aplicar al menos 3 herramientas del curso.','Entregar un portfolio breve con conclusiones.'],
f'''<section class="bloque-cuerpo">
<h2>Encargo</h2>
<p>Elige <strong>un</strong> escenario. Debe incluir: (1) un conteo o matriz o grafo, (2) una función o PL o sistema, (3) un dato estocástico (probabilidad o estadística). Escribe con editor, dibuja en canvas, justifica con porqués.</p>
<table class="datos"><thead><tr><th>Escenario</th><th>Pistas de bloques</th></tr></thead><tbody>
<tr><td>Ruta escolar</td><td>Grafo + camino mínimo + tiempos</td></tr>
<tr><td>Taller solidario</td><td>PL + porcentajes + encuesta</td></tr>
<tr><td>Feria</td><td>Combinatoria + precios + binomial</td></tr>
</tbody></table>
{S('Portfolio','''
<text x="40" y="70" fill="#E6E1D6">1. Contexto  2. Modelo  3. Cálculo  4. Gráfico  5. Conclusión ética/límites</text>
<text x="40" y="140" fill="#9A9488">Extensión orientativa: 1–2 páginas en el editor + 1 dibujo</text>
''')}
<h2>Ejemplo guiado (ruta)</h2>
<ol class="pasos">
<li>Grafo de 5 paradas con minutos (C).</li>
<li>Coste total como función del número de transbordos (D).</li>
<li>Probabilidad de lluvia y plan B (E).</li>
</ol>
<h2>Ejemplo guiado (taller)</h2>
<ol class="pasos">
<li>Restricciones de material → PL (D).</li>
<li>Precio con IVA (A).</li>
<li>Encuesta de satisfacción 2×2 (E).</li>
</ol>
<h2>Ejemplo guiado (feria)</h2>
<ol class="pasos">
<li>Combinaciones de stand (A).</li>
<li>Ingresos afines (D).</li>
<li>Binomial de visitantes que compran (E).</li>
</ol>
{ej(1,'Diseño','Lista 3 bloques CyL que usarás y por qué.','Respuesta abierta: debe nombrar A–F concretos ligados al escenario.','e38a')}
{ej(2,'Modelo','Escribe las variables y unidades.','Sin unidades el modelo no es integrable ni comprobable.','e38b')}
{ej(3,'Límite','Una limitación de tu modelo.','Ej.: pesos constantes, independencia asumida, muestra pequeña…','e38c')}
{ej(4,'Cierre','¿Qué reutilizarías de L14 o L26?','Derivada/ritmo o vértices de PL, según escenario.','e38d')}
<canvas id="lienzo38" class="lienzo" width="900" height="320"></canvas>
<div class="fila"><button type="button" class="boton" data-clear="lienzo38">Borrar</button></div>
<label for="portfolio38">Portfolio (escribe aquí el proyecto)</label>
<textarea class="editor" id="portfolio38" placeholder="Contexto, modelo, cálculos, conclusión…" style="min-height:12rem"></textarea>
</section>''',
[('Mínimo de bloques','3'),('Portfolio','contexto+modelo+cálculo+gráfico+límites'),('Offline','sin depender de red')],
'Entrega','Completa el portfolio en el editor y el diagrama en el lienzo; autoevalúa con la lista de 5 puntos.')

# CIERRE
md5 = md5_pack()
sizes=[]
for i in range(1,39):
    p=list(Path('/workspace/lesvencimos/staging/bach1/mates-gen/lecciones').glob(f'leccion-{i:02d}-*.html'))[0]
    sizes.append(p.stat().st_size)
sizes.sort()
cier = Path('/workspace/lesvencimos/staging/bach1/mates-gen/CIERRE.md')
cier.write_text(f'''# Cierre ampliado — Matemáticas Generales 1º Bach

- Path: `/workspace/lesvencimos/staging/bach1/mates-gen/`
- Lecciones: **38/38** amplificadas (densidad Bach: explicación, SVG, 2–3 ejemplos numéricos, ejercicios con porqués largos, canvas)
- MD5 pack: `{md5}`
- Tamaños HTML lección (bytes): min={sizes[0]}, mediana={sizes[19]}, max={sizes[-1]}
- Cadena: Revisor Bach `a8d723de-f137-42a9-a5c8-4937cf349386` → Web LV
- Deadline: domingo 4 oct 2026, 10:00 Europe/Madrid
- **NO publicar**
''', encoding='utf-8')
print('MD5', md5)
print('sizes min/med/max', sizes[0], sizes[19], sizes[-1])
for i in range(29,39):
    p=list(Path('/workspace/lesvencimos/staging/bach1/mates-gen/lecciones').glob(f'leccion-{i:02d}-*.html'))[0]
    print(i, p.stat().st_size)
