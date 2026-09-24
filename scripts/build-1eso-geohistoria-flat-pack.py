#!/usr/bin/env python3
"""Build online shell + flat offline pack for 1º ESO Geografía e Historia (L01–L36)."""
from __future__ import annotations

import html
import json
import pathlib
import re
import shutil
import unicodedata
import zipfile

REPO = pathlib.Path("/workspace/lesvencimos")
COURSE_DIR = REPO / "profesor/1eso-geografia-historia"
LEC = COURSE_DIR / "lecciones"
PLANTILLA = REPO / "profesor/_plantilla-leccion"
HUB = COURSE_DIR / "1eso-geografia-historia.html"
DESCARGAS = REPO / "descargas.html"
INDEX = REPO / "index.html"
PACK_DIR = REPO / "downloads/_build-1eso-geohistoria-flat"
ZIP_PATH = REPO / "downloads/1eso-geografia-historia-offline.zip"
COURSE_ICONS = COURSE_DIR / "icons"
BRAND_ICONS = REPO / "brand/favicon"
TOTAL = 36
AVAILABLE = 36

COURSE_NAME = "1º ESO Geografía e Historia"
COURSE_SHORT = "1º ESO GeoHistoria"
ZIP_FOLDER = "1eso-geografia-historia-offline"

# UD ranges: A = L01–L10, B = L11–L24, C = L25–L36
UD_BLOCKS = {
    "A": ("UD A · Retos del mundo actual", "bloque A"),
    "B": ("UD B · Sociedades y territorios", "bloque B"),
    "C": ("UD C · Compromiso cívico", "bloque C"),
}


def ud_for_lesson(n: int) -> str:
    if 1 <= n <= 10:
        return "A"
    if 11 <= n <= 24:
        return "B"
    if 25 <= n <= 36:
        return "C"
    raise ValueError(f"lesson out of range: {n}")


def eyebrow_ud(n: int) -> str:
    return UD_BLOCKS[ud_for_lesson(n)][0]


def meta_for_lesson(n: int) -> str:
    bloque = UD_BLOCKS[ud_for_lesson(n)][1]
    return f"1º ESO Geografía e Historia · CyL Decreto 39/2022 · {bloque}"


def pack_ud_blurb(*, short: bool = False) -> str:
    """Human copy for which UDs the current AVAILABLE pack covers."""
    if AVAILABLE >= TOTAL:
        if short:
            return "UD A + UD B + UD C · Compromiso cívico"
        return (
            "UD A · Retos del mundo actual + UD B · Sociedades y territorios "
            "+ UD C · Compromiso cívico"
        )
    # Partial: only A+B while C still pending
    if short:
        return "UD A + UD B"
    return "UD A · Retos del mundo actual + UD B · Sociedades y territorios"


def pack_interactivos_blurb() -> str:
    base = (
        "mapas, relieve y clima (UD A); pensamiento histórico, Prehistoria, "
        "civilizaciones, Grecia–Roma y patrimonio CyL (UD B)"
    )
    if AVAILABLE >= TOTAL:
        return (
            base
            + "; compromiso cívico, derechos, convivencia, atlas y proyectos (UD C)"
        )
    return base


# Full temario titles (curso completo L01–L36) — from TEMARIO.md
TEMARIO = [
    "Orientarse en el espacio: mapas, escalas y TIG",
    "Continentes, océanos, mares y ríos del mundo",
    "Europa, España y Castilla y León en el mapa (relieve y ríos)",
    "Fondos marinos y formas de relieve",
    "Clima: elementos, factores y gráficos meteorológicos",
    "Emergencia climática: riesgos, vulnerabilidad y resiliencia",
    "Zonas bioclimáticas y biodiversidad planetaria",
    "Ecosistemas, patrimonio natural y huella humana",
    "Buscar y leer información: TIC, redes seguras y pensamiento crítico",
    "Ciencias sociales: objetivos, términos y plataformas digitales",
    "Pensar como geógrafo y como historiador",
    "Fuentes históricas y arqueológicas; museos, archivos y bibliotecas",
    "Origen del ser humano y grandes migraciones",
    "Paleolítico: supervivencia y primeras culturas",
    "Neolítico y Edad de los Metales: territorio, desigualdad y poder",
    "Nacimiento de las civilizaciones y rutas comerciales",
    "Arte, cultura y patrimonio en las primeras civilizaciones",
    "Grecia: de las polis a Alejandro Magno",
    "Roma: monarquía, república e imperio; Mediterráneo",
    "Religión, poder e identidades en el mundo antiguo",
    "Personas invisibilizadas: mujeres, esclavos y extranjeros",
    "Prehistoria en la Península: Atapuerca y arte prehistórico",
    "Pueblos prerromanos e Hispania romana",
    "Romanización y patrimonio en Castilla y León",
    "Conciencia ambiental: cuidar el planeta y los seres vivos",
    "Alteridad: respeto y rechazo a la discriminación",
    "Dignidad humana y derechos del niño",
    "Igualdad de género: conductas no sexistas",
    "Convivencia democrática y participación ciudadana",
    "Ciclos vitales, tiempo libre y hábitos de consumo (antes y ahora)",
    "Seguridad vial y espacio público sostenible",
    "Línea del tiempo del curso: de la Prehistoria a Roma (síntesis)",
    "Atlas interactivo CyL–España–Europa–mundo (repaso geográfico)",
    "Mini-investigación con fuentes (proyecto guiado)",
    "Proyecto integrador: paisaje local + historia cercana",
    "Autoevaluación, portfolio y hábitos de ciudadanía",
]

