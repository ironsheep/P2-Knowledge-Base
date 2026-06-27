# AN013 — Menus and Messaging with the Propeller Window Manager Framework (WMF)

**Curated reference extraction** · Parallax Semiconductor Application Note **AN013**, *GUI &
Graphics Series*, v1.0, © 2011 · 49 pages · Propeller 1 (P8X32A), Spin1 + PASM1.

> Companion to **AN004** (Getting Started with VGA and Terminal Output) and **AN005** (Simple
> VGA Menus). This note is the advanced GUI tutorial in the series: data-driven controls
> (menus + buttons), an event/message queue, and real-world event handlers.

---

## Document structure (as authored)

The note teaches **top-down then drill-down**: it opens with the GUI/event-driven philosophy,
establishes the object & data-flow model, then walks each control type (button → hotbar →
hotlist), builds a reusable application template, presents four worked demos of escalating
complexity, and closes with a formal treatment of message/event handling plus a full API
listing.

1. **Introduction** — why GUI programming is a *design* process; microcontroller constraints;
   the event-driven model (à la Windows/OS X/Android) and its ROI for the app programmer.
2. **Architectural Concepts for the WMF** — WMF is a single Spin object
   (`WMF_Framework_010.spin`); a **text-based** GUI (not bitmapped) on an 800×600 / 8×12-font
   VGA screen = 100×50 chars (Fig 1). Object model (Fig 2): `User_App → WMF_Framework →
   {VGA, Mouse, Keyboard}`.
3. **Understanding Controls and Events** — the two user-app responsibilities: (a) create
   controls via DAT data statements + attach them; (b) process messages from the event queue
   and call handlers. "Control" = anything the user interacts with; WMF supports two
   (**menus** and **buttons**). Data-flow model (Fig 3).
4. **Creating Controls** — active vs static GUI elements; static rendering via `PrintString`
   and `DrawFrame` (Fig 4 multi-control demo).
5. **Creating Button Controls** — the 6 button fields (Fig 5); binary DAT format; attribute
   flags; style/state flags; IDs; `AttachButton` (Fig 6).
6. **Creating Menu Controls** — two menu kinds: **HotBar** (horizontal, Fig 7) and **HotList**
   (vertical, Fig 9); both send the same messages, share processing code.
7. **Declaring HotBar Menus** — 7-byte header, width formula, item list, `AttachMenu` (Fig 8).
8. **Declaring HotList Menus** — nearly identical to hotbar; simpler width = MAX(title,
   item)+borders (Fig 10).
9. **Attaching Controls to WMF** — `AttachButton`/`DetachButton`/`DrawButton`;
   `AttachMenu`/`DetachMenu`/`DrawHotMenu`; `NUM_MENUBARS=8`, `NUM_BUTTONS=16`,
   `NUM_MESSAGES=16` limits.
10. **Building a Generic User Application Template** — the `CreateAppGUI` + main-event-loop
    pattern all demos follow (Fig 11).
11. **The Main Event Loop / The Messaging API** — `ProcessGUI`, `GetNumMessages`,
    `GetMessage`; message format `WORD = [id:8 | code:8]`.
12. **WMF GUI Examples** — four demos (below).
13. **Processing Messages and Events** — formal event-handler model (Fig 17), routing by ID
    range, handler-writing guidelines.
14. **Summary · API Listing · Resources · References · Revision History**.

---

## Core architecture (key facts)

- **WMF = one Spin object** (`WMF_Framework_010.spin`) exposing terminal text, direct
  rendering, drawing, keyboard/mouse interfaces, and the menu/button controls. It encapsulates
  everything except the VGA/mouse/keyboard drivers it includes.
- **Text-based GUI:** box-drawing ASCII characters draw lines/boxes/borders/shadows. VGA is
  800×600, each char 8×12 px ⇒ **100×50 character screen** (configurable in the VGA driver).
- **Single-cog GUI:** the WMF runs in one cog; an event handler that does heavy work *starves*
  `ProcessGUI`, so handlers must return quickly (or spawn another cog).
- **Data-driven controls:** controls are declared as **DAT byte records**, not method calls —
  "Programmers familiar with XML … will feel at home."
- **Message queue** (`gMsgQueue[NUM_MESSAGES]`, head/tail/num) is the sole link between WMF
  (producer) and the user app (consumer). The app's *entire view* of the GUI is the messages
  it receives.

