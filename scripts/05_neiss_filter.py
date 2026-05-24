#!/usr/bin/env python3
"""Filter a NEISS annual file (TSV/CSV) down to sport-related youth dental
injuries per PROTOCOL §3.1 and the corrected NEISS code map (docs/decisions.md
2026-05-21 entry).

CPSC does not publish stable direct URLs for NEISS annual files — they are
accessible only via the on-line query builder at
https://www.cpsc.gov/cgibin/NEISSQuery/UserCriteria.aspx. The script therefore
expects a manually-downloaded file in `data/raw/neiss/neiss_<year>.tsv`. See
the README under `data/raw/neiss/README.md` for step-by-step download
instructions.

Filter logic (verified against the 2024 NEISS Coding Manual, Appendix C and
Appendix H — see docs/decisions.md):

  body_part == 88                                  # Mouth (incl. teeth) — primary
   OR (body_part == 76 AND diagnosis indicates       # Face — only when dental
                            dental involvement)      #    involvement per §3.3
  AND product_1 ∈ SPORT_PRODUCT_CODES               # 23 sport codes
  AND 5 ≤ age ≤ 22                                 # NEISS quirk: ages <2y are
                                                     #    coded as 200+months;
                                                     #    we exclude those.
Output one row per matched NEISS case to:
    data/extracted/neiss_dental_sports_<year>.csv
plus a single combined master at:
    data/extracted/neiss_dental_sports_all.csv

This is the *filtering* half. Mapping to DATA_DICTIONARY columns happens in
a separate extraction step (TODO: scripts/07_neiss_to_extraction.py) so the
raw filtered output retains all NEISS columns for QA.
"""

import argparse
import csv
import re
from pathlib import Path

ROOT = Path("/Users/vihaanbanga/youth-dental-injury-database")
RAW_DIR = ROOT / "data/raw/neiss"
OUT_DIR = ROOT / "data/extracted"

# Body-part codes (per 2024 NEISS Coding Manual, Appendix C)
PRIMARY_BODY_PART = "88"             # Mouth (incl. teeth)
SECONDARY_BODY_PART = "76"           # Face — only with dental dx

# NEISS sport product codes (per Appendix H — see docs/decisions.md for the
# full mapping to the project's `sport` controlled vocabulary).
SPORT_PRODUCT_CODES = {
    "1205": ("basketball",         "limited_contact"),
    "1207": ("boxing",             "contact"),
    "1211": ("football_american",  "contact"),
    "1215": ("lacrosse_mens",      "contact"),    # see decisions.md note re: disambiguation
    "1266": ("volleyball",         "non_contact"),
    "1267": ("football_association","limited_contact"),
    "1270": ("wrestling",          "contact"),
    "1272": ("gymnastics",         "non_contact"),
    "1279": ("hockey_ice",         "contact"),
    "1295": ("hockey_field",       "limited_contact"),
    "1333": ("skateboarding",      "limited_contact"),
    "3234": ("rugby",              "contact"),
    "3245": ("hockey_street",      "limited_contact"),  # provisional taxonomy
    "3254": ("cheerleading",       "limited_contact"),
    "3257": ("martial_arts_other", "contact"),
    "3272": ("hockey_unspecified", ""),                  # needs case-by-case review
    "3274": ("swimming",           "non_contact"),
    "3276": ("water_polo",         "contact"),
    "3284": ("tennis",             "non_contact"),
    "5030": ("track_and_field",    "non_contact"),
    "5032": ("hockey_roller",      "limited_contact"),   # provisional taxonomy
    "5034": ("softball",           "limited_contact"),
    "5041": ("baseball",           "limited_contact"),
}

