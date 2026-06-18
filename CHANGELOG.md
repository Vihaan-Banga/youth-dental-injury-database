# Changelog

All notable changes to the Youth Sports Dental Injury Database are documented here. The format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/) once we reach v1.0. Pre-1.0 versions are timeline snapshots.

## [Unreleased]

(Working state on `main`. Will become v0.1.0 at the next tag.)

### 2026-06-16 — Author-attribution integrity repair

#### Fixed
- **Corrected fabricated author attributions across 67 of 93 PubMed sources.** An audit found the AI-assisted extractions had copied paper titles correctly but invented author names (e.g. `williams2024`→ actually Liang & Chuang; `collins2004`→ Beachy; `radelet1996`→ Pasternack; `benson2002`→ Stuart). Rebuilt every `source_id` + `citation` from the authoritative PubMed abstract metadata. Audit (`scripts/34`) now reports **0 author/year mismatches**; re-running the extraction scripts reproduces `master.csv` byte-for-byte. See `docs/decisions.md` 2026-06-16.

#### Added
- `scripts/34_audit_citations.py` — reusable citation/author audit against cached PubMed abstracts (run before releases).
- `scripts/35_fix_attributions.py`, `scripts/36_fix_batch_script_attributions.py` — the one-time repair (data + scripts).
- `scripts/37_audit_numbers.py` + `outputs/number_audit.md` — sanity-checks extracted numeric values (counts, rates, sample sizes, mouthguard use) against the source abstract. 80% corroborate in-abstract; the rest are flagged for full-text review (full-text-table values, or computed figures such as back-calculated `injury_count`s). Not a pass/fail — a reviewer aid.

#### Changed
- `scripts/26_bibliography.py` — BibTeX keys now parsed from `docs/sources.md` (was a hardcoded map that carried the wrong ids).
- `scripts/03_apply_screening_to_sources.py` — `source_id`s are ASCII-folded (e.g. `omalley2012`, `gabris2001`) for valid filenames/BibTeX keys.
- C11 rate blanking (2026-06-13) encoded into `scripts/19` and `scripts/20` so it survives re-extraction.

### 2026-06-12 — full-text review of the open-access `needs_additional_review` subset

