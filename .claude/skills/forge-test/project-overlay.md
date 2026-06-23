# forge-test — P2-Knowledge-Base overlay

Applies additively to the central `forge-test` skill.

## Pre-submit static gates (run BEFORE Step 2 "Submit the request")

A daemon round-trip costs ~25–35 s plus the inspect cycle. Two cheap static checks catch a whole class of
defects that otherwise only surface *after* a full Forge build — so run them on the **opus-master source**
(not the assembled/escaped copy) before you stage and submit:

```bash
# inline code must be ASCII — a non-ASCII char in a `like this` span makes \lstinline abort xelatex
python3 engineering/tools/validation/audit-inline-code-ascii.py <opus-master source file(s)>
# code lines must fit the manual's K (code boxes don't wrap; an over-long line is an authorship defect)
python3 engineering/tools/validation/audit-code-line-length.py <opus-master source file(s)>
```

- **Inline-ASCII fail** → a U+2026 ellipsis / U+2212 minus / smart quote crept into an inline code span; it
  will crash the build with `! Undefined control sequence` only after pandoc→tex→xelatex. Fix in source
  (`...`, `-`, plain quotes) and re-run — do **not** spend a daemon cycle to discover it.
- **Line-length fail** → shorten in source (legal Spin2 `...` continuation, or shorten the comment) before
  submitting.

These are the same gates `prepare-manual` runs before production staging — the point of this overlay is that
the *interactive* daemon path must run them too, **up front**, so a statically-catchable defect never burns a
round-trip. (Adopted at the 2026-06-23 Architect's Guide retrospective, after the test-v1 build crashed on an
inline-code ellipsis that `audit-inline-code-ascii.py` would have caught for free.)

## Notes specific to this project's manuals

- A manual that loads TikZ diagrams (`\usepackage{p2kb-architect-diagrams}` → `\RequirePackage{p2kb-platform-diagrams}`)
  must stage **`p2kb-platform-diagrams.sty`** to the daemon `templates/` — it is a shared platform file the
  daemon store does not have unless a prior daemon run staged it.
- Render-only defects the static gates **cannot** catch (still need the daemon round-trip + visual/text-presence
  inspection): silent table-row drops from a non-breaking tabularray `tblr`, figure numbering format (e.g.
  `\thefigure` yielding "0.N" under unnumbered chapters), and missing-glyph drops (emoji markers).
