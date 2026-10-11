"""Cifrado de payloads: clave derivada (PBKDF2) de la secuencia; seq_hash = HMAC(secreto, secuencia)."""
import hashlib
import hmac
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KDF_ITERATIONS = 600_000
MIN_SEQUENCE_LEN = 6


def seq_string(seq_ids):
    return ">".join(str(int(i)) for i in seq_ids)


def seq_hash(secret, seq_ids):
    return hmac.new(secret, seq_string(seq_ids).encode(), hashlib.sha256).digest()


def derive_key(seq_ids, salt, iterations=KDF_ITERATIONS):
    return hashlib.pbkdf2_hmac("sha256", seq_string(seq_ids).encode(), salt, iterations, dklen=32)


def encrypt(seq_ids, plaintext, salt, iterations=KDF_ITERATIONS):
    nonce = os.urandom(12)
    return nonce, AESGCM(derive_key(seq_ids, salt, iterations)).encrypt(nonce, plaintext, None)


def decrypt(seq_ids, nonce, ciphertext, salt, iterations=KDF_ITERATIONS):
    """Devuelve el texto plano o None si la secuencia es incorrecta."""
    try:
        return AESGCM(derive_key(seq_ids, salt, iterations)).decrypt(nonce, ciphertext, None)
    except InvalidTag:
        return None
