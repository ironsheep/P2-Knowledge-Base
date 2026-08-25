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

EXIT STATUS
    0  no Tier 1 violations
    1  one or more Tier 1 violations
    2  the KB tree was not found -- nothing audited, which is never a pass

USAGE
    audit-yaml-claim-sourcing.py [--inventory] [--advisory] [--negative-control]
"""

import argparse
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
    "  nothing here reads the cited document. Guide rules R6, R7 and R9 have no\n"
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
    r"reference|references|authority|derived_from|verified_against|documentation)\s*:\s*(.*)$",
    re.IGNORECASE)

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

# An INLINE attribution is a citation. The question this tool asks is "does this
# claim say where it came from", and `"343.75ns at 160MHz (55 clocks per Silicon
# Doc v35 verbatim)"` answers it perfectly well without a `source:` field.
# Demanding one particular spelling would turn a correctly-attributed claim into
# a violation, which teaches people the gate is wrong rather than that the claim
# was.
# `rev\s*[BC]\b` was in this vocabulary and is deliberately NOT any more. It was
# reasoning from `Silicon Doc Rev C` prose, but in a hardware file `Rev B` is the
# board's OWN IDENTITY, not a document reference --
#     power_configuration: "5V shunt jumper required on P2-ES Eval Board Rev B"
# -- and that one string marked the whole `specifications` block cited, hiding
# 500mA/1A/~2mA. It did its worst damage exactly where it fired most: the board
# tree, where every file legitimately names a board revision.
#
# Nothing genuine was lost with it. Measured across all 1129 files: every real
# citation in the corpus that contains a revision also names the document it is
# a revision OF -- `"P2 Silicon Doc v35 (KNOWN BUGS, Rev C) -- verbatim"`,
# `"Propeller 2 Documentation v35 - Rev B/C Silicon"`, `"#64000 Propeller 2 Eval
# Board Rev C Guide v2.0"` -- so each is still recognised by `silicon doc`,
# `p2 documentation` or the `guide` value token. The ten blocks the token was
# holding up were board and silicon revisions, every one.
INLINE_CITE_RE = re.compile(
    r"(silicon\s*doc|datasheet|data\s*sheet|spin2\s*v\d|p2\s*documentation|"
    r"hardware[- ]verified|empirical|EF-\d+|per\s+the\s+doc|verbatim|"
    r"parallax\s+p2)", re.IGNORECASE)

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
# attributes, and `INLINE_CITE_RE` already accepts it.
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


def is_citation(value):
    """A cite key's VALUE counts only when it names a document (or an empirical
    record) AND that naming attributes the claim rather than deferring it."""
    v = value.strip().strip('"').strip("'").strip()
    if points_away(v):
        return False
    return bool(CITE_VALUE_RE.search(v))


def inline_cite(text):
    """An inline attribution, judged PER LINE so a deferral cannot silence the
    line it sits on. `INLINE_CITE_RE` matched the bare word `datasheet` anywhere
    in a block body, which is the other half of how F-335(e) passed."""
    for ln in text.split("\n"):
        if not INLINE_CITE_RE.search(ln):
            continue
        seg = ln.split(":", 1)[1] if ":" in ln else ln
        if points_away(seg):
            continue
        return True
    return False


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
            if any(is_citation(ln.split(":", 1)[-1]) for ln in value.split("\n")):
                return True
            continue
        if is_citation(value):
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
    if not KB_ROOT.is_dir():
        return None, None, 0
    tier1, tier2, scanned = [], [], 0
    for path in sorted(KB_ROOT.rglob("*.yaml")):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        scanned += 1
        rel = path.relative_to(REPO)
        file_cites = cites_in(lines) or inline_cite("\n".join(lines))
        prose = strip_code_regions(lines)

        for name, start, end in top_level_blocks(lines):
            body = "\n".join(prose[start:end])
            qty = quantities_in(body)
            if not qty:
                continue
            block_cites = cites_in(lines, start, end) or inline_cite(body)
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
    return tier1, tier2, scanned


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
        ("short-form document citation — MUST NOT FIRE",
         ['absolute_maximum:', '  source: "P2 Datasheet"',
          '  vdd_max: "3.6V"'], False),
        ("versioned document citation — MUST NOT FIRE",
         ['timing:', '  source: "P2 Silicon Doc v35"',
          '  branch: "13 clocks at 160MHz"'], False),
        ("a GENUINE citation that also carries a revision — MUST NOT FIRE",
         ['known_bug:', '  source: "P2 Silicon Doc v35 (KNOWN BUGS, Rev C) -- verbatim"',
          '  delta: "PTRx advances 4 ns later"'], False),
        ("`derived_from:` naming a source file + line — MUST NOT FIRE",
         ['loader:', '  derived_from: "Parallax P2 flash_loader.spin2 line 259"',
          '  spi_clock: "2 MHz"'], False),
        ("`verified_against:` naming the empirical ledger — MUST NOT FIRE",
         ['drive:',
          '  verified_against: "engineering/ingestion/external-sources/'
          'hardware-verification/P2-EMPIRICAL-FINDINGS.md EF-053 (2026-08-14)"',
          '  sink: "50 mA"'], False),
        ("`sources:` introducing a LIST of documents — MUST NOT FIRE",
         ['adc:', '  sources:',
          '    - "Propeller 2 Documentation v35 - Rev B/C Silicon (Chip Gracey)"',
          '  sample_period: "1024 clocks at 160MHz"'], False),
        ("inline attribution with no cite key at all — MUST NOT FIRE",
         ['branch_cost: "343.75ns at 160MHz (55 clocks per Silicon Doc v35 verbatim)"'],
         False),
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
         ['timing:', '  source: "See the P2 Silicon Doc v35, KNOWN BUGS"',
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
          '  primary: "P2 Eval Add-on Boards (#64006 Series) v2.0"',
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

    total = len(cases) + len(region_cases) + len(cite_cases)
    print(f"\n{total} case(s): quantity {len(cases)} · region {len(region_cases)} "
          f"· citation {len(cite_cases)}")
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
    args = ap.parse_args()

    if args.negative_control:
        return negative_control()

    tier1, tier2, scanned = audit()
    if tier1 is None:
        print(f"ERROR  {KB_ROOT} not found — nothing audited. Not a pass.")
        return 2

    if args.inventory:
        print(f"scanned   {scanned} YAML file(s) under {KB_ROOT.relative_to(REPO)}")
        print(f"Tier 1    {len(tier1)} uncited quantitative block(s) in citing files")
        print(f"Tier 2    {len(tier2)} uncited quantitative block(s) in non-citing files\n")

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

    if tier1:
        print(f"FAIL  {len(tier1)} Tier 1 violation(s) across {scanned} file(s)")
        return 1
    print(f"PASS  no Tier 1 violations across {scanned} file(s); "
          f"{len(tier2)} Tier 2 advisory block(s) remain (advisory, not blocking)")
    print()
    print(SCOPE_NOTE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
