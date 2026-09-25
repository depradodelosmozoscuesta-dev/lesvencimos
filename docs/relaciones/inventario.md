# Inventario de módulos publicados

**Ámbito:** `/workspace/lesvencimos/modulos/` (Escritorio / estantería offline).  
**Fecha del inventario:** 25 sep 2026 (Europe/Madrid).  
**Fuera de alcance:** Ruleta / patente; red ciudadana / juego (solo se menciona como frontera). Cuba queda en línea aparte (`_aparte-cuba.md` / `docs/aparado-cuba.md`).

**Conteo:** 34 HTML en `modulos/` → **29 módulos únicos** + **5 aliases idénticos** (byte-a-byte).  
Aliases: `gym.html`=`gimnasio.html`, `caja.html`=`caja-fuerte.html`, `guitar.html`=`guitarra.html`, `medita.html`=`meditacion.html`, `biblio.html`=`biblioteca.html`.

**Docs anexos en la carpeta:** `HOGAR-INDICE.md`, `_aparte-cuba.md`, 28 `LEEME-*.txt` (incluido `LEEME-vida.txt` sin HTML gemelo aún).

**Núcleo asistente:** la mayoría de LEEME solo indican `file://` / Archivos. Menciones explícitas al hub: Calculadora («se puede enlazar luego desde el asistente»), Gimnasio («como el Asistente»), QR (catálogo compartido con Estantería), Informática (antes pack Profesor, ahora módulo aparte). Arquitectura Jorge: web = escaparate; asistente offline = corazón; módulos pesados descargables; «Añadir módulo»; privacidad en dispositivo.

---

## Tabla rápida

| Módulo (canónico) | Archivo | Tamaño ≈ | LEEME | Estado | Aliases |
|---|---|---:|---|---|---|
| Apagón | `apagon.html` | 17 KB | `LEEME-apagon.txt` | Contenido útil (5 lecciones) | — |
| Biblioteca | `biblioteca.html` | 4,3 MB | — | Contenido rico (catálogo + JSON en `biblioteca-libros/`) | `biblio.html` |
| Bricolaje | `bricolaje.html` | 17 KB | `LEEME-bricolaje.txt` | Contenido (5 guías) | — |
| Caja fuerte | `caja-fuerte.html` | 23 KB | `LEEME-caja-fuerte.txt` | Contenido (PIN + entradas) | `caja.html` |
| Calculadora | `calculadora.html` | 7 KB | `LEEME-calculadora.txt` | Contenido ligero | — |
| Campo | `campo.html` | 11 KB | `LEEME-campo.txt` | Contenido (6 lecciones outdoor) | — |
| Clima hogar | `clima.html` | 57 KB | `LEEME-clima.txt` | Contenido rico (14 lecciones) | — |
| Economía | `economia.html` | 187 KB | `LEEME-economia.txt` | Contenido muy rico + localStorage | — |
| Electricidad | `electricidad.html` | 21 KB | `LEEME-electricidad.txt` | Contenido (5 guías SVG) | — |
| Gimnasio | `gimnasio.html` | 52 KB | `LEEME-gimnasio.txt` | Contenido rico (hubs niveles) | `gym.html` |
| Guías de viaje | `guias-viaje.html` | 4 KB | `LEEME-guias-viaje.txt` | **Esqueleto / lanzadera** al pack `/guias-viaje/` + ZIP | — |
| Guitarra | `guitarra.html` | 38 KB | `LEEME-guitarra.txt` | Contenido rico | `guitar.html` |
| Hogar | `hogar.html` | 179 KB | `LEEME-hogar.txt` + `HOGAR-INDICE.md` | Contenido muy rico | — |
| Informática | `informatica.html` | 228 KB | `LEEME-informatica.txt` | Contenido muy rico (14 materias / quizzes) | — |
| Jardín | `jardin.html` | 158 KB | `LEEME-jardin.txt` | Contenido muy rico + diccionario ~150 | — |
| Legal casa | `legal-casa.html` | 95 KB | `LEEME-legal-casa.txt` | Contenido rico (A–F + fiscal Va 2026) | — |
| Mapas | `mapas.html` | 22 KB | `LEEME-mapas.txt` | Núcleo GPS + punta a packs ZIP | — |
| Mascotas | `mascotas.html` | 154 KB | `LEEME-mascotas.txt` | Contenido rico | — |
| Medicación | `medicacion.html` | 10 KB | `LEEME-medicacion.txt` | Contenido útil (recordatorios) | — |
| Meditación | `meditacion.html` | 20 KB | `LEEME-meditacion.txt` | Contenido (estaciones + diario) | `medita.html` |
| Moda | `moda.html` | 104 KB | `LEEME-moda.txt` + `moda-svg-kit/` | Contenido rico | — |
| Primeros auxilios | `primeros-auxilios.html` | 51 KB | `LEEME-primeros-auxilios.txt` | Contenido rico + quizzes | — |
| Pack tono (plantilla) | `profesor-pack-plantilla.html` | 1 KB | — | **Esqueleto** frontera Profesor | — |
| QR | `qr.html` | 33 KB | `LEEME-qr.txt` | Contenido (generador offline) | — |
| Radio | `radio.html` | 8 KB | `LEEME-radio.txt` | UI offline; **audio necesita red** | — |
| Salud | `salud.html` | 19 KB | `LEEME-salud.txt` | Contenido (pastillas/médicos/informes) | — |
| Resiliencia | `supervivencia.html` | 17 KB | `LEEME-supervivencia.txt` | Contenido (5 lecciones domésticas) | — |
| Tinta escritura | `tinta-escritura.html` | 67 KB | `LEEME-tinta-escritura.txt` | Contenido (editor) | — |
| Tinta estudio | `tinta-estudio.html` | 78 KB | `LEEME-tinta-estudio.txt` | Contenido (dibujo) | — |

