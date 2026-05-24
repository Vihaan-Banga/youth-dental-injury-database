#!/usr/bin/env python3
"""Rewrite docs/sources.md so each PubMed candidate row reflects its current
screening decision (status, reason_if_excluded, extractor).

This pulls the canonical decisions from
data/extracted/_screening/screening_decisions.csv (produced by
02_screen_candidates.py) and the canonical citation metadata from the
parsed esummary records (data/raw/papers/_abstracts/_index.csv plus the
per-PMID JSONs).

It preserves the existing surrounding sections (status definitions,
surveillance system list, search history, inter-rater log) and only
replaces the candidate table.
"""

import csv
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path("/Users/vihaanbanga/youth-dental-injury-database")
SOURCES_MD = ROOT / "docs/sources.md"
DECISIONS_CSV = ROOT / "data/extracted/_screening/screening_decisions.csv"
ABS_DIR = ROOT / "data/raw/papers/_abstracts"

EXTRACTOR_TAG = "VB-AI-assisted-2026-05-21"


def first_author(rec):
    authors = rec.get("authors") or []
    return authors[0] if authors else "Unknown"


def lastname(name):
    return name.split()[0].lower()


def short_cite(rec):
    fa = first_author(rec)
    yr = rec.get("pub_year") or ""
    title = (rec.get("title") or "").rstrip(".")
    title = title[:90] + "..." if len(title) > 90 else title
    return f"{fa} ({yr}) — {title}"


# Build source_id with collision handling (same logic as 00_pubmed_seed_sources.py).
records = {p.stem: json.load(open(p)) for p in ABS_DIR.glob("*.json")}
decisions = list(csv.DictReader(open(DECISIONS_CSV)))

seen = Counter()
sid_for_pmid = {}
for d in sorted(decisions, key=lambda r: (r["pub_year"] or "0", r["pmid"]), reverse=True):
    rec = records.get(d["pmid"], {})
    base = f"{lastname(first_author(rec))}{rec.get('pub_year') or 'noyear'}"
    seen[base] += 1
    if seen[base] == 1:
        sid_for_pmid[d["pmid"]] = base
    else:
        # Retroactively suffix the first occurrence to 'a' the first time we collide.
        if seen[base] == 2:
            for pmid, s in sid_for_pmid.items():
                if s == base:
                    sid_for_pmid[pmid] = base + "a"
                    break
        sid_for_pmid[d["pmid"]] = base + chr(ord("a") + seen[base] - 1)

today = date.today().isoformat()


def doi_link(rec):
    for art in rec.get("articleids", []) if "articleids" in rec else []:
        if art.get("idtype") == "doi":
            return f"[{art['value']}](https://doi.org/{art['value']})"
    return ""


EXTRACTED_DIR = ROOT / "data/extracted"
EXTRACTED_SOURCES = {
    p.stem for p in EXTRACTED_DIR.glob("*.csv")
    if not p.stem.startswith("_") and p.is_file()
}


def fmt_row(d):
    pmid = d["pmid"]
    rec = records.get(pmid, {})
    sid = sid_for_pmid[pmid]
    pmid_link = f"[{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)"
    cite = short_cite(rec).replace("|", "\\|")
    journal = (rec.get("journal") or "").replace("|", "\\|")
    decision = d["decision"]
    # If we've already extracted this source, status advances to 'extracted'.
    if sid in EXTRACTED_SOURCES:
        decision = "extracted"
        reason = ""
    else:
        reason = d["reason_code"] if decision != "screened_included" else ""
    # Short-form note for the table
    return (f"| {sid} | {pmid_link} | {cite} | {journal} |  | "
            f"{decision} | {reason} | 2026-05-21 | {EXTRACTOR_TAG} |")


rows = [fmt_row(d) for d in sorted(
    decisions, key=lambda r: (r["decision"], r["pub_year"] or "0", r["pmid"]), reverse=True
)]

