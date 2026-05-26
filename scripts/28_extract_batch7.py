#!/usr/bin/env python3
"""Batch 7 — final round of bulk extractions, clearing the remaining
screened_included PubMed pile (15 sources; 1 FEA-only study skipped)."""

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
EXTRACTOR, EDATE = "VB-AI-assisted-2026-05-25", "2026-05-25"


def make(sid, **kw):
    b = {c: "" for c in COLUMNS}
    b.update(source_id=sid, peer_reviewed="TRUE",
        extraction_basis="youth_primary", exposure_context="all",
        injury_category="unspecified_dental", mouthguard_required="unspecified",
        mouthguard_injury_relation="not_addressed",
        extraction_date=EDATE, extractor=EXTRACTOR, quality_flag="partial_data")
    b.update(kw); return b


def w(sid, rows):
    p = OUT / f"{sid}.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=COLUMNS); wr.writeheader()
        for r in rows: wr.writerow({c: r.get(c, "") for c in COLUMNS})
    print(f"wrote {p.name} ({len(rows)} rows)")


# 15022997 — Norway 7-18
w("skaare2003", [make("skaare2003",
    citation="Skaare AB, Jacobsen I. (2003). Etiological factors related to dental injuries in Norwegians aged 7-18 years.",
    pub_year=2003, study_type="cross_sectional", country="NO", region="Nord-Trøndelag + Oslo",
    population_setting="mixed", age_min=7, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="recreational",
    sport_raw="all causes — sport = 8% of total",
    sport="all_activities_aggregate", sport_category="",
    sample_size=1275, injury_count=int(round(1275 * 0.08)),
    injury_type_raw="sport-related dental trauma (sport subset of 1275 total)",
    rate_raw=8.0, rate_denominator_raw="(%) of 1275 total TDI attributed to sport",
    extraction_notes="1-yr registration by Norwegian public dental service. 1275 children 7-18 with TDI. 48% injured at school. Sport-related = 8%, violence = 8%. 4% severe; only 1/3 of severe were judged preventable.",
    season_or_timeframe="1-year prospective registration",
)])

# 15522054 — UK London cost study
w("lee2004", [make("lee2004",
    citation="Lee JY, Divaris K. (2004). The cost of treating children and adolescents with injuries to their permanent incisors at a dental hospital in the United Kingdom.",
    pub_year=2004, study_type="case_series", country="GB", region="London",
    population_setting="mixed", age_min=5, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    sport_raw="all causes — sport = 22% of injuries",
    sport="all_activities_aggregate", sport_category="",
    sample_size=81, injury_count=int(round(81 * 0.22)),
    injury_type_raw="permanent incisor traumatic injuries (sport-related subset)",
    rate_raw=22.0, rate_denominator_raw="(%) of 81 children with sport-attributed incisor trauma",
    extraction_notes="London teaching hospital dental trauma clinic 1990-2001. 81 patients, 111 traumatized incisors. Mean age 9.9 (SD 2.33), M:F 3:2. Median 8 visits / 21 months. Causes: accidental falls 30%, falls w/ 2nd person 22%, sport 22%, road 17%. Mean cost £856/pt. Outcome: 97% success for uncomplicated, 58% for complicated.",
    season_or_timeframe="1990-2001",
)])

# 21299945 — Cork Ireland
w("lewis2011", [make("lewis2011",
    citation="Lewis B, et al. (2011). Clinical audit of children with permanent tooth injuries treated at a dental hospital in Ireland.",
    pub_year=2011, study_type="case_series", country="IE", region="Cork",
    population_setting="mixed", age_min=5, age_max=15, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    sport_raw="all causes — sport = 23.2% of injuries",
    sport="all_activities_aggregate", sport_category="",
    sample_size=94, injury_count=int(round(168 * 0.232)),
    injury_type_raw="permanent dentition trauma (sport-related subset)",
    rate_raw=23.2, rate_denominator_raw="(%) of 168 injured teeth attributable to sport",
    extraction_notes="Cork University Dental School audit. 94 children (65M, 29F), mean age 10.1 ± 2.64. 168 teeth involved. Causes: sport 23.2%, falls 22.6%, bicycle 15.5%, domestic 6.5%, assault 4.2%, vehicle 3.0%. Injury distribution: 39 uncomplicated crown fx, 18 complicated crown fx, 37 subluxations, 9 root fx, 10 extrusions, 14 lateral luxations, 7 intrusions, 30 avulsions.",
    season_or_timeframe="audit",
)])

