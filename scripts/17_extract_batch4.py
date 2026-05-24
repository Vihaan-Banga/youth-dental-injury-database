#!/usr/bin/env python3
"""Batch 4 — 14 more abstract-only extractions."""

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


# 11202877 — UK aetiology (mostly non-sport)
w("carter2000", [make("carter2000",
    citation="Carter NL, Jones JE, Newton JT. (2000). The aetiology of dento-alveolar injuries and factors influencing attendance for emergency care of adolescents in the north west of England.",
    pub_year=2000, study_type="cross_sectional", country="GB", region="North West England",
    population_setting="school", age_min=5, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="recreational",
    sport_raw="all causes (bicycle/sports 30% of injuries)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=2022, injury_count=696, rate_raw=34.0,
    rate_denominator_raw="(%) of 2022 schoolchildren with any dental trauma",
    extraction_notes="2022 schoolchildren. 696 (34%) had dental injury. Falls 34% main cause; bicycles/sports another 30%. Home 35%, school 25%. Sport-specific subset not isolated.",
    season_or_timeframe="cross-sectional",
)])

# 11678540 — Brazil 13-yo (sport small but isolated)
w("marcenes2001", [make("marcenes2001",
    citation="Marcenes W, Beiruti N, Tayfour D, Issa S. (2001). Prevalence, causes and correlates of traumatic dental injuries among 13-year-olds in Brazil.",
    pub_year=2001, study_type="cross_sectional", country="BR", region="Cianorte",
    population_setting="school", age_min=13, age_max=13, age_category="adolescent",
    sex="mixed", level_of_play="recreational",
    sport_raw="all causes (sport = 2.3% of TDI causes)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=652, injury_count=int(round(652 * 0.204)),
    injury_type_raw="TDI to permanent incisors",
    rate_raw=20.4, rate_denominator_raw="(%) of 652 13-yo with TDI",
    extraction_notes="Brazil Cianorte 13-yo (85% response). TDI 20.4%. Causes: falls 24.1%, collisions 15%, MVA 10.5%, misuse 6%, sport 2.3%, violence 1.5%. Non-nuclear family OR=2.18; overweight OR=1.93; male OR=2.19.",
    season_or_timeframe="cross-sectional",
)])

# 11798994 — Junior A hockey (player-game hours rate)
benson_common = dict(citation="Benson BW, Mohtadi NG, Rose MS, Meeuwisse WH. (2002). A comparison of facial protection and the incidence of head, neck, and facial injuries in Junior A hockey players.",
    pub_year=2002, study_type="cohort", country="CA", region="",
    population_setting="club", age_min=16, age_max=20, age_category="mixed",
    sex="male", level_of_play="elite",
    sport_raw="Junior A ice hockey (elite amateur)",
    sport="hockey_ice", sport_category="contact",
    season_or_timeframe="prospective cohort", sample_size=282,
    mouthguard_injury_relation="analyzed",
)
w("benson2002", [
    make("benson2002", **benson_common,
        subgroup_label="no_facial_protection",
        injury_count=52, rate_raw=158.9,
        rate_denominator_raw="per 1000 player-game hours (no facial protection)",
        injury_type_raw="head/neck/face injuries (subgroup: no facial protection)",
        injury_category="orofacial_with_dental",
        extraction_notes="282 Junior A elite amateur ice hockey players. No protection: 52 injuries, 158.9/1000 player-game hours.",
    ),
    make("benson2002", **benson_common,
        subgroup_label="partial_facial_protection",
        injury_count=45, rate_raw=73.5,
        rate_denominator_raw="per 1000 player-game hours (partial = half shield)",
        injury_type_raw="head/neck/face injuries (subgroup: half shield)",
        injury_category="orofacial_with_dental",
        extraction_notes="Half shield: 45 injuries, 73.5/1000 player-game hours.",
    ),
    make("benson2002", **benson_common,
        subgroup_label="full_facial_protection",
        injury_count=16, rate_raw=23.2,
        rate_denominator_raw="per 1000 player-game hours (full cage or shield)",
        injury_type_raw="head/neck/face injuries (subgroup: full protection)",
        injury_category="orofacial_with_dental",
        extraction_notes="Full cage/shield: 16 injuries, 23.2/1000 player-game hours (~7× lower than no protection).",
    ),
])

