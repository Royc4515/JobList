#!/usr/bin/env python3
"""Visual pass on Roy's English base CV: same words, same structure, easier to scan.

Approved request 2026-11-26: links must stand out from the body text (the old link
navy 1F4E79 was almost the same as the grey 434343 body), the portfolio link most of
all, and the facts an HR screener should catch must be visible at a glance.

What it changes (formatting only):
- every hyperlink: bright blue LINK, underlined; project names also bold.
- the portfolio link (contact line + "more on my portfolio"): bold, light-blue
  highlight; on the contact line one size up.
- EMPHASIS phrases: bold, near-black INK, so numbers and keywords pop out of the grey.
- "Available 2-3 days a week" line: the day count bold.

Usage:
    python3 scripts/style_cv.py <base .docx> <output .docx>

The output contains personal details - never commit it (this repo is public).
"""
import copy
import sys

import docx
from docx.oxml.ns import qn

LINK = "0B5FD6"
INK = "111111"
HIGHLIGHT = "DCEBFF"
PORTFOLIO = "roy-carmelli-portfolio"

# Phrases to bold, in reading order. Each must appear verbatim in a plain (non-link) run.
EMPHASIS = [
    "2-3 days a week",
    "3rd-year B.Sc.", "honors program",
    "AI & Full-Stack developer", "LLM apps and agents",
    "guardrails",
    "led people and projects",
    "teaching, tutoring and professional training",
    "Native English and Hebrew",
    "MEG study",
    "all live or open source",
    "Promoted by the department", "1,500+ page views",
    "its own MCP server",
    "agentic AI sommelier",
    "225 problems",
    "team of 2", "React Native",
    "400+ reserve-duty days",
    "mass-casualty events",
    "12 to 30+ people",
    "Claude Code, AI agents, MCP and LLM APIs",
    "Anthropic certificates",
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


def style_link(r, bold=False, highlight=False, size=None):
    rpr = r.find(qn("w:rPr"))
    set_prop(rpr, "w:color", LINK)
    set_prop(rpr, "w:u", "single")
    if bold:
        set_prop(rpr, "w:b", "1")
        set_prop(rpr, "w:bCs", "1")
    if highlight:
        shd = rpr.find(qn("w:shd"))
        if shd is None:
            shd = rpr.makeelement(qn("w:shd"), {})
            rpr.append(shd)
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), HIGHLIGHT)
    if size:
        set_prop(rpr, "w:sz", size)
        set_prop(rpr, "w:szCs", size)


def emphasize(d, phrase):
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
            set_prop(mrpr, "w:b", "1")
            set_prop(mrpr, "w:bCs", "1")
            set_prop(mrpr, "w:color", INK)
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
                style_link(r, bold=portfolio or project, highlight=portfolio,
                           size="21" if portfolio and i < 3 else None)
    for phrase in EMPHASIS:
        emphasize(d, phrase)
    d.save(sys.argv[2])
    print("wrote", sys.argv[2])


if __name__ == "__main__":
    main()
