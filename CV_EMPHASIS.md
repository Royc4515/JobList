# CV emphasis - how to highlight (Roy's method, 2026-11-26)

HR does not read a CV; the eye lands on what stands out. This guide covers *how* to make the
right things stand out without the page shouting. It applies to every CV: the General one and
every tailored version (`scripts/tailor_cv.py` -> `scripts/style_cv.py`).

Formatting only. Never change wording or structure to create emphasis - those were approved
separately (recruiter + hiring manager review, 2026-11-25).

## 1. Emphasis is a scale, not yes/no

The body text is grey `434343`. Each level is one step louder than the one before it.

| Level | Look | Use it for | Budget (one page) |
|---|---|---|---|
| 0 - body | grey, regular | everything else | - |
| 1 - **soft** | same weight, near-black ink `161616` | keywords that match the posting, phrases that back a claim | about one per entry/bullet, never two side by side |
| 2 - **strong** | bold, softened black `262626` (not pure black) | the 2-4 hard facts a screener should leave with: role identity, real-user numbers, scale of leadership | 2-4 per page |
| links | blue `1A5FC8` + underline | anything clickable | - |
| key links | blue + underline + bold | project names (they head each entry), the portfolio | - |
| top link | key link, +0.5pt on the contact line | the portfolio only | 1 |

### Other tools: size, italic, and a different font

These are separate dimensions, and each is a scale of its own. Use them only after the critique
in section 2.

**Size (`"grow"` in the JSON, in half-points: 1 = +0.5pt).**
- It's the quietest way to push one fact a step above strong. The eye picks up a slightly bigger
  word without reading it.
- Only on top of strong, and only on a number with its noun. At most +0.5pt in running text
  (+1pt only on a standalone line). At most 2 per page.
- Critique: a size jump inside a line raises that line's height. More than +0.5pt starts to look
  like a typo or a copy-paste from another document. Re-check line breaks, since it widens the line.
- General CV: "1,500+ page views" and "12 to 30+ people" get +0.5pt. They're the two proofs to
  remember. "AI & Full-Stack developer" stays at normal size, because it's already near the top.

**Italic (`"italic": true`).**
- In a sans-serif font, italic reads as *different* and *quieter*, not louder. It's a tool for
  setting something apart, not for promoting it.
- Good for: a name or title of a thing (a course, a certificate, a study), or a short aside you
  want the eye to skip. Also good for a standalone line of context; the availability line is
  already italic for this reason.
- Critique: italic + bold together looks loud and off. Italic on a keyword makes it *weaker*.
  Several italic islands in one paragraph make the page look busy.
- General CV: none in the body. The page already has one italic line (availability), and that's
  the right amount.

**A different font.**
- Don't use one inside running text. A word in another typeface mid-sentence looks like a
  copy-paste error to HR, not a design choice. Monospace for tech names makes the line look
  like a README.
- The only legitimate use is a deliberate pairing at the *structure* level: one font for the
  name and section headings, another for the body. That's a whole-CV design decision. It needs
  Roy's approval and a full render check, and is never done per phrase.

Rules that come out of the scale:
- **Something that's already loud doesn't get louder.** Headings, job titles and the military
  labels ("Leadership:") are already bold, so nothing next to them goes higher than soft.
  Don't stack emphasis on a link either.
- **Links must look clickable.** Use the underline as well as the color. Without it, bold blue
  project names read as headings (Roy, 2026-11-26).
- **Emphasize the shortest phrase that carries the fact.** A number goes together with its noun
  ("1,500+ page views", not "1,500+"). Never emphasize a whole sentence. One exception is the
  skills stack line, where the whole line is the keyword list.
- **Soft is free, strong costs width.** Bold is wider. After every strong emphasis, re-check
  that no line now ends with a single word on a new line ("browser.", "simulator."). If one
  does, drop to soft or drop the emphasis. Never change words to make it fit.
- **Restraint is the point.** If everything stands out, nothing does. When unsure, go one
  level lower.

## 2. Critique every candidate, then decide

For each candidate phrase, write one line in this format:

`phrase -> level | why (what it signals to *this* reader) | critique (risk) | how (exact words, level)`

Questions for the critique:
1. **Signal:** does it answer what this posting screens for (role match, stack keyword, scale,
   proof of real users, availability)? If it doesn't, leave it at body.
