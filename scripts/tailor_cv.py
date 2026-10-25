#!/usr/bin/env python3
"""Build Roy's tailored CV versions (one per entry in VARIANTS) from his base CV (.docx).

Base CV: `Roy_Carmelli_CV.docx` (Drive, October 2026 - honors program, reserve duty,
military service, Anthropic certificates; the Nechita Raka project line and the 2028
graduation year were added on 2026-10-12; on 2026-10-22, after a recruiter's
review, the summary became bullets, a "Seeking..." line moved to the top, PROJECTS got its own
section, the tech stack moved to SKILLS and the degree reads "2024 - present"). Until 2026-10-11 the base was
`Roy_Carmelli_CV_sep2026.docx`; packages submitted before then used that one.

What changes per version (everything else is copied from the base file as-is):
- the second summary line ("AI & Full-Stack developer ...") becomes the role's focus line;
- optionally a GPA + coursework line under the reserve-duty line (only where a posting
  asks for grades or the coursework is the point);
- optionally the neuro-data project line after the other projects (data roles).
The graduation year is always set to 2028 (Roy finishes in February 2028).

Usage:
    pip install python-docx
    python3 scripts/tailor_cv.py <path to Roy_Carmelli_CV.docx> <output dir>

Then export each .docx to PDF (Word or LibreOffice) and check it is one page.
The output contains personal details - never commit it (this repo is public).
"""
import copy
import sys
from pathlib import Path

import docx

GPA = "GPA 85.09"
COURSES = {
    "PDP": "Python Data Processing (98)",
    "DS": "Data Structures (93)",
    "OOP": "OOP in Java (92)",
    "LA": "Linear Algebra (97)",
    "CALC": "Calculus (100)",
    "NEURO": "Neuroscience (94)",
    "ASP": "Advanced Systems Programming (C++/Node.js)",
    "ARCH": "Computer Architecture (C/Assembly)",
}
NEURO_PROJECT = "Cognitive Background: OpenNeuro logs cleaned for regression (Pandas, NumPy), team of 4."

