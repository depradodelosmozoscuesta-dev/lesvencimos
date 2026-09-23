#!/usr/bin/env python3
"""Build online shell + flat offline pack for 1º ESO Biología y Geología (L01–L10)."""
from __future__ import annotations

import html
import json
import pathlib
import re
import shutil
import zipfile

REPO = pathlib.Path("/workspace/lesvencimos")
COURSE_DIR = REPO / "profesor/1eso-biologia-geologia"
LEC = COURSE_DIR / "lecciones"
PLANTILLA = REPO / "profesor/_plantilla-leccion"
HUB = COURSE_DIR / "1eso-biologia-geologia.html"
DESCARGAS = REPO / "descargas.html"
INDEX = REPO / "index.html"
PACK_DIR = REPO / "downloads/_build-1eso-byg-flat"
ZIP_PATH = REPO / "downloads/1eso-biologia-geologia-offline.zip"
COURSE_ICONS = COURSE_DIR / "icons"
BRAND_ICONS = REPO / "brand/favicon"
TOTAL = 40
AVAILABLE = 10

# Full temario titles (L11–L40 shown as próximamente on hub)
TEMARIO = [
    "El método científico en experimentos sencillos",
    "Fuentes veraces frente a bulos y pseudociencia",
    "Laboratorio: instrumentos, espacios y normas de seguridad",
    "Observar, tomar datos, modelar y presentar resultados",
    "Científicas y científicos que cambiaron la biología y la geología",
    "Rocas y minerales: qué son y en qué se diferencian",
    "Clasificar rocas: sedimentarias, metamórficas e ígneas",
    "El ciclo de las rocas",
    "Rocas y minerales relevantes (con foco en Castilla y León)",
    "Extracción minera: aplicaciones, economía y sociedad en CyL",
    "Estructura de la geosfera y movimientos de la Tierra",
    "Atmósfera: composición y estructura",
    "Contaminación, efecto invernadero, ozono y Agenda 2030",
    "Hidrosfera y el ciclo del agua",
    "Mares, aguas continentales, contaminación y uso sostenible",
    "Por qué atmósfera e hidrosfera hacen posible la vida",
    "La célula: unidad estructural y funcional",
    "Célula procariota y sus partes",
    "Célula eucariota animal y sus partes",
    "Célula eucariota vegetal y sus partes",
    "Observar y comparar células al microscopio",
    "Funciones vitales: nutrición, relación y reproducción",
    "Clasificación, nomenclatura binomial y especies de CyL",
    "De los antiguos reinos a los dominios actuales",
    "Hongos: características y micología en Castilla y León",
    "Plantas: grupos, flor, fruto y semilla",
    "Animales invertebrados: anatomía y fisiología básicas",
    "Animales vertebrados y animales como seres sintientes",
    "Identificar especies del entorno (guías y claves)",
    "Ecosistemas del entorno y sus elementos",
    "Relaciones intraespecíficas e interespecíficas",
    "Cadenas, redes y pirámides tróficas",
    "Conservar ecosistemas, biodiversidad y desarrollo sostenible",
    "Especies amenazadas y figuras de protección ambiental",
    "Atmósfera, hidrosfera, geosfera y biosfera: suelo y relieve",
    "Cambio climático y consecuencias en los ecosistemas",
    "Hábitos sostenibles (consumo, residuos, respeto al medio)",
    "One Health: salud ambiental, humana y de otros seres vivos",
    "Proyecto integrador del curso (ciencia + entorno CyL)",
    "Autoevaluación, portfolio y hábitos de trabajo científico",
]

