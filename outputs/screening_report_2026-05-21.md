# Screening Report — PubMed seed of 2026-05-21

_Generated 2026-05-22 from `data/extracted/_screening/screening_decisions.csv`._

## What this is

This is the audit trail for the first-pass screening of the 200 PubMed candidates seeded on 2026-05-21. Decisions were made by reading **title + abstract + publication-type metadata only** — no full texts have been reviewed yet.

**This is not a final screening decision.** Per PROTOCOL.md §4.4, the project lead is the primary screener and an advisor (or designee) second-screens 20% of records. Treat each row below as the AI-assisted screener's recommendation; verify before promoting any record to `included`.

**Where to start as the human screener:** 

1. **Spot-check exclusions first.** Wrong exclusions cost the most because excluded records exit the audit. The high-confidence excludes (non-English, case reports, off-topic) are low-risk; the `E-age` and `E-noprim` excludes are worth confirming.

2. **Then work through `needs_human_review`.** Most of these are blocked on age range or sport-related subset visibility — answerable from the methods section of the full text.

3. **Then second-screen 20% of the `screened_included` rows** to satisfy PROTOCOL §4.4 inter-rater reliability.


## Totals

- `screened_included`: **73**
- `needs_human_review`: **63**
- `screened_excluded`: **64**
- Total: **200**

---

## screened_included  (73)

### I-pri — Primary epidemiology — sport-related dental/orofacial injury data, ages overlap 5–22  (73)

- **42052228** (2026) — Epidemiology of Softball Injuries Comparison of Softball-Related Injuries at US Emergency Departments Between High School and Collegiate Athletes: A 10-Year NEISS Analysis, 2015-2024.
  - confidence: `high` — 10-yr NEISS analysis 2015–2024 comparing HS vs collegiate softball injuries — direct §3.1 fit with AE-comparable data.
- **41501720** (2026) — Prevalence and risk factors of orofacial trauma among child and adolescent athletes in Damascus, Syria: a cross-sectional study.
  - confidence: `high` — n=445 child/adolescent athletes 6–16 Damascus Syria; orofacial trauma prevalence + risk factors.
- **40917008** (2026) — Epidemiology of Orofacial Trauma in Syrian Pediatric Athletes: A Cross-Sectional Study on Prevalence and Injury Patterns.
  - confidence: `high` — n=582 Syrian child athletes 6–16; orofacial-dental trauma prevalence + injury patterns + protective gear — direct §3.1 fit.
- **40771058** (2026) — Youth Basketball Players' Awareness and Experiences of Sports-Related Traumatic Dental Injuries and Mouthguards in Turkey: A Cross-Sectional Study.
  - confidence: `high` — n=125 youth basketball players Turkey 2024–25 season; TDI prevalence + mouthguard knowledge — direct §3.1 fit.
- **40655786** (2025) — Prevalence and Outcomes of Dental Trauma in Sports-Related Injuries in the Last 2 Years.
  - confidence: `high` — Retrospective 100-case sports-related dental trauma study with focus on children/adolescents and contact sports.
- **39452438** (2024) — Traumatic Dental Injuries: Prevalence, First Aid, and Mouthguard Use in a Sample of Italian Kickboxing Athletes.
  - confidence: `high` — PMC full-text confirms n=142 amateur athletes ages 5–65; n=38 (27%) are under 18 (youth subset). Source qualifies for inclusion; per the 2026-05-22 decision, youth rows tagged youth_primary and adult rows tagged adult_comparator. [Resolved via PMC11505621 full-text fetch, 2026-05-22.]
- **39297708** (2024) — Permanent tooth avulsions: A retrospective analysis of the demographics and aetiology of cases at a tertiary hospital in Sydney, Australia.
  - confidence: `high` — Sydney tertiary hospital 2001–2021 avulsion cohort, median age 12 (IQR 9–17); non-organized sport = most common cause — youth + sport fit.
- **38131151** (2024) — Oro-dental trauma burden and mouthguard usage among contact sports players: A call for sports dentistry initiatives in Sri Lanka.
  - confidence: `high` — n=1340 adolescent contact-sport players Colombo Sri Lanka; oro-dental trauma burden + mouthguard usage — perfect §3.1 fit.
- **37818921** (2024) — Mechanisms of dental injuries in basketball, United States, 2003-2022.
  - confidence: `high` — NEISS basketball dental injury mechanisms 2003–2022; primary mechanism data.
- **37743045** (2023) — Trends in Soccer-Related Craniomaxillofacial Injuries, United States 2003-2022.
  - confidence: `high` — NEISS retrospective 2003–2022 soccer craniomaxillofacial injuries; demographic stratification — youth subset extractable.
- **36929194** (2023) — Head injuries caused by contact with teeth during sports and exercise activities in Japanese schools during the period 2012-2018.
  - confidence: `high` — Japan school head injuries from tooth contact 2012–2018; school-age population by definition; primary count data.
- **36428271** (2023) — Quantitative text analysis of the mechanisms of tooth injury: Analysis of accidents in five sports that occurred in 15 years under school control.
  - confidence: `high` — n=7684 Japan school dental injury cases over 15 years across 5 sports — large governing-body surveillance dataset.
- **36394781** (2023) — Assessment of mouthguards worn by Irish children playing contact sports: an observational cross-sectional cohort study.
  - confidence: `high` — PMC full-text confirms n=106 children aged 9–16 (squarely within scope). Sport = Gaelic football (contact). Primary outcome is MG design adequacy, but the paper carries TDI prevalence data for the cohort as a §3.3 outcome. [Resolved via PMC9669524 full-text fetch, 2026-05-22.]
- **36317716** (2023) — Traumatic dental injuries in high school athletes in the United States of America from 2005 to 2020.
  - confidence: `high` — National HS Sports-Related Injury Surveillance Study 2005/06–2019/20; dental injury counts + AE + mouthguard utilization — directly extractable.
- **34879017** (2022) — Baseball-Related Craniofacial Injury Among the Youth: A National Electronic Injury Surveillance System Database Study.
  - confidence: `high` — NEISS baseball craniofacial injuries youth (5–19) — perfect §3.1 age + sport fit, primary surveillance dataset.
