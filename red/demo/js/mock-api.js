/* mock-api.js
 * Capa demo para GitHub Pages / hosting estático en /red/demo/.
 *
 * Intercepta window.fetch hacia /api/* y responde con fixtures de Valladolid.
 * Esto NO es el nodo Go: chat E2E, depósito, federación viva, VitaInk, etc.
 * quedan vacíos o con mensajes honestos de demostración.
 *
 * Comentarios en español a propósito (demo comercial cívico).
 */
(function () {
  "use strict";

  const DEMO_BASE = "/red/demo";
  const DEMO_VERSION = "5.18.0-pages-demo";
  const DEMO_NODE = "demo-pages-valladolid";
  const DEMO_USER = "demo-user-civic-pages";

  const PLACES = [
  {
    "id": "ayuntamiento",
    "name": "Ayuntamiento",
    "category": "administracion",
    "description": "Casa Consistorial de Valladolid. Gestiones municipales, padrones y atención ciudadana.",
    "emoji": "🏛️",
    "zone": "centro",
    "map_x": 50,
    "map_y": 46
  },
  {
    "id": "comisaria",
    "name": "Comisaría",
    "category": "seguridad",
    "description": "Comisaría de Policía Nacional en Valladolid. Denuncias, avisos de seguridad y atención ciudadana.",
    "emoji": "🚓",
    "zone": "este",
    "map_x": 72,
    "map_y": 40
  },
  {
    "id": "mercado",
    "name": "Mercado",
    "category": "comercio",
    "description": "Mercado del Val y mercados municipales de Valladolid. Puestos locales, frescos y comercio de barrio.",
    "emoji": "🥬",
    "zone": "centro",
    "map_x": 42,
    "map_y": 52
  },
  {
    "id": "centro-comercial",
    "name": "Centro comercial",
    "category": "comercio",
    "description": "Centros comerciales y comercio local de Valladolid. Horarios, servicios y directorio de tiendas.",
    "emoji": "🛍️",
    "zone": "este",
    "map_x": 82,
    "map_y": 55
  },
  {
    "id": "residencial",
    "name": "Residencial",
    "category": "vivienda",
    "description": "Zonas residenciales y vivienda comunitaria de Valladolid. Portales, avisos de vecinos y servicios del edificio.",
    "emoji": "🏘️",
    "zone": "oeste",
    "map_x": 18,
    "map_y": 48
  },
  {
    "id": "tablon-anuncios",
    "name": "Tablón de anuncios",
    "category": "comunicacion",
    "description": "Tablón cívico de Valladolid. Anuncios locales, avisos del barrio y carteles ciudadanos sin trackers.",
    "emoji": "📋",
    "zone": "centro",
    "map_x": 56,
    "map_y": 58
  },
  {
    "id": "biblioteca-publica",
    "name": "Biblioteca",
    "category": "cultura",
    "description": "Biblioteca Pública de Valladolid · torre de la academia ciudadana. Catálogo, préstamos, sala de lectura y salón de pergaminos bajo lámparas cálidas.",
    "emoji": "📚",
    "zone": "oeste",
    "map_x": 28,
    "map_y": 36
  },
  {
    "id": "universidad",
    "name": "Universidad",
    "category": "educacion",
    "description": "Universidad de Valladolid. Avisos académicos, campus y servicios al estudiante.",
    "emoji": "🎓",
    "zone": "norte",
    "map_x": 38,
    "map_y": 18
  },
  {
    "id": "iglesia",
    "name": "Iglesia",
    "category": "religion",
    "description": "Iglesias y parroquias de Valladolid. Horarios de culto, avisos parroquiales y actividades comunitarias.",
    "emoji": "⛪",
    "zone": "centro",
    "map_x": 46,
    "map_y": 38
  },
  {
    "id": "hospital-clinico",
    "name": "Hospital",
    "category": "salud",
    "description": "Hospital Clínico Universitario de Valladolid. Urgencias, citas y avisos sanitarios locales.",
    "emoji": "🏥",
    "zone": "norte",
    "map_x": 58,
    "map_y": 14
  },
  {
    "id": "centro-salud",
    "name": "Centro de salud",
    "category": "salud",
    "description": "Centros de salud de Valladolid. Citas de atención primaria, vacunas y avisos sanitarios de barrio.",
    "emoji": "🩺",
    "zone": "este",
    "map_x": 78,
    "map_y": 28
  },
  {
    "id": "farmacia-guardia",
    "name": "Farmacia de guardia",
    "category": "salud",
    "description": "Farmacias de guardia en Valladolid. Turnos, avisos de urgencia farmacéutica y localización del día.",
    "emoji": "💊",
    "zone": "este",
    "map_x": 70,
    "map_y": 32
  },
  {
    "id": "correos",
    "name": "Correos",
    "category": "servicios",
    "description": "Oficina de Correos en Valladolid. Envíos, recogidas, certificados y atención postal local.",
    "emoji": "📮",
    "zone": "centro",
    "map_x": 54,
    "map_y": 48
  },
  {
    "id": "estacion",
    "name": "Estación",
    "category": "transporte",
    "description": "Estación de tren y autobuses de Valladolid. Horarios, andenes, incidencias y servicios al viajero.",
    "emoji": "🚉",
    "zone": "sur",
    "map_x": 48,
    "map_y": 78
  },
  {
    "id": "parque",
    "name": "Parque",
    "category": "ocio",
    "description": "Parque Campo Grande y otros parques de Valladolid. Zonas verdes, avisos de mantenimiento y actividades al aire libre.",
    "emoji": "🌳",
    "zone": "oeste",
    "map_x": 32,
    "map_y": 58
  },
  {
    "id": "colegio",
    "name": "Colegio",
    "category": "educacion",
    "description": "Colegios e institutos de Valladolid. Avisos escolares, calendario y servicios a familias.",
    "emoji": "🏫",
    "zone": "oeste",
    "map_x": 22,
    "map_y": 30
  },
  {
    "id": "bomberos",
    "name": "Bomberos",
    "category": "seguridad",
    "description": "Parque de Bomberos de Valladolid. Emergencias, prevención y avisos de seguridad ciudadana.",
    "emoji": "🚒",
    "zone": "este",
    "map_x": 86,
    "map_y": 42
  },
  {
    "id": "juzgados",
    "name": "Juzgados",
    "category": "administracion",
    "description": "Ciudad de la Justicia de Valladolid. Información de sedes, citaciones y atención al público.",
    "emoji": "⚖️",
    "zone": "norte",
    "map_x": 66,
    "map_y": 22
  },
  {
    "id": "teatro",
    "name": "Teatro",
    "category": "cultura",
    "description": "Teatro Calderón y espacios escénicos de Valladolid. Cartelera, entradas y avisos culturales.",
    "emoji": "🎭",
    "zone": "centro",
    "map_x": 44,
    "map_y": 44
  },
  {
    "id": "museo",
    "name": "Museo",
    "category": "cultura",
    "description": "Museo Nacional de Escultura y museos de Valladolid. Exposiciones, horarios y visitas.",
    "emoji": "🖼️",
    "zone": "centro",
    "map_x": 38,
    "map_y": 42
  },
  {
    "id": "piscina",
    "name": "Piscina",
    "category": "deporte",
    "description": "Piscinas municipales de Valladolid. Horarios, abonos y avisos de mantenimiento.",
    "emoji": "🏊",
    "zone": "sur",
    "map_x": 30,
    "map_y": 72
  },
  {
    "id": "polideportivo",
    "name": "Polideportivo",
    "category": "deporte",
    "description": "Polideportivos municipales de Valladolid. Pistas, reservas y actividades deportivas.",
    "emoji": "🏟️",
    "zone": "sur",
    "map_x": 62,
    "map_y": 74
  },
  {
    "id": "cementerio",
    "name": "Cementerio",
    "category": "servicios",
    "description": "Cementerio municipal de Valladolid. Horarios de visita, información de servicios y avisos.",
    "emoji": "🕊️",
    "zone": "sur",
    "map_x": 78,
    "map_y": 82
  },
  {
    "id": "oficina-empleo",
    "name": "Oficina de empleo",
    "category": "servicios",
    "description": "Oficina de empleo de Valladolid. Citas, ofertas locales y orientación laboral ciudadana.",
    "emoji": "💼",
    "zone": "norte",
    "map_x": 48,
    "map_y": 26
  },
  {
    "id": "gimnasio",
    "name": "Gimnasio",
    "category": "deporte",
    "description": "Gimnasios y actividad física suave en Valladolid. App local Virginia y avisos del centro.",
    "emoji": "🏋️",
    "zone": "oeste",
    "map_x": 16,
    "map_y": 62
  },
  {
    "id": "salud",
    "name": "Salud",
    "category": "salud",
    "description": "Apartado de salud de Valladolid: acceso igual a Hospital, Centro de salud, Farmacia de guardia y Gimnasio (sin ranking de pago).",
    "emoji": "❤️",
    "zone": "norte",
    "map_x": 54,
    "map_y": 20
  },
  {
    "id": "herramientas",
    "name": "Herramientas y utilidades",
    "category": "herramientas",
    "description": "Taller cívico de Valladolid: Tinta (texto e imagen), Wikipedia offline, impresora 3D, asistente y Gimnasio Virginia.",
    "emoji": "🧰",
    "zone": "red",
    "map_x": 88,
    "map_y": 14
  },
  {
    "id": "taller-comunitario",
    "name": "Taller comunitario",
    "category": "comunidad",
    "description": "Colaboración ciudadana: proponé un proyecto, partid tareas, procesad en local y compartid el resultado. Sin nube Big Tech ni ranking de pago.",
    "emoji": "🛠️",
    "zone": "red",
    "map_x": 80,
    "map_y": 22
  },
  {
    "id": "personas",
    "name": "Personas",
    "category": "comunidad",
    "description": "Directorio ligero de tarjetas públicas de vecinos. No es la casa privada: bio breve, imagen opcional y opt-in de timbre.",
    "emoji": "👤",
    "zone": "red",
    "map_x": 12,
    "map_y": 16
  },
  {
    "id": "federacion",
    "name": "Federación",
    "category": "red",
    "description": "Nodos autónomos federados: avisos críticos, índices de prensa y directorio cívico esencial entre peers conocidos. Sin chat privado ni casas ni depósitos.",
    "emoji": "🔗",
    "zone": "red",
    "map_x": 90,
    "map_y": 86
  },
  {
    "id": "prensa",
    "name": "Prensa",
    "category": "medios",
    "description": "Prensa limpia de Valladolid: ediciones .pucela en hojas (pasar página). Gratis para el lector. Anuncios solo estáticos. Sin vídeo, pop-ups ni trackers.",
    "emoji": "📰",
    "zone": "centro",
    "map_x": 60,
    "map_y": 54
  }
];
  const THEMES = {
  "biblioteca-publica": [
    "torre-academia",
    "Torre de la academia",
    "Piedra gótica, lámparas cálidas y un salón de pergaminos."
  ],
  "ayuntamiento": [
    "piedra-civica",
    "Piedra cívica",
    "Sillería clara, faroles de plaza y el ritmo pausado del consistorio."
  ],
  "mercado": [
    "plaza-mercado",
    "Plaza de mercado",
    "Toldos, puestos y un aire de plaza cuando toca día de mercado."
  ],
  "hospital-clinico": [
    "salud-suave",
    "Salud suave",
    "Luz limpia, pasillos calmados y un pulso sereno de cuidado."
  ],
  "centro-salud": [
    "salud-suave",
    "Salud suave",
    "Luz limpia y un pulso sereno de cuidado."
  ],
  "salud": [
    "salud-suave",
    "Salud suave",
    "Luz limpia y un pulso sereno de cuidado."
  ],
  "farmacia-guardia": [
    "salud-suave",
    "Salud suave",
    "Luz limpia y un pulso sereno de cuidado."
  ],
  "parque": [
    "jardin",
    "Jardín",
    "Hojas que se mueven con la brisa y bancos a la sombra."
  ],
  "iglesia": [
    "piedra-sagrada",
    "Piedra sagrada",
    "Arcos serenos y una luz tibia de vela en la nave."
  ],
  "residencial": [
    "bolson",
    "Bolsón vecinal",
    "Portales redondos, verdes musgo y el calor de la madriguera."
  ]
};

  function jsonResp(data, status) {
    return new Response(JSON.stringify(data), {
      status: status || 200,
      headers: { "Content-Type": "application/json; charset=utf-8" },
    });
  }

  function notFound(msg) {
    return jsonResp({ error: msg || "no encontrado (demo)" }, 404);
  }

  function pathnameOf(url) {
    try { return new URL(url, location.origin).pathname; }
    catch (_) { return String(url || ""); }
  }

  function queryOf(url) {
    try { return new URL(url, location.origin).searchParams; }
    catch (_) { return new URLSearchParams(); }
  }

  function filterPlaces(q) {
    if (!q) return PLACES.slice();
    const needle = String(q).toLowerCase();
    return PLACES.filter(function (p) {
      return (
        p.name.toLowerCase().indexOf(needle) >= 0 ||
        p.category.toLowerCase().indexOf(needle) >= 0 ||
        p.description.toLowerCase().indexOf(needle) >= 0 ||
        p.id.toLowerCase().indexOf(needle) >= 0
      );
    });
  }

  function findPlace(id) {
    id = decodeURIComponent(id);
    return PLACES.find(function (p) { return p.id === id; }) || null;
  }

  function buildPage(p) {
    const th = THEMES[p.id] || null;
    const page = {
      place: p,
      format: "place-page",
      version: 1,
      assistant: {
        status: "local",
        label: "Asistente del " + p.name,
        ask_path: "/api/places/" + p.id + "/asistente/ask",
        faq_path: "/api/places/" + p.id + "/asistente/faq",
        note: "FAQ local offline · demo Pages · no es IA en la nube",
      },
      sections: [
        {
          id: "info",
          title: "Info",
          body: p.description,
          items: [
            "Información local del nodo. Sin dependencia de la nube.",
            "Demo Pages: contenido embebido (fixture).",
          ],
        },
        {
          id: "avisos",
          title: "Avisos",
          items: [
            "Sin avisos nuevos en este piloto.",
            "Demo Pages: la campana real requiere el nodo Go.",
          ],
        },
        {
          id: "contacto",
          title: "Contacto",
          items: [
            "Contacto local del lugar en Valladolid.",
            "Chat E2E entre vecinos: usa la sección Mensajes (requiere nodo).",
          ],
        },
      ],
      stalls: [],
      tools: [],
    };
    if (th) {
      page.theme = th[0];
      page.theme_label = th[1];
      page.theme_flavor = th[2];
    }
    return page;
  }

  function citymap() {
    return {
      places: PLACES.map(function (p) {
        return {
          id: p.id,
          name: p.name,
          emoji: p.emoji,
          category: p.category,
          zone: p.zone,
          map_x: p.map_x,
          map_y: p.map_y,
        };
      }),
      demo: true,
      note: "Mapa esquemático demo (no GIS).",
    };
  }

  function handleApi(pathname, method, url) {
    method = (method || "GET").toUpperCase();
    var path = pathname.replace(/\/+$/, "") || "/";
    var qs = queryOf(url);

    if (path === "/api/health") {
      return jsonResp({
        ok: true,
        name: "Red Ciudadano Valladolid (Pages demo)",
        version: DEMO_VERSION,
        node_id: DEMO_NODE,
        user_id: DEMO_USER,
        demo: true,
      });
    }
    if (path === "/api/whoami") {
      return jsonResp({
        user_id: DEMO_USER,
        node_id: DEMO_NODE,
        box_public: "demo",
        version: DEMO_VERSION,
        name: "Red Ciudadano Valladolid (Pages demo)",
        casa: { exists: false },
        presence: { mode: "ausente" },
        demo: true,
      });
    }

    if (path === "/api/places") {
      var q = qs.get("q") || "";
      var list = filterPlaces(q);
      return jsonResp({ places: list, count: list.length, q: q, demo: true });
    }
    var mPage = path.match(/^\/api\/places\/([^/]+)\/page$/);
    if (mPage) {
      var pl = findPlace(mPage[1]);
      if (!pl) return notFound("lugar no encontrado");
      return jsonResp(buildPage(pl));
    }
    var mPlace = path.match(/^\/api\/places\/([^/]+)$/);
    if (mPlace && method === "GET") {
      var p1 = findPlace(mPlace[1]);
      if (!p1) return notFound("lugar no encontrado");
      return jsonResp(p1);
    }
    var mFaq = path.match(/^\/api\/places\/([^/]+)\/asistente\/faq$/);
    if (mFaq) {
      return jsonResp({
        faqs: [
          { question: "¿Qué es esta demo?", answer: "Cáscara PWA para Pages en /red/demo/. Datos mock; el nodo Go no está aquí." },
          { question: "¿Cómo pruebo la red real?", answer: "En el repo del nodo: make run-civic → http://127.0.0.1:8080/" },
        ],
        demo: true,
      });
    }
    var mAsk = path.match(/^\/api\/places\/([^/]+)\/asistente\/ask$/);
    if (mAsk) {
      return jsonResp({
        answer: "Demo Pages: no hay motor FAQ del nodo. Explora Lugares y Mapa con datos embebidos de Valladolid.",
        demo: true,
      });
    }

    if (path === "/api/peers") {
      return jsonResp({
        peers: [],
        count: 0,
        multicast_limited: true,
        note: "Demo Pages: sin mDNS ni peers LAN.",
        service: "_valladolid-node._tcp",
        demo: true,
      });
    }

    if (path === "/api/citymap") return jsonResp(citymap());

    if (path.indexOf("/api/city/") === 0) {
      if (path === "/api/city/stamps") return jsonResp({ stamps: [], album: [], count: 0, demo: true });
      if (path === "/api/city/events") return jsonResp({ events: [], count: 0, demo: true });
      if (path === "/api/city/missions") return jsonResp({ missions: [], count: 0, demo: true });
      if (path === "/api/city/paradas") return jsonResp({ paradas: [], count: 0, demo: true });
      if (path === "/api/city/bancos") return jsonResp({ bancos: [], count: 0, demo: true });
      if (path === "/api/city/luces") return jsonResp({ luces: [], count: 0, demo: true });
      if (path === "/api/city/mercado") return jsonResp({ open: false, demo: true });
      if (path.indexOf("/api/city/vignette") === 0) return jsonResp({ vignette: null, demo: true });
      return jsonResp({ demo: true, items: [] });
    }

    if (path === "/api/campana" || path === "/api/campana/leer") {
      return jsonResp({ items: [], unread: 0, count: 0, demo: true });
    }

    if (path === "/api/contacts") return jsonResp({ contacts: [], count: 0, demo: true });
    if (path === "/api/chat/presence" || path === "/api/chat/presence/rotate") {
      return jsonResp({ mode: "ausente", mode_label: "Ausente (demo)", demo: true });
    }
    if (path.indexOf("/api/chat/") === 0) {
      return jsonResp({ messages: [], threads: [], demo: true });
    }

    // VitaInk: 404 → la UI cívica oculta chips de juego
    if (path.indexOf("/api/vitaink") === 0) {
      return notFound("VitaInk no incluido en demo cívico Pages");
    }

    if (path === "/api/herramientas") {
      return jsonResp({ tools: [], count: 0, demo: true });
    }
    if (path.indexOf("/api/herramientas/asistente") === 0) {
      return jsonResp({
        answer: "Asistente general no disponible en la cáscara Pages. Usa el directorio de lugares.",
        faqs: [],
        demo: true,
      });
    }

    if (path === "/api/shops" || path.indexOf("/api/shops/") === 0) {
      return jsonResp({ shops: [], count: 0, demo: true });
    }
    if (path === "/api/personas" || path.indexOf("/api/personas/") === 0) {
      return jsonResp({ personas: [], count: 0, demo: true });
    }
    if (path === "/api/prensa" || path.indexOf("/api/prensa/") === 0) {
      return jsonResp({ editions: [], count: 0, demo: true });
    }
    if (path === "/api/pucela" || path.indexOf("/api/pucela/") === 0) {
      return jsonResp({ items: [], count: 0, demo: true });
    }
    if (path.indexOf("/api/taller") === 0) return jsonResp({ proyectos: [], count: 0, demo: true });
    if (path.indexOf("/api/casa") === 0) return jsonResp({ demo: true, note: "Mi casa requiere nodo." });
    if (path.indexOf("/api/deposito") === 0) return jsonResp({ items: [], demo: true });
    if (path.indexOf("/api/mostrador") === 0) return jsonResp({ catalog: [], solicitudes: [], demo: true });
    if (path.indexOf("/api/files") === 0) return jsonResp({ files: [], demo: true });
    if (path.indexOf("/api/federacion") === 0) return jsonResp({ peers: [], avisos: [], count: 0, demo: true });
    if (path.indexOf("/api/node") === 0) {
      return jsonResp({ places_count: PLACES.length, peers_count: 0, version: DEMO_VERSION, demo: true });
    }
    if (path.indexOf("/api/changelog") === 0 || path.indexOf("/api/novedades") === 0) {
      return jsonResp({ items: [], demo: true });
    }

    if (path.indexOf("/api/") === 0) {
      return jsonResp({ ok: true, demo: true, stub: path, note: "Endpoint no implementado en demo Pages." });
    }
    return null;
  }

  // Mantener history bajo /red/demo/
  function rebaseHistoryUrl(url) {
    if (typeof url !== "string") return url;
    if (url.startsWith("http://") || url.startsWith("https://") || url.startsWith("?")) return url;
    if (url.startsWith(DEMO_BASE)) return url;
    if (url === "/" || url === "") return DEMO_BASE + "/";
    if (url.startsWith("/")) return DEMO_BASE + url;
    return url;
  }
  try {
    var _push = history.pushState.bind(history);
    var _replace = history.replaceState.bind(history);
    history.pushState = function (state, title, url) {
      return _push(state, title, rebaseHistoryUrl(url));
    };
    history.replaceState = function (state, title, url) {
      return _replace(state, title, rebaseHistoryUrl(url));
    };
  } catch (_) {}

  function ensureBanner() {
    if (document.getElementById("pages-demo-banner")) return;
    var b = document.createElement("div");
    b.id = "pages-demo-banner";
    b.setAttribute("role", "status");
    b.innerHTML =
      "<strong>Demo Pages</strong> · cáscara cívica con datos mock · sin nodo Go · " +
      "<span>ruta <code>/red/demo/</code></span>";
    document.body.insertBefore(b, document.body.firstChild);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ensureBanner);
  } else {
    ensureBanner();
  }

  var _fetch = window.fetch.bind(window);
  window.fetch = function (input, init) {
    var url = typeof input === "string" ? input : (input && input.url) || "";
    var method = (init && init.method) || (input && input.method) || "GET";
    var path = pathnameOf(url);
    if (path.indexOf("/api/") === 0) {
      var mocked = handleApi(path, method, url);
      if (mocked) return Promise.resolve(mocked);
    }
    return _fetch(input, init);
  };

  window.__RCV_PAGES_DEMO__ = {
    base: DEMO_BASE,
    places: PLACES,
    version: DEMO_VERSION,
  };
})();
