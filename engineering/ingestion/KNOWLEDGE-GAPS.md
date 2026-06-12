# Knowledge Gaps & Questions-for-Experts — Moving Ledger

> Backing doc #3 of the ingestion **quad** (README dashboard + `AUTHORITATIVE-SOURCES` +
> `DOCUMENT-LINEAGE` + this). Added per the breadth study (`INGESTION-PERSPECTIVES-STUDY.md`, perspectives
> **#8 gap-evolution ledger** + **#9 questions-for-experts**) — the single biggest gap the triad was missing.
> Unlike the other backing docs (static trust / lineage), this is a **moving worklist**: holes open as new
> sources arrive and close as later sources / the designer fill them. _2026-06-12._

## Why this is its own doc
The dashboard answers "how complete is each source." This answers the orthogonal question: **"what does the KB
still not know, and who can answer it?"** It's the boundary of what's verifiable from sources at all. The
dashboard rolls it up as a Tier-1 line (open-questions count + how many are routed to an expert).

---

## Part A — Gap-evolution ledger  ‹perspective #8›

Each row is a knowledge hole. Status **moves**: `OPEN` → `ANSWERED` (cite the source/edition that filled it) →
or `STILL-UNKNOWN` (no source covers it; escalate to Part B). Record the **edition** that closed it so a
later supersession can re-open it if it overturns the answer.

| # | Domain | The gap (question / missing fact) | Status | Filled by (source @ edition) | Opened | Closed |
|---|--------|-----------------------------------|--------|------------------------------|--------|--------|
| _seed from `central-analysis/knowledge-gaps/gaps-consolidated.md` (strikethrough = ANSWERED) + cross-source-qa/questions-remaining_ | | | | | | |

> **Format heritage (from the study):** three prior representations worth carrying — resolution-status tags +
> per-question source-check list (`questions-remaining.md`), strikethrough before/after (`gaps-consolidated.md`),
> and dated "what changed since" batches (`chip-clarifications-update`). This table unifies them.

## Part B — Questions for experts (the answerable-only-by-designer residue)  ‹perspective #9›

The subset of Part A that **no source can close** — only Chip Gracey (or another named authority) can. Carries a
**who-to-ask** routing so the question can actually be sent.

| # | Question | Why no source settles it | Who to ask | State (open / asked / answered) | Links |
|---|----------|--------------------------|------------|---------------------------------|-------|
| _seed from `questions-for-chip-language-focused`, `who-to-ask-remaining-questions`, `missing-content-requests`_ | | | | | |

---

## Inputs that feed this ledger
- **`ingest-source` pass 6** (cross-source conflict audit) — unresolved conflicts and uncovered facts land here.
- **Reviewer notes harvested from source DOCX** — technical questions in embedded editorial notes / Google-Docs
  comments are routed here as credible feedback (e.g. Smart Pins (Titus) rev 5's 27 comments). See the project
  rule on ingesting reviewer notes.
- **The corrections register** — a finding that turns out to be unanswerable-from-sources is mirrored here as a
  Part-B question rather than left CONFIRMED-but-unfixable.

## Maintenance
Updated by `ingest-source` on every pass-6 and on each new edition (a supersession may ANSWER or RE-OPEN rows).
The dashboard's Tier-1 Q&A line reads its counts from here. Stale 2025 gap instances (`gaps-consolidated`,
`questions-remaining`, `AREAS-NOW-UNDERSTOOD`, …) fold into this ledger, then archive.
