#!/usr/bin/env python3
"""Scan public career boards for student/intern roles in Israel.

Also re-checks every tracked posting URL in applications/ directly, because a
board's API is not a reliable liveness signal (Lever's API has been seen to omit
postings that are still live).

Stdlib only. Usage:  python3 scripts/scan_boards.py
"""
import concurrent.futures as cf
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPS = ROOT / "applications"

# Boards confirmed live on 2026-09-27. Add a company by appending its board token.
GREENHOUSE = [
    "appsflyer", "axonius", "catonetworks", "forter", "gongio", "island", "jfrog",
    "lightricks", "melio", "nice", "payoneer", "riskified", "similarweb", "taboola",
]
LEVER_EU = ["mobileye"]
SMARTRECRUITERS = ["Wix2"]
# Workday: (tenant, wd-host, site). Searched for "student" and "intern" in Israel.
WORKDAY = [
    ("intel", "wd1", "External"), ("marvell", "wd1", "MarvellCareers"),
    ("hpe", "wd5", "Jobsathpe"), ("motorolasolutions", "wd5", "Careers"),
    ("nvidia", "wd5", "NVIDIAExternalCareerSite"), ("kla", "wd1", "Search"),
    ("amat", "wd1", "External"), ("salesforce", "wd12", "External_Career_Site"),
    ("crowdstrike", "wd5", "crowdstrikecareers"),
]

STUDENT = re.compile(r"\b(student|intern|internship)\b|סטודנט", re.I)
ISRAEL = re.compile(
    r"israel|tel[ -]?aviv|herzliya|haifa|jerusalem|petah|petach|ra.?anana|netanya|"
    r"rehovot|yokneam|be.?er ?sheva|ramat|hod hasharon|kfar saba|modi|caesarea|"
    r"or yehuda|airport city|kiryat|migdal|ישראל",
    re.I,
)
UA = {"User-Agent": "Mozilla/5.0"}


