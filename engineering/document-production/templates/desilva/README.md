# DeSilva Template Stack

Complete PDF generation template system for DeSilva-style P2 manuals.

## Components

### LaTeX Templates
- `p2kb-desilva.latex` - Main template file (loads foundation and content layers)
- `p2kb-desilva-content.sty` - DeSilva content layer with 5-color code system and pedagogical environments

### Lua Filters (Proven Working - Adapted from Smart Pins)
- `p2kb-desilva-code-coloring.lua` - 5-color code block system (Spin2-green, PASM2-yellow, CORDIC-purple, Multi-COG-blue, Antipattern-red)
- `p2kb-desilva-semantic.lua` - DeSilva pedagogical elements (Medicine Cabinet, Your Turn, Sidetrack, Uff, Well, Have Fun)
- `p2kb-desilva-pagination.lua` - Smart page breaks for Parts/Chapters

### Configuration
- `request.json` - Sample PDF Forge request with all required pandoc arguments

## 5-Color Code Block System

```markdown
::: spin2
' Spin2 code in green blocks
PUB main()
  debug("Hello P2!")
:::

::: pasm2
' PASM2 code in yellow blocks
        org     0
        mov     outa, #1
:::

::: cordic
' CORDIC operations in purple blocks
        qrotate ##90_000000_000  ' 90 degrees in CORDIC format
        getqx   angle
:::

::: multicog
' Multi-COG examples in blue blocks
cogstart(@cog_task, @stack_space)
:::

::: antipattern
' Common mistakes in red blocks
' DON'T DO THIS - causes timing issues
:::
```

## DeSilva Pedagogical Elements

```markdown
::: medicine-cabinet
When things go wrong, try this simpler approach first.
:::

::: your-turn
Now it's time for you to try this concept yourself.
:::

::: sidetrack
This is interesting but not essential to understanding.
:::

::: uff
We just got through something complex! Take a breath.
:::

::: well
You might think X, but actually Y is what happens.
:::

::: have-fun
Celebrate! You've mastered an important concept.
:::
```

## Usage

1. **Copy template files to your document directory**:
   ```bash
   cp p2kb-desilva.latex /path/to/your/document/
   cp p2kb-desilva-*.lua /path/to/your/document/filters/
   ```

2. **Update request.json** with your document specifics:
   - Change input filename
   - Update title/subtitle/version
   - Adjust any pandoc arguments if needed

3. **Deploy to PDF Forge** as normal

## Foundation Layer

Uses the shared `p2kb-foundation.sty` which provides:
- Pandoc compatibility
- Part/Chapter pagination logic
- Basic typography and layout
- Image scaling and placement
- Index and TOC support

## Source

Adapted from proven Smart Pins template system:
- Smart Pins workspace filters (p2kb-sp-code-coloring.lua, p2kb-sp-semantic.lua, p2kb-sp-pagination.lua)
- Smart Pins content layer (p2kb-sp-styles.sty)
- Latest Smart Pins foundation improvements

All filters are proven working in production Smart Pins PDF generation.