# 22051036 — kick-scooter
w("muller_bolla2012", [make("muller_bolla2012",
    citation="Müller-Bolla M, et al. (2012). Dental injuries with kick-scooters in 6- to 12-year-old children.",
    pub_year=2012, study_type="cross_sectional", country="CH", region="near Basel",
    population_setting="school", age_min=6, age_max=12, age_category="youth",
    sex="mixed", level_of_play="recreational",
    sport_raw="kick-scooter riders (children 6-12)",
    sport="skateboarding", sport_category="limited_contact",  # closest in vocab
    subgroup_label="kick_scooter",
    sample_size=953,
    injury_count=int(round(953 * 0.29 * 0.112)),  # 29% had accident, 11.2% dental
    injury_type_raw="dental injury from kick-scooter accident",
    rate_raw=3.2, rate_denominator_raw="(%) of 953 children with kick-scooter dental injury (11.2% of 29% who had an accident)",
    mouthguard_use_rate=0.02,
    extraction_notes="953 children mean age 9.1 (range 6-12), 3 schools near Basel. 29% had a scooter accident; of those: lower extremities 41.4%, upper extremities 37.0%, head 21.6%, dental 11.2%. 20.3% required medical treatment. Helmet 39.6%, other protective gear 2%, NO gear 58.3%. Kick-scooter mapped to nearest taxonomy value 'skateboarding'.",
    season_or_timeframe="cross-sectional",
)])

# 28054391 — children's football
w("nilsson2017", [make("nilsson2017",
    citation="Nilsson D, Faber MT, Steffen K, et al. (2017). Head injuries in children's football-results from two prospective cohort studies in four European countries.",
    pub_year=2017, study_type="cohort", country="", region="4 European countries",
    population_setting="club", age_min=7, age_max=12, age_category="youth",
    sex="mixed", level_of_play="club",
    sport_raw="organized children's football (4-country prospective cohort)",
    sport="football_association", sport_category="limited_contact",
    sample_size="", athlete_exposures=int(688045),  # player-hours total
    injury_count=40,  # 39 head + 1 neck
    injury_type_raw="head/neck injuries (children's football, 5% of 791 total injuries)",
    injury_category="orofacial_with_dental",
    rate_raw=0.25, rate_denominator_raw="per 1000 MATCH hours (head/neck)",
    rate_per_1000_ae="",  # explicitly NOT per AE — per match-hours
    extraction_notes="2 prospective cohorts + RCT, 4 European countries, ages 7-12. 9,933 player-seasons, 688,045 total hours. 791 total injuries; 40 head/neck (5%). Match rate 0.25 (CI 0.15-0.35) per 1000 match-hr; training rate 0.03. Among head: 11 concussions (27.5%), 9 contusions (22.5%), 8 lacerations (20%), 2 nose fractures, 2 DENTAL injuries (2.5%), 8 other. 75% from contact with another player.",
    season_or_timeframe="2 seasons + RCT season",
)])

# 28969286 — India 10-17 self-esteem
w("jain2017", [make("jain2017",
    citation="Jain S, et al. (2017). Traumatic Dental Injuries Prevalence and their Impact on Self-esteem among Adolescents in India.",
    pub_year=2017, study_type="case_series", country="IN",
    population_setting="school", age_min=10, age_max=17, age_category="mixed",
    sex="mixed", level_of_play="recreational",
    sport_raw="all causes (sport listed as primary cause but specific subset not quantified in abstract)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=636,  # 424 controls + 212 cases
    injury_count=212,
    injury_type_raw="anterior TDI (Ellis classification)",
    injury_category="crown_fracture",
    rate_raw=33.3, rate_denominator_raw="(%) of 636 adolescents (cases) — case-control 1:2",
    extraction_notes="Population-based comparative study Nov 2014-Jan 2016. 424 controls + 212 cases (1:2 ratio). Ellis Class I 53.3%, Class II 33.49%, Class III 13.20%. Maxillary arch most affected (72.48%). Self-esteem comparison via RSES showed significant impact of TDI on self-esteem (lower esteem in cases).",
    season_or_timeframe="Nov 2014 - Jan 2016",
)])

