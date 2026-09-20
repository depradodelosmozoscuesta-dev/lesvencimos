# Arranque paso a paso (Linux / Ubuntu / WSL)

Guía corta para poner en marcha **Red Ciudadano Valladolid** en tu PC.
Pensada para quien ya tropezó con `make: go: No such file or directory`.

## 0. Requisitos

- Terminal Linux (Ubuntu nativo o **WSL** en Windows).
- Conexión a internet **solo** para instalar Go/git y clonar (luego el nodo es local).
- Navegador (Chrome, Firefox…).

## 1. Si `apt` dice “Waiting for cache lock”

Otro proceso (a menudo `unattended-upgr`) tiene pillado el instalador.

1. Espera a que termine (puede tardar varios minutos).
2. Cuando vuelva el prompt, sigue.
3. Si lleva más de ~20 min, en **otra** terminal:

```bash
ps aux | grep -E 'unattended|apt|dpkg' | grep -v grep
```

No lances otro `apt` en paralelo mientras veas el candado.

## 2. Instalar herramientas

### Opción A — Go oficial (recomendada; el proyecto pide Go **1.22+**)

```bash
sudo apt update
sudo apt install -y curl git make build-essential

# Descarga Go 1.24.x (ajusta la versión si en go.dev hay una más nueva)
curl -fsSL https://go.dev/dl/go1.24.4.linux-amd64.tar.gz -o /tmp/go.tgz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf /tmp/go.tgz

# PATH (bash)
echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

go version   # debe mostrar go1.24.x
make --version
```

### Opción B — solo `apt` (a veces trae un Go viejo)

```bash
sudo apt update
sudo apt install -y golang-go make git
go version
```

Si `go version` es **menor que 1.22**, usa la **opción A**.

## 3. Clonar o actualizar el repo

**Repo correcto:**

`https://github.com/depradodelosmozoscuesta-dev/Red-ciudadano-valladolid`

```bash
cd ~
git clone https://github.com/depradodelosmozoscuesta-dev/Red-ciudadano-valladolid.git
cd Red-ciudadano-valladolid
git pull
```

Si ya lo tenías clonado:

```bash
cd ~/Red-ciudadano-valladolid   # o la carpeta donde esté
git pull
```

## 4. Compilar y arrancar

```bash
cd ~/Red-ciudadano-valladolid
make run
```

Deja esa terminal abierta. Deberías ver el nodo escuchando.

Solo red cívica (sin juego VitaInk):

```bash
make run-civic
```

## 5. Abrir en el navegador

**En el mismo PC:**

http://127.0.0.1:8080/

**Desde el móvil (misma Wi‑Fi):**

1. Para el `make run` (Ctrl+C).
2. Arranca escuchando en todas las interfaces:

```bash
make build
./bin/valladolid-node --addr 0.0.0.0:8080 --data-dir ./data
```

3. En el PC: `hostname -I` (o `ip a`) y copia la IP (p. ej. `192.168.1.42`).
4. En el móvil: `http://ESA_IP:8080/`
5. Si no carga, abre el puerto en el firewall de Windows/WSL o prueba primero en el PC con `127.0.0.1`.

## 6. Primeros clics (1 minuto)

1. Home / lugares de Valladolid.
2. **Calles** — caminar con flechas / WASD / D-pad.
3. **🏠 Mi casa** — bolsón (puerta, huerto, cocina…).
4. **Biblioteca** — torre-academia.
5. Opcional: chip **🎮 VitaInk** (OFF por defecto) — capa de juego.

Recorrido guiado de ~10 min: [RECORRIDO-10MIN.md](RECORRIDO-10MIN.md).

## 7. Problemas frecuentes

| Síntoma | Qué hacer |
|---------|-----------|
| `make: go: No such file or directory` | Instala Go (paso 2A) y `source ~/.bashrc`. |
| `Waiting for cache lock` | Espera a `unattended-upgr` (paso 1). |
| Go &lt; 1.22 y falla el build | Instala Go oficial 1.24+ (paso 2A). |
| `git: command not found` | `sudo apt install -y git` |
| El navegador no carga | Confirma que `make run` sigue en marcha; prueba `curl -s http://127.0.0.1:8080/api/health` |
| Móvil no ve el nodo | Usa `--addr 0.0.0.0:8080` y la IP de la LAN; misma Wi‑Fi. |
| Puerto ocupado | Otra instancia del nodo: `./bin/valladolid-node --addr 127.0.0.1:8081 --data-dir ./data2` |

Comprobación rápida:

```bash
curl -s http://127.0.0.1:8080/api/health
```

Debe devolver JSON con `"version"` (p. ej. `5.6.0`).

## 8. Parar el nodo

En la terminal del `make run`: **Ctrl+C**.
