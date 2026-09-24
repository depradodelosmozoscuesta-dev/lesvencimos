#!/usr/bin/env python3
"""
Mi día — central de la casa (red local)
=======================================

Sirve mi-dia.html a todas las pantallas de la casa (tablet de la cocina,
tele del salón, móvil…) y guarda en un archivo las medicinas, los avisos y
qué pastillas se han tomado. Así, si se marca en la cocina, deja de sonar
en el salón.

No necesita internet ni instalar nada: solo Python 3.8 o superior.

    python3 mi-dia-servidor.py            (puerto 8080)
    python3 mi-dia-servidor.py 9000       (otro puerto)

Luego, en cada pantalla, abre la dirección que aparece al arrancar,
por ejemplo  http://192.168.1.50:8080

Los datos quedan en  mi-dia-datos.json  junto a este archivo.
Haz copia de ese archivo de vez en cuando.
"""
import json
import os
import socket
import sys
import tempfile
import threading
from datetime import datetime, timedelta
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

CARPETA = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(CARPETA, "mi-dia-datos.json")
PAGINA = "mi-dia.html"
MAX_CUERPO = 5 * 1024 * 1024       # 5 MB (las fotos de pastillas van reducidas)
DIAS_HISTORIAL = 90                # se borran las tomas más antiguas

cerrojo = threading.Lock()


def cargar():
    try:
        with open(DATOS, encoding="utf-8") as f:
            d = json.load(f)
        d.setdefault("version", 0)
        d.setdefault("config", None)
        d.setdefault("tomas", {})
        d.setdefault("pin", None)
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


def publico():
    """Lo que ven las pantallas: todo menos el PIN."""
    return {"version": estado["version"], "config": estado["config"], "tomas": estado["tomas"]}


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
                return self.json(200, publico())
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

            if ruta == "/api/pin":
                return self.json(200, {"ok": estado["pin"] is not None and cuerpo.get("pin") == estado["pin"]})

            if ruta in ("/api/config", "/api/importar"):
                primera_vez = estado["pin"] is None
                if not primera_vez and cuerpo.get("pin") != estado["pin"]:
                    return self.json(403, {"error": "pin"})
                config = cuerpo.get("config")
                if not isinstance(config, dict) or not isinstance(config.get("meds", []), list):
                    return self.json(400, {"error": "config"})
                nuevo = cuerpo.get("nuevoPin")
                if nuevo is not None:
                    if not (isinstance(nuevo, str) and nuevo.isdigit() and 4 <= len(nuevo) <= 8):
                        return self.json(400, {"error": "nuevoPin"})
                    estado["pin"] = nuevo
                elif primera_vez:
                    return self.json(400, {"error": "falta PIN"})
                estado["config"] = config
                if ruta == "/api/importar" and isinstance(cuerpo.get("tomas"), dict):
                    estado["tomas"] = cuerpo["tomas"]
                return self.cambio()

        self.json(404, {"error": "ruta"})

    def cambio(self):
        estado["version"] += 1
        estado["tomas"] = podar(estado["tomas"])
        try:
            guardar(estado)
        except OSError as e:
            print("⚠ No se pudo guardar:", e, file=sys.stderr)
            return self.json(500, {"error": "disco"})
        return self.json(200, publico())

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
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    if not os.path.exists(os.path.join(CARPETA, PAGINA)):
        sys.exit(f"Falta {PAGINA} en esta carpeta ({CARPETA}).")
    servidor = ThreadingHTTPServer(("0.0.0.0", puerto), Manejador)
    print("─" * 52)
    print("  Mi día · central de la casa")
    print(f"  En cada pantalla abre:  http://{ip_local()}:{puerto}")
    print(f"  En este ordenador:      http://localhost:{puerto}")
    print(f"  Datos en: {DATOS}")
    print("  Para parar: Ctrl+C")
    print("─" * 52)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nParado.")


if __name__ == "__main__":
    main()
