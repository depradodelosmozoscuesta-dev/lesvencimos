#!/usr/bin/env python3
"""Build leccion-NN.html shells (online + flat offline pack) for 1º ESO Mate."""
from __future__ import annotations

import pathlib
import re
import shutil
import zipfile

REPO = pathlib.Path("/workspace/lesvencimos")
LEC = REPO / "profesor/1eso-matematicas/lecciones"
PLANTILLA = REPO / "profesor/_plantilla-leccion"
HUB = REPO / "profesor/1eso-matematicas/1eso-matematicas.html"
DESCARGAS = REPO / "descargas.html"
PACK_DIR = REPO / "downloads/_build-1eso-mate-flat"
ZIP_PATH = REPO / "downloads/1eso-matematicas-offline.zip"
TOTAL = 47
AVAILABLE = 9  # L01–L09

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
    "vida_t": "Aplicaciones",
    "vida": [
      "Excursión del instituto: plazas del autobús, menús, presupuesto en €.",
      "¿Da tiempo a llegar andando al polideportivo?",
      "Repartir turnos de limpieza o cocina sin pelearse «a ojo».",
      "Cuando falta un dato, replantear con calma en lugar de abandonar.",
    ],
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
    "vida_t": "Aplicaciones",
    "vida": [
      "Leer años en monumentos o iglesias escritos en números romanos.",
      "Entender por qué las horas tienen 60 minutos.",
      "Importes en €: 12,05 € ≠ 12,50 € (el orden de las cifras importa).",
      "Códigos postales y números de teléfono.",
    ],
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
    "curiosidad_t": "Las casitas del valor",
    "curiosidad": "Imagina pisos en un edificio: planta baja = unidades (×1), 1.º = decenas (×10), 2.º = centenas (×100)… Misma cifra 5, distinto piso, distinto «alquiler». Sin valor posicional no hay fracciones, enteros ni álgebra cómodos.",
    "curiosidad_fig": "mapa.svg",
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
    "vida_t": "Aplicaciones",
    "vida": [
      "Odómetro del coche o habitantes de tu municipio (INE).",
      "Precio de una bicicleta: 1 299 € son mil euros, no «doce noventa y nueve».",
      "Numeración de calles, dorsal de carrera o escolar.",
      "Contar asistencia en un partido del equipo local.",
    ],
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
    "vida_t": "Aplicaciones",
    "vida": [
      "Comparar precios de dos mochilas en el escaparate.",
      "Quién llegó antes en una carrera (orden de tiempos).",
      "Cola del comedor: ticket más bajo suele entrar antes.",
      "Distancias en km entre pueblos de CyL.",
    ],
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
    "vida_t": "Aplicaciones",
    "vida": [
      "¿Caben 18,90 € + 7,25 € + 3,10 € en un billete de 30 €?",
      "Tiempo estimado de viaje (el GPS ya redondea minutos).",
      "Material escolar: «unas 40 carpetas» para un curso.",
      "Periodismo local: «cerca de 2 500 asistentes».",
    ],
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
    "curiosidad_t": "Cajas, filas y un criptograma",
    "curiosidad": "Multiplicar es juntar grupos iguales (filas × columnas de botellas). Dividir es repartir. Si a×b=p, entonces p÷b=a. Las propiedades (conmutativa, asociativa, distributiva) son atajos — y un criptograma de productos premia calcular bien.",
    "curiosidad_fig": "olla.svg",
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
    "vida_t": "Aplicaciones",
    "vida": [
      "Cajas de huevos, packs de agua, bandejas del mercadillo.",
      "Precio total: unidades × precio unitario.",
      "Repartir cromos, asientos o turnos en grupos iguales.",
      "Estimar si «me llega el dinero» antes de pagar.",
    ],
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
    "curiosidad_t": "Torre de factores",
    "curiosidad": "aⁿ significa a multiplicado por sí mismo n veces (una torre de n pisos). El cuadrado s² es el área de un cuadrado de lado s; la raíz √q es el lado cuando q es cuadrado perfecto. No intercambies base y exponente sin pensar.",
    "curiosidad_fig": "mapa.svg",
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
    "vida_t": "Aplicaciones",
    "vida": [
      "Baldosas o azulejos en cuadrado (área = lado × lado).",
      "Papel cuadriculado: contar cuadraditos.",
      "Leer bien el enunciado antes de elevar o «duplicar».",
      "Estimar si un número «parece» cuadrado perfecto.",
    ],
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
    "curiosidad_t": "Cadena de oro",
    "curiosidad": "dato → representación → operación → comprobación → frase con unidades. El significado elige la operación; el orden y los paréntesis evitan trampas. Una excursión CyL (autobús, entrada, merienda) lo deja claro.",
    "curiosidad_fig": "mapa.svg",
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
    "vida_t": "Aplicaciones",
    "vida": [
      "Presupuesto de una excursión (entradas × personas + autobús).",
      "Compra en el mercadillo (packs × precio).",
      "Reparto de merienda o material.",
      "«¿Me llega?» antes de pagar con un billete.",
    ],
    "vida_fig": "ticket.svg",
    "widgets": [
      ("Interactivo · excursión CyL", "l09-excursion-problemas.html"),
    ],
    "reto_t": "Un problema de mi semana",
    "reto": "Inventa un problema corto (3–5 frases) de tu semana que mezcle al menos dos operaciones. Resuélvelo con la cadena de oro y una frase final con unidades.",
    "reto_id": "1eso-mate-L09",
    "cierre": "El significado elige la operación. El orden y los paréntesis evitan trampas. Siempre: frase con unidades.",
  },
]


