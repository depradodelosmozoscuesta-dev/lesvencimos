const C = require('./colores.js'), w = 4, h = 2, d = new Uint8Array(w * h * 4);
const set = (p, r, g, b) => d.set([r, g, b, 255], 4 * p);
for (let p = 0; p < 8; p++) set(p, 255, 0, 0);
set(3, 0, 0, 255); set(6, 0, 0, 255); set(7, 10, 20, 30);
const r = C.analyze(d, w, h);
const ok = C.LEVELS ** 3 === 97336 && r.totalPixels === 8 && r.distinctColors === 3 &&
  r.colors[0].count === 5 && JSON.stringify(r.colors[1].pixels) === '[{"x":3,"y":0},{"x":2,"y":1}]';
console.log(ok ? 'OK' : 'FAIL', r.totalPixels, r.distinctColors); process.exit(ok ? 0 : 1);
