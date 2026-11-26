#!/usr/bin/env python3
"""Visual pass on Roy's English base CV: same words, same structure, easier to scan.

Approved request 2026-11-26: links must stand out from the body text (the old link
navy 1F4E79 was almost the same as the grey 434343 body), the portfolio link most of
all, and the facts an HR screener should catch must be visible at a glance.

What it changes (formatting only). Emphasis is a scale, not on/off - the body is grey
434343, and each level is one step louder than the last:
- "soft": the same weight, a darker ink (SOFT_INK). Noticed on a skim, never shouts.
  Keywords that match job ads or back a claim.
- "strong": bold in a slightly softened black (STRONG_INK). Only the few hard facts
  a screener should leave with (role identity, real-user numbers, leadership scale).
- links: bright blue LINK. Project names are bold and not underlined (they head
  each entry; the blue says "link"). Inline links (email, LinkedIn, GitHub,
  certificates) keep a regular weight with an underline. The portfolio - the one
  link Roy wants clicked - is bold + underlined, half a point larger on the contact line.

Usage:
    python3 scripts/style_cv.py <base .docx> <output .docx>

The output contains personal details - never commit it (this repo is public).
"""
import copy
import sys

import docx
from docx.oxml.ns import qn

LINK = "1A5FC8"
SOFT_INK = "161616"
STRONG_INK = "262626"
PORTFOLIO = "roy-carmelli-portfolio"

# (phrase, level) in reading order. Each must appear verbatim in a plain (non-link) run.
EMPHASIS = [
    ("honors program", "soft"),
    ("AI & Full-Stack developer", "strong"),
    ("LLM apps and agents", "soft"),
    ("all live or open source", "soft"),
    ("Promoted by the department", "soft"),
    ("1,500+ page views", "strong"),
    ("its own MCP server", "soft"),
    ("225 problems", "soft"),
    ("400+ reserve-duty days", "soft"),
    ("mass-casualty events", "soft"),
    ("12 to 30+ people", "strong"),
]

WOLT_OLD = ", a food-delivery app built by a team of 2 in a systems course. My part:"
WOLT_NEW = (", a full food-delivery app built by a team of 2 in a systems course, growing from "
            "a C++ recommendation engine into React web and React Native apps on a Node.js and "
            "MongoDB backend.")


def set_prop(rpr, tag, val):
    el = rpr.find(qn(tag))
    if el is None:
        el = rpr.makeelement(qn(tag), {})
        rpr.append(el)
    el.set(qn("w:val"), val)
    return el


def style_link(r, bold=False, underline=True, size=None):
    rpr = r.find(qn("w:rPr"))
    set_prop(rpr, "w:color", LINK)
    set_prop(rpr, "w:u", "single" if underline else "none")
    if bold:
        set_prop(rpr, "w:b", "1")
        set_prop(rpr, "w:bCs", "1")
    if size:
        set_prop(rpr, "w:sz", size)
        set_prop(rpr, "w:szCs", size)


def emphasize(d, phrase, level):
    for p in d.paragraphs:
        for r in p._p.findall(qn("w:r")):
            t = r.find(qn("w:t"))
            if t is None or not t.text or phrase not in t.text:
                continue
            before, after = t.text.split(phrase, 1)
            mid = copy.deepcopy(r)
            mt = mid.find(qn("w:t"))
            mt.text = phrase
            mt.set(qn("xml:space"), "preserve")
            mrpr = mid.find(qn("w:rPr"))
            if level == "strong":
                set_prop(mrpr, "w:b", "1")
                set_prop(mrpr, "w:bCs", "1")
            set_prop(mrpr, "w:color", STRONG_INK if level == "strong" else SOFT_INK)
            tail = copy.deepcopy(r)
            tail.find(qn("w:t")).text = after
            tail.find(qn("w:t")).set(qn("xml:space"), "preserve")
            t.text = before
            t.set(qn("xml:space"), "preserve")
            r.addnext(mid)
            mid.addnext(tail)
            return
    raise SystemExit(f"CV text changed: could not find {phrase!r}")


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    d = docx.Document(sys.argv[1])
    for p in d.paragraphs:
        for r in p._p.findall(qn("w:r")):
            t = r.find(qn("w:t"))
            if t is not None and t.text.startswith(WOLT_OLD):
                t.text = WOLT_NEW
    for i, p in enumerate(d.paragraphs):
        for h in p._p.findall(qn("w:hyperlink")):
            text = "".join(x.text or "" for x in h.iter(qn("w:t")))
            portfolio = PORTFOLIO in text or text == "portfolio"
            project = h is p._p.find(qn("w:hyperlink")) and p._p.index(h) <= 1 and i > 3 \
                and "Claude" not in text
            for r in h.findall(qn("w:r")):
                style_link(r, bold=portfolio or project, underline=not project,
                           size="20" if portfolio and i < 3 else None)
    for phrase, level in EMPHASIS:
        emphasize(d, phrase, level)
    d.save(sys.argv[2])
    print("wrote", sys.argv[2])


if __name__ == "__main__":
    main()
