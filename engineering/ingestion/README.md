# Ingestion — Status Dashboard

> The ingestion head's **front-door dashboard** (this folder's README). Multi-tier: glance → registry → drill-down.
> Carries the best ideas from every prior tracker (tags show provenance: ‹DASH›=INGESTION-DASHBOARD,
> ‹MATRIX›=INGESTION-AUDIT-MATRIX, ‹AUTH›=AUTHORITATIVE-SOURCES, ‹LIN›=DOCUMENT-LINEAGE, ‹SKILL›=ingest-source).
> Per-source cells **scanned 2026-06-12**. Registry grounded in `sources/` on disk. _Went live 2026-06-12 (was the quad prototype); folds the former INGESTION-DASHBOARD + INGESTION-AUDIT-MATRIX._

## Tier 1 — At a glance
- **Sources:** 36 folders on disk → **32 logical sources** · 29 P2 · 3 P1  ‹v51a = lineage; code-analysis + marketing-materials = meta; pasm2-manual-development = dev scaffold›
- **By authority:** 🏆 21 · 🟢 7 · 🟡 4  ‹32 logical sources; v51a lineage + 3 non-source folders excluded›
- **Ingest completeness:** mature ~17 (≥90% + audit) · partial ~8 (40–89%) · minimal/not-started ~7 (incl. hyperRam un-ingested, Titus rev5 staged)  ‹scanned 2026-06-12›
- **Open questions:** _(n)_ in the gap ledger · _(m)_ routed to an expert  ‹rolled up from KNOWLEDGE-GAPS›
- **Latest ingested:** Spin2 Language Reference @ **v55** (matched-compiler; augmentative over v51a) ‹LIN›
- **What's next:** re-ingest **Smart Pins (Titus) rev 5** (replaces lossy extraction) — cross-checks the *I/O & Smart Pins User Guide*
- **Why track this:** qualified inputs feed the YAML KB → **download-on-demand (MCP)** → agents writing P1/P2 code their models were never trained on. Input trust + completeness propagate straight to agent reliability.

## Tier 2 — Source registry (by category — categories preserved from existing trackers)

> **Rows = logical sources at their CURRENT edition** (not raw folders). A version update *replaces* the prior doc as authority; prior editions are lineage in `DOCUMENT-LINEAGE`, not separate rows — two sub-cases: **augmentative** (newer edition, content grew, keep prior) vs **re-extraction** (prior was lossy, discard it). **Role** ≠ authority: a source is *primary* (derive content) or *cross-check* (corroborate/hint).
Cells: ✅ done · ◐ partial · ⏳ pending · — n/a · ? verify  |  Passes ‹SKILL 7-pass›: **C** content · **K** code · **I** images · **A** audit/validated · **X** cross-source (pass 6 — connected/corroborated vs other sources)  |  Auth: 🏆 authoritative · 🟢 green · 🟡 yellow · ◳ draft

### P2 · Core language & architecture  ‹AUTH "Core Technical"›
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| silicon-doc | 🏆 | ✅ | ✅ | ✅ | ✅ | ✅ | 75% _(stated; arch 100%, some sections 90%)_ |
| **Spin2 Language Reference** @ v55 ‹prior v51a — lineage, augmentative› | 🏆 | ✅ | ✅ | ✅ | ✅ | ⏳ | 100% _(delta v52→v55; X pending. v51a lineage fully extracted)_ |
| p2-instructions-csv | 🏆 | ✅ | — | — | ✅ | ⏳ | 100% _(audit: pasm2-spreadsheet-audit.md — aliased)_ |
| chip-gracey-clarifications | 🏆 | ✅ | — | — | ⏳ | ⏳ | ? _(structured text; no audit / cross-source doc)_ |
| p2-qa-spreadsheet | 🟢 | ✅ | — | — | ✅ | ⏳ | ~80% _(991 rows; audit present; no cross-source)_ |
| **PASM2 Manual** (Parallax, preliminary) | 🏆 | ✅ | ◐ | ◐ | ✅ | ✅ | 64% _(stated; code embedded in docx md, not a validated catalog; **superseded** as the PASM2 reference by our Assembly manual)_ |

### P2 · Smart Pins
| smart-pins | 🟢 | ✅ | ✅ | ✅ | ✅ | ✅ | 97% _(stated; 174 examples, 21 mode images)_ |
| **Smart Pins (Titus)** @ rev 5 ‹re-ingest, old extraction retired› | 🟡 **cross-check** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | 0% _(rev5 docx staged — **next ingestion**; prior PDF extraction retired; cross-checks IOSP guide)_ |

### P2 · Hardware ecosystem  ‹distinct top-level category — boards/add-ons/datasheets, NOT software/compilers›
_Boards share a 12-pin header (8 I/O + power/ground); ×8 headers = all 64 pins. Add-on boards ride one header or a header pair._

**Datasheets & specs (PDF)**  ‹AUTH "Core Technical" → re-filed as hardware›
| p2-datasheet | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 94% _(stated; audit: datasheet-audit-report.md — aliased)_ |
| p2-spec-sheet | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | 99% _(stated; audit: spec-sheet-audit-report.md — aliased; no images/cross-source)_ |

