# Collateral IQ

A small, working business-intelligence tool for residential collateral
valuation - and a safe playground for learning VS Code and GitHub Copilot on our
own domain rather than on somebody else's to-do list app.

It screens comparable sales, adjusts them, reconciles an indicated value, and
rolls the portfolio up into a dashboard that flags which files a reviewer should
open first. The data is synthetic. None of these properties exist.

**New here? Go straight to [docs/00-start-here.md](docs/00-start-here.md).**

## Run it in three minutes

You need Python 3.10 or newer. Nothing else - no pip install, no npm, no build.

```bash
git clone <this-repo>
cd collateral-iq

export PYTHONPATH=src            # PowerShell: $env:PYTHONPATH = "src"

python -m unittest discover -s tests    # should end with OK
python -m collateral_iq value SUBJ-001  # one adjustment grid
python -m collateral_iq flags           # portfolio quality check
python -m collateral_iq serve           # dashboard at localhost:8000
```

Opening the folder in VS Code sets `PYTHONPATH` for you, so you can skip the
export. Say yes when it offers to install the recommended extensions.

## The guided lessons

Read in order the first time. Each is 15 to 35 minutes.

| Lesson | What you get out of it |
| --- | --- |
| [00 - Start here](docs/00-start-here.md) | What this is, and getting it running |
| [01 - Set up your machine](docs/01-setup.md) | Install, sign in, prove Copilot is alive |
| [02 - The VS Code tour](docs/02-vscode-tour.md) | The six parts you actually use |
| [03 - How you talk to Copilot](docs/03-copilot-modes.md) | Completions, ask, agent mode, coding agent |
| [04 - Instructions](docs/04-instructions.md) | Teaching Copilot our vocabulary and rules |
| [05 - Skills](docs/05-skills.md) | Packaging a procedure it loads on demand |
| [06 - Custom agents](docs/06-agents.md) | Giving it a job description and a boundary |
| [07 - READMEs and pull requests](docs/07-readmes-and-prs.md) | Writing docs, shipping a change |
| [08 - Your turn](docs/08-your-turn.md) | Nine open-ended exercises |

## The side-by-side labs

The lessons explain what instructions, skills, and agents are. The three labs in
[docs/demos/](docs/demos/README.md) make you watch the same prompt produce two
different answers with and without them, which is the part that actually
convinces people.

```bash
python tools/make_baseline.py     # builds ../collateral-iq-baseline
```

That is a stripped copy - identical code, identical data, no customization at
all. Open it in a second VS Code window, run each lab prompt in both, and compare.
Lab 1 isolates instructions, lab 2 isolates skills, lab 3 isolates agents. One
variable each, because "Copilot got better" teaches you nothing about which file
to write when you hit the problem at work.

Record what you get in `docs/demos/results/`. Model behaviour drifts, and three
people's results side by side make the point far better than one person's.

## Am I actually getting anywhere

```bash
python tools/check_progress.py
```

Ten checks across the lessons and labs. Most are behavioural rather than
cosmetic - the pool check runs the adjustment and sees which way the money moved,
so any correct fix passes and a fix that merely looks right does not. Nothing is
graded and nothing is reported anywhere; it exists because reading eight lessons
and building nothing feels identical to reading eight lessons and building
everything.

## Instructions, skills, agents - the short version

The distinction is the whole reason this repository exists, so here it is once,
plainly:

| | What it is | When it loads | Lives in |
| --- | --- | --- | --- |
| **Instructions** | A standing rule | Always, or whenever a matching file is open | `.github/copilot-instructions.md`, `.github/instructions/` |
| **Skill** | A procedure, with reference material and scripts | When your question matches its description | `.github/skills/<name>/SKILL.md` |
| **Agent** | A persona with a job and a tool boundary | When you select it from the chat dropdown | `.github/agents/<name>.agent.md` |

What is already set up here:

- **Instructions** - our domain vocabulary ("comp" means a closed sale), the
  standard-library-only rule, and the rule that adjustment rates live in exactly
  one place. Plus scoped rules for Python files and for Markdown.
- **Skills** - `comp-selection` (screening, bracketing, and when to refuse to
  produce a number) and `market-snapshot` (trend and absorption, with a bundled
  script that tells you when our configured time adjustment has gone stale).
- **Agents** - `appraisal-reviewer`, a read-only reviewer that audits valuation
  logic for defensibility, and `data-explorer`, which answers data questions for
  someone who does not write Python.

## What is in the box

```
src/collateral_iq/   loader, valuation, metrics, server, CLI
web/index.html       single-page dashboard, no framework
data/*.csv           synthetic subjects, comps, monthly market roll-up
tools/               data generator
tests/               unittest suite
docs/                the eight lessons
.github/             instructions, skills, agents, PR template
AGENTS.md            terse repository map, written for coding agents
```

## Known planted problems

Three things are wrong on purpose. Finding them is the exercise.

1. **A reversed sign** in one adjustment line in `valuation.py`. It does not
   crash, it does not fail a test, and it changes indicated values. Lesson 06
   finds it with the reviewer agent.
2. **A missing test** in `tests/test_valuation.py` - the one that would have
   caught the above. Lesson 05 and lesson 06 both point at it.
3. **Lazy reconciliation** - `reconcile()` takes an unweighted mean of the top
   three comps. Exercise 1 in lesson 08 fixes it.

They are marked `TODO(lesson-NN)` in the code. Search for `TODO(lesson` if you
want to skip ahead, but the point is to find them with the tools.

## Ground rules

- **Standard library only.** A reviewer must be able to clone this on a
  locked-down work laptop. If something seems to need a package, that is a
  design conversation, not a `pip install`.
- **The data is synthetic.** Do not point this at a real MLS, AVM, or borrower
  record, and do not commit anything that identifies a real property or person.
- **This is not an appraisal.** It is analysis that would support one. Every
  number it produces carries a line-by-line audit trail, because a number you
  cannot defend line by line is worse than no number.
- **Review every diff.** Especially the ones that touch `valuation.py`. Copilot
  is a fast junior colleague, not a merge button.

Full rules, including the domain vocabulary, are in
[.github/copilot-instructions.md](.github/copilot-instructions.md).

## Contributing

Branch, commit, open a pull request. The template will ask you whether your
change moves an indicated value - answer honestly. Exercises are claimed by
opening an issue with the "Playground exercise" template.

MIT licensed. Break it freely.
