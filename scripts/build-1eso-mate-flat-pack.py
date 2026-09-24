#!/usr/bin/env python3
"""Build leccion-NN.html shells (online + flat offline pack) for 1º ESO Mate."""
from __future__ import annotations

import html
import json
import pathlib
import re
import shutil
import unicodedata
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[1]
LEC = REPO / "profesor/1eso-matematicas/lecciones"
PLANTILLA = REPO / "profesor/_plantilla-leccion"
HUB = REPO / "profesor/1eso-matematicas/1eso-matematicas.html"
DESCARGAS = REPO / "descargas.html"
PACK_DIR = REPO / "downloads/_build-1eso-mate-flat"
ZIP_PATH = REPO / "downloads/1eso-matematicas-offline.zip"
COURSE_DIR = REPO / "profesor/1eso-matematicas"
COURSE_ICONS = COURSE_DIR / "icons"
BRAND_ICONS = REPO / "brand/favicon"
TOTAL = 47
AVAILABLE = 47  # L01–L47

# (num, short_ud, title, meta, curiosidad_title, curiosidad_text, figura_cur,
#  objetivos[list], cuerpo_extra_html, vida_title, vida_items, vida_figura,
#  widgets[(label, file)], reto_title, reto_body, reto_id, cierre)
LESSONS = [
  {
    "n": 1,
    "eyebrow": "Lección 01 · UD0 · Arranque",
    "title_html": "Qué es pensar matemáticamente: <em>problemas</em>, estrategias y el error como aprendizaje",
    "title_plain": "Qué es pensar matemáticamente: problemas, estrategias y el error como aprendizaje",
    "meta": "Saberes CyL (Decreto 39/2022): E (socioafectivo); A.1 · énfasis socioafectivo [E]",
    "curiosidad_t": "El error que enseña",
    "curiosidad": "Matemáticos y artesanos siempre han corregido midiendo otra vez: un cálculo fallido en una viga o en una receta no se «borra» — se anota qué falló. En clase pasa lo mismo: el error bien mirado acelera más que el acierto sin explicación.",
    "curiosidad_fig": "fuego.svg",
    "curiosidad_label": "Actitud",
    "objetivos": [
      "Distinguir un problema de un ejercicio rutinario.",
      "Probar al menos cuatro estrategias (ensayo-error, dibujo, descomponer, patrón).",
      "Usar el error como información útil, no como fracaso.",
      "Explicar con palabras propias los pasos de una solución.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Las matemáticas de 1º ESO no son solo «hacer cuentas». Son una forma de <strong>pensar con claridad</strong> cuando algo no se resuelve de un vistazo.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.5rem"><strong>Ejercicio</strong> — practica una técnica conocida: «Calcula 23 × 7».</p>
      <p style="margin:0"><strong>Problema</strong> — hay que decidir qué hacer: plazas de autobús, cinta para un patio, presupuesto en €…</p>
    </div>
    <h2>Ejemplo · Autobús y plazas</h2>
    <p>Cabida 55. Hay 38. Suben 3 grupos de 6. ¿Cabe todo el mundo?</p>
    <ol>
      <li>Personas que quieren subir: 3 × 6 = 18.</li>
      <li>Total si suben: 38 + 18 = 56.</li>
      <li>56 &gt; 55 → falta 1 plaza.</li>
    </ol>
""",
    "cuerpo_after_widgets": """
    <h2>Ejemplo · Camino rectangular</h2>
    <p>Patio 12 m de <strong>largo (L)</strong> y 5 m de <strong>ancho (A)</strong>. Cinta = <strong>perímetro (P)</strong>: P = 2 × (L + A) = 2 × (12 + 5) = <strong>34 m</strong>.</p>
""",
    "widget_split": True,  # first widget before second cuerpo block
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "vida2_t": "Euros y comprobación",
    "vida2": "Un ticket o un menú pide sumar, comparar con lo que llevas y comprobar el cambio. Las unidades (€, personas, metros) evitan respuestas absurdas.",
    "vida2_fig": "ticket.svg",
    "widgets": [
      ("Problema · interactivo · autobús", "l01-autobus-plazas.html"),
      ("Problema · interactivo · perímetro", "l01-rectangulo-perimetro.html"),
    ],
    "reto_t": "Una estrategia para mi barrio",
    "reto": "Elige una estrategia de esta lección (dibujo, descomponer, ensayo-error…). Describe una situación real de tu casa, instituto o pueblo/ciudad de CyL donde esa estrategia ayudaría (5–8 frases).",
    "reto_id": "1eso-mate-L01",
    "cierre": "Un problema se aborda con estrategias y se comprueba. El error bien analizado acelera el aprendizaje.",
  },
  {
    "n": 2,
    "eyebrow": "Lección 02 · UD0 · Arranque",
    "title_html": "El origen de nuestras cifras y otros <em>sistemas de numeración</em>",
    "title_plain": "El origen de nuestras cifras y otros sistemas de numeración",
    "meta": "Saberes CyL (Decreto 39/2022): A.1 Conteo; A.4 Relaciones (sistema de numeración)",
    "curiosidad_t": "Cifras indias, camino árabe",
    "curiosidad": "Nuestras cifras 0–9 llegaron a Europa a través del mundo árabe (origen indio). Lo revolucionario no es solo el dibujo: es el sistema posicional decimal y el cero como «guardaespaldas del puesto vacío».",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "Curiosidad histórica",
    "objetivos": [
      "Explicar por qué usamos un sistema decimal posicional.",
      "Comparar nuestro sistema con al menos otro (romano o egipcio a nivel básico).",
      "Leer y escribir números valorando la posición de cada cifra.",
      "Valorar que las matemáticas son una construcción cultural humana.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>La cifra <strong>3</strong> en 3 son unidades; en 30, decenas; en 300, centenas. El <strong>cero</strong> marca «no hay nada en esa posición» y permite escribir 105 sin confusión.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Romanos:</strong> I=1, V=5, X=10, L=50, C=100, D=500, M=1000. No es posicional decimal: XIV = 10+5−1 = 14. Incómodo para cálculos largos.</p>
    </div>
    <p>¿Por qué base 10? Seguramente por contar con los dedos. La herencia sexagesimal (base 60) sigue viva en horas y grados.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · sistemas de numeración", "l02-sistemas-numeracion.html"),
      ("Interactivo · monedas y cambio", "l02-monedas-cambio.html"),
    ],
    "reto_t": "Cifras en mi entorno",
    "reto": "Haz una «caza» de 3 números escritos de forma especial cerca de ti (romano en una placa, dorsal, código, reloj…). Describe: ¿qué sistema usan y por qué crees que lo eligieron?",
    "reto_id": "1eso-mate-L02",
    "cierre": "El sistema decimal posicional con cero hace eficientes el cálculo y la escritura. Otros sistemas enriquecen la mirada cultural.",
  },
  {
    "n": 3,
    "eyebrow": "Lección 03 · UD1 · Números naturales",
    "title_html": "Números naturales y <em>valor posicional</em>",
    "title_plain": "Números naturales y valor posicional",
    "meta": "Saberes CyL (Decreto 39/2022): A.2 Cantidad; A.4 Relaciones (sistema decimal posicional)",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Reconocer el conjunto de los números naturales y para qué sirven.",
      "Descomponer un natural en unidades, decenas, centenas…",
      "Escribir números en forma desarrollada y viceversa.",
      "Usar el vocabulario: cifra, orden, clase (unidades, miles…).",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Los <strong>números naturales</strong> (ℕ) sirven para contar y ordenar: 0, 1, 2, 3… (en este curso incluimos el 0).</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Forma desarrollada</strong> de 34 205:<br/>
      3×10&nbsp;000 + 4×1&nbsp;000 + 2×100 + 0×10 + 5×1.</p>
    </div>
    <p>En español europeo se usan espacios de millar: <strong>1 250 €</strong> (no comas estadounidenses).</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · valor posicional", "l03-valor-posicional.html"),
    ],
    "reto_t": "El número de mi semana",
    "reto": "Elige un número natural grande que haya aparecido en tu semana (pasos del móvil, precio, habitantes…). Descompónlo en forma desarrollada y cuenta en una frase para qué servía ese número.",
    "reto_id": "1eso-mate-L03",
    "cierre": "Naturales + valor posicional = base de casi todo el sentido numérico del curso.",
  },
  {
    "n": 4,
    "eyebrow": "Lección 04 · UD1 · Orden y recta",
    "title_html": "Orden, comparación y <em>recta numérica</em> con naturales",
    "title_plain": "Orden, comparación y recta numérica con naturales",
    "meta": "Saberes CyL (Decreto 39/2022): A.2 Cantidad (recta numérica / representaciones)",
    "curiosidad_t": "La bocita que come al grande",
    "curiosidad": "El signo &lt; / &gt; es una «bocita»: siempre mira (come) al número más grande. 3 &lt; 7 → la boca abierta mira al 7. El lado estrecho toca al pequeño; el ancho, al grande.",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "Truco",
    "objetivos": [
      "Comparar naturales usando valor posicional.",
      "Representar naturales en la recta numérica.",
      "Usar correctamente &lt;, &gt; e =.",
      "Situar números entre decenas o centenas consecutivas.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <ol>
      <li>Quien tiene <strong>más cifras</strong> es mayor: 999 &lt; 1000.</li>
      <li>Si tienen las mismas cifras, compara de <strong>izquierda a derecha</strong>.</li>
    </ol>
    <p>La <strong>recta numérica</strong> ordena de menor a mayor hacia la derecha. Encadenar: 3 &lt; 7 &lt; 10.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · recta numérica", "l04-recta-numerica.html"),
    ],
    "reto_t": "Recta de mi pueblo",
    "reto": "Inventa una mini recta numérica con 4 lugares de tu entorno (casa, kiosko, instituto, polideportivo…) asignando distancias en minutos a pie desde tu casa. ¿Qué conclusiones de orden sacas?",
    "reto_id": "1eso-mate-L04",
    "cierre": "Ordenar naturales es comparar posiciones. La recta da imagen mental para enteros, fracciones y decimales.",
  },
  {
    "n": 5,
    "eyebrow": "Lección 05 · UD1 · Estimaciones",
    "title_html": "Estimaciones con la <em>precisión adecuada</em>",
    "title_plain": "Estimaciones con la precisión adecuada",
    "meta": "Saberes CyL (Decreto 39/2022): A.2 Cantidad (estimaciones)",
    "curiosidad_t": "Cinco o más, ¡a subir!",
    "curiosidad": "Regla del portero: si la cifra siguiente es 5 o más, empuja hacia arriba (subes 1); si es 4 o menos, se queda quieto. Frase: «Cinco o más, ¡a subir!; cuatro o menos, ¡a dormir!»",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "Truco",
    "objetivos": [
      "Redondear naturales a decenas, centenas o millares.",
      "Elegir el grado de precisión según el contexto.",
      "Usar la estimación para comprobar si un resultado es razonable.",
      "Distinguir estimación de cálculo exacto.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p><strong>Estimar</strong> es dar un valor aproximado suficiente para decidir. No siempre hace falta el número exacto.</p>
    <div class="tarjeta">
      <p style="margin:0">3 746 a centenas → mira 4 (decenas) → ≤ 4 → <strong>3 700</strong>.<br/>
      3 760 a centenas → mira 6 → ≥ 5 → <strong>3 800</strong>.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "olla.svg",
    "widgets": [
      ("Interactivo · redondeo", "l05-redondeo.html"),
      ("Interactivo · regateo en el mercadillo", "l05-regateo.html"),
    ],
    "reto_t": "Estimación detective",
    "reto": "Sin calculadora, estima algo medible en tu entorno (páginas de un libro, pasos hasta la esquina, compra familiar semanal). Luego comprueba. Cuenta el método y el error aproximado.",
    "reto_id": "1eso-mate-L05",
    "cierre": "Estimar es sentido numérico: ahorra tiempo y detecta absurdos. Elige la precisión según la pregunta.",
  },
  {
    "n": 6,
    "eyebrow": "Lección 06 · UD2 · Operaciones",
    "title_html": "Suma y resta: propiedades, <em>inversas</em> y cálculo mental",
    "title_plain": "Suma y resta: propiedades, relaciones inversas y cálculo mental",
    "meta": "Saberes CyL (Decreto 39/2022): A.3 Sentido de las operaciones",
    "curiosidad_t": "Espejo suma ↔ resta",
    "curiosidad": "Si a+b=s, entonces s−a=b y s−b=a. Comprobar una resta sumando es un hábito de oro. La suma es conmutativa; la resta no: 10−3 ≠ 3−10.",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "Truco",
    "objetivos": [
      "Usar conmutativa y asociativa de la suma para calcular con soltura.",
      "Reconocer suma y resta como operaciones inversas.",
      "Aplicar estrategias de cálculo mental (descomponer, completar a 10/100).",
      "Resolver problemas de suma/resta en contexto (euros, personas, medidas).",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>La <strong>suma</strong> reúne; la <strong>resta</strong> halla la diferencia o lo que falta (el cambio).</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.4rem"><strong>Mental:</strong> 48+27 → 48+30−3 = 75.</p>
      <p style="margin:0"><strong>Descomponer:</strong> 63−28 = 63−30+2 = 35.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "Aplicaciones",
    "vida": [
      "Sumar productos en el supermercado sin sacar siempre el móvil.",
      "Calcular el cambio con billete de 20 € o 50 €.",
      "Marcador de un partido: diferencia de goles.",
      "Páginas que te quedan de un libro.",
    ],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · suma y resta (caja del mercadillo)", "l06-suma-resta.html"),
    ],
    "reto_t": "Truco mental que uso",
    "reto": "Explica un truco de cálculo mental con sumas o restas que te funcione. Pon un ejemplo numérico y por qué ahorra tiempo.",
    "reto_id": "1eso-mate-L06",
    "cierre": "Suma flexible + resta como inversa + comprobación = base del cálculo. El mental se entrena.",
  },
  {
    "n": 7,
    "eyebrow": "Lección 07 · UD2 · Operaciones",
    "title_html": "Multiplicación y división: <em>propiedades</em> y eficiencia",
    "title_plain": "Multiplicación y división: propiedades y eficiencia",
    "meta": "Saberes CyL (Decreto 39/2022): A.3 Sentido de las operaciones",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "olla.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Entender la multiplicación como grupos iguales (y la división como reparto).",
      "Usar conmutativa, asociativa y distributiva para calcular con eficiencia.",
      "Relacionar × y ÷ como operaciones inversas y comprobar.",
      "Aplicar × y ÷ en contextos (cajas, precios, personas).",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>× = grupos iguales; ÷ = reparto. Comprobar una división multiplicando. Distributiva mental: 7×12 = 7×10 + 7×2.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "olla.svg",
    "widgets": [
      ("Interactivo · cajas de zumo (+ criptograma)", "l07-cajas-zumo.html"),
    ],
    "reto_t": "Mi truco con × o ÷",
    "reto": "Explica un truco tuyo de multiplicar o dividir (mental o con papel). Pon un ejemplo numérico y en qué situación real lo usarías.",
    "reto_id": "1eso-mate-L07",
    "cierre": "× = grupos iguales; ÷ = reparto; propiedades = atajos; inversa = comprobación.",
  },
  {
    "n": 8,
    "eyebrow": "Lección 08 · UD2 · Potencias",
    "title_html": "Potencias de exponente natural y <em>raíces cuadradas</em> sencillas",
    "title_plain": "Potencias de exponente natural y raíces cuadradas sencillas",
    "meta": "Saberes CyL (Decreto 39/2022): A.3 Sentido de las operaciones · A.2 Cantidad",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Interpretar aⁿ como a multiplicado por sí mismo n veces.",
      "Distinguir base y exponente; leer potencias en español.",
      "Relacionar el cuadrado s² con la raíz √q en cuadrados perfectos.",
      "Calcular potencias sencillas y raíces de cuadrados perfectos pequeños.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>2³ = 2×2×2 = 8. «Duplicar tres veces» no es lo mismo que elevar a 3 sin leer el enunciado. Espejo: si s² = q, entonces √q = s (cuadrados perfectos).</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · torres y baldosas", "l08-torres-potencias.html"),
    ],
    "reto_t": "Mi potencia o mi raíz del entorno",
    "reto": "Busca en tu entorno un ejemplo de potencia o de cuadrado/raíz (baldosas, área, «al cuadrado» en un texto). Explícalo con números pequeños.",
    "reto_id": "1eso-mate-L08",
    "cierre": "Potencia = torre de factores. Raíz = lado del cuadrado. No intercambies base y exponente sin pensar.",
  },
  {
    "n": 9,
    "eyebrow": "Lección 09 · UD2 · Problemas",
    "title_html": "Resolución de problemas aritméticos <em>contextualizados</em>",
    "title_plain": "Resolución de problemas aritméticos contextualizados (mezcla de operaciones)",
    "meta": "Saberes CyL (Decreto 39/2022): A.3 Sentido de las operaciones (situaciones contextualizadas)",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Traducir un enunciado a una expresión con +, −, ×, ÷ y paréntesis.",
      "Elegir el orden según el significado (no solo «de memoria»).",
      "Seguir la cadena: dato → representación → operación → comprobación → frase con unidades.",
      "Resolver problemas con mezcla de operaciones en contextos cercanos.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Primero entiende la historia; después escribe la expresión. Ejemplo autobus: (4×5)−6 = 14 viajeros que quedan. Siempre cierra con unidades y una frase.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · excursión CyL", "l09-excursion-problemas.html"),
    ],
    "reto_t": "Un problema de mi semana",
    "reto": "Inventa un problema corto (3–5 frases) de tu semana que mezcle al menos dos operaciones. Resuélvelo con la cadena de oro y una frase final con unidades.",
    "reto_id": "1eso-mate-L09",
    "cierre": "El significado elige la operación. El orden y los paréntesis evitan trampas. Siempre: frase con unidades.",
  },
  {
    "n": 10,
    "eyebrow": "Lección 10 · UD3 · Divisibilidad",
    "title_html": "Múltiplos, divisores y <em>criterios de divisibilidad</em>",
    "title_plain": "Múltiplos, divisores y criterios de divisibilidad",
    "meta": "Saberes CyL (Decreto 39/2022): A.4 Relaciones (múltiplos, divisores)",
    "curiosidad_t": "Rectángulo sin huecos",
    "curiosidad": "Si el rectángulo cierra sin huecos, d divide a n. Múltiplo y divisor son dos caras del mismo reparto exacto: a = k×b. Los criterios (2, 3, 4, 5, 6, 9, 10) ahorran divisiones largas — la foto es un montón de bloques que cabe en filas iguales.",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "Truco",
    "objetivos": [
      "Definir múltiplo y divisor con ejemplos.",
      "Aplicar criterios de divisibilidad por 2, 3, 4, 5, 6, 9 y 10.",
      "Listar divisores de un número pequeño de forma sistemática.",
      "Usar divisibilidad en problemas de agrupación.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p><strong>a</strong> es múltiplo de <strong>b</strong> si a = k×b. <strong>b</strong> es divisor de a si divide exacto. Criterios rápidos: 2 (unidades par), 5 (0 o 5), 10 (0), 3/9 (suma de cifras), 4 (dos últimas), 6 (2 y 3).</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · bloques y criterios", "l10-bloques-divisibilidad.html"),
    ],
    "reto_t": "Reparto sin resto",
    "reto": "Propón un reparto real (merienda, material, equipos) donde importe la divisibilidad. ¿Qué criterio te ayudó?",
    "reto_id": "1eso-mate-L10",
    "cierre": "Múltiplos y divisores organizan el reparto exacto. Los criterios ahorran divisiones largas. El rectángulo sin huecos es la foto del divisor.",
  },
  {
    "n": 11,
    "eyebrow": "Lección 11 · UD3 · Divisibilidad",
    "title_html": "Números primos y <em>factorización</em>",
    "title_plain": "Números primos y factorización",
    "meta": "Saberes CyL (Decreto 39/2022): A.4 Relaciones (primos, factorización)",
    "curiosidad_t": "La criba de Eratóstenes",
    "curiosidad": "Eratóstenes de Cirene (s. III a. C.) ideó una criba para hallar primos: se escriben los naturales y se tachan los múltiplos de 2, 3, 5… Lo que no se tacha es primo. Factorizar es apilar esos «ladrillos» primos; el 1 no es primo ni compuesto.",
    "curiosidad_fig": "fuego.svg",
    "curiosidad_label": "Curiosidad histórica",
    "objetivos": [
      "Definir número primo y compuesto.",
      "Usar la criba de Eratóstenes a escala pequeña.",
      "Descomponer en factores primos.",
      "Escribir la factorización con potencias.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Primo: solo divisores 1 y él mismo. Compuesto: más divisores. Factorizar es escribir el producto de primos (única salvo orden). Criba: lista hasta N y tacha múltiplos.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "olla.svg",
    "widgets": [
      ("Interactivo · criba y ladrillos", "l11-criba-factorizacion.html"),
    ],
    "reto_t": "Primo en la calle",
    "reto": "Encuentra un número primo que aparezca en tu día (dorsal, precio entero, número de bus…). Cuenta por qué sabes que es primo.",
    "reto_id": "1eso-mate-L11",
    "cierre": "Primos son ladrillos de los naturales. Factorizar es escribir un número como producto de esos ladrillos.",
  },
  {
    "n": 12,
    "eyebrow": "Lección 12 · UD3 · Divisibilidad",
    "title_html": "mcd y mcm: <em>estrategias</em> y problemas",
    "title_plain": "mcd y mcm: estrategias y problemas",
    "meta": "Saberes CyL (Decreto 39/2022): A.4 Relaciones (mcd/mcm)",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Calcular mcd y mcm por listados y por factores primos.",
      "Elegir mcd o mcm según el enunciado.",
      "Resolver problemas de coincidencia de ciclos y de reparto máximo.",
      "Relacionar mcd×mcm = producto (para dos números).",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p><strong>mcd(a,b)</strong>: mayor natural que divide a ambos. <strong>mcm(a,b)</strong>: menor múltiplo común. Por factores: menores exponentes → mcd; mayores → mcm. Relación: mcd×mcm = a×b.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · barras, ciclos y Venn", "l12-barras-mcd-mcm.html"),
    ],
    "reto_t": "Ciclos de mi semana",
    "reto": "Inventa dos rutinas con periodos distintos (entreno, serie, recogida de basura…). ¿Cada cuántos días coinciden? Usa mcm.",
    "reto_id": "1eso-mate-L12",
    "cierre": "mcd = mayor divisor común; mcm = menor múltiplo común. El enunciado decide cuál.",
  },
  {
    "n": 13,
    "eyebrow": "Lección 13 · UD4 · Enteros",
    "title_html": "Números enteros: necesidad, <em>representación</em> y orden",
    "title_plain": "Números enteros: necesidad, representación y orden",
    "meta": "Saberes CyL (Decreto 39/2022): A.2 Cantidad (enteros); recta numérica",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Justificar la necesidad de los enteros (deudas, temperaturas, profundidades).",
      "Representar enteros en la recta y hallar el opuesto y el valor absoluto.",
      "Ordenar enteros correctamente.",
      "Usar el vocabulario: positivo, negativo, cero, opuesto.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Los <strong>enteros</strong> (ℤ) = …, −2, −1, 0, 1, 2, …. A la derecha, mayores. <strong>Opuesto</strong> de a es −a. <strong>Valor absoluto</strong> |a| = distancia a 0. Trampa: |−8| &gt; |−3|, pero −8 &lt; −3.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "Aplicaciones",
    "vida": [
      "Partes meteorológicos en invierno castellano-leonés.",
      "Saldo de una cuenta o «debo 5 €».",
      "Ascensor: planta −1 (garaje).",
      "Clasificaciones con diferencia de goles / puntos negativos de sanción.",
    ],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · recta, termómetro y ascensor", "l13-enteros-recta.html"),
    ],
    "reto_t": "Negativos a mi alrededor",
    "reto": "Lista tres situaciones de tu vida donde un número negativo tenga sentido. Elige una y explícala a alguien de tu familia.",
    "reto_id": "1eso-mate-L13",
    "cierre": "Enteros = naturales + negativos + cero. En la recta, a la derecha se crece. El signo indica dirección o sentido.",
  },
  {
    "n": 14,
    "eyebrow": "Lección 14 · UD4 · Enteros",
    "title_html": "Operaciones con enteros y <em>relaciones inversas</em>",
    "title_plain": "Operaciones con enteros y relaciones inversas",
    "meta": "Saberes CyL (Decreto 39/2022): A.3 Operaciones con enteros",
    "curiosidad_t": "Amigos y enemigos",
    "curiosidad": "Resta = sumar el opuesto: a−b = a+(−b). En producto/división: signos iguales → +; distintos → −. Frase: «Restar es sumar el opuesto. Amigos (+ + / − −) → + ; enemigos → −.»",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "Truco",
    "objetivos": [
      "Sumar y restar enteros con recta o reglas de signos.",
      "Multiplicar y dividir enteros (regla de signos).",
      "Usar la resta como sumar el opuesto.",
      "Comprobar operaciones con la inversa.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Suma: misma dirección → suman absolutos; signos distintos → restan y gana el de mayor absoluto. Resta: a−b = a+(−b). × y ÷: iguales → +; distintos → −.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · saltos e inversas", "l14-enteros-operaciones.html"),
    ],
    "reto_t": "Termómetro matemático",
    "reto": "Inventa un mini relato del tiempo en tu provincia con 4 temperaturas enteras a lo largo del día y calcula la variación entre cada tramo.",
    "reto_id": "1eso-mate-L14",
    "cierre": "Resta = suma del opuesto. En producto/división, signos iguales → +; distintos → −.",
  },
  {
    "n": 15,
    "eyebrow": "Lección 15 · UD4 · Enteros",
    "title_html": "Problemas con enteros en <em>contextos</em> cotidianos",
    "title_plain": "Problemas con enteros en contextos cotidianos",
    "meta": "Saberes CyL (Decreto 39/2022): A.3 Operaciones contextualizadas; E socioafectivo · énfasis [E]",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "olla.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Modelar situaciones con enteros eligiendo un origen 0.",
      "Resolver problemas multi-paso con enteros.",
      "Interpretar el significado del signo en la respuesta.",
      "Colaborar y revisar errores sin ridiculizar.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Elige el <strong>origen 0</strong> y no lo cambies a mitad. Traduce ganancias/pérdidas a sumas de enteros. Comprueba el sentido del resultado. Feedback amable centrado en el paso ([E]).</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · historias con enteros [E]", "l15-enteros-contextos.html"),
    ],
    "reto_t": "Modelo con zero casero",
    "reto": "Elige un origen 0 en tu casa (termo, hucha, planta del edificio) y escribe un problema de 3 acciones con enteros. Ofrece la solución.",
    "reto_id": "1eso-mate-L15",
    "cierre": "Los enteros modelan ida y vuelta respecto de un origen. La interpretación final importa tanto como la cuenta.",
  },
  {
    "n": 16,
    "eyebrow": "Lección 16 · UD5 · Fracciones",
    "title_html": "Fracciones: significado, <em>equivalencia</em> y simplificación",
    "title_plain": "Fracciones: significado, equivalencia y simplificación",
    "meta": "Saberes CyL (Decreto 39/2022): A.2 Cantidad (fracciones); A.3",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "fuego.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Interpretar una fracción como parte de un todo, cociente y razón sencilla.",
      "Reconocer y construir fracciones equivalentes.",
      "Simplificar fracciones dividiendo por el mcd.",
      "Usar vocabulario: numerador, denominador, fracción irreducible.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Una fracción <strong>a/b</strong> (b≠0) puede significar parte de un todo, cociente a ÷ b o razón «a por cada b». Amplificar multiplica arriba y abajo por el mismo número; simplificar divide ambos por el <strong>mcd</strong>, sin cambiar el valor.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 18/24 = 3/4 porque mcd(18,24)=6. Fracciones mayores que 1 también son válidas: 9/4 son dos enteros y un cuarto.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "Aplicaciones",
    "vida": [
      "Recetas: 3/4 de taza de harina.",
      "Ofertas: la segunda unidad a mitad de precio.",
      "Progreso de una serie: llevas 5/8 capítulos.",
      "Repartir una pizza o un bocadillo en partes iguales.",
    ],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · pizza, equivalencia y simplificar", "l16-fracciones-pizza.html"),
    ],
    "reto_t": "Fracción del recreo",
    "reto": "Mide o estima qué fracción del recreo usas en tres actividades (hablar, jugar, merendar…). Simplifica si puedes y comenta si el total da aproximadamente 1.",
    "reto_id": "1eso-mate-L16",
    "cierre": "Fracción = parte, cociente o razón. Equivalentes = mismo valor. Simplificar se hace con el mcd.",
  },
  {
    "n": 17,
    "eyebrow": "Lección 17 · UD5 · Fracciones",
    "title_html": "Comparación y representación de fracciones en la <em>recta</em>",
    "title_plain": "Comparación y representación de fracciones en la recta",
    "meta": "Saberes CyL (Decreto 39/2022): A.2 Cantidad (recta / representaciones)",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Comparar fracciones de igual denominador o igual numerador.",
      "Comparar con distinto denominador mediante equivalentes o decimales sencillos.",
      "Situar fracciones en la recta numérica.",
      "Reconocer fracciones propias, impropias y números mixtos sencillos.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Con igual denominador, mayor numerador → mayor fracción. Con igual numerador, mayor denominador → menor fracción. Si son distintos, usa equivalentes con <strong>mcm</strong> o una referencia como 1/2. Una propia tiene a&lt;b; una impropia, a≥b.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 3/4=9/12 y 5/6=10/12; por tanto 3/4 &lt; 5/6. En la recta, 1/2 queda justo entre 0 y 1.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · comparar en la recta", "l17-fracciones-recta.html"),
    ],
    "reto_t": "Recta del bocadillo",
    "reto": "Dibuja una recta de 0 a 1 y marca cuánto bocadillo (o merienda) sueles comer. Pregunta a dos personas y márcalo: ¿quién come más fracción?",
    "reto_id": "1eso-mate-L17",
    "cierre": "Comparar fracciones exige el mismo tamaño de trozo o una buena referencia. La recta fija la intuición.",
  },
  {
    "n": 18,
    "eyebrow": "Lección 18 · UD5 · Fracciones",
    "title_html": "Suma y resta de <em>fracciones</em>",
    "title_plain": "Suma y resta de fracciones",
    "meta": "Saberes CyL (Decreto 39/2022): A.3 Operaciones (fracciones)",
    "curiosidad_t": "Alinea los trozos",
    "curiosidad": "El denominador dice el tamaño del trozo. Por eso 2/8 + 3/8 = 5/8: se suman numeradores porque ya hablamos de octavos. Con denominadores distintos, primero alinea los tamaños con el mcm.",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "Truco",
    "objetivos": [
      "Sumar y restar fracciones con igual denominador.",
      "Sumar y restar con distinto denominador usando el mcm.",
      "Simplificar el resultado.",
      "Resolver problemas de partes de un mismo todo.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Con igual denominador, suma o resta numeradores y conserva el denominador. Con distinto denominador, calcula el <strong>mcm</strong>, amplifica, opera y simplifica.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 1/4 + 1/6 → mcm(4,6)=12 → 3/12 + 2/12 = 5/12. Error típico: 1/2 + 1/3 ≠ 2/5.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "olla.svg",
    "widgets": [
      ("Interactivo · suma y resta con barras", "l18-fracciones-suma.html"),
    ],
    "reto_t": "Suma de partes del día",
    "reto": "Parte un día laborable en fracciones (cole, deberes, ocio, sueño…). Súmalas y mira si te acercas a 1. Ajusta y comenta qué te sorprendió.",
    "reto_id": "1eso-mate-L18",
    "cierre": "Solo se suman o restan fracciones con el mismo denominador. El mcm es tu herramienta.",
  },
  {
    "n": 19,
    "eyebrow": "Lección 19 · UD5 · Fracciones",
    "title_html": "Multiplicación y división de <em>fracciones</em>",
    "title_plain": "Multiplicación y división de fracciones",
    "meta": "Saberes CyL (Decreto 39/2022): A.3 Operaciones (fracciones)",
    "curiosidad_t": "Parte de una parte",
    "curiosidad": "Multiplicar fracciones puede significar tomar una parte de otra parte. Para dividir, dale la vuelta solo a la segunda fracción y multiplica por su inversa.",
    "curiosidad_fig": "olla.svg",
    "curiosidad_label": "Truco",
    "objetivos": [
      "Multiplicar fracciones y simplificar el resultado.",
      "Calcular una fracción de una cantidad.",
      "Dividir fracciones multiplicando por la inversa.",
      "Resolver problemas de parte de parte y repartos.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Para multiplicar, multiplica numerador por numerador y denominador por denominador. Puedes <strong>cancelar</strong> antes para trabajar con números pequeños. Para dividir, multiplica por la <strong>inversa</strong> de la segunda fracción.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 2/3 ÷ 4/5 = 2/3 × 5/4 = 10/12 = <strong>5/6</strong>. Se da la vuelta solo al segundo número.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · producto y división con área", "l19-fracciones-producto.html"),
    ],
    "reto_t": "Parte de parte",
    "reto": "Describe una situación casera de «parte de una parte» (nevera, playlist, depósito). Escríbela con un producto de fracciones y calcúlala.",
    "reto_id": "1eso-mate-L19",
    "cierre": "Multiplicar: arriba×arriba, abajo×abajo. Dividir: multiplica por la inversa. «Fracción de» suele significar producto.",
  },
  {
    "n": 20,
    "eyebrow": "Lección 20 · UD5 · Fracciones",
    "title_html": "Problemas con <em>fracciones</em>",
    "title_plain": "Problemas con fracciones",
    "meta": "Saberes CyL (Decreto 39/2022): A.3 Operaciones contextualizadas",
    "curiosidad_t": "¿Del todo o del resto?",
    "curiosidad": "En un problema, el todo puede cambiar. Si dice «de lo que queda», dibuja una cinta, marca lo que has quitado y usa el resto como nuevo todo.",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "Truco",
    "objetivos": [
      "Elegir la operación adecuada según el enunciado.",
      "Combinar fracción de cantidad con sumas y restas.",
      "Detectar si el todo cambia a mitad del problema.",
      "Explicar la solución con una frase y sus unidades.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>«Fracción de» suele indicar un producto; «en total» suma; «queda» resta; «repartir» divide. No son palabras mágicas: dibuja o escribe los datos y comprueba cuál es el todo en cada paso.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> de 120 páginas lees 1/4 = 30; quedan 90. Después lees 1/3 de 90 = 30. En total has leído <strong>60 páginas</strong>.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · problemas CyL con cinta", "l20-problemas-fracciones.html"),
    ],
    "reto_t": "Problema para un compañero",
    "reto": "Escribe un problema con fracciones ambientado en tu instituto o pueblo. Incluye la solución al dorso (o al final). Debe necesitar al menos dos pasos.",
    "reto_id": "1eso-mate-L20",
    "cierre": "Lee dos veces: ¿la fracción es del total o del resto? Un dibujo o esquema evita muchos fallos.",
  },
  {
    "n": 21,
    "eyebrow": "Lección 21 · UD6 · Decimales",
    "title_html": "Números decimales: lectura, escritura y <em>operaciones</em>",
    "title_plain": "Números decimales: lectura, escritura y operaciones",
    "meta": "Saberes CyL (Decreto 39/2022): A.2 Cantidad (decimales); A.3 Operaciones",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Leer y escribir decimales con valor posicional.",
      "Ordenar decimales y usar &lt;, &gt; e =.",
      "Sumar, restar, multiplicar y dividir decimales sencillos.",
      "Usar decimales en euros y medidas cotidianas.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>En España usamos la <strong>coma decimal</strong>: 3,14. Para sumar o restar, alinea las comas. Para multiplicar, cuenta las cifras decimales; para dividir, puedes convertir el divisor en natural desplazando la coma en ambos números.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 2,45 + 0,8 = 2,45 + 0,80 = <strong>3,25</strong>. En dinero, redondea a céntimos cuando sea necesario.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "Aplicaciones",
    "vida": [
      "Precios de supermercado, tickets y cambio en euros.",
      "Alturas, distancias y medidas en metros.",
      "Gasolina expresada en euros por litro.",
      "Tiempos deportivos y marcas con centésimas.",
    ],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · rejilla posicional y dinero €", "l21-decimales-euro.html"),
    ],
    "reto_t": "Detective de comas",
    "reto": "Recoge 5 precios reales (foto mental) y ordénalos. Calcula el total y propón un billete o pago con el que pagarías.",
    "reto_id": "1eso-mate-L21",
    "cierre": "Los decimales extienden el sistema posicional a la derecha de la coma. En dinero, trabaja a céntimos y comprueba el cambio.",
  },

  {
    "n": 22,
    "eyebrow": "Lección 22 · UD6 · Decimales y porcentajes",
    "title_html": "Relación entre <em>fracciones, decimales y porcentajes</em>",
    "title_plain": "Relación entre fracciones, decimales y porcentajes",
    "meta": "Saberes CyL (Decreto 39/2022): A.2 Cantidad; A.5 Razonamiento proporcional (porcentajes intro)",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Pasar de fracción a decimal y viceversa en casos sencillos.",
      "Entender % como «de cada 100».",
      "Convertir entre fracción, decimal y porcentaje habituales.",
      "Elegir la representación más cómoda según el problema.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Una cantidad puede expresarse de varias formas equivalentes: <strong>1/2 = 0,5 = 50 %</strong>. De fracción a decimal dividimos; de decimal a porcentaje multiplicamos por 100; de porcentaje a decimal dividimos entre 100.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 3/4 = 0,75 = <strong>75 %</strong>. El porcentaje significa 75 de cada 100.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · fracción, decimal y porcentaje", "l22-fraccion-decimal-porcentaje.html"),
    ],
    "reto_t": "Tres trajes de un número",
    "reto": "Elige un porcentaje de una noticia o anuncio. Escríbelo también como decimal y como fracción. ¿En qué forma se entiende mejor?",
    "reto_id": "1eso-mate-L22",
    "cierre": "Fracción, decimal y % son tres trajes del mismo número. Elige el traje cómodo; traduce sin perder valor.",
  },
  {
    "n": 23,
    "eyebrow": "Lección 23 · UD7 · Proporcionalidad",
    "title_html": "<em>Razones y proporciones</em>",
    "title_plain": "Razones y proporciones",
    "meta": "Saberes CyL (Decreto 39/2022): A.5 Razonamiento proporcional",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Definir razón como cociente comparado.",
      "Reconocer una proporción como igualdad de dos razones.",
      "Calcular el término desconocido en una proporción.",
      "Distinguir razón de diferencia («3 más» no es «razón 3»).",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>La razón entre <strong>a</strong> y <strong>b</strong> se escribe <strong>a:b</strong> o <strong>a/b</strong>. En una proporción, <strong>a/b = c/d</strong>, y la propiedad fundamental dice que <strong>a×d = b×c</strong>.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 3/4 = x/12 → 3×12 = 4x → <strong>x = 9</strong>. «3 € más» es una diferencia, no una razón.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · razones, proporciones y recta doble", "l23-razones-proporciones.html"),
    ],
    "reto_t": "Razón en mi cocina o deporte",
    "reto": "Enuncia una razón real (ingredientes, goles o distancias). Formúlala a:b, simplifícala y di qué informa.",
    "reto_id": "1eso-mate-L23",
    "cierre": "Razón compara dividiendo. Proporción: dos razones iguales; usa productos cruzados para hallar la incógnita.",
  },
  {
    "n": 24,
    "eyebrow": "Lección 24 · UD7 · Proporcionalidad",
    "title_html": "Proporcionalidad <em>directa</em>: igualdad de razones y reducción a la unidad",
    "title_plain": "Proporcionalidad directa: igualdad de razones y reducción a la unidad",
    "meta": "Saberes CyL (Decreto 39/2022): A.5 Proporcionalidad directa",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Reconocer magnitudes directamente proporcionales.",
      "Completar tablas de proporcionalidad directa.",
      "Resolver problemas por reducción a la unidad y por proporción.",
      "Detectar cuándo no hay proporcionalidad directa.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Si <strong>y = k·x</strong>, la razón y/x es constante. Para resolver un problema, reduce primero a una unidad y después multiplica por lo pedido.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 4 cuadernos = 12 € → 1 cuaderno = 3 € → <strong>7 cuadernos = 21 €</strong>. Un taxi con bajada de bandera no es directa pura: no pasa por el origen.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · unidad, tabla k y razones", "l24-proporcionalidad-directa.html"),
    ],
    "reto_t": "¿Es proporcional?",
    "reto": "Pon un ejemplo de tu barrio que sí sea proporcionalidad directa y otro que lo parezca pero no lo sea. Justifica con números pequeños.",
    "reto_id": "1eso-mate-L24",
    "cierre": "Directa ⇒ razón constante. Reduce a 1 y multiplica, o monta una proporción. Primero pregunta: ¿es proporcional?",
  },

  {
    "n": 25,
    "eyebrow": "Lección 25 · UD7 · Proporcionalidad y porcentajes",
    "title_html": "Porcentajes: <em>cálculo y problemas</em>",
    "title_plain": "Porcentajes: cálculo y problemas",
    "meta": "Saberes CyL (Decreto 39/2022): A.5 Porcentajes",
    "curiosidad_t": "De cada cien",
    "curiosidad": "El símbolo % resume una idea antigua y poderosa: contar cuántas partes hay si el todo se reparte en cien. Por eso 25 % es 25 de cada 100, o la cuarta parte.",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "Curiosidad histórica",
    "objetivos": [
      "Calcular el p % de una cantidad.",
      "Hallar el porcentaje que representa una parte respecto a un total.",
      "Resolver aumentos y descuentos porcentuales.",
      "Encadenar descuentos sin sumar porcentajes a lo loco.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p><strong>p % de N = (p/100) × N</strong>. Para hallar qué porcentaje representa una parte, calcula parte ÷ total × 100. En un descuento del 20 %, pagas el 80 %, es decir, multiplicas por 0,8.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> una sudadera de 80 € con 25 % de descuento → pagas el 75 %: 80 × 0,75 = <strong>60 €</strong>. Dos descuentos sucesivos se calculan paso a paso.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "Aplicaciones",
    "vida": [
      "Rebajas de temporada y etiquetas de tiendas.",
      "Porcentaje de aciertos en un examen o tiros en un partido.",
      "Aumentos, recargos e impuestos sencillos en un ticket.",
      "Comparar cuánto sube o baja un precio sin confundir euros con porcentajes.",
    ],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · etiquetas de rebajas y descuentos", "l25-porcentajes-descuentos.html"),
    ],
    "reto_t": "Cazador de descuentos",
    "reto": "Encuentra una oferta real (%). Calcula el precio final de un artículo inventado o real. ¿El cartel es claro o confunde? Comenta en 4 frases.",
    "reto_id": "1eso-mate-L25",
    "cierre": "% = de cada 100. Multiplica por p/100. En descuentos, multiplica por (1−p/100). Encadenados: paso a paso.",
  },
  {
    "n": 26,
    "eyebrow": "Lección 26 · UD8 · Educación financiera sencilla",
    "title_html": "Leer información numérica en <em>tickets, ofertas y presupuestos</em>",
    "title_plain": "Leer información numérica en tickets, ofertas y presupuestos",
    "meta": "Saberes CyL (Decreto 39/2022): A.6 Educación financiera; E · énfasis socioafectivo [E]",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Leer un ticket sencillo identificando base, impuestos, total y redondeos.",
      "Interpretar ofertas 2x1, 2ª al 50 % y precio por unidad o kilogramo.",
      "Detectar información engañosa o incompleta.",
      "Elaborar un presupuesto mínimo con ingresos y gastos.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>En un ticket, multiplica <strong>cantidad × precio</strong> en cada línea y suma. El precio unitario (€/kg, €/L o €/ud) permite comparar envases distintos. En una oferta 2×1 pagas una unidad y llevas dos; en «2ª al 50 %» pagas el 100 % de una y el 50 % de la segunda.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 1,5 L a 1,20 € cuestan 0,80 €/L. Un presupuesto también es una cuenta: ingresos − gastos = dinero libre.</p>
    </div>
    <div class="tarjeta">
      <p style="margin:0"><strong>Momento [E]:</strong> usa cantidades ficticias si hablar de dinero te resulta sensible y respeta la privacidad de cada casa.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "Aplicaciones",
    "vida": [
      "Ticket del supermercado, la panadería o una excursión.",
      "Comparar packs de cereales por €/100 g o €/kg.",
      "Leer ofertas de móviles, videojuegos y tiendas con letra pequeña.",
      "Preparar un presupuesto semanal de ejemplo.",
    ],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · ticket térmico, ofertas y presupuesto", "l26-ticket-ofertas.html"),
    ],
    "reto_t": "Ticket detective",
    "reto": "Analiza un ticket real (o inventado realista) de al menos 4 líneas. Calcula un precio unitario y señala si hubo oferta. Propón una mejora de gasto.",
    "reto_id": "1eso-mate-L26",
    "cierre": "Leer números de la compra es alfabetización financiera. Precio unitario y condiciones de la oferta mandan.",
  },
  {
    "n": 27,
    "eyebrow": "Lección 27 · UD8 · Educación financiera sencilla",
    "title_html": "Decisiones de consumo: <em>calidad-precio y valor-precio</em>",
    "title_plain": "Decisiones de consumo: calidad-precio y valor-precio",
    "meta": "Saberes CyL (Decreto 39/2022): A.6 Consumo responsable; E · énfasis socioafectivo [E]",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Distinguir precio bajo, calidad-precio y valor personal.",
      "Usar criterios numéricos y no numéricos en una decisión de compra.",
      "Valorar sostenibilidad y necesidad frente al impulso.",
      "Argumentar una elección con datos.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p><strong>Precio</strong> es lo que pagas; <strong>calidad-precio</strong> relaciona prestaciones o duración con ese precio; <strong>valor</strong> es lo que aporta a una persona. Un producto caro puede salir más barato al mes si dura mucho más.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 60 € durante 24 meses son 2,50 €/mes; 25 € durante 5 meses son 5 €/mes. Después de calcular, pregunta también: «¿lo necesito?, ¿me durará?, ¿puedo repararlo?»</p>
    </div>
    <div class="tarjeta">
      <p style="margin:0"><strong>Momento [E]:</strong> en un debate, ataca el argumento, no a la persona. Las preferencias ajenas pueden tener valor personal.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · estantería de calidad-precio y valor", "l27-calidad-precio.html"),
    ],
    "reto_t": "Compra con cabeza",
    "reto": "Elige un producto que quieras o necesites. Compara dos opciones con precio, duración estimada y un criterio personal. Publica tu decisión razonada.",
    "reto_id": "1eso-mate-L27",
    "cierre": "Decidir bien mezcla números (precio, €/uso) y valores (necesidad, ética, gusto). El consumo responsable también se calcula.",
  },
  {
    "n": 28,
    "eyebrow": "Lección 28 · UD9 · Medida en el plano",
    "title_html": "Magnitudes, <em>unidades</em> y elección de unidad (longitud, amplitud, área)",
    "title_plain": "Magnitudes, unidades y elección de unidad (longitud, amplitud, área)",
    "meta": "Saberes CyL (Decreto 39/2022): B.1 Magnitud",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Distinguir magnitud de unidad y de cantidad.",
      "Manejar unidades de longitud, amplitud angular y área.",
      "Convertir unidades habituales (m, cm, mm, km; m², cm²).",
      "Elegir la unidad adecuada al objeto medido.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p><strong>Magnitud</strong> es lo que medimos; <strong>unidad</strong> es el patrón; <strong>cantidad</strong> es número × unidad. En longitud usamos km, m, cm y mm; en área, m² y cm²; los ángulos se expresan en grados (°).</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Ejemplo:</strong> 1 m = 100 cm = 1000 mm y 1 m² = 10 000 cm². En áreas el factor también se «cuadra».</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · estaciones de magnitud", "l28-magnitudes-unidades.html"),
    ],
    "reto_t": "Unidad justa",
    "reto": "Elige 5 objetos y escribe la magnitud y la unidad más razonable para cada uno. Uno debe ser un ángulo.",
    "reto_id": "1eso-mate-L28",
    "cierre": "Magnitud + unidad adecuada = medida útil. Domina los factores 10, 100, 1000 y el 10 000 del m²↔cm².",
  },
  {
    "n": 29,
    "eyebrow": "Lección 29 · UD9 · Medida en el plano",
    "title_html": "Medir longitudes y ángulos; <em>precisión</em> y estimación",
    "title_plain": "Medir longitudes y ángulos; precisión y estimación",
    "meta": "Saberes CyL (Decreto 39/2022): B.2 Medición; B.3 Estimación y relaciones",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Usar regla, cinta métrica y transportador con buena técnica.",
      "Estimar longitudes y ángulos antes de medir.",
      "Expresar una medida con la precisión adecuada.",
      "Formular conjeturas sobre medidas y contrastarlas.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Para medir una longitud, alinea el <strong>0</strong> de la regla con un extremo y mira de frente. Para medir un ángulo, coloca el vértice en el centro del transportador y un lado sobre 0°. Estima antes y calcula el error absoluto <strong>|E−M|</strong>.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Precisión:</strong> si una regla aprecia milímetros, no tiene sentido escribir 12,387 cm. Informa solo las cifras que realmente ves.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · regla y transportador", "l29-regla-transportador.html"),
    ],
    "reto_t": "Ojo de medidor",
    "reto": "Estima tres longitudes y un ángulo en tu entorno, mídelos y calcula los errores. ¿En qué tipo de magnitud fallas más?",
    "reto_id": "1eso-mate-L29",
    "cierre": "Estimar → medir → contrastar. La precisión la marca el instrumento y el uso.",
  },
  {
    "n": 30,
    "eyebrow": "Lección 30 · UD9 · Medida en el plano",
    "title_html": "Áreas de figuras planas elementales: <em>deducción</em> y aplicación",
    "title_plain": "Áreas de figuras planas elementales: deducción y aplicación",
    "meta": "Saberes CyL (Decreto 39/2022): B.2 Medición (áreas); B.3 Estimación y relaciones",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Deducir y usar áreas de rectángulo, cuadrado, triángulo, paralelogramo y trapecio.",
      "Descomponer figuras compuestas.",
      "Distinguir perímetro (u) de área (u²).",
      "Resolver problemas de pintura, suelos y cartulinas.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Rectángulo y paralelogramo: <strong>A=b×h</strong>; cuadrado: <strong>A=L²</strong>; triángulo: <strong>A=½×b×h</strong>; trapecio: <strong>A=½(B+b)×h</strong>. La altura siempre es perpendicular a la base.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Perímetro ≠ área:</strong> el perímetro mide el contorno en unidades (u); el área mide la superficie en unidades cuadradas (u²). Las figuras compuestas se suman o se restan.</p>
    </div>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "Aplicaciones",
    "vida": [
      "Comprar césped artificial, baldosas o cartulina.",
      "Pintar una pared descontando puertas y ventanas.",
      "Descomponer el plano de una habitación en rectángulos.",
      "Comparar perímetro y superficie de una pista.",
    ],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · áreas con deducción", "l30-areas-figuras.html"),
    ],
    "reto_t": "Área de mi sitio",
    "reto": "Calcula el área aproximada de tu mesa de estudio o de tu habitación (croquis). Explica para qué te serviría ese dato en casa.",
    "reto_id": "1eso-mate-L30",
    "cierre": "Área mide superficie. Fórmulas básicas + descomposición resuelven casi todo el plano elemental de 1º.",
  },

  {
    "n": 31,
    "eyebrow": "Lección 31 · UD10 · Figuras planas",
    "title_html": "Elementos y <em>clasificación</em> de figuras planas",
    "title_plain": "Elementos y clasificación de figuras planas",
    "meta": "Saberes CyL (Decreto 39/2022): C.1 Figuras geométricas 2D",
    "curiosidad_t": "El lenguaje de las figuras",
    "curiosidad": "Desde Euclides, nombrar un vértice, un lado o un ángulo permite que otra persona reconstruya exactamente la figura. Clasificar no es poner etiquetas al azar: es reconocer propiedades que se mantienen.",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "Curiosidad histórica",
    "objetivos": [
      "Identificar puntos, segmentos, rectas, rayos, ángulos y polígonos.",
      "Clasificar triángulos por lados y por ángulos.",
      "Clasificar cuadriláteros y reconocer sus inclusiones.",
      "Usar vocabulario preciso: vértice, lado, diagonal, base y altura.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Un <strong>polígono</strong> es una figura cerrada de lados rectos. Los triángulos se clasifican por lados (equilátero, isósceles, escaleno) y por ángulos (acutángulo, rectángulo, obtusángulo).</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Cuadriláteros:</strong> cuadrado, rectángulo, rombo y romboide son paralelogramos; el trapecio tiene al menos un par de lados paralelos. Todo cuadrado es rectángulo y rombo, pero no al revés.</p>
    </div>
    <p>Un polígono de <strong>n</strong> lados tiene <strong>n(n−3)/2</strong> diagonales. En un triángulo hay 0 y en un hexágono hay 9.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · clasificar polígonos", "l31-clasificar-figuras.html"),
    ],
    "reto_t": "Zoo geométrico",
    "reto": "Fotografía mental de 6 formas en tu entorno y clasifícalas con el vocabulario de la lección. Una debe ser un triángulo no equilátero.",
    "reto_id": "1eso-mate-L31",
    "cierre": "Clasificar es organizar el zoo de figuras por propiedades. El vocabulario preciso evita confusiones en problemas.",
  },
  {
    "n": 32,
    "eyebrow": "Lección 32 · UD10 · Figuras planas",
    "title_html": "Posiciones relativas de <em>rectas y circunferencias</em>",
    "title_plain": "Posiciones relativas de rectas y circunferencias",
    "meta": "Saberes CyL (Decreto 39/2022): C.1 Rectas y circunferencias",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Determinar posiciones relativas entre dos rectas.",
      "Distinguir exterior, tangente y secante en recta-circunferencia.",
      "Reconocer casos básicos entre dos circunferencias.",
      "Relacionar la distancia centro-recta con el radio.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Dos rectas pueden ser <strong>paralelas</strong>, <strong>secantes</strong> o <strong>perpendiculares</strong>. Para una recta y una circunferencia de centro O y radio r, compara la distancia perpendicular d de O a la recta.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>d &gt; r</strong>: exterior, 0 puntos · <strong>d = r</strong>: tangente, 1 punto · <strong>d &lt; r</strong>: secante, 2 puntos.</p>
    </div>
    <p>La <strong>circunferencia</strong> es el borde; el <strong>círculo</strong> es el disco interior. El diámetro mide 2r.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · posiciones con d y r", "l32-posiciones-rectas-circulos.html"),
    ],
    "reto_t": "Tangentes en la calle",
    "reto": "Encuentra un ejemplo de rectas paralelas, uno de perpendiculares y uno de tangencia aproximada. Explica por qué encajan.",
    "reto_id": "1eso-mate-L32",
    "cierre": "Las posiciones relativas se deciden con ángulos (rectas) o comparando d y r (recta-circunferencia).",
  },
  {
    "n": 33,
    "eyebrow": "Lección 33 · UD10 · Figuras planas",
    "title_html": "Construcción de figuras: <em>regla y compás</em>",
    "title_plain": "Construcción de figuras: regla y compás",
    "meta": "Saberes CyL (Decreto 39/2022): C.1 Construcción manipulativa y digital",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Construir triángulos dados lados o ángulos con regla y compás.",
      "Comprender la idea de mediatriz y bisectriz.",
      "Describir una construcción digital paso a paso.",
      "Valorar la precisión y la reproducibilidad.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>La <strong>regla</strong> traza segmentos y el <strong>compás</strong> dibuja circunferencias o arcos de radio fijo. La mediatriz reúne los puntos equidistantes de los extremos de un segmento; la bisectriz divide un ángulo en dos iguales.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Triángulo SSS:</strong> desde A dibuja un arco de radio b y desde B otro de radio a. Su intersección es C. Solo cierra si se cumple la desigualdad triangular.</p>
    </div>
    <p>Deja constancia de los pasos y comprueba las medidas: así otra persona puede repetir la construcción.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · construcción con regla y compás", "l33-construccion-figuras.html"),
    ],
    "reto_t": "Mini construcción",
    "reto": "Construye en papel o GeoGebra un triángulo o un cuadrado con medidas concretas. Lista 3 comprobaciones que demuestren que está bien.",
    "reto_id": "1eso-mate-L33",
    "cierre": "Construir es demostrar con las manos (o el software) que una figura existe y cumple propiedades. Precisión + desigualdad triangular.",
  },

  {
    "n": 34,
    "eyebrow": "Lección 34 · UD11 · Semejanza, Tales y Pitágoras",
    "title_html": "Congruencia, <em>semejanza y escalas</em>",
    "title_plain": "Congruencia, semejanza y escalas",
    "meta": "Saberes CyL (Decreto 39/2022): C.1 Congruencia, semejanza, escalas",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Distinguir figuras congruentes y semejantes.",
      "Usar la razón de semejanza k.",
      "Interpretar escalas numéricas y gráficas en mapas y planos.",
      "Calcular medidas reales a partir de un plano y viceversa.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Dos figuras son <strong>congruentes</strong> si tienen la misma forma y tamaño. Son <strong>semejantes</strong> si mantienen la forma: sus ángulos son iguales y sus lados homólogos guardan la misma proporción.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Razón k:</strong> k = lado de la imagen ÷ lado original. Si k = 2, cada longitud se duplica y cada área se multiplica por k² = 4.</p>
    </div>
    <p>En una escala <strong>1:500</strong>, 1 unidad en el plano representa 500 unidades reales. Convierte primero a la misma unidad: 3 cm en un plano 1:1000 son 3000 cm = 30 m.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "Planos y mapas",
    "vida": [
      "Planos de viviendas y catastro.",
      "Mapas de senderismo de la sierra de Gredos o Picos.",
      "Maquetas y modelismo con escalas como 1:43.",
      "Ampliar un dibujo en una fotocopiadora.",
    ],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · semejanza y escalas", "l34-semejanza-escalas.html"),
    ],
    "reto_t": "Plano de bolsillo",
    "reto": "Haz un croquis a escala simple de tu mesa o de un balcón/patio pequeño. Indica la escala y una medida real comprobada.",
    "reto_id": "1eso-mate-L34",
    "cierre": "Semejanza = misma forma + lados proporcionales. Escala = semejanza entre dibujo y realidad; las áreas usan k².",
  },
  {
    "n": 35,
    "eyebrow": "Lección 35 · UD11 · Semejanza, Tales y Pitágoras",
    "title_html": "Teorema de Tales y <em>criterios de semejanza</em>",
    "title_plain": "Teorema de Tales y criterios de semejanza de triángulos",
    "meta": "Saberes CyL (Decreto 39/2022): C.1 Teorema de Tales; criterios de semejanza",
    "curiosidad_t": "Medir sin trepar",
    "curiosidad": "Con una sombra y una regla podemos estimar la altura de una farola o un árbol. La luz del Sol llega casi con rayos paralelos y crea triángulos semejantes.",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "Curiosidad histórica",
    "objetivos": [
      "Aplicar el teorema de Tales cuando paralelas cortan un haz.",
      "Reconocer los criterios AA, LAL y LLL.",
      "Calcular segmentos desconocidos mediante proporciones.",
      "Usar Tales en problemas introductorios de alturas y sombras.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Si varias <strong>paralelas</strong> cortan dos rectas transversales, los segmentos correspondientes son proporcionales. En un triángulo, una paralela a un lado forma un triángulo pequeño semejante al grande.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Criterios:</strong> AA (dos ángulos iguales), LAL (dos lados proporcionales y ángulo comprendido igual) y LLL (tres lados proporcionales). Alinea siempre lados homólogos.</p>
    </div>
    <p>Para una sombra solar, persona y edificio forman triángulos semejantes: altura persona / sombra persona = altura edificio / sombra edificio. No mezcles sombras de horas distintas.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · Tales y criterios", "l35-tales-semejanza.html"),
    ],
    "reto_t": "Altura sin trepar",
    "reto": "Diseña, con números razonables, un experimento de sombras para estimar una farola o un muro. Indica medidas y la proporción.",
    "reto_id": "1eso-mate-L35",
    "cierre": "Tales relaciona segmentos proporcionales; la semejanza de triángulos se reconoce con AA, LAL o LLL.",
  },
  {
    "n": 36,
    "eyebrow": "Lección 36 · UD11 · Semejanza, Tales y Pitágoras",
    "title_html": "Relación <em>pitagórica</em>: identificación y problemas",
    "title_plain": "Relación pitagórica: identificación y problemas",
    "meta": "Saberes CyL (Decreto 39/2022): C.1 Relación pitagórica",
    "curiosidad_t": "La escuadra de una cuerda",
    "curiosidad": "Una cuerda marcada en 3, 4 y 5 unidades permite comprobar una esquina de 90 grados. Las ternas pitagóricas convierten una regla geométrica en una herramienta práctica.",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "Curiosidad histórica",
    "objetivos": [
      "Enunciar el teorema de Pitágoras en triángulos rectángulos.",
      "Reconocer ternas pitagóricas sencillas y sus múltiplos.",
      "Calcular un lado desconocido.",
      "Aplicar la relación a diagonales, escaleras y distancias.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>En un triángulo rectángulo, los <strong>catetos</strong> a y b forman el ángulo de 90° y la <strong>hipotenusa</strong> c es el lado mayor, frente a ese ángulo:</p>
    <div class="tarjeta">
      <p style="margin:0;text-align:center;font-size:1.15rem"><strong>a² + b² = c²</strong></p>
      <p style="margin:.5rem 0 0">Para hallar un cateto: a = √(c² − b²). Comprueba antes que c es la hipotenusa.</p>
    </div>
    <p>Las ternas 3-4-5, 5-12-13 y sus múltiplos ayudan a reconocer resultados. Solo aplicamos esta relación cuando hay un ángulo recto.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · Pitágoras con cuadrados", "l36-pitagoras.html"),
    ],
    "reto_t": "Escuadra 3-4-5",
    "reto": "Propón cómo marcar un ángulo recto en un jardín o patio solo con una cuerda marcada a 3, 4 y 5 unidades. Describe el procedimiento.",
    "reto_id": "1eso-mate-L36",
    "cierre": "Cateto² + cateto² = hipotenusa². La hipotenusa es la más larga y mira al ángulo recto.",
  },
  {
    "n": 37,
    "eyebrow": "Lección 37 · UD12 · Coordenadas y modelización",
    "title_html": "Coordenadas cartesianas y <em>localización de puntos</em>",
    "title_plain": "Coordenadas cartesianas y localización de puntos",
    "meta": "Saberes CyL (Decreto 39/2022): C.2 Localización (coordenadas)",
    "curiosidad_t": "El mapa que piensa con dos números",
    "curiosidad": "Descartes popularizó la unión entre álgebra y geometría: dos números pueden señalar un punto. Hoy la misma intuición aparece en mapas, juegos y GPS, aunque el GPS real use sistemas más complejos.",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "Curiosidad histórica",
    "objetivos": [
      "Situar puntos en el plano cartesiano y reconocer los cuatro cuadrantes.",
      "Leer coordenadas (x, y) y localizar el origen (0,0).",
      "Calcular distancias horizontales, verticales y diagonales sencillas.",
      "Explicar por qué el orden de la pareja (x,y) importa.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>El eje <strong>X</strong> es horizontal y el eje <strong>Y</strong> vertical. Su cruce es el <strong>origen O(0,0)</strong>. En un punto P(a,b), primero leemos la abscisa x y después la ordenada y.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Cuadrantes:</strong> I (+,+), II (−,+), III (−,−), IV (+,−). El origen no pertenece a ningún cuadrante.</p>
    </div>
    <p>En una misma horizontal o vertical basta una resta: |x₂−x₁| o |y₂−y₁|. Para una diagonal, combina los desplazamientos con Pitágoras: d = √(Δx² + Δy²).</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "Mapas con dos números",
    "vida": [
      "Batalla naval y juegos de cuadrícula.",
      "Mapa de asientos de un cine: fila y columna.",
      "Planos de calles en retícula.",
      "Videojuegos: posición (x,y) del personaje.",
    ],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · plano-mapa cartesiano", "l37-coordenadas-plano.html"),
    ],
    "reto_t": "Mapa del recreo",
    "reto": "Dibuja un eje sobre un croquis del recreo o de tu habitación y da coordenadas a 5 sitios. Explica tu unidad (baldosas, pasos…).",
    "reto_id": "1eso-mate-L37",
    "cierre": "Primero abscisa (↔), luego ordenada (↕): el orden importa. Los signos indican el cuadrante y las distancias se comprueban con Pitágoras.",
  },
  {
    "n": 38,
    "eyebrow": "Lección 38 · UD12 · Coordenadas y modelización",
    "title_html": "Modelización geométrica de <em>situaciones en el plano</em>",
    "title_plain": "Modelización geométrica de situaciones en el plano",
    "meta": "Saberes CyL (Decreto 39/2022): C.3 Visualización y modelización",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Traducir una situación real a un croquis geométrico.",
      "Elegir figuras y medidas relevantes e ignorar el ruido.",
      "Combinar área, perímetro, semejanza o Pitágoras según el caso.",
      "Validar el modelo comprobando unidades y sentido de la respuesta.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p><strong>Modelizar</strong> es simplificar la realidad con geometría útil. El método: dibujar, etiquetar datos, elegir propiedades o fórmulas, calcular, interpretar y revisar los límites del modelo.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Conserva:</strong> longitudes, ángulos rectos, paralelas y escalas. <strong>Ignora como ruido:</strong> texturas, nombres y curvas que no cambian la pregunta.</p>
    </div>
    <p>Un informe claro incluye croquis, datos, fórmula, cálculo, resultado con unidades y una frase «esto no incluye…». Así otra persona puede validar la decisión.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · mini-mapas de Castilla y León", "l38-modelizacion-plano.html"),
    ],
    "reto_t": "Problema del barrio",
    "reto": "Formula un problema geométrico real de tu entorno (parque, pista, habitación). Resuélvelo y di qué simplificaste.",
    "reto_id": "1eso-mate-L38",
    "cierre": "Dibujo → datos → fórmula → número → ¿tiene sentido? Un modelo útil declara sus simplificaciones y unidades.",
  },
  {
    "n": 39,
    "eyebrow": "Lección 39 · UD13 · Álgebra inicial",
    "title_html": "Patrones numéricos y geométricos: <em>describir la regla</em>",
    "title_plain": "Patrones numéricos y geométricos: describir la regla",
    "meta": "Saberes CyL (Decreto 39/2022): D.1 Patrones",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Reconocer patrones en sucesiones numéricas y figuras.",
      "Describir la regla con palabras y con una fórmula sencilla.",
      "Predecir términos siguientes y comprobar la predicción.",
      "Conectar patrones con tablas de valores.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Un <strong>patrón</strong> es una regularidad. Si la diferencia entre términos consecutivos es constante, tenemos una sucesión aritmética: aₙ = a₁ + (n−1)·d.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Fósforos en cuadrados seguidos:</strong> el primer cuadrado usa 4 y cada paso añade 3; por eso aₙ = 3n + 1. Comprueba siempre n=1 y n=2.</p>
    </div>
    <p>Cuenta lados, fósforos o baldosas, organiza los datos en una tabla y expresa la regla primero con palabras: «multiplica la posición por… y suma…».</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · patrones visibles", "l39-patrones-regla.html"),
    ],
    "reto_t": "Patrón de mi casa",
    "reto": "Encuentra un patrón visual o numérico en casa (azulejos, horarios, coleccionables). Describe la regla y predice el siguiente elemento.",
    "reto_id": "1eso-mate-L39",
    "cierre": "Mira → cuenta → di la regla → escribe aₙ → comprueba n=1 y n=2. Una tabla convierte el patrón en una predicción comprobable.",
  },
  {
    "n": 40,
    "eyebrow": "Lección 40 · UD13 · Álgebra inicial",
    "title_html": "Del lenguaje cotidiano al <em>lenguaje algebraico</em>",
    "title_plain": "Del lenguaje cotidiano al lenguaje algebraico",
    "meta": "Saberes CyL (Decreto 39/2022): D.2 Modelo matemático; D.3 Variable (intro)",
    "curiosidad_t": "Palabras que se vuelven símbolos",
    "curiosidad": "Durante siglos muchos problemas se resolvían con palabras («retórica»). En la Europa moderna aparecieron símbolos compactos: hoy una frase como «3 más que el doble» puede escribirse 2x+3. La notación cambia, pero la idea sigue siendo la misma.",
    "curiosidad_fig": "ticket.svg",
    "curiosidad_label": "Curiosidad histórica",
    "objetivos": [
      "Traducir frases a expresiones algebraicas.",
      "Distinguir expresión, ecuación e identidad a nivel intuitivo.",
      "Usar letras para cantidades desconocidas o variables.",
      "Evitar errores de traducción, especialmente con «el doble de». ",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>El álgebra comprime frases: «un número» → <strong>x</strong>, «el siguiente» → <strong>x+1</strong>, «el doble» → <strong>2x</strong>, «la mitad» → <strong>x/2</strong> y «3 más que el doble» → <strong>2x+3</strong>.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.45rem"><strong>Expresión:</strong> 2x+3 se puede evaluar. <strong>Ecuación:</strong> 2x+3=11 se resuelve.</p>
      <p style="margin:0"><strong>Convención:</strong> 2x significa 2·x; se omite el signo × para no confundirlo con la letra x.</p>
    </div>
    <p>Para traducir: lee la frase, subraya la cantidad, define qué representa cada letra, escribe la expresión y comprueba con un número. «El doble de x más 3» suele ser 2x+3, no 2(x+3), salvo que la frase incluya los paréntesis.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · traducir frases y expresiones", "l40-lenguaje-algebraico.html"),
    ],
    "reto_t": "Frase secreta algebraica",
    "reto": "Escribe 3 frases cotidianas y su expresión algebraica. Reta a un compañero a traducirlas al revés, de expresión a frase.",
    "reto_id": "1eso-mate-L40",
    "cierre": "Traducir al álgebra es poner orden a lo que ya dices con palabras. Define las letras y cuidado con «doble de» y paréntesis.",
  },
  {
    "n": 41,
    "eyebrow": "Lección 41 · UD13 · Álgebra inicial",
    "title_html": "Variable e incógnita: <em>fórmulas</em>",
    "title_plain": "Variable e incógnita; fórmulas",
    "meta": "Saberes CyL (Decreto 39/2022): D.3 Variable; fórmulas",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Distinguir variable (puede cambiar) e incógnita (valor a descubrir).",
      "Sustituir en fórmulas de área, perímetro, velocidad y temperatura.",
      "Despejar una variable en fórmulas lineales sencillas.",
      "Valorar el papel histórico del lenguaje simbólico.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>En <strong>A=L·L</strong> de un cuadrado, las letras representan magnitudes que pueden variar. En <strong>2x+3=11</strong>, x es la incógnita: buscamos el valor que cumple la igualdad.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.45rem"><strong>Fórmulas:</strong> P=2(a+b) y d=v·t empaquetan modelos. Para despejar, usa operaciones inversas en ambos miembros: P/2=a+b → b=P/2−a.</p>
      <p style="margin:0"><strong>Unidades:</strong> v=d/t con d en km y t en h da km/h. Al sustituir números negativos, usa paréntesis.</p>
    </div>
    <p>Truco: ¿cambia a voluntad? → variable. ¿La buscas en una igualdad? → incógnita. Sustituye con paréntesis y despeja con pasos reversibles.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · variables, incógnitas y fórmulas", "l41-variable-formulas.html"),
    ],
    "reto_t": "Fórmula casera",
    "reto": "Inventa una fórmula útil en tu casa (minutos de horno, coste de datos, riego…). Define las variables y pon un ejemplo numérico.",
    "reto_id": "1eso-mate-L41",
    "cierre": "Variable = puede variar; incógnita = se busca. Las fórmulas se usan sustituyendo o despejando con operaciones inversas.",
  },
  {
    "n": 42,
    "eyebrow": "Lección 42 · UD13 · Álgebra inicial",
    "title_html": "Equivalencia de expresiones y <em>ecuaciones lineales</em>",
    "title_plain": "Equivalencia de expresiones y ecuaciones lineales (coeficientes enteros)",
    "meta": "Saberes CyL (Decreto 39/2022): D.4 Igualdad y desigualdad; equivalencia",
    "curiosidad_t": "La balanza de la igualdad",
    "curiosidad": "Una balanza se mantiene equilibrada si hacemos lo mismo en los dos platos. Esa imagen ayuda a entender las ecuaciones equivalentes: sumar, restar, multiplicar o dividir por el mismo número (distinto de cero) conserva las soluciones.",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "Truco",
    "objetivos": [
      "Simplificar expresiones reduciendo términos semejantes.",
      "Aplicar la propiedad distributiva con enteros.",
      "Reconocer ecuaciones equivalentes.",
      "Montar ecuaciones lineales con coeficientes enteros a partir de enunciados.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Los términos semejantes tienen la misma parte literal: 3x−7x=−4x, pero 3x y 2 no se pueden sumar. La distributiva reparte el factor: <strong>−2(x−5)=−2x+10</strong>.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.45rem"><strong>Ecuaciones equivalentes:</strong> x+3=7 equivale a x=4 porque ambas tienen la misma solución. Haz siempre la misma operación en los dos miembros.</p>
      <p style="margin:0"><strong>Enunciados:</strong> subraya «es / equivale / resulta»; ahí suele ir el signo =. La balanza es una metáfora útil para comprobar.</p>
    </div>
    <p>Truco: junta lo parecido, reparte el paréntesis, haz lo mismo en los dos platos y comprueba la solución. No sumes 3x+2 como si fuera 5x ni multipliques un solo lado.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · equivalencia y balanza", "l42-equivalencia-ecuaciones.html"),
    ],
    "reto_t": "Balanza de palabras",
    "reto": "Escribe un enunciado cotidiano y su ecuación. Enseña dos ecuaciones equivalentes a esa y explica los pasos que has hecho en ambos miembros.",
    "reto_id": "1eso-mate-L42",
    "cierre": "Simplifica con términos semejantes y distributiva. Ecuaciones equivalentes = misma solución. Mantén la balanza equilibrada.",
  },
  {
    "n": 43,
    "eyebrow": "Lección 43 · UD13 · Álgebra inicial",
    "title_html": "Resolución de ecuaciones lineales y <em>comprobación de soluciones</em>",
    "title_plain": "Resolución de ecuaciones lineales y comprobación de soluciones",
    "meta": "Saberes CyL (Decreto 39/2022): D.4 Ecuaciones lineales; coeficientes enteros",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Resolver ecuaciones del tipo ax+b=c y ax+b=cx+d con enteros.",
      "Usar la trasposición de términos con criterio.",
      "Comprobar siempre sustituyendo la solución.",
      "Interpretar la solución en un problema verbal.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Resuelve en cuatro pasos: simplifica cada miembro, agrupa letras a un lado y números al otro, despeja <strong>x</strong> y <strong>comprueba</strong> sustituyendo.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.45rem"><strong>Ejemplo:</strong> 3x−5=2x+4 → 3x−2x=4+5 → <strong>x=9</strong>. Comprobación: 3·9−5=22 y 2·9+4=22.</p>
      <p style="margin:0"><strong>Casos especiales:</strong> 0·x=5 no tiene solución; 0·x=0 tiene infinitas. Si aparece x/2, multiplica ambos miembros por 2 para limpiar la fracción.</p>
    </div>
    <p>Define primero la incógnita en los problemas («x = precio de una entrada en €») y termina con una frase que interprete la solución. No cambies de miembro sin cambiar el signo ni dividas solo un término.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · resolver y comprobar ecuaciones", "l43-ecuaciones-resolver.html"),
    ],
    "reto_t": "Ecuación del día",
    "reto": "Inventa un problema breve cuya ecuación sea lineal. Resuélvelo y muestra la comprobación. Propón el enunciado para la web.",
    "reto_id": "1eso-mate-L43",
    "cierre": "Resuelve con operaciones inversas, agrupa y comprueba sustituyendo. La comprobación es el control de calidad de la solución.",
  },
  {
    "n": 44,
    "eyebrow": "Lección 44 · UD14 · Relaciones y funciones",
    "title_html": "Relaciones cuantitativas: <em>tablas y gráficas</em>",
    "title_plain": "Relaciones cuantitativas: tablas y gráficas",
    "meta": "Saberes CyL (Decreto 39/2022): D.5 Relaciones y funciones",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Organizar datos en tablas de entrada y salida.",
      "Representar puntos en ejes y unirlos cuando tenga sentido.",
      "Leer máximos y tendencias sencillas de una gráfica.",
      "Relacionar expresión, tabla y gráfica en relaciones lineales.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Una <strong>relación</strong> asocia valores de <strong>x</strong> con valores de <strong>y</strong>. Puede expresarse con palabras, una tabla, una gráfica o una fórmula. En <strong>y=2x+1</strong>, para x=0,1,2,3 obtenemos y=1,3,5,7.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.45rem"><strong>Recorrido:</strong> elige x → calcula y → coloca los puntos (x,y) en ejes graduados → observa si crece, baja o se alinea.</p>
      <p style="margin:0"><strong>Ojo con la escala:</strong> empezar el eje Y en 50 puede exagerar diferencias. En categorías no unas puntos sin una razón.</p>
    </div>
    <p>Normalmente x es la variable independiente (horas, kg) y y la dependiente (km, €, °C). Una relación lineal y=m·x+n produce puntos alineados; y=x² es una relación no lineal que crece cada vez más deprisa.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · tabla y gráfica", "l44-tablas-graficas.html"),
    ],
    "reto_t": "Gráfica de mi semana",
    "reto": "Haz una tabla de algo que midas 5 días (pasos, minutos de lectura, temperatura…). Dibuja la gráfica y escribe 3 conclusiones.",
    "reto_id": "1eso-mate-L44",
    "cierre": "Verbal ↔ tabla ↔ gráfica ↔ fórmula. Pasar de una representación a otra ayuda a leer relaciones y tendencias.",
  },
  {
    "n": 45,
    "eyebrow": "Lección 45 · UD14 · Relaciones y pensamiento computacional",
    "title_html": "Algoritmos sencillos: <em>interpretar y modificar pasos</em>",
    "title_plain": "Algoritmos sencillos: interpretar y modificar pasos",
    "meta": "Saberes CyL (Decreto 39/2022): D.6 Pensamiento computacional; E (socioafectivo)",
    "curiosidad_t": "El algoritmo de Euclides",
    "curiosidad": "Euclides, en los Elementos (s. III a. C.), describió un procedimiento paso a paso para hallar el máximo común divisor: restar (o dividir) una y otra vez hasta llegar al resto cero. Es uno de los algoritmos más antiguos que seguimos usando.",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "Curiosidad histórica",
    "objetivos": [
      "Interpretar un algoritmo escrito en pasos o diagrama sencillo.",
      "Detectar errores y mejorar la claridad de un algoritmo.",
      "Modificar un algoritmo para un objetivo nuevo.",
      "Valorar el trabajo en equipo y depurar sin frustración excesiva.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Un <strong>algoritmo</strong> es una secuencia finita de pasos claros para resolver una tarea. Tiene entradas, acciones y una salida. En pseudocódigo usamos <strong>SI…ENTONCES…SI NO</strong> y repeticiones como <strong>MIENTRAS</strong> o <strong>REPETIR HASTA</strong>.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.45rem"><strong>Depurar:</strong> prueba con un ejemplo, localiza dónde falla y corrige ese paso. Prueba también con 0, números iguales o un valor extremo.</p>
      <p style="margin:0"><strong>Ejemplo:</strong> leer a,b; si a≥b escribir a; si no escribir b. Para tres números, añade la comparación con c.</p>
    </div>
    <p>Los pasos deben ser precisos, finitos, eficaces y comprensibles. Si no cuadra, pregunta «¿me miras el paso 3?»; depurar juntos es normal y no hace falta acertar a la primera.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · algoritmos en tarjetas", "l45-algoritmos-pasos.html"),
    ],
    "reto_t": "Algoritmo de mi barrio",
    "reto": "¿Para qué se podría usar un algoritmo de este estilo en tu día a día o en tu barrio? Da una idea concreta con entradas, pasos y salida.",
    "reto_id": "1eso-mate-L45",
    "cierre": "Algoritmo = pasos claros y finitos. Interpretar, probar y modificar es pensamiento computacional en 1º ESO.",
  },
  {
    "n": 46,
    "eyebrow": "Lección 46 · UD15 · Cierre de curso",
    "title_html": "Proyecto integrador: <em>un problema real</em>",
    "title_plain": "Proyecto integrador: un problema real",
    "meta": "Saberes CyL (Decreto 39/2022): A–D integrados; E (trabajo en equipo)",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "mapa.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Elegir y delimitar un problema real abordable.",
      "Movilizar al menos tres sentidos: numérico, medida, espacial o algebraico.",
      "Presentar un informe claro con croquis, cálculos y conclusiones.",
      "Trabajar en equipo con roles y respeto.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Un proyecto integra lo aprendido: primero se formula una pregunta, después se recogen datos, se elige un modelo, se calculan resultados y se revisa si tienen sentido. Puede tratarse del rediseño del patio, un viaje, un huerto o una tienda solidaria.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.45rem"><strong>Cadena:</strong> propuesta → datos → modelo → cálculos → revisión → exposición.</p>
      <p style="margin:0"><strong>Ejemplo:</strong> para un patio de 20×35 m, el área es 700 m² y el perímetro 110 m. Si un bote cubre 40 m², el número de botes se redondea hacia arriba.</p>
    </div>
    <p>Recuerda distinguir área y perímetro, convertir la escala con cuidado y escribir unidades. Un buen resultado también explica el límite del modelo.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "mapa.svg",
    "widgets": [
      ("Interactivo · proyecto patio", "l46-proyecto-patio.html"),
    ],
    "reto_t": "Pitch de mi proyecto",
    "reto": "Resume tu proyecto en 8–10 líneas: problema, matemáticas usadas, resultado y qué mejorarías. Aporta una idea concreta de tu centro, barrio o localidad.",
    "reto_id": "1eso-mate-L46",
    "cierre": "Un proyecto convierte datos reales en un modelo que se calcula, se revisa y se explica. Calidad matemática y conexión con la vida van juntas.",
  },
  {
    "n": 47,
    "eyebrow": "Lección 47 · UD15 · Cierre de curso",
    "title_html": "Autoevaluación, portfolio y <em>hábitos matemáticos</em>",
    "title_plain": "Autoevaluación, portfolio y hábitos matemáticos",
    "meta": "Saberes CyL (Decreto 39/2022): E Sentido socioafectivo; metacognición",
    "curiosidad_t": "",
    "curiosidad": "",
    "curiosidad_fig": "fuego.svg",
    "curiosidad_label": "",
    "objetivos": [
      "Revisar evidencias de aprendizaje del curso en un portfolio.",
      "Identificar fortalezas y lagunas con honestidad.",
      "Formular hábitos de estudio matemático sostenibles.",
      "Valorar el error, la perseverancia y la colaboración.",
    ],
    "cuerpo": """
    <h2>Explicación breve</h2>
    <p>Un <strong>portfolio</strong> reúne 6–10 piezas: problemas corregidos, croquis, proyectos, retos y reflexiones. La autoevaluación con una rúbrica de 1 a 4 mira comprensión, cálculo, geometría, álgebra, explicación y actitud.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.45rem"><strong>Hábitos:</strong> leer todo antes de calcular, estimar y comprobar, anotar el error y rehacer, y pedir ayuda concreta («no entiendo el paso 2»).</p>
      <p style="margin:0"><strong>Plan:</strong> 10–15 minutos cada dos días con problemas variados mantiene mejor que un atracón el último día.</p>
    </div>
    <p>Tu valor no es tu última nota: es tu capacidad de seguir aprendiendo con otros. El portfolio señala qué repasar al empezar 2º ESO.</p>
""",
    "cuerpo_after_widgets": "",
    "widget_split": False,
    "vida_t": "",
    "vida": [],
    "vida_fig": "fuego.svg",
    "widgets": [
      ("Interactivo · portfolio y hábitos", "l47-portfolio-habitos.html"),
    ],
    "reto_t": "Mi mejor idea del curso",
    "reto": "Elige la idea, truco o proyecto del año del que más orgulloso/a estés. Explícalo en 6–8 frases con un ejemplo concreto para la galería de retos.",
    "reto_id": "1eso-mate-L47",
    "cierre": "Saber mates incluye saber cómo aprendes. Portfolio, hábitos pequeños, error útil y respeto forman un buen cierre de 1º ESO.",
  },

]


def slugify(title_plain: str, max_len: int = 40) -> str:
    """Return a short, filesystem-safe Spanish topic slug."""
    text = unicodedata.normalize("NFKD", title_plain)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    # In titles such as L02, the phrase after “y otros” is the useful topic.
    text = re.split(r"\s+y\s+otros?\s+", text, maxsplit=1, flags=re.IGNORECASE)[-1]
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    if len(text) <= max_len:
        return text
    text = text[:max_len].rstrip("-")
    return text.rsplit("-", 1)[0] or text


def lesson_filename(n: int) -> str:
    """Canonical lesson filename; the NN prefix keeps Downloads sorted."""
    lesson = next((item for item in LESSONS if item["n"] == n), None)
    if lesson is None:
        raise KeyError(f"unknown lesson {n}")
    return f"leccion-{n:02d}-{slugify(lesson['title_plain'])}.html"


def manifest_text() -> str:
    return json.dumps({
        "name": "1º ESO Matemáticas · Les vencimos",
        "short_name": "1º ESO Matemáticas",
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "theme_color": "#FAF7F0",
        "background_color": "#FAF7F0",
        "accent_color": "#C4A15A",
        "icons": [
            {"src": "icons/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
            {"src": "icons/favicon-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "icons/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
            {"src": "icons/app-icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, ensure_ascii=False, indent=2) + "\n"


def ensure_course_branding() -> None:
    COURSE_ICONS.mkdir(parents=True, exist_ok=True)
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "app-icon-512.png"):
        shutil.copy2(BRAND_ICONS / name, COURSE_ICONS / name)
    (COURSE_DIR / "manifest.webmanifest").write_text(manifest_text(), encoding="utf-8")


def progress_pct(n: int) -> str:
    return f"{(n / TOTAL) * 100:.2f}".rstrip("0").rstrip(".")


def nav_html(n: int, *, offline: bool) -> str:
    calc = "calculadora.html" if offline else "../../../modulos/calculadora.html"
    if n <= 1:
        prev = '<span class="atajo atajo-prev is-disabled" aria-disabled="true" title="Primera lección">← Anterior</span>'
    else:
        prev = f'<a class="atajo atajo-prev" href="{lesson_filename(n - 1)}" title="Lección {n-1:02d}">← Anterior</a>'
    if n >= TOTAL:
        hub = "index.html" if offline else "../1eso-matematicas.html"
        nxt = f'<a class="atajo atajo-next" href="{hub}" title="Volver al índice">Fin del curso</a>'
    elif n >= AVAILABLE:
        nxt = '<span class="atajo atajo-next is-disabled" aria-disabled="true" title="Próximamente">Siguiente →</span>'
    else:
        nxt = f'<a class="atajo atajo-next" href="{lesson_filename(n + 1)}" title="Lección {n+1:02d}">Siguiente →</a>'
    return f"""  <nav class="leccion-barra" aria-label="Navegación de lección"
       data-actual="{n}" data-total="{TOTAL}">
    <div class="leccion-progreso" role="status">
      <span class="progreso-texto"><strong>{n}</strong> de <strong>{TOTAL}</strong></span>
      <div class="progreso-pista" aria-hidden="true"><div class="progreso-lleno" style="width:{progress_pct(n)}%"></div></div>
    </div>
    <div class="leccion-atajos">
      <a class="atajo atajo-calc" href="{calc}" title="Calculadora offline">Calculadora</a>
      {prev}
      {nxt}
    </div>
  </nav>"""


def srcdoc_escape(doc: str) -> str:
    """Escape widget HTML for use inside a double-quoted srcdoc attribute."""
    return (
        doc.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
    )


def load_widget_html(fname: str) -> str:
    path = LEC / fname
    if not path.exists():
        raise SystemExit(f"missing widget {fname}")
    return path.read_text(encoding="utf-8")


_EXTERNAL_URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.I)
_EXTERNAL_OK = ("w3.org", "www.w3.org", "xmlns", "schema.org", "schemas.xmlsoap")


def assert_widget_offline_safe(fname: str, doc: str) -> None:
    """Fail build if a widget pulls CDN/network assets that would break offline."""
    bad = []
    for url in sorted(set(_EXTERNAL_URL_RE.findall(doc))):
        if any(ok in url for ok in _EXTERNAL_OK):
            continue
        bad.append(url)
    if bad:
        raise SystemExit(
            f"widget {fname} has network URL(s) that break offline: {', '.join(bad[:8])}"
        )


def widget_block(
    label: str,
    fname: str,
    *,
    offline: bool = False,
    widget_html: str | None = None,
) -> str:
    title = html.escape(label, quote=True)
    if offline and widget_html is not None:
        # Sibling iframe src= often fails on Android file:// / content://.
        # Embed the full widget via srcdoc so animations run inside the lesson.
        onload = (
            "try{var d=this.contentDocument||this.contentWindow.document;"
            "if(d){var h=Math.max("
            "(d.documentElement&&d.documentElement.scrollHeight)||0,"
            "(d.body&&d.body.scrollHeight)||0,560);"
            "this.style.height=h+'px';this.parentElement.style.minHeight=h+'px';}}"
            "catch(e){}"
        )
        iframe = (
            f'<iframe title="{title}" class="widget-srcdoc" '
            f'srcdoc="{srcdoc_escape(widget_html)}" '
            f'onload="{html.escape(onload, quote=True)}"></iframe>'
        )
        fallback = (
            f'Si el marco embebido no responde, abre el widget suelto: '
            f'<a href="{fname}">{fname}</a>.'
        )
    else:
        iframe = f'<iframe title="{title}" src="{fname}" loading="lazy"></iframe>'
        fallback = (
            f'Si el marco no carga (<code>file://</code>), abre '
            f'<a href="{fname}">{fname}</a>.'
        )
    marco_extra = " marco-offline-embed" if offline else ""
    return f"""  <section class="bloque-interactivo">
    <div class="marco-interactivo-cabecera">
      <span class="etiqueta-interactivo">{label}</span>
      <a class="enlace-abrir" href="{fname}">Abrir en pestaña →</a>
    </div>
    <div class="marco-interactivo{marco_extra}">
      {iframe}
    </div>
    <p class="fallback-enlace">{fallback}</p>
  </section>"""


def render_lesson(lesson: dict, *, offline: bool) -> str:
    n = lesson["n"]
    css = "leccion-shell.css" if offline else "../../_plantilla-leccion/leccion-shell.css"
    js = "leccion-shell-nav.js" if offline else "../../_plantilla-leccion/leccion-shell-nav.js"
    fig = (lambda f: f"figuras/{f}" if offline else f"../../_plantilla-leccion/figuras/{f}")
    home = "index.html" if offline else "../../../index.html"
    marca_meta = "1º ESO Matemáticas · offline" if offline else "1º ESO Matemáticas"
    icon_root = "icons" if offline else "../../../brand/favicon"
    manifest_href = "manifest.webmanifest" if offline else "../manifest.webmanifest"
    body_class = "leccion-shell offline-embed" if offline else "leccion-shell"

    objs = "".join(f"      <li>{o}</li>\n" for o in lesson["objetivos"])
    def _wblock(lab: str, fn: str) -> str:
        wh = None
        if offline:
            wh = load_widget_html(fn)
            assert_widget_offline_safe(fn, wh)
        return widget_block(lab, fn, offline=offline, widget_html=wh)

    widgets = lesson["widgets"]
    if lesson.get("widget_split") and len(widgets) >= 2:
        w_html = _wblock(*widgets[0])
        mid = lesson.get("cuerpo_after_widgets") or ""
        # wrap mid in section if present
        mid_html = f'  <section class="bloque-cuerpo">\n{mid}\n  </section>\n' if mid.strip() else ""
        w_html = w_html + "\n" + mid_html + _wblock(*widgets[1])
    else:
        w_html = "\n".join(_wblock(lab, fn) for lab, fn in widgets)


    # Omit empty curiosidad / vida (Jorge cleanup: no fake «Curiosidad histórica»)
    cur_text = (lesson.get("curiosidad") or "").strip()
    cur_title = (lesson.get("curiosidad_t") or "").strip()
    cur_label = (lesson.get("curiosidad_label") or "Curiosidad histórica").strip()
    if cur_text and cur_title and cur_label:
        curiosidad_html = f"""  <aside class="bloque-curiosidad">
    <p class="etiqueta-bloque">{cur_label}</p>
    <h2 class="titulo-curiosidad">{cur_title}</h2>
    <p class="texto-curiosidad">{cur_text}</p>
    <div class="ilustracion-slot">
      <img src="{fig(lesson.get('curiosidad_fig') or 'mapa.svg')}" width="96" height="96" alt=""/>
    </div>
  </aside>
"""
    else:
        curiosidad_html = ""

    vida_items = lesson.get("vida") or []
    vida_title = (lesson.get("vida_t") or "").strip()
    vida_html = ""
    if vida_items and vida_title:
        vida_lis = "".join(f"        <li>{v}</li>\n" for v in vida_items)
        vida_html = f"""  <section class="bloque-vida-real con-figura">
    <div class="figura" aria-hidden="true">
      <img src="{fig(lesson.get('vida_fig') or 'mapa.svg')}" width="96" height="96" alt=""/>
    </div>
    <div class="contenido-vida">
      <p class="etiqueta-bloque">En la vida real</p>
      <h2 class="titulo-vida">{vida_title}</h2>
      <ul>
{vida_lis}      </ul>
    </div>
  </section>
"""
    if lesson.get("vida2"):
        vida_html += f"""
  <section class="bloque-vida-real con-figura">
    <div class="figura" aria-hidden="true">
      <img src="{fig(lesson['vida2_fig'])}" width="96" height="96" alt=""/>
    </div>
    <div class="contenido-vida">
      <p class="etiqueta-bloque">En la vida real</p>
      <h2 class="titulo-vida">{lesson['vida2_t']}</h2>
      <p>{lesson['vida2']}</p>
    </div>
  </section>
"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#FAF7F0"/>
<title>Lección {n:02d} · {lesson['title_plain']} · Les vencimos</title>
<link rel="icon" href="{icon_root}/favicon.svg" type="image/svg+xml"/>
<link rel="icon" href="{icon_root}/favicon-32.png" sizes="32x32" type="image/png"/>
<link rel="apple-touch-icon" href="{icon_root}/apple-touch-icon.png"/>
<link rel="manifest" href="{manifest_href}"/>
<link rel="stylesheet" href="{css}"/>
<script src="{js}" defer></script>
</head>
<body class="{body_class}">
<div class="leccion-wrap">

{nav_html(n, offline=offline)}

  <header class="leccion-top">
    <a class="leccion-marca" href="{home}">Les <span>vencimos</span></a>
    <p class="leccion-meta-top">{marca_meta}</p>
  </header>

  <header class="bloque-titulo">
    <span class="eyebrow">{lesson['eyebrow']}</span>
    <h1 class="titulo-leccion">{lesson['title_html']}</h1>
    <p class="meta-leccion">{lesson['meta']}</p>
  </header>

{curiosidad_html}
  <section class="bloque-cuerpo">
    <h2>Objetivos</h2>
    <ol>
{objs}    </ol>
{lesson['cuerpo']}  </section>

{vida_html}
{w_html}

  <section class="bloque-cuerpo">
    <h2>Mini cierre</h2>
    <p>{lesson['cierre']}</p>
  </section>

  <section class="bloque-reto">
    <span class="etiqueta-reto">Reto Profesor</span>
    <h2 class="titulo-reto">{lesson['reto_t']}</h2>
    <p>{lesson['reto']}</p>
    <ul>
      <li>Ser clara: se entiende en una lectura.</li>
      <li>Conectar de verdad con lo aprendido en la lección.</li>
      <li>Aportar una idea concreta (lugar, persona o situación).</li>
    </ul>
    <p class="reto-id">reto_id: {lesson['reto_id']}</p>
  </section>

  <footer class="leccion-pie">
    <strong>Les vencimos</strong> · L{n:02d} de {TOTAL} · shell HTML · offline / file:// · sin instalar
  </footer>
</div>
</body>
</html>
"""


def write_redirect(path: pathlib.Path, target: str, label: str) -> None:
    path.write_text(f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta http-equiv="refresh" content="0; url={target}"/>
<link rel="canonical" href="{target}"/>
<title>{label} · redirige · Les vencimos</title>
<style>
  body{{font-family:system-ui,sans-serif;max-width:36rem;margin:2rem auto;padding:0 1rem;line-height:1.5;color:#2A2620;background:#FAF7F0}}
  a{{color:#2F5D7A}}
</style>
</head>
<body>
  <h1>{label}</h1>
  <p>Esta página se ha movido a <a href="{target}"><strong>{target}</strong></a>.</p>
  <p>Si no redirige sola, usa el enlace.</p>
</body>
</html>
""", encoding="utf-8")


def update_hub() -> None:
    text = HUB.read_text(encoding="utf-8")
    # status blurb (idempotent across AVAILABLE bumps)
    text = re.sub(
        r"<strong>Lecciones 01–\d{2} disponibles</strong> en shell HTML \(interactivos Mate\)\.",
        f"<strong>Lecciones 01–{AVAILABLE:02d} disponibles</strong> en shell HTML (interactivos Mate).",
        text,
        count=1,
    )
    text = re.sub(
        r"<strong>Lección 01 disponible</strong> en el shell visual \(interactivos Mate \+ presentación\)\.\s*"
        r"El resto del curso está <strong>en construcción</strong>[^<]*(?:<[^>]+>[^<]*)*?"
        r"<code>1eso-matematicas-offline\.zip</code>\).",
        f"<strong>Lecciones 01–{AVAILABLE:02d} disponibles</strong> en shell HTML (interactivos Mate).\n"
        "      El resto aparece como <strong>próximamente</strong>.\n"
        "      <strong>ZIP offline</strong> (sin instalar: descomprime y abre <code>index.html</code>) en "
        "<a href=\"../../descargas.html\">Descargas</a>.",
        text,
        count=1,
        flags=re.S,
    )
    text = text.replace(
        'href="lecciones/01-presentacion.html">Abrir lección 01 · Presentación →</a>',
        f'href="lecciones/{lesson_filename(1)}">Abrir lección 01 →</a>',
    )
    text = re.sub(
        r'href="lecciones/leccion-01(?:-[^"]+)?\.html"',
        f'href="lecciones/{lesson_filename(1)}"',
        text, count=1,
    )
    if 'rel="manifest"' not in text:
        text = text.replace(
            '</title>',
            '</title>\n<meta name="theme-color" content="#FAF7F0"/>\n'
            '<link rel="icon" href="../../brand/favicon/favicon.svg" type="image/svg+xml"/>\n'
            '<link rel="icon" href="../../brand/favicon/favicon-32.png" sizes="32x32" type="image/png"/>\n'
            '<link rel="apple-touch-icon" href="../../brand/favicon/apple-touch-icon.png"/>\n'
            '<link rel="manifest" href="manifest.webmanifest"/>',
            1,
        )
    text = re.sub(
        r"Disponibles L01–L\d{2} como <code>leccion-NN\.html</code>\.",
        f"Disponibles L01–L{AVAILABLE:02d} como <code>leccion-NN-titulo.html</code> (con alias <code>leccion-NN.html</code>).",
        text,
        count=1,
    )
    text = text.replace(
        "Solo enlazan las que ya tienen HTML de shell.",
        f"Disponibles L01–L{AVAILABLE:02d} como <code>leccion-NN-titulo.html</code> (con alias <code>leccion-NN.html</code>).",
    )
    if AVAILABLE >= TOTAL:
        text = text.replace("      El resto aparece como <strong>próximamente</strong>.\n", "")
        text = text.replace("Índice del temario (47 lecciones previstas).", "Índice completo del temario (47 lecciones).")
        text = text.replace("1º ESO Matemáticas · curso en marcha", "1º ESO Matemáticas · curso completo")

    # replace first AVAILABLE list items to link to leccion-NN
    titles = {L["n"]: L["title_plain"] for L in LESSONS}

    def item_available(n: int) -> str:
        return (
            f'      <li class="hub-item hub-disponible">\n'
            f'        <a href="lecciones/{lesson_filename(n)}">\n'
            f'          <span class="hub-num">{n:02d}</span>\n'
            f'          <span class="hub-titulo">{titles[n]}</span>\n'
            f'          <span class="hub-estado">Disponible</span>\n'
            f'        </a>\n'
            f'      </li>'
        )

    # Replace L01 and L02 presentacion blocks and L03-L09 pronto blocks
    # Simpler: rebuild the ol content for items 01-09 via regex on hub-num
    for n in range(1, AVAILABLE + 1):
        # match either available <a> or pronto span block for this number
        pat = re.compile(
            rf'      <li class="hub-item hub-(?:disponible|pronto)">\s*'
            rf'(?:<a href="lecciones/[^"]+">\s*)?'
            rf'<span class="hub-num">{n:02d}</span>\s*'
            rf'<span class="hub-titulo">[^<]*</span>\s*'
            rf'<span class="hub-estado">[^<]*</span>\s*'
            rf'(?:</a>\s*)?'
            rf'</li>',
            re.S,
        )
        text, count = pat.subn(item_available(n), text, count=1)
        if count != 1:
            print(f"WARN: hub item {n:02d} replacements={count}")
    HUB.write_text(text, encoding="utf-8")
    # downloads/ copy uses paths relative to downloads/
    hub_dl = text
    hub_dl = hub_dl.replace(
        'href="../_plantilla-leccion/leccion-shell.css"',
        'href="../profesor/_plantilla-leccion/leccion-shell.css"',
    )
    hub_dl = hub_dl.replace('href="../../index.html"', 'href="../index.html"')
    hub_dl = hub_dl.replace('href="../../descargas.html"', 'href="../descargas.html"')
    hub_dl = hub_dl.replace('href="lecciones/', 'href="../profesor/1eso-matematicas/lecciones/')
    hub_dl = hub_dl.replace('href="../../brand/favicon/', 'href="../brand/favicon/')
    hub_dl = hub_dl.replace('href="manifest.webmanifest"', 'href="../profesor/1eso-matematicas/manifest.webmanifest"')
    (REPO / "downloads/1eso-matematicas.html").write_text(hub_dl, encoding="utf-8")
    print("Updated hub (+ downloads copy)")


def update_descargas() -> None:
    text = DESCARGAS.read_text(encoding="utf-8")
    before = text
    # Idempotent bump of pack range + ensure wording
    text, n = re.subn(
        r'(Pack plano con lecciones <strong>)01–\d{2}(</strong>)',
        rf'\g<1>01–{AVAILABLE:02d}\2',
        text,
        count=1,
    )
    text = re.sub(
        r'href="/profesor/1eso-matematicas/lecciones/leccion-01(?:-[^"]+)?\.html"',
        f'href="/profesor/1eso-matematicas/lecciones/{lesson_filename(1)}"',
        text, count=1,
    )
    text = text.replace(">Descargar 1º ESO Matemáticas</a>", ">Descargar ZIP</a>")
    needle = f"Pack plano con lecciones <strong>01–{AVAILABLE:02d}</strong>"
    if needle not in text:
        text2 = re.sub(
            r'(<h2>1º ESO Matemáticas</h2>\s*<p class="kicker">[^<]*</p>\s*)<p>.*?</p>',
            rf'\1<p><strong>No se instala.</strong> Descomprime y abre <code>index.html</code>. '
            rf'Pack plano con lecciones <strong>01–{AVAILABLE:02d}</strong> (HTML + interactivos)'
            rf'{("; resto próximamente" if AVAILABLE < TOTAL else ", curso completo")}. Sin nube ni servidor.</p>',
            text,
            count=1,
            flags=re.S,
        )
        if needle not in text2:
            raise SystemExit("descargas.html pattern not found")
        text = text2
    if AVAILABLE >= TOTAL:
        text = text.replace("(HTML + interactivos); resto próximamente.", "(HTML + interactivos), curso completo.")
        text = text.replace("Oficial CyL · Decreto 39/2022 · en marcha", "Oficial CyL · Decreto 39/2022 · curso completo")
    if text != before:
        DESCARGAS.write_text(text, encoding="utf-8")
        print("Updated descargas")
    else:
        print("descargas already up to date")


def update_plantilla_readme() -> None:
    readme = PLANTILLA / "README.md"
    text = readme.read_text(encoding="utf-8")
    block = """

## Naming canónico · `leccion-NN-titulo.html` + pack offline plano

- **Online (sitio):** `profesor/1eso-matematicas/lecciones/leccion-01-tema.html` … `leccion-47-tema.html`; el prefijo NN conserva el orden en Descargas.
  CSS/JS: `../../_plantilla-leccion/leccion-shell.css` (+ `leccion-shell-nav.js`).
  Calculadora: `../../../modulos/calculadora.html`.
  Prev/next: usan siempre el nombre con slug; los iframes `l0N-….html` siguen en la misma carpeta.
- **Offline (ZIP plano):** una sola carpeta con `ABRE-AQUI.html` (= `index.html`), `LEEME.md`, `leccion-NN-titulo.html`, alias `leccion-NN.html`, widgets `l0N-….html`,
  y **vendor** de `leccion-shell.css`, `leccion-shell-nav.js`, `calculadora.html`, `figuras/*.svg` e `icons/*`.
  En offline los interactivos van **embebidos** (`iframe srcdoc=…`) para que animaciones funcionen en Android `file://`.
- Los alias antiguos (`leccion-NN.html`, `01-presentacion.html`) redirigen al archivo con slug para no romper enlaces.
- El alumno **no instala nada**: descomprime el ZIP y abre `ABRE-AQUI.html` / `index.html` desde la carpeta descomprimida (`file://`), nunca desde Descargas `content://`.
"""
    section_re = re.compile(r"\n## Naming canónico .*?(?=\n## Qué no hacer)", re.S)
    if section_re.search(text):
        text = section_re.sub(block.rstrip("\n"), text, count=1)
    elif "## Qué no hacer" in text:
        text = text.replace("## Qué no hacer", block + "\n## Qué no hacer", 1)
    else:
        text += block
    readme.write_text(text, encoding="utf-8")
    print("Updated plantilla README")


def build_offline_pack() -> None:
    if PACK_DIR.exists():
        shutil.rmtree(PACK_DIR)
    root = PACK_DIR / "1eso-matematicas-offline"
    root.mkdir(parents=True)

    # LEEME first lines critical
    (root / "LEEME.md").write_text(
        f"""# 1º ESO Matemáticas — pack offline

No hay que instalar nada. Descomprime y abre **ABRE-AQUI.html** (o index.html).

**Qué es:** lecciones de **Educación obligatoria** (currículo oficial Castilla y León, Decreto 39/2022).
Este pack trae las lecciones **01–{AVAILABLE:02d}** en HTML plano (shell + interactivos Mate embebidos).

**Cómo abrir (Android / PC) — 4 pasos**

1. Descarga el ZIP.
2. Abre **Archivos / Mis archivos** (NO la lista Descargas del navegador).
3. Descomprime y entra en la carpeta `1eso-matematicas-offline`.
4. Toca **`ABRE-AQUI.html`** o **`index.html`** → Chrome / Samsung Internet.

Todo funciona **offline**, sin nube ni servidor (`file://`). Sin instalación, sin app store, sin «setup».

**Importante en Android:** abre siempre desde la **carpeta descomprimida** (`file://`).
**Nunca** abras el HTML desde la lista Descargas del navegador (`content://`): ahí fallan
imágenes, CSS e interactivos/animaciones.
En Chrome/Android: menú → **Añadir a pantalla de inicio**.

Los interactivos van **embebidos** en cada lección (funcionan sin cargar iframes hermanos).
Si hace falta, cada lección sigue teniendo el enlace «Abrir en pestaña →» al widget suelto.

**Contenido:** `ABRE-AQUI.html`, `index.html`, `LEEME.md`, `leccion-NN-titulo.html` (con slugs),
alias `leccion-NN.html`, widgets `lNN-….html`, calculadora, CSS/JS, `figuras/*.svg` e iconos —
todo en la misma carpeta.
""",
        encoding="utf-8",
    )

    # index hub
    items = []
    for L in LESSONS:
        items.append(
            f'    <li class="ok"><a href="{lesson_filename(L["n"])}"><strong>L{L["n"]:02d}</strong> — {L["title_plain"]}</a></li>'
        )
    if AVAILABLE < TOTAL:
        for n in range(AVAILABLE + 1, min(AVAILABLE + 6, TOTAL + 1)):
            items.append(f'    <li class="soon"><span><strong>L{n:02d}</strong> — próximamente</span></li>')
        items.append(f'    <li class="soon"><span>… hasta L{TOTAL} — próximamente</span></li>')

    (root / "index.html").write_text(
        f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#FAF7F0"/>
<title>1º ESO Matemáticas · offline · Les vencimos</title>
<link rel="icon" href="icons/favicon.svg" type="image/svg+xml"/>
<link rel="icon" href="icons/favicon-32.png" sizes="32x32" type="image/png"/>
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png"/>
<link rel="manifest" href="manifest.webmanifest"/>
<link rel="stylesheet" href="leccion-shell.css"/>
<style>
  .hub-lista-flat{{list-style:none;padding:0;margin:1.25rem 0 0;display:grid;gap:0.55rem}}
  .hub-lista-flat li{{background:#fff;border:1px solid #E8E0D0;border-radius:12px;padding:0.85rem 1rem}}
  .hub-lista-flat li.ok a{{color:#2F5D7A;text-decoration:none;font-weight:600}}
  .hub-lista-flat li.ok a:hover{{text-decoration:underline}}
  .hub-lista-flat li.soon{{color:#5C564C;opacity:0.85}}
  .big-cta{{display:inline-block;margin-top:1rem;padding:0.85rem 1.35rem;background:#C4A15A;color:#0E0E0C;border-radius:999px;font-weight:700;text-decoration:none}}
  .no-install{{background:#EAF3EC;border:1px solid #B7D0BE;border-radius:12px;padding:0.9rem 1rem;margin:1rem 0}}
</style>
</head>
<body class="leccion-shell">
<div class="leccion-wrap">
  <header class="leccion-top">
    <a class="leccion-marca" href="index.html">Les <span>vencimos</span></a>
    <p class="leccion-meta-top">Pack offline</p>
  </header>
  <header class="bloque-titulo">
    <span class="eyebrow">Educación obligatoria · CyL</span>
    <h1 class="titulo-leccion">1º ESO Matemáticas</h1>
    <p class="meta-leccion">Lecciones 01–{AVAILABLE:02d} listas · curso completo</p>
  </header>
  <div class="no-install">
    <strong>No hay que instalar nada.</strong> Abre <code>ABRE-AQUI.html</code> o <code>index.html</code> desde esta carpeta
    (Archivos / Mis archivos → carpeta descomprimida → <code>file://</code>).
    Los interactivos van embebidos en cada lección.
    En Chrome/Android: menú → <strong>Añadir a pantalla de inicio</strong>.
    <strong>Nunca</strong> abras desde la lista Descargas del navegador (<code>content://</code>).
  </div>
  <p><a class="big-cta" href="{lesson_filename(1)}">Abrir lección 01 →</a>
     &nbsp; <a href="calculadora.html">Calculadora</a></p>
  <p class="hub-nota">Los nombres incluyen un slug del tema para reconocer cada archivo en Archivos/Descargas; usa siempre este índice.</p>
  <section class="bloque-cuerpo">
    <h2>Lecciones</h2>
    <ol class="hub-lista-flat">
{chr(10).join(items)}
    </ol>
  </section>
  <footer class="leccion-pie"><strong>Les vencimos</strong> · pack plano · sin instalar · lee LEEME.md</footer>
</div>
</body>
</html>
""",
        encoding="utf-8",
    )
    # Entry UX like Estantería: same hub under a clear Android-friendly name
    (root / "ABRE-AQUI.html").write_text(
        (root / "index.html").read_text(encoding="utf-8"), encoding="utf-8"
    )

    # vendor css/js/figuras/calc/icons
    shutil.copy2(PLANTILLA / "leccion-shell.css", root / "leccion-shell.css")
    shutil.copy2(PLANTILLA / "leccion-shell-nav.js", root / "leccion-shell-nav.js")
    shutil.copy2(REPO / "modulos/calculadora.html", root / "calculadora.html")
    icons_dst = root / "icons"
    icons_dst.mkdir()
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "app-icon-512.png"):
        shutil.copy2(BRAND_ICONS / name, icons_dst / name)
    (root / "manifest.webmanifest").write_text(manifest_text(), encoding="utf-8")

    fig_dst = root / "figuras"
    fig_dst.mkdir()
    for svg in (PLANTILLA / "figuras").glob("*.svg"):
        shutil.copy2(svg, fig_dst / svg.name)

    # lessons + widgets
    widget_files = set()
    for L in LESSONS:
        (root / lesson_filename(L["n"])).write_text(
            render_lesson(L, offline=True), encoding="utf-8"
        )
        write_redirect(root / f"leccion-{L['n']:02d}.html", lesson_filename(L["n"]), f"Lección {L['n']:02d}")
        for _, wf in L["widgets"]:
            widget_files.add(wf)
    for wf in sorted(widget_files):
        src = LEC / wf
        if not src.exists():
            raise SystemExit(f"missing widget {wf}")
        wh = src.read_text(encoding="utf-8")
        assert_widget_offline_safe(wf, wh)
        shutil.copy2(src, root / wf)

    # zip: put files at root of zip (folder name as top-level)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                arc = path.relative_to(PACK_DIR).as_posix()
                zf.write(path, arc)
    size = ZIP_PATH.stat().st_size
    print(f"Wrote {ZIP_PATH} ({size} bytes)")
    # keep build dir for inspection? remove to avoid accidental commit
    shutil.rmtree(PACK_DIR)


def main() -> None:
    # Online lesson pages
    ensure_course_branding()
    for L in LESSONS:
        out = LEC / lesson_filename(L["n"])
        out.write_text(render_lesson(L, offline=False), encoding="utf-8")
        write_redirect(LEC / f"leccion-{L['n']:02d}.html", out.name, f"Lección {L['n']:02d} (alias)")
        print("Wrote", out.name)

    write_redirect(LEC / "01-presentacion.html", lesson_filename(1), "Lección 01 (alias)")
    write_redirect(LEC / "02-presentacion.html", lesson_filename(2), "Lección 02 (alias)")

    update_hub()
    update_descargas()
    update_plantilla_readme()
    build_offline_pack()
    print("DONE available=", AVAILABLE)


if __name__ == "__main__":
    main()
