# Authoritative Sources — Trust Catalog

> Backing doc #1 of the ingestion quad (with the README dashboard + `DOCUMENT-LINEAGE` + `KNOWLEDGE-GAPS`).
> The dashboard's **Auth** column derives from this catalog. **Existing trust mechanism adopted unchanged** —
> tiers are not re-categorized. Per-source assignments marked _(re-ground)_ are confirmed during the verification pass. _Live 2026-06-12._

## Source-ID scheme  ‹decision: folder slug = canonical ID›
The **`sources/<slug>/` folder name IS the canonical source ID** (e.g. `silicon-doc`, `smart-pins-titus`,
`spin2-v55`). Reference a source anywhere as the grep-sigil **`src:<slug>`**. The **edition** (v51a, rev 5, …)
is a *field*, never part of the ID — except frozen lineage editions, which each keep their own version-suffixed
folder (`spin2-v51` prior, `spin2-v55` current). Where a doc has been called other names, list the **aliases**
so lookups resolve. Genuine gaps (a source with no ID/tier) are surfaced, never invented.

| Canonical ID (slug) | Aliases / former names |
|---------------------|------------------------|
| `spin2-v55` | `spin2_lang_ref_v55` *(renamed 2026-06-12)* · "Spin2 Language Reference v55" |
| `spin2-v51` | spin2-v51a · "Spin2 Documentation v51" |
| `smart-pins-titus` | "Smart Pins (Titus)" · SPTutTItus · "Smart Pins rev 5" |
| `smart-pins` | "P2 SmartPins" · smart-pins community doc |
| `hardware-verification` | "empirical evidence" · "hardware tests" · `external-sources/hardware-verification` |
| `p2-hub75-adapter` | #64032 · "P2 Eval HUB75 Adapter Board" · "HUB75 adapter" · "RGB LED matrix adapter" · "LED panel interface" *(folder created 2026-08-26 from two loose captures in `sources/`)* |
| _…seed the rest during the research pass…_ | |

## Trust tiers (existing mechanism — adopted as-is)
| Tier | Meaning | How to use |
|------|---------|-----------|
| 🏆 Authoritative | Official Parallax / chip designer | cite without verification; wins conflicts |
| 🟢 Green | Community-validated, cross-verified, tested | trusted; light verification |
| 🟡 Yellow | Community / unverified | corroborate before use (cross-check role) |
| 🔴 Red | Contradicted / P1-applied-to-P2 / untrusted | do not use |
| ⚠️ Draft/Partial | Official but incomplete / not fully vetted | trusted on what it covers; flag the gaps |

## Conflict-resolution precedence (authority order)
**hardware-verification** (a clean run on real P2 silicon — empirical ground truth; see `external-sources/hardware-verification/`) → `pnut_ts` compiler (matched edition) → Silicon Doc → P2 datasheet / spec-sheet → instructions-CSV → community / cross-check,
with `chip-gracey-clarifications` the tiebreaker on flag & semantics. _(from `ingest-source` §4 corroboration matrix)_

