#!/usr/bin/env python3
"""Find which needs_additional_review PMIDs have a free PMC full-text version.

Unpaywall (scripts/30) points mostly at publisher PDFs that sit behind
Cloudflare/paywall bot-checks and 403 on programmatic fetch. PubMed Central
(PMC), by contrast, serves free full-text HTML that is cleanly fetchable.

For each needs_additional_review PMID this script asks NCBI elink
(dbfrom=pubmed, db=pmc) whether a PMC record exists, and writes:

    internal/needs_additional_review_pmc.csv
      pmid, pmcid, pmc_url

A non-empty pmcid means the article's full text is readable at
https://www.ncbi.nlm.nih.gov/pmc/articles/<pmcid>/ without a paywall.

Reuses the eutils access pattern from scripts/30_oa_url_lookup.py.
"""
from __future__ import annotations

import csv
import time
import urllib.parse
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SCREENING_CSV = ROOT / "data/extracted/_screening/screening_decisions.csv"
OUT_CSV = ROOT / "internal/needs_additional_review_pmc.csv"
EMAIL = "Vihaan-Banga@users.noreply.github.com"
UA = f"YouthDentalInjuryDB/0.1 (+{EMAIL})"
ELINK = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def pmc_for(pmid: str) -> str:
    params = {
        "dbfrom": "pubmed",
        "db": "pmc",
        "id": pmid,
        "linkname": "pubmed_pmc",
        "tool": "youth-dental-injury-db",
        "email": EMAIL,
    }
    url = f"{ELINK}?{urllib.parse.urlencode(params)}"
    try:
        root = ET.fromstring(_get(url))
    except Exception:
        return ""
    for link in root.iter("Link"):
        idn = link.findtext("Id")
        if idn:
            return f"PMC{idn}"
    return ""


def main() -> None:
    pmids = [
        r["pmid"]
        for r in csv.DictReader(open(SCREENING_CSV))
        if r["decision"] == "needs_additional_review"
    ]
    rows = []
    found = 0
    for i, pmid in enumerate(pmids, 1):
        pmcid = pmc_for(pmid)
        if pmcid:
            found += 1
        url = (
            f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/"
            if pmcid
            else ""
        )
        rows.append({"pmid": pmid, "pmcid": pmcid, "pmc_url": url})
        print(f"[{i:>2}/{len(pmids)}] {pmid:>9}  {pmcid or '-'}")
        time.sleep(0.34)  # NCBI: <=3 req/s without an API key

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pmid", "pmcid", "pmc_url"])
        w.writeheader()
        w.writerows(rows)
    print(f"\n{found}/{len(pmids)} have a free PMC full text. Wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
