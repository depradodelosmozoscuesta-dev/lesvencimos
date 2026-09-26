# Les vencimos — rediseño visual

## Moodboard
1. Manual técnico de campo: numeración 01–04, reglas de 1 px, silencio entre bloques.
2. Kinfolk sobrio: papel sobre tinta, un acento, cero decoración.
3. Bloomberg Businessweek: titular serif con carácter, body grotesk, densidad útil.
4. Panel de instrumentos: cifras grandes, labels en small-caps, estado en palabras.
5. Señalética de aeropuerto: tracking amplio, mayúsculas quietas, sin gritar.
6. Empaque de herramienta profesional: radio 2 px, mate, sin glow.
7. Lámpara de aceite / apagón: carbón y ámbar quemado. Nada de indigo SaaS.
8. Revista impresa: márgenes levemente asimétricos, claim al cierre, footer-colofón.
9. Cero mascota, cero blob, cero ilustración genérica, cero raster en landing. (La figura Chico/Chica del Gimnasio es silueta de ejercicio, no mascota «Mari».)
10. El paraguas de cuatro pétalos se queda. No se redibuja cute.

## Tokens
Ver `brand/tokens.css`.

- Fondo `#0E0E0C` / superficie `#161512` / panel `#1C1A16`
- Tinta `#E6E1D6` / suave `#9A9488`
- Acción única `#C4A15A` sobre texto `#1A160E`
- Peligro `#C46A4A` / ok tipográfico `#8F9A72`
- Display: Iowan Old Style / Palatino / Georgia
- Body: Segoe UI / system-ui
- Escala 1.25. Pesos 400 / 600 / 700. Cero 800.

## Qué se quitó (AI slop)
1. Puntito verde `::before` en la pill de status.
2. Gradiente navy `#0B1220 → #121A2B` y tile `lluvia` de fondo.
3. Cuatro cards clon radio-16 con sombra suave.
4. Acento indigo `#C7D2FE`.
5. `font-weight: 800` y tracking `-0.04em` que grita.
6. Glass `rgba(255,255,255,.03)` y pills badge.
7. Pulse infinito de la sirena (ahora 150 ms × 2).
8. Chips pastel como sistema visual (pasan a etiqueta tipográfica).
9. Hero vacío con aire de plantilla 2024.
10. Semáforo de estado. Offline se dice en small-caps.

## Restricciones respetadas
HTML estático. CSP original. Sin CDN. Sin Google Fonts. file:// con paths relativos. Touch ≥ 44 px. Contraste AA. Misma información. JS de Alarma Cuba intacto.