### Two control classes
- **Static** (window dressing): text, frames, boxes — drawn via API calls (`PrintString`,
  `DrawFrame`), no interaction.
- **Active** (interactive): **buttons** and **menus** — must be declared *and* attached so WMF
  renders + processes them.

---

## Buttons (the simple control)

Six fields (Fig 5): type · render attributes · (x,y) · state · id · label string (NUL-term).

```
button1    LONG                                  ' long-align (pointer-arithmetic safety)
           BYTE WMF#BUTTON_STYLE_TYPE_STANDARD   ' only type currently
           BYTE WMF#ATTR_DRAW_NORMAL
           BYTE 2, 6                             ' x,y  (width derived from string)
           BYTE WMF#BUTTON_STYLE_STATE_ACTIVE, 50, "RED",0   ' state, id, label, NUL
```

**Rendering attribute flags** (OR-able; context-sensitive "hints"):
```
ATTR_DRAW_SHADOW = $01   ATTR_DRAW_SOLID  = $02 (NI)   ATTR_DRAW_DASH = $04 (NI)
ATTR_DRAW_BORDER = $08   ATTR_DRAW_INVERSE= $10        ATTR_DRAW_NORMAL = $00
```
**Button style/state** — only two effective values: `BUTTON_STYLE_STATE_ACTIVE = $10`
(active); `GRAYED`/`DISABLED`/`INACTIVE` all `= $00` (placeholders; always use ACTIVE for now).

**ID** [1..255] (0 = NULL): convention is grouped blocks (e.g. 10–19, 50–59). Returned in the
message so the app knows which control fired. Same ID may legitimately serve two buttons.

**Attach + initial draw:**
```
button_id1 := WMF.AttachButton( 0, @button1 )      ' returns a slot "handle" (≠ your id)
WMF.DrawButton( button_id1, -1, WMF#BUTTON_DRAW_CMD_STATIC )
```
`DrawButton(pButtonId, pSelected, pCommand)` — `pCommand` `BUTTON_DRAW_CMD_STATIC=$04` /
`_DYNAMIC=$08` (OR-able) lets WMF redraw only static (border/shadow) or only dynamic parts to
save cycles. `DetachButton(id)` removes it.

---

## Menus — HotBar (horizontal) and HotList (vertical)

WMF's menus are deliberately simple: list options, hover, select, done. Both menu types send
the **same** messages and are drawn by the **same** methods (only layout + collision differ).

### HotBar — 7-byte header + item list
```
demo_hotbar_menu0 LONG
   BYTE WMF#MENU_STYLE_TYPE_HOTBAR                  ' type
   BYTE WMF#ATTR_DRAW_NORMAL | WMF#ATTR_DRAW_BORDER ' attributes
   BYTE WMF#ASCII_VLINE                             ' space-filler char between items
   BYTE 4,7,60                                      ' x, y, width
   BYTE 5                                           ' number of hot buttons
   BYTE "User Profile Tabs",0                       ' optional title
   BYTE WMF#MENU_STYLE_STATE_ACTIVE, 10, "My Profile", 0   ' style, id, label, NUL
   ...
```
**Width formula (hotbar):** `width = Σ(len of each item string) + (number of items) + 1`
(e.g. "On"+"Off" ⇒ (2+3)+2+1 = 8). Oversize/undersize intentionally for custom looks.
Separator char: use `ASCII_VLINE` (15) with borders, `ASCII_SPACE` for free-floating.

### HotList — same 7-byte header, simpler width
```
demo_hotlist_menu1 LONG
   BYTE WMF#MENU_STYLE_TYPE_HOTLIST
   BYTE WMF#ATTR_DRAW_NORMAL | WMF#ATTR_DRAW_BORDER
   BYTE WMF#ASCII_VLINE                             ' filler unused in hotlist (kept for binary compat)
   BYTE 20,7,18                                     ' x, y, width
   BYTE 4
   BYTE "Paint Colors", 0
   BYTE WMF#MENU_STYLE_STATE_ACTIVE, 20, "Forrest Green", 0
   ...
```
**Width (hotlist):** `width = MAX(title, largest item) + border padding (+2 if bordered)`.
Filler byte is ignored but retained so a record can be reused interchangeably as hotbar/hotlist.

**Menu style flags** mirror buttons: `MENU_STYLE_STATE_ACTIVE=$10`; GRAYED/DISABLED/INACTIVE
`=$00` (always ACTIVE for now).