# 29406619 — Alberta ice hockey 15-yr
w("nielsen2018", [make("nielsen2018",
    citation="Nielsen TA, et al. (2018). Oral injuries related to Ice Hockey in the province of Alberta, Canada: Trends over the last 15 years.",
    pub_year=2018, study_type="surveillance", country="CA", region="Alberta",
    population_setting="club", age_min=5, age_max=99, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="minor ice hockey (Hockey Alberta sanctioned events, all ages)",
    sport="hockey_ice", sport_category="contact",
    sample_size="", injury_count=int(round(12433 * 0.16)),
    injury_type_raw="oral injuries (16% of all ice hockey injuries)",
    rate_raw=16.0, rate_denominator_raw="(%) of 12,433 ice hockey injuries that were oral",
    extraction_notes="Hockey Alberta 2001-2016 (15 yrs). 12,433 total ice hockey injuries. Oral region = 16% (3rd most common after arms + legs). Annual oral injuries 99-174. Mostly short absence (≤1 wk). Oral mechanism: struck by stick or puck; total-injury mechanism: collisions with boards or other players.",
    season_or_timeframe="2001-2016 (15 years)",
)])

# 31228311 — Norway 16-yo life course
w("schuller2019", [make("schuller2019",
    citation="Schuller AA, et al. (2019). Traumatic dental injuries and experiences along the life course - a study among 16-yr-old pupils in western Norway.",
    pub_year=2019, study_type="cross_sectional", country="NO", region="western Norway",
    population_setting="school", age_min=16, age_max=16, age_category="adolescent",
    sex="mixed", level_of_play="recreational",
    sport_raw="all activities — wrestling associated with severe TDI",
    sport="all_activities_aggregate", sport_category="",
    sample_size=2055,  # of 5184 invited
    injury_count="", injury_type_raw="TDI (any anterior) and severity / multiple episodes",
    rate_raw="", rate_denominator_raw="(%) of 2055 16-yo Norwegian pupils with TDI (not quantified in abstract)",
    extraction_notes="2055 respondents from 5184 invited (39.6% response). Life-course retrospective. More TDI: boys, higher SES, adverse psychosocial+behavioral scores. MODERATE+SEVERE TDI: associated with wrestling specifically. MULTIPLE EPISODES: associated with sports participation generally.",
    season_or_timeframe="cross-sectional 16-yo cohort (born 1997)",
)])

# 31624810 — Lithuania 11-13
narb_common = dict(citation="Narbutaite J, Kazimieras K. (2020). Dental Trauma Experience, Attitudes and Trauma Prevention in 11- to 13-Year-Old Lithuanian Schoolchildren.",
    pub_year=2020, study_type="cross_sectional", country="LT",
    population_setting="school", age_min=11, age_max=13, age_category="youth",
    sex="mixed", level_of_play="recreational",
    season_or_timeframe="cross-sectional",
)
w("narbutaite2020", [
    make("narbutaite2020", **narb_common,
        sport_raw="all causes (sport/leisure = 32% of self-reported)",
        sport="all_activities_aggregate", sport_category="",
        subgroup_label="overall_clinical",
        sample_size=807, injury_count=int(round(807 * 0.52)),
        injury_type_raw="clinically-detected TDI (trauma index)",
        rate_raw=52.0, rate_denominator_raw="(%) of 807 schoolchildren with clinical TDI evidence",
        mouthguard_use_rate=0.03, mouthguard_injury_relation="analyzed",
        extraction_notes="Probability-sampled. 807 6th graders Lithuania (31% consent return). 52% clinical TDI, 13% self-reported, 7% did not remember. Sport/leisure = 32% of self-reported TDI causes; falls/collisions = 63%. 1/3 played contact sport; only 3% always wore MG. ~50% of severe injuries untreated.",
    ),
    make("narbutaite2020", **narb_common,
        sport_raw="contact-sport children subset (~1/3 of cohort)",
        sport="all_sports_aggregate", sport_category="contact",
        subgroup_label="contact_sport_subset",
        sample_size=int(807/3), injury_count="",
        injury_type_raw="contact-sport playing children — MG use 3%",
        mouthguard_use_rate=0.03, mouthguard_injury_relation="analyzed",
        rate_raw="", rate_denominator_raw="(%) of 1/3 contact-sport subset who always wear MG",
        extraction_notes="Contact-sport subset: 1/3 of total (~269). Only 3% always used MG.",
    ),
])

