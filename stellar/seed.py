"""Crea una BD demo: catálogo + árbol de menú + un mensaje oculto."""
from stellar.catalog import loader
from stellar.engine.sequence import SequenceEvaluator


def build_demo(path=":memory:", secret=b"demo-secret", salt=b"demo-salt-16bytes", iterations=600_000):
    con = loader.connect(path)
    loader.create_schema(con)
    loader.load_catalog(con)
    sid = lambda n: con.execute("SELECT id FROM star WHERE name=?", (n,)).fetchone()[0]
    with con:
        con.execute("INSERT INTO menu_node(id,parent_id,label,hint) VALUES(1,NULL,'Inicio','Apunta al norte y localiza Casiopea')")
        con.execute("INSERT INTO menu_node(id,parent_id,label,hint) VALUES(2,1,'Casiopea','Ahora busca Andrómeda')")
        con.execute("INSERT INTO menu_node(id,parent_id,label,hint,is_leaf) VALUES(3,2,'Andrómeda','Confirma con Sirio',1)")
        con.execute("INSERT INTO menu_edge VALUES(1,?,2)", (sid("Schedar"),))
        con.execute("INSERT INTO menu_edge VALUES(2,?,3)", (sid("Mirach"),))
    ev = SequenceEvaluator(con, secret, salt, iterations)
    seq = [sid(n) for n in ("Schedar", "Mirach", "Almach", "Caph", "Alpheratz", "Ruchbah")]
    ev.add_payload(seq, "¿Quieres casarte conmigo?".encode("utf-8"))
    return con, ev, seq