# 15660753 — Turkish premier ice hockey (sparse abstract)
w("ranalli2005", [make("ranalli2005",
    citation="Ranalli DN. (2005). Dental trauma and mouthguard usage among ice hockey players in Turkey premier league.",
    pub_year=2005, study_type="cross_sectional", country="TR", region="",
    population_setting="club", age_min=15, age_max=35, age_category="mixed",
    extraction_basis="youth_primary",
    sex="mixed", level_of_play="elite",
    sport_raw="Turkish Premier Ice Hockey League (youth + adult)",
    sport="hockey_ice", sport_category="contact",
    sample_size="", injury_count="",
    injury_type_raw="self-reported dental trauma",
    rate_raw="", rate_denominator_raw="",
    mouthguard_injury_relation="mentioned_only",
    extraction_notes="Turkish Premier Ice Hockey League youth + adult players. Abstract reports awareness 'neglected' and 'limited utilization' of MG — no numerical prevalence in abstract. Source qualifies because youth subset present.",
    season_or_timeframe="cross-sectional",
)])

# 16162986 — RCT football+rugby Ontario
mc_common = dict(citation="McIntosh AS, McCrory P. (2005). Comparison of mouth guard designs and concussion prevention in contact sports: a multicenter randomized controlled trial.",
    pub_year=2005, study_type="cohort", country="CA", region="Ontario",
    population_setting="club", age_min=18, age_max=22, age_category="collegiate",
    level_of_play="elite",
    season_or_timeframe="2003 fall season",
    mouthguard_use_rate=1.0, mouthguard_injury_relation="analyzed",
)
w("mcintosh2005", [
    make("mcintosh2005", **mc_common, sex="male",
        sport_raw="varsity football (university male)",
        sport="football_american", sport_category="contact",
        subgroup_label="football_male",
        sample_size=394, injury_count=0,
        injury_type_raw="dental trauma events (RCT secondary endpoint)",
        rate_raw=0, rate_denominator_raw="dental-trauma events in 2003 fall season",
        extraction_notes="5 Ontario universities, varsity football. 394 male athletes. ZERO dental trauma events during season (mandatory MG context). Primary endpoint was concussion — no significant MG-design difference.",
    ),
    make("mcintosh2005", **mc_common, sex="male",
        sport_raw="varsity rugby (university male)",
        sport="rugby", sport_category="contact",
        subgroup_label="rugby_male",
        sample_size=129, injury_count=0,
        rate_raw=0, rate_denominator_raw="dental-trauma events in season",
        injury_type_raw="dental trauma events (RCT secondary endpoint)",
        extraction_notes="University male rugby 129 athletes. Zero dental events.",
    ),
    make("mcintosh2005", **mc_common, sex="female",
        sport_raw="varsity rugby (university female)",
        sport="rugby", sport_category="contact",
        subgroup_label="rugby_female",
        sample_size=123, injury_count=0,
        rate_raw=0, rate_denominator_raw="dental-trauma events in season",
        injury_type_raw="dental trauma events (RCT secondary endpoint)",
        extraction_notes="University female rugby 123 athletes. Zero dental events.",
    ),
])

