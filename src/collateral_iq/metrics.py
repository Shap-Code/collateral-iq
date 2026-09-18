"""Business-intelligence roll-ups across the whole portfolio.

Valuation answers "what is this house worth". Metrics answers the questions a
chief appraiser or a lender's collateral desk asks: where is the market moving,
which submarkets are thinning out, and which of our own reports look risky.
"""
from __future__ import annotations

from collections import defaultdict
from statistics import mean, median

from .loader import load_comps, load_market, load_subjects
from .valuation import value_subject


def price_per_sqft_by_submarket() -> list[dict]:
    """Median $/sqft of closed sales, grouped by submarket."""
    buckets: dict[str, list[float]] = defaultdict(list)
    for comp in load_comps():
        buckets[comp["submarket"]].append(comp["sale_price"] / comp["gla_sqft"])
    rows = [
        {
            "submarket": submarket,
            "median_ppsf": round(median(values), 2),
            "sales": len(values),
        }
        for submarket, values in buckets.items()
    ]
    return sorted(rows, key=lambda r: r["median_ppsf"], reverse=True)


def market_trend(submarket: str, months: int = 12) -> list[dict]:
    """The last N months of median $/sqft for one submarket, oldest first."""
    rows = [r for r in load_market() if r["submarket"] == submarket]
    rows.sort(key=lambda r: r["month"])
    return [
        {
            "month": r["month"],
            "median_ppsf": r["median_ppsf"],
            "median_dom": r["median_dom"],
            "months_supply": r["months_supply"],
            "closed_sales": r["closed_sales"],
        }
        for r in rows[-months:]
    ]


def absorption_summary() -> list[dict]:
    """Most recent month's supply and days-on-market per submarket.

    Months of supply under 3 is generally a seller's market; over 6 is a
    buyer's market. Between the two, market-conditions adjustments are the
    hardest to defend, which is worth flagging.
    """
    latest: dict[str, dict] = {}
    for row in load_market():
        current = latest.get(row["submarket"])
        if current is None or row["month"] > current["month"]:
            latest[row["submarket"]] = row

    out = []
    for submarket, row in latest.items():
        supply = row["months_supply"]
        if supply < 3:
            condition = "Seller's market"
        elif supply > 6:
            condition = "Buyer's market"
        else:
            condition = "Balanced"
        out.append({
            "submarket": submarket,
            "month": row["month"],
            "months_supply": supply,
            "median_dom": row["median_dom"],
            "condition": condition,
        })
    return sorted(out, key=lambda r: r["months_supply"])


def portfolio_risk_flags() -> list[dict]:
    """Run every subject and flag the ones a reviewer should look at first.

    These thresholds are the quality checks most review appraisers apply by
    habit. Encoding them is the whole point of the tool: the reviewer's
    attention goes to the four files that need it, not all forty.
    """
    flags = []
    for subject in load_subjects():
        result = value_subject(subject["subject_id"])
        rec = result["reconciliation"]
        reasons = []

        if result["candidates_after_screening"] < 5:
            reasons.append(
                f"Thin comp set ({result['candidates_after_screening']} survived screening)"
            )
        if rec.get("spread_pct") is not None and rec["spread_pct"] > 15:
            reasons.append(f"Wide adjusted range ({rec['spread_pct']}% spread)")

        worst_gross = max((g["gross_adjustment_pct"] for g in result["grid"][:3]), default=0)
        if worst_gross > 25:
            reasons.append(f"Heavy adjustments (gross {worst_gross}% on a primary comp)")

        flags.append({
            "subject_id": subject["subject_id"],
            "address": subject["address"],
            "submarket": subject["submarket"],
            "indicated_value": rec.get("indicated_value"),
            "risk": "Review" if reasons else "Clear",
            "reasons": reasons,
        })
    return sorted(flags, key=lambda f: (f["risk"] != "Review", f["subject_id"]))


def dashboard_payload() -> dict:
    """Everything the web dashboard needs, in one call."""
    ppsf = price_per_sqft_by_submarket()
    return {
        "generated_for": "Collateral IQ demo portfolio",
        "subject_count": len(load_subjects()),
        "comp_count": len(load_comps()),
        "average_ppsf": round(mean(r["median_ppsf"] for r in ppsf), 2),
        "price_per_sqft": ppsf,
        "absorption": absorption_summary(),
        "flags": portfolio_risk_flags(),
        "trend": {
            row["submarket"]: market_trend(row["submarket"]) for row in ppsf
        },
    }
