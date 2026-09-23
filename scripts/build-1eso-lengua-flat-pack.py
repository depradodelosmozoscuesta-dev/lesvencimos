#!/usr/bin/env python3
"""Build online shell + flat offline pack for 1º ESO Lengua Castellana y Literatura (L01–L40 of 40)."""
from __future__ import annotations

import html
import json
import pathlib
import re
import shutil
import unicodedata
import zipfile

REPO = pathlib.Path("/workspace/lesvencimos")
COURSE_DIR = REPO / "profesor/1eso-lengua-castellana"
LEC = COURSE_DIR / "lecciones"
PLANTILLA = REPO / "profesor/_plantilla-leccion"
HUB = COURSE_DIR / "1eso-lengua-castellana.html"
DESCARGAS = REPO / "descargas.html"
INDEX = REPO / "index.html"
PACK_DIR = REPO / "downloads/_build-1eso-lengua-flat"
ZIP_PATH = REPO / "downloads/1eso-lengua-castellana-offline.zip"
COURSE_ICONS = COURSE_DIR / "icons"
BRAND_ICONS = REPO / "brand/favicon"
TOTAL = 40
AVAILABLE = 40

COURSE_NAME = "1º ESO Lengua Castellana y Literatura"
COURSE_SHORT = "1º ESO Lengua"
ZIP_FOLDER = "1eso-lengua-castellana-offline"
HUB_BASENAME = "1eso-lengua-castellana.html"
DOWNLOADS_HUB = "1eso-lengua-castellana.html"
ZIP_BASENAME = "1eso-lengua-castellana-offline.zip"
ARTICLE_NUM = "08d"

# UD ranges: A = L01–L09, B = L10–L27, C = L28–L35, D = L36–L40
UD_BLOCKS = {
    "A": ("UD A · Las lenguas y sus hablantes", "bloque A"),
    "B": ("UD B · Comunicación", "bloque B"),
    "C": ("UD C · Educación literaria", "bloque C"),
    "D": ("UD D · Reflexión sobre la lengua", "bloque D"),
}


def ud_for_lesson(n: int) -> str:
    if 1 <= n <= 9:
        return "A"
    if 10 <= n <= 27:
        return "B"
    if 28 <= n <= 35:
        return "C"
    if 36 <= n <= 40:
        return "D"
    raise ValueError(f"lesson out of range: {n}")


def eyebrow_ud(n: int) -> str:
    return UD_BLOCKS[ud_for_lesson(n)][0]


def meta_for_lesson(n: int) -> str:
    bloque = UD_BLOCKS[ud_for_lesson(n)][1]
    return f"1º ESO Lengua Castellana y Literatura · CyL Decreto 39/2022 · {bloque}"


def pack_ud_blurb(*, short: bool = False) -> str:
    """Human copy for which UDs the current AVAILABLE pack covers."""
    if AVAILABLE >= TOTAL:
        if short:
            return "UD A + UD B + UD C + UD D"
        return (
            "UD A · Las lenguas y sus hablantes + UD B · Comunicación "
            "+ UD C · Educación literaria + UD D · Reflexión sobre la lengua"
        )
    if AVAILABLE >= 27:
        # UD A + UD B complete (L01–L27); NOT full course
        if short:
            return "UD A + UD B"
        return (
            "UD A · Las lenguas y sus hablantes + UD B · Comunicación"
        )
    # Partial: A + inicio B (L10)
    if short:
        return "UD A + inicio UD B"
    return "UD A · Las lenguas y sus hablantes + L10 Comunicación"


def pack_interactivos_blurb() -> str:
    base_a = (
        "lenguas/dialectos/hablas, marco legal CyL, biografía lingüística, "
        "familias del mundo, mapa de España y signos, plurilingüismo, "
        "prejuicios e inclusivo, fenómenos (seseo–voseo), variedades CyL (UD A)"
    )
    base_b = (
        "hecho comunicativo, no verbal, secuencias, diálogo/exposición, adecuación, "
        "géneros personales y educativos, redes/medios, turno/cortesía, "
        "comprensión y producción oral/escrita, instrucciones, oral-escrito/coloquial-formal, "
        "deixis/cohesión, verbos/puntuación, debates (UD B)"
    )
    base_c = (
        "biblioteca e itinerario, literatura/placer/artes, recomendar lecturas, "
        "géneros literarios, recursos expresivos, perspectiva de género, "
        "lectura expresiva/dramatización, crear textos breves (UD C)"
    )
    base_d = (
        "sintaxis/léxico/pragmática, unidades sonido–palabra–oración, "
        "clases de palabras, forma/función y oración simple, "
        "ortografía/diccionarios/vulgarismos CyL + portfolio (UD D)"
    )
    if AVAILABLE >= TOTAL:
        return base_a + "; " + base_b + "; " + base_c + "; " + base_d
    if AVAILABLE >= 27:
        return base_a + "; " + base_b
    # L01–L10 only
    return base_a + "; hecho comunicativo (inicio UD B)"


