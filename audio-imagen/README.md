# Imagen por audio

Prototipo web: transmite imágenes como audio. Cada símbolo es un acorde de 6 voces (una por banda de 1 kHz), con 16 tonos posibles por voz → 16^6 = 16.777.216 variaciones (3 bytes) por acorde.

Paquete: `IM` + ancho + alto + píxeles de 4 bits + CRC16. Precede un doble acorde de sincronía.
Prueba del códec: `node test.js`.

## Colores
`colores.js`: paleta de 1.000.000 colores (100 niveles/canal). `Colores.analyze(rgba,w,h)` devuelve nº de píxeles, colores distintos y las posiciones (x,y) de cada color. Prueba: `node test-colores.js`.

## Bloques (bloques.js)
Paleta reducida a ~100.000 colores (46³ = 97.336). La imagen se trocea en bloques 8×8 en orden de lectura (la posición se deduce, no se envía). Cada bloque es un símbolo/acorde: `FLAT` (color liso), `GRAD` (gradiente exacto: color base + pendiente por canal), `REF` (bloque ya enviado, diccionario adaptativo) o `RAW`. Reconstrucción exacta respecto a la paleta. Prueba: `node test-bloques.js`.
