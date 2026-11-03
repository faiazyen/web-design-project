# Progress 02: Seminar 3 (prototype)

**Festival:** Atardecer Bachata Festival, Valencia, 25–27 June 2027. **Team:** Faiaz Hossain Mazumder Yen, Oscar Muz, Sebastian Betancur. **Date:** 2026-11-03.

## Prototype
- **Live link (any computer, no installation):** https://faiazyen.github.io/web-design-project/prototype/
- **Offline:** open `prototype/index.html` by double-click. The footer link "Prototype guide" walks through both key scenarios and has a button that resets the demo.
- **What it is:** a mid-fidelity wireframe in plain HTML, CSS and JavaScript, built from the project specification. It is grayscale on purpose (team rule); images are labelled boxes. The sample content comes from `data.json` (65 sessions, 64 performers, 3 venues).
- **Mobile first:** the default layout is a phone (320 px and up). From 900 px wide the layout changes: header in two rows, filters in a left column, detail pages in two columns.
- **Screens:** Home, Programme, Session detail, Performers, Performer detail, Venues, Search results, My Programme, Log in / Sign up, plus a Prototype guide. Roots, Practical info and Tickets are in the navigation but open a short placeholder, because they are outside the two key scenarios.
- **Navigation and hierarchy:** main menu with a Tickets button, a search field and login status in every header, breadcrumbs, a skip link, and a Menu button on phones. Home shows what and when first, then the two key actions, the two moods (day, night), people, and the personal programme.

## 1. Proposed functions
| # | Function | In the prototype |
|---|---|---|
| 1 | Programme filters: day, venue, type, level, role focus, day or night | Yes |
| 2 | Search (header field, results grouped by performers, sessions, venues) and a name filter on Performers | Yes |
| 3 | My Programme: save and remove sessions, clash warning, calendar download | Yes |
| 4 | Simulated sign-up and login (My Programme is personal; teacher feedback from Seminar 2) | Yes |
| 5–8 | Day/Night theme, level quiz, venue map, FAQ accordion | Planned for the build |

## 2. How the functions meet user needs
| Function | User need | Group and scenario |
|---|---|---|
| 1 Filters | Beginners find workshops at their level and role. Night dancers find tonight's socials. | Groups 1 and 2, Scenarios 1 and 2 |
| 2 Search | A returning visitor finds one artist by name and sees every session. | Group 3, Scenario 3 |
| 3 My Programme | A personal schedule with no clashes that can be taken away. | Groups 1 and 2, Scenario 1 |
| 4 Simulated login | A personal programme belongs to a person and is kept when they come back. | Group 1, Scenarios 1 and 6 |

Each one changes what the visitor sees or keeps something for them. None is only a menu or a slideshow.

## 3. What we verified, and how
Full record and screenshots: `docs/evidence/prototype-verification.md`.
- **Key scenario 1 (phone, 375 px):** filter Saturday beginner follower workshops (4 results), Save while logged out, sign up, return with the first workshop saved, save a second one, see both in My Programme with "No clashes". **Passed**, on a local test server and again on the live site.
- **Key scenario 2 (desktop, 1280 px):** filter Friday, Social, Night, Marea Club (4 sessions), open the 22:00 session, follow the DJ link to the set times. **Passed**, locally and on the live site.
- **Opening by double-click:** all main pages were opened from `file://` in real Chrome: they render, and browser storage is available. Safari and Firefox were not tested.
- **Extra checks:** clash warning, accent-insensitive search ("raiz" finds "Raíz"), log out and in again, phone menu with the keyboard, no password stored, the downloaded calendar file has valid events and times (09:30 Madrid time is 07:30 UTC).
- **Layout and accessibility (automated page check, 320 px and 1280 px):** one h1 per page, no skipped heading levels, every input labelled, every button named, no horizontal overflow, touch targets of at least 44 px, no external requests.
- **Problems found by testing and fixed:** a pending Save was lost on the login page; the performers list skipped a heading level; the filter title lacked a space; sets after midnight read "Fri 00:00"; on a phone the filters filled a whole screen.
- **Not verified:** screen readers, tablets, real users.

## 4. Use of AI, and how we checked it
- **What AI (Claude Code) did:** planned the screens and functions, wrote the prototype code, wrote the design kit (palette, type, image brief), ran the browser tests, and drafted this file and the slides.
- **What we decided:** grayscale mid-fidelity for the prototype; scenarios 1 and 2 as the key scenarios; the simulated login; for the build, palette "Golden Hour", the fonts Fraunces and Source Sans 3, and illustrated avatars for 56 performers (`docs/design-kit.md`).
- **How we checked AI output:** we ran both scenarios step by step in a real browser, on two hosts, and counted headings, labels, overflow and touch targets on every page. We checked the data with a script (0 errors), calculated palette contrast instead of guessing, and wrote down the bugs the tests found (section 3).
- **Accepted:** the page structure, the four functions, the design kit. **Modified after testing:** the saved-session logic, the late-night time label, the phone filter layout. **Rejected:** colours and photos in the prototype (team rule).
- **AI limits we saw:** the AI first lost a saved session on the login page and mislabelled late-night sessions; both showed up only by running the scenarios. Sample bios and descriptions are fictional and formulaic.

## Next
Build the real site in `web/`: apply the Golden Hour look and generated images, add the planned functions.
