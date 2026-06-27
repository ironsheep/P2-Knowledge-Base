# AN004 — Code Catalog (pass 2: CAPTURE + CATALOG ONLY)

**Validation status: `code_validated: false` — NOT compiled.** Per the P1 ingestion charter
§3, P1 code cannot be machine-validated here: `pnut_ts` is **P2-only**, and a P1 compiler
(flexspin / Propeller Tool / openspin) is **not installed** in this container. These 7 files
are captured **verbatim** and cataloged; they are NOT compile-verified.

- **Source:** companion ZIP from `www.parallaxsemiconductor.com/an004`, supplied alongside
  the PDF in `sources/P1-App-Notes/AN004-GUI-StartVGA/AN004-GUI-StartVGA-Code-v1.0/`.
- **Copied to:** `assets/code-2026-06-27/` (byte-for-byte; original mtimes preserved).
- **Encoding note:** all 7 files are **UTF-16 LE with CRLF** (BOM present) — the Propeller
  Tool's native save format of the era. Any downstream P1 tooling must read UTF-16, not
  assume UTF-8/ASCII.
- **Language:** Spin1 (top-level + terminal driver) with inline **PASM1** cogcode in the
  video/keyboard/mouse drivers. **No P2 constructs** (no smart pins, streamer, CORDIC).

## Object hierarchy (build graph)

```
WMF_HelloWorld_010      ┐
WMF_GuessMyNumber_010   ├─ (top-level demo; pick ONE as the compile root)
WMF_ColorThemeDemo_010  ┘
   │  OBJ WMF   = WMF_Terminal_Services_010
   │  OBJ kbd   = Keyboard_011
   │  OBJ mouse = Mouse_011
   │
   └─ WMF_Terminal_Services_010   (terminal/console framework driver)
          └─ OBJ vga = VGA_HiRes_Text_010   (raw VGA text-mode video driver; PASM1)

Keyboard_011   (leaf PASM1 driver, no sub-objects)
Mouse_011      (leaf PASM1 driver, no sub-objects)
```

Each of the three demos is an **independent top-level program** that pulls in the same three
drivers; they are alternative roots, not a single combined build.

## Per-file catalog

| File | LOC | Role | Author / origin | OBJ deps |
|---|---:|---|---|---|
| `WMF_HelloWorld_010.spin` | 334 | **Top-level demo** (Example 1) | André LaMothe / Parallax, 2011 | WMF, kbd, mouse |
| `WMF_GuessMyNumber_010.spin` | 376 | **Top-level demo** (Example 2) | André LaMothe / Parallax, 2011 | WMF, kbd, mouse |
| `WMF_ColorThemeDemo_010.spin` | 463 | **Top-level demo** (Example 3) | André LaMothe / Parallax, 2011 | WMF, kbd, mouse |
| `WMF_Terminal_Services_010.spin` | 1177 | **Framework driver** — terminal/console + frame-buffer rendering + string/numeric conversion + delays; the note's API-listing object | André LaMothe / Parallax, 2011 | vga |
| `VGA_HiRes_Text_010.spin` | 541 | **Reused OBEX driver** — VGA hi-res text-mode video generator (PASM1 cog video) | **Chip Gracey / Parallax, 2006** | none |
| `Keyboard_011.spin` | 735 | **Reused OBEX driver** — PS/2 keyboard driver v1.0.1 (PASM1) | **Chip Gracey / Parallax, 2004–06** | none |
| `Mouse_011.spin` | 491 | **Reused OBEX driver** — PS/2 mouse driver v1.1 (PASM1) | **Chip Gracey / Parallax, 2006** | none |

**Reused stock drivers:** `VGA_HiRes_Text_010`, `Keyboard_011`, and `Mouse_011` are the
classic Parallax-internal / OBEX P1 driver objects (Chip Gracey), reused unmodified — exactly
the "tested, well-understood stock driver" choice the note's Introduction argues for. The
**WMF_*** files (terminal services + the three demos) are the new material authored by André
LaMothe for this app-note series.

## What each demo demonstrates

- **WMF_HelloWorld_010** — the minimal VGA+terminal bring-up and the **recommended GUI
  software pattern**: `CreateAppGUI` init (start mouse/keyboard/VGA, bind cursor globals,
  clear screen to a theme) then an **infinite main event loop** that reads mouse globals and
  prints a scrolling string. Teaches `WMF.Init` bit-packed return, `child#const` syntax.
- **WMF_GuessMyNumber_010** — **keyboard text input**: a local single-line editor
  (`GetStringTerm`, handling CR/LF/backspace), `WMF.atoi` string→int, and **pin-noise RNG
  seeding** feeding Spin1's `?` LFSR operator (`||(?gRandSeed // 100)`).
- **WMF_ColorThemeDemo_010** — selecting among the driver's predefined 2-color **`CTHEME_*`
  schemes** by keyboard; backdrop for the note's GUI color-design guidance.

## Verification debt (for a later dedicated P1 code pass)

- **Not compiled** — when a P1 toolchain is available, compile each of the 3 demo roots
  (each pulls the 4 shared drivers) and record pass/fail.
- Confirm the pin-group `CON` constants and the **5 MHz crystal** assumption noted in the
  PDF match each demo's `CON` block.
