#!/usr/bin/env python3
"""Additional abstract-only extractions added 2026-05-23 while NEISS query
builder was down for maintenance.

Sources:
  azadani2023  PMID 36317716 — Dental Traumatology. Extends collins2016's
               RIO surveillance through 2019-20 (459 dental injuries in
               49.9M AE; per-sport rates, MG-at-injury).
  quarrie2020  PMID 31506903 — Sports Medicine. NZ Rugby ACC nationwide
               claims 2005-2017, ages 5-40 (635,657 claims, 2.0% dental).
               Multi-row per age band; demonstrates the youth_primary /
               adult_comparator split.
  welch2010    PMID 21197817 — NZ Dental Journal. NZ ACC sports dental
               1999-2008 (~28,000 claims/year); per-sport breakdown for the
               11-20 age group, which is squarely within youth_primary scope.

All extractions are from abstracts only — every row carries
quality_flag = 'partial_data' until a full-text re-extraction.
"""

import csv
from pathlib import Path

ROOT = Path("/Users/vihaanbanga/youth-dental-injury-database")
OUT = ROOT / "data/extracted"
OUT.mkdir(parents=True, exist_ok=True)

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


def write_csv(source_id, rows):
    path = OUT / f"{source_id}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLUMNS})
    print(f"wrote {path} ({len(rows)} rows)")


EXTRACTOR = "VB-AI-assisted-2026-05-23"
EXTRACTION_DATE = "2026-05-23"


# ----------------------------------------------------------------------------
# azadani2023 — PMID 36317716 — RIO HS surveillance 2005-2020 dental
# ----------------------------------------------------------------------------
azadani_citation = (
    "Azadani, E. N., Peng, J., Townsend, J. A., & Collins, C. L. (2023). "
    "Traumatic dental injuries in high school athletes in the United States "
    "of America from 2005 to 2020. Dental Traumatology, 39(1), 73-81."
)
azadani_common = {
    "source_id": "azadani2023",
    "citation": azadani_citation,
    "doi": "10.1111/edt.12800",
    "pub_year": 2023,
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
    "subgroup_label": "",
    "season_or_timeframe": "2005/06 through 2019/20 academic years",
    "mouthguard_required": "no",
    "mouthguard_injury_relation": "analyzed",
    "extraction_date": EXTRACTION_DATE,
    "extractor": EXTRACTOR,
    "injury_type_raw": "dental injuries (unspecified type)",
    "injury_category": "unspecified_dental",
}
azadani_overall = dict(azadani_common,
    sex="mixed",
    sport_raw="All sports (aggregate, RIO 2005/06-2019/20)",
    sport="all_sports_aggregate",
    sport_category="",
    exposure_context="all",
    sample_size="",
    athlete_exposures=49_987_927,
    injury_count=459,
    rate_raw=0.9,
    rate_denominator_raw="per 100,000 athlete-exposures",
    rate_per_1000_ae=round(459 / 49_987_927 * 1000, 5),  # = 0.00918
    mouthguard_use_rate=round(1 - 0.751, 3),  # 75.1% of injured were NOT wearing MG
    extraction_notes=(
        "15-year aggregate. 459 dental injuries / 108,574 total injuries = 0.4% "
        "of all athlete injuries. mouthguard_use_rate is *at time of injury* "
        "(24.9% wearing MG when injured), not population-level prevalence. "
        "Mechanism: 60.4% contact with another player, 31.9% with apparatus."
    ),
    quality_flag="partial_data",
)
azadani_competition = dict(azadani_common,
    sex="mixed",
    sport_raw="All sports (competition, RIO 2005/06-2019/20)",
    sport="all_sports_aggregate",
    sport_category="",
    exposure_context="competition",
    sample_size="",
    athlete_exposures="",
    injury_count=256,
    rate_raw="",
    rate_denominator_raw="per 100,000 athlete-exposures (competition only)",
    rate_per_1000_ae="",
    extraction_notes=(
        "Competition-only subset: 256 of 459 dental injuries (55.8%). RR vs "
        "practice = 3.6 (95% CI 3.0-4.4). AE denominator for competition not "
        "in abstract — needs full text."
    ),
    quality_flag="partial_data",
)
azadani_practice = dict(azadani_common,
    sex="mixed",
    sport_raw="All sports (practice, RIO 2005/06-2019/20)",
    sport="all_sports_aggregate",
    sport_category="",
    exposure_context="practice",
    sample_size="",
    athlete_exposures="",
    injury_count=200,
    rate_raw="",
    rate_denominator_raw="per 100,000 athlete-exposures (practice only)",
    rate_per_1000_ae="",
    extraction_notes=(
        "Practice-only subset: 200 of 459 dental injuries (43.6%). 3 injuries "
        "(0.7%) had unclear exposure context. AE denominator for practice not "
        "in abstract — needs full text."
    ),
    quality_flag="partial_data",
)
azadani_field_hockey = dict(azadani_common,
    sex="female",
    sport_raw="girls' field hockey",
    sport="hockey_field",
    sport_category="limited_contact",
    exposure_context="all",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    rate_raw=3.5,
    rate_denominator_raw="per 100,000 athlete-exposures",
    rate_per_1000_ae=0.035,
    mouthguard_use_rate="",  # population-level not stated
    extraction_notes=(
        "Highest per-sport rate among girls' sports. Per-sport AE denominator "
        "and injury count require full text."
    ),
    quality_flag="partial_data",
)
azadani_basketball_m = dict(azadani_common,
    sex="male",
    sport_raw="boys' basketball",
    sport="basketball",
    sport_category="limited_contact",
    exposure_context="all",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    rate_raw=2.4,
    rate_denominator_raw="per 100,000 athlete-exposures",
    rate_per_1000_ae=0.024,
    mouthguard_use_rate="",
    extraction_notes=(
        "Highest per-sport rate among boys' sports. Per-sport AE denominator "
        "and injury count require full text. Note: collins2016 (same surveillance, "
        "2008-2014 subset) reported boys' basketball = 2.6 per 100k AE — the rate "
        "is broadly stable across the longer window."
    ),
    quality_flag="partial_data",
)
write_csv("azadani2023", [
    azadani_overall, azadani_competition, azadani_practice,
    azadani_field_hockey, azadani_basketball_m,
])


