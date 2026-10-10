# P2 Eval HUB75 Adapter (#64032) — designer's statement, 2026-10-10

**Who**: Stephen M Moraco, Iron Sheep Productions, LLC — the board's designer and manufacturer.
He designed and engineered the board, had it made, and sells it to the Parallax store.
**Given**: 2026-10-10, in a working session on F-567, in his own words (below).
**Authority**: golden source for this board (`AUTHORITATIVE-SOURCES.md`, the designer's-own-hardware
rule of 2026-10-10). Cite as: *Stephen M Moraco (Iron Sheep Productions, LLC), designer's
statement for the P2 Eval HUB75 Adapter (#64032), 2026-10-10*.

## The figures

These three figures were already in our captures of the board's product specification. Stephen
confirmed all three as the designer's own and told us to use them. The board size is his hand
measurement.

| Figure | Value |
|---|---|
| Board size (hand-measured) | 1.9 x 2.8 inches (48 x 71 mm) |
| Board current draw | under 50 mA (the level shifters and support circuitry) |
| Maximum clock rate | 70 MHz, limited by the level shifter ICs |

The schematic names the level shifters: two 74HCT244 buffers powered at 5 V
(`p2-hub75-adapter-netlist.md`).

## His words (verbatim)

> "My own documents, since I created this board, I engineered the board, designed the board, had
> them made, and I sell them to the store, are also trusted golden sources. … So, board size, the
> power consumption, and the clock rates really don't affect what we're doing because the boards
> that we're driving with that controller will never go to 70 MHz. Those numbers are perfectly
> fine to use. Let's just use them, and you can cite me as the source. I hand-measure the boards."

## Product facts confirmed (later the same day)

Asked the same day which product claims on the KB page he stands behind, Stephen confirmed these
four, as put to him, by choosing the option "confirm (a)–(d), remove (e)". He was told that his
reply would be read as standing behind (a)–(d) exactly as listed, and he raised no correction
over the four questions that followed.

| | Fact | As confirmed |
|---|---|---|
| (a) | Host boards | P2 Eval Board (#64000); P2 Edge Module Breadboard (#64020) with a P2 Edge Module (P2-EC); P2 Edge Mini Breakout Board (#64019) with a P2 Edge Module (P2-EC) |
| (b) | Address lines to panel rows | A-B-C for 16-row panels; A-B-C-D for 32-row panels; A-B-C-D-E for 64-row panels |
| (c) | P2-side headers | female pass-through |
| (d) | Status | retiring, limited stock |

Not confirmed, and removed from the KB on his choice: (e) the generic panel material — scan-rate,
resolution and pixel-pitch lists, daisy-chaining, wiring advice and a toolchain list. That is
panel and driver material, owned by the driver's own documentation (OBEX 2850).

His reply (verbatim): "yes A".

## Scope

This record covers only the three figures and the four product facts above. Anything else about
the board comes from the schematic (`p2-hub75-adapter-netlist.md`) or from a further statement by
the designer, recorded the same way.
