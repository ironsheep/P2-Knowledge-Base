#!/usr/bin/env python3
"""
audit-yaml-claim-sourcing.py - a quantitative claim in the shipped KB must say
where it came from.

WHY THIS EXISTS
    `audit-constant-fidelity.py` compares the KB's description of a NAMED
    CONSTANT against the source's. Within an hour of it shipping, F-327 was
    found -- and that tool was structurally blind to it, because the defect
    named no constants at all:

        drive_strength_configurations:
          current_modes:
            - mode: "1.5mA"
              impedance: "~2000Ohm"
            ...
        slew_rate_control:
          fast_slew:
            rise_fall: "< 2ns with strong drive"

    None of that exists. The P2 has no 1.5mA/3.0mA/15mA/75mA/150mA drive ladder,
    no impedance table, and no programmable slew rate -- the string "slew"
    appears ZERO times across the Silicon Doc, the Spin2 sources, and the
    smart-pins catalog. It is not a mislabel of a real mechanism; it is a
    mechanism that does not exist, stated in six numbers and a feature name.

    This is the "information that should no longer be in the files" half of the
    release gate, and the fidelity tool cannot see it. Name coverage is not
    semantic coverage, and that cuts both ways.

THE TELL, AND WHY IT IS MECHANICAL
    The file that carried F-327 cites its sources -- three sections up:

        absolute_maximum_ratings:
          source: "Parallax P2 Datasheet (Absolute Maximum Electrical Ratings...)"
        special_timing_modes:
          source: "P2 Silicon Doc v35"

    ...and then states a drive ladder, an impedance table and a whole feature
    with no `source:` field anywhere near them.

    That asymmetry IS the signal, and it needs no judgement about content. A
    file that demonstrably knows the citing convention, and then abandons it for
    a block full of physical quantities, is flagging itself. This tool does
    nothing cleverer than notice that.

    It is deliberately NOT "every claim must be cited" -- that would fire on the
    entire corpus at once, be triaged as noise, and get switched off. It asks
    the narrower question the evidence actually supports.

TWO TIERS
  Tier 1 -- BLOCKS. `UNCITED_IN_CITING_FILE`: the file cites somewhere, and a
      block carrying physical quantities does not. This is the F-327 shape
      exactly, and the file's own other sections are the control.

  Tier 2 -- ADVISORY. `UNCITED_FILE`: the file carries physical quantities and
      cites nothing, anywhere. Could be wholesale fabrication; could equally be
      a file authored before the convention existed. There is no in-file control
      to compare against, so a human decides. Advisory rather than blocking
      because the population is large and mostly historical, and a gate that
      fires on hundreds of legacy files on day one is a gate that gets disabled.

WHAT COUNTS AS A QUANTITY -- and what deliberately does not
    Counted: currents, resistances, voltages, times, frequencies, capacitances,
    data rates -- claims about the physical world that must come from somewhere.

    NOT counted, because they are structure rather than measurement:
      * bare integers and hex -- pin numbers, indices, counts
      * P2 BINARY literals (`%0000_0000_000_...`). In Spin2 `%` is the binary
        prefix, NOT a percent sign. Reading it as a unit would flag every mode
        word in the knowledge base.
      * version numbers, dates, byte/bit widths

WHAT COUNTS AS A CITATION -- and what deliberately does not
    A citation names a DOCUMENT, or an empirical record. It is not a hardware
    revision and it is not a physical supply. Both of those were read as
    citations by the shipped detector (F-334) and both silenced the gate:

      * `Rev B` / `Rev C` was an INLINE citation token. On a board file that is
        the board's own identity -- `"5V shunt jumper required on P2-ES Eval
        Board Rev B"` -- and it marked the block cited.
      * ANY key literally named `source:` was a citation, whatever it named.
        `source: External 5V power supply (required)` is a POWER source, and it
        passed a block stating twelve currents.

    Both are false NEGATIVES: they do not produce a wrong finding, they produce
    no finding, which is worse. A gate that cannot fail manufactures confidence.

    So the key name is not the test; the VALUE is. See CITE_VALUE_RE.

WHAT MAY BE CITED -- THE ACCEPTANCE RULE («#412», S-393; Stephen Q3/Q4/Q5/Q12)
    A citation names an official Parallax document, never one we created. A
    citation VALUE counts only when it carries ONE of:

      * a Parallax document TITLE from the ingested-source registry
        (CANONICAL_TITLES below, each READ OFF the document's own cover/footer),
        with its edition or section, plus `p.N` when the document is a
        paginated PDF -- `"<Parallax title> <edition>, <section heading>"`;
      * a Parallax published SOURCE LISTING (the Spin2 interpreter, the Spin2
        debugger, the ROM booter, the flash loader -- rows marked in
        LISTING_EDITION_RE), named WITH the edition that is currently ingested,
        then the routine or section: `"<listing title> <edition>, <routine>"`.
        A listing citation with no edition is NO_EDITION; one naming any other
        edition is STALE_EDITION (Stephen, 2026-10-10: a listing changes with
        each compiler/firmware revision, so a newer ingested edition makes every
        citation of an older one stale until re-checked). Never by line;
      * an EF-NNN that EXISTS as a `### EF-NNN` entry in
        P2-EMPIRICAL-FINDINGS.md (a fact measured on silicon);
      * a CP-NNN that EXISTS as a `### CP-NNN` entry in COMPILE-PROOFS.md
        (a compile proof, Q12);
      * an OBEX object by id -- `OBEX 2842 (Full Duplex Serial)` -- when that id
        EXISTS as `<id>.yaml` in community/obex/objects/ (the object is the artifact
        and the id is its citation). A nonexistent id is BAD_ID; the bare word OBEX
        with no id names no object and is refused.

    ...and it carries NONE of: an extraction path (`silicon-doc-text.txt:NNN`,
    any `engineering/` path), a register or summary of ours (`SOURCE-ERRATA.md`,
    `complete-*.md`, `P2 Errata`), a batch label (`parallax-quick-bytes`), a line
    locator, or an EF/CP/XF id that does not exist. Catalog entries under
    community/quick-bytes/ are cited by their parallax.com `url:` (Q5).

    `enhancement_source:` is NOT a citation key (Q3) -- its 356 lines are labels,
    deleted by «#422». CITE_KEY_RE teaches `documentation_source` only.

    BAD_CITATION (this rule applied to every claimed citation, wherever it sits)
    BLOCKS, and so does Tier 1. Tier 2 is built SWITCHABLE (TIER2_BLOCKING) --
    its switch-on follows S-295..S-307 and is OWED to the citations task.

EXIT STATUS
    0  no Tier 1 violations
    1  one or more Tier 1 violations
    2  the KB tree was not found -- nothing audited, which is never a pass

USAGE
    audit-yaml-claim-sourcing.py [--inventory] [--advisory] [--negative-control]
"""

import argparse
import functools
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
KB_ROOT = REPO / "deliverables" / "ai" / "P2"

# Printed on EVERY run, pass or fail. This gate is armed and blocking in
# `release-yamls` and in `validate-dod-release.py`, and a green from a blocking
# gate gets read as a guarantee unless the gate says what it did not look at.
SCOPE_NOTE = (
    "WHAT THIS GREEN DOES NOT CERTIFY\n"
    "  This instrument checks QUANTITATIVE CLAIMS -- a block carrying physical\n"
    "  quantities, in a file that demonstrably knows the citing convention.\n"
    "  Prose that describes a behaviour without stating a number passes\n"
    "  untouched, and Tier 2 (a file that cites nothing anywhere) is ADVISORY:\n"
    "  it does not block, and its population is not zero.\n"
    "  A citation being PRESENT is not the same as the citation being RIGHT --\n"
    "  nothing here reads the cited document -- a Parallax title, an EF or a CP\n"
    "  id is checked for EXISTING, not for supporting the claim beside it.\n"
    "  Only keys in FLAG_KEYS are judged; a citation in any other key, or in\n"
    "  prose with no cite key, is seen only by the per-line inline test.\n"
    "  Community/obex/objects/ is skipped, and the OBEX-metadata-vs-index check\n"
    "  (S-308c) is NOT built. Guide rules R6, R7 and R9 have no\n"
    "  instrument and are held by review. A clean run means NOT CAUGHT BY THESE\n"
    "  CHECKS -- never `correct`.")

# A citation KEY, in any of the spellings the corpus actually uses. The key name
# alone is NOT the test -- see CITE_VALUE_RE and is_citation().
#
# `documentation` was added 2026-08-25 (F-335a). The eval add-on board files cite
# as `documentation:` -> `primary: "<doc>"`, a spelling no key here matched, so
# eight board files that DO know the citing convention scored as wholly-uncited
# and their blocks could never reach Tier 1 -- the file's own other sections
# could not act as the control. Until F-334's repair the `Rev B` token was
# propping those files up in Tier 1 by accident, for entirely the wrong reason,
# which is why the gap was invisible.
CITE_KEY_RE = re.compile(
    r"^(\s*)-?\s*(source|sources|source_document|source_documents|citation|citations|"
    r"reference|references|authority|derived_from|verified_against|documentation|"
    r"documentation_source)\s*:\s*(.*)$",
    re.IGNORECASE)
# `documentation_source` is taught (Q3, 2026-10-09). `enhancement_source` is
# deliberately ABSENT: its values are bookkeeping labels, not documents.

# The keys whose claimed value is JUDGED by the acceptance rule (BAD_CITATION).
# `reference`/`references` are left out on purpose: they list cross-reference
# paths, which are not citations and must not be reported as bad ones.
FLAG_KEYS = {"source", "sources", "source_document", "source_documents",
             "citation", "citations", "authority", "derived_from",
             "verified_against", "documentation", "documentation_source"}

