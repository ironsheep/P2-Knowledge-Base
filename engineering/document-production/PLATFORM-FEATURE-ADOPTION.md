# Platform Feature Adoption — the per-document state table

**One table. Rows are documents, columns are platform features that each document
adopts at its own next release.** This is the master list: it answers "has this
document taken feature X yet," and it is what `prepare-manual` consults before
staging.

**Why this exists.** A shared-platform feature that needs per-document work cannot
be turned on set-wide — that would churn every published corpus to fix one. So
adoption is deliberately per document, at its next natural release, for any reason.
Until then the document is unchanged, never broken.

**Why it is ONE table.** Adoption used to live in three places — a per-feature file,
prose in the punch list, and the roster's coarse `Platform` column. The per-feature
file recorded the rule correctly and was then passed over about a dozen times
(**F-301**), because nothing consulted it at the moment of release. State lives here;
each feature's *mechanism* stays in its own document, linked below.

**Legend:** ✅ adopted · 🔧 adopting/proving · ⏳ owed at next release · — n/a

---

## The table

| Document | Type | Metadata single-source | Rights metadata | Cross-ref filter | Generated example headers |
|---|---|:--:|:--:|:--:|:--:|
| Getting Started | manual | ⏳ | ⏳ | ⏳ | **✅** ¹⁰ |
| I/O & Smart Pins | manual | ⏳ | ⏳ | ✅ ¹ | 🔧 ¹¹ |
| **Assembly Reference** | manual | **✅** ⁹ | **✅** ⁹ | **✅** ⁹ | — |
| DeSilva Tutorial | manual | ⏳ ² | ⏳ | ⏳ | **✅** ¹⁰ |
| Debug Window | manual | ⏳ | ⏳ | ⏳ | **✅** ¹⁰ |
| **Streamer Guide** | manual | **✅** ⁷ | **✅** ⁸ | ✅ | — |
| Architect's Guide | manual | ⏳ | ⏳ | ⏳ | — |
| Interpreters & Emulators (XBYTE) | manual | ⏳ ³ | ⏳ | ⏳ | ✅ |
| **Single-Step Debugger** | manual | **✅** | ⏳ | ⏳ | — |
| **PNut-Term-TS User Guide** | guide | **✅** | ⏳ ¹² | ⏳ ⁶ | — |
| P2AN001 … P2AN007 | app-note | ⏳ ⁴ | ⏳ | ⏳ | ⏳ ⁵ |
| Layout Torture Test | instrument | — | — | — | — |
| AI Privacy Guide | guide | — | ⏳ | — | — |

