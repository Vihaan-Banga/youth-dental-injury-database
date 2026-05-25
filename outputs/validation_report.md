# Validation Report — 2026-05-25

_Run against `data/harmonized/master.csv` (256 rows)._

## Summary

- Rows checked: **256**
- Distinct sources: **73**
- FAILs: **0**
- WARNs: **0**
- Rows flagged `quality_flag=review_needed`: **0**

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
| alawawdeh2021 | 1 | youth_primary |
| alawawdeh2022 | 1 | youth_primary |
| ali2007 | 2 | youth_primary |
| alotaibi2014 | 1 | youth_primary |
| amy2005 | 1 | youth_primary |
| azadani2023 | 5 | youth_primary |
| azimi2020 | 1 | youth_primary |
| baek2021 | 1 | youth_primary |
| benson2002 | 3 | youth_primary |
| calderon2020 | 1 | youth_primary |
| carter2000 | 1 | youth_primary |
| cetin2026 | 1 | youth_primary |
| cetinbas2008 | 2 | youth_primary |
| chan2011 | 1 | youth_primary |
| chapman2004 | 1 | youth_primary |
| collins2004 | 5 | youth_primary |
| collins2016 | 5 | youth_primary |
| collins_baseball2008 | 1 | youth_primary |
| collins_rugby2008 | 2 | youth_primary |
| danis2000 | 1 | youth_primary |
| deshpande2014 | 2 | youth_primary |
| emshoff1997 | 3 | youth_primary |
| fakhruddin2009 | 1 | youth_primary |
| finch2005 | 1 | youth_primary |
| goswami2017 | 4 | youth_primary |
| hamdan2026 | 1 | youth_primary |
| hayran2010 | 1 | youth_primary |
| hosea1996 | 1 | youth_primary |
| ivanovics2012 | 1 | youth_primary |
| labella2002 | 2 | youth_primary |
| leite2012 | 1 | youth_primary |
| levin2003 | 3 | youth_primary |
| levin2007 | 1 | youth_primary |
| livny2008 | 1 | youth_primary |
| mahlangu2008 | 1 | youth_primary |
| marcenes2001 | 1 | youth_primary |
| mate2001 | 1 | youth_primary |
| mcdonough2008 | 1 | youth_primary |
| mcevoy2012 | 1 | youth_primary |
| mcintosh2005 | 3 | youth_primary |
| mooney2021 | 1 | youth_primary |
| naasan2021 | 3 | youth_primary |
| naidoo2009 | 1 | youth_primary |
| nalcaci2006 | 1 | youth_primary |
| nasu2023 | 3 | youth_primary |
| neiss2013 | 22 | youth_primary |
| neiss2014 | 19 | youth_primary |
| neiss2015 | 19 | youth_primary |
| neiss2016 | 22 | youth_primary |
| neiss2017 | 22 | youth_primary |
| neiss2023 | 21 | youth_primary |
| pattussi2006 | 1 | youth_primary |
| quarrie2020 | 7 | adult_comparator, youth_primary |
| radelet1996 | 1 | youth_primary |
| ranalli2005 | 1 | youth_primary |
| shore2023 | 1 | youth_primary |
| singh2014 | 2 | youth_primary |
| stewart2009 | 4 | youth_primary |
| trinidad2007 | 3 | youth_primary |
| tsuchiya2017 | 3 | youth_primary |
| udayamalee2024 | 2 | youth_primary |
| vanierssel2021 | 1 | youth_primary |
| welch2010 | 10 | youth_primary |
| williams2023 | 1 | youth_primary |
| williams2024 | 1 | youth_primary |
| wong2008 | 1 | youth_primary |
| wormald2022 | 3 | youth_primary |
| yamada2009 | 2 | youth_primary |
| yard2008 | 1 | youth_primary |
| yard2015 | 2 | youth_primary |
| yildirim2013 | 1 | youth_primary |
| zaror2018 | 5 | youth_primary |
| zazryn2010 | 1 | youth_primary |