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
| rio2021_22 | NFHS / National HS Sports-Related Injury Surveillance Study — Summary Report, 2021–22 academic year. | NFHS / Center for Injury Research and Policy | https://khsaa.org/httpdocs/sportsmedicine/NFHS/High%20School%20RIO/2021-2022/2021-22%20NFHS%20ISS%20Summary%20Report%20-%20August%202022_FINAL.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | Found via Kentucky HS Athletic Association mirror; 8-page summary infographic (shorter than the older Colorado SPH reports). |
| rio2023_24 | NFHS / National HS Sports-Related Injury Surveillance Study — Summary Report, 2023–24 academic year. | NFHS / Center for Injury Research and Policy | https://www.mshsaa.org/resources/SportsMedicine/2023-24%20NFHS%20ISS%20Summary%20Report%20-%20August%202024%20-%20FINAL.pdf | included | 2026-05-23 | VB-AI-assisted-2026-05-23 | Found via Missouri State HS Activities Association mirror; 9-page summary. 19th annual edition of the surveillance program. |

**Gaps to fill on the next session** (years where the URL pattern returned 404):
- RIO 2013–14, 2014–15, 2015–16, 2019–20, 2020–21, 2021–22, 2022–23 — likely posted under different URL stems on PIPER's site. Search the PIPER project page directly: https://coloradosph.cuanschutz.edu (project search for "RIO" or "High School Sports-Related Injury Surveillance Study").
- NATA Position Statement on Preventing and Managing Sport-Related Dental and Oral Injuries (PMID 27875057 — already in `sources.md` as `E-noprim` exclusion; but the position statement itself does mine the primary literature in a useful way — consider promoting it to a secondary-source mining record like aapd2025).
- NCAA Injury Surveillance Program (NCAA ISP / Datalys) aggregate reports — datalys.org returned no response on 2026-05-23, likely the program migrated. Try ncaa.org/sportsscience or the SOSS data portal.

## International governing-body sources (canvassed 2026-05-24)

| source_id | citation_short | publisher | url | status | date_added | extractor | notes |
|---|---|---|---|---|---|---|---|
| world_rugby_iss_2023 | World Rugby Medical Commission (2024). 2023 Annual Injury Surveillance Review. | World Rugby | https://resources.worldrugby-rims.pulselive.com/worldrugby/document/2024/11/12/91fe0cef-ae77-4dec-8c35-192066e2adfa/6-c.-2023_MCC_Annual-ISS-Review.pdf | identified | 2026-05-24 | VB-AI-assisted-2026-05-24 | Adult elite rugby focus per protocol §3 — needs youth-subset review. Useful for cross-reference to youth-sport rugby data we have. |
| england_prisp_2022-23 | England Professional Rugby Injury Surveillance Project (2024). PRISP 2022-23 Report. | RFU / PRISP | https://keepyourbootson.co.uk/wp-content/uploads/2024/04/PRISP-22-23-Report.pdf | identified | 2026-05-24 | VB-AI-assisted-2026-05-24 | English professional rugby — adult, but useful denominators. 37 pages. |
| rugby_europe_iss_2024 | Rugby Europe (2024). Injury Surveillance Report March 2024. | Rugby Europe | https://www.rugbyeurope.eu/media/gxwdngx2/re-injury-surveillance-report-march-2024.pdf | identified | 2026-05-24 | VB-AI-assisted-2026-05-24 | Includes Under-20 and Under-18 championship data — DIRECTLY in scope. 16 pages. |
| orchard_afl_comparison | Orchard JW. (n.d.). Comparing AFL Injury Surveillance to other Codes. | John Orchard (independent) | https://www.johnorchard.com/resources/article-comparisoncodesSH.pdf | identified | 2026-05-24 | VB-AI-assisted-2026-05-24 | Methodological comparison piece; useful for harmonization decisions about AE denominators across rugby/AFL/soccer. 4 pages. |

**Not found / blocked**:
- USA Hockey (https://www.usahockey.com) — only player-facing claim forms publicly available; aggregate annual injury reports not public.
- Hockey Canada — same: player-facing injury report forms only, no aggregate.
- AFL annual injury reports (aflplayers.com.au, afl.com.au) — visible in WebSearch but pages return 403 to non-browser clients. User could fetch with Chrome MCP if needed.
- AIHW Sports Injury in Australia — 403 to WebFetch.
- US Lacrosse / USA Wrestling / USA Football / USA Boxing — searches did not surface aggregate injury surveillance reports beyond what RIO already covers (i.e., HS-level data is in RIO summaries we already have).

**Pending governing bodies (PROTOCOL §4.3) — not yet canvassed:**
- NFHS direct (their Sports Medicine Advisory Committee) — Have RIO via PIPER instead, which is funded by NFHS; likely redundant.

## Pending governing bodies (not yet searched)

Per PROTOCOL §4.3 these are listed but the original search may want manual exploration:
- USA Hockey (https://www.usahockey.com) — see note above.
- US Lacrosse (now USA Lacrosse)
- USA Wrestling
- USA Football
- USA Boxing

---

## How to extract from these sources

Most of these are PDF policy documents and PDF surveillance reports, not structured data files. Extraction workflow:

1. Read the methods section to confirm population, definitions, and denominator (AE vs population vs claims).
2. Pull tables that report dental / orofacial injuries.
3. Map columns to `DATA_DICTIONARY.md`. Cite the page number in `extraction_notes`.
4. Use `source_id` = the value in the table above (e.g. `rio2018_19`, `aapd2025`).
5. The `extractor` tag should include "PDF-page-N-extracted" so the audit trail is complete.

The RIO PDFs are the highest-value targets — each year report typically has a per-sport table that maps cleanly to a `sport` × `exposure_context` × `injury_count` × `athlete_exposures` row.
