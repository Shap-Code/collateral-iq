# 01 - Set up your machine

**Time:** 30 to 45 minutes the first time
**You will learn:** how to get VS Code, Python, Git, and Copilot working together
**You will need:** admin rights on your laptop, and a GitHub account

Skip this lesson only if you already write code on this machine. If you have
never opened a terminal, this is the lesson that matters most - and the one that
most often goes wrong quietly, so do every verification step even when you are
sure.

Work through it in order. Each step ends with a check that either passes or
fails. Do not move on from a failed check.

---

## Step 1 - Install VS Code

Download from <https://code.visualstudio.com> and install it normally.

On Mac, drag it to Applications, then open it once from Applications so macOS
stops asking whether you trust it.

**Check:** VS Code opens and shows a Welcome tab.

---

## Step 2 - Install Python

Collateral IQ needs Python 3.10 or newer.

**Mac:** open Terminal (Cmd+Space, type "Terminal") and run `python3 --version`.
macOS may ship something old or nothing at all. If you get anything below 3.10,
install from <https://www.python.org/downloads/> and take the default options.

**Windows:** install from <https://www.python.org/downloads/>. On the very first
screen of the installer, tick **"Add python.exe to PATH"** before clicking
Install. This one checkbox is the single most common cause of "python is not
recognized" an hour later.

**Check:** open a *new* terminal window and run:

```bash
python3 --version     # Mac / Linux
py --version          # Windows
```

You should see `Python 3.10.x` or higher. A new window matters - an old one does
not know about anything you just installed.

---

## Step 3 - Install Git

**Mac:** run `git --version`. If Git is missing, macOS offers to install the
developer tools. Accept, wait, and run it again.

**Windows:** install from <https://git-scm.com/download/win>, defaults are fine.

**Check:** `git --version` prints a version number.

Then tell Git who you are, once, ever:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@yourcompany.com"
```

Use the same email as your GitHub account, or your commits will not link to you.

---

## Step 4 - Get the repository onto your machine

Pick a folder you will remember. `Documents/code` is fine.

```bash
cd ~/Documents
mkdir -p code
cd code
git clone <the URL from the green Code button on GitHub>
cd collateral-iq
```

If `git clone` asks for a password, it wants a token rather than your GitHub
password. Easiest route: install the GitHub CLI from <https://cli.github.com>,
run `gh auth login`, follow the browser prompts, then try the clone again.

**Check:** `ls` (Mac) or `dir` (Windows) shows `README.md`, `src`, `docs`.

---

## Step 5 - Open the folder, not a file

In VS Code: `File > Open Folder`, and select **collateral-iq** - the folder that
contains `README.md`.

This matters more than it sounds. Opening the folder is what makes VS Code load
`.vscode/settings.json` and what lets Copilot see the repository around the file
you are editing. Opening a single file gets you an editor with no context.

VS Code will ask whether you trust the authors. Say yes. It will then offer to
install the recommended extensions from `.vscode/extensions.json`. Say yes to
that too - that is Copilot, Copilot Chat, and the Python extension.

**Check:** the Explorer on the left shows the full file tree, and the window
title says "collateral-iq".

---

## Step 6 - Point VS Code at your Python

Press `Ctrl/Cmd+Shift+P` to open the command palette, type
**Python: Select Interpreter**, and pick any 3.10 or newer entry.

**Check:** open `src/collateral_iq/valuation.py`. The `from .loader import ...`
line at the top should have no red squiggle underneath it. If it does, the
interpreter is wrong or the folder is wrong - go back to step 5.

---

## Step 7 - Prove the code runs

Open the built-in terminal with `Ctrl+`` ` `` (the backtick key, above Tab).
It opens already inside the repository folder.

```bash
python -m unittest discover -s tests
```

**Check:** the last line says `OK`. Nine tests should run.

If you get `No module named collateral_iq`, `PYTHONPATH` did not take effect.
Close the terminal panel entirely and open a new one - `.vscode/settings.json`
sets it only for terminals opened after VS Code loaded the folder.

Then:

```bash
python -m collateral_iq flags
```

**Check:** you get a table of five subjects with indicated values.

---

## Step 8 - Sign in to Copilot

Click the account icon at the bottom of the left activity bar, choose **Sign in
with GitHub**, and complete the browser flow.

You need an active Copilot licence on that account. If you are not sure, go to
<https://github.com/settings/copilot> - it will tell you plainly. If your
organisation assigns licences, ask whoever administers your GitHub org; there is
nothing you can do from this end.

**Check:** the Copilot icon in the title bar is solid rather than crossed out.

---

## Step 9 - Prove Copilot is actually alive

Two separate things have to work, and they fail independently.

**Completions.** Open `src/collateral_iq/metrics.py`, scroll to the bottom, and
type this line and press Enter:

```python
def count_comps_by_city() -> dict:
```

Wait two seconds. Grey suggested text should appear. Press `Esc` to reject it -
we do not want this function. If nothing appears after five seconds, completions
are not working.

**Chat.** Open the chat panel with `Ctrl/Cmd+Alt+I` and ask:

> What does this repository do?

**Check:** you get an answer that mentions collateral, comps, or valuation
specifically - not a generic description of a Python project. If it is generic,
Copilot is not reading your workspace, which usually means step 5 went wrong.

---

## Step 10 - The check that matters

Still in chat, ask:

> What rules am I supposed to follow when writing code in this repository?

**Check:** the answer mentions the standard-library-only rule, or our definition
of "comp", or the rule that adjustment rates live in one place.

If it does, `.github/copilot-instructions.md` is loading, and everything in
lessons 04 through 06 will work. If the answer is generic advice about clean
code, something is wrong with your setup - go back to step 5 before continuing.

This is the first time you will see a customization file change Copilot's
behaviour. It will not be the last.

---

## When something is broken

| Symptom | Almost always |
| --- | --- |
| `python: command not found` | Wrong command for your OS, or PATH checkbox missed on Windows. Try `python3` or `py`. |
| `No module named collateral_iq` | Wrong folder open, or a terminal opened before the folder loaded. |
| Red squiggles on imports | Interpreter not selected. Step 6. |
| Copilot gives generic answers | A single file is open instead of the folder. Step 5. |
| Copilot does nothing at all | Not signed in, or no licence. Step 8. |
| Changes you made are ignored | The file is unsaved. Copilot reads disk. Turn on `Files: Auto Save`. |

Ask in the team channel rather than losing an hour. Every one of these has been
hit by somebody already.

Next: [02 - The VS Code tour](02-vscode-tour.md)
