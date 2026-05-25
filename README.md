# Youth Sports Dental Injury Database

An open-access harmonized database aggregating epidemiological data on dental and orofacial injuries in youth sports, drawn from national surveillance systems, published research, and sport-governing-body reports.

**Status:** Pre-launch (data collection phase). Not yet published. Do not cite externally until v1.0 release.

**Project lead:** Vihaan Banga, Olentangy Liberty High School, in collaboration with [Advisor name when secured], OSU College of Dentistry.

## What this is and isn't

This is a *secondary data* project. We are not collecting injuries directly from athletes or clinicians. We are aggregating data that has already been collected and published by national surveillance systems, peer-reviewed studies, and sport-governing-body injury reports, then standardizing it into a single comparable format.

The gap we fill: youth dental injury data exists in dozens of fragmented sources using different definitions, age ranges, and injury classifications. No unified resource lets a researcher answer questions like "what is the rate of avulsed teeth across youth contact sports in North America?" without manually reconciling 40 papers. We are building that resource.

## Repository structure

```
youth-dental-injury-database/
├── README.md                  This file
├── PROTOCOL.md                Pre-registered research protocol — read this first
├── DATA_DICTIONARY.md         Column-by-column definitions of the master dataset
├── data/
│   ├── raw/                   Original downloaded sources (NEISS CSVs, paper PDFs)
│   │   ├── neiss/
│   │   ├── papers/
│   │   └── surveillance_reports/
│   ├── extracted/             Tables and figures extracted from each source
│   ├── cleaned/               Per-source cleaned data, one file per source
│   └── harmonized/            The unified database (master.csv)
├── scripts/                   Python scripts for download, extraction, harmonization
├── docs/
│   ├── sources.md             Running list of all candidate sources with status
│   ├── decisions.md           Log of every harmonization decision and why
│   └── meeting_notes/         Notes from advisor meetings
└── outputs/
    ├── figures/               Charts for the methods paper and website
    └── tables/                Summary tables
```

## How to use this repo (workflow)

1. **Read PROTOCOL.md first.** It defines what's in, what's out, and how decisions get made.
2. **Add candidate sources to `docs/sources.md`** as you find them. Mark status (identified → screened → included → extracted → harmonized).
3. **Extract data from included sources** into `data/extracted/<source_id>.csv` using the template in `DATA_DICTIONARY.md`.
4. **Log every non-obvious harmonization decision** in `docs/decisions.md`. When a future reviewer asks "why did you classify X this way?" — you need an answer.
5. **Run harmonization scripts** to build `data/harmonized/master.csv`.
6. **Commit early and often.** Every meaningful change gets a git commit with a clear message.

## How this will be cited (when published)

```
Banga, V., [Advisor name]. (2026). Youth Sports Dental Injury Database (Version 1.0)
[Data set]. Zenodo. https://doi.org/[TBD]
```

A formal `CITATION.cff` file will be added at publication.

## License

- **Code:** MIT — see [`LICENSE`](LICENSE)
- **Data:** Creative Commons Attribution 4.0 International (CC BY 4.0) — see [`LICENSE-DATA`](LICENSE-DATA)

Use the code freely (with attribution per MIT). Use the data freely (with attribution per CC BY 4.0). The two-license split is standard for open-research projects: open code, open data.

## Contact

Vihaan Banga — GitHub [@Vihaan-Banga](https://github.com/Vihaan-Banga) ([email to be added])
