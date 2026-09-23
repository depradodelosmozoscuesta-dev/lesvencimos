# QA L01 · Método científico · 1º ESO ByG (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta principal:** `/workspace/lesvencimos/profesor/1eso-biologia-geologia/lecciones/`  
**Espejo md5:** `/workspace/lescircimos/profesor/1eso-biologia-geologia/lecciones/`

---

## Inventario

| Archivo | Rol |
|---|---|
| `01.md` | Lección completa (objetivos, explicación, vida real CyL, ejemplos, práctica, soluciones, errores, glosario, mnemónico, reto) |
| `l01-metodo-cientifico.html` | Interactivo offline file:// (escena cubito + 6 pasos + sliders + mini-check) |
| `l01-metodo-cientifico-preview.png` | Captura Chrome headless `?preview=1` |
| `_qa-l01.md` | Este checklist |

---

## Decreto 39/2022 (alcance L01)

- [x] Solo viñeta A: **«Método científico. Aplicación en experimentos sencillos.»**
- [x] No se vuelcan fuentes/laboratorio/científicas/os (L02–L05).
- [x] TEMARIO ya listaba L01 con ese título; sin cambio de alcance.

---

## Interactivo

- [x] Tema crema `#FAF7F0` (plantilla Mate).
- [x] Escena realista SVG: vaso, cubito, agua que sube, termómetro, reloj, ventana/sol, Lucía.
- [x] Pasos en español: Observar → Preguntar → Hipotetizar → Experimentar → Datos → Concluir.
- [x] Transiciones de narración; pills; Anterior/Siguiente; Auto-avance/Pausa; Reiniciar.
- [x] Sliders independientes: temperatura (variable) y tiempo.
- [x] Modelo toy de fusión: a más °C y más minutos, menos hielo.
- [x] Mini-check: ordenar pasos (mnemónico) + hipótesis buena vs mala.
- [x] Glosario en HTML; sin CDN; `file://` OK.
- [x] `?preview=1` → paso Experimentar, T=26 °C, t=14 min, mid-melt.

---

## Markdown

- [x] Header curso / UD A / Decreto 39/2022 A (método).
- [x] Mnemónico «Oso Pequeño Hace Experimentos De Ciencia».
- [x] Términos en español primero (hipótesis, variable, control, datos…).
- [x] Enlace relativo al HTML + nota offline.
- [x] Soluciones con porqués; errores frecuentes; mini cierre; Reto Profesor.

---

## Preview

- [x] `google-chrome --headless --screenshot` con `file://…html?preview=1`.
- [x] PNG inspeccionado: vaso + hielo parcial + banner «4 · Experimentar», T=26 °C, t=14 min, pastilla 4 activa, tema crema.

---

## Límites conocidos

- Modelo de fusión es didáctico (no física cuantitativa exacta).
- Auto-avance también empuja el tiempo; el alumno puede pausar y usar sliders a mano.
