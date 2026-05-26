# master.sqlite — sample queries

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
