#!/usr/bin/env python3
"""Patch biblioteca.html for resume TTS, background keepalive, richer SFX (v20260922p)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "modulos" / "biblioteca.html"

def main():
    html = HTML.read_text(encoding="utf-8")
    orig = html

    # ── 1) Reader bar UI: Continuar / Desde principio / keep-screen toggle ──
    old_bar = '''    <div class="reader-bar" id="reader-bar" aria-label="Controles de lectura">
      <div class="row">
        <button type="button" class="primary" id="tts-play">Leer</button>
        <button type="button" id="tts-pause">Pausa</button>
        <button type="button" id="tts-stop">Parar</button>
        <button type="button" id="sfx-toggle" class="on">SFX</button>
      </div>
      <label class="field" style="margin:0 0 .35rem"><span>Voz del sistema</span>
        <select id="tts-voice"></select>
      </label>
      <label class="field" style="margin:0"><span>Velocidad</span>
        <input type="range" id="tts-rate" min="0.7" max="1.4" step="0.05" value="1">
      </label>
      <p class="status" id="tts-status"></p>
    </div>
    <p class="tap-hint" id="voice-note">Toca un párrafo para «Leer desde aquí». Controles fijos arriba · no hace falta bajar al final.</p>'''

    new_bar = '''    <div class="reader-bar" id="reader-bar" aria-label="Controles de lectura">
      <div class="row">
        <button type="button" class="primary" id="tts-play">Leer</button>
        <button type="button" id="tts-continue" hidden>Continuar</button>
        <button type="button" id="tts-from-start">Desde el principio</button>
        <button type="button" id="tts-pause">Pausa</button>
        <button type="button" id="tts-stop">Parar</button>
        <button type="button" id="sfx-toggle" class="on">SFX</button>
      </div>
      <label class="field" style="margin:0 0 .35rem"><span>Voz del sistema</span>
        <select id="tts-voice"></select>
      </label>
      <label class="field" style="margin:0 0 .35rem"><span>Velocidad</span>
        <input type="range" id="tts-rate" min="0.7" max="1.4" step="0.05" value="1">
      </label>
      <label class="field" style="margin:0;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap">
        <input type="checkbox" id="tts-keep-awake" style="width:auto;min-height:0">
        <span>Mantener lectura con pantalla apagada</span>
      </label>
      <p class="status" id="tts-status"></p>
      <p class="hint" id="tts-bg-tip" style="margin:.25rem 0 0;font-size:.78rem;opacity:.85">Si apagas la pantalla, Android suele matar speechSynthesis; al volver te ofrecemos Continuar. Ambientes se pausan con la voz para no quedar solos.</p>
    </div>
    <p class="tap-hint" id="voice-note">Toca un párrafo para «Leer desde aquí». Usa Continuar si hay posición guardada. Controles fijos arriba.</p>
    <div class="row" id="jump-row" style="margin:.35rem 0 .55rem;flex-wrap:wrap;gap:.35rem"></div>'''

    if old_bar not in html:
        raise SystemExit('reader bar block not found')
    html = html.replace(old_bar, new_bar, 1)

    # Ambient buttons: add interiores + muchedumbre
    old_amb = '''    <div class="row" id="amb-btns">
      <button type="button" data-amb="bosque">Bosque</button>
      <button type="button" data-amb="lluvia">Lluvia</button>
      <button type="button" data-amb="caballos">Caballos</button>
      <button type="button" data-amb="fuego">Fuego</button>
      <button type="button" data-amb="mar">Mar</button>
      <button type="button" data-amb="noche">Noche</button>
      <button type="button" data-amb="rio">Río</button>
      <button type="button" data-amb="viento">Viento</button>
    </div>'''
    new_amb = '''    <div class="row" id="amb-btns">
      <button type="button" data-amb="bosque">Bosque</button>
      <button type="button" data-amb="lluvia">Lluvia</button>
      <button type="button" data-amb="caballos">Caballos</button>
      <button type="button" data-amb="fuego">Fuego</button>
      <button type="button" data-amb="mar">Mar</button>
      <button type="button" data-amb="noche">Noche</button>
      <button type="button" data-amb="rio">Río</button>
      <button type="button" data-amb="viento">Viento</button>
      <button type="button" data-amb="interiores">Interiores</button>
      <button type="button" data-amb="muchedumbre">Muchedumbre</button>
      <button type="button" data-amb="tormenta">Tormenta</button>
    </div>'''
    if old_amb not in html:
        raise SystemExit('amb buttons not found')
    html = html.replace(old_amb, new_amb, 1)

    # SFX hint text
    html = html.replace(
        'Al leer o al tocar un párrafo, si el texto habla de caballos, lluvia, truenos, mar, bosque, fuego… suena un efecto corto (Web Audio). El botón SFX de la barra lo activa o apaga.',
        'Al leer o al tocar un párrafo: lluvia, tormenta, mar, bosque, caballos, fuego, noche, viento, río, campana, espada, lobo, interiores (eco/pasos/puerta), muchedumbre/plaza/mercado… Efectos Web Audio en capas. El botón SFX de la barra lo activa o apaga.',
        1,
    )

    # Info list tip
    html = html.replace(
        '<li>En Leer, la barra superior fija tiene Leer / Pausa / Parar, voz y velocidad (sin bajar al final). Toca un párrafo para leer desde ahí.</li>',
        '<li>En Leer: Continuar (posición guardada), Desde el principio, o toca un párrafo. «Mantener lectura con pantalla apagada» intenta Wake Lock + audio silencioso; Android a menudo mata speechSynthesis igual — al volver te ofrecemos Continuar.</li>',
        1,
    )

    # ── 2) JS: LS keys + resume state after LS_SFX ──
    old_ls = """  var LS_VOICE = 'lv-biblio-voice';
  var LS_RATE = 'lv-biblio-rate';
  var LS_SFX = 'lv-biblio-sfx';
  var currentId = null;
  var currentText = '';
  var currentCat = 'todas';
  var paras = [];"""

    new_ls = """  var LS_VOICE = 'lv-biblio-voice';
  var LS_RATE = 'lv-biblio-rate';
  var LS_SFX = 'lv-biblio-sfx';
  var LS_POS = 'lv-biblio-pos-v1';
  var LS_KEEP = 'lv-biblio-keep-awake';
  var currentId = null;
  var currentText = '';
  var currentCat = 'todas';
  var paras = [];
  var paraStartIdx = 0; // paragraph index where current TTS queue starts
  var resumeParaIdx = 0;
  var resumeChunkOff = 0;
  var ttsWasReading = false;
  var ttsKeepAwake = localStorage.getItem(LS_KEEP) === '1';
  var wakeLockSentinel = null;
  var keepAliveAudio = null;
  var ambPausedByHide = false;
  var ambKindBeforeHide = null;"""

    if old_ls not in html:
        raise SystemExit('LS block not found')
    html = html.replace(old_ls, new_ls, 1)

    # ── 3) Replace showText click handler + end of showText to add resume UI ──
    old_show_click = """      p.addEventListener('click', function () {
        body.querySelectorAll('p').forEach(function (x) { x.classList.remove('active'); });
        p.classList.add('active');
        triggerSfxFromText(para);
        // Leer desde este párrafo hasta el final del capítulo/libro
        var fromHere = paras.slice(idx).join('\\n\\n');
        document.getElementById('tts-status').textContent = 'Desde párrafo ' + (idx + 1) + '…';
        speakText(fromHere);
      });
      body.appendChild(p);
      paras.push(para);
    });
    renderBooks();
    goLeer();
    stopTTS();
    // Scroll so sticky bar + title stay visible at top of reader
    try {
      document.getElementById('reader').scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (e) {}
  }"""

    new_show_click = """      p.addEventListener('click', function () {
        body.querySelectorAll('p').forEach(function (x) { x.classList.remove('active'); });
        p.classList.add('active');
        triggerSfxFromText(para);
        savePos(currentId, idx, 0);
        resumeParaIdx = idx; resumeChunkOff = 0;
        updateResumeUI();
        var fromHere = paras.slice(idx).join('\\n\\n');
        document.getElementById('tts-status').textContent = 'Desde párrafo ' + (idx + 1) + '…';
        speakText(fromHere, { paraStart: idx, chunkOff: 0 });
      });
      body.appendChild(p);
      paras.push(para);
    });
    renderBooks();
    goLeer();
    stopTTS(false);
    loadPosForBook(currentId);
    updateResumeUI();
    buildJumpRow();
    try {
      document.getElementById('reader').scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (e) {}
  }

  function posKey(id) { return LS_POS + ':' + id; }
  function loadPosForBook(id) {
    resumeParaIdx = 0; resumeChunkOff = 0;
    if (!id) return;
    try {
      var raw = localStorage.getItem(posKey(id));
      if (!raw) return;
      var o = JSON.parse(raw);
      resumeParaIdx = Math.max(0, parseInt(o.para, 10) || 0);
      resumeChunkOff = Math.max(0, parseInt(o.chunk, 10) || 0);
    } catch (e) {}
  }
  function savePos(id, para, chunk) {
    if (!id) return;
    try {
      localStorage.setItem(posKey(id), JSON.stringify({ para: para|0, chunk: chunk|0, t: Date.now() }));
    } catch (e) {}
    resumeParaIdx = para|0; resumeChunkOff = chunk|0;
    updateResumeUI();
  }
  function updateResumeUI() {
    var btn = document.getElementById('tts-continue');
    if (!btn) return;
    var has = currentId && paras.length && resumeParaIdx > 0;
    btn.hidden = !has;
    if (has) btn.textContent = 'Continuar · ¶' + (resumeParaIdx + 1);
  }
  function buildJumpRow() {
    var row = document.getElementById('jump-row');
    if (!row) return;
    row.innerHTML = '';
    if (!paras.length) return;
    var heads = [];
    paras.forEach(function (p, i) {
      var t = String(p || '').trim();
      if (/^Cap[ií]tulo\\b/i.test(t) || /^PART\\b/i.test(t) || /^Chapter\\b/i.test(t) || /^PRIMERA PARTE/i.test(t) || /^SEGUNDA PARTE/i.test(t)) {
        heads.push({ i: i, label: t.split(/\\n/)[0].slice(0, 42) });
      }
    });
    heads.slice(0, 12).forEach(function (h) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = h.label;
      b.style.fontSize = '.78rem';
      b.addEventListener('click', function () {
        savePos(currentId, h.i, 0);
        var el = document.querySelector('#r-body p[data-i=\"' + h.i + '\"]');
        if (el) {
          document.querySelectorAll('#r-body p').forEach(function (x) { x.classList.remove('active'); });
          el.classList.add('active');
          try { el.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (e) {}
        }
        speakText(paras.slice(h.i).join('\\n\\n'), { paraStart: h.i, chunkOff: 0 });
      });
      row.appendChild(b);
    });
  }"""

    if old_show_click not in html:
        raise SystemExit('showText click block not found')
    html = html.replace(old_show_click, new_show_click, 1)

    # ── 4) Replace stopTTS / speakChunk progress / speakText / play handlers ──
    old_stop = """  function stopTTS() {
    ttsStopping = true;
    ttsQueue = [];
    ttsQueueIdx = 0;
    ttsActiveText = '';
    if (window.speechSynthesis) speechSynthesis.cancel();
    ttsUtter = null;
    ttsPaused = false;
    document.getElementById('tts-status').textContent = '';
    if (ttsWatch) { clearInterval(ttsWatch); ttsWatch = null; }
    setTimeout(function () { ttsStopping = false; }, 80);
  }"""

    new_stop = """  function stopTTS(clearPos) {
    ttsStopping = true;
    ttsWasReading = false;
    // Persist current place before wiping queue
    if (currentId && ttsQueue.length) {
      savePos(currentId, paraStartIdx + Math.max(0, ttsQueueIdx), 0);
    }
    ttsQueue = [];
    ttsQueueIdx = 0;
    ttsActiveText = '';
    if (window.speechSynthesis) speechSynthesis.cancel();
    ttsUtter = null;
    ttsPaused = false;
    if (clearPos) {
      resumeParaIdx = 0; resumeChunkOff = 0;
      if (currentId) try { localStorage.removeItem(posKey(currentId)); } catch (e) {}
    }
    document.getElementById('tts-status').textContent = clearPos ? 'Reinicio.' : '';
    if (ttsWatch) { clearInterval(ttsWatch); ttsWatch = null; }
    releaseWakeLock();
    stopKeepAliveAudio();
    clearMediaSession();
    updateResumeUI();
    setTimeout(function () { ttsStopping = false; }, 80);
  }

  function ensureKeepAliveAudio() {
    if (!ttsKeepAwake) return;
    try {
      if (!keepAliveAudio) {
        // Tiny silent wav data URI — keeps media session / audio focus alive on some browsers
        keepAliveAudio = new Audio('data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=');
        keepAliveAudio.loop = true;
        keepAliveAudio.volume = 0.001;
      }
      var p = keepAliveAudio.play();
      if (p && p.catch) p.catch(function () {});
    } catch (e) {}
  }
  function stopKeepAliveAudio() {
    try { if (keepAliveAudio) { keepAliveAudio.pause(); keepAliveAudio.currentTime = 0; } } catch (e) {}
  }
  async function requestWakeLock() {
    if (!ttsKeepAwake || !('wakeLock' in navigator)) return;
    try {
      wakeLockSentinel = await navigator.wakeLock.request('screen');
      wakeLockSentinel.addEventListener('release', function () { wakeLockSentinel = null; });
    } catch (e) { wakeLockSentinel = null; }
  }
  function releaseWakeLock() {
    try { if (wakeLockSentinel) wakeLockSentinel.release(); } catch (e) {}
    wakeLockSentinel = null;
  }
  function setMediaSession(playing) {
    if (!('mediaSession' in navigator)) return;
    try {
      var title = (document.getElementById('r-title') || {}).textContent || 'Biblioteca';
      navigator.mediaSession.metadata = new MediaMetadata({
        title: title,
        artist: 'Les vencimos · lectura',
        album: 'Biblioteca offline'
      });
      navigator.mediaSession.playbackState = playing ? 'playing' : 'paused';
      navigator.mediaSession.setActionHandler('play', function () {
        document.getElementById('tts-play').click();
      });
      navigator.mediaSession.setActionHandler('pause', function () {
        document.getElementById('tts-pause').click();
      });
      navigator.mediaSession.setActionHandler('stop', function () {
        stopTTS(false);
      });
    } catch (e) {}
  }
  function clearMediaSession() {
    if (!('mediaSession' in navigator)) return;
    try { navigator.mediaSession.playbackState = 'none'; } catch (e) {}
  }

  function pauseAllForBackground() {
    // Keep voice+ambient consistent: pause both when OS may kill speech
    if (window.speechSynthesis && (speechSynthesis.speaking || speechSynthesis.paused)) {
      try { speechSynthesis.pause(); } catch (e) {}
      ttsPaused = true;
    }
    if (ambKind) {
      ambKindBeforeHide = ambKind;
      ambPausedByHide = true;
      stopAmb();
    }
    setMediaSession(false);
    document.getElementById('tts-status').textContent =
      'Pausa (pantalla/app en segundo plano). Al volver: Continuar. Android suele cortar speechSynthesis.';
  }

  function onVisibility() {
    if (document.hidden || document.visibilityState === 'hidden') {
      if (ttsWasReading || (window.speechSynthesis && speechSynthesis.speaking)) {
        if (currentId && ttsQueue.length) {
          savePos(currentId, paraStartIdx + Math.max(0, ttsQueueIdx), 0);
        }
        if (ttsKeepAwake) {
          // Best-effort: keep silent audio + try resume loop; still pause ambient with voice
          ensureKeepAliveAudio();
          requestWakeLock();
          // Still pause ambient so it doesn't play alone if speech dies
          if (ambKind) {
            ambKindBeforeHide = ambKind;
            ambPausedByHide = true;
            stopAmb();
          }
          setMediaSession(true);
          document.getElementById('tts-status').textContent =
            'Intentando mantener lectura… (el SO puede cortar la voz; al volver Continuar).';
        } else {
          pauseAllForBackground();
        }
      }
    } else {
      // Visible again
      if (ttsKeepAwake) requestWakeLock();
      if (ambPausedByHide && ambKindBeforeHide) {
        startAmb(ambKindBeforeHide);
        ambPausedByHide = false; ambKindBeforeHide = null;
      }
      if (ttsWasReading && window.speechSynthesis) {
        var dead = !speechSynthesis.speaking && !speechSynthesis.paused && ttsQueue.length && ttsQueueIdx < ttsQueue.length;
        if (dead || ttsPaused) {
          updateResumeUI();
          var btn = document.getElementById('tts-continue');
          if (btn) btn.hidden = false;
          document.getElementById('tts-status').textContent =
            dead
              ? 'La voz se cortó en segundo plano. Pulsa Continuar (¶' + (resumeParaIdx + 1) + ').'
              : 'De vuelta. Pulsa Continuar o Reanudar.';
          // Auto-offer: flash continue; do not silently restart from start
          if (dead) {
            try { btn && btn.focus(); } catch (e) {}
          } else if (ttsPaused) {
            try { speechSynthesis.resume(); ttsPaused = false; setMediaSession(true); } catch (e2) {}
          }
        }
      }
    }
  }
  document.addEventListener('visibilitychange', onVisibility);
  window.addEventListener('pagehide', function () {
    if (currentId && ttsQueue.length) savePos(currentId, paraStartIdx + Math.max(0, ttsQueueIdx), 0);
    if (!ttsKeepAwake) pauseAllForBackground();
  });
  document.addEventListener('freeze', function () {
    if (currentId && ttsQueue.length) savePos(currentId, paraStartIdx + Math.max(0, ttsQueueIdx), 0);
  });"""

    if old_stop not in html:
        raise SystemExit('stopTTS not found')
    html = html.replace(old_stop, new_stop, 1)

    # Update speakChunk onend to save progress
    old_onend = """    u.onend = function () {
      if (ttsStopping) return;
      ttsQueueIdx = idx + 1;
      speakChunk(ttsQueueIdx);
    };"""
    new_onend = """    u.onend = function () {
      if (ttsStopping) return;
      ttsQueueIdx = idx + 1;
      if (currentId) savePos(currentId, paraStartIdx + ttsQueueIdx, 0);
      speakChunk(ttsQueueIdx);
    };"""
    if old_onend not in html:
        raise SystemExit('onend not found')
    html = html.replace(old_onend, new_onend, 1)

    # speakChunk start: mark reading + keepalive
    old_speak_chunk_start = """  function speakChunk(idx) {
    if (ttsStopping) return;
    if (!window.speechSynthesis) {
      document.getElementById('tts-status').textContent = ttsTip('synthesis-unavailable');
      return;
    }
    if (idx >= ttsQueue.length) {
      document.getElementById('tts-status').textContent = 'Fin.';
      ttsUtter = null;
      ttsRetry = {};
      if (ttsWatch) { clearInterval(ttsWatch); ttsWatch = null; }
      return;
    }"""
    new_speak_chunk_start = """  function speakChunk(idx) {
    if (ttsStopping) return;
    if (!window.speechSynthesis) {
      document.getElementById('tts-status').textContent = ttsTip('synthesis-unavailable');
      return;
    }
    if (idx >= ttsQueue.length) {
      document.getElementById('tts-status').textContent = 'Fin.';
      ttsUtter = null;
      ttsRetry = {};
      ttsWasReading = false;
      if (ttsWatch) { clearInterval(ttsWatch); ttsWatch = null; }
      releaseWakeLock();
      stopKeepAliveAudio();
      clearMediaSession();
      if (currentId) savePos(currentId, paras.length ? paras.length - 1 : 0, 0);
      return;
    }
    ttsWasReading = true;
    ensureKeepAliveAudio();
    requestWakeLock();
    setMediaSession(true);"""
    if old_speak_chunk_start not in html:
        raise SystemExit('speakChunk start not found')
    html = html.replace(old_speak_chunk_start, new_speak_chunk_start, 1)

    # speakText signature + paraStart
    old_speak_text = """  function speakText(text) {
    if (!window.speechSynthesis) {
      document.getElementById('tts-status').textContent = ttsTip('synthesis-unavailable');
      return;
    }
    // Natural pack must NEVER gate system TTS
    ttsStopping = true;
    speechSynthesis.cancel();
    ttsRetry = {};
    ttsQueue = chunkText(text);
    ttsQueueIdx = 0;
    ttsActiveText = text || '';
    ttsSfxCursor = 0;"""
    new_speak_text = """  function speakText(text, opts) {
    opts = opts || {};
    if (!window.speechSynthesis) {
      document.getElementById('tts-status').textContent = ttsTip('synthesis-unavailable');
      return;
    }
    // Natural pack must NEVER gate system TTS
    ttsStopping = true;
    speechSynthesis.cancel();
    ttsRetry = {};
    paraStartIdx = opts.paraStart || 0;
    ttsQueue = chunkText(text);
    ttsQueueIdx = Math.max(0, opts.chunkOff || 0);
    if (ttsQueueIdx >= ttsQueue.length) ttsQueueIdx = 0;
    ttsActiveText = text || '';
    ttsSfxCursor = 0;
    ttsWasReading = true;
    if (currentId) savePos(currentId, paraStartIdx + ttsQueueIdx, 0);
    ensureKeepAliveAudio();
    requestWakeLock();
    setMediaSession(true);"""
    if old_speak_text not in html:
        raise SystemExit('speakText not found')
    html = html.replace(old_speak_text, new_speak_text, 1)

    # Also fix speakChunk(0) calls inside speakText to use ttsQueueIdx
    html = html.replace(
        """          ttsStopping = false;
          speakChunk(0);
        }
      }, 150);
    } else {
      // Small delay after cancel() avoids Chrome "interrupted" ghost errors
      setTimeout(function () {
        ttsStopping = false;
        speakChunk(0);
      }, 60);
    }""",
        """          ttsStopping = false;
          speakChunk(ttsQueueIdx);
        }
      }, 150);
    } else {
      // Small delay after cancel() avoids Chrome "interrupted" ghost errors
      setTimeout(function () {
        ttsStopping = false;
        speakChunk(ttsQueueIdx);
      }, 60);
    }""",
        1,
    )

    # Replace play / pause / stop handlers
    old_handlers = """  document.getElementById('tts-play').addEventListener('click', function () {
    if (!currentText) {
      document.getElementById('tts-status').textContent = 'Elige primero un libro.';
      return;
    }
    if (ttsPaused && window.speechSynthesis) {
      try { speechSynthesis.resume(); } catch (e) {}
      ttsPaused = false;
      document.getElementById('tts-status').textContent = 'Reanudado…';
      return;
    }
    speakText(currentText);
  });
  document.getElementById('tts-pause').addEventListener('click', function () {
    if (!window.speechSynthesis) return;
    if (speechSynthesis.speaking && !speechSynthesis.paused) {
      speechSynthesis.pause(); ttsPaused = true;
      document.getElementById('tts-status').textContent = 'Pausa.';
    } else if (ttsPaused) {
      speechSynthesis.resume(); ttsPaused = false;
      document.getElementById('tts-status').textContent = 'Reanudado…';
    }
  });
  document.getElementById('tts-stop').addEventListener('click', stopTTS);"""

    new_handlers = """  document.getElementById('tts-play').addEventListener('click', function () {
    if (!currentText) {
      document.getElementById('tts-status').textContent = 'Elige primero un libro.';
      return;
    }
    if (ttsPaused && window.speechSynthesis) {
      try { speechSynthesis.resume(); } catch (e) {}
      ttsPaused = false;
      ttsWasReading = true;
      setMediaSession(true);
      ensureKeepAliveAudio();
      document.getElementById('tts-status').textContent = 'Reanudado…';
      return;
    }
    // Default Play resumes saved position if any
    if (resumeParaIdx > 0 && resumeParaIdx < paras.length) {
      speakText(paras.slice(resumeParaIdx).join('\\n\\n'), { paraStart: resumeParaIdx, chunkOff: resumeChunkOff });
      document.getElementById('tts-status').textContent = 'Continúo desde ¶' + (resumeParaIdx + 1) + '…';
      return;
    }
    speakText(currentText, { paraStart: 0, chunkOff: 0 });
  });
  var contBtn = document.getElementById('tts-continue');
  if (contBtn) contBtn.addEventListener('click', function () {
    if (!paras.length) return;
    var i = Math.min(resumeParaIdx, paras.length - 1);
    speakText(paras.slice(i).join('\\n\\n'), { paraStart: i, chunkOff: resumeChunkOff });
  });
  var startBtn = document.getElementById('tts-from-start');
  if (startBtn) startBtn.addEventListener('click', function () {
    if (!currentText) return;
    savePos(currentId, 0, 0);
    speakText(currentText, { paraStart: 0, chunkOff: 0 });
  });
  var keepCb = document.getElementById('tts-keep-awake');
  if (keepCb) {
    keepCb.checked = !!ttsKeepAwake;
    keepCb.addEventListener('change', function () {
      ttsKeepAwake = !!keepCb.checked;
      localStorage.setItem(LS_KEEP, ttsKeepAwake ? '1' : '0');
      if (ttsKeepAwake) { ensureKeepAliveAudio(); requestWakeLock(); }
      else { releaseWakeLock(); stopKeepAliveAudio(); }
    });
  }
  document.getElementById('tts-pause').addEventListener('click', function () {
    if (!window.speechSynthesis) return;
    if (speechSynthesis.speaking && !speechSynthesis.paused) {
      speechSynthesis.pause(); ttsPaused = true;
      if (currentId && ttsQueue.length) savePos(currentId, paraStartIdx + ttsQueueIdx, 0);
      setMediaSession(false);
      document.getElementById('tts-status').textContent = 'Pausa.';
    } else if (ttsPaused) {
      speechSynthesis.resume(); ttsPaused = false;
      setMediaSession(true);
      document.getElementById('tts-status').textContent = 'Reanudado…';
    }
  });
  document.getElementById('tts-stop').addEventListener('click', function () { stopTTS(false); });"""

    if old_handlers not in html:
        raise SystemExit('tts handlers not found')
    html = html.replace(old_handlers, new_handlers, 1)

    # ── 5) Richer SFX_MAP + playSfx kinds + ambient interiores/muchedumbre/tormenta ──
    old_sfx_map = """  var SFX_MAP = [
    { re: /caballos?|galope|jinete|troc[eé]|relinch/i, kind: 'caballos' },
    { re: /truenos?|tormenta|rel[aá]mpago|tempestad|rayo/i, kind: 'trueno' },
    { re: /lluvia|llovizna|aguacero|chaparr[oó]n/i, kind: 'lluvia' },
    { re: /\\bmar\\b|olas?|oc[eé]ano|oleaje|playa|nav[ií]o|bergant[ií]n|velero/i, kind: 'mar' },
    { re: /bosque|p[aá]jaros?|hayas?|encinas?|selva/i, kind: 'bosque' },
    { re: /viento|vendaval|brisa|hurac[aá]n|temporal/i, kind: 'viento' },
    { re: /fuego|hoguera|llamaradas?|brasas?|incendio|antorcha/i, kind: 'fuego' },
    { re: /lobos?|aullido/i, kind: 'lobo' },
    { re: /\\br[ií]o\\b|arroyo|corriente|cascada/i, kind: 'rio' },
    { re: /grillos?|noche quieta|nocturno/i, kind: 'grillos' },
    { re: /port[aá]n|puerta|cerr[oó]|golpe[oó] la puerta/i, kind: 'puerta' },
    { re: /campanas?|campanario|ta[nñ]ido/i, kind: 'campana' },
    { re: /lluvia sobre el tejado|tejado|gotera/i, kind: 'tejado' },
    { re: /espada|acero|choque de armas|esgrima/i, kind: 'espada' },
    { re: /caballo|roc[ií]n/i, kind: 'caballos' }
  ];"""

    new_sfx_map = """  var SFX_MAP = [
    { re: /muchedumbre|multitud|plaza|mercado|feria|vocer[ií]o|alboroto|gent[ií]o|bullicio|coro de voces/i, kind: 'muchedumbre' },
    { re: /sal[oó]n|c[aá]mara|estancia|habitaci[oó]n|despacho|interior|pasillo|escalera de madera|tablones|ecos? en la sala|biblioteca/i, kind: 'interiores' },
    { re: /pasos en (la )?madera|cruj(?:i[oó]|en|ir) (?:el|la|los|las)? ?tabl|piso de madera/i, kind: 'pasos' },
    { re: /caballos?|galope|jinete|troc[eé]|relinch|roc[ií]n/i, kind: 'caballos' },
    { re: /truenos?|tormenta|rel[aá]mpago|tempestad|rayo|tormentoso/i, kind: 'trueno' },
    { re: /lluvia|llovizna|aguacero|chaparr[oó]n/i, kind: 'lluvia' },
    { re: /\\bmar\\b|olas?|oc[eé]ano|oleaje|playa|nav[ií]o|bergant[ií]n|velero|puerto/i, kind: 'mar' },
    { re: /bosque|p[aá]jaros?|hayas?|encinas?|selva|arboleda/i, kind: 'bosque' },
    { re: /viento|vendaval|brisa|hurac[aá]n|temporal|rafaga|ráfaga/i, kind: 'viento' },
    { re: /fuego|hoguera|llamaradas?|brasas?|incendio|antorcha|chimenea/i, kind: 'fuego' },
    { re: /lobos?|aullido/i, kind: 'lobo' },
    { re: /\\br[ií]o\\b|arroyo|corriente|cascada|riachuelo/i, kind: 'rio' },
    { re: /grillos?|noche quieta|nocturno|\\bnoche\\b|oscuridad|penumbra/i, kind: 'grillos' },
    { re: /port[aá]n|puerta|cerr[oó]|golpe[oó] la puerta|aldaba|cerradura/i, kind: 'puerta' },
    { re: /campanas?|campanario|ta[nñ]ido|repique/i, kind: 'campana' },
    { re: /tejado|gotera|canal[oó]n/i, kind: 'tejado' },
    { re: /espada|acero|choque de armas|esgrima|sable|estoque/i, kind: 'espada' }
  ];"""

    if old_sfx_map not in html:
        raise SystemExit('SFX_MAP not found')
    html = html.replace(old_sfx_map, new_sfx_map, 1)

    # Extend playSfx with new kinds before status line
    old_espada = """    } else if (kind === 'espada') {
      burstNoise(0.18, 'highpass', 2400, 0.35, 1.2);
      tone(1200, 0.12, 'triangle', 0.15);
    }
    document.getElementById('sfx-status').textContent = 'Efecto: ' + kind;"""

    new_espada = """    } else if (kind === 'espada') {
      burstNoise(0.18, 'highpass', 2400, 0.35, 1.2);
      tone(1200, 0.12, 'triangle', 0.15);
      setTimeout(function () { if (AC) burstNoise(0.12, 'highpass', 3200, 0.2, 1.4); }, 90);
    } else if (kind === 'interiores') {
      // soft room tone + wood creak
      burstNoise(0.9, 'lowpass', 280, 0.18, 0.5);
      tone(140, 0.35, 'triangle', 0.08);
      setTimeout(function () {
        if (!AC) return;
        burstNoise(0.2, 'bandpass', 900, 0.12, 1.1);
        tone(220, 0.15, 'sine', 0.05);
      }, 220);
    } else if (kind === 'pasos') {
      for (var pi = 0; pi < 4; pi++) {
        (function (d) {
          setTimeout(function () {
            if (!AC) return;
            burstNoise(0.08, 'lowpass', 160, 0.35, 0.9);
            tone(70 + Math.random() * 20, 0.07, 'triangle', 0.2);
          }, d);
        })(pi * 160);
      }
    } else if (kind === 'muchedumbre') {
      // layered murmur: several noise bands + random chirps as "voices"
      burstNoise(1.4, 'bandpass', 500, 0.22, 0.4);
      setTimeout(function () { if (AC) burstNoise(1.1, 'bandpass', 900, 0.14, 0.5); }, 80);
      for (var vi = 0; vi < 7; vi++) {
        (function (d) {
          setTimeout(function () {
            if (!AC) return;
            tone(280 + Math.random() * 520, 0.08 + Math.random() * 0.1, 'sine', 0.04);
          }, d);
        })(100 + vi * 130);
      }
    }
    document.getElementById('sfx-status').textContent = 'Efecto: ' + kind;"""

    if old_espada not in html:
        raise SystemExit('espada block not found')
    html = html.replace(old_espada, new_espada, 1)

    # Allow multiple SFX triggers per chunk (muchedumbre + puerta etc.) — change break to allow 2
    old_trig = """  function triggerSfxFromText(text) {
    if (!sfxOn || !text) return;
    for (var i = 0; i < SFX_MAP.length; i++) {
      if (SFX_MAP[i].re.test(text)) {
        playSfx(SFX_MAP[i].kind);
        break;
      }
    }
  }"""
    new_trig = """  function triggerSfxFromText(text) {
    if (!sfxOn || !text) return;
    var hit = 0;
    for (var i = 0; i < SFX_MAP.length; i++) {
      if (SFX_MAP[i].re.test(text)) {
        playSfx(SFX_MAP[i].kind);
        hit++;
        if (hit >= 2) break;
      }
    }
  }"""
    if old_trig not in html:
        raise SystemExit('triggerSfx not found')
    html = html.replace(old_trig, new_trig, 1)

    # Ambient: add interiores, muchedumbre, tormenta before src.start()
    old_amb_end = """    } else if (kind === 'viento') {
      filter.type = 'bandpass'; filter.frequency.value = 500; filter.Q.value = 0.25; gain.gain.value = 0.3;
      var lfo2 = AC.createOscillator(); var lfoG2 = AC.createGain();
      lfo2.frequency.value = 0.12; lfoG2.gain.value = 0.12;
      lfo2.connect(lfoG2); lfoG2.connect(gain.gain); lfo2.start(); ambNodes.push(lfo2, lfoG2);
    }
    src.start();"""

    new_amb_end = """    } else if (kind === 'viento') {
      filter.type = 'bandpass'; filter.frequency.value = 500; filter.Q.value = 0.25; gain.gain.value = 0.3;
      var lfo2 = AC.createOscillator(); var lfoG2 = AC.createGain();
      lfo2.frequency.value = 0.12; lfoG2.gain.value = 0.12;
      lfo2.connect(lfoG2); lfoG2.connect(gain.gain); lfo2.start(); ambNodes.push(lfo2, lfoG2);
    } else if (kind === 'tormenta') {
      filter.type = 'lowpass'; filter.frequency.value = 700; gain.gain.value = 0.45;
      var hpfT = AC.createBiquadFilter(); hpfT.type = 'highpass'; hpfT.frequency.value = 300;
      src.disconnect(); src.connect(hpfT); hpfT.connect(filter); ambNodes.push(hpfT);
      crackTimer = setInterval(function () {
        if (ambKind !== 'tormenta' || !AC) return;
        if (Math.random() > 0.55) return;
        var t0 = AC.currentTime;
        var src2 = AC.createBufferSource(); src2.buffer = noiseBuffer(0.9);
        var f2 = AC.createBiquadFilter(); f2.type = 'lowpass'; f2.frequency.value = 160;
        var g2 = AC.createGain();
        g2.gain.setValueAtTime(0.0001, t0);
        g2.gain.exponentialRampToValueAtTime(0.55, t0 + 0.02);
        g2.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.8);
        src2.connect(f2); f2.connect(g2); g2.connect(masterAmb);
        src2.start(t0); src2.stop(t0 + 0.85);
      }, 2800);
    } else if (kind === 'interiores') {
      filter.type = 'lowpass'; filter.frequency.value = 380; filter.Q.value = 0.7; gain.gain.value = 0.16;
      // soft room hum
      var hum = AC.createOscillator(); var humG = AC.createGain();
      hum.type = 'sine'; hum.frequency.value = 85; humG.gain.value = 0.03;
      hum.connect(humG); humG.connect(masterAmb); hum.start(); ambNodes.push(hum, humG);
      crackTimer = setInterval(function () {
        if (ambKind !== 'interiores' || !AC) return;
        if (Math.random() > 0.4) return;
        var o = AC.createOscillator(); var g = AC.createGain(); var f = AC.createBiquadFilter();
        f.type = 'bandpass'; f.frequency.value = 700 + Math.random() * 400; f.Q.value = 1.2;
        o.type = 'triangle'; o.frequency.value = 120 + Math.random() * 40;
        g.gain.setValueAtTime(0.0001, AC.currentTime);
        g.gain.exponentialRampToValueAtTime(0.08, AC.currentTime + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, AC.currentTime + 0.25);
        o.connect(f); f.connect(g); g.connect(masterAmb); o.start(); o.stop(AC.currentTime + 0.28);
      }, 2200);
    } else if (kind === 'muchedumbre') {
      filter.type = 'bandpass'; filter.frequency.value = 650; filter.Q.value = 0.35; gain.gain.value = 0.28;
      var srcB = AC.createBufferSource(); srcB.buffer = noiseBuffer(2.5); srcB.loop = true;
      var fB = AC.createBiquadFilter(); fB.type = 'bandpass'; fB.frequency.value = 1100; fB.Q.value = 0.5;
      var gB = AC.createGain(); gB.gain.value = 0.18;
      srcB.connect(fB); fB.connect(gB); gB.connect(masterAmb); srcB.start(); ambNodes.push(srcB, fB, gB);
      birdTimer = setInterval(function () {
        if (ambKind !== 'muchedumbre' || !AC) return;
        var o = AC.createOscillator(); var g = AC.createGain();
        o.type = 'sine'; o.frequency.value = 260 + Math.random() * 600;
        g.gain.setValueAtTime(0.0001, AC.currentTime);
        g.gain.exponentialRampToValueAtTime(0.05, AC.currentTime + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, AC.currentTime + 0.12);
        o.connect(g); g.connect(masterAmb); o.start(); o.stop(AC.currentTime + 0.14);
      }, 280);
    }
    src.start();"""

    if old_amb_end not in html:
        raise SystemExit('amb end not found')
    html = html.replace(old_amb_end, new_amb_end, 1)

    if html == orig:
        raise SystemExit('no changes applied')
    HTML.write_text(html, encoding="utf-8")
    print('patched biblioteca.html', len(orig), '->', len(html))

if __name__ == '__main__':
    main()
