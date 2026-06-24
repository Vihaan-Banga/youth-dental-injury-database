#!/usr/bin/env python3
"""Validate `data/harmonized/master.csv` against DATA_DICTIONARY.md.

Checks:
  C1. Every required column present (schema)
  C2. Every categorical column contains only documented values
  C3. Numeric fields are non-negative and within plausible ranges:
        - rate_per_1000_ae:    0 ≤ x < 100 (PROTOCOL §7 plausibility cap)
        - rate_raw:            0 ≤ x         (raw can be in any denominator)
        - age_min, age_max:    0 ≤ x ≤ 130
        - athlete_exposures:   0 ≤ x
        - injury_count:        0 ≤ x
        - mouthguard_use_rate: 0 ≤ x ≤ 1
  C4. age_min ≤ age_max
  C5. age_category is consistent with age_min/age_max bands
        (youth: 5–12; adolescent: 13–17; collegiate: 18–22; adult: 23+; mixed/unspecified accepted)
  C6. extraction_basis = adult_comparator iff age_category = adult
  C7. sport values in the controlled vocabulary OR flagged in extraction_notes
        as an aggregate/non-sport row
  C8. quality_flag in allowed set
  C9. Every row's source_id appears at least once with extraction_basis = youth_primary
        (catches sources where we accidentally extracted only adult rows from a youth-eligible source)
  C10. No duplicate (source_id, sport, age_category, sex, level_of_play, extraction_basis,
       season_or_timeframe) combinations — surfaces accidental re-extractions
  C11. rate_per_1000_ae is populated only when rate_denominator_raw names an
       athlete-exposure denominator (not hours / season / population / % of injuries)
  C12. measure_type populated + in controlled vocabulary; comparability_group populated
  C13. data_provenance populated + in controlled vocabulary

Output: outputs/validation_report.md with per-check counts and any failing rows.
Exit code 0 if all hard checks pass (any C5/C9 mismatches surface as warnings,
not failures, since the schema is intentionally permissive for the pilot phase).
"""

import csv
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from _derived_columns import MEASURE_TYPES, DATA_PROVENANCE

# Resolve relative to this script so it works on any machine / CI.
ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data/harmonized/master.csv"
REPORT = ROOT / "outputs/validation_report.md"

EXPECTED_COLUMNS = [
    "source_id", "citation", "doi", "pub_year", "study_type", "peer_reviewed",
    "country", "region", "population_setting",
    "age_min", "age_max", "age_category", "extraction_basis",
    "sex", "level_of_play",
    "sport_raw", "sport", "sport_category", "exposure_context", "subgroup_label",
    "sample_size", "athlete_exposures", "season_or_timeframe",
    "injury_count", "injury_type_raw", "injury_category",
    "rate_raw", "rate_denominator_raw", "rate_per_1000_ae",
    "mouthguard_required", "mouthguard_use_rate", "mouthguard_injury_relation",
    "extraction_date", "extractor", "extraction_notes", "quality_flag",
    # Derived at harmonization (scripts/07 via scripts/_derived_columns.py):
    "measure_type", "comparability_group", "data_provenance",
]

ALLOWED = {
    "study_type": {"surveillance", "cross_sectional", "cohort", "case_series",
                   "registry", "governing_body_report"},
    "peer_reviewed": {"TRUE", "FALSE", ""},
    "population_setting": {"school", "club", "recreational", "professional",
                           "mixed", "unspecified", ""},
    "age_category": {"youth", "adolescent", "collegiate", "adult", "mixed",
                     "unspecified", ""},
    "extraction_basis": {"youth_primary", "adult_comparator", ""},
    "sex": {"male", "female", "mixed", "unspecified", ""},
    "level_of_play": {"recreational", "school_jv", "school_varsity", "club",
                      "elite", "mixed", "unspecified", ""},
    "sport_category": {"contact", "limited_contact", "non_contact", ""},
    "exposure_context": {"all", "competition", "practice", "training", "other", ""},
    "injury_category": {"enamel_fracture", "crown_fracture", "root_fracture",
                        "luxation", "avulsion", "concussion", "other_dental",
                        "orofacial_with_dental", "unspecified_dental", ""},
    "mouthguard_required": {"yes", "no", "unspecified", ""},
    "mouthguard_injury_relation": {"analyzed", "mentioned_only", "not_addressed", ""},
    "quality_flag": {"clean", "assumption_made", "partial_data", "review_needed", ""},
}

