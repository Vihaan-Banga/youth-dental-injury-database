#!/usr/bin/env python3
"""Batch 5 — 12 abstract-only extractions for the new includes from round-2
journal searches (J Endod/J OMFS/Pediatrics/Inj Prev/OJSM)."""

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
EXTRACTOR, EDATE = "VB-AI-assisted-2026-05-24", "2026-05-24"


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


# 11003192 — Indiana youth baseball face guards
w("danis2000", [make("danis2000",
    citation="Danis RP, Hu K, Bell M. (2000). Acceptability of baseball face guards and reduction of oculofacial injury in receptive youth league players. Injury prevention : journal of the International Society for Child and Adolescent Injury Prevention.",
    pub_year=2000, study_type="cohort", country="US", region="Indiana",
    population_setting="club", age_min=5, age_max=15, age_category="mixed",
    sex="mixed", level_of_play="club",
    sport_raw="youth league baseball (Indiana)",
    sport="baseball", sport_category="limited_contact",
    sample_size="",  # 238 teams, players per team not specified
    injury_count="", injury_type_raw="oculofacial injuries (face guard vs control)",
    injury_category="orofacial_with_dental",
    mouthguard_injury_relation="analyzed",
    extraction_notes="238 youth baseball teams Central + Southern Indiana 1997. Non-randomized prospective cohort. ~half got face guard helmets (intervention). Significant reduction in oculofacial injury reported by intervention parents/players/coaches (p=0.04). No adverse performance.",
    season_or_timeframe="1997 season",
)])

# 15178672 — youth soccer parents MG
w("pribble2004", [make("pribble2004",
    citation="Pribble JM, Maio RF, Freed GL. (2004). Parental perceptions regarding mandatory mouthguard use in competitive youth soccer. Injury prevention : journal of the International Society for Child and Adolescent Injury Prevention.",
    pub_year=2004, study_type="cross_sectional", country="US", region="",
    population_setting="club", age_min=8, age_max=14, age_category="mixed",
    sex="mixed", level_of_play="club",
    sport_raw="competitive youth soccer (8-14 yo)",
    sport="football_association", sport_category="limited_contact",
    sample_size=120,
    injury_count=int(round(120 * 0.11)),
    injury_type_raw="self-reported orofacial injury (last 12 mo)",
    rate_raw=11.0, rate_denominator_raw="(%) of 120 youth soccer parents reporting orofacial injury in child",
    mouthguard_use_rate=0.14, mouthguard_injury_relation="analyzed",
    extraction_notes="120 parents of 8-14 yo soccer players (mean 11.8 ± 1.5; 48% female). 14% wore MG; 11% had orofacial injuries. 92% parents thought MG effective; 50% agreed mandatory. Dentist/physician recommendation associated with mandatory support (OR=2.9).",
    season_or_timeframe="fall 2002",
)])

# 16081755 — Australian Football MG RCT
w("finch2005", [make("finch2005",
    citation="Finch C, Braham R, McIntosh A, McCrory P, Wolfe R. (2005). Should football players wear custom fitted mouthguards? Results from a group randomised controlled trial. Injury prevention : journal of the International Society for Child and Adolescent Injury Prevention.",
    pub_year=2005, study_type="cohort", country="AU", region="",
    population_setting="club", age_min=18, age_max=99, age_category="mixed",
    extraction_basis="youth_primary",
    sex="male", level_of_play="club",
    sport_raw="Australian Rules Football (community league)",
    sport="australian_rules_football", sport_category="contact",
    subgroup_label="",
    sample_size=301,
    injury_count="", injury_type_raw="head/orofacial (H/O) injuries — Aus rules football",
    injury_category="orofacial_with_dental",
    rate_raw=2.7, rate_denominator_raw="per 1000 person-hours of playing time (H/O combined)",
    mouthguard_use_rate=1.0, mouthguard_injury_relation="analyzed",
    extraction_notes="23 teams, 301 players, largest Australian community football league, 2001 season. Cluster RCT custom vs control MG. Both arms wore MGs (custom less common in controls). Overall H/O rate 2.7/1000 exposure hours. Game > training rate. Adjusted IRR custom-vs-control = 0.56 (95% CI 0.32-0.97) suggesting benefit.",
    season_or_timeframe="2001 season",
)])

