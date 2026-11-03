/* Placeholder for pages that the specification plans but this prototype does not design. */
(function () {
  "use strict";
  var PLANS = {
    "Venues": "Three venues (Arena Stage on the beach, Pabellón Brisa, Marea Club) with address, access facts, an interactive map and the sessions held there.",
    "Roots": "The story of bachata dominicana: origins, instruments and a short timeline.",
    "Practical info": "One page with sections for Travel, Accommodation, Accessibility, FAQ and Code of conduct.",
    "Tickets": "Passes, prices, what is included and group information."
  };
  var page = Site.params().page || "";
  if (!PLANS.hasOwnProperty(page)) page = "Planned page";
  var nav = { "Venues": "venues", "Roots": "roots", "Practical info": "practical" }[page] || "";
  Site.init({ nav: nav, crumbs: [["Home", "index.html"], [page]] });
  document.title = page + " (not in this prototype) | Atardecer Bachata Festival";
  document.getElementById("h").textContent = page;
  document.getElementById("content").innerHTML =
    '<div class="empty"><p><strong>This page is planned but not designed in the Seminar 3 prototype.</strong></p>' +
    "<p>" + Site.esc(PLANS[page] || "See the project specification.") + "</p>" +
    "<p>The prototype covers the key parts: Home, Programme, Session, Performers, Search, My Programme and Log in / Sign up.</p>" +
    '<div class="btn-row"><a class="btn btn-primary" href="programme.html">Go to the programme</a><a class="btn btn-secondary" href="index.html">Home</a></div></div>';
})();
