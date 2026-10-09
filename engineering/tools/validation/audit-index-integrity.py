#!/usr/bin/env python3
"""Does the P2KB index agree with what is committed, and is its .gz the same bytes?

WHY THIS EXISTS (F-441 / S-384, F-405 / S-385).
  F-441  v1.19.1 shipped an index carrying the PRE-change SHA-256 of two edited files;
         the MCP server refused to serve them. Nothing compared an entry's sha256 with
         the committed blob.
  F-405  the index and its .gz drifted (F-357 recurred), the index was also stale against
         later content commits, and nothing ran the validator.

Three limbs, one script (`--limb sha256|fresh|gz|all`, default all).

  sha256  For every entry in the index `files`, `sha256` must equal the SHA-256 of
          `git show HEAD:<path>` -- the exact bytes generate-p2kb-index.py::get_git_blob_sha256
          hashes. One `git cat-file --batch` for all paths. FAIL on a mismatch, on a path
          absent at HEAD, and on a HEAD-tracked YAML under deliverables/ai/P2 that has no
          entry (the generator skips files named manifest.yaml; so does this).
  fresh   Clone the repo locally (`git clone --local`) into a temp dir, import
          generate-p2kb-index.py, call generate_index(clone) THERE (nothing in the working
          tree is touched) and compare with the index IGNORING `system.generated`. FAIL on any
          difference. Valid only when `git status --porcelain -- deliverables/ai/P2` is
          empty (aliases and categories come from working-tree YAML): a dirty tree without
          --post-commit prints SKIPPED (exit decided by the other limbs); WITH --post-commit a
          dirty tree is exit 2.
  gz      the .gz decompresses to exactly the index's bytes (the dod runner's
          validate_gzip_compression checks the same pair; repeated here so this gate alone
          answers "a stale .gz fails").

Usage:
    audit-index-integrity.py [--limb LIMB] [--post-commit] [--root DIR] [--index REL]
                             [--committed-index]    # read the index from `git show HEAD:` instead of the working tree
    audit-index-integrity.py --negative-control

Exit 0 clean, 1 defects found (release blocks), 2 the tool could not audit.

A green does NOT certify: that the CONTENT of any entry is right; that the published tree
(raw.githubusercontent.com) serves the same bytes (probing the published tree is a separate
act); or that the aliases are findable (see audit-index-findability.py).

Measured wall time of the `fresh` limb on the real tree: see the runner's docstring
(validate_index_integrity in engineering/tools/validate-dod-release.py).
"""
import argparse
import contextlib
import gzip
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

INDEX_REL = "deliverables/ai/p2kb-index.json"
KB_PREFIX = "deliverables/ai/P2"


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / ".git").exists() and (p / "engineering").is_dir():
            return p
    # .backups copies break a path-derived root; fail loudly rather than guess.
    sys.exit("ERROR: could not locate the repository root from this script's path.")


def git(root, *args, input=None, check=True):
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, input=input)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.decode(errors='replace').strip()}")
    return r


def head_blobs(root, paths):
    """{path: sha256-hex or None (absent at HEAD)} via one `git cat-file --batch`."""
    req = "".join(f"HEAD:{p}\n" for p in paths).encode()
    out = git(root, "cat-file", "--batch", input=req).stdout
    res = {}
    pos = 0
    for p in paths:
        nl = out.index(b"\n", pos)
        header = out[pos:nl].decode()
        pos = nl + 1
        if header.endswith(" missing"):
            res[p] = None
            continue
        size = int(header.split()[2])
        res[p] = hashlib.sha256(out[pos:pos + size]).hexdigest()
        pos += size + 1
    return res


def head_yamls(root):
    out = git(root, "ls-tree", "-r", "--name-only", "HEAD", KB_PREFIX).stdout.decode().split("\n")
    return sorted(p for p in out if p.endswith(".yaml") and os.path.basename(p) != "manifest.yaml")


def load_index(root, index_rel, committed):
    if committed:
        raw = git(root, "show", f"HEAD:{index_rel}").stdout
    else:
        raw = (Path(root) / index_rel).read_bytes()
    return json.loads(raw), raw


