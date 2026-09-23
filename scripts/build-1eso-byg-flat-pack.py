#!/usr/bin/env python3
"""Build online shell + flat offline pack for 1º ESO Biología y Geología (L01–L40)."""
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
AVAILABLE = 40

# Full temario titles (curso completo L01–L40)
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

    {
        "n": 11,
        "slug": "estructura-de-la-geosfera-y-movimientos-de-la-tierra",
        "eyebrow": "Lección 11 · UD B · Geosfera",
        "title_html": "<em>Estructura de la geosfera</em> y movimientos de la Tierra",
        "title_plain": "Estructura de la geosfera y movimientos de la Tierra",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque B",
        "curiosidad_t": "Naranja abierta, planeta vivo",
        "curiosidad": (
            "Desde Wegener hasta la sismología moderna, la Tierra se entiende mejor en "
            "<strong>corte</strong>: capas con distinta composición y comportamiento. "
            "Rotación y traslación —conocidas desde la Antigüedad, precisadas después— "
            "explican día/noche y, con el eje inclinado, las estaciones que notamos en CyL."
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            "Identificar las capas del corte: <strong>corteza, manto, núcleo externo e interno</strong>.",
            "Distinguir modelo <strong>geodinámico</strong> (comportamiento) y <strong>geoquímico</strong> (composición).",
            "Explicar <strong>rotación</strong> (día/noche) y <strong>traslación</strong> (año / estaciones con eje inclinado).",
            "Relacionar el corte con lo que «vivimos» en la corteza.",
            "Usar el mnemónico Co-Man-NuEx-NuIn y RoTa.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>La <strong>geosfera</strong> es la parte sólida de la Tierra. En un <strong>corte</strong> (como naranja abierta) ves:</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.35rem"><strong>Corteza</strong> — fina y rocosa; vivimos aquí</p>
      <p style="margin:0 0 0.35rem"><strong>Manto</strong> — la más gruesa; rocas calientes</p>
      <p style="margin:0 0 0.35rem"><strong>Núcleo externo</strong> — Fe+Ni <strong>líquido</strong></p>
      <p style="margin:0"><strong>Núcleo interno</strong> — Fe+Ni <strong>sólido</strong> (por la presión)</p>
    </div>
    <p><strong>Modelo geodinámico:</strong> capas según cómo se comportan (litosfera rígida, astenosfera plástica…).
    <strong>Modelo geoquímico:</strong> según de qué están hechas (silicatos, hierro-níquel…).</p>
    <p><strong>Rotación</strong> ≈ 24 h → día y noche. <strong>Traslación</strong> ≈ 365 días + eje inclinado → estaciones.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Co-Man-NuEx-NuIn» y «RoTa» (Rotación / Traslación).</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Invierno/verano marcados por <strong>traslación</strong> + inclinación del eje.",
            "Día y noche = <strong>rotación</strong> (reloj solar o la sombra del recreo).",
            "Sismos lejanos nos recuerdan un planeta en capas (ondas que viajan por el interior).",
            "L06–L10 hablan de rocas de la corteza; L11 sitúa esa corteza en el corte completo.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Geosfera · corte y movimientos", "l11-geosfera-movimientos.html"),
        ],
        "reto_t": "Explica el corte en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante "
            "de esta lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L11",
        "cierre": (
            "<strong>Co-Man-NuEx-NuIn · RoTa.</strong> "
            "Corteza fina; núcleo externo líquido; rotación = día/noche."
        ),
    },
    {
        "n": 12,
        "slug": "atmosfera-composicion-y-estructura",
        "eyebrow": "Lección 12 · UD C · Atmósfera e hidrosfera",
        "title_html": "<em>Atmósfera</em>: composición y estructura",
        "title_plain": "Atmósfera: composición y estructura",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque C",
        "curiosidad_t": "Capas de aire, no de magia",
        "curiosidad": (
            "Hasta el siglo XX se pensaba a veces en una atmósfera «uniforme». "
            "Globos, cohetes y satélites mostraron <strong>capas</strong> con distinto "
            "comportamiento térmico. El clima que sentimos ocurre abajo, en la "
            "<strong>troposfera</strong>; el ozono protector, en gran parte, más arriba."
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            "Nombrar las capas principales de la atmósfera (de abajo a arriba).",
            "Recordar que el aire seco es ~<strong>78 % N₂</strong> y ~<strong>21 % O₂</strong>.",
            "Situar el clima en la <strong>troposfera</strong> y el ozono (en gran parte) en la <strong>estratosfera</strong>.",
            "Relacionar composición con lo que respiramos.",
            "Usar el mnemónico Tri-Es-Me-Ter-Ex · Ni-Oxi.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>La <strong>atmósfera</strong> es la envoltura de gases.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.35rem"><strong>Capas (abajo → arriba):</strong> troposfera → estratosfera → mesosfera → termosfera → exosfera</p>
      <p style="margin:0"><strong>Composición (aire seco, aprox.):</strong> N₂ ~78 %, O₂ ~21 %, argón ~0,9 %, CO₂ ~0,04 %, más vapor de agua variable</p>
    </div>
    <p>El <strong>tiempo</strong> (nubes, lluvia) ocurre en la troposfera. Gran parte del <strong>ozono</strong> protector está en la estratosfera.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Tri-Es-Me-Ter-Ex» · «Ni-Oxi» (78 / 21).</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "El tiempo en Valladolid, León o Burgos ocurre en la <strong>troposfera</strong>.",
            "Partículas y nieblas de valle: fenómenos de la capa más baja.",
            "AEMET informa del tiempo troposférico, no de la termosfera.",
            "Respiramos ~21 % de oxígeno: dato útil frente a mitos de «aire puro» mágicos.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Atmósfera · capas y composición", "l12-atmosfera-composicion-estructura.html"),
        ],
        "reto_t": "Capas en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante "
            "de esta lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L12",
        "cierre": (
            "<strong>Tri-Es-Me-Ter-Ex · Ni-Oxi.</strong> "
            "Clima abajo; ozono (en gran parte) en estratosfera."
        ),
    },
    {
        "n": 13,
        "slug": "contaminacion-efecto-invernadero-ozono-y-agenda-2030",
        "eyebrow": "Lección 13 · UD C · Atmósfera e hidrosfera",
        "title_html": "Contaminación, efecto invernadero, ozono y <em>Agenda 2030</em>",
        "title_plain": "Contaminación, efecto invernadero, ozono y Agenda 2030",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque C",
        "curiosidad_t": "Invernadero natural, exceso humano",
        "curiosidad": (
            "Fourier y Tyndall intuían que ciertos gases retienen calor; Arrhenius calculó "
            "el papel del CO₂. El <strong>efecto invernadero natural</strong> permite la vida; "
            "el exceso lo desequilibra. La capa de ozono y la Agenda 2030 añaden otra lección: "
            "ciencia + cooperación internacional."
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            "Ejemplificar <strong>contaminación</strong> del aire.",
            "Explicar efecto invernadero (<strong>natural vs exceso</strong>).",
            "Diferenciar ozono «bueno» (alto) y su papel frente a UV.",
            "Relacionar medidas con <strong>Agenda 2030</strong> / ODS.",
            "Usar el mnemónico COIA.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <div class="tarjeta">
      <p style="margin:0 0 0.35rem"><strong>Contaminación atmosférica</strong> — partículas y gases nocivos (tráfico, industrias…)</p>
      <p style="margin:0 0 0.35rem"><strong>Efecto invernadero</strong> — gases retienen calor; el natural permite vida; el exceso calienta de más</p>
      <p style="margin:0 0 0.35rem"><strong>Capa de ozono</strong> — O₃ en estratosfera filtra UV</p>
      <p style="margin:0"><strong>Agenda 2030</strong> — plan ONU; ODS 13 (clima), 7 (energía limpia), 11 (ciudades)…</p>
    </div>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico COIA:</strong> Contaminación · invernadero · Ozono · Agenda 2030</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Medidas locales: transporte, energía, calidad del aire.",
            "Contrastar titulares con fuentes oficiales (Junta, AEMET, ministerios).",
            "ODS en el centro: proyectos escolares de ahorro y movilidad.",
            "L12 sitúa capas; L13 explica riesgos y respuestas.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("COIA · contaminación, invernadero, ozono", "l13-contaminacion-invernadero-ozono-agenda2030.html"),
        ],
        "reto_t": "COIA en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante "
            "de esta lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L13",
        "cierre": (
            "<strong>COIA.</strong> Invernadero natural ≠ exceso. "
            "Ozono alto filtra UV; Agenda 2030 = medidas."
        ),
    },
    {
        "n": 14,
        "slug": "hidrosfera-y-el-ciclo-del-agua",
        "eyebrow": "Lección 14 · UD C · Atmósfera e hidrosfera",
        "title_html": "<em>Hidrosfera</em> y el ciclo del agua",
        "title_plain": "Hidrosfera y el ciclo del agua",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque C",
        "curiosidad_t": "El mismo vaso, otra nube",
        "curiosidad": (
            "Desde Aristóteles hasta los modelos climáticos actuales, el <strong>ciclo del agua</strong> "
            "explica que el agua no «desaparece»: cambia de estado y de lugar. "
            "Casi toda está en océanos; el agua dulce usable es escasa —por eso importa en CyL."
        ),
        "curiosidad_fig": "olla.svg",
        "objetivos": [
            "Definir <strong>hidrosfera</strong>.",
            "Ordenar evaporación, condensación, precipitación, escorrentía e infiltración.",
            "Comprender que casi toda el agua está en océanos y el agua dulce usable es escasa.",
            "Relacionar el ciclo con ríos y nubes del entorno.",
            "Usar el mnemónico EVaCoPEsIn.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Hidrosfera</strong> = toda el agua del planeta.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.35rem"><strong>Ciclo:</strong> evaporación → condensación (nubes) → precipitación → escorrentía / infiltración</p>
      <p style="margin:0"><strong>Distribución:</strong> océanos ≈ 97 %; el resto incluye hielo, subterránea, lagos, ríos, vapor…</p>
    </div>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «EVaCoPEsIn».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Piensa en el <strong>Duero</strong>: evaporación, nubes, lluvia, río otra vez.",
            "Embalses y sequías: el ciclo no garantiza agua dulce «infinita».",
            "Niebla y rocío: condensación a escala local.",
            "L12–L13 = aire; L14 = agua en movimiento.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Hidrosfera · ciclo del agua", "l14-hidrosfera-ciclo-agua.html"),
        ],
        "reto_t": "Ciclo en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante "
            "de esta lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L14",
        "cierre": (
            "<strong>EVaCoPEsIn.</strong> Hidrosfera = toda el agua; "
            "océanos dominan; dulce usable es escasa."
        ),
    },
    {
        "n": 15,
        "slug": "mares-aguas-continentales-contaminacion-y-uso-sostenible",
        "eyebrow": "Lección 15 · UD C · Atmósfera e hidrosfera",
        "title_html": "Mares, aguas continentales, contaminación y <em>uso sostenible</em>",
        "title_plain": "Mares, aguas continentales, contaminación y uso sostenible",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque C",
        "curiosidad_t": "Mar salado, río de pueblo",
        "curiosidad": (
            "Romanos y pueblos de la Meseta ya distinguían pozos, ríos y mar. "
            "Hoy añadimos <strong>acuíferos</strong>, depuradoras y el reto de no ensuciar "
            "lo que bebe el territorio. Sostenibilidad no es eslogan: es no vertir y sí ahorrar."
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            "Distinguir aguas <strong>marinas</strong> y <strong>continentales</strong> (superficiales/subterráneas).",
            "Ejemplificar <strong>contaminación</strong> del agua.",
            "Proponer <strong>usos sostenibles</strong>.",
            "Situar ríos y embalses de CyL en el mapa mental.",
            "Usar Ma-Su-Sub · No-Viertas / Sí-Ahorras.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <div class="tarjeta">
      <p style="margin:0 0 0.35rem"><strong>Marinas</strong> — saladas (mares/océanos)</p>
      <p style="margin:0 0 0.35rem"><strong>Continentales superficiales</strong> — ríos, lagos, embalses…</p>
      <p style="margin:0 0 0.35rem"><strong>Subterráneas</strong> — acuíferos</p>
      <p style="margin:0 0 0.35rem"><strong>Contaminación</strong> — vertidos, plásticos, abonos en exceso…</p>
      <p style="margin:0"><strong>Uso sostenible</strong> — ahorrar, depurar, no ensuciar, riego eficiente</p>
    </div>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Ma-Su-Sub» · «No-Viertas / Sí-Ahorras».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "<strong>Duero</strong>, Tajo, embalses y acuíferos: agua para pueblos y campos.",
            "Depuradoras municipales: ejemplo de «sí depuras».",
            "Plásticos en cauces: contaminación visible en salidas de campo.",
            "Riego por goteo en huertos escolares = uso sostenible concreto.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Aguas · mares, continentales, sostenible", "l15-mares-continentales-contaminacion.html"),
        ],
        "reto_t": "Agua local en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante "
            "de esta lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L15",
        "cierre": (
            "<strong>Ma-Su-Sub · No-Viertas / Sí-Ahorras.</strong> "
            "Salada ≠ dulce; cuidar lo que bebemos."
        ),
    },
    {
        "n": 16,
        "slug": "por-que-atmosfera-e-hidrosfera-hacen-posible-la-vida",
        "eyebrow": "Lección 16 · UD C · Atmósfera e hidrosfera",
        "title_html": "Por qué atmósfera e hidrosfera hacen posible la <em>vida</em>",
        "title_plain": "Por qué atmósfera e hidrosfera hacen posible la vida",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque C",
        "curiosidad_t": "No es decorado",
        "curiosidad": (
            "Comparar la Tierra con Marte o la Luna deja claro: sin atmósfera protectora "
            "ni agua líquida estable, la vida compleja no encaja. "
            "Oxígeno, escudo UV, temperatura habitable, ciclo del agua y clima "
            "no son adorno: son condiciones."
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            "Relacionar oxígeno, escudo, temperatura, agua y clima con la vida.",
            "Argumentar por qué atmósfera e hidrosfera no son «decorado».",
            "Integrar ideas de L12–L15 en un relato único.",
            "Imaginar qué fallaría sin atmósfera o sin agua líquida.",
            "Usar O-Es-Te-Agua-Cli.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Funciones clave de atmósfera e hidrosfera para la vida:</p>
    <ol>
      <li><strong>Oxígeno</strong> para respirar</li>
      <li><strong>Escudo</strong> (UV / meteoros)</li>
      <li><strong>Temperatura</strong> habitable (invernadero natural)</li>
      <li><strong>Agua líquida</strong> y ciclo</li>
      <li><strong>Clima</strong> y transporte de calor/agua</li>
    </ol>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «O-Es-Te-Agua-Cli».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Sin lluvia ni aire limpio, campos y ciudades de CyL no funcionarían igual.",
            "Sequía + calor extremo: se nota qué es «planeta habitable».",
            "Bosques y cultivos dependen del ciclo del agua troposférico.",
            "Cierre de UD C antes de entrar en la célula (UD D).",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Atmósfera + hidrosfera → vida", "l16-atmosfera-hidrosfera-vida.html"),
        ],
        "reto_t": "5 funciones en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante "
            "de esta lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L16",
        "cierre": (
            "<strong>O-Es-Te-Agua-Cli.</strong> "
            "Atmósfera e hidrosfera no son decorado: hacen posible la vida."
        ),
    },
    {
        "n": 17,
        "slug": "la-celula-unidad-estructural-y-funcional",
        "eyebrow": "Lección 17 · UD D · La célula",
        "title_html": "La célula: <em>unidad estructural y funcional</em>",
        "title_plain": "La célula: unidad estructural y funcional",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque D",
        "curiosidad_t": "Ladrillos vivos",
        "curiosidad": (
            "Hooke vio «celdas» en el corcho (1665); Schleiden y Schwann formularon la "
            "<strong>teoría celular</strong> en el XIX: todos los seres vivos están hechos de células. "
            "Estructural = construyen; funcional = hacen las funciones vitales. "
            "Procariota vs eucariota es el siguiente mapa (L18–L20)."
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            "Definir <strong>célula</strong>.",
            "Explicar unidad <strong>estructural</strong> y <strong>funcional</strong>.",
            "Reconocer <strong>procariota</strong> vs <strong>eucariota</strong> (preview L18–L20).",
            "Relacionar célula con tejidos y órganos.",
            "Usar el mnemónico CE-FU.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>La <strong>célula</strong> es la unidad básica de los seres vivos.</p>
    <div class="tarjeta">
      <p style="margin:0 0 0.35rem"><strong>Estructural</strong> — forma tejidos y órganos (ladrillos)</p>
      <p style="margin:0 0 0.35rem"><strong>Funcional</strong> — realiza nutrición, relación y reproducción</p>
      <p style="margin:0"><strong>Procariota</strong> — sin núcleo · <strong>Eucariota</strong> — con núcleo (animal / vegetal)</p>
    </div>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «CE-FU».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "En el lab del instituto observaréis células (L21); hoy la idea base.",
            "Piel, sangre, hoja de encina: todo arranca en células.",
            "Yogur/compost: mundo microbiano (procariotas) en tu entorno.",
            "Puente UD C → UD D: de planeta habitable a unidad de la vida.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Célula · unidad estructural y funcional", "l17-celula-unidad.html"),
        ],
        "reto_t": "CE-FU en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante "
            "de esta lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L17",
        "cierre": (
            "<strong>CE-FU.</strong> Célula = ladrillo + motor. "
            "Pro sin núcleo; eu con núcleo."
        ),
    },
    {
        "n": 18,
        "slug": "celula-procariota-y-sus-partes",
        "eyebrow": "Lección 18 · UD D · La célula",
        "title_html": "Célula <em>procariota</em> y sus partes",
        "title_plain": "Célula procariota y sus partes",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque D",
        "curiosidad_t": "Sin núcleo, con historia",
        "curiosidad": (
            "Las bacterias son procariotas: ADN en un <strong>nucleoide</strong>, sin membrana nuclear. "
            "Leeuwenhoek las intuyó con lentes simples; hoy sabemos que también pueden tener "
            "cápsula, pared, flagelo o plásmidos. Pequeñas, pero cruciales en yogur, compost e higiene."
        ),
        "curiosidad_fig": "olla.svg",
        "objetivos": [
            "Identificar partes: cápsula, pared, membrana, nucleoide, ribosomas, plásmido, flagelo, pili.",
            "Entender que <strong>no hay núcleo</strong> con membrana.",
            "Relacionar flagelo con movimiento.",
            "Distinguir de la eucariota (L19–L20).",
            "Usar Pro-SIN-núcleo · Ca-Pa-Me-Nu-Ri-Fla.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Procariota</strong> (p. ej. bacteria): ADN en <strong>nucleoide</strong> (sin membrana nuclear).
    Puede tener cápsula, pared, membrana, ribosomas, plásmidos, flagelo y pili.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Pro-SIN-núcleo» · «Ca-Pa-Me-Nu-Ri-Fla».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Yogur, compost, infecciones… el mundo microbiano está en tu entorno (con higiene).",
            "Fermentación en cocina = procariotas trabajando.",
            "No confundir «bacteria = siempre mala»: muchas son útiles.",
            "L17 define; L18 dibuja la pro.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Célula procariota · partes", "l18-celula-procariota.html"),
        ],
        "reto_t": "Nucleoide en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante "
            "de esta lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L18",
        "cierre": (
            "<strong>Pro-SIN-núcleo · Ca-Pa-Me-Nu-Ri-Fla.</strong> "
            "ADN en nucleoide; flagelo para moverse."
        ),
    },
    {
        "n": 19,
        "slug": "celula-eucariota-animal-y-sus-partes",
        "eyebrow": "Lección 19 · UD D · La célula",
        "title_html": "Célula eucariota <em>animal</em> y sus partes",
        "title_plain": "Célula eucariota animal y sus partes",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque D",
        "curiosidad_t": "Núcleo con puerta",
        "curiosidad": (
            "La célula animal eucariota guarda el ADN en un <strong>núcleo</strong> con membrana. "
            "Mitocondrias (energía), RE, Golgi y lisosomas organizan el trabajo interno. "
            "A diferencia de la vegetal: sin pared rígida ni cloroplastos."
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            "Localizar núcleo, membrana, mitocondrias, RE, Golgi, lisosomas, centriolos, ribosomas.",
            "Notar <strong>ausencia</strong> de pared y cloroplastos.",
            "Asociar mitocondria con energía.",
            "Comparar con procariota (L18).",
            "Usar Nu-Mi-RE-Go-Li-Ce.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Célula <strong>animal</strong> = eucariota. Forma flexible. Orgánulos: núcleo, mitocondrias (energía),
    RE, Golgi, lisosomas, centriolos, ribosomas, membrana.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Nu-Mi-RE-Go-Li-Ce».</p>
    </div>
    <p>Sin <strong>pared</strong> de celulosa ni <strong>cloroplastos</strong> (eso es vegetal, L20).</p>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Tus células de la piel o de la sangre son animales eucariotas.",
            "Herida que cicatriza: células trabajando (nutrición, relación).",
            "Microscopio escolar (L21): células de mucosa/epitelio como ejemplo.",
            "L18 pro · L19 animal · L20 vegetal.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Célula animal · orgánulos", "l19-celula-eucariota-animal.html"),
        ],
        "reto_t": "Orgánulos en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante "
            "de esta lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L19",
        "cierre": (
            "<strong>Nu-Mi-RE-Go-Li-Ce.</strong> "
            "Núcleo + mitocondrias; sin pared ni cloroplastos."
        ),
    },
    {
        "n": 20,
        "slug": "celula-eucariota-vegetal-y-sus-partes",
        "eyebrow": "Lección 20 · UD D · La célula",
        "title_html": "Célula eucariota <em>vegetal</em> y sus partes",
        "title_plain": "Célula eucariota vegetal y sus partes",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque D",
        "curiosidad_t": "Pared, verde y vacuola",
        "curiosidad": (
            "La célula vegetal añade tres pistas frente a la animal: "
            "<strong>pared</strong> (celulosa), <strong>cloroplastos</strong> (fotosíntesis) y "
            "<strong>vacuola</strong> central grande. Forma más rectangular/fija. "
            "Pa-Clo-Va resume la diferencia que verás al microscopio."
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            "Reconocer <strong>pared</strong>, <strong>cloroplastos</strong> y <strong>vacuola</strong> grande.",
            "Comparar claramente con la animal (L19).",
            "Explicar fotosíntesis a nivel de orgánulo.",
            "Notar forma más fija/rectangular.",
            "Usar Pa-Clo-Va.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Célula <strong>vegetal</strong>: pared (celulosa), cloroplastos (fotosíntesis), vacuola central grande
    + núcleo, mitocondrias, etc. Forma más rectangular/fija.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Pa-Clo-Va».</p>
    </div>
    <p><strong>Tres diferencias clave vs animal:</strong> pared · cloroplastos · vacuola grande.</p>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Hojas de encina o lechuga del huerto escolar: tejidos de células vegetales.",
            "Verde = cloroplastos trabajando (luz + CO₂ → materia orgánica).",
            "Célula vegetal «hinchada»: vacuola y turgencia.",
            "Cierra el bloque L17–L20 antes del microscopio (L21).",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Célula vegetal · pared, cloroplasto, vacuola", "l20-celula-eucariota-vegetal.html"),
        ],
        "reto_t": "Pa-Clo-Va en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante "
            "de esta lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L20",
        "cierre": (
            "<strong>Pa-Clo-Va.</strong> "
            "Pared · cloroplastos · vacuola: la firma vegetal."
        ),
    },
    {
        "n": 21,
        "slug": "observar-y-comparar-celulas-al-microscopio",
        "eyebrow": "Lección 21 · UD D · La célula",
        "title_html": "Observar y comparar <em>células</em> al microscopio",
        "title_plain": "Observar y comparar células al microscopio",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque D",
        "curiosidad_t": "Poco aumento primero",
        "curiosidad": (
            'En el lab del instituto, la regla de oro del microscopio es empezar con el '
            '<strong>objetivo de menor aumento</strong>: así localizas la muestra sin «perderte». '
            'Luego subes el aumento y comparas: ¿núcleo? ¿pared? ¿verde de cloroplastos?'
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            'Preparar la observación: porta, cubre, enfoque grueso y fino.',
            'Comparar procariota, animal y vegetal al microscopio (o en modelo).',
            'Anotar diferencias visibles: núcleo, pared, cloroplastos, tamaño.',
            'Usar el mnemónico Por-Cu-Fo en el laboratorio.',
            'Relacionar L17–L20 con lo que se ve al microscopio.',
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>El <strong>microscopio óptico</strong> amplía lo que no vemos a simple vista. Para comparar células: enfoca con el objetivo de <strong>menor aumento</strong>, luego sube. Busca: ¿hay <strong>núcleo</strong>? ¿<strong>pared</strong> rígida? ¿color <strong>verde</strong> (cloroplastos)?</p>
    <div class="tarjeta" style="overflow-x:auto">
      <table style="width:100%;border-collapse:collapse;font-size:0.95em">
        <tr><th style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Tipo</th><th style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Qué destacar</th></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Procariota</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Sin núcleo; suele ser más pequeña</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Animal</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Núcleo; sin pared ni cloroplastos</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Vegetal</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Núcleo + pared + cloroplastos + vacuola</td></tr>
      </table>
    </div>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Por-Cu-Fo».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            'En el laboratorio del instituto (CyL) se suele observar epidermis de cebolla (vegetal) y células de mucosa oral (animal).',
            'Epidermis de cebolla (vegetal) y mucosa oral (animal) son clásicos de 1º ESO.',
            'Empieza siempre con poco aumento; después el fino.',
            'Cierra el bloque D (L17–L21) con observación real o modelo.',
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Microscopio · comparar tipos", "l21-observar-celulas-microscopio.html"),
        ],
        "reto_t": "Microscopio en 1 minuto",
        "reto": (
            'Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta '
            'lección en 1 minuto.'
        ),
        "reto_id": "1eso-byg-L21",
        "cierre": '<strong>Por-Cu-Fo.</strong> Porta · Cubre · Enfoque: compara procariota, animal y vegetal.',
    },
    {
        "n": 22,
        "slug": "funciones-vitales-nutricion-relacion-y-reproduccion",
        "eyebrow": "Lección 22 · UD E · Seres vivos",
        "title_html": "Funciones vitales: <em>nutrición</em>, relación y reproducción",
        "title_plain": "Funciones vitales: nutrición, relación y reproducción",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque E",
        "curiosidad_t": "Tres palabras, toda la vida",
        "curiosidad": (
            'Todo ser vivo hace tres cosas: conseguir materia y energía (<strong>nutrición</strong>), '
            'detectar el medio y responder (<strong>relación</strong>) y dar lugar a nuevos '
            'individuos (<strong>reproducción</strong>). Un roble de CyL las hace a su modo; tú '
            'también.'
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            'Definir las tres funciones vitales.',
            'Relacionar cada función con ejemplos de plantas y animales.',
            'Explicar por qué sin alguna de ellas no hay vida plena.',
            'Usar Nu-Re-Re para recordar las tres funciones.',
            'Clasificar ejemplos cotidianos en las tres funciones.',
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Nutrición:</strong> obtener materia y energía (comer, fotosíntesis, respirar…). <strong>Relación:</strong> detectar cambios y responder (luz, sonido, peligro…). <strong>Reproducción:</strong> dar lugar a nuevos individuos (sexual o asexual).</p>
    <p>Todos los seres vivos realizan las tres (aunque no siempre de la misma forma).</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Nu-Re-Re».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            'Un roble de CyL hace fotosíntesis (nutrición), abre/cierra estomas y crece hacia la luz (relación) y produce bellotas (reproducción).',
            'Roble: fotosíntesis, estomas/luz y bellotas = las tres funciones.',
            'Tú: comer, girar la cabeza al oír tu nombre, y… la especie continúa.',
            'Sin alguna de las tres no hay vida «completa» a escala biológica.',
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Tres funciones vitales", "l22-funciones-vitales.html"),
        ],
        "reto_t": "Nu-Re-Re en 1 minuto",
        "reto": (
            'Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta '
            'lección en 1 minuto.'
        ),
        "reto_id": "1eso-byg-L22",
        "cierre": '<strong>Nu-Re-Re.</strong> Nutrición · Relación · Reproducción: las tres funciones vitales.',
    },
    {
        "n": 23,
        "slug": "clasificacion-nomenclatura-binomial-y-especies-de-cyl",
        "eyebrow": "Lección 23 · UD E · Seres vivos",
        "title_html": "Clasificación, <em>nomenclatura binomial</em> y especies de CyL",
        "title_plain": "Clasificación, nomenclatura binomial y especies de CyL",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque E",
        "curiosidad_t": "Dos nombres, un idioma mundial",
        "curiosidad": (
            'Linneo propuso la <strong>nomenclatura binomial</strong>: <em>Género especie</em> (ej. '
            '<em>Quercus ilex</em>, la encina). Así científicos de todo el mundo hablan de lo mismo. '
            'En CyL: encina, lobo ibérico, trucha, águila real…'
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            'Explicar por qué clasificamos a los seres vivos.',
            'Usar nomenclatura binomial (Género especie en cursiva).',
            'Reconocer especies representativas de CyL.',
            'Usar Ge-es (Género · especie).',
            'Citar al menos una especie representativa de CyL.',
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Clasificar = agrupar por <strong>características comunes</strong>. <strong>Nomenclatura binomial</strong> (Linneo): dos nombres en latín — <em>Género</em> + <em>especie</em> (ej. <em>Quercus ilex</em>, la encina).</p>
    <p>En Castilla y León: encina, roble, pino silvestre, lobo ibérico, águila real, trucha común…</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Ge-es».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            'La encina (<em>Quercus ilex</em>) domina muchas dehesas de CyL; el lobo ibérico (<em>Canis lupus signatus</em>) es un mamífero emblemático de la región.',
            'Encina (<em>Quercus ilex</em>) en dehesas; lobo ibérico (<em>Canis lupus signatus</em>).',
            'Clasificar ordena la diversidad y evita confusiones de nombre común.',
            'Género primero, especie después — nunca al revés.',
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Binomial · especies CyL", "l23-clasificacion-nomenclatura-cyl.html"),
        ],
        "reto_t": "Ge-es en 1 minuto",
        "reto": (
            'Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta '
            'lección en 1 minuto.'
        ),
        "reto_id": "1eso-byg-L23",
        "cierre": '<strong>Ge-es.</strong> Género · especie: dos palabras en cursiva para nombrar con precisión.',
    },
    {
        "n": 24,
        "slug": "de-los-antiguos-reinos-a-los-dominios-actuales",
        "eyebrow": "Lección 24 · UD E · Seres vivos",
        "title_html": "De los antiguos <em>reinos</em> a los dominios actuales",
        "title_plain": "De los antiguos reinos a los dominios actuales",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque E",
        "curiosidad_t": "De 5 reinos a 3 dominios",
        "curiosidad": (
            'Clase a clase se enseñaban <strong>cinco reinos</strong> (Monera, Protoctista, Hongos, '
            'Vegetal, Animal). Con genética molecular hoy se usan <strong>tres dominios</strong>: '
            'Bacteria, Archaea y Eukarya. Monera se reparte entre Bacteria y Archaea.'
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            'Nombrar los cinco reinos clásicos.',
            'Nombrar los tres dominios actuales.',
            'Relacionar: Bacteria/Archaea ≈ procariotas; Eukarya ≈ eucariotas (protistas, hongos, plantas, animales).',
            'Usar Mo-Pro-Ho-Ve-An → Bac-Ar-Eu.',
            'Situar hongos, plantas y animales en Eukarya.',
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Antes se hablaba de <strong>5 reinos</strong>: Monera, Protoctista (protistas), Hongos, Vegetal y Animal. Hoy, con datos moleculares, se usan <strong>3 dominios</strong>: - <strong>Bacteria</strong> - <strong>Archaea</strong> - <strong>Eukarya</strong> (incluye protistas, hongos, plantas y animales)</p>
    <p>Monera se reparte entre Bacteria y Archaea.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Mo-Pro-Ho-Ve-An → Bac-Ar-Eu».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            'En el suelo de un robledal de CyL hay bacterias (Bacteria), arqueas en nichos extremos (Archaea) y eucariotas (hongos, plantas, animales).',
            'En un robledal de CyL: bacterias, arqueas (nichos) y eucariotas conviviendo.',
            'Seta, roble y lobo: todos Eukarya.',
            'Actualiza la ficha mental: Monera ya no es un dominio.',
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Reinos → dominios", "l24-reinos-dominios.html"),
        ],
        "reto_t": "Bac-Ar-Eu en 1 minuto",
        "reto": (
            'Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta '
            'lección en 1 minuto.'
        ),
        "reto_id": "1eso-byg-L24",
        "cierre": '<strong>Mo-Pro-Ho-Ve-An → Bac-Ar-Eu.</strong> Cinco reinos clásicos; tres dominios actuales.',
    },
    {
        "n": 25,
        "slug": "hongos-caracteristicas-y-micologia-en-castilla-y-leon",
        "eyebrow": "Lección 25 · UD E · Seres vivos",
        "title_html": "<em>Hongos</em>: características y micología en Castilla y León",
        "title_plain": "Hongos: características y micología en Castilla y León",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque E",
        "curiosidad_t": "Hongos ≠ plantas",
        "curiosidad": (
            'Los hongos no hacen fotosíntesis: son <strong>heterótrofos</strong> con pared de quitina '
            'y esporas. En CyL la <strong>micología</strong> importa (níscalo, boletus…), pero la '
            'regla es clara: sin guía experta, <strong>no comas</strong> una seta. La amanita roja '
            'con puntos es tóxica.'
        ),
        "curiosidad_fig": "olla.svg",
        "objetivos": [
            'Describir rasgos de los hongos (sin clorofila, heterótrofos, paredes de quitina, esporas).',
            'Distinguir setas comestibles de tóxicas sin inventar: solo con guía experta.',
            'Valorar la micología en CyL (níscalo, boletus… y respeto al monte).',
            'Usar Ho-no-pla + ¡Guía!',
            'Explicar por qué no se improvisa con setas.',
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Los <strong>hongos</strong> no son plantas: no hacen fotosíntesis. Se alimentan de materia orgánica; muchos forman <strong>setas</strong> (cuerpo fructífero) con <strong>esporas</strong>.</p>
    <p><strong>Micología en CyL:</strong> muy importante cultural y económica (níscalo <em>Lactarius deliciosus</em>, boletus…). <strong>Nunca</strong> comas una seta sin identificación experta. La <em>Amanita muscaria</em> (roja con puntos) es tóxica; otras amanitas pueden ser mortales.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Ho-no-pla + ¡Guía!».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            'En pinares de Soria, León o Segovia se recolectan níscalos en temporada; siempre con permiso y conocimiento. Si dudas: no la cojas para comer.',
            'Pinares de Soria, León o Segovia: níscalos con permiso y conocimiento.',
            'Si dudas: no la cojas para comer.',
            'Micología = ciencia de los hongos; seta = cuerpo fructífero.',
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Hongos · micología CyL", "l25-hongos-micologia-cyl.html"),
        ],
        "reto_t": "Ho-no-pla en 1 minuto",
        "reto": (
            'Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta '
            'lección en 1 minuto.'
        ),
        "reto_id": "1eso-byg-L25",
        "cierre": '<strong>Ho-no-pla + ¡Guía!</strong> Hongos ≠ plantas; identifica con experto o no comas.',
    },
    {
        "n": 26,
        "slug": "plantas-grupos-flor-fruto-y-semilla",
        "eyebrow": "Lección 26 · UD E · Seres vivos",
        "title_html": "Plantas: grupos, <em>flor</em>, fruto y semilla",
        "title_plain": "Plantas: grupos, flor, fruto y semilla",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque E",
        "curiosidad_t": "Flor → fruto → semilla",
        "curiosidad": (
            'Las <strong>angiospermas</strong> siguen el camino flor → fruto → semilla. Las '
            '<strong>gimnospermas</strong> (pino) llevan semillas en piña, sin fruto típico. En CyL: '
            'pinos en la Cordillera y Sistema Ibérico; encinas y robles en dehesas.'
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            'Distinguir grupos básicos (musgos, helechos, gimnospermas, angiospermas) a nivel 1º ESO.',
            'Identificar piezas de la flor y relacionar flor→fruto→semilla.',
            'Comparar gimnospermas (piñas) y angiospermas (flores / frutos).',
            'Usar Flo-Fru-Sem.',
            'Relacionar estambres y pistilo con la reproducción.',
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Plantas:</strong> autótrofas con fotosíntesis.</p>
    <div class="tarjeta" style="overflow-x:auto">
      <table style="width:100%;border-collapse:collapse;font-size:0.95em">
        <tr><th style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Grupo</th><th style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Idea</th></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Musgos</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Sin vasos verdaderos; viven húmedos</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Helechos</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Con vasos; esporas (sin semilla)</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Gimnospermas</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Semillas en piña (pino)</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Angiospermas</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Flor → fruto con semillas</td></tr>
      </table>
    </div>
    <p><strong>Flor:</strong> sépalos, pétalos, estambres (♂), pistilo (♀). Tras la fecundación: <strong>fruto</strong> que guarda la <strong>semilla</strong>.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Flo-Fru-Sem».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            'Pinos (gimnospermas) en Cordillera Cantábrica y Sistema Ibérico; encinas y robles (angiospermas) en dehesas y bosques de CyL.',
            'Estambres (♂) y pistilo (♀): piezas clave de la flor.',
            'Helechos: vasos sí, semillas no (esporas).',
            'Musgos: viven húmedos, sin vasos verdaderos.',
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Flor · fruto · semilla", "l26-plantas-flor-fruto-semilla.html"),
        ],
        "reto_t": "Flo-Fru-Sem en 1 minuto",
        "reto": (
            'Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta '
            'lección en 1 minuto.'
        ),
        "reto_id": "1eso-byg-L26",
        "cierre": '<strong>Flo-Fru-Sem.</strong> Flor → fruto → semilla; el pino va por piñas (gimnosperma).',
    },
    {
        "n": 27,
        "slug": "animales-invertebrados-anatomia-y-fisiologia-basicas",
        "eyebrow": "Lección 27 · UD E · Seres vivos",
        "title_html": "Animales <em>invertebrados</em>: anatomía y fisiología básicas",
        "title_plain": "Animales invertebrados: anatomía y fisiología básicas",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque E",
        "curiosidad_t": "Sin columna, con mil formas",
        "curiosidad": (
            'Los <strong>invertebrados</strong> no tienen columna vertebral y son la mayoría de las '
            'especies: lombrices (anélidos), caracoles (moluscos), insectos y arañas (artrópodos)… En '
            'huertos y ríos de CyL los tienes a diario.'
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            'Definir invertebrado (sin columna vertebral).',
            'Reconocer grupos: poríferos, cnidarios, anélidos, moluscos, artrópodos, equinodermos (nivel 1º).',
            'Relacionar forma y función básica (caparazón, patas articuladas, segmentos…).',
            'Usar In-ver = sin vértebras.',
            'Citar un invertebrado del entorno de CyL.',
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Invertebrados:</strong> animales <strong>sin</strong> columna vertebral. Son la mayoría de las especies.</p>
    <div class="tarjeta" style="overflow-x:auto">
      <table style="width:100%;border-collapse:collapse;font-size:0.95em">
        <tr><th style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Grupo</th><th style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Ejemplo</th><th style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Idea</th></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Anélidos</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Lombriz</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Cuerpo segmentado</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Moluscos</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Caracol</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Pie muscular; muchos con concha</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Artrópodos</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Insecto, araña</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Patas articuladas + exoesqueleto</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Cnidarios</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Medusa</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Células urticantes</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Equinodermos</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Estrella</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Piel con espinas / placas</td></tr>
      </table>
    </div>
    <p>Fisiología básica: se alimentan, respiran (piel, branquias, tráqueas…), se relacionan y reproducen de formas muy variadas.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «In-ver = sin vértebras».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            'En huertos y ríos de CyL: lombrices, caracoles, insectos polinizadores, cangrejos de río (protegidos / especies sensibles).',
            'Lombriz = anélido segmentado; caracol = molusco con concha.',
            'Mariposa y araña = artrópodos (patas articuladas + exoesqueleto).',
            'Cangrejos de río: especies sensibles — respeta el cauce.',
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Invertebrados del entorno", "l27-invertebrados.html"),
        ],
        "reto_t": "In-ver en 1 minuto",
        "reto": (
            'Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta '
            'lección en 1 minuto.'
        ),
        "reto_id": "1eso-byg-L27",
        "cierre": '<strong>In-ver = sin vértebras.</strong> Anélidos, moluscos, artrópodos… anatomía distinta, sin columna.',
    },
    {
        "n": 28,
        "slug": "animales-vertebrados-y-animales-como-seres-sintientes",
        "eyebrow": "Lección 28 · UD E · Seres vivos",
        "title_html": "Animales <em>vertebrados</em> y animales como seres sintientes",
        "title_plain": "Animales vertebrados y animales como seres sintientes",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque E",
        "curiosidad_t": "Cinco grupos + respeto",
        "curiosidad": (
            'Peces, anfibios, reptiles, aves y mamíferos: los cinco grupos de '
            '<strong>vertebrados</strong>. Además, el decreto recuerda que los animales son '
            '<strong>seres sintientes</strong>: sienten y merecen trato ético en el campo y en casa.'
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            'Nombrar los 5 grupos de vertebrados y un rasgo de cada uno.',
            'Relacionar anatomía básica (aletas, pulmones, plumas, pelo, amnios…).',
            'Explicar que los animales son <strong>seres sintientes</strong>: sienten y hay que respetarlos.',
            'Usar Pe-An-Re-Av-Ma + Siento.',
            'Dar un ejemplo de trato ético hacia animales.',
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Vertebrados:</strong> tienen columna vertebral.</p>
    <div class="tarjeta" style="overflow-x:auto">
      <table style="width:100%;border-collapse:collapse;font-size:0.95em">
        <tr><th style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Grupo</th><th style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Rasgo clave</th></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Peces</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Branquias; aletas; vida acuática</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Anfibios</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Piel húmeda; metamorfo (renacuajo→rana)</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Reptiles</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Escamas; respiración pulmonar</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Aves</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Plumas; pico; homeotermos</td></tr>
        <tr><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Mamíferos</td><td style="border:1px solid #E8E0D0;padding:0.35rem 0.5rem;text-align:left">Pelo; glándulas mamarias</td></tr>
      </table>
    </div>
    <p><strong>Seres sintientes:</strong> pueden sentir (dolor, miedo, bienestar). La ciencia y las leyes piden <strong>trato ético</strong>: no maltratar, cuidar mascotas y fauna silvestre.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Pe-An-Re-Av-Ma + Siento».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            'En CyL: trucha (pez), sapo (anfibio), lagarto (reptil), águila / buitre (aves), ciervo / lobo / oveja (mamíferos). Respeto en el campo y en casa.',
            'CyL: trucha, sapo, lagarto, águila, ciervo / lobo / oveja.',
            'Homeotermos: aves y mamíferos mantienen temperatura.',
            'Sintiente ≠ «solo mascota»: fauna silvestre también.',
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Vertebrados · sintiencia", "l28-vertebrados-sintientes.html"),
        ],
        "reto_t": "Pe-An-Re-Av-Ma en 1 minuto",
        "reto": (
            'Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta '
            'lección en 1 minuto.'
        ),
        "reto_id": "1eso-byg-L28",
        "cierre": '<strong>Pe-An-Re-Av-Ma + Siento.</strong> Cinco grupos de vertebrados; todos sintientes.',
    },
    {
        "n": 29,
        "slug": "identificar-especies-del-entorno-guias-y-claves",
        "eyebrow": "Lección 29 · UD E · Seres vivos",
        "title_html": "Identificar especies del entorno (<em>guías y claves</em>)",
        "title_plain": "Identificar especies del entorno (guías y claves)",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque E",
        "curiosidad_t": "No adivines: pregunta sí/no",
        "curiosidad": (
            'Una <strong>clave dicotómica</strong> es un árbol de decisiones (sí/no) hasta nombrar el '
            'grupo o la especie. Combínala con <strong>visu</strong>, guía de campo y apps — siempre '
            'contrastando. Observa; no arranques ni molestes sin necesidad.'
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            'Usar una clave dicotómica sencilla (sí/no).',
            'Combinar visu (observar), guías de campo y herramientas digitales con criterio.',
            'Identificar especies comunes del entorno sin dañarlas.',
            'Usar Vi-Gu-Cla-Di.',
            'Aplicar una clave dicotómica sencilla de dos pasos.',
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Identificar</strong> = poner nombre correcto a lo que ves.</p>
    <p>Herramientas del decreto: - <strong>Visu:</strong> mirar con atención (forma, color, hábitat). - <strong>Guías</strong> de campo (libros / fichas). - <strong>Claves dicotómicas:</strong> preguntas de dos opciones (sí/no) hasta llegar a la especie o grupo. - <strong>Herramientas digitales:</strong> apps y webs — siempre contrastar.</p>
    <p>Regla de oro: observa, no arranques ni molestes sin necesidad.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Vi-Gu-Cla-Di».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            'En un paseo por la ribera del Pisuerga o un robledal: usa una clave de hojas (lobulada / entera…) o una guía de aves de CyL.',
            'Ribera del Pisuerga o robledal: clave de hojas o guía de aves.',
            'Apps ayudan, no sustituyen el contraste con guía.',
            'Regla de oro: observa, no destroces el entorno.',
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Claves · guías · visu", "l29-identificar-especies.html"),
        ],
        "reto_t": "Vi-Gu-Cla-Di en 1 minuto",
        "reto": (
            'Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta '
            'lección en 1 minuto.'
        ),
        "reto_id": "1eso-byg-L29",
        "cierre": '<strong>Vi-Gu-Cla-Di.</strong> Visu · Guía · Clave · Digital: identifica sin dañar.',
    },
    {
        "n": 30,
        "slug": "ecosistemas-del-entorno-y-sus-elementos",
        "eyebrow": "Lección 30 · UD F · Ecología y sostenibilidad",
        "title_html": "<em>Ecosistemas</em> del entorno y sus elementos",
        "title_plain": "Ecosistemas del entorno y sus elementos",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque F",
        "curiosidad_t": "Biótico + abiótico + relaciones",
        "curiosidad": (
            'Un <strong>ecosistema</strong> une seres vivos (<strong>bióticos</strong>), factores del '
            'medio (<strong>abióticos</strong>: luz, agua, suelo…) y las <strong>relaciones</strong> '
            'entre ellos. Dehesa, pinar, ribera del Duero o parque urbano: todos son ecosistemas de '
            'CyL.'
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            'Definir ecosistema (seres vivos + medio + relaciones).',
            'Distinguir factores bióticos y abióticos.',
            'Describir un ecosistema cercano (dehesa, río, bosque, parque).',
            'Usar Bio-Abio-Rel.',
            'Describir un ecosistema cercano con bióticos y abióticos.',
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Un <strong>ecosistema</strong> = <strong>bióticos</strong> (seres vivos) + <strong>abióticos</strong> (luz, agua, suelo, temperatura…) + <strong>relaciones</strong> entre ellos.</p>
    <p>Ejemplos en CyL: dehesa, pinar, ribera fluvial, páramo, parque urbano.</p>
    <p>Elementos: - Productores (plantas) - Consumidores (herbívoros, carnívoros) - Descomponedores (hongos, bacterias) - Medio físico (sol, agua, rocas, aire)</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «Bio-Abio-Rel».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            'Una dehesa de encinas en Salamanca o un tramo del Duero: sol, suelo, agua, encinas, insectos, aves, hongos… forman el ecosistema.',
            'Dehesa de encinas en Salamanca o tramo del Duero: ejemplo cercano.',
            'Productores, consumidores y descomponedores + medio físico.',
            'Cierra el bloque F de ecosistemas; L31–L40 completan relaciones y sostenibilidad.',
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Ecosistema del entorno", "l30-ecosistemas-entorno.html"),
        ],
        "reto_t": "Bio-Abio-Rel en 1 minuto",
        "reto": (
            'Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta '
            'lección en 1 minuto.'
        ),
        "reto_id": "1eso-byg-L30",
        "cierre": '<strong>Bio-Abio-Rel.</strong> Bióticos + abióticos + relaciones = ecosistema.',
    },
    {
        "n": 31,
        "slug": "relaciones-intraespecificas-e-interespecificas",
        "eyebrow": "Lección 31 · UD F · Ecología y sostenibilidad",
        "title_html": "Relaciones <em>intraespecíficas</em> e <em>interespecíficas</em>",
        "title_plain": "Relaciones intraespecíficas e interespecíficas",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque F",
        "curiosidad_t": "INTRA = misma · INTER = distintas",
        "curiosidad": (
            "Las relaciones ecológicas unen a los seres vivos. "
            "<strong>Intraespecífica</strong>: misma especie (manada, familia…). "
            "<strong>Interespecífica</strong>: especies distintas (depredación, mutualismo…)."
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            "Distinguir relaciones <strong>intraespecíficas</strong> e <strong>interespecíficas</strong>.",
            "Reconocer cooperación, competencia, depredación, mutualismo y parasitismo.",
            "Poner un ejemplo cercano (CyL o patio/parque).",
            "Usar el mnemónico INTRA / INTER.",
            "Clasificar una relación dada como intra o inter.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Las <strong>relaciones ecológicas</strong> unen a los seres vivos.</p>
    <ul>
      <li><strong>Intraespecífica:</strong> entre individuos de la <strong>misma</strong> especie (manada, familia, competencia por pareja).</li>
      <li><strong>Interespecífica:</strong> entre <strong>especies distintas</strong>.</li>
    </ul>
    <table>
      <thead><tr><th>Tipo inter</th><th>Idea</th></tr></thead>
      <tbody>
        <tr><td>Depredación</td><td>Uno caza y se come al otro</td></tr>
        <tr><td>Competencia</td><td>Compiten por el mismo recurso</td></tr>
        <tr><td>Mutualismo</td><td>Ambos salen beneficiados</td></tr>
        <tr><td>Parasitismo</td><td>Uno se beneficia y el otro sale perjudicado</td></tr>
      </tbody>
    </table>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «INTRA = misma · INTER = distintas».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Lobos en manada (intraespecífica) en paisajes de CyL.",
            "Lobo y conejo: depredación (interespecífica).",
            "Abeja y flor: mutualismo; dos encinas por la luz: competencia.",
            "Garrapata en un ciervo: parasitismo.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Relaciones intra e inter", "l31-relaciones-intra-inter.html"),
        ],
        "reto_t": "INTRA / INTER en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta "
            "lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L31",
        "cierre": "<strong>INTRA = misma · INTER = distintas.</strong> Clasifica siempre la relación antes de nombrar el tipo.",
    },
    {
        "n": 32,
        "slug": "cadenas-redes-y-piramides-troficas",
        "eyebrow": "Lección 32 · UD F · Ecología y sostenibilidad",
        "title_html": "Cadenas, redes y <em>pirámides tróficas</em>",
        "title_plain": "Cadenas, redes y pirámides tróficas",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque F",
        "curiosidad_t": "PRO-CON-DES",
        "curiosidad": (
            "La <strong>estructura trófica</strong> cuenta cómo fluye la materia y la energía: "
            "<strong>cadena</strong> (línea), <strong>red</strong> (telaraña) y <strong>pirámide</strong> "
            "(base = productores)."
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            "Explicar <strong>cadena trófica</strong> (quién come a quién).",
            "Diferenciar cadena, red y pirámide trófica.",
            "Situar productores, consumidores y descomponedores.",
            "Usar PRO-CON-DES.",
            "Completar una cadena sencilla de dehesa o ribera.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>La <strong>estructura trófica</strong> cuenta cómo fluye la materia y la energía.</p>
    <ul>
      <li><strong>Cadena:</strong> línea simple: hierba → conejo → zorro.</li>
      <li><strong>Red:</strong> muchas cadenas cruzadas (parece una <strong>telaraña</strong> de comidas).</li>
      <li><strong>Pirámide:</strong> niveles; la base son los <strong>productores</strong>; arriba hay menos biomasa/energía disponible.</li>
    </ul>
    <p>Niveles: productores → consumidores 1º → 2º → … + descomponedores.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «PRO-CON-DES (Productor · Consumidor · Descomponedor)».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "En una dehesa o ribera de CyL: encinas/hierba (productores).",
            "Insectos y conejos (herbívoros / consumidores 1º).",
            "Rapaces y carnívoros (consumidores superiores).",
            "Hongos y bacterias: descomponedores que cierran el ciclo.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Cadenas, redes y pirámides", "l32-cadenas-redes-piramides.html"),
        ],
        "reto_t": "PRO-CON-DES en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta "
            "lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L32",
        "cierre": "<strong>PRO-CON-DES.</strong> Cadena = línea; red = telaraña; pirámide = base de productores.",
    },
    {
        "n": 33,
        "slug": "conservar-ecosistemas-biodiversidad-y-desarrollo-sostenible",
        "eyebrow": "Lección 33 · UD F · Ecología y sostenibilidad",
        "title_html": "Conservar ecosistemas, <em>biodiversidad</em> y desarrollo sostenible",
        "title_plain": "Conservar ecosistemas, biodiversidad y desarrollo sostenible",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque F",
        "curiosidad_t": "HOY-sin-agotar-MAÑANA",
        "curiosidad": (
            "<strong>Conservar</strong> es cuidar para que el ecosistema siga funcionando. "
            "<strong>Desarrollo sostenible</strong>: cubrir necesidades de <strong>hoy</strong> "
            "sin agotar las de <strong>mañana</strong>."
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            "Explicar por qué importa conservar ecosistemas y biodiversidad.",
            "Definir <strong>desarrollo sostenible</strong> con palabras propias.",
            "Proponer una acción concreta y cercana.",
            "Usar HOY-sin-agotar-MAÑANA.",
            "Relacionar biodiversidad con servicios del ecosistema.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Conservar</strong> = cuidar para que el ecosistema siga funcionando.</p>
    <p><strong>Biodiversidad</strong> = variedad de seres vivos y de hábitats.</p>
    <p><strong>Desarrollo sostenible</strong> = cubrir necesidades de <strong>hoy</strong> sin agotar las de <strong>mañana</strong> (recursos, hábitats, clima).</p>
    <p>Si perdemos especies o suelos, perdemos servicios: agua limpia, polinización, alimentos, belleza del paisaje.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «HOY-sin-agotar-MAÑANA».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Montes, riberas y dehesas de CyL: biodiversidad local = calidad de vida.",
            "Agua limpia, suelo fértil y polinización son servicios del ecosistema.",
            "Turismo respetuoso y gestión responsable también son conservación.",
            "Una acción cercana: cuidar un tramo de ribera o el huerto escolar.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Conservar y desarrollo sostenible", "l33-conservar-biodiversidad-sostenible.html"),
        ],
        "reto_t": "HOY-sin-agotar-MAÑANA en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta "
            "lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L33",
        "cierre": "<strong>HOY-sin-agotar-MAÑANA.</strong> Conservar biodiversidad es también cuidar servicios del ecosistema.",
    },
    {
        "n": 34,
        "slug": "especies-amenazadas-y-figuras-de-proteccion-ambiental",
        "eyebrow": "Lección 34 · UD F · Ecología y sostenibilidad",
        "title_html": "Especies <em>amenazadas</em> y figuras de protección ambiental",
        "title_plain": "Especies amenazadas y figuras de protección ambiental",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque F",
        "curiosidad_t": "LUGAR + ESPECIE = PROTECCIÓN",
        "curiosidad": (
            "Una <strong>especie amenazada</strong> corre riesgo serio de desaparecer. "
            "Proteger el <strong>lugar</strong> (parque, ZEPA, reserva…) ayuda a proteger a las "
            "<strong>especies</strong> que viven ahí."
        ),
        "curiosidad_fig": "mapa.svg",
        "objetivos": [
            "Explicar qué es una <strong>especie amenazada</strong>.",
            "Reconocer figuras de protección (parque nacional/natural, Red Natura, reserva…).",
            "Relacionar protección del lugar y de la especie.",
            "Usar LUGAR + ESPECIE = PROTECCIÓN.",
            "Respetar normas en rutas y espacios protegidos de CyL.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Especie amenazada:</strong> corre riesgo serio de desaparecer si no se actúa.</p>
    <p><strong>Figuras de protección</strong> (ejemplos):</p>
    <ul>
      <li>Parque Nacional (protección muy alta)</li>
      <li>Parque Natural / Regional (CyL tiene varios)</li>
      <li>ZEPA / LIC (Red Natura 2000: aves / hábitats)</li>
      <li>Reserva o monumento natural</li>
    </ul>
    <p>Proteger el <strong>lugar</strong> ayuda a proteger a las <strong>especies</strong> que viven ahí.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «LUGAR + ESPECIE = PROTECCIÓN».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "En CyL hay parques naturales, ZEPA y otras figuras de protección.",
            "En rutas: mirar carteles y respetar normas.",
            "No molestar fauna ni dejar basura en espacios protegidos.",
            "Proteger el hábitat es proteger a las especies amenazadas.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Amenazadas y protección", "l34-especies-amenazadas-proteccion.html"),
        ],
        "reto_t": "LUGAR + ESPECIE en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta "
            "lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L34",
        "cierre": "<strong>LUGAR + ESPECIE = PROTECCIÓN.</strong> Amenazada ≠ extinguida: aún se puede actuar.",
    },
    {
        "n": 35,
        "slug": "atmosfera-hidrosfera-geosfera-y-biosfera-suelo-y-relieve",
        "eyebrow": "Lección 35 · UD F · Ecología y sostenibilidad",
        "title_html": "Atmósfera, hidrosfera, geosfera y biosfera: <em>suelo y relieve</em>",
        "title_plain": "Atmósfera, hidrosfera, geosfera y biosfera: suelo y relieve",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque F",
        "curiosidad_t": "A-H-G-B → SUELO y RELIEVE",
        "curiosidad": (
            "Las cuatro esferas (<strong>atmósfera, hidrosfera, geosfera, biosfera</strong>) "
            "interactúan en la <strong>edafogénesis</strong> (formación del suelo) y en el "
            "<strong>modelado del relieve</strong>."
        ),
        "curiosidad_fig": "olla.svg",
        "objetivos": [
            "Nombrar las cuatro esferas y qué aporta cada una.",
            "Explicar que el suelo nace de interacciones (<strong>edafogénesis</strong>).",
            "Relacionar modelado del relieve con agua, aire, roca y seres vivos.",
            "Usar A-H-G-B → SUELO y RELIEVE.",
            "Poner un ejemplo de CyL (páramo, hoz, ribera…).",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Cuatro “capas” del sistema Tierra:</p>
    <ul>
      <li><strong>Atmósfera</strong> (aire)</li>
      <li><strong>Hidrosfera</strong> (agua)</li>
      <li><strong>Geosfera</strong> (rocas, relieve)</li>
      <li><strong>Biosfera</strong> (seres vivos)</li>
    </ul>
    <p><strong>Edafogénesis:</strong> formación del <strong>suelo</strong> (roca + clima + agua + seres vivos + tiempo).</p>
    <p><strong>Modelado del relieve:</strong> ríos, viento, hielo, gravedad y seres vivos desgastan y construyen formas del terreno.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «A-H-G-B → SUELO y RELIEVE».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Páramos, hoces, riberas y suelos agrícolas de CyL nacen de esas interacciones.",
            "Clima + agua + roca + seres vivos + tiempo = suelo.",
            "El viento y los ríos también modelan el relieve.",
            "Sin suelo fértil y relieve estable, la vida terrestre se complica.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Esferas, suelo y relieve", "l35-esferas-suelo-relieve.html"),
        ],
        "reto_t": "A-H-G-B en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta "
            "lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L35",
        "cierre": "<strong>A-H-G-B → SUELO y RELIEVE.</strong> Las esferas no trabajan aisladas.",
    },
    {
        "n": 36,
        "slug": "cambio-climatico-y-consecuencias-en-los-ecosistemas",
        "eyebrow": "Lección 36 · UD F · Ecología y sostenibilidad",
        "title_html": "<em>Cambio climático</em> y consecuencias en los ecosistemas",
        "title_plain": "Cambio climático y consecuencias en los ecosistemas",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque F",
        "curiosidad_t": "CAUSA → CALOR → ECOSISTEMA",
        "curiosidad": (
            "El <strong>cambio climático</strong> es un cambio a <strong>largo plazo</strong> "
            "(no el tiempo de mañana). Actividades humanas refuerzan el efecto invernadero; "
            "en clase <strong>no inventamos cifras</strong>."
        ),
        "curiosidad_fig": "fuego.svg",
        "objetivos": [
            "Relacionar actividades humanas con el refuerzo del efecto invernadero.",
            "Describir consecuencias generales en ecosistemas (sin inventar cifras).",
            "Distinguir clima (largo plazo) de tiempo atmosférico (días).",
            "Usar CAUSA → CALOR → ECOSISTEMA.",
            "Observar el entorno de CyL sin alarmismo falso ni negación.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Cambio climático:</strong> cambio a <strong>largo plazo</strong> del clima del planeta.</p>
    <p><strong>Causas humanas principales (idea):</strong> quema de combustibles, deforestación y aumento de ciertos <strong>gases de efecto invernadero</strong> → se retiene más calor.</p>
    <p><strong>Consecuencias en ecosistemas</strong> (honestas, sin números inventados):</p>
    <ul>
      <li>Cambios de temperatura y lluvias</li>
      <li>Estrés en especies (migración, ciclos de vida)</li>
      <li>Riesgo en hábitats sensibles</li>
      <li>Relación con fenómenos extremos (olas de calor, sequías)</li>
    </ul>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «CAUSA → CALOR → ECOSISTEMA». Sin porcentajes inventados.</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "En CyL se notan sequías, olas de calor y cambios en ríos/montes.",
            "Observar el entorno ayuda a entender el tema con rigor.",
            "Clima ≠ el tiempo de mañana: es a largo plazo.",
            "Usa fuentes científicas; no inventes porcentajes en el examen.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Cambio climático y ecosistemas", "l36-cambio-climatico-ecosistemas.html"),
        ],
        "reto_t": "CAUSA → CALOR → ECOSISTEMA",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta "
            "lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L36",
        "cierre": "<strong>CAUSA → CALOR → ECOSISTEMA.</strong> Clima = largo plazo; sin cifras inventadas.",
    },
    {
        "n": 37,
        "slug": "habitos-sostenibles-consumo-residuos-respeto-al-medio",
        "eyebrow": "Lección 37 · UD F · Ecología y sostenibilidad",
        "title_html": "<em>Hábitos sostenibles</em> (consumo, residuos, respeto al medio)",
        "title_plain": "Hábitos sostenibles (consumo, residuos, respeto al medio)",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque F",
        "curiosidad_t": "3R: Reducir > Reutilizar > Reciclar",
        "curiosidad": (
            "Los <strong>hábitos sostenibles</strong> son acciones diarias que cuidan recursos. "
            "Orden de las 3R: primero <strong>reducir</strong>, luego reutilizar, después reciclar."
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            "Aplicar las <strong>3R</strong>: reducir, reutilizar, reciclar (en ese orden).",
            "Relacionar consumo responsable y gestión de residuos.",
            "Proponer gestos de respeto al medio en el centro y en casa.",
            "Usar 3R: Reducir > Reutilizar > Reciclar.",
            "Cuidar agua y energía además de separar residuos.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Hábitos sostenibles</strong> = acciones diarias que cuidan recursos y entorno.</p>
    <ol>
      <li><strong>Reducir</strong> (lo más importante): menos consumo innecesario.</li>
      <li><strong>Reutilizar:</strong> segunda vida a objetos.</li>
      <li><strong>Reciclar:</strong> separar residuos (orgánico, papel, envases, vidrio…).</li>
    </ol>
    <p>También: cuidar agua y energía, no abandonar basura, respetar seres vivos y espacios naturales.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «3R: Reducir > Reutilizar > Reciclar».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "En el instituto y en pueblos/ciudades de CyL: contenedores bien usados.",
            "Huerto escolar y caminos sin basura.",
            "Compra con menos plástico = reducir.",
            "Reutilizar ≠ reciclar: otra vida vs procesar material.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Hábitos sostenibles", "l37-habitos-sostenibles.html"),
        ],
        "reto_t": "3R en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta "
            "lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L37",
        "cierre": "<strong>3R: Reducir > Reutilizar > Reciclar.</strong> Reducir es la R más importante.",
    },
    {
        "n": 38,
        "slug": "one-health-salud-ambiental-humana-y-de-otros-seres-vivos",
        "eyebrow": "Lección 38 · UD F · Ecología y sostenibilidad",
        "title_html": "<em>One Health</em>: salud ambiental, humana y de otros seres vivos",
        "title_plain": "One Health: salud ambiental, humana y de otros seres vivos",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · bloque F",
        "curiosidad_t": "3 SALUDES unidas",
        "curiosidad": (
            "<strong>One Health (una sola salud)</strong>: la salud de las <strong>personas</strong>, "
            "de <strong>otros seres vivos</strong> y del <strong>medio ambiente</strong> están conectadas."
        ),
        "curiosidad_fig": "olla.svg",
        "objetivos": [
            "Explicar One Health con el diagrama de tres círculos.",
            "Dar un ejemplo que una persona, animal y entorno.",
            "Relacionar higiene, mascotas, agua limpia y ecosistemas.",
            "Usar 3 SALUDES unidas (persona · animal · entorno).",
            "Ver la salud como un sistema, no como magia.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>One Health (una sola salud):</strong> la salud de las <strong>personas</strong>, de <strong>otros seres vivos</strong> y del <strong>medio ambiente</strong> están conectadas.</p>
    <p>Ejemplos sencillos:</p>
    <ul>
      <li>Agua contaminada → enferma gente y animales.</li>
      <li>Cuidar mascotas + higiene → menos riesgos compartidos.</li>
      <li>Ecosistema sano → mejor aire, agua y alimentos.</li>
    </ul>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «3 SALUDES unidas (persona · animal · entorno)».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "En CyL: ríos limpios, ganado, mascotas y pueblos/ciudades comparten aire y agua.",
            "Cuidar el entorno es también cuidarnos.",
            "Agua sucia conecta salud humana y animal.",
            "One Health no ignora el medio: es una de las tres saludes.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("One Health", "l38-one-health.html"),
        ],
        "reto_t": "3 SALUDES en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta "
            "lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L38",
        "cierre": "<strong>3 SALUDES unidas (persona · animal · entorno).</strong> One Health = sistema conectado.",
    },
    {
        "n": 39,
        "slug": "proyecto-integrador-del-curso-ciencia-entorno-cyl",
        "eyebrow": "Lección 39 · UD F · Cierre",
        "title_html": "Proyecto integrador del curso (<em>ciencia + entorno CyL</em>)",
        "title_plain": "Proyecto integrador del curso (ciencia + entorno CyL)",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · cierre A–F",
        "curiosidad_t": "PREGUNTA → OBSERVA → MODELA → CUENTA",
        "curiosidad": (
            "Cerramos el curso con un <strong>mini-proyecto</strong> local: pregunta clara, "
            "observar evidencias, modelar (esquema/tabla) y comunicar — sin inventar datos."
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            "Elegir una pregunta local (CyL / barrio / centro).",
            "Seguir pasos: preguntar → observar → modelar → comunicar.",
            "Usar vocabulario científico del curso (A–F).",
            "Usar PREGUNTA → OBSERVA → MODELA → CUENTA.",
            "Registrar lo que ves y citar fuentes si usas web.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p>Cerramos el curso con un <strong>mini-proyecto</strong>:</p>
    <ol>
      <li><strong>Pregunta</strong> clara y local</li>
      <li><strong>Observar</strong> y reunir evidencias (notas, fotos, medidas sencillas)</li>
      <li><strong>Modelo</strong> (esquema, mapa, tabla)</li>
      <li><strong>Comunicar</strong> (informe corto oral o escrito)</li>
    </ol>
    <p>Ideas CyL: dehesa/pinar, río, parque, residuos del centro, roca local, One Health en casa.</p>
    <p>No inventes datos: registra lo que ves y cita fuentes si usas web.</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «PREGUNTA → OBSERVA → MODELA → CUENTA».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Elige un lugar real cerca de ti en CyL (patio, parque, ribera, monte).",
            "Aplica saberes A–F: método, geosfera, agua, célula, seres vivos, ecología.",
            "Ideas: dehesa, río, residuos del centro, roca local, One Health.",
            "Comunica con rigor: evidencias, no inventos.",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Proyecto integrador CyL", "l39-proyecto-integrador-cyl.html"),
        ],
        "reto_t": "Cuenta tu proyecto en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta "
            "lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L39",
        "cierre": "<strong>PREGUNTA → OBSERVA → MODELA → CUENTA.</strong> Proyecto local, evidencias reales.",
    },
    {
        "n": 40,
        "slug": "autoevaluacion-portfolio-y-habitos-de-trabajo-cientifico",
        "eyebrow": "Lección 40 · UD F · Cierre",
        "title_html": "<em>Autoevaluación</em>, portfolio y hábitos de trabajo científico",
        "title_plain": "Autoevaluación, portfolio y hábitos de trabajo científico",
        "meta": "1º ESO Biología y Geología · CyL Decreto 39/2022 · cierre",
        "curiosidad_t": "SÉ · GUARDO · MEJORO",
        "curiosidad": (
            "Cierra las <strong>40 lecciones</strong> de ByG 1º ESO: autoevaluación honesta, "
            "portfolio de evidencias y hábitos científicos (curiosidad, rigor, honestidad, respeto, constancia)."
        ),
        "curiosidad_fig": "ticket.svg",
        "objetivos": [
            "Completar una autoevaluación honesta del curso.",
            "Organizar el <strong>portfolio</strong> (evidencias de aprendizaje).",
            "Listar hábitos científicos a mantener el próximo curso.",
            "Usar SÉ · GUARDO · MEJORO.",
            "Guardar el portfolio para el curso siguiente.",
        ],
        "cuerpo": """
    <h2>Explicación</h2>
    <p><strong>Autoevaluación:</strong> ¿qué sé hacer solo? Marca con honestidad.</p>
    <p><strong>Portfolio:</strong> carpeta con esquemas, fotos de prácticas, glosarios, retos, proyecto L39 y esta checklist.</p>
    <p><strong>Hábitos científicos:</strong> curiosidad, rigor, honestidad con los datos, respeto y constancia.</p>
    <p>Esto cierra las <strong>40 lecciones</strong> de ByG 1º ESO (CyL).</p>
    <div class="tarjeta">
      <p style="margin:0"><strong>Mnemónico:</strong> «SÉ · GUARDO · MEJORO».</p>
    </div>
""",
        "vida_t": "Castilla y León",
        "vida": [
            "Tu portfolio es la prueba de lo aprendido en el instituto y en salidas por CyL.",
            "Guárdalo para el curso siguiente.",
            "Autoevaluar no es copiar del solucionario: es honestidad.",
            "Curso completo: 40 lecciones (A–F + cierre).",
        ],
        "vida_fig": "mapa.svg",
        "widgets": [
            ("Autoevaluación y portfolio", "l40-autoevaluacion-portfolio-habitos.html"),
        ],
        "reto_t": "SÉ · GUARDO · MEJORO en 1 minuto",
        "reto": (
            "Explica a un compañero, con el dibujo del interactivo, la idea más importante de esta "
            "lección en 1 minuto."
        ),
        "reto_id": "1eso-byg-L40",
        "cierre": "<strong>SÉ · GUARDO · MEJORO.</strong> Fin del curso ByG 1º ESO: 40/40.",
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
      <strong>Pack completo L01–L{AVAILABLE:02d}</strong> (UD A–F + cierre: proyecto científico, geosfera, atmósfera/hidrosfera, célula, seres vivos, ecosistemas y sostenibilidad) en shell HTML.
      Curso <strong>cerrado</strong> ({TOTAL}/{TOTAL} lecciones disponibles).
      <strong>ZIP offline</strong> (sin instalar: descomprime y abre <code>ABRE-AQUI.html</code>) en <a href="{descargas}">Descargas</a>.
    </p>
    <a class="hub-cta" href="{lec_prefix}{l01}">Abrir lección 01 →</a>
  </section>

  <p class="hub-nota">Índice del temario completo ({TOTAL} lecciones). Todas disponibles como <code>leccion-NN-….html</code> (alias <code>leccion-NN.html</code>). Pack completo — sin «próximamente».</p>

  <ol class="hub-lista">
{chr(10).join(items)}
  </ol>

  <p class="hub-pie-nota">
    Educación obligatoria · currículo oficial CyL (Decreto 39/2022). Distinto del pack Profesor (multi-materia).
    Interactivos L01–L{AVAILABLE:02d}: método, geosfera, atmósfera/hidrosfera, célula, seres vivos, ecosistemas y sostenibilidad (UD A–F + cierre).
  </p>

  <footer class="leccion-pie">
    <strong>Les vencimos</strong> · 1º ESO Biología y Geología · pack completo L01–L{AVAILABLE:02d}/{TOTAL}
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

    text = text.replace(
        "Oficial CyL · Decreto 39/2022 · en construcción (40 lecciones)",
        "Oficial CyL · Decreto 39/2022 · pack completo (40 lecciones)",
    )
    text = re.sub(
        r"L01–L\d{2} disponibles \(UD A–F:.*?\); curso en construcción \(40 lecciones previstas\)",
        f"Pack completo L01–L{AVAILABLE:02d} (UD A–F + cierre: proyecto científico, geosfera, atmósfera/hidrosfera, célula, seres vivos, ecosistemas y sostenibilidad). Curso cerrado ({TOTAL}/{TOTAL})",
        text,
        count=1,
    )

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
        f"            Pack completo L01–L{AVAILABLE:02d} (UD A–F + cierre: proyecto científico, geosfera, atmósfera/hidrosfera, célula, seres vivos, ecosistemas y sostenibilidad). "
        f"Curso cerrado ({TOTAL}/{TOTAL}). Sin nube ni servidor.\n"
        f"            Distinto del pack Profesor."
    )

    if "1eso-biologia-geologia-offline.zip" in text:
        text2, n = re.subn(
            r"(<h2>1º ESO Biología y Geología</h2>\s*"
            r'<p class="kicker">Oficial CyL · Decreto 39/2022 · pack completo \(40 lecciones\)</p>\s*'
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
            f"L01–L{AVAILABLE:02d} disponibles (UD A–F: proyecto científico, geosfera, atmósfera/hidrosfera, célula, seres vivos, ecosistemas); curso en construcción ({TOTAL} lecciones previstas)",
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
            <p class="kicker">Oficial CyL · Decreto 39/2022 · pack completo (40 lecciones)</p>
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
Este pack trae el curso **completo**: lecciones **01–{AVAILABLE:02d}/{TOTAL}** (UD A–F + cierre: proyecto científico, geosfera, atmósfera/hidrosfera, célula, seres vivos, ecosistemas y sostenibilidad) en HTML plano (shell + interactivos embebidos).
**Pack completo** — sin lecciones «próximamente».

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
    <p class="meta-leccion">Pack completo L01–L{AVAILABLE:02d}/{TOTAL} · curso cerrado</p>
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
  <p class="hub-nota">Curso completo ({TOTAL}/{TOTAL}). Usa siempre este índice.</p>
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