# ----------------------------------------------------------------------------
# quarrie2020 — PMID 31506903 — NZ Rugby ACC claims 2005-2017
# ----------------------------------------------------------------------------
quarrie_citation = (
    "Quarrie, K., Gianotti, S., & Murphy, I. (2020). Injury Risk in New Zealand "
    "Rugby Union: A Nationwide Study of Injury Insurance Claims from 2005 to 2017. "
    "Sports Medicine, 50(2), 415-428."
)
quarrie_common = {
    "source_id": "quarrie2020",
    "citation": quarrie_citation,
    "doi": "10.1007/s40279-019-01217-3",
    "pub_year": 2020,
    "study_type": "surveillance",
    "peer_reviewed": "TRUE",
    "country": "NZ",
    "region": "",
    "population_setting": "mixed",  # community + competitive
    "sex": "mixed",
    "level_of_play": "mixed",  # community to elite
    "sport_raw": "rugby union (NZ)",
    "sport": "rugby",
    "sport_category": "contact",
    "exposure_context": "all",
    "subgroup_label": "",
    "season_or_timeframe": "2005-2017",
    "mouthguard_required": "unspecified",
    "mouthguard_use_rate": "",
    "mouthguard_injury_relation": "not_addressed",
    "extraction_date": EXTRACTION_DATE,
    "extractor": EXTRACTOR,
    "injury_type_raw": "dental injuries (subset of all injury claims)",
    "injury_category": "unspecified_dental",
}
# Dental injuries are 2.0% of 635,657 total claims = ~12,713 over 13 years
TOTAL_CLAIMS = 635_657
DENTAL_FRACTION = 0.020
total_dental = int(TOTAL_CLAIMS * DENTAL_FRACTION)  # 12,713

