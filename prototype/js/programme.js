/* Programme page: filters (day, venue, type, level, role focus, day or night). */
(function () {
  "use strict";
  Site.init({ nav: "programme", crumbs: [["Home", "index.html"], ["Programme"]] });

  var form = document.getElementById("filter-form");
  var ids = { day: "f-day", venue: "f-venue", type: "f-type", level: "f-level", role: "f-role", daypart: "f-daypart" };

  function fill(selectId, list, labelKey) {
    var sel = document.getElementById(selectId);
    list.forEach(function (x) {
      var o = document.createElement("option");
      o.value = x.id; o.textContent = x[labelKey || "label"];
      sel.appendChild(o);
    });
  }
  fill(ids.day, Site.data.days.map(function (d) { return { id: d.id, label: Site.dateLong(d.id) }; }));
  fill(ids.venue, Site.data.venues.map(function (v) { return { id: v.id, label: v.name }; }));
  fill(ids.type, Site.cat.types);
  fill(ids.level, Site.cat.levels);
  fill(ids.role, Site.cat.roleFocus);
  fill(ids.daypart, Site.cat.dayParts);

  // start state from the URL (for example programme.html?daypart=night)
  var p = Site.params();
  Object.keys(ids).forEach(function (k) {
    var el = document.getElementById(ids[k]);
    if (p[k] && el.querySelector('option[value="' + p[k] + '"]')) el.value = p[k];
  });

  function current() {
    var f = {};
    Object.keys(ids).forEach(function (k) { f[k] = document.getElementById(ids[k]).value; });
    return f;
  }

  function matches(it, f) {
    return (!f.day || it.dayId === f.day) && (!f.venue || it.venueId === f.venue) && (!f.type || it.type === f.type) &&
      (!f.level || it.level === f.level) && (!f.role || it.roleFocus === f.role || (f.role !== "both" && it.roleFocus === "both")) &&
      (!f.daypart || it.dayPart === f.daypart);
  }

  function render() {
    var f = current();
    var list = Site.items.filter(function (it) { return matches(it, f); });
    var active = Object.keys(f).filter(function (k) { return f[k]; }).length;
    document.getElementById("filter-badge").textContent = active ? " (" + active + " active)" : "";
    document.getElementById("count").textContent = "Showing " + list.length + " of " + Site.items.length + " sessions";

    var out = document.getElementById("results");
    if (!list.length) {
      out.innerHTML = '<div class="empty"><p><strong>No sessions match these filters.</strong></p><p>Try a different level or role, or clear all filters.</p></div>';
    } else {
      var html = "";
      Site.data.days.forEach(function (d) {
        var day = list.filter(function (it) { return it.dayId === d.id; });
        if (!day.length) return;
        html += "<h3>" + Site.esc(Site.dateLong(d.id)) + ' <span class="meta">(' + day.length + ")</span></h3>" +
          '<ul class="card-list">' + day.map(function (it) { return Site.sessionCard(it); }).join("") + "</ul>";
      });
      out.innerHTML = html;
    }
    // keep the URL in step so the page can be shared or reloaded
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
  document.addEventListener("programme-changed", function () { /* buttons already refreshed */ });

  render();
  // on a phone, when filters are already set (for example from a link), show the results first and fold the filter panel
  if (window.matchMedia && window.matchMedia("(max-width: 899px)").matches && Object.keys(current()).some(function (k) { return current()[k]; })) {
    document.getElementById("filters").open = false;
  }
})();
