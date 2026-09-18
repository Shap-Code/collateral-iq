# 02 - How you talk to Copilot

**Time:** 30 minutes
**You will learn:** the four ways to use Copilot, and which one to reach for
**You will need:** the Copilot and Copilot Chat extensions signed in

There are four distinct things people mean by "using Copilot". They behave very
differently, and picking the wrong one is the most common reason people conclude
the tool is not useful.

## 1. Inline completions

You type, grey text appears, `Tab` accepts it. No chat, no prompt.

Try it: open `src/collateral_iq/metrics.py`, go to the bottom, and type:

```python
def median_dom_by_submarket() -> list[dict]:
    """Median days on market for closed sales, grouped by submarket."""
```

Press Enter and wait. Copilot will propose a body, and it will probably be close,
because the file above it establishes the pattern. Press `Esc` to reject it -
we do not actually need this function.

**Reach for it when:** you already know what you are writing and want to type
less. It is autocomplete with a longer memory, nothing more.

## 2. Ask

The chat panel with the mode set to **Ask**. It reads, it explains, it does not
change your files.

Open the chat panel and try:

> Explain what screen_comps in valuation.py does, in terms an appraiser would
> recognise. What would happen to the portfolio if I raised max_distance_miles
> to 3.0?

Then attach a file for context. Click the paperclip, add
`src/collateral_iq/valuation.py`, and ask:

> Which of these adjustment lines would a state board consider the weakest support?

**Reach for it when:** you are trying to understand something, or you want a
second opinion before you change anything. This is where most of your hours
will go, and it is the safest mode to learn in.

## 3. Agent mode

Same chat panel, mode set to **Agent**. Now Copilot can read files, edit files,
run terminal commands, and loop until the task is done. It shows you each change
and waits for you to accept or reject.

Try a small one:

> Run the test suite. If it passes, add a test to tests/test_valuation.py that
> checks a comp with an inferior condition rating produces a positive condition
> adjustment. Run the tests again and show me the result.

Watch what it does, not just what it produces. It should read the file first,
propose an edit, ask permission to run the command, and report the outcome.

**Reach for it when:** the task touches more than one file, or needs a run-check-
fix loop. Keep the tasks small. "Refactor the valuation module" is a bad agent
task; "add a weighted reconciliation function with tests" is a good one.

**The rule that matters:** you review every diff. Agent mode is a fast junior
colleague, not a merge button. In this repository specifically, any change to
`valuation.py` changes somebody's opinion of value.

## 4. The coding agent

This one does not run in your editor. On GitHub, you assign an issue to Copilot,
and it works in its own cloud environment and opens a pull request. You review
the PR the way you would review a colleague's.

We will use this in lesson 07. For now, just know the distinction: agent mode is
Copilot at your desk; the coding agent is Copilot doing a task while you do
something else.

## Which to reach for

| Situation | Mode |
| --- | --- |
| Finishing a line or a function you already planned | Inline completions |
| "What does this do / why is this wrong" | Ask |
| "Change these three files and make the tests pass" | Agent mode |
| "Do this while I am on an inspection" | Coding agent |

## The habit that separates people who get value from people who do not

Give Copilot the same context you would give a new hire. "Fix the pool bug" gets
you guesswork. "In valuation.py, the pool adjustment line does not follow the
sign convention documented in the adjust_comp docstring - every adjustment moves
the comp toward the subject. Show me the fix and the test that would have caught
it" gets you the answer.

Lessons 04 to 06 are about making that context permanent, so you stop retyping it.

Next: [04 - Instructions](04-instructions.md)
