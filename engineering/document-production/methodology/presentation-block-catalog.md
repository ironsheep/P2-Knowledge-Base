# Presentation Block Catalog (Registry)

**Status:** Draft 1 (2026-06-06). Companion to
`presentation-platform-unification-STUDY.md`. This is **the map every manual
picks from** — a controlled vocabulary of block/callout types so manuals
*select* instead of reinventing the same concept under new names.

> Drafted from a census of every `\newtcolorbox` across the 6 live manuals + the
> torture instrument, deduped **by meaning**. Counts/names verified against the
> source. The "Open classification calls" (§7) need your decisions before lock.

---

## 1. How to use this catalog (the anti-reinvention rule)

1. **Before inventing a box, find its meaning here.** If the concept exists, use
   the canonical type — re-skin it if your manual's voice differs (§3).
2. **Skin, don't fork the semantics.** Override *color / title / icon* in your
   `p2kb-<slug>-local.sty`. Never invent a new *type* for an existing meaning.
3. **A genuinely new concept?** Add it to this catalog (so the next manual
   reuses it), don't bury it as a silent local. (Same discipline as Sacred Rule
   #7 for YAML cross-refs: point to the canonical thing, don't duplicate it.)

## 2. The model: type vs skin, fenced vs div

- **Type** = canonical semantic (shared, presentation-neutral): `tip`,
  `exercise`, `antipattern`, `pasm2`…
- **Skin** = presentation (per-manual override): color, **title text**, icon.
  deSilva's "Your Turn" and a terse "Exercise" are the *same type* `exercise`,
  different skins.
- **Authoring convention** (settles the deSilva regression too):
  - **Code & notation → fenced** ` ```lang ` (verbatim, machine-renderable):
    `spin2 pasm2 cordic multicog`, and notation `syntax layout formula`.
  - **Callouts & semantic boxes → divs** `::: type` (prose content):
    `note tip caution … exercise aside example gotcha …`.

---

## 3. The catalog

Legend — **B**ehavior: `KT`=keep-together (not breakable) · `BR+M`=breakable
with continuation markers · `BR`=breakable. Skin colors are **defaults**,
overridable per manual.

### 3a. Code family — author as ` ```lang ` (already consistent everywhere)

| Type | Semantic | Default skin | B |
|------|----------|--------------|---|
| `spin2` | Spin2 source | blue fill/border | BR+M |
| `pasm2` | PASM2 source | green fill/border | BR+M |
| `cordic` | CORDIC example | purple | BR+M |
| `multicog` | multi-COG example | teal / blue-gray | BR+M |
| `command` | terminal command you TYPE (NOT P2 source) | charcoal frame + faint tint + "TERMINAL" tag; **no line numbers, no prompt** | BR |

> **Naming fix:** the technical twins call the PASM2 box `IOSPBlock` (legacy).
> Canonical type is **`pasm2`**; `IOSPBlock` becomes an alias to retire.
> **`command`** is the platform `CommandBlock` (added 2026-06-07): author shell/CLI
> invocations as ` ```command ` (aliases: `console`/`terminal`/`shell`) so they read
> as "run this," never as code. Cross-platform — deliberately no `$`/`>` prompt.

### 3b. Notation / reference family — author as ` ```kind ` (technical manuals)

| Type | Semantic | Default skin | B |
|------|----------|--------------|---|
| `syntax` | instruction/method syntax form | slate left-bar | KT |
| `layout` | bit-field / register-layout diagram | bronze fill | BR+M |
| `formula` | math / worked calculation | indigo left-bar | KT |
| `mode` | mode reference card | red corner-bar | KT |

### 3c. Admonition family — author as `::: type` (align to standard vocab)

| Type | Semantic | Default skin | B |
|------|----------|--------------|---|
| `note` | neutral aside / FYI | gray-blue | BR |
| `tip` | helpful suggestion | green | BR |
| `important` | must-not-miss point | blue | BR |
| `caution` | proceed carefully | amber | BR |
| `warning` | danger / will break | red | BR |
| `hardware` | hardware-specific consideration | brown | BR |
| `performance` | timing/throughput implication | violet | BR |
| `antipattern` | "don't do this" (dual-mode: code *or* prose) | red | BR / BR+M |

