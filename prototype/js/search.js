/* Search results: sessions, performers and venues. Accent- and case-insensitive. */
(function () {
  "use strict";
  var q = (Site.params().q || "").trim();
  Site.init({ nav: "", crumbs: [["Home", "index.html"], [q ? 'Search results for "' + q + '"' : "Search results"]] });
  document.title = (q ? 'Search: ' + q : "Search results") + " | Atardecer Bachata Festival (prototype)";
  var input = document.getElementById("site-search");
  if (input) input.value = q;
  var out = document.getElementById("results");
  var terms = Site.norm(q).split(/\s+/).filter(Boolean);

  if (!terms.length) {
    out.innerHTML = '<div class="empty"><p><strong>Type a name, a session or a venue in the search box.</strong></p>' +
      '<p>Try: <a href="search.html?q=guitar">guitar</a>, <a href="search.html?q=beginner">beginner</a>, <a href="search.html?q=marisol">marisol</a>.</p></div>';
    return;
  }

  function hit(hay) { return terms.every(function (t) { return hay.indexOf(t) > -1; }); }

  function mark(text) {
    var n = Site.norm(text);
    if (n.length !== text.length) return Site.esc(text);
    var ranges = [];
    terms.forEach(function (t) {
      var from = 0, i;
      while ((i = n.indexOf(t, from)) > -1) { ranges.push([i, i + t.length]); from = i + t.length; }
    });
    ranges.sort(function (a, b) { return a[0] - b[0]; });
    var res = "", pos = 0;
    ranges.forEach(function (r) {
      if (r[0] < pos) return;
      res += Site.esc(text.slice(pos, r[0])) + "<mark>" + Site.esc(text.slice(r[0], r[1])) + "</mark>";
      pos = r[1];
    });
    return res + Site.esc(text.slice(pos));
  }

  var sessions = Site.items.filter(function (it) {
    var v = Site.venueById[it.venueId];
    var names = Site.performersOf(it).map(function (p) { return p.name + " " + p.members.join(" "); }).join(" ");
    return hit(Site.norm([it.title, it.description, it.tags.join(" "), Site.label("styles", it.style), Site.label("types", it.type),
      Site.label("levels", it.level), Site.roleLabel(it.roleFocus), v ? v.name : "", names].join(" ")));
  });
  var people = Site.data.performers.filter(function (p) {
    return hit(Site.norm([p.name, p.members.join(" "), p.bio, Site.country(p.country), p.styles.join(" "), Site.label("performerTypes", p.type)].join(" ")));
  });
  var venues = Site.data.venues.filter(function (v) {
    return hit(Site.norm([v.name, v.description, v.kind, v.address.streetAddress].join(" ")));
  });

  var total = sessions.length + people.length + venues.length;
  var html = '<p class="count" role="status">' + total + (total === 1 ? " result" : " results") + ' for "' + Site.esc(q) + '"</p>';

  if (!total) {
    html += '<div class="empty"><p><strong>No results.</strong></p><p>Check the spelling, try one word, or browse the <a href="programme.html">programme</a> or the <a href="performers.html">performers</a>.</p></div>';
  }
  if (people.length) {
    html += "<h2>Performers (" + people.length + ")</h2>" + '<ul class="card-list cols-2">' + people.map(function (p) {
      var n = Site.sessionsOf(p.id).length;
      return '<li class="card"><h3><a href="performer.html?slug=' + Site.esc(p.slug) + '">' + mark(p.name) + "</a></h3><p class=\"meta\">" +
        Site.esc(Site.label("performerTypes", p.type)) + " · " + Site.esc(Site.country(p.country)) + " · " + n + (n === 1 ? " session" : " sessions") + "</p></li>";
    }).join("") + "</ul>";
  }
  if (sessions.length) {
    html += "<h2>Sessions (" + sessions.length + ")</h2>" + '<ul class="card-list">' + sessions.map(function (it) {
      return Site.sessionCard(it, { extra: "" });
    }).join("") + "</ul>";
  }
  if (venues.length) {
    html += "<h2>Venues (" + venues.length + ")</h2>" + '<ul class="card-list">' + venues.map(function (v) {
      return '<li class="card"><h3>' + mark(v.name) + '</h3><p class="meta">' + Site.esc(v.setting) + " · capacity " + Site.esc(v.capacity) + "</p><p>" + Site.esc(v.description) + "</p></li>";
    }).join("") + "</ul>";
  }
  html += '<p class="meta">FAQ and Roots pages are not part of this prototype, so they are not searched here.</p>';
  out.innerHTML = html;
})();