# ...because `source:` is the most overloaded key in this knowledge base. Of the
# 312 cite-KEY lines in the corpus, 224 do not name a document at all:
#
#     hub75_adapter.yaml:133   source: External 5V power supply (required)
#     hub75_adapter.yaml:129   source: P2 development board 5V supply
#     smart_pin_patterns.yaml  source: motor_control
#     event_system.yaml        sources: ["CT-passed-CT1", "CT-passed-CT2", ...]
#     external-symbols.yaml    source: "-I directories"
#
# The first two are a POWER source. The rest are pattern-category tags, event
# names and compiler search paths. Every one of them silenced the block it sat
# in -- `hub75_adapter.yaml` `power_requirements` states twelve currents
# (35mA, 1.5A/4A peak, ... 5A/20A peak) and was passed by the gate because a
# 5V supply was named as its "source".
#
# So a cite key counts only when its VALUE names a DOCUMENT (or an empirical
# record). This vocabulary is drawn from the 88 values in the corpus that ARE
# citations, not from intuition -- it covers every short form they actually use
# (`"P2 Datasheet"`, `"Silicon Doc v35"`, `"Hardware Manual 2022-11-01"`,
# `"PNut v47 release notes"`, `flash_loader.spin2`, `parallax-quick-bytes`,
# `complete-builtin-symbols.md`, `…/P2-EMPIRICAL-FINDINGS.md EF-053`) as well as
# the long ones. A key that introduces STRUCTURE (`sources:` + a list, `source:
# |` + a block scalar) is tested against its nested body, which is where the
# document is actually named.
CITE_VALUE_RE = re.compile(
    r"(doc\b|docs\b|documentation|datasheet|data\s*sheet|manual|guide|guides|"
    r"reference|spec\b|specification|book|tutorial|release\s*notes|symbol\s*table|"
    r"spreadsheet|schematic|app(lication)?\s*note|whitepaper|study|standard|errata|"
    r"silicon|parallax|chip\s+gracey|spin2|pasm2|pnut|obex|titus|"
    r"EF-\d+|empirical|hardware[- ]verified|verif|validat|measured|verbatim|"
    r"clarification|"
    r"\.(md|ya?ml|txt|spin2|pas|pdf|docx?|csv|py|json)\b|https?://|"
    r"\bline[s]?\s+\d|\bp\.\s*\d|\brow\s+\d|:\d+[-:]\d+|\bv\d{2}\b|\bv\d\.\d)",
    re.IGNORECASE)

# The YAML spellings that mean "the value is below, not here".
_STRUCTURE_VALUE = {"", "|", ">", ">-", ">+", "|-", "|+"}

# Physical quantities. Unit REQUIRED -- a bare number is structure, not a claim.
#
# The NUMBER accepts thousands separators (F-351, second artifact): without them
# `range: "3,333,333 Hz to 500,000,000 Hz"` split into the tokens `333 Hz` and
# `000 Hz`, which made no false finding but inflated every advisory's per-block
# count -- a number printed by a gate that nobody can reproduce by hand.
QTY_RE = re.compile(
    r"(?<![\w%$])"                       # not inside a %binary or $hex literal
    r"~?(\d+(?:,\d{3})*(?:\.\d+)?)\s*"
    r"(mA|uA|µA|μA|nA|A|kΩ|kOhm|kohm|Ω|Ohm|ohm|mV|uV|µV|V|"
    r"ns|us|µs|μs|ms|MHz|kHz|Hz|dB|pF|nF|uF|µF|Mbps|kbps|bps)"
    r"(?![\w])")

# THE BARE AMPERE IS THE ONE UNIT A PART NUMBER CAN IMPERSONATE (F-351).
# `A` is a single letter and the guard on the number's left edge passes at the
# start of a string and after `+`, so the detector read:
#     part_number: "64006A"      -> 64006 amperes   (a Parallax part number)
#     ISO/IEC 14443 A/MIFARE     -> 14443 amperes   (an RFID standard)
# Ten Tier-2 blocks KB-wide stated no quantity at all and were pure artifacts of
# this, every one of them in `hardware/`, the tree where part numbers are densest.
#
# The discriminator is magnitude, not vocabulary: a current claim in this domain
# is written with at most three integer digits (`150mA`, `1.5A`, `20A`, `4A`),
# while a part number or a standard designator is a four-or-more digit run. So a
# bare `A` preceded by >=4 integer digits is not a current. Deliberately NOT
# applied to the other units -- `500,000,000 Hz` and `2000Ohm` are real claims.
AMPERE_DIGIT_LIMIT = 3

# P2 binary literal -- masked out before scanning so `%0000_0000` never reads
# as a percentage and `%01` never reads as a quantity.
BINARY_RE = re.compile(r"%[01_]+")
HEX_RE = re.compile(r"\$[0-9A-Fa-f_]+")
# A Unicode code point is a code point, not a current: `unicode: "U+221A"` (the
# SQUARE ROOT sign) read as 221 amperes. Same masking treatment as $hex (F-351).
CODEPOINT_RE = re.compile(r"U\+[0-9A-Fa-f]+")

# A quantity inside an EXAMPLE is a chosen parameter, not a claim about the
# silicon. `WAITX ##25_000_000` and `_clkfreq = 180 MHz` are the author picking
# numbers for a demo; nobody needs to cite their own example. Flagging them
# buried the real findings under example code, so code regions are skipped.
#
# The trailing `(#.*)?` is not cosmetic. `runnable_code:` is IN this vocabulary,
# and a single trailing YAML comment --
#     runnable_code:        # reference to the validated artifact -- NOT inlined
# -- defeated the `$` anchor, leaked the whole manifest into the claim scan, and
# produced a Tier 1 "finding" against a list of filenames. An anchor that a
# comment can defeat is an anchor that silently changes what the gate measures.
CODE_KEY_RE = re.compile(
    r"^(\s*)-?\s*(code|example|examples|runnable_code|snippet|snippets|usage|"
    r"spin2|pasm2|listing|sample|demo)\s*:\s*[|>]?\s*(#.*)?$", re.IGNORECASE)

# ...but a fixed vocabulary of THIRTEEN key names cannot be the test for "is this
# region code". The same example body is skipped when it is called `example:` and
# scanned when it is called `setup_example:`, `implementation:`, `wrong:`, or
# `measurement_time:` -- all of which are real keys in this KB holding real PASM2.
# The structural signal is the block-scalar indicator plus the CONTENT, not the
# name: a `|` region carrying a Spin2/PASM2 apostrophe-comment or a PUB/PRI
# declaration is code, whatever its key is called.
#
# Deliberately NOT "every block scalar is code": prose lives in `|` regions too
# (`description: |` in pin-power-domains.yaml states 300 mA per LDO), and
# blanking those wholesale would turn this gate off by stealth.
BLOCK_SCALAR_RE = re.compile(r"^(\s*)-?\s*[\w.-]+\s*:\s*[|>][-+0-9]*\s*(#.*)?$")
CODE_MARKER_RE = re.compile(r"^\s*(?:'|(?:PUB|PRI)\s+\w)")

# ...and a block scalar is not the only way this KB stores an example. F-335(c):
# `language/pasm2/waitx.yaml` keeps its PASM2 in a DOUBLE-QUOTED scalar with
# literal `\n` escapes --
#     code: "' HUB75 panel driver clock generation\nrgb_clock_cycle\n  ..."
# -- so BLOCK_SCALAR_RE never matched, the region was never stripped, and the
# gate read FOUR quantities out of PASM2 COMMENTS (`' For 1kHz PWM at 200MHz
# clock:`, `' 100us @ 200MHz`). Those are the demo's chosen parameters, which
# this tool's own header says it exists to skip.
#
# Note the key here IS in CODE_KEY_RE's vocabulary (`code:`) and that did not
# help: CODE_KEY_RE requires the VALUE to be empty or a block indicator. The
# lesson is the one already learned above -- the shape of the value decides, not
# the name of the key -- applied to the other value shape.
QUOTED_SCALAR_RE = re.compile(r'^(\s*)-?\s*[\w.-]+\s*:\s*"')

# An INLINE attribution is a citation (`inline_cite`, judged per line by the same
# acceptance rule as a cite key). A board revision alone (`Rev B`) is the board's
# own identity, not a document reference -- it never makes a line a citation.

# ---------------------------------------------------------------------------
# A CITATION POINTS **AT** A SOURCE FOR THE CLAIM. THREE THINGS POINT AWAY.
#
# F-334 patched two of them (a board revision, a power supply) and F-335 then
# found three more (a deferral, a slug, a missing key spelling). That is the
# signal: every one of these detectors matched on THE PRESENCE OF A TOKEN and
# never on whether the sentence attributes the block to a document. Patching the
# sixth instance would have found a seventh, so the two vetoes below are written
# against the SHAPE rather than against the instances.
#
#   DEFERRAL (F-335e) -- an instruction to go look elsewhere. `max_current_total:
#   "Check datasheet for package limits"` scored a whole block cited, which is
#   how `max_current_per_pin: "150mA"` shipped against the datasheet's stated
#   `Max. allowable current per I/O pin ±30 mA` -- FIVE TIMES the absolute
#   maximum, in the exact number a reader uses to size an LED series resistor,
#   through two purges. A deferral names a document CLASS and a topic to look
#   up; a citation names a document. So the veto fires only when the value
#   carries NO identity at all -- no proper name, no version, no date, no page
#   or line locator, no filename, no URL. `"See P2 Silicon Doc v35 §4.2"` is an
#   attribution phrased as an instruction and still counts.
#
#   SLUG (F-335d) -- `source: hub75_driver`, `source: inline_pasm2_pattern`,
#   `source: lock_validation`: a pattern-category tag, not a document. These are
#   the same shape as `source: motor_control`, which F-334's controls already
#   reject; the ones that got through did so because a bare `pasm2` / `validat`
#   token happens to sit INSIDE the identifier. A lowercase snake_case
#   identifier with no extension, no space and no version is a category name.
#   `flash_loader.spin2` (extension) and `parallax-quick-bytes` (hyphenated
#   product name) are unaffected.
#
# The slug veto matters for a second reason: it was MASKING a quantity-side
# false positive. `waitx.yaml examples` was scored cited by its slugs while the
# gate read four quantities out of PASM2 comments (F-335c) -- the block read
# clean for two wrong reasons that cancelled. Repairing either alone would have
# started failing a block that was never a real violation, so (c) and (d) land
# together or not at all.
# Matched as a PHRASE, not anchored at the start of the value. The deferral that
# shipped `150mA` was `"Check datasheet for package limits"` (anchored), but the
# same sentence reads `"Sinks 150mA per pin; see the datasheet for package
# limits."` just as easily -- and an anchor would miss it, which is how a veto
# becomes another one-off patch. `per the doc` is deliberately ABSENT: that form
# attributes, and `classify()` judges it like any other citation.
DEFERRAL_RE = re.compile(
    r"\b(?:check|see|refer\s+to|consult|look\s*up|lookup|read|review|contact|"
    r"visit|ask)\s+(?:the\s+|a\s+|an\s+|your\s+|its\s+)?(?:\w+\s+){0,2}?"
    r"(?:doc|docs|documentation|datasheet|data\s*sheet|manual|guide|spec|"
    r"specification|reference|errata|schematic)\b", re.IGNORECASE)
