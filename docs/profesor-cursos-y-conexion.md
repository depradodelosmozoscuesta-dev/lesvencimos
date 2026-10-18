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
