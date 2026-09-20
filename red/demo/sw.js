/* Service worker — demo Pages en /red/demo/
 * Shell cache-first con rutas relativas al scope del SW.
 * /api/* no se cachea: la página usa mock-api.js (fixtures).
 */
const CACHE = "valladolid-pages-demo-v1";
const SHELL = [
  "./",
  "./index.html",
  "./css/app.css",
  "./js/app.js",
  "./js/mock-api.js",
  "./manifest.webmanifest",
  "./icons/icon.svg",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
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
  const url = new URL(req.url);
  if (url.pathname.includes("/api/")) {
    // Dejar pasar / fallar: el mock vive en la página (fetch parchado).
    event.respondWith(
      fetch(req).catch(() =>
        new Response(JSON.stringify({ error: "demo pages · sin red", demo: true }), {
          status: 503,
          headers: { "Content-Type": "application/json" },
        })
      )
    );
    return;
  }
  event.respondWith(
    caches.match(req).then((cached) => cached || fetch(req).then((res) => {
      const copy = res.clone();
      caches.open(CACHE).then((c) => c.put(req, copy));
      return res;
    }).catch(() => caches.match("./index.html")))
  );
});