TITLE_HTML = {
    1: "Orientarse en el espacio: <em>mapas</em>, escalas y TIG",
    2: "<em>Continentes</em>, océanos, mares y ríos del mundo",
    3: "Europa, España y <em>Castilla y León</em> en el mapa (relieve y ríos)",
    4: "Fondos marinos y <em>formas de relieve</em>",
    5: "Clima: elementos, factores y <em>gráficos</em> meteorológicos",
    6: "<em>Emergencia climática</em>: riesgos, vulnerabilidad y resiliencia",
    7: "Zonas bioclimáticas y <em>biodiversidad</em> planetaria",
    8: "Ecosistemas, patrimonio natural y <em>huella humana</em>",
    9: "Buscar y leer información: TIC, redes seguras y <em>pensamiento crítico</em>",
    10: "Ciencias sociales: objetivos, términos y <em>plataformas digitales</em>",
    11: "Pensar como <em>geógrafo</em> y como <em>historiador</em>",
    12: "Fuentes históricas; <em>museos</em>, archivos y bibliotecas",
    13: "Origen del ser humano y <em>grandes migraciones</em>",
    14: "<em>Paleolítico</em>: supervivencia y primeras culturas",
    15: "<em>Neolítico</em> y Edad de los Metales: territorio, desigualdad y poder",
    16: "Nacimiento de las <em>civilizaciones</em> y rutas comerciales",
    17: "Arte, cultura y <em>patrimonio</em> en las primeras civilizaciones",
    18: "<em>Grecia</em>: de las polis a Alejandro Magno",
    19: "<em>Roma</em>: monarquía, república e imperio; Mediterráneo",
    20: "Religión, poder e <em>identidades</em> en el mundo antiguo",
    21: "Personas <em>invisibilizadas</em>: mujeres, esclavos y extranjeros",
    22: "Prehistoria en la Península: <em>Atapuerca</em> y arte prehistórico",
    23: "Pueblos prerromanos e <em>Hispania</em> romana",
    24: "<em>Romanización</em> y patrimonio en Castilla y León",
    25: "Conciencia ambiental: <em>cuidar</em> el planeta y los seres vivos",
    26: "<em>Alteridad</em>: respeto y rechazo a la discriminación",
    27: "Dignidad humana y <em>derechos del niño</em>",
    28: "Igualdad de género: conductas <em>no sexistas</em>",
    29: "Convivencia democrática y <em>participación</em> ciudadana",
    30: "Ciclos vitales, tiempo libre y <em>hábitos de consumo</em>",
    31: "Seguridad vial y espacio público <em>sostenible</em>",
    32: "Línea del tiempo: de la Prehistoria a <em>Roma</em>",
    33: "Atlas interactivo <em>CyL–España–Europa–mundo</em>",
    34: "Mini-investigación con <em>fuentes</em>",
    35: "Proyecto integrador: <em>paisaje</em> local + historia cercana",
    36: "Autoevaluación, <em>portfolio</em> y hábitos de ciudadanía",

}

WIDGETS = {
    1: ("Laboratorio · mapas, escalas y TIG", "l01-orientarse-mapas-escalas-tig.html"),
    2: ("Laboratorio · continentes, océanos, mares y ríos", "l02-continentes-oceanos-mares-rios.html"),
    3: ("Laboratorio · Europa, España y CyL (relieve y ríos)", "l03-europa-espana-cyl-relieve-rios.html"),
    4: ("Laboratorio · fondos marinos y relieve", "l04-fondos-marinos-formas-relieve.html"),
    5: ("Laboratorio · clima y gráficos meteorológicos", "l05-clima-elementos-factores-graficos.html"),
    6: ("Laboratorio · emergencia climática y resiliencia", "l06-emergencia-climatica-riesgos-resiliencia.html"),
    7: ("Laboratorio · zonas bioclimáticas y biodiversidad", "l07-zonas-bioclimaticas-biodiversidad.html"),
    8: ("Laboratorio · ecosistemas, patrimonio y huella", "l08-ecosistemas-patrimonio-huella-humana.html"),
    9: ("Laboratorio · TIC, redes seguras y lectura crítica", "l09-tic-redes-seguras-lectura-critica.html"),
    10: ("Laboratorio · ciencias sociales: objetivos y términos", "l10-ciencias-sociales-objetivos-terminos.html"),
    11: ("Laboratorio · pensar como geógrafo e historiador", "l11-pensar-geografo-historiador.html"),
    12: ("Laboratorio · fuentes, museos, archivos y bibliotecas", "l12-fuentes-museos-archivos-bibliotecas.html"),
    13: ("Laboratorio · origen humano y migraciones", "l13-origen-humano-migraciones.html"),
    14: ("Laboratorio · Paleolítico: supervivencia y culturas", "l14-paleolitico-supervivencia-culturas.html"),
    15: ("Laboratorio · Neolítico y Edad de los Metales", "l15-neolitico-edad-metales.html"),
    16: ("Laboratorio · civilizaciones y rutas comerciales", "l16-civilizaciones-rutas-comerciales.html"),
    17: ("Laboratorio · arte, cultura y patrimonio", "l17-arte-cultura-patrimonio-civilizaciones.html"),
    18: ("Laboratorio · Grecia: polis y Alejandro", "l18-grecia-polis-alejandro.html"),
    19: ("Laboratorio · Roma: monarquía, república e imperio", "l19-roma-monarquia-republica-imperio.html"),
    20: ("Laboratorio · religión, poder e identidades", "l20-religion-poder-identidades-antiguedad.html"),
    21: ("Laboratorio · personas invisibilizadas", "l21-invisibilizados-mujeres-esclavos-extranjeros.html"),
    22: ("Laboratorio · Prehistoria peninsular y Atapuerca", "l22-prehistoria-peninsula-atapuerca.html"),
    23: ("Laboratorio · prerromanos e Hispania romana", "l23-pueblos-prerromanos-hispania-romana.html"),
    24: ("Laboratorio · romanización y patrimonio CyL", "l24-romanizacion-patrimonio-cyl.html"),
    25: ("Laboratorio · conciencia ambiental", "l25-conciencia-ambiental-planeta-seres-vivos.html"),
    26: ("Laboratorio · alteridad", "l26-alteridad-respeto-no-discriminacion.html"),
    27: ("Laboratorio · dignidad y derechos del niño", "l27-dignidad-humana-derechos-nino.html"),
    28: ("Laboratorio · igualdad de género", "l28-igualdad-genero-conductas-no-sexistas.html"),
    29: ("Laboratorio · convivencia democrática", "l29-convivencia-democratica-participacion.html"),
    30: ("Laboratorio · ciclos vitales y consumo", "l30-ciclos-vitales-tiempo-libre-consumo.html"),
    31: ("Laboratorio · seguridad vial", "l31-seguridad-vial-espacio-publico.html"),
    32: ("Laboratorio · línea del tiempo del curso", "l32-linea-tiempo-prehistoria-roma.html"),
    33: ("Laboratorio · atlas CyL–España–Europa–mundo", "l33-atlas-interactivo-cyl-espana-europa-mundo.html"),
    34: ("Laboratorio · mini-investigación", "l34-mini-investigacion-fuentes.html"),
    35: ("Laboratorio · proyecto paisaje + historia", "l35-proyecto-integrador-paisaje-historia.html"),
    36: ("Laboratorio · autoevaluación y portfolio", "l36-autoevaluacion-portfolio-ciudadania.html"),

}

