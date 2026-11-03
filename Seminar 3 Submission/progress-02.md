# Progress 02: Seminar 3 (prototype)

**Festival:** Atardecer Bachata Festival, Valencia, 25–27 June 2027.
**Team:** Faiaz Hossain Mazumder Yen, Oscar Muz, Sebastian Betancur.
**Date:** 2026-11-03.

## What we submit
- **Prototype:** the `prototype/` folder. It is a mid-fidelity wireframe in plain HTML, CSS and JavaScript. No installation: double-click `prototype/index.html`. Start with the "Prototype guide" link in the footer. It lists the two key scenarios step by step and has a button that resets the demo.
- **Look:** grayscale on purpose (team rule: mid-fidelity wireframes). Images are labelled gray boxes. The sample content comes from `data.json` (65 sessions, 64 performers, 3 venues).
- **Mobile first:** the default layout is a phone (320 px and up). At 900 px and wider the layout changes: header in two rows, filters in a left column, detail pages in two columns.
- **Screens in the prototype (9 plus a guide):** Home, Programme with filters, Session detail, Performers, Performer detail, Search results, My Programme, Log in / Sign up, a placeholder for planned pages, and the Prototype guide. Venues, Roots, Practical info and Tickets are in the navigation, but they open a short placeholder because they are outside the two key scenarios.
- **Navigation and hierarchy:** main menu (Programme, Performers, Venues, Roots, Practical info, My Programme) with a Tickets button, a search field and login status in every header, breadcrumbs on every inner page, and a skip link. On a phone the menu folds under a Menu button. Home shows what and when first, then the two key buttons, then the two moods (day and night), people, and the personal programme.

## 1. Proposed functions
Four functions are built in the prototype. Four more are planned from the specification for the real build.

| # | Function | In the prototype |
|---|---|---|
| 1 | Programme filters: day, venue, type, level, role focus, day or night, with a result count and a clear button | Yes |
| 2 | Search (header field and a results page grouped by performers, sessions and venues), plus a name filter on the performers list | Yes |
| 3 | My Programme: save and remove sessions, clash warning, calendar file download | Yes |
| 4 | Simulated sign-up and login (needed because My Programme is personal; teacher feedback from Seminar 2) | Yes |
| 5 | Day/Night colour theme | Planned (needs colour, not in a grayscale wireframe) |
| 6 | "Which level am I?" quiz | Planned |
| 7 | Interactive venue map | Planned |
| 8 | FAQ accordion | Planned |

## 2. How the functions meet user needs

| Function | User need | Target group and scenario | Where in the prototype |
|---|---|---|---|
| 1 Filters | Beginners find workshops at their level and role. Night dancers find tonight's socials. | Groups 1 and 2, Scenarios 1 and 2 | Programme page (and links from the two moods on Home) |
| 2 Search | Returning visitors find one artist by name and see everything they do. | Group 3, Scenario 3 | Header on every page, Search results, Performers |
| 3 My Programme | A personal schedule with no clashes that can be taken away. | Groups 1 and 2, Scenario 1 | Save button on every session, My Programme |
| 4 Simulated login | A personal programme belongs to a person and is kept when they come back. | Group 1, Scenarios 1 and 6 | Log in / Sign up, header status |

None of these is only a menu or a slideshow. Each one changes what the visitor sees or keeps something for them.

## 3. What we verified, and how
Details and results are in `docs/evidence/prototype-verification.md`, with screenshots.

- **Key scenario 1 (phone, 375 px):** filter Saturday beginner follower workshops (4 results), press Save while logged out, sign up, return to the session list with the first workshop saved, save a second one, and see both in My Programme with "No clashes". Passed.
- **Key scenario 2 (desktop, 1280 px):** filter Friday, Social, Night, Marea Club (4 sessions), open the 22:00 session, follow the DJ link, and read the set times. Passed.
- **Extra checks:** clash warning (an overlapping session is flagged in text and removed again), search with accents ("raiz" finds "Raíz"), log out and log in again restores the saved sessions, the phone menu opens and closes with the keyboard, the password is never stored.
- **Layout and accessibility, by an automated page check:** 11 pages at 320 px and 7 pages at 1280 px. One h1 per page, no skipped heading levels, every input labelled, every button named, no horizontal overflow, touch targets of at least 44 px, no duplicate ids. The prototype makes no network requests.
- **Problems found by testing and fixed:** (1) a pending Save was lost on the login page, so the first workshop was not saved after sign-up; (2) the performers list skipped a heading level; (3) the filter panel title had no space; (4) sets after midnight read "Fri 00:00", now "Fri night 00:00–01:30 (after midnight)"; (5) on a phone the filters filled a whole screen, so they are now two columns and fold away when filters are preset.

**Not verified yet:** opening by double-click in Chrome, Safari and Firefox (the test used a local web server; the code uses no network calls and only `localStorage`, which these browsers allow on file pages, but the team has to confirm it); screen readers; tablets; testing with real users; opening the downloaded calendar file in a calendar app.

## 4. Use of AI, and how we checked it
**What AI did (Claude Code):** proposed the page and function plan, wrote the prototype code (HTML, CSS, JavaScript), generated the sample data earlier in the project, wrote the design kit (palette options, type, image brief), ran the browser tests, and drafted this file.

**What we decided ourselves:**
- The prototype stays mid-fidelity grayscale; the brand look is for the real build.
- Palette A "Golden Hour" and the fonts Fraunces and Source Sans 3 for the build (`docs/design-kit.md`).
- Illustrated avatars for the 56 non-featured performers.
- Scenarios 1 and 2 as the two key scenarios; the simulated login flow after the teacher's feedback.

**How we checked AI output:** we did not accept "it looks right". We ran both scenarios step by step in a real browser, checked data with a script (a validation script, 0 errors), counted headings, labels, overflow and touch targets on every page, and wrote down the five bugs the tests found (section 3). Contrast of the three palette options was calculated, not guessed.

**Accepted:** the page structure, the four functions, the filter and search logic, the design kit.
**Modified:** after testing, the pending-save logic, the time label for late sets, and the phone filter layout.
**Rejected:** colours and photos in the prototype (team rule), and showing placeholder pages as finished designs.
**Limits and errors of AI work:** the AI first lost a saved session on the login page and mislabelled late-night sessions; both were found only by running the scenarios. The browser tool could not open `file://` pages with scripts, so double-click opening is still for the team to check. Sample bios and descriptions are fictional and formulaic.

## Next
Next phase: build the real site in `web/` from the specification, apply the Golden Hour look and the generated images, and add the planned functions (theme, level quiz, map, FAQ).
