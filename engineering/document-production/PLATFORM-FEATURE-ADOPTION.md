# Platform Feature Adoption — the per-document state table

**One table. Rows are documents, columns are platform features that each document
adopts at its own next release.** This is the master list: it answers "has this
document taken feature X yet," and it is what `prepare-manual` consults before
staging.

**Why this exists.** A shared-platform feature that needs per-document work cannot
be turned on set-wide — that would churn every published corpus to fix one. So
adoption is deliberately per document, at its next natural release, for any reason.
Until then the document is unchanged, never broken.

> **THE STANDING RULE (Stephen, 2026-09-10): every time we release a document, that
> document adopts everything still outstanding for it.** A release is the opportunity,
> and the opportunity is not declined. This replaces the earlier framing in which
> deferral was a judgement call made per release — it was that framing which let ⏳
> rows sit through about a dozen releases (**F-301**).
>
> A `⏳` in a row therefore means *"owed, and it will be taken at that document's next
> release"* — never *"pending a decision about whether to bother."* The only thing a
> release may not do is mark a feature `✅` it has not PROVEN on the returned PDF:
> adoption is wired **and** audited, so a document mid-release sits at `🔧` and
> `release-manual` Phase 3e flips it once the artifact says so.
>
> Where adoption is genuinely blocked by something outside the release (a prerequisite
> another document owns, a conflict needing a ruling), the block is named in the
> footnote with what would unblock it — a blocker is a fact, not a deferral.

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
| Getting Started | manual | 🔧 ¹⁵ | 🔧 ¹⁵ | 🔧 ¹⁵ | **✅** ¹⁰ |
| I/O & Smart Pins | manual | 🔧 ¹⁵ | 🔧 ¹⁵ | 🔧 ¹ ¹⁵ | 🔧 ¹¹ |
| **Assembly Reference** | manual | 🔧 ⁹ ¹⁶ | **✅** ⁹ | **✅** ⁹ | — |
| DeSilva Tutorial | manual | 🔧 ² ¹⁵ | 🔧 ¹⁵ | 🔧 ¹⁵ | **✅** ¹⁰ |
| Debug Window | manual | ⏳ | ⏳ | ⏳ | **✅** ¹⁰ |
| **Streamer Guide** | manual | **✅** ⁷ | **✅** ⁸ | ✅ | — |
| Architect's Guide | manual | ⏳ | ⏳ | ⏳ | — |
| Interpreters & Emulators (XBYTE) | manual | ⏳ ³ | ⏳ | ⏳ | ✅ |
| **Single-Step Debugger** | manual | **✅** | **✅** ¹³ | **✅** ¹⁴ | — |
| **PNut-Term-TS User Guide** | guide | **✅** | **✅** ¹² | **✅** ⁶ | — |
| **P2AN001** | app-note | **✅** ¹⁷ | **✅** ¹⁷ | **✅** ¹⁷ | **✅** ¹⁸ |
| P2AN002 · P2AN004 | app-note | 🔧 ⁴ ¹⁵ | 🔧 ¹⁵ | 🔧 ¹⁵ | 🔧 ¹⁸ |
| P2AN003 · P2AN005 · P2AN006 · P2AN007 | app-note | ⏳ ⁴ | ⏳ | ⏳ | ⏳ ⁵ |
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
⁶ **ADOPTED AND AUDITED 2026-08-23 — verified on the returned PDF, 27 of 27.**
`p2kb-platform-crossref` now sits between `figures` and `tables` in `request.json`, the ordering
the three adopted manuals share; it MUST precede `tables`, which flattens each cell to a string
and would leave table-borne refs dead. The filter itself was already in the manual store
(hash match), so only `request.json` staged.