- **34643329** (2021) — Cross-sectional cohort study on the use of mouthguards by children playing Gaelic football in Ireland.
  - confidence: `high` — Cross-sectional observational cohort 9–16 yr Gaelic football children + parents; MG knowledge + dental trauma.
- **33848349** (2021) — Sex-Based Differences in Symptoms With Mouthguard Use After Pediatric Sport-Related Concussion.
  - confidence: `high` — Prospective cohort 9 Canadian pediatric EDs, ages 5–18 with sport-related concussion + mouthguard outcomes — direct §3.3 fit.
- **33746633** (2021) — Prevalence and Etiological Factors of Dental Trauma among 12- and 15-Year-Old Schoolchildren of Lebanon: A National Study.
  - confidence: `high` — n=7902 12- and 15-yr-old Lebanese schoolchildren national TDI study — large sample, perfect age fit.
- **33741876** (2021) — Kick Start to an Epidemiological Report of Soccer-Related Craniofacial Trauma Analysis.
  - confidence: `high` — 10-yr NEISS soccer craniofacial injuries with demographic stratification — youth subset extractable.
- **33710063** (2021) — Skating on Thin Ice: Craniofacial Injuries in Amateur Ice Hockey.
  - confidence: `high` — 10-yr NEISS amateur ice hockey craniofacial injuries; explicit youth/amateur/professional breakdown — youth subset extractable.
- **33710051** (2021) — Prevalence of Dentofacial Injuries and Concussions Among College Athletes and Their Perceptions of Mouthguards.
  - confidence: `high` — n=682 NCAA Division I college athletes Columbia; dento-facial injury + concussion + mouthguard — college fits.
- **33654038** (2021) — Heads Up Play: Acute Assessment and Management of Basketball-Related Craniofacial Injuries by On-Court Personnel.
  - confidence: `high` — 10-yr NEISS retrospective cohort of basketball-related craniofacial injuries; on-court management focus but primary epi data available.
- **33292522** (2020) — Random forest algorithm to identify factors associated with sports-related dental injuries in 6 to 13-year-old athlete children in Hamadan, Iran-2018 -a cross-sectional study.
  - confidence: `high` — Children 6–13 Hamadan Iran sports-related dental injury study (random forest); primary data on athletes.
- **31765062** (2020) — Experience with mouthguards and prevalence of orofacial injuries among field hockey players in Catalonia.
  - confidence: `high` — n=325 Catalonia field hockey players 'all age categories' incl. women; sport-specific orofacial injury + mouthguard data.
- **31624810** (2020) — Dental Trauma Experience, Attitudes and Trauma Prevention in 11- to 13-Year-Old Lithuanian Schoolchildren.
  - confidence: `high` — Lithuanian 11–13 schoolchildren with focus on contact-sport mouthguard use; TDI prevalence + sport-specific data.
- **31506903** (2020) — Injury Risk in New Zealand Rugby Union: A Nationwide Study of Injury Insurance Claims from 2005 to 2017.
  - confidence: `high` — NZ ACC rugby injury claims 2005–2017 ages 5–40 with differences by age — large surveillance, youth subset (5–22) directly extractable.
- **31228311** (2019) — Traumatic dental injuries and experiences along the life course - a study among 16-yr-old pupils in western Norway.
  - confidence: `high` — n=2055 16-yr-old Norwegian pupils retrospective longitudinal TDI; life-course risk factors.
- **31179757** (2019) — Pediatric Sports- and Recreation-Related Dental Injuries Treated in US Emergency Departments.
  - confidence: `high` — NEISS pediatric sports/recreation dental injuries treated in US EDs — large-scale surveillance, exactly the kind of source PROTOCOL §4.1 targets.
- **30865370** (2019) — Prevalence and severity of traumatic dental injuries among young amateur soccer players: A screening investigation.
  - confidence: `high` — Amateur soccer players 7–18 Kuwait; TDI prevalence/type/causes — perfect age + sport fit.
- **29526055** (2018) — Knowledge and attitudes about sports-related dental injuries and mouthguard use in young athletes in four different contact sports-water polo, karate, taekwondo and handball.
  - confidence: `high` — n=229 young athletes 4 contact sports (water polo/karate/taekwondo/handball); sport-related dental injury + mouthguard.
- **29406619** (2018) — Oral injuries related to Ice Hockey in the province of Alberta, Canada: Trends over the last 15 years.
  - confidence: `high` — Hockey Alberta surveillance 2001–2016 'all ages'; rates + mechanisms — youth subset extractable from governing-body dataset.
- **29403232** (2017) — Evaluation of Knowledge, Awareness, and Occurrence of Dental Injuries in Participant Children during Sports in New Delhi: A Pilot Study.
  - confidence: `high` — n=450 children 6–16 New Delhi; dental injury prevalence during sport + mouthguard awareness — direct fit.
- **29284466** (2017) — Factors associated with sports-related dental injuries among young athletes: a cross-sectional study in Miyagi prefecture.
  - confidence: `high` — School-aged athletes Miyagi prefecture Japan; sports-related dental injury prevalence + risk factors — explicit §3.3 outcome.
- **28969286** (2017) — Traumatic Dental Injuries Prevalence and their Impact on Self-esteem among Adolescents in India: A Comparative Study.
  - confidence: `high` — PMC full-text confirms population is 10–17 yr adolescents (squarely within scope). Primary outcome is TDI prevalence with self-esteem comparison; sport activities are listed as a primary etiology. [Resolved via PMC5620908 full-text fetch, 2026-05-22.]
- **28054391** (2017) — Head injuries in children's football-results from two prospective cohort studies in four European countries.
  - confidence: `high` — Prospective cohort study of organized football in 7–12 yr children across 4 European countries; head/neck injuries documented — age fit + sport-specific.
- **27452795** (2016) — Descriptive study of dental injury incurred by junior high school and high school students during participation in school sports clubs.
  - confidence: `high` — Japan junior HS + HS school sports clubs dental injury risk by sport; school-age population (mostly 12–18).
- **26408377** (2016) — Dental injuries sustained by high school athletes in the United States, from 2008/2009 through 2013/2014 academic years.
  - confidence: `high` — National HS Sports-Related Injury Surveillance Study 2008/09–2013/14; n=222 dental injuries with AE-denominator data per sport — gold-standard.
