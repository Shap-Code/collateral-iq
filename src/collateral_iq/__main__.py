"""Command line entry point.

    python -m collateral_iq value SUBJ-001
    python -m collateral_iq flags
    python -m collateral_iq market "Peoria - Vistancia"
    python -m collateral_iq serve
"""
from __future__ import annotations

import json
import sys

from . import metrics, valuation


def _money(value) -> str:
    return "n/a" if value is None else f"${value:,.0f}"


def cmd_value(subject_id: str) -> None:
    result = valuation.value_subject(subject_id)
    subject = result["subject"]
    rec = result["reconciliation"]
    print(f"\n{subject['address']}, {subject['city']}  ({subject['subject_id']})")
    print(f"{subject['submarket']}  |  {subject['gla_sqft']:,} sqft  |  effective {subject['effective_date']}")
    print(f"Comps: {result['candidates_considered']} considered, "
          f"{result['candidates_after_screening']} passed screening\n")
    print(f"{'Comp':<10} {'Sale date':<12} {'Sale price':>12} {'Net adj':>10} {'Gross %':>9} {'Adjusted':>12}")
    print("-" * 69)
    for row in result["grid"][:5]:
        print(f"{row['comp_id']:<10} {row['sale_date']:<12} {_money(row['sale_price']):>12} "
              f"{_money(row['net_adjustment']):>10} {row['gross_adjustment_pct']:>8}% "
              f"{_money(row['adjusted_price']):>12}")
    print("-" * 69)
    print(f"\nIndicated value: {_money(rec.get('indicated_value'))}   "
          f"(range {_money(rec.get('low'))} - {_money(rec.get('high'))}, "
          f"spread {rec.get('spread_pct')}%)")
    print(f"Comps relied on: {', '.join(rec.get('used', [])) or 'none'}\n")


def cmd_flags() -> None:
    print(f"\n{'Subject':<10} {'Risk':<8} {'Value':>12}  Reasons")
    print("-" * 78)
    for row in metrics.portfolio_risk_flags():
        reasons = "; ".join(row["reasons"]) or "-"
        print(f"{row['subject_id']:<10} {row['risk']:<8} {_money(row['indicated_value']):>12}  {reasons}")
    print()


def cmd_market(submarket: str) -> None:
    rows = metrics.market_trend(submarket)
    if not rows:
        print(f"No market data for {submarket!r}. Known submarkets:")
        for row in metrics.price_per_sqft_by_submarket():
            print(f"  - {row['submarket']}")
        return
    print(f"\n{submarket}")
    print(f"{'Month':<9} {'$/sqft':>9} {'DOM':>5} {'Supply':>8}  Trend")
    print("-" * 52)
    peak = max(r["median_ppsf"] for r in rows)
    for row in rows:
        bar = "#" * int(row["median_ppsf"] / peak * 20)
        print(f"{row['month']:<9} {row['median_ppsf']:>9.2f} {row['median_dom']:>5} "
              f"{row['months_supply']:>8}  {bar}")
    print()


def cmd_serve() -> None:
    from .server import serve
    serve()


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help", "help"}:
        print(__doc__)
        return 0
    command, *rest = argv
    if command == "value":
        cmd_value(rest[0] if rest else "SUBJ-001")
    elif command == "flags":
        cmd_flags()
    elif command == "market":
        cmd_market(rest[0] if rest else "Peoria - Vistancia")
    elif command == "serve":
        cmd_serve()
    elif command == "json":
        print(json.dumps(metrics.dashboard_payload(), indent=2, default=str))
    else:
        print(f"Unknown command {command!r}\n")
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