# Full temario titles (curso completo L01–L40) — from TEMARIO.md
TEMARIO = [
    "Lenguas, dialectos y hablas: variantes territoriales",
    "Constitución y Estatuto de CyL: marco lingüístico",
    "Mi biografía lingüística y la diversidad en CyL",
    "Familias lingüísticas y lenguas del mundo",
    "Lenguas de España: origen, mapa y lengua de signos",
    "Plurilingüismo frente a diversidad dialectal",
    "Prejuicios lingüísticos y lenguaje inclusivo",
    "Seseo, ceceo, yeísmo y voseo (ejemplos sencillos)",
    "Variedades del español con foco en Castilla y León",
    "El hecho comunicativo: elementos, intención y canal",
    "Comunicación no verbal",
    "Secuencias narrativas y descriptivas",
    "Diálogo y exposición",
    "Adecuación del texto a la situación",
    "Géneros personales: la conversación",
    "Géneros educativos: tipologías textuales",
    "Redes sociales y medios: lectura crítica",
    "Turno de palabra, cortesía y escucha activa",
    "Comprensión oral: sentido global e información relevante",
    "Producción oral: formal e informal",
    "Comprensión lectora: intención, forma y contenido",
    "Producción escrita: redactar, revisar, editar",
    "Instrucciones, normas y avisos del día a día",
    "Oral / escrito y coloquial / formal en la escuela",
    "Deixis, registro y cohesión (conectores y referencias)",
    "Formas verbales y puntuación básica",
    "Debates y cooperación en el aprendizaje",
    "Biblioteca e itinerario lector personal",
    "Literatura: placer, actualidad y otras artes",
    "Recomendar lecturas (oral y soportes)",
    "Géneros literarios: rasgos y fragmentos",
    "Lenguaje literario y recursos expresivos",
    "Lectura con perspectiva de género",
    "Lectura expresiva, dramatización y recitación",
    "Crear textos literarios breves (imitación / transformación)",
    "Oral y escrito: sintaxis, léxico y pragmática",
    "Unidades de la lengua: sonido, palabra, oración",
    "Clases de palabras (sustantivo a interjección)",
    "Forma y función; oración simple; formación de palabras",
    "Ortografía, diccionarios, vulgarismos/localismos de CyL + cierre portfolio",
]

