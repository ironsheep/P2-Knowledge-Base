#!/usr/bin/env python3
"""Check every ingestion dashboard row against the artifacts on disk behind it.

WHY THIS EXISTS
---------------
The ingestion-backlog sprint (closed 2026-08-26) hit the SAME defect three times,
and each time it was found by a human reading, never by a gate:

  p2-hardware-manual  the row read ~65% and its audit read "Extraction Health 100%"
                      while NO extracted text existed in the repository at all.
  p2-datasheet        the row read 94% and the audit read "Tables preserved 85% /
                      Technical accuracy 100% / Zero contradictions" while the folder
                      held no table artifact and no raw-text artifact, and a sibling
                      file listed 10 structurally-lost tables. It sat eleven months.
  #64000 Eval Board   the row read "100% (stated)" while the 2025 capture had every
                      digit deleted, because the PDF's body font maps no numerals.

One sentence covers all three: **a status cell was believed instead of the artifact
under it.** That is this repo's oldest lesson wearing an ingestion hat
([[feedback_a_gate_must_read_the_artifact]], [[feedback_status_line_is_not_evidence]]).

`audit-extraction-digit-density.py` closed the third case only — it catches total
numeral loss in a file that EXISTS. Nothing asked the prior question: does the file
exist at all, for every pass the dashboard claims is done?

THE CONTRACT IT CHECKS
----------------------
Taken from `ingest-source` SKILL.md, not invented here. Each pass column in the
Tier-2 registry has an artifact it is supposed to leave behind:

  C  content    <src>-text.txt, or a curated complete-*.md
  K  code       assets/code-<date>/ holding files
  I  images     assets/images-<src>-<date>/image-catalog.md
  A  audit      <src>-*extraction-audit*.md
  X  cross-src  <src>-cross-source-analysis.md   (WARN only -- pass 6's primary
                outputs are the CENTRAL registers KNOWLEDGE-GAPS.md and
                P2KB-CORRECTION-FINDINGS.md, so a per-source file is conventional
                rather than required)

A cell reading ✅ is a claim that the pass ran. This tool asks the artifact whether
it did.

ADVISORY BY DEFAULT, ON PURPOSE
-------------------------------
Exit 0 even with findings, so it can be read at a release without blocking one
(Stephen, 2026-09-10). `--blocking` makes CRITICAL exit 1 when we are ready for that.
An advisory instrument still has to be honest: it reports what it could NOT check as
loudly as what failed, because a check that quietly skipped is the failure it is
meant to catch.

Exit 0 = advisory (always, unless --blocking). Exit 1 = CRITICAL under --blocking.
Exit 2 = usage/IO error, INCLUDING "parsed no rows" -- auditing nothing is not a pass.
"""
import argparse
import os
import re
import sys
from pathlib import Path

DASHBOARD = "engineering/ingestion/README.md"
SOURCES = "engineering/ingestion/sources"

# A row name is prose with decorations; a folder is a slug. Where the two genuinely
# differ the alias is declared HERE, visibly -- never guessed at runtime, because a
# silent fuzzy match is how a row gets checked against the wrong folder and passes.
# A value may be a LIST: the dashboard's own model is "41 folders -> 36 logical
# sources", so one row can legitimately span two folders -- `taqoz` is the
# preliminary web research PLUS the authoritative Bit Bashers Guide that upgraded
# it, and the row names the second folder in its own note. Resolving such a row to
# one folder reports the other's artifacts as missing; that false CRITICAL was the
# last one standing after the contract was corrected.
ALIASES = {
    "spin2 language reference": "spin2-v55",
    "taqoz": ["taqoz", "TAQOZ-Forth-Bitbashers-Guide"],
}

# Folders that are not logical sources (the dashboard says so itself).
NOT_A_SOURCE = {"code-analysis", "marketing-materials", "pasm2-manual-development", "spin2-v51"}

