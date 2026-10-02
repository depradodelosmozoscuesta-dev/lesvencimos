# Balda Salud — pase 1 (Jorge/Web)

Fecha: 2026-10-02 (Europe/Madrid). Trabajador: Balda Salud LV.  
Ámbito: inventario + flojos + mejoras offline en working tree.  
**Sin publicar, sin git push, sin tocar producción remota.**

## 1. Inventario

Referencia estantería (`offline-estanteria/estanteria.shell.html`):

- Shelf `salud`: `medicacion`, `gimnasio`, `alto-rendimiento`, `primeros-auxilios`, `higiene`
- Icono hub `salud` → embed `modulos/salud.html` («Pastillas y médicos»)
- Pack-casa nota: «salud básica»; casa shelf también lista `salud` + `medicacion` + `primeros-auxilios` + `higiene`

| Módulo | Path | Tamaño HTML | Catálogo | ZIP offline | Shelf |
|--------|------|-------------|----------|-------------|-------|
| salud | `modulos/salud.html` | 28054 | sí (añadido) | `downloads/salud-offline.zip` (9152) | salud (hub) |
| medicacion | `modulos/medicacion.html` | 11612 | sí (actualizado) | `downloads/medicacion-offline.zip` (4437) | salud |
| primeros-auxilios | `modulos/primeros-auxilios.html` | 51322 | sí | `downloads/primeros-auxilios-offline.zip` | salud |
| higiene | `modulos/higiene.html` | 71206 | sí (añadido) | `downloads/higiene-offline.zip` (21362) | salud |
| gimnasio | `modulos/gimnasio.html` | 286484 | sí | `downloads/gimnasio-offline.zip` | salud |
| alto-rendimiento | `modulos/alto-rendimiento.html` | 423776 | sí (añadido) | `downloads/alto-rendimiento-offline.zip` | salud |

LEEME:

- `modulos/LEEME-salud.txt` (actualizado v20261002a)
- `modulos/LEEME-medicacion.txt` (actualizado)
- `modulos/LEEME-primeros-auxilios.txt` (sin cambio este pase)
- `modulos/LEEME-higiene.txt` (**creado**)
- `modulos/HIGIENE-INDICE.md` (ya existía)
- Gimnasio / alto-rendimiento: LEEME propios; no reescritos (especialista Gimnasio)

Embed pack completo: `offline-pack-completo-embed/modulos/{salud,medicacion,primeros-auxilios,higiene,gimnasio,alto-rendimiento}.html`  
Tras este pase: `salud.html` y `medicacion.html` sincronizados con `modulos/`.

Descargas web (`descargas.html`): ya enlazaba `salud-offline`, `higiene-offline`, `alto-rendimiento-offline` aunque el catálogo no los listaba.

### localStorage (coherencia)

| Clave | Rol |
|-------|-----|
| `lv-medicacion-v1` | Lista de medicinas (fuente de verdad compartida Salud ↔ Medicación) |
| `lv-med-check-YYYY-MM-DD` | Checklist del día (canónico) |
| `lv-salud-docs-v1` | Médicos / centros |
| `lv-salud-reports-v1` | Informes / notas |
| `lv-salud-hist-v1` | Historial de tomas marcadas en Salud |
| `lv-salud-meds-v1` | Legado (solo migrate → medicacion) |
| `lv-salud-check-*` | Legado (migrate one-shot → `lv-med-check-*`) |
| `lv-salud-meds-migrated-v1` / `lv-salud-checks-migrated-v1` | Flags migrate |
| `lv-salud-simple` / `lv-med-simple` | Modo letras grandes |

## 2. Flojos priorizados (antes del pase)

1. **Catálogo incompleto:** faltaban `salud`, `higiene` y `alto-rendimiento` en `catalogo.json` y `app/catalogo.json` (sí había ZIP + ficha en descargas + icono en estantería).
2. **ZIP `salud-offline.zip` desfasado:** HTML del zip ~18.5 KB vs disco ~20.5 KB (pre-mejora); LEEME del zip sin documentar migrate/keys.
3. **Bug historial:** pestaña Historial leía `lv-salud-hist-v1` pero marcar pastillas **nunca escribía** ahí → historial siempre vacío.
4. **Enlace cruzado incompleto:** Salud → Medicación sí; Medicación → Salud no.
5. **UX Salud:** sin modo sencillo, sin export/import, hub sin atajos a Primeros auxilios / Higiene.
6. **ZIP `higiene`:** HTML zip ligeramente viejo (~70.6 vs 71.2 KB); sin `LEEME-higiene.txt` en repo.
7. **Presets:** `midia`/`casa` no listaban el hub `salud` (ni higiene en casa).
8. **Gimnasio / alto-rendimiento:** en shelf Salud pero catálogo sin alto-rendimiento; coherencia de enlace/temario dejada al especialista Gimnasio (solo nota + entrada de catálogo).

