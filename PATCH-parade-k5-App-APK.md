# PATCH parade k5 — App APK / Completo (1 oct 2026 ~02:53 CEST)

## Causa raíz (para Jorge)

El PWA Completo (stamp k3) **sí** mueve iconos porque tiene `ensureShelfIconsOverflow` (clones «ghost» + reinicio al volver + pausa 5s).

En APK/WebView la desfilada fallaba así:

1. **Fat Completo 2.0.0** (`com.lesvencimos.cascaron`) ya llevaba lógica k3 en `assets/embed/completo-offline.zip`, pero en **WebView** a menudo `scrollWidth` no crece al clonar iconos → el parade cree que no hay overflow y **no arranca**. Además, si la app ya se abrió antes, el marker `.lv-extracted=v20261001embed` **no re-extraía** un ZIP nuevo al actualizar.
2. El proyecto `lesvencimos/android-apk` (WebView de prueba) tenía parade **viejo** (sin `ensureShelfIconsOverflow`).
3. Mesa del cascarón tenía k3, pero el mismo fallo de overflow en WebView la dejaba estática.

## Fix aplicado (stamp **v20261001k5**)

- `ensureShelfIconsOverflow`: `min-width` en ghosts + **padding-right forzado** si WebView sigue reportando sin overflow.
- En app nativa (`LvBridge` / `LesVencimosAndroid`): no abortar por `prefers-reduced-motion` (sigue pausando ~5s al tocar).
- CSS `.shelf-parade-ghost { flex:0 0 auto }`.
- Marker de extracción: `v20261001embed` → **`v20261001k5`** (fuerza re-extraer Completo al actualizar APK).
- Mesa cascarón: misma endurecida.

## Archivos tocados

| Ruta | Qué |
|------|-----|
| `lesvacimos/android-cascaron/app/src/main/assets/embed/completo-offline.zip` | ZIP embebido fat |
| `lesvacimos/android-cascaron/app/src/main/assets/mesa.html` | Parade baldas mesa |
| `lesvacimos/android-cascaron/.../PackExtractor.java` | EXPECTED_VERSION=k5 |
| `lesvencimos/offline-pack-completo(-embed)/estanteria.html` | Shell Completo |
| `lesvencimos/offline-estanteria/estanteria.shell.html` | Fuente canónica shell |
| `lesvencimos/android-cascaron/.../mesa.html` | Cascarón flaco (fuente) |
| `lesvencimos/android-apk/.../assets/estanteria.html` | APK prueba |
| `lesultimos/offline-estanteria/*` + `estanteria.html` | Mirror PWA |
| `downloads/completo-offline.zip` | Pack embed sideload |
| `downloads/pack-completo-offline.zip` | Pack thin sideload |

## MD5 (post-fix)

```
completo-offline.zip              61e285fa94aa31db8b7811dd05d5cc63
pack-completo-offline.zip         75e798682774c88670562322493feed3
lesvencimos-completo.apk (2.0.0)    a4d740df96f4a40224bdc5eacece26e5
estanteria (dentro completo ZIP)  68c1181f66320eb57c8cbc14266232df
estanteria pack thin staging      402c0db5556c1d2089734b7341103db9
mesa.html (lesvacimos fat)        a6801f0dcedb33351844d9ac7f2cc74e
```

## ¿App APK debe rebuild?

- **Fat Completo 2.0.0**: **YA rebuild + firmado** en esta pasada → `app/lesvencimos-completo.apk` y `downloads/lesvencimos-completo.apk` (md5 `a4d740df…`). versionName sigue **2.0.0** / versionCode **20**; el embed + marker cambian (re-extract al abrir).
- **Cascarón flaco** (`lesvencimos/android-cascaron` 1.0.6): `mesa.html` parcheada en fuente; **sí conviene rebuild** si se sigue repartiendo el APK flaco (no republicado aquí).
- **android-apk** (prueba WebView antigua): assets actualizados; rebuild opcional (no es el producto 2.0.0).

## Cómo verificar en el teléfono

1. Instalar/actualizar `lesvencimos-completo.apk` (md5 nuevo).
2. Al abrir debe re-extraer Completo (marker k5) — overlay «Instalando…».
3. Baldas Completo: iconos deben desfilar despacio; al tocar pausan ~5s.
4. Si no: borrar datos de la app y abrir de nuevo (fuerza extract limpio).
