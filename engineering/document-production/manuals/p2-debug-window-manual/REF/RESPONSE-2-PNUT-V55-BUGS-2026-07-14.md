# Response 2 — root-cause analysis of your two PNut v55 bug reports

**From:** PNut-Term-TS (IronSheep) · **To:** P2 Knowledge Base doc team · **Date:** 2026-07-14
**Re:** `PNUT-BUG-scope-xy-parser-hang.md`, `PNUT-BUG-save-window-wrong-rect.md`
**Follow-on to:** `RESPONSE-REF-CLEANUP-2026-07-14.md`

We traced both reports to the exact defective lines in v55 and **appended a root-cause section to each of
your two docs** (in place, below your original text — your reports are untouched). Both are ready to go to
Chip as-is.

Below: what closed, **one correction you must make**, two questions only you can answer, and a new
doc-impact item for the manual.

---

## 1. SCOPE_XY parser hang — loop closed, and it closed nicely

Worth noting how this one went, because the process worked exactly as intended:

- §5 of our last response **predicted this from the source** and said *"worth confirming on silicon."*
- You **confirmed it on real hardware** with the TERM-heartbeat instrument — which was the right call, and
  the right instrument: a screenshot genuinely cannot distinguish *hung* from *window never opened*.
- We have now **proven the mechanism and bounded the blast radius**.

**Your diagnosis is correct and your suggested fix is correct.** Confirmations to bank:

- The proof is in `NextElement` (L4129): it advances `ptr` **only** on a type match, and `NextEnd` never
  advances it at all. `SCOPE_XY_Configure` handles `ele_key` and `ele_str` but not `ele_num` → `ptr`
  freezes → infinite loop.
- **It is an omission, not a design choice.** Chip uses the guard idiom (`if NextNum then Break;`) in
  **six** places — including `SCOPE_XY_Update`, the *same window's* other loop. He guarded the update loop
  and missed the configure loop.
- **We extended your audit from 9 loops to 18.** You checked the nine `*_Configure` loops; we also checked
  the nine `*_Update` loops, which share the loop shape and could have hidden the same hole. They don't.
  **`SCOPE_XY_Configure` is the only hole in the entire file.** Your blast-radius conclusion survives the
  wider sweep — you can state it without hedging.

### Doc impact for the manual

A bare number is **invalid** on a `SCOPE_XY` create line (as it is on `LOGIC`'s). Worth stating plainly,
because until Chip ships the fix, in v55 it does not merely get ignored — **it hangs the tool.**

---

## 2. SAVE WINDOW — 🔴 a correction you need to make

**Your "Suggested area to look at" is wrong. Please don't carry it forward** into the manual, a follow-up,
or the note to Chip.

> *"it appears to use the **client** dimensions where it needs the **outer/frame** rectangle"*

It does not. `KeySave` (L2839) already uses `Width`/`Height` — which for a VCL top-level form **are** the
outer frame dimensions. That part of Chip's code is correct, and pointing him at it would cost him time.

**The actual flaw is one level down, and it is a single false assumption:** the routine feeds the form's
`Left/Top/Width/Height` straight into a `BitBlt` from a desktop DC — i.e. it assumes *the process's window
coordinates are the screen's pixels*. They aren't, because **`PNut_v55.exe` ships with no application
manifest at all** (we verified this against the binary: zero occurrences of the manifest schema URN, and
`PNut.dpr` adds none). No manifest ⇒ **DPI-unaware process** ⇒ above 100% display scaling, Windows
virtualizes PNut's coordinate space while the framebuffer stays physical.

**Your own measurements corroborate this independently of the binary finding.** The saved file is 70×93 —
and those two numbers *are* `Width`/`Height`, written straight into the bitmap. But you measured the
on-screen window at ~114 tall, and `93 × 1.25 = 116`. The window you see is ~1.25× the window the app
believes it has. That is the definition of DPI virtualization. With that one scale factor, **all three of
your evidences fall out** — including your "~21 missing rows", which the model predicts to within a pixel
or two without being tuned.

Full derivation, the three-evidence table, and the recommended fix (`PrintWindow` — which also kills the
occlusion, paint-race and multi-monitor failures in the same stroke) are in the appended section of your
doc.

---

## 3. Two questions back to you — you have the Windows box, we don't

Neither blocks the fix (the recommended fix is correct under every hypothesis). Both are cheap, and they
would let us state the mechanism as *confirmed* rather than *strongly indicated*:

1. **What is the display scaling on the machine you tested on?** Your numbers imply ~**125%**. If it is
   actually **100%**, our model is wrong and the cause is the secondary paint-race defect instead — we'd
   want to know.

2. **Which edge is the ~4 px wallpaper strip on — left or right?** You wrote **right**; the mechanism
   predicts **left** (the read rectangle is displaced *toward the screen origin*). This is the one datum
   that doesn't fit cleanly. It may just be a misread, but if it is genuinely on the right, one of our
   sign assumptions is off.

3. **The one-minute experiment that settles it:** set Windows display scaling to **100%** and re-run the
   repro. If `SAVE WINDOW` captures correctly at 100% and misbehaves at 125%/150%, DPI virtualization is
   confirmed as the cause, full stop.

---

## 4. New doc-impact item for the DEBUG Window Manual

Independent of whether Chip fixes anything, this is a **sharp edge worth documenting**:

**`SAVE`'s two forms live in different coordinate spaces.**

- `POS x y` is **logical** — `KeyPos` (L2714) does `Left := val + P2.DebugDisplayLeft`, a VCL form coord.
- `SAVE <l> <t> <w> <h> 'name'` numbers are consumed as **physical framebuffer** coordinates (that is what
  a `BitBlt` from a desktop DC reads).

Under any display scaling above 100% these disagree by the scale factor. A user who places a window at
`POS 300 0` and then writes `SAVE 300 0 400 400 'shot'` **does not capture their window.** Same root cause
as the `SAVE WINDOW` bug, different route — and note that `PrintWindow` **cannot** fix this one, because
that form captures an *arbitrary screen region* (per your own ledger entry), which may not be a PNut window
at all. We've flagged it to Chip as a **design call, not a defect fix**: the source does not settle whether
the user is meant to reason in `POS`-space or in physical pixels.

---

## 5. Still outstanding from round 1

§7 of our last response: **re-run your systematic v55 ↔ REF diff** against the re-grounded REF. We expect
the survivors to be **v55-manual defects**, not REF defects. Candidates we flagged and still stand behind:

- `KeyValWithin` documented as *"ignored"*
- TERM 300×200
- SCOPE_XY 512
- LOGIC `LINESIZE 1..7`
- the `TRIGGER` mask/match form

Your two bug reports are evidence you've been doing exactly this kind of verification against the tool —
so some of this may already be in flight. If so, ignore this section.
