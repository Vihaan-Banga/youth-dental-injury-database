# Contributing to the Youth Sports Dental Injury Database

Thanks for your interest. This database is the work of one student-led project so far; suggestions, corrections, and additions are welcome.

## Quick contribution paths

### Found a wrong row?

Open an issue with:
- The `source_id` and `pub_year`
- The row's content (paste the line from `master.csv`)
- The correct value, with the source citation

I'll verify against the original publication, log the correction in `docs/decisions.md`, and amend.

### Suggesting a source we missed?

Open an issue with:
- PMID or DOI
- Why it fits PROTOCOL §3.1–3.3 (study population aged 5–22, sport-related, dental or orofacial-with-dental outcome)
- Any quantitative data you've noticed in the abstract

I'll add it to `docs/sources.md` with status `identified`, screen it against the protocol criteria, and extract it if it passes.

### Adding a source yourself

1. Fork the repo.
2. Add the citation to `docs/sources.md` with status `screened_included`.
3. Read the source's abstract (or full text if available) and create `data/extracted/<source_id>.csv` following the schema in `DATA_DICTIONARY.md`. Use an existing extraction (e.g., `data/extracted/labella2002.csv`) as a template.
4. Run `python3 scripts/07_harmonize.py` to regenerate `master.csv`.
5. Run `python3 scripts/08_validate.py` — fix any FAILs.
6. Open a PR. CI will re-run the validator on your branch.

The CI workflow at `.github/workflows/validate.yml` runs on every push and PR. Don't merge if the validator fails.

## Pipeline overview

| script | what it does | when to run |
|---|---|---|
| `00_pubmed_seed_sources.py` | Run main PubMed query, seed `docs/sources.md` | once per major source-discovery round |
| `01_parse_abstracts.py` | Parse PubMed efetch XML into per-PMID JSON | after a new efetch |
| `02_screen_candidates.py` | Apply auto rules + manual overrides | after adding to `screening_overrides.py` |
| `03_apply_screening_to_sources.py` | Rewrite `docs/sources.md` from decisions | after any screening change |
| `04_write_screening_report.py` | Update `outputs/screening_report_*.md` | after any screening change |
| `05_neiss_filter.py` | Filter manually-downloaded NEISS TSV → CSV | after dropping a new TSV in `data/raw/neiss/` |
| `07_harmonize.py` | Combine `data/extracted/*.csv` → `master.csv` | after any new extraction |
| `08_validate.py` | Run 10 validation checks | after harmonization |
| `18_visualize.py` | Regenerate baseline figures | after major data updates |
| `21_cross_source_compare.py` | Cross-source rate comparison | after any new sport extraction |
| `22_neiss_extract_all_years.py` | Split multi-year NEISS files into per-year extractions | after running 05 on new years |
| `23_neiss_trends.py` | NEISS year-over-year trends | after new NEISS year |
| `24_sport_factsheets.py` | Per-sport one-pagers | after major data updates |
| `26_bibliography.py` | BibTeX export of included sources | as needed |
| `27_sqlite_export.py` | SQLite export of `master.csv` | after major data updates |

## Style notes

- **Decisions log**: every non-mechanical harmonization choice goes in `docs/decisions.md` as an append-only entry, dated.
- **Protocol edits**: `PROTOCOL.md` is the pre-registered research protocol. Changes to methodology must be logged in `docs/decisions.md` first; protocol text edits should follow advisor sign-off when possible.
- **Source IDs**: format `<firstauthor><year>` for PubMed-keyed sources (`collins2016`, `labella2002`); `<system><year>` for surveillance (`neiss2023`, `rio2018_19`); add `a`, `b` suffix for collisions.
- **Extraction notes**: always populate `extraction_notes` with anything not obvious from the row itself (e.g., back-calculated values, denominator caveats, age-band overlap concerns).
- **Quality flag**: `clean` only when extracted from full text and all fields confirmed. `partial_data` for abstract-only or otherwise incomplete. `review_needed` for ambiguous cases.

## Schema additions

If you need a new column in the data dictionary:
1. Add the column definition to `DATA_DICTIONARY.md` with type, allowed values, and rationale.
2. Add it to the `EXPECTED_COLUMNS` list in `scripts/07_harmonize.py`.
3. If categorical, add it to the validator's `ALLOWED` dict in `scripts/08_validate.py`.
4. Backfill or document handling for existing rows.

If you need a new sport in the taxonomy: add it to the `docs/decisions.md` "Sport taxonomy" table at the top of file AND to `scripts/08_validate.py`'s `ALLOWED_SPORTS` set. Cite the source that prompted it.

## Code of conduct

This is a student-led research project. Be respectful in discussions. Disagreements about methodology should be raised in issues, not in commit messages. If a correction reflects on an extraction someone else did, frame it as "improving the record" not "calling out a mistake."

## Licenses

Code under MIT (see `LICENSE`). Data under CC BY 4.0 (see `LICENSE-DATA`). Contributing implies you have the right to release your contribution under these terms.
