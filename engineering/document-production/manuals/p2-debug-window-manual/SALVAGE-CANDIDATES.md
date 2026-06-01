# Salvage Candidates — Debug Window Manual

**Purpose.** When the manual was rewritten from the narrative-themed legacy
`chapters/` into the window-reference `chapters-v3/` (now the canonical
`opus-master/` source), substantial *teaching content and worked patterns* were
dropped. The legacy material is **pre-v55 and pre-audit** — it contains the very
fabrications the audit methodology exists to catch (e.g., LOGIC protocol
decoding). So we do **not** merge it back. Instead, each valuable pattern is
re-authored **clean-room** from the v55 Bibles.

## Retrieval

The full legacy corpus (legacy `chapters/` + the old single-file assemblies) is
preserved in git history — last present at commit **`270289f`** (the snapshot
taken immediately before the opus-master cleanup). Retrieve any legacy file with:

```
git show 270289f:engineering/document-production/manuals/p2-debug-window-manual/opus-master/chapters/<file>
```

## Clean-room method (per the approved approach)

For each candidate below, **one at a time**, for review:

1. **Study** the legacy chapter for the *capability / pattern it teaches* — not its prose.
2. **Re-author** fresh content grounded in `REF/theory-of-operations/` (v55) and the
   directive matrix; validate every code example with `pnut_ts`.
3. **Place** it at the correct location in the current window-reference structure
   (it does **not** return as its old chapter number).
4. Present for review; incorporate on approval.

## Do NOT resurrect (correctly purged — would re-inject errors)

- LOGIC **protocol decoding** (I2C/SPI/UART/CAN) — documented fabrication; v55 LOGIC shows raw waveforms only.
- The **"20× performance"** layer claim/benchmark — unverified marketing number.
- Any worked example not re-validated with `pnut_ts` against v55.

## Candidates (approved scope: legacy ch 1, 2, 4, 6, 12, 13, 14)

| # | Legacy source (`270289f:…/chapters/`) | Pattern to re-author | Target location in current manual | Status |
|---|----------------------------------------|----------------------|-----------------------------------|--------|
| 1 | `chapter-01-vision-gap.md` | "Debug Iceberg" motivation + concrete failure scenarios (why visual debugging) | `ch01-foundation.md` / front matter | TODO |
| 2 | `chapter-02-terminal-mastery.md` | GOTOXY terminal dashboards, menus, bar-graphs, multi-field updates (the *patterns*, not the bare control codes) | `ch03-term.md` | TODO |
| 3 | `chapter-04-layer-composition.md` | LAYER/sprite *techniques* for low-flicker updates (no "20×" claim) | `ch05-plot.md` | TODO |
| 4 | `chapter-06-professional-instruments.md` | Built examples: analog gauge, LED panel, VU meter, toggle switches, knob/slider | `ch05-plot.md` (+ relevant window chapters) | TODO |
| 5 | `chapter-12-multi-window.md` | Multi-window orchestration: synchronized capture, dashboard layouts, bandwidth pacing | `ch14-multiwindow-pasm.md` | TODO |
| 6 | `chapter-13-pasm-integration.md` | PASM debug patterns: cycle-aware DEBUG placement, FIFO/cog-coordination, profiling | `ch14-multiwindow-pasm.md` | TODO |
| 7 | `chapter-14-production-workflows.md` | Screenshot-driven docs, automated/CI test reporting, field-diagnostic workflows | New section in `ch14` (or its own chapter) | TODO |

## Optional extras (flagged by the audit, not in the approved scope — confirm before doing)

- `appendix-c-performance-guide.md` — optimization/bandwidth/buffer-pooling guidance (no v55 appendix equivalent).
- `appendix-e-hover-coordinates.md` — per-window mouse-hover readout formats (useful reference; partly in `appendix-c-color-coordinate.md`).
