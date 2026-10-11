"""Evaluación de una secuencia de estrellas contra la tabla payload."""
from . import crypto


class SequenceEvaluator:
    def __init__(self, con, secret, salt, iterations=crypto.KDF_ITERATIONS):
        self.con, self.secret, self.salt, self.iterations = con, secret, salt, iterations

    def add_payload(self, seq_ids, plaintext, kind="text", media_path=None):
        nonce, ct = crypto.encrypt(seq_ids, plaintext, self.salt, self.iterations)
        with self.con:
            self.con.execute(
                "INSERT INTO payload(seq_hash,kind,nonce,ciphertext,media_path) VALUES(?,?,?,?,?)",
                (crypto.seq_hash(self.secret, seq_ids), kind, nonce, ct, media_path))

    def evaluate(self, seq_ids):
        """Devuelve {'kind','data','media_path'} o None (sin distinguir causa del fallo)."""
        row = self.con.execute(
            "SELECT kind,nonce,ciphertext,media_path FROM payload WHERE seq_hash=?",
            (crypto.seq_hash(self.secret, seq_ids),)).fetchone()
        if not row:
            return None
        data = crypto.decrypt(seq_ids, row["nonce"], row["ciphertext"], self.salt, self.iterations)
        if data is None:
            return None
        return {"kind": row["kind"], "data": data, "media_path": row["media_path"]}
