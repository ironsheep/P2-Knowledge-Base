#!/usr/bin/env python3
"""Does any YAML plain scalar get silently cut short by a same-line ` #` comment?

WHY THIS EXISTS (S-200 / S-183). `- MOV reg, #42` is parsed by YAML as the scalar
`MOV reg,` followed by the COMMENT `#42`. Every other gate reads the parsed value,
which looks fine; the compile gate sees the cut text only where the cut leaves
illegal code. The loss is silent at parse time, so this gate reads the composed
node tree and the source line, not the loaded object.

Rule (exact). `yaml.compose_all(text, SafeLoader)` per file; for every ScalarNode
with `style is None` (plain), take the source line at `end_mark.line`; if
`line[end_mark.column:]` matches `^\\s*#`, the remainder is a comment. FLAG when any of:
  R1  the character after `#` is not a space   (`#42`, `##addr`, `#@label`)
  R2  the scalar is empty                      (a key or `- ` item with nothing before the comment)
  R3  the scalar contains whitespace           (a multi-word value followed by a comment)
ALLOW a comment after a single-token plain scalar with a space after the `#`
(`- language/pasm2/rep.yaml  # note`, `133  # Per datasheet`). Block scalars and
quoted scalars are never plain, so they are not touched.

Usage:
    audit-yaml-plain-scalar-comment.py [path ...]     # files or directories (default deliverables/ai/P2)
    audit-yaml-plain-scalar-comment.py --negative-control

Exit 0 clean, 1 cut scalars found, 2 the tool could not audit (no files / a file
that does not parse / nothing was a comment-after-plain candidate at all).

A green does NOT certify: that every `#` in a served string survived. A QUOTED scalar
that itself lost text, a flow `[a, b #c]` collection, and a plain scalar whose `#` is
preceded by non-whitespace are outside the rule. Nor that the quoting is semantically
right -- only that nothing is cut by a comment.
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

COMMENT_RE = re.compile(r'^\s*#')


def scan_text(text):
    """Return (n_comment_after_plain, [flag dicts]) for one document text.

    Raises on a parse failure -- the caller decides that is a gate failure.
    """
    lines = text.split('\n')
    flags = []
    n_cand = 0
    for root in yaml.compose_all(text, Loader=yaml.SafeLoader):
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                continue
            if isinstance(node, yaml.ScalarNode):
                if node.style is not None:
                    continue
                ln = node.end_mark.line
                if ln >= len(lines):
                    continue
                rest = lines[ln][node.end_mark.column:]
                if not COMMENT_RE.match(rest):
                    continue
                n_cand += 1
                served = node.value
                lost = rest.strip()
                rules = []
                after = lost[1:2]
                if after != ' ' and after != '':
                    rules.append('R1')
                if served == '':
                    rules.append('R2')
                if re.search(r'\s', served):
                    rules.append('R3')
                if rules:
                    flags.append({'line': ln + 1, 'served': served, 'lost': lost,
                                  'rules': rules})
            elif isinstance(node, yaml.MappingNode):
                for k, v in node.value:
                    stack.append(k)
                    stack.append(v)
            elif isinstance(node, yaml.SequenceNode):
                stack.extend(node.value)
    return n_cand, flags


def scan(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += glob.glob(os.path.join(p, '**', '*.yaml'), recursive=True)
        elif p.endswith('.yaml'):
            files.append(p)
    files = sorted(set(files))
    bad_files = 0
    flagged = 0
    parse_fail = 0
    cand = 0
    for f in files:
        try:
            with open(f, encoding='utf-8') as fh:
                text = fh.read()
            n, flags = scan_text(text)
        except Exception as e:  # noqa: BLE001
            print(f"  PARSE-FAIL {f}: {e}")
            parse_fail += 1
            continue
        cand += n
        if flags:
            bad_files += 1
            for fl in flags:
                flagged += 1
                print(f"  CUT-BY-COMMENT {f}:{fl['line']} [{','.join(fl['rules'])}] "
                      f"served {fl['served']!r}, comment swallowed {fl['lost']!r}")
    return files, cand, flagged, bad_files, parse_fail


def negative_control():
    """A gate that cannot fail has not been verified, it has been RUN."""
    fire = [
        ("R1+R3: `- MOV reg, #42  ' x`", "code:\n  - MOV reg, #42  ' x\n"),
        ("R1: `- CALL #target`", "code:\n  - CALL #target\n"),
        ("R2: `key:  # note`", "key:  # note\n"),
        ("R3: `- JMP vector  # Jump to address`", "code:\n  - JMP vector  # Jump to address\n"),
        ("R1: `syntax: CALLD PA|PB,  #label`", "syntax: CALLD PA|PB,  #label\n"),
    ]
    clean = [
        ("single token + spaced comment (path)", "related:\n  - language/pasm2/rep.yaml  # note\n"),
        ("number + spaced comment", "value: 133  # Per datasheet\n"),
        ("double-quoted scalar holding `#`", 'code:\n  - "MOV reg, #42"\n'),
        ("single-quoted scalar holding `#`", "code:\n  - 'MOV r, #1'\n"),
        ("literal block holding `mov a, #1`", "code: |\n  mov a, #1\n"),
        ("`key: a#b` (no whitespace before #, not a comment)", "key: a#b\n"),
        ("file with no comments (positive control)", "a: 1\nb:\n  - x\n  - y\n"),
    ]
    ok = True
    d = tempfile.mkdtemp()
    cases = [(l, b, True) for l, b in fire] + [(l, b, False) for l, b in clean]
    for label, body, must_fire in cases:
        try:
            _, flags = scan_text(body)
        except Exception as e:  # noqa: BLE001
            print(f"  [**FAIL**] {label}: case file did not parse ({e}) -- a gate failure, not a skip")
            ok = False
            continue
        got = bool(flags)
        good = got == must_fire
        ok = ok and good
        print(f"  [{'PASS' if good else '**FAIL**'}] {label}: "
              f"{'FIRED' if got else 'clean'} (want {'FIRE' if must_fire else 'clean'})")
    # one end-to-end case through scan() so the file path is exercised too
    p = os.path.join(d, 'bad.yaml')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write("code:\n  - CALL #target\n")
    _, _, flagged, _, _ = scan([p])
    good = flagged == 1
    ok = ok and good
    print(f"  [{'PASS' if good else '**FAIL**'}] end-to-end scan() of a bad file: {flagged} flagged (want 1)")
    print()
    if ok:
        print("Negative control PASSED -- the gate fires on R1, R2 and R3 cuts and does NOT fire on")
        print("spaced comments after a single token, quoted scalars, block scalars, `a#b`, or comment-free files.")
    else:
        print("Negative control FAILED.")
    return 0 if ok else 1


if __name__ == '__main__':
    argv = sys.argv[1:]
    if '--negative-control' in argv:
        sys.exit(negative_control())
    args = argv or ['deliverables/ai/P2']
    files, cand, flagged, bad_files, parse_fail = scan(args)
    if not files:
        print("NOTHING MEASURED -- no .yaml files found under the given path(s). This is not a pass.")
        sys.exit(2)
    print(f"\n  files scanned: {len(files)}   comment-after-plain scalars seen: {cand}   "
          f"flagged: {flagged} in {bad_files} files   parse failures: {parse_fail}")
    if parse_fail:
        print("  FAIL: a file did not parse -- nothing audited for it, which is not a pass.")
        sys.exit(2)
    if flagged:
        print(f"  FAIL: {flagged} plain scalar(s) in {bad_files} file(s) are cut by a same-line comment.")
        sys.exit(1)
    if cand == 0 and len(files) > 20:
        print("  NOTHING MEASURED -- no comment-after-plain scalar was seen at all; suspicious. Not a pass.")
        sys.exit(2)
    print("  PASS. NOTE: this finds plain scalars cut by a ` #` comment only. A quoted scalar that lost")
    print("  text, a flow collection `[a, b #c]`, or a `#` with no whitespace before it are outside the rule.")
    sys.exit(0)
