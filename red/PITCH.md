# Red Ciudadano Valladolid — pitch escaparate

Red ciudadana **local** para Valladolid: mapa de lugares (sin URLs ni ranking de pago), avisos, prensa en hojas **`.pucela`**, mensajes y **taller** comunitario. Peer-to-peer en el barrio; sin nube obligatoria.

> **Mensaje comercial:** solo red cívica. **No** incluir VitaInk ni juego en el copy de producto.

## Qué enseña el escaparate

- Directorio táctil de lugares (biblioteca, hospital, ayuntamiento, prensa…)
- Calles / mapa / lista — misma ciudad, sin GPS comercial
- Casa privada, mensajes, envíos ligeros
- Formato ciudadano `.pucela` y taller federable

## Demo completa (recomendada)

Desde el repo privado del nodo:

```bash
make run-civic
```

Abre `http://127.0.0.1:8080/`. El binario cívico (`-tags novitaink`) no monta el plugin de juego.

Guías en `docs/ARRANQUE.md` y `docs/RECORRIDO-10MIN.md` (usa solo la **Parte A — Solo cívico**).

## Cáscara PWA estática (opcional)

`red-ciudadano-pwa-static.zip` contiene la UI web **sin** la carpeta de juego embebida. Es un **visual shell**: para API real (lugares, chat, prensa, taller) hace falta el nodo Go.

Ver `README-PWA-STATIC.md` junto al zip.
