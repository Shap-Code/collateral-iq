# Adjustment grid reference

Read this when writing the narrative that accompanies a comp set, or when
adding a new adjustment line to `valuation.py`.

## What each line has to justify

| Line | Support the reader expects |
| --- | --- |
| Market conditions | The monthly rate, and the source: paired sales, median $/sqft trend, or the submarket roll-up in `market_monthly.csv`. |
| Concessions | The dollar amount from the settlement statement, applied in full. |
| Gross living area | The $/sqft rate, and confirmation it is below the market's own $/sqft (adjusting at full market rate double-counts land). |
| Lot size | Only where lot size actually drives price locally. In tract subdivisions it often does not. |
| Garage | Per-space rate, with a note on whether the space is attached. |
| Pool | A single flat amount. Pools rarely return their cost in the West Valley, which is why this number is well below installed cost. |
| Age | Effective age, not chronological, when the two differ. |
| Condition / Quality | The UAD rating step, plus one sentence on what physically differs. |
| View | Beneficial or adverse relative to the subject, never in the abstract. |

## Sentence patterns

Use these shapes. They are dull on purpose; a narrative that reads as
distinctive prose reads as advocacy to a reviewer.

- Selection: "Comp 2 was selected as the most similar sale, requiring a gross
  adjustment of 8.4% and bracketing the subject on gross living area."
- Exclusion: "A closed sale at 15220 W Aster Dr was considered and excluded; the
  transaction was a relocation sale and therefore not arms-length."
- Market conditions: "Sales in Surprise - Marley Park have appreciated
  approximately 0.35% monthly over the trailing twelve months, supported by the
  median price-per-square-foot trend for the submarket."
- Reconciliation: "Greatest weight was given to Comps 1 and 3, which required
  the least adjustment and are the most recent closings within the subject's
  subdivision."

## Sign convention, stated once

Every adjustment moves the **comp** toward the **subject**.

- Subject superior to comp -> adjustment is **positive** (add to the comp).
- Comp superior to subject -> adjustment is **negative** (subtract from the comp).

If a line in `valuation.py` does not follow this, it is a bug even if the
resulting value looks reasonable.
