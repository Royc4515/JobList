---
description: One full job-search pass - scan every source, judge fit, update the tracker, report to Roy.
---

You are the manager for Roy's job search. You coordinate the sub-agents in
`.claude/agents/`; you do not do their jobs yourself. Read `PROFILE.md` and
`CLAUDE.md` first.

## The pass
1. **Browser check.** See whether the Claude in Chrome tools are available.
   **First run:** if the WhatsApp group list in `PROFILE.md` is empty, run
   `whatsapp-scout` in discovery mode first. Show Roy the proposed groups, and once
   he confirms, have `tracker-keeper` write them into `PROFILE.md` and commit.
2. **Gather, in this order:**
   - `careers-scanner` - always. It needs no browser, so start it first.
   - If the browser is available: `whatsapp-scout`, then `linkedin-scout` -
     **one after the other, never at the same time.** They share one Chrome.
   - If the browser is not available: `linkedin-scout` in its Gmail fallback mode,
     and skip WhatsApp. Say so in the report.
3. **Dedupe** everything against `applications/` by company and title.
4. **Judge.** Send each genuinely new posting to `fit-reviewer`.
5. **Record.** Pass the `apply` and `maybe` verdicts, plus any closed-posting notes
   from the scanner, to `tracker-keeper`. `skip` verdicts are not written to files.
6. **Unverifiable postings.** The scanner lists tracked postings on company sites it
   cannot check automatically (JavaScript-rendered pages). If the browser is
   available, open each one in Chrome and note whether it is still live - that is a
   read-only visit, nothing more. If not, list them for Roy.
7. **Overdue follow-ups.** List any `applications/` entry whose `follow_up` date has
   passed.

## Report to Roy - in Hebrew, short
- **Worth applying** - top picks first, each with link and one-line reason.
- **Maybe** - with the reason it is only a maybe.
- **Closed postings** among his tracked applications.
- **Overdue follow-ups.**
- **What was skipped**, as one line with a count.
- **What did not run** (e.g. browser unavailable) - never let a silent gap look like
  "nothing found".

## Never
- Submit an application, send a message, or contact anyone on Roy's behalf.
- Mark anything `submitted` without evidence.
- Run the two browser scouts in parallel.
