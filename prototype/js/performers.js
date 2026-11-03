/* Performers list: filter by type and by name. */
(function () {
  "use strict";
  Site.init({ nav: "performers", crumbs: [["Home", "index.html"], ["Performers"]] });
  var sel = document.getElementById("p-type"), name = document.getElementById("p-name");
  Site.cat.performerTypes.forEach(function (t) {
    var o = document.createElement("option"); o.value = t.id; o.textContent = t.label; sel.appendChild(o);
  });
  var p = Site.params();
  if (p.type) sel.value = p.type;
  if (p.name) name.value = p.name;

  function render() {
    var q = Site.norm(name.value.trim());
    var list = Site.data.performers.filter(function (x) {
      var hay = Site.norm(x.name + " " + x.members.join(" "));
      return (!sel.value || x.type === sel.value) && (!q || hay.indexOf(q) > -1);
    });
    document.getElementById("count").textContent = "Showing " + list.length + " of " + Site.data.performers.length + " performers";
    document.getElementById("list").innerHTML = list.length ? list.map(function (x) {
      var n = Site.sessionsOf(x.id).length;
      return '<li class="card"><div class="ph ph-square" aria-hidden="true">Photo</div><h3><a href="performer.html?slug=' + Site.esc(x.slug) + '">' + Site.esc(x.name) + '</a></h3>' +
        '<p class="meta">' + Site.esc(Site.label("performerTypes", x.type)) + " · " + Site.esc(Site.country(x.country)) + " · " + n + (n === 1 ? " session" : " sessions") + "</p></li>";
    }).join("") : '<li class="empty"><p><strong>No performer matches.</strong></p><p>Try fewer letters or choose All types.</p></li>';
  }
  document.getElementById("pf").addEventListener("input", render);
  document.getElementById("pf").addEventListener("submit", function (e) { e.preventDefault(); render(); });
  render();
})();
