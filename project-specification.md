# Project Specification — Atardecer Bachata Festival

CZU Web Design course, Seminar 2 submission. Fictional festival.
**Team:** Faiaz Hossain Mazumder Yen (A), Oscar Muz (B), Sebastian Betancur (C).
**Status:** DRAFT for Seminar 2. After Seminar 2 only about 15% may change, each change with a written justification.

## 1. Festival Identity

| Field | Decision |
|---|---|
| **Name** | Atardecer Bachata Festival |
| **Edition / year** | 1st edition ("Primera Ola"), 2027 |
| **Location** | Valencia, Spain. Open-air stage on the beachfront, a seaside pavilion for workshops, and an indoor club for night socials. |
| **Date range** | Friday 25 June – Sunday 27 June 2027 (3 days) |
| **Type / character** | Social-first, beginner-friendly Latin bachata festival. **Sea by day, club by night:** outdoor dancing on the sand in the daytime, indoor socials with DJs after dark. Workshops by level, evening shows, late socials. |
| **Main genres / themes** | **Genres:** bachata dominicana (traditional), bachata sensual, bachata moderna, plus salsa socials. **Themes:** the sea, the Dominican roots of bachata, dancers from many countries meeting in one city. |

**The name:** *Atardecer* is Spanish for sunset. The sunset social on the sand is the festival's signature moment each day.

**Why this concept (team reason, from Faiaz):** We want a Latin bachata festival where people from different parts of the world come to dance. Valencia is a clean, modern Spanish city with good access to the sea, so we can dance outdoors by the water and indoors at night. There are bars, artists, shows and DJs playing bachata, Latin American music and salsa.

**Unique angle (drives website features):** the festival has two moods, *Sea* (day, outdoor, relaxed) and *Club* (night, indoor, intense). The website shows this as a Day/Night theme, a Day/Night filter in the programme, and a dedicated **Roots** page on the story of bachata dominicana.

## 2. Purpose of the Website

**What it is for.** The website helps dancers decide to come, plan their three days, and find practical information. It is the only official source for the programme, the artists, the venues and the tickets.

**Main objectives**
1. Show clearly what Atardecer is: dates, city, mood, who it is for.
2. Let visitors build a personal schedule (workshops, socials, shows) without time clashes.
3. Make every artist, venue and session findable by browsing, filtering or search.
4. Give beginners the confidence to come (levels, role focus, what to expect, code of conduct).
5. Provide practical information: tickets, travel, accommodation, accessibility, FAQ.
6. Express the identity: sea by day, club by night, and the roots of bachata dominicana.

**Key user actions**
- Filter the programme by day, venue, type and level.
- Open a session, an artist or a venue.
- Save sessions to My Programme and see clashes.
- Search for an artist, a session or a venue by name.
- Find ticket prices and how to buy.
- Check accessibility and the code of conduct before booking.

## 3. Target Groups

| Group | Needs | Expectations | Information and functions needed |
|---|---|---|---|
| **1. First-time and beginner dancers** (many are followers who come with friends) | Know which workshops suit their level. Feel welcome and safe. | Clear level labels, a place to start, no jargon. Beginner workshops during the day, not at night. | Level guide and "Which level am I?" quiz. Programme filter by level and role focus (lead, follow, both). My Programme. Code of conduct. |
| **2. Experienced social dancers from abroad** | Plan nights: who plays where, when the social ends. Book travel and a room. | A fast overview of DJs, live acts and set times. Travel and accommodation facts they can trust. | Programme filter by day, venue and Night. DJ and band pages with set times. Venue pages. Travel and accommodation pages. Tickets. |
| **3. Returning visitors and fans of specific artists** | Find a particular instructor, DJ or show team and see everything they do at the festival. | Search that understands names. A page per artist that lists all their sessions. | Search with results page. Performer detail with their sessions. Link to save each session. |
| **4. Visitors with access needs, and people in groups** | Check step-free access, toilets, quiet areas and the conduct policy. Plan for a group. | Honest, specific accessibility facts per venue. Contact for questions. | Accessibility page. Access details on each venue page. Code of conduct. FAQ. Group information on Tickets. |

