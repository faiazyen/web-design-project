# Progress 03: Seminar 4 (first functional implementation)

**Festival:** Atardecer Bachata Festival, Valencia, 25–27 June 2027. **Team:** Faiaz Hossain Mazumder Yen, Oscar Muz, Sebastian Betancur. **Date:** 2026-11-17.

**Live (any computer, no installation):** https://faiazyen.github.io/web-design-project/web/ . **Offline:** open `web/index.html` by double-click. The earlier wireframe stays at `/prototype/`.

## 1. What has been implemented
- **142 real pages** in plain HTML, CSS and JavaScript (no framework, no build step to run, no server needed): Home, Programme, Performers, Venues, Roots, Practical info, Tickets, My Programme, Log in / Sign up, Search results, plus one page for each of the 65 sessions, 64 performers and 3 venues.
- **Home page and pages with very different content:** Home (hero, mood switch, numbers, opening night, venues, featured artists), Programme (65 sessions with filters), Tickets (price table), Practical info (travel, accommodation table, accessibility, FAQ, code of conduct), Roots (timeline and instruments), session, performer and venue pages.
- **Main navigation:** Programme, Performers, Venues, Roots, Practical info, My Programme and a Tickets button in the header of every page, the current page marked, breadcrumbs, a skip link, a footer with the same key links. On a phone the header folds behind one Menu button. No link leads to a missing page (3,750 internal links checked by script).
- **Responsive, mobile first:** the base CSS is for 320 px and up, with larger layouts from 600 px and 900 px. Tables turn into stacked cards on a phone. No horizontal scrolling at 320 px.
- **Functional interactive features** (JavaScript only improves pages that already work as HTML):
  1. Programme filters: day, venue, type, level, role focus, day or night. Filters live in the URL, so a filtered list can be shared. A count is announced, an empty state is shown.
  2. Search over sessions, performers and venues (accent and case insensitive, matches highlighted), plus a name and type filter on Performers.
  3. My Programme: save and remove sessions, clash warning, calendar download (.ics).
  4. Simulated sign-up and login (accounts and saved sessions in the browser, no password stored). Saving while logged out sends the visitor to log in and then saves the session after returning.
  5. Day/Night theme switch that also follows the system setting.
  6. FAQ as native expandable sections (works without JavaScript).
