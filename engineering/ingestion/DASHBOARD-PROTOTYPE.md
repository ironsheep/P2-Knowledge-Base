# Ingestion — Status Dashboard  ‹PROTOTYPE›

> **PROTOTYPE** of the new `engineering/ingestion/README.md`. Multi-tier: glance → registry → drill-down.
> Carries the best ideas from every prior tracker (tags show provenance: ‹DASH›=INGESTION-DASHBOARD,
> ‹MATRIX›=INGESTION-AUDIT-MATRIX, ‹AUTH›=AUTHORITATIVE-SOURCES, ‹LIN›=DOCUMENT-LINEAGE, ‹SKILL›=ingest-source).
> **Per-source work-state cells are PLACEHOLDERS** — filled by authoritative re-scan (step 4). Old trackers stay
> live until go-live. Registry grounded in `sources/` on disk (36 folders). _Prototype 2026-06-11._

## Tier 1 — At a glance
- **Sources:** 36 on disk · 33 P2 · 3 P1  ‹ground truth, not the stale 24›
- **By authority:** 🏆 _(n)_ · 🟢 _(n)_ · 🟡 _(n)_ · ◳ draft _(n)_  _(verify)_
- **Ingest completeness:** fully (7/7 passes) _(n)_ · in-progress _(n)_ · not-started _(n)_  _(verify)_
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
| silicon-doc | 🏆 | ? | ? | ? | ? | ? | _(verify)_ |
| **Spin2 Language Reference** @ v55 ‹prior v51a — lineage, augmentative› | 🏆 | ? | ? | ? | ? | ? | _(verify)_ |
| p2-instructions-csv | 🏆 | ? | ? | — | ? | ? | _(verify)_ |
| chip-gracey-clarifications | 🏆 | ? | ? | — | ? | ? | _(verify)_ |
| p2-qa-spreadsheet | 🟢 | ? | ? | — | ? | ? | _(verify)_ |
| **PASM2 Manual** (Parallax, preliminary) | 🏆 | ? | ? | ? | ? | ? | _(trusted Parallax but **incomplete / not fully vetted**; **superseded** as the PASM2 reference by our produced P2 Assembly Language Reference Manual)_ |
| pasm2-manual-development | — | ? | ? | ? | ? | ? | _(verify: collapse into above, or our dev workspace — not a separate source?)_ |

### P2 · Smart Pins
| smart-pins | 🟢 | ? | ? | ? | ? | ? | _(verify)_ |
| **Smart Pins (Titus)** @ rev 5 ‹re-ingest, old extraction retired› | 🟡 **cross-check** | ? | ? | ? | ? | ? | _(community-built / Jon Titus, not Parallax → below authoritative; cross-checks IOSP guide)_ |

### P2 · Hardware ecosystem  ‹distinct top-level category — boards/add-ons/datasheets, NOT software/compilers›
_Boards share a 12-pin header (8 I/O + power/ground); ×8 headers = all 64 pins. Add-on boards ride one header or a header pair._

**Datasheets & specs (PDF)**  ‹AUTH "Core Technical" → re-filed as hardware›
| p2-datasheet | 🏆 | ? | — | ? | ? | ? | _(verify)_ |
| p2-spec-sheet | 🏆 | ? | — | ? | ? | ? | _(verify)_ |

**Development boards (12-pin header system)**  ‹AUTH "Hardware Boards"›
| p2-eval-board ‹Rev C — retired / left behind› | 🏆 | ? | — | ? | ? | ? | _(verify)_ |
| edge-standard-module | 🏆 | ? | — | ? | ? | ? | _(verify)_ |
| edge-32mb-module | 🏆 | ? | — | ? | ? | ? | _(verify)_ |
| edge-breakout-board | 🏆 | ? | — | ? | ? | ? | _(verify)_ |
| edge-mini-breakout | 🏆 | ? | — | ? | ? | ? | _(verify)_ |
| edge-module-breadboard | 🏆 | ? | — | ? | ? | ? | _(verify)_ |

**Add-on boards (ride on headers)**  ‹AUTH "Add-On Modules"›
| p2-eval-add-on-boards ‹collection — incl. HUB75 + range› | 🏆 | ? | — | ? | ? | ? | _(verify: enumerate individual add-ons incl. HUB75)_ |
| universal-motor-driver | 🏆 | ? | — | ? | ? | ? | _(verify)_ |
| hyperRam-n-hyperFlash | 🟢 | ? | — | ? | ? | ? | _(verify)_ |

