# Overnight session summary — 2026-05-24

Worked from ~midnight on. Pushed 16 commits while you slept. Read this first.

## Bottom line

`data/harmonized/master.csv` went from **158 rows / 12 sources** to **256 rows / 73 sources** overnight. Still **0 FAILs, 0 WARNs**. Candidate pool went from 343 to 436. Pipeline is reproducible end-to-end; everything is on GitHub at https://github.com/Vihaan-Banga/youth-dental-injury-database.

## Status board

| metric | last night | this morning |
|---|---:|---:|
| master.csv rows | 158 | **256** |
| distinct sources extracted | 12 | **73** |
| candidate pool (PubMed) | 332 | **436** |
| screened_included (PubMed) | 78 | 73 |
| extracted (PubMed-keyed) | 6 | 21 |
| NEISS source-years | 6 (2013-17, 2023) | 6 (same) |
| validation FAILs | 0 | 0 |
| validation WARNs | 0 | 0 |
| countries represented | ~14 | 19 |

## What got done

**Quick wins (early in the session)**
- Fixed NEISS filter to also recover cases where Mouth is `Body_Part_2` (secondary body part). +87 cases in 2023 alone. master.csv 155→158.
- Added `CITATION.cff` — GitHub now shows a "Cite this repository" button on the repo home.
- PMC ID-converter run against all 81 included PubMed PMIDs → 16 new full-text XMLs fetched, now 22 PMC papers cached.

