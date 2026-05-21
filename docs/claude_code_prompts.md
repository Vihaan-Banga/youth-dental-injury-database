# Starter Prompts for Claude Code Sessions

Copy-paste these to get Claude Code oriented quickly at the start of each session. The right prompt depends on what phase you're in.

---

## First session ever (project initialization)

```
I'm working on a research project to build an open-access harmonized database of
youth sports dental injury epidemiology. The project structure, protocol, and data
dictionary are in this repository.

Please read these files in order, then summarize the project back to me so I know
you're oriented:
1. README.md
2. PROTOCOL.md
3. DATA_DICTIONARY.md
4. docs/sources.md
5. docs/decisions.md

After you've read them, tell me what you'd recommend as my next action.
```

---

## Starting a NEISS data download session

```
I'm in the data acquisition phase. Read PROTOCOL.md sections 4.1 and the NEISS
section. Then help me write `scripts/01_neiss_download.py` that:

1. Downloads NEISS annual CSV files from 2000–most recent for sports-related
   dental injuries
2. Filters by body part codes and sport-related product codes
3. Writes filtered data to data/extracted/neiss_dental_sports.csv

First, walk me through the NEISS coding system. I want to verify the body part
codes and product codes before we write the script. Don't write code until I
confirm the codes.
```

---

## Starting a paper extraction session

```
I'm extracting data from a peer-reviewed paper. The PDF is at
data/raw/papers/<filename>.pdf.

Read PROTOCOL.md section 5 and DATA_DICTIONARY.md, then:
1. Open the PDF and find any tables with dental injury data
2. Walk me through each table — what rows would map to which columns
3. Flag any ambiguous classifications (especially injury type or sport category)
4. After I make decisions, generate the extraction file at
   data/extracted/<source_id>.csv per the data dictionary format
5. Add an entry to docs/sources.md updating status to "extracted"

Do not invent data. If a field isn't clearly stated in the source, leave it
empty and add a note in extraction_notes.
```

---

## Starting a harmonization session

```
I'm harmonizing all extracted data into the master dataset. Read PROTOCOL.md
section 6 and docs/decisions.md.

Walk me through:
1. List all files in data/extracted/
2. For each file, identify any values in sport_raw or injury_type_raw that
   don't have a mapping yet in docs/decisions.md
3. Stop and ask me about each unmapped value before assuming a mapping
4. Once all mappings are settled, generate scripts/03_harmonize.py that
   combines extractions, applies mappings, and writes data/harmonized/master.csv

We will commit a new decision to docs/decisions.md for any new mapping I approve.
```

---

## Starting a validation session

```
The master dataset is at data/harmonized/master.csv. Read PROTOCOL.md section 7
and DATA_DICTIONARY.md.

Write scripts/04_validate.py that:
1. Loads master.csv
2. Checks every column against the data dictionary (type, allowed categorical values)
3. Flags duplicate source_id+sport+age_category rows that aren't justified
4. Flags impossible values (negative rates, ages outside protocol range)
5. Outputs a validation report to outputs/validation_report.md

Then run it and walk me through any failures.
```

---

## End-of-session checklist

Before closing any Claude Code session, ensure:

- [ ] All file changes committed to git (`git add . && git commit -m "..."`)
- [ ] If a new harmonization decision was made, it's in `docs/decisions.md`
- [ ] If a source was extracted, it's logged in `docs/sources.md`
- [ ] If a new column or category was added, `DATA_DICTIONARY.md` is updated

A good commit message:
```
Extracted Collins 2019 — HS football dental injuries, 47 events across 1245 athletes
```

A bad commit message:
```
update
```
