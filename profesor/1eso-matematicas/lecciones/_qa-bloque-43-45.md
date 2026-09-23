# QA bloque L43–L45 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta primaria (interactivos):** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`  
**Sync:** mismos HTML/PNG/md copiados a `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`  
*(El usuario escribió «lescircimos» dos veces; el espejo real es **lesvencimos**.)*

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `43.md` | Lección resolver/comprobar + glosario + interactivo | ~6–7 KB |
| `44.md` | Lección tablas/gráficas + glosario + interactivo | ~6–7 KB |
| `45.md` | Lección algoritmos + glosario + socioafectivo + interactivo | ~7 KB |
| `l43-ecuaciones-resolver.html` | Interactivo offline (file://) | ~22 KB |
| `l43-ecuaciones-resolver-preview.png` | Preview Chrome · ambos lados · x=9 equilibra | ~230 KB |
| `l44-tablas-graficas.html` | Interactivo offline | ~21 KB |
| `l44-tablas-graficas-preview.png` | Preview · manzanas León y=2x+1 · tabla→gráfica | ~220 KB |
| `l45-algoritmos-pasos.html` | Interactivo offline | ~20 KB |
| `l45-algoritmos-pasos-preview.png` | Preview · máximo de 2 · a=7,b=4 · paso 3a | ~245 KB |
| `_qa-bloque-43-45.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://…?preview=1` (sin red) para L43, L44, L45.
- [x] Preview L43 inspeccionado: **Ambos lados** 3x−5=2x+4 · paso Despejar · x=9 · comprobación 9=9 ✓ · balanza de dos platos etiquetados.
- [x] Preview L44 inspeccionado: **Manzanas (€/kg)** mercadillo de León · tabla (0,1)…(4,9) · ejes en castellano · puntos alineados · destacar (2,5).
- [x] Preview L45 inspeccionado: **Máximo de 2** · tarjetas numeradas (no spaghetti) · traza a=7,b=4 → salida 7 · consejo socioafectivo suave.

### Matemáticas
- [x] L43: ax+b=c; ambos lados; paréntesis; problema verbal; pasos inversos; comprobación por sustitución.
- [x] L44: verbal ↔ tabla ↔ gráfica ↔ fórmula; y=mx+n; lectura de gráfica; contexto CyL.
- [x] L45: interpretar pasos; modificar max2→max3; bucle mientras par; depurar fallo (n−2 vs n÷2).

### Calidad Jorge (barra L01)
- [x] **Dibujos = lo que nombran:** balanza de dos platos (L43); tabla real + ejes (L44); tarjetas de pasos claras (L45) — no blobs / no spaghetti.
- [x] **Controles independientes:** L43 coeficientes/paso/x-prueba; L44 m/n/puntos/destacar; L45 a/b/c y avance de paso.
- [x] **Glosario en español primero:** x = «la cantidad desconocida»; ejes/tabla en castellano; algoritmo/entrada/salida — en HTML + md.
- [x] Mnemónicos visibles en los 3 interactivos y en los 3.md.
- [x] Historias / contexto CyL: mercadillo Valladolid/León; bici Castilla; temperatura Burgos.
- [x] Tono ~12 años; UD13 L43 · UD14 L44–L45.
- [x] Single-file HTML, `file://`, sin dependencias de red. Tema crema (#FAF7F0) alineado a `_plantilla-leccion`.
- [x] Sin inventar currículo: Decreto 39/2022 D.4, D.5, D.6 / E.
- [x] L45 socioafectivo **ligero**: «¿me miras el paso 3?» / depurar es normal — no sermón.

### Markdown
- [x] `43.md` / `44.md` / `45.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones/reto.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lescircimos` y `lesvencimos`.

---

## Límites conocidos

1. **L43 balanza:** tipado visual ±8°; no simula masas físicas reales.
2. **L43 pasos:** 3 (simple/ambos/problema) o 4 (paréntesis); asume coeficiente de x ≠ 0 al despejar.
3. **L43 problemas:** banco de 3 enunciados; «es» → =.
4. **L44:** modelos lineales escolares (no meteorología oficial ni tarifas reales).
5. **L44 puntos:** x enteros por redondeo; con nPts=4 y xMax=4 puede saltar un valor (preview usa 5 → 0..4).
6. **L44 «Leer»:** 3 preguntas de banco; no genera ítems aleatorios.
7. **L45 tarjetas:** layout 2×3 con flechas simples (no diagrama de flujo completo ISO).
8. **L45 bug:** el fallo es n←n−2 en lugar de n←n÷2; un distractor basta para 1º.
9. **L45 socioafectivo:** consejo opcional (checkbox); tono suave.
10. **Preview estática** del estado `?preview=1` (L43 x=9; L44 manzanas 2x+1; L45 max2 paso 3a).
11. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l43-ecuaciones-resolver.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l44-tablas-graficas.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l45-algoritmos-pasos.html"
```

---

## Veredicto

**OK para bloque 43–45.** Interactivos de situaciones-problema (balanza/mercadillo, tabla→gráfica CyL, algoritmos en tarjetas); glosarios con nombres en español primero; visuals alineados al concepto (barra L01); controles independientes; socioafectivo ligero en L45; previews alineados con la UI; sync en ambos árboles.
