# QA bloque L07–L09 · 1º ESO Matemáticas (CyL)

**Fecha:** 2026-09-23 (Europe/Madrid, CEST / UTC+2)  
**Ruta:** `/workspace/lescircimos/profesor/1eso-matematicas/lecciones/`  
**Árbol sync `lescircimos`:** solo existe `/workspace/lescircimos/…` (ya es el destino; no había segundo clon que copiar).

---

## Inventario (todos presentes)

| Archivo | Rol | Tamaño aprox. |
|---|---|---|
| `07.md` | Lección + enlace interactivo + glosario + criptograma | ~6.7 KB |
| `08.md` | Lección potencias/raíces + enlace | ~5.4 KB |
| `09.md` | Lección problemas contextualizados + enlace | ~5.7 KB |
| `l07-cajas-zumo.html` | Interactivo offline (file://) | ~33 KB |
| `l07-cajas-zumo-preview.png` | Preview Chrome headless | ~556 KB (alto, incluye criptograma) |
| `l08-torres-potencias.html` | Interactivo offline | ~24 KB |
| `l08-torres-potencias-preview.png` | Preview | ~299 KB |
| `l09-excursion-problemas.html` | Interactivo offline | ~27 KB |
| `l09-excursion-problemas-preview.png` | Preview | ~289 KB |
| `_qa-bloque-07-09.md` | Este checklist | — |

---

## Qué se probó

### Render / preview
- [x] `google-chrome --headless --screenshot` con `file://` (sin red) para L07, L08, L09.
- [x] Preview L07 inspeccionado: rejilla 3×4 de botellas, producto 12, cociente 12÷4=3, chips de propiedades, sección **Criptograma** visible (pistas M…L y mensaje numérico).
- [x] Preview L08 inspeccionado: torre 2³ con 3 pisos, `2×2×2=8`, chips de cuadrados 1²…10², glosas de a/n/√.
- [x] Preview L09 inspeccionado: escena autobús Burgos→museo, tickets Salían 20 / Bajan 6 / Quedan 14, **14** figuras en el bus, plan paso a paso y expresión `(4×5)−6=14`.

### Matemáticas
- [x] Criptograma L07: pistas productos → mapa único; mensaje `12 15 20 21 · 21 24 · 25 15 28 30 35` = **MATE ES FACIL** (sin tilde a propósito: entrada de 1 letra ASCII).
- [x] Inversas L07: a×b=p ⇒ p÷b=a (comprobado en UI por defecto 3×4).
- [x] Conmutativa / asociativa / distributiva: fórmulas en demo usan los a,b,c actuales.
- [x] Potencias L08: aⁿ = producto de n factores a (bucle entero, sin `**` flotante raro).
- [x] Raíz L08: solo cuadrados perfectos vía lado s; √(s²)=s.
- [x] L09 bus: (a×b)−c; shop: (a×b)×c; snack: (a×b)+c. Casos por defecto 14, 36, 21.

### Calidad Jorge (barra)
- [x] Cada símbolo de UI explicado en español (×, ÷, =, ≠, √, aⁿ, ( ), letras a/b/c/n/s).
- [x] Glosario en cada HTML + glosario en cada `.md`.
- [x] Mnemónicos presentes en las tres lecciones.
- [x] Controles independientes (filas≠columnas; base≠exponente; a/b/c del problema no se reescalan juntos).
- [x] Escenas que **se parecen** a la situación (botellas, torre/baldosas, bus/mercadillo/merienda).
- [x] **Un criptograma** en el bloque: L07 (productos). Clave explicada en la propia tarjeta morada.
- [x] Single-file HTML, `file://`, sin dependencias de red.
- [x] Música: omitida (no natural aquí).

### Markdown
- [x] `07.md` / `08.md` / `09.md` creados (no existían aún en el árbol) alineados a títulos del borrador CyL UD2 y a A.3 del Decreto 39/2022.
- [x] Enlaces relativos a los HTML + nota offline.
- [x] Sin inventar saberes fuera de operaciones con naturales / potencias de exponente natural / raíces sencillas / problemas contextualizados.

---

## Límites conocidos

1. **Rangos acotados a propósito:** L07 filas/columnas 1–8 (rejilla legible); L08 exponente 1–5 y base 1–9 (torre visible); raíz por lado 1–10 (solo perfectos).
2. **Criptograma sin tildes:** mensaje `FACIL` (no `FÁCIL`) para inputs de una letra; se explica en el juego.
3. **L09 validez:** si en el bus `c > a×b`, la UI avisa enunciado no válido en naturales (no inventa negativos).
4. **Preview es captura estática:** no sustituye jugar el HTML; el criptograma en el PNG se ve en estado vacío (esperado).
5. **Chrome headless** puede loguear errores DBus inocuos en este entorno; el PNG se escribe igual.
6. **No hay segundo árbol** `/workspace/lescircimos` distinto: el pack ya vive bajo `lescircimos/profesor/…`.
7. **Distributiva / asociativa** en L07 muestran el tercer factor c solo al activar esas demos (el control c se oculta en modo normal para no confundir).
8. **Raíces no perfectas:** fuera de alcance de L08 (currículo: raíces sencillas / cuadrados perfectos en 1º).

---

## Cómo reabrir offline

```bash
# Desde el explorador de archivos: doble clic en el .html
# O:
google-chrome "file:///workspace/lescircimos/profesor/1eso-matematicas/lecciones/l07-cajas-zumo.html"
```

---

## Veredicto

**OK para bloque 07–09.** Interactivos visibles y correctos, glosarios completos, criptograma presente y matemáticamente coherente, previews alineados con la UI.
