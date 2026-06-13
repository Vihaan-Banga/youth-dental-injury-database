# Advisor Outreach Brief — Youth Sports Dental Injury Database

**This file is designed to be pasted, in full, into a fresh Claude conversation. It is a self-contained briefing so that Claude can help me draft outreach emails to potential research advisors without me having to re-explain context every time.**

> **Instructions for the new Claude conversation:** I am preparing to email faculty researchers to ask if they will serve as the senior advisor on a research-database project I've been building. Below is everything you need to know about me, the project, and what I want from the advisor. Help me draft tailored, professional outreach emails to specific faculty members — keep them short (200–300 words), specific to the recipient's published work, and honest about what the project needs from them. I will tell you which specific faculty member to draft an email to in my next message after this one.

---

## 1. About me (the project lead)

- **Name:** Vihaan Banga
- **Status:** High school student, Olentangy Liberty High School, Powell, OH
- **Project goal:** First major research project. Targeting submission to the **Conrad Challenge** in the Sept–Nov 2026 window, plus an open-access data descriptor paper in *Scientific Data* (Nature) or *Data in Brief* (Elsevier).
- **GitHub:** @Vihaan-Banga
- **Geography note:** Powell, OH is ~20 miles from OSU campus — geographically convenient for OSU College of Dentistry, OSU Sports Medicine, or Nationwide Children's Hospital faculty.

I am new to academic research processes. I have built the project to date by leading every step myself with AI assistance (Claude Code), using the formal research-methods structure (pre-registered protocol, decision log, controlled vocabulary, validation pipeline, version control). The work is rigorous; I just need a senior researcher to credibly co-author and sign off.

## 2. What the project is

**An open-access harmonized database of dental and orofacial injury epidemiology in youth sports** (ages 5–22).

The problem it solves: youth dental injury data is fragmented across dozens of national surveillance systems (NEISS, RIO/NFHS, NCAA, NZ ACC, etc.), peer-reviewed studies, and sport-governing-body reports. Each uses different definitions, age categories, exposure denominators (per athlete-exposure, per population, per player-game-hour), and outcome classifications. No unified resource lets a researcher answer questions like "what's the per-1000-athlete-exposure dental injury rate across youth contact sports?" or "how have rates changed since youth mouthguard mandates?" without manually reconciling 40+ papers.

This database does that reconciliation, once, openly, with a transparent methodology.

**Live website:** https://vihaan-banga.github.io/youth-dental-injury-database/
**Repository:** https://github.com/Vihaan-Banga/youth-dental-injury-database
**Current release:** v0.1.0 (pre-launch, pre-registration-pending)

## 3. Concrete state of the project (as of late May 2026)

### Data
- **426 rows** in `data/harmonized/master.csv`, drawn from **106 distinct sources** across **29 countries**
- **12 treatment years of NEISS** case-level data (2013–2019, 2021–2025; 2020 returned no matching cases — real COVID-era youth-sport gap). To my knowledge, this is the first published aggregation of NEISS dental-sport data at this temporal breadth for the youth-specific subset.
- ~8,800 underlying NEISS case-level records filtered to youth + body-part-mouth + 23 sport product codes.
- All extracted rows pass 10 automated validation checks (schema, categorical vocabulary, numeric plausibility, age-category consistency, source coverage). **0 FAILs, 0 WARNs** at current state.
- SQLite export for queryable use (`data/harmonized/master.sqlite`).

### Methodology
- **Pre-registered research protocol** (`PROTOCOL.md`) covering inclusion/exclusion criteria, search strategy, harmonization rules, validation, and authorship. Currently `Draft v0.1 — pre-registration pending`.
- **Data dictionary** (`DATA_DICTIONARY.md`) — 34 columns, each with type, allowed values, and definition.
- **Append-only decisions log** (`docs/decisions.md`) capturing every non-mechanical harmonization decision with date, options considered, reasoning, and affected rows.
- **Source tracking** (`docs/sources.md`) showing every candidate source's screening journey: identified → screened_included / screened_excluded / needs_human_review.
- **AI-assisted screening**: 444 PubMed candidates screened against PROTOCOL §3.1–3.3 using rule-based auto-exclusion + Claude-assisted abstract review, with full per-decision reasoning logged.

### Pipeline (reproducibility)
- 29+ versioned Python scripts: source identification → screening → per-source extraction → harmonization → validation → analysis.
- **GitHub Actions CI**: runs the validator on every push and PR; passing.
- All scripts portable (no hardcoded paths); pipeline reproducible from scratch on any machine.

