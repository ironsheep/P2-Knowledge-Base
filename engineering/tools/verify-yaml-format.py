#!/usr/bin/env python3
"""
verify-yaml-format.py — YAML parse verification for the P2 Knowledge Base.

Two modes:
  Tree-wide (default):
      python verify-yaml-format.py
      Parses every .yaml under deliverables/ai/P2/ and reports any that fail.
      Useful as a pre-release sanity check to catch latent broken YAML.

  Targeted (--files):
      python verify-yaml-format.py --files <path1> <path2> ...
      Parses only the listed files. Useful as the Step 2.5 per-edit verify
      called by yaml-knowledge-base-maintenance immediately after edits,
      before running cross-ref validation or index regeneration.

Exit codes:
  0 — all parsed files are well-formed
  1 — one or more files failed to parse
  2 — usage error (e.g., a listed file does not exist)

Output:
  Reports per-file errors (path + parser message) and a final summary
  (clean count / failed count).
"""

import argparse
import sys
from pathlib import Path
import yaml


KB_ROOT = Path(__file__).resolve().parents[2] / "deliverables" / "ai" / "P2"


def collect_yaml_files(roots):
    """Return sorted list of all .yaml files under the given roots."""
    files = []
    for root in roots:
        root = Path(root)
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(sorted(root.rglob("*.yaml")))
        else:
            print(f"ERROR: not a file or directory: {root}", file=sys.stderr)
            sys.exit(2)
    return files


def verify_file(path):
    """Return (ok, error_message). error_message is None on success."""
    try:
        with open(path, "r") as f:
            yaml.safe_load(f)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)
    except Exception as e:
        return False, f"unexpected error: {e}"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--files",
        nargs="+",
        help="Specific files to verify (default: scan all YAML under deliverables/ai/P2/)",
    )
    args = parser.parse_args()

    if args.files:
        files = collect_yaml_files(args.files)
        mode = f"targeted ({len(files)} file(s))"
    else:
        files = collect_yaml_files([KB_ROOT])
        mode = f"tree-wide ({KB_ROOT.relative_to(Path.cwd()) if KB_ROOT.is_relative_to(Path.cwd()) else KB_ROOT})"

    print(f"Verifying YAML format — {mode}")

    failures = []
    for path in files:
        ok, err = verify_file(path)
        if not ok:
            failures.append((path, err))

    clean_count = len(files) - len(failures)

    print()
    print("=" * 60)
    print(f"  Files scanned: {len(files)}")
    print(f"  Parsed clean:  {clean_count}")
    print(f"  Parse failed:  {len(failures)}")
    print("=" * 60)

    if failures:
        print()
        print("FAILURES:")
        for path, err in failures:
            print(f"  {path}")
            # Indent the multi-line error for readability
            for line in err.split("\n"):
                print(f"      {line}")
        sys.exit(1)

    print()
    print("All YAML files parsed cleanly.")
    sys.exit(0)


if __name__ == "__main__":
    main()
