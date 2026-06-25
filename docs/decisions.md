# Harmonization Decisions Log

Every non-mechanical decision about how to classify, harmonize, or handle ambiguous data goes here, with date and reasoning.

**Why this exists:** A reviewer (advisor, journal reviewer, future Claude session, future you) will eventually ask "why did you classify X this way?" The answer must exist somewhere in writing. This is that place.

**Format:** Append-only. Never delete entries. If a decision is revised, add a new entry referencing the old one and update affected data.

---

## Decision template

```
### YYYY-MM-DD: Short title of decision

**Trigger:** What source or situation prompted this decision?

**Question:** What was the ambiguity?

**Options considered:** What were the alternatives?

**Decision:** What was chosen?

**Reasoning:** Why?

**Affected rows/sources:** Which entries does this apply to?

**Reviewer:** Who signed off? (Initials)
```

---

## Sport taxonomy (controlled vocabulary)

Standardized `sport` column values. Add to this list before extracting a new sport.

| sport (column value) | includes | sport_category | notes |
|---|---|---|---|
| `basketball` | 5-on-5, 3-on-3, half-court | limited_contact | |
| `football_american` | tackle, flag (if specified, mark sub-variant in notes) | contact | flag football is limited_contact — split if needed |
| `football_association` | soccer | limited_contact | "Football" outside US contexts |
| `hockey_ice` | ice hockey, varsity and youth | contact | |
| `hockey_field` | field hockey | limited_contact | |
| `lacrosse_mens` | men's lacrosse | contact | |
| `lacrosse_womens` | women's lacrosse | limited_contact | rules differ significantly |
| `rugby` | union, league, sevens | contact | |
| `wrestling` | folkstyle, freestyle, Greco-Roman | contact | |
| `boxing` | amateur, youth | contact | |
| `mma` | mixed martial arts | contact | |
| `baseball` | hardball baseball | limited_contact | |
| `softball` | fastpitch, slowpitch | limited_contact | |
| `volleyball` | indoor, beach | non_contact | |
| `tennis` | singles, doubles | non_contact | |
| `track_and_field` | all events | non_contact | |
| `swimming` | all strokes, water polo handled separately | non_contact | |
| `water_polo` | | contact | |
| `gymnastics` | artistic, rhythmic | non_contact | |
| `cheerleading` | competitive, sideline | limited_contact | |
| `skateboarding` | | limited_contact | |
| `martial_arts_other` | karate, taekwondo if not boxing/MMA | contact | sub-discipline in notes |
| `judo` | judo | contact | broken out from martial_arts_other 2026-05-24 |
| `kickboxing` | kickboxing | contact | added 2026-05-24 |
| `muay_thai` | Muay Thai | contact | added 2026-05-24 |
| `cricket` | cricket all formats | limited_contact | added 2026-05-24 |
| `netball` | netball | limited_contact | added 2026-05-24 |
| `cycling` | road, BMX, MTB-not-split, scooter | non_contact | added 2026-05-24 |
| `mountain_biking` | MTB when reported separately | limited_contact | added 2026-05-24 |
| `hurling` | Gaelic hurling | contact | added 2026-05-24 |
| `kabaddi` | Kabaddi | contact | added 2026-05-24 |
| `gaelic_football_mens` | men's Gaelic football | contact | added 2026-05-24 |
| `gaelic_football_womens` | Ladies Gaelic football | limited_contact | added 2026-05-24 |
| `australian_rules_football` | AFL | contact | added 2026-05-24 |
| `skiing` | alpine + telemark | non_contact | added 2026-05-24 |
| `snowboarding` | snowboard | limited_contact | added 2026-05-24 |
| `equestrian` | pony + horseback + showjumping | limited_contact | added 2026-05-24 |
| `inline_skating` | inline skating + inline-skater hockey | limited_contact | added 2026-05-24 |
| `crossfit` | CrossFit | limited_contact | added 2026-05-24 |
| `handball` | team handball | contact | added 2026-05-24 (broken out from generic) |
| `floorball` | floorball | limited_contact | added 2026-05-24 |

When a new sport is encountered:
1. Check if it fits an existing category
2. If not, propose a new entry below in a decision entry
3. Get advisor approval
4. Then add to this table

---

## NEISS code mappings (verified 2026-05-21)

**Body part codes** (per 2024 NEISS Coding Manual, Appendix C, p. 24):

| code | meaning | use for this project? |
|---|---|---|
| 88 | Mouth (including lips, tongue, **and teeth**) | **Yes — primary inclusion code for dental injuries** |
| 76 | Face (eyelid, eye area, nose) | Yes — only when filtering for orofacial injury with dental involvement; requires diagnosis review per PROTOCOL §3.3 |
| 77 | Eyeball | No — not relevant to dental outcomes |
| 75 | Head | No (unless diagnosis explicitly cites dental involvement) |

**Sport product codes** (per 2024 NEISS Coding Manual, Appendix H, pp. 201–202):

| code | sport | maps to `sport` column |
|---|---|---|
| 1205 | Basketball | `basketball` |
| 1207 | Boxing | `boxing` |
| 1211 | Football (American) | `football_american` |
| 1215 | Lacrosse | needs disambiguation — NEISS does not split men's/women's; default to `lacrosse_mens` and flag with `quality_flag = review_needed` |
| 1266 | Volleyball | `volleyball` |
| 1267 | Soccer | `football_association` |
| 1270 | Wrestling | `wrestling` |
| 1272 | Gymnastics | `gymnastics` |
| 1279 | Ice hockey | `hockey_ice` |
| 1295 | Field hockey | `hockey_field` |
| 1333 | Skateboards | `skateboarding` |
| 3234 | Rugby | `rugby` |
| 3245 | Street hockey | new category — propose `hockey_street`, advisor approval needed |
| 3254 | Cheerleading | `cheerleading` |
| 3257 | Martial arts | `martial_arts_other` |
| 3272 | Hockey, not specified | flag for review; assign tentative `hockey_ice` only if comment indicates ice |
| 3274 | Swimming | `swimming` |
| 3276 | Water polo | `water_polo` |
| 3284 | Tennis | `tennis` |
| 5030 | Track and field | `track_and_field` |
| 5032 | Roller hockey | new category — propose `hockey_roller`, advisor approval needed |
| 5034 | Softball | `softball` |
| 5041 | Baseball (excluding softball) | `baseball` |

