#!/usr/bin/env python3
"""Build initial sources.md candidate rows from a PubMed esummary.json dump.

For each record we emit one row of the docs/sources.md table with status
`identified`, plus a separate summary section listing the journal mix and
date range so the project lead can see at a glance what the search returned.
"""

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

DATA = json.load(open("/tmp/pubmed_search/esummary.json"))["result"]
uids = DATA["uids"]
records = [DATA[u] for u in uids]


def first_author(rec):
    authors = rec.get("authors") or []
    for a in authors:
        if a.get("authtype") == "Author":
            return a["name"]
    return authors[0]["name"] if authors else "Unknown"


def lastname(name):
    # esummary returns "Last FM" — first whitespace-delimited token is the surname
    return name.split()[0].lower()


def pubyear(rec):
    pd = rec.get("pubdate", "")
    m = re.search(r"(\d{4})", pd)
    return m.group(1) if m else ""


def doi(rec):
    for art in rec.get("articleids", []):
        if art.get("idtype") == "doi":
            return art["value"]
    return ""


def short_cite(rec):
    fa = first_author(rec)
    yr = pubyear(rec)
    title = rec.get("title", "").rstrip(".")
    title = (title[:90] + "...") if len(title) > 90 else title
    return f"{fa} ({yr}) — {title}"


# Build source_id with collision handling
seen = Counter()
rows = []
for rec in records:
    fa = first_author(rec)
    yr = pubyear(rec) or "noyear"
    base = f"{lastname(fa)}{yr}"
    seen[base] += 1
    suffix = chr(ord("a") + seen[base] - 1) if seen[base] > 1 else ""
    if seen[base] == 2:
        # retroactively suffix the prior occurrence as 'a'
        for r in rows:
            if r["source_id"] == base:
                r["source_id"] = base + "a"
                break
    sid = base + suffix
    rows.append({
        "source_id": sid,
        "pmid": rec["uid"],
        "citation_short": short_cite(rec),
        "journal": rec.get("fulljournalname", ""),
        "pub_year": yr,
        "doi": doi(rec),
    })

# Sort rows by pub_year desc then source_id
rows.sort(key=lambda r: (r["pub_year"] or "0", r["source_id"]), reverse=True)

today = date.today().isoformat()

# Print a markdown table block
print(f"<!-- Generated {today} from PubMed E-utilities. Query: see PROTOCOL.md §4.2. {len(rows)} records. -->")
print()
print("| source_id | pmid | citation_short | journal | doi | status | reason_if_excluded | date_added | extractor |")
print("|---|---|---|---|---|---|---|---|---|")
for r in rows:
    doi_link = f"[{r['doi']}](https://doi.org/{r['doi']})" if r["doi"] else ""
    pmid_link = f"[{r['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/)"
    cite = r["citation_short"].replace("|", "\\|")
    journal = r["journal"].replace("|", "\\|")
    print(f"| {r['source_id']} | {pmid_link} | {cite} | {journal} | {doi_link} | identified | | {today} | |")

# Summary stats to stderr-ish — print to a separate file
journals = Counter(r["journal"] for r in rows if r["journal"])
years = Counter(r["pub_year"] for r in rows if r["pub_year"])
Path("/tmp/pubmed_search/summary.txt").write_text(
    "Top 15 journals:\n"
    + "\n".join(f"  {c:3d}  {j}" for j, c in journals.most_common(15))
    + f"\n\nYear distribution (min/max/most recent counts):\n"
    + f"  Years span: {min(years)}–{max(years)}\n"
    + "\n".join(f"  {y}: {c}" for y, c in sorted(years.items(), reverse=True)[:10])
    + f"\n\nTotal records: {len(rows)}\n"
)
