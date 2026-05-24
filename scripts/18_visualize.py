#!/usr/bin/env python3
"""Generate baseline visualization PNGs from data/harmonized/master.csv.

Outputs under outputs/figures/. Intended for presentations to advisor /
Conrad judges. Each figure is a single PNG, simple style, no fancy theming.
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt

ROOT = Path("/Users/vihaanbanga/youth-dental-injury-database")
MASTER = ROOT / "data/harmonized/master.csv"
OUT = ROOT / "outputs/figures"
OUT.mkdir(parents=True, exist_ok=True)

# Load
rows = list(csv.DictReader(open(MASTER)))
print(f"Loaded {len(rows)} master.csv rows, {len(set(r['source_id'] for r in rows))} sources")


def save(name, dpi=150):
    plt.tight_layout()
    p = OUT / name
    plt.savefig(p, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"  -> {p.relative_to(ROOT)}")


# ---------------------------------------------------------------------
# 1. Rows per source (top 20)
# ---------------------------------------------------------------------
src_counts = Counter(r["source_id"] for r in rows)
top = src_counts.most_common(20)
labels = [s for s, _ in top]
values = [c for _, c in top]
plt.figure(figsize=(10, 6))
plt.barh(labels[::-1], values[::-1], color="#4c72b0")
plt.xlabel("Rows in master.csv")
plt.title(f"Rows per source (top 20 of {len(src_counts)} sources)")
save("rows_per_source_top20.png")


# ---------------------------------------------------------------------
# 2. Sport coverage — distinct sources per sport
# ---------------------------------------------------------------------
sport_to_sources = defaultdict(set)
for r in rows:
    s = r["sport"]
    if s and s not in ("all_sports_aggregate", "all_activities_aggregate",
                       "sports_aggregate", "recreational_mixed", "non_sport_setting"):
        sport_to_sources[s].add(r["source_id"])
sport_counts = sorted(sport_to_sources.items(), key=lambda x: -len(x[1]))
labels = [s for s, _ in sport_counts]
values = [len(srcs) for _, srcs in sport_counts]
plt.figure(figsize=(10, 7))
plt.barh(labels[::-1], values[::-1], color="#dd8452")
plt.xlabel("Distinct sources reporting this sport")
plt.title(f"Sport coverage — {len(sport_counts)} sport-specific values across sources")
save("sport_coverage.png")


# ---------------------------------------------------------------------
# 3. Country coverage — distinct sources per country
# ---------------------------------------------------------------------
country_to_sources = defaultdict(set)
for r in rows:
    c = r["country"]
    if c:
        country_to_sources[c].add(r["source_id"])
ctry = sorted(country_to_sources.items(), key=lambda x: -len(x[1]))
labels = [c for c, _ in ctry]
values = [len(s) for _, s in ctry]
plt.figure(figsize=(9, max(4, len(labels) * 0.3)))
plt.barh(labels[::-1], values[::-1], color="#55a868")
plt.xlabel("Distinct sources")
plt.title(f"Country coverage — {len(country_to_sources)} countries")
save("country_coverage.png")


# ---------------------------------------------------------------------
# 4. Year coverage — sources by pub_year
# ---------------------------------------------------------------------
year_to_sources = defaultdict(set)
for r in rows:
    try:
        y = int(r["pub_year"])
    except (TypeError, ValueError):
        continue
    year_to_sources[y].add(r["source_id"])
years = sorted(year_to_sources)
counts = [len(year_to_sources[y]) for y in years]
plt.figure(figsize=(10, 4))
plt.bar(years, counts, color="#c44e52", edgecolor="none")
plt.xlabel("Publication / treatment year")
plt.ylabel("Distinct sources")
plt.title(f"Year coverage — sources span {min(years)}–{max(years)}")
plt.xticks(rotation=45)
save("year_coverage.png")


# ---------------------------------------------------------------------
# 5. Age category distribution
# ---------------------------------------------------------------------
age_counts = Counter(r["age_category"] for r in rows if r["age_category"])
labels = list(age_counts.keys())
values = list(age_counts.values())
plt.figure(figsize=(7, 5))
colors = ["#4c72b0", "#dd8452", "#55a868", "#c44e52", "#8172b3", "#937860"]
plt.bar(labels, values, color=colors[:len(labels)])
plt.ylabel("Rows in master.csv")
plt.title("Rows by age category")
save("age_category_distribution.png")


# ---------------------------------------------------------------------
# 6. Extraction basis split (youth_primary vs adult_comparator)
# ---------------------------------------------------------------------
basis_counts = Counter(r["extraction_basis"] for r in rows if r["extraction_basis"])
plt.figure(figsize=(6, 5))
plt.pie(basis_counts.values(), labels=basis_counts.keys(),
        autopct="%1.1f%%", startangle=90,
        colors=["#4c72b0", "#c44e52"])
plt.title("Rows by extraction_basis (youth scope vs adult comparator)")
save("extraction_basis_split.png")


# ---------------------------------------------------------------------
# 7. Headline summary — combine sport + N (where N = sum of injury counts)
# ---------------------------------------------------------------------
sport_to_inj = defaultdict(int)
for r in rows:
    s = r["sport"]
    if not s or s.startswith(("all_sports_", "all_activities_", "sports_", "non_sport", "recreational_")):
        continue
    try:
        n = int(float(r["injury_count"])) if r["injury_count"] else 0
    except (TypeError, ValueError):
        n = 0
    sport_to_inj[s] += n
top_inj = sorted(sport_to_inj.items(), key=lambda x: -x[1])[:15]
labels = [s for s, _ in top_inj]
values = [v for _, v in top_inj]
plt.figure(figsize=(10, 6))
plt.barh(labels[::-1], values[::-1], color="#8172b3")
plt.xlabel("Total injury count across all sources in master.csv")
plt.title("Cumulative reported injury count by sport (top 15)")
save("injury_count_by_sport.png")


# ---------------------------------------------------------------------
# 8. Overall stats panel — one figure with 4 sub-stats
# ---------------------------------------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
ax = axes[0]
ax.axis("off")
ax.text(0.5, 0.6, f"{len(rows):,}", ha="center", fontsize=36, fontweight="bold", color="#4c72b0")
ax.text(0.5, 0.3, "rows in\nmaster.csv", ha="center", fontsize=12)
ax = axes[1]
ax.axis("off")
ax.text(0.5, 0.6, f"{len(src_counts):,}", ha="center", fontsize=36, fontweight="bold", color="#dd8452")
ax.text(0.5, 0.3, "distinct\nsources", ha="center", fontsize=12)
ax = axes[2]
ax.axis("off")
ax.text(0.5, 0.6, f"{len(country_to_sources):,}", ha="center", fontsize=36, fontweight="bold", color="#55a868")
ax.text(0.5, 0.3, "countries\nrepresented", ha="center", fontsize=12)
ax = axes[3]
ax.axis("off")
total_inj = sum(sport_to_inj.values())
ax.text(0.5, 0.6, f"{total_inj:,}", ha="center", fontsize=36, fontweight="bold", color="#c44e52")
ax.text(0.5, 0.3, "cumulative\nreported injuries", ha="center", fontsize=12)
plt.suptitle(f"Youth Sports Dental Injury Database — snapshot",
             fontsize=14, y=1.0)
save("headline_snapshot.png")

print(f"\nGenerated {len(list(OUT.glob('*.png')))} figures in {OUT.relative_to(ROOT)}/")