**Sin HTML aún:** `LEEME-vida.txt` («Aprender para la vida») — Electricidad ya existe; anuncia Fontanería, Gas/calefacción, Pintura/yeso *en preparación*.

---

## Fichas por módulo

### Hogar — `hogar.html` (179 KB)
- **Title/H1:** Hogar — Les vencimos / Hogar.
- **LEEME:** descriptivo + claves `lv-hogar-compra-v1`, `lv-hogar-nevera-v1`, `lv-hogar-listas-v1`, `lv-hogar-reloj-v1`. Temario en `HOGAR-INDICE.md`.
- **Secciones (tabs):** Inicio, Recetas (109), Nevera (4 zonas), Súper, Alimentos (447 fichas), Casa → Limpieza zonas/materiales, Manchas, Olores, Orden, Lavado (20), Mantén. (14), Listas (4), Reloj, Consejos (36).
- **Estado:** contenido rico. Sin domótica. Límites: no gas ni electricidad interna → profesional / 112.
- **Asistente:** candidato natural a modo Hogar (listas, nevera, reloj).

### Economía — `economia.html` (187 KB)
- **Title/H1:** Economía.
- **LEEME:** muy descriptivo; localStorage v3 (presupuesto, gastos, ahorro, compra, menú, suministros, hábitos, prioridades, millón, patrimonio, asesor).
- **Secciones:** Hub, Primer millón, Patrimonio, Asesor, Presupuesto, Gastos, Ahorro, Compra (≥35 tips + comparador), Menú 2 semanas, Luz y agua (≥25 tips + calc), Hábitos, Prioridades.
- **Estado:** contenido muy rico. Educativo; no asesor colegiado.
- **Cruce:** compra/menú/nevera → Hogar; luz/agua/termostato → Clima; vivienda/derramas → Legal-casa; categoría mascotas/ropa → Mascotas/Moda.

