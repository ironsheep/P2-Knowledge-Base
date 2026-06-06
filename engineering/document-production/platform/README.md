# P2KB Presentation Platform (shared rendering stack)

Canonical, **shared** stylesheets + Lua filters that every manual consumes —
replacing the old fork-per-manual model. Promoted from the certified torture
instrument stack (2026-06-06).

**Design:** `../methodology/presentation-platform-unification-STUDY.md`
**Block vocabulary:** `../methodology/presentation-block-catalog.md`

## Contents

```
platform/templates/
  p2kb-platform-foundation.sty   geometry, widow/orphan penalties, titlespacing, hyperref
  p2kb-platform-content.sty      code/reference box family, contmarkers, keep-together, iosp-* palette
platform/filters/
  p2kb-platform-figures.lua      figure move-whole (needspace)
  p2kb-platform-tables.lua       longtblr split + rowhead + token-fit (fix #5) + continuation markers
  p2kb-platform-code-coloring.lua
  p2kb-platform-mnemonic-bold.lua
  p2kb-platform-pagination.lua
```

## How a manual consumes the platform

The manual's `reference.latex` loads the shared layers, then its own thin override + diagrams:

```latex
\usepackage{p2kb-platform-foundation}   % shared
\usepackage{p2kb-platform-content}      % shared
\usepackage{p2kb-<slug>-local}          % per-manual skins / local tail (thin)
\usepackage{p2kb-<slug>-diagrams}       % per-manual TikZ content
```

and its `request.json` lists the platform filters by name (`p2kb-platform-figures`, …).

**Per-manual files** stay in `workspace/<slug>/`: `reference.latex`, `request.json`,
`templates/p2kb-<slug>-local.sty`, `templates/p2kb-<slug>-diagrams.sty`, `assets/`.

**A platform fix happens once here** and every manual inherits it on next build. The
torture instrument also consumes the platform, so certifying on the instrument
certifies the exact files manuals ship.

## Pilot status

- **Streamer** migrated first (twin manual). Initial PDF generated on the platform
  stack: 65 pp, clean compile (run `streamer-platform-v3`). Remaining before
  release: Figures & Tables standard + screenshot keyline (catalog §8), fix 18
  overlong code lines + seed K=76, then production.
