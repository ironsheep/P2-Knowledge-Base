# LED Matrix Add-on Board (#64006C)

**Part:** #64006C · **Series:** P2 Eval Add-on Boards (#64006) · **Source:** Product Guide v2.0 (1/12/2021)
**Cross-edition:** present in the 2020 #64006-ES set edition.

**Image:** `../assets/images-p2-eval-add-on-boards-2026-06-22/img-006.png` (8×7 Charlieplex grid photo). See `image-catalog.md`.

## Function
An **8 × 7 grid of Charlieplexed green LEDs** — display text/graphics across **56 LEDs using only 8 I/O
pins**. Charlieplexing exploits the one-way current flow of diodes plus the tri-state property of P2 I/O pins
(see https://en.wikipedia.org/wiki/Charlieplexing).

To light one LED, drive one I/O **HIGH** and one **LOW** per the lookup table; set both pins to **INPUT**
to turn it off. Multiple LEDs are multiplexed fast (P2 can switch each I/O > 180 MHz); switching each LED
on/off ≥ 50 Hz removes visible flicker. Each LED draws ~**4 mA** lit; Charlieplexing lights one at a time, so
instantaneous current stays ~4 mA (vs ~224 mA if all 56 were on at once).

## Charlieplex lookup table (which I/O HIGH / which I/O LOW per LED)
| Row | Col1 | Col2 | Col3 | Col4 | Col5 | Col6 | Col7 | Col8 |
|-----|------|------|------|------|------|------|------|------|
| 1 | 0H/1L | 0H/2L | 0H/3L | 0H/4L | 0H/5L | 0H/6L | 0H/7L | 1H/0L |
| 2 | 1H/2L | 1H/3L | 1H/4L | 1H/5L | 1H/6L | 1H/7L | 2H/0L | 2H/1L |
| 3 | 2H/3L | 2H/4L | 2H/5L | 2H/6L | 2H/7L | 3H/0L | 3H/1L | 3H/2L |
| 4 | 3H/4L | 3H/5L | 3H/6L | 3H/7L | 4H/0L | 4H/1L | 4H/2L | 4H/3L |
| 5 | 4H/5L | 4H/6L | 4H/7L | 5H/0L | 5H/1L | 5H/2L | 5H/3L | 5H/4L |
| 6 | 5H/6L | 5H/7L | 6H/0L | 6H/1L | 6H/2L | 6H/3L | 6H/4L | 6H/5L |
| 7 | 6H/7L | 7H/0L | 7H/1L | 7H/2L | 7H/3L | 7H/4L | 7H/5L | 7H/6L |

(e.g. Row 3 Col 6 = "3 HIGH, 0 LOW" → drive IO 3 HIGH and IO 0 LOW.)
