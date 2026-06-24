"""Shared derivation of the comparability columns added to master.csv at
harmonization time (scripts/07). Imported by 07 (populate), 08 (validate C12),
and consumed downstream by 33 (Rate Explorer).

These columns are DERIVED — they are computed from source-reported fields, not
stored in the per-source extraction CSVs.

measure_type — controlled vocabulary describing the row's outcome measure /
rate basis. Two rows are directly comparable only when they share a
measure_type (and, for the rate families, the same unit; per-AE rates are
normalised in rate_per_1000_ae). Added 2026-06-24 (see docs/decisions.md) to
address the comparability critique (different denominators were mixed with no
machine-readable flag).

  incidence_per_AE            per athlete-exposure (incl. per-100k-AE, per-1000
                              athlete-sessions; the comparable rate tier)
  incidence_per_exposure_hours per player-/athlete-/match-hours
  incidence_per_population    per 100,000 population (NOT athlete-exposures)
  incidence_per_season        per season / player-year
  prevalence_proportion       a reported proportion / percentage (of a sample,
                              or of injuries). NOTE: the proportion's denominator
                              population is in rate_denominator_raw and must be
                              checked before pooling (phase-2 case_definition).
  ed_visit_estimate           NEISS / ED weighted national estimate or ED count
  raw_count                   an unnormalised count of injuries/cases
  rate_ratio_or_effect_size   a rate ratio / odds ratio / effect size
  unclassified_pending_review TEMPORARY — auto-classifier was not confident;
                              awaiting manual classification (see decisions.md).

comparability_group — coarse key on which DIRECT comparison is permitted:
the short measure family, suffixed '__aggregate' for pooled/non-sport-specific
rows (all_sports_aggregate etc.), which should not be pooled with sport-specific
rows even at the same measure_type.
"""
from __future__ import annotations

import re

MEASURE_TYPES = {
    "incidence_per_AE", "incidence_per_exposure_hours", "incidence_per_population",
    "incidence_per_season", "prevalence_proportion", "ed_visit_estimate",
    "raw_count", "rate_ratio_or_effect_size", "unclassified_pending_review",
}

AGGREGATE_SPORTS = {
    "all_sports_aggregate", "all_activities_aggregate", "sports_aggregate",
    "recreational_mixed", "non_sport_setting",
}

_SHORT = {
    "incidence_per_AE": "per_AE",
    "incidence_per_exposure_hours": "per_exposure_hours",
    "incidence_per_population": "per_population",
    "incidence_per_season": "per_season",
    "prevalence_proportion": "prevalence",
    "ed_visit_estimate": "ed_estimate",
    "raw_count": "count",
    "rate_ratio_or_effect_size": "effect_size",
    "unclassified_pending_review": "unclassified",
}

# Manual classifications for the long-tail the auto-classifier can't resolve.
# Keyed by (source_id, rate_denominator_raw.lower().strip()). Fill in after
# manual review; until then those rows are 'unclassified_pending_review'.
# Example: ("shore2021", ""): "raw_count",
MANUAL_MEASURE_TYPE: dict[tuple[str, str], str] = {
}


def measure_type(row: dict) -> str:
    """Classify a master row's outcome measure. Deterministic; returns
    'unclassified_pending_review' when not confident (then listed for manual
    review and optionally pinned via MANUAL_MEASURE_TYPE)."""
    d = (row.get("rate_denominator_raw") or "").lower().strip()
    src = row.get("source_id") or ""

    manual = MANUAL_MEASURE_TYPE.get((src, d))
    if manual:
        return manual

    if "rate ratio" in d or "odds ratio" in d or "incidence rate ratio" in d \
            or re.search(r"\brr\b", d):
        return "rate_ratio_or_effect_size"
    if "hour" in d:
        return "incidence_per_exposure_hours"
    if ("athlete-exposure" in d or "athletic-exposure" in d
            or "athlete exposure" in d or "athlete-session" in d
            or re.search(r"\bae\b", d)):
        return "incidence_per_AE"
    if (("100,000" in d or "100000" in d or "100 000" in d)
            and any(k in d for k in ("population", "children", "capita",
                                     "person", "/year", "participants",
                                     "<18", "youth"))):
        return "incidence_per_population"
    if "season" in d or "player-year" in d or "athlete-year" in d:
        return "incidence_per_season"
    if "%" in d or "(%)" in d or "per cent" in d or "percent" in d \
            or "prevalence" in d or "proportion" in d:
        return "prevalence_proportion"
    if src.startswith("neiss"):
        return "ed_visit_estimate"
    if any(k in d for k in ("national estimate", "ed visit", "neds",
                            "emergency department", "neiss")):
        return "ed_visit_estimate"
    if "count" in d:
        return "raw_count"
    return "unclassified_pending_review"


def comparability_group(row: dict, mtype: str | None = None) -> str:
    mtype = mtype or measure_type(row)
    base = _SHORT.get(mtype, "unclassified")
    if (row.get("sport") or "") in AGGREGATE_SPORTS:
        return base + "__aggregate"
    return base


# --- Data provenance / redistribution rights (per source) ----------------
# Added 2026-06-24 (see docs/decisions.md) after a data-rights critique
# (NCAA-ISP data are owned by the NCAA with redistribution restrictions). The
# database holds NO raw/restricted microdata; every value is one of:
DATA_PROVENANCE = {
    "public_domain_raw",     # extracted from public-domain raw data (NEISS / CPSC)
    "published_summary",     # summary statistics reported in a peer-reviewed paper
    "governing_body_public",  # figures from a public governing-body report
}

# Governing-body / report sources (not peer-reviewed papers, not public-raw).
GOVERNING_BODY_SOURCES = {"rugby_europe_iss_2024"}


def data_provenance(row: dict) -> str:
    """Provenance class of a row's source, for redistribution-rights clarity."""
    src = row.get("source_id") or ""
    if src.startswith("neiss"):
        return "public_domain_raw"
    if src in GOVERNING_BODY_SOURCES:
        return "governing_body_public"
    return "published_summary"
