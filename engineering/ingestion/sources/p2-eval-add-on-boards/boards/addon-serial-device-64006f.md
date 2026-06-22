# Serial Device Add-on Board (#64006F)

**Part:** #64006F · **Series:** P2 Eval Add-on Boards (#64006) · **Source:** Product Guide v2.0 (1/12/2021)
**Cross-edition:** identical in the 2020 #64006-ES set edition.

## Function
Two **microUSB-type** sockets, each with two activity LEDs — lets the Propeller 2 behave as up to **two
USB-type devices**, connecting to a USB host (computer or other USB-capable microcontroller). Two
user-controlled activity LEDs (**red + blue**) beside each microUSB socket.

## Pin map (I/O 0–7)
| I/O | Function |
|-----|----------|
| 0 | Blue LED, 1 kΩ series resistor. Assert high to light. |
| 1 | Red LED, 1 kΩ series resistor. Assert high to light. |
| 2 | Serial channel 1 : Data D− |
| 3 | Serial channel 1 : Data D+ |
| 4 | Serial channel 2 : Data D− |
| 5 | Serial channel 2 : Data D+ |
| 6 | Blue LED, 1 kΩ series resistor. Assert high to light. |
| 7 | Red LED, 1 kΩ series resistor. Assert high to light. |

> The v1.1 Rev B 5V note (ACC HDR/5V shunt jumper) applies to the Serial boards on the P2-ES Eval Board Rev B.