Codes not yet mapped because the taxonomy needs an advisor decision: 1200 (sports NEC), 3235 (other ball sports), 3236 (ball sports NS), 1392 (toy sports equipment).

---

## Decisions (chronological)

### 2026-05-21: Correction to PROTOCOL §4.1 — NEISS body part codes

**Trigger:** Verifying NEISS codes before writing `01_neiss_download.py`, as instructed by `scripts/README.md`.

**Question:** PROTOCOL.md §4.1 currently states: *"All entries with body part code 76 (mouth) or 77 (lower trunk/teeth) or 88 (face)..."* — are these labels correct?

**Options considered:**
- (a) Use the codes as printed in the protocol.
- (b) Use the codes from the official 2024 NEISS Coding Manual.

**Decision:** Use option (b). The protocol's labels are wrong; the codes appear shuffled. Per the official 2024 manual (Appendix C, p. 24):
- 76 = **Face** (eyelid, eye area, nose) — *not* mouth
- 77 = **Eyeball** — *not* "lower trunk/teeth" (which is also not a valid NEISS category)
- 88 = **Mouth** (including lips, tongue, **and teeth**) — this is the code that captures dental injuries

Inclusion filter for the NEISS extraction should be **body part = 88 (Mouth)** as the primary filter, with **76 (Face)** as a secondary filter only for cases whose diagnosis text indicates dental involvement (per PROTOCOL §3.3 "orofacial injury with dental involvement").

**Reasoning:** The codes in the original protocol cannot have been correctly verified — Appendix C is unambiguous and the 88-Mouth code is the only one whose definition mentions teeth. Proceeding with the protocol's labels would have excluded the actual dental cases (88) and included unrelated eyeball injuries (77).

**Affected rows/sources:** All NEISS extractions. None done yet, so no rework required. PROTOCOL.md §4.1 should be amended in the next protocol revision; until then this decision overrides.

**Reviewer:** Pending advisor review when advisor is secured.

