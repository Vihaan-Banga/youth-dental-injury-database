#!/usr/bin/env python3
"""Write pilot extractions for three high-quality sources to stress-test the
data dictionary and surface harmonization decisions before the formal
extraction phase.

Pilots:
  collins2016  PMID 26408377 — National HS Sports-Related Injury Surveillance
               Study (RIO), 2008/09–2013/14, AE-denominator data, multiple sports
  labella2002  PMID 11782645 — NCAA Division I men's college basketball MG
               cohort comparison, 1999–2000 season, AE-denominator data
  stewart2009  PMID 19614738 — NEISS retrospective 1990–2003 dental injuries
               in children 0–17, population-denominator surveillance

The extractions use the abstract-level data only — no full-text retrieval was
performed. Fields not visible in the abstract are left empty and a note is
recorded in `extraction_notes` indicating the field requires full-text review.
Every row carries `quality_flag = partial_data` until the full text is read.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/extracted"
OUT.mkdir(parents=True, exist_ok=True)

COLUMNS = [
    # Source identification
    "source_id", "citation", "doi", "pub_year", "study_type", "peer_reviewed",
    # Population
    "country", "region", "population_setting",
    "age_min", "age_max", "age_category", "extraction_basis",
    "sex", "level_of_play",
    # Exposure
    "sport_raw", "sport", "sport_category", "exposure_context", "subgroup_label",
    "sample_size", "athlete_exposures", "season_or_timeframe",
    # Outcome
    "injury_count", "injury_type_raw", "injury_category",
    "rate_raw", "rate_denominator_raw", "rate_per_1000_ae",
    # Protective equipment
    "mouthguard_required", "mouthguard_use_rate", "mouthguard_injury_relation",
    # Provenance and quality
    "extraction_date", "extractor", "extraction_notes", "quality_flag",
]


def write_csv(source_id, rows):
    path = OUT / f"{source_id}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            # Ensure every column is present (empty string if missing)
            w.writerow({c: r.get(c, "") for c in COLUMNS})
    print(f"wrote {path} ({len(rows)} rows)")


EXTRACTOR = "VB-AI-assisted-2026-05-22"
EXTRACTION_DATE = "2026-05-22"


# ----------------------------------------------------------------------------
# collins2016 — RIO HS surveillance (PMID 26408377)
# ----------------------------------------------------------------------------
collins_citation = (
    "Collins, C. L., McKenzie, L. B., Ferketich, A. K., Andridge, R., & Xiang, H. (2016). "
    "Dental injuries sustained by high school athletes in the United States, "
    "from 2008/2009 through 2013/2014 academic years. Dental Traumatology, 32(2), 121–127."
)
collins_common = {
    "source_id": "collins2016",
    "citation": collins_citation,
    "doi": "10.1111/edt.12228",
    "pub_year": 2016,
    "study_type": "surveillance",
    "peer_reviewed": "TRUE",
    "country": "US",
    "region": "",
    "population_setting": "school",
    "age_min": 14,
    "age_max": 18,
    "age_category": "adolescent",
    "extraction_basis": "youth_primary",
    "level_of_play": "school_varsity",
    "exposure_context": "all",
    "subgroup_label": "",
    "season_or_timeframe": "2008/09–2013/14 academic years",
    "mouthguard_required": "no",
    "mouthguard_injury_relation": "analyzed",
    "extraction_date": EXTRACTION_DATE,
    "extractor": EXTRACTOR,
}
# Aggregate row (all sports pooled)
collins_aggregate = dict(collins_common,
    sex="mixed",
    sport_raw="All sports (aggregate)",
    sport="all_sports_aggregate",
    sport_category="",
    sample_size="",
    athlete_exposures=24_787_258,
    injury_count=222,
    injury_type_raw="dental injuries (unspecified type)",
    injury_category="unspecified_dental",
    rate_raw=0.90,
    rate_denominator_raw="per 100,000 athlete-exposures",
    rate_per_1000_ae=round(222 / 24_787_258 * 1000, 4),  # = 0.0090
    mouthguard_use_rate=round((1 - 0.725), 3),  # 27.5% of injured athletes wore MG
    extraction_notes=(
        "Aggregate row across all reported sports. Mouthguard use rate is "
        "computed from abstract: 72.5% of injured athletes were not wearing a MG, "
        "so 27.5% were — note this is MG use AT TIME OF INJURY (not population "
        "prevalence). 95.9% of worn MGs were self-fitted. Per-sport rates by "
        "competition vs practice not extracted at aggregate level (see other rows)."
    ),
    quality_flag="partial_data",
)
# Sport-specific rows visible in the abstract
collins_field_hockey = dict(collins_common,
    sex="female",
    sport_raw="girls' field hockey",
    sport="hockey_field",
    sport_category="limited_contact",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    injury_type_raw="dental injuries (unspecified type)",
    injury_category="unspecified_dental",
    rate_raw=3.9,
    rate_denominator_raw="per 100,000 athlete-exposures",
    rate_per_1000_ae=0.039,
    extraction_notes=(
        "Highest sport-specific rate reported in the abstract. Denominator "
        "(per 100k AE) was the headline metric; injury_count and "
        "athlete_exposures per-sport require full text."
    ),
    quality_flag="partial_data",
)
collins_basketball_m = dict(collins_common,
    sex="male",
    sport_raw="boys' basketball",
    sport="basketball",
    sport_category="limited_contact",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    injury_type_raw="dental injuries (unspecified type)",
    injury_category="unspecified_dental",
    rate_raw=2.6,
    rate_denominator_raw="per 100,000 athlete-exposures",
    rate_per_1000_ae=0.026,
    extraction_notes=(
        "Second-highest sport-specific rate reported in abstract. Per-sport "
        "injury counts and AE denominators require full text."
    ),
    quality_flag="partial_data",
)
# Mechanism-stratified rows (competition vs practice) at the aggregate level
collins_competition = dict(collins_common,
    sex="mixed",
    sport_raw="All sports (competition)",
    sport="all_sports_aggregate",
    sport_category="",
    exposure_context="competition",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    injury_type_raw="dental injuries (unspecified type)",
    injury_category="unspecified_dental",
    rate_raw=1.8,
    rate_denominator_raw="per 100,000 athlete-exposures (competition only)",
    rate_per_1000_ae=0.018,
    extraction_notes=(
        "Rate during competition only. Abstract reports RR competition vs "
        "practice = 3.1 (95% CI 2.3–4.0)."
    ),
    quality_flag="partial_data",
)
collins_practice = dict(collins_common,
    sex="mixed",
    sport_raw="All sports (practice)",
    sport="all_sports_aggregate",
    sport_category="",
    exposure_context="practice",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    injury_type_raw="dental injuries (unspecified type)",
    injury_category="unspecified_dental",
    rate_raw=0.6,
    rate_denominator_raw="per 100,000 athlete-exposures (practice only)",
    rate_per_1000_ae=0.006,
    extraction_notes="Rate during practice only.",
    quality_flag="partial_data",
)
write_csv("collins2016", [
    collins_aggregate, collins_field_hockey, collins_basketball_m,
    collins_competition, collins_practice,
])


# ----------------------------------------------------------------------------
# labella2002 — NCAA Div I men's college basketball MG cohort (PMID 11782645)
# ----------------------------------------------------------------------------
labella_citation = (
    "Labella, C. R., Smith, B. W., & Sigurdsson, A. (2002). "
    "Effect of mouthguards on dental injuries and concussions in college basketball. "
    "Medicine and Science in Sports & Exercise, 34(1), 41–44."
)
labella_common = {
    "source_id": "labella2002",
    "citation": labella_citation,
    "doi": "10.1097/00005768-200201000-00007",
    "pub_year": 2002,
    "study_type": "cohort",
    "peer_reviewed": "TRUE",
    "country": "US",
    "region": "",
    "population_setting": "club",  # NCAA collegiate athletic programs
    "age_min": 18,
    "age_max": 22,
    "age_category": "collegiate",
    "extraction_basis": "youth_primary",
    "sex": "male",
    "level_of_play": "elite",  # NCAA Division I
    "sport_raw": "men's college basketball",
    "sport": "basketball",
    "sport_category": "limited_contact",
    "exposure_context": "all",
    "season_or_timeframe": "1999–2000 season",
    "mouthguard_required": "no",
    "mouthguard_injury_relation": "analyzed",
    "extraction_date": EXTRACTION_DATE,
    "extractor": EXTRACTOR,
    "injury_type_raw": "dental injuries",
    "injury_category": "unspecified_dental",
}
# Two rows: mouthguard users vs nonusers
labella_mg_users = dict(labella_common,
    subgroup_label="mouthguard_users",
    sample_size=50,  # teams; individual count not in abstract
    athlete_exposures=8663,
    injury_count="",
    rate_raw=0.12,
    rate_denominator_raw="per 1000 athlete-exposures (custom-fitted MG users)",
    rate_per_1000_ae=0.12,
    mouthguard_use_rate=1.0,  # by construction — this subgroup
    extraction_notes=(
        "Subgroup: athletes using custom-fitted mouthguards. AE = 8663 of 70,936 "
        "total (12.2% of AE). Injury count not directly in abstract; back-calc "
        "from rate × AE = ~1 injury. Confirm with full text."
    ),
    quality_flag="partial_data",
)
labella_mg_nonusers = dict(labella_common,
    subgroup_label="mouthguard_nonusers",
    sample_size=50,  # teams
    athlete_exposures=70_936 - 8_663,  # = 62,273
    injury_count="",
    rate_raw=0.67,
    rate_denominator_raw="per 1000 athlete-exposures (non-MG users)",
    rate_per_1000_ae=0.67,
    mouthguard_use_rate=0.0,  # by construction
    extraction_notes=(
        "Subgroup: athletes NOT using custom-fitted mouthguards. AE = 62,273 "
        "(= 70,936 total − 8,663 MG users). Injury count not directly in abstract; "
        "back-calc from rate × AE ≈ 42 injuries. Confirm with full text. "
        "Abstract reports P<0.05 for MG vs non-MG dental injury rate difference."
    ),
    quality_flag="partial_data",
)
write_csv("labella2002", [labella_mg_users, labella_mg_nonusers])


# ----------------------------------------------------------------------------
# stewart2009 — NEISS pediatric dental injuries 1990–2003 (PMID 19614738)
# ----------------------------------------------------------------------------
stewart_citation = (
    "Stewart, G. B., Shields, B. J., Fields, S., Comstock, R. D., & Smith, G. A. (2009). "
    "Consumer products and activities associated with dental injuries to children "
    "treated in United States emergency departments, 1990–2003. "
    "Dental Traumatology, 25(4), 399–405."
)
stewart_common = {
    "source_id": "stewart2009",
    "citation": stewart_citation,
    "doi": "10.1111/j.1600-9657.2009.00800.x",
    "pub_year": 2009,
    "study_type": "surveillance",
    "peer_reviewed": "TRUE",
    "country": "US",
    "region": "",
    "population_setting": "mixed",  # NEISS ED-treated, all settings
    "sex": "mixed",
    "level_of_play": "unspecified",
    "exposure_context": "all",
    "subgroup_label": "",
    "season_or_timeframe": "1990–2003",
    "mouthguard_required": "unspecified",
    "mouthguard_use_rate": "",
    "mouthguard_injury_relation": "not_addressed",
    "extraction_date": EXTRACTION_DATE,
    "extractor": EXTRACTOR,
    "injury_type_raw": "dental injuries (unspecified type) treated in US EDs",
    "injury_category": "unspecified_dental",
}
# Aggregate row for children 0–17
stewart_aggregate = dict(stewart_common,
    age_min=0,
    age_max=17,
    age_category="mixed",  # spans youth + adolescent + sub-5
    extraction_basis="youth_primary",
    sport_raw="all activities (aggregate; not sport-restricted)",
    sport="all_activities_aggregate",
    sport_category="",
    sample_size="",
    athlete_exposures="",
    injury_count=22000,  # average annual
    rate_raw=31.6,
    rate_denominator_raw="per 100,000 children <18 yrs per year (population denominator)",
    rate_per_1000_ae="",  # NEISS uses population denom, not AE
    extraction_notes=(
        "Population-denominator surveillance, NOT athlete-exposure denominator — "
        "rate_per_1000_ae left empty (incompatible denominators). NEISS counts all "
        "ED-treated dental injuries, not only sport-related; sport subset is "
        "described qualitatively in the abstract (highest in 13–17 group, "
        "baseball and basketball leading). Source's age range 0–17 partially "
        "overlaps the 5–22 inclusion floor; per PROTOCOL §3.1 the source qualifies "
        "(majority within scope)."
    ),
    quality_flag="partial_data",
)
# Per-dentition-stage rows (qualitative only from abstract; counts not given per stage)
stewart_primary = dict(stewart_common,
    age_min=0,
    age_max=6,
    age_category="unspecified",  # band crosses §3.1 inclusion floor (5+); majority sub-youth
    extraction_basis="youth_primary",
    sport_raw="primary dentition group — home structures/furniture leading",
    sport="non_sport_setting",
    sport_category="",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    rate_raw="",
    rate_denominator_raw="",
    rate_per_1000_ae="",
    extraction_notes=(
        "Children with primary dentition (<7y). Abstract states >50% of all "
        "dental injuries in the dataset; products were predominantly home "
        "structures/furniture (non-sport). Numerical counts per dentition stage "
        "require full text."
    ),
    quality_flag="partial_data",
)
stewart_mixed = dict(stewart_common,
    age_min=7,
    age_max=12,
    age_category="youth",
    extraction_basis="youth_primary",
    sport_raw="mixed dentition — outdoor recreational products; ~half bicycle",
    sport="recreational_mixed",
    sport_category="",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    rate_raw="",
    rate_denominator_raw="",
    rate_per_1000_ae="",
    extraction_notes=(
        "Children with mixed dentition (7–12y). Outdoor recreational "
        "products/activities led; ~50% bicycle-associated. Numerical counts "
        "per stage require full text."
    ),
    quality_flag="partial_data",
)
stewart_permanent = dict(stewart_common,
    age_min=13,
    age_max=17,
    age_category="adolescent",
    extraction_basis="youth_primary",
    sport_raw="permanent dentition — sports-related products led; baseball + basketball top",
    sport="sports_aggregate",
    sport_category="",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    rate_raw="",
    rate_denominator_raw="",
    rate_per_1000_ae="",
    extraction_notes=(
        "13–17y adolescents with permanent dentition. Sports-related products "
        "led this band; baseball and basketball topped the sport list. Per-sport "
        "counts require full text. Note: would map to two separate sport-specific "
        "rows (`baseball`, `basketball`) when full text is extracted."
    ),
    quality_flag="partial_data",
)
write_csv("stewart2009", [
    stewart_aggregate, stewart_primary, stewart_mixed, stewart_permanent,
])

print()
print("Pilot extractions written. Use these to validate the data dictionary "
      "before scaling extraction. Surfaced harmonization issues are documented "
      "in docs/decisions.md under the 2026-05-22 pilot-extraction entry.")
