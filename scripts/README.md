# Scripts

Python scripts for downloading, extracting, and harmonizing source data.

## Setup

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# venv\Scripts\activate    # On Windows

# Install dependencies
pip install -r requirements.txt
```

Recommended dependencies (to add to `requirements.txt` when needed):
- `pandas` — data manipulation
- `requests` — HTTP downloads
- `pdfplumber` — extracting tables from PDFs
- `openpyxl` — reading Excel files (some surveillance data)
- `pyyaml` — config files

## Scripts (planned)

Scripts will be created as needed during the extraction and harmonization phases. The naming convention is:

- `01_*` — Download scripts (pull data from external sources)
- `02_*` — Extraction helpers (parse PDFs, structured data)
- `03_*` — Cleaning scripts (per-source cleaning)
- `04_*` — Harmonization (combining and standardizing)
- `05_*` — Validation (QA checks)
- `06_*` — Output generation (figures, tables for the paper)

## Initial scripts to write (in order)

### `01_neiss_download.py`

Downloads NEISS data for years 2000–present, filters for sports-related dental/orofacial injuries. NEISS landing page:
https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data

**Note on access:** CPSC does not publish stable direct URLs for annual files. Two options:
- Use the on-line query system (https://www.cpsc.gov/cgibin/NEISSQuery/) and pull tab-delimited exports by year. This is the canonical path but is interactive.
- Use the archived annual data mirror on DataLumos (https://www.datalumos.org/datalumos/project/230963/view) for years up to the most recent archive. Acceptable as a programmatic source provided we cite the mirror.

The script should:
1. Download each year's tab-delimited file to `data/raw/neiss/neiss_<year>.tsv`
2. Cache the coding manual under `data/raw/neiss/_reference/coding_manual_<year>.pdf`
3. Filter rows by:
   - `Body_Part == 88` (Mouth, including teeth) — primary filter
   - `Body_Part == 76` (Face) — secondary filter, AND `Diagnosis` / narrative indicates dental involvement
   - `Product_1 IN {1205, 1207, 1211, 1215, 1266, 1267, 1270, 1272, 1279, 1295, 1333, 3234, 3245, 3254, 3257, 3272, 3274, 3276, 3284, 5030, 5032, 5034, 5041}` (verified 2026-05-21; see `docs/decisions.md` for full code-to-sport mapping)
   - `Age` between 5 and 22 (NEISS codes <2y old as 200+age_in_months — handle that quirk)
4. Output filtered subset to `data/extracted/neiss_dental_sports.csv` using `DATA_DICTIONARY.md` column names

**The body-part codes in PROTOCOL.md §4.1 are incorrect** (76/77/88 are mislabeled). The correct codes above come from the 2024 NEISS Coding Manual Appendix C, verified 2026-05-21. See `docs/decisions.md` for the correction entry.

### `02_pdf_extract.py`

Helper for extracting tables from peer-reviewed PDFs in `data/raw/papers/`. Uses `pdfplumber` to pull tables, with manual review required for each.

This is *not* fully automated — many papers have non-standard table formats. The script provides a UI/CLI for working through papers one at a time, extracting tables into a template that matches `DATA_DICTIONARY.md`.

### `03_harmonize.py`

Reads all files in `data/extracted/`, applies the standardization rules from `PROTOCOL.md` and `docs/decisions.md`, and writes `data/harmonized/master.csv`.

Validates against `DATA_DICTIONARY.md` — fails loudly if any column is wrong type or any required column is missing.

### `04_validate.py`

QA script. Runs after harmonization. Checks:
- All `source_id`s are unique within each source
- All `sport` values are in the controlled vocabulary
- All `rate_per_1000_ae` values are non-negative and plausible (<100)
- All categorical columns contain only documented values
- Reports any rows flagged `review_needed`

Run before every version release.

---

## When to write a script vs. do it manually

For this project, most extraction is manual reading of PDFs and copying tables. Scripts help with:
- Bulk operations (downloading NEISS by year)
- Standardization (applying sport taxonomy)
- Validation (catching inconsistencies)

Do not over-engineer. A one-time data download doesn't need a polished script — a working Python file with comments is fine.
