# Lab 2 - Skills

**Time:** 30 minutes
**This isolates:** `SKILL.md`, its reference file, and its bundled script
**Pairs with:** [Lesson 05 - Skills](../05-skills.md)

Lab 1 showed instructions changing *how* Copilot writes. This one shows a skill
changing *what work it does before writing*. The difference is larger and more
obvious, which is why this is the lab to run first if you only have time for one.

---

## Prompt A - the market-conditions paragraph

Run in both windows, in **Agent** mode. Agent mode matters here: a skill that
bundles a script needs permission to run it.

> Write the market-conditions paragraph for Goodyear - Estrella that would go in
> a report with an effective date of September 1, 2026. Include the monthly rate
> of change we should be applying.

### What to look for

| Criterion | Why it matters |
| --- | --- |
| Did it **run anything**? | The baseline writes a paragraph from nothing. The customized run should execute `.github/skills/market-snapshot/scripts/market_stats.py`. Watch the terminal, not just the text. |
| Is the monthly rate **derived or invented**? | The script computes it from `market_monthly.csv`. Compare the number in each paragraph against what the script actually prints. |
| Does it cite absorption and days on market? | The skill requires all three. |
| Does it flag that the constant in `valuation.py` may be stale? | The script prints a mismatch warning. Did the paragraph notice? |
| Three sentences, in the order the skill specifies? | |

Run the script yourself so you know the truth:

```bash
python .github/skills/market-snapshot/scripts/market_stats.py "Goodyear - Estrella"
```

Then hold both paragraphs against it. This is the moment the lab is built for:
one paragraph is checkable against a computation and the other is prose that
sounds like an appraiser wrote it.

**A caution.** The baseline paragraph will often read *better*. It will be
fluent, confident, and professionally toned. That is the hazard, not a point
against the exercise. Fluency and support are unrelated.

---

## Prompt B - the refusal test

The most valuable thing in our `comp-selection` skill is the section headed
"when to push back instead of producing a number". Run in both windows:

> Value SUBJ-004 using whatever comps are available and give me a single number
> I can send to the client this afternoon.

### What to look for

| Criterion | |
| --- | --- |
| Does it produce a number without qualification? | |
| Does it report how many comps survived screening? | |
| Does it check bracketing - superior and inferior on GLA? | |
| Does it **decline** if the adjusted spread is too wide? | SUBJ-004's spread is above our 15% threshold. The skill says do not produce a value in that case. |
| Does it mention the threshold it applied? | |

An assistant that gives you a number every single time you ask is not a
colleague. Getting Copilot to say "not from this comp set, and here is why" is
the hardest and most useful thing in this repository.

---

## Prompt C - the loading test

This one demonstrates the mechanism rather than the output. In the real
repository, ask three questions and watch which skill loads:

> How do I make the dashboard table sortable?

> Why was that comp excluded from the grid?

> Is the market still appreciating in Vistancia?

The first should load **neither** skill. The second should load
`comp-selection`. The third should load `market-snapshot`.

That is progressive disclosure working: twenty skills could be installed and the
CSS question would pay for none of them. Only names and descriptions stay
resident; the body loads when the description matches, and the reference file or
script loads only if the body points at it.

If the wrong skill loads, or none does, the fix is the **description**, not the
body. The description is the entire triggering mechanism. Open
`.github/skills/comp-selection/SKILL.md` and look at how many different phrasings
its description names - screening, bracketing, why a comp was excluded,
defending a set to an underwriter. Each one is a hook for a way somebody might
actually ask.

---

## What to write down

Beyond the scorecard:

**How far off was the baseline's invented monthly rate?**

Put the two numbers side by side, then work out what that percentage does to an
indicated value over a nine-month-old sale on a $500,000 comp. A rate that is
wrong by a quarter of a point is not an academic problem; it is several thousand
dollars on a number somebody signs.

That arithmetic is the whole case for skills, in one line, and it is the slide
worth putting in front of anyone who thinks this is a developer toy.

Next: [Lab 3 - Agents](lab-3-agents.md)
