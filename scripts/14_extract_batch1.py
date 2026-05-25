#!/usr/bin/env python3
"""Batch 1 of bulk abstract-only extractions for screened_included papers.

Twelve high-priority sources extracted from their PubMed abstracts. All rows
quality_flag = 'partial_data'. Generated 2026-05-24 overnight.

Each source produces 1-3 rows depending on how much the abstract stratifies
(aggregate, plus per-sex / per-sport breakdowns where the abstract gives them).
"""

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

EXTRACTOR = "VB-AI-assisted-2026-05-24"
EXTRACTION_DATE = "2026-05-24"


def make(source_id, **kw):
    """Build a row with defaults, overridden by kw."""
    base = {c: "" for c in COLUMNS}
    base.update(dict(
        source_id=source_id,
        peer_reviewed="TRUE",
        extraction_basis="youth_primary",
        exposure_context="all",
        injury_category="unspecified_dental",
        mouthguard_required="unspecified",
        mouthguard_injury_relation="not_addressed",
        extraction_date=EXTRACTION_DATE,
        extractor=EXTRACTOR,
        quality_flag="partial_data",
    ))
    base.update(kw)
    return base


def write_csv(source_id, rows):
    path = OUT / f"{source_id}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLUMNS})
    print(f"wrote {path.name} ({len(rows)} rows)")


# ----- hamdan2026 (PMID 41501720) -----
hamdan_cite = "Hamdan TR, Alshayeb L, Dashash M. (2026). Prevalence and risk factors of orofacial trauma among child and adolescent athletes in Damascus, Syria: a cross-sectional study. BMC Public Health."
write_csv("hamdan2026", [make("hamdan2026",
    citation=hamdan_cite, pub_year=2026, study_type="cross_sectional",
    country="SY", region="Damascus", population_setting="club",
    age_min=6, age_max=16, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    sport_raw="multiple sports — contact and non-contact",
    sport="all_sports_aggregate", sport_category="",
    sample_size=445, season_or_timeframe="cross-sectional study period",
    injury_count=int(round(445 * 0.474)),
    injury_type_raw="orofacial dental trauma (self-reported + clinical exam, WHO criteria)",
    rate_raw=47.4,
    rate_denominator_raw="prevalence (%) among 445 child/adolescent athletes",
    mouthguard_use_rate=0.339,
    mouthguard_injury_relation="analyzed",
    extraction_notes="11 sports clubs Damascus, multistage cluster sampling. Contact sports (football, basketball) had higher rates than gymnastics/karate. MG use significantly associated with reduced ODT risk (OR=0.286, 95% CI 0.141-0.577, p<0.004).",
)])


# ----- udayamalee2024 (PMID 38131151) -----
ud_cite = "Udayamalee I, Amarasinghe H, Zhang P. (2024). Oro-dental trauma burden and mouthguard usage among contact sports players: A call for sports dentistry initiatives in Sri Lanka. Dental Traumatology."
ud_common = dict(citation=ud_cite, pub_year=2024, study_type="cross_sectional",
    country="LK", region="Colombo", population_setting="school",
    age_min=13, age_max=18, age_category="adolescent",
    sex="mixed", level_of_play="school_varsity",
    season_or_timeframe="cross-sectional",
    sample_size=1340, mouthguard_use_rate=0.208, mouthguard_injury_relation="analyzed",
)
write_csv("udayamalee2024", [
    make("udayamalee2024", **ud_common,
        sport_raw="all contact sports (aggregate: football, rugby, hockey, boxing, basketball, martial arts)",
        sport="all_sports_aggregate", sport_category="contact",
        subgroup_label="all_sports_aggregate",
        injury_count=int(round(1340 * 0.359)),
        injury_type_raw="self-reported oro-dental trauma in last 12 months",
        rate_raw=35.9,
        rate_denominator_raw="self-reported pooled ODT prevalence (%) in 1340 contact-sport school children",
        extraction_notes="Adolescent contact-sport school players Colombo. 63.1% male / 36.9% female. ODT highest in boxing, rugby, hockey. Dental trauma 23.8% (uncomplicated 15.8% + complicated 8%); soft tissue 12.1%. 91% of MG users wore ready-made.",
    ),
    make("udayamalee2024", **ud_common,
        sport_raw="all contact sports (dental-trauma subset)",
        sport="all_sports_aggregate", sport_category="contact",
        subgroup_label="dental_trauma_subset",
        injury_count=319, injury_type_raw="dental trauma (15.8% uncomplicated + 8% complicated)",
        rate_raw=23.8, rate_denominator_raw="dental-trauma-specific prevalence (%) within 1340",
        extraction_notes="Of 1340 players, 319 (23.8%) had dental trauma (211 uncomplicated, 108 complicated). 0+/-12 mo recall.",
    ),
])


