# Document Production Pipeline

*Status synced to PUBLICATION-ROSTER 2026-06-12. The roster is the **source of truth** for
publication state; this README mirrors its current snapshot. (The sections below the publications
table still carry the older "shape" and await a separate refresh.)*

> **Authoritative roster → [`PUBLICATION-ROSTER.md`](PUBLICATION-ROSTER.md)** — every manual-shaped
> folder is categorized there exactly once (live / in-dev / instrument / orphaned), with the full
> per-gate pipeline. The table below is a glance; the roster is the detail.

## Production States

| State | Symbol | Description |
|-------|--------|-------------|
| Planned | 🔴 | Identified need, not started |
| Content Ready | 🟡 | Source material available |
| In Production | 🟢 | Actively being generated |
| Released | ✅ | Published and available |
| Deferred | ⏸️ | Valid but not current priority |

## Live publications (synced to roster)

| Publication | Slug | State |
|-------------|------|-------|
| P2 Assembly Language Reference | `p2-assembly-language-manual` | ✅ **Released v3.1.1** (503pp, 2026-06-29) — Ch.1 execution-model refinements + §1.4.4 streamer + CMP Operation: line; uppercase mnemonics in prose; chip review outstanding (external) |
| DeSilva PASM2 Tutorial | `p2-pasm-desilva-style` | ✅ **Released v3.0.1** (162pp, 2026-06-25) — accuracy re-audit (all examples pnut-ts-certified) + Plex typography refresh + example-library ZIP; both prior deferrals resolved; chip review outstanding |
| AI Privacy Guide | `ai-privacy-guide` | ✅ **Released** — both reviews complete; presentation-class |
| P2 I/O & Smart Pins User Guide | `p2-io-and-smart-pins-user-guide` | ✅ **v1.0.0** (396pp) released 2026-07-03 — maiden Community Review Edition; cross-ref filter pilot; 15-program example ZIP ("Blue Book") |
| P2 Single-Step Debugger Manual | `p2-single-step-debugger-manual` | 🟢 draft, platform stack; **cover repaired 2026-06-12**; in technical review (chip + community) |
| P2 Streamer Programming Guide | `p2-streamer-programming-guide` | ✅ **v1.0.3 released 2026-07-03** (75pp); Wave-3 designer-authoritative additions (SINC2 constant-iteration constraint, HDMI/DVI blanking guidance, capture-to-spectrum pointer) + cross-ref filter adopted; chip review outstanding |
| P2 Debug Window Manual | `p2-debug-window-manual` | ✅ **v1.0.1 released 2026-06-26** (community review, 156pp); accuracy + typography refresh; 32-demo example library bundled |

## In development / parked · Instruments · Orphaned (see roster for detail)

| Publication | Slug | Category |
|-------------|------|----------|
| Spin2 Reference Manual | `spin2-reference-manual` | in development / parked |
| P2 XBYTE Programming Guide | `p2-xbyte-programming-guide` | in development (v0.1.0 first draft) |
| The P2 Architect's Guide | `p2-architect-guide` | in development (split in progress) |
| P2 Layout Torture Test | `p2-layout-torture-test` | instrument (serves the layout-standards effort) |
| Smart Pins Tutorial ("Green Book") | `p2-smart-pins-tutorial` | orphaned — superseded by the I/O & Smart Pins guide |

## Application Notes (`P2ANxxx`) — synced to roster

A distinct document class (see [`app-notes/README.md`](app-notes/README.md)). Candidate
backlog + production plan: [`p2-app-note-roster.md`](../analysis/p2-app-note-roster.md).
In production:

| App note | Slug | State |
|----------|------|-------|
| P2AN001 — Single-Pin ADC Instrumentation | `P2AN001` | ✅ **v1.0.1 released 2026-07-03** (20pp) — exemplar + companion-schema pilot (Family A0); ships YAML companion + example ZIP |
| P2AN002 — CORDIC for Real Work | `P2AN002` | ✅ **v1.0.0 released 2026-07-03** (14pp) — Math family lead (B1); 6 recipes + FOC ceiling; ships YAML companion + example ZIP |
| P2AN003 — DAC & Analog Signal Generation | `P2AN003` | ✅ **v1.0.0 released 2026-07-03** (19pp) — Family A1 (output sibling to ADC); techniques-catalog (5 recipes + reSound ceiling); ships YAML companion + example ZIP |
| P2AN004 — Frequency / Period / Pulse Measurement | `P2AN004` | 🔴 planned (Family A2) — IOSP Release Campaign Input 3 |

## Template Architecture

### Layer Stack
```
Foundation → Content Type → Presentation Style
p2kb-foundation → [reference/tutorial/user-guide] → [draft/tech-review/official]
```

### Document-Template Matrix

| Type | Content Layer | Presentation Flow |
|------|--------------|-------------------|
| Reference Manual | reference-manual | tech-review → official |
| Tutorial | tutorial-manual | tech-review |
| User Guide | user-guide | draft → tech-review |

## Visual Assets

| Source | Available | Status |
|--------|-----------|--------|
| P2 Edge Ecosystem | 60 images | ✅ Complete |
| Smart Pins | 21 images | ✅ Complete |
| Spin2 v51 | 24 images | ✅ Complete |
| Silicon Doc | 34 images | ✅ Complete |
| **Total Available** | **139 images** | Ready for use |

## Production Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Template Reliability | 100% | ✅ Achieved |
| Production Speed | <1 day | ✅ Achieved |
| Branding Switch | <30 sec | ✅ Achieved |
| Template Debug Cycles | 0 | ✅ Achieved |

## Production Triggers

Document enters production when:
- [x] Content fully validated
- [x] Template stack tested
- [x] Audience need confirmed
- [x] Sprint scheduled
- [x] Visual assets assessed

## Quick Links

- [Working Documents](workspace/)
- [Platform Template Stack](platform/templates/) · [Template Catalog](TEMPLATE-CATALOG.md)
- [Visual Assets Matrix](../ingestion/visual-assets-catalog/INGESTION-IMAGE-EXTRACTION-MATRIX.md)
- [Technical Debt / Punch List](PUNCH-LIST.md)

---

[→ Methodology & Details](ABOUT.md) | [→ Operations Dashboard](../README.md)