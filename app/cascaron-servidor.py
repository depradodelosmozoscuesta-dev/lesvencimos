#!/usr/bin/python3
"""
Les vencimos — cascarón local
=============================

Sirve ABRE-AQUI.html y escribe los módulos que le pases
(HTML o ZIP) a la carpeta modules/<id>/ de este directorio.

    python3 cascaron-servidor.py
    python3 cascaron-servidor.py 8787
    python3 cascaron-servidor.py --lan          # wifi de casa (Mi día)

Por defecto escucha SOLO en 127.0.0.1. Los datos no salen a la wifi.
--lan abre 0.0.0.0: cualquiera en esa red local lee /api/datos.
Eso es la casa, no internet. No lo uses en un bar.

No necesita internet. No envía nada. Los datos quedan en data/.
data/ no se sirve como fichero estático. Si se va la luz, el archivo
anterior sigue entero.
"""
from __future__ import annotations

import hashlib
import json
import os
import posixpath
import re
import socket
import sys
import tempfile
import zipfile
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

CARPETA = os.path.dirname(os.path.abspath(__file__))
MODULOS = os.path.join(CARPETA, "modules")
DATOS = os.path.join(CARPETA, "data")
CATALOGO = os.path.join(CARPETA, "catalogo.json")
PAGINA = "ABRE-AQUI.html"
MAX_CUERPO = 30 * 1024 * 1024  # 30 MB: un pack ESO cabe; la biblioteca de 16 MB no entra por aquí
ID_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

os.makedirs(MODULOS, exist_ok=True)
os.makedirs(DATOS, exist_ok=True)


