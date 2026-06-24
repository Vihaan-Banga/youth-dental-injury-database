# Validation Report — 2026-06-24

_Run against `data/harmonized/master.csv` (426 rows)._

## Summary

- Rows checked: **426**
- Distinct sources: **106**
- FAILs: **0**
- WARNs: **1**
- Rows flagged `quality_flag=review_needed`: **0**

## ✅ No FAILs

All hard validation checks (schema, categorical values, numeric ranges, age consistency, source coverage) passed.

## ⚠️  WARNs (review, not blocking)

- **C12** — 20 rows are measure_type='unclassified_pending_review' — awaiting manual classification

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
- **C11** `rate_per_1000_ae` populated only when `rate_denominator_raw` is an athlete-exposure denominator
- **C12** `measure_type` populated and in the controlled vocabulary; `comparability_group` populated
- **C13** `data_provenance` populated and in the controlled vocabulary

## Per-source row count

| source_id | rows | bases |
|---|---|---|
| abdel2021 | 3 | youth_primary |
| allareddy2014 | 1 | youth_primary |
| amy2005 | 1 | youth_primary |
| azadani2023 | 5 | youth_primary |
| barbic2005 | 3 | youth_primary |
| baumgartner2012 | 1 | youth_primary |
| beachy2004 | 5 | youth_primary |
| biagi2024 | 1 | youth_primary |
| blinkhorn2000 | 1 | youth_primary |
| bradshaw2024 | 1 | youth_primary |
| bratteberg2019 | 1 | youth_primary |
| caglar2005 | 1 | youth_primary |
| caglar2006 | 1 | youth_primary |
| caglar2010 | 1 | youth_primary |
| cetinbas2008 | 2 | youth_primary |
| chan2011 | 1 | youth_primary |
| chisholm2020 | 2 | youth_primary |
| cohenca2007 | 3 | youth_primary |
| collins2008 | 1 | youth_primary |
| collins2016 | 5 | youth_primary |
| comert2026 | 1 | youth_primary |
| danis2000 | 1 | youth_primary |
| emshoff1997 | 3 | youth_primary |
| fakhruddin2008 | 1 | youth_primary |
| farhadian2020 | 1 | youth_primary |
| faude2017 | 1 | youth_primary |
| finch2005 | 1 | youth_primary |
| gabris2001 | 1 | youth_primary |
| galic2018 | 5 | youth_primary |
| gardner2015 | 2 | youth_primary |
| gomez1996 | 1 | youth_primary |
| goswami2017 | 4 | youth_primary |
| goyal2017 | 1 | youth_primary |
| halabchi2007 | 1 | youth_primary |
| hamdan2026a | 1 | youth_primary |
| hamdan2026b | 1 | youth_primary |
| huang2009 | 1 | youth_primary |
| huffman2008 | 1 | youth_primary |
| isokungas2012 | 1 | youth_primary |
| jagger2009 | 2 | youth_primary |
| kanemitsu2023 | 3 | youth_primary |
| kaplan2022 | 2 | youth_primary |
| kerr2008 | 2 | youth_primary |
| kovacs2012 | 1 | youth_primary |
| kroon2016 | 1 | youth_primary |
| labella2002 | 2 | youth_primary |
| levin2003 | 3 | youth_primary |
| levin2007 | 1 | youth_primary |
| liang2023 | 1 | youth_primary |
| liang2024 | 1 | youth_primary |
| lin2008 | 1 | youth_primary |
| mertz2022 | 3 | youth_primary |
| molina2008 | 1 | youth_primary |
| montero2019 | 1 | youth_primary |
| nahas2021 | 1 | youth_primary |
| naidoo2009 | 1 | youth_primary |
| neiss2013 | 22 | youth_primary |
| neiss2014 | 19 | youth_primary |
| neiss2015 | 19 | youth_primary |
| neiss2016 | 22 | youth_primary |
| neiss2017 | 22 | youth_primary |
| neiss2018 | 21 | youth_primary |
| neiss2019 | 18 | youth_primary |
| neiss2021 | 20 | youth_primary |
| neiss2022 | 21 | youth_primary |
| neiss2023 | 21 | youth_primary |
| neiss2024 | 22 | youth_primary |
| neiss2025 | 23 | youth_primary |
| nicolau2001 | 1 | youth_primary |
| nonoyama2016 | 4 | youth_primary |
| omalley2012 | 1 | youth_primary |
| ozbay2013 | 1 | youth_primary |
| pandey2025 | 1 | youth_primary |
| park2021 | 1 | youth_primary |
| pasternack1996 | 1 | youth_primary |
| pattussi2006 | 1 | youth_primary |
| pierrot2021 | 2 | youth_primary |
| pribble2004 | 1 | youth_primary |
| quarrie2020 | 7 | adult_comparator, youth_primary |
| qudeimat2019 | 1 | youth_primary |
| rattai2018 | 1 | youth_primary |
| rugby_europe_iss_2024 | 8 | youth_primary |
| sgancohen2008 | 1 | youth_primary |
| shimizu2023 | 1 | youth_primary |
| shirani2010 | 1 | youth_primary |
| shore2021 | 1 | youth_primary |
| shore2023 | 1 | youth_primary |
| singh2014 | 2 | youth_primary |
| skaare2003 | 1 | youth_primary |
| slavin2021 | 1 | youth_primary |
| stanbouly2021 | 3 | youth_primary |
| stanbouly2022c | 1 | youth_primary |
| stewart2009 | 4 | youth_primary |
| stewart2011 | 1 | youth_primary |
| stuart2002 | 3 | youth_primary |
| tiwari2014 | 2 | youth_primary |
| tsuchiya2017 | 3 | youth_primary |
| tyler2026 | 3 | youth_primary |
| udayamalee2024 | 2 | youth_primary |
| van2021 | 1 | youth_primary |
| welch2010 | 10 | youth_primary |
| wong2004 | 1 | youth_primary |
| wright2007 | 2 | youth_primary |
| zaleckiene2020 | 2 | youth_primary |
| zamoraolave2020 | 1 | youth_primary |
| zendler2021 | 1 | youth_primary |