# P2-Knowledge-Base overlay — release-manual

This project ships **technical** manuals whose claims are consumed by readers
and by remote AI agents. Some manuals also ship a **reader example corpus** — a
`manuals/<slug>/examples-library/` of loose `*.spin2` files bundled as
`examples-library.zip` and published next to the PDF. A loose file that has
silently drifted from the manual's printed code block is a trust defect the
reader hits in their editor, so the release must guard against it exactly as
Phase 1 guards against silent PDF content-drop.

## Augments Phase 1 — VERIFY: add the example-corpus identity gate

For any manual that publishes an `examples-library.zip`, the PDF silent-drop
check is **not sufficient** — also verify the example corpus has not drifted:

- **Run the identity checker; it must be GREEN before the ZIP is published**
  (before the `git add -f …-src.zip` in Phase 5, and before any re-zip):

  ```bash
  python3 engineering/tools/verify-example-corpus-identity.py            # default: Debug Window
  python3 engineering/tools/verify-example-corpus-identity.py --manual <manual-dir>   # any other
  ```

  Exit 0 = GREEN (every loose `*.spin2` is byte-identical to its `opus-master`
  code block, no orphan files/blocks, no duplicate captions). A RED result
  **blocks the release** — the published ZIP would hand readers files that don't
  match the printed manual ([[feedback_example_file_matches_code_block_not_figure]]).

- **Re-zip only from a GREEN corpus.** If you rebuild `examples-library.zip`
  during the release, run the checker first; never zip over a drifted corpus.

- Manuals with **no** `examples-library/` (reference-only manuals) skip this gate
  — the checker prints GREEN and exits 0 when no corpus is present, so it is safe
  to run unconditionally.

### The identity gate does NOT tell you the published ZIP is current

`verify-example-corpus-identity.py` compares `examples-library/` against
`opus-master/`. It says **nothing** about `DOCs/<slug>-src.zip`, the archive the
reader actually downloads. Those are two different questions that read like one
sentence, and the gap between them shipped:

> **Debug Window v1.1.3** — corpus identity **GREEN 34/34**, while the published
> ZIP was dated three weeks earlier and **13 example files had changed since**.
> Several were the F-281/F-290/F-292 repairs, where the old code **compiles clean
> and runs a different program** than the page shows. It was caught by asking
> "have examples changed since the last tag?" — a question on nobody's checklist.

**So run BOTH gates. Corpus identity first, then ZIP currency:**

```bash
python3 engineering/tools/verify-example-corpus-identity.py  --manual <manual-dir>   # corpus ↔ printed blocks
python3 engineering/tools/validation/verify-published-zip-currency.py --manual <manual-dir>   # ZIP ↔ corpus
```

- Exit 0 = every shippable corpus file is present in the ZIP **and byte-identical**.
  It compares bytes, not timestamps — **a ZIP rebuilt from a stale directory has a
  fresh mtime and stale contents**, so an mtime check would have passed here too.
- **RED blocks the release.** Rebuild the ZIP from the corpus (identity GREEN
  first — never zip over a drifted corpus), then re-run until GREEN.
- Safe to run unconditionally: a manual with no `examples-library/` exits 0.
- The ZIP filename carries **no date** — it is overwritten in place each release so
  the published URL never changes.

**Order matters.** Identity green + ZIP stale is the failure that shipped; ZIP
currency is meaningless if the corpus itself has drifted. Run them in that order,
and rebuild between them if either is RED.

## Augments Phase 1 — VERIFY: the in-doc Revision History agreement gate

