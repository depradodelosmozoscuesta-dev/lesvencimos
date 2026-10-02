# Balda Varios LV · Mapas Valladolid · prototipo «Ir a»

**Fecha:** 2026-10-02 (Europe/Madrid)  
**Alcance:** pack `valladolid-offline` + nota mínima en `mapas.html`  
**Hecho (2026-10-02):** publish web + sync ×3 + ZIP valladolid + pack-útiles. Sin APK. Merge sobre mapa con capas/chips/deep-link (no sustituir por prototipo suelto).

## Qué se añade

En `mapa.html` = `ABRE-AQUI.html`:

- Elegir destino: tap en mapa, botón «Ir a aquí» en popup POI/calle, o buscar POI/calle del GeoJSON (sugerencias) → «Ir a».
- Línea recta GPS→destino (polyline discontinua), distancia (m/km), ETA a pie (~5 km/h) y coche urbano (~30 km/h).
- «Seguir GPS» (`watchPosition`) actualiza posición, línea y ETA; «Parar» corta el watch; «Quitar destino» limpia.
- Aviso UI: **no es navegación tipo Maps** (sin routing calle-a-calle, sin voz, sin CDN; Leaflet vendored).

## Paths (sync ×3)

| Copia | Ruta |
|-------|------|
| modulos | `modulos/valladolid-offline/` |
| embed/modulos | `offline-pack-completo-embed/modulos/valladolid-offline/` |
| pack-utiles | `offline-pack-completo-embed/modules/pack-utiles/modulos/valladolid-offline/` |

Archivos tocados en cada copia: `mapa.html`, `ABRE-AQUI.html`, `LEEME.txt` (datos/vendor sin cambio).

`mapas.html` (nota en tarjeta Valladolid) ×3:

- `modulos/mapas.html`
- `offline-pack-completo-embed/modulos/mapas.html`
- `offline-pack-completo-embed/modules/pack-utiles/modulos/mapas.html` (href local al pack conservado)

Informe: `_balda-varios-mapas-ir-a.md` (este).

## Límites (honesto)

- Solo **línea recta**; no sigue calles ni evita obstáculos.
- ETA orientativas (5 / 30 km/h); tráfico, semáforos y desvíos no entran.
- Calles en búsqueda usan **punto medio** del LineString, no portal.
- GPS depende del navegador/permisos; en `file://` algunos WebView limitan geolocalización.
- ZIP `downloads/mapas/valladolid-offline.zip` regenerado.
- `downloads/pack-utiles-offline.zip` (+ alias v20261002d) regenerado.

## Cómo probar

1. Abrir `modulos/valladolid-offline/ABRE-AQUI.html` (o la copia en pack-utiles) en Chrome.
2. Buscar p. ej. «Zorrilla» → «Ir a», o tocar el mapa.
3. «Seguir GPS» → conceder ubicación → ver línea y ETA; «Parar».
