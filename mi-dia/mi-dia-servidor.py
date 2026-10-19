#!/usr/bin/env python3
"""
Mi día — central de la casa (red local)
=======================================

Sirve mi-dia.html a todas las pantallas de la casa (tablet de la cocina,
tele del salón, móvil…) y guarda en un archivo las medicinas, los avisos y
qué pastillas se han tomado. Así, si se marca en la cocina, deja de sonar
en el salón.

No necesita internet ni instalar nada: solo Python 3.8 o superior.

    python3 mi-dia-servidor.py --lan        (red de casa, puerto 8080)
    python3 mi-dia-servidor.py --lan 9000   (otro puerto)
    python3 mi-dia-servidor.py              (solo este ordenador)

Sin --lan solo responde a este mismo ordenador (127.0.0.1). Con --lan
responde a todos los aparatos de la wifi de casa; la conexión no va
cifrada (HTTP), así que úsalo solo en una wifi de casa con contraseña.

Luego, en cada pantalla, abre la dirección que aparece al arrancar,
por ejemplo  http://192.168.1.50:8080

La primera vez, si se configura desde otra pantalla (no desde este
ordenador), Mi día pide el código que sale aquí al arrancar.

Los datos quedan en  mi-dia-datos.json  junto a este archivo.
Haz copia de ese archivo de vez en cuando.
"""
import hashlib
import hmac
import json
import os
import re
import secrets
import socket
import sys
import tempfile
import threading
import time
from datetime import datetime, timedelta
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

CARPETA = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(CARPETA, "mi-dia-datos.json")
PAGINA = "mi-dia.html"
MAX_CUERPO = 5 * 1024 * 1024       # 5 MB (las fotos de pastillas van reducidas)
DIAS_HISTORIAL = 90                # se borran las tomas más antiguas

cerrojo = threading.Lock()

# ── PIN: solo se guarda su hash (PBKDF2-SHA256 con sal) ──
ITER_PIN = 100_000


def hash_pin(pin):
    sal = secrets.token_bytes(16)
    h = hashlib.pbkdf2_hmac("sha256", pin.encode("utf-8"), sal, ITER_PIN)
    return f"pbkdf2-sha256${ITER_PIN}${sal.hex()}${h.hex()}"


def pin_correcto(pin, guardado):
    if not isinstance(pin, str) or not isinstance(guardado, str) or len(pin) > 64:
        return False
    partes = guardado.split("$")
    if len(partes) != 4 or partes[0] != "pbkdf2-sha256":
        return False
    try:
        h = hashlib.pbkdf2_hmac("sha256", pin.encode("utf-8"), bytes.fromhex(partes[2]), int(partes[1]))
    except ValueError:
        return False
    return hmac.compare_digest(h.hex(), partes[3])


# ── Intentos fallidos: tras 5 seguidos, espera creciente (30 s, 1, 2, 4, 8 min… hasta 15 min) ──
fallos = {}          # ip -> [n, hasta]; "*" cuenta todos los aparatos juntos


def espera(ip):
    ahora = time.monotonic()
    claves = [ip] if es_local_ip(ip) else [ip, "*"]
    return max((max(0, fallos.get(k, [0, 0])[1] - ahora) for k in claves), default=0)


def anotar_fallo(ip):
    ahora = time.monotonic()
    for k, umbral in ((ip, 5), ("*", 20)):
        f = fallos.setdefault(k, [0, 0])
        f[0] += 1
        if f[0] >= umbral:
            f[1] = ahora + min(900, 30 * 2 ** (f[0] - umbral))


def anotar_acierto(ip):
    fallos.pop(ip, None)


def es_local_ip(ip):
    return ip == "::1" or ip.startswith("127.") or ip == "::ffff:127.0.0.1"


# ── Datos que llegan de fuera: fotos solo locales y sin teléfonos de pago ──
RE_FOTO_DATA = re.compile(r"^data:image/(png|jpeg|webp|gif);base64,[A-Za-z0-9+/]+={0,2}$")
RE_FOTO_RUTA = re.compile(r"^(?![/\\])(?!.*\.\.)[^:?#\\<>\"'\s]+\.(png|jpe?g|webp|gif)$", re.I)


def foto_segura(f):
    if isinstance(f, str) and len(f) <= 3_000_000 and (RE_FOTO_DATA.match(f) or RE_FOTO_RUTA.match(f)):
        return f
    return None


