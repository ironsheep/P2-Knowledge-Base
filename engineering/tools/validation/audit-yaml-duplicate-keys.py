#!/usr/bin/env python3
"""Find duplicate mapping keys in YAML files.

WHY THIS EXISTS (F-360). A duplicate key does not error. `yaml.safe_load` keeps the
LAST one and discards the first silently, so a block's content vanishes at parse time
while every other gate stays green. On 2026-08-25 this destroyed the central corrective
sentence of an entire sprint: `pin-drive-configuration.yaml` had `note:` twice inside
`idioms:`, the second won, and every consumer -- the index generator, the MCP server, an
agent -- read the wrong paragraph. F-360 recorded five sites and noted that "no gate can
see them". This is that gate.

It walks the COMPOSED NODE TREE rather than the loaded object, because by the time you
have a dict the evidence is already gone.

Usage:
    audit-yaml-duplicate-keys.py [path ...]        # files or directories
    audit-yaml-duplicate-keys.py --negative-control

Exit 0 clean, 1 duplicates found, 2 nothing measured.
"""
import sys, os, glob, tempfile
try:
    import yaml
except ImportError:
    print("PyYAML not available", file=sys.stderr); sys.exit(2)


def walk(node, path, out):
    if isinstance(node, yaml.MappingNode):
        seen = {}
        for k, v in node.value:
            key = getattr(k, 'value', None)
            if key in seen:
                out.append((path or '<root>', key, seen[key], k.start_mark.line + 1))
            seen[key] = k.start_mark.line + 1
            walk(v, f"{path}.{key}" if path else str(key), out)
    elif isinstance(node, yaml.SequenceNode):
        for i, v in enumerate(node.value):
            walk(v, f"{path}[{i}]", out)


def scan(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += glob.glob(os.path.join(p, '**', '*.yaml'), recursive=True)
        elif p.endswith('.yaml'):
            files.append(p)
    files = sorted(set(files))
    bad = 0
    for f in files:
        out = []
        try:
            walk(yaml.compose(open(f, encoding='utf-8')), '', out)
        except Exception as e:
            print(f"  PARSE-FAIL {f}: {e}")
            bad += 1
            continue
        if out:
            bad += 1
            for p, k, l1, l2 in out:
                print(f"  DUPLICATE  {f}\n             key '{k}' under {p} at lines {l1} and {l2}"
                      f" -- the line {l2} value WINS and the line {l1} value is discarded")
    return files, bad


def negative_control():
    """A gate that cannot fail has not been verified, it has been RUN."""
    cases = [
        ("a duplicate at the ROOT -- MUST FAIL", "a: 1\nb: 2\na: 3\n", 1),
        ("a duplicate NESTED in a mapping -- MUST FAIL", "top:\n  x: 1\n  y: 2\n  x: 3\n", 1),
        ("a duplicate inside a LIST ITEM -- MUST FAIL", "items:\n  - k: 1\n    j: 2\n    k: 3\n", 1),
        ("no duplicates -- MUST BE CLEAN", "a: 1\nb:\n  c: 2\n  d: 3\n", 0),
        ("same key at DIFFERENT depths is legal -- MUST BE CLEAN", "a: 1\nb:\n  a: 2\n", 0),
    ]
    ok = True
    for label, body, want in cases:
        d = tempfile.mkdtemp()
        p = os.path.join(d, "t.yaml")
        open(p, 'w').write(body)
        out = []
        walk(yaml.compose(open(p, encoding='utf-8')), '', out)
        got = 1 if out else 0
        status = "PASS" if got == want else "**FAIL**"
        if got != want:
            ok = False
        print(f"  [{status}] {label}: got {'duplicates' if got else 'clean'}")
    print()
    print("Negative control PASSED -- the gate fires on a root, nested and in-list duplicate,"
          if ok else "Negative control FAILED.")
    if ok:
        print("and does NOT fire on clean input or on the same key legitimately reused at a")
        print("different depth.")
    return 0 if ok else 1


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--negative-control']
    if '--negative-control' in sys.argv[1:]:
        sys.exit(negative_control())
    if not args:
        args = ['deliverables/ai/P2']
    files, bad = scan(args)
    if not files:
        print("NOTHING MEASURED -- no .yaml files found under the given path(s). This is not a pass.")
        sys.exit(2)
    print(f"\n  files scanned: {len(files)}   files with duplicate keys: {bad}")
    if bad == 0:
        print("  CLEAN. NOTE: this finds DUPLICATE KEYS only. A file can be free of them and")
        print("  still be wrong in every other way -- never read this as a correctness result.")
    sys.exit(1 if bad else 0)
