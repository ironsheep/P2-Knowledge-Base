# Document Lineage — Derivation & Supersession

> Backing doc #2 of the ingestion quad. Maps the **trust chain** and records **edition relationships** (the dashboard's "@ edition" markers resolve
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
| Smart Pins (Titus) | **rev 5** (`.docx`, canonical in `sources/smart-pins-titus/`) | PDF-scraped code (`smart-pins-catalog/`) | **re-extraction — DONE 2026-06-12** — prior was scraped from the *PDF* (code fragmented at page breaks, whitespace lost; needed a 5-script recovery); the rev-5 *DOCX* restores fidelity (28/30 examples pnut-ts-validated, 21 figures lossless). Prior `smart-pins-catalog/` **archived** with a pointer (§0.6); downstream re-validation below. | prior archived (not deleted) — git history is the record |
| PASM2 Manual (Parallax) | preliminary | — | **superseded-by-deliverable** — fed our *P2 Assembly Language Reference Manual*; no longer the reference | source kept as input |

## Source → output lineage  ‹which inputs feed which produced output›
| Produced output (manual / KB) | Primary sources | Cross-check / support |
|-------------------------------|-----------------|----------------------|
| P2 Assembly Language Reference Manual | pasm2-manual · p2-instructions-csv · pnut-ts-pasm-ref · silicon-doc | — |
| I/O & Smart Pins User Guide (IOSP) | silicon-doc · smart-pins | **Smart Pins (Titus)** |
| Streamer Programming Guide | silicon-doc · _(verify)_ | _(verify)_ |
| Debug Window User Guide | spin2 (DEBUG) · _(verify)_ | _(verify)_ |
| P2 Assembly Programming (deSilva-style) | authored · silicon-doc · pnut-ts | — |
| `hardware/addon-hyperram-hyperflash.yaml` _(to author — F-122)_ | **hyperRam-n-hyperFlash** (#64004-ES Product Guide, ingested 2026-06-22) | board schematic (Rev A, title-block only) |
| `hardware/addon-*.yaml` ×8 _(to rebuild — F-121)_ | **p2-eval-add-on-boards** per-board docs `boards/addon-*.md` (2025 `#64006`, ingested 2026-06-22) | 2020 `#64006-ES` set edition (cross-edition, forced-OCR) |
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
| smart-pins-titus rev5 | **conflicts** | silicon-doc | WRPIN %AAAA/%BBBB input-selector: Titus `x101=−1, x111=−3` vs silicon-doc `x101=−3, x111=−1` | **silicon-doc wins** — Titus has the two swapped (reviewer #21 correct). Our YAML carries neither yet → gap G-001 |
| smart-pins-titus rev5 | corroborates | silicon-doc · smart-pins | 32-mode taxonomy, mode bit-numbers, X/Y/Z register roles | agree (HIGH) — Titus adds technique/app-note color |

## Downstream re-validation after the Titus re-extraction (§0.6) — 2026-06-12
The prior Titus capture was a **PDF code-scrape** (`smart-pins-catalog/`), not a prose source, and our
Smart-Pins YAML + the *I/O & Smart Pins User Guide* derive primarily from `silicon-doc` + `smart-pins`
(Titus is **cross-check**, not primary). Re-anchoring open findings to the rev5 DOCX surfaced **no
conflict with existing published YAML** (the one confirmed Titus error, #21, concerns a sub-field our
YAML does not carry → logged as gap G-001, not a correction). **Action for the Smart-Pins manual
certification audit:** when it runs, spot-check that no manual text repeated Titus's swapped
x101/x111 selector values; use the silicon-doc values.

## Trust propagation
A source's tier (in `AUTHORITATIVE-SOURCES`) propagates to everything derived from it. A conflict that touches published
YAML → the corrections register (`operations/P2KB-CORRECTION-FINDINGS.md`). On supersession, re-anchor open findings to
the **new** edition (it may confirm, refine, or overturn them).

## Source-code inputs  ‹analyzed production source — carried from old DOCUMENT-LINEAGE›
| Source code | Origin / attribution | Produced | Trust |
|-------------|----------------------|----------|-------|
| `spin-interpreter/v51/Spin2_interpreter.spin2` | Parallax official (SPIN2 v51 distribution) | `spin-interpreter-v51-complete-analysis.md` → (planned) P2 Bytecode Spec | 🟢 |
| `chip-flash-filesystem/flash_fs_v2.0.0.spin2` | **Core:** Chip Gracey · **Production enhancements:** Stephen M. Moraco (Iron Sheep Productions, LLC) — File System API, multi-COG locking, 1000+ unit tests · **Additional:** Jon McPhalen | `chip-flash-filesystem-complete-analysis.md` → 35+ production P2 patterns | 🟢 |

## Planned outputs  ‹**OPEN/deferred** 2026-06-12 — still planned or stale? (see dashboard parked ideas)›
- **P2 Bytecode Specification** (from spin-interpreter analysis) → **Binary Decoder Tool** for PNut Term integration
- **Terminal Window Manual** (from spin2-terminal-windows + screenshots)
- **Hardware Interface Guide** (future, V1.1+)

## Visual assets (cross-cutting)  ‹carried from old DOCUMENT-LINEAGE›
Screenshot/diagram capture feeds **all manuals**. Priorities tracked in `central-analysis/FINAL-SCREENSHOT-NEEDS-V2.md`: architecture diagrams (6, critical) · timing diagrams (8, important) · IDE screenshots (10, helpful). Edge: Screenshots → All Manuals (visual understanding).

## Maintenance
Updated by `ingest-source`: record supersession on each new edition (augment vs re-extraction vs superseded-by-deliverable),
and add source→output links as manuals are produced. This is the lineage half of the sacred trust chain.