- **25881567** (2016) — Mouthguard Use and Awareness of Junior Rugby League Players in the Gold Coast, Australia: A Need for More Education.
  - confidence: `high` — n=494 junior rugby league players + coaches Gold Coast; knowledge + TDI experience — junior population fits.
- **26093006** (2015) — Head, Face, and Eye Injuries in Collegiate Women's Field Hockey.
  - confidence: `high` — Collegiate women's field hockey head/face/eye injury epidemiology; college age within 18–22 — direct sport+age fit.
- **25520762** (2014) — A study of sports related occurrence of traumatic orodental injuries and associated risk factors in high school students in north India.
  - confidence: `high` — n=cross-sectional HS students 8–16 in North India organized sports teams; sport-related orodental injury prevalence.
- **25500920** (2014) — Dental trauma and mouthguard awareness and use among contact and noncontact athletes in central India.
  - confidence: `high` — Cross-sectional athletes 12–22 in central India contact vs noncontact; mouthguard awareness + injury rates — perfect §3.1 age + sport fit.
- **23532813** (2013) — Incidence and prevention of traumatic injuries in paediatric handball players in Istanbul, Turkey.
  - confidence: `high` — Pediatric handball players Istanbul amateur national league; TDI frequency + mouthguard knowledge — sport + youth fit.
- **23045787** (2012) — Mouthguard use and dental injury in sport: a questionnaire study of national school children in the west of Ireland.
  - confidence: `high` — n=1111 Irish children ages 9–13; mouthguard use + dental trauma in sport — directly addresses §3.3.
- **22976571** (2012) — Prevalence of traumatic dental injuries in children who attended two dental clinics in Targu Mures between 2003 and 2011.
  - confidence: `high` — Targu Mures retrospective study, ages 1–18, with physical-activity risk factor — youth-specific TDI data.
- **21457187** (2011) — Orofacial and dental trauma of young children in Dunedin, New Zealand.
  - confidence: `high` — Dunedin NZ children 0–10 orofacial trauma audit; sport contributes to causes in older subgroup.
- **21299945** (2011) — Clinical audit of children with permanent tooth injuries treated at a dental hospital in Ireland.
  - confidence: `high` — Cork University Dental School pediatric trauma audit; cause and prevalence by type — primary clinical data.
- **21197817** (2010) — ACC claims for sports-related dental trauma from 1999 to 2008: a retrospective analysis.
  - confidence: `high` — NZ ACC sports-related dental insurance claims 1999–2008; ~25–31k claims/year with age/sex/region/sport breakdown — large-scale surveillance, youth subset extractable.
- **21063551** (2010) — Prevalence and patterns of combat sport related maxillofacial injuries.
  - confidence: `high` — PMC full-text confirms ages 18–25 (mean ~22). Within-scope: 18–22 subset = youth_primary; 23–25 subset = adult_comparator (decision 2026-05-22). Combat sports (boxing/taekwondo/kickboxing/Muay Thai). [Resolved via PMC2966561 full-text fetch, 2026-05-22.]
- **20486946** (2010) — Orofacial and dental injuries of snowboarders in Turkey.
  - confidence: `high` — Snowboarders Turkey n=86; framed as 'adolescent and young adult' — within 5–22 envelope.
- **19614738** (2009) — Consumer products and activities associated with dental injuries to children treated in United States emergency departments, 1990-2003.
  - confidence: `high` — NEISS analysis 1990–2003 of dental injuries to children 0–17; consumer products + activities including sport — primary surveillance dataset.
- **19566982** (2009) — A pilot study of the prevalence of orofacial and head injuries in schoolboy cricketers at eight private schools in England and Australia.
  - confidence: `high` — n=411 schoolboy cricketers at 8 private schools England + Australia; head/face/dental prevalence by country — strong sport+age fit.
- **19290905** (2009) — Traumatic dental injuries of permanent incisors in 11- to 13-year-old South African schoolchildren.
  - confidence: `high` — Random cluster sample of n=2610 South African 11–13 schoolchildren; TDI prevalence.
- **19208012** (2009) — Activities related to the occurrence of traumatic dental injuries in 15- to 18-year-olds.
  - confidence: `high` — Random sample of n=6312 Taiwanese 15–18 yr senior HS students; TDI prevalence + activity-related etiology.
- **19030141** (2008) — Epidemiology of rare injuries and conditions among United States high school athletes during the 2005-2006 and 2006-2007 school years.
  - confidence: `high` — RIO surveillance HS athletes 2005/06 and 2006/07; dental injuries are one of the RIC categories reported.
- **18821957** (2008) — The relationship between sports activities and permanent incisor crown fractures in a group of school children aged 7-9 and 11-13 in Ankara, Turkey.
  - confidence: `high` — n=2570 Ankara schoolchildren ages 7–9 and 11–13; specifically studies the role of sport in crown fractures.
- **18721348** (2008) — Dental trauma among 5th and 6th grade Arab schoolchildren in Eastern Jerusalem.
  - confidence: `high` — 5th–6th grade Arab schoolchildren Jerusalem n=453; TDI prevalence + etiology.
- **18689347** (2008) — Causes and prevalence of traumatic injuries to the permanent incisors of school children aged 10-14 years in Maseru, Lesotho.
  - confidence: `high` — Schoolchildren 10–14 Maseru Lesotho; permanent incisor TDI prevalence and etiology.
- **18410389** (2008) — Etiology and environment of dental injuries in 12- to 14-year-old Ontario schoolchildren.
  - confidence: `high` — Population-based case-comparison study of n=2422 Ontario schoolchildren ages 12 and 14; primary etiology data.
- **17991235** (2007) — Dental and oral trauma during childhood and adolescence in Israel: occurrence, causes, and outcomes.
  - confidence: `high` — n=427 young adults ages 18–21 Israel; sport-specific dental injury counts + mouthguard data.
- **17670881** (2007) — The incidence and severity of dental trauma in intercollegiate athletes.
  - confidence: `high` — USC intercollegiate athletes 1996–2005, n=51 dental injuries with sport-level detail; college = within 18–22 age range.
