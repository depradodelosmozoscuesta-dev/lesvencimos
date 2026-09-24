/*! Les vencimos · modo maestro runtime (offline / file://)
 *  Carga maestro.json, habla con speechSynthesis, desplaza, enfoca y mueve el puntero.
 *  Voces por rol (narrador/chico/chica/mayor/perro/timbre) y diálogos multi-réplica.
 *  Atajo «Modo maestro» siempre (si body[data-maestro-json]); barra grande con ?maestro=1.
 */
(function (global) {
  'use strict';

  var NS = 'LesVencimosMaestro';
  if (global[NS] && global[NS].__booted) return;

  /** Catálogo de roles: pitch/rate relativos + pista de género para pickVoice */
  var ROLES = {
    narrador: { pitch: 1, rate: 1, gender: 'any', label: 'Narrador', chip: 'narrador' },
    chico: { pitch: 0.88, rate: 1.02, gender: 'male', label: 'Chico', chip: 'chico' },
    chica: { pitch: 1.22, rate: 1.05, gender: 'female', label: 'Chica', chip: 'chica' },
    mayor: { pitch: 0.72, rate: 0.82, gender: 'male', label: 'Mayor', chip: 'mayor' },
    perro: { pitch: 1.75, rate: 1.35, gender: 'any', label: 'Perro', chip: 'perro' },
    timbre: { pitch: 1.4, rate: 1.15, gender: 'any', label: 'Timbre', chip: 'timbre' }
  };

  /** Alias de guion → rol de voz (la etiqueta en barra usa el alias capitalizado) */
  var VOZ_ALIAS = {
    narrador: 'narrador',
    chico: 'chico',
    chica: 'chica',
    mayor: 'mayor',
    perro: 'perro',
    timbre: 'timbre',
    vendedor: 'mayor',
    alumna: 'chica',
    alumno: 'chico'
  };

  var MALE_HINTS = /male|hombre|man|boy|david|jorge|juan|pablo|diego|miguel|carlos|pedro|antonio|jose|josé|raul|raúl|sergio|andres|andrés|miguel|francisco|manuel|paul|james|mark|john|thomas|daniel|microsoft\s+pablo|google\s+español.*españa.*male|español\s+españa\s+masculino|es-es-x-eed|es-es-x-eea|es_es_male|neural2-b|wavenet-b|wavenet-c|standard-b|standard-c/i;
  var FEMALE_HINTS = /female|mujer|woman|girl|maria|maría|lucia|lucía|carmen|ana|elena|laura|sofia|sofía|isabel|monica|mónica|patricia|sara|paulina|conchita|monica|microsoft\s+helena|microsoft\s+sabina|google\s+español.*female|español\s+españa\s+femenino|es-es-x-ef[a-z]|es_es_female|neural2-a|neural2-c|neural2-e|wavenet-a|wavenet-d|wavenet-e|standard-a|standard-d|standard-e/i;

  var state = {
    json: null,
    pasos: [],
    idx: -1,
    speaking: false,
    paused: false,
    running: false,
    utter: null,
    focusEl: null,
    bar: null,
    pointer: null,
    reducedMotion: false,
    /** Monotón: sube en stop/next para abortar cadenas de diálogo */
    speakGen: 0,
    chipEl: null,
    /** Usuario activó maestro en esta página (atajo o ?maestro=1) */
    uiActive: false,
    atajoEl: null,
    guionReady: false,
    guionLoading: null
  };

  function qs(sel, root) {
    try { return (root || document).querySelector(sel); } catch (e) { return null; }
  }

  function qsa(sel, root) {
    try { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); } catch (e) { return []; }
  }

  function paramMaestro() {
    try {
      var u = new URL(global.location.href);
      return u.searchParams.get('maestro') === '1';
    } catch (e) {
      return /[?&]maestro=1(?:&|$)/.test(String(global.location.search || ''));
    }
  }

  function jsonUrlFromPage() {
    var body = document.body;
    var fromData = body && body.getAttribute('data-maestro-json');
    if (fromData) return fromData;
    var link = qs('link[rel="maestro-script"], meta[name="maestro-json"]');
    if (link) {
      return link.getAttribute('content') || link.getAttribute('href');
    }
    return 'maestro-01.json';
  }

  function ensurePointer() {
    if (state.pointer) return state.pointer;
    var el = document.createElement('div');
    el.id = 'maestro-puntero';
    el.setAttribute('aria-hidden', 'true');
    el.innerHTML =
      '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img">' +
      '<path fill="#0f172a" stroke="#fff" stroke-width="2" ' +
      'd="M18 8 L18 42 L26 36 L32 52 L38 50 L32 34 L44 34 Z"/>' +
      '</svg>';
    document.body.appendChild(el);
    state.pointer = el;
    return el;
  }

  function hidePointer() {
    if (state.pointer) state.pointer.classList.remove('is-visible');
  }

  function movePointerTo(el) {
    if (!el) { hidePointer(); return; }
    var p = ensurePointer();
    var r = el.getBoundingClientRect();
    var x = r.left + Math.min(r.width * 0.55, Math.max(24, r.width / 2));
    var y = r.top + Math.min(40, Math.max(16, r.height * 0.25));
    p.style.left = x + 'px';
    p.style.top = y + 'px';
    p.classList.add('is-visible');
  }

  function clearFocus() {
    if (state.focusEl) {
      state.focusEl.classList.remove('maestro-focus');
      state.focusEl = null;
    }
    qsa('.maestro-focus').forEach(function (n) { n.classList.remove('maestro-focus'); });
  }

  function applyFocus(el) {
    clearFocus();
    if (!el) return;
    el.classList.add('maestro-focus');
    state.focusEl = el;
  }

  function resolveAncla(paso) {
    if (!paso || !paso.ancla) return null;
    return qs(paso.ancla);
  }

  function resolvePunteroTarget(paso, anclaEl) {
    if (!paso) return anclaEl;
    if (paso.puntero === false) return null;
    if (typeof paso.puntero === 'string' && paso.puntero.length) {
      var inside = anclaEl ? qs(paso.puntero, anclaEl) : null;
      return inside || qs(paso.puntero) || anclaEl;
    }
    return anclaEl;
  }

  function scrollToEl(el) {
    if (!el || typeof el.scrollIntoView !== 'function') return;
    try {
      el.scrollIntoView({ behavior: state.reducedMotion ? 'auto' : 'smooth', block: 'center', inline: 'nearest' });
    } catch (e) {
      try { el.scrollIntoView(true); } catch (e2) { /* ignore */ }
    }
  }

  function postToIframes(cmd) {
    if (!cmd || !cmd.type) return;
    var frames = qsa('iframe');
    frames.forEach(function (frame) {
      try {
        if (frame.contentWindow) {
          frame.contentWindow.postMessage(cmd, '*');
        }
      } catch (e) { /* file:// / cross-origin may throw; ignore */ }
    });
  }

  function capitalizeLabel(key) {
    var k = String(key || '');
    if (!k) return 'Narrador';
    return k.charAt(0).toUpperCase() + k.slice(1);
  }

  function resolveRole(vozKey) {
    var raw = String(vozKey || 'narrador').toLowerCase().trim();
    var roleId = VOZ_ALIAS[raw] || (ROLES[raw] ? raw : 'narrador');
    var role = ROLES[roleId] || ROLES.narrador;
    return {
      id: roleId,
      alias: raw,
      pitch: role.pitch,
      rate: role.rate,
      gender: role.gender,
      label: capitalizeLabel(raw),
      chip: role.chip
    };
  }

  /**
   * pickVoice(preferGender: 'male'|'female'|'any')
   * Prefiere voces es-* y, si hay pista de género en el nombre, la usa.
   */
  function pickVoice(preferGender) {
    if (!global.speechSynthesis) return null;
    var voices = global.speechSynthesis.getVoices() || [];
    if (!voices.length) return null;
    var want = String(preferGender || 'any').toLowerCase();

    var es = [];
    var preferLang = [
      /es[-_]ES/i, /Spanish.*Spain/i, /español.*España/i,
      /es[-_]MX/i, /es[-_]AR/i, /^es\b/i, /Spanish/i
    ];
    for (var i = 0; i < preferLang.length; i++) {
      for (var j = 0; j < voices.length; j++) {
        var v = voices[j];
        var label = (v.lang || '') + ' ' + (v.name || '');
        if (preferLang[i].test(v.lang) || preferLang[i].test(label)) {
          if (es.indexOf(v) === -1) es.push(v);
        }
      }
      if (es.length) break;
    }
    var pool = es.length ? es : voices;

    function scoreGender(v) {
      var name = (v.name || '') + ' ' + (v.lang || '');
      var isF = FEMALE_HINTS.test(name);
      var isM = MALE_HINTS.test(name);
      if (want === 'female') {
        if (isF && !isM) return 2;
        if (isF) return 1;
        if (isM && !isF) return -1;
        return 0;
      }
      if (want === 'male') {
        if (isM && !isF) return 2;
        if (isM) return 1;
        if (isF && !isM) return -1;
        return 0;
      }
      return 0;
    }

    if (want === 'male' || want === 'female') {
      var best = null;
      var bestScore = -99;
      for (var k = 0; k < pool.length; k++) {
        var s = scoreGender(pool[k]);
        if (s > bestScore) {
          bestScore = s;
          best = pool[k];
        }
      }
      if (best && bestScore > 0) return best;
    }
    return pool[0];
  }

  function bumpSpeakGen() {
    state.speakGen += 1;
    return state.speakGen;
  }

  function stopSpeech() {
    bumpSpeakGen();
    state.speaking = false;
    state.utter = null;
    if (global.speechSynthesis) {
      try { global.speechSynthesis.cancel(); } catch (e) { /* ignore */ }
    }
  }

  /**
   * Habla una línea. opts:
   *   - voz: clave de rol/alias (default narrador)
   *   - cancel: si true (default), cancela voz previa; false = encadenar diálogo
   *   - gen: generación esperada; si state.speakGen cambió, no habla
   */
  function speak(text, opts) {
    opts = opts || {};
    var doCancel = opts.cancel !== false;
    var expectedGen = opts.gen != null ? opts.gen : state.speakGen;

    return new Promise(function (resolve) {
      var done = false;
      function finish() {
        if (done) return;
        done = true;
        state.speaking = false;
        state.utter = null;
        resolve();
      }

      if (expectedGen !== state.speakGen) { finish(); return; }
      if (!text) { finish(); return; }
      if (!global.speechSynthesis || typeof global.SpeechSynthesisUtterance !== 'function') {
        finish();
        return;
      }

      if (doCancel) {
        // Cancelar sin bumpear gen (seguimos en la misma cadena / paso)
        state.speaking = false;
        state.utter = null;
        try { global.speechSynthesis.cancel(); } catch (e) { /* ignore */ }
      }

      if (expectedGen !== state.speakGen) { finish(); return; }

      var role = resolveRole(opts.voz);
      var u = new global.SpeechSynthesisUtterance(String(text));
      u.lang = 'es-ES';
      u.rate = role.rate;
      u.pitch = role.pitch;
      var voice = pickVoice(role.gender);
      if (voice) u.voice = voice;
      u.onend = function () {
        if (expectedGen !== state.speakGen) { finish(); return; }
        finish();
      };
      u.onerror = finish;
      state.utter = u;
      state.speaking = true;
      try {
        global.speechSynthesis.speak(u);
      } catch (e) {
        finish();
      }
    });
  }

  function wait(ms) {
    return new Promise(function (resolve) {
      global.setTimeout(resolve, Math.max(0, ms || 0));
    });
  }

  function setChip(roleOrNull) {
    if (!state.bar) return;
    var chip = state.chipEl || qs('.maestro-voz-chip', state.bar);
    if (!chip) return;
    state.chipEl = chip;
    if (!roleOrNull) {
      chip.hidden = true;
      chip.textContent = '';
      chip.className = 'maestro-voz-chip';
      return;
    }
    chip.hidden = false;
    chip.textContent = roleOrNull.label;
    chip.className = 'maestro-voz-chip maestro-voz-' + (roleOrNull.chip || 'narrador');
  }

  function setBarText(paso, extra, lineText, role) {
    if (!state.bar) return;
    var txt = qs('.maestro-paso-texto', state.bar);
    var st = qs('.maestro-estado', state.bar);
    if (txt) {
      if (lineText != null) {
        if (role && role.label) {
          txt.textContent = role.label + ': ' + lineText;
        } else {
          txt.textContent = lineText;
        }
      } else if (paso && paso.dialogo && paso.dialogo.length) {
        txt.textContent = '(diálogo · ' + paso.dialogo.length + ' réplicas)';
      } else {
        txt.textContent = (paso && paso.decir) || '';
      }
    }
    setChip(role || null);
    if (st) {
      var n = state.pasos.length;
      var i = state.idx + 1;
      var base = n ? ('Paso ' + Math.max(i, 0) + ' / ' + n) : 'Sin guion';
      st.textContent = extra ? base + ' · ' + extra : base;
    }
  }


  function hasMaestroPage() {
    return !!(document.body && document.body.getAttribute('data-maestro-json'));
  }

  function withMaestroQuery(href) {
    if (!href || href === '#' || /^javascript:/i.test(href)) return href;
    try {
      var abs = new URL(href, global.location.href);
      abs.searchParams.set('maestro', '1');
      // If original was a relative filename / relative path, keep relative form
      if (!/^[a-z]+:/i.test(href) && href.indexOf('//') !== 0) {
        var hash = abs.hash || '';
        var q = abs.search || '';
        // Preserve directory prefixes from original href
        var pathOnly = href.split('#')[0].split('?')[0];
        return pathOnly + q + hash;
      }
      return abs.pathname + abs.search + abs.hash;
    } catch (e) {
      if (/[?&]maestro=1(?:&|#|$)/.test(href)) return href;
      var parts = href.split('#');
      var base = parts[0];
      var hash = parts.length > 1 ? '#' + parts.slice(1).join('#') : '';
      base += base.indexOf('?') >= 0 ? '&maestro=1' : '?maestro=1';
      return base + hash;
    }
  }

  function patchNavLinks() {
    qsa('a.atajo-prev, a.atajo-next').forEach(function (a) {
      var href = a.getAttribute('href');
      if (!href) return;
      var next = withMaestroQuery(href);
      if (next && next !== href) a.setAttribute('href', next);
    });
  }

  function setUrlMaestro() {
    try {
      var u = new URL(global.location.href);
      if (u.searchParams.get('maestro') === '1') return;
      u.searchParams.set('maestro', '1');
      global.history.replaceState({}, '', u.pathname + u.search + u.hash);
    } catch (e) {
      /* file:// or odd URLs: ignore */
    }
  }

  function updateAtajoLabel() {
    var el = state.atajoEl;
    if (!el) return;
    if (state.uiActive) {
      el.textContent = 'Modo maestro · activo';
      el.setAttribute('title', 'Abrir o ir a la barra de modo maestro');
      el.setAttribute('aria-pressed', 'true');
      el.classList.add('is-activo');
    } else {
      el.textContent = 'Modo maestro';
      el.setAttribute('title', 'Activar modo maestro (voz + puntero)');
      el.setAttribute('aria-pressed', 'false');
      el.classList.remove('is-activo');
    }
  }

  function ensureAtajoControl() {
    if (state.atajoEl && state.atajoEl.isConnected) return state.atajoEl;
    if (!hasMaestroPage()) return null;

    var pie = qs('.leccion-pie');
    var existing = qs('.atajo-maestro');
    if (existing) {
      // Keep the shortcut at the bottom even if an older shell placed it above.
      if (pie && existing.parentNode !== pie) pie.appendChild(existing);
      state.atajoEl = existing;
      return existing;
    }

    var el = document.createElement('a');
    el.href = '#maestro-barra';
    el.className = 'atajo atajo-maestro';
    el.setAttribute('role', 'button');
    el.textContent = 'Modo maestro';
    el.setAttribute('title', 'Activar modo maestro (voz + puntero)');
    el.setAttribute('aria-pressed', 'false');

    var atajos = qs('.leccion-atajos');
    if (pie) {
      pie.appendChild(el);
    } else if (atajos) {
      atajos.appendChild(el);
    } else {
      el.style.cssText = 'position:fixed;left:12px;bottom:12px;z-index:99999';
      document.body.appendChild(el);
    }

    el.addEventListener('click', function (ev) {
      ev.preventDefault();
      if (state.uiActive) {
        showBar(true);
        var bar = ensureBar();
        try {
          if (bar && typeof bar.scrollIntoView === 'function') {
            bar.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        } catch (e2) { /* ignore */ }
        return;
      }
      activateMaestroUi();
    });

    state.atajoEl = el;
    return el;
  }

  async function loadGuionOnce() {
    if (state.guionReady) return true;
    if (state.guionLoading) return state.guionLoading;
    state.guionLoading = (async function () {
      var url = jsonUrlFromPage();
      try {
        state.json = await loadJson(url);
        state.pasos = (state.json && state.json.pasos) || [];
        setBarText(null, state.pasos.length ? 'listo · pulsa Empezar' : 'guion vacío');
        state.guionReady = true;
        try {
          global.dispatchEvent(new CustomEvent('maestro:ready', { detail: { url: url, pasos: state.pasos.length } }));
        } catch (e) { /* ignore */ }
        return true;
      } catch (err) {
        setBarText(null, 'No se pudo cargar el guion (file://). Usa Empezar tras servir en local o incrusta el JSON.');
        console.warn('[maestro]', err);
        return false;
      } finally {
        state.guionLoading = null;
      }
    })();
    return state.guionLoading;
  }

  function preloadVoices() {
    if (!global.speechSynthesis) return;
    try { global.speechSynthesis.getVoices(); } catch (e) { /* ignore */ }
    if (typeof global.speechSynthesis.onvoiceschanged !== 'undefined') {
      global.speechSynthesis.onvoiceschanged = function () {
        pickVoice('any');
      };
    }
  }

  async function activateMaestroUi() {
    state.uiActive = true;
    setUrlMaestro();
    patchNavLinks();
    updateAtajoLabel();
    showBar(true);
    setBarText(null, 'cargando guion…');
    ensurePointer();
    preloadVoices();
    await loadGuionOnce();
    return true;
  }

  function ensureBar() {
    if (state.bar) return state.bar;
    var bar = document.createElement('div');
    bar.id = 'maestro-barra';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Modo maestro');
    bar.innerHTML =
      '<p class="maestro-barra-titulo">Modo maestro <span class="maestro-voz-chip" hidden></span></p>' +
      '<p class="maestro-paso-texto"></p>' +
      '<p class="maestro-estado"></p>' +
      '<div class="maestro-barra-botones">' +
      '<button type="button" data-cmd="start">Empezar</button>' +
      '<button type="button" class="secondary" data-cmd="next">Siguiente</button>' +
      '<button type="button" class="secondary" data-cmd="repeat">Repite</button>' +
      '<button type="button" class="secondary" data-cmd="stop">Para</button>' +
      '</div>';
    document.body.appendChild(bar);
    bar.addEventListener('click', function (ev) {
      var btn = ev.target && ev.target.closest ? ev.target.closest('[data-cmd]') : null;
      if (!btn) return;
      var cmd = btn.getAttribute('data-cmd');
      if (cmd === 'start') api.start();
      else if (cmd === 'next') api.next();
      else if (cmd === 'repeat') api.repeat();
      else if (cmd === 'stop') api.stop();
    });
    state.bar = bar;
    state.chipEl = qs('.maestro-voz-chip', bar);
    return bar;
  }

  function showBar(on) {
    var bar = ensureBar();
    if (on) bar.classList.add('is-on');
    else bar.classList.remove('is-on');
  }

  function linesFromPaso(paso) {
    if (!paso) return [];
    if (paso.dialogo && Object.prototype.toString.call(paso.dialogo) === '[object Array]' && paso.dialogo.length) {
      return paso.dialogo.map(function (line) {
        return {
          voz: (line && line.voz) || 'narrador',
          decir: (line && line.decir) || ''
        };
      });
    }
    return [{
      voz: paso.voz || 'narrador',
      decir: paso.decir || ''
    }];
  }

  async function speakPasoLines(paso, gen) {
    var lines = linesFromPaso(paso);
    for (var i = 0; i < lines.length; i++) {
      if (gen !== state.speakGen || state.paused) return false;
      var line = lines[i];
      var role = resolveRole(line.voz);
      setBarText(paso, 'hablando…', line.decir, role);
      // Primera línea cancela eco previo; el resto encadena sin cancel
      await speak(line.decir, {
        voz: line.voz,
        cancel: i === 0,
        gen: gen
      });
      if (gen !== state.speakGen || state.paused) return false;
      // Micro-pausa entre réplicas de diálogo (no entre única línea)
      if (i < lines.length - 1) {
        await wait(180);
      }
    }
    return gen === state.speakGen && !state.paused;
  }

  async function runPaso(i) {
    if (i < 0 || i >= state.pasos.length) {
      state.running = false;
      state.idx = state.pasos.length;
      setBarText(null, 'Fin');
      setChip(null);
      hidePointer();
      clearFocus();
      return;
    }
    state.idx = i;
    state.running = true;
    state.paused = false;
    var paso = state.pasos[i];
    var gen = bumpSpeakGen();
    setBarText(paso, 'hablando…');

    var ancla = resolveAncla(paso);
    if (ancla) {
      scrollToEl(ancla);
      applyFocus(ancla);
      var tip = resolvePunteroTarget(paso, ancla);
      await wait(paso.esperaMs != null ? paso.esperaMs : 350);
      if (gen !== state.speakGen) return;
      movePointerTo(tip || ancla);
    } else {
      clearFocus();
      hidePointer();
      await wait(paso.esperaMs != null ? paso.esperaMs : 200);
      if (gen !== state.speakGen) return;
    }

    if (paso.iframeCmd) {
      postToIframes(paso.iframeCmd);
      await wait(120);
      if (gen !== state.speakGen) return;
    }

    if (state.paused || gen !== state.speakGen) {
      setBarText(paso, 'en pausa');
      return;
    }

    var ok = await speakPasoLines(paso, gen);

    if (!ok || state.paused || gen !== state.speakGen) {
      if (state.paused) setBarText(paso, 'en pausa');
      return;
    }

    // Autoavance al siguiente si seguimos en marcha y nadie pidió pausa
    if (state.running && !state.paused && state.idx === i && gen === state.speakGen) {
      setBarText(paso, 'listo');
      await wait(280);
      if (state.running && !state.paused && state.idx === i && gen === state.speakGen) {
        await runPaso(i + 1);
      }
    }
  }

  async function loadJson(url) {
    // file:// : fetch a veces falla; intentar XHR y, si no, incrustar vía <script type="application/json">
    var embedded = qs('script[type="application/json"][data-maestro="guion"]');
    if (embedded && embedded.textContent) {
      return JSON.parse(embedded.textContent);
    }
    if (global.fetch) {
      try {
        var res = await global.fetch(url, { cache: 'no-store' });
        if (res && res.ok) return await res.json();
      } catch (e) { /* fall through */ }
    }
    return await new Promise(function (resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', url, true);
      xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) return;
        if (xhr.status === 0 || (xhr.status >= 200 && xhr.status < 300)) {
          try { resolve(JSON.parse(xhr.responseText)); }
          catch (err) { reject(err); }
        } else {
          reject(new Error('No se pudo cargar ' + url + ' (status ' + xhr.status + ')'));
        }
      };
      xhr.onerror = function () { reject(new Error('Error de red/local al cargar ' + url)); };
      xhr.send();
    });
  }

  var api = {
    __booted: false,
    roles: ROLES,
    activate: activateMaestroUi,
    patchNavLinks: patchNavLinks,
    resolveRole: resolveRole,
    pickVoice: pickVoice,
    speak: speak,
    getState: function () {
      return {
        idx: state.idx,
        total: state.pasos.length,
        running: state.running,
        paused: state.paused,
        speaking: state.speaking,
        titulo: state.json && state.json.titulo
      };
    },
    command: function (name) {
      var n = String(name || '').toLowerCase().trim();
      if (n === 'siguiente' || n === 'next') return api.next();
      if (n === 'repite' || n === 'repetir' || n === 'repeat') return api.repeat();
      if (n === 'para' || n === 'stop' || n === 'pausa') return api.stop();
      if (n === 'pregunta' || n === 'preguntar') return api.askMode();
      if (n === 'empezar' || n === 'start' || n === 'modo maestro') {
        if (!state.uiActive && hasMaestroPage()) {
          return activateMaestroUi().then(function () { return api.start(); });
        }
        return api.start();
      }
      return false;
    },
    askMode: function () {
      api.stop();
      setBarText(state.pasos[state.idx] || null, 'modo preguntar (puedes escribir o hablar)');
      try {
        global.dispatchEvent(new CustomEvent('maestro:preguntar', { detail: api.getState() }));
      } catch (e) { /* ignore */ }
      return true;
    },
    start: function () {
      if (!state.uiActive && hasMaestroPage()) {
        return activateMaestroUi().then(function () {
          if (!state.pasos.length) return false;
          state.paused = false;
          stopSpeech();
          showBar(true);
          runPaso(0);
          return true;
        });
      }
      if (!state.pasos.length) return false;
      state.paused = false;
      stopSpeech();
      showBar(true);
      runPaso(0);
      return true;
    },
    next: function () {
      if (!state.pasos.length) return false;
      state.paused = false;
      stopSpeech();
      var n = state.idx < 0 ? 0 : state.idx + 1;
      runPaso(n);
      return true;
    },
    repeat: function () {
      if (!state.pasos.length) return false;
      if (state.idx < 0) return api.start();
      state.paused = false;
      stopSpeech();
      runPaso(state.idx);
      return true;
    },
    stop: function () {
      state.paused = true;
      state.running = false;
      stopSpeech();
      setBarText(state.pasos[state.idx] || null, 'parado');
      return true;
    },
    destroy: function () {
      api.stop();
      hidePointer();
      clearFocus();
      showBar(false);
    }
  };

  async function boot() {
    if (api.__booted) return api;
    api.__booted = true;
    state.reducedMotion = !!(global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches);

    // Siempre: atajo compacto si la lección declara guion (Mate shells).
    if (hasMaestroPage()) {
      ensureAtajoControl();
    }

    var wantUi = paramMaestro() ||
      (document.body && document.body.getAttribute('data-maestro-autostart') === '1');

    if (wantUi && hasMaestroPage()) {
      await activateMaestroUi();
    } else if (wantUi && !hasMaestroPage()) {
      // Página sin data-maestro-json (p.ej. demo): barra clásica
      state.uiActive = true;
      showBar(true);
      setBarText(null, 'cargando guion…');
      ensurePointer();
      preloadVoices();
      await loadGuionOnce();
    }

    global[NS] = api;
    return api;
  }

  global[NS] = api;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { boot(); });
  } else {
    boot();
  }
})(typeof window !== 'undefined' ? window : this);
