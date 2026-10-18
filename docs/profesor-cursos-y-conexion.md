# Profesor por cursos + Conexión a internet en el Asistente (rama profesor-cursos, 18-10-2026)

## 1. Asistente (asistente.html): «Conexión a internet»
- Ajustes → nueva fila «Conexión a internet» (después de «Voz del asistente»). Viene APAGADA (`ajustes.internet:false`; los datos guardados antes la heredan apagada).
- Encendida: aparece arriba a la derecha una pastilla discreta «● Conectado». Al apagarla, la pastilla desaparece y la radio se corta.
- Radio con la conexión apagada: pide confirmación («La radio necesita internet. ¿Enciendo la conexión?…»). Si aceptas, se enciende y suena; si no, no sale nada a la red.
- Todo lo demás (agenda, salud, gimnasio, juegos…) sigue igual sin red.
- La función de IA en línea del chat (`Xn`) sigue siendo un stub que devuelve `offline`: no existe servidor; no se ha inventado ninguno.
- Parche sobre el bundle compilado (no hay fuente React en el repo ni en el box): 3 sustituciones en la línea 84.

## 2. Profesor
- `profesor.html` (y copia `educacion/Profesor.html` para la APK): hub nuevo, blanco, verdes y azules. Pestañas «Cursos» y «Extraescolares» separadas.
- Cursos: 1º ESO (10 materias, 364 lecciones) y 1º Bach (11 materias, 388 lecciones). 2º–4º ESO y 2º Bach aparecen como «Sin temario todavía».
- Formalidad progresiva: `body[data-nivel=1..6]`; 1º ESO redondeado y alegre → 1º Bach serif, esquinas de 8 px, colores sobrios.
- Extraescolares: Linux Essentials, Arduino ×4, Raspberry Pi ×4, Robot ×4, Informática, Oposiciones + Policía Nacional, Conducir + Test permiso B, Curso de dibujo, El Profesor clásico.
- El antiguo `profesor.html` (El Profesor, 37 cursos de cultura general, 269 lecciones) se movió sin cambios a `educacion/profesor-clasico.html`.
- No se ha tocado ninguna lección ni el modo Maestro.
- En la app (host appassets) los 1º ESO enlazan a `/educacion/1eso-*/index.html` (packs planos del embed).
- `scripts/build-pack-completo-embed.py`: copia también `educacion/profesor-clasico.html` al embed.

## 3. Modo Maestro en 4 materias de 1º Bach (v20261018b)
- Dibujo Técnico I (31), TIC I (32), Matemáticas CCSS I (33), Economía (26) + EEAE (18): 140 lecciones con guion.
- Mismo runtime local que el resto de Bach: `<materia>/_maestro/maestro-runtime.js` + `maestro-puntero.css` (copiados de `educacion/fyq/_maestro`, md5 8deca3f0…).
- Guion incrustado en cada lección (`<script type="application/json" data-maestro="guion">`), derivado solo del texto: título (h1) y cada apartado (h2) con su primera frase. Los h2 sin id reciben `id="maestro-pN"`; los que ya tenían id (TIC) se usan tal cual. Máximo 14 pasos.
- En mates-ccs había 17 plantillas vacías de guion (sin pasos): se sustituyeron.
- El atajo «Modo maestro» lo inyecta el runtime (barra de progreso o botón fijo).
- Generador reproducible: `scripts/maestro-bach4-guion.py` (se salta lecciones que ya tengan runtime).
- ZIP de descarga regenerados: `downloads/bach1-{dibujo-tec,tic,mates-ccs,economia}-offline.zip`.
- Comprobado en Chrome sin interfaz: 140/140 lecciones cargan con `?maestro=1` sin errores de consola, con el guion cargado y todas las anclas presentes.
