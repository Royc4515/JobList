# CLAUDE.md - Operating guide for the JobList tracker

Roy's job-search tracker. Each role is a Markdown file with YAML frontmatter
under `applications/`; networking contacts live under `leads/`. The README
dashboard is auto-generated - never hand-edit it.

## Workflow for any change
1. Add/edit the relevant `applications/*.md` or `leads/*.md` file.
   - New application: copy `templates/application.md`, filename kebab-case
     `<company>-<role>.md`.
   - New lead: copy `templates/lead.md`.
2. Run `python3 scripts/build_dashboard.py` to regenerate the README dashboard.
3. Commit and push.

## Frontmatter rules
- `status` allowed values ONLY: `not-submitted | submitted | in-review |
  interview | offer | rejected`.
- `applied` / `follow_up`: ISO date (e.g. 2026-08-09) or empty.
- Set `gmail:` to a one-line status summary. Hebrew is fine in `gmail:` and
  `## Notes`.

## How Roy wants me to operate (standing agreement)
- Be autonomous. Open a PR to `main` whenever a batch of work is ready - do NOT
  wait to be asked each time. Reconcile branch work back into `main` so the
  daily automation (below) stays accurate.
- Solve problems end-to-end (broken automation, wrong data, divergence) without
  handing them back unless a real decision needs Roy.
- No em dashes in values written to Roy's Google Sheets; use a plain hyphen.
- Only mark a role `submitted` with real evidence (a confirmation email) or
  Roy's explicit confirmation. Otherwise `not-submitted`.

## Determining application status from Gmail
A confirmation email ("we received your application", "your application was
sent to X") means submitted - use its date. Job-board digests (Alljobs,
SecretHunter, LinkedIn "jobs similar to" / "is hiring") are NOT applications;
never mark those submitted.

## Automation
A daily Routine "Daily JobList Gmail Sweep" (05:00 UTC) scans Gmail and commits
straight to `main`. It clones/pushes `Royc4515/JobList` (exact casing matters -
the git proxy allowlist is case-sensitive). If it fails to push, check the repo
name casing in the Routine prompt first.
</content>
