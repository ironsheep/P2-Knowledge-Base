# AN013 WMF Menus — Code Catalog (capture-only, NOT compiled)

**Source:** AN013 *GUI & Graphics Series — Menus and Messaging with the Propeller Window
Manager Framework* v1.0 (Parallax Semiconductor, © 2011), companion ZIP
`AN013-WMF-Menus-Code-v1.0`.
**Platform:** Propeller 1 (P8X32A), Spin1 + PASM1.
**Capture date:** 2026-06-27.

> **`code_validated: false` — no P1 compiler.** Per ingestion charter §3, P1 sources are
> CAPTURED + CATALOGED only. `pnut_ts` is P2-only and no P1 compiler (flexspin/openspin/
> bstc) is installed in this container, so none of these 12 objects were compiled. They are
> verbatim byte-for-byte copies of the Parallax-published ZIP. Spin1 `OUTA[]`, `DIRA`,
> object-constant reference syntax `OBJ#CONST`, and the `_clkmode`/`_xinfreq` CON idioms
> below are all P1-specific and will NOT compile under a P2 toolchain.

## Object dependency tree

```
WMF_TemplateDemo_010      ─┐
WMF_ButtonDemo_010        ─┤
WMF_ButtonDemo2_010       ─┼─OBJ─► WMF_Framework_010 ─OBJ─► VGA_HiRes_Text_010
WMF_HotBarMenuDemo_010    ─┤                          ├─OBJ─► Mouse_011
WMF_HotListMenuDemo_010   ─┘                          └─OBJ─► Keyboard_011
WMF_MultiControlDemo_010  ──OBJ─► WMF_Framework_010 (+ drivers above)
                            ├─OBJ─► NS_sound_drv_052_11khz_16bit   (DTMF tones)
                            └─OBJ─► pwmAsm_010                      (DC-motor PWM)
```

The 6 `WMF_*Demo` files are **top-level application objects** (each has a `PUB Start`);
the other 6 are **included driver/library objects**. The user application includes only
`WMF_Framework_010`, which transitively pulls in VGA, mouse, and keyboard — the framework
"completely insulates the application programmer" (doc, p.2). MultiControlDemo additionally
includes the sound + PWM drivers directly for its real-world event handlers.

## Per-file catalog

| File | LOC | Role | Demonstrates / contains | OBJ / include deps |
|------|----:|------|-------------------------|--------------------|
| `WMF_TemplateDemo_010.spin` | 238 | top-level demo | Minimal GUI skeleton: 1 static string + 1 button; the `CreateAppGUI` + main-event-loop software pattern reused by every demo (Fig 11) | `WMF_Framework_010` |
| `WMF_ButtonDemo_010.spin` | 359 | top-level demo | Example 1: three button-attribute variants (plain/border/border+shadow "RED/GREEN/YELLOW") + a 12-button "Parallax pPhone" keypad matrix built by pointer-arithmetic loop over equal-size button records (Fig 12) | `WMF_Framework_010` |
| `WMF_ButtonDemo2_010.spin` | 363 | top-level demo | Identical to ButtonDemo plus a single message-code FILTER (`WMF_MSG_BUTTON_CLICKED` / `WMF_MSG_MENU_BUTTON_CLICKED`) in the event loop — shows ignoring hover/focus events while still draining the queue | `WMF_Framework_010` |
| `WMF_HotBarMenuDemo_010.spin` | 354 | top-level demo | Example 2: four horizontally-oriented HotBar menus (one per screen corner) showing border/title/shadow permutations; integrates keyboard pass-through (`WMF.KeyboardKey`) printing into a static "User Input Box" frame (Fig 13) | `WMF_Framework_010` |
| `WMF_HotListMenuDemo_010.spin` | 328 | top-level demo | Example 3: three vertically-oriented HotList menus (no-title / title / title+shadow); decomposes message into a "pretty-printed" string inside a "Message Box" frame (Fig 14) | `WMF_Framework_010` |
| `WMF_MultiControlDemo_010.spin` | 706 | top-level demo (capstone) | Example 4: LED-control HotBar (IDs 10–19), Motor-speed HotList (IDs 30–36), pPhone keypad button matrix (IDs 61–74); real-world event handlers `LED_MessageHandler` / `Motor_MessageHandler` / `Phone_MessageHandler` drive LEDs, a DC motor (PWM), and DTMF tones (Figs 15–17) | `WMF_Framework_010`, `NS_sound_drv_052_11khz_16bit`, `pwmAsm_010` |
| `WMF_Framework_010.spin` | 2498 | **shared library** (included) | The entire WMF: message queue, `ProcessGUI`/`AttachButton`/`AttachMenu`/`DrawButton`/`DrawHotMenu`, direct-frame-buffer renderer (`PrintString`/`DrawFrame`), terminal console, string/numeric helpers (`itoa`/`atoi`), mouse+keyboard pass-throughs; all CON constants (`ATTR_DRAW_*`, `MENU_STYLE_*`, `BUTTON_STYLE_*`, `WMF_MSG_*`, `ASCII_*`, `CTHEME_*`) | `VGA_HiRes_Text_010`, `Mouse_011`, `Keyboard_011` |
| `VGA_HiRes_Text_010.spin` | 541 | driver (included) | 800×600 VGA text driver, 8×12 font ⇒ 100×50 char screen; the rendering surface for the whole GUI | — (PASM1 cog driver) |
| `Mouse_011.spin` | 491 | driver (included) | Standard Parallax PS/2 mouse driver (cog) | — |
| `Keyboard_011.spin` | 735 | driver (included) | Standard Parallax PS/2 keyboard driver (cog) | — |
| `NS_sound_drv_052_11khz_16bit.spin` | 1272 | driver (included by MultiControl) | HYDRA 11 kHz / 16-bit sound driver — generates the DTMF tones for the pPhone keypad | — |
| `pwmAsm_010.spin` | 139 | driver (included by MultiControl) | Simple PASM1 PWM object (based on AN001 Counters) driving the DC-motor pin | — (PASM1 counter driver) |

**Total captured:** 12 files, 6,884 LOC.

## Shared-driver note (self-containment)

Four objects — `Keyboard_011`, `Mouse_011`, `VGA_HiRes_Text_010`, `WMF_Framework_010` — are
the **same shared GUI/driver stack distributed with AN004** (Getting Started with VGA and
Terminal Output). Per ingestion convention each app note keeps **its own copy** of these
drivers so the note is self-contained; do not de-duplicate across AN004/AN013. (`pwmAsm_010`
traces to AN001 Counters; `NS_sound_drv_052_11khz_16bit` is the HYDRA sound driver, ref [5].)

## CON idioms worth noting (P1)

```
_clkmode = xtal1 + pll16x      ' P1 clock-mode CON
_xinfreq = 5_000_000           ' 5 MHz crystal assumed by all demos
VGA_BASE_PIN  = 16             ' VGA pins 16-23  (Propeller Demo Board Rev C)
MOUSE_DATA_PIN=24 MOUSE_CLK_PIN=25 KBD_DATA_PIN=26 KBD_CLK_PIN=27
```
All demos target the **Propeller Demo Board Rev C** (#32100); CON pin constants must be
edited per board. Object-constant import uses Spin1 `WMF#CONSTANT` syntax throughout.
