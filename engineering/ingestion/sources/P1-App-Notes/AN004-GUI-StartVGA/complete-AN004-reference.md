# AN004 — GUI & Graphics Series: Getting Started with VGA and Terminal Output

> **Curated reference extraction** (pass 1). Source: `AN004-GUI-StartVGA-v1.0.pdf`
> (Parallax Semiconductor Application Note AN004, 16 pp., © 2011 Parallax, Inc.).
> **Platform: Propeller 1 (P8X32A)** — Spin1 + PASM1, 8 cogs, per-cog video generator
> driving VGA. Text layer clean (no OCR needed). Prose structure, headings, and tutorial
> voice are preserved verbatim-in-spirit below for the downstream P2 app-note style guide.

---

## Document metadata

| Field | Value |
|---|---|
| Title | GUI & Graphics Series — Getting Started with VGA and Terminal Output |
| Series | GUI & Graphics Series (this is the **first** tutorial in the series) |
| Doc # | AN004, v1.0 |
| Publisher | Parallax Semiconductor (Parallax, Inc.) |
| Year | 2011 |
| Target chip | Propeller **P8X32A** (Propeller 1) |
| Language | Spin1 (top-level + terminal driver); PASM1 (video/keyboard/mouse drivers) |
| Companion code | 7 `.spin` files (ZIP from `www.parallaxsemiconductor.com/an004`) |
| Figures | 7 (3 line diagrams + 4 VGA screenshots; Fig 7 = 9 color-theme thumbnails) |

---

## Abstract (as published)

> Each of the multicore P8X32A's eight cogs includes a video generator. This first tutorial
> in the GUI & Graphics series covers basic VGA character graphics, console terminals,
> mousing and simple text input with the Propeller P8X32A microcontroller. Example demos
> make use of available drivers to illustrate how effortless it can be to implement a simple
> VGA terminal application.

---

## Document structure (headings, in order)

1. **Introduction** — the Propeller's software-defined-peripheral philosophy; why pick a "stock" VGA driver
2. **The VGA Driver Features in Detail** — `ScreenPtr` / `ColorPtr` / `CursorPtr` interface
3. **Terminal Services and Console Support** — the WMF terminal/console layer over the raw VGA driver
4. **Selecting Sub-Object Locations in the Hierarchy** — Spin1 object call-graph rules
5. **Example 1: Hello World** — `WMF_HelloWorld_010` walkthrough (init pattern + main event loop)
6. **Example 2: Text Input with "Guess My Number?"** — keyboard input, single-line editor, `atoi`, `?` RNG
7. **Example 3: The Art of Selecting Appropriate Colors** — color themes + GUI color-design guidance
8. **Summary**
9. **API Listing** — full `WMF_Terminal_Services_010` public-method catalog
10. **Resources / References / Revision History**

---

## 1. Introduction — the software-defined-peripheral thesis

The note opens on the Propeller's defining idea: peripherals (RS-232, SPI, I2C, **VGA
generation**, sound, keyboard, mouse) are implemented as **software drivers loaded at run
time**, not fixed hardware. The author frames this freedom as *also* the chip's biggest
challenge — "There is no 'correct' way to do something" — and uses that to motivate choosing
a tested, widely-used "stock" driver rather than hunting the Object Exchange for the newest one.

The chosen driver: **VGA High Res Text Driver**, version 1.0 = `VGA_HiRes_Text_010.spin`.
Stated features:

- Multiple resolutions: 640×480, 800×600, 1024×768
- 2 unique colors per row
- Requires only 2 cogs to run
- "Very short, only a couple hundred lines of assembly language"
- Simple control interface: pointer to character memory + color words
- Clean classic 8×12-pixel "IBM PC"-style console font
- Two independent screen cursors (mousing / text-input tracking)

## 2. The VGA driver interface in detail

The driver knows nothing about text, strings, consoles, or input — **its single job is to
render a screen matrix from a buffer you provide.** Matrix max size = 128 cols × 64 rows
(128×64) = 8192 bytes for 1024×768. Worked example: 800×600 with an 8×12 font →
800/8 × 600/12 = **100×50 characters**, ≈ 5 KB (illustrated by **Figure 1**).

All interfacing is via three pointers:

- **`ScreenPtr`** — up to 8192 ASCII bytes, one per cell, laid out left-to-right /
  top-to-bottom. Resolution → grid: 640×480 = 80×40, 800×600 = 100×50, 1024×768 = 128×64.
  Each byte's **MSB = inverse-video flag**, lower 7 bits = ASCII. e.g. "A" = 64 =
  `%0_1000001`; set MSB → `%1_1000001` draws reversed ("inverse video").
