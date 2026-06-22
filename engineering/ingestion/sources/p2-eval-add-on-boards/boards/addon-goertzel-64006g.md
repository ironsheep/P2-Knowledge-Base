# Goertzel Add-on Board (#64006G)

**Part:** #64006G · **Series:** P2 Eval Add-on Boards (#64006) · **Source:** Product Guide v2.0 (1/12/2021)
**Cross-edition delta:** the 2020 #64006-ES edition's Goertzel had **probe posts**; **v2.0 (Rev B) replaced
them with touch switch pads** (the documented edition change). Pin map/function otherwise consistent.

**Image:** `../assets/images-p2-eval-add-on-boards-2026-06-22/img-011.png` (Rev B touch-pad board photo). See `image-catalog.md`.

## Function
A Goertzel experimenter board (Rev B) with **pads for non-contact switching / position sensing**. Pads
**4, 5, 6** are typically used as on/off (switch-style) inputs; pads **0, 1, 2, 3, 7** form a set of Goertzel
input pads (compass-style positions around a center common pad).

## Pin map (I/O 0–7)
| I/O | Function |
|-----|----------|
| 0 | Goertzel E (3 o'clock) |
| 1 | Goertzel W (9 o'clock) |
| 2 | Goertzel N (12 o'clock) |
| 3 | Goertzel S (6 o'clock) |
| 4 | Switch pad (Left) |
| 5 | Switch pad (Right) |
| 6 | Switch pad common reference |
| 7 | Goertzel C (Center common pad) |
