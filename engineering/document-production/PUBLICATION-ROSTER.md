# Publication Roster

Tracks every **manual-shaped** publication and document instrument in
`engineering/document-production/`, by category. The categories drive both
**consistency scope** (only the live set must stay mutually consistent) and
**how skills resume work** (e.g. `whats-next` reads this roster to decide
resume-vs-revive-vs-new).

Categories: **Live** (in front of the community) · **In development / parked**
(intended; may be a pre-production walk-away — *not* orphaned) · **Instruments**
(test/standards harnesses, not publications) · **Orphaned** (not carrying
forward). The discriminator between *parked* and *orphaned* is **intent**, not
state — a started-then-paused doc is parked if we still mean to ship it.

**Invariant:** every `workspace|manuals|outbound/<name>` folder appears in
exactly **one** section below. A folder with no entry is an **anomaly to
reconcile** (classify it), not a silent guess.

*Established: 2026-05-28 — Updated: 2026-06-05 (categorized into live / parked /
instruments / orphaned; Green Book retired in favor of the I/O & Smart Pins guide).*

---

## Live publications

These are the live working set. Any shared visual or editorial convention MUST be
kept consistent across the live set — a change to one that affects a shared
convention is a change to all of them.

| Publication | Workspace | Live since | Convention-reconciled? | Notes |
|-------------|-----------|-----------|------------------------|-------|
| P2 I/O & Smart Pins User Guide | `workspace/p2-io-and-smart-pins-user-guide/` | 2026-05-28 | yes | "Blue Book" reference; the standard others rebase on |
| P2 Assembly Language Reference | `workspace/p2-assembly-language-manual/` | 2026-05-28 | yes | PASM2 instruction reference |
| DeSilva PASM2 Tutorial | `workspace/p2-pasm-desilva-style/` | 2026-05-28 | yes | Pedagogical homage tutorial |
| P2 Debug Window Manual | `workspace/p2-debug-window-manual/` | 2026-06-04 | **pending** | promoted 2026-06-04 |
| P2 Single-Step Debugger Manual | `workspace/p2-single-step-debugger-manual/` | 2026-06-04 | **pending** | promoted 2026-06-04 |
| P2 Streamer Programming Guide | `workspace/p2-streamer-programming-guide/` | 2026-06-04 | **pending** | promoted 2026-06-04 |
| AI Privacy Guide | `workspace/ai-privacy-guide/` | 2026-06-04 | **pending** | presentation-class; rides pristine `p2kb-foundation.sty` |

> **Newly-promoted (2026-06-04):** Debug Window, Single-Step Debugger, Streamer, and
> AI Privacy Guide are now live, but their cross-publication convention reconciliation
> (per the **Rule** at the bottom of this file) is **pending** — to be completed as part
> of the manual layout-standards effort. Until then, the three original live publications
> remain the reconciled reference.

## In development / parked (NOT live)

Intended for production but not released — actively progressing or a
pre-production walk-away we still mean to ship. Free to evolve independently;
they do **not** constrain the live set and are **not** constrained by it until
promoted. Reconcile conventions against this roster at promotion.

| Publication | Workspace | State |
|-------------|-----------|-------|
| Spin2 Reference Manual | `workspace/spin2-reference-manual/` | parked; may go forward |

## Instruments (not publications)

Test / standards harnesses. Manual-shaped (full folder triad, generate PDFs) but
never released; each serves an **effort**, not the community. Not
consistency-bound. Resume into the effort it serves.

| Instrument | Workspace | Serves |
|------------|-----------|--------|
| P2 Layout Torture Test | `workspace/p2-layout-torture-test/` | the manual layout-standards effort (`methodology/manual-layout-standards-*`) |

## Orphaned (not carrying forward)

Started, then retired by decision — superseded or abandoned. Kept for history;
**not** resumed without an explicit revive decision; never consistency-bound.

| Publication | Workspace | Why retired |
|-------------|-----------|-------------|
| Smart Pins Tutorial ("Green Book") | `workspace/p2-smart-pins-tutorial/` | superseded by the I/O & Smart Pins User Guide (newer generation) |

---

## Shared conventions across the live set

### Code-block color = language (IDE-aligned)

One color = one language, so a reader moving between the live publications never
has to relearn the palette. Values match the Propeller Tool / FlexProp IDEs.

| Block | Color | Background | Border |
|-------|-------|-----------|--------|
| Spin2 | blue | `E3F2FD` | `1976D2` |
| PASM2 | green | `EBFCEB` | `4CB04C` |
| CORDIC | purple | `F8F5FF` | `A785C2` |
| Multi-COG | blue-gray | `F5F9FC` | `7FA8C9` |
| Antipattern | pink/red | `FFF5F5` | `C08080` |

Geometry (all five): `boxrule=2pt`, `leftrule=4pt` (accessibility), other rules
`0.5pt`, rounded corners, `left=30pt` (clears inset line numbers), `right=10pt`,
`top/bottom=8pt`, `before/after skip=15pt`, `breakable`.

Defined in each *reconciled* live publication's content style package:
- `p2-io-and-smart-pins-user-guide/templates/p2kb-iosp-content.sty`
- `p2-assembly-language-manual/templates/p2kb-pasm2-content.sty`
- `p2-pasm-desilva-style/templates/p2kb-desilva-content.sty`

> The four publications promoted 2026-06-04 (debug-window, ssdbg, streamer,
> ai-privacy) must have this convention verified/added to their content style
> packages as part of reconciliation — see the newly-promoted note above.

> **Note:** In the I/O & Smart Pins guide the assembly/PASM2 code-block
> environment is named `IOSPBlock` (guide-specific name) but is colored **green**
> — the PASM2 color — for cross-publication consistency, NOT yellow.

**Rule:** Do not diverge a shared convention in one live publication without
updating all reconciled live publications together. When a dormant publication is
promoted to live, reconcile its conventions against this roster as part of the
promotion.
