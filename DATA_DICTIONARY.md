# Data Dictionary

This document defines every column in the harmonized master dataset (`data/harmonized/master.csv`) and in the per-source extraction files (`data/extracted/<source_id>.csv`).

When adding a new source, follow these definitions exactly. When a definition is ambiguous for a given source, log the decision in `docs/decisions.md`.

---

## Master dataset columns

### Source identification

| Column | Type | Description | Example |
|---|---|---|---|
| `source_id` | string | Unique identifier for the source. Format: `<lastname><year>` or `<surveillance><year>` | `collins2019`, `neiss2022` |
| `citation` | string | Full citation in APA format | "Collins, C. L., et al. (2019). ..." |
| `doi` | string | DOI if available; empty if none | `10.1111/edt.12453` |
| `pub_year` | integer | Publication year | `2019` |
| `study_type` | category | One of: `surveillance`, `cross_sectional`, `cohort`, `case_series`, `registry`, `governing_body_report` | `cross_sectional` |
| `peer_reviewed` | boolean | TRUE if published in a peer-reviewed venue | `TRUE` |

### Population

| Column | Type | Description | Example |
|---|---|---|---|
| `country` | string | ISO 3166-1 alpha-2 code | `US`, `CA`, `BR` |
| `region` | string | Sub-national region if reported | `Ohio`, `Quebec` |
| `population_setting` | category | One of: `school`, `club`, `recreational`, `professional`, `mixed`, `unspecified` | `school` |
| `age_min` | integer | Minimum age in sample (years) | `12` |
| `age_max` | integer | Maximum age in sample (years) | `17` |
| `age_category` | category | One of: `youth` (5–12), `adolescent` (13–17), `collegiate` (18–22), `mixed`, `unspecified`. See PROTOCOL §6.2 for rules when sample spans categories. | `adolescent` |
| `sex` | category | One of: `male`, `female`, `mixed`, `unspecified` | `mixed` |
| `level_of_play` | category | One of: `recreational`, `school_jv`, `school_varsity`, `club`, `elite`, `mixed`, `unspecified` | `school_varsity` |

### Exposure

| Column | Type | Description | Example |
|---|---|---|---|
| `sport_raw` | string | Sport as named in the source | `"American football"` |
| `sport` | category | Standardized sport name per controlled vocabulary (see `docs/decisions.md`) | `football_american` |
| `sport_category` | category | One of: `contact`, `limited_contact`, `non_contact`. See `docs/decisions.md` for assignment rules. | `contact` |
| `sample_size` | integer | Number of individuals in sample | `1245` |
| `athlete_exposures` | integer | Total athlete-exposures (athlete × session) if reported; empty if not | `45000` |
| `season_or_timeframe` | string | Data collection period | `"2018-2019 season"` |

### Outcome

| Column | Type | Description | Example |
|---|---|---|---|
| `injury_count` | integer | Number of dental/orofacial injuries reported | `47` |
| `injury_type_raw` | string | Injury terminology as used in source | `"tooth avulsion"` |
| `injury_category` | category | Standardized per Andreasen classification: `enamel_fracture`, `crown_fracture`, `root_fracture`, `luxation`, `avulsion`, `concussion`, `other_dental`, `orofacial_with_dental`, `unspecified_dental` | `avulsion` |
| `rate_raw` | float | Rate as reported in source | `0.43` |
| `rate_denominator_raw` | string | Original denominator phrasing | `"per 1000 athlete-exposures"` |
| `rate_per_1000_ae` | float | Standardized rate per 1000 athlete-exposures. Empty if source doesn't provide computable data. | `0.43` |

### Protective equipment

| Column | Type | Description | Example |
|---|---|---|---|
| `mouthguard_required` | category | Whether mouthguards were mandated in the studied population: `yes`, `no`, `unspecified` | `yes` |
| `mouthguard_use_rate` | float | Proportion of sample using mouthguards (0–1); empty if not reported | `0.62` |
| `mouthguard_injury_relation` | category | Whether source analyzed mouthguard use vs. injury: `analyzed`, `mentioned_only`, `not_addressed` | `analyzed` |

### Provenance and quality

| Column | Type | Description | Example |
|---|---|---|---|
| `extraction_date` | date | YYYY-MM-DD | `2026-06-15` |
| `extractor` | string | Initials of extractor | `JD` |
| `extraction_notes` | string | Any extraction-time notes; empty if none | "Combined ages 13–14 and 15–17 reported separately; aggregated for this row" |
| `quality_flag` | category | One of: `clean`, `assumption_made`, `partial_data`, `review_needed` | `clean` |

---

## Naming conventions

### `source_id`

- Single-author paper: `lastname<year>` → `collins2019`
- Multi-author paper: `firstauthor_lastname<year>` → `collins2019`
- Multiple sources from same author/year: append letter → `collins2019a`, `collins2019b`
- Surveillance system reports: `<system_abbreviation><year>` → `neiss2022`, `hsrio2021`
- Governing body reports: `<org><year>` → `usahockey2020`

### File naming

- Extracted source: `data/extracted/<source_id>.csv`
- Cleaned source: `data/cleaned/<source_id>_clean.csv`
- Master: `data/harmonized/master.csv`

---

## When a column is empty vs. zero vs. NA

- **Empty cell:** Information not reported in source
- **`0`:** Information reported as zero (e.g., zero injuries in a tracked period)
- **`NA`:** Information not applicable to this row (e.g., `mouthguard_use_rate` for a study where the sport doesn't typically use mouthguards)

Be consistent. The distinction matters for analysis.

---

## Adding new columns

If a useful column is missing, do not just add it to your extraction file. Add it here first with a clear definition and example, log the decision in `docs/decisions.md`, and only then update extractions. The dictionary is the source of truth.
