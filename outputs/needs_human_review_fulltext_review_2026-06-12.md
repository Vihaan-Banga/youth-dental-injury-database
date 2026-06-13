# Full-text review of the open-access `needs_human_review` subset — 2026-06-12

This logs the full-text review pass that resolved part of the 91-record
`needs_human_review` pile. It is the project lead's full-text screening step
(AI-assisted, same basis as the 2026-05-21 abstract screen). It is **not** the
PROTOCOL §4.4 20% inter-rater reliability re-screen, which still awaits the
advisor.

## How the candidate set was found

1. `scripts/30_oa_url_lookup.py` — Unpaywall best-OA-URL for all 91 records → 24 have a free full-text URL.
2. `scripts/31_pmc_availability.py` — NCBI `elink` PubMed→PMC for all 91 → 8 have a free PMC full text (6 of them BMJ papers whose publisher PDF 403s but whose PMC copy is reachable).

Union of fetchable records: 25 distinct PMIDs.

## How full text was retrieved

- **PMC HTML** (`pmc.ncbi.nlm.nih.gov/articles/PMCxxxxxxx/`) — cleanest; reads as text.
- **Repository / OA-journal PDFs** — WebFetch downloads the PDF bytes; text extracted with `pdfplumber`.
- **DOI redirects** to OA journals (e.g. Acta Odontologica on medicaljournalssweden.se) — followed.

## Outcomes

### Resolved — included (1)

| PMID | source_id | summary |
|---|---|---|
| 24198704 | **halabchi2007** | Women's Shotokan karate national championships, Iran, 2004-2005 (PMC3809047). 186 injuries / 1139 bouts / 1019 athletes; dental = 3 (1.6%) tooth avulsion/subluxation. Sport-related dental count + youth competitors present → included; extracted as 1 pooled mixed-age row. |

### Resolved — full-text excluded (6)

| PMID | source_id | reason | note |
|---|---|---|---|
| 15562172 | exadaktylos2004 | E-age | Swiss ED maxillofacial surveillance (PMC1724969); not age-stratified, facial fractures without separate dental count. |
| 16118304 | (n/a) | E-age | NZ rugby ecological MG study (PMC1725322); national all-ages ACC dental claims not separable to 5-22. |
| 19925982 | (n/a) | E-offtop | LA adolescents 14-20 orofacial trauma (PMC2782766); only 3% sport-related, no sport-specific data. |
| 2893649 | (n/a) | E-age | International (elite adult) field hockey (PMC1478470); no age data, no youth subset. |
| 36538371 | (n/a) | E-age | Finnish trauma-centre ice-hockey facial fractures (Acta Odontol Scand); adult-dominated (98.5% male), not age-stratified. |
| 39060115 | tadmor2025 | E-nodent | UK rugby league (brain) concussion symptom non-reporting (Leeds Beckett repository); no dental/orofacial injury outcome. |

### Reviewed but still `needs_human_review` (1)

| PMID | reason | note |
|---|---|---|
| 40662680 | R-age (confidence → low) | Swiss Muay Thai/K-1/kickboxing survey (Robbiani & Filippi 2025). Full text retrieved; reports all-ages dental injuries (52 cases, 19%; 8.7% during competition) and MG use (75% any, 31.5% professional). The subject **age distribution** sits in a PDF table that did not extract cleanly (readable strata are training-experience bands, not ages), so a 5-22 subset could not be confirmed/isolated. Needs a human read of the age table. |

### Not resolvable programmatically (stay `needs_human_review`)

- **Scanned page-image PMC records** (no OCR text): PMID 18254, 1982928, 6130812 (pre-1995 BJSM rugby papers).
- **Cloudflare / paywalled publisher PDFs** (403/402 to any non-browser client): Wiley `pdfdirect` (15853840, 19021650, 20666978, 21199336, 23374909, 25721283, 30431180, 37431232), JOMS (19615582), lww (25244279).
- **Repository 403 / URL 404:** Amsterdam UMC pure (25416466); Swiss Dental Journal download URLs (26678302, 27622524).

These need advisor library access or an interactive browser session (Chrome MCP).

## Net effect

- `needs_human_review`: **91 → 84**.
- master.csv: **425 → 426 rows**, **105 → 106 sources** (halabchi2007; +Iran, +karate via `martial_arts_other`).
- All 10 validation checks still pass: **0 FAILs, 0 WARNs**.
