#!/usr/bin/env python3
"""Batch 2 — 11 more abstract-only extractions. Same template as batch 1.

Skipped: 39417350 (Stress Distribution FEA study — lab simulation, no real
injury counts; would yield an empty epi row).
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
EXTRACTOR = "VB-AI-assisted-2026-05-24"
EXTRACTION_DATE = "2026-05-24"


def make(source_id, **kw):
    base = {c: "" for c in COLUMNS}
    base.update(source_id=source_id, peer_reviewed="TRUE",
        extraction_basis="youth_primary", exposure_context="all",
        injury_category="unspecified_dental", mouthguard_required="unspecified",
        mouthguard_injury_relation="not_addressed",
        extraction_date=EXTRACTION_DATE, extractor=EXTRACTOR,
        quality_flag="partial_data")
    base.update(kw)
    return base


def write_csv(sid, rows):
    p = OUT / f"{sid}.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLUMNS})
    print(f"wrote {p.name} ({len(rows)} rows)")


# 40771058 — youth basketball Turkey
ce_cite = "Cetin SE, et al. (2026). Youth Basketball Players' Awareness and Experiences of Sports-Related Traumatic Dental Injuries and Mouthguards in Turkey: A Cross-Sectional Study."
write_csv("cetin2026", [make("cetin2026",
    citation=ce_cite, pub_year=2026, study_type="cross_sectional",
    country="TR", region="", population_setting="club",
    age_min=8, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="club",
    sport_raw="youth basketball (Turkey, 25 randomly-selected teams)",
    sport="basketball", sport_category="limited_contact",
    sample_size=125, season_or_timeframe="2024-2025 season",
    injury_count=int(round(125 * 0.168)),
    injury_type_raw="self-reported dental injury (tooth fracture predominant 57.1%)",
    injury_category="crown_fracture",
    rate_raw=16.8, rate_denominator_raw="(%) of 125 youth basketball players",
    mouthguard_use_rate=0.072, mouthguard_injury_relation="mentioned_only",
    extraction_notes="125 youth basketball players, 25 teams, 2024-25 season. TDI prevalence 16.8%; tooth fractures most common type. Only 29.6% knew timely replantation helps. MG use 7.2%; primary reason for non-use = perception of being unnecessary (41.1%).",
)])


# 37818921 — NEISS basketball mechanism study
wi_cite = "Williams T, et al. (2024). Mechanisms of dental injuries in basketball, United States, 2003-2022. Dental Traumatology."
write_csv("williams2024", [make("williams2024",
    citation=wi_cite, pub_year=2024, study_type="surveillance",
    country="US", region="", population_setting="mixed",
    age_min=0, age_max=99, age_category="mixed",  # NEISS analysis, full age range
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="basketball (NEISS, all ages)",
    sport="basketball", sport_category="limited_contact",
    sample_size=4419,
    injury_count=int(round(4419 * 0.147)),
    injury_type_raw="oral injuries (dental subset 14.7%)",
    rate_raw=14.7, rate_denominator_raw="(%) of 4419 basketball oral-injury cases that were dental",
    season_or_timeframe="2003-2022 (20 years)",
    extraction_notes="NEISS 2003-2022 basketball oral injuries. n=4,419 raw cases, national estimate 138,980. 14.7% were dental injuries. Collisions with objects (OR=4.39), falls (OR=3.35), basketball contact (OR=1.77) all significantly higher dental-injury odds than player-contact baseline. Full age range — youth subset extractable from full text.",
)])


# 37743045 — NEISS soccer craniomaxillofacial 2003-2022
wi23_cite = "Williams T, et al. (2023). Trends in Soccer-Related Craniomaxillofacial Injuries, United States 2003-2022. Journal of Oral & Maxillofacial Surgery."
write_csv("williams2023", [make("williams2023",
    citation=wi23_cite, pub_year=2023, study_type="surveillance",
    country="US", region="", population_setting="mixed",
    age_min=0, age_max=99, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="soccer (NEISS craniomaxillofacial)",
    sport="football_association", sport_category="limited_contact",
    sample_size=26642,
    injury_count=26642,
    injury_type_raw="craniomaxillofacial injury (any region; includes mouth)",
    injury_category="orofacial_with_dental",
    rate_raw=799393,
    rate_denominator_raw="weighted national estimate over 20 years",
    season_or_timeframe="2003-2022 (20 years)",
    extraction_notes="NEISS 2003-2022 soccer craniomaxillofacial. 26,642 raw cases, national estimate 799,393. Ages 30+ had higher hospitalization OR vs 10-19 reference. Males OR=1.53 vs females. Head OR=8.42, Neck OR=15.8 vs reference. Incidence increased 2003-2012, decreased 2016-2020.",
)])


# 36929194 — Japan HICBT
nasu_cite = "Nasu A, et al. (2023). Head injuries caused by contact with teeth during sports and exercise activities in Japanese schools during the period 2012-2018. Dental Traumatology."
nasu_common = dict(citation=nasu_cite, pub_year=2023, study_type="surveillance",
    country="JP", region="", population_setting="school",
    sex="mixed", level_of_play="school_jv",
    season_or_timeframe="2012-2018 (7 years)",
)
write_csv("nasu2023", [
    make("nasu2023", **nasu_common,
        age_min=4, age_max=18, age_category="mixed",
        sport_raw="all school sports (HICBT aggregate)",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label="all_school_sports",
        sample_size=463527,
        injury_count=3650,
        injury_type_raw="head injuries caused by contact with teeth (HICBT), sport-related subset",
        injury_category="orofacial_with_dental",
        rate_raw=0.79, rate_denominator_raw="(%) of 463,527 school head injuries = HICBT sport-related (3650)",
        extraction_notes="Japan Sport Council 2012-2018 school head injuries. 4495 HICBT total (1% of head injuries), 3650 (81.2%) sport-related. Basketball 57.07% (JHS) / 50.43% (HS) of HICBT; soccer/futsal 13.38% / 24.01%; tag games 22.73% (kindergarten) / 39.03% (elementary).",
    ),
    make("nasu2023", **nasu_common,
        age_min=12, age_max=15, age_category="adolescent",
        sport_raw="basketball — junior high school (HICBT)",
        sport="basketball", sport_category="limited_contact",
        subgroup_label="basketball_junior_high",
        sample_size="",
        rate_raw=57.07, rate_denominator_raw="(%) of HICBT in JHS attributed to basketball",
        extraction_notes="Basketball was the #1 cause of HICBT in Japanese junior high schools (57.07%).",
    ),
    make("nasu2023", **nasu_common,
        age_min=15, age_max=18, age_category="adolescent",
        sport_raw="basketball — high school (HICBT)",
        sport="basketball", sport_category="limited_contact",
        subgroup_label="basketball_high_school",
        sample_size="",
        rate_raw=50.43, rate_denominator_raw="(%) of HICBT in HS attributed to basketball",
        extraction_notes="Basketball was the #1 cause of HICBT in Japanese high schools (50.43%).",
    ),
])


# 34643329 — Gaelic football children
mo_cite = "Mooney J, et al. (2021). Cross-sectional cohort study on the use of mouthguards by children playing Gaelic football in Ireland. Dental Traumatology."
write_csv("mooney2021", [make("mooney2021",
    citation=mo_cite, pub_year=2021, study_type="cross_sectional",
    country="IE", region="", population_setting="club",
    age_min=9, age_max=16, age_category="mixed",
    sex="mixed", level_of_play="club",
    sport_raw="Gaelic football (children, men's variant inferred)",
    sport="gaelic_football_mens", sport_category="contact",
    subgroup_label="",
    sample_size=121, injury_count="",
    injury_type_raw="(MG compliance study — no dental injury counts)",
    mouthguard_use_rate=0.992,
    mouthguard_injury_relation="mentioned_only",
    extraction_notes="121 children + 118 parents. MG use during competition 99.2%, during training 80.8%. As age increased, training compliance decreased (OR=0.18, p<.001). Only 3.8% had custom MG; 73.7% of parents believed custom would be best. Children played median 2 contact sports.",
    season_or_timeframe="cross-sectional",
)])


# 33746633 — Lebanon
na_cite = "Naasan H, et al. (2021). Prevalence and Etiological Factors of Dental Trauma among 12- and 15-Year-Old Schoolchildren of Lebanon: A National Study."
na_common = dict(citation=na_cite, pub_year=2021, study_type="cross_sectional",
    country="LB", region="", population_setting="school",
    sport_raw="all causes (national TDI study — sport one of several etiologies)",
    sport="all_activities_aggregate", sport_category="",
    season_or_timeframe="national cross-sectional",
    level_of_play="recreational", sex="mixed",
)
write_csv("naasan2021", [
    make("naasan2021", **na_common,
        age_min=12, age_max=15, age_category="mixed",
        subgroup_label="overall",
        sample_size=7902,
        injury_count=int(round(7902 * 0.109)),
        injury_type_raw="dental trauma to anterior teeth (enamel fracture 68.3%)",
        injury_category="enamel_fracture",
        rate_raw=10.9, rate_denominator_raw="(%) of 7902 schoolchildren with TDI",
        extraction_notes="National stratified study Lebanon. 3806M / 4096F. Maxillary central incisors 83.7%. Causes: falls 52.5% leading. Risk factors: overjet (OR=2.32), deficient lip coverage (OR=5.73), gender (OR=5.36).",
    ),
    make("naasan2021", **na_common,
        age_min=12, age_max=12, age_category="youth",
        subgroup_label="age_12",
        sample_size=3985, injury_count="",
        rate_raw="", rate_denominator_raw="age-12 subset of national sample (n=3985, prevalence not stratified in abstract)",
        extraction_notes="Age-12 subset; per-age prevalence not in abstract.",
    ),
    make("naasan2021", **na_common,
        age_min=15, age_max=15, age_category="adolescent",
        subgroup_label="age_15",
        sample_size=3917, injury_count="",
        rate_raw="", rate_denominator_raw="age-15 subset of national sample (n=3917, prevalence not stratified in abstract)",
        extraction_notes="Age-15 subset.",
    ),
])


# 33292522 — Hamadan Iran random forest
az_cite = "Azizi A, et al. (2020). Random forest algorithm to identify factors associated with sports-related dental injuries in 6 to 13-year-old athlete children in Hamadan, Iran-2018."
write_csv("azimi2020", [make("azimi2020",
    citation=az_cite, pub_year=2020, study_type="cross_sectional",
    country="IR", region="Hamadan", population_setting="club",
    age_min=6, age_max=13, age_category="youth",
    sex="mixed", level_of_play="club",
    sport_raw="multiple (athlete children, mixed sports)",
    sport="all_sports_aggregate", sport_category="",
    sample_size=356,
    injury_count=55,
    injury_type_raw="self-reported sports-related dental injury",
    rate_raw=15.4, rate_denominator_raw="(%) of 356 athlete children 6-13",
    mouthguard_injury_relation="analyzed",
    extraction_notes="356 athlete children 6-13. Sports-related dental injury 15.4% (55). Higher in boys (p=0.008), and in children of mothers with lower education (p=0.045). MG awareness/use significantly reduces injury (p<0.001). RF model 89.3% accuracy.",
    season_or_timeframe="2018",
)])


# 31765062 — Catalonia field hockey
ca_cite = "Calderon-Diaz J, et al. (2020). Experience with mouthguards and prevalence of orofacial injuries among field hockey players in Catalonia."
write_csv("calderon2020", [make("calderon2020",
    citation=ca_cite, pub_year=2020, study_type="cross_sectional",
    country="ES", region="Catalonia", population_setting="club",
    age_min=10, age_max=99, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="mixed",
    sport_raw="field hockey",
    sport="hockey_field", sport_category="limited_contact",
    sample_size=325, injury_count=int(round(325 * 0.502)),
    injury_type_raw="orofacial injury lifetime (mean dental injuries per player = 0.18)",
    injury_category="orofacial_with_dental",
    rate_raw=50.2, rate_denominator_raw="(%) of 325 field hockey players with at least one orofacial injury",
    mouthguard_use_rate=0.957,
    mouthguard_injury_relation="mentioned_only",
    extraction_notes="325 Catalonia field hockey players (28% female). All age categories. Mean lifetime per player: oral lacerations 1.59, TMD pain 0.24, dental injuries 0.18. MG tried 95.7%; habitually used in training 86.8%, competition 91.3%. Custom-made rated most comfortable (p<.05).",
    season_or_timeframe="lifetime recall",
)])


# 29526055 — 4 contact sports
za_cite = "Zaror et al. (2018). Knowledge and attitudes about sports-related dental injuries and mouthguard use in young athletes in four different contact sports."
za_common = dict(citation=za_cite, pub_year=2018, study_type="cross_sectional",
    country="", region="", population_setting="club",
    age_min=10, age_max=20, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    season_or_timeframe="cross-sectional",
)
write_csv("zaror2018", [
    make("zaror2018", **za_common,
        sport_raw="all 4 contact sports (aggregate)",
        sport="all_sports_aggregate", sport_category="contact",
        subgroup_label="all_4_sports",
        sample_size=229,
        injury_count=31, injury_type_raw="dental injuries (subset of 58 orofacial)",
        rate_raw=13.5, rate_denominator_raw="(%) of 229 young athletes with dental injury",
        mouthguard_use_rate=0.41, mouthguard_injury_relation="analyzed",
        extraction_notes="229 young athletes (mean age 12.9 ± 3.2). Orofacial injury 25.3% (58); dental 13.5% (31). MG use 41% overall (taekwondo 73.7%, karate 70.7%, handball 14.5%, water polo 5.1%).",
    ),
    make("zaror2018", **za_common, sport_raw="water polo", sport="water_polo", sport_category="contact",
        subgroup_label="", sample_size=59,
        injury_count=int(round(59 * 0.186)),
        rate_raw=18.6, rate_denominator_raw="(%) of 59 water polo athletes with dental injury",
        mouthguard_use_rate=0.051, extraction_notes="Water polo subset: dental injury 18.6%, MG 5.1%.",
    ),
    make("zaror2018", **za_common, sport_raw="karate", sport="martial_arts_other", sport_category="contact",
        subgroup_label="karate", sample_size=58,
        injury_count=int(round(58 * 0.172)),
        rate_raw=17.2, rate_denominator_raw="(%) of 58 karate athletes with dental injury",
        mouthguard_use_rate=0.707, extraction_notes="Karate subset: dental 17.2%, MG 70.7%.",
    ),
    make("zaror2018", **za_common, sport_raw="taekwondo", sport="martial_arts_other", sport_category="contact",
        subgroup_label="taekwondo", sample_size=57,
        injury_count=int(round(57 * 0.035)),
        rate_raw=3.5, rate_denominator_raw="(%) of 57 taekwondo athletes with dental injury",
        mouthguard_use_rate=0.737, extraction_notes="Taekwondo subset: dental 3.5% (lowest), MG 73.7% (highest).",
    ),
    make("zaror2018", **za_common, sport_raw="handball", sport="handball", sport_category="contact",
        subgroup_label="", sample_size=55,
        injury_count=int(round(55 * 0.218)),
        rate_raw=21.8, rate_denominator_raw="(%) of 55 handball athletes with dental injury",
        mouthguard_use_rate=0.145, extraction_notes="Handball subset: dental 21.8% (highest), MG 14.5%.",
    ),
])


# 26093006 — NCAA women's field hockey
yard_cite = "Yard EE, Comstock RD. (2015). Head, Face, and Eye Injuries in Collegiate Women's Field Hockey."
yard_common = dict(citation=yard_cite, pub_year=2015, study_type="surveillance",
    country="US", region="", population_setting="club",
    age_min=18, age_max=22, age_category="collegiate",
    sex="female", level_of_play="elite",
    sport_raw="NCAA women's field hockey",
    sport="hockey_field", sport_category="limited_contact",
    season_or_timeframe="2004-05 through 2008-09 seasons",
)
write_csv("yard2015", [
    make("yard2015", **yard_common,
        subgroup_label="head_face_eye_aggregate",
        sample_size=150, injury_count=150,
        injury_type_raw="head/face/eye traumatic injury (composite)",
        rate_raw=0.94, rate_denominator_raw="per 1000 AE (head/face/eye combined)",
        rate_per_1000_ae=0.94,
        extraction_notes="NCAA ISS 2004-05 through 2008-09 seasons. 150 traumatic head/face/eye injuries; weighted occurrence 1587.3. Contact with apparatus caused 72.9% (elevated ball 47.9%).",
    ),
    make("yard2015", **yard_common,
        subgroup_label="dental_subset",
        sample_size="", injury_count="",
        injury_type_raw="traumatic dental injury (subset of head/face/eye)",
        injury_category="unspecified_dental",
        rate_raw=0.06, rate_denominator_raw="per 1000 AE (dental specifically)",
        rate_per_1000_ae=0.06,
        extraction_notes="Dental subset: 0.06/1000 AE (95% CI 0.04-0.14) — much smaller than overall 0.94. Eye 0.07, nose 0.10.",
    ),
])


# 25500920 — central India 12-22
de_cite = "Deshpande et al. (2014). Dental trauma and mouthguard awareness and use among contact and noncontact athletes in central India."
de_common = dict(citation=de_cite, pub_year=2014, study_type="cross_sectional",
    country="IN", region="Central India", population_setting="club",
    age_min=12, age_max=22, age_category="mixed",
    sex="mixed", level_of_play="elite",
    season_or_timeframe="cross-sectional",
    mouthguard_injury_relation="analyzed",
)
write_csv("deshpande2014", [
    make("deshpande2014", **de_common,
        sport_raw="contact sports (subset)",
        sport="all_sports_aggregate", sport_category="contact",
        subgroup_label="contact",
        sample_size=167,  # 15/9% → ~167 to yield 15
        injury_count=15,
        rate_raw=9.0, rate_denominator_raw="(%) of contact athletes with dental injury",
        extraction_notes="Contact sports n~167 (15 dental injuries / 0.09). Dental injuries significantly more in contact (9%) vs noncontact (2.5%).",
    ),
    make("deshpande2014", **de_common,
        sport_raw="noncontact sports (subset)",
        sport="all_sports_aggregate", sport_category="non_contact",
        subgroup_label="noncontact",
        sample_size=160, injury_count=4,
        rate_raw=2.5, rate_denominator_raw="(%) of noncontact athletes with dental injury",
        extraction_notes="Noncontact n~160 (4/0.025). Lower dental injury rate than contact.",
    ),
])

print("\nDone — batch 2 complete.")
