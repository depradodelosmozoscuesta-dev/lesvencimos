# Inventario de módulos — Les vencimos (Relaciones)

Fecha: 26 sep 2026 · Europe/Madrid (UTC+2)  
Fuente: estado ACTUAL de `/workspace/lesvencimos/modulos/` (HTML + LEEME + HOGAR-INDICE + `_aparte-cuba`).  
Método: listado de disco, `md5sum` + `cmp` byte-a-byte para aliases, lectura de todos los LEEME-*.

## Resumen

| Métrica | Valor |
|--------|------:|
| HTML en `modulos/` | 34 |
| **Módulos únicos** (hash MD5) | **29** |
| Pares alias idénticos | 5 |
| LEEME-*.txt | 28 (+ LEEME-vida meta sin HTML) |
| Hub temario extra | `HOGAR-INDICE.md` |
| Nota aparte | `_aparte-cuba.md` → `docs/aparado-cuba.md` |

**Aliases byte-a-byte (`cmp -s` = idénticos):**

| Canónico (LEEME) | Alias |
|------------------|-------|
| `biblioteca.html` | `biblio.html` |
| `caja-fuerte.html` | `caja.html` |
| `guitarra.html` | `guitar.html` |
| `gimnasio.html` | `gym.html` |
| `meditacion.html` | `medita.html` |

Aliases = OK (mismo archivo duplicado por nombre corto). No son datos duplicados.

---

## Lista de módulos únicos

Densidad: **denso** / **medio** / **fino** / **esqueleto** (tamaño + riqueza de secciones/fichas).

| # | Módulo | Tamaño | Densidad | Tema | Aliases | LEEME |
|--:|--------|-------:|----------|------|---------|-------|
| 1 | `hogar.html` | 176K | denso | Cocina + casa (hub) | — | `LEEME-hogar.txt` + `HOGAR-INDICE.md` |
| 2 | `economia.html` | 185K | denso | Presupuesto, gastos, compra, energía, patrimonio, asesor | — | `LEEME-economia.txt` |
| 3 | `clima.html` | 56K | medio | Confort térmico, humedad, moho, CO | — | `LEEME-clima.txt` |
| 4 | `salud.html` | 19K | fino | Pastillas, médicos, informes, historial | — | `LEEME-salud.txt` |
| 5 | `medicacion.html` | 11K | fino | Recordatorio medicinas + checklist hoy | — | `LEEME-medicacion.txt` |
| 6 | `moda.html` | 102K | medio | Principios, cuidado, estilos, costura, probador SVG | kit `moda-svg-kit/` | `LEEME-moda.txt` |
| 7 | `jardin.html` | 171K | denso | Plantas, huerto, diccionario ~150 | — | `LEEME-jardin.txt` |
| 8 | `mascotas.html` | 151K | denso | Tekel + razas + gatos + urgencias | — | `LEEME-mascotas.txt` |
| 9 | `gimnasio.html` | 347K | denso | Ejercicios, rutinas, Moverse | `gym.html` | `LEEME-gimnasio.txt` |
| 10 | `meditacion.html` | 178K | denso | Sentarse, camino, viaje, biblioteca | `medita.html` | `LEEME-meditacion.txt` |
| 11 | `informatica.html` | 224K | denso | 14 materias · 108 lecciones · Central Cuba | — | `LEEME-informatica.txt` |
| 12 | `biblioteca.html` | 4.2M | denso | Libros offline (+ `biblioteca-libros/`) | `biblio.html` | (no LEEME en modulos; pack en downloads) |
| 13 | `legal-casa.html` | 93K | medio | CyL / Valladolid · fiscal 2026 | — | `LEEME-legal-casa.txt` |
| 14 | `tinta-estudio.html` | 77K | medio | Dibujo / ilustración | — | `LEEME-tinta-estudio.txt` |
| 15 | `tinta-escritura.html` | 66K | medio | Editor de texto | — | `LEEME-tinta-escritura.txt` |
| 16 | `primeros-auxilios.html` | 50K | medio | RCP, enfermería básica, quizzes | — | `LEEME-primeros-auxilios.txt` |
| 17 | `guitarra.html` | 38K | fino | Teoría, afinador, acordes | `guitar.html` | `LEEME-guitarra.txt` |
| 18 | `qr.html` | 33K | fino | Generador QR offline | — | `LEEME-qr.txt` |
| 19 | `caja-fuerte.html` | 23K | fino | Caja con PIN local | `caja.html` | `LEEME-caja-fuerte.txt` |
| 20 | `mapas.html` | 22K | fino | Núcleo GPS; packs en downloads | — | `LEEME-mapas.txt` |
| 21 | `electricidad.html` | 21K | fino | Enchufes, clavijas, se va la luz | — | `LEEME-electricidad.txt` |
| 22 | `apagon.html` | 18K | fino | Preparación corte de luz | — | `LEEME-apagon.txt` |
| 23 | `supervivencia.html` | 17K | fino | Resiliencia doméstica (no militar) | — | `LEEME-supervivencia.txt` |
| 24 | `bricolaje.html` | 17K | fino | DIY básico (cuadro, taladro…) | — | `LEEME-bricolaje.txt` |
| 25 | `campo.html` | 12K | fino | Supervivencia outdoor | — | `LEEME-campo.txt` |
| 26 | `radio.html` | 8.0K | fino | Lista emisoras (audio necesita red) | — | `LEEME-radio.txt` |
| 27 | `calculadora.html` | 6.8K | esqueleto | Calculadora táctil | — | `LEEME-calculadora.txt` |
| 28 | `guias-viaje.html` | 4.9K | esqueleto | Piloto España (CCAA parcial) | — | `LEEME-guias-viaje.txt` |
| 29 | `profesor-pack-plantilla.html` | 1.1K | esqueleto | Plantilla stub pack Profesor | — | — |

