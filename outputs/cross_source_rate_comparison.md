# Cross-source rate comparison

_Auto-generated from `data/harmonized/master.csv`. Compares per-1000-athlete-exposure dental / orofacial injury rates across sources for each sport with >= 2 sources._

**Sports with multi-source AE-rate data:** 4


Note: rates can legitimately differ across sources because of differences in:

- Definition of "dental injury" (some include lip lacerations; some don't)
- Age range (collegiate athletes can have 10× the rate of HS in some sports)
- Time period (rates have decreased with mouthguard mandates)
- Exposure denominator (athlete-exposures vs hours vs sessions)
- Subgroup (MG users vs nonusers; competition vs practice)

Large spread across sources is expected; it does NOT mean the database is wrong.


## baseball (2 sources, 2 rows)

| source_id | year | country | age | sex | rate /1000 AE | denominator phrasing | subgroup |
|---|---:|---|---|---|---:|---|---|
| radelet1996 | 1996 | US | mixed | mixed | **0.570** | per 100 player-hours (overall) |  |
| collins_baseball2008 | 2008 | US | adolescent | male | **1.260** | per 1000 athlete-exposures (HS baseball overall) |  |

*Spread: min=0.570, max=1.260, ratio=2.2x*

## basketball (3 sources, 4 rows)

| source_id | year | country | age | sex | rate /1000 AE | denominator phrasing | subgroup |
|---|---:|---|---|---|---:|---|---|
| azadani2023 | 2023 | US | adolescent | male | **0.024** | per 100,000 athlete-exposures |  |
| collins2016 | 2016 | US | adolescent | male | **0.026** | per 100,000 athlete-exposures |  |
| labella2002 | 2002 | US | collegiate | male | **0.120** | per 1000 athlete-exposures (custom-fitted MG users) | mouthguard_users |
| labella2002 | 2002 | US | collegiate | male | **0.670** | per 1000 athlete-exposures (non-MG users) | mouthguard_nonusers |

*Spread: min=0.024, max=0.670, ratio=27.9x*

## hockey_field (3 sources, 4 rows)

| source_id | year | country | age | sex | rate /1000 AE | denominator phrasing | subgroup |
|---|---:|---|---|---|---:|---|---|
| azadani2023 | 2023 | US | adolescent | female | **0.035** | per 100,000 athlete-exposures |  |
| collins2016 | 2016 | US | adolescent | female | **0.039** | per 100,000 athlete-exposures |  |
| yard2015 | 2015 | US | collegiate | female | **0.060** | per 1000 AE (dental specifically) | dental_subset |
| yard2015 | 2015 | US | collegiate | female | **0.940** | per 1000 AE (head/face/eye combined) | head_face_eye_aggregate |

*Spread: min=0.035, max=0.940, ratio=26.9x*

## rugby (2 sources, 10 rows)

| source_id | year | country | age | sex | rate /1000 AE | denominator phrasing | subgroup |
|---|---:|---|---|---|---:|---|---|
| rugby_europe_iss_2024 | 2024 |  | adolescent | male | **7.850** | per 1000 player-match-hours (head/face subset) | u18_men_trophy_headface |
| rugby_europe_iss_2024 | 2024 |  | adolescent | female | **11.780** | per 1000 player-match-hours (head/face subset) | u18_women_championship_headface |
| rugby_europe_iss_2024 | 2024 |  | adolescent | female | **15.200** | per 1000 player-match-hours (Sevens — U18 Women's Trophy) | u18_women_trophy |
| rugby_europe_iss_2024 | 2024 |  | adolescent | female | **15.240** | per 1000 player-match-hours (head/face subset) | u18_women_trophy_headface |
| collins_rugby2008 | 2008 | US | collegiate | male | **22.500** | per 1000 game athletic-exposures (male) | male_game |
| collins_rugby2008 | 2008 | US | collegiate | female | **22.700** | per 1000 game athletic-exposures (female) | female_game |
| rugby_europe_iss_2024 | 2024 |  | adolescent | female | **23.600** | per 1000 player-match-hours (Sevens — U18 Women's Championship) | u18_women_championship |
| rugby_europe_iss_2024 | 2024 |  | adolescent | male | **27.000** | per 1000 player-match-hours (head/face subset) | u18_men_championship_headface |
| rugby_europe_iss_2024 | 2024 |  | adolescent | male | **63.000** | per 1000 player-match-hours (Sevens — U18 Men's Championship) | u18_men_championship |
| rugby_europe_iss_2024 | 2024 |  | adolescent | male | **70.600** | per 1000 player-match-hours (Sevens — U18 Men's Trophy) | u18_men_trophy |

*Spread: min=7.850, max=70.600, ratio=9.0x*