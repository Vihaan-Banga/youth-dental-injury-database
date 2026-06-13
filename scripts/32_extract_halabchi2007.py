#!/usr/bin/env python3
"""Extraction — halabchi2007 (PMID 24198704), resolved from the
needs_human_review pile by full-text review on 2026-06-12.

Source: Halabchi F, Ziaee V, Lotfian S. (2007). Injury profile in women
Shotokan karate championships in Iran (2004-2005). Journal of Sports Science
& Medicine. Full text read via PMC3809047.

Prospective injury surveillance of 6 consecutive women's national Shotokan
karate championships, Iran, 2004-2005, across all age groups (youth
competitors present). 186 injuries from 1139 bouts / 1019 athletes
(0.163 injuries/bout; 183 injuries/1000 athletes). Dental injuries =
"tooth avulsion or subluxation" (3, 1.6% of injuries).

One pooled mixed-age row: the source does not stratify the dental count by
age, so a youth-only count cannot be isolated (quality_flag=partial_data).
The combined "avulsion or subluxation" count cannot be split into a single
Andreasen category, so injury_category=unspecified_dental with the raw
description preserved (see docs/decisions.md, 2026-06-12).
"""

import csv
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
EXTRACTOR, EDATE = "VB-AI-assisted-2026-06-12", "2026-06-12"


def make(sid, **kw):
    b = {c: "" for c in COLUMNS}
    b.update(source_id=sid, peer_reviewed="TRUE",
        extraction_basis="youth_primary", exposure_context="all",
        injury_category="unspecified_dental", mouthguard_required="unspecified",
        mouthguard_injury_relation="not_addressed",
        extraction_date=EDATE, extractor=EXTRACTOR, quality_flag="partial_data")
    b.update(kw)
    return b


def w(sid, rows):
    p = OUT / f"{sid}.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=COLUMNS)
        wr.writeheader()
        for r in rows:
            wr.writerow({c: r.get(c, "") for c in COLUMNS})
    print(f"wrote {p.name} ({len(rows)} rows)")


w("halabchi2007", [make("halabchi2007",
    citation="Halabchi F, Ziaee V, Lotfian S. (2007). Injury profile in women "
             "Shotokan karate championships in Iran (2004-2005). Journal of "
             "Sports Science & Medicine.",
    pub_year=2007, study_type="surveillance", peer_reviewed="TRUE",
    country="IR", population_setting="club",
    age_category="mixed", sex="female", level_of_play="elite",
    sport_raw="Shotokan karate", sport="martial_arts_other",
    sport_category="contact", exposure_context="competition",
    sample_size=1019, season_or_timeframe="2004-2005 (6 national championships)",
    injury_count=3,
    injury_type_raw="tooth avulsion or subluxation",
    injury_category="unspecified_dental",
    rate_raw=1.6, rate_denominator_raw="(%) of 186 recorded injuries (3 of 186)",
    mouthguard_required="yes", mouthguard_injury_relation="mentioned_only",
    extraction_notes=(
        "Full text via PMC3809047, 2026-06-12. Prospective injury recording, "
        "6 women's national Shotokan karate championships, all age groups; "
        "186 injuries / 1139 bouts / 1019 athletes (0.163/bout; 183/1000 "
        "athletes). Dental = 3 (1.6%) 'tooth avulsion or subluxation', not "
        "separable into avulsion vs luxation and not age-stratified, so one "
        "pooled mixed-age row with injury_category=unspecified_dental. "
        "Head/neck = 55.4% of injuries. Mouthguards stated compulsory in "
        "karate competition since 1994 (general statement, not sample-specific "
        "enforcement, so mouthguard_injury_relation=mentioned_only). "
        "Denominators are bouts/athletes, not athlete-exposures, so "
        "rate_per_1000_ae left empty."),
    quality_flag="partial_data")])
