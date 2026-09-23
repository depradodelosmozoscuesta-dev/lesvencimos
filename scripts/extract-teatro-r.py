#!/usr/bin/env python3
"""Pack PD teatro / guiones for biblioteca v20260922r.

Prefer dialogue-friendly paragraphs for TTS. Sources: Project Gutenberg +
Ciudad Seva reprints of Golden-Age PD texts. No modern film/TV screenplays.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "modulos" / "biblioteca-libros"
TMP = ROOT / ".tmp-books" / "teatro"
CATALOG = LIB / "catalog.json"
MAX_CHARS = 42000

CATALOG_NOTE = {
    "id": "nota-teatro-guiones",
    "titulo": "Sobre teatro / guiones (aviso)",
    "autor": "Les vencimos",
    "nota": "catálogo · aviso PD",
    "categoria": "nota",
}


def clean_text(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = s.replace("¬\n", "").replace("¬", "").replace("\xad", "")
    s = re.sub(r"([A-Za-zÁÉÍÓÚáéíóúñÑüÜ])-\n([a-záéíóúñü])", r"\1\2", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()


def strip_pg(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    m = re.search(r"\*\*\*\s*START OF (?:THE |THIS )?PROJECT GUTENBERG EBOOK[^*\n]*\*\*\*", text, re.I)
    if m:
        text = text[m.end() :]
    m = re.search(r"\*\*\*\s*END OF (?:THE |THIS )?PROJECT GUTENBERG EBOOK", text, re.I)
    if m:
        text = text[: m.start()]
    return text.strip()


def dialogue_blocks(s: str) -> str:
    """Keep speaker turns as short paragraphs (TTS-friendly)."""
    s = clean_text(s)
    lines = [ln.rstrip() for ln in s.split("\n")]
    parts: list[str] = []
    buf: list[str] = []

    speaker_re = re.compile(
        r"^(?:"
        r"[A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜa-záéíóúñü\.\'’\- ]{0,40}[.:,]\s*$"  # COMENDADOR. / Hamlet.
        r"|[A-ZÁÉÍÓÚÑÜ]{2,}(?:\s+[A-ZÁÉÍÓÚÑÜ]{2,}){0,3}\s*$"  # ALL CAPS name
        r"|D\.\s*[A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜa-záéíóúñü\. ]{0,30}\s*$"  # D. CÁRL.
        r"|_[^_]{2,60}_\s*$"  # stage direction italic line
        r"|\([^)]{3,80}\)\s*$"  # (Salen…)
        r")"
    )

    def flush():
        nonlocal buf
        if buf:
            parts.append(" ".join(x.strip() for x in buf if x.strip()))
            buf = []

    for ln in lines:
        if not ln.strip():
            flush()
            continue
        raw = ln.strip()
        # verse indent lines that continue speech
        if speaker_re.match(raw) or re.match(r"^\([_A-Za-zÁÉÍÓÚáéíóú].{2,90}\)$", raw):
            flush()
            parts.append(raw)
            continue
        # "NAME: dialogue" on one line (Ciudad Seva)
        if re.match(r"^[A-ZÁÉÍÓÚÑÜ][A-Za-zÁÉÍÓÚáéíóúñüÑÜ\.\'’ ]{1,30}:\s+\S", raw):
            flush()
            parts.append(raw)
            continue
        buf.append(raw)
    flush()
    out = "\n\n".join(p for p in parts if p.strip())
    return out


def trim_body(body: str, max_chars: int = MAX_CHARS) -> str:
    body = clean_text(body)
    if len(body) <= max_chars:
        return body
    cut = body[:max_chars]
    sp = cut.rfind("\n\n")
    if sp > max_chars * 0.55:
        cut = cut[:sp]
    return cut.strip() + "\n\n[…continúa en la fuente PD…]"



def body_acts(text: str, patterns: list[str]) -> list[tuple[str, int]]:
    acts = find_spans(text, patterns)
    # If ACT I appears twice (TOC + body), keep from second ACT I onward
    first_titles = {}
    body = []
    for title, st in acts:
        key = re.sub(r"\s+", " ", title).split(".")[0].strip().upper()
        if key not in first_titles:
            first_titles[key] = st
        else:
            # second wave — take this and the rest starting here
            # rebuild from first second-wave index
            idx = acts.index((title, st))
            # include matching first act of body: find earliest second occurrences
            seconds = []
            seen = set()
            for t2, st2 in acts:
                k2 = re.sub(r"\s+", " ", t2).split(".")[0].strip().upper()
                if k2 in seen:
                    seconds.append((t2, st2))
                else:
                    seen.add(k2)
            return seconds if seconds else acts
    return acts

def find_spans(text: str, patterns: list[str]) -> list[tuple[str, int]]:
    starts: list[tuple[str, int]] = []
    for pat in patterns:
        for m in re.finditer(pat, text, re.M):
            title = re.sub(r"\s+", " ", m.group(0)).strip()
            starts.append((title, m.start()))
    starts.sort(key=lambda x: x[1])
    uniq: list[tuple[str, int]] = []
    for title, st in starts:
        if uniq and st - uniq[-1][1] < 30:
            continue
        uniq.append((title, st))
    return uniq


def slice_acts(text: str, starts: list[tuple[str, int]], n: int, max_chars: int = MAX_CHARS) -> str:
    if not starts:
        return trim_body(dialogue_blocks(text), max_chars)
    chosen = starts[:n]
    start = chosen[0][1]
    # end at next act after chosen, or EOF
    if len(starts) > n:
        end = starts[n][1]
    else:
        end = len(text)
    body = dialogue_blocks(text[start:end])
    return trim_body(body, max_chars)


def write_book(bid: str, titulo: str, autor: str, nota: str, texto: str) -> dict:
    texto = trim_body(dialogue_blocks(texto) if "\n" in texto else texto)
    data = {
        "id": bid,
        "titulo": titulo,
        "autor": autor,
        "nota": nota,
        "categoria": "teatro",
        "texto": texto,
        "inline": True,
    }
    (LIB / f"{bid}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  + {bid} ({len(texto)} chars) {titulo}")
    return {k: data[k] for k in ("id", "titulo", "autor", "nota", "categoria")}


def load(name: str) -> str:
    p = TMP / name
    if not p.exists():
        raise SystemExit(f"missing source {p}")
    return p.read_text(encoding="utf-8", errors="replace")


def extract_between(text: str, start_pat: str, end_pat: str | None = None) -> str:
    m = re.search(start_pat, text, re.I | re.M)
    if not m:
        return ""
    start = m.start()
    if end_pat:
        m2 = re.search(end_pat, text[m.end() :], re.I | re.M)
        end = m.end() + m2.start() if m2 else len(text)
    else:
        end = len(text)
    return text[start:end]


def build() -> list[dict]:
    meta: list[dict] = []
    print("=== Teatro / guiones PD ===")

    # --- Spanish Golden Age ---
    fuente = strip_pg(load("fuenteovejuna.txt"))
    acts = find_spans(fuente, [r"(?m)^ACTO\s+(PRIMERO|SEGUNDO|TERCERO)\b.*"])
    meta.append(
        write_book(
            "fuenteovejuna-1",
            "Fuenteovejuna · Acto I",
            "Lope de Vega",
            "1619 · ES · dominio público · Gutenberg #60198",
            slice_acts(fuente, acts, 1),
        )
    )
    meta.append(
        write_book(
            "fuenteovejuna-2",
            "Fuenteovejuna · Acto II",
            "Lope de Vega",
            "1619 · ES · dominio público · Gutenberg #60198",
            slice_acts(fuente, acts[1:], 1) if len(acts) > 1 else slice_acts(fuente, acts, 1),
        )
    )

    vida = strip_pg(load("vida-sueno-es.txt"))
    # comedy starts near SEGISMUNDO / LA VIDA ES SUEÑO heading with PERSONAS including SEGISMUNDO
    block = extract_between(
        vida,
        r"(?m)^LA VIDA ES SUEÑO\.\s*$",
        r"(?m)^(?:GUÁRDATE DEL AGUA MANSA|EL LAUREL DE APOLO|LA PÚRPURA|\*\*\*\s*END)",
    )
    if "SEGISMUNDO" not in block.upper():
        # fallback: from first SEGISMUNDO stage block
        i = vida.upper().find("SEGISMUNDO")
        block = vida[max(0, i - 400) :]
    jornadas = find_spans(block, [r"(?m)^JORNADA\s+(PRIMERA|SEGUNDA|TERCERA)\b.*"])
    meta.append(
        write_book(
            "vida-sueno-1",
            "La vida es sueño · Jornada I",
            "Pedro Calderón de la Barca",
            "1635 · ES · dominio público · Gutenberg #54436 (Teatro selecto I)",
            slice_acts(block, jornadas, 1),
        )
    )
    if len(jornadas) > 1:
        meta.append(
            write_book(
                "vida-sueno-2",
                "La vida es sueño · Jornada II",
                "Pedro Calderón de la Barca",
                "1635 · ES · dominio público · Gutenberg #54436",
                slice_acts(block, jornadas[1:], 1),
            )
        )

    burlador = load("burlador-plain.txt")
    acts = find_spans(burlador, [r"(?m)^ACTO\s+(PRIMERO|SEGUNDO|TERCERO)\b.*"])
    meta.append(
        write_book(
            "burlador-1",
            "El burlador de Sevilla · Acto I",
            "Tirso de Molina",
            "c. 1630 · ES · dominio público · texto clásico (Ciudad Seva)",
            slice_acts(burlador, acts, 1),
        )
    )
    if len(acts) > 1:
        meta.append(
            write_book(
                "burlador-2",
                "El burlador de Sevilla · Acto II",
                "Tirso de Molina",
                "c. 1630 · ES · dominio público · texto clásico (Ciudad Seva)",
                slice_acts(burlador, acts[1:], 1),
            )
        )

    perro = load("perro-plain.txt")
    acts = find_spans(perro, [r"(?m)^ACTO\s+(PRIMERO|SEGUNDO|TERCERO)\b.*"])
    meta.append(
        write_book(
            "perro-hortelano-1",
            "El perro del hortelano · Acto I",
            "Lope de Vega",
            "1618 · ES · dominio público · texto clásico (Ciudad Seva)",
            slice_acts(perro, acts, 1),
        )
    )

    # Retag / keep Celestina as teatro (existing short Auto I)
    cel_path = LIB / "celestina.json"
    if cel_path.exists():
        cel = json.loads(cel_path.read_text(encoding="utf-8"))
        cel["categoria"] = "teatro"
        cel["titulo"] = cel.get("titulo") or "La Celestina · Auto I (extracto)"
        cel["nota"] = "1499 · dominio público · extracto diálogo (Auto I)"
        cel_path.write_text(json.dumps(cel, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        meta.append(
            {
                "id": "celestina",
                "titulo": cel["titulo"],
                "autor": cel.get("autor", "Fernando de Rojas"),
                "nota": cel["nota"],
                "categoria": "teatro",
            }
        )
        print("  ~ celestina retagged → teatro")

    # tenorio already teatro — refresh note
    ten_path = LIB / "tenorio.json"
    if ten_path.exists():
        ten = json.loads(ten_path.read_text(encoding="utf-8"))
        ten["categoria"] = "teatro"
        ten_path.write_text(json.dumps(ten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        meta.append(
            {
                "id": "tenorio",
                "titulo": ten["titulo"],
                "autor": ten["autor"],
                "nota": ten.get("nota", "1844 · dominio público"),
                "categoria": "teatro",
            }
        )

    # --- English classics ---
    hamlet = strip_pg(load("hamlet.txt"))
    acts = find_spans(hamlet, [r"(?m)^ACT\s+[IVX]+\b.*"])
    # skip TOC-only early ACT lines: prefer those followed soon by SCENE with dialogue
    real = []
    for title, st in acts:
        window = hamlet[st : st + 400]
        if re.search(r"(?m)^[A-Z][A-Z\-'\. ]{1,30}\.\s*$", window) or "Scene" in window[:80]:
            # Prefer body acts: look for speaker after
            if "FRANCISCO" in hamlet[st : st + 2500] or "HAMLET" in hamlet[st : st + 2500] or st > 5000:
                real.append((title, st))
    if len(real) < 3:
        # fall back: find "ACT I" near first FRANCISCO
        i = hamlet.find("FRANCISCO")
        body = hamlet[max(0, i - 200) :]
        real = find_spans(body, [r"(?m)^ACT\s+[IVX]+\b.*"])
        if not real:
            real = [("ACT I", 0)]
            body_src = body
        else:
            body_src = body
        meta.append(
            write_book(
                "hamlet-1",
                "Hamlet · Act I",
                "William Shakespeare",
                "c. 1601 · EN · PD · Gutenberg #1524",
                slice_acts(body_src, real, 1),
            )
        )
        if len(real) > 1:
            meta.append(
                write_book(
                    "hamlet-2",
                    "Hamlet · Act II",
                    "William Shakespeare",
                    "c. 1601 · EN · PD · Gutenberg #1524",
                    slice_acts(body_src, real[1:], 1),
                )
            )
        if len(real) > 2:
            meta.append(
                write_book(
                    "hamlet-3",
                    "Hamlet · Act III",
                    "William Shakespeare",
                    "c. 1601 · EN · PD · Gutenberg #1524",
                    slice_acts(body_src, real[2:], 1),
                )
            )
    else:
        meta.append(
            write_book(
                "hamlet-1",
                "Hamlet · Act I",
                "William Shakespeare",
                "c. 1601 · EN · PD · Gutenberg #1524",
                slice_acts(hamlet, real, 1),
            )
        )
        meta.append(
            write_book(
                "hamlet-2",
                "Hamlet · Act II",
                "William Shakespeare",
                "c. 1601 · EN · PD · Gutenberg #1524",
                slice_acts(hamlet, real[1:], 1),
            )
        )
        meta.append(
            write_book(
                "hamlet-3",
                "Hamlet · Act III",
                "William Shakespeare",
                "c. 1601 · EN · PD · Gutenberg #1524",
                slice_acts(hamlet, real[2:], 1),
            )
        )

    macbeth = strip_pg(load("macbeth.txt"))
    acts = body_acts(macbeth, [r"(?m)^ACT\s+[IVX]+\b.*", r"(?m)^Act\s+[IVX]+\b.*"])
    meta.append(
        write_book(
            "macbeth-1",
            "Macbeth · Act I",
            "William Shakespeare",
            "c. 1606 · EN · PD · Gutenberg #2264",
            slice_acts(macbeth, acts, 1),
        )
    )
    if len(acts) > 1:
        meta.append(
            write_book(
                "macbeth-2",
                "Macbeth · Act II",
                "William Shakespeare",
                "c. 1606 · EN · PD · Gutenberg #2264",
                slice_acts(macbeth, acts[1:], 1),
            )
        )

    romeo = strip_pg(load("romeo.txt"))
    acts = body_acts(romeo, [r"(?m)^ACT\s+[IVX]+\b.*", r"(?m)^Act\s+[IVX]+\b.*"])
    meta.append(
        write_book(
            "romeo-1",
            "Romeo and Juliet · Act I",
            "William Shakespeare",
            "c. 1597 · EN · PD · Gutenberg #1112",
            slice_acts(romeo, acts, 1),
        )
    )
    if len(acts) > 1:
        meta.append(
            write_book(
                "romeo-2",
                "Romeo and Juliet · Act II",
                "William Shakespeare",
                "c. 1597 · EN · PD · Gutenberg #1112",
                slice_acts(romeo, acts[1:], 1),
            )
        )

    earnest = strip_pg(load("earnest.txt"))
    acts = find_spans(earnest, [r"(?m)^FIRST ACT\b.*", r"(?m)^SECOND ACT\b.*", r"(?m)^THIRD ACT\b.*"])
    if len(acts) < 2:
        acts = find_spans(earnest, [r"(?m)^ACT\s+[IVXLC]+\b.*"])
        # drop TOC-only (very early, short distance)
        acts = [(t, st) for t, st in acts if st > 800]
    meta.append(
        write_book(
            "earnest-1",
            "The Importance of Being Earnest · Act I",
            "Oscar Wilde",
            "1895 · EN · PD (Wilde †1900) · Gutenberg #844",
            slice_acts(earnest, acts, 1),
        )
    )
    if len(acts) > 1:
        meta.append(
            write_book(
                "earnest-2",
                "The Importance of Being Earnest · Act II",
                "Oscar Wilde",
                "1895 · EN · PD · Gutenberg #844",
                slice_acts(earnest, acts[1:], 1),
            )
        )

    ideal = strip_pg(load("ideal-husband.txt"))
    acts = find_spans(ideal, [r"(?m)^FIRST ACT\b.*", r"(?m)^SECOND ACT\b.*", r"(?m)^THIRD ACT\b.*", r"(?m)^FOURTH ACT\b.*"])
    if len(acts) < 1:
        acts = [(t, st) for t, st in find_spans(ideal, [r"(?m)^ACT\s+[IVXLC]+\b.*"]) if st > 2500]
    meta.append(
        write_book(
            "ideal-husband-1",
            "An Ideal Husband · Act I",
            "Oscar Wilde",
            "1895 · EN · PD (Wilde †1900) · Gutenberg #885",
            slice_acts(ideal, acts, 1),
        )
    )
    if len(acts) > 1:
        meta.append(
            write_book(
                "ideal-husband-2",
                "An Ideal Husband · Act II",
                "Oscar Wilde",
                "1895 · EN · PD · Gutenberg #885",
                slice_acts(ideal, acts[1:], 1),
            )
        )

    # --- Greek ---
    oed = strip_pg(load("oedipus.txt"))
    king = extract_between(
        oed,
        r"(?m)^OEDIPUS THE KING\s*$",
        r"(?m)^OEDIPUS AT COLONUS\s*$",
    )
    meta.append(
        write_book(
            "oedipus-king",
            "Oedipus the King",
            "Sophocles · F. Storr trans.",
            "1912 Loeb · EN · PD · Gutenberg #31",
            trim_body(dialogue_blocks(king)),
        )
    )
    antig = extract_between(
        oed,
        r"(?m)^ANTIGONE\s*$",
        r"(?m)^\*\*\*\s*END OF",
    )
    # ANTIGONE title appears in cast lists; take last major block
    idxs = [m.start() for m in re.finditer(r"(?m)^ANTIGONE\s*$", oed)]
    if idxs:
        start = idxs[-1]
        # if last is too late tiny, use previous
        for i in reversed(idxs):
            if len(oed) - i > 20000:
                start = i
                break
        antig = oed[start:]
        m_end = re.search(r"\*\*\*\s*END OF", antig)
        if m_end:
            antig = antig[: m_end.start()]
    meta.append(
        write_book(
            "antigone",
            "Antigone",
            "Sophocles · F. Storr trans.",
            "1912 Loeb · EN · PD · Gutenberg #31",
            trim_body(dialogue_blocks(antig)),
        )
    )

    # --- Molière ---
    tart = strip_pg(load("tartuffe.txt"))
    acts = find_spans(tart, [r"(?m)^ACT\s+[IVXLC]+\b.*", r"(?m)^Act\s+[IVXLC]+\b.*"])
    meta.append(
        write_book(
            "tartuffe-1",
            "Tartuffe · Act I",
            "Molière",
            "1664 · EN trans. PD · Gutenberg #2027",
            slice_acts(tart, acts, 1),
        )
    )
    if len(acts) > 1:
        meta.append(
            write_book(
                "tartuffe-2",
                "Tartuffe · Act II",
                "Molière",
                "1664 · EN trans. PD · Gutenberg #2027",
                slice_acts(tart, acts[1:], 1),
            )
        )

    mis = load("misanthrope-fr.txt")
    acts = find_spans(mis, [r"(?m)^ACTE\s+[IVXLC]+\b.*", r"(?m)^ACTE\s+PREMIER\b.*"])
    meta.append(
        write_book(
            "misanthrope-1",
            "Le Misanthrope · Acte I",
            "Molière",
            "1666 · FR · dominio público · Gutenberg #50173",
            slice_acts(mis, acts, 1),
        )
    )

    # English Life Is a Dream (optional classic trans.)
    vida_en = strip_pg(load("vida-sueno-en.txt"))
    acts = find_spans(
        vida_en,
        [r"(?m)^ACT\s+[IVXLC]+\b.*", r"(?m)^FIRST DAY\b.*", r"(?m)^SECOND DAY\b.*", r"(?m)^ACTO\s+.*"],
    )
    meta.append(
        write_book(
            "life-dream-1",
            "Life Is a Dream · Act I (EN)",
            "Calderón · PD English trans.",
            "EN · PD · Gutenberg #2587 / #6363",
            slice_acts(vida_en, acts, 1) if acts else trim_body(dialogue_blocks(vida_en)),
        )
    )

    # Catalog note (no large text file needed — short aviso)
    nota_txt = (
        "Este filtro «Teatro / guiones» reúne drama clásico en formato diálogo "
        "(Siglo de Oro, Shakespeare, Wilde, Sófocles, Molière…), textos en dominio público.\n\n"
        "No entran guiones de cine o series modernas: casi nunca son dominio público por derechos."
    )
    write_book(
        CATALOG_NOTE["id"],
        CATALOG_NOTE["titulo"],
        CATALOG_NOTE["autor"],
        CATALOG_NOTE["nota"],
        nota_txt,
    )
    # force categoria nota
    p = LIB / f"{CATALOG_NOTE['id']}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["categoria"] = "nota"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    meta.append({**CATALOG_NOTE})
    print("  + nota-teatro-guiones (aviso)")

    return meta


def upsert_catalog(metas: list[dict]) -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_id = {e["id"]: i for i, e in enumerate(catalog)}
    for m in metas:
        entry = {k: m[k] for k in ("id", "titulo", "autor", "nota", "categoria")}
        if m["id"] in by_id:
            catalog[by_id[m["id"]]] = entry
        else:
            catalog.append(entry)
            by_id[m["id"]] = len(catalog) - 1
    # ensure celestina teatro
    if "celestina" in by_id:
        catalog[by_id["celestina"]]["categoria"] = "teatro"
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"catalog={len(catalog)} upserted={len(metas)}")


def main() -> None:
    LIB.mkdir(parents=True, exist_ok=True)
    metas = build()
    upsert_catalog(metas)


if __name__ == "__main__":
    main()