- **17635356** (2007) — Dentoalveolar trauma in Glasgow: an audit of mechanism and injury.
  - confidence: `high` — Glasgow pediatric dental trauma audit; abstract reports 79% of sporting-related injuries were in males — sport-specific data extractable.
- **17073918** (2006) — Dental and orofacial trauma in pony and horseback riding children.
  - confidence: `high` — Pony/horseback riding children, n=214; sport-specific dental trauma prevalence reported.
- **16809595** (2006) — Neighborhood social capital and dental injuries in Brazilian adolescents.
  - confidence: `high` — Brazilian adolescents 14–15 n=1302 multilevel study; dental injury as outcome — likely sport-related subset extractable from full text.
- **16162986** (2005) — Comparison of mouth guard designs and concussion prevention in contact sports: a multicenter randomized controlled trial.
  - confidence: `high` — Multicenter cluster-RCT, varsity football and rugby teams, mouthguard vs mouthguard, concussion + dental trauma outcomes per playing season — high-quality primary data.
- **15876321** (2005) — Oro-facial injuries in Central American and Caribbean sports games: a 20-year experience.
  - confidence: `high` — 20-year experience of dental services at Central American & Caribbean Games; sport-related orofacial injuries reported across multiple sports.
- **15660753** (2005) — Dental trauma and mouthguard usage among ice hockey players in Turkey premier league.
  - confidence: `high` — Turkish Premier Ice Hockey League youth AND adult players — youth subset is extractable per the abstract's explicit framing.
- **15592602** (2004) — Dental Injuries in Intermediate and High School Athletes: A 15-Year Study at Punahou School.
  - confidence: `high` — Punahou School longitudinal 1988–2003 intermediate+HS athletes; dental injury rates/1000 athlete-sessions by sport — directly extractable AE-denominator data.
- **15022997** (2003) — Etiological factors related to dental injuries in Norwegians aged 7-18 years.
  - confidence: `high` — Norwegian children 7–18, n=1275 injured individuals; sport = 8% of dental injury etiology; primary data extractable.
- **14708646** (2003) — Dental and oral trauma and mouthguard use during sport activities in Israel.
  - confidence: `high` — n=943 young adults ages 18–19 Israel; sport-specific dental injury counts (soccer, basketball) + mouthguard awareness — perfect §3.1 fit.
- **11782645** (2002) — Effect of mouthguards on dental injuries and concussions in college basketball.
  - confidence: `high` — Prospective study of 50 NCAA Div I men's college basketball teams; reports dental injury rates/1000 AE with mouthguard effect — gold-standard fit (sport=basketball, age=collegiate, primary AE-denominator data).
- **11678540** (2001) — Prevalence, causes and correlates of traumatic dental injuries among 13-year-olds in Brazil.
  - confidence: `high` — n=652 13-year-old adolescents Brazil; sport-related = 2.3% of TDI etiology; meets §3.1 age + sport + numerical data.
- **11499758** (2001) — Dental trauma in children presenting for treatment at the Department of Dentistry for Children and Orthodontics, Budapest, 1985-1999.
  - confidence: `high` — Children 7–14 (88% of 590-child cohort); sports listed as etiology with frequency rank; primary data extractable for sport subset.
- **11202877** (2000) — The aetiology of dento-alveolar injuries and factors influencing attendance for emergency care of adolescents in the north west of England.
  - confidence: `high` — Schoolchildren n=2022, sport-related causes ~30% of TDI; primary epidemiology data, age range consistent with 5–18.

---

## needs_human_review  (63)

### R-age — Needs review — age range / population unclear from abstract  (35)

- **39630092** (2026) — Experience of Orofacial Injuries and Use of Mouthguards - A Survey in German Elite Sport.
  - confidence: `medium` — German elite athletes 18–35; 18–22 subset within scope but mixed-ages population.
- **40662680** (2025) — From Fitness to Fight: Associations between training motivation and injury prevalence in Muay Thai, K-1 and Kickboxing.
  - confidence: `medium` — Swiss Muay Thai/K-1/Kickboxing n=440 martial artists — age range not in abstract.
- **37055924** (2024) — Sports-related dental injuries and oral health status among Malaysian para-athletes: A cross-sectional study.
  - confidence: `medium` — Malaysian para-athletes n=61 — age range not in abstract.
- **36327493** (2024) — 'Benched' the effect of the COVID-19 lockdown on injury incidence in sub-elite football in Australia: a retrospective population study using injury insurance records.
  - confidence: `medium` — Australian sub-elite football (soccer) injury insurance 2018–2020 — age group breakdown reported but exact ranges not in abstract.
- **37791703** (2023) — Mouthguards reduce dental injuries and associated costs in Ladies Gaelic football.
  - confidence: `medium` — Ladies Gaelic football MG cost reduction; abstract truncated in our dump — Ladies GAA is adult, but youth subset may exist.
- **37431232** (2023) — Incidence, characteristics and cost of head, neck and dental injuries in non-professional football (soccer) using 3 years of sports injury insurance data.
  - confidence: `medium` — Australian non-professional football insurance 2018–2020; age categories reported but ranges unclear.
- **37341423** (2023) — Knowledge of traumatic dental injuries and mouthguard behavior among Croatian soccer players.
  - confidence: `medium` — Croatian soccer all leagues n=393 — age range not in abstract.
- **36922269** (2023) — Prevalence and pattern of traumatic orofacial injuries in Kabaddi players in Delhi-NCR region.
  - confidence: `medium` — Kabaddi players Delhi-NCR — age range not in abstract; likely mixed youth/adult.
- **36538371** (2023) — Maxillofacial injuries among ice hockey players: a retrospective study from a Finnish trauma Centre.
  - confidence: `medium` — Finnish trauma centre 2013–2020 ice hockey facial fractures; professional + recreational — youth subset extractable.
- **34343071** (2021) — Dental Trauma Among Hockey Players: Preventive Measures, Compliance and Injury Types.
  - confidence: `medium` — Ice hockey n=169 online survey — age range not in abstract.