# focus: replaces the "AI & Full-Stack developer ..." summary line - keep it to one line.
# courses: list of COURSES keys -> adds a GPA + coursework line. neuro: adds the project.
# Each added line must stay one line: with neuro, use at most two courses, or the CV spills.
VARIANTS = {
    "General": {"focus": None},
    "Google": {"grad": True, "focus": "Software developer focused on AI systems and backend, building LLM agents "
                        "in Python.",
               "courses": ["DS", "PDP"]},
    "Marvell": {"focus": "Developer focused on data and AI infrastructure, turning raw data into "
                         "model-ready datasets.",
                "courses": ["PDP", "DS"], "neuro": True},
    "FIL": {"focus": "Backend developer building APIs and services for real systems with Node.js, "
                     "Python and C++."},
    "OptimumEDA": {"focus": "Python developer focused on automation: scripts and tools that take "
                            "repetitive work off people's hands."},
    "AmazonMLIL": {"grad": True, "focus": "Python developer focused on ML infrastructure and automation, building "
                            "tools with AI coding agents.",
                   "courses": ["PDP", "DS", "ARCH"]},
    "Claroty": {"focus": "Software developer, Python and AI tooling first, building agents and tools "
                         "that work end to end."},
    "F5": {"focus": "Python and backend/web developer interested in web application security, "
                    "building tools over many APIs."},
    "IAI_AI": {"focus": "AI developer working in Python on AI algorithms and the software around "
                        "them; taking Machine Learning this semester.",
               "courses": ["PDP", "LA"], "neuro": True},
    "IAI_SW": {"focus": "C/C++ and Python developer interested in real-time and signal-processing "
                        "systems.",
               "courses": ["ARCH", "DS"], "neuro": True},
    "Apple": {"focus": "Developer interested in low-level software: C/C++, Python and the layer "
                       "between hardware and software.",
              "courses": ["ARCH", "ASP", "DS"]},
    "GrowthSpace": {"focus": "AI agent builder: prompting, agent behaviour and conversation quality, "
                             "using Claude and other models every day."},
    "Upstream": {"focus": "Python developer focused on data analysis with Pandas, turning raw "
                          "real-world data into findings.",
                 "courses": ["PDP", "LA"], "neuro": True},
    "Rafael_AI": {"focus": "AI developer integrating LLM APIs (Claude, OpenAI, Gemini) into tools "
                           "with React UIs."},
    "ChargeAfter": {"focus": "Full-stack developer building React, Node.js and MongoDB apps, with AI "
                             "integrations."},
    "Mobileye_Calib": {"grad": True, "focus": "C++ and Python developer with ML basics, coding daily with Claude "
                                "Code.",
                       "courses": ["LA", "CALC"], "neuro": True},
    "Samsung": {"focus": "Python and C++ developer building tools and automation with Claude "
                         "Code."},
    "Marvell_Validation": {"focus": "Python and C++ developer focused on automation, coding daily with AI "
                                    "tools.",
                           "courses": ["ARCH", "ASP"]},
    "Google_Research": {"grad": True, "focus": "Building LLM agents and data pipelines, interested in research where ML "
                                 "meets cognition.",
                        "courses": ["LA", "PDP"], "neuro": True},
    "AIWeb": {"focus": "AI web developer building React/TypeScript products end to end with Claude "
                       "Code."},
    "AmazonHaifa": {"grad": True, "focus": "Developer interested in systems software: C, low-level code and the "
                             "layer between hardware and software.",
                    "courses": ["ARCH", "ASP", "DS"]},
    "Artlist": {"focus": "Full-stack developer building React and Node.js apps, coding daily with "
                         "Claude Code."},
    "Mobileye_Data": {"grad": True, "focus": "Python developer focused on data analysis, turning large raw datasets "
                               "into clear reports.",
                      "courses": ["PDP", "LA"], "neuro": True},
}


def find(paragraphs, needle):
    for p in paragraphs:
        if needle in p.text:
            return p
    raise SystemExit(f"Base CV changed: could not find {needle!r}")


def set_text(p, text):
    p.runs[0].text = text
    for r in p.runs[1:]:
        r.text = ""


def insert_after(anchor, template, text):
    """New paragraph after `anchor`, formatted like `template` (a plain one-run line)."""
    el = copy.deepcopy(template._p)
    anchor._p.addnext(el)
    p = docx.text.paragraph.Paragraph(el, anchor._parent)
    set_text(p, text)
    return p


def build(base, spec):
    d = docx.Document(base)
    P = d.paragraphs
    if spec.get("focus"):
        set_text(find(P, "AI & Full-Stack developer"), "• " + spec["focus"])
    if spec.get("grad"):  # postings that ask for the graduation date (Google, Amazon, Mobileye)
        rd = find(P, "reserve duty")
        rd.runs[-1].text = rd.runs[-1].text.rstrip() + " · Expected graduation: Feb 2028"
    plain = find(P, "Native English and Hebrew")  # a one-run, non-bold body line
    # Each added line costs one: drop the least job-relevant summary lines to stay on one page.
    extra = bool(spec.get("courses")) + bool(spec.get("neuro"))
    for needle in ["Experienced in teaching", "Excellent interpersonal skills"][:extra]:
        p = find(P, needle)
        p._p.getparent().remove(p._p)
    if spec.get("courses"):
        line = f"{GPA} · Relevant coursework: " + " · ".join(COURSES[c] for c in spec["courses"]) + "."
        insert_after(find(P, "reserve duty"), plain, line)
    if spec.get("neuro"):
        insert_after(find(P, "Wolt Clone"), plain, NEURO_PROJECT)
    return d


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    base, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for name, spec in VARIANTS.items():
        path = out / f"Roy_Carmelli_CV_{name}.docx"
        build(base, spec).save(path)
        print("wrote", path)


if __name__ == "__main__":
    main()
