# Youth Sports Dental Injury Database

**A free, open collection of published statistics on dental and mouth injuries in young athletes — gathered from 103 research studies and national injury-surveillance reports and organized into one consistent, searchable dataset.**

- 🔍 **[Explore the data in your browser](https://vihaan-banga.github.io/youth-dental-injury-database/rate-explorer.html)** — filter by sport and age group; no download or login
- 📥 **[Download the full dataset (CSV — opens in Excel or Google Sheets)](https://raw.githubusercontent.com/Vihaan-Banga/youth-dental-injury-database/main/data/harmonized/master.csv)**
- 🌐 **[Project website](https://vihaan-banga.github.io/youth-dental-injury-database/)** · 📖 **[What each column means](DATA_DICTIONARY.md)**

> [!IMPORTANT]
> **Read before using the data**
> - **These are published findings, not patient cases.** Each of the 421 entries is a statistic reported by a study or surveillance system — for example, *"459 dental injuries across nearly 50 million athlete-exposures."* Entries should not be added together or counted as individual injuries.
> - **The data are mostly from the United States.** 28 countries are represented, but US sources contribute about **72%** of entries. Findings may not apply to other countries.
> - **Most entries don't say what kind of dental injury occurred.** **84%** of entries report only "dental injury," without separating avulsion, fracture, or luxation (87% of sources never specify the type).
> - **Numbers are not yet fully verified.** Every entry is currently flagged as not fully verified. Entries were extracted by one reviewer with AI assistance; values have been checked for internal consistency and, where possible, against each study's abstract, but verification against the full-text articles is still in progress.
> - **Entries are not all directly comparable.** Studies measure injuries differently — per athlete-exposure, per season, as a percentage of athletes, or as emergency-department visits. Compare only entries that use the same measure (each entry is labeled).
> - **Not for individual clinical decisions.** This summarizes population-level research and cannot predict any individual patient's risk.

## What's in it

| | |
|---|---|
| **Entries** | 421 published findings |
| **Sources** | 103 — 90 peer-reviewed studies, 12 years of US emergency-department surveillance (NEISS), and 1 sport governing-body report |
| **Ages** | Focus on ages 5–22 (some studies also report wider age ranges; these are labeled) |
| **Countries** | 28 (US-weighted — see above) |
| **Publication years** | 2000–2026 |
| **US emergency-department data** | NEISS, 2013–2019 and 2021–2025 (~8,200 sampled emergency-department records); 2020 not yet included |
| **Sports** | 30 specific sports; the most-studied are basketball, rugby, soccer, ice hockey, and baseball |
| **Mouthguard information** | Mouthguard use is reported for 41 entries |
| **License** | Free to use and share with attribution ([CC BY 4.0](LICENSE-DATA)) |

## What it can — and can't — help answer

**Good for:**
- How often high school athletes sustain dental injuries in a given sport (e.g., basketball: 2.4 per 100,000 athlete-exposures in US high school surveillance)
- Whether injured athletes were wearing mouthguards, where studies report it
- What published studies found about mouthguard effectiveness in specific sports
- Which sports, ages, and countries are well studied — and where the evidence gaps are

**Not designed for:**
- The mix of injury types (avulsion vs. fracture vs. luxation) — most sources don't report it
- Treatment details such as storage medium, time to treatment, or tooth survival — these are not recorded
- Estimating an individual patient's risk

## How it was built

Sources were identified through systematic PubMed searches, targeted journal searches, US Consumer Product Safety Commission (NEISS) data, and sport governing-body reports, then screened against a written [research protocol](PROTOCOL.md): ages 5–22, sport-related, dental or orofacial injury, published 2000 or later. Each finding was extracted into a standard format with its full source citation, and every data decision is logged in [`docs/decisions.md`](docs/decisions.md).

Automated checks run on every update to catch formatting errors and internal inconsistencies. These checks confirm the data are well-formed — **not** that every number matches its original source (see "Read before using" above).

## Status and how to cite

**Pre-release (version 0.1).** You're welcome to explore the data and use it to find and read the underlying research. Until the formal v1.0 release, please cite the **original studies** — every entry includes its full source citation — rather than database-wide totals.

To reference the database itself:

> Banga V. (2026). *Youth Sports Dental Injury Database* (Version 0.1, pre-release) [Data set]. GitHub. https://github.com/Vihaan-Banga/youth-dental-injury-database

GitHub's **"Cite this repository"** button (right sidebar) provides this in other formats.

## About and contact

Created and maintained by **Vihaan Banga**, Olentangy Liberty High School (Powell, Ohio).

Questions, corrections, or suggestions: email **vihaansbanga@gmail.com** or open an [issue on GitHub](https://github.com/Vihaan-Banga/youth-dental-injury-database/issues). If you spot an error in an entry, please include the source and the value you believe is correct — corrections are logged publicly.

---

## For researchers and developers

### Files

| File | What it is |
|---|---|
| [`data/harmonized/master.csv`](data/harmonized/master.csv) | The full dataset (421 rows × 40 columns) |
| [`data/harmonized/master.sqlite`](data/harmonized/master.sqlite) | The same data as a SQLite database |
| [`datapackage.json`](datapackage.json) | Machine-readable dataset description ([Frictionless Data](https://frictionlessdata.io/) standard) |
| [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) | Definition of every column |
| [`PROTOCOL.md`](PROTOCOL.md) | Research protocol: inclusion criteria, search strategy, harmonization rules |
| [`docs/sources.md`](docs/sources.md) | Every candidate source and its screening decision |
| [`docs/decisions.md`](docs/decisions.md) | Log of every data decision and the reason for it |
| [`outputs/data_quality.md`](outputs/data_quality.md) | Data-quality report: verification tiers and flagged entries |
| [`data/extracted/`](data/extracted/) | One file per source, before combining |

### Comparing entries correctly

Each row carries a `measure_type` and a `comparability_group`. **Values are directly comparable only within the same `comparability_group`**; for per-athlete-exposure rates, use the normalized `rate_per_1000_ae`. NEISS figures count emergency-department-treated injuries only and undercount injuries treated in dental offices. Aggregate rows (`all_sports_aggregate`, etc.) should not be pooled with sport-specific rows. `dental_specific = FALSE` marks entries whose rate covers all injuries rather than dental injuries specifically. Every row is currently `quality_flag = partial_data`.

### Reproduce the database

The entire dataset rebuilds from the committed per-source extraction files — deterministically and offline — with one command:

```bash
python3 scripts/run_all.py            # rebuild master.csv, validate, regenerate all outputs
python3 scripts/run_all.py --core     # just harmonize + validate (Python standard library only)
python3 scripts/run_all.py --check    # fail if a fresh build changes master.csv
```

The core pipeline (`07_harmonize.py` → `08_validate.py`) needs only the Python standard library and runs 14 automated checks (C1–C14). Figures need `matplotlib` (`pip install -r requirements.txt`). The source-extraction scripts (`00`–`06`, `09`–`32`) query PubMed, Unpaywall, and NEISS; they document how the extraction files were produced and are not part of the offline rebuild. Continuous integration re-runs `run_all.py --core --check` on every push.

To contribute a source or correction, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

### License

- **Data:** Creative Commons Attribution 4.0 International (CC BY 4.0) — see [`LICENSE-DATA`](LICENSE-DATA)
- **Code:** MIT — see [`LICENSE`](LICENSE)
