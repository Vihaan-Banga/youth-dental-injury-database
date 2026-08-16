#!/usr/bin/env python3
"""Internal-consistency (re-computation) audit of harmonized numeric values.

Read-only. For every row whose stored numbers can be *derived from its own other
fields*, this recomputes the value and checks it against what's stored:

  1. injury_count  vs  rate_raw% × base        (base parsed from rate_denominator_raw)
  2. rate_per_1000_ae  vs  rate_raw converted   (per-100,000 ÷100; per-100 ×10; per-1000/session ×1)
  3. rate_per_1000_ae  vs  injury_count / athlete_exposures × 1000
  4. mislabel heuristic: the injury_count value appears as "<count> of ..." inside
     rate_denominator_raw — a sign the field holds a *denominator*, not a count.

This is NOT source verification (it can't confirm a number against the paper — that
needs full text). It catches ARITHMETIC and FIELD-LABELING errors: a back-calculated
count that doesn't follow from its inputs, a unit conversion done wrong, or a count
whose denominator doesn't match its rate. Complements:
  - scripts/37 (numbers vs the PubMed abstract — external corroboration)
  - scripts/08 (schema / vocabulary validation)

Tolerances are deliberately loose (12% for %×base, since stored percentages are
often rounded) so ordinary rounding doesn't flag; only real mismatches (typically
40%+ off, or a mislabeled field) surface.

Writes outputs/recompute_audit.md and prints a summary. Exit status is always 0 —
this is a reviewer aid, not a build gate.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data/harmonized/master.csv"
OUT = ROOT / "outputs/recompute_audit.md"

# NEISS year files + governing-body report: weighted national estimates / official
# figures, not derivable from stored fields — skip (verify against source query).
SKIP_PREFIX = ("neiss",)
SKIP_IDS = {"rugby_europe_iss_2024"}

PCT_TOL = 0.12      # relative tolerance for count = rate% × base (rounding-tolerant)
CONV_TOL = 0.02     # relative tolerance for a mechanical unit conversion
RATE_TOL = 0.05     # relative tolerance for rate = count / AE × 1000


def num(s):
    try:
        return float(str(s).replace(",", "").replace("%", "").strip())
    except (ValueError, AttributeError):
        return None


def parse_base(denom: str):
    """Extract the population the percentage applies to, from strings like
    '(%) of 2570 schoolchildren...' or '(3 of 186)'. Returns (base, matched_text)
    or (None, None) if no base can be confidently read."""
    if not denom:
        return None, None
    # "of <N>" — the population the proportion is taken over
    m = re.search(r"\bof\s+([\d,]{2,})", denom)
    if m:
        return float(m.group(1).replace(",", "")), m.group(0)
    # "<n> of <N>" fallback
    m = re.search(r"\b(\d[\d,]*)\s+of\s+([\d,]+)", denom)
    if m:
        return float(m.group(2).replace(",", "")), m.group(0)
    return None, None


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-9)


def audit_row(r):
    """Return list of (kind, detail, status) findings for one row."""
    out = []
    inj = num(r.get("injury_count"))
    n = num(r.get("sample_size"))
    ae = num(r.get("athlete_exposures"))
    rr = num(r.get("rate_raw"))
    rp = num(r.get("rate_per_1000_ae"))
    denom = (r.get("rate_denominator_raw") or "")
    dl = denom.lower()

    # --- 4. mislabel heuristic: the injury_count value appears as "<count> of
    # <POPULATION>" in the denominator — a sign the field holds a denominator, not a
    # count. Only population nouns trigger it; "<count> of <N> injuries/teeth/cases"
    # is the legitimate "subset of an injury pool" phrasing and must NOT flag.
    POP = (r"total\s+sample|sample|players|athletes|participants|students|"
           r"children|respondents|pupils|schoolchildren|competitors|boxers|judokas")
    if inj is not None:
        ival = str(int(inj)) if inj == int(inj) else str(inj)
        if re.search(rf"\b{re.escape(ival)}\s+of\s+(?:the\s+)?(?:{POP})\b", denom, re.I):
            out.append(("mislabel?", f"injury_count={ival} appears as '{ival} of <population>' "
                        f"in denominator — may be a DENOMINATOR, not a count", "FLAG"))

    # --- 1. injury_count vs rate_raw% × base
    if inj is not None and rr is not None and ("%" in denom or "of " in dl):
        base, matched = parse_base(denom)
        if base and base != inj:                      # base==inj would be circular
            exp = rr / 100 * base
            status = "CONSISTENT" if rel(exp, inj) <= PCT_TOL else "FLAG"
            out.append(("count=rate%×base",
                        f"{rr}% × {base:g} = {exp:.1f}  (stored {inj:g})", status))

    # --- 2. rate_per_1000_ae vs rate_raw conversion
    if rp is not None and rr is not None and rp != rr:
        if "100,000" in denom or "100000" in dl or "100 000" in denom:
            exp = rr / 100
            status = "CONSISTENT" if rel(exp, rp) <= CONV_TOL else "FLAG"
            out.append(("rate/1000AE (÷100)", f"{rr}/100 = {exp:g}  (stored {rp:g})", status))
        elif re.search(r"per 100 (player|athlete|game|match)", dl):
            exp = rr * 10
            status = "CONSISTENT" if rel(exp, rp) <= CONV_TOL else "FLAG"
            out.append(("rate/1000AE (×10)", f"{rr}×10 = {exp:g}  (stored {rp:g})", status))
        # per-1000 / per-session should already equal rate_raw; any diff is odd
        elif "per 1000" in dl or "session" in dl:
            out.append(("rate/1000AE", f"denominator reads per-1000/session yet "
                        f"rate_raw={rr} != rate_per_1000_ae={rp}", "FLAG"))

    # --- 3. rate_per_1000_ae vs injury_count / AE × 1000
    if rp is not None and inj is not None and ae:
        exp = inj / ae * 1000
        status = "CONSISTENT" if rel(exp, rp) <= RATE_TOL else "FLAG"
        out.append(("rate=count/AE×1000",
                    f"{inj:g}/{ae:g}×1000 = {exp:.4g}  (stored rate {rp:g})", status))

    return out


def main() -> None:
    rows = list(csv.DictReader(open(MASTER)))
    checked_rows = flagged_rows = 0
    consistent = flags = 0
    detail = []       # (source_id, subgroup, findings)
    uncheckable = 0

    for r in rows:
        sid = r["source_id"]
        if sid.startswith(SKIP_PREFIX) or sid in SKIP_IDS:
            continue
        findings = audit_row(r)
        if not findings:
            uncheckable += 1
            continue
        checked_rows += 1
        row_flags = [f for f in findings if f[2] == "FLAG"]
        consistent += sum(1 for f in findings if f[2] == "CONSISTENT")
        flags += len(row_flags)
        if row_flags:
            flagged_rows += 1
        detail.append((sid, r.get("subgroup_label") or r.get("sport") or "", findings))

    # ---- report ----
    L = ["# Re-computation audit (internal numeric consistency)\n",
         "_Generated by `scripts/38_recompute_audit.py`. Recomputes each derivable value "
         "from the row's own inputs. A FLAG means the stored number does not follow from "
         "its inputs (arithmetic or field-labeling issue) — NOT that it's wrong against the "
         "source. NEISS year files and the governing-body report are skipped (weighted "
         "estimates, not derivable). Read-only; not a build gate._\n",
         f"\n**{checked_rows} rows had a recomputable value.** "
         f"{consistent} checks consistent, **{flags} flagged** across "
         f"**{flagged_rows} rows**. ({uncheckable} rows had no recomputable value.)\n"]

    flagged = [(s, sub, f) for (s, sub, f) in detail if any(x[2] == "FLAG" for x in f)]
    if flagged:
        L.append("\n## 🔴 Flagged rows (recompute one at a time)\n")
        L.append("| source_id | subgroup/sport | check | recomputation |")
        L.append("|---|---|---|---|")
        for sid, sub, findings in flagged:
            for kind, det, status in findings:
                if status == "FLAG":
                    L.append(f"| `{sid}` | {sub} | {kind} | {det} |")

    ok_rows = [(s, sub, f) for (s, sub, f) in detail if all(x[2] == "CONSISTENT" for x in f)]
    if ok_rows:
        L.append(f"\n## 🟢 Consistent rows ({len(ok_rows)})\n")
        L.append("Recomputed and matched within tolerance — low arithmetic risk (still verify "
                 "the underlying figure against the source when possible).\n")
        L.append("| source_id | subgroup/sport | check | recomputation |")
        L.append("|---|---|---|---|")
        for sid, sub, findings in ok_rows:
            for kind, det, status in findings:
                L.append(f"| `{sid}` | {sub} | {kind} | {det} |")

    OUT.write_text("\n".join(L) + "\n")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"  {checked_rows} rows recomputable; {consistent} consistent, "
          f"{flags} flags across {flagged_rows} rows.")
    for sid, sub, findings in flagged:
        for kind, det, status in findings:
            if status == "FLAG":
                print(f"  FLAG  {sid} [{sub}]  {kind}: {det}")


if __name__ == "__main__":
    main()