**Full accounting of all 47 `Chapter N` occurrences in the generated `.tex`: 19 are chapter
headings (never self-linked, by design), 27 are linked, 1 is a LaTeX comment.** The artifact
itself carries 201 `/Link` annotations and 250 `/GoTo` actions, so the links exist in the PDF
and not merely in the markup. **Zero mis-fires** — every reference is a self-reference, and the
one external pointer (*The P2 Architect's Guide, **Part 3***) says "Part", which the filter
does not match.

**The first pass linked only 26 of 27, and the miss is worth carrying forward as a hazard for
every adopting manual.** The source had wrapped a reference across a line:

```
...configures 8N1 exclusively (Chapter
7), and 300 baud is...
```

Pandoc renders that as `Str "(Chapter"` · **SoftBreak** · `Str "7),"`, and the filter matches
`Chapter` + *Space* + number — a SoftBreak is not a Space, so the reference is invisible to it.
**Not a filter bug: a source line-wrap artifact, and a SILENT one** — nothing in the build
reports a reference that failed to link. Fixed by reflowing the paragraph; the second render
then read 27 of 27.

Swept all four adopted manuals for the same pattern afterwards: **zero** elsewhere, so this was
a one-off rather than a fleet condition.

> **✅ PLATFORM FIX APPROVED AND LANDED 2026-08-23** (Stephen's call). The filter now accepts a
> **Space OR a SoftBreak** between the keyword and its number, so a reference that straddles a
> line break in the author's source links like any other.
>
> **Proven by a before/after round-trip on the interactive daemon, read off the ARTIFACT** — a
> purpose-built 4-page document carrying eight cases: three ordinary-space controls, three
> line-wrapped cases, and **two negative controls** (`Chapter 99` plain, `Chapter 98` wrapped)
> targeting headings that do not exist.
>
> | Run | Filter | Body links on the case page | Wrapped cases | Negative controls |
> |---|---|:--:|---|---|
> | `crossref-softbreak-v1` | before | **3** | all three DEAD | correctly plain |
> | `crossref-softbreak-v2` | after | **6** | all three link, correct targets | **still correctly plain** |
>
> The negative controls are the load-bearing half: the SoftBreak branch still honours the
> target-must-exist rule, so the fix did not turn the filter into something that links anything
> that looks like a reference. Compile log clean on all five serious signatures. **Visually
> confirmed on the rendered page: no visual change at all** — a wrapped reference sets as
> ordinary inline prose, because pandoc's LaTeX writer emits a newline for SoftBreak and TeX
> reads that as a space, which is exactly what the emitted Space produces.
>
> **Re-swept the WHOLE corpus at landing, not just the adopted four: ZERO wrapped-reference
> sites in any manual or app note.** So this is a **pure no-op today** and carries **no
> re-render debt for anyone** — it is preventive, protecting future authoring rather than fixing
> present output. **Adoption stays per manual, at each one's next release** (Stephen, 2026-08-23);
> no document is re-rendered on account of this change.

*Prior state, for the record:* deferred at the v1.0.0 prepare (2026-08-19) because the audit
would have gated a release scoped not to wait. That reason expired once this build needed a
Forge round-trip for two recaptured figures. **That deferral was recorded as Stephen's call and
should not have been** — the reasoning was sound, the attribution was not his.
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


¹⁵ **Adopted 2026-09-10 in the v1.18.0 wave, under the standing rule** — six documents took
every feature they still owed, because they were being released. Wiring done and gated; each
mark flips `🔧` → `✅` only when `release-manual` Phase 3e reads it off that document's returned
PDF.

What was wired: **cross-ref** added to `lua_filters` **before** `p2kb-platform-tables` in five
`request.json` (tables flattens each cell to a string, so a filter after it cannot see a
table-borne reference); I/O & Smart Pins already had it and owed only the audit footnote 1 left
open. **Rights + metadata single-source** needed the part `request.json` alone does not do — all
four templates (`getting-started`, `iosp`, `desilva`, and the shared `appnote`) bound **zero**
`\Doc*` macros, the same shape that shipped Assembly v3.1.6 with Title, Subject and Author
EMPTY; each now binds all seven, copying Streamer's proven block. Covers stopped hardcoding
version and date and read `\DocVersion` / `\DocDate`, which is what makes single-sourcing real:
this same wave had already found **two covers stuck on August** while their metadata said
September.

Copyright was sourced from **each document's own licence page**, never copied between them —
DeSilva carries a year RANGE (*2025-2026*) where the others carry 2026, and the metadata gate
compares the declared rights against that page. Five `metadata.version` values lost a leading
`v`, which the gate would never have found on page 1 (it prints *"Version 1.0.4"*).

**DeSilva's footnote-2 blocker was resolved rather than carried:** its `request.json` said
*"Discovering P2 Assembly"* / *"Build, Experiment, and Master the Propeller 2"* while its cover
said *"P2 Assembly Programming"* / *"A Human-Centered Approach to Parallel Processing"*. The
cover wins — confirmed on the **shipped v3.0.6 PDF's own page 1** and the public deliverables
index, where the `request.json` title appears nowhere a reader has ever seen.

The four app notes not in this wave keep `⏳`: the shared template is converted and ready for
them, but no release has rendered or audited them, and a row does not go green on a template.

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

¹² **PNut-Term-TS — rights were HALF-WIRED; FIXED 2026-08-22, before any render.** Found while
re-opening the guide for its visual pass. Its template `p2kb-pnut-term-ts.latex` bound **five** of
the seven `\Doc*` macros — Title, Subtitle, Version, Date, Author (`:23-27`) — and **neither
`\DocCopyright` nor `\DocLicense`**. `request.json` declared no `copyright`/`license` either.

That combination is exactly **F-319**: the platform's rights guard does not fire for a document
whose rights macros sit at their `\providecommand{}` defaults, so `pdfkeywords` is emitted anyway
and comes out as the literal `"; licensed under "` — which is what Assembly's first v3.1.7 render
produced. **This guide is F-319's first live victim, not merely a candidate.**

BOTH halves were fixed (the two-part rule, and here it was 5-of-7 rather than 0-of-7, which is
harder to spot):
1. added `\renewcommand{\DocCopyright}{$copyright$}` and `\renewcommand{\DocLicense}{$license$}`
   to the template beside the other five — now 7/7;
2. added to `request.json` metadata, sourced from **this guide's own** licence page
   (`opus-master/front-matter.md:102`) — it is the ONE document in the set that is **Iron Sheep
   ALONE**, no Parallax:
   `"copyright": "Copyright 2026 Iron Sheep Productions, LLC"`, `"license": "CC BY-SA 4.0"`.

**Verified before the render, not after:** `audit-pdf-metadata.py`'s own `norm_rights()` was run
over the declared string and the copyright page's `Copyright © 2026 Iron Sheep Productions, LLC.`
— both normalise to `copyright 2026 iron sheep productions, llc`, so check 6 (metadata rights
AGREE with the document's own copyright page) will pass. The artifact check still has to happen on
the returned PDF; this only rules out a mismatch that would have been guaranteed to fail.

**This does NOT close F-319.** The shared guard in `p2kb-platform-foundation.sty:332-350` is still
broken for every document that has not wired these two macros — the `⏳` rows in the Rights column
above. Adopting the guide out of the victim pool also removes it as a possible **negative control**
for F-319; the Layout Torture Test is the remaining candidate.

From here on `audit-pdf-metadata.py --require-rights` gates this guide's rights on every render.

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

¹⁶ **Assembly Reference — ✅ under the AUGUST bar, re-opened 2026-09-10 because the bar moved.**
Footnote 9 is accurate about what it proved: the template binds all seven `\Doc*` macros and the
v3.1.7 info dictionary carried Title, Subject, Author and Keywords where v3.1.6 carried none. That
was the whole standard in August. The **September** wave raised it — *"covers stopped hardcoding
version and date and read `\DocVersion` / `\DocDate`, which is what makes single-sourcing real"* —
after finding two covers stuck on August while their metadata said September. Assembly was marked
✅ before that clause existed and was never re-swept against it, so it kept **two** version
locations: `metadata.version` **and** a literal `Version 3.1.8` on its own cover.

Nothing was rendering wrong — the two agreed at 3.1.8 — which is exactly why it survived a release.
A row that reads ✅ is not evidence; this was found by reading the covers of all 20 documents, not
the table. Assembly is the ONLY document in that state: Streamer, Single-Step Debugger and
PNut-Term-TS all read the macros already.

Converted 2026-09-10 in `opus-master/front-matter.md` (two lines; title and subtitle stay literal
on the cover by convention, as they do on every converted document). Costs no template deploy —
Assembly's `p2kb-pasm2-reference.latex` has bound `\DocVersion`/`\DocDate` since August and is
already in the manual store. Flips back to ✅ when `release-manual` Phase 3e reads
`September 2026` / `Version 3.1.8` off the returned v3.1.8 PDF.

¹⁷ **P2AN001 — all three PROVEN on the returned v1.0.5 PDF, 2026-09-10 23:37, and split out of the
shared app-note row because the three documents now diverge.** P2AN002 and P2AN004 are staged but
unrendered, and a row may not carry a ✅ its artifact has not earned.

**Metadata single-source + rights.** `audit-pdf-metadata.py` CLEAN, all seven declared fields
round-tripped: cover page 1 reads `September 2026` / `Version 1.0.5`, the info dictionary carries
Title, Subject and Author where v1.0.4 carried **none of the three**, and `Keywords` reads
*"Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed under CC BY-SA 4.0"*
where v1.0.4 carried no machine-readable rights at all.

**The first render is why this footnote exists.** At 23:02 the same document came back with the
cover reading `Version` and nothing after it, the date gone, and all four identity fields EMPTY —
because the Forge still held the OLD shared `p2kb-appnote-reference.latex`. The wave staged that
template ONCE, with P2AN002, and this note was built third. Footnote 9's rule proved itself again,
with a new edge: **adoption takes two parts, and the second part must physically reach the manual
store before any document that depends on it renders.** Staging a shared file with one manual
assumes the build order is followed; it is not a guarantee. Written up as Trap 3 in the
`prepare-manual` project overlay.

**Cross-ref filter — adopted, audited, and a correct NO-OP here; the negative half is the whole
result.** `p2kb-platform-crossref` sits between `figures` and `tables` in `request.json`. Measured
on the artifact: **4 link annotations, all URI** (two to the Parallax forum thread, two to the CC
licence) and **zero internal GOTO** — identical to the v1.0.4 render. All **4** prose `Chapter N`
occurrences name the *I/O & Smart Pins User Guide*, an external document, and the filter correctly
left **every one** plain. The note has no numbered chapters of its own — it is organised by Recipe
— so there is nothing here for the filter to link, and a link would have been a defect. Adoption
verified as behaving correctly, not as producing a number.

**Generated example headers stay ⏳, and the blocker is footnote 5's prerequisite: fence captions.**
This release did NOT take them, and that is a miss against footnote 5's own directive (*"at each app
note's next adjustment or update, add the captions"*) — v1.0.5 was such an update. Recorded rather
than glossed: the captions are reader-visible (the code-coloring filter emits them into the rendered
listing, `p2kb-platform-code-coloring.lua:510`), so they cannot be added to an already-rendered PDF
and would cost this note a second render cycle. 31 of the 32 app-note corpus files are already
byte-identical to a printed fence, so the work is annotation only. **Decision owed:** take captions
on P2AN001/002/004 now at the cost of re-rendering, or at the app notes' next content touch.

¹⁸ **App-note fence captions + generated example headers — the prerequisite taken 2026-09-10, on
Stephen's call: *"we can't miss things, we have the roster so we don't."*** Footnote 5 recorded
this as blocked and said to take it *"at each app note's next adjustment or update"*; the v1.18.0
wave was such an update for P2AN001/002/004, so it was taken here rather than carried.

**Captions.** 12 fences across the three notes now carry `caption="<file>.spin2"`. Each was matched
to its corpus file by **byte-identity of the fence body**, never by name or position — every one of
the 12 corpus files matched exactly one fence, with zero orphans on either side. Result:
`verify-example-corpus-identity.py` **GREEN** on all three (3/3, 6/6, 3/3, zero mismatched, zero
orphan, zero duplicate captions), and the prepare gate runner moved from *8 passed · 1 known-gap*
to **9 passed · 0 known-gap**. The KNOWN gap that printed on every app-note prepare is closed.

**Generated headers.** Adopted via `sync-manual-examples.py --adopt` against a new
`examples-library/PURPOSES.md` per note (the tool refuses to invent a Purpose). Headers carry
`Version.... v1.0.5 (2026-09-10)` — derived from the CHANGELOG, which is a *second* identity source
beside `request.json`; the two were checked and agree across all eight wave documents. ZIPs
repacked; `verify-published-zip-currency.py` **GREEN** 4/4, 7/7, 4/4, with `PURPOSES.md` correctly
excluded from the shipped archive.

**Two defects in the generated header itself, found by reading the first one produced and fixed in
`sync-manual-examples.py`:**
1. `Manual..... P2AN001` — the slug, not the title. All seven app-note changelogs use a **fourth**
   H1 shape, `# P2AN00N Changelog: <Title>`, matching neither pattern, so `doc_meta` fell back to
   the directory name. This is the *same failure* the loop was widened for in August (when Getting
   Started, Debug Window and IOSP silently fell back to their slugs) — the widening just did not
   reach far enough. An optional prefix before the keyword closes it. Verified across **all 17**
   documents: every title now derives correctly and none of the previously-working shapes moved.
2. `Appears in.  -- The Base Build` — a leading separator, because `where` was built as
   `chapter + " -- " + heading` and app notes have no `# Chapter N` headings at all. Now joins only
   the parts that exist.

**P2AN001 ✅ — PROVEN ON THE RETURNED PDF, 2026-09-11 00:00 (render 3).** The header half was
already proven off the repacked ZIP; the caption half is now proven on the page. All three captions
read in the artifact — `adc-single-pin-base.spin2` p7, `adc-three-pin.spin2` p11,
`adc-filter-cascade.spin2` p14 — and pages 7 and 14 were rendered and inspected: a small grey
right-aligned filename closing each listing inside its Spin2Block, code alignment and margins
unchanged. Still **20pp**, gates 8 PASS, cover and all seven metadata fields unmoved.

**The word-count delta was accounted rather than accepted**, and it is the reason to record this
at all: 6805 → 6803 looked like a *loss* while three captions had been added. A token-multiset
comparison against render 2 resolved it exactly — **+3 gained** (the captions), **−5 lost**, and
those five are one complete `continued from previous page` banner that a re-flowed listing no
longer needs. **Zero prose or code tokens moved in either direction.** A page-count check would
have read 20 = 20 and said nothing; the multiset is what proves no content left.

**P2AN002 · P2AN004 stay 🔧** — wired identically and staged, but neither has rendered. Each flips
on its own returned PDF.

**P2AN003 / P2AN005 / P2AN006 / P2AN007 keep ⏳ ⁵ deliberately** — they are not in this wave, and
captioning them now would put their opus-master ahead of their published PDFs. They take it at
their own next update, exactly as footnote 5 directs.

¹³ **Single-Step Debugger — rights wired and VERIFIED ON THE ARTIFACT 2026-09-09.** Its template
`p2kb-ssdbg.latex` bound `\DocTitle`/`\DocVersion`/`\DocDate` and **not** `\DocCopyright`/`\DocLicense`
— the same half-wired shape found on PNut-Term-TS (¹²), and invisible from `request.json` alone
because the platform's `\providecommand` defaults them to empty and the build stays clean. Both
`\renewcommand`s added to the template and both values added to `request.json`
(**ISP + Parallax**, unlike PNut-Term-TS which is ISP alone). Confirmed by reading the returned
PDF's metadata, not by the declaration: `Keywords` = *"Copyright 2026 Iron Sheep Productions, LLC
and Parallax Inc.; licensed under CC BY-SA 4.0"*.

¹⁴ **Single-Step Debugger — cross-ref filter adopted and AUDITED ON THE RENDER 2026-09-09.**
The audit *is* the adoption, so it was measured rather than assumed, before/after on the same
document: **NAMED internal links 127 → 147, +20** — and the source carries **exactly 20 reachable
prose `Chapter N` references** (32 occurrences, less 10 chapter headings, less 2 inside a raw-LaTeX
block), so every reachable one links. **0 links unresolved** (each resolves to a real page; a link
to nowhere is worse than no link) and **47 → 47 pages**, so nothing re-flowed.
**The negative half was checked too:** all 50 remaining `Chapter N` occurrences are chapter
headings and running heads — every one ends `N:` — and the filter correctly left every one of them
plain. **Known structural limit, not a defect:** the two references inside the Chapter 3 landmark
table do NOT link, because that table is a hand-authored `` ```{=latex} `` block and pandoc passes
raw LaTeX through untouched — no Lua filter can see inside it. Anything needing a live
cross-reference must live in markdown, not in a raw block.

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