### Documentation + outputs
- `outputs/methods_paper_draft.md` — skeleton following *Scientific Data* structure (Abstract, Background, Methods, Data Records, Technical Validation, Usage Notes).
- `outputs/factsheet.md` — one-page project summary.
- `outputs/neiss_trends.md` — 12-year trend analysis (novel).
- `outputs/cross_source_rate_comparison.md` — internal-consistency check across sources.
- `outputs/sport_factsheets/` — one-pager per sport (19 sports covered).
- `outputs/country_breakdown.md` — geographic coverage analysis.
- `outputs/sources_bibliography.bib` — BibTeX file with 93 article + 5 surveillance source entries.
- `CONTRIBUTING.md` + `CHANGELOG.md` — repo polish for credibility.

### Licensing + citation infrastructure
- **Code under MIT License** (LICENSE)
- **Data under CC BY 4.0** (LICENSE-DATA)
- **CITATION.cff** at repo root — GitHub renders "Cite this repository" button
- Zenodo integration walkthrough ready — minting a permanent DOI is a 5-min user toggle away (the project will get `10.5281/zenodo.XXXXXXX` for permanent academic citability at v1.0)

### Key analytical findings already in the database
- **NEISS US youth dental-sport ED visits**: weighted national estimate ranged from 26,424 (2013) → 17,000 (2019) → ~15,000 (2021, COVID trough) → 21,000 (2024–25 recovery).
- **Cross-source US HS basketball internal consistency**: `collins2016` reports 0.026 per 100k AE; `azadani2023` reports 0.024 per 100k AE — statistically indistinguishable estimates from two independent papers covering overlapping years.
- **Mouthguard effect (`labella2002` college basketball RCT)**: 0.12 (MG users) vs 0.67 (non-users) per 1000 AE — 5.6× reduction.
- **Junior A hockey facial-protection dose-response (`benson2002`)**: 158.9 → 73.5 → 23.2 per 1000 player-game-hours across no / partial / full facial protection.

## 4. What's NOT yet done (the gap an advisor would help close)

1. **No senior advisor co-author yet** — this is what I'm trying to fix.
2. **OSF pre-registration not filed** — depends on advisor sign-off.
3. **20% inter-rater reliability re-screening not done** — depends on advisor (or designee).
4. **91 records still in `needs_human_review` status** — most are publisher-paywalled abstracts where I can't see the methods section. An advisor with university library access could resolve these quickly.
5. **Methods paper not yet drafted in full** — skeleton exists; needs co-author input.
6. **Not yet submitted to Conrad Challenge or any journal**.

## 5. What I'm asking the advisor for

I am asking for **co-authorship of the v1.0 release and the methods paper**, in exchange for:

- **Reviewing the protocol** and signing off on the pre-registration (~2 hours)
- **Conducting (or supervising) the 20% inter-rater reliability re-screening** (~4–6 hours)
- **Reviewing the methods paper draft** (~2–3 hours)
- **Lending institutional / academic credibility** to the project (no specific time cost — just letting their name be on it)
- **Optional but appreciated**: helping resolve the 91 `needs_human_review` records via library full-text access, and/or letting me use a library subscription for future extractions.

**Estimated total time commitment: 10–15 hours over the next 3–6 months**, spread out, not concentrated. Most can be done asynchronously.

**Authorship offer**: I will be first author (project lead, conceived project, did all source identification + screening + extraction + harmonization + pipeline + paper draft). The advisor would be senior (last) author. Any additional contributors (e.g., a graduate student helping with reliability re-screening) can be middle authors.

## 6. What's in it for the advisor

- **A publication in *Scientific Data* (Nature group) or *Data in Brief* (Elsevier)** without having to do the extraction work. These are real, citable, peer-reviewed venues — *Scientific Data* has an impact factor ~7.
- **An open dataset with their name on it** that the dental/sports-medicine research community can cite for years. Data descriptors accumulate citations slowly but steadily.
- **A mentorship narrative** for their CV / NIH biosketch ("Mentored a high school student in conducting a systematic review and publishing a peer-reviewed data descriptor"). Particularly useful for NIDCR-funded faculty whose grants require mentoring components.
- **A starting point for their own empirical papers** — the database supports trend analysis, mouthguard-mandate evaluation, cross-country comparison, economic burden estimation. Several spinoff papers are plausible from the same dataset.
- **Zero risk of methodological embarrassment** — the work is already done to standards that exceed most master's theses; they would be co-authoring something already substantially rigorous, not bailing out a flailing project.

## 7. Who would be ideal advisors (profile)

I am looking for a senior researcher (any tenure stage including assistant prof) with at least one of:

