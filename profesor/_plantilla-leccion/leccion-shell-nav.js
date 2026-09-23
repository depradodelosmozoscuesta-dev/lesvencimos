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
