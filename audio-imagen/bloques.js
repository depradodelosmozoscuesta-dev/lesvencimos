// Imagen -> simbolos (acordes de 24 bits) por bloques, en orden de lectura (la posicion se deduce).
// Paleta ~100.000 colores (colores.js). Por bloque: FLAT, GRAD (gradiente exacto), REF (diccionario adaptativo) o RAW.
// Cada simbolo cabe en un acorde (<16.777.216): 2 bits de tipo + 22 de carga.
(function (root) {
  const C = typeof module !== 'undefined' ? require('./colores.js') : root.Colores;
  const L = C.LEVELS, FLAT = 0, GRAD = 1, REF = 2, RAW = 3, SH = 22;
  const sym = (t, v) => t * 2 ** SH + v;
  const chan = i => [(i / (L * L)) | 0, ((i / L) | 0) % L, i % L];
  const unchan = (r, g, b) => (r * L + g) * L + b;
  const pack = d => d.reduce((a, v) => (a << 3) | (v + 4), 0); // 6 pendientes de -4..3
  const unpack = v => [5, 4, 3, 2, 1, 0].map(j => ((v >> (3 * j)) & 7) - 4);

  function quantize(rgba, w, h) {
    const q = new Uint32Array(w * h);
    for (let p = 0; p < w * h; p++) q[p] = C.index(rgba[4 * p], rgba[4 * p + 1], rgba[4 * p + 2]);
    return q;
  }
  function encode(rgba, w, h, B = 8) {
    const q = quantize(rgba, w, h), out = [], dict = new Map();
    for (let by = 0; by < h; by += B) for (let bx = 0; bx < w; bx += B) {
      const bw = Math.min(B, w - bx), bh = Math.min(B, h - by), px = [];
      for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) px.push(q[(by + y) * w + bx + x]);
      const key = bw + ',' + bh + ':' + px.join(',');
      if (dict.has(key)) { out.push(sym(REF, dict.get(key))); continue; }
      dict.set(key, dict.size);
      if (px.every(v => v === px[0])) { out.push(sym(FLAT, px[0])); continue; }
      const base = chan(px[0]), s = [0, 0, 0, 0, 0, 0];
      for (let c = 0; c < 3; c++) {
        if (bw > 1) s[c] = chan(px[1])[c] - base[c];
        if (bh > 1) s[3 + c] = chan(px[bw])[c] - base[c];
      }
      let grad = s.every(v => v >= -4 && v <= 3);
      for (let y = 0; grad && y < bh; y++) for (let x = 0; x < bw && grad; x++) {
        const v = chan(px[y * bw + x]);
        for (let c = 0; c < 3; c++) if (v[c] !== base[c] + s[c] * x + s[3 + c] * y) grad = false;
      }
      if (grad) out.push(sym(GRAD, px[0]), pack(s));
      else out.push(sym(RAW, px.length), ...px);
    }
    return out;
  }
  // devuelve indices de paleta w*h
  function decode(syms, w, h, B = 8) {
    const q = new Uint32Array(w * h), dict = [];
    let i = 0;
    for (let by = 0; by < h; by += B) for (let bx = 0; bx < w; bx += B) {
      const bw = Math.min(B, w - bx), bh = Math.min(B, h - by), s = syms[i++], t = (s / 2 ** SH) | 0, v = s % 2 ** SH;
      let px = [];
      if (t === REF) px = dict[v];
      else {
        if (t === FLAT) px = new Array(bw * bh).fill(v);
        else if (t === GRAD) {
          const base = chan(v), d = unpack(syms[i++]);
          for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++)
            px.push(unchan(...[0, 1, 2].map(c => base[c] + d[c] * x + d[3 + c] * y)));
        } else { px = syms.slice(i, i + v); i += v; }
        dict.push(px);
      }
      for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) q[(by + y) * w + bx + x] = px[y * bw + x];
    }
    return q;
  }
  root.Bloques = { encode, decode, quantize };
  if (typeof module !== 'undefined') module.exports = root.Bloques;
})(typeof window !== 'undefined' ? window : globalThis);
