#!/usr/bin/env python3
"""Tests for build_waiting_page.py.

Stdlib only, matching the script.  Run:  python3 scripts/test_build_waiting_page.py
"""
import unittest

import build_waiting_page as wp


def app(file="applications/x.md", status="submitted", **fields):
    a = {"_file": file, "status": status, "company": "Acme Ltd.", "role": "Student"}
    a.update(fields)
    return a


def collect(apps, leads=(), bodies=None):
    bodies = bodies or {}
    return wp.collect(list(apps), list(leads), lambda f: bodies.get(f, ""))


class Collect(unittest.TestCase):
    def test_only_waiting_statuses(self):
        apps = [app(f"applications/{s}.md", s) for s in
                ("submitted", "in-review", "interview", "offer",
                 "not-submitted", "rejected", "dropped")]
        got = {e["status"] for e in collect(apps)}
        self.assertEqual(got, {"submitted", "in-review", "interview", "offer"})

    def test_private_fields_never_exported(self):
        entry = collect([app(contact="a@b.com", gmail="secret", fit_role="9")])[0]
        for key in ("contact", "gmail", "fit_role", "_file"):
            self.assertNotIn(key, entry)

    def test_company_suffix_stripped(self):
        self.assertEqual(collect([app()])[0]["company"], "Acme")

    def test_placeholder_link_dropped(self):
        self.assertEqual(collect([app(jd_link="לינק למשרה")])[0]["link"], "")
        self.assertEqual(collect([app(jd_link="https://x.io/j")])[0]["link"], "https://x.io/j")

    def test_bad_date_becomes_empty(self):
        self.assertEqual(collect([app(applied="soon")])[0]["applied"], "")
        self.assertEqual(collect([app(applied="2026-08-09")])[0]["applied"], "2026-08-09")

    def test_referral_from_lead_or_contact(self):
        lead = {"status": "referred", "linked_application": "applications/a.md"}
        got = collect([app("applications/a.md"), app("applications/b.md"),
                       app("applications/c.md", contact="referral via Dana")], [lead])
        self.assertEqual([e["referral"] for e in got], [True, False, True])

    def test_contacted_lead_is_not_a_referral(self):
        lead = {"status": "contacted", "linked_application": "applications/a.md"}
        self.assertFalse(collect([app("applications/a.md")], [lead])[0]["referral"])

    def test_closed_posting_detected_from_notes(self):
        bodies = {"applications/a.md": "2026-10-01 - Posting closed as of today."}
        got = collect([app("applications/a.md"), app("applications/b.md")], bodies=bodies)
        self.assertEqual([e["posting_closed"] for e in got], [True, False])


class Render(unittest.TestCase):
    def test_script_close_is_escaped(self):
        html = wp.render([{"role": "</script><b>x"}], "2026-10-01")
        self.assertNotIn("</script><b>", html)
        self.assertIn("2026-10-01", html)


if __name__ == "__main__":
    unittest.main()