# ----- vanierssel2021 (PMID 33848349) -----
vi_cite = "van Ierssel J, Ledoux AA, Tang K, Zemek R. (2021). Sex-Based Differences in Symptoms With Mouthguard Use After Pediatric Sport-Related Concussion. Journal of Athletic Training."
write_csv("vanierssel2021", [make("vanierssel2021",
    citation=vi_cite, pub_year=2021, study_type="cohort",
    country="CA", region="", population_setting="mixed",
    age_min=5, age_max=18, age_category="mixed",
    sex="mixed", level_of_play="mixed",
    sport_raw="collision/contact sports (multi-sport ED cohort)",
    sport="all_sports_aggregate", sport_category="contact",
    sample_size=1019, season_or_timeframe="9-site prospective cohort",
    injury_count=1019, injury_type_raw="sport-related concussion (collision/contact sport, ED-assessed within 48h)",
    injury_category="concussion",
    mouthguard_use_rate=0.42,
    mouthguard_injury_relation="analyzed",
    extraction_notes="9 Canadian pediatric EDs. 73% male. Median age 13.43 (IQR 11.01-15.27). 42% wore MG at injury. PRIMARY OUTCOME = concussion symptoms (not dental injury); included because §3.3 captures concussion + MG-relation. No significant group-by-sex-by-time interaction for symptoms.",
)])


# ----- goswami2017 (PMID 29403232) -----
go_cite = "Goswami M, Kumar P, Bhushan U. (2017). Evaluation of Knowledge, Awareness, and Occurrence of Dental Injuries in Participant Children during Sports in New Delhi: A Pilot Study. Int J Clin Pediatr Dent."
go_common = dict(citation=go_cite, pub_year=2017, study_type="cross_sectional",
    country="IN", region="New Delhi", population_setting="school",
    age_min=6, age_max=16, age_category="mixed",
    level_of_play="mixed", sample_size=450,
    sport_raw="multiple sports (children participating in sports)",
    sport="all_sports_aggregate", sport_category="",
    mouthguard_use_rate=0.209, mouthguard_injury_relation="mentioned_only",
    season_or_timeframe="cross-sectional pilot",
)
write_csv("goswami2017", [
    make("goswami2017", **go_common, sex="mixed",
        subgroup_label="tooth_fracture",
        injury_count=27, injury_type_raw="chipping or fracture of teeth",
        injury_category="crown_fracture",
        rate_raw=6.0, rate_denominator_raw="(%) of 450 children",
        extraction_notes="450 children 6-16, New Delhi. 69.6% male, mean age 12.6. Aware of MG 71.3%; used MG 20.9%.",
    ),
    make("goswami2017", **go_common, sex="mixed",
        subgroup_label="avulsion",
        injury_count=24, injury_type_raw="avulsion of teeth",
        injury_category="avulsion",
        rate_raw=5.4, rate_denominator_raw="(%) of 450 children",
        extraction_notes="Avulsion subset, same cohort.",
    ),
    make("goswami2017", **go_common, sex="mixed",
        subgroup_label="soft_tissue_laceration",
        injury_count=25, injury_type_raw="soft-tissue laceration",
        injury_category="other_dental",
        rate_raw=5.6, rate_denominator_raw="(%) of 450 children",
        extraction_notes="Soft-tissue laceration subset (oral lacerations).",
    ),
    make("goswami2017", **go_common, sex="mixed",
        subgroup_label="jaw_bone_fracture",
        injury_count=18, injury_type_raw="jaw/bone fracture",
        injury_category="orofacial_with_dental",
        rate_raw=4.0, rate_denominator_raw="(%) of 450 children",
        extraction_notes="Jaw/bone fracture subset.",
    ),
])