# Short curiosidades (MD sources lack a dedicated block)
CURIOSIDADES = {
    1: (
        "La rosa de los vientos",
        "En la Edad Media, las cartas portulanas dibujaban una <strong>rosa de los vientos</strong> "
        "para orientar a los navegantes. Hoy tu móvil hace lo mismo con satélites, pero la pregunta "
        "sigue siendo la misma: ¿dónde estoy y hacia dónde voy?",
        "mapa.svg",
    ),
    2: (
        "Un planisferio, muchas historias",
        "Durante siglos, cada cultura colocó el «centro» del mundo en un sitio distinto. "
        "Un planisferio escolar no es la única vista posible: es una <strong>convención útil</strong> "
        "para situar continentes, océanos y grandes ríos.",
        "mapa.svg",
    ),
    3: (
        "La Meseta vista desde el aire",
        "Castilla y León ocupa buena parte de la <strong>Meseta Norte</strong>. Desde un satélite "
        "se ve el contraste entre páramos, valles y la curva de la Cordillera Cantábrica: geografía "
        "que explica clima, ríos y caminos históricos.",
        "mapa.svg",
    ),
    4: (
        "Montañas bajo el mar",
        "El relieve no termina en la playa. Dorsales, fosas y plataformas continentales "
        "dibujan un paisaje oculto. Sin él no entenderías terremotos, mares ni la forma de las costas.",
        "fuego.svg",
    ),
    5: (
        "Del termómetro al climograma",
        "AEMET y los observatorios escolares miden lluvia y temperatura todos los días. "
        "Cuando juntas 12 meses en un <strong>climograma</strong>, dejas de hablar del «tiempo de hoy» "
        "y empiezas a hablar de <strong>clima</strong>.",
        "ticket.svg",
    ),
    6: (
        "Resiliencia no es magia",
        "Tras una riada o una ola de calor, las comunidades que mejor se recuperan no son las que "
        "ignoran el riesgo: son las que lo <strong>miden</strong>, lo explican y preparan planes. "
        "Eso es resiliencia: ciencia + cuidado colectivo.",
        "olla.svg",
    ),
    7: (
        "Biomas en un mapa",
        "Del desierto al bosque boreal, las <strong>zonas bioclimáticas</strong> agrupan climas y seres vivos. "
        "No son cajas cerradas, pero ayudan a ver por qué no hay la misma biodiversidad en todos los lugares.",
        "mapa.svg",
    ),
    8: (
        "Patrimonio que se pisa",
        "Un robledal, una laguna o un parque natural de CyL son <strong>patrimonio natural</strong>. "
        "La huella humana —carreteras, cultivos, basura— deja marcas que el geógrafo mide y el ciudadano "
        "puede reducir.",
        "fuego.svg",
    ),
    9: (
        "Antes de compartir, contrastar",
        "En el siglo XV ya circulaban mapas erróneos que se copiaban sin comprobar. "
        "Hoy pasa lo mismo en chats y redes: <strong>fuente + fecha + contraste</strong> siguen siendo "
        "el antídoto del pensamiento crítico.",
        "ticket.svg",
    ),
    10: (
        "Gafas para leer el mundo",
        "Las Ciencias Sociales no son un cajón de datos sueltos. Son <strong>gafas</strong> para leer "
        "el espacio, el tiempo y la convivencia: mapa, fuente, término preciso y plataforma fiable.",
        "mapa.svg",
    ),
    11: (
        "Dos gafas, un mapa",
        "El geógrafo pregunta <strong>dónde</strong>; el historiador, <strong>cuándo y por qué</strong>. "
        "Juntas, esas gafas convierten un paisaje o una noticia en una lección de Ciencias Sociales.",
        "mapa.svg",
    ),
    12: (
        "El archivo no es un almacén muerto",
        "Una carta, una moneda o un hueso en un museo son <strong>fuentes</strong>. Sin archivo, biblioteca "
        "y museo, el pasado se vuelve rumor: el patrimonio es memoria compartida.",
        "ticket.svg",
    ),
    13: (
        "De África al mundo",
        "El modelo científico actual sitúa el origen de <strong>Homo sapiens</strong> en África. "
        "Las migraciones duraron decenas de miles de años: poblar la Tierra no fue un viaje de fin de semana.",
        "mapa.svg",
    ),
    14: (
        "Piedra, fuego y cooperación",
        "En el Paleolítico no había ciudades: había grupos que cazaban, recolectaban y tallaban piedra. "
        "El <strong>arte rupestre</strong> ya era cultura, no solo decoración de cueva.",
        "fuego.svg",
    ),
    15: (
        "Cuando la tierra se guarda",
        "Con la agricultura llegan aldeas, almacenes… y a menudo <strong>desigualdad</strong>. "
        "Controlar cosechas y metales cambia el poder mucho antes de que existan «países» modernos.",
        "olla.svg",
    ),
    16: (
        "Rutas antes de carreteras",
        "Las primeras civilizaciones no vivían aisladas: grano, metales y textiles viajaban por "
        "<strong>rutas</strong> terrestres y marítimas. El Mediterráneo ya era un mar de conexiones.",
        "mapa.svg",
    ),
    17: (
        "Arte que manda mensaje",
        "Templo, palacio o tumba no eran solo edificios bonitos: comunicaban <strong>poder</strong> y "
        "creencias. Por eso hoy hablamos de patrimonio cultural que hay que proteger.",
        "ticket.svg",
    ),
    18: (
        "Muchas polis, no un solo país",
        "La Grecia antigua era un mosaico de <strong>polis</strong> (ciudades-Estado). Atenas y Esparta "
        "fueron famosas, pero Alejandro Magno llevó ideas helenísticas mucho más lejos.",
        "mapa.svg",
    ),
    19: (
        "753 a.C.: tradición, no laboratorio",
        "La fundación de Roma en <strong>753 a.C.</strong> es fecha legendaria escolar. Lo histórico "
        "sí es el paso de monarquía a república e imperio… y el Mediterráneo como <em>mare nostrum</em>.",
        "fuego.svg",
    ),
    20: (
        "Dioses en la plaza",
        "En el mundo antiguo, religión e identidad no vivían solo en privado: templos, fiestas y "
        "cultos públicos reforzaban la <strong>comunidad</strong> y, a menudo, el poder.",
        "olla.svg",
    ),
    21: (
        "Más que reyes y batallas",
        "Si solo cuentas emperadores, <strong>invisibilizas</strong> a mujeres, esclavos y extranjeros. "
        "La Historia completa incluye a quienes casi no dejan su nombre en las fuentes.",
        "ticket.svg",
    ),
    22: (
        "Atapuerca en el mapa de CyL",
        "La sierra de <strong>Atapuerca</strong> (Burgos) es UNESCO: fósiles y herramientas de muchas "
        "épocas. Las dataciones se revisan; no son un DNI grabado en piedra.",
        "mapa.svg",
    ),
    23: (
        "Hispania no nació en un día",
        "Íberos, celtíberos y otros pueblos vivían en la Península antes de Roma. La conquista "
        "desde <strong>218 a.C.</strong> fue larga: Numancia (Soria) es solo un capítulo.",
        "fuego.svg",
    ),
    24: (
        "Roma bajo tus pies en CyL",
        "Acueducto de Segovia, León campamental, Clunia, Las Médulas… La <strong>romanización</strong> "
        "dejó vías, latín y ciudades; no borró del todo lo anterior ni fue homogénea.",
        "mapa.svg",
    ),
    25: ("3R + seres vivos", "Cuidar el planeta es también cuidar <strong>seres vivos</strong>: reducir, reutilizar, reciclar y respetar hábitats. En CyL, espacios naturales se consultan en fuentes oficiales.", "mapa.svg"),
    26: ("El otro también cuenta", "<strong>Alteridad</strong> es respetar al otro. Diferencia enriquece; discriminación y segregación excluyen. En el patio: incluir, no burlar.", "mapa.svg"),
    27: ("CDN 1989", "La <strong>Convención sobre los Derechos del Niño</strong> (ONU, 1989) reconoce derechos a menores de 18. Dignidad = valor de toda persona. Sin inventar artículos.", "mapa.svg"),
    28: ("Igualdad, no clones", "<strong>Igualdad de género</strong>: mismos derechos y oportunidades. Conductas no sexistas en casa, patio y aula. El talento no tiene género.", "mapa.svg"),
    29: ("Participar en lo común", "Democracia = normas justas + diálogo + participación. A tu escala: aula, centro, barrio. Proyectos comunitarios cuidan el bien común.", "mapa.svg"),
    30: ("Antes / ahora con matices", "Ciclo vital y ocio cambian. Compara <strong>antes/ahora</strong> con fuentes; no idealices el pasado ni consumas a ciegas.", "mapa.svg"),
    31: ("Mirar · parar · cruzar", "Seguridad vial y <strong>espacio público</strong> de todos. Movilidad sostenible (andar, bici, bus) según el contexto de cada pueblo.", "mapa.svg"),
    32: ("Pa–Ne–Me–Gre–Ro", "Síntesis: Paleolítico → Neolítico → Metales → Grecia → Roma → Hispania/CyL. <strong>753 a.C.</strong> = tradición; fechas antiguas = rangos.", "mapa.svg"),
    33: ("MU–EU–ES–CyL", "Atlas de escalas: mundo → Europa → España → <strong>CyL</strong> (Meseta, Duero). SVG didáctico, no carta oficial.", "mapa.svg"),
    34: ("Pregunta · busca · contrasta · cita", "Mini-investigación: fuentes primarias/secundarias, contrastar ≥2 y <strong>citar</strong>. Si no consta, dilo.", "mapa.svg"),
    35: ("Paisaje + historia", "Proyecto: croquis del lugar + 3 rasgos de paisaje + una huella histórica cercana con fuentes. Sin inventar leyendas.", "mapa.svg"),
    36: ("Sé · portfolio · hábitos", "Cierre: autoevaluación honesta, portfolio (3–5 evidencias) y 3 <strong>hábitos cívicos</strong>. Curso 36/36.", "mapa.svg"),

}