# Stats for the header note (post-extraction-advance)
by_dec = Counter()
for d in decisions:
    sid = sid_for_pmid[d["pmid"]]
    by_dec[("extracted" if sid in EXTRACTED_SOURCES else d["decision"])] += 1
by_code = Counter(d["reason_code"] for d in decisions if d["decision"] != "screened_included")

content = f"""# Source Tracking Log

Every candidate source — whether eventually included or excluded — is logged here. This creates an audit trail for the systematic review process required for publication.

**Status values:**
- `identified`: Citation found but not yet reviewed
- `screened_excluded`: Abstract reviewed, does not meet inclusion criteria. Reason required.
- `screened_included`: Abstract reviewed, meets criteria, pending full-text review
- `needs_human_review`: Abstract reviewed but a key §3.1 attribute (age, sport-relatedness, data extractability) could not be confirmed from the abstract alone — needs full-text review before final include/exclude call.
- `fulltext_excluded`: Full text reviewed, does not meet criteria. Reason required.
- `included`: Meets criteria, queued for extraction
- `extracted`: Data extracted into `data/extracted/<source_id>.csv`
- `harmonized`: Extracted data merged into master dataset

**Reason codes** (used in `reason_if_excluded` and `needs_human_review` rows; full reasoning in `outputs/screening_report_2026-05-21.md`):

| code | meaning |
|---|---|
| E-lang   | non-English (§3.1 v1.0 scope) |
| E-review | review/SR/MA — kept for source mining, not extracted (§3.2) |
| E-case   | single case report / n<5 (§3.2) |
| E-age    | population outside 5–22 (§3.1) — adults only, military, etc. |
| E-offtop | not sport-related or wrong subject (§3.1/§3.3) |
| E-noprim | no extractable primary numerical injury data (§3.1) |
| E-nodent | no dental/orofacial-with-dental outcome (§3.3) |
| E-nonpr  | non-peer-reviewed and not an approved surveillance/governing body source (§3.2) |
| R-age    | age range / population unclear from abstract |
| R-mixed  | mixed adult+youth, youth subset extractability needs full text |
| R-data   | not obvious whether numerical injury counts are extractable |
| R-other  | other ambiguity — see notes in the screening report |

---

## Sources

**Screening summary as of 2026-05-21** (AI-assisted first pass; project lead and advisor still need to second-screen the 20% reliability sample per PROTOCOL §4.4, and the `needs_human_review` set requires full-text review before a final decision):

- `screened_included`: **{by_dec.get('screened_included', 0)}** ({100 * by_dec.get('screened_included', 0) // 200}%)
- `needs_human_review`: **{by_dec.get('needs_human_review', 0)}** ({100 * by_dec.get('needs_human_review', 0) // 200}%)
- `screened_excluded`: **{by_dec.get('screened_excluded', 0)}** ({100 * by_dec.get('screened_excluded', 0) // 200}%)

PubMed initial seed (search run 2026-05-21, query per PROTOCOL.md §4.2 — 202 hits, top 200 retrieved). See `outputs/screening_report_2026-05-21.md` for per-decision reasoning. Raw esearch/esummary/efetch dumps preserved under `data/raw/papers/_search_logs/`.

| source_id | pmid | citation_short | journal | doi | status | reason_if_excluded | date_added | extractor |
|---|---|---|---|---|---|---|---|---|
""" + "\n".join(rows) + """

<!-- Add new rows as sources are identified. Keep this table updated. -->

---

## Surveillance systems to query (separate from individual papers)

| system | url | status | notes |
|---|---|---|---|
| NEISS | https://www.cpsc.gov/cgibin/NEISSQuery/ | not_started | Free, public query interface. Annual CSV files at https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data. Body part code 88=Mouth (incl. teeth) — see `docs/decisions.md` for the correction to PROTOCOL §4.1. |
| High School RIO | https://www.nationwidechildrens.org/research/areas-of-research/center-for-injury-research-and-policy/research-projects/high-school-rio | not_started | Published annual reports |
| NCAA ISP | https://www.datalys.org/ncaa-injury-surveillance-program/ | not_started | Aggregate reports public |

---

## Search history

Document every search query run, where, when, and how many results.

| date | source | query | results_count | screened_in | notes |
|---|---|---|---|---|---|
| 2026-05-21 | PubMed (E-utilities) | PROTOCOL.md §4.2 main query verbatim | 202 | (see screening report) | Top 200 PMIDs retrieved via esearch+esummary+efetch. Dumps under `data/raw/papers/_search_logs/`. AI-assisted screening details in `outputs/screening_report_2026-05-21.md`. |
| 2026-05-23 | PubMed (E-utilities) | journal-restricted: `"Dent Traumatol"[journal] AND (dental OR tooth OR orofacial) AND (sport OR athletic)` | 140 | (see screening report) | Targeted search per PROTOCOL §4.2 supplementary list. |
| 2026-05-23 | PubMed (E-utilities) | journal-restricted: `"Pediatr Dent"[journal] AND (trauma OR injury) AND (sport OR athletic)` | 4 | (see screening report) | Targeted search per PROTOCOL §4.2 supplementary list. |
| 2026-05-23 | PubMed (E-utilities) | journal-restricted: `"Am J Sports Med"[journal] AND (dental OR orofacial OR tooth OR maxillofacial)` | 11 | (see screening report) | Targeted search per PROTOCOL §4.2 supplementary list. |
| 2026-05-23 | PubMed (E-utilities) | journal-restricted: `"Br J Sports Med"[journal] AND (dental OR orofacial OR tooth OR maxillofacial)` | 47 | (see screening report) | Targeted search per PROTOCOL §4.2 supplementary list. |
| 2026-05-23 | PubMed (E-utilities) | journal-restricted: `"J Athl Train"[journal] AND (dental OR orofacial OR tooth OR maxillofacial)` | 10 | (see screening report) | Targeted search per PROTOCOL §4.2 supplementary list. |
| 2026-05-23 | (deduplication) | Union of 2026-05-23 journal searches | 212 | 132 NEW after deduplication against 2026-05-21 seed | Dumps at `data/raw/papers/_search_logs/pubmed_*_journal_2026-05-23.*`. |
| 2026-05-24 | PubMed (E-utilities) | journal-restricted: `"J Endod"[journal] AND (dental OR tooth OR avulsion OR luxation) AND (sport OR athletic)` | 8 | (see screening report) | Round 2 of PROTOCOL §4.2 supplementary searches. |
| 2026-05-24 | PubMed (E-utilities) | journal-restricted: `"J Oral Maxillofac Surg"[journal] AND (dental OR mouth OR orofacial OR tooth) AND (sport OR athletic)` | 44 | (see screening report) | Round 2. |
| 2026-05-24 | PubMed (E-utilities) | journal-restricted: `"Pediatrics"[journal] AND (dental OR tooth OR orofacial OR maxillofacial) AND (sport OR athletic)` | 5 | (see screening report) | Round 2. |
| 2026-05-24 | PubMed (E-utilities) | journal-restricted: `"Inj Prev"[journal] AND (dental OR orofacial OR tooth OR maxillofacial OR mouthguard)` | 24 | (see screening report) | Round 2. |
| 2026-05-24 | PubMed (E-utilities) | journal-restricted: `"Orthop J Sports Med"[journal] AND (dental OR orofacial OR tooth OR mouth OR maxillofacial)` | 30 | (see screening report) | Round 2. |
| 2026-05-24 | (deduplication) | Union of 2026-05-24 journal searches | 111 | 104 NEW after deduplication against prior seeds | Dumps at `data/raw/papers/_search_logs/pubmed_*_journal2_2026-05-24.*` and per-journal esearch JSONs. |

---

## Inter-rater check log

For 20% sample of screened sources reviewed by second screener (advisor):

| source_id | primary_decision | secondary_decision | agreement | resolution |
|---|---|---|---|---|
| | | | | |
"""

SOURCES_MD.write_text(content)
print(f"Wrote {len(content)} bytes to {SOURCES_MD}")
print("Status distribution:", dict(by_dec))
