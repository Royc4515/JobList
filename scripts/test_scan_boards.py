#!/usr/bin/env python3
"""Tests for the parsing and triage logic in scan_boards.py (no network).

Stdlib only, matching the script.  Run:  python3 scripts/test_scan_boards.py
"""
import json
import unittest
from unittest import mock

import scan_boards as sb

COMEET_HTML = 'x <script>var COMPANY_POSITIONS_DATA = ' + json.dumps([
    {"name": "AI Engineer - Student Position", "location": {"name": "Tel Aviv", "country": "IL"},
     "url_comeet_hosted_page": "https://www.comeet.com/jobs/acme/C5.004/ai-engineer/FA.D53",
     "time_updated": "2026-10-01T10:00:00Z"},
    {"name": "Sales Lead", "location": None, "url_comeet_hosted_page": None},
]) + ';\nvar OTHER = 1;</script>'


class Parsers(unittest.TestCase):
    def test_comeet_positions_read_from_embedded_json(self):
        rows = sb.parse_comeet("acme", sb.comeet_positions(COMEET_HTML))
        self.assertEqual(rows[0], ("acme", "AI Engineer - Student Position", "Tel Aviv Israel",
                                   "https://www.comeet.com/jobs/acme/C5.004/ai-engineer/FA.D53",
                                   "2026-10-01"))
        # Missing location / url must not crash.
        self.assertEqual(rows[1][2].strip(), "")

    def test_comeet_page_without_data_raises(self):
        # An empty list would make every tracked role at the company look closed.
        with self.assertRaises(ValueError):
            sb.comeet_positions("<html>consent page</html>")

    def test_null_fields_do_not_crash(self):
        ashby = {"jobs": [{"title": "Backend Intern", "location": None, "secondaryLocations": None,
                           "address": None, "jobUrl": "u"},
                          {"title": "Data Intern", "address": {"postalAddress": None}, "jobUrl": "v"}]}
        self.assertEqual(len(sb.parse_ashby("acme", ashby)), 2)
        gh = {"jobs": [{"title": "T", "location": None, "absolute_url": "u"}]}
        self.assertEqual(sb.parse_greenhouse("acme", gh)[0][2], "")
        sr = {"content": [{"name": "T", "id": 1, "location": None}]}
        self.assertEqual(sb.parse_smartrecruiters("acme", sr)[0][2].strip(), "")

    def test_ashby_uses_country_and_skips_unlisted(self):
        data = {"jobs": [
            {"title": "Backend Intern", "location": "Tel Aviv", "secondaryLocations": [],
             "address": {"postalAddress": {"addressCountry": "Israel"}},
             "jobUrl": "https://jobs.ashbyhq.com/acme/1", "publishedAt": "2026-09-30T00:00:00Z"},
            {"title": "Hidden", "isListed": False, "jobUrl": "u"},
        ]}
        rows = sb.parse_ashby("acme", data)
        self.assertEqual(len(rows), 1)
        self.assertIn("Israel", rows[0][2])
        self.assertEqual(rows[0][4], "2026-09-30")

    def test_greenhouse_and_lever(self):
        gh = sb.parse_greenhouse("acme", {"jobs": [
            {"title": "T", "location": {"name": "Tel Aviv"}, "absolute_url": "u", "updated_at": "2026-10-02T1"}]})
        self.assertEqual(gh, [("acme", "T", "Tel Aviv", "u", "2026-10-02")])
        lv = sb.parse_lever("acme", [{"text": "T", "hostedUrl": "u",
                                      "categories": {"location": "Haifa", "allLocations": ["Tel Aviv"]}}])
        self.assertEqual(lv[0][2], "Haifa Tel Aviv")


