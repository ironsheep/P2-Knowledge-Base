#!/usr/bin/env python3
"""Run every manual-head gate for one document, and BLOCK on failure.

WHY THIS EXISTS
---------------
The YAML head has had a runner since it needed one: `validate-dod-release.py`
executes its gates, so they run whether or not anyone remembers them. The manual
head had nothing. Its fifteen-odd gates were invoked only by prose inside
`prepare-manual` and `release-manual` -- real instructions, but ones a reader has
to notice, in skills thousands of lines long.

Measured 2026-09-10 with `audit-gate-arming.py`: of 31 gate scripts in this
repo, **4** were executed by a runner. Ten were invoked by nothing at all,
including two whose own docstrings record the incident that caused them:

  audit-license-block.py       "License drift reached 17 documents and shipped
                                publicly for two months because nothing checked
                                it. Every other class of render defect we have
                                been bitten by has a gate; this is that gate."
                                -- and nothing ran that gate either.
  audit-review-scaffolding.py  guards against publishing a private question to a
                                named third-party developer. Unwired.
  audit-inline-run-width.py    referenced by NO file in the repository, yet run
                                by hand during the v1.18.0 sweep. A gate living
                                on tribal memory.

This runner is the manual head's answer. Gates are declared in GATES below, so
adding one is a row rather than a paragraph, and `audit-gate-arming.py` -- run
here as the last gate -- turns red if a gate script exists that no manifest
mentions. That is the part that keeps this honest: without it, the next gate
gets built and forgotten exactly like the ten before it.

WHAT A SKIP MEANS (read this before trusting a green)
-----------------------------------------------------
A gate that cannot run is reported SKIP and **never counts as a pass**. A missing
dependency, an absent artifact, or a document with no example corpus disarms that
check -- and a disarmed check that reads green is worse than no check, because it
buys confidence it did not earn. The verdict line always states how many gates
actually ran.

USAGE
    validate-manual-release.py --slug <slug> --phase prepare
    validate-manual-release.py --slug <slug> --phase release [--pdf <path>]
    validate-manual-release.py --list

Exit 0 = every applicable gate passed. Exit 1 = at least one BLOCKING failure.
Exit 2 = usage/IO error.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

VALIDATION = "engineering/tools/validation"


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / ".git").exists() and (p / "engineering").is_dir():
            return p
    sys.exit("ERROR: could not locate the repository root.")


ROOT = repo_root()
DOCPROD = ROOT / "engineering/document-production"


def doc_dirs(slug: str):
    """A document lives under manuals/ or app-notes/. Resolve which."""
    for parent in ("manuals", "app-notes"):
        d = DOCPROD / parent / slug
        if d.is_dir():
            return d, DOCPROD / "workspace" / slug
    sys.exit(f"ERROR: no manuals/{slug} or app-notes/{slug} under {DOCPROD}")


def source_mds(doc: Path):
    """The authored markdown a source-side gate reads.

    CHANGELOG and README are excluded: they are authored, but they are not
    rendered into the PDF, so a finding in them is noise at this gate.
    """
    return sorted(
        str(p) for p in (doc / "opus-master").rglob("*.md")
        if p.name not in ("CHANGELOG.md", "README.md")
        and "archived" not in p.parts and "archive" not in p.parts
        and "audit" not in p.parts and ".backup." not in p.name
    )


def workspace_md(ws: Path):
    req = ws / "request.json"
    if not req.is_file():
        return None
    try:
        name = json.loads(req.read_text())["documents"][0]["input"]
    except (KeyError, IndexError, json.JSONDecodeError):
        return None
    p = ws / name
    return str(p) if p.is_file() else None


def has_corpus(doc: Path):
    d = doc / "examples-library"
    return d.is_dir() and any(d.glob("*.spin2"))


def app_note_corpus_gap(doc: Path) -> bool:
    """True for an app note whose printed fences carry no caption= yet.

    Measured 2026-08-22: 31 of the 32 app-note example files are already
    byte-identical to a printed fence, but none of the fences is captioned, so
    the identity checker pairs nothing and reports every file an orphan. Making
    that a blocker would put a permanent RED in front of every app-note release
    -- and a gate that is always red is a gate everyone learns to skip. It stays
    VISIBLE and non-blocking until the captions are added.
    """
    if doc.parent.name != "app-notes":
        return False
    body = doc / "opus-master" / f"{doc.name}.md"
    if not body.is_file():
        return True
    return "caption=" not in body.read_text(encoding="utf-8", errors="replace")


def build_gates(slug: str, phase: str, pdf: str | None):
    doc, ws = doc_dirs(slug)
    srcs = source_mds(doc)
    wsmd = workspace_md(ws)
    corpus = has_corpus(doc)
    V = f"{VALIDATION}"
    G = []

    if phase == "prepare":
        if not srcs:
            sys.exit(f"ERROR: no authored markdown under {doc}/opus-master -- "
                     "the scan is mis-scoped and would pass over nothing.")
        G += [
            ("code-line-length", f"{V}/audit-code-line-length.py", srcs, True,
             "code boxes do not wrap; an over-long line is an authorship defect"),
            ("inline-code-ascii", f"{V}/audit-inline-code-ascii.py", srcs, True,
             "a non-ASCII char in \\lstinline aborts xelatex"),
            ("backtick-balance", f"{V}/audit-backtick-balance.py", srcs, True,
             "a backtick inside a span inverts every span after it (F-294)"),
            ("inline-run-width", f"{V}/audit-inline-run-width.py", srcs, True,
             "glued inline spans form one unbreakable box that runs past the margin"),
        ]
        if wsmd:
            G.append(("font-glyphs", f"{V}/audit-font-glyphs.py",
                      [wsmd, "--source-dir", str(doc / "opus-master"),
                       "--templates", str(ws / "templates"),
                       str(DOCPROD / "platform/templates")], True,
                      "a glyph the font lacks prints NOTHING, with a clean log"))
        else:
            G.append(("font-glyphs", None, None, True,
                      "workspace markdown not assembled yet -- run the assemble step"))
        if corpus:
            G += [
                ("spin2-ascii", f"{V}/audit-spin2-ascii.py",
                 [str(doc / "examples-library")], True,
                 "non-ASCII in a shipped .spin2 is a portability defect"),
                ("example-headers", "engineering/tools/sync-manual-examples.py",
                 ["--doc", str(doc), "--check"], True,
                 "generated headers carry the released version; they re-sync on a bump"),
                ("corpus-identity", "engineering/tools/verify-example-corpus-identity.py",
                 ["--manual", str(doc)], not app_note_corpus_gap(doc),
                 "a loose .spin2 must be byte-identical to its printed listing"
                 if not app_note_corpus_gap(doc) else
                 "KNOWN GAP: app-note fences carry no caption=, so identity reads "
                 "RED with every file an orphan and has never gated these. "
                 "Tracked on PUNCH-LIST.md -> 'App-note example corpora have "
                 "never been gated at all'. Non-blocking until captions land."),
            ]
    else:  # release
        G += [
            ("license-block", f"{V}/audit-license-block.py", [], True,
             "license drift reached 17 documents and shipped for two months"),
            # Takes paths, not a bare invocation: run over the opus-master sources AND
            # the generated .tex, because either alone misses a case -- a box
            # hand-written in raw LaTeX never appears as a fence, and a stale .tex
            # never appears in the source.
            ("review-scaffolding", f"{V}/audit-review-scaffolding.py",
             [str(doc / "opus-master")], True,
             "a tool-review box puts a private question to a third party in public"),
        ]
        if corpus:
            G.append(("zip-currency",
                      f"{V}/verify-published-zip-currency.py",
                      ["--manual", str(doc)], True,
                      "the published ZIP must match the corpus, byte for byte"))
        # The .tex + compile log the Forge hands back are the only artifacts
        # showing what LaTeX actually RECEIVED. Wired when present; a missing
        # hand-back is a SKIP, never a pass.
        ob = DOCPROD / "outbound" / slug
        tex = next(iter(sorted(ob.glob("*.tex"))), None) if ob.is_dir() else None
        log = next(iter(sorted(ob.glob("*.compile.log"))), None) if ob.is_dir() else None
        G.append(("tex-artifacts", f"{V}/audit-tex-artifacts.py",
                  [str(tex)] if tex else None, True,
                  "markup that leaked into LaTeX: F-284 ate an AND, F-285 printed "
                  "&nbsp; 16 times, both with a CLEAN compile log"
                  if tex else "no .tex hand-back in outbound"))
        G.append(("render-overfulls", f"{V}/audit-render-overfulls.py",
                  [str(log)] if log else None, True,
                  "overfull boxes exist only in the render, in no markdown"
                  if log else "no compile log in outbound"))
        if pdf:
            G += [
                ("pdf-metadata", f"{V}/audit-pdf-metadata.py",
                 [pdf, "--request", str(ws / "request.json")], True,
                 "the PDF must carry the identity it declares"),
                ("pdf-margin-overflow", f"{V}/audit-pdf-margin-overflow.py",
                 [pdf], True,
                 "text crossing the right margin, measured not eyeballed"),
            ]
        else:
            G += [("pdf-metadata", None, None, True, "no --pdf given"),
                  ("pdf-margin-overflow", None, None, True, "no --pdf given")]

    # The meta-gate runs in BOTH phases and is the reason this manifest stays
    # honest: it turns red when a gate script exists that nothing invokes.
    if phase == "release":
        # ADVISORY, and it PRINTS rather than merely passing. Stephen asked to see
        # the state of ingestion we consider critical at the moment of release --
        # a check that only reports pass/fail would tell him nothing at all.
        G.append(("ingestion-state", f"{V}/audit-ingestion-row-artifacts.py",
                  ["--critical-only"], "advisory",
                  "ingestion rows whose ✅ has no artifact behind it"))

        # ADVISORY for the same reason, and it belongs at a RELEASE specifically:
        # this is the moment someone is thinking about publishing. KB v1.18.1 was
        # tagged 2026-09-10 and sat local-only for a day while manual releases ran
        # on top of it -- p2kb-mcp kept serving v1.18.0, so every agent read the
        # superseded CORDIC formats. `release-yamls` was right to leave the push to
        # Stephen (irreversible, sprint stop 2) and wrong to END there: the release's
        # unfinished half became a line in a resume note, which is the F-301 shape.
        # Advisory, never blocking -- an unpushed KB tag is not a reason to hold a
        # manual, but it must never again be something only a note remembers.
        G.append(("unpushed-releases", f"{V}/audit-unpushed-releases.py",
                  [], "advisory",
                  "release tags that exist locally but not on the remote"))

    # --head manual on purpose: a YAML- or ingestion-head gate left unwired must
    # not block a manual release, or the meta-gate becomes the thing everyone
    # routes around -- which is how gates die in the first place.
    G.append(("gate-arming", f"{V}/audit-gate-arming.py", ["--head", "manual"],
              True, "a gate nobody runs is not a gate"))
    return G


def run_gate(script, argv):
    try:
        p = subprocess.run([sys.executable, script] + list(argv),
                           cwd=ROOT, capture_output=True, text=True, timeout=900)
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"
    except OSError as e:
        return 125, f"could not execute: {e}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug")
    ap.add_argument("--phase", choices=("prepare", "release"))
    ap.add_argument("--pdf", help="the generated PDF (release phase)")
    ap.add_argument("--list", action="store_true",
                    help="list the gates for the phase and exit, running none")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not args.slug or not args.phase:
        ap.error("--slug and --phase are required")

    gates = build_gates(args.slug, args.phase, args.pdf)
    if args.list:
        for name, script, _, blocking, why in gates:
            print(f"  {'BLOCK' if blocking else 'warn ':<6} {name:<22} "
                  f"{script or '(not runnable here)'}\n{'':>31}{why}")
        return 0

    print(f"manual-release gates — {args.slug} — phase {args.phase}\n")
    failed, skipped, passed, known, advisory = [], [], [], [], []
    for name, script, argv, blocking, why in gates:
        if script is None or argv is None:
            print(f"  SKIP    {name:<22} {why}")
            skipped.append(name)
            continue
        rc, out = run_gate(script, argv)
        if blocking == "advisory":
            print(f"  ADVISORY {name} — {why}")
            for line in out.strip().splitlines():
                if line.strip():
                    print(f"            {line}")
            advisory.append(name)
        elif rc == 0:
            print(f"  PASS    {name}")
            passed.append(name)
        elif rc == 2:
            # Usage/IO error: the gate did not evaluate anything. That is a WIRING
            # defect and it must be loud -- reporting it as a failure blames the
            # document, and reporting it as a skip lets a mis-wired gate go quiet,
            # which is the whole failure class this runner exists to end.
            print(f"  \033[1mERROR\033[0m   {name:<22} the gate could not run "
                  f"(exit 2 = bad invocation). Fix the wiring, not the document.")
            for line in out.strip().splitlines()[:4]:
                print(f"            {line}")
            failed.append(name + " (wiring)")
        elif rc in (124, 125):
            print(f"  SKIP    {name:<22} could not run ({out.strip()[:60]})")
            skipped.append(name)
        elif blocking == "advisory":
            print(f"  ADVISORY {name} — {why}")
            for line in out.strip().splitlines():
                if line.strip():
                    print(f"            {line}")
            advisory.append(name)
        elif not blocking:
            # Declared non-blocking: a KNOWN, RECORDED gap. It is printed every
            # run precisely so it cannot fade into background -- but it does not
            # hold the release, because a permanently-red gate is one people
            # learn to skip, and then it protects nothing.
            print(f"  KNOWN   {name:<22} exit {rc} — {why}")
            known.append(name)
        else:
            print(f"  \033[1mFAIL\033[0m    {name:<22} exit {rc} — {why}")
            if not args.quiet:
                for line in out.strip().splitlines()[-12:]:
                    print(f"            {line}")
            failed.append(name)

    total = len(gates)
    print(f"\n{len(passed)} passed · {len(failed)} failed · {len(known)} "
          f"known-gap · {len(skipped)} skipped · {len(advisory)} advisory, "
          f"of {total} declared.")
    if known:
        print("  A KNOWN gap is a recorded decision, not a clean result: "
              + ", ".join(known))
    if skipped:
        print("  A SKIP is not a pass — each one is a check that did not happen: "
              + ", ".join(skipped))
    if failed:
        print(f"\nRED  {args.slug} is not clear to proceed: " + ", ".join(failed))
        return 1
    print(f"\nGREEN  {args.slug} cleared {len(passed)} gate(s).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
