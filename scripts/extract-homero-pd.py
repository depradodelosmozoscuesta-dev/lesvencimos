#!/usr/bin/env python3
"""Extract readable PD Spanish Homeric cantos from Archive.org DjVuTXT (Segalá)."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / ".tmp-books"
LIB = ROOT / "modulos" / "biblioteca-libros"

ROMAN = {
    "PRIMERO": 1, "I": 1, "1": 1,
    "SEGUNDO": 2, "II": 2, "2": 2,
    "TERCERO": 3, "III": 3, "3": 3, "111": 3,  # OCR III->111
    "CUARTO": 4, "IV": 4, "4": 4,
    "QUINTO": 5, "V": 5, "5": 5,
    "SEXTO": 6, "VI": 6, "6": 6,
    "SÉPTIMO": 7, "SEPTIMO": 7, "VII": 7, "7": 7,
    "OCTAVO": 8, "VIII": 8, "8": 8,
    "NOVENO": 9, "IX": 9, "9": 9,
    "DÉCIMO": 10, "DECIMO": 10, "X": 10, "10": 10,
    "UNDÉCIMO": 11, "UNDECIMO": 11, "XI": 11,
    "DUODÉCIMO": 12, "DUODECIMO": 12, "XII": 12,
}

def clean_ocr(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"([A-Za-zÁÉÍÓÚáéíóúñÑüÜ])-\n([a-záéíóúñü])", r"\1\2", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    # common OCR fixes
    s = s.replace("Habíame, Musa", "Háblame, Musa")
    s = s.replace("Habíame Musa", "Háblame, Musa")
    s = s.replace("ítaca", "Ítaca")
    s = s.replace("á ", "á ")  # keep historical spelling
    return s

def strip_verse_noise(s: str) -> str:
    lines = []
    for line in s.split("\n"):
        # drop lone page numbers
        if re.fullmatch(r"\s*\d{1,3}\s*", line):
            continue
        # drop running headers like "CANTO PRIMERO" mid-flow (keep first)
        # strip leading verse numbers: "63 Contestóle" or "158 «¡Caro"
        line = re.sub(r"^(\d{1,4}|[ivxlcdm]{1,6})\s+(?=\S)", "", line, flags=re.I)
        lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def find_canto_starts(text: str):
    """Return list of (canto_num, start_index, subtitle) for real canto openings."""
    starts = []
    # Pattern: CANTO NAME\n\nALLCAPS SUBTITLE (with — or .)
    pat = re.compile(
        r"(?m)^CANTO\s+([A-ZÁÉÍÓÚÜÑ0-9]+)\s*\n\n([A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ0-9\s\.,;—\-–]{8,120})\n",
    )
    for m in pat.finditer(text):
        name = m.group(1).strip().upper()
        # OCR fixes
        name = name.replace("111", "III")
        num = ROMAN.get(name)
        if not num:
            continue
        sub = re.sub(r"\s+", " ", m.group(2)).strip(" .—–-")
        starts.append((num, m.start(), sub, m.end()))
    # de-dupe: keep first occurrence of each canto number
    seen = set()
    out = []
    for num, start, sub, end in starts:
        if num in seen:
            continue
        seen.add(num)
        out.append((num, start, sub, end))
    out.sort(key=lambda x: x[0])
    return out

def extract_cantos(text: str, max_cantos: int = 6):
    starts = find_canto_starts(text)
    if not starts:
        return []
    # also find absolute end markers
    results = []
    for i, (num, start, sub, body_start) in enumerate(starts):
        if num > max_cantos:
            break
        if i + 1 < len(starts):
            end = starts[i + 1][1]
        else:
            # until next CANTO after this, or +80k chars
            m = re.search(r"(?m)^CANTO\s+", text[body_start + 200 :])
            end = body_start + 200 + m.start() if m else min(len(text), body_start + 80000)
        body = text[start:end]
        # Remove subsequent running headers of same canto
        body = re.sub(r"(?m)^CANTO\s+[A-ZÁÉÍÓÚÜÑ0-9]+\s*\n+(?:\d{1,3}\s*\n+)?", "\n", body)
        # Keep title line once
        title = f"Canto {num}"
        if sub:
            title += f" · {sub.title()}"
        body = strip_verse_noise(body)
        # Cap length (~like Mosqueteros chapters)
        if len(body) > 42000:
            # cut at paragraph near limit
            cut = body[:42000].rfind("\n\n")
            if cut > 30000:
                body = body[:cut].rstrip() + "\n\n[…continúa en el canto completo.]"
        results.append((num, title, body))
    return results

def write_book(bid, titulo, autor, nota, categoria, texto):
    data = {
        "id": bid,
        "titulo": titulo,
        "autor": autor,
        "nota": nota,
        "texto": texto,
        "categoria": categoria,
    }
    (LIB / f"{bid}.json").write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"wrote {bid}: {len(texto)} chars · {titulo[:60]}")

def main():
    od = clean_ocr((TMP / "odisea-1910.txt").read_text(encoding="utf-8", errors="replace"))
    il = clean_ocr((TMP / "iliada-segala-1908.txt").read_text(encoding="utf-8", errors="replace"))

    print("=== Odisea starts ===")
    for n, s, sub, e in find_canto_starts(od)[:12]:
        print(n, sub[:70], "at", s)

    print("=== Ilíada starts ===")
    for n, s, sub, e in find_canto_starts(il)[:12]:
        print(n, sub[:70], "at", s)

    od_cantos = extract_cantos(od, max_cantos=6)
    il_cantos = extract_cantos(il, max_cantos=6)

    # Replace stub homero.json with real Canto I; add more as separate entries
    nota_od = "trad. Luis Segalá y Estalella, 1910 · PD (m. 1938 → ES vida+70)"
    nota_il = "trad. Luis Segalá y Estalella, 1908 · PD (m. 1938 → ES vida+70)"
    autor = "Homero · trad. Luis Segalá y Estalella"

    if od_cantos:
        # primary entry keeps id 'homero' for catalog compat, retitled
        n, title, body = od_cantos[0]
        write_book(
            "homero",
            f"La Odisea · {title}",
            autor,
            nota_od,
            "poesia",
            body,
        )
        for n, title, body in od_cantos[1:]:
            write_book(
                f"odisea-{n}",
                f"La Odisea · {title}",
                autor,
                nota_od,
                "poesia",
                body,
            )
    else:
        print("WARNING: no Odyssey cantos extracted")

    if il_cantos:
        for n, title, body in il_cantos:
            write_book(
                f"iliada-{n}",
                f"La Ilíada · {title}",
                autor,
                nota_il,
                "poesia",
                body,
            )
    else:
        print("WARNING: no Iliad cantos extracted")

if __name__ == "__main__":
    main()
