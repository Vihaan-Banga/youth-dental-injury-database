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

<!-- Add new decisions above this line, most recent first or chronological — pick one and stick with it. Chronological recommended for audit trail. -->
