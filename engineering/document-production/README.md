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
| P2 Assembly Language Reference | `p2-assembly-language-manual` | ✅ **Released v3.1.0** (501pp, 2026-06-25) — accuracy + voicing/typography pass; Ω/μ/µ glyph fallback; chip review outstanding (external) |
| DeSilva PASM2 Tutorial | `p2-pasm-desilva-style` | ✅ **Released v3.0.0** (172pp, 2026-06-10) — re-audit (~33 fixes); chip review outstanding; 2 deferred wrap-up items |
| AI Privacy Guide | `ai-privacy-guide` | ✅ **Released** — both reviews complete; presentation-class |
| P2 I/O & Smart Pins User Guide | `p2-io-and-smart-pins-user-guide` | 🟢 draft (387pp), platform-migrated; **awaiting Stephen's technical + asset review** ("Blue Book") |
| P2 Single-Step Debugger Manual | `p2-single-step-debugger-manual` | 🟢 draft, platform stack; **cover repaired 2026-06-12**; in technical review (chip + community) |
| P2 Streamer Programming Guide | `p2-streamer-programming-guide` | 🟢 draft, platform stack; awaiting chip + community review |
| P2 Debug Window Manual | `p2-debug-window-manual` | ✅ **v1.0.0 released 2026-06-16** (community review); all figures captured; 32-demo example library bundled |

## In development / parked · Instruments · Orphaned (see roster for detail)

| Publication | Slug | Category |
|-------------|------|----------|
| Spin2 Reference Manual | `spin2-reference-manual` | in development / parked |
| P2 Layout Torture Test | `p2-layout-torture-test` | instrument (serves the layout-standards effort) |
| Smart Pins Tutorial ("Green Book") | `p2-smart-pins-tutorial` | orphaned — superseded by the I/O & Smart Pins guide |

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
- [Template Masters](../pdf-templates-master/)
- [Visual Assets Matrix](../ingestion/visual-assets/INGESTION-IMAGE-EXTRACTION-MATRIX.md)
- [Technical Debt](../technical-debt/VISUAL-ASSETS-DEBT.md)

---

[→ Methodology & Details](ABOUT.md) | [→ Operations Dashboard](../README.md)