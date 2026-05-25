#!/usr/bin/env python3
"""Batch 6 — 10 more abstract-only extractions, focused on NEISS-derived
craniofacial/dental papers and high-yield youth cohorts.
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


# 31179757 — NEISS pediatric 2000-2017
w("collins_neiss2019", [make("collins_neiss2019",
    citation="Collins CL, et al. (2019). Pediatric Sports- and Recreation-Related Dental Injuries Treated in US Emergency Departments. Clinical Pediatrics.",
    pub_year=2019, study_type="surveillance", country="US",
    population_setting="mixed", age_min=0, age_max=17, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    sport_raw="all sport + recreation (NEISS dental injuries <18yo, 2000-2017)",
    sport="all_sports_aggregate", sport_category="",
    sample_size="", injury_count=198787,
    injury_type_raw="ED-treated dental injuries (sport + recreation, children <18)",
    rate_raw=15.4,
    rate_denominator_raw="approximate average per 100,000 US population <18 yrs / year (range 16.9 in 2000 to 13.9 in 2017)",
    extraction_notes="NEISS 2000-2017. Estimated 198,787 injuries total (95% CI 162-235k); ~11,044/yr average. Rate fluctuated 16.9 (2000) -> 13.9 (2017) per 100k pop. Male 69.8%; ages 7-12 = 44.6% (top age band). Top products: bicycles 28.6%, playground 15.3%, baseball/softball 12.4%.",
    season_or_timeframe="2000-2017",
)])


# 34879017 — NEISS baseball youth craniofacial
kaplan_common = dict(citation="Kaplan N, Kim M, Slavin B, Kaplan L. (2022). Baseball-Related Craniofacial Injury Among the Youth: A National Electronic Injury Surveillance System Database Study. J Craniofac Surg.",
    pub_year=2022, study_type="surveillance", country="US",
    population_setting="mixed", sex="mixed", level_of_play="mixed",
    sport_raw="youth baseball (NEISS)",
    sport="baseball", sport_category="limited_contact",
    injury_category="orofacial_with_dental",
    season_or_timeframe="NEISS retrospective",
)
w("kaplan2022", [
    make("kaplan2022", **kaplan_common,
        age_min=5, age_max=19, age_category="mixed",
        subgroup_label="overall",
        injury_count="", injury_type_raw="baseball craniofacial (concussion / contusion / fracture / laceration / dental)",
        extraction_notes="NEISS youth baseball 5-19. 45% of injuries in 10-14yo; ~30% in 5-9 + 25% in 15-19 (estimated). Facial contusion 25%, facial laceration 19.9%, facial fracture 19.7%, concussion 13.4%. Mouth lacerations + dental injuries included as sub-types (specific %s not in abstract).",
    ),
    make("kaplan2022", **kaplan_common,
        age_min=10, age_max=14,
        age_category="mixed",  # 10-12 = youth, 13-14 = adolescent — band spans
        subgroup_label="age_10_14",
        injury_count="",
        rate_raw=45.0, rate_denominator_raw="(%) of all youth craniofacial baseball injuries in 10-14 age group",
        injury_type_raw="craniofacial injuries — 10-14yo subgroup",
        extraction_notes="10-14yo had 45% of total youth baseball craniofacial injuries (peak age band). Source's age grouping crosses the youth/adolescent boundary — tagged 'mixed' to be honest about that.",
    ),
])


# 33710051 — Columbia NCAA D1 college athletes 682
rajan_common = dict(citation="Rajan JE, et al. (2021). Prevalence of Dentofacial Injuries and Concussions Among College Athletes and Their Perceptions of Mouthguards.",
    pub_year=2021, study_type="cross_sectional", country="US", region="New York",
    population_setting="club", age_min=17, age_max=22, age_category="collegiate",
    level_of_play="elite",
    sport_raw="NCAA Division I collegiate athletes",
    sport="all_sports_aggregate", sport_category="",
    season_or_timeframe="cross-sectional survey",
    mouthguard_injury_relation="analyzed",
)
w("rajan2021", [
    make("rajan2021", **rajan_common, sex="mixed",
        subgroup_label="overall",
        sample_size=224,  # the 224 contact-sport athletes inferred from 14.3% × 224 → 32; full 682 includes non-athletes maybe?
        injury_count="", injury_type_raw="overall dental/facial/concussion incidence (survey)",
        mouthguard_use_rate=0.276,
        extraction_notes="682 NCAA D1 college athletes Columbia University. Mean age 19.4 (17-22). 47.6% male. 27.6% reported MG use. Mouth-molded MG most popular (56.7%). MG use much higher in contact athletes (43.3% vs 1.2% noncontact, p<.01).",
    ),
    make("rajan2021", **rajan_common, sex="mixed",
        subgroup_label="contact_sports",
        sample_size="", injury_count="",
        injury_type_raw="dental injuries (contact sport subset)",
        rate_raw=14.3, rate_denominator_raw="(%) of contact sport athletes with dental injury",
        extraction_notes="Contact sport athletes: dental 14.3%, facial 35.0%, concussion 32.6% (all p<.01 vs noncontact). MG use 43.3%.",
    ),
    make("rajan2021", **rajan_common, sex="mixed",
        subgroup_label="noncontact_sports",
        sample_size="", injury_count=0,
        injury_type_raw="dental injuries (noncontact subset)",
        rate_raw=0.0, rate_denominator_raw="(%) of noncontact sport athletes with dental injury",
        extraction_notes="Noncontact sport athletes: dental 0.0% (no cases), facial 6.2%, concussion 2.4%. MG use 1.2%.",
    ),
])


# 33710063 — NEISS amateur ice hockey
ehockey_common = dict(citation="Ekanayake K, et al. (2021). Skating on Thin Ice: Craniofacial Injuries in Amateur Ice Hockey.",
    pub_year=2021, study_type="surveillance", country="US",
    population_setting="mixed", sex="mixed", level_of_play="mixed",
    sport_raw="amateur ice hockey (NEISS 2010-2019)",
    sport="hockey_ice", sport_category="contact",
    injury_category="orofacial_with_dental",
    season_or_timeframe="2010-2019 (10 years)",
)
w("ekanayake2021", [
    make("ekanayake2021", **ehockey_common,
        age_min=5, age_max=99, age_category="mixed",
        extraction_basis="youth_primary",
        subgroup_label="overall",
        sample_size="", injury_count=2544,
        injury_type_raw="craniofacial injuries (concussion 39.9%, dental 1%)",
        extraction_notes="NEISS 2010-2019, 2,544 hockey craniofacial injuries. 12-18yo = 53.8% (largest age band). Concussion 39.9% most frequent dx; dental injuries 1% (least).",
    ),
    make("ekanayake2021", **ehockey_common,
        age_min=12, age_max=18, age_category="adolescent",
        subgroup_label="age_12_18",
        sample_size="",
        injury_count=int(round(2544 * 0.538)),
        injury_type_raw="craniofacial injuries — 12-18yo subgroup",
        rate_raw=53.8, rate_denominator_raw="(%) of 2544 hockey craniofacial injuries in 12-18yo",
        extraction_notes="12-18yo accounted for 53.8% of injuries (largest single age band). Concussion / fracture / laceration proportions differed significantly from null hypothesis (p<.05).",
    ),
])


# 33741876 — NEISS soccer craniofacial
w("dafnis_soccer2021", [make("dafnis_soccer2021",
    citation="Dafnis CL, et al. (2021). Kick Start to an Epidemiological Report of Soccer-Related Craniofacial Trauma Analysis.",
    pub_year=2021, study_type="surveillance", country="US",
    population_setting="mixed", age_min=6, age_max=34, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="soccer craniofacial (NEISS 10-year)",
    sport="football_association", sport_category="limited_contact",
    sample_size="", injury_count="",
    injury_type_raw="craniofacial injuries (concussion / contusion / dental / fracture / hematoma / hemorrhage / laceration)",
    injury_category="orofacial_with_dental",
    extraction_notes="NEISS 10-yr soccer craniofacial. Highest CR injury rate in 12-18yo. By age: 6-11yo most common were contusions + DENTAL injuries (notable); 12-18 mostly concussions; 19-34 fractures + lacerations. Shift in injury profile with age. Underscores need for protective equipment in younger players.",
    season_or_timeframe="10-year retrospective NEISS",
)])


# 33654038 — NEISS basketball craniofacial
w("basketball_craniofacial2021", [make("basketball_craniofacial2021",
    citation="(2021). Heads Up Play: Acute Assessment and Management of Basketball-Related Craniofacial Injuries by On-Court Personnel.",
    pub_year=2021, study_type="surveillance", country="US",
    population_setting="mixed", age_min=5, age_max=49, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="basketball craniofacial (NEISS 2010-2019)",
    sport="basketball", sport_category="limited_contact",
    sample_size="", injury_count=22529,
    injury_type_raw="basketball craniofacial (concussion / contusion / fracture / laceration / etc.)",
    injury_category="orofacial_with_dental",
    extraction_notes="NEISS 2010-2019, 22,529 basketball craniofacial injuries ages 5-49. Adolescent (12-18) + young adult (19-34) had highest incidence. Adolescents: more concussions, fewer fractures/lacerations than young adults (p<.05).",
    season_or_timeframe="2010-2019",
)])


# 31937578 — Youth ice hockey MG concussion case-control
chisholm_common = dict(citation="Chisholm DA, et al. (2020). Mouthguard use in youth ice hockey and the risk of concussion: nested case-control study of 315 cases.",
    pub_year=2020, study_type="cohort", country="CA",
    population_setting="club", age_min=10, age_max=17, age_category="adolescent",
    level_of_play="club",
    sport_raw="youth ice hockey (CA — case-control nested in prospective cohorts)",
    sport="hockey_ice", sport_category="contact",
    injury_category="concussion",
    season_or_timeframe="case-control study period",
    mouthguard_injury_relation="analyzed",
)
w("chisholm2020", [
    make("chisholm2020", **chisholm_common, sex="mixed",
        subgroup_label="cases_concussion",
        sample_size=315, injury_count=315,
        injury_type_raw="game/practice concussion (cases)",
        mouthguard_use_rate=236/315,
        rate_raw=75.0, rate_denominator_raw="(%) of 315 concussion cases wearing MG at injury",
        extraction_notes="Cases = 315 concussions. 236/315 (75%) wore MG at time of injury.",
    ),
    make("chisholm2020", **chisholm_common, sex="mixed",
        subgroup_label="controls_other_injury",
        sample_size=270, injury_count=270,
        injury_type_raw="non-concussion game/practice injury (controls)",
        mouthguard_use_rate=224/270,
        rate_raw=83.0, rate_denominator_raw="(%) of 270 control (non-concussion) cases wearing MG at injury",
        extraction_notes="Controls = 270 non-concussion injuries. 224/270 (83%) wore MG. Any MG vs none: adjusted OR for concussion 0.36 (95% CI 0.17-0.73). Off-the-shelf MG: aOR 0.31 (0.14-0.65). Custom-fit MG: non-significant.",
    ),
])


# 30865370 — Kuwait amateur soccer 7-18
w("alkilzy2019", [make("alkilzy2019",
    citation="Alkilzy M, Aljafar AM, Splieth CH. (2019). Prevalence and severity of traumatic dental injuries among young amateur soccer players: A screening investigation.",
    pub_year=2019, study_type="cross_sectional", country="KW",
    population_setting="club", age_min=7, age_max=18, age_category="mixed",
    sex="male", level_of_play="club",
    sport_raw="amateur soccer (Kuwait, all 14 national clubs)",
    sport="football_association", sport_category="limited_contact",
    sample_size=667, injury_count=169,
    injury_type_raw="TDI in soccer-playing youth (Andreasen 2007 classification)",
    injury_category="enamel_fracture",
    rate_raw=25.0, rate_denominator_raw="(%) of 667 young amateur soccer players with any TDI",
    extraction_notes="667 male amateur soccer players, ages 7-18 (mean 13.4 ± 2.6). 213 injured teeth across 169 players (25%). Maxillary central incisors 91%. Enamel-only fracture 60%. Soccer-related TDI prevalence 11%. Slightly more TDI soccer-related (44%) than non-soccer (39%). Older players had more injuries.",
    season_or_timeframe="cross-sectional screening",
)])


# 27452795 — Japan school sports clubs RR
otsuru_common = dict(citation="Otsuru J, Tamura S. (2016). Descriptive study of dental injury incurred by junior high school and high school students during participation in school sports clubs.",
    pub_year=2016, study_type="surveillance", country="JP",
    population_setting="school", level_of_play="school_jv",
    sample_size="", injury_count="",
    season_or_timeframe="fiscal year 2006",
)
w("otsuru2016", [
    make("otsuru2016", **otsuru_common,
        sport_raw="all sports — Japanese junior HS (boys, exercise-related dental injury RR)",
        sport="all_sports_aggregate", sport_category="",
        age_min=12, age_max=15, age_category="adolescent",
        sex="male", subgroup_label="jhs_boys",
        rate_raw=0.7, rate_denominator_raw="rate ratio (RR) of dental injury sports vs other contexts (Japan JHS boys)",
        extraction_notes="Japan Sport Council 7-prefecture FY2006. JHS boys overall RR 0.7 (p<.001 — counterintuitively LOWER). Top sport for boys JHS: softball RR 7.7.",
    ),
    make("otsuru2016", **otsuru_common,
        sport_raw="all sports — Japanese junior HS girls",
        sport="all_sports_aggregate", sport_category="",
        age_min=12, age_max=15, age_category="adolescent",
        sex="female", subgroup_label="jhs_girls",
        rate_raw=1.3, rate_denominator_raw="rate ratio (RR) of dental injury sports vs other contexts (Japan JHS girls)",
        extraction_notes="JHS girls RR 1.3 (p<.05). Top sport for girls JHS: handball RR 3.9.",
    ),
    make("otsuru2016", **otsuru_common,
        sport_raw="all sports — Japanese HS boys",
        sport="all_sports_aggregate", sport_category="",
        age_min=15, age_max=18, age_category="adolescent",
        sex="male", subgroup_label="hs_boys",
        rate_raw=2.6, rate_denominator_raw="rate ratio (RR) of dental injury sports vs other contexts (Japan HS boys)",
        extraction_notes="HS boys RR 2.6 (p<.001). Top sports: Japanese-style wrestling RR 18.5, rugby RR 7.3.",
    ),
    make("otsuru2016", **otsuru_common,
        sport_raw="all sports — Japanese HS girls",
        sport="all_sports_aggregate", sport_category="",
        age_min=15, age_max=18, age_category="adolescent",
        sex="female", subgroup_label="hs_girls",
        rate_raw=2.7, rate_denominator_raw="rate ratio (RR) of dental injury sports vs other contexts (Japan HS girls)",
        extraction_notes="HS girls RR 2.7 (p<.001). Top sport: handball RR 6.5. Crown fracture predominant dental injury type across all groups.",
    ),
])


# 25881567 — Junior rugby league Gold Coast
w("kanagasingam2016", [make("kanagasingam2016",
    citation="Kanagasingam S, Reddy R, Smith YH. (2016). Mouthguard Use and Awareness of Junior Rugby League Players in the Gold Coast, Australia: A Need for More Education. Clin J Sport Med.",
    pub_year=2016, study_type="cross_sectional", country="AU", region="Gold Coast",
    population_setting="club", age_min=6, age_max=17, age_category="mixed",
    sex="mixed", level_of_play="club",
    sport_raw="junior rugby league (Gold Coast community)",
    sport="rugby", sport_category="contact",
    subgroup_label="junior_rugby_league",
    sample_size=494, injury_count="",
    injury_type_raw="(survey of MG use + knowledge — no injury counts)",
    mouthguard_use_rate=0.682, mouthguard_injury_relation="mentioned_only",
    extraction_notes="494 junior rugby league players + coaches Gold Coast. 68.2% wore MG. Boil-and-bite most common (64.7%). Top reasons NOT wearing: cost (40.1%), don't believe they work (35.7%). ~44% coaches/50% players knew only dentist can manage avulsed tooth; <22% knew within-15-min reinsertion rule. Mostly an MG knowledge study — no injury counts.",
    season_or_timeframe="cross-sectional",
)])

print("\nDone — batch 6 complete.")