quarrie_overall = dict(quarrie_common,
    age_min=5,
    age_max=40,
    age_category="mixed",
    extraction_basis="youth_primary",  # source qualified via youth subset
    sample_size="",
    athlete_exposures="",
    injury_count=total_dental,
    rate_raw="",
    rate_denominator_raw="",
    rate_per_1000_ae="",
    extraction_notes=(
        "13-year aggregate across all ages 5-40. Dental = 2.0% of 635,657 "
        "total injury claims = 12,713 dental claims (computed). Per-age "
        "claim rates (probability of at least one claim per season) are "
        "reported in age-stratified rows below; this row is the topline."
    ),
    quality_flag="partial_data",
)
# Per-age-band probability-of-at-least-one-claim rates (rugby OVERALL — not dental specifically)
# But these still establish exposure denominators by age band.
# We can NOT use these probabilities as dental rates; rate_raw left empty.
age_bands = [
    (5, 6,  1.0,  "youth",       "youth_primary"),
    (7, 12, 8.3,  "youth",       "youth_primary"),
    (13, 17, 35,   "adolescent",  "youth_primary"),
    (18, 20, 53,   "collegiate",  "youth_primary"),
    (21, 30, 57,   "adult",       "adult_comparator"),
    (31, 40, 47,   "adult",       "adult_comparator"),
]
quarrie_rows = [quarrie_overall]
for lo, hi, season_prob, cat, basis in age_bands:
    row = dict(quarrie_common,
        age_min=lo, age_max=hi,
        age_category=cat,
        extraction_basis=basis,
        subgroup_label=f"age_{lo}_{hi}",
        injury_count="",  # dental count by age band not in abstract
        injury_type_raw="all rugby injury claims (any body site, dental is 2.0% overall)",
        injury_category="orofacial_with_dental",  # broader; dental is a fraction
        rate_raw=season_prob,
        rate_denominator_raw="probability (%) of at least one injury claim per season (any body site, not dental-specific)",
        rate_per_1000_ae="",
        extraction_notes=(
            f"Age band {lo}-{hi} years. This row's rate is the probability of "
            f"making at least one rugby injury claim per season (any body site), "
            f"not the dental-specific rate. Dental fraction (2.0% topline) is "
            f"likely lower in <13 yo (mostly soft-tissue) and higher in "
            f"adolescents/adults; abstract doesn't stratify dental by age. "
            f"Demographics: ~10% of players are female; female claim rate is "
            f"0.57x male overall."
        ),
        quality_flag="partial_data",
    )
    quarrie_rows.append(row)
write_csv("quarrie2020", quarrie_rows)


