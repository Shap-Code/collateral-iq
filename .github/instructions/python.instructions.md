---
applyTo: "**/*.py"
description: Python conventions for Collateral IQ.
---

# Python conventions

These apply on top of `.github/copilot-instructions.md`, and only to Python files.

- Target Python 3.10+. `from __future__ import annotations` at the top of every
  module, then modern type hints (`list[dict]`, `str | None`).
- Four-space indent, 100-character lines.
- Public functions get a docstring whose first line says what the caller gets
  back, in domain language: "Return the comp's adjusted sale price plus a
  line-by-line audit trail."
- Prefer a plain `dict` with documented keys over a class, unless behaviour
  travels with the data. This codebase is read far more often than it is extended.
- No bare `except:`. If you catch something, name it and explain in a comment
  what you expect to go wrong.
- Modules under `src/collateral_iq/` must not print. Printing belongs in
  `__main__.py` and `server.py` only, so the logic stays usable from a notebook
  or a test.
- When you change anything in `valuation.py`, add or update a test in
  `tests/test_valuation.py` in the same change. State in your summary which
  test would have caught the bug.