# Controlled sport vocabulary plus accepted aggregate values.
# Last expanded 2026-05-24 (see docs/decisions.md "Sport taxonomy formally expanded").
ALLOWED_SPORTS = {
    # Original v0.1 vocabulary (PROTOCOL §6.1 / decisions.md 2026-05-22)
    "basketball", "football_american", "football_association",
    "hockey_ice", "hockey_field", "lacrosse_mens", "lacrosse_womens",
    "rugby", "wrestling", "boxing", "mma", "baseball", "softball",
    "volleyball", "tennis", "track_and_field", "swimming", "water_polo",
    "gymnastics", "cheerleading", "skateboarding", "martial_arts_other",
    # Provisional hockey variants (decisions.md 2026-05-21 NEISS section)
    "hockey_street", "hockey_roller", "hockey_unspecified",
    # Aggregate / non-sport-specific values (decisions.md 2026-05-22)
    "all_sports_aggregate", "all_activities_aggregate", "sports_aggregate",
    "recreational_mixed", "non_sport_setting",
    "sports_aggregate_unmapped",  # used when source's sport label has no v0.1 mapping yet
    # Sport taxonomy expansion (decisions.md 2026-05-24)
    "cricket", "netball",
    "cycling", "mountain_biking",
    "hurling", "kabaddi",
    "gaelic_football_mens", "gaelic_football_womens",
    "australian_rules_football",
    "skiing", "snowboarding",
    "equestrian", "inline_skating",
    "crossfit",
    "kickboxing", "muay_thai", "judo",
    "handball", "floorball",
    "",
}

# Numeric-field validation rules: (min, max_exclusive, allow_empty)
NUMERIC_RULES = {
    "age_min":            (0, 131, True),
    "age_max":            (0, 131, True),
    "athlete_exposures":  (0, 10**12, True),
    "injury_count":       (0, 10**8, True),
    "rate_raw":           (0, 10**6, True),
    "rate_per_1000_ae":   (0, 100, True),  # PROTOCOL §7 plausibility cap
    "mouthguard_use_rate":(0, 1.0001, True),
    "sample_size":        (0, 10**8, True),
    "pub_year":           (1800, 2100, True),
}


def parse_num(s):
    if s is None or s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return ("ERR", s)


# Denominators that disqualify a rate from the athlete-exposure scale.
_NON_AE_DENOM = ("hour", "season", "population", "per cent", "% of",
                 "person-year", "player-match", "match-hour", "player-hour",
                 "per 100 player", "players", "per child", "capita")
# Athlete-exposure family. athlete-session is the standard AE unit
# (1 athlete in 1 practice/game = 1 AE); see docs/decisions.md 2026-05-24.
_AE_DENOM = ("athlete-exposure", "athletic-exposure", "athlete exposure",
             "athlete-session", "athlete session")


def denom_is_ae(denom):
    """True iff `denom` (the rate_denominator_raw phrasing) is an
    athlete-exposure denominator, so rate_per_1000_ae may be populated."""
    d = (denom or "").lower()
    if any(bad in d for bad in _NON_AE_DENOM):
        return False
    if any(good in d for good in _AE_DENOM):
        return True
    return bool(re.search(r"\bae\b", d))  # e.g. "per 1000 AE (dental specifically)"