- **`ColorPtr`** — up to 64 words, one per text row. Low byte = foreground RGB, high byte =
  background RGB. RGB is **2-bits-per-channel**: `%RRGGBB00` = RGB[2:2:2:0] (low 2 bits
  always 0). 4 levels/channel → 4·4·4 = **64 colors**. e.g. `%%0020_3300` = yellow on blue.
- **`CursorPtr`** — 6 contiguous bytes controlling **two overlay cursors** drawn on top of
  the text. Bytes 0,1,2 = Cx,Cy,MODE of cursor 0; bytes 3,4,5 = cursor 1. Cx,Cy are in
  **character** units, not pixels. MODE uses only the low 3 bits:

  | MODE bits | Meaning |
  |---|---|
  | `%x00` | cursor off |
  | `%x01` | cursor on |
  | `%x10` | cursor on, blink slow |
  | `%x11` | cursor on, blink fast |
  | `%0xx` | cursor is solid block |
  | `%1xx` | cursor is underscore |

  e.g. `(0, 0, %011)` = upper-corner solid block, blinking fast.

## 3. Terminal Services and Console Support

With the raw VGA driver in hand, the note builds a **terminal/console** layer that mimics
PC "standard out" (print, wrap, scroll), like C/BASIC print or a VT-100. Rather than bolt an
OBEX terminal onto the VGA driver, the author wrote one **from scratch** for the series —
`WMF_Terminal_Services_010.spin` — to be "a framework to build upon." Features:

- Direct character/text printing to VGA screen memory (high-speed path)
- Terminal emulation: chars, strings, numbers (hex/dec/bin), wrap, scroll
- Complex rendering: shadowed boxes, frames, outlines (for buttons, lists, menus, GUI objects)
- Number conversion + string/char manipulation emulating Unix C lib (`atoi()`, `itoa()`,
  `strupper()`, …)
- Simple time-delay methods

**The "WMF" prefix = Propeller "Window Manager Framework"** — the series' label for
graphics/window/GUI modules. **Figure 2** shows the component stack; per the figure, every
app has a **top-level file** that instantiates the terminal-services driver plus the mouse and
keyboard drivers, and the **terminal-services driver itself includes the VGA driver.**

## 4. Selecting Sub-Object Locations in the Hierarchy (Spin1 object rules)

A teaching aside on **Spin1's object call-graph constraints**: Spin does **not** allow direct
communication between child objects, and a child cannot call a parent's methods. So the
top-level app cannot call the VGA driver directly (the terminal driver instantiates it) — a
pass-through interface layer would be required. **Figure 3** illustrates the legal-call rules:
a parent can call its children's methods, but **siblings can't call each other** and a parent
**can't call through to grandchildren**.

Practical consequence the author draws: it is *cleaner* abstraction-wise to nest mouse and
keyboard inside terminal services, but that would force pass-through methods, so for now the
mouse and keyboard are **"dragged up" to the application level** and instantiated directly —
state is passed downward. (Voice note: the author repeatedly surfaces design *tradeoffs* and
defers the cleaner abstraction to "later," teaching pragmatism over purity.)

## 5. Example 1: Hello World (`WMF_HelloWorld_010`)

Setup boilerplate stated for **every** demo: needs a Propeller dev board with VGA + PS/2
mouse + keyboard; change the VGA/mouse/keyboard base pin groups in the `CON` block; source
assumes a **5 MHz crystal** (change as needed). **Figure 4** = the output on an 800×600 /
100×50 VGA LCD TV.

> **Tip (sidebar):** rather than buying an LCD monitor, use an LCD TV — most support at
> least 1280×768, and you get a tuner too.

The demo's `PUB Start` establishes the **recommended GUI software pattern**: call an init
method (`CreateAppGUI`), then enter an **infinite main event loop** that reads user input
(mouse/keyboard globals `gMouseCurs*`), prints to the terminal, repeats:

```spin
PUB Start
  CreateAppGUI                       ' first step: create the GUI itself
  repeat                             ' MAIN EVENT LOOP
    gMouseCursX := mouse.bound_x
    gMouseCursY := mouse.bound_y
    gMouseButtons := mouse.buttons
    WMF.StringTerm(string("Hello World! from the Propeller ..."))
    WMF.DelayMilliSec( 10 )          ' slow it down so you can see it
```

