#!/usr/bin/env python3
"""Pack Orwell EN (PD-EU via PGAU) for biblioteca v20260922q.
Sources: Project Gutenberg Australia only (not US Gutenberg).
No Spanish translations.
"""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "modulos" / "biblioteca-libros"
TMP = ROOT / ".tmp-books" / "orwell"
CATALOG = LIB / "catalog.json"
MAX_CHARS = 42000

NOTE = (
    "texto inglés, dominio público en la UE; sin traducción española "
    "· Project Gutenberg Australia (PD AU/EU; NO PD en EE.UU. hasta ~2044)"
)
NOTE_1984 = NOTE + " · #0100021"
NOTE_AF = NOTE + " · #0100011"
NOTE_HOM = NOTE + " · #0201111"
NOTE_DO = NOTE + " · #0100171"
NOTE_WIG = NOTE + " · #0200391"


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


def trim_body(body: str, max_chars: int = MAX_CHARS) -> str:
    body = clean_text(body)
    if len(body) <= max_chars:
        return body
    cut = body[:max_chars]
    sp = cut.rfind("\n\n")
    if sp > max_chars * 0.55:
        cut = cut[:sp]
    return cut.strip() + "\n\n[…continúa en la fuente PD…]"


def write_book(bid, titulo, autor, nota, categoria, texto):
    texto = trim_body(texto)
    data = {
        "id": bid,
        "titulo": titulo,
        "autor": autor,
        "nota": nota,
        "categoria": categoria,
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
    }


def strip_pg_header(text: str, start_re: str) -> str:
    m = re.search(start_re, text, re.M)
    if m:
        return text[m.start() :]
    return text


def split_by_regex(text: str, pat: str):
    """Return list of (title, body) for each match of pat at chapter starts."""
    starts = list(re.finditer(pat, text, re.M))
    out = []
    for i, mm in enumerate(starts):
        title = re.sub(r"\s+", " ", mm.group(0)).strip()
        st = mm.start()
        en = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        out.append((title, text[st:en]))
    return out


def pack_groups(chapters, max_chars=MAX_CHARS):
    """Greedy group complete chapters under max_chars; oversized alone (trimmed later)."""
    groups = []
    cur, cur_len = [], 0
    for title, body in chapters:
        bl = len(body)
        if cur and cur_len + bl > max_chars:
            groups.append(cur)
            cur, cur_len = [], 0
        cur.append((title, body))
        cur_len += bl
        if cur_len >= max_chars:
            groups.append(cur)
            cur, cur_len = [], 0
    if cur:
        groups.append(cur)
    return groups


def join_group(group):
    return paras("\n\n".join(body for _, body in group))


def label_chs(group, roman=False):
    nums = []
    for title, _ in group:
        m = re.search(r"(?:Chapter|CHAPTER)\s+([IVXLC\d]+)", title, re.I)
        if m:
            nums.append(m.group(1))
        else:
            m2 = re.fullmatch(r"([IVXLC]+)", title.strip())
            if m2:
                nums.append(m2.group(1))
    if not nums:
        return "?"
    if len(nums) == 1:
        return nums[0]
    return f"{nums[0]}–{nums[-1]}"


def split_oversized(title, body, max_chars=MAX_CHARS):
    """Split a single oversized chapter into ~max_chars slices at paragraph breaks."""
    body = paras(body)
    if len(body) <= max_chars:
        return [(title, body)]
    parts = []
    rest = body
    idx = 1
    while rest:
        if len(rest) <= max_chars:
            parts.append((f"{title} ({idx})" if idx > 1 or len(parts) else title, rest))
            break
        cut = rest[:max_chars]
        sp = cut.rfind("\n\n")
        if sp < max_chars * 0.5:
            sp = max_chars
        chunk = rest[:sp].strip()
        parts.append((f"{title} ({idx})", chunk))
        rest = rest[sp:].strip()
        idx += 1
    # Fix first title if we split
    if len(parts) > 1 and not parts[0][0].endswith(")"):
        parts[0] = (f"{title} (1)", parts[0][1])
    return parts


