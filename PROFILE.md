# Roy's search profile

Shared reference for every agent in `.claude/agents/`. Read this before judging any
posting. Keep it current - if Roy's situation changes, update it here once rather
than in each agent.

## Who
- Roy Carmelli. Third-year B.Sc., **Computer Science + Neuroscience**, Bar-Ilan
  University (Ramat Gan). **Expected graduation: February 2028** - about three semesters
  (~17 months) remaining as of October 2026. Available 2-3 days a week.
- Reservist. Served as a battalion medic in the Gaza sector from 7 October and
  continues reserve duty - availability can be interrupted by call-ups.
- GitHub: https://github.com/Royc4515 - Portfolio: https://roy-carmelli-portfolio.vercel.app/

## Strengths (claim these)
- **Python** is the main language.
- **Daily AI-tooling practice**: Claude Code, MCP. Builds agents unprompted:
  Aside (browser extension talking to six model providers), Wine Sommelier
  (Telegram agent), this JobList tracker, LAMBDA (academic management).
- Data Structures: 93.
- MongoDB from an advanced systems programming course (coursework, not production).

## Gaps (never overclaim these)
- No industrial cloud / DevOps (AWS, Docker, CI/CD).
- Java and Kotlin light. Relational SQL basic.
- No production code yet.

## Target roles
**Tier 1 - the bullseye:** AI Engineer, GenAI / LLM Engineer, Applied AI Engineer,
Backend Developer, Python Developer - all as student positions.

**Tier 2 - wider net:** Software Engineer, Automation Engineer, Data Engineer,
Integration Engineer, Algorithm Developer - student positions.

**Tier 3 - rare and distinctive:** NeuroAI / computational neuroscience, research
engineer on medical AI or brain data.

## Skip
QA / Software Quality, IT support, non-engineering roles (accounting, HR, branding,
operations), hardware / firmware / physical design, PhD-only roles.
Exception: an application already tracked stays tracked regardless of category.

## Hard gates - check every posting
1. **Studies remaining.** Roy graduates February 2028: three semesters left from
   October 2026. "3 semesters" passes; "1.5 years" is borderline (~17 months); "2 years"
   fails. Older wording below assumed one year. A posting that requires 1.5+
   years or 3+ semesters remaining is a likely fail; say so plainly.
2. **Grades.** Roy's GPA is not recorded here. If a posting sets a cutoff, flag it
   as "verify GPA" - never guess whether he passes.
3. **Location.** Base is Ramat Gan. Tel Aviv / Gush Dan / Herzliya / Petah Tikva are
   easy; Haifa, Jerusalem, Be'er Sheva and the north are long commutes unless hybrid.
4. **Scope.** Full-time student plus reserve duty: 2-3 days a week fits, 4+ is heavy.

## Fit score rubric
Every tracked role gets four sub-scores, 0-10 each, stored as frontmatter keys.
`scripts/build_dashboard.py` adds them into a total out of 40 and ranks the
not-submitted roles by it. Never store the total yourself - it is derived so it
can never disagree with its parts.

| Key | Measures | Anchors |
| --- | --- | --- |
| `fit_role` | Direction | Tier 1: 8-10 · Tier 3: 8-9 · Tier 2: 5-7 · adjacent but off-direction (security research, Android, DevOps, .NET): 2-4 · Skip category: 0-1 |
| `fit_stack` | Must-haves Roy really has (Strengths/Gaps above) | Core is Python / AI tooling: 8-10 · gaps are nice-to-haves only: 6-7 · a learnable must-have missing (Java/Spring, SQL): 3-5 · a hard must-have missing (C#/.NET, reverse engineering): 0-2 |
| `fit_gates` | Hard gates 1-4 | All clear: 9-10 · commute, heavy scope or "verify GPA": subtract 1-3 each · **any hard gate failed: 0** |
| `fit_path` | Route to a human | Referral made: 9-10 · warm insider in `leads/`, not yet asked: 7-8 · contact asked and pending, or cold at a startup / small company: 5-6 · cold through a big-brand ATS: 2-3 |

- **`fit_gates: 0` means disqualified, not low.** The dashboard lists it under
  "Gated out" regardless of the other three, because a failed gate is usually an
  automatic ATS rejection. Studies-remaining is the gate that fails most often.
- `fit_path` is weighted on purpose. Roy's only interview so far came from a
  startup, and the method agreed with Afik is to find a contact before applying.
  A cold big-brand application scores low here by design.
- Add `fit_note:` - one line on what drives the score.

## WhatsApp groups to scan
<!-- Filled on the first /job-hunt run: whatsapp-scout proposes job groups from
     the chat list and Roy confirms them. The scout reads ONLY groups named here -
     add or remove lines by hand at any time. -->
