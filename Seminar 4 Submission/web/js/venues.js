/* Venues page: interactive venue map. The venue details are already in the HTML. This only shows one panel at a time
   and lets the visitor pick a day for the session list. Without JavaScript all panels are listed one after another. */
(function () {
  "use strict";
  Site.ready(function () {
    var map = document.getElementById("venue-map");
    if (!map) return;
    map.hidden = false;
    var hint = document.getElementById("map-hint"); hint.hidden = false;
    var pins = Array.prototype.slice.call(map.querySelectorAll(".pin"));
    var panels = Array.prototype.slice.call(document.querySelectorAll(".map-panel"));

    function showDay(panel, day) {
      Array.prototype.forEach.call(panel.querySelectorAll(".map-day"), function (d) { d.hidden = d.getAttribute("data-day") !== day; });
    }
    panels.forEach(function (p) {
      var pick = p.querySelector(".day-pick"), sel = p.querySelector("select");
      pick.hidden = false;
      showDay(p, sel.value);
      sel.addEventListener("change", function () { showDay(p, sel.value); });
    });

    function show(id) {
      pins.forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-venue") === id)); });
      panels.forEach(function (p) { p.classList.toggle("active", p.getAttribute("data-venue") === id); });
      hint.hidden = !!id;
    }
    pins.forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-venue");
        show(b.getAttribute("aria-pressed") === "true" ? null : id);
      });
    });
    show(null);
  });
})();
