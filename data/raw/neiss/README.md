# NEISS raw data

This directory holds raw NEISS annual files. CPSC does not publish stable direct download URLs for NEISS annuals (verified 2026-05-22 against the CPSC NEISS page and data.gov catalog entry), so files must be obtained one of two ways:

## Option A — CPSC Online Query (current data, manual, recommended)

1. Visit https://www.cpsc.gov/cgibin/NEISSQuery/UserCriteria.aspx
2. Select **User Affiliation** (e.g., "Student") and accept the data use agreement.
3. **Filters to apply** (one query per year, 2000 onward):
   - **Body Part:** check **88 Mouth** (and optionally **76 Face** — we filter `Face` cases downstream for dental involvement).
   - **Product:** check each sport code in `scripts/05_neiss_filter.py` `SPORT_PRODUCT_CODES` (1205 Basketball, 1207 Boxing, 1211 Football, 1215 Lacrosse, 1266 Volleyball, 1267 Soccer, 1270 Wrestling, 1272 Gymnastics, 1279 Ice hockey, 1295 Field hockey, 1333 Skateboards, 3234 Rugby, 3245 Street hockey, 3254 Cheerleading, 3257 Martial arts, 3272 Hockey NS, 3274 Swimming, 3276 Water polo, 3284 Tennis, 5030 Track & field, 5032 Roller hockey, 5034 Softball, 5041 Baseball).
   - **Age:** leave wide (we filter 5–22 downstream).
   - **Date range:** one calendar year per file.
4. Export as **Tab-Delimited Text** and save as `neiss_<year>.tsv` in this directory (e.g., `neiss_2023.tsv`).
5. Run `python3 scripts/05_neiss_filter.py` — it will scan the directory, filter each file, and write per-year and combined extractions to `data/extracted/neiss_dental_sports_<year>.csv`.

The body-part and product codes were verified against the **2024 NEISS Coding Manual** (Appendix C and Appendix H). See `docs/decisions.md` (entry 2026-05-21) for the verification record and a correction to PROTOCOL §4.1 (the protocol's printed body-part code labels are wrong; 88 = Mouth/teeth, not 76).

## Option B — hadley/neiss historical archive (2013–2017, programmatic)

The file `injuries_hadley_2013-2017.rda` (downloaded 2026-05-22 from https://github.com/hadley/neiss/blob/master/data/injuries.rda) contains 5 years of NEISS data in R serialized format. Converting to CSV requires either:
- **R**: `R -e 'load("injuries_hadley_2013-2017.rda"); write.csv(injuries, "injuries_2013-2017.csv", row.names=FALSE)'`
- **Python**: `pyreadr.read_r("injuries_hadley_2013-2017.rda")` — note that pyreadr's pip wheels often fail on stock macOS; use `conda` if pip fails. The pure-Python `rdata` package can also read it but is slow (10+ min on 72MB).

Once converted, drop the resulting `injuries_2013-2017.csv` here and run the filter script.

## What does NOT go in this directory (gitignored)

Per `.gitignore`, `*.csv`, `*.zip`, and `*.tsv` files in this directory are excluded from git so we don't accidentally commit large raw datasets that are re-downloadable from CPSC. The `.rda` file IS committed because it is small enough and is the only historical archive we depend on.

## What goes in this directory (committed)

- This `README.md`
- `_reference/` — copies of the NEISS Coding Manual PDFs (when downloaded)
- The hadley `.rda` archive (until we have a script that downloads it on demand)
