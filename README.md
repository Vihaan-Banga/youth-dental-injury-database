# Youth Sports Dental Injury Database

[![Validate master.csv](https://github.com/Vihaan-Banga/youth-dental-injury-database/actions/workflows/validate.yml/badge.svg)](https://github.com/Vihaan-Banga/youth-dental-injury-database/actions/workflows/validate.yml)
[![Website](https://img.shields.io/badge/website-vihaan--banga.github.io-blue)](https://vihaan-banga.github.io/youth-dental-injury-database/)

**Website:** https://vihaan-banga.github.io/youth-dental-injury-database/

An open-access harmonized database aggregating epidemiological data on dental and orofacial injuries in youth sports, drawn from national surveillance systems, published research, and sport-governing-body reports.

**Status:** Pre-launch (data collection phase). Not yet published. Do not cite externally until v1.0 release.

**Project lead:** Vihaan Banga, Olentangy Liberty High School, in collaboration with [Advisor name when secured].

## At a glance

| | |
|---|---|
| Harmonized rows | **421** |
| Distinct sources | **103** (90 peer-reviewed papers · 12 NEISS treatment-years · 1 governing-body report) |
| Countries | **28** |
| Publication years | **2000–2026** (per PROTOCOL §3.1) |
| NEISS case-level coverage | **12 treatment-years** (2013–2019, 2021–2025; 2020 is a real COVID-era gap), ~8,800 underlying records |
| Validation | **0 FAILs / 0 WARNs** across 13 automated checks (run in CI on every push) |
| Provenance | every row author-verified against PubMed; carries `measure_type`, `comparability_group`, and `data_provenance` flags |

## What this is and isn't

This is a *secondary data* project. We are not collecting injuries directly from athletes or clinicians. We are aggregating data that has already been collected and published by national surveillance systems, peer-reviewed studies, and sport-governing-body injury reports, then standardizing it into a single comparable format.

The gap we fill: youth dental injury data exists in dozens of fragmented sources using different definitions, age ranges, and injury classifications. No unified resource lets a researcher answer questions like "what is the rate of avulsed teeth across youth contact sports in North America?" without manually reconciling 40 papers. We are building that resource.

## Comparability & limitations (read before comparing rows)

Harmonizing these sources into one schema does **not** make every row comparable. Sources use fundamentally different measures, so each row carries a `measure_type` and a `comparability_group` (see `DATA_DICTIONARY.md`), and **values are only directly comparable within the same `comparability_group`.**

- **Denominators differ.** Rows are incidence per athlete-exposure, per player/athlete-hours, per 100,000 population, per season, prevalence proportions, ED-visit estimates, or raw counts. Only rows sharing the same `measure_type` are comparable; for per-AE rates use the normalized `rate_per_1000_ae`.
- **NEISS figures are emergency-department-treated only** (weighted national estimates). They undercount injuries treated in dental/primary-care settings and are **not** comparable to athlete-exposure rates.
- **Aggregate rows exist** (`all_sports_aggregate`, `all_activities_aggregate`, etc.) — do not pool them with sport-specific rows.
- **Definitions and inclusion criteria vary** across sources (e.g., all-cause dental-trauma prevalence vs sport-related ED-treated incidence). Make cross-source comparisons within a `comparability_group`, not naively across the whole table.
- **Quality:** all current rows are `quality_flag = partial_data` — validated against schema and controlled vocabularies, with full-text numeric verification still pending.

## Repository structure

```
youth-dental-injury-database/
├── README.md                  This file
├── PROTOCOL.md                Pre-registered research protocol — read this first
├── DATA_DICTIONARY.md         Column-by-column definitions of the master dataset
├── data/
│   ├── raw/                   Original downloaded sources (NEISS CSVs, paper PDFs)
│   │   ├── neiss/
│   │   ├── papers/
│   │   └── surveillance_reports/
│   ├── extracted/             Tables and figures extracted from each source
│   ├── cleaned/               Per-source cleaned data, one file per source
│   └── harmonized/            The unified database (master.csv)
├── scripts/                   Python scripts for download, extraction, harmonization
├── docs/
│   ├── sources.md             Running list of all candidate sources with status
│   ├── decisions.md           Log of every harmonization decision and why
│   └── meeting_notes/         Notes from advisor meetings
└── outputs/
    ├── figures/               Charts for the methods paper and website
    └── tables/                Summary tables
```

## How to use this repo (workflow)

1. **Read PROTOCOL.md first.** It defines what's in, what's out, and how decisions get made.
2. **Add candidate sources to `docs/sources.md`** as you find them. Mark status (identified → screened → included → extracted → harmonized).
3. **Extract data from included sources** into `data/extracted/<source_id>.csv` using the template in `DATA_DICTIONARY.md`.
4. **Log every non-obvious harmonization decision** in `docs/decisions.md`. When a future reviewer asks "why did you classify X this way?" — you need an answer.
5. **Run harmonization scripts** to build `data/harmonized/master.csv`.
6. **Commit early and often.** Every meaningful change gets a git commit with a clear message.

## How this will be cited (when published)

```
Banga, V., [Advisor name]. (2026). Youth Sports Dental Injury Database (Version 1.0)
[Data set]. Zenodo. https://doi.org/[TBD]
```

A `CITATION.cff` file is at the repo root — GitHub renders a "Cite this repository" button on the repo home.

## License

- **Code:** MIT — see [`LICENSE`](LICENSE)
- **Data:** Creative Commons Attribution 4.0 International (CC BY 4.0) — see [`LICENSE-DATA`](LICENSE-DATA)

Use the code freely (with attribution per MIT). Use the data freely (with attribution per CC BY 4.0). The two-license split is standard for open-research projects: open code, open data.

## Contact

Vihaan Banga — GitHub [@Vihaan-Banga](https://github.com/Vihaan-Banga) Email: vihaansbanga@gmail.com
