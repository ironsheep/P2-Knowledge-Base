# Single-Step Debugger — Operation Guide & Parity Audit

> **Purpose**: A lightweight, fact-based operator's guide to the P2 single-step
> debugger window, **plus** a TypeScript-vs-Pascal parity audit from the user-
> interaction standpoint. Every keystroke, mouse action, and window behavior
> below was verified against the actual source on both sides:
>
> - **Pascal (the specification)**: `/pascal-source/P2_PNut_Public/DebuggerUnit.pas`
>   — handlers `FormKeyDown` (L1012), `FormKeyPress` (L1033), `FormMouseDown`
>   (L716), `FormMouseWheel` (L972), `FormMouseMove` (L632).
> - **TypeScript (the reimplementation)**: `src/classes/debugDebuggerWin.ts`,
>   `src/classes/shared/debuggerInteraction.ts`,
>   `src/classes/shared/debuggerProtocol.ts`.
>
> Where the two differ, the Pascal behavior is correct (per project policy) and
> the discrepancy is flagged in **Part B** as work to do.

---

# PART A — OPERATOR'S GUIDE

## A.1 How the debugger appears

- The debugger is **not opened from a menu**. It opens automatically when the P2
  hits a debug breakpoint, which happens when:
  - the program executes a `DEBUG` statement, or
  - a configured break condition fires (`DEBUG_MAIN`, `DEBUG_COGINIT`, etc.).
- **One window per COG.** Each COG (0–7) that breaks gets its **own** window,
  titled **`Debugger - Cog N`**. There is no tab switching — up to **8 windows**
  coexist, each driven independently. (TS: `DebugDebuggerWindow` is constructed
  per `cogId`, `windowId = "debugger-${cogId}"`; COG id is range-checked 0–7.)
- Windows cascade so they don't stack exactly on top of each other.
- The debugger is **read-only**: you observe state and control execution. You
  **cannot** edit registers, memory, or pins from the window. (Confirmed: Pascal
  `FormMouseDown` has no edit/write path anywhere.)

## A.2 Window anatomy (123 × 77 half-row character grid)

```
     REGMAP  LUTMAP   C  Z  PC      SKIP/SKIPF pattern        XBYTE   CT(64-bit)
   +--------+--------+----------------------------------------------------------+
   |        |        | DISASSEMBLY (16 lines)        | WATCH | SFR ($1F0-$1FF) | E
   | reg    | lut    |                               | (reg  | (16 regs, 2 col)| V
   | heat   | heat   |                               | delta)|                 | E
   | map    | map    | EXEC  STACK (8 longs)                          BUTTON    | N
   |        |        | INT1/2/3   PTR (FPTR/PTRA/PTRB + bytes)         PANEL     | T
   |        |        | STATUS  PIN (DIR/OUT/IN, 64-bit binary)        (13 btns) |
   |        |        | SMART PIN WATCH                                          |
   |        |        | HUB DATA (8 rows × 16 bytes hex+ASCII)      HUB HEATMAP   |
   |        |        |            HINT BAR                                      |
   +--------+--------+----------------------------------------------------------+
```

Panels (all display-only unless noted in the mouse table):

| Panel | Shows |
|---|---|
| REG / LUT heatmap | Per-bit change "heat" for COG `$000–$1FF` / LUT `$200–$3FF` |
| C / Z / PC | Carry, Zero, 20-bit program counter (5 hex) |
| SKIP / SKIPF | 32-bit skip pattern (dim "Suspended…" when in CALL/interrupt) |
| XBYTE | XBYTE engine config (3 hex + checkmark if C/Z affected) |
| CT | 64-bit clock-tick counter (16 hex) |
| DISASSEMBLY | 16 disassembled lines; PC line inverse-highlighted |
| WATCH | Auto delta list of changed COG registers |
| SFR | The 16 special-function registers `$1F0–$1FF` |
| EVENT | 16 event flags (INT, CT1…QMT) as 0/1 |
| EXEC | Current context: MAIN / INT1 / INT2 / INT3 |
| STACK | 8 hardware-stack longs (STK0 = top) |
| INT1/2/3 | Interrupt event + idle/wait/busy state |
| PTR | 14 bytes of hub around FPTR, PTRA, PTRB |
| STATUS | INIT, STALLI, STR, MOD, LUTS indicators |
| PIN | DIR / OUT / IN as 64-bit binary |
| SMART | Auto delta list of changed smart-pin RQPIN values |
| HUB | Hub hex+ASCII viewer (8×16) |
| HUB heatmap | Block-level hub change activity |
| HINT BAR | Context help for whatever the mouse is over |

