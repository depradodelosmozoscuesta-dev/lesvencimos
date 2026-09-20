(() => {
  "use strict";

  /* ============================================================================
   * app.js — PWA Red Ciudadano Valladolid (UI española).
   *
   * Módulos lógicos en este archivo (un solo bundle embebido):
   *   1) Núcleo cívico / Calles: mapa esquemático, HUD día-noche/clima/bici,
   *      capas (paradas, bancos, sellos, misiones cívicas), ruta/cerca, casa,
   *      chat, prensa, federación. No depende de VitaInk.
   *   2) VitaInk (opcional): se activa solo si GET /api/vitaink/estado responde
   *      y el usuario enciende la capa. Personaje, sedes, tesoros, ranking,
   *      PNJ (Ángel/El Diablo/Hada/Gnomo/Duende/Sabio/Satán), panel Dios (PIN operador), crónica,
   *      maestros (roles, maestrías, lecciones, diario, prueba, reliquias, sínodo, voto, ermita, rito, peregrinación, códice).
   * Por qué un solo app.js: PWA offline embebida con go:embed; sin bundler.
   * Frontera: si el nodo se compiló con -tags novitaink, las rutas de juego
   * dan 404 y esta UI oculta chips VitaInk (red ciudadana pura).
   * ============================================================================ */

  const $ = (sel) => document.querySelector(sel);
  const placesGrid = $("#places-grid");
  const mapPins = $("#map-pins");
  const civicMap = $("#civic-map");
  const cityStreets = $("#city-streets");
  const streetsSvg = $("#streets-svg");
  const streetBuildings = $("#street-buildings");
  const playerAvatar = $("#player-avatar");
  const streetLabel = $("#street-label");
  const streetNameChip = $("#street-name-chip");
  const dpad = $("#dpad");
  const homeHint = $("#home-hint");
  const search = $("#search");
  const empty = $("#empty");
  const viewHome = $("#view-home");
  const onboarding = $("#onboarding");
  const ONBOARDING_KEY = "rcv_onboarding_v13_done";
  let homeViewMode = "calles"; // calles | mapa | lista
  const viewPlace = $("#view-place");
  const viewMessages = $("#view-messages");
  const viewThread = $("#view-thread");
  const viewFiles = $("#view-files");
  const viewEnvios = $("#view-envios");
  const viewFederacion = $("#view-federacion");
  const viewNodo = $("#view-nodo");
  const viewNovedades = $("#view-novedades");
  const viewSellos = $("#view-sellos");
  const viewMisiones = $("#view-misiones");
  const viewCasa = $("#view-casa");
  const viewPucela = $("#view-pucela");
  const viewToolFrame = $("#view-tool-frame");
  const viewToolWiki = $("#view-tool-wiki");
  const viewTool3d = $("#view-tool-3d");
  const viewToolAsistente = $("#view-tool-asistente");
  const viewShop = $("#view-shop");
  const viewPersona = $("#view-persona");
  const viewPrensa = $("#view-prensa");
  const btnBack = $("#btn-back");
  const title = $("#title");
  const subtitle = $("#subtitle");
  const statusEl = $("#status");
  const statusText = $("#status-text");
  const mainNav = $("#main-nav");
  const threadsList = $("#threads-list");
  const threadsEmpty = $("#threads-empty");
  const threadMessages = $("#thread-messages");
  const compose = $("#compose");
  const composeBody = $("#compose-body");

  let placesCache = [];
  let currentPlace = null;
  let me = { user_id: "", node_id: "" };
  let currentPeer = null;
  let pollTimer = null;
  let privacyCountdown = null;
  let lastPresence = null;
  let toolReturnPlace = null;
  let currentShop = null;
  let currentPersona = null;
  let currentEdition = null;
  let hojaIndex = 0;
  let asistenteAskURL = "/api/herramientas/asistente/ask";
  let asistenteFAQURL = "/api/herramientas/asistente/faq";
  let asistenteReturn = null;
  let currentMostradorTicket = null;
  let currentMostradorPlace = null;
  let currentTallerProyectoId = null;
  let currentTallerRemoto = null; // { origin_node_id, proyecto_id, title, ... }
  let currentTallerRemotoCompleteId = null;
  let currentTallerRemotoJobId = null;
  let mostradorCatalog = [];

  function setStatus(msg, kind) {
    statusText.textContent = msg;
    statusEl.classList.remove("ok", "err");
    if (kind) statusEl.classList.add(kind);
  }

  async function fetchJSON(url, opts) {
    const res = await fetch(url, {
      headers: { Accept: "application/json", ...(opts && opts.body ? { "Content-Type": "application/json" } : {}) },
      ...opts,
    });
    if (!res.ok) {
      let detail = "HTTP " + res.status;
      try {
        const j = await res.json();
        if (j.error) detail = j.error;
      } catch (_) {}
      throw new Error(detail);
    }
    return res.json();
  }

  function categoryLabel(cat) {
    const map = {
      administracion: "Administración",
      salud: "Salud",
      cultura: "Cultura",
      comercio: "Comercio",
      medios: "Medios",
      educacion: "Educación",
      seguridad: "Seguridad",
      vivienda: "Vivienda",
      comunicacion: "Comunicación",
      religion: "Religión",
      servicios: "Servicios",
      transporte: "Transporte",
      ocio: "Ocio",
      deporte: "Deporte",
      herramientas: "Herramientas",
      comunidad: "Comunidad",
      red: "Red",
    };
    return map[cat] || cat;
  }

  function zoneLabel(z) {
    const map = {
      centro: "Centro",
      norte: "Norte",
      sur: "Sur",
      este: "Este",
      oeste: "Oeste",
      red: "Red",
    };
    return map[z] || z || "";
  }

  function fmtCountdown(sec) {
    if (!sec || sec <= 0) return "caducada";
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    if (m >= 60) return Math.floor(m / 60) + " h " + (m % 60) + " min";
    if (m > 0) return m + " min " + s + " s";
    return s + " s";
  }

  function reachBadge(q, label) {
    const cls = "reach-badge reach-" + (q || "desconocida");
    return '<span class="' + cls + '">' + escapeHTML(label || q || "desconocida") + "</span>";
  }

  function privacyEls(prefix) {
    return {
      status: $(prefix + "-status"),
      modes: $(prefix + "-modes"),
      zone: $(prefix + "-zone"),
      ttl: $(prefix + "-ttl"),
      ttlWrap: $(prefix + "-ttl-wrap"),
      rotate: $(prefix + "-rotate") || $("#btn-privacy-rotate"),
      fb: $(prefix + "-feedback"),
    };
  }

  function renderPrivacyInto(prefix, view) {
    const els = privacyEls(prefix);
    lastPresence = view;
    if (els.zone && view.zone_pref !== undefined) {
      els.zone.value = view.zone_pref || "";
    }
    if (els.ttl && view.precisa_ttl_sec) {
      els.ttl.value = String(view.precisa_ttl_sec);
    }
    if (els.ttlWrap) {
      els.ttlWrap.classList.toggle("hidden", view.mode !== "precisa_temporal");
    }
    let status = "Modo: " + (view.mode_label || view.mode);
    if (view.zone_hint) status += " · zona " + view.zone_hint;
    if (view.barrio) status += " · barrio " + view.barrio;
    if (view.mode === "precisa_temporal" && view.tip && view.tip_expires_in > 0) {
      status += " · pista precisa: " + fmtCountdown(view.tip_expires_in);
    } else if (view.is_expired) {
      status += " · pista caducada → " + (view.fallback || "aproximada");
    }
    if (els.status) {
      els.status.textContent = status;
      els.status.classList.toggle("expired", !!view.is_expired);
    }
    if (els.modes) {
      const modes = view.modes || [];
      els.modes.innerHTML = "";
      for (const m of modes) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "privacy-mode" + (m.id === view.mode ? " active" : "");
        btn.setAttribute("role", "radio");
        btn.setAttribute("aria-checked", m.id === view.mode ? "true" : "false");
        btn.dataset.mode = m.id;
        btn.innerHTML = "<strong>" + escapeHTML(m.label) + "</strong><span>" + escapeHTML(m.summary) + "</span>";
        btn.addEventListener("click", () => savePresence(m.id, prefix));
        els.modes.appendChild(btn);
      }
    }
  }

  function startPrivacyCountdown() {
    if (privacyCountdown) clearInterval(privacyCountdown);
    privacyCountdown = setInterval(() => {
      if (!lastPresence || lastPresence.mode !== "precisa_temporal") return;
      if (typeof lastPresence.tip_expires_in === "number" && lastPresence.tip_expires_in > 0) {
        lastPresence.tip_expires_in -= 1;
        renderPrivacyInto("#privacy", lastPresence);
        if ($("#casa-privacy-status")) renderPrivacyInto("#casa-privacy", lastPresence);
      }
    }, 1000);
  }

  async function loadPresence() {
    const view = await fetchJSON("/api/chat/presence");
    renderPrivacyInto("#privacy", view);
    if ($("#casa-privacy-status")) renderPrivacyInto("#casa-privacy", view);
    startPrivacyCountdown();
    return view;
  }

  async function savePresence(mode, prefix) {
    const els = privacyEls(prefix || "#privacy");
    const body = {
      mode: mode || (lastPresence && lastPresence.mode) || "aproximada",
      zone_pref: els.zone ? els.zone.value : "",
      precisa_ttl_sec: els.ttl ? parseInt(els.ttl.value, 10) : 1800,
    };
    try {
      const data = await fetchJSON("/api/chat/presence", {
        method: "POST",
        body: JSON.stringify(body),
      });
      const view = data.presence || data;
      renderPrivacyInto("#privacy", view);
      if ($("#casa-privacy-status")) renderPrivacyInto("#casa-privacy", view);
      if (els.fb) els.fb.textContent = "Modo guardado: " + (view.mode_label || view.mode);
      setStatus("Privacidad: " + (view.mode_label || view.mode), "ok");
    } catch (e) {
      if (els.fb) els.fb.textContent = "Error: " + e.message;
      setStatus("Privacidad: " + e.message, "err");
    }
  }

  async function rotatePresence(prefix) {
    const els = privacyEls(prefix || "#privacy");
    try {
      const data = await fetchJSON("/api/chat/presence/rotate", { method: "POST", body: "{}" });
      const view = data.presence || data;
      renderPrivacyInto("#privacy", view);
      if ($("#casa-privacy-status")) renderPrivacyInto("#casa-privacy", view);
      if (els.fb) els.fb.textContent = "Pista de chat rotada.";
      setStatus("Pista de chat rotada", "ok");
    } catch (e) {
      if (els.fb) els.fb.textContent = "Error: " + e.message;
    }
  }

  async function loadContacts() {
    const box = $("#contacts-list");
    const emptyEl = $("#contacts-empty");
    if (!box) return;
    const data = await fetchJSON("/api/contacts");
    const list = data.contacts || [];
    box.innerHTML = "";
    if (!list.length) {
      if (emptyEl) emptyEl.classList.remove("hidden");
      return;
    }
    if (emptyEl) emptyEl.classList.add("hidden");
    for (const c of list) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "thread-card";
      btn.setAttribute("role", "listitem");
      const name = c.display_name || shortId(c.user_id);
      const zone = c.last_zone ? " · " + zoneLabel(c.last_zone) : "";
      btn.innerHTML =
        "<strong>" + escapeHTML(name) + reachBadge(c.reach_quality, c.reach_label) + "</strong>" +
        '<span class="preview muted">' + escapeHTML((c.last_mode || "—") + zone) + "</span>";
      btn.addEventListener("click", () => openThread(c.user_id, name));
      box.appendChild(btn);
    }
  }

  function escapeHTML(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function shortId(id) {
    if (!id) return "";
    return id.length > 10 ? id.slice(0, 8) + "…" : id;
  }

  function hideAllViews() {
    viewHome.classList.add("hidden");
    viewPlace.classList.add("hidden");
    viewMessages.classList.add("hidden");
    viewThread.classList.add("hidden");
    viewFiles.classList.add("hidden");
    if (viewEnvios) viewEnvios.classList.add("hidden");
    if (viewFederacion) viewFederacion.classList.add("hidden");
    if (viewNodo) viewNodo.classList.add("hidden");
    if (viewNovedades) viewNovedades.classList.add("hidden");
    if (viewSellos) viewSellos.classList.add("hidden");
    if (viewMisiones) viewMisiones.classList.add("hidden");
    if (viewCasa) viewCasa.classList.add("hidden");
    if (viewPucela) viewPucela.classList.add("hidden");
    if (viewToolFrame) viewToolFrame.classList.add("hidden");
    if (viewToolWiki) viewToolWiki.classList.add("hidden");
    if (viewTool3d) viewTool3d.classList.add("hidden");
    if (viewToolAsistente) viewToolAsistente.classList.add("hidden");
    if (viewShop) viewShop.classList.add("hidden");
    if (viewPersona) viewPersona.classList.add("hidden");
    if (viewPrensa) viewPrensa.classList.add("hidden");
  }

  function setNav(name) {
    document.querySelectorAll(".nav-btn").forEach((b) => {
      b.classList.toggle("active", b.dataset.nav === name);
    });
    mainNav.classList.toggle("hidden", name === "thread" || name === "place" || name === "tool" || name === "shop" || name === "persona" || name === "prensa");
  }

  function setHomeViewMode(mode) {
    if (mode === "lista") homeViewMode = "lista";
    else if (mode === "mapa") homeViewMode = "mapa";
    else homeViewMode = "calles";
    const btnCalles = $("#btn-view-calles");
    const btnMapa = $("#btn-view-mapa");
    const btnLista = $("#btn-view-lista");
    if (btnCalles) btnCalles.classList.toggle("active", homeViewMode === "calles");
    if (btnMapa) btnMapa.classList.toggle("active", homeViewMode === "mapa");
    if (btnLista) btnLista.classList.toggle("active", homeViewMode === "lista");
    if (cityStreets) cityStreets.classList.toggle("hidden", homeViewMode !== "calles");
    if (civicMap) civicMap.classList.toggle("hidden", homeViewMode !== "mapa");
    if (placesGrid) placesGrid.classList.toggle("hidden", homeViewMode !== "lista");
    if (homeHint) {
      homeHint.textContent =
        homeViewMode === "calles"
          ? "Calles · camina y entra · sin URLs"
          : homeViewMode === "mapa"
            ? "Mapa cívico · toca un lugar · sin URLs"
            : "Lista · toca un lugar · sin URLs";
    }
    if (homeViewMode === "calles") {
      ensureCitymap().then(() => {
        renderStreetBuildings(placesCache.length ? placesCache : placesCacheFull);
        startStreetLoop();
      }).catch(() => {});
    } else {
      stopStreetLoop();
    }
    try {
      localStorage.setItem("rcv_home_view_v24", homeViewMode);
    } catch (_) {}
  }


  /* —— v2.4 city streets game —— */
  let citymapCache = null;
  let citymapPromise = null;
  let playerX = 50;
  let playerY = 46;
  let playerVX = 0;
  let playerVY = 0;
  let keysDown = Object.create(null);
  let streetRAF = 0;
  let lastStreetTS = 0;
  let nearPlaceId = null;
  let enterCooldown = 0;
  let streetSegments = []; // {x1,y1,x2,y2,name,from,to}
  let placeNodes = []; // {id,place_id,x,y,label,emoji}
  const WALK_SPEED = 22; // % per second (v2.6 mirrors cityfeatures.WalkSpeed)
  const BIKE_SPEED = 40; // faster along streets; still stay-on-street
  const SNAP_MAX = 2.8; // max snap distance when moving
  const BIKE_LS_KEY = "rcv_bike_v26";
  const VIGNETTE_SKIP_KEY = "rcv_vignette_skip_v26";
  const MISSION_BADGES_KEY = "rcv_mission_badges_v26";
  let bikeMode = false;

  /* —— Calles cívicas: vistas / ruta / capas / cerca (núcleo; sin VitaInk) ——
   * Capas cívicas (paradas, bancos, sellos, misiones) viven en cityfeatures.
   * VitaInk es interruptor aparte: OFF = PWA cívica pura; ON = overlay LARP.
   * —— v2.9 vistas / ruta / capas / cerca —— */
  const VISTA_LS_KEY = "rcv_vista_v29";
  const CAPAS_LS_KEY = "rcv_capas_v29";
  const ROUTE_FOLLOW_KEY = "rcv_route_follow_v29";
  let vistaMode = "planta"; // planta | inclinada | mirador
  let capasState = { paradas: true, bancos: true, sellos: true, misiones: true, clima: true, vitaink: false };
  const VITAINK_LS_KEY = "rcv_vitaink_v32";
  const VITAINK_PJ_LS_KEY = "rcv_vitaink_pj_v32";
  /* v5.1: zoom Calles + modo juego limpio (prefs locales) */
  const CALLES_ZOOM_LS_KEY = "rcv_calles_zoom_v51";
  const JUEGO_LIMPIO_LS_KEY = "rcv_juego_limpio_v51";
  const CALLES_ZOOM_MIN = 0.7;
  const CALLES_ZOOM_MAX = 2.2;
  const CALLES_ZOOM_STEP = 0.15;
  let callesZoom = 1;
  let callesFsFallback = false;
  let juegoLimpio = false;
  let vitainkOn = false;
  let vitainkAvailable = false; // plugin mounted (GET /api/vitaink/estado)
  let vitainkMapa = null; // { ownerships, factions, casas, tesoros, tint }
  let vitainkByPlace = Object.create(null);
  let vitainkCasas = [];
  let vitainkTesoros = [];
  let tesoroRadius = 4;
  let nearTesoroId = null;
  let botRadius = 9; // v4.2 proximidad a alma/marcador PNJ

  /* —— v5.5 Mari lote 2 (Dibujar Mari) en Calles / Maestros ——
     Qué: facing front/qleft/qright/top + cycle/ multi-frame + night + pins regenerados.
     Por qué: avatar jugable según rumbo/zoom/tod; fallback from-mari-gym → emoji. */
  /* —— v5.6 Modo naturalista (opt-in adulto) ——
     Convención de rutas (si existen): base/skin-01/{day|night}/{angle}/nudist|naturalist/{idle,walk-L,walk-R}.png
     y opcional cycle/; masters/{id}/nudist|naturalist/pin.png.
     Alternativa solo con toggle ON: from-mari-gym/sintop/{idle,walk-L,walk-R}.png
     o pose/frames/idle-sintop.png. Si falta el pack → vestida. Default OFF. */
  const MARI_BASE = "/vitaink/sprites/mari";
  /* Cuerpo vestido: skin-01 (ángulos completos). Naturalista: skin-01..04 según FaceRecipe. */
  const MARI_SKIN_DEFAULT = "skin-01";
  /* inventory faces.face_skin_align invertido: face-kit skin → base/{id} naturalista */
  const MARI_FACE_TO_BODY_SKIN = {
    "skin-02": "skin-01",
    "skin-05": "skin-02",
    "skin-07": "skin-03",
    "skin-08": "skin-04",
  };
  function mariBodySkinId() {
    const faceSkin = (mariFaceRecipe && mariFaceRecipe.skin) || "skin-04";
    let nat = false;
    try { nat = !!mariNaturalista; } catch (_) { nat = false; }
    if (nat) return MARI_FACE_TO_BODY_SKIN[faceSkin] || MARI_SKIN_DEFAULT;
    return MARI_SKIN_DEFAULT;
  }
  function mariSkinBase() {
    return MARI_BASE + "/base/" + mariBodySkinId();
  }
  /** @deprecated use mariSkinBase(); kept as getter-like for rare string concat */
  const MARI_SKIN = MARI_BASE + "/base/skin-01";
  const MARI_FALLBACK_IDLE = MARI_BASE + "/from-mari-gym/idle.png";
  const MARI_FALLBACK_WALK_L = MARI_BASE + "/from-mari-gym/marcha-L.png";
  const MARI_FALLBACK_WALK_R = MARI_BASE + "/from-mari-gym/marcha-R.png";
  const MARI_SINTOP_DIR = MARI_BASE + "/from-mari-gym/sintop";
  const MARI_SINTOP_POSE_IDLE = MARI_BASE + "/pose/frames/idle-sintop.png";


  /* —— v5.15 Rostros Mari lote1 + v5.16 cara en cuerpo + v5.17 body-shapes ——
     Qué: selector de capas shape/skin/eyes/brows/nose/mouth + canvas alpha.
     Por qué: receta JSON en personaje (regenerable); no PNG horneado.
     Pelo: select deshabilitado listo para lote futuro.
     v5.16: además, capas faces/on-body sobre el avatar Calles (front/top). */
  const MARI_FACES_BASE = MARI_BASE + "/faces";
  const MARI_FACES_CATALOG_URL = MARI_FACES_BASE + "/catalog.json";
  const MARI_FACES_FRONT = MARI_FACES_BASE + "/front";
  const MARI_FACE_KIT = "mari-faces-lote1";
  const MARI_FACE_DEFAULT = {
    kit: MARI_FACE_KIT,
    shape: "shape-01",
    skin: "skin-04",
    eyes: "eyes-brown-01",
    brows: "brows-01",
    nose: "nose-01",
    mouth: "mouth-smile-01",
  };
  let mariFaceCatalog = null;
  let mariFaceRecipe = Object.assign({}, MARI_FACE_DEFAULT);
  let mariFaceImgCache = Object.create(null);
  let mariFaceComposeBusy = false;
  let mariFaceComposeQueued = false;

  /* —— v5.17 Siluetas body-shapes (pecho × cadera-muslos) ——
     Qué: BodyRecipe bust-01…06 × hips-01…06; idle front vestido 512×768
     (compatible on-body) y naturalista 1280×720 (sin on-body).
     Por qué: variedad de silueta sin hornear PNG; receta en personaje.json.
     Limitaciones: walk/cycle/night/q* siguen en base/; top solo clothed. */
  const MARI_BODY_BASE = MARI_BASE + "/body-shapes";
  const MARI_BODY_CATALOG_URL = MARI_BODY_BASE + "/catalog.json";
  const MARI_BODY_KIT = "mari-body-shapes";
  const MARI_BODY_DEFAULT = {
    kit: MARI_BODY_KIT,
    bust: "bust-03",
    hips: "hips-03",
  };
  const MARI_BODY_BUST_IDS = ["bust-01","bust-02","bust-03","bust-04","bust-05","bust-06"];
  const MARI_BODY_HIPS_IDS = ["hips-01","hips-02","hips-03","hips-04","hips-05","hips-06"];
  const MARI_BODY_BUST_LABELS = {
    "bust-01": "plano", "bust-02": "suave", "bust-03": "medio",
    "bust-04": "lleno", "bust-05": "pleno", "bust-06": "muy pleno",
  };
  const MARI_BODY_HIPS_LABELS = {
    "hips-01": "fino", "hips-02": "delgado", "hips-03": "medio",
    "hips-04": "ancho", "hips-05": "ancho+", "hips-06": "muy ancho",
  };
  let mariBodyCatalog = null;
  let mariBodyRecipe = Object.assign({}, MARI_BODY_DEFAULT);

  function mariBodyShapesSkinId() {
    // Piel de silueta alineada al kit facial (inventory face_skin_align invertido).
    const faceSkin = (mariFaceRecipe && mariFaceRecipe.skin) || "skin-04";
    return MARI_FACE_TO_BODY_SKIN[faceSkin] || MARI_SKIN_DEFAULT;
  }
  function mariBodyShapesIdleURL(facing) {
    const r = mariBodyRecipe || MARI_BODY_DEFAULT;
    const bust = r.bust || MARI_BODY_DEFAULT.bust;
    const hips = r.hips || MARI_BODY_DEFAULT.hips;
    if (!bust || !hips) return "";
    try {
      if (typeof encarnarMaestroIdActivo === "function" && encarnarMaestroIdActivo()) return "";
    } catch (_) {}
    if (mariUseGymFallback) return "";
    try {
      if (typeof mariSintopActive === "function" && mariSintopActive()) return "";
    } catch (_) {}
    const dir = typeof mariDirFolder === "function"
      ? mariDirFolder(facing || (typeof mariFacingAngle === "function" ? mariFacingAngle() : "front"))
      : (facing || "front");
    const bodySkin = mariBodyShapesSkinId();
    // Naturalista → nudist leaf body-shapes aunque falte el pack base/…
    let useNudist = false;
    try { useNudist = !!mariNaturalista; } catch (_) { useNudist = false; }
    const outfit = useNudist ? "nudist" : "clothed";
    if (dir === "top") {
      if (useNudist) return ""; // sin top naturalista en pack
      return MARI_BODY_BASE + "/top/clothed/idle/" + bust + "__" + hips + ".png";
    }
    if (dir !== "front") return "";
    // Night front: sin warps night en body-shapes → no forzar
    try {
      if (typeof mariIsNight === "function" && mariIsNight()) return "";
    } catch (_) {}
    let folder = outfit + "/idle";
    if (bodySkin && bodySkin !== "skin-01") folder = outfit + "/idle-" + bodySkin;
    return MARI_BODY_BASE + "/front/" + folder + "/" + bust + "__" + hips + ".png";
  }
  function readMariBodyRecipeFromUI() {
    const g = (id) => (($("#" + id) && $("#" + id).value) || "").trim();
    return {
      kit: MARI_BODY_KIT,
      bust: g("vitaink-body-bust") || MARI_BODY_DEFAULT.bust,
      hips: g("vitaink-body-hips") || MARI_BODY_DEFAULT.hips,
    };
  }
  function applyMariBodyRecipeToUI(recipe) {
    const r = Object.assign({}, MARI_BODY_DEFAULT, recipe || {});
    mariBodyRecipe = r;
    const map = {
      "vitaink-body-bust": r.bust,
      "vitaink-body-hips": r.hips,
    };
    for (const [id, val] of Object.entries(map)) {
      const el = $("#" + id);
      if (el && val) el.value = val;
    }
  }
  async function ensureMariBodyCatalog() {
    if (mariBodyCatalog && mariBodyCatalog._wired) return mariBodyCatalog;
    if (!mariBodyCatalog) {
      try {
        const res = await fetch(MARI_BODY_CATALOG_URL, { headers: { Accept: "application/json" } });
        if (!res.ok) throw new Error("body catalog " + res.status);
        mariBodyCatalog = await res.json();
      } catch (_) {
        mariBodyCatalog = {
          version: "1.0.0-body-shapes",
          combinations: 36,
          axes: {
            bust: MARI_BODY_BUST_IDS.map((id) => ({ id, label: MARI_BODY_BUST_LABELS[id] })),
            hips: MARI_BODY_HIPS_IDS.map((id) => ({ id, label: MARI_BODY_HIPS_LABELS[id] })),
          },
        };
      }
    }
    const axes = mariBodyCatalog.axes || {};
    const busts = (axes.bust || []).map((b) => (typeof b === "string" ? b : b.id));
    const hips = (axes.hips || []).map((h) => (typeof h === "string" ? h : h.id));
    const bustLabels = Object.assign({}, MARI_BODY_BUST_LABELS);
    const hipsLabels = Object.assign({}, MARI_BODY_HIPS_LABELS);
    for (const b of (axes.bust || [])) {
      if (b && typeof b === "object") bustLabels[b.id] = b.label || b.id;
    }
    for (const h of (axes.hips || [])) {
      if (h && typeof h === "object") hipsLabels[h.id] = h.label || h.id;
    }
    fillMariFaceSelect($("#vitaink-body-bust"), busts.length ? busts : MARI_BODY_BUST_IDS, bustLabels);
    fillMariFaceSelect($("#vitaink-body-hips"), hips.length ? hips : MARI_BODY_HIPS_IDS, hipsLabels);
    applyMariBodyRecipeToUI(mariBodyRecipe);
    mariBodyCatalog._wired = true;
    return mariBodyCatalog;
  }
  function wireMariBodyControls() {
    const ids = ["vitaink-body-bust", "vitaink-body-hips"];
    for (const id of ids) {
      const el = $("#" + id);
      if (!el || el.dataset.bodyWired) continue;
      el.dataset.bodyWired = "1";
      el.addEventListener("change", () => {
        mariBodyRecipe = readMariBodyRecipeFromUI();
        refreshMariFacePreviews().catch(() => {});
        // Forzar idle Calles con la nueva silueta
        const img = $("#player-mari");
        if (img) {
          img.dataset.frame = "";
          img.dataset.facing = "";
        }
        if (typeof applyPlayerAvatarLook === "function") applyPlayerAvatarLook();
      });
    }
  }


  function mariFaceLabel(id) {
    if (!id) return "—";
    return String(id).replace(/^(shape|skin|eyes|brows|nose|mouth)-/, "").replace(/-/g, " ");
  }
  function mariFaceSkinnedURL(shape, skin) {
    return MARI_FACES_FRONT + "/shape_skinned/" + shape + "__" + skin + ".png";
  }
  function mariFacePartURL(kind, id) {
    return MARI_FACES_FRONT + "/" + kind + "/" + id + ".png";
  }
  function mariFaceLayerURLs(recipe) {
    const r = recipe || mariFaceRecipe;
    return [
      mariFaceSkinnedURL(r.shape, r.skin),
      mariFacePartURL("brows", r.brows),
      mariFacePartURL("eyes", r.eyes),
      mariFacePartURL("nose", r.nose),
      mariFacePartURL("mouth", r.mouth),
    ];
  }
  function loadMariFaceImage(url) {
    if (url in mariFaceImgCache) {
      const hit = mariFaceImgCache[url];
      return hit ? Promise.resolve(hit) : Promise.reject(new Error("face img fail"));
    }
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.decoding = "async";
      img.onload = () => { mariFaceImgCache[url] = img; resolve(img); };
      img.onerror = () => { mariFaceImgCache[url] = null; reject(new Error("face img fail")); };
      img.src = url;
    });
  }

  /** Vista previa Personaje: cuerpo idle 512×768 + capas on-body (si vestida). */
  async function composeMariBodyFacePreview(canvas, faceRecipe, bodyRecipe) {
    if (!canvas || !canvas.getContext) return false;
    const body = Object.assign({}, MARI_BODY_DEFAULT, bodyRecipe || mariBodyRecipe || {});
    const face = faceRecipe || mariFaceRecipe;
    const naturalista = !!(typeof mariNaturalista !== "undefined" && mariNaturalista);
    // Naturalista body-shapes es 1280×720 → preview solo silueta, sin on-body.
    if (naturalista) {
      canvas.width = 512;
      canvas.height = 288;
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      try {
        const skin = mariBodyShapesSkinId();
        let folder = "nudist/idle";
        if (skin && skin !== "skin-01") folder = "nudist/idle-" + skin;
        const url = MARI_BODY_BASE + "/front/" + folder + "/" + body.bust + "__" + body.hips + ".png";
        const img = await loadMariFaceImage(url);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        return true;
      } catch (_) {
        return composeMariFaceOnto(canvas, face);
      }
    }
    canvas.width = 512;
    canvas.height = 768;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, 512, 768);
    try {
      const skin = mariBodyShapesSkinId();
      let folder = "clothed/idle";
      if (skin && skin !== "skin-01") folder = "clothed/idle-" + skin;
      const bodyURL = MARI_BODY_BASE + "/front/" + folder + "/" + body.bust + "__" + body.hips + ".png";
      const bodyImg = await loadMariFaceImage(bodyURL);
      ctx.drawImage(bodyImg, 0, 0, 512, 768);
      try {
        const layers = mariFaceOnBodyLayerURLs(face, "front");
        const imgs = await Promise.all(layers.map((u) => loadMariFaceImage(u)));
        for (const img of imgs) ctx.drawImage(img, 0, 0, 512, 768);
      } catch (_) { /* sin pack on-body: solo cuerpo */ }
      return true;
    } catch (_) {
      canvas.width = 512;
      canvas.height = 512;
      return composeMariFaceOnto(canvas, face);
    }
  }

  async function composeMariFaceOnto(canvas, recipe) {
    if (!canvas || !canvas.getContext) return false;
    const ctx = canvas.getContext("2d");
    const w = canvas.width || 512;
    const h = canvas.height || 512;
    ctx.clearRect(0, 0, w, h);
    try {
      const imgs = await Promise.all(mariFaceLayerURLs(recipe).map((u) => loadMariFaceImage(u)));
      for (const img of imgs) ctx.drawImage(img, 0, 0, w, h);
      return true;
    } catch (_) {
      try {
        const sample = await loadMariFaceImage(MARI_FACES_FRONT + "/_previews/sample-01.png");
        ctx.drawImage(sample, 0, 0, w, h);
      } catch (__) {
        ctx.fillStyle = "#fed7aa";
        ctx.beginPath();
        ctx.arc(w / 2, h / 2, Math.min(w, h) * 0.42, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#9a3412";
        ctx.font = Math.floor(w / 12) + "px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("rostro", w / 2, h / 2);
      }
      return false;
    }
  }
  async function refreshMariFacePreviews() {
    if (mariFaceComposeBusy) {
      mariFaceComposeQueued = true;
      return;
    }
    mariFaceComposeBusy = true;
    try {
      const main = $("#vitaink-face-canvas");
      const puppet = $("#vitaink-puppet-face");
      const badge = $("#player-face-badge");
      if (main) await composeMariBodyFacePreview(main, mariFaceRecipe, mariBodyRecipe);
      if (puppet) await composeMariFaceOnto(puppet, mariFaceRecipe);
      if (badge) {
        const ok = await composeMariFaceOnto(badge, mariFaceRecipe);
        const show = !!(ok && typeof mariAvatarEnabled === "function" && mariAvatarEnabled()
          && mariFaceRecipe && mariFaceRecipe.shape
          && typeof encarnarMaestroIdActivo === "function" && !encarnarMaestroIdActivo());
        badge.classList.toggle("hidden", !show);
      }
      // v5.16: cara compuesta también sobre el cuerpo en Calles
      if (typeof syncMariFaceOnBodyAvatar === "function") {
        await syncMariFaceOnBodyAvatar();
      }
      const combo = $("#vitaink-face-combo");
      if (combo) {
        const n = (mariFaceCatalog && (mariFaceCatalog.combinations || mariFaceCatalog.combos)) || 24576;
        const b = (mariBodyCatalog && (mariBodyCatalog.combinations || mariBodyCatalog.combos)) || 36;
        combo.textContent = Number(n).toLocaleString("es-ES") + " rostros · " + Number(b) + " siluetas · body-shapes";
      }
    } finally {
      mariFaceComposeBusy = false;
      if (mariFaceComposeQueued) {
        mariFaceComposeQueued = false;
        refreshMariFacePreviews().catch(() => {});
      }
    }
  }
  function readMariFaceRecipeFromUI() {
    const g = (id) => (($("#" + id) && $("#" + id).value) || "").trim();
    return {
      kit: MARI_FACE_KIT,
      shape: g("vitaink-face-shape") || MARI_FACE_DEFAULT.shape,
      skin: g("vitaink-face-skin") || MARI_FACE_DEFAULT.skin,
      eyes: g("vitaink-face-eyes") || MARI_FACE_DEFAULT.eyes,
      brows: g("vitaink-face-brows") || MARI_FACE_DEFAULT.brows,
      nose: g("vitaink-face-nose") || MARI_FACE_DEFAULT.nose,
      mouth: g("vitaink-face-mouth") || MARI_FACE_DEFAULT.mouth,
    };
  }
  function applyMariFaceRecipeToUI(recipe) {
    const r = Object.assign({}, MARI_FACE_DEFAULT, recipe || {});
    mariFaceRecipe = r;
    const map = {
      "vitaink-face-shape": r.shape,
      "vitaink-face-skin": r.skin,
      "vitaink-face-eyes": r.eyes,
      "vitaink-face-brows": r.brows,
      "vitaink-face-nose": r.nose,
      "vitaink-face-mouth": r.mouth,
    };
    for (const [id, val] of Object.entries(map)) {
      const el = $("#" + id);
      if (el && val) el.value = val;
    }
  }
  function fillMariFaceSelect(sel, ids, labels) {
    if (!sel) return;
    const cur = sel.value;
    sel.innerHTML = "";
    for (const id of ids) {
      const opt = document.createElement("option");
      opt.value = id;
      opt.textContent = (labels && labels[id]) || mariFaceLabel(id);
      sel.appendChild(opt);
    }
    if (cur && ids.indexOf(cur) >= 0) sel.value = cur;
  }
  async function ensureMariFaceCatalog() {
    if (mariFaceCatalog && mariFaceCatalog._wired) return mariFaceCatalog;
    if (!mariFaceCatalog) {
      try {
        const res = await fetch(MARI_FACES_CATALOG_URL, { headers: { Accept: "application/json" } });
        if (!res.ok) throw new Error("catalog " + res.status);
        mariFaceCatalog = await res.json();
      } catch (_) {
        mariFaceCatalog = {
          version: "1.0.0-faces-lote1",
          combinations: 24576,
          parts: {
            shape: ["shape-01","shape-02","shape-03","shape-04","shape-05","shape-06","shape-07","shape-08"],
            skin: [
              {id:"skin-01",label:"muy clara rosa"},{id:"skin-02",label:"clara"},{id:"skin-03",label:"clara-media"},
              {id:"skin-04",label:"media clara"},{id:"skin-05",label:"oliva"},{id:"skin-06",label:"bronce"},
              {id:"skin-07",label:"mora"},{id:"skin-08",label:"profunda"}
            ],
            eyes: ["eyes-blue-01","eyes-brown-01","eyes-dark-01","eyes-green-01","eyes-grey-01","eyes-hazel-01"],
            brows: ["brows-01","brows-02","brows-03","brows-04"],
            nose: ["nose-01","nose-02","nose-03","nose-04"],
            mouth: ["mouth-neutral-01","mouth-neutral-02","mouth-smile-01","mouth-smile-02"],
          },
        };
      }
    }
    const parts = mariFaceCatalog.parts || {};
    const shapes = parts.shape || [];
    const skins = (parts.skin || []).map((s) => (typeof s === "string" ? s : s.id));
    const skinLabels = {};
    for (const s of (parts.skin || [])) {
      if (s && typeof s === "object") skinLabels[s.id] = s.label || s.id;
    }
    fillMariFaceSelect($("#vitaink-face-shape"), shapes);
    fillMariFaceSelect($("#vitaink-face-skin"), skins, skinLabels);
    fillMariFaceSelect($("#vitaink-face-eyes"), parts.eyes || []);
    fillMariFaceSelect($("#vitaink-face-brows"), parts.brows || []);
    fillMariFaceSelect($("#vitaink-face-nose"), parts.nose || []);
    fillMariFaceSelect($("#vitaink-face-mouth"), parts.mouth || []);
    applyMariFaceRecipeToUI(mariFaceRecipe);
    mariFaceCatalog._wired = true;
    return mariFaceCatalog;
  }
  function wireMariFaceControls() {
    const ids = [
      "vitaink-face-shape","vitaink-face-skin","vitaink-face-eyes",
      "vitaink-face-brows","vitaink-face-nose","vitaink-face-mouth"
    ];
    for (const id of ids) {
      const el = $("#" + id);
      if (!el || el.dataset.faceWired) continue;
      el.dataset.faceWired = "1";
      el.addEventListener("change", () => {
        const prevSkin = mariFaceRecipe && mariFaceRecipe.skin;
        mariFaceRecipe = readMariFaceRecipeFromUI();
        refreshMariFacePreviews().catch(() => {});
        // Naturalista multi-skin: si cambia la piel del kit, re-probe base/skin-XX/nudist
        if (id === "vitaink-face-skin" && mariFaceRecipe.skin !== prevSkin) {
          const img = $("#player-mari");
          if (img) { img.dataset.frame = ""; img.dataset.facing = ""; }
          if (typeof applyPlayerAvatarLook === "function") applyPlayerAvatarLook();
          if (mariNaturalista && typeof refreshMariNaturalistaPack === "function") {
            refreshMariNaturalistaPack().catch(() => {});
          }
        }
      });
    }
  }

  /* —— v5.16 Cara en cuerpo avatar (Calles) ——
     Pack Dibujar Mari: faces/on-body/front (512×768) y top (1280×720).
     Orden front: face_cover → shape_skinned → brows → eyes → nose → mouth.
     Anclas documentadas (ES) — catalog 1.1.0-on-body / placement.json:
       front: scale 0.4, dest (153, 42), neck_keep_frac 0.7 sobre cuerpo 512×768 (capas ya bakeadas).
       top:   corona shape_skinned sobre 1280×720 (placement top/).
     Compose: body frame → cover-soft → shape_skinned → brows → eyes → nose → mouth.
     Fallback CSS si falta el pack: slot cabeza idle ~ top 8% left 28% 44%×20%.
     Limitaciones: walk JPEG / cycle·night·nudist 1280×720 no alinean con front 512×768
     → on-body en day front (idle) + top day; naturalista oculta on-body; q* sin pack. */
  const MARI_ONBODY_FRONT = MARI_FACES_BASE + "/on-body/front";
  const MARI_ONBODY_TOP = MARI_FACES_BASE + "/on-body/top";
  const MARI_ONBODY_COVER = MARI_ONBODY_FRONT + "/face_cover/cover-soft.png";
  let mariOnBodyPackState = "unknown"; // unknown | ok | missing

  function mariFaceOnBodyMode() {
    if (typeof mariAvatarEnabled !== "function" || !mariAvatarEnabled()) return "";
    if (!mariFaceRecipe || !mariFaceRecipe.shape) return "";
    if (typeof encarnarMaestroIdActivo === "function" && encarnarMaestroIdActivo()) return "";
    if (mariUseGymFallback) return "";
    if (typeof mariSintopActive === "function" && mariSintopActive()) return "";
    // Naturalista (base o body-shapes nudist 1280×720) no alinea con on-body 512×768
    if (mariNaturalista) return "";
    // body-shapes clothed front sí es 512×768 → on-body compatible
    const facing = typeof mariFacingAngle === "function" ? mariFacingAngle() : "front";
    if (facing === "front" && typeof mariIsNight === "function" && !mariIsNight()) return "front";
    if (facing === "top" && typeof mariIsNight === "function" && !mariIsNight()) return "top";
    return "";
  }
  function mariFaceOnBodyLayerURLs(recipe, mode) {
    const r = recipe || mariFaceRecipe;
    if (mode === "top") {
      return [MARI_ONBODY_TOP + "/shape_skinned/" + r.shape + "__" + r.skin + ".png"];
    }
    // front (default)
    return [
      MARI_ONBODY_COVER,
      MARI_ONBODY_FRONT + "/shape_skinned/" + r.shape + "__" + r.skin + ".png",
      MARI_ONBODY_FRONT + "/brows/" + r.brows + ".png",
      MARI_ONBODY_FRONT + "/eyes/" + r.eyes + ".png",
      MARI_ONBODY_FRONT + "/nose/" + r.nose + ".png",
      MARI_ONBODY_FRONT + "/mouth/" + r.mouth + ".png",
    ];
  }
  async function composeMariFaceOnBodyOnto(canvas, recipe, mode) {
    if (!canvas || !canvas.getContext) return false;
    const tw = mode === "top" ? 1280 : 512;
    const th = mode === "top" ? 720 : 768;
    if (canvas.width !== tw || canvas.height !== th) {
      canvas.width = tw;
      canvas.height = th;
    }
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, tw, th);
    try {
      const imgs = await Promise.all(mariFaceOnBodyLayerURLs(recipe, mode).map((u) => loadMariFaceImage(u)));
      for (const img of imgs) ctx.drawImage(img, 0, 0, tw, th);
      mariOnBodyPackState = "ok";
      return true;
    } catch (_) {
      mariOnBodyPackState = "missing";
      return false;
    }
  }
  /** Fallback: pinta el kit 512×512 en el canvas y marca anclas CSS de cabeza. */
  async function composeMariFaceOnBodyFallback(canvas, recipe) {
    if (!canvas || !canvas.getContext) return false;
    canvas.width = 512;
    canvas.height = 512;
    const ok = await composeMariFaceOnto(canvas, recipe);
    canvas.classList.add("fallback-anchor");
    canvas.classList.remove("onbody-pack");
    return ok;
  }
  async function syncMariFaceOnBodyAvatar() {
    const canvas = $("#player-face-on-body");
    if (!canvas) return;
    const mode = mariFaceOnBodyMode();
    if (!mode) {
      canvas.classList.add("hidden");
      return;
    }
    canvas.classList.remove("fallback-anchor");
    canvas.classList.add("onbody-pack");
    let ok = false;
    try {
      ok = await composeMariFaceOnBodyOnto(canvas, mariFaceRecipe, mode);
    } catch (_) { ok = false; }
    if (!ok && mode === "front") {
      // Sin pack on-body: overlay CSS sobre slot cabeza del sprite idle.
      ok = await composeMariFaceOnBodyFallback(canvas, mariFaceRecipe);
    }
    canvas.classList.toggle("hidden", !ok);
  }

  const NATURALISTA_LS_KEY = "rcv_vitaink_naturalista_v56";
  const MARI_NUDIST_SUBDIRS = ["nudist", "naturalist"];
  /* Walk cycles (day only). Night uses idle/walk-L/R under night/{front,top}. */
  const MARI_CYCLE_WALK = {
    front: ["f0.png", "f1.png", "f2.png", "f3.png"],
    top: ["f1.png", "f2.png", "f3.png", "f4.png"],
    qleft: ["f1.png", "f2.png"],
    qright: ["f1.png", "f2.png"],
  };
  let mariSpritesOk = true;
  let mariUseGymFallback = false;
  let mariWalkPhase = 0;
  let mariLastStepAt = 0;
  let mariMoving = false;
  let mariFacingCached = "front";
  let mariNaturalista = false; // default OFF (clothed)
  /* off | probing | ok | sintop | sintop-pose | missing */
  let mariNudistPackState = "off";
  let mariNudistSubdir = ""; // nudist | naturalist
  let mariNudistHasCycle = false;
  let mariNudistCycleFront = null; // e.g. ["f0-idle.png","f1.png","f2.png","f3.png"] when pack uses that naming
  let mariNudistAngles = Object.create(null); // day dirs with idle.png under nudist/
  let mariMaestroNudistSubdir = ""; // optional pins variant
  /* Bot id (API) → carpeta masters/{…}. Plug packs Mari aquí cuando lleguen day/. */
  const MARI_MAESTRO_FOLDER = {
    angel: "angel", santo: "angel",
    demonio: "demon", diablo: "diablo", /* demonio→demon DISTINCT from diablo/ */
    hada: "fairy",
    gnomo: "gnome",
    duende: "goblin",
    sabio: "sage",
    satan: "satan",
  };
  const MARI_MAESTRO_FOLDER_FALLBACK = {}; /* diablo y demon son packs distintos; sin fallback cruzado */
  /* Registro de packs completos (misma forma para todos los maestros).
   * Qué: folder, bustPrefer, hasDay, cycleFront opcional.
   * Por qué: al entregar Mari masters/{id}/day/… se añade una entrada y Encarnar funciona. */
  const MARI_MAESTRO_PACKS = {
    diablo: {
      folder: "diablo",
      bustPrefer: "serio", // serio|front|smile
      hasDay: true,
      cycleFront: ["f0-idle.png", "f1.png", "f2.png", "f3.png", "f4.png"],
    },
    demonio: {
      folder: "demon",
      bustPrefer: "serio",
      hasDay: true,
      cycleFront: ["f0-idle.png", "f1.png", "f2.png"],
    },
    angel: {
      folder: "angel",
      bustPrefer: "smile",
      hasDay: true,
      cycleFront: ["f0-idle.png", "f1.png", "f2.png"],
    },
    hada: {
      folder: "fairy",
      fallback: "hada",
      bustPrefer: "smile",
      hasDay: true,
      cycleFront: ["f0-idle.png", "f1.png", "f2.png"],
    },
    gnomo: {
      folder: "gnome",
      bustPrefer: "smile",
      hasDay: true,
      cycleFront: ["f0-idle.png", "f1.png", "f2.png"],
    },
    duende: {
      folder: "goblin",
      fallback: "duende",
      bustPrefer: "smile",
      hasDay: true,
      cycleFront: ["f0-idle.png", "f1.png", "f2.png"],
    },
    sabio: {
      folder: "sage",
      bustPrefer: "smile",
      hasDay: true,
      cycleFront: ["f0-idle.png", "f1.png", "f2.png"],
    },
    satan: {
      folder: "satan",
      bustPrefer: "front",
      hasDay: true,
      cycleFront: ["f0-idle.png", "f1.png", "f2.png"],
    },
  };
  const MARI_MAESTRO_SMILE = {
    angel: true, santo: true, hada: true, sabio: true, gnomo: true, duende: true,
    demonio: false, diablo: false, satan: false,
  };
  const MARI_MAESTRO_TINT = {
    angel: "#2563eb", santo: "#2563eb", demonio: "#dc2626", diablo: "#b91c1c",
    hada: "#db2777", gnomo: "#16a34a", duende: "#ca8a04", sabio: "#7c3aed", satan: "#7f1d1d",
  };
  let mariMaestroFolderResolved = Object.create(null); // id → folder tras probe
  function maestroPack(mOrId) {
    const id = (typeof mOrId === "string") ? mOrId : ((mOrId && mOrId.id) ? String(mOrId.id) : "");
    const key = String(id || "").toLowerCase();
    const canon = (key === "santo") ? "angel" : key; // demonio es pack propio (demon/), no alias de diablo
    // Preferir meta del API (sprite_folder / bust_prefer / has_day_pack) si viene en el objeto
    if (mOrId && typeof mOrId === "object") {
      const folder = mOrId.sprite_folder || (MARI_MAESTRO_PACKS[canon] && MARI_MAESTRO_PACKS[canon].folder) || MARI_MAESTRO_FOLDER[key] || "";
      const bustPrefer = mOrId.bust_prefer || (MARI_MAESTRO_PACKS[canon] && MARI_MAESTRO_PACKS[canon].bustPrefer) || (MARI_MAESTRO_SMILE[key] === false ? "front" : "smile");
      const hasDay = !!(mOrId.has_day_pack || (MARI_MAESTRO_PACKS[canon] && MARI_MAESTRO_PACKS[canon].hasDay));
      const cycleFront = (MARI_MAESTRO_PACKS[canon] && MARI_MAESTRO_PACKS[canon].cycleFront) || null;
      const fallback = (MARI_MAESTRO_PACKS[canon] && MARI_MAESTRO_PACKS[canon].fallback) || MARI_MAESTRO_FOLDER_FALLBACK[canon] || "";
      return { id: canon, folder, bustPrefer, hasDay, cycleFront, fallback };
    }
    const pack = MARI_MAESTRO_PACKS[canon] || {};
    return {
      id: canon,
      folder: pack.folder || MARI_MAESTRO_FOLDER[key] || "",
      bustPrefer: pack.bustPrefer || "front",
      hasDay: !!pack.hasDay,
      cycleFront: pack.cycleFront || null,
      fallback: pack.fallback || MARI_MAESTRO_FOLDER_FALLBACK[canon] || "",
    };
  }
  function maestroFolder(mOrId) {
    const pack = maestroPack(mOrId);
    const key = pack.id;
    if (mariMaestroFolderResolved[key]) return mariMaestroFolderResolved[key];
    return pack.folder || "";
  }
  async function ensureMaestroSpriteFolder(mOrId) {
    const pack = maestroPack(mOrId);
    const key = pack.id;
    if (!pack.folder) return "";
    if (mariMaestroFolderResolved[key]) return mariMaestroFolderResolved[key];
    try {
      if (typeof mariUrlExists === "function") {
        if (await mariUrlExists(MARI_BASE + "/masters/" + pack.folder + "/pin.png")) {
          mariMaestroFolderResolved[key] = pack.folder;
        } else if (pack.fallback && await mariUrlExists(MARI_BASE + "/masters/" + pack.fallback + "/pin.png")) {
          mariMaestroFolderResolved[key] = pack.fallback;
        } else {
          mariMaestroFolderResolved[key] = pack.folder;
        }
      } else {
        mariMaestroFolderResolved[key] = pack.folder;
      }
    } catch (_) {
      mariMaestroFolderResolved[key] = pack.folder;
    }
    return mariMaestroFolderResolved[key];
  }
  async function ensureDiabloSpriteFolder() {
    return ensureMaestroSpriteFolder("diablo");
  }
  /* Qué: ¿avatar Calles usa pack day/ del maestro encarnado (discípulo opt-in)? */
  function encarnarMaestroIdActivo() {
    if (!vitainkOn || !encarnarMaestroId) return "";
    if (typeof puedeEncarnarMaestro !== "function") return "";
    return puedeEncarnarMaestro(encarnarMaestroId) ? maestroPack(encarnarMaestroId).id : "";
  }
  function encarnarDiabloActivo() {
    return encarnarMaestroIdActivo() === "diablo";
  }
  function maestroAvatarBase(maestroId, facing) {
    const pack = maestroPack(maestroId);
    const folder = maestroFolder(maestroId) || pack.folder;
    if (!folder || !pack.hasDay) return "";
    const f = facing || mariFacingAngle();
    const dir = (f === "top") ? "top" : "front";
    return MARI_BASE + "/masters/" + folder + "/day/" + dir;
  }
  function diabloAvatarBase(facing) {
    return maestroAvatarBase("diablo", facing);
  }


  /* v5.7–v5.9.1: encarnar avatar Calles (day pack) si discípulo — packs con hasDay */
  const ENCARNAR_MAESTRO_KEY = "rcv_vitaink_encarnar_maestro_v581";
  const ENCARNAR_DIABLO_KEY = "rcv_vitaink_encarnar_diablo_v57"; // legacy
  let encarnarMaestroId = "";
  try {
    encarnarMaestroId = localStorage.getItem(ENCARNAR_MAESTRO_KEY) || "";
    if (!encarnarMaestroId && localStorage.getItem(ENCARNAR_DIABLO_KEY) === "1") encarnarMaestroId = "diablo";
  } catch (_) {}
  let encarnarDiablo = false; // mirror legacy
  try { encarnarDiablo = encarnarMaestroId === "diablo"; } catch (_) {}

  let nearBotId = null;
  let nearErmitaId = null;
  let vitainkErmitas = [];
  let vitainkRito = null;
  let vitainkPeregrinacion = null; // snapshot GET /api/vitaink/peregrinacion
  let vitainkPeregrinacionAutoUntil = 0; // debounce auto-etapa cerca
  let vitainkMisiones = null;
  let vitainkPersonaje = null;
  let vitainkRanking = null;
  let vitainkRankTab = "monedas"; // monedas | reputacion
  /* v3.5–v4.6 — Dios / PNJ / crónica / maestros+senda+diálogo/encuentro+reliquias/sínodo+voto/ermita/rito/peregrinación/códice */
  let vitainkBots = [];
  let vitainkCronica = [];
  let vitainkMaestros = [];
  let vitainkRolesDisponibles = [];
  let vitainkRolPendiente = "seguidor";
  let vitainkValorSel = "";
  let vitainkAlineacion = null;
  let vitainkMaestroSel = null; // id seleccionado en panel
  let vitainkLecciones = null; // snapshot GET .../lecciones
  let vitainkDiario = [];
  let vitainkPrueba = null;
  let vitainkDialogo = null; // snapshot GET .../dialogo
  let vitainkReliquias = [];
  let vitainkSinodo = null;
  let vitainkDiosPin = ""; // solo memoria de página; no se persiste
  let vitainkDiosOk = false;
  let currentVitaCasaId = null;
  let activeRoute = null;
  let routeNavigating = false;
  let routeStepIndex = 0;
  let routeFollow = false;
  let routeDestPlaceId = null;

  /* —— v3.0 brújula / mini-mapa / pasos / favoritos —— */
  const ORIENT_LS_KEY = "rcv_orient_v30";
  const MINIMAP_ALWAYS_KEY = "rcv_minimap_always_v30";
  const FAVORITOS_LS_KEY = "rcv_favoritos_v30";
  let playerHeading = 0; // degrees: 0 = norte (arriba), 90 = este
  let orientMode = "norte"; // norte | rumbo
  let minimapAlways = false;
  let favoritosIds = [];
  let pasosOpen = false;
  let pasosTouchY0 = null;

  function ensureCitymap() {
    if (citymapCache) return Promise.resolve(citymapCache);
    if (citymapPromise) return citymapPromise;
    citymapPromise = fetchJSON("/api/citymap").then((g) => {
      citymapCache = g;
      buildStreetIndex(g);
      if (g.spawn) {
        playerX = g.spawn.x;
        playerY = g.spawn.y;
      }
      placePlayer();
      updateMiniMapaVisibility();
      updateMiniMapa();
      loadCityPois().catch(() => {});
      return g;
    }).catch((e) => {
      citymapPromise = null;
      throw e;
    });
    return citymapPromise;
  }

  function buildStreetIndex(g) {
    const byId = Object.create(null);
    placeNodes = [];
    for (const n of g.nodes || []) {
      byId[n.id] = n;
      if (n.kind === "place" && n.place_id) placeNodes.push(n);
    }
    streetSegments = [];
    for (const e of g.edges || []) {
      const a = byId[e.from];
      const b = byId[e.to];
      if (!a || !b) continue;
      streetSegments.push({
        x1: a.x, y1: a.y, x2: b.x, y2: b.y,
        name: e.name || "Calle",
        width: e.width || 1,
        from: e.from, to: e.to,
        fromLabel: a.label || "",
        toLabel: b.label || "",
      });
    }
    drawStreets(g, byId);
  }

  function drawStreets(g, byId) {
    if (!streetsSvg) return;
    let html = "";
    for (const e of g.edges || []) {
      const a = byId[e.from];
      const b = byId[e.to];
      if (!a || !b) continue;
      const w = Math.max(1, Math.min(3, e.width || 1));
      const sw = 1.2 + w * 0.9;
      html += `<line class="street-edge-outline" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke-width="${sw + 0.7}" />`;
      html += `<line class="street-edge w${w}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke-width="${sw}" />`;
    }
    for (const n of g.nodes || []) {
      if (n.kind !== "intersection") continue;
      html += `<circle cx="${n.x}" cy="${n.y}" r="0.55" fill="rgba(120,90,50,0.35)" />`;
    }
    streetsSvg.innerHTML = html;
    drawRouteOverlay();
  }

  function drawRouteOverlay() {
    if (!streetsSvg) return;
    // Ruta cívica (si hay)
    if (activeRoute && activeRoute.found) {
      const poly = activeRoute.polyline || [];
      if (poly.length >= 2) {
        let d = "";
        for (let i = 0; i < poly.length; i++) {
          d += (i === 0 ? "M" : "L") + poly[i].x + " " + poly[i].y + " ";
        }
        const end = poly[poly.length - 1];
        const start = poly[0];
        const frag =
          `<path class="route-line-outline" d="${d.trim()}" />` +
          `<path class="route-line" d="${d.trim()}" />` +
          `<circle class="route-marker" cx="${start.x}" cy="${start.y}" r="0.7" />` +
          `<circle class="route-marker" cx="${end.x}" cy="${end.y}" r="0.9" />`;
        streetsSvg.insertAdjacentHTML("beforeend", frag);
      }
    }
    drawPeregrinacionOverlay();
  }
  /* v4.5: guiones de peregrinación desde coords API (estilo ruta; sin import cívico→vitaink) */
  function drawPeregrinacionOverlay() {
    if (!streetsSvg || !vitainkOn || !vitainkPeregrinacion || !vitainkPeregrinacion.activa) return;
    const act = vitainkPeregrinacion.activa;
    if (act.terminada) return;
    const poly = act.polyline || [];
    if (poly.length >= 2) {
      let d = "";
      for (let i = 0; i < poly.length; i++) {
        d += (i === 0 ? "M" : "L") + poly[i].x + " " + poly[i].y + " ";
      }
      streetsSvg.insertAdjacentHTML(
        "beforeend",
        `<path class="peregrinacion-line-outline" d="${d.trim()}" />` +
        `<path class="peregrinacion-line" d="${d.trim()}" />`
      );
    }
    const paradas = act.paradas || [];
    for (const s of paradas) {
      if (s.x == null || s.y == null) continue;
      const cls = "peregrinacion-marker" + (s.actual ? " next" : "");
      const r = s.actual ? 1.05 : (s.hecha ? 0.55 : 0.75);
      streetsSvg.insertAdjacentHTML(
        "beforeend",
        `<circle class="${cls}" cx="${s.x}" cy="${s.y}" r="${r}" />`
      );
    }
  }

  function renderStreetBuildings(list) {
    if (!streetBuildings || !placeNodes.length) return;
    const hitIds = new Set((list || []).map((p) => p.id));
    const filtering = list && placesCacheFull && list.length < placesCacheFull.length && (search && search.value || "").trim();
    streetBuildings.innerHTML = "";
    for (const n of placeNodes) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "street-building";
      btn.dataset.placeId = n.place_id;
      // Tinte Calles (v4.7): biblioteca = torre-academia; residencial = bolsón
      if (n.place_id === "biblioteca-publica") btn.classList.add("theme-torre-academia");
      else if (n.place_id === "residencial") btn.classList.add("theme-bolson");
      // v5.8: idle bob en pins clave; bandera de mercado
      if (n.place_id === "ayuntamiento" || n.place_id === "mercado" || n.place_id === "hospital-clinico") {
        btn.classList.add("pin-idle-bob");
      }
      if (n.place_id === "mercado") {
        btn.classList.add("pin-mercado");
      }
      if (filtering && !hitIds.has(n.place_id)) btn.classList.add("dim");
      btn.style.left = Math.max(4, Math.min(96, n.x)) + "%";
      btn.style.top = Math.max(4, Math.min(96, n.y)) + "%";
      btn.title = (n.label || "") + (n.zone ? " · " + zoneLabel(n.zone) : "");
      btn.setAttribute("aria-label", n.label || "Lugar");
      const stamped = isPlaceStamped(n.place_id);
      const mission = isMissionTarget(n.place_id);
      if (stamped) btn.classList.add("stamped");
      if (mission) btn.classList.add("mission-target");
      const own = vitainkOn ? vitainkByPlace[n.place_id] : null;
      let vitaBadge = "";
      if (own) {
        btn.classList.add("vitaink-owned");
        btn.style.setProperty("--vita-color", own.color || "#94a3b8");
        const status = own.libre ? "libre" : "conquistado";
        btn.dataset.vitaink = status;
        const tip = own.libre ? "Libre (VitaInk)" : ("Conquistado por " + (own.owner_label || own.faction_name || ""));
        vitaBadge = `<span class="pin-vitaink" title="${escapeHTML(tip)}" aria-hidden="true">${escapeHTML(own.emoji || "🎮")}</span>`;
      }
      btn.innerHTML =
        `<span class="pin-emoji" aria-hidden="true">${escapeHTML(n.emoji || "📍")}</span>` +
        `<span class="pin-name">${escapeHTML(n.label || "")}</span>` +
        (n.place_id === "mercado" ? `<span class="pin-banner" aria-hidden="true"></span>` : "") +
        (stamped ? `<span class="pin-stamp" title="Visitado" aria-hidden="true">🔖</span>` : "") +
        vitaBadge;
      btn.addEventListener("click", (ev) => {
        ev.stopPropagation();
        openPlace(n.place_id, { fromCalles: true });
      });
      streetBuildings.appendChild(btn);
    }
    highlightNearBuilding();
    renderVitainkCasas();
  }

  function closestPointOnSeg(px, py, s) {
    const dx = s.x2 - s.x1;
    const dy = s.y2 - s.y1;
    const len2 = dx * dx + dy * dy;
    let t = 0;
    if (len2 > 1e-9) t = ((px - s.x1) * dx + (py - s.y1) * dy) / len2;
    t = Math.max(0, Math.min(1, t));
    return { x: s.x1 + t * dx, y: s.y1 + t * dy, t, dist: Math.hypot(px - (s.x1 + t * dx), py - (s.y1 + t * dy)), seg: s };
  }

  function snapToStreets(px, py, maxDist) {
    let best = null;
    for (const s of streetSegments) {
      const c = closestPointOnSeg(px, py, s);
      if (!best || c.dist < best.dist) best = c;
    }
    if (!best) return { x: px, y: py, name: "", ok: false, t: 0.5, seg: null };
    if (maxDist != null && best.dist > maxDist) return { x: px, y: py, name: best.seg.name, ok: false, t: best.t, seg: best.seg };
    return { x: best.x, y: best.y, name: best.seg.name, ok: true, dist: best.dist, t: best.t, seg: best.seg };
  }

  function placePlayer() {
    if (!playerAvatar) return;
    playerAvatar.style.left = playerX + "%";
    playerAvatar.style.top = playerY + "%";
    playerAvatar.style.setProperty("--facing", playerHeading + "deg");
    updateFollowCamera();
    updateBrujulaUI();
    updateMiniMapa();
    if (routeNavigating) updateRouteProgress();
  }

  const STREET_CORNER = 0.16;
  function streetNameOpacity(tt) {
    if (tt < 0) tt = 0;
    if (tt > 1) tt = 1;
    if (tt < STREET_CORNER) return tt / STREET_CORNER;
    if (tt > 1 - STREET_CORNER) return (1 - tt) / STREET_CORNER;
    return 1;
  }
  function streetNameAtProgress(seg, tt) {
    if (!seg) return "";
    if (tt <= STREET_CORNER && seg.fromLabel) return seg.fromLabel;
    if (tt >= 1 - STREET_CORNER && seg.toLabel) return seg.toLabel;
    return seg.name || "";
  }
  function updateStreetNameChip(seg, tt) {
    if (!streetNameChip) return;
    if (tt == null) tt = 0.5;
    const text = streetNameAtProgress(seg, tt);
    const showingCorner = !!(seg && ((tt <= STREET_CORNER && seg.fromLabel) || (tt >= 1 - STREET_CORNER && seg.toLabel)));
    let op = streetNameOpacity(tt);
    if (showingCorner) op = 1 - op;
    streetNameChip.textContent = text || "";
    streetNameChip.style.opacity = String(Math.max(0, Math.min(1, op)));
    streetNameChip.classList.toggle("visible", !!text && op > 0.12);
  }
  function updateStreetLabel(name, seg, tt) {
    if (streetLabel) {
      if (nearPlaceId) {
        const n = placeNodes.find((p) => p.place_id === nearPlaceId);
        streetLabel.textContent = n ? ("Entrar · " + (n.label || nearPlaceId)) : (name || "");
      } else if (nearParadaId) {
        const p = cityParadas.find((x) => x.id === nearParadaId);
        streetLabel.textContent = p ? ("Parada · " + (p.name || "")) : "";
      } else if (vitainkOn && nearTesoroId) {
        const tr = vitainkTesoros.find((x) => x.id === nearTesoroId);
        streetLabel.textContent = tr ? ("Tesoro · " + (tr.label || "💎")) : "";
      } else if (vitainkOn && nearErmitaId) {
        const er = vitainkErmitas.find((x) => x.id === nearErmitaId);
        streetLabel.textContent = er ? ("Retiro · " + (er.nombre || er.id)) : "Retiro";
      } else if (vitainkOn && nearBotId) {
        const b = vitainkBots.find((x) => x.id === nearBotId);
        streetLabel.textContent = b ? ("Hablar · " + (b.display_name || b.id)) : "Hablar";
      } else if (nearBancoId) {
        const b = cityBancos.find((x) => x.id === nearBancoId);
        streetLabel.textContent = b ? ("Banco · " + (b.name || "")) : "";
      } else {
        streetLabel.textContent = "";
      }
    }
    updateStreetNameChip(seg || null, tt);
    updateCivicAction();
  }

  function highlightNearBuilding() {
    const radius = (citymapCache && citymapCache.meta && citymapCache.meta.enter_radius) || 3.5;
    let best = null;
    for (const n of placeNodes) {
      const d = Math.hypot(playerX - n.x, playerY - n.y);
      if (d <= radius && (!best || d < best.d)) best = { id: n.place_id, d };
    }
    nearPlaceId = best ? best.id : null;
    if (streetBuildings) {
      streetBuildings.querySelectorAll(".street-building").forEach((el) => {
        el.classList.toggle("near", el.dataset.placeId === nearPlaceId);
      });
    }
  }

  function tryEnterNear() {
    if (!nearPlaceId) return;
    const now = performance.now();
    if (now < enterCooldown) return;
    enterCooldown = now + 800;
    openPlace(nearPlaceId, { fromCalles: true });
  }

  function movePlayer(dx, dy, dt) {
    if (!streetSegments.length) return;
    if (performance.now() < sittingUntil) return;
    const len = Math.hypot(dx, dy) || 1;
    // Heading: 0 = norte (arriba / -Y), 90 = este (+X). Screen Y grows down.
    if (dx || dy) {
      playerHeading = (Math.atan2(dx, -dy) * 180 / Math.PI + 360) % 360;
    }
    const step = (bikeMode ? BIKE_SPEED : WALK_SPEED) * dt;
    const nx = playerX + (dx / len) * step;
    const ny = playerY + (dy / len) * step;
    // Prefer snap near intended point; allow slightly larger search along movement
    let snapped = snapToStreets(nx, ny, SNAP_MAX);
    if (!snapped.ok) {
      // Try projecting further along intent onto network
      snapped = snapToStreets(nx, ny, SNAP_MAX * 2.2);
    }
    if (!snapped.ok) {
      // Stay but refresh label from current snap
      const cur = snapToStreets(playerX, playerY, null);
      updateStreetLabel(cur.name, cur.seg, cur.t);
      return;
    }
    playerX = Math.max(2, Math.min(98, snapped.x));
    playerY = Math.max(2, Math.min(98, snapped.y));
    placePlayer();
    highlightNearBuilding();
    highlightNearPois();
    updateStreetLabel(snapped.name, snapped.seg, snapped.t);
    if (Math.random() < 0.08) maybeSpawnStreetEvent();
    maybeSpawnMarketDay();
    // Auto-enter when very close and still moving toward building
    if (nearPlaceId) {
      const n = placeNodes.find((p) => p.place_id === nearPlaceId);
      if (n && Math.hypot(playerX - n.x, playerY - n.y) < 1.6) tryEnterNear();
    }
  }

  function readInputVector() {
    let dx = 0, dy = 0;
    if (keysDown.ArrowLeft || keysDown.a || keysDown.A || keysDown.left) dx -= 1;
    if (keysDown.ArrowRight || keysDown.d || keysDown.D || keysDown.right) dx += 1;
    if (keysDown.ArrowUp || keysDown.w || keysDown.W || keysDown.up) dy -= 1;
    if (keysDown.ArrowDown || keysDown.s || keysDown.S || keysDown.down) dy += 1;
    return { dx, dy };
  }

  function streetLoop(ts) {
    if (homeViewMode !== "calles") {
      streetRAF = 0;
      return;
    }
    if (!lastStreetTS) lastStreetTS = ts;
    let dt = (ts - lastStreetTS) / 1000;
    lastStreetTS = ts;
    if (dt > 0.05) dt = 0.05;
    const { dx, dy } = readInputVector();
    const moving = !!(dx || dy);
    if (moving) movePlayer(dx, dy, dt);
    updateMariWalkFrame(moving);
    streetRAF = requestAnimationFrame(streetLoop);
  }

  function startStreetLoop() {
    if (streetRAF) return;
    lastStreetTS = 0;
    placePlayer();
    const cur = snapToStreets(playerX, playerY, null);
    updateStreetLabel(cur.name, cur.seg, cur.t);
    streetRAF = requestAnimationFrame(streetLoop);
  }

  function stopStreetLoop() {
    if (streetRAF) cancelAnimationFrame(streetRAF);
    streetRAF = 0;
    lastStreetTS = 0;
  }

  function bindStreetControls() {
    window.addEventListener("keydown", (e) => {
      if (homeViewMode !== "calles") return;
      const k = e.key;
      if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "w", "a", "s", "d", "W", "A", "S", "D"].includes(k)) {
        keysDown[k] = true;
        e.preventDefault();
      }
      if (k === "Enter" || k === " ") {
        tryCivicAction();
        e.preventDefault();
      }
    });
    window.addEventListener("keyup", (e) => {
      keysDown[e.key] = false;
    });

    if (dpad) {
      const setDir = (dir, on) => {
        if (dir === "enter") {
          if (on) tryCivicAction();
          return;
        }
        keysDown[dir] = on;
      };
      dpad.querySelectorAll(".dpad-btn").forEach((btn) => {
        const dir = btn.dataset.dir;
        const down = (ev) => {
          ev.preventDefault();
          btn.classList.add("held");
          setDir(dir, true);
        };
        const up = (ev) => {
          ev.preventDefault();
          btn.classList.remove("held");
          setDir(dir, false);
        };
        btn.addEventListener("pointerdown", down);
        btn.addEventListener("pointerup", up);
        btn.addEventListener("pointerleave", up);
        btn.addEventListener("pointercancel", up);
      });
    }

    // Touch drag on the streets canvas (not on dpad/buildings)
    if (cityStreets) {
      let dragging = false;
      let lastTX = 0, lastTY = 0;
      const toWorldPct = (clientX, clientY) => {
        const r = cityStreets.getBoundingClientRect();
        const sx = ((clientX - r.left) / r.width) * 100;
        const sy = ((clientY - r.top) / r.height) * 100;
        const z = (typeof callesZoom === "number" && isFinite(callesZoom) && callesZoom > 0.01) ? callesZoom : 1;
        const camFollow = !!(routeFollow && activeRoute) || (orientMode === "rumbo" && vistaMode !== "mirador") || Math.abs(z - 1) > 0.001;
        if (!camFollow || vistaMode === "mirador") return { x: sx, y: sy };
        // Inversa de translate(50 - p*z) scale(z) con origin 0,0
        return {
          x: playerX + (sx - 50) / z,
          y: playerY + (sy - 50) / z,
        };
      };
      cityStreets.addEventListener("pointerdown", (e) => {
        if (homeViewMode !== "calles") return;
        if (e.target.closest(".dpad") || e.target.closest(".street-building") || e.target.closest(".street-poi") || e.target.closest(".civic-action") || e.target.closest(".calles-tools") || e.target.closest(".vita-bot-pin") || e.target.closest(".vita-ermita-pin") || e.target.closest("#calles-fs-exit")) return;
        dragging = true;
        cityStreets.setPointerCapture(e.pointerId);
        const p = toWorldPct(e.clientX, e.clientY);
        lastTX = p.x; lastTY = p.y;
        const dx = p.x - playerX, dy = p.y - playerY;
        if (Math.hypot(dx, dy) > 1) movePlayer(dx, dy, 0.08);
      });
      cityStreets.addEventListener("pointermove", (e) => {
        if (!dragging || homeViewMode !== "calles") return;
        const p = toWorldPct(e.clientX, e.clientY);
        const dx = p.x - lastTX, dy = p.y - lastTY;
        lastTX = p.x; lastTY = p.y;
        if (Math.hypot(dx, dy) > 0.15) movePlayer(dx, dy, 0.05);
      });
      const endDrag = (e) => {
        dragging = false;
        try { cityStreets.releasePointerCapture(e.pointerId); } catch (_) {}
      };
      cityStreets.addEventListener("pointerup", endDrag);
      cityStreets.addEventListener("pointercancel", endDrag);
    }
  }


  /* —— v2.5 especiales ciudad —— */
  /* —— v2.6 bici / misiones / viñeta —— */

  const TOD_DEMO_KEY = "rcv_tod_demo_v25";
  const TOD_FORCE_KEY = "rcv_tod_force_v25";
  const STAMPS_LS_KEY = "rcv_stamps_v25";
  const EVENT_COOLDOWN_MS = 45000;
  let cityEvents = [];
  let stampsAlbum = null;
  let stampsCount = 0;
  let lastEventAt = 0;
  let lastEventId = "";
  let todPhase = "dia";
  let todDemo = false;
  let todForce = "";
  let todDemoHour = 12;
  let todTimer = 0;
  let eventToastPlaceId = "";

  const CLIMA_FORCE_KEY = "rcv_clima_force_v27";
  const MERCADO_FORCE_KEY = "rcv_mercado_force_v27";
  let climaSky = "sol";
  let climaForce = "";
  let climaTimer = 0;
  let marketDayActive = false;
  let marketForce = false;
  let marketEvent = null;
  let lastMarketToastAt = 0;

  /* —— v2.8 paradas / luces / bancos —— */
  let cityParadas = [];
  let cityBancos = [];
  let cityTips = [];
  let cityLuces = [];
  let paradaRadius = 4;
  let bancoRadius = 3.5;
  let sitMs = 1500;
  let nearParadaId = null;
  let nearBancoId = null;
  let tipRotate = 0;
  let sittingUntil = 0;
  let linePickerFrom = null;

  async function loadCityPois() {
    try {
      const [pa, ba, lu] = await Promise.all([
        fetchJSON("/api/city/paradas"),
        fetchJSON("/api/city/bancos"),
        fetchJSON("/api/city/luces"),
      ]);
      cityParadas = (pa && pa.paradas) || [];
      if (pa && pa.radius) paradaRadius = pa.radius;
      cityBancos = (ba && ba.bancos) || [];
      cityTips = (ba && ba.tips) || [];
      if (ba && ba.radius) bancoRadius = ba.radius;
      if (ba && ba.sit_ms) sitMs = ba.sit_ms;
      cityLuces = (lu && lu.lights) || [];
    } catch (_) {
      if (!cityParadas.length) {
        cityParadas = [
          { id: "parada-plaza-mayor", name: "Plaza Mayor", x: 51.2, y: 49.5, emoji: "🚏", line: "Línea Cívica" },
          { id: "parada-fuente-dorada", name: "Fuente Dorada", x: 45.5, y: 41.2, emoji: "🚏", line: "Línea Cívica" },
          { id: "parada-circular", name: "Plaza Circular", x: 73.2, y: 39.5, emoji: "🚏", line: "Línea Este" },
          { id: "parada-estacion", name: "Estación", x: 53.0, y: 78.8, emoji: "🚏", line: "Línea Sur" },
        ];
      }
      if (!cityBancos.length) {
        cityBancos = [
          { id: "banco-plaza-mayor", name: "Banco Plaza Mayor", x: 48.5, y: 46.8, emoji: "🪑" },
          { id: "banco-campo", name: "Banco Campo Grande", x: 32.5, y: 59.2, emoji: "🪑" },
        ];
      }
      if (!cityTips.length) {
        cityTips = [
          { id: "tip-agua", body: "Bebe agua de las fuentes públicas cuando puedas: es un bien común." },
          { id: "tip-plaza", body: "Las plazas son de todos: comparte el banco y el espacio." },
        ];
      }
    }
    renderStreetPois();
    ensureWarmWindows(true);
  }

  function renderStreetPois() {
    const box = $("#street-pois");
    if (!box) return;
    box.innerHTML = "";
    const add = (item, kind) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "street-poi " + kind;
      btn.dataset.poiId = item.id;
      btn.dataset.kind = kind;
      btn.style.left = Math.max(3, Math.min(97, item.x)) + "%";
      btn.style.top = Math.max(3, Math.min(97, item.y)) + "%";
      btn.title = item.name || kind;
      btn.setAttribute("aria-label", item.name || kind);
      btn.textContent = item.emoji || (kind === "parada" ? "🚏" : "🪑");
      btn.addEventListener("click", (ev) => {
        ev.stopPropagation();
        if (kind === "parada") openLinePicker(item.id);
        else if (kind === "banco") descansarEnBanco(item.id);
      });
      box.appendChild(btn);
    };
    for (const p of cityParadas) add(p, "parada");
    for (const b of cityBancos) add(b, "banco");
    highlightNearPois();
  }

  function highlightNearPois() {
    nearParadaId = null;
    nearBancoId = null;
    nearTesoroId = null;
    nearBotId = null;
    nearErmitaId = null;
    let bestP = null, bestB = null, bestT = null, bestBot = null, bestE = null;
    for (const p of cityParadas) {
      const d = Math.hypot(playerX - p.x, playerY - p.y);
      if (d <= paradaRadius && (!bestP || d < bestP.d)) bestP = { id: p.id, d };
    }
    for (const b of cityBancos) {
      const d = Math.hypot(playerX - b.x, playerY - b.y);
      if (d <= bancoRadius && (!bestB || d < bestB.d)) bestB = { id: b.id, d };
    }
    nearParadaId = bestP ? bestP.id : null;
    nearBancoId = bestB ? bestB.id : null;
    if (vitainkOn && vitainkAvailable) {
      for (const tr of vitainkTesoros) {
        if (tr.claimed) continue;
        const d = Math.hypot(playerX - tr.x, playerY - tr.y);
        if (d <= tesoroRadius && (!bestT || d < bestT.d)) bestT = { id: tr.id, d };
      }
      for (const b of vitainkBots) {
        if (!b || b.enabled === false) continue;
        const d = Math.hypot(playerX - (b.x || 50), playerY - (b.y || 50));
        if (d <= botRadius && (!bestBot || d < bestBot.d)) bestBot = { id: b.id, d };
      }
      for (const e of vitainkErmitas) {
        if (!e) continue;
        const d = Math.hypot(playerX - (e.x || 50), playerY - (e.y || 50));
        if (d <= botRadius && (!bestE || d < bestE.d)) bestE = { id: e.id, d };
      }
    }
    nearTesoroId = bestT ? bestT.id : null;
    nearBotId = bestBot ? bestBot.id : null;
    nearErmitaId = bestE ? bestE.id : null;
    const tesBox = $("#street-vitaink-tesoros");
    if (tesBox) {
      tesBox.querySelectorAll(".vita-tesoro-pin").forEach((el) => {
        el.classList.toggle("near", el.dataset.tesoroId === nearTesoroId);
      });
    }
    const botsBox = $("#street-vitaink-bots");
    if (botsBox) {
      botsBox.querySelectorAll(".vita-bot-pin").forEach((el) => {
        el.classList.toggle("near", el.dataset.botId === nearBotId);
      });
    }
    const ermBox = $("#street-vitaink-ermitas");
    if (ermBox) {
      ermBox.querySelectorAll(".vita-ermita-pin").forEach((el) => {
        el.classList.toggle("near", el.dataset.ermitaId === nearErmitaId);
      });
    }
    renderVitainkPeregrinacionPins();
    maybeAutoEtapaPeregrinacion();
    const box = $("#street-pois");
    if (box) {
      box.querySelectorAll(".street-poi").forEach((el) => {
        const id = el.dataset.poiId;
        el.classList.toggle("near", id === nearParadaId || id === nearBancoId);
      });
    }
    updateCivicAction();
  }

  function updateCivicAction() {
    const btn = $("#civic-action");
    if (!btn) return;
    btn.classList.remove("civic-hablar");
    if (homeViewMode !== "calles" || performance.now() < sittingUntil) {
      btn.classList.add("hidden");
      return;
    }
    if (vitainkOn && nearTesoroId) {
      const tr = vitainkTesoros.find((x) => x.id === nearTesoroId);
      btn.textContent = "💎 Reclamar tesoro" + (tr && tr.label ? " · " + tr.label : "");
      btn.dataset.action = "tesoro";
      btn.classList.remove("hidden");
      return;
    }
    if (vitainkOn && nearErmitaId) {
      const er = vitainkErmitas.find((x) => x.id === nearErmitaId);
      btn.textContent = "🛕 Retiro" + (er && er.nombre ? " · " + er.nombre : "");
      btn.classList.remove("hidden");
      btn.dataset.action = "retiro";
      btn.dataset.ermitaId = nearErmitaId;
      return;
    }
    if (vitainkOn && nearBotId) {
      const b = vitainkBots.find((x) => x.id === nearBotId);
      btn.textContent = "💬 Hablar" + (b && b.display_name ? " · " + b.display_name : "");
      btn.dataset.action = "hablar";
      btn.dataset.botId = nearBotId;
      btn.classList.add("civic-hablar");
      btn.classList.remove("hidden");
      return;
    }
    if (nearParadaId) {
      const p = cityParadas.find((x) => x.id === nearParadaId);
      btn.textContent = "🚏 Tomar línea" + (p && p.name ? " · " + p.name : "");
      btn.dataset.action = "linea";
      btn.classList.remove("hidden");
      return;
    }
    if (nearBancoId && !nearPlaceId) {
      const b = cityBancos.find((x) => x.id === nearBancoId);
      btn.textContent = "🪑 Descansar" + (b && b.name ? " · " + b.name : "");
      btn.dataset.action = "descansar";
      btn.classList.remove("hidden");
      return;
    }
    btn.classList.add("hidden");
    btn.dataset.action = "";
  }

  function openLinePicker(fromId) {
    const modal = $("#line-picker");
    const list = $("#line-picker-list");
    if (!modal || !list) return;
    linePickerFrom = fromId || nearParadaId;
    list.innerHTML = "";
    const others = cityParadas.filter((p) => p.id !== linePickerFrom);
    if (!others.length) {
      setStatus("No hay otras paradas", "err");
      return;
    }
    for (const p of others) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "line-picker-item";
      btn.setAttribute("role", "listitem");
      btn.innerHTML =
        `<span aria-hidden="true">${escapeHTML(p.emoji || "🚏")}</span>` +
        `<span><strong>${escapeHTML(p.name || p.id)}</strong>` +
        `<div class="meta">${escapeHTML(p.line || "Línea cívica")}</div></span>`;
      btn.addEventListener("click", () => {
        teleportToParada(p.id);
        closeLinePicker();
      });
      list.appendChild(btn);
    }
    modal.classList.remove("hidden");
  }

  function closeLinePicker() {
    const modal = $("#line-picker");
    if (modal) modal.classList.add("hidden");
    linePickerFrom = null;
  }

  function teleportToParada(id) {
    const p = cityParadas.find((x) => x.id === id);
    if (!p) return;
    const snapped = snapToStreets(p.x, p.y, null);
    playerX = Math.max(2, Math.min(98, snapped.ok ? snapped.x : p.x));
    playerY = Math.max(2, Math.min(98, snapped.ok ? snapped.y : p.y));
    placePlayer();
    highlightNearBuilding();
    highlightNearPois();
    updateStreetLabel(snapped.name || "", snapped.seg, snapped.t);
    setStatus("Llegada · " + (p.name || "parada"), "ok");
  }

  function nextCivicTip() {
    if (!cityTips.length) return { body: "Descansa un momento. La plaza es de todos." };
    const tip = cityTips[tipRotate % cityTips.length];
    tipRotate = (tipRotate + 1) % cityTips.length;
    return tip;
  }

  function descansarEnBanco(id) {
    const b = cityBancos.find((x) => x.id === (id || nearBancoId));
    if (!b) return;
    if (performance.now() < sittingUntil) return;
    sittingUntil = performance.now() + sitMs;
    if (playerAvatar) playerAvatar.classList.add("sitting");
    // Soft nudge onto bench
    playerX = b.x;
    playerY = b.y;
    placePlayer();
    const tip = nextCivicTip();
    showEventToast({
      id: tip.id || "tip-banco",
      title: "Descanso · " + (b.name || "Banco"),
      body: tip.body || "",
      kind: "tip",
    });
    updateCivicAction();
    setTimeout(() => {
      if (playerAvatar) playerAvatar.classList.remove("sitting");
      sittingUntil = 0;
      highlightNearPois();
    }, sitMs);
  }

  function tryCivicAction() {
    if (performance.now() < sittingUntil) return true;
    if (nearPlaceId) {
      tryEnterNear();
      return true;
    }
    if (nearParadaId) {
      openLinePicker(nearParadaId);
      return true;
    }
    if (vitainkOn && nearTesoroId) {
      reclamarTesoroCercano().catch(() => {});
      return true;
    }
    if (nearBancoId) {
      descansarEnBanco(nearBancoId);
      return true;
    }
    return false;
  }


  function loadTodPrefs() {
    try {
      todDemo = localStorage.getItem(TOD_DEMO_KEY) === "1";
      todForce = localStorage.getItem(TOD_FORCE_KEY) || "";
    } catch (_) {}
  }

  function saveTodPrefs() {
    try {
      localStorage.setItem(TOD_DEMO_KEY, todDemo ? "1" : "0");
      if (todForce) localStorage.setItem(TOD_FORCE_KEY, todForce);
      else localStorage.removeItem(TOD_FORCE_KEY);
    } catch (_) {}
  }

  function phaseFromHour(h) {
    h = ((h % 24) + 24) % 24;
    if (h >= 7 && h <= 18) return "dia";
    if (h === 19 || h === 20) return "atardecer";
    return "noche";
  }

  function todMeta(phase) {
    if (phase === "noche") return { icon: "🌙", label: "Noche" };
    if (phase === "atardecer") return { icon: "🌇", label: "Atardecer" };
    return { icon: "☀️", label: "Día" };
  }

  function ensureWarmWindows(force) {
    const fill = (el, n) => {
      if (!el) return;
      if (!force && el.childElementCount) return;
      let html = "";
      const lights = cityLuces.length ? cityLuces : null;
      if (lights) {
        for (let i = 0; i < lights.length; i++) {
          const L = lights[i];
          const s = Math.max(0.7, Math.min(1.4, L.size || 1));
          html += `<span class="win" style="left:${L.x}%;top:${L.y}%;transform:scale(${s})"></span>`;
          html += `<span class="win" style="left:${(L.x + 1.1).toFixed(1)}%;top:${(L.y + 0.7).toFixed(1)}%;transform:scale(${(s * 0.85).toFixed(2)})"></span>`;
        }
      } else {
        const seeds = [
          [22, 28], [48, 44], [55, 50], [70, 36], [34, 60], [80, 48],
          [18, 42], [42, 20], [60, 72], [88, 16], [12, 18], [50, 80],
          [28, 38], [74, 30], [40, 54], [64, 42],
        ];
        for (let i = 0; i < Math.min(n, seeds.length); i++) {
          const [x, y] = seeds[i];
          html += `<span class="win" style="left:${x}%;top:${y}%"></span>`;
          html += `<span class="win" style="left:${x + 1.2}%;top:${y + 0.8}%"></span>`;
        }
      }
      // Extra glows near place buildings on Calles
      if (el.id === "street-windows" && placeNodes.length) {
        for (let i = 0; i < placeNodes.length; i += 2) {
          const n = placeNodes[i];
          html += `<span class="win" style="left:${(n.x + 0.6).toFixed(1)}%;top:${(n.y - 0.8).toFixed(1)}%"></span>`;
        }
      }
      el.innerHTML = html;
    };
    fill($("#street-windows"), 16);
    fill($("#map-windows"), 12);
  }

  function applyTodPhase(phase) {
    todPhase = phase || "dia";
    const meta = todMeta(todPhase);
    const hud = $("#hud-tod");
    if (hud) hud.textContent = meta.icon + " " + meta.label;
    ensureWarmWindows();
    // Calles/Mapa + Mi casa (ventanas redondas v5.0) comparten la misma fase.
    [cityStreets, civicMap, viewCasa].forEach((el) => {
      if (!el) return;
      el.classList.remove("tod-dia", "tod-atardecer", "tod-noche");
      el.classList.add("tod-" + todPhase);
    });
    // Mari lote2: day↔night paths (front/top night).
    if (typeof applyPlayerAvatarLook === "function") applyPlayerAvatarLook();
  }

  function currentHour() {
    if (todDemo) return Math.floor(todDemoHour) % 24;
    return new Date().getHours();
  }

  function refreshTod() {
    let phase = todForce || phaseFromHour(currentHour());
    applyTodPhase(phase);
    if (todDemo) {
      todDemoHour = (todDemoHour + 0.35) % 24;
    }
    refreshClima();
  }

  function startTodLoop() {
    if (todTimer) return;
    refreshTod();
    todTimer = setInterval(refreshTod, todDemo ? 800 : 60000);
  }

  function restartTodLoop() {
    if (todTimer) clearInterval(todTimer);
    todTimer = 0;
    startTodLoop();
  }

  function loadClimaPrefs() {
    try {
      climaForce = localStorage.getItem(CLIMA_FORCE_KEY) || "";
      marketForce = localStorage.getItem(MERCADO_FORCE_KEY) === "1";
    } catch (_) {}
  }
  function saveClimaPrefs() {
    try {
      if (climaForce) localStorage.setItem(CLIMA_FORCE_KEY, climaForce);
      else localStorage.removeItem(CLIMA_FORCE_KEY);
      if (marketForce) localStorage.setItem(MERCADO_FORCE_KEY, "1");
      else localStorage.removeItem(MERCADO_FORCE_KEY);
    } catch (_) {}
  }
  function yearDayLocal(d) {
    const start = Date.UTC(d.getFullYear(), 0, 0);
    const now = Date.UTC(d.getFullYear(), d.getMonth(), d.getDate());
    return Math.round((now - start) / 86400000);
  }
  function skyFromClock(d) {
    const h = ((d.getHours() % 24) + 24) % 24;
    const slot = Math.floor(h / 3);
    const seed = d.getFullYear() * 400 + yearDayLocal(d);
    let v = (seed * 17 + slot * 31) % 10;
    if (v < 0) v += 10;
    if (v <= 3) return "sol";
    if (v <= 7) return "nubes";
    return "lluvia";
  }
  function climaMeta(sky) {
    if (sky === "lluvia") return { icon: "🌧️", label: "Lluvia ligera", rain: true };
    if (sky === "nubes") return { icon: "☁️", label: "Nubes", rain: false };
    return { icon: "☀️", label: "Sol", rain: false };
  }
  function ensureRainDrops() {
    const el = $("#clima-rain");
    if (!el || el.childElementCount) return;
    let html = "";
    for (let i = 0; i < 22; i++) {
      const left = (3 + (i * 4.3) % 94).toFixed(1);
      const delay = ((i * 0.11) % 0.9).toFixed(2);
      const dur = (0.7 + (i % 5) * 0.08).toFixed(2);
      html += `<span class="drop" style="left:${left}%;animation-delay:${delay}s;animation-duration:${dur}s"></span>`;
    }
    el.innerHTML = html;
  }
  function applyClimaSky(sky) {
    climaSky = sky || "sol";
    const meta = climaMeta(climaSky);
    const hud = $("#hud-clima");
    if (hud) {
      hud.textContent = meta.icon + " " + meta.label;
      hud.classList.toggle("clima-lluvia-chip", climaSky === "lluvia");
    }
    ensureRainDrops();
    if (cityStreets) {
      cityStreets.classList.remove("clima-sol", "clima-nubes", "clima-lluvia");
      cityStreets.classList.add("clima-" + climaSky);
    }
  }
  function currentClimaSky() {
    if (climaForce === "sol" || climaForce === "nubes" || climaForce === "lluvia") return climaForce;
    const d = todDemo ? new Date(new Date().setHours(currentHour(), 0, 0, 0)) : new Date();
    if (todDemo) d.setHours(currentHour(), 0, 0, 0);
    return skyFromClock(d);
  }
  function refreshClima() {
    applyClimaSky(currentClimaSky());
  }
  function startClimaLoop() {
    if (climaTimer) return;
    refreshClima();
    climaTimer = setInterval(refreshClima, todDemo ? 800 : 60000);
  }
  function restartClimaLoop() {
    if (climaTimer) clearInterval(climaTimer);
    climaTimer = 0;
    startClimaLoop();
  }

  async function refreshMarketDay() {
    try {
      const q = marketForce ? "?force=1" : "";
      const v = await fetchJSON("/api/city/mercado" + q);
      marketDayActive = !!(v && v.active) || marketForce;
      marketEvent = (v && v.event) || (marketDayActive ? {
        id: "ev-dia-mercado",
        title: "Día de mercado",
        body: "Hoy hay mercado en la plaza",
        place_id: "mercado",
        near: "plaza-mayor",
        kind: "tip",
      } : null);
    } catch (_) {
      marketDayActive = marketForce;
      marketEvent = marketDayActive ? {
        id: "ev-dia-mercado",
        title: "Día de mercado",
        body: "Hoy hay mercado en la plaza",
        place_id: "mercado",
        near: "plaza-mayor",
        kind: "tip",
      } : null;
    }
    syncMarketDayClass();
  }

  function syncMarketDayClass() {
    // v5.8: bandera de plaza solo en día de mercado (CSS .dia-mercado)
    if (cityStreets) cityStreets.classList.toggle("dia-mercado", !!marketDayActive);
  }

  function maybeSpawnMarketDay() {
    if (homeViewMode !== "calles") return;
    if (!marketDayActive || !marketEvent) return;
    const now = performance.now();
    if (now - lastEventAt < EVENT_COOLDOWN_MS) return;
    if (now - lastMarketToastAt < EVENT_COOLDOWN_MS * 2) return;
    const spots = [
      { x: 50, y: 48 }, // Plaza Mayor
      { x: 44, y: 42 }, // Fuente Dorada
      { x: 42, y: 52 }, // Mercado
      { x: 82, y: 55 }, // Centro comercial
    ];
    let near = nearPlaceId === "mercado" || nearPlaceId === "centro-comercial";
    if (!near) {
      for (const s of spots) {
        if (Math.hypot(playerX - s.x, playerY - s.y) <= 9) { near = true; break; }
      }
    }
    if (!near) return;
    lastMarketToastAt = now;
    showEventToast(marketEvent);
  }

  function localStampsMap() {
    try {
      return JSON.parse(localStorage.getItem(STAMPS_LS_KEY) || "{}") || {};
    } catch (_) {
      return {};
    }
  }

  function saveLocalStamp(placeId) {
    const m = localStampsMap();
    if (!m[placeId]) {
      m[placeId] = Math.floor(Date.now() / 1000);
      try { localStorage.setItem(STAMPS_LS_KEY, JSON.stringify(m)); } catch (_) {}
    }
  }

  function updateStampsHUD(count) {
    stampsCount = count;
    const el = $("#hud-stamps-count");
    if (el) el.textContent = String(count);
    if (homeViewMode === "calles" && placeNodes.length) renderStreetBuildings(placesCache);
  }

  async function refreshStamps() {
    try {
      const album = await fetchJSON("/api/city/stamps");
      stampsAlbum = album;
      updateStampsHUD(album.collected || 0);
      // merge localStorage extras (offline visits) best-effort sync
      const local = localStampsMap();
      const missing = Object.keys(local).filter((id) => {
        const e = (album.entries || []).find((x) => x.place_id === id);
        return e && !e.collected;
      });
      for (const id of missing.slice(0, 5)) {
        try {
          await fetchJSON("/api/city/stamps", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ place_id: id, user_id: me.user_id || "" }),
          });
        } catch (_) {}
      }
      if (missing.length) {
        stampsAlbum = await fetchJSON("/api/city/stamps");
        updateStampsHUD(stampsAlbum.collected || 0);
      }
      return stampsAlbum;
    } catch (e) {
      const local = localStampsMap();
      updateStampsHUD(Object.keys(local).length);
      return null;
    }
  }

  async function stampPlaceVisit(placeId) {
    if (!placeId) return;
    saveLocalStamp(placeId);
    try {
      const res = await fetchJSON("/api/city/stamps", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ place_id: placeId, user_id: me.user_id || "" }),
      });
      if (res.album) {
        stampsAlbum = res.album;
        updateStampsHUD(res.album.collected || res.collected || 0);
      } else if (typeof res.collected === "number") {
        updateStampsHUD(res.collected);
      }
      if (res.new) setStatus("Sello · " + placeId, "ok");
      refreshMissions().catch(() => {});
    } catch (_) {
      updateStampsHUD(Object.keys(localStampsMap()).length);
    }
  }

  function renderSellosAlbum(album) {
    const box = $("#sellos-album");
    const prog = $("#sellos-progress");
    if (!box) return;
    box.innerHTML = "";
    if (!album) {
      if (prog) prog.textContent = "—";
      return;
    }
    if (prog) prog.textContent = (album.collected || 0) + " / " + (album.total || 0);
    for (const e of album.entries || []) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "sello-card " + (e.collected ? "collected" : "missing");
      btn.setAttribute("role", "listitem");
      btn.innerHTML =
        `<span class="sello-emoji" aria-hidden="true">${escapeHTML(e.emoji || "📍")}</span>` +
        `<span class="sello-name">${escapeHTML(e.name || e.place_id)}</span>` +
        (e.collected
          ? `<span class="sello-stamp-mark">Sellado</span>`
          : `<span class="sello-meta">Por visitar</span>`);
      btn.addEventListener("click", () => {
        openPlace(e.place_id).catch(() => {});
      });
      box.appendChild(btn);
    }
  }

  async function showSellos() {
    stopPoll();
    hideAllViews();
    if (viewSellos) viewSellos.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = "Libro de sellos";
    subtitle.textContent = "Lugares visitados · iguales";
    setNav("lugares");
    const album = await refreshStamps();
    renderSellosAlbum(album || stampsAlbum);
    history.pushState({ view: "sellos" }, "", "/sellos");
  }

  async function loadCityEvents() {
    try {
      const q = marketForce ? "?force=1" : "";
      const snap = await fetchJSON("/api/city/events" + q);
      cityEvents = snap.events || [];
    } catch (_) {
      cityEvents = [];
    }
    await refreshMarketDay();
  }

  function hubNearPlayer() {
    // Match citymap hub labels loosely via place proximity / zone hubs coords
    const hubs = [
      { near: "plaza-mayor", x: 50, y: 48 },
      { near: "fuente-dorada", x: 44, y: 42 },
      { near: "zorrilla", x: 48, y: 68 },
      { near: "campo-grande", x: 34, y: 58 },
      { near: "universidad", x: 42, y: 22 },
      { near: "hospital", x: 56, y: 18 },
      { near: "circular", x: 74, y: 38 },
      { near: "parque-bomberos", x: 84, y: 48 },
      { near: "parquesol", x: 18, y: 40 },
      { near: "estacion", x: 52, y: 80 },
      { near: "red-norte", x: 88, y: 12 },
    ];
    let best = null;
    for (const h of hubs) {
      const d = Math.hypot(playerX - h.x, playerY - h.y);
      if (d <= 8 && (!best || d < best.d)) best = { ...h, d };
    }
    return best;
  }

  function showEventToast(ev) {
    const toast = $("#event-toast");
    if (!toast || !ev) return;
    // En modo juego limpio no interrumpir con ruido cívico (mercado, etc.)
    if (vitainkOn && juegoLimpio) return;
    $("#event-toast-title").textContent = ev.title || "Aviso callejero";
    $("#event-toast-body").textContent = ev.body || "";
    eventToastPlaceId = ev.place_id || "";
    const go = $("#event-toast-place");
    if (go) {
      if (eventToastPlaceId) go.classList.remove("hidden");
      else go.classList.add("hidden");
    }
    toast.classList.remove("hidden");
    lastEventId = ev.id || "";
    lastEventAt = performance.now();
  }

  function dismissEventToast() {
    const toast = $("#event-toast");
    if (toast) toast.classList.add("hidden");
    eventToastPlaceId = "";
  }

  function maybeSpawnStreetEvent() {
    if (homeViewMode !== "calles") return;
    if (!cityEvents.length) return;
    const now = performance.now();
    if (now - lastEventAt < EVENT_COOLDOWN_MS) return;
    const hub = hubNearPlayer();
    if (!hub) return;
    // Prefer events tagged for this hub; fallback any
    let pool = cityEvents.filter((e) => e.near === hub.near);
    if (!pool.length) pool = cityEvents;
    // Avoid repeating the same immediately
    pool = pool.filter((e) => e.id !== lastEventId);
    if (!pool.length) pool = cityEvents;
    const ev = pool[Math.floor(Math.random() * pool.length)];
    showEventToast(ev);
  }


  function loadBikePref() {
    try { bikeMode = localStorage.getItem(BIKE_LS_KEY) === "1"; } catch (_) { bikeMode = false; }
  }
  function saveBikePref() {
    try { localStorage.setItem(BIKE_LS_KEY, bikeMode ? "1" : "0"); } catch (_) {}
  }
  function applyBikeUI() {
    if (playerAvatar) {
      playerAvatar.classList.toggle("bike-mode", bikeMode);
      playerAvatar.title = bikeMode ? "Tú (bici)" : "Tú";
    }
    const hud = $("#hud-bike");
    if (hud) {
      hud.textContent = bikeMode ? "🚲 Bici" : "🚶 Andar";
      hud.setAttribute("aria-pressed", bikeMode ? "true" : "false");
      hud.classList.toggle("active-bike", bikeMode);
    }
    applyPlayerAvatarLook();
  }

  /* Avatar Calles: VitaInk ON → Mari lote2 (facing+cycle+night); si no, emoji. */
  function mariAvatarEnabled() {
    return !!(vitainkOn && vitainkAvailable && mariSpritesOk);
  }
  function mariPreferTopView() {
    // Mirador o zoom muy alejado: aproximación cenital (top).
    return vistaMode === "mirador" || (typeof callesZoom === "number" && callesZoom <= 0.85);
  }
  function mariIsNight() {
    return todPhase === "noche";
  }
  function mariFacingAngle() {
    if (mariPreferTopView()) return "top";
    const h = ((playerHeading % 360) + 360) % 360;
    // 0=N, 90=E, 180=S, 270=W — qleft/qright por rumbo E/O; N/S → front.
    if (h >= 45 && h < 135) return "qright";
    if (h >= 225 && h < 315) return "qleft";
    return "front";
  }
  function mariDirFolder(facing) {
    // Night solo tiene front+top; ¾ cae a front de noche.
    if (mariIsNight()) {
      return (facing === "top") ? "top" : "front";
    }
    return facing || "front";
  }
  function mariAngleBase(facing) {
    // v5.7–v5.8.1: avatar pack maestro (day/) si Encarnar activo (discípulo).
    const encId = encarnarMaestroIdActivo();
    if (encId) return maestroAvatarBase(encId, facing);
    const dir = mariDirFolder(facing || mariFacingAngle());
    const tod = mariIsNight() ? "night" : "day";
    let base = mariSkinBase() + "/" + tod + "/" + dir;
    // Nudist/naturalist solo de día y solo en ángulos con asset (probe). Night/qleft/etc → vestida.
    if (
      mariNaturalista &&
      mariNudistPackState === "ok" &&
      mariNudistSubdir &&
      tod === "day" &&
      mariNudistAngles[dir]
    ) {
      base += "/" + mariNudistSubdir;
    }
    return base;
  }
  function mariSintopActive() {
    return !!(mariNaturalista && (mariNudistPackState === "sintop" || mariNudistPackState === "sintop-pose"));
  }
  function mariIdleSrc(facing) {
    if (mariUseGymFallback) return MARI_FALLBACK_IDLE;
    if (mariNaturalista && mariNudistPackState === "sintop") return MARI_SINTOP_DIR + "/idle.png";
    if (mariNaturalista && mariNudistPackState === "sintop-pose") return MARI_SINTOP_POSE_IDLE;
    // v5.17: silueta body-shapes (front/top idle) si hay receta
    const shaped = typeof mariBodyShapesIdleURL === "function" ? mariBodyShapesIdleURL(facing) : "";
    if (shaped) return shaped;
    return mariAngleBase(facing) + "/idle.png";
  }
  function mariWalkLSrc(facing) {
    if (mariUseGymFallback) return MARI_FALLBACK_WALK_L;
    if (mariNaturalista && mariNudistPackState === "sintop") return MARI_SINTOP_DIR + "/walk-L.png";
    if (mariNaturalista && mariNudistPackState === "sintop-pose") return MARI_SINTOP_POSE_IDLE;
    return mariAngleBase(facing) + "/walk-L.png";
  }
  function mariWalkRSrc(facing) {
    if (mariUseGymFallback) return MARI_FALLBACK_WALK_R;
    if (mariNaturalista && mariNudistPackState === "sintop") return MARI_SINTOP_DIR + "/walk-R.png";
    if (mariNaturalista && mariNudistPackState === "sintop-pose") return MARI_SINTOP_POSE_IDLE;
    return mariAngleBase(facing) + "/walk-R.png";
  }
  function mariCycleFrames(facing) {
    if (mariUseGymFallback) return null;
    const f = facing || mariFacingAngle();
    // Pack maestro con day/: cycle front si el registro lo declara.
    const encCyc = encarnarMaestroIdActivo();
    if (encCyc) {
      if (f === "top" || mariIsNight()) return null;
      const pack = maestroPack(encCyc);
      return pack.cycleFront || null;
    }
    if (mariIsNight()) return null;
    if (mariSintopActive()) return null;
    if (mariNaturalista && mariNudistPackState === "ok") {
      if (!mariNudistAngles[f] || !mariNudistHasCycle) return null;
      if (f === "front" && mariNudistCycleFront && mariNudistCycleFront.length) return mariNudistCycleFront;
      return null;
    }
    const list = MARI_CYCLE_WALK[f];
    if (!list || !list.length) return null;
    return list;
  }
  function mariCycleSrc(facing, idx) {
    const frames = mariCycleFrames(facing);
    if (!frames) return "";
    const name = frames[((idx % frames.length) + frames.length) % frames.length];
    return mariAngleBase(facing) + "/cycle/" + name;
  }
  function applyPlayerAvatarLook() {
    if (!playerAvatar) return;
    const encIdLook = encarnarMaestroIdActivo();
    if (encIdLook) ensureMaestroSpriteFolder(encIdLook).catch(() => {});
    else ensureDiabloSpriteFolder().catch(() => {});
    const emo = $("#player-emoji");
    const img = $("#player-mari");
    const useMari = mariAvatarEnabled();
    const facing = mariFacingAngle();
    mariFacingCached = facing;
    playerAvatar.classList.toggle("mari-mode", useMari);
    playerAvatar.classList.toggle("mari-top", useMari && facing === "top" && !mariUseGymFallback);
    // v5.7–v5.8.1: tinte suave «encarnar» si discípulo opt-in (day pack)
    const tintOn = !!encIdLook;
    playerAvatar.classList.toggle("encarnar-maestro", tintOn);
    playerAvatar.classList.toggle("encarnar-diablo", encIdLook === "diablo"); // legacy
    if (tintOn) playerAvatar.style.setProperty("--encarnar-tint", MARI_MAESTRO_TINT[encIdLook] || "#6366f1");
    else playerAvatar.style.removeProperty("--encarnar-tint");
    if (useMari && img) {
      img.classList.remove("hidden");
      if (emo) emo.classList.add("hidden");
      // Idle inmediato; streetLoop anima marcha/cycle al moverse.
      if (!img.getAttribute("src") || img.dataset.frame === "broken" || img.dataset.frame === "idle" || img.dataset.facing !== facing) {
        img.src = mariIdleSrc(facing);
        img.dataset.frame = "idle";
        img.dataset.facing = facing;
      }
      if (!img.dataset.boundErr) {
        img.dataset.boundErr = "1";
        img.addEventListener("error", () => {
          // Ángulo nudist ausente → ese ángulo vestido; no tumbar todo el pack.
          if (mariNaturalista && mariNudistPackState === "ok") {
            const facing = img.dataset.facing || mariFacingAngle();
            const dir = mariDirFolder(facing);
            if (mariNudistAngles[dir]) {
              delete mariNudistAngles[dir];
              img.dataset.frame = "idle";
              img.src = mariIdleSrc(facing);
              if (!Object.keys(mariNudistAngles).length) {
                mariNudistPackState = "missing";
                mariNudistSubdir = "";
                mariNudistHasCycle = false;
                mariNudistCycleFront = null;
                mariMaestroNudistSubdir = "";
              }
              syncNaturalistaUI();
              return;
            }
          }
          if (mariNaturalista && mariSintopActive()) {
            mariNudistPackState = "missing";
            img.dataset.frame = "idle";
            img.src = mariSkinBase() + "/day/front/idle.png";
            syncNaturalistaUI();
            return;
          }
          if (!mariUseGymFallback) {
            mariUseGymFallback = true;
            img.dataset.frame = "idle";
            img.src = MARI_FALLBACK_IDLE;
            return;
          }
          mariSpritesOk = false;
          img.dataset.frame = "broken";
          applyPlayerAvatarLook();
        });
      }
      updateMariWalkFrame(mariMoving);
    } else {
      if (img) img.classList.add("hidden");
      if (emo) {
        emo.classList.remove("hidden");
        emo.textContent = bikeMode ? "🚲" : "🚶";
      } else {
        playerAvatar.textContent = bikeMode ? "🚲" : "🚶";
      }
    }
    // Badge de rostro compuesto (Calles): visible con Mari + receta, oculto si Encarnar maestro
    const faceBadge = $("#player-face-badge");
    if (faceBadge) {
      const showBadge = !!(useMari && mariFaceRecipe && mariFaceRecipe.shape && !encarnarMaestroIdActivo());
      faceBadge.classList.toggle("hidden", !showBadge);
      if (showBadge) composeMariFaceOnto(faceBadge, mariFaceRecipe).catch(() => {});
    }
    // v5.16: capas on-body (o fallback anclas) sobre #player-mari; se oculta con Encarnar
    if (typeof syncMariFaceOnBodyAvatar === "function") {
      syncMariFaceOnBodyAvatar().catch(() => {});
    } else {
      const onBody = $("#player-face-on-body");
      if (onBody) onBody.classList.add("hidden");
    }
  }
  function updateMariWalkFrame(moving) {
    mariMoving = !!moving;
    if (!mariAvatarEnabled()) return;
    const img = $("#player-mari");
    if (!img) return;
    const facing = mariFacingAngle();
    const top = facing === "top" && !mariUseGymFallback;
    playerAvatar && playerAvatar.classList.toggle("mari-top", top);
    if (img.dataset.facing !== facing) {
      img.dataset.facing = facing;
      mariWalkPhase = 0;
      img.dataset.frame = "";
    }
    mariFacingCached = facing;
    if (!moving) {
      const want = mariIdleSrc(facing);
      if (img.dataset.frame !== "idle" || img.getAttribute("src") !== want) {
        img.src = want;
        img.dataset.frame = "idle";
      }
      return;
    }
    const now = performance.now();
    const interval = bikeMode ? 140 : 220;
    const cycle = mariCycleFrames(facing);
    if (!img.dataset.frame || img.dataset.frame === "idle" || (now - mariLastStepAt) > interval) {
      mariLastStepAt = now;
      if (cycle && cycle.length) {
        if (img.dataset.frame === "idle" || !String(img.dataset.frame || "").startsWith("c")) {
          mariWalkPhase = 0;
        } else {
          mariWalkPhase = (mariWalkPhase + 1) % cycle.length;
        }
        img.src = mariCycleSrc(facing, mariWalkPhase);
        img.dataset.frame = "c" + mariWalkPhase;
      } else {
        mariWalkPhase = mariWalkPhase ? 0 : 1;
        img.src = mariWalkPhase ? mariWalkLSrc(facing) : mariWalkRSrc(facing);
        img.dataset.frame = mariWalkPhase ? "L" : "R";
      }
    }
  }

  /* Busts maestros (CLEAN) + tinte; pins en mapa vía botAlmaURL. */
  function maestroBustURL(m) {
    const pack = maestroPack(m || "");
    const folder = maestroFolder(m) || pack.folder;
    if (!folder) return "";
    const prefer = pack.bustPrefer || "front";
    if (prefer === "serio") return MARI_BASE + "/masters/" + folder + "/bust-serio.png";
    if (prefer === "smile") return MARI_BASE + "/masters/" + folder + "/bust-smile.png";
    return MARI_BASE + "/masters/" + folder + "/bust-front.png";
  }
  function maestroPinURL(mOrId) {
    const folder = maestroFolder(mOrId);
    if (!folder) return "";
    // Pins nudist/naturalist solo si el probe los encontró; si no, vestidos.
    if (mariNaturalista && mariMaestroNudistSubdir) {
      return MARI_BASE + "/masters/" + folder + "/" + mariMaestroNudistSubdir + "/pin.png";
    }
    return MARI_BASE + "/masters/" + folder + "/pin.png";
  }
  function maestroHeadURL(m) {
    // Panel: bust CLEAN; legacy heads siguen en disco como último recurso vía onerror→emoji.
    return maestroBustURL(m) || "";
  }
  function maestroTint(m) {
    const id = (m && m.id) ? String(m.id).toLowerCase() : "";
    return MARI_MAESTRO_TINT[id] || "#64748b";
  }
  function bindImgEmojiFallback(img, emoji) {
    if (!img || img.dataset.fallbackBound) return;
    img.dataset.fallbackBound = "1";
    img.addEventListener("error", () => {
      img.classList.add("hidden");
      const span = document.createElement("span");
      span.className = "vita-alma-fallback";
      span.textContent = emoji || "🧭";
      span.setAttribute("aria-hidden", "true");
      if (img.parentNode) img.parentNode.insertBefore(span, img);
    }, { once: true });
  }
  function maestroThumbHTML(m, size) {
    const sz = size || 36;
    const head = maestroHeadURL(m);
    const tint = maestroTint(m);
    const emo = (m && m.emoji) || "🧭";
    if (!head) return `<span class="vita-alma-fallback">${escapeHTML(emo)}</span>`;
    return `<img class="vita-alma-thumb maestro-head" src="${escapeHTML(head)}" alt="" width="${sz}" height="${sz}" loading="lazy" data-emoji="${escapeHTML(emo)}" style="--maestro-tint:${escapeHTML(tint)}">`;
  }
  function wireMaestroThumbFallbacks(root) {
    const box = root || document;
    box.querySelectorAll("img.maestro-head").forEach((img) => {
      bindImgEmojiFallback(img, img.dataset.emoji || "🧭");
    });
  }
  function toggleBikeMode() {
    bikeMode = !bikeMode;
    saveBikePref();
    applyBikeUI();
    setStatus(bikeMode ? "Modo bici · más rápido por calles" : "Modo andar", "ok");
  }

  let missionsSnap = null;
  function loadMissionBadges() {
    try { return JSON.parse(localStorage.getItem(MISSION_BADGES_KEY) || "{}") || {}; }
    catch (_) { return {}; }
  }
  function saveMissionBadge(id, note) {
    const m = loadMissionBadges();
    if (!m[id]) {
      m[id] = { note: note || "", at: Math.floor(Date.now() / 1000) };
      try { localStorage.setItem(MISSION_BADGES_KEY, JSON.stringify(m)); } catch (_) {}
    }
  }
  function updateMissionsHUD(snap) {
    missionsSnap = snap;
    const el = $("#hud-missions-count");
    if (el) el.textContent = (snap.completed || 0) + "/" + (snap.total || 0);
    // persist local badges for newly completed
    for (const m of snap.missions || []) {
      if (m.done) saveMissionBadge(m.id, m.badge || m.title);
    }
    if (homeViewMode === "calles" && placeNodes.length) renderStreetBuildings(placesCache);
  }
  async function refreshMissions() {
    try {
      const snap = await fetchJSON("/api/city/missions");
      updateMissionsHUD(snap);
      return snap;
    } catch (_) {
      const el = $("#hud-missions-count");
      if (el && !missionsSnap) el.textContent = "—";
      return missionsSnap;
    }
  }
  function renderMisionesAlbum(snap) {
    const box = $("#misiones-album");
    const prog = $("#misiones-progress");
    const badges = $("#misiones-badges");
    if (!box) return;
    box.innerHTML = "";
    if (!snap) {
      if (prog) prog.textContent = "—";
      return;
    }
    if (prog) prog.textContent = (snap.completed || 0) + " / " + (snap.total || 0);
    for (const m of snap.missions || []) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "mision-card " + (m.done ? "done" : "open");
      btn.setAttribute("role", "listitem");
      btn.innerHTML =
        `<span class="mision-title">${escapeHTML(m.title || m.id)}</span>` +
        `<span class="mision-body">${escapeHTML(m.body || "")}</span>` +
        `<span class="mision-prog">${m.current || 0} / ${m.target || 0}</span>` +
        (m.done ? `<span class="mision-badge">${escapeHTML(m.badge || "Completada")}</span>` : "");
      if (m.kind === "places" && Array.isArray(m.place_ids) && m.place_ids.length) {
        btn.addEventListener("click", () => openPlace(m.place_ids[0]).catch(() => {}));
      } else {
        btn.addEventListener("click", () => showSellos().catch(() => {}));
      }
      box.appendChild(btn);
    }
    if (badges) {
      const local = loadMissionBadges();
      const notes = Object.keys(local).map((k) => local[k].note || k).filter(Boolean);
      badges.textContent = notes.length ? ("Insignias locales: " + notes.join(" · ")) : "Sin insignias aún — completa misiones visitando lugares.";
    }
  }
  async function showMisiones() {
    stopPoll();
    hideAllViews();
    if (viewMisiones) viewMisiones.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = "Misiones cívicas";
    subtitle.textContent = "Progreso desde sellos · sin nube";
    setNav("lugares");
    const snap = await refreshMissions();
    renderMisionesAlbum(snap || missionsSnap);
    history.pushState({ view: "misiones" }, "", "/misiones");
  }

  function vignetteSkipEnabled() {
    try { return localStorage.getItem(VIGNETTE_SKIP_KEY) === "1"; } catch (_) { return false; }
  }
  function setVignetteSkip(on) {
    try {
      if (on) localStorage.setItem(VIGNETTE_SKIP_KEY, "1");
      else localStorage.removeItem(VIGNETTE_SKIP_KEY);
    } catch (_) {}
  }

  /** Aplica clase CSS theme-* y banner de sabor (v4.7). Sin marcas ajenas. */
  function applyPlaceTheme(el, page) {
    if (!el) return;
    const toRemove = [];
    el.classList.forEach((c) => { if (c.indexOf("theme-") === 0) toRemove.push(c); });
    toRemove.forEach((c) => el.classList.remove(c));
    const theme = (page && page.theme) || "";
    const banner = $("#place-theme-banner");
    if (theme) {
      el.classList.add("theme-" + theme);
      if (banner) {
        const label = (page.theme_label || "").trim();
        const flavor = (page.theme_flavor || "").trim();
        banner.textContent = label ? (label + (flavor ? " · " + flavor : "")) : flavor;
        banner.classList.toggle("hidden", !banner.textContent);
      }
    } else if (banner) {
      banner.textContent = "";
      banner.classList.add("hidden");
    }
    // v5.8: capas ambient CSS (polvo, hojas) según theme — sin vídeo pesado
    fillPlaceAmbient(el, theme);
  }

  /** Rellena .place-ambient con motas/hojas (solo transform/opacity vía CSS). */
  function fillPlaceAmbient(el, theme) {
    if (!el) return;
    const layer = el.querySelector(".place-ambient");
    if (!layer) return;
    layer.innerHTML = "";
    if (!theme) return;
    const n = 6;
    if (theme === "torre-academia" || theme === "cultura") {
      for (let i = 0; i < n; i++) {
        const m = document.createElement("span");
        m.className = "dust-mote";
        m.style.left = (8 + (i * 14) % 84) + "%";
        m.style.top = (18 + (i * 11) % 60) + "%";
        layer.appendChild(m);
      }
    } else if (theme === "jardin") {
      for (let i = 0; i < 3; i++) {
        const leaf = document.createElement("span");
        leaf.className = "leaf";
        leaf.style.left = (20 + i * 25) + "%";
        leaf.style.top = (10 + i * 8) + "%";
        layer.appendChild(leaf);
      }
    }
  }

  function presentVignette(place) {
    return new Promise(async (resolve) => {
      const overlay = $("#place-vignette");
      if (!overlay || vignetteSkipEnabled()) {
        resolve();
        return;
      }
      let flavor = "Entras en " + (place.name || "el lugar") + ".";
      try {
        const v = await fetchJSON("/api/city/vignette?place_id=" + encodeURIComponent(place.id || ""));
        if (v && v.flavor) flavor = v.flavor;
        if (v && v.skip_key) { /* server hint; we keep VIGNETTE_SKIP_KEY */ }
      } catch (_) {}
      $("#vignette-emoji").textContent = place.emoji || "📍";
      $("#vignette-name").textContent = place.name || place.id || "Lugar";
      $("#vignette-flavor").textContent = flavor;
      // Tema de viñeta (Biblioteca = torre-academia)
      const vcard = $("#vignette-card") || overlay.querySelector(".vignette-card");
      if (vcard) {
        ["theme-torre-academia"].forEach((c) => vcard.classList.remove(c));
        if ((place.id || "") === "biblioteca-publica") vcard.classList.add("theme-torre-academia");
      }
      const dont = $("#vignette-dont-show");
      if (dont) dont.checked = false;
      overlay.classList.remove("hidden");
      const finish = () => {
        if (dont && dont.checked) setVignetteSkip(true);
        overlay.classList.add("hidden");
        resolve();
      };
      const enter = $("#vignette-enter");
      const skip = $("#vignette-skip-once");
      const onEnter = () => { cleanup(); finish(); };
      const onSkip = () => { cleanup(); finish(); };
      function cleanup() {
        if (enter) enter.removeEventListener("click", onEnter);
        if (skip) skip.removeEventListener("click", onSkip);
      }
      if (enter) enter.addEventListener("click", onEnter);
      if (skip) skip.addEventListener("click", onSkip);
    });
  }


  function isPlaceStamped(placeId) {
    if (!placeId) return false;
    try {
      const local = localStampsMap();
      if (local[placeId]) return true;
    } catch (_) {}
    if (stampsAlbum && Array.isArray(stampsAlbum.entries)) {
      const e = stampsAlbum.entries.find((x) => x.place_id === placeId);
      if (e && e.collected) return true;
    }
    return false;
  }

  function isMissionTarget(placeId) {
    if (!placeId || !missionsSnap || !Array.isArray(missionsSnap.missions)) return false;
    for (const m of missionsSnap.missions) {
      if (m.done) continue;
      if (Array.isArray(m.place_ids) && m.place_ids.indexOf(placeId) >= 0) return true;
    }
    return false;
  }

  function loadVistaPref() {
    try {
      const v = localStorage.getItem(VISTA_LS_KEY);
      if (v === "planta" || v === "inclinada" || v === "mirador") vistaMode = v;
    } catch (_) {}
  }
  function saveVistaPref() {
    try { localStorage.setItem(VISTA_LS_KEY, vistaMode); } catch (_) {}
  }
  function applyVista() {
    if (!cityStreets) return;
    cityStreets.classList.remove("vista-planta", "vista-inclinada", "vista-mirador");
    cityStreets.classList.add("vista-" + vistaMode);
    const hud = $("#hud-vista");
    const labels = { planta: "👁️ Planta", inclinada: "📐 Inclinada", mirador: "🔭 Mirador" };
    if (hud) hud.textContent = labels[vistaMode] || "👁️ Vista";
    document.querySelectorAll(".vista-choice").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.vista === vistaMode);
    });
    updateFollowCamera();
  }
  function setVista(mode) {
    if (mode !== "planta" && mode !== "inclinada" && mode !== "mirador") return;
    vistaMode = mode;
    saveVistaPref();
    applyVista();
    applyPlayerAvatarLook();
    setStatus("Vista · " + mode, "ok");
  }
  function openVistaPanel() {
    const panel = $("#vista-panel");
    if (!panel) return;
    applyVista();
    panel.classList.remove("hidden");
  }
  function closeVistaPanel() {
    const panel = $("#vista-panel");
    if (panel) panel.classList.add("hidden");
  }

  function loadCapasPref() {
    try {
      const raw = localStorage.getItem(CAPAS_LS_KEY);
      if (raw) {
        const o = JSON.parse(raw);
        capasState = Object.assign(capasState, o);
      }
    } catch (_) {}
    // VitaInk default OFF; prefer dedicated key, fall back to capasState.vitaink
    try {
      let v = localStorage.getItem(VITAINK_LS_KEY);
      if (v !== "1" && v !== "0") v = localStorage.getItem("rcv_vitaink_v31");
      if (v === "1" || v === "0") vitainkOn = v === "1";
      else vitainkOn = !!capasState.vitaink;
    } catch (_) {
      vitainkOn = !!capasState.vitaink;
    }
    capasState.vitaink = vitainkOn;
  }
  function saveCapasPref() {
    capasState.vitaink = vitainkOn;
    try { localStorage.setItem(CAPAS_LS_KEY, JSON.stringify(capasState)); } catch (_) {}
    try { localStorage.setItem(VITAINK_LS_KEY, vitainkOn ? "1" : "0"); } catch (_) {}
  }
  function applyCapas() {
    if (!cityStreets) return;
    cityStreets.classList.toggle("capa-off-paradas", !capasState.paradas);
    cityStreets.classList.toggle("capa-off-bancos", !capasState.bancos);
    cityStreets.classList.toggle("capa-off-sellos", !capasState.sellos);
    cityStreets.classList.toggle("capa-off-misiones", !capasState.misiones);
    cityStreets.classList.toggle("capa-off-clima", !capasState.clima);
    cityStreets.classList.toggle("capa-vitaink-on", !!vitainkOn);
    const hud = $("#hud-capas");
    if (hud) hud.classList.toggle("capas-active", !capasState.paradas || !capasState.bancos || !capasState.sellos || !capasState.misiones || !capasState.clima || vitainkOn);
    const map = {
      "capa-paradas": "paradas",
      "capa-bancos": "bancos",
      "capa-sellos": "sellos",
      "capa-misiones": "misiones",
      "capa-clima": "clima",
    };
    for (const id of Object.keys(map)) {
      const el = $("#" + id);
      if (el) el.checked = !!capasState[map[id]];
    }
    const cv = $("#capa-vitaink");
    if (cv) cv.checked = !!vitainkOn;
    updateVitainkHUD();
    applyPlayerAvatarLook();
  }

  /* —— v5.1 zoom / fullscreen / modo juego limpio —— */
  function loadCallesZoomPref() {
    try {
      const raw = localStorage.getItem(CALLES_ZOOM_LS_KEY);
      const n = raw != null ? parseFloat(raw) : 1;
      if (isFinite(n)) callesZoom = Math.min(CALLES_ZOOM_MAX, Math.max(CALLES_ZOOM_MIN, n));
    } catch (_) { callesZoom = 1; }
  }
  function saveCallesZoomPref() {
    try { localStorage.setItem(CALLES_ZOOM_LS_KEY, String(callesZoom)); } catch (_) {}
  }
  function loadJuegoLimpioPref() {
    try { juegoLimpio = localStorage.getItem(JUEGO_LIMPIO_LS_KEY) === "1"; } catch (_) { juegoLimpio = false; }
  }
  function saveJuegoLimpioPref() {
    try { localStorage.setItem(JUEGO_LIMPIO_LS_KEY, juegoLimpio ? "1" : "0"); } catch (_) {}
  }
  function loadNaturalistaPref() {
    try { mariNaturalista = localStorage.getItem(NATURALISTA_LS_KEY) === "1"; } catch (_) { mariNaturalista = false; }
  }
  function saveNaturalistaPref() {
    try { localStorage.setItem(NATURALISTA_LS_KEY, mariNaturalista ? "1" : "0"); } catch (_) {}
  }
  function mariUrlExists(url) {
    return new Promise((resolve) => {
      const im = new Image();
      im.onload = () => resolve(true);
      im.onerror = () => resolve(false);
      im.src = url;
    });
  }
  function syncNaturalistaUI() {
    const cb = $("#vitaink-pj-naturalista");
    if (cb) cb.checked = !!mariNaturalista;
    const note = $("#vitaink-pj-naturalista-note");
    if (!note) return;
    if (!mariNaturalista) {
      note.textContent = "Por defecto: pack vestido. Opción de juego adulto (cubierta vegetal) · no sexualiza.";
      return;
    }
    if (mariNudistPackState === "ok") {
      const angs = Object.keys(mariNudistAngles).join(",") || "—";
      note.textContent = "Pack «" + mariNudistSubdir + "» · cuerpo " + mariBodySkinId() + " (" + angs + ") · hoja naturalista · solo avatar VitaInk.";
    } else if (mariNudistPackState === "sintop" || mariNudistPackState === "sintop-pose") {
      note.textContent = "Usando sintop (mari-gym) · pack nudist/naturalist aún no instalado.";
    } else if (mariNudistPackState === "probing") {
      note.textContent = "Buscando pack naturalista…";
    } else {
      note.textContent = "Pack naturalista no encontrado · se mantiene vestimenta (fallback).";
    }
  }
  async function refreshMariNaturalistaPack() {
    mariNudistSubdir = "";
    mariNudistHasCycle = false;
    mariNudistCycleFront = null;
    mariNudistAngles = Object.create(null);
    mariMaestroNudistSubdir = "";
    if (!mariNaturalista) {
      mariNudistPackState = "off";
      mariUseGymFallback = false;
      syncNaturalistaUI();
      applyPlayerAvatarLook();
      if (typeof renderVitainkBots === "function") renderVitainkBots();
      return;
    }
    mariNudistPackState = "probing";
    syncNaturalistaUI();
    const skinBase = mariSkinBase(); // skin-01..04 según FaceRecipe (mapa face_skin_align)
    const dayFront = skinBase + "/day/front";
    let found = "";
    // Prefer nudist/ (leaf naturalist pack), then naturalist/
    for (const sub of MARI_NUDIST_SUBDIRS) {
      if (await mariUrlExists(dayFront + "/" + sub + "/idle.png")) {
        found = sub;
        break;
      }
    }
    if (found) {
      mariNudistSubdir = found;
      mariNudistPackState = "ok";
      const angleDirs = ["front", "top", "qleft", "qright", "back", "profile-L", "profile-R"];
      for (const dir of angleDirs) {
        if (await mariUrlExists(skinBase + "/day/" + dir + "/" + found + "/idle.png")) {
          mariNudistAngles[dir] = true;
        }
      }
      const cIdle = dayFront + "/" + found + "/cycle/f0-idle.png";
      const c0 = dayFront + "/" + found + "/cycle/f0.png";
      if (await mariUrlExists(cIdle)) {
        mariNudistHasCycle = true;
        mariNudistCycleFront = ["f0-idle.png", "f1.png", "f2.png", "f3.png"];
      } else if (await mariUrlExists(c0)) {
        mariNudistHasCycle = true;
        mariNudistCycleFront = ["f0.png", "f1.png", "f2.png", "f3.png"];
      }
      if (await mariUrlExists(MARI_BASE + "/masters/angel/" + found + "/pin.png")) {
        mariMaestroNudistSubdir = found;
      }
    } else if (await mariUrlExists(MARI_SINTOP_DIR + "/idle.png")) {
      // sintop from-mari-gym SOLO detrás del toggle
      mariNudistPackState = "sintop";
    } else if (await mariUrlExists(MARI_SINTOP_POSE_IDLE)) {
      mariNudistPackState = "sintop-pose";
    } else {
      mariNudistPackState = "missing";
    }
    if (!mariMaestroNudistSubdir) {
      for (const sub of MARI_NUDIST_SUBDIRS) {
        if (await mariUrlExists(MARI_BASE + "/masters/angel/" + sub + "/pin.png")) {
          mariMaestroNudistSubdir = sub;
          break;
        }
      }
    }
    mariUseGymFallback = false;
    syncNaturalistaUI();
    applyPlayerAvatarLook();
    if (typeof renderVitainkBots === "function") renderVitainkBots();
  }
  async function setMariNaturalista(on) {
    mariNaturalista = !!on;
    saveNaturalistaPref();
    await refreshMariNaturalistaPack();
    setStatus(
      mariNaturalista
        ? (mariNudistPackState === "ok" || mariSintopActive()
          ? "Modo naturalista ON"
          : "Modo naturalista ON · sin pack (vestida)")
        : "Modo naturalista OFF · vestida",
      "ok"
    );
  }
  function setCallesZoom(z, opts) {
    const silent = opts && opts.silent;
    let n = typeof z === "number" ? z : parseFloat(z);
    if (!isFinite(n)) n = 1;
    callesZoom = Math.min(CALLES_ZOOM_MAX, Math.max(CALLES_ZOOM_MIN, Math.round(n * 100) / 100));
    saveCallesZoomPref();
    updateFollowCamera();
    applyPlayerAvatarLook();
    if (!silent) setStatus("Zoom Calles · " + Math.round(callesZoom * 100) + "%", "ok");
  }
  function bumpCallesZoom(dir) {
    setCallesZoom(callesZoom + (dir < 0 ? -CALLES_ZOOM_STEP : CALLES_ZOOM_STEP));
  }
  function applyJuegoLimpio() {
    const on = !!(vitainkOn && vitainkAvailable && juegoLimpio);
    if (cityStreets) cityStreets.classList.toggle("modo-juego-limpio", on);
    const hud = $("#city-hud");
    if (hud) hud.classList.toggle("hud-compact", on);
    document.body.classList.toggle("juego-limpio-on", on);
    const nav = $("#main-nav");
    if (nav) {
      nav.classList.toggle("nav-collapsed-limpio", on);
      nav.setAttribute("aria-hidden", on ? "true" : "false");
    }
    const btn = $("#hud-juego-limpio");
    if (btn) {
      btn.classList.toggle("hidden", !(vitainkOn && vitainkAvailable));
      btn.classList.toggle("limpio-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.textContent = on ? "🎮 Solo VitaInk" : "👁️ Ocultar cívico";
      btn.title = on
        ? "Modo juego limpio ON · toca para mostrar de nuevo el ruido cívico"
        : "Ocultar paradas, bancos, sellos, nav inferior y compactar HUD (modo juego)";
    }
    const toast = $("#event-toast");
    if (toast) toast.classList.toggle("limpio-hide", on);
  }
  function setJuegoLimpio(on) {
    juegoLimpio = !!on;
    saveJuegoLimpioPref();
    applyJuegoLimpio();
    setStatus(juegoLimpio && vitainkOn ? "Modo juego limpio ON" : "Ruido cívico visible", "ok");
  }
  function isCallesFullscreen() {
    const fs = document.fullscreenElement || document.webkitFullscreenElement;
    if (fs && cityStreets && (fs === cityStreets || cityStreets.contains(fs))) return true;
    return !!callesFsFallback;
  }
  function syncFullscreenBtn() {
    const btn = $("#hud-fullscreen");
    const on = isCallesFullscreen();
    if (btn) {
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.title = on ? "Salir de pantalla completa (Esc)" : "Pantalla completa";
      btn.setAttribute("aria-label", on ? "Salir de pantalla completa" : "Pantalla completa");
    }
    const exitBtn = $("#calles-fs-exit");
    if (exitBtn) exitBtn.classList.toggle("hidden", !on);
    if (cityStreets) cityStreets.classList.toggle("calles-fs-fallback", !!callesFsFallback);
    document.documentElement.classList.toggle("calles-fs-active", on);
  }
  async function toggleCallesFullscreen() {
    if (!cityStreets) return;
    try {
      if (isCallesFullscreen()) {
        if (callesFsFallback) {
          callesFsFallback = false;
        } else if (document.exitFullscreen) {
          await document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen();
        }
      } else {
        let ok = false;
        try {
          if (cityStreets.requestFullscreen) {
            await cityStreets.requestFullscreen();
            ok = true;
          } else if (cityStreets.webkitRequestFullscreen) {
            cityStreets.webkitRequestFullscreen();
            ok = true;
          }
        } catch (err) {
          ok = false;
          setStatus("Pantalla completa bloqueada · usando maximizado", "err");
        }
        if (!ok) {
          // Fallback CSS maximize (iOS / política del navegador)
          callesFsFallback = true;
          setStatus("Maximizado (fallback) · toca ✕ para salir", "ok");
        }
      }
    } catch (e) {
      callesFsFallback = !callesFsFallback;
      setStatus((e && e.message) || "Maximizado (fallback)", callesFsFallback ? "ok" : "err");
    }
    syncFullscreenBtn();
  }
  function bindCallesTools() {
    bindAdventureHUD();
    loadCallesZoomPref();
    loadJuegoLimpioPref();
    loadNaturalistaPref();
    refreshMariNaturalistaPack().catch(() => {});
    applyJuegoLimpio();
    updateFollowCamera();
    const zin = $("#hud-zoom-in");
    const zout = $("#hud-zoom-out");
    if (zin) zin.addEventListener("click", () => bumpCallesZoom(1));
    if (zout) zout.addEventListener("click", () => bumpCallesZoom(-1));
    const fs = $("#hud-fullscreen");
    if (fs) fs.addEventListener("click", () => { toggleCallesFullscreen().catch(() => {}); });
    document.addEventListener("fullscreenchange", () => { syncFullscreenBtn(); updateFollowCamera(); });
    document.addEventListener("webkitfullscreenchange", () => { syncFullscreenBtn(); updateFollowCamera(); });
    const fsExit = $("#calles-fs-exit");
    if (fsExit) fsExit.addEventListener("click", () => { toggleCallesFullscreen().catch(() => {}); });
    document.addEventListener("keydown", (ev) => {
      if (ev.key === "Escape" && callesFsFallback) {
        callesFsFallback = false;
        syncFullscreenBtn();
      }
    });
    const limpio = $("#hud-juego-limpio");
    if (limpio) {
      limpio.addEventListener("click", () => {
        if (!(vitainkOn && vitainkAvailable)) return;
        setJuegoLimpio(!juegoLimpio);
      });
    }
    // Pellizco opcional (2 dedos) sobre Calles
    if (cityStreets) {
      let pinch0 = 0;
      let zoom0 = 1;
      cityStreets.addEventListener("touchstart", (e) => {
        if (!e.touches || e.touches.length !== 2) { pinch0 = 0; return; }
        const a = e.touches[0], b = e.touches[1];
        pinch0 = Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);
        zoom0 = callesZoom;
      }, { passive: true });
      cityStreets.addEventListener("touchmove", (e) => {
        if (!pinch0 || !e.touches || e.touches.length !== 2) return;
        const a = e.touches[0], b = e.touches[1];
        const d = Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);
        if (d < 8) return;
        setCallesZoom(zoom0 * (d / pinch0), { silent: true });
      }, { passive: true });
      cityStreets.addEventListener("touchend", () => { pinch0 = 0; }, { passive: true });
      cityStreets.addEventListener("touchcancel", () => { pinch0 = 0; }, { passive: true });
    }
  }

  function updateVitainkHUD() {
    const show = !!(vitainkAvailable && vitainkOn);
    const hud = $("#hud-vitaink");
    if (hud) {
      hud.classList.toggle("hidden", !vitainkAvailable);
      hud.classList.toggle("vitaink-active", !!show);
      hud.setAttribute("aria-pressed", show ? "true" : "false");
      hud.textContent = show ? "🎮 VitaInk ON" : "🎮 VitaInk";
      hud.title = !vitainkAvailable
        ? "VitaInk no montado en este nodo"
        : (show ? "VitaInk ON · LARP virtual (solo puntos)" : "VitaInk OFF · red ciudadana pura");
    }
    const pjHud = $("#hud-vitaink-pj");
    if (pjHud) {
      pjHud.classList.toggle("hidden", !show);
      if (show && vitainkPersonaje && vitainkPersonaje.exists) {
        const lab = vitainkPersonaje.reputacion_label || "Reputación";
        const n = vitainkPersonaje.reputacion != null ? vitainkPersonaje.reputacion : 0;
        pjHud.textContent = (vitainkPersonaje.faccion_emoji || "🧍") + " " + (vitainkPersonaje.nombre || "Personaje") + " · " + lab + " " + n;
      } else if (show) {
        pjHud.textContent = "🧍 Personaje";
      }
    }
    const tesHud = $("#hud-vitaink-tesoros");
    if (tesHud) tesHud.classList.toggle("hidden", !show);
    const misHud = $("#hud-vitaink-misiones");
    if (misHud) misHud.classList.toggle("hidden", !show);
    const rankHud = $("#hud-vitaink-ranking");
    if (rankHud) rankHud.classList.toggle("hidden", !show);
    const diosHud = $("#hud-vitaink-dios");
    if (diosHud) {
      diosHud.classList.toggle("hidden", !show);
      diosHud.classList.toggle("dios-ok", !!(show && vitainkDiosOk));
      diosHud.title = vitainkDiosOk ? "Panel Dios (PIN OK)" : "Panel Dios (requiere PIN operador)";
    }
    const maeHud = $("#hud-vitaink-maestros");
    if (maeHud) maeHud.classList.toggle("hidden", !show);
    const relHud = $("#hud-vitaink-reliquias");
    if (relHud) relHud.classList.toggle("hidden", !show);
    const synHud = $("#hud-vitaink-sinodo");
    if (synHud) synHud.classList.toggle("hidden", !show);
    const ritoHud = $("#hud-vitaink-rito");
    if (ritoHud) ritoHud.classList.toggle("hidden", !show);
    const perHud = $("#hud-vitaink-peregrinacion");
    if (perHud) perHud.classList.toggle("hidden", !show);
    const codHud = $("#hud-vitaink-codice");
    if (codHud) codHud.classList.toggle("hidden", !show);
    const croHud = $("#hud-vitaink-cronica");
    if (croHud) croHud.classList.toggle("hidden", !show);
    const capaLi = $("#capa-vitaink");
    if (capaLi && capaLi.closest) {
      const row = capaLi.closest("li");
      if (row) {
        row.classList.toggle("capa-vitaink-missing", !vitainkAvailable);
        row.classList.toggle("hidden", !vitainkAvailable);
      }
      capaLi.disabled = !vitainkAvailable;
    }
    const note = $("#capa-vitaink-note");
    if (note) note.classList.toggle("hidden", !vitainkAvailable);
    applyJuegoLimpio();
    updateAdventureHUD();
  }

  /* —— v5.18 HUD aventura Calles (iconos lote 1) ——
     Qué: franja ligera corazones/stamina/monedas + atajos quest/torre/inventario.
     Cuándo: solo VitaInk ON; se oculta en modo cívico (VitaInk OFF).
     Salud/resistencia: stub visual (sin campos en personaje aún).
     Monedas: desde vitainkPersonaje.monedas si existe.
     Preferencia SVG; onerror → PNG 128. */
  const VAH_HUD_BASE = "/vitaink/sprites/hud";
  const VAH_HEARTS_MAX = 5;
  let adventureHudBound = false;

  function vahIconURL(name, ext) {
    if (ext === "png") return VAH_HUD_BASE + "/png/128/" + name + ".png";
    return VAH_HUD_BASE + "/svg/" + name + ".svg";
  }
  function vahBindIconFallback(img) {
    if (!img || img.dataset.hudFallbackBound) return;
    img.dataset.hudFallbackBound = "1";
    img.addEventListener("error", () => {
      const id = img.getAttribute("data-hud-icon");
      if (!id) return;
      if (img.dataset.hudTriedPng === "1") return;
      img.dataset.hudTriedPng = "1";
      img.src = vahIconURL(id, "png");
    });
  }
  function vahEnsureIconFallbacks(root) {
    if (!root) return;
    root.querySelectorAll("img[data-hud-icon]").forEach(vahBindIconFallback);
  }
  function vahHeartState(i, filled) {
    // i 0-based; filled = cuantos llenos
    return i < filled ? "heart-full" : "heart-empty";
  }
  function vahStaminaName(level) {
    // level: 0 vacío, 1 medio, 2 lleno (stub)
    if (level <= 0) return "stamina-empty";
    if (level === 1) return "stamina-half";
    return "stamina-full";
  }
  function updateAdventureHUD() {
    const el = $("#vitaink-adventure-hud");
    if (!el) return;
    const show = !!(vitainkAvailable && vitainkOn);
    el.classList.toggle("hidden", !show);
    if (show) el.removeAttribute("hidden");
    else el.setAttribute("hidden", "");
    if (!show) return;

    vahEnsureIconFallbacks(el);

    // Vitales stub: 5 corazones llenos si hay personaje; 3 si no.
    // Stamina: llena con personaje; media sin ficha.
    const hasPj = !!(vitainkPersonaje && vitainkPersonaje.exists);
    const heartsFilled = hasPj ? VAH_HEARTS_MAX : 3;
    const staminaLevel = hasPj ? 2 : 1;

    const hearts = $("#vah-hearts");
    if (hearts) {
      let html = "";
      for (let i = 0; i < VAH_HEARTS_MAX; i++) {
        const id = vahHeartState(i, heartsFilled);
        html += '<img class="vah-icon" src="' + vahIconURL(id, "svg") + '" width="36" height="36" alt="" aria-hidden="true" data-hud-icon="' + id + '">';
      }
      hearts.innerHTML = html;
      hearts.setAttribute("aria-label", "Salud " + heartsFilled + " de " + VAH_HEARTS_MAX);
      vahEnsureIconFallbacks(hearts);
    }
    const stam = $("#vah-stamina");
    if (stam) {
      const id = vahStaminaName(staminaLevel);
      stam.innerHTML = '<img class="vah-icon" src="' + vahIconURL(id, "svg") + '" width="36" height="36" alt="" aria-hidden="true" data-hud-icon="' + id + '">';
      stam.setAttribute("aria-label", "Resistencia " + (staminaLevel === 2 ? "llena" : staminaLevel === 1 ? "media" : "vacía"));
      vahEnsureIconFallbacks(stam);
    }
    const coins = $("#vah-coin-count");
    if (coins) {
      if (hasPj && vitainkPersonaje.monedas != null) {
        coins.textContent = String(vitainkPersonaje.monedas);
      } else {
        coins.textContent = "—";
      }
    }
  }
  function bindAdventureHUD() {
    if (adventureHudBound) return;
    adventureHudBound = true;
    const q = $("#vah-btn-quest");
    if (q) q.addEventListener("click", () => {
      if (!(vitainkOn && vitainkAvailable)) return;
      openVitainkMisiones().catch(() => {});
    });
    const t = $("#vah-btn-tower");
    if (t) t.addEventListener("click", () => {
      if (!(vitainkOn && vitainkAvailable)) return;
      openVitainkRanking().catch(() => {});
    });
    const inv = $("#vah-btn-inventory");
    if (inv) inv.addEventListener("click", () => {
      if (!(vitainkOn && vitainkAvailable)) return;
      openVitainkPjPanel().catch(() => {});
    });
    vahEnsureIconFallbacks($("#vitaink-adventure-hud"));
  }
  function factionMeta(id) {
    const list = (vitainkMapa && vitainkMapa.factions) || [];
    for (const f of list) if (f.id === id) return f;
    return { id: id || "libre", name: "Libre", color: "#94a3b8", emoji: "🕊️" };
  }
  function indexVitainkMapa(snap) {
    vitainkMapa = snap || null;
    vitainkByPlace = Object.create(null);
    vitainkCasas = (snap && snap.casas) || [];
    vitainkBots = (snap && Array.isArray(snap.bots)) ? snap.bots : [];
    vitainkErmitas = (snap && Array.isArray(snap.ermitas)) ? snap.ermitas : [];
    if (snap && Array.isArray(snap.tesoros)) {
      vitainkTesoros = snap.tesoros;
    }
    if (!snap || !snap.ownerships) return;
    for (const o of snap.ownerships) {
      const f = factionMeta(o.faction_id);
      const libre = !o.faction_id || o.faction_id === "libre" || /libre/i.test(o.owner_label || "");
      vitainkByPlace[o.place_id] = {
        faction_id: o.faction_id,
        faction_name: f.name,
        color: f.color,
        emoji: libre ? "🕊️" : (f.emoji || "🎮"),
        owner_label: o.owner_label,
        monedas_sede: o.monedas_sede,
        libre: libre,
      };
    }
  }
  async function fetchVitainkMapa() {
    try {
      const snap = await fetchJSON("/api/vitaink/mapa");
      indexVitainkMapa(snap);
      renderVitainkCasas();
      if (vitainkOn) fetchVitainkPeregrinacion().catch(() => {});
      renderVitainkTesoros();
      renderVitainkBots();
      renderVitainkErmitas();
      return snap;
    } catch (_) {
      vitainkMapa = null;
      vitainkByPlace = Object.create(null);
      vitainkCasas = [];
      vitainkTesoros = [];
      vitainkBots = [];
      vitainkErmitas = [];
      renderVitainkCasas();
      renderVitainkTesoros();
      renderVitainkBots();
      renderVitainkErmitas();
      return null;
    }
  }
  function mirrorPersonajeLS(p) {
    try {
      if (p && p.exists) localStorage.setItem(VITAINK_PJ_LS_KEY, JSON.stringify({
        nombre: p.nombre, faccion_id: p.faccion_id, monedas: p.monedas,
        reputacion: p.reputacion, reputacion_label: p.reputacion_label,
        face: p.face || null
      }));
    } catch (_) {}
  }
  async function fetchVitainkPersonaje() {
    try {
      const data = await fetchJSON("/api/vitaink/personaje");
      vitainkPersonaje = data.personaje || null;
      if (vitainkPersonaje && vitainkPersonaje.face) {
        mariFaceRecipe = Object.assign({}, MARI_FACE_DEFAULT, vitainkPersonaje.face);
      }
      if (vitainkPersonaje && vitainkPersonaje.body) {
        mariBodyRecipe = Object.assign({}, MARI_BODY_DEFAULT, vitainkPersonaje.body);
      } else if (vitainkPersonaje && vitainkPersonaje.exists) {
        mariBodyRecipe = Object.assign({}, MARI_BODY_DEFAULT);
      }
      mirrorPersonajeLS(vitainkPersonaje);
      updateVitainkHUD();
      refreshMariFacePreviews().catch(() => {});
      return data;
    } catch (_) {
      vitainkPersonaje = null;
      return null;
    }
  }
  function renderVitainkCasas() {
    const box = $("#street-vitaink-casas");
    if (!box) return;
    box.innerHTML = "";
    if (!vitainkOn || !vitainkCasas.length) return;
    for (const c of vitainkCasas) {
      const f = factionMeta(c.faction_id);
      const libre = !c.faction_id || c.faction_id === "libre" || /libre/i.test(c.owner_label || "");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vita-casa-pin";
      btn.style.left = Math.max(4, Math.min(96, c.x)) + "%";
      btn.style.top = Math.max(4, Math.min(96, c.y)) + "%";
      btn.style.setProperty("--vita-color", f.color || "#94a3b8");
      btn.title = (c.label || "Casa") + " · " + (libre ? "Libre" : (c.owner_label || f.name));
      btn.setAttribute("aria-label", c.label || "Casa VitaInk");
      btn.innerHTML =
        `<span class="pin-emoji" aria-hidden="true">${escapeHTML(c.emoji || "🏠")}</span>` +
        `<span class="pin-name">${escapeHTML(c.label || "")}</span>` +
        `<span class="pin-vitaink" aria-hidden="true">${escapeHTML(libre ? "🕊️" : (f.emoji || "🎮"))}</span>`;
      btn.addEventListener("click", (ev) => {
        ev.stopPropagation();
        openVitainkCasa(c.id).catch(() => {});
      });
      box.appendChild(btn);
    }
  }
  function renderVitainkTesoros() {
    const box = $("#street-vitaink-tesoros");
    if (!box) return;
    box.innerHTML = "";
    if (!vitainkOn || !vitainkAvailable || !vitainkTesoros.length) return;
    for (const tr of vitainkTesoros) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vita-tesoro-pin" + (tr.claimed ? " claimed" : "");
      btn.dataset.tesoroId = tr.id;
      btn.style.left = Math.max(4, Math.min(96, tr.x)) + "%";
      btn.style.top = Math.max(4, Math.min(96, tr.y)) + "%";
      btn.title = (tr.label || "Tesoro") + (tr.claimed ? " · reclamado" : " · acércate para reclamar");
      btn.setAttribute("aria-label", tr.label || "Tesoro VitaInk");
      btn.textContent = tr.emoji || "💎";
      btn.addEventListener("click", (ev) => {
        ev.stopPropagation();
        if (tr.claimed) {
          setStatus("Tesoro ya reclamado", "ok");
          return;
        }
        if (nearTesoroId === tr.id) reclamarTesoroCercano(tr.id).catch(() => {});
        else setStatus("Acércate para reclamar el tesoro", "ok");
      });
      box.appendChild(btn);
    }
  }
  async function probeVitaink() {
    try {
      const est = await fetchJSON("/api/vitaink/estado");
      vitainkAvailable = !!(est && est.layer === "vitaink");
    } catch (_) {
      vitainkAvailable = false;
    }
    if (!vitainkAvailable) {
      vitainkOn = false;
      capasState.vitaink = false;
      try { localStorage.setItem(VITAINK_LS_KEY, "0"); } catch (_) {}
    }
    updateVitainkHUD();
    return vitainkAvailable;
  }
  async function fetchVitainkTesoros() {
    if (!vitainkAvailable) return null;
    try {
      const snap = await fetchJSON("/api/vitaink/tesoros");
      vitainkTesoros = (snap && snap.tesoros) || [];
      if (snap && snap.radius) tesoroRadius = snap.radius;
      const el = $("#hud-vitaink-tesoros-count");
      if (el) el.textContent = (snap.claimed || 0) + "/" + (snap.total || 0);
      renderVitainkTesoros();
      return snap;
    } catch (_) {
      return null;
    }
  }
  async function fetchVitainkMisiones() {
    if (!vitainkAvailable) return null;
    try {
      const snap = await fetchJSON("/api/vitaink/misiones");
      vitainkMisiones = snap;
      const el = $("#hud-vitaink-misiones-count");
      if (el) el.textContent = (snap.completed || 0) + "/" + (snap.total || 0);
      return snap;
    } catch (_) {
      return null;
    }
  }
  function renderVitainkMisionesAlbum(snap) {
    const box = $("#vitaink-misiones-album");
    const prog = $("#vitaink-misiones-progress");
    if (!box) return;
    box.innerHTML = "";
    if (!snap) {
      if (prog) prog.textContent = "—";
      return;
    }
    if (prog) prog.textContent = (snap.completed || 0) + " / " + (snap.total || 0);
    for (const m of snap.misiones || []) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "mision-card " + (m.done ? "done" : "open");
      btn.setAttribute("role", "listitem");
      btn.innerHTML =
        `<span class="mision-title">${escapeHTML(m.title || m.id)}</span>` +
        `<span class="mision-body">${escapeHTML(m.body || "")}</span>` +
        `<span class="mision-prog">${m.current || 0} / ${m.target || 0}` +
        (m.reward ? " · +" + m.reward + " 🪙" : "") + "</span>" +
        (m.done ? `<span class="mision-badge">${escapeHTML(m.badge || "Completada")}</span>` : "");
      box.appendChild(btn);
    }
  }

  // Marcador VitaInk (solo con plugin + capa ON). No afecta HUD cívico.
  async function fetchVitainkRanking(by) {
    const q = by || vitainkRankTab || "monedas";
    try {
      const snap = await fetchJSON("/api/vitaink/ranking?by=" + encodeURIComponent(q === "both" ? "both" : q));
      vitainkRanking = snap;
      return snap;
    } catch (_) {
      vitainkRanking = null;
      return null;
    }
  }
  function renderVitainkRanking(snap) {
    const list = $("#vitaink-ranking-list");
    const empty = $("#vitaink-ranking-empty");
    if (!list) return;
    list.innerHTML = "";
    const tab = vitainkRankTab === "reputacion" ? "reputacion" : "monedas";
    const rows = (snap && (tab === "reputacion" ? snap.reputacion : snap.monedas)) || [];
    if (!rows.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const e of rows) {
      const li = document.createElement("li");
      if (e.you) li.classList.add("you");
      const score = tab === "reputacion"
        ? ((e.reputacion_label || "Rep") + " " + (e.reputacion != null ? e.reputacion : 0))
        : ("🪙 " + (e.monedas != null ? e.monedas : 0));
      const meta = (e.faccion_emoji || "") + " " + (e.faccion_name || e.faccion_id || "") + (e.demo ? " · demo" : "") + (e.you ? " · tú" : "");
      li.innerHTML =
        '<span class="rank-pos">' + escapeHTML(String(e.rank || "")) + '</span>' +
        '<span class="rank-name">' + escapeHTML(e.nombre || "—") +
        '<span class="rank-meta">' + escapeHTML(meta.trim()) + '</span></span>' +
        '<span class="rank-score">' + escapeHTML(score) + '</span>';
      list.appendChild(li);
    }
  }
  function syncVitainkRankTabs() {
    const m = $("#vitaink-rank-tab-monedas");
    const r = $("#vitaink-rank-tab-rep");
    if (m) {
      m.classList.toggle("active", vitainkRankTab === "monedas");
      m.setAttribute("aria-selected", vitainkRankTab === "monedas" ? "true" : "false");
    }
    if (r) {
      r.classList.toggle("active", vitainkRankTab === "reputacion");
      r.setAttribute("aria-selected", vitainkRankTab === "reputacion" ? "true" : "false");
    }
  }

  /* —— v3.5–v4.6 PNJ + ermitas + peregrinación markers, crónica, panel Dios / maestros + diálogo/encuentro/voto/rito/códice —— */
  /* Qué: marcadores PNJ con miniatura de alma + lema (v3.8) + Hablar cerca (v4.2).
     Por qué: la personalidad filosófica debe verse en Calles cuando VitaInk ON. */
  function botAlmaURL(b) {
    // Preferir pin CLEAN del pack Mari; alma clásica como fallback de ruta.
    const pin = maestroPinURL(b);
    if (pin) return pin;
    if (b && b.alma_url) return b.alma_url;
    const id = (b && b.id) ? String(b.id).toLowerCase() : "";
    const alias = { demonio: "demon", santo: "angel" }; // v5.9.1 demonio→demon (diablo stays diablo)
    const canon = alias[id] || id;
    return canon ? ("/vitaink/almas/" + canon + ".png") : "";
  }
  function renderVitainkBots() {
    const box = $("#street-vitaink-bots");
    if (!box) return;
    box.innerHTML = "";
    if (!vitainkOn || !vitainkBots.length) return;
    for (const b of vitainkBots) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vita-bot-pin vita-bot-hit" + (nearBotId === b.id ? " near" : "");
      btn.dataset.botId = b.id;
      btn.style.left = Math.max(4, Math.min(96, b.x || 50)) + "%";
      btn.style.top = Math.max(4, Math.min(96, b.y || 50)) + "%";
      const botColors = {
        angel: "#2563eb", demonio: "#dc2626", diablo: "#dc2626", santo: "#2563eb",
        hada: "#db2777", gnomo: "#16a34a", duende: "#ca8a04", sabio: "#7c3aed", satan: "#7f1d1d",
      };
      const color = botColors[b.id] || "#64748b";
      btn.style.setProperty("--vita-bot-color", color);
      const lema = b.lema || b.note || "PNJ VitaInk";
      btn.title = (b.display_name || b.id) + " · " + lema + " · Toca para 💬 Hablar";
      const alma = botAlmaURL(b);
      const thumb = alma
        ? `<img class="vita-alma-thumb" src="${escapeHTML(alma)}" alt="" width="30" height="30" loading="lazy">`
        : `<span>${escapeHTML(b.emoji || "🤖")}</span>`;
      const lemaEl = b.lema
        ? `<span class="pin-lema">${escapeHTML(b.lema)}</span>`
        : "";
      btn.innerHTML = `${thumb} <span class="pin-name">${escapeHTML(b.display_name || b.id)}</span>${lemaEl}`;
      btn.addEventListener("click", (ev) => {
        ev.stopPropagation();
        // Hit target amplio: encuentro directo (API no exige proximidad).
        // Si está lejos, igual habla; el panel Maestros sigue disponible aparte.
        nearBotId = b.id;
        updateCivicAction();
        hablarConBotCercano(b.id).catch(() => {});
      });
      box.appendChild(btn);
    }
  }
  function renderVitainkErmitas() {
    const box = $("#street-vitaink-ermitas");
    if (!box) return;
    box.innerHTML = "";
    if (!vitainkOn || !vitainkErmitas.length) return;
    for (const e of vitainkErmitas) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vita-ermita-pin" + (nearErmitaId === e.id ? " near" : "");
      btn.dataset.ermitaId = e.id;
      btn.style.left = Math.max(4, Math.min(96, e.x || 50)) + "%";
      btn.style.top = Math.max(4, Math.min(96, e.y || 50)) + "%";
      btn.title = (e.nombre || "Ermita") + " · Retiro si estás cerca";
      btn.setAttribute("aria-label", e.nombre || "Ermita de la senda");
      btn.textContent = e.emoji || "🛕";
      btn.addEventListener("click", (ev) => {
        ev.stopPropagation();
        const d = Math.hypot(playerX - (e.x || 50), playerY - (e.y || 50));
        if (d <= botRadius) {
          nearErmitaId = e.id;
          updateCivicAction();
          retiroEnErmita(e.id).catch(() => {});
        } else {
          setStatus("Acércate a la ermita para el Retiro", "ok");
        }
      });
      box.appendChild(btn);
    }
  }
  async function retiroEnErmita(id) {
    const eid = id || nearErmitaId;
    if (!eid) { setStatus("Ninguna ermita cerca", "err"); return; }
    try {
      const body = { ensenanza: true };
      if (vitainkValorSel) body.valor_id = vitainkValorSel;
      const res = await fetchJSON("/api/vitaink/ermitas/" + encodeURIComponent(eid) + "/retiro", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (res && res.ok) {
        const msg = res.ya_retirado_hoy
          ? ("Retiro ya hecho hoy · " + (res.ensenanza || "vuelve mañana"))
          : ("Retiro · +" + (res.bonus_alineacion || 0) + " · " + (res.ensenanza || res.conclusion || ""));
        setStatus(msg, "ok");
        await fetchVitainkAlineacion();
        renderVitainkMaestroDetail();
      }
    } catch (e) {
      setStatus((e && e.message) || "Retiro no disponible", "err");
    }
  }

  async function fetchVitainkCronica() {
    try {
      const snap = await fetchJSON("/api/vitaink/cronica");
      vitainkCronica = (snap && snap.events) || [];
      return snap;
    } catch (_) {
      vitainkCronica = [];
      return null;
    }
  }
  function renderVitainkCronica() {
    const list = $("#vitaink-cronica-list");
    const empty = $("#vitaink-cronica-empty");
    if (!list) return;
    list.innerHTML = "";
    if (!vitainkCronica.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    // Qué: miniatura de alma del actor + título/cuerpo (v3.8).
    // Por qué: la crónica debe reconocer la voz filosófica del PNJ de un vistazo.
    const almaByActor = Object.create(null);
    for (const b of vitainkBots) {
      if (b && b.id) almaByActor[b.id] = botAlmaURL(b);
    }
    almaByActor.demonio = almaByActor.diablo || "/vitaink/almas/diablo.png";
    almaByActor.santo = almaByActor.angel || "/vitaink/almas/angel.png";
    for (const ev of vitainkCronica.slice(0, 30)) {
      const row = document.createElement("div");
      row.className = "cr-row";
      row.setAttribute("role", "listitem");
      const actor = (ev.actor || "").toLowerCase();
      const alma = almaByActor[actor] || (actor && actor !== "dios" ? ("/vitaink/almas/" + actor + ".png") : "");
      const thumb = alma
        ? `<img class="vita-alma-thumb cr-alma" src="${escapeHTML(alma)}" alt="" width="32" height="32" loading="lazy">`
        : "";
      row.innerHTML = `<div class="cr-head">${thumb}<strong>${escapeHTML(ev.title || ev.kind || "evento")}</strong></div>` +
        `<span>${escapeHTML(ev.body || "")}</span>`;
      list.appendChild(row);
    }
  }
  async function openVitainkCronica() {
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk para la crónica", "err");
      return;
    }
    await fetchVitainkCronica();
    renderVitainkCronica();
    const panel = $("#vitaink-cronica-panel");
    if (panel) panel.classList.remove("hidden");
  }
  function closeVitainkCronica() {
    const panel = $("#vitaink-cronica-panel");
    if (panel) panel.classList.add("hidden");
  }

  /* —— v4.1–v4.4 Maestros (voto + diálogo / encuentro + lecciones / diario / prueba / reliquias / sínodo + roles) ——
     Qué: panel para seguir un PNJ como guía filosófica con rol, grado, senda y diálogo.
     Por qué: alineación consciente sin culto; se puede cambiar maestro y rol. */
  async function fetchVitainkMaestros() {
    try {
      const snap = await fetchJSON("/api/vitaink/maestros");
      vitainkMaestros = (snap && snap.maestros) || [];
      vitainkRolesDisponibles = (snap && snap.roles_disponibles) || [];
      return snap;
    } catch (_) {
      vitainkMaestros = [];
      vitainkRolesDisponibles = [];
      return null;
    }
  }
  async function fetchVitainkAlineacion() {
    try {
      vitainkAlineacion = await fetchJSON("/api/vitaink/alineacion");
      return vitainkAlineacion;
    } catch (_) {
      vitainkAlineacion = null;
      return null;
    }
  }
  async function fetchVitainkLecciones(id) {
    if (!id) { vitainkLecciones = null; return null; }
    try {
      vitainkLecciones = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(id) + "/lecciones");
      return vitainkLecciones;
    } catch (_) {
      vitainkLecciones = null;
      return null;
    }
  }
  async function fetchVitainkDiario() {
    try {
      const snap = await fetchJSON("/api/vitaink/diario");
      vitainkDiario = (snap && snap.entries) || [];
      return snap;
    } catch (_) {
      vitainkDiario = [];
      return null;
    }
  }
  async function fetchVitainkPrueba(id) {
    if (!id) { vitainkPrueba = null; return null; }
    try {
      vitainkPrueba = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(id) + "/prueba");
      return vitainkPrueba;
    } catch (_) {
      vitainkPrueba = null;
      return null;
    }
  }
  async function fetchVitainkDialogo(id) {
    if (!id) { vitainkDialogo = null; return null; }
    try {
      vitainkDialogo = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(id) + "/dialogo");
      return vitainkDialogo;
    } catch (_) {
      vitainkDialogo = null;
      return null;
    }
  }
  async function fetchVitainkReliquias() {
    try {
      const snap = await fetchJSON("/api/vitaink/reliquias");
      vitainkReliquias = (snap && snap.reliquias) || [];
      return snap;
    } catch (_) {
      vitainkReliquias = [];
      return null;
    }
  }
  async function fetchVitainkSinodo() {
    try {
      vitainkSinodo = await fetchJSON("/api/vitaink/sinodo");
      return vitainkSinodo;
    } catch (_) {
      vitainkSinodo = null;
      return null;
    }
  }
  async function refreshVitainkSenda(id) {
    await Promise.all([
      fetchVitainkLecciones(id),
      fetchVitainkDiario(),
      fetchVitainkPrueba(id),
      fetchVitainkDialogo(id),
      fetchVitainkReliquias(),
    ]);
  }
  function setMaestrosFb(msg, err) {
    const fb = $("#vitaink-maestros-fb");
    if (!fb) return;
    fb.textContent = msg || "";
    fb.classList.toggle("err", !!err);
  }
  function rolDeMaestro(id) {
    const roles = (vitainkAlineacion && vitainkAlineacion.roles) || {};
    if (roles[id]) return roles[id];
    if (vitainkAlineacion && vitainkAlineacion.maestro_primario === id && vitainkAlineacion.rol) {
      return vitainkAlineacion.rol;
    }
    return vitainkRolPendiente || "seguidor";
  }
  function maestriaDe(id) {
    const map = (vitainkAlineacion && vitainkAlineacion.maestrias) || {};
    if (map[id]) return map[id];
    if (vitainkAlineacion && vitainkAlineacion.maestro_primario === id && vitainkAlineacion.maestria) {
      return vitainkAlineacion.maestria;
    }
    return null;
  }
  function rolMeta(id) {
    return (vitainkRolesDisponibles || []).find((r) => r.id === id) || { id: id, nombre: id, color: "#6366f1", descripcion: "" };
  }

  function puedeEncarnarMaestro(maestroId) {
    const pack = maestroPack(maestroId || "");
    if (!pack.hasDay || !pack.id) return false;
    const al = vitainkAlineacion;
    if (!al) return false;
    const id = pack.id;
    const followed = al.maestro_primario === id || ((al.maestros_secundarios || []).indexOf(id) >= 0);
    if (!followed) return false;
    const rol = (al.roles && al.roles[id]) || (al.maestro_primario === id ? al.rol : "") || "";
    return rol === "discipulo" || rol === "discípulo";
  }
  function puedeEncarnarDiablo() {
    return puedeEncarnarMaestro("diablo");
  }
  function encarnarMaestroLabel(id) {
    const pack = maestroPack(id);
    const names = { diablo: "El Diablo", demonio: "Demonio", angel: "Ángel", hada: "Hada", gnomo: "Gnomo", duende: "Duende", sabio: "Sabio", satan: "Satán" };
    const emos = { diablo: "👹", demonio: "😈", angel: "😇", hada: "🧚", gnomo: "🧙", duende: "👺", sabio: "🦉", satan: "⛧" };
    return { name: names[pack.id] || pack.id, emo: emos[pack.id] || "✨", folder: pack.folder || pack.id };
  }
  function renderVitainkMaestrosList() {
    const box = $("#vitaink-maestros-list");
    if (!box) return;
    box.innerHTML = "";
    const scores = (vitainkAlineacion && vitainkAlineacion.scores) || {};
    const prim = (vitainkAlineacion && vitainkAlineacion.maestro_primario) || "";
    const secs = (vitainkAlineacion && vitainkAlineacion.maestros_secundarios) || [];
    for (const m of vitainkMaestros) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "maestro-row" + (vitainkMaestroSel === m.id ? " active" : "");
      btn.setAttribute("role", "listitem");
      const score = scores[m.id] != null ? scores[m.id] : 0;
      let badge = "";
      if (prim === m.id) badge = " · primario";
      else if (secs.indexOf(m.id) >= 0) badge = " · afinidad";
      const mae = maestriaDe(m.id);
      const rol = (prim === m.id || secs.indexOf(m.id) >= 0) ? rolDeMaestro(m.id) : "";
      const rolLabel = rol ? (" · " + (rolMeta(rol).nombre || rol)) : "";
      const maeLabel = mae ? (" · " + (mae.titulo || mae.grado || "")) : "";
      const pruebas = (vitainkAlineacion && vitainkAlineacion.pruebas_disponibles) || {};
      const pruebaBadge = pruebas[m.id] ? " · prueba disponible" : "";
      // Miniatura: cabeza Mari + tinte del maestro; onerror → emoji.
      btn.innerHTML =
        maestroThumbHTML(m, 36) +
        `<span class="maestro-meta"><strong>${escapeHTML((m.emoji || "") + " " + (m.display_name || m.id))}</strong>` +
        `<span>Alineación ${score}/100${badge}${escapeHTML(rolLabel)}${escapeHTML(maeLabel)}${escapeHTML(pruebaBadge)}</span></span>`;
      btn.addEventListener("click", () => {
        vitainkMaestroSel = m.id;
        const r = rolDeMaestro(m.id);
        if (r) vitainkRolPendiente = r;
        refreshVitainkSenda(m.id).then(() => {
          renderVitainkMaestrosList();
          renderVitainkMaestroDetail();
        }).catch(() => {
          renderVitainkMaestrosList();
          renderVitainkMaestroDetail();
        });
      });
      box.appendChild(btn);
    }
    wireMaestroThumbFallbacks(box);
  }
  function renderVitainkMaestroDetail() {
    const detail = $("#vitaink-maestro-detail");
    if (!detail) return;
    const m = vitainkMaestros.find((x) => x.id === vitainkMaestroSel);
    if (!m) {
      detail.classList.add("hidden");
      return;
    }
    detail.classList.remove("hidden");
    const alma = $("#vitaink-maestro-alma");
    if (alma) {
      // Preferir bust CLEAN Mari + tinte; fallback pin/alma clásica / emoji.
      alma.classList.add("maestro-head");
      alma.style.setProperty("--maestro-tint", maestroTint(m));
      alma.src = maestroHeadURL(m) || maestroPinURL(m) || m.alma_url || botAlmaURL(m);
      alma.alt = m.display_name || m.id;
      alma.dataset.emoji = m.emoji || "🧭";
      alma.classList.remove("hidden");
      // Quitar fallback previo si se re-renderiza.
      const prev = alma.parentNode && alma.parentNode.querySelector(".vita-alma-fallback");
      if (prev) prev.remove();
      bindImgEmojiFallback(alma, m.emoji || "🧭");
    }
    const name = $("#vitaink-maestro-name");
    if (name) name.textContent = (m.emoji || "") + " " + (m.display_name || m.id);
    const lema = $("#vitaink-maestro-lema");
    if (lema) lema.textContent = m.lema || "";
    const bio = $("#vitaink-maestro-bio");
    if (bio) bio.textContent = m.bio || "";
    const voz = $("#vitaink-maestro-voz");
    if (voz) voz.textContent = m.voz ? ("Voz: " + m.voz) : "";
    const mantra = $("#vitaink-maestro-mantra");
    if (mantra) mantra.textContent = m.mantra ? ("Mantra: " + m.mantra) : "";
    const temper = $("#vitaink-maestro-temperamento");
    if (temper) temper.textContent = m.temperamento ? ("Temperamento: " + m.temperamento) : "";
    const encBtn = $("#btn-vitaink-encarnar-diablo");
    if (encBtn) {
      const pack = maestroPack(m);
      const canPack = !!pack.hasDay;
      const can = canPack && puedeEncarnarMaestro(m.id);
      const lab = encarnarMaestroLabel(m.id);
      const activeHere = encarnarMaestroIdActivo() === pack.id;
      encBtn.classList.toggle("hidden", !canPack);
      encBtn.disabled = !can;
      encBtn.textContent = activeHere && can
        ? (lab.emo + " Encarnando (quitar)")
        : (lab.emo + " Encarnar avatar " + lab.name);
      encBtn.title = can
        ? ("Avatar Calles con sprites masters/" + lab.folder + "/day/ + tinte mientras eres discípulo")
        : ("Sigue a " + lab.name + " con rol discípulo para encarnar su avatar");
      encBtn.onclick = () => {
        if (!puedeEncarnarMaestro(m.id)) {
          setMaestrosFb("Necesitas seguir a " + lab.name + " como discípulo", true);
          return;
        }
        const next = activeHere ? "" : pack.id;
        encarnarMaestroId = next;
        encarnarDiablo = next === "diablo";
        try {
          localStorage.setItem(ENCARNAR_MAESTRO_KEY, next);
          localStorage.setItem(ENCARNAR_DIABLO_KEY, next === "diablo" ? "1" : "0");
        } catch (_) {}
        ensureMaestroSpriteFolder(pack.id).catch(() => {});
        applyPlayerAvatarLook();
        renderVitainkMaestroDetail();
        setMaestrosFb(next ? ("Encarnas el avatar de " + lab.name + " en Calles") : ("Avatar " + lab.name + " quitado"));
      };
    }
    const scores = (vitainkAlineacion && vitainkAlineacion.scores) || {};
    const score = scores[m.id] != null ? scores[m.id] : 0;
    const fill = $("#vitaink-maestro-align-fill");
    if (fill) fill.style.width = Math.max(0, Math.min(100, score)) + "%";
    const lab = $("#vitaink-maestro-align-label");
    if (lab) lab.textContent = score + " / 100";

    const rol = rolDeMaestro(m.id);
    vitainkRolPendiente = rol || vitainkRolPendiente || "seguidor";
    const chip = $("#vitaink-maestro-rol-chip");
    if (chip) {
      const meta = rolMeta(vitainkRolPendiente);
      const followed = !!(vitainkAlineacion && (vitainkAlineacion.maestro_primario === m.id || ((vitainkAlineacion.maestros_secundarios || []).indexOf(m.id) >= 0)));
      if (followed) {
        chip.classList.remove("hidden");
        chip.textContent = meta.nombre || vitainkRolPendiente;
        chip.style.background = meta.color || "#6366f1";
        chip.title = meta.descripcion || "";
      } else {
        chip.classList.add("hidden");
      }
    }

    const mae = maestriaDe(m.id);
    const mfill = $("#vitaink-maestro-maestria-fill");
    const mlab = $("#vitaink-maestro-maestria-label");
    const priv = $("#vitaink-maestro-privilegio");
    if (mae) {
      if (mfill) mfill.style.width = Math.max(0, Math.min(100, mae.progreso != null ? mae.progreso : 0)) + "%";
      if (mlab) mlab.textContent = (mae.titulo || mae.grado || "—") + (mae.siguiente ? (" → " + mae.siguiente + " (" + (mae.progreso || 0) + "%)") : " · tope");
      if (priv) priv.textContent = mae.privilegio || (vitainkAlineacion && vitainkAlineacion.privilegio) || "—";
    } else {
      if (mfill) mfill.style.width = "0%";
      if (mlab) mlab.textContent = "Sin maestría activa · sigue a este maestro para abrir el camino";
      if (priv) priv.textContent = "El privilegio filosófico aparece al seguir y avanzar de grado (texto, no paywall).";
    }

    const rolesBox = $("#vitaink-maestro-roles");
    if (rolesBox) {
      rolesBox.innerHTML = "";
      for (const r of (vitainkRolesDisponibles || [])) {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "rol-pick" + (vitainkRolPendiente === r.id ? " active" : "");
        b.setAttribute("role", "option");
        b.setAttribute("aria-selected", vitainkRolPendiente === r.id ? "true" : "false");
        b.title = r.descripcion || r.nombre;
        b.textContent = r.nombre || r.id;
        if (vitainkRolPendiente === r.id) {
          b.style.background = r.color || "#6366f1";
          b.style.color = "#fff";
        }
        b.addEventListener("click", () => {
          vitainkRolPendiente = r.id;
          const followed = !!(vitainkAlineacion && (vitainkAlineacion.maestro_primario === m.id || ((vitainkAlineacion.maestros_secundarios || []).indexOf(m.id) >= 0)));
          if (followed) {
            cambiarRolVitainkMaestro(m.id, r.id).catch(() => {});
          } else {
            renderVitainkMaestroDetail();
            setMaestrosFb("Rol «" + (r.nombre || r.id) + "» listo · pulsa Seguir para vincularlo");
          }
        });
        rolesBox.appendChild(b);
      }
    }

    const dudaBtn = $("#btn-vitaink-meditar-duda");
    const dudaHint = $("#vitaink-maestro-sabor-hint");
    const isInter = vitainkRolPendiente === "interrogante";
    if (dudaHint) dudaHint.hidden = !isInter;
    if (dudaBtn) {
      dudaBtn.classList.toggle("hidden", !isInter);
      dudaBtn.onclick = () => {
        const vid = vitainkValorSel || ((m.valores && m.valores[0]) ? m.valores[0].id : "");
        if (!vid) { setMaestrosFb("Elige un valor primero", true); return; }
        meditarVitainkMaestro(m.id, vid, "duda").catch(() => {});
      };
    }

    const vals = $("#vitaink-maestro-valores");
    if (vals) {
      vals.innerHTML = "";
      for (const v of (m.valores || [])) {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "valor-chip" + (vitainkValorSel === v.id ? " active" : "");
        b.title = v.nota || "Meditar / afirmar este valor";
        b.textContent = "✨ " + (v.nombre || v.id);
        b.addEventListener("click", () => {
          vitainkValorSel = v.id;
          vals.querySelectorAll(".valor-chip").forEach((x) => x.classList.remove("active"));
          b.classList.add("active");
          const ve = $("#vitaink-voto-estado");
          if (ve && vitainkAlineacion && vitainkAlineacion.maestro_primario === m.id) {
            ve.textContent = "Valor elegido para voto: «" + (v.nombre || v.id) + "» · pulsa Tomar voto o Meditar";
          }
          meditarVitainkMaestro(m.id, v.id).catch(() => {});
        });
        vals.appendChild(b);
      }
    }
    // v4.4 — estado del voto
    const votoEst = $("#vitaink-voto-estado");
    const al = vitainkAlineacion;
    const voto = al && al.voto;
    const isPrim = !!(al && al.maestro_primario === m.id);
    if (votoEst) {
      if (voto && voto.maestro_id === m.id) {
        votoEst.textContent = "Voto activo · «" + (voto.valor_nombre || voto.valor_id) + "» — " + (voto.texto || "") +
          " · refuerzos " + (voto.refuerzos || 0) + " · tensiones " + (voto.quiebres || 0);
      } else if (isPrim) {
        votoEst.textContent = "Sin voto activo · elige un valor y pulsa «Tomar voto» (solo primario).";
      } else {
        votoEst.textContent = "El voto solo se toma con el maestro primario.";
      }
    }

    const ens = $("#vitaink-maestro-ensenanzas");
    if (ens) {
      ens.innerHTML = "";
      for (const line of (m.ensenanzas || [])) {
        const li = document.createElement("li");
        li.textContent = line;
        ens.appendChild(li);
      }
    }
    renderVitainkDialogo(m.id);
    renderVitainkLecciones(m.id);
    renderVitainkPrueba(m.id);
    renderVitainkMaestroReliquias(m.id);
    renderVitainkDiario(m.id);
    const conc = $("#vitaink-maestro-conclusion");
    if (conc) {
      const al = vitainkAlineacion || {};
      if (al.ultimo_maestro === m.id && al.ultima_conclusion) {
        conc.textContent = al.ultima_conclusion;
      } else if (score >= 55) {
        conc.textContent = m.conclusion_si_alineado || "—";
      } else {
        conc.textContent = m.conclusion_si_desalineado || "Aún no has meditado con este maestro.";
      }
    }
  }
  async function openVitainkMaestros() {
    ensureDiabloSpriteFolder().catch(() => {});
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk para los maestros", "err");
      return;
    }
    await fetchVitainkMaestros();
    await fetchVitainkAlineacion();
    if (!vitainkMaestroSel && vitainkAlineacion && vitainkAlineacion.maestro_primario) {
      vitainkMaestroSel = vitainkAlineacion.maestro_primario;
    }
    if (!vitainkMaestroSel && vitainkMaestros.length) {
      vitainkMaestroSel = vitainkMaestros[0].id;
    }
    if (vitainkMaestroSel) vitainkRolPendiente = rolDeMaestro(vitainkMaestroSel) || "seguidor";
    await refreshVitainkSenda(vitainkMaestroSel);
    renderVitainkMaestrosList();
    renderVitainkMaestroDetail();
    const panel = $("#vitaink-maestros-panel");
    if (panel) panel.classList.remove("hidden");
  }
  function closeVitainkMaestros() {
    const panel = $("#vitaink-maestros-panel");
    if (panel) panel.classList.add("hidden");
  }
  async function seguirVitainkMaestro(secundario) {
    if (!vitainkMaestroSel) return;
    const body = secundario
      ? { secundario: true, rol: vitainkRolPendiente || "seguidor" }
      : { primario: true, rol: vitainkRolPendiente || "seguidor" };
    try {
      vitainkAlineacion = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(vitainkMaestroSel) + "/seguir", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      setMaestrosFb(secundario ? "Afinidad secundaria registrada" : "Maestro primario elegido · rol «" + (rolMeta(vitainkRolPendiente).nombre || vitainkRolPendiente) + "»");
      await refreshVitainkSenda(vitainkMaestroSel);
      renderVitainkMaestrosList();
      renderVitainkMaestroDetail();
      await fetchVitainkCronica();
    } catch (e) {
      setMaestrosFb((e && e.message) || "No se pudo seguir", true);
    }
  }
  async function cambiarRolVitainkMaestro(id, rol) {
    try {
      vitainkAlineacion = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(id) + "/rol", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rol: rol }),
      });
      vitainkRolPendiente = rol;
      setMaestrosFb("Rol cambiado a «" + (rolMeta(rol).nombre || rol) + "»");
      await refreshVitainkSenda(id);
      renderVitainkMaestrosList();
      renderVitainkMaestroDetail();
      await fetchVitainkCronica();
    } catch (e) {
      setMaestrosFb((e && e.message) || "No se pudo cambiar el rol", true);
    }
  }
  async function dejarVitainkMaestro() {
    if (!vitainkMaestroSel) return;
    try {
      vitainkAlineacion = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(vitainkMaestroSel) + "/seguir", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dejar: true }),
      });
      setMaestrosFb("Has dejado a este maestro · el camino sigue abierto");
      await refreshVitainkSenda(vitainkMaestroSel);
      renderVitainkMaestrosList();
      renderVitainkMaestroDetail();
    } catch (e) {
      setMaestrosFb((e && e.message) || "No se pudo dejar", true);
    }
  }
  async function meditarVitainkMaestro(id, valorId, sabor) {
    try {
      const payload = { valor_id: valorId };
      if (sabor) payload.sabor = sabor;
      const res = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(id) + "/meditar", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      await fetchVitainkAlineacion();
      await refreshVitainkSenda(id);
      renderVitainkMaestrosList();
      renderVitainkMaestroDetail();
      const mae = res && res.maestria ? (" · " + (res.maestria.titulo || "")) : "";
      setMaestrosFb((res && res.conclusion) ? ("Meditaste · " + (res.valor_nombre || valorId) + mae) : "Meditación registrada");
      await fetchVitainkCronica();
      setStatus("Conclusión en la crónica · " + (res && res.valor_nombre ? res.valor_nombre : valorId), "ok");
    } catch (e) {
      setMaestrosFb((e && e.message) || "No se pudo meditar", true);
    }
  }

  function renderVitainkDialogo(maestroId) {
    const box = $("#vitaink-maestro-dialogo");
    if (!box) return;
    box.innerHTML = "";
    const snap = (vitainkDialogo && vitainkDialogo.maestro_id === maestroId) ? vitainkDialogo : null;
    const list = (snap && snap.preguntas) || [];
    if (!list.length) {
      box.innerHTML = "<p class=\"muted small\">Sin preguntas sugeridas aún.</p>";
      return;
    }
    for (const q of list) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "dialogo-q";
      b.setAttribute("role", "listitem");
      b.textContent = q.texto || q.id;
      b.title = (q.tema || "") + " · preguntar";
      b.addEventListener("click", () => dialogarConMaestro(maestroId, { pregunta_id: q.id }).catch(() => {}));
      box.appendChild(b);
    }
  }
  async function dialogarConMaestro(id, payload) {
    try {
      const res = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(id) + "/dialogo", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload || {}),
      });
      const out = $("#vitaink-dialogo-respuesta");
      if (res && res.rate_limited) {
        const msg = "Espera " + (res.retry_after_sec || "?") + "s · rate-limit suave";
        if (out) out.textContent = msg;
        setMaestrosFb(msg, true);
        return res;
      }
      if (out) {
        out.textContent = (res && res.respuesta)
          ? ((res.pregunta ? ("Tu pregunta: " + res.pregunta + "\n\n") : "") + res.respuesta)
          : "Sin respuesta";
      }
      await fetchVitainkAlineacion();
      await fetchVitainkDiario();
      renderVitainkMaestroDetail();
      setMaestrosFb((res && res.tema) ? ("Diálogo · " + res.tema) : "Diálogo registrado");
      await fetchVitainkCronica();
      return res;
    } catch (e) {
      setMaestrosFb((e && e.message) || "No se pudo dialogar", true);
      return null;
    }
  }
  function showEncuentroToast(res) {
    const toast = $("#vita-encuentro-toast");
    if (!toast || !res) return;
    const alma = $("#vita-encuentro-alma");
    if (alma) {
      alma.src = res.alma_url || botAlmaURL({ id: res.maestro_id });
      alma.alt = res.display_name || res.maestro_id || "";
    }
    const title = $("#vita-encuentro-title");
    if (title) {
      title.textContent = (res.emoji || "💬") + " " + (res.display_name || "Encuentro") +
        (res.tipo === "pregunta" ? " · pregunta" : " · enseñanza");
    }
    const body = $("#vita-encuentro-body");
    if (body) body.textContent = res.texto || res.note || "";
    toast.classList.remove("hidden");
  }
  function closeEncuentroToast() {
    const toast = $("#vita-encuentro-toast");
    if (toast) toast.classList.add("hidden");
  }
  async function hablarConBotCercano(id) {
    const botId = id || nearBotId;
    if (!botId) return;
    try {
      const res = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(botId) + "/encuentro", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ desde_mapa: true }),
      });
      if (res && res.rate_limited) {
        setStatus("Encuentro en cooldown · " + (res.cooldown_left_sec || "?") + "s con este maestro", "err");
        return res;
      }
      showEncuentroToast(res);
      setStatus("Encuentro · " + ((res && res.display_name) || botId), "ok");
      await fetchVitainkDiario();
      await fetchVitainkCronica();
      if (vitainkMaestroSel === botId) {
        await fetchVitainkAlineacion();
        renderVitainkMaestroDetail();
      }
      return res;
    } catch (e) {
      setStatus((e && e.message) || "No se pudo hablar", "err");
      return null;
    }
  }

  function renderVitainkLecciones(maestroId) {
    const box = $("#vitaink-maestro-lecciones");
    if (!box) return;
    box.innerHTML = "";
    const list = (vitainkLecciones && vitainkLecciones.maestro_id === maestroId)
      ? (vitainkLecciones.lecciones || [])
      : [];
    if (!list.length) {
      const li = document.createElement("li");
      li.className = "muted";
      li.textContent = "Sigue a este maestro para abrir la primera lección.";
      box.appendChild(li);
      return;
    }
    for (const lec of list) {
      const li = document.createElement("li");
      li.className = "leccion-row leccion-" + (lec.estado || "bloqueada");
      const locked = lec.estado === "bloqueada";
      const title = document.createElement(locked ? "span" : "button");
      if (!locked) {
        title.type = "button";
        title.className = "leccion-open";
        title.addEventListener("click", () => leerVitainkLeccion(maestroId, lec.indice).catch(() => {}));
      }
      title.textContent = (lec.estado === "leida" ? "✓ " : locked ? "🔒 " : "📖 ") + (lec.titulo || ("Lección " + (lec.indice + 1)));
      li.appendChild(title);
      if (lec.texto) {
        const p = document.createElement("p");
        p.className = "leccion-texto";
        p.textContent = lec.texto;
        li.appendChild(p);
      }
      box.appendChild(li);
    }
  }
  function renderVitainkPrueba(maestroId) {
    const box = $("#vitaink-maestro-prueba");
    if (!box) return;
    const of = vitainkPrueba;
    const ok = of && of.disponible && of.maestro_id === maestroId;
    box.classList.toggle("hidden", !ok);
    if (!ok) return;
    const meta = $("#vitaink-prueba-meta");
    if (meta) meta.textContent = "Umbral " + (of.titulo || of.grado || "") + " · " + (of.umbral != null ? of.umbral : "") + "/100 · filosófica, no combate";
    const q = $("#vitaink-prueba-pregunta");
    if (q) q.textContent = of.pregunta || "";
    const ops = $("#vitaink-prueba-opciones");
    if (ops) {
      ops.innerHTML = "";
      for (const o of (of.opciones || [])) {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "prueba-op prueba-" + (o.alineacion || o.id || "");
        b.textContent = o.texto || o.id;
        b.title = (o.alineacion || o.id || "") + " · elegir con peso";
        b.addEventListener("click", () => hacerVitainkPrueba(maestroId, o.id).catch(() => {}));
        ops.appendChild(b);
      }
    }
  }
  function renderVitainkDiario(maestroId) {
    const box = $("#vitaink-maestro-diario");
    if (!box) return;
    box.innerHTML = "";
    const rows = (vitainkDiario || []).filter((e) => !maestroId || e.maestro_id === maestroId).slice(0, 8);
    if (!rows.length) {
      box.innerHTML = "<p class=\"muted small\">Aún no hay páginas en el diario de esta senda.</p>";
      return;
    }
    for (const e of rows) {
      const div = document.createElement("div");
      div.className = "diario-row";
      div.setAttribute("role", "listitem");
      const when = e.at ? new Date(e.at * 1000).toLocaleString("es-ES", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" }) : "";
      div.innerHTML = "<strong>" + escapeHTML(e.title || e.kind || "nota") + "</strong>" +
        (when ? "<span class=\"diario-when\">" + escapeHTML(when) + "</span>" : "") +
        "<p>" + escapeHTML(e.body || "") + "</p>";
      box.appendChild(div);
    }
  }
  function renderReliquiaRow(r) {
    const div = document.createElement("div");
    div.className = "reliquia-row";
    div.setAttribute("role", "listitem");
    const when = r.at ? new Date(r.at * 1000).toLocaleString("es-ES", { day: "2-digit", month: "short" }) : "";
    const maestro = (vitainkMaestros || []).find((m) => m.id === r.maestro_id);
    const maeLabel = maestro ? ((maestro.emoji || "") + " " + (maestro.display_name || r.maestro_id)) : (r.maestro_id || "");
    div.innerHTML =
      "<span class=\"reliquia-simbolo\" aria-hidden=\"true\">" + escapeHTML(r.simbolo || "🕯️") + "</span>" +
      "<span><strong>" + escapeHTML(r.nombre || r.id || "Reliquia") + "</strong>" +
      "<span class=\"reliquia-meta\">" + escapeHTML(maeLabel) +
      (r.grado ? (" · " + escapeHTML(r.grado)) : "") +
      (when ? (" · " + escapeHTML(when)) : "") + "</span>" +
      "<p>" + escapeHTML(r.significado || "") + "</p></span>";
    return div;
  }
  function renderVitainkReliquiasList(boxSel, emptySel, filterMaestroId) {
    const box = $(boxSel);
    if (!box) return;
    box.innerHTML = "";
    let rows = vitainkReliquias || [];
    if (filterMaestroId) rows = rows.filter((r) => r.maestro_id === filterMaestroId);
    const empty = emptySel ? $(emptySel) : null;
    if (!rows.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const r of rows) box.appendChild(renderReliquiaRow(r));
  }
  function renderVitainkMaestroReliquias(maestroId) {
    renderVitainkReliquiasList("#vitaink-maestro-reliquias", null, maestroId);
    const box = $("#vitaink-maestro-reliquias");
    if (box && !(vitainkReliquias || []).some((r) => r.maestro_id === maestroId)) {
      box.innerHTML = "<p class=\"muted small\">Sin reliquias de este maestro aún.</p>";
    }
  }
  function renderVitainkPjReliquias() {
    renderVitainkReliquiasList("#vitaink-pj-reliquias", "#vitaink-pj-reliquias-empty", null);
  }
  function renderVitainkReliquiasPanel() {
    renderVitainkReliquiasList("#vitaink-reliquias-list", "#vitaink-reliquias-empty", null);
  }
  function renderVitainkSinodo() {
    const box = $("#vitaink-sinodo-list");
    const tens = $("#vitaink-sinodo-tension");
    if (!box) return;
    box.innerHTML = "";
    const snap = vitainkSinodo;
    const filas = (snap && snap.filas) || [];
    if (tens) {
      const note = (snap && (snap.tension_creativa || ((snap.tensiones || [])[0] && snap.tensiones[0].nota))) || "";
      if (note) {
        tens.classList.remove("hidden");
        tens.textContent = "Tensión creativa · " + note;
      } else {
        tens.classList.add("hidden");
        tens.textContent = "";
      }
    }
    for (const f of filas) {
      const div = document.createElement("div");
      div.className = "sinodo-row" + (f.primario ? " primario" : "") + (f.seguido ? " seguido" : "");
      div.setAttribute("role", "listitem");
      const score = f.score != null ? f.score : 0;
      const rol = f.rol_nombre || f.rol || (f.seguido ? "—" : "no seguido");
      div.innerHTML =
        "<div class=\"sinodo-head\"><strong>" + escapeHTML((f.emoji || "") + " " + (f.display_name || f.maestro_id)) +
        "</strong><span class=\"sinodo-score\">" + score + "/100</span></div>" +
        (f.lema ? ("<p class=\"sinodo-lema\">" + escapeHTML(f.lema) + "</p>") : "") +
        "<div class=\"sinodo-bar\" aria-hidden=\"true\"><div class=\"sinodo-bar-fill\" style=\"width:" + Math.max(0, Math.min(100, score)) + "%\"></div></div>" +
        "<p class=\"sinodo-sub\">" + escapeHTML((f.titulo || f.grado || "Novicio") + " · rol " + rol) +
        (f.primario ? " · primario" : (f.seguido ? " · afinidad" : "")) + "</p>";
      box.appendChild(div);
    }
  }
  async function openVitainkReliquias() {
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk para las reliquias", "err");
      return;
    }
    const panel = $("#vitaink-reliquias-panel");
    if (!panel) return;
    closeHudMoreMenu();
    await fetchVitainkMaestros();
    await fetchVitainkReliquias();
    renderVitainkReliquiasPanel();
    panel.classList.remove("hidden");
  }
  function closeVitainkReliquias() {
    const panel = $("#vitaink-reliquias-panel");
    if (panel) panel.classList.add("hidden");
  }

  async function openVitainkRito() {
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk para el rito diario", "err");
      return;
    }
    closeHudMoreMenu();
    try {
      vitainkRito = await fetchJSON("/api/vitaink/rito");
    } catch (_) {
      vitainkRito = null;
    }
    renderVitainkRito();
    const panel = $("#vitaink-rito-panel");
    if (panel) panel.classList.remove("hidden");
  }
  function closeVitainkRito() {
    const panel = $("#vitaink-rito-panel");
    if (panel) panel.classList.add("hidden");
  }
  function renderVitainkRito() {
    const meta = $("#vitaink-rito-meta");
    const list = $("#vitaink-rito-list");
    const fb = $("#vitaink-rito-fb");
    const r = vitainkRito;
    if (meta) {
      if (!r || !r.maestro_id) {
        meta.textContent = "Sigue a un maestro primario (panel Maestros) para abrir el rito.";
      } else {
        meta.textContent = (r.emoji || "") + " " + (r.display_name || r.maestro_id) +
          " · día " + (r.dia_local || "") +
          (r.hecho_hoy ? " · ya celebrado hoy" : " · pendiente");
      }
    }
    if (!list) return;
    list.innerHTML = "";
    const hecho = !!(r && r.hecho_hoy);
    for (const ref of ((r && r.reflexiones) || [])) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "rito-chip";
      b.disabled = hecho || !r.maestro_id;
      b.textContent = ref.texto || ref.id;
      b.addEventListener("click", () => celebrarRito(ref.id).catch(() => {}));
      list.appendChild(b);
    }
    if (fb) fb.textContent = hecho ? "Rito ya celebrado hoy · vuelve mañana." : "";
  }
  async function celebrarRito(reflexionId) {
    const fb = $("#vitaink-rito-fb");
    try {
      const res = await fetchJSON("/api/vitaink/rito", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reflexion_id: reflexionId || undefined }),
      });
      if (res && res.ok) {
        const msg = res.ya_hecho_hoy
          ? "Ya celebrado hoy (idempotente)"
          : ("Rito · +" + (res.bonus_alineacion || 0) + " alineación");
        if (fb) fb.textContent = msg;
        setStatus(msg, "ok");
        vitainkRito = await fetchJSON("/api/vitaink/rito");
        renderVitainkRito();
        await fetchVitainkAlineacion();
      }
    } catch (e) {
      if (fb) fb.textContent = (e && e.message) || "No se pudo celebrar el rito";
    }
  }
  async function fetchVitainkPeregrinacion() {
    if (!vitainkOn || !vitainkAvailable) {
      vitainkPeregrinacion = null;
      return null;
    }
    try {
      vitainkPeregrinacion = await fetchJSON("/api/vitaink/peregrinacion");
    } catch (_) {
      vitainkPeregrinacion = null;
    }
    renderVitainkPeregrinacionPins();
    // Redibujar guiones sobre el grafo cívico cacheado (estilo ruta; coords desde API)
    if (homeViewMode === "calles" && streetsSvg) {
      try {
        if (citymapCache && citymapCache.nodes) {
          const byId = Object.create(null);
          for (const n of citymapCache.nodes) byId[n.id] = n;
          drawStreets(citymapCache, byId);
        } else {
          streetsSvg.querySelectorAll(".peregrinacion-line,.peregrinacion-line-outline,.peregrinacion-marker").forEach((el) => el.remove());
          drawPeregrinacionOverlay();
        }
      } catch (_) {}
    }
    return vitainkPeregrinacion;
  }

  /* —— v4.6 Códice de la senda + export diario .pucela —— */
  let vitainkCodice = null;
  async function fetchVitainkCodice(q) {
    const qs = (q && String(q).trim()) ? ("?q=" + encodeURIComponent(String(q).trim())) : "";
    vitainkCodice = await fetchJSON("/api/vitaink/codice" + qs);
    return vitainkCodice;
  }
  async function openVitainkCodice() {
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk para el códice", "err");
      return;
    }
    closeHudMoreMenu();
    const inp = $("#vitaink-codice-q");
    const q = inp ? inp.value : "";
    await fetchVitainkCodice(q);
    renderVitainkCodicePanel();
    const panel = $("#vitaink-codice-panel");
    if (panel) panel.classList.remove("hidden");
  }
  function closeVitainkCodice() {
    const panel = $("#vitaink-codice-panel");
    if (panel) panel.classList.add("hidden");
  }
  function renderVitainkCodicePanel() {
    const snap = vitainkCodice;
    const list = $("#vitaink-codice-list");
    const empty = $("#vitaink-codice-empty");
    const meta = $("#vitaink-codice-meta");
    const fb = $("#vitaink-codice-fb");
    if (fb) fb.textContent = "";
    const entries = (snap && snap.entries) || [];
    if (meta) {
      const q = snap && snap.query ? (' · filtro «' + snap.query + '»') : "";
      meta.textContent = (snap ? (snap.count + " / " + (snap.total != null ? snap.total : snap.count) + " fichas") : "—") + q;
    }
    if (list) list.innerHTML = "";
    if (!entries.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const e of entries) {
      const div = document.createElement("div");
      div.className = "codice-row";
      div.setAttribute("role", "listitem");
      const kind = e.kind || "";
      const when = e.at ? new Date(e.at * 1000).toLocaleString("es-ES", { dateStyle: "short", timeStyle: "short" }) : "";
      div.innerHTML =
        "<span class=\"codice-kind\">" + escapeHTML(kind) + "</span>" +
        "<strong>" + escapeHTML(e.title || "") + "</strong>" +
        (when ? "<span class=\"codice-when\">" + escapeHTML(when) + "</span>" : "") +
        "<p>" + escapeHTML(e.body || "") + "</p>";
      list.appendChild(div);
    }
  }
  async function exportDiarioPucela(fbEl) {
    const fb = fbEl || $("#vitaink-codice-fb") || $("#vitaink-maestros-fb");
    if (fb) fb.textContent = "Sellando diario .pucela…";
    try {
      const res = await fetch("/api/vitaink/diario/export.pucela", { method: "GET", credentials: "same-origin" });
      if (!res.ok) {
        let msg = "No se pudo exportar el diario";
        try {
          const j = await res.json();
          if (j && j.error) msg = j.error;
        } catch (_) {}
        throw new Error(msg);
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "diario-senda.pucela";
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 2000);
      if (fb) fb.textContent = "Diario exportado · diario-senda.pucela";
      setStatus("Diario exportado como .pucela", "ok");
    } catch (err) {
      if (fb) fb.textContent = err.message || "Error al exportar";
      setStatus(err.message || "Error al exportar diario", "err");
    }
  }

  async function openVitainkPeregrinacion() {
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk para la peregrinación", "err");
      return;
    }
    closeHudMoreMenu();
    await fetchVitainkPeregrinacion();
    renderVitainkPeregrinacionPanel();
    const panel = $("#vitaink-peregrinacion-panel");
    if (panel) panel.classList.remove("hidden");
  }
  function closeVitainkPeregrinacion() {
    const panel = $("#vitaink-peregrinacion-panel");
    if (panel) panel.classList.add("hidden");
  }
  function renderVitainkPeregrinacionPanel() {
    const snap = vitainkPeregrinacion;
    const meta = $("#vitaink-peregrinacion-meta");
    const list = $("#vitaink-peregrinacion-list");
    const actBox = $("#vitaink-peregrinacion-activa");
    const btnEtapa = $("#vitaink-peregrinacion-etapa");
    const titulos = $("#vitaink-peregrinacion-titulos");
    const fb = $("#vitaink-peregrinacion-fb");
    if (fb) fb.textContent = "";
    const act = snap && snap.activa;
    if (meta) {
      meta.textContent = act
        ? ((act.emoji || "🚶") + " " + (act.nombre || act.ruta_id) +
           " · etapa " + ((act.etapa_index || 0) + 1) + "/" + (act.total || "?") +
           (act.terminada ? " · terminada" : ""))
        : "Elige una ruta para caminar la senda en Calles.";
    }
    if (actBox) {
      if (act && !act.terminada && act.siguiente) {
        actBox.classList.remove("hidden");
        actBox.innerHTML =
          "<strong>Siguiente:</strong> " + escapeHTML((act.siguiente.emoji || "") + " " + (act.siguiente.nombre || act.siguiente.id)) +
          "<br><span class='muted'>" + escapeHTML(act.siguiente.nota || snap.cerca_hint || "") + "</span>";
      } else if (act && act.terminada) {
        actBox.classList.remove("hidden");
        const t = act.titulo;
        actBox.innerHTML = t
          ? ("Terminada · título " + escapeHTML((t.simbolo || "") + " " + (t.nombre || "")))
          : "Terminada · inicia otra ruta cuando quieras.";
      } else {
        actBox.classList.add("hidden");
        actBox.innerHTML = "";
      }
    }
    if (btnEtapa) {
      const show = !!(act && !act.terminada);
      btnEtapa.classList.toggle("hidden", !show);
    }
    if (list) {
      list.innerHTML = "";
      for (const r of ((snap && snap.rutas) || [])) {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "peregrinacion-ruta" + (act && act.ruta_id === r.id ? " active" : "");
        b.innerHTML =
          "<strong>" + escapeHTML((r.emoji || "") + " " + (r.nombre || r.id)) + "</strong>" +
          "<br><span class='muted small'>" + escapeHTML(r.descripcion || "") + "</span>";
        b.addEventListener("click", () => iniciarPeregrinacion(r.id).catch(() => {}));
        list.appendChild(b);
      }
    }
    if (titulos) {
      const ts = (snap && snap.titulos) || [];
      titulos.textContent = ts.length
        ? ts.map((t) => (t.simbolo || "") + " " + (t.nombre || t.id)).join(" · ")
        : "Aún no hay títulos de senda.";
    }
  }
  async function iniciarPeregrinacion(rutaId) {
    const fb = $("#vitaink-peregrinacion-fb");
    try {
      const res = await fetchJSON("/api/vitaink/peregrinacion/iniciar", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ruta_id: rutaId }),
      });
      if (res && res.ok) {
        setStatus("Peregrinación iniciada · camina las paradas", "ok");
        if (fb) fb.textContent = res.note || "Iniciada";
        await fetchVitainkPeregrinacion();
        renderVitainkPeregrinacionPanel();
      }
    } catch (e) {
      if (fb) fb.textContent = (e && e.message) || "No se pudo iniciar";
    }
  }
  async function completarEtapaPeregrinacion(opts) {
    opts = opts || {};
    const fb = $("#vitaink-peregrinacion-fb");
    const body = {};
    if (opts.cerca) {
      body.cerca = true;
      if (opts.stop_id) body.stop_id = opts.stop_id;
    } else if (opts.etapa_id) {
      body.etapa_id = opts.etapa_id;
    }
    try {
      const res = await fetchJSON("/api/vitaink/peregrinacion/etapa", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (res && res.ok) {
        const msg = res.terminada
          ? ("Senda terminada · " + ((res.titulo && (res.titulo.simbolo + " " + res.titulo.nombre)) || "título"))
          : ("Etapa · +" + (res.bonus_alineacion || 0) + " alineación");
        setStatus(msg, "ok");
        if (fb) fb.textContent = res.note || msg;
        await fetchVitainkPeregrinacion();
        renderVitainkPeregrinacionPanel();
        if (typeof fetchVitainkAlineacion === "function") await fetchVitainkAlineacion();
      }
    } catch (e) {
      if (fb) fb.textContent = (e && e.message) || "No se pudo completar etapa";
      if (!opts.silent) setStatus((e && e.message) || "Etapa fallida", "err");
    }
  }
  function renderVitainkPeregrinacionPins() {
    const box = $("#street-vitaink-peregrinacion");
    if (!box) return;
    box.innerHTML = "";
    if (!vitainkOn || !vitainkPeregrinacion || !vitainkPeregrinacion.activa) return;
    const act = vitainkPeregrinacion.activa;
    if (act.terminada) return;
    for (const s of (act.paradas || [])) {
      if (s.x == null || s.y == null) continue;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vita-peregrinacion-pin" + (s.actual ? " next" : "") + (s.hecha ? " hecha" : "");
      btn.style.left = Math.max(3, Math.min(97, s.x)) + "%";
      btn.style.top = Math.max(3, Math.min(97, s.y)) + "%";
      btn.dataset.stopId = s.id;
      btn.title = (s.nombre || s.id) + (s.actual ? " · siguiente" : "");
      btn.textContent = s.emoji || "📍";
      btn.addEventListener("click", (ev) => {
        ev.stopPropagation();
        if (s.actual) completarEtapaPeregrinacion({ etapa_id: s.id }).catch(() => {});
        else setStatus(s.hecha ? "Parada ya hecha" : "Sigue el orden de la senda", "ok");
      });
      box.appendChild(btn);
    }
  }
  function maybeAutoEtapaPeregrinacion() {
    if (!vitainkOn || !vitainkAvailable || !vitainkPeregrinacion || !vitainkPeregrinacion.activa) return;
    const act = vitainkPeregrinacion.activa;
    if (act.terminada || !act.siguiente) return;
    if (performance.now() < vitainkPeregrinacionAutoUntil) return;
    const s = act.siguiente;
    const d = Math.hypot(playerX - (s.x || 50), playerY - (s.y || 50));
    if (d > (typeof botRadius === "number" ? botRadius : 3.5)) return;
    vitainkPeregrinacionAutoUntil = performance.now() + 4000;
    completarEtapaPeregrinacion({ cerca: true, stop_id: s.id, silent: true }).catch(() => {});
  }

  async function tomarVotoMaestro() {
    if (!vitainkMaestroSel) { setMaestrosFb("Elige un maestro", true); return; }
    const vid = vitainkValorSel || "";
    if (!vid) { setMaestrosFb("Elige un valor (toca un chip) antes del voto", true); return; }
    const inp = $("#vitaink-voto-texto");
    const texto = inp ? inp.value.trim() : "";
    try {
      const res = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(vitainkMaestroSel) + "/voto", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ valor_id: vid, texto: texto || undefined }),
      });
      if (res && res.ok) {
        setMaestrosFb("Voto activo · " + ((res.voto && res.voto.valor_nombre) || vid));
        await fetchVitainkAlineacion();
        renderVitainkMaestroDetail();
      }
    } catch (e) {
      setMaestrosFb((e && e.message) || "No se pudo tomar el voto", true);
    }
  }
  async function renunciarVotoMaestro() {
    if (!vitainkMaestroSel) { setMaestrosFb("Elige un maestro", true); return; }
    try {
      const res = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(vitainkMaestroSel) + "/voto", {
        method: "DELETE",
      });
      if (res && res.ok) {
        setMaestrosFb("Voto renunciado · queda en el diario");
        await fetchVitainkAlineacion();
        renderVitainkMaestroDetail();
      }
    } catch (e) {
      setMaestrosFb((e && e.message) || "No se pudo renunciar", true);
    }
  }

  async function openVitainkSinodo() {
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk para el sínodo", "err");
      return;
    }
    const panel = $("#vitaink-sinodo-panel");
    if (!panel) return;
    closeHudMoreMenu();
    await fetchVitainkSinodo();
    renderVitainkSinodo();
    panel.classList.remove("hidden");
  }
  function closeVitainkSinodo() {
    const panel = $("#vitaink-sinodo-panel");
    if (panel) panel.classList.add("hidden");
  }
    async function leerVitainkLeccion(id, indice) {
    try {
      vitainkLecciones = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(id) + "/lecciones", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ indice: indice }),
      });
      await fetchVitainkDiario();
      renderVitainkMaestroDetail();
      setMaestrosFb("Lección leída · el diario y la siguiente se actualizan");
      await fetchVitainkCronica();
    } catch (e) {
      setMaestrosFb((e && e.message) || "No se pudo leer la lección", true);
    }
  }
  async function hacerVitainkPrueba(id, opcionId) {
    const fb = $("#vitaink-prueba-fb");
    try {
      const res = await fetchJSON("/api/vitaink/maestros/" + encodeURIComponent(id) + "/prueba", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ opcion_id: opcionId }),
      });
      await fetchVitainkAlineacion();
      await refreshVitainkSenda(id);
      renderVitainkMaestrosList();
      renderVitainkMaestroDetail();
      let msg;
      if (res && res.exito) {
        msg = "Grado confirmado · " + (res.titulo || "");
        if (res.reliquia && res.reliquia.nombre) {
          msg += " · reliquia " + (res.reliquia.simbolo || "") + " " + res.reliquia.nombre;
        } else if (res.privilegio) {
          msg += " — " + res.privilegio;
        }
      } else {
        msg = (res && res.ensenanza) || "La senda enseña; el umbral espera.";
      }
      if (fb) fb.textContent = msg;
      setMaestrosFb(msg);
      await fetchVitainkCronica();
    } catch (e) {
      const m = (e && e.message) || "No se pudo completar la prueba";
      if (fb) fb.textContent = m;
      setMaestrosFb(m, true);
    }
  }
  function diosHeaders() {
    const h = { "Content-Type": "application/json" };
    if (vitainkDiosPin) h["X-Operator-Pin"] = vitainkDiosPin;
    return h;
  }
  async function refreshDiosOverview() {
    const box = $("#vitaink-dios-overview");
    if (!box) return;
    try {
      const q = vitainkDiosPin ? ("?pin=" + encodeURIComponent(vitainkDiosPin)) : "";
      const st = await fetchJSON("/api/vitaink/dios/estado" + q);
      const ov = st && st.overview;
      if (!ov) {
        box.innerHTML = "<span class=\"muted\">Sin overview (PIN requerido)</span>";
        return;
      }
      const cro = ov.ultima_cronica
        ? escapeHTML((ov.ultima_cronica.title || "") + " — " + (ov.ultima_cronica.body || "").slice(0, 80))
        : "—";
      const bots = (ov.bots || []).map((b) => {
        const on = b.enabled ? "ON" : "OFF";
        return (b.emoji || "") + " " + (b.display_name || b.id) + " " + on + "/" + (b.intensity || "med");
      }).join(" · ");
      box.innerHTML =
        "<strong>Overview Dios</strong>" +
        "Sedes: " + (ov.sedes_libre || 0) + " libres / " + (ov.sedes_claimed || 0) + " claimed (" + (ov.sedes_total || 0) + ")<br>" +
        "Monedas virtuales: local " + (ov.monedas_local || 0) + " · demos " + (ov.monedas_demos || 0) +
        " · sedes " + (ov.monedas_sedes || 0) + " · total " + (ov.monedas_totales_virtuales || 0) + "<br>" +
        "Personaje: " + (ov.personaje_existe ? (ov.personaje_suspendido ? "⛔ suspendido" : "✅ activo") : "sin crear") + "<br>" +
        "Bots: " + escapeHTML(bots || "—") + "<br>" +
        "Última crónica: " + cro;
    } catch (_) {
      box.innerHTML = "<span class=\"muted\">No se pudo cargar overview</span>";
    }
  }
  async function refreshDiosBotsPanel() {
    await refreshDiosOverview();
    const box = $("#vitaink-dios-bots");
    if (!box) return;
    let bots = [];
    try {
      const snap = await fetchJSON("/api/vitaink/bots");
      bots = (snap && snap.bots) || [];
      vitainkBots = bots.filter((b) => b.enabled);
    } catch (_) {}
    box.innerHTML = "";
    for (const b of bots) {
      const inten = b.intensity || "med";
      const row = document.createElement("div");
      row.className = "bot-row";
      const alma = botAlmaURL(b);
      const thumb = alma
        ? `<img class="vita-alma-thumb" src="${escapeHTML(alma)}" alt="" width="36" height="36" loading="lazy">`
        : `<span>${escapeHTML(b.emoji || "")}</span>`;
      const lema = b.lema ? `<em class="bot-lema">${escapeHTML(b.lema)}</em>` : "";
      row.innerHTML =
        `<span class="bot-idline">${thumb} ${escapeHTML(b.display_name || b.id)}</span>` +
        lema +
        `<label><input type="checkbox" data-bot="${escapeHTML(b.id)}" ${b.enabled ? "checked" : ""}> ON</label>` +
        `<select data-inten="${escapeHTML(b.id)}" aria-label="Intensidad ${escapeHTML(b.id)}">` +
        `<option value="low" ${inten === "low" ? "selected" : ""}>low</option>` +
        `<option value="med" ${inten === "med" ? "selected" : ""}>med</option>` +
        `<option value="high" ${inten === "high" ? "selected" : ""}>high</option>` +
        `</select>` +
        `<button type="button" class="btn-secondary btn-sm" data-tick="${escapeHTML(b.id)}">Tick</button>`;
      box.appendChild(row);
    }
    box.querySelectorAll("input[data-bot]").forEach((inp) => {
      inp.addEventListener("change", async () => {
        const id = inp.getAttribute("data-bot");
        const enabled = {};
        enabled[id] = !!inp.checked;
        try {
          await fetchJSON("/api/vitaink/dios/bots", {
            method: "POST", headers: diosHeaders(),
            body: JSON.stringify({ enabled }),
          });
          setDiosFb("Bot " + id + (inp.checked ? " ON" : " OFF"));
          await fetchVitainkMapa();
          await refreshDiosOverview();
        } catch (e) {
          setDiosFb((e && e.message) || "Error toggle bot", true);
          inp.checked = !inp.checked;
        }
      });
    });
    box.querySelectorAll("select[data-inten]").forEach((sel) => {
      sel.addEventListener("change", async () => {
        const id = sel.getAttribute("data-inten");
        const intensities = {};
        intensities[id] = sel.value;
        try {
          await fetchJSON("/api/vitaink/dios/intensidad", {
            method: "POST", headers: diosHeaders(),
            body: JSON.stringify({ intensities }),
          });
          setDiosFb("Intensidad " + id + " = " + sel.value);
          await refreshDiosOverview();
        } catch (e) {
          setDiosFb((e && e.message) || "Error intensidad", true);
        }
      });
    });
    box.querySelectorAll("button[data-tick]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-tick");
        try {
          const res = await fetchJSON("/api/vitaink/dios/bots/" + encodeURIComponent(id) + "/tick", {
            method: "POST", headers: diosHeaders(), body: "{}",
          });
          setDiosFb((res && res.message) || ("Tick " + id));
          await fetchVitainkMapa();
          await fetchVitainkPersonaje();
          await fetchVitainkCronica();
          await refreshDiosOverview();
        } catch (e) {
          setDiosFb((e && e.message) || "Error tick", true);
        }
      });
    });
    // Rellenar select de rivales demo desde ranking
    const sel = $("#vitaink-dios-target");
    if (sel) {
      const cur = sel.value || "local";
      sel.innerHTML = '<option value="local">Personaje local</option>';
      try {
        const rank = await fetchJSON("/api/vitaink/ranking?by=monedas");
        const rows = (rank && rank.monedas) || [];
        for (const e of rows) {
          if (e.demo && e.nombre) {
            const opt = document.createElement("option");
            opt.value = e.nombre;
            opt.textContent = e.nombre + " (demo)";
            sel.appendChild(opt);
          }
        }
      } catch (_) {}
      sel.value = cur;
    }
  }
  function setDiosFb(msg, err) {
    const fb = $("#vitaink-dios-fb");
    if (fb) {
      fb.textContent = msg || "";
      fb.classList.toggle("err", !!err);
    }
  }
  async function openVitainkDios() {
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk para el panel Dios", "err");
      return;
    }
    const panel = $("#vitaink-dios-panel");
    const body = $("#vitaink-dios-body");
    const auth = $("#vitaink-dios-auth");
    if (panel) panel.classList.remove("hidden");
    // Comprobar estado PIN
    try {
      const st = await fetchJSON("/api/vitaink/dios/estado" + (vitainkDiosPin ? ("?pin=" + encodeURIComponent(vitainkDiosPin)) : ""));
      vitainkDiosOk = !!st.authenticated;
      if (st.pin_required && !vitainkDiosOk) {
        if (auth) auth.classList.remove("hidden");
        if (body) body.classList.add("hidden");
      } else {
        vitainkDiosOk = true;
        if (auth) auth.classList.add("hidden");
        if (body) body.classList.remove("hidden");
        await refreshDiosBotsPanel();
      }
      updateVitainkHUD();
    } catch (e) {
      setStatus("No se pudo abrir panel Dios", "err");
    }
  }
  function closeVitainkDios() {
    const panel = $("#vitaink-dios-panel");
    if (panel) panel.classList.add("hidden");
  }

  async function openVitainkRanking() {
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk para el ranking", "err");
      return;
    }
    const panel = $("#vitaink-ranking-panel");
    if (!panel) return;
    closeHudMoreMenu();
    syncVitainkRankTabs();
    const snap = await fetchVitainkRanking(vitainkRankTab);
    renderVitainkRanking(snap || vitainkRanking);
    panel.classList.remove("hidden");
  }
  function closeVitainkRanking() {
    const panel = $("#vitaink-ranking-panel");
    if (panel) panel.classList.add("hidden");
  }
  // Menú «Más»: colapsa chips secundarios en móvil; cívico funciona sin VitaInk.
  function closeHudMoreMenu() {
    const menu = $("#hud-more-menu");
    const btn = $("#hud-more");
    if (menu) menu.classList.add("hidden");
    if (btn) btn.setAttribute("aria-expanded", "false");
  }
  function toggleHudMoreMenu() {
    const menu = $("#hud-more-menu");
    const btn = $("#hud-more");
    if (!menu || !btn) return;
    // On wide screens menu uses display:contents; toggle is a no-op visually but keep aria honest on narrow.
    const open = menu.classList.contains("hidden");
    menu.classList.toggle("hidden", !open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  async function openVitainkMisiones() {
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk para las misiones de juego", "err");
      return;
    }
    const panel = $("#vitaink-misiones-panel");
    if (!panel) return;
    const snap = await fetchVitainkMisiones();
    renderVitainkMisionesAlbum(snap || vitainkMisiones);
    panel.classList.remove("hidden");
  }
  function closeVitainkMisiones() {
    const panel = $("#vitaink-misiones-panel");
    if (panel) panel.classList.add("hidden");
  }
  async function reclamarTesoroCercano(id) {
    const tid = id || nearTesoroId;
    if (!tid || !vitainkOn || !vitainkAvailable) return;
    try {
      const res = await fetchJSON("/api/vitaink/tesoros/" + encodeURIComponent(tid) + "/reclamar", { method: "POST" });
      setStatus((res && res.message) || "Tesoro reclamado (virtual)", "ok");
      await fetchVitainkPersonaje();
      await fetchVitainkTesoros();
      await fetchVitainkMisiones();
      fillVitainkPjForm(vitainkPersonaje);
      highlightNearPois();
    } catch (e) {
      setStatus((e && e.message) || "No se pudo reclamar el tesoro", "err");
      await fetchVitainkTesoros();
    }
  }
  async function setVitainkOn(on) {
    vitainkOn = !!on;
    capasState.vitaink = vitainkOn;
    saveCapasPref();
    applyCapas();
    if (vitainkOn && vitainkAvailable) {
      // Al activar VitaInk, modo limpio ON por defecto (menos chrome cívico).
      if (!juegoLimpio) setJuegoLimpio(true);
      else applyJuegoLimpio();
      await fetchVitainkMapa();
      await fetchVitainkPersonaje();
      await fetchVitainkTesoros();
      await fetchVitainkMisiones();
    } else {
      if (on && !vitainkAvailable) {
        setStatus("VitaInk no está montado en este nodo", "err");
      }
      vitainkOn = false;
      capasState.vitaink = false;
      vitainkCasas = [];
      vitainkTesoros = [];
      renderVitainkCasas();
      renderVitainkTesoros();
      closeVitainkPjPanel();
      closeVitainkCasaSheet();
      closeVitainkMisiones();
      applyCapas();
      applyJuegoLimpio();
    }
    if (homeViewMode === "calles" && placeNodes.length) {
      renderStreetBuildings(placesCache.length ? placesCache : placesCacheFull);
    }
    if (currentPlace && currentPlace.id) {
      updatePlaceVitainkCard(currentPlace.id).catch(() => {});
    }
  }
  async function updatePlaceVitainkCard(placeId) {
    const box = $("#place-vitaink");
    if (!box) return;
    if (!vitainkOn) {
      box.classList.add("hidden");
      return;
    }
    try {
      const card = await fetchJSON("/api/vitaink/sede/" + encodeURIComponent(placeId));
      const badge = $("#vitaink-sede-badge");
      const owner = $("#vitaink-sede-owner");
      const coins = $("#vitaink-sede-coins");
      const note = $("#vitaink-sede-note");
      const claimRow = $("#vitaink-claim-row");
      const color = card.faction_color || "#94a3b8";
      box.style.setProperty("--vita-color", color);
      if (badge) badge.textContent = card.status === "libre" ? "🕊️" : "🎮";
      if (owner) {
        owner.innerHTML =
          `<span class="vitaink-dot" style="background:${escapeHTML(color)}"></span>` +
          (card.status === "libre"
            ? "<strong>Libre</strong> · nadie la ha conquistado (virtual)"
            : ("<strong>" + escapeHTML(card.faction_name || "") + "</strong> · " + escapeHTML(card.owner_label || "conquistado")));
      }
      if (coins) coins.textContent = "Monedas-sede (demo): " + (card.monedas_sede != null ? card.monedas_sede : 0);
      if (note) note.textContent = card.note || "Solo puntos virtuales · sin plata";
      if (claimRow) claimRow.classList.remove("hidden");
      // Prefer personaje faction in claim select
      const sel = $("#vitaink-claim-faction");
      if (sel && vitainkPersonaje && vitainkPersonaje.faccion_id) {
        sel.value = vitainkPersonaje.faccion_id;
      }
      box.classList.remove("hidden");
    } catch (_) {
      box.classList.add("hidden");
    }
  }
  async function claimVitainkSede() {
    if (!currentPlace || !currentPlace.id || !vitainkOn) return;
    const faction = ($("#vitaink-claim-faction") && $("#vitaink-claim-faction").value) || "explorador";
    const pin = ($("#vitaink-claim-pin") && $("#vitaink-claim-pin").value) || "";
    const ownerLabel = (vitainkPersonaje && vitainkPersonaje.nombre) || "Conquistado (demo local)";
    try {
      const res = await fetchJSON("/api/vitaink/claim", {
        method: "POST",
        body: JSON.stringify({
          place_id: currentPlace.id,
          faction_id: faction,
          pin: pin,
          owner_label: ownerLabel,
        }),
      });
      setStatus((res && res.message) || "Sede reclamada (virtual)", "ok");
      await fetchVitainkMapa();
      await fetchVitainkPersonaje();
      await fetchVitainkMisiones();
      fillVitainkPjForm(vitainkPersonaje);
      await updatePlaceVitainkCard(currentPlace.id);
      if (homeViewMode === "calles" && placeNodes.length) {
        renderStreetBuildings(placesCache.length ? placesCache : placesCacheFull);
      }
    } catch (e) {
      setStatus((e && e.message) || "No se pudo reclamar", "err");
    }
  }
  function fillVitainkPjForm(p) {
    const nom = $("#vitaink-pj-nombre");
    const fac = $("#vitaink-pj-faccion");
    const mon = $("#vitaink-pj-monedas");
    syncNaturalistaUI();
    if (p && p.exists) {
      if (nom) nom.value = p.nombre || "";
      if (fac && p.faccion_id) fac.value = p.faccion_id;
      if (mon) mon.textContent = "Monedas virtuales: " + (p.monedas != null ? p.monedas : 0);
      const rep = $("#vitaink-pj-rep");
      const badge = $("#vitaink-pj-rep-badge");
      const lab = p.reputacion_label || "Reputación";
      const n = p.reputacion != null ? p.reputacion : 0;
      if (rep) rep.textContent = lab + ": " + n;
      if (badge) {
        badge.textContent = lab + " " + n;
        badge.classList.remove("hidden");
      }
      applyMariFaceRecipeToUI(p.face || MARI_FACE_DEFAULT);
      applyMariBodyRecipeToUI(p.body || MARI_BODY_DEFAULT);
    } else {
      if (mon) mon.textContent = "Monedas virtuales: — (se crean 500 al guardar)";
      const rep = $("#vitaink-pj-rep");
      const badge = $("#vitaink-pj-rep-badge");
      if (rep) rep.textContent = "Reputación: —";
      if (badge) badge.classList.add("hidden");
      applyMariFaceRecipeToUI(MARI_FACE_DEFAULT);
      applyMariBodyRecipeToUI(MARI_BODY_DEFAULT);
    }
    refreshMariFacePreviews().catch(() => {});
  }
  async function refreshVitainkHistorial() {
    const box = $("#vitaink-historial");
    const empty = $("#vitaink-historial-empty");
    if (!box) return;
    try {
      const data = await fetchJSON("/api/vitaink/historial");
      const rows = data.historial || [];
      const mon = $("#vitaink-pj-monedas");
      if (mon && data.monedas != null) mon.textContent = "Monedas virtuales: " + data.monedas;
      box.innerHTML = "";
      if (!rows.length) {
        if (empty) empty.classList.remove("hidden");
        return;
      }
      if (empty) empty.classList.add("hidden");
      for (const tx of rows.slice(0, 40)) {
        const row = document.createElement("div");
        row.className = "tx-row";
        row.setAttribute("role", "listitem");
        const amt = tx.amount || 0;
        row.innerHTML =
          `<span>${escapeHTML(tx.label || tx.kind || "")}</span>` +
          `<span class="tx-amt ${amt >= 0 ? "pos" : "neg"}">${amt >= 0 ? "+" : ""}${amt}</span>`;
        box.appendChild(row);
      }
    } catch (_) {
      box.innerHTML = "";
      if (empty) empty.classList.remove("hidden");
    }
  }
  async function openVitainkPjPanel() {
    if (!vitainkOn || !vitainkAvailable) {
      setStatus("Activa VitaInk en Capas para el personaje", "err");
      return;
    }
    const panel = $("#vitaink-pj-panel");
    if (!panel) return;
    await ensureMariFaceCatalog();
    wireMariFaceControls();
    await ensureMariBodyCatalog();
    wireMariBodyControls();
    await fetchVitainkPersonaje();
    fillVitainkPjForm(vitainkPersonaje);
    await fetchVitainkMaestros();
    await fetchVitainkReliquias();
    renderVitainkPjReliquias();
    await refreshVitainkHistorial();
    panel.classList.remove("hidden");
  }
  function closeVitainkPjPanel() {
    const panel = $("#vitaink-pj-panel");
    if (panel) panel.classList.add("hidden");
  }
  async function saveVitainkPersonaje() {
    const nombre = ($("#vitaink-pj-nombre") && $("#vitaink-pj-nombre").value || "").trim();
    const faccion = ($("#vitaink-pj-faccion") && $("#vitaink-pj-faccion").value) || "explorador";
    const face = readMariFaceRecipeFromUI();
    const body = readMariBodyRecipeFromUI();
    mariFaceRecipe = face;
    mariBodyRecipe = body;
    const fb = $("#vitaink-pj-feedback");
    try {
      const data = await fetchJSON("/api/vitaink/personaje", {
        method: "POST",
        body: JSON.stringify({ nombre: nombre, faccion_id: faccion, face: face, body: body }),
      });
      vitainkPersonaje = data.personaje || null;
      mirrorPersonajeLS(vitainkPersonaje);
      fillVitainkPjForm(vitainkPersonaje);
      updateVitainkHUD();
      await refreshVitainkHistorial();
      await refreshMariFacePreviews();
      if (typeof applyPlayerAvatarLook === "function") applyPlayerAvatarLook();
      if (fb) fb.textContent = "Personaje + rostro + silueta guardados (virtual)";
      setStatus("Personaje VitaInk guardado", "ok");
    } catch (e) {
      if (fb) fb.textContent = (e && e.message) || "Error";
      setStatus((e && e.message) || "No se pudo guardar", "err");
    }
  }
  async function transferVitainkStub() {
    const to = ($("#vitaink-tr-to") && $("#vitaink-tr-to").value || "").trim();
    const amt = parseInt(($("#vitaink-tr-amt") && $("#vitaink-tr-amt").value) || "0", 10);
    try {
      const res = await fetchJSON("/api/vitaink/transfer", {
        method: "POST",
        body: JSON.stringify({ to_label: to, amount: amt }),
      });
      setStatus((res && res.message) || "Transferencia registrada", "ok");
      await fetchVitainkPersonaje();
      fillVitainkPjForm(vitainkPersonaje);
      await refreshVitainkHistorial();
    } catch (e) {
      setStatus((e && e.message) || "Transferencia fallida", "err");
    }
  }
  async function openVitainkCasa(id) {
    currentVitaCasaId = id;
    const sheet = $("#vitaink-casa-sheet");
    if (!sheet) return;
    try {
      const card = await fetchJSON("/api/vitaink/casa/" + encodeURIComponent(id));
      const title = $("#vitaink-casa-title");
      const owner = $("#vitaink-casa-owner");
      const coins = $("#vitaink-casa-coins");
      const note = $("#vitaink-casa-note");
      if (title) title.textContent = (card.emoji || "🏠") + " " + (card.label || "Casa VitaInk");
      const color = card.faction_color || "#94a3b8";
      const cardEl = sheet.querySelector(".civic-sheet-card");
      if (cardEl) cardEl.style.setProperty("--vita-color", color);
      if (owner) {
        owner.innerHTML =
          `<span class="vitaink-dot" style="background:${escapeHTML(color)}"></span>` +
          (card.status === "libre"
            ? "<strong>Libre</strong> · casa virtual sin dueño"
            : ("<strong>" + escapeHTML(card.faction_name || "") + "</strong> · " + escapeHTML(card.owner_label || "")));
      }
      if (coins) coins.textContent = "Monedas-casa (demo): " + (card.monedas_casa != null ? card.monedas_casa : 0);
      if (note) note.textContent = card.note || "Solo virtual · no es Mi casa cívica";
      const sel = $("#vitaink-casa-faction");
      if (sel && vitainkPersonaje && vitainkPersonaje.faccion_id) sel.value = vitainkPersonaje.faccion_id;
      sheet.classList.remove("hidden");
    } catch (e) {
      setStatus((e && e.message) || "Casa no disponible", "err");
    }
  }
  function closeVitainkCasaSheet() {
    const sheet = $("#vitaink-casa-sheet");
    if (sheet) sheet.classList.add("hidden");
    currentVitaCasaId = null;
  }
  async function claimVitainkCasa() {
    if (!currentVitaCasaId || !vitainkOn) return;
    const faction = ($("#vitaink-casa-faction") && $("#vitaink-casa-faction").value) || "explorador";
    const pin = ($("#vitaink-casa-pin") && $("#vitaink-casa-pin").value) || "";
    const ownerLabel = (vitainkPersonaje && vitainkPersonaje.nombre) || "";
    try {
      const res = await fetchJSON("/api/vitaink/casa/claim", {
        method: "POST",
        body: JSON.stringify({
          casa_id: currentVitaCasaId,
          faction_id: faction,
          pin: pin,
          owner_label: ownerLabel,
        }),
      });
      setStatus((res && res.message) || "Casa reclamada (virtual)", "ok");
      await fetchVitainkMapa();
      await fetchVitainkPersonaje();
      await fetchVitainkMisiones();
      fillVitainkPjForm(vitainkPersonaje);
      await openVitainkCasa(currentVitaCasaId);
    } catch (e) {
      setStatus((e && e.message) || "No se pudo reclamar la casa", "err");
    }
  }

  function openCapasPanel() {
    const panel = $("#capas-panel");
    if (!panel) return;
    applyCapas();
    panel.classList.remove("hidden");
  }
  function closeCapasPanel() {
    const panel = $("#capas-panel");
    if (panel) panel.classList.add("hidden");
  }

  function formatETA(sec) {
    if (sec == null || sec < 0) return "—";
    if (sec < 60) return sec + " s";
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return s ? m + " min " + s + " s" : m + " min";
  }

  function nearestFromAvatar() {
    return "x=" + encodeURIComponent(playerX.toFixed(2)) + "&y=" + encodeURIComponent(playerY.toFixed(2));
  }

  async function fetchRouteTo(placeOrNode) {
    const q = nearestFromAvatar() + "&to=" + encodeURIComponent(placeOrNode);
    const route = await fetchJSON("/api/city/ruta?" + q);
    return route;
  }

  function showRouteBanner(route) {
    const banner = $("#route-banner");
    if (!banner) return;
    activeRoute = route;
    routeStepIndex = 0;
    const tip = $("#route-tip");
    const meta = $("#route-meta");
    if (tip) tip.textContent = (route.steps && route.steps[0] && route.steps[0].text) || ("Hacia " + (route.to_label || route.to));
    if (meta) {
      meta.textContent =
        "≈ " + (route.distance || 0) + " u. · a pie " + formatETA(route.eta_walk_sec) +
        " · bici " + formatETA(route.eta_bike_sec) +
        (route.to_label ? " · " + route.to_label : "");
    }
    banner.classList.remove("hidden");
    const hud = $("#hud-ruta");
    if (hud) hud.classList.add("ruta-active");
    if (citymapCache) {
      const byId = Object.create(null);
      for (const n of citymapCache.nodes || []) byId[n.id] = n;
      drawStreets(citymapCache, byId);
    } else {
      drawRouteOverlay();
    }
    renderPasosList();
    updateMiniMapaVisibility();
    updateMiniMapa();
  }

  function clearRoute() {
    activeRoute = null;
    routeNavigating = false;
    routeStepIndex = 0;
    routeDestPlaceId = null;
    const banner = $("#route-banner");
    if (banner) banner.classList.add("hidden");
    const hud = $("#hud-ruta");
    if (hud) hud.classList.remove("ruta-active");
    if (cityStreets) cityStreets.classList.remove("route-follow-on");
    closePasosSheet();
    applyVista();
    updateMiniMapaVisibility();
    updateMiniMapa();
    if (citymapCache) {
      const byId = Object.create(null);
      for (const n of citymapCache.nodes || []) byId[n.id] = n;
      drawStreets(citymapCache, byId);
    }
  }

  function startRouteNav() {
    if (!activeRoute || !activeRoute.found) return;
    routeNavigating = true;
    routeStepIndex = 0;
    setStatus("Ruta iniciada · sigue las indicaciones", "ok");
    openPasosSheet();
    updateRouteProgress();
    updateMiniMapaVisibility();
  }

  function updateRouteProgress() {
    if (!routeNavigating || !activeRoute) return;
    const steps = activeRoute.steps || [];
    const poly = activeRoute.polyline || [];
    // Advance tip when near upcoming step points
    let bestIdx = routeStepIndex;
    for (let i = routeStepIndex; i < steps.length; i++) {
      const s = steps[i];
      if (s.x == null) continue;
      const d = Math.hypot(playerX - s.x, playerY - s.y);
      if (d < 3.2) bestIdx = i;
    }
    routeStepIndex = bestIdx;
    const tip = $("#route-tip");
    if (tip && steps[routeStepIndex]) tip.textContent = steps[routeStepIndex].text;
    highlightPasosCurrent();
    // Arrive?
    if (poly.length) {
      const end = poly[poly.length - 1];
      if (Math.hypot(playerX - end.x, playerY - end.y) < 2.2) {
        if (tip) tip.textContent = steps.length ? steps[steps.length - 1].text : "Has llegado";
        setStatus("Has llegado", "ok");
        routeNavigating = false;
        highlightPasosCurrent();
      }
    }
  }

  function updateFollowCamera() {
    const stage = $("#streets-stage");
    if (!stage || !cityStreets) return;
    const z = (typeof callesZoom === "number" && isFinite(callesZoom)) ? callesZoom : 1;
    const rumbo = orientMode === "rumbo" && vistaMode !== "mirador";
    const headingRot = rumbo ? ("rotate(" + (-playerHeading) + "deg) ") : "";
    const followRoute = !!(routeFollow && activeRoute);
    // Zoom = escala del mundo (no traslación del personaje). Con zoom≠1 / rumbo /
    // seguir-ruta la cámara mantiene al avatar centrado en el viewport.
    const camFollow = followRoute || rumbo || Math.abs(z - 1) > 0.001;
    cityStreets.classList.toggle("route-follow-on", !!followRoute);
    cityStreets.classList.toggle("zoom-cam-on", camFollow);
    stage.style.transition = "none";
    let t = "";
    if (vistaMode === "mirador" && !camFollow) {
      stage.style.transformOrigin = "50% 50%";
      t = "scale(" + (0.52 * z).toFixed(4) + ")";
    } else if (vistaMode === "inclinada" && !camFollow) {
      stage.style.transformOrigin = "50% 85%";
      t = "rotateX(28deg) scale(" + (1.08 * z).toFixed(4) + ") translateY(-2%)";
    } else if (!camFollow) {
      stage.style.transformOrigin = "50% 50%";
      t = "";
    } else {
      // origin 0,0 + translate(50 - p*zScale) scale(zScale) → avatar en centro
      stage.style.transformOrigin = "0 0";
      let zScale = z;
      let yExtra = 0;
      if (vistaMode === "mirador") zScale = 0.72 * z;
      else if (vistaMode === "inclinada") { zScale = (followRoute ? 1.2 : 1.08) * z; yExtra = -2; }
      else if (followRoute) zScale = 1.18 * z;
      const mx = 50 - playerX * zScale;
      const my = 50 - playerY * zScale + yExtra;
      if (vistaMode === "inclinada") {
        t = headingRot + "rotateX(28deg) translate(" + mx.toFixed(3) + "%, " + my.toFixed(3) + "%) scale(" + zScale.toFixed(4) + ")";
      } else {
        t = headingRot + "translate(" + mx.toFixed(3) + "%, " + my.toFixed(3) + "%) scale(" + zScale.toFixed(4) + ")";
      }
    }
    stage.style.transform = t;
  }

  async function setRouteDestination(placeId) {
    routeDestPlaceId = placeId;
    closeRutaPanel();
    setHomeViewMode("calles");
    try {
      await ensureCitymap();
      const route = await fetchRouteTo(placeId);
      if (!route.found) {
        setStatus(route.error || "No hay ruta", "err");
        return;
      }
      showRouteBanner(route);
      setStatus("Ruta lista · " + (route.to_label || placeId), "ok");
    } catch (e) {
      setStatus(e.message || "Error de ruta", "err");
    }
  }

  function openRutaPanel(tab) {
    const panel = $("#ruta-panel");
    if (!panel) return;
    panel.classList.remove("hidden");
    setRutaTab(tab || "dest");
    fillRutaDestList();
    if (tab === "cerca") loadCercaList().catch(() => {});
  }
  function closeRutaPanel() {
    const panel = $("#ruta-panel");
    if (panel) panel.classList.add("hidden");
  }
  function setRutaTab(tab) {
    const destPane = $("#ruta-dest-pane");
    const cercaPane = $("#ruta-cerca-pane");
    const tDest = $("#ruta-tab-dest");
    const tCerca = $("#ruta-tab-cerca");
    const isCerca = tab === "cerca";
    if (destPane) destPane.classList.toggle("hidden", isCerca);
    if (cercaPane) cercaPane.classList.toggle("hidden", !isCerca);
    if (tDest) tDest.classList.toggle("active", !isCerca);
    if (tCerca) tCerca.classList.toggle("active", isCerca);
    if (isCerca) loadCercaList().catch(() => {});
  }
  function fillRutaDestList(filter) {
    const box = $("#ruta-dest-list");
    if (!box) return;
    const q = (filter || "").trim().toLowerCase();
    const list = (placesCacheFull || placesCache || []).slice();
    list.sort((a, b) => (a.name || "").localeCompare(b.name || "", "es"));
    box.innerHTML = "";
    let n = 0;
    for (const p of list) {
      const hay = ((p.name || "") + " " + (p.id || "") + " " + (p.category || "")).toLowerCase();
      if (q && hay.indexOf(q) < 0) continue;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "ruta-list-item";
      btn.setAttribute("role", "listitem");
      btn.innerHTML =
        `<span aria-hidden="true">${escapeHTML(p.emoji || "📍")}</span>` +
        `<span><strong>${escapeHTML(p.name || p.id)}</strong>` +
        `<div class="meta">${escapeHTML(zoneLabel(p.zone) || p.category || "")}</div></span>`;
      btn.addEventListener("click", () => setRouteDestination(p.id));
      box.appendChild(btn);
      n++;
      if (n >= 40) break;
    }
    if (!n) {
      const empty = document.createElement("p");
      empty.className = "empty";
      empty.textContent = "Ningún lugar coincide.";
      box.appendChild(empty);
    }
  }
  async function loadCercaList() {
    const box = $("#ruta-cerca-list");
    if (!box) return;
    box.innerHTML = "<p class='hint'>Calculando…</p>";
    try {
      const snap = await fetchJSON("/api/city/cerca?" + nearestFromAvatar() + "&limit=25");
      box.innerHTML = "";
      for (const p of snap.places || []) {
        if (p.distance === 0) continue; // skip self-ish
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "ruta-list-item";
        btn.setAttribute("role", "listitem");
        const eta = Math.max(1, Math.ceil((p.distance || 0) / (bikeMode ? BIKE_SPEED : WALK_SPEED)));
        btn.innerHTML =
          `<span aria-hidden="true">${escapeHTML(p.emoji || "📍")}</span>` +
          `<span><strong>${escapeHTML(p.label || p.place_id)}</strong>` +
          `<div class="meta">≈ ${p.distance} u. · ~${eta} s · ${escapeHTML(zoneLabel(p.zone) || "")}</div></span>`;
        btn.addEventListener("click", () => setRouteDestination(p.place_id));
        const openBtn = document.createElement("button");
        openBtn.type = "button";
        openBtn.className = "btn-secondary btn-sm";
        openBtn.textContent = "Abrir";
        openBtn.addEventListener("click", (ev) => {
          ev.stopPropagation();
          closeRutaPanel();
          openPlace(p.place_id).catch(() => {});
        });
        btn.appendChild(openBtn);
        box.appendChild(btn);
      }
      if (!box.children.length) {
        box.innerHTML = "<p class='empty'>No hay lugares cercanos en el grafo.</p>";
      }
    } catch (e) {
      box.innerHTML = "<p class='empty'>" + escapeHTML(e.message || "Error") + "</p>";
    }
  }


  /* —— v3.0 helpers —— */
  function headingCardinal(deg) {
    const d = ((deg % 360) + 360) % 360;
    if (d >= 315 || d < 45) return "N";
    if (d < 135) return "E";
    if (d < 225) return "S";
    return "O";
  }

  function updateBrujulaUI() {
    const dial = $("#brujula-dial");
    const label = $("#hud-brujula-label");
    const hud = $("#hud-brujula");
    const card = headingCardinal(playerHeading);
    if (label) label.textContent = card;
    // Norte arriba: dial rotates with heading (needle = facing).
    // Rumbo arriba: dial keeps N absolute → rotate by -heading so N points true north on chip.
    const rot = orientMode === "rumbo" ? -playerHeading : playerHeading;
    if (dial) dial.style.setProperty("--brujula-rot", rot + "deg");
    if (hud) {
      hud.title = "Brújula · " + card + " · " + (orientMode === "rumbo" ? "Rumbo arriba" : "Norte arriba");
      hud.classList.toggle("brujula-active", orientMode === "rumbo");
      hud.setAttribute("aria-pressed", orientMode === "rumbo" ? "true" : "false");
    }
  }

  function loadOrientPref() {
    try {
      const o = localStorage.getItem(ORIENT_LS_KEY);
      if (o === "norte" || o === "rumbo") orientMode = o;
      minimapAlways = localStorage.getItem(MINIMAP_ALWAYS_KEY) === "1";
    } catch (_) {}
  }
  function saveOrientPref() {
    try {
      localStorage.setItem(ORIENT_LS_KEY, orientMode);
      localStorage.setItem(MINIMAP_ALWAYS_KEY, minimapAlways ? "1" : "0");
    } catch (_) {}
  }
  function setOrientMode(mode) {
    if (mode !== "norte" && mode !== "rumbo") return;
    orientMode = mode;
    saveOrientPref();
    document.querySelectorAll(".orient-choice").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.orient === orientMode);
    });
    updateBrujulaUI();
    updateFollowCamera();
    setStatus(orientMode === "rumbo" ? "Orientación · Rumbo arriba" : "Orientación · Norte arriba", "ok");
  }

  function updateMiniMapaVisibility() {
    const mm = $("#mini-mapa");
    if (!mm) return;
    const show = minimapAlways || !!(activeRoute && activeRoute.found);
    mm.classList.toggle("hidden", !show);
  }

  function updateMiniMapa() {
    const svg = $("#mini-mapa-svg");
    if (!svg) return;
    if (!citymapCache) {
      svg.innerHTML = "";
      return;
    }
    let html = "";
    const byId = Object.create(null);
    for (const n of citymapCache.nodes || []) byId[n.id] = n;
    for (const e of citymapCache.edges || []) {
      const a = byId[e.from], b = byId[e.to];
      if (!a || !b) continue;
      html += `<line class="mm-edge" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" />`;
    }
    if (activeRoute && activeRoute.found && activeRoute.polyline && activeRoute.polyline.length > 1) {
      let d = "";
      for (let i = 0; i < activeRoute.polyline.length; i++) {
        const p = activeRoute.polyline[i];
        d += (i ? " L " : "M ") + p.x + " " + p.y;
      }
      html += `<path class="mm-route" d="${d}" />`;
    }
    // facing triangle
    const rad = (playerHeading * Math.PI) / 180;
    const fx = playerX + Math.sin(rad) * 3.2;
    const fy = playerY - Math.cos(rad) * 3.2;
    html += `<circle class="mm-avatar" cx="${playerX}" cy="${playerY}" r="2.2" />`;
    html += `<polygon class="mm-facing" points="${fx},${fy} ${playerX + Math.cos(rad) * 1.6},${playerY + Math.sin(rad) * 1.6} ${playerX - Math.cos(rad) * 1.6},${playerY - Math.sin(rad) * 1.6}" />`;
    svg.innerHTML = html;
  }

  function renderPasosList() {
    const list = $("#pasos-list");
    if (!list) return;
    list.innerHTML = "";
    const steps = (activeRoute && activeRoute.steps) || [];
    steps.forEach((s, i) => {
      const li = document.createElement("li");
      li.dataset.idx = String(i);
      if (i < routeStepIndex) li.classList.add("done");
      if (i === routeStepIndex) li.classList.add("current");
      const street = s.street ? `<span class="paso-street">${escapeHTML(s.street)}</span>` : "";
      li.innerHTML =
        `<span class="paso-num" aria-hidden="true">${i + 1}</span>` +
        `<span><span class="paso-text">${escapeHTML(s.text || "")}</span>${street}</span>`;
      list.appendChild(li);
    });
    if (!steps.length) {
      list.innerHTML = "<li><span class='paso-num'>—</span><span class='paso-text'>Sin pasos</span></li>";
    }
  }

  function highlightPasosCurrent() {
    const list = $("#pasos-list");
    if (!list) return;
    const items = list.querySelectorAll("li");
    items.forEach((li) => {
      const i = parseInt(li.dataset.idx || "-1", 10);
      li.classList.toggle("done", i >= 0 && i < routeStepIndex);
      li.classList.toggle("current", i === routeStepIndex);
    });
    const cur = list.querySelector("li.current");
    if (cur && pasosOpen) {
      try { cur.scrollIntoView({ block: "nearest", behavior: "smooth" }); } catch (_) {}
    }
  }

  function openPasosSheet() {
    const sheet = $("#pasos-sheet");
    if (!sheet || !activeRoute) return;
    renderPasosList();
    highlightPasosCurrent();
    sheet.classList.remove("hidden");
    pasosOpen = true;
  }
  function closePasosSheet() {
    const sheet = $("#pasos-sheet");
    if (sheet) sheet.classList.add("hidden");
    pasosOpen = false;
  }

  function loadFavoritos() {
    try {
      const raw = localStorage.getItem(FAVORITOS_LS_KEY);
      const arr = raw ? JSON.parse(raw) : [];
      favoritosIds = Array.isArray(arr) ? arr.filter((x) => typeof x === "string") : [];
    } catch (_) {
      favoritosIds = [];
    }
  }
  function saveFavoritos() {
    try { localStorage.setItem(FAVORITOS_LS_KEY, JSON.stringify(favoritosIds)); } catch (_) {}
  }
  function isFavorito(id) {
    return !!id && favoritosIds.indexOf(id) >= 0;
  }
  function toggleFavorito(id) {
    if (!id) return false;
    const i = favoritosIds.indexOf(id);
    if (i >= 0) favoritosIds.splice(i, 1);
    else favoritosIds.push(id);
    saveFavoritos();
    updateFavoritoButton(id);
    const hud = $("#hud-favoritos");
    if (hud) hud.classList.toggle("favoritos-active", favoritosIds.length > 0);
    return isFavorito(id);
  }
  function updateFavoritoButton(id) {
    const btn = $("#btn-favorito");
    if (!btn) return;
    const on = isFavorito(id);
    btn.textContent = on ? "★ Favorito" : "☆ Favorito";
    btn.classList.toggle("fav-on", on);
    btn.setAttribute("aria-pressed", on ? "true" : "false");
    btn.title = on ? "Quitar de favoritos" : "Añadir a favoritos";
  }

  function openFavoritosPanel() {
    const panel = $("#favoritos-panel");
    if (!panel) return;
    fillFavoritosList();
    panel.classList.remove("hidden");
  }
  function closeFavoritosPanel() {
    const panel = $("#favoritos-panel");
    if (panel) panel.classList.add("hidden");
  }
  function fillFavoritosList() {
    const box = $("#favoritos-list");
    if (!box) return;
    box.innerHTML = "";
    const places = placesCacheFull || placesCache || [];
    const byId = Object.create(null);
    for (const p of places) byId[p.id] = p;
    if (!favoritosIds.length) {
      box.innerHTML = "<p class='empty'>Aún no hay favoritos. Ábrelo en un lugar y toca ★ Favorito.</p>";
      return;
    }
    for (const id of favoritosIds) {
      const p = byId[id] || { id, name: id, emoji: "📍" };
      const row = document.createElement("div");
      row.className = "ruta-list-item";
      row.setAttribute("role", "listitem");
      row.style.display = "flex";
      row.style.alignItems = "center";
      row.style.gap = "8px";
      row.innerHTML =
        `<span aria-hidden="true">${escapeHTML(p.emoji || "📍")}</span>` +
        `<span style="flex:1"><strong>${escapeHTML(p.name || id)}</strong>` +
        `<div class="meta">${escapeHTML(zoneLabel(p.zone) || p.category || "")}</div></span>`;
      const ir = document.createElement("button");
      ir.type = "button";
      ir.className = "btn-primary btn-sm";
      ir.textContent = "Ir aquí";
      ir.addEventListener("click", () => {
        closeFavoritosPanel();
        setRouteDestination(id).catch((e) => setStatus(e.message, "err"));
      });
      const open = document.createElement("button");
      open.type = "button";
      open.className = "btn-secondary btn-sm";
      open.textContent = "Abrir";
      open.addEventListener("click", () => {
        closeFavoritosPanel();
        openPlace(id).catch(() => {});
      });
      const unstar = document.createElement("button");
      unstar.type = "button";
      unstar.className = "btn-secondary btn-sm";
      unstar.textContent = "★";
      unstar.title = "Quitar";
      unstar.addEventListener("click", () => {
        toggleFavorito(id);
        fillFavoritosList();
      });
      row.appendChild(ir);
      row.appendChild(open);
      row.appendChild(unstar);
      box.appendChild(row);
    }
  }

  function bindV30UI() {
    loadOrientPref();
    loadFavoritos();
    document.querySelectorAll(".orient-choice").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.orient === orientMode);
    });
    const always = $("#minimapa-always");
    if (always) always.checked = minimapAlways;
    updateBrujulaUI();
    updateMiniMapaVisibility();
    const hudFav = $("#hud-favoritos");
    if (hudFav) {
      hudFav.classList.toggle("favoritos-active", favoritosIds.length > 0);
      hudFav.addEventListener("click", () => openFavoritosPanel());
    }
    const hudBru = $("#hud-brujula");
    if (hudBru) {
      hudBru.addEventListener("click", () => {
        // cycle orientation; long-press alternative = open vista panel
        setOrientMode(orientMode === "norte" ? "rumbo" : "norte");
      });
    }
    document.querySelectorAll(".orient-choice").forEach((btn) => {
      btn.addEventListener("click", () => setOrientMode(btn.dataset.orient));
    });
    if (always) {
      always.addEventListener("change", () => {
        minimapAlways = !!always.checked;
        saveOrientPref();
        updateMiniMapaVisibility();
        updateMiniMapa();
      });
    }
    const mm = $("#mini-mapa");
    if (mm) {
      mm.addEventListener("click", () => {
        setVista("mirador");
        setStatus("Mirador · vista del grafo", "ok");
      });
    }
    const pasosBtn = $("#route-pasos");
    if (pasosBtn) pasosBtn.addEventListener("click", () => {
      if (pasosOpen) closePasosSheet();
      else openPasosSheet();
    });
    const pasosClose = $("#pasos-close");
    if (pasosClose) pasosClose.addEventListener("click", closePasosSheet);
    const sheet = $("#pasos-sheet");
    if (sheet) {
      const handle = $("#pasos-handle") || sheet;
      handle.addEventListener("touchstart", (ev) => {
        if (!ev.touches || !ev.touches[0]) return;
        pasosTouchY0 = ev.touches[0].clientY;
      }, { passive: true });
      handle.addEventListener("touchend", (ev) => {
        if (pasosTouchY0 == null) return;
        const y = (ev.changedTouches && ev.changedTouches[0]) ? ev.changedTouches[0].clientY : pasosTouchY0;
        if (y - pasosTouchY0 > 48) closePasosSheet();
        pasosTouchY0 = null;
      }, { passive: true });
    }
    const favClose = $("#favoritos-panel-close");
    if (favClose) favClose.addEventListener("click", closeFavoritosPanel);
    const favPanel = $("#favoritos-panel");
    if (favPanel) favPanel.addEventListener("click", (ev) => { if (ev.target === favPanel) closeFavoritosPanel(); });
    const btnFav = $("#btn-favorito");
    if (btnFav) {
      btnFav.addEventListener("click", () => {
        const id = (currentPlace && currentPlace.id) || "";
        if (!id) return;
        const on = toggleFavorito(id);
        setStatus(on ? "Añadido a favoritos" : "Quitado de favoritos", "ok");
      });
    }
  }

  function bindV29UI() {
    loadVistaPref();
    loadCapasPref();
    try { routeFollow = localStorage.getItem(ROUTE_FOLLOW_KEY) === "1"; } catch (_) {}
    applyVista();
    applyCapas();
    bindCallesTools();
    probeVitaink().then((ok) => {
      if (ok && vitainkOn) {
        return Promise.all([fetchVitainkMapa(), fetchVitainkPersonaje(), fetchVitainkTesoros(), fetchVitainkMisiones()]).then(() => {
          if (homeViewMode === "calles" && placeNodes.length) renderStreetBuildings(placesCache);
        });
      }
      applyCapas();
    }).catch(() => {});

    const hudVista = $("#hud-vista");
    if (hudVista) hudVista.addEventListener("click", () => openVistaPanel());
    const hudRuta = $("#hud-ruta");
    if (hudRuta) hudRuta.addEventListener("click", () => openRutaPanel(activeRoute ? "dest" : "cerca"));
    const hudCapas = $("#hud-capas");
    if (hudCapas) hudCapas.addEventListener("click", () => openCapasPanel());

    document.querySelectorAll(".vista-choice").forEach((btn) => {
      btn.addEventListener("click", () => {
        setVista(btn.dataset.vista);
        closeVistaPanel();
      });
    });
    const vistaClose = $("#vista-panel-close");
    if (vistaClose) vistaClose.addEventListener("click", closeVistaPanel);
    const vistaPanel = $("#vista-panel");
    if (vistaPanel) vistaPanel.addEventListener("click", (ev) => { if (ev.target === vistaPanel) closeVistaPanel(); });

    const capasClose = $("#capas-panel-close");
    if (capasClose) capasClose.addEventListener("click", closeCapasPanel);
    const capasPanel = $("#capas-panel");
    if (capasPanel) capasPanel.addEventListener("click", (ev) => { if (ev.target === capasPanel) closeCapasPanel(); });
    ["paradas", "bancos", "sellos", "misiones", "clima", "vitaink"].forEach((key) => {
      const el = $("#capa-" + key);
      if (!el) return;
      el.addEventListener("change", () => {
        if (key === "vitaink") {
          setVitainkOn(!!el.checked).catch(() => {});
          return;
        }
        capasState[key] = !!el.checked;
        saveCapasPref();
        applyCapas();
        if (key === "sellos" || key === "misiones") {
          renderStreetBuildings(placesCache);
        }
      });
    });

    const hudVita = $("#hud-vitaink");
    if (hudVita) {
      hudVita.addEventListener("click", () => {
        setVitainkOn(!vitainkOn).then(() => {
          setStatus(vitainkOn ? "VitaInk ON · LARP virtual" : "VitaInk OFF · red cívica", "ok");
        }).catch(() => {});
      });
    }
    const btnClaim = $("#btn-vitaink-claim");
    if (btnClaim) btnClaim.addEventListener("click", () => claimVitainkSede().catch(() => {}));
    const hudPj = $("#hud-vitaink-pj");
    if (hudPj) hudPj.addEventListener("click", () => { closeHudMoreMenu(); openVitainkPjPanel().catch(() => {}); });
    const pjClose = $("#vitaink-pj-close");
    if (pjClose) pjClose.addEventListener("click", closeVitainkPjPanel);
    const pjPanel = $("#vitaink-pj-panel");
    if (pjPanel) pjPanel.addEventListener("click", (ev) => { if (ev.target === pjPanel) closeVitainkPjPanel(); });
    const btnPjSave = $("#btn-vitaink-pj-save");
    if (btnPjSave) btnPjSave.addEventListener("click", () => saveVitainkPersonaje().catch(() => {}));
    const natCb = $("#vitaink-pj-naturalista");
    if (natCb) {
      natCb.checked = !!mariNaturalista;
      natCb.addEventListener("change", () => {
        setMariNaturalista(!!natCb.checked).catch(() => {});
      });
    }
    const btnTr = $("#btn-vitaink-transfer");
    if (btnTr) btnTr.addEventListener("click", () => transferVitainkStub().catch(() => {}));
    const casaClose = $("#vitaink-casa-close");
    if (casaClose) casaClose.addEventListener("click", closeVitainkCasaSheet);
    const casaSheet = $("#vitaink-casa-sheet");
    if (casaSheet) casaSheet.addEventListener("click", (ev) => { if (ev.target === casaSheet) closeVitainkCasaSheet(); });
    const btnCasaClaim = $("#btn-vitaink-casa-claim");
    if (btnCasaClaim) btnCasaClaim.addEventListener("click", () => claimVitainkCasa().catch(() => {}));
    const hudTes = $("#hud-vitaink-tesoros");
    if (hudTes) hudTes.addEventListener("click", () => {
      if (!vitainkOn || !vitainkAvailable) return;
      const left = vitainkTesoros.filter((x) => !x.claimed).length;
      setStatus(left ? ("Tesoros · " + left + " por reclamar · acércate a un 💎") : "Todos los tesoros reclamados", "ok");
    });
    const hudVmis = $("#hud-vitaink-misiones");
    if (hudVmis) hudVmis.addEventListener("click", () => { closeHudMoreMenu(); openVitainkMisiones().catch(() => {}); });
    const vmisClose = $("#vitaink-misiones-close");
    if (vmisClose) vmisClose.addEventListener("click", closeVitainkMisiones);
    const vmisPanel = $("#vitaink-misiones-panel");
    if (vmisPanel) vmisPanel.addEventListener("click", (ev) => { if (ev.target === vmisPanel) closeVitainkMisiones(); });

    const hudRank = $("#hud-vitaink-ranking");
    if (hudRank) hudRank.addEventListener("click", () => openVitainkRanking().catch(() => {}));
    const hudDios = $("#hud-vitaink-dios");
    if (hudDios) hudDios.addEventListener("click", () => openVitainkDios().catch(() => {}));
    const hudMae = $("#hud-vitaink-maestros");
    if (hudMae) hudMae.addEventListener("click", () => { closeHudMoreMenu(); openVitainkMaestros().catch(() => {}); });
    const hudRel = $("#hud-vitaink-reliquias");
    if (hudRel) hudRel.addEventListener("click", () => openVitainkReliquias().catch(() => {}));
    const hudSyn = $("#hud-vitaink-sinodo");
    if (hudSyn) hudSyn.addEventListener("click", () => openVitainkSinodo().catch(() => {}));
    const hudRito = $("#hud-vitaink-rito");
    if (hudRito) hudRito.addEventListener("click", () => openVitainkRito().catch(() => {}));
    const ritoClose = $("#vitaink-rito-close");
    if (ritoClose) ritoClose.addEventListener("click", closeVitainkRito);
    const ritoPanel = $("#vitaink-rito-panel");
    if (ritoPanel) ritoPanel.addEventListener("click", (ev) => { if (ev.target === ritoPanel) closeVitainkRito(); });
    const hudPer = $("#hud-vitaink-peregrinacion");
    if (hudPer) hudPer.addEventListener("click", () => openVitainkPeregrinacion().catch(() => {}));
    const perClose = $("#vitaink-peregrinacion-close");
    if (perClose) perClose.addEventListener("click", closeVitainkPeregrinacion);
    const perPanel = $("#vitaink-peregrinacion-panel");
    if (perPanel) perPanel.addEventListener("click", (ev) => { if (ev.target === perPanel) closeVitainkPeregrinacion(); });
    const perEtapa = $("#vitaink-peregrinacion-etapa");
    if (perEtapa) perEtapa.addEventListener("click", () => completarEtapaPeregrinacion({}).catch(() => {}));
    const hudCod = $("#hud-vitaink-codice");
    if (hudCod) hudCod.addEventListener("click", () => openVitainkCodice().catch(() => {}));
    const codClose = $("#vitaink-codice-close");
    if (codClose) codClose.addEventListener("click", closeVitainkCodice);
    const codPanel = $("#vitaink-codice-panel");
    if (codPanel) codPanel.addEventListener("click", (ev) => { if (ev.target === codPanel) closeVitainkCodice(); });
    const btnCodBuscar = $("#btn-vitaink-codice-buscar");
    if (btnCodBuscar) btnCodBuscar.addEventListener("click", () => openVitainkCodice().catch(() => {}));
    const codQ = $("#vitaink-codice-q");
    if (codQ) {
      codQ.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter") {
          ev.preventDefault();
          openVitainkCodice().catch(() => {});
        }
      });
    }
    const btnCodExport = $("#btn-vitaink-codice-export");
    if (btnCodExport) btnCodExport.addEventListener("click", () => exportDiarioPucela($("#vitaink-codice-fb")).catch(() => {}));
    const btnMaeExport = $("#btn-vitaink-export-diario");
    if (btnMaeExport) btnMaeExport.addEventListener("click", () => exportDiarioPucela($("#vitaink-maestros-fb")).catch(() => {}));
    const btnVoto = $("#btn-vitaink-voto");
    if (btnVoto) btnVoto.addEventListener("click", () => tomarVotoMaestro().catch(() => {}));
    const btnVotoRen = $("#btn-vitaink-voto-renunciar");
    if (btnVotoRen) btnVotoRen.addEventListener("click", () => renunciarVotoMaestro().catch(() => {}));
    const relClose = $("#vitaink-reliquias-close");
    if (relClose) relClose.addEventListener("click", closeVitainkReliquias);
    const relPanel = $("#vitaink-reliquias-panel");
    if (relPanel) relPanel.addEventListener("click", (ev) => { if (ev.target === relPanel) closeVitainkReliquias(); });
    const synClose = $("#vitaink-sinodo-close");
    if (synClose) synClose.addEventListener("click", closeVitainkSinodo);
    const synPanel = $("#vitaink-sinodo-panel");
    if (synPanel) synPanel.addEventListener("click", (ev) => { if (ev.target === synPanel) closeVitainkSinodo(); });
    const maeClose = $("#vitaink-maestros-close");
    if (maeClose) maeClose.addEventListener("click", closeVitainkMaestros);
    const maePanel = $("#vitaink-maestros-panel");
    if (maePanel) maePanel.addEventListener("click", (ev) => { if (ev.target === maePanel) closeVitainkMaestros(); });
    const btnHablarAhora = $("#btn-vitaink-hablar-ahora");
    if (btnHablarAhora) {
      btnHablarAhora.addEventListener("click", () => {
        const id = vitainkMaestroSel;
        if (!id) { setMaestrosFb("Elige un maestro", true); return; }
        hablarConBotCercano(id).then((res) => {
          if (res && res.rate_limited) setMaestrosFb("Cooldown · " + (res.cooldown_left_sec || "?") + "s", true);
          else if (res) setMaestrosFb("Encuentro · " + (res.display_name || id));
        }).catch(() => {});
      });
    }
    const btnSeguir = $("#btn-vitaink-seguir");
    if (btnSeguir) btnSeguir.addEventListener("click", () => seguirVitainkMaestro(false).catch(() => {}));
    const btnSeguirSec = $("#btn-vitaink-seguir-sec");
    if (btnSeguirSec) btnSeguirSec.addEventListener("click", () => seguirVitainkMaestro(true).catch(() => {}));
    const btnDejar = $("#btn-vitaink-dejar");
    if (btnDejar) btnDejar.addEventListener("click", () => dejarVitainkMaestro().catch(() => {}));
    const btnDialogoLibre = $("#btn-vitaink-dialogo-libre");
    if (btnDialogoLibre) {
      btnDialogoLibre.addEventListener("click", () => {
        const inp = $("#vitaink-dialogo-libre");
        const q = inp ? inp.value.trim() : "";
        if (!vitainkMaestroSel) { setMaestrosFb("Elige un maestro", true); return; }
        if (!q) { setMaestrosFb("Escribe una pregunta libre", true); return; }
        dialogarConMaestro(vitainkMaestroSel, { pregunta_libre: q }).then((res) => {
          if (res && res.ok && inp) inp.value = "";
        }).catch(() => {});
      });
    }
    const dialogoLibreInp = $("#vitaink-dialogo-libre");
    if (dialogoLibreInp) {
      dialogoLibreInp.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter") {
          ev.preventDefault();
          const b = $("#btn-vitaink-dialogo-libre");
          if (b) b.click();
        }
      });
    }
    const encClose = $("#vita-encuentro-close");
    if (encClose) encClose.addEventListener("click", closeEncuentroToast);
    const encToast = $("#vita-encuentro-toast");
    if (encToast) encToast.addEventListener("click", (ev) => { if (ev.target === encToast) closeEncuentroToast(); });
    const hudCro = $("#hud-vitaink-cronica");
    if (hudCro) hudCro.addEventListener("click", () => openVitainkCronica().catch(() => {}));
    const diosClose = $("#vitaink-dios-close");
    if (diosClose) diosClose.addEventListener("click", closeVitainkDios);
    const croClose = $("#vitaink-cronica-close");
    if (croClose) croClose.addEventListener("click", closeVitainkCronica);
    const btnDiosAuth = $("#btn-vitaink-dios-auth");
    if (btnDiosAuth) btnDiosAuth.addEventListener("click", async () => {
      const pinEl = $("#vitaink-dios-pin");
      const pin = pinEl ? pinEl.value.trim() : "";
      const afb = $("#vitaink-dios-auth-fb");
      try {
        const res = await fetchJSON("/api/vitaink/dios/auth", {
          method: "POST", headers: { "Content-Type": "application/json", "X-Operator-Pin": pin },
          body: JSON.stringify({ pin }),
        });
        if (res && res.ok) {
          vitainkDiosPin = pin;
          vitainkDiosOk = true;
          if (afb) afb.textContent = "PIN OK";
          const auth = $("#vitaink-dios-auth");
          const body = $("#vitaink-dios-body");
          if (auth) auth.classList.add("hidden");
          if (body) body.classList.remove("hidden");
          updateVitainkHUD();
          await refreshDiosBotsPanel();
        }
      } catch (e) {
        if (afb) afb.textContent = (e && e.message) || "PIN incorrecto";
        vitainkDiosOk = false;
        updateVitainkHUD();
      }
    });
    const btnAj = $("#btn-vitaink-dios-ajustar");
    if (btnAj) btnAj.addEventListener("click", async () => {
      const target = ($("#vitaink-dios-target") || {}).value || "local";
      const dm = parseInt(($("#vitaink-dios-delta-mon") || {}).value || "0", 10);
      const dr = parseInt(($("#vitaink-dios-delta-rep") || {}).value || "0", 10);
      try {
        const res = await fetchJSON("/api/vitaink/dios/ajustar", {
          method: "POST", headers: diosHeaders(),
          body: JSON.stringify({ target, delta_monedas: dm, delta_reputacion: dr }),
        });
        setDiosFb((res && res.message) || "Ajustado");
        await fetchVitainkPersonaje();
        await fetchVitainkMapa();
        await refreshDiosOverview();
      } catch (e) { setDiosFb((e && e.message) || "Error", true); }
    });
    const btnEv = $("#btn-vitaink-dios-evento");
    if (btnEv) btnEv.addEventListener("click", async () => {
      const mode = ($("#vitaink-dios-evento-mode") || {}).value || "otorgar";
      const amount = parseInt(($("#vitaink-dios-evento-amt") || {}).value || "1", 10);
      const target = ($("#vitaink-dios-evento-target") || {}).value || "todos";
      const body = { mode, amount, target };
      if (mode === "plaga") body.percent = amount;
      if (mode === "otorgar") body.target = "local";
      if (mode === "redistribuir") body.target = "all_sedes";
      if (mode === "reset_tesoros") { body.amount = 0; }
      try {
        const res = await fetchJSON("/api/vitaink/dios/evento", {
          method: "POST", headers: diosHeaders(),
          body: JSON.stringify(body),
        });
        setDiosFb((res && res.message) || "Evento OK");
        await fetchVitainkPersonaje();
        await fetchVitainkMapa();
        await fetchVitainkTesoros();
        await fetchVitainkCronica();
        await refreshDiosOverview();
      } catch (e) { setDiosFb((e && e.message) || "Error", true); }
    });
    const btnLib = $("#btn-vitaink-dios-liberar");
    if (btnLib) btnLib.addEventListener("click", async () => {
      const place_id = (($("#vitaink-dios-liberar-id") || {}).value || "").trim();
      try {
        const res = await fetchJSON("/api/vitaink/dios/liberar", {
          method: "POST", headers: diosHeaders(),
          body: JSON.stringify({ place_id }),
        });
        setDiosFb((res && res.message) || "Sede liberada");
        await fetchVitainkMapa();
        await refreshDiosOverview();
      } catch (e) { setDiosFb((e && e.message) || "Error", true); }
    });
    async function diosSuspend(flag) {
      try {
        const res = await fetchJSON("/api/vitaink/dios/suspender", {
          method: "POST", headers: diosHeaders(),
          body: JSON.stringify({ suspendido: !!flag }),
        });
        setDiosFb((res && res.message) || (flag ? "Suspendido" : "Rehabilitado"));
        await fetchVitainkPersonaje();
        await fetchVitainkCronica();
        await refreshDiosOverview();
      } catch (e) { setDiosFb((e && e.message) || "Error", true); }
    }
    const btnSus = $("#btn-vitaink-dios-suspender");
    if (btnSus) btnSus.addEventListener("click", () => diosSuspend(true));
    const btnReh = $("#btn-vitaink-dios-rehabilitar");
    if (btnReh) btnReh.addEventListener("click", () => diosSuspend(false));
    const btnMsg = $("#btn-vitaink-dios-mensaje");
    if (btnMsg) btnMsg.addEventListener("click", async () => {
      const title = (($("#vitaink-dios-msg-title") || {}).value || "").trim();
      const body = (($("#vitaink-dios-msg-body") || {}).value || "").trim();
      try {
        const res = await fetchJSON("/api/vitaink/dios/mensaje", {
          method: "POST", headers: diosHeaders(),
          body: JSON.stringify({ title, body }),
        });
        setDiosFb((res && res.message) || "Mensaje publicado");
        await fetchVitainkCronica();
        await refreshDiosOverview();
      } catch (e) { setDiosFb((e && e.message) || "Error", true); }
    });
    const btnAud = $("#btn-vitaink-dios-auditoria");
    if (btnAud) btnAud.addEventListener("click", async () => {
      const box = $("#vitaink-dios-auditoria");
      if (!box) return;
      try {
        const q = vitainkDiosPin ? ("?pin=" + encodeURIComponent(vitainkDiosPin)) : "";
        const snap = await fetchJSON("/api/vitaink/dios/auditoria" + q);
        const entries = (snap && snap.entries) || [];
        box.classList.remove("hidden");
        box.innerHTML = "";
        if (!entries.length) {
          box.innerHTML = "<span class=\"muted\">Sin entradas de auditoría</span>";
          return;
        }
        for (const e of entries.slice(0, 40)) {
          const row = document.createElement("div");
          row.className = "aud-row";
          row.setAttribute("role", "listitem");
          row.innerHTML = `<strong>${escapeHTML(e.action || "")}</strong> · ${escapeHTML(e.what || "")}<br><span class="muted">${escapeHTML(e.detail || "")}</span>`;
          box.appendChild(row);
        }
        setDiosFb("Auditoría: " + entries.length + " entradas");
      } catch (e) { setDiosFb((e && e.message) || "Error auditoría", true); }
    });
    const rankClose = $("#vitaink-ranking-close");
    if (rankClose) rankClose.addEventListener("click", closeVitainkRanking);
    const rankPanel = $("#vitaink-ranking-panel");
    if (rankPanel) rankPanel.addEventListener("click", (ev) => { if (ev.target === rankPanel) closeVitainkRanking(); });
    const tabMon = $("#vitaink-rank-tab-monedas");
    if (tabMon) tabMon.addEventListener("click", () => {
      vitainkRankTab = "monedas";
      syncVitainkRankTabs();
      fetchVitainkRanking("monedas").then((s) => renderVitainkRanking(s)).catch(() => {});
    });
    const tabRep = $("#vitaink-rank-tab-rep");
    if (tabRep) tabRep.addEventListener("click", () => {
      vitainkRankTab = "reputacion";
      syncVitainkRankTabs();
      fetchVitainkRanking("reputacion").then((s) => renderVitainkRanking(s)).catch(() => {});
    });

    const hudMore = $("#hud-more");
    if (hudMore) hudMore.addEventListener("click", (ev) => {
      ev.stopPropagation();
      toggleHudMoreMenu();
    });
    document.addEventListener("click", (ev) => {
      const wrap = $("#hud-more-wrap");
      if (!wrap || wrap.contains(ev.target)) return;
      closeHudMoreMenu();
    });
    // Close Más after choosing a secondary chip (narrow HUD)
    const moreMenu = $("#hud-more-menu");
    if (moreMenu) {
      moreMenu.addEventListener("click", (ev) => {
        const btn = ev.target && ev.target.closest ? ev.target.closest(".hud-chip") : null;
        if (btn && btn.id !== "hud-more") {
          // defer close so the chip click handler still runs
          setTimeout(closeHudMoreMenu, 0);
        }
      });
    }

    const rutaClose = $("#ruta-panel-close");
    if (rutaClose) rutaClose.addEventListener("click", closeRutaPanel);
    const rutaPanel = $("#ruta-panel");
    if (rutaPanel) rutaPanel.addEventListener("click", (ev) => { if (ev.target === rutaPanel) closeRutaPanel(); });
    const tDest = $("#ruta-tab-dest");
    const tCerca = $("#ruta-tab-cerca");
    if (tDest) tDest.addEventListener("click", () => setRutaTab("dest"));
    if (tCerca) tCerca.addEventListener("click", () => setRutaTab("cerca"));
    const search = $("#ruta-dest-search");
    if (search) search.addEventListener("input", () => fillRutaDestList(search.value));

    const routeStart = $("#route-start");
    if (routeStart) routeStart.addEventListener("click", () => startRouteNav());
    const routeCancel = $("#route-cancel");
    if (routeCancel) routeCancel.addEventListener("click", () => {
      clearRoute();
      setStatus("Ruta cancelada", "ok");
    });
    const follow = $("#route-follow");
    if (follow) {
      follow.checked = routeFollow;
      follow.addEventListener("change", () => {
        routeFollow = !!follow.checked;
        try { localStorage.setItem(ROUTE_FOLLOW_KEY, routeFollow ? "1" : "0"); } catch (_) {}
        if (!routeFollow) {
          const stage = $("#streets-stage");
          if (stage) stage.style.transform = "";
          applyVista();
        } else updateFollowCamera();
      });
    }

    const ir = $("#btn-ir-aqui");
    if (ir) {
      ir.addEventListener("click", () => {
        const id = (currentPlace && currentPlace.id) || "";
        if (!id) return;
        setRouteDestination(id).catch((e) => setStatus(e.message, "err"));
      });
    }
  }

  function bindCityHUD() {
    const hudTod = $("#hud-tod");
    if (hudTod) {
      hudTod.addEventListener("click", () => {
        // cycle force for quick delight: auto → dia → atardecer → noche → auto
        const order = ["", "dia", "atardecer", "noche"];
        const i = order.indexOf(todForce);
        todForce = order[(i + 1) % order.length];
        saveTodPrefs();
        const sel = $("#nodo-tod-force");
        if (sel) sel.value = todForce;
        refreshTod();
        const m = todMeta(todForce || phaseFromHour(currentHour()));
        setStatus(todForce ? ("Fase · " + m.label) : "Fase · reloj local", "ok");
      });
    }
    const hudClima = $("#hud-clima");
    if (hudClima) {
      hudClima.addEventListener("click", () => {
        const order = ["", "sol", "nubes", "lluvia"];
        const i = order.indexOf(climaForce);
        climaForce = order[(i + 1) % order.length];
        saveClimaPrefs();
        const sel = $("#nodo-clima-force");
        if (sel) sel.value = climaForce;
        refreshClima();
        const m = climaMeta(climaForce || currentClimaSky());
        setStatus(climaForce ? ("Clima · " + m.label) : "Clima · ciclo local", "ok");
      });
    }
    const hudSt = $("#hud-stamps");
    if (hudSt) hudSt.addEventListener("click", () => showSellos().catch((e) => setStatus(e.message, "err")));
    const hudBike = $("#hud-bike");
    if (hudBike) hudBike.addEventListener("click", () => toggleBikeMode());
    const hudMis = $("#hud-missions");
    if (hudMis) hudMis.addEventListener("click", () => showMisiones().catch((e) => setStatus(e.message, "err")));
    const btnFooterMis = $("#btn-footer-misiones");
    if (btnFooterMis) btnFooterMis.addEventListener("click", () => showMisiones().catch((e) => setStatus(e.message, "err")));
    const dismiss = $("#event-toast-dismiss");
    if (dismiss) dismiss.addEventListener("click", dismissEventToast);
    const go = $("#event-toast-place");
    if (go) {
      go.addEventListener("click", () => {
        const id = eventToastPlaceId;
        dismissEventToast();
        if (id) openPlace(id).catch(() => {});
      });
    }
    const btnFooterSellos = $("#btn-footer-sellos");
    if (btnFooterSellos) btnFooterSellos.addEventListener("click", () => showSellos().catch((e) => setStatus(e.message, "err")));

    const hudParadas = $("#hud-paradas");
    if (hudParadas) {
      hudParadas.addEventListener("click", () => {
        if (nearParadaId) openLinePicker(nearParadaId);
        else if (cityParadas.length) {
          // walk hint: open picker from nearest or Plaza Mayor
          let best = cityParadas[0];
          let bestD = Infinity;
          for (const p of cityParadas) {
            const d = Math.hypot(playerX - p.x, playerY - p.y);
            if (d < bestD) { bestD = d; best = p; }
          }
          openLinePicker(best.id);
        } else setStatus("Paradas no cargadas", "err");
      });
    }
    const civicAct = $("#civic-action");
    if (civicAct) {
      civicAct.addEventListener("click", (ev) => {
        ev.stopPropagation();
        const a = civicAct.dataset.action;
        if (a === "linea") openLinePicker(nearParadaId);
        else if (a === "descansar") descansarEnBanco(nearBancoId);
        else if (a === "tesoro") reclamarTesoroCercano().catch(() => {});
        else if (a === "retiro") retiroEnErmita(civicAct.dataset.ermitaId || nearErmitaId).catch(() => {});
        else if (a === "hablar") hablarConBotCercano(civicAct.dataset.botId || nearBotId).catch(() => {});
      });
    }
    const lineCancel = $("#line-picker-cancel");
    if (lineCancel) lineCancel.addEventListener("click", closeLinePicker);
    const lineModal = $("#line-picker");
    if (lineModal) {
      lineModal.addEventListener("click", (ev) => {
        if (ev.target === lineModal) closeLinePicker();
      });
    }

    const demo = $("#nodo-tod-demo");
    const force = $("#nodo-tod-force");
    const fb = $("#nodo-tod-feedback");
    if (demo) {
      demo.checked = todDemo;
      demo.addEventListener("change", () => {
        todDemo = demo.checked;
        saveTodPrefs();
        restartTodLoop();
        if (fb) fb.textContent = todDemo ? "Demo acelerada activa" : "Reloj local";
      });
    }
    if (force) {
      force.value = todForce;
      force.addEventListener("change", () => {
        todForce = force.value || "";
        saveTodPrefs();
        refreshTod();
        if (fb) fb.textContent = todForce ? ("Fase forzada: " + todForce) : "Automático";
      });
    }

    const climaSel = $("#nodo-clima-force");
    const mercadoChk = $("#nodo-mercado-force");
    const climaFb = $("#nodo-clima-feedback");
    if (climaSel) {
      climaSel.value = climaForce;
      climaSel.addEventListener("change", () => {
        climaForce = climaSel.value || "";
        saveClimaPrefs();
        refreshClima();
        if (climaFb) climaFb.textContent = climaForce ? ("Clima forzado: " + climaForce) : "Ciclo sembrado";
      });
    }
    if (mercadoChk) {
      mercadoChk.checked = marketForce;
      mercadoChk.addEventListener("change", () => {
        marketForce = mercadoChk.checked;
        saveClimaPrefs();
        refreshMarketDay().then(() => loadCityEvents()).catch(() => {});
        if (climaFb) climaFb.textContent = marketForce ? "Día de mercado forzado (demo)" : "Mercado según miércoles/sábado";
      });
    }
  }

  function renderMapPins(list, allForDim) {
    if (!mapPins) return;
    mapPins.innerHTML = "";
    const hitIds = new Set((list || []).map((p) => p.id));
    const source = allForDim && allForDim.length ? allForDim : list;
    for (const p of source) {
      const x = typeof p.map_x === "number" ? p.map_x : 50;
      const y = typeof p.map_y === "number" ? p.map_y : 50;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "map-pin";
      if (list.length && !hitIds.has(p.id)) btn.classList.add("dim");
      else if (list.length && hitIds.has(p.id) && list.length < (allForDim || list).length) btn.classList.add("hit");
      btn.style.left = Math.max(4, Math.min(96, x)) + "%";
      btn.style.top = Math.max(4, Math.min(96, y)) + "%";
      btn.setAttribute("role", "listitem");
      btn.title = (p.name || "") + (p.zone ? " · " + zoneLabel(p.zone) : "");
      btn.setAttribute("aria-label", p.name || "Lugar");
      btn.innerHTML =
        `<span class="pin-emoji" aria-hidden="true">${escapeHTML(p.emoji || "📍")}</span>` +
        `<span class="pin-name">${escapeHTML(p.name || "")}</span>`;
      btn.addEventListener("click", () => openPlace(p.id));
      mapPins.appendChild(btn);
    }
  }

  function renderPlaces(list) {
    placesGrid.innerHTML = "";
    if (!list.length) {
      empty.classList.remove("hidden");
      if (mapPins) mapPins.innerHTML = "";
      return;
    }
    empty.classList.add("hidden");
    const q = (search && search.value || "").trim();
    // When filtering, keep full cache pins dimmed so the map stays a city
    const all = placesCacheFull && placesCacheFull.length ? placesCacheFull : list;
    renderMapPins(list, q ? all : list);
    if (citymapCache) renderStreetBuildings(list);
    for (const p of list) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "place-card";
      btn.setAttribute("role", "listitem");
      const zone = p.zone ? zoneLabel(p.zone) : categoryLabel(p.category);
      btn.innerHTML =
        `<span class="place-emoji" aria-hidden="true">${escapeHTML(p.emoji || "📍")}</span>` +
        `<strong>${escapeHTML(p.name)}</strong>` +
        `<span class="cat">${escapeHTML(zone)}</span>`;
      btn.addEventListener("click", () => openPlace(p.id));
      placesGrid.appendChild(btn);
    }
  }

  let placesCacheFull = [];

  async function loadPlaces(q) {
    const url = q ? `/api/places?q=${encodeURIComponent(q)}` : "/api/places";
    const data = await fetchJSON(url);
    placesCache = data.places || [];
    if (!q) placesCacheFull = placesCache.slice();
    renderPlaces(placesCache);
  }

  function fillSectionItems(elId, items) {
    const ul = $("#" + elId);
    if (!ul) return;
    ul.innerHTML = "";
    for (const it of items || []) {
      const li = document.createElement("li");
      li.textContent = it;
      ul.appendChild(li);
    }
  }

  function sectionById(sections, id) {
    return (sections || []).find((s) => s.id === id) || null;
  }

  async function openPlace(id, opts) {
    opts = opts || {};
    if (id === "federacion") {
      showFederacion();
      return;
    }
    stopPoll();
    const page = await fetchJSON(`/api/places/${encodeURIComponent(id)}/page`);
    const p = page.place || {};
    currentPlace = p;
    currentPeer = null;
    if (opts.fromCalles) {
      await presentVignette(p);
    }
    stampPlaceVisit(p.id || id).catch(() => {});
    $("#place-emoji").textContent = p.emoji || "📍";
    $("#place-name").textContent = p.name || "";
    $("#place-category").textContent = categoryLabel(p.category);
    $("#place-desc").textContent = p.description || "";
    updateFavoritoButton(p.id || id);
    updatePlaceVitainkCard(p.id || id).catch(() => {});

    // Tema visual del lugar (v4.7): torre-academia en Biblioteca, etc.
    applyPlaceTheme(viewPlace, page);

    const asst = $("#place-assistant");
    if (page.assistant && page.assistant.label) {
      $("#place-assistant-label").textContent = page.assistant.label;
      $("#place-assistant-note").textContent = page.assistant.note || "FAQ local offline · no es IA en la nube";
      asst.classList.remove("hidden");
      asst.dataset.ask = page.assistant.ask_path || `/api/places/${p.id}/asistente/ask`;
      asst.dataset.faq = page.assistant.faq_path || `/api/places/${p.id}/asistente/faq`;
    } else {
      asst.classList.add("hidden");
    }

    const info = sectionById(page.sections, "info");
    $("#tab-info-body").textContent = (info && info.body) || p.description || "";
    fillSectionItems("tab-info-items", info && info.items);
    const avisos = sectionById(page.sections, "avisos");
    fillSectionItems("tab-avisos-items", avisos && avisos.items);
    const contacto = sectionById(page.sections, "contacto");
    fillSectionItems("tab-contacto-items", contacto && contacto.items);
    const servicios = sectionById(page.sections, "servicios");
    const btnServ = $("#tab-btn-servicios");
    const tabsNav = $("#place-tabs");
    if (servicios) {
      fillSectionItems("tab-servicios-items", servicios.items);
      btnServ.classList.remove("hidden");
      tabsNav.classList.add("tabs-4");
      tabsNav.classList.remove("tabs-3");
    } else {
      fillSectionItems("tab-servicios-items", []);
      btnServ.classList.add("hidden");
      tabsNav.classList.remove("tabs-4");
      tabsNav.classList.add("tabs-3");
    }

    const stallsBox = $("#place-stalls");
    const stallsList = $("#stalls-list");
    const stallsTitle = $("#stalls-title");
    stallsList.innerHTML = "";
    const stalls = page.stalls || [];
    const createBox = $("#stall-create");
    if (createBox) createBox.classList.add("hidden");
    if (stalls.length || p.id === "mercado" || p.id === "centro-comercial" || p.id === "personas" || p.id === "residencial" || p.id === "prensa") {
      const kinds = new Set(stalls.map((s) => s.kind));
      let titleTxt = "Listado";
      if (kinds.has("puesto") || p.id === "mercado") titleTxt = "Puestos";
      else if (kinds.has("tienda") || p.id === "centro-comercial") titleTxt = "Tiendas";
      else if (kinds.has("persona") || p.id === "personas") titleTxt = "Personas";
      else if (kinds.has("portal")) titleTxt = "Portales y personas";
      else if (kinds.has("lugar")) titleTxt = "Lugares relacionados";
      else if (kinds.has("edicion") || p.id === "prensa") titleTxt = "Ediciones (hojas .pucela)";
      stallsTitle.textContent = titleTxt;
      for (const st of stalls) {
        const li = document.createElement("li");
        li.textContent = st.name;
        if (st.id && (st.kind === "lugar" || st.kind === "puesto" || st.kind === "tienda" || st.kind === "persona" || st.kind === "edicion")) {
          li.className = "stall-link";
          li.tabIndex = 0;
          li.setAttribute("role", "link");
          const go = () => {
            if (st.kind === "puesto" || st.kind === "tienda") return openShop(st.id);
            if (st.kind === "persona") return openPersona(st.id);
            if (st.kind === "edicion") return openEdition(st.id);
            return openPlace(st.id);
          };
          li.addEventListener("click", () => go().catch(() => {}));
          li.addEventListener("keydown", (ev) => {
            if (ev.key === "Enter") go().catch(() => {});
          });
        }
        stallsList.appendChild(li);
      }
      setupStallCreate(p.id);
      stallsBox.classList.remove("hidden");
    } else {
      stallsBox.classList.add("hidden");
    }

    const toolsBox = $("#place-tools");
    const toolsList = $("#tools-list");
    if (toolsBox && toolsList) {
      toolsList.innerHTML = "";
      const tools = page.tools || [];
      if (tools.length) {
        for (const tool of tools) {
          const li = document.createElement("li");
          li.className = "tool-card";
          li.tabIndex = 0;
          li.setAttribute("role", "button");
          li.innerHTML =
            `<strong>${escapeHTML(tool.name)}</strong>` +
            `<span class="tool-status">${escapeHTML(tool.status || "listo")}</span>` +
            `<span class="preview">${escapeHTML(tool.description || "")}</span>` +
            (tool.hint ? `<span class="preview">${escapeHTML(tool.hint)}</span>` : "");
          const open = () => openTool(tool, p.id);
          li.addEventListener("click", open);
          li.addEventListener("keydown", (ev) => {
            if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(); }
          });
          toolsList.appendChild(li);
        }
        toolsBox.classList.remove("hidden");
      } else {
        toolsBox.classList.add("hidden");
      }
    }

    setupMostrador(page, p).catch(() => {});
    setupTaller(page, p).catch(() => {});

    const prensaPub = $("#prensa-publish");
    if (prensaPub) {
      if (p.id === "prensa") {
        prensaPub.classList.remove("hidden");
        const fb = $("#prensa-publish-feedback");
        if (fb) fb.textContent = "";
      } else {
        prensaPub.classList.add("hidden");
      }
    }

    hideAllViews();
    viewPlace.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = p.name || "Lugar";
    subtitle.textContent = "Página del lugar";
    setNav("place");
    activateTab("info");
    history.pushState({ view: "place", id: p.id }, "", `/lugar/${p.id}`);
  }


  function openTool(tool, fromPlaceId) {
    toolReturnPlace = fromPlaceId || (currentPlace && currentPlace.id) || "herramientas";
    stopPoll();
    if (tool.open_url) {
      openToolFrame(tool);
      return;
    }
    switch (tool.workspace || tool.id) {
      case "wikipedia-offline":
        openToolWiki(tool);
        break;
      case "numeros-impresora-3d":
        openTool3d(tool);
        break;
      case "asistente-general":
        openToolAsistente(tool);
        break;
      case "panel-nodo":
        showNodoPanel();
        break;
      case "taller-comunitario":
        openPlace("taller-comunitario").catch((e) => setStatus(e.message, "err"));
        break;
      default:
        setStatus("Herramienta aún no colgada: " + (tool.name || tool.id), "err");
    }
  }

  function openToolFrame(tool) {
    hideAllViews();
    const iframe = $("#tool-iframe");
    if (iframe) iframe.src = tool.open_url;
    viewToolFrame.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = tool.name || "Herramienta";
    subtitle.textContent = "App local del nodo";
    setNav("tool");
    history.pushState({ view: "tool", tool: tool.id, place: toolReturnPlace }, "", `/herramienta/${encodeURIComponent(tool.id)}`);
  }

  async function openToolWiki(tool) {
    hideAllViews();
    viewToolWiki.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = tool.name || "Wikipedia offline";
    subtitle.textContent = "ZIM · Kiwix · sin nube";
    setNav("tool");
    history.pushState({ view: "tool-wiki", place: toolReturnPlace }, "", "/herramienta/wikipedia-offline");
    try {
      const st = await fetchJSON("/api/herramientas/wiki");
      $("#wiki-status-hint").textContent = st.hint || "";
      $("#wiki-instructions").textContent = st.instructions || "";
      const kiwixBtn = $("#wiki-open-kiwix");
      if (kiwixBtn) {
        const url = st.kiwix_url || "http://127.0.0.1:8081/";
        kiwixBtn.href = url;
        if (st.has_zim) {
          kiwixBtn.classList.remove("hidden");
          kiwixBtn.textContent = "Abrir Kiwix (" + url.replace(/^https?:\/\//, "").replace(/\/$/, "") + ")";
        } else {
          kiwixBtn.classList.add("hidden");
        }
      }
      const zimData = await fetchJSON("/api/herramientas/wiki/zims");
      const zimBox = $("#wiki-zims");
      if (zimBox) {
        zimBox.innerHTML = "";
        for (const z of zimData.zims || []) {
          const row = document.createElement("div");
          row.className = "thread-row";
          const sizeMiB = z.size ? (z.size / (1024 * 1024)).toFixed(1) + " MiB" : "0 B";
          row.innerHTML = `<strong>${escapeHTML(z.name)}</strong><span class="preview">${escapeHTML(z.status || "listo")} · ${sizeMiB}</span>`;
          zimBox.appendChild(row);
        }
        if (!(zimData.zims || []).length) {
          zimBox.innerHTML = `<p class="empty">Sin .zim. Descarga uno en library.kiwix.org y colócalo en data-dir/herramientas/wiki/pack/</p>`;
        }
      }
      const data = await fetchJSON("/api/herramientas/wiki/articles");
      const box = $("#wiki-articles");
      box.innerHTML = "";
      for (const a of data.articles || []) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "thread-row";
        btn.innerHTML = `<strong>${escapeHTML(a.title)}</strong><span class="preview">${escapeHTML(a.source)} · ${a.size || 0} B</span>`;
        btn.addEventListener("click", async () => {
          const doc = await fetchJSON(`/api/herramientas/wiki/articles/${encodeURIComponent(a.id)}`);
          $("#wiki-open-title").textContent = doc.title || a.title;
          $("#wiki-open-body").textContent = doc.body || "";
          $("#wiki-open-card").classList.remove("hidden");
        });
        box.appendChild(btn);
      }
      if (!(data.articles || []).length) {
        box.innerHTML = `<p class="empty">Sin artículos locales. La muestra debería aparecer al arrancar el nodo.</p>`;
      }
    } catch (e) {
      setStatus("Wiki: " + e.message, "err");
    }
  }

  function openTool3d(tool) {
    hideAllViews();
    viewTool3d.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = tool.name || "Impresora 3D";
    subtitle.textContent = "Hueco colgable";
    setNav("tool");
    history.pushState({ view: "tool-3d", place: toolReturnPlace }, "", "/herramienta/numeros-impresora-3d");
    runN3dPreview();
  }

  async function runN3dPreview() {
    const texto = ($("#n3d-texto") && $("#n3d-texto").value) || "123";
    try {
      const data = await fetchJSON("/api/herramientas/impresora3d/preview", {
        method: "POST",
        body: JSON.stringify({ texto }),
      });
      $("#n3d-note").textContent = data.note || "";
      $("#n3d-preview").innerHTML = data.svg || "";
    } catch (e) {
      $("#n3d-note").textContent = e.message;
    }
  }

  async function openToolAsistente(tool) {
    await openLocalAsistente({
      label: "Asistente local del nodo",
      ask: "/api/herramientas/asistente/ask",
      faq: "/api/herramientas/asistente/faq",
      path: "/herramienta/asistente",
      returnTo: { type: "place", id: toolReturnPlace || "herramientas" },
      hello: "Hola. Soy el asistente local del nodo. Pregúntame por la red, .pucela, puestos, personas o Mi casa.",
    });
  }

  async function openLocalAsistente(opts) {
    stopPoll();
    asistenteAskURL = opts.ask;
    asistenteFAQURL = opts.faq;
    asistenteReturn = opts.returnTo || null;
    hideAllViews();
    viewToolAsistente.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = opts.label || "Asistente local";
    subtitle.textContent = "FAQ offline · sin nube";
    setNav("tool");
    history.pushState({ view: "tool-asistente", asistente: true, returnTo: asistenteReturn }, "", opts.path || "/asistente");
    const log = $("#asistente-log");
    if (log) {
      log.innerHTML = `<div class="asistente-bubble">${escapeHTML(opts.hello || "Hola. Asistente local FAQ offline.")}</div>`;
    }
    try {
      const data = await fetchJSON(asistenteFAQURL);
      const ul = $("#asistente-faq");
      ul.innerHTML = "";
      for (const f of data.faq || []) {
        const li = document.createElement("li");
        li.textContent = f.question;
        li.style.cursor = "pointer";
        li.addEventListener("click", () => {
          $("#asistente-q").value = f.question;
          askAsistente(f.question);
        });
        ul.appendChild(li);
      }
    } catch (e) {
      setStatus("Asistente: " + e.message, "err");
    }
  }

  async function askAsistente(q) {
    const log = $("#asistente-log");
    const user = document.createElement("div");
    user.className = "asistente-bubble user";
    user.textContent = q;
    log.appendChild(user);
    try {
      const data = await fetchJSON(asistenteAskURL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ q }),
      });
      const bot = document.createElement("div");
      bot.className = "asistente-bubble";
      bot.textContent = data.answer || "(sin respuesta)";
      log.appendChild(bot);
    } catch (e) {
      const bot = document.createElement("div");
      bot.className = "asistente-bubble";
      bot.textContent = "Error: " + e.message;
      log.appendChild(bot);
    }
    log.scrollTop = log.scrollHeight;
  }

  function setupStallCreate(placeId) {
    const box = $("#stall-create");
    if (!box) return;
    const isShop = placeId === "mercado" || placeId === "centro-comercial";
    const isPerson = placeId === "personas" || placeId === "residencial";
    if (!isShop && !isPerson) {
      box.classList.add("hidden");
      return;
    }
    box.classList.remove("hidden");
    box.dataset.mode = isShop ? "shop" : "person";
    box.dataset.parent = placeId;
    $("#stall-create-title").textContent = isShop
      ? (placeId === "mercado" ? "Crear puesto" : "Crear tienda")
      : "Crear tarjeta de persona";
    $("#stall-create-name-label").textContent = isShop ? "Nombre del puesto/tienda" : "Nombre público";
    $("#stall-create-name").value = "";
    $("#stall-create-bio").value = "";
    $("#stall-create-feedback").textContent = "";
    const tw = $("#stall-create-timbre-wrap");
    if (isPerson) tw.classList.remove("hidden");
    else tw.classList.add("hidden");
  }

  async function openShop(id) {
    stopPoll();
    const page = await fetchJSON(`/api/shops/${encodeURIComponent(id)}/page`);
    const sh = page.shop || {};
    currentShop = sh;
    currentPlace = { id: sh.parent_id };
    $("#shop-name").textContent = sh.name || "";
    $("#shop-kind").textContent = sh.kind === "tienda" ? "Tienda" : "Puesto";
    $("#shop-info").textContent = sh.info || "";
    $("#shop-emoji").textContent = sh.kind === "tienda" ? "🛍️" : "🧺";
    $("#shop-assistant-label").textContent = (page.assistant && page.assistant.label) || ("Asistente de " + sh.name);
    const asst = $("#shop-assistant");
    asst.dataset.ask = (page.assistant && page.assistant.ask_path) || `/api/shops/${sh.id}/asistente/ask`;
    asst.dataset.faq = (page.assistant && page.assistant.faq_path) || `/api/shops/${sh.id}/asistente/faq`;

    const info = (page.sections || []).find((s) => s.id === "info");
    $("#shop-tab-info-body").textContent = (info && info.body) || sh.info || "";
    fillSectionItems("shop-tab-info-items", info && info.items);
    const avisos = (page.sections || []).find((s) => s.id === "avisos");
    fillSectionItems("shop-tab-avisos-items", avisos && avisos.items);
    const contacto = (page.sections || []).find((s) => s.id === "contacto");
    $("#shop-tab-contacto-body").textContent = (contacto && contacto.body) || sh.contact || "";
    fillSectionItems("shop-tab-contacto-items", contacto && contacto.items);

    const pucelaBox = $("#shop-pucela");
    const pucelaList = $("#shop-pucela-list");
    pucelaList.innerHTML = "";
    const ids = page.pucela_ids || sh.pucela_ids || [];
    if (ids.length) {
      for (const pid of ids) {
        const li = document.createElement("li");
        li.textContent = ".pucela " + pid.slice(0, 8) + "…";
        pucelaList.appendChild(li);
      }
      pucelaBox.classList.remove("hidden");
    } else {
      pucelaBox.classList.add("hidden");
    }

    hideAllViews();
    viewShop.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = sh.name || "Puesto";
    subtitle.textContent = "Página del puesto/tienda · igual rango";
    setNav("shop");
    document.querySelectorAll("[data-shoptab]").forEach((b) => b.classList.toggle("active", b.dataset.shoptab === "info"));
    ["info", "avisos", "contacto"].forEach((t) => {
      const el = $("#shop-tab-" + t);
      if (el) el.classList.toggle("hidden", t !== "info");
    });
    history.pushState({ view: "shop", id: sh.id, parent: sh.parent_id }, "", `/puesto/${sh.id}`);
  }

  async function openPersona(id) {
    stopPoll();
    const page = await fetchJSON(`/api/personas/${encodeURIComponent(id)}/page`);
    const person = page.person || {};
    currentPersona = person;
    $("#persona-name").textContent = person.display_name || "";
    $("#persona-bio").textContent = person.bio || "";
    $("#persona-assistant-label").textContent = (page.assistant && page.assistant.label) || ("Asistente de " + person.display_name);
    const asst = $("#persona-assistant");
    asst.dataset.ask = (page.assistant && page.assistant.ask_path) || `/api/personas/${person.id}/asistente/ask`;
    asst.dataset.faq = (page.assistant && page.assistant.faq_path) || `/api/personas/${person.id}/asistente/faq`;

    const img = $("#persona-image");
    const emoji = $("#persona-emoji");
    if (page.image_url) {
      img.src = page.image_url;
      img.alt = person.display_name || "";
      img.classList.remove("hidden");
      emoji.classList.add("hidden");
    } else {
      img.classList.add("hidden");
      emoji.classList.remove("hidden");
    }

    const timbreBox = $("#persona-timbre");
    if (page.timbre && page.timbre.opt_in) {
      $("#persona-timbre-hint").textContent = page.timbre.hint || "Opt-in de timbre activo.";
      timbreBox.classList.remove("hidden");
      const btn = $("#btn-persona-timbre");
      btn.onclick = () => {
        showCasa();
        if (page.timbre.peer_url) {
          const input = $("#timbre-peer-url");
          if (input) input.value = page.timbre.peer_url;
        }
        setStatus("Usa «Tocar timbre de otra casa» — la casa es privada.", "ok");
      };
    } else {
      timbreBox.classList.add("hidden");
    }

    hideAllViews();
    viewPersona.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = person.display_name || "Persona";
    subtitle.textContent = "Tarjeta pública · no es la casa";
    setNav("persona");
    history.pushState({ view: "persona", id: person.id }, "", `/persona/${person.id}`);
  }

  function showHome() {
    stopPoll();
    currentPlace = null;
    currentPeer = null;
    hideAllViews();
    viewHome.classList.remove("hidden");
    btnBack.classList.add("hidden");
    title.textContent = "Valladolid";
    subtitle.textContent = "Mapa ciudadano";
    setNav("lugares");
  }

  function showMessages() {
    stopPoll();
    currentPlace = null;
    currentPeer = null;
    hideAllViews();
    viewMessages.classList.remove("hidden");
    btnBack.classList.add("hidden");
    title.textContent = "Mensajes";
    subtitle.textContent = "Chat E2E en la LAN";
    setNav("mensajes");
    Promise.all([loadThreads(), loadContacts(), loadPresence()]).catch((e) =>
      setStatus("Error mensajes: " + e.message, "err")
    );
    history.pushState({ view: "mensajes" }, "", "/mensajes");
  }


  function showEnvios() {
    stopPoll();
    currentPlace = null;
    currentPeer = null;
    hideAllViews();
    if (viewEnvios) viewEnvios.classList.remove("hidden");
    btnBack.classList.add("hidden");
    title.textContent = "Envíos";
    subtitle.textContent = "Depósito excepcional · cita/cuota";
    setNav("envios");
    loadDeposito().catch((e) => setStatus("Error envíos: " + e.message, "err"));
    history.pushState({ view: "envios" }, "", "/envios");
  }

  function fmtMiB(bytes) {
    if (!bytes) return "0";
    return (bytes / (1024 * 1024)).toFixed(bytes >= 10 * 1024 * 1024 ? 0 : 1);
  }

  async function loadDeposito() {
    const lim = await fetchJSON("/api/deposito/limits");
    const label = $("#dep-max-label");
    if (label) label.textContent = fmtMiB(lim.max_bytes) + " MiB";
    const data = await fetchJSON("/api/deposito");
    const list = data.deposits || [];
    const box = $("#dep-list");
    const emptyEl = $("#dep-empty");
    if (!box) return;
    box.innerHTML = "";
    if (!list.length) {
      emptyEl.classList.remove("hidden");
      return;
    }
    emptyEl.classList.add("hidden");
    for (const d of list) {
      const row = document.createElement("button");
      row.type = "button";
      row.className = "thread-card";
      row.setAttribute("role", "listitem");
      const exp = d.expires ? new Date(d.expires * 1000).toLocaleString() : "—";
      row.innerHTML =
        "<strong>" + (d.name || shortId(d.id)) + "</strong>" +
        "<span class=\"muted small\">" + d.status + " · " + (d.size || 0) + " B / " + fmtMiB(d.max_bytes) + " MiB · caduca " + exp + "</span>" +
        "<span class=\"mono small\">" + shortId(d.id) + "</span>";
      row.addEventListener("click", () => {
        $("#dep-upload-id").value = d.id;
        $("#dep-redeem-id").value = d.id;
        setStatus("Cita " + shortId(d.id) + " · " + d.status, "ok");
      });
      box.appendChild(row);
    }
  }

  function showFiles() {
    stopPoll();
    currentPlace = null;
    currentPeer = null;
    hideAllViews();
    viewFiles.classList.remove("hidden");
    btnBack.classList.add("hidden");
    title.textContent = "Archivos";
    subtitle.textContent = "Ficheros ligeros E2E";
    setNav("archivos");
    Promise.all([loadFileContacts(), loadFilesList()]).catch((e) =>
      setStatus("Error archivos: " + e.message, "err")
    );
    history.pushState({ view: "archivos" }, "", "/archivos");
  }

  let lastRemoteTimbreId = null;
  let rechazosAlarmId = null;


  function showPucela() {
    stopPoll();
    currentPlace = null;
    currentPeer = null;
    hideAllViews();
    if (viewPucela) viewPucela.classList.remove("hidden");
    btnBack.classList.add("hidden");
    title.textContent = "Pucela";
    subtitle.textContent = "Documentos ciudadanos .pucela";
    setNav("pucela");
    loadPucelaList().catch((e) => setStatus("Error pucela: " + e.message, "err"));
    history.pushState({ view: "pucela" }, "", "/pucela");
  }

  async function loadPucelaList() {
    const data = await fetchJSON("/api/pucela?enrich=1");
    const list = data.documents || [];
    const box = $("#pucela-list");
    const emptyEl = $("#pucela-empty");
    box.innerHTML = "";
    if (!list.length) {
      emptyEl.classList.remove("hidden");
      return;
    }
    emptyEl.classList.add("hidden");
    for (const d of list) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "thread-card";
      btn.setAttribute("role", "listitem");
      const kinds = (d.kinds || []).join(", ") || "—";
      const when = d.created
        ? new Date(d.created * 1000).toLocaleString("es-ES", {
            day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit",
          })
        : "";
      btn.innerHTML =
        `<strong>${escapeHTML(d.title || "Sin título")}</strong>` +
        `<span class="preview">${escapeHTML(kinds)} · ${d.part_count || "?"} partes · ${formatBytes(d.size || 0)}</span>` +
        `<span class="preview muted">${escapeHTML(when)}</span>`;
      btn.addEventListener("click", () => openPucelaDoc(d.id));
      box.appendChild(btn);
    }
  }

  function formatBytes(n) {
    if (n < 1024) return n + " B";
    if (n < 1048576) return (n / 1024).toFixed(1) + " KiB";
    return (n / 1048576).toFixed(1) + " MiB";
  }

  async function openPucelaDoc(id) {
    const data = await fetchJSON("/api/pucela/" + encodeURIComponent(id) + "/open", {
      method: "POST",
      body: "{}",
    });
    const card = $("#pucela-open-card");
    const body = $("#pucela-open-body");
    $("#pucela-open-title").textContent = data.title || "Documento";
    body.innerHTML = "";
    if (data.channel || (data.version && data.version >= 6)) {
      const ch = document.createElement("p");
      ch.className = "muted small";
      ch.textContent = "Formato v" + (data.version || 6) + " · canal audio codificado verificado (no es un zip).";
      body.appendChild(ch);
    }
    for (const part of data.parts || []) {
      if (part.role === "canal" || part.name === "canal.wav") continue; // side-channel, no UI
      const wrap = document.createElement("div");
      wrap.className = "pucela-part";
      if (part.kind === "text") {
        const pre = document.createElement("pre");
        pre.className = "pucela-text";
        pre.textContent = part.text || "";
        wrap.appendChild(pre);
      } else if (part.kind === "image" && part.data_b64) {
        const img = document.createElement("img");
        img.alt = part.name || "imagen";
        img.className = "pucela-img";
        img.src = "data:" + (part.mime || "image/jpeg") + ";base64," + part.data_b64;
        wrap.appendChild(img);
        if (part.fitted) {
          const note = document.createElement("p");
          note.className = "muted small";
          note.textContent = "Imagen ajustada automáticamente a la red (máx. 1600px / 512 KiB).";
          wrap.appendChild(note);
        }
      } else if (part.kind === "sound" && part.data_b64) {
        const audio = document.createElement("audio");
        audio.controls = true;
        audio.className = "pucela-audio";
        audio.src = "data:" + (part.mime || "audio/mpeg") + ";base64," + part.data_b64;
        wrap.appendChild(audio);
      } else {
        wrap.textContent = part.kind + ": " + (part.name || "");
      }
      body.appendChild(wrap);
    }
    card.classList.remove("hidden");
    card.scrollIntoView({ behavior: "smooth", block: "nearest" });
    setStatus("Documento abierto (sesión local)", "ok");
  }


  function roleLabel(role) {
    if (role === "banner") return "Anuncio · banner estático";
    if (role === "fullpage-ad") return "Anuncio · hoja completa";
    return "";
  }

  function renderHoja() {
    if (!currentEdition) return;
    const hojas = currentEdition.hojas || [];
    const n = hojas.length;
    const i = Math.max(0, Math.min(hojaIndex, Math.max(0, n - 1)));
    hojaIndex = i;
    const h = hojas[i] || {};
    const counter = $("#hoja-counter");
    if (counter) counter.textContent = n ? `${i + 1} / ${n}` : "0 / 0";
    const roleEl = $("#hoja-role");
    const stage = $("#hoja-stage");
    const body = $("#hoja-body");
    const label = roleLabel(h.role);
    stage.classList.remove("role-banner", "role-fullpage-ad");
    if (h.role === "banner") stage.classList.add("role-banner");
    if (h.role === "fullpage-ad") stage.classList.add("role-fullpage-ad");
    if (label) {
      roleEl.textContent = label;
      roleEl.classList.remove("hidden");
    } else {
      roleEl.classList.add("hidden");
    }
    body.innerHTML = "";
    if (h.kind === "text") {
      const pre = document.createElement("div");
      pre.textContent = h.text || "";
      body.appendChild(pre);
    } else if (h.kind === "image" && h.data_b64) {
      const img = document.createElement("img");
      img.className = "hoja-img";
      img.alt = h.name || "imagen";
      img.src = "data:" + (h.mime || "image/jpeg") + ";base64," + h.data_b64;
      img.draggable = false;
      body.appendChild(img);
    } else if (h.kind === "sound" && h.data_b64) {
      const audio = document.createElement("audio");
      audio.controls = true;
      audio.src = "data:" + (h.mime || "audio/mpeg") + ";base64," + h.data_b64;
      body.appendChild(audio);
    } else {
      body.textContent = (h.kind || "?") + ": " + (h.name || "");
    }
    const prev = $("#btn-hoja-prev");
    const next = $("#btn-hoja-next");
    if (prev) prev.disabled = i <= 0;
    if (next) next.disabled = i >= n - 1;
  }

  function flipHoja(delta) {
    if (!currentEdition) return;
    const n = (currentEdition.hojas || []).length;
    const next = hojaIndex + delta;
    if (next < 0 || next >= n) return;
    hojaIndex = next;
    renderHoja();
  }

  async function openEdition(id) {
    stopPoll();
    const data = await fetchJSON("/api/prensa/" + encodeURIComponent(id) + "/open", {
      method: "POST",
      body: "{}",
    });
    currentEdition = data;
    hojaIndex = 0;
    hideAllViews();
    if (viewPrensa) viewPrensa.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = data.title || "Edición";
    subtitle.textContent = "Hojas · lectura gratuita";
    setNav("prensa");
    const note = $("#prensa-ads-note");
    if (note) note.textContent = data.ads_note || "Anuncios solo estáticos. Sin vídeo ni trackers.";
    renderHoja();
    history.pushState({ view: "prensa", id: data.id }, "", "/prensa/" + encodeURIComponent(data.id));
    setStatus("Edición abierta en local (cerrojo .pucela)", "ok");
  }

  /* --- v4.8–5.0 Mi casa bolsón: estancias + puerta + huerto/cocina/despensa/ventanas --- */
  const CASA_PUERTA_KEY = "rcv_casa_puerta_v48";
  const CASA_ESTANCIA_KEY = "rcv_casa_estancia_v48";
  const CASA_SALON_ESTADO_KEY = "rcv_casa_salon_estado_v48";
  const CASA_SALON_NOTAS_KEY = "rcv_casa_salon_notas_v48";
  const CASA_CHIMENEA_KEY = "rcv_casa_chimenea_v49";
  const CASA_HUERTO_KEY = "rcv_casa_huerto_v49";
  const CASA_DESPENSA_KEY = "rcv_casa_despensa_v50";
  const CASA_COMIDA_KEY = "rcv_casa_comida_v50";
  const CASA_ESTANCIAS = ["recibidor", "salon", "huerto", "cocina", "despensa", "mirador"];
  const HUERTO_CROPS = [
    { id: "tomate", name: "Tomate cherry", empty: "🪴", stages: ["🌱", "🌿", "🍅", "🍅"], harvest: "Tomates maduros: olor a verano en el patio.", jar: "🍅" },
    { id: "lechuga", name: "Lechuga", empty: "🪴", stages: ["🌱", "🥬", "🥬", "🥗"], harvest: "Lechuga crujiente para la ensalada del mediodía.", jar: "🥬" },
    { id: "menta", name: "Hierbabuena", empty: "🪴", stages: ["🌱", "🌿", "🌿", "🍃"], harvest: "Hierbabuena fresca: perfecta para una infusión.", jar: "🍃" },
    { id: "calabaza", name: "Calabaza", empty: "🪴", stages: ["🌱", "🍃", "🎃", "🎃"], harvest: "Calabaza dorada: la despensa sonríe.", jar: "🎃" },
  ];
  const HUERTO_STAGE_LABELS = ["Vacío", "Brote", "Creciendo", "Casi listo", "Listo para cosechar"];
  // Recetas locales de la madriguera (qué: sabor; por qué: consumen despensa, no simulan nutrición).
  const COCINA_RECETAS = [
    {
      id: "sopa_raiz",
      name: "Sopa de raíz",
      emoji: "🥣",
      needs: { calabaza: 1, lechuga: 1 },
      desc: "Calabaza y hojas al fuego lento: vapor que huele a tarde de lluvia.",
      flavor: "La sopa de raíz reconforta la madriguera. Un tazón humeante en el salón.",
      meal: "Olor a sopa de raíz en el salón · tazón humeante.",
      durationMin: 45,
    },
    {
      id: "te_hierbas",
      name: "Té de hierbas",
      emoji: "🍵",
      needs: { menta: 1 },
      desc: "Hierbabuena en agua caliente: verde y limpio.",
      flavor: "El té de hierbas despierta la nariz. Una taza junto a la ventana redonda.",
      meal: "Té de hierbas humeante · la ventana huele a menta.",
      durationMin: 30,
    },
    {
      id: "pan_madriguera",
      name: "Pan de madriguera",
      emoji: "🍞",
      needs: { tomate: 1, lechuga: 1 },
      desc: "Panecillo de horno con tomate y un toque de hoja: merienda de puerta redonda.",
      flavor: "Pan de madriguera recién hecho. Migas cálidas en el mantel del salón.",
      meal: "Pan de madriguera en la mesa · migas cálidas.",
      durationMin: 40,
    },
  ];
  let huertoTimer = null;
  let timbreAlarmId = null;
  let rechazoAlarmId = null;

  function getCasaPuertaCerrada() {
    try {
      const v = localStorage.getItem(CASA_PUERTA_KEY);
      if (v === "abierta") return false;
      return true; // por defecto cerrada (privacidad)
    } catch (_) {
      return true;
    }
  }

  function setCasaPuertaCerrada(cerrada) {
    try {
      localStorage.setItem(CASA_PUERTA_KEY, cerrada ? "cerrada" : "abierta");
    } catch (_) {}
    applyCasaPuertaUI(cerrada);
  }

  function applyCasaPuertaUI(cerrada) {
    if (!viewCasa) return;
    viewCasa.classList.toggle("puerta-cerrada", !!cerrada);
    viewCasa.classList.toggle("puerta-abierta", !cerrada);
    const cap = $("#casa-puerta-caption");
    const btn = $("#btn-casa-puerta");
    const tog = $("#btn-casa-puerta-toggle");
    if (cap) {
      cap.textContent = cerrada
        ? "Puerta cerrada · bolsón"
        : "Puerta abierta · madriguera";
    }
    if (btn) btn.setAttribute("aria-pressed", cerrada ? "true" : "false");
    if (tog) tog.textContent = cerrada ? "Abrir puerta" : "Cerrar puerta";
  }

  function toggleCasaPuerta() {
    setCasaPuertaCerrada(!getCasaPuertaCerrada());
    setStatus(
      getCasaPuertaCerrada()
        ? "Puerta cerrada — privacidad acentuada; el timbre sigue activo"
        : "Puerta abierta — bienvenida visual (el timbre no cambia)",
      "ok"
    );
  }

  function getCasaEstancia() {
    try {
      const v = localStorage.getItem(CASA_ESTANCIA_KEY);
      if (CASA_ESTANCIAS.indexOf(v) >= 0) return v;
    } catch (_) {}
    return "recibidor";
  }

  function setCasaEstancia(id) {
    if (CASA_ESTANCIAS.indexOf(id) < 0) id = "recibidor";
    try {
      localStorage.setItem(CASA_ESTANCIA_KEY, id);
    } catch (_) {}
    applyCasaEstanciaUI(id);
  }

  function applyCasaEstanciaUI(id) {
    if (!viewCasa) return;
    viewCasa.setAttribute("data-estancia", id);
    document.querySelectorAll(".casa-estancia-tab").forEach((tab) => {
      const on = tab.dataset.estancia === id;
      tab.classList.toggle("active", on);
      tab.setAttribute("aria-selected", on ? "true" : "false");
    });
    document.querySelectorAll(".casa-estancia").forEach((panel) => {
      const on = panel.dataset.estancia === id;
      panel.classList.toggle("hidden", !on);
      if (on) panel.removeAttribute("hidden");
      else panel.setAttribute("hidden", "");
    });
  }

  function loadCasaSalonPrefs() {
    const estado = $("#casa-salon-estado");
    const notas = $("#casa-salon-notas");
    try {
      if (estado) estado.value = localStorage.getItem(CASA_SALON_ESTADO_KEY) || "";
      if (notas) notas.value = localStorage.getItem(CASA_SALON_NOTAS_KEY) || "";
    } catch (_) {}
  }

  function saveCasaSalonPrefs() {
    const estado = ($("#casa-salon-estado") && $("#casa-salon-estado").value.trim()) || "";
    const notas = ($("#casa-salon-notas") && $("#casa-salon-notas").value) || "";
    const fb = $("#casa-salon-feedback");
    try {
      localStorage.setItem(CASA_SALON_ESTADO_KEY, estado.slice(0, 80));
      localStorage.setItem(CASA_SALON_NOTAS_KEY, notas.slice(0, 2000));
      if (fb) fb.textContent = "Guardado en este dispositivo.";
      setStatus("Salón actualizado", "ok");
    } catch (e) {
      if (fb) fb.textContent = "No se pudo guardar: " + (e && e.message ? e.message : "error");
    }
  }

  function getChimeneaOn() {
    try { return localStorage.getItem(CASA_CHIMENEA_KEY) === "on"; } catch (_) { return false; }
  }
  function setChimeneaOn(on) {
    try { localStorage.setItem(CASA_CHIMENEA_KEY, on ? "on" : "off"); } catch (_) {}
    applyChimeneaUI(on);
  }
  function applyChimeneaUI(on) {
    const panel = $("#casa-chimenea-panel");
    const status = $("#casa-chimenea-status");
    const btn = $("#btn-casa-chimenea");
    if (panel) panel.classList.toggle("chimenea-on", !!on);
    // v5.8: humo también en fachada del bolsón
    if (viewCasa) viewCasa.classList.toggle("chimenea-on", !!on);
    if (status) {
      status.textContent = on
        ? "La lumbre crepita · el salón se calienta con olor a leña."
        : "Chimenea apagada · el salón espera la lumbre.";
    }
    if (btn) {
      btn.textContent = on ? "Apagar chimenea" : "Encender chimenea";
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    }
  }
  function toggleChimenea() {
    const next = !getChimeneaOn();
    setChimeneaOn(next);
    setStatus(next ? "Chimenea encendida" : "Chimenea apagada", "ok");
  }

  function defaultHuertoState() {
    return {
      day: 1,
      lastTick: Date.now(),
      plots: HUERTO_CROPS.map((c) => ({ id: c.id, stage: 0 })), // 0 vacío, 1–4 crecimiento
    };
  }
  function loadHuertoState() {
    try {
      const raw = localStorage.getItem(CASA_HUERTO_KEY);
      if (!raw) return defaultHuertoState();
      const st = JSON.parse(raw);
      if (!st || !Array.isArray(st.plots) || st.plots.length !== HUERTO_CROPS.length) {
        return defaultHuertoState();
      }
      return st;
    } catch (_) {
      return defaultHuertoState();
    }
  }
  function saveHuertoState(st) {
    try { localStorage.setItem(CASA_HUERTO_KEY, JSON.stringify(st)); } catch (_) {}
  }
  function cropMeta(id) {
    return HUERTO_CROPS.find((c) => c.id === id) || HUERTO_CROPS[0];
  }
  function huertoTick(force) {
    const st = loadHuertoState();
    const now = Date.now();
    // Día / tick: ~45s en vista, o forzado por botón; también avanza si pasó ≥1h offline
    const elapsed = now - (st.lastTick || now);
    const due = force || elapsed >= 45000 || elapsed >= 3600000;
    if (!due) {
      renderHuerto();
      return;
    }
    let grew = false;
    for (const plot of st.plots) {
      if (plot.stage >= 1 && plot.stage < 4) {
        plot.stage += 1;
        grew = true;
      }
    }
    st.lastTick = now;
    if (force || grew) st.day = (st.day || 1) + 1;
    saveHuertoState(st);
    renderHuerto();
    const fb = $("#casa-huerto-flavor");
    if (fb) {
      if (grew) fb.textContent = "El sol de la madriguera ha hecho su trabajo…";
      else if (force) fb.textContent = "Ha pasado un rato en el huerto. La tierra espera.";
    }
  }
  function plantHuerto(plotId) {
    const st = loadHuertoState();
    const plot = st.plots.find((p) => p.id === plotId);
    if (!plot || plot.stage !== 0) return;
    plot.stage = 1;
    saveHuertoState(st);
    const meta = cropMeta(plotId);
    const fb = $("#casa-huerto-flavor");
    if (fb) fb.textContent = "Has plantado " + meta.name.toLowerCase() + ". Un brote asoma en la tierra.";
    renderHuerto();
    setStatus("Plantado: " + meta.name, "ok");
  }
  function harvestHuerto(plotId) {
    const st = loadHuertoState();
    const plot = st.plots.find((p) => p.id === plotId);
    if (!plot || plot.stage < 4) return;
    const meta = cropMeta(plotId);
    plot.stage = 0;
    saveHuertoState(st);
    // v5.0: la cosecha alimenta la despensa real (contadores).
    addDespensaItem(plotId, 1);
    const fb = $("#casa-huerto-flavor");
    if (fb) fb.textContent = meta.harvest + " → a la despensa.";
    renderHuerto();
    renderDespensa();
    renderCocina();
    setStatus("Cosecha: " + meta.name + " (despensa +1)", "ok");
  }
  function renderHuerto() {
    const box = $("#casa-huerto-plots");
    const dayEl = $("#casa-huerto-day");
    if (!box) return;
    const st = loadHuertoState();
    if (dayEl) dayEl.textContent = "Día del huerto: " + (st.day || 1);
    box.innerHTML = "";
    for (const plot of st.plots) {
      const meta = cropMeta(plot.id);
      const stage = plot.stage | 0;
      const emoji = stage === 0 ? meta.empty : meta.stages[Math.min(stage, 4) - 1];
      const label = HUERTO_STAGE_LABELS[Math.min(stage, 4)] || "—";
      const art = document.createElement("article");
      art.className = "casa-huerto-plot";
      art.setAttribute("role", "listitem");
      art.dataset.plot = plot.id;
      let action = "";
      if (stage === 0) {
        action = `<button type="button" class="btn-primary btn-huerto-plant" data-id="${escapeHTML(plot.id)}">Plantar</button>`;
      } else if (stage >= 4) {
        action = `<button type="button" class="btn-primary btn-huerto-harvest" data-id="${escapeHTML(plot.id)}">Cosechar</button>`;
      } else {
        action = `<span class="muted small">Creciendo…</span>`;
      }
      art.innerHTML =
        `<span class="plot-emoji" aria-hidden="true">${emoji}</span>` +
        `<div class="plot-name">${escapeHTML(meta.name)}</div>` +
        `<div class="plot-stage">${escapeHTML(label)}</div>` +
        action;
      box.appendChild(art);
    }
    box.querySelectorAll(".btn-huerto-plant").forEach((btn) => {
      btn.addEventListener("click", () => plantHuerto(btn.dataset.id));
    });
    box.querySelectorAll(".btn-huerto-harvest").forEach((btn) => {
      btn.addEventListener("click", () => harvestHuerto(btn.dataset.id));
    });
  }
  function startHuertoTimer() {
    stopHuertoTimer();
    huertoTimer = setInterval(() => {
      if (viewCasa && !viewCasa.classList.contains("hidden") && getCasaEstancia() === "huerto") {
        huertoTick(false);
      }
    }, 15000);
  }
  function stopHuertoTimer() {
    if (huertoTimer) {
      clearInterval(huertoTimer);
      huertoTimer = null;
    }
  }

  /* --- v5.0 despensa real + cocina --- */
  function defaultDespensa() {
    const stock = {};
    HUERTO_CROPS.forEach((c) => { stock[c.id] = 0; });
    return { stock: stock };
  }
  function loadDespensa() {
    try {
      const raw = localStorage.getItem(CASA_DESPENSA_KEY);
      if (!raw) return defaultDespensa();
      const st = JSON.parse(raw);
      if (!st || typeof st.stock !== "object") return defaultDespensa();
      const base = defaultDespensa();
      HUERTO_CROPS.forEach((c) => {
        const n = parseInt(st.stock[c.id], 10);
        base.stock[c.id] = Number.isFinite(n) && n > 0 ? n : 0;
      });
      return base;
    } catch (_) {
      return defaultDespensa();
    }
  }
  function saveDespensa(st) {
    try { localStorage.setItem(CASA_DESPENSA_KEY, JSON.stringify(st)); } catch (_) {}
  }
  function addDespensaItem(cropId, n) {
    const st = loadDespensa();
    if (!(cropId in st.stock)) st.stock[cropId] = 0;
    st.stock[cropId] = Math.max(0, (st.stock[cropId] | 0) + (n | 0));
    saveDespensa(st);
    return st;
  }
  function canAffordRecipe(recipe, stock) {
    for (const k of Object.keys(recipe.needs)) {
      if ((stock[k] | 0) < recipe.needs[k]) return false;
    }
    return true;
  }
  function formatNeeds(needs) {
    return Object.keys(needs).map((id) => {
      const m = cropMeta(id);
      return needs[id] + "× " + m.name;
    }).join(" · ");
  }
  function renderDespensa() {
    const box = $("#casa-despensa-stock");
    const emptyEl = $("#casa-despensa-empty");
    if (!box) return;
    const st = loadDespensa();
    box.innerHTML = "";
    let total = 0;
    for (const crop of HUERTO_CROPS) {
      const n = st.stock[crop.id] | 0;
      total += n;
      const art = document.createElement("article");
      art.className = "casa-despensa-item" + (n === 0 ? " empty-jar" : "");
      art.setAttribute("role", "listitem");
      art.innerHTML =
        `<span class="jar-emoji" aria-hidden="true">${crop.jar || "🫙"}</span>` +
        `<div class="jar-name">${escapeHTML(crop.name)}</div>` +
        `<div class="jar-count">${n}</div>`;
      box.appendChild(art);
    }
    if (emptyEl) emptyEl.classList.toggle("hidden", total > 0);
  }
  function loadComidaActiva() {
    try {
      const raw = localStorage.getItem(CASA_COMIDA_KEY);
      if (!raw) return null;
      const m = JSON.parse(raw);
      if (!m || !m.until || !m.label) return null;
      if (Date.now() > m.until) {
        localStorage.removeItem(CASA_COMIDA_KEY);
        return null;
      }
      return m;
    } catch (_) {
      return null;
    }
  }
  function setComidaActiva(recipe) {
    const until = Date.now() + (recipe.durationMin || 30) * 60 * 1000;
    const m = { id: recipe.id, label: recipe.meal, until: until, name: recipe.name };
    try { localStorage.setItem(CASA_COMIDA_KEY, JSON.stringify(m)); } catch (_) {}
    renderComidaStatus();
  }
  function renderComidaStatus() {
    const el = $("#casa-comida-status");
    if (!el) return;
    const m = loadComidaActiva();
    if (!m) {
      el.classList.add("hidden");
      el.textContent = "";
      return;
    }
    const mins = Math.max(1, Math.ceil((m.until - Date.now()) / 60000));
    el.textContent = m.label + " (queda ~" + mins + " min)";
    el.classList.remove("hidden");
  }
  function renderCocina() {
    const box = $("#casa-cocina-recetas");
    if (!box) return;
    const st = loadDespensa();
    box.innerHTML = "";
    for (const r of COCINA_RECETAS) {
      const ok = canAffordRecipe(r, st.stock);
      const art = document.createElement("article");
      art.className = "casa-receta-card";
      art.setAttribute("role", "listitem");
      art.innerHTML =
        `<p class="receta-title">${r.emoji} ${escapeHTML(r.name)}</p>` +
        `<p class="receta-needs">Ingredientes: ${escapeHTML(formatNeeds(r.needs))}</p>` +
        `<p class="receta-desc">${escapeHTML(r.desc)}</p>` +
        `<button type="button" class="btn-primary btn-cocinar" data-id="${escapeHTML(r.id)}" ${ok ? "" : "disabled"}>Cocinar</button>`;
      box.appendChild(art);
    }
    box.querySelectorAll(".btn-cocinar").forEach((btn) => {
      btn.addEventListener("click", () => cocinarReceta(btn.dataset.id));
    });
  }
  function cocinarReceta(recipeId) {
    const recipe = COCINA_RECETAS.find((r) => r.id === recipeId);
    if (!recipe) return;
    const st = loadDespensa();
    if (!canAffordRecipe(recipe, st.stock)) {
      setStatus("Faltan ingredientes en la despensa", "err");
      return;
    }
    for (const k of Object.keys(recipe.needs)) {
      st.stock[k] = Math.max(0, (st.stock[k] | 0) - recipe.needs[k]);
    }
    saveDespensa(st);
    setComidaActiva(recipe);
    const fb = $("#casa-cocina-flavor");
    if (fb) fb.textContent = recipe.flavor;
    renderDespensa();
    renderCocina();
    renderComidaStatus();
    setStatus("Listo: " + recipe.name, "ok");
  }

  function initCasaBolsonPrefs() {
    applyCasaPuertaUI(getCasaPuertaCerrada());
    applyCasaEstanciaUI(getCasaEstancia());
    loadCasaSalonPrefs();
    applyChimeneaUI(getChimeneaOn());
    renderHuerto();
    renderDespensa();
    renderCocina();
    renderComidaStatus();
    // Asegura clase TOD en la casa aunque Calles no esté visible.
    if (todPhase) {
      viewCasa.classList.remove("tod-dia", "tod-atardecer", "tod-noche");
      viewCasa.classList.add("tod-" + todPhase);
    }
    startHuertoTimer();
  }

  function showCasa() {
    stopPoll();
    currentPlace = null;
    currentPeer = null;
    hideAllViews();
    viewCasa.classList.remove("hidden");
    btnBack.classList.add("hidden");
    title.textContent = "Mi casa";
    subtitle.textContent = "Madriguera · cocina, despensa y ventanas";
    setNav("casa");
    initCasaBolsonPrefs();
    loadCasa().catch((e) => setStatus("Error casa: " + e.message, "err"));
    history.pushState({ view: "casa" }, "", "/casa");
  }

  async function loadCasa() {
    const st = await fetchJSON("/api/casa");
    const addrEl = $("#casa-address");
    const metaEl = $("#casa-address-meta");
    addrEl.textContent = st.current_address || "—";
    addrEl.classList.toggle("expired", !!st.is_expired);
    const exp = st.expires_at
      ? new Date(st.expires_at * 1000).toLocaleString("es-ES", {
          day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit",
        })
      : "";
    metaEl.textContent = st.is_expired
      ? "Dirección caducada — rota o acepta un timbre para renovar."
      : "Válida hasta " + exp + " · pendientes: " + (st.pending_timbre || 0);
    await Promise.all([loadTimbrePending(), loadAlarms(), loadAvisos(), loadVisitas(), loadPresence()]);
  }

  async function loadVisitas() {
    const box = $("#visitas-list");
    const emptyEl = $("#visitas-empty");
    if (!box) return;
    try {
      const data = await fetchJSON("/api/casa/visitas");
      const list = data.visitas || [];
      box.innerHTML = "";
      if (!list.length) {
        if (emptyEl) emptyEl.classList.remove("hidden");
        return;
      }
      if (emptyEl) emptyEl.classList.add("hidden");
      for (const v of list) {
        const row = document.createElement("article");
        row.className = "visita-row";
        row.setAttribute("role", "listitem");
        const when = v.created
          ? new Date(v.created * 1000).toLocaleString("es-ES", {
              day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit",
            })
          : "";
        row.innerHTML =
          `<strong>${escapeHTML(v.name || shortId(v.from_user_id || ""))}</strong>` +
          `<span class="visita-note">«${escapeHTML(v.note || "")}»</span>` +
          `<span class="visita-when">${escapeHTML(when)}</span>`;
        box.appendChild(row);
      }
    } catch (e) {
      box.innerHTML = "";
      if (emptyEl) {
        emptyEl.classList.remove("hidden");
        emptyEl.textContent = "No se pudo cargar el libro de visitas.";
      }
    }
  }

  async function loadTimbrePending() {
    const data = await fetchJSON("/api/casa/timbre?status=pendiente");
    const list = data.requests || [];
    const box = $("#timbre-pending");
    const emptyEl = $("#timbre-empty");
    box.innerHTML = "";
    if (!list.length) {
      emptyEl.classList.remove("hidden");
      return;
    }
    emptyEl.classList.add("hidden");
    for (const r of list) {
      const row = document.createElement("article");
      row.className = "timbre-card";
      row.setAttribute("role", "listitem");
      const when = r.created
        ? new Date(r.created * 1000).toLocaleString("es-ES", {
            day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit",
          })
        : "";
      row.innerHTML =
        `<div class="timbre-card-main">` +
        `<span class="timbre-badge">🔔 En la puerta</span>` +
        `<strong>${escapeHTML(shortId(r.from_user_id))}</strong>` +
        `<span class="preview">${escapeHTML(r.message || "(sin mensaje)")}</span>` +
        `<span class="cat">${escapeHTML(when)} · ${escapeHTML(r.status_label || r.status)}</span>` +
        `</div>` +
        `<div class="timbre-actions">` +
        `<button type="button" class="btn-primary btn-aceptar" data-id="${escapeHTML(r.id)}" aria-label="Aceptar timbre y revelar dirección">✓ Abrir · Aceptar</button>` +
        `<button type="button" class="btn-secondary btn-rechazar" data-id="${escapeHTML(r.id)}" aria-label="Rechazar timbre">✕ No abrir · Rechazar</button>` +
        `</div>`;
      box.appendChild(row);
    }
    box.querySelectorAll(".btn-aceptar").forEach((btn) => {
      btn.addEventListener("click", () => resolveTimbre(btn.dataset.id, "aceptar"));
    });
    box.querySelectorAll(".btn-rechazar").forEach((btn) => {
      btn.addEventListener("click", () => resolveTimbre(btn.dataset.id, "rechazar"));
    });
  }

  async function resolveTimbre(id, action) {
    try {
      await fetchJSON("/api/casa/timbre/" + encodeURIComponent(id) + "/" + action, {
        method: "POST",
        body: "{}",
      });
      await loadCasa();
      setStatus(action === "aceptar" ? "Timbre aceptado" : "Timbre rechazado", "ok");
    } catch (e) {
      setStatus("Timbre: " + e.message, "err");
    }
  }

  async function loadAlarms() {
    const data = await fetchJSON("/api/casa/alarmas");
    const list = data.alarms || [];
    const box = $("#alarms-list");
    const emptyEl = $("#alarms-empty");
    if (!box) return;
    box.innerHTML = "";
    rechazosAlarmId = null;
    timbreAlarmId = null;
    rechazoAlarmId = null;
    let rechazosArmed = false;
    let timbreArmed = false;
    let rechazoArmed = false;
    let shown = 0;
    for (const a of list) {
      if (a.kind === "rechazos") {
        rechazosAlarmId = a.id;
        rechazosArmed = !!a.armed;
      } else if (a.kind === "timbre") {
        timbreAlarmId = a.id;
        timbreArmed = !!a.armed;
      } else if (a.kind === "rechazo") {
        rechazoAlarmId = a.id;
        rechazoArmed = !!a.armed;
      }
      const row = document.createElement("div");
      row.className = "alarm-row";
      row.setAttribute("role", "listitem");
      row.innerHTML =
        `<span>${escapeHTML(a.kind_label || a.kind)} · ${escapeHTML(a.armed_label)}` +
        (a.contact_user_id ? " · " + escapeHTML(shortId(a.contact_user_id)) : "") +
        `</span>` +
        `<button type="button" class="btn-secondary btn-sm btn-toggle-alarm" data-id="${escapeHTML(a.id)}" data-armed="${a.armed ? "1" : "0"}">` +
        (a.armed ? "Desarmar" : "Armar") +
        `</button>`;
      box.appendChild(row);
      shown++;
    }
    if (emptyEl) emptyEl.classList.toggle("hidden", shown > 0);
    const setTog = (sel, armed) => {
      const el = $(sel);
      if (el) {
        el.checked = !!armed;
        el.dataset.bound = "1";
      }
    };
    setTog("#alarm-rechazos-toggle", rechazosArmed);
    setTog("#alarm-timbre-toggle", timbreArmed);
    setTog("#alarm-rechazo-toggle", rechazoArmed);
    box.querySelectorAll(".btn-toggle-alarm").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const armed = btn.dataset.armed !== "1";
        await fetchJSON("/api/casa/alarmas/" + encodeURIComponent(btn.dataset.id), {
          method: "PATCH",
          body: JSON.stringify({ armed }),
        });
        await loadAlarms();
      });
    });
  }

  async function ensureAlarmKind(kind, armed, idRef) {
    if (idRef) {
      await fetchJSON("/api/casa/alarmas/" + encodeURIComponent(idRef), {
        method: "PATCH",
        body: JSON.stringify({ armed }),
      });
    } else if (armed) {
      await fetchJSON("/api/casa/alarmas", {
        method: "POST",
        body: JSON.stringify({ kind, armed: true, note: "UI v4.9" }),
      });
    }
    await loadAlarms();
  }

  async function loadAvisos() {
    const data = await fetchJSON("/api/casa/avisos");
    const list = data.avisos || [];
    const box = $("#avisos-list");
    const emptyEl = $("#avisos-empty");
    box.innerHTML = "";
    if (!list.length) {
      emptyEl.classList.remove("hidden");
      return;
    }
    emptyEl.classList.add("hidden");
    for (const v of list) {
      const row = document.createElement("div");
      row.className = "aviso-row" + (v.seen ? " seen" : "");
      row.textContent = v.message || v.kind;
      box.appendChild(row);
    }
  }

  function formatBytes(n) {
    n = Number(n) || 0;
    if (n < 1024) return n + " B";
    if (n < 1024 * 1024) return (n / 1024).toFixed(1) + " KB";
    return (n / (1024 * 1024)).toFixed(2) + " MB";
  }

  function statusLabel(st) {
    return ({ pending: "pendiente", delivered: "entregado", received: "recibido" })[st] || st;
  }

  async function loadFileContacts() {
    const data = await fetchJSON("/api/contacts");
    const sel = $("#file-contact");
    const cur = sel.value;
    sel.innerHTML = '<option value="">— Elige un contacto —</option>';
    for (const c of data.contacts || []) {
      const opt = document.createElement("option");
      opt.value = c.user_id;
      opt.textContent = (c.display_name || shortId(c.user_id)) + " · " + shortId(c.user_id);
      sel.appendChild(opt);
    }
    if (cur) sel.value = cur;
  }

  async function loadFilesList() {
    const data = await fetchJSON("/api/files");
    const list = data.files || [];
    const box = $("#files-list");
    const emptyEl = $("#files-empty");
    box.innerHTML = "";
    if (!list.length) {
      emptyEl.classList.remove("hidden");
      return;
    }
    emptyEl.classList.add("hidden");
    for (const f of list) {
      const row = document.createElement("article");
      row.className = "file-card";
      row.setAttribute("role", "listitem");
      const when = f.created
        ? new Date(f.created * 1000).toLocaleString("es-ES", {
            day: "2-digit",
            month: "short",
            hour: "2-digit",
            minute: "2-digit",
          })
        : "";
      const dirLabel = f.direction === "out" ? "Enviado" : "Recibido";
      let actions = "";
      if (f.direction === "in") {
        actions =
          `<button type="button" class="btn-secondary btn-dl" data-id="${escapeHTML(f.id)}" data-name="${escapeHTML(f.name)}">Descargar</button>`;
      }
      row.innerHTML =
        `<div class="file-card-main">` +
        `<strong>${escapeHTML(f.name)}</strong>` +
        `<span class="preview">${escapeHTML(dirLabel)} · ${escapeHTML(formatBytes(f.size))} · ${escapeHTML(statusLabel(f.status))}</span>` +
        `<span class="cat">${escapeHTML(when)}</span>` +
        `</div>${actions}`;
      box.appendChild(row);
    }
    box.querySelectorAll(".btn-dl").forEach((btn) => {
      btn.addEventListener("click", () => downloadFile(btn.dataset.id, btn.dataset.name));
    });
  }

  async function downloadFile(id, name) {
    try {
      const res = await fetch("/api/files/" + encodeURIComponent(id) + "/download");
      if (!res.ok) {
        let detail = "HTTP " + res.status;
        try {
          const j = await res.json();
          if (j.error) detail = j.error;
        } catch (_) {}
        throw new Error(detail);
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = name || "fichero.bin";
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      setStatus("Descarga lista: " + (name || id), "ok");
    } catch (e) {
      setStatus("No se pudo descargar: " + e.message, "err");
    }
  }

  async function loadThreads() {
    const data = await fetchJSON("/api/chat/threads");
    const threads = data.threads || [];
    threadsList.innerHTML = "";
    if (!threads.length) {
      threadsEmpty.classList.remove("hidden");
    } else {
      threadsEmpty.classList.add("hidden");
      for (const th of threads) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "thread-card";
        btn.setAttribute("role", "listitem");
        const name = th.display_name || shortId(th.peer_id);
        const preview = (th.last && th.last.body) || "";
        btn.innerHTML =
          `<strong>${escapeHTML(name)}${reachBadge(th.reach_quality, th.reach_label)}</strong>` +
          `<span class="preview">${escapeHTML(preview)}</span>` +
          `<span class="cat">${th.count || 0} mensajes</span>`;
        btn.addEventListener("click", () => openThread(th.peer_id, name));
        threadsList.appendChild(btn);
      }
    }
  }

  async function openThread(peerId, displayName) {
    currentPeer = peerId;
    currentPlace = null;
    hideAllViews();
    viewThread.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = displayName || shortId(peerId);
    subtitle.textContent = "Conversación cifrada";
    setNav("thread");
    await refreshThread();
    startPoll();
    history.pushState({ view: "thread", peer: peerId, name: displayName }, "", `/mensajes/${peerId.slice(0, 16)}`);
  }

  async function refreshThread() {
    if (!currentPeer) return;
    const data = await fetchJSON(`/api/chat/inbox?peer=${encodeURIComponent(currentPeer)}`);
    const msgs = data.messages || [];
    threadMessages.innerHTML = "";
    for (const m of msgs) {
      const div = document.createElement("div");
      const mine = m.direction === "out" || m.from === me.user_id;
      div.className = "bubble " + (mine ? "out" : "in");
      const when = m.ts ? new Date(m.ts * 1000).toLocaleString("es-ES", { hour: "2-digit", minute: "2-digit", day: "2-digit", month: "short" }) : "";
      const deliv = mine ? (m.delivered ? " · entregado" : " · pendiente") : "";
      div.innerHTML = `${escapeHTML(m.body)}<span class="meta">${escapeHTML(when + deliv)}</span>`;
      threadMessages.appendChild(div);
    }
    threadMessages.scrollTop = threadMessages.scrollHeight;
  }

  function startPoll() {
    stopPoll();
    pollTimer = setInterval(() => {
      refreshThread().catch(() => {});
    }, 3000);
  }
  function stopPoll() {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  }


  function kindLabel(k) {
    return ({ aviso: "Aviso", prensa: "Prensa", directorio: "Directorio" })[k] || k;
  }

  function fmtTime(ts) {
    if (!ts) return "—";
    try { return new Date(ts * 1000).toLocaleString("es-ES"); } catch (_) { return String(ts); }
  }

  async function loadFederacion() {
    const data = await fetchJSON("/api/federacion");
    const peersBox = $("#fed-peers-list");
    const peersEmpty = $("#fed-peers-empty");
    peersBox.innerHTML = "";
    const peers = data.peers || [];
    peersEmpty.classList.toggle("hidden", peers.length > 0);
    for (const p of peers) {
      const div = document.createElement("div");
      div.className = "file-row";
      div.setAttribute("role", "listitem");
      const ok = p.last_ok ? "✓" : (p.last_sync ? "✗" : "·");
      div.innerHTML = `<div class="file-meta"><strong>${escapeHTML(p.name || shortId(p.node_id) || "peer")}</strong>
        <span class="muted small">${escapeHTML(p.url)}</span>
        <span class="muted small">${ok} sync ${fmtTime(p.last_sync)}${p.last_error ? " · " + escapeHTML(p.last_error) : ""}</span></div>
        <button type="button" class="btn-secondary btn-fed-rm" data-url="${escapeHTML(p.url)}">Quitar</button>`;
      peersBox.appendChild(div);
    }
    peersBox.querySelectorAll(".btn-fed-rm").forEach((btn) => {
      btn.addEventListener("click", async () => {
        try {
          await fetchJSON("/api/federacion/peers", { method: "DELETE", body: JSON.stringify({ peer_url: btn.dataset.url }) });
          await loadFederacion();
          setStatus("Peer quitado", "ok");
        } catch (e) { setStatus(e.message, "err"); }
      });
    });

    const inbox = (data.inbox || []).filter((it) => it.kind === "aviso" || it.kind === "prensa");
    const inboxBox = $("#fed-inbox-list");
    const inboxEmpty = $("#fed-inbox-empty");
    inboxBox.innerHTML = "";
    inboxEmpty.classList.toggle("hidden", inbox.length > 0);
    for (const it of inbox.slice(0, 40)) {
      const div = document.createElement("div");
      div.className = "file-row";
      div.setAttribute("role", "listitem");
      div.innerHTML = `<div class="file-meta"><strong>${escapeHTML(kindLabel(it.kind))}: ${escapeHTML(it.title)}</strong>
        <span class="muted small">${escapeHTML(it.summary || "")}</span>
        <span class="muted small">origen ${escapeHTML(shortId(it.origin_node_id))} · ${fmtTime(it.created)}</span></div>`;
      inboxBox.appendChild(div);
    }

    const mdns = data.mdns || [];
    const mdnsBox = $("#fed-mdns-list");
    const mdnsEmpty = $("#fed-mdns-empty");
    mdnsBox.innerHTML = "";
    mdnsEmpty.classList.toggle("hidden", mdns.length > 0);
    for (const m of mdns) {
      const div = document.createElement("div");
      div.className = "file-row";
      div.setAttribute("role", "listitem");
      const hint = m.url_hint || "";
      div.innerHTML = `<div class="file-meta"><strong>${escapeHTML(m.name || m.host)}</strong>
        <span class="muted small">${escapeHTML(shortId(m.node_id))} · puerto ${m.port}</span></div>
        ${hint ? `<button type="button" class="btn-secondary btn-fed-mdns" data-url="${escapeHTML(hint)}">Añadir</button>` : ""}`;
      mdnsBox.appendChild(div);
    }
    mdnsBox.querySelectorAll(".btn-fed-mdns").forEach((btn) => {
      btn.addEventListener("click", async () => {
        try {
          await fetchJSON("/api/federacion/peers", { method: "POST", body: JSON.stringify({ peer_url: btn.dataset.url }) });
          await loadFederacion();
          setStatus("Peer mDNS añadido", "ok");
        } catch (e) { setStatus(e.message, "err"); }
      });
    });

    const prensaNotes = data.last_prensa_fetched || [];
    const prensaBox = $("#fed-prensa-list");
    const prensaEmpty = $("#fed-prensa-empty");
    if (prensaBox && prensaEmpty) {
      prensaBox.innerHTML = "";
      const okNotes = prensaNotes.filter((n) => n.ok);
      prensaEmpty.classList.toggle("hidden", okNotes.length > 0 || prensaNotes.length > 0);
      if (prensaNotes.length === 0) {
        prensaEmpty.classList.remove("hidden");
      } else {
        prensaEmpty.classList.add("hidden");
      }
      for (const n of prensaNotes.slice(0, 30)) {
        const div = document.createElement("div");
        div.className = "file-row";
        div.setAttribute("role", "listitem");
        const mark = n.ok ? "✓" : "·";
        div.innerHTML = `<div class="file-meta"><strong>${mark} ${escapeHTML(n.title || n.pucela_id)}</strong>
          <span class="muted small">${escapeHTML(n.pucela_id || "")}${n.note ? " · " + escapeHTML(n.note) : ""}</span>
          <span class="muted small">${fmtTime(n.at)}${n.from_url ? " · " + escapeHTML(n.from_url) : ""}</span></div>`;
        prensaBox.appendChild(div);
      }
    }

    const last = $("#fed-last-sync");
    if (last) last.textContent = data.last_sync_at ? "Última sync: " + fmtTime(data.last_sync_at) : "Sin sync todavía.";
  }

  function showFederacion() {
    stopPoll();
    hideAllViews();
    viewFederacion.classList.remove("hidden");
    btnBack.classList.add("hidden");
    title.textContent = "Federación";
    subtitle.textContent = "Nodos autónomos · feed firmado";
    setNav("federacion");
    history.pushState({ view: "federacion" }, "", "/federacion");
    loadFederacion().catch((e) => setStatus(e.message, "err"));
  }

  async function loadNodoStatus() {
    const data = await fetchJSON("/api/node/status");
    const set = (id, v) => { const el = $(id); if (el) el.textContent = v; };
    set("#nodo-version", data.version || "—");
    set("#nodo-id-short", (data.node_id_short || "—") + "…");
    set("#nodo-uptime", data.uptime_human || "—");
    set("#nodo-datadir", data.data_dir_human || "—");
    set("#nodo-peers", String(data.peers_count ?? "—"));
    set("#nodo-places", String(data.places_count ?? "—"));
    set("#nodo-health", data.health || "—");
    const warn = $("#nodo-pin-warning");
    const hint = $("#nodo-pin-hint");
    const pinReq = !!data.operator_pin_required;
    if (warn) {
      if (!pinReq && data.operator_pin_warning) {
        warn.textContent = "⚠️ " + data.operator_pin_warning;
        warn.classList.remove("hidden");
      } else {
        warn.textContent = pinReq ? "PIN activo en este nodo." : "";
        warn.classList.toggle("hidden", !pinReq);
        if (pinReq) warn.classList.remove("warn-secret");
      }
    }
    if (hint) {
      hint.textContent = pinReq
        ? "PIN obligatorio para backup y restore (cabecera X-Operator-Pin)."
        : "Sin PIN (modo dev). En un Pi real: --operator-pin o data-dir/operator.pin.";
    }
    return data;
  }

  function operatorPinHeaders(extra) {
    const h = Object.assign({}, extra || {});
    const pinEl = $("#nodo-operator-pin");
    const pin = pinEl && pinEl.value ? pinEl.value.trim() : "";
    if (pin) h["X-Operator-Pin"] = pin;
    return h;
  }


  /* —— v1.7 kiosk + novedades —— */
  const KIOSK_KEY = "rcv_kiosk_v17";
  const KIOSK_IDLE_KEY = "rcv_kiosk_idle_min";
  const KIOSK_FS_HINT_KEY = "rcv_kiosk_fs_hint_v17";
  let kioskOn = false;
  let kioskIdleMin = 2;
  let kioskIdleTimer = null;
  let kioskHoldTimer = null;
  let kioskHoldStart = 0;

  function readKioskPrefs() {
    try {
      kioskOn = localStorage.getItem(KIOSK_KEY) === "1";
      const n = parseInt(localStorage.getItem(KIOSK_IDLE_KEY) || "2", 10);
      kioskIdleMin = n >= 1 && n <= 5 ? n : 2;
    } catch (_) {
      kioskOn = false;
      kioskIdleMin = 2;
    }
  }

  function saveKioskPrefs() {
    try {
      localStorage.setItem(KIOSK_KEY, kioskOn ? "1" : "0");
      localStorage.setItem(KIOSK_IDLE_KEY, String(kioskIdleMin));
    } catch (_) {}
  }

  function applyKioskUI() {
    document.body.classList.toggle("kiosk-mode", kioskOn);
    document.querySelectorAll(".kiosk-only").forEach((el) => {
      el.classList.toggle("hidden", !kioskOn);
    });
    const tog = $("#nodo-kiosk-toggle");
    if (tog) tog.checked = kioskOn;
    const sel = $("#nodo-kiosk-idle");
    if (sel) sel.value = String(kioskIdleMin);
    const fab = $("#btn-kiosk-exit-fab");
    if (fab) fab.classList.toggle("hidden", !kioskOn);
    const hold = $("#btn-kiosk-exit-hold");
    if (hold) hold.classList.toggle("hidden", !kioskOn);
    if (kioskOn) {
      setHomeViewMode("calles");
      maybeShowKioskFsHint();
      armKioskIdle();
    } else {
      hideKioskFsHint();
      clearKioskIdle();
    }
  }

  function setKioskEnabled(on) {
    kioskOn = !!on;
    saveKioskPrefs();
    applyKioskUI();
    const fb = $("#nodo-kiosk-feedback");
    if (fb) fb.textContent = kioskOn ? "Kiosko activo · toques grandes · backup oculto" : "Kiosko desactivado";
    setStatus(kioskOn ? "Modo kiosko" : "Kiosko off", "ok");
  }

  function setKioskIdleMin(n) {
    n = parseInt(n, 10);
    if (!(n >= 1 && n <= 5)) n = 2;
    kioskIdleMin = n;
    saveKioskPrefs();
    if (kioskOn) armKioskIdle();
  }

  function clearKioskIdle() {
    if (kioskIdleTimer) {
      clearTimeout(kioskIdleTimer);
      kioskIdleTimer = null;
    }
  }

  function armKioskIdle() {
    clearKioskIdle();
    if (!kioskOn) return;
    kioskIdleTimer = setTimeout(() => {
      if (!kioskOn) return;
      try {
        setHomeViewMode("calles");
        showHome();
        history.pushState({ view: "home" }, "", "/");
        setStatus("Kiosko · vuelta al mapa", "ok");
      } catch (_) {}
      armKioskIdle();
    }, kioskIdleMin * 60 * 1000);
  }

  function bumpKioskIdle() {
    if (kioskOn) armKioskIdle();
  }

  function maybeShowKioskFsHint() {
    const box = $("#kiosk-fs-hint");
    if (!box || !kioskOn) return;
    try {
      if (localStorage.getItem(KIOSK_FS_HINT_KEY) === "1") {
        box.classList.add("hidden");
        return;
      }
    } catch (_) {}
    box.classList.remove("hidden");
  }

  function hideKioskFsHint() {
    const box = $("#kiosk-fs-hint");
    if (box) box.classList.add("hidden");
  }

  function bindHoldToExit(el) {
    if (!el || el.dataset.holdBound === "1") return;
    el.dataset.holdBound = "1";
    const HOLD_MS = 2000;
    const clearHold = () => {
      if (kioskHoldTimer) {
        clearInterval(kioskHoldTimer);
        kioskHoldTimer = null;
      }
      el.style.setProperty("--hold-pct", "0%");
    };
    const start = (ev) => {
      if (!kioskOn) return;
      ev.preventDefault();
      kioskHoldStart = Date.now();
      clearHold();
      kioskHoldTimer = setInterval(() => {
        const pct = Math.min(100, ((Date.now() - kioskHoldStart) / HOLD_MS) * 100);
        el.style.setProperty("--hold-pct", pct + "%");
        if (pct >= 100) {
          clearHold();
          setKioskEnabled(false);
        }
      }, 40);
    };
    const end = () => clearHold();
    el.addEventListener("pointerdown", start);
    el.addEventListener("pointerup", end);
    el.addEventListener("pointerleave", end);
    el.addEventListener("pointercancel", end);
  }

  async function loadNovedades() {
    const data = await fetchJSON("/api/changelog");
    const cur = $("#novedades-current");
    if (cur) cur.textContent = data.current || "—";
    const box = $("#novedades-list");
    if (!box) return data;
    box.innerHTML = "";
    for (const e of data.entries || []) {
      const card = document.createElement("article");
      card.className = "novedades-card" + (e.version === data.current ? " current" : "");
      card.setAttribute("role", "listitem");
      const lis = (e.highlights || []).map((h) => `<li>${escapeHTML(h)}</li>`).join("");
      card.innerHTML =
        `<h3><span class="novedades-ver">v${escapeHTML(e.version)}</span>${escapeHTML(e.title || "")}</h3>` +
        `<ul>${lis}</ul>`;
      box.appendChild(card);
    }
    return data;
  }

  function showNovedades() {
    stopPoll();
    hideAllViews();
    if (viewNovedades) viewNovedades.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = "Qué hay de nuevo";
    subtitle.textContent = "Historial del nodo";
    setNav("tool");
    history.pushState({ view: "novedades" }, "", "/novedades");
    loadNovedades()
      .then(() => setStatus("Novedades", "ok"))
      .catch((e) => setStatus(e.message, "err"));
  }

  function showNodoPanel() {
    stopPoll();
    hideAllViews();
    if (viewNodo) viewNodo.classList.remove("hidden");
    btnBack.classList.remove("hidden");
    title.textContent = "Panel del nodo";
    subtitle.textContent = kioskOn ? "Kiosko · ajustes" : "Operador · kiosko · backup";
    setNav("tool");
    history.pushState({ view: "nodo" }, "", "/nodo");
    loadNodoStatus()
      .then(() => setStatus("Panel del nodo", "ok"))
      .catch((e) => setStatus(e.message, "err"));
  }



  /* --- Taller comunitario (v5.13 claims + colas firmadas) --- */
  function showTallerStep(name) {
    ["list", "form", "detail", "remoto"].forEach((n) => {
      const el = $("#taller-view-" + n);
      if (el) el.classList.toggle("hidden", n !== name);
    });
  }

  async function setupTaller(page, p) {
    const box = $("#place-taller");
    if (!box) return;
    if (!p || p.id !== "taller-comunitario") {
      box.classList.add("hidden");
      currentTallerProyectoId = null;
      return;
    }
    box.classList.remove("hidden");
    showTallerStep("list");
    const meta = await fetchJSON("/api/taller").catch(() => null);
    if (meta && meta.nota) {
      const n = $("#taller-nota");
      if (n) n.textContent = meta.nota;
    }
    await loadTallerProyectos();
  }

  async function loadTallerProyectos() {
    const estado = ($("#taller-filter-estado") || {}).value || "";
    const categoria = ($("#taller-filter-categoria") || {}).value || "";
    const ambito = ($("#taller-filter-ambito") || {}).value || "nodo";
    const q = new URLSearchParams();
    if (estado) q.set("estado", estado);
    if (categoria) q.set("categoria", categoria);
    if (ambito) q.set("ambito", ambito);
    const url = "/api/taller/proyectos" + (q.toString() ? "?" + q.toString() : "");
    const data = await fetchJSON(url);
    const ul = $("#taller-proyectos");
    const empty = $("#taller-list-empty");
    if (!ul) return;
    ul.innerHTML = "";
    const list = data.proyectos || [];
    const btnNuevo = $("#btn-taller-nuevo");
    if (btnNuevo) btnNuevo.classList.toggle("hidden", ambito === "red");
    if (!list.length) {
      if (empty) {
        empty.textContent = data.empty_hint || "Aún no hay proyectos.";
        empty.classList.remove("hidden");
      }
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const pr of list) {
      const li = document.createElement("li");
      const isRemote = ambito === "red" && pr.origin_node_id && me && me.node_id && pr.origin_node_id !== me.node_id;
      const isPublicDto = !!pr.title || !!pr.origin_node_id;
      li.className = "tool-card" + (isRemote ? " taller-remote" : "");
      li.tabIndex = 0;
      if (isRemote) {
        li.setAttribute("role", "button");
        const title = pr.title || pr.titulo || pr.id;
        const cat = pr.category || pr.categoria || "";
        const est = pr.status || pr.estado || "";
        const blurb = pr.blurb || pr.descripcion || "";
        li.innerHTML =
          `<strong>${escapeHTML(title)}</strong>` +
          `<span class="tool-status">🌐 red · ${escapeHTML(est)} · ${escapeHTML(cat)}</span>` +
          `<span class="preview">${escapeHTML(String(blurb).slice(0, 140))}</span>` +
          `<span class="preview">Tareas abiertas: ${pr.open_tasks || 0} · origen ${escapeHTML(shortId(pr.origin_node_id || ""))}</span>` +
          `<span class="hint">Reclamar en el origen (firmado) · sin sync del tablero</span>`;
        const openRemoto = () => openTallerRemoto({
          origin_node_id: pr.origin_node_id,
          proyecto_id: pr.id,
          title: title,
          blurb: blurb,
          category: cat,
          status: est,
          open_tasks: pr.open_tasks || 0,
        }).catch((e) => setStatus(e.message, "err"));
        li.addEventListener("click", openRemoto);
        li.addEventListener("keydown", (ev) => {
          if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); openRemoto(); }
        });
      } else {
        li.setAttribute("role", "button");
        const cat = pr.categoria || pr.category || "";
        const est = pr.estado || pr.status || "";
        const titulo = pr.titulo || pr.title || pr.id;
        const desc = pr.descripcion || pr.blurb || "";
        li.innerHTML =
          `<strong>${escapeHTML(titulo)}</strong>` +
          `<span class="tool-status">${escapeHTML(est)} · ${escapeHTML(cat)}</span>` +
          `<span class="preview">${escapeHTML(String(desc).slice(0, 140))}</span>` +
          (isPublicDto
            ? `<span class="preview">Tareas abiertas: ${pr.open_tasks || 0}</span>`
            : `<span class="preview">Tareas: ${pr.tareas_libres || 0} libres · ${pr.tareas_reclamadas || 0} reclamadas · ${pr.tareas_hechas || 0} hechas · aportes ${pr.aportes_n || 0}</span>`);
        const open = () => openTallerDetalle(pr.id).catch((e) => setStatus(e.message, "err"));
        li.addEventListener("click", open);
        li.addEventListener("keydown", (ev) => {
          if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(); }
        });
      }
      ul.appendChild(li);
    }
  }

  async function openTallerDetalle(id) {
    currentTallerProyectoId = id;
    const det = await fetchJSON("/api/taller/proyectos/" + encodeURIComponent(id));
    showTallerStep("detail");
    const pr = det.proyecto || {};
    $("#taller-detail-titulo").textContent = pr.titulo || id;
    $("#taller-detail-meta").textContent =
      (pr.categoria || "") + " · " + (pr.estado || "") + " · owner " + shortId(pr.owner_id || "");
    $("#taller-detail-desc").textContent = pr.descripcion || "";
    const sel = $("#taller-detail-estado");
    if (sel) sel.value = pr.estado || "abierto";
    if (det.nota) {
      const n = $("#taller-nota");
      if (n) n.textContent = det.nota;
    }
    renderTallerTareas(det.tareas || []);
    renderTallerAportes(det.aportes || []);
    await loadTallerCola(id);
    const fb = $("#taller-detail-feedback");
    if (fb) fb.textContent = "";
  }

  function renderTallerTareas(list) {
    const ul = $("#taller-tareas");
    const empty = $("#taller-tareas-empty");
    if (!ul) return;
    ul.innerHTML = "";
    if (!list.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const ta of list) {
      const li = document.createElement("li");
      li.className = "taller-tarea";
      const claimer = ta.claimed_by ? " · " + shortId(ta.claimed_by) : "";
      li.innerHTML =
        `<strong>${escapeHTML(ta.titulo || ta.id)}</strong>` +
        `<span class="tool-status">${escapeHTML(ta.estado || "")}${escapeHTML(claimer)}</span>` +
        (ta.notas ? `<span class="preview">${escapeHTML(ta.notas)}</span>` : "") +
        `<span class="row-actions taller-tarea-actions"></span>`;
      const actions = li.querySelector(".taller-tarea-actions");
      const addBtn = (label, act) => {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "btn-secondary btn-sm";
        b.textContent = label;
        b.addEventListener("click", (ev) => {
          ev.stopPropagation();
          tallerTareaAction(ta.id, act).catch((e) => setStatus(e.message, "err"));
        });
        actions.appendChild(b);
      };
      if (ta.estado === "libre") addBtn("Reclamar", "reclamar");
      if (ta.estado === "reclamada") {
        addBtn("Liberar", "liberar");
        addBtn("Completar", "completar");
      }
      ul.appendChild(li);
    }
  }

  function renderTallerAportes(list) {
    const ul = $("#taller-aportes");
    const empty = $("#taller-aportes-empty");
    if (!ul) return;
    ul.innerHTML = "";
    if (!list.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const ap of list) {
      const li = document.createElement("li");
      const refs = [];
      if (ap.file_id) refs.push("file:" + ap.file_id);
      if (ap.pucela_id) refs.push("pucela:" + ap.pucela_id);
      li.innerHTML =
        `<strong>${escapeHTML(ap.titulo || ap.id)}</strong>` +
        `<span class="preview">por ${escapeHTML(shortId(ap.author_id || ""))}` +
        (refs.length ? " · " + escapeHTML(refs.join(" · ")) : "") +
        `</span>` +
        (ap.notas ? `<span class="preview">${escapeHTML(ap.notas)}</span>` : "");
      ul.appendChild(li);
    }
  }

  async function tallerTareaAction(tareaId, action) {
    const path = "/api/taller/tareas/" + encodeURIComponent(tareaId) + "/" + action;
    await fetchJSON(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: me.user_id || "" }),
    });
    if (currentTallerProyectoId) await openTallerDetalle(currentTallerProyectoId);
    setStatus("Tarea actualizada", "ok");
  }



  async function loadTallerCola(proyectoId) {
    const data = await fetchJSON("/api/taller/proyectos/" + encodeURIComponent(proyectoId) + "/cola").catch(() => ({ jobs: [] }));
    renderTallerCola(data.jobs || []);
  }

  function renderTallerCola(list) {
    const ul = $("#taller-cola");
    const empty = $("#taller-cola-empty");
    if (!ul) return;
    ul.innerHTML = "";
    if (!list.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const j of list) {
      const li = document.createElement("li");
      li.className = "taller-tarea";
      const tip = j.holder_tip ? " · " + j.holder_tip : "";
      li.innerHTML =
        `<strong>${escapeHTML(j.title || j.id)}</strong>` +
        `<span class="tool-status">${escapeHTML(j.status || "")}${escapeHTML(tip)}</span>` +
        (j.blurb ? `<span class="preview">${escapeHTML(j.blurb)}</span>` : "");
      ul.appendChild(li);
    }
  }

  async function tallerAddJob() {
    if (!currentTallerProyectoId) return;
    const fb = $("#taller-detail-feedback");
    const titulo = ($("#taller-job-titulo") || {}).value || "";
    const payload = ($("#taller-job-payload") || {}).value || "";
    await fetchJSON("/api/taller/proyectos/" + encodeURIComponent(currentTallerProyectoId) + "/cola", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: titulo, blurb: "", payload: payload }),
    });
    if ($("#taller-job-titulo")) $("#taller-job-titulo").value = "";
    if ($("#taller-job-payload")) $("#taller-job-payload").value = "";
    await loadTallerCola(currentTallerProyectoId);
    if (fb) fb.textContent = "Job añadido a la cola";
    setStatus("Job en cola", "ok");
  }


  async function openTallerRemoto(meta) {
    currentTallerRemoto = meta;
    currentTallerRemotoCompleteId = null;
    showTallerStep("remoto");
    $("#taller-remoto-titulo").textContent = meta.title || meta.proyecto_id;
    $("#taller-remoto-meta").textContent =
      "origen " + shortId(meta.origin_node_id || "") + " · " + (meta.status || "") + " · " + (meta.category || "") +
      " · abiertas (índice): " + (meta.open_tasks || 0);
    $("#taller-remoto-blurb").textContent = meta.blurb || "";
    const fb = $("#taller-remoto-feedback");
    if (fb) fb.textContent = "";
    const box = $("#taller-remoto-complete-box");
    if (box) box.classList.add("hidden");
    await refreshTallerRemoto();
  }

  async function refreshTallerRemoto() {
    if (!currentTallerRemoto) return;
    const q = new URLSearchParams({
      origin_node_id: currentTallerRemoto.origin_node_id,
      proyecto_id: currentTallerRemoto.proyecto_id,
    });
    const data = await fetchJSON("/api/taller/remoto/claimable?" + q.toString());
    renderTallerRemotoTareas(data.tareas || []);
    const all = await fetchJSON("/api/taller/remoto/mis-claims").catch(() => ({ claims: [] }));
    const mine = (all.claims || []).filter(
      (c) => c.origin_node_id === currentTallerRemoto.origin_node_id && c.proyecto_id === currentTallerRemoto.proyecto_id
    );
    renderTallerRemotoMis(mine);
    const cola = await fetchJSON("/api/taller/remoto/cola?" + q.toString()).catch(() => ({ jobs: [] }));
    renderTallerRemotoCola(cola.jobs || []);
    const leases = await fetchJSON("/api/taller/remoto/mis-leases").catch(() => ({ leases: [] }));
    const myLeases = (leases.leases || []).filter(
      (c) => c.origin_node_id === currentTallerRemoto.origin_node_id && c.proyecto_id === currentTallerRemoto.proyecto_id
    );
    renderTallerRemotoMisLeases(myLeases);
  }

  function renderTallerRemotoTareas(list) {
    const ul = $("#taller-remoto-tareas");
    const empty = $("#taller-remoto-tareas-empty");
    if (!ul) return;
    ul.innerHTML = "";
    const open = (list || []).filter((t) => t.status === "open");
    if (!open.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const ta of open) {
      const li = document.createElement("li");
      li.className = "taller-tarea";
      li.innerHTML =
        `<strong>${escapeHTML(ta.title || ta.id)}</strong>` +
        `<span class="tool-status">${escapeHTML(ta.status || "")}</span>` +
        (ta.blurb ? `<span class="preview">${escapeHTML(ta.blurb)}</span>` : "") +
        `<span class="row-actions"></span>`;
      const actions = li.querySelector(".row-actions");
      const b = document.createElement("button");
      b.type = "button";
      b.className = "btn-secondary btn-sm";
      b.textContent = "Reclamar";
      b.addEventListener("click", (ev) => {
        ev.stopPropagation();
        tallerRemotoClaim(ta).catch((e) => setStatus(e.message, "err"));
      });
      actions.appendChild(b);
      ul.appendChild(li);
    }
  }

  function renderTallerRemotoMis(list) {
    const ul = $("#taller-remoto-mis");
    const empty = $("#taller-remoto-mis-empty");
    if (!ul) return;
    ul.innerHTML = "";
    if (!list.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const c of list) {
      const li = document.createElement("li");
      li.className = "taller-tarea";
      li.innerHTML =
        `<strong>${escapeHTML(c.tarea_title || c.tarea_id)}</strong>` +
        `<span class="tool-status">${escapeHTML(c.status || "")}</span>` +
        `<span class="row-actions"></span>`;
      const actions = li.querySelector(".row-actions");
      if (c.status === "claimed") {
        const liberar = document.createElement("button");
        liberar.type = "button";
        liberar.className = "btn-secondary btn-sm";
        liberar.textContent = "Liberar";
        liberar.addEventListener("click", (ev) => {
          ev.stopPropagation();
          tallerRemotoRelease(c).catch((e) => setStatus(e.message, "err"));
        });
        actions.appendChild(liberar);
        const completar = document.createElement("button");
        completar.type = "button";
        completar.className = "btn-primary btn-sm";
        completar.textContent = "Entregar";
        completar.addEventListener("click", (ev) => {
          ev.stopPropagation();
          currentTallerRemotoCompleteId = c.tarea_id;
          const box = $("#taller-remoto-complete-box");
          if (box) box.classList.remove("hidden");
          const tit = $("#taller-remoto-aporte-titulo");
          if (tit) tit.value = "Aporte: " + (c.tarea_title || c.tarea_id);
          setStatus("Completá notas y refs, luego «Completar y entregar»", "ok");
        });
        actions.appendChild(completar);
      }
      ul.appendChild(li);
    }
  }


  function renderTallerRemotoCola(list) {
    const ul = $("#taller-remoto-cola");
    const empty = $("#taller-remoto-cola-empty");
    if (!ul) return;
    ul.innerHTML = "";
    const queued = (list || []).filter((j) => j.status === "queued");
    if (!queued.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const j of queued) {
      const li = document.createElement("li");
      li.className = "taller-tarea";
      li.innerHTML =
        `<strong>${escapeHTML(j.title || j.id)}</strong>` +
        `<span class="tool-status">${escapeHTML(j.status || "")}</span>` +
        (j.blurb ? `<span class="preview">${escapeHTML(j.blurb)}</span>` : "") +
        `<span class="row-actions"></span>`;
      const actions = li.querySelector(".row-actions");
      const b = document.createElement("button");
      b.type = "button";
      b.className = "btn-secondary btn-sm";
      b.textContent = "Tomar job";
      b.addEventListener("click", (ev) => {
        ev.stopPropagation();
        tallerRemotoColaLease(j).catch((e) => setStatus(e.message, "err"));
      });
      actions.appendChild(b);
      ul.appendChild(li);
    }
    // Botón tomar siguiente sin id
    const next = document.createElement("li");
    next.className = "taller-tarea";
    next.innerHTML = `<strong>Siguiente en cola</strong><span class="row-actions"></span>`;
    const nb = document.createElement("button");
    nb.type = "button";
    nb.className = "btn-primary btn-sm";
    nb.textContent = "Tomar siguiente";
    nb.addEventListener("click", (ev) => {
      ev.stopPropagation();
      tallerRemotoColaLease(null).catch((e) => setStatus(e.message, "err"));
    });
    next.querySelector(".row-actions").appendChild(nb);
    ul.appendChild(next);
  }

  function renderTallerRemotoMisLeases(list) {
    const ul = $("#taller-remoto-mis-leases");
    const empty = $("#taller-remoto-mis-leases-empty");
    if (!ul) return;
    ul.innerHTML = "";
    if (!list.length) {
      if (empty) empty.classList.remove("hidden");
      return;
    }
    if (empty) empty.classList.add("hidden");
    for (const c of list) {
      const li = document.createElement("li");
      li.className = "taller-tarea";
      li.innerHTML =
        `<strong>${escapeHTML(c.job_title || c.job_id)}</strong>` +
        `<span class="tool-status">${escapeHTML(c.status || "")}</span>` +
        `<span class="row-actions"></span>`;
      const actions = li.querySelector(".row-actions");
      if (c.status === "leased") {
        const ren = document.createElement("button");
        ren.type = "button";
        ren.className = "btn-secondary btn-sm";
        ren.textContent = "Renovar";
        ren.addEventListener("click", (ev) => {
          ev.stopPropagation();
          tallerRemotoColaRenew(c).catch((e) => setStatus(e.message, "err"));
        });
        actions.appendChild(ren);
        const ent = document.createElement("button");
        ent.type = "button";
        ent.className = "btn-primary btn-sm";
        ent.textContent = "Entregar";
        ent.addEventListener("click", (ev) => {
          ev.stopPropagation();
          currentTallerRemotoJobId = c.job_id;
          const box = $("#taller-remoto-job-complete-box");
          if (box) box.classList.remove("hidden");
          setStatus("Completá notas y «Entregar job»", "ok");
        });
        actions.appendChild(ent);
      }
      ul.appendChild(li);
    }
  }

  async function tallerRemotoColaLease(job) {
    if (!currentTallerRemoto) return;
    const body = {
      origin_node_id: currentTallerRemoto.origin_node_id,
      proyecto_id: currentTallerRemoto.proyecto_id,
      proyecto_title: currentTallerRemoto.title || "",
    };
    if (job && job.id) {
      body.job_id = job.id;
      body.job_title = job.title || "";
    }
    const res = await fetchJSON("/api/taller/remoto/cola/lease", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    setStatus("Job arrendado" + (res.job && res.job.payload ? " · payload recibido" : ""), "ok");
    await refreshTallerRemoto();
  }

  async function tallerRemotoColaRenew(c) {
    await fetchJSON("/api/taller/remoto/cola/renew", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        origin_node_id: c.origin_node_id,
        proyecto_id: c.proyecto_id,
        job_id: c.job_id,
      }),
    });
    setStatus("Lease renovado", "ok");
    await refreshTallerRemoto();
  }

  async function tallerRemotoColaComplete() {
    if (!currentTallerRemoto || !currentTallerRemotoJobId) {
      setStatus("Elegí un job arrendado (Entregar)", "err");
      return;
    }
    const maxBytes = 8 * 1024 * 1024;
    const fileInput = $("#taller-remoto-job-file");
    const file = fileInput && fileInput.files && fileInput.files[0];
    const prog = $("#taller-remoto-job-progress");
    if (file && file.size > maxBytes) {
      const msg = "Fichero demasiado grande (máx ~8 MiB)";
      if (prog) prog.textContent = msg;
      setStatus(msg, "err");
      return;
    }
    const fd = new FormData();
    fd.append("origin_node_id", currentTallerRemoto.origin_node_id);
    fd.append("proyecto_id", currentTallerRemoto.proyecto_id);
    fd.append("proyecto_title", currentTallerRemoto.title || "");
    fd.append("job_id", currentTallerRemotoJobId);
    fd.append("result_notas", ($("#taller-remoto-job-notas") || {}).value || "");
    if (file) fd.append("file", file, file.name);
    if (prog) prog.textContent = file ? "Subiendo y entregando…" : "Entregando job…";
    const res = await fetch("/api/taller/remoto/cola/complete", { method: "POST", body: fd, headers: { Accept: "application/json" } });
    if (!res.ok) {
      let detail = "HTTP " + res.status;
      try { const j = await res.json(); if (j.error) detail = j.error; } catch (_) {}
      if (prog) prog.textContent = detail;
      throw new Error(detail);
    }
    if (prog) prog.textContent = "Job entregado";
    currentTallerRemotoJobId = null;
    const box = $("#taller-remoto-job-complete-box");
    if (box) box.classList.add("hidden");
    if (fileInput) fileInput.value = "";
    setStatus("Job entregado en el origen", "ok");
    await refreshTallerRemoto();
  }

  async function tallerRemotoColaFail() {
    if (!currentTallerRemoto || !currentTallerRemotoJobId) {
      setStatus("Elegí un job arrendado", "err");
      return;
    }
    await fetchJSON("/api/taller/remoto/cola/fail", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        origin_node_id: currentTallerRemoto.origin_node_id,
        proyecto_id: currentTallerRemoto.proyecto_id,
        job_id: currentTallerRemotoJobId,
        result_notas: ($("#taller-remoto-job-notas") || {}).value || "fallido",
      }),
    });
    currentTallerRemotoJobId = null;
    const box = $("#taller-remoto-job-complete-box");
    if (box) box.classList.add("hidden");
    setStatus("Job marcado fallido", "ok");
    await refreshTallerRemoto();
  }

  async function showTallerMisLeasesGlobal() {
    const data = await fetchJSON("/api/taller/remoto/mis-leases");
    const list = data.leases || [];
    if (!list.length) {
      setStatus("No tenés leases de cola aún", "ok");
      return;
    }
    const c = list[0];
    await openTallerRemoto({
      origin_node_id: c.origin_node_id,
      proyecto_id: c.proyecto_id,
      title: c.proyecto_title || c.proyecto_id,
      blurb: "", category: "", status: "", open_tasks: 0,
    });
    setStatus("Mis leases: " + list.length, "ok");
  }


  async function tallerRemotoClaim(ta) {
    if (!currentTallerRemoto) return;
    await fetchJSON("/api/taller/remoto/claim", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        origin_node_id: currentTallerRemoto.origin_node_id,
        proyecto_id: currentTallerRemoto.proyecto_id,
        proyecto_title: currentTallerRemoto.title || "",
        tarea_id: ta.id,
        tarea_title: ta.title || "",
      }),
    });
    setStatus("Tarea reclamada en el origen", "ok");
    await refreshTallerRemoto();
  }

  async function tallerRemotoRelease(c) {
    if (!currentTallerRemoto) return;
    await fetchJSON("/api/taller/remoto/release", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        origin_node_id: c.origin_node_id,
        proyecto_id: c.proyecto_id,
        tarea_id: c.tarea_id,
        tarea_title: c.tarea_title || "",
      }),
    });
    setStatus("Tarea liberada", "ok");
    await refreshTallerRemoto();
  }

  async function tallerRemotoComplete() {
    if (!currentTallerRemoto || !currentTallerRemotoCompleteId) {
      setStatus("Elegí una tarea reclamada (Entregar)", "err");
      return;
    }
    const maxBytes = 8 * 1024 * 1024; // alineado con files.MaxBytes
    const fileInput = $("#taller-remoto-aporte-file");
    const pucelaInput = $("#taller-remoto-aporte-pucela");
    const prog = $("#taller-remoto-upload-progress");
    const file = fileInput && fileInput.files && fileInput.files[0];
    const pucela = pucelaInput && pucelaInput.files && pucelaInput.files[0];
    if (file && file.size > maxBytes) {
      const msg = "Fichero demasiado grande (máx ~8 MiB cívicos)";
      if (prog) prog.textContent = msg;
      setStatus(msg, "err");
      return;
    }
    if (pucela && pucela.size > maxBytes) {
      const msg = ".pucela demasiado grande (máx ~8 MiB)";
      if (prog) prog.textContent = msg;
      setStatus(msg, "err");
      return;
    }
    const fd = new FormData();
    fd.append("origin_node_id", currentTallerRemoto.origin_node_id);
    fd.append("proyecto_id", currentTallerRemoto.proyecto_id);
    fd.append("proyecto_title", currentTallerRemoto.title || "");
    fd.append("tarea_id", currentTallerRemotoCompleteId);
    fd.append("aporte_titulo", ($("#taller-remoto-aporte-titulo") || {}).value || "");
    fd.append("aporte_notas", ($("#taller-remoto-aporte-notas") || {}).value || "");
    if (file) fd.append("file", file, file.name);
    if (pucela) fd.append("pucela", pucela, pucela.name);
    if (prog) {
      prog.textContent = file || pucela
        ? "Subiendo artefacto al origen…"
        : "Completando claim…";
    }
    const res = await fetch("/api/taller/remoto/complete", { method: "POST", body: fd, headers: { Accept: "application/json" } });
    if (!res.ok) {
      let detail = "HTTP " + res.status;
      try {
        const j = await res.json();
        if (j.error) detail = j.error;
      } catch (_) {}
      if (prog) prog.textContent = detail;
      throw new Error(detail);
    }
    const data = await res.json();
    if (prog) {
      const bits = [];
      if (data.file_id) bits.push("file:" + data.file_id);
      if (data.pucela_id) bits.push("pucela:" + data.pucela_id);
      prog.textContent = bits.length ? "Subido · " + bits.join(" · ") : "Entregado sin adjunto";
    }
    currentTallerRemotoCompleteId = null;
    const box = $("#taller-remoto-complete-box");
    if (box) box.classList.add("hidden");
    if (fileInput) fileInput.value = "";
    if (pucelaInput) pucelaInput.value = "";
    setStatus("Aporte entregado en el origen", "ok");
    await refreshTallerRemoto();
  }

  async function showTallerMisClaimsGlobal() {
    const data = await fetchJSON("/api/taller/remoto/mis-claims");
    const list = data.claims || [];
    if (!list.length) {
      setStatus("No tenés claims remotos aún", "ok");
      return;
    }
    // Abrir el más reciente
    const c = list[0];
    await openTallerRemoto({
      origin_node_id: c.origin_node_id,
      proyecto_id: c.proyecto_id,
      title: c.proyecto_title || c.proyecto_id,
      blurb: "",
      category: "",
      status: "",
      open_tasks: 0,
    });
    setStatus("Mis claims: " + list.length, "ok");
  }

  function bindTallerUI() {

    const btnNuevo = $("#btn-taller-nuevo");
    if (btnNuevo) btnNuevo.addEventListener("click", () => {
      showTallerStep("form");
      const fb = $("#taller-form-feedback");
      if (fb) fb.textContent = "";
    });
    const btnCancel = $("#btn-taller-cancel-form");
    if (btnCancel) btnCancel.addEventListener("click", () => {
      showTallerStep("list");
      loadTallerProyectos().catch((e) => setStatus(e.message, "err"));
    });
    const btnBack = $("#btn-taller-back-list");
    if (btnBack) btnBack.addEventListener("click", () => {
      currentTallerProyectoId = null;
      showTallerStep("list");
      loadTallerProyectos().catch((e) => setStatus(e.message, "err"));
    });
    const btnCrear = $("#btn-taller-crear");
    if (btnCrear) btnCrear.addEventListener("click", async () => {
      const fb = $("#taller-form-feedback");
      try {
        const data = await fetchJSON("/api/taller/proyectos", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            titulo: ($("#taller-form-titulo") || {}).value || "",
            descripcion: ($("#taller-form-desc") || {}).value || "",
            categoria: ($("#taller-form-categoria") || {}).value || "otro",
          }),
        });
        if (fb) fb.textContent = "Proyecto creado";
        const id = data.proyecto && data.proyecto.id;
        if (id) await openTallerDetalle(id);
        else {
          showTallerStep("list");
          await loadTallerProyectos();
        }
        setStatus("Proyecto creado", "ok");
      } catch (e) {
        if (fb) fb.textContent = e.message;
        setStatus(e.message, "err");
      }
    });
    for (const id of ["taller-filter-estado", "taller-filter-categoria", "taller-filter-ambito"]) {
      const el = $("#" + id);
      if (el) el.addEventListener("change", () => loadTallerProyectos().catch((e) => setStatus(e.message, "err")));
    }
    const btnSync = $("#btn-taller-sync");
    if (btnSync) btnSync.addEventListener("click", async () => {
      try {
        setStatus("Actualizando índices de taller…", "ok");
        const res = await fetchJSON("/api/taller/sync", { method: "POST" });
        const ambito = $("#taller-filter-ambito");
        if (ambito) ambito.value = "red";
        await loadTallerProyectos();
        setStatus("Red taller: " + (res.merged || 0) + " fichas · " + (res.ok_count || 0) + "/" + (res.tried || 0) + " peers", "ok");
      } catch (e) { setStatus(e.message, "err"); }
    });
    const btnMis = $("#btn-taller-mis-claims");
    if (btnMis) btnMis.addEventListener("click", () => {
      showTallerMisClaimsGlobal().catch((e) => setStatus(e.message, "err"));
    });
    const btnBackRemoto = $("#btn-taller-back-remoto");
    if (btnBackRemoto) btnBackRemoto.addEventListener("click", () => {
      currentTallerRemoto = null;
      currentTallerRemotoCompleteId = null;
      currentTallerRemotoJobId = null;
      showTallerStep("list");
      loadTallerProyectos().catch((e) => setStatus(e.message, "err"));
    });
    const btnEntregar = $("#btn-taller-remoto-entregar");
    if (btnEntregar) btnEntregar.addEventListener("click", () => {
      tallerRemotoComplete().catch((e) => {
        const fb = $("#taller-remoto-feedback");
        if (fb) fb.textContent = e.message;
        setStatus(e.message, "err");
      });
    });

    const btnEstado = $("#btn-taller-guardar-estado");
    if (btnEstado) btnEstado.addEventListener("click", async () => {
      if (!currentTallerProyectoId) return;
      try {
        await fetchJSON("/api/taller/proyectos/" + encodeURIComponent(currentTallerProyectoId), {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ estado: ($("#taller-detail-estado") || {}).value || "abierto" }),
        });
        await openTallerDetalle(currentTallerProyectoId);
        setStatus("Estado guardado", "ok");
      } catch (e) { setStatus(e.message, "err"); }
    });
    const btnTarea = $("#btn-taller-add-tarea");
    if (btnTarea) btnTarea.addEventListener("click", async () => {
      if (!currentTallerProyectoId) return;
      const fb = $("#taller-detail-feedback");
      try {
        await fetchJSON("/api/taller/proyectos/" + encodeURIComponent(currentTallerProyectoId) + "/tareas", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            titulo: ($("#taller-tarea-titulo") || {}).value || "",
            notas: ($("#taller-tarea-notas") || {}).value || "",
          }),
        });
        if ($("#taller-tarea-titulo")) $("#taller-tarea-titulo").value = "";
        if ($("#taller-tarea-notas")) $("#taller-tarea-notas").value = "";
        await openTallerDetalle(currentTallerProyectoId);
        if (fb) fb.textContent = "Tarea añadida";
        setStatus("Tarea añadida", "ok");
      } catch (e) {
        if (fb) fb.textContent = e.message;
        setStatus(e.message, "err");
      }
    });
    const btnAporte = $("#btn-taller-add-aporte");
    if (btnAporte) btnAporte.addEventListener("click", async () => {
      if (!currentTallerProyectoId) return;
      const fb = $("#taller-detail-feedback");
      try {
        await fetchJSON("/api/taller/proyectos/" + encodeURIComponent(currentTallerProyectoId) + "/aportes", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            titulo: ($("#taller-aporte-titulo") || {}).value || "",
            notas: ($("#taller-aporte-notas") || {}).value || "",
            file_id: ($("#taller-aporte-file") || {}).value || "",
            pucela_id: ($("#taller-aporte-pucela") || {}).value || "",
            user_id: me.user_id || "",
          }),
        });
        for (const id of ["taller-aporte-titulo", "taller-aporte-notas", "taller-aporte-file", "taller-aporte-pucela"]) {
          if ($("#" + id)) $("#" + id).value = "";
        }
        await openTallerDetalle(currentTallerProyectoId);
        if (fb) fb.textContent = "Aporte compartido";
        setStatus("Aporte compartido", "ok");
      } catch (e) {
        if (fb) fb.textContent = e.message;
        setStatus(e.message, "err");
      }
    });

    const btnAddJob = $("#btn-taller-add-job");
    if (btnAddJob) btnAddJob.addEventListener("click", () => {
      tallerAddJob().catch((e) => setStatus(e.message, "err"));
    });
    const btnMisLeases = $("#btn-taller-mis-leases");
    if (btnMisLeases) btnMisLeases.addEventListener("click", () => {
      showTallerMisLeasesGlobal().catch((e) => setStatus(e.message, "err"));
    });
    const btnJobEntregar = $("#btn-taller-remoto-job-entregar");
    if (btnJobEntregar) btnJobEntregar.addEventListener("click", () => {
      tallerRemotoColaComplete().catch((e) => setStatus(e.message, "err"));
    });
    const btnJobFail = $("#btn-taller-remoto-job-fail");
    if (btnJobFail) btnJobFail.addEventListener("click", () => {
      tallerRemotoColaFail().catch((e) => setStatus(e.message, "err"));
    });

  }


  async function setupMostrador(page, p) {
    const box = $("#place-mostrador");
    if (!box) return;
    const slot = page.mostrador;
    currentMostradorTicket = null;
    currentMostradorPlace = null;
    mostradorCatalog = [];
    if (!slot || !slot.enabled) {
      box.classList.add("hidden");
      return;
    }
    currentMostradorPlace = p.id;
    $("#mostrador-title").textContent = slot.label || "Mostrador de gestiones";
    $("#mostrador-note").textContent = slot.note || "Cola local · trámites stub · sin nube";
    box.classList.remove("hidden");
    showMostradorStep("catalog");
    $("#mostrador-form-feedback").textContent = "";
    $("#mostrador-ticket-feedback").textContent = "";
    try {
      const cat = await fetchJSON(slot.catalog_path || `/api/mostrador/catalog?place_id=${encodeURIComponent(p.id)}`);
      mostradorCatalog = cat.tramites || [];
      renderMostradorCatalog(mostradorCatalog);
      await refreshMostradorQueue(p.id);
    } catch (err) {
      $("#mostrador-tramites").innerHTML = "";
      const empty = $("#mostrador-catalog-empty");
      empty.textContent = err.message || "No se pudo cargar el mostrador.";
      empty.classList.remove("hidden");
    }
  }

  function showMostradorStep(name) {
    ["catalog", "form", "ticket"].forEach((n) => {
      const el = $("#mostrador-step-" + n);
      if (el) el.classList.toggle("hidden", n !== name);
    });
  }

  function renderMostradorCatalog(list) {
    const ul = $("#mostrador-tramites");
    const empty = $("#mostrador-catalog-empty");
    ul.innerHTML = "";
    if (!list.length) {
      empty.classList.remove("hidden");
      return;
    }
    empty.classList.add("hidden");
    for (const tr of list) {
      const li = document.createElement("li");
      li.setAttribute("role", "button");
      li.tabIndex = 0;
      li.innerHTML =
        (tr.stub ? `<span class="chip-stub">stub</span>` : "") +
        `<strong>${escapeHTML(tr.title || tr.id)}</strong>` +
        `<span>${escapeHTML(tr.summary || "")}</span>`;
      const open = () => openMostradorForm(tr);
      li.addEventListener("click", open);
      li.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(); }
      });
      ul.appendChild(li);
    }
  }

  function openMostradorForm(tr) {
    showMostradorStep("form");
    $("#mostrador-form-title").textContent = tr.title || "Trámite";
    $("#mostrador-form-summary").textContent = tr.summary || "";
    $("#mostrador-form-feedback").textContent = "";
    const form = $("#mostrador-form");
    form.innerHTML = "";
    form.dataset.tramiteId = tr.id;
    for (const f of tr.fields || []) {
      const label = document.createElement("label");
      label.className = "field";
      const span = document.createElement("span");
      span.textContent = f.label + (f.required ? " *" : "");
      label.appendChild(span);
      let input;
      if (f.kind === "note") {
        input = document.createElement("textarea");
        input.rows = 3;
        input.maxLength = 2000;
      } else {
        input = document.createElement("input");
        input.type = "text";
        input.maxLength = 500;
      }
      input.id = "mostrador-field-" + f.id;
      input.dataset.fieldId = f.id;
      input.required = !!f.required;
      if (f.hint) input.placeholder = f.hint;
      input.autocomplete = "off";
      label.appendChild(input);
      form.appendChild(label);
    }
    const tips = $("#mostrador-form-tips");
    tips.innerHTML = "";
    for (const tip of tr.tips || []) {
      const li = document.createElement("li");
      li.textContent = tip;
      tips.appendChild(li);
    }
  }

  async function submitMostradorForm() {
    const form = $("#mostrador-form");
    const tramiteId = form.dataset.tramiteId;
    const placeId = currentMostradorPlace;
    if (!tramiteId || !placeId) return;
    const fields = {};
    form.querySelectorAll("[data-field-id]").forEach((el) => {
      fields[el.dataset.fieldId] = (el.value || "").trim();
    });
    const fb = $("#mostrador-form-feedback");
    fb.textContent = "Sacando ticket…";
    try {
      const data = await fetchJSON("/api/mostrador/solicitudes", {
        method: "POST",
        body: JSON.stringify({ place_id: placeId, tramite_id: tramiteId, fields }),
      });
      currentMostradorTicket = data.solicitud || null;
      showMostradorTicket(currentMostradorTicket);
      await refreshMostradorQueue(placeId);
      fb.textContent = "";
    } catch (err) {
      fb.textContent = err.message || "No se pudo crear la solicitud.";
    }
  }

  function showMostradorTicket(sol) {
    if (!sol) return;
    showMostradorStep("ticket");
    $("#mostrador-ticket-id").textContent = sol.ticket || "";
    $("#mostrador-ticket-title").textContent = sol.title || "";
    $("#mostrador-ticket-status").textContent = sol.status_label || sol.status || "";
    $("#mostrador-ticket-note").textContent = sol.note || "";
    $("#mostrador-ticket-feedback").textContent = "";
    currentMostradorTicket = sol;
  }

  async function refreshMostradorQueue(placeId) {
    const ul = $("#mostrador-solicitudes");
    const empty = $("#mostrador-queue-empty");
    if (!ul || !empty) return;
    ul.innerHTML = "";
    try {
      const data = await fetchJSON(`/api/mostrador/solicitudes?place_id=${encodeURIComponent(placeId)}`);
      const list = data.solicitudes || [];
      if (!list.length) {
        empty.classList.remove("hidden");
        empty.textContent = data.empty_hint || "Aún no hay solicitudes. Elige un trámite arriba.";
        return;
      }
      empty.classList.add("hidden");
      for (const sol of list) {
        const li = document.createElement("li");
        li.className = "solicitud-row";
        li.tabIndex = 0;
        li.setAttribute("role", "button");
        li.innerHTML =
          `<span class="sol-ticket">${escapeHTML(sol.ticket || "")}</span>` +
          `<span class="sol-meta">${escapeHTML(sol.title || "")} · ${escapeHTML(sol.status_label || sol.status || "")}</span>`;
        const open = () => showMostradorTicket(sol);
        li.addEventListener("click", open);
        li.addEventListener("keydown", (ev) => {
          if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(); }
        });
        ul.appendChild(li);
      }
    } catch (_) {
      empty.classList.remove("hidden");
      empty.textContent = "No se pudo cargar la cola local.";
    }
  }

  async function exportMostradorRecibo() {
    if (!currentMostradorTicket || !currentMostradorTicket.id) return;
    const fb = $("#mostrador-ticket-feedback");
    fb.textContent = "Sellando recibo .pucela…";
    try {
      const data = await fetchJSON(`/api/mostrador/solicitudes/${encodeURIComponent(currentMostradorTicket.id)}/recibo`, {
        method: "POST",
        body: "{}",
      });
      fb.textContent = data.note || ("Recibo guardado: " + (data.pucela_id || ""));
      if (data.pucela_id) currentMostradorTicket.pucela_id = data.pucela_id;
    } catch (err) {
      fb.textContent = err.message || "No se pudo exportar el recibo.";
    }
  }

  function activateTab(name) {
    document.querySelectorAll("#place-tabs .tab").forEach((t) => {
      t.classList.toggle("active", t.dataset.tab === name);
    });
    ["info", "avisos", "contacto", "servicios"].forEach((n) => {
      const panel = $("#tab-" + n);
      if (panel) panel.classList.toggle("hidden", n !== name);
    });
  }

  document.querySelectorAll(".tab").forEach((t) => {
    t.addEventListener("click", () => activateTab(t.dataset.tab));
  });

  const btnMostradorBack = $("#btn-mostrador-back-catalog");
  if (btnMostradorBack) {
    btnMostradorBack.addEventListener("click", () => {
      showMostradorStep("catalog");
      $("#mostrador-form-feedback").textContent = "";
    });
  }
  const btnMostradorSubmit = $("#btn-mostrador-submit");
  if (btnMostradorSubmit) {
    btnMostradorSubmit.addEventListener("click", () => submitMostradorForm().catch(() => {}));
  }
  const btnMostradorOtra = $("#btn-mostrador-otra");
  if (btnMostradorOtra) {
    btnMostradorOtra.addEventListener("click", () => {
      currentMostradorTicket = null;
      showMostradorStep("catalog");
    });
  }
  const btnMostradorRecibo = $("#btn-mostrador-recibo");
  if (btnMostradorRecibo) {
    btnMostradorRecibo.addEventListener("click", () => exportMostradorRecibo().catch(() => {}));
  }


  document.querySelectorAll(".nav-btn").forEach((b) => {
    b.addEventListener("click", () => {
      if (b.dataset.nav === "lugares") {
        showHome();
        history.pushState({ view: "home" }, "", "/");
        loadPlaces(search.value.trim()).catch(() => {});
      } else if (b.dataset.nav === "mensajes") {
        showMessages();
      } else if (b.dataset.nav === "archivos") {
        showFiles();
      } else if (b.dataset.nav === "envios") {
        showEnvios();
      } else if (b.dataset.nav === "casa") {
        showCasa();
      } else if (b.dataset.nav === "pucela") {
        showPucela();
      } else if (b.dataset.nav === "federacion") {
        showFederacion();
      }
    });
  });



  const btnFedSync = $("#btn-fed-sync");
  if (btnFedSync) {
    btnFedSync.addEventListener("click", async () => {
      const fb = $("#fed-sync-feedback");
      try {
        btnFedSync.disabled = true;
        fb.textContent = "Sincronizando…";
        const data = await fetchJSON("/api/federacion/sync", { method: "POST", body: "{}" });
        const n = (data.results || []).length;
        const ok = (data.results || []).filter((r) => r.ok).length;
        let fetched = 0;
        for (const r of data.results || []) fetched += (r.prensa_fetched || []).length;
        fb.textContent = `Listo: ${ok}/${n} peers OK` + (fetched ? ` · ${fetched} edición(es) .pucela` : "") + ".";
        await loadFederacion();
        setStatus("Federación sincronizada", "ok");
      } catch (e) {
        fb.textContent = "Error: " + e.message;
        setStatus(e.message, "err");
      } finally {
        btnFedSync.disabled = false;
      }
    });
  }
  const btnFedSyncPrensa = $("#btn-fed-sync-prensa");
  if (btnFedSyncPrensa) {
    btnFedSyncPrensa.addEventListener("click", async () => {
      const fb = $("#fed-sync-feedback");
      try {
        btnFedSyncPrensa.disabled = true;
        fb.textContent = "Sincronizando prensa…";
        const data = await fetchJSON("/api/federacion/sync/prensa", { method: "POST", body: "{}" });
        let fetched = 0, skipped = 0;
        for (const r of data.results || []) {
          fetched += (r.prensa_fetched || []).length;
          skipped += (r.prensa_skipped || []).length;
        }
        fb.textContent = `Prensa: ${fetched} traída(s)` + (skipped ? `, ${skipped} omitida(s)` : "") + ".";
        await loadFederacion();
        setStatus("Prensa federada sincronizada", "ok");
      } catch (e) {
        fb.textContent = "Error: " + e.message;
        setStatus(e.message, "err");
      } finally {
        btnFedSyncPrensa.disabled = false;
      }
    });
  }
  const btnFedAdd = $("#btn-fed-add-peer");
  if (btnFedAdd) {
    btnFedAdd.addEventListener("click", async () => {
      const url = ($("#fed-peer-url").value || "").trim();
      const fb = $("#fed-peer-feedback");
      if (!url) { fb.textContent = "Indica la URL del peer."; return; }
      try {
        btnFedAdd.disabled = true;
        await fetchJSON("/api/federacion/peers", { method: "POST", body: JSON.stringify({ peer_url: url }) });
        $("#fed-peer-url").value = "";
        fb.textContent = "Peer añadido a la allowlist.";
        await loadFederacion();
      } catch (e) { fb.textContent = "Error: " + e.message; }
      finally { btnFedAdd.disabled = false; }
    });
  }
  const btnFedAviso = $("#btn-fed-aviso");
  if (btnFedAviso) {
    btnFedAviso.addEventListener("click", async () => {
      const titleEl = $("#fed-aviso-title");
      const bodyEl = $("#fed-aviso-body");
      const sev = $("#fed-aviso-severity");
      const fb = $("#fed-aviso-feedback");
      try {
        btnFedAviso.disabled = true;
        await fetchJSON("/api/federacion/avisos", {
          method: "POST",
          body: JSON.stringify({
            title: (titleEl.value || "").trim(),
            body: (bodyEl.value || "").trim(),
            severity: sev.value,
          }),
        });
        titleEl.value = "";
        bodyEl.value = "";
        fb.textContent = "Aviso listo para federar.";
        await loadFederacion();
        setStatus("Aviso federado publicado", "ok");
      } catch (e) { fb.textContent = "Error: " + e.message; }
      finally { btnFedAviso.disabled = false; }
    });
  }

  function bindPrivacyControls(prefix) {
    const els = privacyEls(prefix);
    if (els.zone) {
      els.zone.addEventListener("change", () => savePresence(null, prefix));
    }
    if (els.ttl) {
      els.ttl.addEventListener("change", () => savePresence("precisa_temporal", prefix));
    }
    if (els.rotate) {
      els.rotate.addEventListener("click", () => rotatePresence(prefix));
    }
  }
  bindPrivacyControls("#privacy");
  bindPrivacyControls("#casa-privacy");

  // v4.8–5.0: puerta, estancias, salón, huerto, cocina, despensa, chimenea, ventanas
  (function bindCasaBolsonUI() {
    const puertaBtn = $("#btn-casa-puerta");
    const puertaTog = $("#btn-casa-puerta-toggle");
    if (puertaBtn) puertaBtn.addEventListener("click", toggleCasaPuerta);
    if (puertaTog) puertaTog.addEventListener("click", toggleCasaPuerta);
    document.querySelectorAll(".casa-estancia-tab").forEach((tab) => {
      tab.addEventListener("click", () => {
        setCasaEstancia(tab.dataset.estancia);
        if (tab.dataset.estancia === "huerto") renderHuerto();
        if (tab.dataset.estancia === "despensa") renderDespensa();
        if (tab.dataset.estancia === "cocina") renderCocina();
        if (tab.dataset.estancia === "salon") renderComidaStatus();
      });
    });
    const btnSalon = $("#btn-casa-salon-guardar");
    if (btnSalon) btnSalon.addEventListener("click", saveCasaSalonPrefs);
    const btnDespensa = $("#btn-casa-despensa-archivos");
    if (btnDespensa) {
      btnDespensa.addEventListener("click", () => {
        showFiles();
        setStatus("Despensa → Archivos ligeros", "ok");
      });
    }
    const btnChim = $("#btn-casa-chimenea");
    if (btnChim) btnChim.addEventListener("click", toggleChimenea);
    const btnHuertoTick = $("#btn-casa-huerto-tick");
    if (btnHuertoTick) btnHuertoTick.addEventListener("click", () => huertoTick(true));
    initCasaBolsonPrefs();
  })();

  $("#btn-rotar").addEventListener("click", async () => {
    const fb = $("#casa-rotate-feedback");
    try {
      $("#btn-rotar").disabled = true;
      const data = await fetchJSON("/api/casa/rotar", { method: "POST", body: "{}" });
      fb.textContent = "Nueva dirección generada.";
      await loadCasa();
      setStatus("Dirección rotada", "ok");
      void data;
    } catch (e) {
      fb.textContent = "Error: " + e.message;
    } finally {
      $("#btn-rotar").disabled = false;
    }
  });

  $("#btn-timbre-remote").addEventListener("click", async () => {
    const url = $("#timbre-peer-url").value.trim();
    const msg = $("#timbre-message").value.trim();
    const fb = $("#timbre-remote-feedback");
    const reveal = $("#timbre-reveal");
    reveal.classList.add("hidden");
    if (!url) {
      fb.textContent = "Indica la URL del nodo.";
      return;
    }
    try {
      $("#btn-timbre-remote").disabled = true;
      fb.textContent = "Tocando timbre…";
      const data = await fetchJSON("/api/casa/timbre", {
        method: "POST",
        body: JSON.stringify({
          peer_url: url,
          from_user_id: me.user_id,
          message: msg,
        }),
      });
      const rid = data.request && data.request.id;
      lastRemoteTimbreId = rid;
      fb.textContent = "Solicitud enviada (" + (rid ? shortId(rid) : "?") + "). Esperando aceptación…";
      if (rid) {
        // Poll reveal on remote via local proxy: GET on remote not available through us;
        // visitor polls the peer's reveal endpoint directly.
        pollTimbreReveal(url, rid);
      }
    } catch (e) {
      fb.textContent = "Error: " + e.message;
    } finally {
      $("#btn-timbre-remote").disabled = false;
    }
  });

  async function pollTimbreReveal(peerBase, requestId) {
    const reveal = $("#timbre-reveal");
    const fb = $("#timbre-remote-feedback");
    peerBase = peerBase.replace(/\/$/, "");
    for (let i = 0; i < 40; i++) {
      await new Promise((r) => setTimeout(r, 2000));
      try {
        const res = await fetch(
          peerBase + "/api/casa/timbre/" + encodeURIComponent(requestId) +
            "?from=" + encodeURIComponent(me.user_id)
        );
        if (!res.ok) continue;
        const v = await res.json();
        if (v.status === "rechazada") {
          fb.textContent = "Rechazada — sin acceso.";
          reveal.classList.add("hidden");
          return;
        }
        if (v.status === "aceptada" && v.bound_address) {
          fb.textContent = "Aceptada.";
          reveal.classList.remove("hidden");
          reveal.innerHTML =
            "<strong>Dirección efímera:</strong> <code>" +
            escapeHTML(v.bound_address) +
            "</code>" +
            (v.can_enter ? " · usable ahora" : " · ya no es la dirección actual");
          return;
        }
      } catch (_) {}
    }
    fb.textContent = (fb.textContent || "") + " (sigue pendiente; revisa más tarde)";
  }

  async function bindAlarmToggle(sel, kind, getId) {
    const el = $(sel);
    if (!el) return;
    el.addEventListener("change", async (ev) => {
      const armed = ev.target.checked;
      try {
        await ensureAlarmKind(kind, armed, getId());
        setStatus(armed ? ("Alarma «" + kind + "» armada") : ("Alarma «" + kind + "» desarmada"), "ok");
      } catch (e) {
        setStatus("Alarma: " + e.message, "err");
        ev.target.checked = !armed;
      }
    });
  }
  bindAlarmToggle("#alarm-rechazos-toggle", "rechazos", () => rechazosAlarmId);
  bindAlarmToggle("#alarm-timbre-toggle", "timbre", () => timbreAlarmId);
  bindAlarmToggle("#alarm-rechazo-toggle", "rechazo", () => rechazoAlarmId);

  $("#btn-alarm-contact").addEventListener("click", async () => {
    const uid = $("#alarm-contact-id").value.trim();
    if (!uid) {
      setStatus("Indica un user_id", "err");
      return;
    }
    try {
      await fetchJSON("/api/casa/alarmas", {
        method: "POST",
        body: JSON.stringify({ kind: "contacto", contact_user_id: uid, armed: true }),
      });
      $("#alarm-contact-id").value = "";
      await loadAlarms();
      setStatus("Alarma de contacto armada", "ok");
    } catch (e) {
      setStatus("Alarma: " + e.message, "err");
    }
  });

  $("#btn-send-file").addEventListener("click", async () => {
    const to = $("#file-contact").value;
    const input = $("#file-input");
    const fb = $("#file-send-feedback");
    if (!to) {
      fb.textContent = "Elige un contacto.";
      return;
    }
    if (!input.files || !input.files[0]) {
      fb.textContent = "Elige un fichero.";
      return;
    }
    const file = input.files[0];
    const max = 8 * 1024 * 1024;
    if (file.size > max) {
      fb.textContent = "Demasiado grande (máx. 8 MiB).";
      return;
    }
    const fd = new FormData();
    fd.append("to", to);
    fd.append("file", file, file.name);
    try {
      $("#btn-send-file").disabled = true;
      fb.textContent = "Cifrando y enviando…";
      const res = await fetch("/api/files/send", { method: "POST", body: fd });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.error || "HTTP " + res.status);
      fb.textContent = data.delivered
        ? "Entregado: " + (data.file && data.file.name ? data.file.name : file.name)
        : "Guardado para reintento (peer no alcanzable).";
      input.value = "";
      await loadFilesList();
    } catch (e) {
      fb.textContent = "Error: " + e.message;
    } finally {
      $("#btn-send-file").disabled = false;
    }
  });

  btnBack.addEventListener("click", () => {
    if (currentPeer) {
      showMessages();
      return;
    }
    if (viewNodo && !viewNodo.classList.contains("hidden")) {
      showHome();
      history.pushState({ view: "home" }, "", "/");
      return;
    }
    const iframe = $("#tool-iframe");
    const onAsistente = viewToolAsistente && !viewToolAsistente.classList.contains("hidden");
    const onTool = viewToolFrame && !viewToolFrame.classList.contains("hidden")
      || viewToolWiki && !viewToolWiki.classList.contains("hidden")
      || viewTool3d && !viewTool3d.classList.contains("hidden");
    if (onAsistente && asistenteReturn) {
      const r = asistenteReturn;
      if (r.type === "shop" && r.id) { openShop(r.id).catch(() => showHome()); return; }
      if (r.type === "persona" && r.id) { openPersona(r.id).catch(() => showHome()); return; }
      if (r.type === "place" && r.id) { openPlace(r.id).catch(() => showHome()); return; }
    }
    if (onTool || onAsistente) {
      if (iframe) iframe.src = "about:blank";
      const place = toolReturnPlace || (asistenteReturn && asistenteReturn.id) || "herramientas";
      openPlace(place).catch(() => showHome());
      return;
    }
    if (viewShop && !viewShop.classList.contains("hidden") && currentShop && currentShop.parent_id) {
      openPlace(currentShop.parent_id).catch(() => showHome());
      return;
    }
    if (viewPersona && !viewPersona.classList.contains("hidden")) {
      openPlace("personas").catch(() => showHome());
      return;
    }
    if (viewPrensa && !viewPrensa.classList.contains("hidden")) {
      openPlace("prensa").catch(() => showHome());
      return;
    }
    showHome();
    history.pushState({ view: "home" }, "", "/");
  });

  $("#btn-add-contact").addEventListener("click", async () => {
    const url = $("#contact-peer-url").value.trim();
    const name = $("#contact-name").value.trim();
    const fb = $("#contact-feedback");
    if (!url) {
      fb.textContent = "Indica la URL del nodo peer.";
      return;
    }
    try {
      $("#btn-add-contact").disabled = true;
      const data = await fetchJSON("/api/contacts", {
        method: "POST",
        body: JSON.stringify({ peer_url: url, display_name: name }),
      });
      fb.textContent = "Contacto " + shortId(data.contact.user_id) + " registrado.";
      $("#contact-peer-url").value = "";
      await Promise.all([loadThreads(), loadContacts()]);
      // Open thread with new contact
      if (data.contact && data.contact.user_id) {
        await openThread(data.contact.user_id, data.contact.display_name || name || shortId(data.contact.user_id));
      }
    } catch (e) {
      fb.textContent = "Error: " + e.message;
    } finally {
      $("#btn-add-contact").disabled = false;
    }
  });

  compose.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    if (!currentPeer) return;
    const body = composeBody.value.trim();
    if (!body) return;
    try {
      compose.querySelector("button").disabled = true;
      const sent = await fetchJSON("/api/chat/send", {
        method: "POST",
        body: JSON.stringify({ to: currentPeer, body }),
      });
      composeBody.value = "";
      await refreshThread();
      if (sent.pending) {
        const q = sent.reach_quality === "caducada" || sent.tip_stale
          ? "Pista caducada — en bandeja de salida."
          : "Peer no alcanzable — en bandeja de salida.";
        setStatus(q, "err");
      } else if (sent.delivered) {
        setStatus("Entregado", "ok");
      }
    } catch (e) {
      setStatus("No se pudo enviar: " + e.message, "err");
    } finally {
      compose.querySelector("button").disabled = false;
      composeBody.focus();
    }
  });


  const btnPucelaCreate = $("#btn-pucela-create");
  if (btnPucelaCreate) {
    btnPucelaCreate.addEventListener("click", async () => {
      const fb = $("#pucela-create-feedback");
      const titleEl = $("#pucela-title");
      const textEl = $("#pucela-text");
      const imgEl = $("#pucela-image");
      const soundEl = $("#pucela-sound");
      const fd = new FormData();
      fd.append("title", (titleEl && titleEl.value) || "");
      fd.append("text", (textEl && textEl.value) || "");
      if (imgEl && imgEl.files && imgEl.files[0]) {
        fd.append("image", imgEl.files[0]);
      }
      if (soundEl && soundEl.files && soundEl.files[0]) {
        fd.append("sound", soundEl.files[0]);
      }
      try {
        btnPucelaCreate.disabled = true;
        fb.textContent = "Creando y sellando…";
        const res = await fetch("/api/pucela", { method: "POST", body: fd });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "HTTP " + res.status);
        let msg = "Creado: " + (data.document && data.document.id ? data.document.id.slice(0, 8) + "…" : "ok");
        if (data.fitted) msg += " · imagen ajustada automáticamente";
        fb.textContent = msg;
        if (textEl) textEl.value = "";
        if (titleEl) titleEl.value = "";
        if (imgEl) imgEl.value = "";
        if (soundEl) soundEl.value = "";
        await loadPucelaList();
        setStatus("Documento .pucela sellado", "ok");
      } catch (e) {
        fb.textContent = "Error: " + e.message;
        setStatus("Error pucela: " + e.message, "err");
      } finally {
        btnPucelaCreate.disabled = false;
      }
    });
  }

  const btnPucelaClose = $("#btn-pucela-close");
  if (btnPucelaClose) {
    btnPucelaClose.addEventListener("click", () => {
      const card = $("#pucela-open-card");
      if (card) card.classList.add("hidden");
    });
  }


  const btnHojaPrev = $("#btn-hoja-prev");
  const btnHojaNext = $("#btn-hoja-next");
  if (btnHojaPrev) btnHojaPrev.addEventListener("click", () => flipHoja(-1));
  if (btnHojaNext) btnHojaNext.addEventListener("click", () => flipHoja(1));
  const hojaStage = $("#hoja-stage");
  if (hojaStage) {
    let touchX = null;
    hojaStage.addEventListener("keydown", (ev) => {
      if (ev.key === "ArrowLeft") flipHoja(-1);
      if (ev.key === "ArrowRight") flipHoja(1);
    });
    hojaStage.addEventListener("touchstart", (ev) => {
      if (ev.changedTouches && ev.changedTouches[0]) touchX = ev.changedTouches[0].clientX;
    }, { passive: true });
    hojaStage.addEventListener("touchend", (ev) => {
      if (touchX == null || !ev.changedTouches || !ev.changedTouches[0]) return;
      const dx = ev.changedTouches[0].clientX - touchX;
      touchX = null;
      if (Math.abs(dx) < 40) return;
      if (dx < 0) flipHoja(1);
      else flipHoja(-1);
    }, { passive: true });
  }
  const btnPrensaPub = $("#btn-prensa-publish");
  if (btnPrensaPub) {
    btnPrensaPub.addEventListener("click", async () => {
      const titleEl = $("#prensa-title");
      const textEl = $("#prensa-text");
      const fb = $("#prensa-publish-feedback");
      const titleV = (titleEl && titleEl.value || "").trim();
      const textV = (textEl && textEl.value || "").trim();
      if (!titleV || !textV) {
        if (fb) fb.textContent = "Indica título y al menos una hoja de texto.";
        return;
      }
      try {
        btnPrensaPub.disabled = true;
        if (fb) fb.textContent = "Sellando edición .pucela…";
        const data = await fetchJSON("/api/prensa", {
          method: "POST",
          body: JSON.stringify({ title: titleV, text: textV }),
        });
        if (fb) fb.textContent = "Publicada: " + ((data.edition && data.edition.title) || titleV);
        if (titleEl) titleEl.value = "";
        if (textEl) textEl.value = "";
        await openPlace("prensa");
        if (data.edition && data.edition.id) {
          await openEdition(data.edition.id);
        }
      } catch (e) {
        if (fb) fb.textContent = "Error: " + e.message;
      } finally {
        btnPrensaPub.disabled = false;
      }
    });
  }

  let searchTimer = null;
  search.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      loadPlaces(search.value.trim()).catch((e) =>
        setStatus("Error al buscar: " + e.message, "err")
      );
    }, 180);
  });

  window.addEventListener("popstate", (ev) => {
    const st = ev.state;
    if (st && st.view === "place" && st.id) {
      openPlace(st.id).catch(() => showHome());
    } else if (st && st.view === "shop" && st.id) {
      openShop(st.id).catch(() => showHome());
    } else if (st && st.view === "persona" && st.id) {
      openPersona(st.id).catch(() => showHome());
    } else if (st && st.view === "mensajes") {
      showMessages();
    } else if (st && st.view === "archivos") {
      showFiles();
    } else if (st && st.view === "envios") {
      showEnvios();
    } else if (st && st.view === "casa") {
      showCasa();
    } else if (st && st.view === "pucela") {
      showPucela();
    } else if (st && st.view === "federacion") {
      showFederacion();
    } else if (st && st.view === "nodo") {
      showNodoPanel();
    } else if (st && st.view === "sellos") {
      showSellos().catch(() => showHome());
    } else if (st && st.view === "misiones") {
      showMisiones().catch(() => showHome());
    } else if (st && st.view === "novedades") {
      showNovedades();
    } else if (st && st.view === "prensa" && st.id) {
      openEdition(st.id).catch(() => openPlace("prensa"));
    } else if (st && st.view === "thread" && st.peer) {
      openThread(st.peer, st.name).catch(() => showMessages());
    } else if (st && (st.view === "tool" || st.view === "tool-wiki" || st.view === "tool-3d" || st.view === "tool-asistente")) {
      const place = st.place || "herramientas";
      openPlace(place).then(() => {
        // re-open tool if id known
        if (st.tool) {
          fetchJSON("/api/herramientas").then((data) => {
            const tool = (data.tools || []).find((x) => x.id === st.tool);
            if (tool) openTool(tool, place);
          }).catch(() => {});
        }
      }).catch(() => showHome());
    } else {
      showHome();
    }
  });


  const btnDepRes = $("#btn-dep-reservar");
  if (btnDepRes) {
    btnDepRes.addEventListener("click", async () => {
      const fb = $("#dep-reservar-feedback");
      const name = ($("#dep-name").value || "").trim();
      const mib = parseFloat($("#dep-mib").value);
      const payload = {};
      if (name) payload.name = name;
      if (mib > 0) payload.max_bytes = Math.floor(mib * 1024 * 1024);
      try {
        btnDepRes.disabled = true;
        fb.textContent = "Reservando…";
        const data = await fetchJSON("/api/deposito/reservar", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        $("#dep-code-box").classList.remove("hidden");
        $("#dep-code-show").textContent = data.code;
        $("#dep-id-show").textContent = "ID: " + data.id + " · caduca " + new Date(data.expires * 1000).toLocaleString();
        $("#dep-upload-id").value = data.id;
        $("#dep-upload-code").value = data.code;
        $("#dep-redeem-id").value = data.id;
        $("#dep-redeem-code").value = data.code;
        fb.textContent = "Cita creada. Guarda el código.";
        setStatus("Cita reservada", "ok");
        await loadDeposito();
      } catch (e) {
        fb.textContent = "Error: " + e.message;
      } finally {
        btnDepRes.disabled = false;
      }
    });
  }

  const btnDepUp = $("#btn-dep-upload");
  if (btnDepUp) {
    btnDepUp.addEventListener("click", async () => {
      const fb = $("#dep-upload-feedback");
      const id = ($("#dep-upload-id").value || "").trim();
      const code = ($("#dep-upload-code").value || "").trim();
      const fileInput = $("#dep-file");
      if (!id || !code || !fileInput.files || !fileInput.files[0]) {
        fb.textContent = "Indica ID, código y fichero.";
        return;
      }
      const fd = new FormData();
      fd.append("code", code);
      fd.append("file", fileInput.files[0]);
      try {
        btnDepUp.disabled = true;
        fb.textContent = "Cifrando y subiendo…";
        const res = await fetch("/api/deposito/" + encodeURIComponent(id) + "/upload", {
          method: "POST",
          body: fd,
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.error || res.statusText);
        fb.textContent = "Depositado (" + ((data.deposit && data.deposit.size) || "?") + " B).";
        setStatus("Depósito listo", "ok");
        await loadDeposito();
      } catch (e) {
        fb.textContent = "Error: " + e.message;
      } finally {
        btnDepUp.disabled = false;
      }
    });
  }

  const btnDepRed = $("#btn-dep-redeem");
  if (btnDepRed) {
    btnDepRed.addEventListener("click", async () => {
      const fb = $("#dep-redeem-feedback");
      const id = ($("#dep-redeem-id").value || "").trim();
      const code = ($("#dep-redeem-code").value || "").trim();
      if (!id || !code) {
        fb.textContent = "Indica ID y código.";
        return;
      }
      try {
        btnDepRed.disabled = true;
        fb.textContent = "Canjeando…";
        const res = await fetch("/api/deposito/" + encodeURIComponent(id) + "/redeem", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code }),
        });
        if (!res.ok) {
          const data = await res.json().catch(() => ({}));
          throw new Error(data.error || res.statusText);
        }
        const blob = await res.blob();
        const cd = res.headers.get("Content-Disposition") || "";
        let fname = "deposito.bin";
        const m = /filename="([^"]+)"/.exec(cd);
        if (m) fname = m[1];
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = fname;
        document.body.appendChild(a);
        a.click();
        a.remove();
        fb.textContent = "Descargado y borrado del nodo.";
        setStatus("Canje OK · auto-borrado", "ok");
        await loadDeposito();
      } catch (e) {
        fb.textContent = "Error: " + e.message;
      } finally {
        btnDepRed.disabled = false;
      }
    });
  }

  const btnDepRef = $("#btn-dep-refresh");
  if (btnDepRef) {
    btnDepRef.addEventListener("click", async () => {
      try {
        await fetchJSON("/api/deposito/sweep", { method: "POST", body: "{}" });
        await loadDeposito();
        setStatus("Listado actualizado", "ok");
      } catch (e) {
        setStatus("Error: " + e.message, "err");
      }
    });
  }

  const btnPanelNodo = $("#btn-panel-nodo");
  if (btnPanelNodo) {
    btnPanelNodo.addEventListener("click", () => showNodoPanel());
  }
  const btnNodoRefresh = $("#btn-nodo-refresh");
  if (btnNodoRefresh) {
    btnNodoRefresh.addEventListener("click", async () => {
      const fb = $("#nodo-status-feedback");
      try {
        btnNodoRefresh.disabled = true;
        await loadNodoStatus();
        if (fb) fb.textContent = "Actualizado.";
        setStatus("Estado actualizado", "ok");
      } catch (e) {
        if (fb) fb.textContent = "Error: " + e.message;
        setStatus(e.message, "err");
      } finally {
        btnNodoRefresh.disabled = false;
      }
    });
  }
  const btnNodoBackup = $("#btn-nodo-backup");
  if (btnNodoBackup) {
    btnNodoBackup.addEventListener("click", async () => {
      const fb = $("#nodo-backup-feedback");
      try {
        btnNodoBackup.disabled = true;
        if (fb) fb.textContent = "Generando copia (incluye claves)…";
        const res = await fetch("/api/node/backup", { headers: operatorPinHeaders({ Accept: "application/gzip" }) });
        if (!res.ok) {
          let detail = "HTTP " + res.status;
          try { const j = await res.json(); if (j.error) detail = j.error; } catch (_) {}
          throw new Error(detail);
        }
        const blob = await res.blob();
        const cd = res.headers.get("Content-Disposition") || "";
        let fname = "valladolid-backup.tar.gz";
        const m = /filename="([^"]+)"/.exec(cd);
        if (m) fname = m[1];
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = fname;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(a.href);
        if (fb) fb.textContent = "Descargado: " + fname + " · guárdalo como secreto.";
        setStatus("Backup descargado", "ok");
      } catch (e) {
        if (fb) fb.textContent = "Error: " + e.message;
        setStatus(e.message, "err");
      } finally {
        btnNodoBackup.disabled = false;
      }
    });
  }
  const btnNodoRestore = $("#btn-nodo-restore");
  if (btnNodoRestore) {
    btnNodoRestore.addEventListener("click", async () => {
      const fb = $("#nodo-restore-feedback");
      const input = $("#nodo-restore-file");
      const conf = $("#nodo-restore-confirm");
      if (!input || !input.files || !input.files[0]) {
        if (fb) fb.textContent = "Elige un archivo .tar.gz o .zip.";
        return;
      }
      if (!conf || !conf.checked) {
        if (fb) fb.textContent = "Marca la casilla de confirmación REPLACE.";
        return;
      }
      if (!window.confirm("Esto SUSTITUYE todo el data-dir. ¿Continuar? Luego debes reiniciar el nodo.")) {
        return;
      }
      const fd = new FormData();
      fd.append("confirm", "REPLACE");
      fd.append("file", input.files[0], input.files[0].name);
      try {
        btnNodoRestore.disabled = true;
        if (fb) fb.textContent = "Restaurando… quieta el tráfico y reinicia después.";
        const res = await fetch("/api/node/restore", { method: "POST", headers: operatorPinHeaders(), body: fd });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.error || "HTTP " + res.status);
        if (fb) fb.textContent = (data.message || "OK") + " · reinicia el proceso del nodo.";
        setStatus("Restaurado · reinicio requerido", "ok");
        conf.checked = false;
        input.value = "";
      } catch (e) {
        if (fb) fb.textContent = "Error: " + e.message;
        setStatus(e.message, "err");
      } finally {
        btnNodoRestore.disabled = false;
      }
    });
  }


  /* --- Campana de avisos (v1.6) --- */
  let campanaPoll = null;

  function sourceLabel(src) {
    return ({
      casa_timbre: "Casa · timbre",
      casa_aviso: "Casa · alarma",
      federacion: "Federación",
      mostrador: "Mostrador",
    })[src] || src;
  }

  function updateCampanaBadge(unread) {
    const badge = $("#campana-badge");
    const btn = $("#btn-campana");
    if (!badge || !btn) return;
    const n = Number(unread) || 0;
    if (n > 0) {
      badge.textContent = n > 99 ? "99+" : String(n);
      badge.classList.remove("hidden");
      btn.classList.add("has-unread");
      btn.setAttribute("aria-label", `Campana de avisos · ${n} sin leer`);
    } else {
      badge.classList.add("hidden");
      btn.classList.remove("has-unread");
      btn.setAttribute("aria-label", "Campana de avisos");
    }
  }

  async function refreshCampanaBadge() {
    try {
      const snap = await fetchJSON("/api/campana");
      updateCampanaBadge(snap.unread);
      return snap;
    } catch (_) {
      return null;
    }
  }

  function openCampanaSheet() {
    const sheet = $("#campana-sheet");
    const btn = $("#btn-campana");
    if (!sheet) return;
    sheet.classList.remove("hidden");
    if (btn) btn.setAttribute("aria-expanded", "true");
    loadCampanaInbox().catch((e) => setStatus("Campana: " + e.message, "err"));
  }

  function closeCampanaSheet() {
    const sheet = $("#campana-sheet");
    const btn = $("#btn-campana");
    if (sheet) sheet.classList.add("hidden");
    if (btn) btn.setAttribute("aria-expanded", "false");
  }

  async function loadCampanaInbox() {
    const snap = await fetchJSON("/api/campana");
    updateCampanaBadge(snap.unread);
    const list = $("#campana-list");
    const emptyEl = $("#campana-empty");
    if (!list) return;
    list.innerHTML = "";
    const items = snap.items || [];
    if (!items.length) {
      if (emptyEl) emptyEl.classList.remove("hidden");
      return;
    }
    if (emptyEl) emptyEl.classList.add("hidden");
    for (const it of items) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "campana-item" + (it.unread ? " unread" : "");
      btn.setAttribute("role", "listitem");
      btn.dataset.nav = it.nav || "";
      btn.dataset.ref = it.ref || "";
      const meta = document.createElement("span");
      meta.className = "campana-item-meta";
      meta.textContent = sourceLabel(it.source) + (it.unread ? " · nuevo" : "");
      const title = document.createElement("span");
      title.className = "campana-item-title";
      title.textContent = it.title || "Aviso";
      btn.appendChild(meta);
      btn.appendChild(title);
      if (it.body) {
        const body = document.createElement("span");
        body.className = "campana-item-body";
        body.textContent = it.body;
        btn.appendChild(body);
      }
      btn.addEventListener("click", () => navigateCampanaItem(it));
      list.appendChild(btn);
    }
  }

  function navigateCampanaItem(it) {
    closeCampanaSheet();
    const nav = it && it.nav;
    if (nav === "casa") {
      showCasa();
    } else if (nav === "federacion") {
      showFederacion();
    } else if (nav === "mostrador") {
      const place = (it.ref || "ayuntamiento");
      openPlace(place).catch((e) => setStatus(e.message, "err"));
    } else {
      showHome();
    }
  }

  async function markCampanaRead() {
    const snap = await fetchJSON("/api/campana/leer", { method: "POST", body: "{}" });
    updateCampanaBadge(snap.unread);
    await loadCampanaInbox();
    setStatus("Avisos marcados como leídos", "ok");
  }

  function startCampanaPoll() {
    if (campanaPoll) return;
    campanaPoll = setInterval(() => {
      refreshCampanaBadge();
    }, 20000);
  }

  async function boot() {
    try {
      const health = await fetchJSON("/api/health");
      me.user_id = health.user_id || health.node_id;
      me.node_id = health.node_id;
      try {
        const who = await fetchJSON("/api/whoami");
        me.user_id = who.user_id;
        me.node_id = who.node_id;
      } catch (_) {}
      setStatus(
        `Nodo local · v${health.version} · ${String(me.user_id).slice(0, 8)}…`,
        "ok"
      );
      await loadPlaces("");
      loadCityEvents().catch(() => {});
      refreshStamps().catch(() => {});
      loadCityPois().catch(() => {});
      const path = location.pathname;
      const m = path.match(/^\/lugar\/([^/]+)\/?$/);
      const mShop = path.match(/^\/puesto\/([^/]+)\/?$/);
      const mPerson = path.match(/^\/persona\/([^/]+)\/?$/);
      const mPrensa = path.match(/^\/prensa\/([^/]+)\/?$/);
      if (m) {
        await openPlace(decodeURIComponent(m[1]));
      } else if (mShop) {
        await openShop(decodeURIComponent(mShop[1]));
      } else if (mPerson) {
        await openPersona(decodeURIComponent(mPerson[1]));
      } else if (mPrensa) {
        await openEdition(decodeURIComponent(mPrensa[1]));
      } else if (path.startsWith("/herramienta/")) {
        const tid = decodeURIComponent(path.replace(/^\/herramienta\//, "").replace(/\/$/, ""));
        await openPlace("herramientas");
        const data = await fetchJSON("/api/herramientas");
        const tool = (data.tools || []).find((x) => x.id === tid);
        if (tool) openTool(tool, "herramientas");
      } else if (path.startsWith("/mensajes")) {
        showMessages();
      } else if (path.startsWith("/archivos")) {
        showFiles();
      } else if (path.startsWith("/envios")) {
        showEnvios();
      } else if (path.startsWith("/casa")) {
        showCasa();
      } else if (path.startsWith("/pucela")) {
        showPucela();
      } else if (path.startsWith("/sellos")) {
        await showSellos();
      } else if (path.startsWith("/misiones")) {
        await showMisiones();
      } else if (path.startsWith("/novedades") || path.startsWith("/changelog")) {
        showNovedades();
      } else if (path.startsWith("/nodo") || path.startsWith("/panel")) {
        showNodoPanel();
      } else if (path.startsWith("/federacion")) {
        showFederacion();
      } else {
        history.replaceState({ view: "home" }, "", "/");
        showHome();
      }
      maybeShowOnboarding();
      refreshCampanaBadge().then(() => startCampanaPoll());
    } catch (e) {
      setStatus("Sin conexión al nodo local. ¿Está en marcha?", "err");
    }
  }

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/sw.js").catch(() => {});
    });
  }


  const btnN3d = $("#btn-n3d-preview");
  if (btnN3d) btnN3d.addEventListener("click", () => runN3dPreview());
  const formAsist = $("#asistente-form");
  if (formAsist) {
    formAsist.addEventListener("submit", (ev) => {
      ev.preventDefault();
      const q = $("#asistente-q").value.trim();
      if (!q) return;
      $("#asistente-q").value = "";
      askAsistente(q);
    });
  }
  const btnWikiClose = $("#btn-wiki-close");
  if (btnWikiClose) {
    btnWikiClose.addEventListener("click", () => {
      const card = $("#wiki-open-card");
      if (card) card.classList.add("hidden");
    });
  }


  const btnPlaceAsist = $("#btn-place-assistant");
  if (btnPlaceAsist) {
    btnPlaceAsist.addEventListener("click", () => {
      const box = $("#place-assistant");
      openLocalAsistente({
        label: $("#place-assistant-label").textContent || "Asistente del lugar",
        ask: box.dataset.ask,
        faq: box.dataset.faq,
        path: "/asistente/lugar",
        returnTo: { type: "place", id: currentPlace && currentPlace.id },
        hello: "Asistente local del lugar. Si no sé, pregunta en el mostrador.",
      });
    });
  }
  const btnShopAsist = $("#btn-shop-assistant");
  if (btnShopAsist) {
    btnShopAsist.addEventListener("click", () => {
      const box = $("#shop-assistant");
      openLocalAsistente({
        label: $("#shop-assistant-label").textContent || "Asistente del puesto",
        ask: box.dataset.ask,
        faq: box.dataset.faq,
        path: "/asistente/puesto",
        returnTo: { type: "shop", id: currentShop && currentShop.id },
        hello: "Asistente local del puesto/tienda. Si no sé, pregunta en el mostrador.",
      });
    });
  }
  const btnPersAsist = $("#btn-persona-assistant");
  if (btnPersAsist) {
    btnPersAsist.addEventListener("click", () => {
      const box = $("#persona-assistant");
      openLocalAsistente({
        label: $("#persona-assistant-label").textContent || "Asistente",
        ask: box.dataset.ask,
        faq: box.dataset.faq,
        path: "/asistente/persona",
        returnTo: { type: "persona", id: currentPersona && currentPersona.id },
        hello: "Asistente local de la tarjeta pública (offline).",
      });
    });
  }
  document.querySelectorAll("[data-shoptab]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tab = btn.dataset.shoptab;
      document.querySelectorAll("[data-shoptab]").forEach((b) => b.classList.toggle("active", b === btn));
      ["info", "avisos", "contacto"].forEach((t) => {
        const el = $("#shop-tab-" + t);
        if (el) el.classList.toggle("hidden", t !== tab);
      });
    });
  });
  const btnStallCreate = $("#btn-stall-create");
  if (btnStallCreate) {
    btnStallCreate.addEventListener("click", async () => {
      const box = $("#stall-create");
      const mode = box.dataset.mode;
      const parent = box.dataset.parent;
      const name = $("#stall-create-name").value.trim();
      const bio = $("#stall-create-bio").value.trim();
      const fb = $("#stall-create-feedback");
      if (!name) { fb.textContent = "Nombre obligatorio."; return; }
      try {
        if (mode === "shop") {
          const kind = parent === "mercado" ? "puesto" : "tienda";
          await fetchJSON("/api/shops", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ parent_id: parent, name, kind, info: bio }),
          });
          fb.textContent = "Creado (igual rango).";
          await openPlace(parent);
        } else {
          await fetchJSON("/api/personas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              display_name: name,
              bio,
              timbre_opt_in: $("#stall-create-timbre").checked,
            }),
          });
          fb.textContent = "Tarjeta creada.";
          await openPlace(parent === "residencial" ? "residencial" : "personas");
        }
      } catch (e) {
        fb.textContent = e.message;
      }
    });
  }

  function maybeShowOnboarding() {
    if (!onboarding) return;
    try {
      if (localStorage.getItem(ONBOARDING_KEY) === "1") return;
    } catch (_) {}
    onboarding.classList.remove("hidden");
  }

  const btnOnb = $("#btn-onboarding-ok");
  if (btnOnb) {
    btnOnb.addEventListener("click", () => {
      try { localStorage.setItem(ONBOARDING_KEY, "1"); } catch (_) {}
      if (onboarding) onboarding.classList.add("hidden");
    });
  }

  const btnViewCalles = $("#btn-view-calles");
  const btnViewMapa = $("#btn-view-mapa");
  const btnViewLista = $("#btn-view-lista");
  if (btnViewCalles) btnViewCalles.addEventListener("click", () => setHomeViewMode("calles"));
  if (btnViewMapa) btnViewMapa.addEventListener("click", () => setHomeViewMode("mapa"));
  if (btnViewLista) btnViewLista.addEventListener("click", () => setHomeViewMode("lista"));
  bindStreetControls();
  loadTodPrefs();
  loadClimaPrefs();
  loadBikePref();
  applyBikeUI();
  bindCityHUD();
  bindV29UI();
  bindV30UI();
  refreshMissions().catch(() => {});
  startTodLoop();
  startClimaLoop();
  refreshMarketDay().catch(() => {});
  try {
    const saved = localStorage.getItem("rcv_home_view_v24") || localStorage.getItem("rcv_home_view_v13");
    if (saved === "lista" || saved === "mapa" || saved === "calles") setHomeViewMode(saved);
    else setHomeViewMode("calles");
  } catch (_) {
    setHomeViewMode("calles");
  }


  const btnCampana = $("#btn-campana");
  if (btnCampana) {
    btnCampana.addEventListener("click", () => {
      const sheet = $("#campana-sheet");
      if (sheet && !sheet.classList.contains("hidden")) closeCampanaSheet();
      else openCampanaSheet();
    });
  }
  const btnCampanaCerrar = $("#btn-campana-cerrar");
  if (btnCampanaCerrar) btnCampanaCerrar.addEventListener("click", () => closeCampanaSheet());
  const campanaBackdrop = $("#campana-backdrop");
  if (campanaBackdrop) campanaBackdrop.addEventListener("click", () => closeCampanaSheet());
  const btnCampanaLeer = $("#btn-campana-leer");
  if (btnCampanaLeer) {
    btnCampanaLeer.addEventListener("click", async () => {
      try { await markCampanaRead(); } catch (e) { setStatus(e.message, "err"); }
    });
  }
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") refreshCampanaBadge();
  });


  /* kiosk + novedades wiring (v1.7) */
  readKioskPrefs();
  applyKioskUI();
  ["pointerdown", "keydown", "touchstart", "mousemove", "click", "scroll"].forEach((ev) => {
    document.addEventListener(ev, bumpKioskIdle, { passive: true });
  });
  const kioskToggle = $("#nodo-kiosk-toggle");
  if (kioskToggle) {
    kioskToggle.addEventListener("change", () => setKioskEnabled(kioskToggle.checked));
  }
  const kioskIdleSel = $("#nodo-kiosk-idle");
  if (kioskIdleSel) {
    kioskIdleSel.addEventListener("change", () => setKioskIdleMin(kioskIdleSel.value));
  }
  bindHoldToExit($("#btn-kiosk-exit-hold"));
  bindHoldToExit($("#btn-kiosk-exit-fab"));
  const btnFsDismiss = $("#btn-kiosk-fs-dismiss");
  if (btnFsDismiss) {
    btnFsDismiss.addEventListener("click", () => {
      try { localStorage.setItem(KIOSK_FS_HINT_KEY, "1"); } catch (_) {}
      hideKioskFsHint();
    });
  }
  const btnNodoNov = $("#btn-nodo-novedades");
  if (btnNodoNov) btnNodoNov.addEventListener("click", () => showNovedades());
  const btnFootNov = $("#btn-footer-novedades");
  if (btnFootNov) btnFootNov.addEventListener("click", () => showNovedades());
  const btnOnbNov = $("#btn-onboarding-novedades");
  if (btnOnbNov) {
    btnOnbNov.addEventListener("click", () => {
      try { localStorage.setItem(ONBOARDING_KEY, "1"); } catch (_) {}
      if (onboarding) onboarding.classList.add("hidden");
      showNovedades();
    });
  }

  bindTallerUI();

  boot();
})();
