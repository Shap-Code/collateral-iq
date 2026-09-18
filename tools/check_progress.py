"""Check which lessons and labs you have actually completed.

    python tools/check_progress.py

Nothing here is graded and nothing is reported anywhere. It exists because
reading eight lessons and building nothing feels identical to reading eight
lessons and building everything, and a checklist you can run is the cheapest
possible way to tell the difference.

Checks are behavioural where possible. The pool check does not look for a
particular line of code - it runs the adjustment and sees which way the money
moved, so any correct fix passes and a fix that only looks right does not.
"""
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

sys.dont_write_bytecode = True  # never leave a stale .pyc behind a check

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

PASS, FAIL, SKIP = "PASS", "TODO", "n/a"


def frontmatter(path: Path) -> dict:
    """Parse the YAML-ish frontmatter of a markdown file. Only handles key: value."""
    if not path.exists():
        return {}
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, value = line.partition(":")
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


# --------------------------------------------------------------------------
# Individual checks. Each returns (status, detail).
# --------------------------------------------------------------------------

def check_environment():
    if sys.version_info < (3, 10):
        return FAIL, f"Python {sys.version_info.major}.{sys.version_info.minor}; need 3.10+"
    return PASS, f"Python {sys.version_info.major}.{sys.version_info.minor}"


def check_tests():
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"],
        cwd=REPO, capture_output=True, text=True,
        env={"PYTHONPATH": str(REPO / "src"), "PATH": "/usr/bin:/bin:/usr/local/bin"},
    )
    tail = (result.stderr or result.stdout).strip().splitlines()
    if result.returncode == 0:
        return PASS, tail[-1] if tail else "OK"
    return FAIL, "suite is failing - fix before continuing"


def check_data_instructions():
    path = REPO / ".github/instructions/data.instructions.md"
    meta = frontmatter(path)
    if not meta:
        return FAIL, "write .github/instructions/data.instructions.md (lesson 04)"
    if "applyTo" not in meta:
        return FAIL, "file exists but has no applyTo glob, so it will never load"
    return PASS, f"applyTo: {meta['applyTo']}"


def check_file_review_skill():
    path = REPO / ".github/skills/file-review/SKILL.md"
    meta = frontmatter(path)
    if not meta:
        return FAIL, "write .github/skills/file-review/SKILL.md (lesson 05)"
    problems = []
    if meta.get("name") != "file-review":
        problems.append("name must match the folder exactly")
    description = meta.get("description", "")
    if len(description) < 60:
        problems.append("description too short to trigger reliably")
    elif "use when" not in description.lower() and "use whenever" not in description.lower():
        problems.append("description does not say when to use it")
    if problems:
        return FAIL, "; ".join(problems)
    return PASS, f"{len(description)} char description"


def check_repo_guide_agent():
    path = REPO / ".github/agents/repo-guide.agent.md"
    meta = frontmatter(path)
    if not meta:
        return FAIL, "write .github/agents/repo-guide.agent.md (lesson 06)"
    tools = meta.get("tools", "")
    if "editFiles" in tools:
        return FAIL, "a read-only guide should not list editFiles"
    return PASS, f"tools: {tools or 'not restricted'}"


def check_pool_sign():
    """A comp with a pool, against a subject without one, must be adjusted DOWN."""
    from collateral_iq import valuation

    subject = {
        "effective_date": date(2026, 9, 1), "gla_sqft": 2000, "lot_sqft": 7000,
        "year_built": 2010, "garage_spaces": 2, "pool": 0,
        "condition_rating": "C3", "quality_rating": "Q3", "view_rating": "N",
    }
    comp = dict(subject, pool=1, sale_price=500_000, concessions=0,
                comp_id="CHK", address="-", sale_date=date(2026, 9, 1),
                distance_miles=0.4, sale_type="Arms length")
    line = next(l for l in valuation.adjust_comp(subject, comp)["lines"] if l["item"] == "Pool")
    if line["amount"] < 0:
        return PASS, f"pool adjustment {line['amount']:+,} - correct direction"
    return FAIL, f"pool adjustment {line['amount']:+,} - still reversed (lesson 06)"


def check_pool_test():
    text = (REPO / "tests/test_valuation.py").read_text(encoding="utf-8")
    if "TODO(lesson-05)" in text:
        return FAIL, "the placeholder TODO is still there; write the test (lesson 05)"
    if "pool" not in text.lower():
        return FAIL, "no test mentions the pool adjustment"
    return PASS, "a pool test exists"


def check_weighted_reconciliation():
    text = (REPO / "src/collateral_iq/valuation.py").read_text(encoding="utf-8")
    if "TODO(lesson-08)" in text:
        return FAIL, "reconcile() is still an unweighted mean (lesson 08, exercise 1)"
    if "weight" not in text.lower():
        return FAIL, "TODO removed but no weighting found - did you mean to?"
    return PASS, "reconciliation is weighted"


def check_baseline():
    baseline = REPO.parent / "collateral-iq-baseline"
    if not baseline.exists():
        return FAIL, "run python tools/make_baseline.py"
    if (baseline / ".github").exists():
        return FAIL, "the baseline contains .github - it is not a control group"
    return PASS, str(baseline)


def check_lab_results():
    results = sorted(
        p for p in (REPO / "docs/demos/results").glob("*.md")
        if p.name != "TEMPLATE.md"
    )
    if not results:
        return FAIL, "no lab results recorded yet"
    return PASS, f"{len(results)} recorded: {', '.join(p.stem for p in results)}"


CHECKS = [
    ("Setup", "Python 3.10 or newer", check_environment),
    ("Setup", "Test suite passes", check_tests),
    ("Labs", "Baseline copy built", check_baseline),
    ("Labs", "Lab results recorded", check_lab_results),
    ("Lesson 04", "Wrote a scoped instructions file", check_data_instructions),
    ("Lesson 05", "Wrote the file-review skill", check_file_review_skill),
    ("Lesson 05", "Wrote the missing pool test", check_pool_test),
    ("Lesson 06", "Wrote the repo-guide agent", check_repo_guide_agent),
    ("Lesson 06", "Fixed the reversed pool sign", check_pool_sign),
    ("Lesson 08", "Weighted reconciliation", check_weighted_reconciliation),
]


def main() -> int:
    print("\nCollateral IQ - progress check\n")
    done = 0
    group = None
    for heading, label, check in CHECKS:
        if heading != group:
            print(f"  {heading}")
            group = heading
        try:
            status, detail = check()
        except Exception as exc:  # a broken check should not hide the others
            status, detail = FAIL, f"check errored: {type(exc).__name__}: {exc}"
        done += status == PASS
        marker = "x" if status == PASS else " "
        print(f"    [{marker}] {label:<34} {detail}")

    total = len(CHECKS)
    print(f"\n  {done} of {total} complete.")
    if done == total:
        print("  Everything on the list is done. Lesson 08 has six exercises left.\n")
    else:
        nxt = next(label for _, label, check in CHECKS if check()[0] != PASS)
        print(f"  Next up: {nxt}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
