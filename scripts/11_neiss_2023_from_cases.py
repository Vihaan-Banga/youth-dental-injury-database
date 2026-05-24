#!/usr/bin/env python3
"""Generate per-sport / per-age-band NEISS 2023 extraction rows from the
filtered case-level data at data/extracted/neiss_dental_sports_neiss_2023.csv.

Replaces the aggregate-only neiss2023.csv produced by scripts/10_neiss_2023_aggregate.py
(written before the user actually got the download working).

Rows produced:
  - 1 aggregate row (all sports, all youth 5-22)
  - 3 age-band rows (youth 5-12, adolescent 13-17, collegiate 18-22) across all sports
  - 1 row per sport with >= 5 raw cases (mixed sex, all youth)
  - 2 sex rows (male / female) across all sports, all youth — context for the 83% male signal

Each row's injury_count is the raw NEISS case count. The weighted national
estimate (sum of the NEISS Weight column for matching cases) is recorded in
extraction_notes — the data dictionary doesn't currently have a dedicated
column for it (proposed for next session in docs/decisions.md).
"""

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/vihaanbanga/youth-dental-injury-database")
FILTERED = ROOT / "data/extracted/neiss_dental_sports_neiss_2023.csv"
OUT = ROOT / "data/extracted/neiss2023.csv"

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

CITATION = (
    "Consumer Product Safety Commission. National Electronic Injury "
    "Surveillance System (NEISS), 2006-2025 (online database, released "
    "April 2026). Case-level extract: Body Part = 88 (Mouth) × all 23 "
    "sport-related product codes × treatment dates 01/01/2023-12/31/2023. "
    "Retrieved via https://www.cpsc.gov/cgibin/NEISSQuery/ on 2026-05-23."
)


def parse_filtered():
    rows = list(csv.DictReader(open(FILTERED)))
    cases = []
    for r in rows:
        try:
            age = int(r["Age"])
            wt = float(r["Weight"]) if r["Weight"] else 0.0
            sex_code = r["Sex"]
            sex = {"1": "male", "2": "female"}.get(sex_code, "unspecified")
            cases.append({
                "age": age,
                "sex": sex,
                "sport": r["__sport__"],
                "sport_category": r["__sport_category__"],
                "weight": wt,
            })
        except (ValueError, KeyError):
            continue
    return cases


def age_band(age):
    if 5 <= age <= 12: return ("youth", 5, 12, "youth_primary")
    if 13 <= age <= 17: return ("adolescent", 13, 17, "youth_primary")
    if 18 <= age <= 22: return ("collegiate", 18, 22, "youth_primary")
    return None  # outside scope, shouldn't occur (filter already restricts)


# Build the rows
cases = parse_filtered()
print(f"loaded {len(cases)} filtered cases", flush=True)

# Common template
common = {
    "source_id": "neiss2023",
    "citation": CITATION,
    "doi": "",
    "pub_year": 2023,
    "study_type": "surveillance",
    "peer_reviewed": "FALSE",  # surveillance system itself
    "country": "US",
    "region": "",
    "population_setting": "mixed",
    "level_of_play": "mixed",
    "season_or_timeframe": "2023 calendar year",
    "injury_type_raw": "ED-treated mouth injury (NEISS Body_Part = 88, includes teeth) — sport-related (Product_1 ∈ 23 sport codes)",
    "injury_category": "unspecified_dental",
    "mouthguard_required": "unspecified",
    "mouthguard_use_rate": "",
    "mouthguard_injury_relation": "not_addressed",
    "extraction_date": "2026-05-23",
    "extractor": "VB-AI-assisted-2026-05-23",
    "exposure_context": "all",
    "extraction_basis": "youth_primary",
}


def make_row(label, subset, *, age_min, age_max, age_category, sex,
             sport_raw, sport, sport_category, subgroup_label, extra_note=""):
    n = len(subset)
    weighted = sum(c["weight"] for c in subset)
    note = (
        f"Raw NEISS case count for {label}; "
        f"weighted national estimate = {weighted:,.0f}. "
        f"Filtered from neiss_dental_sports_neiss_2023.csv on 2026-05-23. "
        + extra_note
    ).strip()
    return dict(common,
        age_min=age_min, age_max=age_max, age_category=age_category,
        sex=sex,
        sport_raw=sport_raw, sport=sport, sport_category=sport_category,
        subgroup_label=subgroup_label,
        sample_size="",
        athlete_exposures="",
        injury_count=n,
        rate_raw="",
        rate_denominator_raw="",
        rate_per_1000_ae="",  # NEISS uses population denominator not AE
        extraction_notes=note,
        quality_flag="partial_data" if n >= 5 else "review_needed",
    )


rows = []

# 1. Aggregate row — all sports, all youth 5-22
rows.append(make_row(
    "all sports × all youth (5-22)", cases,
    age_min=5, age_max=22, age_category="mixed", sex="mixed",
    sport_raw="all 23 sport-related product codes",
    sport="all_sports_aggregate", sport_category="",
    subgroup_label="all_youth_aggregate",
    extra_note="Headline 2023 NEISS rollup for the project's scope.",
))

# 2. Age-band rows (across all sports)
for cat, lo, hi, _ in (
    ("youth", 5, 12, "youth_primary"),
    ("adolescent", 13, 17, "youth_primary"),
    ("collegiate", 18, 22, "youth_primary"),
):
    subset = [c for c in cases if lo <= c["age"] <= hi]
    rows.append(make_row(
        f"all sports × {cat} ({lo}-{hi})", subset,
        age_min=lo, age_max=hi, age_category=cat, sex="mixed",
        sport_raw=f"all 23 sport-related product codes ({cat} band)",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label=f"age_band_{cat}",
    ))

# 3. Per-sport rows (mixed sex, all youth, only sports with >=5 cases)
sport_groups = defaultdict(list)
sport_cats = {}
for c in cases:
    sport_groups[c["sport"]].append(c)
    sport_cats[c["sport"]] = c["sport_category"]

for sport, subset in sorted(sport_groups.items(), key=lambda x: -len(x[1])):
    if len(subset) < 5:
        continue
    rows.append(make_row(
        f"{sport} × all youth (5-22)", subset,
        age_min=5, age_max=22, age_category="mixed", sex="mixed",
        sport_raw=sport.replace("_", " "),
        sport=sport, sport_category=sport_cats[sport],
        subgroup_label="",  # main per-sport row
    ))

# 4. Sex-stratified all-sport rows
for sex in ("male", "female"):
    subset = [c for c in cases if c["sex"] == sex]
    rows.append(make_row(
        f"all sports × {sex} × all youth (5-22)", subset,
        age_min=5, age_max=22, age_category="mixed", sex=sex,
        sport_raw=f"all 23 sport-related product codes ({sex})",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label=f"sex_{sex}",
    ))

# Write
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLUMNS)
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, "") for c in COLUMNS})
print(f"wrote {OUT} ({len(rows)} rows)")

# Print summary
print("\nRow summary:")
for r in rows:
    label = f"{r['sport']} × {r['age_category']} × {r['sex']}"
    sg = f" [{r['subgroup_label']}]" if r['subgroup_label'] else ""
    print(f"  {r['injury_count']:>4}  {label}{sg}")