## 4. Information Architecture

### Sitemap (nested list)

All pages are static HTML files in `web/`. Detail pages are one template each, filled from the URL query `?slug=` using `web/js/data.js`.

- **Home** (`index.html`) — first impression, dates, Sea/Night mood, next steps.
  - **Programme** (`programme.html`) — all sessions with filters by day, venue, type, level, role focus and Day/Night.
    - **Programme item detail** (`programme-item.html?slug=`) — one session: time, venue, level, role focus, performers, save button.
  - **Performers** (`performers.html`) — all artists with filter by type (instructor, DJ, band, show team).
    - **Performer detail** (`performer.html?slug=`) — one artist: bio and all their sessions.
  - **Venues** (`venues.html`) — the three venues with an interactive map.
    - **Venue detail** (`venue.html?slug=`) — address, access details, sessions held there.
  - **Roots** (`roots.html`) — story of bachata dominicana: origins, instruments, timeline.
  - **Practical info** (`practical.html`) — hub linking to the six pages below.
    - **Tickets** (`tickets.html`) — passes, prices, what is included, group information.
    - **Travel** (`travel.html`) — how to reach Valencia and the venues, local transport, sustainability note.
    - **Accommodation** (`accommodation.html`) — recommended places to stay with distance and price.
    - **Accessibility** (`accessibility.html`) — access facts per venue and the site's accessibility statement.
    - **FAQ** (`faq.html`) — short, direct answers to common questions.
    - **Code of conduct** (`code-of-conduct.html`) — rules for a safe, respectful dance floor and how to report.
  - **My Programme** (`my-programme.html`) — the visitor's personal schedule with clash warnings.
  - **Search results** (`search.html?q=`) — results for a query, grouped by type.

17 page files in total. Search field and the main navigation appear on every page.

### Main navigation

**Programme, Performers, Venues, Roots, Practical info, My Programme.** A search field sits in the header of every page. **Tickets** is a highlighted button linking to `tickets.html`. The footer repeats the Practical info pages, the festival dates and location, and a contact email.

### Breadcrumbs

Every page except Home shows breadcrumbs as an ordered list inside `<nav aria-label="Breadcrumb">`. The current page is plain text with `aria-current="page"`.

| Page | Breadcrumb |
|---|---|
| Programme, Performers, Venues, Roots, Practical info, My Programme | Home > Page |
| Programme item detail | Home > Programme > *Session title* |
| Performer detail | Home > Performers > *Artist name* |
| Venue detail | Home > Venues > *Venue name* |
| Tickets, Travel, Accommodation, Accessibility, FAQ, Code of conduct | Home > Practical info > Page |
| Search results | Home > Search results for "*query*" |

### Relationships between sections

- Programme item ⇄ Performer: a session lists its performers, and a performer page lists all their sessions.
- Programme item ⇄ Venue: a session names its venue, and a venue page lists all sessions held there.
- Programme item → My Programme: every session has a Save button.
- Search covers sessions, performers, venues, Roots and FAQ.
- Accessibility facts appear on each venue page and are summarised on the Accessibility page.
- Home links to Programme, Tickets and Roots.

## 5. Interactive Functions (planned)

All work in the browser from `file://`, with data from `web/js/data.js`.

| # | Function | Target group need it serves |
|---|---|---|
| 1 | **Programme filters:** day, venue, type (workshop, show, social), level, role focus, Day/Night. Shows a result count and a clear-all button. | Beginners need to find workshops at their level and role. Experienced dancers need to find tonight's socials. |
| 2 | **Search** with a field on every page and a results page, grouped by Sessions, Performers, Venues, Roots, FAQ. Accent- and case-insensitive. | Returning visitors need to find an artist by name and see all their sessions. |
| 3 | **My Programme:** save and remove sessions, clash warning when two saved sessions overlap, saved in the browser's `localStorage`, download as a calendar file (`.ics`). | Beginners and travelling dancers need a schedule with no clashes they can take with them. |
| 4 | **Day/Night theme:** a toggle (and the system setting) switches the whole site between a light "Sea" look and a dark "Club" look. | Experienced night dancers and everyone with light or glare sensitivity. Supports the festival's two-mood identity. |
| 5 | **"Which level am I?" quiz:** five questions, result links to the beginner, intermediate or advanced workshops. | First-timers need confidence about their level. |
| 6 | **Interactive venue map:** an SVG map of the three venues. Selecting a zone shows the venue's name, access facts and today's sessions. | Visitors with access needs and visitors planning their route between venues. |
| 7 | **FAQ accordion** using native `<details>`. | Visitors in all groups need fast answers. |