**Adapters & connectivity**
| parallax-wx-wifi | 🏆 | ? | — | ? | ? | ? | _(verify)_ |
| p2-wx-adapter | 🏆 | ? | — | ? | ? | ? | _(verify)_ |
| propplug-rev-e | 🏆 | ? | — | ? | ? | ? | _(verify)_ |

### P2 · Boot & loaders
| rom-booter | 🟢 | ? | ? | — | ? | ? | _(verify)_ |
| flash-loader | 🟢 | ? | ? | — | ? | ? | _(verify)_ |

### P2 · Compiler & tooling  ‹proposed bucket — veto anytime›
| pnut-ts-pasm-ref | 🏆 | ? | ? | — | ? | ? | _(verify)_ |
| iron-sheep-compiler | 🟢 | ? | ? | — | ? | ? | _(verify)_ |

### P2 · Community code & tutorials  ‹proposed›
| taqoz | 🟡 | ? | ? | — | ? | ? | _(verify)_ |
| quick-bytes-code | 🟡 | ? | ? | — | ? | ? | _(verify)_ |

### P2 · Other reference  ‹proposed›
| p2docs-github-io | 🟡 | ? | ? | ? | ? | ? | _(verify)_ |
| marketing-materials | 🟡 | ? | — | ? | ? | ? | _(verify)_ |
| code-analysis | 🟡 | ? | ? | — | ? | ? | _(verify; source or meta-folder?)_ |

### P1 · (queued — bring the P1 database up to P2-level richness)  ‹DASH "P1 Sources"›
_P1 = first Propeller, P2 = second. 2–3 core P1 docs queued (datasheet + manual, possibly deSilva P1 tutorial); some already partially ingested (text+audit) → queue completes images/code + enriches._
| p1-propeller-manual-v1.2 | 🏆 | ? | ? | ? | ? | ? | _(verify)_ |
| p1-datasheet-v1.4 | 🏆 | ? | — | ? | ? | ? | _(verify)_ |
| desilva-p1-tutorial | 🟢 | ? | ? | ? | ? | ? | _(verify)_ |

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
- **Trust + source metadata** (tier / origin / conflict precedence) → `AUTHORITATIVE-SOURCES-PROTOTYPE.md` (→ `AUTHORITATIVE-SOURCES.md` at go-live)
- **Derivation & supersession** (editions; source → KB/manual) → `DOCUMENT-LINEAGE-PROTOTYPE.md` (→ `DOCUMENT-LINEAGE.md` at go-live)
- **Knowledge gaps & expert questions** (moving ledger — what we still don't know + who to ask) → `KNOWLEDGE-GAPS-PROTOTYPE.md` (→ `KNOWLEDGE-GAPS.md` at go-live)

## Planned ingestions  (pushdown — newest intent first)  ‹DASH "Planned"›
| When | Source | Note |
|------|--------|------|
| next | Smart Pins (Titus) rev 5 | canonical staged at `sources/smart-pins-titus/` (rev5 .docx, 2026-03-31, **27 reviewer comments**). **Re-extraction** replaces the lossy *PDF*-scraped prior (`smart-pins-catalog/`). **Harvest the reviewer comments + inline editor notes as credible feedback** → technical Qs to KNOWLEDGE-GAPS. Role: cross-check for IOSP guide. |
| next | _(2nd source — TBD with user)_ | |
| **queued** | P1 datasheet + P1 manual (+ deSilva P1?) | bring P1 DB up to P2 richness; some partially ingested → complete + enrich |
| later | Quick Bytes | re-confirm intent — old "next 2-3 days" note was stale |

## Parked ideas to adjudicate (keep until proven meaningless)  ‹MATRIX›
- **Enrichment axis** — narrative / style-analysis / cross-source / central-hub-link. Tracked the 2025-09 central-analysis effort (stalled). Keep as drill-down column, fold, or drop?
- **Knowledge-domain coverage** — ✅ **un-parked** → now **Tier 2b** (by-topic lens) above.
- **Completeness% method** — two old guesses exist (DASH 75% vs MATRIX 85%, and per-source disagree). Re-derive from passes-done at verification; bracketed for now per your note.

---
_Categories above are the existing ones (preserved). Per-source cells fill in at step 4 (authoritative re-scan of each source). `INGESTION-DASHBOARD.md` + `INGESTION-AUDIT-MATRIX.md` remain live until this goes live._
