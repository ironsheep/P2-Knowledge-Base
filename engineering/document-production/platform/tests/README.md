# Platform filter test fixtures

Small, purpose-built documents that prove a **platform filter** behaves as claimed.
They are not publications and never ship — each one exists so a platform change can be
re-verified later by someone who was not there when it was made.

**Why they live here and not in `pdf-forge/interactive-testing/`.** That whole tree is
git-ignored working space with a 7-day retention, so a proof staged there evaporates. A
platform change is permanent; the evidence that it works has to be at least as durable as
the change. The fixture is tracked; the *run output* stays disposable.

**Every fixture must carry negative controls.** A test that only shows the new behaviour
working cannot tell you whether the filter started matching things it should not. The
negative control is the half that makes the result mean something.

---

## `crossref-softbreak-test.md` — `p2kb-platform-crossref.lua`

**Proves:** a cross-reference that straddles a **line break in the author's source** still
links, and that making it link did not make the filter link references whose target does
not exist.

**Background.** The filter matched `Chapter` + *Space* + number. When the source wraps
between the keyword and its number, pandoc emits `Str "(Chapter"` · **SoftBreak** ·
`Str "7),"` — and a SoftBreak is not a Space, so the reference silently did not link.
**Nothing in the build reports a reference that failed to link**, so this is only ever
caught by counting links in the rendered PDF. Fixed 2026-08-23 to accept either separator.

**The eight cases** (all on page 1, each tagged with a unique `CASE-` marker):

| Case | Expect |
|---|---|
| `CASE-CONTROL-SPACE` · `(Chapter 2)` | **link** — ordinary-space control, must not regress |
| `CASE-FIX-WRAP` · `(Chapter`⏎`3)` | **link** — the fix |
| `CASE-NEG-PLAIN` · `Chapter 99` | **plain** — no such chapter |
| `CASE-NEG-WRAP` · `Chapter`⏎`98` | **plain** — negative control for the *new* branch |
| `CASE-APPX-SPACE` / `CASE-APPX-WRAP` | **link** both |
| `CASE-SECT-SPACE` / `CASE-SECT-WRAP` | **link** both |

**Expected result: 6 body links on the case page.** Before the fix it was 3.

### Re-running it

Escape it, stage it, and submit it to the interactive daemon (see the `forge-test` skill —
it owns the daemon lifecycle; ask the user to start the daemon first):

```bash
engineering/tools/conversion/latex-escape-all.sh \
  engineering/document-production/platform/tests/crossref-softbreak-test.md \
  engineering/pdf-forge/interactive-testing/test-documents/Crossref-SoftBreak-Test.md
```

Request: template `p2kb-pnut-term-ts.latex`, filters in production order
(`figures, crossref, tables, mnemonic-bold, code-coloring, pagination`), pandoc args
`--top-level-division=chapter --toc --toc-depth=2`.

**Read the result off the ARTIFACT, not the success flag.** Links are emitted as
`\hyperlink` → **named** destinations, so count *all* link kinds, not just `LINK_GOTO`
(counting only GoTo reports zero and looks like a total failure):

```python
import pymupdf                      # /opt/pdf-tools/venv/bin/python
doc = pymupdf.open("<run>/full-doc/output.pdf")
pg  = next(p for p in doc if "CASE-CONTROL-SPACE" in p.get_text())
print(len(pg.get_links()))          # expect 6
```

Cross-check `output.tex` for `\hyperlink{...}` on each case — the `.tex` shows plainly
which cases linked and which stayed prose.
