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

## Decisions (chronological)

### YYYY-MM-DD: [First decision will go here]

**Trigger:** [example placeholder — delete when first real decision added]

This is where every harmonization decision gets recorded. The first entry will likely concern the exact age range cutoffs, since the protocol allows for some judgment when sources report overlapping age categories.

---

<!-- Add new decisions above this line, most recent first or chronological — pick one and stick with it. Chronological recommended for audit trail. -->