FIG_CYCLE = ("mapa.svg", "fuego.svg", "ticket.svg", "olla.svg")


def slugify(title: str, max_len: int = 72) -> str:
    s = unicodedata.normalize("NFKD", title)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if len(s) > max_len:
        s = s[:max_len].rstrip("-")
    return s or "leccion"


def md_inline(text: str) -> str:
    """Convert light markdown inline marks; leave raw HTML alone if already present."""
    text = text.strip()
    # Protect code spans
    codes: list[str] = []

    def _code(m: re.Match[str]) -> str:
        codes.append(m.group(1))
        return f"\x00C{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", _code, text)
    # Links [t](url) — keep label; drop local md links to widgets
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Bold / italic
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    # Escape leftover < that aren't tags we introduced — skip; content is trusted course MD
    for i, c in enumerate(codes):
        text = text.replace(f"\x00C{i}\x00", f"<code>{html.escape(c)}</code>")
    return text


def _split_table_row(line: str) -> list[str]:
    line = line.strip().strip("|")
    return [c.strip() for c in line.split("|")]


def md_blocks_to_html(md: str) -> str:
    """Minimal markdown → HTML for lesson cuerpo (headings, lists, tables, quotes, p)."""
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped == "---":
            i += 1
            continue
        if stripped.startswith("### "):
            out.append(f"    <h3>{md_inline(stripped[4:])}</h3>")
            i += 1
            continue
        if stripped.startswith("## "):
            out.append(f"    <h2>{md_inline(stripped[3:])}</h2>")
            i += 1
            continue
        if stripped.startswith("> "):
            quote = [stripped[2:]]
            i += 1
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip("> ").rstrip())
                i += 1
            out.append(
                '    <div class="tarjeta"><p style="margin:0">'
                + md_inline(" ".join(quote))
                + "</p></div>"
            )
            continue
        if "|" in stripped and stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(_split_table_row(lines[i]))
                i += 1
            if len(rows) >= 2:
                # skip separator row
                body_start = 1
                if all(re.match(r"^:?-+:?$", c or "") for c in rows[1]):
                    body_start = 2
                thead = "".join(f"<th>{md_inline(c)}</th>" for c in rows[0])
                body = []
                for r in rows[body_start:]:
                    body.append("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>")
                out.append(
                    "    <div class=\"tarjeta\" style=\"overflow-x:auto\">"
                    f"<table style=\"width:100%;border-collapse:collapse;font-size:0.95rem\">"
                    f"<thead><tr>{thead}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"
                )
            continue
        if re.match(r"^[-*] ", stripped) or re.match(r"^\d+\.\s", stripped):
            ordered = bool(re.match(r"^\d+\.\s", stripped))
            items = []
            while i < len(lines):
                s = lines[i].strip()
                if ordered:
                    m = re.match(r"^\d+\.\s+(.*)$", s)
                else:
                    m = re.match(r"^[-*]\s+(.*)$", s)
                if not m:
                    break
                items.append(f"      <li>{md_inline(m.group(1))}</li>")
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"    <{tag}>\n" + "\n".join(items) + f"\n    </{tag}>")
            continue
        # paragraph: gather until blank
        para = [stripped]
        i += 1
        while i < len(lines):
            s = lines[i].strip()
            if (
                not s
                or s == "---"
                or s.startswith("#")
                or s.startswith(">")
                or s.startswith("|")
                or re.match(r"^[-*] ", s)
                or re.match(r"^\d+\.\s", s)
            ):
                break
            para.append(s)
            i += 1
        out.append(f"    <p>{md_inline(' '.join(para))}</p>")
    return "\n".join(out) + ("\n" if out else "")


