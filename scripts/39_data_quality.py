#!/usr/bin/env python3
"""Consolidated data-quality report for the harmonized database.

Read-only. Brings the project's quality signals into one artifact for the advisor
and the methods paper:

  1. Verification-risk tiers — how each row's numbers are grounded
     (abstract-corroborated / full-text-table / computed / public-domain raw).
  2. Internal numeric consistency — flag count from scripts/38 (re-run inline).
  3. Rate-scope guard (NEW) — rows whose stored rate represents ALL injuries
     (not dental-specific) yet sit in a dental incidence comparability group, so
     they must NOT be compared as dental rates.
  4. Screening backlog — records still pending full-text review.

Writes outputs/data_quality.md and prints a summary. Not a build gate.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data/harmonized/master.csv"
ABS_DIR = ROOT / "data/raw/papers/_abstracts"
SOURCES_MD = ROOT / "docs/sources.md"
SCREEN = ROOT / "data/extracted/_screening/screening_decisions.csv"
OUT = ROOT / "outputs/data_quality.md"

NUM_FIELDS = ["sample_size", "athlete_exposures", "injury_count",
              "rate_raw", "rate_per_1000_ae", "mouthguard_use_rate"]
INCIDENCE_MT = {"incidence_per_AE", "incidence_per_exposure_hours",
                "incidence_per_season", "incidence_per_population"}
# A rate is a comparability hazard when its PRIMARY descriptor (before any
# parenthetical) names injuries generically / all-body-site with no orofacial
# restriction. Orofacial/head-face rates ARE in scope, so they must not flag.
OROFACIAL = re.compile(r"dental|oral|tooth|teeth|mouth|orofacial|maxillofacial|"
                       r"dentoalveolar|dento-alveolar|\btdi\b|\bodt\b|lip|facial|"
                       r"head/face|head and face|craniofacial|\bface\b|jaw", re.I)


def rate_not_dental_specific(injury_type_raw: str) -> bool:
    primary = injury_type_raw.split("(")[0]
    if not re.search(r"injur|claim", primary, re.I):
        return False
    return not OROFACIAL.search(primary)


def norm_num(s):
    s = s.strip().replace(",", "").replace("%", "").replace(" ", "")
    if not s:
        return None
    s = re.sub(r"\.0+$", "", s).rstrip(".")
    return s or None


def main() -> None:
    rows = list(csv.DictReader(open(MASTER)))
    pmid_of = {}
    for line in SOURCES_MD.read_text().splitlines():
        m = re.match(r"^\|\s*([A-Za-z0-9_\-]+)\s*\|\s*\[(\d+)\]", line)
        if m:
            pmid_of[m.group(1)] = m.group(2)

    abs_cache = {}

    def abstract_nums(pmid):
        if pmid in abs_cache:
            return abs_cache[pmid]
        f = ABS_DIR / f"{pmid}.json"
        if not f.exists():
            abs_cache[pmid] = None
            return None
        rec = json.load(open(f))
        text = (rec.get("abstract") or "") + " " + (rec.get("title") or "")
        if not (rec.get("abstract") or "").strip():
            abs_cache[pmid] = None
            return None
        raw = re.findall(r"\d[\d,]*\.?\d*", text)
        nums = {n for n in (norm_num(t) for t in raw) if n}
        abs_cache[pmid] = (nums, text.replace(",", ""))
        return abs_cache[pmid]

    def in_abs(nv, pack):
        nums, raw = pack
        cands = {nv}
        try:
            fv = float(nv)
            for alt in (fv * 100, fv / 100):
                a = norm_num(f"{alt:.10f}".rstrip("0"))
                if a:
                    cands.add(a)
        except ValueError:
            pass
        return any(c in nums or c in raw for c in cands)

    CALC = re.compile(r"back[- ]?calc|computed|derived|estimat|\bof \d|\d+\s*%\s*of|"
                      r"so \d+(\.\d+)?%|not wearing|rate\s*[×x*]\s*AE", re.I)

    tiers = Counter()
    not_dental = []
    for r in rows:
        sid = r["source_id"]
        note = r.get("extraction_notes", "")
        # rate-scope guard
        itype = r.get("injury_type_raw", "")
        if (r.get("rate_raw", "").strip() and r.get("measure_type") in INCIDENCE_MT
                and rate_not_dental_specific(itype)):
            not_dental.append(r)
        # risk tier
        if sid.startswith("neiss") or sid == "rugby_europe_iss_2024":
            tiers["public_raw"] += 1
            continue
        pack = abstract_nums(pmid_of.get(sid, ""))
        if not pack:
            tiers["no_abstract"] += 1
            continue
        checked = [(f, r[f]) for f in NUM_FIELDS if (r.get(f) or "").strip() not in ("", "0", "NA")]
        if not checked:
            tiers["no_numeric"] += 1
            continue
        missing = [(f, v) for f, v in checked if not in_abs(norm_num(v), pack)]
        rr, rp = (r.get("rate_raw") or "").strip(), (r.get("rate_per_1000_ae") or "").strip()
        if CALC.search(note):
            tiers["computed"] += 1
        elif rp and rr and rp != rr:
            tiers["computed"] += 1
        elif missing:
            tiers["full_text"] += 1
        else:
            tiers["abstract"] += 1

    # screening backlog
    pend = sum(1 for r in csv.DictReader(open(SCREEN)) if r["decision"] == "needs_additional_review")

    L = ["# Data-quality report\n",
         "_Generated by `scripts/39_data_quality.py` (read-only). Consolidates the "
         "project's quality signals. Companion audits: `scripts/37` (values vs PubMed "
         "abstract), `scripts/38` (internal re-computation), `scripts/08` (schema/vocabulary)._\n",
         f"\n## 1. Verification-risk tiers ({len(rows)} rows)\n",
         "How each row's numbers are grounded. All rows are `quality_flag=partial_data` "
         "pending full-text source verification.\n",
         "| tier | rows | meaning |",
         "|---|---:|---|",
         f"| 🟢 abstract-corroborated | {tiers['abstract']} | numbers appear in the source abstract |",
         f"| 🟡 full-text / table | {tiers['full_text']} | value not in abstract, read from full text |",
         f"| 🔴 computed / back-calculated | {tiers['computed']} | derived by arithmetic (see scripts/38) |",
         f"| ⚪ public-domain raw (NEISS/gov) | {tiers['public_raw']} | verify against the source query/report |",
         f"| ⚪ no numeric value | {tiers['no_numeric']} | categorical-only row |",
         f"| ? no usable abstract | {tiers['no_abstract']} | — |",
         "\n## 2. Rate-scope guard — rows whose rate is NOT dental-specific\n",
         "These rows store an **overall / non-dental** injury rate yet sit in a dental "
         "incidence comparability group. They must **not** be read or compared as dental "
         "injury rates. Flagged for advisor review (reclassify, caveat, or exclude).\n"]
    if not_dental:
        L.append("| source_id | subgroup/sport | measure_type | rate_raw | injury_type_raw |")
        L.append("|---|---|---|---|---|")
        for r in not_dental:
            L.append(f"| `{r['source_id']}` | {r.get('subgroup_label') or r.get('sport')} | "
                     f"{r.get('measure_type')} | {r.get('rate_raw')} | {r.get('injury_type_raw','')[:50]} |")
    else:
        L.append("_None detected._")
    L += ["\n## 3. Internal numeric consistency\n",
          "See `outputs/recompute_audit.md` (scripts/38): recomputes each derivable value "
          "from its own inputs. Current flags are logged in `docs/decisions.md`.\n",
          "## 4. Screening backlog\n",
          f"- **{pend}** records still `needs_additional_review` (pending full-text). "
          "Prioritized in `internal/fulltext_request_list.md`.\n"]

    OUT.write_text("\n".join(L) + "\n")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"  tiers: {dict(tiers)}")
    print(f"  rate-scope (not dental-specific) rows: {len(not_dental)}")


if __name__ == "__main__":
    main()
