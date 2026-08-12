# P2 Single-Step Debugger Manual Changelog

## v1.0.0 (pending — co-releases with the PNut-Term-TS User Guide)

### Interaction completeness pass — the full keyboard, mouse, and wheel set

Grounded on a new source feed derived from the **PNut v55 Pascal source**
(`DebuggerUnit.pas`, the v55 parity baseline) and validated against the Tests 0–14
hardware walk. The feed lives in `REF-NO-COMMIT/` and is source only — it is never
shipped and is not cited in the manual.

**The structural defect this fixed.** Chapter 5 said it "gathers them into one
place to look up" and then gave the mouse **five generic bullets** — thinner than
the Chapter 3 it claimed to consolidate. A reader who went to the Command
Reference to look something up got *less* than by re-reading Chapter 3. Chapter 5
is now the complete set: every key, every click, every wheel step. Chapter 3 keeps
its job — teaching the regions where they live.

**Keyboard — four things the manual did not say:**
- The **five Ctrl combinations** (Ctrl+C/D/K/L/M) reach hub navigation instead of
  the letter commands; every other Ctrl combination does nothing. None of this was
  documented anywhere in the manual.
- **Ctrl+D is hub-scroll-down, not the DEBUG toggle** — the manual taught `D` for
  DEBUG with no hint that a held Ctrl silently reaches a different command in a
  different region. Now carried as a `caution` (the manual's first `:::` fence).
- Keys dispatch on the **character typed, not the physical key**, and are
  case-insensitive — so non-QWERTY layouts behave identically.
- **R** clears **both** delta watch lists, register *and* LUT. The manual said
  register only — half the behavior. Corrected in Chapter 3 (region 6) as well.
- **Enter**'s continuous mode is **throttled to ~20 breaks/sec**, which is why it
  does not look like free-running.

**Mouse — the click table replaces the five bullets**, 16 regions with left and
right stated separately, split into the cluster that *runs* the program and the
regions you click to *look* at something (one 16-row table stranded half a page
behind its own heading, and two grouped tables are easier to scan besides).
Included: break-condition buttons set *exclusively* on
left but toggle *without disturbing the others* on right; BREAK is not
button-sensitive; the Smart-Pin Watch right-click resets **and** switches the
all-pins/DIR-only filter; hub hex and hub ASCII are separate regions; an event
name left-click **arms** the event, it does not merely select it. Also documented:
a right-click address breakpoint is **refused in hub mode below `$400`** — silent,
and previously undocumented, so it read as a bug.

**Wheel — the matrix was half-present and is now complete.** Chapter 3 gave
`Ctrl ×4, Shift ×16`; the real behavior is four tiers across two modes (cog: 1 / 4
/ 16 / 32 registers; hub: 4 / 16 / 64 / 128 bytes), with **Ctrl+Shift** and the
entire hub-mode column previously missing. Added with it: cog scrolling **stops at
`$000` and `$3F0`** rather than wrapping; in hub mode the disassembly and hub
viewer **share one address** and move together; the hub data box has its own
four-tier scheme (16 / 1 / 4 / 128 bytes); and the wheel does **nothing** over the
hub heat map — click it, and it jumps to that 128-byte sub-block.

**Chapter 3 corrections** where it was narrower than the source: region 5 (wheel
tiers), region 6 (R clears both lists), region 7 (SFR navigation is *every* value,
with the `IJMP3`–`IRET1` below-`$400` cog-space rule — not just `PTRA`/`PTRB`),
region 16 (hex and ASCII as separate regions; wheel over data scrolls), region 17
(heat map jumps by 128-byte sub-block; the wheel is inert there).
