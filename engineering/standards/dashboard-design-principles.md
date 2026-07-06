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

## 7b. The prescribed shape — status matrix + detail list (NOT a notes column)

Rule 4 ("no prose in a row") is violated the moment a scannable matrix grows a free-text
**Notes** column: every row becomes as tall as its prose, and the checkbox columns can no
longer be read down. This is the recurring "broken shape." The fix is structural — **split the
one wide table into two:**

**❌ Broken — matrix and prose in one table (rows are prose-tall; columns unscannable):**
```
| Publication | Draft | Assets | Released | Notes |
|-------------|:--:|:--:|:--:|-------|
| Doc A       | ✅ | ✅ | ✅ | v1.0.2 — long paragraph … several hundred chars … |
| Doc B       | ✅ | ✅ | ✅ | v3.1.2 — another long paragraph … |
```

**✅ Fixed — a one-line-per-row matrix, then a keyed detail list:**
```
### Status matrix (scan down a column)
| Publication | Ver | Draft | Assets | Released |
|-------------|-----|:--:|:--:|:--:|
| Doc A | 1.0.2 | ✅ | ✅ | ✅ |
| Doc B | 3.1.2 | ✅ | ✅ | ✅ |

### Per-item detail
**Doc A** · `slug-a`
v1.0.2 — the full paragraph lives here, any length, no grid to bloat.

**Doc B** · `slug-b`
v3.1.2 — …
```

Rules for the split:
- **The matrix carries only fixed-vocabulary columns** (gate symbols) **+ a short identity + a
  version/date token.** Never a sentence. A row must be one physical line.
- **All prose — history, provenance, audit notes, slugs — moves to the detail list,** keyed by
  the same identity, in the **same order** as the matrix.
- The detail list is `**Name** · `slug`` followed by the prose. It may be long; that's fine — it
  is read one item at a time, not scanned as a grid.
- Applies to **every** status-matrix table (the publication roster's status matrices — `Done` /
  `In progress` / `Upcoming` — are the reference implementation; its freshness-status table and any
  per-head README status grid follow the same shape). If a table has checkbox/symbol columns AND a
  notes column, it is wrong — split it.

### Two fixes — pick by whether the table owns the detail or mirrors it

The split above is one of **two** fixes. Choose by the table's role:

1. **SPLIT** (matrix + keyed detail list) — when the table **owns** the detail (it's the
   source-of-truth board, e.g. the roster's status matrices, the ingestion registry). The prose has
   nowhere else to live, so it moves to a detail list right below the matrix.
2. **TIGHTEN + LINK** — when the table is a **rollup or a mirror** whose detail already lives in
   a linked doc. Do **not** restate paragraphs the source owns. Shorten every cell to a token +
   one short clause and let the linked doc carry the depth. Examples fixed this way: the
   front-door heads board (each head's detail is in its own dashboard) and the
   `document-production/README.md` publication mirror (detail is in the roster → the mirror
   became a compact `Publication | Ver | pp | Released` matrix + a "detail → roster" pointer).
   Restating detail in a mirror is a **double-home** violation (rule 3) as well as a shape one.

### Exemptions — these are NOT the anti-pattern; leave them

- **Logs / ledgers** — chronological, newest-on-top entries where a long "what/why" is the entry
  itself (the YAML-head release ledger, the ingestion push-down intent log, the platform freshness
  ledger). A log is not a status matrix; a scannable-column rule doesn't apply.
- **Reader-facing content / reference matrices** — coverage matrices, gap matrices, template
  lookups, mode-reference tables. The prose is the payload, not a notes column bolted onto a
  status grid. (Litmus: is there a dedicated status/gate column being made unscannable? If the
  ✅ tokens are *embedded in* prose cells rather than in their own column, it's content, not a
  broken dashboard.)
- **Small tables whose cells are already ~one line** — a status column beside short one-liner
  notes is fine; only split/tighten once a cell grows to paragraph length. Watch the borderline
  ones (they tip to broken as notes grow).

### Authoring pressure-test (apply while writing any table)

Before committing a table, ask: **"Does any row have a cell longer than ~one line while another
column in that row is a status symbol?"** If yes → SPLIT (if it owns the detail) or TIGHTEN+LINK
(if it mirrors/rolls up). Never ship the fused shape.

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
