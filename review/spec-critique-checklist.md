# Spec critique checklist (Step 1.3)

**For:** Sebastian Betancur (C), with Oscar Muz (B) for spec text and scenarios.
**Ticks:** Sebastian reported on 2026-10-19 that he checked every item by hand. He cannot edit `.md` files, so Claude entered the ticks on his instruction (marked "S.B."). Item 31 and the name-related notes stay open because the name is being changed.
**What to do:** read `project-specification.md` against the assignment line by line. Tick each box **yourself** after you check it. A box ticked by the AI does not count: the course says "we verified it using AI" is not validation.
**Files to check:** `project-specification.md`, `data.json`, `data.xml`.

## A. Official requirements for the spec ("must contain at least")

| # | Requirement from the assignment | Where in the spec | Checked by C (tick and date) |
|---|---|---|---|
| 1 | Festival Identity table: name | Section 1 | ☑ S.B. 2026-10-19 |
| 2 | Edition / year | Section 1 | ☑ S.B. 2026-10-19 |
| 3 | Location | Section 1 | ☑ S.B. 2026-10-19 |
| 4 | Date range | Section 1 | ☑ S.B. 2026-10-19 |
| 5 | Type / character | Section 1 | ☑ S.B. 2026-10-19 |
| 6 | Main genres or themes | Section 1 | ☑ S.B. 2026-10-19 |
| 7 | Purpose: what the website is for | Section 2 | ☑ S.B. 2026-10-19 |
| 8 | Purpose: main objectives | Section 2 | ☑ S.B. 2026-10-19 |
| 9 | Purpose: important user actions | Section 2 | ☑ S.B. 2026-10-19 |
| 10 | Target groups (each with needs, expectations, information or functions) | Section 3 | ☑ S.B. 2026-10-19 |
| 11 | Sitemap | Section 4 | ☑ S.B. 2026-10-19 |
| 12 | Main navigation | Section 4 | ☑ S.B. 2026-10-19 |
| 13 | Relationships between main sections | Section 4 | ☑ S.B. 2026-10-19 |
| 14 | One-line purpose of each section | Section 4 | ☑ S.B. 2026-10-19 |
| 15 | Home page | Section 4 | ☑ S.B. 2026-10-19 |
| 16 | Programme | Section 4 | ☑ S.B. 2026-10-19 |
| 17 | Performers: list and detail pages | Section 4 | ☑ S.B. 2026-10-19 |
| 18 | Venues / stages | Section 4 | ☑ S.B. 2026-10-19 |
| 19 | Practical information | Section 4 | ☑ S.B. 2026-10-19 |
| 20 | Additional interactive sections for this festival | Sections 4 and 5 | ☑ S.B. 2026-10-19 |
| 21 | Several user scenarios, each with user type, goal, initial situation, expected outcome | Section 6 | ☑ S.B. 2026-10-19 |
| 22 | At least 3 key scenarios marked | Section 6 | ☑ S.B. 2026-10-19 |

## B. Extra requirements from the team brief

| # | Requirement | Where | Checked by C |
|---|---|---|---|
| 23 | Programme filters: day, venue, type, level | Sections 4, 5 | ☑ S.B. 2026-10-19 |
| 24 | Search field on every page and a results page | Sections 4, 5 | ☑ S.B. 2026-10-19 |
| 25 | My Programme (personal schedule) | Sections 4, 5 | ☑ S.B. 2026-10-19 |
| 26 | Breadcrumbs on all inner pages | Section 4 | ☑ S.B. 2026-10-19 |
| 27 | Practical info has tickets, travel, accommodation, accessibility, FAQ, code of conduct | Section 4 | ☑ S.B. 2026-10-19 |
| 28 | At least 4 interactive functions, each naming the user need it serves | Section 5 | ☑ S.B. 2026-10-19 |
| 29 | Every scenario can be done with the planned data fields | Section 6 and `docs/data-schema.md` | ☑ S.B. 2026-10-19 |
| 30 | No sentence is generic enough to fit any festival | whole spec | ☑ S.B. 2026-10-19 |
| 31 | The festival is not a 1:1 copy of an existing festival (search the name by hand) | Section 1 | ☐ Open: S.B. searched on 2026-10-19 and found a festival with a similar name. The name is being changed, then searched again. |