### 3d. Pedagogy family — author as `::: type` (tutorial / guide voice)

| Type | Semantic | Default skin | B |
|------|----------|--------------|---|
| `exercise` | reader does something now | amber | BR |
| `aside` | optional tangent (deSilva "Sidetrack"; adds a TOC line) | rose | BR |
| `interlude` | narrative breather | soft orange | BR |
| `gotcha` | common confusion + the fix | tan | BR |
| `example` | worked real-world example | brown | BR |
| `summary` | chapter/section recap / at-a-glance | blue | BR |
| `remark` | short author voice-aside (deSilva "Uff!/Well…/Have Fun!") | light | BR |

### 3e. Media family

| Type | Semantic | Default skin | B |
|------|----------|--------------|---|
| `screenshot` | annotated captured image (state: `needs-asset` placeholder) | white frame | BR |
| `discovery` | notable finding / key result | orange | BR |

---

## 4. Per-manual mapping (type → each manual's current local name)

`·` = not used. Current names shown; under unification these become *skins* of
the canonical type (or get renamed to it).

| Type | torture/iosp/streamer | ALM (pasm2) | deSilva | debug-window | ssdbg |
|------|----------------------|-------------|---------|--------------|-------|
| spin2 | Spin2Block | DeSilvaSpin2Block | DeSilvaSpin2Block | DebugWinSpin2Block / Spin2Block | Spin2Block |
| pasm2 | **IOSPBlock** | DeSilvaPASM2Block | DeSilvaPASM2Block | DebugWinPASM2Block / Pasm2Block | Pasm2Block |
| cordic | CORDICBlock | DeSilvaCORDICBlock | DeSilvaCORDICBlock | · | · |
| multicog | MultiCOGBlock | DeSilvaMultiCOGBlock | DeSilvaMultiCOGBlock | · | · |
| antipattern | AntipatternBlock *(prose)* | DeSilvaAntipatternBlock | DeSilvaAntipatternBlock *(code)* | · | · |
| syntax | SyntaxBlock | syntaxbox / syntaxforms | · | · | · |
| layout | LayoutBlock | · | · | · | · |
| formula | FormulaBlock | · | · | · | · |
| mode | ModeBlock | · | · | · | · |
| note | · | notebox | · | · | · |
| tip | · | tipbox | · | DebugWinTip / dwtip | · |
| caution/warning | · | warningbox | · | · | · |
| hardware | · | hardwarebox | · | · | · |
| performance | · | · | performancenote | DebugWinPerformance / dwperformance | · |
| exercise | · | · | DeSilvaYourTurn ("Your Turn") | DebugWinExperiment ("Experiment")? | · |
| aside | · | · | DeSilvaSidetrack ("Sidetrack") | · | · |
| interlude | · | · | DeSilvaInterlude | · | · |
| gotcha | · | · | DeSilvaMedicineCabinet + commongotas | · | · |
| example | · | · | realworldexample | · | · |
| summary | · | ataglance | DeSilvaChapterEnd ("Chapter Summary") | · | · |
| remark | · | · | dsuff/dswell/dshavefun | · | · |
| discovery | · | · | · | DebugWinDiscovery / dwdiscovery | · |
| screenshot | · | · | · | DebugWinScreenshot + NeedsScreenshot | · |

**The reinvention this exposes** (same meaning, different names today):
`performance` (deSilva + debug-window), `tip` (ALM + debug-window), `exercise`
vs `experiment`, `summary` (ALM `ataglance` + deSilva `ChapterEnd`),
`antipattern` (everywhere). Unifying collapses these to one name each.

---

## 5. The genuinely-local tail (stays per-manual unless it generalizes)

