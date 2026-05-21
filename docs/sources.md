# Source Tracking Log

Every candidate source — whether eventually included or excluded — is logged here. This creates an audit trail for the systematic review process required for publication.

**Status values:**
- `identified`: Citation found but not yet reviewed
- `screened_excluded`: Abstract reviewed, does not meet inclusion criteria. Reason required.
- `screened_included`: Abstract reviewed, meets criteria, pending full-text review
- `fulltext_excluded`: Full text reviewed, does not meet criteria. Reason required.
- `included`: Meets criteria, queued for extraction
- `extracted`: Data extracted into `data/extracted/<source_id>.csv`
- `harmonized`: Extracted data merged into master dataset

---

## Sources

| source_id | citation_short | status | reason_if_excluded | date_added | extractor |
|---|---|---|---|---|---|
| (example) collins2019 | Collins et al. (2019) — Dental injuries in HS sports | identified | | 2026-06-01 | JD |

<!-- Add new rows as sources are identified. Keep this table updated. -->

---

## Surveillance systems to query (separate from individual papers)

| system | url | status | notes |
|---|---|---|---|
| NEISS | https://www.cpsc.gov/cgibin/NEISSQuery/ | not_started | Free, public query interface |
| High School RIO | https://www.nationwidechildrens.org/research/areas-of-research/center-for-injury-research-and-policy/research-projects/high-school-rio | not_started | Published annual reports |
| NCAA ISP | https://www.datalys.org/ncaa-injury-surveillance-program/ | not_started | Aggregate reports public |

---

## Search history

Document every search query run, where, when, and how many results.

| date | source | query | results_count | screened_in | notes |
|---|---|---|---|---|---|
| | | | | | |

---

## Inter-rater check log

For 20% sample of screened sources reviewed by second screener (advisor):

| source_id | primary_decision | secondary_decision | agreement | resolution |
|---|---|---|---|---|
| | | | | |
