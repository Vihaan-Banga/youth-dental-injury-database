# Research Protocol: Youth Sports Dental Injury Database

**Status:** Draft v0.1 — pre-registration pending
**Last updated:** 2026-06-24
**Project lead:** Vihaan Banga (Olentangy Liberty High School)
**Advisor:** [TBD — outreach in progress, project lead leading recruitment independently]
**Pre-registration:** [OSF link when filed]

---

## 1. Background and rationale

Dental and orofacial injuries are among the most common facial injuries in youth sports, yet no unified data source documents their incidence across sports, age groups, and geographies. Existing data is fragmented across:

- National injury surveillance systems (NEISS, High School RIO, NCAA ISP)
- Peer-reviewed epidemiological studies
- Sport-governing-body injury reports
- International dental trauma registries

These sources use heterogeneous definitions (e.g., "dental trauma" vs. "orofacial injury" vs. "tooth avulsion"), inconsistent age categories, and different reporting denominators (per athlete-exposure, per season, per 1000 participants). The result: researchers, policymakers, and clinicians cannot easily compare findings across sources or aggregate evidence to inform prevention recommendations.

This project addresses that gap by harmonizing publicly available youth dental injury data into a single, citable, open-access database.

## 2. Research questions the database will support

The database is designed to enable researchers to answer questions including:

- What are the incidence rates of dental injuries across youth sports in published research?
- How do rates vary by age group, sex, level of play, and use of protective equipment?
- How have reported rates changed over time?
- What are the gaps in current surveillance coverage?

The project does not itself test specific hypotheses. It is an *infrastructure* project — a data resource for future research.

## 3. Scope and eligibility criteria

### 3.1 Inclusion criteria

A source is eligible if it meets *all* of the following:

- **Population:** Reports data on individuals aged 5–22 (i.e., youth through collegiate level)
- **Outcome:** Reports incidence, prevalence, or count of dental or orofacial injuries (see §3.3 for definitions)
- **Setting:** Sport-related injuries (organized or recreational athletic activity)
- **Geography:** No geographic restriction. International sources included.
- **Time:** Published or reported on or after January 1, 2000
- **Language:** English-language publications only (v1.0 limitation; multilingual expansion in future versions)
- **Data accessibility:** Numerical data extractable from the published report

### 3.2 Exclusion criteria

A source is excluded if it:

- Reports only on adults (>22) or only on children outside the age range
- Reports only non-sport-related dental trauma
- Is a single case report (n=1) or small case series (n<5)
- Reports only soft tissue injuries with no dental component
- Is a review article without primary data extraction tables (review articles may be used to *identify* primary sources but are not themselves extracted)
- Is a non-peer-reviewed source other than recognized national surveillance systems or sport-governing-body reports

### 3.3 Outcome definitions

For inclusion, a source must report at least one of:

- **Dental injury:** Tooth fracture (enamel, dentin, pulp), tooth luxation, tooth avulsion, root fracture
- **Orofacial injury with dental involvement:** Maxillofacial injury where dental structures are included in the reported count
- **Mouthguard usage data:** Self-reported or observed mouthguard use during the injury event

Sources reporting only lip lacerations, soft-tissue mouth injuries without dental involvement, or jaw fractures without tooth involvement are *not* included.

## 4. Source identification (search strategy)

### 4.1 Surveillance systems

