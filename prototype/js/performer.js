/* Performer detail: profile plus all of their sessions (derived from the programme data). */
(function () {
  "use strict";
  var p = Site.performerBySlug[Site.params().slug || ""];
  var out = document.getElementById("content");
  if (!p) {
    Site.init({ nav: "performers", crumbs: [["Home", "index.html"], ["Performers", "performers.html"], ["Performer not found"]] });
    document.title = "Performer not found | Atardecer Bachata Festival (prototype)";
    out.innerHTML = '<h1>Performer not found</h1><div class="empty"><p>We could not find that performer.</p><p><a class="btn btn-primary" href="performers.html">Back to performers</a></p></div>';
    return;
  }
  Site.init({ nav: "performers", crumbs: [["Home", "index.html"], ["Performers", "performers.html"], [p.name]] });
  document.title = p.name + " | Atardecer Bachata Festival (prototype)";
  var sessions = Site.sessionsOf(p.id);
  var styles = p.styles.map(function (s) { return Site.label("styles", s); }).join(", ");
  out.innerHTML =
    '<div class="layout-detail"><div><h1>' + Site.esc(p.name) + "</h1>" +
    '<ul class="tags" aria-label="About this performer"><li class="tag">' + Site.esc(Site.label("performerTypes", p.type)) + '</li><li class="tag">' + Site.esc(Site.country(p.country)) + "</li></ul>" +
    "<p>" + Site.esc(p.bio) + "</p>" +
    (p.members.length ? "<p><strong>Dancers:</strong> " + p.members.map(Site.esc).join(" and ") + "</p>" : "") +
    "<p><strong>Styles:</strong> " + Site.esc(styles) + "</p>" +
    "<h2>" + (sessions.length === 1 ? "Session" : "All " + sessions.length + " sessions") + "</h2>" +
    '<ul class="card-list">' + sessions.map(function (s) { return Site.sessionCard(s); }).join("") + "</ul>" +
    '<aside class="note"><strong>Scenarios 2 and 3 end here.</strong> A DJ page shows the set time; an instructor page lists every workshop with a Save button.</aside></div>' +
    '<div><div class="ph ph-square" role="img" aria-label="Image placeholder: portrait of ' + Site.esc(p.name) + '">Image placeholder<br>Portrait, 1:1</div></div></div>';
})();