DONE, PARTIAL, PENDING, NA, VERIFY = "✅", "◐", "⏳", "—", "?"


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / ".git").exists() and (p / "engineering").is_dir():
            return p
    sys.exit("ERROR: could not locate the repository root.")


ROOT = repo_root()


def parse_rows():
    rows, path = [], ROOT / DASHBOARD
    if not path.is_file():
        sys.exit(f"ERROR: no dashboard at {DASHBOARD}")
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            continue
        if cells[0] == "Source" or set(cells[0]) <= set("-: "):
            continue
        rows.append((n, cells))
    return rows


def clean(name: str) -> str:
    name = re.sub(r"‹[^›]*›", "", name)          # provenance tags
    name = re.sub(r"\*\*|\*|`|_", "", name)      # emphasis
    name = re.sub(r"@.*$", "", name)             # "@ v55" edition marker
    name = name.replace("(", " ").replace(")", " ")   # "Smart Pins (Titus)"
    return re.sub(r"\s+", " ", name).strip()


def resolve(name: str, folders):
    key = clean(name).lower()
    if key in ALIASES:
        a = ALIASES[key]
        return (a if isinstance(a, list) else [a]), "alias"
    slug = key.replace(" ", "-")
    if slug in folders:
        return [slug], "exact"
    hits = [f for f in folders if f == slug or f in slug or slug in f]
    if len(hits) == 1:
        return [hits[0]], "matched"
    if hits:
        # LONGEST wins. A shorter folder name is a prefix of a more specific one --
        # "smart-pins" is a substring of "smart-pins-titus" -- and taking the short
        # one audits a row against the WRONG source, then reports its artifacts as
        # missing. That false CRITICAL appeared on the first run.
        hits.sort(key=len, reverse=True)
        return [hits[0]], "matched(longest)"
    return None, "UNRESOLVED"


