/* Cascarón Les vencimos — service worker.
   Solo cachea el cascarón. No cachea internet ajeno.
   No intercepta /api/ ni /data/. No hay telemetría. */
const CACHE = "lv-cascaron-v20260929seg";
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

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  const path = url.pathname;
  if (path.includes("/api/") || path.includes("/data/")) return;
  event.respondWith(
    caches.match(req).then((hit) => {
      if (hit) return hit;
      return fetch(req).catch(() => caches.match("./ABRE-AQUI.html"));
    })
  );
});