**Development boards (12-pin header system)**  ‹AUTH "Hardware Boards"›
| p2-eval-board ‹Rev C — retired / left behind› | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 100% _(stated)_ |
| edge-standard-module | 🏆 | ✅ | — | ✅ | ⏳ | ✅ | ~80% _(missing audit doc — only row with X but no A)_ |
| edge-32mb-module | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 100% _(stated)_ |
| edge-breakout-board | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 100% _(stated; 18 images)_ |
| edge-mini-breakout | 🏆 | ✅ | — | ⏳ | ✅ | ✅ | 100% _(stated; no images extracted)_ |
| edge-module-breadboard | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 100% _(stated; 20 images — most complete board)_ |

**Add-on boards (ride on headers)**  ‹AUTH "Add-On Modules"›
| p2-eval-add-on-boards ‹collection — incl. HUB75 + range› | 🏆 | ✅ | — | ⏳ | ✅ | ✅ | ~95% _(no images; still enumerate individual add-ons incl. HUB75)_ |
| universal-motor-driver | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | ~85% _(raw txt; no images/cross-source)_ |
| hyperRam-n-hyperFlash | 🟢 | ⏳ | — | ⏳ | ⏳ | ⏳ | 0% _(**un-ingested** — only raw CAD/schematic files)_ |

**Adapters & connectivity**
| parallax-wx-wifi | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | ~90% _(stated; 12+ images flagged as debt)_ |
| p2-wx-adapter | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | ~90% _(stated; 8+ images flagged as debt)_ |
| propplug-rev-e | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | ~95% _(stated; no images)_ |

### P2 · Boot & loaders
| rom-booter | 🟢 | ✅ | ✅ | — | ⏳ | ⏳ | ~40% _(.lst assembly; no audit / cross-source)_ |
| flash-loader | 🟢 | ✅ | ✅ | — | ⏳ | ⏳ | ~50% _(.spin2 source; no audit / cross-source)_ |

### P2 · Compiler & tooling  ‹proposed bucket — veto anytime›
| pnut-ts-pasm-ref | 🏆 | ✅ | ✅ | — | ◐ | ⏳ | 95% _(stated; 359-instr JSON DB; audit material in audit/ subfolder — needs a consolidated rollup doc, 5B)_ |
| iron-sheep-compiler | 🟢 | ◐ | — | — | ⏳ | ⏳ | ~15% _(single condition-codes doc only)_ |

### P2 · Community code & tutorials  ‹proposed›
| taqoz | 🟡 | ◐ | — | — | ⏳ | ⏳ | ~25% _(preliminary web research only; unverified)_ |
| quick-bytes-code | 🟡 | ⏳ | ◐ | — | ⏳ | ⏳ | ~15% _(one .spin2; zips unextracted; no narrative)_ |

### P2 · Other reference  ‹proposed›
| p2docs-github-io | 🟡 | ◐ | — | — | ⏳ | ⏳ | ~30% _(narrative + validation report only)_ |

### P1 · (queued — bring the P1 database up to P2-level richness)  ‹DASH "P1 Sources"›
_P1 = first Propeller, P2 = second. 2–3 core P1 docs queued (datasheet + manual, possibly deSilva P1 tutorial); some already partially ingested (text+audit) → queue completes images/code + enriches._ **Plan:** `plans/p1-sources-ingestion-plan.md`.
| p1-propeller-manual-v1.2 | 🏆 | ✅ | ⏳ | ⏳ | ✅ | ⏳ | ~60% _(803KB text + audit; code inline; no images)_ |
| p1-datasheet-v1.4 | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | 100% _(stated; no images extracted)_ |
| desilva-p1-tutorial | 🟢 | ✅ | ◐ | ⏳ | ⏳ | ⏳ | ~45% _(text + voice-analysis; code inline; no audit)_ |
| p1-application-notes (AN001–015, 018–019 · 17 docs) | 🏆 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | 0% _(queued; **AN016/AN017 never published**; topics: counters / exec-time / sigma-delta ADC / VGA GUI / GPS NMEA / XBee / SD-FS / coroutines …)_ |

## Not standalone sources  ‹folders under sources/ that are NOT registry rows›
| Folder | Why | Disposition |
|--------|-----|-------------|
| code-analysis | derived analysis docs (BLDC / debugger / flash-loader) — not raw extraction | reclassify as derived-analysis; archive/relocate out of `sources/` at cleanup |
| marketing-materials | 2.9 KB summary, not a source document | reclassify; low value |
| pasm2-manual-development | dev scaffold for the PASM2 Manual | **collapse** into the PASM2 Manual / workspace; archive |

## Tier 2b — Domain coverage (by-topic lens)  ‹un-parked per perspectives-study #10›
> Orthogonal to the per-source registry: how well is each *knowledge domain* covered, across all sources combined? Cells fill at the research pass.