class ComeetUid(unittest.TestCase):
    def test_last_uid_is_the_position_not_the_company(self):
        url = "https://www.comeet.com/jobs/chargeafter/C5.004/fullstack-engineer-intern/FA.D53"
        self.assertEqual(sb.comeet_pos(url), "FA.D53")

    def test_company_site_links(self):
        self.assertEqual(sb.comeet_pos(
            "https://chargeafter.com/careers-2/co/tel-aviv-israel/FA.D53/fullstack-engineer-intern/all"), "FA.D53")
        self.assertEqual(sb.comeet_pos(
            "https://cellebrite.com/en/about/careers/positions/?comeet_cat=israel-tlv&comeet_pos=50.F69&comeet_all=all"),
            "50.F69")

    def test_non_comeet_link(self):
        self.assertIsNone(sb.comeet_pos("https://jobs.apple.com/en-il/details/200612345/sw-student"))

    def test_prefix_of_another_company_never_matches(self):
        # Review finding: "port" must not judge a Portnox role, nor "team8" a "Team" role.
        link = "https://portnox.com/careers/BB.222/dev"
        self.assertIsNone(sb.comeet_state(link, "company: Portnox", {"port": {"AA.111"}}))
        self.assertIsNone(sb.comeet_state(link, "company: Team", {"team8": {"AA.111"}}))
        self.assertEqual(sb.comeet_state(link, "company: Port Inc", {"port": {"AA.111"}}), "closed")

    def test_empty_board_is_not_evidence(self):
        link = "https://chargeafter.com/careers-2/co/x/FA.D53/y/all"
        self.assertIsNone(sb.comeet_state(link, "company: ChargeAfter", {"chargeafter": set()}))

    def test_hosted_link_left_to_direct_check(self):
        # Unlisted positions are live by direct link but absent from the board list.
        link = "https://www.comeet.com/jobs/chargeafter/C5.004/role/FA.D53"
        self.assertIsNone(sb.comeet_state(link, "company: ChargeAfter", {"chargeafter": {"AA.000"}}))

    def test_state_from_scanned_board(self):
        text = "company: ChargeAfter\nrole: x"
        link = "https://chargeafter.com/careers-2/co/tel-aviv-israel/FA.D53/x/all"
        self.assertEqual(sb.comeet_state(link, text, {"chargeafter": {"FA.D53"}}), "open")
        self.assertEqual(sb.comeet_state(link, text, {"chargeafter": {"AA.000"}}), "closed")
        # No board for this company: fall back to the direct check.
        self.assertIsNone(sb.comeet_state(link, text, {"rapyd": {"FA.D53"}}))

    def test_short_slug_does_not_match_unrelated_company(self):
        # "port" must not claim a file whose company merely contains "port".
        boards = {"port": {"CC.333"}}
        self.assertIsNone(sb.comeet_state("https://x.com/AB.123/", "company: Support Systems Ltd", boards))
        self.assertIsNone(sb.comeet_state("https://x.com/AB.123/", "company: Acme\nport", boards))
        self.assertEqual(sb.comeet_state("https://x.com/AB.123/", "company: Port", boards), "closed")