IDENTITY_RE = re.compile(
    r"(parallax|silicon|spin2|pasm2|pnut|obex|titus|chip\s+gracey|propeller|"
    r"\bp1\b|\bp2\b|EF-\d+|\bv\d|\d{4}-\d{2}-\d{2}|\bp\.\s*\d|\blines?\s+\d|:\d+|"
    r"\.(md|ya?ml|txt|spin2|pas|pdf|docx?|csv|py|json)\b|https?://)", re.IGNORECASE)
SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")


def points_away(value):
    """True when the text points the reader ELSEWHERE instead of attributing the
    claim to a source. Shape-based, so it does not need a new case per token."""
    v = value.strip().strip('"').strip("'").strip()
    if not v:
        return True
    if SLUG_RE.match(v):
        return True
    return bool(DEFERRAL_RE.search(v)) and not bool(IDENTITY_RE.search(v))


# ---------------------------------------------------------------------------
# THE ACCEPTANCE RULE («#412», S-393). A citation names an official Parallax
# document, an accepted EF record, or a CP record -- nothing we wrote.
#
# CANONICAL_TITLES is READ OFF THE DOCUMENTS, not remembered and not taken from the
# ingestion dashboard's row names (the first cut of this table did that and
# rejected the documents' own printed titles -- «#412» correction, 2026-10-09).
# Scope: the Parallax-authored sources in engineering/ingestion/README.md. Left OUT
# on purpose: Smart Pins (Titus), chip-gracey-clarifications, p2-qa-spreadsheet,
# p2docs-github-io (community / upstream leads); pnut-ts-pasm-ref,
# iron-sheep-compiler, quick-bytes-code (not Parallax documents); the TAQOZ Bit
# Bashers Guide (Peter Jakacki); p2-hub75-adapter (manufacturer is not Parallax);
# the AK5704 datasheet (third party). Parallax's published SOURCE LISTINGS (the
# Spin2 interpreter, the Spin2 debugger, the ROM booter, the flash loader) ARE
# citable since Stephen's ruling of 2026-10-10, pinned to their edition -- they
# are the rows at the END of this table, each marked in LISTING_EDITION_RE.
# Codenames ("Silicon Doc", "Blue Book") are NOT titles and are refused.
#
# Row = (key, [printed title forms], edition form as printed, paginated PDF?,
# provenance). The FIRST form is the canonical one a citation should use. Further
# forms are ones the document ITSELF prints (a running footer/header) or, for the
# DOCX-primary Parallax publications, the DOCX filename the source folder holds.
# Nothing is invented. A part-number suffix is part of the title because the
# cover/footer prints it. Provenance paths are under engineering/ingestion/sources/
# and "pdftotext p1" means `pdftotext -l 1 -layout <pdf>` of the PDF named.
CANONICAL_TITLES = [
    ("silicon-doc",
     ["Parallax Propeller 2 Documentation", "Propeller 2 Documentation", "P2 Documentation"],
     "v35 (Rev B/C silicon), 2021-05-18", False,
     "silicon-doc/silicon-doc-text.txt:3-6 (cover); `Parallax Propeller 2 Documentation v35 - "
     "Rev B_C Silicon.docx` and `P2 Documentation v35 - Rev B_C Silicon-Part1of5.pdf` (filenames)"),
    ("spin2-v55",
     ["Parallax Propeller 2 Spin2 Language Documentation", "Parallax Spin2 Documentation",
      "Spin2 Language Documentation"],
     "v55, 2026-05-07", False,
     "spin2-v55/spin2-v55-text.txt:1-4 (cover: `Parallax Propeller 2 / Spin2 Language "
     "Documentation`, `v 55`); `Parallax Spin2 Documentation v55.docx` (filename)"),
    ("pasm2-manual",
     ["Propeller 2 Assembly Language (PASM2) Manual", "Propeller 2 Assembly Language Manual"],
     "Nov 1, 2022 Release (2022/11/01)", True,
     "pasm2-manual/P2-Assembly-Language-PASM2-Manual-Draft-221117.pdf pdftotext p1 (cover and "
     "footer `Propeller 2 Assembly Language Manual   Page 1`); `Propeller 2 Assembly Language "
     "(PASM2) Manual - 20221101.docx` (filename)"),
    ("p2-datasheet",
     ["Parallax Propeller 2 (P2X8C4M64P) Datasheet", "Propeller 2 (P2X8C4M64P) Datasheet"],
     "Release November 1, 2022 (2022/11/01)", True,
     "p2-datasheet/p2-datasheet-text.txt:1 and :14 (cover), :64 (footer `Parallax Propeller 2 "
     "(P2X8C4M64P) Datasheet   Page 1`)"),
    ("p2-hardware-manual",
     ["Propeller 2 P2X8C4M64P Hardware Manual", "Propeller 2 Hardware Manual"],
     "Nov 1, 2022 Release", True,
     "p2-hardware-manual/p2-hardware-manual-text.txt:2-4 (cover); `Propeller 2 Hardware Manual - "
     "20221101.docx` (filename)"),
    ("p2-instructions-csv",
     ["P2 Instructions"],
     "v35 - Rev B/C Silicon", False,
     "p2-instructions-csv/`P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv` (filename; a "
     "spreadsheet -- no cover)"),
    ("p2-spec-sheet",
     ["Propeller P2X8C4M64P (P2) Multicore Microcontroller Spec Sheet"],
     "none printed on the first page", False,
     "p2-spec-sheet/p2-spec-sheet-narrative.txt:5 (title line; source PDF not held)"),
    ("p2-eval-board",
     ["Propeller 2 Eval Board Rev C (64000)", "Propeller 2 ES Evaluation Board Rev C (64000)"],
     "v2.0 29/6/2020", True,
     "p2-eval-board/p2-eval-board-text.txt:10 (cover), :52 (footer), :103 (running footer "
     "`Propeller 2 ES Evaluation Board Rev C (64000)  v2.0 29/6/2020 Page 2 of 17`)"),
    ("edge-standard-module",
     ["P2 Edge Module Rev D (#P2-EC)", "P2 Edge Module (#P2-EC)"],
     "v3.0 6/3/2022", True,
     "edge-standard-module/edge-standard-module-text.txt:9 (cover); P2-EC-Edge-Module-RevD-"
     "Product-Guide-3.0.pdf pdftotext p1 footer `P2 Edge Module (#P2-EC)  v3.0 6/3/2022 Page 1 of 13`"),
    ("edge-32mb-module",
     ["P2 Edge Module with 32MB RAM (#P2-EC32MB)", "P2 Edge Module (#P2-EC32MB)"],
     "v2.0 5/23/2022", True,
     "edge-32mb-module/P2-EC32MB-Edge-Module-Rev-B-Guide-v2.0.pdf pdftotext p1 (cover and footer "
     "`P2 Edge Module (#P2-EC32MB)  v2.0 5/23/2022 Page 1 of 13`)"),
    ("edge-breakout-board",
     ["P2 Edge Breakout Board (#64029)"],
     "v1.0 03/01/2023", True,
     "edge-breakout-board/64029-P2-Edge-Breakout-Board-Guide-20230301.pdf pdftotext p1 (cover and footer)"),
    ("edge-mini-breakout",
     ["P2 Edge Mini Breakout Board (#64019)"],
     "v1.1 11/30/2020", True,
     "edge-mini-breakout/64019-P2-Edge-MiniBreakoutBoardGuide-v1.1.pdf pdftotext p1 (cover and footer)"),
    ("edge-module-breadboard",
     ["P2 Edge Module Breadboard (#64020)"],
     "v1.2 01/07/2021", True,
     "edge-module-breadboard/64020-P2-Edge-Module-Breadboard-Product-Guide-REVB.pdf pdftotext p1 "
     "(cover and footer; the cover does not print `Rev B`)"),
    ("p2-eval-add-on-boards",
     ["P2 Eval Add-on Boards (#64006 Series)", "P2 Eval Add-on Boards"],
     "v2.0 1/12/2021", True,
     "p2-eval-add-on-boards/64006-P2-Eval-Add-on-Boards-Product-Guide.pdf pdftotext p1 (cover "
     "`P2 Eval Add-on Boards`; footer `P2 Eval Add-on Boards (#64006 Series)  v2.0 1/12/2021 Page 1 of 12`)"),
    ("p2-universal-motor-driver",
     ["Universal Motor Driver P2 Add-on Board (#64010)"],
     "v2.0 5/5/2022", True,
     "p2-universal-motor-driver/64010-UniversalMotorDriverP2AddOnGuide-RevB-v2.0.pdf pdftotext p1 "
     "(cover and footer)"),
    ("p2-microSD-addon",
     ["P2 microSD Add-on Board (#64009)", "microSD Add-on Board (#64009)"],
     "v1.0 22/02/2021", True,
     "p2-microSD-addon/64009-P2-microSD-AddOn-Guide-v1.0.pdf pdftotext p1 (cover; footer omits `P2`)"),
    ("P2-RTC-Add-on",
     ["P2 RTC Add-on (#64013)", "P2 RTC Add-on Board (#64013)"],
     "v1.0 11/29/2022", True,
     "P2-RTC-Add-on/64013-P2-RTC-Add-on-Guide-20221129.pdf pdftotext p1 (cover; footer adds `Board`)"),
    ("P2-HD-Audio-Add-on",
     ["P2 HD Audio Add-on Set (#64014)"],
     "v1.0 10/16/2022", True,
     "P2-HD-Audio-Add-on/64014-P2-HD-Audio-Add-on-Set-Guide.pdf pdftotext p1 (cover and footer)"),
    ("hyperRam-n-hyperFlash",
     ["P2-ES Eval HyperRAM/Flash Add-on (#64004-ES)", "P2-ES Eval HyperRAM_Flash Memory Board Product Guide"],
     "1.0 11/5/2019", True,
     "hyperRam-n-hyperFlash/`64004-ES P2-ES Eval HyperRAM_Flash Memory Board Product Guide.pdf` "
     "pdftotext p1 footer `P2-ES Eval HyperRAM/Flash Add-on (#64004-ES)  1.0 11/5/2019 Page 1 of 9` "
     "(the cover glyphs are garbled in the text layer; the second form is the filename)"),
    ("p2-wx-adapter",
     ["P2 WX Adapter Add-on Board (#64007)"],
     "v1.0 11/12/2020", True,
     "p2-wx-adapter/64007-P2-WX-Adapter-Guide-v1.0.pdf pdftotext p1 (cover and footer)"),
    ("parallax-wx-wifi",
     ["Parallax WX ESP8266 Wi-Fi Modules", "ESP8266 Wi-Fi Module (#32420)"],
     "v1.0 05/12/2016", True,
     "parallax-wx-wifi/32420-Parallax-WX-WiFi-Module-Guide-v1.0.pdf pdftotext p1 (cover; footer "
     "`ESP8266 Wi-Fi Module (#32420)  v1.0 05/12/2016 Page 1 of 12`)"),
    ("propplug-rev-e",
     ["Prop Plug (#32201) Rev E"],
     "v3.0 2/03/2021", True,
     "propplug-rev-e/32201-PropPlugRev-Guide-RevE.pdf pdftotext p1 (cover and footer)"),
    ("p2-click-adapter",
     ["P2 mikroBUS Adapter"],
     "Part Number 64008, Revision A", False,
     "p2-click-adapter/p2-click-adapter-text.txt:6, :11, :13 (the schematic's title block; a "
     "one-page schematic, so no page number)"),
    # --- PUBLISHED SOURCE LISTINGS (Stephen, 2026-10-10). For these rows the edition
    # field is the CURRENTLY INGESTED edition, written as a citation writes it -- the
    # staleness check reads the current edition from HERE and nowhere else. When a
    # newer edition is ingested, change the edition field of its row: every citation
    # of the old edition then fails STALE_EDITION until it is re-checked. Provenance
    # paths are under engineering/ingestion/; titles are the listing's own banner.
    ("spin2-interpreter",
     ["Spin2 Interpreter"],
     "v55 (2026.05.07)", False,
     "external-inputs/source-code/spin-interpreter/v55/Spin2_interpreter.spin2:4 (banner "
     "`Spin2 Interpreter - v55 - 2026.05.07`). Editions held: v51 (`v51 - 2025.04.02`, "
     "spin-interpreter/v51/:4) and v55; v55 is current (DOCUMENT-LINEAGE.md, Source-code "
     "inputs). Stephen's ruling writes it `Parallax Spin2 Interpreter v55 (2026.05.07)`, "
     "which contains the printed title"),
    ("spin2-debugger",
     ["Spin2/PASM Debugger"],
     "v51 (2025.04.02)", False,
     "external-inputs/source-code/spin-debugger/v51/Spin2_debugger.spin2:2 (banner "
     "`Spin2/PASM Debugger - v51 - 2025.04.02`). The only edition held; current for the v55 "
     "toolchain (DOCUMENT-LINEAGE.md: PNut-TS v1.55.8 embeds exactly this v51 image)"),
    ("rom-booter",
     ["Propeller 2 ROM Booter"],
     "v33_01j", False,
     "sources/rom-booter/rom_booter_v33_01j.lst:118 (banner `Propeller 2 ROM Booter`) and "
     ":87-93 (revision history ending `v33_01a .. j  use \"G\" for Prop2 silicon v2`), :131 "
     "(`ver = \"G\" 'Prop2 Silicon v2`). The SILICON listing. Its banner still prints "
     "`5/28/2018 - v32i`, as does ROM_Booter.lst:113 -- the FPGA build (`ver = \"A\"`, :118), an "
     "EARLIER revision whose history ends at v141 (:84; F-421, F-555) -- so the banner version "
     "does not identify the silicon ROM and v33_01j, the listing's last revision record, is the "
     "edition a citation names"),
    ("flash-loader",
     ["SPI Flash Programmer and Boot Loader"],
     "v51", False,
     "sources/flash-loader/flash_loader.spin2:1 (header `*** SPI FLASH PROGRAMMER AND BOOT "
     "LOADER`). The listing prints NO edition; v51 is the Spin2/PNut distribution it was taken "
     "from (external-inputs/source-code/spin-flash-loader/v51/flash_loader.spin2, byte-identical "
     "to the sources/ copy by `diff`, 2026-10-10). The only edition held"),
]
_TITLES = [(row[0], [re.sub(r"\s+", " ", t.lower()) for t in row[1]], row[3])
           for row in CANONICAL_TITLES]

