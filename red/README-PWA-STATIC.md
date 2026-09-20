# PWA estática — Red Ciudadano Valladolid (cáscara visual)

Contenido: assets de `web/` (HTML/CSS/JS, icons, service worker, manifest) **sin** la carpeta de juego embebida.

## Qué es

Una **cáscara visual** de la PWA ciudadana. Útil para enseñar layout y flujo en un hosting estático o `npx serve`.

## Qué NO es

No sustituye al nodo. Las rutas `/api/*` (lugares, mensajes, prensa `.pucela`, taller, federación) las sirve el binario Go.

## Demo completa

En el repositorio privado del nodo:

```bash
make run-civic
```

Eso arranca el núcleo cívico en `http://127.0.0.1:8080/` (sin plugin de juego).

## Abrir solo la cáscara

```bash
unzip red-ciudadano-pwa-static.zip
cd web
npx serve .
```

Las llamadas a API fallarán o quedarán vacías sin el nodo en marcha.