## 6. User Scenarios

Scenarios 1, 2 and 3 are the **KEY** scenarios.

### Scenario 1 — KEY: First-timer, beginner follower
- **User type:** Group 1, first-time dancer who usually dances the follow role.
- **Goal:** Pick two Saturday beginner workshops and have a personal schedule with no clashes.
- **Initial situation:** She lands on the Home page from a friend's message and has never been to a bachata festival.
- **Expected outcome:** She opens Programme, filters Day = Saturday, Type = Workshop, Level = Beginner, Role = Follow or Both, saves two sessions, and My Programme lists both with no clash warning.
- **Data needed:** `programmeItems` with `dayId`, `type`, `level`, `roleFocus`, `start`, `end`.

### Scenario 2 — KEY: Experienced social dancer, evening
- **User type:** Group 2, experienced dancer who travelled from abroad.
- **Goal:** Find out which DJ plays the main social tonight and when it ends.
- **Initial situation:** It is Friday afternoon. He is on Programme.
- **Expected outcome:** He filters Day = Friday, Type = Social, Day/Night = Night, opens the main club social, sees the DJ's name and the end time, then opens the DJ's performer page and sees the set time.
- **Data needed:** `programmeItems.performerIds`, `venueId`, `end`; `performers.type = "dj"`.

### Scenario 3 — KEY: Returning visitor searching by name
- **User type:** Group 3, returning visitor who follows a particular instructor.
- **Goal:** See all workshops taught by that instructor.
- **Initial situation:** She is on any page and remembers only the instructor's name.
- **Expected outcome:** She types the name into the header search, lands on Search results, opens the instructor's page, and sees every session of that instructor, each with a Save button.
- **Data needed:** `performers.name` and `slug`; every `programmeItems.performerIds` entry resolves to a performer.

### Scenario 4: Visitor checking access before booking
- **User type:** Group 4, visitor with reduced mobility travelling with a friend.
- **Goal:** Confirm that all venues are step-free and read the conduct policy before buying a pass.
- **Initial situation:** He is on Practical info and has not decided to attend.
- **Expected outcome:** He opens Accessibility, sees step-free and toilet facts for each venue, opens a venue page for details, reads the Code of conduct, and finds the contact address in the FAQ.
- **Data needed:** `venues.accessibility`; `festival.codeOfConduct`; `festival.faq`.

### Scenario 5: Group of friends planning the trip
- **User type:** Group 2, four friends flying in from different countries.
- **Goal:** Compare pass prices, find a place to stay near the venues, and work out how to get from the airport.
- **Initial situation:** They know the dates and have not yet booked.
- **Expected outcome:** On Tickets they compare passes, on Accommodation they pick a place by distance and price, and on Travel they find airport-to-city options.
- **Data needed:** `festival.tickets`, `festival.accommodation`, `festival.travel`.

## 7. Data Model

`data.json` is the single source of truth. `data.xml` is generated from it by `scripts/json-to-xml.py` for the Seminar 2 submission, because the assignment accepts XML or JSON and the submission list names both. `scripts/json-to-xml.py` also checks that both files hold the same ids, counts and relations. Entity fields below. The full schema with one example record per entity is in `docs/data-schema.md`.

Top-level keys: `festival`, `days`, `categories`, `venues`, `performers`, `programmeItems`.

