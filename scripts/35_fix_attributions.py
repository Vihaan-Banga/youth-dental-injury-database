#!/usr/bin/env python3
"""Repair fabricated author attributions in the extracted sources.

Background (2026-06-16 audit, scripts/34): the AI-assisted batch extractions
copied paper TITLES correctly but invented AUTHOR names for ~66 of 93 PubMed
sources, and derived source_ids from those wrong authors (e.g. williams2024 /
"Williams T" for a paper actually by Liang & Chuang; collins2004 for a Beachy
paper; benson2002 for a Stuart paper). The authoritative author/title/journal
metadata lives in data/raw/papers/_abstracts/<PMID>.json, and docs/sources.md
already maps each PMID to the correct author-derived source_id (via script 03).

This script joins each extracted source to its PMID by TITLE, then rewrites the
source_id, citation, and doi from the authoritative metadata, and renames the
per-source CSV. It NEVER touches the data columns (counts/rates/etc.).

Dry run by default (prints the full old->new mapping and flags collisions /
unmatched files). Pass --apply to write the changes.

    python3 scripts/35_fix_attributions.py            # dry run
    python3 scripts/35_fix_attributions.py --apply     # execute
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "data/extracted"
ABS_DIR = ROOT / "data/raw/papers/_abstracts"
SOURCES_MD = ROOT / "docs/sources.md"

# Sources that are not PubMed papers — never touch.
SKIP_PREFIXES = ("neiss",)
SKIP_IDS = {"rugby_europe_iss_2024"}

# Title-match failed on punctuation/abbreviation for these; pin the PMID by the
# current (wrong) source_id. Verified by hand against sources.md 2026-06-16.
PMID_OVERRIDE = {
    "azimi2020": "33292522",   # -> farhadian2020
    "benson2002": "11798994",  # -> stuart2002 (Stuart MJ et al., AJSM 2002)
    "jain2017": "28969286",    # -> goyal2017
    "zaror2018": "29526055",   # -> galic2018
    "tyler2026": "42052228",   # id already correct; rebuild full citation
}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def citation_title(cit: str) -> str:
    after = re.split(r"\)\.\s*", cit, maxsplit=1)
    seg = after[1] if len(after) > 1 else cit
    return re.split(r"\.\s+", seg)[0]


def build_citation(rec: dict) -> str:
    authors = rec.get("authors") or []
    astr = ", ".join(authors) if authors else "Unknown"
    year = rec.get("pub_year") or ""
    title = (rec.get("title") or "").rstrip(". ")
    journal = (rec.get("journal") or "").rstrip(". ")
    cit = f"{astr}. ({year}). {title}."
    if journal:
        cit += f" {journal}."
    return cit


def load_sources_md_ids() -> dict:
    """pmid -> correct source_id, parsed from the docs/sources.md table."""
    out = {}
    row_re = re.compile(r"^\|\s*([A-Za-z0-9_\-]+)\s*\|\s*\[(\d+)\]")
    for line in SOURCES_MD.read_text().splitlines():
        m = row_re.match(line)
        if m:
            out[m.group(2)] = m.group(1)  # pmid -> source_id
    return out


def main() -> None:
    apply = "--apply" in sys.argv

    abstracts = {}
    by_title = {}
    for p in ABS_DIR.glob("*.json"):
        d = json.load(open(p))
        pmid = str(d.get("pmid", p.stem))
        abstracts[pmid] = d
        tn = norm(d.get("title", ""))
        if tn:
            by_title[tn] = pmid

    pmid_to_correct_sid = load_sources_md_ids()

    plans = []          # (old_sid, new_sid, old_cit, new_cit, pmid, file)
    unmatched = []
    unchanged = 0
    for f in sorted(EXTRACTED.glob("*.csv")):
        sid = f.stem
        if sid.startswith(SKIP_PREFIXES) or sid in SKIP_IDS:
            continue
        rows = list(csv.DictReader(open(f)))
        if not rows:
            continue
        cit = rows[0].get("citation", "")
        pmid = PMID_OVERRIDE.get(sid) or by_title.get(norm(citation_title(cit)))
        if not pmid:
            unmatched.append(sid)
            continue
        new_sid = pmid_to_correct_sid.get(pmid)
        rec = abstracts.get(pmid, {})
        if not new_sid or not rec:
            unmatched.append(f"{sid} (pmid {pmid} but no sources.md id / abstract)")
            continue
        new_cit = build_citation(rec)
        new_doi = rec.get("doi", "") or rows[0].get("doi", "")
        if new_sid == sid and new_cit == cit:
            unchanged += 1
            continue
        plans.append((sid, new_sid, cit, new_cit, pmid, f, new_doi, rows))

    # Collision check: do two different files map to the same new_sid?
    from collections import Counter
    newids = Counter(p[1] for p in plans)
    collisions = {k: v for k, v in newids.items() if v > 1}
    # Also collisions with files that are already correct (unchanged) and keep their id
    existing_correct = {f.stem for f in EXTRACTED.glob("*.csv")
                        if not (f.stem.startswith(SKIP_PREFIXES) or f.stem in SKIP_IDS)}

    print(f"=== ATTRIBUTION REPAIR {'(APPLY)' if apply else '(DRY RUN)'} ===")
    print(f"changed: {len(plans)}   unchanged/correct: {unchanged}   unmatched: {len(unmatched)}")
    print()
    for old, new, oc, nc, pmid, f, doi, rows in plans:
        tag = "  (id same)" if old == new else ""
        print(f"{old:>22} -> {new:<22} pmid {pmid}{tag}")
        if old != new:
            print(f"     old: {oc[:95]}")
            print(f"     new: {nc[:95]}")
    if collisions:
        print("\n!!! COLLISIONS (multiple files map to same new id) — MUST resolve before apply:")
        for k, v in collisions.items():
            print(f"    {k}: {v} files")
    if unmatched:
        print(f"\nUNMATCHED (left unchanged): {unmatched}")

    if not apply:
        print("\n(dry run — no files changed. Re-run with --apply once the mapping looks right.)")
        return

    if collisions:
        print("\nABORTING apply: resolve collisions first.")
        sys.exit(2)

    COLUMNS = list(rows[0].keys()) if plans else []
    for old, new, oc, nc, pmid, f, doi, rows in plans:
        for r in rows:
            r["source_id"] = new
            r["citation"] = nc
            r["doi"] = doi
        target = EXTRACTED / f"{new}.csv"
        with open(target, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        if target != f:
            f.unlink()
    print(f"\nApplied {len(plans)} repairs. Re-run scripts/07, 03, 04, 26, 21, 24, 29, 18, 33, 08, 34.")


if __name__ == "__main__":
    main()