**Box-drawing ASCII constants** (in WMF CON): `ASCII_HLINE=14 VLINE=15 TOPLT=10 TOPRT=11
TOPT=16 BOTT=17 LTT=18 RTT=19 BOTLT=12 BOTRT=13 DITHER=24 NULL=0`.

**Attach + draw** (same call for both menu kinds):
```
demo_hotlist_id0 := WMF.AttachMenu( 0, @demo_hotlist_menu0 )
WMF.DrawHotMenu( demo_hotlist_id0, -1, WMF#MENU_DRAW_CMD_MENUBAR_STATIC )
```
`DrawHotMenu(pMenuId, pSelHotButton, pCommand)` — `pSelHotButton` = item index drawn inverse
(or -1); commands `MENU_DRAW_CMD_MENUBAR_STATIC=$04` / `_DYNAMIC=$08`. `DetachMenu(id)` removes.

**Control limits:** `NUM_MENUBARS=8`, `NUM_BUTTONS=16`, `NUM_MESSAGES=16` (in
`WMF_Framework_010.spin` CON/VAR — edit to raise).

---

## The application template + main event loop

The universal pattern (Fig 11): `Start` calls `CreateAppGUI` once, then loops.

```
PUB Start | wmf_message, wmf_message_id, wmf_message_code, key, index
  CreateAppGUI                              ' build GUI once
  repeat                                    ' MAIN EVENT LOOP
    WMF.ProcessGUI                          ' give the GUI a cycle; may enqueue messages
    if ( WMF.GetNumMessages > 0 )
      wmf_message      := WMF.GetMessage
      wmf_message_code := wmf_message & $FF       ' low byte  = code
      wmf_message_id   := (wmf_message >> 8)      ' high byte = control id
      ... handle / print ...
```

`CreateAppGUI` (one-time): `WMF.Init(VGA_BASE_PIN, MOUSE_DATA_PIN, MOUSE_CLK_PIN, KBD_DATA_PIN,
KBD_CLK_PIN, WMF#NULL)` returns packed geometry+buffer (`rows=hi8`, `cols=lo8`,
`videoBuffer=retVal>>16`); then `ClearScreen(fg,bg)`, draw static elements, attach + initial-
draw all controls.

**Message format:** `WORD = [message_id:8 | message_code:8]`.

**Menu message** (single, only on click-and-release on the same item):
`WMF_MSG_MENU_BUTTON_CLICKED = $08`.

**Button messages** (rich — buttons emit many; drain the queue every loop or it overflows):
```
WMF_MSG_BUTTON_CLICKED  = $10   ' full press+release cycle
WMF_MSG_BUTTON_PRESSED  = $11
WMF_MSG_BUTTON_RELEASED = $12
WMF_MSG_BUTTON_ONFOCUS  = $13   ' hover-over
WMF_MSG_BUTTON_LOSTFOCUS= $14   ' hover-off
```
Filtering example (ButtonDemo2): only act on `..._MENU_BUTTON_CLICKED` OR `..._BUTTON_CLICKED`
— but always read every message out regardless, to prevent overflow.

---

## The four demos

| # | Demo | Teaches |
|---|------|---------|
| 1 | **ButtonDemo** (`WMF_ButtonDemo_010`) | 3 button-attribute variants + 12-button "pPhone" keypad matrix built by a pointer-arithmetic loop over equal-size button records; floods messages. ButtonDemo2 adds a click-only filter. |
| 2 | **HotBarMenuDemo** (`WMF_HotBarMenuDemo_010`) | 4 corner hotbars (all border/title/shadow permutations); pretty-prints into a "Message Box" static frame; integrates keyboard pass-through into a "User Input Box". |
| 3 | **HotListMenuDemo** (`WMF_HotListMenuDemo_010`) | 3 vertical hotlists; same loop, just hotlist DAT records. |
| 4 | **MultiControlDemo** (`WMF_MultiControlDemo_010`) | **Capstone**: LED-Control hotbar (IDs 10–19), Motor-Speed hotlist (IDs 30–36), pPhone keypad matrix (IDs 61–74); routes by ID range to `LED_MessageHandler` / `Motor_MessageHandler` / `Phone_MessageHandler` which drive **real hardware** — LEDs, a PWM DC motor, and DTMF tones. |

### Demo hardware (P1)
- **Propeller Demo Board Rev C** (#32100), 5 MHz crystal (`_clkmode = xtal1 + pll16x`,
  `_xinfreq = 5_000_000`).
