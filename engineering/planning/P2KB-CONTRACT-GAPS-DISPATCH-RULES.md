# P2KB contract gaps — dispatch rules

The one home for what every agent dispatched in this sprint must follow. Each remaining task points
here, and an agent reads this whole file before starting. Plan:
`engineering/planning/P2KB-CONTRACT-GAPS-SPRINT-PLAN.md`.

## How the sprint runs

**Parallel where appropriate.** Stephen, 2026-11-09: "yes resume and use parallel agenst where
appropriate". This sets the dispatch model for this sprint, in place of the repo's `arbiter-serial`
default.

- Every YAML file has one owning agent at a time. The prompt lists the files an agent owns. An edit
  needed in a file another agent owns goes in the report as a proposed edit, and the arbiter applies
  or routes it.
- Agents do not write the shared records: `engineering/operations/YAML-CERTIFICATION-RECORD.md`,
  `P2KB-CONTRACT-GAPS-CERTIFY-LIST.txt`, `P2KB-CONTRACT-GAPS-MANUAL-REACH.md`,
  `engineering/operations/P2KB-CORRECTION-FINDINGS.md`, the compile-proof register, or the compile
  manifest. Each agent writes its rows to its own staging file named in the prompt, and the arbiter
  merges them.
- New register numbers (F-, CP-, EF-, E-) are the arbiter's. An agent writes `F-TBD` or `CP-TBD`.
- Agents run file-scoped checks only (`--files`, or the single YAML file). Whole-tree gates would
  read other agents' unfinished edits, so the arbiter runs them when the wave has returned.
- Read-only audits of separate file groups run together. The next batch may start while the last is
  being audited, when the two share no file.

**A turn never ends with the sprint idle.** The arbiter ends a turn only with an agent dispatched, a
named stop, or the sprint finished (`.claude/doctrine-overlay.md`, *A running sprint ends a turn only
with work in flight*).

## Certification

Plan §16. Every YAML file in the release diff is read WHOLE against its sources once, each claim
checked against a source line, a CP or an EF/XF. Unsupported claims are corrected or stated as not
documented in the same pass. The file gets a row in the record (file, date, sources read, result).

**Later changes to a certified file:**

- If the later change only adds or removes a `related:` entry or a whole key, the row stands. A diff
  audit must prove nothing else changed, and the row is updated to say so.
- If the later change alters served wording, the file is read whole again and the row is updated.

Files added to the change set go on the certify list. Each package closes with a change-set audit: a
fresh read-only agent reads the diff, reads every served statement of the files in its group, and
reports any hunk not wanted, warranted, correct and complete. The arbiter has each fixed before close.

## Before the first audit: the class sweep

Over the task's files, read for these recurring defects and fix them before any audit runs:

- unsourced suitability words ("fast", "precise", "high precision", "applications", "ideal for");
- facts about a sibling instruction in a single-instruction file;
- comments that misdescribe the code;
- document framing ("this section", "as described in");
- glosses no source states ("real/imaginary", "sqrt");
- unsourced negatives, advice and superlatives.

## Audit sizing

- Instruction YAML files: batches of about 20, one full-read audit per batch.
- Large architecture or concept prose files: groups of 3 to 6. Expect more than one round; loop until
  a full-read round contradicts nothing.

## Standing sweep

Tools in `engineering/tools/`, `audit-*` under `validation/`. The arbiter re-runs all of them at the
boundary.

Baseline after «#460»: `verify-yaml-format.py` 1141 parse · `validate-crossref-keys.py` 4733 resolve ·
`audit-kb-code-compiles.py` PASS 3206 blocks · `audit-yaml-claim-sourcing.py` 1010 files 0/0/0 ·
`audit-yaml-duplicate-keys.py` 0 over 1140 · `audit-yaml-plain-scalar-comment.py` 0 ·
`audit-yaml-provenance-key-names.py` clean · `audit-constant-fidelity.py` 0/0 over 120 ·
`audit-adc-encoding.py`, `audit-hardware-revision-scope.py`, `audit-index-findability.py`,
`audit-index-integrity.py`, source-lock PASS · `audit-yaml-certification-record.py` PASS ·
`audit-kb-pending.py --session` listed, all dispositioned · `validate-dod-release.py` fails only
"Orphaned Files: 3" (`instruction_encoding_key.yaml`, `language/pasm2/concepts/pixel_mixer.yaml`,
`architecture/streamer/colorspace-and-dvi.yaml`) until the index regenerates at release.

File and block counts grow when a task adds YAML files; say so. Any other moved value: report the
delta and the reason, never absorb it.

## YAML rules

