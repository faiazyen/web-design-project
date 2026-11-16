/* Atardecer Bachata Festival: shared code for every page.
   The pages are complete HTML without this file. This code only adds: the phone menu, Day/Night switch, login status,
   Save buttons and the toast. Plain JavaScript, no build step, works from file://. */
(function () {
  "use strict";

  var root = document.documentElement.getAttribute("data-root") || "";
  var D = window.FESTIVAL_DATA || null;           // only loaded on Search and My Programme
  var Site = { root: root, data: D };
  window.Site = Site;

  /* ------------------------------------------------------------ helpers */
  Site.esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  };
  Site.norm = function (s) { return String(s == null ? "" : s).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); };
  Site.params = function () {
    var out = {}, q = window.location.search.replace(/^\?/, "");
    if (!q) return out;
    q.split("&").forEach(function (pair) {
      var kv = pair.split("=");
      try { out[decodeURIComponent(kv[0])] = decodeURIComponent((kv[1] || "").replace(/\+/g, " ")); } catch (e) { /* ignore bad escapes */ }
    });
    return out;
  };
  Site.here = function () {   // path of this page relative to the site folder, for example sessions/x.html
    var parts = window.location.pathname.split("/"), depth = root.split("../").length - 1;
    return parts.slice(parts.length - 1 - depth).join("/") + window.location.search;
  };

  /* ------------------------------------------------------------ safe storage */
  function sGet(key, fallback) { try { var v = localStorage.getItem(key); return v === null ? fallback : JSON.parse(v); } catch (e) { return fallback; } }
  function sSet(key, val) { try { localStorage.setItem(key, JSON.stringify(val)); return true; } catch (e) { return false; } }
  var K_USERS = "atardecer.users", K_SESSION = "atardecer.session", K_PROG = "atardecer.programme.", K_PENDING = "atardecer.pending", K_THEME = "atardecer.theme";
  Site.storageOk = (function () { try { localStorage.setItem("atardecer.test", "1"); localStorage.removeItem("atardecer.test"); return true; } catch (e) { return false; } })();

  /* ------------------------------------------------------------ simulated account (no backend, the password is never stored) */
  Site.currentUser = function () {
    var id = sGet(K_SESSION, null);
    if (!id) return null;
    var users = sGet(K_USERS, []);
    for (var i = 0; i < users.length; i++) if (users[i].id === id) return users[i];
    return null;
  };
  Site.signUp = function (name, email) {
    var users = sGet(K_USERS, []), e = email.trim().toLowerCase();
    for (var i = 0; i < users.length; i++) if (users[i].email === e) return { error: "An account with this email already exists in this browser. Please log in." };
    var user = { id: "u-" + Date.now().toString(36) + Math.floor(Math.random() * 1000).toString(36), name: name.trim(), email: e };
    users.push(user);
    if (!sSet(K_USERS, users)) return { error: "This browser blocks storage, so the demo account cannot be created." };
    sSet(K_SESSION, user.id);
    return { user: user };
  };
  Site.logIn = function (email) {
    var users = sGet(K_USERS, []), e = email.trim().toLowerCase();
    for (var i = 0; i < users.length; i++) if (users[i].email === e) { sSet(K_SESSION, users[i].id); return { user: users[i] }; }
    return { error: "No account in this browser. Please sign up first." };
  };
  Site.logOut = function () { try { localStorage.removeItem(K_SESSION); } catch (e) { /* ignore */ } };

  /* ------------------------------------------------------------ My Programme store */
  Site.saved = function () { var u = Site.currentUser(); return u ? sGet(K_PROG + u.id, []) : []; };
  Site.isSaved = function (id) { return Site.saved().indexOf(id) > -1; };
  function writeSaved(list) { var u = Site.currentUser(); if (u) sSet(K_PROG + u.id, list); }

  /* Toggle a session. Logged out: remember it, go to the simulated login, come back, finish the save. */
  Site.toggleSave = function (id, title) {
    if (!Site.currentUser()) {
      try { sessionStorage.setItem(K_PENDING, JSON.stringify({ id: id, title: title })); } catch (e) { /* ignore */ }
      window.location.href = root + "login.html?reason=save&next=" + encodeURIComponent(Site.here());
      return "login";
    }
    var list = Site.saved().slice(), idx = list.indexOf(id);
    if (idx > -1) { list.splice(idx, 1); writeSaved(list); return "removed"; }
    list.push(id); writeSaved(list); return "saved";
  };
  function finishPending() {
    if (!Site.currentUser()) return null;   // keep the pending save until the visitor is logged in
    var p = null;
    try { p = JSON.parse(sessionStorage.getItem(K_PENDING)); sessionStorage.removeItem(K_PENDING); } catch (e) { p = null; }
    if (p && p.id) {
      var list = Site.saved().slice();
      if (list.indexOf(p.id) === -1) { list.push(p.id); writeSaved(list); }
      return p;
    }
    return null;
  }

  /* ------------------------------------------------------------ Save buttons on static pages */
  function refreshSaveButtons() {
    var btns = document.querySelectorAll("[data-save]");
    for (var i = 0; i < btns.length; i++) {
      var b = btns[i], id = b.getAttribute("data-save"), title = b.getAttribute("data-title") || "";
      b.hidden = false;
      if (b.getAttribute("data-mode") === "remove") continue;
      var on = Site.isSaved(id);
      b.setAttribute("aria-pressed", String(on));
      b.setAttribute("aria-label", (on ? "Saved: " : "Save ") + title + (on ? ". Press to remove" : " to My Programme"));
      b.textContent = on ? "Saved ✓" : "Save";
    }
  }
  Site.refreshSaveButtons = refreshSaveButtons;

  var toastTimer = null;
  Site.toast = function (msg) {
    var t = document.getElementById("toast");
    if (!t) return;
    t.textContent = msg;
    t.className = "toast show";
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.className = "toast"; }, 3200);
  };

  /* ------------------------------------------------------------ shared data helpers (Search and My Programme only) */
  if (D) {
    var byId = function (list) { var m = {}; list.forEach(function (x) { m[x.id] = x; }); return m; };
    Site.items = D.programmeItems.slice().sort(function (a, b) { return a.start < b.start ? -1 : a.start > b.start ? 1 : 0; });
    Site.itemById = byId(D.programmeItems);
    Site.performerById = byId(D.performers);
    Site.venueById = byId(D.venues);
    Site.dayById = byId(D.days);
    Site.label = function (group, id) { var l = D.categories[group] || []; for (var i = 0; i < l.length; i++) if (l[i].id === id) return l[i].label; return id; };
    Site.country = function (code) { try { return new Intl.DisplayNames(["en"], { type: "region" }).of(code) || code; } catch (e) { return code; } };
    Site.sessionsOf = function (pid) { return Site.items.filter(function (i) { return i.performerIds.indexOf(pid) > -1; }); };
    var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    Site.range = function (it) { return it.start.slice(11, 16) + "–" + it.end.slice(11, 16); };
    Site.dateLong = function (dayId) { var d = Site.dayById[dayId], n = d.date.split("-"); return d.label + " " + parseInt(n[2], 10) + " " + MONTHS[parseInt(n[1], 10) - 1]; };
    Site.when = function (it) {
      var d = Site.dayById[it.dayId];
      return it.start.slice(0, 10) !== d.date ? d.label.slice(0, 3) + " night " + Site.range(it) + " (after midnight)" : d.label.slice(0, 3) + " " + Site.range(it);
    };
    Site.clashes = function (ids) {
      var list = ids.map(function (id) { return Site.itemById[id]; }).filter(Boolean), out = {};
      for (var i = 0; i < list.length; i++) for (var j = i + 1; j < list.length; j++) {
        var a = list[i], b = list[j];
        if (Date.parse(a.start) < Date.parse(b.end) && Date.parse(b.start) < Date.parse(a.end)) { (out[a.id] = out[a.id] || []).push(b); (out[b.id] = out[b.id] || []).push(a); }
      }
      return out;
    };
    Site.sessionCard = function (it, opts) {
      opts = opts || {};
      var v = Site.venueById[it.venueId];
      var people = it.performerIds.map(function (id) { return Site.performerById[id]; }).filter(Boolean).map(function (p) {
        return '<a href="performers/' + Site.esc(p.slug) + '.html">' + Site.esc(p.name) + "</a>";
      }).join(", ");
      var tags = [Site.label("types", it.type), Site.label("levels", it.level), Site.label("roleFocus", it.roleFocus)].map(function (t) { return '<li class="tag">' + Site.esc(t) + "</li>"; }).join("") +
        '<li class="tag tag-' + it.dayPart + '">' + (it.dayPart === "night" ? "Night" : "Day") + "</li>";
      var save = opts.remove
        ? '<button type="button" class="btn btn-2 btn-small" data-save="' + Site.esc(it.id) + '" data-mode="remove" data-title="' + Site.esc(it.title) + '" aria-label="Remove ' + Site.esc(it.title) + ' from My Programme">Remove</button>'
        : '<button type="button" class="btn btn-2 btn-small" data-save="' + Site.esc(it.id) + '" data-title="' + Site.esc(it.title) + '" hidden>Save</button>';
      return '<article class="session"><p class="when">' + Site.esc(Site.when(it)) + '</p><div class="session-main"><h3 class="session-title"><a href="sessions/' + Site.esc(it.slug) + '.html">' + Site.esc(it.title) + "</a></h3>" +
        '<ul class="tags" aria-label="Session details">' + tags + "</ul>" +
        '<p class="meta"><a href="venues/' + Site.esc(v.slug) + '.html">' + Site.esc(v.name) + "</a>" + (people ? " · With " + people : "") + "</p>" + (opts.extra || "") + '</div><div class="session-actions">' + save + "</div></article>";
    };
  }

  /* ------------------------------------------------------------ header: menu, theme, login status */
  function setupHeader() {
    var btn = document.querySelector(".menu-btn"), nav = document.getElementById("main-nav"), tools = document.getElementById("tools");
    if (btn && nav) {   // phones: search, login and the main menu fold behind one Menu button
      btn.hidden = false;
      var setOpen = function (open) { nav.classList.toggle("open", open); if (tools) tools.classList.toggle("open", open); btn.setAttribute("aria-expanded", String(open)); };
      btn.addEventListener("click", function () { setOpen(!nav.classList.contains("open")); });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && nav.classList.contains("open")) { setOpen(false); btn.focus(); }
      });
    }

    var theme = document.getElementById("theme-btn"), html = document.documentElement;
    function paintTheme() {
      var night = html.getAttribute("data-theme") === "night";
      theme.textContent = night ? "Day" : "Night";
      theme.setAttribute("aria-label", night ? "Switch to day mode" : "Switch to night mode");
      var m = document.querySelector('meta[name="theme-color"]'); if (m) m.setAttribute("content", night ? "#0D1B2A" : "#FFF7EC");
    }
    if (theme) {
      theme.hidden = false; paintTheme();
      theme.addEventListener("click", function () {
        var next = html.getAttribute("data-theme") === "night" ? "day" : "night";
        html.setAttribute("data-theme", next);
        try { localStorage.setItem(K_THEME, next); } catch (e) { /* ignore */ }
        paintTheme();
      });
    }

    var auth = document.getElementById("auth"), u = Site.currentUser();
    if (auth) {
      if (u) {
        auth.innerHTML = "Hi, <strong>" + Site.esc(u.name) + '</strong> <button type="button" class="btn btn-2 btn-small" id="logout">Log out</button>';
        document.getElementById("logout").addEventListener("click", function () { Site.logOut(); window.location.href = root + "index.html"; });
      } else {
        auth.querySelector("a").href = root + "login.html?next=" + encodeURIComponent(Site.here());
      }
    }
  }

  function init() {
    setupHeader();
    refreshSaveButtons();
    document.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("[data-save]") : null;
      if (!b) return;
      var id = b.getAttribute("data-save"), title = b.getAttribute("data-title") || "this session";
      var res = Site.toggleSave(id, title);
      if (res === "login") return;
      refreshSaveButtons();
      Site.toast(res === "saved" ? "Saved to My Programme: " + title : "Removed from My Programme: " + title);
      document.dispatchEvent(new CustomEvent("programme-changed"));
    });
    var done = finishPending();
    if (done) { refreshSaveButtons(); Site.toast("Saved to My Programme: " + (done.title || "session")); }
    if (!Site.storageOk) {
      var w = document.createElement("p");
      w.className = "banner banner-warn wrap";
      w.textContent = "This browser blocks storage, so sign-up and saved sessions will not work in the demo.";
      document.body.insertBefore(w, document.getElementById("main"));
    }
  }
  Site.ready = function (fn) { if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn); else fn(); };
  Site.ready(init);
})();
