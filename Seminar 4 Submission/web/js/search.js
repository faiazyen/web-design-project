/* Search results: sessions, performers and venues from js/data.js. Accent- and case-insensitive. */
(function () {
  "use strict";
  Site.ready(function () {
    var q = (Site.params().q || "").trim();
    var input = document.getElementById("site-search");
    if (input) input.value = q;
    if (q) document.title = "Search: " + q + " | Atardecer Bachata Festival";
    var out = document.getElementById("results");
    var terms = Site.norm(q).split(/\s+/).filter(Boolean);
    if (!terms.length || !Site.data) { document.documentElement.classList.add("ready"); return; }   // the page already says what to do

    function hit(hay) { return terms.every(function (t) { return hay.indexOf(t) > -1; }); }
    function mark(text) {
      var n = Site.norm(text);
      if (n.length !== text.length) return Site.esc(text);
      var ranges = [];
      terms.forEach(function (t) { var from = 0, i; while ((i = n.indexOf(t, from)) > -1) { ranges.push([i, i + t.length]); from = i + t.length; } });
      ranges.sort(function (a, b) { return a[0] - b[0]; });
      var res = "", pos = 0;
      ranges.forEach(function (r) { if (r[0] < pos) return; res += Site.esc(text.slice(pos, r[0])) + "<mark>" + Site.esc(text.slice(r[0], r[1])) + "</mark>"; pos = r[1]; });
      return res + Site.esc(text.slice(pos));
    }

    var sessions = Site.items.filter(function (it) {
      var v = Site.venueById[it.venueId];
      var names = it.performerIds.map(function (id) { var p = Site.performerById[id]; return p ? p.name + " " + p.members.join(" ") : ""; }).join(" ");
      return hit(Site.norm([it.title, it.description, it.tags.join(" "), Site.label("styles", it.style), Site.label("types", it.type), Site.label("levels", it.level), Site.label("roleFocus", it.roleFocus), v ? v.name : "", names].join(" ")));
    });
    var people = Site.data.performers.filter(function (p) {
      return hit(Site.norm([p.name, p.members.join(" "), p.bio, Site.country(p.country), p.styles.join(" "), Site.label("performerTypes", p.type)].join(" ")));
    });
    var venues = Site.data.venues.filter(function (v) { return hit(Site.norm([v.name, v.description, v.kind, v.address.streetAddress].join(" "))); });

    var total = sessions.length + people.length + venues.length;
    var html = '<p class="count" role="status">' + total + (total === 1 ? " result" : " results") + ' for "' + Site.esc(q) + '"</p>';
    if (!total) html += '<div class="empty"><p><strong>No results.</strong></p><p>Check the spelling, try one word, or browse the <a href="programme.html">programme</a> or the <a href="performers.html">performers</a>.</p></div>';
    if (people.length) {
      html += "<h2>Performers (" + people.length + ")</h2>" + '<ul class="grid grid-3 plain">' + people.map(function (p) {
        var n = Site.sessionsOf(p.id).length;
        return '<li class="card artist"><img class="avatar" src="' + Site.esc(p.image.src) + '" alt="" width="72" height="72" loading="lazy"><h3><a href="performers/' + Site.esc(p.slug) + '.html">' + mark(p.name) + "</a></h3>" +
          '<p class="meta">' + Site.esc(Site.label("performerTypes", p.type)) + " · " + Site.esc(Site.country(p.country)) + " · " + n + (n === 1 ? " session" : " sessions") + "</p></li>";
      }).join("") + "</ul>";
    }
    if (sessions.length) html += "<h2>Sessions (" + sessions.length + ')</h2><div class="session-list">' + sessions.map(function (it) { return Site.sessionCard(it); }).join("") + "</div>";
    if (venues.length) {
      html += "<h2>Venues (" + venues.length + ')</h2><div class="grid grid-3">' + venues.map(function (v) {
        return '<article class="card"><h3><a href="venues/' + Site.esc(v.slug) + '.html">' + mark(v.name) + '</a></h3><p class="meta">' + Site.esc(v.setting) + " · capacity " + Site.esc(v.capacity) + "</p><p>" + Site.esc(v.description) + "</p></article>";
      }).join("") + "</div>";
    }
    out.innerHTML = html;
    Site.refreshSaveButtons();
    document.documentElement.classList.add("ready");
  });
})();
