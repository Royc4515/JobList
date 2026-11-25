#!/usr/bin/env python3
"""Rebuild Roy's current base CV from the October 2026 base on Drive.

The Drive file `Roy_Carmelli_CV.docx` (2026-10-12) is the last version Roy uploaded. Every
change approved since then is applied here, in order, so the current base can be rebuilt
after a container reset instead of living only in a scratch folder:

1. 2026-10-22 recruiter notes: "Central Israel" on the contact line, the "Seeking..." line
   moved under it, summary as bullets, degree "2024 - present", a PROJECTS section, and the
   tech stack moved to the top of SKILLS.
2. 2026-11-03 Nechita Raka described as a multi-faculty hub, CS / Neuroscience linked.
3. 2026-11-08 tighter layout (body 11.5pt, no gap above the name), the military section and
   project details from the Amazon SDE CV, CareerPredict AI added.

Usage:
    python3 scripts/build_base_cv.py <Drive Roy_Carmelli_CV.docx> <output .docx>

Then feed the output to scripts/tailor_cv.py. The output contains personal details - never
commit it (this repo is public).
"""
import copy
import sys

import docx
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Pt

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

MILITARY = [
    "Regular service 2021 - Aug 2024, reservist since (400+ days of reserve duty alongside "
    "full-time studies).",
    "• Decision-making under pressure: led the medical response in mass-casualty events, in "
    "the field and in the division war room, making fast triage and evacuation calls.",
    "• Leadership: led a medical unit that grew from 12 to 30+ people during high-intensity "
    "operations, running a regional clinic and several teams in parallel.",
    "• Coordination: ran real-time medical coordination and logistics across units from the "
    "division war room.",
    "• Training: trained medics and combat soldiers to give medical care in the field.",
]
CS_SITE = "https://nechita-raka.vercel.app/"
NEURO_SITE = "https://nechita-raka-neuro.vercel.app/"
CAREER_SITE = "https://career-predictor-cnvg.onrender.com"


def find(d, needle):
    for p in d.paragraphs:
        if needle in p.text:
            return p
    raise SystemExit(f"Base CV changed: could not find {needle!r}")


def set_text(p, text):
    p.runs[0].text = text
    for r in p.runs[1:]:
        r.text = ""


def tail_run(p, needle):
    for r in p.runs:
        if needle in r.text:
            return r
    raise SystemExit(f"Base CV changed: no run with {needle!r}")


def new_link(p, template, text, url):
    """A copy of the hyperlink `template` with new text and target, not bold."""
    h = copy.deepcopy(template)
    h.set(qn("r:id"), p.part.relate_to(url, RT.HYPERLINK, is_external=True))
    runs = h.findall(qn("w:r"))
    for r in runs[1:]:
        h.remove(r)
    runs[0].find(qn("w:t")).text = text
    for b in list(runs[0].iter(qn("w:b"))):
        b.getparent().remove(b)
    return h


def plain_run(template_run, text):
    r = copy.deepcopy(template_run._r)
    t = r.find(qn("w:t"))
    t.text = text
    t.set(qn("xml:space"), "preserve")
    return r


