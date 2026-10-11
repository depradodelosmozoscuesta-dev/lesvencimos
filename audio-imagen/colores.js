// Analisis de color: paleta de 97.336 colores (~100.000: 46 niveles por canal RGB, 46^3).
// Devuelve nº de pixeles, nº de colores distintos y las posiciones de cada color.
(function (root) {
  const LEVELS = 46; // 46^3 = 97.336 (~100.000)
  const q = v => Math.round(v * (LEVELS - 1) / 255);
  const index = (r, g, b) => (q(r) * LEVELS + q(g)) * LEVELS + q(b); // 0..999999
  const toRGB = i => [Math.round((i / (LEVELS * LEVELS) | 0) * 255 / (LEVELS - 1)),
    Math.round((((i / LEVELS) | 0) % LEVELS) * 255 / (LEVELS - 1)), Math.round((i % LEVELS) * 255 / (LEVELS - 1))];
  // rgba: Uint8ClampedArray/Uint8Array RGBA (ImageData.data). Pixeles totalmente transparentes se ignoran.
  function analyze(rgba, w, h) {
    const positions = new Map(); // colorIndex -> [pixelIndex...] (pixel = y*w+x)
    for (let p = 0; p < w * h; p++) {
      if (rgba[4 * p + 3] === 0) continue;
      const c = index(rgba[4 * p], rgba[4 * p + 1], rgba[4 * p + 2]);
      const l = positions.get(c);
      if (l) l.push(p); else positions.set(c, [p]);
    }
    const colors = [...positions].map(([i, l]) => ({
      index: i, rgb: toRGB(i), count: l.length,
      pixels: l.map(p => ({ x: p % w, y: (p / w) | 0 })),
    })).sort((a, b) => b.count - a.count);
    return { width: w, height: h, totalPixels: w * h, distinctColors: colors.length, paletteSize: LEVELS ** 3, colors };
  }
  root.Colores = { LEVELS, index, toRGB, analyze };
  if (typeof module !== 'undefined') module.exports = root.Colores;
})(typeof window !== 'undefined' ? window : globalThis);
