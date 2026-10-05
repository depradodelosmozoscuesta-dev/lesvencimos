(function () {
  document.querySelectorAll(".quiz").forEach(function (q) {
    var btn = q.querySelector(".corregir");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var sol = q.getAttribute("data-solucion");
      var marcada = q.querySelector("input:checked");
      q.classList.add("visto");
      q.classList.remove("acierto", "fallo");
      if (!marcada) {
        q.classList.add("fallo");
        return;
      }
      q.classList.add(marcada.value === sol ? "acierto" : "fallo");
    });
  });
  document.querySelectorAll(".editor").forEach(function (ed) {
    var clave = "bach-eco:" + (ed.getAttribute("data-clave") || location.pathname);
    var ta = ed.querySelector("textarea");
    var n = ed.querySelector(".palabras");
    var estado = ed.querySelector(".estado-editor");
    if (!ta) return;
    try { var prev = localStorage.getItem(clave); if (prev) ta.value = prev; } catch (e) {}
    function contar() {
      var t = ta.value.trim();
      var c = t ? t.split(/\s+/).length : 0;
      if (n) n.textContent = String(c);
    }
    contar();
    ta.addEventListener("input", contar);
    var g = ed.querySelector(".guardar");
    if (g) g.addEventListener("click", function () {
      try {
        localStorage.setItem(clave, ta.value);
        if (estado) estado.textContent = "Guardado en este aparato.";
      } catch (e) {
        if (estado) estado.textContent = "No se pudo guardar. Copia el texto antes de cerrar.";
      }
    });
  });
})();
