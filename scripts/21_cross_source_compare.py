#!/usr/bin/env python3
"""Cross-source rate comparison — for sports we have multiple sources on,
compare their reported dental-injury rates side-by-side.

Goal: a sanity check on database internal consistency. If 5 sources for
basketball all report rates in the same order of magnitude, the database is
internally coherent; if they disagree by 10×, that's a red flag worth a note.

Outputs:
  - outputs/cross_source_rate_comparison.md (Markdown table by sport)
  - outputs/figures/cross_source_comparison.png (visual)
"""

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data/harmonized/master.csv"
OUT_MD = ROOT / "outputs/cross_source_rate_comparison.md"
OUT_PNG = ROOT / "outputs/figures/cross_source_comparison.png"

rows = list(csv.DictReader(open(MASTER)))

# Group by sport — collect rows with extractable numerical rate (rate_per_1000_ae)
# OR rate_raw with a clear AE-based denominator
sport_rows = defaultdict(list)
for r in rows:
    sport = r["sport"]
    if not sport or sport.startswith(("all_sports_", "all_activities_", "sports_",
                                       "non_sport", "recreational_")):
        continue
    rate_ae = r.get("rate_per_1000_ae", "")
    if not rate_ae:
        continue
    try:
        rate = float(rate_ae)
    except (TypeError, ValueError):
        continue
    sport_rows[sport].append({
        "source_id": r["source_id"], "year": r["pub_year"],
        "rate_per_1000_ae": rate, "country": r["country"],
        "age": r["age_category"], "sex": r["sex"],
        "denom": r["rate_denominator_raw"][:80],
        "subgroup": r.get("subgroup_label", ""),
    })

# Keep sports with >= 2 sources reporting per-1000-AE rates
multi_source = {sp: rs for sp, rs in sport_rows.items()
                if len({r["source_id"] for r in rs}) >= 2}

# -------- Markdown output --------
md = ["# Cross-source rate comparison\n",
      "_Auto-generated from `data/harmonized/master.csv`. "
      "Compares per-1000-athlete-exposure dental / orofacial injury rates across sources for each sport with >= 2 sources._\n"]

if not multi_source:
    md.append("No sport currently has >= 2 sources with `rate_per_1000_ae` populated.\n")
else:
    md.append(f"**Sports with multi-source AE-rate data:** {len(multi_source)}\n")
    md.append("\nNote: rates can legitimately differ across sources because of differences in:\n")
    md.append("- Definition of \"dental injury\" (some include lip lacerations; some don't)")
    md.append("- Age range (collegiate athletes can have 10× the rate of HS in some sports)")
    md.append("- Time period (rates have decreased with mouthguard mandates)")
    md.append("- Exposure denominator (athlete-exposures vs hours vs sessions)")
    md.append("- Subgroup (MG users vs nonusers; competition vs practice)")
    md.append("\nLarge spread across sources is expected; it does NOT mean the database is wrong.\n")
    for sport, srcs in sorted(multi_source.items()):
        srcs = sorted(srcs, key=lambda r: r["rate_per_1000_ae"])
        md.append(f"\n## {sport} ({len({s['source_id'] for s in srcs})} sources, {len(srcs)} rows)\n")
        md.append("| source_id | year | country | age | sex | rate /1000 AE | denominator phrasing | subgroup |")
        md.append("|---|---:|---|---|---|---:|---|---|")
        for s in srcs:
            md.append(f"| {s['source_id']} | {s['year']} | {s['country']} | {s['age']} | {s['sex']} | "
                      f"**{s['rate_per_1000_ae']:.3f}** | {s['denom']} | {s['subgroup']} |")
        # Compute spread
        rates = [s["rate_per_1000_ae"] for s in srcs]
        spread_ratio = max(rates) / min(rates) if min(rates) > 0 else float("inf")
        md.append(f"\n*Spread: min={min(rates):.3f}, max={max(rates):.3f}, ratio={spread_ratio:.1f}x*")

OUT_MD.write_text("\n".join(md))
print(f"Wrote {OUT_MD.relative_to(ROOT)}")

# -------- Figure: log-scaled scatter of rates by sport --------
sports_to_plot = sorted(multi_source.keys(),
                        key=lambda s: -len({r["source_id"] for r in multi_source[s]}))
if sports_to_plot:
    fig, ax = plt.subplots(figsize=(11, max(5, len(sports_to_plot) * 0.6)))
    palette = ["#4c72b0", "#dd8452", "#55a868", "#c44e52", "#8172b3",
               "#937860", "#da8bc3", "#8c8c8c", "#ccb974", "#64b5cd"]
    for y_pos, sport in enumerate(sports_to_plot):
        for s in multi_source[sport]:
            ax.scatter(s["rate_per_1000_ae"], y_pos,
                       s=60, alpha=0.7,
                       color=palette[hash(s["source_id"]) % len(palette)],
                       label=s["source_id"] if y_pos == 0 else None)
            ax.annotate(f"  {s['source_id']}",
                        (s["rate_per_1000_ae"], y_pos),
                        xytext=(5, 0), textcoords="offset points",
                        fontsize=7, color="#555", va="center")
    ax.set_yticks(range(len(sports_to_plot)))
    ax.set_yticklabels(sports_to_plot)
    ax.set_xscale("log")
    ax.set_xlabel("Dental / orofacial injury rate per 1000 athlete-exposures (log scale)")
    ax.set_title("Cross-source rate comparison — sports with ≥ 2 sources reporting AE-denominator rates")
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Wrote {OUT_PNG.relative_to(ROOT)}")
else:
    print("No multi-source data — skipped figure.")
