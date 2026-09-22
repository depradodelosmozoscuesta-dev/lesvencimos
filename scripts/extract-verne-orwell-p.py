#!/usr/bin/env python3
"""Pack Spanish Verne (PD) + Orwell 1984 EN (PD-EU) for biblioteca v20260922p."""
from __future__ import annotations
import html as htmlmod
import json, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "modulos" / "biblioteca-libros"
TMP = ROOT / ".tmp-books"
CATALOG = LIB / "catalog.json"
MAX_CHARS = 42000

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
                parts.append(" ".join(buf)); buf = []
        else:
            buf.append(line.strip())
    if buf:
        parts.append(" ".join(buf))
    return "\n\n".join(p for p in parts if p.strip())

def trim_body(body: str, max_chars: int = MAX_CHARS) -> str:
    body = clean_text(body)
    if len(body) <= max_chars:
        return body
    cut = body[:max_chars]
    sp = cut.rfind("\n\n")
    if sp > max_chars * 0.6:
        cut = cut[:sp]
    return cut.strip() + "\n\n[…continúa en la fuente PD…]"

def write_book(bid, titulo, autor, nota, categoria, texto):
    texto = trim_body(texto)
    data = {
        "id": bid, "titulo": titulo, "autor": autor,
        "nota": nota, "categoria": categoria,
        "texto": texto, "inline": True,
    }
    (LIB / f"{bid}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  + {bid} ({len(texto)} chars) {titulo}")
    return {"id": bid, "titulo": titulo, "autor": autor, "nota": nota, "categoria": categoria}

def wiki_plain(wikitext: str) -> str:
    t = wikitext
    t = re.sub(r"\{\{[Ee]ncabezado[\s\S]*?\}\}", "", t)
    t = re.sub(r"\{\{t2\|([^}]+)\}\}", r"\1", t)
    t = re.sub(r"\{\{[^}]+\}\}", "", t)
    t = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", t)
    t = re.sub(r"'{2,}", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"(?m)^(cs|en|fr|pl|de|it|pt):.+$", "", t)
    t = re.sub(r"(?m)^Viaje al centro de la Tierra: Capítulo \d+\s*$", "", t)
    return paras(t)

def html_to_text(s: str) -> str:
    s = re.sub(r"(?is)<script[^>]*>.*?</script>", "", s)
    s = re.sub(r"(?is)<style[^>]*>.*?</style>", "", s)
    s = re.sub(r"(?is)<br\s*/?>", "\n", s)
    s = re.sub(r"(?is)</p>", "\n\n", s)
    s = re.sub(r"(?is)</h[1-6]>", "\n\n", s)
    s = re.sub(r"(?is)<[^>]+>", "", s)
    s = htmlmod.unescape(s).replace("\xa0", " ")
    return paras(s)

def epub_chapters(epub_path: Path, name_re: str, limit: int):
    z = zipfile.ZipFile(epub_path)
    names = sorted(n for n in z.namelist() if re.search(name_re, n) and n.endswith((".xhtml", ".html")))
    out = []
    for n in names[:limit]:
        raw = z.read(n).decode("utf-8", "replace")
        hs = re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", raw, re.I | re.S)
        title = re.sub(r"<[^>]+>", "", hs[0]).strip() if hs else Path(n).stem
        title = htmlmod.unescape(title)
        body = html_to_text(raw)
        if body.startswith(title):
            body = body[len(title):].lstrip()
        out.append((title, body))
    return out

def pack_from_clean(path: Path, patterns, n):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"(?m)^Cap[ií]tulo\b", text)
    if m:
        text = text[m.start():]
    starts = []
    for pat in patterns:
        for mm in re.finditer(pat, text, re.M):
            title = re.sub(r"\s+", " ", mm.group(0)).strip()
            starts.append((mm.start(), title))
    starts.sort(key=lambda x: x[0])
    uniq = []
    for st, title in starts:
        if uniq and st - uniq[-1][0] < 40:
            continue
        uniq.append((st, title))
    chosen = uniq[:n]
    if not chosen:
        return paras(text[:MAX_CHARS]), 0
    start = chosen[0][0]
    end = uniq[n][0] if len(uniq) > n else len(text)
    return paras(text[start:end]), len(chosen)

