# Imagen por audio

Prototipo web: transmite imágenes como audio. Cada símbolo es un acorde de 6 voces (una por banda de 1 kHz), con 16 tonos posibles por voz → 16^6 = 16.777.216 variaciones (3 bytes) por acorde.

Paquete: `IM` + ancho + alto + píxeles de 4 bits + CRC16. Precede un doble acorde de sincronía.
Prueba del códec: `node test.js`.
