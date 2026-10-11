const A = require('./codec.js');
const w = 16, h = 16, g = new Uint8Array(w * h).map((_, i) => ((i * 7) % 16) * 17);
const sr = 44100, sym = 0.08;
const audio = A.synth(A.bytesToChords(A.packImage(g, w, h)), sr, sym);
const lead = new Float32Array(Math.round(sr * 0.123)), rx = new Float32Array(lead.length + audio.length);
rx.set(audio, lead.length);
for (let i = 0; i < rx.length; i++) rx[i] += (Math.random() - 0.5) * 0.05;
const r = A.decode(rx, sr, sym);
console.log('variaciones por acorde:', 16 ** 6, 'acordes:', A.bytesToChords(A.packImage(g, w, h)).length);
if (!r || r.w !== w || r.h !== h || r.gray.some((v, i) => v !== g[i])) { console.error('FAIL'); process.exit(1); }
console.log('OK');