def limb_sha256(root, idx, say):
    files = idx.get("files") or {}
    if not files:
        say("  sha256: the index has no `files` entries -- nothing audited.")
        return None
    paths = [e["path"] for e in files.values()]
    blobs = head_blobs(root, paths)
    stale, absent = [], []
    for key, e in files.items():
        h = blobs[e["path"]]
        if h is None:
            absent.append((key, e["path"]))
        elif h != e.get("sha256"):
            stale.append((key, e["path"]))
    indexed = set(paths)
    unindexed = [p for p in head_yamls(root) if p not in indexed]
    for key, p in stale:
        say(f"  STALE-SHA256   {p}  (entry {key}: index sha256 is not the HEAD blob's)")
    for key, p in absent:
        say(f"  ABSENT-AT-HEAD {p}  (entry {key}: path is not in HEAD)")
    for p in unindexed:
        say(f"  NO-ENTRY       {p}  (tracked at HEAD, not in the index)")
    say(f"  sha256 limb: {len(files)} entries; stale {len(stale)}; absent at HEAD {len(absent)}; "
        f"tracked YAML with no entry {len(unindexed)}")
    return len(stale) + len(absent) + len(unindexed)


def _load_generator(real_root):
    spec = importlib.util.spec_from_file_location(
        "generate_p2kb_index", str(Path(real_root) / "engineering/tools/generate-p2kb-index.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _strip_generated(idx):
    d = json.loads(json.dumps(idx))
    d.get("system", {}).pop("generated", None)
    return d


def _diff_summary(a, b):
    """Short human summary of how two index dicts differ (index vs fresh)."""
    out = []
    for sect in sorted(set(a) | set(b)):
        if a.get(sect) == b.get(sect):
            continue
        sa, sb = a.get(sect), b.get(sect)
        if isinstance(sa, dict) and isinstance(sb, dict):
            ks = sorted(set(sa) | set(sb))
            diff = [k for k in ks if sa.get(k) != sb.get(k)]
            out.append(f"{sect}: {len(diff)} differing (first: {', '.join(map(str, diff[:5]))})")
        else:
            out.append(f"{sect}: differs")
    return out


def limb_fresh(root, idx, post_commit, say, generator_root):
    st = git(root, "status", "--porcelain", "--", KB_PREFIX).stdout.decode().strip()
    if st:
        if post_commit:
            say("  fresh limb: uncommitted YAML under deliverables/ai/P2 with --post-commit -- cannot audit.")
            for ln in st.split("\n")[:10]:
                say(f"      {ln}")
            return 2
        say("  fresh limb: SKIPPED (uncommitted YAML -- expected before step 6a)")
        return 0
    gen = _load_generator(generator_root)
    tmp = tempfile.mkdtemp(prefix="idx-fresh-")
    clone = os.path.join(tmp, "clone")
    cwd = os.getcwd()
    try:
        r = subprocess.run(["git", "clone", "--quiet", "--local", "--no-hardlinks", str(root), clone],
                           capture_output=True, text=True)
        if r.returncode != 0:
            say(f"  fresh limb: git clone failed: {r.stderr.strip()}")
            return 2
        os.chdir(clone)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                gen.assert_git_usable(Path(clone))
                fresh = gen.generate_index(Path(clone))
        except SystemExit as e:
            say(f"  fresh limb: the generator refused (exit {e.code}):")
            for ln in buf.getvalue().strip().split("\n")[-6:]:
                say(f"      {ln}")
            return 2
        finally:
            os.chdir(cwd)
        a, b = _strip_generated(idx), _strip_generated(fresh)
        if a == b:
            say("  fresh limb: the index equals a fresh regeneration at HEAD (system.generated ignored)")
            return 0
        say("  fresh limb: the index differs from a fresh regeneration at HEAD:")
        for ln in _diff_summary(a, b):
            say(f"      {ln}")
        return 1
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)


def limb_gz(root, index_rel, raw_json, say):
    gz = Path(root) / (index_rel + ".gz")
    if not gz.exists():
        say(f"  gz limb: {gz} does not exist -- cannot audit.")
        return 2
    try:
        data = gzip.decompress(gz.read_bytes())
    except Exception as e:  # noqa: BLE001
        say(f"  gz limb: cannot decompress: {e}")
        return 2
    if data == raw_json:
        say("  gz limb: the .gz decompresses to exactly the index bytes")
        return 0
    say("  STALE-GZ: the .gz does not decompress to the index file's bytes")
    return 1


def run(root, index_rel=INDEX_REL, limb="all", post_commit=False, committed=False,
        say=print, generator_root=None):
    generator_root = generator_root or repo_root()
    try:
        idx, raw = load_index(root, index_rel, committed)
    except Exception as e:  # noqa: BLE001
        say(f"  cannot read the index ({index_rel}): {e} -- nothing audited, not a pass.")
        return 2
    rcs = []
    try:
        if limb in ("sha256", "all"):
            n = limb_sha256(root, idx, say)
            rcs.append(2 if n is None else (1 if n else 0))
        if limb in ("fresh", "all"):
            rcs.append(limb_fresh(root, idx, post_commit, say, generator_root))
        if limb in ("gz", "all"):
            if committed:
                say("  gz limb: not applicable with --committed-index (skipped)")
            else:
                rcs.append(limb_gz(root, index_rel, raw, say))
    except RuntimeError as e:
        say(f"  git failed: {e} -- nothing audited, not a pass.")
        return 2
    if 2 in rcs:
        return 2
    return 1 if 1 in rcs else 0


# ---------------------------------------------------------------- negative control
def _env():
    e = dict(os.environ)
    e.update(GIT_AUTHOR_NAME="nc", GIT_AUTHOR_EMAIL="nc@example.invalid",
             GIT_COMMITTER_NAME="nc", GIT_COMMITTER_EMAIL="nc@example.invalid")
    return e


def _g(root, *args):
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, env=_env())
    if r.returncode != 0:
        raise RuntimeError(f"scratch git {' '.join(args)}: {r.stderr}")


