# Validation Report — 2026-05-23

_Run against `data/harmonized/master.csv` (35 rows)._

## Summary

- Rows checked: **35**
- Distinct sources: **7**
- FAILs: **0**
- WARNs: **0**
- Rows flagged `quality_flag=review_needed`: **3**

## ✅ No FAILs

All hard validation checks (schema, categorical values, numeric ranges, age consistency, source coverage) passed.

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
| azadani2023 | 5 | youth_primary |
| collins2016 | 5 | youth_primary |
| labella2002 | 2 | youth_primary |
| neiss2023 | 2 | youth_primary |
| quarrie2020 | 7 | adult_comparator, youth_primary |
| stewart2009 | 4 | youth_primary |
| welch2010 | 10 | youth_primary |