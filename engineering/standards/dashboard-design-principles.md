# Dashboard Design Principles

> How we build status dashboards across the repo (the per-head READMEs + their backing docs).
> Distilled from the four original ingestion trackers — keeping what worked, dropping what drifted.

## 1. What a dashboard is

An **infographic, not prose.** Dense, scannable status; symbols over sentences. The eye should find
state by *pattern* — never by reading paragraphs. If you're writing sentences in a row, it's not a dashboard.

## 2. The two tiers — what each does, and why

| Tier | What it is | Its job | Holds truth? |
|------|-----------|---------|--------------|
| **Top-level dashboard** (rollup) | the per-head README / front door | instant situational awareness — *where everything stands + what's next*, at a glance | **No — it's derived** |
| **Deeper dashboard** (detail) | a backing doc / per-item record | the authoritative record of **one dimension**, where the work is logged and the rollup is computed from | **Yes — the ground truth** |

## 3. Data-flow rule (single source of truth)

1. **Every fact has exactly one home** — the level where it lives. Two homes = drift (the old
   `INGESTION-DASHBOARD` vs `INGESTION-AUDIT-MATRIX` disagreed on the same numbers for this reason).
2. **Do the work where the fact lives** — decorate the detail doc that owns it.
3. **Rollups are derived, not authored** — recompute the top-level value from the detail; never hand-maintain
   it independently.
4. **Propagate on change** — if a decoration changes a value the rollup aggregates, update the rollup; if it
   doesn't touch a rolled-up value, leave the rollup alone.

## 4. Infographic rules (both tiers)

- **One row per item, ~one line tall.** No prose in a row.
- **Independent rating columns** — each column is one dimension with its **own controlled symbol vocabulary**,
  so a *row* reads as a pattern and a *column* scanned top-to-bottom shows where everyone stands on that axis.
- **Consistent symbols + a legend** — a symbol always means the same thing; columns deliberately *look different*
  so gaps/outliers pop.
- **Controlled vocabularies, not free text** — ratings are a small fixed set (`✅ ◐ ⏳ —`; `🏆 🟢 🟡`), never sentences.
- **Rollup metrics at the top** — counts, %, X/N — before the matrix.
- **Group rows by meaningful category.**
- **Half-page glance.** Long notes → footnotes or a linked detail doc, **never in-row** (the tall-notes-column
  anti-pattern that bloated the publication roster).

## 5. Top-level (rollup) dashboard — specific rules

- Lead with the at-a-glance: per-front rollup + an explicit **"what's next."**
- **Every cell is traceable** to a named detail doc; the dashboard *reflects*, it does not *author*.
- Keep it to one screen — if it won't fit, push detail down a tier.

## 6. Deeper dashboard — specific rules

- **Owns exactly one dimension's ground truth** (e.g. trust, or lineage, or per-source work-state). Don't let
  two detail docs own the same fact.
- This is **where decoration (the work) lands.**
- May be denser/longer than the rollup (it's the record), but stays **columnar and scannable** — same infographic rules.
- States **who maintains it** and **what rolls up from it.**

## 7. Worked example — the ingestion triad

```
README.md (rollup)  ──rolls up──┬─ AUTHORITATIVE-SOURCES  (owns: trust tier)
                                ├─ DOCUMENT-LINEAGE        (owns: editions, source→output)
                                └─ sources/<src>/*-extraction-audit.md  (owns: C·K·I·A, completeness)
```
Verification work **decorates the three detail homes**; the README rollup changes only where a rolled-up value does.

---
_Operating guidance mirror: memory `feedback_dashboard_design_density`. Placement of dashboards (per-head READMEs under
`engineering/`, KB excepted) lives there too._
