/* VitaInk offline service worker — relative scope (works at /juego/ and unzip root) */
const CACHE = 'vitaink-juego-offline-v1';
const PRECACHE = [
  "./",
  "./index.html",
  "./README-DESCARGA.md",
  "./_bundle/index-DH3RTdl_.js",
  "./assets/hud/png/128/coin-disabled.png",
  "./assets/hud/png/128/coin-night.png",
  "./assets/hud/png/128/coin.png",
  "./assets/hud/png/128/heart-empty-disabled.png",
  "./assets/hud/png/128/heart-empty-night.png",
  "./assets/hud/png/128/heart-empty.png",
  "./assets/hud/png/128/heart-full-disabled.png",
  "./assets/hud/png/128/heart-full-night.png",
  "./assets/hud/png/128/heart-full.png",
  "./assets/hud/png/128/inventory-disabled.png",
  "./assets/hud/png/128/inventory-night.png",
  "./assets/hud/png/128/inventory.png",
  "./assets/hud/png/128/quest-disabled.png",
  "./assets/hud/png/128/quest-night.png",
  "./assets/hud/png/128/quest.png",
  "./assets/hud/png/128/stamina-empty-disabled.png",
  "./assets/hud/png/128/stamina-empty-night.png",
  "./assets/hud/png/128/stamina-empty.png",
  "./assets/hud/png/128/stamina-full-disabled.png",
  "./assets/hud/png/128/stamina-full-night.png",
  "./assets/hud/png/128/stamina-full.png",
  "./assets/hud/png/128/stamina-half-disabled.png",
  "./assets/hud/png/128/stamina-half-night.png",
  "./assets/hud/png/128/stamina-half.png",
  "./assets/hud/png/128/tower_eye-disabled.png",
  "./assets/hud/png/128/tower_eye-night.png",
  "./assets/hud/png/128/tower_eye.png",
  "./assets/mari/puppet/front/abdomen.png",
  "./assets/mari/puppet/front/calf.png",
  "./assets/mari/puppet/front/catalog.json",
  "./assets/mari/puppet/front/chest.png",
  "./assets/mari/puppet/front/elbow_joint.png",
  "./assets/mari/puppet/front/foot.png",
  "./assets/mari/puppet/front/forearm.png",
  "./assets/mari/puppet/front/hand.png",
  "./assets/mari/puppet/front/head.png",
  "./assets/mari/puppet/front/hips.png",
  "./assets/mari/puppet/front/knee_joint.png",
  "./assets/mari/puppet/front/neck_joint.png",
  "./assets/mari/puppet/front/placement.json",
  "./assets/mari/puppet/front/shoulder_joint.png",
  "./assets/mari/puppet/front/thigh.png",
  "./assets/mari/puppet/front/upperarm.png",
  "./assets/mari/puppet/q3/abdomen.png",
  "./assets/mari/puppet/q3/calf.png",
  "./assets/mari/puppet/q3/catalog.json",
  "./assets/mari/puppet/q3/chest.png",
  "./assets/mari/puppet/q3/elbow_joint.png",
  "./assets/mari/puppet/q3/foot.png",
  "./assets/mari/puppet/q3/forearm.png",
  "./assets/mari/puppet/q3/hand.png",
  "./assets/mari/puppet/q3/head.png",
  "./assets/mari/puppet/q3/hips.png",
  "./assets/mari/puppet/q3/knee_joint.png",
  "./assets/mari/puppet/q3/neck_joint.png",
  "./assets/mari/puppet/q3/placement.json",
  "./assets/mari/puppet/q3/shoulder_joint.png",
  "./assets/mari/puppet/q3/thigh.png",
  "./assets/mari/puppet/q3/upperarm.png",
  "./assets/mari/puppet/side/abdomen.png",
  "./assets/mari/puppet/side/calf.png",
  "./assets/mari/puppet/side/catalog.json",
  "./assets/mari/puppet/side/chest.png",
  "./assets/mari/puppet/side/elbow_joint.png",
  "./assets/mari/puppet/side/foot.png",
  "./assets/mari/puppet/side/forearm.png",
  "./assets/mari/puppet/side/hand.png",
  "./assets/mari/puppet/side/head.png",
  "./assets/mari/puppet/side/hips.png",
  "./assets/mari/puppet/side/knee_joint.png",
  "./assets/mari/puppet/side/neck_joint.png",
  "./assets/mari/puppet/side/placement.json",
  "./assets/mari/puppet/side/shoulder_joint.png",
  "./assets/mari/puppet/side/thigh.png",
  "./assets/mari/puppet/side/upperarm.png",
  "./assets/props/side-persp/prop_key_bronze_qleft.png",
  "./assets/props/side-persp/prop_key_silver_qleft.png",
  "./assets/props/side-persp/prop_ring_bronze_qleft.png",
  "./assets/ropa/day/viajero-pradera/boots_L.png",
  "./assets/ropa/day/viajero-pradera/boots_R.png",
  "./assets/ropa/day/viajero-pradera/pants_L.png",
  "./assets/ropa/day/viajero-pradera/pants_R.png",
  "./assets/ropa/day/viajero-pradera/placement.json",
  "./assets/ropa/day/viajero-pradera/sleeves_L.png",
  "./assets/ropa/day/viajero-pradera/sleeves_R.png",
  "./assets/ropa/day/viajero-pradera/torso.png",
  "./assets/ropa/viajero-pradera/acc_cape_short.png",
  "./assets/ropa/viajero-pradera/placement.json",
  "./assets/world/side-persp/compat-1024/atenas/oleo/far.png",
  "./assets/world/side-persp/compat-1024/atenas/oleo/mid.png",
  "./assets/world/side-persp/compat-1024/atenas/oleo/near.png",
  "./assets/world/side-persp/compat-1024/berlin-muro/oleo/far.png",
  "./assets/world/side-persp/compat-1024/berlin-muro/oleo/mid.png",
  "./assets/world/side-persp/compat-1024/berlin-muro/oleo/near.png",
  "./favicon.svg",
  "./icon.svg",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon.svg",
  "./icons.svg",
  "./manifest.webmanifest",
  "./sw.js"
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).then((res) => {
        if (!res || res.status !== 200 || (res.type !== 'basic' && res.type !== 'cors')) return res;
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copy));
        return res;
      }).catch(() => caches.match('./index.html'));
    })
  );
});
