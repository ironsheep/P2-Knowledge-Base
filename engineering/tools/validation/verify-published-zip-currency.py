#!/usr/bin/env python3
"""
verify-published-zip-currency.py - the PUBLISHED example ZIP matches the corpus.

WHY THIS EXISTS
    `verify-example-corpus-identity.py` proves that `examples-library/*.spin2`
    matches the manual's printed code blocks. It says NOTHING about the archive
    readers actually download, `deliverables/documents/DOCs/<slug>-src.zip`.
    Those are different questions, and the gap between them shipped:

        Debug Window v1.1.3 - corpus identity GREEN 34/34, while the published
        ZIP was dated three weeks earlier and 13 example files had changed since.
        Several were the F-281/F-290/F-292 repairs, where the OLD code compiles
        clean and runs a DIFFERENT PROGRAM than the page shows. A reader
        downloading that ZIP would have got working-looking code that contradicts
        the manual they were reading.

    Nothing caught it. The release checklist verified corpus identity, saw GREEN,
    and moved on - because "the examples are correct" and "the archive we ship
    contains the correct examples" read like the same sentence.

WHAT IT CHECKS
    Every file in the published ZIP is byte-identical to its counterpart in
    examples-library/, and every shippable corpus file is present in the ZIP.
    Byte comparison, not timestamps: a ZIP rebuilt from a stale directory has a
    fresh mtime and stale contents.

NOT SHIPPED, BY DESIGN
    Editor/OS droppings (.DS_Store, .vscode), compiler output (*.bin, *.lst -
    recreatable from source and never committed), and any dated scratch folder.
    These are excluded from the "must be in the ZIP" side, not flagged as drift.

USAGE
    verify-published-zip-currency.py --manual <manual-dir> [--zip <path>]

    --zip defaults to deliverables/documents/DOCs/<slug>-src.zip

EXIT STATUS
    0  ZIP matches the corpus (or the manual publishes no ZIP - nothing to check)
    1  ZIP is stale, incomplete, or carries files the corpus does not
    2  usage error
"""

import argparse
import filecmp
import os
import sys
import tempfile
import zipfile

# Never expected inside the published archive.
EXCLUDE_NAMES = {'.DS_Store', '.vscode', '__pycache__'}
EXCLUDE_EXT = {'.bin', '.lst', '.zip'}


def shippable(root):
    """Files in the corpus that the published ZIP is expected to carry."""
    out = {}
    for name in os.listdir(root):
        path = os.path.join(root, name)
        if name in EXCLUDE_NAMES or name.startswith('.'):
            continue
        if os.path.isdir(path):
            continue                       # dated scratch folders never ship
        if os.path.splitext(name)[1].lower() in EXCLUDE_EXT:
            continue
        out[name] = path
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--manual', required=True,
                    help='manual dir containing examples-library/')
    ap.add_argument('--zip', dest='zippath')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    slug = os.path.basename(os.path.normpath(args.manual))
    corpus = os.path.join(args.manual, 'examples-library')
    zippath = args.zippath or os.path.join(
        'deliverables', 'documents', 'DOCs', f'{slug}-src.zip')

    if not os.path.isdir(corpus):
        if not args.quiet:
            print(f'GREEN: no examples-library/ under {slug} — no ZIP to check.')
        return 0
    if not os.path.isfile(zippath):
        print(f'RED: {slug} has an examples-library/ but no published ZIP at '
              f'{zippath}', file=sys.stderr)
        return 1

    expected = shippable(corpus)
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(zippath) as zf:
            zf.extractall(tmp)
        shipped = {}
        for dirpath, _dirs, files in os.walk(tmp):
            for f in files:
                shipped[os.path.relpath(os.path.join(dirpath, f), tmp)] = \
                    os.path.join(dirpath, f)

        missing = sorted(set(expected) - set(shipped))
        extra = sorted(set(shipped) - set(expected))
        stale = sorted(n for n in set(expected) & set(shipped)
                       if not filecmp.cmp(expected[n], shipped[n], shallow=False))

        if not (missing or extra or stale):
            if not args.quiet:
                print(f'GREEN: {len(expected)}/{len(expected)} files in '
                      f'{os.path.basename(zippath)} byte-identical to '
                      f'examples-library/ ({slug})')
            return 0

        print(f'RED: published ZIP does not match the corpus ({slug})')
        if stale:
            print(f'  {len(stale)} file(s) DIFFER — the ZIP ships different code '
                  f'than the corpus:')
            for n in stale:
                print(f'      {n}')
        if missing:
            print(f'  {len(missing)} corpus file(s) MISSING from the ZIP:')
            for n in missing:
                print(f'      {n}')
        if extra:
            print(f'  {len(extra)} file(s) in the ZIP with no corpus counterpart:')
            for n in extra:
                print(f'      {n}')
        print('\nFIX: rebuild the ZIP from examples-library/ (after corpus '
              'identity is GREEN), then re-run this.')
        return 1


if __name__ == '__main__':
    sys.exit(main())