def tel_de_pago(t):
    d = re.sub(r"[^\d+]", "", str(t or ""))
    if d.startswith("+34"):
        d = d[3:]
    elif d.startswith("0034"):
        d = d[4:]
    return bool(re.match(r"^(803|806|807|905|907|118)", d))


def sanear(config):
    config["meds"] = [dict(m, foto=foto_segura(m.get("foto"))) for m in config.get("meds", []) if isinstance(m, dict)]
    contactos = config.get("contactos", [])
    if isinstance(contactos, list):
        config["contactos"] = [c for c in contactos if isinstance(c, dict) and not tel_de_pago(c.get("tel"))]
    return config


# Código para fijar el PIN la primera vez desde otra pantalla (se enseña en la consola)
codigo_inicial = f"{secrets.randbelow(10**6):06d}"


def cargar():
    try:
        with open(DATOS, encoding="utf-8") as f:
            d = json.load(f)
        d.setdefault("version", 0)
        d.setdefault("config", None)
        d.setdefault("tomas", {})
        d.setdefault("pin", None)
        if isinstance(d["pin"], str) and d["pin"].isdigit():
            d["pin"] = hash_pin(d["pin"])        # versiones anteriores lo guardaban en claro
            guardar(d)
        return d
    except FileNotFoundError:
        return {"version": 0, "config": None, "tomas": {}, "pin": None}


def guardar(d):
    """Escritura atómica: si se va la luz a mitad, el archivo anterior sigue entero."""
    fd, tmp = tempfile.mkstemp(dir=CARPETA, prefix=".mi-dia-", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, DATOS)


def podar(tomas):
    limite = (datetime.now() - timedelta(days=DIAS_HISTORIAL)).strftime("%Y-%m-%d")
    return {k: v for k, v in tomas.items() if k[:10] >= limite}


estado = cargar()


def publico(necesita_codigo=False):
    """Lo que ven las pantallas: todo menos el PIN."""
    d = {"version": estado["version"], "config": estado["config"], "tomas": estado["tomas"]}
    if necesita_codigo:
        d["necesitaCodigo"] = True
    return d