- Fix everything you see wrong in a file you read, in this pass, and search the class by meaning
  wider than the target (KB carve-out). Only a true blocker (bench, missing document, Stephen's call)
  goes to the corrections register, and the wrong claim is removed or marked not documented meanwhile.
- Every new or changed statement rests on a source line, a CP or an EF/XF.
- Citations go in source fields, never in served text. No version stamps in served text.
- Aliases go under `aliases:`, never `keywords:`. New traps go under `anti_patterns`.
- Never delete a `related:` reference; redirect it (Sacred Rule 7). Use full KB paths.
- Call a KB file a YAML file.
- No YAML commit: the change set commits when the release starts (task «#467»).
- Never edit a manual master. When a fix's claim appears in one, add a reach row (file:line, what it
  says, the YAML change it waits on) to your staging file at that moment.

## Sources and served text

- Every file edited is read whole, each claim checked, and a row states exactly what was read. A
  certified file with a known defect is a false row.
- Run the full tier list before "not documented" AND before removing a factual claim: Silicon Doc,
  P2 Documentation, Hardware Manual, datasheet, PASM2 Manual, instruction CSV, Spin2 v55, Spin2
  interpreter listing, ROM booter listing, the bench ledger, the compile-proof register, the XF
  ledger. Tab-formatted lines defeat naive greps. `clkfreq` at `LONG[$44]` is `spin2-v55-text.txt:1731`.
- A formula or mapping in the KB is a derivation until a source line states it.
- Titus is not citable. Our YAML is never a source (navigation pointers are fine). OBEX code is not a
  source for a P2 fact. PNut REF theory-of-operations
  (`engineering/document-production/manuals/p2-debug-window-manual/REF/theory-of-operations/`) is
  ground truth for DEBUG displays.
- Served values carry facts only: no document names, pages, rows or locators (PNut routine names and
  "the worked program" included); no EF/CP ids, "measured", "documented" or "compiler-verified"
  framing; no test scores or past-tense test reports; no build-history YAML comments; no emphasis
  capitals.
- Citation keys are only `source:`, `sources:`, `documentation_source:`. Pages are required; Hardware
  Manual pages come from its table of contents, not docx page breaks. No SD:/EF: line locators, even
  in source fields. Inside source fields EF-/XF-/CP- ids and provenance are allowed; F-/E-/S-/VO-
  register ids are not (the gate rejects them). Keep a document's full title on one line in folded
  source scalars.
- Two documents disagree: state both values, documents unnamed ("Parallax's documents also give …").
- Compiler versus Spin2 document on legality: the KB teaches what compiles, and the document's error
  is filed once proven.
- EF facts are scoped by tested conditions, not run counts. A bench-proven workaround may be stated
  as a workaround. The P2's 8 cogs is a fact. No pre-Rev-B history. No erratum numbers in prose.
- No unsourced suitability, advice or imperatives, superlatives or negatives; `common_uses` and
  `common_applications` lists go. Unknowns are "Not documented: …". No derived arithmetic.
- Single-instruction files state only their own instruction's facts. Comments describe what the code
  does.
- Spin2 interpreter timing is unsourced, so smart-pin poll gaps go in inline PASM. A served wait must
  not rest on an untested assumption where it can hang.
- `"egg beater"` is a Parallax term (`p2-documentation.txt:298`).

## Code and YAML mechanics

- In PASM2 examples, code comes first, initialized LONG data after it and before RES.
- Under ORG a label on unaligned byte data is refused ("Cog symbol must be long-aligned").
- Spin2 `RDPIN()` returns C in bit 31 (`spin2-v55-text.txt:543`), so MSB-justified reads use inline
  PASM2.
- Count `##` AUGS words in REP blocks (CP-038). WAITX waits 2 + D clocks.
- Edit tool only. Quote " #" values. Use `|2` for deeper first-line literal blocks.
- No provenance-looking key names (`example_source` was refused; use `example_program`).
- Record rows have exactly 4 cells, no literal `|` inside a cell, path without the
  `deliverables/ai/P2/` prefix.
- Leave the `compiler_*` table blocks alone until task «#468».
- Removing a block shifts line numbers cited in range files; re-point them.
- A legality fact with no source can be settled by a CP. Design its control so it can fail. A CP
  record needs a `*KB:*` line or `validate-dod-release.py` fails.
- Compile manifest (arbiter only): `--refresh` needs `--files` and does not prune stale assumes;
  `--apply not-code` needs a reason; a key rename needs `--apply` for the new address and the old
  entry deleted by hand; after the text settles: `--apply`, delete ORPHANs, `--refresh`, gates.

## By role

**Fix agents.** Quote a source line for every new served sentence. Where no line says it, write
"Not documented: …" instead of composing a replacement. Carry the rulings below. Run file-scoped
gates. No `--refresh` or `--apply`.

**Audit agents.** Read-only, whole-file read of every served statement, full tier list before calling
anything unsourced. The rulings below are not findings.

**Arbiter.** Open the source before applying any auditor correction. Compile a fix agent's example in
its real context before trusting STALE as a pass. Full sweep including `validate-dod-release.py`
before close.

## Rulings: correct as they stand, do not report

- "Parallax's documents also give …" for a two-document disagreement.
- The allow-listed `not_stated_by_any_source` key.
- EF results stated by tested conditions without per-run counts.
- "Not documented: …" statements backed by a listed search.
- The statement that the P2 has 8 cogs.
- "egg beater" as a term.
- `compiler_*` table blocks, until task «#468».
