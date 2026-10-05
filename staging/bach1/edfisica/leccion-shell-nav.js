/*! Les vencimos — barra de lección (offline).
 * Lee data-actual / data-total en .leccion-barra y actualiza
 * .progreso-texto y .progreso-lleno. No inventa hrefs prev/next.
 */
(function () {
  function initBarra(barra) {
    var actual = parseInt(barra.getAttribute("data-actual"), 10);
    var total = parseInt(barra.getAttribute("data-total"), 10);
    if (!isFinite(actual) || !isFinite(total) || total <= 0) return;
    if (actual < 1) actual = 1;
    if (actual > total) actual = total;

    var texto = barra.querySelector(".progreso-texto");
    if (texto) {
      texto.innerHTML =
        "<strong>" + actual + "</strong> de <strong>" + total + "</strong>";
    }

    var lleno = barra.querySelector(".progreso-lleno");
    if (lleno) {
      var pct = (actual / total) * 100;
      lleno.style.width = (Math.round(pct * 100) / 100) + "%";
    }
  }

  function run() {
    var barras = document.querySelectorAll(".leccion-barra");
    for (var i = 0; i < barras.length; i++) initBarra(barras[i]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();

/* Vista alumno / maestro cuando esta página no carga maestro-runtime.js */
(function () {
  function hasRuntime() {
    var ss = document.scripts;
    for (var i = 0; i < ss.length; i++) {
      if ((ss[i].getAttribute("src") || "").indexOf("maestro-runtime") !== -1) return true;
    }
    return false;
  }
  function storageGet(k) {
    try { return localStorage.getItem(k); } catch (e) { return null; }
  }
  function storageSet(k, v) {
    try { localStorage.setItem(k, v); } catch (e) {}
  }
  function maestroOn() {
    try {
      if (new URL(location.href).searchParams.get("maestro") === "1") return true;
    } catch (e) {
      if (/[?&]maestro=1(?:&|$)/.test(location.search || "")) return true;
    }
    return storageGet("lv-modo-maestro") === "1";
  }
  function markClaves() {
    var details = document.querySelectorAll("details");
    for (var i = 0; i < details.length; i++) {
      var d = details[i];
      if (d.classList.contains("term") || d.classList.contains("extra-placa")) continue;
      var sum = d.querySelector("summary");
      var txt = sum ? sum.textContent || "" : "";
      if (d.classList.contains("porque") || d.classList.contains("correccion") || d.classList.contains("comprueba") || /^\s*(porqu[eé]|correcci[oó]n|soluci[oó]n|respuesta)\b/i.test(txt)) {
        d.classList.add("lv-clave");
      }
    }
  }
  function apply(on) {
    document.body.classList.toggle("modo-maestro", !!on);
    document.body.classList.toggle("vista-alumno", !on);
    if (on) {
      markClaves();
      var open = document.querySelectorAll("details.porque, details.correccion, details.comprueba, details.lv-clave");
      for (var i = 0; i < open.length; i++) open[i].open = true;
    }
  }
  function label(on) {
    var nodes = document.querySelectorAll(".atajo-maestro, #maestro-atajo-fijo");
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].textContent = on ? "Vista alumno" : "Modo maestro";
      nodes[i].setAttribute("aria-pressed", on ? "true" : "false");
      nodes[i].classList.toggle("is-activo", !!on);
    }
  }
  function run() {
    if (hasRuntime()) return;
    var lesson = document.querySelector(".leccion-barra, .leccion-nav, .leccion-shell, body.leccion-shell");
    if (!lesson && !document.querySelector("details.porque, details.correccion, .porque, .nota-shell")) return;
    var on = maestroOn();
    apply(on);
    label(on);
    var nodes = document.querySelectorAll(".atajo-maestro");
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].getAttribute("data-vista-wired") === "1") continue;
      nodes[i].setAttribute("data-vista-wired", "1");
      nodes[i].addEventListener("click", function (ev) {
        ev.preventDefault();
        on = !document.body.classList.contains("modo-maestro");
        try { localStorage.setItem("lv-modo-maestro", on ? "1" : "0"); } catch (e) {}
        apply(on);
        label(on);
      });
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
