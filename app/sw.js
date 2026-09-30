/* Legacy /app/ SW — v20260930m: product is Estantería Completo, not cascarón.
   Clears old cascarón caches and stays out of the way. */
const CACHE = "lv-app-redirect-v20260930m";
self.addEventListener("install", (e) => { e.waitUntil(self.skipWaiting()); });
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.mode === "navigate" && url.pathname.indexOf("/app") === 0) {
    event.respondWith(Response.redirect("/estanteria.html", 302));
  }
});
