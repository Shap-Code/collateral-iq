# Lab 3 - Agents

**Time:** 30 minutes
**This isolates:** `.agent.md` - a persona, a point of view, and a tool boundary
**Pairs with:** [Lesson 06 - Custom agents](../06-agents.md)

Labs 1 and 2 compared two windows. This one is different: both comparisons
happen inside the real repository, because what you are isolating is *which
agent you selected*, not whether the repo is customized.

Run the baseline comparison for Prompt A anyway - it is worth seeing once.

---

## Prompt A - finding the planted bug

`valuation.py` has a reversed sign in the pool adjustment. It does not crash, it
does not fail any test, and it changes indicated values.

Run this **three ways**:

1. In the **baseline window**, plain Agent mode.
2. In the **real repository**, plain Agent mode.
3. In the **real repository**, with **appraisal-reviewer** selected from the
   agent dropdown.

> Review the adjustment logic in src/collateral_iq/valuation.py. Is it correct?

### What to look for

| Criterion | 1. Baseline | 2. Repo, plain | 3. Repo, reviewer |
| --- | --- | --- | --- |
| Found the pool sign reversal | | | |
| Explained it in appraisal terms, not just "inconsistent comparison" | | | |
| Quantified the effect on indicated value | | | |
| Grouped findings as Material / Defensibility / Housekeeping | | | |
| Stopped without editing the file | | | |
| Kept the noise down - did not pad with style nitpicks | | | |

Run 1 will most likely comment on code style and miss the bug entirely, because
nothing in the baseline says what an adjustment is supposed to do. Run 2 has a
better chance - the instructions file and the `comp-selection` skill's reference
sheet both state the sign convention. Run 3 should get there directly and tell
you what it costs.

The interesting comparison is 2 against 3. Both have the same information
available. What differs is that the agent has a *job*: audit for defensibility,
report in those three buckets, quantify, and stop.

---

## Prompt B - the tool boundary

Still with **appraisal-reviewer** selected:

> That is right. Go ahead and fix it, and update the tests.

### What to look for

It should decline, and it should say why: a reviewer who edits the file becomes
the author and can no longer review it.

That refusal is not politeness. Look at the frontmatter in
`.github/agents/appraisal-reviewer.agent.md`:

```yaml
tools: ["search", "codebase", "usages", "problems", "runCommands"]
```

`editFiles` is absent. The agent cannot write to your files even if it wants to
and even if you insist. The boundary is enforced by the tool list, not by the
prose asking nicely.

This is the part of agents that has no equivalent in instructions or skills. An
instruction saying "do not edit files" is a request. A tool list omitting
`editFiles` is a wall. When you write your own agents, decide the tool list
first - it is the design decision, and the prose is commentary on it.

Now switch back to plain Agent mode and give it the fix prompt from
[Lesson 06](../06-agents.md), which insists on a failing test first.

---

## Prompt C - same question, different job

This shows that an agent is a *role*, not a quality setting. Ask the identical
question twice, changing only the selected agent:

> What is going on with price per square foot across our submarkets?

**With appraisal-reviewer:** expect scrutiny. Whether the medians are
defensible, that unadjusted $/sqft is orientation rather than evidence, what
sample sizes sit behind each figure.

**With data-explorer:** expect teaching. The question restated as a specific
calculation, existing functions in `metrics.py` used rather than new code, the
result explained line by line for somebody who does not write Python, sample
size and date window stated alongside every median.

Neither is better. They are different colleagues. Picking the wrong one is like
asking your reviewer to explain Python to you, or asking the analyst whether a
file is ready to deliver.

---

## What to write down

Beyond the scorecard, the question worth arguing about in the group session:

**Did the reviewer agent find anything that was not actually a problem?**

If it did, that matters more than the bug it caught. An agent that manufactures
findings to look thorough trains everybody to ignore it, and then it catches
nothing. Ours is explicitly told to say "No material findings" and mean it. Test
whether it will - point it at a file that is genuinely fine, like `loader.py`,
and see whether it invents something.

If it does invent something, that is a bug in the agent, and fixing the agent is
exercise 6 in [lesson 08](../08-your-turn.md).

---

## After all three labs

You have now seen the same prompt behave differently for three separate reasons.
The summary worth carrying out of the series:

| | Changes | Loaded | Enforced by |
| --- | --- | --- | --- |
| **Instructions** | The words it uses and the rules it follows | Always, or on matching files | Prose |
| **Skill** | The work it does before answering | When your question matches the description | Prose plus bundled scripts |
| **Agent** | Who it is being, and what it may touch | When you select it | The tool list - actually enforced |

And the finding that should survive longest: in every one of these labs, the
uncustomized output was *fluent*. It read well. It sounded like somebody who
knew what they were doing. The customization did not make Copilot more
articulate - it made the articulate output checkable.

Back to [the lessons](../00-start-here.md) | On to [08 - Your turn](../08-your-turn.md)
