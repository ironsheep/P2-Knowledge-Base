# YAML Head — P2KB Dashboard

> The **YAML knowledge-base head**'s standing-state board: what shipped recently
> (release ledger) and what hardware the KB serves (inventory). The served data
> lives in `deliverables/ai/P2/`; the open to-do list is
> [`P2KB-CORRECTION-FINDINGS.md`](P2KB-CORRECTION-FINDINGS.md). This board is an
> engineering doc — the YAML never links here.
>
> **Green** = `validate-yaml-syntax.py` + `validate-crossref-keys.py` +
> `validate-dod-release.py` all pass. **Release** = two-commit Path B (content →
> regenerate index → tag the index commit). Versions are git tags
> (`--sort=version:refname`).

## Release ledger (most recent first)

| Version | Date | What & why |
|---------|------|------------|
| **v1.11.2** | 2026-06-25 | **CORDIC rotation, COGINIT, and LSTRING accuracy.** QROTATE operand mapping corrected (X from D, Y from SETQ, angle from S, results via GETQX/GETQY) data-set-wide — `architecture/cordic.yaml` `rotate` + `rotation_matrix` and the `pasm2/pi.yaml` examples (F-166). COGINIT load size 496→504 longs ($000..$1F7) (F-167). LSTRING `{Spin2_v43}` version gate documented, pnut-ts-proven (F-168). Drains the DeSilva-tutorial release-gate. |
| v1.11.1 | 2026-06-25 | PASM2 reference accuracy: GETBRK per-flag-effect reference, the program counter (CALLD/CALL return address), and signed ADD/SUB C-flag semantics. |
| v1.11.0 | 2026-06-24 | **Eval-header board model + Assembly gate-drain.** Standardized all 10 eval-header boards to one self-contained shape (`pin_group.size` 8/16 + offset→signal `signal_map` + direction + `actual = base + offset`); authored the HyperRAM/HyperFlash board (#64004-ES); folded HUB75 onto the shape; removed 4 fabricated orphan boards; one `eval_addon_boards` category. Added the RDLUT/WRLUT immediate-address contract (F-161); removed the unsourced `pin_efficiency` metric (F-160); fixed the goertzel ultrasonic-as-pinout fabrication (F-162). Drains the Assembly manual's YAML-HEAD gate. |
| v1.10.1 | 2026-06-20 | Smart Pin reference depth and language accuracy (internal-consistency batch F-141…F-158 + Silicon-backed smart-pin additions G-001/002/003). |
| v1.10.0 | 2026-06-18 | DEBUG feed idioms + smart-pin sequencing (universal Reset→Setup→Enable→Operate order). |
| v1.9.1 | 2026-06-14 | DEBUG display directive accuracy (CLOSE, SIZE, legacy debug.yaml). |
| v1.9.0 | 2026-06-13 | Smart-pin & DEBUG accuracy + hardware findability (aliases + categories). |

## Eval-header board model (the base + offset convention)

Every P2 Eval add-on board plugs into one of the Eval Board's **8-pin accessory
headers** (or, for 16-pin boards, two adjacent headers). A board never owns fixed
P2 pins — it defines its functions by **offset** within its pin group, and the
user chooses which header it occupies. So:

> **`actual_P2_pin = base_pin + offset`** — `base_pin` is the first pin of the
> chosen group (8-pin: 0, 8, 16, 24, 32, 40, 48, 56; 16-pin: 0, 16, 32, 48).

Each board YAML is self-contained and carries this directly: `eval_header_occupant:
true`, `pin_group.size` (8 or 16), and a `signal_map` of `{offset, signal,
direction, notes}`. **Direction** is the P2-side role (out/in/bidir), stated only
where the source documents it. The browse-time answer to *"what eval boards do we
know about?"* is the `eval_addon_boards` category (10 boards).

## Known-hardware inventory

### Eval-header occupants (`eval_addon_boards` category)

| Part # | Board | Pins | Status |
|--------|-------|------|--------|
| 64006A | Control (4 LEDs + 4 buttons) | 8 | active |
| 64006B | Serial Host (twin USB-A) | 8 | active |
| 64006C | LED Matrix (8×7 Charlieplex, 56 LEDs) | 8 | active |
| 64006D | Digital Video Out (HDMI-type TMDS) | 8 | active |
| 64006E | Mini Prototyping (8×12 grid) | 8 | active |
| 64006F | Serial Device (twin microUSB) | 8 | active |
| 64006G | Goertzel / Touch (compass + switch pads) | 8 | active |
| 64006H | A/V Breakout (VGA + RCA + audio) | 8 | active |
| 64032 | HUB75 Adapter (RGB LED panel) | 16 | retiring (limited stock) |
| 64004-ES | HyperRAM + HyperFlash (16 MB + 32 MB) | 16 | limited edition |

### Host boards, modules, carriers & reference

| File | Kind |
|------|------|
| p2-eval-board | Host eval board (64000) |
| edge-standard-module · edge-32mb-module | Edge CPU modules |
| edge-breadboard-carrier · edge-mini-breakout · edge-standard-breakout | Edge carriers/breakouts |
| hardware-compatibility-matrix · p2-hardware-feature-comparison · p2-hardware-selection-guide · p1_rom_font_character_set | Reference data |

> Inventory and categories are kept 1:1 with the served files — adding or removing
> a board updates the file, `engineering/tools/p2kb-categories.json`, and this
> table together, and the regenerated index is asserted to match.
