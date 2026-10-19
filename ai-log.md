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