class Manejador(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=CARPETA, **k)

    # Solo se sirve la página y la API: nunca el archivo de datos ni el propio servidor.
    def do_GET(self):
        ruta = urlparse(self.path)
        if ruta.path in ("/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/" + PAGINA)
            self.end_headers()
            return
        if ruta.path == "/api/estado":
            v = parse_qs(ruta.query).get("v", [None])[0]
            with cerrojo:
                if v is not None and v == str(estado["version"]):
                    return self.json(200, {"sinCambios": True, "version": estado["version"]})
                return self.json(200, publico(self.necesita_codigo()))
        if ruta.path == "/" + PAGINA:
            return super().do_GET()
        self.send_error(404, "No encontrado")

    def do_HEAD(self):
        self.send_error(405)

    def do_POST(self):
        ruta = urlparse(self.path).path
        try:
            largo = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self.json(400, {"error": "cuerpo"})
        if largo <= 0 or largo > MAX_CUERPO:
            return self.json(413, {"error": "tamaño"})
        try:
            cuerpo = json.loads(self.rfile.read(largo).decode("utf-8"))
            if not isinstance(cuerpo, dict):
                raise ValueError
        except (ValueError, UnicodeDecodeError):
            return self.json(400, {"error": "json"})

        with cerrojo:
            if ruta == "/api/toma":
                clave, info = cuerpo.get("clave"), cuerpo.get("info")
                if not isinstance(clave, str) or len(clave) > 200 or not isinstance(info, dict):
                    return self.json(400, {"error": "datos"})
                # Si ya estaba marcada (otra pantalla a la vez), se queda la primera.
                if clave not in estado["tomas"]:
                    estado["tomas"][clave] = {k: str(info.get(k, ""))[:60] for k in ("hora", "en")}
                    estado["tomas"][clave]["ts"] = info.get("ts") if isinstance(info.get("ts"), (int, float)) else 0
                    return self.cambio()
                return self.json(200, publico())

            if ruta == "/api/deshacer":
                clave = cuerpo.get("clave")
                if isinstance(clave, str) and estado["tomas"].pop(clave, None) is not None:
                    return self.cambio()
                return self.json(200, publico())

            ip = self.client_address[0]
            if ruta == "/api/pin":
                s = espera(ip)
                if s:
                    return self.json(429, {"error": "bloqueado", "espera": int(s) + 1})
                ok = estado["pin"] is not None and pin_correcto(cuerpo.get("pin"), estado["pin"])
                anotar_acierto(ip) if ok else anotar_fallo(ip)
                return self.json(200, {"ok": ok})

            if ruta in ("/api/config", "/api/importar"):
                primera_vez = estado["pin"] is None
                s = espera(ip)
                if s:
                    return self.json(429, {"error": "bloqueado", "espera": int(s) + 1})
                if not primera_vez:
                    if not pin_correcto(cuerpo.get("pin"), estado["pin"]):
                        anotar_fallo(ip)
                        return self.json(403, {"error": "pin"})
                    anotar_acierto(ip)
                elif self.necesita_codigo():
                    # Sin PIN todavía: desde otra pantalla hace falta el código de la consola
                    codigo = cuerpo.get("codigo")
                    if not (isinstance(codigo, str) and hmac.compare_digest(codigo.strip(), codigo_inicial)):
                        anotar_fallo(ip)
                        return self.json(403, {"error": "codigo"})
                config = cuerpo.get("config")
                if not isinstance(config, dict) or not isinstance(config.get("meds", []), list):
                    return self.json(400, {"error": "config"})
                config = sanear(config)
                nuevo = cuerpo.get("nuevoPin")
                if nuevo is not None:
                    if not (isinstance(nuevo, str) and nuevo.isdigit() and 4 <= len(nuevo) <= 8):
                        return self.json(400, {"error": "nuevoPin"})
                    estado["pin"] = hash_pin(nuevo)
                elif primera_vez:
                    return self.json(400, {"error": "falta PIN"})
                estado["config"] = config
                if ruta == "/api/importar" and isinstance(cuerpo.get("tomas"), dict):
                    estado["tomas"] = cuerpo["tomas"]
                return self.cambio()

        self.json(404, {"error": "ruta"})

    def necesita_codigo(self):
        return estado["pin"] is None and not es_local_ip(self.client_address[0])

    def cambio(self):
        estado["version"] += 1
        estado["tomas"] = podar(estado["tomas"])
        try:
            guardar(estado)
        except OSError as e:
            print("⚠ No se pudo guardar:", e, file=sys.stderr)
            return self.json(500, {"error": "disco"})
        return self.json(200, publico(self.necesita_codigo()))

    def json(self, codigo, obj):
        datos = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def end_headers(self):
        if not self.path.startswith("/api/"):
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        if args and "/api/estado" in str(args[0]):
            return   # las pantallas preguntan cada 3 s: no llenar la consola
        sys.stderr.write("%s  %s\n" % (datetime.now().strftime("%H:%M:%S"), fmt % args))


def ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))   # no envía nada: solo pregunta qué interfaz usaría
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def main():
    args = sys.argv[1:]
    lan = "--lan" in args
    resto = [a for a in args if a != "--lan"]
    if len(resto) > 1 or (resto and not resto[0].isdigit()):
        sys.exit("Uso: python3 mi-dia-servidor.py [--lan] [puerto]")
    puerto = int(resto[0]) if resto else 8080
    if not os.path.exists(os.path.join(CARPETA, PAGINA)):
        sys.exit(f"Falta {PAGINA} en esta carpeta ({CARPETA}).")
    servidor = ThreadingHTTPServer(("0.0.0.0" if lan else "127.0.0.1", puerto), Manejador)
    print("─" * 52)
    print("  Mi día · central de la casa")
    if lan:
        print(f"  En cada pantalla abre:  http://{ip_local()}:{puerto}")
    print(f"  En este ordenador:      http://localhost:{puerto}")
    print(f"  Datos en: {DATOS}")
    if lan:
        print("  ⚠ Modo red de casa (--lan): cualquier aparato de esta wifi")
        print("    puede abrir Mi día. La conexión NO va cifrada (HTTP):")
        print("    úsalo solo en la wifi de casa, con contraseña.")
        if estado["pin"] is None:
            print(f"  Código para la primera configuración desde otra pantalla: {codigo_inicial}")
    else:
        print("  Solo este ordenador puede abrirlo. Para las demás")
        print("  pantallas de casa, arranca con:  python3 mi-dia-servidor.py --lan")
    print("  Para parar: Ctrl+C")
    print("─" * 52)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nParado.")


if __name__ == "__main__":
    main()
