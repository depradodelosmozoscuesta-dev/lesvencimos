# Balda Varios — Pase 2 (contenido: caja · mapas · fichas ciudad)

**Fecha:** 2026-10-02 (Europe/Madrid)  
**Ámbito:** solo `/workspace/lesvencimos` · sin publish · sin git push · sin APK · sin rebuild `estanteria.html` / EMBEDDED  
**Precedente:** `_balda-varios-pase1.md`

---

## 1. Caja unificada (`caja` embed key intacto)

| Pieza | Decisión |
|---|---|
| Canónica | `modulos/caja-fuerte.html` (fuente; build scripts ya la usan para embed key `caja`) |
| Alias | `modulos/caja.html` = **copia idéntica** (ZIP / file:// / `build-estanteria-offline.py`) |
| Shell | id módulo `caja-fuerte`, `embed: 'caja'` → sin cambio de clave |

**Diff previo:** solo faltaba la brandbar LV en `caja.html` (~567 B).  
**Ahora:** ambos **23 933 B**, `diff` vacío. Comentario HTML bajo `<title>` documenta la regla «no divergir».

### Sync
| Path | Estado |
|---|---|
| `modulos/caja-fuerte.html` | canónica |
| `modulos/caja.html` | idéntica |
| `offline-pack-completo-embed/modulos/caja-fuerte.html` | sync |
| `offline-pack-completo-embed/modulos/caja.html` | sync (creada/igualada) |

**Riesgo:** bajo. Misma lógica PIN + AES-GCM `lv-caja-v1`. Embed inyectado en `estanteria.html` **no** regenerado aquí → Web debe rebuild EMBEDDED.caja si el binario embebido debe llevar esta versión (contenido funcional ya era el de caja-fuerte; solo brandbar + comentario).

---

## 2. Mapas alineados + UX file://

| Copia | Antes | Después |
|---|---:|---:|
| `modulos/mapas.html` | 22 844 | **24 401** |
| `offline-pack-completo-embed/modulos/mapas.html` | 22 844 | **24 401** |
| `…/pack-utiles/modulos/mapas.html` | 22 832 (drift href locales) | **24 401** (unificado) |

**Qué había:** pack-útiles apuntaba en HTML a `valladolid-offline/ABRE-AQUI.html`; modulos/embed a `/downloads/mapas/*.zip` (~12 B + semántica distinta).

**Qué hay:** una sola lógica en JS `setupPacks()`:
- **http(s):** reescribe ZIP relativos según pathname (`../downloads/mapas/`, etc.).
- **file://:** enlaces → «Abrir pack … (local)» al hermano `*/ABRE-AQUI.html`; **no** usa `fetch` (suele fallar en file://); «Abrir pack local» navega al candidato más probable.
- Sin CDN.

### Sync
- `offline-pack-completo-embed/modulos/mapas.html`
- `offline-pack-completo-embed/modules/pack-utiles/modulos/mapas.html`

**Riesgo:** en file://, si el pack no está junto al HTML, el usuario verá error/página en blanco al abrir — mensaje lo dice. En web, comportamiento ZIP intacto.

---

## 3. Fichas ciudad enriquecidas (`guias-viaje/`)

Piloto LEEME: CyL (Va/Sa/Le) + Madrid + Barcelona + Sevilla. Hub pase 1 intacto; aquí **contenido de ficha**.

| Ficha | Antes | Después | Material añadido |
|---|---:|---:|---|
| `…/castilla-y-leon/valladolid.html` | 4 541 | **6 881** | Delicias→Zorrilla/Campo Grande; esquema ascii; orientación; errores; 062; hospitales sin inventar tel. |
| `…/castilla-y-leon/salamanca.html` | 4 214 | **5 722** | Estación→subida casco; Plaza Mayor cero; medio día / un día; errores |
| `…/castilla-y-leon/leon.html` | 4 040 | **5 465** | Tren→Regla; Húmedo/Romántico; Camino; criterio vidrieras |
| `…/madrid/madrid.html` | 4 187 | **5 516** | Atocha/Chamartín/aeropuerto; un museo/día; pickpocket; SAMUR vía 112 |
| `…/cataluna/barcelona.html` | 4 081 | **5 325** | Sants/Prat; mar–montaña; tickets con hora; bolso |
| `…/andalucia/sevilla.html` | 3 851 | **5 165** | Santa Justa; río/Triana; calor; sombra |
| `…/castilla-y-leon/index.html` | 4 286 | **4 326** | Blurbs de tarjeta (pie de calle) |

Estilo: español claro, Les vencimos, sin promesa de más CCAA, sin radios de taxi inventadas.

### Sync fichas
| Destino | Sync |
|---|---|
| `offline-pack-completo-embed/guias-viaje/espana/**` (6 ciudades + index CyL) | sí |
| `offline-pack-completo-embed/modules/pack-utiles/modulos/guias-viaje-espana/espana/**` | sí |

---

## 4. Qué queda (para Web / siguientes)

1. **Rebuild EMBEDDED** / pack completo si el APK/ZIP embebido debe incluir mapas (+ caja brandbar) y, si el embed lleva hub guías, el hub ya venía de pase 1 — las **fichas** van por carpeta `guias-viaje/` (external al iframe embed del hub).  
2. QR: refrescar `CATALOG` embebido si el catálogo creció (sigue pendiente desde pase 1).  
3. Cámara / `openNative` en cascarón (fuera de HTML).  
4. No tocado: APK, `estanteria.html` binario, publish, push, temario Profesor/ESO.

---

## 5. Archivos tocados (este pase)

```
modulos/caja-fuerte.html
modulos/caja.html
modulos/mapas.html
guias-viaje/espana/castilla-y-leon/{valladolid,salamanca,leon,index}.html
guias-viaje/espana/madrid/madrid.html
guias-viaje/espana/cataluna/barcelona.html
guias-viaje/espana/andalucia/sevilla.html
offline-pack-completo-embed/modulos/{caja-fuerte,caja,mapas}.html
offline-pack-completo-embed/modules/pack-utiles/modulos/mapas.html
offline-pack-completo-embed/guias-viaje/espana/** (fichas sync)
offline-pack-completo-embed/modules/pack-utiles/modulos/guias-viaje-espana/espana/** (fichas sync)
_balda-varios-pase2.md
```

---

## 6. Criterios de éxito

- [x] Caja unificada; embed key `caja` sin romper  
- [x] Mapas alineados modulos ↔ pack-utiles (+ UX file:// barata/segura)  
- [x] Varias fichas CyL (+ piloto suelto) materialmente más útiles  
- [x] Informe para entrega a Web  
- [x] Sin publish / sin push / sin APK / sin regenerar EMBEDDED  