2. **Proof or claim:** a number or outcome can go up to strong. An adjective or keyword stays soft.
3. **Risk:** can the emphasis hurt? Example: making "400+ reserve-duty days" strong can read
   as "often unavailable", so it stays soft.
4. **Competition:** does it fight a heading, a link or another emphasis in the same line or
   entry? If so, lower one of them.
5. **Width:** if it's strong, did a line break move?

Only after the critique do you decide **yes at which level** and **exactly which words**.

## 3. Tailoring per role

The role decides the levels. Run the critique again against the posting's requirements and
`## Keywords` in the application file:
- Data or neuro roles: "MEG study" and the neuro project can go to strong, and the web-app
  numbers drop to soft.
- AI-agent roles: "its own MCP server", "agentic AI", "guardrails" go to soft-to-strong.
- Systems or C++ roles: the Wolt Clone C++ engine and "C/C++" in the stack get soft; the AI
  keywords drop to body.
- `tailor_cv.py` replaces the summary's focus line, so the General phrase
  "AI & Full-Stack developer" may not exist. Choose the strong phrase from the new focus line.

Write the decisions to `cv_emphasis/<Variant>.json` (no personal data, so it's safe for this
public repo):

```json
[
  {"phrase": "1,500+ page views", "level": "strong", "grow": 1,
   "why": "only real-user proof on the page; critique: next to a soft phrase, no conflict"}
]
```

Then run:

```
python3 scripts/style_cv.py <tailored .docx> <out .docx> cv_emphasis/<Variant>.json
```

Copy the decisions table (phrase / level / why) into the role's submission package, so Roy
can see why each phrase was chosen.

## 4. Check before sending

1. Extract the text from the PDF and compare it with the unstyled version. It must be identical.
   For Hebrew, strip whitespace and bidi control marks (U+200E/F, U+202A-202E) before comparing:
   pdftotext inserts them wherever a line break lands, so a moved break looks like a text change.
2. The PDF is exactly one page, and has the same line count as the unstyled version.
3. Every link annotation is still there.
4. Look at the rendered page: once at full page ("what does the eye catch in 6 seconds?") and
   once zoomed in, to see the soft level is visible but quiet.

## General CV decisions (2026-11-26)

Hebrew General CV: the same choices, in `cv_emphasis/General_HE.json`. Run
`python3 scripts/style_cv.py <Roy_Carmelli_CV_HE.docx> <out> cv_emphasis/General_HE.json`.

| Phrase | Level | Why / critique |
|---|---|---|
| Available 2-3 days a week | soft | HR filters student roles on availability first. It's in italic; bold + italic looked odd, so soft. |
| honors program | soft | A differentiator but not a fact to leave with. Strong would compete with the first line. |
| AI & Full-Stack developer | strong | Role identity - what HR matches to the job title. |
| LLM apps and agents | soft | Keyword match; it's in the same line as the strong phrase, so not strong. |
| guardrails | soft | Signals production-minded AI work. The list after it is the proof, so only one word. |
| Native English and Hebrew | soft | Matters to companies with English-speaking clients or teams. |
| MEG study | soft | The research signal of the dual degree. Goes to strong for neuro or data roles. |
| all live or open source | soft | Tells the reader the links are worth clicking, without competing with the project names. |
| Promoted by the department | soft | Supports the number that follows. Strong would compete with it. |
| 1,500+ page views | strong +0.5pt | The only real-user number on the page. The size bump puts it one step above the other strong phrases. |
| its own MCP server | soft | A strong AI-tooling keyword. |
| agentic AI | soft | Keyword; the rest of the line is description. |
| 225 problems | soft | Gives the project scale. Without it, it reads as "another site". |
| 400+ reserve-duty days | soft | Shows commitment. Strong could read as "unavailable". |
| mass-casualty events | soft | Context for decisions under pressure. The label next to it is already bold. |
| 12 to 30+ people | strong +0.5pt | Leadership scale as a number. The size bump lets it stand out from the bold "Leadership:" label next to it. |
| Skills stack line | soft | The keyword list HR matches against; the whole line on purpose. |
| Wolt Clone, Aside text | none | The project names already stand out, and there's no number worth lifting. |
