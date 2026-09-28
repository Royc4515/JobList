#!/usr/bin/env python3
"""Regenerate the README.md dashboard from applications/*.md.

Stdlib only (no PyYAML). Frontmatter is a flat `key: value` block between
`---` fences. The dashboard is written between the DASHBOARD markers in
README.md so any hand-written intro text above them is preserved.

Usage:  python scripts/build_dashboard.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPS_DIR = ROOT / "applications"
LEADS_DIR = ROOT / "leads"
README = ROOT / "README.md"

START = "<!-- DASHBOARD:START -->"
END = "<!-- DASHBOARD:END -->"

# Canonical application status order + display labels
STATUS_ORDER = ["offer", "interview", "in-review", "submitted", "not-submitted", "rejected"]
STATUS_LABEL = {
    "offer": "🎉 Offer",
    "interview": "💬 Interview",
    "in-review": "🔎 In review",
    "submitted": "📤 Submitted",
    "not-submitted": "📝 Not submitted",
    "rejected": "❌ Rejected",
}

# Fit-score sub-keys, rubric in PROFILE.md. The total is derived here and never
# stored in frontmatter, so it cannot drift from its parts.
FIT_KEYS = ("fit_role", "fit_stack", "fit_gates", "fit_path")
FIT_SHORT = {"fit_role": "role", "fit_stack": "stack", "fit_gates": "gates", "fit_path": "path"}
FIT_MAX = 10

# Networking-lead status order + display labels
LEAD_STATUS_ORDER = ["responded", "referred", "intro-requested", "contacted", "to-contact", "dead"]
LEAD_STATUS_LABEL = {
    "responded": "🟢 Responded",
    "referred": "✅ Referred",
    "intro-requested": "🤝 Intro requested",
    "contacted": "📨 Contacted",
    "to-contact": "🔵 To contact",
    "dead": "⚫ Dead",
}


def parse_frontmatter(text):
    """Return a dict from a flat `key: value` frontmatter block."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data


def parse_fit(app):
    """Return (total, parts, gated) for a fully scored app, else None.

    Also returns a warning string (or None) so a half-filled or malformed score
    is reported loudly instead of silently ranking the role as if it scored 0.
    """
    parts = {}
    for key in FIT_KEYS:
        # Strip inline `# comment`s: the template documents keys that way, and a
        # copied-but-unedited template line must not break int parsing.
        raw = app.get(key, "").split("#", 1)[0].strip()
        if raw == "":
            continue
        try:
            value = int(raw)
        except ValueError:
            return None, f"{app['_file']}: {key}={raw!r} is not an integer - score ignored"
        if not 0 <= value <= FIT_MAX:
            return None, f"{app['_file']}: {key}={value} outside 0-{FIT_MAX} - score ignored"
        parts[key] = value

    if not parts:
        return None, None  # unscored is a normal state, not an error
    if len(parts) < len(FIT_KEYS):
        missing = ", ".join(k for k in FIT_KEYS if k not in parts)
        return None, f"{app['_file']}: partial fit score, missing {missing} - score ignored"

    # don't touch / gates == 0 is the disqualification signal defined in
    # PROFILE.md. It must override the sum: a role failing studies-remaining
    # with 9s elsewhere would otherwise outrank a genuinely viable role.
    gated = parts["fit_gates"] == 0
    return (sum(parts.values()), parts, gated), None


def fmt_parts(parts):
    return " · ".join(f"{FIT_SHORT[k]} {parts[k]}" for k in FIT_KEYS)


def build_queue(apps):
    """Ranked 'Next to submit' section for not-submitted roles."""
    pending = [a for a in apps if a.get("status") == "not-submitted"]
    if not pending:
        return []

    ranked, gated, unscored = [], [], []
    for a in pending:
        fit = a.get("_fit")
        if fit is None:
            unscored.append(a)
        elif fit[2]:
            gated.append(a)
        else:
            ranked.append(a)

    # Ties break on path, then role: between equal totals, the one with a human
    # route in is the one that actually gets an interview.
    ranked.sort(
        key=lambda a: (a["_fit"][0], a["_fit"][1]["fit_path"], a["_fit"][1]["fit_role"]),
        reverse=True,
    )

    def line(a, prefix):
        role = a.get("role", "")
        role_txt = f" — {role}" if role else ""
        note = a.get("fit_note", "").strip()
        note_txt = f" — {note}" if note else ""
        return (
            f"{prefix}[{esc(a.get('company'))}{role_txt}]({a['_file']}) "
            f"· {fmt_parts(a['_fit'][1])}{note_txt}"
        )

    out = ["## Next to submit", ""]
    out.append(
        f"Not-submitted roles ranked by fit score out of {FIT_MAX * len(FIT_KEYS)} "
        "(rubric in [`PROFILE.md`](PROFILE.md))."
    )
    out.append("")
    for i, a in enumerate(ranked, 1):
        out.append(line(a, f"{i}. **{a['_fit'][0]}** "))
    if gated:
        out.append("")
        out.append(f"**Gated out ({len(gated)})** - a hard gate failed; close or drop:")
        for a in sorted(gated, key=lambda x: x.get("company", "").lower()):
            out.append(line(a, "- "))
    if unscored:
        out.append("")
        out.append(f"**Unscored ({len(unscored)})** - run fit-reviewer:")
        for a in sorted(unscored, key=lambda x: x.get("company", "").lower()):
            role = a.get("role", "")
            role_txt = f" — {role}" if role else ""
            out.append(f"- [{esc(a.get('company'))}{role_txt}]({a['_file']})")
    out.append("")
    return out


