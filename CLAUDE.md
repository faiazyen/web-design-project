# CLAUDE.md — Web Design Project (Bachata Festival website)

Course project: a website for a fictional bachata festival. The repo and folder name stay **web-design-project**.

## Hard rules (apply to every session)

1. **No build step, no Node, no framework.** The final site is plain HTML, CSS and JS in `web/`.
2. **Works from `file://`.** Open `web/index.html` by double-click. No server, no `fetch()` of local files.
3. **`data.json` is the source of truth.** `web/js/data.js` is generated from it by a script in `scripts/` (Python or shell, never Node). Never edit `data.js` by hand.
4. **Semantic HTML, WCAG AA, valid markup.** Landmarks, heading order, alt text, visible focus, AA contrast, keyboard operable.
5. **`project-specification.md` is binding.** After Seminar 2 only about 15% may change, each change with a written justification.
6. **Reference tools are inspiration only.** 21st.dev (React + Tailwind) and Google Stitch exports are never shipped. Rewrite ideas as vanilla HTML/CSS/JS.
7. **Required in the sitemap:** search, breadcrumbs, a search results page, and every section the final brief demands.

## AI logging

Log every AI session in `ai-log.md`: what the AI did, how it was checked, what was accepted, what was rejected. Add the entry at the time, not afterwards.

## Git

- Repo is **public**: `github.com/faiazyen/web-design-project`.
- After every change: commit and push. The local folder and GitHub must always match (`git status` clean, in sync with `origin/main`).
- Never commit secrets (API keys, `.env`).

## Structure

```
project-specification.md   binding spec
data.json                  content source of truth
documentation.md           final write-up
ai-log.md                  graded AI log
prototype/                 Stitch / design prototypes (not shipped)
web/                       the shipped site: css/, js/, images/
review/                    review notes
scripts/                   build-free helpers (data.json -> web/js/data.js)
docs/evidence/             screenshots and validation proof
```