def fetch_json(url, body=None):
    headers = dict(UA, **({"Content-Type": "application/json"} if body else {}))
    req = urllib.request.Request(url, json.dumps(body).encode() if body else None, headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def board_jobs(kind, token):
    """Return (company, title, location, url, date) rows for one board."""
    rows = []
    if kind == "greenhouse":
        data = fetch_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs")
        for j in data["jobs"]:
            rows.append((token, j["title"], j.get("location", {}).get("name", ""),
                         j["absolute_url"], j.get("updated_at", "")[:10]))
    elif kind == "lever_eu":
        for j in fetch_json(f"https://api.eu.lever.co/v0/postings/{token}?mode=json"):
            c = j.get("categories", {})
            loc = " ".join([c.get("location", "")] + (c.get("allLocations") or []))
            rows.append((token, j["text"], loc, j["hostedUrl"], ""))
    elif kind == "smartrecruiters":
        url = f"https://api.smartrecruiters.com/v1/companies/{token}/postings?limit=100"
        for j in fetch_json(url)["content"]:
            loc = j.get("location", {})
            rows.append((token, j["name"], f'{loc.get("city", "")} {loc.get("country", "")}',
                         f"https://jobs.smartrecruiters.com/{token}/{j['id']}",
                         (j.get("releasedDate") or "")[:10]))
    elif kind == "workday":
        tenant, wd, site = token
        base = f"https://{tenant}.{wd}.myworkdayjobs.com"
        seen = set()
        for term in ("student israel", "intern israel"):
            data = fetch_json(f"{base}/wday/cxs/{tenant}/{site}/jobs",
                              {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": term})
            for j in data.get("jobPostings", []):
                if j["externalPath"] in seen:
                    continue
                seen.add(j["externalPath"])
                # locationsText can be "2 Locations"; the path carries the city.
                rows.append((tenant, j["title"], f'{j.get("locationsText", "")} {j["externalPath"]}',
                             f"{base}/en-US/{site}{j['externalPath']}", j.get("postedOn", "")))
    return rows


def _open(url):
    url = urllib.parse.quote(url, safe=":/?&=%#@+,;~")
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=20)


def is_live(url):
    """Direct check. Returns 'open', 'closed', or 'unknown: <reason>'.

    Only trusted on applicant-tracking hosts whose closed state is unambiguous.
    Company sites (Apple, Siemens, SentinelOne...) render jobs with JavaScript and
    carry "not found" strings in their page code even when a posting is live, so
    they are reported as unknown rather than guessed at.
    """
    host = urllib.parse.urlparse(url).netloc.lower()
    try:
        if "smartrecruiters.com" in host:
            m = re.search(r"smartrecruiters\.com/([^/]+)/(\d+)", url)
            if not m:
                return "unknown: unrecognised SmartRecruiters link"
            api = f"https://api.smartrecruiters.com/v1/companies/{m.group(1)}/postings/{m.group(2)}"
            with _open(api):
                return "open"
        if "lever.co" in host:
            with _open(url):
                return "open"
        if "myworkdayjobs.com" in host:
            m = re.search(r"https://([^.]+)\.[^/]+/(?:[a-z]{2}-[A-Z]{2}/)?([^/]+)(/job/.+)", url)
            if not m:
                return "unknown: unrecognised Workday link"
            api = f"https://{host}/wday/cxs/{m.group(1)}/{m.group(2)}{m.group(3)}"
            with _open(api):
                return "open"
        if "greenhouse.io" in host:
            with _open(url) as r:
                final = r.geturl()
            # A closed Greenhouse job redirects off the board to a generic careers page.
            return "open" if "greenhouse.io" in urllib.parse.urlparse(final).netloc else "closed"
    except urllib.error.HTTPError as e:
        return "closed" if e.code in (404, 410) else f"unknown: HTTP {e.code}"
    except Exception as e:  # network trouble is not evidence of closure
        return f"unknown: {type(e).__name__}"
    return "unknown: company site, check by hand"


def tracked():
    """(filename, status, jd_link, full text) for each application file."""
    out = []
    for f in sorted(APPS.glob("*.md")):
        t = f.read_text(encoding="utf-8")
        link = re.search(r"^jd_link:[ \t]*(\S*)", t, re.M)
        status = re.search(r"^status:[ \t]*(\S*)", t, re.M)
        out.append((f.name, status.group(1) if status else "",
                    link.group(1) if link else "", t.lower()))
    return out


def main():
    jobs = [("greenhouse", t) for t in GREENHOUSE] + [("lever_eu", t) for t in LEVER_EU] \
        + [("smartrecruiters", t) for t in SMARTRECRUITERS] + [("workday", t) for t in WORKDAY]
    rows, unreachable = [], []
    with cf.ThreadPoolExecutor(8) as ex:
        futures = {ex.submit(board_jobs, k, t): t for k, t in jobs}
        for fut in cf.as_completed(futures):
            try:
                rows.extend(fut.result())
            except Exception as e:
                t = futures[fut]
                unreachable.append(f"{t[0] if isinstance(t, tuple) else t} ({type(e).__name__})")

    apps = tracked()
    links = {a[2].rstrip("/") for a in apps if a[2]}
    hits = sorted({r[:2] + (r[2].split(" /job/")[0],) + r[3:] for r in rows if STUDENT.search(r[1])
                   and (ISRAEL.search(r[2]) or r[0] in LEVER_EU)})
    new = [r for r in hits if r[3].rstrip("/") not in links]

    print(f"Scanned {len(rows)} open jobs across {len(jobs) - len(unreachable)} boards.")
    if unreachable:
        print("Unreachable boards: " + ", ".join(unreachable))
    print(f"\n## New student/intern roles in Israel ({len(new)})")
    for co, title, loc, url, date in new:
        print(f"- {co} | {title} | {loc.strip()} | {date or '-'} | {url}")

    # Only check live-trackable postings: submitted or not-submitted with a real link.
    to_check = [a for a in apps if a[2].startswith("http") and a[1] in ("submitted", "not-submitted", "in-review")]
    with cf.ThreadPoolExecutor(8) as ex:
        states = list(ex.map(lambda a: is_live(a[2]), to_check))
    closed = [(a, s) for a, s in zip(to_check, states) if s == "closed"]
    unknown = [(a, s) for a, s in zip(to_check, states) if s.startswith("unknown")]
    print(f"\n## Tracked postings no longer live ({len(closed)})")
    print("(closed to new applicants - NOT a rejection)")
    for (name, status, link, _), _ in closed:
        print(f"- {name} [{status}] {link}")
    if unknown:
        print(f"\n## Could not verify automatically ({len(unknown)})")
        for (name, _, link, _), s in unknown:
            print(f"- {name}: {s.removeprefix('unknown: ')}")


if __name__ == "__main__":
    main()
