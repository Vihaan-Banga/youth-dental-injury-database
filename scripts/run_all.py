#!/usr/bin/env python3
"""End-to-end reproducibility orchestrator for the Youth Sports Dental Injury Database.

Rebuilds `data/harmonized/master.csv` from the committed per-source extraction
CSVs, validates it, and regenerates every downstream analysis output and figure —
deterministically and offline. This is the one command a reviewer or collaborator
runs to reproduce the whole database from source-of-truth inputs.

    python3 scripts/run_all.py            # build + validate + regenerate outputs + audit
    python3 scripts/run_all.py --check    # build + validate + audit, then FAIL if the
                                          #   freshly-harmonized master.csv differs from
                                          #   the committed one (reproducibility gate)
    python3 scripts/run_all.py --core     # just harmonize + validate (zero external deps)
    python3 scripts/run_all.py --no-audit # skip the citation audit

STAGES
------
  core      07_harmonize  -> data/harmonized/master.csv   (stdlib only)
            08_validate   -> outputs/validation_report.md  (stdlib only; exits 1 on any FAIL)
  outputs   18,21,23,24,26,27,29,33 — regenerate figures, factsheets, bibliography,
            SQLite export, country + cross-source + NEISS-trend reports, Rate Explorer
            data. Reads master.csv only. Needs matplotlib (see requirements.txt).
  audit     34_audit_citations — re-checks author/year attributions against the cached
            PubMed abstracts. Offline. A reviewer aid, not a pass/fail build gate.

NOT run here: the extraction stage (00-06, 09, 11-17, 19, 20, 22, 25, 28, 30-32).
Those scripts query PubMed / Unpaywall / NEISS and are how the committed
`data/extracted/*.csv` files were originally produced. They require network access
and manual steps, so they are documented provenance, not part of the offline rebuild.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data/harmonized/master.csv"

CORE = [
    ("07_harmonize.py", "Harmonize extraction CSVs -> master.csv"),
    ("08_validate.py", "Validate master.csv against DATA_DICTIONARY (C1-C13)"),
]
OUTPUTS = [
    ("18_visualize.py", "Baseline figures"),
    ("21_cross_source_compare.py", "Cross-source rate comparison"),
    ("23_neiss_trends.py", "NEISS year-over-year trends + figures"),
    ("24_sport_factsheets.py", "Per-sport factsheets"),
    ("26_bibliography.py", "BibTeX bibliography"),
    ("27_sqlite_export.py", "SQLite export"),
    ("29_per_country_analysis.py", "Per-country breakdown + figure"),
    ("33_rate_explorer_data.py", "Rate Explorer data JSON"),
]
AUDIT = [
    ("34_audit_citations.py", "Citation / author attribution audit"),
]


def run(script: str, desc: str) -> tuple[bool, float]:
    """Run one pipeline script; return (ok, seconds)."""
    path = ROOT / "scripts" / script
    print(f"\n\033[1m▶ {script}\033[0m — {desc}")
    t0 = time.monotonic()
    proc = subprocess.run([sys.executable, str(path)], cwd=ROOT)
    dt = time.monotonic() - t0
    ok = proc.returncode == 0
    print(f"  {'✓' if ok else '✗ FAILED'} ({dt:.1f}s)")
    return ok, dt


def git_dirty_master() -> bool | None:
    """True if master.csv differs from the committed version, None if git unavailable."""
    try:
        r = subprocess.run(
            ["git", "diff", "--quiet", "--", str(MASTER.relative_to(ROOT))],
            cwd=ROOT,
        )
        return r.returncode != 0
    except (FileNotFoundError, ValueError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Rebuild + validate the database end-to-end.")
    ap.add_argument("--core", action="store_true", help="only harmonize + validate")
    ap.add_argument("--no-audit", action="store_true", help="skip the citation audit")
    ap.add_argument("--check", action="store_true",
                    help="reproducibility gate: fail if a fresh harmonize changes master.csv")
    args = ap.parse_args()

    stages = list(CORE)
    if not args.core:
        stages += OUTPUTS
        if not args.no_audit:
            stages += AUDIT

    failures: list[str] = []
    total = 0.0
    core_names = {s for s, _ in CORE}

    for script, desc in stages:
        ok, dt = run(script, desc)
        total += dt
        if not ok:
            failures.append(script)
            # A core failure is fatal — downstream stages read master.csv.
            if script in core_names:
                print(f"\n\033[31mCore stage {script} failed — aborting.\033[0m")
                return 1

    # Reproducibility gate: committed master.csv must match a fresh harmonize.
    if args.check:
        dirty = git_dirty_master()
        if dirty is None:
            print("\n\033[33m--check: git not available; skipped the drift check.\033[0m")
        elif dirty:
            print("\n\033[31m--check FAILED: fresh harmonize produced a master.csv that differs "
                  "from the committed one. Commit the regenerated file or investigate drift.\033[0m")
            return 1
        else:
            print("\n\033[32m--check OK: committed master.csv reproduces byte-for-byte.\033[0m")

    print(f"\n\033[1mDone in {total:.1f}s.\033[0m", end=" ")
    if failures:
        print(f"\033[31m{len(failures)} non-core stage(s) failed: {', '.join(failures)}\033[0m")
        return 1
    print("\033[32mAll stages passed.\033[0m")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
