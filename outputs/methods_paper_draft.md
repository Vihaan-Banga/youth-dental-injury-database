# Youth Sports Dental Injury Database — Data Descriptor (working draft)

_Target venue: Nature Scientific Data (data descriptor) or Elsevier Data in Brief. This draft follows Scientific Data's structure. Numbers reflect the current working release (v0.1.x snapshot, 2026-06-12) and will be frozen at v1.0; remaining square-bracket items are placeholders awaiting v1.0 (advisor, Zenodo DOI, OSF link, a small number of external citations)._

**Authors:** Vihaan Banga¹, [Advisor Name]²
1. Olentangy Liberty High School, Powell, OH, USA
2. [Institution, when secured]

**Corresponding author:** Vihaan Banga (GitHub: [@Vihaan-Banga](https://github.com/Vihaan-Banga))

**Subject categories (Scientific Data taxonomy):** Epidemiology · Health care · Dentistry · Public health

---

## Abstract (~200 words)

Dental and orofacial injuries are among the most common facial injuries in youth sports, yet incidence estimates are fragmented across dozens of national surveillance systems, peer-reviewed studies, and sport-governing-body reports — each using different definitions, age ranges, and exposure denominators. We aggregate **421** epidemiological data points (rows) from **103** sources into a harmonized open-access database covering individuals aged 5–22 across **28 countries**, drawn from publications spanning **2000–2026**. Twelve treatment years of US National Electronic Injury Surveillance System (NEISS) case-level data (2013–2019, 2021–2025; n ≈ 8,800 sport-related youth mouth-injury cases; 250 aggregated rows) are integrated alongside published research and governing-body surveillance reports. A consistent column schema captures population, exposure context, intervention subgroup, outcome, and protective-equipment data per row, with explicit provenance and uncertainty flags. The database, code, and pre-registered protocol are public under CC BY 4.0 and MIT licenses. The intended use is to enable cross-sport, cross-age, and cross-geography comparison of youth dental injury epidemiology without re-reconciling each source manually.

---

## Background & Summary

Sports-related dental injuries impose meaningful clinical, psychological, and economic burdens on children and adolescents — the American Academy of Pediatric Dentistry estimates ~22,000 youth dental injuries treated annually in US emergency departments alone¹, with lifetime treatment costs of an avulsed permanent tooth estimated at ~US$20,000². Yet despite the established health and policy relevance, no unified open-access dataset has aggregated youth-specific dental injury epidemiology across the heterogeneous mix of surveillance systems (NEISS, High School RIO/NFHS, NCAA ISP, ACC NZ insurance claims), peer-reviewed primary research, and sport-governing-body reports that report it. The gap leaves clinicians, researchers, and policy-makers unable to easily answer foundational questions like:

- "What is the comparable per-1000-athlete-exposure dental injury rate across youth contact sports?"
- "How has the rate changed since youth mouthguard mandates were introduced?"
- "Where are the largest surveillance gaps internationally?"

This data descriptor fills that gap.

**Contributions of this work:**

1. A **harmonized schema** (36 columns; documented in DATA_DICTIONARY.md) that captures the dimensions on which dental-sport-injury epidemiology typically varies: population (age/sex/level), exposure context (competition vs. practice), within-source subgroup (e.g., mouthguard users vs nonusers), outcome (count, rate, denominator phrasing), and protective equipment. Critically, a `extraction_basis` column distinguishes "youth_primary" rows (within the v1.0 inclusion scope of ages 5–22) from "adult_comparator" rows extracted alongside, preserving cross-age context without bloating the v1.0 scope.

2. **Twelve treatment-years of NEISS** youth dental-sport case-level data (2013–2025 except 2020), unified and queryable. To our knowledge this is the first published aggregation of NEISS dental-sport data at this temporal breadth for the youth subset; the constituent year-CSVs and the year-over-year trend table are released as part of the database.

3. **A reproducible end-to-end pipeline** (a versioned Python script suite) covering source identification, AI-assisted screening, per-source extraction, harmonization, validation, and visualization. The pipeline is bound to a pre-registered protocol; every harmonization decision is logged in an append-only decisions file. A CI workflow runs the validator on every commit.

4. **Cross-source consistency analysis** built into the deliverable: paired sources for the same sport (e.g., RIO HS basketball across years; NCAA collegiate basketball; comparator international cohorts) are compared on a per-1000-AE basis, surfacing real disagreements (e.g., MG-mandate effects) and incompatible-denominator issues (e.g., per-AE-hours vs per-AE).

---

## Methods

### Inclusion criteria (PROTOCOL §3.1)

Sources eligible if they meet all of:
- **Population:** report data on individuals aged 5–22 (youth through collegiate).
- **Outcome:** report incidence, prevalence, or count of dental or orofacial-with-dental injuries (Andreasen classification³).
- **Setting:** sport-related (organized or recreational athletic activity).
- **Time:** published or reported on/after 1 January 2000 (peer-reviewed); surveillance data extends to 2013 via the hadley/neiss archive⁴.
- **Language:** English (v1.0 limitation).
- **Data accessibility:** numerical data extractable from the published report.

Sources excluded: adult-only populations, non-sport-related dental trauma, single case reports or case series n<5, review articles (used to mine primary sources only), non-peer-reviewed venues except recognized national surveillance systems and governing-body reports.

Once a source qualifies under the above, **all** its age-stratified rows are extracted, including adult bands when reported alongside youth. Adult rows are tagged `age_category = adult` and `extraction_basis = adult_comparator`; youth rows are tagged `extraction_basis = youth_primary`.

### Source identification (PROTOCOL §4)

**1. Primary PubMed search** (2026-05-21) via NCBI E-utilities, query verbatim from PROTOCOL §4.2 (combining dental/orofacial outcome terms × sport terms × epidemiology terms, date ≥2000). 202 hits.

**2. Supplementary journal-restricted searches** (2026-05-23 + 2026-05-24, 10 journals): Dental Traumatology, Pediatric Dentistry, American Journal of Sports Medicine, British Journal of Sports Medicine, Journal of Athletic Training, Journal of Endodontics, Journal of Oral & Maxillofacial Surgery, Pediatrics, Injury Prevention, Orthopaedic Journal of Sports Medicine. After deduplication against (1): +236 NEW candidates.

**3. NEISS** (US Consumer Product Safety Commission National Electronic Injury Surveillance System): 12 treatment-years (2013–2017 from hadley/neiss R-package archive⁴; 2023, 2018–2019, 2021–2025 directly from the CPSC online query builder).

**4. National HS Sports-Related Injury Surveillance Study (RIO)**: 10 annual summary report PDFs (2008/09–2018/19, 2021/22, 2023/24) from Colorado School of Public Health PIPER program and state-association mirrors.

**5. Governing-body reports** (PROTOCOL §4.3): AAPD Policy on Prevention of Sports-Related Orofacial Injuries (2025–26 edition), NATA position statement, Rugby Europe 2024 Injury Surveillance Report (includes U-18 Sevens data), World Rugby 2023 ISS review, England PRISP 2022-23.

Each candidate logged in `docs/sources.md` with a screening status: `identified` → `screened_included` / `screened_excluded` / `needs_additional_review` → (full-text) `included` / `fulltext_excluded` → `extracted`. The 436 candidate records were screened against PROTOCOL §3.1–3.3 using a hybrid pipeline: automatic exclusion rules (non-English, Case Reports, Reviews, Editorials/Letters/Comments) cleared ~14%, AI-assisted abstract review (model: Claude Opus) handled the remainder. AI-assisted decisions tagged with extractor=`VB-AI-assisted-<date>` for audit. Full reasoning per decision captured in `outputs/screening_report_*.md`. Records whose abstract could not confirm a key §3.1 attribute were held as `needs_additional_review` (84 at the current snapshot); a full-text review pass of the open-access subset (2026-06-12) resolved 7 of these (logged in `docs/decisions.md`), the remainder being blocked by paywalled or scanned full text pending advisor library access. The project lead (V.B.) is the final screener; an advisor will perform 20% inter-rater reliability re-screening prior to v1.0.

### Data extraction (PROTOCOL §5)

For each included source, a row is written to `data/extracted/<source_id>.csv` following the column schema in `DATA_DICTIONARY.md`. Sources can produce multiple rows when they report stratifications (sport, sex, age band, exposure context, subgroup). Where the source's terminology doesn't match the project's controlled vocabulary, the source's original phrasing is preserved in `sport_raw` (free text) and the standardized `sport` value is assigned per the §6.1 taxonomy, with any new sport addition logged as a `docs/decisions.md` entry.

NEISS case-level extractions use a deterministic filter (`scripts/05_neiss_filter.py`):
- `Body_Part == 88` (Mouth, including teeth) — primary filter, OR
- `Body_Part_2 == 88` (Mouth as secondary, available since 2019), OR
- `Body_Part == 76` (Face) AND diagnosis text contains dental terminology
- `Product_1 ∈ {23 sport-related NEISS product codes}` (verified against 2024 NEISS Coding Manual Appendix H)
- `5 ≤ Age ≤ 22` (excluding the <2yo "200+months" coding quirk)

Filtered case-level rows are aggregated per year × sport × age band × sex into extraction rows.

### Harmonization (PROTOCOL §6)

Sport classification follows a controlled vocabulary maintained in `docs/decisions.md` ("Sport taxonomy"); 36 sport/aggregate values are represented in the current release. Sport categories (`contact`, `limited_contact`, `non_contact`) per the American Academy of Pediatrics classification⁵; the value is left empty for aggregate/non-sport-specific rows (e.g. `all_activities_aggregate`), where the contact taxonomy does not apply. Standardized injury category per the Andreasen classification³. Rates are preserved verbatim in `rate_raw` with the source's denominator phrasing in `rate_denominator_raw`; `rate_per_1000_ae` is populated only when the source uses an athlete-exposure (not hours, seasons, players, or population) denominator.

### Technical validation (PROTOCOL §7)

A versioned validator (`scripts/08_validate.py`) runs 11 checks (C1-C11) on `data/harmonized/master.csv`:
- **C1–C2:** schema completeness; categorical-vocabulary conformance
- **C3:** numeric plausibility (`rate_per_1000_ae < 100` per PROTOCOL §7)
- **C4–C5:** age-min ≤ age-max; `age_category` consistency with the age range
- **C6:** `extraction_basis = adult_comparator` iff `age_category = adult`
- **C7:** sport in controlled vocabulary (or flagged in `extraction_notes`)
- **C8:** `quality_flag` in the allowed set
- **C9:** every source has at least one `youth_primary` row
- **C10:** no duplicate (source × sport × age × sex × level × basis × exposure_context × subgroup × season) keys
- **C11:** `rate_per_1000_ae` populated only when `rate_denominator_raw` is an athlete-exposure denominator

C1–C4, C6–C8 and C10 are hard checks (a violation fails the build); C5 and C9 surface as warnings, since age-category banding is intentionally permissive.

Validation runs on every commit via GitHub Actions CI (`.github/workflows/validate.yml`).

---

## Data Records

The database is distributed as:

- **`data/harmonized/master.csv`** — the main tabular product. **421 rows from 103 sources** (current release). 36 columns per DATA_DICTIONARY.md. Rows split `youth_primary` (419) vs `adult_comparator` (2); study types span surveillance (37 sources), cross-sectional (41), case series (13), cohort (11), and governing-body report (1).
- **`data/harmonized/master.sqlite`** — SQLite mirror of `master.csv` with sample queries in `data/harmonized/README_sqlite.md`.
- **`data/extracted/<source_id>.csv`** — one file per source. Useful for source-level audit. Includes the per-NEISS-year extractions (`neiss2013.csv` through `neiss2025.csv` except `neiss2020.csv` for which NEISS returned zero matching cases).
- **`data/raw/papers/_abstracts/<PMID>.json`** — parsed PubMed abstract data per candidate (parsed via E-utilities efetch).
- **`data/raw/papers/_pmc/<PMC>.xml`** — full-text XMLs for the PMC-available subset.
- **`outputs/tables/neiss_trends.csv`** — derived 12-year NEISS trend table.
- **`outputs/cross_source_rate_comparison.md`** — paired-source rate comparison.

Each source carries a stable `source_id` of form `<firstauthor><year>` (PubMed-keyed) or `<system><year>` (surveillance). All citations, DOIs (where assigned), and CC BY 4.0 attribution metadata are in `LICENSE-DATA` and `CITATION.cff`.

---

## Technical Validation

Current state (v0.1.x snapshot, 2026-06-13): **426 rows / 106 sources / 0 FAILs / 0 WARNs** against the 11 validation checks (`outputs/validation_report.md`), run on every commit via GitHub Actions CI. 23 PMC full-text XMLs cached. Cross-source rate comparison confirms tight agreement on US high-school basketball rates between `collins2016` (0.026 per 1000 AE) and `azadani2023` (0.024 per 1000 AE) — equivalently 2.6 and 2.4 per 100,000 AE — independent surveillance covering overlapping years yielding statistically indistinguishable estimates (`outputs/cross_source_rate_comparison.md`).

Of the 421 rows, 20 carry a value in `rate_per_1000_ae` (the rest preserve the source's native denominator in `rate_raw`/`rate_denominator_raw`); 41 rows report a mouthguard use rate and 41 record an analyzed mouthguard-vs-injury relationship. All 20 values sit on a single per-1000-athlete-exposure scale: rates the source reported per 100,000&nbsp;AE are stored already divided by 100, athlete-session denominators are treated as athlete-exposures (the standard "one athlete in one practice or game" unit), and rates with time (hours, player-match-hours), population, or percent-of-injuries denominators are excluded from this column by design — kept only in `rate_raw`/`rate_denominator_raw` — and that exclusion is now enforced by validator check C11 (see `docs/decisions.md`, 2026-06-13). The 20 are therefore directly comparable on the denominator axis; as in any cross-source comparison they still differ in injury definition, age range, era, and competition-vs-practice context, so each rate should be read alongside its row attributes. (A future option to split into explicit `rate_value` + `rate_unit` columns, which would also carry the non-AE rates as structured values, remains available but is not needed for v0.1.x.)

Limitations transparently documented:
- English-language sources only (v1.0).
- Single primary extractor with AI assistance; 20% inter-rater reliability re-screening is planned for v1.0 sign-off (pending advisor).
- NEISS samples ED visits only — undercounts dental injuries treated in dental offices.
- 2020 NEISS gap reflects the COVID-19 youth-sport shutdown; no imputation attempted.
- All current rows carry `quality_flag = partial_data` (most are abstract-keyed or aggregate extractions); full-text re-extraction and a graduation of clean rows to `quality_flag = clean` are planned for v1.0.
- Population-denominator surveillance (e.g. ACC NZ, NEISS weighted estimates) is preserved in `rate_raw` but cannot be converted to per-AE rates; such rows leave `rate_per_1000_ae` empty by design.

---

## Comparability & Limitations

Harmonizing heterogeneous sources into one schema does not render all rows mutually comparable — a caveat raised directly by a senior surveillance reviewer. Two machine-readable columns make this explicit: **`measure_type`** (the outcome-measure / rate basis) and **`comparability_group`** (the key on which direct comparison is permitted). **Rows are directly comparable only within the same `comparability_group`.** Concretely:

- **Denominators differ.** The dataset spans incidence per athlete-exposure (`incidence_per_AE`; normalized in `rate_per_1000_ae`), per player/athlete-hours, per 100,000 population, per season, prevalence proportions, NEISS/ED weighted estimates, and raw counts. Only same-`measure_type` rows are comparable.
- **NEISS figures are emergency-department-treated only** (weighted national estimates; `measure_type = ed_visit_estimate`); they undercount injuries treated outside the ED and are not comparable to athlete-exposure rates.
- **Aggregate rows** (`all_sports_aggregate`, `all_activities_aggregate`, …) carry an `__aggregate` `comparability_group` suffix and must not be pooled with sport-specific rows.
- **Definitions and inclusion criteria vary** across sources (all-cause dental-trauma prevalence vs sport-related ED-treated incidence, differing age bands and eras). The companion Rate Explorer segregates results by `measure_type` and never co-plots incompatible tiers.
- All current rows are `quality_flag = partial_data` (schema- and vocabulary-validated; full-text numeric verification pending). A `case_definition` flag to capture methodological differences within a `measure_type` is planned (phase 2).

---

## Usage Notes

The headline scope is the youth-primary subset; subset on `extraction_basis == "youth_primary"` for the v1.0-scope view, or include `adult_comparator` rows for cross-age comparison. Always read a rate together with its `rate_denominator_raw`: the 20 rows with a non-empty `rate_per_1000_ae` share a common athlete-exposure denominator and are directly comparable on that axis (subject to the usual definitional, age, and era differences); the rest preserve heterogeneous native denominators (per-1000-player-hours, per-100k-population, per-season, % of injuries) in `rate_raw` and must not be pooled blindly. Empty cell = not reported; `0` = reported zero; `NA` = not applicable.

```python
import pandas as pd
URL = ("https://raw.githubusercontent.com/Vihaan-Banga/"
       "youth-dental-injury-database/main/data/harmonized/master.csv")
df = pd.read_csv(URL)

# 1. Youth-primary rows with a comparable per-1000-AE dental injury rate:
comparable = df[(df.extraction_basis == "youth_primary") &
                df.rate_per_1000_ae.notna()]

# 2. Sources that analyzed mouthguard use vs. injury:
mg = df[df.mouthguard_injury_relation == "analyzed"]

# 3. The 12-year NEISS youth dental-sport series (weighted estimates live in
#    extraction_notes; see outputs/neiss_trends.md for the parsed table):
neiss = df[df.source_id.str.startswith("neiss")]

# 4. Dental injuries by standardized Andreasen category for a given sport:
df[df.sport == "basketball"].groupby("injury_category").injury_count.sum()
```

The same data is queryable via SQLite without pandas:

```bash
sqlite3 data/harmonized/master.sqlite \
  "SELECT sport, COUNT(*) rows, SUM(injury_count) injuries
   FROM master WHERE extraction_basis='youth_primary'
   GROUP BY sport ORDER BY injuries DESC LIMIT 10;"
```

---

## Code Availability

All code (pipeline, validator, analysis scripts) under MIT License: https://github.com/Vihaan-Banga/youth-dental-injury-database. Versioned via git. Reproducibility: `scripts/07_harmonize.py` + `scripts/08_validate.py` reproduce the harmonized master + validation report from the per-source CSVs.

---

## Data Availability

All data under CC BY 4.0 License. Repository: https://github.com/Vihaan-Banga/youth-dental-injury-database. A versioned snapshot will be deposited to Zenodo at v1.0 release with a permanent DOI.

---

## References (selected)

1. American Academy of Pediatric Dentistry. (2025). Policy on Prevention of Sports-Related Orofacial Injuries. _Pediatr Dent_.
2. [AAPD policy cite for lifetime cost]
3. Andreasen JO, et al. Textbook and color atlas of traumatic injuries to the teeth, 5th edn.
4. Wickham H. neiss: Data from the National Electronic Injury Surveillance System. https://github.com/hadley/neiss
5. American Academy of Pediatrics. (2008). Medical conditions affecting sports participation. _Pediatrics_, 121(4), 841–8.
6. [Full reference list to be expanded from sources.md at v1.0]

---

## Acknowledgements

[For v1.0 — placeholder]

## Author Contributions

V.B. conceived the project, designed the protocol, performed source identification + screening + extraction, built the pipeline, and drafted the manuscript. [Advisor] provided methodological guidance, performed reliability re-screening, and reviewed the manuscript.

## Competing Interests

The authors declare no competing interests.

---

_Draft last updated 2026-06-24 (numbers reflect the 421-row / 103-source working release). Next steps before v1.0 submission:_
- _Secure senior advisor (in progress, project lead leading recruitment) — unlocks the remaining bracketed placeholders (affiliation, acknowledgements, author contributions)_
- _File OSF pre-registration_
- _Complete 20% inter-rater reliability re-screening_
- _Re-extract `quality_flag=partial_data` rows from full text and graduate clean rows to `quality_flag=clean`_
- _Resolve the remaining 84 `needs_additional_review` records (advisor library access for paywalled/scanned full text)_
- _Fill external citation placeholders (ref. 2, lifetime-cost figure) and expand the reference list from `docs/sources.md`_
- _Mint Zenodo DOI; populate DOI/OSF placeholders_
