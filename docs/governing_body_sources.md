# Governing-body and surveillance-system sources

PROTOCOL §3.2 explicitly allows non-peer-reviewed sources when they are "recognized national surveillance systems or sport-governing-body reports." §4.3 lists the targeted ones. This file is the audit trail for those grey-literature sources, separate from `sources.md` (which is PubMed/PMID-keyed).

**Schema** is the same `source_id` convention as `sources.md` — `<system_abbreviation_or_org><year>`. Each row gets a status from the same vocabulary (`identified` / `included` / `extracted` / `harmonized`).

Local copies of each PDF are under `data/raw/surveillance_reports/`. The `.gitignore` excludes that directory's `*.pdf` files from git — re-download from the canonical URL when needed.

---

## Sources

| source_id | citation_short | publisher / system | url | status | date_added | extractor | notes |
|---|---|---|---|---|---|---|---|
| aapd2025 | AAPD (2025). Policy on Prevention of Sports-Related Orofacial Injuries. Revised 2023, 2025–2026 edition. | American Academy of Pediatric Dentistry | https://www.aapd.org/media/policies_guidelines/p_sports.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | Policy document with 79 numbered references, embedded statistics (22k dental injuries/yr in <18yo from NEISS 1990–2003; 31.6/100k pop; HS sport-specific rates). Treat as a **secondary-source mining list** rather than primary epi — extract the numbered references for screening. |
| rio2008_09 | National HS Sports-Related Injury Surveillance Study — Summary Report, 2008–09 academic year. | Center for Injury Research and Policy / RIO™ (originally Nationwide Children's, now PIPER / Colorado SPH) | https://coloradosph.cuanschutz.edu/docs/librariesprovider204/default-document-library/2008-09.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | Annual RIO summary; methodology includes dental injuries regardless of time loss. |
| rio2009_10 | National HS Sports-Related Injury Surveillance Study — Summary Report, 2009–10 academic year. | Center for Injury Research and Policy / RIO™ | https://coloradosph.cuanschutz.edu/docs/librariesprovider204/default-document-library/2009-10.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | |
| rio2010_11 | National HS Sports-Related Injury Surveillance Study — Summary Report, 2010–11 academic year. | Center for Injury Research and Policy / RIO™ | https://coloradosph.cuanschutz.edu/docs/librariesprovider204/default-document-library/2010-11.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | |
| rio2011_12 | National HS Sports-Related Injury Surveillance Study — Summary Report, 2011–12 academic year. | Center for Injury Research and Policy / RIO™ | https://coloradosph.cuanschutz.edu/docs/librariesprovider204/default-document-library/2011-12.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | |
| rio2012_13 | National HS Sports-Related Injury Surveillance Study — Summary Report, 2012–13 academic year. | Center for Injury Research and Policy / RIO™ | https://coloradosph.cuanschutz.edu/docs/librariesprovider204/default-document-library/2012-13.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | |
| rio2016_17 | National HS Sports-Related Injury Surveillance Study — Summary Report, 2016–17 academic year. | Center for Injury Research and Policy / RIO™ | https://coloradosph.cuanschutz.edu/docs/librariesprovider204/default-document-library/2016-17.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | |
| rio2017_18 | National HS Sports-Related Injury Surveillance Study — Summary Report, 2017–18 academic year. | Center for Injury Research and Policy / RIO™ | https://coloradosph.cuanschutz.edu/docs/librariesprovider204/default-document-library/2017-18.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | |
| rio2018_19 | National HS Sports-Related Injury Surveillance Study — Summary Report, 2018–19 academic year. | Center for Injury Research and Policy / RIO™ | https://coloradosph.cuanschutz.edu/docs/librariesprovider204/default-document-library/2018-19.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | 130-page report; dental injuries reported regardless of time loss (see Methods, p. 11). |

**Gaps to fill on the next session** (years where the URL pattern returned 404):
- RIO 2013–14, 2014–15, 2015–16, 2019–20, 2020–21, 2021–22, 2022–23 — likely posted under different URL stems on PIPER's site. Search the PIPER project page directly: https://coloradosph.cuanschutz.edu (project search for "RIO" or "High School Sports-Related Injury Surveillance Study").
- NATA Position Statement on Preventing and Managing Sport-Related Dental and Oral Injuries (PMID 27875057 — already in `sources.md` as `E-noprim` exclusion; but the position statement itself does mine the primary literature in a useful way — consider promoting it to a secondary-source mining record like aapd2025).
- NCAA Injury Surveillance Program (NCAA ISP / Datalys) aggregate reports — datalys.org returned no response on 2026-05-23, likely the program migrated. Try ncaa.org/sportsscience or the SOSS data portal.

## Pending governing bodies (not yet searched)

Per PROTOCOL §4.3 these are listed but have not been canvassed yet:
- USA Hockey (https://www.usahockey.com) — no dedicated injury surveillance found in initial search; may have a Safety/Sport Sciences page worth checking manually.
- US Lacrosse (now USA Lacrosse)
- USA Wrestling
- USA Football
- USA Boxing
- NFHS (National Federation of State High School Associations) — has a Sports Medicine Advisory Committee
- International equivalents: Hockey Canada, Rugby Football Union (England), Hockey Australia — English-language

Manual exploration of each governing body's website is the most realistic next step (no programmatic API).

---

## How to extract from these sources

Most of these are PDF policy documents and PDF surveillance reports, not structured data files. Extraction workflow:

1. Read the methods section to confirm population, definitions, and denominator (AE vs population vs claims).
2. Pull tables that report dental / orofacial injuries.
3. Map columns to `DATA_DICTIONARY.md`. Cite the page number in `extraction_notes`.
4. Use `source_id` = the value in the table above (e.g. `rio2018_19`, `aapd2025`).
5. The `extractor` tag should include "PDF-page-N-extracted" so the audit trail is complete.

The RIO PDFs are the highest-value targets — each year report typically has a per-sport table that maps cleanly to a `sport` × `exposure_context` × `injury_count` × `athlete_exposures` row.