### Meta / fuera de lista de módulos HTML

| Archivo | Rol |
|---------|-----|
| `LEEME-vida.txt` | Catálogo «Aprender para la vida»; anuncia Fontanería / Gas / Pintura **en preparación** (sin HTML) |
| `HOGAR-INDICE.md` | Temario contadores Hogar (recetas 109, alimentos 447, lavado 20…) |
| `_aparte-cuba.md` | Alarma/Central Cuba fuera del Escritorio; ver `docs/aparado-cuba.md` |

---

## Tabs / secciones clave (evidencia HTML actual)

### Hogar (`hogar.html`)
Tabs: `hub`, `recetas`, `nevera`, `super`, `fichas` (Alimentos), `casa`, `lavado`, `manten`, `listas`, `reloj`, `tips`.  
Sub-Casa: `zonas`, `materiales`, `manchas`, `olores`, `orden`.

**localStorage (KEYS reales):**
- `lv-lista-compra-v1` ← canónica lista compra (KEYS.compra)
- `lv-hogar-nevera-v1`, `lv-hogar-listas-v1`, `lv-hogar-reloj-v1`
- Legado leído en migración: `lv-hogar-compra-v1`, `lv-economia-lista-v1`
- Flag: `lv-lista-compra-migrated-v1`

> LEEME-hogar aún cita `lv-hogar-compra-v1` como clave viva — **desfasado** respecto al HTML (ver limpieza).

### Economía
Tabs: `hub`, `millon`, `patrimonio`, `asesor`, `presupuesto`, `gastos`, `ahorro`, `compra`, `menu`, `luz`, `habitos`, `prioridades`.

**KEYS:**
- `lv-economia-presupuesto-v1`, `…-gastos-v1`, `…-ahorro-v1`, `…-compra-tips-v1`
- `lv-lista-compra-v1` (KEYS.lista — **compartida con Hogar**)
- `lv-economia-suministros-v1`, `…-energia-habits-v1`, `…-habitos-v1`, `…-prioridades-v1`
- `lv-economia-millon-v1`, `…-patrimonio-v1`, `…-asesor-v1`
- Misma migración/flag que Hogar

### Clima
Lecciones id: `bases`, `frio`, `calor`, `calefaccion`, `frio-ac`, `ventilacion`, `corrientes`, `humedad`, `moho`, `aislamiento`, `riesgos`, `acustica`, `temporadas`, `viviendas`.  
Sin localStorage propio.

### Salud
Tabs: `hub`, `pastillas`, `medicos`, `informes`, `historial`, `consejos`.  
Pastillas → `lv-medicacion-v1` (canónica). Legacy `lv-salud-meds-v1` + flag `lv-salud-meds-migrated-v1`.  
También: `lv-salud-docs-v1`, `lv-salud-reports-v1`, `lv-salud-hist-v1`, checks `lv-salud-check-YYYY-MM-DD`.  
Medicación suelta: `lv-medicacion-v1`, `lv-med-check-…`, `lv-med-simple`.

### Moda
Temas (entre otros): `cuidado` → `simbolos`, `lavar`, `manchas`, `plancha-guardar`; más estilos/combinar/costura/probador. Sin LS persistente de inventario.

---

## Packs downloads (solo densidad)

Usados como contexto, no inventariados como módulos: `hogar-offline.zip`, `economia-offline.zip`, `clima-offline.zip`, `moda-offline.zip`, `salud-offline.zip`, `medicacion-offline.zip`, `mapas/` (valladolid/españa), etc.

*Fin inventario · Les vencimos · offline*