def artifacts(folder: Path):
    """What actually exists, per pass. Presence AND non-triviality."""
    def big(p, floor=2000):
        try:
            return p.stat().st_size >= floor
        except OSError:
            return False

    # The contract as the corpus actually practises it, not as the skill's table
    # abbreviates it. `<src>-text.txt` is ONE shape among several: the dominant one
    # is `<src>-narrative.txt`, and a source whose original IS structured data keeps
    # it in that form (`.csv` for the instruction spreadsheet, `.lst` for the ROM
    # booter listing). Checking only for `-text.txt` produced 18 CRITICALs on the
    # first run, nearly all of them false -- and a gate that cries wolf is a gate
    # that gets ignored, which is how the next real hole ships.
    # Loose on the NAME, strict on the QUESTION. Extraction filenames vary more than
    # the skill's `<src>-text.txt` shorthand suggests -- smart-pins ships
    # `smartpins-text-fresh.txt` and `smartpins-narrative-from-docx.txt` -- and an
    # anchored glob reported that fully-extracted source as having no content at all.
    def live(q):
        return not any(q.name.endswith(x) for x in (".deprecated", ".bak", ".orig"))
    text = [q for q in folder.glob("*text*.txt") if live(q)]
    text += [q for q in folder.glob("*narrative*.txt") if live(q)]
    text += [q for q in folder.glob("complete-*.md")]
    text += [q for q in folder.glob("*.csv")]
    text += [q for q in folder.glob("*.lst")]
    # A source whose original is a BINARY document must have an extraction; a source
    # that simply IS a set of authored notes does not. That distinction is the whole
    # instrument, and getting it wrong in either direction breaks the tool:
    #
    #   too strict -- chip-gracey-clarifications holds dated .md notes and no binary
    #                 original. The notes ARE the source. Demanding a -text.txt there
    #                 is a false CRITICAL.
    #   too loose  -- the first version accepted "any substantial .md that is not an
    #                 audit". REPLAYED AGAINST HISTORY (git fd49b9f4, the state before
    #                 the 2026-08-24 re-ingestion) that rule reads
    #                 `hardware-manual-2022-extraction.md` at 6,226 bytes as content
    #                 and calls the folder fine -- MISSING the exact incident this
    #                 tool was built for, where a .docx sat with no extraction beside
    #                 it while the audit claimed "Extraction Health 100%".
    #
    # So: only a folder holding NO binary original may fall back to authored .md.
    originals = [q for ext in ("*.pdf", "*.docx", "*.xlsx", "*.doc")
                 for q in folder.glob(ext)]
    if not text and not originals:
        text = [p for p in folder.glob("*.md")
                if big(p, 2000) and "audit" not in p.name.lower()
                and p.name.lower() not in ("readme.md", "ingestion-process.md")]
    code = [d for d in folder.glob("assets/code-*") if d.is_dir() and any(d.iterdir())]
    # Catalog FILENAMES are not standardised in this corpus, and an anchored glob
    # called two fully-catalogued sources uncatalogued. Three live shapes:
    #   image-catalog.md                     p2-hardware-manual, smart-pins-titus, ...
    #   <doc>_image_catalog.md               p2-datasheet (x3 extractions)
    #   <doc>_smartpins_catalog.md           smart-pins
    # Match on the QUESTION (is there a catalog beside the images?), not the name.
    # The naming drift is itself worth fixing at the source one day; until then a
    # gate that only knows one spelling manufactures false gaps.
    # ...and not the DIRECTORY name either: p2-click-adapter's visuals live under
    # assets/render-*/ because that source has zero embedded images (vector art with
    # its text converted to curves), so its figures are rendered pages rather than
    # extracted XObjects.
    imgs = [q for q in folder.glob("assets/*/*")
            if q.suffix.lower() in (".md", ".json") and "catalog" in q.name.lower()]
    audit = [p for p in folder.glob("*audit*.md") if big(p, 500)]
    xsrc = list(folder.glob("*cross-source*.md"))
    # SIZE is a separate question from PRESENCE, and conflating them cost a false
    # CRITICAL: p2-click-adapter's extraction is 1,190 bytes and that is the CORRECT
    # outcome -- the schematic is vector art with its text converted to curves, so the
    # text layer holds only the title block and the source was read from rendered
    # pages instead. A tiny artifact is a question, not a verdict.
    thin = [q for q in text if not big(q)]
    return {"C": text, "K": code, "I": imgs, "A": audit, "X": xsrc, "_thin": thin}


