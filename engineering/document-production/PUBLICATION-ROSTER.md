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

*Established: 2026-05-28 — Updated: 2026-06-09 (Platform column corrected against
on-disk reality: I/O & Smart Pins / Assembly / DeSilva are bespoke forks ⏳ — NOT
yet migrated; Single-Step / Streamer confirmed ✅ on the shared platform stack).
2026-06-05: categorized into live / parked / instruments / orphaned; Green Book
retired in favor of the I/O & Smart Pins guide.*

---

## Live publications

These are the live working set. Any shared visual or editorial convention MUST be
kept consistent across the live set — a change to one that affects a shared
convention is a change to all of them.

**Status pipeline** — each manual migrates left → right through these gates. `Chip`
and `Community` review are **independent** (a manual can be released and
community-reviewed while chip review is still outstanding — see Assembly / DeSilva).
Markers: ✅ done · 🔄 in review / in progress · ⏳ awaiting · — n/a · _(blank)_ not yet reached.
`Platform` = migrated onto the shared **`p2kb-platform`** display stack and its
cross-publication conventions (the **Rule** at the bottom); `—` = a different class
that does not ride the shared stack.

| Publication | Slug | Draft | Assets | Platform | Chip review | Community review | Released | Notes |
|-------------|------|:--:|:--:|:--:|:--:|:--:|:--:|-------|
| P2 I/O & Smart Pins User Guide | `p2-io-and-smart-pins-user-guide` | ✅ | ⏳ | ✅ | | | | migrated 2026-06-09 onto the shared platform stack (twin migration: `.latex`→platform + empty `p2kb-iosp-local`; content already correct fences); proven on forge daemon (387pp, clean log; gained continuation markers + numbered captions/LoF); production bundle prepared. Uses the shared common cover (`book-artwork.png`, identical across all manuals). Awaiting Stephen's technical + asset review; "Blue Book" reference |
| P2 Assembly Language Reference | `p2-assembly-language-manual` | ✅ | ✅ | ⏳ | ⏳ | ✅ | ✅ | released on bespoke `p2kb-pasm2-*` fork (sty+lua, forked ~2026-01-23); awaiting platform migration; chip review outstanding |
| DeSilva PASM2 Tutorial | `p2-pasm-desilva-style` | ✅ | 🔄 | ✅ | ⏳ | ✅ | ✅ | migrated 2026-06-09 onto the shared platform stack (code divisions→fences in opus-master, `p2kb-desilva-local` overlay, 5 platform lua filters). **v2.3.0 (2026-06-10) content-accuracy release** — complete chapter-by-chapter re-audit vs the current P2KB fixed ~33 latent errors (4 CRITICAL incl. two inverted LOCKTRY spin-locks, an inverted SKIP table, a fabricated SETSE edge mode); regenerated clean (172pp, clean log, vbox-overflow 0). Audit record: local `audit/content-reaudit-2026-06-10.md`. chip review outstanding. **DEFERRED to final wrap-up (both REQUIRED, not release-blocking):** (1) repair the "P1 COG" image `\CogAnatomyDiagram` (Ch2 "COG Anatomy 101", `opus-master` ~L557); (2) `pnut-ts` compile-cert re-audit of ALL built-in code examples (use `-d` for DEBUG blocks). |
| P2 Debug Window Manual | `p2-debug-window-manual` | ✅ | ⏳ | ✅ | | | | awaiting screenshots — 5/10 hero figures + TERM captures still placeholders |
| P2 Single-Step Debugger Manual | `p2-single-step-debugger-manual` | ✅ | ✅ | ✅ | ⏳ | ⏳ | | on shared platform stack (foundation/content/diagrams); awaiting chip + community review |
| P2 Streamer Programming Guide | `p2-streamer-programming-guide` | ✅ | ✅ | ✅ | ⏳ | ⏳ | | on shared platform stack (foundation/content + streamer-local/-diagrams); awaiting chip + community review |
| AI Privacy Guide | `ai-privacy-guide` | ✅ | ✅ | — | ✅ | ✅ | ✅ | released; both reviews complete; presentation-class (rides pristine `p2kb-foundation.sty`) |

**Slug** is the one folder name each manual uses across all three trees —
`manuals/<slug>/`, `workspace/<slug>/`, and `outbound/<slug>/`. When a manual needs
more detail than fits in **Notes**, add a slim `↳` continuation row (markers blank,
detail in Notes).

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
consistency-bound. Resume into the effort it serves. **An instrument's analysis
IS its product** — unlike a publication's transient release-audit, its `audit/`
is **git-tracked** alongside its cases (see the `.gitignore` exception), so the
instrument, its analysis, and the fixes it drives version together.

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

Defined **once** in the shared platform content package for every reconciled live
publication:
- `platform/templates/p2kb-platform-content.sty` — used by **Debug Window**,
  **Single-Step Debugger**, **Streamer**, **DeSilva**, and **I/O & Smart Pins**.