def slug(nombre: str) -> str:
    s = nombre.lower()
    s = re.sub(r"\.(html?|htm|zip)$", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")[:48]
    return s or ("mod-%d" % int(datetime.now().timestamp()))


def atomic_write(ruta: str, datos: bytes) -> None:
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(ruta), prefix=".lv-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(datos)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, ruta)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def sha256_bytes(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def leer_catalogo():
    if not os.path.isfile(CATALOGO):
        return {"modulos": []}
    try:
        with open(CATALOGO, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {"modulos": []}
        data.setdefault("modulos", [])
        return data
    except (OSError, ValueError):
        return {"modulos": []}


def listar_modulos():
    out = []
    if not os.path.isdir(MODULOS):
        return out
    for nombre in sorted(os.listdir(MODULOS)):
        if nombre.startswith("."):
            continue
        d = os.path.join(MODULOS, nombre)
        if not os.path.isdir(d):
            continue
        meta = os.path.join(d, "module.json")
        rec = {"id": nombre, "nombre": nombre, "entrada": "index.html", "bytes": None, "version": None}
        if os.path.isfile(meta):
            try:
                with open(meta, encoding="utf-8") as f:
                    leido = json.load(f)
                if isinstance(leido, dict):
                    rec.update(leido)
            except (OSError, ValueError):
                pass
        rec["id"] = nombre
        out.append(rec)
    return out


def ruta_datos(ident: str) -> str:
    if not ID_OK.match(ident):
        raise ValueError("id")
    return os.path.join(DATOS, ident + ".json")


def leer_datos(ident: str):
    ruta = ruta_datos(ident)
    if not os.path.isfile(ruta):
        return None
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def escribir_datos(ident: str, obj) -> None:
    if not isinstance(obj, (dict, list)):
        raise ValueError("json")
    raw = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
    if len(raw) > 2 * 1024 * 1024:
        raise ValueError("datos demasiado grandes")
    atomic_write(ruta_datos(ident), raw)


def instalar_html(ident: str, nombre: str, datos: bytes) -> dict:
    if not ID_OK.match(ident):
        ident = slug(ident)
    destino = os.path.join(MODULOS, ident)
    atomic_write(os.path.join(destino, "index.html"), datos)
    meta = {
        "id": ident,
        "nombre": nombre or ident,
        "version": datetime.now().strftime("%Y%m%d"),
        "publico": "varios",
        "entrada": "index.html",
        "red": False,
        "permisos": [],
        "sha256": sha256_bytes(datos),
        "bytes": len(datos),
    }
    atomic_write(os.path.join(destino, "module.json"), json.dumps(meta, ensure_ascii=False, indent=2).encode("utf-8"))
    return meta


def _aplanar_zip(destino: str) -> None:
    """Si el ZIP trae una sola carpeta envoltorio, sube su contenido."""
    nombres = [n for n in os.listdir(destino) if n != "module.json" and not n.startswith(".")]
    if len(nombres) != 1:
        return
    unica = os.path.join(destino, nombres[0])
    if not os.path.isdir(unica):
        return
    for item in os.listdir(unica):
        origen = os.path.join(unica, item)
        final = os.path.join(destino, item)
        if os.path.exists(final):
            continue
        os.replace(origen, final)
    try:
        os.rmdir(unica)
    except OSError:
        pass


def instalar_zip(nombre_zip: str, datos: bytes, ident: str | None = None) -> dict:
    ident = ident or slug(nombre_zip)
    if not ID_OK.match(ident):
        ident = slug(ident)
    destino = os.path.join(MODULOS, ident)
    os.makedirs(destino, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=CARPETA, prefix=".lvpack-", suffix=".zip")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(datos)
            f.flush()
            os.fsync(f.fileno())
        with zipfile.ZipFile(tmp) as z:
            if z.testzip() is not None:
                raise ValueError("zip corrupto")
            nombres = z.namelist()
            if any(n.startswith("/") or ".." in n.replace("\\", "/") for n in nombres):
                raise ValueError("zip con rutas peligrosas")
            z.extractall(destino)
        _aplanar_zip(destino)
        entrada = "index.html"
        for cand in ("index.html", "ABRE-AQUI.html"):
            if os.path.isfile(os.path.join(destino, cand)):
                entrada = cand
                break
        else:
            # primer html en la raíz o un nivel
            hallado = None
            for root, _dirs, files in os.walk(destino):
                for fn in files:
                    if fn.lower().endswith(".html"):
                        hallado = os.path.relpath(os.path.join(root, fn), destino)
                        break
                if hallado:
                    break
            if not hallado:
                raise ValueError("el zip no trae HTML")
            entrada = hallado.replace("\\", "/")
        meta_path = os.path.join(destino, "module.json")
        meta = {
            "id": ident,
            "nombre": ident,
            "version": datetime.now().strftime("%Y%m%d"),
            "publico": "varios",
            "entrada": entrada,
            "red": False,
            "permisos": [],
            "sha256": sha256_bytes(datos),
            "bytes": len(datos),
        }
        if os.path.isfile(meta_path):
            try:
                with open(meta_path, encoding="utf-8") as f:
                    viejo = json.load(f)
                if isinstance(viejo, dict):
                    meta.update({k: viejo[k] for k in viejo if k in ("id", "nombre", "version", "publico", "red", "entrada", "permisos")})
            except (OSError, ValueError):
                pass
        atomic_write(meta_path, json.dumps(meta, ensure_ascii=False, indent=2).encode("utf-8"))
        return meta
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def url_permitida(url: str) -> bool:
    """Solo tubería de ficheros. Cero redirects a otra casa."""
    from urllib.parse import urlparse as _p
    u = _p(url)
    host = (u.hostname or "").lower()
    path = u.path or "/"
    if u.scheme == "https" and host == "lesvencimos.com":
        return path.startswith("/downloads/") or path == "/catalogo.json"
    if u.scheme == "http" and host in ("127.0.0.1", "localhost"):
        return path.startswith("/downloads/") or path.endswith(".zip") or path.endswith(".html")
    return False


class _SinRedirect(Exception):
    pass


def bajar_url(url: str) -> bytes:
    from urllib.request import Request, build_opener, HTTPRedirectHandler
    if not url_permitida(url):
        raise ValueError("origen no permitido")

    class BloqueaRedirect(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise _SinRedirect("redirect no permitido")

    opener = build_opener(BloqueaRedirect)
    req = Request(url, headers={"User-Agent": "LesVencimos-cascaron/20260929"})
    try:
        with opener.open(req, timeout=90) as r:
            final = r.geturl()
            if not url_permitida(final):
                raise ValueError("origen no permitido")
            largo = r.headers.get("Content-Length")
            if largo and int(largo) > MAX_CUERPO:
                raise ValueError("tamaño")
            datos = r.read(MAX_CUERPO + 1)
    except _SinRedirect:
        raise ValueError("origen no permitido")
    if len(datos) > MAX_CUERPO:
        raise ValueError("tamaño")
    return datos


def instalar_desde_catalogo(ident: str) -> dict:
    ident = slug(ident)
    cat = leer_catalogo()
    hallado = None
    for m in cat.get("modulos") or []:
        if isinstance(m, dict) and m.get("id") == ident:
            hallado = m
            break
    if not hallado:
        raise ValueError("no está en el catálogo local")
    url = hallado.get("url")
    if not isinstance(url, str) or not url:
        raise ValueError("sin url")
    datos = bajar_url(url)
    meta = instalar_zip(ident + ".zip", datos, ident=ident)
    # conserva nombre/público del catálogo
    meta["nombre"] = hallado.get("nombre") or meta.get("nombre")
    meta["publico"] = hallado.get("publico") or meta.get("publico")
    meta["id"] = ident
    # entrada del catálogo solo si ese archivo existe; si no, la que detectó el ZIP
    cand = hallado.get("entrada")
    if isinstance(cand, str) and cand and os.path.isfile(os.path.join(MODULOS, ident, cand)):
        meta["entrada"] = cand
    atomic_write(
        os.path.join(MODULOS, ident, "module.json"),
        json.dumps(meta, ensure_ascii=False, indent=2).encode("utf-8"),
    )
    return meta


class Manejador(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=CARPETA, **k)

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "geolocation=(), camera=(), microphone=(), payment=(), usb=()")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        super().end_headers()

    def _json(self, codigo: int, obj) -> None:
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        ruta = urlparse(self.path)
        if ruta.path in ("/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/" + PAGINA)
            self.end_headers()
            return
        if ruta.path in ("/api/modulos", "/api/lista"):
            return self._json(200, {"modulos": listar_modulos()})
        if ruta.path == "/api/catalogo":
            return self._json(200, leer_catalogo())
        if ruta.path == "/api/datos":
            from urllib.parse import parse_qs
            qs = parse_qs(ruta.query or "")
            ident = slug((qs.get("id") or [""])[0])
            if not ident:
                return self._json(400, {"error": "id"})
            try:
                obj = leer_datos(ident)
            except ValueError:
                return self._json(400, {"error": "id"})
            except (OSError, json.JSONDecodeError) as e:
                return self._json(500, {"error": "disco", "detalle": str(e)})
            return self._json(200, {"id": ident, "datos": obj})
        # no servir el propio servidor, el expediente ni basura temporal
        rel = posixpath.normpath(ruta.path.lstrip("/"))
        primero = rel.split("/")[0]
        if (
            primero in ("data",) or
            rel.endswith(".py") or
            rel.endswith(".lvpack") or
            rel.startswith(".") or
            "/." in rel or
            rel.startswith(".lv") or
            primero.startswith(".lv")
        ):
            self.send_error(404, "No encontrado")
            return
        return super().do_GET()

    def do_PUT(self):
        if urlparse(self.path).path == "/api/datos":
            return self.do_POST()
        return self._json(405, {"error": "metodo"})

    def do_POST(self):
        ruta = urlparse(self.path).path
        try:
            largo = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self._json(400, {"error": "cuerpo"})
        if largo < 0 or largo > MAX_CUERPO:
            return self._json(413, {"error": "tamaño"})
        datos = self.rfile.read(largo) if largo else b""
        nombre = os.path.basename(self.headers.get("X-Nombre", "modulo.html"))
        ident_hdr = slug(self.headers.get("X-Id", "") or nombre)

        if ruta in ("/api/bajar", "/api/descargar"):
            try:
                cuerpo = json.loads(datos.decode("utf-8") or "{}")
                ident = slug(str(cuerpo.get("id") or ""))
            except (ValueError, UnicodeDecodeError):
                return self._json(400, {"error": "json"})
            if not ident:
                return self._json(400, {"error": "id"})
            try:
                meta = instalar_desde_catalogo(ident)
            except ValueError as e:
                return self._json(400, {"error": str(e)})
            except OSError as e:
                return self._json(500, {"error": "disco", "detalle": str(e)})
            except Exception as e:
                return self._json(502, {"error": "red", "detalle": str(e)})
            return self._json(200, meta)

        if ruta == "/api/datos":
            from urllib.parse import parse_qs
            qs = parse_qs(urlparse(self.path).query or "")
            try:
                cuerpo = json.loads(datos.decode("utf-8") or "{}")
            except (ValueError, UnicodeDecodeError):
                return self._json(400, {"error": "json"})
            ident = slug(str((qs.get("id") or [cuerpo.get("id") or ""])[0]))
            payload = cuerpo.get("datos", cuerpo)
            if "id" in cuerpo and "datos" in cuerpo:
                payload = cuerpo.get("datos")
            try:
                escribir_datos(ident, payload)
            except ValueError as e:
                return self._json(400, {"error": str(e)})
            except OSError as e:
                return self._json(500, {"error": "disco", "detalle": str(e)})
            return self._json(200, {"ok": True, "id": ident})

        if ruta in ("/api/borrar", "/api/quitar"):
            try:
                cuerpo = json.loads(datos.decode("utf-8") or "{}")
                ident = slug(str(cuerpo.get("id") or ""))
            except (ValueError, UnicodeDecodeError):
                return self._json(400, {"error": "json"})
            destino = os.path.join(MODULOS, ident)
            if ident and os.path.isdir(destino):
                import shutil
                shutil.rmtree(destino)
            if cuerpo.get("datos") is True:
                try:
                    os.unlink(ruta_datos(ident))
                except OSError:
                    pass
            return self._json(200, {"ok": True, "id": ident})

        if ruta == "/api/instalar":
            try:
                cuerpo = json.loads(datos.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                return self._json(400, {"error": "json"})
            ident = slug(str(cuerpo.get("id") or cuerpo.get("nombre") or "modulo"))
            html = cuerpo.get("html")
            if not isinstance(html, str) or "<html" not in html.lower():
                return self._json(400, {"error": "html"})
            try:
                meta = instalar_html(ident, str(cuerpo.get("nombre") or ident), html.encode("utf-8"))
            except OSError as e:
                return self._json(500, {"error": "disco", "detalle": str(e)})
            return self._json(200, meta)

        if ruta == "/api/importar":
            if not datos:
                return self._json(400, {"error": "cuerpo"})
            try:
                if nombre.lower().endswith(".zip"):
                    meta = instalar_zip(nombre, datos)
                else:
                    meta = instalar_html(ident_hdr, nombre, datos)
            except ValueError as e:
                return self._json(400, {"error": str(e)})
            except OSError as e:
                return self._json(500, {"error": "disco", "detalle": str(e)})
            return self._json(200, meta)
        return self._json(404, {"error": "ruta"})

    def log_message(self, fmt, *args):
        sys.stderr.write("%s  %s\n" % (datetime.now().strftime("%H:%M:%S"), fmt % args))


def ip_local() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.gethostbyname(socket.gethostname()) if False else s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def main() -> None:
    args = [a for a in sys.argv[1:] if a]
    puerto = 8787
    if "--puerto" in args:
        i = args.index("--puerto")
        puerto = int(args[i + 1])
    elif args and args[0].lstrip("-").isdigit():
        puerto = int(args[0].lstrip("-"))
    if not os.path.exists(os.path.join(CARPETA, PAGINA)):
        sys.exit("Falta %s en %s" % (PAGINA, CARPETA))
    lan = "--lan" in args or "--casa" in args
    host = "0.0.0.0" if lan else "127.0.0.1"
    httpd = ThreadingHTTPServer((host, puerto), Manejador)
    print("─" * 52)
    print("  Les vencimos · cascarón")
    print("  En este ordenador:  http://127.0.0.1:%s" % puerto)
    if lan:
        print("  En la casa:         http://%s:%s" % (ip_local(), puerto))
        print("  AVISO: --lan. Quien esté en esta wifi puede leer data/")
        print("         (pastillas, avance). Eso es la casa, no internet.")
    else:
        print("  Wifi de casa:       python3 cascaron-servidor.py --lan")
    print("  Módulos en:         %s" % MODULOS)
    print("  Expediente:         %s  (no se sirve por HTTP)" % DATOS)
    print("  Para parar: Ctrl+C")
    print("─" * 52)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nParado.")


if __name__ == "__main__":
    main()
