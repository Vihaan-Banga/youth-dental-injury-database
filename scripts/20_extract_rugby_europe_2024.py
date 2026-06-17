#!/usr/bin/env python3
"""Extract U-18 rugby 7s match injury data from the Rugby Europe 2024
Injury Surveillance Report (PDF at data/raw/surveillance_reports/_international/).

Source-level details:
  - 2022/2023 Rugby Europe Sevens tournaments
  - Definition: injury preventing player participation for >1 day
  - Reported as injuries per 1000 player-match-hours
  - U-18 Championship + Trophy for both Men and Women separately

Head/face is the proxy for orofacial-with-dental in this report (the
underlying classification doesn't break out dental specifically; head/face
in rugby 7s commonly involves dental + lip/teeth — see World Rugby's
consensus statement).
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
CITATION = (
    "Rugby Europe. (March 2024). Injury Surveillance Report. Source: "
    "https://www.rugbyeurope.eu/media/gxwdngx2/re-injury-surveillance-report-march-2024.pdf. "
    "Covers 2022/2023 Rugby Europe Sevens tournaments at multiple competition tiers, "
    "including U-18 Men's and Women's Championship + Trophy."
)


def make(**kw):
    base = {c: "" for c in COLUMNS}
    base.update(
        source_id="rugby_europe_iss_2024", citation=CITATION,
        pub_year=2024, study_type="governing_body_report", peer_reviewed="FALSE",
        country="", region="Europe (multi-nation)",
        population_setting="club", level_of_play="elite",
        sport_raw="rugby union — Sevens (Rugby Europe U-18)",
        sport="rugby", sport_category="contact",
        exposure_context="competition",  # match-only data per their methods
        extraction_basis="youth_primary",
        season_or_timeframe="2022/2023 season",
        mouthguard_required="unspecified",
        mouthguard_injury_relation="not_addressed",
        extraction_date="2026-05-24",
        extractor="VB-AI-assisted-2026-05-24",
        quality_flag="partial_data",
    )
    base.update(kw)
    return base


rows = []

# ---- U-18 overall injury incidence per Table 2 ----
rows.append(make(
    age_min=15, age_max=18, age_category="adolescent",
    sex="male", subgroup_label="u18_men_championship",
    athlete_exposures=int(111.1 * 1000),  # converting PMH × 1000 = player-match-units; note denominator stays per-1000-PMH
    sample_size=34,  # 34 player-matches from the report
    injury_count=7,
    injury_type_raw="all-cause match injury (>1 day loss) — U-18 Men's Championship",
    injury_category="orofacial_with_dental",
    rate_raw=63.0,
    rate_denominator_raw="per 1000 player-match-hours (Sevens — U18 Men's Championship)",
    rate_per_1000_ae="",  # C11: player-match-hours is not an athlete-exposure denominator (decisions 2026-06-13)
    extraction_notes="Table 2. U18 Men's Championship 2022/23 Rugby Europe Sevens. 7 injuries / 111.1 PMH. Head/face = 3/7 (42.8%) per Table 5.",
))
rows.append(make(
    age_min=15, age_max=18, age_category="adolescent",
    sex="male", subgroup_label="u18_men_trophy",
    athlete_exposures=int(127.4 * 1000),
    sample_size=39, injury_count=9,
    injury_type_raw="all-cause match injury (>1 day loss) — U-18 Men's Trophy",
    injury_category="orofacial_with_dental",
    rate_raw=70.6,
    rate_denominator_raw="per 1000 player-match-hours (Sevens — U18 Men's Trophy)",
    rate_per_1000_ae="",  # C11: player-match-hours is not an athlete-exposure denominator (decisions 2026-06-13)
    extraction_notes="Table 2. U18 Men's Trophy. 9 injuries / 127.4 PMH. Head/face = 1/9 (11.1%) per Table 5.",
))
rows.append(make(
    age_min=15, age_max=18, age_category="adolescent",
    sex="female", subgroup_label="u18_women_championship",
    athlete_exposures=int(84.9 * 1000),
    sample_size=26, injury_count=2,
    injury_type_raw="all-cause match injury (>1 day loss) — U-18 Women's Championship",
    injury_category="orofacial_with_dental",
    rate_raw=23.6,
    rate_denominator_raw="per 1000 player-match-hours (Sevens — U18 Women's Championship)",
    rate_per_1000_ae="",  # C11: player-match-hours is not an athlete-exposure denominator (decisions 2026-06-13)
    extraction_notes="Table 2. U18 Women's Championship. 2 injuries / 84.9 PMH. Head/face = 1/2 (50.0%) per Table 5.",
))
rows.append(make(
    age_min=15, age_max=18, age_category="adolescent",
    sex="female", subgroup_label="u18_women_trophy",
    athlete_exposures=int(65.6 * 1000),
    sample_size=21, injury_count=1,
    injury_type_raw="all-cause match injury (>1 day loss) — U-18 Women's Trophy",
    injury_category="orofacial_with_dental",
    rate_raw=15.2,
    rate_denominator_raw="per 1000 player-match-hours (Sevens — U18 Women's Trophy)",
    rate_per_1000_ae="",  # C11: player-match-hours is not an athlete-exposure denominator (decisions 2026-06-13)
    extraction_notes="Table 2. U18 Women's Trophy. 1 injury / 65.6 PMH. That 1 injury was head/face (100%) per Table 5.",
))

# ---- U-18 head/face-only subset rows (the dental-adjacent fraction) ----
for label, n_total, head_face_n, head_face_pct, pmh, sex in (
    ("u18_men_championship_headface",   7, 3, 42.8, 111.1, "male"),
    ("u18_men_trophy_headface",         9, 1, 11.1, 127.4, "male"),
    ("u18_women_championship_headface", 2, 1, 50.0,  84.9, "female"),
    ("u18_women_trophy_headface",       1, 1, 100.0, 65.6, "female"),
):
    head_face_rate = head_face_n / pmh * 1000
    rows.append(make(
        age_min=15, age_max=18, age_category="adolescent",
        sex=sex, subgroup_label=label,
        athlete_exposures=int(pmh * 1000),
        sample_size="", injury_count=head_face_n,
        injury_type_raw=f"head/face match injuries (subset, {head_face_pct}% of all match injuries)",
        injury_category="orofacial_with_dental",
        rate_raw=round(head_face_rate, 2),
        rate_denominator_raw="per 1000 player-match-hours (head/face subset)",
        rate_per_1000_ae="",  # C11: player-match-hours is not an athlete-exposure denominator (decisions 2026-06-13)
        extraction_notes=(
            f"Head/face subset: {head_face_n}/{n_total} injuries ({head_face_pct}%). "
            f"Calculated rate {head_face_rate:.2f}/1000 PMH. Rugby Europe reports head/face as "
            "a composite body region — exact dental-only fraction not reported. Use as upper bound."
        ),
    ))

with (OUT / "rugby_europe_iss_2024.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLUMNS); w.writeheader()
    for r in rows: w.writerow({c: r.get(c, "") for c in COLUMNS})
print(f"wrote rugby_europe_iss_2024.csv ({len(rows)} rows)")
