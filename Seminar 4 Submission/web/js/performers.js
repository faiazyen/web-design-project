/* Performers list: filters the artists that are already in the HTML, by name and by type. */
(function () {
  "use strict";
  Site.ready(function () {
    var sel = document.getElementById("p-type"), name = document.getElementById("p-name"), form = document.getElementById("pf");
    var cards = Array.prototype.slice.call(document.querySelectorAll("#list > li"));
    var p = Site.params();
    if (p.type && sel.querySelector('option[value="' + p.type + '"]')) sel.value = p.type;
    if (p.name) name.value = p.name;

    function render() {
      var q = Site.norm(name.value.trim()), shown = 0;
      cards.forEach(function (c) {
        var m = (!sel.value || c.getAttribute("data-type") === sel.value) && (!q || c.getAttribute("data-name").indexOf(q) > -1);
        c.hidden = !m; if (m) shown++;
      });
      var filtered = sel.value || q;
      document.getElementById("count").textContent = filtered ? "Showing " + shown + " of " + cards.length + " performers" : "Showing all " + cards.length + " performers";
      document.getElementById("none").hidden = shown !== 0;
    }
    form.addEventListener("input", render);
    form.addEventListener("change", render);
    form.addEventListener("submit", function (e) { e.preventDefault(); render(); });
    render();
  });
})();
