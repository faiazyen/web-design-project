/* Simulated sign-up and login. Accounts live in localStorage. The password is checked for presence only and never stored. */
(function () {
  "use strict";
  var p = Site.params();
  Site.init({ nav: "", crumbs: [["Home", "index.html"], ["Log in / Sign up"]] });

  var next = /^[a-z0-9-]+\.html(\?[^#\s]*)?$/i.test(p.next || "") ? p.next : "my-programme.html";
  var reason = document.getElementById("reason");
  if (p.reason === "save") { reason.hidden = false; reason.textContent = "Log in or sign up to save sessions to your own programme. We will bring you back and save it."; }

  if (Site.currentUser()) {
    var box = document.createElement("p");
    box.className = "banner";
    box.innerHTML = "You are logged in as <strong>" + Site.esc(Site.currentUser().name) + '</strong>. <a href="' + Site.esc(next) + '">Continue</a>';
    document.querySelector(".layout-two").before(box);
  }

  function setErr(id, msg, inputId) {
    var e = document.getElementById(id), inp = document.getElementById(inputId);
    e.hidden = !msg; e.textContent = msg || "";
    if (msg) inp.setAttribute("aria-invalid", "true"); else inp.removeAttribute("aria-invalid");
  }
  function validEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); }
  function firstBad(list) { for (var i = 0; i < list.length; i++) if (list[i]) return list[i]; return null; }

  document.getElementById("signup").addEventListener("submit", function (e) {
    e.preventDefault();
    var name = document.getElementById("su-name").value, email = document.getElementById("su-email").value, pass = document.getElementById("su-pass").value;
    var bad = [];
    setErr("su-name-err", name.trim() ? "" : "Please enter your name.", "su-name"); if (!name.trim()) bad.push("su-name");
    var emailMsg = !email.trim() ? "Please enter your email." : (!validEmail(email) ? "Please enter an email like name@example.com." : "");
    setErr("su-email-err", emailMsg, "su-email"); if (emailMsg) bad.push("su-email");
    setErr("su-pass-err", pass ? "" : "Please enter a demo password (any text).", "su-pass"); if (!pass) bad.push("su-pass");
    if (bad.length) { document.getElementById(bad[0]).focus(); return; }
    var res = Site.signUp(name, email);
    if (res.error) { setErr("su-email-err", res.error, "su-email"); document.getElementById("su-email").focus(); return; }
    window.location.href = next;
  });

  document.getElementById("login").addEventListener("submit", function (e) {
    e.preventDefault();
    var email = document.getElementById("li-email").value, pass = document.getElementById("li-pass").value;
    var bad = [];
    var emailMsg = !email.trim() ? "Please enter your email." : (!validEmail(email) ? "Please enter an email like name@example.com." : "");
    setErr("li-email-err", emailMsg, "li-email"); if (emailMsg) bad.push("li-email");
    setErr("li-pass-err", pass ? "" : "Please enter your demo password.", "li-pass"); if (!pass) bad.push("li-pass");
    if (bad.length) { document.getElementById(bad[0]).focus(); return; }
    var res = Site.logIn(email);
    if (res.error) { setErr("li-email-err", res.error, "li-email"); document.getElementById("li-email").focus(); return; }
    window.location.href = next;
  });
})();