**Common rules:** ids are stable strings (`ven-001`, `perf-014`, `item-037`). Every detail page has a unique `slug`. All dates and times are ISO 8601 with offset, timezone `Europe/Madrid` (UTC+02:00 in June 2027). Images carry `alt`, `credit` and `source`. All people, venues and organisations are fictional.

### festival
`id`, `slug`, `name`, `edition`, `editionLabel`, `year`, `startDate`, `endDate`, `timezone`, `city`, `country`, `countryCode`, `tagline`, `description`, `themes[]`, `genres[]`, `language`, `currency`, `contact{email}`, `tickets[]`, `accommodation[]`, `travel[]`, `faq[]`, `codeOfConduct{}`, `accessibility{}`, `sustainability{}`, `roots{}`.

### days
`id` (`day-fri`, `day-sat`, `day-sun`), `date`, `label`, `theme`.

### categories
Lookup lists used by filters and the quiz: `types[]` (workshop, show, social), `levels[]` (beginner, intermediate, advanced, all-levels, each with a description), `roleFocus[]` (lead, follow, both), `styles[]` (dominicana, sensual, moderna, salsa), `performerTypes[]` (instructor, dj, band, singer, show-team), `dayParts[]` (day, night).

### venues (3 records)
`id`, `slug`, `name`, `kind` (beach-stage, pavilion, club), `setting` (outdoor, indoor), `description`, `address{streetAddress, postalCode, addressLocality, addressRegion, addressCountry}`, `geo{latitude, longitude}`, `capacity`, `accessibility{stepFree, accessibleToilets, quietSpace, notes}`, `mapZone`, `image{src, alt, credit, source}`.

### performers (64 records)
`id`, `slug`, `name`, `type` (instructor, dj, band, singer, show-team), `members[]` (for couples and teams), `country`, `styles[]`, `bio`, `featured`, `image{src, alt, credit, source}`.

### programmeItems (65 records)
`id`, `slug`, `title`, `type`, `level`, `roleFocus`, `style`, `dayId`, `start`, `end`, `dayPart` (night when it starts at 20:00 or later, or before 06:00, otherwise day), `venueId`, `performerIds[]`, `description`, `capacity`, `tags[]`.

A **programme day runs from 06:00 to 06:00**. A set that starts at 01:30 on Saturday morning belongs to Friday night, so its `dayId` is `day-fri`.

### Relations
- `programmeItems.venueId` → `venues.id` (many to one).
- `programmeItems.performerIds[]` → `performers.id` (many to many).
- `programmeItems.dayId` → `days.id`.
- A performer's sessions are **derived** from `programmeItems`, never stored on the performer.
- Rules checked by `scripts/validate-data.py`: every performer appears in at least one item; no venue has overlapping items; no performer is in two places at once; all referenced ids exist; no duplicate ids or slugs; every item belongs to a programme day of 25–27 June 2027 (06:00 to 06:00) and ends by 06:00 the next morning at the latest; `dayId` and `dayPart` match `start`; workshops start between 09:00 and 21:00, and beginner workshops start before 19:00.

## 8. Use of AI and Verification

### AI tool
Claude Code (Sonnet 5.5) was used for the specification draft, the data schema, the data, the validation and conversion scripts, and the presentation.

### Team roles and task split

| Role | Person | Tasks | Status |
|---|---|---|---|
| **A** | Faiaz Hossain Mazumder Yen | Claude Code work: repo, `CLAUDE.md`, skills, concept options and name check, schema, `data.json`, `validate-data.py`, `build-data.py`, `ai-log.md`, commits | Done: repo, rules, skills, name check, spec draft, data schema, `data.json` (64 performers, 65 items), `data.xml`, `validate-data.py`, `build-data.py`, `json-to-xml.py`, the 5-slide presentation file, log entries. |
| **B** | Oscar Muz | Spec text and scenarios: review and edit sections 1–6 | Not yet done |
| **C** | Sebastian Betancur | Critique of the spec and data against the brief, name check, Moodle upload | 🟢 Done (2026-10-19): checked every item of the critique checklist by hand, searched the name and found a similar festival, asked for the name change and for 65 programme items. To do: Moodle upload. |