def progress_pct(n: int) -> str:
    return f"{(n / TOTAL) * 100:.2f}".rstrip("0").rstrip(".")


def nav_html(n: int, *, offline: bool) -> str:
    calc = "calculadora.html" if offline else "../../../modulos/calculadora.html"
    if n <= 1:
        prev = '<span class="atajo atajo-prev is-disabled" aria-disabled="true" title="Primera lección">← Anterior</span>'
    else:
        prev = f'<a class="atajo atajo-prev" href="leccion-{n-1:02d}.html" title="Lección {n-1:02d}">← Anterior</a>'
    if n >= AVAILABLE:
        nxt = '<span class="atajo atajo-next is-disabled" aria-disabled="true" title="Próximamente">Siguiente →</span>'
    else:
        nxt = f'<a class="atajo atajo-next" href="leccion-{n+1:02d}.html" title="Lección {n+1:02d}">Siguiente →</a>'
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


def widget_block(label: str, fname: str) -> str:
    return f"""  <section class="bloque-interactivo">
    <div class="marco-interactivo-cabecera">
      <span class="etiqueta-interactivo">{label}</span>
      <a class="enlace-abrir" href="{fname}">Abrir en pestaña →</a>
    </div>
    <div class="marco-interactivo">
      <iframe title="{label}" src="{fname}" loading="lazy"></iframe>
    </div>
    <p class="fallback-enlace">Si el marco no carga (<code>file://</code>), abre <a href="{fname}">{fname}</a>.</p>
  </section>"""


