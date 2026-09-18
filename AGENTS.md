# Repository map for coding agents

A short orientation so an agent - Copilot, or any other - can find its way
without reading every file. Humans starting out should read `README.md` instead.

## Layout

| Path | What lives here |
| --- | --- |
| `src/collateral_iq/loader.py` | Reads the CSVs in `data/` into dicts. No logic. |
| `src/collateral_iq/valuation.py` | Screening, adjustments, reconciliation. The numbers come from here. |
| `src/collateral_iq/metrics.py` | Portfolio roll-ups and quality flags. |
| `src/collateral_iq/server.py` | Stdlib JSON API plus static file serving. |
| `src/collateral_iq/__main__.py` | The `python -m collateral_iq ...` command line. |
| `web/index.html` | Single-page dashboard. No build step, no framework. |
| `data/*.csv` | Synthetic sample data. Regenerate with `python tools/generate_data.py`. |
| `tests/` | `unittest` suite. |
| `docs/` | The guided lessons. Numbered; read in order. |
| `docs/demos/` | Side-by-side labs comparing output with and without customization. |
| `tools/make_baseline.py` | Builds the uncustomized control copy the labs compare against. |
| `tools/check_progress.py` | Behavioural checks for which lessons have been completed. |
| `.github/` | Copilot instructions, scoped instructions, skills, custom agents. |

## Commands

```bash
python -m unittest discover -s tests   # tests
python -m collateral_iq flags          # portfolio quality check
python -m collateral_iq serve          # dashboard on localhost:8000
python tools/generate_data.py          # regenerate sample data
python tools/make_baseline.py          # build the control copy for the labs
python tools/check_progress.py         # what is done, what is not
```

`src/` is not installed as a package. The CLI works because `python -m` is run
from the repository root with `src` on the path via `.vscode/settings.json`, or
by setting `PYTHONPATH=src` yourself.

## Constraints that are not negotiable

- Standard library only.
- Adjustment rates live in one place: `ADJUSTMENTS` in `valuation.py`.
- Anything that changes an indicated value must also appear in the audit trail
  returned by `adjust_comp()`.
- The data is synthetic. Do not wire this to a real MLS, AVM, or borrower record.

Fuller rules, including the domain vocabulary, are in
`.github/copilot-instructions.md`.
