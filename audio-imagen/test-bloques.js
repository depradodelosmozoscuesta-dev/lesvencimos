const B = require('./bloques.js'), w = 67, h = 45, d = new Uint8Array(w * h * 4); // no multiplo de 8
for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
  const p = 4 * (y * w + x), lum = 255 - x * 3; // luz lateral: degradado de derecha a izquierda
  d.set(y > 30 && x < 20 ? [(x * 37 + y * 11) % 256, (x * y) % 256, (x ^ y) * 5 % 256, 255] : [lum, lum * .8, lum * .5, 255], p);
}
const s = B.encode(d, w, h), q = B.quantize(d, w, h), r = B.decode(s, w, h);
const exact = q.every((v, i) => v === r[i]), max = Math.max(...s);
const ok = exact && max < 2 ** 24;
console.log(ok ? 'OK' : 'FAIL', 'pixeles', w * h, 'simbolos', s.length);
process.exit(ok ? 0 : 1);
