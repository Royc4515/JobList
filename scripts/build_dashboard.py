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
    out.append("| Company | Role | Status | Applied | Follow-up |")
    out.append("| --- | --- | --- | --- | --- |")
    for a in sorted(
        apps, key=lambda x: (x.get("applied", "") == "", x.get("applied", "")), reverse=True
    ):
        out.append(
            "| [{company}]({file}) | {role} | {status} | {applied} | {follow} |".format(
                company=esc(a.get("company")),
                file=a["_file"],
                role=esc(a.get("role")),
                status=STATUS_LABEL.get(a.get("status"), a.get("status", "")),
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


if __name__ == "__main__":
    main()