def main():
    if not MASTER.exists():
        print(f"ERROR: {MASTER} does not exist. Run 07_harmonize.py first.")
        sys.exit(2)

    with MASTER.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    findings = []  # list of (severity, check_id, message)
    def add(sev, cid, msg):
        findings.append((sev, cid, msg))

    # C1 — schema
    headers = list(rows[0].keys()) if rows else []
    if headers != EXPECTED_COLUMNS:
        missing = set(EXPECTED_COLUMNS) - set(headers)
        extra = set(headers) - set(EXPECTED_COLUMNS)
        if missing:
            add("FAIL", "C1", f"Missing columns: {sorted(missing)}")
        if extra:
            add("WARN", "C1", f"Extra columns (not in dictionary): {sorted(extra)}")

    # C2 — categorical values
    for col, allowed in ALLOWED.items():
        for i, r in enumerate(rows):
            v = r.get(col, "")
            if v not in allowed:
                add("FAIL", "C2", f"row {i+1}: {col}='{v}' not in {sorted(allowed)}")

    # C2b — sport vocabulary
    for i, r in enumerate(rows):
        sport = r.get("sport", "")
        if sport not in ALLOWED_SPORTS:
            add("FAIL", "C2", f"row {i+1}: sport='{sport}' not in controlled vocabulary")

    # C3 — numeric ranges
    for col, (lo, hi, _) in NUMERIC_RULES.items():
        for i, r in enumerate(rows):
            n = parse_num(r.get(col, ""))
            if n is None:
                continue
            if isinstance(n, tuple):
                add("FAIL", "C3", f"row {i+1}: {col} is not numeric: '{n[1]}'")
                continue
            if not (lo <= n < hi):
                add("FAIL", "C3", f"row {i+1}: {col}={n} outside plausible range [{lo}, {hi})")

    # C4 — age_min <= age_max
    for i, r in enumerate(rows):
        nmin = parse_num(r.get("age_min", ""))
        nmax = parse_num(r.get("age_max", ""))
        if isinstance(nmin, float) and isinstance(nmax, float) and nmin > nmax:
            add("FAIL", "C4", f"row {i+1}: age_min={nmin} > age_max={nmax}")

    # C5 — age_category consistency (warnings — categories are intentionally permissive)
    for i, r in enumerate(rows):
        cat = r.get("age_category", "")
        nmin = parse_num(r.get("age_min", ""))
        nmax = parse_num(r.get("age_max", ""))
        if cat in ("mixed", "unspecified", ""):
            continue
        if not (isinstance(nmin, float) and isinstance(nmax, float)):
            continue
        expected_for_band = {
            "youth": (5, 12),
            "adolescent": (13, 17),
            "collegiate": (18, 22),
            "adult": (23, 130),
        }
        lo, hi = expected_for_band.get(cat, (None, None))
        if lo is None:
            continue
        # Permissive: a row's age_min/age_max should overlap the category band but
        # may extend slightly past it (e.g., 'youth' for an 11-14 sample).
        overlap = max(0, min(nmax, hi) - max(nmin, lo))
        span = nmax - nmin
        if span > 0 and overlap / span < 0.5:
            add("WARN", "C5", f"row {i+1}: age_category='{cat}' "
                              f"({lo}-{hi}) overlaps <50% of row's age range "
                              f"({nmin:.0f}-{nmax:.0f}) — verify categorization")

    # C6 — adult_comparator iff age_category=adult
    for i, r in enumerate(rows):
        cat = r.get("age_category", "")
        basis = r.get("extraction_basis", "")
        if cat == "adult" and basis != "adult_comparator":
            add("WARN", "C6", f"row {i+1}: age_category='adult' but "
                              f"extraction_basis='{basis}' (expected 'adult_comparator')")
        if basis == "adult_comparator" and cat != "adult":
            add("WARN", "C6", f"row {i+1}: extraction_basis='adult_comparator' but "
                              f"age_category='{cat}' (expected 'adult')")

    # C9 — every source has at least one youth_primary row
    by_source = defaultdict(set)
    for r in rows:
        by_source[r["source_id"]].add(r.get("extraction_basis", ""))
    for sid, bases in by_source.items():
        if "youth_primary" not in bases:
            add("FAIL", "C9", f"source_id='{sid}' has no youth_primary row "
                              f"(found only: {sorted(bases)})")

    # C10 — duplicate row check (uniqueness key per DATA_DICTIONARY.md
    # "Exposure context and subgroup rows")
    seen = Counter()
    for r in rows:
        key = (r["source_id"], r["sport"], r["age_category"], r["sex"],
               r["level_of_play"], r["extraction_basis"],
               r.get("exposure_context", ""), r.get("subgroup_label", ""),
               r["season_or_timeframe"])
        seen[key] += 1
    for key, n in seen.items():
        if n > 1:
            add("FAIL", "C10", f"{n} rows share key {key} — true duplicate "
                                "(exposure_context + subgroup_label should already "
                                "disambiguate legitimate stratifications)")

    # C11 — rate_per_1000_ae is reserved for athlete-exposure denominators.
    # If the row carries a per-1000-AE value, rate_denominator_raw must name an
    # AE denominator (not hours/season/population/% of injuries).
    # See DATA_DICTIONARY.md and docs/decisions.md (2026-05-24, 2026-06-13).
    for i, r in enumerate(rows):
        if not r.get("rate_per_1000_ae", "").strip():
            continue
        denom = r.get("rate_denominator_raw", "")
        if not denom_is_ae(denom):
            add("FAIL", "C11", f"row {i+1}: rate_per_1000_ae is populated but "
                               f"rate_denominator_raw='{denom}' is not an "
                               f"athlete-exposure denominator — move the value to "
                               f"rate_raw and leave rate_per_1000_ae empty")

    # C12 — comparability columns populated and in vocabulary.
    # measure_type must be one of the controlled values; comparability_group
    # must be non-empty. See DATA_DICTIONARY.md and docs/decisions.md 2026-06-24.
    for i, r in enumerate(rows):
        mt = (r.get("measure_type") or "").strip()
        if not mt:
            add("FAIL", "C12", f"row {i+1}: measure_type is empty")
        elif mt not in MEASURE_TYPES:
            add("FAIL", "C12", f"row {i+1}: measure_type='{mt}' not in controlled vocabulary")
        if not (r.get("comparability_group") or "").strip():
            add("FAIL", "C12", f"row {i+1}: comparability_group is empty")
    n_pending = sum(1 for r in rows
                    if r.get("measure_type") == "unclassified_pending_review")
    if n_pending:
        add("WARN", "C12", f"{n_pending} rows are measure_type="
                           f"'unclassified_pending_review' — awaiting manual classification")

    # C13 — data_provenance populated and in vocabulary (redistribution-rights
    # clarity). See docs/decisions.md 2026-06-24.
    for i, r in enumerate(rows):
        dp = (r.get("data_provenance") or "").strip()
        if not dp:
            add("FAIL", "C13", f"row {i+1}: data_provenance is empty")
        elif dp not in DATA_PROVENANCE:
            add("FAIL", "C13", f"row {i+1}: data_provenance='{dp}' not in controlled vocabulary")

    # Generate report
    fails = [f for f in findings if f[0] == "FAIL"]
    warns = [f for f in findings if f[0] == "WARN"]
    review_needed = [r for r in rows if r.get("quality_flag") == "review_needed"]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    W = lines.append
    W(f"# Validation Report — {date.today().isoformat()}\n")
    W(f"_Run against `data/harmonized/master.csv` ({len(rows)} rows)._\n")
    W("## Summary\n")
    W(f"- Rows checked: **{len(rows)}**")
    W(f"- Distinct sources: **{len(by_source)}**")
    W(f"- FAILs: **{len(fails)}**")
    W(f"- WARNs: **{len(warns)}**")
    W(f"- Rows flagged `quality_flag=review_needed`: **{len(review_needed)}**\n")
    if fails:
        W("## ❌ FAILs\n")
        for _, cid, msg in fails:
            W(f"- **{cid}** — {msg}")
        W("")
    else:
        W("## ✅ No FAILs\n")
        W("All hard validation checks (schema, categorical values, numeric ranges, age consistency, source coverage) passed.\n")
    if warns:
        W("## ⚠️  WARNs (review, not blocking)\n")
        for _, cid, msg in warns:
            W(f"- **{cid}** — {msg}")
        W("")
    W("## Check reference\n")
    W("- **C1** schema completeness")
    W("- **C2** categorical values in dictionary")
    W("- **C3** numeric fields in plausible ranges (`rate_per_1000_ae` < 100 per PROTOCOL §7)")
    W("- **C4** `age_min ≤ age_max`")
    W("- **C5** `age_category` consistent with `age_min`/`age_max` (warning only)")
    W("- **C6** `extraction_basis = adult_comparator` iff `age_category = adult`")
    W("- **C7** `sport` in controlled vocabulary (`docs/decisions.md`)")
    W("- **C8** `quality_flag` in allowed set (covered by C2)")
    W("- **C9** every source has at least one `youth_primary` row")
    W("- **C10** no duplicate (source × sport × age × sex × level × basis × season) keys")
    W("- **C11** `rate_per_1000_ae` populated only when `rate_denominator_raw` is an athlete-exposure denominator")
    W("- **C12** `measure_type` populated and in the controlled vocabulary; `comparability_group` populated")
    W("- **C13** `data_provenance` populated and in the controlled vocabulary")
    W("\n## Per-source row count\n")
    W("| source_id | rows | bases |")
    W("|---|---|---|")
    for sid in sorted(by_source):
        n = sum(1 for r in rows if r["source_id"] == sid)
        W(f"| {sid} | {n} | {', '.join(sorted(by_source[sid])) or '(empty)'} |")
    REPORT.write_text("\n".join(lines))

    print(f"Wrote {REPORT.relative_to(ROOT)}")
    print(f"  rows: {len(rows)}; FAILs: {len(fails)}; WARNs: {len(warns)}")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