# ----------------------------------------------------------------------------
# welch2010 — PMID 21197817 — NZ ACC sports-related dental 1999-2008
# ----------------------------------------------------------------------------
welch_citation = (
    "Welch, C. L., Thomson, W. M., & Kennedy, R. (2010). ACC claims for "
    "sports-related dental trauma from 1999 to 2008: a retrospective analysis. "
    "New Zealand Dental Journal, 106(4), 137-142."
)
welch_common = {
    "source_id": "welch2010",
    "citation": welch_citation,
    "doi": "",  # NZDJ pre-2011 articles typically no DOI
    "pub_year": 2010,
    "study_type": "surveillance",
    "peer_reviewed": "TRUE",
    "country": "NZ",
    "region": "",
    "population_setting": "mixed",
    "level_of_play": "mixed",
    "subgroup_label": "",
    "season_or_timeframe": "1999-2008",
    "mouthguard_required": "unspecified",
    "mouthguard_use_rate": "",
    "mouthguard_injury_relation": "not_addressed",
    "extraction_date": EXTRACTION_DATE,
    "extractor": EXTRACTOR,
    "injury_type_raw": "sports-related dental trauma (ACC claims)",
    "injury_category": "unspecified_dental",
    "exposure_context": "all",
}
# 10-year average ~28,000 claims/yr; sport = 20.6-26.2% of claims
# 11-20yo = 41.7-44.4% of sports-related claims
# Sport-related: rugby 22.2-33.1%, water sports 14.2-20.8%, cycling rising
welch_overall = dict(welch_common,
    age_min=0,
    age_max=99,
    age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed",
    sport_raw="All sports (aggregate, ACC dental claims)",
    sport="all_sports_aggregate",
    sport_category="",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    rate_raw="",
    rate_denominator_raw="",
    rate_per_1000_ae="",
    extraction_notes=(
        "10-year aggregate, all ages. Annual new claims for orofacial injury "
        "(any cause) ranged 24,998-31,257 (~28k/yr; ~280k over 10 yrs). "
        "Sport-related = 20.6-26.2% of new claims. Across the 10 years, "
        "ages 11-20 made 41.7-44.4% of sports-related claims. Sex split: "
        "61.3% male, 38.7% female."
    ),
    quality_flag="partial_data",
)
welch_youth = dict(welch_common,
    age_min=11,
    age_max=20,
    age_category="mixed",  # adolescent (13-17) + collegiate (18-20) bands
    extraction_basis="youth_primary",
    sex="mixed",
    sport_raw="All sports (ages 11-20 subset, ACC dental claims)",
    sport="all_sports_aggregate",
    sport_category="",
    subgroup_label="age_11_20",
    sample_size="",
    athlete_exposures="",
    injury_count="",
    rate_raw="",
    rate_denominator_raw="",
    rate_per_1000_ae="",
    extraction_notes=(
        "Ages 11-20 made up 41.7-44.4% of sports-related dental claims "
        "across 1999-2008. Absolute count not in abstract; can be computed "
        "from full text or ACC raw."
    ),
    quality_flag="partial_data",
)
# Per-sport share within sports-related claims (10-year window)
welch_sport_rows = []
for sport_raw, sport, sport_cat, share_pct_low, share_pct_high in [
    ("rugby",         "rugby",                  "contact",         22.2, 33.1),
    ("water sports",  "swimming",               "non_contact",     14.2, 20.8),  # imperfect — water sports broader
    ("cycling",       "non_sport_setting",      "",                 1.5, 15.3),  # cycling not a §3.1 sport
    ("hockey",        "hockey_unspecified",     "",                 4.4, 4.4),
    ("basketball",    "basketball",             "limited_contact",  4.8, 4.8),
    ("soccer",        "football_association",   "limited_contact",  6.9, 6.9),
    ("cricket",       "all_activities_aggregate", "",               4.7, 4.7),  # cricket not in current taxonomy
    ("netball",       "all_activities_aggregate", "",               3.9, 3.9),  # netball not in current taxonomy
]:
    share_repr = f"{share_pct_low}-{share_pct_high}%" if share_pct_low != share_pct_high else f"{share_pct_low}%"
    # Use the raw sport name in subgroup_label so cricket/netball/cycling
    # rows don't collide on the all_activities_aggregate placeholder.
    welch_sport_rows.append(dict(welch_common,
        age_min=0, age_max=99,
        age_category="mixed",
        extraction_basis="youth_primary",
        sex="mixed",
        sport_raw=sport_raw,
        sport=sport,
        sport_category=sport_cat,
        subgroup_label=f"source_sport_{sport_raw.replace(' ', '_')}",
        injury_count="",
        rate_raw="",
        rate_denominator_raw=f"share of sports-related dental claims (range across 1999-2008): {share_repr}",
        rate_per_1000_ae="",
        extraction_notes=(
            f"Source reports this sport accounted for {share_repr} of sports-related "
            f"dental claims across 1999-2008. Absolute counts require full text. "
            f"NOTE: source's sport categories don't all map cleanly: 'water sports' "
            f"is broader than the project's `swimming` value; 'cycling', 'cricket', "
            f"and 'netball' are not currently in the §6.1 controlled vocabulary "
            f"(see docs/decisions.md for next-session taxonomy expansion). "
            f"subgroup_label preserves the source's original sport name for those "
            f"that collapse to the same placeholder sport value."
        ),
        quality_flag="review_needed" if sport in ("non_sport_setting", "all_activities_aggregate") else "partial_data",
    ))
write_csv("welch2010", [welch_overall, welch_youth] + welch_sport_rows)

print()
print("Done — 3 additional sources extracted. Run scripts/07_harmonize.py + "
      "scripts/08_validate.py to re-build master.csv.")