**Sources of truth:**
- [NEISS Coding Manual, January 2024](https://www.cpsc.gov/s3fs-public/January-2024-NEISS-CPSC-only-Coding-Manual.pdf), Appendix C (Body Part Codes), p. 24 of PDF body text
- A local copy preserved at `data/raw/neiss/_reference/coding_manual_2024.pdf` (after first download — see `scripts/README.md`)

---

### 2026-05-24: Cross-source rate comparison surfaces denominator-unit issue

**Trigger:** First run of `scripts/21_cross_source_compare.py` showed basketball with a 345× spread in `rate_per_1000_ae` across 5 sources. Investigation: the wormald2022 rows had per-1000-AE-HOURS values stuffed into the per-1000-AE column. These are different units (1 AE ≈ 1 hour for some sports, but ~2-3 hours for soccer games, etc.).

**Decision:**
- For wormald2022, move the rates from `rate_per_1000_ae` into `rate_raw` (keeping the original number), leave `rate_per_1000_ae` empty, and update `rate_denominator_raw` to say "per 1000 athlete-exposure HOURS (not per AE)".
- Add a project-wide rule: `rate_per_1000_ae` is reserved for rates whose denominator is *exposures* (an athlete-session count). If the source's denominator is *hours*, `athlete-seasons`, `players` or `population`, leave `rate_per_1000_ae` empty and put the value in `rate_raw` with an explicit denominator string.
- Future refinement: add an `ae_denominator_type` controlled-vocab column (`ae`, `ae_hours`, `athlete_seasons`, `player_match_hours`, `population`, `players`) so the validator can enforce this. Deferred for now (additional schema change costs re-extraction).

**Affected rows:** wormald2022.csv (3 rows updated). Cross-source comparison re-run produces a cleaner basketball view.

**Reviewer:** Pending advisor review.

---

### 2026-05-24: Sport taxonomy formally expanded

**Trigger:** Project lead approved the taxonomy expansion that had been deferred since the 2026-05-23 "Sport taxonomy expansion needed" entry below. As of this entry these sports are now part of the controlled vocabulary instead of being stuffed into `sport = all_sports_aggregate` with a `subgroup_label` workaround.

**Decision:** the following are added to the §6.1 controlled vocabulary (also reflected in this file's "Sport taxonomy" table at the top):

| sport (column value) | includes | sport_category | rationale |
|---|---|---|---|
| `cricket` | hardball cricket all formats | limited_contact | yamada2009 (UK + AU schoolboy), 19566982 |
| `netball` | indoor / outdoor netball | limited_contact | welch2010 (NZ ACC) |
| `cycling` | road, BMX, mountain-bike, scooter (when reported as cycling) | non_contact | welch2010, emshoff1997, baek2021, NEISS papers |
| `hurling` | Gaelic hurling | contact | 20669600 |
| `kabaddi` | Kabaddi (South Asian contact sport) | contact | 36922269 |
| `gaelic_football_mens` | Gaelic football men's | contact | 34643329, 36394781 |
| `gaelic_football_womens` | Ladies Gaelic football | limited_contact | 37791703 |
| `australian_rules_football` | AFL | contact | finch2005, 23529288 |
| `skiing` | alpine ski, telemark | non_contact | 33377302, 20486946 (snowboarding-adjacent), emshoff1997 |
| `snowboarding` | snowboard riding | limited_contact | hayran2010 (PMID 20486946) |
| `equestrian` | pony + horseback riding, showjumping | limited_contact | nalcaci2006 (PMID 17073918), 26542314 (showjumping) |
| `inline_skating` | inline skating (incl. inline skater hockey when not split) | limited_contact | 17511835, 36878220 |
| `mountain_biking` | MTB specifically (when reported separately from road cycling) | limited_contact | 18821955, 33220143 |
| `crossfit` | CrossFit | limited_contact | 33188561 |
| `kickboxing` | kickboxing | contact | 40662680, 39452438 |
| `muay_thai` | Muay Thai | contact | 40662680 |
| `judo` | judo | contact | 31994310 |
| `handball` | team handball | contact | 23532813, 27622524, 28160512, 34047017 |
| `floorball` | floorball | limited_contact | 21199336 |

**Implementation:**
- Top-of-file taxonomy table extended (see "Sport taxonomy" section).
- `scripts/08_validate.py` `ALLOWED_SPORTS` set extended (validator now accepts these).
- A small follow-up pass over existing extractions updates rows that were using the `all_sports_aggregate + subgroup_label` workaround to use the proper sport value. Specifically:
  - welch2010 cricket/netball/cycling rows.
  - emshoff1997 cycling row.
  - mooney2021 / shore2023 / 34643329 Gaelic football rows.
  - finch2005 → `australian_rules_football`.
  - nalcaci2006 → `equestrian`.
  - hayran2010 → `snowboarding`.

**Reviewer:** Project lead approved 2026-05-24. Pending advisor review.

---

### 2026-05-23: Sport taxonomy expansion needed — cricket, netball, cycling, hurling, Kabaddi

**Trigger:** welch2010 extraction (NZ ACC sports dental claims 1999-2008) reports per-sport shares for cricket, netball, and cycling — none in the current §6.1 controlled vocabulary. Several already-included PubMed sources also reference hurling (PMID 20669600) and Kabaddi (PMID 36922269), which are also not in the vocabulary.

**Temporary handling (for now):** these sport names are stuffed into `sport = all_activities_aggregate` with the source's original sport name preserved in `subgroup_label = source_sport_<name>` and `quality_flag = review_needed`. Validator passes; the audit trail is preserved.

**Decision needed at advisor sign-off / before formal extraction begins:** add the following to the §6.1 sport vocabulary in this file:

| proposed value | includes | proposed sport_category | rationale |
|---|---|---|---|
| `cricket` | hardball cricket, traditional formats | limited_contact | major sport in UK/India/Australia/NZ youth populations; explicitly mentioned in 19566982 (PMID, included) |
| `netball` | indoor / outdoor variants | limited_contact | major in Commonwealth youth sports; mentioned in welch2010 |
| `cycling` | road, BMX, mountain bike when not extreme | non_contact OR move under "recreational" | high in NZ ACC data; debate whether to count cycling as a sport vs recreation |
| `hurling` | Gaelic hurling | contact | mentioned in 20669600 (Ireland) |
| `kabaddi` | traditional South Asian contact sport | contact | mentioned in 36922269 (India) |
| `gaelic_football_mens` / `gaelic_football_womens` | distinguish from football_american / football_association | contact / limited_contact | mentioned in 37791703 (Ladies GAA), 36394781 (Gaelic football children), 40267058 (adult Gaelic football) |
| `australian_rules_football` | AFL | contact | mentioned in 23529288 (review), 36327493 (sub-elite Australia) |

**Affected rows:** welch2010's per-sport breakdown (3 rows under all_activities_aggregate); future extractions of hurling / Kabaddi / Gaelic football sources.

**Reviewer:** Pending advisor review.

---

### 2026-05-23: Add `exposure_context` and `subgroup_label` columns to the data dictionary

**Trigger:** Project lead approved option A from the 2026-05-22 schema-gap entry. The schema-design todo flagged by validator check C10 is now resolved.

**Decision:** Two new columns added to the master extraction schema:

- `exposure_context` ∈ {`all`, `competition`, `practice`, `training`, `other`, *empty*} — which activity context the row's count/rate covers.
- `subgroup_label` (free-text snake_case) — within-source subgroups not already captured by sex / age_category / level_of_play / sport / exposure_context (most commonly: protective-equipment splits).

**Reasoning:** Even with only 3 pilot sources extracted, both patterns are universal in sports-injury epidemiology — every RIO-style surveillance paper reports competition/practice splits, and every protective-equipment study reports user/non-user subgroups. Waiting until source #10 to introduce the columns would mean re-extracting up to 7 additional sources. Doing it now costs 3 re-extractions (the pilots).

**Implementation:**
- `DATA_DICTIONARY.md`: columns + an "Exposure context and subgroup rows" section spelling out the values and the new uniqueness key `(sport × sex × age × level × basis × exposure_context × subgroup_label × season)`.
- `scripts/07_harmonize.py` `EXPECTED_COLUMNS` list extended.
- `scripts/08_validate.py`: new categorical check on `exposure_context`; C10 uniqueness key now includes both new columns; C10 should no longer warn on the two legitimate stratifications in collins2016 and labella2002.
- `scripts/06_write_pilot_extractions.py`: each of the 11 pilot rows tagged with the new columns. collins2016's overall row → `exposure_context=all`; competition row → `competition`; practice row → `practice`. labella2002's two rows → `subgroup_label=mouthguard_users` / `mouthguard_nonusers`. stewart2009's rows → `exposure_context=all`, `subgroup_label=""` (no protective-equipment subgroups in that source).

**Affected rows/sources:** 11 pilot rows in `data/extracted/{collins2016,labella2002,stewart2009}.csv`. PROTOCOL.md unchanged (this is a data-dictionary / extraction-schema concern, not a methodology change).

**Reviewer:** Pending advisor review.

---

### 2026-05-22: Schema gaps surfaced by first harmonization run (master.csv v0.1)

**Trigger:** First run of `scripts/07_harmonize.py` + `scripts/08_validate.py` against the three pilot extractions produced two C10 (duplicate-key) warnings flagging legitimate stratifications the schema can't disambiguate:

- **collins2016**: three rows share (source × sport × age × sex × level × basis × season) but differ on **exposure context** (all / competition / practice). Currently disambiguated only via `rate_denominator_raw` free text.
- **labella2002**: two rows share the same key but differ on **mouthguard subgroup** (users vs non-users). Currently disambiguated only via `mouthguard_use_rate` value (1.0 vs 0.0) — fragile because that field is also used for population-prevalence semantics.

**Question:** Add new columns to the data dictionary now to express these stratifications, or wait until more sources demand them?

**Decision (deferred — not making the schema change yet):** Keep `rate_denominator_raw` carrying the exposure context (e.g., "...(competition only)") and `mouthguard_use_rate` carrying the subgroup identifier for now. Revisit at the latest of: (a) the 10th extracted source, (b) advisor sign-off, or (c) the point at which we discover a third stratification dimension. Proposed columns when we do change:
- `exposure_context` ∈ `all` | `competition` | `practice` | `training` | `other`
- `subgroup_label` (free-text short label for protective-equipment / risk-modifier subgroups)

**Reasoning:** Two sources is not enough to lock in column choices; we'd risk picking names that don't generalize. Validation C10 will continue to warn on these rows, which is fine — they are surfaced as schema-design todos, not as data quality issues.

**Affected rows:** collins2016 (3 stratified rows), labella2002 (2 subgroup rows). No change to extractions; only the validator's interpretation of the warning.

**Reviewer:** Pending advisor review.

---

### 2026-05-22: stewart2009 primary-dentition row age_category re-tagged from `youth` to `unspecified`

**Trigger:** Validation check C5 flagged a <50% overlap between the row's age range (0–6) and the `youth` category band (5–12).

**Decision:** Re-tag `age_category = unspecified` for this row. Per PROTOCOL §6.2, when a source reports a range spanning categories, it's reported under the majority category — for this row, the majority is sub-5 (5 of 7 years), which is below the §3.1 inclusion floor and not represented in the youth/adolescent/collegiate/adult taxonomy. `unspecified` is the honest tag.

**Affected rows:** stewart2009 row "primary dentition" (age_min=0, age_max=6). Source still qualifies for inclusion because *other* age bands in the same source (mixed dentition 7–12, permanent 13–17) are squarely within scope.

**Reviewer:** Pending advisor review.

---

### 2026-05-22: Issues surfaced by pilot extractions (collins2016, labella2002, stewart2009)

**Trigger:** Three pilot extractions performed against the data dictionary before formal extraction begins (PROTOCOL pre-registration checklist item "First two sources extracted as pilot" — methodologically; formal extraction still gated on OSF pre-registration).

**Issues surfaced and provisional handling:**

1. **Aggregate / non-sport-specific rows need `sport` values not in the controlled vocabulary.** The pilots produced rows that don't map cleanly: `all_sports_aggregate` (collins2016 pooled rate), `all_activities_aggregate` (NEISS overall), `recreational_mixed` (NEISS 7–12y bicycle-led), `sports_aggregate` (NEISS 13–17y), `non_sport_setting` (NEISS home/furniture-led primary dentition).
   - **Provisional decision:** Add these as legitimate `sport` values for aggregate/non-sport-specific rows, with `sport_category = ''` (empty) since the contact taxonomy doesn't apply.
   - **Why:** Sources frequently report headline aggregate rates alongside per-sport rates. Throwing the aggregate row out loses important context. The alternative (one row per sport with `is_aggregate=TRUE` flag) restructures the schema more than needed.
   - **Add to taxonomy:** Pending advisor review. For now, these values flow through the data dictionary unchanged.

2. **Population-denominator surveillance is not AE-denominator.** NEISS-based stewart2009 reports rates as "per 100,000 children <18 yrs per year" (population denominator); the data dictionary's `rate_per_1000_ae` assumes athlete-exposure denominator. The two cannot be converted without external exposure data.
   - **Decision:** When the source uses a population denominator, leave `rate_per_1000_ae` empty; preserve the source's number in `rate_raw` and the denominator phrase in `rate_denominator_raw`. Note in `extraction_notes`.
   - **Why:** Fabricating an AE rate from population data would corrupt downstream analyses. The raw fields exist for exactly this case (PROTOCOL §6.4 — original denominators preserved).

3. **`mouthguard_use_rate` semantics are ambiguous.** Sources can report (a) MG use among all athletes in the sample, (b) MG use *among injured* athletes only (e.g., collins2016: "72.5% of injuries occurred while not wearing a MG"). These are different denominators.
   - **Provisional decision:** Use `mouthguard_use_rate` for the population-level prevalence whenever the source reports it. When only the injured-subset prevalence is available, record it in `mouthguard_use_rate` and clearly say so in `extraction_notes`. Add an explicit `mouthguard_use_rate_denominator` column in a future data dictionary revision if this becomes common.
   - **Pending:** Decide whether to add the explicit denominator column before scaling extraction.

4. **Injury counts sometimes have to be back-calculated.** labella2002 abstract gives rates (per 1000 AE) and total AE, but does not state injury counts directly. Reading the full text will give the exact counts; for the pilot, the count column is left empty and the back-calc is noted in `extraction_notes`.
   - **Decision:** Do **not** populate `injury_count` with back-calculated values when the source doesn't state the count explicitly. Leave the field empty and note the back-calc in `extraction_notes` so analysts know it can be computed but isn't sourced.

5. **Sub-5 ages overlap the inclusion floor.** stewart2009 reports a primary-dentition (<7y) age band that partially overlaps below the 5–22 inclusion floor.
   - **Decision:** Extract the row as the source reports it (`age_min = 0, age_max = 6`), flag `quality_flag = partial_data`, and let downstream filtering by `age_min >= 5` handle exclusion if needed. The alternative (synthetically restricting the band) is unjustified without raw data.

**Affected rows/sources:** Pilot extractions at `data/extracted/{collins2016, labella2002, stewart2009}.csv` (11 rows total). All future extractions follow these rules until revised. The data dictionary is updated to flag the population-denominator case; the others will be revisited after advisor review.

**Reviewer:** Pending advisor review.

---

### 2026-05-22: Extract adult-comparator rows from already-included sources

**Trigger:** Project lead asked whether the youth-only scope (PROTOCOL §3.1, ages 5–22) was too narrow and whether adult populations should be incorporated. Screening of the 200 PubMed candidates produced 51 records held back by age (6 `E-age`, 37 `R-age`, 8 `R-mixed`) — meaningful but not catastrophic.

**Question:** Should the project (a) broaden inclusion to all ages, (b) keep youth-only and discard adult data even when it is present in included sources, or (c) keep youth-only at the *source* level but extract adult bands alongside youth when the source reports both?

**Options considered:**
- (a) Broaden to all ages. Doubles the include set (~120 records) and dilutes the project's stated differentiator (PROTOCOL §1 — the gap is youth-specific). Rebrand required; Conrad Challenge alignment weakens; ~doubles extraction workload before the Sept–Nov deadline.
- (b) Status quo. Throws away age-stratified adult data already present in surveillance sources (NEISS, NZ ACC, NCAA-adjacent insurance, multi-age cohort studies) at extraction time. Wasteful.
- (c) Middle path: source inclusion stays youth-only; extraction captures all age bands the source reports; adult bands tagged `extraction_basis = adult_comparator`.

**Decision:** Option (c).

**Reasoning:**
- The project's headline identity ("Youth Sports Dental Injury Database") and its stated gap (PROTOCOL §1) remain youth-centred — no rebrand, no narrative shift, no Conrad Challenge framing rework.
- Adult rows are essentially free to extract when they sit in the same table as the youth data we are already extracting. Discarding them would be a sunk-cost loss.
- Researchers using the dataset can answer cross-age questions ("is youth rate higher than adult?") by including the comparator rows; the published headline analyses subset to `extraction_basis = 'youth_primary'`.
- This does **not** rescue any of the records currently held in `screened_excluded` for `E-age` (adult-only sources), since those sources have no youth data to anchor inclusion.

**Implementation:**
- `DATA_DICTIONARY.md`: add `adult` to allowed `age_category` values and add an `extraction_basis` column with values `youth_primary` | `adult_comparator`.
- `PROTOCOL.md` §6.2.1 added (new subsection); §9 outputs note that master.csv carries both row types.
- Re-screening not needed: the 6 `E-age` and 37 `R-age` records were excluded/held because their *source* had no youth data; the new rule changes only what we extract from sources that already pass §3.1.

**Affected rows/sources:** None of the existing 200 candidate decisions change. The decision affects extraction templates for every future extraction. When pilot extractions are run, both youth and adult bands are captured per source.

**Reviewer:** Pending advisor review when advisor is secured.

---

### 2026-06-12: Full-text review of the open-access subset of the needs_additional_review pile

**Trigger:** `scripts/30_oa_url_lookup.py` (Unpaywall) and `scripts/31_pmc_availability.py` (NCBI PMC) identified which of the 91 `needs_additional_review` PubMed records have free full text. Full texts were retrieved (PMC HTML, repository PDFs read with pdfplumber, OA-journal redirects) and reviewed against PROTOCOL §3.1/§3.3. This is the project lead's full-text screening step (AI-assisted, same basis as the 2026-05-21 abstract screen), not the §4.4 reliability re-screen, which still awaits the advisor.

**Retrievability (why most of the 91 stay pending):** publisher PDFs behind Cloudflare (Wiley `pdfdirect`, BMJ, JOMS, lww) return 403/402 to any non-browser client; three PMC records (PMIDs 18254, 1982928, 6130812 — pre-1995 BJSM rugby papers) are scanned page-images with no OCR text; two Swiss Dental Journal download URLs now 404. These remain `needs_additional_review` (advisor library access or a browser session needed).

**Decisions made (7 records resolved; needs_additional_review 91 → 84):**

| PMID | source_id | decision | reason | basis |
|---|---|---|---|---|
| 24198704 | halabchi2007 | **included** → extracted | I-pri | Iran women's Shotokan karate championships; sport-related dental count (3 avulsion/subluxation) with youth competitors present |
| 15562172 | exadaktylos2004 | fulltext_excluded | E-age | Swiss ED maxillofacial surveillance; not age-stratified, facial fractures w/o separate dental count |
| 16118304 | — | fulltext_excluded | E-age | NZ rugby ecological MG study; national all-ages ACC dental claims not separable to 5-22 |
| 19925982 | — | fulltext_excluded | E-offtop | LA adolescents 14-20 orofacial trauma but only 3% sport-related, no sport-specific data |
| 2893649 | — | fulltext_excluded | E-age | International (elite adult) field hockey; no age data, no youth subset |
| 36538371 | — | fulltext_excluded | E-age | Finnish trauma-centre ice-hockey facial fractures; adult-dominated (98.5% male), not age-stratified |
| 39060115 | tadmor2025 | fulltext_excluded | E-nodent | UK rugby league (brain) concussion symptom non-reporting; no dental/orofacial injury outcome |

One record (40662680, Swiss Muay Thai/K-1/kickboxing survey, Robbiani & Filippi 2025) had its full text retrieved but stays `needs_additional_review` (confidence lowered to `low`): it reports all-ages dental injuries (52 cases, 19%) and MG use, but the subject age distribution sits in a PDF table that did not extract cleanly, so a 5-22 subset could not be confirmed or isolated.

**Reasoning for the exclusions:** several of these report real dental/orofacial data but at the population level with no way to isolate the 5-22 band (§3.1) — consistent with the existing rule that a row needs an identifiable youth (or extractable adult-comparator alongside youth) population. Excluding all-ages-only sources where no youth slice is separable is the honest PRISMA outcome of full-text review, not a scope change.

**Audit trail:** decisions live in `scripts/screening_overrides.py` (with per-record full-text notes dated 2026-06-12); `outputs/needs_additional_review_fulltext_review_2026-06-12.md` records every fetch attempt and outcome; `docs/sources.md` and `outputs/screening_report_2026-05-21.md` regenerated via scripts 02→03→04.

**Reviewer:** Pending advisor review.

---

### 2026-06-12: halabchi2007 — combined "avulsion or subluxation" count and mixed-age pooled row

**Trigger:** Extracting halabchi2007 (see entry above).

**Issues and handling:**

1. **Combined injury category that spans two Andreasen classes.** The source reports "tooth avulsion or subluxation (3, 1.6%)" as a single un-splittable count. Avulsion and luxation/subluxation are distinct Andreasen categories, so neither single `injury_category` value is fully correct.
   - **Decision:** `injury_category = unspecified_dental`, with the verbatim "tooth avulsion or subluxation" preserved in `injury_type_raw` and explained in `extraction_notes`. Do not invent a split of the 3 cases.
   - **Why:** consistent with existing precedent (e.g. zazryn2010, where a combined displacement/luxation/fracture/avulsion dental count maps to `unspecified_dental`). Preserves the raw description without overclaiming a category.

2. **Dental count not age-stratified in a mixed-age championship.** The 3 dental injuries are pooled across all age groups (≤10 to ≥31); a youth-only count cannot be isolated.
   - **Decision:** one pooled row, `age_category = mixed`, `extraction_basis = youth_primary` (per the established convention that mixed-age rows from youth-qualifying sources are youth_primary), `age_min`/`age_max` left empty (exact bounds not reported), `quality_flag = partial_data`.

3. **Denominators are bouts/athletes, not athlete-exposures.** `rate_raw = 1.6` (% of 186 injuries) with the denominator phrase preserved; `rate_per_1000_ae` left empty (not convertible without AE data), per the 2026-05-21 population-denominator rule.

**Reviewer:** Pending advisor review.

---

### 2026-06-13: `rate_per_1000_ae` is enforced as a single per-1000-athlete-exposure scale

**Trigger:** Audit of the 29 rows carrying a `rate_per_1000_ae` value found the column was being read as if it held a common scale, but next to it sat `rate_denominator_raw` strings naming *different* denominators ("per 100,000 athlete-exposures", "per 1000 player-match-hours", "per 100 player-hours", "per 1000 athlete-sessions"). This extends the 2026-05-24 "denominator-unit issue" entry, which set the rule but was never enforced across the full dataset or by the validator.

**Question:** Were the 29 values actually on different scales, and if so how do we put them on one true per-1000-AE scale (or split into value+unit)?

**Investigation (corrects an assumption in the trigger):**
- The 9 rows whose *raw* rate is reported "per 100,000 athlete-exposures" (azadani2023 ×3, collins2016 ×5, yard2008 ×1) were **already correctly converted** at extraction time: `rate_per_1000_ae = rate_raw ÷ 100` (e.g. azadani2023 basketball `rate_raw = 2.4` per 100k AE → `rate_per_1000_ae = 0.024` per 1000 AE). The "per 100,000" phrasing in `rate_denominator_raw` describes `rate_raw`, **not** the per-1000-AE column. These needed **no** change — dividing them again would have corrupted correct data.
- `rate_denominator_raw` is, by definition (DATA_DICTIONARY.md), the original phrasing for `rate_raw`. It is *not* a label for `rate_per_1000_ae`. This was the source of the confusion.
- The only genuinely mis-filed rows were **time-denominator** rates pasted verbatim into the AE column:
  - **radelet1996** (1 row): `0.57` per-1000-*player-hours* (raw `0.057` per 100 player-hours).
  - **rugby_europe_iss_2024** (8 rows): per-1000-*player-match-hours* (Sevens championship/trophy + head/face subsets).
- **collins2004** (4 rows) reports "per 1000 **athlete-sessions**." An athlete-exposure is, by the standard NCAA-ISS / RIO definition, one athlete participating in one practice or competition — i.e. one session. The 2026-05-24 entry already defines AE as "an athlete-session count." So athlete-sessions **are** the AE unit; these 4 rows are valid per-1000-AE and stay. (An earlier framing of this audit listed athlete-sessions as non-AE; that is incorrect and is overridden here.)

**Decision:**
- **Approach (a), convert-and-null in place** — keep the `rate_per_1000_ae` column rather than splitting into `rate_value` + `rate_unit`. This honours the 2026-05-24 decision (which reserved this column for AE denominators and explicitly *deferred* a richer multi-column schema because it would force re-extraction). The split option remains available as a future v1.0 step if multi-unit structured comparison is ever needed.
- **Invariant:** `rate_per_1000_ae` is populated **iff** the source denominator is an athlete-exposure (athlete-/athletic-exposure, athlete-session, or "AE"). Per-100,000-AE rates are stored already divided by 100. Time (hours / player-match-hours), season, population, and percent-of-injuries denominators leave `rate_per_1000_ae` empty; their value stays in `rate_raw` + `rate_denominator_raw`.
- Blanked `rate_per_1000_ae` for the 9 time-denominator rows above (values preserved in `rate_raw`). Result: 20 rows now carry a per-1000-AE value, all on one scale.

**Implementation:**
- `data/extracted/radelet1996.csv` (1 row) and `data/extracted/rugby_europe_iss_2024.csv` (8 rows): `rate_per_1000_ae` blanked; all other fields unchanged.
- `DATA_DICTIONARY.md`: `rate_per_1000_ae` and `rate_denominator_raw` definitions tightened to state the AE-only invariant and that `rate_denominator_raw` describes `rate_raw`.
- `scripts/08_validate.py`: new **C11** (FAIL) — every populated `rate_per_1000_ae` row must have an AE-type `rate_denominator_raw`.
- Re-ran `07_harmonize.py` → `08_validate.py` (0 FAILs), `21_cross_source_compare.py`, `33_rate_explorer_data.py`. As a consequence the cross-source view no longer pools rugby AE rates (collins_rugby2008) with rugby player-match-hours rates (rugby_europe).
- Methods paper and Rate Explorer caveats updated (count 29 → 20; mixed-denominator warning replaced with the normal cross-source comparability caveats).

**Affected rows/sources:** radelet1996 (1), rugby_europe_iss_2024 (8). No other extractions changed.

**Reviewer:** Pending advisor review.

---

### 2026-06-16: Repair of fabricated author attributions across the extracted sources

**Trigger:** A reader question about Liang & Chuang (2024) "Mechanisms of dental injuries in basketball" surfaced that its master.csv row was attributed to a non-existent first author ("Williams T") under source_id `williams2024`. A systematic audit (`scripts/34_audit_citations.py`) then compared every extracted source's citation against the authoritative cached PubMed abstract metadata (`data/raw/papers/_abstracts/<PMID>.json`) by matching on title.

**Finding (serious):** the AI-assisted batch extractions had copied paper **titles** correctly but **invented author names** for a large fraction of sources, and derived `source_id`s from those wrong authors. **67 of the 106 sources** (67 of the 93 PubMed-keyed sources) carried an incorrect author-derived id and a fabricated citation. Examples: `collins2004`→ actually **Beachy G** (PMID 15592602); `radelet1996`→ **Pasternack JS et al.**; `hosea1996`→ **Gomez E et al.**; `zazryn2010`→ **Shirani G et al.**; `benson2002`→ **Stuart MJ et al.**; `williams2024`/`williams2023`→ **Liang & Chuang**. The 39 unchanged ids were 26 already-correct PubMed sources + 12 NEISS year files + Rugby Europe + `halabchi2007`.

**Root causes (two layers):**
1. The per-source extraction scripts (`scripts/14-19, 25, 28`) hardcoded the wrong `source_id` and a fabricated `citation=` string for each affected source.
2. `scripts/26_bibliography.py` carried a **hardcoded** `PMID_TO_SOURCE_ID` map echoing the same wrong ids.

**Decision:** correct authorship from the authoritative PubMed metadata, end-to-end (data, scripts, and generators), and add guards so it cannot recur.

**Implementation:**
- `scripts/34_audit_citations.py` — new reusable audit; FAILs if any source's first-author surname (ASCII-folded) disagrees with its PMID's abstract. Run it before releases.
- `scripts/35_fix_attributions.py` — rewrote `source_id` + `citation` (+ doi) in every extracted CSV from `sources.md` (authoritative ids) + the abstract JSON (authoritative authors/title/journal), joining by title. Renamed the per-source files.
- `scripts/36_fix_batch_script_attributions.py` — applied the same correction to the hardcoded id/citation literals **inside** the batch extraction scripts, so re-running them reproduces the corrected data rather than reverting it.
- `scripts/26_bibliography.py` — replaced the hardcoded `PMID_TO_SOURCE_ID` with a parse of `docs/sources.md`, so BibTeX keys can no longer drift from the dataset.
- `scripts/03_apply_screening_to_sources.py` — `lastname()` now ASCII-folds (Cetinbaş→cetinbas, O'Malley→omalley, Gábris→gabris, Zaleckienė→zaleckiene) so ids are valid filenames and BibTeX keys; `sources.md` regenerated.
- The 2026-06-13 C11 blanking (radelet/pasternack, rugby_europe) was encoded into `scripts/19` and `scripts/20` so it survives re-extraction.

**Verification:** `scripts/34` now reports **0 author mismatches / 0 year mismatches** (92 of 93 confirmed against PubMed; `stuart2002` correct but its title isn't auto-matchable). Re-running all batch extraction scripts → `07_harmonize.py` reproduces `data/harmonized/master.csv` **byte-for-byte** (md5 identical to the pre-repair-verified corrected snapshot). Validator: 426 rows, **0 FAILs / 0 WARNs**.

**Note on prior references:** entries in this log dated before 2026-06-16, plus older `CHANGELOG.md` and `outputs/session_*_summary.md` entries, refer to sources by their **old** ids (e.g. `zazryn2010`, `collins2004`, `radelet1996`, `benson2002`, `collins_rugby2008`). Those are point-in-time records and are left intact (append-only); the authoritative current id for any of them is whatever `docs/sources.md` now lists for that PMID. The full 67-id old→new mapping is reproducible from `git show HEAD~:data/harmonized/master.csv` vs the current file.

**Reviewer:** Pending advisor review. Recommend the advisor spot-check a sample of citations against PubMed as part of sign-off.

---

### 2026-06-24: Comparability tiering — `measure_type` + `comparability_group` columns

**Trigger:** A senior surveillance researcher (Christy Collins, President of Datalys / NCAA-ISP) warned that "these databases/studies are not actually comparable due to differences in definitions, methodology, inclusion/exclusion criteria." An audit confirmed the database mixed at least 7 incompatible outcome-measure bases in one value space (ED-visit estimates, per-AE rates, per-hours rates, per-population rates, per-season rates, prevalence proportions, raw counts) with **no machine-readable flag** distinguishing them — so a consumer of `master.csv`/SQLite could naively line up a NEISS ED estimate next to a per-100k-AE rate next to a survey prevalence.

**Decision:** Add two **derived** columns to `master.csv` (computed at harmonization, not stored in the per-source extraction CSVs):
- `measure_type` — controlled vocabulary of the row's outcome-measure / rate basis: `incidence_per_AE`, `incidence_per_exposure_hours`, `incidence_per_population`, `incidence_per_season`, `prevalence_proportion`, `ed_visit_estimate`, `raw_count`, `rate_ratio_or_effect_size`, plus a temporary `unclassified_pending_review`.
- `comparability_group` — coarse key on which **direct** comparison is permitted: the short measure family, suffixed `__aggregate` for pooled / non-sport-specific rows. Two rows are directly comparable only when they share this value.

**Implementation:**
- `scripts/_derived_columns.py` (new) — deterministic classifier from `rate_denominator_raw` + `source_id`, a `MANUAL_MEASURE_TYPE` override table for the long tail, and the `comparability_group` derivation. Imported by `07` (populate) and `08` (validate).
- `scripts/07_harmonize.py` — separates `EXTRACTED_COLUMNS` (36, source-of-truth) from `DERIVED_COLUMNS` (2); master is now 38 columns.
- `scripts/08_validate.py` — new check **C12** (FAIL if `measure_type` empty or out-of-vocab, or `comparability_group` empty; WARN listing the `unclassified_pending_review` count).
- `DATA_DICTIONARY.md` — documents both columns + the comparability rule.
- `scripts/27` (SQLite) and `scripts/33` + `docs/rate-explorer.html` regenerated/updated: the Rate Explorer now **segregates results into one table per `measure_type`** (ordered most-comparable-first) and never co-plots incompatible tiers.

**Auto-classification result (426 rows):** ed_visit_estimate 255, prevalence_proportion 89, incidence_per_AE 22, incidence_per_exposure_hours 17, incidence_per_season 11, raw_count 6, rate_ratio_or_effect_size 4, incidence_per_population 2, **unclassified_pending_review 20** (all empty-denominator rows — listed in the 2026-06-24 session report for manual classification; to be pinned via `MANUAL_MEASURE_TYPE`).

**Limitation (phase 2):** `prevalence_proportion` currently lumps population-prevalence (% of athletes injured) with within-injury proportions (% of injuries that were dental); separating those needs the planned `case_definition` flag. Validator: 426 rows, 0 FAILs, 1 WARN (the 20 pending rows).

**Reviewer:** Pending advisor review.

---

### 2026-06-24: Data provenance flag + redistribution-rights documentation

**Trigger:** Christy Collins (Datalys / NCAA-ISP) cautioned: "make sure each of the datasets [is] able to be used in this manner. For example, the NCAA-ISP data are owned by the NCAA, and they have restrictions on who can use the data and for what purposes." A provenance audit confirmed the database holds **no** raw NCAA-ISP / RIO / ACC microdata — every NCAA/RIO/ACC-derived number comes from a peer-reviewed publication reporting its own results.

**Decision:** Make provenance explicit and document redistribution rights.
- Added a derived per-source column **`data_provenance`** ∈ {`public_domain_raw`, `published_summary`, `governing_body_public`} (computed in `scripts/_derived_columns.py`; master now 39 columns). Result: 12 NEISS sources → `public_domain_raw`; Rugby Europe → `governing_body_public`; 93 peer-reviewed papers → `published_summary`.
- Added **PROTOCOL.md §12 "Data provenance and redistribution rights"** and a matching section in **LICENSE-DATA**, stating the database redistributes only public-domain surveillance (NEISS, aggregated), published summary statistics, and public governing-body reports; contains no raw/restricted NCAA-ISP/RIO/ACC microdata; and that CC BY 4.0 covers the *compilation*, with all source facts attributed.
- Added validator check **C13** (`data_provenance` populated + in vocabulary).

**Open item flagged for the project lead:** confirm the **Rugby Europe 2024 Injury Surveillance Report** reuse/redistribution terms before v1.0 (marked TODO in PROTOCOL §12 and LICENSE-DATA). It is the one `governing_body_public` source.

**Reviewer:** Pending advisor review.

---

### 2026-06-24: Prominent "Comparability & limitations" note in public-facing docs

**Trigger:** Same reviewer critique (comparability). Beyond the machine-readable `measure_type` tiering (2026-06-24 entry above), readers arriving at the repo/site/paper need a plain-language warning.

**Decision:** Add a "Comparability & limitations" section to the three public-facing surfaces — `README.md`, the live landing page (`docs/index.md`), and `outputs/methods_paper_draft.md` — stating that denominators differ across sources, that aggregate rows exist, that NEISS figures are ED-treated only, that all rows are `quality_flag = partial_data`, and that comparisons must be made within a `comparability_group` / `measure_type` tier. Documentation only; no data change.

**Reviewer:** Pending advisor review.

---

### 2026-06-24: Classify the 20 long-tail rows; add `mouthguard_use_proportion` measure type

**Trigger:** The 2026-06-24 comparability tiering left 20 empty-denominator rows as `unclassified_pending_review` for manual classification by the project lead.

**Decision (project-lead classifications):**
- **`ed_visit_estimate`** (8 rows) — NEISS / pediatric-ED craniofacial counts & weighted estimates: `kaplan2022`, `nahas2021`, `pierrot2021`, `slavin2021`, `stewart2009` (×3), `van2021`.
- **`raw_count`** (6 rows) — raw injury / insurance-claim counts: `chan2011`, `pandey2025`, `quarrie2020`, `welch2010` (×2), `danis2000`.
- **`prevalence_proportion`** (2 rows) — population prevalence / awareness surveys: `pattussi2006`, `caglar2005`.
- **`mouthguard_use_proportion`** (4 rows) — see new measure type below: `kroon2016`, `shore2021`, `shore2023`, `stanbouly2021`.

These are pinned in `scripts/_derived_columns.py` `MANUAL_MEASURE_TYPE`, keyed by `(source_id, "")` (all are empty-denominator rows).

**New measure type — `mouthguard_use_proportion`:** added as a 9th controlled value. Rationale: four rows measure protective-equipment (mouthguard) **use** as a proportion (e.g. "99.2% wore a mouthguard") and have **no injury outcome** — none of the eight injury-measure types fit, and forcing them into `prevalence_proportion` would conflate equipment-use prevalence with injury prevalence. The new value is explicitly **not comparable to any injury measure**. Added to `DATA_DICTIONARY.md`, the `MEASURE_TYPES` vocab (so validator C12 accepts it), and the Rate Explorer's tier metadata.

**Result:** all 426 rows now carry a `measure_type`; **0 remain `unclassified_pending_review`**. Validator: 426 rows, **0 FAILs, 0 WARNs**. Final distribution: ed_visit_estimate 263, prevalence_proportion 91, incidence_per_AE 22, incidence_per_exposure_hours 17, raw_count 12, incidence_per_season 11, mouthguard_use_proportion 4, rate_ratio_or_effect_size 4, incidence_per_population 2.

**Reviewer:** Pending advisor review.

---

### 2026-06-24: Move internal working docs out of the public repo (`internal/`, gitignored)

**Trigger:** Pre-meeting repo review. The public repository mixed the scientific artifact (data, protocol, dictionary, decisions, methods, validation) with *internal working docs* — outreach strategy, AI-session logs, and screening scratch files — which add noise and reveal project-management detail not relevant to a research consumer.

**Decision:** Moved the following into a new **gitignored `internal/` folder** (kept locally, removed from the public/deployed repo): `advisor_outreach_brief.md`; the seven `session_2026-*_summary.md` logs; `zenodo_setup_walkthrough.md`; the four `needs_additional_review_*` screening-scratch files (OA-URL and PMC lookup CSVs, the status doc, and the 2026-06-12 full-text review log); and the `_pdf_upload_server.py` dev helper.

**Reference fixes (so the public repo has no dead links):**
- `scripts/30`, `scripts/31` now write their lookup CSVs to `internal/` (created on run).
- `scripts/03` template and `outputs/methods_paper_draft.md` no longer link the moved full-text-review file; they point to `docs/decisions.md` (which stays public). `sources.md` regenerated.
- Append-only historical mentions in this log and `CHANGELOG.md` (dated 2026-06-12 entries) are left intact per the append-only convention; the artifacts they name now live in `internal/`.

**Note:** the screening audit trail itself remains fully public — every record's status and reason is in `docs/sources.md` and `outputs/screening_report_2026-05-21.md`; only the supplementary scratch/lookup files moved. Nothing affecting reproducibility of `master.csv` was moved.

**Reviewer:** Pending advisor review.

---

<!-- Add new decisions above this line, most recent first or chronological — pick one and stick with it. Chronological recommended for audit trail. -->