- **Semantic HTML:** `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, `time`, `address`, `details`, lists, tables only for prices and accommodation, every control has a `label`, one h1 per page, no skipped heading levels.
- **Visual design:** the Golden Hour palette (Day and Night), Fraunces and Source Sans 3 bundled in the site (no external requests), 12 illustrated avatars, 3 venue scenes, a sunset hero drawn in SVG that changes with the theme. All images are AI-generated vector drawings, recorded in `docs/image-prompts.md`.
- **For search engines and AI tools:** every page has its own title, description, canonical address and Open Graph tags; JSON-LD (Festival, Event, Place, Person or PerformingGroup, BreadcrumbList, FAQPage, offers) that matches visible text; `sitemap.xml`, `robots.txt`, `llms.txt`.

## 2. Current best practices and trends in UX and design, and how we used them
| Practice or trend | Where it comes from | How we implemented it |
|---|---|---|
| Content in HTML first, JavaScript as an improvement (progressive enhancement) | web standards practice, and needed by search and AI crawlers that do not run scripts | all 142 pages are complete HTML. Filters hide and show cards that are already there. Without JavaScript the full list is still readable |
| Structured data and answer-first content for search and AI answers (SEO, AEO, GEO) | schema.org, search engine guidance | JSON-LD on each page, checked by script against the visible text. FAQ with real questions and short answers. `llms.txt` with the key facts |
| Speed and Core Web Vitals | Google's page experience metrics | no framework, one 17 KB stylesheet, one small script per page, vector images, fonts bundled and swapped in. Lighthouse performance 100, largest paint 0.2 to 1.2 s, layout shift near 0 (local test) |
| Mobile first and thumb-friendly targets | usage patterns, WCAG 2.2 target size guidance | base CSS for 320 px, 44 px minimum targets (checked on all pages), the menu folds on a phone |
| Accessibility as a base layer | WCAG 2.0 AA (our minimum) | contrast of 4.8:1 or higher on 30 colour pairs, visible 3 px focus ring, skip link, labelled forms with announced errors, `aria-live` for filter counts and the toast, `prefers-reduced-motion` |
| Dark mode that follows the system | `prefers-color-scheme` | the page starts in the user's system mode and a button changes it. The choice is remembered. It is also our concept: Sea by day, club by night |
| Clear hierarchy and plain language | usability practice | one h1, what and when first, two big choices (day, night), short paragraphs, text lines of about 70 characters |
| Empty, error and success states | interaction design practice | "no sessions match", "log in to see your programme", "no clashes", toast messages, inline form errors |
| Design tokens and a spacing scale | design system practice | all colours, sizes and spacing are CSS variables on a 4 px grid. Day and Night only swap the colour variables |
| Illustrated avatars and vector scenes instead of stock photos | current brand illustration trend, and licensing safety | 15 SVG images drawn in the palette, no real people, no licence issues |

## 3. What changed compared with the prototype, and why
| Prototype (Seminar 3) | Real site (Seminar 4) | Why |
|---|---|---|
| Grayscale wireframe, placeholder boxes | Golden Hour colours, real fonts, illustrations | the prototype was mid-fidelity on purpose; the build is the final look |
| Pages built in the browser by JavaScript from `data.js` | Pages written as HTML by `scripts/build-site.py` | search engines, AI tools and HTML validators must see the content without running scripts |
| 3 template pages with `?slug=` for sessions, performers and venues | 132 pages, one per entity | same reason; also unique titles, descriptions and JSON-LD for each |
| Roots, Practical info and Tickets were placeholders | three real pages with content from `data.json` | they were outside the two key scenarios, now part of the site |
| Header with search and login status | same, plus Day/Night button, and everything but the brand folds behind Menu on a phone | the first header took a third of a phone screen |
| Image fields in `data.json` pointed to nothing | they point to the generated vector images | the images exist now |
| No theme switch | Day/Night switch that follows the system | a function planned in the spec (Day/Night theme) |
| Tables | stacked cards on a phone | four columns do not fit 320 px |
All changes are in the table in `documentation.md` and in `project-specification.md` (section 8). The sitemap, the entities, the functions 1–4 and the scenarios did not change.

## 4. Tests and checks (details and screenshots: `docs/evidence/web-verification.md`)
- **Both key scenarios in the real design, passed.** Scenario 1 on a 375 px phone: filter Saturday beginner follower workshops, Save while logged out, sign up, return, save a second workshop, My Programme shows both with no clashes (a deliberate clash was warned about on both cards, and Remove cleared it). Scenario 2 on 1280 px desktop: Friday night socials at the club, the 22:00 session, its DJ page with both sets. Search for "marisol" found the performer and 3 sessions.
- **Page audit of all 142 pages at 320, 375, 768 and 1280 px: 0 problems** (one h1, no skipped headings, labelled controls, no overflow, targets of at least 44 px, alt text, metadata).
- **Offline site check: 0 problems:** 3,750 links and 809 assets resolve, balanced tags, unique titles and descriptions, 277 JSON-LD blocks match the visible text, sitemap files exist, no external requests.
- **Contrast:** 30 pairs, Day and Night, lowest 4.81:1.
- **Lighthouse (phone and desktop presets), local and on the live site:** Home, Programme and a session page: Performance, Accessibility, Best practices and SEO all 100. Search, My Programme and Login: Accessibility, Best practices and SEO 100, Performance 98 to 100 (the live run found a layout shift on Search, fixed, now 0).
- **Double-click test:** pages open from `file://` in Chrome and filters and search work.
- **Problems found and fixed (10):** footer and breadcrumb links under 44 px wide; two session pages with the same title; tickets JSON-LD that listed venues not shown on the page; a missing space in the filter label; a phone header that took a third of the screen; a phone hero whose art was hidden; a Night hero that was too dark; tables too tight on a phone; cropped phone screenshots; a layout shift of 0.567 on the Search page, found by Lighthouse on the live site and now 0.
- **Not verified:** Safari, Firefox, screen readers, real users, and the W3C online validator on all pages.

## 5. Use of AI, and how we checked it
- **AI (Claude Code) did:** planned the build, wrote the page generator, the CSS, the JavaScript, the 15 vector images, the check scripts, and drafted this file and the slides.
- **We decided:** build all pages from the data by script, draw the images as vectors now, bundle the two fonts, keep the prototype available, and what to show in the presentation.
- **How we checked:** we did not accept the code because it looked right. We ran scripts over all 142 pages, ran both key scenarios in a real browser on phone and desktop sizes, read screenshots, and measured contrast, targets, headings and links.
- **Accepted:** the generator approach, the layout, the JavaScript features. **Modified after testing:** the 10 items above. **Rejected:** a loading video in the hero (speed and no marks), stock photos, and framework code from design tools.
- **AI limits seen:** the first headers, heroes and tables looked fine on desktop and failed on a phone; the audit and screenshots found it. It also first listed venues in a JSON-LD block where they were not visible on the page. Sample bios are still fictional and formulaic.
- Every step is in `ai-log.md`.

## Not built yet, and next
Two planned functions from the spec are not built yet: the level quiz and the venue map. The Programme filters already cover choosing by level, and the venue pages carry the address and access facts, so Scenarios 1 and 2 do not depend on them. Next: cross-review of the build by Oscar and Sebastian, native Safari and Firefox tests, screen reader check, the final polish and the remaining documentation.
