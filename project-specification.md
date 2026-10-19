# Project Specification — Raíces del Mar Bachata Festival

**Status:** DRAFT, binding after Seminar 2 (about 15% may change, each with a justification).
**Last updated:** 2026-10-19

## 1. Festival identity

| Field | Decision |
|---|---|
| **Name** | Raíces del Mar — Valencia Bachata Roots Festival |
| **Edition / year** | 5th edition, 2027 |
| **Location** | Valencia, Spain. Beachfront venue on the Mediterranean, with a dance floor on the sand. |
| **Date range** | 24–27 June 2027 (Thursday to Sunday, 4 days) |
| **Type** | Open-air summer festival. Social, welcoming, all levels. |
| **Character** | Warm, sunlit and community-driven. It joins the relaxed seaside atmosphere to a serious respect for where bachata comes from. |
| **Main genres** | Bachata dominicana (traditional), bachata sensual, bachata moderna. Small kizomba and salsa social rooms. |
| **Main themes** | **The sea** (Mediterranean setting, sunset social dancing on the sand) and **roots and heritage** (origins of bachata, live guitar and bands, learning through workshops). |

## 2. Audience and goals

### Audiences

| Audience | Who | What they need from the site |
|---|---|---|
| **Travelling dancers** | Social dancers from across Europe, intermediate and up, who book flights and rooms. | Dates, ticket prices, travel and accommodation, the line-up, a clear schedule. |
| **Local dancers** | Dancers from Valencia and Spain. | Day passes, party times, how to get there, workshop levels. |
| **Beginners and the heritage-curious** | People new to bachata or interested in its Dominican origins. | A plain-language story of bachata, beginner workshops, reassurance that all levels are welcome. |

### Goals

1. **Convert:** a visitor can find ticket options and prices within two clicks from any page.
2. **Inform:** every artist, workshop and programme slot is reachable by browsing or by search.
3. **Express identity:** the sea and the roots of bachata are visible on the home page without scrolling.
4. **Be usable by everyone:** keyboard operable, WCAG AA, readable on a phone.

### Success checks (testable)

- Any page is reachable in 3 clicks or fewer from the home page.
- Searching "guitar", "beginner" or an artist name returns results.
- All pages pass HTML validation and the AA contrast checks.
- The site works when `web/index.html` is opened directly from the file system.

## 3. Sitemap

All files live in `web/`. Detail pages are one shared template filled from the URL query (`?id=`) using `web/js/data.js`, so no build step is needed.

```
Home                          index.html
├── The Festival              festival.html        story, sea, roots of bachata
├── Programme                 programme.html       day-by-day schedule, filter by day and type
├── Artists                   artists.html         list with filter
│   └── Artist detail         artist.html?id=
├── Workshops                 workshops.html       list with filter by level and style
│   └── Workshop detail       workshop.html?id=
├── Tickets                   tickets.html         passes, prices, what is included
├── Venue & Travel            venue.html           map, getting there, where to stay
├── FAQ                       faq.html
├── Contact                   contact.html
├── Search results            search.html?q=
└── Accessibility statement   accessibility.html
```

12 page files in total. Artist, workshop and search pages render many results from one file each.

> **Assumption to confirm:** the final brief's list of required sections was not available when this was drafted. If it names a section missing above, it is added here before the spec is locked.

### Global elements (on every page)

- **Header:** logo and name, main navigation, search field.
- **Skip link** to the main content, first in tab order.
- **Breadcrumbs** on every page except Home.
- **Footer:** dates and location, links to Contact, FAQ and Accessibility.

## 4. Navigation and breadcrumbs

**Main navigation (6 items):** The Festival, Programme, Artists, Workshops, Tickets, Venue & Travel. FAQ and Contact sit in the footer and in a secondary link row. Tickets is styled as a call-to-action.

**Breadcrumb pattern:** `Home > Section > Detail`, as an ordered list inside `<nav aria-label="Breadcrumb">`. The current page is plain text with `aria-current="page"`.

| Page | Breadcrumb |
|---|---|
| Home | none |
| Section pages (Festival, Programme, Artists, Workshops, Tickets, Venue, FAQ, Contact, Accessibility) | Home > Section |
| Artist detail | Home > Artists > *Artist name* |
| Workshop detail | Home > Workshops > *Workshop title* |
| Search results | Home > Search results for "*query*" |

Detail-page names come from `data.js` using the `id` in the URL. An unknown `id` shows a clear "not found" message with links back to the list.

## 5. Search

- A search form in the header of every page submits by GET to `search.html?q=...`.
- `search.html` reads `q`, searches `data.js` in the browser, and lists results grouped by type (Artists, Workshops, Programme, FAQ, Pages).
- Each result shows a title, a short excerpt and a link. Matching text is highlighted with `<mark>`.
- Matching is case- and accent-insensitive, so "raices" finds "Raíces".
- Empty query and no-result states show helpful text and suggestions, not a blank page.
- No server, no `fetch()`, no framework.

## 6. Open sections (to write next)

6. Page templates and content types
7. Visual direction and content tone
8. Accessibility and validity targets in detail
9. Data model (`data.json` shape)
10. Folder structure and build-free workflow
11. Reference patterns (21st.dev, Stitch), used as ideas only
