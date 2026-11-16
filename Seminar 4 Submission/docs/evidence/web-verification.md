# Verification of the real site (web/), Seminar 4

Date: 2026-11-17. Everything below was run on our own computer against the built files in `web/`. The same checks are repeated on the live site after the push (see the end of this file).

## Scripts that make the checks repeatable
| Script | What it does |
|---|---|
| `python3 scripts/validate-data.py` | data checks (0 errors, 0 warnings) |
| `python3 scripts/build-site.py` | writes the 142 pages, `sitemap.xml`, `robots.txt`, `llms.txt` from `data.json` |
| `python3 scripts/check-site.py` | offline: links, assets, anchors, balanced tags, unique titles and descriptions, JSON-LD against visible text, sitemap, contrast |
| `scripts/audit-pages.js` | browser audit: loads every page at a given width and checks headings, labels, overflow, touch targets, alt text, metadata |
| `scripts/make-evidence-shots.sh` | screenshots of the real site from `file://` |

## Results
| Check | Result |
|---|---|
| Offline check (`check-site.py`) | **PASS, 0 problems.** 142 pages, 3,750 internal links and 809 asset references resolve, 277 JSON-LD blocks parse and their names, times, prices, addresses and FAQ text appear as visible text, 140 sitemap URLs exist, no external requests, every title and description is unique |
| Colour contrast (30 pairs, Day and Night) | lowest pair 4.81:1 (Day, link colour on the page background). Main text 13.6:1 (Day) and 15.9:1 (Night). Button text 5.1:1 and 6.8:1 |
| Page audit at 320, 375, 768 and 1280 px (142 pages each) | **0 problems** at every width: one h1, no skipped headings, every control has a label, no horizontal overflow, all touch targets at least 44 px, every image has `alt`, skip link, `lang`, canonical and Open Graph tags present, no text under 14 px |
| Lighthouse (throttled phone and desktop presets) | Home, Programme and a session page, on a local server and on the live site: Performance 100, Accessibility 100, Best practices 100, SEO 100 on all runs, largest paint 0.2 to 1.2 s, layout shift 0 to 0.004, blocking time 0 to 70 ms. Search, My Programme and Login after the fix in item 10 below: Accessibility, Best practices and SEO 100, Performance 98 to 100, layout shift 0 |
| Opened from `file://` in real Chrome (double-click case) | Programme filters, search and the Day/Night follow-the-system rule work with no server. A dark system setting gives `data-theme="night"` |
| Keyboard | the first Tab stops on "Skip to main content" with a visible 3 px focus ring |

## Scenarios run in the real design
- **Scenario 1 (phone, 375 px), passed:** Programme filtered to Saturday, workshops, beginner, follow. Save while logged out went to the sign-up page with the reason shown. After a demo sign-up the page returned to the same filtered list and the pending session was saved. A second workshop was saved. My Programme showed both with "No clashes". Saving a session at the same time as the first showed the clash warning on both cards, and Remove cleared it.
- **Scenario 2 (desktop, 1280 px), passed:** Friday, Marea Club, social, night filters showed 4 sets. The 22:00 session opened and its DJ link led to the DJ page with both sets.
- **Scenario 3 (search):** "marisol" returned 1 performer and 3 sessions with the name highlighted.

## Problems found by these checks, and fixed
1. Navigation, breadcrumb and footer links were 35 to 38 px wide, under the 44 px target (found by the audit on all 142 pages). Fixed with a minimum width.
2. Two sessions had the same title on different days, so two page titles were identical (found by `check-site.py`). Fixed by adding the day to the page title.
3. The tickets page JSON-LD listed venues that are not shown on that page, so it did not match the visible content. The venues were removed from that block.
4. The "(4 active)" filter label had no space after "Filters".
5. The phone header (search, login, theme and a menu) filled a third of the screen. Search, login and the theme button now fold behind the Menu button.
6. The phone hero was almost fully covered by its text card, so the sunset art was hidden. The art now has its own space above the card.
7. The Night hero was too dark and the card blended into the sky. A dusk gradient and a card border were added.
8. On a phone, tables with 4 columns were too tight. They now turn into stacked cards, and the table caption was squeezed into one word per line (fixed with `display: block`).
9. The headless Chrome screenshots of the phone layout were cropped at 500 px (its minimum window width), so the phone screenshots were taken in the browser pane instead.
10. Lighthouse on the live site found a layout shift of 0.567 on the Search page (performance 78 on a phone): the results are drawn by JavaScript and pushed the footer down. The footer now stays hidden until the results are in place, and the results area has a reserved height. After the fix the layout shift is 0 on Search and My Programme (performance 100 and 98).

## Not verified
Safari, Firefox, screen readers (NVDA, VoiceOver) and real users. The W3C online HTML checker was not run on the 142 pages in this round (it rate-limits repeated use); the offline check covers balanced tags, duplicate ids and links. Lighthouse numbers come from a local server and will differ a little on GitHub Pages.

## Live site check (https://faiazyen.github.io/web-design-project/web/), after the final push
- **Files:** all 177 files in `web/` were downloaded from the live site and compared by checksum with the local files: 0 differ.
- **Page audit** of all 142 live pages at 320 px: 0 problems (run before the last small fix). The audit was not repeated on the live site at the other widths.
- **Lighthouse on the live site:** Home, Programme and a session page: 100 in all four categories on phone and desktop. Search and My Programme after the fix: Accessibility, Best practices and SEO 100, Performance 99 to 100, layout shift 0 to 0.003.
- **Scenario 1 on the live site (phone size), passed:** Save while logged out, demo sign-up, return to the same filtered list with the session saved, second workshop saved, My Programme shows both with "No clashes". Scenario 2 was run locally only.
