/* Atardecer Bachata Festival: Seminar 3 prototype.
   Shared code: data helpers, simulated account, My Programme store, header and footer.
   Plain JavaScript, no build step, works from file://. Data comes from js/data.js (window.FESTIVAL_DATA). */
(function () {
  "use strict";

  var D = window.FESTIVAL_DATA;
  var Site = { data: D };
  window.Site = Site;

  /* ------------------------------------------------------------ small helpers */
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  Site.esc = esc;

  function norm(s) {
    return String(s == null ? "" : s).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  }
  Site.norm = norm;

  Site.params = function () {
    var out = {};
    var q = window.location.search.replace(/^\?/, "");
    if (!q) return out;
    q.split("&").forEach(function (pair) {
      var kv = pair.split("=");
      try { out[decodeURIComponent(kv[0])] = decodeURIComponent((kv[1] || "").replace(/\+/g, " ")); } catch (e) { /* ignore bad escapes */ }
    });
    return out;
  };

  /* ------------------------------------------------------------ data lookups */
  var byId = function (list) { var m = {}; list.forEach(function (x) { m[x.id] = x; }); return m; };
  var bySlug = function (list) { var m = {}; list.forEach(function (x) { m[x.slug] = x; }); return m; };
  Site.items = D.programmeItems.slice().sort(function (a, b) { return a.start < b.start ? -1 : a.start > b.start ? 1 : 0; });
  Site.itemById = byId(D.programmeItems);
  Site.itemBySlug = bySlug(D.programmeItems);
  Site.performerById = byId(D.performers);
  Site.performerBySlug = bySlug(D.performers);
  Site.venueById = byId(D.venues);
  Site.dayById = byId(D.days);
  Site.cat = D.categories;

  Site.label = function (group, id) {
    var list = D.categories[group] || [];
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i].label;
    return id;
  };
  Site.roleLabel = function (id) { return Site.label("roleFocus", id); };

  Site.performersOf = function (item) {
    return item.performerIds.map(function (id) { return Site.performerById[id]; }).filter(Boolean);
  };
  Site.sessionsOf = function (performerId) {
    return Site.items.filter(function (i) { return i.performerIds.indexOf(performerId) > -1; });
  };
  Site.sessionsAt = function (venueId) {
    return Site.items.filter(function (i) { return i.venueId === venueId; });
  };
  Site.country = function (code) {
    try { return new Intl.DisplayNames(["en"], { type: "region" }).of(code) || code; } catch (e) { return code; }
  };

  /* ------------------------------------------------------------ time (all festival times are Europe/Madrid, read from the ISO text) */
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  Site.clock = function (iso) { return iso.slice(11, 16); };
  Site.range = function (item) { return Site.clock(item.start) + "–" + Site.clock(item.end); };
  Site.dateLong = function (dayId) {
    var d = Site.dayById[dayId];
    var n = d.date.split("-");
    return d.label + " " + parseInt(n[2], 10) + " " + MONTHS[parseInt(n[1], 10) - 1];
  };
  Site.when = function (item) {
    var d = Site.dayById[item.dayId];
    if (item.start.slice(0, 10) !== d.date) return d.label.slice(0, 3) + " night " + Site.range(item) + " (after midnight)";
    return d.label.slice(0, 3) + " " + Site.range(item);
  };

  /* ------------------------------------------------------------ safe storage */
  function sGet(key, fallback) {
    try { var v = localStorage.getItem(key); return v === null ? fallback : JSON.parse(v); } catch (e) { return fallback; }
  }
  function sSet(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); return true; } catch (e) { return false; }
  }
  var K_USERS = "atardecer.users", K_SESSION = "atardecer.session", K_PROG = "atardecer.programme.", K_PENDING = "atardecer.pending";
  Site.storageOk = (function () { try { localStorage.setItem("atardecer.test", "1"); localStorage.removeItem("atardecer.test"); return true; } catch (e) { return false; } })();

  /* ------------------------------------------------------------ simulated account (no backend, password never stored) */
  Site.currentUser = function () {
    var id = sGet(K_SESSION, null);
    if (!id) return null;
    var users = sGet(K_USERS, []);
    for (var i = 0; i < users.length; i++) if (users[i].id === id) return users[i];
    return null;
  };
  Site.signUp = function (name, email) {
    var users = sGet(K_USERS, []);
    var e = email.trim().toLowerCase();
    for (var i = 0; i < users.length; i++) if (users[i].email === e) return { error: "An account with this email already exists in this browser. Please log in." };
    var user = { id: "u-" + Date.now().toString(36) + Math.floor(Math.random() * 1000).toString(36), name: name.trim(), email: e };
    users.push(user);
    if (!sSet(K_USERS, users)) return { error: "This browser blocks storage, so the demo account cannot be created." };
    sSet(K_SESSION, user.id);
    return { user: user };
  };
  Site.logIn = function (email) {
    var users = sGet(K_USERS, []);
    var e = email.trim().toLowerCase();
    for (var i = 0; i < users.length; i++) {
      if (users[i].email === e) { sSet(K_SESSION, users[i].id); return { user: users[i] }; }
    }
    return { error: "No account in this browser. Please sign up first." };
  };
  Site.logOut = function () { try { localStorage.removeItem(K_SESSION); } catch (e) { /* ignore */ } };
  Site.resetDemo = function () {
    try {
      var drop = [];
      for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k && k.indexOf("atardecer.") === 0) drop.push(k); }
      drop.forEach(function (k) { localStorage.removeItem(k); });
      sessionStorage.removeItem(K_PENDING);
    } catch (e) { /* ignore */ }
  };

  /* ------------------------------------------------------------ My Programme */
  Site.saved = function () {
    var u = Site.currentUser();
    return u ? sGet(K_PROG + u.id, []) : [];
  };
  Site.isSaved = function (id) { return Site.saved().indexOf(id) > -1; };
  function writeSaved(list) { var u = Site.currentUser(); if (u) sSet(K_PROG + u.id, list); }

  Site.clashes = function (ids) {
    var list = ids.map(function (id) { return Site.itemById[id]; }).filter(Boolean);
    var out = {};
    for (var i = 0; i < list.length; i++) {
      for (var j = i + 1; j < list.length; j++) {
        var a = list[i], b = list[j];
        if (Date.parse(a.start) < Date.parse(b.end) && Date.parse(b.start) < Date.parse(a.end)) {
          (out[a.id] = out[a.id] || []).push(b);
          (out[b.id] = out[b.id] || []).push(a);
        }
      }
    }
    return out;
  };

  /* Toggle a session. Logged out: remember it, go to the simulated login, come back, finish the save. */
  Site.toggleSave = function (id) {
    var u = Site.currentUser();
    if (!u) {
      try { sessionStorage.setItem(K_PENDING, id); } catch (e) { /* ignore */ }
      var here = window.location.pathname.split("/").pop() + window.location.search;
      window.location.href = "login.html?reason=save&next=" + encodeURIComponent(here);
      return "login";
    }
    var list = writeSavedList();
    var idx = list.indexOf(id);
    if (idx > -1) { list.splice(idx, 1); writeSaved(list); return "removed"; }
    list.push(id); writeSaved(list); return "saved";
  };
  function writeSavedList() { return Site.saved().slice(); }

  function finishPending() {
    if (!Site.currentUser()) return null;   // keep the pending save until the visitor is logged in
    var id = null;
    try { id = sessionStorage.getItem(K_PENDING); sessionStorage.removeItem(K_PENDING); } catch (e) { /* ignore */ }
    if (id && Site.itemById[id]) {
      var list = Site.saved();
      if (list.indexOf(id) === -1) { list.push(id); writeSaved(list); }
      return Site.itemById[id];
    }
    return null;
  }

  /* ------------------------------------------------------------ shared markup */
  Site.tagsFor = function (item) {
    var t = [
      '<li class="tag">' + esc(Site.label("types", item.type)) + "</li>",
      '<li class="tag">' + esc(Site.label("levels", item.level)) + "</li>",
      '<li class="tag">' + esc(Site.roleLabel(item.roleFocus)) + "</li>",
      '<li class="tag tag-' + item.dayPart + '">' + esc(item.dayPart === "night" ? "Night" : "Day") + "</li>",
    ];
    return '<ul class="tags" aria-label="Session details">' + t.join("") + "</ul>";
  };

  Site.saveButton = function (item) {
    var on = Site.isSaved(item.id);
    return '<button type="button" class="btn btn-secondary btn-small" data-save="' + esc(item.id) + '" aria-pressed="' + on + '" aria-label="' +
      (on ? "Saved: " : "Save ") + esc(item.title) + (on ? ". Press to remove" : " to My Programme") + '">' + (on ? "Saved ✓" : "Save") + "</button>";
  };

  Site.sessionCard = function (item, opts) {
    opts = opts || {};
    var performers = Site.performersOf(item).map(function (p) {
      return '<a href="performer.html?slug=' + esc(p.slug) + '">' + esc(p.name) + "</a>";
    }).join(", ");
    var venue = Site.venueById[item.venueId];
    return '<li class="card session-row"><div class="when">' + esc(Site.when(item)) + "</div><div>" +
      '<h3><a href="programme-item.html?slug=' + esc(item.slug) + '">' + esc(item.title) + "</a></h3>" +
      Site.tagsFor(item) +
      '<p class="meta">' + esc(venue ? venue.name : "") + (performers ? " · With " + performers : "") + "</p>" +
      (opts.extra || "") + "</div><div>" + (opts.noSave ? "" : Site.saveButton(item)) + (opts.actions || "") + "</div></li>";
  };

  function refreshSaveButtons() {
    var btns = document.querySelectorAll("[data-save]");
    for (var i = 0; i < btns.length; i++) {
      var item = Site.itemById[btns[i].getAttribute("data-save")];
      if (!item) continue;
      var on = Site.isSaved(item.id);
      btns[i].setAttribute("aria-pressed", String(on));
      btns[i].setAttribute("aria-label", (on ? "Saved: " : "Save ") + item.title + (on ? ". Press to remove" : " to My Programme"));
      btns[i].textContent = on ? "Saved ✓" : "Save";
    }
  }

  var toastTimer = null;
  Site.toast = function (msg) {
    var t = document.getElementById("toast");
    if (!t) return;
    t.textContent = msg;
    t.className = "toast show";
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.className = "toast"; }, 3200);
  };

  /* ------------------------------------------------------------ header, breadcrumbs, footer */
  var NAV = [
    ["programme", "Programme", "programme.html"],
    ["performers", "Performers", "performers.html"],
    ["venues", "Venues", "venues.html"],
    ["roots", "Roots", "placeholder.html?page=Roots"],
    ["practical", "Practical info", "placeholder.html?page=Practical%20info"],
    ["my", "My Programme", "my-programme.html"],
  ];

  function authHtml() {
    var u = Site.currentUser();
    var here = window.location.pathname.split("/").pop() + window.location.search;
    if (u) return "<span>Hi, <strong>" + esc(u.name) + '</strong></span><button type="button" class="btn btn-secondary btn-small" id="logout">Log out</button>';
    return '<a href="login.html?next=' + encodeURIComponent(here) + '">Log in / Sign up</a>';
  }

  Site.init = function (opts) {
    opts = opts || {};
    var main = document.getElementById("main");
    var navHtml = NAV.map(function (n) {
      return '<li><a href="' + n[2] + '"' + (opts.nav === n[0] ? ' aria-current="page"' : "") + ">" + n[1] + "</a></li>";
    }).join("") + '<li><a class="btn btn-primary" href="placeholder.html?page=Tickets">Tickets</a></li>';

    var header = document.createElement("div");
    header.innerHTML =
      '<a class="skip-link" href="#main">Skip to main content</a>' +
      '<header class="site-header"><div class="container header-row">' +
      '<div class="bar"><a class="brand" href="index.html"><span class="logo-ph" aria-hidden="true">LOGO</span><span>Atardecer<small>Bachata Festival · Valencia</small></span></a>' +
      '<button class="menu-btn" type="button" aria-expanded="false" aria-controls="main-nav">Menu</button></div>' +
      '<div class="tools"><form class="search-form" role="search" action="search.html" method="get">' +
      '<label for="site-search">Search the festival</label>' +
      '<input id="site-search" name="q" type="search" placeholder="Artist, session or venue" autocomplete="off">' +
      '<button class="btn btn-secondary" type="submit">Search</button></form>' +
      '<div class="auth" id="auth">' + authHtml() + "</div></div></div>" +
      '<nav id="main-nav" class="main-nav" aria-label="Main"><ul class="container">' + navHtml + "</ul></nav></header>";
    while (header.firstChild) document.body.insertBefore(header.firstChild, main);

    if (opts.crumbs) {
      var li = opts.crumbs.map(function (c, i) {
        return i === opts.crumbs.length - 1 ? '<li><span aria-current="page">' + esc(c[0]) + "</span></li>" : '<li><a href="' + c[1] + '">' + esc(c[0]) + "</a></li>";
      }).join("");
      var bc = document.createElement("nav");
      bc.className = "breadcrumb container";
      bc.setAttribute("aria-label", "Breadcrumb");
      bc.innerHTML = "<ol>" + li + "</ol>";
      document.body.insertBefore(bc, main);
    }

    var f = D.festival;
    var footer = document.createElement("footer");
    footer.className = "site-footer";
    footer.innerHTML = '<div class="container"><p><strong>' + esc(f.name) + "</strong><br>" + esc(f.city) + ", " + esc(f.country) + " · 25–27 June 2027 · " +
      '<a href="mailto:' + esc(f.contact.email) + '">' + esc(f.contact.email) + "</a></p>" +
      '<ul><li><a href="placeholder.html?page=Practical%20info">Practical info</a></li><li><a href="placeholder.html?page=Tickets">Tickets</a></li>' +
      '<li><a href="walkthrough.html">Prototype guide</a></li></ul>' +
      "<p>Seminar 3 prototype: mid-fidelity wireframe, grayscale, sample content. Accounts and saved sessions stay in your browser.</p></div>";
    document.body.appendChild(footer);

    var toast = document.createElement("div");
    toast.id = "toast"; toast.className = "toast"; toast.setAttribute("role", "status"); toast.setAttribute("aria-live", "polite");
    document.body.appendChild(toast);

    var btn = document.querySelector(".menu-btn");
    var nav = document.getElementById("main-nav");
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.focus(); }
    });

    var lo = document.getElementById("logout");
    if (lo) lo.addEventListener("click", function () { Site.logOut(); window.location.href = "index.html"; });

    document.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("[data-save]") : null;
      if (!b) return;
      var item = Site.itemById[b.getAttribute("data-save")];
      var res = Site.toggleSave(item.id);
      if (res === "login") return;
      refreshSaveButtons();
      Site.toast(res === "saved" ? "Saved to My Programme: " + item.title : "Removed from My Programme: " + item.title);
      document.dispatchEvent(new CustomEvent("programme-changed"));
    });

    var done = finishPending();
    if (done) { refreshSaveButtons(); Site.toast("Saved to My Programme: " + done.title); }

    if (!Site.storageOk) {
      var w = document.createElement("p");
      w.className = "banner banner-warn container";
      w.textContent = "This browser blocks storage, so sign-up and saved sessions will not work in the demo.";
      document.body.insertBefore(w, main);
    }
  };
})();
