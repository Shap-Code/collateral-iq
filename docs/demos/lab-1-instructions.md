# Lab 1 - Instructions

**Time:** 25 minutes
**You isolates:** `.github/copilot-instructions.md` and the scoped `.instructions.md` files
**Pairs with:** [Lesson 04 - Instructions](../04-instructions.md)

Two windows open: `collateral-iq-baseline` and `collateral-iq`. Three runs of
each prompt in each window. Record in `results/`.

---

## Prompt A - the vocabulary test

Run this in both windows, in **Ask** mode:

> I need to add a function that pulls together every recent sale near SUBJ-002
> that we could use to support a value. Where should it go and what should it
> look like?

### What to look for

| Criterion | Why it matters |
| --- | --- |
| Uses the word **comp** for a closed sale | The baseline will say "properties", "listings", "similar homes". Those are three different things in our work and only one of them is evidence. |
| Distinguishes closed sales from active listings | If it happily includes listings, it has not understood what a comp is. |
| Uses the existing `load_comps()` rather than opening the CSV itself | Knowing the codebase's own front door is context, not intelligence. |
| Standard library only | The baseline will reach for pandas within two sentences. |
| Puts it in `valuation.py` or `metrics.py`, not somewhere arbitrary | |

The vocabulary point is the one to dwell on in the group session. An assistant
that calls an active listing a comp will eventually put one in a report.

---

## Prompt B - the invented number test

This is the sharper of the two. Run in both windows, in **Ask** mode:

> Add a fireplace adjustment to the valuation model. What should the rate be?

### What to look for

| Criterion | Why it matters |
| --- | --- |
| Does it **invent a dollar amount**? | The baseline almost always will - $3,000, $5,000, something plausible-sounding with no support. A confident invented number is the single most dangerous failure mode in this whole domain. |
| Does it put the rate in `ADJUSTMENTS`? | Our rule is one place, always. |
| Does it say where the number should come from? | Paired sales, local market analysis, "you need to derive this" - any of those is the right answer. |
| Does it add a comment recording the source? | Required by our instructions. |

A customized run that still invents a number, but puts it in the right place
with a comment saying it needs deriving, is a partial win. Record it as a
partial win rather than rounding it up.

---

## Prompt C - the scoped instructions test

This one shows that `applyTo` globs actually do something. Run in both windows:

> Write a short section for the README explaining what the flags command does.

Then, in the **real repository only**, open `.github/instructions/docs.instructions.md`
and read it before judging the output.

### What to look for

| Criterion | |
| --- | --- |
| Does it avoid the word "simply"? | Our docs instructions forbid it explicitly. |
| Code fences named with a language | |
| Leads with what the reader can do, no preamble about importance | |

Now the control that proves the scoping works. In the real repository, ask the
same question but about a Python file:

> Write a docstring for the flags command handler in __main__.py.

The Markdown rules should not be visible in the answer, because
`docs.instructions.md` only applies to `**/*.md`. The Python rules should be -
type hints, a first line saying what the caller gets back. Scoping means a rule
loads where it is relevant and stays out of the way everywhere else.

---

## What to write down

Fill in the scorecard, then answer the question that actually matters:

**Which of these differences would have reached a client?**

The vocabulary slip probably would have - it reads fine to anyone who is not an
appraiser. The invented fireplace rate definitely would have. The pandas import
would not, because the code would have failed in an obvious way on somebody's
machine.

That distinction is the argument for instructions files. They are not about
making Copilot write prettier code. They are about closing the failure modes
that look fine on the way out the door.

Next: [Lab 2 - Skills](lab-2-skills.md)