| Domain | Primary sources | Coverage | Notes |
|--------|-----------------|----------|-------|
| Architecture (cogs/hub/CORDIC/streamer/events) | silicon-doc · p2-datasheet | _(verify)_ | |
| PASM2 instruction set | p2-instructions-csv · pnut-ts-pasm-ref · silicon-doc | _(verify)_ | X/491 instructions |
| Spin2 language | spin2-v55 · pnut_ts | _(verify)_ | |
| Smart Pins | smart-pins · smart-pins-titus (rev5) · silicon-doc | _(verify)_ | |
| Hardware ecosystem (boards/add-ons) | edge-* · eval-board · datasheets | _(verify)_ | |
| Boot & loaders | rom-booter · flash-loader · silicon-doc | _(verify)_ | |
| P1 → P2 | p1-* · desilva-p1 | _(verify)_ | bring P1 to P2 richness |

## Tier 3 — Drill-down & provenance (linked, never inlined)
- **Per-source work-state & evidence** → `sources/<src>/<src>-complete-extraction-audit.md` ‹SKILL: the 7-pass definition of "complete"›
- **Trust + source metadata** (tier / origin / conflict precedence) → `AUTHORITATIVE-SOURCES.md`
- **Derivation & supersession** (editions; source → KB/manual) → `DOCUMENT-LINEAGE.md`
- **Knowledge gaps & expert questions** (moving ledger — what we still don't know + who to ask) → `KNOWLEDGE-GAPS.md`
- **Central analysis hub** (cross-source Q&A, gaps, instruction/feature matrices, syntheses) → `central-analysis/` _(synthesis doc still pending)_

## Navigation & how-to  ‹carried from the former README hub›
- **How to ingest** → `methodology/source-ingestion-methodology.md` · `work-modes/document-ingestion-focused.md` · `methodology/ingestion-pipeline/ingestion-audit-protocol.md` · or the `ingest-source` skill
- **Matrices** → `extraction-matrices/` · `visual-assets/` (image + code extraction matrices)
- **Source folders** → `sources/` · **Plans** → `plans/`

## Planned ingestions  (pushdown — newest intent first)  ‹DASH "Planned"›
| When | Source | Note |
|------|--------|------|
| next | Smart Pins (Titus) rev 5 | canonical staged at `sources/smart-pins-titus/` (rev5 .docx, 2026-03-31, **27 reviewer comments**). **Re-extraction** replaces the lossy *PDF*-scraped prior (`smart-pins-catalog/`). **Harvest the reviewer comments + inline editor notes as credible feedback** → technical Qs to KNOWLEDGE-GAPS. Role: cross-check for IOSP guide. |
| next | _(2nd source — TBD with user)_ | |
| **queued** | P1 datasheet + P1 manual (+ deSilva P1?) | bring P1 DB up to P2 richness; some partially ingested → complete + enrich |
| later | Quick Bytes | plan: `plans/QUICK-BYTES-READY-TO-EXECUTE.md`; scraper tools ready (`scrape-quick-bytes.py`, `extract-tag-taxonomy.py`, `youtube-playlist-correlator.py`); re-confirm intent (old "next 2-3 days" note stale) |

## Parked ideas to adjudicate (keep until proven meaningless)  ‹MATRIX›
- **Enrichment axis** — narrative / style-analysis / cross-source / central-hub-link. Tracked the 2025-09 central-analysis effort (stalled). Keep as drill-down column, fold, or drop?
- **Knowledge-domain coverage** — ✅ **un-parked** → now **Tier 2b** (by-topic lens) above.
- **Completeness% method** — two old guesses exist (DASH 75% vs MATRIX 85%, and per-source disagree). Re-derive from passes-done at verification; bracketed for now per your note.
- **Style / voice analysis** (per-source 4-level style profile; 2/24 done in the old matrix) — **OPEN / deferred** (2026-06-12). Likely *manual-head* metadata, not an ingestion pass. Carried-not-dropped; revisit when ready.
- **Pipeline deliverables** (P2 Bytecode Spec, Terminal Window Manual, Hardware Interface Guide, Binary Decoder Tool — from old DOCUMENT-LINEAGE) — **OPEN / deferred** (2026-06-12): still planned or stale? Parked in DOCUMENT-LINEAGE 'planned outputs' until confirmed.

---
_Per-source cells **scanned 2026-06-12** (read-only fan-out over all 36 folders). **Normalization findings (for go-live / verification fill):** (1) ✅ **audit-filename drift — RESOLVED (aliased):** actual audit filenames recorded in the rows; canonical `<src>-complete-extraction-audit.md` applies to new ingestions. `pnut-ts-pasm-ref` still needs a *consolidated* rollup audit (5B). (2) ✅ **Non-sources demoted:** `code-analysis` + `marketing-materials` (meta) and `pasm2-manual-development` (dev scaffold) moved out of the registry → see 'Not standalone sources'. Physical archive/relocate deferred to cleanup. (3) **Image debt** is the most common gap (most hardware rows + the P1 docs have no images extracted). (4) **Zero/un-ingested:** `hyperRam-n-hyperFlash` (raw CAD only); `smart-pins-titus` staged (= next ingestion). **Cross-source (X)** is absent on ~20 sources — the bulk of the verification fill. folds the former `INGESTION-DASHBOARD` + `INGESTION-AUDIT-MATRIX` (archived 2026-06-12)._