class Triage(unittest.TestCase):
    def test_skip_categories(self):
        for t in ("IT Support Engineer (Student)", "Design Verification - Intern", "Layout Student",
                  "Employer Branding Student", "Haifa Lab technician - Student", "QA Automation Student",
                  "Equity Compensation Administration Student", "NOC - Student Position",
                  "FP&A Analyst - Student Position", "Controller - Part-Time (50%)"):
            self.assertEqual(sb.triage(t), "skip", t)

    def test_strong_engineering_word_beats_soft_skip(self):
        # Review finding: these Tier 1-2 titles were hidden by substring Skip words.
        for t in ("Salesforce Developer Student", "AI Operations Student", "MLOps Operations Student",
                  "Backend Student - Accounting Automation", "Financial Data Engineer Student",
                  "Student Software Engineer, Content Understanding"):
            self.assertNotEqual(sb.triage(t), "skip", t)

    def test_hard_skip_wins_even_with_engineering_words(self):
        for t in ("Software Quality Student", "Tier 2 Customer Software Support - Student Position",
                  "Hardware Engineer Student"):
            self.assertEqual(sb.triage(t), "skip", t)

    def test_focus_titles(self):
        for t in ("AI Engineer - Student Position", "Backend Intern", "Python Developer Student",
                  "Algorithm Developer Student", "Software Engineer - Student Position"):
            self.assertEqual(sb.triage(t), "focus", t)

    def test_israel_student_filter(self):
        self.assertTrue(sb.is_israel_student(("acme", "Backend Intern", "Tel Aviv", "u", "")))
        self.assertFalse(sb.is_israel_student(("acme", "Backend Intern", "Berlin", "u", "")))
        self.assertFalse(sb.is_israel_student(("acme", "Backend Engineer", "Tel Aviv", "u", "")))
        self.assertTrue(sb.is_israel_student(("mobileye", "Student", "", "u", ""), ("mobileye",)))

    def test_part_time_counts_as_student(self):
        self.assertTrue(sb.is_israel_student(("acme", "AI Agent Designer (Part-Time)", "Tel Aviv", "u", "")))

    def test_already_tracked_by_company_and_title(self):
        apps = [("hpe.md", "dropped", "l", "company: hewlett packard enterprise\nrole: backend intern (1211019)\n"
                 "jd_link: https://hpe.wd5.myworkdayjobs.com/x")]
        self.assertTrue(sb.already_tracked(("hpe", "Backend Intern", "", "u", ""), apps))
        self.assertFalse(sb.already_tracked(("nice", "Backend Intern", "", "u", ""), apps))


class Liveness(unittest.TestCase):
    def test_ashby_checks_board_api(self):
        job = "https://jobs.ashbyhq.com/acme/0b1d2c3e-1111-2222-3333-444455556666"
        with mock.patch.object(sb, "fetch_json", return_value={"jobs": [{"id": "0b1d2c3e-1111-2222-3333-444455556666"}]}):
            self.assertEqual(sb.is_live(job), "open")
        with mock.patch.object(sb, "fetch_json", return_value={"jobs": []}):
            self.assertEqual(sb.is_live(job), "closed")
        gone = sb.urllib.error.HTTPError("u", 404, "nf", {}, None)
        with mock.patch.object(sb, "fetch_json", side_effect=gone):
            self.assertTrue(sb.is_live(job).startswith("unknown"))

    def test_comeet_redirect_to_board_means_closed(self):
        url = "https://www.comeet.com/jobs/acme/C5.004/role/FA.D53"

        def opener(final):
            resp = mock.MagicMock()
            resp.__enter__.return_value.geturl.return_value = final
            return mock.patch.object(sb, "_open", return_value=resp)

        with opener(url):
            self.assertEqual(sb.is_live(url), "open")
        with opener("https://www.comeet.com/jobs/acme/C5.004"):
            self.assertEqual(sb.is_live(url), "closed")

    def test_greenhouse_job_on_company_site(self):
        link = "https://www.taboola.com/careers/job/software-engineer-intern?gh_jid=4847843"
        text = "company: taboola\n"
        err = sb.urllib.error.HTTPError("u", 404, "nf", {}, None)
        with mock.patch.object(sb, "_open", side_effect=err):
            self.assertEqual(sb.greenhouse_state(link, text), "closed")
        with mock.patch.object(sb, "_open", return_value=mock.MagicMock()):
            self.assertEqual(sb.greenhouse_state(link, text), "open")
        self.assertIsNone(sb.greenhouse_state(link, "company: unknownco\n"))
        # Review finding: the 3-letter "via" board must not judge a Viavi role.
        self.assertIsNone(sb.greenhouse_state("https://viavi.com/jobs?gh_jid=1", "company: Viavi Solutions\n"))
        self.assertIsNone(sb.greenhouse_state("https://jobs.apple.com/x", text))

    def test_every_board_kind_is_dispatchable(self):
        kinds = {k for k, _ in sb.all_boards()}
        self.assertEqual(kinds, {"greenhouse", "lever", "lever_eu", "ashby", "smartrecruiters", "workday", "comeet"})


if __name__ == "__main__":
    unittest.main()
