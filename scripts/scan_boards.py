#!/usr/bin/env python3
"""Scan public career boards for student/intern roles in Israel.

Also re-checks every tracked posting URL in applications/ directly, because a
board's API is not a reliable liveness signal (Lever's API has been seen to omit
postings that are still live).

Boards: Greenhouse, Lever (global + EU), Ashby, SmartRecruiters, Workday and
Comeet. Comeet is what most Israeli startups use; it has no public API, but each
company's hosted page (comeet.com/jobs/<slug>/<uid>) embeds the full position
list as JSON, so no browser is needed.

New finds are triaged by title against PROFILE.md: likely-relevant roles first,
Skip-category titles (hardware, IT, QA, HR...) collapsed to one line, and roles
already tracked under another req number are listed separately.

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

# Every token below was confirmed to return live jobs on 2026-10-05 (most with
# Israel locations). Add a company by appending its board token.
GREENHOUSE = [
    "apiiro", "appsflyer", "axonius", "catonetworks", "connecteam", "cymulate", "datadog",
    "duda", "eleoshealth", "forter", "gongio", "guardz", "jfrog", "lightricks", "lightrun",
    "melio", "mixtiles", "mongodb", "nanit", "nice", "optimove", "orcasecurity", "payoneer",
    "riskified", "saltsecurity", "similarweb", "sweetsecurity", "taboola", "torq",
    "transmitsecurity", "via", "wizinc", "yotpo",
]
LEVER = ["cloudinary", "walkme"]
LEVER_EU = ["mobileye"]
ASHBY = ["finout", "lemonade", "moonactive", "sisense", "snowflake", "wonderful"]
SMARTRECRUITERS = ["Wix2", "armis", "servicenow"]
# Workday: (tenant, wd-host, site). Searched for "student" and "intern" in Israel.
WORKDAY = [
    ("intel", "wd1", "External"), ("marvell", "wd1", "MarvellCareers"),
    ("hpe", "wd5", "Jobsathpe"), ("motorolasolutions", "wd5", "Careers"),
    ("nvidia", "wd5", "NVIDIAExternalCareerSite"), ("kla", "wd1", "Search"),
    ("amat", "wd1", "External"), ("salesforce", "wd12", "External_Career_Site"),
    ("crowdstrike", "wd5", "crowdstrikecareers"),
]
# Comeet: (slug, company uid) from the hosted page URL comeet.com/jobs/<slug>/<uid>.
COMEET = [
    ("abra_rnd", "15.007"), ("ai21", "E6.001"), ("alice", "D5.005"),
    ("arpeely", "57.001"), ("askai", "1A.00C"), ("autobrains", "57.004"),
    ("automatit", "26.003"), ("ceragon", "D3.003"), ("ceva", "76.005"),
    ("chargeafter", "C5.004"), ("checkmarx", "C0.008"), ("Claroty", "F2.004"),
    ("clover_security", "7A.00A"), ("cognyte", "F2.009"), ("comm-it", "76.008"),
    ("crossriver", "C7.00F"), ("drivenets", "72.006"), ("etoro", "41.009"),
    ("exodigo", "89.005"), ("factify", "A9.00F"), ("fiverr", "60.002"),
    ("flexor", "F9.006"), ("fullpath", "54.002"), ("global-e", "62.002"),
    ("growthspace", "D7.00A"), ("imagene-ai", "D7.000"), ("infinidat", "D6.003"),
    ("inmanage", "B7.006"), ("integritylabs", "43.009"), ("jifiti", "47.005"),
    ("joinattil", "38.00A"), ("kaltura", "E2.00D"), ("kelatechnologies", "2A.007"),
    ("majesticlabs", "AA.004"), ("native", "5A.00A"), ("navina", "E6.00C"),
    ("nayax", "13.009"), ("nextsilicon", "18.007"), ("nimbleway", "09.00F"),
    ("nova", "A5.007"), ("oligosecurity", "5A.00B"), ("onezerobank", "36.00A"),
    ("optibus", "D1.00C"), ("pango", "59.002"), ("papayaglobal", "16.005"),
    ("papayagaming", "46.00B"), ("pentera", "C5.00D"), ("play_perfect", "69.001"),
    ("port", "59.004"), ("quantummachines", "D6.000"), ("rapyd", "73.00E"),
    ("reeco", "0A.00D"), ("regulus", "9A.00D"), ("risecodes", "A9.000"),
    ("samsung", "D4.005"), ("senai", "CA.004"), ("sensi", "E7.00F"),
    ("silverfort", "54.007"), ("solaredge", "71.00A"), ("tabnine", "39.006"),
    ("team8", "61.003"), ("thetaray", "72.00F"), ("upstream", "E4.003"),
    ("upwind", "49.004"), ("uveye", "92.00F"), ("vastdata", "43.001"), ("vega", "C9.009"),
    ("voyantis", "86.00B"), ("waterfall-security", "C7.009"), ("wiliot", "F6.003"),
    ("xsightlabs", "46.00C"), ("zenity", "19.000"), ("zipher", "4B.00C"), ("zyg", "DA.006"),
]

STUDENT = re.compile(r"\b(student|intern|internship|part[- ]?time)\b|סטודנט", re.I)
ISRAEL = re.compile(
    r"israel|tel[ -]?aviv|herzliya|haifa|jerusalem|petah|petach|ra.?anana|netanya|"
    r"rehovot|yokneam|be.?er ?sheva|ramat|hod hasharon|kfar saba|modi|caesarea|"
    r"or yehuda|airport city|kiryat|migdal|ישראל",
    re.I,
)
# Titles in PROFILE.md's Skip list. HARD_SKIP (QA, IT support, hardware) is a Skip
# whatever else the title says; SOFT_SKIP (non-engineering words) yields to a
# STRONG Tier 1-2 word, so "Salesforce Developer Student" or "AI Operations
# Student" stay visible.
HARD_SKIP = re.compile(
    r"\bqa\b|quality|\bit\b|help ?desk|\bnoc\b|\bsupport\b|technician|layout|"
    r"physical design|design verification|digital ic|analog|\basic\b|vlsi|\brtl\b|\bdft\b|"
    r"fpga|signal integrity|hardware|firmware|board design|\blab\b|mechanical|electrical|"
    r"industrial engineer|practical engineering",
    re.I,
)
SOFT_SKIP = re.compile(
    r"controller|fp&a|\bhr\b|human resources|recruit|talent|employer brand|\baccount|"
    r"audit|bookkeep|\bfinanc|payroll|equity|legal|marketing|\bsales\b|\bsdr\b|\bbdr\b|"
    r"\boffice\b|\badmin|procurement|buyer|customer success|operator|\boperations\b|"
    r"\bchip\b|silicon|product owner|product manag|graphic|\bcontent\b|labeler|tagging",
    re.I,
)
STRONG = re.compile(
    r"\bai\b|\bml\b|mlops|machine learning|llm|genai|gen ai|\bagents?\b|python|backend|"
    r"back-end|software|developer|algorithm|data engineer|full[- ]?stack",
    re.I,
)
# Tier 1-2 direction words from PROFILE.md, used only to order the relevant list.
FOCUS = re.compile(
    r"\bai\b|\bml\b|machine learning|llm|genai|gen ai|agent|python|backend|back-end|data|"
    r"algorithm|automation|integration|software|developer|engineer|research",
    re.I,
)
COMEET_UID = re.compile(r"(?:comeet_pos=|/)([0-9A-F]{2}\.[0-9A-F]{3})(?=[/&?#]|$)", re.I)
COMEET_MARK = "COMPANY_POSITIONS_DATA = "
UA = {"User-Agent": "Mozilla/5.0"}


def fetch_json(url, body=None):
    headers = dict(UA, **({"Content-Type": "application/json"} if body else {}))
    req = urllib.request.Request(url, json.dumps(body).encode() if body else None, headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def fetch_text(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "replace")


# --- Parsers: board payload -> (company, title, location, url, date) rows ---------

def parse_greenhouse(token, data):
    return [(token, j["title"], (j.get("location") or {}).get("name") or "",
             j["absolute_url"], j.get("updated_at", "")[:10]) for j in data["jobs"]]


def parse_lever(token, data):
    rows = []
    for j in data:
        c = j.get("categories") or {}
        loc = " ".join([c.get("location", "") or ""] + (c.get("allLocations") or []))
        rows.append((token, j["text"], loc, j["hostedUrl"], ""))
    return rows


def parse_ashby(token, data):
    rows = []
    for j in data["jobs"]:
        if j.get("isListed") is False:
            continue
        address = (j.get("address") or {}).get("postalAddress") or {}
        extra = [(x or {}).get("location") or "" for x in j.get("secondaryLocations") or []]
        locs = [j.get("location") or ""] + extra
        country = address.get("addressCountry") or ""
        rows.append((token, j["title"], " ".join(locs + [country]), j["jobUrl"],
                     (j.get("publishedAt") or "")[:10]))
    return rows


def parse_smartrecruiters(token, data):
    rows = []
    for j in data["content"]:
        loc = j.get("location") or {}
        rows.append((token, j["name"], f'{loc.get("city") or ""} {loc.get("country") or ""}',
                     f"https://jobs.smartrecruiters.com/{token}/{j['id']}",
                     (j.get("releasedDate") or "")[:10]))
    return rows


def comeet_positions(html):
    """The position list a Comeet hosted page embeds.

    Raises when the page carries no list (a consent or bot page, a layout change):
    the board is then reported unreachable instead of looking empty, because an
    empty board would make every tracked role at that company look closed.
    """
    i = html.find(COMEET_MARK)
    if i < 0:
        raise ValueError("no COMPANY_POSITIONS_DATA on the Comeet page")
    return json.JSONDecoder().raw_decode(html, i + len(COMEET_MARK))[0]


def parse_comeet(slug, positions):
    rows = []
    for p in positions:
        loc = p.get("location") or {}
        country = "Israel" if loc.get("country") == "IL" else (loc.get("country") or "")
        rows.append((slug, p["name"], f'{loc.get("name") or ""} {country}',
                     p.get("url_comeet_hosted_page") or "", (p.get("time_updated") or "")[:10]))
    return rows


def workday_jobs(token):
    tenant, wd, site = token
    base = f"https://{tenant}.{wd}.myworkdayjobs.com"
    rows, seen = [], set()
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


def board_jobs(kind, token):
    """Return (company, title, location, url, date) rows for one board."""
    if kind == "greenhouse":
        return parse_greenhouse(token, fetch_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs"))
    if kind == "lever":
        return parse_lever(token, fetch_json(f"https://api.lever.co/v0/postings/{token}?mode=json"))
    if kind == "lever_eu":
        return parse_lever(token, fetch_json(f"https://api.eu.lever.co/v0/postings/{token}?mode=json"))
    if kind == "ashby":
        return parse_ashby(token, fetch_json(f"https://api.ashbyhq.com/posting-api/job-board/{token}"))
    if kind == "smartrecruiters":
        url = f"https://api.smartrecruiters.com/v1/companies/{token}/postings?limit=100"
        return parse_smartrecruiters(token, fetch_json(url))
    if kind == "comeet":
        slug, uid = token
        return parse_comeet(slug, comeet_positions(fetch_text(f"https://www.comeet.com/jobs/{slug}/{uid}")))
    if kind == "workday":
        return workday_jobs(token)
    raise ValueError(f"unknown board kind {kind}")


# --- Triage -----------------------------------------------------------------------

def norm(s):
    return re.sub(r"[^a-z0-9א-ת]", "", s.lower())


def triage(title):
    """'skip' for PROFILE.md Skip-category titles, 'focus' for Tier 1-2 words, else 'other'."""
    if HARD_SKIP.search(title) or (SOFT_SKIP.search(title) and not STRONG.search(title)):
        return "skip"
    return "focus" if FOCUS.search(title) else "other"


def already_tracked(row, apps):
    """True when a tracked file names the same company and title (another req number)."""
    company = re.compile(r"\b" + re.escape(row[0].lower()))
    title = norm(row[1])
    return any(title and title in norm(text) and company.search(text) for *_, text in apps)


def is_israel_student(row, eu_lever=()):
    return bool(STUDENT.search(row[1]) and (ISRAEL.search(row[2]) or row[0] in eu_lever))


# --- Liveness ---------------------------------------------------------------------

def _open(url):
    url = urllib.parse.quote(url, safe=":/?&=%#@+,;~")
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=20)


def comeet_pos(link):
    """The position uid in a Comeet link (the last uid; the first is the company's)."""
    parts = urllib.parse.urlparse(link)
    found = COMEET_UID.findall(f"{parts.path}?{parts.query}")
    return found[-1].upper() if found else None


def company_of(text):
    m = re.search(r"^company:[ \t]*(.*)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


def same_company(board, company):
    """A board token names the company a file names: the whole name or its first word.

    Exact on purpose - a prefix match would check a Portnox role against the
    "port" board, or a Viavi role against "via", and call it closed.
    """
    words = company.split()
    return bool(words) and norm(board) in (norm(company), norm(words[0]))


def comeet_state(link, text, boards):
    """Liveness of a Comeet position from the scanned boards, or None if no board matches.

    Companies embed Comeet in their own site (chargeafter.com/.../FA.D53/...,
    cellebrite.com/...?comeet_pos=50.F69), so the position uid in the link is
    looked up in the board of the company the file names.
    """
    pos, company = comeet_pos(link), company_of(text)
    if not pos or "comeet.com" in link:
        return None  # a hosted link gets the direct check, which also sees unlisted jobs
    for slug, uids in boards.items():
        if uids and same_company(slug, company):
            return "open" if pos in uids else "closed"
    return None


def greenhouse_state(link, text):
    """Liveness of a Greenhouse job embedded in a company site (taboola.com/...?gh_jid=N).

    The job id is checked against the board of the company the file names; None
    when the link has no gh_jid or no tracked board matches.
    """
    m, company = re.search(r"[?&]gh_jid=(\d+)", link), company_of(text)
    if not m or "greenhouse.io" in link:
        return None
    for token in GREENHOUSE:
        if same_company(token, company):
            try:
                with _open(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs/{m.group(1)}"):
                    return "open"
            except urllib.error.HTTPError as e:
                return "closed" if e.code in (404, 410) else f"unknown: HTTP {e.code}"
            except Exception as e:
                return f"unknown: {type(e).__name__}"
    return None


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
        if "comeet.com" in host:
            pos = comeet_pos(url)
            if not pos:
                return "unknown: unrecognised Comeet link"
            with _open(url) as r:
                final = r.geturl()
            # A closed Comeet position redirects to the company's board root.
            return "open" if comeet_pos(final) == pos else "closed"
        if "ashbyhq.com" in host:
            m = re.search(r"ashbyhq\.com/([^/]+)/([0-9a-f-]{36})", url)
            if not m:
                return "unknown: unrecognised Ashby link"
            # The job page is a client-side app (always 200); the board API is the truth.
            # A missing board (renamed slug) says nothing about the job: unknown, not closed.
            try:
                data = fetch_json(f"https://api.ashbyhq.com/posting-api/job-board/{m.group(1)}")
            except urllib.error.HTTPError as e:
                return f"unknown: Ashby board HTTP {e.code}"
            return "open" if any(j.get("id") == m.group(2) for j in data.get("jobs") or []) else "closed"
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


# --- Report -----------------------------------------------------------------------

def all_boards():
    return ([("greenhouse", t) for t in GREENHOUSE] + [("lever", t) for t in LEVER]
            + [("lever_eu", t) for t in LEVER_EU] + [("ashby", t) for t in ASHBY]
            + [("smartrecruiters", t) for t in SMARTRECRUITERS] + [("workday", t) for t in WORKDAY]
            + [("comeet", t) for t in COMEET])


def scan(boards):
    """Fetch every board. Returns (rows, unreachable names, comeet uids by slug)."""
    rows, unreachable, comeet = [], [], {}
    with cf.ThreadPoolExecutor(12) as ex:
        futures = {ex.submit(board_jobs, k, t): (k, t) for k, t in boards}
        for fut in cf.as_completed(futures):
            kind, token = futures[fut]
            name = token[0] if isinstance(token, tuple) else token
            try:
                got = fut.result()
            except Exception as e:
                unreachable.append(f"{name} ({type(e).__name__})")
                continue
            rows.extend(got)
            if kind == "comeet":
                comeet[name] = {comeet_pos(r[3]) for r in got} - {None}
    return rows, unreachable, comeet


def print_rows(rows):
    for co, title, loc, url, date in rows:
        print(f"- {co} | {title} | {loc.strip()} | {date or '-'} | {url}")


def report_new(rows, apps):
    links = {a[2].rstrip("/") for a in apps if a[2]}
    hits = sorted({r[:2] + (r[2].split(" /job/")[0],) + r[3:] for r in rows
                   if is_israel_student(r, LEVER_EU)})
    new = [r for r in hits if r[3].rstrip("/") not in links]
    dupes = [r for r in new if already_tracked(r, apps)]
    fresh = [r for r in new if r not in dupes]
    groups = {k: [r for r in fresh if triage(r[1]) == k] for k in ("focus", "other", "skip")}

    relevant = groups["focus"] + groups["other"]
    print(f"\n## New student/intern roles in Israel - likely relevant ({len(relevant)})")
    print_rows(relevant)
    if dupes:
        print(f"\n## Same company and title already tracked - new req number? ({len(dupes)})")
        print_rows(dupes)
    if groups["skip"]:
        print(f"\n## Skip-category titles per PROFILE.md ({len(groups['skip'])}): "
              + "; ".join(f"{r[0]} - {r[1].strip()}" for r in groups["skip"]))


def report_liveness(apps, comeet):
    # Only check live-trackable postings: submitted or not-submitted with a real link.
    to_check = [a for a in apps if a[2].startswith("http") and a[1] in ("submitted", "not-submitted", "in-review")]

    def state(a):
        return comeet_state(a[2], a[3], comeet) or greenhouse_state(a[2], a[3]) or is_live(a[2])

    with cf.ThreadPoolExecutor(8) as ex:
        states = list(ex.map(state, to_check))
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


def main():
    boards = all_boards()
    rows, unreachable, comeet = scan(boards)
    print(f"Scanned {len(rows)} open jobs across {len(boards) - len(unreachable)} boards.")
    if unreachable:
        print("Unreachable boards: " + ", ".join(unreachable))
    apps = tracked()
    report_new(rows, apps)
    report_liveness(apps, comeet)


if __name__ == "__main__":
    main()
