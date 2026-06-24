#!/usr/bin/env python3
"""Export data/harmonized/master.csv to a SQLite database for easier querying.

Output: data/harmonized/master.sqlite with one table `master` containing all
columns. Numeric columns are typed appropriately. Includes a README with
sample queries.
"""

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data/harmonized/master.csv"
DB = ROOT / "data/harmonized/master.sqlite"

# Columns and their SQLite types
SCHEMA = {
    "source_id": "TEXT", "citation": "TEXT", "doi": "TEXT", "pub_year": "INTEGER",
    "study_type": "TEXT", "peer_reviewed": "TEXT",
    "country": "TEXT", "region": "TEXT", "population_setting": "TEXT",
    "age_min": "INTEGER", "age_max": "INTEGER", "age_category": "TEXT", "extraction_basis": "TEXT",
    "sex": "TEXT", "level_of_play": "TEXT",
    "sport_raw": "TEXT", "sport": "TEXT", "sport_category": "TEXT",
    "exposure_context": "TEXT", "subgroup_label": "TEXT",
    "sample_size": "INTEGER", "athlete_exposures": "INTEGER", "season_or_timeframe": "TEXT",
    "injury_count": "INTEGER", "injury_type_raw": "TEXT", "injury_category": "TEXT",
    "rate_raw": "REAL", "rate_denominator_raw": "TEXT", "rate_per_1000_ae": "REAL",
    "mouthguard_required": "TEXT", "mouthguard_use_rate": "REAL", "mouthguard_injury_relation": "TEXT",
    "extraction_date": "TEXT", "extractor": "TEXT", "extraction_notes": "TEXT",
    "quality_flag": "TEXT",
    "measure_type": "TEXT", "comparability_group": "TEXT", "data_provenance": "TEXT",
}

def coerce(value, sql_type):
    if value is None or value == "":
        return None
    try:
        if sql_type == "INTEGER":
            return int(float(value))
        if sql_type == "REAL":
            return float(value)
    except ValueError:
        return None  # silently drop bad numerics; row still inserted with NULL
    return value

# Remove existing DB and rebuild fresh
if DB.exists():
    DB.unlink()

conn = sqlite3.connect(DB)
cur = conn.cursor()

cols_sql = ", ".join(f'"{c}" {t}' for c, t in SCHEMA.items())
cur.execute(f"CREATE TABLE master ({cols_sql})")

# Insert rows
rows = list(csv.DictReader(open(MASTER)))
placeholders = ", ".join("?" * len(SCHEMA))
col_names = ", ".join(f'"{c}"' for c in SCHEMA)
for r in rows:
    vals = [coerce(r.get(c, ""), t) for c, t in SCHEMA.items()]
    cur.execute(f"INSERT INTO master ({col_names}) VALUES ({placeholders})", vals)

# Indexes for common queries
cur.execute("CREATE INDEX idx_sport ON master(sport)")
cur.execute("CREATE INDEX idx_country ON master(country)")
cur.execute("CREATE INDEX idx_age_category ON master(age_category)")
cur.execute("CREATE INDEX idx_source_id ON master(source_id)")
cur.execute("CREATE INDEX idx_pub_year ON master(pub_year)")

conn.commit()

# Verify
cur.execute("SELECT COUNT(*) FROM master")
n = cur.fetchone()[0]
cur.execute("SELECT COUNT(DISTINCT source_id) FROM master")
nsrc = cur.fetchone()[0]
conn.close()

print(f"Wrote {DB.relative_to(ROOT)} — {n} rows / {nsrc} sources")
print(f"  size: {DB.stat().st_size:,} bytes")

# Sample-query README
SAMPLE_MD = ROOT / "data/harmonized/README_sqlite.md"
SAMPLE_MD.write_text("""# master.sqlite — sample queries

This is `data/harmonized/master.csv` loaded into SQLite as a single table `master`.
Useful when you want a queryable view rather than parsing CSV.

## Open it

```bash
sqlite3 data/harmonized/master.sqlite
```

Or in Python:

```python
import sqlite3
conn = sqlite3.connect("data/harmonized/master.sqlite")
df = pd.read_sql_query("SELECT * FROM master WHERE sport = 'basketball'", conn)
```

## Sample queries

### All US HS basketball rows with a per-1000-AE rate
```sql
SELECT source_id, pub_year, sex, age_category, rate_per_1000_ae
FROM master
WHERE sport = 'basketball'
  AND country = 'US'
  AND age_category = 'adolescent'
  AND rate_per_1000_ae IS NOT NULL
ORDER BY rate_per_1000_ae;
```

### Year-by-year US NEISS aggregate counts
```sql
SELECT pub_year AS year, SUM(injury_count) AS total_cases
FROM master
WHERE source_id LIKE 'neiss____'
  AND sport = 'all_sports_aggregate'
  AND age_category = 'mixed'
  AND sex = 'mixed'
  AND subgroup_label = 'all_youth_aggregate'
GROUP BY pub_year
ORDER BY year;
```

### Sports represented in 5+ sources
```sql
SELECT sport, COUNT(DISTINCT source_id) AS source_count
FROM master
WHERE sport NOT LIKE 'all_%'
  AND sport NOT LIKE 'sports_%'
GROUP BY sport
HAVING source_count >= 5
ORDER BY source_count DESC;
```

### All mouthguard-use evidence sorted by use rate
```sql
SELECT source_id, sport, sex, mouthguard_use_rate, mouthguard_injury_relation
FROM master
WHERE mouthguard_use_rate IS NOT NULL
ORDER BY mouthguard_use_rate;
```

### Indexes available

```
idx_sport, idx_country, idx_age_category, idx_source_id, idx_pub_year
```

## Regenerating

```bash
python3 scripts/27_sqlite_export.py
```

This script reads `master.csv` and overwrites `master.sqlite`. Run it after every harmonization.
""")
print(f"Wrote {SAMPLE_MD.relative_to(ROOT)}")
