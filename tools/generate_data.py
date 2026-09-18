"""Regenerate the sample datasets in data/.

Everything is synthetic but shaped like real Maricopa County residential data.
Seeded, so running this twice produces identical files.

    python tools/generate_data.py
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 85374
DATA = Path(__file__).resolve().parents[1] / "data"

SUBMARKETS = {
    # name: (base price per sqft, monthly appreciation, typical dom)
    "Surprise - Marley Park": (232.0, 0.0038, 34),
    "Surprise - Sun City Grand": (248.0, 0.0031, 41),
    "Peoria - Vistancia": (255.0, 0.0044, 29),
    "Goodyear - Estrella": (221.0, 0.0036, 45),
    "Glendale - Arrowhead": (244.0, 0.0029, 38),
}
CITIES = {
    "Surprise - Marley Park": ("Surprise", "85379"),
    "Surprise - Sun City Grand": ("Surprise", "85374"),
    "Peoria - Vistancia": ("Peoria", "85383"),
    "Goodyear - Estrella": ("Goodyear", "85338"),
    "Glendale - Arrowhead": ("Glendale", "85308"),
}
STREETS = [
    "W Sweetwater Ave", "N Cotton Ln", "W Aster Dr", "N 163rd Dr", "W Calavar Rd",
    "N Sunrise Blvd", "W Gambit Trl", "N Vista Ln", "W Melinda Ln", "N Saguaro Dr",
]
EFFECTIVE_DATE = date(2026, 9, 1)


def months_between(earlier, later):
    return (later.year - earlier.year) * 12 + (later.month - earlier.month)


def main():
    rng = random.Random(SEED)
    DATA.mkdir(exist_ok=True)

    # ---------- subjects ----------
    subjects = []
    for i, submarket in enumerate(SUBMARKETS, start=1):
        city, zipcode = CITIES[submarket]
        subjects.append({
            "subject_id": f"SUBJ-{i:03d}",
            "apn": f"{501 + i}-{rng.randint(10, 89)}-{rng.randint(100, 899)}",
            "address": f"{rng.randint(12000, 18999)} {rng.choice(STREETS)}",
            "city": city,
            "zip": zipcode,
            "submarket": submarket,
            "effective_date": EFFECTIVE_DATE.isoformat(),
            "gla_sqft": rng.choice([1640, 1885, 2120, 2380, 2755]),
            "lot_sqft": rng.choice([6000, 6500, 7200, 8400, 9600]),
            "year_built": rng.choice([1998, 2004, 2011, 2016, 2021]),
            "beds": rng.choice([3, 3, 4, 4, 5]),
            "baths": rng.choice([2.0, 2.5, 3.0, 3.5]),
            "garage_spaces": rng.choice([2, 2, 3]),
            "pool": rng.choice([0, 1]),
            "condition_rating": rng.choice(["C3", "C3", "C4"]),
            "quality_rating": rng.choice(["Q3", "Q4"]),
            "view_rating": rng.choice(["N", "N", "B"]),  # N=neutral, B=beneficial
            "assignment_type": rng.choice(["Purchase", "Refinance", "Portfolio review"]),
            "client": rng.choice(["Cactus Ridge Lending", "Saguaro Capital", "Internal QC"]),
        })

    # ---------- comps ----------
    comps = []
    comp_no = 0
    for subject in subjects:
        submarket = subject["submarket"]
        base_ppsf, appreciation, base_dom = SUBMARKETS[submarket]
        city, zipcode = CITIES[submarket]
        for _ in range(28):
            comp_no += 1
            sale_date = EFFECTIVE_DATE - timedelta(days=rng.randint(15, 330))
            age_months = months_between(sale_date, EFFECTIVE_DATE)
            gla = subject["gla_sqft"] + rng.randint(-420, 420)
            pool = rng.choice([0, 0, 1])
            garage = rng.choice([2, 2, 2, 3])
            # Price drifts down as you go back in time, plus feature premiums and noise.
            ppsf = base_ppsf * (1 - appreciation) ** age_months
            price = ppsf * gla
            price += 31000 * pool
            price += 9000 * (garage - 2)
            price *= rng.uniform(0.94, 1.06)
            comps.append({
                "comp_id": f"CMP-{comp_no:04d}",
                "subject_id": subject["subject_id"],
                "apn": f"{501}-{rng.randint(10, 89)}-{rng.randint(100, 899)}",
                "address": f"{rng.randint(12000, 18999)} {rng.choice(STREETS)}",
                "city": city,
                "zip": zipcode,
                "submarket": submarket,
                "sale_date": sale_date.isoformat(),
                "sale_price": int(round(price, -2)),
                "gla_sqft": gla,
                "lot_sqft": rng.choice([5800, 6400, 7000, 8100, 9900, 12500]),
                "year_built": subject["year_built"] + rng.randint(-9, 6),
                "beds": rng.choice([3, 3, 4, 4, 5]),
                "baths": rng.choice([2.0, 2.5, 3.0, 3.5]),
                "garage_spaces": garage,
                "pool": pool,
                "condition_rating": rng.choice(["C2", "C3", "C3", "C4", "C4", "C5"]),
                "quality_rating": rng.choice(["Q2", "Q3", "Q3", "Q4", "Q5"]),
                "view_rating": rng.choice(["N", "N", "N", "B", "A"]),  # A = adverse
                "dom": max(4, int(rng.gauss(base_dom, 14))),
                "concessions": rng.choice([0, 0, 0, 3500, 6000, 9500]),
                "distance_miles": round(abs(rng.gauss(0.9, 0.7)) + 0.05, 2),
                "sale_type": rng.choice(
                    ["Arms length"] * 9 + ["REO", "Short sale", "Relocation"]
                ),
            })

    # ---------- monthly market roll-up ----------
    market = []
    for submarket, (base_ppsf, appreciation, base_dom) in SUBMARKETS.items():
        for back in range(23, -1, -1):
            month_start = (EFFECTIVE_DATE.replace(day=1) - timedelta(days=back * 30)).replace(day=1)
            age = months_between(month_start, EFFECTIVE_DATE)
            ppsf = base_ppsf * (1 - appreciation) ** age * rng.uniform(0.99, 1.01)
            market.append({
                "month": month_start.strftime("%Y-%m"),
                "submarket": submarket,
                "median_ppsf": round(ppsf, 2),
                "median_sale_price": int(round(ppsf * rng.uniform(2000, 2200), -2)),
                "closed_sales": rng.randint(18, 74),
                "median_dom": max(6, int(rng.gauss(base_dom, 9))),
                "months_supply": round(abs(rng.gauss(2.8, 0.9)) + 0.4, 1),
            })

    for name, rows in (
        ("subjects.csv", subjects),
        ("comps.csv", comps),
        ("market_monthly.csv", market),
    ):
        path = DATA / name
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {path.relative_to(DATA.parent)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
