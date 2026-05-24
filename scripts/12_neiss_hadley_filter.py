#!/usr/bin/env python3
"""Filter the hadley/neiss historical CSV (2013-2017, 1.87M rows) to youth
dental sport injuries, splitting output by year.

hadley's R package pre-processed the data, so this can't share scripts/05's
filter — the columns are named differently (snake_case) and the values are
human-readable text (body_part = 'Mouth', not '88') plus dates are encoded
as integer days-since-1970.

Output: data/extracted/neiss_dental_sports_hadley_<year>.csv per year, plus
a combined data/extracted/neiss_dental_sports_hadley_all.csv.
"""

import csv
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path("/Users/vihaanbanga/youth-dental-injury-database")
RAW = ROOT / "data/raw/neiss/injuries_hadley_2013-2017.csv"
OUT_DIR = ROOT / "data/extracted"

# Same SPORT_PRODUCT_CODES as scripts/05 — codes are numeric in hadley's prod1.
SPORT_PRODUCT_CODES = {
    "1205": ("basketball",         "limited_contact"),
    "1207": ("boxing",             "contact"),
    "1211": ("football_american",  "contact"),
    "1215": ("lacrosse_mens",      "contact"),
    "1266": ("volleyball",         "non_contact"),
    "1267": ("football_association", "limited_contact"),
    "1270": ("wrestling",          "contact"),
    "1272": ("gymnastics",         "non_contact"),
    "1279": ("hockey_ice",         "contact"),
    "1295": ("hockey_field",       "limited_contact"),
    "1333": ("skateboarding",      "limited_contact"),
    "3234": ("rugby",              "contact"),
    "3245": ("hockey_street",      "limited_contact"),
    "3254": ("cheerleading",       "limited_contact"),
    "3257": ("martial_arts_other", "contact"),
    "3272": ("hockey_unspecified", ""),
    "3274": ("swimming",           "non_contact"),
    "3276": ("water_polo",         "contact"),
    "3284": ("tennis",             "non_contact"),
    "5030": ("track_and_field",    "non_contact"),
    "5032": ("hockey_roller",      "limited_contact"),
    "5034": ("softball",           "limited_contact"),
    "5041": ("baseball",           "limited_contact"),
}

# In the hadley CSV body_part is human-readable text.
# Body Part 88 = "Mouth", Body Part 76 = "Face" (per the 2024 coding manual).
PRIMARY_BODY_PART = "Mouth"
SECONDARY_BODY_PART = "Face"

# Diagnosis text patterns suggesting dental involvement
DENTAL_DX_PATTERNS = re.compile(
    r"\b(tooth|teeth|dental|avuls|luxat|crown\s+fract|root\s+fract|incisor|"
    r"molar|canine|enamel|dentin|pulp|orthodont|mandibul|maxill|alveolar)",
    re.IGNORECASE,
)


def days_to_year(d):
    """hadley encodes dates as integer days since 1970-01-01 (R convention)."""
    try:
        days = int(float(d))
    except (TypeError, ValueError):
        return None
    try:
        return (date(1970, 1, 1) + timedelta(days=days)).year
    except (OverflowError, ValueError):
        return None


def filter_row(row):
    """Return (sport, sport_cat, kept_reason) or None."""
    # prod1 is "3299.0" or "1205.0" — strip ".0"
    p1_raw = (row.get("prod1") or "").strip()
    try:
        p1 = str(int(float(p1_raw)))
    except (TypeError, ValueError):
        return None
    if p1 not in SPORT_PRODUCT_CODES:
        return None

    bp = (row.get("body_part") or "").strip()
    if bp == PRIMARY_BODY_PART:
        body_keep = "primary"
    elif bp == SECONDARY_BODY_PART:
        dx = (row.get("diag") or "") + " " + (row.get("diag_other") or "") + " " + (row.get("narrative") or "")
        if not DENTAL_DX_PATTERNS.search(dx):
            return None
        body_keep = "secondary_dental"
    else:
        return None

    try:
        age = int(float(row.get("age", "")))
    except (TypeError, ValueError):
        return None
    # NEISS quirk: <2y coded as 200+months. hadley appears to have left this raw.
    if age >= 200 or age < 5 or age > 22:
        return None

    sport, sport_cat = SPORT_PRODUCT_CODES[p1]
    return sport, sport_cat, body_keep, age


def main():
    if not RAW.exists():
        print(f"ERROR: {RAW} not found. Did scripts/12 prereq finish?")
        sys.exit(1)

    by_year = {}
    counts = {"total": 0, "kept": 0}
    with RAW.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            counts["total"] += 1
            if counts["total"] % 200000 == 0:
                print(f"  scanned {counts['total']:,} rows, kept {counts['kept']}")
            res = filter_row(row)
            if res is None:
                continue
            sport, sport_cat, body_keep, age = res
            yr = days_to_year(row.get("trmt_date"))
            if yr is None:
                continue
            row["__sport__"] = sport
            row["__sport_category__"] = sport_cat
            row["__body_part_label__"] = "Mouth" if body_keep == "primary" else "Face_with_dental"
            row["__year__"] = yr
            row["__age_int__"] = age
            by_year.setdefault(yr, []).append(row)
            counts["kept"] += 1

    print(f"\nScanned {counts['total']:,} rows. Kept {counts['kept']:,} youth dental sport cases across years: {sorted(by_year)}")

    # Per-year output
    all_rows = []
    for yr in sorted(by_year):
        rows = by_year[yr]
        path = OUT_DIR / f"neiss_dental_sports_hadley_{yr}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            if rows:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
        print(f"  {yr}: {len(rows):>4} rows -> {path.name}")
        all_rows.extend(rows)

    # Combined output
    if all_rows:
        path = OUT_DIR / "neiss_dental_sports_hadley_all.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
            w.writeheader()
            w.writerows(all_rows)
        print(f"\nCombined: {len(all_rows):,} rows -> {path.name}")


if __name__ == "__main__":
    main()