# Heuristic — when body_part==76, only keep cases whose Diagnosis text or
# Narrative mentions a tooth/dental term. Conservative to avoid sweeping in
# eye-area-only injuries that happen to land in code 76.
DENTAL_DX_PATTERNS = re.compile(
    r"\b(tooth|teeth|dental|avuls|luxat|crown\s+fract|root\s+fract|incisor|"
    r"molar|canine|enamel|dentin|pulp|denture|orthodont|jaw\s+fract|"
    r"alveolar|mandibul|maxill)",
    re.IGNORECASE,
)


def is_in_age_range(age_raw: str) -> bool:
    """NEISS quirk: ages under 2 are coded as 200+months (e.g., 213 = 13 mo).
    Return True iff age in [5,22] in completed years.
    """
    try:
        age = int(age_raw)
    except (TypeError, ValueError):
        return False
    if age >= 200:
        return False  # under 2 — always below the 5 floor
    return 5 <= age <= 22


def likely_dental(diag_text: str, narrative_text: str) -> bool:
    """Used only when body_part == 76. Body part 88 already implies the mouth."""
    if not diag_text and not narrative_text:
        return False
    return bool(DENTAL_DX_PATTERNS.search(f"{diag_text} {narrative_text}"))


def find_column(headers, *candidates):
    """Resolve a column name regardless of NEISS's variable casing/spacing."""
    norm = {h.strip().lower().replace("_", " ").replace("-", " "): h for h in headers}
    for cand in candidates:
        key = cand.lower().replace("_", " ").replace("-", " ")
        if key in norm:
            return norm[key]
    raise KeyError(f"No column matches any of {candidates} in {headers}")


def detect_delimiter(path: Path) -> str:
    with path.open(encoding="utf-8", errors="replace") as f:
        first = f.readline()
    if "\t" in first:
        return "\t"
    if "," in first:
        return ","
    return "\t"  # NEISS default is tab-delimited


