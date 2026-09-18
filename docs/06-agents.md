# 05 - Custom agents

**Time:** 30 minutes
**You will learn:** what a custom agent is, how it differs from a skill, and how to use one to find a real bug
**You will need:** lesson 05 finished

## Where an agent sits

- **Instructions** - rules, always on.
- **Skill** - a procedure, loaded when relevant.
- **Agent** - a *persona with a job and a boundary*, that you select deliberately.

An agent is who Copilot is being for this conversation. It has a point of view,
a set of tools it is allowed to use, and things it will refuse to do. You pick an
agent from the mode dropdown in the chat panel, the same place you switch between
Ask and Agent mode.

A skill is a set of steps. An agent is a person following them, with judgement
about what to raise and what to leave alone.

## The anatomy

```markdown
---
name: appraisal-reviewer
description: A review appraiser who audits valuation logic and comp sets for defensibility.
tools: ["search", "codebase", "usages", "problems", "runCommands"]
---
```

The `tools` list is the boundary. Ours deliberately omits `editFiles`, because a
reviewer who edits the file becomes the author and can no longer review it. That
constraint is the most useful line in the file.

Open `.github/agents/appraisal-reviewer.agent.md` and read it. Notice it has
opinions - actual positions about averaging, gross adjustment limits, and what
counts as support - and that it is told to say "no material findings" rather than
manufacture one. A reviewer who always finds something is as useless as one who
never does.

Then open `.github/agents/data-explorer.agent.md`. Same mechanism, completely
different job: it explains rather than judges, it is allowed to edit files, and
it is told to restate the question as a calculation before writing any code.

## Use the reviewer to find the planted bug

Select **appraisal-reviewer** from the agent dropdown. Then:

> Review the adjustment logic in src/collateral_iq/valuation.py against the sign
> convention documented in the adjust_comp docstring. Report material findings only.

It should land on the pool adjustment. The docstring says every adjustment moves
the comp toward the subject - positive when the subject is superior. The pool
line computes `comp["pool"] - subject["pool"]`, which is backwards: a comp with a
pool against a subject without one gets a *positive* adjustment, inflating the
comp instead of discounting it.

Before you fix it, quantify it. Ask:

> How much does this change the indicated value for each subject? Run the
> portfolio and show me before and after.

This is the difference between a code bug and an appraisal bug. A code bug is a
line to fix. An appraisal bug is a number that went out the door, and the first
question anybody will ask is "which reports were affected".

## Fix it properly

Switch back to ordinary **Agent** mode - the reviewer is not allowed to edit, and
that is the point.

> The pool adjustment in valuation.py has its sign reversed relative to the
> convention in the adjust_comp docstring. First add a failing test to
> tests/test_valuation.py that proves it - a comp with a pool against a subject
> without one should reduce the comp's adjusted price. Run the tests and show me
> it fails. Then fix valuation.py and run them again.

Insist on the failing test first. A fix without a failing test is a claim; a fix
with one is evidence. This also closes the `TODO(lesson-05)` in the test file.

## Write your own

A third agent worth having is an onboarding guide - something a new team member
can ask "where does X live" without interrupting anyone. Create
`.github/agents/repo-guide.agent.md`:

```markdown
---
name: repo-guide
description: A patient guide to this codebase for someone who has never worked in it, answering where things live and why they are structured that way.
tools: ["search", "codebase", "usages"]
---

# Repository guide

You help someone who knows real estate and does not yet know this codebase.

- Answer with the file and the function, then one sentence on why it lives there.
- Always point at the smallest thing that answers the question. Do not paste a
  whole module when three lines will do.
- When a design choice looks odd, explain the constraint behind it - usually the
  standard-library-only rule, or the requirement that every number be auditable.
- Never edit anything. If the answer is "that does not exist yet", say so and
  point at docs/08-your-turn.md.
- End every answer with one suggested next file to read.
```

Test it with the question a genuine newcomer asks:

> Where does the indicated value actually get calculated, and why is it separate
> from the dashboard?

## Choosing between the three

| You want to... | Use |
| --- | --- |
| Make one rule apply everywhere, forever | Instructions |
| Capture a repeatable procedure with reference material | Skill |
| Change who Copilot is being, and what it is allowed to touch | Agent |

They compose. The reviewer agent works better *because* the instructions file
already taught Copilot our vocabulary, and it can pull in the comp-selection
skill's reference sheet when it needs the sign convention spelled out.

## Now go and see it

Reading this lesson is not the same as believing it. Run
[Lab 3 - Agents](demos/lab-3-agents.md) before moving on - it puts the same prompt
through an uncustomized copy and this one, side by side.

Next: [07 - READMEs and pull requests](07-readmes-and-prs.md)