def extract_section(md: str, *title_prefixes: str) -> str:
    """Return body of first ## section whose title starts with any prefix."""
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.M)
    matches = list(pattern.finditer(md))
    for idx, m in enumerate(matches):
        title = m.group(1).strip()
        if any(title.lower().startswith(p.lower()) for p in title_prefixes):
            start = m.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(md)
            body = md[start:end]
            body = re.sub(r"^\n+|\n+$", "", body)
            body = re.sub(r"\n---\s*$", "", body).strip()
            return body
    return ""


def parse_objetivos(body: str) -> list[str]:
    items = []
    for m in re.finditer(r"^\d+\.\s+(.+)$", body, re.M):
        items.append(md_inline(m.group(1).strip()))
    return items


def parse_vida(body: str) -> list[str]:
    items = []
    for m in re.finditer(r"^[-*]\s+(.+)$", body, re.M):
        items.append(md_inline(m.group(1).strip()))
    if not items:
        # fallback: non-empty lines as bullets
        for line in body.splitlines():
            s = line.strip()
            if s and not s.startswith("#") and s != "---":
                items.append(md_inline(s))
    return items[:8]


def parse_cierre(body: str) -> str:
    parts = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s == "---":
            continue
        parts.append(md_inline(s))
    return " ".join(parts) if parts else "Repasa los objetivos y el interactivo de esta lección."


def parse_reto(body: str) -> tuple[str, str, str]:
    """Return (reto_id, reto_title, reto_html)."""
    rid_m = re.search(r"reto_id:\s*`?([^`\n]+)`?", body)
    rid = (rid_m.group(1).strip() if rid_m else "")
    title_m = re.search(r"^###\s+(.+)$", body, re.M)
    title = title_m.group(1).strip() if title_m else "Reto de la lección"
    # Remove reto_id line and ### title for body
    cleaned = re.sub(r"^\*\*?reto_id:?\*?\*?:?\s*`?[^`\n]+`?\s*$", "", body, flags=re.M | re.I)
    cleaned = re.sub(r"^###\s+.+$", "", cleaned, count=1, flags=re.M)
    cleaned = cleaned.strip()
    # Prefer first substantial paragraph / lines
    paras = []
    buf: list[str] = []
    for line in cleaned.splitlines():
        s = line.strip()
        if not s or s == "---":
            if buf:
                paras.append(md_inline(" ".join(buf)))
                buf = []
            continue
        if s.startswith("#"):
            continue
        buf.append(s)
    if buf:
        paras.append(md_inline(" ".join(buf)))
    reto_html = " ".join(paras) if paras else md_inline(cleaned)
    return rid, title, reto_html


def load_lesson(n: int) -> dict:
    path = LEC / f"{n:02d}.md"
    if not path.exists():
        raise SystemExit(f"missing lesson markdown: {path}")
    md = path.read_text(encoding="utf-8")
    title_plain = TEMARIO[n - 1]
    slug = slugify(title_plain)

    objetivos = parse_objetivos(extract_section(md, "Objetivos"))
    if not objetivos:
        raise SystemExit(f"L{n:02d}: no objetivos")

    expl = extract_section(md, "Explicación")
    ejemplos = extract_section(md, "Ejemplos resueltos", "Ejemplos")
    cuerpo_md = expl
    if ejemplos:
        cuerpo_md = expl.rstrip() + "\n\n## Ejemplos resueltos\n\n" + ejemplos
    cuerpo = md_blocks_to_html(cuerpo_md)
    if not cuerpo.strip():
        raise SystemExit(f"L{n:02d}: empty cuerpo")

    vida_body = extract_section(md, "En la vida real")
    vida = parse_vida(vida_body)
    # (generic vida fallback removed — Jorge filler cleanup)

    cierre = parse_cierre(extract_section(md, "Mini cierre"))
    rid, reto_t, reto = parse_reto(extract_section(md, "Reto Profesor"))
    if not rid:
        rid = f"1eso-gh-L{n:02d}"

    cur_t, cur, cur_fig = CURIOSIDADES[n]
    w_label, w_file = WIDGETS[n]
    if not (LEC / w_file).exists():
        raise SystemExit(f"missing widget {w_file}")

    lesson = {
        "n": n,
        "slug": slug,
        "eyebrow": f"Lección {n:02d} · {eyebrow_ud(n)}",
        "title_html": TITLE_HTML[n],
        "title_plain": title_plain,
        "meta": meta_for_lesson(n),
        "curiosidad_t": cur_t,
        "curiosidad": cur,
        "curiosidad_fig": cur_fig,
        "objetivos": objetivos,
        "cuerpo": "\n" + cuerpo,
        "vida_t": "Castilla y León · mundo",
        "vida": vida,
        "vida_fig": FIG_CYCLE[(n - 1) % len(FIG_CYCLE)],
        "widgets": [(w_label, w_file)],
        "reto_t": reto_t,
        "reto": reto,
        "reto_id": rid,
        "cierre": cierre,
    }
    apply_filler_cleanup(lesson)
    return lesson