def filter_file(in_path: Path, out_path: Path) -> dict:
    """Filter a single NEISS annual file. Returns counter dict."""
    delim = detect_delimiter(in_path)
    with in_path.open(encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f, delimiter=delim)
        headers = reader.fieldnames or []
        col_body_part = find_column(headers, "Body_Part", "body_part_1", "body part 1", "body part")
        # Body_Part_2 was added to NEISS in 2019 — may not exist in older files
        try:
            col_body_part_2 = find_column(headers, "Body_Part_2", "body_part_2", "body part 2")
        except KeyError:
            col_body_part_2 = None
        col_product_1 = find_column(headers, "Product_1", "product_1", "product 1")
        col_age = find_column(headers, "Age")
        col_diagnosis = find_column(headers, "Diagnosis", "Diagnosis_1", "diagnosis 1")
        col_narrative = None
        for c in ("Narrative", "Narrative_1", "narrative_1", "narrative"):
            if c in headers:
                col_narrative = c
                break

        kept_rows = []
        counts = {"total": 0, "kept_88_primary": 0, "kept_88_secondary": 0, "kept_76": 0,
                  "rejected_body": 0, "rejected_product": 0,
                  "rejected_age": 0, "rejected_76_no_dental": 0}
        for row in reader:
            counts["total"] += 1
            bp = (row.get(col_body_part) or "").strip()
            bp2 = (row.get(col_body_part_2) or "").strip() if col_body_part_2 else ""
            prod = (row.get(col_product_1) or "").strip()
            age = (row.get(col_age) or "").strip()
            dx = (row.get(col_diagnosis) or "")
            narrative = (row.get(col_narrative) or "") if col_narrative else ""

            # Body-part criteria: primary = 88 (Mouth), OR
            #                     secondary = 88 (since 2019), OR
            #                     primary = 76 (Face) with dental-dx evidence
            body_keep = None
            if bp == PRIMARY_BODY_PART:
                body_keep = "primary_88"
            elif bp2 == PRIMARY_BODY_PART:
                body_keep = "secondary_88"
            elif bp == SECONDARY_BODY_PART:
                if likely_dental(dx, narrative):
                    body_keep = "primary_76_dental"
                else:
                    counts["rejected_76_no_dental"] += 1
                    continue
            else:
                counts["rejected_body"] += 1
                continue

            if prod not in SPORT_PRODUCT_CODES:
                counts["rejected_product"] += 1
                continue
            if not is_in_age_range(age):
                counts["rejected_age"] += 1
                continue

            sport, sport_cat = SPORT_PRODUCT_CODES[prod]
            row["__sport__"] = sport
            row["__sport_category__"] = sport_cat
            row["__body_part_label__"] = {
                "primary_88": "Mouth_primary",
                "secondary_88": "Mouth_secondary",
                "primary_76_dental": "Face_with_dental",
            }[body_keep]
            kept_rows.append(row)
            if body_keep == "primary_88":
                counts["kept_88_primary"] += 1
            elif body_keep == "secondary_88":
                counts["kept_88_secondary"] += 1
            else:
                counts["kept_76"] += 1

    if kept_rows:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        # Original NEISS columns + 3 derived columns
        out_headers = headers + ["__sport__", "__sport_category__", "__body_part_label__"]
        with out_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=out_headers, extrasaction="ignore")
            w.writeheader()
            w.writerows(kept_rows)
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?",
                    help="Path to a NEISS annual TSV/CSV (defaults: scan data/raw/neiss/)")
    ap.add_argument("--out", default=None,
                    help="Output CSV path (default: data/extracted/neiss_dental_sports_<basename>.csv)")
    args = ap.parse_args()

    if args.file:
        files = [Path(args.file)]
    else:
        files = sorted(p for p in RAW_DIR.glob("*.tsv")) + sorted(p for p in RAW_DIR.glob("*.csv"))
        files = [p for p in files if not p.name.startswith("_")]

    if not files:
        print(f"No NEISS annual files found in {RAW_DIR}.")
        print("Manual download steps:")
        print("  1. Go to https://www.cpsc.gov/cgibin/NEISSQuery/UserCriteria.aspx")
        print("  2. Choose User Affiliation, accept the data use agreement")
        print("  3. Filter Body Part = 'Mouth' (code 88) and optionally 'Face' (code 76)")
        print("  4. Filter Product = each sport code (1205, 1211, 1267, ... — see SPORT_PRODUCT_CODES)")
        print("  5. Set Age range 0–22 (we filter to 5–22 here; <2y NEISS codes need exclusion)")
        print("  6. Export as Tab-Delimited Text and save to data/raw/neiss/neiss_<year>.tsv")
        print()
        print("(Or, for 2013–2017 historical data, the hadley/neiss .rda file at")
        print(" data/raw/neiss/injuries_hadley_2013-2017.rda can be converted with R")
        print(" or pyreadr on a machine with sufficient memory/time.)")
        return

    grand_total = {"total": 0, "kept_88_primary": 0, "kept_88_secondary": 0, "kept_76": 0,
                   "rejected_body": 0, "rejected_product": 0,
                   "rejected_age": 0, "rejected_76_no_dental": 0}
    for in_path in files:
        stem = in_path.stem
        out_path = Path(args.out) if args.out else OUT_DIR / f"neiss_dental_sports_{stem}.csv"
        print(f"-> {in_path.name}")
        try:
            counts = filter_file(in_path, out_path)
        except KeyError as e:
            print(f"   SKIPPED — column resolution failed: {e}")
            continue
        for k, v in counts.items():
            grand_total[k] = grand_total.get(k, 0) + v
        kept = counts["kept_88_primary"] + counts["kept_88_secondary"] + counts["kept_76"]
        print(f"   {counts['total']:>7} rows -> {kept:>5} kept "
              f"({counts['kept_88_primary']} body1=88, "
              f"{counts['kept_88_secondary']} body2=88, "
              f"{counts['kept_76']} body=76+dental). "
              f"Output: {out_path.name}")
    print()
    print("TOTAL:", grand_total)


if __name__ == "__main__":
    main()
