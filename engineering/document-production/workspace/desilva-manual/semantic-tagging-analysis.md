# Technical Analysis: Semantic Tagging for PASM Instructions

## The Challenge
We want PASM instructions to appear as **UPPERCASE + BOLD** everywhere, but we need to evaluate if semantic tagging is technically feasible without breaking our toolchain.

## Option 1: Direct Markdown (**MOV** in source)
✅ **Pros:**
- Simple, works immediately
- No toolchain changes needed
- What you see is what you get
- No escaping issues

❌ **Cons:**
- Formatting baked into content
- Harder to change style later
- Not semantically clean

## Option 2: Custom LaTeX Commands (\pasm{mov})
❌ **BLOCKER:** LaTeX commands DON'T work inside code blocks!
- Code blocks use `verbatim` or `lstlisting` environments
- These environments treat content as literal text
- `\pasm{mov}` would appear literally in the output
- This is a fundamental limitation

## Option 3: Listings Package Keywords (BEST TECHNICAL SOLUTION)

The `listings` package we're already using can automatically style keywords!

### How it works:
```latex
\lstset{
  morekeywords=[2]{MOV, ADD, SUB, WAITX, DRVH, DRVL, JMP, ...},
  keywordstyle=[2]\bfseries\uppercase,
  % ... rest of settings
}
```

### In markdown, we write:
```pasm2
        mov     pa, #5          ' Normal lowercase
        add     pb, pa
        waitx   ##1000
```

### LaTeX automatically renders as:
```
        MOV     pa, #5          ' Bold + uppercase
        ADD     pb, pa
        WAITX   ##1000
```

✅ **Pros:**
- Clean markdown source (normal lowercase)
- Automatic formatting by LaTeX
- No escaping issues
- Single source of truth (template)
- Already using listings package

❌ **Cons:**
- Need to list ALL PASM instructions in template
- Case-insensitive matching might be tricky
- May need listings package configuration

## Option 4: Pandoc Filter (Complex but Powerful)

Write a custom Pandoc filter to process code blocks:
- Detect `pasm2` code blocks
- Parse and identify mnemonics
- Wrap them with formatting

❌ **Cons:**
- Requires custom Lua/Python filter
- Another moving part in toolchain
- Complexity for maintenance

## Option 5: Pre-processor Script (Current Approach)

Run a script before pandoc that modifies the markdown:
```python
mov pa, #5  →  **MOV** pa, #5
```

✅ **Pros:**
- We already have the script written
- Predictable results
- No toolchain surprises

❌ **Cons:**
- Extra processing step
- Modifies source content

## RECOMMENDATION: Hybrid Approach

### For THIS document specifically:
1. **Use direct markdown** (**MOV** in source) because:
   - PASM instruction format is NOT adjustable (as you noted)
   - We want absolute consistency
   - No technical surprises
   - Document is pedagogical, not reference

### BUT, implement smartly:
1. Keep original files with lowercase
2. Use script to generate "presentation" version with **UPPERCASE**
3. This gives us both:
   - Clean source files (lowercase)
   - Formatted output (**UPPERCASE**)
   - Ability to regenerate if needed

### Why not listings keywords?
The listings package approach is technically cleanest, BUT:
- Getting case-insensitive uppercase transform is non-trivial
- Would need extensive listings customization
- Risk of edge cases and surprises
- More LaTeX debugging

## Code Block Colors in Gray Regions

You're right about deSilva's yellow code blocks everywhere! We should:
1. Keep code blocks yellow even inside gray sidetrack boxes
2. This creates visual consistency: "code is always yellow"
3. Technically easy - don't override code block color in sidetrack environment

## Final Technical Assessment

**Most Reliable Path:** Direct markdown with **UPPERCASE + BOLD**
- No pandoc interference ✅
- No LaTeX complications ✅
- No escaping issues ✅
- What you write is what you get ✅

**Most Maintainable Path:** Keep two versions
- Source: lowercase (clean for editing)
- Generated: **UPPERCASE** (for PDF generation)
- Script to convert between them

This isn't fighting your instinct - it's recognizing that for pedagogical documents where formatting IS meaning, baking it in is actually the right choice.