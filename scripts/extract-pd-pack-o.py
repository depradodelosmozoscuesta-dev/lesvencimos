#!/usr/bin/env python3
"""Build Verne/adventure + religión PD chapter packs for biblioteca-libros."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "modulos" / "biblioteca-libros"
TMP = ROOT / ".tmp-books"
CATALOG = LIB / "catalog.json"
MAX_CHARS = 42000  # like Odisea chapter packs

def strip_pg(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    m = re.search(r"\*\*\*\s*START OF (?:THE |THIS )?PROJECT GUTENBERG EBOOK[^*\n]*\*\*\*", text, re.I)
    if m:
        text = text[m.end():]
    m = re.search(r"\*\*\*\s*END OF (?:THE |THIS )?PROJECT GUTENBERG EBOOK", text, re.I)
    if m:
        text = text[:m.start()]
    return text.strip()

def clean_text(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = s.replace("¬\n", "").replace("¬", "")
    s = s.replace("\xad", "")
    s = re.sub(r"([A-Za-zÁÉÍÓÚáéíóúñÑüÜ])-\n([a-záéíóúñü])", r"\1\2", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()

def paras(s: str) -> str:
    """Normalize into paragraph-separated text."""
    s = clean_text(s)
    # collapse single newlines inside paragraphs
    parts = []
    buf = []
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

def find_chapters(text: str, patterns: list[str]):
    """Return list of (title, start, end) chapter slices."""
    starts = []
    for pat in patterns:
        for m in re.finditer(pat, text, re.M):
            title = re.sub(r"\s+", " ", m.group(0)).strip()
            starts.append((m.start(), title))
    starts.sort(key=lambda x: x[0])
    # de-dupe near-identical starts
    uniq = []
    for st, title in starts:
        if uniq and st - uniq[-1][0] < 40:
            continue
        uniq.append((st, title))
    out = []
    for i, (st, title) in enumerate(uniq):
        end = uniq[i + 1][0] if i + 1 < len(uniq) else len(text)
        out.append((title, st, end))
    return out

def take_chapters(text: str, chapters, n: int, max_chars: int = MAX_CHARS):
    chosen = chapters[:n]
    if not chosen:
        body = paras(text[:max_chars])
        return body[:max_chars]
    start = chosen[0][1]
    end = chosen[-1][2]
    body = paras(text[start:end])
    if len(body) > max_chars:
        # trim at paragraph
        cut = body[:max_chars]
        sp = cut.rfind("\n\n")
        if sp > max_chars * 0.6:
            cut = cut[:sp]
        body = cut.strip() + "\n\n[…continúa en la fuente PD…]"
    return body

def write_book(bid: str, titulo: str, autor: str, nota: str, categoria: str, texto: str):
    texto = clean_text(texto)
    if len(texto) > MAX_CHARS + 2000:
        texto = texto[:MAX_CHARS]
        sp = texto.rfind("\n\n")
        if sp > MAX_CHARS * 0.6:
            texto = texto[:sp]
        texto = texto.strip() + "\n\n[…continúa en la fuente PD…]"
    data = {
        "id": bid,
        "titulo": titulo,
        "autor": autor,
        "nota": nota,
        "categoria": categoria,
        "texto": texto,
        "inline": True,
    }
    (LIB / f"{bid}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  + {bid} ({len(texto)} chars) [{categoria}] {titulo}")
    return {
        "id": bid,
        "titulo": titulo,
        "autor": autor,
        "nota": nota,
        "categoria": categoria,
    }

def wiki_plain(wikitext: str) -> str:
    t = wikitext
    # drop templates encabezado
    t = re.sub(r"\{\{encabezado[\s\S]*?\}\}", "", t)
    t = re.sub(r"\{\{t2\|([^}]+)\}\}", r"\1", t)
    t = re.sub(r"\{\{[^}]+\}\}", "", t)
    t = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", t)
    t = re.sub(r"'{2,}", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    return paras(t)

def build_verne():
    print("=== Verne ===")
    meta = []
    # Spanish Viaje 1-6 from Wikisource JSON
    parts = []
    for i in range(1, 7):
        p = TMP / "verne" / "es" / f"viaje-cap{i}.json"
        if not p.exists():
            # also check wrong path from earlier
            p2 = TMP / "verne" / f"viaje-cap{i}.json"
            p = p2 if p2.exists() else p
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        wt = d.get("parse", {}).get("wikitext", {}).get("*", "")
        plain = wiki_plain(wt)
        parts.append(f"Capítulo {i}\n\n{plain}")
    if parts:
        meta.append(write_book(
            "verne-viaje-es",
            "Viaje al centro de la Tierra · Cap. I–VI",
            "Julio Verne",
            "trad. esp. PD (Wikisource) · Ribot y Fontseré †1871 · dominio público",
            "narrativa",
            "\n\n".join(parts),
        ))

    specs = [
        ("pg3748.txt", "verne-viaje-en", "Journey to the Interior of the Earth · Ch. I–IV",
         "Jules Verne", "1871 · Malleson · PD · English · Gutenberg #3748",
         [r"(?m)^CHAPTER\s+[IVXLC]+\.?.*"], 4),
        ("pg164.txt", "verne-leguas", "Twenty Thousand Leagues · Ch. I–IV",
         "Jules Verne", "1870 · PD · English · Gutenberg #164",
         [r"(?m)^CHAPTER\s+[IVXLC]+\b.*"], 4),
        ("pg103.txt", "verne-mundo80", "Around the World in Eighty Days · Ch. I–V",
         "Jules Verne", "1873 · PD · English · Gutenberg #103",
         [r"(?m)^CHAPTER\s+[IVXLC]+\.?.*"], 5),
        ("pg83.txt", "verne-luna", "From the Earth to the Moon · Ch. I–V",
         "Jules Verne", "1865 · PD · English · Gutenberg #83",
         [r"(?m)^CHAPTER\s+[IVXLC]+\.?.*"], 5),
        ("pg1268.txt", "verne-isla", "The Mysterious Island · Ch. 1–4",
         "Jules Verne", "1874 · PD · English · Gutenberg #1268",
         [r"(?m)^Chapter\s+\d+\b.*"], 4),
        ("pg1842.txt", "verne-strogoff", "Michael Strogoff · Ch. I–IV",
         "Jules Verne", "1876 · PD · English · Gutenberg #1842",
         [r"(?m)^CHAPTER\s+[IVXLC]+\.?.*"], 4),
    ]
    for fname, bid, titulo, autor, nota, pats, n in specs:
        path = TMP / "verne" / fname
        if not path.exists():
            print("  missing", path)
            continue
        text = strip_pg(path.read_text(encoding="utf-8", errors="replace"))
        ch = find_chapters(text, pats)
        body = take_chapters(text, ch, n)
        meta.append(write_book(bid, titulo, autor, nota, "narrativa", body))

    # Fix mislabeled leguas.json → keep as alias to mundo content was wrong; overwrite leguas with real 20k
    # Keep id "leguas" for catalog continuity but point to real leagues excerpt
    path = TMP / "verne" / "pg164.txt"
    if path.exists():
        text = strip_pg(path.read_text(encoding="utf-8", errors="replace"))
        ch = find_chapters(text, [r"(?m)^CHAPTER\s+[IVXLC]+\b.*"])
        body = take_chapters(text, ch, 3)
        meta.append(write_book(
            "leguas",
            "20,000 Leagues Under the Sea · Ch. I–III",
            "Jules Verne",
            "1870 · PD · English · Gutenberg #164 (corregido: antes mal etiquetado)",
            "narrativa",
            body,
        ))
    return meta

def build_adventure():
    print("=== Adventure ===")
    meta = []
    specs = [
        ("adv/pg829.txt", "gulliver", "Gulliver's Travels · Part I Ch. I–III",
         "Jonathan Swift", "1726 · PD · English · Gutenberg #829",
         [r"(?m)^CHAPTER\s+[IVXLC]+\.?.*"], 3),
        ("adv/pg521.txt", "crusoe", "Robinson Crusoe · Ch. I–II",
         "Daniel Defoe", "1719 · PD · English · Gutenberg #521",
         [r"(?m)^CHAPTER\s+[IVXLC]+\.?.*"], 2),
        ("adv/pg19942.txt", "candide", "Candide · Ch. I–VI",
         "Voltaire", "1759 · PD · English · Gutenberg #19942",
         [r"(?m)^CHAPTER\s+[IVXLC\d]+\.?.*", r"(?m)^I{1,3}\.\s+\S+"], 6),
        ("adv/pg696.txt", "otranto", "The Castle of Otranto · Ch. I–II",
         "Horace Walpole", "1764 · PD · English · Gothic · Gutenberg #696",
         [r"(?m)^CHAPTER\s+[IVXLC]+\.?.*"], 2),
        ("adv/pg421.txt", "kidnapped", "Kidnapped · Ch. I–III",
         "Robert Louis Stevenson", "1886 · PD · English · Gutenberg #421",
         [r"(?m)^CHAPTER\s+[IVXLC]+\b.*"], 3),
        ("adv/pg35.txt", "timemachine", "The Time Machine · Ch. I–III",
         "H. G. Wells", "1895 · PD · English · Gutenberg #35",
         [r"(?m)^CHAPTER\s+[IVXLC\d]+\.?.*", r"(?m)^I{0,3}V?I{0,3}\n"], 3),
        ("adv/pg5230.txt", "invisible", "The Invisible Man · Ch. I–IV",
         "H. G. Wells", "1897 · PD · English · Gutenberg #5230",
         [r"(?m)^CHAPTER\s+[IVXLC]+\.?.*"], 4),
        ("adv/pg34206.txt", "arabian", "Thousand and One Nights · Prologue & early tales",
         "Anonymous (Burton / PD ed.)", "Vol. I · PD · English · Gutenberg #34206",
         [r"(?m)^THE\s+[A-Z][A-Z \-']{4,60}$", r"(?m)^Story of\b.*"], 4),
    ]
    for fname, bid, titulo, autor, nota, pats, n in specs:
        path = TMP / fname
        if not path.exists():
            print("  missing", path)
            continue
        text = strip_pg(path.read_text(encoding="utf-8", errors="replace"))
        ch = find_chapters(text, pats)
        if len(ch) < 2:
            # fallback: first max_chars of body
            body = paras(text)[:MAX_CHARS]
            sp = body.rfind("\n\n")
            if sp > MAX_CHARS * 0.5:
                body = body[:sp]
        else:
            body = take_chapters(text, ch, n)
        meta.append(write_book(bid, titulo, autor, nota, "narrativa", body))
    return meta

def build_religion():
    print("=== Religión ===")
    meta = []
    # RV1909 from es_rvr.json
    bible_path = TMP / "relig" / "es_rvr.json"
    data = json.loads(bible_path.read_text(encoding="utf-8-sig"))
    by_ab = {b["abbrev"]: b for b in data}

    def book_text(abbrev: str, chap_from: int = 1, chap_to: int | None = None, header: str = "") -> str:
        b = by_ab[abbrev]
        chaps = b["chapters"]
        end = chap_to or len(chaps)
        parts = []
        if header:
            parts.append(header)
        for i in range(chap_from - 1, min(end, len(chaps))):
            verses = chaps[i]
            block = f"Capítulo {i + 1}\n\n" + "\n\n".join(f"{j+1} {v}" for j, v in enumerate(verses))
            parts.append(block)
        return "\n\n".join(parts)

    # AT packs
    meta.append(write_book(
        "biblia-at-genesis",
        "Biblia · Génesis 1–11 (RV 1909)",
        "Biblia (Reina-Valera 1909)",
        "Antiguo Testamento · Reina-Valera 1909 · dominio público",
        "religion",
        book_text("gn", 1, 11, "Génesis"),
    ))
    meta.append(write_book(
        "biblia-at-exodo",
        "Biblia · Éxodo 1–14 (RV 1909)",
        "Biblia (Reina-Valera 1909)",
        "Antiguo Testamento · Reina-Valera 1909 · dominio público",
        "religion",
        book_text("ex", 1, 14, "Éxodo"),
    ))
    meta.append(write_book(
        "biblia-at-salmos",
        "Biblia · Salmos 1–41 (RV 1909)",
        "Biblia (Reina-Valera 1909)",
        "Antiguo Testamento · Reina-Valera 1909 · dominio público",
        "religion",
        book_text("ps", 1, 41, "Salmos · Libro I"),
    ))
    meta.append(write_book(
        "biblia-at-isaias",
        "Biblia · Isaías 1–12 (RV 1909)",
        "Biblia (Reina-Valera 1909)",
        "Antiguo Testamento · Reina-Valera 1909 · dominio público",
        "religion",
        book_text("is", 1, 12, "Isaías"),
    ))
    # NT packs
    meta.append(write_book(
        "biblia-nt-mateo",
        "Biblia · Evangelio según Mateo 1–14 (RV 1909)",
        "Biblia (Reina-Valera 1909)",
        "Nuevo Testamento · Reina-Valera 1909 · dominio público",
        "religion",
        book_text("mt", 1, 14, "Evangelio según San Mateo"),
    ))
    meta.append(write_book(
        "biblia-nt-juan",
        "Biblia · Evangelio según Juan (RV 1909)",
        "Biblia (Reina-Valera 1909)",
        "Nuevo Testamento · Reina-Valera 1909 · dominio público",
        "religion",
        book_text("jo", 1, None, "Evangelio según San Juan"),
    ))
    meta.append(write_book(
        "biblia-nt-hechos",
        "Biblia · Hechos 1–12 (RV 1909)",
        "Biblia (Reina-Valera 1909)",
        "Nuevo Testamento · Reina-Valera 1909 · dominio público",
        "religion",
        book_text("act", 1, 12, "Hechos de los Apóstoles"),
    ))
    meta.append(write_book(
        "biblia-nt-apocalipsis",
        "Biblia · Apocalipsis (RV 1909)",
        "Biblia (Reina-Valera 1909)",
        "Nuevo Testamento · Reina-Valera 1909 · dominio público",
        "religion",
        book_text("re", 1, None, "Apocalipsis de San Juan"),
    ))
    # Keep/expand stub reina as Salmo 23 still
    meta.append(write_book(
        "reina",
        "Biblia · Salmo 23 (RV 1909)",
        "Biblia (Reina-Valera 1909)",
        "Salmo 23 · Reina-Valera 1909 · dominio público",
        "religion",
        book_text("ps", 23, 23, "Salmo 23"),
    ))

    # KJV companion for English readers (Genesis + Matthew samples)
    kjv = strip_pg((TMP / "relig" / "kjv.txt").read_text(encoding="utf-8", errors="replace"))
    # crude: take from Genesis to end of chapter markers
    ch = find_chapters(kjv, [r"(?m)^Book of Genesis\b", r"(?m)^The First Book of Moses.*", r"(?m)^Genesis\b"])
    # Better: Project Gutenberg KJV uses "Book of Genesis" etc.
    # Just extract a readable window after "Book of Genesis"
    m = re.search(r"(?m)^The First Book of Moses.*Called Genesis\.?\s*$", kjv)
    if not m:
        m = re.search(r"Book of Genesis", kjv)
    if m:
        chunk = kjv[m.start(): m.start() + 35000]
        # stop before next book if present
        nxt = re.search(r"(?m)^The Second Book of Moses", chunk)
        if nxt:
            chunk = chunk[:nxt.start()]
        meta.append(write_book(
            "biblia-kjv-genesis",
            "Bible · Genesis 1– (KJV)",
            "Bible (King James Version)",
            "1611/1769 · PD · English · Gutenberg #10",
            "religion",
            paras(chunk),
        ))

    # Quran Rodwell — split by sura
    qpath = TMP / "relig" / "quran_rodwell.txt"
    q = strip_pg(qpath.read_text(encoding="utf-8", errors="replace"))
    suras = find_chapters(q, [r"(?m)^SURA\s+[IVXLC\d]+.*", r"(?m)^Sura\s+[IVXLC\d]+.*"])
    if not suras:
        suras = find_chapters(q, [r"(?m)^[IVXLC]+\.\s+[A-Z].{0,60}$"])
    print("  quran suras found", len(suras))
    if suras:
        # pack 1: first ~12 suras
        body = take_chapters(q, suras, min(12, len(suras)), max_chars=38000)
        meta.append(write_book(
            "coran-1",
            "The Koran · Suras I–XII (Rodwell)",
            "Qur'an · J. M. Rodwell trans.",
            "1861 · PD · English · Gutenberg #2800",
            "religion",
            body,
        ))
        if len(suras) > 12:
            # another pack mid
            mid = suras[12:24]
            start = mid[0][1]
            end = mid[-1][2]
            body = paras(q[start:end])
            meta.append(write_book(
                "coran-2",
                "The Koran · Suras XIII–XXIV (Rodwell)",
                "Qur'an · J. M. Rodwell trans.",
                "1861 · PD · English · Gutenberg #2800",
                "religion",
                body,
            ))
    else:
        meta.append(write_book(
            "coran-1",
            "The Koran · opening (Rodwell)",
            "Qur'an · J. M. Rodwell trans.",
            "1861 · PD · English · Gutenberg #2800",
            "religion",
            paras(q)[:35000],
        ))

    # Hindu / Tao / Buddhist / Confucian
    gita = strip_pg((TMP / "relig" / "gita.txt").read_text(encoding="utf-8", errors="replace"))
    meta.append(write_book(
        "gita",
        "Bhagavad-Gîtâ · Song Celestial (extract)",
        "from the Mahâbhârata · Arnold trans.",
        "1885 · PD · English · Gutenberg #2388",
        "religion",
        paras(gita)[:38000],
    ))

    upa = strip_pg((TMP / "relig" / "upanishads.txt").read_text(encoding="utf-8", errors="replace"))
    meta.append(write_book(
        "upanishads",
        "The Upanishads · selections",
        "Vedanta · Max Müller / PD ed.",
        "PD · English · Gutenberg #3283",
        "religion",
        paras(upa)[:38000],
    ))

    tao = strip_pg((TMP / "relig" / "tao.txt").read_text(encoding="utf-8", errors="replace"))
    meta.append(write_book(
        "tao",
        "Tao Teh King (Tao Te Ching)",
        "Laozi · James Legge trans.",
        "1891 · PD · English · Gutenberg #216",
        "religion",
        paras(tao)[:38000],
    ))

    dham = strip_pg((TMP / "relig" / "dhamma.txt").read_text(encoding="utf-8", errors="replace"))
    meta.append(write_book(
        "dhammapada",
        "Dhammapada · selections",
        "Buddhist canon · Max Müller trans.",
        "PD · English · Gutenberg #2017",
        "religion",
        paras(dham)[:38000],
    ))

    anal = strip_pg((TMP / "relig" / "analects.txt").read_text(encoding="utf-8", errors="replace"))
    meta.append(write_book(
        "analects",
        "Analects of Confucius · selections",
        "Confucius · Legge trans.",
        "PD · English · Gutenberg #3330",
        "religion",
        paras(anal)[:38000],
    ))
    return meta

def clean_mosqueteros():
    print("=== Clean Mosqueteros OCR ¬ ===")
    for p in sorted(LIB.glob("mosqueteros-*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        before = d.get("texto", "")
        after = clean_text(before)
        if after != before:
            d["texto"] = after
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"  cleaned {p.name}: {before.count('¬')} ¬ removed, {len(after)} chars")
        else:
            print(f"  ok {p.name}")

def merge_catalog(new_entries: list[dict]):
    cat = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in cat}
    for e in new_entries:
        by_id[e["id"]] = {k: e[k] for k in ("id", "titulo", "autor", "nota", "categoria")}
    # drop lotr if any
    for bad in list(by_id):
        if "lotr" in bad or "tolkien" in bad or "hobbit" in bad:
            del by_id[bad]
    out = sorted(by_id.values(), key=lambda x: (x.get("categoria", ""), x["titulo"].lower()))
    CATALOG.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"catalog entries: {len(out)}")

def main():
    clean_mosqueteros()
    entries = []
    entries += build_verne()
    entries += build_adventure()
    entries += build_religion()
    merge_catalog(entries)

if __name__ == "__main__":
    main()