## A.3 Execution model (what "running" means here)

The cog is always either **halted in the debug ISR** (polling the host ~15×/sec)
or **running**. The host drives three states (TS `sendDebugCommand`, mirrors
Pascal §4):

| State | How you enter it | Behavior |
|---|---|---|
| **Halted** | Default at every break | Display fully drawn. Go button reads **"Go"**. |
| **Single Go** | `SPACE` or **left-click Go** | Sends the break condition **once**, cog runs until the condition is met, then halts again (one step). |
| **Repeat** | `ENTER` or **right-click Go** | Cog runs continuously, throttled to ~20 breaks/sec for visual tracking. Go button reads **"Stop"**. Press `SPACE`/`ENTER`/click Go to stop. |
| **Dimmed** | ~250 ms with no new break while running | Whole display dims (brightness halved); Go button reads **"Break"**. Next break re-brightens it. |

## A.4 Keyboard — complete set

This is the **entire** keyboard interface. There are no other keys.
(Pascal `FormKeyPress` handles SPACE/ENTER/B/I/D/M/R; `FormKeyDown` handles the
arrow/page keys. TS `KEYBOARD_SHORTCUTS` matches exactly.)

| Key | Action | Equivalent to |
|---|---|---|
| **Space** | Single-step (one Go) | Left-click **Go** |
| **Enter** | Toggle repeat (continuous) run | Right-click **Go** |
| **B** | Async-break mode: clear all break conditions except INIT | Left-click **BREAK** |
| **I** | Toggle INIT break (bit 8) | Right-click **INIT** |
| **D** | Toggle DEBUG break (bit 4) | Right-click **DEBUG** |
| **M** | Toggle MAIN single-step (bit 0) | Right-click **MAIN** |
| **R** | Reset the register-watch list | Left-click **WATCH** box |
| **↑ / ↓** | Hub viewer −/+ `$10` (one row) | — |
| **PageUp / PageDown** | Hub viewer −/+ `$80`; **Ctrl** = `$1000`; **Shift** = `$10000` | — |
| **Tab** | Captured/ignored (prevents focus loss) | — |

Letter keys are case-insensitive. Arrow/Page keys are global to the window (no
panel needs focus first).

## A.5 Mouse — complete set

Left/right click and the wheel are the only mouse inputs.
(Reference: Pascal `FormMouseDown` L716–971, `FormMouseWheel` L972–1010.)

### Clicks

| Region | Left-click | Right-click |
|---|---|---|
| **Break-condition buttons** (MAIN, INT1/2/3, DEBUG, INT1E/2E/3E, INIT, EVENT, ADDR) | Set that condition **exclusively** (keeps INIT bit 8) | **Toggle** that condition on/off |
| **BREAK button** | Clear all conditions except INIT | — |
| **Go button** | Single-step | Toggle repeat mode |
| **Disassembly** | Lock view to the clicked line (`dmPC → dmCog`) | Toggle an address breakpoint at that line (sets ADDR) |
| **REG / LUT heatmap** | Lock disassembly to that COG/LUT address | — |
| **PC box** | Return to follow-PC mode (`dmPC`) | — |
| **SFR value** | IJMP/IRET → lock disassembly there; PA/PB/PTRA/PTRB → jump hub viewer | — |
| **Stack value** | Jump disassembly to that return address | — |
| **Event name** | Select that event as the EVENT-break target | — |
| **Pointer box (FPTR/PTRA/PTRB)** | Jump hub viewer to that pointer | — |
| **Hub data / hub heatmap** | Jump hub viewer to the clicked address | — |
| **WATCH box** | Reset register-watch list | — |
| **SMART pin watch box** | Reset smart-pin watch list | Toggle "DIR-only / all pins" filter |

### Wheel

| Over… | No modifier | Ctrl | Shift |
|---|---|---|---|
| **Disassembly (cog-locked)** | ±1 reg | ±4 | ±16 |
| **Disassembly (hub-locked)** | ±16 bytes | ±1 | ±4 |
| **Hub data box** | ±16 bytes | ±1 | ±4 |
| **Hub address digits** | ±1 on the hex nibble under the cursor | — | — |

Wheeling the disassembly while in follow-PC mode first unlocks it to cog/hub mode.

### Hover

