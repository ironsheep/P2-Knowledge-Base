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
| Getting Started with the Propeller 2 | `p2-getting-started-guide` | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | **v1.0.0 (2026-06-24)** — initial community-review release. The orientation on-ramp, split 2026-06-24 from the P2 Architect's Guide first draft (orientation Chs 1–3 "Meet the Propeller 2" / "Reading P2 Code" / "Putting It to Work" + Where-to-Next); born on the shared platform stack with `p2kb-getting-started-*` locals; release-gate audited (drain GREEN) + finalized; 25pp. Links out to the reference manuals + the Architect's Guide. chip review outstanding |
| P2 I/O & Smart Pins User Guide | `p2-io-and-smart-pins-user-guide` | ✅ | ⏳ | ✅ | | | | migrated 2026-06-09 onto the shared platform stack (twin migration: `.latex`→platform + empty `p2kb-iosp-local`; content already correct fences); proven on forge daemon (387pp, clean log; gained continuation markers + numbered captions/LoF); production bundle prepared. Uses the shared common cover (`book-artwork.png`, identical across all manuals). Awaiting Stephen's technical + asset review; "Blue Book" reference |
| P2 Assembly Language Reference | `p2-assembly-language-manual` | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | **v3.0.0 (2026-06-10)** — migrated off the bespoke `p2kb-pasm2-*` fork onto the shared platform stack (`p2kb-pasm2-local` overlay + 5 platform lua filters + 2 local entry filters); content re-certified vs the current P2KB and rebuilt clean (492pp). chip review outstanding |
| DeSilva PASM2 Tutorial | `p2-pasm-desilva-style` | ✅ | 🔄 | ✅ | ⏳ | ✅ | ✅ | migrated 2026-06-09 onto the shared platform stack (code divisions→fences in opus-master, `p2kb-desilva-local` overlay, 5 platform lua filters). **v3.0.0 (2026-06-10) release** — absorbs the content-accuracy re-audit (~33 latent errors fixed vs the current P2KB: two inverted LOCKTRY spin-locks, an inverted SKIP table, a fabricated SETSE edge mode, etc.) and the Ch2 egg-beater diagram fix; regenerated clean (172pp). Audit record: local `audit/content-reaudit-2026-06-10.md`. chip review outstanding. **DEFERRED to final wrap-up (both REQUIRED, not release-blocking):** (1) repair the "P1 COG" image `\CogAnatomyDiagram` (Ch2 "COG Anatomy 101", `opus-master` ~L557); (2) `pnut-ts` compile-cert re-audit of ALL built-in code examples (use `-d` for DEBUG blocks). |
| P2 Debug Window Manual | `p2-debug-window-manual` | ✅ | ✅ | ✅ | | ✅ | ✅ | **v1.0.0 (2026-06-16)** — initial community-review release; all figures captured; 32-demo example library bundled (source ZIP) |
| P2 Single-Step Debugger Manual | `p2-single-step-debugger-manual` | ✅ | ✅ | ✅ | ⏳ | ⏳ | | on shared platform stack (foundation/content/diagrams); awaiting chip + community review |
| P2 Streamer Programming Guide | `p2-streamer-programming-guide` | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | **v1.0.1 (2026-06-19)** released as community-review edition — grounding-audit corrections + §3.5 clock-accuracy section + emoji→fenced callouts; platform-unification pilot. chip review outstanding |
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
| **The P2 Architect's Guide** (design book) | `manuals/p2-architect-guide/` + `workspace/p2-architect-guide/` | **in development — SPLIT in progress (2026-06-24).** The v0.1.0 first draft (4 ch, 48pp, born on the unified `p2kb-platform-*` stack) is being divided into two books after a walkthrough review (`manuals/p2-architect-guide/audit/walkthrough-feedback-2026-06-24.md`). **This folder retains the design / realization book** — *The P2 Architect's Guide — Designing Real Systems on the Propeller 2* — keeping Ch4 (functional decomposition) + a new front-end (peripherals → buses → pin budget) + a realization / AI-assist pillar. Orientation Chs 1–3 split out to **Getting Started**, now released v1.0.0 (see the Live table). Charter / voice / changelog to be re-cut to the design scope. |

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
- `platform/templates/p2kb-platform-content.sty` — used by **Assembly Language
  Reference**, **Debug Window**, **Single-Step Debugger**, **Streamer**, **DeSilva**,
  and **I/O & Smart Pins** (all six live technical publications).

> All live technical publications are now reconciled onto the shared
> `p2kb-platform-*` stack — the **Assembly Language Reference** completed migration in
> **v3.0.0 (2026-06-10)**, retiring the last bespoke fork (`p2kb-pasm2-*`; its
> `p2kb-pasm2-content.sty` is now vestigial). The AI Privacy Guide is
> presentation-class and does not ride the shared stack.

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
> pruned on seeding. The **Assembly Language Reference** completed its platform
> migration on 2026-06-10 (v3.0.0) and now appears in the ledger like the others.

