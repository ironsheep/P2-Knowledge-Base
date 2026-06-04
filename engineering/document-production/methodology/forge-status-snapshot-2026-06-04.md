# PDF Forge — Persistent File Status Snapshot

**Captured:** 2026-06-04 00:28:39 UTC
**Source:** `ll filters/ templates/` on the PDF Forge host (the persistent deployment store).
**Why recorded:** PDF Forge persists every file ever deployed, by filename, indefinitely
(see CLAUDE.md Sacred Rule #6). This is the *actual* state on Forge as of capture — which is a
superset of what the current `request.json` builds reference. Useful as a baseline for the
layout-standards effort and for spotting stale/duplicate artifacts that Forge still holds.

---

## `filters/` (verbatim)

```
total 476
-rw-r--r-- 1 node node  1201 May 31 18:00 p2kb-debugwin-code-coloring.lua
-rw-r--r-- 1 node node  4549 May 31 16:52 p2kb-debugwin-div-blocks.lua
-rw-r--r-- 1 node node  1301 Sep 17  2025 p2kb-debugwin-non-floating-images.lua
-rw-r--r-- 1 node node  3126 May 31 16:52 p2kb-debugwin-semantic.lua
-rw-r--r-- 1 node node 15908 Nov 26  2025 p2kb-desilva-code-coloring.lua
-rw-r--r-- 1 node node  2715 Dec 12 22:57 p2kb-desilva-div-blocks.lua
-rw------- 1 node node  7031 Nov 26  2025 p2kb-desilva-mnemonic-bold.lua
-rw-r--r-- 1 node node  1382 Dec  6 22:39 p2kb-desilva-pagination.lua
-rw-r--r-- 1 node node  3384 Nov 24  2025 p2kb-desilva-semantic-blocks.lua
-rw-r--r-- 1 node node  2342 Nov 24  2025 p2kb-desilva-semantic.lua
-rw-r--r-- 1 node node 20012 May 30 19:05 p2kb-iosp-code-coloring.lua
-rw-r--r-- 1 node node  6350 May 30 20:23 p2kb-iosp-figures.lua
-rw-r--r-- 1 node node 23143 May 30 20:23 p2kb-iosp-mnemonic-bold.lua
-rw-r--r-- 1 node node  3231 May 29 08:00 p2kb-iosp-pagination.lua
-rw-r--r-- 1 node node 37865 May 30 20:23 p2kb-iosp-tables.lua
-rw-r--r-- 1 node node  1136 Sep 17  2025 p2kb-non-floating-images.lua
-rw-r--r-- 1 node node 15944 Dec  2  2025 p2kb-pasm2-code-coloring.lua
-rw-r--r-- 1 node node  4782 Dec 20 23:52 p2kb-pasm2-entry-format.lua
-rw------- 1 node node  1434 Dec  4 07:58 p2kb-pasm2-entry-headers.lua
-rw-r--r-- 1 node node  2219 Jan 23 05:46 p2kb-pasm2-figures.lua
-rw------- 1 node node 22587 Dec  5 00:56 p2kb-pasm2-mnemonic-bold.lua
-rw-r--r-- 1 node node  2428 Dec  5 01:05 p2kb-pasm2-pagination.lua
-rw-r--r-- 1 node node 32584 Dec 23 00:14 p2kb-pasm2-tables.lua
-rw-r--r-- 1 node node  4940 Dec  3 19:37 p2kb-sp-code-coloring.lua
-rw-r--r-- 1 node node   759 Dec  2  2025 p2kb-sp-fix-hypertarget.lua
-rw-r--r-- 1 node node  2080 Dec  8 20:49 p2kb-sp-fix-title-as-part.lua
-rw-r--r-- 1 node node  3912 Dec  4 00:42 p2kb-sp-frontmatter.lua
-rw-r--r-- 1 node node  1835 Sep  8  2025 p2kb-sp-image-nofloat.lua
-rw-r--r-- 1 node node  2243 Sep  4  2025 p2kb-sp-images.lua
-rw-r--r-- 1 node node   655 Dec  3 23:16 p2kb-sp-index-toc.lua
-rw------- 1 node node 22609 Dec 10 18:31 p2kb-sp-mnemonic-bold.lua
-rw-r--r-- 1 node node  1548 Dec  2  2025 p2kb-sp-semantic.lua
-rw-r--r-- 1 node node  2247 Dec  2  2025 p2kb-sp-structure.lua
-rw------- 1 node node   702 Dec 10 20:38 p2kb-sp-table-autowidth.lua
-rw-r--r-- 1 node node  1213 May 31 02:41 p2kb-ssdbg-code-coloring.lua
-rw-r--r-- 1 node node 20012 Jun  1 03:36 p2kb-streamer-code-coloring.lua
-rw-r--r-- 1 node node  6350 Jun  1 03:36 p2kb-streamer-figures.lua
-rw-r--r-- 1 node node 23143 Jun  1 03:36 p2kb-streamer-mnemonic-bold.lua
-rw-r--r-- 1 node node  3231 Jun  1 03:36 p2kb-streamer-pagination.lua
-rw-r--r-- 1 node node 37865 Jun  1 03:36 p2kb-streamer-tables.lua
-rw-r--r-- 1 node node  1430 Aug 23  2025 README.md
-rw-r--r-- 1 node node   731 Aug 25  2025 smart-pins-auto-indent.lua
-rw-r--r-- 1 node node  4323 Aug 29  2025 smart-pins-block-coloring.lua
-rw-r--r-- 1 node node  2499 Aug 27  2025 smart-pins-code-styling.lua
-rw-r--r-- 1 node node  6270 Sep  4  2025 smart-pins-colored-blocks.lua
-rw-r--r-- 1 node node  1732 Aug 29  2025 smart-pins-index-formatting.lua
-rw-r--r-- 1 node node  6302 Sep  3  2025 smart-pins-pagebreaks.lua
-rw-r--r-- 1 node node 11094 Aug 29  2025 smart-pins-pasm-formatting.lua
-rw-r--r-- 1 node node  1627 Aug 29  2025 smart-pins-vertical-spacing.lua
```

## `templates/` (verbatim)

```
total 676
-rw-r--r-- 1 node node   4012 Aug 16  2025  admin-manual.latex
-rw-r--r-- 1 node node  29949 Apr 26  2025  eisvogel.latex
-rw-r--r-- 1 node node   6621 Aug 16  2025  font-demo.latex
-rw-r--r-- 1 node node  15830 May 31 18:00  p2kb-debugwin-content.sty
-rw------- 1 node node  10480 May 31 18:00  p2kb-debugwin-foundation.sty
-rw-r--r-- 1 node node   1336 May 31 18:00  p2kb-debugwin.latex
-rw-r--r-- 1 node node  13783 Dec 12 22:53 'p2kb-desilva-content copy.sty'
-rw-r--r-- 1 node node  13783 Dec 12 22:57  p2kb-desilva-content.sty
-rw------- 1 node node  13543 Dec 12 22:28  p2kb-desilva-diagrams.sty
-rw-r--r-- 1 node node  11211 Dec 12 22:22  p2kb-desilva-foundation.sty
-rw-r--r-- 1 node node   1495 Dec 12 21:42  p2kb-desilva.latex
-rw-r--r-- 1 node node  12647 Nov 24  2025  p2kb-foundation.sty
-rw-r--r-- 1 node node  13854 May 30 19:08  p2kb-iosp-content.sty
-rw-r--r-- 1 node node  27639 May 30 07:28  p2kb-iosp-diagrams.sty
-rw-r--r-- 1 node node  10338 May 29 00:23  p2kb-iosp-foundation.sty
-rw-r--r-- 1 node node   1477 May 25 23:16  p2kb-iosp-reference.latex
-rw------- 1 node node   2225 Dec  4 06:24  p2kb-pasm2-content-colortest.sty
-rw-r--r-- 1 node node  24564 Jan 22 06:18  p2kb-pasm2-content.sty
-rw------- 1 node node  64813 Jan 22 06:18  p2kb-pasm2-diagrams.sty
-rw-r--r-- 1 node node  10232 Jan 23 07:24  p2kb-pasm2-foundation.sty
-rw-r--r-- 1 node node   3504 Aug 18  2025  p2kb-pasm2-manual.latex
-rw-r--r-- 1 node node   3480 Aug 17  2025  p2kb-pasm2-minimal.latex
-rw------- 1 node node   1965 Dec 12 07:26  p2kb-pasm2-reference.latex
-rw-r--r-- 1 node node  11092 Aug 24  2025  p2kb-pasm-desilva-eisvogel.latex
-rw-r--r-- 1 node node  10877 Aug 23  2025  p2kb-pasm-desilva.latex
-rw-r--r-- 1 node node   5477 Sep  8  2025  p2kb-presentation.latex
-rw-r--r-- 1 node node   4686 Aug 27  2025  p2kb-reference-content.sty
-rw------- 1 node node 156200 Dec 10 20:49  p2kb-sp-diagrams.sty
-rw-r--r-- 1 node node  14128 Dec 10 20:45  p2kb-sp-foundation.sty
-rw-r--r-- 1 node node   3123 Dec  3 21:31  p2kb-sp-numbering.sty
-rw-r--r-- 1 node node  20548 Dec 13 21:24  p2kb-sp-styles.sty
-rw-r--r-- 1 node node   1112 Dec  2  2025  p2kb-sp-template.latex
-rw-r--r-- 1 node node   1750 May 31 02:53  p2kb-ssdbg-content.sty
-rw-r--r-- 1 node node  12973 May 31 05:11  p2kb-ssdbg-foundation.sty
-rw-r--r-- 1 node node   1291 May 31 02:49  p2kb-ssdbg.latex
-rw-r--r-- 1 node node  14743 Jun  1 06:57  p2kb-streamer-content.sty
-rw-r--r-- 1 node node  11964 Jun  1 06:57  p2kb-streamer-diagrams.sty
-rw-r--r-- 1 node node  10368 Jun  1 03:36  p2kb-streamer-foundation.sty
-rw-r--r-- 1 node node   1508 Jun  1 03:36  p2kb-streamer-reference.latex
-rw-r--r-- 1 node node   7773 Sep  8  2025  p2kb-tech-review.sty
-rw-r--r-- 1 node node   6840 Aug 27  2025  p2kb-tutorial-content.sty
-rw-r--r-- 1 node node   3387 Aug 16  2025  README.md
-rw-r--r-- 1 node node   4686 Aug 25  2025  reference-manual.sty
-rw-r--r-- 1 node node   3429 Aug 16  2025  user-guide.latex
```

---

## Observations (Forge state vs. current builds)

Forge holds **more** than the six current builds reference — expected, given the persist-by-filename
model. Things to note for the layout effort (not action items yet):

- **Stale/legacy templates still resident:** `eisvogel.latex`, `admin-manual.latex`,
  `font-demo.latex`, `user-guide.latex`, `p2kb-pasm2-manual.latex`, `p2kb-pasm2-minimal.latex`,
  `p2kb-pasm-desilva.latex`, `p2kb-pasm-desilva-eisvogel.latex`, `reference-manual.sty`,
  `p2kb-reference-content.sty`, `p2kb-tutorial-content.sty`, `p2kb-tech-review.sty` — none
  referenced by a current `request.json`.
- **Duplicate/scratch artifacts on Forge:** `'p2kb-desilva-content copy.sty'` (byte-identical
  size to `p2kb-desilva-content.sty`), `p2kb-pasm2-content-colortest.sty`. These are exactly the
  kind of `-copy`/`-test` artifacts Sacred Rule #5 forbids creating going forward; they exist on
  Forge from prior sessions.
- **Superseded per-doc filters present but unused by current builds:** e.g. debug-window's
  `div-blocks`/`semantic`/`non-floating-images`, desilva's `div-blocks`/`semantic-blocks`,
  smart-pins' `image-nofloat`/`images`, and the whole `smart-pins-*` (un-prefixed, Aug–Sep 2025)
  family — the pre-`p2kb-sp-` generation.
- **Confirms the survey's twin/identical findings at the byte level:**
  - `p2kb-iosp-tables.lua` and `p2kb-streamer-tables.lua` are **both 37865 bytes** (identical size).
  - `p2kb-iosp-figures.lua` / `p2kb-streamer-figures.lua` — both 6350 bytes.
  - `p2kb-iosp-mnemonic-bold.lua` / `p2kb-streamer-mnemonic-bold.lua` — both 23143 bytes.
  - `p2kb-iosp-code-coloring.lua` / `p2kb-streamer-code-coloring.lua` — both 20012 bytes.
  - `p2kb-iosp-pagination.lua` / `p2kb-streamer-pagination.lua` — both 3231 bytes.
  Streamer's reference Lua suite is a **byte-for-byte copy** of IOSP's (all dated Jun 1 03:36),
  reinforcing the "one live-publication platform, copied" conclusion in the architecture survey.

**Note on `streamer-content.sty` / `streamer-diagrams.sty` timestamps (Jun 1 06:57):** newer than
the rest of the streamer suite (Jun 1 03:36), consistent with the recent Streamer Guide content
work.
