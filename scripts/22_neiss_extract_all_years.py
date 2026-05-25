#!/usr/bin/env python3
"""Generate per-year NEISS extraction CSVs from any combination of filtered
output files in data/extracted/neiss_dental_sports_*.csv.

Splits multi-year files by the year extracted from Treatment_Date and
emits one extraction CSV per treatment year (skipping 2023 to avoid
overlap with the existing scripts/11 output).

Each year's rows follow the same row structure as scripts/11_neiss_2023_from_cases.py:
  - 1 aggregate row
  - 3 age-band rows (youth 5-12 / adolescent 13-17 / collegiate 18-22)
  - 1 row per sport with >= 5 cases
  - 2 sex-stratified rows
"""

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/extracted"

COLUMNS = [
    "source_id", "citation", "doi", "pub_year", "study_type", "peer_reviewed",
    "country", "region", "population_setting",
    "age_min", "age_max", "age_category", "extraction_basis",
    "sex", "level_of_play",
    "sport_raw", "sport", "sport_category", "exposure_context", "subgroup_label",
    "sample_size", "athlete_exposures", "season_or_timeframe",
    "injury_count", "injury_type_raw", "injury_category",
    "rate_raw", "rate_denominator_raw", "rate_per_1000_ae",
    "mouthguard_required", "mouthguard_use_rate", "mouthguard_injury_relation",
    "extraction_date", "extractor", "extraction_notes", "quality_flag",
]

CITATION_TPL = (
    "Consumer Product Safety Commission. National Electronic Injury "
    "Surveillance System (NEISS), {year} treatment-year data. Filtered "
    "to body part = 88 (Mouth, primary or secondary, since 2019) × all 23 "
    "sport-related product codes × ages 5-22. Retrieved via "
    "https://www.cpsc.gov/cgibin/NEISSQuery/ in 2026."
)

# Years that already have their own extraction (don't overwrite):
SKIP_YEARS = {2013, 2014, 2015, 2016, 2017, 2023}


def parse_year(date_str):
    """NEISS treatment dates are MM/DD/YYYY."""
    try:
        return int(date_str.split("/")[-1])
    except (ValueError, IndexError):
        return None


def aggregate_by_year(filtered_path):
    """Return {year: [cases]} where each case is a dict of needed fields."""
    by_year = defaultdict(list)
    with filtered_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yr = parse_year(row.get("Treatment_Date", ""))
            if yr is None:
                continue
            try:
                age = int(row.get("Age", 0))
            except ValueError:
                continue
            if age >= 200 or age < 5 or age > 22:
                continue
            sex_code = row.get("Sex", "")
            sex = {"1": "male", "2": "female"}.get(sex_code, "unspecified")
            try:
                weight = float(row.get("Weight", 0))
            except ValueError:
                weight = 0.0
            by_year[yr].append({
                "age": age, "sex": sex,
                "sport": row["__sport__"],
                "sport_category": row["__sport_category__"],
                "body_part_label": row["__body_part_label__"],
                "weight": weight,
            })
    return by_year


def make_row(source_id, year, label, subset, *,
             age_min, age_max, age_category, sex,
             sport_raw, sport, sport_category, subgroup_label, extra_note=""):
    n = len(subset)
    weighted = sum(c["weight"] for c in subset)
    secondary_count = sum(1 for c in subset if "secondary" in c["body_part_label"])
    note_parts = [
        f"Raw NEISS case count for {label}, treatment year {year}",
        f"weighted national estimate = {weighted:,.0f}",
    ]
    if secondary_count > 0:
        note_parts.append(
            f"includes {secondary_count} cases where Mouth was the secondary body part "
            "(Body_Part_2 = 88, recovered after the 2026-05-24 filter fix)"
        )
    note_parts.append(
        "Source: CPSC NEISS online query (manually downloaded by project lead 2026-05-25), "
        "filtered by scripts/05_neiss_filter.py, split + extracted by scripts/22."
    )
    if extra_note:
        note_parts.append(extra_note)
    return {
        "source_id": source_id,
        "citation": CITATION_TPL.format(year=year),
        "doi": "", "pub_year": year, "study_type": "surveillance", "peer_reviewed": "FALSE",
        "country": "US", "region": "", "population_setting": "mixed",
        "age_min": age_min, "age_max": age_max, "age_category": age_category,
        "extraction_basis": "youth_primary",
        "sex": sex, "level_of_play": "mixed",
        "sport_raw": sport_raw, "sport": sport, "sport_category": sport_category,
        "exposure_context": "all", "subgroup_label": subgroup_label,
        "sample_size": "", "athlete_exposures": "",
        "season_or_timeframe": f"{year} calendar year",
        "injury_count": n,
        "injury_type_raw": "ED-treated mouth injury (NEISS Body_Part = 88, primary or secondary since 2019) — sport-related",
        "injury_category": "unspecified_dental",
        "rate_raw": "", "rate_denominator_raw": "", "rate_per_1000_ae": "",
        "mouthguard_required": "unspecified", "mouthguard_use_rate": "",
        "mouthguard_injury_relation": "not_addressed",
        "extraction_date": "2026-05-25", "extractor": "VB-AI-assisted-2026-05-25",
        "extraction_notes": ". ".join(note_parts) + ".",
        "quality_flag": "partial_data" if n >= 5 else "review_needed",
    }


