# AI Log

Format per entry: **Prompt → What AI did → How I checked → Accepted / Rejected.**

## 2026-10-19 — Setup (Claude Code, Sonnet 5.5)

### 1. Which GitHub account is active?
- **AI did:** ran `gh auth status`; reported account `faiazyen`, HTTPS, scopes `repo`, `workflow`, `read:org`, `gist`.
- **Checked:** read the command output myself.
- **Accepted:** yes.

### 2. Create a GitHub repo for this folder
- **AI did:** found the folder empty, asked for name and visibility, then created public repo `web-design-project` with a one-line README.
- **Checked:** opened the repo link; `gh` reported it public.
- **Accepted:** yes.

### 3. Separate `bachata-festival` repo (rejected)
- **AI did:** created a *private* `bachata-festival` repo and cloned it, which went against my instruction that repos be public. After I corrected it, it switched the repo to public. The first push failed with `403 repository is disabled`; a retry minutes later worked.
- **Checked:** `gh repo view` for visibility, `git ls-remote` to compare hashes.
- **Rejected:** I decided to keep the project name **web-design-project** and not use `bachata-festival`. That repo is unused.
- **Lesson:** state visibility explicitly; verify local and remote match after every push.

### 5. Festival identity options
- **AI did:** proposed three fictional festivals (Sabor del Mar in Valencia, Noches de Bachata in Berlin, Raíces in Santo Domingo) with name, edition, location, dates, character, genres and themes, and recommended A.
- **Checked:** I compared them against site workload, imagery and WCAG AA contrast.
- **Accepted:** location, edition and dates from A; genres and themes from C.
- **Rejected:** B (dark neon theme, harder AA contrast) and the Santo Domingo location.
- **Follow-up from me:** "theme of the sea" and "theme of number C". AI read this as two themes together (the sea plus C's roots and heritage) and made both explicit in the themes row.
- **AI then:** wrote section 1 of `project-specification.md`. It invented the merged working name "Raíces del Mar", which I have not yet confirmed.

### 6. Audience, sitemap, navigation and search
- **AI did:** I chose to keep the name "Raíces del Mar". AI wrote sections 2–5 of the spec: three audiences, goals with testable checks, a 12-page sitemap, navigation and breadcrumb rules, and search behaviour.
- **Design choice to check:** artist and workshop detail pages are one template each, filled from `?id=` and `data.js`, which keeps the site build-free and `file://`-safe.
- **Flagged by AI:** the final brief's list of required sections was not available, so the sitemap carries an assumption note to confirm.
- **Checked:** I need to compare the sitemap with the final brief. Not done yet.

### 4. Project setup in this repo
- **AI did:** created the required folder structure, `CLAUDE.md` with the project rules, and this log.
- **Checked:** reviewed the rules against the brief (no build, `file://`, semantic HTML, AI logging).
- **Accepted:** yes.

## 2026-10-19 – Install project rules and skills; analyse reference site – Claude Code
- Tool/model: Claude Code (Sonnet 5.5), Firecrawl scrape (19 pages of bachatagenevafestival.com)
- Prompt (short): "Inspect this festival website A to Z, every page and its structure"; paste of CLAUDE.md rules and the ai-log and quality-gate skills.
- What AI produced: `CLAUDE.md` (replaced my earlier version with the supplied rules, kept the public-repo and commit-and-push rule), `.claude/skills/ai-log/SKILL.md`, `.claude/skills/quality-gate/SKILL.md`, and `docs/reference-analysis.md` (sitemap, patterns, gaps, proposed adaptations).
- How we verified it: page lists and links came from the scraped home-page link list; 19 of the linked pages returned HTTP 200. Facts in the analysis were checked against the scraped text. Not yet checked visually in a browser.
- Accepted: pending review by the user.
- Modified (what and why): none yet.
- Rejected (what and why): `/terms`, `/privacy` and `/hq` were not analysed (legal text and a private dashboard).
- Errors/limitations found: Firecrawl rate-limited the first batch (`429`), so nine pages were retried, and the last 11 pages were read as summaries, not full text. The reference mixes 2026 and 2027 data (ticket price €199 vs €140). Visual design, fonts and the interactive maps were not inspected. `scripts/validate-data.py` and `scripts/build-data.py`, which the rules and the quality-gate skill call, do not exist yet.

## 2026-10-19 – Name check, concept decisions, deeper reference analysis – Claude Code
- Tool/model: Claude Code (Sonnet 5.5), Firecrawl search and scrape, built-in browser
- Prompt (short): check the name for clashes; suggest new names; analyse the Geneva site further for visual identity and ideas we are missing.
- What AI produced: six candidate names; a rename recommendation; sections 7 and 8 added to `docs/reference-analysis.md` (visual and navigation findings, 14 vibe ideas).
- How we verified it: name searches (5 results each) dropped three names that already exist (Ola Latina, Sal y Sol, Brisa Bachata) and found a real festival "RAICES" (5th edition) that clashed with our first name. The Geneva navigation, fonts and the missing search and breadcrumbs were checked in the live page DOM, not only from scraped text. Excerpt-level search is not proof, so the team must still search the chosen name by hand.
- Accepted (team decisions, by Faiaz): name **Latino Mar Bachata Festival**; dates Fri 25 – Sun 27 June 2027; genres bachata dominicana, sensual, moderna plus salsa; character social-first, beginner-friendly, sea by day and club by night; keep the Roots page and the sustainability note; drop the partners row, the Volunteers page and talks and live music as item types. Team concept call with B and C: done.
- Reason for the concept (Faiaz, in own words): a Latin bachata festival where people from around the world come to dance. Valencia is a clean, modern Spanish city with good sea access, so there is outdoor dancing by the sea and indoor dancing at night, with bars, artists, shows and DJs playing bachata, Latin American music and salsa.
- Modified: none yet.
- Rejected: the name "Raíces del Mar" (clashes with the real festival RAICES); the 4-day length (brief asks for 3 days).
- Errors/limitations found: browser inspection did not show the dropdown contents except Support, which lists FAQ. The earlier JSON extraction of the nav menu disagreed with the live page and was discarded. Open: names of team members B and C not yet provided; edition number (1st) not yet confirmed.

## 2026-10-19 – Step 1.1 Lock the concept – Claude Code (chat), decided by the team
- Tool/model: Claude Code (Sonnet 5.5); Firecrawl web search
- Prompt (short): asked for concept options for a fictional bachata festival, then for new names after a clash was found.
- What AI produced: three concepts (Valencia, Berlin, Santo Domingo), six name candidates.
- How we verified it: web searches per name (5–8 results each). A real festival "RAICES" (5th edition) clashed with the first name, so it was rejected. Three further names (Ola Latina, Sal y Sol, Brisa Bachata) already exist. Exact search for "Latino Mar Bachata Festival" found no match. The team still searches by hand.
- Accepted: Valencia location with the Dominican-roots theme; name Latino Mar Bachata Festival; 3 days, 25–27 June 2027. Decided by Faiaz after the team call with Oscar Muz and Sebastian Betancur.
- Modified (what and why): date range cut from 4 days to 3 because the brief asks for 3.
- Rejected (what and why): Berlin concept (dark neon, harder AA contrast, too different from the team's vision); the name "Raíces del Mar" (clash with RAICES).
- Errors/limitations found: the brief asks for 5 concepts; AI gave 3. Search results were excerpts only.
- Reason for the choice (Faiaz): a Latin bachata festival where people from around the world come to dance. Valencia is clean and modern with good sea access, so dancing outdoors by the sea and indoors at night, with bars, artists, shows and DJs playing bachata, Latin music and salsa.

## 2026-10-19 – Step 1.2 Draft the specification – Claude Code
- Tool/model: Claude Code (Sonnet 5.5)
- Prompt (short): write `project-specification.md` with the 9 required sections for the chosen concept; the sitemap must include all pages named in the brief.
- What AI produced: the spec with 9 sections, a 17-page sitemap, 4 target groups, 7 interactive functions, 5 scenarios (3 KEY), data model summary.
- How we verified it: AI re-read the brief line by line: identity table has the 6 fields; sitemap includes Home, Programme with day/venue/type/level filters, item detail, performers and venues lists and details, six practical pages, search on every page plus results page, My Programme, and breadcrumbs; every scenario has user type, goal, situation and outcome; every function names its user need. Independent review by B and C is still to do.
- Accepted: pending B and C review.
- Modified (what and why): an earlier free-form draft was replaced because it did not follow the 9-section structure. Detail URLs changed from `?id=` to `?slug=` to match the brief's schema step. Timezone Europe/Madrid instead of the brief's Europe/Prague (our festival is in Valencia; both are UTC+02:00 in June).
- Rejected (what and why): Volunteers page, partners row, talks as item types (team decision, not needed for the brief).
- Errors/limitations found: B and C role assignment for Oscar Muz and Sebastian Betancur not yet confirmed. Section 9 is partly filled and needs validator results.

## 2026-10-19 – Step 1.4 Propose the data schema – Claude Code
- Tool/model: Claude Code (Sonnet 5.5)
- Prompt (short): propose a JSON schema for `data.json` with ids, slugs, ISO 8601 times with timezone, address fields, performer and venue references, and fields for every filter. Do not generate data.
- What AI produced: `docs/data-schema.md` with field tables for festival, days, categories, venues, performers, programme items, one example record per entity, and a self-check table mapping every spec feature and scenario to fields.
- How we verified it: mapped each filter, search, function and scenario in the spec to a field; all rows answered. Examples are valid JSON by inspection; the validator will test real data.
- Accepted: waiting for Faiaz's approval.
- Modified (what and why): none yet.
- Rejected (what and why): none yet.
- Errors/limitations found: none yet. Data has not been generated (the brief says to wait for approval).

## 2026-10-19 – Step 1.5 Generate the data – Claude Code
- Tool/model: Claude Code (Sonnet 5.5). A one-off Python generator (kept outside the repo, in the session scratchpad) produced `data.json` from hand-written content lists.
- Prompt (short): generate `data.json` from the approved schema: 3 days, 3 venues, 64 performers, 72 programme items; fictional names only; every performer in at least one item; no venue overlaps; no performer in two places at once.
- What AI produced: `data.json` with 3 venues, 64 performers (22 instructors, 14 DJs, 6 bands, 6 singers, 16 show teams) and 72 items (36 workshops, 27 socials, 9 shows), plus festival content (tickets, accommodation, travel, FAQ, code of conduct, accessibility, sustainability, roots).
- How we verified it: `python3 scripts/validate-data.py`. First run: **9 errors** (8 after-midnight sets with the wrong `dayId`, 1 set starting on 28 June). Final run: 0 errors, 0 warnings. 10 random records read by hand. Scenario 1, 2 and 3 checked against real records.
- Accepted: the schema, the venue and performer mix, the content structure.
- Modified (what and why): added a programme-day rule (06:00 to 06:00) to the schema and the spec, because the validator showed the schema had no rule for sets after midnight. Changed `dayPart` so that 00:00–05:59 counts as night (a 01:30 set had been labelled day). Removed an internal note ("the team will confirm this fact") from the visible Roots text.
- Rejected (what and why): nothing rejected so far. Image files do not exist yet: the `src` paths in `data.json` are planned paths for AI-generated images, to be created and credited later.
- Errors/limitations found: performer bios and event descriptions are short and somewhat formulaic and need a human pass. Travel facts (airport metro time) and the 2019 UNESCO listing in the Roots timeline must be checked before publishing. Fictional venue and performer names were not individually searched online.

## 2026-10-19 – Step 1.5 Write and test the validator – Claude Code
- Tool/model: Claude Code (Sonnet 5.5)
- Prompt (short): write `scripts/validate-data.py` that checks the rules plus minimum counts, duplicate ids and slugs, and dates inside the festival range; run it and show the output.
- What AI produced: `scripts/validate-data.py` (standard library only, exit code 1 on any error).
- How we verified it: ran it on the real data (PASS), then on 11 deliberately broken copies. It failed all 11 with a clear message: venue overlap, performer double-booking, unknown performer id, duplicate slug, unused performer, beginner workshop at 02:00, real artist name, date outside the range, wrong `dayPart`, wrong UTC offset, too few performers.
- Accepted: the validator as written.
- Modified (what and why): the date and `dayPart` checks were rewritten for the programme-day rule after the first run.
- Rejected (what and why): none.
- Errors/limitations found: the real-artist list is a short blocklist of well-known names and cannot guarantee no clash with any real person. The validator checks structure and logic, not whether the text makes sense.

## 2026-10-19 – Step 1.6 Data for the website – Claude Code
- Tool/model: Claude Code (Sonnet 5.5)
- Prompt (short): write `scripts/build-data.py` that converts `data.json` into `web/js/data.js` as `window.FESTIVAL_DATA = {...};` with a generated-file header.
- What AI produced: `scripts/build-data.py` and the generated `web/js/data.js` (about 110 KB).
- How we verified it: ran the script, read the header and the end of the file, and confirmed the file parses as JavaScript (a one-off check in a local runtime; the site itself uses no Node).
- Accepted: yes.
- Modified (what and why): none.
- Rejected (what and why): none.
- Errors/limitations found: `data.js` is not yet loaded by any page, so the `file://` behaviour has not been tested in a browser.

## 2026-10-19 – Step 1.7 Roles confirmed, final commit – Claude Code
- Tool/model: Claude Code (Sonnet 5.5)
- Prompt (short): Faiaz confirmed Oscar Muz is B and Sebastian Betancur is C; fill section 9 from the log and commit.
- What AI produced: section 9 of the spec updated with the roles, concrete validator evidence and the test results.
- How we verified it: compared each claim in section 9 with the validator output and this log.
- Accepted: pending review by B and C.
- Modified (what and why): none.
- Rejected (what and why): none.
- Errors/limitations found: B has not yet reviewed the spec text and C has not yet written the critique (step 1.3), so the "changed versus the AI draft" list is still to be written by them.

## 2026-10-19 – Strict audit against the official Seminar 2 requirements – Claude Code
- Tool/model: Claude Code (Sonnet 5.5), scripts in `scripts/`, LibreOffice render of the deck
- Prompt (short): audit everything against the official Seminar 1/2 requirements and fix what is missing so the Seminar 2 deliverables are complete.
- What AI produced: an audit table; `data.xml` and `scripts/json-to-xml.py`; `presentation.pptx` (5 slides, speaker notes); `docs/image-prompts.md`; `review/spec-critique-checklist.md`; a rewritten `README.md`; small edits to the spec (data.xml, limits of our checking).
- How we verified it: `python3 scripts/validate-data.py` (0 errors); `python3 scripts/json-to-xml.py` (3 venues, 64 performers, 72 items, ids and references match JSON); `xmllint` finds `data.xml` well-formed; deck file passes the pptx validator; every slide was rendered and read as an image.
- Accepted: the deliverable set (spec, data.json, data.xml, deck).
- Modified (what and why): slide 1 had a heading that wrapped over its text and several slides had large empty areas; fixed by shortening the heading and raising body text to 17–18 pt.
- Rejected (what and why): nothing new.
- Errors/limitations found by the audit: (1) the official text says groups of 4, but only 3 people are named. Open question. (2) The submission list names `data.xml` and `data.json`, and we only had JSON. Fixed. (3) `data.json` pointed to `docs/image-prompts.md`, which did not exist. Fixed. (4) No presentation file existed, and only submitted files may be presented. Fixed. (5) Our own check of the spec against the brief was done by the AI. That is not valid verification, so a manual checklist for B and C was written. Still open until they tick it. (6) Bios and descriptions need a human pass; images do not exist yet; the name search must be repeated by hand.

## 2026-10-19 – Team size and presentation split confirmed – Claude Code
- Tool/model: Claude Code (Sonnet 5.5)
- Prompt (short): Oscar Muz and Sebastian Betancur, with Faiaz, confirmed the team has three members (no fourth assigned yet) and accepted the proposed slide split.
- What AI produced: a "Presentation split" table in section 9 of the spec.
- How we verified it: matched the table with the presenter lines in the speaker notes of `presentation.pptx` (slides 1 and 5 Faiaz, 2 and 3 Oscar, 4 Sebastian).
- Accepted: the split and the team size of three.
- Modified (what and why): closes the open question from the audit entry about "groups of 4". If the course adds a fourth member, the spec header, `CLAUDE.md` and slide 5 need updating.
- Rejected (what and why): none.
- Errors/limitations found: none new.

## 2026-10-19 – Sebastian's review round: 65 items, checklist ticks, name search – Claude Code, on request of Sebastian Betancur (C)
- Tool/model: Claude Code (Sonnet 5.5); Firecrawl web search; the one-off generator in the session scratchpad
- Prompt (short): Sebastian (C) asked to cut programme items from 72 to 65 (closer to the minimum of 60), reported that he checked the checklist by hand, and reported that the name needs to change because a similar festival exists.
- What AI produced: `data.json` regenerated with 65 items (36 workshops, 20 socials, 9 shows) and 64 performers; `data.xml`, `web/js/data.js` rebuilt; deck and docs updated to 65; checklist ticks entered; candidate festival names with web searches.
- How we verified it: `validate-data.py` 0 errors (minimum items now 65); `json-to-xml.py` match; every performer still appears in an item; spot check repeated on 10 random records of the final data.
- Accepted: 65 items; Sebastian's finding that the name is too generic and needs a new Latin-word name.
- Modified (what and why): the 7 socials removed were extra late practicas and late sets, so no performer lost all their sessions and the club schedule that the FAQ and scenarios describe is unchanged. Ticks on the checklist were entered by Claude on Sebastian's verbal confirmation because he cannot edit `.md` files; item 31 (name search) stays open.
- Rejected (what and why): candidate names that already exist: Ola Latina, Sal y Sol, Brisa Bachata, Marejada (a Latin music event and venue), Oleaje (a dance act at a salsa and bachata festival), Brisamar (clubs and bars), Ritmo y Raíz (a dance school offering bachata workshops).
- Errors/limitations found: **the hand spot check found a real error the validator cannot see:** a beginner specialist (Jimena Cruz) was co-teaching an advanced lead class, and instructors who teach leaders were teaching a follower workshop. Fixed with teaching-fit rules in the generator (0 mismatches afterwards). The spec's spot-check text had cited item ids from the old 72-item version; it was rewritten to match the new data. Name searches are excerpt-only (5 results each).

## 2026-10-19 – Spec trimmed to what the course asks for – Claude Code, on request of Sebastian Betancur (C)
- Tool/model: Claude Code (Sonnet 5.5)
- Prompt (short): Sebastian asked to remove from `project-specification.md` the "limits of our checking" part, the tools list with Firecrawl and the reference-site text, the "closest real festivals" block, and the technical principles section (SEO, AEO, GEO), and to mark his role as done.
- What AI produced: the trimmed spec. Technical and Quality Principles removed (old section 8); "Use of AI and Verification" renumbered to section 8 and reduced to one tool line, the roles and presentation tables, and the decisions and checks; Sebastian's status set to done.
- How we verified it: checked the official requirements text. The spec must contain identity, purpose, target groups, information architecture and user scenarios. It does not mention SEO, AEO, GEO, structured data, WCAG or any technical rules, so removing them does not break a requirement. A search of the spec for "Firecrawl", "Geneva", "SEO", "AEO", "GEO", "WCAG", "inspiration" and "Limits of our" returns nothing.
- Accepted: all removals asked for.
- Modified (what and why): the technical rules (no build, `file://`, semantic HTML, WCAG, SEO) are no longer in the spec, but they stay in `CLAUDE.md` as the project's implementation rules, so later phases still follow them. Sebastian's status says "To do: Moodle upload" because the upload has not happened yet.
- Rejected (what and why): nothing.
- Errors/limitations found: the instruction "the third of the 9 sections, Use of AI and Verification, should be removed" conflicts with keeping the roles table inside that section, so the section was kept in short form and the question was sent back to the team. The record of the closest real festivals is still in this log (name search entries).

## 2026-10-19 – Festival renamed to Atardecer Bachata Festival – Claude Code, decided by the team (Sebastian proposed the change)
- Tool/model: Claude Code (Sonnet 5.5); Firecrawl web search
- Prompt (short): Sebastian found a festival with a name similar to "Latino Mar Bachata Festival" and called it too generic; the team asked for a Latin-word name. The team picked "Atardecer Bachata Festival".
- What AI produced: candidate names with exact web searches; a repo-wide rename (spec, data, XML, `data.js`, deck, README, `CLAUDE.md`, docs, checklist); the new slug `atardecer-bachata-festival-2027` and email domain `atardecer.example`.
- How we verified it: searched the exact name: no festival called "Atardecer Bachata Festival" appeared; results were songs and posts that use the word (for example "Bachata al Atardecer", "Bachata Sunset"). A search of the repo for the old name now finds it only in older log entries, which are kept as history. `validate-data.py` passes; `json-to-xml.py` confirms the XML matches; the deck file validates and slide 1 was re-read.
- Accepted: the name "Atardecer Bachata Festival" (Spanish for sunset; fits the daily sunset social).
- Modified (what and why): the spec's name story now lists both rejected names and the reason. Deck slides 1 and 5 say "renamed twice".
- Rejected (what and why): Orilla, Cala and Ola y Sal were kept in reserve; Marejada, Oleaje, Brisamar, Ritmo y Raíz were rejected because they already exist.
- Errors/limitations found: "Atardecer" is a common word, so the name is distinctive only with "Bachata Festival" after it, and searches only return excerpts. Sebastian must search the name by hand (checklist item 31 is still open).

## 2026-10-19 – Sitemap reduced from 17 to 12 pages – Claude Code, decided by the team
- Tool/model: Claude Code (Sonnet 5.5)
- Prompt (short): after an audit against the teacher's requirements, the team agreed to merge the six practical pages into one so the sitemap shrinks from 17 to about 12 pages. Everything else in the audit suggestions stays as it is.
- What AI produced: spec section 4 with one Practical info page (sections Travel, Accommodation, Accessibility, FAQ, Code of conduct) and a separate Tickets page, 12 pages in total; updated breadcrumbs, relationships, scenarios 4 and 5 and the target group table; deck slides 2 and 3 redrawn.
- How we verified it: searched the spec, README, docs and checklist for the old page names and the number 17 (no leftovers); rebuilt the deck, validated the file and read slide 3 as an image; data files unchanged (`validate-data.py` still passes).
- Accepted: the 12-page sitemap. Tickets stays its own page because it is the main call to action and the key user action "find ticket prices".
- Modified (what and why): the team said "about 12"; merging all six pages would give 11, so Tickets was kept separate to make 12.
- Rejected (what and why): the other audit suggestions (fewer interactive functions, shorter data model and section 8) were not applied, by the team's decision.
- Errors/limitations found: the spec still mentions `docs/data-schema.md` and scripts that are not in the Moodle upload.

## 2026-10-19 – Hand search of the final name – Sebastian Betancur (C), entered by Claude Code
- Tool/model: none (manual web search by Sebastian)
- Prompt (short): Sebastian searched "Atardecer Bachata Festival" by hand and reported the result.
- What AI produced: ticks for checklist items 1 and 31, and this entry.
- How we verified it: Sebastian's own search, reported to Claude on 2026-10-19. It agrees with the earlier AI search, which found only songs and posts that use the word.
- Accepted: the name, with no festival found under it.
- Modified (what and why): none.
- Rejected (what and why): none.
- Errors/limitations found: web searches cannot prove that no small local event uses a name.

## 2026-10-19 – Sebastian's section 8 answers – Sebastian Betancur (C), written into the spec by Claude Code
- Tool/model: Claude Code (Sonnet 5.5), questions answered by Sebastian as multiple choice
- Prompt (short): Claude asked Sebastian what he checked, found, decided, accepted and saw the AI get wrong; he chose the options.
- What AI produced: the "Sebastian's part (C)" subsection of section 8 in the spec, using only the options Sebastian ticked.
- How we verified it: each line matches a choice Sebastian made in this session; the spec facts (65 items, 12 pages, final name) match the files in the repo.
- Accepted: Sebastian ticked: spec and data checked against the brief; found the name too similar, 72 items too many, the spec trimmed, the sitemap cut to 12 pages; accepted the target groups, the scenarios and the presentation; saw the AI overdo names, scope, data count and bios.
- Modified (what and why): none.
- Rejected (what and why): none.
- Errors/limitations found: the answers are multiple choice, so the wording is Claude's. Sebastian should read his subsection and change anything that is not how he would say it.
