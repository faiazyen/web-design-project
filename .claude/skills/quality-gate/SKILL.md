---
name: quality-gate
description: Run before every commit that touches web/ or data. Reports pass/fail per check.
---
1. python3 scripts/validate-data.py  (data integrity)
2. Every page: one h1, no skipped headings, title + meta description + viewport present.
3. Every img has alt; every input/select has a label; no div used as a button.
4. No external framework, no fetch() of local files, no npm imports in web/.
5. No horizontal overflow at 320px (check CSS widths, images max-width:100%).
6. JSON-LD values match visible text on the page.
Report a table: check | pass/fail | file:line | fix. Do not mark pass without evidence.
