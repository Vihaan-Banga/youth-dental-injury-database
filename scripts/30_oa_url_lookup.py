#!/usr/bin/env python3
"""Resolve OA URLs for the needs_additional_review PubMed records.

For each needs_additional_review PMID:
  1. Use NCBI eutils (efetch) to pull the DOI from the article metadata
  2. Query Unpaywall for the best OA URL
  3. Persist a CSV: pmid, doi, journal, title, oa_url, oa_host_type, publisher

Output: outputs/needs_additional_review_oa_urls.csv
"""

from __future__ import annotations

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SCREENING_CSV = ROOT / "data/extracted/_screening/screening_decisions.csv"
ABSTRACT_DIR = ROOT / "data/raw/papers/_abstracts"
OUT_CSV = ROOT / "outputs/needs_additional_review_oa_urls.csv"
EMAIL = "Vihaan-Banga@users.noreply.github.com"

UA = f"YouthDentalInjuryDB/0.1 (+{EMAIL})"


def http_get(url: str, accept: str = "*/*", timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_doi_efetch(pmid: str) -> Optional[str]:
    """Use NCBI efetch (XML mode) to extract DOI for one PMID."""
    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        f"?db=pubmed&id={pmid}&retmode=xml&tool=youth_dental_db&email={EMAIL}"
    )
    try:
        body = http_get(url, accept="application/xml", timeout=25)
    except Exception as exc:
        print(f"  efetch FAIL {pmid}: {exc}")
        return None
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return None
    # DOI lives in <ArticleId IdType="doi">...</ArticleId>
    for aid in root.iter("ArticleId"):
        if aid.attrib.get("IdType") == "doi" and aid.text:
            return aid.text.strip()
    # Some records put DOI under ELocationID
    for el in root.iter("ELocationID"):
        if el.attrib.get("EIdType") == "doi" and el.text:
            return el.text.strip()
    return None


def unpaywall_lookup(doi: str) -> Optional[dict]:
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={EMAIL}"
    try:
        body = http_get(url, accept="application/json", timeout=20)
    except Exception as exc:
        print(f"  unpaywall FAIL {doi}: {exc}")
        return None
    try:
        return json.loads(body)
    except Exception:
        return None


def main() -> None:
    nhr = []
    with open(SCREENING_CSV) as f:
        for r in csv.DictReader(f):
            if r["decision"] == "needs_additional_review":
                nhr.append(r)
    print(f"{len(nhr)} needs_additional_review records")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "pmid", "pub_year", "journal", "title", "reason_code",
        "doi", "is_oa", "oa_url", "oa_host_type", "publisher",
    ]
    with open(OUT_CSV, "w", newline="") as out:
        w = csv.DictWriter(out, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(nhr, 1):
            pmid = r["pmid"]
            print(f"[{i}/{len(nhr)}] PMID {pmid}")
            row = {
                "pmid": pmid, "pub_year": r["pub_year"], "journal": r["journal"],
                "title": r["title"], "reason_code": r["reason_code"],
                "doi": "", "is_oa": "", "oa_url": "", "oa_host_type": "",
                "publisher": "",
            }
            doi = fetch_doi_efetch(pmid)
            time.sleep(0.35)  # respect NCBI rate limit
            if not doi:
                print("  no DOI")
                w.writerow(row)
                continue
            row["doi"] = doi
            up = unpaywall_lookup(doi)
            time.sleep(0.2)
            if not up:
                w.writerow(row)
                continue
            row["is_oa"] = str(bool(up.get("is_oa")))
            row["publisher"] = up.get("publisher", "") or ""
            best = up.get("best_oa_location") or {}
            if best:
                row["oa_url"] = best.get("url_for_pdf") or best.get("url") or ""
                row["oa_host_type"] = best.get("host_type") or ""
            w.writerow(row)

    print(f"\nWrote {OUT_CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
