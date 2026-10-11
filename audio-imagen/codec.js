// Imagen -> audio. Cada "acorde" = 6 voces simultaneas, 16 tonos posibles por voz.
// 16^6 = 16.777.216 variaciones por acorde = 24 bits = 3 bytes por acorde.
(function (root) {
  const VOICES = 6, LEVELS = 16, BASE = 1000, BAND = 1000, STEP = 50;
  const freq = (v, k) => BASE + v * BAND + k * STEP;
  const SYNC = [0, 15, 0, 15, 0, 15]; // acorde de sincronia
  const MAGIC = [0x49, 0x4d];

  function crc16(b) {
    let c = 0xffff;
    for (const x of b) { c ^= x << 8; for (let i = 0; i < 8; i++) c = c & 0x8000 ? ((c << 1) ^ 0x1021) & 0xffff : (c << 1) & 0xffff; }
    return c;
  }
  // gray: Uint8Array w*h (0..255) -> bytes de paquete
  function packImage(gray, w, h) {
    const px = new Uint8Array(Math.ceil(w * h / 2));
    for (let i = 0; i < w * h; i++) {
      const q = gray[i] >> 4;
      px[i >> 1] |= i & 1 ? q : q << 4;
    }
    const body = [...MAGIC, w, h, ...px];
    const c = crc16(body);
    const all = [...body, c >> 8, c & 255];
    while (all.length % 3) all.push(0);
    return Uint8Array.from(all);
  }
  function unpackImage(bytes) {
    if (bytes[0] !== MAGIC[0] || bytes[1] !== MAGIC[1]) return null;
    const w = bytes[2], h = bytes[3], n = Math.ceil(w * h / 2), end = 4 + n;
    if (!w || !h || bytes.length < end + 2) return null;
    const c = crc16(bytes.subarray(0, end));
    if (c !== ((bytes[end] << 8) | bytes[end + 1])) return null;
    const gray = new Uint8Array(w * h);
    for (let i = 0; i < w * h; i++) {
      const b = bytes[4 + (i >> 1)], q = i & 1 ? b & 15 : b >> 4;
      gray[i] = q * 17;
    }
    return { w, h, gray };
  }
  // 3 bytes -> 6 nibbles (un acorde)
  function bytesToChords(bytes) {
    const out = [SYNC, SYNC];
    for (let i = 0; i < bytes.length; i += 3) {
      const v = (bytes[i] << 16) | (bytes[i + 1] << 8) | bytes[i + 2];
      out.push([0, 1, 2, 3, 4, 5].map(j => (v >> (20 - 4 * j)) & 15));
    }
    return out;
  }
  function chordsToBytes(chords) {
    const out = [];
    for (const c of chords) {
      let v = 0;
      for (let j = 0; j < 6; j++) v = (v << 4) | c[j];
      out.push((v >> 16) & 255, (v >> 8) & 255, v & 255);
    }
    return Uint8Array.from(out);
  }
  function synth(chords, sr, symSec) {
    const n = Math.round(sr * symSec), out = new Float32Array(n * chords.length);
    const fade = Math.round(n * 0.1);
    chords.forEach((ch, s) => {
      for (let v = 0; v < VOICES; v++) {
        const w = 2 * Math.PI * freq(v, ch[v]) / sr;
        for (let i = 0; i < n; i++) {
          const e = Math.min(1, i / fade, (n - 1 - i) / fade);
          out[s * n + i] += Math.sin(w * i) * e / VOICES;
        }
      }
    });
    return out;
  }
  function goertzel(x, start, n, f, sr) {
    const k = 2 * Math.cos(2 * Math.PI * f / sr);
    let a = 0, b = 0;
    for (let i = 0; i < n; i++) { const t = x[start + i] + k * a - b; b = a; a = t; }
    return a * a + b * b - k * a * b;
  }
  function readChord(x, start, n, sr) {
    const ch = [];
    let score = 0;
    for (let v = 0; v < VOICES; v++) {
      let best = 0, bp = -1, tot = 0;
      for (let k = 0; k < LEVELS; k++) {
        const p = goertzel(x, start, n, freq(v, k), sr);
        tot += p;
        if (p > bp) { bp = p; best = k; }
      }
      ch.push(best);
      score += tot ? bp / tot : 0;
    }
    return { ch, score: score / VOICES };
  }
  // Busca el acorde de sincronia y decodifica hasta recibir paquete valido
  function decode(x, sr, symSec) {
    const n = Math.round(sr * symSec), hop = Math.max(1, n >> 4);
    const win = Math.round(n * 0.8), pad = (n - win) >> 1;
    const ok = s => {
      const a = readChord(x, s + pad, win, sr), b = readChord(x, s + n + pad, win, sr);
      return a.score > 0.5 && b.score > 0.5 && a.ch.join() === SYNC.join() && b.ch.join() === SYNC.join();
    };
    let off = -1;
    for (let s = 0; s + 2 * n <= x.length && s < sr * 8; s += hop) {
      if (!ok(s)) continue;
      const m = 2 * n, hop2 = Math.max(1, n >> 6);
      let best = -1;
      for (let t = Math.max(0, s - n); t + m <= x.length && t <= s + n; t += hop2) {
        let p = 0;
        for (let v = 0; v < VOICES; v++) p += goertzel(x, t, m, freq(v, SYNC[v]), sr);
        if (p > best) { best = p; off = t; }
      }
      break;
    }
    if (off < 0) return null;
    const chords = [];
    for (let s = off + 2 * n; s + pad + win <= x.length; s += n) chords.push(readChord(x, s + pad, win, sr).ch);
    const bytes = chordsToBytes(chords);
    return unpackImage(bytes);
  }
  root.AudioImg = { readChord, VOICES, LEVELS, freq, packImage, unpackImage, bytesToChords, chordsToBytes, synth, decode, crc16 };
  if (typeof module !== 'undefined') module.exports = root.AudioImg;
})(typeof window !== 'undefined' ? window : globalThis);