# How a citation writes an EDITION of each source listing, as a pattern whose group 1
# is the edition token. Membership in this map is what makes a CANONICAL_TITLES row a
# LISTING: for those rows the edition must FOLLOW the title (`<title> <edition>, ...`)
# and must equal the token in the row's edition field (the current edition).
LISTING_EDITION_RE = {
    "spin2-interpreter": re.compile(r"v\s?(\d+)\b"),
    "spin2-debugger": re.compile(r"v\s?(\d+)\b"),
    "rom-booter": re.compile(r"v(\d+(?:_\d+)?[a-z]?)\b"),
    "flash-loader": re.compile(r"v\s?(\d+)\b"),
}
_LISTING_CURRENT = {row[0]: LISTING_EDITION_RE[row[0]].match(row[2].lower()).group(1)
                    for row in CANONICAL_TITLES if row[0] in LISTING_EDITION_RE}


def listing_edition_class(key, nv, end):
    """Judge the edition written right AFTER a listing title that ends at `end` in the
    normalised value `nv`. Returns None (current edition), "STALE_EDITION" (some other
    edition) or "NO_EDITION" (none written)."""
    m = LISTING_EDITION_RE[key].match(nv[end:].lstrip(" -("))
    if not m:
        return "NO_EDITION"
    return None if m.group(1) == _LISTING_CURRENT[key] else "STALE_EDITION"


def _norm(s):
    """Case-insensitive, whitespace-normalised, dash-normalised."""
    return re.sub(r"\s+", " ", s.replace("–", "-").replace("—", "-").lower())


# After a title there must be an EDITION (v35, 2022/11/01, Rev C, a month-year) or
# a SECTION (a comma, then a heading).
EDITION_RE = re.compile(
    r"(\bv\s?\d+(?:\.\d+)?\b|\b\d{4}[-/]\d{2}[-/]\d{2}\b|\brev\s*[a-z]\b|"
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[ -]\d{4}\b|\b(?:19|20)\d{2}\b)",
    re.IGNORECASE)
SECTION_RE = re.compile(r",\s*\S")
PAGE_RE = re.compile(r"\bpp?\.\s*\d", re.IGNORECASE)

# What a citation must NOT carry, whatever else it names.
FORBIDDEN = [
    ("BATCH_LABEL", re.compile(r"\bparallax-quick-bytes\b|\bPNUT_TS_v[\w.-]*", re.IGNORECASE)),
    ("EXTRACTION_PATH", re.compile(
        r"[\w.-]*-text\.txt|\bpart\d+-[\w-]+\.txt|\.txt\b|\bengineering/|\bdeliverables/|"
        r"\bingestion/|\.csv\b|\.docx\b", re.IGNORECASE)),
    ("REGISTER_PATH", re.compile(
        r"SOURCE-ERRATA|P2KB-CORRECTION|P2-EMPIRICAL-FINDINGS\.md|COMPILE-PROOFS\.md|"
        r"\bcomplete-[\w-]+\.md|\.md\b|click-adapter\s+netlist|\bP2\s+Errata\b",
        re.IGNORECASE)),
    # A pointer at another KB file is our own page, not a Parallax document.
    ("KB_PATH", re.compile(r"\.ya?ml\b", re.IGNORECASE)),
    ("LINE_LOCATOR", re.compile(
        r"\blines?\s+\d|(?<=[A-Za-z_])\:\d{1,5}\b|(?:^|[\s,(])\:\d{2,5}\b", re.IGNORECASE)),
]
ID_RE = re.compile(r"\b(?:EF|CP|XF)-\d+\b")
_CLASS_ORDER = ["BATCH_LABEL", "EXTRACTION_PATH", "REGISTER_PATH", "KB_PATH", "LINE_LOCATOR",
                "BAD_ID", "STALE_EDITION", "NO_EDITION", "NO_PAGE", "BOOKKEEPING",
                "NO_PARALLAX_DOC"]

EF_LEDGER = REPO / "engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md"
CP_REGISTER = REPO / "engineering/ingestion/external-sources/compiler-verification/COMPILE-PROOFS.md"
# XF = the external-project hardware tier, equal in standing to EF.
XF_LEDGER = REPO / "engineering/ingestion/external-sources/hardware-verification/EXTERNAL-HARDWARE-FINDINGS.md"