# 18519488 — HS baseball RIO 2005-07
w("collins2008", [make("collins2008",
    citation="Collins CL, Comstock RD. (2008). Epidemiological features of high school baseball injuries in the United States, 2005-2007. Pediatrics.",
    pub_year=2008, study_type="surveillance", country="US", region="",
    population_setting="school", age_min=14, age_max=18, age_category="adolescent",
    sex="male", level_of_play="school_varsity",
    sport_raw="boys' high school baseball (national RIO surveillance)",
    sport="baseball", sport_category="limited_contact",
    sample_size="", athlete_exposures="",  # not specified; rate 1.26/1000 AE
    injury_count=431,
    injury_type_raw="baseball injuries (head/face 12.3%, mouth/teeth subset within batted-ball injuries)",
    injury_category="orofacial_with_dental",
    rate_raw=1.26, rate_denominator_raw="per 1000 athlete-exposures (HS baseball overall)",
    rate_per_1000_ae=1.26,
    extraction_notes="National HS RIO 2005-06 + 2006-07. 100 schools. National est 131,555 baseball injuries. 431 reported injuries → rate 1.26/1000 AE. Head/face 12.3% of body sites injured. Of 50 batted-ball injuries (11.6% of all), head/face 48.0% and mouth/teeth 16.0%. 9.7% medical disqualification season; 9.4% surgery.",
    season_or_timeframe="2005/06 + 2006/07 academic years",
)])

# 22260909 — pediatric facial fractures + dental
w("isokungas2012", [make("isokungas2012",
    citation="Iso-Kungas P, Törnwall J, Suominen AL, Lindqvist C, Thorén H. (2012). Dental injuries in pediatric patients with facial fractures are frequent and severe. Journal of oral and maxillofacial surgery : official journal of the American Association of Oral and Maxillofacial Surgeons.",
    pub_year=2012, study_type="case_series", country="", region="",
    population_setting="mixed", age_min=0, age_max=16, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    sport_raw="multi-cause pediatric facial fracture cohort (sport one of several causes)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=200, injury_count=45,
    injury_type_raw="dental injuries in facial-fracture pts (crown fx 59.9% of DIs, premolars 37.4%)",
    injury_category="crown_fracture",
    rate_raw=22.5, rate_denominator_raw="(%) of 200 pediatric facial fracture pts with dental injury",
    extraction_notes="12-yr study, 200 patients <=16 with facial fracture (59.5% male). Mean age 12.6. 45 (22.5%) had DI. Crown fracture predominant (59.9%); premolars 37.4%. Multiple DIs in 71.1% of those with DI; severe in 66.7%. DI significantly associated with MVC (p=0.02) and mandibular fracture (p=0.03).",
    season_or_timeframe="12 years",
)])

# 24813778 — Nationwide ED facial fractures
w("allareddy2014", [make("allareddy2014",
    citation="Allareddy V, Itty A, Maiorini E, Lee MK, Rampa S, Allareddy V, Nalliah RP. (2014). Emergency department visits with facial fractures among children and adolescents: an analysis of profile and predictors of causes of injuries. Journal of oral and maxillofacial surgery : official journal of the American Association of Oral and Maxillofacial Surgeons.",
    pub_year=2014, study_type="surveillance", country="US", region="",
    population_setting="mixed", age_min=0, age_max=21, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="all causes pediatric facial fracture ED visits (sport one of many)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=336124, injury_count=336124,
    injury_type_raw="facial fracture (nasal + mandible most common)",
    injury_category="orofacial_with_dental",
    rate_raw="", rate_denominator_raw="aggregate ED visit count 2008-2010 (NEDS)",
    extraction_notes="Nationwide Emergency Department Sample 2008-2010, all ED visits with facial fracture aged ≤21. 336,124 visits. Late adolescents 18-21 = 45.6% of visits, middle adolescents 15-17 = 26.6%. 74.7% male. Most common: nasal bones + mandible. Younger: falls/pedal cycle; older: firearm/MVA/assault.",
    season_or_timeframe="2008-2010",
)])

# 32866487 — Pusan 5-yr sports OMF
w("park2021", [make("park2021",
    citation="Park HK, Park JY, Choi NR, Kim UK, Hwang DS. (2021). Sports-Related Oral and Maxillofacial Injuries: A 5-Year Retrospective Study, Pusan National University Dental Hospital. Journal of oral and maxillofacial surgery : official journal of the American Association of Oral and Maxillofacial Surgeons.",
    pub_year=2021, study_type="case_series", country="KR", region="Pusan",
    population_setting="mixed", age_min=5, age_max=99, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="multi-sport — sports-related OMF trauma cohort",
    sport="all_sports_aggregate", sport_category="",
    sample_size=517, injury_count=517,
    injury_type_raw="sports-related oral & maxillofacial injuries",
    injury_category="orofacial_with_dental",
    rate_raw="", rate_denominator_raw="case count 2014-2018",
    extraction_notes="517 patients Pusan National University Dental Hospital ED 2014-2018. Teenagers 27.9% (largest age group), <10yo 23.2% (2nd). Cycling = #1 cause overall (43.5%, NC). Within contact sports: football 47.7%. Within limited-contact: baseball 50.0%. Within noncontact: cycling 74.8%. Mechanisms: contact = other person's body 53.4%; LC = other objects 60.9%; NC = slip down 77.4%.",
    season_or_timeframe="2014-2018 (5 years)",
)])

