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

### 4. Project setup in this repo
- **AI did:** created the required folder structure, `CLAUDE.md` with the project rules, and this log.
- **Checked:** reviewed the rules against the brief (no build, `file://`, semantic HTML, AI logging).
- **Accepted:** yes.