PASS_NAME = {"C": "content", "K": "code", "I": "images", "A": "audit", "X": "cross-source"}
# Absence of these two is what produced every incident this tool exists for.
CRITICAL_PASSES = {"C", "A"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--blocking", action="store_true",
                    help="exit 1 on CRITICAL (default is advisory, exit 0)")
    ap.add_argument("--critical-only", action="store_true",
                    help="print only CRITICAL findings -- the release-time view")
    ap.add_argument("--negative-control", action="store_true",
                    help="prove the check can fail: audit a row against a folder "
                         "known to hold none of the artifacts")
    args = ap.parse_args()

    rows = parse_rows()
    if not rows:
        sys.exit("ERROR: parsed 0 registry rows -- the dashboard's table shape changed "
                 "and this tool is auditing nothing, which is never a pass.")

    src_root = ROOT / SOURCES
    folders = {d.name.lower() for d in src_root.iterdir() if d.is_dir()}

    if args.negative_control:
        # A GUARANTEED-empty directory. The first version of this control pointed at
        # engineering/tools -- a real directory with no ingestion artifacts -- and the
        # control FAILED, because the last-resort ".md" rule below found ordinary
        # documentation there and called it content. That is worth recording: the
        # last-resort rule is deliberately loose, so it must only ever be applied to
        # a source folder, never to an arbitrary path.
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            found = artifacts(Path(td))
            missing = [k for k in "CKIAX" if not found[k]]
        ok = missing == list("CKIAX")
        print(f"negative control: an empty folder reports missing {missing}")
        print("PASS -- the check can fail" if ok else
              "FAIL -- the check found artifacts where there are none; it is inert")
        return 0 if ok else 1

    critical, warn, info, unresolved = [], [], [], []
    checked = 0

    for lineno, c in rows:
        name, auth, cells, cmpl = c[0], c[1], c[2:7], c[7]
        folder_names, how = resolve(name, folders)
        if folder_names is None or all(f in NOT_A_SOURCE for f in folder_names):
            unresolved.append((clean(name), how))
            continue
        # Union across the row's folders: a logical source is done if the pass's
        # artifact exists in ANY folder the row covers.
        found = {k: [] for k in ("C", "K", "I", "A", "X", "_thin")}
        real = []
        for fn in folder_names:
            d = src_root / fn
            if not d.is_dir():
                # case-insensitive fallback: the registry writes TAQOZ-..., disk may differ
                d = next((x for x in src_root.iterdir()
                          if x.is_dir() and x.name.lower() == fn.lower()), None)
            if d is None:
                continue
            real.append(d.name)
            for k, v in artifacts(d).items():
                found[k].extend(v)
        if not real:
            unresolved.append((clean(name), "folder named but absent on disk"))
            continue
        folder_name = "+".join(real)
        checked += 1

        for col, cell in zip("CKIAX", cells):
            claimed = cell.startswith(DONE) or cell.startswith(PARTIAL)
            if not claimed or found[col]:
                continue
            item = (clean(name), folder_name, col, PASS_NAME[col], auth, cell)
            (critical if col in CRITICAL_PASSES and cell.startswith(DONE) else warn).append(item)

        if found["C"] and found["_thin"] and len(found["C"]) == len(found["_thin"]):
            warn.append((clean(name), folder_name, "C",
                         f"content artifact present but only "
                         f"{min(q.stat().st_size for q in found['_thin'])} bytes — "
                         f"verify it is the whole document", auth, cells[0]))

        # A percentage that says "stated" is a declaration. #64000 read
        # "100% (stated)" over a capture with every digit deleted.
        if re.search(r"\bstated\b", cmpl, re.I):
            warn.append((clean(name), folder_name, "%", "completeness declared, not measured",
                         auth, cmpl[:70]))
        if cmpl.strip().startswith("?"):
            info.append((clean(name), folder_name, "%", "completeness unknown", auth, cmpl[:60]))

    print(f"ingestion row-vs-artifact audit — {checked} source rows checked "
          f"of {len(rows)} registry rows\n")

    if critical:
        print(f"🔴 CRITICAL ({len(critical)}) — the row says the pass is DONE and the "
              f"artifact is not there:")
        for nm, f, col, pn, auth, cell in critical:
            print(f"   {auth}  {nm}  [{f}]  {col}={cell} but no {pn} artifact")
        print()
    else:
        print("🔴 CRITICAL (0) — every ✅ content and audit claim has an artifact behind it.\n")

    if not args.critical_only:
        if warn:
            print(f"🟡 WARN ({len(warn)}):")
            for nm, f, col, pn, auth, cell in warn:
                print(f"   {auth}  {nm}  [{f}]  {pn} — {cell}")
            print()
        if info:
            print(f"⚪ INFO ({len(info)}) — honestly marked as unknown, not a defect:")
            for nm, f, col, pn, auth, cell in info:
                print(f"   {auth}  {nm}  [{f}]  {cell}")
            print()
        if unresolved:
            print(f"❓ NOT CHECKED ({len(unresolved)}) — a row this tool could not tie to a "
                  f"source folder. These are the rows it is SILENT about, which is exactly "
                  f"the state that hides a defect:")
            for nm, how in unresolved:
                print(f"   {nm}  ({how})")
            print()

    print(f"advisory — CRITICAL {len(critical)} · WARN {len(warn)} · INFO {len(info)} · "
          f"not checked {len(unresolved)}")
    if args.blocking and critical:
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