### Presentation split
Team size is three (confirmed by the team on 2026-10-19; the course has not assigned a fourth member). Each person presents one or two slides.

| Slides | Presenter |
|---|---|
| 1 Festival, purpose and main decisions; 5 Use of AI and verification | Faiaz Hossain Mazumder Yen (A) |
| 2 Target groups; 3 Information architecture | Oscar Muz (B) |
| 4 Two key scenarios | Sebastian Betancur (C) |

### What was decided by the team (not by AI)
- **Concept:** Faiaz and the team chose Valencia with the Dominican-roots theme from three options AI proposed. The reason is in section 1. The team call with B and C took place on 2026-10-19.
- **Name:** the first name, "Raíces del Mar", was dropped because of the real festival RAICES. The second name was dropped after Sebastian (C) searched it and found a festival with a similar name, and judged it too generic. The team then chose "Atardecer Bachata Festival" from options AI had searched. Atardecer is Spanish for sunset.
- **Dates and extras:** 3 days, 25–27 June 2027. Roots page and sustainability note kept. Partners row, Volunteers page, and talks as item types rejected.

### Accepted, changed, rejected
- **Rejected:** the first name "Raíces del Mar", because a web search found a real festival, RAICES, with the same word and a 5th edition. The second name, "Latino Mar Bachata Festival", because Sebastian found a festival with a similar name. 72 programme items, cut to 65, which is closer to the minimum of 60. The 4-day length, because the brief asks for 3 days.
- **Changed:** the spec structure was rewritten from a free-form draft to the sections the course requires (identity, purpose, target groups, information architecture, scenarios), plus interactive functions and the data model. Detail URLs changed from `?id=` to `?slug=`. Timezone: the brief's schema prompt says Europe/Prague, which is for a Czech festival. Our festival is in Valencia, so we use Europe/Madrid. In June both are UTC+02:00.
- **Accepted:** the data schema (approved by Faiaz, with 3 venues and the 64-performer mix). The spec text was checked by Sebastian (C) by hand. Oscar (B) is still reviewing it.

### How we checked
- Name: web searches for six names, then for the exact chosen name (no exact match found). To be repeated by hand.
- Data: `python3 scripts/validate-data.py` checks counts, duplicate ids and slugs, all references, performers in at least one item, venue overlaps, performer double-booking, date range, `dayId` and `dayPart`, sensible workshop times, and real-artist names. **Real errors found:** the first run reported 9 errors. Eight late-night sets that start after midnight were given the wrong `dayId`, and one Sunday set started on 28 June. The cause was that our schema had no rule for after-midnight sets, so we added a programme day of 06:00 to 06:00. While fixing this we also found that a 01:30 set was labelled `day`, so `dayPart` now treats 00:00–05:59 as `night`. After the fix the run reports 0 errors.
- Validator test: we broke the data on purpose in 11 ways (venue overlap, performer in two places, unknown performer id, duplicate slug, unused performer, beginner workshop at 02:00, real artist name, date outside the festival, wrong `dayPart`, wrong UTC offset, too few performers). The validator caught all 11.
- XML: `python3 scripts/json-to-xml.py` writes `data.xml` and re-reads it. It confirms 3 venues, 64 performers and 65 programme items, identical ids, and that every venue and performer reference resolves.
- Spot check: 10 random records were read by hand, on the first version with 72 items and again on the final version with 65 items. Example: item-018, a club social at 01:30 on Saturday morning, belongs to Friday night; item-023 is a beginner workshop at 11:00. Times make sense for a bachata festival, and all beginner workshops start between 09:30 and 15:30. **The hand check found a problem the validator cannot see:** a beginner specialist was co-teaching an advanced class, and instructors who teach leaders were teaching a follower workshop. We added teaching-fit rules to the generator and checked again: 0 mismatches.
- Scenarios: Scenario 1 has four Saturday beginner follow or both workshops, two of which do not clash. Scenario 2 has four Friday club sets with a DJ and an end time each. Scenario 3 has instructors teaching up to three workshops.

The step-by-step record is in `ai-log.md`.
