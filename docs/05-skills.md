# 04 - Skills

**Time:** 35 minutes
**You will learn:** what a skill is, how it differs from an instructions file, and how to write one
**You will need:** lesson 04 finished

## The one-sentence difference

An **instructions file** is a standing rule that is always in effect.
A **skill** is a procedure that gets loaded only when it is relevant.

Instructions answer "how do we do things here". Skills answer "here is exactly
how to do this particular task, step by step, with the reference material".

## Why the difference matters

If you put every procedure you own into `copilot-instructions.md`, that file
becomes thousands of words long and loads into every conversation, including the
ones about CSS. Everything competes for attention and nothing lands.

Skills fix that by loading in stages:

1. **Always loaded:** just the skill's name and one-line description.
2. **Loaded when relevant:** the body of `SKILL.md`, once Copilot decides the
   description matches what you asked.
3. **Loaded only if referenced:** extra files in the skill folder - reference
   docs, scripts, templates.

So you can have twenty skills installed and pay almost nothing for the nineteen
that are not relevant to the question you just asked.

## The anatomy

```
.github/skills/comp-selection/
├── SKILL.md                          <- required
└── references/
    └── adjustment-grid.md            <- loaded only when SKILL.md points at it
```

`SKILL.md` starts with YAML frontmatter with exactly two required fields:

```markdown
---
name: comp-selection
description: Select and defend comparable sales for a subject property ...
---
```

`name` must be kebab-case and identical to the folder name. `description` is the
trigger - it is the only thing Copilot sees when deciding whether to load the
skill, so it has to say both *what the skill does* and *when to use it*.

## Read ours

Open `.github/skills/comp-selection/SKILL.md`. Notice:

- The description names the situations that should trigger it: choosing comps,
  why a comp was excluded, screening thresholds, bracketing, defending a set to
  an underwriter. That is not padding - each phrase is a hook.
- The body is a numbered workflow, not an essay.
- There is a section on **when to push back instead of producing a number**. This
  is the most valuable part of the whole skill. Encoding when to refuse is what
  turns an assistant into a colleague.
- The reference file is pointed at explicitly, with a note on when to read it.

Now open `.github/skills/market-snapshot/SKILL.md`. This one bundles a script.
Copilot can run `scripts/market_stats.py` without ever loading its contents into
the conversation - it just executes it and reads the output. That is how a skill
stays cheap while doing real work.

## Try both

Type `/` in the chat input. Installed skills appear alongside prompt files, and
you can invoke one directly.

Or just ask naturally and watch it trigger:

> I am valuing SUBJ-004. Walk me through which comps survive screening and
> whether the set brackets the subject.

> What is the market doing in Goodyear - Estrella, and does our configured time
> adjustment still hold up?

The second one should end with Copilot running the bundled script and telling you
whether `ADJUSTMENTS["monthly_market_trend"]` is stale.

## Write one

Here is a real gap: we have no skill for the quality checks a reviewer runs
before a file goes out. Create `.github/skills/file-review/SKILL.md`:

```markdown
---
name: file-review
description: Run the pre-delivery quality checks on a Collateral IQ valuation before it reaches a client, covering comp count, adjusted spread, gross adjustment limits, and audit-trail completeness. Use whenever the user asks to review a file, check a valuation before delivery, run QC, or asks whether a subject is ready to send.
---

# File review

## The checks

Run `python -m collateral_iq flags` first. Then for the subject in question, run
`python -m collateral_iq value <SUBJECT_ID>` and confirm:

1. At least five comps survived screening. Fewer means the screens are doing the
   appraiser's job for them.
2. Adjusted spread across the relied-upon comps is 15% or less.
3. No primary comp carries a gross adjustment above 25%.
4. Every line item in the grid has a non-zero justification or a zero that makes
   sense - a zero condition adjustment between a C3 and a C5 is a defect.

## Reporting

One paragraph, then a table of each check with pass or fail and the number that
decided it. If any check fails, say what would have to change, not just that it
failed.

## Do not

Do not adjust thresholds to make a file pass. Do not produce a "ready to deliver"
verdict when a check failed.
```

Save it, start a new chat, and ask:

> Is SUBJ-003 ready to send to the client?

If the skill triggers, the description is doing its job. If it does not, the
description is too vague - add the words you would actually use. The description
is the whole triggering mechanism, so it is worth more editing time than the body.

## The test for whether something should be a skill

Ask: *would I write this down for a new hire?* If the answer is a one-line rule,
it belongs in instructions. If the answer is a procedure with steps, judgement
calls, and a reference sheet, it is a skill.

## Now go and see it

Reading this lesson is not the same as believing it. Run
[Lab 2 - Skills](demos/lab-2-skills.md) before moving on - it puts the same prompt
through an uncustomized copy and this one, side by side.

Next: [06 - Custom agents](06-agents.md)
