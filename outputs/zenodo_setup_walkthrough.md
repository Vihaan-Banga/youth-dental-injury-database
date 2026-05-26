# Zenodo setup walkthrough — getting a permanent DOI for the database

_Read time: 3 min. Total setup time: ~5–10 min, one-time._

## What this gets you

A **permanent, citeable DOI** for the dataset — formatted like `10.5281/zenodo.XXXXXXX`. Researchers cite this when using your data in papers. Two DOIs are minted: a **concept DOI** (always points to the latest version) and a **version DOI** (e.g., `v1.0.0`).

The DOI is what makes the dataset citable in academic literature. Once you have it, you can put it on your CV, the methods paper, the Conrad Challenge submission, the project website, everywhere.

## Cost & maintenance

Free. Zenodo is operated by CERN (yes, the European particle physics lab — they also run the world's largest open-data archive). Once set up, every new GitHub release automatically gets a new DOI minted. No ongoing work.

## When to do this

Best moment: **right before submitting v1.0** for academic use (or before any external use you want cited). Don't bother now — v0.1.0 is a development snapshot. Mint the DOI when:

- [ ] Advisor has signed off on the methodology
- [ ] OSF pre-registration is filed
- [ ] All `needs_human_review` records resolved or transparently documented
- [ ] Methods paper is at least in draft

Tagging v1.0.0 in GitHub triggers Zenodo to mint the DOI automatically.

## The 5-minute setup (you do this once)

### Step 1 — Sign up for Zenodo

Go to https://zenodo.org/login

Click **Login** → **Sign in with GitHub**. This is the easiest path — it links your Zenodo account to your GitHub account using OAuth. You won't have to enter passwords anywhere.

If you prefer not to use GitHub OAuth, you can create a Zenodo account with your school email. Either works.

### Step 2 — Enable Zenodo for your repository

Once logged in, go to https://zenodo.org/account/settings/github/

You'll see a list of all GitHub repositories you have access to. Find:

> Vihaan-Banga/youth-dental-injury-database

Flip the toggle next to it from **Off** to **On**.

That's literally the only Zenodo setup. From this point on, every GitHub release (any tag pushed to the repo) will automatically have a snapshot deposited to Zenodo with its own DOI.

### Step 3 — When you're ready to mint the v1.0 DOI

When you're ready for v1.0 (post-advisor, post-pre-registration, etc.), I'll prepare a v1.0.0 release commit + tag. Then either you or I push the tag, and within ~30 minutes Zenodo emails you with:

- A confirmation that the deposit succeeded
- The version DOI (e.g., `10.5281/zenodo.12345678`)
- The concept DOI (e.g., `10.5281/zenodo.12345677`)

After Zenodo confirms, I:
- Update `CITATION.cff` with the concept DOI
- Update `LICENSE-DATA` to include the DOI in the citation block
- Update the README + website to display the DOI as a clickable badge
- Update the methods paper draft to cite the dataset DOI

## What it looks like once set up

Your repo gets a Zenodo DOI badge that looks like this:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

The DOI URL takes anyone to a Zenodo page showing your dataset metadata, files, version history, and a citation snippet they can copy.

## Optional: Zenodo metadata polish

Zenodo will read most metadata from your repo's `CITATION.cff` automatically — title, author, keywords, license. But you can also customize on Zenodo's side:

- Add an **ORCID** for the author if you have one (free at https://orcid.org — useful for academic identity in general; takes 2 min to register)
- Add additional authors (advisor when secured)
- Pick a **community** (Zenodo lets you submit to themed collections — e.g., "Open Health Data" or "Dental Research")
- Add related publications (link to the methods paper when published)

None of this is required; default Zenodo metadata is fine.

## Summary

| step | who | when | time |
|---|---|---|---|
| Sign in to Zenodo with GitHub | you | now or before v1.0 | 2 min |
| Toggle on `youth-dental-injury-database` | you | same time | 30 sec |
| Tag v1.0.0 | me (with your approval) | when ready for v1.0 | 5 min |
| Zenodo mints DOIs | automatic | within 30 min of tag push | 0 min |
| Update badges + CITATION + methods paper | me | after DOI lands | 15 min |

**The only step that needs you is step 1+2** (which is one continuous flow). Everything else can be automated.

When you're ready to do step 1, follow the link above. When done, tell me and I'll prep the v1.0.0 release commit.
