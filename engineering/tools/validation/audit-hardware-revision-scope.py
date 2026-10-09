#!/usr/bin/env python3
"""Is every board rating in a revision-declaring hardware YAML stated with its revision scope?

WHY THIS EXISTS (F-454 / S-386). A CORRECT current-revision number stripped of the scope
that made it correct: Rev A/B VIN maximum is 5.5 V, Rev C and later 16 V. Applying the
16 V figure to a Rev A/B module destroys it. No content check can know that a rating
differs across revisions -- that lives in the source's Revision History -- so this gate
cannot judge the number. What it CAN enforce is that the author MADE AND RECORDED the
decision, and that a rating in a revision-declaring file carries its scope.

Scope: deliverables/ai/P2/hardware/*.yaml (or the paths given).

Rules.
  R-A  declared decision. A file that declares a board revision (top-level
       `module_revision:` / `board_revision:` / `board_revision_note:`, or a `# Revision:`
       header comment line) must contain, at any depth, either a non-empty `board_revisions:`
       mapping or a `revision_scope_reviewed:` mapping with non-empty `source:` and `finding:`.
       Else FAIL: "revision declared, scope never reviewed".
  R-B  rating scoped. In such a file, every string under a rating key
       ^(vin|input_voltage|absolute_maximum|supply_voltage|vin_maximum|max_[a-z_]+|[a-z_]+_max(imum)?)$
       that holds a number with an electrical unit (V, VDC, A, mA, W ...) must name a revision
       (\\bRev(ision)?[ .]?[A-F]\\b) in the same string, or sit inside the `board_revisions:`
       mapping. A non-empty `revision_scope_reviewed:` mapping (source + finding) waives R-B:
       the recorded review is the scope decision.
       Frequencies with an SI prefix (kHz, MHz, GHz) are NOT electrical ratings that change
       with a board revision here: `recommended_maximum: "180 MHz"` in the real Rev D file
       (edge-standard-module.yaml) must stay clean. Key lists and units are proposals for review.

Usage:
    audit-hardware-revision-scope.py [path ...]     # files or directories (default deliverables/ai/P2/hardware)
    audit-hardware-revision-scope.py --negative-control

Exit 0 clean, 1 defects found (release blocks), 2 the tool could not audit.

A green does NOT certify: that a rating is right for the revision named, or that the Revision
History was read correctly -- only that the file records a scope decision and that a rating in
a revision-declaring file is qualified. A deleted Revision History that leaves no
`module_revision` marker (the F-454 mechanism exactly, if the marker went with it) is
INVISIBLE to this gate.
"""
import glob
import os
import re
import sys
import tempfile

try:
    import yaml
except ImportError:
    print("PyYAML not available", file=sys.stderr)
    sys.exit(2)

DECL_KEYS = ("module_revision", "board_revision", "board_revision_note")
HEADER_RE = re.compile(r'^#\s*Revision:', re.M)
RATING_KEY_RE = re.compile(
    r'^(vin|input_voltage|absolute_maximum|supply_voltage|vin_maximum|max_[a-z_]+|[a-z_]+_max(imum)?)$')
UNIT_RE = re.compile(r'(?<![A-Za-z])\d+(?:\.\d+)?\s*(?:m|k|u|µ)?(?:V|A|W)(?:DC|AC|cc|CC)?(?![A-Za-z])'
                     r'|(?<![A-Za-z])\d+(?:\.\d+)?\s*Hz\b')
REV_RE = re.compile(r'\bRev(?:ision)?[ .]?[A-F]\b')


def declares_revision(text, doc):
    if HEADER_RE.search(text):
        return True
    return isinstance(doc, dict) and any(k in doc for k in DECL_KEYS)