The one not-yet-reconciled fork still defines the convention in its **own**
content package (retired on migration onto `p2kb-platform-content`):
- `p2-assembly-language-manual/templates/p2kb-pasm2-content.sty`

> Publications still pending platform reconciliation (`Platform ⏳` in the status
> pipeline above — only **Assembly Language Reference** remains) must migrate onto
> the shared `p2kb-platform-*` stack (retiring their bespoke fork `.sty` + `.lua`).
> Debug Window, Single-Step, Streamer, DeSilva, and I/O & Smart Pins are reconciled
> (on the shared `p2kb-platform-content`); the AI Privacy Guide is presentation-class
> and does not ride the shared stack.

> **Note:** In the I/O & Smart Pins guide the assembly/PASM2 code-block
> environment is named `IOSPBlock` (guide-specific name) but is colored **green**
> — the PASM2 color — for cross-publication consistency, NOT yellow.

**Rule:** Do not diverge a shared convention in one live publication without
updating all reconciled live publications together. When a dormant publication is
promoted to live, reconcile its conventions against this roster as part of the
promotion.

---

## Platform Freshness Ledger — which manuals need reproduction

Because the manuals share one `platform/` stack (see the column pipeline above), a
manual's PDF goes stale the moment a **platform file it consumes** is changed after
that PDF was generated. This ledger is the detector.

**How it works — a push-down list, newest on top:**
- **Append a `PLATFORM` line** every time a `platform/` file is modified.
- **Append a `PUBLISH` line** every time a manual's PDF is generated (record it when
  the generation is *confirmed clean*, not merely staged).
- **A manual is OUT OF DATE** if any `PLATFORM` line for a file *it consumes* sits
  **above** (newer than) that manual's most-recent `PUBLISH` line.
- **Prune to stay short:** collapse same-item duplicates to the latest; **drop a
  `PLATFORM` line once every consuming manual has a `PUBLISH` above it** (fully
  absorbed — git keeps the permanent modification history, so the ledger only carries
  what is still live). When all platform changes are absorbed, only `PUBLISH` lines
  remain → everything is current.

> **Source (2026-06-10):** `PUBLISH` datetimes are the **actual PDF mtimes from the
> Forge outbox** (the authoritative generation times); `PLATFORM` datetimes are the git
> commit that last modified each file. Two fully-absorbed platform lines (`tables.lua`
> 2026-06-06, `mnemonic-bold.lua` 2026-06-06 — every manual generated after them) were
> pruned on seeding. The **Assembly Language Reference** is a bespoke fork (not on the
> shared platform), so platform changes do not affect it — it joins this ledger when it
> migrates (its last PDF was 2026-05-23).

```
2026-06-10 02:37  PUBLISH   p2-pasm-desilva-style            (v2.3.0, 172pp — clean)
2026-06-09 23:39  PUBLISH   p2-io-and-smart-pins-user-guide
2026-06-09 22:50  PLATFORM  filters/p2kb-platform-figures.lua
2026-06-09 21:08  PLATFORM  templates/p2kb-platform-content.sty
2026-06-09 20:56  PUBLISH   p2-debug-window-manual
2026-06-09 20:39  PLATFORM  filters/p2kb-platform-code-coloring.lua
2026-06-08 08:32  PLATFORM  templates/p2kb-platform-foundation.sty
2026-06-08 08:32  PLATFORM  filters/p2kb-platform-pagination.lua
2026-06-07 20:25  PUBLISH   p2-streamer-programming-guide
2026-06-07 08:32  PUBLISH   p2-single-step-debugger-manual
2026-06-07 06:58  PLATFORM  templates/p2kb-platform-diagrams.sty
2026-06-07 03:04  PUBLISH   p2-layout-torture-test
```

**Currently out of date (read off the list above):**

| Manual | Status | Behind on (platform files changed since its PDF was generated) |
|--------|--------|----------------------------------------------------|
| `p2-pasm-desilva-style` | ✅ current | — (rebuilt on the latest platform today) |
| `p2-io-and-smart-pins-user-guide` | ✅ current | — (generated 23:39, *after* `figures.lua` 22:50; its figures.lua carry-over appears already resolved — worth one confirm) |
| `p2-debug-window-manual` | ⏳ stale | `figures.lua`, `content.sty` (it absorbed `code-coloring.lua` at 20:39) |
| `p2-streamer-programming-guide` | ⏳ stale | `figures.lua`, `content.sty`, `code-coloring.lua`, `foundation.sty`, `pagination.lua` |
| `p2-single-step-debugger-manual` | ⏳ stale | `figures.lua`, `content.sty`, `code-coloring.lua`, `foundation.sty`, `pagination.lua` |
| `p2-layout-torture-test` | ⏳ stale | all of the above + `diagrams.sty` |

**Maintenance discipline (must be honored or the ledger lies):** `prepare-manual`
appends/updates a `PUBLISH` line when a generation is confirmed clean; any edit to a
`platform/` file appends/updates a `PLATFORM` line. (Wiring this into those skills so
it is automatic — rather than hand-maintained — is an open follow-up.)
