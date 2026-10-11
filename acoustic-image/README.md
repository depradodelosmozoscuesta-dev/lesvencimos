# acoustic-image

Compresión, transmisión acústica simulada y reconstrucción de imágenes (100 % local).

- `encoder/`: `gradient.py` detecta bloques 8×8 que son un plano (base + dx·x + dy·y) y se envían como fórmula; `peeling.py` hace *Color Peeling* con el resto (color dominante → máscara sí/no por RLE → retirar píxeles → repetir; la última capa no necesita máscara). Si hay más de `max_layers` colores se cuantiza (con pérdida).
- `audio_protocol/`: `chords.py` (2^24 acordes, 6 voces × 16 tonos), `bursts.py` (flujo → ráfagas de 8 acordes; el **orden de llegada** es una permutación de 8 ranuras cuyo rango, hasta 8! = 40320, lleva el nº de secuencia gratis; CRC32), `channel.py` (audio simulado; el silencio delimita ráfagas y se cuenta el nº de elementos).
- `decoder/reconstruct.py`: aplica gradientes y capas acumulativas.
- `database/models.py`: SQLite/SQLAlchemy con el abecedario de 4096 acordes base (cada color de 24 bits = pareja de acordes base, 4096² = 16.777.216), transmisiones y capas.
- `api/app.py`: FastAPI (`/send`, `/packets/{id}`, `/receive`).

```
pip install -r requirements.txt
python run_e2e.py [imagen]            # end-to-end con audio simulado
python -m unittest discover tests
uvicorn api.app:app
```
El error máximo por canal es ≤ `tol` (1 por defecto) en bloques de gradiente; las capas de color son exactas mientras haya ≤ 64 colores fuera de gradientes.