# 36428271 — Japan 5 sports text analysis
w("nasu2023b", [make("nasu2023b",
    citation="Nasu A, et al. (2023). Quantitative text analysis of the mechanisms of tooth injury: Analysis of accidents in five sports that occurred in 15 years under school control.",
    pub_year=2023, study_type="surveillance", country="JP",
    population_setting="school", age_min=12, age_max=18, age_category="adolescent",
    sex="mixed", level_of_play="school_jv",
    sport_raw="5 sports — baseball, basketball, soccer, volleyball, rugby (Japan Sports Council 2005-2020)",
    sport="all_sports_aggregate", sport_category="",
    subgroup_label="multi_sport_aggregate",
    sample_size=7684, injury_count=533,
    injury_type_raw="detailed sport-related dental injury descriptions",
    rate_raw=6.94, rate_denominator_raw="(%) of 7684 school dental injury cases with detailed descriptions (n=533)",
    extraction_notes="Japan Sports Council 2005-2020. 7684 school dental injury cases screened; 533 detailed sport descriptions analyzed. 5 sports by descending freq: baseball, basketball, soccer, volleyball, rugby. Males injured more in all except volleyball. Number of accidents increased in HS. Text-mining co-occurrence networks differ per sport.",
    season_or_timeframe="2005-2020 (15 years)",
)])

# 39297708 — Sydney avulsion
w("madireddy2024", [make("madireddy2024",
    citation="Madireddy R, et al. (2024). Permanent tooth avulsions: A retrospective analysis of the demographics and aetiology of cases at a tertiary hospital in Sydney, Australia.",
    pub_year=2024, study_type="case_series", country="AU", region="Sydney",
    population_setting="mixed", age_min=5, age_max=22, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    sport_raw="non-organized sports = #1 cause (42.7%)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=91, injury_count=int(round(91 * 0.427)),
    injury_type_raw="permanent anterior tooth avulsion",
    injury_category="avulsion",
    rate_raw=42.7, rate_denominator_raw="(%) of 91 avulsion patients attributable to non-organized sport",
    extraction_notes="Tertiary dental hospital Sydney 2001-2021. 91 patients with 117 avulsed permanent anterior teeth. Median age 12 (IQR 9.0-17.0). 68.4% male. Non-organized sport = #1 cause (42.7%). Maxillary central incisors 83.3%. Peak weekend timing.",
    season_or_timeframe="2001-2021 (20 yrs)",
)])

# 39452438 — Italy kickboxing
w("dipalma2024", [make("dipalma2024",
    citation="Di Palma M, et al. (2024). Traumatic Dental Injuries: Prevalence, First Aid, and Mouthguard Use in a Sample of Italian Kickboxing Athletes.",
    pub_year=2024, study_type="cross_sectional", country="IT",
    population_setting="club", age_min=5, age_max=65, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="kickboxing (Italian amateur)",
    sport="kickboxing", sport_category="contact",
    sample_size=142, injury_count=int(round(142 * 0.13)),
    injury_type_raw="TDI during kickboxing (training or fighting)",
    rate_raw=13.0, rate_denominator_raw="(%) of 142 amateur Italian kickboxing athletes with TDI",
    mouthguard_use_rate=0.68, mouthguard_injury_relation="analyzed",
    extraction_notes="142 amateur athletes 5-65 yo, ASD club. 13% had TDI. 94% know MG; 68% use; 74% bought in sports shop. First aid awareness: 61% know replantation possible, 10% know <15 min rule, 37% know keep wet. Wide age range — youth subset extractable from full text.",
    season_or_timeframe="cross-sectional questionnaire",
)])

# 40655786 — 100 cases
w("patel2025", [make("patel2025",
    citation="Patel, et al. (2025). Prevalence and Outcomes of Dental Trauma in Sports-Related Injuries in the Last 2 Years.",
    pub_year=2025, study_type="case_series", country="",
    population_setting="mixed", age_min=6, age_max=99, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="sports-related dental trauma (case series, football+basketball top)",
    sport="all_sports_aggregate", sport_category="",
    sample_size=100, injury_count=100,
    injury_type_raw="sports-related dental trauma cases",
    rate_raw="", rate_denominator_raw="",
    extraction_notes="100 cases over 2 years. 70% male. Highest prevalence 6-10yo (40%). Top sports: football 40%, basketball 30%. Injury types: tooth fractures 50% (#1), avulsions 30%. Treatment outcomes: <30 min = 80% success; 1-24h = 50%; >24h = 20%.",
    season_or_timeframe="2-year retrospective",
)])