Every **app note** (and any document that prints a `## Revision History` in its body —
**no manual currently does; grep, don't assume**) states its version in a place the
reader actually reads, *separate* from the cover and from `CHANGELOG.md`. Phase 2a audits
`CHANGELOG.md`; **nothing looked at the rendered Revision History**, so the two drifted
silently — and the *release itself* was the thing causing the drift, because it bumped the
cover and left the table behind (F-215: four app notes shipped a cover version that appears
nowhere in their own history).

**Authoring this belongs to `prepare-manual` (see its `project-overlay.md`), not here** —
the Revision History is inside the body markdown that gets rendered, and by the time this
skill runs the PDF already exists. This gate is the **backstop**: it catches a miss, and a
miss costs a full re-render.

**Assert against the RENDERED PDF (not the source — the source may be right and the PDF
stale from an earlier build):**

```bash
PDF=deliverables/documents/DOCs/<PDF>
COVER=$(pdftotext -f 1 -l 1 "$PDF" - | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" | head -1)
TOP=$(pdftotext "$PDF" - | grep -A4 -i "^Revision History" | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" | head -1)
echo "cover=$COVER  revision-history-top=$TOP"
```

Both must hold:
1. **`TOP` == `COVER`** — the document's own history lists the version it *is*.
2. **No never-shipped version is named anywhere in the section.** Authority is `git tag`,
   not the CHANGELOG: `git tag | grep -i "<slug>"`. Any `0.x` review draft is *not* a
   release and must not appear.

**A mismatch BLOCKS the release** exactly as a content-drop does: fix the Revision History
in `opus-master`, re-prepare, regenerate, re-verify. Do not promote a document whose own
history contradicts its cover.

> **Detection note (why F-215 was under-counted on first pass):** the original sweep grepped
> for the literal `v0.1.0` / "initial draft" and so missed four app notes whose tables say a
> bare `0.1.0` / "First draft". **Key on the shape of the defect (a version < the cover, or a
> version with no tag), never on one spelling of it.**

## Augments Phase 5 — the example ZIP is NOT gitignored in this repo

The central skill suggests `git add -f …-src.zip` "for a gitignored example ZIP."
**In this project the ZIP is tracked normally** — `git check-ignore` returns
nothing for it, and a plain `git add` stages it. The `-f` is harmless, but the
premise is not: read it as "the ZIP is excluded from normal staging" and it is
easy to leave a rebuilt archive out of the release commit entirely, publishing a
PDF whose linked examples are the previous release's.

So: **stage the ZIP by explicit path in the Phase 5 `git add`, every release that
rebuilt it**, and confirm it appears in `git diff --cached --name-only` before
committing.

After the push, verify both published links actually resolve — the PDF and the
ZIP — rather than assuming the push activated them:

```bash
for u in ".../DOCs/<PDF>" ".../DOCs/<slug>-src.zip"; do
  curl -s -o /dev/null -w '%{http_code} %{size_download}B\n' \
    "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/deliverables/documents/$u"
done
```

`200` plus a byte count matching the local artifact is the proof. A `404` means
the file never reached the remote; a `200` with the *wrong* size means a stale
copy is being served, which is the same defect the currency gate above exists to
prevent — just one stage later.

## Augments Phase 3 — advance `last_published_tag` to the tag THIS release creates

`MANUAL-DESCRIPTOR.md` carries `last_published_tag`, the baseline every
diff-since-published audit measures from (Dimension #15, and `audit-changelog`'s
content check). Nothing in the release process advances it, so **every release
makes its own descriptor stale the moment it tags** — the baseline still points
at the version just superseded.

That is not a slow drift; it is manufactured once per release. A fleet sweep
found **six of nine tagged manuals stale**, two of them freshly broken by the
releases run minutes earlier, and others two to five versions behind — meaning
those manuals' "what changed since we published" audits had been reading from
the wrong point for months.

**So in Phase 3, alongside the roster row, set:**

```
last_published_tag: <slug>-v<X.Y.Z>   # baseline for Dimension #15 (released <YYYY-MM-DD>, <NN>pp)
```

- The tag is the one this release creates, not the prior one.
- **Take the date and page count from git, never from memory or the roster**:
  `git log -1 --format=%ad --date=short <tag>` and
  `git show <tag>:deliverables/documents/DOCs/<PDF> | pdfinfo -`.
  The trailing comment is part of the record — a stale comment beside a corrected
  value is the same defect wearing a disguise, and three descriptors were found
  carrying wrong dates, wrong page counts, and one still calling a released
  manual a maiden release.
- An unreleased manual (no tag) correctly carries an empty value — leave it.

**Verify the whole fleet, not just the manual you released** — the check is one
command and it is how the six stale ones surfaced:

```bash
for d in engineering/document-production/manuals/*/MANUAL-DESCRIPTOR.md; do
  slug=$(basename $(dirname $d))
  rec=$(grep -h 'last_published_tag' $d | head -1 | sed -E 's/last_published_tag: *([^ #]*).*/\1/')
  act=$(git tag | grep "^$slug-v" | sort -V | tail -1)
  [ "$rec" = "$act" ] || echo "STALE $slug: $rec vs $act"
done
```
