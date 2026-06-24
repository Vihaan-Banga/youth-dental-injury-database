#!/usr/bin/env python3
"""Derive docs/rate_explorer_data.json — the data backing the static Rate
Explorer page (docs/rate-explorer.html).

This is a faithful projection of data/harmonized/master.csv: it copies the
fields the explorer displays for each youth-primary row, plus a small meta
block. It invents nothing — it is a column subset of master.csv, so the page
can run as a simple client-side filter (the v1 spec: "simple filter over
master.csv, no ML").

The explorer is a POPULATION RATE EXPLORER, not an individual risk calculator;
that framing lives in the page itself.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data/harmonized/master.csv"
OUT = ROOT / "docs/rate_explorer_data.json"

# Fields the page shows. Subset of the 38-column schema, incl. the derived
# measure_type / comparability_group so the page can segregate by rate basis.
FIELDS = [
    "source_id", "citation", "pub_year", "study_type", "country",
    "age_category", "age_min", "age_max", "extraction_basis", "sex",
    "level_of_play", "sport", "sport_raw", "sport_category",
    "exposure_context", "subgroup_label",
    "sample_size", "athlete_exposures",
    "injury_count", "injury_type_raw", "injury_category",
    "rate_raw", "rate_denominator_raw", "rate_per_1000_ae",
    "mouthguard_required", "mouthguard_use_rate", "mouthguard_injury_relation",
    "quality_flag", "measure_type", "comparability_group",
]


def main() -> None:
    rows = list(csv.DictReader(open(MASTER)))
    # Headline scope = youth-primary subset (PROTOCOL §6.2.1 / §9).
    youth = [r for r in rows if r.get("extraction_basis") == "youth_primary"]
    projected = [{k: r.get(k, "") for k in FIELDS} for r in youth]

    sports = sorted({r["sport"] for r in projected if r["sport"]})
    ages = sorted({r["age_category"] for r in projected if r["age_category"]})
    n_ae = sum(1 for r in projected if r["rate_per_1000_ae"].strip())
    n_mg = sum(1 for r in projected
               if r["mouthguard_injury_relation"] == "analyzed")

    payload = {
        "meta": {
            "generated": "2026-06-13",
            "source": "data/harmonized/master.csv",
            "scope": "youth_primary rows (ages 5-22 inclusion scope)",
            "n_rows": len(projected),
            "n_sources": len({r["source_id"] for r in projected}),
            "n_with_comparable_ae_rate": n_ae,
            "n_mouthguard_analyzed": n_mg,
            "sports": sports,
            "age_categories": ages,
        },
        "rows": projected,
    }
    OUT.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(projected)} rows, "
          f"{len(sports)} sports, {n_ae} with per-1000-AE rate, "
          f"{n_mg} mouthguard-analyzed. ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
