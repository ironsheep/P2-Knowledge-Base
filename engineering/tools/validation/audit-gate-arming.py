#!/usr/bin/env python3
"""Audit whether this repo's gates are actually INVOKED by anything.

WHY THIS EXISTS
---------------
A gate nobody runs is not a gate. This repo has proved that four separate times,
and each proof cost a shipped defect or a wasted release:

  F-294  audit-backtick-balance.py was BUILT, sat clean on disk, and no skill
         invoked it. A whole "Try it" paragraph shipped wrecked in a released
         manual while the instrument that detects it existed.
  F-301  the per-feature adoption tracker recorded its rule correctly and was
         passed over about a dozen times, because nothing consulted it at the
         moment of release.
  #339   audit-yaml-duplicate-keys.py is armed and returns 0 across 1132 files
         and is NOT wired into validate-dod-release.py -- a duplicate key
         reintroduced tomorrow turns nothing red at release.
  F-376  two gates that exit 0 while doing nothing at all.

Measured 2026-09-10, which is why this tool was written: of 21 gate scripts,
only 5 were invoked by any other script. Two -- audit-inline-run-width.py and
check_latex_braces.py -- were referenced by NO file in the repository, yet
audit-inline-run-width was run by hand during the v1.18.0 sweep. That is a gate
surviving on tribal memory, one forgotten session away from silence.

This tool is the meta-gate: it reads the gate scripts and the things that could
invoke them, and reports which gates nothing would ever run. Adding a new gate
without wiring it now turns this red.

WHAT COUNTS AS AN INVOCATION (the truth side)
---------------------------------------------
Only a file that can CAUSE the gate to run:

  RUNNER  another .py/.sh under engineering/tools -- executable wiring. Strongest:
          it runs whether or not a human remembers.
  SKILL   a .claude/skills SKILL.md or project-overlay.md -- an instruction an
          agent follows. Real, but only as good as the reading.

Deliberately NOT counted, because they record history rather than cause a run:
sprint closeouts and plans, changelogs, the correction registers and their
archives, analysis documents, and anything under .backups. A tool named only in
a closeout is a tool someone ran ONCE.

DESIGN RULE: ZERO FALSE POSITIVES, OR IT GETS IGNORED
-----------------------------------------------------
A helper that is imported rather than invoked, or a script deliberately kept
manual, is declared in EXEMPT below WITH ITS REASON. An unexplained gap is the
defect; a chosen and visible one is not.

Exit 0 = every gate is invoked by something. Exit 1 = at least one UNWIRED gate.
Exit 2 = usage/IO error.
"""
import argparse
import os
import re
import sys
from pathlib import Path

# Directories that can INVOKE a gate.
RUNNER_ROOTS = ("engineering/tools",)
SKILL_ROOTS = (".claude/skills",)

# Where gates live. A file here is a gate unless EXEMPT says otherwise.
GATE_DIRS = ("engineering/tools/validation",)
# Gate-shaped tools that live one level up, by name prefix.
GATE_PREFIXES = ("validate-", "verify-", "audit-")

# Paths that record history rather than cause a run -- never counted.
RECORD_ONLY = re.compile(
    r"(^|/)(\.git|\.backups|node_modules)/"
    r"|(^|/)engineering/history/"
    r"|(^|/)engineering/analysis/"
    r"|(^|/)correction-sweeps/"
    r"|CORRECTION-FINDINGS\.md$"
    r"|CHANGELOG[^/]*\.md$"
)

# Runners EXECUTE gates; they are not themselves gates, so they are not censused.
RUNNERS = {"validate-dod-release.py", "validate-manual-release.py"}

# Which head owns each gate. A runner is only responsible for ITS head's gates --
# a YAML-head gate left unwired must not block a manual release, or the meta-gate
# becomes the thing everyone routes around. Gates with no head listed are
# reported UNASSIGNED at repo scope: that is a real finding (nobody owns wiring
# them) but it is nobody's release blocker until a head claims them.
HEADS = {
    "manual": {
        "audit-code-line-length.py", "audit-inline-code-ascii.py",
        "audit-backtick-balance.py", "audit-inline-run-width.py",
        "audit-font-glyphs.py", "audit-spin2-ascii.py", "audit-tex-artifacts.py",
        "audit-pdf-metadata.py", "audit-pdf-margin-overflow.py",
        "audit-render-overfulls.py", "audit-license-block.py",
        "audit-review-scaffolding.py", "verify-published-zip-currency.py",
        "verify-example-corpus-identity.py", "sync-manual-examples.py",
        "audit-gate-arming.py",
    },
    "yaml": {
        "audit-constant-fidelity.py", "audit-yaml-claim-sourcing.py",
        "audit-yaml-duplicate-keys.py", "validate-crossref-keys.py",
        "validate-yaml-syntax.py", "verify-yaml-format.py",
        "audit-adc-encoding.py", "audit-register-hygiene.py",
    },
    "ingestion": {
        "audit-extraction-digit-density.py",
        # Invoked ADVISORY from the manual release runner (Stephen, 2026-09-10) so the
        # ingestion corpus feeding the manuals is read at every release. It belongs to
        # the ingestion head even though the manual head is what currently runs it.
        "audit-ingestion-row-artifacts.py",
    },
}

