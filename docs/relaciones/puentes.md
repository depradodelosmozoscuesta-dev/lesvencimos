# Puentes útiles (conceptuales + UX «Añadir módulo»)

Principio: **núcleo ligero**; módulos opcionales; datos en el dispositivo; deep-links / etiquetas comunes sin fusionar HTML.

---

## Etiquetas comunes propuestas (catálogo)

Usar en QR, Estantería y «Añadir módulo» el mismo `id` estable:

`hogar` · `economia` · `clima` · `jardin` · `legal-casa` · `moda` · `mascotas` · `salud` · `medicacion` · `primeros-auxilios` · `gimnasio` · `meditacion` · `apagon` · `supervivencia` · `campo` · `electricidad` · `bricolaje` · `mapas` · `guias-viaje` · `informatica` · `caja-fuerte` · `qr` · `radio` · `calculadora` · `biblioteca` · `guitarra` · `tinta-escritura` · `tinta-estudio`

Aliases solo de archivo (`gym`→`gimnasio`, etc.), un id canónico.

---

## Puentes prioritarios (3 para ejecutar primero)

### P1 — Lista de la compra unificada (Hogar ↔ Economía)
- **Dato compartido:** `lv-lista-compra-v1` (o puente: Economía importa `lv-hogar-compra-v1` y viceversa).
- **UX:** en Economía Menú «Enviar a lista» y en Hogar Súper badge «también en Economía».
- **Asistente:** modo Hogar «qué falta» lee una sola clave.
- **Deep-link:** `economia.html#compra` ↔ `hogar.html` tab `super`.

### P2 — Recordatorio de medicación único (Medicación → Salud)
- **Frontera:** Medicación = fuente de verdad de dosis/horarios; Salud tab Pastillas = vista o enlace («Abrir Medicación»).
- **Dato:** solo `localStorage` de Medicación; Salud no duplica altas.
- **Asistente modo Salud:** dispara checklist Hoy desde Medicación; emergencias 112 + deep-link Auxilios.

### P3 — Confort y euro (Clima ↔ Economía Luz/agua)
- **Dato:** hábitos booleanos compartidos (`lv-energia-habits-v1` ya en Economía) + checklist temporada Clima.
- **UX:** desde tip Economía «Bajar 1 °C» → `clima.html` lección calefacción; desde Clima checklist → «ver impacto en Economía».
- **Asistente:** en ola de calor/frío, sugerir card Clima + card Luz/agua sin mezclar con juego/red.

---

## Otros puentes concretos

| Puente | Mecánica sugerida |
|---|---|
| Apagón → Electricidad / Radio / Medicación | Botones al pie Apagón: `electricidad` (se va la luz), `radio`, `medicacion`, `supervivencia` |
| Supervivencia ↔ Apagón ↔ Campo | Hub «Resiliencia» en asistente con 3 chips (casa / corte luz / outdoor); no unificar HTML |
| Jardín toxicidad → Mascotas | En ficha planta tóxica: «Ver Mascotas · urgencias»; en Mascotas consejo: «Diccionario Jardín» |
| Legal animales ↔ Mascotas | Lección Legal «Animales en la comunidad» → deep-link `mascotas` |
| Legal derramas / IBI ↔ Economía patrimonio/vivienda | Card «Anotar derrama en gastos» (categoría vivienda) |
| Moda cuidado ↔ Hogar Lavado | Misma etiqueta `lavado`; desde Moda manchas → `hogar` manchas |
| Mapas ↔ Guías | Si pack Va instalado y guía Va existe: CTA cruzada «Guía Valladolid» / «Mapa offline Va» |
| QR → cualquier módulo | Ya lista nombres catálogo; mantener sincronizado con ids de arriba |
| Caja fuerte ↔ Informática | Tras lección contraseñas/SSH: «guarda el secreto en Caja fuerte» (link) |
| Hogar Mantén. ↔ Bricolaje / Electricidad | Si tarea > límite usuario → card oficio vida |
| Gimnasio ↔ Salud | No compartir datos médicos; sí CTA «calentamiento / mayores» desde consejos Salud |
| Meditación ↔ Salud | CTA suave desde consejo respiración; sin historial clínico |
| Biblioteca ↔ Tinta escritura | «Citar / nota» futura; hoy solo frontera cultural |
| Guías ↔ Profesor | Ya separado en LEEME; Estantería: estante Cultura ≠ Cole |

---

## UX núcleo «Añadir módulo»

1. Estantería muestra módulos **no instalados** con tamaño ZIP y LEEME corto.
2. Instalados → aparecen en Escritorio + resolubles por `id` (QR / asistente).
3. Paquetes pesados (Biblioteca, Informática, Mapas packs, Guías ZIP) = descarga aparte; núcleo no los embebe.
4. Cuba / Alarma / Central: **no** en Añadir módulo del Escritorio (aparte); Informática puede seguir teniendo la materia sin listar Alarma en home.
5. Ruleta / red / juego: fuera del catálogo de este informe.

## Deep-links recomendados (fragment o query)

Patrón: `modulo.html#seccion` o `?tab=`.

Ejemplos: `hogar.html#super` · `economia.html#menu` · `economia.html#luz` · `clima.html#calefaccion` · `medicacion.html` · `apagon.html` · `legal-casa.html` (bloque E fiscal) · `jardin.html` diccionario · `mapas.html` packs.

*Fin puentes.*
