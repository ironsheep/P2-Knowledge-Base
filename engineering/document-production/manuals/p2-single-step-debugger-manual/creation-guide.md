# Creation Guide — P2 Single-Step Debugger Manual

**Status:** DRAFT for review (Phase 1 — pedagogical plan + merge map)
**Created:** 2026-05-31
**Companion:** `voice-guide.md` (read together)

This guide is the plan for producing the Opus Master of the P2 Single-Step
Debugger Manual by blending and correcting the two existing source documents. It
exists so the shape, audience, and sourcing are agreed **before** any manual
prose is written.

---

## 1. Goal

Teach a P2 user — *lightly* familiar with the P2 (possibly P1 background),
*never* having used this debugger — how to use the **single-step debugger** to
observe and control a running P2 program and fix problems in it.

This is the new-environment release: the debugger is hosted in **`pnut-term-ts`**
and ships alongside it. The interaction model is **ported unchanged** from the
classic single-step debugger, so the existing command/UI material is fact.

## 2. Source documents (what we're blending)

| Source | Role in the blend | Notes |
|--------|-------------------|-------|
| `current-document.md` (Sep 2) | **The SHAPE.** Narrative arc, Quick Start, workflows, and the **Version History appendix**. | Tutorial-shaped; has P1-isms + SCOPE content to fix/detune. |
| `DEBUGGER-USER-MANUAL.md` (Sep 18) | **What we TEACH.** The debugger interaction: window layout, keyboard/mouse commands, breakpoints, memory/register inspection, SFR map. | Tool-accurate (ported model) but written PNut-IDE-flavored; re-host to `pnut-ts`/`pnut-term-ts`. |

Neither is the master. The Opus Master is a new blend, corrected against P2/
pnut-ts truth.

## 3. Audience & assumed knowledge

- **Assumed:** P2 has COGs, hub RAM, registers, flags (C/Z), pins; reader can
  write/compile a basic Spin2/PASM2 program.
- **NOT assumed:** any debugger experience; any knowledge of breakpoints,
  watches, single-stepping, heat maps.
- **P1→P2 bridge:** where a P1 habit will mislead, name it once (e.g. `cognew`→
  `COGSPIN`/`COGINIT`). Do **not** include a full P2 architecture refresher —
  point to the P2 fundamentals / IOSP material instead (one-line cross-ref).

## 4. Pedagogical arc (concept → orientation → guided doing → mastery → reference)

1. **What single-step debugging is, and why** — the core concept, in plain terms,
   motivated by a relatable "my code misbehaves" scenario. What you can *observe*
   vs *control*. (NEW prose; not in either source.)
2. **Turning on debugging & starting a session** — `pnut-ts -d`, run via
   `pnut-term-ts`, what triggers the debugger (DEBUG statement / PASM `debug` /
   COGINIT-with-debug). (From `current-document` Quick Start + `DEBUGGER-USER`
   "Invoking", CORRECTED for tooling.)
3. **Orientation: the debugger window** — the 123×77 layout and what each pane
   shows (COG/LUT heat maps, control registers, disassembly, watch, stack, hub
   viewer, buttons). Introduce each pane's *purpose* before its mechanics.
   (From `DEBUGGER-USER` "Window Interface".)
4. **Your first session (guided)** — a tiny program, set one breakpoint, step,
   read a register, resume. Show-then-formalize. (NEW prose stitching source
   examples; the teaching centerpiece.)
5. **The command vocabulary** — keyboard + mouse command tables. (From
   `DEBUGGER-USER`, verbatim-accurate.)
6. **Breakpoints in depth** — kinds (MAIN/INT/DEBUG/INIT/EVENT/ADDR/COGBRK), the
   break-condition register, setting/clearing. (From `DEBUGGER-USER`.)
7. **Observing state** — memory (COG/LUT/hub), registers + SFR map, flags, call
   stack, smart pins, events, heat-map reading. (From `DEBUGGER-USER`.)
8. **Working sessions / richer tasks** — PASM-level debugging, multi-COG
   debugging, performance/timing, finding memory corruption, debugging
   interrupts. (From both; CORRECTED.)
9. **DEBUG output, briefly** — just enough to read DEBUG text output; the nine
   display windows are **cross-referenced to the Debug Window Manual**, not
   taught here.
10. **Tips, best practices, troubleshooting.** (Merge both.)
11. **Appendix A: Version history / feature timeline.** (From `current-document`,
    fact-checked.)

## 5. In-scope vs cross-referenced

- **In scope:** the single-step debugger UI, commands, breakpoints, memory/
  register/stack inspection, multi-COG single-step workflows, DEBUG-to-trigger.
- **Cross-referenced (NOT taught here):** the nine DEBUG **display windows**
  (Terminal, Logic, Scope, XY, Plot, FFT, Bitmap, MIDI, Logger) → Debug Window
  Manual. Deep DEBUG output formatting → Debug Window Manual / Spin2 reference.

## 5a. Code-example styling (MUST match the sibling manuals)

All code examples in this manual use the **same colored code-block convention**
as the **PASM2 Assembly Language Reference Manual** and the **Smart Pins** guide
(and the IOSP User Guide, which adopted it from Smart Pins). This keeps the P2
publication set visually consistent.

The convention is **language-keyed coloring**, applied by a per-manual Lua
filter, driven by the fenced-code language tag:

| Fence tag | Block | Color (bg / left-bar border) |
|-----------|-------|------------------------------|
| ` ```spin2 ` | Spin2Block | light **blue** bg / blue border |
| ` ```pasm2 ` | PASM2 / IOSP block | light **green** bg / green border |

