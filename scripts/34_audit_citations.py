#!/usr/bin/env python3
"""Audit every extracted source's citation against the authoritative PubMed
abstract metadata (data/raw/papers/_abstracts/<PMID>.json).

Motivation: the 2026-06-16 audit found williams2023/williams2024 — two rows
whose citation named a fabricated first author ("Williams T") for a paper
actually authored by Liang & Chuang. This script systematically hunts for the
same class of error across all sources.

Method (title is the join key, since extracted rows carry no PMID column):
  1. Index every abstract JSON by a normalized title -> (pmid, first-author
     lastname, pub_year, journal).
  2. For each distinct source in master.csv, parse the claimed first-author
     lastname + year from source_id and the title from the citation string.
  3. Match the citation title to an abstract title (exact-normalized, else
     prefix/containment). If matched, compare:
       - claimed lastname (from source_id) vs real first-author lastname
       - claimed year vs real pub_year
     and flag any mismatch.
  4. Sources that match no abstract title are reported separately (expected
     for NEISS year files and governing-body reports; anything else is a
     suspect — possibly a wrong/invented title).

Read-only. Prints a report; changes nothing.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data/harmonized/master.csv"
ABS_DIR = ROOT / "data/raw/papers/_abstracts"

# Sources legitimately without a PubMed abstract (don't expect a title match).
NON_PUBMED_PREFIXES = ("neiss",)
NON_PUBMED_IDS = {"rugby_europe_iss_2024"}


def norm(s: str) -> str:
    """Lowercase, strip punctuation/whitespace for fuzzy title comparison."""
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def ascii_fold(s: str) -> str:
    """Lowercase, strip diacritics and non-alphanumerics — so 'O'Malley',
    'Iso-Kungas', 'Cetinbaş' compare equal to the ASCII source_id forms
    (omalley / isokungas / cetinbas) produced by scripts/03's lastname()."""
    folded = unicodedata.normalize("NFKD", s or "")
    folded = "".join(c for c in folded if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", folded.lower())


def lastname(author: str) -> str:
    # abstract authors look like "Liang L" / "Azadani EN" -> surname is token 0
    return ascii_fold(author.split()[0]) if author else ""


def parse_source_id(sid: str):
    """source_id 'liang2024' / 'collins2019a' -> ('liang', '2024', 'a')."""
    m = re.match(r"^([a-z][a-z\-']*?)(\d{4})([a-z]?)$", sid)
    if not m:
        return None, None, None
    return m.group(1), m.group(2), m.group(3)


def citation_title(cit: str) -> str:
    """Extract the title from 'Authors (YEAR). Title. Journal.' -> 'Title'."""
    # take everything after the first ').' then the segment up to the next '. '
    after = re.split(r"\)\.\s*", cit, maxsplit=1)
    seg = after[1] if len(after) > 1 else cit
    # title is up to the first '. ' that precedes the journal
    parts = re.split(r"\.\s+", seg)
    return parts[0] if parts else seg


def main() -> None:
    # 1. Index abstracts by normalized title.
    abstracts = []
    for p in ABS_DIR.glob("*.json"):
        d = json.load(open(p))
        authors = d.get("authors") or []
        abstracts.append({
            "pmid": d.get("pmid", p.stem),
            "lastname": lastname(authors[0]) if authors else "",
            "year": str(d.get("pub_year") or ""),
            "title": d.get("title") or "",
            "title_norm": norm(d.get("title") or ""),
            "journal": d.get("journal") or "",
        })
    by_title = {a["title_norm"]: a for a in abstracts if a["title_norm"]}

    def find_abstract(title_norm: str):
        if not title_norm:
            return None
        if title_norm in by_title:
            return by_title[title_norm]
        # prefix / containment fallback (handles truncated titles)
        for a in abstracts:
            t = a["title_norm"]
            if not t:
                continue
            if t.startswith(title_norm) or title_norm.startswith(t) or title_norm in t:
                if abs(len(t) - len(title_norm)) < 30:
                    return a
        return None

    # 2. Distinct sources from master.csv.
    sources = {}
    for r in csv.DictReader(open(MASTER)):
        sources.setdefault(r["source_id"], r["citation"])

    author_mismatch, year_mismatch, no_match, ok = [], [], [], 0
    for sid, cit in sorted(sources.items()):
        if sid.startswith(NON_PUBMED_PREFIXES) or sid in NON_PUBMED_IDS:
            continue
        claim_last, claim_year, _ = parse_source_id(sid)
        t_norm = norm(citation_title(cit))
        ab = find_abstract(t_norm)
        if ab is None:
            no_match.append((sid, citation_title(cit)[:70]))
            continue
        if claim_last and ab["lastname"] and claim_last != ab["lastname"]:
            author_mismatch.append((sid, claim_last, ab["lastname"], ab["pmid"],
                                    citation_title(cit)[:60]))
        elif claim_year and ab["year"] and claim_year != ab["year"]:
            year_mismatch.append((sid, claim_year, ab["year"], ab["pmid"]))
        else:
            ok += 1

    print(f"Audited {len(sources)} distinct sources "
          f"({sum(1 for s in sources if not s.startswith(NON_PUBMED_PREFIXES) and s not in NON_PUBMED_IDS)} PubMed-type).")
    print(f"  OK (author+year match abstract): {ok}")
    print()
    print(f"AUTHOR MISMATCHES ({len(author_mismatch)}):")
    for sid, claim, real, pmid, title in author_mismatch:
        print(f"  {sid:<22} claims '{claim}' but PMID {pmid} first author is '{real}'  | {title}")
    print()
    print(f"YEAR MISMATCHES ({len(year_mismatch)}):")
    for sid, claim, real, pmid in year_mismatch:
        print(f"  {sid:<22} source_id year {claim} but PMID {pmid} pub_year {real}")
    print()
    print(f"NO ABSTRACT-TITLE MATCH ({len(no_match)} — expected for governing/surveillance, suspect otherwise):")
    for sid, title in no_match:
        print(f"  {sid:<22} | {title}")

    # exit non-zero if any author mismatch (the serious class)
    sys.exit(1 if author_mismatch else 0)


if __name__ == "__main__":
    main()