- **34047017** (2021) — Prevalence of orofacial trauma and the attitude towards mouthguard use in handball players: A survey in Lorraine, France.
  - confidence: `medium` — Lorraine France handball n=>15 yr — primarily adult; 15–22 subset extractable.
- **33220143** (2021) — Mouthguard use and attitudes regarding dental trauma among elite cross-country mountain biking and field hockey athletes.
  - confidence: `medium` — Elite cross-country mountain biking + field hockey athletes pre-Olympic competitions Rio; elite likely adult, but some youth elite athletes may be present.
- **33188561** (2021) — Occurrence and patterns of orofacial injury in CrossFit practitioners.
  - confidence: `medium` — CrossFit practitioners online survey; population likely adult (self-selected practitioners).
- **31994310** (2020) — The prevalence of orofacial injuries in judo: A cross-sectional study.
  - confidence: `medium` — Bern Switzerland judo n=382; age range not in abstract.
- **30156365** (2018) — Risk of orofacial injuries and mouthguard use in water polo players.
  - confidence: `medium` — Water polo n=347 players 2015–16 season; age range not in abstract.
- **28160512** (2017) — Prevalence of dental trauma and use of mouthguards in professional handball players.
  - confidence: `medium` — Professional handball n=100; professional = adult likely.
- **27622524** (2016) — Dental and General Trauma in Team Handball.
  - confidence: `medium` — Team handball 'top athletes' n=542; age range not in abstract — likely senior.
- **26542314** (2016) — Dental trauma in showjumping - A trinational study between Switzerland, France and Germany.
  - confidence: `medium` — Showjumping Switzerland/France/Germany n=608 — age range not in abstract.
- **26678302** (2015) — Prevention of dental accidents in Swiss boxing clubs.
  - confidence: `medium` — Swiss boxing clubs n=217 boxers; age range not in abstract.
- **26058666** (2015) — Association of dental trauma experience and first-aid knowledge among rugby players in Malaysia.
  - confidence: `medium` — Rugby players Malaysia, aged 16+ — most likely adult, but 16–22 subset extractable.
- **25721283** (2015) — Reporting dental trauma and its inclusion in an injury surveillance system in Victoria, Australia.
  - confidence: `medium` — Royal Dental Hospital Melbourne 2009–2012 emergency surveillance audit — age range not in abstract.
- **25536987** (2014) — Orofacial injuries reported by professional and non-professional basketball players in zagreb and zagreb county.
  - confidence: `medium` — Zagreb amateur (n=60) + professional (n=135) basketball — adult-dominant likely; youth subset extractable only if amateurs include U18.
- **22882839** (2013) — Prevalence of oral trauma in Para-Pan American Games athletes.
  - confidence: `medium` — Para-Pan American Games athletes Rio — adults likely dominate; youth (16–22) subset may be present.
- **22107072** (2012) — Dental injuries in water polo, a survey of players in Switzerland.
  - confidence: `medium` — Water polo Switzerland n=415 players from 6 divisions — likely mostly adult but youth subset may exist.
- **21199336** (2011) — Eye injuries and orofacial traumas in floorball--a survey in Switzerland and Sweden.
  - confidence: `medium` — Floorball Switzerland + Sweden n=608 (565 athletes + 43 coaches); age range not stated.
- **20669600** (2010) — Maxillofacial and dental injuries sustained in hurling.
  - confidence: `medium` — Hurling injuries Mid-Western Regional Hospital Limerick n=70; age range not stated.
- **20572841** (2010) — Prevalence of dental trauma in Pan American games athletes.
  - confidence: `medium` — Pan American Games athletes 2007 — adult/elite athletes, likely mostly outside 5–22.
- **19021660** (2008) — Dental trauma in an Australian rural centre.
  - confidence: `medium` — Australian rural dental trauma — age range not stated in abstract excerpt.
- **18821955** (2008) — Dental injuries in mountain biking--a survey in Switzerland, Austria, Germany and Italy.
  - confidence: `medium` — Mountain biking Switzerland/Austria/Germany/Italy n=423 males; age range not in abstract.
- **18721342** (2008) — Basketball players' experience of dental injury and awareness about mouthguard in China.
  - confidence: `medium` — China basketball players n=236, 77 professional; age range not stated.
- **24198704** (2007) — Injury profile in women shotokan karate championships in iran (2004-2005).
  - confidence: `medium` — Iranian women Shotokan karate national championships 'in all age groups'; youth subset may be extractable from full text.
- **17846669** (2007) — Risk factors for traumatic dental injuries in an adolescent male population in India.
  - confidence: `medium` — n=370 male enrollees National Cadet Corps India; age range not stated — NCC enrollees often 13–22, but needs verification.
- **17511835** (2007) — Dental injuries in inline skating - level of information and prevention.
  - confidence: `medium` — Inline skating Switzerland + Germany; age range not in abstract — could be predominantly adult.
- **12154770** (2002) — Dental trauma and level of information: mouthguard use in different contact sports.
  - confidence: `medium` — Professional and semi-professional contact-sport athletes — age range not stated; full text needed to confirm any youth (5–22) data.
- **11880801** (2002) — Dental injuries in ice hockey games and training.
  - confidence: `medium` — Finland ice hockey 1991–1992 insurance dataset (n=479 injured); abstract does not state age distribution — likely includes youth + adult, full text needed.

### R-data — Needs review — extractable numerical injury data unclear from abstract  (21)

- **26939219** (2015) — Prevalence and unmet treatment need of traumatized incisor among Cameroonian schoolchildren in North West Province.
  - confidence: `medium` — Cameroon 12–13 schoolchildren incisor trauma n=2287; sport-related subset not isolated.
- **26545273** (2015) — Mandatory mouthguard rules for high school athletes in the United States.
  - confidence: `medium` — HS athletes US mouthguard mandate review — may be policy overview without primary injury data; full text needed.
- **25244279** (2014) — A retrospective evaluation of traumatic dental injury in children who applied to the dental hospital, Turkey.
  - confidence: `medium` — Samsun Turkey 2007–11 emergency dental trauma in children n=320; sport-related subset not isolated.
- **24505897** (2013) — Clinical--imaging aspects of young permanent teeth traumas and the ethiopatogenic mechanisms involved.
  - confidence: `medium` — n=372 Romanian 8–20 yr; sport-related subset not isolated.
