/* Programme page: filters the sessions that are already in the HTML (day, venue, type, level, role focus, day or night).
   Without JavaScript the full list is still there. */
(function () {
  "use strict";
  Site.ready(function () {
    var form = document.getElementById("filter-form");
    var ids = { day: "f-day", venue: "f-venue", type: "f-type", level: "f-level", role: "f-role", daypart: "f-daypart" };
    var attr = { day: "day", venue: "venue", type: "type", level: "level", role: "role", daypart: "daypart" };
    var cards = Array.prototype.slice.call(document.querySelectorAll(".session"));
    var groups = Array.prototype.slice.call(document.querySelectorAll(".day-group"));
    var total = cards.length;

    var p = Site.params();
    Object.keys(ids).forEach(function (k) {
      var el = document.getElementById(ids[k]);
      if (p[k] && el.querySelector('option[value="' + p[k] + '"]')) el.value = p[k];
    });

    function current() { var f = {}; Object.keys(ids).forEach(function (k) { f[k] = document.getElementById(ids[k]).value; }); return f; }
    function ok(c, f) {
      return (!f.day || c.getAttribute("data-day") === f.day) && (!f.venue || c.getAttribute("data-venue") === f.venue) && (!f.type || c.getAttribute("data-type") === f.type) &&
        (!f.level || c.getAttribute("data-level") === f.level) && (!f.daypart || c.getAttribute("data-daypart") === f.daypart) &&
        (!f.role || c.getAttribute("data-role") === f.role || (f.role !== "both" && c.getAttribute("data-role") === "both"));
    }

    function render() {
      var f = current(), shown = 0;
      cards.forEach(function (c) { var m = ok(c, f); c.hidden = !m; if (m) shown++; });
      groups.forEach(function (g) {
        var n = g.querySelectorAll(".session:not([hidden])").length;
        g.hidden = n === 0;
        g.querySelector(".day-count").textContent = n;
      });
      var active = Object.keys(f).filter(function (k) { return f[k]; }).length;
      document.getElementById("filter-badge").textContent = active ? "(" + active + " active)" : "";
      document.getElementById("count").textContent = active ? "Showing " + shown + " of " + total + " sessions" : "Showing all " + total + " sessions";
      document.getElementById("none").hidden = shown !== 0;
      try {
        var q = Object.keys(f).filter(function (k) { return f[k]; }).map(function (k) { return k + "=" + encodeURIComponent(f[k]); }).join("&");
        history.replaceState(null, "", "programme.html" + (q ? "?" + q : ""));
      } catch (e) { /* file:// in some browsers */ }
    }

    form.addEventListener("change", render);
    form.addEventListener("submit", function (e) { e.preventDefault(); render(); });
    document.getElementById("clear").addEventListener("click", function () {
      Object.keys(ids).forEach(function (k) { document.getElementById(ids[k]).value = ""; });
      render();
      document.getElementById(ids.day).focus();
    });

    // wide screens: filters always open. Phones: folded when a link already set filters, so the results come first.
    var panel = document.getElementById("filters"), wide = window.matchMedia("(min-width: 900px)");
    function fit() { if (wide.matches) panel.open = true; }
    fit();
    if (wide.addEventListener) wide.addEventListener("change", fit);
    render();
    if (!wide.matches && Object.keys(current()).some(function (k) { return current()[k]; })) panel.open = false;
  });
})();