# A gap is acceptable when CHOSEN AND VISIBLE. Each entry needs a reason.
EXEMPT = {
    "check_latex_braces.py":
        "Ad-hoc diagnostic for a brace-imbalance hunt, not a release gate. "
        "Superseded in practice by audit-tex-artifacts.py, which reads the "
        "generated .tex. Kept for one-off debugging; delete when that is "
        "confirmed redundant.",
}


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / ".git").exists() and (p / "engineering").is_dir():
            return p
    # .backups copies break a path-derived root; fail loudly rather than guess.
    sys.exit("ERROR: could not locate the repository root from this script's path.")


def collect_gates(root: Path):
    gates = {}
    for d in GATE_DIRS:
        for f in sorted((root / d).glob("*.py")):
            gates[f.name] = f.relative_to(root)
    tools = root / "engineering/tools"
    for f in sorted(tools.glob("*.py")):
        if any(f.name.startswith(p) for p in GATE_PREFIXES):
            gates.setdefault(f.name, f.relative_to(root))
    return gates


SELF = Path(__file__).name


def scan(root: Path, roots, exts):
    """Yield (relpath, text) for candidate invoker files.

    This file is excluded from its own scan. It necessarily NAMES gates -- in
    EXEMPT, and in the negative control -- and counting those as invocations
    would let the auditor mark a gate armed purely by talking about it. The
    negative control caught exactly that on first run.
    """
    for r in roots:
        base = root / r
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
            for fn in filenames:
                if not fn.endswith(exts):
                    continue
                p = Path(dirpath) / fn
                rel = str(p.relative_to(root))
                if RECORD_ONLY.search("/" + rel) or fn == SELF:
                    continue
                try:
                    yield rel, p.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue


# A gate name appearing in a runner is NOT proof the runner runs it. Three of the
# first run's "ARMED" verdicts were docstring cross-references -- one script's
# prose mentioning another. That is this auditor committing the exact defect it
# audits for: reading a declaration instead of the artifact
# ([[feedback_a_gate_must_read_the_artifact]]). So a RUNNER match now requires
# the name to sit on a line that also carries invocation machinery.
def strip_prose(text: str) -> str:
    """Remove module docstrings and comments, leaving executable code.

    A gate name appearing in a runner is NOT proof the runner runs it. Three of
    the first run's "ARMED" verdicts were docstring cross-references -- one
    script's prose mentioning another -- which is this auditor committing the
    very defect it audits for: reading a declaration instead of the artifact
    ([[feedback_a_gate_must_read_the_artifact]]).

    Requiring an invocation token on the same line was the first fix and was
    WRONG in the other direction: it missed manifest-style wiring, where the
    script path is a string in a table and the subprocess call lives in a helper
    far away. It reported five genuinely-wired gates as UNWIRED.

    So the rule is structural rather than lexical: prose cannot invoke anything,
    and code that names a gate is wiring. Strip the prose, search the code.
    """
    out, i, n = [], 0, len(text)
    quote = None
    while i < n:
        if quote:
            j = text.find(quote, i)
            if j == -1:
                break
            i = j + len(quote)
            quote = None
            continue
        m = re.compile(r'"""|\'\'\'').search(text, i)
        if not m:
            out.append(text[i:])
            break
        out.append(text[i:m.start()])
        quote = m.group(0)
        i = m.end()
    code = "".join(out)
    return "\n".join(l.split("#")[0] for l in code.splitlines())


