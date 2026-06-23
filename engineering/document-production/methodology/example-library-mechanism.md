# Example-Library Mechanism

**Status:** Standard — adopted in the doc-style-change sprint (2026-06-23), proven
end-to-end before rollout.
**Applies to:** every manual built on the shared platform stack
(`p2kb-platform-*`).

A P2 manual ships a small **example library**: the complete, runnable programs a
reader will want to copy out and compile. This document defines how those examples
are marked in the source, rendered in the PDF, extracted into a ZIP, and
distributed — and the single rule that keeps the printed code and the shipped file
from ever disagreeing.

The convention generalizes the one already shipped with the **P2 DEBUG Window
Manual** (`manuals/p2-debug-window-manual/examples-library/`): curated, complete,
semantically-named programs with a README index — not a dump of every fenced
snippet.

---

## 1. What is (and isn't) a library example

An **example** is a *complete, runnable worked program* the author has curated. The
DEBUG manual's criteria are the standard:

- **Self-contained and runnable** — compiles and runs as shown.
- **Exactly as printed** — the file is, verbatim, the code block in the manual.
- **Keeps running** — ends with a `repeat` (or a PASM `jmp` back into the cog loop)
  so the program (and any DEBUG window) stays alive.
- **Compiles clean** — `pnut_ts` (or `pnut-ts -d` when the block contains `debug()`
  directive content).

A **snippet** is everything else: a one- or two-line fragment shown to make a point
(`WRPIN(pin, P_HIGH_15K | P_LOW_FLOAT)`), an instruction-syntax form, a bit-field
layout, a worked formula, an OS-terminal command. Snippets are **not** examples —
they get no caption and are not extracted. Most fenced blocks in a reference manual
are snippets; only a curated handful are examples.

> **Not auto-extraction.** We deliberately do **not** turn every fenced block into a
> file. A library of hundreds of non-compilable fragments is worse than a curated
> set of a few dozen runnable programs. Curation is an authoring act.

---

## 2. Marking an example — the caption attribute (single source of truth)

The author tags a worked-example code block with a **filename caption attribute on
the code fence**:

````markdown
```{.spin2 caption="ch05-plot-gauge.spin2"}
CON _clkfreq = 200_000_000
PUB main()
  ...
  repeat
```
````

That one attribute is the **single source of truth**. It drives both:

1. **the printed caption** — the code-coloring filter prints the filename quietly at
   the bottom-right inside the code box, so a reader can find that exact program in
   the ZIP; and
2. **the extracted file** — `build-example-library.py` writes the block, verbatim,
   to a file of that name and zips it.

Because both read the same attribute on the same block, the printed caption and the
shipped file can never drift apart — the file *is* the printed block.

### The caption goes on the fence, never on a wrapping div

If a worked example is wrapped in a color div (`::: spin2`), the caption still goes
on the **inner ``` fence**, not the `:::` div:

````markdown
::: spin2
```{.spin2 caption="ch02-uart-echo.spin2"}
...
```
:::
````

Pandoc transforms the inner code block *before* the outer div, so a caption placed
on the div never reaches the renderer. Keeping it on the fence is the one rule the
renderer and the extractor both honor.

### Which block colors accept a caption

Captions are honored on the **runnable-code** block classes only:

| Class (fence info) | Box | Caption? |
|---|---|---|
| `spin2` | Spin2Block (green) | yes |
| `pasm2` / `pasm` / `iosp` | IOSPBlock (PASM2 green) | yes |
| `cordic` | CORDICBlock | yes |
| `multicog` | MultiCOGBlock | yes |
| `antipattern` | AntipatternBlock (red) | **no** — wrong-on-purpose, never shipped |
| `*-syntax`, `layout`, `formula`, `command`/`console`/`terminal`/`shell` | reference/diagram/command boxes | **no** — not programs |

### Naming

Use the shipped semantic convention: **`chNN-short-description.spin2`** (or
`.pasm2` for a standalone PASM program), lower-case kebab description, chapter
number prefix so the files sort in reading order. Each filename must be unique
within a manual (the build fails on a duplicate).

---

## 3. Building the library — `build-example-library.py`

```
engineering/tools/conversion/build-example-library.py <manual.md> <examples-library-dir> [--zip <path>]
```

The script scans the manual's markdown, extracts every caption-tagged fence to a
file of that name in `<examples-library-dir>`, (re)builds the ZIP, and reports. It:

- writes each example **verbatim** (whitespace intact — the whole point);
- **fails** on a duplicate caption or an unsafe filename (path separators);
- **reports** (does not delete) files in the directory no longer referenced by a
  caption, so the author can prune intentionally;
- never overwrites a hand-authored `README.md`, and includes it in the ZIP if
  present.

Run it on the **prepared/workspace markdown** (after assembly), as a prepare-manual
step — see Integration below.

### The README index (author-curated)

Each `examples-library/` carries a `README.md` index — a table of *file → what it
shows* — authored once and maintained as examples change. The DEBUG manual's README
is the template (columns: File / Window / Example). The build script does not
generate this; it is curation, like the examples themselves.

---

## 4. Distribution (decided 2026-06-23)

macOS Preview drops whitespace on in-PDF copy, so clean copy is routed through the
ZIP, **not** an in-document link:

- **No download links inside any PDF.** The document body carries only the per-block
  filename **caption** (a label, not a link).
- **The example-library ZIP is published alongside the manual's PDF** in the public
  deliverables area.
- **The ZIP's download link lives in the public manuals roster / release index** —
  the reader-facing "which manuals are available" listing — beside the PDF's
  force-download link.
- **No per-example file links** anywhere. Distribution is the whole-manual ZIP via
  the roster only. The caption + the ZIP is the entire mechanism.

---

## 5. Integration into the pipeline

- **prepare-manual** runs `build-example-library.py` on the prepared markdown so the
  ZIP is regenerated from the current source whenever the manual is built. (Logged
  as a prepare-manual skill-evolution candidate.)
- **release-manual** publishes the ZIP beside the PDF in deliverables and adds/
  refreshes the roster download link. (Logged as a release-manual skill-evolution
  candidate — the release roster gains an example-library-ZIP column.)

---

## 6. Verification

- **Normal:** every worked example shows its filename caption; no snippet does; the
  ZIP contains exactly the captioned files, byte-for-byte equal to the printed
  blocks (whitespace intact); each file compiles per its criteria (§1).
- **Distribution:** the roster links each manual's ZIP; no ZIP/download link appears
  inside any PDF; no roster entry points at a missing ZIP.
- **Consistency:** the set of printed captions equals the set of files in the ZIP
  (guaranteed by the single-source-of-truth attribute, but worth a glance after a
  large edit).

---

## 7. Rollout

This standard is established and proven; the per-manual passes apply it by curating
each manual's worked examples (tagging the fences, authoring the README) and the
release path publishes the ZIP. The DEBUG Window Manual's existing library already
embodies the curated philosophy and naming; bringing it onto the caption-driven
build is a later, mechanical step (tag its example fences so its shipped files are
generated from the body rather than hand-maintained).
