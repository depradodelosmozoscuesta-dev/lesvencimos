# Balda Varios LV · Mapa metro Valladolid (máximo OSM offline)

**Fecha:** 2026-10-02 (Europe/Madrid)  
**Ámbito:** `/workspace/lesvencimos` · **sin** publish · **sin** git push · **sin** APK · **sin** rebuild `EMBEDDED` / `estanteria.html`  
**Encargo:** Jorge — mapa COMPLETO máximo posible solo área metro VA; luego decidir ampliar.

---

## 1. Bbox y fuente

| | |
|---|---|
| **Bbox** | lon **−4.95…−4.55** · lat **41.52…41.78** |
| **Cobertura** | Valladolid ciudad + Laguna de Duero + La Cistérniga + Arroyo de la Encomienda, Simancas, Zaratán, Santovenia de Pisuerga, Tudela de Duero, Fuensaldaña, Villanubla (y anillo inmediato) |
| **Fuente** | Geofabrik `castilla-y-leon-260930.osm.pbf` (177 519 551 B, HTTP 200) → `osmium extract` → filtro tags → GeoJSON + grafo |
| **Overpass** | Falló (TLS EOF / timeout en overpass-api.de y kumi). **No bloqueó:** Geofabrik + osmium OK |
| **Extracto metro PBF** | `metro-va-raw.osm.pbf` ≈ **5,9 MiB** (work: `_parade-work/mapas-metro-va/`) |

---

## 2. Features y peso (honesto)

### Pack `valladolid-offline` (una copia)

| Archivo | Bytes | MiB |
|---|---:|---:|
| `data.geojson` | 12 024 981 | **11,47** |
| `routing-graph.json` | ≈ 4 087 000 | **3,90** |
| `mapa.html` = `ABRE-AQUI.html` | ≈ 38 KB | 0,04 |
| `vendor/` (Leaflet) | ≈ 150 KB | 0,15 |
| **Total pack** | | **≈ 15,6 MiB** |
| ZIP `downloads/mapas/valladolid-offline.zip` | 3 219 115 | **3,07** |

**Techo mid ~30–40 MiB:** **no se supera** (una copia ~16 MiB). Triple sync ≈ 47 MiB en disco (intencional hermanos modulos/embed/pack-útiles). **No hace falta recorte ahora**; opciones de recorte abajo si en móvil va lento.

### Contenido GeoJSON (41 521 features)

| Capa | Cantidad (aprox.) |
|---|---:|
| LineStrings (calles/agua/rail) | 29 551 |
| Points POI/lugares | 11 090 |
| Edificios nombrados (centroide) | 880 |
| **footway** | **5 577** (antes: 0) |
| path / steps / service | 1 481 / 340 / 3 342 |
| residential + resto calzada | como extracto previo + densificación |
| waterway / railway | ríos/arroyos/canales · rail+estaciones |
| restaurant / cafe / bar / pub | **445 / 176 / 106 / 528** (antes casi 0 hostelería) |
| pharmacy / school / fuel / supers… | densos según OSM |

**Edificios:** solo centroides con `name` (no huellas poligonales — peso).  
**Sin tiles raster OSM.**

### Grafo routing embebido

| | |
|---|---|
| Modo | Peatonal (walk) |
| Nodos | 62 185 |
| Aristas | 134 298 |
| Peso | ≈ 3,9 MiB |
| Algoritmo UI | snap ≈120–140 m + **A\***; fallback línea recta |
| Honestidad | **No es OSRM/Maps**: sin voz, sin tráfico, tracks rurales fuera del grafo, coste heurístico |

---

## 3. UX actualizada

- Capas: calles (incl. footways verdes) / agua / rail / POI / lugares  
- Chips: farmacias, salud, gasolineras, supers, **bares/rest.**, colegios, turismo, **edif. nombrados**  
- «Ir a»: ruta peatonal sólida si grafo+snap OK; discontinua si recta  
- Zoom útil **10–18**  
- Aviso de peso en `LEEME.txt`, subtítulo mapa y tarjeta `mapas.html`

---

## 4. Sync ×3 + ZIPs

| Copia | Ruta | Tamaño |
|---|---|---|
| modulos | `modulos/valladolid-offline/` | ≈16 MiB |
| embed/modulos | `offline-pack-completo-embed/modulos/valladolid-offline/` | idem |
| pack-utiles | `offline-pack-completo-embed/modules/pack-utiles/modulos/valladolid-offline/` | idem |

También: `mapas.html` ×3 · `LEEME-mapas.txt` · pack-útiles `LEEME.txt` (tamaño) · `downloads/mapas/LEEME.txt`

ZIPs:

- `downloads/mapas/valladolid-offline.zip` (3,07 MiB)  
- `downloads/mapas/valladolid-offline-v20261002e.zip` (alias)

**md5 `data.geojson` (×3):** `552dd72c3b685423961b93e316b8bc5b`

---

## 5. Recorte (oferta, no aplicado)

Si en tablet/móvil el pack ~16 MiB se nota pesado, o se quiere ampliar provincia sin pasar ~30–40 MiB:

1. **Quitar `routing-graph.json`** (−3,9 MiB) → vuelve «Ir a» solo línea recta.  
2. **Quitar edificios nombrados** (−~880 pts).  
3. **Quitar `track` / parte de `service`** del GeoJSON.  
4. **Recortar bbox** al núcleo ciudad (p. ej. −4.82…−4.66 / 41.58…41.72).  
5. Ampliar después a Cigales/Cabezón/etc. con segunda capa o bbox mayor.

---

## 6. No tocado (por encargo)

- publish web · git push · APK · rebuild `estanteria.html` / `EMBEDDED.*` gigante  
- `pack-utiles-offline.zip` catálogo completo (solo datos en carpeta embed)

---

## 7. Cómo probar

1. Abrir `modulos/valladolid-offline/ABRE-AQUI.html`  
2. Capas: ver footways verdes; chip «Bares/Rest.»  
3. Buscar p. ej. «Zorrilla» o un bar → «Ir a» + «Seguir GPS» → polyline por calles si hay grafo  
4. Comprobar peso: LEEME / subtítulo / tarjeta Mapas

