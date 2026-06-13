# `needs_human_review` pile — status & next steps

_As of 2026-06-12 (originally 2026-05-25)._

> **2026-06-12 update — full-text review of the open-access subset.** A full-text
> review pass resolved **7 records (pile 91 → 84)**: 1 included (`halabchi2007`,
> women's Shotokan karate, Iran) and 6 full-text excluded. `scripts/30_oa_url_lookup.py`
> (Unpaywall) found a free URL for **24/91**, and `scripts/31_pmc_availability.py`
> found a free PMC full text for **8/91**. The rest are still unreachable
> programmatically (Cloudflare/paywalled publisher PDFs, scanned page-image PMC
> records, dead URLs). Per-record decisions and the full fetch log:
> `outputs/needs_human_review_fulltext_review_2026-06-12.md` and `docs/decisions.md`.

**84 PubMed records** remain in `needs_human_review` status — abstracts (and, for the unreachable open-access subset, the still-unread full text) lack enough information (usually age range or sport-specific subset) to make a final include/exclude call.

## Why they're stuck

Most need full-text retrieval. Unpaywall finds a free URL for **24 of 91**, and PMC adds free full text for **8 of 91** — but the publisher copies behind those URLs usually block direct fetching:

| publisher | result |
|---|---|
| Wiley Online Library (Dental Traumatology, Community Dentistry...) | HTTP 403 |
| BMJ Journals (BJSM, Injury Prevention) | HTTP 403 |
| Elsevier (Journal of Oral & Maxillofacial Surgery) | HTTP 403 |
| Swiss Dental Journal | HTTP 404 (URL pattern changed) |
| Some publisher direct sites | HTTP 403 |

These publishers serve their PDFs via Cloudflare or similar bot-detection layers that block standard HTTP user-agents. The PDFs ARE legally open access via Unpaywall — but only readable through a browser session.

## How to resolve them

### Option A — Chrome MCP (programmatic browser)

Since the Chrome extension is connected, we can drive a real browser through the URLs from a future session. Each PDF takes ~30 seconds:
- Navigate to the URL
- Browser passes bot check
- Download triggered automatically
- File lands in ~/Downloads
- Move into `data/raw/papers/_oa_pdfs/` and re-screen

I can do this batch-style next session. 18 PDFs ≈ 10–15 min including the screening review per record.

### Option B — Manual review per record

You pull up each PubMed abstract on your end (publisher access via library, school subscription, or Sci-Hub if you're comfortable) and update `screening_overrides.py` with the decision. Doesn't scale beyond ~10 records / hour.

### Option C — Accept current state

Lock the v0.1 release with these 91 as `needs_human_review` and document the limitation transparently. They're not actively blocking any analysis — just an inventory of "couldn't fully resolve from the abstract."

## What we already know about the 91

Distribution by reason code:
- `R-age` (~55): age range not stated in abstract
- `R-data` (~23): unclear whether numerical injury counts are extractable
- `R-mixed` (~7): mixed adult+youth populations, can't isolate youth from abstract
- `R-other` (~6): other ambiguity

Most of these are old (pre-2010) papers from non-PMC journals, OR Wiley dental journals where the publisher blocks programmatic access.

## Recommendation

Take **Option C** for v0.1 release. The 91 are honestly logged as "needs full-text review" with reasons; this transparency is fine for a v0.1 dataset and matches good practice for systematic reviews (the PRISMA workflow expects some records to fall into "uncertain" buckets). Address them post-v1.0 if/when an advisor with library access can pull the PDFs.
