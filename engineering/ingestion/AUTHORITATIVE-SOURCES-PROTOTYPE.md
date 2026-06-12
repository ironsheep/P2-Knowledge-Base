# Authoritative Sources — Trust Catalog  ‹PROTOTYPE›

> **PROTOTYPE** — backing doc #1 of the ingestion quad (with the README dashboard + `DOCUMENT-LINEAGE` + `KNOWLEDGE-GAPS`).
> Replaces `AUTHORITATIVE-SOURCES.md` at go-live; kept side-by-side until then. The dashboard's **Auth** column
> derives from this catalog. **Existing trust mechanism adopted unchanged** — tiers are NOT being re-categorized.
> Per-source assignments are seeded from the current catalog and marked _(re-ground)_ for the research pass. _2026-06-11._

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
`pnut_ts` compiler (matched edition) → Silicon Doc → P2 datasheet / spec-sheet → instructions-CSV → community / cross-check,
with `chip-gracey-clarifications` the tiebreaker on flag & semantics. _(from `ingest-source` §4 corroboration matrix)_

## Per-source trust assignments  ‹seeded — re-ground in the research pass›
| Source | Tier | Origin / rationale | Edition |
|--------|------|--------------------|---------|
| silicon-doc | 🏆 | Chip Gracey — P2 architecture reference | v35 _(verify)_ |
| Spin2 Language Reference | 🏆 | Parallax/Chip — language spec; matched-compiler edition | v55 |
| pnut-ts-pasm-ref | 🏆 | matched compiler — ratified authority for PASM | _(verify)_ |
| chip-gracey-clarifications | 🏆 | direct from the chip designer | — |
| p2-datasheet · p2-spec-sheet | 🏆 | official Parallax hardware specs | _(verify)_ |
| Edge modules · eval board · add-on boards | 🏆 | official Parallax product guides | _(verify)_ |
| parallax-wx-wifi · p2-wx-adapter · propplug-rev-e · universal-motor-driver | 🏆 | official Parallax peripherals | _(verify)_ |
| p2-instructions-csv · p2-qa-spreadsheet | 🏆/🟢 | Parallax instruction data | _(verify)_ |
| PASM2 Manual (Parallax) | ⚠️ Draft/Partial | official but preliminary / not fully vetted | Nov-2022 |
| smart-pins | 🟢 | community-validated smart-pins documentation | _(verify)_ |
| Smart Pins (Titus) | 🟡 | community (Jon Titus), not Parallax — **cross-check** role | rev 5 |
| hyperRam-n-hyperFlash · iron-sheep-compiler | 🟢 | validated / Iron Sheep production | _(verify)_ |
| taqoz · quick-bytes-code · p2docs-github-io · marketing-materials | 🟡 | community / informal | _(verify)_ |
| p1-propeller-manual · p1-datasheet | 🏆 | official Parallax (P1) | _(verify)_ |
| desilva-p1-tutorial | 🟢 | community tutorial (P1) | _(verify)_ |

## Maintenance
Updated by `ingest-source` on each ingestion (new source → assign a tier; edition change → re-confirm). The dashboard's
Auth column reads tiers **from here** — manuals derive trust from this catalog, they don't re-tier. Genuine gaps (a source
with no assignment) are surfaced for the user, never invented.