# ----- tsuchiya2017 (PMID 29284466) -----
ts_cite = "Tsuchiya S, Tsuchiya M, Momma H, Sekiguchi T. (2017). Factors associated with sports-related dental injuries among young athletes: a cross-sectional study in Miyagi prefecture. BMC Oral Health."
ts_common = dict(citation=ts_cite, pub_year=2017, study_type="cross_sectional",
    country="JP", region="Miyagi prefecture", population_setting="school",
    age_min=6, age_max=15, age_category="mixed",
    sport_raw="multiple sports (school-aged athletes)",
    sport="all_sports_aggregate", sport_category="",
    level_of_play="school_jv", season_or_timeframe="cross-sectional self-report",
    mouthguard_injury_relation="mentioned_only",
)
write_csv("tsuchiya2017", [
    make("tsuchiya2017", **ts_common, sex="mixed", sample_size=5735,
        subgroup_label="overall",
        injury_count=763, injury_type_raw="self-reported sports-related dental injury",
        rate_raw=13.3,
        rate_denominator_raw="(%) of 5735 school-aged athletes",
        extraction_notes="Large self-report cohort 6-15. Insufficient break, verbal abuse, physical punishment from coaches associated with higher dental injury prevalence in males only.",
    ),
    make("tsuchiya2017", **ts_common, sex="male", sample_size=4132,
        subgroup_label="sex_male",
        injury_count=592, rate_raw=14.3, rate_denominator_raw="(%) of 4132 males",
        extraction_notes="Male subset.",
    ),
    make("tsuchiya2017", **ts_common, sex="female", sample_size=1603,
        subgroup_label="sex_female",
        injury_count=171, rate_raw=10.7, rate_denominator_raw="(%) of 1603 females",
        extraction_notes="Female subset. OR vs male 1.48 (1.22-1.79) for male predominance.",
    ),
])


# ----- singh2014 (PMID 25520762) -----
si_cite = "Singh G, Garg S, Damle SG, Dhindsa A. (2014). A study of sports related occurrence of traumatic orodental injuries and associated risk factors in high school students in north India. Asian J Sports Med."
write_csv("singh2014", [
    make("singh2014",
        citation=si_cite, pub_year=2014, study_type="cross_sectional",
        country="IN", region="North India", population_setting="school",
        age_min=8, age_max=16, age_category="mixed",
        sex="mixed", level_of_play="school_varsity",
        sport_raw="multiple organized school sports (aggregate)",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label="all_sports",
        sample_size=1105,
        injury_count=335, injury_type_raw="traumatic orodental injury",
        rate_raw=30.3, rate_denominator_raw="(%) of 1105 HS students",
        mouthguard_injury_relation="mentioned_only",
        extraction_notes="1105 students from 19 school sports teams/academies, multistage cluster sampling. Soft tissue 48%, tooth fractures 43%. High-velocity sports 44.1% and medium-intensity 46.6% of injuries. MG use: boys 6%, girls 2%.",
        season_or_timeframe="cross-sectional",
    ),
    make("singh2014",
        citation=si_cite, pub_year=2014, study_type="cross_sectional",
        country="IN", region="North India", population_setting="school",
        age_min=8, age_max=16, age_category="mixed",
        sex="mixed", level_of_play="school_varsity",
        sport_raw="basketball (highest-rate sport in study)",
        sport="basketball", sport_category="limited_contact",
        subgroup_label="",
        sample_size="",
        rate_raw=50.0,
        rate_denominator_raw="(%) of basketball players with injury (sport-specific within study)",
        extraction_notes="Basketball had highest injury rate at 50% (p<0.05). Compared to badminton (lowest at 6.1%).",
        season_or_timeframe="cross-sectional",
    ),
])


# ----- chan2011 (PMID 21457187) -----
ch_cite = "Chan YM, Williams S, Davidson LE, Drummond BK. (2011). Orofacial and dental trauma of young children in Dunedin, New Zealand. Dental Traumatology."
write_csv("chan2011", [make("chan2011",
    citation=ch_cite, pub_year=2011, study_type="case_series",
    country="NZ", region="Dunedin", population_setting="mixed",
    age_min=0, age_max=10, age_category="youth",
    sex="mixed", level_of_play="recreational",
    sport_raw="multiple — sport one of several causes (collisions, falls, sports)",
    sport="all_activities_aggregate", sport_category="",
    sample_size=288, season_or_timeframe="1999-2000 (2-year retrospective)",
    injury_count=300, injury_type_raw="orofacial trauma episodes (288 children, 300 incidents)",
    injury_category="orofacial_with_dental",
    extraction_notes="University Dental School clinic Dunedin. Ages 0-10. 86.6% had cause noted. In younger children mainly falls; in school-aged children sports + collisions + falls. Predominant dental injuries: concussions and subluxations (more common in primary dentition, p<0.001). Upper central incisors most affected. Lip injuries dominant non-dental.",
    quality_flag="partial_data",
)])


