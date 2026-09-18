# 07 - Your turn

**Time:** open-ended
**You will learn:** whatever you build
**You will need:** lessons 00 to 07 finished

Claim one by opening an issue with the "Playground exercise" template, so two
people do not build the same thing. Work on a branch. Open a pull request even
if nobody merges it - the PR is where the interesting conversation happens.

Each exercise names the Copilot feature it is meant to exercise. That is the
point of the exercise, not the code.

## Starter

**1. The last planted problem.** `reconcile()` in `valuation.py` takes an
unweighted mean of the top three comps. Real reconciliation weights the closest,
most recent, least-adjusted sales more heavily. Implement weighting, and add a
test proving the weighted result still falls inside the comp range.
*Practises:* agent mode, test-first.

**2. A listing-status column.** Add `listing_status` to the generator and the
loader so the dataset can hold pending sales and active listings, and make
`screen_comps` exclude anything that is not a closed sale. Notice how the
instructions file you wrote in lesson 04 pushes back if you try to hand-edit the
CSV.
*Practises:* instructions files, data discipline.

**3. Export an adjustment grid.** `python -m collateral_iq export SUBJ-001`
should write a CSV of the grid that could be pasted into a report. Standard
library `csv` only.
*Practises:* inline completions, CLI patterns.

## Intermediate

**4. Subject detail view.** The dashboard has no page for a single subject's
grid, though `/api/value` already returns one. Build it. No frameworks.
*Practises:* the coding agent - this is a well-bounded task, so try delegating it.

**5. A time-adjustment skill.** We have `market-snapshot`, which reports the
trend. Write a skill that goes further: derives the appropriate market-conditions
adjustment for a specific subject from its own submarket's data, explains the
derivation, and writes the paragraph. Test whether your description reliably
triggers it.
*Practises:* skill authoring, description tuning.

**6. A second reviewer agent.** The appraisal reviewer checks the math. Write a
`narrative-reviewer` agent that checks the *prose* - reads a market-conditions
paragraph and flags unsupported claims, advocacy language, and conclusions the
data does not carry.
*Practises:* agent authoring, tool boundaries.

## Harder

**7. Regression-derived adjustments.** The rates in `ADJUSTMENTS` are made up.
Derive GLA and pool adjustments from the comp data itself using a simple ordinary
least squares fit - which you will have to write by hand, because no numpy. Then
compare against the hard-coded constants and write up the difference.
*Practises:* everything, plus the standard-library constraint biting properly.

**8. Confidence, not a point value.** An indicated value with no measure of
confidence is half an answer. Produce a range with a stated basis - comp spread,
count, recency, adjustment magnitude - and surface it on the dashboard. Decide
what you would actually defend, then build that.
*Practises:* using Ask mode to think before using agent mode to build.

**9. Break the repository on purpose.** Plant a subtle bug in `valuation.py` on
a branch - a reversed comparison, an off-by-one in a date window, a threshold
that reads the wrong constant. Then hand the branch to a colleague and see
whether the appraisal-reviewer agent catches it. If it does not, improve the
agent until it does.
*Practises:* the thing that actually matters, which is knowing where these tools
fail.

## When you are done

Write up what you learned in the pull request description, including where
Copilot was wrong and how you noticed. That last part is the most useful thing
you can hand the rest of the team.
