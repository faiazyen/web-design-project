# Latino Mar Bachata Festival (web-design-project)

CZU Web Design course project: a website for a fictional bachata festival in Valencia, 25–27 June 2027. Sea by day, club by night.

**Team:** Faiaz Hossain Mazumder Yen (A), Oscar Muz (B), Sebastian Betancur (C).

## Seminar 2 deliverables

| File | What it is |
|---|---|
| `project-specification.md` | Specification: identity, purpose, target groups, information architecture, interactive functions, scenarios, data model, AI use |
| `data.json` | Data foundation (source of truth): 1 festival, 3 days, 3 venues, 64 performers, 65 programme items |
| `data.xml` | The same data as XML, generated from `data.json` |
| `presentation.pptx` | 5-slide presentation (3 to 5 minutes) |

## Supporting files

- `ai-log.md`: log of every AI-assisted step (what AI did, how it was checked, what was accepted, changed, rejected)
- `docs/data-schema.md`: data schema with one example per entity
- `docs/reference-analysis.md`: analysis of the reference festival site (inspiration only)
- `review/spec-critique-checklist.md`: checklist for B and C
- `CLAUDE.md` and `.claude/skills/`: project rules and skills for Claude Code

## Commands (Python 3, no installs)

```bash
python3 scripts/validate-data.py   # check data.json
python3 scripts/build-data.py      # data.json -> web/js/data.js
python3 scripts/json-to-xml.py     # data.json -> data.xml, and check they match
```

The website itself (`web/`) is plain HTML, CSS and JavaScript, with no build step, and works from `file://`. It is built in later phases.
