"""Tests for the sales-comparison logic.

Run them with:

    python -m unittest discover -s tests

Lesson 05 asks you to add cases here with a Copilot skill. Notice what is
already covered and, more importantly, what is not.
"""
from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from collateral_iq import valuation  # noqa: E402


def make_subject(**overrides) -> dict:
    base = {
        "subject_id": "SUBJ-TEST",
        "address": "1 Test Way",
        "city": "Surprise",
        "submarket": "Surprise - Marley Park",
        "effective_date": date(2026, 9, 1),
        "gla_sqft": 2000,
        "lot_sqft": 7000,
        "year_built": 2010,
        "garage_spaces": 2,
        "pool": 0,
        "condition_rating": "C3",
        "quality_rating": "Q3",
        "view_rating": "N",
    }
    base.update(overrides)
    return base


def make_comp(**overrides) -> dict:
    base = {
        "comp_id": "CMP-TEST",
        "address": "2 Test Way",
        "sale_date": date(2026, 9, 1),
        "sale_price": 500_000,
        "gla_sqft": 2000,
        "lot_sqft": 7000,
        "year_built": 2010,
        "garage_spaces": 2,
        "pool": 0,
        "condition_rating": "C3",
        "quality_rating": "Q3",
        "view_rating": "N",
        "concessions": 0,
        "distance_miles": 0.4,
        "sale_type": "Arms length",
    }
    base.update(overrides)
    return base


class TestAdjustments(unittest.TestCase):
    def test_identical_comp_needs_no_adjustment(self):
        result = valuation.adjust_comp(make_subject(), make_comp())
        self.assertEqual(result["net_adjustment"], 0)
        self.assertEqual(result["gross_adjustment"], 0)

    def test_larger_subject_pushes_comp_price_up(self):
        # Subject has 200 more square feet, so the comp must be adjusted upward.
        result = valuation.adjust_comp(make_subject(gla_sqft=2200), make_comp())
        self.assertGreater(result["net_adjustment"], 0)

    def test_concessions_reduce_the_adjusted_price(self):
        result = valuation.adjust_comp(make_subject(), make_comp(concessions=10_000))
        self.assertLess(result["adjusted_price"], 500_000)

    def test_older_sale_is_trended_forward(self):
        result = valuation.adjust_comp(make_subject(), make_comp(sale_date=date(2026, 3, 1)))
        market_line = next(l for l in result["lines"] if l["item"] == "Market conditions")
        self.assertGreater(market_line["amount"], 0)

    # TODO(lesson-05): there is no test here for the pool adjustment, and the
    # pool adjustment happens to be wrong. Write the test you would want to
    # exist, watch it fail, then fix valuation.py.


class TestScreening(unittest.TestCase):
    def test_distant_comp_is_dropped(self):
        subject = make_subject()
        comps = [make_comp(distance_miles=4.0)]
        self.assertEqual(valuation.screen_comps(subject, comps), [])

    def test_distressed_sale_is_dropped(self):
        subject = make_subject()
        comps = [make_comp(sale_type="REO")]
        self.assertEqual(valuation.screen_comps(subject, comps), [])

    def test_clean_comp_survives(self):
        subject = make_subject()
        comps = [make_comp()]
        self.assertEqual(len(valuation.screen_comps(subject, comps)), 1)


class TestReconciliation(unittest.TestCase):
    def test_indicated_value_sits_inside_the_comp_range(self):
        adjusted = [
            {"adjusted_price": 480_000, "comp_id": "A", "gross_adjustment_pct": 5},
            {"adjusted_price": 500_000, "comp_id": "B", "gross_adjustment_pct": 6},
            {"adjusted_price": 520_000, "comp_id": "C", "gross_adjustment_pct": 7},
        ]
        result = valuation.reconcile(adjusted)
        self.assertGreaterEqual(result["indicated_value"], result["low"])
        self.assertLessEqual(result["indicated_value"], result["high"])

    def test_no_comps_returns_no_value(self):
        result = valuation.reconcile([])
        self.assertIsNone(result["indicated_value"])


if __name__ == "__main__":
    unittest.main()