def _ledger_ids(path, prefix):
    """The ids that EXIST as `### PREFIX-NNN` headings, or None if the register is
    missing -- a missing register must never read as 'no ids are wrong'."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    return set(re.findall(rf"^### ({prefix}-\d{{3}})\b", text, re.M))


# An OBEX object is cited by its catalog ID: `OBEX 2842 (Full Duplex Serial)`. The
# catalog stores one `<id>.yaml` per object, so the id EXISTS when that file does.
# The bare word OBEX, with no id, names no object and is not a citation. A catalog
# that is missing reads as None -- never as "no id is wrong".
OBEX_CATALOG = KB_ROOT / "community" / "obex" / "objects"
OBEX_ID_RE = re.compile(r"\bOBEX\s+#?(\d+)\b", re.IGNORECASE)


def _obex_ids(path):
    try:
        return {p.stem for p in path.glob("*.yaml") if p.stem.isdigit()} or None
    except OSError:
        return None


OBEX_IDS = _obex_ids(OBEX_CATALOG)

EF_IDS = _ledger_ids(EF_LEDGER, "EF")
CP_IDS = _ledger_ids(CP_REGISTER, "CP")
XF_IDS = _ledger_ids(XF_LEDGER, "XF")


def classify(value):
    """Judge one citation VALUE by the acceptance rule. Returns (ok, classes)."""
    v = value.strip().strip('"').strip("'").strip()
    classes = [name for name, rx in FORBIDDEN if rx.search(v)]
    good = False
    for m in ID_RE.finditer(v):
        i = m.group(0)
        known = (EF_IDS if i.startswith("EF-") else CP_IDS if i.startswith("CP-")
                 else XF_IDS if i.startswith("XF-") else set()) or set()
        if i in known:
            good = True
        elif "BAD_ID" not in classes:
            classes.append("BAD_ID")
    for m in OBEX_ID_RE.finditer(v):
        if m.group(1) in (OBEX_IDS or set()):
            good = True
        elif "BAD_ID" not in classes:
            classes.append("BAD_ID")
    nv = _norm(v)
    for key, forms, paginated in _TITLES:
        if key in LISTING_EDITION_RE:
            # A source listing: EVERY occurrence of its title must carry the current
            # edition right after it. A section alone does not do -- the routine it
            # names may differ between editions.
            for f in forms:
                at = nv.find(f)
                while at >= 0:
                    cls = listing_edition_class(key, nv, at + len(f))
                    if cls is None:
                        good = True
                    elif cls not in classes:
                        classes.append(cls)
                    at = nv.find(f, at + 1)
            continue
        end = max((nv.find(f) + len(f) for f in forms if f in nv), default=-1)
        if end < 0:
            continue
        if not (EDITION_RE.search(nv) or SECTION_RE.search(nv[end:])):
            if "NO_EDITION" not in classes:
                classes.append("NO_EDITION")
        elif paginated and not PAGE_RE.search(v):
            if "NO_PAGE" not in classes:
                classes.append("NO_PAGE")
        else:
            good = True
    if not good and not classes:
        classes.append("BOOKKEEPING" if re.fullmatch(r"[\w-]+", v) else "NO_PARALLAX_DOC")
    return (good and not classes), classes


def primary_class(classes):
    return next((c for c in _CLASS_ORDER if c in classes), classes[0] if classes else "")


@functools.lru_cache(maxsize=None)
def is_citation(value):
    """A cite key's VALUE counts only when it passes the acceptance rule AND
    attributes the claim rather than deferring it. Pure (the EF/CP id sets are
    fixed at import), so the per-line repeats across file and block scans are cached."""
    v = value.strip().strip('"').strip("'").strip()
    if points_away(v):
        return False
    return classify(v)[0]


def inline_cite(text):
    """An inline attribution, judged PER LINE by the SAME acceptance rule -- a
    deferral cannot silence the line it sits on, and neither can the bare word
    `datasheet` or `Silicon Doc` (the retired keyword vocabulary), which named no
    document we are willing to cite."""
    for ln in text.split("\n"):
        seg = ln.split(":", 1)[1] if ":" in ln else ln
        if is_citation(seg):
            return True
    return False


def _line_value(ln):
    """The value part of one nested body line: `key: value`, `- value`, or text."""
    s = ln.strip()
    if s.startswith("- "):
        s = s[2:].strip()
    m = re.match(r"^[\w.-]+\s*:\s+(.*)$", s)
    return m.group(1) if m else s


def full_value(lines, i, indent, value):
    """A plain or quoted scalar may continue on the lines below (indented deeper
    than its key). A citation is judged WHOLE: `P2 Eval Add-on Boards ... v2.0
    (Parallax Inc.,` on one line and `2020), Board A, p.5` on the next is one
    citation, not a title with no page."""
    cont = [ln.strip() for ln in _nested_body(lines, i, indent).split("\n") if ln.strip()]
    if cont and not any(re.match(r"^[\w.-]+\s*:(\s|$)", c) or c.startswith("- ") for c in cont):
        return " ".join([value] + cont)
    return value


def citation_values(lines):
    """Every claimed citation value: (lineno, key, value). A structure-valued cite
    key (`sources:` + a list, `documentation:` -> `primary:`) yields its body line
    by line. Only FLAG_KEYS are judged -- see their comment."""
    for i, line in enumerate(lines):
        m = CITE_KEY_RE.match(line)
        if not m or m.group(2).lower() not in FLAG_KEYS:
            continue
        key, value = m.group(2).lower(), m.group(3).strip()
        if value in _STRUCTURE_VALUE:
            body = _nested_body(lines, i, len(m.group(1))).split("\n")
            for k, ln in enumerate(body):
                if ln.strip():
                    yield i + 2 + k, key, _line_value(ln)
        else:
            yield i + 1, key, full_value(lines, i, len(m.group(1)), value)


def claimed(key, value):
    """Is this value an attempt at a citation (so the rule judges it)? Any value
    under `documentation_source`; elsewhere `source:` is overloaded (a power
    supply, a pattern category), so only a value that LOOKS like a citation or
    carries a forbidden token is judged."""
    v = value.strip().strip('"').strip("'").strip()
    if not v:
        return False
    if key == "documentation_source":
        return True
    if SLUG_RE.match(v):
        return False
    nv = _norm(v)
    if any(f in nv for _, forms, _p in _TITLES for f in forms):
        return True
    return (bool(CITE_VALUE_RE.search(v)) or bool(ID_RE.search(v))
            or any(rx.search(v) for _, rx in FORBIDDEN))


CATALOG_DIR = "community/quick-bytes"
CATALOG_URL_RE = re.compile(r"^\s*url:\s*[\"']?https?://(?:www\.)?parallax\.com/\S+", re.MULTILINE)


def is_catalog(rel):
    return CATALOG_DIR in rel.as_posix()


def catalog_cited(lines):
    """Q5: a catalog entry is cited by its parallax.com `url:`."""
    return bool(CATALOG_URL_RE.search("\n".join(lines)))


# The Tier-2 switch («#412», S-308b). Tier 2 (a file that cites nothing anywhere)
# stays ADVISORY until S-295..S-307 are applied in the architecture/spin2 area
# tasks. SWITCH-ON IS OWED TO THE CITATIONS TASK: flip this to True (or pass
# --tier2-blocking) and record it there.
TIER2_BLOCKING = False

# S-308a: example blocks are the author's chosen parameters, exempt by LOCATION.
# NOT anti_patterns / common_patterns -- those state claims.
EXAMPLE_BLOCK_RE = re.compile(
    r"^(?:(?:\w+_)?examples?|quick_example|complete_example|usage_example|worked_escape)$")


def is_example_block(name, body_lines):
    if EXAMPLE_BLOCK_RE.match(name):
        return True
    if any(re.match(r"^\s*authority_tier\s*:\s*EXAMPLE\b", ln) for ln in body_lines):
        return True
    content = [ln for ln in body_lines[1:] if ln.strip()]
    return name in ("wrong", "correct") and len(content) <= 1


def _nested_body(lines, i, indent):
    """The lines below `i` that belong to it -- the body of a key whose value is
    a list or a map or a block scalar."""
    out, j = [], i + 1
    while j < len(lines):
        bare = lines[j].strip()
        if bare and (len(lines[j]) - len(lines[j].lstrip())) <= indent:
            break
        out.append(lines[j])
        j += 1
    return "\n".join(out)


def cites_in(lines, lo=0, hi=None):
    """True when some line in [lo, hi) is a citation: a cite KEY whose VALUE
    names a document or an empirical record. The value test is the whole point
    -- `source: External 5V power supply (required)` is a power source, and
    reading it as a citation is what let an uncited twelve-quantity block pass."""
    if hi is None:
        hi = len(lines)
    for i in range(lo, min(hi, len(lines))):
        m = CITE_KEY_RE.match(lines[i])
        if not m:
            continue
        value = m.group(3).strip()
        if value in _STRUCTURE_VALUE:
            value = _nested_body(lines, i, len(m.group(1)))
            # A key that introduces STRUCTURE is tested line by line: its body
            # holds one document per line (`documentation:` -> `primary: "..."`,
            # `sources:` -> a list), and judging the whole body as one string
            # would let a deferral on one line be rescued by an identity token
            # on another.
            if any(is_citation(_line_value(ln)) for ln in value.split("\n") if ln.strip()):
                return True
            continue
        if is_citation(full_value(lines, i, len(m.group(1)), value)):
            return True
    return False


def top_level_blocks(lines):
    """Split a YAML file into top-level key blocks. Line-based on purpose:
    these files must be auditable even when a block is malformed."""
    blocks, name, start = [], None, 0
    for i, line in enumerate(lines):
        if re.match(r"^[A-Za-z_][\w-]*\s*:", line):
            if name is not None:
                blocks.append((name, start, i))
            name, start = line.split(":", 1)[0].strip(), i
    if name is not None:
        blocks.append((name, start, len(lines)))
    return blocks


def _scalar_code_regions(lines):
    """Indices of block-scalar bodies whose CONTENT is code, regardless of the
    key's name. Answers the question the vocabulary list only approximates."""
    blank = set()
    i, n = 0, len(lines)
    while i < n:
        m = BLOCK_SCALAR_RE.match(lines[i])
        if not m:
            i += 1
            continue
        indent, j = len(m.group(1)), i + 1
        while j < n:
            bare = lines[j].strip()
            if bare and (len(lines[j]) - len(lines[j].lstrip())) <= indent:
                break
            j += 1
        if any(CODE_MARKER_RE.match(lines[k]) for k in range(i + 1, j)):
            blank.update(range(i, j))
        i = j
    return blank


def _quoted_scalar_regions(lines):
    """Indices of DOUBLE-QUOTED scalar bodies whose content is code (F-335c).

    The same question `_scalar_code_regions` asks of a `|` block, asked of the
    other way this KB stores an example: one quoted scalar carrying literal `\\n`
    escapes. The scalar is split on those escapes and the resulting logical lines
    are tested with the SAME `CODE_MARKER_RE` -- so a quoted region is judged
    code by exactly the criterion a block region is, never by its key's name."""
    blank = set()
    i, n = 0, len(lines)
    while i < n:
        m = QUOTED_SCALAR_RE.match(lines[i])
        if not m:
            i += 1
            continue
        # Walk to the closing quote, honouring backslash escapes. A trailing
        # backslash at end-of-line escapes the line break (YAML's continuation),
        # so escape state does not survive into the next line's first character.
        body, end, esc = [], None, False
        for j in range(i, n):
            seg = lines[j][m.end(0):] if j == i else lines[j]
            for k, ch in enumerate(seg):
                if esc:
                    esc = False
                    continue
                if ch == "\\":
                    esc = True
                    continue
                if ch == '"':
                    body.append(seg[:k])
                    end = j
                    break
            if end is not None:
                break
            body.append(seg)
            esc = False
        if end is None:                  # unterminated -- leave the region alone
            i += 1
            continue
        joined = "".join(body)
        # A LITERAL `\n` ESCAPE IS REQUIRED, and it is not a formality. Without
        # it this rule blanked `p2an003-dac-analog-signal-generation.yaml:118`,
        # a `source_statement:` holding a QUOTED SENTENCE that opens with an
        # apostrophe -- which `CODE_MARKER_RE` reads as a Spin2 comment. That is
        # prose, and blanking it is the "turn the gate off by stealth" failure
        # this file's block-scalar rule already warns about, reproduced in the
        # other value shape. A stored code example is MULTI-LINE by construction;
        # a quoted sentence is not.
        logical = re.split(r"\\n", joined)
        if len(logical) > 1 and any(CODE_MARKER_RE.match(x.replace("\\", ""))
                                    for x in logical):
            blank.update(range(i, end + 1))
        i = end + 1
    return blank


