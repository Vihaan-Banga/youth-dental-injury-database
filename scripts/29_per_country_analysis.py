#!/usr/bin/env python3
"""Per-country breakdown of the database. Shows which countries are well-
represented and which are gaps — useful for advisor outreach and for the
methods paper's 'limitations' section.
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data/harmonized/master.csv"
OUT_MD = ROOT / "outputs/country_breakdown.md"
OUT_PNG = ROOT / "outputs/figures/country_breakdown.png"

rows = list(csv.DictReader(open(MASTER)))

# Aggregate by country
by_country = defaultdict(lambda: {
    "sources": set(), "rows": 0, "sports": set(),
    "min_year": None, "max_year": None, "total_injuries": 0,
})
for r in rows:
    c = r["country"] or "(no country tag)"
    e = by_country[c]
    e["sources"].add(r["source_id"])
    e["rows"] += 1
    if r["sport"] and not r["sport"].startswith(("all_", "sports_", "non_sport", "recreational_")):
        e["sports"].add(r["sport"])
    try:
        yr = int(r["pub_year"])
        e["min_year"] = min(e["min_year"], yr) if e["min_year"] else yr
        e["max_year"] = max(e["max_year"], yr) if e["max_year"] else yr
    except (TypeError, ValueError):
        pass
    try:
        n = int(float(r["injury_count"])) if r["injury_count"] else 0
        e["total_injuries"] += n
    except (TypeError, ValueError):
        pass

# Sort by source count desc
ranked = sorted(by_country.items(), key=lambda x: (-len(x[1]["sources"]), -x[1]["rows"]))

ISO_TO_NAME = {
    "US": "United States", "GB": "United Kingdom", "CA": "Canada",
    "AU": "Australia", "IE": "Ireland", "IL": "Israel", "IN": "India",
    "BR": "Brazil", "ZA": "South Africa", "LB": "Lebanon", "NZ": "New Zealand",
    "JP": "Japan", "TR": "Turkey", "ES": "Spain", "HU": "Hungary",
    "RO": "Romania", "AT": "Austria", "KR": "South Korea", "SY": "Syria",
    "LK": "Sri Lanka", "KW": "Kuwait", "CH": "Switzerland", "DE": "Germany",
    "FR": "France", "IT": "Italy", "NO": "Norway", "LT": "Lithuania",
    "LS": "Lesotho", "PR": "Puerto Rico", "MY": "Malaysia", "ID": "Indonesia",
    "PT": "Portugal", "TW": "Taiwan", "MX": "Mexico", "AR": "Argentina",
    "NG": "Nigeria", "EG": "Egypt", "SE": "Sweden", "FI": "Finland",
    "DK": "Denmark", "IR": "Iran",
}


# Markdown report
md = ["# Per-country breakdown\n",
      f"_Auto-generated from `data/harmonized/master.csv`. {len(by_country)} unique country tags across {len(rows)} rows._\n",
      "## Coverage table\n",
      "| country | sources | rows | distinct sports | year span | cumulative injury count |",
      "|---|---:|---:|---:|---|---:|"]

for code, e in ranked:
    yr_span = f"{e['min_year']}-{e['max_year']}" if e["min_year"] else "—"
    name = ISO_TO_NAME.get(code, code)
    md.append(f"| {name} (`{code}`) | {len(e['sources'])} | {e['rows']} | {len(e['sports'])} | {yr_span} | {e['total_injuries']:,} |")

md.append("\n## Geographic gaps & observations\n")
md.append("- **Heavily-represented regions:** Western Europe + UK, North America, Australia/NZ, parts of Asia (India, Japan, Turkey, Israel).")
md.append("- **Underrepresented regions:** Sub-Saharan Africa (only South Africa + Lesotho); Latin America (Brazil only); Middle East beyond Israel/Lebanon/Syria; nearly all of central + east Asia outside Japan/Korea.")
md.append("- **Reasons for gaps:**")
md.append("  - PROTOCOL §3.1 limits v1.0 to English-language sources — excludes substantial Spanish/Portuguese/Chinese/Arabic literature.")
md.append("  - Many low-/middle-income countries lack publicly published youth-sport injury surveillance.")
md.append("  - PubMed indexing skews toward English-publishing journals.")
md.append("- **Methods-paper implication:** the 'Limitations' section should explicitly note these gaps and frame the v1.0 dataset as North America + Anglophone-Europe + selected international, not truly global.\n")

md.append("## How to use this\n")
md.append("- For a researcher comparing youth dental injury rates across countries: the table gives row + source counts per country to indicate sample-size confidence.")
md.append("- For an advisor or peer reviewer: this is the answer to \"what's the geographic distribution of your sources?\"")
md.append("- For future v2.0 source-hunt prioritization: focus on countries with active youth-sport programs but currently 0–1 sources here (Brazil, Mexico, mainland China, francophone Africa).\n")

OUT_MD.write_text("\n".join(md))
print(f"Wrote {OUT_MD.relative_to(ROOT)}")

# Figure: bar chart of source count per country
top = ranked[:20]
plt.figure(figsize=(11, max(6, len(top) * 0.35)))
labels = [ISO_TO_NAME.get(c, c) for c, _ in top]
values = [len(e["sources"]) for _, e in top]
plt.barh(labels[::-1], values[::-1], color="#55a868")
plt.xlabel("Distinct sources contributing to master.csv")
plt.title(f"Source count by country — top {len(top)} of {len(by_country)}")
plt.tight_layout()
plt.savefig(OUT_PNG, dpi=160, bbox_inches="tight")
plt.close()
print(f"Wrote {OUT_PNG.relative_to(ROOT)}")