¹ Wired in `request.json` with the correct filter ordering and shipped in released
PDFs, **but no visual audit is recorded** — the pilot row was left mid-flight. Close
the audit at its next release rather than assuming it passed.
² Its template declares **no `\title` and no `\author` at all**, and cover vs
`request.json` disagree on **both** title and subtitle. Needs the conflict resolved
(the cover wins) before it can convert.
³ Its template still carries the pre-v1.1.0 name `P2 XBYTE Programming Guide`; the
shipped cover reads *"P2 Interpreters & Emulators Guide"*.
⁴ All seven share `p2kb-appnote-reference.latex`, which hardcodes
`\title{P2 Application Note}`. Converting the shared template converts all seven at
once — `request.json` `metadata.title` already equals each cover title.
⁶ **Deferred at the v1.0.0 prepare (2026-08-19), Stephen's call, reason recorded:** adopting
cross-ref requires a visual audit of the auto-links in the rendered PDF, and that audit would gate
a release explicitly scoped to *not* wait — the same reasoning that removed the reviewer questions.
Not a silent pass-over (which is what F-301 was); take it at the next release.
⁵ **App notes owe a PREREQUISITE before this column can move: fence captions.**
`sync-manual-examples.py` and `verify-example-corpus-identity.py` both pair a corpus file to
its printed listing by ```` ```{.spin2 caption="<name>.spin2"} ````, and **no app-note master
carries a single caption** — so identity reads RED (every file an orphan) and header adoption
cannot even be attempted. **At each app note's next adjustment or update, add the captions to
its printed fences.** Measured 2026-08-22: **31 of the 32 files are already byte-identical to
a printed fence**, so this is annotation only — no code moves, and it flips that note's
identity gate to GREEN. Per-note counts and the full rationale: `PUNCH-LIST.md` -> "App-note
example corpora have never been gated at all".

Two cautions for whoever does it. **Do not run `build-example-library.py` on an app note
before its captions exist** — dry-run against P2AN003 found ZERO of its six examples and would
have written an empty library over a good corpus; use `--repack` until then. And
`P2AN006/examples-library/isp_stack_check.spin2` is a shipped **utility object** carrying its
own hand-written header, not an example — it is why P2AN006 reads 4+1 rather than 5, and
whatever convention lands must let a corpus hold a non-example file without flagging it.


¹⁰ **Getting Started + DeSilva — generated example headers adopted 2026-08-22, and this is the
one feature whose proof is NOT a rendered PDF.** `--adopt` writes only the `.spin2` files; it
never touches `opus-master`, and the identity gate compares the **body** once a file carries a
generated header. So the header exists solely in the archive a reader downloads, the printed
listing is unchanged, and **no re-render was needed or performed** — which is exactly why these
two could go first while their manuals stay unreleased.

Verified on the shipped artifacts instead: corpus identity GREEN (4/4 and 3/3, body-compared),
all 7 files compile clean on pnut-ts, the `.spin2` ASCII gate passes, and both `-src.zip`
archives were repacked and re-verified byte-identical to their corpora with the fleet still at
12/12 current.

**A defect caught before it spread.** The header's `Manual.....` line is derived from the
CHANGELOG H1, and the regex only matched `<Title> - Changelog`. This fleet writes three shapes —
`P2 Debug Window Manual: Change Log` (colon, two words) and `Changelog: Getting Started with the
Propeller 2` (title last) also occur — so Getting Started, Debug Window and IOSP silently fell
back to the **slug**. The first sync wrote `Manual..... p2-getting-started-guide` into files a
reader opens. Fixed in `sync-manual-examples.py` to match all three, re-synced, and XBYTE
regression-checked unchanged. Had it gone unnoticed, the slug would have shipped in 49 more
headers at the Debug Window / IOSP adoption.

¹¹ **I/O & Smart Pins — headers adopted in source 2026-08-22, ZIP DELIBERATELY NOT REPUBLISHED.**
Unlike the other three, IOSP's ASCII fixes changed the example BODIES (`µs`->`us`, `°`->` deg`,
`→`->`->`, `Ω`->`ohm` in comments), so the printed listings in `opus-master` changed with them.
The **shipped v1.0.9 PDF still prints the old characters.** Republishing the archive now would
hand a reader a file that disagrees with the book it came from, which is the one promise the
corpus makes. So `p2-io-and-smart-pins-user-guide-src.zip` is knowingly left stale and
`verify-published-zip-currency.py` reads **RED for this document by design** until IOSP renders.

At that render, in order: re-run `sync-manual-examples.py --check` (the header carries the
released version, so it needs a re-sync once the version bumps), then repack the ZIP, then
confirm currency GREEN. Everything else is done and gated: identity 15/15 body-compared, ASCII
clean, 15/15 compile.

Contrast Debug Window, adopted the same day and flipped to ✅: its 34 ASCII violations were all
in `figure-generators/` and `audit/verification-tests/` — internal tooling, never printed and
never shipped — so its example bodies never moved and its archive still matches the shipped
v1.1.3 PDF exactly.

¹² **PNut-Term-TS — rights are HALF-WIRED, and rendering it as-is would ship a MALFORMED rights
string.** Found 2026-08-22 while re-opening the guide for its visual pass. Its template
`p2kb-pnut-term-ts.latex` binds **five** of the seven `\Doc*` macros — Title, Subtitle, Version,
Date, Author (`:23-27`) — and binds **neither `\DocCopyright` nor `\DocLicense`**. `request.json`
declares no `copyright`/`license` either.

That combination is exactly **F-319**: the platform's rights guard does not fire for a document
whose rights macros sit at their `\providecommand{}` defaults, so `pdfkeywords` is emitted anyway
and comes out as the literal `"; licensed under "` — which is what Assembly's first v3.1.7 render
produced. **This guide is F-319's first live victim, not merely a candidate.**

Fix BOTH halves before the render (the two-part rule, and here it is 5-of-7 rather than 0-of-7,
which is harder to spot):
1. add `\renewcommand{\DocCopyright}{$copyright$}` and `\renewcommand{\DocLicense}{$license$}`
   to the template beside the other five;
2. add to `request.json` metadata, sourced from **this guide's own** licence page — it is the ONE
   document in the set that is **Iron Sheep ALONE**, no Parallax:
   `"copyright": "Copyright 2026 Iron Sheep Productions, LLC"`, `"license": "CC BY-SA 4.0"`.

Then `audit-pdf-metadata.py --require-rights` gates it. Note this also removes the guide as a
possible negative control for F-319 — use the layout torture test instead.

⁷ **Streamer Guide, verified on the returned v1.1.0 PDF 2026-08-21 — not on staging, not on a clean compile log.** Page 1 reads the four expected lines exactly (title · subtitle · `August 2026` · `Version 1.1.0`), so the `\Doc*` macros resolved and the blank-cover failure mode did not fire. The info dictionary carries Title, Subject and Author, where v1.0.9 carried **none of the three**. `Subject` reads *"Comprehensive Reference for Propeller 2 Streamer Hardware"* — the intended change, since `request.json` and the cover had disagreed and the recorded rule is that the cover wins. Zero occurrences of `1.0.9` or `June 2026` across all 91 pages. Re-confirmed on the 2026-08-22 build that added rights (footnote 8): identical page and word counts, and **zero pages whose text differs** — the metadata change moved nothing.


⁹ **Assembly Reference — declared 2026-08-22 for v3.1.7, NOT yet proven.** All three land in one
`request.json` edit: `p2kb-platform-crossref` added second in `lua_filters` (the Streamer's adopted
ordering), and `copyright` + `license` added to `metadata`. The copyright string is sourced from
**this document's own** licence page — *Copyright 2025-2026 Iron Sheep Productions, LLC and Parallax
Inc.* — a year RANGE, unlike the Streamer's single 2026; the gate's check 6 compares metadata rights
against that page, so the range is what has to be declared. `version` also changed form, from
`"v3.1.6"` to `"3.1.7"`: the gate substring-matches the declared version against page 1's rendered
text, which prints *"Version 3.1.7"*, and a leading `v` would never be found there.
**Negative control run 2026-08-22** against the *released v3.1.6* PDF with the new `request.json`:
the gate reported `title-empty`, `subject-empty`, `author-empty`, `cover-version-missing`,
`stale-version`, `rights-declared-not-emitted` and `rights-missing` — it reads the artifact, not the
declaration, and it is armed.

**✅ PROVEN on the returned v3.1.7 PDF, 2026-08-22 (505pp).** `audit-pdf-metadata.py --prior 3.1.6
--require-rights` reads **CLEAN**, all seven declared fields verified in the artifact: Title *"P2
Assembly Language Reference Manual"*, Subject *"Complete PASM2 Instruction Set Documentation"*,
Author, and Keywords *"Copyright 2025-2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed
under CC BY-SA 4.0"* — where v3.1.6 carried **none of the four**. Cover page 1 reads
`August 2026` / `Version 3.1.7`, and `3.1.6` appears **zero** times across all 505 pages.
Cross-ref filter live at **+87 internal links** (3142 → 3229).

**Adoption took TWO parts, and the first render proved it.** Declaring the keys in `request.json`
is only half: the manual's own `*-reference.latex` must bind pandoc variables to the platform
macros with seven `\renewcommand{\Doc*}` lines. Assembly's template instead hardcoded
`\title`/`\author`/`\date{December 2025}`, which are **inert** here because the foundation
populates the info dictionary from `\Doc*` and deliberately not from `\@title`/`\@author`. Render 1
came back with all four fields EMPTY and `Keywords` reading literally `"; licensed under "`.
**Any document adopting this must edit its template, not just its request.json.**

⁸ **Rights metadata (F-316) — proven on the returned v1.1.0 PDF 2026-08-22.** The PDF's `Keywords` now reads *"Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed under CC BY-SA 4.0"*, where every published PDF in the set previously carried **no** machine-readable rights at all. Fed per document from its own `request.json` — never a platform constant, because 17 documents are ISP + Parallax and `pnut-term-ts-user-guide` is ISP alone. Gated from here on by `audit-pdf-metadata.py --require-rights`, which verifies each declared value ROUND-TRIPPED into the artifact rather than merely that something rights-shaped is present. XMP `dc:rights` is not yet emitted (needs `hyperxmp`; unconfirmed in the Forge's TeX Live) — `Keywords` is the carrier today.

---

## The features

### Metadata single-source — `\DocTitle` / `\DocSubtitle` / `\DocVersion` / `\DocDate` / `\DocAuthor`

**Mechanism:** `platform/templates/p2kb-platform-foundation.sty` (§ DOCUMENT METADATA).
**Finding:** F-300. **Proven:** interactive daemon, 2026-08-19, four round-trips.

Every identity string lives once, in the document's `request.json` metadata, and
reaches **both** the PDF info dictionary and the cover page from there. The macros
carry the **value**; the cover keeps its own **presentation** — which is how
PNut-Term-TS prints *"Version 0.9.0 — Tool Developer Review Draft"* from a stored
value of `0.9.0`.

**To adopt a document:**
1. In its `.latex` template, after `\usepackage{p2kb-platform-foundation}`, add the
   five `\renewcommand`s from the pandoc variables, then `\title{\DocTitle}`,
   `\author{\DocAuthor}`, `\date{\DocDate}`. **`\renewcommand`, not `\newcommand`** —
   the foundation has already `\providecommand`'d them.
2. In `opus-master/front-matter.md`, replace the cover's literal title / subtitle /
   date / version / publisher line with the macros. Keep any surrounding wording
   ("Version", a qualifier) in the cover.
3. Normalize `request.json` `metadata.version` to the **bare number** — the cover
   supplies the word "Version".
4. Round-trip and **read the rendered PDF**: cover unchanged, and
   `pymupdf.open(pdf).metadata` carries title / author / subject.

**Two traps, both hit on the first conversion.** Removing a hand-placed `\\` from a
subtitle lets it re-break badly — constrain the measure (`minipage`) rather than
re-hardcoding the text. And a `minipage` sets its own first baseline, which silently
ate 9.5pt of the title-to-subtitle gap; measure the gap before and after rather than
eyeballing it.

An unconverted document is **safe**: the foundation `\providecommand`s all five
macros empty, so it writes exactly what it wrote before.

### Cross-reference filter — `p2kb-platform-crossref.lua`

**Mechanism + the mandatory filter ordering:** `CROSSREF-FILTER-ADOPTION.md`.
**Leak:** F-301.

Auto-links in-prose "Chapter N" / "Appendix X" / "§N.N" to their anchors. Adoption is
two steps and the second is not optional: add the filter to `request.json`
`lua_filters` **before `p2kb-platform-tables`**, then **visually audit** the rendered
PDF — every auto-link points where it should and nothing was wrongly linked.

### Generated example headers — `sync-manual-examples.py`

**Mechanism:** `PUNCH-LIST.md` (the example-header section).

Each example's header is generated from what the repo already knows, including where
in the manual the block sits. A document is adopted once its corpus files carry
generated headers (`--adopt` on first run).

---

## How this table is kept honest

- **`prepare-manual` reads it.** Every prepare, for the document being prepared, the
  skill surfaces each ⏳ in that document's row as work owed **this** release. That is
  the enforcement — a table nobody consults at the decision point is what produced
  F-301 and, in a different costume, «#250».
- **A new document gets a row when it enters the roster**, with every existing
  feature marked ⏳ or — .
- **A new feature gets a column when it lands**, seeded from *detected* state, not
  from what a document claims.
- **A column retires when it is ✅ or — everywhere**: drop it here and prune the
  matching `PLATFORM` line from the Freshness Ledger.
- **The roster's `Platform` column stays coarse** — "on the shared stack, yes/no" —
  and points here for per-feature state.