- **23534038** (2013) — Traumatic dental injuries among 12-year-old schoolchildren in Jordan: prevalence, risk factors and treatment need.
  - confidence: `medium` — n=2560 12-yr Jordanian schoolchildren TDI; sport-related subset not isolated in abstract.
- **21880516** (2011) — The association between orthodontic treatment need and maxillary incisor trauma, a retrospective clinical study.
  - confidence: `medium` — n=502 schoolchildren 11–14 orthodontic risk factor study; sport involvement not in abstract.
- **21790975** (2011) — Non-accidental collision followed by dental trauma: associated factors.
  - confidence: `medium` — n=387 Brazilian adolescents 12–15; focus on 'non-accidental collision' — sport-related subset unclear.
- **21755701** (2011) — Orofacial injuries reported by junior and senior basketball players.
  - confidence: `medium` — Junior AND senior basketball players orofacial injuries; junior subset likely extractable but abstract does not give counts by group.
- **20666978** (2010) — Prevalence and associated factors of traumatic dental injuries in Brazilian schoolchildren.
  - confidence: `medium` — n=1612 11–14 yr Brazilian schoolchildren TDI; sport-related subset not isolated.
- **20089070** (2010) — Prevalence of traumatic injuries to maxillary permanent teeth in 9- to 14-year-old school children in Yazd, Iran.
  - confidence: `medium` — Yazd Iran 9–14 yr schoolchildren TDI; sport-related subset not isolated in abstract.
- **19021650** (2008) — Retrospective clinical study of 90 avulsed permanent teeth in 58 children.
  - confidence: `medium` — Czech 90 avulsed permanent teeth in 58 children — youth fits, but sport-related subset not isolated in abstract.
- **18173668** (2008) — Dental trauma that require fixation in a children's hospital.
  - confidence: `medium` — Children's Hospital Buffalo pediatric dental trauma requiring fixation; sport-related subset not isolated in abstract.
- **17227375** (2007) — Effectiveness of mouthguards in reducing neurocognitive deficits following sports-related cerebral concussion.
  - confidence: `medium` — Mouthguard effect on neurocognitive deficits after concussion; primary outcome is concussion neurocog, dental injury data may be secondary in full text.
- **17194069** (2006) — Prevalence and factors associated with traumatic dental injuries (TDI) to anterior teeth of 11-13 year old Thai children.
  - confidence: `medium` — n=2725 Thai children 11–13; sport-related subset not isolated in abstract.
- **16872385** (2006) — Aetiology and rates of treatment of traumatic dental injuries among 12-year-old school children in a town in southern Brazil.
  - confidence: `medium` — 12-yr Brazilian schoolchildren TDI; abstract focuses on overjet risk factor — full text needed for sport-related subset counts.
- **15853840** (2005) — Dental trauma and its association with anatomic, behavioral, and social variables among fifth and sixth grade schoolchildren in Jerusalem.
  - confidence: `medium` — 5th–6th grade Jerusalem schoolchildren n=1195; sport mentioned among reasons but not isolated as primary data.
- **15362317** (2004) — Do community football players wear allocated protective equipment? Descriptive results from a randomised controlled trial.
  - confidence: `medium` — Australian Football Injury Prevention Project RCT; abstract reports MG compliance, not injury counts — full text may contain dental injury outcome data.
- **15643760** (2003) — Etiology of traumatic dental injuries in 11 to 13-year-old schoolchildren.
  - confidence: `medium` — 11–13 yr Brazilian schoolchildren; 'physical leisure activities' 28.9% but specific sport-related counts not isolated.
- **12656848** (2003) — Traumatic dental injuries in children presenting for treatment at the Department of Pediatric Dentistry, Faculty of Dentistry, University of Jordan, 1997-2000.
  - confidence: `medium` — University of Jordan pediatric dentistry 1997–2000, ages 10–12 peak; sport-related etiology not isolated in abstract.
- **12017183** (2002) — Causes of dental fractures in the early permanent dentition: a retrospective study.
  - confidence: `medium` — Dicle University 1995–98 pediatric dental fractures; ages 9–11 peak. Sport-related subset not isolated in abstract — confirm in full text.
- **11678537** (2001) — A retrospective study of dento-alveolar injuries of children in Ankara, Turkey.
  - confidence: `medium` — n=150 Ankara children TDI study; abstract does not isolate sport-related subset — confirm in full text whether sport-related counts are extractable.

### R-mixed — Needs review — mixed adult+youth, youth subset extractability needs full text  (7)

- **30431180** (2019) — Prevalence of dental trauma in individuals with special needs participating in local Special Olympics games.
  - confidence: `medium` — Israeli Special Olympics 2016 — Special Olympics athletes mixed ages (8+ allowed); youth subset extractable.
- **25600092** (2015) — A multicenter study on dental trauma in permanent incisors among Special Olympics athletes in Europe and Eurasia.
  - confidence: `medium` — n=15941 Special Olympics athletes Europe/Eurasia — mixed ages (Special Olympics allows adults too); youth subset extractable.
- **20946344** (2010) — A retrospective study of 889 injured permanent teeth.
  - confidence: `medium` — n=384 patients ages 7–65, 66% children — youth subset extractable but full text needed.
- **19615582** (2009) — Dental injuries in association with facial fractures.
  - confidence: `medium` — n=273 facial fracture patients Switzerland — age range not stated, could include adults.
- **18352919** (2008) — Dental and maxillofacial skeletal injuries seen at the University of Otago School of Dentistry, New Zealand 2000-2004.
  - confidence: `medium` — Otago NZ 2000–2004 dental school, ages 2–86 peak 16–25; youth (5–22) subset overlaps but full text needed to extract.
- **12139268** (2002) — A survey of dental and oral trauma in south-east Queensland during 1998.
  - confidence: `medium` — SE Queensland 1998 dental trauma survey, ages 1–64; 16–20 group reported as sport-related — youth subset extractable but needs full text.
- **11766091** (2001) — A retrospective study of traumatic dental injuries in a Brazilian dental trauma clinic.
  - confidence: `medium` — n=250 patients ages 1–59 Brazil; sport = 3.6% of causes — full text needed to extract youth (5–22) subset.

