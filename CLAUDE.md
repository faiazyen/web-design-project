# Project: Atardecer Bachata Festival website (CZU Web Design, team of 3)

Repo and folder name stay **web-design-project**.

## Hard constraints (never break)
- Pure client-side: HTML, CSS, vanilla JS. NO npm packages in the site, NO build step,
  NO frameworks (React, Vue, Tailwind, Bootstrap), NO backend, NO database.
- Must work by double-clicking web/index.html (file://). Never use fetch() for local data.
  Data comes from web/js/data.js, generated from /data.json by scripts/build-data.py.
- data.json is the single source of truth. Never edit data.js by hand.
- Mobile-first CSS (min-width media queries), no horizontal overflow at 320px.
- Semantic HTML: header, nav, main, section, article, aside, footer, time, address,
  lists, tables only for tabular data, every form control has a <label>.
- One h1 per page, no skipped heading levels.
- WCAG 2.0 AA minimum: contrast 4.5:1, visible focus, keyboard operable, alt text,
  skip link, aria only where native HTML is not enough.
- Every page: specific <title>, meta description, viewport, canonical, Open Graph.
- JSON-LD (schema.org Event/Festival, Place, Person) must match visible content exactly.
- All texts and images are AI-generated or free-licensed; record the source.
- Login is a client-side simulation only (no backend): accounts and each user's saved programme live in
  localStorage, and no password is ever stored (see project-specification.md, simulated sign-up and login flow).

## Wireframes (strict)
- All wireframes and prototypes in this project use **mid-level fidelity**, for the whole project:
  real layout and section order, real labels and navigation text, realistic placeholder content, defined
  components and states, neutral grayscale. No low-fi sketches, no final colours, photos or polished type.
- Applies to everything in prototype/. Ask the team before changing this rule.

## Design decisions (team, 2026-11-03)
- Brand look for the real build: palette A "Golden Hour", fonts Fraunces + Source Sans 3 (bundled locally),
  12 illustrated avatars for the 56 non-featured performers. Details and hex values: docs/design-kit.md.
- The Seminar 3 prototype (prototype/) is mid-fidelity grayscale and frozen after Seminar 3.

## Scope lock
- project-specification.md is binding (max ~15% change). If a task would change the
  sitemap, entities or scenarios, STOP and ask. Do not silently diverge.

## Workflow
- Before coding: state the plan in 3-6 bullets and wait for approval.
- After each task: run the quality-gate skill, then append an entry with the ai-log skill.
- Small commits with clear messages. Never commit secrets or API keys.
- prototype/ is frozen after Seminar 3. Never edit it afterwards.

## Git (project owner's rule)
- Repo is **public**: github.com/faiazyen/web-design-project.
- After every change: commit and push. The local folder and GitHub must always match
  (`git status` clean and in sync with `origin/main`).

## References
- 21st.dev (React + Tailwind) and Google Stitch exports are inspiration only; never ship their code.

## Structure
```
project-specification.md   binding spec
data.json                  content source of truth
documentation.md           final write-up
ai-log.md                  graded AI log
prototype/                 Stitch / design prototypes (not shipped)
web/                       the shipped site: css/, js/, images/
review/                    review notes
scripts/                   build-data.py, validate-data.py
docs/evidence/             screenshots and validation proof
.claude/skills/            ai-log, quality-gate
```
