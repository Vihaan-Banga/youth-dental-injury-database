#!/usr/bin/env python3
"""Capture the NEISS 2023 aggregate count as a single extraction row.

Source: CPSC NEISS On-Line Query (https://www.cpsc.gov/cgibin/NEISSQuery/),
manually queried 2026-05-23 by the project lead. The new (2025-redesigned)
NEISS web UI does not expose a case-level download, only the aggregate
"Number of Cases" + "National Estimate" summary table. We capture that
summary table as one row of master.csv.

Query parameters (per the user-selected display on the NEISS results page):
- Treatment Dates: 01/01/2023 - 12/31/2023
- Body Part: 88 (Mouth, includes teeth) — primary filter
- Product 1: all 23 sport codes (1205, 1207, 1211, 1215, 1266, 1267, 1270,
  1272, 1279, 1295, 1333, 3234, 3245, 3254, 3257, 3272, 3274, 3276, 3284,
  5030, 5032, 5034, 5041) — see docs/decisions.md 2026-05-21 NEISS code map.
- Age: not restricted (full range)

Results:
- Number of Cases: 807 (raw NEISS records)
- National Estimate: 23,725 (weighted)

Limitations / caveats (logged in extraction_notes):
- This is the full age range — NOT filtered to 5-22. The age subset is
  buried inside the case-level data we couldn't download. The age-stratified
  rows from this query require either (a) the new NEISS UI to add a
  download button back, (b) the CPSC FOIA path, or (c) the hadley/neiss
  historical archive for older years.
- Body Part 76 (Face) was NOT queried — only Mouth (88). If/when face is
  added it should be a separate row tagged exposure_context = "all" with
  a clear note that face-only-with-dental requires diagnosis-text filtering.
"""

import csv
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

# Two rows: (1) raw NEISS case count, (2) the CPSC-derived national estimate.
# Same underlying source/query — distinguish via subgroup_label.
common = {
    "source_id": "neiss2023",
    "citation": (
        "Consumer Product Safety Commission. National Electronic Injury "
        "Surveillance System (NEISS), 2006-2025 (online database, released "
        "April 2026). Query: Body Part = 88 (Mouth) × all 23 sport-related "
        "product codes × treatment dates 01/01/2023-12/31/2023. Retrieved "
        "via https://www.cpsc.gov/cgibin/NEISSQuery/ on 2026-05-23."
    ),
    "doi": "",
    "pub_year": 2023,  # year of treatment data, not publication
    "study_type": "surveillance",
    "peer_reviewed": "FALSE",  # surveillance system, not a journal article
    "country": "US",
    "region": "",
    "population_setting": "mixed",  # NEISS = ED treatment, all settings
    "age_min": 0,
    "age_max": 99,
    "age_category": "mixed",
    "extraction_basis": "youth_primary",  # source qualifies because it includes 5-22 subset (we just can't isolate)
    "sex": "mixed",
    "level_of_play": "mixed",
    "sport_raw": "all 23 sport-related product codes (combined)",
    "sport": "all_sports_aggregate",
    "sport_category": "",
    "exposure_context": "all",
    "season_or_timeframe": "2023 calendar year",
    "injury_type_raw": "ED-treated injuries with body-part = Mouth (NEISS code 88, includes teeth)",
    "injury_category": "unspecified_dental",
    "mouthguard_required": "unspecified",
    "mouthguard_use_rate": "",
    "mouthguard_injury_relation": "not_addressed",
    "extraction_date": "2026-05-23",
    "extractor": "VB-AI-assisted-2026-05-23",
    "quality_flag": "partial_data",
}

# Row 1 — raw NEISS case count (unweighted)
neiss_raw = dict(common,
    subgroup_label="raw_case_count_unweighted",
    sample_size="",
    athlete_exposures="",
    injury_count=807,
    rate_raw="",
    rate_denominator_raw="raw NEISS case count (unweighted, full age range; not population-denominator)",
    rate_per_1000_ae="",
    extraction_notes=(
        "Raw NEISS case count from CPSC online query — 807 actual hospital "
        "records reviewed across the NEISS hospital sample for treatment year "
        "2023, body part 88 (Mouth), one of 23 sport-related product codes. "
        "Note: this is the FULL age range (NEISS does not pre-stratify in the "
        "result table). The 5-22 subset requires either case-level data "
        "(not currently downloadable from the redesigned NEISS UI) or a "
        "case-level archive like hadley/neiss for older years. Mouthguard, "
        "age, and per-sport breakdowns are all locked inside the case-level "
        "rows we couldn't pull."
    ),
)

# Row 2 — CPSC's weighted national estimate
neiss_estimate = dict(common,
    subgroup_label="national_estimate_weighted",
    sample_size="",
    athlete_exposures="",
    injury_count=23725,
    rate_raw="",
    rate_denominator_raw="CPSC-published national estimate (weighted, full age range; not population-denominator)",
    rate_per_1000_ae="",
    extraction_notes=(
        "CPSC's weighted national estimate from the same query as the "
        "raw_case_count_unweighted row. The weight = ~29.4 per raw case "
        "(23725 / 807). Same caveats apply: full age range, not 5-22 only; "
        "no sport/age/MG breakdown available."
    ),
)

path = OUT / "neiss2023.csv"
with path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLUMNS)
    w.writeheader()
    for row in (neiss_raw, neiss_estimate):
        w.writerow({c: row.get(c, "") for c in COLUMNS})
print(f"wrote {path} (2 rows)")