LESSONS: list[dict] = []


def lesson_filename(n: int) -> str:
    lesson = next(item for item in LESSONS if item["n"] == n)
    return f"leccion-{n:02d}-{lesson['slug']}.html"


def manifest_text(*, offline: bool = False) -> str:
    return json.dumps(
        {
            "name": f"{COURSE_NAME} · Les vencimos",
            "short_name": COURSE_SHORT,
            "start_url": "./index.html" if offline else "./1eso-geografia-historia.html",
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
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n"


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
    hub = "index.html" if offline else "../1eso-geografia-historia.html"
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
            "catch(e){}"
        )
        iframe = (
            f'<iframe title="{title}" class="widget-srcdoc" '
            f'srcdoc="{srcdoc_escape(widget_html)}" '
            f'onload="{html.escape(onload, quote=True)}"></iframe>'
        )
        fallback = (
            f"Si el marco embebido no responde, abre el widget suelto: "
            f'<a href="{fname}">{fname}</a>.'
        )
    else:
        iframe = f'<iframe title="{title}" src="{fname}" loading="lazy"></iframe>'
        fallback = (
            f"Si el marco no carga (<code>file://</code>), abre "
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



# --- Jorge filler cleanup (same policy as Mate) ---
# Curiosidad: keep «Curiosidad histórica» only if genuine; mnemonics → «Truco»; else omit.
# Vida real: keep only strong items (~1 per ~5 lessons).
_CURIOSIDAD_LABEL_BY_N = {1: 'Curiosidad histórica', 5: 'Truco', 9: 'Curiosidad histórica', 11: 'Truco', 15: 'Curiosidad histórica', 16: 'Curiosidad histórica', 18: 'Curiosidad histórica', 19: 'Curiosidad histórica', 22: 'Curiosidad histórica', 23: 'Curiosidad histórica', 24: 'Curiosidad histórica', 25: 'Truco', 27: 'Curiosidad histórica', 31: 'Truco', 32: 'Truco', 33: 'Truco', 34: 'Truco'}
_VIDA_KEEP = {1, 5, 8, 13, 22, 24, 31}


def apply_filler_cleanup(lesson: dict) -> dict:
    """Mutate lesson dict in place for render: label/omit curiosidad; thin vida."""
    n = lesson["n"]
    label = _CURIOSIDAD_LABEL_BY_N.get(n, "")
    lesson["curiosidad_label"] = label
    if not label:
        lesson["curiosidad_t"] = ""
        lesson["curiosidad"] = ""
    if n not in _VIDA_KEEP:
        lesson["vida_t"] = ""
        lesson["vida"] = []
    return lesson


def ship_maestro_into_pack(root: pathlib.Path) -> None:
    """Copy shared _maestro runtime + all lecciones/maestro-*.json into flat pack root."""
    maestro_src = REPO / "profesor/_maestro"
    if maestro_src.is_dir():
        dst = root / "_maestro"
        dst.mkdir(exist_ok=True)
        for fname in ("maestro-runtime.js", "maestro-puntero.css", "maestro-demo.html", "README.md"):
            src = maestro_src / fname
            if src.exists():
                shutil.copy2(src, dst / fname)
                print("Shipped", f"_maestro/{fname}")
    n_json = 0
    for mj in sorted(LEC.glob("maestro-*.json")):
        shutil.copy2(mj, root / mj.name)
        n_json += 1
    print(f"Shipped {n_json} maestro-*.json from lecciones/")


def rewrite_maestro_paths_offline(doc: str) -> str:
    """Flat-pack path rewrite for modo maestro assets (sibling _maestro/)."""
    doc = doc.replace("../../_maestro/maestro-puntero.css", "_maestro/maestro-puntero.css")
    doc = doc.replace("../../_maestro/maestro-runtime.js", "_maestro/maestro-runtime.js")
    return doc


def ensure_offline_embed_class(doc: str) -> str:
    """Add offline-embed to body.leccion-shell without stripping attributes (e.g. data-maestro-json)."""
    def repl(m: re.Match) -> str:
        attrs = m.group(1) or ""
        if re.search(r'\bclass="', attrs):
            def class_repl(cm: re.Match) -> str:
                classes = cm.group(1)
                if re.search(r'(?<![\w-])offline-embed(?![\w-])', classes):
                    return cm.group(0)
                return f'class="{classes} offline-embed"'
            attrs2 = re.sub(r'\bclass="([^"]*)"', class_repl, attrs, count=1)
            return f"<body{attrs2}>"
        return f'<body{attrs} class="leccion-shell offline-embed">'
    return re.sub(r"<body([^>]*)>", repl, doc, count=1, flags=re.I)


def apply_maestro_wire(shell_path: pathlib.Path, n: int, *, offline: bool = False) -> None:
    """Re-wire shell for modo maestro after render_lesson (idempotent)."""
    mj = LEC / f"maestro-{n:02d}.json"
    if not mj.exists() or not shell_path.exists():
        return
    import json
    import sys
    wire_dir = str(REPO / "profesor/_maestro")
    if wire_dir not in sys.path:
        sys.path.insert(0, wire_dir)
    from wire_shell_maestro import wire  # type: ignore
    data = json.loads(mj.read_text(encoding="utf-8"))
    curso = data.get("curso") or COURSE_NAME
    titulo = data.get("titulo") or ""
    pasos = data.get("pasos") or []
    wire(shell_path, n, curso, titulo, pasos)
    if offline:
        doc = shell_path.read_text(encoding="utf-8")
        doc = rewrite_maestro_paths_offline(doc)
        shell_path.write_text(doc, encoding="utf-8")


def render_lesson(lesson: dict, *, offline: bool) -> str:
    n = lesson["n"]
    css = "leccion-shell.css" if offline else "../../_plantilla-leccion/leccion-shell.css"
    js = "leccion-shell-nav.js" if offline else "../../_plantilla-leccion/leccion-shell-nav.js"
    fig = (lambda f: f"figuras/{f}" if offline else f"../../_plantilla-leccion/figuras/{f}")
    home = "index.html" if offline else "../../../index.html"
    marca_meta = f"{COURSE_NAME} · offline" if offline else COURSE_NAME
    icon_root = "icons" if offline else "../icons"
    manifest_href = "manifest.webmanifest" if offline else "../manifest.webmanifest"
    body_class = "leccion-shell offline-embed" if offline else "leccion-shell"

    objs = "".join(f"      <li>{o}</li>\n" for o in lesson["objetivos"])

    w_parts = []
    for lab, fn in lesson["widgets"]:
        wh = None
        if offline:
            wh = load_widget_html(fn)
            assert_widget_offline_safe(fn, wh)
        w_parts.append(widget_block(lab, fn, offline=offline, widget_html=wh))
    w_html = "\n".join(w_parts)


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
    else:
        vida_html = ""

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
      <li>Usa mapa, escala, gráfico o fuente con criterio.</li>
      <li>Conecta con CyL, España o el mundo cercano.</li>
      <li>Emplea el vocabulario de la lección con precisión.</li>
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
    path.write_text(
        f"""<!DOCTYPE html>
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
""",
        encoding="utf-8",
    )


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

  .hub-cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
    align-items: center;
  }
  .hub-cta-maestro {
    background: transparent;
    color: var(--lv-titulo);
    border: 1px solid var(--lv-acento);
  }
  .hub-cta-maestro:hover {
    background: rgba(196, 161, 90, 0.12);
    color: var(--lv-titulo);
    filter: none;
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
    if for_downloads:
        css = "../profesor/_plantilla-leccion/leccion-shell.css"
        home = "../index.html"
        descargas = "../descargas.html"
        brand = "../brand/favicon/"
        manifest = "../profesor/1eso-geografia-historia/manifest.webmanifest"
        lec_prefix = "../profesor/1eso-geografia-historia/lecciones/"
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
<title>{COURSE_NAME} · Les vencimos</title>
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
    <h1 id="hub-titulo">{COURSE_NAME}</h1>
    <p class="hub-status">
      <strong>{"Pack completo L01–L%02d" % AVAILABLE if AVAILABLE >= TOTAL else "Lecciones 01–%02d disponibles" % AVAILABLE}</strong> ({pack_ud_blurb()}) en shell HTML.
      {"Curso cerrado" if AVAILABLE >= TOTAL else "Curso en construcción"} ({AVAILABLE}/{TOTAL} lecciones).
      <strong>ZIP offline</strong> (sin instalar: descomprime y abre <code>ABRE-AQUI.html</code>) en <a href="{descargas}">Descargas</a>.
    </p>
    <div class="hub-cta-row">
    <a class="hub-cta" href="{lec_prefix}{l01}">Abrir lección 01 →</a>
    <a class="hub-cta hub-cta-maestro" href="{lec_prefix}{l01}?maestro=1">Modo maestro →</a>
    </div>
  </section>

  <p class="hub-nota">Índice del temario completo ({TOTAL} lecciones). Disponibles L01–L{AVAILABLE:02d} como <code>leccion-NN-….html</code> (alias <code>leccion-NN.html</code>).{' Curso completo.' if AVAILABLE >= TOTAL else f' L{AVAILABLE+1:02d}–L{TOTAL} próximamente.'}</p>

  <ol class="hub-lista">
{chr(10).join(items)}
  </ol>

  <p class="hub-pie-nota">
    Educación obligatoria · currículo oficial CyL (Decreto 39/2022). Misma familia que Mate y ByG; distinto del pack Profesor (multi-materia).
    Interactivos L01–L{AVAILABLE:02d}: {pack_interactivos_blurb()}.
  </p>

  <footer class="leccion-pie">
    <strong>Les vencimos</strong> · {COURSE_NAME} · {"pack completo " if AVAILABLE >= TOTAL else ""}L01–L{AVAILABLE:02d}/{TOTAL}
  </footer>
</div>
</body>
</html>
"""


def write_hub() -> None:
    HUB.write_text(render_hub(for_downloads=False), encoding="utf-8")
    (REPO / "downloads/1eso-geografia-historia.html").write_text(
        render_hub(for_downloads=True), encoding="utf-8"
    )
    print("Wrote hub (+ downloads mirror)")


def update_descargas() -> None:
    text = DESCARGAS.read_text(encoding="utf-8")
    lead_old_patterns = [
        r"Currículo oficial Castilla y León \(LOMLOE\)\. 1º ESO Matemáticas y Biología y Geología \(L01–L40\)\. <strong>No es el pack Profesor</strong> \(ese es otro: muchas materias, más sencillo\)\.",
        r"Currículo oficial Castilla y León \(LOMLOE\)\. 1º ESO Matemáticas y Biología y Geología \(L01–L\d+\)\. <strong>No es el pack Profesor</strong> \(ese es otro: muchas materias, más sencillo\)\.",
        r"Currículo oficial Castilla y León \(LOMLOE\)\. 1º ESO Matemáticas, Biología y Geología y Geografía e Historia \(L01–L\d+ de \d+\)\. <strong>No es el pack Profesor</strong> \(ese es otro: muchas materias, más sencillo\)\.",
    ]
    lead_new = (
        "Currículo oficial Castilla y León (LOMLOE). 1º ESO Matemáticas, Biología y Geología "
        f"y Geografía e Historia (L01–L{AVAILABLE:02d} de {TOTAL}). "
        "<strong>No es el pack Profesor</strong> (ese es otro: muchas materias, más sencillo)."
    )
    for pat in lead_old_patterns:
        text2, n = re.subn(pat, lead_new, text, count=1)
        if n:
            text = text2
            break

    article = f"""        <article class="item">
          <div class="num">08c</div>
          <div>
            <h2>1º ESO Geografía e Historia</h2>
            <p class="kicker">Oficial CyL · Decreto 39/2022 · {"pack completo (" + str(TOTAL) + " lecciones)" if AVAILABLE >= TOTAL else f"L01–L{AVAILABLE:02d} (de {TOTAL} previstas)"}</p>
            <p><strong>No se instala.</strong> Descomprime y abre <code>ABRE-AQUI.html</code> / <code>index.html</code>.
            Pack plano L01–L{AVAILABLE:02d} ({pack_ud_blurb(short=True)}: mapas y clima; pensamiento histórico, Prehistoria, civilizaciones, Grecia–Roma y patrimonio CyL{"; compromiso cívico y proyectos" if AVAILABLE >= TOTAL else ""}).
            {"Curso cerrado (" + f"{TOTAL}/{TOTAL}" + ")" if AVAILABLE >= TOTAL else f"Curso en construcción ({AVAILABLE}/{TOTAL})"}. Sin nube ni servidor.
            Distinto del pack Profesor.</p>
            <div class="actions">
              <a class="btn-download" href="/downloads/1eso-geografia-historia-offline.zip" download="1eso-geografia-historia-offline.zip">Descargar ZIP</a>
              <a class="textlink" href="/profesor/1eso-geografia-historia/lecciones/{lesson_filename(1)}">Abrir lección 01</a>
              <a class="textlink" href="/profesor/1eso-geografia-historia/1eso-geografia-historia.html">Índice del curso</a>
            </div>
          </div>
        </article>
"""

    if "1eso-geografia-historia-offline.zip" in text:
        # Replace existing GeoHistoria article block
        text2, n = re.subn(
            r'        <article class="item">\s*<div class="num">08c</div>.*?</article>\n',
            article,
            text,
            count=1,
            flags=re.S,
        )
        if n:
            text = text2
            print("Updated descargas.html GeoHistoria article")
        else:
            print("descargas.html already had ZIP link; article pattern not replaced")
    else:
        needle = '        </article>\n      </div>\n\n      <div class="section-modulos">\n        <h2>Aprender para el cole</h2>'
        # Insert after ByG article (last article before Aprender para el cole in Educación block)
        marker = "1eso-biologia-geologia-offline.zip"
        idx = text.find(marker)
        if idx < 0:
            raise SystemExit("descargas.html ByG block not found for GeoHistoria insert")
        # find end of that article
        art_end = text.find("</article>", idx)
        if art_end < 0:
            raise SystemExit("descargas.html ByG article end not found")
        art_end = art_end + len("</article>\n")
        text = text[:art_end] + article + text[art_end:]
        print("Inserted descargas.html GeoHistoria article")

    DESCARGAS.write_text(text, encoding="utf-8")


def update_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    new = (
        f"1º ESO Matemáticas + Biología y Geología + Geografía e Historia L01–L{AVAILABLE:02d} "
        "(oficial CyL). Descarga ZIP offline en Descargas."
    )
    patterns = [
        r"1º ESO Matemáticas \+ Biología y Geología \+ Geografía e Historia(?: \+ Lengua)? L0?\d+(?:–L?\d+)? \(oficial CyL\)\. Descarga ZIP offline en Descargas\.?",
        r"1º ESO Matemáticas \+ Biología y Geología L0?\d+(?:–L?\d+)? \(oficial CyL\)\. Descarga ZIP offline en Descargas\.?",
        r"1º ESO Matemáticas \(oficial CyL\)\. L01 lista — descarga ZIP offline en Descargas\.?",
    ]
    for pat in patterns:
        text2, n = re.subn(pat, new, text, count=1)
        if n:
            INDEX.write_text(text2, encoding="utf-8")
            print("Updated index.html")
            return
    print("WARN: index.html card text not found — leaving home untouched")
    return


def build_offline_pack() -> None:
    if PACK_DIR.exists():
        shutil.rmtree(PACK_DIR)
    root = PACK_DIR / ZIP_FOLDER
    root.mkdir(parents=True)

    (root / "LEEME.md").write_text(
        f"""# {COURSE_NAME} — pack offline

No hay que instalar nada. Descomprime y abre **ABRE-AQUI.html** (o index.html).

**Qué es:** lecciones de **Educación obligatoria** (currículo oficial Castilla y León, Decreto 39/2022).
{"Este pack trae el **curso completo** (lecciones **01–%02d/%d**)" % (AVAILABLE, TOTAL) if AVAILABLE >= TOTAL else "Este pack trae las lecciones **01–%02d/%d**" % (AVAILABLE, TOTAL)} ({pack_ud_blurb()}) en HTML plano (shell + interactivos embebidos).
{"" if AVAILABLE >= TOTAL else "L%02d–L%d próximamente (UD C · Compromiso cívico)." % (AVAILABLE + 1, TOTAL) + chr(10)}
**Cómo abrir (Android / PC) — 4 pasos**

1. Descarga el ZIP.
2. Abre **Archivos / Mis archivos** (NO la lista Descargas del navegador).
3. Descomprime y entra en la carpeta `{ZIP_FOLDER}`.
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
<title>{COURSE_NAME} · offline · Les vencimos</title>
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
    <h1 class="titulo-leccion">{COURSE_NAME}</h1>
    <p class="meta-leccion">{"Pack completo L01–L%02d/%d · curso cerrado" % (AVAILABLE, TOTAL) if AVAILABLE >= TOTAL else "L01–L%02d/%d · UD A + UD B · curso en construcción" % (AVAILABLE, TOTAL)}</p>
  </header>
  <div class="no-install">
    <strong>No hay que instalar nada.</strong> Abre <code>ABRE-AQUI.html</code> o <code>index.html</code> desde esta carpeta
    (Archivos / Mis archivos → carpeta descomprimida → <code>file://</code>).
    El interactivo va embebido en la lección.
    En Chrome/Android: menú → <strong>Añadir a pantalla de inicio</strong>.
    <strong>Nunca</strong> abras desde la lista Descargas del navegador (<code>content://</code>).
  </div>
  <p><a class="big-cta" href="{lesson_filename(1)}">Abrir lección 01 →</a>
     &nbsp; <a class="big-cta hub-cta-maestro" href="{lesson_filename(1)}?maestro=1" style="background:transparent;color:#0E0E0C;border:2px solid #C4A15A;box-shadow:none">Probar modo maestro</a>
     &nbsp; <a href="calculadora.html">Calculadora</a></p>
  <p class="hub-nota">{"Curso completo (%d/%d). Usa siempre este índice." % (TOTAL, TOTAL) if AVAILABLE >= TOTAL else "Disponibles L01–L%02d. L%02d–L%d próximamente. Usa siempre este índice." % (AVAILABLE, AVAILABLE + 1, TOTAL)}</p>
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
        apply_maestro_wire(root / lesson_filename(L["n"]), L["n"], offline=True)
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

    ship_maestro_into_pack(root)

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
    global LESSONS
    LESSONS = [load_lesson(n) for n in range(1, AVAILABLE + 1)]
    ensure_course_branding()
    for L in LESSONS:
        out = LEC / lesson_filename(L["n"])
        out.write_text(render_lesson(L, offline=False), encoding="utf-8")
        apply_maestro_wire(out, L["n"], offline=False)
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
