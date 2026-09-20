const CACHE = "vitaink-juego-ultra2-2026-09-20";
const PRECACHE = [
  "./_bundle/index-DafhLu3u.js",
  "./assets/hud/png/128/heart-empty.png",
  "./assets/hud/png/128/heart-full.png",
  "./assets/hud/png/128/key.png",
  "./assets/mari/from-mari-gym/idle.png",
  "./assets/mari/from-mari-gym/marcha-L.png",
  "./assets/mari/from-mari-gym/marcha-R.png",
  "./assets/mari/fullbody/idle-clothed-side.png",
  "./assets/mari/fullbody/idle-front.png",
  "./assets/props/side-persp/prop_door_ruin_qleft.png",
  "./assets/props/side-persp/prop_key_bronze_qleft.png",
  "./assets/props/side-persp/prop_key_silver_qleft.png",
  "./assets/props/side-persp/prop_ring_bronze_qleft.png",
  "./assets/world/side-persp/atenas/oleo/far.png",
  "./assets/world/side-persp/atenas/oleo/mid.png",
  "./assets/world/side-persp/atenas/oleo/near.png",
  "./assets/world/side-persp/compat-1024/berlin-muro/oleo/far.png",
  "./assets/world/side-persp/compat-1024/berlin-muro/oleo/mid.png",
  "./assets/world/side-persp/compat-1024/berlin-muro/oleo/near.png",
  "./favicon.svg",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon.svg",
  "./icons.svg",
  "./index.html",
  "./manifest.webmanifest"
];
self.addEventListener("install", (event) => { event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", (event) => { event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", (event) => { if (event.request.method !== "GET") return; event.respondWith(caches.match(event.request).then((cached) => cached || fetch(event.request).then((response) => { const copy = response.clone(); caches.open(CACHE).then((cache) => cache.put(event.request, copy)); return response; }).catch(() => caches.match("./index.html")))); });
