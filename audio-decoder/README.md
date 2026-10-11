# audio-decoder

Decodificador local (sin nube) de ráfagas de acordes delimitadas por silencios.

- `acordes/chords.py`: espacio de 2^24 acordes (6 voces × 16 tonos, 1–6,75 kHz, igual que `audio-imagen/codec.js`) y análisis FFT.
- `acordes/segmenter.py`: umbral de amplitud (RMS), silencio = delimitador de bloque, k = nº de elementos, orden de llegada.
- `acordes/permutation.py`: rango/permutación del orden (k!, o k!/∏m! con repetidos).
- `acordes/router.py`: tabla extensible bloque → acción (`on_sequence`, `on_set`, `on_length`, `default`).
- `acordes/audio_io.py`: WAV, micrófono (`sounddevice` opcional) y simulador.

Cada acorde dura `--sym-dur` (60 ms por defecto); los acordes de un bloque van seguidos y los bloques se separan con ≥30 ms de silencio.

```
pip install -r requirements.txt
python -m acordes.cli demo
python -m acordes.cli decode archivo.wav
python -m acordes.cli mic 10
python -m unittest discover tests
```
