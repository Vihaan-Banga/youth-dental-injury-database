#!/usr/bin/env python3
"""Fix the fabricated author attributions at their ROOT: the hardcoded
source_id and citation string literals inside the batch extraction scripts.

scripts/35 corrected the extracted CSVs, but the batch scripts that generated
them (14-19, 25, ...) still hardcode the wrong ids/citations, so re-running any
of them would re-introduce the error (and duplicate files). This patches the
script source so re-running reproduces the CORRECT data.

For every  make("<id>", citation="<cit>", ...)  the script:
  - parses the title out of <cit>, matches it to a PubMed abstract JSON,
  - looks up the correct source_id from docs/sources.md and rebuilds the
    citation from the abstract authors/year/title/journal (same as scripts/35),
  - rewrites the id literals  w("id"/write_csv("id"/make("id")  and the
    citation literal in place.

Idempotent. Dry run by default; --apply to write.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ABS_DIR = ROOT / "data/raw/papers/_abstracts"
SOURCES_MD = ROOT / "docs/sources.md"
TARGETS = sorted(ROOT.glob("scripts/*_extract_batch*.py")) + [
    ROOT / "scripts/09_write_more_extractions.py",
    ROOT / "scripts/13_neiss_hadley_extractions.py",
]

CIT_OVERRIDE_PMID = {  # title-match misses (punctuation); pin by id.
    # keyed by BOTH the original (wrong) id and the corrected id, so the patcher
    # is idempotent whether run before or after the id rename.
    "azimi2020": "33292522", "farhadian2020": "33292522",
    "benson2002": "11798994", "stuart2002": "11798994",
    "jain2017": "28969286", "goyal2017": "28969286",
    "zaror2018": "29526055", "galic2018": "29526055",
    "tyler2026": "42052228",
}


def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def citation_title(cit):
    after = re.split(r"\)\.\s*", cit, maxsplit=1)
    seg = after[1] if len(after) > 1 else cit
    return re.split(r"\.\s+", seg)[0]


def build_citation(rec):
    authors = ", ".join(rec.get("authors") or []) or "Unknown"
    title = (rec.get("title") or "").rstrip(". ")
    journal = (rec.get("journal") or "").rstrip(". ")
    cit = f"{authors}. ({rec.get('pub_year') or ''}). {title}."
    return cit + (f" {journal}." if journal else "")


def main():
    apply = "--apply" in sys.argv
    abstracts, by_title = {}, {}
    for p in ABS_DIR.glob("*.json"):
        d = json.load(open(p)); pmid = str(d.get("pmid", p.stem))
        abstracts[pmid] = d
        if d.get("title"):
            by_title[norm(d["title"])] = pmid
    pmid_to_sid = {}
    for line in SOURCES_MD.read_text().splitlines():
        m = re.match(r"^\|\s*([A-Za-z0-9_\-]+)\s*\|\s*\[(\d+)\]", line)
        if m:
            pmid_to_sid[m.group(2)] = m.group(1)

    # A "citation literal" is any double-quoted string containing "(YYYY).".
    CIT_LIT = re.compile(r'"([^"]*\(\d{4}\)\.[^"]*)"')

    def resolve(cit):
        """citation literal -> (pmid, new_citation) or (None, None)."""
        pmid = by_title.get(norm(citation_title(cit)))
        if not pmid:
            return None, None
        rec = abstracts.get(pmid)
        return (pmid, build_citation(rec)) if rec else (None, None)

    total_changed = 0
    for path in TARGETS:
        if not path.exists():
            continue
        text = orig = path.read_text()

        # Single pass keyed on each source's opener (w()/write_csv("id")). For
        # each, find the nearest citation literal (the shared dict sits just
        # above; an inline citation just below) and resolve the correct pmid
        # (override first, else by title). Then rewrite both that citation
        # literal and the id. One literal per source, so nearest is unambiguous.
        openers = list(re.finditer(r'(?:w|write_csv)\(\s*"([^"]+)"', orig))
        cit_positions = [(m.start(), m.group(1)) for m in CIT_LIT.finditer(orig)]
        id_map, cit_map = {}, {}
        for om in openers:
            old_id = om.group(1)
            near = min(cit_positions, key=lambda cp: abs(cp[0] - om.start()),
                       default=None)
            lit = near[1] if near and abs(near[0] - om.start()) <= 600 else None
            pmid = CIT_OVERRIDE_PMID.get(old_id) or (
                by_title.get(norm(citation_title(lit))) if lit else None)
            if not pmid:
                continue
            rec = abstracts.get(pmid)
            new_id = pmid_to_sid.get(pmid)
            if not rec or not new_id:
                continue
            new_cit = build_citation(rec)
            if lit and new_cit != lit:
                cit_map[lit] = new_cit
            if new_id != old_id:
                id_map[old_id] = new_id
        for lit, new_cit in cit_map.items():
            text = text.replace(f'"{lit}"', f'"{new_cit}"')
        for old_id, new_id in id_map.items():
            for pat in (f'w("{old_id}"', f'write_csv("{old_id}"', f'make("{old_id}"'):
                text = text.replace(pat, pat.replace(f'"{old_id}"', f'"{new_id}"'))

        if text != orig:
            print(f"{path.name}: patched ({len(cit_map)} citations, {len(id_map)} ids)")
            total_changed += 1
            if apply:
                path.write_text(text)
    print(f"\n{'APPLIED' if apply else 'DRY RUN'} — {total_changed} script(s) "
          f"{'changed' if apply else 'would change'}.")
    if not apply:
        print("Re-run with --apply, then re-run the batch scripts + 07 + 08 + 34 to verify.")


if __name__ == "__main__":
    main()
