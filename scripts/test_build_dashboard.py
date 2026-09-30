#!/usr/bin/env python3
"""Tests for the fit-score logic in build_dashboard.py.

Stdlib only, matching the script.  Run:  python3 scripts/test_build_dashboard.py
"""
import unittest

import build_dashboard as bd


def app(file="applications/x.md", status="not-submitted", **fit):
    a = {"_file": file, "status": status, "company": file, "role": "R"}
    a.update({k: str(v) for k, v in fit.items()})
    return a


FULL = dict(fit_role=8, fit_stack=7, fit_gates=9, fit_path=5)


class ParseFit(unittest.TestCase):
    def test_full_score_sums(self):
        fit, warn = bd.parse_fit(app(**FULL))
        self.assertIsNone(warn)
        self.assertEqual(fit[0], 29)
        self.assertFalse(fit[2])

    def test_unscored_is_silent(self):
        # Most historical files have no score; that must not spam warnings.
        self.assertEqual(bd.parse_fit(app()), (None, None))

    def test_partial_score_warns_and_is_ignored(self):
        fit, warn = bd.parse_fit(app(fit_role=8, fit_stack=7))
        self.assertIsNone(fit)
        self.assertIn("fit_gates", warn)

    def test_out_of_range_warns(self):
        fit, warn = bd.parse_fit(app(**{**FULL, "fit_path": 11}))
        self.assertIsNone(fit)
        self.assertIn("outside", warn)

    def test_non_integer_warns(self):
        fit, warn = bd.parse_fit(app(**{**FULL, "fit_stack": "high"}))
        self.assertIsNone(fit)
        self.assertIn("not an integer", warn)

    def test_inline_comment_is_stripped(self):
        a = app(**FULL)
        a["fit_role"] = "8   # Tier 1"
        fit, warn = bd.parse_fit(a)
        self.assertIsNone(warn)
        self.assertEqual(fit[1]["fit_role"], 8)

    def test_zero_gates_marks_gated(self):
        fit, _ = bd.parse_fit(app(fit_role=10, fit_stack=10, fit_gates=0, fit_path=10))
        self.assertTrue(fit[2])


class Queue(unittest.TestCase):
    def build(self, apps):
        for a in apps:
            a["_fit"], _ = bd.parse_fit(a)
        return "\n".join(bd.build_queue(apps))

    def test_gated_never_ranked_above_viable(self):
        text = self.build([
            app("applications/gated.md", fit_role=10, fit_stack=10, fit_gates=0, fit_path=10),
            app("applications/ok.md", fit_role=3, fit_stack=3, fit_gates=3, fit_path=3),
        ])
        ranked, gated_block = text.split("**Gated out")
        self.assertIn("ok.md", ranked)
        self.assertNotIn("gated.md", ranked)
        self.assertIn("gated.md", gated_block)

    def test_tie_breaks_on_path(self):
        text = self.build([
            app("applications/cold.md", fit_role=9, fit_stack=9, fit_gates=9, fit_path=3),
            app("applications/warm.md", fit_role=7, fit_stack=7, fit_gates=9, fit_path=7),
        ])
        self.assertLess(text.index("warm.md"), text.index("cold.md"))

    def test_submitted_roles_excluded(self):
        text = self.build([app("applications/done.md", status="submitted", **FULL)])
        self.assertEqual(text, "")

    def test_unscored_listed(self):
        text = self.build([app("applications/new.md")])
        self.assertIn("Unscored (1)", text)


if __name__ == "__main__":
    unittest.main()
