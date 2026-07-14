# pnut-term-ts — the case for a manual, and its spine

**To:** the pnut-term-ts development agent
**From:** the P2 Debug Window Manual team
**Date:** 2026-07-14
**Ask:** draft the essential content against the spine below. We'll bring it back here for content
development and production (same pipeline as our other manuals).

---

## 1. Why the obvious framing is wrong

The instinct is: *"placement, logging, headless — three features. Not much of a manual."* And that's true
**if you frame it as a feature list.** A feature list is what the in-app help already is, and duplicating it
would produce a thin, low-value document that nobody reads twice.

**The features are not the product. The workflow they compose into is the product.**

## 2. The spine: *driving the P2 from an agent or a CI job*

> **Run headless → capture structured output → read it back → decide → repeat.**

That loop is the thing pnut-term-ts can do that **PNut cannot** (PNut is Windows-GUI-bound; term-ts is
cross-platform and headless-capable). It is the reason for the tool to exist as a separate product rather
than a port, and **nobody has written it down.**

It is also not hypothetical — **we ran it all night.** Here is the evidence, from a single P2 debug session
on 2026-07-14:

- We needed to know whether a suspected parser bug hangs the tool. **The screenshot could not answer it**
  (a hung tool writes no file, and "no file" is indistinguishable from "the window didn't open"). What
  answered it was a **TERM heartbeat printed into the log**: `pre 1…5` → suspect line → `post 1…20`.
- We needed to know where windows land when `POS` is omitted. The desktop screenshot was ambiguous.
  **The log answered it exactly**, because term-ts emits
  `[SYSTEM] WINDOW_PLACED (1076,60 408x308 Mon:4) PLOT 'Pa'` — window geometry to the pixel.
- We learned `SCOPE_XY SIZE` is a **radius** (default 128 ⇒ a 256×256 canvas) — **read straight off a
  `[SYSTEM]` line**, not from any document.

**Two of five findings that night came out of the log, not the images.** That is a debugging instrument, and
it deserves a manual.

Fold in one more thing: **`DEBUG(DEBUG_END_SESSION)`** `{Spin2_v52}`. v55 documents it as the anchor of exactly
this loop — *edit → delete `DEBUG.LOG` → run headless → wait for a non-empty log → read it back.* It is
**absent from our entire Debug Window Manual**, and it belongs to *your* story, not ours.

## 3. Proposed chapters (the spine, not a wish-list)

Each chapter earns its place by serving the loop. If a chapter doesn't, cut it.

1. **The automation loop** — the spine, stated up front. Edit → headless run → structured capture → read back →
   decide. Show the whole cycle working end to end in one page, then unpack it. This is the chapter that makes
   the rest make sense.
2. **Invocation & headless operation** — CLI flags, exit codes, what "headless" actually suppresses, how a run
   terminates deterministically (`DEBUG_END_SESSION`, `DEBUG_LOG_SIZE`, and the `-rd`-equivalent). **How do I
   know the run finished, and finished *successfully*?** — an agent cannot proceed without that answer.
3. **The log as a machine-readable contract** — the highest-value chapter, and the one only you can write.
   The `[SYSTEM]` line grammar (`WINDOW_PLACED`, `DOWNLOAD SUCCESS`, `BAUD_RATE_SET`), timestamps, session
   boundaries, what is guaranteed vs incidental. **Treat it as an API with stability promises**, because
   downstream tooling (ours included) is already parsing it. Say what a consumer may rely on.
4. **Window placement & layout** — the auto-layout algorithm, when it engages (only when `POS` is absent),
   how to override it, and multi-monitor behaviour. **State plainly that this is a term-ts feature PNut does
   not have** (see §4).
5. **Capture: `SAVE` and its sharp edges** — the six forms, which three silently write nothing, the
   filename-last rule, the front-buffer/stale-frame trap under `UPDATE` mode, and the BITMAP-specific
   1×-un-`DOTSIZE`d gotcha. *(We just documented all of these the hard way; they are yours to own too.)*
6. **Settings & preferences** — `pnut-term-settings.json`, baud, fonts, defaults.
7. **Parity with PNut: what differs, and which one to trust** — see §4. **Non-negotiable.**

*(If §1–3 alone carry the weight, this is a strong app-note. If §4–7 fill out, it's a short manual. Draft it
and let the content decide — don't pad to hit a page count.)*

## 4. 🔴 The chapter that is non-negotiable: **a stated parity position**

**term-ts is a port, and it has diverged.** Your own team found and fixed **four live render defects** this
week — SCOPE_XY polar sin/cos swapped, PLOT vertical TEXTSTYLE inverted, PLOT `OPACITY` clamped instead of
wrapped, and `SAVE … CLOSE` never closing the window. Every one of those meant term-ts drew something PNut
does not.

A reader — **and an AI agent generating P2 code** — needs to know:

- **PNut is ground truth for P2 DEBUG behaviour.** term-ts mirrors it. Where they disagree, PNut wins and
  term-ts is the thing to repair.
- **Where term-ts deliberately differs** (auto-layout, headless, cross-platform) that is a **feature**, and
  should be labelled as such — not left for a reader to mistake for chip behaviour.
- **A current parity/divergence table**, kept honest.

We learned this one the expensive way. Our knowledge base currently tells agents that DEBUG windows
"don't overlap" — which is **your auto-layout, recorded as a P2 fact.** It is false for every PNut user. That
defect exists because nobody ever wrote down where the tool ends and the chip begins. **Your manual is where
that line gets drawn.**

## 5. What this manual is *not*

- **Not a DEBUG-display language reference.** The backtick protocol, the nine windows, their directives, the
  packed-data modes — those are the **P2 Debug Window Manual**, and they are tool-agnostic by design. Cross-
  reference us; don't re-teach us.
- **Not a P2 tutorial.**
- **Not a restatement of the in-app help.** If a section could be replaced by a `--help` dump, cut it.

## 6. What we need back

A draft with real content in §1–4 — especially **the log grammar (§3)** and **the parity position (§4)**,
because those are the two things **only you can author** and the two we most need downstream. Structure and
prose we can develop here; the facts have to come from you.
