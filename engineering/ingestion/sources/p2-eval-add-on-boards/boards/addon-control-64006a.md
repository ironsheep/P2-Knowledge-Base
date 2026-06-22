# Control Add-on Board (#64006A)

**Part:** #64006A · **Series:** P2 Eval Add-on Boards (#64006) · **Source:** Product Guide v2.0 (1/12/2021)
**Cross-edition:** identical in the 2020 #64006-ES set edition (pin map + function unchanged).

## Function
Four push-buttons and four blue LEDs. The push-buttons give simple digital input control; each
**active-high** push-button has a **470 Ω series resistor** so the I/O pin is driven low while the button is
asserted. The LEDs are **active-high**, positioned next to each button, each on its own independent I/O pin.

## Pin map (I/O pin offsets 0–7 on the board's 2×6 header block)
| I/O | Function |
|-----|----------|
| 0 | Blue LED, 470 Ω series resistor. Assert high to light. Use PWM for brightness. |
| 1 | Blue LED, 470 Ω series resistor. Assert high to light. Use PWM for brightness. |
| 2 | Blue LED, 470 Ω series resistor. Assert high to light. Use PWM for brightness. |
| 3 | Blue LED, 470 Ω series resistor. Assert high to light. Use PWM for brightness. |
| 4 | Tactile push switch, 470 Ω series resistor, active high. |
| 5 | Tactile push switch, 470 Ω series resistor, active high. |
| 6 | Tactile push switch, 470 Ω series resistor, active high. |
| 7 | Tactile push switch, 470 Ω series resistor, active high. |

## Notes
Shared form factor / power / mounting in the overview (`../complete-p2-eval-add-on-boards-reference.md`).
