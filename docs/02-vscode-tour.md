# 01 - The VS Code tour

**Time:** 20 minutes
**You will learn:** the six parts of VS Code you will actually use
**You will need:** lesson 01 finished

## Opening the repository

`File > Open Folder`, and choose the folder that contains `README.md`. Opening
the *folder*, not a single file, is what gives Copilot the surrounding context -
and it is what makes the settings in `.vscode/` take effect.

The first time you open it, VS Code will offer to install the recommended
extensions listed in `.vscode/extensions.json`. Say yes.

## The six parts

**1. Explorer** (the file tree, top icon in the left bar, or `Ctrl/Cmd+Shift+E`)
Your files. Click `src/collateral_iq/valuation.py` and read it - that is where
the numbers come from.

**2. The command palette** (`Ctrl/Cmd+Shift+P`)
The single most useful key combination in VS Code. Everything the editor can do
is in here, searchable by name. Try typing "Python: Select Interpreter".

**3. The integrated terminal** (`Ctrl+\`` - the backtick key)
A normal terminal, inside the editor, already in the right folder. Run:

```bash
python -m collateral_iq flags
```

**4. Source control** (the branch icon, or `Ctrl/Cmd+Shift+G`)
Every change you make shows up here. Blue is modified, green is new. You stage
changes with the `+`, write a message, and commit. We will use this properly in
lesson 07.

**5. Search across files** (`Ctrl/Cmd+Shift+F`)
Search for `TODO(lesson` and you will find the three planted problems.

**6. The Copilot chat panel** (the chat icon in the title bar, or `Ctrl/Cmd+Alt+I`)
Lesson 03 is entirely about this.

## The things beginners lose an hour to

- **The wrong Python interpreter.** If imports show red squiggles, open the
  command palette, run "Python: Select Interpreter", and pick any Python 3.10+.
- **The wrong folder.** If the terminal says `No module named collateral_iq`,
  you probably opened a subfolder. Close it and open the repository root.
- **Unsaved files.** Copilot reads what is on disk. `Ctrl/Cmd+S` before asking
  it about a file you just edited. Turn on `Files: Auto Save` and stop thinking
  about it.

## Try it

1. Open `src/collateral_iq/metrics.py`.
2. Put your cursor inside `absorption_summary` and press `Ctrl/Cmd+Shift+P`,
   then run "Go to Definition" on `load_market`. Notice you jump to `loader.py`.
3. Press `Ctrl/Cmd+-` (or the back arrow) to jump back.

That jump-and-return is how you read code you did not write. You will do it
constantly.

Next: [03 - How you talk to Copilot](03-copilot-modes.md)
