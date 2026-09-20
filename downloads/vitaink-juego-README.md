# VitaInk — descarga offline

Juego Canvas2D **standalone** (Mari + mundos Berlín/Atenas).  
**No** depende de Red Ciudadano ni de ninguna API remota.

## Online (recomendado en móvil)

1. Abre **https://lesvencimos.com/juego/** en el navegador.
2. Espera a que cargue (la primera visita descarga los assets y el service worker).
3. **Instalar / Añadir a pantalla de inicio**:
   - **Android (Chrome)**: menú ⋮ → *Instalar aplicación* o *Añadir a la pantalla de inicio*.
   - **iOS (Safari)**: Compartir → *Añadir a pantalla de inicio*.
4. Tras instalar, puedes abrir VitaInk sin red (modo standalone).

## Offline (zip descargable)

1. Descomprime este zip en una carpeta.
2. **PC / Mac / Linux**: sirve la carpeta con un servidor estático (el service worker **no** funciona bien con `file://`):

   ```bash
   npx --yes serve .
   ```

   O cualquier host estático (nginx, Caddy, Python `http.server`, etc.) apuntando a esta carpeta.

3. Abre la URL que indique el servidor (p. ej. `http://localhost:3000`).
4. Opcional: Instalar / Añadir a pantalla de inicio desde ese origen local.

### Por qué no abrir el `index.html` a doble clic

Los navegadores bloquean service workers y a menudo módulos ES en `file://`. Usa siempre un servidor estático local o la web.

## Controles

| Entrada | Acción |
|---------|--------|
| **WASD** / flechas | Mover |
| **E** | Cambiar etapa (Berlín ↔ Atenas) |
| **T** | Cambiar estilo disponible |
| **V / 1·2·3** | Vista puppet |
| **O** | Ropa |
| **U** | Puppet / skel-skin |
| **B** | Debug huesos |

En **pantalla táctil** (móvil/tablet) aparece un **D-pad** (WASD) y botones **E** / **T**.  
En escritorio también puedes usar teclado. Si el D-pad no aparece, gira el dispositivo o usa teclado / teclado Bluetooth.

## Requisitos

- Navegador moderno (Chrome, Firefox, Safari, Edge).
- Tras la primera carga online (o desde el servidor local), funciona **offline**.
- Tamaño del paquete: ~8–10 MiB.

## Independencia

VitaInk en `/juego` es independiente de **Red Ciudadano** (`/red`). No llama APIs cívicas ni P2P.
