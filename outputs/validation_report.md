# Validation Report — 2026-05-22

_Run against `data/harmonized/master.csv` (11 rows)._

## Summary

- Rows checked: **11**
- Distinct sources: **3**
- FAILs: **0**
- WARNs: **2**
- Rows flagged `quality_flag=review_needed`: **0**

## ✅ No FAILs

All hard validation checks (schema, categorical values, numeric ranges, age consistency, source coverage) passed.

## ⚠️  WARNs (review, not blocking)

- **C10** — 3 rows share key ('collins2016', 'all_sports_aggregate', 'adolescent', 'mixed', 'school_varsity', 'youth_primary', '2008/09–2013/14 academic years') — possible duplicate or valid stratification we haven't captured in another column
- **C10** — 2 rows share key ('labella2002', 'basketball', 'collegiate', 'male', 'elite', 'youth_primary', '1999–2000 season') — possible duplicate or valid stratification we haven't captured in another column

## Check reference

- **C1** schema completeness
- **C2** categorical values in dictionary
- **C3** numeric fields in plausible ranges (`rate_per_1000_ae` < 100 per PROTOCOL §7)
- **C4** `age_min ≤ age_max`
- **C5** `age_category` consistent with `age_min`/`age_max` (warning only)
- **C6** `extraction_basis = adult_comparator` iff `age_category = adult`
- **C7** `sport` in controlled vocabulary (`docs/decisions.md`)
- **C8** `quality_flag` in allowed set (covered by C2)
- **C9** every source has at least one `youth_primary` row
- **C10** no duplicate (source × sport × age × sex × level × basis × season) keys

## Per-source row count

| source_id | rows | bases |
|---|---|---|
| collins2016 | 5 | youth_primary |
| labella2002 | 2 | youth_primary |
| stewart2009 | 4 | youth_primary |