#### Added
- `scripts/30_oa_url_lookup.py` + `outputs/needs_additional_review_oa_urls.csv` — Unpaywall best-OA-URL lookup for all 91 `needs_additional_review` records (24 have a free URL).
- `scripts/31_pmc_availability.py` + `outputs/needs_additional_review_pmc.csv` — PubMed→PMC lookup (8 have free PMC full text).
- `scripts/32_extract_halabchi2007.py` + `data/extracted/halabchi2007.csv` — new included source: **halabchi2007** (women's Shotokan karate championships, Iran; 3 dental avulsion/subluxation of 186 injuries). First Iran source and first `martial_arts_other` row from a dedicated study.
- `outputs/needs_additional_review_fulltext_review_2026-06-12.md` — audit log of every fetch attempt and per-record decision.

#### Changed
- `needs_additional_review` pile **91 → 84**: 1 record promoted to `included`/`extracted`, 6 `fulltext_excluded` (E-age ×4, E-offtop, E-nodent). Logged in `docs/decisions.md` and `scripts/screening_overrides.py`.
- `data/harmonized/master.csv` **425 → 426 rows**, **105 → 106 sources**; SQLite, bibliography (93 → 94), country breakdown, sport factsheets, and figures regenerated. Validator: 0 FAILs / 0 WARNs.
- `scripts/26_bibliography.py` — now includes full-text-promoted `included` records, not just `screened_included`.
- `scripts/03_apply_screening_to_sources.py` — screening-summary percentages now use the real denominator (was a hardcoded `/200`, producing a >100% figure) and list the `included`/`extracted`/`fulltext_excluded` statuses.

### Added
- GitHub Pages site at https://vihaan-banga.github.io/youth-dental-injury-database/ (Jekyll, theme `minima`).
- `outputs/sources_bibliography.bib` — BibTeX file with 93 included PubMed sources + 5 governing-body @misc entries.
- `data/harmonized/master.sqlite` — SQLite export of `master.csv` for easier querying (487 KB). With sample queries in `data/harmonized/README_sqlite.md`.
- `CONTRIBUTING.md` — contribution guidelines.
- `CHANGELOG.md` (this file).

## 2026-05-25 — pre-v0.1 working snapshot

### Added
- **NEISS coverage expanded to 12 treatment years** (2013–2019, 2021–2025) after user manually downloaded 2018–2019 and 2021–2025 from CPSC. 2020 returned no matching cases (real COVID-era youth-sport gap). 6 new per-year extractions: `neiss2018`, `neiss2019`, `neiss2021`, `neiss2022`, `neiss2024`, `neiss2025`.
- `outputs/neiss_trends.md` + 3 trend figures — first published 12-year aggregation of NEISS youth dental-sport data.
- `outputs/cross_source_rate_comparison.md` + figure — internal consistency check.
- `outputs/methods_paper_draft.md` — Scientific Data data-descriptor skeleton.
- `outputs/sport_factsheets/` — 19 per-sport one-pagers.
- GitHub Actions CI at `.github/workflows/validate.yml` — runs validator on every push and PR.
- 10 more PubMed bulk extractions (batch 6): `collins_neiss2019`, `kaplan2022`, `rajan2021`, `ekanayake2021`, `dafnis_soccer2021`, `basketball_craniofacial2021`, `chisholm2020`, `alkilzy2019`, `otsuru2016`, `kanagasingam2016`.

### Changed
- All 20 scripts now use `Path(__file__).resolve().parent.parent` for ROOT — portable across machines / CI.
- `wormald2022` rates moved from `rate_per_1000_ae` to `rate_raw` after cross-source analysis revealed they were per-AE-HOURS not per-AE. Documented as a project-wide rule.

### Fixed
- `headline_snapshot.png` rendering — earlier version was blank for some viewers; switched to explicit axis limits.

## 2026-05-24 — sport-taxonomy expansion

### Added
- 19 new sport taxonomy entries: cricket, netball, cycling, mountain_biking, hurling, kabaddi, gaelic_football_mens, gaelic_football_womens, australian_rules_football, skiing, snowboarding, equestrian, inline_skating, crossfit, kickboxing, muay_thai, judo, handball, floorball.
- Rugby Europe 2024 U-18 PDF extraction.
- 12 more PubMed bulk extractions across 5 batches.
- 8 baseline visualization PNGs.
- `CITATION.cff` for GitHub "Cite this repository" button.

### Changed
- NEISS filter (`scripts/05_neiss_filter.py`) now also accepts `Body_Part_2 = 88` (Mouth as secondary body part — column added by NEISS in 2019). Recovered ~15% more cases per applicable year.

## 2026-05-23 — repo publication + extractions

### Added
- Repo published publicly on GitHub.
- `exposure_context` + `subgroup_label` columns to data dictionary (option A from previous schema todo).
- 11 RIO summary report PDFs (2008-09 through 2023-24, 2 from state-association mirrors).
- 132 new PubMed candidates via 5 journal-restricted searches (Dent Traumatol, Pediatr Dent, AJSM, BJSM, J Athl Train).
- Adult-comparator scope decision implemented (`extraction_basis` column).
- 3 abstract-only extractions: `azadani2023`, `quarrie2020`, `welch2010`.
- Initial NEISS pipeline (filter + 2023 extraction + hadley 2013-2017 archive).

## 2026-05-22 — schema-gap fixes

### Added
- 11 governing-body PDFs catalogued.
- First pilot extractions: `collins2016`, `labella2002`, `stewart2009`.

## 2026-05-21 — project initialization

### Added
- Git repo initialized.
- PubMed seed search via NCBI E-utilities — 200 candidates.
- AI-assisted screening of all 200 against PROTOCOL §3.1–3.3.
- NEISS body-part codes verified against 2024 NEISS Coding Manual (corrected protocol's incorrect labels for codes 76/77/88).
- Initial scripts: harmonize, validate, screen.
