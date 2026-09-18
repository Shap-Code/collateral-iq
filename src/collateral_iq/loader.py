"""Read the CSV files in data/ into plain Python dictionaries.

No pandas, no database. Small enough to hold in memory, simple enough to read
line by line when you are learning what the code does.
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# Columns that should be converted out of text into real Python types.
INT_FIELDS = {
    "sale_price", "gla_sqft", "lot_sqft", "year_built", "beds",
    "garage_spaces", "pool", "dom", "concessions", "closed_sales",
    "median_sale_price",
}
FLOAT_FIELDS = {"baths", "distance_miles", "median_ppsf", "months_supply"}
DATE_FIELDS = {"sale_date", "effective_date"}


def _coerce(row: dict[str, str]) -> dict:
    """Turn the strings csv gives us into numbers and dates where it makes sense."""
    out: dict = {}
    for key, value in row.items():
        if key in INT_FIELDS:
            out[key] = int(value)
        elif key in FLOAT_FIELDS:
            out[key] = float(value)
        elif key in DATE_FIELDS:
            out[key] = date.fromisoformat(value)
        else:
            out[key] = value
    return out


def _read(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run: python tools/generate_data.py"
        )
    with path.open(newline="", encoding="utf-8") as fh:
        return [_coerce(row) for row in csv.DictReader(fh)]


def load_subjects() -> list[dict]:
    """Every property we have been asked to value."""
    return _read("subjects.csv")


def load_comps(subject_id: str | None = None) -> list[dict]:
    """Closed sales available as comparables, optionally filtered to one subject."""
    comps = _read("comps.csv")
    if subject_id:
        comps = [c for c in comps if c["subject_id"] == subject_id]
    return comps


def load_market() -> list[dict]:
    """Monthly submarket roll-up: median price per sqft, days on market, supply."""
    return _read("market_monthly.csv")


def get_subject(subject_id: str) -> dict:
    """Look up one subject property by id, e.g. 'SUBJ-001'."""
    for subject in load_subjects():
        if subject["subject_id"] == subject_id:
            return subject
    raise KeyError(f"No subject named {subject_id!r}")
