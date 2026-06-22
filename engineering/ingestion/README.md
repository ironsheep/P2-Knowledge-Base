# Ingestion — Status Dashboard

> The ingestion head's **front-door dashboard** (this folder's README). Multi-tier: glance → registry → drill-down.
> Carries the best ideas from every prior tracker (tags show provenance: ‹DASH›=INGESTION-DASHBOARD,
> ‹MATRIX›=INGESTION-AUDIT-MATRIX, ‹AUTH›=AUTHORITATIVE-SOURCES, ‹LIN›=DOCUMENT-LINEAGE, ‹SKILL›=ingest-source).
> Per-source cells **scanned 2026-06-12**. Registry grounded in `sources/` on disk. _Went live 2026-06-12 (was the quad prototype); folds the former INGESTION-DASHBOARD + INGESTION-AUDIT-MATRIX._

## Tier 1 — At a glance
- **Sources:** 38 folders on disk → **33 logical sources** · 30 P2 · **P1 now tracked separately** → `P1-INGESTION-DASHBOARD.md`  ‹+2 folders 2026-06-22: **p2-hardware-manual** (un-mis-filed from p2-eval-board → now a distinct logical source, +1) and **TAQOZ-Forth-Bitbashers-Guide** (the authoritative `.docx` for the existing `taqoz` logical source — folds in, not +1). v51a = lineage; code-analysis + marketing-materials = meta; pasm2-manual-development = dev scaffold›
- **By authority:** 🏆 23 · 🟢 6 · 🟡 4  ‹33 logical sources; p2-hardware-manual added 🏆; v51a lineage + 3 non-source folders excluded; hyperRam promoted 🟢→🏆 on ingestion›
- **Ingest completeness:** mature ~19 (≥90% + audit, **incl. Titus rev5 ✅, HyperRAM #64004-ES ✅**) · partial ~8 (40–89%) · minimal/not-started ~5  ‹scanned 2026-06-12; HyperRAM ingested 2026-06-22›
- **Open questions:** **9** in the gap ledger (G-001..008 Smart-Pins/Titus + **G-009** 64004-ES part-numbers) · **3** routed to an expert (Q-001..003)  ‹rolled up from KNOWLEDGE-GAPS›
- **Latest ingested:** **P2 Eval Add-on Boards (#64006)** — cross-edition re-ingestion (2026-06-22, 🏆; **fabrication rescue** + 8 per-board source docs) · prior: HyperRAM/HyperFlash #64004-ES (2026-06-22, 🏆) ‹LIN›
- **What's next:** **silicon-doc re-extraction from the `.docx`** — clean image catalog (Titus-style) + modern re-validation; `.docx` now staged in `sources/silicon-doc/` (v35 Rev B/C). _Then: **F-122** → YAML head authors the 64004-ES standalone board YAML from the new extraction (part-numbers G-009 to verify first)._  ‹HyperRAM #64004-ES ✅ 2026-06-22 · Titus rev5 ✅/DETUNED · YAML v1.10.1 ✅ 2026-06-20›
- **Why track this:** qualified inputs feed the YAML KB → **download-on-demand (MCP)** → agents writing P1/P2 code their models were never trained on. Input trust + completeness propagate straight to agent reliability.

## Tier 2 — Source registry (by category — categories preserved from existing trackers)

> **Rows = logical sources at their CURRENT edition** (not raw folders). A version update *replaces* the prior doc as authority; prior editions are lineage in `DOCUMENT-LINEAGE`, not separate rows — two sub-cases: **augmentative** (newer edition, content grew, keep prior) vs **re-extraction** (prior was lossy, discard it). **Role** ≠ authority: a source is *primary* (derive content) or *cross-check* (corroborate/hint).
Cells: ✅ done · ◐ partial · ⏳ pending · — n/a · ? verify  |  Passes ‹SKILL 7-pass›: **C** content · **K** code · **I** images · **A** audit/validated · **X** cross-source (pass 6 — connected/corroborated vs other sources)  |  Auth: 🏆 authoritative · 🟢 green · 🟡 yellow · ◳ draft

### P2 · Core language & architecture  ‹AUTH "Core Technical"›
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| silicon-doc | 🏆 | ✅ | ✅ | ◐ | ✅ | ✅ | 75% _(stated; arch 100%, some sections 90%; **docx re-extraction SCHEDULED 2026-06-22** — `.docx` in `external-inputs/p2/`; 2025-08 docx text-extract measured +48 tables/607 sections over PDF; clean image catalog never built — redo for the Titus-style image win + modern re-validation)_ |
| **Spin2 Language Reference** @ v55 ‹prior v51a — lineage, augmentative› | 🏆 | ✅ | ✅ | ✅ | ✅ | ⏳ | 100% _(delta v52→v55; X pending. v51a lineage fully extracted)_ |
| p2-instructions-csv | 🏆 | ✅ | — | — | ✅ | ⏳ | 100% _(audit: pasm2-spreadsheet-audit.md — aliased)_ |
| chip-gracey-clarifications | 🏆 | ✅ | — | — | ⏳ | ⏳ | ? _(structured text; no audit / cross-source doc)_ |
| p2-qa-spreadsheet | 🟢 | ✅ | — | — | ✅ | ⏳ | ~80% _(991 rows; audit present; no cross-source)_ |
| **PASM2 Manual** (Parallax, preliminary) | 🏆 | ✅ | ◐ | ◐ | ✅ | ✅ | 64% _(stated; code embedded in docx md, not a validated catalog; **superseded** as the PASM2 reference by our Assembly manual)_ |

### P2 · Smart Pins
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| smart-pins | 🟢 | ✅ | ✅ | ✅ | ✅ | ✅ | 97% _(stated; 174 examples, 21 mode images)_ |
| **Smart Pins (Titus)** @ rev 5 ‹re-ingest DONE 2026-06-12; old PDF extraction archived› | 🟡 **cross-check** | ✅ | ✅ | ✅ | ✅ | ✅ | ~90% _(32/32 modes; 28/30 code pnut-ts-validated; 21 figures extracted CLEAN + catalogued (4 deep-OCR'd, 17 waveform-label OCR debt = **WON'T-DO**); 27 reviewer comments harvested; #21 WRPIN selector error confirmed vs silicon-doc; 0 corrections, 8 gaps + 3 expert-Qs logged)_ · **DETUNED 2026-06-22** — superseded by IOSP manual (own generated figures); no further Titus-source investment; gaps G-001..008 still feed YAML/expert as normal |

### P2 · Hardware ecosystem  ‹distinct top-level category — boards/add-ons/datasheets, NOT software/compilers›
_Boards share a 12-pin header (8 I/O + power/ground); ×8 headers = all 64 pins. Add-on boards ride one header or a header pair._

**Datasheets & specs (PDF)**  ‹AUTH "Core Technical" → re-filed as hardware›
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| p2-datasheet | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 94% _(stated; audit: datasheet-audit-report.md — aliased)_ |
| p2-spec-sheet | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | 99% _(stated; audit: spec-sheet-audit-report.md — aliased; no images/cross-source)_ |
| **p2-hardware-manual** ‹P2X8C4M64P Hardware Manual, Nov-2022; folder created 2026-06-22 — artifacts relocated from `extraction-matrices/` + `p2-eval-board/` (was mis-filed)› | 🏆 | ✅ | ⏳ | ⏳ | ✅ | ⏳ | ~65% _(prior effort 2025-08-15: 3026 paras / 53 tables / 2144 sections + audit; **no images**; **newer `.docx` staged → re-ingestion pending** (silicon-doc-style refresh))_ |

**Development boards (12-pin header system)**  ‹AUTH "Hardware Boards"›
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| p2-eval-board ‹Rev C — retired / left behind› | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 100% _(stated)_ |
| edge-standard-module | 🏆 | ✅ | — | ✅ | ⏳ | ✅ | ~80% _(missing audit doc — only row with X but no A)_ |
| edge-32mb-module | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 100% _(stated)_ |
| edge-breakout-board | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 100% _(stated; 18 images)_ |
| edge-mini-breakout | 🏆 | ✅ | — | ⏳ | ✅ | ✅ | 100% _(stated; no images extracted)_ |
| edge-module-breadboard | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 100% _(stated; 20 images — most complete board)_ |

**Add-on boards (ride on headers)**  ‹AUTH "Add-On Modules"›
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| p2-eval-add-on-boards ‹#64006 series — 8 boards A–H + set SKU› | 🏆 | ✅ | — | ✅ | ✅ | ✅ | ~98% _(**re-ingested cross-edition 2026-06-22** — prior extraction was **FABRICATED** (invented board lineup); now **8 per-board source docs** in `boards/` + overview + **17-image catalog** (photos corroborate pin maps; PCB-dimension drawings); 2025 clean + 2020 `#64006-ES` forced-OCR, pin maps cross-validated. **F-121** → YAML head rebuilds `addon-*.yaml`)_ |
| universal-motor-driver | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | ~85% _(raw txt; no images/cross-source)_ |
| hyperRam-n-hyperFlash | 🏆 | ✅ | — | ✅ | ✅ | ✅ | 95% _(**ingested 2026-06-22**, forced-OCR — PDF text layer corrupt; pin map **triple-validated** (text∩OCR∩drawing); no code in source; 7 images. Standalone YAML pending → **F-122** (yaml head); part-numbers OCR-unverified → **G-009**)_ |

**Adapters & connectivity**
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| parallax-wx-wifi | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | ~90% _(stated; 12+ images flagged as debt)_ |
| p2-wx-adapter | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | ~90% _(stated; 8+ images flagged as debt)_ |
| propplug-rev-e | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | ~95% _(stated; no images)_ |

### P2 · Boot & loaders
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| rom-booter | 🟢 | ✅ | ✅ | — | ⏳ | ⏳ | ~40% _(.lst assembly; no audit / cross-source)_ |
| flash-loader | 🟢 | ✅ | ✅ | — | ⏳ | ⏳ | ~50% _(.spin2 source; no audit / cross-source)_ |

### P2 · Compiler & tooling  ‹proposed bucket — veto anytime›
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| pnut-ts-pasm-ref | 🏆 | ✅ | ✅ | — | ◐ | ⏳ | 95% _(stated; 359-instr JSON DB; audit material in audit/ subfolder — needs a consolidated rollup doc, 5B)_ |
| iron-sheep-compiler | 🟢 | ◐ | — | — | ⏳ | ⏳ | ~15% _(single condition-codes doc only)_ |

### P2 · Community code & tutorials  ‹proposed›
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| taqoz | 🟡→🏆 | ◐ | — | — | ⏳ | ⏳ | ~25% _(preliminary web research only, unverified) — **authoritative `.docx` now staged:** `sources/TAQOZ-Forth-Bitbashers-Guide/` ("The Bit Bashers Guide to the Parallax P2 — Using TAQOZ ROM Forth"). Future effort ingests it as the **primary** (upgrades 🟡→🏆), grounding F-123 and reconciling this preliminary row. (Prior PDF in `external-inputs/p2/quarantine/`.)_ |
| quick-bytes-code | 🟡 | ⏳ | ◐ | — | ⏳ | ⏳ | ~15% _(one .spin2; zips unextracted; no narrative)_ |

### P2 · Other reference  ‹proposed›
| Source | Auth | C | K | I | A | X | Cmpl* |
|--------|------|---|---|---|---|---|-------|
| p2docs-github-io | 🟡 | ◐ | — | — | ⏳ | ⏳ | ~30% _(narrative + validation report only)_ |

### P1 · (separate corpus — bootstrap in progress 2026-06-22)  ‹DASH "P1 Sources"›
_P1 = first Propeller. The P1 corpus now has its **own dashboard + quad** (namespaced `G-P1-/Q-P1-/F-P1-`), stood up by the P1 bootstrap — it is **no longer tracked inline here.**_
**→ `P1-INGESTION-DASHBOARD.md`** (registry) · `P1-AUTHORITATIVE-SOURCES.md` · `P1-DOCUMENT-LINEAGE.md` · `P1-KNOWLEDGE-GAPS.md` · `operations/P1-CORRECTION-FINDINGS.md`. Bootstrap design: `plans/P1-KB-BOOTSTRAP-CHARTER.md` · source list: `plans/p1-sources-ingestion-plan.md` · KB target: `deliverables/ai/P1/`.

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
| ✅ done 2026-06-12 · **DETUNED 2026-06-22** | Smart Pins (Titus) rev 5 | **Re-extraction COMPLETE** (certification run for the updated skill). 32/32 modes; 28/30 code pnut-ts-validated; 21 figures extracted clean + catalogued; **27 reviewer comments harvested** → 8 gaps (G-001..008) + 3 expert-Qs (Q-001..003) in KNOWLEDGE-GAPS; **#21 WRPIN x101/x111 selector swap CONFIRMED** vs silicon-doc (Titus errata, 0 corrections). Prior PDF extraction archived (§0.6). **DETUNED** — superseded by the IOSP "Blue Book" manual (its own generated figures replace Titus's); no further Titus-source work (17-figure OCR-label debt = WON'T-DO). Stays 🟡 cross-check; G-001..008 still feed YAML/expert. |
| ✅ done 2026-06-22 | 64004-ES HyperRAM/HyperFlash Memory Board (Parallax #64004-ES) | **INGESTION COMPLETE** (95%; first PDF-only-ladder run). Forced-OCR (corrupt PDF text layer); pin map triple-validated (text∩OCR∩drawing); no code in source; 7 images cataloged. **F-122 handed to YAML head** (author `hardware/addon-hyperram-hyperflash.yaml` from `sources/hyperRam-n-hyperFlash/complete-hyperram-hyperflash-reference.md`); **G-009** logged (part-numbers OCR-unverified). Skill gained the corrupt-text-layer→force-OCR refinement. |
| **next** ‹scheduled 2026-06-22› | silicon-doc — **re-extraction from the `.docx`** (v35 Rev B/C) | `.docx` confirmed: `external-inputs/p2/Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx`. Prior 2025-08 docx text-extract (`sources/silicon-doc/silicon-from-docx.md`) already measured the win (**607 sections, 48 tables** vs PDF/text) but the **clean image catalog was never built** (the 2025-09 `IMAGE-ENHANCEMENT-PLAN`, never executed). Redo via the modern DOCX-primary `ingest-source` path: lossless `word/media/*` image extraction + `image-tools-mcp` catalog (Titus-style) + pnut_ts code re-validation + refreshed audit. **Crown-jewel source — highest downstream leverage; sequence after HyperRAM.** |
| **queued** ‹2026-06-22› | **p2-hardware-manual** refresh (P2X8C4M64P Hardware Manual, Nov-2022) | Source folder stood up 2026-06-22; prior 2025-08-15 effort's artifacts relocated in (extraction + audit + methodology). **Newer `.docx` staged** in the folder (differs from the `external-inputs/p2/` copy). Re-ingest DOCX-primary (`ingest-source`) to refresh content + **add the missing image catalog** + pnut_ts code pass + cross-source. _Note: `external-inputs/p2/` holds an older export — reconcile which is canonical at ingestion._ |
| **queued** ‹2026-06-22› | **TAQOZ — "The Bit Bashers Guide to the Parallax P2 (Using TAQOZ ROM Forth)"** | Authoritative `.docx` staged `sources/TAQOZ-Forth-Bitbashers-Guide/`. Ingest as the **primary** TAQOZ source (upgrades the preliminary web-research `taqoz/` row 🟡→🏆); **grounds F-123** (TAQOZ/ROM-Monitor capability detail currently rests on web research). Reconcile with the existing `taqoz/` folder + the quarantined PDF at ingestion. Code-heavy (Forth) — expect a substantial code-extraction pass. |
| ✅ done 2026-06-22 | #64006 P2 Eval Add-on Boards — **cross-edition** (Aug-2020 `#64006-ES` + Aug-2025 `#64006`) | **CROSS-EDITION RE-INGESTION COMPLETE.** Discovered the prior extraction **fabricated the entire board lineup**; rebuilt from both editions (2025 clean + 2020 forced-OCR — 2nd corrupt-text-layer case). **8 per-board source docs** in `boards/addon-*.md` + overview; pin maps cross-validated. Fabricated files stubbed-in-place (git history retains). **F-121 updated** → YAML head rebuilds `hardware/addon-*.yaml` to the 8 real boards + drops the 4 non-#64006 orphans. |
| **queued** | P1 datasheet + P1 manual (+ deSilva P1?) | bring P1 DB up to P2 richness; some partially ingested → complete + enrich |
| later | Quick Bytes | plan: `plans/QUICK-BYTES-READY-TO-EXECUTE.md`; scraper tools ready (`scrape-quick-bytes.py`, `extract-tag-taxonomy.py`, `youtube-playlist-correlator.py`); re-confirm intent (old "next 2-3 days" note stale) |

## Parked ideas to adjudicate (keep until proven meaningless)  ‹MATRIX›
- **Enrichment axis** — narrative / style-analysis / cross-source / central-hub-link. Tracked the 2025-09 central-analysis effort (stalled). Keep as drill-down column, fold, or drop?
- **Knowledge-domain coverage** — ✅ **un-parked** → now **Tier 2b** (by-topic lens) above.
- **Completeness% method** — two old guesses exist (DASH 75% vs MATRIX 85%, and per-source disagree). Re-derive from passes-done at verification; bracketed for now per your note.
- **Style / voice analysis** (per-source 4-level style profile; 2/24 done in the old matrix) — **OPEN / deferred** (2026-06-12). Likely *manual-head* metadata, not an ingestion pass. Carried-not-dropped; revisit when ready.
- **Pipeline deliverables** (P2 Bytecode Spec, Terminal Window Manual, Hardware Interface Guide, Binary Decoder Tool — from old DOCUMENT-LINEAGE) — **OPEN / deferred** (2026-06-12): still planned or stale? Parked in DOCUMENT-LINEAGE 'planned outputs' until confirmed.

---
_Per-source cells **scanned 2026-06-12** (read-only fan-out over all 36 folders). **Normalization findings (for go-live / verification fill):** (1) ✅ **audit-filename drift — RESOLVED (aliased):** actual audit filenames recorded in the rows; canonical `<src>-complete-extraction-audit.md` applies to new ingestions. `pnut-ts-pasm-ref` still needs a *consolidated* rollup audit (5B). (2) ✅ **Non-sources demoted:** `code-analysis` + `marketing-materials` (meta) and `pasm2-manual-development` (dev scaffold) moved out of the registry → see 'Not standalone sources'. Physical archive/relocate deferred to cleanup. (3) **Image debt** is the most common gap (most hardware rows + the P1 docs have no images extracted). (4) **Zero/un-ingested:** `hyperRam-n-hyperFlash` (raw CAD + **Product Guide PDF staged 2026-06-13** → queued as next ingestion); `smart-pins-titus` **ingested ✅ 2026-06-12** (first full quad-update + reviewer-harvest run). **Cross-source (X)** is absent on ~20 sources — the bulk of the verification fill. folds the former `INGESTION-DASHBOARD` + `INGESTION-AUDIT-MATRIX` (archived 2026-06-12)._
