#!/usr/bin/env python3
"""Emit outputs/screening_report_2026-05-21.md — a human-readable audit
trail for every screening decision so the project lead (and advisor) can
verify the AI-assisted first pass.

The report groups decisions by decision-status and then by reason code,
showing per-PMID title + reason + confidence + note. This is the document
to spot-check before promoting any rows to `included`.
"""

import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECISIONS_CSV = ROOT / "data/extracted/_screening/screening_decisions.csv"
ABS_DIR = ROOT / "data/raw/papers/_abstracts"
OUT_PATH = ROOT / "outputs/screening_report_2026-05-21.md"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

decisions = list(csv.DictReader(open(DECISIONS_CSV)))
records = {p.stem: json.load(open(p)) for p in ABS_DIR.glob("*.json")}

# Group by decision then reason
by_dec_reason = defaultdict(lambda: defaultdict(list))
for d in decisions:
    by_dec_reason[d["decision"]][d["reason_code"]].append(d)


REASON_LABELS = {
    "I-pri":    "Primary epidemiology — sport-related dental/orofacial injury data, ages overlap 5–22",
    "E-lang":   "Excluded — non-English (§3.1 v1.0 scope)",
    "E-review": "Excluded — review / SR / MA: kept for source mining only (§3.2)",
    "E-case":   "Excluded — single case report (§3.2)",
    "E-age":    "Excluded — population outside 5–22 age range (§3.1)",
    "E-offtop": "Excluded — not sport-related or wrong subject (§3.1 / §3.3)",
    "E-noprim": "Excluded — no extractable primary numerical injury data (§3.1)",
    "E-nodent": "Excluded — no dental / orofacial-with-dental outcome (§3.3)",
    "E-nonpr":  "Excluded — non-peer-reviewed and not an approved surveillance/governing body source (§3.2)",
    "R-age":    "Needs review — age range / population unclear from abstract",
    "R-mixed":  "Needs review — mixed adult+youth, youth subset extractability needs full text",
    "R-data":   "Needs review — extractable numerical injury data unclear from abstract",
    "R-other":  "Needs review — other ambiguity",
}


lines = []
W = lines.append

W(f"# Screening Report — PubMed seed of 2026-05-21\n")
W(f"_Generated {date.today().isoformat()} from `data/extracted/_screening/screening_decisions.csv`._\n")

W("## What this is\n")
W("This is the audit trail for the first-pass screening of the 200 PubMed candidates seeded on 2026-05-21. Decisions were made by reading **title + abstract + publication-type metadata only** — no full texts have been reviewed yet.\n")
W("**This is not a final screening decision.** Per PROTOCOL.md §4.4, the project lead is the primary screener and an advisor (or designee) second-screens 20% of records. Treat each row below as the AI-assisted screener's recommendation; verify before promoting any record to `included`.\n")
W("**Where to start as the human screener:** \n")
W("1. **Spot-check exclusions first.** Wrong exclusions cost the most because excluded records exit the audit. The high-confidence excludes (non-English, case reports, off-topic) are low-risk; the `E-age` and `E-noprim` excludes are worth confirming.\n")
W("2. **Then work through `needs_additional_review`.** Most of these are blocked on age range or sport-related subset visibility — answerable from the methods section of the full text.\n")
W("3. **Then second-screen 20% of the `screened_included` rows** to satisfy PROTOCOL §4.4 inter-rater reliability.\n\n")

# Totals
from collections import Counter
by_dec = Counter(d["decision"] for d in decisions)
W("## Totals\n")
W(f"- `screened_included`: **{by_dec.get('screened_included', 0)}**")
W(f"- `needs_additional_review`: **{by_dec.get('needs_additional_review', 0)}**")
W(f"- `screened_excluded`: **{by_dec.get('screened_excluded', 0)}**")
W(f"- Total: **{sum(by_dec.values())}**\n")

# Per-decision breakdown
for dec in ("screened_included", "needs_additional_review", "screened_excluded"):
    if dec not in by_dec_reason:
        continue
    W(f"---\n\n## {dec}  ({by_dec.get(dec, 0)})\n")
    for code, group in sorted(by_dec_reason[dec].items()):
        label = REASON_LABELS.get(code, code)
        W(f"### {code} — {label}  ({len(group)})\n")
        # Sort within group by pub_year desc
        group = sorted(group, key=lambda d: (d["pub_year"] or "0", d["pmid"]), reverse=True)
        for d in group:
            rec = records.get(d["pmid"], {})
            title = rec.get("title", "") or "(no title)"
            yr = d["pub_year"] or "????"
            pmid = d["pmid"]
            conf = d["confidence"]
            note = d["note"]
            W(f"- **{pmid}** ({yr}) — {title}")
            W(f"  - confidence: `{conf}` — {note}")
        W("")

W("---\n\n## How decisions were made\n")
W("- **Auto-rules** (`02_screen_candidates.py`): non-English (`language != 'eng'`), `PublicationType = 'Case Reports'`, and `PublicationType ∈ {Review, Systematic Review, Meta-Analysis}` → automatic `screened_excluded` with reason `E-lang`, `E-case`, or `E-review`. Reviews are kept in the source list because PROTOCOL §3.2 explicitly allows them to be mined for primary-source citations — they are just not extracted themselves.")
W("- **Manual decisions** (`screening_overrides.py`): every other record was assigned a decision after reading the title, abstract, and publication-type list from the per-PMID JSON in `data/raw/papers/_abstracts/`. Where the abstract did not disclose age range, sport-related subset, or extractable numerical data, the decision defaulted to `needs_additional_review` rather than risking a wrong exclusion.")
W("- **No full texts were retrieved.** All decisions are reversible by the project lead reading the full text.")
W("- **Confidence ratings**: `high` = the abstract is decisive; `medium` = abstract supports the call but a reasonable reader could disagree; `low` = used only for genuine ambiguity in `needs_additional_review`.\n")

W("## Files referenced\n")
W("- `data/raw/papers/_abstracts/<PMID>.json` — full parsed record per candidate")
W("- `data/raw/papers/_abstracts/_index.csv` — one-line-per-record index")
W("- `data/extracted/_screening/screening_decisions.csv` — canonical decisions CSV")
W("- `scripts/02_screen_candidates.py` — applies auto rules + manual overrides")
W("- `scripts/screening_overrides.py` — the manual decision dictionary")
W("- `scripts/03_apply_screening_to_sources.py` — regenerates `docs/sources.md` from decisions")
W("- `scripts/04_write_screening_report.py` — generates this report")

OUT_PATH.write_text("\n".join(lines))
print(f"Wrote {OUT_PATH} ({len(lines)} lines)")
