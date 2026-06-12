# Ingestion Perspectives — Breadth Study  ‹study artifact›

> **Purpose:** before we reconcile the ingestion panels, collect *every lens* we've ever used to track and
> learn from ingestion — so the new triad carries them all, not just the ones already in it. Built from a
> 5-agent breadth+depth survey of ~150 **meta** markdown docs across `engineering/ingestion/**` (raw extracted
> content excluded). _2026-06-11._
>
> **Key framing:** most instance docs are **stale** (2025-08/09, pre-`ingest-source`-skill, pre-v55). We extract
> the **perspective** (the lens) here; the stale instances then **fold-and-archive** once a panel carries the lens.

---

## Part 1 — Every perspective we found (consolidated, 20)

`A` = judges ingestion **accuracy/quality** · `R` = captures **relationships / derived metadata** · *In triad?* = already in the new dashboard/authoritative/lineage prototypes.

| # | Perspective | What it tracks | A/R | In triad? | Exemplar docs (mostly stale) |
|---|-------------|----------------|-----|-----------|------------------------------|
| 1 | **Source discovery / inventory** | the universe of logical sources (36, not the stale 24) | A | ✅ dashboard registry | SOURCE-DISCOVERY-V2, P2-SOURCE-STUDY-COMPLETE-MAP |
| 2 | **Per-source completeness (7-pass C·K·I·A·X)** | which passes done per source | A | ✅ dashboard | `sources/*/*-complete-extraction-audit.md`, EXTRACTION-INDEX-V2 |
| 3 | Extraction-accuracy / structural validation | clean capture; broken tables; CSV/JSON field validity | A | ⚠ folds into #2 | pasm2-spreadsheet-audit, identified-broken-tables, pnut-ts content-analysis |
| 4 | Section-walkthrough gap-ID | section-by-section coverage % | A | ✗ | datasheet-walkthrough-analysis, silicon-doc-v35-walkthrough-audit |
| 5 | Multi-axis health scoring | 7 axes (style/extract/complete/consistency/gaps/quality/usability) → health % | A | ✗ (could refine #2) | datasheet-audit-report |
| 6 | **Trust / authority tiering + precedence** | per-source tier + conflict-resolution order | A | ✅ authoritative | AUTHORITATIVE-SOURCES, conflicts-and-trust-zones, source-quality-matrix |
| 7 | Cross-source conflict detection | A-says / B-says + resolution | A+R | ⚠ partial (X + corrections register) | conflicts-and-trust-zones, VERSION-HISTORY-CONFLICTS, `*-cross-source-analysis.md` |
| 8 | **Knowledge-gap evolution ledger** | **known / answered / still-unknown — moving as later sources fill holes** | A+R | ✗ **ADD** | cross-source-qa/questions-remaining, knowledge-gaps/gaps-consolidated (strikethrough), AREAS-NOW-UNDERSTOOD, chip-clarifications-update |
| 9 | **Questions-for-experts / unresolved routing** | the answerable-only-by-Chip residue + who-to-ask | A | ✗ **ADD** | questions-for-chip-language-focused, who-to-ask-remaining-questions, missing-content-requests |
| 10 | **Coverage matrices (instruction / feature / domain)** | X/491 instructions; by-topic domain rollup | A | ✗ (domain = dashboard "parked") **ADD** | P2-FEATURE-COVERAGE-MATRIX, instruction-completion-matrix, P2-COMPLETE-INSTRUCTION-MATRIX |
| 11 | **Lineage / supersession (editions)** | augment / re-extraction / superseded-by-deliverable | A+R | ✅ lineage | DOCUMENT-LINEAGE, V1-TO-V2-MIGRATION-AUDIT, silicon-v35-comparative |
| 12 | **Source → output lineage** | which sources fed which manual / KB area | R | ✅ lineage | DOCUMENT-LINEAGE |
| 13 | Per-claim corroboration matrix | claim × source → CONSISTENT / conflict | A+R | ⚠ (this is the *format behind* X) | smart-pins basic-io/source-audit, instruction-completion-matrix |
| 14 | **Derived cross-source facts (hardware pin-mapping &c.)** | board × adapter → accessible pins/power; unified syntheses | R | ✗ **ADD (marquee)** | p2-edge-complete-ecosystem-compatibility-matrix, `sources/p2-board-pin-mapping-knowledge.md`, p2-complete-signal-flow-matrix |
| 15 | Cross-generation comparison (P1 ↔ P2) | P1-vs-P2 feature/instruction deltas | R | ✗ (folds into #14) | P1-P2-FEATURE-COMPARISON |
| 16 | Code-pattern / idiom corpus extraction | patterns & idioms across the 730-file corpus | R | ✗ (derived subtype) | COMPLETE-PATTERN-AUDIT-730-FILES, idiom-extraction-* |
| 17 | Visual-asset extraction tracking | images extracted / failed / per-image reviewed | A | ⚠ (the **I** in C·K·I·A) | INGESTION-IMAGE-EXTRACTION-MATRIX, EXTRACTION-FAILURES-MASTER-LIST |
| 18 | Style / voice capture | 4-level style profile (for manual production) | R | ✗ (manual-head metadata) | datasheet-style-analysis, spec-sheet-style-analysis |
| 19 | Enrichment status (priority queue) | per-instruction enrichment backlog (heat-scored) | A | ✗ (yaml-head metadata) | enriched-instructions/enrichment-status |
| 20 | Provenance integrity (right-source) | caught wrong-source content (manual-gen masquerading as Titus) | A | ⚠ folds into #2/#11 | smart-pins CODE-SOURCE-CORRECTION-SUMMARY |

---

## Part 2 — Already carried by the triad
#1 inventory, #2 completeness (C·K·I·A·X), #6 trust+precedence, #11 editions/supersession, #12 source→output, plus #7/#13 partially (the **X** column + corrections register). The triad's backbone is sound — the survey **confirms** it.

## Part 3 — Perspectives to ADD to the panels (the point of this study)

Four genuinely-missing lenses, each recurring across many docs and (8, 14) the ones you described by name:

1. **Knowledge-gap evolution ledger (#8)** — the moving *known / answered / still-unknown*, where each new source opens and fills holes. This is the facts-and-holes cross-check you described, and it's the single biggest gap in the triad. It was represented three ways worth copying: **resolution-status tags** + per-question source-check list (`questions-remaining.md`), **strikethrough before/after** (`gaps-consolidated.md`), and **dated "what changed since" batches** (`chip-clarifications-update`). → **new panel or a lineage section** (decision below).
2. **Derived cross-source facts (#14, marquee)** — facts that exist *only* by combining sources: board × adapter → which hardware lands on which P2 pin/rail. These **already exist** as `sources/p2-board-pin-mapping-knowledge.md`, `p2-complete-signal-flow-matrix.md`, and the edge compatibility matrices — they're just not registered in the triad. This is exactly the derived metadata that feeds download-on-demand. → **register in `DOCUMENT-LINEAGE`'s relationships section** (it already holds edges/stacks).
3. **Coverage matrices — domain + instruction (#10)** — a *by-topic* rollup orthogonal to per-source (Architecture / PASM2 / Spin2 / Smart Pins / Hardware / Boot / P1→P2), plus instruction-set coverage (X/491). Domain-coverage is already the dashboard's "parked idea" — **un-park it as a second dashboard lens.**
4. **Questions-for-experts / unresolved routing (#9)** — the residue only the designer can answer + a who-to-ask matrix. Marks the *boundary of what's verifiable from sources at all*. → companion to the gap ledger (#8).

**Enrichers (not new panels — they refine existing cells/formats):** #13 per-claim corroboration matrix *is* the record format behind the **X** column; #5 multi-axis health scoring could refine how **completeness** is computed; #4 walkthrough is a *method* for filling #2; #16 code-patterns + #15 P1↔P2 are subtypes of #14; #18 style + #19 enrichment are really **manual-head / yaml-head** metadata, noted for those heads.

## Part 4 — Structural finding: the per-source detail backbone already has a schema
Every source is *meant* to carry two level-3 detail docs — `*-complete-extraction-audit.md` (accuracy/completeness, perspective #2–5) + `*-cross-source-analysis.md` (relationships/trust, #6–8) — bound by `sources/CROSS-SOURCE-CONNECTION-TEMPLATE.md`. **These are exactly the detail homes the dashboard rolls up from** (per the data-flow rule). Coverage is **uneven: 18/36 have an audit, 12/36 have a cross-source-analysis.** So the verification fill is partly: **create the missing per-source detail docs**, and **link the already-existing derived hardware syntheses** into lineage.

## Part 5 — Disposition (per the archive process)
Almost every instance doc here is 2025-08/09 historical (pre-skill, pre-v55). Path: extract the perspective (this study) → make the panels carry it → then **fold-and-archive** the stale instances to a gitignored `archive/`. Freshest live exceptions to *keep*: the code/image extraction matrices (updated 2025-11), `smart-pins/.../basic-io/source-audit.md` (2026-01), and the existing derived hardware syntheses.

---

## Decisions for next session
- **Gap ledger (#8) + questions-routing (#9):** a **4th ingestion panel** ("Cross-Source Q&A & Gap Ledger"), or a **section inside `DOCUMENT-LINEAGE`**? (They're substantial and moving — I lean toward a 4th panel.)
- **Domain-coverage (#10):** confirm un-parking it as the dashboard's second (by-topic) lens.
- **Derived facts (#14):** register the existing pin-mapping/signal-flow syntheses in `DOCUMENT-LINEAGE`'s relationships section — confirm that's the home.
