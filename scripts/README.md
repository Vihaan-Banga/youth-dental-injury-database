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

Downloads NEISS data for years 2000–present, filters for sports-related dental/orofacial injuries. NEISS data is available at:
https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data

The site provides annual CSV files. The script:
1. Downloads each year's CSV to `data/raw/neiss/`
2. Filters for body part codes: 76 (mouth), 77 (lower face/jaw), 88 (face) — verify codes against NEISS coding manual
3. Filters for sport-related product codes (basketball = 1205, football = 1211, etc.)
4. Outputs filtered subset to `data/extracted/neiss_dental_sports.csv`

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