Moving the mouse over any panel updates the **HINT BAR** at the bottom with
context help (register address+value, "click to reset", "Special function
registers", disassembly mode, etc.). See Pascal `FormMouseMove`.

## A.6 Break conditions (the button panel)

Break conditions are **bitmask flags** in `BreakValue`; several can be active at
once. Left-click = exclusive set (keeps INIT); right-click = toggle.

| Button | Bit / mask | Meaning |
|---|---|---|
| MAIN | `$001` | Break on each MAIN instruction (single-step) |
| INT1 / INT2 / INT3 | `$002 / $004 / $008` | Single-step within that interrupt |
| DEBUG | `$010` | Break on `DEBUG` (BRK with non-zero code) — **mutually exclusive** with the single-step bits |
| INT1E / INT2E / INT3E | `$020 / $040 / $080` | Break on interrupt entry |
| INIT | `$100` | Break on COGINIT — **independent**, never cleared by other buttons |
| EVENT | `$200` (+ event id in bits 15:12) | Break on a chosen event |
| ADDR | `$400` (+ addr in bits 31:12) | Break on an address match |
| BREAK | — | Clear all conditions except INIT (async-break mode) |
| (internal) | `$800` | STALL flag — keeps the cog halted; not a user button |

## A.7 Multi-COG notes

- Each COG window steps/runs **independently**.
- **COGBRK (async break)** lets one halted cog force another into the debugger —
  but only works while **some** cog is already halted in its debug ISR and
  pumping the protocol. If no cog is in debug, the host cannot force a break.

---

# PART B — TYPESCRIPT ↔ PASCAL PARITY AUDIT (user-interaction)

Scope: only the **operator-facing** behaviors above. Rendering/protocol internals
are out of scope here. Legend: ✅ implemented & matches · ⚠️ partial/incorrect ·
❌ missing · ➕ TS-only behavior not in Pascal (should be removed).

## B.1 Keyboard — ✅ full parity

All keys (`SPACE, ENTER, B, I, D, M, R, ↑, ↓, PgUp, PgDn` + modifiers, `Tab`
captured) are present and behave as Pascal does.
(`debuggerInteraction.ts` `KEYBOARD_SHORTCUTS` L32–50, `executeKeyboardAction`
L160–216.) **No action needed.**

## B.2 Execution control & buttons — ✅ parity

- Single Go / Repeat / Stall state machine matches Pascal §4
  (`sendDebugCommand`, L875–1044).
- All 13 buttons, with left-exclusive / right-toggle semantics and the DEBUG
  mutual-exclusion mask, match `FormMouseDown` L716–790. **No action needed.**

## B.3 Wheel scrolling — ⚠️ partial

- The **hub box** wheel works: it routes through `hubNavigate` with the correct
  Pascal deltas (none 16 / Ctrl 1 / Shift 4). (`handleMouseWheel` L309–338,
  `handleHubNavigate` L1050.)
- ❌ The **disassembly** wheel does **nothing**: the window's `disassemblyScroll`
  listener is an empty TODO (`debugDebuggerWin.ts` L766: "Wire to disassembly
  mode switching + scroll … For now [no-op]"). So mouse-wheel over the
  disassembly (which should auto-unlock `dmPC→dmCog/dmHub` and scroll, per
  `FormMouseWheel` L984–1003) has no effect.
- ❌ The **address-digit** nibble wheel is also unhandled (see B.4 note).

(The `command`/`hubNavigate`/`disassemblyScroll` listeners are each registered
once — `debugDebuggerWin.ts` L760/763/766 — so there is no double-fire.)

## B.4 Mouse-click navigation — ❌ largely missing

Pascal's `FormMouseDown` makes most panels clickable for navigation. The TS hit
tester (`debuggerInteraction.ts` `hitTest` L343–538) only recognizes: buttons,
COG/LUT register cells, hub-memory cells, disassembly lines, a 4-row "register
watch", and pin cells. The following Pascal click behaviors are **not
implemented** (clicking does nothing):

| # | Pascal click behavior | Pascal ref | TS status |
|---|---|---|---|
| 1 | **REG heatmap** → lock disassembly to cog addr (`dmCog`) | FMD L857–862 | ❌ treated as a "memory" cell instead |
| 2 | **LUT heatmap** → lock disassembly to lut addr (`dmCog`) | FMD L857–862 | ❌ treated as a "memory" cell instead |
| 3 | **PC box** → return to follow-PC (`dmPC`) | FMD L863–865 | ❌ no PC hit region |
| 4 | **SFR value** → nav disasm (IJMP3..IRET1) / hub (PA/PB/PTRA/PTRB) | FMD L893–908 | ❌ no SFR hit region |
| 5 | **Stack value** → nav disasm/hub from the value as a pointer | FMD L909–924 | ❌ no stack hit region |
| 6 | **Event name** → set EVENT-break target (`BreakEvent`) | FMD L826–840 | ❌ no event hit region (makes EVENT breakpoints hard to aim) |
| 7 | **Pointer box** (FPTR/PTRA/PTRB addr/data/chr) → jump hub | FMD L925–946 | ❌ no ptr hit region |
| 8 | **Hub data / ASCII** click → jump hub viewer to addr | FMD L955–966 | ⚠️ hit region exists but only sets an internal `selectedAddress`; does not move the hub viewer base (`HubAddr`) |
| 9 | **Hub heatmap** click → jump hub viewer | FMD L967–969 | ❌ no hub-map hit region |
| 10 | **SMART pin watch** box: L=reset, R=toggle DIR filter | FMD L947–954 | ❌ no smart-watch hit region |
| 11 | **WATCH box** click → reset reg-watch list | FMD L890–892 | ⚠️ hit region returns fabricated names and only marks dirty; **does not reset** (only the `R` key resets) |

Also note **the address-digit wheel** (`FormMouseWheel` InHubAddr, L1004–1006): wheeling
over the hub address digits changes the individual hex nibble under the cursor.
TS `handleMouseWheel` only handles disassembly/hub-box/stack focus — ❌ nibble
editing is missing.

## B.5 Hover hint bar — ❌ not wired

Pascal updates the hint bar on **every** `FormMouseMove`. In TS,
`handleMouseMove` exists (`debuggerInteraction.ts` L278–295) but **no
`mousemove` listener is attached to the canvas** (the renderer only wires
`resize`, `keydown`, `click`, `wheel`). Result: the context-sensitive hint bar
described in A.5/A.7 is effectively **non-functional**. **Fix**: add a
`mousemove` IPC bridge and route it to `handleMouseMove`.

## B.6 Disassembly left/right-click — ✅ parity (verified)

Initially suspected inverted, but the Pascal source confirms TS is correct:
`FormMouseDown` InDis branch is `if LB then DisMode := dmPC` (left-click =
follow-PC) and right-click toggles an address breakpoint at the clicked line
(L866–889). TS matches exactly (`debuggerInteraction.ts` L254–263). The `dmCog`
lock comes from the separate REG/LUT **map** regions (B.4 #1/#2), and the PC box
also forces `dmPC` (B.4 #3) — both still to be wired, but the disassembly click
itself needs no change.

## B.7 TS-only inventions not in Pascal — ➕ should be removed

These exist in TS but have **no counterpart** in Pascal, and are stubs that only
log. They also contradict the read-only nature of the debugger and would mislead
users:

| TS behavior | Where | Issue |
|---|---|---|
| Double-click register/memory → "edit dialog" | `handleMouseClick` L239–251, `editMemory`/`editRegister` L673–681 | Pascal has no editing; debugger is read-only. Remove. |
| Click pin → `togglePin` | L266–268, L712–716 | Pascal pins are display-only; no pin hit region exists there. Remove. |
| Stack **wheel** scroll | `handleMouseWheel` `case 'stack'` L333–335 | Pascal has no stack wheel behavior. Remove. |

## B.8 Documentation note

The existing `DOCs/DEBUGGER-USER-MANUAL.md` describes the full Pascal mouse model
(REG/LUT/PC/SFR/stack/event/ptr/hub-map clicks, hover hints) as if present. Per
B.4–B.5 most of that is **not yet implemented in TypeScript**. Until the gaps are
closed, that manual reads as a spec, not as current behavior. **Part A above is
written to the Pascal spec** (the target); treat **Part B** as the punch list of
what must be built for Part A to be fully true of the TS build.

## B.9 Suggested work order (smallest → largest)

1. Wire `disassemblyScroll`, currently a no-op TODO at `debugDebuggerWin.ts` L766
   — wheel-scrolling the disassembly does nothing yet (B.3).
2. Add the REG/LUT-map → `dmCog` lock and the PC-box → `dmPC` regions (B.4 #1,2,3).
3. Add the remaining click hit-regions (B.4 #4,5,6,7,9,10) — pure hit-test plus a
   `HubAddr`/`CogAddr`/`BreakEvent` setter each; the protocol fields already exist.
4. Correct WATCH-box reset and hub-data click; add the address-nibble wheel (B.4 #8,11 + nibble note).
5. Wire `mousemove` → hint bar (B.5).
6. Remove the non-Pascal edit/pin/stack-wheel stubs (B.7).

---

*Verified against `DebuggerUnit.pas` (v51a tree) and the current TypeScript
sources, 2026-05-31. Pascal references use `FMD` = `FormMouseDown`.*