## Per-source trust assignments  ‹seeded — re-ground in the research pass›
| Source | Tier | Origin / rationale | Edition |
|--------|------|--------------------|---------|
| silicon-doc | 🏆 | Chip Gracey — P2 architecture reference | **v35 (Rev B/C silicon), CONFIRMED 2026-08-26** — re-extracted DOCX-primary from `Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx`; edition read off the document itself (`v35 (Rev B/C silicon)`, `P2X8C4M64PES`, `LPD1941 (Rev B) or LHU2019 (Rev C)`, dated 2021-05-18). Tier unchanged at 🏆 and now better earned: 48/48 tables recovered where the prior capture had none. **One qualification worth carrying:** the document is not self-consistent everywhere — E-012, E-013 and E-014 are self-contradictions or omissions found in this edition, and E-015 is a section the designer himself says is incomplete. 🏆 means highest available authority, not inerrant. |
| hardware-verification | 🏆 | **empirical** — the chip's own behavior, proven by test (`external-sources/hardware-verification/`) | running ledger |
| Spin2 Language Reference | 🏆 | Parallax/Chip — language spec; matched-compiler edition | v55 |
| pnut-ts-pasm-ref | 🏆 | matched compiler — ratified authority for PASM | _(verify)_ |
| chip-gracey-clarifications | 🏆 | direct from the chip designer | — |
| p2-datasheet · p2-spec-sheet | 🏆 | official Parallax hardware specs | _(verify)_ |
| p2-hardware-manual | 🏆 | official Parallax — **P2X8C4M64P Hardware Manual** (release, not draft). Core hardware reference. **Re-ingested DOCX-primary 2026-08-24** (7 passes; tier re-confirmed 🏆 — release document, matching edition, no conflicts against it). Carries clean table structure for four tables the **p2-datasheet** PDF lost, so it is the datasheet's **cross-check partner** for electrical/pin-mode facts. **Aliases:** Hardware Manual, P2X8C4M64P, P2 hardware reference. | Nov-2022 |
| Edge modules · eval board · add-on boards | 🏆 | official Parallax product guides | _(verify)_ |
| HyperRAM/HyperFlash Add-on (#64004-ES) | 🏆 | official Parallax product guide (board Rev A, Open Source Hardware CC BY-SA 4.0). Ingested 2026-06-22 via forced OCR (corrupt PDF text layer); pin map triple-validated. **Aliases:** 64004-ES, HyperRAM, HyperFlash, HyperBUS, hyper memory add-on. | Guide v1.0 (2019) |
| p2-click-adapter (#64008) | 🏆 | official Parallax **schematic**, Rev A 2020-08-10, **Open Source Hardware CC BY-SA 4.0**. **Given its own row rather than folded into "add-on boards" because its provenance is unusual: there is NO user guide for this board** — the schematic plus the MikroElektronika mikroBUS standard are the complete documentation set. Ingested 2026-08-26 by **rendered-page visual read**; the sheet is vector art with its text converted to curves, so no text-extraction path can work on it (proven by negative control: 0 occurrences of every net and refdes token). All 12 pin offsets confirmed, 0 corrections. **Limit of this tier:** it is authoritative for the P2-side wiring only — Click-side signal MEANINGS come from the mikroBUS standard, which this repo does not hold (→ G-022). | Rev A (2020-08-10) |
| p2-hub75-adapter (#64032) | 🟢 | **Iron Sheep Productions, LLC — the board's manufacturer**, not Parallax (the board is sold through the Parallax store, retiring / limited stock), so it fails the 🏆 admission test's *official Parallax* clause however good the data is. **Given its own row rather than folded into "add-on boards" because, like #64008, its provenance is unusual: no vendor primary document is staged and none is known to exist** — the board has no Parallax datasheet or user guide, and the folder holds three **authored captures**, not an extraction of a document: `p2-hub75-adapter-official-specs.md` (physical/electrical specs, A-B-C / A-B-C-D / A-B-C-D-E address-line support, panel power table, refresh figures), `p2-hub75-adapter-complete-pinout.md` (the base-pin + offset HUB75 signal map, io+0..io+13) and `p2-hub75-adapter-preliminary-knowledge.md`, which labels its own contents *"Known Specifications (To Be Confirmed)"* and is **⚠️ Draft/Partial — corroborate before use**. Folder created 2026-08-26 from two loose captures that had been sitting in `sources/` root (captures committed 2025-09-05). Feeds `deliverables/ai/P2/hardware/hub75_adapter.yaml`, which already cites these files by `path:line`. **Aliases:** 64032, HUB75 adapter, HUB75 Adapter Board, P2 Eval HUB75 Adapter, RGB LED matrix adapter, LED panel interface. | board in production _(verify — no document edition to cite)_ |
| rom-booter · flash-loader | 🟢 | **P2 boot code itself** — `ROM_Booter.lst` / `rom_booter_v33_01j.lst` assembly listings and `flash_loader.spin2`. A distinct trust category from documentary sources: this is **what the silicon actually runs**, so on boot behaviour it outranks prose that describes it — which is why E-014 (the Silicon Doc omits microSD boot) resolves against the Silicon Doc and not against these. 🟢 rather than 🏆 because neither has had an audit or cross-source pass; the artifacts are trustworthy, our *reading* of them is not yet verified. | ROM v33/01j |
| parallax-wx-wifi (#32420) · p2-wx-adapter (#64007) · propplug-rev-e (#32201) · p2-universal-motor-driver (#64010) | 🏆 | official Parallax peripherals (WX/adapter/motor-driver **re-extracted 2026-06-27**; **Prop Plug Rev E re-extracted 2026-06-29**, addon-wave-2026-06; prior captures archived §0.6). **Aliases:** WX ESP8266 Wi-Fi module, P2-WX adapter, Universal Motor Driver RevB, **Prop Plug, PropPlug, FTDI FT231X programming adapter, USB-to-serial programmer**. | guides v1.0 / RevB v2.0 / Prop Plug doc v3.0 (Rev E) |
| p2-microSD-addon (#64009) · P2-RTC-Add-on (#64013) · P2-HD-Audio-Add-on (#64014) | 🏆 | official Parallax add-on board guides — **ingested 2026-06-27** (addon-wave-2026-06). **Aliases:** P2 microSD Add-on/Accessory; P2 RTC Add-on (NXP PCF8523); P2 HD Audio Add-on Set (AKM AK5704EN codec). | guides 2022 |
| AK5704 datasheet (companion to #64014) | 🟡 | AKM component datasheet — **cross-check only**: corroborates the #64014 HD-Audio codec facts (11/11 confirmed, 0 conflicts); never promoted as a P2 fact authority. | AK5704EN (EN) |
| p2-instructions-csv · p2-qa-spreadsheet | 🏆/🟢 | Parallax instruction data | _(verify)_ |
| PASM2 Manual (Parallax) | ⚠️ Draft/Partial | official but preliminary / not fully vetted | Nov-2022 |
| smart-pins | 🟢 | community-validated smart-pins documentation | _(verify)_ |
| Smart Pins (Titus) | 🟡 | community (Jon Titus), not Parallax — **cross-check** role. Ingested rev5 2026-06-12: corroborates the mode taxonomy, but a WRPIN bit-field table here was **demonstrably wrong** (x101/x111 swapped vs silicon-doc, caught in peer review #21) — **never an encoding/bit-field authority**; use for technique/app-note color only. | rev 5 |
| iron-sheep-compiler | 🟢 | validated / Iron Sheep production | _(verify)_ |
| taqoz · quick-bytes-code · p2docs-github-io · marketing-materials | 🟡 | community / informal | _(verify)_ |
| p1-propeller-manual · p1-datasheet | 🏆 | official Parallax (P1) | _(verify)_ |
| desilva-p1-tutorial | 🟢 | community tutorial (P1) | _(verify)_ |

## Hardware part numbers  ‹Parallax board SKUs — carried from old AUTHORITATIVE-SOURCES›
| Board (source) | Part # |
|----------------|--------|
| p2-eval-board (Rev C) | #64000 |
| edge-standard-module | #64000-ES |
| edge-32mb-module | #64000-32MB |
| edge-module-breadboard | #64020 |
| edge-breakout-board | #64029 |
| edge-mini-breakout | #64019 |
| p2-wx-adapter | #64007 |
| p2-microSD-addon | #64009 |
| p2-universal-motor-driver | #64010 |
| P2-RTC-Add-on | #64013 |
| P2-HD-Audio-Add-on | #64014 |
| p2-hub75-adapter | #64032 |
| parallax-wx-wifi | #32420 |

## Admission & usage  ‹carried from old AUTHORITATIVE-SOURCES›
**Authoritative-tier admission criteria** (all four required): (1) official Parallax documentation; (2) current/production version; (3) covers P2 (not P1) specs; (4) complete (not draft/partial). *A draft/partial official doc gets ⚠ Draft, not 🏆.*

**Usage (AI consumers + developers):** treat 🏆 Authoritative as ground truth — cite without qualification, no cross-verification, conflicts resolve in its favor, generate code confidently. 🟢 Green = trusted, light verification. 🟡 Yellow = corroborate before use. All derived docs must align with Authoritative sources.

## Maintenance
Updated by `ingest-source` on each ingestion (new source → assign a tier; edition change → re-confirm). The dashboard's
Auth column reads tiers **from here** — manuals derive trust from this catalog, they don't re-tier. Genuine gaps (a source
with no assignment) are surfaced for the user, never invented.
