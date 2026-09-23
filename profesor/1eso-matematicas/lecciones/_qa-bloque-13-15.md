# QA bloque L13–L15 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta primaria (interactivos):** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`  
**Sync:** mismos HTML/PNG/md copiados a `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`  
*(Ambos árboles existen; no hay `les0imos` en el workspace actual.)*

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `13.md` | Lección + enlace + glosario (currículo CyL UD4) | ~6.4 KB |
| `14.md` | Lección operaciones + enlace | ~5.8 KB |
| `15.md` | Lección contextos + [E] socioafectivo + enlace | ~6.8 KB |
| `l13-enteros-recta.html` | Interactivo offline (file://) | ~25 KB |
| `l13-enteros-recta-preview.png` | Preview Chrome headless | ~260 KB |
| `l14-enteros-operaciones.html` | Interactivo offline | ~21 KB |
| `l14-enteros-operaciones-preview.png` | Preview | ~238 KB |
| `l15-enteros-contextos.html` | Interactivo offline + [E] | ~23 KB |
| `l15-enteros-contextos-preview.png` | Preview | ~374 KB |
| `_qa-bloque-13-15.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://` (sin red) para L13, L14, L15.
- [x] Preview L13 inspeccionado: recta −12…12, a=−5 / b=3, opuesto −a=5, |a|=5, orden −5<3, glosario − + |a| < > visible; chips de vista Recta/Termómetro/Ascensor/Fichas.
- [x] Preview L14 inspeccionado: (−3)+5=2, arco naranja de −3→2, inversa 2−5=−3, glosario de operaciones.
- [x] Preview L15 inspeccionado: historia deuda s₀=15, d₁=−8, d₂=+10, d₃=−20 → final −3 € «debes»; bloque socioafectivo [E] con feedback ❌/✅.

### Matemáticas
- [x] Opuesto: −(−5)=5; |−5|=5; orden −10 < −3 (regla de recta).
- [x] Suma: −3+5=2; −3+(−8)=−11. Resta: 7−(−5)=12; a−b=a+(−b).
- [x] Producto: (−4)×(−3)=12; (−4)×3=−12. División: −15÷3=−5; ÷0 bloqueado en UI.
- [x] Contexto L15: 15−8+10−20=−3 (ejemplo de la lección). Ascensor −2+6=4 (preset elev).

### Calidad Jorge (barra)
- [x] Cada símbolo de UI glosado en español (−, +, | |, <, >, ×, ÷, =, s₀, d₁…).
- [x] Glosario en cada HTML + sección «Letras y símbolos» + mnemónico en cada `.md`.
- [x] Mnemónicos: L13 frío/garaje; L14 resta=suma del opuesto / amigos-enemigos; L15 primero el 0.
- [x] Controles independientes (a↔b, s₀↔dᵢ) — sin asignación cruzada de valores.
- [x] Escenas que **se parecen** al concepto: recta+termómetro+ascensor+fichas; saltos/arcos; wallet/termómetro/cabina + timeline de historia.
- [x] Criptograma/juego de letras: **omitido a propósito** (no forzar en este bloque).
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Sin inventar currículo: títulos y saberes alineados a hub CyL UD4 / Decreto 39/2022 A.2–A.3 + E.
- [x] L15 incluye momento socioafectivo [E] explícito.

### Markdown
- [x] `13.md` / `14.md` / `15.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones del pack.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lescircimos` y `lesvencimos`.

---

## Límites conocidos

1. **Rangos acotados a propósito:** L13 a,b=−12…12 (recta legible); L14 a,b=−9…9 y recta de salto −18…18; L15 s₀=−20…40, di=−20…20.
2. **División L14:** si el cociente no es entero, la UI lo avisa (prioridad pedagógica a cocientes enteros en 1º ESO).
3. **Termómetro/ascensor L13:** la vista termómetro/ascensor muestra sobre todo **a** (b sigue en resultados y en recta/fichas).
4. **Calendario a.C./d.C.** del md L15 no está modelado en el HTML (sutileza del año 0); los tres contextos del interactivo son deuda/temp/ascensor.
5. **Preview es captura estática** del estado inicial (L13 recta; L14 suma; L15 deuda).
6. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l13-enteros-recta.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l14-enteros-operaciones.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l15-enteros-contextos.html"
```

---

## Veredicto

**OK para bloque 13–15.** Interactivos visibles y correctos, glosarios completos, visuals alineados al concepto (recta-termómetro-ascensor / saltos-inversas / historias+[E]), previews alineados con la UI, sync en ambos árboles. Sin criptograma (a propósito).