LESSONS = [
    {
        "n": 1,
        "slug": "el-metodo-cientifico-en-experimentos-sencillos",
        "eyebrow": "Lección 01 · UD A · Proyecto científico",
        "title_html": "El <em>método científico</em> en experimentos sencillos",
        "title_plain": "El método científico en experimentos sencillos",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque A",
        "curiosidad_t": "Probar antes de creer",
        "curiosidad": (
            "Hace casi mil años, Ibn al-Haytham (Alhazén) insistió en comprobar "
            "las ideas sobre la luz con experimentos, no solo con argumentos. "
            "Ese hábito —observar, preguntar y poner a prueba— es el germen del "
            "método científico que usas en el laboratorio de Biología y Geología."
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            "Nombrar y ordenar los pasos del <strong>método científico</strong> en un experimento sencillo.",
            "Distinguir <strong>observación</strong>, <strong>pregunta</strong>, <strong>hipótesis</strong>, <strong>experimento</strong>, <strong>datos</strong> y <strong>conclusión</strong>.",
            "Reconocer qué es una <strong>hipótesis comprobable</strong> y qué no lo es.",
            "Identificar la <strong>variable</strong> que cambias y lo que dejas igual (<strong>control</strong>).",
            "Aplicar el método a una escena real: un <strong>cubito de hielo</strong> que se derrite.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>La ciencia no es «adivinar a ciegas». Es un <strong>camino ordenado</strong> para entender la naturaleza con pruebas. Ese camino se llama <strong>método científico</strong>.</p>
    <div class="tarjeta">
      <p style="margin:0">En un colegio de <strong>Valladolid</strong>, Lucía deja un <strong>cubito de hielo</strong> en un vaso. Al rato es más pequeño y hay más agua. Marcos dice: «¡Se ha evaporado!». Lucía: «No lo sé todavía… vamos a <strong>investigarlo</strong> como científicos».</p>
    </div>
    <h2>Los 6 pasos</h2>
    <ol>
      <li><strong>Observar</strong> — mirar con atención y anotar lo que ves (sin inventar aún la causa).</li>
      <li><strong>Preguntar</strong> — convertir la curiosidad en una pregunta investigable.</li>
      <li><strong>Hipotetizar</strong> — proponer una hipótesis: explicación <strong>comprobable</strong>.</li>
      <li><strong>Experimentar</strong> — prueba justa (cambiar una cosa, controlar el resto).</li>
      <li><strong>Tomar datos</strong> — medir y anotar (números, dibujos, tablas).</li>
      <li><strong>Concluir</strong> — decidir si los datos apoyan o no la hipótesis.</li>
    </ol>
    <div class="tarjeta">
      <p style="margin:0 0 0.5rem"><strong>Mnemónico:</strong> «Oso Pequeño Hace Experimentos De Ciencia»</p>
      <p style="margin:0"><strong>O</strong>bservar · <strong>P</strong>reguntar · <strong>H</strong>ipotetizar · <strong>E</strong>xperimentar · <strong>D</strong>atos · <strong>C</strong>oncluir</p>
    </div>
    <p><strong>Variable</strong> = lo que cambias a propósito. <strong>Control</strong> = lo que dejas igual para que la comparación sea justa.</p>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "En invierno en <strong>Burgos</strong> o <strong>León</strong>, el hielo del patio se derrite cuando sale el sol: misma pregunta que Lucía.",
            "En casa: ¿el chocolate se ablanda más cerca del radiador? Método científico casero.",
            "En el huerto escolar: ¿las plantas del alféizar crecen distinto a las de la sombra? (hoy practicamos el <strong>método</strong>).",
            "Un meteorólogo de CyL también observa → pregunta → mide → concluye sobre el tiempo.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Laboratorio · método científico · cubito", "l01-metodo-cientifico.html"),
        ],
        "reto_t": "Mi mini-experimento",
        "reto": (
            "Describe en 4–6 líneas un experimento <strong>sencillo</strong> que podrías hacer "
            "en casa o en el patio (agua, temperatura, plantas de alféizar, hielo…). "
            "Marca con claridad: observación, pregunta, hipótesis y qué medirías."
        ),
        "reto_id": "1eso-byg-L01",
        "cierre": (
            "<strong>Oso Pequeño Hace Experimentos De Ciencia.</strong> "
            "Observas → preguntas → hipotetizas → experimentas → tomas datos → concluyes. "
            "Una hipótesis no es un deseo: es una idea que se puede <strong>poner a prueba</strong>."
        ),
    },
    {
        "n": 2,
        "slug": "fuentes-veraces-frente-a-bulos-y-pseudociencia",
        "eyebrow": "Lección 02 · UD A · Proyecto científico",
        "title_html": "<em>Fuentes veraces</em> frente a bulos y pseudociencia",
        "title_plain": "Fuentes veraces frente a bulos y pseudociencia",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque A",
        "curiosidad_t": "Lupa sí, bola de cristal no",
        "curiosidad": (
            "Antes de la prensa moderna, almanaques y curanderos mezclaban consejos útiles con "
            "promesas milagro. La ciencia moderna exige <strong>autoría</strong>, <strong>datos</strong> "
            "y la posibilidad de <strong>comprobar</strong>. Ese filtro —no el volumen de likes— "
            "sigue siendo el mejor antídoto frente a bulos y pseudociencia."
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            "Explicar qué es una <strong>fuente veraz</strong> de información científica.",
            "Distinguir <strong>bulo</strong> (noticia falsa/rumor) de <strong>pseudociencia</strong> (disfraz de ciencia).",
            "Usar pistas simples: autor, datos, institución, posibilidad de comprobar.",
            "Aplicar el criterio a mensajes del móvil, vídeos y titulares.",
            "Valorar por qué en CyL necesitamos fuentes fiables sobre salud, clima y naturaleza.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Internet y los chats van llenos de mensajes. Algunos son ciencia de verdad; otros son <strong>bulos</strong>; otros se disfrazan de ciencia (<strong>pseudociencia</strong>).</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.5rem"><strong>Fuente veraz</strong> — autor claro, datos, institución seria (AEMET, museo, universidad).</p>
      <p style="margin:0 0 0.5rem"><strong>Bulo</strong> — afirmación falsa o rumor sin pruebas («cura milagrosa en 24 h»).</p>
      <p style="margin:0"><strong>Pseudociencia</strong> — palabras «científicas» sin método (cristales que «alinean energía»).</p>
    </div>
    <h2>Pistas rápidas</h2>
    <ol>
      <li>¿Quién lo firma? (nombre + cargo/institución)</li>
      <li>¿Hay <strong>datos</strong> o solo opiniones?</li>
      <li>¿Se puede <strong>comprobar</strong> o repetir?</li>
      <li>¿Suena a milagro demasiado fácil?</li>
    </ol>
    <div class="tarjeta">
      <p style="margin:0 0 0.5rem"><strong>Mnemónico VERAZ:</strong></p>
      <p style="margin:0"><strong>V</strong>iene de experto · <strong>E</strong>scrita con datos · <strong>R</strong>eplicable · <strong>A</strong>utor claro · <strong>Z</strong>ona/contexto citado</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Consultar el tiempo en <strong>AEMET</strong>, no en un mensaje anónimo.",
            "Leer carteles de un <strong>museo de Ciencias</strong> (Valladolid, León…) con autores y fechas.",
            "Desconfiar de remedios «milagro» vendidos en redes sin ensayos.",
            "Noticias de incendios o inundaciones: priorizar fuentes oficiales de la Junta / emergencias.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Detective · fuentes veraces · bulos", "l02-fuentes-veraces.html"),
        ],
        "reto_t": "Clasifica un mensaje real",
        "reto": (
            "Elige un mensaje real (captura o copia) de redes/chat sobre salud o naturaleza. "
            "Clasifícalo (veraz / bulo / pseudociencia) y justifica con 3 pistas <strong>VERAZ</strong>."
        ),
        "reto_id": "1eso-byg-L02",
        "cierre": (
            "<strong>VERAZ.</strong> Lupa sí, bola de cristal no. "
            "Autor + datos + se puede comprobar."
        ),
    },
    {
        "n": 3,
        "slug": "laboratorio-instrumentos-espacios-y-normas-de-seguridad",
        "eyebrow": "Lección 03 · UD A · Proyecto científico",
        "title_html": "<em>Laboratorio</em>: instrumentos, espacios y normas de seguridad",
        "title_plain": "Laboratorio: instrumentos, espacios y normas de seguridad",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque A",
        "curiosidad_t": "Bata antes que prisa",
        "curiosidad": (
            "Los primeros laboratorios escolares del siglo XIX ya insistían en orden y ropa de protección. "
            "Hoy el <strong>EPI</strong> (bata, gafas) no es teatro: evita salpicaduras, cortes y "
            "contaminación. Un laboratorio seguro es el que respeta normas antes de «hacer el experimento chulo»."
        ),
        "curiosidad_fig": "olla.svg",
        "objetivos": [
            "Nombrar instrumentos básicos del laboratorio (vaso de precipitados, tubos, balanza, mechero…).",
            "Reconocer espacios: mesa de trabajo, fregadero, armario.",
            "Distinguir normas <strong>obligatorias</strong> y <strong>prohibidas</strong>.",
            "Explicar para qué sirven bata y gafas (<strong>EPI</strong>).",
            "Actuar con prudencia: avisar en roturas o derrames.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>El <strong>laboratorio</strong> es un espacio preparado para experimentar con seguridad. No es el patio: hay material frágil, a veces calor o productos que no se tocan sin permiso.</p>
    <h2>Instrumentos habituales (1º ESO)</h2>
    <ul>
      <li><strong>Vaso de precipitados</strong> — contiene líquidos.</li>
      <li><strong>Tubos de ensayo + gradilla</strong> — pruebas pequeñas.</li>
      <li><strong>Balanza</strong> — mide la <strong>masa</strong> (gramos).</li>
      <li><strong>Mechero Bunsen</strong> — llama; solo con permiso y supervisión.</li>
      <li><strong>Termómetro</strong> — temperatura.</li>
    </ul>
    <div class="tarjeta">
      <p style="margin:0 0 0.5rem"><strong>Normas de oro:</strong> bata y gafas cuando toque; no comer ni beber; no correr; no pipetear con la boca; ordenar y lavar; avisar si algo se rompe.</p>
      <p style="margin:0"><strong>Mnemónico B-G-O-A-N:</strong> Bata · Gafas · Orden · Agua · Nunca comas</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "En el lab del IES: misma lógica que un taller — EPI y orden.",
            "En una salida de campo (río, monte): también hay normas (no beber agua sin permiso, no tocar fauna…).",
            "Cocina de casa ≠ laboratorio, pero sí: no mezclar productos de limpieza a ciegas.",
            "Avisar al adulto responsable ante roturas o derrames: hábito de seguridad.",
        ],
        "vida_fig": "olla.svg",
        "widgets": [
            ("Laboratorio seguro · instrumentos y normas", "l03-laboratorio-seguridad.html"),
        ],
        "reto_t": "Plano del lab con normas",
        "reto": (
            "Dibuja el plano del lab de tu centro (o uno ideal) y señala "
            "<strong>5 normas</strong> en carteles."
        ),
        "reto_id": "1eso-byg-L03",
        "cierre": (
            "<strong>B-G-O-A-N.</strong> Instrumentos con nombre; normas claras; "
            "avisar si hay problema."
        ),
    },
    {
        "n": 4,
        "slug": "observar-tomar-datos-modelar-y-presentar-resultados",
        "eyebrow": "Lección 04 · UD A · Proyecto científico",
        "title_html": "Observar, tomar <em>datos</em>, modelar y presentar resultados",
        "title_plain": "Observar, tomar datos, modelar y presentar resultados",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque A",
        "curiosidad_t": "El mapa no es el territorio",
        "curiosidad": (
            "Un mapa, una gráfica o una maqueta no «son» la realidad: la "
            "<strong>representan</strong> de forma útil. Desde los primeros "
            "cuadernos de campo, científicos y científicas anotan medidas con "
            "unidades y luego dibujan modelos para que otros entiendan el hallazgo."
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            "Diferenciar <strong>observación</strong>, <strong>dato</strong>, <strong>modelo</strong> y <strong>presentación</strong>.",
            "Registrar medidas en una <strong>tabla</strong>.",
            "Construir un <strong>modelo</strong> sencillo (gráfica de barras).",
            "Redactar un resultado claro para un póster o informe.",
            "Analizar si los datos muestran un cambio (crece / no crece).",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Después de preguntar e hipotetizar (L01), hay que <strong>mirar con método</strong>:</p>
    <ol>
      <li><strong>Observar</strong> con un instrumento (regla, cronómetro…).</li>
      <li><strong>Tomar datos</strong> (anotar números con unidades: cm, min, °C).</li>
      <li><strong>Modelar</strong>: simplificar la realidad en tabla, gráfica o maqueta.</li>
      <li><strong>Presentar</strong>: explicar a otros (póster, informe, exposición oral).</li>
    </ol>
    <div class="tarjeta">
      <p style="margin:0 0 0.5rem">Un <strong>modelo</strong> no es la cosa real: es un «mapa» útil. La gráfica de barras no es la hoja; <strong>representa</strong> su longitud.</p>
      <p style="margin:0"><strong>Mnemónico ODaMoPre:</strong> Observar · Datos · Modelo · Presentar</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Crecimiento de plantas del huerto escolar.",
            "Temperatura diaria anotada en el pueblo (comparar con AEMET).",
            "Contar especies en un tramo de río (salida de campo).",
            "Póster o gráfica en papel: presentar sin depender de internet.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("De la planta a la gráfica · datos y modelo", "l04-observar-datos-modelo.html"),
        ],
        "reto_t": "Tabla + barras en 4 días",
        "reto": (
            "Mide algo 4 días (temperatura, altura de brote, minutos de lluvia). "
            "Tabla + barras en papel + 3 líneas de conclusión."
        ),
        "reto_id": "1eso-byg-L04",
        "cierre": (
            "<strong>ODaMoPre.</strong> Sin datos no hay modelo serio; "
            "sin presentación, el hallazgo no viaja."
        ),
    },
    {
        "n": 5,
        "slug": "cientificas-y-cientificos-que-cambiaron-la-biologia-y-la-geologia",
        "eyebrow": "Lección 05 · UD A · Proyecto científico",
        "title_html": "<em>Científicas y científicos</em> que cambiaron la biología y la geología",
        "title_plain": "Científicas y científicos que cambiaron la biología y la geología",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque A",
        "curiosidad_t": "Ciencia colectiva, no mitos",
        "curiosidad": (
            "Mary Anning encontró fósiles que cambiaron la paleontología; Cajal dibujó neuronas "
            "con rigor de orfebre; Franklin aportó evidencia clave del ADN. La historia honesta "
            "incluye a más personas de las que caben en un meme: la ciencia avanza en equipo y se corrige."
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            "Nombrar al menos 5 figuras relevantes (con siglo y campo).",
            "Relacionar cada persona con un <strong>aporte</strong> concreto (no solo fama).",
            "Incluir científicas y al menos una figura española (Cajal).",
            "Evitar mitos inventados: distinguir hecho histórico de leyenda.",
            "Valorar que la ciencia es colectiva y se corrige con el tiempo.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Las ciencias biológicas y geológicas avanzaron porque personas observaron, midieron, discutieron y publicaron pruebas.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.35rem"><strong>Mary Anning</strong> — paleontología · fósiles de reptiles marinos</p>
      <p style="margin:0 0 0.35rem"><strong>Charles Lyell</strong> — geología · procesos lentos explican el pasado</p>
      <p style="margin:0 0 0.35rem"><strong>Charles Darwin</strong> — biología · selección natural</p>
      <p style="margin:0 0 0.35rem"><strong>Gregor Mendel</strong> — biología · herencia (guisantes)</p>
      <p style="margin:0 0 0.35rem"><strong>Santiago Ramón y Cajal</strong> — neurociencia · neuronas (Nobel 1906)</p>
      <p style="margin:0 0 0.35rem"><strong>Rosalind Franklin</strong> — biofísica · evidencia estructural del ADN</p>
      <p style="margin:0"><strong>Barbara McClintock</strong> — genética · elementos genéticos móviles</p>
    </div>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «CaMe DaLy Ma» → Cajal · Mendel · Darwin · Lyell · Mary Anning (+ Franklin / McClintock)</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Buscar en biblioteca/museo fichas reales (no solo vídeos virales).",
            "Cajal es referencia en institutos españoles: células nerviosas.",
            "Geología de CyL (páramos, Cordillera) se entiende mejor con la idea de tiempo largo (Lyell).",
            "Contrastar biografías con fuentes veraces (enlace con L02).",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Línea del tiempo · científicas y científicos", "l05-cientificas-cientificos.html"),
        ],
        "reto_t": "Mini-póster de una figura",
        "reto": (
            "Elige una figura y prepara un mini-póster A5: fechas, aporte, "
            "una evidencia, una fuente bibliográfica real."
        ),
        "reto_id": "1eso-byg-L05",
        "cierre": (
            "Personas + pruebas + tiempo. <strong>Cajal</strong> en España; "
            "<strong>Anning, Franklin, McClintock</strong> en el relato completo."
        ),
    },
    {
        "n": 6,
        "slug": "rocas-y-minerales-que-son-y-en-que-se-diferencian",
        "eyebrow": "Lección 06 · UD B · Geosfera",
        "title_html": "<em>Rocas y minerales</em>: qué son y en qué se diferencian",
        "title_plain": "Rocas y minerales: qué son y en qué se diferencian",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque B",
        "curiosidad_t": "Ladrillo y muro",
        "curiosidad": (
            "Desde la Antigüedad se usaron piedras sin distinguir bien mineral y roca. "
            "La geología moderna aclara: el <strong>mineral</strong> es el «ladrillo» "
            "(composición definida); la <strong>roca</strong> es el «muro» (agregado de minerales). "
            "Esa metáfora ordena lo que ves en el patio o en una cantera."
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            "Definir <strong>mineral</strong> y <strong>roca</strong> en español claro.",
            "Explicar la metáfora <strong>ladrillo / muro</strong>.",
            "Clasificar ejemplos sencillos (granito, cuarzo, arenisca, calcita…).",
            "Reconocer que una roca puede contener varios minerales.",
            "Situar ambos en la <strong>geosfera</strong>.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>La <strong>geosfera</strong> es la parte sólida de la Tierra. Está hecha de materiales naturales:</p>
    <ul>
      <li><strong>Mineral:</strong> sólido natural con composición química definida (y, a menudo, estructura cristalina). Ej.: <strong>cuarzo</strong>, <strong>calcita</strong>, <strong>mica</strong>.</li>
      <li><strong>Roca:</strong> agregado natural de uno o varios minerales. Ej.: <strong>granito</strong> (cuarzo + feldespato + mica), <strong>arenisca</strong>, <strong>basalto</strong>.</li>
    </ul>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Mineral = ladrillo; Roca = muro».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Encimeras o bordillos de <strong>granito</strong> (roca).",
            "Arena de río: muchos granos son minerales (p. ej. cuarzo).",
            "Caliza de páramos: roca; su mineral principal suele ser calcita.",
            "Una piedra del patio con granos distintos: pista de roca policomponente.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Comparador · roca ↔ mineral", "l06-rocas-minerales.html"),
        ],
        "reto_t": "Dos muestras: roca y mineral",
        "reto": (
            "Trae (o dibuja) 2 muestras: una «tipo roca» y una «tipo mineral» y justifica."
        ),
        "reto_id": "1eso-byg-L06",
        "cierre": (
            "<strong>Ladrillo / muro.</strong> Sin minerales no hay rocas; "
            "una roca cuenta una historia de minerales juntos."
        ),
    },
    {
        "n": 7,
        "slug": "clasificar-rocas-sedimentarias-metamorficas-e-igneas",
        "eyebrow": "Lección 07 · UD B · Geosfera",
        "title_html": "Clasificar rocas: <em>sedimentarias, metamórficas e ígneas</em>",
        "title_plain": "Clasificar rocas: sedimentarias, metamórficas e ígneas",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque B",
        "curiosidad_t": "Tres familias, un origen",
        "curiosidad": (
            "Clasificar por color engaña: una roca negra puede ser basalto (ígnea) o una pizarra oscura "
            "(metamórfica). La llave es el <strong>origen</strong>: magma/lava, sedimentos, o cambio "
            "por presión y temperatura. Esa idea ordena el laboratorio de rocas desde el siglo XIX."
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            "Nombrar las <strong>tres familias</strong> de rocas.",
            "Relacionar cada familia con su <strong>origen</strong>.",
            "Clasificar ejemplos: granito, basalto, arenisca, caliza, pizarra, mármol.",
            "Usar pistas visuales (capas, láminas, aspecto volcánico).",
            "Evitar memorizar listas sin el «porqué».",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <div class="tarjeta">
      <p style="margin:0 0 0.35rem"><strong>Ígneas</strong> — magma o lava que se enfría · granito, basalto</p>
      <p style="margin:0 0 0.35rem"><strong>Sedimentarias</strong> — sedimentos acumulados y compactados · arenisca, caliza</p>
      <p style="margin:0"><strong>Metamórficas</strong> — roca previa cambiada por presión/temperatura · pizarra, mármol</p>
    </div>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico ISI-SE-ME:</strong> Ígneas · Sedimentarias · Metamórficas</p>
    </div>
    <p>Si ves <strong>estratos</strong>, piensa sedimentaria; si ves <strong>láminas</strong> tipo pizarra, metamórfica; si viene de <strong>enfriar fundido</strong>, ígnea.</p>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "<strong>Pizarra</strong> en cubiertas (León y zonas próximas históricas).",
            "<strong>Calizas</strong> y páramos sedimentarios.",
            "<strong>Granitos</strong> del Sistema Central / Gredos (ígneas plutónicas).",
            "Mármol = metamorfismo de calizas (pista de familia).",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Clasificar rocas · tres familias", "l07-clasificar-rocas.html"),
        ],
        "reto_t": "Tabla de 6 rocas",
        "reto": (
            "Haz una tabla de 6 rocas del entorno o del lab con familia + pista visual."
        ),
        "reto_id": "1eso-byg-L07",
        "cierre": (
            "<strong>ISI-SE-ME.</strong> Origen = llave de la clasificación."
        ),
    },
    {
        "n": 8,
        "slug": "el-ciclo-de-las-rocas",
        "eyebrow": "Lección 08 · UD B · Geosfera",
        "title_html": "El <em>ciclo de las rocas</em>",
        "title_plain": "El ciclo de las rocas",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque B",
        "curiosidad_t": "Despacio, pero sin parar",
        "curiosidad": (
            "Hutton y Lyell ayudaron a ver que la Tierra cambia a escala de millones de años. "
            "El <strong>ciclo de las rocas</strong> no es un microondas: enfriamiento, erosión, "
            "sedimentación, metamorfismo y fusión tejen rutas lentas —y hay más de un camino posible."
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            "Explicar qué es el <strong>ciclo de las rocas</strong>.",
            "Relacionar procesos: enfriamiento, erosión, sedimentación, metamorfismo, fusión.",
            "Seguir al menos un recorrido completo en el diagrama.",
            "Entender que los cambios son <strong>lentos</strong> a escala humana.",
            "Conectar con la clasificación de L07.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Las rocas no están «fijas para siempre». Procesos geológicos las transforman:</p>
    <ul>
      <li>Magma <strong>enfría</strong> → ígnea</li>
      <li>Ígnea (u otras) se <strong>rompe/erosiona</strong> → sedimentos → <strong>sedimentaria</strong></li>
      <li>Con <strong>presión y temperatura</strong> → <strong>metamórfica</strong></li>
      <li>Si <strong>funde</strong> → magma otra vez</li>
    </ul>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Enfría · Rompe · Enterra · Aprieta · Funde»</p>
    </div>
    <p>No hay un único círculo obligatorio: hay <strong>muchas rutas</strong>. L07 clasifica; L08 muestra cómo pasan de una a otra.</p>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Cantos de río = erosión en marcha.",
            "Estratos de páramo = sedimentación antigua.",
            "El tiempo geológico explica paisajes de la comunidad.",
            "Inventar un «viaje» de 4 pasos con una roca local ayuda a fijar el ciclo.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Ciclo de las rocas · rutas y procesos", "l08-ciclo-rocas.html"),
        ],
        "reto_t": "Viaje de 4 pasos",
        "reto": (
            "Elige una roca de CyL e inventa (con lógica) un «viaje» de 4 pasos por el ciclo."
        ),
        "reto_id": "1eso-byg-L08",
        "cierre": (
            "<strong>Enfría · Rompe · Enterra · Aprieta · Funde.</strong> "
            "Despacio, pero sin parar."
        ),
    },
    {
        "n": 9,
        "slug": "rocas-y-minerales-relevantes-con-foco-en-castilla-y-leon",
        "eyebrow": "Lección 09 · UD B · Geosfera",
        "title_html": "Rocas y minerales relevantes <em>(foco Castilla y León)</em>",
        "title_plain": "Rocas y minerales relevantes (con foco en Castilla y León)",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque B",
        "curiosidad_t": "Leer el territorio en piedra",
        "curiosidad": (
            "Páramos de caliza, berrocales de granito, cubiertas de pizarra: Castilla y León "
            "se lee también en sus materiales. Sin inventar minas ni cifras: lo honesto es "
            "decir «tradicional / frecuente» y contrastar con mapa o museo."
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            "Citar al menos 4 ejemplos relevantes (mundo + CyL).",
            "Asociar <strong>granito, caliza, pizarra, cuarzo, yeso</strong> a una zona o uso típico en CyL.",
            "Distinguir dato geológico de mito local inventado.",
            "Relacionar con familias de L07.",
            "Valorar el patrimonio geológico cercano.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>En Castilla y León (orientativo y honesto):</strong></p>
    <div class="tarjeta">
      <p style="margin:0 0 0.35rem"><strong>Granito</strong> (ígnea) — Sistema Central / Gredos (p. ej. Ávila)</p>
      <p style="margin:0 0 0.35rem"><strong>Caliza</strong> (sedimentaria) — páramos y cuestas de la Meseta</p>
      <p style="margin:0 0 0.35rem"><strong>Pizarra</strong> (metamórfica) — tradición en comarcas leonesas (cubiertas)</p>
      <p style="margin:0 0 0.35rem"><strong>Cuarzo</strong> (mineral) — abundante en granitos y arenas</p>
      <p style="margin:0"><strong>Yeso</strong> (mineral / evaporita) — cuencas sedimentarias</p>
    </div>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico Gra-Ca-Pi-Cuar-Ye:</strong> Granito · Caliza · Pizarra · Cuarzo · Yeso</p>
    </div>
    <p>No inventamos minas «famosas» ni fechas falsas: si no hay dato seguro, se dice «tradicional / frecuente» y se contrastará en L10 con fuentes.</p>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Pueblo en páramo: muros/calizas.",
            "Zona de Gredos: berrocales graníticos.",
            "Cubiertas de pizarra en arquitectura tradicional.",
            "Contrastar con atlas / museo / mapa geológico (IGME).",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Rocas y minerales CyL · mapa honesto", "l09-rocas-minerales-cyl.html"),
        ],
        "reto_t": "1 roca de tu provincia",
        "reto": (
            "Elige tu provincia y busca (web del centro / atlas) 1 roca típica. Cita la fuente."
        ),
        "reto_id": "1eso-byg-L09",
        "cierre": (
            "<strong>Gra-Ca-Pi-Cuar-Ye.</strong> CyL se lee también en sus rocas."
        ),
    },
    {
        "n": 10,
        "slug": "extraccion-minera-aplicaciones-economia-y-sociedad-en-cyl",
        "eyebrow": "Lección 10 · UD B · Geosfera",
        "title_html": "<em>Extracción minera</em>: aplicaciones, economía y sociedad en CyL",
        "title_plain": "Extracción minera: aplicaciones, economía y sociedad en CyL",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque B",
        "curiosidad_t": "Usar y restaurar",
        "curiosidad": (
            "Extraer materiales del terreno alimenta obras y oficios, pero también deja huella. "
            "En CyL el carbón de León–Palencia marcó generaciones; hoy pesan más áridos, "
            "pizarra y la idea de <strong>restaurar</strong> espacios. Sin cifras inventadas: "
            "beneficio + reto + fuente."
        ),
        "curiosidad_fig": "olla.svg",
        "objetivos": [
            "Describir métodos básicos: <strong>cielo abierto</strong> y <strong>subterráneo</strong>.",
            "Relacionar extracción con <strong>aplicaciones</strong> (construcción, industria, energía histórica).",
            "Explicar beneficios (empleo, materiales) y retos (paisaje, seguridad, emisiones).",
            "Situar a CyL: tradición (carbón León-Palencia en declive; pizarra; áridos) sin cifras inventadas.",
            "Hablar de <strong>perspectivas</strong>: restauración, diversificación, transición energética.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Extraer</strong> = sacar minerales/rocas del terreno con técnica y normas.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.35rem"><strong>Métodos</strong> — cielo abierto (canteras) / galerías subterráneas</p>
      <p style="margin:0 0 0.35rem"><strong>Aplicaciones</strong> — áridos, piedra ornamental, pizarra, caliza, metales…</p>
      <p style="margin:0 0 0.35rem"><strong>Economía</strong> — empleo e industria local (variable según recurso y época)</p>
      <p style="margin:0 0 0.35rem"><strong>Sociedad</strong> — oficios, despoblación/reactivación, salud laboral</p>
      <p style="margin:0"><strong>Futuro</strong> — menos carbón; más restauración y otras actividades</p>
    </div>
    <div class="tarjeta">
      <p style="margin:0 0 0.5rem"><strong>Honestidad:</strong> el carbón fue central en cuencas de León y Palencia; hoy se reduce su uso energético. No afirmamos cifras exactas sin fuente del año en curso.</p>
      <p style="margin:0"><strong>Mnemónico USA-RESTAURA:</strong> Usar · Seguridad · Aplicaciones · Restaurar</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Canteras de áridos cerca de obras.",
            "Memoria minera en cuencas (museos / patrimonio industrial).",
            "Debate local: empleo vs impacto ambiental.",
            "L09 nombra materiales; L10 explica cómo salen del terreno.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Extracción minera CyL · usos y sociedad", "l10-extraccion-minera-cyl.html"),
        ],
        "reto_t": "Beneficio + reto + fuente",
        "reto": (
            "Entrevista (o busca noticia con fuente) sobre una cantera/mina/patrimonio minero de CyL. "
            "Resume beneficio + reto + fuente."
        ),
        "reto_id": "1eso-byg-L10",
        "cierre": (
            "<strong>USA-RESTAURA.</strong> Recursos del territorio, "
            "con seguridad y mirada de futuro."
        ),
    },
]


