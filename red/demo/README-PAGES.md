# Red Ciudadano Valladolid — pack Pages (demo cívico)

Cáscara PWA **estática** lista para GitHub Pages / hosting estático en:

**`https://lesvencimos.com/red/demo/`**

## Qué incluye

- `index.html`, `css/`, `js/`, `icons/`, `manifest.webmanifest`, `sw.js`
- `js/mock-api.js` — intercepta `fetch` a `/api/*` con fixtures de Valladolid
- Sin carpeta VitaInk / sin assets de juego
- Mensaje comercial **solo cívico** (chips VitaInk ocultos por CSS)

## Base y rutas de assets

```html
<base href="/red/demo/">
```

Los CSS/JS/iconos/manifest usan rutas **relativas** (`css/app.css`, `js/app.js`, …) para que resuelvan bajo `/red/demo/` y no en la raíz del dominio (evita el 404 que dejaba el HTML “en bruto” y parecía “solo el asistente”).

## Capa mock (límites honestos)

`mock-api.js` responde, entre otros:

| Endpoint | Contenido demo |
|----------|----------------|
| `GET /api/health`, `/api/whoami` | Nodo/demo ficticio |
| `GET /api/places` (+ `?q=`) | ~31 lugares de Valladolid |
| `GET /api/places/{id}` y `.../page` | Ficha + secciones + asistente FAQ stub |
| `GET /api/peers` | Lista vacía |
| `GET /api/citymap` | Pines esquemáticos |
| `GET /api/city/*` | Listas vacías / stubs |
| `GET /api/campana` | Sin avisos |
| `GET/POST /api/chat/*`, contactos, etc. | Vacíos |
| `/api/vitaink/*` | **404** (demo cívico, sin juego) |

**No sustituye al nodo Go.** Chat E2E, depósito, federación viva, prensa firmada, taller, casa, etc. no funcionan de verdad en Pages.

Demo completa con API real (repo privado del nodo):

```bash
make run-civic
# → http://127.0.0.1:8080/
```

## Vista por defecto

Arranca en **mapa** (home / lugares / mapa), no en el asistente ni en calles-first.

## Despliegue sugerido

1. Sube el contenido de esta carpeta (o del zip) a la ruta pública `/red/demo/`.
2. Asegura que `index.html` quede en `/red/demo/index.html`.
3. No hace falta backend.

Vista previa local (desde esta carpeta, simulando la base):

```bash
# Opción A: servir con path /red/demo/
mkdir -p /tmp/pages-root/red && cp -a . /tmp/pages-root/red/demo
npx --yes serve /tmp/pages-root -p 4173
# abrir http://127.0.0.1:4173/red/demo/
```

## Origen

Copia de trabajo desde `nuevo-internet/red-ciudadano-valladolid/web/` (sin `vitaink/`), adaptada en `escaparate-lesvencimos/`. **No** modifica `/workspace/lesvencimos` ni el repo fuente.

Fecha: 2026-09-20 (Europe/Madrid).
