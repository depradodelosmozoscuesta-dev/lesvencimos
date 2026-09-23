# -*- coding: utf-8 -*-
"""Helpers to assemble 1º ESO Matemáticas lesson markdown."""
from pathlib import Path

OUT = Path("/workspace/lesvencimos/profesor/1eso-matematicas/lecciones")

def save(meta, body):
    n = meta["n"]
    L = []
    a = L.append
    a("# Lección %02d. %s" % (n, meta["titulo"]))
    a("")
    a("**Curso:** 1º ESO Matemáticas · **UD%s:** %s" % (meta["ud"], meta["ud_titulo"]))
    a("**Saberes CyL (Decreto 39/2022):** %s" % meta["saberes"])
    if meta.get("e"):
        a("**Énfasis socioafectivo [E]:** sí")
    a("")
    a("---")
    a("")
    a("## Objetivos")
    a("")
    for i, o in enumerate(body["objetivos"], 1):
        a("%d. %s" % (i, o))
    a("")
    a("## Explicación")
    a("")
    a(body["explicacion"].strip())
    a("")
    a("## En la vida real")
    a("")
    vr = body.get("vida_real") or []
    if isinstance(vr, str):
        a(vr.strip())
    else:
        for item in vr:
            a("- %s" % item)
    a("")
    a("## Ejemplos resueltos")
    a("")
    for i, ex in enumerate(body["ejemplos"], 1):
        tit = (": %s" % ex["titulo"]) if ex.get("titulo") else ""
        a("### Ejemplo %d%s" % (i, tit))
        a("")
        a(ex["texto"].strip())
        a("")
    a("## Practica")
    a("")
    a("*Haz los ejercicios sin mirar las soluciones. Van de más fáciles a más exigentes.*")
    a("")
    for i, pr in enumerate(body["practica"], 1):
        a("**%d.** %s" % (i, pr))
        a("")
    if meta.get("e") and body.get("socio"):
        a("## Momento socioafectivo")
        a("")
        a(body["socio"].strip())
        a("")
    a("## Soluciones y porqués")
    a("")
    for s in body["soluciones"]:
        a("**%s.** %s" % (s["n"], s["sol"]))
        a("")
        a("*Porqué:* %s" % s["porque"])
        a("")
    a("## Errores frecuentes")
    a("")
    for e in body["errores"]:
        a("- %s" % e)
    a("")
    a("## Mini cierre — qué recordar")
    a("")
    a(body["cierre"].strip())
    a("")
    reto = body.get("reto")
    if reto:
        rid = reto.get("id") or ("1eso-mate-L%02d" % n)
        a("<!-- RETO_WEB id=%s -->" % rid)
        a("")
        a("## Reto Profesor")
        a("")
        a("**reto_id:** `%s`" % rid)
        a("")
        a("### %s" % reto["titulo"])
        a("")
        a(reto["enunciado"].strip())
        a("")
        a("**Una buena idea suele…**")
        a("")
        for c in reto.get("criterios", []):
            a("- %s" % c)
        a("")
        a("*Este reto está pensado para publicarlo en lesvencimos.com (idea + votación / premio). Aún no hace falta enviarlo a ninguna web: guárdalo en tu cuaderno o portfolio.*")
        a("")
    md = "\n".join(L)
    path = OUT / ("%02d.md" % n)
    path.write_text(md, encoding="utf-8")
    return len(md.split()), len(md.splitlines()), path