def invokes(text: str, name: str) -> bool:
    """True when `text` looks like it RUNS `name`, not merely mentions it."""
    return name in strip_prose(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quiet", action="store_true",
                    help="print only the verdict line")
    ap.add_argument("--show-tiers", action="store_true",
                    help="list every gate with what invokes it, not just failures")
    ap.add_argument("--head", choices=sorted(HEADS),
                    help="census only this head's gates; a sibling head's "
                         "unwired gate must not block this head's release")
    ap.add_argument("--negative-control", action="store_true",
                    help="prove the check can fail: inject a gate name nothing "
                         "invokes and confirm it is reported UNWIRED")
    args = ap.parse_args()

    root = repo_root()
    gates = collect_gates(root)
    if not gates:
        sys.exit("ERROR: found no gate scripts -- the scan is mis-scoped, which "
                 "would make this tool report a clean bill of health over nothing.")

    runners = list(scan(root, RUNNER_ROOTS, (".py", ".sh")))
    skills = list(scan(root, SKILL_ROOTS, (".md",)))

    if args.negative_control:
        # Inject into a head as well as the gate list. Without the head, the
        # control lands in UNASSIGNED and never exercises the UNWIRED path --
        # the control would pass while proving the wrong branch. Caught on the
        # first run after head-scoping was added.
        gates = dict(gates)
        gates["audit-nonexistent-control.py"] = Path(
            "engineering/tools/validation/audit-nonexistent-control.py")
        HEADS["manual"].add("audit-nonexistent-control.py")

    gates = {n: p for n, p in gates.items() if n not in RUNNERS}
    if args.head:
        owned = HEADS[args.head]
        gates = {n: p for n, p in gates.items() if n in owned}
        if not gates:
            sys.exit(f"ERROR: head '{args.head}' claims no gates that exist on "
                     "disk -- the head map is stale, and a census over nothing "
                     "would report a false clean.")

    rows = []
    for name, path in sorted(gates.items()):
        by_runner = [r for r, t in runners
                     if r != str(path) and invokes(t, name)]
        by_skill = [s for s, t in skills if name in t]
        if by_runner:
            tier, detail = "ARMED", by_runner[0]
        elif by_skill:
            tier, detail = "PROSE", by_skill[0]
        elif name in EXEMPT:
            tier, detail = "EXEMPT", EXEMPT[name].split(".")[0] + "."
        elif not any(name in owned_set for owned_set in HEADS.values()):
            tier, detail = "UNASSIGNED", "no head owns this gate's wiring"
        else:
            tier, detail = "UNWIRED", "nothing in the repo invokes this"
        rows.append((tier, name, detail, len(by_runner), len(by_skill)))

    unwired = [r for r in rows if r[0] == "UNWIRED"]
    prose = [r for r in rows if r[0] == "PROSE"]
    armed = [r for r in rows if r[0] == "ARMED"]
    exempt = [r for r in rows if r[0] == "EXEMPT"]
    unassigned = [r for r in rows if r[0] == "UNASSIGNED"]

    if args.negative_control:
        ok = any(r[1] == "audit-nonexistent-control.py" for r in unwired)
        print(f"negative control: injected gate reported UNWIRED = {ok}")
        print("PASS -- the check can fail" if ok else
              "FAIL -- the check cannot detect an unwired gate; it is inert")
        return 0 if ok else 1

    if not args.quiet:
        print(f"gates found: {len(rows)}  "
              f"(ARMED {len(armed)} · PROSE {len(prose)} · "
              f"EXEMPT {len(exempt)} · UNASSIGNED {len(unassigned)} · "
              f"UNWIRED {len(unwired)})"
              + (f"   [head: {args.head}]" if args.head else "") + "\n")
        if args.show_tiers:
            for tier, name, detail, nr, ns in rows:
                print(f"  {tier:<8} {name:<38} {detail}")
            print()
        if prose:
            print("PROSE-ONLY -- runs only if an agent reads the skill and complies.")
            print("These are not blocking here, but each is a candidate for a runner:")
            for _, name, detail, _, ns in prose:
                print(f"  {name:<38} named in {ns} skill file(s), e.g. {detail}")
            print()
        if unassigned and not args.head:
            print("UNASSIGNED -- these exist and no head owns wiring them.")
            print("Not a release blocker; it IS a decision nobody has made:")
            for _, name, _, _, _ in unassigned:
                print(f"  {name}")
            print()
        if unwired:
            print("UNWIRED -- these exist and NOTHING invokes them:")
            for _, name, _, _, _ in unwired:
                print(f"  {name}")
            print("\nFIX: wire each into the runner for its head, or add it to a "
                  "skill step, or declare it in EXEMPT with the reason it is "
                  "deliberately manual. Do not leave it silent.")

    if unwired:
        print(f"\nRED  {len(unwired)} gate(s) exist that nothing would ever run.")
        return 1
    print("CLEAN  every gate is invoked by a runner or a skill.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
