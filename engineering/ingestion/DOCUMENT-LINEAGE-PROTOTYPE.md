# Document Lineage — Derivation & Supersession  ‹PROTOTYPE›

> **PROTOTYPE** — backing doc #2 of the ingestion quad. Replaces `DOCUMENT-LINEAGE.md` at go-live; kept side-by-side
> until then. Maps the **trust chain** and records **edition relationships** (the dashboard's "@ edition" markers resolve
> here) plus **source → output lineage** (which sources fed which produced manual / KB area). Current relationships
> seeded; deep per-artifact derivation marked _(re-ground)_ for the research pass. _2026-06-11._

## The trust chain (why this exists)
**Trusted sources → qualified (per `AUTHORITATIVE-SOURCES`) → YAML KB (`deliverables/ai/P2`, served via MCP =
download-on-demand) → agents writing P1/P2 code** — AND → **produced community manuals** (human readers). Every link
must preserve fidelity; this doc is the map of those links.

## Editions & supersession  ‹the three relationship flavors — see the edition/role model›
| Logical source | Current | Prior | Relationship | Prior kept? |
|----------------|---------|-------|--------------|-------------|
| Spin2 Language Reference | **v55** | v51a | **augment** — v55 is the full doc (v51a content **+** new language extensions); the document replaces, the material accumulates | yes — lineage/diff |
| Smart Pins (Titus) | **rev 5** (`.docx`, canonical in `sources/smart-pins-titus/`) | PDF-scraped code (`smart-pins-catalog/`) | **re-extraction** — prior was scraped from the *PDF* (code fragmented at page breaks, whitespace lost; needed a 5-script recovery); the rev-5 *DOCX* restores fidelity | no — discard on re-ingest |
| PASM2 Manual (Parallax) | preliminary | — | **superseded-by-deliverable** — fed our *P2 Assembly Language Reference Manual*; no longer the reference | source kept as input |

## Source → output lineage  ‹which inputs feed which produced output›
| Produced output (manual / KB) | Primary sources | Cross-check / support |
|-------------------------------|-----------------|----------------------|
| P2 Assembly Language Reference Manual | pasm2-manual · p2-instructions-csv · pnut-ts-pasm-ref · silicon-doc | — |
| I/O & Smart Pins User Guide (IOSP) | silicon-doc · smart-pins | **Smart Pins (Titus)** |
| Streamer Programming Guide | silicon-doc · _(verify)_ | _(verify)_ |
| Debug Window User Guide | spin2 (DEBUG) · _(verify)_ | _(verify)_ |
| P2 Assembly Programming (deSilva-style) | authored · silicon-doc · pnut-ts | — |
| **YAML KB** (`deliverables/ai/P2`) | all qualified sources | _(re-ground)_ |
| _(future)_ P1 outputs | p1-propeller-manual · p1-datasheet | desilva-p1-tutorial |

## Source relationships (edges)  ‹folds in `CROSS-SOURCE-CONNECTION-SUMMARY` → that doc archives›
Source-to-source connections, keyed by **source ID**. **Structural** edges are placed at acceptance; **analytical**
edges (corroboration / conflict) are populated by `ingest-source` **pass 6** — the dashboard's **X** column tracks pass-6 done.

**Layer stacks** (which sources build on which — structural):
- **Hardware:** `silicon-doc` → `edge-modules` / `eval-board` → `breakouts` → `add-on-boards`
- **Software:** `pasm2` → `spin2-lang-ref` → `smart-pins` → (examples)

**Derived cross-source facts** (synthesized — exist only by *combining* sources; perspective #14, marquee):  ‹register the already-existing syntheses›
- **Board × adapter → accessible P2 pins / power rails** → `sources/p2-board-pin-mapping-knowledge.md`, `p2-complete-signal-flow-matrix.md`, the p2-edge ecosystem-compatibility matrices.
- **P1 ↔ P2 feature / instruction deltas** → `P1-P2-FEATURE-COMPARISON` (folds in here).
- This is the derived metadata that feeds download-on-demand — registered here, not re-derived per query.

**Corroboration / conflict edges** (analytical — pass 6): _(populated during the verification fill)_
| Source A | relation | Source B | on (fact) | resolution (authority) |
|----------|----------|----------|-----------|------------------------|
| _…_ | corroborates / conflicts | _…_ | _…_ | _…_ |

## Trust propagation
A source's tier (in `AUTHORITATIVE-SOURCES`) propagates to everything derived from it. A conflict that touches published
YAML → the corrections register (`operations/P2KB-CORRECTION-FINDINGS.md`). On supersession, re-anchor open findings to
the **new** edition (it may confirm, refine, or overturn them).

## Maintenance
Updated by `ingest-source`: record supersession on each new edition (augment vs re-extraction vs superseded-by-deliverable),
and add source→output links as manuals are produced. This is the lineage half of the sacred trust chain.