### Clima hogar — `clima.html` (57 KB)
- **Title/H1:** Clima hogar.
- **LEEME:** confort térmico, calefacción/refrigeración, ventilación, humedad, aislamiento, riesgos CO/moho.
- **Lecciones:** Bases confort; Frío; Calor; Calefacción; Refrigeración; Ventilación; Corrientes; Humedad; Moho; Aislamiento casero; Riesgos CO; Confort acústico; Checklist temporada; Casos España.
- **Estado:** rico. No sustituye técnico.
- **Cruce:** tips energía Economía; humedad/moho Hogar limpieza; frío/calor Supervivencia/Apagón.

### Jardín — `jardin.html` (158 KB)
- **LEEME:** muy descriptivo (casa/balcón/huerto ES + diccionario ~150 + toxicidad mascotas/niños).
- **Lecciones:** Empezar; Luz; Riego; Sustratos; Macetas; Plagas leves; Poda; Temporada ES; Balcón; Huerto mínimo; Huerto serio; Interior; Bonsáis; Supervivencia/catástrofes; Problemas frecuentes.
- **Cruce:** Campo (recolectar/qué no comer); Mascotas (toxicidad); Clima (humedad interior); Economía (riego/terraza en tips energía).

### Legal casa — `legal-casa.html` (95 KB)
- **LEEME:** España / CyL / Valladolid capital; fiscal 2026 embebido (Guía contribuyente, OOFF, residuos, Aquavall, ITP/AJD). Mantenimiento semanal del bloque fiscal.
- **Bloques:** A Comunidades; B Convivencia; C Alquiler; D Reclamaciones; E Impuestos/tasas Va; F Puntos de vista; glosarios.
- **Lecciones clave:** PH, cuotas/derramas, ruidos, animales comunidad, humedades, arrendamiento, facturas/servicios, IVTM/novedades fiscales (vía E).
- **Cruce:** Economía (vivienda, comunidad, derramas); Hogar (humedades/mantenimiento ligero); Mascotas (animales en comunidad).

### Moda — `moda.html` (104 KB)
- **Secciones:** Principios; Cuidado (etiquetas, lavar, manchas, plancha); Estilos; Combinar + SVG; Ocasiones; Costura básica; Curiosidades. Kit `moda-svg-kit/`.
- **Cruce fuerte:** Hogar → Lavado / Manchas / Plancha. Economía → presupuesto ropa / comprar menos.

### Informática — `informatica.html` (228 KB)
- **LEEME:** 14 materias · 108 lecciones · 324 preguntas; Linux, ciberseguridad, Python, C++, algoritmos, LPI, **Central Cuba**.
- **Estado:** muy rico. Cultura general; *no* temario escolar Profesor (frontera).
- **Cuba:** materia «Central de la casa (Cuba)» — respetar línea aparte del Escritorio/home (ver `_aparte-cuba.md`).
- **Cruce herramientas:** Caja fuerte, QR, Radio (herramientas digitales offline).

### Mascotas — `mascotas.html` (154 KB)
- **Secciones:** Salchicha/Tekel; Razas perro; Gatos; Peso; Urgencias; Veterinario ES; Biblioteca práctica.
- **Cruce:** Jardín (plantas tóxicas); Legal (animales comunidad); Economía (partida mascotas); Primeros auxilios (urgencias humanas ≠ vet).

### Apagón — `apagon.html` (17 KB)
- Lecciones: Se fue la luz ahora; Nevera/comida; Luz y pilas; Personas/vecinos; Preparar el próximo. Enlace ligero a Electricidad «se va la luz». Cruce: Radio, Medicación, Supervivencia, Hogar nevera.

### Campo — `campo.html` (11 KB)
- Prioridades; Agua; Comida; Recolectar; Fuego; Orientación. Distinto de Resiliencia (casa). Cruce: Jardín supervivencia; Mapas; Primeros auxilios; Supervivencia.

