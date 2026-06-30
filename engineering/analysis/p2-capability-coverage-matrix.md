# P2 Capability Coverage Matrix

> **Status:** v1 (2026-06-29), *Capability Coverage & App-Note Roster* sprint,
> Phase 6 (task #137). Cross-tabulates the four corpora — **P1 app notes**,
> **Quick Bytes**, **OBEX**, and **P2 manual/reference coverage** — against the
> capability spine (`engineering/standards/p2-capability-taxonomy.md`). This is
> the **data**; the ranked, placement-routed app-note **roster** is #138
> (`p2-app-note-roster.md`), built from this.

## Column sources
- **P1** — `engineering/analysis/p1-app-note-spine-mapping.md` (17 app notes).
- **QB** — `deliverables/ai/P2/community/quick-bytes/` (42 Quick Bytes).
- **OBEX** — `deliverables/ai/P2/community/obex/objects/` (130 capability objects + 5 design assets excluded).
- **Manual** — `engineering/analysis/p2-manual-coverage-by-domain.md` (live manuals + `deliverables/ai/P2/` reference YAMLs).

## The matrix (domain level)

Counts are primary-domain classifications. **Manual** records *type*, not just
presence (a "reference" cell can still sit atop an app-note gap).

| Domain | P1 | QB | OBEX | Manual | Coverage read |
|---|:--:|:--:|:--:|---|---|
| **A. Core compute model** | **5** | **0** | 7 | **Strong — reference only** (PASM2 ref, DeSilva, Architect's Guide, arch YAMLs) | Heavy P1 precedent, **zero QB** (you can't quick-demo a compute concept), OBEX = a few libs + the emulators; manual is ISA/tutorial, **no guided-application tier**. **The app-note seam.** |
| **B. Smart Pins & I/O** | 4 | 6 | 15 | **Strong** (IOSP User Guide) | Well covered every tier. Reference + applied patterns + demos exist. |
| **C. Math & DSP** | 0 | 2 | 9 | **Partial** (`cordic.yaml`, PASM2 ISA) | P2-unique; community present (FFT, JPEG, PRNG, CORDIC libs); **no guided CORDIC/DSP manual**. |
| **D. Streaming & video gen** | 0 | 0 | 1 | **Good** (Streamer guide + XBYTE guide in dev) | P2-unique; manual-covered; **community-thin** (gen is hard to package as a part). |
| **E. Comms & protocols** | 1 | 6 | **25** | **Weak** (only smart-pin serial via IOSP) | **Richest community vein**; manual thin. Parts+demos abundant. |
| **F. Sensors & environment** | 1 | 7 | **20** | **None** | Pure application domain; richly community-served. |
| **G. Displays & graphics** | 3 | **11** | **21** | **Weak** (gen mechanism in Streamer only) | Heavy community (QB + OBEX) + some P1; drivers/GUI unmanualed. |
| **H. Motors & motion** | 0 | 3 | 9 | **None** | Community-served application domain. |
| **I. Storage & memory** | 2 | 1 | 8 | **Partial** (`hub`/`lookup_ram` YAMLs) | Subsystem (hub) in reference; storage *apps* (SD/flash/RAM) community — incl. Stephen's 4261/5404/5405. |
| **J. Audio** | 0 | 1 | 7 | **None** | Community-served (incl. the 5 Wuerfel_21 sound-chip cores). |
| **K. Dev tools & workflow** | 1 | 5 | 3 (+5 design assets, excluded) | **Good** (Debug Window, Single-Step, Getting Started) | Well covered. |

## Notable leaf-level facts (so the roster doesn't false-flag)

- **AN006 FAT filesystem is NOT a gap.** OBEX carries FAT32/SD/flash: Gadd
  4269, Allen 4894, evanh 5048, and **Stephen's 4261 (flash) / 5404 (microSD) /
  5405 (dual)**. Domain I storage is community-covered.
- **Emulation is a P2 strength, already being manualed.** 7 emulation-flavored
  OBEX objects (NeoYume/MegaYume → A; 5 sound-chip cores → J), all Wuerfel_21,
  all P2. The **XBYTE Programming Guide** (in dev) is the guided home — so
  "build an emulator" is *not* an open app-note gap.
- **Domain A's OBEX count (7) is libraries + emulators, not compute-model
  tutorials.** It does **not** close the guided-composition gap.
- **5 hardware-design assets** (KiCAD/PCB/3D) sit at K·hardware-design and are
  **excluded** from gap analysis (non-capability resources, per the taxonomy).

## What the matrix says (hand-off to the roster #138)

Three coverage *signatures* emerge, and each routes differently under the
placement rubric — the routing/ranking is #138's job, but the signatures are the
matrix's finding:

1. **High-precedent, demo-less, reference-only (Domain A).** P1 taught it,
   QB can't demo it, manuals only reference it. → the **guided-composition
   app-note** signature. Strongest candidates: multicore, coroutines→multitasking,
   execution-timing, stack, data-structures.
2. **P2-unique, thin guidance (C; parts of D).** No P1 precedent, modest
   community, partial/sufficient manual. → app-note candidates surfaced from the
   *P2 side* (e.g. guided CORDIC use); D mostly closed by Streamer/XBYTE.
3. **Community-saturated application domains (E/F/G/H/J).** Abundant OBEX + QB,
   weak/no manual — *as expected* (applications, not subsystems). → the rubric
   mostly routes these **away from app notes** (OBEX adoption / QB suggestion);
   an app note earns a place only as a *synthesizing* guide over a recurring
   multi-subsystem task.

> Built into the ranked, placement-routed roster in `p2-app-note-roster.md` (#138).