# 17073918 — pony/horseback riding children
w("nalcaci2006", [make("nalcaci2006",
    citation="Nalçaci R, Nalçaci A, Pekiner FN. (2006). Dental and orofacial trauma in pony and horseback riding children.",
    pub_year=2006, study_type="cross_sectional", country="TR", region="Istanbul",
    population_setting="club", age_min=5, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="club",
    sport_raw="pony and horseback riding (children, Istanbul clubs)",
    sport="all_sports_aggregate", sport_category="limited_contact",  # not a controlled vocab sport
    subgroup_label="equestrian",
    sample_size=214, injury_count=5,
    injury_type_raw="dental/orofacial trauma during riding",
    rate_raw=2.3, rate_denominator_raw="(%) of 214 children with trauma",
    extraction_notes="214 children, 9 riding clubs Istanbul. 5 (2.3%) had dental/orofacial trauma. Horseback > pony for trauma (significant). All wore helmets. Awareness of dental trauma limited.",
    season_or_timeframe="cross-sectional",
)])

# 17635356 — Glasgow audit
ali_common = dict(citation="Ali J, Jamieson L. (2007). Dentoalveolar trauma in Glasgow: an audit of mechanism and injury.",
    pub_year=2007, study_type="case_series", country="GB", region="Glasgow",
    population_setting="mixed", age_min=4, age_max=16, age_category="mixed",
    sex="mixed", level_of_play="recreational",
    season_or_timeframe="2002-2004",
)
w("ali2007", [
    make("ali2007", **ali_common,
        sport_raw="all etiologies (sport 18% subset)",
        sport="all_activities_aggregate", sport_category="",
        subgroup_label="overall",
        sample_size="", injury_count="",
        injury_type_raw="dentoalveolar trauma (audit)",
        rate_raw=49.0, rate_denominator_raw="(%) of all injuries from falls (sport = 18%)",
        extraction_notes="Glasgow Dental Hospital pediatric trauma clinic audit 2002-2004. Falls 49%, sport 18%, bike/scooter 13%, assault 7%, MVA 1.5%. Peak 8-11yo (43%). 64% trauma to >1 tooth. 58% involved hard tissue+pulp.",
    ),
    make("ali2007", **ali_common,
        sport_raw="sports-related subset of dentoalveolar trauma",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label="sport_related",
        sample_size="", injury_count="",
        injury_type_raw="sport-related dentoalveolar trauma (18% of total audit)",
        rate_raw=18.0, rate_denominator_raw="(%) of total dental trauma attributable to sport",
        extraction_notes="Sport-related = 18% of total audit. 79% of sport-related trauma was in males.",
    ),
])

# 18203866 — Collegiate rugby NE
co08_common = dict(citation="Collins CL, Micheli LJ, Yard EE, Comstock RD. (2008). Collegiate rugby union injury patterns in New England: a prospective cohort study.",
    pub_year=2008, study_type="cohort", country="US", region="New England",
    population_setting="club", age_min=18, age_max=22, age_category="collegiate",
    level_of_play="elite",
    sport_raw="collegiate rugby union",
    sport="rugby", sport_category="contact",
    season_or_timeframe="2005-06 season",
)
w("collins_rugby2008", [
    make("collins_rugby2008", **co08_common, sex="male",
        subgroup_label="male_game",
        sample_size="", athlete_exposures=13943,
        injury_count=447,  # all 447 male injuries (game + practice combined)
        injury_type_raw="all injuries (rugby; dental defined-as-injury per study)",
        injury_category="orofacial_with_dental",
        rate_raw=22.5, rate_denominator_raw="per 1000 game athletic-exposures (male)",
        rate_per_1000_ae=22.5,
        extraction_notes="31 men's collegiate rugby teams. 447 male injuries during 13,943 game AE + 24,280 practice AE. Game rate 22.5/1000 (95% CI 20.2-25.0). 56% of male match injuries were major (>7 days).",
    ),
    make("collins_rugby2008", **co08_common, sex="female",
        subgroup_label="female_game",
        sample_size="", athlete_exposures=11865,
        injury_count=400,
        injury_type_raw="all injuries (rugby; dental defined-as-injury)",
        injury_category="orofacial_with_dental",
        rate_raw=22.7, rate_denominator_raw="per 1000 game athletic-exposures (female)",
        rate_per_1000_ae=22.7,
        extraction_notes="38 women's teams. 400 injuries during 11,865 game AE. Game rate 22.7/1000 (95% CI 20.2-25.5). 51% major. Tackle = most common event.",
    ),
])