def strip_yaml_comment(line):
    """Drop a YAML `#` comment, respecting quotes. A comment is invisible to
    every consumer of this KB -- the MCP and every reader see PARSED yaml, where
    comments do not exist -- so a quantity that lives only in a comment is not a
    claim the knowledge base ships. Scanning them produced a Tier 1 violation
    against a pure list of cross-reference paths, whose only `dB` was in a
    trailing annotation.

    APPLIED TO THE QUANTITY SCAN ONLY, and the asymmetry is deliberate. A
    comment cannot be a shipped CLAIM (no consumer sees it), but it is a
    perfectly good record of where content CAME FROM, which is the question the
    citation half asks -- and it is asked of the repository, not of the parse.
    Stripping comments from both halves at once was tried and immediately
    produced three fresh Tier 1 violations against blocks that were correctly
    attributed in a comment: `smart-pin-11011-usb-host-device.yaml:21` (cited
    `# Silicon Doc p2-documentation.txt:8886-9006`), `addon-serial-device.yaml:82`
    and `edge-32mb-module.yaml:445`. A gate that fires on correctly-attributed
    content teaches people the gate is wrong."""
    q = None
    for i, ch in enumerate(line):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    return line


def strip_code_regions(lines):
    """Drop example bodies in either scalar shape. A demo's chosen numbers are
    not claims about the silicon, and nobody cites their own example."""
    scalar_code = _scalar_code_regions(lines) | _quoted_scalar_regions(lines)
    out, skip_indent = [], None
    for idx, line in enumerate(lines):
        if idx in scalar_code:
            out.append("")
            continue
        if skip_indent is not None:
            bare = line.strip()
            indent = len(line) - len(line.lstrip())
            if bare and indent <= skip_indent:
                skip_indent = None
            else:
                out.append("")
                continue
        m = CODE_KEY_RE.match(line)
        if m:
            skip_indent = len(m.group(1))
            out.append("")
            continue
        out.append(line)
    return out


def quantities_in(text):
    """The physical quantities a region states, as unit tokens."""
    decommented = "\n".join(strip_yaml_comment(ln) for ln in text.split("\n"))
    masked = CODEPOINT_RE.sub(" ", HEX_RE.sub(" ", BINARY_RE.sub(" ", decommented)))
    out = []
    for num, unit in QTY_RE.findall(masked):
        if unit == "A" and len(num.split(".")[0].replace(",", "")) > AMPERE_DIGIT_LIMIT:
            continue                     # a part number or a standard designator
        out.append(unit)
    return out


def audit():
    if not KB_ROOT.is_dir() or EF_IDS is None or CP_IDS is None or OBEX_IDS is None:
        return None, None, 0, None
    tier1, tier2, scanned = [], [], 0
    bad = []        # (class, "rel:line", key, excerpt) -- BAD_CITATION, blocking
    for path in sorted(KB_ROOT.rglob("*.yaml")):
        rel = path.relative_to(REPO)
        if "community/obex/objects" in rel.as_posix():
            continue                      # S-308c: third-party objects, not our claims
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        scanned += 1
        catalog = is_catalog(rel)
        cat_url = catalog and catalog_cited(lines)
        if catalog and not cat_url:
            bad.append(("NO_CATALOG_URL", f"{rel}:1", "url",
                        "catalog entry has no parallax.com `url:` (Q5)"))
        for lineno, key, value in citation_values(lines):
            if not claimed(key, value):
                continue
            ok, classes = classify(value)
            if not ok:
                bad.append((primary_class(classes), f"{rel}:{lineno}", key,
                            value.strip()[:100]))
        file_cites = cat_url or cites_in(lines) or inline_cite("\n".join(lines))
        prose = strip_code_regions(lines)

        for name, start, end in top_level_blocks(lines):
            if is_example_block(name, lines[start:end]):
                continue
            body = "\n".join(prose[start:end])
            qty = quantities_in(body)
            if not qty:
                continue
            block_cites = cat_url or cites_in(lines, start, end) or inline_cite(body)
            if block_cites:
                continue
            units = sorted({u for u in qty})
            detail = (f"{rel}:{start + 1} block `{name}` states "
                      f"{len(qty)} quantit{'y' if len(qty) == 1 else 'ies'} "
                      f"({', '.join(units[:6])}) with no source")
            if file_cites:
                tier1.append((name, f"{detail}; this file DOES cite elsewhere "
                                    f"— its own other sections are the control"))
            else:
                tier2.append((name, f"{detail}; file cites nothing anywhere"))
    return tier1, tier2, scanned, bad


