# Balda Varios — Pase 1 (inventario + mejoras offline)

**Fecha:** 2026-10-02 (Europe/Madrid)  
**Ámbito:** solo `/workspace/lesvencimos` · sin publish · sin git push · sin APK  
**Fuente de verdad:** `offline-estanteria/estanteria.shell.html` (`SHELF_LEADS.varios = caja-fuerte`; priority after lead: `calculadora`, `qr`, `mapas`, `camara`)

---

## 1. Inventario completo (shelf: `varios`)

| id | título | archivo(s) | bytes | embed vs external | estado | nota breve |
|---|---|---|---:|---|---|---|
| caja-fuerte | Caja fuerte | `modulos/caja-fuerte.html` (+ `caja.html` 23 226 B, variante) | 23 793 | embed (`caja`) | OK | PIN + AES-GCM localStorage; aviso honesto PIN olvidado. Lead de balda. |
| calculadora | Cálculo | `modulos/calculadora.html` | 14 426 | embed (`calc`) | **mejorado** (antes flojo ~7,5 KB) | Memoria MC/MR/M±, ⌫, √, x², 1/x, historial local. |
| qr | QR | `modulos/qr.html` | 33 606 | embed (`qr`) | OK | Lib QR embebida; Wi‑Fi/URL/módulo; print. Sin CDN. |
| mapas | Mapas | `modulos/mapas.html` + packs `valladolid-offline` / `espana-offline` en pack-útiles | 22 844 | embed (`mapas`) | OK (núcleo) | GPS + rumbo + km + ETA; packs Leaflet vendored. Drift mínimo pack-utiles (22 832 B). |
| camara | Cámara | — | — | openNative / Fotos | OK (dispositivo) | No HTML de módulo; depende del cascarón/APK. |
| protocolo | Protocolo | `modulos/protocolo.html` | 20 446 | embed (`protocolo`) | **mejorado** (antes flojo ~14 KB) | + ruido/vecinos, niños/mayores; libreta con plantillas + export/import. |
| moda | Moda | `modulos/moda.html` | 121 431 | embed (`moda`) | OK | Contenido sustancial; LEEME mínimo. |
| legal-casa | Legal | `modulos/legal-casa.html` | 95 397 | embed (`legal`) | OK | Fiscal Va/CyL 2026 embebido; divulgativo. |
| informatica | Info | `modulos/informatica.html` | 228 989 | embed (`info`) | OK | 14 materias / cultura general (no temario Profesor). |
| guias-viaje | Guías | `modulos/guias-viaje.html` + carpeta `guias-viaje/` (~55 KB) | 9 861 (hub) | embed (`guias`) | **mejorado** (hub offline roto) | Hub reescribe bases file:// → `../guias-viaje/` o `guias-viaje-espana/`. Ciudades piloto CyL + fichas. |
| profesor | Profesor | `profesor.html` | 492 677 | external | **solo-coordinación** | Link `/profesor.html` OK. No reescrito. |
| mate-1eso | Mates | `profesor/1eso-matematicas/1eso-matematicas.html` | 19 808 | external | **solo-coordinación** | Carpeta + lecciones presentes. |
| byg-1eso | Biología | `profesor/1eso-biologia-geologia/…` | 19 577 | external | **solo-coordinación** | OK empaquetado. |
| geo-1eso | Geo e Historia | `profesor/1eso-geografia-historia/…` | 18 356 | external | **solo-coordinación** | OK. |
| lengua-1eso | Lengua | `profesor/1eso-lengua-castellana/…` | 19 986 | external | **solo-coordinación** | OK. |
| plastica-1eso | Plástica | `profesor/1eso-plastica-visual/…` | 16 100 | external | **solo-coordinación** | OK. |
| linux-essentials | Linux | `profesor/linux-essentials/linux-essentials.html` | 12 009 | external | **solo-coordinación** | OK. |
| w-clock | Reloj | widget shell | — | widget | OK | En shell, no HTML suelto. |
| w-clock-lg | Reloj grande | widget shell | — | widget | OK | |
| w-date | Fecha | widget shell | — | widget | OK | |
| w-dia | ¿Qué día es? | widget shell | — | widget | OK | |
| w-cal | Calendario | widget shell | — | widget | OK | |
| w-ori | Orientación | widget shell | — | widget | OK | |

**Conteo:** 17 módulos de catálogo + 6 widgets = **23 ítems** en balda Varios.  
**Educación (external):** 7 ítems · estado empaquetado OK en `profesor/` y `offline-pack-completo-embed/modules/pack-1eso/educacion/` (también `Profesor.html` en pack). **No se reescribió temario.**

---

## 2. Análisis de flojos (no-escolares)

### Prioridad antes del pase

| # | Módulo | Por qué flojo | Hueco vs LEEME/promesa |
|---|---|---|---|
| 1 | **calculadora** (~7,5 KB) | Solo +−×÷ % ±; sin ⌫, sin memoria, sin historial | LEEME promete «dedos / botones grandes» pero utilidad mínima frente a calculadora del sistema |
| 2 | **guias-viaje hub** (~5,6 KB) | En `file://` el script **desactivaba** todas las tarjetas aunque el pack sí tenía rutas relativas | LEEME: abrir desde Archivos offline; hub mentía / bloqueaba |
| 3 | **protocolo** (~14 KB) | Patrones útiles pero cortos; libreta solo alta/baja | LEEME: casa/calle/visita/duelo + libreta; faltaban ruido, niños, plantillas, backup |
| 4 | **mapas** núcleo | Funcional; packs aparte | LEEME OK; mejora futura = mejor descubrimiento de packs en file:// |
| 5 | **caja-fuerte / qr / moda / legal / info** | Sustanciales | No prioritarios en pase 1 |

