# Packs de tono — Profesor (visión)

> Stub / diseño. **No implementar del todo aún.** Pedido Jorge 2026-09-23.

## Idea

El temario oficial (CyL) es el mismo. Cambia **cómo** se enseña:

- Un profesor (o creador) elige **tono y estilo**: más formal, más humor, más visual, más riguroso, narrativo tipo «Profesor Xavier», etc.
- Puede **adaptar o colgar sus lecciones** sobre la base del curso (ej. 1º ESO Matemáticas).
- La gente **descarga el pack** que más le guste (como elegir profesor), offline y privado.

## Modelo previsto

| Pieza | Rol |
|---|---|
| Núcleo del curso | Saberes + lecciones canónicas Les vencimos (decreto) |
| Pack de tono | Metadatos (autor, nombre del profesor, tono) + textos/estilo overlay o lecciones sustituidas |
| Catálogo web | Listar packs verificados / comunitarios por curso+asignatura |
| Estantería / Profesor | Cargar pack opcional; sin pack = tono por defecto |

## Plantilla vacía

- Módulo: `modulos/profesor-pack-plantilla.html`
- Carpeta: `profesor/packs/_plantilla/` (`pack.json` + `LEEME.txt`)

## Fuera de alcance ahora

- Subida comunitaria, moderación, premios de tono, firma de packs.
- Solo queda el hueco y este documento.
