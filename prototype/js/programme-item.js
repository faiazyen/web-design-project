/* Session detail page: contextual display of one programme item. */
(function () {
  "use strict";
  var item = Site.itemBySlug[Site.params().slug || ""];
  var out = document.getElementById("content");

  if (!item) {
    Site.init({ nav: "programme", crumbs: [["Home", "index.html"], ["Programme", "programme.html"], ["Session not found"]] });
    document.title = "Session not found | Atardecer Bachata Festival (prototype)";
    out.innerHTML = '<h1>Session not found</h1><div class="empty"><p>We could not find that session.</p><p><a class="btn btn-primary" href="programme.html">Back to the programme</a></p></div>';
    return;
  }

  Site.init({ nav: "programme", crumbs: [["Home", "index.html"], ["Programme", "programme.html"], [item.title]] });
  document.title = item.title + " | Atardecer Bachata Festival (prototype)";

  var venue = Site.venueById[item.venueId];
  var performers = Site.performersOf(item);
  var level = Site.cat.levels.filter(function (l) { return l.id === item.level; })[0];
  var others = Site.sessionsAt(item.venueId).filter(function (i) { return i.dayId === item.dayId && i.id !== item.id; }).slice(0, 4);

  out.innerHTML =
    "<h1>" + Site.esc(item.title) + "</h1>" +
    "<p class=\"lede\">" + Site.esc(Site.dateLong(item.dayId)) + " · " + Site.esc(Site.range(item)) + (item.start.slice(0, 10) !== Site.dayById[item.dayId].date ? " (after midnight)" : "") + "</p>" +
    Site.tagsFor(item) +
    '<div class="layout-detail"><div>' +
    "<p>" + Site.esc(item.description) + "</p>" +
    '<div class="btn-row">' + Site.saveButton(item) + '<a class="btn btn-secondary" href="my-programme.html">Open My Programme</a></div>' +
    "<h2>Who is on</h2>" +
    '<ul class="card-list">' + performers.map(function (p) {
      return '<li class="card"><h3><a href="performer.html?slug=' + Site.esc(p.slug) + '">' + Site.esc(p.name) + "</a></h3><p class=\"meta\">" +
        Site.esc(Site.label("performerTypes", p.type)) + " · " + Site.esc(Site.country(p.country)) + "</p></li>";
    }).join("") + "</ul>" +
    '<aside class="note"><strong>Function · contextual details.</strong> The session page answers "where, when, who, for whom" in one place and links to the performer pages. The Save button works the same as on the Programme list.</aside>' +
    "</div><div>" +
    "<h2 style=\"margin-top:0\">Facts</h2>" +
    '<dl class="facts"><dt>Where</dt><dd>' + Site.esc(venue.name) + " (" + Site.esc(venue.setting) + ")</dd>" +
    "<dt>Type</dt><dd>" + Site.esc(Site.label("types", item.type)) + "</dd>" +
    "<dt>Level</dt><dd>" + Site.esc(level ? level.label : item.level) + (level ? "<br><small>" + Site.esc(level.description) + "</small>" : "") + "</dd>" +
    "<dt>Role focus</dt><dd>" + Site.esc(Site.roleLabel(item.roleFocus)) + "</dd>" +
    "<dt>Style</dt><dd>" + Site.esc(Site.label("styles", item.style)) + "</dd>" +
    "<dt>Places</dt><dd>" + (item.capacity ? Site.esc(item.capacity) : "Open, no booking needed") + "</dd></dl>" +
    '<div class="ph" role="img" aria-label="Image placeholder: venue photo">Image placeholder<br>Venue photo, 4:3</div>' +
    (others.length ? "<h2>Also at " + Site.esc(venue.name) + " that day</h2><ul>" + others.map(function (o) {
      return '<li><a href="programme-item.html?slug=' + Site.esc(o.slug) + '">' + Site.esc(Site.clock(o.start) + " " + o.title) + "</a></li>";
    }).join("") + "</ul>" : "") +
    "</div></div>";
})();
