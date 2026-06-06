# Torture Test — Baseline Review Findings (master list)

**Status:** 🟢 CERTIFIED CANDIDATE READY (v9, 2026-06-06) — **12 verified cases GREEN**, **6 defect
clusters AMBER**, clean compile, 48pp. Pending Stephen's manual-regen walk + commit. Greened:
1.1, 1.2, 1.5, 2.3, 3.1, 3.3, 5.2, 6.3, 7.2, 7.3, 8.2, Ch9-opener. **Held amber pending closer
check** (conservative — verify before greening): 1.4 (deep-heading needspace coverage), 3.2 (quote
line-strand shares Ch4's widow risk), 9.1 (whitespace-tolerance = judgment). **Instrument polish
deferred to post-walk:** #29 EXPECT-box separation (partly inherent to the move-whole demo),
1.3/#14 heading-cohesion rig, 5.3 table-caption source syntax.

(history below) RESOLVE IN PROGRESS — inventory CLOSED (32 findings, Ch 1–9).

**Step A — v6 (2026-06-05): root cause of the entire `under-force` cluster found & fixed.**
`\leavebottom` carried a hard-coded `0.32\textheight` floor that clamped **every** case ~2.9in
above the page foot, so short content never reached a boundary (only content taller than 2.9in —
big callouts, 2-figures, 60-row table — split at all). Fix: parameterized the floor (small default
`0.04\textheight` so strand/split cases reach the foot; figure cases pass `0.32\textheight` so their
figures aren't ejected). **v6 render: 37 → 48 pp (+11), compile log clean (0 dropped), figures intact
(27 drawings on the 1.2 page), and forced content now lands at the foot (verified visually on 3.1).**
Reclassifying each under-force case case-by-case as it now fires.

**v6 reclassification pass (2026-06-06):** under-force cases now reach the foot and overwhelmingly
behave correctly — **3.1, 7.2 confirmed HANDLED** (clean split / no detach). **CORRECTION: Ch4 →
DEFECT-BASELINE** — its EXPECT note says the foundation has no clubpenalty/widowpenalty, so v6's
clean split was *coincidental*, not protection. (Lesson: verify against the EXPECT note + implementation,
not the visual.) 3.2, 3.3, 5.2, 8.2, 9.1, 9.1.1 provisional HANDLED — but each must be checked against
its EXPECT note in Step B, not just visually. **TBDs:** Ch2 blank page RESOLVED; 6.3 HANDLED
(moved-whole permitted); 5.3 caption → TEST-FIX (unsupported `Table:` syntax). **#29 EXPECT-box
separation CONFIRMED pervasive** — main remaining rig fix. **Genuine DEFECT-BASELINE list:** continuation
(2.1/7.1/8.1), table-fit (6.1/6.2), part→chapter (15), long-line (2.2), long-table (16), **widow-orphan (Ch4)**.
**Process:** `document-finalize` (gather-then-resolve). Companion: `punch-list-maintenance`.
**Subject:** the v0.3 baseline render of `P2-Layout-Torture-Test.md` (the layout-standards harness).
**Render/verify mechanism:** `/forge-test` interactive round-trip (daemon must be ON). PyMuPDF to
render/inspect any page. Re-baseline once after the whole batch.

## How this list is used (the agreed plan)

1. Stephen walks the baseline PDF and hands findings **a group at a time**.
2. After each group, record it here (append to the table, new group heading).
3. When Stephen says **"final group, recorded"** → the inventory is COMPLETE; stop gathering.
4. Then **resolve** (gather-then-resolve — no auditing mid-gather):
   a. **Audit the HANDLED-UNVERIFIED worklist first.** Per item: confirm the rule is load-bearing
      (toggle it off → re-render → the case strands) AND matches the documented standard
      (`../../../methodology/manual-layout-standards-INPUTS.md` / `-USER-PREFERENCES.md`) AND
      generalizes across sibling cases. → `HANDLED-VERIFIED`, or reclassify to `DEFECT-BASELINE`.
   b. Cluster the `DEFECT-BASELINE` + `TEST-FIX` findings by shared fix → order to avoid rework →
      apply the whole batch with **no render between**.
   c. Re-baseline once → verify each finding is resolved.

## Classify every finding (determines whether the TEST changes)

- **TEST-FIX** — the instrument is wrong/incomplete (a case that doesn't reproduce its defect, a
  wrong EXPECT box, a harness/forcing artifact, a missing concern). → edit the torture doc.
- **DEFECT-BASELINE** — the test *correctly* shows a real layout defect. → do NOT change the test;
  it becomes a template fix target for the later fixes phase. Record but don't "fix" in this pass.
- **HANDLED-UNVERIFIED** *(default for any pass)* — the case forces its boundary and renders correctly because the desired behavior is **already implemented** in the stylesheet draft (e.g. `\needspace{4\baselineskip}` / `\nobreak`). At gather time we do **not** stop to confirm it — record and move on; it goes on the **verification worklist** (audited in resolve step 4a).
- **HANDLED-VERIFIED** — a HANDLED-UNVERIFIED item whose resolve-phase audit passed: the rule is load-bearing (toggle) AND matches the documented standard AND generalizes across sibling cases. Keep as a regression guard; no template work. (A failed audit → reclassify to `DEFECT-BASELINE`.)
- **TBD** — needs me to pull up the page and investigate before classifying.

> **Framework note (2026-06-05):** the torture stylesheets are the **standard-in-progress**, not a pristine/unprotected base — so the baseline is a *mix*: some defects already HANDLED, some still open. "Demonstrate the failures" therefore means demonstrate the **remaining** ones. (Open design choice: keep evolving-standard, or temporarily strip protections to show every raw defect as a clean "before" — Stephen to decide.)

## Findings

| # | Group | Location (ch / §/ case) | Observation (see vs. expect) | Class | Cluster | Status |
|---|-------|-------------------------|------------------------------|-------|---------|--------|
| 1 | G1 | Ch1 §1.1 Orphaned Heading | Tested heading (1.1.1) held its body — no strand. **Cause found in the templates:** orphan control is already implemented — `\needspace{4\baselineskip}` after headings (foundation.sty:209, content.sty:120) + `\nobreak`. Without those lines 1.1 would strand. | HANDLED | — | not a defect, not a broken case — the standard-draft's orphan protection is working — on the verification worklist for resolve step 4a (toggle `\needspace`/`\nobreak` + check vs the standard + confirm it covers all heading depths). |
| 2 | G1 | Ch1 §1.2 Heading+Intro+Diagram+Caption block | All four pieces moved together to the next page; none detached. | HANDLED-UNVERIFIED | — | keep-together held ("room on pg 1" is the forced `\leavebottom{1.6in}` gap; block taller than the space left → moved as a unit). On the worklist: confirm which rule held it + matches standard. |
| 3 | G1 | Ch1 §1.3 Heading followed by Code | Code forced low; heading 1.3 at page TOP; both on same page, no jump. | TEST-FIX | — | heading sits at page top (after `\clearpage`) with the EXPECT box + `\leavebottom` BETWEEN it and the code → adjacency broken, heading can't strand. Case doesn't test heading/code cohesion at a boundary. |
| 4 | G1 | Ch1 §1.4 Deep Nesting | All nested headings + body stayed on one page; nothing crossed to the next page. | TBD | — | ambiguous: either **under-forced** (boundary never reached) OR `\needspace` is keeping the nested headings with their bodies (HANDLED). Pull the page in resolve to tell which. |
| 5 | G2 | Ch1 §1.5 Long/Wrapped Heading | Heading wraps to 2 lines (as expected); paragraph bound below it; all at top of page. **No `\leavebottom`** — 1.5 is a spacing/binding test, not a page-break test, so top-of-page is correct. | HANDLED-UNVERIFIED | — | confirm wrapped-heading spacing + binding vs standard; also verify whether first-paragraph-after-heading **indent** is intended (user noted it's indented). |
| 6 | G2 | Ch2 intro → §2.1 boundary | ~~spurious blank page~~ → **v6: Ch2 intro p11 → §2.1 p12 are consecutive, NO blank page.** Reflow resolved it (the v5 "blank page" was the intro page's blank tail). | RESOLVED | — | not reproduced in v6. |
| 7 | G2 | Ch2 §2.1 Listing splits across page (C10) | **✅ FIXED v21** — breakable styled boxes now carry a `contmarkers` tcolorbox style: an italic ``continues on next page →'' marker in the footer on the breaking part and ``↪ continued from previous page'' in the header on the resuming part, drawn just outside the frame so they never overprint content; the colored frame/fill stays intact on both parts. Verified p12→p13 (code listing). GREEN. | FIXED → green | continuation | **Phase-2 fix #6 complete (C10).** Shared across all five code/callout boxes. |
| 8 | G2 | Ch2 §2.2 Long code lines | **↻ RECLASSIFIED v22 — PROCESS, not template.** Fix #4's `breaklines` auto-wrap was **reverted**: a typeset wrap can't break a comment + re-indent it nor add a language line-continuation, so it renders wrong code AND hides the problem. Code boxes now stay hard (over-long lines overflow *visibly*). Standard: each box has a calibrated **column budget K** (measured via the v22 ruler = **76 cols** for the shared IOSPBlock style), recorded in each manual's `creation-guide.md`; the `prepare-manual` line-length audit flags any source line > K; the author shortens it. Case 2.2 now carries a blue ProcessBox + the calibration ruler + deliberately-overlong lines (the audit's self-test fixture). | PROCESS (build audit + authorship) | line-length | **Supersedes fix #4.** Not render-green by design — verification is the audit catching the demo lines. |
| 9 | G2 | Ch2 §2.3 Code block at page foot | Code box stayed together, but likely **not stressed** (box too short to need breaking); only the §2.3 section heading sits above the `\leavebottom` gap — no subheading adjacent to the code. User: "not sure 2.3 is demonstrating what you want." | TBD | under-force | likely TEST-FIX (rig: add a subheading adjacent to the code and/or lengthen the listing so the box reaches the foot under stress). Pull page in resolve. |
| 10 | G3 | Ch3 §3.1 List splits across page | ~~not splitting~~ → **v6: reaches the foot and splits CLEANLY** (items 1–5 p17, 6–10 p18; correct numbering, no strand/restart/mid-item break). | HANDLED-UNVERIFIED | (was under-force) | floor fix un-stuck it; list-split behavior is correct → verify the rule in Step B. |
| 11 | G3 | Ch3 §3.2 Block Quote at boundary | Paragraph not close enough to the page bottom; **nothing splits** to the next page. | TEST-FIX | under-force | quote never reaches the boundary — strengthen forcing / lengthen quote. |
| 12 | G3 | Ch3 §3.3 Box Formula at boundary | Boxed formula too short (2 lines); not overrunning margin, not near the bottom — **can't tell**. User: "need a longer example." | TEST-FIX | under-force | under-forced + example too short. Lengthen the boxed formula so it must split; strengthen forcing. |
| 13 | G4 | Ch4 Widows/Orphans in Prose | **✅ FIXED v10** — foundation now sets `\clubpenalty`/`\widowpenalty`/`\displaywidowpenalty = 10000`; paragraph splits 4 lines/3 lines across p22→p23 (≥2 each side, no widow/orphan). GREEN. | FIXED → green | widow-orphan | **Phase-2 fix #1 complete.** |
| 14 | G4 | **Global / instrument-wide** | Add a **subheading immediately before each tested paragraph/block** (not just the chapter/section title), so heading↔content cohesion is observable AND the content is positioned to be driven to the foot. | TEST-FIX | rig-redesign | cross-cutting rig improvement; pairs with the `under-force` fix and resolves the heading-at-top cases (1.3, 2.3). |
| 15 | G5 | Part I/II/III opener → chapter heading | **✅ FIXED v12** — pinned-chapter spacing fix (+60pt in `\conditionalclearpage`, canceling the chapter's -38pt top-pull) flows the chapter title cleanly below the part intro on all 3 parts (verified Part I/II/III). GREEN. | FIXED → green | part-flow | **Phase-2 fix #2 complete.** |
| 16 | G5 | Ch5 §5.1 Long table (60+ rows) | **✅ FIXED v13** — `handle_auto_shrink_table` now routes wide tables with >20 rows to a breakable `longtblr` (`rowhead=1`) instead of a non-breaking `tblr`. Table breaks across p24→p25→p26, repeats its header on each continuation page, and shows "Table 5.1: (Continued)" + "Continued on next page" markers. GREEN. | FIXED → green | long-table | **Phase-2 fix #3 complete.** Narrow `tall` branch deliberately untouched (compress-to-one-page by design). |
| 17 | G5 | Ch5 §5.2 Table forced to boundary | Short table **not close enough to the foot** to test (kept-whole push). | TEST-FIX | under-force | under-forced. |
| 18 | G5 | Ch5 §5.3 Captioned table (split) | Table **not close enough to the foot** to split. | TEST-FIX | under-force | under-forced. |
| 19 | G5 | Ch5 §5.3 Captioned table (caption) | **v6: table renders (p30) but caption is ABSENT.** Source uses Pandoc `Table: …` syntax, which this pipeline drops; figures use a working `::: {.figurecaption}` div. | TEST-FIX | caption | fix source to a supported table-caption mechanism. **Flags a standard question:** does the pipeline support table captions at all? If not → DEFECT-BASELINE for the manuals. |
| 20 | G6 | Ch6 §6.1 Many Wide Columns | **✅ FIXED v20** — 10-column tables now route to the token-fit wide branch (`<=12` cols) with a `\tiny` tier. The width allocator was made identifier-aware: only *hard* units (underscores/digits/acronyms) set a column's floor (×1.25 for wide glyphs); ordinary words hyphenate to a 6-char soft floor; `usable` lowered to 0.93 so colsep no longer compresses columns. Verified p31: all 10 columns fit, mnemonics whole and clear of Bits/Clk, prose wraps cleanly, no overlap. GREEN. | FIXED → green | table-fit | **Phase-2 fix #5a complete.** Governed by symbol-name constraint #23 — no splitting. |
| 21 | G6 | Ch6 §6.2 Long Unbreakable Tokens (narrow col) | **✅ FIXED v20** — the symbol/description (`is_instr_desc`) allocator sizes column 1 to its longest unbreakable token (≈60 chars/`\linewidth`, floor 0.18, cap 0.55) instead of a fixed 0.18. Verified p32: all three 30–32-char symbols sit whole in column 1, no overlap into the description. GREEN. | FIXED → green | table-fit | **Phase-2 fix #5b complete.** Solved via column-width strategy, NOT token splitting (#23). |
| 22 | G6 | Ch6 §6.3 Tall table forced to boundary | **v6: 16-row table moved WHOLE to p34** — which the EXPECT permits ("either breaks OR moves whole"). The "weird" was the #29 EXPECT-box staying on p33. | HANDLED-UNVERIFIED | rig | not a defect; table too short to exercise the *break* path — mild TEST-FIX: lengthen it. EXPECT-box separation = #29. |
| 23 | G6 | **Standard / design constraint** | **Never split symbol names** (even at the underscores that look like split points) — splitting harms reader comprehension of the symbol. Long symbols in tables must be made to fit by **font-size reduction / column-width strategy**, keeping every token whole. Recurs across multiple manuals. | STANDARD | table-fit | add to `methodology/manual-layout-standards-USER-PREFERENCES.md`; governs the #20/#21 fix. See [[reference_smartpin_symbols_unicode]]. |
| 24 | G7 | Ch7 §7.1 Diagram forced to a boundary | **✅ FIXED v21** — the case is a single [H] diagram (not a breakable box). Forced near the page foot, it cannot fit in the space left, so the page breaks before it and the whole diagram + caption move to the next page rather than overrunning the bottom margin. Verified p35→p36 (VGA timing diagram + caption together at the top of p36, nothing off-page). GREEN. | FIXED → green | continuation | **Phase-2 fix #6 complete (figure arm).** A graphic can't split, so the standard is move-whole, not signpost. |
| 25 | G7 | Ch7 §7.2 Figure + long caption at foot | **v6: figure + long caption now at the foot of p37, stayed welded (no detach).** | HANDLED-UNVERIFIED | (was under-force) | keep-together works once forcing reaches the foot → verify in Step B. |
| 26 | G7 | Ch7 §7.3 Two figures back-to-back | First figure+caption stayed on pg 1; second figure+caption moved to pg 2 — clean split, captions intact. User: "correct but unverified." | HANDLED-UNVERIFIED | — | back-to-back figure split looks correct; confirm rule + standard in resolve. |
| 27 | G8 | Ch8 §8.1 Long callout spans page (C11) | **✅ FIXED v21** — the AntipatternBlock callout shares the same `contmarkers` style as the code boxes, so a long callout splitting across a page gets the footer ``continues on next page →'' and header ``↪ continued from previous page'' markers, colored fill/border intact on both parts. Verified p41→p42 (pink callout, both markers, styling unbroken). GREEN. | FIXED → green | continuation | **Phase-2 fix #6 complete (C11 = C10 = C9).** (Box/heading separation still tracked separately → #29.) |
| 28 | G8 | Ch8 §8.2 Short callout at boundary | 8.2 heading stayed; EXPECT box + short callout went to the next page; callout **didn't go down far enough** to split or move. | TEST-FIX | under-force | under-forced (`\leavebottom{1.5in}` insufficient for the short callout). |
| 29 | G8 | **Instrument rig — EXPECT box placement** | The unbreakable EXPECT box **separates from its case heading / is pushed to the next page** with the forced content (seen in 6.3, 8.1, 8.2). Made unbreakable to fix a measurement bug, but now it jumps pages. | TEST-FIX | rig-redesign | anchor the EXPECT box to its case heading; force only the tested content. Pairs with #14. |
| 30 | G9 | Ch9 opener — chapter continuation | EXPECT says the chapter should **continue on the previous page**, but Ch9 **broke to a new page** (its own page after the Ch8 anti-pattern block). | TBD | flow | check EXPECT intent — is break-to-new-page the defect (chapter-start-flow), or is a new page expected? Pull EXPECT + page in resolve. |
| 31 | G9 | Ch9 §9.1 Keep-together unit leaves tail blank | Unit all showed on the **same page** — the "leave the tail blank / move whole" behavior didn't trigger. | TEST-FIX | under-force | under-forced — didn't reach the boundary. |
| 32 | G9 | Ch9 §9.1.1 | **Not demonstrated** — not pushed down far enough to show anything. | TEST-FIX | under-force | under-forced. |

## Authoritative classification — Step B by EXPECT note (2026-06-06)

Read every EXPECT box. The author's `(today)`/`(current)`/"expected to fail" notes are the truth
(they name what is/isn't implemented), so this supersedes visual guesses.

**DEFECT-BASELINE (stay amber — real template-fix targets):**
- **part→chapter overlap** — Part I/II/III intros (#15): "chapter title overlaps the intro lines"
- **continuation** — 2.1 (code), 8.1 (callout): "(today) splits with NO continuation markers"; 7.1 (diagram): overruns because figures filter pins `[H]`
- **long-line** — 2.2: "runs past the right edge off the page"
- **widow-orphan** — Ch4: "(today) no clubpenalty/widowpenalty"
- **long-table** — 5.1: "(current) runs off the bottom… emitted as non-breaking tblr not longtable"
- **table-fit** — 6.1: "(current) columns on top of each other"; 6.2: "(current) token runs out of its column"

**HANDLED (→ green VerifiedBox; no fail-note + correct behavior):**
- confirmed: **1.1** (needspace orphan), **1.2** (keep-together block), **1.5** (wrapped heading),
  **3.1** ✅, **7.2** ✅, **7.3** (two-figure clean split), **Ch9 opener** (#30 — A3 *wants* a fresh
  page; it broke correctly → not a defect)
- keep-whole/keep-together, expect green after a confirming render: **2.3, 3.2, 3.3, 5.2, 6.3, 8.2, 1.4**

**TEST-FIX (instrument, not template):** 1.3 (heading sits at page top — push it to the foot);
5.3 (caption source syntax); #14 subheading-adjacent cases; #29 EXPECT-box anchoring;
9.1 (whitespace-tolerance knob = the `\leavebottom` floor — tune the tail-blank tolerance).

## Clusters & fix order

**Inventory CLOSED — 32 findings, Ch 1–9.** Rework-safe order: instrument before template fixes;
standards before application.

**Step A — Instrument rebuild** (FIRST — under-forced cases can't reveal defects until the rig works):
- `under-force` (10–12): 3.1, 3.2, 3.3, Ch4, 5.2, 5.3, 7.2, 8.2, 9.1, 9.1.1 (+2.3, 1.4) — stronger
  forcing / longer examples so content actually reaches the page foot.
- `rig-redesign`: #14 subheading-adjacent cases · 1.3 heading pushed to the foot (not page top) ·
  #29 anchor the EXPECT box to its case heading (keep it unbreakable; stop it jumping pages).
- → re-render → **reclassify** each now-firing case as HANDLED-UNVERIFIED or DEFECT-BASELINE.

**Step B — Verify HANDLED-UNVERIFIED** (1.1, 1.2, 1.5, 7.3): re-check under the strengthened forcing
(must still hold) + toggle the implementing rule (`needspace`/`nobreak`) + check vs the standard →
HANDLED-VERIFIED, or → DEFECT-BASELINE if it strands under real stress.

**Step C — Resolve TBDs:** Ch2 blank page (stray `\clearpage` vs `openright` verso), 2.3 rig,
5.3 missing caption (source vs render), 6.3 weird table jump, Ch9 chapter-flow (#30).

**Step D — Record STANDARD #23** (never split symbol names) into
`../../../methodology/manual-layout-standards-USER-PREFERENCES.md`.

**Step E — (NEXT session, after Stephen walks the rebuilt "before")** template defect-fixes by cluster:
- `continuation` (2.1 · 7.1 · 8.1) — one C9/C10/C11 signposting mechanism across code/callout/figure
- `table-fit` (6.1 · 6.2) — font-size / column strategy per #23
- `flow` (15 part→chapter) · `long-line` (2.2) · `long-table` (16, split + repeat header)

## Render-once gate

_(after the batch is applied: one `/forge-test` round-trip → verify each finding above → re-commit
the corrected baseline as the true "where we started.")_