### Top mejoras hechas (este pase)

1. Calculadora usable offline (memoria + historial + unarios).  
2. Hub guías con rutas relativas según contexto (web / modulos / pack-útiles) — **sin matar enlaces en file://**.  
3. Protocolo ampliado + libreta con plantillas y export/import JSON.

---

## 3. Qué se mejoró (diff resumen)

### `modulos/calculadora.html` (7 519 → 14 426 B)
- Filas MC / MR / M+ / M−; C + ⌫; √, x², 1/x.
- Historial (hasta 30) en `localStorage` `lv-calc-hist-v1`; tap para reutilizar resultado.
- Memoria persistente `lv-calc-mem-v1`.
- Teclado: Backspace, Escape, Enter.
- Estilo LV (carbón/ámbar), sin CDN.

### `modulos/guias-viaje.html` (5 617 → 9 861 B)
- Eliminado el comportamiento que quitaba `href` en `file://`.
- Resolución de base: `https?` → `/guias-viaje/`; pack-útiles → `guias-viaje-espana/`; `modulos/` → `../guias-viaje/`.
- Blurbs por ciudad, teléfonos 112/091/092, nota de uso offline.
- Botón ZIP → `ABRE-AQUI.html` cuando aplica layout pack.

### `modulos/protocolo.html` (14 408 → 20 446 B)
- Nuevas secciones: **Ruido y vecinos**, **Niños y mayores**; fichas llaves/nevera/préstamo/quedarse.
- Tabla «cómo se acuerda».
- Libreta: 6 plantillas; export/import JSON; vaciar con confirmación.

### Sincronización packs
| Destino | Sync |
|---|---|
| `offline-pack-completo-embed/modules/pack-utiles/modulos/calculadora.html` | sí |
| `offline-pack-completo-embed/modules/pack-utiles/modulos/guias-viaje.html` | sí |
| `offline-pack-completo-embed/modules/pack-casa/modulos/protocolo.html` | sí |
| `offline-pack-completo-embed/modulos/{calculadora,guias-viaje,protocolo}.html` | sí |
| Copias `calculadora.html` bajo `**/educacion/**` (embed + `offline-pack-completo`) | sí (20+10) — utilidad compartida, no temario |

### Pendiente de sync / drift
- `mapas.html`: pack-utiles 22 832 vs modulos/embed 22 844 (drift previo; **no tocado** este pase).
- `caja.html` ≠ `caja-fuerte.html` (dos variantes; shell embebe `caja` → id `caja-fuerte`). Revisar unificación en pase 2.
- `estanteria.html` / `EMBEDDED` inyectado: rebuild del pack completo **no** hecho aquí (sin publish). El agente Web debe regenerar embed si el APK/ZIP completo debe llevar estos HTML.

---

## 4. Educación — solo coordinación

| Check | Resultado |
|---|---|
| `profesor.html` | OK (492 KB) |
| Links shell → `/profesor/1eso-*/…` | Archivos existen |
| `profesor/linux-essentials/` | OK |
| Pack `pack-1eso/educacion/` | Carpetas 1eso + `Profesor.html` presentes |
| Acción contenido | **Ninguna** (no reescritura temario ESO/Profesor) |

---

## 5. Qué queda (pase 2 recomendado)

1. **Rebuild embed** de estantería/pack completo para que `EMBEDDED.calc|guias|protocolo` lleven las versiones nuevas (si el flujo Web lo exige).  
2. Unificar o documentar `caja.html` vs `caja-fuerte.html`.  
3. Alinear `mapas.html` pack-utiles ↔ modulos (12 B drift + UX packs en file://).  
4. Enriquecer fichas ciudad en `guias-viaje/` (siguen ~4 KB; piloto honesto pero corto).  
5. QR: refrescar `CATALOG` embebido si el catálogo de estantería ha crecido.  
6. Cámara: verificar `openNative` en cascarón (fuera de este pase HTML).

---

## 6. Archivos tocados

```
modulos/calculadora.html
modulos/guias-viaje.html
modulos/protocolo.html
offline-pack-completo-embed/modules/pack-utiles/modulos/calculadora.html
offline-pack-completo-embed/modules/pack-utiles/modulos/guias-viaje.html
offline-pack-completo-embed/modules/pack-casa/modulos/protocolo.html
offline-pack-completo-embed/modulos/calculadora.html
offline-pack-completo-embed/modulos/guias-viaje.html
offline-pack-completo-embed/modulos/protocolo.html
offline-pack-completo-embed/**/educacion/**/calculadora.html  (×20)
offline-pack-completo/**/educacion/**/calculadora.html       (×10)
_balda-varios-pase1.md  (este informe)
```

**No tocado:** APK, git push, publish, lecciones ESO, `profesor/*` temario, `estanteria.html` binario embebido.

---

## 7. Criterios de éxito

- [x] Inventario completo Varios  
- [x] ≥2 módulos no-escolares materialmente mejorados (calculadora, guías, protocolo = 3)  
- [x] Informe listo para entrega a Web  
- [x] Sin publicar / sin push  
