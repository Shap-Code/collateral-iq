---
name: comp-selection
description: Select and defend comparable sales for a subject property in this repository, including screening, ranking, and writing the comp-selection narrative. Use this skill whenever the user asks about choosing comps, why a comp was excluded, comp screening thresholds, adjustment grids, bracketing, or defending a comp set to a reviewer or underwriter.
---

# Comp selection

Use this when someone needs to choose, defend, or explain a comparable-sales
set in Collateral IQ.

## The workflow

1. **Load the subject.** `get_subject(subject_id)` in
   `src/collateral_iq/loader.py`. Note the GLA, effective date, submarket, and
   condition/quality ratings before looking at any comp.

2. **Screen.** Run `screen_comps()`. The thresholds live in the `SCREENS` dict
   in `src/collateral_iq/valuation.py`. Report how many candidates fell out and
   why - a comp set that survives screening by a hair is a different story from
   one that survives comfortably.

3. **Adjust and rank.** `adjust_comp()` then `rank_comps()`. Ranking is by gross
   adjustment percentage, because gross adjustment is the honest measure of how
   much appraiser judgement went into the number.

4. **Check bracketing.** The chosen comps should bracket the subject on GLA and
   on the main value drivers - at least one superior and one inferior on each.
   A comp set where every comp is superior produces a value that leans, and a
   reviewer will say so. If the set does not bracket, say that plainly rather
   than proceeding.

5. **Write the narrative.** See `references/adjustment-grid.md` for the sentence
   patterns this team uses and for what each adjustment line has to justify.

## When to push back instead of producing a number

Say so explicitly, and do not produce an indicated value, if:

- Fewer than three comps survive screening.
- Every surviving comp is more than 180 days old in a market moving more than
  0.3% a month.
- The gross adjustment on a primary comp exceeds 25%.
- The comp set does not bracket the subject's GLA.

These are the same conditions `portfolio_risk_flags()` in `metrics.py` checks.
If you change one here, change it there too.

## What not to do

- Do not widen a screening threshold to make a comp fit. Widening a threshold
  is a decision about the whole market, not about one file, and it belongs in
  `SCREENS` with a comment explaining the market conditions that justify it.
- Do not use a distressed sale (REO, short sale, relocation) as a primary comp
  in an arms-length assignment.
- Do not average your way out of a wide spread. A 25% spread between adjusted
  comps means the adjustments are wrong, not that the middle is right.
