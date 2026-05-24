#!/usr/bin/env python3
"""Turn the hadley/neiss 2013-2017 per-year filtered case-level CSVs into
master.csv extraction rows (one extraction file per year).

Mirrors the structure of scripts/11_neiss_2023_from_cases.py — for each year:
  - 1 aggregate row (all sports, all youth 5-22)
  - 3 age-band rows (youth 5-12, adolescent 13-17, collegiate 18-22)
  - 1 row per sport with >= 5 raw cases
  - 2 sex rows (male / female, all youth)

Source IDs: neiss2013, neiss2014, neiss2015, neiss2016, neiss2017.
"""

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/vihaanbanga/youth-dental-injury-database")
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
    "Surveillance System (NEISS), {year} treatment-year data, retrieved "
    "from the hadley/neiss historical archive at "
    "https://github.com/hadley/neiss (2013-2017 5-year window). "
    "Filtered to body part = 88 (Mouth, primary) OR 76 (Face) with dental "
    "diagnosis × all 23 sport-related product codes × ages 5-22."
)


def parse_year(year):
    fpath = OUT / f"neiss_dental_sports_hadley_{year}.csv"
    cases = []
    for r in csv.DictReader(open(fpath)):
        try:
            age = int(r["__age_int__"])
            wt = float(r["weight"]) if r["weight"] else 0.0
            # hadley pre-processed Sex column → "Male" / "Female"
            sex_raw = (r.get("sex") or "").strip()
            sex = {"Male": "male", "Female": "female"}.get(sex_raw, "unspecified")
            cases.append({
                "age": age, "sex": sex,
                "sport": r["__sport__"],
                "sport_category": r["__sport_category__"],
                "body_part_label": r["__body_part_label__"],
                "weight": wt,
            })
        except (ValueError, KeyError):
            continue
    return cases


def make_row(source_id, year, label, subset, *,
             age_min, age_max, age_category, sex,
             sport_raw, sport, sport_category, subgroup_label, extra_note=""):
    n = len(subset)
    weighted = sum(c["weight"] for c in subset)
    facial_with_dental = sum(1 for c in subset if c["body_part_label"] == "Face_with_dental")
    note_parts = [
        f"Raw NEISS case count for {label}, treatment year {year}",
        f"weighted national estimate = {weighted:,.0f}",
    ]
    if facial_with_dental > 0:
        note_parts.append(
            f"includes {facial_with_dental} cases where mouth was secondary "
            f"body-part to Face (recovered via dental-diagnosis text match)"
        )
    note_parts.append(
        "Source: hadley/neiss historical archive (2013-2017). "
        "Filtered by scripts/12_neiss_hadley_filter.py."
    )
    if extra_note:
        note_parts.append(extra_note)
    return {
        "source_id": source_id,
        "citation": CITATION_TPL.format(year=year),
        "doi": "",
        "pub_year": year,
        "study_type": "surveillance",
        "peer_reviewed": "FALSE",
        "country": "US",
        "region": "",
        "population_setting": "mixed",
        "age_min": age_min, "age_max": age_max, "age_category": age_category,
        "extraction_basis": "youth_primary",
        "sex": sex,
        "level_of_play": "mixed",
        "sport_raw": sport_raw,
        "sport": sport, "sport_category": sport_category,
        "exposure_context": "all",
        "subgroup_label": subgroup_label,
        "sample_size": "",
        "athlete_exposures": "",
        "season_or_timeframe": f"{year} calendar year",
        "injury_count": n,
        "injury_type_raw": "ED-treated mouth injury (NEISS Body_Part = 88, primary, or 76+dental) — sport-related (Product_1 ∈ 23 sport codes)",
        "injury_category": "unspecified_dental",
        "rate_raw": "",
        "rate_denominator_raw": "",
        "rate_per_1000_ae": "",
        "mouthguard_required": "unspecified",
        "mouthguard_use_rate": "",
        "mouthguard_injury_relation": "not_addressed",
        "extraction_date": "2026-05-23",
        "extractor": "VB-AI-assisted-2026-05-23",
        "extraction_notes": ". ".join(note_parts) + ".",
        "quality_flag": "partial_data" if n >= 5 else "review_needed",
    }


def build_year(year):
    cases = parse_year(year)
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

    # 3. Per-sport (>= 5 cases)
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
            sport=sport, sport_category=sport_cats[sport],
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


for year in (2013, 2014, 2015, 2016, 2017):
    source_id, rows = build_year(year)
    path = OUT / f"{source_id}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLUMNS})
    print(f"wrote {path.name} ({len(rows)} rows)")