def negative_control():
    """A check that cannot fail has not been verified, it has been run."""
    print("NEGATIVE CONTROL -- proving the tool discriminates\n")
    cases = [
        ("the F-327 shape (mA + ohms, uncited)", 'mode: "1.5mA"\nimpedance: "~2000Ohm"', True),
        ("slew claim (ns, uncited)", 'rise_fall: "< 2ns with strong drive"', True),
        ("P2 binary literal — MUST NOT fire", 'bit_pattern: "%0000_0000_000_0000000101000_00_00000_0"', False),
        ("pin numbers and counts — MUST NOT fire", 'pins: 64\nrange: "0-63"\ncogs: 8', False),
        ("hex constant — MUST NOT fire", 'value: "$0000_2800"', False),
        # F-351: three things that are not amperes. Ten Tier-2 blocks stated no
        # quantity at all and were pure artifacts of the bare `A` unit.
        ("Parallax part number `64006A` — MUST NOT fire", 'part_number: "64006A"', False),
        ("Unicode code point `U+221A` — MUST NOT fire", 'unicode: "U+221A"', False),
        ("ISO designator `14443 A` — MUST NOT fire", 'std: "ISO/IEC 14443 A/MIFARE"', False),
        ("a REAL bare-ampere current — MUST STILL FIRE",
         'current_per_panel: "1.5A typical, 4A peak"', True),
        ("a REAL three-digit ampere — MUST STILL FIRE", 'inrush: "100A for 2ms"', True),
        # The rail-name decision, recorded as a control so it cannot flip in
        # silence: a voltage designator in a hardware file is a CLAIM about a
        # physical board and stays in scope. Deciding otherwise would disarm the
        # gate on `vdd_max` / `VOH_min` — the exact F-348 shape that shipped a
        # figure five times the datasheet's absolute maximum.
        ("a rail NAME is still a claim — MUST STILL FIRE", 'label: "5V"', True),
        ("an absolute-maximum rating — MUST STILL FIRE", 'vdd_max: "3.6V"', True),
    ]
    ok = True
    for label, text, want in cases:
        fired = bool(quantities_in(text))
        good = fired == want
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label}: fired={fired} expected={want}")

    # Region cases -- these exercise strip_code_regions, which decides WHAT is
    # scanned at all. Each MUST-NOT-FIRE case here is a real Tier 1 false
    # positive this tool produced; each MUST-FIRE case is the control proving
    # the strippers did not simply switch the gate off.
    print()
    region_cases = [
        ("PASM2 in a non-vocabulary block scalar (`setup_example:`) — MUST NOT fire",
         ["setup_example: |", "  ' Setup 1ms timer event",
          "  ADDCT1  timeout, ##160_000  ' 1ms at 160MHz"], False),
        ("Spin2 in `wrong:` — MUST NOT fire",
         ["wrong: |", "  ' Drifts", "  REPEAT", "    waitms(100)    ' 100ms AFTER work"], False),
        ("code key with a trailing YAML comment — MUST NOT fire",
         ["runnable_code:   # NOT inlined", "  note: \"read above 3.3 V\"" ], False),
        ("quantity only in a trailing YAML comment — MUST NOT fire",
         ["cross_references:", "  - architecture/x.yaml   # dither @ -48dB"], False),
        ("PROSE block scalar stating a real quantity — MUST STILL FIRE",
         ["description: |", "  Eight LDO regulators, 300 mA each, one per header group."], True),
        ("the F-327 encoding block (a `|` region that is NOT code) — MUST STILL FIRE",
         ["encoding: |", "  %00 = 1.5mA (impedance ~2000Ohm)"], True),
        ("a `#` inside a quoted value is not a comment — MUST STILL FIRE",
         ['note: "clamp #1 draws 10 mA"'], True),
        # F-335(c): the OTHER value shape. A code example stored as a quoted
        # scalar with literal `\n` escapes was invisible to the region stripper.
        ("PASM2 in a QUOTED scalar with `\\n` escapes — MUST NOT fire",
         ['code: "\' HUB75 clock gen\\nrgb_cycle\\n  waitx #2   \' Hold 100us @ 200MHz\\n"'],
         False),
        # ...and the guard that keeps that rule from disarming the gate: a quoted
        # SENTENCE opening with an apostrophe is prose, not a Spin2 comment.
        ("a quoted sentence that OPENS with an apostrophe — MUST STILL FIRE",
         ['source_statement: "\'PWM dithering gives better range at 200MHz\'"'], True),
    ]
    for label, lines, want in region_cases:
        fired = bool(quantities_in("\n".join(strip_code_regions(lines))))
        good = fired == want
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label}: fired={fired} expected={want}")

    # Citation cases -- these exercise the OTHER half of the gate, the half
    # F-334 proved was broken. Every case carries a real quantity, so nothing
    # here can pass by having nothing to find: what is being measured is purely
    # whether the block is judged CITED. `fired` = the gate would report it.
    #
    # MUST-FIRE means "this is not a citation, so the claim is uncited".
    # MUST-NOT-FIRE means "this IS a citation and must still be recognised" --
    # one per spelling the corpus actually uses, which is what stops the value
    # test from being tightened into a gate that fires on correctly-sourced work.
    print()
    cite_cases = [
        ("board revision `Rev B` is the board's identity, not a document — MUST FIRE",
         ['specifications:',
          '  electrical:',
          '    current_per_port: "Up to 500mA continuous"',
          '    power_configuration: "5V shunt jumper required on P2-ES Eval Board Rev B"'], True),
        ("silicon revision `Rev B/C` in prose is not a document — MUST FIRE",
         ['description: |',
          '  The counter is free-running (Rev B/C silicon) and wraps around',
          '  approximately every 21 seconds at 200MHz.'], True),
        ("`source:` naming a POWER supply is not a citation — MUST FIRE",
         ['power_requirements:',
          '  led_panels:',
          '    source: External 5V power supply (required)',
          '    current_per_panel: "1.5A typical, 4A peak"'], True),
        ("`source:` naming a host power rail is not a citation — MUST FIRE",
         ['adapter_board:',
          '  source: P2 development board 5V supply',
          '  current: 35mA typical @ 35MHz'], True),
        ("`source:` naming a pattern CATEGORY is not a citation — MUST FIRE",
         ['timing:', '  source: motor_control', '  settle: "20 ms debounce"'], True),
        ("`sources:` listing EVENT NAMES is not a citation — MUST FIRE",
         ['events:', '  sources: ["CT-passed-CT1", "CT-passed-CT2"]',
          '  resolution: "1 clock at 160MHz"'], True),
        # «#412»: the fixtures below were rewritten to the OFFICIAL-TITLE form.
        # Their old spellings (`P2 Datasheet`, `P2 Silicon Doc v35`, a
        # `flash_loader.spin2 line 259`, a repo path to the ledger) are exactly
        # what the acceptance rule now refuses -- see the rule cases further down.
        ("official-title document citation with page — MUST NOT FIRE",
         ['absolute_maximum:',
          '  source: "Parallax Propeller 2 (P2X8C4M64P) Datasheet 2022/11/01, DC Characteristics, p.47"',
          '  vdd_max: "3.6V"'], False),
        ("versioned document citation — MUST NOT FIRE",
         ['timing:', '  source: "Propeller 2 Documentation v35, Branch Timing"',
          '  branch: "13 clocks at 160MHz"'], False),
        ("a GENUINE citation that also carries a revision — MUST NOT FIRE",
         ['known_bug:', '  source: "Propeller 2 Documentation v35 (KNOWN BUGS, Rev C)"',
          '  delta: "PTRx advances 4 ns later"'], False),
        ("`derived_from:` naming a Parallax source by title + section — MUST NOT FIRE",
         ['loader:', '  derived_from: "Parallax Propeller 2 Documentation v35, Boot Sequence"',
          '  spi_clock: "2 MHz"'], False),
        ("`verified_against:` naming an EF record that EXISTS — MUST NOT FIRE",
         ['drive:',
          '  verified_against: "EF-053 (2026-08-14)"',
          '  sink: "50 mA"'], False),
        ("`sources:` introducing a LIST of documents — MUST NOT FIRE",
         ['adc:', '  sources:',
          '    - "Propeller 2 Documentation v35 - Rev B/C Silicon (Chip Gracey)"',
          '  sample_period: "1024 clocks at 160MHz"'], False),
        ("inline attribution with no cite key at all — MUST NOT FIRE",
         ['branch_cost: "343.75ns at 160MHz (55 clocks per Propeller 2 Documentation v35, Branch Timing)"'],
         False),
        ("inline `Silicon Doc` (a codename, not a title) — MUST FIRE",
         ['branch_cost: "343.75ns at 160MHz (55 clocks per Silicon Doc v35 verbatim)"'],
         True),
        # F-335(e) — a DEFERRAL points the reader AWAY. This one shipped
        # `max_current_per_pin: "150mA"` against the datasheet's ±30 mA through
        # two purges, because the bare word `datasheet` marked the block cited.
        ("`source:` that DEFERS to a datasheet is not a citation — MUST FIRE",
         ['absolute_maximum:',
          '  max_current_per_pin: "150mA"',
          '  max_current_total: "Check datasheet for package limits"'], True),
        ("an inline deferral in prose is not a citation — MUST FIRE",
         ['note: "Sinks 150mA per pin; see the datasheet for package limits."'], True),
        ("a deferral that NAMES the document IS an attribution — MUST NOT FIRE",
         ['timing:', '  source: "See the Propeller 2 Documentation v35, KNOWN BUGS"',
          '  branch: "13 clocks at 160MHz"'], False),
        # F-335(d) — a slug names a pattern CATEGORY, not a document. These got
        # through because a bare `pasm2` / `validat` token sits INSIDE the
        # identifier, and they were masking (c) in `waitx.yaml`.
        ("`source:` naming a slug with an embedded language token — MUST FIRE",
         ['timing:', '  source: inline_pasm2_pattern',
          '  hold: "100us @ 200MHz"'], True),
        ("`source:` naming a slug with an embedded `validat` token — MUST FIRE",
         ['timing:', '  source: lock_validation',
          '  settle: "20 ms"'], True),
        # F-335(a) — the spelling eight board files actually use. Without it they
        # scored wholly-uncited, so Tier 1 could never apply to them at all.
        ("`documentation:` -> `primary: \"<doc>\"` IS a citation — MUST NOT FIRE",
         ['documentation:',
          '  primary: "P2 Eval Add-on Boards (#64006 Series) v2.0, Board A, p.5"',
          'specifications:',
          '  supply_voltage: "3.3V from host"'], False),
    ]
    for label, lines, want in cite_cases:
        body = "\n".join(strip_code_regions(lines))
        assert quantities_in(body), f"control case states no quantity: {label}"
        cited = cites_in(lines) or inline_cite(body)
        fired = not cited
        good = fired == want
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label}: fired={fired} expected={want}")

    # ACCEPTANCE-RULE cases («#412», S-393). Each MUST-FIRE line is a REAL line
    # from deliverables/ai/P2 (file:line quoted, 2026-10-09) unless marked
    # CONSTRUCTED; `want_class` is the class the line must be reported under.
    # The MUST-PASS lines are the other half: the rule has not been tightened
    # into refusing a good citation. A register that is missing is not a pass.
    print()
    if EF_IDS is None or CP_IDS is None or XF_IDS is None or OBEX_IDS is None:
        print("  [FAIL] the EF ledger, XF ledger, CP register or OBEX catalog is missing "
              "-- cannot judge ids")
        return 1
    rule_cases = [
        ("EXTRACTION PATH `silicon-doc-text.txt:NNN`, valid title beside it -- "
         "language/pasm2/setq2.yaml:35",
         '  source: "Propeller 2 Documentation v35 -- silicon-doc-text.txt:3264-3267 '
         '(SETQ2 + RDLONG reads hub longs into lookup RAM)"', "EXTRACTION_PATH"),
        ("REGISTER PATH `SOURCE-ERRATA.md` -- guides/pasm2-getting-started.yaml:607",
         '    source: "P2 Datasheet 2022/11/01, AC Characteristics (p.48) -- '
         'engineering/ingestion/sources/p2-datasheet/p2-datasheet-text.txt:2196-2200, '
         'footnote 2 at :2209. Compiler default from Parallax Spin2 Documentation v55 -- '
         'engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:1718. framing: '
         'E-007 in engineering/ingestion/SOURCE-ERRATA.md."', "REGISTER_PATH"),
        ("BATCH LABEL `parallax-quick-bytes` -- community/quick-bytes/tetris.yaml:33",
         "    source: parallax-quick-bytes", "BATCH_LABEL"),
        ("EF id that does not exist (CONSTRUCTED: language/pasm2/getxacc.yaml:27 with "
         "EF-069 -> EF-999)",
         '    source: "Hardware-verified on Rev C (EF-999): 50 of 50 idle/non-Goertzel '
         'reads equal the prior value; 8 of 8 mid-burst partitions exact."', "BAD_ID"),
        ("CP id that does not exist (CONSTRUCTED: language/pasm2/brk.yaml:22 with "
         "EF-085 -> CP-999)",
         '  source: "Parallax Spin2 Documentation v55 (conditional DEBUG: \'an '
         'opposite-condition SKIP instruction is placed before it\'); compiles '
         '(CP-999)"', "BAD_ID"),
        ("XF id that does not exist (CONSTRUCTED: XF-999)",
         '  source: "Hardware-verified on P2 silicon (XF-999): write-side pad is a phase of period hp."',
         "BAD_ID"),
        ("S-292 bookkeeping word -- language/pasm2/qvector.yaml:75",
         "documentation_source: p2_datasheet", "BOOKKEEPING"),
        ("Parallax paginated PDF cited WITHOUT p.N (CONSTRUCTED: variant of "
         "guides/pasm2-getting-started.yaml:607)",
         '  source: "Parallax Propeller 2 (P2X8C4M64P) Datasheet 2022/11/01, AC Characteristics"',
         "NO_PAGE"),
        ("codename `Silicon Doc v35` is not a title (the arbiter's probe)",
         '  source: "Silicon Doc v35, Clock Setup"', "NO_PARALLAX_DOC"),
        ("a title the document does not print: `P2 Datasheet` (the arbiter's probe)",
         '  source: "P2 Datasheet 2022/11/01, PASM2 instruction table, p.12"', "NO_PARALLAX_DOC"),
        ("a title the document does not print: `Parallax Propeller 2 Datasheet` (probe)",
         '  source: "Parallax Propeller 2 Datasheet 2022-11-01, Absolute Maximum Ratings, p.4"',
         "NO_PARALLAX_DOC"),
        ("a title the cover does not print: `32201 Prop Plug Guide` (probe)",
         '  source: "32201 Prop Plug Guide v3.0, Specifications, p.2"', "NO_PARALLAX_DOC"),
        ("a registry-excluded community document is not a Parallax title (CONSTRUCTED)",
         '  source: "Smart Pins (Titus) rev 5, WRPIN selector table"', "NO_PARALLAX_DOC"),
        # Source listings (Stephen, 2026-10-10): pinned to the CURRENT ingested edition.
        ("listing at an OLDER edition: interpreter v51 while v55 is current (CONSTRUCTED)",
         '  source: "Parallax Spin2 Interpreter v51 (2025.04.02), PINHIGH routine"',
         "STALE_EDITION"),
        ("listing at the banner edition the FPGA build shares: ROM booter v32i (CONSTRUCTED)",
         '  source: "Parallax Propeller 2 ROM Booter v32i, shut_down routine"', "STALE_EDITION"),
        ("OBEX id that does not exist in the catalog (CONSTRUCTED: OBEX 99999)",
         '  source: "OBEX 99999 (Imaginary Driver)"', "BAD_ID"),
        ("the bare word OBEX with no id names no object (CONSTRUCTED)",
         '  source: "OBEX community objects"', "NO_PARALLAX_DOC"),
        ("a real OBEX id beside a nonexistent one is still refused (CONSTRUCTED)",
         '  source: "OBEX 2842 (Full Duplex Serial); OBEX 99999 (Imaginary Driver)"', "BAD_ID"),
        ("listing with NO edition (CONSTRUCTED)",
         '  source: "Parallax Spin2 Interpreter, PINHIGH routine"', "NO_EDITION"),
        ("listing edition written BEFORE the title, not after -- architecture/xbyte_engine.yaml:113",
         '    source: "Chip Gracey, P2 silicon designer; v55 Spin2 interpreter '
         'Theory-of-Operations review."', "NO_EDITION"),
        ("listing cited by LINE NUMBER, current edition and all (CONSTRUCTED from "
         "streamer_smartpin_control.yaml:407 `flash_loader.spin2 line 259`)",
         '    source: "Parallax SPI Flash Programmer and Boot Loader v51 line 259"',
         "LINE_LOCATOR"),
    ]
    rule_pass = [
        ("Parallax title + edition + EF that exists -- language/pasm2/brk.yaml:22",
         '  source: "Parallax Spin2 Documentation v55 (conditional DEBUG: \'an '
         'opposite-condition SKIP instruction is placed before it\'); behaviour '
         'hardware-verified (EF-085)"'),
        ("a real EF with no document -- architecture/smart-pins/"
         "smart-pin-11000-adc-internal-clock.yaml:181",
         '  source: "Hardware-verified on P2 silicon (Rev C): hardware-verification '
         'ledger EF-024."'),
        ("a real OBEX object by id -- OBEX 2842 exists in the catalog",
         '  source: "OBEX 2842 (Full Duplex Serial)"'),
        ("two real OBEX objects in one citation -- OBEX 2842 and OBEX 2824",
         '  source: "OBEX 2842 (Full Duplex Serial); OBEX 2824 (NEC RX)"'),
        ("a real XF with no document (CONSTRUCTED) -- XF-001 exists",
         '  source: "Hardware-verified on P2 silicon (XF-001)"'),
        ("a real CP (CONSTRUCTED: no KB line cites a CP yet) -- CP-001 exists",
         '  source: "Compiler-proved (CP-001)"'),
        ("official title + edition + section + p.N (CONSTRUCTED)",
         '  source: "Parallax Propeller 2 (P2X8C4M64P) Datasheet 2022/11/01, AC Characteristics, p.48"'),
        ("listing at the CURRENT edition, routine named -- the form of Stephen's ruling",
         '  source: "Parallax Spin2 Interpreter v55 (2026.05.07), PINHIGH routine"'),
        ("listing in the banner's own spelling `<title> - v55 - <date>` (CONSTRUCTED)",
         '  source: "Spin2 Interpreter - v55 - 2026.05.07, PINHIGH routine"'),
    ]
    # One positive per CANONICAL_TITLES document and per printed form: the form,
    # an edition, a section, and `p.N` where the document is paginated.
    for key, forms, edition, paginated, _prov in CANONICAL_TITLES:
        for form in forms:
            cite = f"{form} {edition}, Section Heading" + (", p.7" if paginated else "")
            rule_pass.append((f"canonical title [{key}] form `{form}` (CONSTRUCTED)",
                              f'  source: "{cite}"'))
    for label, text, want_class in rule_cases:
        found = list(citation_values([text]))
        hit = [(v, classify(v)) for _, k, v in found if claimed(k, v)]
        fired = bool(hit) and not hit[0][1][0]
        classes = hit[0][1][1] if hit else []
        good = fired and want_class in classes
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label}: fired={fired} "
              f"classes={classes} expected={want_class}")
    for label, text in rule_pass:
        found = list(citation_values([text]))
        hit = [(v, classify(v)) for _, k, v in found if claimed(k, v)]
        passed = bool(hit) and hit[0][1][0]
        ok &= passed
        print(f"  [{'PASS' if passed else 'FAIL'}] {label}: accepted={passed}")

    # Q3: `enhancement_source` must not count as a citation (real line
    # language/pasm2/qvector.yaml:84), Q5: catalog url rule.
    extra = []
    ql = ['timing:', '  latency: "55 clocks at 160MHz"',
          'enhancement_source: PNUT_TS_v2.0_complete_operand_integration_2025-09-13']
    extra.append(("`enhancement_source:` does not cite -- qvector.yaml:84 -- block stays uncited",
                  not cites_in(ql)))
    tetris_head = ["metadata:", "  url: https://www.parallax.com/tetris/", "  source: parallax-quick-bytes"]
    extra.append(("catalog entry WITH a parallax.com url IS cited (quick-bytes/tetris.yaml:4)",
                  catalog_cited(tetris_head)))
    extra.append(("catalog entry WITHOUT a url is NOT cited (CONSTRUCTED: tetris.yaml head, url removed)",
                  not catalog_cited(["metadata:", "  source: parallax-quick-bytes"])))
    extra.append(("catalog entry with a NON-parallax url is NOT cited (CONSTRUCTED)",
                  not catalog_cited(["metadata:", "  url: https://example.com/tetris/"])))
    for label, passed in extra:
        ok &= passed
        print(f"  [{'PASS' if passed else 'FAIL'}] {label}")

    # S-308a: example blocks are exempt by LOCATION; claim-bearing blocks are not.
    def _block_fires(blk):
        name = blk[0].split(":")[0]
        return (not is_example_block(name, blk)) and bool(quantities_in("\n".join(blk)))
    exempt = [
        ("`examples:` block", ["examples:", "  - clk: 160MHz"], False),
        ("`quick_example:` block", ["quick_example:", "  clk: 160MHz"], False),
        ("`usage_example:` block", ["usage_example: |", "  waitms at 160MHz"], False),
        ("`authority_tier: EXAMPLE` block", ["worked:", "  authority_tier: EXAMPLE", "  clk: 160MHz"], False),
        ("uncited prose", ["description: |", "  Runs at 160MHz."], True),
        ("`notes` beside an exempt example", ["notes:", "  - Runs at 160MHz."], True),
        ("PRINCIPLE-tier figures", ["rule:", "  authority_tier: PRINCIPLE", "  clk: 160MHz"], True),
        ("`common_patterns` is NOT exempt", ["common_patterns:", "  - clk: 160MHz"], True),
    ]
    for label, blk, want in exempt:
        fired = _block_fires(blk)
        good = fired == want
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] S-308a {label}: fired={fired} expected={want}")

    total = (len(cases) + len(region_cases) + len(cite_cases) + len(rule_cases)
             + len(rule_pass) + len(extra) + len(exempt))
    print(f"\n{total} case(s): quantity {len(cases)} · region {len(region_cases)} "
          f"· citation {len(cite_cases)} · acceptance rule {len(rule_cases)} refuse + "
          f"{len(rule_pass)} accept · Q3/Q5 {len(extra)} · S-308a {len(exempt)}")
    print()
    print(SCOPE_NOTE)
    print("Negative control PASSED -- quantities detected, P2 syntax not "
          "mistaken for units, code/comment regions skipped WITHOUT silencing "
          "prose claims, and a board revision / a power supply no longer read "
          "as a citation while every real citation form still is."
          if ok else "Negative control FAILED -- do not trust this run.")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--inventory", action="store_true", help="print coverage first")
    ap.add_argument("--advisory", action="store_true", help="also print Tier 2 in full")
    ap.add_argument("--negative-control", action="store_true",
                    help="prove the tool can fail; audits nothing")
    ap.add_argument("--tier2-blocking", action="store_true",
                    help="make Tier 2 BLOCK too (the S-308b switch; owed to the citations task)")
    ap.add_argument("--list", action="store_true",
                    help="list every BAD_CITATION (default: first 5 per class; counts are always complete)")
    args = ap.parse_args()

    if args.negative_control:
        return negative_control()

    tier1, tier2, scanned, bad = audit()
    if tier1 is None:
        print(f"ERROR  {KB_ROOT} or the EF ledger / CP register not found — "
              f"nothing audited. Not a pass.")
        return 2
    t2_block = TIER2_BLOCKING or args.tier2_blocking

    if args.inventory:
        print(f"scanned   {scanned} YAML file(s) under {KB_ROOT.relative_to(REPO)}")
        print(f"Tier 1    {len(tier1)} uncited quantitative block(s) in citing files")
        print(f"Tier 2    {len(tier2)} uncited quantitative block(s) in non-citing files\n")

    # BAD_CITATION -- the acceptance rule applied to every claimed citation.
    by_class = {}
    for cls, where, key, excerpt in bad:
        by_class.setdefault(cls, []).append((where, key, excerpt))
    if bad:
        print(f"BAD_CITATION -- a citation that names something we may not cite "
              f"({len(bad)}) -- these block")
        print("  by class: " + " · ".join(
            f"{c} {len(by_class[c])}" for c in _CLASS_ORDER + ["NO_CATALOG_URL"]
            if c in by_class) + "\n")
        for cls in _CLASS_ORDER + ["NO_CATALOG_URL"]:
            rows = by_class.get(cls, [])
            if not rows:
                continue
            print(f"  {cls}: {len(rows)}")
            for where, key, excerpt in (rows if args.list else rows[:5]):
                print(f"        {where} [{key}] {excerpt}")
            if not args.list and len(rows) > 5:
                print(f"        ... {len(rows) - 5} more (--list)")
        print()
    else:
        print("BAD_CITATION: none\n")

    if tier1:
        print(f"TIER 1 -- UNCITED IN A CITING FILE ({len(tier1)}) -- these block\n")
        for name, detail in sorted(tier1, key=lambda t: t[1]):
            print(f"  [UNCITED_IN_CITING_FILE] {name}\n        {detail}")
        print()
    else:
        print("TIER 1: none\n")

    if args.advisory and tier2:
        print(f"TIER 2 -- WHOLLY UNCITED FILES ({len(tier2)}) -- advisory\n")
        for name, detail in sorted(tier2, key=lambda t: t[1]):
            print(f"  [UNCITED_FILE] {name}\n        {detail}")
        print()
    elif tier2:
        print(f"TIER 2 -- ADVISORY: {len(tier2)} block(s) in wholly-uncited files "
              f"(run with --advisory to list)\n")

    blocking = len(tier1) + len(bad) + (len(tier2) if t2_block else 0)
    if blocking:
        print(f"FAIL  {len(tier1)} Tier 1 + {len(bad)} BAD_CITATION"
              f"{f' + {len(tier2)} Tier 2' if t2_block else ''} violation(s) across "
              f"{scanned} file(s); Tier 2 is "
              f"{'BLOCKING' if t2_block else 'advisory (switch-on owed to the citations task)'}")
        return 1
    print(f"PASS  no Tier 1 or BAD_CITATION violations across {scanned} file(s); "
          f"{len(tier2)} Tier 2 advisory block(s) remain (advisory, not blocking)")
    print()
    print(SCOPE_NOTE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