- **NEISS** (Consumer Product Safety Commission): primary filter is **body part code 88 (Mouth — including lips, tongue, and teeth)**, the code that captures dental injuries; **76 (Face)** is used as a secondary filter only where the diagnosis text indicates dental involvement (per §3.3). Product code must be sport-related. Years 2000–most recent available. (The official 2024 NEISS Coding Manual codes are used; an earlier draft of this protocol mislabeled codes 76/77/88 — corrected per `docs/decisions.md`, 2026-05-21.)
- **High School RIO** (Nationwide Children's Hospital): All published reports.
- **NCAA Injury Surveillance Program:** Annual public reports.
- **National Health Interview Survey (NHIS)** subset on sports injuries.

### 4.2 Peer-reviewed literature

PubMed search using:
```
(("dental trauma"[tw] OR "dental injuries"[tw] OR "tooth avulsion"[tw] OR
  "orofacial injury"[tw] OR "dento-alveolar trauma"[tw])
 AND
 ("sport"[tw] OR "athletic"[tw] OR "youth sport"[tw] OR "school sport"[tw])
 AND
 ("epidemiology"[tw] OR "incidence"[tw] OR "prevalence"[tw] OR "surveillance"[tw])
 AND
 "2000"[dp]:"3000"[dp])
```

Plus targeted searches in *Dental Traumatology*, *Pediatric Dentistry*, *American Journal of Sports Medicine*, and *British Journal of Sports Medicine*.

### 4.3 Sport-governing-body reports

USA Hockey, US Lacrosse, USA Boxing, USA Wrestling, USA Football, NFHS injury reports, NATA position statements. International equivalents where English-language.

### 4.4 Screening process

Each candidate source goes through three stages, logged in `docs/sources.md`:

1. **Identified:** Source discovered, citation logged
2. **Screened:** Abstract/summary reviewed against §3.1 and §3.2 criteria
3. **Included:** Full text reviewed, marked for extraction

A second screener (advisor or peer) reviews 20% of screened sources to assess inter-rater reliability. Discrepancies resolved by discussion.

## 5. Data extraction

For each included source, the following fields are extracted into `data/extracted/<source_id>.csv` per the column definitions in `DATA_DICTIONARY.md`:

- Bibliographic info (citation, DOI, publication year, study type)
- Population (country, region, age range, sex, level of play)
- Exposure (sport, sport category, total athlete-exposures or sample size)
- Outcome (injury type, count, rate, denominator)
- Mouthguard data (use rate, mandate status) if reported

When a source reports multiple sports or subgroups, each is extracted as a separate row.

Extraction is performed by the project lead. A 10% random subsample is re-extracted independently by the advisor (or designee) to assess extraction reliability.

## 6. Harmonization

This is the methodological core of the project. The harmonization rules are:

### 6.1 Sport classification

All sports map to a controlled vocabulary defined in `DATA_DICTIONARY.md` (e.g., "basketball" includes both 5-on-5 and 3-on-3; "football" includes American football, distinguishing from soccer which is "association football"). The full taxonomy is maintained in `docs/decisions.md`.

### 6.2 Age categorization

Original age data preserved when available. Standardized categories applied for cross-source comparison:
- Youth (5–12)
- Adolescent (13–17)
- Collegiate (18–22)
- Adult (23+) — *comparator only*, see §6.2.1

When a source reports a range spanning categories, it is flagged and reported in whichever category contains the majority of the sample.

#### 6.2.1 Adult comparator rows

The v1.0 source-inclusion criterion (§3.1) is unchanged: a source qualifies iff it reports some data on individuals aged 5–22. Once a source clears that gate, however, all of its age-stratified rows are extracted, including adult bands when reported alongside youth. Adult rows are tagged `age_category = adult` and `extraction_basis = adult_comparator`; youth rows are tagged `extraction_basis = youth_primary`.

Rationale: many of the strongest surveillance sources (NEISS, ACC NZ, multi-age cohort studies) report youth and adult data together. Discarding the adult fraction at extraction would lose information that future researchers will value for cross-age comparison without changing the project's headline scope. See `DATA_DICTIONARY.md` ("Adult comparator rows") and `docs/decisions.md` (2026-05-22 decision).

### 6.3 Injury classification

Original injury terminology preserved in the `injury_type_raw` column. Standardized classification applied in `injury_category` per the Andreasen classification (the standard taxonomy in dental traumatology) **where the source reports a specific injury breakdown**. Most surveillance and epidemiology sources report aggregate dental-injury counts rather than avulsion/luxation/fracture splits; those rows take `injury_category = unspecified_dental`, with the verbatim source description retained in `injury_type_raw`.

### 6.4 Rate normalization

Original rate denominators preserved. A standardized `rate_per_1000_AE` (athlete-exposures) column added where the source provides sufficient data to compute it. Where computation requires assumptions, the assumption is logged in `docs/decisions.md`.

### 6.5 The decision log

**Every harmonization choice that is not mechanical gets logged in `docs/decisions.md`** with: the decision, the source(s) that prompted it, the reasoning, and the date. This is the difference between a defensible database and a black box.

## 7. Quality control

- All scripts version-controlled in git
- 10% sample of extracted data independently re-extracted by advisor
- All harmonization decisions logged
- Pre-extraction protocol pre-registered on OSF before data extraction begins
- Final dataset validated against §3 inclusion criteria before publication

## 8. Limitations (acknowledged upfront)

The following are known limitations to be stated transparently in the data descriptor:

- English-language sources only (v1.0)
- Publication bias: only published or publicly reported sources
- Heterogeneity in original data collection methods
- NEISS samples ER visits only; underestimates dental injuries treated in dental offices
- Surveillance systems often undercount because dental injuries may not be reported to athletic trainers
- v1.0 is a single-extractor project; expanded inter-rater reliability planned for v2.0

## 9. Outputs

- **Master dataset:** CSV with DOI, deposited on Zenodo, licensed CC BY 4.0. Contains both youth-primary and adult-comparator rows (see §6.2.1); the data descriptor's headline analyses use the youth-primary subset.
- **Data dictionary:** Public, versioned
- **Methods paper:** Submitted to *Data in Brief* (Elsevier) or *Scientific Data* (Nature) as a data descriptor
- **Project website:** Static site with interactive dashboard, hosted on free infrastructure
- **GitHub repository:** Public, MIT-licensed code

## 10. Timeline

- **Weeks 1–2:** Protocol finalization, advisor sign-off, OSF pre-registration
- **Weeks 3–4:** Source identification and screening
- **Weeks 5–7:** Data extraction
- **Week 8:** Harmonization, validation, publication
- **September–November:** Data descriptor paper drafting, Conrad Challenge submission

## 11. Authorship and contribution

- **Project lead:** Vihaan Banga (Olentangy Liberty High School) — conceived project, designed protocol, performed extraction and harmonization, drafted manuscript
- **Senior advisor:** [TBD] — provided methodological guidance, performed reliability review, reviewed manuscript

Both must approve v1.0 release before publication.

---

## 12. Data provenance and redistribution rights

This is a *secondary-data* project. It redistributes, under CC BY 4.0, only material it is entitled to share, and it contains **no raw or restricted microdata** from any access-controlled surveillance system. Every row carries a `data_provenance` flag (see DATA_DICTIONARY.md) classifying its source as one of:

- **`public_domain_raw`** — extracted from public-domain raw data. The only such source is **NEISS** (US Consumer Product Safety Commission), a public-use dataset. Master rows are *aggregated* yearly estimates, not raw case records (the raw NEISS query outputs are gitignored).
- **`published_summary`** — summary statistics already published in a peer-reviewed paper. We reproduce only the specific reported figures (counts, rates, prevalences) with full citation. Individual published facts are not themselves copyrightable; the *compilation* is what is licensed.
- **`governing_body_public`** — figures taken from a publicly released governing-body report (currently only the Rugby Europe 2024 Injury Surveillance Report). **[TODO: confirm the Rugby Europe report's reuse/redistribution terms before v1.0.]**

**Specifically, the database does NOT contain raw or restricted data from NCAA-ISP, High School RIO, or NZ ACC.** Where NCAA-ISP-, RIO-, or ACC-derived numbers appear, they are figures reported in a peer-reviewed publication (`data_provenance = published_summary`) — i.e., citing the published literature, not redistributing the owners' datasets. (Datasets such as NCAA-ISP are owned by their respective bodies and carry use restrictions; this project does not access or redistribute them.)

**Licensing framing:** the CC BY 4.0 data license covers *this project's harmonized compilation* (the schema, harmonization, classifications, and the assembled table). Underlying facts remain attributable to their original sources, every one of which is cited in the `citation` column and `outputs/sources_bibliography.bib`.

---

## Pre-registration checklist (complete before extraction begins)

- [ ] Protocol reviewed and signed off by advisor
- [ ] Inclusion/exclusion criteria finalized
- [ ] Search strategy validated against a test subset
- [ ] Data dictionary complete
- [ ] OSF pre-registration filed
- [ ] Repository initialized with git
- [ ] First two sources extracted as pilot

Only after all boxes checked does the main extraction phase begin.
