#!/usr/bin/env python3
"""Combine every per-source extraction in `data/extracted/` into the
harmonized master dataset at `data/harmonized/master.csv`.

This is the first end-to-end pass: it reads each extracted CSV, validates
its columns against DATA_DICTIONARY.md, and concatenates rows. If the
extraction schema drifts, this script flags it loudly instead of silently
writing a broken master.

Rules:
  - Skip files whose name starts with '_' (internal: _screening, _abstracts, etc.)
  - Skip files whose name starts with 'neiss_dental_sports_' — those are the
    raw NEISS filter outputs (full NEISS column set), not yet mapped to the
    data dictionary schema. They will get their own mapping script.
  - Every extraction must have exactly the columns in EXPECTED_COLUMNS; extra
    columns are warned and dropped; missing columns are added as empty.
  - No type coercion beyond what DictWriter does — values are written as
    strings; pandas-side analysis will re-type.

Output is deterministic: rows sorted by (source_id, sport, age_min) so
diffs are reviewable.
"""

import csv
from pathlib import Path

# Resolve relative to this script's location so it works on any machine / CI.
ROOT = Path(__file__).resolve().parent.parent
EXTRACTED_DIR = ROOT / "data/extracted"
HARMONIZED = ROOT / "data/harmonized/master.csv"

EXPECTED_COLUMNS = [
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


def main():
    files = [p for p in sorted(EXTRACTED_DIR.glob("*.csv"))
             if not p.name.startswith("_")
             and not p.name.startswith("neiss_dental_sports_")]
    if not files:
        print("No per-source extractions found in data/extracted/. Nothing to harmonize.")
        return

    all_rows = []
    issues = []
    for path in files:
        with path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            file_cols = reader.fieldnames or []
            unexpected = set(file_cols) - set(EXPECTED_COLUMNS)
            missing = set(EXPECTED_COLUMNS) - set(file_cols)
            if unexpected:
                issues.append(f"{path.name}: unexpected columns dropped: {sorted(unexpected)}")
            if missing:
                issues.append(f"{path.name}: missing columns (filled empty): {sorted(missing)}")
            for row in reader:
                # Coerce to the expected schema
                clean = {c: row.get(c, "") for c in EXPECTED_COLUMNS}
                all_rows.append(clean)
        print(f"  read {path.name}: {sum(1 for _ in open(path)) - 1} rows")

    # Sort deterministically
    def sort_key(r):
        try:
            age_min = int(r["age_min"])
        except (TypeError, ValueError):
            age_min = 999
        return (r["source_id"], r["sport"], age_min, r["extraction_basis"],
                r.get("exposure_context", ""), r.get("subgroup_label", ""))
    all_rows.sort(key=sort_key)

    HARMONIZED.parent.mkdir(parents=True, exist_ok=True)
    with HARMONIZED.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS)
        w.writeheader()
        w.writerows(all_rows)

    print(f"\nWrote {HARMONIZED.relative_to(ROOT)} — {len(all_rows)} rows from {len(files)} source(s)")
    if issues:
        print("\nSchema notes:")
        for line in issues:
            print(f"  - {line}")
    else:
        print("\nNo schema drift across extractions.")


if __name__ == "__main__":
    main()
