#!/usr/bin/env python3
"""
audit-adc-encoding.py - guard the P2 ADC X[5:4] sub-mode encoding against drift.

WHY THIS EXISTS
    The smart-pin ADC X[5:4] sub-mode map was WRONG for 6.5 months (F-170)
    because it was on no verification checklist. The defect was fixed
    downstream-only (the published deliverables YAML, v1.9.0) while the
    upstream ingestion DONOR kept the inverted misconception
    (%00 = "raw bitstream", %11 = "reserved") and threatened to re-seed the
    bug on any "regenerate from catalog". This gate asserts the four-row map

        X[5:4]  %00 = SINC2 Sampling
                %01 = SINC2 Filtering
                %10 = SINC3 Filtering
                %11 = Bitstream capturing

    is identical across the three published ADC YAMLs and the Silicon Doc
    ground-truth string. Authority: Silicon Doc v35
    `engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt:816,820-821`
    ("WXPIN sets the mode to X[5:4] ..."), confirmed identical in Spin2 v55.
    Run it pre-publish (wired into validate-dod-release.py) and after any
    ADC-YAML edit.

THE DONOR LIMB IS RETIRED (2026-09-21, «#346»)
    This gate originally asserted donor == published == silicon, where the
    donor was the smart-pins-catalog concise YAML. That limb read a file that
    does not exist and cannot be made to exist for a release gate:

      - `/engineering/ingestion/smart-pins-catalog` is GITIGNORED
        (`.gitignore:243`), so the donor is absent from every fresh clone. A
        release gate reading it exits 2 everywhere but one container - which
        is how this gate came to be the repo's only UNWIRED gate.
      - The catalog is formally SUPERSEDED (2026-06-12,
        `SUPERSEDED-BY-rev5-ingestion.md`) by
        `engineering/ingestion/sources/smart-pins-titus/`.
      - The re-seed path the limb guarded is gone. The only catalog->KB
        script, `deploy-to-knowledge-base.sh`, writes to a hardcoded
        `/Users/stephen/...` absolute path and targets
        `engineering/knowledge-base/` (the transient tree), never
        `deliverables/ai/P2/`. This project also has no YAML generators -
        content YAMLs are edited in place - so nothing regenerates the
        published trio from any catalog.

    Deliberately NOT repointed at the rev-5 Titus extraction. Titus is an
    upstream lead, never a peer authority, and that same source is recorded as
    carrying WRPIN `x101`/`x111` SWAPPED versus the Silicon Doc. Asserting
    titus == published would make a Titus erratum surface as a published-KB
    failure and send the reader to fix the wrong tier. A Titus/silicon
    disagreement belongs in `SOURCE-ERRATA.md`.

    What survives is what a shipped artifact can still get wrong: the published
    trio drifting from silicon, or a map row going missing. F-170's downstream
    half is exactly that shape.

WHAT IT CHECKS
    1. The Silicon Doc still binds %00..%11 to SINC2-sampling / SINC2-filtering
       / SINC3-filtering / Bitstream, in that order (grounds the truth here).
    2. Every `%NN = <mode>` / `%NN[_xxxx] - <mode>` documentation binding IN
       X[5:4] SCOPE in each target YAML classifies to the EXPECTED mode (an
       inverted or "reserved" binding fails). Scope is the nearest `bits_5_4`
       key or a scalar naming `X[5:4]` - because the same `%NN` notation also
       describes OTHER bit fields (mode 11010's X[1:0] filter select reads
       "%00=68-tap Tukey"), and those are correct, not drift. WXPIN operands
       like `%00_0111` and prose parentheticals like `(%11)` carry no separator
       and are ignored by the pattern itself.
    3. The two files that carry an explicit map (11000, 11001) each define the
       COMPLETE {%00,%01,%10,%11} set (a deleted row fails). Mode %11010 defers
       its X-config to 11000/11001 and is map-exempt.

USAGE
    audit-adc-encoding.py [--quiet] [--negative-control]
    (no file args - the published / silicon paths are fixed)

EXIT STATUS
    0  all bindings match the silicon-grounded truth; maps complete
    1  a binding drifted/inverted, a row is missing, or silicon truth changed
    2  a target file is missing or malformed (no false pass)

FIX
    Correct the offending `%NN` binding to the silicon map above. The published
    files are under `deliverables/ai/P2/architecture/smart-pins/`. See
    corrections-register finding F-170 for the full root-cause narrative.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:
    print("error: PyYAML is required (pip install --user pyyaml)", file=sys.stderr)
    sys.exit(2)

# Repo root = three levels up from engineering/tools/validation/
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

PUBLISHED = {
    "11000": os.path.join(REPO_ROOT, "deliverables/ai/P2/architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml"),
    "11001": os.path.join(REPO_ROOT, "deliverables/ai/P2/architecture/smart-pins/smart-pin-11001-adc-external-clock.yaml"),
    "11010": os.path.join(REPO_ROOT, "deliverables/ai/P2/architecture/smart-pins/smart-pin-11010-adc-scope-trigger.yaml"),
}
SILICON = os.path.join(REPO_ROOT, "engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt")

# Files that must carry the COMPLETE four-row map. 11010 defers to its siblings.
MAP_BEARING = {"11000", "11001"}

# The canonical mode each X[5:4] value must bind to.
EXPECTED = {
    "00": "SINC2_SAMPLING",
    "01": "SINC2_FILTERING",
    "10": "SINC3_FILTERING",
    "11": "BITSTREAM",
}

# A documentation binding: a %NN value, an optional _xxxx period placeholder,
# then a '=' or '-' separator, then the mode phrase. The mandatory separator
# excludes WXPIN operands (%00_0111, with a 4-bit period and no separator) and
# prose parentheticals ((%11) provides ...).
BINDING_RE = re.compile(r"%(00|01|10|11)(?:_xxxx)?\s*[-=]\s*(.+)")


def classify(phrase):
    """Map a mode phrase to a canonical mode, or None if unclassifiable."""
    p = phrase.lower()
    if "sinc3" in p:
        return "SINC3_FILTERING"
    if "sinc2" in p and "sampl" in p:
        return "SINC2_SAMPLING"
    if "sinc2" in p and "filter" in p:
        return "SINC2_FILTERING"
    if "bitstream" in p or "bit stream" in p or "capturing" in p or ("raw" in p and "captur" in p):
        return "BITSTREAM"
    return None  # e.g. "(Reserved/unused)" - an inversion artifact


def walk_strings(node, key=None):
    """Yield (key, scalar) for every string in a parsed-YAML structure.

    `key` is the nearest enclosing mapping key, which is what tells an X[5:4]
    map from some other bit-field's map - see is_x54_scope().
    """
    if isinstance(node, str):
        yield key, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, k if isinstance(k, str) else key)
    elif isinstance(node, list):
        for v in node:
            yield from walk_strings(v, key)


# A %NN binding belongs to X[5:4] only when its scope says so. Two forms, both
# observed in the shipped trio: the map lives under a `bits_5_4` key (11001), or
# the scalar itself names the field (11000's prose). Anything else is a
# DIFFERENT bit field that happens to use the same %NN notation - mode 11010's
# X[1:0] filter select reads "%00=68-tap Tukey, %01=45-tap Tukey", which is
# correct and is not an ADC sub-mode.
X54_KEYS = {"bits_5_4", "x_5_4", "bits5_4"}


def is_x54_scope(key, scalar):
    """True when a %NN binding in this scalar is an X[5:4] sub-mode binding."""
    if key in X54_KEYS:
        return True
    return "X[5:4]" in scalar


def collect_bindings(path):
    """Return (bindings, error). bindings = {bits: set(classified_modes)}."""
    if not os.path.isfile(path):
        return None, f"not a file: {path}"
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        return None, f"malformed YAML: {path}\n  {exc}"
    bindings = {}
    for key, s in walk_strings(data):
        if not is_x54_scope(key, s):
            continue
        for line in s.splitlines():
            m = BINDING_RE.search(line)
            if not m:
                continue
            bits, phrase = m.group(1), m.group(2).strip()
            bindings.setdefault(bits, set()).add(classify(phrase))
    return bindings, None


def silicon_truth(path, problems):
    """Confirm the Silicon Doc still binds %00..%11 in the expected order."""
    if not os.path.isfile(path):
        problems.append(f"silicon ground-truth file missing: {path}")
        return
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    # The "Mode ->" row lists the four phrases left-to-right under %00 %01 %10 %11.
    order = ["SINC2 Sampling", "SINC2 Filtering", "SINC3 Filtering", "Bitstream"]
    for line in text.splitlines():
        if "SINC2 Sampling" in line and "Bitstream" in line:
            positions = [line.find(tok) for tok in order]
            if all(pos >= 0 for pos in positions) and positions == sorted(positions):
                return  # ground truth intact, in order
            problems.append(
                "Silicon Doc X[5:4] mode row no longer lists "
                "SINC2 Sampling / SINC2 Filtering / SINC3 Filtering / Bitstream "
                "in %00..%11 order - EXPECTED map may be stale (re-verify F-170)."
            )
            return
    problems.append(
        f"could not locate the X[5:4] mode row in {path} "
        "(expected a line naming SINC2 Sampling .. Bitstream)."
    )


NEGATIVE_CONTROL_CASES = [
    # (name, want_exit, file-key, find, replace, why this mutation exists)
    ("map inverted in a published file", 1, "11001",
     "%00 = SINC2 sampling (complete conversion in hardware)",
     "%00 = Bitstream capturing (raw bits, LSB=oldest)",
     "F-170's own shape: a sub-mode bound to the wrong meaning."),
    ("a map row deleted", 1, "11000",
     "      %10 = SINC3 filtering", "      # row removed by self-test",
     "A silently dropped row leaves the survivors individually correct."),
    ("silicon ground truth moved", 1, "SILICON",
     "SINC2 Sampling         SINC2 Filtering",
     "SINC2 Filtering        SINC2 Sampling",
     "If the truth root moves, EXPECTED is stale and must not pass quietly."),
    ("a DIFFERENT bit field uses %NN  [negative control]", 0, "11010",
     "%00=68-tap Tukey", "%00=Bitstream capturing",
     "X[1:0] filter select is correct code, not drift - scope must exclude it."),
    ("inverted X[5:4] binding in prose, outside bits_5_4", 1, "11010",
     "registers:",
     'notes_scratch: "Sub-mode recap (X[5:4]): %11 = SINC2 sampling"\n\nregisters:',
     "Proves the scope rule narrowed by MEANING, not to whatever passes."),
]


def negative_control():
    """Make every limb fail on purpose against a scratch tree (never the repo).

    *The falsification bar*, `skills-docs/SKILLS-AUTHORING.md`: a probe never
    seen to fail is not a falsifier, and the control is kept beside the check it
    proves. Case 4 is the negative control - the one that would catch this gate
    being narrowed until it passes rather than until it is right.
    """
    rel = {k: os.path.relpath(v, REPO_ROOT) for k, v in PUBLISHED.items()}
    rel["SILICON"] = os.path.relpath(SILICON, REPO_ROOT)
    me = os.path.relpath(os.path.abspath(__file__), REPO_ROOT)
    failures = []
    with tempfile.TemporaryDirectory(prefix="adc-selftest-") as scratch:
        for src in list(rel.values()) + [me]:
            dst = os.path.join(scratch, src)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(os.path.join(REPO_ROOT, src), dst)
        gate = os.path.join(scratch, me)

        def run():
            return subprocess.run([sys.executable, gate, "--quiet"],
                                  capture_output=True, text=True).returncode

        base = run()
        if base != 0:
            print(f"Negative control ERROR: unmutated scratch tree exits {base}, "
                  "not 0 - fix the gate before trusting any mutation below.")
            return 2
        print("control  : unmutated scratch tree exits 0")

        for name, want, key, find, repl, why in NEGATIVE_CONTROL_CASES:
            path = os.path.join(scratch, rel[key])
            original = open(path, encoding="utf-8").read()
            if find not in original:
                failures.append(f"{name}: anchor text not found - mutation never applied")
                continue
            open(path, "w", encoding="utf-8").write(original.replace(find, repl, 1))
            got = run()
            open(path, "w", encoding="utf-8").write(original)
            ok = got == want
            print(f"{'PASS' if ok else 'FAIL'}     : {name} -> exit {got} (want {want})")
            if not ok:
                failures.append(f"{name}: exit {got}, want {want}  [{why}]")

        if run() != 0:
            failures.append("scratch tree not clean after revert - a mutation leaked")

    if failures:
        print("\nNegative control FAILED -- this gate is not a falsifier:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nNegative control PASSED -- every limb was made to fail on purpose, "
          "and the different-bit-field case stayed green.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Guard the ADC X[5:4] sub-mode encoding across the "
        "published YAMLs and the Silicon Doc (F-170).")
    ap.add_argument("--quiet", action="store_true",
                    help="print only problems and the summary")
    ap.add_argument("--negative-control", action="store_true",
                    help="prove the gate can fail: mutate a scratch copy per "
                         "limb and assert each verdict (never touches the repo)")
    args = ap.parse_args(argv)

    if args.negative_control:
        return negative_control()

    problems = []

    # 1. Ground the EXPECTED map in the Silicon Doc.
    silicon_truth(SILICON, problems)

    # 2 + 3. Check each target file's bindings and map completeness.
    targets = [(k, v) for k, v in PUBLISHED.items()]
    for name, path in targets:
        bindings, err = collect_bindings(path)
        if err is not None:
            print(f"error: {err}", file=sys.stderr)
            return 2
        # Every binding present must match the expected mode.
        for bits, modes in sorted(bindings.items()):
            want = EXPECTED[bits]
            for got in sorted(modes, key=lambda x: (x is None, x)):
                if got != want:
                    problems.append(
                        f"{name}: X[5:4] %{bits} binds to "
                        f"{got or 'UNCLASSIFIED'} but must be {want}  ({path})")
        # Map-bearing files must define the complete four-row set.
        if name in MAP_BEARING:
            missing = sorted(set(EXPECTED) - set(bindings))
            if missing:
                problems.append(
                    f"{name}: incomplete X[5:4] map - missing "
                    f"%{', %'.join(missing)}  ({path})")
        elif not args.quiet:
            print(f"{name}: map-exempt (defers X-config to siblings) - "
                  f"{len(bindings)} binding(s) found")

        if name in MAP_BEARING and not args.quiet:
            shown = ", ".join(f"%{b}->{next(iter(m)) or '?'}"
                              for b, m in sorted(bindings.items()))
            print(f"{name}: {shown}")

    if problems:
        print("\nFAIL: ADC X[5:4] encoding guard found drift:")
        for p in problems:
            print(f"  - {p}")
        print("\nThe authoritative map is %00 SINC2 Sampling / %01 SINC2 "
              "Filtering / %10 SINC3 Filtering / %11 Bitstream "
              "(silicon part4-smart-pins.txt:820-821; see F-170).")
        return 1

    if not args.quiet:
        print("\nPASS: ADC X[5:4] encoding consistent across the published "
              "YAMLs and the Silicon Doc ground truth.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
