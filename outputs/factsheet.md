# Youth Sports Dental Injury Database — Factsheet

_Auto-generated; reflects `data/harmonized/master.csv` as of the latest harmonization run._

## What it is

An open-access harmonized database of dental and orofacial injury epidemiology in youth sports, ages **5–22**. Aggregates published peer-reviewed studies, national surveillance systems (NEISS, NFHS / High School RIO), and sport-governing-body reports into a single comparable schema. Open data (CC BY 4.0) and open code (MIT).

Repository: **https://github.com/Vihaan-Banga/youth-dental-injury-database**

## Current scale (v0.1-dev)

- **407 rows in master.csv**
- **90 distinct sources** extracted
  - 77 peer-reviewed primary research papers (PubMed-keyed)
  - **12 NEISS year extractions** (2013–2017 via the hadley archive + 2018, 2019, 2021, 2022, 2023, 2024, 2025 directly from CPSC; 2020 returned no matching cases — COVID youth-sport shutdown)
  - 1 international governing-body report (Rugby Europe 2024 U-18 Sevens)
- **~444 candidate sources** identified in total (PubMed-keyed). 91 still pending full-text screening.
- **19+ countries** represented (US, UK, CA, AU, IE, IL, IN, BR, ZA, LB, NZ, JP, TR, ES, HU, RO, AT, KR, SY, LK, KW, etc.)
- **Years covered:** 1996 to 2026 (publication years); treatment-year data 1985–2025.

## Schema highlights

Each row represents one extracted statistic. The data dictionary defines 34 columns including:

- **Source provenance:** citation, DOI, study type, peer-reviewed flag
- **Population:** country, age range + age category (youth 5–12 / adolescent 13–17 / collegiate 18–22 / adult 23+ as comparator), sex, level of play
- **Exposure context:** all / competition / practice / training — disambiguates which slice of the source's data each row represents
- **Subgroup label:** disambiguates mouthguard-user vs nonuser, age-band subsets, etc.
- **Outcome:** raw counts, rates, denominator phrasing, the Andreasen-classification injury category
- **Mouthguard:** mandate status, use rate, whether the source analyzed MG vs injury relationship

`extraction_basis` distinguishes `youth_primary` rows (within the v1.0 scope) from `adult_comparator` rows (extracted alongside when the source reports adult bands).

Validation rules check 10 things — schema, categorical vocabulary, numeric plausibility, age-category consistency, source coverage, uniqueness. **Latest validation: 0 FAILs, 0 WARNs.**

## Sport coverage

Sport-specific rows exist for: basketball, baseball, football (American), football (association/soccer), hockey (ice/field/unspecified), lacrosse, rugby, wrestling, boxing, MMA, softball, volleyball, tennis, track & field, swimming, water polo, gymnastics, cheerleading, skateboarding, martial arts (other / karate / kickboxing / muay thai / judo separately), cricket, netball, cycling, mountain biking, hurling, kabaddi, Gaelic football (m/f), Australian rules football, skiing, snowboarding, equestrian, inline skating, CrossFit, handball, floorball.

## Notable surveillance datasets covered

- **NEISS** — 6 treatment-years (2013–2017 from hadley archive, 2023 directly via CPSC). 4,320+ case-level records filtered for body part = 88 (Mouth) + 23 sport product codes + ages 5–22.
- **National High School Sports-Related Injury Surveillance Study (RIO)** — 8 annual summary reports (2008–2018, 2021–2024); the dental-subset papers `collins2016` and `azadani2023` extracted from the same underlying data.
- **NCAA ISP via Yard 2015** (women's field hockey AE-denominator rates) and via Wormald 2022 (D-I 13 sports maxillofacial — though note the AE-hours vs AE-count denominator distinction).
- **NZ ACC insurance claims** via `welch2010` (sports-related dental claims 1999–2008) and `quarrie2020` (rugby claims 2005–2017, ages 5–40 with full age-band breakdown).
- **Australian Football Injury Prevention Project** via `finch2005` (community-level Aus rules football mouthguard RCT).

## Cross-source internal consistency (sanity check)

Where multiple sources report comparable AE-denominator rates for the same sport, the rates broadly agree:

- **Basketball, US HS:** `collins2016` 0.026 / 100k AE; `azadani2023` 0.024 / 100k AE — essentially identical despite different study windows (2008-14 vs 2005-20).
- **Field hockey, US HS girls:** `collins2016` 0.039 / 100k AE; `azadani2023` 0.035 / 100k AE — also tightly matched.
- **Mouthguard effect (college basketball):** `labella2002` reports 0.12 (MG users) vs 0.67 (non-users) per 1000 AE — a 5.6× difference attributable to MG.

Full cross-source table at [`cross_source_rate_comparison.md`](cross_source_rate_comparison.md).

## What's still in progress

- **Active screening pile:** 91 candidate papers in `needs_human_review` (mostly blocked on age range not visible in the abstract). Most need full-text retrieval.
- **NEISS gap years:** 2018-2022 + 2024-2025 not yet pulled. Pipeline + filter scripts ready to ingest these as soon as the user runs the CPSC query.
- **Pre-registration:** OSF pre-registration not yet filed. Advisor not yet secured.
- **Formal license sign-off:** MIT (code) + CC BY 4.0 (data) are in `LICENSE` / `LICENSE-DATA`, matching PROTOCOL §9, but advisor sign-off pending before v1.0.

## Methods documents

All publicly viewable on the repo:

- **`PROTOCOL.md`** — pre-registration-pending research protocol (inclusion/exclusion criteria, search strategy, harmonization rules).
- **`DATA_DICTIONARY.md`** — column-by-column data dictionary.
- **`docs/decisions.md`** — append-only log of every harmonization decision and why. Includes corrections (e.g., NEISS body-part code labels in PROTOCOL §4.1).
- **`docs/sources.md`** — full audit trail of every candidate source through screening.
- **`outputs/validation_report.md`** — current pass/fail status against the 10 validation checks.
- **`outputs/screening_report_2026-05-21.md`** — per-decision screening audit.

## Citation

`CITATION.cff` is at the repo root; GitHub renders a "Cite this repository" button. v1.0 will include a Zenodo DOI.

```
Banga, V., [Advisor name]. (2026). Youth Sports Dental Injury Database
(Version 1.0) [Data set]. Zenodo. https://doi.org/[TBD]
```

---

_For project-lead correspondence: GitHub @Vihaan-Banga._
