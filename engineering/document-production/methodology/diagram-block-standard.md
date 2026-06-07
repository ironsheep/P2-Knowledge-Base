# Diagram Block Standard

A shared look-and-feel for the manuals' TikZ diagrams, so every figure reads as
one family — **consistent without being overbearing**. Lives in the platform:
`platform/templates/p2kb-platform-diagrams.sty` is the single home of the palette,
node/edge styles, and the `\diagramscale` wrapper; each manual's
`<slug>-diagrams.sty` does `\RequirePackage{p2kb-platform-diagrams}` and defines
only its own `\Diag*` macros against these styles.

## The core principle

**A diagram block is a NAME, not a paragraph.** The block holds the noun
("LUT", "NCO", "DACs"); the descriptive detail ("entry = LUT[NCO[30:22]]",
"S operand", "byte ⊕ \$80") goes **beside** the block as a sub-label, or into the
prose/legend — never crammed inside the box. Text crammed into a block is what
inflates it; pulling it out is what keeps diagrams calm.

## Rules

1. **Label discipline.** Block label ≤ 2 short lines. Qualifiers become an
   `iospsub` sub-label placed *under* the block, or move to prose.
2. **Compact, content-sized blocks.** `iospbox`: `minimum height=7mm`,
   `minimum width=14mm`, content sizing (no oversized fixed `text width`). Single
   words stay compact; two-line labels grow naturally; nothing balloons. A large
   fixed min-height is what ballooned single-line blocks before.
3. **Shrink-to-fit scaling — NEVER upscale.** Wrap the picture in `\diagramscale{…}`,
   not `\resizebox{\textwidth}{!}{…}`. `\diagramscale` renders at the diagram's
   natural size and only shrinks it when it is wider than the text block. Forcing
   every diagram to full text width *magnifies* a sparse diagram (few blocks,
   spread out) ~1.5×, blowing its blocks up out of proportion — the second cause of
   the "overbearing" look. The enclosing `figure`'s `\centering` keeps it centered.
4. **One type scale.** `\small` block labels, `\scriptsize\itshape` sub-labels,
   `\scriptsize` waveform / axis labels. Don't introduce new sizes per diagram.
5. **Two block roles only.** `iospbox` (primary, neutral gray) and `iospkey`
   (terminal / key result, green). No additional box types — guard against palette
   creep, exactly as the content-box catalog does.

## Retrofitting an existing diagram

- Swap `\resizebox{\textwidth}{!}{…}` → `\diagramscale{…}`.
- Move any qualifier text crammed into a block into an `iospsub` node beneath it.
- Delete per-node oversized `text width=…`; let the block size to its label against
  the 14mm floor (keep a `text width` only when you genuinely want a label to wrap).

## Why this standard exists

Two independent causes made some blocks (e.g. Streamer Fig 2.2, Fig 10.1) look
oversized next to their neighbours: (a) a fixed `minimum height=11mm` calibrated for
two-line labels ballooned the single-line ones, and (b) `\resizebox`-to-`\textwidth`
magnified sparse diagrams to fill the page. Rules 2 and 3 fix each at the source, in
one shared place, so the fix applies to every diagram and every manual that adopts
the platform diagrams base — not diagram-by-diagram.

## Adoption status

- **Streamer** (pilot): consumes `p2kb-platform-diagrams`; all `\Diag*` macros use
  `\diagramscale`. First manual on the standard.
- Other manuals' `<slug>-diagrams.sty` still carry their own copied styles; migrate
  them onto `p2kb-platform-diagrams` as each moves to the platform (the same
  one-at-a-time roll-out as the rest of the presentation-platform unification).