---

## screened_excluded  (64)

### E-age — Excluded — population outside 5–22 age range (§3.1)  (7)

- **40267058** (2025) — Motivators and barriers to mouthguard compliance by adult Gaelic football athletes.
  - confidence: `high` — Adult Gaelic football athletes mouthguard compliance; population explicitly adult.
- **33377302** (2021) — Dental trauma and tongue injuries in professional alpine ski racing-A worldwide survey.
  - confidence: `high` — Professional alpine ski racers worldwide; professional adults, outside 5–22.
- **21496201** (2011) — Orofacial trauma in Brazilian basketball players and level of information concerning trauma and mouthguards.
  - confidence: `high` — Brazilian Basketball Confederation Category A-1 adult athletes / national team — outside 5–22.
- **21382033** (2011) — A survey of orofacial injuries among basketball players.
  - confidence: `high` — PMC full-text confirms mean age 23 (no further age stratification visible) — population is predominantly adult, outside 5–22 scope. [Resolved via PMC9374803 full-text fetch, 2026-05-22.]
- **20711109** (2011) — Study of the effect of oral health on physical condition of professional soccer players of the Football Club Barcelona.
  - confidence: `high` — FC Barcelona professional soccer players — adult professionals, outside 5–22 (§3.1).
- **19055884** (2008) — Mouthguards in the American Hockey League [AHL].
  - confidence: `high` — American Hockey League (AHL) — professional adult ice hockey players; outside 5–22 age range (§3.1).
- **16711635** (2006) — Prevalence and causes of oral injuries in a population of Canadian adults aged 18 to 50 years--a brief communication.
  - confidence: `high` — Ontario adults aged 18–50; majority outside 5–22 range; sport-related subset for 18–22 may be too small/unclear from abstract.

### E-case — Excluded — single case report (§3.2)  (1)

- **33369093** (2021) — Oral management with mouthguards during the mixed dentition period: A case report.
  - confidence: `high` — PubMed PublicationType 'Case Reports' — excluded per §3.2.

### E-lang — Excluded — non-English (§3.1 v1.0 scope)  (8)

- **41058495** (2025) — [Online survey Sports and oral health: the results].
  - confidence: `high` — Language='dut' — English-only per PROTOCOL §3.1 v1.0 scope.
- **36878220** (2023) — [Injuries in the First German Inline Skater Hockey League].
  - confidence: `high` — Language='ger' — English-only per PROTOCOL §3.1 v1.0 scope.
- **32854130** (2020) — [Injuries in inline skater hockey].
  - confidence: `high` — Language='ger' — English-only per PROTOCOL §3.1 v1.0 scope.
- **24502091** (2013) — [Traumatic dental injuries in Serbian children--epidemiological study].
  - confidence: `high` — Language='srp' — English-only per PROTOCOL §3.1 v1.0 scope.
- **19402309** (2009) — [Changing approaches to traumatic injuries to primary and permanent teeth based on the reports published in 'Fogorvosi Szemle' in the past 100 years].
  - confidence: `high` — Language='hun' — English-only per PROTOCOL §3.1 v1.0 scope.
- **18623976** (2008) — [Prevalence of oro-dental injuries in wrestling in Senegal].
  - confidence: `high` — Language='fre' — English-only per PROTOCOL §3.1 v1.0 scope.
- **17933358** (2007) — [Dento-alveolar trauma in odonto-stomatologic consultation in a health center in Yaoundé, Cameroon].
  - confidence: `high` — Language='fre' — English-only per PROTOCOL §3.1 v1.0 scope.
- **12602199** (2003) — [Frequency and nature of anterior tooth injuries and the use of mouth protectors in sports clubs in Bern].
  - confidence: `high` — Language='ger' — English-only per PROTOCOL §3.1 v1.0 scope.

### E-noprim — Excluded — no extractable primary numerical injury data (§3.1)  (8)

- **40919643** (2025) — Dental Trauma Prevention and Injury Measures Among Supervisors of German Elite Handball Teams: A Questionnaire-Based Cross-Sectional Study.
  - confidence: `high` — Survey of German elite team SUPERVISORS — preventive knowledge of medical teams, not athlete-level injury counts.
- **36479391** (2023) — Awareness of sports-related dental emergencies and prevention practices among Libyan contact sports coaches: A cross-sectional study.
  - confidence: `high` — Awareness study of Libyan contact-sport coaches; no athlete-level injury counts.
- **35802850** (2022) — Knowledge about the emergency management of dental injuries among field hockey coaches.
  - confidence: `high` — Knowledge survey of field hockey coaches — coaches, not athletes; no athlete-level injury counts.
- **34257165** (2021) — Revisiting Sports Dentistry with a Critical Appraisal.
  - confidence: `high` — Editorial 'Revisiting Sports Dentistry' — no primary epidemiology data; review-type content.
- **32134033** (2020) — Orofacial trauma awareness among sports teachers in Southern Saudi Arabia.
  - confidence: `high` — Awareness/knowledge survey of sports teachers; no athlete-level injury counts.
- **27875057** (2016) — National Athletic Trainers' Association Position Statement: Preventing and Managing Sport-Related Dental and Oral Injuries.
  - confidence: `high` — NATA Position Statement — clinical recommendations / consensus document, not primary epidemiologic data.
- **26545276** (2015) — Splinting rationale and contemporary treatment options for luxated and avulsed permanent teeth.
  - confidence: `high` — Clinical review article on splinting rationale for luxated/avulsed teeth — review content, no primary epidemiology.
- **15562160** (2004) — Perception of Nigerian athletes of the use of mouth guards to prevent the stresses of sports injury.
  - confidence: `high` — Perception/attitude survey of Nigerian athletes; outcome is psychological/sociological stress, no primary dental injury count per athlete-exposure (§3.1 'numerical data extractable' fails).

### E-offtop — Excluded — not sport-related or wrong subject (§3.1 / §3.3)  (5)

- **38729211** (2024) — Noncombat injury and illness prevalence and working score percentage quantify the impact on duty availability in US Army Special Operations military working dogs.
  - confidence: `high` — US Army Special Operations military working DOGS — animal subjects, off-topic.