def build_1984(metas):
    path = TMP / "1984-pgau.txt"
    if not path.exists():
        print("  SKIP 1984 — no source")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    text = strip_pg_header(text, r"(?m)^PART ONE\s*$")

    # Locate parts
    part_pos = {}
    for mm in re.finditer(r"(?m)^(PART (?:ONE|TWO|THREE)|APPENDIX\.?)\s*$", text):
        part_pos[mm.group(1).rstrip(".")] = mm.start()

    def part_slice(name, next_names):
        st = part_pos[name]
        en = len(text)
        for n in next_names:
            key = n.rstrip(".")
            if key in part_pos:
                en = part_pos[key]
                break
        return text[st:en]

    # --- Keep existing Part One I–III pack as-is (do not rewrite) ---
    # Continue from Ch 4 of Part One
    p1 = part_slice("PART ONE", ["PART TWO"])
    p1_chs = split_by_regex(p1, r"(?m)^Chapter\s+\d+\s*$")
    # Arabic → display roman-ish labels in titles via numbers
    cont = p1_chs[3:]  # skip 1,2,3
    # Expand oversized before grouping
    expanded = []
    for title, body in cont:
        expanded.extend(split_oversized(title, body))
    groups = pack_groups(expanded)
    # Naming: p1b, p1c, ...
    letters = "bcdefghij"
    for i, g in enumerate(groups):
        lab = label_chs(g)
        bid = f"orwell-1984-p1{letters[i]}"
        body = join_group(g)
        # Prefer Roman numerals in display for consistency with existing pack
        metas.append(
            write_book(
                bid,
                f"Nineteen Eighty-Four · Part One, Ch. {lab}",
                "George Orwell",
                NOTE_1984,
                "narrativa",
                body,
            )
        )

    # Part Two
    p2 = part_slice("PART TWO", ["PART THREE"])
    p2_chs = split_by_regex(p2, r"(?m)^Chapter\s+\d+\s*$")
    expanded = []
    for title, body in p2_chs:
        expanded.extend(split_oversized(title, body))
    groups = pack_groups(expanded)
    for i, g in enumerate(groups):
        lab = label_chs(g)
        bid = f"orwell-1984-p2{chr(ord('a') + i)}"
        metas.append(
            write_book(
                bid,
                f"Nineteen Eighty-Four · Part Two, Ch. {lab}",
                "George Orwell",
                NOTE_1984,
                "narrativa",
                join_group(g),
            )
        )

    # Part Three
    p3 = part_slice("PART THREE", ["APPENDIX"])
    p3_chs = split_by_regex(p3, r"(?m)^Chapter\s+\d+\s*$")
    expanded = []
    for title, body in p3_chs:
        expanded.extend(split_oversized(title, body))
    groups = pack_groups(expanded)
    for i, g in enumerate(groups):
        lab = label_chs(g)
        bid = f"orwell-1984-p3{chr(ord('a') + i)}"
        metas.append(
            write_book(
                bid,
                f"Nineteen Eighty-Four · Part Three, Ch. {lab}",
                "George Orwell",
                NOTE_1984,
                "narrativa",
                join_group(g),
            )
        )

    # Appendix
    if "APPENDIX" in part_pos:
        app = text[part_pos["APPENDIX"] :]
        # stop at end marker if any
        endm = re.search(r"(?m)^(?:THE END|End of (?:the )?Project Gutenberg)", app)
        if endm:
            app = app[: endm.start()]
        metas.append(
            write_book(
                "orwell-1984-app",
                "Nineteen Eighty-Four · Appendix: The Principles of Newspeak",
                "George Orwell",
                NOTE_1984,
                "narrativa",
                paras(app),
            )
        )


def build_animal_farm(metas):
    path = TMP / "animal-farm-pgau.txt"
    if not path.exists():
        print("  SKIP Animal Farm")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    text = strip_pg_header(text, r"(?m)^Chapter\s+I\b")
    endm = re.search(r"(?m)^(?:THE END|End of (?:the )?Project Gutenberg|\*\*\*END)", text)
    if endm:
        text = text[: endm.start()]
    chs = split_by_regex(text, r"(?m)^Chapter\s+[IVXLC]+\b.*")
    groups = pack_groups(chs)
    for i, g in enumerate(groups):
        lab = label_chs(g)
        bid = "orwell-animal-farm" if i == 0 else f"orwell-animal-farm-{i + 1}"
        metas.append(
            write_book(
                bid,
                f"Animal Farm · Ch. {lab}",
                "George Orwell",
                NOTE_AF,
                "narrativa",
                join_group(g),
            )
        )


def build_homage(metas):
    path = TMP / "homage-pgau.txt"
    if not path.exists():
        print("  SKIP Homage")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    text = strip_pg_header(text, r"(?m)^Chapter\s+1\b")
    endm = re.search(r"(?m)^(?:THE END|End of (?:the )?Project Gutenberg|\*\*\*END)", text)
    if endm:
        text = text[: endm.start()]
    chs = split_by_regex(text, r"(?m)^Chapter\s+\d+\b.*")
    # Selections: first 6 chapters in packs
    sel = chs[:6]
    groups = pack_groups(sel)
    for i, g in enumerate(groups):
        lab = label_chs(g)
        bid = "orwell-homage" if i == 0 else f"orwell-homage-{i + 1}"
        metas.append(
            write_book(
                bid,
                f"Homage to Catalonia · Ch. {lab} (selección)",
                "George Orwell",
                NOTE_HOM,
                "narrativa",
                join_group(g),
            )
        )