def _write(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _scratch(real_root):
    """A scratch repo with 3 YAMLs, the category file, committed; returns its path."""
    d = tempfile.mkdtemp(prefix="idx-nc-")
    _g(d, "init", "--quiet")
    _write(d, "deliverables/ai/P2/x/a.yaml", "name: A\naliases: [alpha]\n")
    _write(d, "deliverables/ai/P2/x/b.yaml", "name: B\n")
    _write(d, "deliverables/ai/P2/x/c.yaml", "name: C\n")
    src = Path(real_root) / "engineering/tools/p2kb-categories.json"
    if src.exists():
        _write(d, "engineering/tools/p2kb-categories.json", src.read_text())
    _g(d, "add", "-A")
    _g(d, "commit", "--quiet", "-m", "init")
    return d


def _regen(root, real_root):
    """Write deliverables/ai/p2kb-index.json (+ .gz) generated at the scratch HEAD."""
    gen = _load_generator(real_root)
    cwd = os.getcwd()
    os.chdir(root)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            idx = gen.generate_index(Path(root))
    finally:
        os.chdir(cwd)
    raw = json.dumps(idx, indent=2).encode()
    _write(root, INDEX_REL, raw.decode())
    (Path(root) / (INDEX_REL + ".gz")).write_bytes(gzip.compress(raw))
    return idx


def negative_control():
    real = repo_root()
    ok = True
    made = []

    def case(label, want, build, limb="all", post_commit=False, expect_text=None):
        nonlocal ok
        d = _scratch(real)
        made.append(d)
        build(d)
        lines = []
        rc = run(d, INDEX_REL, limb, post_commit, say=lines.append, generator_root=real)
        good = rc == want and (expect_text is None or any(expect_text in ln for ln in lines))
        ok = ok and good
        print(f"  [{'PASS' if good else '**FAIL**'}] {label}: exit {rc} (want {want})"
              + (f"; saw {expect_text!r}" if expect_text and good else ""))
        if not good:
            for ln in lines:
                print("        " + ln)

    def regen(d):
        _regen(d, real)

    def edit_commit_b(d):
        _write(d, "deliverables/ai/P2/x/b.yaml", "name: B\nextra: changed\n")
        _g(d, "commit", "--quiet", "-am", "edit b")

    def flip_digit(d):
        p = Path(d) / INDEX_REL
        idx = json.loads(p.read_text())
        k = next(iter(idx["files"]))
        h = idx["files"][k]["sha256"]
        idx["files"][k]["sha256"] = ("0" if h[0] != "0" else "1") + h[1:]
        p.write_text(json.dumps(idx, indent=2))

    def delete_c(d):
        _g(d, "rm", "--quiet", "deliverables/ai/P2/x/c.yaml")
        _g(d, "commit", "--quiet", "-m", "rm c")

    def add_d(d):
        _write(d, "deliverables/ai/P2/x/d.yaml", "name: D\n")
        _g(d, "add", "-A")
        _g(d, "commit", "--quiet", "-m", "add d")

    def drop_alias(d):
        p = Path(d) / INDEX_REL
        idx = json.loads(p.read_text())
        idx["aliases"].pop("alpha", None)
        idx["aliases"].pop("ALPHA", None)
        p.write_text(json.dumps(idx, indent=2))

    def gen_only_differs(d):
        p = Path(d) / INDEX_REL
        idx = json.loads(p.read_text())
        idx["system"]["generated"] = "1999-01-01T00:00:00"
        raw = json.dumps(idx, indent=2)
        p.write_text(raw)
        (Path(d) / (INDEX_REL + ".gz")).write_bytes(gzip.compress(raw.encode()))  # keep the pair consistent

    def dirty_a(d):
        _write(d, "deliverables/ai/P2/x/a.yaml", "name: A\naliases: [alpha, beta]\n")

    def stale_gz(d):
        (Path(d) / (INDEX_REL + ".gz")).write_bytes(gzip.compress(b'{"stale": true}'))

    print("  -- must FIRE --")
    case("F-441 shape: index regenerated, then b.yaml edited and committed",
         1, lambda d: (regen(d), edit_commit_b(d)), limb="sha256", expect_text="STALE-SHA256")
    case("an entry's sha256 flipped one hex digit",
         1, lambda d: (regen(d), flip_digit(d)), limb="sha256", expect_text="STALE-SHA256")
    case("an entry for a path deleted at HEAD",
         1, lambda d: (regen(d), delete_c(d)), limb="sha256", expect_text="ABSENT-AT-HEAD")
    case("a committed YAML with no entry",
         1, lambda d: (regen(d), add_d(d)), limb="sha256", expect_text="NO-ENTRY")
    case("an index missing an alias a regeneration would add (fresh limb, clean tree)",
         1, lambda d: (regen(d), drop_alias(d)), limb="fresh", expect_text="differs from a fresh regeneration")
    case("a stale .gz",
         1, lambda d: (regen(d), stale_gz(d)), limb="gz", expect_text="STALE-GZ")
    case("--post-commit on a dirty tree is exit 2, not 0",
         2, lambda d: (regen(d), dirty_a(d)), limb="fresh", post_commit=True)
    print("  -- must stay CLEAN --")
    case("index regenerated after the commit (positive control, all limbs)",
         0, regen, limb="all")
    case("system.generated alone differing (all limbs)",
         0, lambda d: (regen(d), gen_only_differs(d)), limb="all")
    case("fresh limb on a dirty tree WITHOUT --post-commit prints SKIPPED, does not fail",
         0, lambda d: (regen(d), dirty_a(d)), limb="fresh", expect_text="SKIPPED")
    for d in made:
        shutil.rmtree(d, ignore_errors=True)
    print()
    if ok:
        print("Negative control PASSED -- sha256 (stale, flipped, absent, unindexed), fresh (alias drift,")
        print("dirty-tree skip and exit 2) and gz (stale) limbs fire; clean regenerations and a")
        print("system.generated-only difference stay green.")
    else:
        print("Negative control FAILED.")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--limb", choices=["sha256", "fresh", "gz", "all"], default="all")
    ap.add_argument("--post-commit", action="store_true")
    ap.add_argument("--root", default=None)
    ap.add_argument("--index", default=INDEX_REL)
    ap.add_argument("--committed-index", action="store_true",
                    help="read the index from `git show HEAD:<index>` instead of the working tree")
    ap.add_argument("--negative-control", action="store_true")
    a = ap.parse_args()
    if a.negative_control:
        sys.exit(negative_control())
    root = Path(a.root).resolve() if a.root else repo_root()
    rc = run(root, a.index, a.limb, a.post_commit, a.committed_index)
    print()
    if rc == 0:
        print("PASS: the index agrees with HEAD "
              f"(limb {a.limb}). NOTE: this does not certify entry content, the published tree, or findability.")
    elif rc == 1:
        print(f"FAIL: the index does not agree with what is committed (limb {a.limb}).")
    else:
        print("ERROR: the tool could not audit. Nothing audited is never a pass.")
    sys.exit(rc)


if __name__ == "__main__":
    main()
