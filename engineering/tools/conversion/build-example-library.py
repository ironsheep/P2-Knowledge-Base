#!/usr/bin/env python3
"""
build-example-library.py — extract a manual's worked-example code blocks into a
curated example library + ZIP.

THE MECHANISM (see methodology: example-library-mechanism.md)
------------------------------------------------------------
A *worked example* is a complete, runnable program the author has curated — NOT
every fenced snippet. The author tags each one in the manual's markdown with a
filename caption attribute, using the semantic chNN-description.spin2 naming:

    ```{.spin2 caption="ch05-plot-gauge.spin2"}
    CON _clkfreq = 200_000_000
    PUB main()
      ...
    ```

The caption always rides the CODE FENCE itself. If a worked example is wrapped in a
::: color div, the caption still goes on the inner ``` fence (pandoc transforms the
inner code block before the outer div, so a caption on the div would never render).

The caption attribute is the SINGLE SOURCE OF TRUTH:
  - the code-coloring Lua filter prints it as a small filename under the box, and
  - THIS script extracts every caption-tagged block to a file of that exact name,
    so the shipped file is, verbatim, the printed block ("exactly as printed").

Bare code blocks (no caption attribute) are snippets: not captioned, not extracted.

USAGE
-----
    build-example-library.py <manual.md> <examples-library-dir> [--zip <path.zip>]

Writes one file per caption into <examples-library-dir>, (re)builds the ZIP, and
prints a summary. Existing files in the dir that are no longer referenced are
reported (not deleted — the author decides). A hand-authored README.md in the dir
is never overwritten.
"""
import argparse
import os
import re
import sys
import zipfile

# A fence-open line: 3+ backticks, then either a brace-attr block {...} or a bare
# info word (spin2, pasm2, ...). Capture the tick run and the trailing info.
FENCE_RE = re.compile(r'^(`{3,})[ \t]*(.*?)[ \t]*$')
CAPTION_RE = re.compile(r'caption[ \t]*=[ \t]*"([^"]+)"')


def extract_examples(md_text):
    """Return [(filename, content), ...] in document order for caption-tagged code fences.

    The caption attribute lives on the CODE FENCE itself — ```{.spin2 caption="..."} —
    NOT on any wrapping ::: color div. (Pandoc applies the inner CodeBlock before the
    outer Div, so a caption on the div never reaches the renderer; keeping the caption
    on the fence is the one rule that the renderer and this extractor both honor, so
    the printed caption and the shipped file can never disagree.)
    """
    lines = md_text.split('\n')
    n = len(lines)
    examples = []
    i = 0
    while i < n:
        fm = FENCE_RE.match(lines[i])
        if fm:
            ticks, info = fm.group(1), fm.group(2)
            cap = CAPTION_RE.search(info)
            # Collect body up to the matching close fence (>= same tick count, no info).
            close_re = re.compile(r'^`{%d,}[ \t]*$' % len(ticks))
            j = i + 1
            body = []
            while j < n and not close_re.match(lines[j]):
                body.append(lines[j])
                j += 1
            if cap:
                examples.append((cap.group(1), '\n'.join(body)))
            i = j + 1
            continue
        i += 1
    return examples


def main():
    ap = argparse.ArgumentParser(description="Extract a manual's worked-example code blocks into a curated example library + ZIP.")
    ap.add_argument('markdown', help='the manual markdown to scan')
    ap.add_argument('outdir', help='examples-library directory to write files into')
    ap.add_argument('--zip', dest='zippath', default=None,
                    help='ZIP path to (re)build (default: <outdir>.zip)')
    args = ap.parse_args()

    if not os.path.isfile(args.markdown):
        sys.exit(f"ERROR: markdown not found: {args.markdown}")
    with open(args.markdown, encoding='utf-8') as fh:
        md_text = fh.read()

    examples = extract_examples(md_text)
    if not examples:
        print(f"No caption-tagged examples found in {args.markdown}.")
        print('Tag a worked example with:  ```{.spin2 caption="chNN-description.spin2"}')
        return

    # Duplicate-filename guard: same caption used twice is an authoring error.
    seen = {}
    dupes = []
    for fn, _ in examples:
        seen[fn] = seen.get(fn, 0) + 1
        if seen[fn] == 2:
            dupes.append(fn)
    if dupes:
        sys.exit("ERROR: duplicate example caption(s) — each filename must be unique:\n  "
                 + "\n  ".join(sorted(set(dupes))))

    os.makedirs(args.outdir, exist_ok=True)
    written = []
    for fn, content in examples:
        # the caption is a bare filename; reject path separators defensively
        if '/' in fn or '\\' in fn or fn.startswith('.'):
            sys.exit(f"ERROR: unsafe example filename in caption: {fn!r}")
        path = os.path.join(args.outdir, fn)
        text = content if content.endswith('\n') else content + '\n'
        with open(path, 'w', encoding='utf-8') as out:
            out.write(text)
        written.append(fn)

    # Report orphaned files (present in dir but not referenced) — do not delete.
    referenced = set(written)
    orphans = []
    for existing in sorted(os.listdir(args.outdir)):
        if existing in ('README.md',) or existing.startswith('.'):
            continue
        if existing.endswith('.zip'):
            continue
        if os.path.isfile(os.path.join(args.outdir, existing)) and existing not in referenced:
            orphans.append(existing)

    # (Re)build the ZIP from the referenced files only (deterministic order).
    zippath = args.zippath or (args.outdir.rstrip('/') + '.zip')
    with zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fn in written:
            zf.write(os.path.join(args.outdir, fn), arcname=fn)
        readme = os.path.join(args.outdir, 'README.md')
        if os.path.isfile(readme):
            zf.write(readme, arcname='README.md')

    print(f"Example library built from {args.markdown}")
    print(f"  {len(written)} worked example(s) -> {args.outdir}")
    print(f"  ZIP: {zippath}")
    if orphans:
        print(f"  NOTE: {len(orphans)} file(s) in {args.outdir} are no longer referenced "
              f"by a caption (left in place, NOT zipped): {', '.join(orphans)}")
    if not os.path.isfile(os.path.join(args.outdir, 'README.md')):
        print(f"  NOTE: no README.md index in {args.outdir} — author the curated index "
              f"(File / what-it-shows table) per the methodology.")


if __name__ == '__main__':
    main()
