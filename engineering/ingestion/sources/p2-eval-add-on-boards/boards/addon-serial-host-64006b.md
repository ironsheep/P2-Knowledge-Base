# Serial Host Add-on Board (#64006B)

**Part:** #64006B · **Series:** P2 Eval Add-on Boards (#64006) · **Source:** Product Guide v2.0 (1/12/2021)
**Cross-edition:** identical in the 2020 #64006-ES set edition (incl. the Rev B 5V note → present from v1.1).

**Image:** `../assets/images-p2-eval-add-on-boards-2026-06-22/img-005.png` (twin USB-A photo). See `image-catalog.md`.

## Function
Twin **USB-type A** sockets, each protected by a **current-limited load switch** allowing up to **500 mA**
continuous (subject to available system power); protection includes reverse-current blocking, short-circuit,
over-temperature, and VBUS soft-start. Lets two USB-type devices connect simultaneously (e.g. keyboard +
mouse). Two user-controlled blue activity LEDs beside the sockets. **To enable 5V output on a channel,
set its enable pin high — I/O 1 (channel 1), I/O 5 (channel 2).**

> **Requires 5V to function.** With the P2-ES Eval Board **Rev B**, the shunt jumper must connect that
> board's **ACC HDR** and **5V** pins to supply 5V to its I/O Pin Breakout Edge Headers.

## Pin map (I/O 0–7)
| I/O | Function |
|-----|----------|
| 0 | Blue LED, 1 kΩ series resistor. Assert high to light. Use PWM for brightness. |
| 1 | Serial channel 1 : Enable, active high |
| 2 | Serial channel 1 : Data D− |
| 3 | Serial channel 1 : Data D+ |
| 4 | Blue LED, 1 kΩ series resistor. Assert high to light. Use PWM for brightness. |
| 5 | Serial channel 2 : Enable, active high |
| 6 | Serial channel 2 : Data D− |
| 7 | Serial channel 2 : Data D+ |
