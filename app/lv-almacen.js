/* lv-almacen.js — puente opcional.
   Un módulo nuevo puede cargarlo y guardar en disco
   cuando vive dentro del cascarón (mismo origen).
   Si no hay servidor, cae a localStorage. */
(function (root) {
  var PREFIX = "lv-";
  function lan() {
    return location.protocol === "http:" || location.protocol === "https:";
  }
  function idDeCarpeta() {
    var parts = location.pathname.split("/").filter(Boolean);
    var i = parts.indexOf("modules");
    if (i >= 0 && parts[i + 1]) return parts[i + 1];
    return null;
  }
  root.lvAlmacen = {
    id: idDeCarpeta(),
    async leer(id) {
      id = id || this.id;
      if (lan() && id) {
        try {
          var r = await fetch("/api/datos?id=" + encodeURIComponent(id), { cache: "no-store" });
          if (r.ok) {
            var j = await r.json();
            return j.datos || null;
          }
        } catch (e) {}
      }
      try { return JSON.parse(localStorage.getItem(PREFIX + id) || "null"); }
      catch (e) { return null; }
    },
    async escribir(obj, id) {
      id = id || this.id;
      if (lan() && id) {
        try {
          var r = await fetch("/api/datos?id=" + encodeURIComponent(id), {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ datos: obj })
          });
          if (r.ok) return true;
        } catch (e) {}
      }
      try {
        localStorage.setItem(PREFIX + id, JSON.stringify(obj));
        return true;
      } catch (e) { return false; }
    }
  };
})(window);
