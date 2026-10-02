#!/usr/bin/env python3
"""Build offline CIMA/AEMPS Nomenclátor index for Medicación (Les vencimos).

Downloads https://listadomedicamentos.aemps.gob.es/prescripcion.zip (needs browser UA),
parses Prescripcion.xml + dictionaries, emits modulos/nomenclator/cima-index.json.gz.

Filter: autorizados (cod_sitreg=1) OR comercializados (sw_comercializado=1).
Does NOT embed AEMPS photos. Official fields are not transformed.

Attribution (required):
  Fuente de la información: Agencia Española de Medicamentos y Productos Sanitarios
  www.aemps.gob.es
+ fecha de obtención.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from datetime import date
from pathlib import Path

ZIP_URL = "https://listadomedicamentos.aemps.gob.es/prescripcion.zip"
UA = "Mozilla/5.0 (compatible; LesVencimosNomenclatorBuild/1.0; +https://lesvencimos.com)"
ATRIBUCION = (
    "Fuente de la información: Agencia Española de Medicamentos y Productos Sanitarios "
    "www.aemps.gob.es"
)


def local(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def load_dict(path: Path, item_tag: str, code_tag: str, name_tag: str) -> dict:
    d: dict[str, str] = {}
    for _event, elem in ET.iterparse(path, events=("end",)):
        if local(elem.tag) != item_tag:
            continue
        code = name = None
        for c in elem:
            t = local(c.tag)
            if t == code_tag:
                code = (c.text or "").strip()
            elif t == name_tag:
                name = (c.text or "").strip()
        if code is not None:
            d[code] = name or ""
        elem.clear()
    return d


def download_zip(dest: Path) -> None:
    req = urllib.request.Request(ZIP_URL, headers={"User-Agent": UA, "Accept": "*/*"})
    print(f"Downloading {ZIP_URL} …", flush=True)
    with urllib.request.urlopen(req, timeout=180) as resp, open(dest, "wb") as out:
        while True:
            chunk = resp.read(1024 * 256)
            if not chunk:
                break
            out.write(chunk)
    print(f"  saved {dest} ({dest.stat().st_size} bytes)", flush=True)


def build(xml_dir: Path, out_gz: Path, fecha_obtencion: str) -> dict:
    labs = load_dict(
        xml_dir / "DICCIONARIO_LABORATORIOS.xml",
        "laboratorios",
        "codigolaboratorio",
        "laboratorio",
    )
    pas = load_dict(
        xml_dir / "DICCIONARIO_PRINCIPIOS_ACTIVOS.xml",
        "principiosactivos",
        "nroprincipioactivo",
        "principioactivo",
    )
    formas = load_dict(
        xml_dir / "DICCIONARIO_FORMA_FARMACEUTICA.xml",
        "formasfarmaceuticas",
        "codigoformafarmaceutica",
        "formafarmaceutica",
    )
    formas_s = load_dict(
        xml_dir / "DICCIONARIO_FORMA_FARMACEUTICA_SIMPLIFICADAS.xml",
        "formasfarmaceuticassimplificadas",
        "codigoformafarmaceuticasimplificada",
        "formafarmaceuticasimplificada",
    )

    meds: dict[str, dict] = {}
    list_date = None
    kept_pres = 0

    for _event, elem in ET.iterparse(xml_dir / "Prescripcion.xml", events=("end",)):
        tag = local(elem.tag)
        if tag == "listprescriptiondate":
            list_date = (elem.text or "").strip()
            elem.clear()
            continue
        if tag != "prescription":
            continue

        fields: dict[str, str] = {}
        pa_codes: list[str] = []
        forfar = forfar_s = None
        for c in elem:
            t = local(c.tag)
            if t == "formasfarmaceuticas":
                for sub in c:
                    st = local(sub.tag)
                    if st == "cod_forfar":
                        forfar = (sub.text or "").strip()
                    elif st == "cod_forfar_simplificada":
                        forfar_s = (sub.text or "").strip()
                    elif st == "composicion_pa":
                        for x in sub:
                            if local(x.tag) == "cod_principio_activo":
                                pa_codes.append((x.text or "").strip())
            else:
                fields[t] = (c.text or "").strip() if c.text else ""

        com = fields.get("sw_comercializado", "0")
        sit = fields.get("cod_sitreg", "")
        if not (com == "1" or sit == "1"):
            elem.clear()
            continue

        nreg = fields.get("nro_definitivo", "")
        if not nreg:
            elem.clear()
            continue

        kept_pres += 1
        cn = fields.get("cod_nacion", "")
        prese = fields.get("des_prese", "")
        nombre = fields.get("des_nomco", "")
        dos = fields.get("des_dosific", "")
        lab_c = fields.get("laboratorio_comercializador") or fields.get("laboratorio_titular") or ""
        lab = labs.get(lab_c, "")
        pa_names: list[str] = []
        for code in pa_codes:
            nm = pas.get(code)
            if nm and nm not in pa_names:
                pa_names.append(nm)
        forma = formas_s.get(forfar_s or "", "") or formas.get(forfar or "", "")

        rec = meds.get(nreg)
        if not rec:
            rec = {
                "nr": nreg,
                "n": nombre,
                "dos": dos,
                "forma": forma,
                "pa": pa_names,
                "lab": lab,
                "com": 1 if com == "1" else 0,
                "cn": [],
                "nc": 0,
            }
            meds[nreg] = rec
        else:
            if com == "1":
                rec["com"] = 1
            if not rec["dos"] and dos:
                rec["dos"] = dos
            if not rec["forma"] and forma:
                rec["forma"] = forma
            if not rec["lab"] and lab:
                rec["lab"] = lab
            for p in pa_names:
                if p not in rec["pa"]:
                    rec["pa"].append(p)

        if cn and not any(x["c"] == cn for x in rec["cn"]):
            short = prese if len(prese) <= 80 else (prese[:80] + "…")
            rec["cn"].append({"c": cn, "p": short, "com": 1 if com == "1" else 0})
        elem.clear()

    for rec in meds.values():
        rec["nc"] = len(rec["cn"])
        rec["cn"] = rec["cn"][:8]
        rec["pa"] = rec["pa"][:6]

    items = sorted(meds.values(), key=lambda x: x["n"])
    meta = {
        "fuente": "Agencia Española de Medicamentos y Productos Sanitarios www.aemps.gob.es",
        "atribucion": ATRIBUCION,
        "fecha_listado": list_date,
        "fecha_obtencion": fecha_obtencion,
        "filtro": "autorizados (cod_sitreg=1) o comercializados (sw_comercializado=1)",
        "n_medicamentos": len(items),
        "n_presentaciones": kept_pres,
        "aviso": (
            "Datos oficiales sin transformar. No sustituye el prospecto del envase ni la "
            "indicación médica. Urgencias: 112. Sin fotos AEMPS."
        ),
        "urls": {
            "cima_publico": "https://cima.aemps.es/cima/publico/detalle.html?nregistro={nregistro}",
            "prospecto_html": "https://cima.aemps.es/cima/dochtml/p/{nregistro}/Prospecto.html",
            "ft_html": "https://cima.aemps.es/cima/dochtml/ft/{nregistro}/FichaTecnica.html",
            "api": "https://cima.aemps.es/cima/rest/",
        },
    }
    payload = {"meta": meta, "meds": items}
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    out_gz.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(out_gz, "wb", compresslevel=9) as f:
        f.write(raw)
    meta_path = out_gz.with_suffix("").with_suffix(".meta.json")  # cima-index.meta.json
    # out_gz is cima-index.json.gz → stem handling
    meta_path = out_gz.parent / "cima-index.meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(
        f"Wrote {out_gz} ({out_gz.stat().st_size} bytes gz, {len(raw)} raw) "
        f"meds={len(items)} pres={kept_pres} listado={list_date}",
        flush=True,
    )
    return meta


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--xml-dir",
        type=Path,
        help="Already-unzipped nomenclátor folder (skips download)",
    )
    ap.add_argument(
        "--zip",
        type=Path,
        help="Local prescripcion.zip (skips download)",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent / "nomenclator" / "cima-index.json.gz",
    )
    ap.add_argument(
        "--fecha-obtencion",
        default=date.today().isoformat(),
        help="Date the ZIP was obtained (YYYY-MM-DD), shown in attribution",
    )
    args = ap.parse_args()

    if args.xml_dir:
        meta = build(args.xml_dir, args.out, args.fecha_obtencion)
    else:
        with tempfile.TemporaryDirectory(prefix="nomenclator-") as td:
            td_path = Path(td)
            zpath = args.zip or (td_path / "prescripcion.zip")
            if not args.zip:
                download_zip(zpath)
            with zipfile.ZipFile(zpath, "r") as zf:
                zf.extractall(td_path / "xml")
            meta = build(td_path / "xml", args.out, args.fecha_obtencion)

    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
