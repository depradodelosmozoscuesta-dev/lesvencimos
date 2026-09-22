/* Les vencimos — soft cultural gate (sessionStorage lv-gate-v1) */
(function (global) {
  var KEY = 'lv-gate-v1';
  var LOVE = { love: 1, amor: 1 };
  var BEATLES = { '4': 1, cuatro: 1, four: 1 };

  function letters(s) {
    return String(s || '')
      .trim()
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z]/g, '');
  }

  function digits(s) {
    return String(s || '')
      .trim()
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]/g, '');
  }

  function isUnlocked() {
    try {
      return sessionStorage.getItem(KEY) === 'ok';
    } catch (e) {
      return false;
    }
  }

  function setUnlocked() {
    try {
      sessionStorage.setItem(KEY, 'ok');
    } catch (e) {}
  }

  function applyUnlockUI() {
    document.documentElement.classList.remove('lv-locked');
  }

  function safeNext(next) {
    return !!(next && next.charAt(0) === '/' && next.indexOf('//') === -1);
  }

  function maybeRedirectNext() {
    var params = new URLSearchParams(location.search);
    var next = params.get('next') || '';
    if (safeNext(next)) {
      location.replace(next);
    }
  }

  function unlock() {
    setUnlocked();
    applyUnlockUI();
    maybeRedirectNext();
  }

  function earlyCheck() {
    if (isUnlocked()) {
      applyUnlockUI();
    } else {
      document.documentElement.classList.add('lv-locked');
    }
  }

  function bind(root) {
    root = root || document;
    var gate = root.getElementById ? root.getElementById('lv-gate') : null;
    if (!gate && root.querySelector) gate = root.querySelector('#lv-gate');
    if (!gate) return;

    if (isUnlocked()) {
      applyUnlockUI();
      maybeRedirectNext();
      return;
    }

    var wishOk = false;
    var a1 = gate.querySelector('#ans1');
    var a3 = gate.querySelector('#ans3');
    var err = gate.querySelector('#err');
    var btn = gate.querySelector('#go');
    var choices = gate.querySelectorAll('#ans2 .choice');

    choices.forEach(function (b) {
      b.addEventListener('click', function () {
        choices.forEach(function (x) {
          x.classList.remove('sel');
        });
        b.classList.add('sel');
        wishOk = b.getAttribute('data-v') === '1';
      });
    });

    function tryEnter() {
      var ok1 = !!(a1 && LOVE[letters(a1.value)]);
      var ok2 = wishOk;
      var ok3 = !!(a3 && BEATLES[digits(a3.value)]);
      if (ok1 || ok2 || ok3) {
        if (err) err.textContent = '';
        unlock();
        return;
      }
      if (err) err.textContent = 'Ninguna encaja aún. Prueba otra puerta.';
    }

    if (btn) btn.addEventListener('click', tryEnter);
    [a1, a3].forEach(function (el) {
      if (!el) return;
      el.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') tryEnter();
      });
    });
  }

  function boot() {
    earlyCheck();
    if (isUnlocked()) {
      maybeRedirectNext();
      return;
    }
    function run() {
      bind(document);
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', run);
    } else {
      run();
    }
  }

  global.LVGate = {
    KEY: KEY,
    isUnlocked: isUnlocked,
    unlock: unlock,
    bind: bind,
    boot: boot,
    earlyCheck: earlyCheck
  };

  boot();
})(window);