`CreateAppGUI` does the static init: set text-cursor pos + mode (`%110` = blinking
underscore), set mouse-cursor pos + mode (`%001` = solid block), `mouse.start`,
`mouse.bound_limits` / `bound_scales` (note: a negative 2nd scale **inverts the axis**) /
`bound_preset`, `kbd.start`, then **`WMF.Init(VGA_BASE_PIN, @gTextCursX)`**. Init binds the
VGA base pin group **and the base address of the cursor globals** — "whatever happens to the
globals in the top-level object is reflected almost instantly in the VGA driver's cursor
rendering code" (a deliberate memory-passing interface chosen over per-update method calls).

`Init`'s return value is bit-packed: rows in `[15:8]`, cols in `[7:0]`, video buffer pointer in
`[31:16]`. Finally `WMF.ClearScreen(PWM#CTHEME_ATARI_C64_FG, PWM#CTHEME_ATARI_C64_BG)`
(classic Atari/C64 white-on-blue). **Teaching aside:** the `child_object#constant_name`
syntax (`PWM#CTHEME_...`) pulls a constant from a child object without re-defining it locally.
Per-row recolor is `SetLineColor(pRow, pFG, pBG)`.

## 6. Example 2: Text Input — "Guess My Number?" (`WMF_GuessMyNumber_010`)

Illustrates **keyboard text input** — framed as "a challenging part of programming" because
there are no built-in input commands; you must write the single-line editor yourself. Reuses
the Hello-World template; computes a random number; loops reading guesses and tests
high/low/correct.

**RNG seeding teaching moment:** Spin1's pseudo-random operator is **`?`** (LFSR-based;
`?x` = forward-shift, `x?` = reverse-shift; "refer to Propeller Reference Manual pg. 159").
Because a fixed seed gives a fixed sequence, the demo seeds from **noise on the I/O pins**:

```spin
repeat index from 0 to 1024
  gRandSeed += INA          ' sum random noise on all 32 I/O lines
```

Then `randNumber := 1 + ||(?gRandSeed // 100)` (`||` = absolute value, `?` = LFSR step).

