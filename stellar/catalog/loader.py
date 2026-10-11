"""Carga el catálogo estelar estático (CSV) en SQLite y valida las reglas de negocio."""
import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
MIN_STARS = 100
CONTROL_COUNT = 20

# 20 estrellas brillantes y bien separadas reservadas como comandos del sistema.
CONTROL_STARS = {
    "Polaris": "HOME", "Sirius": "CONFIRM", "Canopus": "BACK", "Vega": "DELETE",
    "Arcturus": "CLEAR", "Capella": "SPACE", "Rigel": "NEXT", "Procyon": "PREV",
    "Betelgeuse": "HELP", "Altair": "CALIBRATE", "Aldebaran": "CANCEL",
    "Spica": "SHIFT", "Antares": "LOCK", "Deneb": "UNLOCK", "Pollux": "REPEAT",
    "Fomalhaut": "HINT", "Achernar": "SETTINGS", "Hadar": "QUIT",
    "Acrux": "SOS", "Regulus": "MENU",
}


def connect(path=":memory:"):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def create_schema(con):
    con.executescript((HERE / "schema.sql").read_text(encoding="utf-8"))


def load_catalog(con, csv_path=HERE / "stars.csv"):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) < MIN_STARS:
        raise ValueError(f"catálogo con {len(rows)} estrellas; mínimo {MIN_STARS}")
    names = {r["name"] for r in rows}
    missing = set(CONTROL_STARS) - names
    if missing:
        raise ValueError(f"estrellas de control ausentes: {sorted(missing)}")
    if len(CONTROL_STARS) != CONTROL_COUNT:
        raise ValueError("deben reservarse exactamente 20 estrellas de control")
    with con:
        for r in rows:
            cmd = CONTROL_STARS.get(r["name"])
            con.execute(
                "INSERT INTO star(name,constel,ra_deg,dec_deg,mag,role,command) VALUES(?,?,?,?,?,?,?)",
                (r["name"], r["constel"], float(r["ra_deg"]), float(r["dec_deg"]),
                 float(r["mag"]), "CONTROL" if cmd else "OPTION", cmd),
            )
    validate(con)


def validate(con):
    total = con.execute("SELECT COUNT(*) FROM star").fetchone()[0]
    ctrl = con.execute("SELECT COUNT(*) FROM star WHERE role='CONTROL'").fetchone()[0]
    if total < MIN_STARS or ctrl != CONTROL_COUNT:
        raise ValueError(f"catálogo inválido: total={total}, control={ctrl}")