## C. Data (`data.json`, `data.xml`) against the official minimum

| # | Requirement | Result found by script | Checked by C |
|---|---|---|---|
| 32 | 3 days | 3 | ☑ S.B. 2026-10-19 |
| 33 | 2 venues or stages | 3 | ☑ S.B. 2026-10-19 |
| 34 | 60 performers | 64 | ☑ S.B. 2026-10-19 |
| 35 | 60 programme items (team target 65) | 65 | ☑ S.B. 2026-10-19 |
| 36 | Entities: festival, venues, performers, programme items | all present | ☑ S.B. 2026-10-19 |
| 37 | Relationships unambiguous (ids only, no free-text names) | `validate-data.py` passes | ☑ S.B. 2026-10-19 |
| 38 | XML or JSON format | both provided, `json-to-xml.py` confirms they match | ☑ S.B. 2026-10-19 |

Run these yourself and paste the output into `docs/evidence/`:

```bash
python3 scripts/validate-data.py
python3 scripts/json-to-xml.py
```

## D. What changed versus the first AI draft (modified / rejected evidence)

Drafted by the AI from its own history. **C: confirm each line is true and add your own changes below.**

| # | First AI draft | Final | Why |
|---|---|---|---|
| 1 | Free-form structure (identity, audience, sitemap, navigation, search, "open sections") | The sections the course requires, plus interactive functions and the data model | Draft did not match the required structure. Sebastian later removed the technical principles (SEO, AEO, GEO, WCAG) and the reference-site text because the course did not ask for them. |
| 2 | Name "Raíces del Mar", 5th edition | "Latino Mar Bachata Festival", 1st edition | A real festival, RAICES (5th edition), uses the same word and theme |
| 3 | 4 days (24–27 June) | 3 days (25–27 June 2027) | The team brief asks for a 3-day range |
| 4 | Pages "Artists" and "Workshops" | Programme, Performers, Venues | Required sitemap items |
| 5 | Detail pages by `?id=` | `?slug=` | The brief asks for slugs in detail URLs |
| 6 | Volunteers page, partners row, talks as item types (AI proposals) | Rejected by the team | Not needed for the brief |
| 7 | Schema day rule: `dayId` = calendar date of the start | Programme day 06:00–06:00 | The validator reported 9 errors on after-midnight sets |
| 8 | `dayPart` night = 20:00 or later | Night = 20:00 or later, or before 06:00 | A 01:30 set was labelled "day" |
| 9 | Timezone Europe/Prague (from the brief's template prompt) | Europe/Madrid | The festival is in Valencia. Both are UTC+02:00 in June. |
| 10 | 3 concepts offered at step 1.1 | Not changed | The brief asks for 5. The team already chose. Noted as a limitation. |

**Changes by B or C (write here):**

-
-

## E. Open items before submission

| # | Item | Owner | Done |
|---|---|---|---|
| 1 | Search "Latino Mar Bachata Festival" online by hand and note the date | C | ☑ S.B. 2026-10-19 |
| 2 | Read all bios and descriptions in `data.json` and rewrite any that sound generic | B | ☑ S.B. 2026-10-19 |
| 3 | Check the 2019 UNESCO line and the airport metro time (Roots and Travel text) | B | ☑ S.B. 2026-10-19 |
| 4 | Fill your own words into section 9 of the spec | B and C | ☑ S.B. 2026-10-19 |
| 5 | Rehearse the 3–5 minute presentation once with a timer | all | ☑ S.B. 2026-10-19 |
| 6 | Upload `project-specification.md`, `data.json`, `data.xml` and the presentation file to Moodle **before** the seminar | C | ☑ S.B. 2026-10-19 |
