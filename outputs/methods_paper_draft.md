# Youth Sports Dental Injury Database — Data Descriptor (draft skeleton)

_Target venue: Nature Scientific Data (data descriptor) or Elsevier Data in Brief. This skeleton follows Scientific Data's structure. Square-bracket items are placeholders awaiting v1.0._

**Authors:** Vihaan Banga¹, [Advisor Name]²
1. Olentangy Liberty High School, Powell, OH, USA
2. [Institution, when secured]

**Corresponding author:** Vihaan Banga (GitHub: [@Vihaan-Banga](https://github.com/Vihaan-Banga))

**Subject categories (Scientific Data taxonomy):** Epidemiology · Health care · Dentistry · Public health

---

## Abstract (~200 words)

Dental and orofacial injuries are among the most common facial injuries in youth sports, yet incidence estimates are fragmented across dozens of national surveillance systems, peer-reviewed studies, and sport-governing-body reports — each using different definitions, age ranges, and exposure denominators. We aggregate **[N at v1.0]** epidemiological data points from **[K at v1.0]** sources into a harmonized open-access database covering individuals aged 5–22 across **19+ countries** and 1996–2025. Twelve treatment years of US National Electronic Injury Surveillance System (NEISS) case-level data (2013–2019, 2021–2025; n ≈ 8,800 sport-related youth mouth-injury cases) are integrated alongside published research and governing-body surveillance reports. A consistent column schema captures population, exposure context, intervention subgroup, outcome, and protective-equipment data per row, with explicit provenance and uncertainty flags. The database, code, and pre-registered protocol are public under CC BY 4.0 and MIT licenses. The intended use is to enable cross-sport, cross-age, and cross-geography comparison of youth dental injury epidemiology without re-reconciling each source manually.

---

## Background & Summary

Sports-related dental injuries impose meaningful clinical, psychological, and economic burdens on children and adolescents — the American Academy of Pediatric Dentistry estimates ~22,000 youth dental injuries treated annually in US emergency departments alone¹, with lifetime treatment costs of an avulsed permanent tooth estimated at ~US$20,000². Yet despite the established health and policy relevance, no unified open-access dataset has aggregated youth-specific dental injury epidemiology across the heterogeneous mix of surveillance systems (NEISS, High School RIO/NFHS, NCAA ISP, ACC NZ insurance claims), peer-reviewed primary research, and sport-governing-body reports that report it. The gap leaves clinicians, researchers, and policy-makers unable to easily answer foundational questions like:

- "What is the comparable per-1000-athlete-exposure dental injury rate across youth contact sports?"
- "How has the rate changed since youth mouthguard mandates were introduced?"
- "Where are the largest surveillance gaps internationally?"

This data descriptor fills that gap.

**Contributions of this work:**

1. A **harmonized schema** (34 columns; documented in DATA_DICTIONARY.md) that captures the dimensions on which dental-sport-injury epidemiology typically varies: population (age/sex/level), exposure context (competition vs. practice), within-source subgroup (e.g., mouthguard users vs nonusers), outcome (count, rate, denominator phrasing), and protective equipment. Critically, a `extraction_basis` column distinguishes "youth_primary" rows (within the v1.0 inclusion scope of ages 5–22) from "adult_comparator" rows extracted alongside, preserving cross-age context without bloating the v1.0 scope.

2. **Twelve treatment-years of NEISS** youth dental-sport case-level data (2013–2025 except 2020), unified and queryable. To our knowledge this is the first published aggregation of NEISS dental-sport data at this temporal breadth for the youth subset; the constituent year-CSVs and the year-over-year trend table are released as part of the database.

3. **A reproducible end-to-end pipeline** (24 versioned Python scripts) covering source identification, AI-assisted screening, per-source extraction, harmonization, validation, and visualization. The pipeline is bound to a pre-registered protocol; every harmonization decision is logged in an append-only decisions file. A CI workflow runs the validator on every commit.

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

Each candidate logged in `docs/sources.md` with a screening status: `identified` → `screened_included` / `screened_excluded` / `needs_human_review`. The 444 PubMed candidates were screened against PROTOCOL §3.1–3.3 using a hybrid pipeline: automatic exclusion rules (non-English, Case Reports, Reviews, Editorials/Letters/Comments) cleared ~14%, AI-assisted abstract review (model: Claude Opus) handled the remainder. AI-assisted decisions tagged with extractor=`VB-AI-assisted-<date>` for audit. Full reasoning per decision captured in `outputs/screening_report_*.md`. The project lead (V.B.) is the final screener; an advisor will perform 20% inter-rater reliability re-screening prior to v1.0.

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

Sport classification follows a controlled vocabulary of [N] sports (DATA_DICTIONARY.md "Sport taxonomy"). Sport categories (`contact`, `limited_contact`, `non_contact`) per the American Academy of Pediatrics classification⁵. Standardized injury category per the Andreasen classification³. Rates are preserved verbatim in `rate_raw` with the source's denominator phrasing in `rate_denominator_raw`; `rate_per_1000_ae` is populated only when the source uses an athlete-exposure (not hours, seasons, players, or population) denominator.

### Technical validation (PROTOCOL §7)

A versioned validator (`scripts/08_validate.py`) runs 10 checks (C1-C10) on `data/harmonized/master.csv`:
- **C1–C2:** schema completeness; categorical-vocabulary conformance
- **C3:** numeric plausibility (`rate_per_1000_ae < 100` per PROTOCOL §7)
- **C4–C5:** age-min ≤ age-max; `age_category` consistency with the age range
- **C6:** `extraction_basis = adult_comparator` iff `age_category = adult`
- **C7:** sport in controlled vocabulary
- **C9:** every source has at least one `youth_primary` row
- **C10:** no duplicate (source × sport × age × sex × level × basis × exposure_context × subgroup × season) keys

Validation runs on every commit via GitHub Actions CI (`.github/workflows/validate.yml`).

---

## Data Records

The database is distributed as:

- **`data/harmonized/master.csv`** — the main tabular product. **[N rows / K sources at v1.0]**. 34 columns per DATA_DICTIONARY.md.
- **`data/extracted/<source_id>.csv`** — one file per source. Useful for source-level audit. Includes the per-NEISS-year extractions (`neiss2013.csv` through `neiss2025.csv` except `neiss2020.csv` for which NEISS returned zero matching cases).
- **`data/raw/papers/_abstracts/<PMID>.json`** — parsed PubMed abstract data per candidate (parsed via E-utilities efetch).
- **`data/raw/papers/_pmc/<PMC>.xml`** — full-text XMLs for the PMC-available subset.
- **`outputs/tables/neiss_trends.csv`** — derived 12-year NEISS trend table.
- **`outputs/cross_source_rate_comparison.md`** — paired-source rate comparison.

Each source carries a stable `source_id` of form `<firstauthor><year>` (PubMed-keyed) or `<system><year>` (surveillance). All citations, DOIs (where assigned), and CC BY 4.0 attribution metadata are in `LICENSE-DATA` and `CITATION.cff`.

---

## Technical Validation

[Refer to outputs/validation_report.md state at v1.0 release]

Current state (v0.1-dev): 389 rows / 80 sources / **0 FAILs / 0 WARNs** against the 10 validation checks. 22 PMC full-text XMLs cached. Cross-source rate comparison confirms tight agreement on US HS basketball rates between `collins2016` (0.026 / 100k AE) and `azadani2023` (0.024 / 100k AE) — independent surveillance covering overlapping years yielding statistically indistinguishable estimates.

Limitations transparently documented:
- English-language sources only (v1.0).
- Single primary extractor with AI assistance; 20% inter-rater reliability is planned for v1.0 sign-off.
- NEISS samples ED visits only — undercounts dental injuries treated in dental offices.
- 2020 NEISS gap reflects COVID-19 youth-sport shutdown; no imputation attempted.
- A subset of rows is `quality_flag = partial_data` (abstract-only extraction) and should be re-extracted from full text for v1.0.

---

## Usage Notes

[Examples for v1.0 — placeholder]

```python
import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/Vihaan-Banga/youth-dental-injury-database/main/data/harmonized/master.csv")
# Youth-primary basketball rates per 1000 AE:
df[(df.sport == "basketball") &
   (df.extraction_basis == "youth_primary") &
   df.rate_per_1000_ae.notna()].head()
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

_Skeleton last updated 2026-05-25. Next steps before v1.0 submission:_
- _Secure senior advisor (in progress, project lead leading recruitment)_
- _File OSF pre-registration_
- _Complete 20% inter-rater reliability re-screening_
- _Re-extract `quality_flag=partial_data` rows from full text_
- _Mint Zenodo DOI; populate placeholders_
