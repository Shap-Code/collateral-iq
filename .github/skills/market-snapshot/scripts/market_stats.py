"""Print trend, absorption, and implied monthly rate of change for a submarket.

    python .github/skills/market-snapshot/scripts/market_stats.py "Peoria - Vistancia"

Bundled with the market-snapshot skill. Standard library only, like everything
else in this repository.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))

from collateral_iq import metrics  # noqa: E402


def implied_monthly_rate(rows: list[dict]) -> float:
    """Compound monthly rate of change across the window, as a decimal."""
    first, last = rows[0]["median_ppsf"], rows[-1]["median_ppsf"]
    periods = len(rows) - 1
    if periods <= 0 or first <= 0:
        return 0.0
    return (last / first) ** (1 / periods) - 1


def main(argv: list[str]) -> int:
    known = [r["submarket"] for r in metrics.price_per_sqft_by_submarket()]
    if not argv:
        print("Usage: market_stats.py <submarket>\n\nKnown submarkets:")
        for name in known:
            print(f"  - {name}")
        return 1

    submarket = argv[0]
    rows = metrics.market_trend(submarket, months=12)
    if not rows:
        print(f"No data for {submarket!r}. Known submarkets: {', '.join(known)}")
        return 1
    if len(rows) < 12:
        print(f"WARNING: only {len(rows)} months available. "
              "A trend from fewer than 12 months is not defensible.\n")

    rate = implied_monthly_rate(rows)
    latest = next(a for a in metrics.absorption_summary() if a["submarket"] == submarket)

    print(f"{submarket}")
    print(f"  Window                 {rows[0]['month']} to {rows[-1]['month']} ({len(rows)} months)")
    print(f"  Median $/sqft          {rows[0]['median_ppsf']:.2f} -> {rows[-1]['median_ppsf']:.2f}")
    print(f"  Implied monthly rate   {rate * 100:+.2f}% per month")
    print(f"  Months of supply       {latest['months_supply']}  ({latest['condition']})")
    print(f"  Median days on market  {latest['median_dom']}")

    from collateral_iq.valuation import ADJUSTMENTS
    configured = ADJUSTMENTS["monthly_market_trend"]
    gap = abs(rate - configured) * 100
    print(f"\n  Configured trend in valuation.py: {configured * 100:.2f}% per month")
    if gap > 0.1:
        print(f"  MISMATCH: differs by {gap:.2f} percentage points. The constant looks stale.")
    else:
        print("  Consistent with the configured constant.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
