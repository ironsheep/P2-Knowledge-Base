---
name: forge-test
description: Round-trip a document/template through the PDF Forge interactive watch daemon and inspect the result YOURSELF — stage files, submit a test request, wait for the PDF, then read the compile log and render any page to verify images/layout/template behavior. Use when the user says "test the <template/doc> on the forge", "round-trip this", "does the layout/diagram look right", "generate a test PDF and check it", or invokes /forge-test. This is for INTERACTIVE TESTING ONLY (nailing down template/layout/feature behavior); production deliverables still use prepare-manual → manual copy-to-Forge.
---

# Forge Test — self-service PDF round-trip

You drive the PDF Forge **interactive watch daemon** end-to-end and verify the result yourself: stage → submit → wait → **inspect (compile log + rendered pages + text-presence)** → iterate. No human courier in the loop.

**Scope:** template/layout/feature testing — "do the images render?", "is the page layout right?", "did this filter change behave?". NOT production. Production deliverables go through `prepare-manual` and the user's manual copy-to-Forge route.

## The bridge (constant)

`engineering/pdf-forge/interactive-testing/` is **bind-mounted to `/workspace/shared/`** on the Forge. You write here; the daemon (running on the user's machine) sees it.

```
interactive-testing/            (THIS dir == /workspace/shared — never make a shared/ subdir)
├── templates/         # *.latex AND *.sty  (the main template + every \usepackage'd .sty)
├── filters/           # *.lua  (no .lua extension needed when naming them in the request)
├── test-documents/    # *.md   (the ESCAPED markdown to render)
├── assets/            # images, if any
├── test-requests/     # drop <id>.json here → daemon picks it up (then archives it)
├── test-runs/         # OUTPUT: one dir per run → {request_id}_{timestamp}/
│   └── <test-name>/   #   result.json, output.pdf, output.tex, output.compile.log, thumbnail.png
└── status/            # forge-ready.txt, queue-status.json, activity.log, errors.log
```

## Daemon lifecycle — YOU own both bookends

The daemon runs on the **user's machine** and consumes resources, so it is **operator-managed** and you must manage the start/stop explicitly — never assume it's running, never leave it running.

- **Before a test session:** tell the user, in plain words, **"start the Forge daemon"** and wait for confirmation. Do not stage-and-hang against a dormant daemon.
- **When testing is complete:** tell the user, in plain words, **"testing is done — you can stop the Forge daemon now."** Always close the loop; don't leave it burning on their machine.

State both explicitly to the user — starting and stopping are their actions, not yours, and they need the prompt at each end.

## Step 0 — Preflight: is the daemon alive?

Check freshness BEFORE staging:

```bash
cd engineering/pdf-forge/interactive-testing
date -u +"now: %Y-%m-%dT%H:%M:%SZ"; head -1 status/forge-ready.txt
```

If `forge-ready.txt`'s stamp is more than a few minutes old (or missing), the daemon is **dormant** — STOP and ask the user to start it (see the lifecycle note above). Re-check the stamp is fresh before submitting.

## Step 1 — Stage the inputs

- **Template + its `.sty` files** → `templates/` (copy ALL `.sty` the `.latex` loads, e.g. foundation/content/diagrams layers).
- **Lua filters** → `filters/`.
- **Markdown** → `test-documents/`, but **escape it first** (the production pipeline does, so match it):
  ```bash
  engineering/tools/conversion/latex-escape-all.sh <source>.md \
      engineering/pdf-forge/interactive-testing/test-documents/<Doc>.md
  ```
- **Assets** (if any) → stage to **the exact path the markdown/template references**, not a guessed dir. Covers and inline images are commonly referenced as `inbox/assets/<img>` (pandoc runs with `--resource-path` rooted at the shared workspace), so a cover `\includegraphics{inbox/assets/book-artwork.png}` needs the file at `interactive-testing/inbox/assets/book-artwork.png`. Grep the template/markdown for the image path and mirror it.

Copy only what this test needs; the daemon persists files across runs by name.

## Step 2 — Submit the request

Write `test-requests/<request_id>.json`. Use a **versioned id** (`<slug>-test-v1`, `-v2`, …) so successive runs are distinguishable.

```json
{
  "format_type": "template_testing",
  "request_id": "<slug>-test-v1",
  "template": "<template>.latex",
  "metadata": { "title": "...", "author": "..." },
  "tests": [
    {
      "name": "full-doc",
      "input": "<Doc>.md",
      "document": "<Doc>.md",
      "lua_filters": ["filter-a", "filter-b"],
      "pandoc_args": ["--top-level-division=chapter", "--toc", "--toc-depth=2"]
    }
  ]
}
```

Gotchas (learned the hard way):
- `template` needs the **`.latex` extension** (resolved as `templates/<template>`).
- Include **both `input` and `document`** with the same value — daemon versions differ on which they read.
- `lua_filters` names need **no `.lua`**. `pandoc_args` should **NOT** include `--pdf-engine` (the daemon adds `xelatex`).
- **A missing referenced image is FATAL, not a warning** — `! Unable to load picture or PDF file '…'` → `No pages of output` → no PDF, even though earlier lines say only `LaTeX Warning: File not found`. If a build fails with no obvious LaTeX error, grep the compile log for `Unable to load picture`; the fix is staging the asset to the referenced path (see Step 1 Assets).
- **A newly-added `.latex` template only registers when the daemon sees it.** It's resolved from `templates/` per request, so a host-side copy is normally picked up; if a brand-new template reports "Template not found," confirm it landed in `templates/` and re-submit.

## Step 3 — Wait for completion

```bash
cd engineering/pdf-forge/interactive-testing
for i in $(seq 1 24); do
  run=$(ls -1dt test-runs/<request_id>_*/ 2>/dev/null | head -1)
  [ -n "$run" ] && [ -f "${run}summary.json" ] && { echo "DONE: $run"; break; }
  sleep 5
done
tail -6 status/activity.log
```
A full document is ~25–35 s. The request file moves out of `test-requests/` (archived) once picked up.

## Step 4 — INSPECT (do not trust the success flag)

**A build can report `success` / 100% while silently dropping content.** Always do all three:

1. **Compile-log scan** — `<run>/<test>/output.compile.log` (present once the patched daemon is deployed; capture added 2026-06-04). Grep for the serious signatures:
   ```bash
   for s in "Float(s) lost" "Not in outer par mode" "! LaTeX Error" "Undefined control sequence" "Emergency stop"; do
     printf "%2s × %s\n" "$(grep -c "$s" <run>/<test>/output.compile.log)" "$s"
   done
   ```
   Any non-zero = content was likely dropped despite a green build. (Overfull/Underfull are normal — not in this list.)

2. **Text-presence check** — the daemon only thumbnails page 1, and your container has **no poppler**, so use **PyMuPDF** (`pip install --user pymupdf`; pure-Python, no system deps) to confirm specific demo strings actually made it into the PDF and to find which page each landed on:
   ```python
   import fitz
   doc = fitz.open("<run>/<test>/output.pdf")
   def page_of(s):
       return next((i+1 for i,pg in enumerate(doc) if s in pg.get_text()), None)
   for label, needle in CHECKS:   # pick strings unique to each demo you expect
       print(f"{'p'+str(page_of(needle)) if page_of(needle) else 'ABSENT':8} | {label}")
   ```
   `ABSENT` = dropped — the real failure mode here, invisible to the success flag.

3. **Visual** — render the pages you care about and LOOK (diagrams = vector paths, won't show in text):
   ```python
   doc[PAGE-1].get_pixmap(dpi=110).save("/tmp/pg.png")   # then Read /tmp/pg.png as an image
   ```
   Check `len(doc[i].get_drawings())` to confirm a TikZ diagram actually rendered on the expected page (and isn't pushed off the mediabox).

## Step 5 — Iterate

Edit the template/filter/markdown, **bump the version** (`-v2`), re-stage (re-escape the markdown), resubmit, and compare. Keep going until the compile log is clean, text-presence shows 0 absent, and the rendered pages look right.

When the behavior is nailed down, port the proven change back to the real source (e.g. promote the markdown to `opus-master`, commit the template/filter), then hand production off to `prepare-manual` + manual deploy.

## Step 6 — Close out the daemon

Testing complete? **Tell the user to stop the Forge daemon** (see the lifecycle note at the top). This is a required step, not optional — the daemon idles on their machine until they stop it, and only you know the session is over.

## Known failure patterns (catalogue)

- **`\vspace*`-based "force to page foot" drops the content below it** — every demo after the `\vspace*` can vanish from the PDF. Prefer mechanisms that don't push a float past the page bottom.
- **Figure nested in a figure drops the image / doubles the caption** — a diagram macro that is itself a `\begin{figure}` wrapped again by the figures filter. De-nest the macro so only one `figure` wraps it.
- See memory `reference_forge_silent_content_drop` and `reference_pdf_forge_interaction_model`.
