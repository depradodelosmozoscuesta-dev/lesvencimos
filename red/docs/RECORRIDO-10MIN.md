# Recorrido de 10 minutos — cívico + VitaInk

Guía rápida y cálida para probar **Red Ciudadano Valladolid** en dos mitades:
primero la **red cívica** (lugares, Calles, Capas), luego la capa opcional **VitaInk** (juego / LARP virtual).

Sin nube. Todo local. VitaInk **no** cambia el directorio cívico.

---

## Preparación (~1 min)

```bash
git pull
make run
```

Abre en el navegador: **http://127.0.0.1:8080/**

**Móvil en la misma red:** arranca el nodo escuchando en todas las interfaces y entra por la IP del equipo:

```bash
./bin/valladolid-node --addr 0.0.0.0:8080 --data-dir ./data
# http://IP-DE-TU-PC:8080/
```

(`make run` usa `127.0.0.1:8080`, solo accesible desde la misma máquina.)

Comprueba que el nodo responde: la PWA carga Calles (o el home) y la campana 🔔 está arriba.

---

## Parte A — Solo cívico (~5 min)

VitaInk viene **OFF** por defecto. Así se ve la red ciudadana pura.

| Min | Qué hacer | Qué notar |
|-----|-----------|-----------|
| 0–1 | Mira el **home / lugares**. Alterna Calles · Mapa · Lista si aparecen. | Lugares **iguales** (sin ranking de pago). |
| 1–3 | En **Calles**, camina con D-pad / flechas / WASD / arrastre. Prueba 🚶 Andar ↔ bici si quieres. | Calles, zonas, clima/día-noche; sin GPS. |
| 3–4 | Abre **un lugar** (tap en pin o desde Lista). Mira Info / Avisos / Contacto. | Página del lugar + asistente FAQ local. |
| 4–5 | Pulsa **🗂️ Capas**. Deja **🎮 VitaInk** desmarcado. Activa/desactiva Paradas, Bancos, Sellos… | Capas cívicas solo. Sin overlay de juego. |

**Opcional — build solo cívico:** si compilas sin plugin (`make build-civic` / `make run-civic`), los chips de juego (**🎮 VitaInk**, **🧍 Personaje**, **🧭 Maestros**, etc.) **no aparecen**: la PWA oculta la capa porque `/api/vitaink/*` no está montado. Con `make run` normal, el chip 🎮 existe pero sigue **OFF** hasta que lo enciendas.

Cuando termines la Parte A, el directorio y Calles siguen siendo la misma red ciudadana.

---

## Parte B — VitaInk (~5 min)

Activa la capa de juego (plugin montado + interruptor ON). Todo es **virtual**, sin plata.

| Min | Qué hacer | Chips / UI |
|-----|-----------|------------|
| 0–1 | Enciende VitaInk: chip **🎮 VitaInk** en el HUD **o** 🗂️ Capas → marca «🎮 VitaInk (juego virtual)». El HUD pasa a «🎮 VitaInk ON». | Aparecen chips de juego bajo **⋯ Más**. |
| 1–2 | **⋯ Más** → **🧍 Personaje**. Nombre / facción / guardar (stub). | Personaje local, solo puntos de juego. |
| 2–3 | **⋯ Más** → **🧭 Maestros**. Elige un maestro → **Seguir maestro** → **Meditar** (o meditar con duda). | Senda filosófica: alineación, lecciones, diario. |
| 3–4 | **Hablar:** acércate a un alma/PNJ en Calles → botón **💬 Hablar** (encuentro breve) **o** en Maestros usa el bloque de diálogo / «Preguntar». | Encuentro cerca del alma · diálogo en panel. |
| 4–5 | Si te sobra un minuto: **⋯ Más** → **🌅 Rito** (una vez al día) **o** acércate a **🛕 Ermita** → Retiro. Luego **⋯ Más** → **📖 Códice** y busca algo (p. ej. «misericordia»). | Rito / ermita opcionales · Códice = archivo de lo desbloqueado. |

Otros chips que puedes ver (no hace falta abrirlos ahora): **🚶 Peregrinación**, **⚡ Dios** (PIN operador), Reliquias, Sínodo, Crónica, Ranking, Tesoros, Misiones.

---

## Cierre — apagar la capa y recordar el build cívico

1. **Apagar VitaInk:** pulsa de nuevo **🎮 VitaInk** (vuelve a OFF) **o** 🗂️ Capas → desmarca «🎮 VitaInk». Calles vuelve a la vista ciudadana; los overlays de juego se ocultan.
2. **Nodo solo cívico (sin plugin):**

   ```bash
   make run-civic
   ```

   Equivale a `go build -tags novitaink …`. Las rutas `/api/vitaink/*` dan 404 y la PWA **oculta** los chips de juego. Ideal si solo quieres red ciudadana (Calles, chat, casa, prensa…).

3. Volver al nodo completo: `make run` (build por defecto con VitaInk montado, capa **OFF** hasta que la actives).

---

## Chips de referencia (UI actual)

| Chip | Dónde | Rol |
|------|--------|-----|
| 🎮 VitaInk | HUD / Capas | Interruptor de la capa de juego |
| 🧍 Personaje | ⋯ Más | Avatar / facción stub |
| 🧭 Maestros | ⋯ Más | Seguir, meditar, voto, diálogo |
| 💬 Hablar | Calles (cerca de alma) | Encuentro breve |
| 🛕 Ermita | Marcador en Calles | Retiro / meditar profundo |
| 🌅 Rito | ⋯ Más | Reflexión diaria |
| 🚶 Peregrinación | ⋯ Más | Senda multi-parada |
| 📖 Códice | ⋯ Más | Archivo buscable de la senda |
| ⚡ Dios | ⋯ Más | Panel operador (PIN) |

---

## Más detalle

- Flujo completo del nodo: [FLUJO-USO.md](FLUJO-USO.md)
- Despliegue / AP / HTTPS: [DESPLIEGUE.md](DESPLIEGUE.md) · [MODO-AP.md](MODO-AP.md) · [HTTPS.md](HTTPS.md)
- README del repo: frontera cívico ↔ VitaInk, `make run` / `make run-civic`
