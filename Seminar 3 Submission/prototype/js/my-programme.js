/* My Programme: saved sessions per simulated account, clash warnings, calendar download. */
(function () {
  "use strict";
  Site.init({ nav: "my", crumbs: [["Home", "index.html"], ["My Programme"]] });
  var out = document.getElementById("content");

  function ics(items) {
    function stamp(iso) { return new Date(iso).toISOString().replace(/[-:]/g, "").split(".")[0] + "Z"; }
    function t(s) { return String(s).replace(/\\/g, "\\\\").replace(/;/g, "\;").replace(/,/g, "\\,").replace(/\n/g, "\\n"); }
    var lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Atardecer Bachata Festival//Prototype//EN", "CALSCALE:GREGORIAN"];
    items.forEach(function (it) {
      var v = Site.venueById[it.venueId];
      lines.push("BEGIN:VEVENT", "UID:" + it.id + "@atardecer.example", "DTSTAMP:" + stamp(new Date().toISOString()),
        "DTSTART:" + stamp(it.start), "DTEND:" + stamp(it.end), "SUMMARY:" + t(it.title),
        "LOCATION:" + t(v.name + ", " + v.address.streetAddress + ", " + v.address.addressLocality), "DESCRIPTION:" + t(it.description), "END:VEVENT");
    });
    lines.push("END:VCALENDAR");
    return lines.join("\r\n");
  }

  function render() {
    var u = Site.currentUser();
    if (!u) {
      out.innerHTML = '<div class="empty"><p><strong>Log in to see your programme.</strong></p>' +
        "<p>My Programme is personal. Sign up takes a name and an email. It is a demo: nothing leaves your browser.</p>" +
        '<div class="btn-row"><a class="btn btn-primary" href="login.html?next=my-programme.html">Log in / Sign up</a><a class="btn btn-secondary" href="programme.html">Browse the programme</a></div></div>';
      return;
    }
    var ids = Site.saved();
    var items = ids.map(function (id) { return Site.itemById[id]; }).filter(Boolean).sort(function (a, b) { return a.start < b.start ? -1 : 1; });
    var clash = Site.clashes(ids);
    var nClash = Object.keys(clash).length;

    var html = "<p>Hi, <strong>" + Site.esc(u.name) + "</strong>. These sessions are saved in this browser.</p>";
    if (!items.length) {
      out.innerHTML = html + '<div class="empty"><p><strong>You have not saved any sessions yet.</strong></p><p><a class="btn btn-primary" href="programme.html">Find sessions</a></p></div>';
      return;
    }
    html += '<p class="count">' + items.length + (items.length === 1 ? " session saved" : " sessions saved") + "</p>";
    html += nClash ? '<p class="banner banner-warn" role="status">⚠ Clash: ' + nClash + " of your sessions overlap. Remove one of each pair.</p>"
                   : '<p class="banner" role="status">✓ No clashes. All your sessions fit together.</p>';
    Site.data.days.forEach(function (d) {
      var day = items.filter(function (i) { return i.dayId === d.id; });
      if (!day.length) return;
      html += "<h2>" + Site.esc(Site.dateLong(d.id)) + "</h2>" + '<ul class="card-list">' + day.map(function (it) {
        var warn = (clash[it.id] || []).map(function (o) {
          return '<p class="clash">⚠ Clash with “' + Site.esc(o.title) + "” (" + Site.esc(Site.range(o)) + ")</p>";
        }).join("");
        return Site.sessionCard(it, { extra: warn, noSave: true, actions: '<button type="button" class="btn btn-secondary btn-small" data-save="' + Site.esc(it.id) + '" aria-pressed="true" aria-label="Remove ' + Site.esc(it.title) + ' from My Programme">Remove</button>' });
      }).join("") + "</ul>";
    });
    html += '<div class="btn-row"><button type="button" class="btn btn-primary" id="dl">Download calendar (.ics)</button><a class="btn btn-secondary" href="programme.html">Add more sessions</a></div>';
    out.innerHTML = html;
    document.getElementById("dl").addEventListener("click", function () {
      var blob = new Blob([ics(items)], { type: "text/calendar" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob); a.download = "my-programme-atardecer.ics";
      document.body.appendChild(a); a.click(); a.remove();
      Site.toast("Calendar file downloaded");
    });
  }

  // the shared click handler toggles a save; here we only redraw. The button label stays "Remove" on this page.
  document.addEventListener("programme-changed", function () { render(); });
  render();
})();
