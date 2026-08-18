# P2-Knowledge-Base overlay — prepare-manual

This project's **app notes** (and any document that prints a `## Revision History`
section in its body) carry the version in a **THIRD** place that the base skill does
not know about. Step 5 enumerates two — the markdown **cover** and `request.json`
**metadata** — and rightly warns that bumping one without the other creates a
mismatch. There is a third, and it is the one that drifts.

## Augments Step 5 + Step 6.2 — the THIRD version location: the in-doc Revision History

A document that renders a `## Revision History` into its own PDF has **three**
version locations, not two:

| # | Location | Rendered where |
|---|----------|----------------|
| 1 | markdown cover (`front-matter.md`, or the single-file cover region) | the PDF's cover page |
| 2 | `request.json` → `metadata.version` | PDF properties / headers / footers |
| 3 | **`## Revision History` in the body markdown** | **a page the reader actually reads** |

**Detect it:** `grep -n "^## Revision History" manuals/<slug>/opus-master/*.md` (for app
notes, it is in the body file — `P2AN00N.md`). Currently: **every app note has one; no
manual does.** Do not assume — grep.

**The rule: if the document has one, bumping the cover REQUIRES adding its new entry in
the same edit.** Never bump #1 and #2 while leaving #3 behind — that is exactly the
defect this overlay exists to prevent (F-215: four app notes shipped with a cover version
that appears nowhere in their own history, because the release bumped the cover and left
the table alone; the release itself was what caused the drift).

**Derive the entry — do not author it fresh.** The row's text comes from the CHANGELOG
entry for the version being released (`opus-master/CHANGELOG.md`), which `release-manual`
Phase 2a has already audited. Two artifacts telling the same story in independently-written
prose *will* diverge; deriving one from the other is what keeps them honest. Condense the
changelog entry to one sentence — the Revision History is a summary, not a second changelog.

**Never name a version that was never released.** Per
`methodology/changelog-style-guide.md` — *"Never-shipped versions are never mentioned …
If a version number was never released, delete any artifact referencing it."* A review
draft (`v0.1.0`) is not a release. **The authority for "was it shipped" is `git tag`**, not
the CHANGELOG and not memory:

```bash
git tag | grep -i "<slug>"          # the definitive list of shipped versions
```

**Form follows history depth** (keeps the section honest about what it is):
- **2+ shipped versions** → a table, newest first:
  ```markdown
  | Version | Date | Notes |
  |---|---|---|
  | 1.0.2 | 2026-07-11 | <one-sentence summary, derived from the CHANGELOG entry> |
  ```
- **Exactly 1 shipped version** → a single bullet that *describes the document*, not a
  delta — there is no prior published baseline to delta against (the style guide's
  "Initial releases describe the document, not a delta"):
  ```markdown
  - **v1.0.0** (July 2026) — initial release for community review. <what the document is>.
  ```

## Augments Step 6 — the EXAMPLE-CORPUS gate (two tools, one before the other)

A manual that ships an `examples-library/` must not render while its loose files and
its printed code blocks disagree — the reader downloads the ZIP and gets code the book
does not show. Two gates, in this order, before the render:

```bash
# 1. headers current (adopted documents only; un-adopted print INFO and pass)
python3 engineering/tools/sync-manual-examples.py --doc <manual dir> --check

# 2. file body == printed code block, plus no orphans either way
python3 engineering/tools/verify-example-corpus-identity.py --manual <manual dir>
```

**Order matters.** The sync tool can *rewrite* headers; run it first, in `--check` mode,
so the identity gate reads settled files. If `--check` reports out-of-sync, re-run the
sync without `--check`, look at the diff, and commit it — never hand-edit a generated
header, because the next sync silently reverts it.

**Adoption is per-document and deliberate.** Only `p2-xbyte-programming-guide` carries
generated headers today (adopted 2026-08-18). Every other document prints
`INFO: ... has not adopted` and passes — that is correct, not a warning to clear. A
document adopts at *its* next release, with `--adopt`, which is also when its
`-src.zip` is rebuilt. Streamer is next in line.

**Known gap, not caused by adoption:** the seven app notes (`P2AN001`–`P2AN007`, 32
files) have **no captioned fences at all** — they key examples to recipe IDs in a
README table — so `verify-example-corpus-identity.py` reports them RED with all files
as orphans, and has never actually gated them. Do not "fix" that by deleting files or
captions; it is on the document-production punch list as its own decision.

---

## Augments Step 6 — the FONT-GLYPH gate (run it; it is not in the base skill)