| Manual | Local-only blocks | Why local |
|--------|-------------------|-----------|
| **ALM** | `instrheader`, `dirheader`, `constheader`, `instructionentry` + encoding-table apparatus (entry-headers.lua, entry-format.lua) | reference-manual entry structure; domain-specific |
| **debug-window** | `DebugWinComparison`, `DebugWinMultiChannel`, `DebugWinGallery`, `DebugWinCommandRef`, per-window-type code blocks (Window/Debug/Terminal + Bitmap/Scope/Logic/Plot/FFT/Spectro/ScopeXY) | debug-window domain semantics |

Everything else above maps to a catalog type. The local tail is **small** —
which is the whole point: most "bespoke" boxes were re-skins, not new concepts.

---

## 6. Governance

- **Home:** this file is the registry; the platform implements the defaults; each
  manual's `-local.sty` carries its skin overrides + local tail.
- **Promotion gate:** a new local type that recurs (or that another manual would
  want) is promoted here. PR/commit that adds a box should state "uses catalog
  type X" or "proposes new catalog type Y."
- **Naming:** admonition types track the established vocabulary
  (`note/tip/important/caution/warning`, per MyST / GitHub alerts); extend only
  with domain types. Don't reinvent the catalog's own names.

---

## 7. Classification decisions (LOCKED 2026-06-06)

1. **`antipattern` = one dual-mode type** — red skin, renders as code *or* prose.
2. **`exercise` = one type** — debug-window "Experiment" is a skin (custom title)
   of `exercise`; not a separate type.
3. **`discovery` and `screenshot` are promoted to catalog** (not debug-local).
4. **`remark` is a catalog type** (author voice-aside); deSilva's
   Uff!/Well…/Have Fun! are skins of it.
5. **Full admonition set adopted** as canonical (`note/tip/important/caution/
   warning`) even where only some are used today — future manuals inherit the
   complete vocabulary.
6. **`summary` = one type, two skins** — ALM "At a Glance" and deSilva "Chapter
   Summary" are skins, not separate types.

> Adopted as the standard going forward. Everything here is a **starting point**,
> subject to continual growth/evolution as we improve — additions go through the
> §6 promotion gate.

---

## 8. Figures & Tables standard (LOCKED 2026-06-06)

Structural/navigational — a **platform standard for all manuals** (not per-manual;
only the *skin* is overridable). Manuals with no figures/tables simply get no
list (graceful).

- **All visual content is a numbered `figure`** — screenshots, TikZ diagrams, and
  bitmaps all route through one figure float so they share one number sequence
  and one List of Figures. (Replaces today's broken state: `\caption*`
  un-numbered captions + the separate `figurecaption` div — consolidate to one
  real numbered `\caption`.)
- **All tables are numbered + captioned** (today `tables.lua` emits no caption).
- **Both are `\label`-able and `\ref`-able** so prose can say "Figure 3.2" /
  "Table 5.1" and they resolve.
- **List of Figures / List of Tables** auto-included **when non-empty**.
- **Caption styling:** the label+number is **bold** ("**Figure 3.2**" /
  "**Table 5.1**"), caption body regular (`caption` pkg `labelfont=bf`). Uniform
  default; skinnable.
- **`[H]` placement is preserved** — placement and numbering are independent; a
  real `\caption` on an `[H]` figure still numbers, lists, and `\ref`s.

### Screenshot keyline (LOCKED)

- The **`screenshot` type renders as a framed figure with a thin keyline border,
  default ON** — fixes the "white screenshot on a white page has an invisible
  edge" problem. Default ≈ **0.5pt neutral mid-gray** with small inner pad.
- Scoped to screenshots (raster captures); **`diagram`/TikZ figures have no
  keyline by default** (their own strokes bound them) but may opt in.
- Border on/off/color/width is a **skin** parameter (default on for screenshots).
  Promote debug-window's existing gray keyline into the platform `screenshot`
  type rather than leaving it manual-only.
- Not the default: drop-shadows (gimmicky/print-inconsistent) and per-image
  selective borders (unpredictable; uniform hairline wins).
