#!/usr/bin/env python3
"""
Verify example-corpus identity for a P2 manual.

Asserts that every loose `examples-library/<name>.spin2` file is BYTE-IDENTICAL
to the fenced code block in the manual's `opus-master/*.md` that carries the
matching `caption="<name>.spin2"`. This is the anti-drift gate for the shipped
example ZIP: readers open the loose files in an external tool (Prop Tool IDE /
PNut-Term-TS), so a loose file that has silently diverged from the manual's
printed code block is a trust defect ([[feedback_example_file_matches_code_block_not_figure]]).

What it checks (all three must hold for GREEN):
  1. IDENTITY   — for every caption that has a library file, block bytes == file bytes.
  2. NO ORPHAN LIBRARY — every `examples-library/*.spin2` has a matching captioned block.
  3. NO ORPHAN BLOCK   — every captioned `*.spin2` block has a matching library file.
  (also flags DUPLICATE captions — the same filename captioned by two blocks.)

The rule is file <-> printed-code-block identity ONLY. It does NOT require the
rendered figure to match the published screenshot, and it does NOT compile or run
the examples (that is pnut-ts -d and the hardware run-list, separate gates).

Usage:
    verify-example-corpus-identity.py [--manual DIR] [--report FILE] [-q]

    --manual DIR   Manual directory containing opus-master/ and examples-library/.
                   Default: the P2 Debug Window manual.
    --report FILE  Also write the full report to FILE (Markdown).
    -q, --quiet    Print only the one-line verdict + any failures.

Exit code: 0 if GREEN (all identical, no orphans, no duplicates), 1 otherwise.
So it can gate a re-zip / release step:  python3 ... && zip ...
"""

import argparse
import sys
from pathlib import Path

# Repo-root-relative default (this file lives at engineering/tools/).
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANUAL = (
    REPO_ROOT
    / "engineering/document-production/manuals/p2-debug-window-manual"
)

FENCE = "```"