# ----- cetinbas2008 (PMID 18821957) -----
ce_cite = "Cetinbaş T, Yildirim G, Sönmez H. (2008). The relationship between sports activities and permanent incisor crown fractures in a group of school children aged 7-9 and 11-13 in Ankara, Turkey. Dental Traumatology."
write_csv("cetinbas2008", [
    make("cetinbas2008",
        citation=ce_cite, pub_year=2008, study_type="cross_sectional",
        country="TR", region="Ankara", population_setting="school",
        age_min=7, age_max=13, age_category="youth",
        sex="mixed", level_of_play="recreational",
        sport_raw="all sports (aggregate)",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label="all_sports",
        sample_size=2570,
        injury_count=191, injury_type_raw="permanent maxillary/mandibular incisor crown fracture (any cause)",
        injury_category="crown_fracture",
        rate_raw=7.43, rate_denominator_raw="(%) of 2570 schoolchildren with dental trauma",
        mouthguard_injury_relation="mentioned_only",
        extraction_notes="2570 students, 10 primary schools, 5 Ankara municipalities. 14.14% of incisal fractures were sport-related. 84% maxillary central incisors. Males higher than females in older group (p<0.01). Bicycling caused significantly higher crown fractures than other sports (p<0.05).",
        season_or_timeframe="cross-sectional",
    ),
    make("cetinbas2008",
        citation=ce_cite, pub_year=2008, study_type="cross_sectional",
        country="TR", region="Ankara", population_setting="school",
        age_min=7, age_max=13, age_category="youth",
        sex="mixed", level_of_play="recreational",
        sport_raw="sport-related subset of incisor crown fractures",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label="sport_related_subset",
        sample_size="",
        injury_count=int(round(222 * 0.1414)),
        injury_type_raw="permanent incisor crown fracture caused by sport (14.14% of 222 fractures)",
        injury_category="crown_fracture",
        rate_raw=14.14, rate_denominator_raw="(%) of fractures attributed to sport",
        extraction_notes="14.14% of the 222 fractured incisors attributed to sport activities (~31 of 222).",
        season_or_timeframe="cross-sectional",
    ),
])


# ----- levin2007 (PMID 17991235) -----
lv7_cite = "Levin L, Samorodnitzky GR, Schwartz-Arad D, Geiger SB. (2007). Dental and oral trauma during childhood and adolescence in Israel: occurrence, causes, and outcomes. Dental Traumatology."
write_csv("levin2007", [make("levin2007",
    citation=lv7_cite, pub_year=2007, study_type="cross_sectional",
    country="IL", region="", population_setting="mixed",
    age_min=18, age_max=21, age_category="collegiate",
    sex="mixed", level_of_play="mixed",
    sport_raw="multi-sport (childhood/adolescence retrospective recall)",
    sport="all_sports_aggregate", sport_category="",
    sample_size=427,
    injury_count=72, injury_type_raw="dental injuries (lifetime recall)",
    rate_raw=16.9, rate_denominator_raw="(%) of 427 young adults with dental injury",
    mouthguard_use_rate=0.028,
    mouthguard_injury_relation="mentioned_only",
    extraction_notes="427 young adults aged 18-21, lifetime recall. 31.1% had oral/dental injuries (133 total); 72 (16.9%) dental. Causes of dental injuries: falls 64%, sport 23.2%, fights 7.2%, MVA 5.6%. Laceration 47.3% / fracture 41.9%. MG aware 22.6%; MG used 2.8%.",
    season_or_timeframe="lifetime recall",
)])


# ----- shore2023 (PMID 36394781) -----
sh_cite = "Shore E, O'Connell AC. (2023). Assessment of mouthguards worn by Irish children playing contact sports: an observational cross-sectional cohort study. European Archives of Paediatric Dentistry."
write_csv("shore2023", [make("shore2023",
    citation=sh_cite, pub_year=2023, study_type="cross_sectional",
    country="IE", region="", population_setting="club",
    age_min=9, age_max=16, age_category="mixed",
    sex="mixed", level_of_play="club",
    sport_raw="Gaelic football (Irish children, men's variant inferred)",
    sport="gaelic_football_mens", sport_category="contact",
    subgroup_label="mg_quality_assessment",
    sample_size=106, injury_count="",
    injury_type_raw="(MG-quality assessment cohort — not injury-count study)",
    mouthguard_use_rate=1.0,  # all 106 presented WITH MG (cohort definition)
    mouthguard_injury_relation="mentioned_only",
    extraction_notes="n=106 Gaelic football children 9-16 with MG. 66.96% mouth-formed; 3.77% custom; rest stock. 81.13% inadequate retention, 83.96% inadequate labial extension. Study focuses on MG quality (not injury rates). Included because §3.3 captures MG use; no injury counts to extract.",
    season_or_timeframe="cross-sectional",
)])


