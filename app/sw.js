/* Cascarón Les vencimos — service worker.
   Solo cachea el cascarón. No cachea internet ajeno.
   No intercepta /api/ ni /data/. No hay telemetría.
   v20260930jorge: network-first en HTML (antes cache-first dejaba
   al Samsung con el cascarón viejo que POSTeaba /api/bajar en Pages). */
const CACHE = "lv-cascaron-v20260930jorge";
const PRECACHE = [
  "./ABRE-AQUI.html",
  "./index.html",
  "./instalar.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./LEEME.txt"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

function esDocumento(req, url) {
  if (req.mode === "navigate") return true;
  const accept = req.headers.get("accept") || "";
  if (accept.includes("text/html")) return true;
  return /\.html?$/i.test(url.pathname);
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  const path = url.pathname;
  if (path.includes("/api/") || path.includes("/data/")) return;
  /* Nunca cachear el propio SW ni JSON vivos del catálogo. */
  if (path.endsWith("/sw.js") || path.endsWith("catalogo.json")) return;

  if (esDocumento(req, url)) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.ok) {
            const copia = res.clone();
            caches.open(CACHE).then((c) => c.put(req, copia)).catch(function () {});
          }
          return res;
        })
        .catch(() =>
          caches.match(req).then((hit) => hit || caches.match("./ABRE-AQUI.html"))
        )
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((hit) => {
      if (hit) return hit;
      return fetch(req)
        .then((res) => {
          if (res && res.ok) {
            const copia = res.clone();
            caches.open(CACHE).then((c) => c.put(req, copia)).catch(function () {});
          }
          return res;
        })
        .catch(() => caches.match("./ABRE-AQUI.html"));
    })
  );
});
