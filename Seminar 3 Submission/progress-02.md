# Progress 02: Seminar 3 (prototype)

**Festival:** Atardecer Bachata Festival, Valencia, 25–27 June 2027. **Team:** Faiaz Hossain Mazumder Yen, Oscar Muz, Sebastian Betancur. **Date:** 2026-11-03.

## Prototype
- **Live (any computer, no installation):** https://faiazyen.github.io/web-design-project/prototype/ . Offline: open `prototype/index.html`. The footer link "Prototype guide" walks through both key scenarios and resets the demo.
- **What it is:** a mid-fidelity, grayscale wireframe in plain HTML, CSS and JavaScript, built from the project specification, with sample content from `data.json`. Mobile first (320 px and up), with a desktop layout from 900 px.
- **Screens:** Home, Programme, Session, Performers, Performer, Venues, Search, My Programme, Log in / Sign up. Roots, Practical info and Tickets open a placeholder (outside the two key scenarios).
- **Navigation and hierarchy:** main menu with a Tickets button, search and login status in every header, breadcrumbs, skip link. Home shows what and when first, then the key actions, the two moods (day, night), people, and the personal programme.
- **Visual design:** the planned Day and Night look (palette "Golden Hour") is on a separate page, "Visual design direction", so the wireframe stays grayscale.

## 1. Proposed functions
| # | Function | In the prototype |
|---|---|---|
| 1 | Programme filters: day, venue, type, level, role focus, day or night | Yes |
| 2 | Search (header, results grouped) and a name filter on Performers | Yes |
| 3 | My Programme: save and remove, clash warning, calendar download | Yes |
| 4 | Simulated sign-up and login (teacher feedback from Seminar 2) | Yes |
| 5–8 | Day/Night theme, level quiz, venue map, FAQ accordion | Planned for the build |

## 2. Functions and user needs
| Function | User need | Group, scenario |
|---|---|---|
| 1 Filters | Beginners find workshops at their level. Night dancers find tonight's socials. | 1 and 2, Scenarios 1 and 2 |
| 2 Search | A returning visitor finds one artist and all their sessions. | 3, Scenario 3 |
| 3 My Programme | A personal schedule without clashes, to take away. | 1 and 2, Scenario 1 |
| 4 Simulated login | The personal programme belongs to a person and is kept. | 1, Scenarios 1 and 6 |

## 3. What we verified, and how
Details and screenshots: `docs/evidence/prototype-verification.md`.
- **Scenario 1 (phone):** filter Saturday beginner follower workshops, Save while logged out, sign up, save a second workshop, My Programme shows both with "No clashes". **Passed** locally and on the live site.
- **Scenario 2 (desktop):** filter Friday night socials at the club, open the 22:00 session, follow the DJ link to the set times. **Passed** locally and on the live site.
- **Double-click:** the main pages open from `file://` in real Chrome, with storage working.
- **Automated page check (all 12 pages at 320 px, key pages at 1280 px):** one h1, no skipped headings, labelled inputs, no overflow, touch targets of at least 44 px, no text under 12 px, text lines of 70 to 80 characters at most, no external requests. The CSS uses one 4 px spacing grid, one radius scale and 7 font sizes. Contrast was calculated: every text pair is at least 7.4:1.
- **Problems found and fixed (12):** a pending Save lost on the login page; a skipped heading level; a missing space in the filter title; a confusing "Fri 00:00" label for late sets; filters filling a whole phone screen; text lines too long; too many font sizes; off-grid spacing; inconsistent corner radius; hard-coded colours; sign-up errors not announced to screen readers; decorative symbols read out twice.
- **Not verified:** Safari, Firefox, screen readers, real users.

## 4. Use of AI, and how we checked it
- **AI (Claude Code) did:** planned the screens, wrote the prototype code, the design kit and the visual design page, ran the tests, drafted this file and the slides.
- **We decided:** grayscale mid-fidelity for the prototype, Scenarios 1 and 2 as key scenarios, the simulated login, and the Golden Hour look, fonts and avatars for the build.
- **How we checked:** we ran both scenarios in a real browser on two hosts, measured headings, labels, overflow, text size, contrast and spacing on every page, checked the data with a script (0 errors), and wrote down every bug found.
- **Accepted:** page structure, the four functions. **Modified after testing:** the 12 items above. **Rejected:** colours and photos in the wireframe pages.
- **AI limits seen:** it first lost a saved session on the login page and left inconsistent sizes and spacing; only running the scenarios and measuring the CSS showed this. Sample bios are fictional and formulaic.

## Next
Build the real site in `web/`: plain HTML for all content (so search engines and AI tools can read it), the Golden Hour look, and the planned functions. Hero: two AI-generated stills (Day and Night) with real text on top. A short loop video is optional and last, with a poster image and a pause button, only if speed checks stay good.