def build_down_out(metas):
    path = TMP / "down-out-pgau.txt"
    if not path.exists():
        print("  SKIP Down and Out")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    # Roman numeral alone on line
    text = strip_pg_header(text, r"(?m)^I\s*$")
    endm = re.search(r"(?m)^(?:THE END|End of (?:the )?Project Gutenberg|\*\*\*END)", text)
    if endm:
        text = text[: endm.start()]
    chs = split_by_regex(text, r"(?m)^([IVXLC]+)\s*$")
    # Filter out tiny false positives (e.g. mid-book single letters) — keep substantial
    chs = [(t, b) for t, b in chs if len(b) > 800]
    sel = chs[:8]  # first 8 chapters
    groups = pack_groups(sel)
    for i, g in enumerate(groups):
        lab = label_chs(g)
        bid = "orwell-down-out" if i == 0 else f"orwell-down-out-{i + 1}"
        metas.append(
            write_book(
                bid,
                f"Down and Out in Paris and London · Ch. {lab}",
                "George Orwell",
                NOTE_DO,
                "narrativa",
                join_group(g),
            )
        )


def build_wigan(metas):
    path = TMP / "wigan-pgau.txt"
    if not path.exists():
        print("  SKIP Wigan")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    text = strip_pg_header(text, r"(?m)^PART ONE\s*$")
    # Part One only until PART TWO
    p2 = re.search(r"(?m)^PART TWO\s*$", text)
    if p2:
        part1 = text[: p2.start()]
    else:
        part1 = text[: MAX_CHARS * 2]
    # Two packs from Part One
    body = paras(part1)
    if len(body) <= MAX_CHARS:
        metas.append(
            write_book(
                "orwell-wigan",
                "The Road to Wigan Pier · Part One (selección)",
                "George Orwell",
                NOTE_WIG,
                "narrativa",
                body,
            )
        )
    else:
        metas.append(
            write_book(
                "orwell-wigan",
                "The Road to Wigan Pier · Part One (1)",
                "George Orwell",
                NOTE_WIG,
                "narrativa",
                body,
            )
        )
        # second pack: skip first MAX_CHARS at para break
        cut = body[:MAX_CHARS]
        sp = cut.rfind("\n\n")
        if sp < 0:
            sp = MAX_CHARS
        rest = body[sp:].strip()
        if len(rest) > 500:
            metas.append(
                write_book(
                    "orwell-wigan-2",
                    "The Road to Wigan Pier · Part One (2)",
                    "George Orwell",
                    NOTE_WIG,
                    "narrativa",
                    rest,
                )
            )


def upsert_catalog(metas):
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_id = {e["id"]: i for i, e in enumerate(catalog)}
    for m in metas:
        entry = {k: m[k] for k in ("id", "titulo", "autor", "nota", "categoria")}
        if m["id"] in by_id:
            catalog[by_id[m["id"]]] = entry
        else:
            # Insert Orwell entries after existing orwell-1984 if present
            if "orwell-1984" in by_id and m["id"].startswith("orwell-"):
                # append near other orwells: find last orwell index
                last = max(i for i, e in enumerate(catalog) if e["id"].startswith("orwell-"))
                catalog.insert(last + 1, entry)
                by_id = {e["id"]: i for i, e in enumerate(catalog)}
            else:
                catalog.append(entry)
                by_id[m["id"]] = len(catalog) - 1
    # Normalize note on existing orwell-1984 to catalog wording
    if "orwell-1984" in by_id:
        e = catalog[by_id["orwell-1984"]]
        e["nota"] = NOTE_1984
        # also update JSON file note
        p = LIB / "orwell-1984.json"
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            data["nota"] = NOTE_1984
            p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"catalog={len(catalog)} new/updated={len(metas)}")


def build():
    metas = []
    print("=== Nineteen Eighty-Four (continue) ===")
    build_1984(metas)
    print("=== Animal Farm ===")
    build_animal_farm(metas)
    print("=== Homage to Catalonia (sel.) ===")
    build_homage(metas)
    print("=== Down and Out (sel.) ===")
    build_down_out(metas)
    print("=== Road to Wigan Pier (sel.) ===")
    build_wigan(metas)
    upsert_catalog(metas)
    print(f"total packs written this run: {len(metas)}")


if __name__ == "__main__":
    build()
