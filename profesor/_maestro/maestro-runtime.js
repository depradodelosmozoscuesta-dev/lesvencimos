/*! Les vencimos · modo maestro runtime (offline / file://)
 *  Carga maestro.json, habla con speechSynthesis, desplaza, enfoca y mueve el puntero.
 *  Autoarranque solo con ?maestro=1 (o data-maestro-autostart).
 */
(function (global) {
  'use strict';

  var NS = 'LesVencimosMaestro';
  if (global[NS] && global[NS].__booted) return;

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
    reducedMotion: false
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
    if (state.reducedMotion) {
      p.style.left = x + 'px';
      p.style.top = y + 'px';
    } else {
      p.style.left = x + 'px';
      p.style.top = y + 'px';
    }
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

  function pickVoice() {
    if (!global.speechSynthesis) return null;
    var voices = global.speechSynthesis.getVoices() || [];
    if (!voices.length) return null;
    var prefer = [
      /es[-_]ES/i, /Spanish.*Spain/i, /español.*España/i,
      /es[-_]MX/i, /es[-_]AR/i, /^es\b/i, /Spanish/i
    ];
    for (var i = 0; i < prefer.length; i++) {
      for (var j = 0; j < voices.length; j++) {
        var v = voices[j];
        var label = (v.lang || '') + ' ' + (v.name || '');
        if (prefer[i].test(v.lang) || prefer[i].test(label)) return v;
      }
    }
    return voices[0];
  }

  function stopSpeech() {
    state.speaking = false;
    state.utter = null;
    if (global.speechSynthesis) {
      try { global.speechSynthesis.cancel(); } catch (e) { /* ignore */ }
    }
  }

  function speak(text) {
    return new Promise(function (resolve) {
      var done = false;
      function finish() {
        if (done) return;
        done = true;
        state.speaking = false;
        state.utter = null;
        resolve();
      }
      if (!text) { finish(); return; }
      if (!global.speechSynthesis || typeof global.SpeechSynthesisUtterance !== 'function') {
        finish();
        return;
      }
      stopSpeech();
      var u = new global.SpeechSynthesisUtterance(String(text));
      u.lang = 'es-ES';
      u.rate = 1;
      u.pitch = 1;
      var voice = pickVoice();
      if (voice) u.voice = voice;
      u.onend = finish;
      u.onerror = finish;
      state.utter = u;
      state.speaking = true;
      try {
        global.speechSynthesis.speak(u);
      } catch (e) {
        finish();
      }
      // Safari / algunos Chromium: si cancelan sin onend, no colgarse
      global.setTimeout(function () {
        if (state.utter === u && state.speaking) {
          /* aún hablando: no forzar */
        }
      }, 50);
    });
  }

  function wait(ms) {
    return new Promise(function (resolve) {
      global.setTimeout(resolve, Math.max(0, ms || 0));
    });
  }

  function setBarText(paso, extra) {
    if (!state.bar) return;
    var txt = qs('.maestro-paso-texto', state.bar);
    var st = qs('.maestro-estado', state.bar);
    if (txt) txt.textContent = (paso && paso.decir) || '';
    if (st) {
      var n = state.pasos.length;
      var i = state.idx + 1;
      var base = n ? ('Paso ' + Math.max(i, 0) + ' / ' + n) : 'Sin guion';
      st.textContent = extra ? base + ' · ' + extra : base;
    }
  }

  function ensureBar() {
    if (state.bar) return state.bar;
    var bar = document.createElement('div');
    bar.id = 'maestro-barra';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Modo maestro');
    bar.innerHTML =
      '<p class="maestro-barra-titulo">Modo maestro</p>' +
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
    return bar;
  }

  function showBar(on) {
    var bar = ensureBar();
    if (on) bar.classList.add('is-on');
    else bar.classList.remove('is-on');
  }

  async function runPaso(i) {
    if (i < 0 || i >= state.pasos.length) {
      state.running = false;
      state.idx = state.pasos.length;
      setBarText(null, 'Fin');
      hidePointer();
      clearFocus();
      return;
    }
    state.idx = i;
    state.running = true;
    state.paused = false;
    var paso = state.pasos[i];
    setBarText(paso, 'hablando…');

    var ancla = resolveAncla(paso);
    if (ancla) {
      scrollToEl(ancla);
      applyFocus(ancla);
      var tip = resolvePunteroTarget(paso, ancla);
      await wait(paso.esperaMs != null ? paso.esperaMs : 350);
      movePointerTo(tip || ancla);
    } else {
      clearFocus();
      hidePointer();
      await wait(paso.esperaMs != null ? paso.esperaMs : 200);
    }

    if (paso.iframeCmd) {
      postToIframes(paso.iframeCmd);
      await wait(120);
    }

    if (state.paused) {
      setBarText(paso, 'en pausa');
      return;
    }

    await speak(paso.decir || '');

    if (state.paused) {
      setBarText(paso, 'en pausa');
      return;
    }

    // Autoavance al siguiente si seguimos en marcha y nadie pidió pausa
    if (state.running && !state.paused && state.idx === i) {
      setBarText(paso, 'listo');
      await wait(280);
      if (state.running && !state.paused && state.idx === i) {
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
      if (n === 'empezar' || n === 'start' || n === 'modo maestro') return api.start();
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

    var wantUi = paramMaestro() ||
      (document.body && document.body.getAttribute('data-maestro-autostart') === '1');

    if (!wantUi) {
      global[NS] = api;
      return api;
    }

    showBar(true);
    setBarText(null, 'cargando guion…');
    ensurePointer();

    var url = jsonUrlFromPage();
    try {
      state.json = await loadJson(url);
      state.pasos = (state.json && state.json.pasos) || [];
      setBarText(null, state.pasos.length ? 'listo · pulsa Empezar' : 'guion vacío');
    } catch (err) {
      setBarText(null, 'No se pudo cargar el guion (file://). Usa Empezar tras servir en local o incrusta el JSON.');
      console.warn('[maestro]', err);
    }

    // Precargar voces (Chrome)
    if (global.speechSynthesis) {
      try { global.speechSynthesis.getVoices(); } catch (e) { /* ignore */ }
      if (typeof global.speechSynthesis.onvoiceschanged !== 'undefined') {
        global.speechSynthesis.onvoiceschanged = function () { pickVoice(); };
      }
    }

    // No auto-hablar sin gesto: políticas de autoplay. Ofrecemos Empezar.
    global[NS] = api;
    try {
      global.dispatchEvent(new CustomEvent('maestro:ready', { detail: { url: url, pasos: state.pasos.length } }));
    } catch (e) { /* ignore */ }
    return api;
  }

  global[NS] = api;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { boot(); });
  } else {
    boot();
  }
})(typeof window !== 'undefined' ? window : this);
