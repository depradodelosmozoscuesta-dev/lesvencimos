# Huecos y temas rotos / incompletos

Qué un usuario de «aprender para la vida» + asistente doméstico esperaría y **no está cubierto**, está **esqueleto**, o está **partido** entre módulos sin puente.

---

## Top huecos (prioridad)

### 1. Fontanería / gas / pintura (anunciados, no existen)
- `LEEME-vida.txt` lista **Fontanería**, **Gas/calefacción básica**, **Pintura y yeso** «en preparación».
- Hoy solo **Electricidad** (+ Bricolaje) cubre oficios vida.
- Clima habla de calefacción como *uso*, no instalación. Hogar Mantén. se detiene ante gas/cuadros.
- **Impacto:** agujero obvio en la estantería «vida».

### 2. Doble fuente de verdad: compra / menú / nevera
- Hogar (Súper, Nevera, Recetas) y Economía (Compra, Menú) no comparten `localStorage`.
- Usuario espera una sola lista. Hoy son dos mundos.
- **Estado:** funcional cada uno; **roto como sistema**.

### 3. Salud ↔ Medicación duplicados
- Ambos gestionan pastillas/horarios en local.
- Sin puente ni LEEME que diga «usa solo uno» o «Salud lee Medicación».
- **Riesgo:** olvidos o dosis dobles en la cabeza del usuario (no en código).

### 4. Guías de viaje casi vacías en `modulos/`
- `guias-viaje.html` ≈ 4 KB: botones a `/guias-viaje/` y ZIP.
- Offline «serio» exige el ZIP; quien solo abre el HTML del módulo ve un índice web-céntrico.
- Resto de CCAA «próximamente» (LEEME).

### 5. Calefacción / gas como oficio vs Clima
- Usuario busca «se estropea la caldera» → no hay módulo Gas; Clima + Economía dan hábitos; Legal no repara.
- Hueco entre Clima (confort) y vida práctica (avería).

---

## Otros huecos relevantes

| Hueco | Detalle |
|---|---|
| Agenda / calendario personal | No hay módulo Agenda en `modulos/`. Asistente futuro tendrá que nacer en núcleo, no en estantería actual. |
| Contactos / familia / vecinos | Apagón menciona vecinos; no hay libreta offline unificada (Caja fuerte es secretos, no agenda). |
| Inventario despensa ≠ nevera rica | Hogar Nevera es zona+lista; no hay caducidad automática cruzada con ficha Alimentos. |
| Domótica | LEEME-hogar: «Sin domótica» — hueco consciente, no bug. |
| Finanzas fiscales personales | Legal embebe impuestos **municipales Va**; no hay IRPF/autónomos (Economía lo declara fuera de alcance). |
| Seguro hogar / pólizas | No cubierto (Legal/Economía evitan productos). |
| Veterinaria de urgencia protocolizada | Mascotas tiene urgencias; no hay puente a Primero auxilios humanos (bien separado) ni a Apagón «qué hago con el perro sin luz». |
| Mapas: España sin calles | Pack país overview zoom bajo; expectativa «Google offline» no cumplida (documentado en LEEME). |
| Radio offline real | Emisoras = stream; en apagón con datos caídos el módulo no cumple la promesa emocional de «radio». |
| Biblioteca sin LEEME | 4,3 MB sin `LEEME-biblioteca.txt` en carpeta. |
| `profesor-pack-plantilla.html` | Esqueleto 1 KB en carpeta de módulos publicados — confunde si aparece en estantería. |
| Vida / fontanería tracking | LEEME-vida huérfano de HTML. |
| Cuba en Informática vs home | Materia Central Cuba visible en Informática mientras Alarma/Central están aparados del Escritorio — coherencia de producto a vigilar. |
| Multiusuario / perfiles | Ningún módulo; asistente Alzheimer/negocios viven fuera (`asistente-*.html` raíz). |
| Export unificado | Economía/Hogar/etc. exportan por su lado; no hay «exportar casa completa». |

---

## Rotos / frágiles (no son huecos temáticos)

- **Guías** enlaces absolutos `/guias-viaje/...` flojos en `file://` puro sin el pack descomprimido al lado.
- **Mapas** packs deben descargarse aparte; núcleo solo GPS.
- **Caja fuerte:** PIN olvidado = datos perdidos (documentado; frágil por diseño).
- **Aliases Android** (`medita`, `gym`, `caja`…): bien; hay que mantenerlos idénticos en builds.

---

## Fuera de alcance (no contar como hueco de este informe)

- Ruleta / patente.
- Red ciudadana / juego.
- Temario escolar Profesor (salvo frontera).
- Productos bancarios / criptos (bloqueo explícito Economía).

*Fin huecos.*