# 40917008 — Syria 6-16
w("dashash2026", [make("dashash2026",
    citation="Dashash M, et al. (2026). Epidemiology of Orofacial Trauma in Syrian Pediatric Athletes: A Cross-Sectional Study on Prevalence and Injury Patterns.",
    pub_year=2026, study_type="cross_sectional", country="SY", region="Damascus",
    population_setting="club", age_min=6, age_max=16, age_category="mixed",
    sex="mixed", level_of_play="club",
    sport_raw="multi-sport pediatric athletes (Damascus clubs)",
    sport="all_sports_aggregate", sport_category="",
    sample_size=582, injury_count=int(round(582 * 0.455)),
    injury_type_raw="orofacial-dental trauma (OT)",
    rate_raw=45.5, rate_denominator_raw="(%) of 582 child athletes 6-16 with OT",
    extraction_notes="2-stage cluster sampling 20% of clubs in Damascus, Dec 2023-Dec 2024. 582 child athletes 6-16. OT prevalence 45.5%. Age 12-16 highest extra-oral soft tissue injuries (39%) then dental (23.5%). Falls = #1 mechanism. 53.2% during training. Sports type significantly affected pattern. Closely related to hamdan2026 (same lab).",
    season_or_timeframe="Dec 2023 - Dec 2024",
)])

# 42052228 — NEISS softball HS vs college
ty_common = dict(citation="Tyler JR, et al. (2026). Epidemiology of Softball Injuries: Comparison of Softball-Related Injuries at US EDs Between High School and Collegiate Athletes. Orthop J Sports Med.",
    pub_year=2026, study_type="surveillance", country="US",
    population_setting="mixed", sex="female",
    sport_raw="female softball (US NEISS 2015-2024)",
    sport="softball", sport_category="limited_contact",
    season_or_timeframe="2015-2024 (10 years)",
)
w("tyler2026", [
    make("tyler2026", **ty_common,
        age_min=14, age_max=23, age_category="mixed",
        extraction_basis="youth_primary",
        level_of_play="mixed",
        subgroup_label="overall_female_14_23",
        sample_size=3385, injury_count=3385,
        injury_type_raw="softball-related injuries (all body sites) — female athletes 14-23",
        injury_category="orofacial_with_dental",
        rate_raw=376295, rate_denominator_raw="weighted national estimate over 10 yrs",
        extraction_notes="NEISS 2015-2024 softball injuries in female athletes 14-23. 3385 raw cases → 376,295 national estimate. Population-based incidence per 100 at-risk participants computed using NFHS + NCAA participation data. IRR comparisons HS vs collegiate reported in paper.",
    ),
    make("tyler2026", **ty_common,
        age_min=14, age_max=18, age_category="adolescent",
        extraction_basis="youth_primary",
        level_of_play="school_varsity",
        subgroup_label="hs_aged",
        sample_size="", injury_count="",
        injury_type_raw="HS-aged (14-18) female softball injuries",
        injury_category="orofacial_with_dental",
        rate_raw="", rate_denominator_raw="component of overall (specific count not in abstract)",
        extraction_notes="HS-aged subset (14-18). Per-subgroup absolute counts require full text.",
    ),
    make("tyler2026", **ty_common,
        age_min=19, age_max=23, age_category="collegiate",
        extraction_basis="youth_primary",
        level_of_play="elite",
        subgroup_label="college_aged",
        sample_size="", injury_count="",
        injury_type_raw="college-aged (19-23) female softball injuries",
        injury_category="orofacial_with_dental",
        rate_raw="", rate_denominator_raw="component of overall (specific count not in abstract)",
        extraction_notes="College-aged subset (19-23). Per-subgroup absolute counts require full text.",
    ),
])

print("\nDone — batch 7 complete. (39417350 FEA study skipped — lab simulation only, no real injury data.)")
