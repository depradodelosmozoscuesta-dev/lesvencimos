#!/usr/bin/env python3
"""Pack PD Spanish novels into biblioteca-libros multipart JSON + update catalog."""
from __future__ import annotations
import html as htmlmod
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "modulos" / "biblioteca-libros"
CATALOG = LIB / "catalog.json"
TMP = ROOT / ".tmp-books" / "pd"
MAX_CHARS = 42000
NOTA_COMPLETO = "completo · dominio público"

def clean_text(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = s.replace("¬\n", "").replace("¬", "").replace("\xad", "")
    s = re.sub(r"([A-Za-zÁÉÍÓÚáéíóúñÑüÜ])-\n([a-záéíóúñü])", r"\1\2", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()

def paras(s: str) -> str:
    s = clean_text(s)
    parts, buf = [], []
    for line in s.split("\n"):
        if not line.strip():
            if buf:
                parts.append(" ".join(buf))
                buf = []
        else:
            buf.append(line.strip())
    if buf:
        parts.append(" ".join(buf))
    return "\n\n".join(p for p in parts if p.strip())

def strip_pg(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    m = re.search(r"\*\*\*\s*START OF (?:THE |THIS )?PROJECT GUTENBERG EBOOK[^*\n]*\*\*\*", text, re.I)
    if m:
        text = text[m.end():]
    m = re.search(r"\*\*\*\s*END OF (?:THE |THIS )?PROJECT GUTENBERG EBOOK", text, re.I)
    if m:
        text = text[:m.start()]
    return text.strip()

def pack_chunks(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Split at paragraph boundaries into ~max_chars chunks."""
    text = paras(text)
    if len(text) <= max_chars:
        return [text]
    chunks = []
    rest = text
    while rest:
        if len(rest) <= max_chars:
            chunks.append(rest.strip())
            break
        cut = rest[:max_chars]
        sp = cut.rfind("\n\n")
        if sp < max_chars * 0.5:
            sp = max_chars
        chunk = rest[:sp].strip()
        if chunk:
            chunks.append(chunk)
        rest = rest[sp:].lstrip()
    return chunks

def write_book(bid, titulo, autor, nota, categoria, texto, idioma="es"):
    texto = clean_text(texto)
    if len(texto) > MAX_CHARS + 500:
        texto = texto[:MAX_CHARS]
        sp = texto.rfind("\n\n")
        if sp > MAX_CHARS * 0.6:
            texto = texto[:sp]
        texto = texto.strip()
    data = {
        "id": bid,
        "titulo": titulo,
        "autor": autor,
        "nota": nota,
        "categoria": categoria,
        "idioma": idioma,
        "texto": texto,
        "inline": True,
    }
    (LIB / f"{bid}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  + {bid} ({len(texto)} chars) {titulo}")
    return {
        "id": bid,
        "titulo": titulo,
        "autor": autor,
        "nota": nota,
        "categoria": categoria,
        "idioma": idioma,
    }

def upsert_catalog(metas: list[dict], remove_ids: set[str] | None = None):
    cat = json.loads(CATALOG.read_text(encoding="utf-8"))
    remove_ids = remove_ids or set()
    by_id = {m["id"]: i for i, m in enumerate(cat)}
    # remove obsolete
    if remove_ids:
        cat = [m for m in cat if m["id"] not in remove_ids]
        by_id = {m["id"]: i for i, m in enumerate(cat)}
    for meta in metas:
        entry = {
            "id": meta["id"],
            "titulo": meta["titulo"],
            "autor": meta["autor"],
            "nota": meta["nota"],
            "categoria": meta["categoria"],
            "idioma": meta.get("idioma", "es"),
        }
        if meta["id"] in by_id:
            cat[by_id[meta["id"]]] = entry
        else:
            cat.append(entry)
            by_id[meta["id"]] = len(cat) - 1
    CATALOG.write_text(json.dumps(cat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"catalog entries: {len(cat)}")

def pack_multipart(base_id, titulo_base, autor, nota, text, categoria="narrativa",
                   existing_suffixes=None):
    """Create base_id, base_id-2, base_id-3... or custom suffixes."""
    chunks = pack_chunks(text)
    metas = []
    n = len(chunks)
    for i, chunk in enumerate(chunks):
        if i == 0:
            bid = base_id
            # keep simple first id
        else:
            bid = f"{base_id}-{i+1}"
        if n == 1:
            tit = titulo_base
        else:
            tit = f"{titulo_base} · parte {i+1}/{n}"
        metas.append(write_book(bid, tit, autor, nota, categoria, chunk))
    return metas, {f"{base_id}-{k}" for k in range(n+2, n+50)}  # noop

# ── Clarín ──────────────────────────────────────────────
def pack_clarin():
    print("=== Clarín ¡Adiós, Cordera! ===")
    h = (TMP / "clarin.html").read_text(encoding="utf-8", errors="replace")
    m = re.search(r'<div class="mw-parser-output">(.*?)(?:<div class="printfooter"|<noscript)', h, re.S)
    if not m:
        raise SystemExit("clarin html parse fail")
    body = m.group(1)
    # drop nav/header tables
    body = re.sub(r"(?is)<table[^>]*>.*?</table>", "", body)
    body = re.sub(r"(?is)<div[^>]*class=\"[^\"]*(?:sisterproject|catlinks|mw-editsection)[^\"]*\"[^>]*>.*?</div>", "", body)
    body = re.sub(r"(?is)<script.*?</script>", "", body)
    body = re.sub(r"(?is)<style.*?</style>", "", body)
    body = re.sub(r"(?is)<br\s*/?>", "\n", body)
    body = re.sub(r"(?is)</p>", "\n\n", body)
    body = re.sub(r"(?is)</h[1-6]>", "\n\n", body)
    body = re.sub(r"(?is)<[^>]+>", "", body)
    body = htmlmod.unescape(body).replace("\xa0", " ")
    text = paras(body)
    # trim wiki chrome
    lines = []
    started = False
    for p in text.split("\n\n"):
        if not started:
            if "¡Adiós, Cordera!" in p and len(p) < 80:
                started = True
                continue
            if p.startswith("Había en el prao") or "Había en un prao" in p or "prado una vaca" in p.lower() or "Había en el prao" in p:
                started = True
                lines.append(p)
                continue
            if "Wikisource" in p or "mw-parser" in p or "Descargar" in p or len(p) < 40:
                continue
            # sometimes story starts without exact match
            if "vaca" in p.lower() and ("prado" in p.lower() or "prao" in p.lower()):
                started = True
                lines.append(p)
                continue
            continue
        if "Categoría:" in p or "Licencia" in p:
            break
        lines.append(p)
    text = "\n\n".join(lines).strip()
    if len(text) < 5000:
        # fallback: take longest stretch
        text = paras(body)
        # cut before Categoría
        cut = text.find("Categoría:")
        if cut > 0:
            text = text[:cut].strip()
        # drop leading chrome until first long para
        ps = text.split("\n\n")
        out = []
        for p in ps:
            if not out and (len(p) < 100 or "Wikisource" in p or "Descargar" in p or "De Wikisource" in p):
                continue
            out.append(p)
        text = "\n\n".join(out)
    if not text.startswith("¡Adiós"):
        text = "¡Adiós, Cordera!\n\n" + text
    nota = f"1892 · {NOTA_COMPLETO} · Wikisource ES (Clarín †1901)"
    meta = write_book(
        "clarin",
        "¡Adiós, Cordera!",
        "Leopoldo Alas «Clarín»",
        nota,
        "narrativa",
        text,
    )
    return [meta]

# ── Quijote ─────────────────────────────────────────────
def pack_quijote():
    print("=== Don Quijote (PG 2000) ===")
    raw = (TMP / "pg2000.txt").read_text(encoding="utf-8", errors="replace")
    text = strip_pg(raw)
    # start at Primera parte / Capítulo primero
    m = re.search(r"Capítulo primero\. Que trata de la condición", text)
    if not m:
        m = re.search(r"Que trata de la condición y ejercicio del famoso", text)
    if m:
        text = text[m.start():]
    text = paras(text)
    nota = f"1605–1615 · {NOTA_COMPLETO} · Project Gutenberg #2000"
    chunks = pack_chunks(text)
    metas = []
    # Remove old quijote-8 only-chapter; use quijote-1..N
    n = len(chunks)
    for i, chunk in enumerate(chunks):
        bid = f"quijote-{i+1}"
        tit = f"Don Quijote · parte {i+1}/{n}"
        metas.append(write_book(bid, tit, "Miguel de Cervantes", nota, "narrativa", chunk))
    return metas

# ── Galdós Doña Perfecta ────────────────────────────────
def pack_galdos():
    print("=== Doña Perfecta (PG 15725 ES body) ===")
    raw = (TMP / "pg15725.txt").read_text(encoding="utf-8", errors="replace")
    # Spanish novel between third title and NOTES
    starts = [m.start() for m in re.finditer("DOÑA PERFECTA", raw)]
    start = starts[2] if len(starts) >= 3 else raw.find("Villahorrenda")
    notes = raw.find("                                   NOTES")
    if notes < 0:
        notes = raw.find("\nNOTES\n")
    body = raw[start:notes if notes > start else None]
    # unwrap student-edition indentation / page numbers
    lines = []
    for line in body.splitlines():
        # drop lone page numbers
        if re.match(r"^\s*\d+\s*$", line):
            continue
        # drop leading indent spaces typical of this edition
        line = re.sub(r"^ {5}", "", line)
        # remove =emphasis= markers
        line = line.replace("=", "")
        lines.append(line)
    text = paras("\n".join(lines))
    # drop trailing English apparatus if any leaked
    for stop in ["NOTES", "VOCABULARY", "Page =1="]:
        idx = text.find(stop)
        if idx > len(text) * 0.7:
            text = text[:idx].strip()
    nota = f"1876 · {NOTA_COMPLETO} · PG #15725 (texto español; ed. Marsh)"
    chunks = pack_chunks(text)
    metas = []
    n = len(chunks)
    for i, chunk in enumerate(chunks):
        bid = "galdos" if i == 0 else f"galdos-{i+1}"
        tit = f"Doña Perfecta · parte {i+1}/{n}" if n > 1 else "Doña Perfecta"
        metas.append(write_book(bid, tit, "Benito Pérez Galdós", nota, "narrativa", chunk))
    return metas

# ── Montecristo ─────────────────────────────────────────
def pack_montecristo():
    print("=== El Conde de Montecristo (IA DjVuTXT PD) ===")
    raw = (TMP / "monte-djvu.txt").read_text(encoding="utf-8", errors="replace")
    # start at first real chapter
    m = re.search(r"Capítulo primero\s*\n\s*Marsella", raw, re.I)
    if not m:
        m = re.search(r"Capítulo primero", raw, re.I)
    if m:
        raw = raw[m.start():]
    # light OCR cleanup
    raw = raw.replace("poiq", "porque")  # common OCR - careful only if wrong
    # don't do aggressive word replacement - keep OCR as-is except hyphenation
    text = paras(raw)
    nota = (
        f"1844–46 · {NOTA_COMPLETO} · trad. esp. s. XIX "
        f"(Archive.org alejadrodumaselcondedemontecristo · DjVuTXT)"
    )
    chunks = pack_chunks(text)
    metas = []
    n = len(chunks)
    for i, chunk in enumerate(chunks):
        bid = "montecristo" if i == 0 else f"montecristo-{i+1}"
        tit = f"El conde de Montecristo · parte {i+1}/{n}"
        metas.append(write_book(bid, tit, "Alexandre Dumas", nota, "narrativa", chunk))
    return metas

def main():
    all_metas = []
    all_metas += pack_clarin()
    all_metas += pack_quijote()
    all_metas += pack_galdos()
    all_metas += pack_montecristo()
    # remove obsolete single-chapter quijote-8 if beyond new count
    quijote_ids = {m["id"] for m in all_metas if m["id"].startswith("quijote-")}
    remove = set()
    # if old quijote-8 not in new set, remove it
    if "quijote-8" not in quijote_ids:
        remove.add("quijote-8")
    upsert_catalog(all_metas, remove_ids=remove)
    print(f"DONE metas={len(all_metas)}")

if __name__ == "__main__":
    main()