def render_lesson(lesson: dict, *, offline: bool) -> str:
    n = lesson["n"]
    css = "leccion-shell.css" if offline else "../../_plantilla-leccion/leccion-shell.css"
    js = "leccion-shell-nav.js" if offline else "../../_plantilla-leccion/leccion-shell-nav.js"
    fig = (lambda f: f"figuras/{f}" if offline else f"../../_plantilla-leccion/figuras/{f}")
    home = "index.html" if offline else "../../../index.html"
    marca_meta = "1º ESO Matemáticas · offline" if offline else "1º ESO Matemáticas"

    objs = "".join(f"      <li>{o}</li>\n" for o in lesson["objetivos"])
    vida_lis = "".join(f"        <li>{v}</li>\n" for v in lesson["vida"])

    widgets = lesson["widgets"]
    if lesson.get("widget_split") and len(widgets) >= 2:
        w_html = widget_block(*widgets[0])
        mid = lesson.get("cuerpo_after_widgets") or ""
        # wrap mid in section if present
        mid_html = f'  <section class="bloque-cuerpo">\n{mid}\n  </section>\n' if mid.strip() else ""
        w_html = w_html + "\n" + mid_html + widget_block(*widgets[1])
    else:
        w_html = "\n".join(widget_block(lab, fn) for lab, fn in widgets)

    vida2 = ""
    if lesson.get("vida2"):
        vida2 = f"""
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
<title>Lección {n:02d} · {lesson['title_plain']} · Les vencimos</title>
<link rel="stylesheet" href="{css}"/>
<script src="{js}" defer></script>
</head>
<body class="leccion-shell">
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

  <aside class="bloque-curiosidad">
    <p class="etiqueta-bloque">Curiosidad histórica</p>
    <h2 class="titulo-curiosidad">{lesson['curiosidad_t']}</h2>
    <p class="texto-curiosidad">{lesson['curiosidad']}</p>
    <div class="ilustracion-slot">
      <img src="{fig(lesson['curiosidad_fig'])}" width="96" height="96" alt=""/>
    </div>
  </aside>

  <section class="bloque-cuerpo">
    <h2>Objetivos</h2>
    <ol>
{objs}    </ol>
{lesson['cuerpo']}  </section>

  <section class="bloque-vida-real con-figura">
    <div class="figura" aria-hidden="true">
      <img src="{fig(lesson['vida_fig'])}" width="96" height="96" alt=""/>
    </div>
    <div class="contenido-vida">
      <p class="etiqueta-bloque">En la vida real</p>
      <h2 class="titulo-vida">{lesson['vida_t']}</h2>
      <ul>
{vida_lis}      </ul>
    </div>
  </section>
{vida2}
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
    # status blurb
    text = text.replace(
        "<strong>Lección 01 disponible</strong> en el shell visual (interactivos Mate + presentación).\n"
        "      El resto del curso está <strong>en construcción</strong> — no hay un lector masivo de los 47 borradores Markdown.\n"
        "      También hay <strong>ZIP offline</strong> en <a href=\"../../descargas.html\">Descargas</a> (<code>1eso-matematicas-offline.zip</code>).",
        f"<strong>Lecciones 01–{AVAILABLE:02d} disponibles</strong> en shell HTML (interactivos Mate).\n"
        "      El resto aparece como <strong>próximamente</strong>.\n"
        "      <strong>ZIP offline</strong> (sin instalar: descomprime y abre <code>index.html</code>) en "
        "<a href=\"../../descargas.html\">Descargas</a>."
    )
    text = text.replace(
        'href="lecciones/01-presentacion.html">Abrir lección 01 · Presentación →</a>',
        'href="lecciones/leccion-01.html">Abrir lección 01 →</a>',
    )
    text = text.replace(
        "Solo enlazan las que ya tienen HTML de shell.",
        f"Disponibles L01–L{AVAILABLE:02d} como <code>leccion-NN.html</code>.",
    )
    # replace first AVAILABLE list items to link to leccion-NN
    titles = {L["n"]: L["title_plain"] for L in LESSONS}

    def item_available(n: int) -> str:
        return (
            f'      <li class="hub-item hub-disponible">\n'
            f'        <a href="lecciones/leccion-{n:02d}.html">\n'
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
    print("Updated hub")


def update_descargas() -> None:
    text = DESCARGAS.read_text(encoding="utf-8")
    old = (
        "<p>Puedes <strong>descargar y usar offline</strong> (sin nube). Incluye <strong>Lección 01</strong> "
        "con interactivos (shell luminoso); más lecciones más adelante.</p>\n"
        "            <div class=\"actions\">\n"
        "              <a class=\"btn-download\" href=\"/downloads/1eso-matematicas-offline.zip\" "
        "download=\"1eso-matematicas-offline.zip\">Descargar 1º ESO Matemáticas</a>\n"
        "              <a class=\"textlink\" href=\"/profesor/1eso-matematicas/lecciones/01-presentacion.html\">"
        "Abrir lección 01</a>\n"
        "              <a class=\"textlink\" href=\"/profesor/1eso-matematicas/1eso-matematicas.html\">"
        "Índice del curso</a>"
    )
    new = (
        "<p><strong>No se instala.</strong> Descomprime y abre <code>index.html</code>. "
        f"Pack plano con lecciones <strong>01–{AVAILABLE:02d}</strong> (HTML + interactivos); "
        "resto próximamente. Sin nube ni servidor.</p>\n"
        "            <div class=\"actions\">\n"
        "              <a class=\"btn-download\" href=\"/downloads/1eso-matematicas-offline.zip\" "
        "download=\"1eso-matematicas-offline.zip\">Descargar ZIP</a>\n"
        "              <a class=\"textlink\" href=\"/profesor/1eso-matematicas/lecciones/leccion-01.html\">"
        "Abrir lección 01</a>\n"
        "              <a class=\"textlink\" href=\"/profesor/1eso-matematicas/1eso-matematicas.html\">"
        "Índice del curso</a>"
    )
    if old not in text:
        # try softer replace
        text2 = re.sub(
            r'(<h2>1º ESO Matemáticas</h2>\s*<p class="kicker">[^<]*</p>\s*)<p>.*?</p>',
            rf'\1<p><strong>No se instala.</strong> Descomprime y abre <code>index.html</code>. '
            rf'Pack plano con lecciones <strong>01–{AVAILABLE:02d}</strong> (HTML + interactivos); '
            rf'resto próximamente. Sin nube ni servidor.</p>',
            text,
            count=1,
            flags=re.S,
        )
        text2 = text2.replace(
            'href="/profesor/1eso-matematicas/lecciones/01-presentacion.html"',
            'href="/profesor/1eso-matematicas/lecciones/leccion-01.html"',
        )
        text2 = text2.replace(
            ">Descargar 1º ESO Matemáticas</a>",
            ">Descargar ZIP</a>",
        )
        if text2 == text:
            raise SystemExit("descargas.html pattern not found")
        text = text2
    else:
        text = text.replace(old, new)
    DESCARGAS.write_text(text, encoding="utf-8")
    print("Updated descargas")


def update_plantilla_readme() -> None:
    readme = PLANTILLA / "README.md"
    text = readme.read_text(encoding="utf-8")
    block = """

