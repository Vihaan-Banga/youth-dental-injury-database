---
layout: default
title: Home
---

# Youth Sports Dental Injury Database

[![Validate master.csv](https://github.com/Vihaan-Banga/youth-dental-injury-database/actions/workflows/validate.yml/badge.svg)](https://github.com/Vihaan-Banga/youth-dental-injury-database/actions/workflows/validate.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/LICENSE)

**An open-access harmonized database of dental and orofacial injury epidemiology in youth sports.**

Aggregating evidence on individuals aged 5–22, drawn from national surveillance systems, peer-reviewed studies, and sport-governing-body reports — into a single comparable schema. CC BY 4.0 for the data; MIT for the code.

---

## At a glance (v0.1-dev, updated 2026-06-12)

|  |  |
|---|---|
| Rows in `master.csv` | **426** |
| Distinct sources | **106** |
| NEISS treatment-years covered | **12** (2013–2019, 2021–2025; 2020 is a real COVID-era gap) |
| Countries represented | **29** |
| Years of publication | 1996–2026 |
| Validation status | **0 FAILs, 0 WARNs** (10 automated checks) |
| Underlying NEISS case-level records | **~8,800** |

> **New:** try the [interactive Rate Explorer](rate-explorer.html) — filter cited dental-injury rates and mouthguard effect sizes by sport and age group. (A population rate explorer, *not* an individual risk calculator — see the note on the page.)

## Comparability & limitations (read before comparing rows)

Harmonizing into one schema does **not** make every row comparable. Each row carries a `measure_type` and `comparability_group`, and **values are only directly comparable within the same `comparability_group`.**

- **Denominators differ** — incidence per athlete-exposure, per player/athlete-hours, per 100,000 population, per season, prevalence proportions, ED-visit estimates, or raw counts. Compare only within the same `measure_type` (use `rate_per_1000_ae` for per-AE rates).
- **NEISS figures are emergency-department-treated only** (weighted national estimates) — they undercount dental-office-treated injuries and are not comparable to athlete-exposure rates.
- **Aggregate rows exist** (`all_sports_aggregate`, etc.) — don't pool them with sport-specific rows.
- **Definitions/inclusion criteria vary** across sources; the Rate Explorer segregates results by `measure_type` for exactly this reason.
- All current rows are `quality_flag = partial_data` (schema-validated; full-text numeric verification pending).

## How to access the data

- **Single best link:** [`data/harmonized/master.csv`](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/data/harmonized/master.csv) — the harmonized master spreadsheet.
- **Per-source CSVs:** [`data/extracted/`](https://github.com/Vihaan-Banga/youth-dental-injury-database/tree/main/data/extracted) — one file per source for audit purposes.
- **NEISS year files:** [`data/extracted/neiss2013.csv`](https://github.com/Vihaan-Banga/youth-dental-injury-database/tree/main/data/extracted) through `neiss2025.csv` (excluding 2020).
- **Raw NEISS dumps:** [`data/raw/neiss/`](https://github.com/Vihaan-Banga/youth-dental-injury-database/tree/main/data/raw/neiss) (gitignored — re-fetch from CPSC).

```python
import pandas as pd
df = pd.read_csv(
    "https://raw.githubusercontent.com/Vihaan-Banga/youth-dental-injury-database/main/data/harmonized/master.csv"
)
df[(df.sport == "basketball") & (df.extraction_basis == "youth_primary")].head()
```

## Methods, documentation, and audit trail

| | |
|---|---|
| Protocol | [`PROTOCOL.md`](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/PROTOCOL.md) — pre-registration-pending research protocol (inclusion criteria, search strategy, harmonization rules) |
| Data dictionary | [`DATA_DICTIONARY.md`](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/DATA_DICTIONARY.md) — column-by-column definitions |
| Source tracking | [`docs/sources.md`](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/docs/sources.md) — every candidate source through screening |
| Governing-body sources | [`docs/governing_body_sources.md`](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/docs/governing_body_sources.md) — non-PubMed surveillance sources |
| Harmonization decisions log | [`docs/decisions.md`](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/docs/decisions.md) — append-only |
| Validation report | [`outputs/validation_report.md`](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/outputs/validation_report.md) |
| Methods-paper draft | [`outputs/methods_paper_draft.md`](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/outputs/methods_paper_draft.md) |

## Derived analyses

- **[NEISS 12-year trends](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/outputs/neiss_trends.md)** — first published aggregation of NEISS youth dental-sport data across 2013–2025.
- **[Cross-source rate comparison](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/outputs/cross_source_rate_comparison.md)** — internal-consistency check across sources reporting the same sport.
- **[Per-sport factsheets](https://github.com/Vihaan-Banga/youth-dental-injury-database/tree/main/outputs/sport_factsheets)** — one-page summary per sport (19 covered).
- **[Per-country breakdown](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/outputs/country_breakdown.md)** — coverage across 29 countries.
- **[Overall factsheet](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/outputs/factsheet.md)** — project-level one-pager.

## Pipeline

A versioned Python pipeline covers source identification → AI-assisted screening → per-source extraction → harmonization → validation → analysis. Reproducibility is enforced via CI: every push to `main` re-runs `scripts/07_harmonize.py` + `scripts/08_validate.py` and fails the build on any FAIL.

```
scripts/00_pubmed_seed_sources.py        # E-utilities seed
scripts/01_parse_abstracts.py            # parse efetch XML to per-PMID JSON
scripts/02_screen_candidates.py          # auto rules + manual decisions
scripts/05_neiss_filter.py               # filter NEISS TSV by body part 88 + 23 sport codes + age 5-22
scripts/07_harmonize.py                  # combine data/extracted/*.csv → master.csv
scripts/08_validate.py                   # 11 validation checks (C1–C11)
scripts/18_visualize.py                  # baseline figures
scripts/22_neiss_extract_all_years.py    # multi-year NEISS orchestrator
scripts/23_neiss_trends.py               # year-over-year trend report
scripts/24_sport_factsheets.py           # per-sport one-pagers
```

(Plus 14+ numbered extraction scripts for individual sources. Full list in the [scripts directory](https://github.com/Vihaan-Banga/youth-dental-injury-database/tree/main/scripts).)

## How to cite

Until v1.0 release (which will mint a Zenodo DOI):

> Banga, V., [Advisor name]. (2026). Youth Sports Dental Injury Database (Version 0.1-dev) [Data set]. GitHub. https://github.com/Vihaan-Banga/youth-dental-injury-database

A formal `CITATION.cff` is at the repo root — GitHub renders a "Cite this repository" button on the repo home.

## Status

This is a pre-launch, pre-registration-pending database. The methodology is established and validated; advisor sign-off and OSF pre-registration are in progress. Do not cite externally for clinical decision-making until v1.0 release.

## Contact / contributing

- Project lead: **Vihaan Banga**, Olentangy Liberty High School (Powell, OH)
- GitHub: [@Vihaan-Banga](https://github.com/Vihaan-Banga)
- Contributions: see [CONTRIBUTING.md](https://github.com/Vihaan-Banga/youth-dental-injury-database/blob/main/CONTRIBUTING.md) at the repo root
- Issues / suggestions: open an issue on GitHub

## Acknowledgements

This project uses data from the US Consumer Product Safety Commission (NEISS), the National High School Sports-Related Injury Surveillance Study (RIO / NFHS), Rugby Europe, and numerous peer-reviewed primary research studies. Each row in `master.csv` carries a full citation in its `citation` column.

The historical 2013–2017 NEISS coverage was enabled by [@hadley](https://github.com/hadley)'s `neiss` R-package archive.