```
2026-06-24 22:36  PUBLISH   p2-getting-started-guide         (v1.0.0, 25pp — initial Community Review Edition; release-gate audited + finalized; clean compile log, 0 overfull)
2026-06-24 21:01  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua   (AG-01: English-collision handling for call/push/ones/test — daemon-verified on Getting Started; other manuals low-urgency regen)
2026-06-23 05:30  PUBLISH   p2-architect-guide               (v0.1.0 first draft, 48pp — FOUR chapters + back matter + 5 figures; IN DEVELOPMENT, not a public release)
2026-06-19 20:44  PUBLISH   p2-streamer-programming-guide    (v1.0.1, 71pp — grounding-audit fixes + §3.5 clock accuracy + fenced callouts)
2026-06-19 20:41  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua   (do not bold the English verb "fit" — subject-pronoun + article-object contexts)
2026-06-19 19:10  PLATFORM  templates/p2kb-platform-content.sty       (add HardwareBlock graphite callout)
2026-06-19 19:10  PLATFORM  filters/p2kb-platform-code-coloring.lua   (map ::: hardware -> HardwareBlock)
2026-06-16 22:39  PUBLISH   p2-debug-window-manual           (v1.0.0, 159pp — initial community-review release)
2026-06-16 20:47  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua   (0ddf83f — stop bolding English-collision words: adds/byte/word/long)
2026-06-12 18:39  PLATFORM  templates/p2kb-platform-content.sty       (a149b8e — ::: tip/caution callouts)
2026-06-12 18:39  PLATFORM  filters/p2kb-platform-code-coloring.lua   (a149b8e — ::: tip/caution callouts)
2026-06-10 23:35  PUBLISH   p2-pasm-desilva-style            (v3.0.0, 172pp — egg-beater Ch2 diagram fixed)
2026-06-10 23:33  PUBLISH   p2-single-step-debugger-manual   (regression rebuild on the latest platform)
2026-06-10 23:32  PUBLISH   p2-assembly-language-manual      (v3.0.0, 492pp — migrated off the bespoke fork onto the platform)
2026-06-09 23:39  PUBLISH   p2-io-and-smart-pins-user-guide
2026-06-09 22:50  PLATFORM  filters/p2kb-platform-figures.lua
2026-06-08 08:32  PLATFORM  templates/p2kb-platform-foundation.sty
2026-06-08 08:32  PLATFORM  filters/p2kb-platform-pagination.lua
2026-06-07 06:58  PLATFORM  templates/p2kb-platform-diagrams.sty
2026-06-07 03:04  PUBLISH   p2-layout-torture-test
```

**Currently out of date (read off the list above):**

**Regeneration status (updated 2026-06-15).** A previously-unrecorded 2026-06-12
platform edit (`a149b8e` — `content.sty` + `code-coloring.lua`, advisory callouts) now
sits ABOVE the 2026-06-10 rebuild wave, so those four are technically behind it (the
callout change is cosmetic for manuals that use no `::: tip` / `::: caution` blocks — a
regen wave is due but low-urgency for them). Only `p2-debug-window-manual` was built on
top of the 06-12 platform.

| Manual | Status | Notes |
|--------|--------|----------------------------------------------------|
| `p2-debug-window-manual` | ✅ current | **v1.0.0 released 2026-06-16** for community review; all figures captured; built on the latest platform (incl. 06-16 `mnemonic-bold.lua`) |
| `p2-assembly-language-manual` | ⏳ behind 06-12 | rebuilt v3.0.0 on 06-10 (492pp); predates the 06-12 platform edit |
| `p2-pasm-desilva-style` | ⏳ behind 06-12 | rebuilt v3.0.0 on 06-10 (172pp); predates the 06-12 platform edit |
| `p2-streamer-programming-guide` | ✅ current | **v1.0.1 released 2026-06-19** (71pp); built on the latest platform (incl. 06-19 HardwareBlock + fit fix) |
| `p2-single-step-debugger-manual` | ⏳ behind 06-12 | regression rebuild 06-10; predates the 06-12 platform edit |
| `p2-io-and-smart-pins-user-guide` | ⏳ to regenerate | last built 2026-06-09; behind `figures.lua` + the 06-12 edit |
| `p2-layout-torture-test` | ⏳ stale (instrument) | behind several platform files + `diagrams.sty` |

**Maintenance discipline (must be honored or the ledger lies):** `prepare-manual`
appends/updates a `PUBLISH` line when a generation is confirmed clean; any edit to a
`platform/` file appends/updates a `PLATFORM` line. (Wiring this into those skills so
it is automatic — rather than hand-maintained — is an open follow-up.)