## Naming canónico · `leccion-NN.html` + pack offline plano

- **Online (sitio):** `profesor/1eso-matematicas/lecciones/leccion-01.html` … `leccion-47.html` (cero-padded).
  CSS/JS: `../../_plantilla-leccion/leccion-shell.css` (+ `leccion-shell-nav.js`).
  Calculadora: `../../../modulos/calculadora.html`.
  Prev/next: `leccion-0N-1.html` / `leccion-0N+1.html`. Iframes: `l0N-….html` en la misma carpeta.
- **Offline (ZIP plano):** una sola carpeta con `index.html`, `LEEME.md`, `leccion-NN.html`, widgets `l0N-….html`,
  y **vendor** de `leccion-shell.css`, `leccion-shell-nav.js`, `calculadora.html`, `figuras/*.svg`
  (mismas rutas relativas en la raíz del pack: sin carpetas `profesor/` anidadas).
- Alias antiguos (`01-presentacion.html`) redirigen a `leccion-01.html` para no romper enlaces.
- El alumno **no instala nada**: descomprime el ZIP y abre `index.html`.
"""
    if "Naming canónico" not in text:
        # insert before "## Qué no hacer"
        if "## Qué no hacer" in text:
            text = text.replace("## Qué no hacer", block + "\n## Qué no hacer")
        else:
            text += block
        # update demo paths mention
        text = text.replace(
            "`profesor/1eso-matematicas/lecciones/01-presentacion.html`",
            "`profesor/1eso-matematicas/lecciones/leccion-01.html`",
        )
        readme.write_text(text, encoding="utf-8")
        print("Updated plantilla README")
    else:
        print("Plantilla README already has naming section")


def build_offline_pack() -> None:
    if PACK_DIR.exists():
        shutil.rmtree(PACK_DIR)
    root = PACK_DIR / "1eso-matematicas-offline"
    root.mkdir(parents=True)

    # LEEME first lines critical
    (root / "LEEME.md").write_text(
        """# 1º ESO Matemáticas — pack offline

