/* "Which level am I?" quiz on the Programme page. Five questions, each worth 0 to 2 points.
   0-3 points: Beginner, 4-7: Intermediate, 8-10: Advanced. The result applies the Programme filters. */
(function () {
  "use strict";
  Site.ready(function () {
    var box = document.getElementById("quiz"), form = document.getElementById("quiz-form");
    if (!box || !form) return;
    box.hidden = false;
    var err = document.getElementById("quiz-err"), out = document.getElementById("quiz-result");
    var levels = {
      beginner: { label: "Beginner", text: "You are at the start or you know the basic step. Choose beginner workshops, they are held in the daytime and no partner is needed." },
      intermediate: { label: "Intermediate", text: "You can dance a full song with turns and you feel the music. Choose intermediate workshops to build variety and connection." },
      advanced: { label: "Advanced", text: "You dance often and want to refine technique. Choose advanced workshops, or stay in the intermediate ones if you want a relaxed session." }
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var score = 0, missing = [];
      for (var i = 1; i <= 5; i++) {
        var checked = form.querySelector('input[name="q' + i + '"]:checked');
        if (checked) score += parseInt(checked.value, 10); else missing.push(i);
      }
      if (missing.length) {
        err.hidden = false;
        err.textContent = "Please answer " + (missing.length === 1 ? "question " + missing[0] : "questions " + missing.join(", ")) + ".";
        form.querySelector('input[name="q' + missing[0] + '"]').focus();
        return;
      }
      err.hidden = true; err.textContent = "";
      var id = score <= 3 ? "beginner" : score <= 7 ? "intermediate" : "advanced", lv = levels[id];
      out.hidden = false;
      out.innerHTML = "<h3>Your level: " + lv.label + "</h3><p>" + lv.text + "</p>" +
        '<p class="btn-row"><a class="btn" id="quiz-go" href="programme.html?type=workshop&amp;level=' + id + '">Show ' + lv.label.toLowerCase() + " workshops</a>" +
        '<button type="button" class="btn btn-2" id="quiz-again">Start again</button></p>';
      out.focus();
      document.getElementById("quiz-go").addEventListener("click", function (ev) {
        var t = document.getElementById("f-type"), l = document.getElementById("f-level");
        if (!t || !l) return;                                  // no filters on this page: follow the link
        ev.preventDefault();
        document.getElementById("f-day").value = ""; document.getElementById("f-venue").value = ""; document.getElementById("f-role").value = ""; document.getElementById("f-daypart").value = "";
        t.value = "workshop"; l.value = id;
        document.getElementById("filter-form").dispatchEvent(new Event("change", { bubbles: true }));
        var f = document.getElementById("filters"); if (f) f.open = true;
        box.open = false;
        var r = document.getElementById("results-title");
        if (r) { r.parentNode.scrollIntoView(); }
        Site.toast("Showing " + lv.label.toLowerCase() + " workshops");
      });
      document.getElementById("quiz-again").addEventListener("click", function () {
        form.reset(); out.hidden = true; out.innerHTML = "";
        form.querySelector('input[name="q1"]').focus();
      });
    });
  });
})();