def recruiter_notes(d):
    contact = find(d, "roy.y.carmelli@gmail.com")
    phone = tail_run(contact, "+972")
    phone.text = phone.text.rstrip() + " · Central Israel"
    seek = find(d, "Seeking a position")
    trailing = seek._p.getprevious()
    contact._p.addnext(seek._p)
    seek.paragraph_format.space_before = Pt(4)
    if trailing is not None and not "".join(trailing.itertext()).strip():
        trailing.getparent().remove(trailing)
    for needle in ["3rd-year B.Sc.", "AI & Full-Stack developer", "Develops software systems",
                   "Excellent interpersonal", "Experienced in teaching", "Native English"]:
        p = find(d, needle)
        p.runs[0].text = "• " + p.runs[0].text
    degree = find(d, "2024 - 2028 (expected)")
    for r in degree.runs:
        r.text = r.text.replace("2024 - 2028 (expected)", "2024 - present")
    builds = find(d, "Builds projects that use")
    heading = find(d, "MILITARY SERVICE")
    spacer = heading._p.getprevious()
    builds._p.addprevious(copy.deepcopy(spacer))
    new_heading = copy.deepcopy(heading._p)
    builds._p.addprevious(new_heading)
    docx.text.paragraph.Paragraph(new_heading, builds._parent).runs[0].text = "PROJECTS"
    for r in docx.text.paragraph.Paragraph(new_heading, builds._parent).runs[1:]:
        r.text = ""
    stack = find(d, "Python, JavaScript, TypeScript, React")
    find(d, "Hands-on with Claude Code")._p.addprevious(stack._p)


def projects(d):
    nechita = find(d, "Nechita Raka")
    hl = nechita._p.find(qn("w:hyperlink"))
    tail = tail_run(nechita, "first-year")
    tail.text = ", a multi-faculty student hub ("
    el = tail._r
    for node in [new_link(nechita, hl, "CS", CS_SITE), plain_run(tail, ", "),
                 new_link(nechita, hl, "Neuroscience", NEURO_SITE),
                 plain_run(tail, ") with a RAG chatbot, 1,300+ visits.")]:
        el.addnext(node)
        el = node
    tail_run(find(d, "Aside"), "Chrome extension").text = (
        ", a Chrome AI sidebar extension: 6 LLM providers behind a base class and factory.")
    sommelier = find(d, "Sommelier Bot")
    tail_run(sommelier, "Telegram").text = (
        ", a Telegram AI agent for a wine cellar: label photos, voice notes, 4-model fallback.")
    wolt = find(d, "Wolt Clone")
    el = copy.deepcopy(sommelier._p)
    wolt._p.addprevious(el)
    career = docx.text.paragraph.Paragraph(el, wolt._parent)
    h = el.find(qn("w:hyperlink"))
    h.set(qn("r:id"), career.part.relate_to(CAREER_SITE, RT.HYPERLINK, is_external=True))
    texts = list(h.iter(qn("w:t")))
    texts[0].text = "CareerPredict AI"
    for t in texts[1:]:
        t.text = ""
    career.runs[-1].text = (", a parody quiz app with AI-generated magazine covers "
                            "(React, Node/Express, OAuth).")
    for r in career.runs[:-1]:
        r.text = ""


def military(d):
    first = find(d, "Managed several small teams")
    second = find(d, "Led the medical response")
    set_text(first, MILITARY[0])
    prev = first
    for text in MILITARY[1:]:
        el = copy.deepcopy(first._p)
        prev._p.addnext(el)
        prev = docx.text.paragraph.Paragraph(el, first._parent)
        set_text(prev, text)
    second._p.getparent().remove(second._p)


def tighter_layout(d):
    # Half-points: body 13 -> 11.5, section headings 13.5 -> 12.5, job titles 14 -> 13,
    # the seeking line 12 -> 11.5 (the same as the Amazon SDE CV's density).
    # Paragraph marks (the size of empty spacer lines) only lost the half point, as in the
    # version Roy approved.
    remap = {"26": "23", "27": "25", "28": "26", "24": "23"}
    for tag in ("sz", "szCs"):
        for sz in d.element.body.iter(W + tag):
            v = sz.get(W + "val")
            mark = sz.getparent().getparent().tag == W + "pPr"
            if v == "24" or (v in remap and not mark):
                sz.set(W + "val", remap[v])
    d.paragraphs[0].paragraph_format.space_before = Pt(0)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    d = docx.Document(sys.argv[1])
    recruiter_notes(d)
    projects(d)
    military(d)
    tighter_layout(d)
    d.save(sys.argv[2])
    print("wrote", sys.argv[2])


if __name__ == "__main__":
    main()
