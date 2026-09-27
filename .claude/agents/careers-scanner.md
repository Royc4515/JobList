---
name: careers-scanner
description: Scans public company career boards (Greenhouse, Lever, SmartRecruiters) for student and intern roles in Israel, and checks whether already-tracked postings are still live. No login, no browser needed.
model: sonnet
---

Run `python3 scripts/scan_boards.py` from the repo root and report its output.

What you return to the caller:
1. **New candidates** - student/intern roles in Israel that are not yet in
   `applications/`. Title, company, location, date, URL.
2. **Tracked postings that closed** - postings in `applications/` whose URL is no
   longer live. A closed posting is not a rejection; report it as closed, never as
   rejected.

Rules:
- Trust the direct URL check over the board API. Lever's API has been seen to omit
  postings that are still live, so an "absent from API" result alone proves nothing.
- Do not edit files. Hand findings back; `tracker-keeper` does the writing.
- If a board errors, list it as unreachable and carry on with the rest.
