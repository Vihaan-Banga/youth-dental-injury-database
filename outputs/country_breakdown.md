# Per-country breakdown

_Auto-generated from `data/harmonized/master.csv`. 30 unique country tags across 426 rows._

## Coverage table

| country | sources | rows | distinct sports | year span | cumulative injury count |
|---|---:|---:|---:|---|---:|
| United States (`US`) | 40 | 306 | 21 | 1996-2026 | 679,607 |
| (no country tag) (`(no country tag)`) | 6 | 17 | 5 | 2010-2025 | 329 |
| Canada (`CA`) | 6 | 11 | 3 | 2002-2021 | 3,982 |
| Turkey (`TR`) | 6 | 7 | 4 | 2005-2026 | 306 |
| Japan (`JP`) | 4 | 11 | 1 | 2016-2023 | 5,709 |
| India (`IN`) | 4 | 9 | 1 | 2014-2017 | 660 |
| United Kingdom (`GB`) | 4 | 5 | 0 | 2000-2009 | 764 |
| Australia (`AU`) | 4 | 4 | 2 | 2005-2024 | 91 |
| Ireland (`IE`) | 4 | 4 | 1 | 2011-2023 | 65 |
| New Zealand (`NZ`) | 3 | 18 | 8 | 2010-2020 | 13,013 |
| Israel (`IL`) | 3 | 5 | 2 | 2003-2008 | 644 |
| Iran (`IR`) | 2 | 2 | 1 | 2007-2020 | 58 |
| Syria (`SY`) | 2 | 2 | 0 | 2026-2026 | 476 |
| Brazil (`BR`) | 2 | 2 | 0 | 2001-2006 | 133 |
| Norway (`NO`) | 2 | 2 | 0 | 2003-2019 | 102 |
| Austria (`AT`) | 1 | 3 | 2 | 1997-1997 | 1,163 |
| Lebanon (`LB`) | 1 | 3 | 0 | 2021-2021 | 861 |
| Lithuania (`LT`) | 1 | 2 | 0 | 2020-2020 | 420 |
| Sri Lanka (`LK`) | 1 | 2 | 0 | 2024-2024 | 800 |
| Kuwait (`KW`) | 1 | 1 | 1 | 2019-2019 | 169 |
| Puerto Rico (`PR`) | 1 | 1 | 0 | 2005-2005 | 18 |
| South Korea (`KR`) | 1 | 1 | 0 | 2021-2021 | 517 |
| Spain (`ES`) | 1 | 1 | 1 | 2020-2020 | 163 |
| Italy (`IT`) | 1 | 1 | 1 | 2024-2024 | 18 |
| Taiwan (`TW`) | 1 | 1 | 0 | 2009-2009 | 387 |
| Romania (`RO`) | 1 | 1 | 0 | 2012-2012 | 0 |
| Lesotho (`LS`) | 1 | 1 | 0 | 2008-2008 | 0 |
| Hungary (`HU`) | 1 | 1 | 0 | 2001-2001 | 590 |
| Switzerland (`CH`) | 1 | 1 | 1 | 2012-2012 | 31 |
| South Africa (`ZA`) | 1 | 1 | 0 | 2009-2009 | 106 |

## Geographic gaps & observations

- **Heavily-represented regions:** Western Europe + UK, North America, Australia/NZ, parts of Asia (India, Japan, Turkey, Israel).
- **Underrepresented regions:** Sub-Saharan Africa (only South Africa + Lesotho); Latin America (Brazil only); Middle East beyond Israel/Lebanon/Syria; nearly all of central + east Asia outside Japan/Korea.
- **Reasons for gaps:**
  - PROTOCOL §3.1 limits v1.0 to English-language sources — excludes substantial Spanish/Portuguese/Chinese/Arabic literature.
  - Many low-/middle-income countries lack publicly published youth-sport injury surveillance.
  - PubMed indexing skews toward English-publishing journals.
- **Methods-paper implication:** the 'Limitations' section should explicitly note these gaps and frame the v1.0 dataset as North America + Anglophone-Europe + selected international, not truly global.

## How to use this

- For a researcher comparing youth dental injury rates across countries: the table gives row + source counts per country to indicate sample-size confidence.
- For an advisor or peer reviewer: this is the answer to "what's the geographic distribution of your sources?"
- For future v2.0 source-hunt prioritization: focus on countries with active youth-sport programs but currently 0–1 sources here (Brazil, Mexico, mainland China, francophone Africa).