No hay que instalar nada. Descomprime y abre index.html

**Qué es:** lecciones de **Educación obligatoria** (currículo oficial Castilla y León, Decreto 39/2022).
Este pack trae las lecciones **01–09** en HTML plano (shell + interactivos Mate). El resto irá entrando como *próximamente*.

**Cómo abrir (3 pasos)**

1. Descomprime este ZIP donde quieras.
2. Entra en la carpeta `1eso-matematicas-offline` (o la raíz del ZIP si ya están los archivos ahí).
3. Abre **`index.html`** con el navegador (doble clic o arrastrar).

Todo funciona **offline**, sin nube ni servidor (`file://`). Sin instalación, sin app store, sin «setup».

**Android:** descomprime con **Archivos / Mis archivos** y abre `index.html` desde ahí (`file://`).
Abrir desde la lista «Descargas» del navegador a veces usa `content://` y falla peor.

**Contenido:** `leccion-01.html` … `leccion-09.html`, widgets `l0N-….html`, calculadora, CSS/JS del shell y figuras SVG — todo en la misma carpeta.
""",
        encoding="utf-8",
    )

    # index hub
    items = []
    for L in LESSONS:
        items.append(
            f'    <li class="ok"><a href="leccion-{L["n"]:02d}.html"><strong>L{L["n"]:02d}</strong> — {L["title_plain"]}</a></li>'
        )
    for n in range(AVAILABLE + 1, min(AVAILABLE + 6, TOTAL + 1)):
        items.append(f'    <li class="soon"><span><strong>L{n:02d}</strong> — próximamente</span></li>')
    items.append(f'    <li class="soon"><span>… hasta L{TOTAL} — próximamente</span></li>')

    (root / "index.html").write_text(
        f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>1º ESO Matemáticas · offline · Les vencimos</title>
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
    <p class="meta-leccion">Lecciones 01–{AVAILABLE:02d} listas · resto próximamente · {TOTAL} previstas</p>
  </header>
  <div class="no-install">
    <strong>No hay que instalar nada.</strong> Descomprime y abre <code>index.html</code>.
    Todo es HTML que se abre en el navegador (<code>file://</code>).
  </div>
  <p><a class="big-cta" href="leccion-01.html">Abrir lección 01 →</a>
     &nbsp; <a href="calculadora.html">Calculadora</a></p>
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

    # vendor css/js/figuras/calc
    shutil.copy2(PLANTILLA / "leccion-shell.css", root / "leccion-shell.css")
    shutil.copy2(PLANTILLA / "leccion-shell-nav.js", root / "leccion-shell-nav.js")
    shutil.copy2(REPO / "modulos/calculadora.html", root / "calculadora.html")
    fig_dst = root / "figuras"
    fig_dst.mkdir()
    for svg in (PLANTILLA / "figuras").glob("*.svg"):
        shutil.copy2(svg, fig_dst / svg.name)

    # lessons + widgets
    widget_files = set()
    for L in LESSONS:
        (root / f"leccion-{L['n']:02d}.html").write_text(
            render_lesson(L, offline=True), encoding="utf-8"
        )
        for _, wf in L["widgets"]:
            widget_files.add(wf)
    for wf in sorted(widget_files):
        src = LEC / wf
        if not src.exists():
            raise SystemExit(f"missing widget {wf}")
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
    for L in LESSONS:
        out = LEC / f"leccion-{L['n']:02d}.html"
        out.write_text(render_lesson(L, offline=False), encoding="utf-8")
        print("Wrote", out.name)

    write_redirect(LEC / "01-presentacion.html", "leccion-01.html", "Lección 01 (alias)")
    write_redirect(LEC / "02-presentacion.html", "leccion-02.html", "Lección 02 (alias)")

    update_hub()
    update_descargas()
    update_plantilla_readme()
    build_offline_pack()
    print("DONE available=", AVAILABLE)


if __name__ == "__main__":
    main()