**Bulk extraction (the main work — 5 batches, 61 new sources, +98 rows)**
Each batch is a separate `scripts/14...19_extract_batchN.py` for reproducibility. Per-source CSVs in `data/extracted/`. All abstract-only, all marked `quality_flag = 'partial_data'`. Highlights by batch:
- **Batch 1 (12):** hamdan2026 (Syria 445 athletes 47.4% ODT), udayamalee2024 (Sri Lanka 1340 contact-sport adolescents), vanierssel2021 (9 Canadian peds EDs concussion+MG, n=1019), levin2003+levin2007 (Israel 943+427), goswami2017 (Delhi 450 kids), tsuchiya2017 (Miyagi 5735), singh2014 (N India 1105 HS), chan2011, cetinbas2008, shore2023, amy2005.
- **Batch 2 (11):** williams2024+williams2023 (NEISS basketball+soccer 20-yr), nasu2023 (Japan school HICBT 4495 cases), zaror2018 (4 contact sports per-sport rates), yard2015 (NCAA women's field hockey 0.94/1000 AE), naasan2021 (Lebanon 7902 national), cetin2026, mooney2021, azimi2020, calderon2020, deshpande2014.
- **Batch 3 (12):** trinidad2007 (USC intercollegiate basketball 10.6/100 athlete-seasons men), collins2004 (Punahou 15-yr per-sport AE rates), zazryn2010 (combat sports 18-25 — first paper triggering adult_comparator split), yard2008 (RIO RIC composite), naidoo2009, mahlangu2008, yildirim2013, mcevoy2012, mcdonough2008, mate2001, hosea1996, pattussi2006.
- **Batch 4 (14):** benson2002 (Junior A hockey 158.9 → 73.5 → 23.2 per 1000 player-game-hours by facial-protection level — clean dose-response), mcintosh2005 (RCT Ontario unis), collins_rugby2008 (collegiate rugby NE 22.5/22.7 per 1000 game AE m/f), fakhruddin2009, wong2008, livny2008, yamada2009 (schoolboy cricketers England/Australia), hayran2010, ivanovics2012, carter2000, marcenes2001, ranalli2005, ali2007, nalcaci2006.
- **Batch 5 (12):** wormald2022 (NCAA D-I 13 sports — 2.06/1000 AE-h overall, men's BB 8.30, men's water polo 8.15), alawawdeh2021+2022 (NEISS youth non-tackle football, NEISS martial arts 20-yr), collins_baseball2008 (HS baseball RIO), finch2005 (Aus football MG RCT), baek2021 (Pusan 5-yr), emshoff1997 (Innsbruck 10-yr mandibular fracture trends), radelet1996 (Little League 2861 players 140k player-hours), leite2012, alotaibi2014, danis2000, chapman2004.

**Search expansion**
- 5 more journal-restricted PubMed searches (J Endod, J OMFS, Pediatrics, Inj Prev, Orthop J Sports Med): 111 hits → 104 NEW → 12 promoted to includes, 90 manually classified (mostly E-offtop OMFS surgical / ortho papers). Two searches dominated: J OMFS (44) and Inj Prev (24).
- Auto-screen rules tightened: Editorial / Letter / Comment publication types now auto-exclude as `E-noprim`.

**International governing-body hunt**
- 4 PDFs identified and downloaded to `data/raw/surveillance_reports/_international/`:
  - World Rugby 2023 Annual Injury Surveillance Review (Medical Commission)
  - England PRISP 2022-23 (37 pages, professional rugby)
  - Rugby Europe 2024 (includes U-20 and U-18 championship data — directly in §3.1 scope)
  - Orchard AFL Comparison (methodology)
- Hockey Canada / USA Hockey / AFL annual reports — could not be directly fetched (player-facing claim forms only, or 403 to non-browser clients). Logged in `docs/governing_body_sources.md`.

**Visualizations**
- 8 baseline PNGs in `outputs/figures/`:
  - `headline_snapshot.png` (256 rows / 73 sources / 19 countries / cumulative injury count)
  - `rows_per_source_top20.png`, `sport_coverage.png`, `country_coverage.png`, `year_coverage.png`, `age_category_distribution.png`, `extraction_basis_split.png`, `injury_count_by_sport.png`
- matplotlib added to `scripts/requirements.txt`.

## What's actionable when you're back, in priority order

1. **Spot-check overnight extractions.** I extracted from abstracts only — the rows are honest about what was visible but you should sanity-check a few. Suggested sample: pick 3 random sources from `data/extracted/` and read the abstract JSON in `data/raw/papers/_abstracts/<PMID>.json` to compare against my row.
2. **Download more NEISS years** — same flow you used for 2023, but with "Most Recent 5 Years (2021-2025)" or "Date Range 2018-2022". Each year adds ~500-800 cases. The bug fix I made today already recovers ~15% more cases per year than the original filter did.
3. **Decide whether to extract from `data/raw/surveillance_reports/_international/*.pdf`.** Rugby Europe in particular has U-18/U-20 data that's directly in §3.1 scope.
4. **Look at the figures** in `outputs/figures/` and tell me which (if any) are useful for your Conrad submission / advisor outreach. I can iterate on them.
5. **Resume needs_human_review screening** — 91 records still pending your full-text review. Most are "age range not in abstract" calls.

## Schema / methodology decisions I made overnight

All logged in `docs/decisions.md`:
- Editorial/Letter/Comment publication types added to auto-exclude as `E-noprim`.
- Several sources had sports not in the §6.1 controlled vocabulary (cricket, cycling, skiing, equestrian, kabaddi, Gaelic football, Australian rules football). Pattern: `sport = all_sports_aggregate` / `sport_category = ""` / `subgroup_label = <descriptor>`. Taxonomy expansion deferred to advisor sign-off (decision dated 2026-05-23 already exists).
- zazryn2010 (combat sports 18-25) and amy2005 (multi-age games) used the adult_comparator extension — first sources to actually exercise the 2026-05-22 scope decision end-to-end.

## What's NOT done

- The remaining ~38 unextracted screened_included PubMed sources (most are very abstract-sparse or repetitive with already-extracted papers). Could extract on request.
- The 91 needs_human_review records — those genuinely need full-text retrieval, which mostly hits publisher paywalls.
- The 11 governing-body PDFs (RIO summary years + AAPD + the 4 international ones) — they're logged as `identified` but not extracted into master.csv. Would yield ~30-50 more rows.
- The `docs/decisions.md` proposed sport-taxonomy expansion (cricket, netball, hurling, kabaddi, etc.) is still pending your decision.

## Commits this session (chronological)

```
8ef6955  NEISS filter: recover cases where Mouth is Body_Part_2
2e39750  Add CITATION.cff
1c518b4  Fetch 16 more PMC full-text XMLs
39d6c6b  Bulk extraction batch 1 — 12 sources
c83d641  Bulk extraction batch 2 — 11 sources
cc96df0  Bulk extraction batch 3 — 12 sources
b880e86  Bulk extraction batch 4 — 14 sources
b31a71a  Add baseline visualizations
2034fc6  5 more journal-restricted searches (round 2)
46dd4d7  International governing-body hunt
2ee3c41  Bulk extraction batch 5 — 12 more sources
```

All pushed to `origin/main`. `gh repo view Vihaan-Banga/youth-dental-injury-database --web` will open the repo in your browser.
