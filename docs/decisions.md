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
| `martial_arts_other` | karate, taekwondo, judo if not boxing/MMA | contact | sub-discipline in notes |

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

<!-- Add new decisions above this line, most recent first or chronological — pick one and stick with it. Chronological recommended for audit trail. -->
