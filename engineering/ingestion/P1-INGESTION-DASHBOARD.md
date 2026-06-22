# P1 Ingestion — Status Dashboard

> The **P1 (Propeller 1)** ingestion registry — standalone, parallel to the P2 dashboard (`README.md`).
> Stood up 2026-06-22 by the P1 bootstrap (`plans/P1-KB-BOOTSTRAP-CHARTER.md`). Source list:
> `plans/p1-sources-ingestion-plan.md`. P1 registers are namespaced (`G-P1-/Q-P1-/F-P1-`) — see the P1 quad:
> `P1-AUTHORITATIVE-SOURCES.md` · `P1-DOCUMENT-LINEAGE.md` · `P1-KNOWLEDGE-GAPS.md` · (corrections → `operations/P1-CORRECTION-FINDINGS.md`).

## Tier 1 — At a glance
- **Logical sources:** 8 rows (incl. the App Notes collection = 17 docs) · all P1.
- **By authority:** 🏆 7 · 🟢 1 (deSilva).
- **Bootstrap phase:** **scaffolding built**; next = **backbone solo** (re-extract the P1 Propeller Manual), then **wave the tail**.
- **Validator:** flexspin (community-tier) — **pending install**; P1 code is documentary-extracted, marked not-yet-validated until then (charter §3).
- **What's next:** ingest the **P1 Propeller Manual v1.2** (re-extraction, fold the errata as correction cross-check) — it seeds the P1 gap ledger.

## Registry  (passes: **C** content · **K** code · **I** images · **A** audit · **X** cross-source · 🏆/🟢 auth)
| Source | Auth | C | K | I | A | X | Cmpl* | Mode for the campaign |
|--------|------|---|---|---|---|---|-------|------------------------|
| p1-propeller-manual-v1.2 | 🏆 | ◐ | ⏳ | ⏳ | ◐ | ⏳ | ~60% _(803KB text + audit; old-tooling; no images)_ | **re-extraction (backbone, solo first)** |
| p1-propeller-manual-errata-v1.1 | 🏆 | ⏳ | — | ⏳ | ⏳ | ⏳ | 0% _(correction layer — outranks base Manual on corrected points)_ | new (with the backbone) |
| p1-datasheet-v1.4 | 🏆 | ✅ | — | ⏳ | ✅ | ⏳ | ~100% text _(no images)_ | completion (images/cross-source) |
| desilva-p1-tutorial | 🟢 | ✅ | ◐ | ⏳ | ⏳ | ⏳ | ~45% _(text + voice-analysis; no audit)_ | completion |
| p1-pe-labs-fundamentals-v1.2 | 🏆 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | 0% | new (wave) |
| p1-xbee-tutorial-v1.0.1 | 🏆 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | 0% | new (wave) |
| p1-xbee-tutorial-errata-v1.0 | 🏆 | ⏳ | — | ⏳ | ⏳ | ⏳ | 0% _(correction layer for the XBee tutorial)_ | new (wave) |
| p1-application-notes ‹AN001–015, 018, 019 · **17 docs**; AN016/017 never published› | 🏆 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | 0% _(each AN is an independent source → fans out 17-wide in the wave)_ | new (wave) |

*\*Cmpl = completeness estimate; bracketed until re-derived at validation.*

## Bootstrap exceptions in force (charter §6)
- **Doc #1 (the Manual) only *raises* questions** — empty "answered-prior" leg is expected, not a defect.
- **Every P1 pass-6 carries the required P1→P2 cross-corpus leg** (how does this relate to / differ from its P2 analog) → `P1-DOCUMENT-LINEAGE.md` edges + `central-analysis/p1-p2-comparison/`.