# ----- amy2005 (PMID 15876321) -----
am_cite = "Amy E. (2005). Oro-facial injuries in Central American and Caribbean sports games: a 20-year experience. Dental Traumatology."
write_csv("amy2005", [make("amy2005",
    citation=am_cite, pub_year=2005, study_type="case_series",
    country="PR", region="",  # Puerto Rican delegation
    population_setting="club", level_of_play="elite",  # international games
    age_min=15, age_max=35, age_category="mixed",
    extraction_basis="youth_primary",  # mixed-age with youth subset
    sex="mixed",
    sport_raw="multi-sport international games (Puerto Rican delegation, 1980s-2005)",
    sport="all_sports_aggregate", sport_category="",
    sample_size=2107,
    injury_count=18, injury_type_raw="acute/emergency orofacial conditions",
    injury_category="orofacial_with_dental",
    rate_raw=6.0, rate_denominator_raw="(%) of 279 dental-clinic visits = 18 acute orofacial cases",
    extraction_notes="20-year retrospective of Central American + Caribbean Sports Games dental services for the Puerto Rican delegation. 2107 total participants across 6 delegations. 279 (13.2%) seen for dental conditions. 18 (6% of 279, 0.85% of all participants) acute orofacial. Lip contusion most frequent (n=4). Basketball had most injuries (n=3). Note: international elite multi-age games; some delegations include youth.",
    season_or_timeframe="20-year retrospective (~1985-2005)",
)])


# ----- levin2003 (PMID 14708646) -----
lv3_cite = "Levin L, Friedlander LD, Geiger SB. (2003). Dental and oral trauma and mouthguard use during sport activities in Israel. Dental Traumatology."
lv3_common = dict(citation=lv3_cite, pub_year=2003, study_type="cross_sectional",
    country="IL", region="", population_setting="mixed",
    age_min=18, age_max=19, age_category="collegiate",
    sex="male", level_of_play="mixed",
    sample_size=943, season_or_timeframe="cross-sectional",
    mouthguard_use_rate=0.03, mouthguard_injury_relation="mentioned_only",
)
write_csv("levin2003", [
    make("levin2003", **lv3_common,
        sport_raw="multi-sport (aggregate, 850 active in at least one sport)",
        sport="all_sports_aggregate", sport_category="",
        subgroup_label="all_sports",
        injury_count=229, injury_type_raw="dental and oral injuries during sport",
        rate_raw=27.0, rate_denominator_raw="(%) of participants with any oral/dental injury",
        extraction_notes="943 young adults (95% male, 5% female), ages 18-19, Israel. 850 (90%) active in >=1 sport. 27% had injuries (229 total); 9% had dental injuries (73). MG aware 27%; MG used 3%.",
    ),
    make("levin2003", **lv3_common,
        sport_raw="basketball",
        sport="basketball", sport_category="limited_contact",
        subgroup_label="",
        injury_count=int(round(229 * 0.42)),
        injury_type_raw="dental and oral injuries from basketball",
        rate_raw=7.2, rate_denominator_raw="(%) of basketball players injured (~96 of total sample played basketball)",
        extraction_notes="Basketball-attributable: 42% of all sport-related injuries; 7.2% of basketball players reported injury.",
    ),
    make("levin2003", **lv3_common,
        sport_raw="soccer (football_association)",
        sport="football_association", sport_category="limited_contact",
        subgroup_label="",
        injury_count=int(round(229 * 0.41)),
        injury_type_raw="dental and oral injuries from soccer",
        rate_raw=6.6, rate_denominator_raw="(%) of soccer players injured",
        extraction_notes="Soccer-attributable: 41% of all sport-related injuries; 6.6% of soccer players reported injury.",
    ),
])

print("\nDone — batch 1 complete (12 sources).")
