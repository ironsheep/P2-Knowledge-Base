# Publication Roster

Tracks which P2 document-production publications are **live** (released to the
community) versus **dormant** (in development, not yet released). This roster
exists so cross-publication consistency work has a clear, authoritative scope:
**only the live set must stay mutually consistent.**

*Established: 2026-05-28*

---

## Live publications

These are released and in front of the community. Any shared visual or editorial
convention MUST be kept consistent across all three — a change to one that
affects a shared convention is a change to all three.

| Publication | Workspace | Notes |
|-------------|-----------|-------|
| P2 I/O & Smart Pins User Guide | `workspace/p2-io-and-smart-pins-user-guide/` | "Blue Book" reference |
| P2 Assembly Language Reference | `workspace/p2-assembly-language-manual/` | PASM2 instruction reference |
| DeSilva PASM2 Tutorial | `workspace/p2-pasm-desilva-style/` | Pedagogical homage tutorial |

## Dormant publications (NOT live)

In development or on hold. Free to evolve independently; they do **not** constrain
the live set and are **not** constrained by it until they are promoted to live.

| Publication | Workspace |
|-------------|-----------|
| Smart Pins Tutorial ("Green Book") | `workspace/p2-smart-pins-tutorial/` |
| Debug Window Manual | `workspace/p2-debug-window-manual/` |
| Single-Step Debugger Manual | `workspace/p2-single-step-debugger-manual/` |
| Streamer Programming Guide | `workspace/p2-streamer-programming-guide/` |
| Spin2 Reference Manual | `workspace/spin2-reference-manual/` |
| AI Privacy Guide | `workspace/ai-privacy-guide/` |

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

Defined in each live publication's content style package:
- `p2-io-and-smart-pins-user-guide/templates/p2kb-iosp-content.sty`
- `p2-assembly-language-manual/templates/p2kb-pasm2-content.sty`
- `p2-pasm-desilva-style/templates/p2kb-desilva-content.sty`

> **Note:** In the I/O & Smart Pins guide the assembly/PASM2 code-block
> environment is named `IOSPBlock` (guide-specific name) but is colored **green**
> — the PASM2 color — for cross-publication consistency, NOT yellow.

**Rule:** Do not diverge a shared convention in one live publication without
updating all three together. When a dormant publication is promoted to live,
reconcile its conventions against this roster as part of the promotion.
