(function () {
  document.querySelectorAll("[data-pasos]").forEach(function (box) {
    var capas = box.querySelectorAll(".paso-capa");
    function show(n) {
      capas.forEach(function (c) {
        var k = Number(c.getAttribute("data-paso"));
        c.toggleAttribute("hidden", k > n);
      });
      box.querySelectorAll(".paso-btn").forEach(function (b) {
        b.setAttribute("aria-pressed", String(Number(b.getAttribute("data-hasta")) === n));
      });
    }
    box.querySelectorAll(".paso-btn").forEach(function (b) {
      b.addEventListener("click", function () { show(Number(b.getAttribute("data-hasta"))); });
    });
    show(1);
  });
  document.querySelectorAll("article.pregunta").forEach(function (art) {
    var ok = art.getAttribute("data-ok");
    art.querySelectorAll("button.opcion").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (art.classList.contains("resuelta")) return;
        art.classList.add("resuelta");
        var bien = btn.getAttribute("data-op") === ok;
        btn.classList.add(bien ? "es-ok" : "es-mal");
        if (!bien) {
          var buena = art.querySelector('button.opcion[data-op="' + ok + '"]');
          if (buena) buena.classList.add("es-ok");
        }
        var p = art.querySelector("p.porque");
        if (p) p.hidden = false;
      });
    });
  });
  document.querySelectorAll("canvas.lienzo").forEach(function (c) {
    var ctx = c.getContext("2d");
    var tool = "lapiz";
    var drawing = false;
    var last = null;
    var anchor = null;
    var snapshot = null;
    function fondo() {
      ctx.fillStyle = "#161512";
      ctx.fillRect(0, 0, c.width, c.height);
      ctx.strokeStyle = "#C4A15A";
      ctx.lineWidth = 1;
      ctx.strokeRect(0.5, 0.5, c.width - 1, c.height - 1);
    }
    function fit() {
      var r = c.getBoundingClientRect();
      var w = Math.max(320, Math.floor(r.width));
      if (c.width !== w) { c.width = w; c.height = 340; fondo(); }
    }
    function pos(ev) {
      var r = c.getBoundingClientRect();
      var s = ev.touches ? ev.touches[0] : ev;
      return { x: (s.clientX - r.left) * c.width / r.width, y: (s.clientY - r.top) * c.height / r.height };
    }
    function stroke() {
      ctx.strokeStyle = "#E6E1D6";
      ctx.lineWidth = 2;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
    }
    var box = c.closest(".lienzo-bloque") || c.parentElement;
    box.querySelectorAll("[data-tool]").forEach(function (b) {
      b.addEventListener("click", function () {
        tool = b.getAttribute("data-tool");
        anchor = null;
        box.querySelectorAll("[data-tool]").forEach(function (o) {
          o.setAttribute("aria-pressed", String(o === b));
        });
      });
    });
    var first = box.querySelector("[data-tool]");
    if (first) first.setAttribute("aria-pressed", "true");
    var clear = box.querySelector("[data-clear]");
    if (clear) clear.addEventListener("click", function () { anchor = null; fondo(); });
    c.addEventListener("pointerdown", function (ev) {
      var p = pos(ev);
      if (tool === "lapiz") { drawing = true; last = p; }
      else if (!anchor) { anchor = p; snapshot = ctx.getImageData(0, 0, c.width, c.height); }
      else {
        stroke();
        ctx.beginPath();
        if (tool === "linea") { ctx.moveTo(anchor.x, anchor.y); ctx.lineTo(p.x, p.y); ctx.stroke(); }
        if (tool === "circ") {
          var dx = p.x - anchor.x, dy = p.y - anchor.y;
          ctx.arc(anchor.x, anchor.y, Math.sqrt(dx * dx + dy * dy), 0, Math.PI * 2);
          ctx.stroke();
        }
        anchor = null;
        snapshot = null;
      }
      ev.preventDefault();
    });
    c.addEventListener("pointermove", function (ev) {
      var p = pos(ev);
      if (tool === "lapiz" && drawing) {
        stroke();
        ctx.beginPath();
        ctx.moveTo(last.x, last.y);
        ctx.lineTo(p.x, p.y);
        ctx.stroke();
        last = p;
      } else if (anchor && snapshot && (tool === "linea" || tool === "circ")) {
        ctx.putImageData(snapshot, 0, 0);
        stroke();
        ctx.beginPath();
        if (tool === "linea") { ctx.moveTo(anchor.x, anchor.y); ctx.lineTo(p.x, p.y); }
        else {
          var dx = p.x - anchor.x, dy = p.y - anchor.y;
          ctx.arc(anchor.x, anchor.y, Math.sqrt(dx * dx + dy * dy), 0, Math.PI * 2);
        }
        ctx.stroke();
      }
      ev.preventDefault();
    });
    function up() { drawing = false; }
    c.addEventListener("pointerup", up);
    c.addEventListener("pointerleave", function (ev) { if (tool === "lapiz") drawing = false; });
    fit();
    window.addEventListener("resize", fit);
  });
})();
