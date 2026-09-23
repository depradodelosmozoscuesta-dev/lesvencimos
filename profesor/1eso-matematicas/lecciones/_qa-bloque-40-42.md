# QA bloque L40–L42 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta primaria (interactivos):** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`  
**Sync:** mismos HTML/PNG/md copiados a `/workspace/lesvencimos/profesor/1eso-matematicas/lecciones/`  
*(El usuario escribió «lescircimos» dos veces; el espejo real es **lesvencimos**.)*

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `40.md` | Lección lenguaje algebraico + glosario + interactivo | ~6.4 KB |
| `41.md` | Lección variable/fórmulas + glosario + interactivo | ~6.1 KB |
| `42.md` | Lección equivalencia/ecuaciones + glosario + interactivo | ~6.5 KB |
| `l40-lenguaje-algebraico.html` | Interactivo offline (file://) | ~27 KB |
| `l40-lenguaje-algebraico-preview.png` | Preview Chrome · emparejar «5 menos que el triple» → 3x−5 | ~195 KB |
| `l41-variable-formulas.html` | Interactivo offline | ~25 KB |
| `l41-variable-formulas-preview.png` | Preview · P=2(L+A) patio L=8 A=5 → P=26 | ~177 KB |
| `l42-equivalencia-ecuaciones.html` | Interactivo offline | ~27 KB |
| `l42-equivalencia-ecuaciones-preview.png` | Preview · balanza 2x+3=11 · x=4 equilibra | ~198 KB |
| `_qa-bloque-40-42.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://…?preview=1` (sin red) para L40, L41, L42.
- [x] Preview L40 inspeccionado: **Emparejar** «5 menos que el triple» → **3x−5** (verde ✓); Lucía + bocadillo; flecha; x = el número.
- [x] Preview L41 inspeccionado: **Perímetro P=2(L+A)** patio L=8 · A=5 → P=26 m; pasos 2(8+5)=26; rol Variables.
- [x] Preview L42 inspeccionado: **Balanza** 2x+3 = 11; x=4 equilibra ✓; paso 1/3; platos con expresiones.

### Matemáticas
- [x] L40: frases → expresiones; 2x vs 2(x+3); evaluar 3x−5; tarifa p=F+c·k.
- [x] L41: variable vs incógnita; P=2(L+A); d=v·t; despeje A=P/2−L.
- [x] L42: términos semejantes; distributiva; ecuaciones equivalentes (misma op. en ambos miembros); montar enunciado→ecuación.

### Calidad Jorge (barra L01)
- [x] **Dibujos = lo que nombran:** bocadillos/tarjetas (L40); patio etiquetado L/A (L41); balanza de dos platos (L42) — no blobs.
- [x] **Controles independientes:** L40 frase/x/F·c·k; L41 L/A o v/t o P/L; L42 a/b/c/xGuess.
- [x] **Glosario en español primero:** x = «la cantidad desconocida»; P/L/A; variable vs incógnita; términos semejantes — en HTML + md.
- [x] Mnemónicos visibles en los 3 interactivos y en los 3.md.
- [x] Historias / contexto CyL: Lucía en Valladolid (cromos); patio del cole; taxi CyL; balanza de cocina.
- [x] Tono ~12 años; UD13 L40–L42.
- [x] Single-file HTML, `file://`, sin dependencias de red. Tema crema (#FAF7F0) alineado a `_plantilla-leccion`.
- [x] Sin inventar currículo: UD13 · Decreto 39/2022 D.2, D.3, D.4.

### Markdown
- [x] `40.md` / `41.md` / `42.md` parchados con interactivo + glosario + mnemónico, conservando objetivos/práctica/soluciones/reto.
- [x] Enlaces relativos a HTML + PNG.
- [x] Sync a `lescircimos` y `lesvencimos`.

---

## Límites conocidos

1. **L40 emparejar:** 10 frases fijas; distractores aleatorios entre el banco.
2. **L40 ambigüedad:** dos versiones de frase (con/sin paréntesis); el alumno elige la expresión.
3. **L40 tarifa:** modelo lineal escolar F+c·k (no tarifas oficiales de taxi).
4. **L41 patio:** croquis proporcional; no plano a escala real del centro.
5. **L41 despeje:** A=P/2−L; si A≤0 avisa (sube P o baja L).
6. **L41 viaje:** d=v·t con unidades km/h × h = km (MRU escolar).
7. **L42 balanza:** 3 pasos (original → restar b → dividir entre a); asume a≠0.
8. **L42 semejantes:** solo una letra x + números (1º ESO).
9. **L42 montar:** 4 enunciados de banco; «es» → =.
10. **Preview estática** del estado `?preview=1` (L40 match #6; L41 patio 8×5; L42 2x+3=11).
11. **Chrome headless** puede loguear errores DBus inocuos; el PNG se escribe igual.

---

## Cómo reabrir offline

```bash
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l40-lenguaje-algebraico.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l41-variable-formulas.html"
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l42-equivalencia-ecuaciones.html"
```

---

## Veredicto

**OK para bloque 40–42.** Interactivos de situaciones-problema (traducción, patio/viaje, balanza); glosarios con nombres en español primero; visuals alineados al concepto (barra L01); controles independientes; previews alineados con la UI; sync en ambos árboles.
