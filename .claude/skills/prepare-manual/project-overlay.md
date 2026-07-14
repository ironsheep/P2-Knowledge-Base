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