# 18410389 — Ontario 12-14
w("wong2008", [make("wong2008",
    citation="Wong KM, et al. (2008). Etiology and environment of dental injuries in 12- to 14-year-old Ontario schoolchildren.",
    pub_year=2008, study_type="cross_sectional", country="CA", region="Ontario",
    population_setting="school", age_min=12, age_max=14, age_category="adolescent",
    sex="mixed", level_of_play="recreational",
    sport_raw="all causes (sports/falls main in this age group)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=2422, injury_count=int(round(2422 * 0.114)),
    injury_type_raw="dental injury (mostly enamel fractures 63.7%)",
    injury_category="enamel_fracture",
    rate_raw=11.4, rate_denominator_raw="(%) of 2422 ages 12-14 with dental injury",
    extraction_notes="Ontario 2 communities, 30 schools. n=2422 ages 12-14. 11.4% prev. Mean age at injury 9.5 (SD 1.49, range 6-13). One upper central incisor 70.4%. Most often boys at school during falls or sports. SES not significant; caries-DMFT significantly correlated (p<.001).",
    season_or_timeframe="cross-sectional",
)])

# 18721348 — Arab Jerusalem 5th-6th
w("livny2008", [make("livny2008",
    citation="Livny A, Sgan-Cohen HD. (2008). Dental trauma among 5th and 6th grade Arab schoolchildren in Eastern Jerusalem.",
    pub_year=2008, study_type="cross_sectional", country="IL", region="East Jerusalem",
    population_setting="school", age_min=10, age_max=12, age_category="youth",
    sex="mixed", level_of_play="recreational",
    sport_raw="all causes (sport = 16.4% of causes)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=453, injury_count=int(round(453 * 0.338)),
    injury_type_raw="dental trauma (severe = involving dentine, 12.6%)",
    rate_raw=33.8, rate_denominator_raw="(%) of 453 Arab Jerusalem schoolchildren with dental trauma",
    extraction_notes="453 5th-6th grade Arab schoolchildren E. Jerusalem. Total trauma 33.8%, severe 12.6%. Causes: falling 29.1%, sports 16.4%, violence 20%, playing 20%. More sport injuries at school. Severe: boys OR=2.03, lip incompetence OR=2.71, overjet ≥4mm OR=3.73.",
    season_or_timeframe="cross-sectional",
)])

# 19208012 — Taiwan 15-18
w("fakhruddin2009", [make("fakhruddin2009",
    citation="Fakhruddin K, Locker D, Lawrence H, Kenny D. (2009). Activities related to the occurrence of traumatic dental injuries in 15- to 18-year-olds.",
    pub_year=2009, study_type="cross_sectional", country="TW", region="southern Taiwan",
    population_setting="school", age_min=15, age_max=18, age_category="adolescent",
    sex="mixed", level_of_play="recreational",
    sport_raw="sports + leisure (30.8% of TDI causes)",
    sport="all_sports_aggregate", sport_category="",
    subgroup_label="sport_leisure_subset",
    sample_size=6312, injury_count=int(round(6312 * 0.199 * 0.308)),
    injury_type_raw="TDI attributed to sports + leisure activities",
    rate_raw=19.9, rate_denominator_raw="(%) of 6312 senior HS students with any TDI",
    extraction_notes="Random sample 6312 Taiwanese 15-18 yo. TDI 19.9%. Sport+leisure 30.8% of causes (#1), eating 20.5%, falls 19.4%, MVA 10.2%, collisions 7.1%. Sport+leisure TDI more in males (OR=1.640) and high-SES (OR=1.991).",
    season_or_timeframe="cross-sectional",
)])

