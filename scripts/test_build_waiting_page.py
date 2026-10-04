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

    def test_blurb_passed_through_and_optional(self):
        self.assertEqual(collect([app(blurb="  פיתוח backend  ")])[0]["blurb"], "פיתוח backend")
        self.assertEqual(collect([app()])[0]["blurb"], "")

    def test_private_text_not_leaked_via_other_fields(self):
        entry = collect([app(contact="dana@x.com", gmail="gmail-secret",
                             fit_note="note-secret", fit_gates="0", blurb="public")],
                        bodies={"applications/x.md": "body-secret"})[0]
        blob = repr(entry)
        for secret in ("dana@x.com", "gmail-secret", "note-secret", "body-secret"):
            self.assertNotIn(secret, blob)
        for key in ("fit_note", "fit_gates", "fit_stack", "fit_path"):
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

    def test_closed_posting_excluded_from_page(self):
        bodies = {"applications/a.md": "2026-10-01 - Posting closed as of today.",
                  "applications/c.md": "Posting no longer live."}
        got = collect([app("applications/a.md"), app("applications/b.md", role="Open"),
                       app("applications/c.md")], bodies=bodies)
        self.assertEqual([e["role"] for e in got], ["Open"])

    def test_company_with_only_closed_roles_disappears(self):
        bodies = {"applications/a.md": "Posting closed."}
        got = collect([app("applications/a.md", company="Gone"),
                       app("applications/b.md", company="Here")], bodies=bodies)
        self.assertEqual({e["company"] for e in got}, {"Here"})


class CompanyKey(unittest.TestCase):
    def test_latin_name_slugged(self):
        self.assertEqual(wp.company_key("Check Point"), "check-point")
        self.assertEqual(wp.company_key("IAI (Israel Aerospace Industries)"),
                         "iai-israel-aerospace-industries")

    def test_hebrew_name_gets_stable_hash(self):
        key = wp.company_key("מערך הדיגיטל הלאומי")
        self.assertRegex(key, r"^c-[0-9a-f]{10}$")
        self.assertEqual(key, wp.company_key("מערך הדיגיטל הלאומי"))

    def test_entry_carries_key(self):
        self.assertEqual(collect([app()])[0]["company_key"], "acme")


class Render(unittest.TestCase):
    def test_stale_days_filled_in(self):
        html = wp.render([], "2026-10-01")
        self.assertNotIn("__STALE_DAYS__", html)
        self.assertIn(f"var STALE_DAYS = {wp.STALE_DAYS};", html)

    def test_script_close_is_escaped(self):
        html = wp.render([{"role": "</script><b>x"}], "2026-10-01")
        self.assertNotIn("</script><b>", html)
        self.assertIn("2026-10-01", html)


if __name__ == "__main__":
    unittest.main()