# 33614796 — NEISS non-tackle football youth
w("zendler2021", [make("zendler2021",
    citation="Zendler JM, Jadischke R, Frantz J, Hall S, Goulet GC. (2021). Emergency Department Visits From 2014 to 2018 for Head Injuries in Youth Non-Tackle Football Compared With Other Sports. Orthopaedic journal of sports medicine.",
    pub_year=2021, study_type="surveillance", country="US", region="",
    population_setting="mixed", age_min=6, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    sport_raw="non-tackle football (flag/touch/7v7) + comparators",
    sport="football_american", sport_category="limited_contact",
    subgroup_label="non_tackle_football",
    sample_size=26770, injury_count=26770,
    injury_type_raw="head-region injuries (head, ear, eyeball, mouth, or face)",
    injury_category="orofacial_with_dental",
    rate_raw="", rate_denominator_raw="NEISS incident reports 2014-2018",
    extraction_notes="NEISS 2014-2018 ages 6-18, basketball+football+soccer head-region injuries. 26,770 reports. Football manually split into tackle vs non-tackle by narrative. Non-tackle: head most-injured body part, then face; most common dx = laceration. Annual rates per 100k participants computed using SFIA participation data.",
    season_or_timeframe="2014-2018",
)])

# 34973164 — NEISS martial arts head/neck
w("stanbouly2022c", [make("stanbouly2022c",
    citation="Stanbouly D, Richardson J, Lee KC, Zeng Q, Perrino MA, Chuang SK. (2022). A Comparison of 2,845 Head and Neck Injuries in Various Martial Arts. Journal of oral and maxillofacial surgery : official journal of the American Association of Oral and Maxillofacial Surgeons.",
    pub_year=2022, study_type="surveillance", country="US", region="",
    population_setting="mixed", age_min=0, age_max=99, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="martial arts (karate, kung fu, kickboxing, taekwondo, judo, jiu jitsu)",
    sport="martial_arts_other", sport_category="contact",
    sample_size=2845, injury_count=2845,
    injury_type_raw="head + neck injuries — NEISS",
    injury_category="orofacial_with_dental",
    rate_raw="", rate_denominator_raw="20-yr NEISS aggregate count",
    extraction_notes="NEISS 20-yr (2000-2019) head+neck martial arts injuries. 2,845 cases. Taekwondo most likely head injury; jiu jitsu/judo most likely neck. Judo highest admission rate.",
    season_or_timeframe="2000-2019 (20 years)",
)])

# 35340727 — NCAA D-I 13 sports maxillofacial
wormald_common = dict(citation="Mertz KC, Bolia IK, English MG, Cho AW, Trasolini N, Hasan LK, Haratian A, Diaz P, Romano R, Gamradt SC, Weber AE. (2022). Epidemiology and Outcomes of Maxillofacial Injuries in NCAA Division I Athletes Participating in 13 Sports. Orthopaedic journal of sports medicine.",
    pub_year=2022, study_type="surveillance", country="US", region="",
    population_setting="club", age_min=18, age_max=22, age_category="collegiate",
    level_of_play="elite",
    season_or_timeframe="2015-16 through 2018-19 (4 seasons)",
)
w("mertz2022", [
    make("mertz2022", **wormald_common, sex="mixed",
        sport_raw="all 13 NCAA D-I sports (aggregate)",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label="all_13_sports",
        sample_size="", athlete_exposures="",
        injury_count=193,
        injury_type_raw="maxillofacial injuries — single-institution registry",
        injury_category="orofacial_with_dental",
        rate_raw=2.06, rate_denominator_raw="per 1000 athlete-exposure HOURS (not per AE)",
        rate_per_1000_ae="",  # intentionally empty — different denominator than per-AE rates
        extraction_notes="Single-institution registry 13 NCAA D-I sports 4 seasons. 193 maxillofacial injuries. Overall 2.06 per 1000 AE-HOURS (not per 1000 AE — different denominator; do not directly compare to RIO/NEISS rates without converting). M 1.92 / F 2.43 per 1000 AE-h.",
    ),
    make("mertz2022", **wormald_common, sex="male",
        sport_raw="men's basketball (NCAA D-I, single institution)",
        sport="basketball", sport_category="limited_contact",
        subgroup_label="",
        rate_raw=8.30, rate_denominator_raw="per 1000 athlete-exposure HOURS (men's BB; not per AE)",
        rate_per_1000_ae="",  # see above
        extraction_notes="Men's basketball — highest rate at 8.30 per 1000 AE-HOURS. NOT per-AE; not directly comparable to collins2016/azadani2023's per-100k-AE rates. ~60 minutes/AE rough conversion gives ~0.14 per 1000 AE which is in the same ballpark as RIO rates.",
    ),
    make("mertz2022", **wormald_common, sex="male",
        sport_raw="men's water polo (NCAA D-I)",
        sport="water_polo", sport_category="contact",
        subgroup_label="",
        rate_raw=8.15, rate_denominator_raw="per 1000 athlete-exposure HOURS (men's water polo; not per AE)",
        rate_per_1000_ae="",
        extraction_notes="Men's water polo — 8.15 per 1000 AE-HOURS. Same denominator caveat as men's basketball row.",
    ),
])

