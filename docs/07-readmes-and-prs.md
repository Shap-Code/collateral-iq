# 06 - READMEs and pull requests

**Time:** 30 minutes
**You will learn:** how to edit Markdown, and how to get a change reviewed and merged
**You will need:** lesson 06 finished, and the pool bug fixed

## Markdown in 90 seconds

A README is a plain text file with a few conventions. VS Code previews it with
`Ctrl/Cmd+Shift+V`, or the split-screen preview icon in the top right.

```markdown
# One heading per document
## Section
### Subsection

**bold**  *italic*  `inline code`

- bullet
- bullet
  - nested, two spaces

1. numbered
2. numbered

[link text](00-start-here.md)

> A blockquote. We use these for prompts you should copy into Copilot Chat.

| Column | Column |
| --- | --- |
| cell | cell |
```

Code fences take a language name, which is what colours them:

````markdown
```python
print("hello")
```
````

That is genuinely most of it.

## Why the README matters more than usual here

Two audiences read it. A person deciding whether this repository is worth their
afternoon, and an AI agent deciding which file to open. Both want the same thing:
what this is, how to run it, and where things live. Neither wants a paragraph
about how important valuation accuracy is.

We split that across two files on purpose. `README.md` is for humans arriving
cold. `AGENTS.md` is a map for coding agents - terser, all tables, no
encouragement. Open both and compare the tone.

## Edit the README with Copilot

You fixed the pool bug in lesson 06, so the README's "Known planted problems"
section is now out of date. In Agent mode:

> The pool sign bug described in README.md has been fixed. Update the "Known
> planted problems" section to reflect that, keeping the other two. Follow the
> conventions in .github/instructions/docs.instructions.md.

Read the diff. Check it did not quietly rewrite three other sections while it was
in there - that is the single most common thing to catch in an agent diff.

## Ship it

### 1. A branch

Source control panel, or the terminal:

```bash
git checkout -b fix/pool-adjustment-sign
```

Branch names: `fix/`, `feat/`, or `docs/`, then a short description in hyphens.

### 2. Commit

Stage your changes with the `+` in the Source Control panel, then write a
message. There is a small sparkle icon in the message box that drafts one from
your diff - use it, then rewrite it, because it describes *what* changed and you
want *why*.

Good: `Fix reversed sign on pool adjustment; add regression test`
Bad: `Update valuation.py`

```bash
git commit -m "Fix reversed sign on pool adjustment; add regression test"
git push -u origin fix/pool-adjustment-sign
```

### 3. Pull request

Push, then open the repository on GitHub and click "Compare & pull request".
Our template in `.github/PULL_REQUEST_TEMPLATE.md` fills in automatically. Fill
it in honestly - particularly the "does this change an indicated value" box,
which for this change is a yes.

Ask Copilot for a review on the PR itself, then read its comments the way you
read anything else from Copilot: some are real, some are noise, and you are the
one accountable for the merge.

## The coding agent

This is the fourth mode from lesson 03, and the pull request is where you meet it.

Open a new issue on GitHub describing a small, well-bounded task. For example:

> The dashboard has no page for a single subject's adjustment grid, even though
> /api/value?subject_id=SUBJ-001 already returns one. Add a subject detail view
> to web/index.html that appears when you click a row in the flags table, showing
> each comp's line items and the adjusted price. No new dependencies.

Assign the issue to Copilot. It works in its own environment and opens a pull
request when it is done. You review it exactly as you would a colleague's - and
the same instructions, skills, and agents in this repository apply to its work,
which is the reason it is worth setting all of that up.

**Good coding-agent tasks:** well-bounded, testable, no ambiguity about what
"done" means.
**Bad coding-agent tasks:** anything where the hard part is deciding what to
build. Decide first, then delegate.

Next: [08 - Your turn](08-your-turn.md)
