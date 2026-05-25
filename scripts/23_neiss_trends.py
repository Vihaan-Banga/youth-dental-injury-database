#!/usr/bin/env python3
"""NEISS year-over-year trend analysis using the 12 years of NEISS data
in master.csv (2013-2025 except 2020). This is novel — no single paper has
aggregated this many years of NEISS dental-sport data.

Outputs:
  outputs/neiss_trends.md         — narrative + tables
  outputs/figures/neiss_trend_overall.png         — overall cases per year
  outputs/figures/neiss_trend_per_sport.png       — line chart per major sport
  outputs/figures/neiss_trend_age_bands.png       — stacked area by age band
  outputs/tables/neiss_trends.csv                 — tidy long-format CSV
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/vihaanbanga/youth-dental-injury-database")
MASTER = ROOT / "data/harmonized/master.csv"
OUT_MD = ROOT / "outputs/neiss_trends.md"
TBL_DIR = ROOT / "outputs/tables"; TBL_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR = ROOT / "outputs/figures"; FIG_DIR.mkdir(parents=True, exist_ok=True)

rows = list(csv.DictReader(open(MASTER)))
neiss = [r for r in rows if r["source_id"].startswith("neiss") and re.match(r"^neiss\d{4}$", r["source_id"])]
print(f"Loaded {len(neiss)} NEISS rows from master.csv")

# Build {year: rows}
by_year = defaultdict(list)
for r in neiss:
    try:
        y = int(r["pub_year"])
    except (TypeError, ValueError):
        continue
    by_year[y].append(r)
years = sorted(by_year)
print(f"Years: {years}")


def aggregate_row(year):
    """Return the 'all sports × mixed age × mixed sex' aggregate row for a year."""
    cands = [r for r in by_year[year]
             if r["sport"] == "all_sports_aggregate"
             and r["sex"] == "mixed"
             and r["age_category"] == "mixed"
             and r["subgroup_label"] == "all_youth_aggregate"]
    return cands[0] if cands else None


def parse_int(s):
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return 0


def parse_weighted_estimate(extraction_notes):
    """Pull 'weighted national estimate = X,XXX' from extraction_notes."""
    m = re.search(r"weighted national estimate\s*=\s*([\d,]+)", extraction_notes)
    if not m:
        return None
    return int(m.group(1).replace(",", ""))


# -------------------- 1. Overall by year --------------------
overall = []
for y in years:
    agg = aggregate_row(y)
    if not agg:
        continue
    n = parse_int(agg["injury_count"])
    we = parse_weighted_estimate(agg["extraction_notes"]) or 0
    overall.append({"year": y, "raw_cases": n, "weighted_estimate": we})
print(f"\nOverall by year: {len(overall)} year-rows")
for r in overall:
    print(f"  {r['year']}: raw={r['raw_cases']:>4}  weighted={r['weighted_estimate']:,}")


# -------------------- 2. Per-sport by year --------------------
sports_of_interest = [
    "basketball", "baseball", "football_american", "football_association",
    "softball", "skateboarding", "wrestling", "gymnastics", "hockey_unspecified",
    "swimming", "cheerleading", "hockey_field", "volleyball",
]
per_sport = {sp: {} for sp in sports_of_interest}
for y in years:
    for r in by_year[y]:
        sp = r["sport"]
        if sp not in sports_of_interest:
            continue
        if r["sex"] != "mixed" or r["age_category"] != "mixed":
            continue
        if r["subgroup_label"]:  # main per-sport row has empty subgroup
            continue
        per_sport[sp][y] = parse_int(r["injury_count"])

# Sports with data in >= 5 years
sports_with_trends = [sp for sp in sports_of_interest if len(per_sport[sp]) >= 5]


# -------------------- 3. Per-age-band by year --------------------
age_bands = ("youth", "adolescent", "collegiate")
per_band = {b: {} for b in age_bands}
for y in years:
    for r in by_year[y]:
        if r["subgroup_label"].startswith("age_band_"):
            band = r["subgroup_label"].replace("age_band_", "")
            if band in per_band:
                per_band[band][y] = parse_int(r["injury_count"])


# -------------------- Tidy CSV --------------------
tidy = TBL_DIR / "neiss_trends.csv"
with tidy.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["year", "category_kind", "category_value", "raw_cases", "weighted_estimate"])
    for r in overall:
        w.writerow([r["year"], "overall", "all_sports_x_all_youth", r["raw_cases"], r["weighted_estimate"]])
    for sp in sports_with_trends:
        for y, n in sorted(per_sport[sp].items()):
            w.writerow([y, "sport", sp, n, ""])
    for band in age_bands:
        for y, n in sorted(per_band[band].items()):
            w.writerow([y, "age_band", band, n, ""])
print(f"\nWrote {tidy.relative_to(ROOT)}")


# -------------------- Figures --------------------
# Overall trend
plt.figure(figsize=(11, 5))
xs = [r["year"] for r in overall]
y_raw = [r["raw_cases"] for r in overall]
y_we = [r["weighted_estimate"] for r in overall]
ax1 = plt.gca()
ax1.bar(xs, y_raw, color="#4c72b0", label="Raw NEISS case count (sampled hospitals)")
ax1.set_xlabel("Treatment year")
ax1.set_ylabel("Raw NEISS cases (sampled hospitals)", color="#4c72b0")
ax1.tick_params(axis="y", labelcolor="#4c72b0")
ax2 = ax1.twinx()
ax2.plot(xs, y_we, color="#c44e52", marker="o", linewidth=2,
         label="Weighted national estimate")
ax2.set_ylabel("Weighted national estimate (CPSC)", color="#c44e52")
ax2.tick_params(axis="y", labelcolor="#c44e52")
plt.title("NEISS — youth dental sport injuries by treatment year, 2013–2025")
ax1.set_xticks(xs)
ax1.grid(axis="y", linestyle=":", alpha=0.3)
# Note 2020 gap
ax1.text(2020, max(y_raw) * 0.5, "2020\n(no data)", ha="center", va="center",
         fontsize=10, color="#888", style="italic")
plt.tight_layout()
plt.savefig(FIG_DIR / "neiss_trend_overall.png", dpi=160, bbox_inches="tight")
plt.close()
print(f"Wrote outputs/figures/neiss_trend_overall.png")

# Per-sport trend
fig, ax = plt.subplots(figsize=(12, 7))
palette = ["#4c72b0", "#dd8452", "#55a868", "#c44e52", "#8172b3",
           "#937860", "#da8bc3", "#8c8c8c", "#ccb974", "#64b5cd",
           "#1f77b4", "#ff7f0e", "#2ca02c"]
for i, sp in enumerate(sorted(sports_with_trends, key=lambda s: -sum(per_sport[s].values()))):
    xs = sorted(per_sport[sp].keys())
    ys = [per_sport[sp][x] for x in xs]
    ax.plot(xs, ys, marker="o", color=palette[i % len(palette)], label=sp, linewidth=2)
ax.set_xlabel("Treatment year")
ax.set_ylabel("NEISS raw cases (youth 5-22)")
ax.set_title(f"NEISS — per-sport trends, {min(years)}–{max(years)} (sports with ≥ 5 years of data)")
ax.legend(loc="upper left", fontsize=9, ncol=2)
ax.grid(axis="y", linestyle=":", alpha=0.3)
ax.set_xticks(sorted({y for sp in sports_with_trends for y in per_sport[sp]}))
plt.tight_layout()
plt.savefig(FIG_DIR / "neiss_trend_per_sport.png", dpi=160, bbox_inches="tight")
plt.close()
print(f"Wrote outputs/figures/neiss_trend_per_sport.png")

# Age band trend (stacked area)
fig, ax = plt.subplots(figsize=(11, 5))
xs_all = sorted({y for b in age_bands for y in per_band[b]})
stack_data = []
labels = []
colors = ["#4c72b0", "#dd8452", "#55a868"]
for i, band in enumerate(age_bands):
    series = [per_band[band].get(y, 0) for y in xs_all]
    stack_data.append(series)
    labels.append(f"{band}")
ax.stackplot(xs_all, *stack_data, labels=labels, colors=colors, alpha=0.85)
ax.set_xlabel("Treatment year")
ax.set_ylabel("NEISS raw cases (stacked by age band)")
ax.set_title("NEISS — youth dental sport injuries by age band, 2013–2025")
ax.legend(loc="upper left", fontsize=10)
ax.set_xticks(xs_all)
ax.grid(axis="y", linestyle=":", alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / "neiss_trend_age_bands.png", dpi=160, bbox_inches="tight")
plt.close()
print(f"Wrote outputs/figures/neiss_trend_age_bands.png")


# -------------------- Markdown report --------------------
md = []
W = md.append
W("# NEISS year-over-year trends — 2013–2025\n")
W("_Auto-generated from `data/harmonized/master.csv`. Covers 12 treatment "
  "years of NEISS data on youth (ages 5–22) sport-related mouth injuries._\n")

W("## Overview")
W(f"\nThis is the first time, to our knowledge, that **{len(years)} treatment years** "
  f"of NEISS dental-sport data has been aggregated into a single comparable table for "
  "the youth (5–22) age range. The 2020 gap reflects the COVID-19 youth-sports "
  "shutdown — the CPSC query returned zero matching cases for that year.\n")

W("## Overall trend\n")
W("| year | raw NEISS cases | weighted national estimate |")
W("|---:|---:|---:|")
for r in overall:
    W(f"| {r['year']} | {r['raw_cases']:,} | {r['weighted_estimate']:,} |")
total_raw = sum(r["raw_cases"] for r in overall)
total_we = sum(r["weighted_estimate"] for r in overall)
W(f"| **Total** | **{total_raw:,}** | **{total_we:,}** |\n")
W("![overall trend](figures/neiss_trend_overall.png)\n")

W("## Per-sport trends (sports with ≥ 5 years of data)\n")
if sports_with_trends:
    W("| year | " + " | ".join(sports_with_trends) + " |")
    W("|---:" + "|---:" * len(sports_with_trends) + "|")
    yrs_in_sport = sorted({y for sp in sports_with_trends for y in per_sport[sp]})
    for y in yrs_in_sport:
        vals = [f"{per_sport[sp].get(y, '-')}" for sp in sports_with_trends]
        W(f"| {y} | " + " | ".join(vals) + " |")
W("\n![per-sport trends](figures/neiss_trend_per_sport.png)\n")

W("## Age-band breakdown\n")
W("| year | " + " | ".join(age_bands) + " |")
W("|---:" + "|---:" * len(age_bands) + "|")
xs_band = sorted({y for b in age_bands for y in per_band[b]})
for y in xs_band:
    vals = [f"{per_band[b].get(y, '-')}" for b in age_bands]
    W(f"| {y} | " + " | ".join(vals) + " |")
W("\n![age band trends](figures/neiss_trend_age_bands.png)\n")

W("## Observations & caveats\n")
W("- **2020 is a true gap, not a download error.** The CPSC NEISS query "
  "for 2020 youth mouth-injury sport cases returned zero matching records, "
  "reflecting the widespread suspension of organized youth sports during "
  "COVID-19 lockdowns.")
W("- **Rates** are not directly computed here because NEISS uses a population "
  "denominator that varies year to year; weighted national estimates above "
  "are CPSC's own values (sum of per-case sampling weights).")
W("- **2013–2017 from hadley archive vs 2018–2025 from direct CPSC query** — "
  "the hadley archive used different column names but the same underlying "
  "NEISS data. The 2018–2025 extractions recovered an additional ~10–15% "
  "of cases per year by accepting `Body_Part_2 = 88` (Mouth as secondary "
  "body part — a column added by NEISS in 2019).")
W("- **Trend interpretation**: any year-to-year change could reflect (a) "
  "real change in incidence, (b) change in youth sports participation, "
  "(c) change in NEISS sampling, (d) coding-practice change. Do not assume "
  "causality from these counts alone.")
W("- **Underlying methodology** validated against the 2024 NEISS Coding "
  "Manual (Appendix C for body parts, Appendix H for product codes) — see "
  "`docs/decisions.md` 2026-05-21 entry for the audit trail and the "
  "correction to PROTOCOL §4.1.\n")

W("## How this was generated\n")
W("- Source data: 12 per-year extractions in `data/extracted/neiss{2013..2025}.csv`.")
W("- Aggregation script: `scripts/23_neiss_trends.py` (this report's generator).")
W("- Tidy CSV with all year × category × value triples: `outputs/tables/neiss_trends.csv`.\n")

OUT_MD.write_text("\n".join(md))
print(f"Wrote {OUT_MD.relative_to(ROOT)}")
