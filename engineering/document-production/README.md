# Document Production Pipeline

*Status synced to PUBLICATION-ROSTER 2026-07-05. The roster is the **source of truth** for
publication state; the tables here are a **glance-only mirror** (compact status matrices — no
prose), with all per-publication detail in the roster.*

> **Authoritative roster → [`PUBLICATION-ROSTER.md`](PUBLICATION-ROSTER.md)** — every manual-shaped
> folder + app note appears there exactly once, organized **by lifecycle status**
> (Done · In progress · Upcoming · Abandoned) with the full per-gate checkbox matrix + per-document
> detail. The tables below are a glance; the roster is the detail.

## Production States

| State | Symbol | Description |
|-------|--------|-------------|
| Planned | 🔴 | Identified need, not started |
| Content Ready | 🟡 | Source material available |
| In Production | 🟢 | Actively being generated |
| Released | ✅ | Published and available |
| Deferred | ⏸️ | Valid but not current priority |

## Done — shipped

| Document | Type | Ver | pp | Released |
|----------|------|-----|:--:|:--:|
| Getting Started | manual | 1.0.1 | 25 | ✅ |
| I/O & Smart Pins | manual | 1.0.5 | 398 | ✅ |
| Assembly Reference | manual | 3.1.3 | 505 | ✅ |
| DeSilva Tutorial | manual | 3.0.3 | 164 | ✅ |
| Debug Window | manual | 1.0.2 | 160 | ✅ |
| Streamer Guide | manual | 1.0.6 | 75 | ✅ |
| Architect's Guide | manual | 1.0.1 | 53 | ✅ |
| P2AN001 — ADC Instrumentation | app-note | 1.0.2 | 20 | ✅ |
| P2AN002 — CORDIC for Real Work | app-note | 1.0.1 | 14 | ✅ |
| P2AN003 — DAC & Signal Generation | app-note | 1.0.1 | 19 | ✅ |
| P2AN004 — Freq / Rotation / RC-Timing | app-note | 1.0.1 | 14 | ✅ |
| P2AN005 — Cooperative Multitasking / TASK | app-note | 1.0.1 | 12 | ✅ |
| P2AN006 — Sizing Cog & Task Stacks | app-note | 1.0.0 | 12 | ✅ |
| AI Privacy Guide | guide | — | — | ✅ |

## In progress

| Document | Type | State |
|----------|------|-------|
| XBYTE Guide | manual | v0.1.0 first draft |
| Single-Step Debugger | manual | draft; in technical review |
| P2 Layout Torture Test | instrument | serves the layout-standards effort |

## Upcoming — planned

App-note candidates + rationale + sequence: [`p2-app-note-roster.md`](../analysis/p2-app-note-roster.md).

| Document | Type |
|----------|------|
| Spin2 Reference Manual | manual |
| B2 Extended-Precision Math · B3 Fixed-Point · C2 Data Structures · Standalone USB | app-note |

## Abandoned

| Document | Type | Why retired |
|----------|------|-------------|
| Smart Pins Tutorial ("Green Book") | manual | superseded by the I/O & Smart Pins guide |

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