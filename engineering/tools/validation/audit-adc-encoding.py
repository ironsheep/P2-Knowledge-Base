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

    is identical across the ingestion donor, the three published ADC YAMLs,
    and the Silicon Doc ground-truth string. Authority: Silicon Doc v35
    `engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt:816,820-821`
    ("WXPIN sets the mode to X[5:4] ..."), confirmed identical in Spin2 v55.
    Run it pre-publish (release-yamls candidate) and after any ADC-YAML edit.

WHAT IT CHECKS
    1. The Silicon Doc still binds %00..%11 to SINC2-sampling / SINC2-filtering
       / SINC3-filtering / Bitstream, in that order (grounds the truth here).
    2. Every `%NN = <mode>` / `%NN[_xxxx] - <mode>` documentation binding found
       anywhere in each target YAML classifies to the EXPECTED mode (an inverted
       or "reserved" binding fails). WXPIN operands like `%00_0111` and prose
       parentheticals like `(%11)` are not bindings and are ignored.
    3. The donor + the two siblings that carry an explicit map (11000, 11001)
       each define the COMPLETE {%00,%01,%10,%11} set (a deleted row fails).
       Mode %11010 defers its X-config to 11000/11001 and is map-exempt.

USAGE
    audit-adc-encoding.py [--quiet]
    (no file args - the donor / published / silicon paths are fixed)

EXIT STATUS
    0  all bindings match the silicon-grounded truth; maps complete
    1  a binding drifted/inverted, a row is missing, or silicon truth changed
    2  a target file is missing or malformed (no false pass)

FIX
    Correct the offending `%NN` binding to the silicon map above. The donor is
    `engineering/ingestion/smart-pins-catalog/ingestionSources/mode-11000-adc-internal-clock/smart-pin-11000-adc-internal-clock-concise.yaml`;
    the published files are under `deliverables/ai/P2/architecture/smart-pins/`.
    See corrections-register finding F-170 for the full root-cause narrative.
"""

import argparse
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("error: PyYAML is required (pip install --user pyyaml)", file=sys.stderr)
    sys.exit(2)

# Repo root = three levels up from engineering/tools/validation/
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

DONOR = os.path.join(
    REPO_ROOT,
    "engineering/ingestion/smart-pins-catalog/ingestionSources/"
    "mode-11000-adc-internal-clock/smart-pin-11000-adc-internal-clock-concise.yaml",
)
PUBLISHED = {
    "11000": os.path.join(REPO_ROOT, "deliverables/ai/P2/architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml"),
    "11001": os.path.join(REPO_ROOT, "deliverables/ai/P2/architecture/smart-pins/smart-pin-11001-adc-external-clock.yaml"),
    "11010": os.path.join(REPO_ROOT, "deliverables/ai/P2/architecture/smart-pins/smart-pin-11010-adc-scope-trigger.yaml"),
}
SILICON = os.path.join(REPO_ROOT, "engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt")

# Files that must carry the COMPLETE four-row map. 11010 defers to its siblings.
MAP_BEARING = {"donor", "11000", "11001"}

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


def walk_strings(node):
    """Yield every string scalar in a parsed-YAML structure."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from walk_strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk_strings(v)


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
    for s in walk_strings(data):
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


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Guard the ADC X[5:4] sub-mode encoding across donor, "
        "published YAMLs, and the Silicon Doc (F-170).")
    ap.add_argument("--quiet", action="store_true",
                    help="print only problems and the summary")
    args = ap.parse_args(argv)

    problems = []

    # 1. Ground the EXPECTED map in the Silicon Doc.
    silicon_truth(SILICON, problems)

    # 2 + 3. Check each target file's bindings and map completeness.
    targets = [("donor", DONOR)] + [(k, v) for k, v in PUBLISHED.items()]
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
        print("\nPASS: ADC X[5:4] encoding consistent across donor, published "
              "YAMLs, and the Silicon Doc ground truth.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