- VGA pins 16–23; mouse data/clk 24/25; keyboard data/clk 26/27.
- MultiControl extras: 4 LEDs on P1–P4 (100–330 Ω series); DC motor 3–6 V/100–200 mA on a
  2N2222/2N3904 NPN switch + 1N4001 flyback diode + storage cap (`DC_MOTOR_PIN=6`); audio out
  `AUDIO_PIN=10` (demo board built-in WMF filter; R1‖C1 low-pass ≈ 21.2 kHz for boards lacking it).

### Event-handler guidelines (closing section)
- Handlers starve `ProcessGUI` (single cog) — be quick or spawn a cog.
- Always provide a default catch-all (robustness against unexpected code/ID).
- Beware GUI mutation across chained handlers in one loop iteration.
- `FlushMessages` clears the queue; `PostMessage` injects synthetic events (e.g. macro replay).

---

## Full API surface (`WMF_Framework_010.spin`)

- **Init:** `Init(pVGABasePin, pMouseDataPin, pMouseClkPin, pKeyboardDataPin, pKeyboardClkPin,
  pBackBufferPtr)`.
- **Queue:** `PostMessage`, `GetMessage`, `PeekMessage`, `GetNumMessages`, `FlushMessages`.
- **GUI/window:** `ProcessGUI`, `AttachButton`/`DetachButton`/`DrawButton`/`ProcessButtons`,
  `AttachMenu`/`DetachMenu`/`ProcessMenus`/`DrawHotMenu`.
- **Direct frame buffer:** `PrintString`, `PrintChar`, `ClearScreen`, `SetLineColor`,
  `DrawFrame`.
- **Mouse/keyboard pass-through:** `GetMouseXYButtons`, `KeyboardPresent`, `KeyboardKey`,
  `KeyboardGetKey`, `KeyboardNewKey`, `KeyboardGotKey`, `KeyboardClearKeys`, `KeyboardKeystate`.
- **Terminal:** `StringTermLn`, `StringTerm`, `DecTerm`, `HexTerm`, `BinTerm`, `NewlineTerm`,
  `PrintTerm`, `OutTerm`, `SetColTerm`, `SetRowTerm`, `GotoXYTerm`, `GetColTerm`, `GetRowTerm`.
- **String/numeric:** `StrCpy`, `StrUpper`, `ToUpper`, `IsInSet`, `IsSpace`, `IsNull`,
  `IsDigit`, `IsAlpha`, `IsPunc`, `HexToDec`, `HexToASCII`, `itoa`, `atoi`.
- **Time:** `DelayMilliSec`, `DelayMicroSec`.

---

## Voice & structure profile (for the downstream P2 app-note style guide)

- **Voice:** warm, conversational, second-person mentor ("let's discuss," "no one gets off easy
  with menus," "It's actually fun and highly recommended," "launch missiles"). Self-deprecating
  asides and humor ("for better or for worst :)", "AREA51 for testing methods"). Confident but
  never terse.
- **Pedagogy:** *philosophy-first* — establishes the **why** (event-driven design as a creative
  process) before the **how**. Heavy use of **deliberate reiteration** ("This concept is very
  important, so let's reiterate…") and progressively-refined bullet lists of the same loop.
- **Structure:** top-down architecture → drill-down per control → reusable template →
  escalating worked demos (template → buttons → hotbar → hotlist → capstone multi-control) →
  formalized theory *after* concrete demos (deliberately deferred "so you had as much context as
  possible") → API appendix.
- **Code-walk style:** show a stripped/commented DAT or PUB excerpt, then narrate it
  line-by-line; emphasize "this is only ~12 lines of real work code" to sell the framework's ROI.
  Uses an explicit `←` continuation glyph for wrapped code lines.
- **Figures:** every concept paired with either an annotated **diagram** (anatomy of a
  button/hotbar/hotlist; data-flow + event-handling models) or a **screenshot** of the running
  demo; one hardware **photo** for the real-world capstone.
- **Recurring devices:** numbered ID-block conventions; "static vs active" framing; the
  producer/consumer queue metaphor ("eyes and ears of the application"); hardware hookup shown as
  inline ASCII schematics inside `{{ }}` doc-comment blocks.

---

*Raw layout-preserving text: `AN013-WMF-Menus-text.txt`. Code: `assets/code-2026-06-27/`
(12 files, capture-only, `code_validated:false`). Images: `assets/images-…-2026-06-27/`
(26 fragments / 17 figures).*
