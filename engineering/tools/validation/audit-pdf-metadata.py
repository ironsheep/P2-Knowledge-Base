#!/usr/bin/env python3
"""
audit-pdf-metadata.py - the finished PDF must carry the identity it claims.

WHY THIS EXISTS
    P2-Streamer-Programming-Guide v1.0.9 shipped with an EMPTY Title, Subject and
    Author. So did every other manual in the set (F-300). Nothing caught it, because
    nothing looked: the compile log is clean, the page count is right, the pages read
    correctly, and the defect lives in a dictionary no reader opens.

    Then «#283» made every identity string on the cover a macro fed from
    request.json. That fixed the emptiness and created a sharper failure: if the
    Forge's foundation .sty predates the DOCUMENT METADATA section, the
    \\renewcommands have nothing to renew and the cover renders BLANK -- not stale,
    blank -- while the compile still exits 0. A page-count check cannot see a blank
    cover. Neither can a glyph audit. Only reading the artifact can.

    And the two halves can disagree with each other: the info dictionary can be
    perfect while the cover is empty, or the cover can be right while request.json
    was never updated. Checking one proves nothing about the other.

WHAT IT CHECKS
    1  Title / Subject / Author are present and non-empty        (the F-300 class)
    2  each AGREES with request.json -- the single source        («#283»)
    3  page 1 actually carries the version and date strings      (the blank cover)
    4  no PRIOR version literal survives anywhere in the document
    5  rights: copyright + licence reachable from the metadata   (F-316)
    6  metadata rights AGREE with the document's own copyright page

    Checks 5 and 6 are advisory until --require-rights is passed; the emitting
    mechanism ships with F-316 and the flag arms them per document.

WHY POPPLER AND NOT PYMUPDF
    audit-pdf-margin-overflow.py needs PyMuPDF, which is NOT in the devcontainer
    image -- discovered 2026-08-21 when that gate failed closed at a release. This
    gate uses pdfinfo/pdftotext, which are. A gate that cannot run is worse than no
    gate, because its silence reads like a pass.

USAGE
    python3 audit-pdf-metadata.py <rendered.pdf> --request <request.json>
                                  [--prior X.Y.Z] [--require-rights]

EXIT
    0 = clean    1 = violations    2 = bad usage
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# HOW EACH request.json METADATA KEY MUST SHOW UP IN THE FINISHED PDF.
#
# The checklist is DERIVED FROM request.json, not hardcoded here: every key the
# document declares must be accounted for by this table, and a key that is not is
# reported as `unverified-metadata-field` rather than ignored. That is deliberate —
# the metadata set is growing (F-316 adds copyright and licence), and a gate whose
# coverage depends on someone remembering to extend a list will silently stop
# covering the newest field, which is the one most likely to be wrong.
#
#   "info"   -> must appear in the PDF info dictionary under this exact key
#   "cover"  -> must appear in the rendered text of page 1 (macro-fed; blank if the
#               platform foundation is stale, which no page count can detect)
#   "rights" -> must be reachable from Keywords or an XMP stream
#   None     -> declared for the build, deliberately not emitted into the PDF
FIELD_MAP = {
    "title":     ("info", "Title"),
    "subtitle":  ("info", "Subject"),
    "author":    ("info", "Author"),
    "keywords":  ("info", "Keywords"),
    "copyright": ("rights", None),
    "license":   ("rights", None),
    "version":   ("cover", None),
    "date":      ("cover", None),
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout


def info_dict(pdf):
    out = {}
    for line in run(["pdfinfo", str(pdf)]).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def page_text(pdf, first=None, last=None):
    cmd = ["pdftotext"]
    if first:
        cmd += ["-f", str(first)]
    if last:
        cmd += ["-l", str(last)]
    return run(cmd + [str(pdf), "-"])


def norm_rights(s):
    """Compare rights on WHO holds them, not on how the symbol was typeset.
    ©, (c) and an omitted symbol are a rendering detail; the holders are the fact."""
    s = re.sub(r"\s*(?:©|\(c\))\s*", " ", (s or ""), flags=re.I)
    return norm(s).rstrip(".").lower()


def norm(s):
    """Compare on visible content: collapse whitespace, unify dashes and quotes."""
    s = (s or "").replace("—", "-").replace("–", "-")
    s = s.replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--request", required=True,
                    help="the document's request.json — the single source for identity strings")
    ap.add_argument("--prior", metavar="X.Y.Z",
                    help="the previously released version; fails if it survives anywhere "
                         "in the rendered text (a third, drifted copy of the version is the "
                         "defect «#283» removed from the template)")
    ap.add_argument("--require-rights", action="store_true",
                    help="treat missing copyright/licence metadata as a FAILURE rather than "
                         "a note (arm this once F-316's mechanism has shipped for the document)")
    args = ap.parse_args()

    pdf = Path(args.pdf)
    if not pdf.is_file():
        print(f"ERROR: not a file: {pdf}")
        return 2
    try:
        req = json.loads(Path(args.request).read_text(encoding="utf-8"))
        meta = req["documents"][0]["metadata"]
    except Exception as e:
        print(f"ERROR: cannot read metadata from {args.request}: {e}")
        return 2

    info = info_dict(pdf)
    p1 = page_text(pdf, 1, 1)
    full = page_text(pdf)
    viol, notes = [], []

    # --- 1: EVERY declared field is accounted for ------------------------------
    # Walk what the document actually declares. An unknown key fails loudly, so a
    # newly-added metadata field cannot slip past this gate unverified.
    unknown = [k for k in meta if k not in FIELD_MAP]
    for k in sorted(unknown):
        viol.append(("unverified-metadata-field",
                     f"request.json declares `{k}` = {meta[k]!r} and this gate has no rule for "
                     f"verifying it reached the PDF. Add it to FIELD_MAP — as \"info\" with its "
                     f"info-dictionary key, \"cover\" if it must render on page 1, \"rights\", or "
                     f"None if it is build-only and deliberately not emitted. Do not skip it: an "
                     f"unchecked field is exactly where the next empty-metadata release comes from"))

    checked = []
    # --- 2 + 3: info-dictionary fields — present, and agreeing with the source --
    for key, (kind, field) in FIELD_MAP.items():
        if kind != "info" or key not in meta:
            continue
        got, want = info.get(field, ""), meta.get(key, "")
        checked.append(f"{field}<-{key}")
        if not want:
            continue
        if not got:
            viol.append((f"{field.lower()}-empty",
                         f"PDF info dictionary has no {field}. This is the F-300 class: it ships "
                         f"invisibly, because no page shows it. request.json says {want!r}"))
        elif norm(got) != norm(want):
            viol.append((f"{field.lower()}-mismatch",
                         f"{field} disagrees with request.json, which is the single source.\n"
                         f"        PDF          : {got!r}\n"
                         f"        request.json : {want!r}"))
    # An info field the PDF carries that NOTHING declared is drift in the other
    # direction — a value from somewhere other than the single source.
    for key, (kind, field) in FIELD_MAP.items():
        if kind == "info" and key not in meta and info.get(field):
            viol.append((f"{field.lower()}-undeclared",
                         f"the PDF carries {field} = {info[field]!r}, and request.json declares no "
                         f"`{key}`. The value came from somewhere other than the single source"))

    # --- 4: the cover actually rendered its identity ---------------------------
    # A blank cover is the one defect a page count cannot see. These strings are
    # macro-fed, so if the foundation .sty is stale they vanish together.
    for key, (kind, _) in FIELD_MAP.items():
        if kind != "cover" or not meta.get(key):
            continue
        want = meta[key]
        checked.append(f"page1<-{key}")
        if norm(want) not in norm(p1):
            viol.append((f"cover-{key}-missing",
                         f"page 1 does not carry the {key} {want!r} that request.json declares. "
                         f"An EMPTY cover field means the Forge's p2kb-platform-foundation.sty "
                         f"predates the DOCUMENT METADATA section, so the \\renewcommands had "
                         f"nothing to renew — that is a PLATFORM problem, not a manuscript one. "
                         f"Deploy the current foundation; do not edit literals back onto the cover"))

    # --- 4: no prior version survives ------------------------------------------
    if args.prior:
        hits = [ln.strip() for ln in full.splitlines() if args.prior in ln]
        if hits:
            viol.append(("stale-version",
                         f"the prior version {args.prior!r} still appears in the rendered text "
                         f"({len(hits)} line(s)) — first: {hits[0][:90]!r}"))

    # --- 5 + 6: rights ---------------------------------------------------------
    # The info dictionary has no copyright field; Keywords and the XMP stream are
    # where rights live. Read the document's own copyright page as the truth.
    page_cr = ""
    m = re.search(r"Copyright\s*(?:©|\(c\))\s*\d{4}[^\n]*", full)
    if m:
        page_cr = m.group(0).strip()
    lic_on_page = bool(re.search(r"CC BY[- ]SA|Creative Commons", full, re.I))

    # READ THE ARTIFACT, NOT THE SOURCE. request.json declaring `copyright` proves
    # only that someone intended it; the question is whether it reached the PDF.
    # Mixing the two here would have made this gate pass on intent -- the precise
    # failure it exists to catch.
    rights_blob = info.get("Keywords", "")
    has_meta_rights = bool(re.search(r"Copyright|CC BY|Creative Commons", rights_blob, re.I))
    has_xmp = info.get("Metadata Stream", "no").lower() == "yes"
    if meta.get("copyright") and not (has_meta_rights or has_xmp):
        viol.append(("rights-declared-not-emitted",
                     f"request.json declares copyright {meta['copyright']!r} and the rendered PDF "
                     f"carries no Keywords and no XMP stream — the value was authored but never "
                     f"emitted. Check that the template consumes it and that the Forge's platform "
                     f"foundation is current"))

    if not has_meta_rights and not has_xmp:
        msg = ("the PDF carries NO machine-readable copyright or licence — no Keywords, no XMP "
               "stream. The page says " +
               (f"{page_cr!r}" if page_cr else "(no copyright line found)") +
               (" and grants CC BY-SA" if lic_on_page else "") +
               ", so a crawler or index reading this file sees an unlicensed document. F-316")
        (viol if args.require_rights else notes).append(
            ("rights-missing", msg) if args.require_rights else msg)
    elif page_cr and meta.get("copyright"):
        # both exist — they must not disagree about WHO holds it
        a, b = norm_rights(meta["copyright"]), norm_rights(page_cr)
        if a not in b and b not in a:
            viol.append(("rights-disagree",
                         f"metadata rights and the copyright page name different holders.\n"
                         f"        page         : {page_cr!r}\n"
                         f"        request.json : {meta['copyright']!r}"))

    # --- report ----------------------------------------------------------------
    print(f"{pdf.name}: {info.get('Pages','?')} pages, checked against {Path(args.request).name}")
    print(f"  declared fields : {', '.join(sorted(meta))}")
    print(f"  verified        : {', '.join(sorted(checked)) or '(none)'}")
    for key, (kind, field) in sorted(FIELD_MAP.items()):
        if kind == "info" and key in meta:
            print(f"  {field:9s}: {info.get(field) or '(EMPTY)'}")
    for n in notes:
        print(f"  note    : {n}")
    if not viol:
        print(f"\nCLEAN  identity metadata agrees with its source"
              f"{' and rights are present' if args.require_rights else ''}")
        return 0
    print(f"\nVIOLATIONS ({len(viol)}) — {pdf}")
    for kind, msg in viol:
        print(f"\n  {kind}\n    - {msg}")
    print("\nFAIL: fix request.json (the single source) or deploy the current platform "
          "foundation, then re-render. Never edit an identity string onto the cover.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
