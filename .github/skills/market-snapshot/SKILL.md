---
name: market-snapshot
description: Produce a market-conditions summary for a submarket in this repository - trend, absorption, days on market - and turn it into the market-conditions paragraph an appraisal report needs. Use whenever the user asks about market trends, months of supply, absorption rates, whether a market is appreciating, time adjustments, or the 1004MC-style market analysis for a submarket.
---

# Market snapshot

Use this to answer "what is the market doing here" for one submarket, and to
turn the answer into the paragraph that supports a market-conditions adjustment.

## Getting the numbers

Run the bundled script rather than writing new analysis code:

```bash
python .github/skills/market-snapshot/scripts/market_stats.py "Peoria - Vistancia"
```

It prints trailing trend, absorption, and the implied monthly rate of change,
reading from `data/market_monthly.csv` and `data/comps.csv`. Pass no argument to
see the list of submarkets.

## Reading the result

- **Months of supply** under 3 favours sellers, over 6 favours buyers. Between 3
  and 6, a market-conditions adjustment is hardest to defend and should be small
  or absent.
- **Implied monthly rate** is the figure that belongs in
  `ADJUSTMENTS["monthly_market_trend"]`. If the script's number and the constant
  in `valuation.py` disagree by more than 0.1 percentage points, flag it. The
  constant is stale.
- **Days on market** moving in the opposite direction from price is the useful
  signal. Rising price with rising DOM usually means the market has turned and
  the closed sales have not caught up yet. Say so.

## Writing the paragraph

Three sentences, in this order: what the trend is, what supports it, what it
means for the adjustment.

> The subject's submarket has shown median price-per-square-foot appreciation of
> approximately 0.44% per month over the trailing twelve months. Months of
> supply currently stands at 2.1 with a median 29 days on market, indicating
> continued demand in excess of supply. A market-conditions adjustment of 0.44%
> per month has therefore been applied to closed sales based on their
> contract-to-effective-date interval.

## Limits

This dataset is synthetic and monthly. Do not present it as a substitute for an
MLS export, and do not compute a trend from fewer than twelve months - the
script will warn you, and the warning is not decorative.
