# Huecos — falta / fino / esqueleto

Fecha: 26 sep 2026 · Europe/Madrid (UTC+2)  
Clasificación respecto al resto del catálogo y a lo que LEEME-vida / índices prometen.

---

## Top 5 huecos (prioridad)

### 1. Fontanería (módulo inexistente)
LEEME-vida lo lista «en preparación». Hogar `manten` solo cubre atascos leves / sifón / aireador.  
**Falta:** módulo vida propio (como Electricidad) con SVG y límites claros.

### 2. Gas / calefacción DIY (módulo inexistente)
Clima explica *uso sensato* y riesgos CO; Hogar dice «nunca DIY de gas».  
**Falta:** guía vida «qué puede el usuario / qué no» sin invitar a manipular gas — o dejar explícito que **no** habrá DIY gas.

### 3. Guías de viaje — esqueleto piloto
`guias-viaje.html` ~5K; solo CyL (3 ciudades), Madrid, Barcelona, Sevilla. Resto CCAA «próximamente».  
**Falta:** densidad real o acotar LEEME a «piloto» sin expectativa de cobertura nacional.

### 4. Salud — fina frente a Medicación / PA
Salud 19K: médicos/informes/historial útiles pero poco contenido educativo. Pastillas ya delegan a `lv-medicacion-v1`.  
**Falta:** o reforzar Salud como hub sanitario personal, o documentar que el cuerpo educativo está en Primeros auxilios + Medicación.

### 5. Mapas núcleo fino vs packs
`mapas.html` 22K = GPS/rumbo/ETA; densidad geográfica está en `/downloads/mapas/*.zip`.  
**Falta:** descubrir packs desde el HTML con más claridad (o hub de packs en el propio módulo).

---

## Otros huecos / finos / esqueletos

| Ítem | Estado | Nota |
|------|--------|------|
| Pintura y yeso | anunciado LEEME-vida | sin HTML |
| `profesor-pack-plantilla.html` | esqueleto 1.1K | stub; Profesor vive en downloads |
| `calculadora.html` | esqueleto útil | completa para su scope |
| `radio.html` | fino | UI offline; audio necesita internet |
| Biblioteca sin LEEME en `modulos/` | denso | LEEME solo en downloads |
| Checks medicación duales | fino técnico | `lv-med-check-*` vs `lv-salud-check-*` no unificados |
| Moda costura | «base; se ampliará» (LEEME) | parcial consciente |
| Campo / Supervivencia / Apagón / Bricolaje | finos | OK como guías cortas; no pedirle densidad Hogar |
| Legal-casa mantenimiento semanal cifras | proceso | no es hueco de módulo; es caducidad fiscal |

## Huecos de relación (no de módulo)

- Export/import unificado Hogar+Economía+Salud (Eco ya tiene JSON v3; Hogar no equivalente completo).
- Puente explícito UI Hogar Lavado → Moda símbolos (hoy solo de contenido).
- Documentar en LEEME-hogar la clave canónica `lv-lista-compra-v1`.

*Fin huecos*
