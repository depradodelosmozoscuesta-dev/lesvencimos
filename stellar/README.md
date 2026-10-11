# StellarMessenger

Mensajería 100% offline que usa el cielo como puntero. Python 3.10+ y `cryptography`.

- `catalog/`: `schema.sql`, `stars.csv` (112 estrellas, 20 de control), loader y repo.
- `astro/`, `sensors/`, `vision/`: coordenadas, fusión de sensores, detección y calibración.
- `engine/`: máquina de estados (dwell 1,5 s, snap 4°), cifrado AES-GCM + PBKDF2, evaluación de secuencias.
- `ui/`, `app.py`: guía, revelado y demo CLI.

Ejecutar: `python3 -m stellar.app` · Tests: `python3 -m unittest stellar.tests.test_stellar`

Nota: la demo usa secuencias de 6 pasos; el secreto de la app debe guardarse en el keystore del dispositivo.