TITLE_HTML = {
    1: "<em>Lenguas</em>, dialectos y hablas: variantes territoriales",
    2: "<em>Constitución</em> y Estatuto de CyL: marco lingüístico",
    3: "Mi <em>biografía lingüística</em> y la diversidad en CyL",
    4: "<em>Familias lingüísticas</em> y lenguas del mundo",
    5: "Lenguas de España: origen, <em>mapa</em> y lengua de signos",
    6: "<em>Plurilingüismo</em> frente a diversidad dialectal",
    7: "Prejuicios lingüísticos y lenguaje <em>inclusivo</em>",
    8: "<em>Seseo</em>, ceceo, yeísmo y voseo (ejemplos sencillos)",
    9: "Variedades del español con foco en <em>Castilla y León</em>",
    10: "El <em>hecho comunicativo</em>: elementos, intención y canal",
    11: "Comunicación <em>no verbal</em>",
    12: "Secuencias <em>narrativas</em> y descriptivas",
    13: "<em>Diálogo</em> y exposición",
    14: "<em>Adecuación</em> del texto a la situación",
    15: "Géneros personales: la <em>conversación</em>",
    16: "Géneros educativos: <em>tipologías</em> textuales",
    17: "Redes sociales y medios: lectura <em>crítica</em>",
    18: "Turno de palabra, <em>cortesía</em> y escucha activa",
    19: "Comprensión oral: sentido <em>global</em> e información relevante",
    20: "Producción oral: <em>formal</em> e informal",
    21: "Comprensión lectora: intención, forma y <em>contenido</em>",
    22: "Producción escrita: redactar, revisar, <em>editar</em>",
    23: "Instrucciones, <em>normas</em> y avisos del día a día",
    24: "Oral / escrito y coloquial / <em>formal</em> en la escuela",
    25: "Deixis, registro y <em>cohesión</em> (conectores y referencias)",
    26: "Formas <em>verbales</em> y puntuación básica",
    27: "<em>Debates</em> y cooperación en el aprendizaje",
    28: "<em>Biblioteca</em> e itinerario lector personal",
    29: "Literatura: <em>placer</em>, actualidad y otras artes",
    30: "<em>Recomendar</em> lecturas (oral y soportes)",
    31: "Géneros literarios: <em>rasgos</em> y fragmentos",
    32: "Lenguaje literario y <em>recursos</em> expresivos",
    33: "Lectura con perspectiva de <em>género</em>",
    34: "Lectura expresiva, <em>dramatización</em> y recitación",
    35: "Crear textos literarios <em>breves</em> (imitación / transformación)",
    36: "Oral y escrito: sintaxis, léxico y <em>pragmática</em>",
    37: "Unidades de la lengua: sonido, <em>palabra</em>, oración",
    38: "Clases de palabras (sustantivo a <em>interjección</em>)",
    39: "Forma y función; oración <em>simple</em>; formación de palabras",
    40: "Ortografía, diccionarios, vulgarismos/localismos de CyL + cierre <em>portfolio</em>",
}

WIDGETS = {
    1: ("Laboratorio · lenguas, dialectos y hablas", "l01-lenguas-dialectos-hablas.html"),
    2: ("Laboratorio · Constitución y Estatuto CyL", "l02-constitucion-estatuto-cyl-marco-linguistico.html"),
    3: ("Laboratorio · biografía lingüística y diversidad CyL", "l03-biografia-linguistica-diversidad-cyl.html"),
    4: ("Laboratorio · familias lingüísticas del mundo", "l04-familias-linguisticas-lenguas-mundo.html"),
    5: ("Laboratorio · lenguas de España y signos", "l05-lenguas-espana-origen-mapa-signos.html"),
    6: ("Laboratorio · plurilingüismo y diversidad dialectal", "l06-plurilinguismo-diversidad-dialectal.html"),
    7: ("Laboratorio · prejuicios y lenguaje inclusivo", "l07-prejuicios-lenguaje-inclusivo.html"),
    8: ("Laboratorio · seseo, ceceo, yeísmo y voseo", "l08-seseo-ceceo-yeismo-voseo.html"),
    9: ("Laboratorio · variedades del español en CyL", "l09-variedades-espanol-castilla-leon.html"),
    10: ("Laboratorio · hecho comunicativo", "l10-hecho-comunicativo-elementos-intencion-canal.html"),
    11: ("Laboratorio · comunicación no verbal", "l11-comunicacion-no-verbal.html"),
    12: ("Laboratorio · secuencias narrativas y descriptivas", "l12-secuencias-narrativas-descriptivas.html"),
    13: ("Laboratorio · diálogo y exposición", "l13-dialogo-y-exposicion.html"),
    14: ("Laboratorio · adecuación del texto a la situación", "l14-adecuacion-texto-situacion.html"),
    15: ("Laboratorio · géneros personales: conversación", "l15-generos-personales-conversacion.html"),
    16: ("Laboratorio · géneros educativos: tipologías", "l16-generos-educativos-tipologias.html"),
    17: ("Laboratorio · redes sociales y lectura crítica", "l17-redes-sociales-medios-lectura-critica.html"),
    18: ("Laboratorio · turno, cortesía y escucha activa", "l18-turno-cortesia-escucha-activa.html"),
    19: ("Laboratorio · comprensión oral: sentido global", "l19-comprension-oral-sentido-global.html"),
    20: ("Laboratorio · producción oral formal e informal", "l20-produccion-oral-formal-informal.html"),
    21: ("Laboratorio · comprensión lectora: intención-forma-contenido", "l21-comprension-lectora-intencion-forma-contenido.html"),
    22: ("Laboratorio · producción escrita: redactar-revisar-editar", "l22-produccion-escrita-redactar-revisar-editar.html"),
    23: ("Laboratorio · instrucciones, normas y avisos", "l23-instrucciones-normas-avisos.html"),
    24: ("Laboratorio · oral/escrito y coloquial/formal", "l24-oral-escrito-coloquial-formal-escuela.html"),
    25: ("Laboratorio · deixis, registro y cohesión", "l25-deixis-registro-cohesion.html"),
    26: ("Laboratorio · formas verbales y puntuación", "l26-formas-verbales-puntuacion-basica.html"),
    27: ("Laboratorio · debates y cooperación", "l27-debates-cooperacion-aprendizaje.html"),
    28: ("Laboratorio · biblioteca e itinerario lector", "l28-biblioteca-itinerario-lector.html"),
    29: ("Laboratorio · literatura: placer, actualidad y artes", "l29-literatura-placer-actualidad-artes.html"),
    30: ("Laboratorio · recomendar lecturas (oral y soportes)", "l30-recomendar-lecturas-oral-soportes.html"),
    31: ("Laboratorio · géneros literarios: rasgos y fragmentos", "l31-generos-literarios-rasgos-fragmentos.html"),
    32: ("Laboratorio · lenguaje literario y recursos", "l32-lenguaje-literario-recursos-expresivos.html"),
    33: ("Laboratorio · lectura con perspectiva de género", "l33-lectura-perspectiva-genero.html"),
    34: ("Laboratorio · lectura expresiva, dramatización y recitación", "l34-lectura-expresiva-dramatizacion-recitacion.html"),
    35: ("Laboratorio · crear textos literarios breves", "l35-crear-textos-literarios-breves.html"),
    36: ("Laboratorio · oral/escrito: sintaxis, léxico y pragmática", "l36-oral-escrito-sintaxis-lexico-pragmatica.html"),
    37: ("Laboratorio · unidades: sonido, palabra, oración", "l37-unidades-lengua-sonido-palabra-oracion.html"),
    38: ("Laboratorio · clases de palabras (sustantivo–interjección)", "l38-clases-de-palabras-sustantivo-interjeccion.html"),
    39: ("Laboratorio · forma/función, oración simple, formación", "l39-forma-funcion-oracion-simple-formacion.html"),
    40: ("Laboratorio · ortografía, diccionarios CyL y portfolio", "l40-ortografia-diccionarios-vulgarismos-cyl-portfolio.html"),
}