def lesson_filename(n: int) -> str:
    lesson = next(item for item in LESSONS if item["n"] == n)
    return f"leccion-{n:02d}-{lesson['slug']}.html"


def manifest_text(*, offline: bool = False) -> str:
    # Online hub lives in course dir; offline pack uses flat icons/
    icons_prefix = "icons/" if offline else "icons/"
    return json.dumps({
        "name": "1º ESO Biología y Geología · Les vencimos",
        "short_name": "1º ESO ByG",
        "start_url": "./index.html" if offline else "./1eso-biologia-geologia.html",
        "scope": "./",
        "display": "standalone",
        "theme_color": "#FAF7F0",
        "background_color": "#FAF7F0",
        "accent_color": "#C4A15A",
        "icons": [
            {"src": f"{icons_prefix}favicon.svg", "sizes": "any", "type": "image/svg+xml"},
            {"src": f"{icons_prefix}favicon-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": f"{icons_prefix}apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
            {"src": f"{icons_prefix}app-icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, ensure_ascii=False, indent=2) + "\n"


def ensure_course_branding() -> None:
    COURSE_ICONS.mkdir(parents=True, exist_ok=True)
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "app-icon-512.png"):
        shutil.copy2(BRAND_ICONS / name, COURSE_ICONS / name)
    (COURSE_DIR / "manifest.webmanifest").write_text(
        manifest_text(offline=False), encoding="utf-8"
    )


def progress_pct(n: int) -> str:
    return f"{(n / TOTAL) * 100:.2f}".rstrip("0").rstrip(".")


def nav_html(n: int, *, offline: bool) -> str:
    calc = "calculadora.html" if offline else "../../../modulos/calculadora.html"
    hub = "index.html" if offline else "../1eso-biologia-geologia.html"
    if n <= 1:
        prev = (
            '<span class="atajo atajo-prev is-disabled" aria-disabled="true" '
            'title="Primera lección">← Anterior</span>'
        )
    else:
        prev = (
            f'<a class="atajo atajo-prev" href="{lesson_filename(n - 1)}" '
            f'title="Lección {n-1:02d}">← Anterior</a>'
        )
    if n >= TOTAL:
        nxt = f'<a class="atajo atajo-next" href="{hub}" title="Volver al índice">Fin del curso</a>'
    elif n >= AVAILABLE:
        nxt = (
            f'<a class="atajo atajo-next" href="{hub}" '
            f'title="Más lecciones próximamente">Índice · próximamente →</a>'
        )
    else:
        nxt = (
            f'<a class="atajo atajo-next" href="{lesson_filename(n + 1)}" '
            f'title="Lección {n+1:02d}">Siguiente →</a>'
        )
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
        onload = (
            "try{var d=this.contentDocument||this.contentWindow.document;"
            "if(d){var h=Math.max("
            "(d.documentElement&&d.documentElement.scrollHeight)||0,"
            "(d.body&&d.body.scrollHeight)||0,560);"
            "this.style.height=h+'px';this.parentElement.style.minHeight=h+'px';}}"
            "catch(e){}}"
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
    marca_meta = "1º ESO Biología y Geología · offline" if offline else "1º ESO Biología y Geología"
    icon_root = "icons" if offline else "../icons"
    # Online icons live under course; brand path also works — prefer course icons
    if not offline:
        icon_root = "../icons"
    manifest_href = "manifest.webmanifest" if offline else "../manifest.webmanifest"
    body_class = "leccion-shell offline-embed" if offline else "leccion-shell"

    objs = "".join(f"      <li>{o}</li>\n" for o in lesson["objetivos"])
    vida_lis = "".join(f"        <li>{v}</li>\n" for v in lesson["vida"])

    w_parts = []
    for lab, fn in lesson["widgets"]:
        wh = None
        if offline:
            wh = load_widget_html(fn)
            assert_widget_offline_safe(fn, wh)
        w_parts.append(widget_block(lab, fn, offline=offline, widget_html=wh))
    w_html = "\n".join(w_parts)

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
      <li>Usar los pasos del método (aunque sea en corto).</li>
      <li>Medir algo concreto (tiempo, temperatura, altura…).</li>
      <li>Conectar con tu entorno (CyL, casa, cole).</li>
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


HUB_STYLES = """
  .hub-hero {
    margin: 0 0 1.75rem;
    padding: 1.5rem 1.35rem 1.6rem;
    background:
      linear-gradient(135deg, rgba(196, 161, 90, 0.12), transparent 55%),
      var(--lv-panel);
    border: 1px solid var(--lv-linea);
    border-left: 3px solid var(--lv-acento);
    border-radius: var(--lv-radio-card);
    box-shadow: var(--lv-sombra);
  }
  .hub-hero h1 {
    margin: 0 0 0.55rem;
    font-family: var(--lv-serif);
    font-size: clamp(1.55rem, 4vw, 2.1rem);
    font-weight: 600;
    color: var(--lv-titulo);
    line-height: 1.2;
  }
  .hub-hero .hub-status {
    margin: 0 0 1.1rem;
    color: var(--lv-suave);
    font-size: 1rem;
    max-width: 40rem;
  }
  .hub-cta {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1.15rem;
    font-size: 1.02rem;
    font-weight: 650;
    text-decoration: none;
    color: var(--lv-acento-texto);
    background: var(--lv-acento);
    border: 1px solid #b08d45;
    border-radius: var(--lv-radio);
    box-shadow: var(--lv-sombra);
  }
  .hub-cta:hover {
    color: var(--lv-acento-texto);
    filter: brightness(1.05);
  }
  .hub-nota {
    margin: 1.25rem 0 0.5rem;
    font-size: 0.92rem;
    color: var(--lv-suave);
  }
  .hub-lista {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    gap: 0.45rem;
  }
  .hub-item {
    display: grid;
    grid-template-columns: 2.5rem 1fr auto;
    gap: 0.65rem 0.85rem;
    align-items: baseline;
    padding: 0.65rem 0.85rem;
    background: var(--lv-panel);
    border: 1px solid var(--lv-linea);
    border-radius: var(--lv-radio);
  }
  .hub-item a {
    display: contents;
    text-decoration: none;
    color: inherit;
  }
  .hub-item.hub-disponible {
    border-color: rgba(196, 161, 90, 0.45);
    background: var(--lv-panel-soft);
  }
  .hub-item.hub-disponible:hover {
    border-color: var(--lv-acento);
  }
  .hub-item.hub-pronto {
    opacity: 0.78;
  }
  .hub-num {
    font-weight: 700;
    color: var(--lv-acento);
    font-variant-numeric: tabular-nums;
  }
  .hub-titulo {
    color: var(--lv-tinta);
    font-size: 0.95rem;
  }
  .hub-estado {
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--lv-suave);
    white-space: nowrap;
  }
  .hub-disponible .hub-estado {
    color: var(--lv-verde);
  }
  .hub-pie-nota {
    margin-top: 1.5rem;
    padding: 0.9rem 1rem;
    font-size: 0.88rem;
    color: var(--lv-suave);
    background: var(--lv-fondo-2);
    border: 1px dashed var(--lv-linea);
    border-radius: var(--lv-radio);
  }
"""


def render_hub(*, for_downloads: bool = False) -> str:
    """Online hub (or downloads/ mirror with adjusted relative paths)."""
    if for_downloads:
        css = "../profesor/_plantilla-leccion/leccion-shell.css"
        home = "../index.html"
        descargas = "../descargas.html"
        brand = "../brand/favicon/"
        manifest = "../profesor/1eso-biologia-geologia/manifest.webmanifest"
        lec_prefix = "../profesor/1eso-biologia-geologia/lecciones/"
    else:
        css = "../_plantilla-leccion/leccion-shell.css"
        home = "../../index.html"
        descargas = "../../descargas.html"
        brand = "../../brand/favicon/"
        manifest = "manifest.webmanifest"
        lec_prefix = "lecciones/"

    items = []
    for i, title in enumerate(TEMARIO, start=1):
        if i <= AVAILABLE:
            fn = lesson_filename(i)
            items.append(
                f'''      <li class="hub-item hub-disponible">
        <a href="{lec_prefix}{fn}">
          <span class="hub-num">{i:02d}</span>
          <span class="hub-titulo">{html.escape(title)}</span>
          <span class="hub-estado">Disponible</span>
        </a>
      </li>'''
            )
        else:
            items.append(
                f'''      <li class="hub-item hub-pronto">
        <span class="hub-num">{i:02d}</span>
        <span class="hub-titulo">{html.escape(title)}</span>
        <span class="hub-estado">Próximamente</span>
      </li>'''
            )

    l01 = lesson_filename(1)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>1º ESO Biología y Geología · Les vencimos</title>
<meta name="theme-color" content="#FAF7F0"/>
<link rel="icon" href="{brand}favicon.svg" type="image/svg+xml"/>
<link rel="icon" href="{brand}favicon-32.png" sizes="32x32" type="image/png"/>
<link rel="apple-touch-icon" href="{brand}apple-touch-icon.png"/>
<link rel="manifest" href="{manifest}"/>
<link rel="stylesheet" href="{css}"/>
<style>
{HUB_STYLES}
</style>
</head>
<body class="leccion-shell">
<div class="leccion-wrap">

  <header class="leccion-top">
    <a class="leccion-marca" href="{home}">Les <span>vencimos</span></a>
    <p class="leccion-meta-top">Curso · shell</p>
  </header>

  <section class="hub-hero" aria-labelledby="hub-titulo">
    <p class="eyebrow" style="display:block;font-size:0.72rem;letter-spacing:0.16em;text-transform:uppercase;color:var(--lv-acento);font-weight:600;margin:0 0 0.55rem">Decreto 39/2022 · Castilla y León</p>
    <h1 id="hub-titulo">1º ESO Biología y Geología</h1>
    <p class="hub-status">
      <strong>Lecciones 01–{AVAILABLE:02d} disponibles</strong> (UD A proyecto científico + UD B geosfera) en shell HTML.
      El curso está <strong>en construcción</strong> ({TOTAL} lecciones previstas).
      <strong>ZIP offline</strong> (sin instalar: descomprime y abre <code>ABRE-AQUI.html</code>) en <a href="{descargas}">Descargas</a>.
    </p>
    <a class="hub-cta" href="{lec_prefix}{l01}">Abrir lección 01 →</a>
  </section>

  <p class="hub-nota">Índice del temario ({TOTAL} lecciones previstas). Disponibles L01–L{AVAILABLE:02d} como <code>leccion-NN-….html</code> (alias <code>leccion-NN.html</code>). L{AVAILABLE+1:02d}–L{TOTAL}: próximamente.</p>

  <ol class="hub-lista">
{chr(10).join(items)}
  </ol>

  <p class="hub-pie-nota">
    Educación obligatoria · currículo oficial CyL (Decreto 39/2022). Distinto del pack Profesor (multi-materia).
    Interactivos L01–L{AVAILABLE:02d}: método, fuentes, laboratorio, datos, científicas/os, rocas y minería CyL.
  </p>

  <footer class="leccion-pie">
    <strong>Les vencimos</strong> · 1º ESO Biología y Geología · L01–L{AVAILABLE:02d} de {TOTAL} · en construcción
  </footer>
</div>
</body>
</html>
"""


def write_hub() -> None:
    HUB.write_text(render_hub(for_downloads=False), encoding="utf-8")
    (REPO / "downloads/1eso-biologia-geologia.html").write_text(
        render_hub(for_downloads=True), encoding="utf-8"
    )
    print("Wrote hub (+ downloads mirror)")


def update_descargas() -> None:
    text = DESCARGAS.read_text(encoding="utf-8")
    import re

    # Lead line (Mate + ByG)
    text = re.sub(
        r"1º ESO Matemáticas y Biología y Geología \(L0?\d+(?:–L?\d+)?\)",
        f"1º ESO Matemáticas y Biología y Geología (L01–L{AVAILABLE:02d})",
        text,
        count=1,
    )
    text = text.replace(
        "Empieza por 1º ESO Matemáticas. <strong>No es el pack Profesor</strong>",
        f"1º ESO Matemáticas y Biología y Geología (L01–L{AVAILABLE:02d}). <strong>No es el pack Profesor</strong>",
    )

    byg_body = (
        f"<strong>No se instala.</strong> Descomprime y abre <code>ABRE-AQUI.html</code> / <code>index.html</code>.\n"
        f"            L01–L{AVAILABLE:02d} disponibles (UD A + UD B geosfera); "
        f"curso en construcción ({TOTAL} lecciones previstas). Sin nube ni servidor.\n"
        f"            Distinto del pack Profesor."
    )

    if "1eso-biologia-geologia-offline.zip" in text:
        text2, n = re.subn(
            r"(<h2>1º ESO Biología y Geología</h2>\s*"
            r'<p class="kicker">Oficial CyL · Decreto 39/2022 · en construcción \(40 lecciones\)</p>\s*'
            r"<p>)(.*?)(</p>\s*"
            r'<div class="actions">\s*'
            r'<a class="btn-download" href="/downloads/1eso-biologia-geologia-offline\.zip")',
            rf"\1{byg_body}\3",
            text,
            count=1,
            flags=re.S,
        )
        if n:
            text = text2
            DESCARGAS.write_text(text, encoding="utf-8")
            print("Updated descargas.html ByG L01–L%02d copy" % AVAILABLE)
            return
        # fallback: softer replaces
        text = re.sub(
            r"L01 disponible \(método científico\); curso en construcción \(40 lecciones previstas\)",
            f"L01–L{AVAILABLE:02d} disponibles (UD A + UD B geosfera); curso en construcción ({TOTAL} lecciones previstas)",
            text,
            count=1,
        )
        text = re.sub(
            r"1º ESO Matemáticas y Biología y Geología \(L01\)",
            f"1º ESO Matemáticas y Biología y Geología (L01–L{AVAILABLE:02d})",
            text,
            count=1,
        )
        DESCARGAS.write_text(text, encoding="utf-8")
        print("Updated descargas.html ByG copy (fallback)")
        return

    byg_article = f"""        <article class="item">
          <div class="num">08b</div>
          <div>
            <h2>1º ESO Biología y Geología</h2>
            <p class="kicker">Oficial CyL · Decreto 39/2022 · en construcción (40 lecciones)</p>
            <p>{byg_body.replace(chr(92)+'n', chr(10))}</p>
            <div class="actions">
              <a class="btn-download" href="/downloads/1eso-biologia-geologia-offline.zip" download="1eso-biologia-geologia-offline.zip">Descargar ZIP</a>
              <a class="textlink" href="/profesor/1eso-biologia-geologia/lecciones/{lesson_filename(1)}">Abrir lección 01</a>
              <a class="textlink" href="/profesor/1eso-biologia-geologia/1eso-biologia-geologia.html">Índice del curso</a>
            </div>
          </div>
        </article>
"""

    needle = """              <a class="textlink" href="/profesor/1eso-matematicas/1eso-matematicas.html">Índice del curso</a>
            </div>
          </div>
        </article>
      </div>

      <div class="section-modulos">
        <h2>Aprender para el cole</h2>"""
    if needle not in text:
        raise SystemExit("descargas.html Mate block not found for ByG insert")
    replacement = f"""              <a class="textlink" href="/profesor/1eso-matematicas/1eso-matematicas.html">Índice del curso</a>
            </div>
          </div>
        </article>
{byg_article}      </div>

      <div class="section-modulos">
        <h2>Aprender para el cole</h2>"""
    text = text.replace(needle, replacement, 1)
    DESCARGAS.write_text(text, encoding="utf-8")
    print("Updated descargas.html")


def update_index() -> None:
    import re
    text = INDEX.read_text(encoding="utf-8")
    target = (
        f"1º ESO Matemáticas + Biología y Geología L01–L{AVAILABLE:02d} (oficial CyL). "
        "Descarga ZIP offline en Descargas."
    )
    if target in text:
        print("index already updated")
        return
    patterns = [
        r"1º ESO Matemáticas \+ Biología y Geología L0?\d+(?:–L?\d+)? \(oficial CyL\)\. Descarga ZIP offline en Descargas\.?",
        r"1º ESO Matemáticas \+ Biología y Geología L01 \(oficial CyL\)\. Descarga ZIP offline en Descargas\.?",
        r"1º ESO Matemáticas \(oficial CyL\)\. L01 lista — descarga ZIP offline en Descargas\.?",
    ]
    for pat in patterns:
        text2, n = re.subn(pat, target, text, count=1)
        if n:
            INDEX.write_text(text2, encoding="utf-8")
            print("Updated index.html")
            return
    if "Biología y Geología" in text and "Educación obligatoria" in text:
        text2, n = re.subn(
            r"(Biología y Geología )L0?\d+(?:–L?\d+)?",
            rf"\1L01–L{AVAILABLE:02d}",
            text,
            count=1,
        )
        if n:
            INDEX.write_text(text2, encoding="utf-8")
            print("Updated index.html ByG range")
            return
        print("index already mentions ByG (no Lxx pattern)")
        return
    raise SystemExit("index.html Educación obligatoria card text not found")


def build_offline_pack() -> None:
    if PACK_DIR.exists():
        shutil.rmtree(PACK_DIR)
    root = PACK_DIR / "1eso-biologia-geologia-offline"
    root.mkdir(parents=True)

    (root / "LEEME.md").write_text(
        f"""# 1º ESO Biología y Geología — pack offline

No hay que instalar nada. Descomprime y abre **ABRE-AQUI.html** (o index.html).

**Qué es:** lecciones de **Educación obligatoria** (currículo oficial Castilla y León, Decreto 39/2022).
Este pack trae las lecciones **01–{AVAILABLE:02d}** (UD A + UD B geosfera) en HTML plano (shell + interactivos embebidos).
Curso en construcción: **{TOTAL}** lecciones previstas (no está completo).

**Cómo abrir (Android / PC) — 4 pasos**

1. Descarga el ZIP.
2. Abre **Archivos / Mis archivos** (NO la lista Descargas del navegador).
3. Descomprime y entra en la carpeta `1eso-biologia-geologia-offline`.
4. Toca **`ABRE-AQUI.html`** o **`index.html`** → Chrome / Samsung Internet.

Todo funciona **offline**, sin nube ni servidor (`file://`). Sin instalación, sin app store, sin «setup».

**Importante en Android:** abre siempre desde la **carpeta descomprimida** (`file://`).
**Nunca** abras el HTML desde la lista Descargas del navegador (`content://`): ahí fallan
imágenes, CSS e interactivos/animaciones.
En Chrome/Android: menú → **Añadir a pantalla de inicio**.

Los interactivos van **embebidos** en cada lección (funcionan sin cargar iframes hermanos).
Si hace falta, cada lección sigue teniendo el enlace «Abrir en pestaña →» al widget suelto.

**Contenido:** `ABRE-AQUI.html`, `index.html`, `LEEME.md`, `leccion-01`…`leccion-{AVAILABLE:02d}-….html`,
alias `leccion-NN.html`, widgets `l01`…`l{AVAILABLE:02d}-….html`, calculadora, CSS/JS,
`figuras/*.svg` e iconos — todo en la misma carpeta.
""",
        encoding="utf-8",
    )

    items = []
    for n in range(1, AVAILABLE + 1):
        items.append(
            f'    <li class="ok"><a href="{lesson_filename(n)}"><strong>L{n:02d}</strong> — {html.escape(TEMARIO[n-1])}</a></li>'
        )
    if AVAILABLE < TOTAL:
        for n in range(AVAILABLE + 1, min(AVAILABLE + 6, TOTAL + 1)):
            items.append(
                f'    <li class="soon"><span><strong>L{n:02d}</strong> — {html.escape(TEMARIO[n-1])} · próximamente</span></li>'
            )
        items.append(f'    <li class="soon"><span>… hasta L{TOTAL} — próximamente</span></li>')

    hub_flat = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#FAF7F0"/>
<title>1º ESO Biología y Geología · offline · Les vencimos</title>
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
    <h1 class="titulo-leccion">1º ESO Biología y Geología</h1>
    <p class="meta-leccion">L01–L{AVAILABLE:02d} listas · curso en construcción ({TOTAL} lecciones previstas)</p>
  </header>
  <div class="no-install">
    <strong>No hay que instalar nada.</strong> Abre <code>ABRE-AQUI.html</code> o <code>index.html</code> desde esta carpeta
    (Archivos / Mis archivos → carpeta descomprimida → <code>file://</code>).
    El interactivo va embebido en la lección.
    En Chrome/Android: menú → <strong>Añadir a pantalla de inicio</strong>.
    <strong>Nunca</strong> abras desde la lista Descargas del navegador (<code>content://</code>).
  </div>
  <p><a class="big-cta" href="{lesson_filename(1)}">Abrir lección 01 →</a>
     &nbsp; <a href="calculadora.html">Calculadora</a></p>
  <p class="hub-nota">L{AVAILABLE+1:02d}–L{TOTAL} próximamente. Usa siempre este índice.</p>
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
"""
    (root / "index.html").write_text(hub_flat, encoding="utf-8")
    (root / "ABRE-AQUI.html").write_text(hub_flat, encoding="utf-8")

    shutil.copy2(PLANTILLA / "leccion-shell.css", root / "leccion-shell.css")
    shutil.copy2(PLANTILLA / "leccion-shell-nav.js", root / "leccion-shell-nav.js")
    shutil.copy2(REPO / "modulos/calculadora.html", root / "calculadora.html")
    icons_dst = root / "icons"
    icons_dst.mkdir()
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "app-icon-512.png"):
        shutil.copy2(BRAND_ICONS / name, icons_dst / name)
    (root / "manifest.webmanifest").write_text(manifest_text(offline=True), encoding="utf-8")

    fig_dst = root / "figuras"
    fig_dst.mkdir()
    for svg in (PLANTILLA / "figuras").glob("*.svg"):
        shutil.copy2(svg, fig_dst / svg.name)

    for L in LESSONS:
        (root / lesson_filename(L["n"])).write_text(
            render_lesson(L, offline=True), encoding="utf-8"
        )
        write_redirect(
            root / f"leccion-{L['n']:02d}.html",
            lesson_filename(L["n"]),
            f"Lección {L['n']:02d}",
        )
        for _, wf in L["widgets"]:
            src = LEC / wf
            if not src.exists():
                raise SystemExit(f"missing widget {wf}")
            wh = src.read_text(encoding="utf-8")
            assert_widget_offline_safe(wf, wh)
            shutil.copy2(src, root / wf)

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                arc = path.relative_to(PACK_DIR).as_posix()
                zf.write(path, arc)
    size = ZIP_PATH.stat().st_size
    print(f"Wrote {ZIP_PATH} ({size} bytes)")
    shutil.rmtree(PACK_DIR)


def main() -> None:
    ensure_course_branding()
    for L in LESSONS:
        out = LEC / lesson_filename(L["n"])
        out.write_text(render_lesson(L, offline=False), encoding="utf-8")
        write_redirect(
            LEC / f"leccion-{L['n']:02d}.html",
            out.name,
            f"Lección {L['n']:02d} (alias)",
        )
        print("Wrote", out.name)

    write_hub()
    update_descargas()
    update_index()
    build_offline_pack()
    print("DONE available=", AVAILABLE, "total=", TOTAL)


if __name__ == "__main__":
    main()
