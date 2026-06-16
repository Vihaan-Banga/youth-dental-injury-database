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
| `age_category` | category | One of: `youth` (5–12), `adolescent` (13–17), `collegiate` (18–22), `adult` (23+ — see "Adult comparator rows" below), `mixed`, `unspecified`. See PROTOCOL §6.2 for rules when sample spans categories. | `adolescent` |
| `extraction_basis` | category | `youth_primary` (row is within the v1.0 inclusion scope of 5–22) or `adult_comparator` (row was extracted alongside the youth data for context — see "Adult comparator rows" below). | `youth_primary` |
| `sex` | category | One of: `male`, `female`, `mixed`, `unspecified` | `mixed` |
| `level_of_play` | category | One of: `recreational`, `school_jv`, `school_varsity`, `club`, `elite`, `mixed`, `unspecified` | `school_varsity` |

### Exposure

| Column | Type | Description | Example |
|---|---|---|---|
| `sport_raw` | string | Sport as named in the source | `"American football"` |
| `sport` | category | Standardized sport name per controlled vocabulary (see `docs/decisions.md`) | `football_american` |
| `sport_category` | category | One of: `contact`, `limited_contact`, `non_contact`. See `docs/decisions.md` for assignment rules. | `contact` |
| `exposure_context` | category | Which activity context the row's data describes: `all` (combined / not stratified), `competition`, `practice`, `training`, `other`. Empty when the row is not exposure-stratified at all (e.g., a one-shot prevalence survey). See "Exposure context and subgroup rows" below. | `competition` |
| `subgroup_label` | string | Short snake_case label for any *within-source* subgroup that isn't already captured by sex / age_category / level_of_play / sport / exposure_context. Used for protective-equipment splits (`mouthguard_users`, `mouthguard_nonusers`), helmet groups, special populations (`with_orthodontic_appliance`), etc. Empty when the row is the source's main/pooled estimate. See "Exposure context and subgroup rows" below. | `mouthguard_users` |
| `sample_size` | integer | Number of individuals in sample | `1245` |
| `athlete_exposures` | integer | Total athlete-exposures (athlete × session) if reported; empty if not | `45000` |
| `season_or_timeframe` | string | Data collection period | `"2018-2019 season"` |

### Outcome

| Column | Type | Description | Example |
|---|---|---|---|
| `injury_count` | integer | Number of dental/orofacial injuries reported | `47` |
| `injury_type_raw` | string | Injury terminology as used in source | `"tooth avulsion"` |
| `injury_category` | category | Standardized per Andreasen classification: `enamel_fracture`, `crown_fracture`, `root_fracture`, `luxation`, `avulsion`, `concussion`, `other_dental`, `orofacial_with_dental`, `unspecified_dental` | `avulsion` |
| `rate_raw` | float | Rate as reported in source (in the source's own denominator) | `0.43` |
| `rate_denominator_raw` | string | Original denominator phrasing — describes **`rate_raw`**, not `rate_per_1000_ae`. | `"per 100,000 athlete-exposures"` |
| `rate_per_1000_ae` | float | Standardized rate per 1000 **athlete-exposures (AE)**. Populated **iff** the source's denominator is an athlete-exposure: athlete-/athletic-exposure, athlete-session (1 athlete in 1 practice or game = 1 AE = 1 session), or a rate already expressed "per … AE". A per-100,000-AE raw rate is stored here already divided by 100 (e.g. `rate_raw` 2.4 per 100k AE → `0.024`). **Leave empty** when the denominator is time (hours, player-match-hours), athlete-seasons, players, population, or percent-of-injuries — those values stay only in `rate_raw` + `rate_denominator_raw`. Enforced by validator check C11. See `docs/decisions.md` 2026-05-24 and 2026-06-13. | `0.024` |

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

## Exposure context and subgroup rows

Sports-injury sources routinely report the same outcome more than once for the same population — broken out by competition vs practice, by mouthguard wearer vs non-wearer, etc. `exposure_context` and `subgroup_label` are how the schema distinguishes those rows from each other (and from accidental duplicates).

**`exposure_context`** — *what activity is the row's count/rate measuring?*

- `all` — combined estimate across activity contexts (competition + practice, or "during the season," etc.). Most rows.
- `competition` — competition / games / matches only.
- `practice` — practice / drills only.
- `training` — strength-and-conditioning / off-season training only (distinguished from `practice` only when the source itself distinguishes them).
- `other` — anything that doesn't fit; explain in `extraction_notes`.
- *(empty)* — row isn't exposure-stratified at all (e.g., a one-shot prevalence survey where the rate isn't tied to an exposure window).

**`subgroup_label`** — *what within-source subgroup is this row?*

Use a short snake_case label, only when the row represents a subgroup that isn't already captured by sex, `age_category`, `level_of_play`, `sport`, or `exposure_context`. Examples:

- `mouthguard_users` / `mouthguard_nonusers`
- `with_helmet` / `without_helmet`
- `with_orthodontic_appliance`
- `varsity_jv_combined` (rare — typically use `level_of_play` instead)

Leave empty when the row is the source's main / pooled estimate. Document the labeling decision in `docs/decisions.md` if you invent a new label.

**Together, `(sport × sex × age_category × level_of_play × extraction_basis × exposure_context × subgroup_label × season_or_timeframe)` is the uniqueness key.** Two rows sharing all those values are duplicates; rows that differ on any one of them are legitimately distinct slices of the source's data.

---

## Adult comparator rows

The v1.0 inclusion criterion (PROTOCOL §3.1) restricts the **source** scope to studies that report data on individuals aged 5–22. Once a source clears that gate, however, many of those sources *also* report stratified adult data (NEISS, ACC NZ insurance claims, NCAA-adjacent surveillance, multi-age cohort studies). Throwing away that adult data would be wasteful.

Rule (decision 2026-05-22, see `docs/decisions.md`):

- A source qualifies for inclusion **iff** it reports some data on individuals aged 5–22 (criterion unchanged).
- When extracting from an included source, all of its age-stratified rows are extracted — including adult bands when reported alongside youth.
- Adult rows are tagged `age_category = adult` and `extraction_basis = adult_comparator`.
- Youth rows (5–22) are tagged with the appropriate youth/adolescent/collegiate/mixed value and `extraction_basis = youth_primary`.
- Analyses can subset by `extraction_basis = 'youth_primary'` to get a v1.0-scope view (the headline result), or include adult rows for comparator context.

This avoids re-scoping the project (the headline remains youth-focused) while preserving information that's already in front of us at extraction time.

---

## When a column is empty vs. zero vs. NA

- **Empty cell:** Information not reported in source
- **`0`:** Information reported as zero (e.g., zero injuries in a tracked period)
- **`NA`:** Information not applicable to this row (e.g., `mouthguard_use_rate` for a study where the sport doesn't typically use mouthguards)

Be consistent. The distinction matters for analysis.

---

## Adding new columns

If a useful column is missing, do not just add it to your extraction file. Add it here first with a clear definition and example, log the decision in `docs/decisions.md`, and only then update extractions. The dictionary is the source of truth.
