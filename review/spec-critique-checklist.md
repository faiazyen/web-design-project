# Spec critique checklist (Step 1.3)

**For:** Sebastian Betancur (C), with Oscar Muz (B) for spec text and scenarios.
**What to do:** read `project-specification.md` against the assignment line by line. Tick each box **yourself** after you check it. A box ticked by the AI does not count: the course says "we verified it using AI" is not validation.
**Files to check:** `project-specification.md`, `data.json`, `data.xml`.

## A. Official requirements for the spec ("must contain at least")

| # | Requirement from the assignment | Where in the spec | Checked by C (tick and date) |
|---|---|---|---|
| 1 | Festival Identity table: name | Section 1 | ☐ |
| 2 | Edition / year | Section 1 | ☐ |
| 3 | Location | Section 1 | ☐ |
| 4 | Date range | Section 1 | ☐ |
| 5 | Type / character | Section 1 | ☐ |
| 6 | Main genres or themes | Section 1 | ☐ |
| 7 | Purpose: what the website is for | Section 2 | ☐ |
| 8 | Purpose: main objectives | Section 2 | ☐ |
| 9 | Purpose: important user actions | Section 2 | ☐ |
| 10 | Target groups (each with needs, expectations, information or functions) | Section 3 | ☐ |
| 11 | Sitemap | Section 4 | ☐ |
| 12 | Main navigation | Section 4 | ☐ |
| 13 | Relationships between main sections | Section 4 | ☐ |
| 14 | One-line purpose of each section | Section 4 | ☐ |
| 15 | Home page | Section 4 | ☐ |
| 16 | Programme | Section 4 | ☐ |
| 17 | Performers: list and detail pages | Section 4 | ☐ |
| 18 | Venues / stages | Section 4 | ☐ |
| 19 | Practical information | Section 4 | ☐ |
| 20 | Additional interactive sections for this festival | Sections 4 and 5 | ☐ |
| 21 | Several user scenarios, each with user type, goal, initial situation, expected outcome | Section 6 | ☐ |
| 22 | At least 3 key scenarios marked | Section 6 | ☐ |

## B. Extra requirements from the team brief

| # | Requirement | Where | Checked by C |
|---|---|---|---|
| 23 | Programme filters: day, venue, type, level | Sections 4, 5 | ☐ |
| 24 | Search field on every page and a results page | Sections 4, 5 | ☐ |
| 25 | My Programme (personal schedule) | Sections 4, 5 | ☐ |
| 26 | Breadcrumbs on all inner pages | Section 4 | ☐ |
| 27 | Practical info has tickets, travel, accommodation, accessibility, FAQ, code of conduct | Section 4 | ☐ |
| 28 | At least 4 interactive functions, each naming the user need it serves | Section 5 | ☐ |
| 29 | Every scenario can be done with the planned data fields | Section 6 and `docs/data-schema.md` | ☐ |
| 30 | No sentence is generic enough to fit any festival | whole spec | ☐ |
| 31 | The festival is not a 1:1 copy of an existing festival (search the name by hand) | Section 1 | ☐ |

## C. Data (`data.json`, `data.xml`) against the official minimum

| # | Requirement | Result found by script | Checked by C |
|---|---|---|---|
| 32 | 3 days | 3 | ☐ |
| 33 | 2 venues or stages | 3 | ☐ |
| 34 | 60 performers | 64 | ☐ |
| 35 | 60 programme items | 72 | ☐ |
| 36 | Entities: festival, venues, performers, programme items | all present | ☐ |
| 37 | Relationships unambiguous (ids only, no free-text names) | `validate-data.py` passes | ☐ |
| 38 | XML or JSON format | both provided, `json-to-xml.py` confirms they match | ☐ |

Run these yourself and paste the output into `docs/evidence/`:

```bash
python3 scripts/validate-data.py
python3 scripts/json-to-xml.py
```

## D. What changed versus the first AI draft (modified / rejected evidence)

Drafted by the AI from its own history. **C: confirm each line is true and add your own changes below.**

| # | First AI draft | Final | Why |
|---|---|---|---|
| 1 | Free-form structure (identity, audience, sitemap, navigation, search, "open sections") | The 9 sections the team brief requires | Draft did not match the required structure |
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
| 1 | Search "Latino Mar Bachata Festival" online by hand and note the date | C | ☐ |
| 2 | Read all bios and descriptions in `data.json` and rewrite any that sound generic | B | ☐ |
| 3 | Check the 2019 UNESCO line and the airport metro time (Roots and Travel text) | B | ☐ |
| 4 | Fill your own words into section 9 of the spec | B and C | ☐ |
| 5 | Rehearse the 3–5 minute presentation once with a timer | all | ☐ |
| 6 | Upload `project-specification.md`, `data.json`, `data.xml` and the presentation file to Moodle **before** the seminar | C | ☐ |