def load_ws_caps(dirpath: Path, pattern: str, label_fn):
    files = sorted(dirpath.glob(pattern))
    parts = []
    for p in files:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            wt = d["parse"]["wikitext"]["*"]
        except Exception:
            continue
        if len(wt) < 400 or "<pages " in wt[:80]:
            continue
        plain = wiki_plain(wt)
        if len(plain) < 200:
            continue
        parts.append(label_fn(p) + "\n\n" + plain)
    return parts

def build():
    metas = []
    es_ia = TMP / "verne" / "es-ia"
    es_ws = TMP / "verne" / "es"
    print("=== Verne ES ===")

    # Viaje Wikisource Ribot
    parts = load_ws_caps(
        es_ws, "viaje-cap*.json",
        lambda p: "Capítulo " + re.search(r"(\d+)", p.stem).group(1),
    )
    # natural order
    def vkey(s):
        m = re.search(r"Capítulo (\d+)", s)
        return int(m.group(1)) if m else 99
    parts.sort(key=vkey)
    if parts:
        mid = min(6, len(parts))
        metas.append(write_book(
            "verne-viaje-es",
            f"Viaje al centro de la Tierra · Cap. I–{mid}",
            "Julio Verne",
            "trad. esp. PD (Wikisource) · Ribot y Fontseré †1871 · dominio público",
            "narrativa", "\n\n".join(parts[:mid]),
        ))
        if len(parts) > mid:
            metas.append(write_book(
                "verne-viaje-es-2",
                f"Viaje al centro de la Tierra · Cap. {mid+1}–{len(parts)}",
                "Julio Verne",
                "trad. esp. PD (Wikisource) · Ribot y Fontseré †1871 · dominio público",
                "narrativa", "\n\n".join(parts[mid:]),
            ))

    # Leguas Guimerá
    ep = es_ia / "leguas.epub"
    if ep.exists():
        chs = epub_chapters(ep, r"Parte1Capitulo0[1-6]\.xhtml$", 6)
        body = "\n\n".join(f"Capítulo {t}\n\n{b}" for t, b in chs)
        metas.append(write_book(
            "verne-leguas-es",
            f"Veinte mil leguas de viaje submarino · Cap. 1–{len(chs)}",
            "Julio Verne",
            "trad. Vicente Guimerá †1902 · PD (Archive.org folkscanomy/epublibre) · no Bartual 1933",
            "narrativa", body,
        ))

    # Vuelta
    clean = es_ia / "vuelta_clean.txt"
    if clean.exists():
        body, n = pack_from_clean(clean, [r"(?m)^Capítulo\s+[IVXLC]+\b.*"], 6)
        metas.append(write_book(
            "verne-mundo80-es",
            f"La vuelta al mundo en ochenta días · Cap. I–{n or 6}",
            "Julio Verne",
            "trad. española clásica (Guimerá †1902 / epublibre) · PD · Archive.org",
            "narrativa", body,
        ))

    # Cinco semanas Wikisource
    roman_order = ["I", "II", "III", "IV", "V", "VI"]
    cparts = []
    for r in roman_order:
        p = es_ws / f"cinco-cap{r}.json"
        if not p.exists():
            p = es_ws / f"cinco-cap{r}.json"
        if not p.exists() and r == "I":
            p = es_ws / "cinco-cap1.json"
        if not p.exists():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            plain = wiki_plain(d["parse"]["wikitext"]["*"])
        except Exception:
            continue
        if len(plain) > 200:
            cparts.append(f"Capítulo {r}\n\n{plain}")
    if len(cparts) < 3 and (es_ia / "cinco_clean.txt").exists():
        body, n = pack_from_clean(es_ia / "cinco_clean.txt", [r"(?m)^Capítulo\s+[IVXLC]+\b.*"], 6)
        metas.append(write_book(
            "verne-cinco-es",
            f"Cinco semanas en globo · Cap. I–{n or 6}",
            "Julio Verne",
            "trad. española clásica (epublibre/folkscanomy) · PD · Archive.org",
            "narrativa", body,
        ))
    elif cparts:
        metas.append(write_book(
            "verne-cinco-es",
            f"Cinco semanas en globo · Cap. I–{len(cparts)}",
            "Julio Verne",
            "trad. esp. PD (Wikisource ES) · dominio público",
            "narrativa", "\n\n".join(cparts),
        ))

    # Luna
    if (es_ia / "luna_clean.txt").exists():
        body, n = pack_from_clean(es_ia / "luna_clean.txt", [r"(?m)^Cap[ií]tulo\s+[IVXLC]+\b.*"], 5)
        metas.append(write_book(
            "verne-luna-es",
            f"De la Tierra a la Luna · Cap. I–{n or 5}",
            "Julio Verne",
            "trad. española clásica (epublibre/folkscanomy) · PD · Archive.org",
            "narrativa", body,
        ))

    # Isla
    ep = es_ia / "isla.epub"
    if ep.exists():
        chs = epub_chapters(ep, r"parte1_00[1-4]\.xhtml$", 4)
        if chs:
            body = "\n\n".join(f"Capítulo {t}\n\n{b}" for t, b in chs)
            metas.append(write_book(
                "verne-isla-es",
                f"La isla misteriosa · Cap. 1–{len(chs)}",
                "Julio Verne",
                "trad. española clásica (epublibre/folkscanomy) · PD · Archive.org",
                "narrativa", body,
            ))

    # Strogoff
    ep = es_ia / "strogoff.epub"
    if ep.exists():
        chs = epub_chapters(ep, r"/10[1-4]\.xhtml$", 4)
        if chs:
            body = "\n\n".join(f"Capítulo {t}\n\n{b}" for t, b in chs)
            metas.append(write_book(
                "verne-strogoff-es",
                f"Miguel Strogoff · Cap. 1–{len(chs)}",
                "Julio Verne",
                "trad. española clásica (epublibre/folkscanomy) · PD · Archive.org",
                "narrativa", body,
            ))

    # Orwell 1984 EN PD-EU
    print("=== Orwell 1984 ===")
    path = TMP / "orwell" / "1984-pgau.txt"
    if not path.exists() or path.stat().st_size < 10000:
        path = TMP / "orwell" / "1984-faded.txt"
    if path.exists():
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"(?m)^PART ONE\s*$", text)
        if m:
            text = text[m.start():]
        p2 = re.search(r"(?m)^PART TWO\s*$", text)
        if p2:
            text = text[: p2.start()]
        chs = list(re.finditer(r"(?m)^Chapter\s+[IVXLC]+\b.*", text))
        n = 3
        if chs:
            st = chs[0].start()
            en = chs[n].start() if len(chs) > n else len(text)
            body = paras(text[st:en])
            label = ["I", "II", "III", "IV", "V"][min(n, len(chs)) - 1]
        else:
            body = paras(text[:MAX_CHARS]); label = "III"
        metas.append(write_book(
            "orwell-1984",
            f"Nineteen Eighty-Four · Part One, Ch. I–{label}",
            "George Orwell",
            "texto inglés de dominio público en la UE; traducción española no incluida (derechos) · Project Gutenberg Australia #0100021 (PD AU/EU; NO PD en EE.UU. hasta ~2044)",
            "narrativa", body,
        ))
    else:
        print("  SKIP 1984 — no source")

    # Catalog upsert
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_id = {e["id"]: i for i, e in enumerate(catalog)}
    for m in metas:
        entry = {k: m[k] for k in ("id", "titulo", "autor", "nota", "categoria")}
        if m["id"] in by_id:
            catalog[by_id[m["id"]]] = entry
        else:
            catalog.append(entry)
    en_map = {
        "verne-mundo80": ("Around the World in Eighty Days · Ch. I–V (EN)", "1873 · PD English · Gutenberg #103 · secundario (hay ES)"),
        "verne-luna": ("From the Earth to the Moon · Ch. I–V (EN)", "1865 · PD English · Gutenberg #83 · secundario (hay ES)"),
        "verne-viaje-en": ("Journey to the Interior of the Earth · Ch. I–IV (EN)", "1871 · Malleson · PD English · Gutenberg #3748 · secundario (hay ES)"),
        "verne-strogoff": ("Michael Strogoff · Ch. I–IV (EN)", "1876 · PD English · Gutenberg #1842 · secundario (hay ES)"),
        "verne-isla": ("The Mysterious Island · Ch. 1–4 (EN)", "1874 · PD English · Gutenberg #1268 · secundario (hay ES)"),
        "verne-leguas": ("Twenty Thousand Leagues · Ch. I–IV (EN)", "1870 · PD English · Gutenberg #164 · secundario (hay ES)"),
        "leguas": ("20,000 Leagues Under the Sea · Ch. I–III (EN)", "1870 · PD English · Gutenberg #164 · secundario (hay ES)"),
    }
    for e in catalog:
        if e["id"] in en_map:
            e["titulo"], e["nota"] = en_map[e["id"]]
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"catalog={len(catalog)} new/updated={len(metas)}")

if __name__ == "__main__":
    build()
