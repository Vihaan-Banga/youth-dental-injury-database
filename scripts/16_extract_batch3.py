#!/usr/bin/env python3
"""Batch 3 — 12 more abstract-only extractions.

Generated overnight 2026-05-24. All quality_flag = 'partial_data'.
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


def make(sid, **kw):
    base = {c: "" for c in COLUMNS}
    base.update(source_id=sid, peer_reviewed="TRUE",
        extraction_basis="youth_primary", exposure_context="all",
        injury_category="unspecified_dental", mouthguard_required="unspecified",
        mouthguard_injury_relation="not_addressed",
        extraction_date=EXTRACTION_DATE, extractor=EXTRACTOR,
        quality_flag="partial_data")
    base.update(kw)
    return base


def w(sid, rows):
    p = OUT / f"{sid}.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=COLUMNS); wr.writeheader()
        for r in rows: wr.writerow({c: r.get(c, "") for c in COLUMNS})
    print(f"wrote {p.name} ({len(rows)} rows)")


# 23532813 — Istanbul handball
w("ozbay2013", [make("ozbay2013",
    citation="Ozbay G, Bakkal M, Abbasoglu Z, Demirel S, Kargul B, Welbury R. (2013). Incidence and prevention of traumatic injuries in paediatric handball players in Istanbul, Turkey. European archives of paediatric dentistry : official journal of the European Academy of Paediatric Dentistry.",
    pub_year=2013, study_type="cross_sectional", country="TR", region="Istanbul",
    population_setting="club", age_min=10, age_max=14, age_category="youth",
    sex="mixed", level_of_play="club",
    sport_raw="paediatric handball (Istanbul amateur national league)",
    sport="all_sports_aggregate", sport_category="contact",
    subgroup_label="paediatric_handball",
    sample_size=212, injury_count=41,
    injury_type_raw="self-reported dental injury (concussion most frequent)",
    rate_raw=19.3, rate_denominator_raw="(%) of 212 paediatric handball players",
    mouthguard_use_rate=0.0, mouthguard_injury_relation="mentioned_only",
    extraction_notes="212 players (74 girls, 138 boys), 14 teams. Mean age 12 ± 1.6. Cause = blow from another player. MG awareness 15.6%, MG use 0%.",
    season_or_timeframe="cross-sectional",
)])

# 23045787 — Ireland west 9-13yo
w("omalley2012", [make("omalley2012",
    citation="O'Malley M, Evans DS, Hewson A, Owens J. (2012). Mouthguard use and dental injury in sport: a questionnaire study of national school children in the west of Ireland. Journal of the Irish Dental Association.",
    pub_year=2012, study_type="cross_sectional", country="IE", region="HSE West",
    population_setting="school", age_min=9, age_max=13, age_category="youth",
    sex="mixed", level_of_play="recreational",
    sport_raw="multiple school + club sports",
    sport="all_sports_aggregate", sport_category="",
    sample_size=505,  # returned questionnaires
    injury_count=int(round(505 * 0.10 * 0.51)),  # 10% had accident, 51% of those dental ≈ 26
    injury_type_raw="dental injury during sport (previous year)",
    rate_raw=5.1, rate_denominator_raw="(%) of 505 children with sport-related dental injury (10% had accident × 51% dental)",
    mouthguard_use_rate=0.22, mouthguard_injury_relation="analyzed",
    extraction_notes="1111 questionnaires sent to parents, 505 returned (46%). 25 randomly-selected schools. >90% involved in sport. MG used 22%. Schools/clubs with MG policy had higher MG use. 10% had sport accident previous year; 51% involved teeth; 72% saw dentist within 2 hours.",
    season_or_timeframe="annual recall",
)])

# 21063551 — combat sports (18-25 mixed scope)
w("shirani2010", [make("shirani2010",
    citation="Shirani G, Kalantar Motamedi MH, Ashuri A, Eshkevari PS. (2010). Prevalence and patterns of combat sport related maxillofacial injuries. Journal of emergencies, trauma, and shock.",
    pub_year=2010, study_type="case_series", country="", region="",
    population_setting="club", age_min=18, age_max=25, age_category="mixed",
    extraction_basis="youth_primary",  # source qualifies because 18-22 subset is in scope
    sex="male", level_of_play="elite",
    sport_raw="combat sports (boxing, taekwondo, kickboxing, Muay Thai)",
    sport="all_sports_aggregate", sport_category="contact",
    subgroup_label="combat_sports_all",
    sample_size=120, injury_count=53,
    injury_type_raw="dental injury (displacement/luxation/fracture/avulsion) among facial trauma cases",
    rate_raw=44.2, rate_denominator_raw="(%) of 120 combat sport athletes with dental injury",
    extraction_notes="120 male combat athletes 18-25 (avg 20). 95 (79.2%) had facial injuries requiring treatment. Lacerations 83 (69.2%), bone fractures 55 (45.1%), dental 53 (44.2%), mandibular dislocation 8 (6.7%). Tooth fractures = 59.7% of dental injuries. Kickboxing most injurious. Nose most-fractured bone (84.7%).",
    season_or_timeframe="case series",
)])

# 19290905 — South Africa 11-13
w("naidoo2009", [make("naidoo2009",
    citation="Naidoo S, Sheiham A, Tsakos G. (2009). Traumatic dental injuries of permanent incisors in 11- to 13-year-old South African schoolchildren. Dental traumatology : official publication of International Association for Dental Traumatology.",
    pub_year=2009, study_type="cross_sectional", country="ZA", region="",
    population_setting="school", age_min=11, age_max=13, age_category="youth",
    sex="mixed", level_of_play="recreational",
    sport_raw="all causes (sport is 2nd most common after falls)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=1665, injury_count=106,
    injury_type_raw="TDI to anterior permanent teeth (enamel fracture 69.1%)",
    injury_category="enamel_fracture",
    rate_raw=6.4, rate_denominator_raw="(%) of 1665 schoolchildren with TDI",
    extraction_notes="Random cluster, 26 primary schools, 1665 of 2610 invited (64% response). 64.4% were 12yo. Boys 2.5× higher OR than girls. Most untreated (85.4%). Falls = main cause; sport = #2; collision with objects = #3.",
    season_or_timeframe="cross-sectional",
)])

# 19030141 — RIO HS 2005-07 RIC
w("huffman2008", [make("huffman2008",
    citation="Huffman EA, Yard EE, Fields SK, Collins CL, Comstock RD. (2008). Epidemiology of rare injuries and conditions among United States high school athletes during the 2005-2006 and 2006-2007 school years. Journal of athletic training.",
    pub_year=2008, study_type="surveillance", country="US", region="",
    population_setting="school", age_min=14, age_max=18, age_category="adolescent",
    sex="mixed", level_of_play="school_varsity",
    sport_raw="9 HS sports (football, soccer m/f, volleyball, basketball m/f, wrestling, baseball, softball) — RIC composite",
    sport="all_sports_aggregate", sport_category="",
    subgroup_label="rare_injuries_composite",
    sample_size="", athlete_exposures=3550141,
    injury_count=321, injury_type_raw="rare injuries+conditions composite (dental is a subset; 62% neck/cervical, 18.7% dehydration/heat)",
    injury_category="orofacial_with_dental",
    rate_raw=9.04, rate_denominator_raw="per 100,000 athlete-exposures (RIC composite)",
    rate_per_1000_ae=0.0904,
    extraction_notes="RIO HS surveillance 2005-06 and 2006-07. 100 schools, 3,550,141 AE. 321 RICs (9.04/100k AE; national estimate 84,223). Football 21.2/100k highest, wrestling 15.2, baseball 7.60. Boys 12.4 vs girls 2.51 (RR=4.93). Dental subset specifically not isolated in abstract.",
    season_or_timeframe="2005/06 and 2006/07 academic years",
)])

# 18821952 — Root fractures
w("molina2008", [make("molina2008",
    citation="Molina JR, Vann WF, McIntyre JD, Trope M, Lee JY. (2008). Root fractures in children and adolescents: diagnostic considerations. Dental traumatology : official publication of International Association for Dental Traumatology.",
    pub_year=2008, study_type="cross_sectional", country="US", region="",
    population_setting="mixed", age_min=6, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    sport_raw="multi-cause permanent anterior tooth trauma (sport one of many)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=114, injury_count=22,
    injury_type_raw="root fractures (RF) in permanent anterior teeth",
    injury_category="root_fracture",
    rate_raw=11.9, rate_denominator_raw="(%) of 185 trauma teeth with RF",
    extraction_notes="8-year cross-sectional, 185 teeth in 114 children ages 6-18. 22 RFs detected. 9.6% of teeth without CF had RF; 13.7% had both. CFs not protective against RFs (OR=1.97, p=0.052). Sport not isolated in abstract.",
    season_or_timeframe="8-year retrospective",
)])

# 18689347 — Lesotho
w("lin2008", [make("lin2008",
    citation="Lin H, Naidoo S. (2008). Causes and prevalence of traumatic injuries to the permanent incisors of school children aged 10-14 years in Maseru, Lesotho. SADJ : journal of the South African Dental Association = tydskrif van die Suid-Afrikaanse Tandheelkundige Vereniging.",
    pub_year=2008, study_type="cross_sectional", country="LS", region="Maseru",
    population_setting="school", age_min=10, age_max=14, age_category="youth",
    sex="mixed", level_of_play="recreational",
    sport_raw="all causes (falls main; sport-related subset)",
    sport="all_activities_aggregate", sport_category="",
    sample_size="", injury_count="",
    injury_type_raw="TDI to permanent incisors (enamel fracture predominant)",
    injury_category="enamel_fracture",
    rate_raw=9.3, rate_denominator_raw="(%) of Maseru schoolchildren 10-14 with TDI",
    extraction_notes="Schoolchildren 10-14, Maseru. Overall TDI 9.3% (boys 13.3% / girls 6.3%). Most common: enamel fracture. Main cause: falls. Sport-specific subset not isolated in abstract.",
    season_or_timeframe="cross-sectional",
)])

# 17670881 — USC intercollegiate
trinidad_common = dict(citation="Cohenca N, Roges RA, Roges R. (2007). The incidence and severity of dental trauma in intercollegiate athletes. Journal of the American Dental Association (1939).",
    pub_year=2007, study_type="cohort", country="US", region="Los Angeles",
    population_setting="club", age_min=18, age_max=22, age_category="collegiate",
    level_of_play="elite", season_or_timeframe="1996-2005 (10 years)",
    mouthguard_injury_relation="analyzed",
)
w("cohenca2007", [
    make("cohenca2007", **trinidad_common,
        sport_raw="all NCAA Division I athletes USC (aggregate)",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label="all_intercollegiate",
        sex="mixed", sample_size="", injury_count=51,
        rate_raw="", rate_denominator_raw="raw count of dental injuries 1996-2005",
        extraction_notes="USC athletic department dental injury surveillance 1996-2005. 51 traumatic dental injuries total. Basketball highest IR; 5× higher than football where MG mandatory.",
    ),
    make("cohenca2007", **trinidad_common,
        sport_raw="men's basketball (NCAA Division I)",
        sport="basketball", sport_category="limited_contact",
        sex="male", sample_size="",
        rate_raw=10.6, rate_denominator_raw="per 100 athlete-seasons (men's basketball)",
        extraction_notes="Men's basketball: 10.6 injuries per 100 athlete-seasons. Highest sport-specific rate. 5× higher than football (MG mandatory there).",
    ),
    make("cohenca2007", **trinidad_common,
        sport_raw="women's basketball (NCAA Division I)",
        sport="basketball", sport_category="limited_contact",
        sex="female", sample_size="",
        rate_raw=5.0, rate_denominator_raw="per 100 athlete-seasons (women's basketball)",
        extraction_notes="Women's basketball: 5.0 injuries per 100 athlete-seasons.",
    ),
])

# 11499758 — Budapest
w("gabris2001", [make("gabris2001",
    citation="Gábris K, Tarján I, Rózsa N. (2001). Dental trauma in children presenting for treatment at the Department of Dentistry for Children and Orthodontics, Budapest, 1985-1999. Dental traumatology : official publication of International Association for Dental Traumatology.",
    pub_year=2001, study_type="case_series", country="HU", region="Budapest",
    population_setting="mixed", age_min=1, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    sport_raw="all etiologies (sport = #2 cause after playing)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=590, injury_count=590,
    injury_type_raw="dental trauma (enamel-dentin crown fracture predominant)",
    injury_category="crown_fracture",
    rate_raw="", rate_denominator_raw="case count over 15 years (1985-1999)",
    extraction_notes="590 children with dental trauma 1985-1999 Budapest. 88% ages 7-14. 810 teeth affected. M:F 58:42. Permanent:primary 90:10. Maxillary central incisors most common. Peak age 10. Etiologies decreasing: playing > sports > falls > cycling > MVA > fighting. 65% at school or home.",
    season_or_timeframe="1985-1999 (15 years)",
)])

# 8883693 — Texas girls' HS basketball
# gomez1996 (PMID 8883693, pub. 1996) removed 2026-06-24 — pre-2000 publication,
# outside PROTOCOL §3.1 time window. See docs/decisions.md (2026-06-24).

# 15592602 — Punahou 15-yr
collins04_common = dict(citation="Beachy G. (2004). Dental Injuries in Intermediate and High School Athletes: A 15-Year Study at Punahou School. Journal of athletic training.",
    pub_year=2004, study_type="cohort", country="US", region="Hawaii",
    population_setting="school", age_min=11, age_max=18, age_category="mixed",
    level_of_play="school_varsity",  # sex defined per row to avoid kwarg conflict
    season_or_timeframe="1988-2003 (15 years)",
)
w("beachy2004", [
    make("beachy2004", **collins04_common,
        sport_raw="all sports — Punahou interscholastic (15-yr aggregate)",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label="all_sports", sample_size=2445, injury_count=56,
        injury_type_raw="dental injury (defined to include jaw, teeth, oral soft tissue requiring referral)",
        rate_raw=0.2, rate_denominator_raw="(%) of 19,492 total injuries that were dental",
        extraction_notes="15-yr longitudinal Punahou School Hawaii. 2445 total students; ~1340 annually in athletics. 123 teams across 19F/18M/2coed sports. 19,492 total injuries → 56 dental (23 tooth, 20 jaw, 13 soft tissue). Rates per 1000 athlete-sessions reported.",
    ),
    make("beachy2004", **collins04_common,
        sport_raw="girls' wrestling",
        sport="wrestling", sport_category="contact",
        sex="female", subgroup_label="",
        rate_raw=0.243, rate_denominator_raw="per 1000 athlete-sessions (95% CI 0-2.3)",
        rate_per_1000_ae=0.243,
        extraction_notes="Highest dental injury rate at Punahou over 15 yrs. Very wide CI.",
    ),
    make("beachy2004", **collins04_common,
        sport_raw="boys' judo",
        sport="martial_arts_other", sport_category="contact",
        sex="male", subgroup_label="",
        rate_raw=0.189, rate_denominator_raw="per 1000 athlete-sessions",
        rate_per_1000_ae=0.189,
        extraction_notes="Boys' judo: 0.189 per 1000 athlete-sessions.",
    ),
    make("beachy2004", **collins04_common,
        sport_raw="boys' soccer",
        sport="football_association", sport_category="limited_contact",
        sex="male", subgroup_label="",
        rate_raw=0.127, rate_denominator_raw="per 1000 athlete-sessions",
        rate_per_1000_ae=0.127,
        extraction_notes="Boys' soccer: 0.127 per 1000 athlete-sessions.",
    ),
    make("beachy2004", **collins04_common,
        sport_raw="football — Punahou",
        sport="football_american", sport_category="contact",
        sex="male", subgroup_label="",
        rate_raw=0.029, rate_denominator_raw="per 1000 athlete-sessions",
        rate_per_1000_ae=0.029,
        extraction_notes="Football: 0.029 per 1000 athlete-sessions. NO tooth injuries (MG mandatory).",
    ),
])

# 16809595 — Brazil adolescents social capital
w("pattussi2006", [make("pattussi2006",
    citation="Pattussi MP, Hardy R, Sheiham A. (2006). Neighborhood social capital and dental injuries in Brazilian adolescents. American journal of public health.",
    pub_year=2006, study_type="cross_sectional", country="BR", region="Distrito Federal",
    population_setting="school", age_min=14, age_max=15, age_category="adolescent",
    sex="mixed", level_of_play="recreational",
    sport_raw="all causes — multilevel social-capital model (sport one of several factors)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=1302, injury_count="",
    injury_type_raw="dental injury (multilevel model; absolute prevalence not in abstract)",
    rate_raw="", rate_denominator_raw="",
    extraction_notes="1302 adolescents 14-15 in 39 schools Distrito Federal Brazil. Multilevel logistic model. Higher neighborhood social capital → lower dental injury (boys, OR=0.55 per 1-unit increase, p=.002). Overall prevalence not isolated in abstract.",
    season_or_timeframe="cross-sectional",
)])

print("\nDone — batch 3 complete.")