The base skill runs two source gates (code-line-length, inline-code-ASCII). There is a
**third**, and it guards the nastiest failure mode in this stack: a glyph the render font
cannot draw makes xelatex **print nothing and leave a hole**, with a **clean compile log**.
That shipped once — a superscript-n silently turned *"MAG multiplies by 2ⁿ"* into the
falsehood *"multiplies by 2"*, inside a correction. Run it on the **assembled** markdown,
after Step 6.3:

```bash
python3 engineering/tools/validation/audit-font-glyphs.py \
    engineering/document-production/workspace/<slug>/<DocName>.md \
    --source-dir engineering/document-production/manuals/<slug>/opus-master \
    --templates  engineering/document-production/workspace/<slug>/templates \
                 engineering/document-production/platform/templates
```

**`--templates` is REQUIRED, not optional.** A codepoint the font lacks still renders if a
template the document loads declares a `\newunicodechar` fallback for it — and coverage is
per-document. App notes load `p2kb-appnote-local.sty`, which draws `⚠`/`💡`/`🔧`/`🔍` as
colored callout markers; the platform templates draw `Ω`/`μ`/`θ`/`✅`/`✓`/`❌`. Omit the flag
and the audit reports those as failures on every app note — and a gate that cries wolf is a
gate that gets ignored, which is how the next real hole ships. Pass the flag and the audit
prints which fallbacks it honored, so the exemption is visible rather than silent.

- **Clean (exit 0)** — proceed.
- **Violations (exit 1)** — STOP. Fix in **opus-master**: replace the character with a form
  the font carries, or drop it. Also catches a **heading inside a blockquote** (`> ### T`),
  which prints a literal `###` (shipped once, Debug Window ch08).
- **Do NOT "fix" a glyph that actually renders.** Superscript/subscript *digits* (`2¹⁶`,
  `log₂`) render correctly and are not flagged. If the audit ever flags one, the audit is
  wrong — confirm against a shipped PDF before butchering correct math into prose.

## Consequence for ordering — why this lives HERE and not in release-manual

The Revision History is **inside the body markdown that gets rendered into the PDF**.
`release-manual` runs *after* the PDF exists, so it **cannot** fix this — by then the
stale table is already printed. The authoring must happen here, **before** assembly
(Step 6.2, alongside the cover edit, so the new value flows into the assembled working
copy). `release-manual` only *verifies* it, as a backstop — and a failure there costs a
full re-render.

## Augments Step 4 — a `debug()` directive line CANNOT be continued, only shortened

The base skill's fix for a code overflow is: *"break at a logical boundary with the legal
Spin2 `...` line-continuation."* That is right for ordinary Spin2 — and **it silently
destroys a `debug()` directive**, which is the bulk of the over-long lines in the Debug
Window manual and appears in every manual that teaches DEBUG.

**Why:** a backtick directive is a **literal string assembled at compile time**, not Spin2
source, so no Spin2 syntax applies inside it. Verified by compiling and reading the
directive back out of the `.bin` (F-290):

| Attempt | Compiles | What ships |
|---|---|---|
| `...` continuation | ✅ clean | `…SPACING 3 ...` — the `...` is embedded **literally** and **everything after it is dropped**. A three-channel LOGIC window became a zero-channel one, 9,438 vs 9,482 bytes. |
| color as a `CON` symbol | ✅ clean | `'CS' 1 C_CS` — the symbol is embedded **verbatim, never resolved**; the PC-side parser can't read it as a color and falls back to defaults. |
| trailing `-` splice | ✅ clean | different program, 9,338 vs 9,408 bytes (F-281) |

Only `` `(expr) `` substitutes a value; a bare token is text.

**So for an over-long `debug()` line the ONLY sanctioned fixes are:**
1. **Drop optional directive keywords** — but first confirm the chapter teaches them elsewhere,
   so nothing is lost. (For F-281's LOGIC line, `TITLE`/`SAMPLES`/`SPACING` were all already
   taught 250 lines earlier with a table row, prose and a prior example: 113 → 70 cols, zero
   pedagogical cost.)
2. **Move a trailing comment to full lines above** the statement at its indent.
3. **Shorten the instance name or label text** where that costs no meaning.

**Never** split the directive. **Always** byte-compare the resulting `.bin` against the
one-line form — a clean compile proves nothing here, and the compiler will never warn you.

**Do NOT drop the explicit channel `count`** (the `1` in `'CS' 1 $00FFFF`) to save room:
`LOGIC_Configure` reads the next token as `count` via `KeyValWithin(v, 1, 32)` **before** the
color, and whether a failed count consumes the token is undetermined in the manual's REF. If it
consumes, the color is lost silently. Treat the explicit count as load-bearing until a bench run
says otherwise.
