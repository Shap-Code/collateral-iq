"""Sales-comparison approach: pick comps, adjust them, reconcile to a value.

This is a teaching model, not a production appraisal engine. The adjustment
amounts below are flat rates chosen for readability. A real engine would derive
them from paired-sales analysis or a regression on the local market.

Read this file top to bottom before Lesson 06 - you will be asking a Copilot
agent to review it, and it is much more interesting if you already have an
opinion about what is wrong.
"""
from __future__ import annotations

from datetime import date

from .loader import get_subject, load_comps

# ---------------------------------------------------------------------------
# Adjustment rates. One place to change them, so the reasoning stays auditable.
# ---------------------------------------------------------------------------
ADJUSTMENTS = {
    "price_per_sqft_gla": 78.0,      # $ per square foot of living-area difference
    "price_per_sqft_lot": 4.5,       # $ per square foot of lot-size difference
    "per_garage_space": 9_000.0,
    "pool": 31_000.0,
    "per_year_of_age": 1_200.0,
    "per_condition_step": 14_000.0,  # C3 -> C4 is one step
    "per_quality_step": 16_000.0,    # Q3 -> Q4 is one step
    "view_beneficial": 12_000.0,
    "view_adverse": -9_000.0,
    "monthly_market_trend": 0.0035,  # 0.35% per month of appreciation
}

# How far a comp can stray before we stop trusting it.
SCREENS = {
    "max_age_days": 270,
    "max_distance_miles": 1.5,
    "max_gla_variance": 0.25,        # +/- 25% of subject living area
    "allowed_sale_types": {"Arms length"},
}

CONDITION_SCALE = {"C1": 1, "C2": 2, "C3": 3, "C4": 4, "C5": 5, "C6": 6}
QUALITY_SCALE = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4, "Q5": 5, "Q6": 6}


def screen_comps(subject: dict, comps: list[dict]) -> list[dict]:
    """Drop comps that fail the basic credibility screens in SCREENS."""
    kept = []
    for comp in comps:
        age_days = (subject["effective_date"] - comp["sale_date"]).days
        gla_variance = abs(comp["gla_sqft"] - subject["gla_sqft"]) / subject["gla_sqft"]
        if age_days > SCREENS["max_age_days"]:
            continue
        if comp["distance_miles"] > SCREENS["max_distance_miles"]:
            continue
        if gla_variance > SCREENS["max_gla_variance"]:
            continue
        if comp["sale_type"] not in SCREENS["allowed_sale_types"]:
            continue
        kept.append(comp)
    return kept