def extract_captioned_blocks(md_path: Path):
    """Yield (caption, block_bytes) for each fenced block whose opening line
    carries caption="<something>.spin2".

    block_bytes is the exact content between the opening fence line and the
    closing fence line, reconstructed as the lines joined by '\n' with a single
    trailing '\n' — the on-disk form a loose .spin2 file takes.
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith(FENCE) and 'caption="' in stripped and ".spin2" in stripped:
            # Pull the caption filename out of caption="...".
            start = stripped.index('caption="') + len('caption="')
            end = stripped.index('"', start)
            caption = stripped[start:end]
            # Collect content until the next bare closing fence.
            body = []
            j = i + 1
            while j < n and lines[j].strip() != FENCE:
                body.append(lines[j])
                j += 1
            block = ("\n".join(body) + "\n").encode("utf-8")
            yield caption, block, md_path.name, i + 1
            i = j + 1
        else:
            i += 1


def main():
    ap = argparse.ArgumentParser(
        description="Verify examples-library files are byte-identical to their opus-master code blocks."
    )
    ap.add_argument("--manual", default=str(DEFAULT_MANUAL),
                    help="Manual dir containing opus-master/ and examples-library/")
    ap.add_argument("--report", default=None, help="Write the full Markdown report to this file too")
    ap.add_argument("-q", "--quiet", action="store_true", help="Only print the verdict and failures")
    args = ap.parse_args()

    manual = Path(args.manual).resolve()
    opus = manual / "opus-master"
    lib = manual / "examples-library"

    if not opus.is_dir():
        print(f"ERROR: no opus-master/ under {manual}", file=sys.stderr)
        return 2
    if not lib.is_dir():
        # No corpus to check — vacuously green.
        print(f"GREEN: no examples-library/ under {manual.name} — nothing to check.")
        return 0

    # Collect captioned blocks across all chapter/appendix masters. Scan
    # RECURSIVELY: some manuals nest chapters (opus-master/part-N/chapter-*.md,
    # e.g. p2-io-and-smart-pins-user-guide) rather than keeping them flat.
    blocks = {}          # caption -> (bytes, source_md, line)
    duplicates = []      # (caption, first_src, dup_src)
    for md in sorted(opus.rglob("*.md")):
        for caption, block, src, line in extract_captioned_blocks(md):
            if caption in blocks:
                duplicates.append((caption, blocks[caption][1], src))
            else:
                blocks[caption] = (block, src, line)

    lib_files = {p.name: p for p in sorted(lib.glob("*.spin2"))}

    # Compare.
    identical, mismatched, orphan_block, orphan_lib = [], [], [], []
    for caption, (block, src, line) in sorted(blocks.items()):
        if caption not in lib_files:
            orphan_block.append((caption, src))
            continue
        file_bytes = lib_files[caption].read_bytes()
        if file_bytes == block:
            identical.append(caption)
        else:
            mismatched.append((caption, src, first_diff(file_bytes, block)))
    for name in sorted(lib_files):
        if name not in blocks:
            orphan_lib.append(name)

    green = not (mismatched or orphan_block or orphan_lib or duplicates)

    # ---- report ----
    out = []
    out.append(f"# Example-corpus identity report — {manual.name}")
    out.append("")
    out.append(f"- captioned `.spin2` blocks: **{len(blocks)}**")
    out.append(f"- `examples-library/*.spin2` files: **{len(lib_files)}**")
    out.append(f"- identical: **{len(identical)}** · mismatched: **{len(mismatched)}** · "
               f"orphan blocks: **{len(orphan_block)}** · orphan library files: **{len(orphan_lib)}** · "
               f"duplicate captions: **{len(duplicates)}**")
    out.append("")
    if mismatched:
        out.append("## MISMATCH — loose file differs from its opus-master block")
        for caption, src, diff in mismatched:
            out.append(f"- `{caption}` (block in `{src}`): {diff}")
        out.append("")
    if orphan_block:
        out.append("## ORPHAN BLOCK — captioned example has no library file")
        for caption, src in orphan_block:
            out.append(f"- `{caption}` (in `{src}`) — no `examples-library/{caption}`")
        out.append("")
    if orphan_lib:
        out.append("## ORPHAN LIBRARY FILE — loose file has no captioned block")
        for name in orphan_lib:
            out.append(f"- `examples-library/{name}` — no `caption=\"{name}\"` block in any master")
        out.append("")
    if duplicates:
        out.append("## DUPLICATE CAPTION — same filename captioned by two blocks")
        for caption, first_src, dup_src in duplicates:
            out.append(f"- `{caption}` — in both `{first_src}` and `{dup_src}`")
        out.append("")
    out.append(f"## VERDICT: {'GREEN — corpus is byte-identical' if green else 'RED — corpus has drifted'}")
    report = "\n".join(out) + "\n"

    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")

    if args.quiet:
        for caption, src, diff in mismatched:
            print(f"MISMATCH {caption} ({src}): {diff}")
        for caption, src in orphan_block:
            print(f"ORPHAN-BLOCK {caption} ({src})")
        for name in orphan_lib:
            print(f"ORPHAN-LIB {name}")
        for caption, a, b in duplicates:
            print(f"DUPLICATE {caption} ({a} & {b})")
        print(f"{'GREEN' if green else 'RED'}: {len(identical)}/{len(blocks)} identical, "
              f"{len(mismatched)} mismatched, {len(orphan_block)+len(orphan_lib)} orphans, "
              f"{len(duplicates)} duplicates ({manual.name})")
    else:
        print(report)

    return 0 if green else 1


def first_diff(a: bytes, b: bytes) -> str:
    """Human-readable location of the first differing byte (1-based line/col)."""
    if a == b:
        return "identical"
    minlen = min(len(a), len(b))
    idx = next((k for k in range(minlen) if a[k] != b[k]), minlen)
    line = a[:idx].count(b"\n") + 1
    col = idx - (a.rfind(b"\n", 0, idx) + 1) + 1
    if idx == minlen and len(a) != len(b):
        longer = "library file" if len(a) > len(b) else "opus-master block"
        return f"length differs ({len(a)} file vs {len(b)} block) — {longer} is longer; first extra at line {line}"
    return f"first differs at line {line}, col {col}"


if __name__ == "__main__":
    sys.exit(main())