- **29190193** (2017) — Characterization and comparison of injuries caused by spontaneous versus organized dogfighting.
  - confidence: `high` — Dogfighting injuries — animal subjects, off-topic (§3.1).
- **23998194** (2014) — Birth order--a risk factor for dental trauma?
  - confidence: `high` — Birth order as risk factor for dental trauma in 1282 Swiss children; non-sport-specific risk factor study, sport-related subset not the focus.
- **19149336** (2008) — Orofacial injuries and mouth guard use in elite commando fighters.
  - confidence: `high` — Israel Defense Forces elite commando fighters — military setting, not sport-related (§3.1); participants adult.
- **15773884** (2005) — Traumatic injuries to the teeth in young individuals with cerebral palsy.
  - confidence: `high` — Cerebral palsy children dental trauma study; explicitly notes 'CP individuals do not take part in violent sport activities' — non-sport-related dental trauma (§3.2).

### E-review — Excluded — review / SR / MA: kept for source mining only (§3.2)  (35)

- **41871283** (2026) — Occurrence of Orofacial and Dental Injuries in Rugby: Systematic Review and Meta-Analysis.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **41760758** (2026) — Emergency management of sport-related orofacial trauma.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **41742174** (2026) — Oral health, orofacial pain and dysfunction, and orofacial trauma in athletes: a scoping review.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **41441433** (2025) — Research Progress on Common Sports Injuries Among Youth Ice Hockey Players and Prevention Strategies: A Narrative Review.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **39578680** (2025) — Position Statement and Recommendations for Custom-Made Sport Mouthguards.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **38641923** (2024) — Comparative analysis of dental trauma in contact and non-contact sports: A systematic review.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **37889242** (2023) — Global research trends of studies related to mouthguards and dental injuries in sports activities: a bibliometric analysis.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **37524627** (2023) — Influence of wearing mouthguards on performance among athletes: A systematic review.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **37208059** (2023) — Emergency Facial Injuries in Athletics.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **35439876** (2022) — Sports-related facial trauma in the Indian population - A systematic review.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **34907662** (2022) — Dental and general injuries among ski and snowboard instructors in Switzerland, Germany, and Austria-A questionnaire-based study.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **34063591** (2021) — The Impact of Sport Training on Oral Health in Athletes.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **33793079** (2021) — Prevalence of orofacial injuries in wheeled non-motor sports athletes: A systematic review and meta-analysis.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **31420968** (2020) — Prevalence of dentofacial injuries among combat sports practitioners: A systematic review and meta-analysis.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **31801589** (2019) — Italian guidelines for the prevention and management of dental trauma in children.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **31148073** (2019) — Effectiveness of Mouthguards for the Prevention of Orofacial Injuries and Concussions in Sports: Systematic Review and Meta-Analysis.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **30222244** (2019) — The use of mouthguards and prevalence of dento-alveolar trauma among athletes: A systematic review and meta-analysis.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **29737221** (2018) — Injuries in karate: systematic review.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **29303400** (2018) — The 'Sequence of Prevention' for musculoskeletal injuries among recreational basketballers: a systematic review of the scientific literature.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **28314416** (2017) — Prevention of Sport-related Facial Injuries.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **28314415** (2017) — Epidemiology of Facial Injuries in Sport.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **26923445** (2016) — Epidemiology and outcomes of traumatic dental injuries: a review of the literature.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **25574879** (2015) — Dental problems in athletes.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **25388551** (2015) — Oral health of elite athletes and association with performance: a systematic review.
  - confidence: `high` — Systematic review or meta-analysis — kept for reference mining; not extracted per §3.2.
- **23635988** (2013) — Evidence-based review of prevention of dental injuries.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **23529288** (2013) — Injury incidence, risk factors and prevention in Australian rules football.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **23439051** (2013) — Evidence-based review of prevention of dental injuries.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **23439040** (2013) — Epidemiology of traumatic dental injuries.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **19208007** (2009) — Aetiology and risk factors related to traumatic dental injuries--a review of the literature.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **16247261** (2005) — Basketball injuries.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **16060339** (2005) — Are mouthguards necessary for basketball?
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **15659273** (2005) — Dental injuries in sports.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **15206262** (2004) — A literature review of sports-related orofacial trauma.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **15085503** (2004) — Craniomaxillofacial trauma in children: a review of 3,385 cases with 6,060 injuries in 10 years.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.
- **12116516** (2002) — Dentofacial trauma in sport accidents.
  - confidence: `high` — Narrative review — kept for reference mining; not extracted per §3.2.

---

## How decisions were made

- **Auto-rules** (`02_screen_candidates.py`): non-English (`language != 'eng'`), `PublicationType = 'Case Reports'`, and `PublicationType ∈ {Review, Systematic Review, Meta-Analysis}` → automatic `screened_excluded` with reason `E-lang`, `E-case`, or `E-review`. Reviews are kept in the source list because PROTOCOL §3.2 explicitly allows them to be mined for primary-source citations — they are just not extracted themselves.
- **Manual decisions** (`screening_overrides.py`): every other record was assigned a decision after reading the title, abstract, and publication-type list from the per-PMID JSON in `data/raw/papers/_abstracts/`. Where the abstract did not disclose age range, sport-related subset, or extractable numerical data, the decision defaulted to `needs_human_review` rather than risking a wrong exclusion.
- **No full texts were retrieved.** All decisions are reversible by the project lead reading the full text.
- **Confidence ratings**: `high` = the abstract is decisive; `medium` = abstract supports the call but a reasonable reader could disagree; `low` = used only for genuine ambiguity in `needs_human_review`.

## Files referenced

- `data/raw/papers/_abstracts/<PMID>.json` — full parsed record per candidate
- `data/raw/papers/_abstracts/_index.csv` — one-line-per-record index
- `data/extracted/_screening/screening_decisions.csv` — canonical decisions CSV
- `scripts/02_screen_candidates.py` — applies auto rules + manual overrides
- `scripts/screening_overrides.py` — the manual decision dictionary
- `scripts/03_apply_screening_to_sources.py` — regenerates `docs/sources.md` from decisions
- `scripts/04_write_screening_report.py` — generates this report