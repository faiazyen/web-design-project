# Documentation: Atardecer Bachata Festival website

CZU Web Design course project. Team: Faiaz Hossain Mazumder Yen, Oscar Muz, Sebastian Betancur. This file is the running write-up. It grows with each seminar and is finished for the final submission.

Live site: https://faiazyen.github.io/web-design-project/web/ . Source: https://github.com/faiazyen/web-design-project

## 1. Project development and changes
The binding specification is `project-specification.md` (Seminar 2). After Seminar 2 only about 15% may change, each change with a reason. This table is the record.

| # | Date | Change | Reason | Effect on the spec |
|---|---|---|---|---|
| 1 | 2026-10-19 | Programme items cut from 72 to 65 | closer to the course minimum of 60, less filler | data only |
| 2 | 2026-11-03 | Login page added (13 pages in total), header login status, function 8, Scenario 6 | teacher feedback on Seminar 2: My Programme uses localStorage but the structure has no login step | +1 page |
| 3 | 2026-11-03 | Practical info (travel, accommodation, accessibility, FAQ, code of conduct) kept as one page with five sections | five thin pages would repeat the same header and footer and say little each | none (it was already one page in the sitemap) |
| 4 | 2026-11-17 | Detail pages: one static HTML file per session (65), performer (64) and venue (3) instead of three templates filled from `?slug=` | a template that is filled by JavaScript shows search engines, AI tools and HTML validators an empty page. The course asks for SEO and AEO/GEO, so the content must be in the HTML | URLs change, sitemap, entities and scenarios do not |
| 5 | 2026-11-17 | `image` paths in `data.json` point to AI-generated vector images in `web/images/` (12 avatars, 3 venue scenes) | the images had no files yet. Vector art loads fast and needs no photo licences | data only |
| 6 | 2026-11-17 | Day/Night switch in the header, following the system setting | the Day/Night theme was a planned function and part of the Golden Hour design decision | the planned theme function is now built |
| 8 | 2026-11-17 | "Which level am I?" quiz (Programme page) and interactive venue map (Venues page) built as planned | functions 5 and 6 of the spec. They live on existing pages, so the sitemap does not change | none, both were planned |
| 7 | 2026-11-17 | Home page shows a short intro text and a four-number summary | the JSON-LD description must match visible text, and first-time visitors see the scale at once | none |

The sitemap still has 13 page types. Only the address form of three of them (the detail pages) changed, and the entities, functions 1–4 and scenarios are the same. We count this as one structural change plus small additions, which stays inside the 15% limit.

### Seminar 4 in short
The prototype (wireframe, grayscale) became the real site in colour. A script on our own computer (`scripts/build-site.py`) writes every page as plain HTML from `data.json`. The finished site needs no build and no server: it opens by double-click. JavaScript only improves the pages (filters, search, My Programme, login, Day/Night switch).

## 2. Cross-review
Each team member reviewed another part of the work. This table records the findings and the result.

| Reviewer | Reviewed | Finding | Result |
|---|---|---|---|
| Oscar Muz | Seminar 2: spec text and scenarios | no changes needed | accepted |
| Sebastian Betancur | Seminar 2: spec and data against the brief, name check | asked for the name change and for 65 items | both done |
| Teacher | Seminar 2 | My Programme needs a login step | simulated login added (change 2) |
| Teacher | Seminar 3 prototype | 7 points, no comments | accepted |
| Oscar Muz and Sebastian Betancur | Seminar 4: the live site on a phone and on a computer (2026-11-17): menu, Programme filters, "Which level am I?" quiz, venue map, Save then demo sign-up then My Programme, Day/Night button | everything worked, no problems reported | accepted, no changes |

The Seminar 4 cross-review was done by Oscar and Sebastian by hand on the live site. Not covered by anyone yet: Safari, Firefox and screen readers.

## 3. Work process
- **Roles:** Faiaz (A) leads and decides, Oscar (B) checks the text and scenarios, Sebastian (C) checks against the brief and uploads. The split for each seminar is in `project-specification.md`, section 8.
- **Tools:** Claude Code (AI) wrote and tested the code, the prototype and the drafts of the documents. The team decided scope, names, look and tradeoffs and checked the results.
- **Version control:** one public GitHub repository. Every change is committed and pushed, so the local folder and GitHub are identical. Hosting is GitHub Pages from the `main` branch.
- **Single source of truth:** `data.json`. Generated from it: `data.xml`, `web/js/data.js`, and the 142 pages.
- **Quality gate after each task:** validate the data, build the pages, run the offline site check, run the page audit at four widths, run both key scenarios, then write the log entry.

## 4. Use of AI
Every AI-assisted step is in `ai-log.md` with the prompt, what AI produced, how we checked it, and what we accepted, changed or rejected. Summary for Seminar 4:
- AI wrote the page generator, the CSS, the JavaScript, the 15 vector images and the check scripts.
- We verified the output with scripts (data, links, JSON-LD against visible text, contrast), a page audit of all 142 pages at four widths, Lighthouse, and both key scenarios in a real browser.
- Errors found in AI output are listed in `docs/evidence/web-verification.md` (11 problems, all fixed).