- **Published peer-reviewed work in pediatric dental traumatology** (especially anyone who has used Andreasen classification, has authored TDI prevalence studies, or has cited surveillance data)
- **Published work using NEISS, RIO/NFHS, or NCAA-ISP** for sports injury epidemiology — extra credit if youth-focused
- **Sports dentistry / sports medicine** clinical and research background
- **Pediatric injury surveillance** research (e.g., CIRP at Nationwide Children's, similar centers)
- **Open-data / FAIR-data methodology experience** (would value the technical infrastructure I've built)

**Especially good fits would be authors of papers already in my database** — they're warm leads because the database literally cites their work and they presumably care about the topic. Highest-priority warm leads:

- **CL Collins, RD Comstock, LB McKenzie** (RIO investigators at PIPER / Colorado SPH, formerly Nationwide Children's; authors of `collins2016`, `azadani2023`, multiple other database sources)
- **JE Townsend, EN Azadani** (Dental Traumatology, RIO-based)
- **CR Labella** (NCAA Div I basketball MG cohort — `labella2002`; based at Lurie Children's Chicago)
- **K Quarrie** (NZ ACC rugby longitudinal study — `quarrie2020`; based at NZ Rugby / U of Otago)
- **AC O'Connell** (Irish pediatric MG studies — `shore2023`; Dublin Dental U Hospital)
- **DN Ranalli, JA Townsend** (sports dentistry leaders)
- **Faculty at OSU College of Dentistry** (proximity advantage; OSU was named as the original target institution in PROTOCOL.md)
- **Faculty at Nationwide Children's CIRP (Center for Injury Research and Policy)** — geographically next door, methodologically aligned

## 8. Logistics

- I'm available for video / phone calls evenings and weekends US Eastern Time.
- I can travel to a Columbus-area meeting in person if useful.
- I can share read-access to the GitHub repo today; the website is already public.
- I would prefer to commit a specific time window (e.g., "1 hour call in the next 2 weeks") rather than open-ended scoping discussions.

## 9. How I want the outreach emails written (style guidance for Claude)

When drafting outreach emails using this brief:

- **Short — 200–300 words maximum.** Faculty get hundreds of cold emails per year. Length signals that I respect their time.
- **Specific to the recipient.** Cite at least one of their published papers — ideally one I have already extracted into the database — and explain how it influenced my work or sits in context with other sources.
- **Lead with the ask, not the backstory.** First paragraph should make clear what I want (their consideration as senior advisor on a publishable data descriptor) so they can decide in 30 seconds whether to read further.
- **Concrete artifacts, not hand-waving.** Mention specific deliverables ("0-FAIL validated database of 426 rows across 106 sources", "Scientific Data data descriptor skeleton ready", "interactive Rate Explorer on the public site"). Include the website link.
- **Honest about my level.** Explicitly say I'm a high school student, that I built this with AI assistance, that I lead the work and need them for credibility + advisor-level review rather than to do the underlying labor. Hiding this would backfire when they look at my email signature.
- **No emojis. No exclamation points except where genuinely warranted (which is approximately never).**
- **End with a specific small ask** — usually "Would you be open to a 30-minute video call in the next two weeks to discuss whether this might fit your interests?" — not an open-ended "let me know if interested."
- **Subject line** suggestion: "High school research project on youth dental injury database — request for advisor consideration" or similar specific framing.

## 10. Honest weaknesses / what an advisor might raise

These are concerns a thoughtful advisor will have. I want to be ready to address them:

- **"You used AI to screen — how do I know the decisions are sound?"** Every screening decision has full per-decision reasoning logged in `outputs/screening_report_*.md`. The 20% inter-rater reliability re-screening (which I'd ask them to do) is the standard answer to this.
- **"Why should I trust a high school student's extractions?"** Validation pipeline + cross-source consistency check (which shows independent papers report tightly matching rates for the same sport) are the empirical answer. The decisions log + reproducible pipeline are the procedural answer.
- **"What's in it for me beyond co-authorship?"** Spinoff papers (Section 6 above). Plus a methods paper that's already half-drafted and rigorously executed.
- **"What if I sign on and you go to college and abandon the project?"** Fair concern. v1.0 release is achievable within 3–6 months — the data assembly is done. If I leave, the dataset stands on its own with the methods paper as the artifact of record. The advisor's name on v1.0 is a complete deliverable.
- **"This is too much scope for a high school student."** I've already done it. The question is whether to co-sign the work or not, not whether the work is realistic.

---

## Closing prompt for the next Claude conversation

After reading this brief in full, please confirm you have a complete picture of:
1. Who I am and what I've built
2. What I'm asking of the advisor
3. Why a particular faculty member might say yes
4. How to write the outreach email

Then ask me which specific faculty member (name, institution, and ideally a link to their research profile or one of their papers) I'd like to draft an email for first. We'll iterate on that first email together — once we have a strong template, you can adapt it for additional faculty.

— Vihaan Banga