def adjust_comp(subject: dict, comp: dict) -> dict:
    """Return the comp's adjusted sale price plus a line-by-line audit trail.

    Convention: every adjustment moves the COMP toward the SUBJECT.
    If the subject is better, the adjustment is positive. If the comp is
    better, the adjustment is negative.
    """
    lines: list[tuple[str, float]] = []

    # Market conditions (time). Older sales get trended forward to the
    # effective date of the appraisal.
    months_old = (subject["effective_date"] - comp["sale_date"]).days / 30.44
    lines.append((
        "Market conditions",
        comp["sale_price"] * ADJUSTMENTS["monthly_market_trend"] * months_old,
    ))

    # Seller concessions come straight off the top.
    lines.append(("Concessions", -float(comp["concessions"])))

    # Living area.
    lines.append((
        "Gross living area",
        (subject["gla_sqft"] - comp["gla_sqft"]) * ADJUSTMENTS["price_per_sqft_gla"],
    ))

    # Site size.
    lines.append((
        "Lot size",
        (subject["lot_sqft"] - comp["lot_sqft"]) * ADJUSTMENTS["price_per_sqft_lot"],
    ))

    # Garage.
    lines.append((
        "Garage",
        (subject["garage_spaces"] - comp["garage_spaces"]) * ADJUSTMENTS["per_garage_space"],
    ))

    # Pool.
    # TODO(lesson-06): the sign convention here does not match the rule in this
    # docstring. Find it with the appraisal-reviewer agent before you fix it.
    lines.append((
        "Pool",
        (comp["pool"] - subject["pool"]) * ADJUSTMENTS["pool"],
    ))

    # Effective age.
    lines.append((
        "Age",
        (subject["year_built"] - comp["year_built"]) * ADJUSTMENTS["per_year_of_age"],
    ))

    # Condition and quality ratings. Lower number = better, so the subtraction
    # is reversed relative to the numeric fields above.
    lines.append((
        "Condition",
        (CONDITION_SCALE[comp["condition_rating"]] - CONDITION_SCALE[subject["condition_rating"]])
        * ADJUSTMENTS["per_condition_step"],
    ))
    lines.append((
        "Quality",
        (QUALITY_SCALE[comp["quality_rating"]] - QUALITY_SCALE[subject["quality_rating"]])
        * ADJUSTMENTS["per_quality_step"],
    ))

    # View.
    view_delta = 0.0
    if comp["view_rating"] == "B" and subject["view_rating"] != "B":
        view_delta = -ADJUSTMENTS["view_beneficial"]
    elif subject["view_rating"] == "B" and comp["view_rating"] != "B":
        view_delta = ADJUSTMENTS["view_beneficial"]
    elif comp["view_rating"] == "A" and subject["view_rating"] != "A":
        view_delta = -ADJUSTMENTS["view_adverse"]
    lines.append(("View", view_delta))

    gross = sum(abs(amount) for _, amount in lines)
    net = sum(amount for _, amount in lines)
    adjusted = comp["sale_price"] + net

    return {
        "comp_id": comp["comp_id"],
        "address": comp["address"],
        "sale_date": comp["sale_date"].isoformat(),
        "sale_price": comp["sale_price"],
        "lines": [{"item": item, "amount": round(amount)} for item, amount in lines],
        "net_adjustment": round(net),
        "gross_adjustment": round(gross),
        "net_adjustment_pct": round(net / comp["sale_price"] * 100, 1),
        "gross_adjustment_pct": round(gross / comp["sale_price"] * 100, 1),
        "adjusted_price": round(adjusted, -2),
        "distance_miles": comp["distance_miles"],
    }


def rank_comps(subject: dict, adjusted: list[dict]) -> list[dict]:
    """Best comp first. Smaller gross adjustment means less appraiser judgement."""
    return sorted(adjusted, key=lambda a: a["gross_adjustment_pct"])


def reconcile(adjusted: list[dict], count: int = 3) -> dict:
    """Blend the top comps into a single indicated value.

    TODO(lesson-08): this is an unweighted mean of the top `count` comps.
    Real reconciliation weights the closest, most recent, least-adjusted sales
    more heavily. Ask Copilot agent mode to implement weighting - and to add
    tests proving the weighted result still sits inside the comp range.
    """
    if not adjusted:
        return {"indicated_value": None, "used": [], "note": "No comps survived screening."}

    used = adjusted[:count]
    prices = [a["adjusted_price"] for a in used]
    indicated = sum(prices) / len(prices)
    return {
        "indicated_value": round(indicated, -3),
        "low": min(prices),
        "high": max(prices),
        "spread_pct": round((max(prices) - min(prices)) / indicated * 100, 1),
        "used": [a["comp_id"] for a in used],
    }


def value_subject(subject_id: str, comp_count: int = 3) -> dict:
    """End-to-end: screen, adjust, rank, reconcile. This is the public entry point."""
    subject = get_subject(subject_id)
    candidates = load_comps(subject_id)
    screened = screen_comps(subject, candidates)
    adjusted = rank_comps(subject, [adjust_comp(subject, c) for c in screened])
    result = reconcile(adjusted, count=comp_count)
    return {
        "subject": {
            "subject_id": subject["subject_id"],
            "address": subject["address"],
            "city": subject["city"],
            "submarket": subject["submarket"],
            "gla_sqft": subject["gla_sqft"],
            "effective_date": subject["effective_date"].isoformat(),
        },
        "candidates_considered": len(candidates),
        "candidates_after_screening": len(screened),
        "reconciliation": result,
        "grid": adjusted[:6],
    }
