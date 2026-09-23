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

  function isHome() {
    return document.documentElement.classList.contains('lv-home');
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
    if (isHome()) return;
    if (isUnlocked()) {
      applyUnlockUI();
    } else if (document.getElementById('lv-gate')) {
      document.documentElement.classList.add('lv-locked');
    }
  }

  function bindChoices(root, onSelect) {
    var choices = root.querySelectorAll('#ans2 .choice, [data-desk-ans2] .choice');
    if (!choices.length) choices = root.querySelectorAll('.choices .choice');
    var wishOk = false;
    choices.forEach(function (b) {
      b.addEventListener('click', function () {
        choices.forEach(function (x) {
          x.classList.remove('sel');
        });
        b.classList.add('sel');
        wishOk = b.getAttribute('data-v') === '1';
        if (onSelect) onSelect(wishOk);
      });
    });
    return function () {
      return wishOk;
    };
  }

  function tryAnswers(a1, wishOk, a3) {
    var ok1 = !!(a1 && LOVE[letters(a1.value)]);
    var ok2 = !!wishOk;
    var ok3 = !!(a3 && BEATLES[digits(a3.value)]);
    return ok1 || ok2 || ok3;
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

    var getWish = bindChoices(gate);
    var a1 = gate.querySelector('#ans1');
    var a3 = gate.querySelector('#ans3');
    var err = gate.querySelector('#err');
    var btn = gate.querySelector('#go');

    function tryEnter() {
      if (tryAnswers(a1, getWish(), a3)) {
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

  function bindDesk(opts) {
    opts = opts || {};
    var openBtn = opts.openBtn || document.getElementById('lv-desk-open');
    var panel = opts.panel || document.getElementById('lv-desk-panel');
    if (!openBtn || !panel) return;

    var a1 = panel.querySelector('#ans1');
    var a3 = panel.querySelector('#ans3');
    var err = panel.querySelector('#err');
    var btn = panel.querySelector('#go');
    var okMsg = panel.querySelector('#lv-desk-ok');
    var actions = panel.querySelector('#lv-desk-actions');
    var getWish = bindChoices(panel);

    function setOpen(open) {
      if (open) {
        panel.hidden = false;
        panel.classList.add('is-open');
        openBtn.setAttribute('aria-expanded', 'true');
        openBtn.classList.add('is-open');
      } else {
        panel.hidden = true;
        panel.classList.remove('is-open');
        openBtn.setAttribute('aria-expanded', 'false');
        openBtn.classList.remove('is-open');
      }
    }

    function showSuccess() {
      if (err) err.textContent = '';
      if (okMsg) {
        okMsg.hidden = false;
        okMsg.textContent = 'Llave aceptada. Pronto habrá algo especial aquí.';
      }
      if (actions) actions.hidden = true;
      if (a1) a1.disabled = true;
      if (a3) a3.disabled = true;
      panel.querySelectorAll('.choice').forEach(function (c) {
        c.disabled = true;
      });
    }

    openBtn.addEventListener('click', function () {
      var open = openBtn.getAttribute('aria-expanded') !== 'true';
      setOpen(open);
      if (open && isUnlocked()) showSuccess();
    });

    if (isUnlocked()) {
      openBtn.classList.add('lv-desk-ready');
    }

    function tryEnter() {
      if (tryAnswers(a1, getWish(), a3)) {
        setUnlocked();
        applyUnlockUI();
        showSuccess();
        openBtn.classList.add('lv-desk-ready');
        return;
      }
      if (err) err.textContent = 'Ninguna encaja aún. Prueba otra puerta.';
      if (okMsg) okMsg.hidden = true;
    }

    if (btn) btn.addEventListener('click', tryEnter);
    [a1, a3].forEach(function (el) {
      if (!el) return;
      el.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') tryEnter();
      });
    });

    return {
      open: function () {
        setOpen(true);
      },
      close: function () {
        setOpen(false);
      }
    };
  }

  function boot() {
    if (isHome()) {
      function runDesk() {
        bindDesk({});
      }
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', runDesk);
      } else {
        runDesk();
      }
      return;
    }

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
    setUnlocked: setUnlocked,
    unlock: unlock,
    bind: bind,
    bindDesk: bindDesk,
    boot: boot,
    earlyCheck: earlyCheck
  };

  boot();
})(window);