Sibling filters to copy from (same lineage — Smart Pins → IOSP → here):
- `workspace/p2-assembly-language-manual/filters/p2kb-pasm2-code-coloring.lua`
- `workspace/p2-smart-pins-tutorial/filters/p2kb-sp-code-coloring.lua`
- `workspace/p2-io-and-smart-pins-user-guide/filters/p2kb-iosp-code-coloring.lua`
  (best-maintained; also carries the blank-line-preservation fix and
  mnemonic-uppercasing — start from this one)

**Build-time requirements (record now so Phase 3 doesn't forget):**
1. Adapt a `p2kb-debugger-code-coloring.lua` filter from the IOSP one (rename
   the Block environments / color names to the `p2kb-debugger-*` prefix; keep the
   Spin2=blue / PASM2=green mapping identical).
2. Define the matching `Spin2Block` / PASM2 color environments in the debugger
   `*-content.sty` with the same HTML color values as the siblings (Spin2 bg
   `E3F2FD` / border `1976D2`; PASM2 bg `EBFCEB` / border `4CB04C`).
3. Tag every example fence explicitly `spin2` or `pasm2` so it picks up coloring
   (untagged fences render plain — same lesson as the IOSP review).
4. Carry the **blank-line-preservation fix** into any mnemonic/coloring filter
   adapted here (the sibling `*-mnemonic-bold.lua` filters drop blank lines in
   code blocks — see the IOSP pending-fixes audit; do not inherit that bug).

## 5b. Code Line Budget

The colored code boxes do NOT wrap, so an over-long code line is an authorship
defect caught by the `prepare-manual` line-length audit
(`engineering/tools/validation/audit-code-line-length.py`).

- **Max code columns (K): 76**
- **Code-box style / font:** the shared **platform** code boxes (`Spin2Block` /
  `IOSPBlock`), Latin Modern Mono at the box's code size with the `numbers=left`
  gutter. This manual consumes the platform code-box stack unchanged, so it
  **inherits the platform reference K** (calibrated in
  `manuals/p2-layout-torture-test/creation-guide.md` → Code Line Budget). Re-measure
  only if this manual ever diverges its code font/box geometry from the platform.

> **Platform note (migrated 2026-06-07):** this manual now renders on the shared
> platform — `p2kb-ssdbg.latex` loads `p2kb-platform-foundation` +
> `p2kb-platform-content`; the five `p2kb-platform-*` Lua filters replace the lone
> `ssdbg-code-coloring` (so PASM2 is `IOSPBlock` green, headings use the platform
> `titlesec` path, figures/tables number per chapter). Screenshots use the platform
> `\screenshotfig` keyline. The §5a build-time filter plan below is superseded by
> the platform stack.

## 6. Correction checklist (apply to ALL carried-forward content)

Each item is a trust-chain fix, sourced:

- [ ] **Tooling:** remove PNut-IDE menus, `pnut.exe -bd/-cd`, "PNut IDE". Replace
      with `pnut-ts -d` (compile w/ DEBUG; per `tools/documentation/
      pnut_ts-usage-guide.md`) and `pnut-term-ts` (host/debug terminal; per
      `narrative/my-posts/my-pnut-term-ts.md`).
- [ ] **P1-isms:** `cognew` → `COGSPIN`/`COGINIT`; `CNT` → `GETCT`. (current-doc
      lines ~71,74,151,161.)
- [ ] **DEBUG formatters:** bare `DEC/HEX/BIN` → `UDEC/UHEX/UBIN` (+`_` variant
      where a label already names the value). (DEBUGGER-USER lines ~59-61, 320+.)
- [ ] **Compile every code example** with `pnut-ts` before shipping (CLAUDE.md
      Trust Chain). pnut-ts at /usr/local/bin (v1.55.0).
- [ ] **SCOPE/displays:** reduce ~32 mentions to a single cross-ref paragraph.
- [ ] **Voice:** strip superlatives/marketing per `voice-guide.md`.
- [ ] **Code coloring:** tag every example `spin2`/`pasm2` and wire the
      `p2kb-debugger-code-coloring.lua` filter so blocks match the Assembly
      Reference / Smart Pins coloring (see §5a).

## 7. Open questions for the user (answer before Phase 2 drafting)

1. **Version-history appendix** — keep the full v35u→v51 evolution timeline, or
   trim to "feature availability by version" (a table)? It's historically PNut-
   flavored; needs reframing for the pnut-ts/pnut-term-ts era.
2. **Worked-example program** — OK for me to author a small, original,
   `pnut-ts`-compilable example for the "first session" chapter (rather than
   reusing the source docs' fragments)?
3. **Title/subtitle & author** — proposed: title "P2 Single-Step Debugger
   Manual"; subtitle TBD (e.g. "Observe and Control Your Running P2 Code");
   author "Iron Sheep Productions, LLC". Confirm or adjust.

## 8. After Phase 1 approval (the remaining phases)

- **Phase 2 — Build the Opus Master** `P2-Single-Step-Debugger-Manual.md` in
  `manuals/.../opus-master/` (single file or chapter tree — TBD by length), to
  this plan + voice, with all corrections applied and examples compiled.
- **Phase 3 — Make build-ready:** template stack (`p2kb-debugger-*` adapted from
  the proven `p2kb-debugwin-*`), `request.json`, `outbound/` — then first
  `pnut-ts`-validated + Forge PDF pass.

## 9. Sourcing references
- Tooling: `engineering/tools/documentation/pnut_ts-usage-guide.md`
- pnut-term-ts: `engineering/narrative/my-posts/my-pnut-term-ts.md` (v0.9.1 notes)
- Interaction model: the two source docs (ported-unchanged classic debugger).
- Template precedent: `workspace/p2-debug-window-manual/` (sibling, build-ready).
