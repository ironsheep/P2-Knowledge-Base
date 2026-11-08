#!/usr/bin/env python3
"""
audit-yaml-certification-record.py — does every changed YAML file have a certification row?

WHY THIS EXISTS
    A YAML file touched for a release is read whole against its sources, and the
    reading is written down as one row in engineering/operations/YAML-CERTIFICATION-RECORD.md.
    This gate fails when a YAML file that differs from the base has no such row.

WHAT IS COMPARED
    The base is the latest KB tag (the highest tag of the form vN.N.N, the same rule
    as audit-kb-pending.py), against the WORKING TREE. So the answer is the same
    before and after the content commit: committed, staged, unstaged and untracked
    new YAML files under deliverables/ai/P2/ all count. --range A..B replaces both
    the tag and the working tree with that explicit range (untracked files are not
    part of a range).

HOW A CHANGE IS CLASSED
    modified / added / type-changed   needs a row
    renamed or copied                 the NEW path needs a row; the old path does not
    deleted                           needs no row
    A file touched only for a related: link is modified like any other and needs a row.

THE RECORD
    Only the table after the "## Record" heading is read. A row is
    | `path` | YYYY-MM-DD | sources read | certified | or | certified with fixes (N) |.
    A VALID row for a file that is not in the diff is harmless. A MALFORMED row, or
    a second row for the same path, fails the audit wherever it is, in the diff or
    out of it: the record promises one valid row per file.

EXIT CODES
    0  pass        1  fail (missing, malformed or duplicate rows)
    2  usage or environment error (no record, no tag, git failed)

    --negative-control   Prove the checks can fail, on synthetic diffs and on a
                         throwaway git repository.
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KB_TREE = "deliverables/ai/P2/"
RECORD = Path("engineering/operations/YAML-CERTIFICATION-RECORD.md")
RECORD_HEADING = "## Record"
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
RESULT = re.compile(r"certified( with fixes \(\d+\))?")
PATH_CELL = re.compile(r"`([^`]+)`")


class GitError(Exception):
    pass


def git(root, *args):
    proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise GitError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout


def repo_root():
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / ".git").exists() and (p / "engineering").is_dir():
            return p
    sys.exit("ERROR: could not locate the repository root from this script's path.")


def latest_tag(root):
    tags = [t for t in git(root, "tag", "--list").split("\n") if re.fullmatch(r"v\d+\.\d+\.\d+", t)]
    return max(tags, key=lambda t: tuple(int(x) for x in t[1:].split("."))) if tags else None


def parse_name_status(tokens):
    """Turn the NUL-separated tokens of `git diff --name-status -z` into (status, path).

    A rename or copy carries two paths; the entry keeps the new one.
    """
    entries, i = [], 0
    while i < len(tokens):
        status = tokens[i]
        if not status:
            i += 1
            continue
        if status[0] in "RC":
            entries.append((status[0], tokens[i + 2]))
            i += 3
        else:
            entries.append((status[0], tokens[i + 1]))
            i += 2
    return entries


def needing_rows(entries):
    """The KB-relative YAML paths in `entries` that need a record row."""
    need = set()
    for status, path in entries:
        if status == "D" or not path.startswith(KB_TREE):
            continue
        if not path.endswith((".yaml", ".yml")):
            continue
        need.add(path[len(KB_TREE):])
    return need


def changed_files(root, base, explicit_range):
    """Entries for every YAML-tree change against `base`, or over `explicit_range`."""
    if explicit_range:
        out = git(root, "diff", "--name-status", "-M", "-z", explicit_range, "--", KB_TREE)
        return parse_name_status(out.split("\0"))
    out = git(root, "diff", "--name-status", "-M", "-z", base, "--", KB_TREE)
    entries = parse_name_status(out.split("\0"))
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z", "--", KB_TREE)
    entries += [("A", p) for p in untracked.split("\0") if p]
    return entries


def path_problem(path):
    if path.startswith("/") or path.startswith("deliverables/") or ".." in path.split("/"):
        return "path is not relative to deliverables/ai/P2/"
    if not path.endswith((".yaml", ".yml")):
        return "path is not a YAML file"
    return None


def parse_record(text):
    """Read the record table. Returns (rows, problems).

    rows maps each valid path to the list of line numbers carrying it;
    problems is a list of (line number, reason) for malformed rows.
    """
    rows, problems = {}, []
    in_record = False
    for n, line in enumerate(text.split("\n"), 1):
        if not in_record:
            in_record = line.strip() == RECORD_HEADING
            continue
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and (cells[0] == "file" or re.fullmatch(r"[-: ]+", cells[0])):
            continue
        if len(cells) != 4:
            problems.append((n, f"{len(cells)} cells, expected 4"))
            continue
        m = PATH_CELL.fullmatch(cells[0])
        if not m:
            problems.append((n, "file is not a backticked path"))
            continue
        why = path_problem(m.group(1))
        if why:
            problems.append((n, why))
            continue
        if not DATE.fullmatch(cells[1]):
            problems.append((n, "date is not YYYY-MM-DD"))
            continue
        if not cells[2]:
            problems.append((n, "sources read is empty"))
            continue
        if not RESULT.fullmatch(cells[3]):
            problems.append((n, "result is not 'certified' or 'certified with fixes (N)'"))
            continue
        rows.setdefault(m.group(1), []).append(n)
    return rows, problems


def judge(need, rows, problems):
    """Returns (missing, bad, duplicates): sorted paths, problem list, {path: lines}."""
    missing = sorted(p for p in need if p not in rows)
    duplicates = {p: ls for p, ls in sorted(rows.items()) if len(ls) > 1}
    return missing, list(problems), duplicates


def report(need, rows, problems):
    missing, bad, duplicates = judge(need, rows, problems)
    for p in missing:
        print(f"  MISSING ROW: {p}")
    for n, why in bad:
        print(f"  BAD ROW line {n}: {why}")
    for p, ls in duplicates.items():
        print(f"  DUPLICATE ROW: {p} (lines {', '.join(map(str, ls))})")
    return missing, bad, duplicates


def row(path, date="2026-01-01", sources="Silicon Doc p1", result="certified"):
    return f"| `{path}` | {date} | {sources} | {result} |"


def record_text(*row_lines):
    head = ("intro\n\n| the table above the record is never read |\n|---|\n| `ignored.yaml` |\n\n"
            f"{RECORD_HEADING}\n\n| file | date | sources read | result |\n|---|---|---|---|\n")
    return head + "".join(r + "\n" for r in row_lines)


def verdict(entries, text):
    need = needing_rows(entries)
    rows, problems = parse_record(text)
    missing, bad, duplicates = judge(need, rows, problems)
    return set(missing), bool(missing or bad or duplicates)


def real_git_cases():
    """Build a throwaway repository and let git itself classify the changes."""
    ident = ["-c", "user.name=control", "-c", "user.email=control@example.invalid",
             "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false"]
    tmp = Path(tempfile.mkdtemp(prefix="yaml-cert-control-"))
    try:
        kb = tmp / KB_TREE
        kb.mkdir(parents=True)
        git(tmp, "init", "-q")
        for name in ("a", "b", "c"):
            (kb / f"{name}.yaml").write_text(
                f"name: {name}\nrelated:\n  - x/y.yaml\nbody: |\n  line one\n  line two\n  line three\n",
                encoding="utf-8")
        git(tmp, "add", "-A")
        git(tmp, *ident, "commit", "-q", "-m", "base")
        git(tmp, "tag", "v9.9.9")
        (kb / "a.yaml").write_text(
            "name: a\nrelated:\n  - x/y.yaml\n  - x/z.yaml\nbody: |\n  line one\n  line two\n  line three\n",
            encoding="utf-8")
        git(tmp, "mv", KB_TREE + "b.yaml", KB_TREE + "b2.yaml")
        (kb / "c.yaml").unlink()
        (kb / "d.yaml").write_text("name: d\n", encoding="utf-8")
        (tmp / "outside.yaml").write_text("name: outside\n", encoding="utf-8")

        entries = changed_files(tmp, latest_tag(tmp), None)
        wanted = {"a.yaml", "b2.yaml", "d.yaml"}
        got = needing_rows(entries)
        no_rows = verdict(entries, record_text())
        with_rows = verdict(entries, record_text(row("a.yaml"), row("b2.yaml"), row("d.yaml")))
        return [
            ("real git: related-only edit, staged rename, deletion and untracked file need exactly a, b2, d",
             got == wanted),
            ("real git: no rows fails naming exactly a, b2 and d",
             no_rows == (wanted, True)),
            ("real git: rows for a, b2 and d pass", with_rows == (set(), False)),
        ]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def negative_control():
    base = KB_TREE
    def m(p): return ("M", base + p)
    cases = [
        # (label, diff entries, record text, should_fail, files that must be named missing)
        ("one uncertified file", [m("a/b.yaml")], record_text(), True, {"a/b.yaml"}),
        ("related-link-only change has no row", [m("x/y.yaml")], record_text(row("other.yaml")),
         True, {"x/y.yaml"}),
        ("rename counts as a new path", [("R", base + "new.yaml")], record_text(row("old.yaml")),
         True, {"new.yaml"}),
        ("untracked new file", [("A", base + "n.yaml")], record_text(), True, {"n.yaml"}),
        ("one of two uncertified", [m("a.yaml"), m("b.yaml")], record_text(row("a.yaml")),
         True, {"b.yaml"}),
        ("duplicate row", [], record_text(row("a.yaml"), row("a.yaml", date="2026-02-02")),
         True, set()),
        ("malformed row: bad date", [], record_text(row("a.yaml", date="Nov 8")), True, set()),
        ("malformed row: path not backticked", [], record_text("| a.yaml | 2026-01-01 | src | certified |"),
         True, set()),
        ("malformed row: bad result", [], record_text(row("a.yaml", result="ok")), True, set()),
        ("a malformed row does not certify its file", [m("a.yaml")],
         record_text(row("a.yaml", date="soon")), True, {"a.yaml"}),
        ("a near-name row does not certify", [m("a/b.yaml")], record_text(row("a/bb.yaml")),
         True, {"a/b.yaml"}),
        ("every changed file has a row", [m("a.yaml"), m("b.yaml"), ("A", base + "c.yaml")],
         record_text(row("a.yaml"), row("b.yaml"), row("c.yaml", result="certified with fixes (2)")),
         False, set()),
        ("deleted file with no row", [("D", base + "gone.yaml")], record_text(), False, set()),
        ("extra row for an unchanged file", [], record_text(row("quiet.yaml")), False, set()),
        ("re-certified file has one row", [m("a.yaml")], record_text(row("a.yaml", date="2026-03-03")),
         False, set()),
        ("renamed file with a row only for the new path", [("R", base + "new.yaml")],
         record_text(row("new.yaml")), False, set()),
        ("change outside YAML is ignored", [m("notes.md")], record_text(), False, set()),
        ("zero-fix count is a valid result", [m("a.yaml")],
         record_text(row("a.yaml", result="certified with fixes (0)")), False, set()),
    ]
    wrong = []
    for label, entries, text, should_fail, named in cases:
        missing, failed = verdict(entries, text)
        if failed != should_fail or missing != named:
            wrong.append(label)
    parsed = parse_name_status(["R100", "old.yaml", "new.yaml", "D", "gone.yaml", "M", "m.yaml", ""])
    if parsed != [("R", "new.yaml"), ("D", "gone.yaml"), ("M", "m.yaml")]:
        wrong.append("name-status parse")
    try:
        for label, ok in real_git_cases():
            if not ok:
                wrong.append(label)
    except (GitError, OSError) as e:
        print(f"ERROR: could not build the throwaway repository: {e}")
        return 2
    if wrong:
        print(f"FAIL: negative control wrong on: {'; '.join(wrong)}")
        return 1
    print("Negative control: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--range", dest="range", metavar="A..B",
                    help="diff this explicit range instead of the latest tag against the working tree")
    ap.add_argument("--negative-control", action="store_true")
    args = ap.parse_args()

    if args.negative_control:
        return negative_control()

    root = repo_root()
    record = root / RECORD
    if not record.exists():
        print(f"ERROR: record not found: {record}")
        return 2
    try:
        base = None
        if args.range:
            print(f"Base: {args.range}")
        else:
            base = latest_tag(root)
            if not base:
                print("ERROR: no KB tag of the form vN.N.N")
                return 2
            print(f"Base: {base} (working tree)")
        entries = changed_files(root, base, args.range)
    except GitError as e:
        print(f"ERROR: {e}")
        return 2

    need = needing_rows(entries)
    print(f"Changed YAML files needing a row: {len(need)}")
    rows, problems = parse_record(record.read_text(encoding="utf-8"))
    missing, bad, duplicates = report(need, rows, problems)
    if missing or bad or duplicates:
        print(f"FAIL: {len(missing)} of {len(need)} changed YAML file(s) lack a certification row; "
              f"{len(bad)} malformed row(s); {len(duplicates)} duplicated path(s)")
        return 1
    if need:
        print(f"PASS: {len(need)} changed YAML file(s), all with a record row")
    else:
        print("PASS: no changed YAML files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
