# Digital Video Out Add-on Board (#64006D)

**Part:** #64006D · **Series:** P2 Eval Add-on Boards (#64006) · **Source:** Product Guide v2.0 (1/12/2021)
**Cross-edition:** present in the 2020 #64006-ES set edition.

**Image:** `../assets/images-p2-eval-add-on-boards-2026-06-22/img-007.png` (HDMI-type board photo). See `image-catalog.md`.

## Function
Provides an **HDMI-type connector** for experimenting with various video standards. The signal pins
connected to the P2-EVAL header carry the TMDS clock + 3 data lanes as differential pairs.

## Pin map (I/O 0–7)
| I/O | Function |
|-----|----------|
| 0 | CLK − |
| 1 | CLK + |
| 2 | D0 − |
| 3 | D0 + |
| 4 | D1 − |
| 5 | D1 + |
| 6 | D2 − |
| 7 | D2 + |

## Notes
Unused video-connector signals are on an unpopulated 0.1" row of 6 pads: **CEC, RSVD, SCL, SDA, 5V▶,
HPD**. Beside the **5V▶** pad is an **ACC 5V** pad (the 5V from the accessory socket); some monitors need
5V on 5V▶, so the two 0.1"-spaced pads make bridging convenient (e.g. a header + shunt plug).
