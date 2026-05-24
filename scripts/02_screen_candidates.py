#!/usr/bin/env python3
"""Apply screening decisions to the 200 PubMed candidates and write
data/extracted/_screening/screening_decisions.csv.

This script combines two layers:
  1. Automatic rules (language, publication type) — deterministic.
  2. A manual override dictionary (`MANUAL_DECISIONS`) populated by the
     project lead / AI-assisted screener after reading abstracts.

Decisions follow PROTOCOL §4.4 status vocabulary:
  - screened_included         meets §3.1–3.3, queue for full-text
  - screened_excluded         fails ≥1 inclusion or hits an exclusion criterion
  - needs_human_review        ambiguous; final call requires the project lead
                              (and/or advisor) to read the full text

Confidence: high | medium | low. Anything below 'high' should be re-checked.

Reason codes (short tags used in sources.md):
  E-lang     non-English (§3.1)
  E-review   review/SR/MA — kept for source mining, not extracted (§3.2)
  E-case     single case report or small case series n<5 (§3.2)
  E-age      population outside 5–22 (§3.1) — adults only, military, etc.
  E-offtop   abstract not about sport-related dental/orofacial injury (§3.1/3.3)
  E-noprim   no extractable primary numerical data (§3.1)
  E-nodent   no dental/orofacial-with-dental outcome reported (§3.3)
  E-nonpr    non-peer-reviewed and not an approved surveillance/governing body source (§3.2)
  I-pri      primary study, sport-related dental injury, ages overlap 5–22
  R-age      age boundaries unclear / spans into adult — full-text needed
  R-mixed    mixed adult+youth, can't tell youth subset from abstract
  R-data     not obvious whether numerical injury counts are extractable
  R-other    other ambiguity (logged per case)
"""

import csv
import json
from pathlib import Path

ROOT = Path("/Users/vihaanbanga/youth-dental-injury-database")
ABS_DIR = ROOT / "data/raw/papers/_abstracts"
OUT_DIR = ROOT / "data/extracted/_screening"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Manual decisions populated after reading abstracts.
# Format: PMID (str) -> (decision, reason_code, confidence, note)
# decision in {"screened_included","screened_excluded","needs_human_review"}
MANUAL_DECISIONS: dict[str, tuple[str, str, str, str]] = {
    # Populated by 02_screen_candidates_decisions.py — see that file.
}

try:
    from screening_overrides import MANUAL_DECISIONS as _M
    MANUAL_DECISIONS.update(_M)
except ImportError:
    pass


def auto_decide(rec):
    """Apply deterministic rules. Returns (decision, reason, confidence, note) or None."""
    lang = rec.get("language", "")
    if lang and lang != "eng":
        return ("screened_excluded", "E-lang", "high",
                f"Language='{lang}' — English-only per PROTOCOL §3.1 v1.0 scope.")
    pts = rec.get("publication_types", [])
    if "Case Reports" in pts:
        return ("screened_excluded", "E-case", "high",
                "PubMed PublicationType 'Case Reports' — excluded per §3.2.")
    if any(p in pts for p in ("Systematic Review", "Meta-Analysis")):
        return ("screened_excluded", "E-review", "high",
                "Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.")
    if "Review" in pts:
        return ("screened_excluded", "E-review", "high",
                "Narrative review — kept for reference mining; not extracted per §3.2.")
    # Non-primary literature types that cannot supply extractable epi data.
    for non_primary, label in [
        ("Editorial", "Editorial"),
        ("Letter", "Letter to the editor"),
        ("Comment", "Comment / correspondence"),
    ]:
        if non_primary in pts:
            return ("screened_excluded", "E-noprim", "high",
                    f"{label} — no extractable primary numerical data (§3.1).")
    return None


def main():
    decisions = []
    for p in sorted(ABS_DIR.glob("*.json")):
        rec = json.load(open(p))
        pmid = rec["pmid"]
        auto = auto_decide(rec)
        if pmid in MANUAL_DECISIONS:
            d, code, conf, note = MANUAL_DECISIONS[pmid]
        elif auto:
            d, code, conf, note = auto
        else:
            d, code, conf, note = ("needs_human_review", "R-other", "low",
                                   "No manual decision recorded yet; review abstract.")
        decisions.append({
            "pmid": pmid,
            "pub_year": rec.get("pub_year", ""),
            "language": rec.get("language", ""),
            "journal": rec.get("journal", ""),
            "title": rec.get("title", ""),
            "publication_types": "|".join(rec.get("publication_types", [])),
            "decision": d,
            "reason_code": code,
            "confidence": conf,
            "note": note,
            "auto_or_manual": "manual" if pmid in MANUAL_DECISIONS else ("auto" if auto else "default"),
        })

    out_csv = OUT_DIR / "screening_decisions.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(decisions[0].keys()))
        w.writeheader()
        w.writerows(decisions)

    # Quick stats
    from collections import Counter
    by_dec = Counter(d["decision"] for d in decisions)
    by_code = Counter(d["reason_code"] for d in decisions)
    by_src = Counter(d["auto_or_manual"] for d in decisions)
    print(f"Wrote {out_csv} — {len(decisions)} rows")
    print("By decision:", dict(by_dec))
    print("By reason code:", dict(by_code))
    print("By source (auto/manual/default):", dict(by_src))


if __name__ == "__main__":
    main()