No tocado a fondo (y OK de momento): disclaimers + 112 en Salud/Medicación/Primeros; temario PA = cultura general; lecciones ESO.

## 3. Mejoras aplicadas (este pase)

1. **Catálogo** — `catalogo.json` + `app/catalogo.json`:
   - Entradas nuevas: `salud`, `higiene`, `alto-rendimiento` (id, nombre, version `20261002a`, url zip, entrada, publico, nota, bytes del zip).
   - Presets: `salud` en midia/casa; `higiene` en casa.
   - `medicacion` version bump a `20261002a` + bytes del zip rebuild.

2. **`modulos/salud.html`**
   - Arreglo historial: al marcar una toma se hace `pushHist` → `lv-salud-hist-v1`.
   - Modo sencillo (letras grandes; respeta `lv-salud-simple` / `lv-med-simple`).
   - Export / import JSON (toolbar + pestaña Datos); documenta claves localStorage en UI.
   - Hub: enlaces cruzados a Medicación, Primeros auxilios, Higiene (`postMessage` lvOpen o `*.html`).
   - Eliminada lista muerta `MEDS_DEF` (nombres de fármacos sin uso; evita menú implícito).
   - Disclaimer 112 reforzado en hub/datos.

3. **`modulos/medicacion.html`**
   - Enlace «Abrir Salud (médicos e informes)» + `postMessage` en embed.

4. **LEEME**
   - Actualizados `LEEME-salud.txt`, `LEEME-medicacion.txt`.
   - Creado `LEEME-higiene.txt`.

5. **ZIPs rebuild** (archivos en raíz del zip, como el resto):
   - `downloads/salud-offline.zip`
   - `downloads/medicacion-offline.zip`
   - `downloads/higiene-offline.zip`

6. **Embed sync:** `offline-pack-completo-embed/modulos/salud.html` y `medicacion.html`.

## 4. Pendientes recomendados

- Rebuild / rehash de **pack-completo** / pack-casa si se quiere que el zip gordo lleve ya estos HTML (este pase solo actualizó el embed suelto + zips de módulo).
- Especialista **Gimnasio**: coherencia de copy/enlaces Salud ↔ gimnasio ↔ alto-rendimiento (sin reescribir temario aquí).
- Primeros auxilios: pase de contraste/modo sencillo + enlace de vuelta a Salud (opcional).
- Higiene: enlace explícito a Salud dentro del HTML + LEEME en zip ya hecho; revisar permisos de archivo (`rw-------` en higiene.html).
- Historial: opcionalmente volcar también desde Medicación al marcar (hoy solo Salud escribe `lv-salud-hist-v1`).
- Actualizar capturas brand (`brand/capturas/captura-medicacion.png`, etc.) si se publica UI.
- Commit local cuando Jorge/Web lo pidan (working tree listo; **no** push).

## 5. Seguridad de contenido

- Sin dosis prescritas, sin «tómate X», sin diagnóstico.
- Disclaimers + 112 mantenidos/reforzados.
- Primeros auxilios no reescrito (sigue aviso de curso oficial).
- Datos solo localStorage / file:// / export JSON local.

## 6. Archivos tocados (lista corta)

- `catalogo.json`, `app/catalogo.json`
- `modulos/salud.html`, `modulos/medicacion.html`
- `modulos/LEEME-salud.txt`, `LEEME-medicacion.txt`, `LEEME-higiene.txt` (nuevo)
- `downloads/salud-offline.zip`, `medicacion-offline.zip`, `higiene-offline.zip`
- `offline-pack-completo-embed/modulos/salud.html`, `medicacion.html`
- `_balda-salud-mitad.txt`, `_balda-salud-pase1.md` (este informe)
