'use strict';
(function (global) {
  var ctxFn = function () { return null; };
  var destFn = function () { return null; };
  var montado = false;
  var ambiente = null;
  var fondo = null;

  function ctx() { return ctxFn(); }
  function dest() { return destFn(); }
  function $(id) { return document.getElementById(id); }
  function ahora() {
    var c = ctx();
    return c ? c.currentTime : 0;
  }
  function cajaFondo() {
    return $('fondo') || $('fondos');
  }

  function ruidoBuf() {
    var c = ctx();
    if (!c) return null;
    if (ruidoBuf.buf && ruidoBuf.buf.sampleRate === c.sampleRate) return ruidoBuf.buf;
    var n = c.sampleRate * 2;
    var b = c.createBuffer(1, n, c.sampleRate);
    var d = b.getChannelData(0);
    var i;
    for (i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
    ruidoBuf.buf = b;
    return b;
  }

  function env(g, t0, ataque, cuerpo, cola, pico) {
    var t = Math.max(ahora(), t0);
    var nivel = pico || 1;
    g.gain.cancelScheduledValues(t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(nivel, t + Math.max(0.004, ataque));
    g.gain.setValueAtTime(nivel, t + ataque + Math.max(0, cuerpo));
    g.gain.exponentialRampToValueAtTime(0.0001, t + ataque + cuerpo + Math.max(0.02, cola));
  }

  function soplo(t0, dur, freq, q, pico) {
    var c = ctx();
    var d = dest();
    if (!c || !d) return;
    var src = c.createBufferSource();
    src.buffer = ruidoBuf();
    src.loop = true;
    var bp = c.createBiquadFilter();
    bp.type = 'bandpass';
    bp.frequency.value = freq;
    bp.Q.value = q || 1;
    var g = c.createGain();
    src.connect(bp);
    bp.connect(g);
    g.connect(d);
    env(g, t0, 0.008, Math.max(0.01, dur * 0.55), Math.max(0.04, dur * 0.4), pico || 0.4);
    var t = Math.max(ahora(), t0);
    src.start(t);
    src.stop(t + dur + 0.25);
  }

  function tono(t0, dur, f0, f1, tipo, pico) {
    var c = ctx();
    var d = dest();
    if (!c || !d) return null;
    var o = c.createOscillator();
    o.type = tipo || 'sine';
    var g = c.createGain();
    o.connect(g);
    g.connect(d);
    var t = Math.max(ahora(), t0);
    o.frequency.setValueAtTime(Math.max(30, f0), t);
    if (f1 != null && f1 !== f0) o.frequency.exponentialRampToValueAtTime(Math.max(30, f1), t + Math.max(0.02, dur));
    env(g, t0, 0.01, Math.max(0.02, dur * 0.55), Math.max(0.03, dur * 0.4), pico || 0.16);
    o.start(t);
    o.stop(t + dur + 0.06);
    return o;
  }

  function rafaga(t0, veces, cada, fn) {
    var i;
    for (i = 0; i < veces; i++) fn(t0 + i * cada, i);
  }

  function pararAmbiente() {
    var a = ambiente;
    ambiente = null;
    if (a) {
      a.vivo = false;
      if (a.timer) clearInterval(a.timer);
      (a.nodos || []).forEach(function (n) {
        try { if (n.stop) n.stop(); } catch (e) {}
        try { if (n.disconnect) n.disconnect(); } catch (e2) {}
      });
    }
    var et = $('ambiente-activa');
    if (et) et.textContent = 'Ambiente: ninguno';
  }

  function abrirAmbiente(id, nombre) {
    if (ambiente && ambiente.vivo && ambiente.id === id) {
      pararAmbiente();
      return false;
    }
    pararAmbiente();
    ambiente = { id: id, vivo: true, timer: null, nodos: [] };
    var et = $('ambiente-activa');
    if (et) et.textContent = 'Ambiente: ' + nombre;
    return true;
  }

  function ruidoVivo(freq, q, tipo, gan) {
    var c = ctx();
    var d = dest();
    var src = c.createBufferSource();
    src.buffer = ruidoBuf();
    src.loop = true;
    var f = c.createBiquadFilter();
    f.type = tipo;
    f.frequency.value = freq;
    f.Q.value = q;
    var g = c.createGain();
    g.gain.value = gan;
    src.connect(f);
    f.connect(g);
    g.connect(d);
    src.start();
    return { src: src, filtro: f, g: g };
  }

  function pararFondo() {
    var f = fondo;
    fondo = null;
    if (f) {
      f.on = false;
      if (f.timer) clearTimeout(f.timer);
      (f.oscs || []).forEach(function (o) {
        try { o.stop(); } catch (e) {}
      });
    }
    var et = $('fondo-activa');
    if (et) et.textContent = 'Fondo: ninguno';
  }

  function notaFondo(bus, t, dur, freq, tipo, pico, armonico) {
    var c = ctx();
    var o = c.createOscillator();
    var g = c.createGain();
    o.type = tipo || 'sine';
    o.frequency.setValueAtTime(freq, t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(Math.max(0.0002, pico), t + Math.min(0.04, dur * 0.35));
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g);
    g.connect(bus);
    o.start(t);
    o.stop(t + dur + 0.04);
    if (fondo) fondo.oscs.push(o);
    if (armonico) {
      var o2 = c.createOscillator();
      var g2 = c.createGain();
      o2.type = 'sine';
      o2.frequency.setValueAtTime(freq * 2, t);
      g2.gain.setValueAtTime(0.0001, t);
      g2.gain.exponentialRampToValueAtTime(Math.max(0.0002, pico * 0.22), t + 0.03);
      g2.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o2.connect(g2);
      g2.connect(bus);
      o2.start(t);
      o2.stop(t + dur + 0.04);
      if (fondo) fondo.oscs.push(o2);
    }
  }

  function bucleFondo(id, nombre, avanzar) {
    var c = ctx();
    var d = dest();
    if (!c || !d) return;
    if (fondo && fondo.on && fondo.id === id) {
      pararFondo();
      return;
    }
    pararFondo();
    var bus = c.createGain();
    bus.gain.value = 0.16;
    bus.connect(d);
    var vivo = { id: id, on: true, timer: null, oscs: [], bus: bus, cursor: c.currentTime + 0.05, paso: 0 };
    fondo = vivo;
    var et = $('fondo-activa');
    if (et) et.textContent = 'Fondo: ' + nombre;
    function tick() {
      if (!vivo.on || fondo !== vivo) return;
      var horizonte = ctx().currentTime + 0.6;
      var guard = 0;
      while (vivo.cursor < horizonte && guard < 32) {
        vivo.cursor += avanzar(vivo.cursor, vivo);
        guard += 1;
      }
      if (vivo.oscs.length > 64) vivo.oscs.splice(0, vivo.oscs.length - 32);
      vivo.timer = setTimeout(tick, 150);
    }
    tick();
  }

  function tocarFondo(id) {
    if (id === 'historia') {
      var frase = [293.66, 440, 523.25, 587.33, 523.25, 440, 392, 349.23, 329.63, 293.66];
      bucleFondo(id, 'Flauta medieval', function (t, vivo) {
        var i = vivo.paso % frase.length;
        var fin = i === frase.length - 1;
        vivo.paso += 1;
        notaFondo(vivo.bus, t, fin ? 0.52 : 0.36, frase[i], 'sine', 0.55, true);
        return fin ? 1.1 : 0.4;
      });
    } else if (id === 'improvisacion') {
      var jig = [293.66, 349.23, 440, 587.33, 440, 349.23, 392, 493.88, 587.33, 440, 349.23, 293.66, 523.25, 440, 349.23, 392, 329.63, 293.66];
      bucleFondo(id, 'Aire irlandés', function (t, vivo) {
        var f = jig[vivo.paso % jig.length];
        vivo.paso += 1;
        notaFondo(vivo.bus, t, 0.12, f, 'sine', 0.42, false);
        return 0.145;
      });
    } else if (id === 'emotivo') {
      bucleFondo(id, 'Nota grave', function (t, vivo) {
        notaFondo(vivo.bus, t, 5.4, 98, 'sine', 0.5, false);
        notaFondo(vivo.bus, t, 5.4, 146.83, 'sine', 0.12, false);
        return 5.8;
      });
    } else if (id === 'educativo') {
      var tres = [392, 523.25, 659.25];
      bucleFondo(id, 'Cortinilla', function (t, vivo) {
        var i = vivo.paso % 4;
        vivo.paso += 1;
        if (i === 3) return 1.3;
        notaFondo(vivo.bus, t, 0.15, tres[i], 'triangle', 0.4, false);
        return 0.19;
      });
    } else if (id === 'radio') {
      var entrada = [523.25, 659.25, 783.99];
      bucleFondo(id, 'Tono de entrada', function (t, vivo) {
        var i = vivo.paso % 4;
        vivo.paso += 1;
        if (i === 3) return 1.45;
        notaFondo(vivo.bus, t, 0.13, entrada[i], 'sine', 0.38, true);
        return 0.17;
      });
    }
  }

  function efecto(id) {
    if (!ctx() || !dest()) return;
    var t = ahora();
    if (id === 'coche-arranca') { tono(t, 0.9, 55, 150, 'sawtooth', 0.14); soplo(t, 0.75, 160, 0.7, 0.35); tono(t + 0.85, 0.22, 95, 70, 'square', 0.06); }
    else if (id === 'coche-aleja') { tono(t, 1.5, 90, 460, 'sawtooth', 0.1); soplo(t + 0.3, 1.6, 480, 0.45, 0.22); tono(t + 1.6, 1.3, 260, 70, 'sawtooth', 0.05); }
    else if (id === 'lluvia') {
      if (!abrirAmbiente(id, 'Lluvia')) return;
      var r = ruidoVivo(2200, 0.4, 'highpass', 0.1);
      ambiente.nodos.push(r.src, r.filtro, r.g);
    }
    else if (id === 'salpicar') rafaga(t, 5, 0.09, function (tt, i) { soplo(tt, 0.05, 1700 + i * 180, 1.5, 0.4); });
    else if (id === 'punetazo') { soplo(t, 0.06, 130, 0.7, 0.7); tono(t, 0.16, 72, 40, 'sine', 0.32); }
    else if (id === 'oh-yeah') { tono(t, 0.28, 196, 294, 'sine', 0.16); tono(t + 0.3, 0.34, 392, 494, 'triangle', 0.14); }
    else if (id === 'perro') rafaga(t, 3, 0.22, function (tt) { tono(tt, 0.11, 220, 130, 'square', 0.1); soplo(tt, 0.07, 380, 1, 0.25); });
    else if (id === 'eructo') { tono(t, 0.42, 115, 52, 'sawtooth', 0.14); soplo(t, 0.32, 190, 0.8, 0.28); }
    else if (id === 'beso') { soplo(t, 0.05, 1500, 2.2, 0.34); tono(t + 0.04, 0.08, 620, 200, 'sine', 0.08); }
    else if (id === 'grito') tono(t, 0.5, 460, 880, 'sawtooth', 0.1);
    else if (id === 'help') { tono(t, 0.2, 640, 520, 'triangle', 0.14); tono(t + 0.26, 0.2, 500, 400, 'triangle', 0.12); tono(t + 0.52, 0.28, 400, 280, 'sine', 0.11); }
    else if (id === 'viva') { tono(t, 0.48, 340, 740, 'triangle', 0.12); soplo(t, 0.55, 1100, 0.5, 0.24); }
    else if (id === 'risa') rafaga(t, 6, 0.13, function (tt, i) { tono(tt, 0.09, 340 + (i % 2) * 50, 260, 'triangle', 0.1); });
    else if (id === 'risa-lata') rafaga(t, 5, 0.15, function (tt, i) { tono(tt, 0.11, 720 + i * 25, 480, 'square', 0.055); tono(tt, 0.11, 1040, 700, 'square', 0.035); });
    else if (id === 'abucheo') { soplo(t, 1.05, 260, 0.55, 0.34); tono(t, 0.85, 210, 100, 'sawtooth', 0.06); }
    else if (id === 'silbido') tono(t, 0.7, 1500, 880, 'sine', 0.11);
    else if (id === 'timbre') { tono(t, 0.32, 880, 880, 'sine', 0.15); tono(t + 0.26, 0.48, 659, 659, 'sine', 0.13); }
    else if (id === 'telefono') rafaga(t, 3, 0.72, function (tt) { tono(tt, 0.26, 440, 440, 'sine', 0.1); tono(tt, 0.26, 480, 480, 'sine', 0.08); });
    else if (id === 'cristal') { soplo(t, 0.1, 3400, 2, 0.42); rafaga(t + 0.04, 6, 0.04, function (tt, i) { tono(tt, 0.16, 1700 + i * 240, 800, 'sine', 0.06); }); }
    else if (id === 'trueno') { soplo(t, 1.25, 80, 0.35, 0.65); tono(t, 1.05, 48, 32, 'sine', 0.28); }
    else if (id === 'viento') {
      if (!abrirAmbiente(id, 'Viento')) return;
      var v = ruidoVivo(280, 0.55, 'lowpass', 0.14);
      var lfo = ctx().createOscillator();
      var prof = ctx().createGain();
      lfo.frequency.value = 0.13;
      prof.gain.value = 120;
      lfo.connect(prof);
      prof.connect(v.filtro.frequency);
      lfo.start();
      ambiente.nodos.push(v.src, v.filtro, v.g, lfo, prof);
    }
    else if (id === 'olas') {
      if (!abrirAmbiente(id, 'Olas')) return;
      var o = ruidoVivo(160, 0.65, 'lowpass', 0.04);
      var lfo2 = ctx().createOscillator();
      var prof2 = ctx().createGain();
      lfo2.frequency.value = 0.16;
      prof2.gain.value = 0.05;
      lfo2.connect(prof2);
      prof2.connect(o.g.gain);
      lfo2.start();
      ambiente.nodos.push(o.src, o.filtro, o.g, lfo2, prof2);
    }
    else if (id === 'fuego') {
      if (!abrirAmbiente(id, 'Fuego')) return;
      ambiente.timer = setInterval(function () {
        if (!ambiente || ambiente.id !== 'fuego') return;
        soplo(ahora(), 0.03 + Math.random() * 0.05, 350 + Math.random() * 1100, 1.6, 0.2);
      }, 80);
    }
    else if (id === 'pajaros') {
      if (!abrirAmbiente(id, 'Pájaros')) return;
      ambiente.timer = setInterval(function () {
        if (!ambiente || ambiente.id !== 'pajaros') return;
        var f0 = 1500 + Math.random() * 1600;
        tono(ahora(), 0.08, f0, f0 * (0.65 + Math.random() * 0.6), 'sine', 0.05);
      }, 480);
    }
    else if (id === 'gallo') { tono(t, 0.16, 680, 920, 'square', 0.07); tono(t + 0.18, 0.32, 500, 860, 'square', 0.07); tono(t + 0.5, 0.38, 900, 420, 'triangle', 0.06); }
    else if (id === 'gato') tono(t, 0.5, 480, 820, 'sine', 0.1);
    else if (id === 'caballo') rafaga(t, 6, 0.26, function (tt, i) { soplo(tt, 0.045, i % 2 ? 210 : 130, 1.1, 0.42); tono(tt, 0.05, 85, 55, 'sine', 0.12); });
    else if (id === 'bocina') { tono(t, 0.7, 370, 370, 'square', 0.09); tono(t, 0.7, 277, 277, 'sawtooth', 0.05); }
    else if (id === 'freno') { soplo(t, 0.75, 2400, 3, 0.28); tono(t, 0.7, 1900, 380, 'sawtooth', 0.05); }
    else if (id === 'avion') { tono(t, 2.1, 110, 250, 'sawtooth', 0.07); soplo(t, 2.1, 550, 0.4, 0.18); }
    else if (id === 'helicoptero') rafaga(t, 18, 0.1, function (tt) { soplo(tt, 0.06, 110, 1.3, 0.4); tono(tt, 0.05, 68, 52, 'sine', 0.09); });
    else if (id === 'disparo') { soplo(t, 0.035, 2000, 0.7, 0.65); tono(t, 0.1, 95, 38, 'sine', 0.24); }
    else if (id === 'espada') soplo(t, 0.26, 1700, 2.4, 0.32);
    else if (id === 'flecha') { soplo(t, 0.14, 2600, 1.6, 0.28); tono(t, 0.1, 980, 360, 'sine', 0.05); }
    else if (id === 'explosion') { soplo(t, 0.65, 90, 0.35, 0.85); tono(t, 0.55, 46, 28, 'sine', 0.36); soplo(t + 0.04, 0.28, 700, 0.5, 0.28); }
    else if (id === 'campanada') { tono(t, 2.1, 196, 196, 'sine', 0.18); tono(t, 1.5, 392, 392, 'sine', 0.07); tono(t, 1.1, 588, 588, 'triangle', 0.04); }
    else if (id === 'reloj') rafaga(t, 6, 0.48, function (tt, i) { soplo(tt, 0.018, i % 2 ? 2000 : 800, 4, 0.32); });
    else if (id === 'maquina') rafaga(t, 14, 0.1, function (tt, i) { soplo(tt, 0.018, 2800, 3, 0.22); if (i % 5 === 4) soplo(tt + 0.03, 0.05, 380, 1, 0.18); });
    else if (id === 'obturador') { soplo(t, 0.018, 3200, 2, 0.38); soplo(t + 0.055, 0.028, 700, 1, 0.28); }
    else if (id === 'monedas') rafaga(t, 7, 0.065, function (tt, i) { tono(tt, 0.1, 1700 + i * 160, 1100, 'sine', 0.07); });
    else if (id === 'caja') { tono(t, 0.18, 1568, 1568, 'sine', 0.11); tono(t + 0.07, 0.32, 2093, 2093, 'sine', 0.09); soplo(t + 0.14, 0.18, 280, 0.8, 0.22); }
    else if (id === 'corcho') { soplo(t, 0.035, 480, 1, 0.48); tono(t, 0.07, 170, 80, 'sine', 0.14); }
    else if (id === 'brindar') { tono(t, 0.38, 1480, 1480, 'sine', 0.09); tono(t + 0.04, 0.42, 1980, 1980, 'sine', 0.07); }
    else if (id === 'tragar') { tono(t, 0.09, 320, 130, 'sine', 0.15); soplo(t + 0.07, 0.07, 460, 1, 0.18); }
    else if (id === 'palmada') soplo(t, 0.055, 1400, 0.8, 0.5);
    else if (id === 'chasquido') soplo(t, 0.012, 4200, 3.2, 0.42);
    else if (id === 'redoble') rafaga(t, 18, 0.045, function (tt, i) { soplo(tt, 0.025, 1900, 1.3, 0.16 + i * 0.012); });
    else if (id === 'platillo') soplo(t, 1.05, 5200, 0.55, 0.26);
    else if (id === 'tambor') { tono(t, 0.18, 78, 48, 'sine', 0.28); soplo(t, 0.04, 180, 1, 0.28); }
    else if (id === 'trompeta') { tono(t, 0.18, 523, 523, 'square', 0.06); tono(t + 0.2, 0.18, 659, 659, 'square', 0.06); tono(t + 0.4, 0.4, 784, 784, 'sawtooth', 0.055); }
    else if (id === 'sad') { tono(t, 0.32, 466, 415, 'sawtooth', 0.07); tono(t + 0.3, 0.32, 392, 349, 'sawtooth', 0.065); tono(t + 0.6, 0.48, 311, 247, 'triangle', 0.06); }
    else if (id === 'riser') tono(t, 1.35, 160, 2400, 'sawtooth', 0.07);
    else if (id === 'exito') { tono(t, 0.65, 523, 523, 'triangle', 0.11); tono(t, 0.75, 659, 659, 'sine', 0.09); tono(t, 0.85, 784, 784, 'sine', 0.07); }
    else if (id === 'fracaso') { tono(t, 0.22, 440, 440, 'square', 0.07); tono(t + 0.2, 0.38, 294, 196, 'sawtooth', 0.07); }
    else if (id === 'heartbeat') { tono(t, 0.09, 58, 42, 'sine', 0.32); tono(t + 0.16, 0.11, 48, 34, 'sine', 0.26); }
    else if (id === 'respiracion') { soplo(t, 0.65, 650, 0.5, 0.2); soplo(t + 0.8, 0.85, 420, 0.4, 0.16); }
    else if (id === 'suspense') { tono(t, 1.15, 440, 446, 'sine', 0.055); tono(t, 1.15, 466, 472, 'sine', 0.045); }
    else if (id === 'laser') tono(t, 0.22, 2000, 160, 'square', 0.07);
    else if (id === 'robot') rafaga(t, 8, 0.09, function (tt, i) { tono(tt, 0.05, 180 + (i % 4) * 110, 180, 'square', 0.07); });
    else if (id === 'burbujas') rafaga(t, 8, 0.11, function (tt, i) { tono(tt, 0.07, 380 + i * 50, 920, 'sine', 0.055); });
    else if (id === 'vater') { rafaga(t, 8, 0.035, function (tt) { soplo(tt, 0.025, 850, 2, 0.28); }); soplo(t + 0.35, 1.05, 220, 0.5, 0.32); }
    else if (id === 'boing') tono(t, 0.42, 300, 80, 'sine', 0.16);
    else if (id === 'flauta') { tono(t, 0.2, 587, 587, 'sine', 0.09); tono(t, 0.2, 1174, 1174, 'sine', 0.025); tono(t + 0.22, 0.2, 659, 659, 'sine', 0.08); tono(t + 0.44, 0.28, 784, 784, 'sine', 0.07); }
    else if (id === 'arpa') { tono(t, 0.48, 262, 262, 'sine', 0.09); tono(t + 0.07, 0.5, 330, 330, 'sine', 0.075); tono(t + 0.14, 0.52, 392, 392, 'sine', 0.06); tono(t + 0.21, 0.58, 523, 523, 'sine', 0.05); }
    else if (id === 'pagina') soplo(t, 0.16, 2400, 0.8, 0.22);
    else if (id === 'pergamino') soplo(t, 0.5, 800, 0.55, 0.26);
    else if (id === 'grada') {
      if (!abrirAmbiente(id, 'Grada')) return;
      var g = ruidoVivo(750, 0.4, 'bandpass', 0.09);
      ambiente.nodos.push(g.src, g.filtro, g.g);
      ambiente.timer = setInterval(function () {
        if (!ambiente || ambiente.id !== 'grada') return;
        soplo(ahora(), 0.22, 950, 0.55, 0.18);
      }, 1200);
    }
    else if (id === 'pitido') tono(t, 0.18, 1000, 1000, 'sine', 0.11);
    else if (id === 'gol') { tono(t, 0.32, 1700, 2300, 'sine', 0.09); soplo(t, 0.75, 780, 0.4, 0.32); }
    else if (id === 'claqueta') { soplo(t, 0.016, 2600, 2, 0.48); soplo(t + 0.08, 0.026, 1600, 1.4, 0.5); }
  }

  var EFECTOS = [
    ['coche-arranca', 'Coche arranca'],
    ['coche-aleja', 'Coche acelera y se aleja'],
    ['lluvia', 'Lluvia'],
    ['salpicar', 'Salpicar'],
    ['punetazo', 'Puñetazo'],
    ['oh-yeah', 'Oh yeah'],
    ['perro', 'Perro'],
    ['eructo', 'Eructo'],
    ['beso', 'Beso'],
    ['grito', 'Grito'],
    ['help', 'Help'],
    ['viva', 'Viva'],
    ['risa', 'Risa'],
    ['risa-lata', 'Risa de lata'],
    ['abucheo', 'Abucheo'],
    ['silbido', 'Silbido'],
    ['timbre', 'Timbre'],
    ['telefono', 'Teléfono antiguo'],
    ['cristal', 'Cristal roto'],
    ['trueno', 'Trueno'],
    ['viento', 'Viento'],
    ['olas', 'Olas'],
    ['fuego', 'Fuego'],
    ['pajaros', 'Pájaros'],
    ['gallo', 'Gallo'],
    ['gato', 'Gato'],
    ['caballo', 'Caballo'],
    ['bocina', 'Bocina'],
    ['freno', 'Freno'],
    ['avion', 'Avión'],
    ['helicoptero', 'Helicóptero'],
    ['disparo', 'Disparo'],
    ['espada', 'Espada'],
    ['flecha', 'Flecha'],
    ['explosion', 'Explosión'],
    ['campanada', 'Campanada'],
    ['reloj', 'Reloj'],
    ['maquina', 'Máquina de escribir'],
    ['obturador', 'Obturador'],
    ['monedas', 'Monedas'],
    ['caja', 'Caja registradora'],
    ['corcho', 'Corcho'],
    ['brindar', 'Brindar'],
    ['tragar', 'Tragar'],
    ['palmada', 'Palmada'],
    ['chasquido', 'Chasquido'],
    ['redoble', 'Redoble'],
    ['platillo', 'Platillo'],
    ['tambor', 'Tambor'],
    ['trompeta', 'Trompeta'],
    ['sad', 'Sad trombone'],
    ['riser', 'Riser'],
    ['exito', 'Sting de éxito'],
    ['fracaso', 'Sting de fracaso'],
    ['heartbeat', 'Heartbeat'],
    ['respiracion', 'Respiración'],
    ['suspense', 'Suspense'],
    ['laser', 'Láser'],
    ['robot', 'Robot'],
    ['burbujas', 'Burbujas'],
    ['vater', 'Cadena del váter'],
    ['boing', 'Muelle boing'],
    ['flauta', 'Flauta corta'],
    ['arpa', 'Arpa'],
    ['pagina', 'Página'],
    ['pergamino', 'Pergamino'],
    ['grada', 'Grada'],
    ['pitido', 'Pitido'],
    ['gol', 'Gol'],
    ['claqueta', 'Claqueta']
  ];

  var FONDOS = [
    ['historia', 'Flauta medieval'],
    ['improvisacion', 'Aire irlandés'],
    ['emotivo', 'Nota grave'],
    ['educativo', 'Cortinilla'],
    ['radio', 'Tono de entrada']
  ];

  function boton(caja, texto, fn) {
    var b = document.createElement('button');
    b.type = 'button';
    b.textContent = texto;
    b.addEventListener('click', fn);
    caja.appendChild(b);
    return b;
  }

  var pintado = false;
  function avisarApagada(id) {
    var n = $(id);
    if (n) n.textContent = 'Enciende la mesa';
  }
  function listo() {
    return montado && !!ctx() && !!dest();
  }
  function pintar() {
    if (pintado) return;
    var efectos = $('efectos');
    var fondos = cajaFondo();
    if (!efectos && !fondos) return;
    pintado = true;
    if (efectos) {
      EFECTOS.forEach(function (x) {
        var b = boton(efectos, x[1], function () {
          if (!listo()) { avisarApagada('ambiente-activa'); return; }
          efecto(x[0]);
        });
        b.dataset.efecto = x[0];
        b.title = 'Enciende la mesa para oírlo';
      });
    }
    var pararA = $('ambiente-parar');
    if (pararA) pararA.addEventListener('click', pararAmbiente);
    if (fondos) {
      FONDOS.forEach(function (x) {
        var b = boton(fondos, x[1], function () {
          if (!listo()) { avisarApagada('fondo-activa'); return; }
          tocarFondo(x[0]);
        });
        b.dataset.fondo = x[0];
        b.title = 'Enciende la mesa para oírlo';
      });
    }
    var pararF = $('fondo-parar');
    if (pararF) pararF.addEventListener('click', pararFondo);
  }

  function montar(op) {
    if (!op) return;
    ctxFn = op.ctxFn || ctxFn;
    destFn = op.destFn || destFn;
    montado = true;
    pintar();
    var bs = document.querySelectorAll('[data-efecto],[data-fondo]');
    for (var i = 0; i < bs.length; i++) bs[i].removeAttribute('title');
    var a = $('ambiente-activa');
    if (a && a.textContent === 'Enciende la mesa') a.textContent = 'Ambiente: ninguno';
    var f = $('fondo-activa');
    if (f && f.textContent === 'Enciende la mesa') f.textContent = 'Fondo: ninguno';
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', pintar);
    else pintar();
  }

  global.LVEfectos = { montar: montar, pintar: pintar };
})(typeof window !== 'undefined' ? window : globalThis);
