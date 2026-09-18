"""Create a stripped copy of this repository with all Copilot customization removed.

The copy is the control group for the side-by-side labs in docs/demos/. It has
identical code and identical data - the only difference is that Copilot has been
told nothing about how we work.

    python tools/make_baseline.py

Writes to ../collateral-iq-baseline/ by default, as a SIBLING of this repository.
That placement is deliberate and not negotiable: VS Code applies
.github/copilot-instructions.md from the root of the open folder, so a baseline
nested inside this repo would still inherit our instructions and the whole
comparison would be meaningless. Open it as its own VS Code window.

    python tools/make_baseline.py --dest /some/other/path
    python tools/make_baseline.py --force     # overwrite an existing baseline
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Copied across: the app, the data, the tests. Everything a prompt might need.
INCLUDE = ["src", "data", "tests", "tools", "web"]

# Never copied: this is the customization whose absence we are demonstrating.
EXCLUDE_NAMES = {".github", "AGENTS.md", "docs", ".vscode", ".devcontainer", ".git"}

NOTICE = """# Collateral IQ (baseline)

This is the **control group** for the side-by-side labs in the main repository,
at `docs/demos/`. Do not develop in it and do not commit it anywhere.

The code and data here are byte-for-byte identical to the real repository. What
is missing is everything that teaches Copilot how we work:

- no `.github/copilot-instructions.md`
- no `.github/instructions/`
- no `.github/skills/`
- no `.github/agents/`
- no `AGENTS.md`

Open this folder in its own VS Code window, run the lab prompt here, save what
you get, then run the identical prompt in the real repository and compare.

Regenerate at any time with `python tools/make_baseline.py` from the real
repository. Anything you change here will be lost, which is the point.
"""


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", default=str(REPO.parent / "collateral-iq-baseline"))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    dest = Path(args.dest).resolve()

    if dest == REPO or REPO in dest.parents:
        print("Refusing to write the baseline inside the repository.")
        print("A nested copy would still inherit .github/, which defeats the comparison.")
        return 1

    if dest.exists():
        if not args.force:
            print(f"{dest} already exists. Re-run with --force to replace it.")
            return 1
        shutil.rmtree(dest)

    dest.mkdir(parents=True)

    for name in INCLUDE:
        source = REPO / name
        if not source.exists():
            continue
        shutil.copytree(
            source,
            dest / name,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

    # The baseline has no need to generate its own baseline.
    stray = dest / "tools" / "make_baseline.py"
    if stray.exists():
        stray.unlink()

    # A plain README so the baseline is not mysterious, and a minimal gitignore.
    (dest / "README.md").write_text(NOTICE, encoding="utf-8")
    (dest / ".gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")

    # Verify nothing customizing leaked through.
    leaked = [
        p.relative_to(dest) for p in dest.rglob("*")
        if p.name in EXCLUDE_NAMES or p.name.endswith(".instructions.md")
        or p.name == "SKILL.md" or p.name.endswith(".agent.md")
    ]
    if leaked:
        print("Customization leaked into the baseline, which should be impossible:")
        for item in leaked:
            print(f"  {item}")
        return 1

    files = sum(1 for p in dest.rglob("*") if p.is_file())
    print(f"Baseline written to {dest} ({files} files).")
    print("\nNext:")
    print("  1. Open that folder in a SEPARATE VS Code window.")
    print("  2. Confirm it is really uncustomized - ask Copilot Chat there:")
    print('       "What rules am I supposed to follow in this repository?"')
    print("     You should get generic advice. If you get our vocabulary, you")
    print("     opened the wrong window.")
    print("  3. Start with docs/demos/lab-1-instructions.md in the real repo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
