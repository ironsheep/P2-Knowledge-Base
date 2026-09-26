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
import re
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


# --- generated-header awareness (see engineering/tools/sync-manual-examples.py) ---
#
# A document that has adopted generated example headers ships each file as
#   <generated header> + <body> + <MIT licence footer>
# where the BODY is what the manual prints. The identity promise is unchanged --
# the code you read is the code that builds -- but it is asserted against the
# body rather than the whole file. A file with no generated header is compared
# whole, exactly as before, so un-adopted documents are unaffected.

ADOPT_SENTINEL = b"This file is an EXAMPLE from the manual above."
_BANNER = b"'' ==="


def strip_generated_wrapper(raw: bytes) -> bytes:
    """Return the body of an adopted example file; raw unchanged if not adopted."""
    if ADOPT_SENTINEL not in raw or not raw.startswith(_BANNER):
        return raw
    end = raw.find(b"\n", raw.find(_BANNER, len(_BANNER)))
    if end == -1:
        return raw
    body = raw[end + 1:].lstrip(b"\n")
    m = re.search(rb"\n\{\{\n(?:.|\n)*?\n\}\}\s*$", body)
    if m:
        body = body[:m.start()]
    return body.rstrip(b"\n") + b"\n"


# --- whole-program archive awareness (sync-manual-examples.py ARCHIVE MODE) ---
#
# Some manuals ship whole test programs and PRINT ONLY EXCERPTS of them (P2
# Errata: 500-1,600-line rigs, 2-15-line excerpts). No block can equal such a
# file, so the file<->block rule cannot apply; the promise is instead that every
# excerpt the manual prints is the program's own code: each uncaptioned
# ```spin2 / ```pasm2 fence must appear, as contiguous lines, in an archive file.
# Opt-in by the sync tool's archive header sentence, so a document that merely
# names a file it has not captioned (the app-note caption gap) is NOT excused.

ARCHIVE_SENTINEL = b"It is the whole"


def is_archive_file(raw: bytes) -> bool:
    return (raw.startswith(_BANNER) and ADOPT_SENTINEL in raw
            and ARCHIVE_SENTINEL in raw[:raw.find(_BANNER, len(_BANNER)) + 1])


def uncaptioned_code_fences(md_path: Path):
    """Yield (lines, source_md, line_no) for each ```spin2/```pasm2 fence with no caption."""
    lines = md_path.read_text(encoding="utf-8").split("\n")
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if (s.startswith(FENCE + "spin2") or s.startswith(FENCE + "pasm2")) and "caption=" not in s:
            body, j = [], i + 1
            while j < n and lines[j].strip() != FENCE:
                body.append(lines[j])
                j += 1
            yield body, md_path.name, i + 1
            i = j + 1
        else:
            i += 1


def contains_contiguous(hay, needle) -> bool:
    k = len(needle)
    return k > 0 and any(hay[p:p + k] == needle for p in range(len(hay) - k + 1))


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
        file_bytes = strip_generated_wrapper(lib_files[caption].read_bytes())
        if file_bytes == block:
            identical.append(caption)
        else:
            mismatched.append((caption, src, first_diff(file_bytes, block)))
    archive = {}         # name -> body lines, for whole-program archive files
    for name in sorted(lib_files):
        if name not in blocks:
            raw = lib_files[name].read_bytes()
            if is_archive_file(raw):
                archive[name] = strip_generated_wrapper(raw).decode("utf-8").split("\n")
            else:
                orphan_lib.append(name)

    # Archive mode: every uncaptioned code fence must be an excerpt of an archive file.
    excerpt_ok, excerpt_bad = 0, []
    if archive:
        for md in sorted(opus.rglob("*.md")):
            for body, src, line in uncaptioned_code_fences(md):
                if any(contains_contiguous(a, body) for a in archive.values()):
                    excerpt_ok += 1
                else:
                    excerpt_bad.append((src, line, body[0] if body else ""))

    green = not (mismatched or orphan_block or orphan_lib or duplicates or excerpt_bad)

    # ---- report ----
    out = []
    out.append(f"# Example-corpus identity report — {manual.name}")
    out.append("")
    out.append(f"- captioned `.spin2` blocks: **{len(blocks)}**")
    out.append(f"- `examples-library/*.spin2` files: **{len(lib_files)}**")
    out.append(f"- identical: **{len(identical)}** · mismatched: **{len(mismatched)}** · "
               f"orphan blocks: **{len(orphan_block)}** · orphan library files: **{len(orphan_lib)}** · "
               f"duplicate captions: **{len(duplicates)}**")
    if archive:
        out.append(f"- whole-program archive files: **{len(archive)}** · printed excerpts found "
                   f"verbatim in them: **{excerpt_ok}** · excerpts NOT found: **{len(excerpt_bad)}**")
    out.append("")
    if excerpt_bad:
        out.append("## EXCERPT DRIFT — a printed fence is not contiguous in any archive file")
        for src, line, first in excerpt_bad:
            out.append(f"- `{src}:{line}` — begins `{first.strip()[:60]}`")
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
        for src, line, first in excerpt_bad:
            print(f"EXCERPT-DRIFT {src}:{line} ({first.strip()[:60]})")
        arch = (f", {len(archive)} archive files with {excerpt_ok} excerpts verbatim"
                f"{', ' + str(len(excerpt_bad)) + ' drifted' if excerpt_bad else ''}"
                if archive else "")
        print(f"{'GREEN' if green else 'RED'}: {len(identical)}/{len(blocks)} identical, "
              f"{len(mismatched)} mismatched, {len(orphan_block)+len(orphan_lib)} orphans, "
              f"{len(duplicates)} duplicates{arch} ({manual.name})")
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
