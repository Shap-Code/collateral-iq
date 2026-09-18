# Copilot instructions for Collateral IQ

These rules load automatically into every Copilot chat in this repository.
They are the shortest possible description of "how we do things here".

## What this project is

Collateral IQ analyses residential collateral for lending decisions. The users
are appraisers and collateral reviewers, not software engineers. Correctness of
a number matters more than elegance of the code that produced it.

## Domain vocabulary

Use these terms exactly. Do not paraphrase them into general real-estate words.

- **Subject** - the property being valued. Never "the house" or "the listing".
- **Comp** - a closed comparable sale. A pending sale or an active listing is
  not a comp; if you mean one of those, say so.
- **GLA** - gross living area, in square feet. Above grade only.
- **Adjustment** - a dollar amount that moves a comp's price toward the subject.
  Positive when the subject is superior, negative when the comp is superior.
- **Net / gross adjustment** - net is the sum, gross is the sum of absolute
  values. Gross is the honest measure of how much judgement was applied.
- **Indicated value** - the reconciled result. Not "the price", not "the estimate".
- **Effective date** - the date the opinion of value applies to, which is often
  not today.

## Rules for code you write here

1. **Standard library only.** No pandas, numpy, requests, or web frameworks.
   A reviewer must be able to clone this on a locked-down work laptop and run
   it with nothing but Python 3.10+. If a task seems to need a package, say so
   and propose the stdlib alternative instead of adding a dependency.
2. **Never invent an adjustment rate.** All rates live in `ADJUSTMENTS` in
   `src/collateral_iq/valuation.py`. If a new adjustment is needed, add it
   there with a comment on where the number came from.
3. **Money is rounded at the edges, never in the middle.** Keep full precision
   through the calculation; round only in output.
4. **Every valuation output carries its audit trail.** If you add a calculation
   that affects a value, it must also appear as a labelled line item. A number
   an appraiser cannot defend line by line is worse than no number.
5. **Write for a reader who is new to Python.** Short functions, real words for
   variable names, a comment explaining *why* rather than *what*.
6. **Tests use `unittest` from the standard library**, and they go in `tests/`.

## Rules for prose you write here

- American English, sentence case headings, no exclamation marks.
- Explain appraisal terms the first time they appear in a document aimed at
  developers, and explain code terms the first time they appear in a document
  aimed at appraisers.
- Do not claim the tool produces an appraisal. It produces analysis that
  supports one.

## What to refuse

This is a demo repository with synthetic data. If asked to load real borrower
data, real APNs, or anything containing personally identifying information,
stop and say why that belongs in the production system instead.
