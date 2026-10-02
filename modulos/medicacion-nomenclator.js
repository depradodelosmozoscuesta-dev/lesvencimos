/* Les vencimos — cargador/búsqueda Nomenclátor CIMA offline (AEMPS)
 * Atribución obligatoria: «Fuente de la información: Agencia Española de Medicamentos y Productos Sanitarios www.aemps.gob.es» + fecha obtención.
 * Sin fotos AEMPS. Campos oficiales sin transformar.
 * v20261002d
 */
(function (root) {
  'use strict';

  var ATRIBUCION =
    'Fuente de la información: Agencia Española de Medicamentos y Productos Sanitarios www.aemps.gob.es';

  function norm(s) {
    return String(s || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');
  }

  /** Map forma farmacéutica (texto oficial) → clave de placeholder propio (no AEMPS). */
  function formaKey(forma) {
    var f = norm(forma);
    if (!f) return 'otro';
    if (/comprim|tableta|gragea|oblea/.test(f)) return 'comprimido';
    if (/capsul|c[aá]psula/.test(f)) return 'capsula';
    if (/jarabe|solucion oral|suspension oral|gotas orales|elixir|granulado.*oral|polvo.*oral/.test(f)) return 'jarabe';
    if (/crema|pomada|gel|ung[uü]ento|locion|emulsi[oó]n cut|pasta/.test(f)) return 'crema';
    if (/colirio|gotas oft|oftalm/.test(f)) return 'gotas';
    if (/inhal|aerosol|nebul|pulm/.test(f)) return 'inhalador';
    if (/inyect|perfusi[oó]n|jeringa|vial|ampolla|implante/.test(f)) return 'inyeccion';
    if (/parche|transd[eé]rm/.test(f)) return 'parche';
    if (/sobre|polvo para|granulado/.test(f)) return 'sobre';
    if (/supositor|ovulo|vaginal|rectal/.test(f)) return 'supositorio';
    if (/espuma|spray|pulveriz/.test(f)) return 'spray';
    return 'otro';
  }

  var PLACEHOLDER_SVG = {
    comprimido:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><rect x="8" y="22" width="48" height="20" rx="10" fill="#C4A15A"/><line x1="32" y1="22" x2="32" y2="42" stroke="#1A160E" stroke-width="2" opacity=".35"/></svg>',
    capsula:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><path d="M14 32c0-8 6-14 14-14h8v28h-8c-8 0-14-6-14-14z" fill="#8F9A72"/><path d="M36 18h8c8 0 14 6 14 14s-6 14-14 14h-8z" fill="#C4A15A"/></svg>',
    jarabe:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><rect x="24" y="8" width="16" height="10" rx="2" fill="#9A9488"/><path d="M20 18h24l4 36H16z" fill="#C4A15A"/><path d="M18 40h28v14H18z" fill="#8F9A72" opacity=".85"/></svg>',
    crema:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><rect x="18" y="10" width="28" height="44" rx="4" fill="#C4A15A"/><rect x="22" y="14" width="20" height="12" rx="2" fill="#1C1A16" opacity=".35"/><circle cx="32" cy="40" r="6" fill="#E6E1D6" opacity=".5"/></svg>',
    gotas:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 8c0 0-14 18-14 28a14 14 0 0028 0C46 26 32 8 32 8z" fill="#6A8FA8"/><circle cx="32" cy="36" r="5" fill="#E6E1D6" opacity=".4"/></svg>',
    inhalador:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><rect x="22" y="6" width="20" height="36" rx="4" fill="#9A9488"/><rect x="26" y="42" width="12" height="14" rx="2" fill="#C4A15A"/><rect x="28" y="10" width="8" height="8" rx="1" fill="#1C1A16" opacity=".4"/></svg>',
    inyeccion:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><rect x="10" y="28" width="28" height="8" rx="2" fill="#9A9488"/><rect x="38" y="30" width="16" height="4" fill="#C4A15A"/><polygon points="54,32 62,28 62,36" fill="#E6E1D6"/><rect x="14" y="20" width="6" height="24" rx="1" fill="#8F9A72"/></svg>',
    parche:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><rect x="12" y="16" width="40" height="32" rx="6" fill="#C4A15A"/><rect x="18" y="22" width="28" height="20" rx="3" fill="#1C1A16" opacity=".25"/></svg>',
    sobre:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><path d="M10 18h44v32H10z" fill="#C4A15A"/><path d="M10 18l22 14L54 18" fill="none" stroke="#1A160E" stroke-width="2" opacity=".4"/></svg>',
    supositorio:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><ellipse cx="32" cy="20" rx="10" ry="8" fill="#C4A15A"/><path d="M22 20c0 20 4 36 10 36s10-16 10-36" fill="#8F9A72"/></svg>',
    spray:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><rect x="24" y="18" width="16" height="36" rx="4" fill="#9A9488"/><rect x="28" y="8" width="8" height="12" rx="2" fill="#C4A15A"/><circle cx="44" cy="14" r="3" fill="#E6E1D6" opacity=".6"/><circle cx="50" cy="10" r="2" fill="#E6E1D6" opacity=".45"/></svg>',
    otro:
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true"><rect x="14" y="14" width="36" height="36" rx="8" fill="#3A3630" stroke="#C4A15A" stroke-width="2"/><text x="32" y="38" text-anchor="middle" font-size="18" fill="#C4A15A" font-family="sans-serif">Rx</text></svg>'
  };

  function placeholderDataUrl(forma) {
    var key = formaKey(forma);
    var svg = PLACEHOLDER_SVG[key] || PLACEHOLDER_SVG.otro;
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  }

  function cimaUrls(nregistro) {
    var nr = encodeURIComponent(String(nregistro || ''));
    return {
      ficha: 'https://cima.aemps.es/cima/publico/detalle.html?nregistro=' + nr,
      prospecto: 'https://cima.aemps.es/cima/dochtml/p/' + nr + '/Prospecto.html',
      ft: 'https://cima.aemps.es/cima/dochtml/ft/' + nr + '/FichaTecnica.html'
    };
  }

  function scriptBase() {
    var scripts = document.getElementsByTagName('script');
    for (var i = scripts.length - 1; i >= 0; i--) {
      var src = scripts[i].src || '';
      if (/medicacion-nomenclator\.js(\?|$)/.test(src)) {
        return src.replace(/medicacion-nomenclator\.js(\?.*)?$/, '');
      }
    }
    return '';
  }

  async function inflateGzip(buf) {
    if (typeof DecompressionStream !== 'undefined') {
      var ds = new DecompressionStream('gzip');
      var stream = new Response(buf).body.pipeThrough(ds);
      var text = await new Response(stream).text();
      return text;
    }
    throw new Error('DecompressionStream no disponible; usa un navegador reciente o el ZIP con servidor local.');
  }

  async function fetchIndex(url) {
    var res = await fetch(url, { cache: 'force-cache' });
    if (!res.ok) throw new Error('HTTP ' + res.status + ' ' + url);
    return res;
  }

  /**
   * Load nomenclátor index. Tries nomenclator/cima-index.json.gz then .json.
   * @returns {Promise<{meta:object, meds:array}>}
   */
  async function loadIndex(baseOverride) {
    var base = baseOverride != null ? baseOverride : scriptBase() + 'nomenclator/';
    var lastErr = null;
    try {
      var resGz = await fetchIndex(base + 'cima-index.json.gz');
      var buf = await resGz.arrayBuffer();
      var text = await inflateGzip(buf);
      return JSON.parse(text);
    } catch (e) {
      lastErr = e;
    }
    try {
      var resJson = await fetchIndex(base + 'cima-index.json');
      return await resJson.json();
    } catch (e2) {
      lastErr = e2;
    }
    throw lastErr || new Error('No se pudo cargar el índice CIMA offline');
  }

  function searchMeds(meds, query, opts) {
    opts = opts || {};
    var limit = opts.limit || 40;
    var onlyCom = !!opts.onlyComercializados;
    var q = norm(query).trim();
    if (q.length < 2) return [];
    var parts = q.split(/\s+/).filter(Boolean);
    var digits = q.replace(/\s+/g, '');
    var isCn = /^\d{6,7}$/.test(digits);
    var scored = [];
    for (var i = 0; i < meds.length; i++) {
      var m = meds[i];
      if (onlyCom && !m.com) continue;
      var score = -1;
      if (isCn) {
        var cns = m.cn || [];
        for (var j = 0; j < cns.length; j++) {
          if (String(cns[j].c) === digits) {
            score = 0;
            break;
          }
        }
        if (score < 0 && String(m.nr) === digits) score = 1;
      } else {
        var nameN = norm(m.n);
        var paN = norm((m.pa || []).join(' '));
        var blob = norm(
          [m.n, m.dos, m.forma, m.lab, (m.pa || []).join(' ')].join(' ')
        );
        if (!parts.every(function (p) { return blob.indexOf(p) >= 0; })) continue;
        if (parts.every(function (p) { return nameN.indexOf(p) >= 0; })) {
          score = nameN.indexOf(parts[0]) === 0 ? 0 : 1;
        } else if (parts.every(function (p) { return paN.indexOf(p) >= 0; })) {
          score = 2;
        } else {
          score = 3;
        }
      }
      if (score >= 0) scored.push({ s: score, m: m });
    }
    scored.sort(function (a, b) {
      if (a.s !== b.s) return a.s - b.s;
      return norm(a.m.n).localeCompare(norm(b.m.n));
    });
    var out = [];
    for (var k = 0; k < scored.length && out.length < limit; k++) out.push(scored[k].m);
    return out;
  }

  // —— IndexedDB for user photos (never upload) ——
  var DB_NAME = 'lv-medicacion-photos';
  var DB_STORE = 'photos';
  var dbPromise = null;

  function openPhotoDb() {
    if (dbPromise) return dbPromise;
    dbPromise = new Promise(function (resolve, reject) {
      if (!root.indexedDB) {
        reject(new Error('IndexedDB no disponible'));
        return;
      }
      var req = indexedDB.open(DB_NAME, 1);
      req.onupgradeneeded = function () {
        var db = req.result;
        if (!db.objectStoreNames.contains(DB_STORE)) {
          db.createObjectStore(DB_STORE, { keyPath: 'id' });
        }
      };
      req.onsuccess = function () {
        resolve(req.result);
      };
      req.onerror = function () {
        reject(req.error || new Error('IDB open failed'));
      };
    });
    return dbPromise;
  }

  function idbReq(req) {
    return new Promise(function (resolve, reject) {
      req.onsuccess = function () {
        resolve(req.result);
      };
      req.onerror = function () {
        reject(req.error);
      };
    });
  }

  async function savePhoto(medId, dataUrl) {
    var db = await openPhotoDb();
    var tx = db.transaction(DB_STORE, 'readwrite');
    await idbReq(tx.objectStore(DB_STORE).put({ id: medId, dataUrl: dataUrl, ts: Date.now() }));
  }

  async function getPhoto(medId) {
    var db = await openPhotoDb();
    var tx = db.transaction(DB_STORE, 'readonly');
    var row = await idbReq(tx.objectStore(DB_STORE).get(medId));
    return row ? row.dataUrl : null;
  }

  async function deletePhoto(medId) {
    var db = await openPhotoDb();
    var tx = db.transaction(DB_STORE, 'readwrite');
    await idbReq(tx.objectStore(DB_STORE).delete(medId));
  }

  /** Compress image file to JPEG dataURL (max edge ~320, quality ~0.7). */
  function compressImageFile(file, maxEdge, quality) {
    maxEdge = maxEdge || 320;
    quality = quality || 0.7;
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        try {
          var w = img.naturalWidth || img.width;
          var h = img.naturalHeight || img.height;
          var scale = Math.min(1, maxEdge / Math.max(w, h));
          var cw = Math.max(1, Math.round(w * scale));
          var ch = Math.max(1, Math.round(h * scale));
          var canvas = document.createElement('canvas');
          canvas.width = cw;
          canvas.height = ch;
          var ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, cw, ch);
          var dataUrl = canvas.toDataURL('image/jpeg', quality);
          URL.revokeObjectURL(url);
          resolve(dataUrl);
        } catch (e) {
          URL.revokeObjectURL(url);
          reject(e);
        }
      };
      img.onerror = function () {
        URL.revokeObjectURL(url);
        reject(new Error('No se pudo leer la imagen'));
      };
      img.src = url;
    });
  }

  root.LV_NOMENCLATOR = {
    ATRIBUCION: ATRIBUCION,
    loadIndex: loadIndex,
    searchMeds: searchMeds,
    formaKey: formaKey,
    placeholderDataUrl: placeholderDataUrl,
    cimaUrls: cimaUrls,
    savePhoto: savePhoto,
    getPhoto: getPhoto,
    deletePhoto: deletePhoto,
    compressImageFile: compressImageFile,
    norm: norm
  };
})(typeof window !== 'undefined' ? window : this);