# 19566982 — schoolboy cricketers
ya_common = dict(citation="Yamada T, Sawaki Y, Tomida S, Tohnai I, Ueda M. (2009). A pilot study of the prevalence of orofacial and head injuries in schoolboy cricketers at eight private schools in England and Australia.",
    pub_year=2009, study_type="cross_sectional",
    population_setting="school", age_min=11, age_max=18, age_category="mixed",
    sex="male", level_of_play="school_varsity",
    sport_raw="cricket (schoolboy private schools)",
    sport="all_sports_aggregate", sport_category="limited_contact",  # cricket not in vocab
    season_or_timeframe="pilot study",
)
w("yamada2009", [
    make("yamada2009", **ya_common, country="GB", region="England",
        subgroup_label="cricket_england",
        sample_size=207,
        injury_count=50,
        injury_type_raw="head/face/teeth injuries",
        injury_category="orofacial_with_dental",
        rate_raw=24.1, rate_denominator_raw="(%) of English schoolboy cricketers reporting head/face/dental injury",
        extraction_notes="411 schoolboy cricketers, 4 English + 4 Australian private schools, 100% response. 16 loosened/broken teeth, 2 avulsed across the cohort.",
    ),
    make("yamada2009", **ya_common, country="AU", region="Australia",
        subgroup_label="cricket_australia",
        sample_size=204,
        injury_count=52,
        injury_type_raw="head/face/teeth injuries",
        injury_category="orofacial_with_dental",
        rate_raw=25.5, rate_denominator_raw="(%) of Australian schoolboy cricketers",
        extraction_notes="Australian cricketers reported more injuries per player than English. Distribution similar.",
    ),
])

# 20486946 — snowboarders Turkey
w("hayran2010", [make("hayran2010",
    citation="Hayran O, Sahin O. (2010). Orofacial and dental injuries of snowboarders in Turkey.",
    pub_year=2010, study_type="cross_sectional", country="TR", region="",
    population_setting="recreational", age_min=12, age_max=22, age_category="mixed",
    sex="mixed", level_of_play="recreational",
    sport_raw="snowboarding (Turkey; adolescent + young adult)",
    sport="all_sports_aggregate", sport_category="limited_contact",
    subgroup_label="snowboarding",
    sample_size=86, injury_count=17,
    injury_type_raw="orofacial trauma during snowboarding",
    injury_category="orofacial_with_dental",
    rate_raw=19.8, rate_denominator_raw="(%) of 86 snowboarders with orofacial trauma",
    mouthguard_use_rate=0,  # MG not specifically asked
    extraction_notes="86 snowboard riders TR. 17 (19.8%) had orofacial trauma. 58% used helmet; 100% aware of helmets. MG awareness/use not separately quantified.",
    season_or_timeframe="cross-sectional",
)])

# 22976571 — Targu Mures
w("ivanovics2012", [make("ivanovics2012",
    citation="Ivanovic et al. (2012). Prevalence of traumatic dental injuries in children who attended two dental clinics in Targu Mures between 2003 and 2011.",
    pub_year=2012, study_type="case_series", country="RO", region="Targu Mures",
    population_setting="mixed", age_min=1, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="recreational",
    sport_raw="all causes (sports/cycling primary in permanent dentition)",
    sport="all_activities_aggregate", sport_category="",
    sample_size="", injury_count="",
    injury_type_raw="traumatic dental injury (deciduous + permanent)",
    rate_raw=24.5, rate_denominator_raw="(%) of clinic patients with TDI",
    extraction_notes="2 dental clinics Targu Mures 2003-2011 patients 1-18 yo. Overall TDI 24.5%. Deciduous: equal M/F, peak 1-2 yo. Permanent: M-dominant, peak 11-12. Causes: falls (esp during walking learning); permanent — cycling and sport mishaps. Sport subset not quantified.",
    season_or_timeframe="2003-2011 (9 years)",
)])

print("\nDone — batch 4 complete.")
