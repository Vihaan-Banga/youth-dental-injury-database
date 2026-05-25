#!/usr/bin/env python3
"""Parse the PubMed efetch XML dump into per-PMID JSON records.

Each record captures the fields screening cares about: title, abstract text
(concatenating structured AbstractText sections), publication types (so we
can spot 'Case Reports' / 'Review' / 'Systematic Review'), MeSH headings,
language, and journal.

Output: data/raw/papers/_abstracts/<PMID>.json — one file per record.
Also writes a single combined CSV at data/raw/papers/_abstracts/_index.csv
for quick scanning.
"""

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XML_PATH = ROOT / "data/raw/papers/_search_logs/pubmed_efetch_abstracts_2026-05-21.xml"
OUT_DIR = ROOT / "data/raw/papers/_abstracts"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def text(el):
    return "".join(el.itertext()).strip() if el is not None else ""


def parse_article(art):
    pmid = art.findtext(".//PMID")
    journal = art.findtext(".//Article/Journal/Title") or ""
    title = text(art.find(".//Article/ArticleTitle"))
    # Abstract: may have multiple AbstractText elements with Label="OBJECTIVE" etc.
    abs_parts = []
    for at in art.findall(".//Abstract/AbstractText"):
        label = at.get("Label")
        body = text(at)
        abs_parts.append(f"{label}: {body}" if label else body)
    abstract = "\n".join(abs_parts).strip()
    pub_types = [text(pt) for pt in art.findall(".//PublicationTypeList/PublicationType")]
    mesh = [text(d) for d in art.findall(".//MeshHeadingList/MeshHeading/DescriptorName")]
    language = art.findtext(".//Article/Language") or ""
    year = (
        art.findtext(".//Article/Journal/JournalIssue/PubDate/Year")
        or art.findtext(".//Article/ArticleDate/Year")
        or ""
    )
    authors = []
    for au in art.findall(".//AuthorList/Author"):
        last = au.findtext("LastName") or ""
        init = au.findtext("Initials") or ""
        coll = au.findtext("CollectiveName") or ""
        if last:
            authors.append(f"{last} {init}".strip())
        elif coll:
            authors.append(coll)
    return {
        "pmid": pmid,
        "title": title,
        "abstract": abstract,
        "publication_types": pub_types,
        "mesh": mesh,
        "language": language,
        "pub_year": year,
        "journal": journal,
        "authors": authors,
    }


tree = ET.parse(XML_PATH)
records = []
for art in tree.getroot().findall(".//PubmedArticle"):
    rec = parse_article(art)
    if not rec["pmid"]:
        continue
    records.append(rec)
    (OUT_DIR / f"{rec['pmid']}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False))

# Combined index CSV
with (OUT_DIR / "_index.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["pmid", "pub_year", "journal", "publication_types", "has_abstract", "language", "title"])
    for r in records:
        w.writerow([
            r["pmid"],
            r["pub_year"],
            r["journal"],
            "|".join(r["publication_types"]),
            "yes" if r["abstract"] else "no",
            r["language"],
            r["title"],
        ])

# Quick stats
with_abs = sum(1 for r in records if r["abstract"])
case_reports = sum(1 for r in records if "Case Reports" in r["publication_types"])
reviews = sum(
    1 for r in records
    if any(p in r["publication_types"] for p in ("Review", "Systematic Review", "Meta-Analysis"))
)
non_english = sum(1 for r in records if r["language"] and r["language"] != "eng")
print(f"Parsed {len(records)} records")
print(f"  with abstract: {with_abs}")
print(f"  Case Reports : {case_reports}")
print(f"  Review/SR/MA : {reviews}")
print(f"  non-English  : {non_english}")