# Short curiosidades (MD sources lack a dedicated block)
CURIOSIDADES = {
    1: (
        "Tres capas, un mapa",
        "Lengua, dialecto y habla no son «mejor / peor»: son <strong>escalas</strong> "
        "del mismo fenómeno. En CyL oyes el abrigo (español), el jersey (variedad regional) "
        "y a veces la camiseta (pueblo o barrio).",
        "mapa.svg",
    ),
    2: (
        "Normas que no son gramática",
        "La Constitución y el Estatuto de CyL no enseñan conjugaciones: fijan el "
        "<strong>marco</strong> de las lenguas en España y en la comunidad. Leerlos "
        "con cuidado evita inventar artículos.",
        "ticket.svg",
    ),
    3: (
        "Tu mapa lingüístico",
        "Una <strong>biografía lingüística</strong> cuenta qué lenguas y variedades "
        "usas en casa, en el cole y con amigos. En CyL ese mapa suele ser rico aunque "
        "no lo notes a diario.",
        "mapa.svg",
    ),
    4: (
        "Familias, no banderas",
        "Las <strong>familias lingüísticas</strong> agrupan lenguas por origen común "
        "(como indoeuropea). No son países: el mapa del mundo de las lenguas no coincide "
        "con el de las fronteras.",
        "fuego.svg",
    ),
    5: (
        "Más que castellano",
        "España es un país con varias <strong>lenguas</strong> y con lengua de signos. "
        "Un mapa escolar recuerda distribución y respeto; no sustituye a un atlas oficial.",
        "mapa.svg",
    ),
    6: (
        "Dos ideas distintas",
        "<strong>Plurilingüismo</strong> = varias lenguas. <strong>Diversidad dialectal</strong> = "
        "variedades de una misma lengua. Confundirlas genera prejuicios inútiles.",
        "ticket.svg",
    ),
    7: (
        "Incluir no es «hablar raro»",
        "El lenguaje <strong>inclusivo</strong> busca no dejar a nadie fuera. "
        "Criticar un acento o burlarse de un signo no es humor: es prejuicio lingüístico.",
        "olla.svg",
    ),
    8: (
        "Fenómenos, no fallos",
        "Seseo, ceceo, yeísmo o voseo son <strong>fenómenos</strong> del español "
        "en distintas zonas. Se describen con ejemplos sencillos; no se castigan.",
        "fuego.svg",
    ),
    9: (
        "CyL también varía",
        "Dentro de Castilla y León hay matices de pronunciación y léxico. "
        "La variedad <strong>norteña</strong> no es «la única correcta»: es una más del español.",
        "mapa.svg",
    ),
    10: (
        "ERM + CCC",
        "Emisor, receptor, mensaje + código, canal, contexto: el esquema del "
        "<strong>hecho comunicativo</strong>. La intención (informar, pedir, convencer…) "
        "explica por qué dices lo que dices.",
        "ticket.svg",
    ),
    11: (
        "GMP-TP",
        "Gestos, mirada, postura · tono y proxémica: el cuerpo también comunica. "
        "Si las palabras y el gesto chocan, mucha gente cree más al <strong>cuerpo</strong>.",
        "fuego.svg",
    ),
    12: (
        "NADES",
        "<strong>NA</strong>rrar = acciones en el tiempo. <strong>DES</strong>cribir = cualidades "
        "y sentidos. Distinguir ambas secuencias evita mezclar «qué pasó» con «cómo es».",
        "mapa.svg",
    ),
    13: (
        "DI-EX",
        "<strong>DI</strong>álogo = varias voces. <strong>EX</strong>posición = explicar con "
        "orden. En el aula y en CyL usas las dos: charla y explicación clara.",
        "ticket.svg",
    ),
    14: (
        "Las 4A",
        "A quién, a qué, a dónde (canal) y ajuste de registro: la <strong>adecuación</strong> "
        "elige el texto que encaja en la situación, no «el más largo».",
        "olla.svg",
    ),
    15: (
        "ADC + turno",
        "Apertura, desarrollo y cierre: la <strong>conversación</strong> personal también "
        "tiene forma. Respetar el turno es cooperación, no formalismo vacío.",
        "fuego.svg",
    ),
    16: (
        "ENDE",
        "Exponer, narrar, describir, entablar diálogo: tipologías del <strong>ámbito "
        "educativo</strong>. Elegir la pieza correcta ahorra confusiones en el instituto.",
        "mapa.svg",
    ),
    17: (
        "FOCCE",
        "Fuente, opinión/hecho, clic-intención, contraste, exclusión: lectura "
        "<strong>crítica</strong> de redes y medios antes de compartir.",
        "ticket.svg",
    ),
    18: (
        "TCE-R",
        "Turno, cortesía, escucha y resolución: el mapa mínimo de una charla "
        "<strong>cooperativa</strong>. Interrumpir sin escuchar rompe el acuerdo.",
        "olla.svg",
    ),
    19: (
        "GIR-D",
        "Global, intención, relevante y ¿discriminación?: la comprensión "
        "<strong>oral</strong> no es solo «oir palabras», es filtrar lo importante.",
        "fuego.svg",
    ),
    20: (
        "FAI",
        "Formal vs audiencia e informal consciente: la producción "
        "<strong>oral</strong> cambia de registro según con quién hablas.",
        "mapa.svg",
    ),
    21: (
        "IFC",
        "Intención, forma y contenido: tres capas de la comprensión "
        "<strong>lectora</strong>. Leer solo el contenido deja a medias el mensaje.",
        "ticket.svg",
    ),
    22: (
        "PRRE",
        "Planifica, redacta, revisa, edita: el ciclo de la producción "
        "<strong>escrita</strong>. Publicar el primer borrador no es «ser rápido»: es saltarse pasos.",
        "olla.svg",
    ),
    23: (
        "INA",
        "Instrucción, norma, aviso: textos del día a día. En CyL (colegio, bus, museo) "
        "saber leerlos evita líos y respeta reglas compartidas.",
        "fuego.svg",
    ),
    24: (
        "OECF",
        "Oral/escrito y coloquial/formal: cuatro polos, no dos. En la "
        "<strong>escuela</strong> mezclarlos sin conciencia genera malentendidos.",
        "mapa.svg",
    ),
    25: (
        "DRC",
        "Deixis (aquí/ahora/yo), registro y cohesión (conectores y referencias): "
        "el pegamento que hace que un texto <strong>siga unido</strong>.",
        "ticket.svg",
    ),
    26: (
        "VP",
        "Verbos coherentes y puntuación con sentido: no son adornos. Cambian el "
        "<strong>significado</strong> de lo que escribes.",
        "olla.svg",
    ),
    27: (
        "TAE-C",
        "Turno, argumento, ejemplo y cooperación: el kit del "
        "<strong>debate</strong> escolar. Ganar no es gritar: es razonar juntos.",
        "fuego.svg",
    ),
    28: (
        "BIEA",
        "Biblioteca, interés, elegir, anotar: el mapa del "
        "<strong>itinerario lector</strong>. No es una nota: es tu identidad como lectora/lector.",
        "mapa.svg",
    ),
    29: (
        "PLA-Vín",
        "Placer + vínculos (actualidad, artes, textos): la "
        "<strong>literatura</strong> no vive sola en el libro de texto.",
        "ticket.svg",
    ),
    30: (
        "G2C",
        "Gancho, 2 razones y cierre (para quién): recomendar una lectura es "
        "<strong>oralidad</strong> con propósito, no un spoiler.",
        "olla.svg",
    ),
    31: (
        "NaLiTe",
        "Narrativa, lírica, teatro: tres familias de "
        "<strong>géneros</strong>. Los rasgos se ven en fragmentos, no en etiquetas vacías.",
        "fuego.svg",
    ),
    32: (
        "CoMeP-HA",
        "Comparación, metáfora, personificación, hipérbole, aliteración: el kit de "
        "<strong>recursos</strong> expresivos del lenguaje literario.",
        "mapa.svg",
    ),
    33: (
        "¿Quién-rol?",
        "¿Quién actúa? ¿Qué rol se impone? ¿Se puede abrir?: lectura con "
        "<strong>perspectiva de género</strong> sin convertir el texto en moralina.",
        "ticket.svg",
    ),
    34: (
        "VoPaGe",
        "Voz, pausas y gesto: la lectura "
        "<strong>expresiva</strong> (y la dramatización) hace oír el texto, no solo verlo.",
        "olla.svg",
    ),
    35: (
        "ITC",
        "Imitar, transformar, continuar: tres puertas para "
        "<strong>crear</strong> textos literarios breves sin inventar un género nuevo.",
        "fuego.svg",
    ),
    36: (
        "SiLéPra",
        "Sintaxis, léxico y pragmática: tres capas al pasar de "
        "<strong>oral</strong> a escrito (y al revés).",
        "mapa.svg",
    ),
    37: (
        "SoPaO",
        "Sonido, palabra, oración: las "
        "<strong>unidades</strong> de la lengua encajan como piezas, no como adornos.",
        "ticket.svg",
    ),
    38: (
        "SA-PD-V + APCI",
        "Sustantivo–adjetivo, pronombre–determinante, verbo, y el resto hasta la "
        "<strong>interjección</strong>: clases de palabras con función, no solo lista.",
        "olla.svg",
    ),
    39: (
        "FoFu-OS-Af",
        "Forma/función, oración simple y afijos: ver "
        "<strong>cómo</strong> se construye una oración y una palabra.",
        "fuego.svg",
    ),
    40: (
        "OrDiVu-P",
        "Ortografía, diccionario, vulgarismos/localismos de CyL y "
        "<strong>portfolio</strong>: cierra el curso con corrección respetuosa y evidencias.",
        "mapa.svg",
    ),
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
    if not vida:
        vida = [
            "Relaciona esta lección con un lugar o noticia de <strong>Castilla y León</strong>.",
            "Explica el concepto clave a alguien de casa con un ejemplo cercano.",
        ]

    cierre = parse_cierre(extract_section(md, "Mini cierre"))
    rid, reto_t, reto = parse_reto(extract_section(md, "Reto Profesor"))
    if not rid:
        rid = f"1eso-lengua-L{n:02d}"

    cur_t, cur, cur_fig = CURIOSIDADES[n]
    w_label, w_file = WIDGETS[n]
    if not (LEC / w_file).exists():
        raise SystemExit(f"missing widget {w_file}")

    return {
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


LESSONS: list[dict] = []


def lesson_filename(n: int) -> str:
    lesson = next(item for item in LESSONS if item["n"] == n)
    return f"leccion-{n:02d}-{lesson['slug']}.html"


def manifest_text(*, offline: bool = False) -> str:
    return json.dumps(
        {
            "name": f"{COURSE_NAME} · Les vencimos",
            "short_name": COURSE_SHORT,
            "start_url": "./index.html" if offline else "./1eso-lengua-castellana.html",
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
    hub = "index.html" if offline else "../1eso-lengua-castellana.html"
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
      <li>Usa términos de la lección con precisión (sin inventar normas).</li>
      <li>Conecta con CyL, el aula o tu entorno lingüístico cercano.</li>
      <li>Evita prejuicios: describe variedades, no las insultes.</li>
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
        manifest = "../profesor/1eso-lengua-castellana/manifest.webmanifest"
        lec_prefix = "../profesor/1eso-lengua-castellana/lecciones/"
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
    <a class="hub-cta" href="{lec_prefix}{l01}">Abrir lección 01 →</a>
  </section>

  <p class="hub-nota">Índice del temario completo ({TOTAL} lecciones). Disponibles L01–L{AVAILABLE:02d} como <code>leccion-NN-….html</code> (alias <code>leccion-NN.html</code>).{' Curso completo.' if AVAILABLE >= TOTAL else f' L{AVAILABLE+1:02d}–L{TOTAL} próximamente.'}</p>

  <ol class="hub-lista">
{chr(10).join(items)}
  </ol>

  <p class="hub-pie-nota">
    Educación obligatoria · currículo oficial CyL (Decreto 39/2022). Misma familia que Mate, ByG y GeoHistoria; distinto del pack Profesor (multi-materia).
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
    (REPO / "downloads/1eso-lengua-castellana.html").write_text(
        render_hub(for_downloads=True), encoding="utf-8"
    )
    print("Wrote hub (+ downloads mirror)")


def update_descargas() -> None:
    text = DESCARGAS.read_text(encoding="utf-8")
    lead_old_patterns = [
        r"Currículo oficial Castilla y León \(LOMLOE\)\. 1º ESO Matemáticas, Biología y Geología y Geografía e Historia \(L01–L\d+ de \d+\)\. <strong>No es el pack Profesor</strong> \(ese es otro: muchas materias, más sencillo\)\.",
        r"Currículo oficial Castilla y León \(LOMLOE\)\. 1º ESO Matemáticas, Biología y Geología, Geografía e Historia y Lengua Castellana y Literatura \(L01–L\d+ de \d+\)\. <strong>No es el pack Profesor</strong> \(ese es otro: muchas materias, más sencillo\)\.",
        r"Currículo oficial Castilla y León \(LOMLOE\)\. 1º ESO Matemáticas, Biología y Geología, Geografía e Historia y Lengua \(L01–L\d+ de \d+\)\. <strong>No es el pack Profesor</strong> \(ese es otro: muchas materias, más sencillo\)\.",
    ]
    lead_new = (
        "Currículo oficial Castilla y León (LOMLOE). 1º ESO Matemáticas, Biología y Geología, "
        f"Geografía e Historia y Lengua Castellana y Literatura (L01–L{AVAILABLE:02d} de {TOTAL}). "
        "<strong>No es el pack Profesor</strong> (ese es otro: muchas materias, más sencillo)."
    )
    for pat in lead_old_patterns:
        text2, n = re.subn(pat, lead_new, text, count=1)
        if n:
            text = text2
            break

    article = f"""        <article class="item">
          <div class="num">{ARTICLE_NUM}</div>
          <div>
            <h2>1º ESO Lengua Castellana y Literatura</h2>
            <p class="kicker">Oficial CyL · Decreto 39/2022 · {"pack completo (" + str(TOTAL) + " lecciones)" if AVAILABLE >= TOTAL else f"L01–L{AVAILABLE:02d} (de {TOTAL} previstas)"}</p>
            <p><strong>No se instala.</strong> Descomprime y abre <code>ABRE-AQUI.html</code> / <code>index.html</code>.
            {"Pack completo L01–L%02d (%s: lenguas y hablantes; comunicación; educación literaria; reflexión sobre la lengua)." % (AVAILABLE, pack_ud_blurb(short=True)) if AVAILABLE >= TOTAL else "Pack plano L01–L%02d (%s: lenguas y hablantes; comunicación completa)." % (AVAILABLE, pack_ud_blurb(short=True))}
            {"Curso cerrado (" + f"{TOTAL}/{TOTAL}" + ")" if AVAILABLE >= TOTAL else f"Curso en construcción ({AVAILABLE}/{TOTAL})"}. Sin nube ni servidor.
            Distinto del pack Profesor.</p>
            <div class="actions">
              <a class="btn-download" href="/downloads/{ZIP_BASENAME}" download="{ZIP_BASENAME}">Descargar ZIP</a>
              <a class="textlink" href="/profesor/1eso-lengua-castellana/lecciones/{lesson_filename(1)}">Abrir lección 01</a>
              <a class="textlink" href="/profesor/1eso-lengua-castellana/{HUB_BASENAME}">Índice del curso</a>
            </div>
          </div>
        </article>
"""

    if ZIP_BASENAME in text:
        text2, n = re.subn(
            rf'        <article class="item">\s*<div class="num">{ARTICLE_NUM}</div>.*?</article>\n',
            article,
            text,
            count=1,
            flags=re.S,
        )
        if n:
            text = text2
            print("Updated descargas.html Lengua article")
        else:
            print("descargas.html already had ZIP link; article pattern not replaced")
    else:
        marker = "1eso-geografia-historia-offline.zip"
        idx = text.find(marker)
        if idx < 0:
            raise SystemExit("descargas.html GeoHistoria block not found for Lengua insert")
        art_end = text.find("</article>", idx)
        if art_end < 0:
            raise SystemExit("descargas.html GeoHistoria article end not found")
        art_end = art_end + len("</article>\n")
        text = text[:art_end] + article + text[art_end:]
        print("Inserted descargas.html Lengua article")

    DESCARGAS.write_text(text, encoding="utf-8")


def update_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    if AVAILABLE >= TOTAL:
        new = (
            f"1º ESO Matemáticas + Biología y Geología + Geografía e Historia + Lengua pack completo "
            f"{AVAILABLE}/{TOTAL} (oficial CyL). Descarga ZIP offline en Descargas."
        )
    else:
        new = (
            f"1º ESO Matemáticas + Biología y Geología + Geografía e Historia + Lengua L01–L{AVAILABLE:02d} "
            "(oficial CyL). Descarga ZIP offline en Descargas."
        )
    patterns = [
        r"1º ESO Matemáticas \+ Biología y Geología \+ Geografía e Historia \+ Lengua pack completo \d+/\d+ \(oficial CyL\)\. Descarga ZIP offline en Descargas\.?",
        r"1º ESO Matemáticas \+ Biología y Geología \+ Geografía e Historia \+ Lengua L0?\d+(?:–L?\d+)? \(oficial CyL\)\. Descarga ZIP offline en Descargas\.?",
        r"1º ESO Matemáticas \+ Biología y Geología \+ Geografía e Historia L0?\d+(?:–L?\d+)? \(oficial CyL\)\. Descarga ZIP offline en Descargas\.?",
        r"1º ESO Matemáticas \+ Biología y Geología L0?\d+(?:–L?\d+)? \(oficial CyL\)\. Descarga ZIP offline en Descargas\.?",
        r"1º ESO Matemáticas \(oficial CyL\)\. L01 lista — descarga ZIP offline en Descargas\.?",
    ]
    for pat in patterns:
        text2, n = re.subn(pat, new, text, count=1)
        if n:
            INDEX.write_text(text2, encoding="utf-8")
            print("Updated index.html")
            return
    raise SystemExit("index.html Educación obligatoria card text not found")



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
{"" if AVAILABLE >= TOTAL else ("L%02d–L%d próximamente (UD C · Educación literaria + UD D · Reflexión sobre la lengua)." % (AVAILABLE + 1, TOTAL) if AVAILABLE >= 27 else "L%02d–L%d próximamente (resto UD B · Comunicación + UD C + UD D)." % (AVAILABLE + 1, TOTAL)) + chr(10)}
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
    <p class="meta-leccion">{"Pack completo L01–L%02d/%d · curso cerrado" % (AVAILABLE, TOTAL) if AVAILABLE >= TOTAL else "L01–L%02d/%d · %s · curso en construcción" % (AVAILABLE, TOTAL, pack_ud_blurb(short=True))}</p>
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
    global LESSONS
    LESSONS = [load_lesson(n) for n in range(1, AVAILABLE + 1)]
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