Two input methods carry the lesson: **`GetStringTerm(@gStrBuff1, 4)`** (gets input, caps
length) and **`WMF.atoi(@gStrBuff1, 4)`** (C/Unix-style ASCII→int; supports `%` binary,
`$` hex, decimal default). `atoi` lives in the terminal driver; `GetStringTerm` is kept
**local** because it needs the locally-instantiated keyboard. The listed `GetStringTerm` is a
**single-line editor**: draws an underscore cursor, waits on `kbd.gotkey`, `case`s on the key —
`ASCII_LF/CR` → null-terminate + return; `ASCII_BS/DEL/LEFT` → backspace edit (emit
space + `$08` backspace bytes); other → store char, echo, bump length. (Voice: the author
explicitly notes a richer editor — arrow keys, copy/paste — "would take a lot more code,
buffers, and state machines," again teaching scope discipline.)

## 7. Example 3: The Art of Selecting Appropriate Colors (`WMF_ColorThemeDemo`)

Uses the keyboard to pick a color scheme by number; the theme updates slowly. The note
spends most of its space on **GUI color-design guidance** ("entire books written about… it's a
complex field"). The driver ships predefined 2-color schemes as constant pairs, e.g.:

```spin
CTHEME_WHITENBLACK_FG      = %%333   ' white-on-black, DOS/CMD console look
CTHEME_WHITENBLACK_BG      = %%000
CTHEME_WHITENBLACK_INFO_FG = %%000
CTHEME_WHITENBLACK_INFO_BG = %%333
```

**Figure 7** shows nine predefined themes: `CTHEME_WHITENBLACK`, `CTHEME_BLACKNWHITE`,
`CTHEME_ATARI_C64`, `CTHEME_APPLE2`, `CTHEME_WASP`, `CTHEME_AUTUMN`, `CTHEME_CREAMSICLE`,
`CTHEME_ORCHID`, `CTHEME_GREMLIN`.

Color-design guidelines (paraphrased list): never red+blue together; avoid weak contrast
(grey on white); match colors to the application; pastels for friendly GUIs; solid backgrounds
for info display; energetic backgrounds grab attention but tire the eyes; **darker backgrounds
+ brighter foreground reduce eye strain** (screens emit, paper reflects); don't use your
favorites; test on real people; when in doubt use black/white, white/black, white-on-dark-blue,
or green/red-on-black for a retro-terminal feel. Closing note on info-bars: use inverse or
complementary colors for distinct vertical regions.

## 8. Summary

Recaps the delivered framework: terminal services + display driver for VGA textual apps,
keyboard input, and color selection / GUI color-design art.

## 9. API Listing — `WMF_Terminal_Services_010.spin` public methods

> "Look to the source code for more details and complete parameter descriptions."

**Initialization**
- `Init(pVGABasePin, pTextCursXPtr)` — init VGA driver + basic terminal params.

**Direct frame-buffer rendering (console + controls)**
- `PrintString(pStrPtr, pCol, pRow, pInvFlag)` — string straight to frame buffer.
- `PrintChar(pChar, pCol, pRow, pInvFlag)` — char straight to frame buffer (bypasses terminal).
- `ClearScreen(pFGroundColor, pBGroundColor)` — clear at memory-buffer level (fast).
- `SetLineColor(pRow, pFGroundColor, pBGroundColor)` — recolor one row.
- `DrawFrame(pCol, pRow, pWidth, pHeight, pTitlePtr, pAttr, pVgaPtr, pVgaWidth)` — titled,
  shadowed rectangular frame.

**Text console terminal**
- `StringTermLn(pStringPtr)` / `StringTerm(pStringPtr)` — print string (+/− newline).
- `DecTerm(pValue, pDigits)` / `HexTerm(pValue, pDigits)` / `BinTerm(pValue, pDigits)` — numeric print.
- `NewlineTerm` — home cursor + carriage return.
- `PrintTerm(pChar)` — print char with scrolling.
- `OutTerm(pChar)` — primary client→driver char interface in "terminal mode."
- `SetColTerm(pCol)` / `SetRowTerm(pRow)` / `GotoXYTerm(pCol, pRow)` — set cursor position.
- `GetColTerm` / `GetRowTerm` — read cursor position.

**String & numeric conversion**
- `StrCpy(pDestStrPtr, pSourceStrPtr)` — copy NUL-terminated string.
- `StrUpper(pStringPtr)` / `ToUpper(pChar)` — uppercase string / char.
- `IsInSet(pChar, pSetStringPtr)` / `IsSpace` / `IsNull` / `IsDigit` / `IsAlpha` / `IsPunc` — char tests.
- `HexToDec(pChar)` / `HexToASCII(pValue)` — hex digit conversions.
- `itoa(pNumber, pBase, pDigits, pStringPtr)` — int→string (dec/hex/bin).
- `atoi(pStringPtr, pLength)` — string→int (supports `%` bin, `$` hex, decimal default).

**Time**
- `DelayMilliSec(pTime)` / `DelayMicroSec(pTime)` — blocking delays.

## 10. Resources / References / Revision History

- **Resources:** example Spin objects ZIP from `www.parallaxsemiconductor.com/an004`
  (the 7 `.spin` files — see code-catalog).
- **References:** [1] Propeller Object Exchange — `http://obex.parallax.com`
- **Revision History:** Version 1.0 — original document.

---

## Voice & structure profile (for the P2 app-note style guide)

- **Genre:** hands-on **tutorial** app-note, not a reference spec. Reference material (the
  API listing) is deferred to the *end*; the body is a guided build.
- **Arc:** *philosophy → driver internals → framework layer → three escalating worked
  examples (Hello World → text input → color/aesthetics) → summary → API appendix.* Each
  example reuses the previous example's template, explicitly ("uses the template from the
  previous demo"), so complexity ramps without restarting.
- **Voice:** second-person, conversational, encouraging ("Have fun!", "it's up to you",
  "you get the idea"). Uses scare-quotes for informal terms ("stock", "drag", "standard out").
- **Pedagogy:** repeatedly surfaces **design tradeoffs** rather than dictating one answer
  (Spin1 hierarchy decisions; "you may want to push GetStringTerm down into the driver
  later"); teaches *scope discipline* (explicitly declines to build the fancier editor and
  says why). Inserts **teaching asides** on language features encountered in passing
  (`child#const` syntax, the `?` LFSR operator, `||` abs-value, bit-packed return values).
- **Reusable scaffolding the series leans on:** boilerplate setup paragraph repeated per
  example (board + pin-group + 5 MHz crystal); a figure-per-example screenshot; "WMF" =
  Window Manager Framework as a series-wide naming convention; an init-then-event-loop
  software pattern presented as *the* recommended GUI structure.
- **Sidebars:** `Tip:` and `Note:` callouts (LCD-TV tip; WMF-prefix note) — good model for
  P2 app-note callout styling.
