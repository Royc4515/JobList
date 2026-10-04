#!/usr/bin/env python3
"""Build a shareable "waiting for an answer" page from applications/*.md.

Picks every role whose status means Roy applied and has no final answer yet
(submitted, in-review, interview, offer) and writes a self-contained HTML page,
grouped by company, to out/waiting.html. Only public-safe fields are exported:
no contacts, Gmail notes or fit scores, since the page is meant to be shared.

Roles whose posting is closed / no longer live (a dated "Posting closed" note in
the tracker file) are left off the page entirely, and a company with no remaining
roles disappears. Their tracker status is unchanged: they are not rejections.

Days-waiting is computed in the browser, so the page stays accurate between
rebuilds. Roles past STALE_DAYS move to a separate "no answer" section.
Stdlib only.

Usage:  python scripts/build_waiting_page.py
"""
import hashlib
import json
import re
from datetime import date
from pathlib import Path

from build_dashboard import ROOT, load_apps, load_leads

TEMPLATE = ROOT / "scripts" / "waiting_template.html"
OUT = ROOT / "out" / "waiting.html"

WAITING_STATUSES = ("offer", "interview", "in-review", "submitted")
# After this many days with no answer a role moves to the page's "no answer"
# section. Almost every answer in this tracker arrived within ~7 weeks.
STALE_DAYS = 50
REFERRAL_LEAD_STATUSES = ("referred", "responded")
CLOSED_PATTERN = re.compile(r"posting (closed|no longer live)", re.IGNORECASE)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COMPANY_SUFFIXES = (" Ltd.", " Ltd", " Inc.", " Inc")


def clean_company(name):
    for suffix in COMPANY_SUFFIXES:
        if name.endswith(suffix):
            return name[: -len(suffix)].strip()
    return name.strip()


def company_key(name):
    """Stable ASCII id for a company, used as its document id in the page's db.

    Non-Latin names (e.g. Hebrew) fall back to a short hash so the key stays
    inside the db path grammar.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "c-" + hashlib.sha1(name.encode("utf-8")).hexdigest()[:10]


def public_link(value):
    """Only real URLs are shared; placeholders like 'לינק למשרה' are dropped."""
    value = (value or "").strip()
    return value if value.startswith(("http://", "https://")) else ""


def iso_or_empty(value):
    value = (value or "").split("#", 1)[0].strip()
    return value if ISO_DATE.match(value) else ""


def referred_files(leads):
    return {
        lead.get("linked_application", "").strip()
        for lead in leads
        if lead.get("status") in REFERRAL_LEAD_STATUSES
    }


def to_entry(app, body, referred):
    contact = app.get("contact", "")
    company = clean_company(app.get("company", ""))
    return {
        "company": company,
        "company_key": company_key(company),
        "role": app.get("role", "").strip(),
        "status": app["status"],
        "applied": iso_or_empty(app.get("applied")),
        "location": app.get("location", "").strip(),
        "work_model": app.get("work_model", "").split("#", 1)[0].strip(),
        "link": public_link(app.get("jd_link")),
        "referral": app["_file"] in referred or "referral" in contact.lower(),
        "posting_closed": bool(CLOSED_PATTERN.search(body)),
    }


def collect(apps, leads, read_body):
    referred = referred_files(leads)
    entries = (
        to_entry(app, read_body(app["_file"]), referred)
        for app in apps
        if app.get("status") in WAITING_STATUSES
    )
    return [e for e in entries if not e["posting_closed"]]


def render(entries, built_on):
    payload = json.dumps(entries, ensure_ascii=False, indent=1)
    # Keep a stray "</script>" in any field from closing the data block early.
    payload = payload.replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8")
    return (
        html.replace("__DATA__", payload)
        .replace("__BUILT__", built_on)
        .replace("__STALE_DAYS__", str(STALE_DAYS))
    )


def main():
    entries = collect(
        load_apps(),
        load_leads(),
        lambda rel: (ROOT / rel).read_text(encoding="utf-8"),
    )
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(render(entries, date.today().isoformat()), encoding="utf-8")
    companies = len({e["company"] for e in entries})
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(entries)} roles at {companies} companies")


if __name__ == "__main__":
    main()
