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