def load_apps():
    apps = []
    for path in sorted(APPS_DIR.glob("*.md")):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        fm["_file"] = f"applications/{path.name}"
        fm.setdefault("status", "not-submitted")
        apps.append(fm)
    return apps


def load_leads():
    leads = []
    if not LEADS_DIR.is_dir():
        return leads
    for path in sorted(LEADS_DIR.glob("*.md")):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        fm["_file"] = f"leads/{path.name}"
        fm.setdefault("status", "to-contact")
        leads.append(fm)
    return leads


def esc(value):
    return (value or "").replace("|", "\\|").strip() or "—"


def build_dashboard(apps, leads):
    total = len(apps)
    counts = {s: 0 for s in STATUS_ORDER}
    for a in apps:
        counts[a.get("status", "not-submitted")] = counts.get(a.get("status"), 0) + 1

    out = [START, ""]

    # Stats line
    stats = " · ".join(
        f"**{counts[s]}** {STATUS_LABEL[s].split(' ', 1)[1]}"
        for s in STATUS_ORDER
        if counts.get(s)
    )
    out.append(f"**{total} applications** — {stats}")
    out.append("")

    # Ranked queue goes first: "what do I submit next" is the question the
    # dashboard exists to answer, and the pipeline below only says what exists.
    out.extend(build_queue(apps))

    # Pipeline grouped by status
    out.append("## Pipeline")
    out.append("")
    for s in STATUS_ORDER:
        group = [a for a in apps if a.get("status") == s]
        if not group:
            continue
        out.append(f"### {STATUS_LABEL[s]} ({len(group)})")
        for a in sorted(group, key=lambda x: x.get("company", "").lower()):
            role = a.get("role", "")
            role_txt = f" — {role}" if role else ""
            out.append(f"- [{esc(a.get('company'))}{role_txt}]({a['_file']})")
        out.append("")

    # Index table
    out.append("## All applications")
    out.append("")
    out.append("| Company | Role | Status | Fit | Applied | Follow-up |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for a in sorted(
        apps, key=lambda x: (x.get("applied", "") == "", x.get("applied", "")), reverse=True
    ):
        fit = a.get("_fit")
        if fit is None:
            fit_txt = "—"
        elif fit[2]:
            fit_txt = "gated"
        else:
            fit_txt = str(fit[0])
        out.append(
            "| [{company}]({file}) | {role} | {status} | {fit} | {applied} | {follow} |".format(
                company=esc(a.get("company")),
                file=a["_file"],
                role=esc(a.get("role")),
                status=STATUS_LABEL.get(a.get("status"), a.get("status", "")),
                fit=fit_txt,
                applied=esc(a.get("applied")),
                follow=esc(a.get("follow_up")),
            )
        )
    out.append("")

    # Networking leads (only rendered when leads/ has entries)
    if leads:
        lc = {s: sum(1 for x in leads if x.get("status") == s) for s in LEAD_STATUS_ORDER}
        lead_stats = " · ".join(
            f"**{lc[s]}** {LEAD_STATUS_LABEL[s].split(' ', 1)[1]}"
            for s in LEAD_STATUS_ORDER
            if lc.get(s)
        )
        out.append("## Networking leads")
        out.append("")
        out.append(f"**{len(leads)} leads** — {lead_stats}")
        out.append("")
        out.append("| Company | Contact | Connection | Target role | Status | Follow-up |")
        out.append("| --- | --- | --- | --- | --- | --- |")
        order = {s: i for i, s in enumerate(LEAD_STATUS_ORDER)}
        for lead in sorted(leads, key=lambda x: order.get(x.get("status"), 99)):
            out.append(
                "| [{company}]({file}) | {contact} | {conn} | {role} | {status} | {follow} |".format(
                    company=esc(lead.get("company")),
                    file=lead["_file"],
                    contact=esc(lead.get("contact")),
                    conn=esc(lead.get("connection_type")),
                    role=esc(lead.get("target_role")),
                    status=LEAD_STATUS_LABEL.get(lead.get("status"), lead.get("status", "")),
                    follow=esc(lead.get("follow_up")),
                )
            )
        out.append("")

    out.append(END)
    return "\n".join(out)


def main():
    apps = load_apps()
    warnings = []
    for a in apps:
        a["_fit"], warn = parse_fit(a)
        if warn:
            warnings.append(warn)
    leads = load_leads()
    dashboard = build_dashboard(apps, leads)

    intro = (
        "# JobList — Job Search Tracker\n\n"
        "My job-application pipeline. Each role lives in "
        "[`applications/`](applications/) as its own Markdown file, and each "
        "networking lead in [`leads/`](leads/) (people who work at a target "
        "company or can make a warm intro). To add one, copy the matching "
        "template from [`templates/`](templates/), fill it in, then run:\n\n"
        "```bash\npython scripts/build_dashboard.py\n```\n\n"
        "The dashboard below is auto-generated — edit the files, not this block.\n\n"
    )

    if README.exists():
        text = README.read_text(encoding="utf-8")
        if START in text and END in text:
            head = text.split(START)[0].rstrip() + "\n\n"
            new_text = head + dashboard + "\n"
        else:
            new_text = intro + dashboard + "\n"
    else:
        new_text = intro + dashboard + "\n"

    README.write_text(new_text, encoding="utf-8")
    print(
        f"Dashboard updated: {len(apps)} applications, {len(leads)} leads "
        f"written to {README}"
    )
    # Printed after the success line so the daily automation's log shows them
    # last, where a human skimming it will actually see them.
    for w in warnings:
        print(f"WARNING: {w}")


if __name__ == "__main__":
    main()