# 8784371 — Little League baseball
w("pasternack1996", [make("pasternack1996",
    citation="Pasternack JS, Veenema KR, Callahan CM. (1996). Baseball injuries: a Little League survey. Pediatrics.",
    pub_year=1996, study_type="cohort", country="US", region="",
    population_setting="club", age_min=7, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="club",
    sport_raw="Little League baseball",
    sport="baseball", sport_category="limited_contact",
    sample_size=2861, athlete_exposures=140932,  # player-hours (close)
    injury_count=81,
    injury_type_raw="baseball injuries (acute + overuse; 18 ball-related facial)",
    injury_category="orofacial_with_dental",
    rate_raw=0.057, rate_denominator_raw="per 100 player-hours (overall)",
    rate_per_1000_ae="",  # C11: per-100-player-hours is not an athlete-exposure denominator (decisions 2026-06-13); rate kept in rate_raw
    extraction_notes="2861 Little League players 7-18, 140,932 player-hours. 81 injuries total (66 acute, 15 overuse). Overall rate 0.057/100 player-hours = 0.57/1000. Severe rate 0.008/100. 62% of acute = hit by ball; 18 ball-related facial injuries (16 on defense).",
    season_or_timeframe="prospective survey",
)])

# 9191640 — Innsbruck mandibular fractures
emshoff_common = dict(citation="Emshoff R, Schöning H, Röthler G, Waldhart E. (1997). Trends in the incidence and cause of sport-related mandibular fractures: a retrospective analysis. Journal of oral and maxillofacial surgery : official journal of the American Association of Oral and Maxillofacial Surgeons.",
    pub_year=1997, study_type="case_series", country="AT", region="Innsbruck",
    population_setting="mixed", age_min=5, age_max=99, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    season_or_timeframe="1984-1993 (10 years)",
)
w("emshoff1997", [
    make("emshoff1997", **emshoff_common,
        sport_raw="all causes mandibular fracture (sport = 31.5%)",
        sport="all_activities_aggregate", sport_category="",
        subgroup_label="overall",
        sample_size=712, injury_count=982,
        injury_type_raw="mandibular fractures (982 total in 712 patients)",
        injury_category="orofacial_with_dental",
        rate_raw="", rate_denominator_raw="case count",
        extraction_notes="712 patients with 982 mandibular fractures, Innsbruck 1984-1993. Causes: sport 31.5% (#1, ↑ from 28.6% to 34.5% over decade), MVA 27.2%, falls 20.8%. M:F 2.5:1.",
    ),
    make("emshoff1997", **emshoff_common,
        sport_raw="skiing (55.3% of sport-related mandibular fractures)",
        sport="skiing", sport_category="non_contact",
        subgroup_label="",
        sample_size="",
        injury_count=int(round(712 * 0.315 * 0.553)),
        injury_type_raw="skiing-related mandibular fractures",
        injury_category="orofacial_with_dental",
        rate_raw=55.3, rate_denominator_raw="(%) of sport-related mandibular fractures from skiing",
        extraction_notes="Skiing was #1 sport for mandibular fractures (55.3% of sport-related). Decreased 19.5% over decade as cycling grew.",
    ),
    make("emshoff1997", **emshoff_common,
        sport_raw="cycling (25.4% of sport-related)",
        sport="cycling", sport_category="non_contact",
        subgroup_label="",
        sample_size="",
        injury_count=int(round(712 * 0.315 * 0.254)),
        injury_type_raw="cycling-related mandibular fractures",
        injury_category="orofacial_with_dental",
        rate_raw=25.4, rate_denominator_raw="(%) of sport-related mandibular fractures from cycling",
        extraction_notes="Cycling 25.4% (↑ 19.3% over decade). Associated injuries rate 133.3/100 mandibular fractures.",
    ),
])

print("\nDone — batch 5 complete.")