def build_year_extraction(year, cases):
    """Produce the same row structure as scripts/11 for one year."""
    source_id = f"neiss{year}"
    rows = []

    # 1. Aggregate
    rows.append(make_row(source_id, year,
        "all sports × all youth (5-22)", cases,
        age_min=5, age_max=22, age_category="mixed", sex="mixed",
        sport_raw="all 23 sport-related product codes",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label="all_youth_aggregate",
    ))

    # 2. Age bands
    for cat, lo, hi in (("youth", 5, 12), ("adolescent", 13, 17), ("collegiate", 18, 22)):
        subset = [c for c in cases if lo <= c["age"] <= hi]
        rows.append(make_row(source_id, year,
            f"all sports × {cat} ({lo}-{hi})", subset,
            age_min=lo, age_max=hi, age_category=cat, sex="mixed",
            sport_raw=f"all 23 sport-related product codes ({cat} band)",
            sport="all_sports_aggregate", sport_category="",
            subgroup_label=f"age_band_{cat}",
        ))

    # 3. Per-sport (>= 5)
    sport_groups = defaultdict(list)
    sport_cats = {}
    for c in cases:
        sport_groups[c["sport"]].append(c)
        sport_cats[c["sport"]] = c["sport_category"]
    for sport, subset in sorted(sport_groups.items(), key=lambda x: -len(x[1])):
        if len(subset) < 5:
            continue
        rows.append(make_row(source_id, year,
            f"{sport} × all youth (5-22)", subset,
            age_min=5, age_max=22, age_category="mixed", sex="mixed",
            sport_raw=sport.replace("_", " "),
            sport=sport, sport_category=sport_cats[sport] or "",
            subgroup_label="",
        ))

    # 4. Sex
    for sex in ("male", "female"):
        subset = [c for c in cases if c["sex"] == sex]
        rows.append(make_row(source_id, year,
            f"all sports × {sex} × all youth (5-22)", subset,
            age_min=5, age_max=22, age_category="mixed", sex=sex,
            sport_raw=f"all 23 sport-related product codes ({sex})",
            sport="all_sports_aggregate", sport_category="",
            subgroup_label=f"sex_{sex}",
        ))

    return source_id, rows


def main():
    # Find all filtered files (excluding hadley which has its own pipeline)
    filtered = sorted(OUT.glob("neiss_dental_sports_neiss_*.csv"))
    print(f"Found {len(filtered)} filtered NEISS files")
    all_by_year = defaultdict(list)
    for fp in filtered:
        by_year = aggregate_by_year(fp)
        for yr, cases in by_year.items():
            print(f"  {fp.name}: {yr} → {len(cases)} cases")
            all_by_year[yr].extend(cases)

    # Generate per-year extractions
    new_years = sorted(y for y in all_by_year if y not in SKIP_YEARS)
    print(f"\nWill emit extractions for: {new_years} (skipping {sorted(SKIP_YEARS)})")
    for year in new_years:
        cases = all_by_year[year]
        source_id, rows = build_year_extraction(year, cases)
        path = OUT / f"{source_id}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            w.writeheader()
            for r in rows:
                w.writerow({c: r.get(c, "") for c in COLUMNS})
        print(f"  wrote {path.name} ({len(rows)} rows, {len(cases)} cases)")


if __name__ == "__main__":
    main()
