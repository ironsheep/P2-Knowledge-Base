# DEBUG display window names — the definitive rules

**Source:** agent study of the **PNut v55** compiler source (`p2com.asm`), commissioned after a
shipped example failed on silicon (F-228). Ground truth per the standing rule — PNut is
authoritative, `pnut_term_ts` mirrors it.
**Recorded:** 2026-07-27. **Upstream of:** `deliverables/ai/P2/language/spin2/statements/debug.yaml`
(`window_name_rules`) and Chapter 2 / Appendix A of the P2 Debug Window Manual.

This is the reference the manual and the KB cite. It supersedes the partial "don't use a directive
name" guidance that preceded it.

---

## The definition

A window name is legal **if and only if** all five hold:

1. **Character set.** Starts with a letter or `_`, then letters / digits / `_` only
   (`check_word_chr_initial` / `check_word_chr`, `p2com.asm:8888`). A **leading digit** makes the
   token parse as a *number* → abort.
2. **Not one of the 103 reserved debug-display words** (the `debug_symbols` table,
   `p2com.asm:19335`) — 9 display types + 94 directive/keyword entries. Full list below.
3. **Not the name of a display that is currently open** — it would resolve to `dd_nam`. After a
   `CLOSE` the name reverts to `dd_unk` and is **reusable**; `parse_debug_string` explicitly
   rewrites the symbol type back.
4. **Matching is case-insensitive.** `check_word_chr` uppercases before storing, so `Trace`,
   `TRACE` and `trace` are the same symbol. The **displayed** name keeps your original casing (the
   code copies the "original non-uppercased symbol to `dd_name`").
5. **Truncated at 30 characters** (`symbol_size_limit = 30`). Extra characters are silently
   dropped — two names sharing their first 30 characters **collide**.

## Why this matters — the failure is silent

A name that violates rule 1 or 2 does not raise a compile error and does not raise a host error.
**No display is declared**, the window never opens, and every later message addressed to that name
goes nowhere. This is the same silent-failure family as double quotes in a display string and a
`SAVE` with no filename.

Empirically isolated (2026-07-26/27, PNut v55, real silicon): six SCOPE creates differing **only**
by name — `A`–`E` opened, `Trace` did not. See F-228 in `P2KB-CORRECTION-FINDINGS.md` and the probe
`audit/verification-tests/probe-ch14-scope-create.spin2`.

## Scope note — two vocabularies, only one collides

**Spin2's reserved words are irrelevant** to window names: the compiler emits the display name as
raw text and never interprets it. A PLOT named `Field` runs correctly even though `FIELD` is a
Spin2 keyword (`examples-library/ch05-plot-field.spin2`, hardware-run). Only the **103 below** can
collide.

---

## The reserved 103, complete

**Display types (9)**
`LOGIC` `SCOPE` `SCOPE_XY` `FFT` `SPECTRO` `PLOT` `TERM` `BITMAP` `MIDI`

**Colors (11)**
`BLACK` `WHITE` `ORANGE` `BLUE` `GREEN` `CYAN` `RED` `MAGENTA` `YELLOW` `GRAY` `GREY`

> Note `GREY` **and** `GRAY` — both spellings are reserved (`GRAY` was added alongside `GREY` in
> Spin2 v37). A per-window directive table listing only ten colors is listing the *color* set, not
> the reserved set.

**Color modes (19)**
`LUT1` `LUT2` `LUT4` `LUT8` `LUMA8` `LUMA8W` `LUMA8X` `HSV8` `HSV8W` `HSV8X` `RGBI8` `RGBI8W`
`RGBI8X` `RGB8` `HSV16` `HSV16W` `HSV16X` `RGB16` `RGB24`

**Packed-data modes (12)**
`LONGS_1BIT` `LONGS_2BIT` `LONGS_4BIT` `LONGS_8BIT` `LONGS_16BIT` `WORDS_1BIT` `WORDS_2BIT`
`WORDS_4BIT` `WORDS_8BIT` `BYTES_1BIT` `BYTES_2BIT` `BYTES_4BIT`

**Directives (52)**
`ALT` `AUTO` `BACKCOLOR` `BOX` `CARTESIAN` `CHANNEL` `CIRCLE` `CLEAR` `CLOSE` `COLOR` `CROP`
`DEPTH` `DOT` `DOTSIZE` `HIDEXY` `HOLDOFF` `LAYER` `LINE` `LINESIZE` `LOGSCALE` `LUTCOLORS` `MAG`
`OBOX` `OPACITY` `ORIGIN` `OVAL` `PC_KEY` `PC_MOUSE` `POLAR` `POS` `PRECISE` `RANGE` `RATE`
`SAMPLES` `SAVE` `SCROLL` `SET` `SIGNED` `SIZE` `SPACING` `SPARSE` `SPRITE` `SPRITEDEF` `TEXT`
`TEXTANGLE` `TEXTSIZE` `TEXTSTYLE` `TITLE` `TRACE` `TRIGGER` `UPDATE` `WINDOW`

---

## Consequences worth carrying into docs and generated code

- **The reserved set is larger than any one window's directive list.** A colour name (`Red`), a
  color-mode name (`RGB24`), a packed-mode name, or another window's directive (`Trace` on a SCOPE)
  is just as fatal as that window's own directives. Do not present "the directives in this
  chapter" as the reserved list.
- **Case gives no escape.** `trace` and `Trace` are the same reserved symbol; only a different
  *word* works.
- **Names are reusable after `CLOSE`** — a program may retire a window and re-declare its name.
- **Keep names well under 30 characters**, and never let two names share a 30-character prefix.
- **A leading digit is a distinct failure** (parsed as a number, aborts), not a keyword collision.