### Resiliencia (`supervivencia.html`) — 17 KB
- Agua casa; Botiquín; Comunicación; Frío/calor; Mochila casa. Solo civil/hogar. Cruce: Apagón, Clima, Primeros auxilios, Campo (frontera indoor/outdoor).

### Electricidad — 21 KB · Bricolaje — 17 KB
- Electricidad: enchufe, clavija, antena, se va la luz (SVG). Bricolaje: cuadro, taladro, silicona, manilla, estante. LEEME-vida anuncia más oficios vida.

### Salud / Medicación / Primeros auxilios / Gimnasio / Meditación
- **Salud** (19 KB): Pastillas, Médicos, Informes, Historial, Consejos — solapa recordatorios con Medicación.
- **Medicación** (10 KB): Hoy / Mis medicinas / Añadir — localStorage; modo letras grandes.
- **Primeros auxilios** (51 KB): RCP, PAS, heridas, medicamentos, DESA, quizzes — frontera con Salud/Medicación (educativo ≠ historial personal).
- **Gimnasio** (52 KB, alias gym): Básico/Medio/Difícil/Mayores/Abdomen; chico/chica; voz/pitido. «Como el Asistente» (sin Mari/avatar).
- **Meditación** (20 KB, alias medita): árbol nombres, estaciones, diario. No terapia.

### Mapas / Guías de viaje
- **Mapas** (22 KB): GPS, rumbo, km, ETA; packs `valladolid-offline.zip`, `espana-offline.zip`.
- **Guías viaje** (4 KB): lanzadera piloto ES (Va, Salamanca, León, Madrid, Barcelona, Sevilla) → contenido real en `/guias-viaje/` + ZIP. **Hueco de densidad** en el HTML de módulos/.

### Herramientas: Calculadora, Caja fuerte, QR, Radio
- Calculadora: aritmética grande.
- Caja fuerte: PIN maestro; tipos Wi‑Fi, DNI, login, nota — irrecuperable si se olvida PIN.
- QR: texto/Wi‑Fi/URL/nombre módulo catálogo Estantería; print.
- Radio: lista emisoras; UI offline, stream online.

### Cultura / estudio: Biblioteca, Guitarra, Tinta×2, Informática, Profesor-plantilla
- Biblioteca 4,3 MB (alias biblio) + `biblioteca-libros/*.json`.
- Guitarra: teoría, afinador, acordes/escalas (sin tablaturas de canciones).
- Tinta escritura / estudio: editor texto y estudio dibujo.
- `profesor-pack-plantilla.html` (1 KB): plantilla tono — **frontera** con `profesor.html` / pack Profesor en raíz (no inventariar el pack completo aquí).
- Tinta escritura/estudio ↔ Profesor: solo nota de frontera (estudio personal vs temario cole).

### Cuba (línea aparte)
- `_aparte-cuba.md`: Alarma Cuba → `/alarma-cuba.html`; Central Cuba → `/downloads/central-cuba.zip`. Fuera del listado Escritorio/home (2026-09-24). Informática sigue mencionando Central Cuba como materia. No mezclar en el escaparate del Escritorio.

### LEEME-vida (sin módulo HTML)
- Catálogo «aprender para la vida»: Electricidad disponible; Fontanería, Gas/calefacción, Pintura/yeso en preparación. Profesor = cole; estos = vida.

---

## Relación con núcleo (asistente / estantería)

| Señal | Módulos |
|---|---|
| «Como el Asistente» / enlazable | Gimnasio, Calculadora |
| Catálogo Estantería / QR de módulos | QR |
| Antes Profesor → módulo aparte | Informática, Primeros auxilios, Guías (cultura ≠ cole) |
| Datos locales listos para modos asistente | Hogar, Economía, Salud, Medicación, Clima (hábitos), Meditación |
| Packs externos (ZIP) | Mapas, Guías viaje, Hogar offline zip, Informática zip |

*Fin inventario.*
