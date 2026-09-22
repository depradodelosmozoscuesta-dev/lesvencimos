# El Profesor

Todo el apartado de enseñanza del asistente, sacado entero para que
puedas meterlo donde quieras.

**37 materias · 269 lecciones · 807 preguntas.** Ninguna lección se
queda sin su quiz, y cada respuesta lleva su **porqué**: eso es lo que
separa enseñar de examinar.

## Qué hay aquí

    Profesor.html          ← esto es lo que quieres. Doble clic y va.
    prueba_profesor.py     la prueba en navegador de verdad
    montar.py              vuelve a armar Profesor.html desde las piezas

    piezas-sueltas/
      temario.js           solo el contenido (37 materias)
      profesor.js          solo el programa
      cabecera.html        el envoltorio y los estilos

    para-servidor/
      ensenanza.py         guardar el avance por persona (Python)
      rutas-para-main.py   las cuatro rutas de la API

## Lo rápido

Abre **`Profesor.html`**. Un solo archivo, sin instalar nada, sin
internet y sin servidor. Pregunta quién estudia, y el avance se guarda
en el propio navegador. Cada persona lleva el suyo y no se mezclan.

## Meterlo en otro asistente

**Lo fácil — un marco.** Cero integración:

```html
<iframe src="Profesor.html" style="width:100%;height:100%;border:0"></iframe>
```

**Lo integrado.** Copia el `<style>`, el temario y el `<script>` dentro
del asistente y dile dónde va:

```js
Profesor.montar(document.getElementById("mi-hueco"), {
  cuerpo: document.getElementById("mi-hueco"),
  titulo: document.getElementById("mi-titulo"),   // opcional
  avance: document.getElementById("mi-avance"),   // opcional
  atras:  document.getElementById("mi-atras"),    // opcional
  quien: "ana",     // si ya sabes quién estudia, no lo pregunta
  rol: "peque",     // "peque" deja solo lo básico y sin adultos
});
```

Y si quieres que el avance vaya a un servidor en vez de al navegador,
le pasas dos funciones más:

```js
  leer:    async ()         => (await fetch("/api/ensenanza/3")).json(),
  guardar: async (av, paso)  => fetch("/api/ensenanza/3", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(paso) }),
```

Sin ellas se apaña solo. Para enseñar el tamaño en una pantalla de
inicio: `Profesor.resumen()` → `{ materias: 37, lecciones: 269,
preguntas: 807 }`.

## Dos decisiones que conviene no deshacer

**Lo que aprende uno es suyo.** No hay una pantalla de enseñanza común:
el avance va por persona. Fue decisión tuya y es la correcta.

**`nivel` y `adultos` son cosas DISTINTAS.** `nivel` dice cuánta base
hace falta (básico / medio / avanzado). `adultos` marca materias que no
deben salir en el perfil de un menor aunque el texto sea sencillo.
Confundirlas dejaba «Sexualidad y bienestar» —que es nivel básico y
está escrita con lenguaje llano— en la lista de un niño de ocho años.
La prueba comprueba las dos cosas por separado.

## Un detalle que parece tontería y no lo es

El temario va **incrustado dentro del HTML**, no en un archivo aparte.
Son 650 KB y tiene su precio, pero **Chrome en Android bloquea la carga
de guiones entre archivos cuando se abre con `file://`**. Si el temario
fuera aparte, en la tablet no cargaría nada y la pantalla saldría vacía
sin decir por qué. Ya nos pasó con las recetas.

Por eso la prueba abre el archivo con `file://` y no por http: probando
por http ese problema no se ve.

## Comprobado antes de dártelo

    python prueba_profesor.py

Abre un Chromium de verdad, con `file://`, y recorre: que el temario
entero está (37/269/807), que un adulto ve las 37 materias y los
niveles salen en orden, que se abre una lección con su texto y su quiz,
que al responder **se marca siempre cuál era la buena** —se acierte o
no— y se explica el porqué, que las demás opciones se bloquean, que se
llega al final con su nota, que el avance se guarda y sigue ahí al
reabrir, y que a un peque no le salen ni LPIC-1 ni la materia de
adultos.

**18 comprobaciones, todas en verde, cero errores de JavaScript.**

## Si añades lecciones

Se edita `piezas-sueltas/temario.js` y se vuelve a pasar `montar.py`.
Formato de cada materia:

```js
{ id, titulo, icono, nivel, adultos?, lecciones: [
  { titulo, contenido: ["párrafo", …],
    quiz: [{ pregunta, opciones: [...], correcta: 0, porque: "…" }] } ]}
```

El `porque` no es opcional de verdad: es lo único que enseña de una
respuesta fallada.


## Nota (2026)

Las materias de informática (Linux, ciberseguridad, Python, C++, algoritmos,
LPI y Central Cuba) se movieron al módulo aparte **Asistente Informática**.
Este Profesor queda como escuela general (37 materias).