def find_key(node, name):
    """Yield every value stored under key `name` at any depth."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == name:
                yield v
            yield from find_key(v, name)
    elif isinstance(node, list):
        for v in node:
            yield from find_key(v, name)


def nonempty(x):
    return isinstance(x, str) and x.strip() != ''


def has_decision(doc):
    """(has_board_revisions, has_reviewed_ok, reviewed_present_but_bad)"""
    br = any(isinstance(v, dict) and v for v in find_key(doc, 'board_revisions'))
    rev_ok = False
    rev_bad = False
    for v in find_key(doc, 'revision_scope_reviewed'):
        if isinstance(v, dict) and nonempty(v.get('source')) and nonempty(v.get('finding')):
            rev_ok = True
        else:
            rev_bad = True
    return br, rev_ok, rev_bad


def rating_strings(node, path='', inside_br=False):
    """Yield (path, key, string) for every string under a rating key outside board_revisions."""
    if isinstance(node, dict):
        for k, v in node.items():
            p = f"{path}.{k}" if path else str(k)
            in_br = inside_br or k == 'board_revisions'
            if isinstance(v, str) and isinstance(k, str) and RATING_KEY_RE.match(k) and not in_br:
                yield p, k, v
            else:
                yield from rating_strings(v, p, in_br)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from rating_strings(v, f"{path}[{i}]", inside_br)


def check_text(text):
    """Return (declares, [(rule, where, detail)]). Raises on parse failure."""
    doc = yaml.safe_load(text)
    if not declares_revision(text, doc):
        return False, []
    out = []
    br, rev_ok, rev_bad = has_decision(doc)
    if not (br or rev_ok):
        if rev_bad:
            out.append(('R-A', 'revision_scope_reviewed',
                        'revision_scope_reviewed is present but its source/finding is empty'))
        else:
            out.append(('R-A', '<file>',
                        'revision declared, scope never reviewed (no board_revisions: and no revision_scope_reviewed:)'))
    if not rev_ok:
        for p, k, s in rating_strings(doc):
            if UNIT_RE.search(s) and not REV_RE.search(s):
                out.append(('R-B', p, f'rating with no revision named: {s!r}'))
    return True, out


def scan(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += glob.glob(os.path.join(p, '*.yaml'))
        elif p.endswith('.yaml'):
            files.append(p)
    files = sorted(set(files))
    declaring = 0
    n_a = n_b = 0
    bad_files = 0
    parse_fail = 0
    for f in files:
        try:
            with open(f, encoding='utf-8') as fh:
                decl, finds = check_text(fh.read())
        except Exception as e:  # noqa: BLE001
            print(f"  PARSE-FAIL {f}: {e}")
            parse_fail += 1
            continue
        declaring += decl
        if finds:
            bad_files += 1
        for rule, where, detail in finds:
            print(f"  {rule} {f} [{where}]: {detail}")
            if rule == 'R-A':
                n_a += 1
            else:
                n_b += 1
    return files, declaring, n_a, n_b, bad_files, parse_fail


def negative_control():
    """A gate that cannot fail has not been verified, it has been RUN."""
    # (label, text, expected set of rules fired)
    fire = [
        ("module_revision Rev B + `vin: 16 V maximum`, no board_revisions -> R-A and R-B",
         'module_revision: "Rev B"\nspecs:\n  vin: "16 V maximum"\n', {'R-A', 'R-B'}),
        ("`absolute_maximum: 5.5 VDC` in a revision-declaring (header-comment) file -> R-B",
         '# Revision: Rev B\nboard_revisions:\n  rev_b:\n    note: x\nspecs:\n  absolute_maximum: "5.5 VDC"\n', {'R-B'}),
        ("revision_scope_reviewed with an EMPTY finding -> R-A",
         'board_revision: "Rev C"\nrevision_scope_reviewed:\n  source: "guide v2 Revision History"\n  finding: ""\n', {'R-A'}),
        ("revision_scope_reviewed with an EMPTY finding does not waive R-B",
         'board_revision: "Rev C"\nrevision_scope_reviewed:\n  source: "g"\n  finding: ""\nsupply_voltage: "USB 5 VDC, absolute maximum 5.5 VDC"\n',
         {'R-A', 'R-B'}),
    ]
    clean = [
        ("real edge-standard-module shape: scalar names Rev, board_revisions present, 180 MHz unqualified",
         'module_revision: "Rev D"\nspecifications:\n  clock:\n    recommended_maximum: "180 MHz"\n'
         '  power:\n    input_voltage: "5-16 VDC on Rev C and later; Rev A and Rev B maximum 5.5 VDC"\n'
         '  board_revisions:\n    source: s\n    rev_b:\n      vin_maximum: "5.5 V"\n', set()),
        ("`vin: 5 V` in a file declaring no revision",
         'specs:\n  vin: "5 V"\n', set()),
        ("`vin_maximum: 5.5 V` inside a board_revisions entry",
         'module_revision: "Rev B"\nboard_revisions:\n  rev_a:\n    vin_maximum: "5.5 V"\n', set()),
        ("revision_scope_reviewed (source+finding) + a rating with no Rev token: R-B waived",
         'board_revision: "Rev C"\nrevision_scope_reviewed:\n  source: "guide Revision History"\n'
         '  finding: "Revision History lists no rating change"\nsupply_voltage: "USB 5 VDC, absolute maximum 5.5 VDC"\n', set()),
        ("non-rating key holding volts in a revision-declaring file",
         'module_revision: "Rev B"\nboard_revisions:\n  rev_b:\n    note: x\ndescription: "runs at 3.3 V"\n', set()),
    ]
    ok = True
    for label, text, want in [(l, t, w) for l, t, w in fire] + [(l, t, w) for l, t, w in clean]:
        try:
            _, finds = check_text(text)
        except Exception as e:  # noqa: BLE001
            print(f"  [**FAIL**] {label}: case did not parse ({e}) -- a gate failure, not a skip")
            ok = False
            continue
        got = {r for r, _, _ in finds}
        good = got == want
        ok = ok and good
        print(f"  [{'PASS' if good else '**FAIL**'}] {label}: fired {sorted(got) or 'nothing'} (want {sorted(want) or 'nothing'})")
    # end-to-end through scan()
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'bad.yaml')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write('module_revision: "Rev B"\nvin: "16 V maximum"\n')
    _, decl, na, nb, bf, pf = scan([p])
    good = (decl, na, nb, bf, pf) == (1, 1, 1, 1, 0)
    ok = ok and good
    print(f"  [{'PASS' if good else '**FAIL**'}] end-to-end scan() of a bad file: declaring={decl} R-A={na} R-B={nb}")
    print()
    if ok:
        print("Negative control PASSED -- R-A and R-B fire on an unreviewed revision-declaring file, on an")
        print("empty review, and on an unqualified rating; the real Rev D shape, scoped ratings and a")
        print("recorded review stay clean.")
    else:
        print("Negative control FAILED.")
    return 0 if ok else 1


if __name__ == '__main__':
    argv = sys.argv[1:]
    if '--negative-control' in argv:
        sys.exit(negative_control())
    args = argv or ['deliverables/ai/P2/hardware']
    files, declaring, n_a, n_b, bad_files, parse_fail = scan(args)
    if not files:
        print("NOTHING MEASURED -- no .yaml files found under the given path(s). This is not a pass.")
        sys.exit(2)
    print(f"\n  files scanned: {len(files)}   declaring a revision: {declaring}   "
          f"R-A findings: {n_a}   R-B findings: {n_b}   files with findings: {bad_files}   parse failures: {parse_fail}")
    if parse_fail:
        print("  FAIL: a file did not parse -- nothing audited for it, which is not a pass.")
        sys.exit(2)
    if declaring == 0:
        print("  NOTHING MEASURED -- no file declared a revision; the detector is suspect. Not a pass.")
        sys.exit(2)
    if n_a + n_b:
        print(f"  FAIL: {n_a + n_b} revision-scope finding(s) in {bad_files} file(s).")
        sys.exit(1)
    print("  PASS. NOTE: this certifies only that a scope decision is recorded and ratings are qualified,")
    print("  not that any rating is right for the revision named.")
    sys.exit(0)
