# P2KB close-out sprint — plan

**Head / element:** `yaml:p2kb`. **Seeded by** the close-out study
`engineering/analysis/2026-10-08-p2kb-close-out-study.md` (steps 0–10 done) and its evidence folder
`engineering/analysis/2026-10-08-p2kb-close-out-evidence/`. **This plan points at the study and the
registers; it does not restate them.** A row's defect, evidence and change spec live on its `S-NNN`
row (and the evidence file it names); a register entry's state lives in
`engineering/operations/P2KB-CORRECTION-FINDINGS.md`; a bench fact lives in
`engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md`.

**Status:** DRAFT — §0 questions open; design decisions in §0.2 await Stephen's per-decision
confirmation before any YAML edit (sprint-plan overlay).

---

## §0 Open questions (each with a recommendation; asked one at a time)

1. ~~What does a KB entry cite for a fact our own compile proved?~~ **RESOLVED 2026-10-09 (study
   Q12):** a separate compile-proof register, `CP-NNN` — "to keep our registers pure". Legality facts
   stay CP; behaviour facts move to EF when a P2 run proves them. Citations are internal provenance.
   Built in §6.
2. **Citation format for the S-392 rewrite** (~150 citations now pointing at our text captures).
   *Recommendation:* `"<Parallax title> <edition>, <section heading>"`, plus `p.N` where the
   document is a paginated PDF (Datasheet, Hardware Manual, PASM2 Manual); no line numbers, no
   repo paths (those name our files). Example: `"Parallax P2 Documentation v35 (Rev B/C), Smart Pins:
   USB host/device %11011"`.
3. **`pnut_ts` → `pnut-ts`** (S-396, 110 lines in 53 files): the only installed executable is
   `pnut-ts`; the compiler's banner prints `'pnut_ts'`. *Recommendation:* the KB names the command a
   reader types — `pnut-ts` — everywhere.

### §0.2 Design decisions to flag (overlay: confirm each before edits start)

- **D-A** Gates land before content (§1 before §2–§7), so every content edit is checked by the gate
  that will judge it at release.
- **D-B** The compile-gate drain (§2) edits each failing block to compile *and* agree with its
  source (F-381: correct = compiles AND sourced); where no source states the example's behaviour,
  the block is removed, not invented (Sacred Rule #7 for any `related:` it held).
- **D-C** Rows whose fix is "remove" (R4 invented facts, R9 tool limits, P1 carry-over) remove the
  claim; nothing is rewritten from memory to fill the gap.
- **D-D** Decision Q8: `language/PASM2-ENCODING-REFERENCE.md` moves to
  `engineering/standards/pasm2-encoding-reference.md` (generated), and
  `engineering/tools/gen-pasm2-encoding-reference.py`'s default output path moves with it.
- **D-E** Proven compiler-vs-document disagreements are filed as `SOURCE-ERRATA` E-020..E-023 (Q9),
  reported to Parallax through Stephen.

---

## Standing rulings this plan rests on (quoted, dated)

- **Fix everything seen, search wider, never defer** (Stephen, 2026-10-08) — doctrine *On the KB,
  what we see wrong we fix in the same pass*.
- **Commits are change sets** (2026-10-08) — doctrine *A commit carries only the work in hand*.
- **Never edit ingested docs** (2026-10-08; scope confirmed 2026-10-09 Q1) — documents, our
  extractions, accepted results; registries and bench workflow via their skills.
- **Bench only where the sources are silent** (2026-10-08).
- **Citations name official Parallax documents; the self-created exceptions are an EF record (silicon)
  and a CP record (compile proof), in separate registers; citations are internal provenance**
  (2026-10-09, Q3/Q4/Q12).
- **Our reasoning is not a source** (2026-10-09) — an unexplained observation stays open.
- **Tests we publish from prove their answer beyond doubt** (2026-10-09).
- **Doc vs compiler: teach what compiles; file proven errata; no PNut checks** (2026-10-09, Q9).
- **§1.5 change-set audit before any release; Stephen reviews before release; no push without him**
  (2026-10-05, 2026-10-08).
- **One close-out release**, the planned v1.24.0 folded in ("we need the new full closeout
  process", 2026-10-08) — task «#398».

## Intent and done

**For:** close out every YAML-scoped correction in one effort and ship it as one release.
**Done means:** every study row S-001..S-396 in its applied state (or its named blocker recorded
in the register with the claim removed meanwhile); `validate-dod-release.py` all green with the
ENH-03 compile gate at 0 FAIL; the §1.5 audit recorded; Stephen's review; tag and push with him;
«#398» follows.

**Baseline measured 2026-10-09** (`python3 engineering/tools/validate-dod-release.py`): every gate
PASS except **KB Code Compiles — 352 FAIL in 176 files, all REGISTERED** (3077 blocks: 501
program, 1932 fragment, 17 never, 627 not-code; `audit-kb-code-compiles.py`).

---

## §1 Gates first (study Group F; S-308; S-393)

**Why:** a content fix is only as good as the gate that judges it at release (D-A).
**Specs:** `engineering/analysis/2026-10-08-p2kb-close-out-evidence/gates-groupF-specs.md` —
S-382 (` #` plain-scalar cut), S-383 (dangling `yaml_file:`, F-364), S-384 (index sha256 vs blob,
F-441), S-385 (index freshness, F-405), S-386 (rating without board revision, F-454), S-387
(directory-name findability, F-389), S-388 (one-line code keys into the compile gate), S-389 (bare
built-in constant as a PASM operand). Plus **S-308** (D4 claim-sourcing tightening) and **S-393**
(`CITE_KEY_RE`: a value counts only when it names a Parallax document or an EF record; teaches
`documentation_source` only; catalog entries' parallax.com `url:`; negative controls for an
extraction path, a register path, a batch label).
**Target:** each gate in `validate-dod-release.py`, with negative controls, failing on today's
population exactly as the spec's counts say, then driven to 0 by §2–§7.
**Verify:** normal — the gate passes a known-good file; edge — the spec's boundary case (e.g. ` #`
inside a quoted scalar must NOT fire); error — each negative control fires; the DoD runner's total
includes the new gate.

## §2 Compile-gate drain (R1)

**Starting point:** 352 registered failures in 176 files (instrument output above); each carries
its `S-NNN` in the manifest (`engineering/tools/validation/kb-compile-manifest/`).
**Target:** 0 FAIL; each block fixed per its row's change spec (D-B); manifest entries removed as
blocks pass; the class sweep for each row's pattern done in the same pass (R2 P1 carry-over, R3
other-language habits, R6 arithmetic/field layout via `CON` folding).
**Verify:** the gate at 0 FAIL / 0 REGISTERED; normal — a fixed program block compiles; edge — a
fragment compiles in its declared wrap; error — a block deliberately broken in scratch fails with
its row unregistered (gate still blocks).

## §3 Content change specs, by KB area (R2–R10)

Every study row whose disposition is a change spec, worked by area so each file is touched once:
`architecture/` (incl. smart-pins, streamer, system-registers, decomposition), `language/spin2/`,
`language/pasm2/`, `language/fundamentals/`, `hardware/`, `guides/`, `application-notes/`,
`community/`, `code-examples/`, `tools/`. Row lists: the study §3 register and the evidence spec
files (`rows-S001-S040-specs.md` … `rows-S220-S280-specs.md`, `groupB-register-items-specs.md`,
`gaps-groupC-specs.md`, `f547-operator-cascade-specs.md`). Includes the R10 gating sweep against
v55's version history and deletion of change notes (D5), and the F-547 operator cascade.
**Verify:** each row's own check (named on the row); every §1 gate green per area batch.

## §4 Citations and provenance (Q3, Q4, Q5; S-292, S-293, S-328, S-390, S-392; F-352)

- S-292: 40 bookkeeping `documentation_source:` words (evidence `f375-bookkeeping-token-sites.txt`).
- S-293: delete the 356 `enhancement_source:` lines.
- S-328: delete `metadata.source: parallax-quick-bytes` (42 files); `url:` is the citation.
- S-390: `code_author: Jane Doe` — check the article page on parallax.com; remove unless it names her.
- S-392: rewrite ~150 citations that name our captures/summaries/registers to the Parallax document
  (format per §0 Q2); a claim with no Parallax document behind it goes through the unsourced search.
- F-352: `click_module_integration.yaml` — offsets already cite the 64008 schematic; the
  `documentation_source: schematic_primary` label is fixed by S-292/S-392; register entry closed.
**Verify:** §1's S-393 gate green; `grep -rn "engineering/ingestion\|-text\.txt\|complete-[a-z-]*\.md\|SOURCE-ERRATA" deliverables/ai/P2` returns 0; normal/edge/error per S-393's controls.

## §5 Bench results into the KB (EF-093..EF-101; VO-J-035)

Per the study §5 *Round 1 results* table (it names each page and what it states). VO-J-035
(«#409») is written into the USB page when its EF exists; until then that page carries no
on-the-fly claim.
**Verify:** each page cites its EF; the bench-ledger gate (`*KB:*` lines) green.

## §6 Compiler vs document (Q9; S-147, S-251, S-280, S-345, S-157; S-354; S-396)

**Premises measured 2026-10-09** (`pnut-ts` v1.55.8, scratch `/tmp/claude-1000/errata/`):
- symbols: 30 characters compile; 31 and 32 → `Symbol exceeds 30 characters` (v55 :166 says 32);
- `w := v\3` compiles; `v\3` alone → `Variable needs an operator` (v55 operator table lists `var\x`);
- `@\"a\db"` → `Expected end of line (m281)`; `\n`, `\\`, `\x01`, `\x00` compile (v55 :59 says unknown
  sequences pass verbatim);
- `C_Z` in Spin2 needs `{Spin2_v46}` (then compiles); in a DAT/PASM block `debug(c_z)` → `Expected
  "("` under `{Spin2_v46}` and `{Spin2_v55}` (v55 :913 "For PASM, DEBUG() statements can output …
  C/Z flags"; :1006 "Useful in PASM code");
- S-354: `-DTARGET_P2_EDGE` and `-D TARGET_P2_EDGE` both define the symbol — **not a defect**;
- S-396 (new): `pnut_ts` appears 110 times in 53 KB files; the only executable is `pnut-ts`.
**Target:**
1. **Stand up the compile-proof register** (Stephen's request, Q12): `engineering/ingestion/external-sources/compiler-verification/COMPILE-PROOFS.md`
   (`CP-NNN`: fact · legality or behaviour · source file in `proofs/` · command · `pnut-ts` version ·
   verbatim output · KB home · `→ EF-NNN` when a P2 run later proves a behaviour fact), with a README
   stating that lifecycle. Teach the sourcing gate (§1, S-393) `CP-NNN` as the second self-created
   citation, and add a CP -> KB-home check alongside the bench ledger's.
2. **CP-001..CP-004** from the proofs above (symbol length; `var\x` statement; unknown escape; `C_Z`
   in PASM), each a versioned `.spin2` that reproduces the output.
3. The KB teaches what compiles (`identifier-rules.yaml`, `escape-strings.yaml`,
   `debug-commands/c-z.yaml`, the operator pages), provenance `CP-NNN`.
4. E-020..E-023 filed in `SOURCE-ERRATA.md`, each pointing at its CP record (D-E).
5. S-396 swept.
**Verify:** each CP source reproduces its recorded output under `pnut-ts`; each taught form compiles
in the compile gate; each erratum names its CP; the gate fires on a KB citation of a CP id that does
not exist (negative control); `grep -rn "pnut_ts" deliverables/ai/P2` = 0.

## §7 Stephen's decisions Q1–Q8 (2026-10-09)

Recorded in the study (*Stephen's decisions on the queued questions*): delete
`debug_interrupt.yaml` `memory_usage`; drop `high_side_weak_with_low_side_floated` and its register
self-cite; remove the unsourced Serial Device "3.3 V supply"; tree hygiene — remove
`deliverables/ai/P2/CHANGELOG.md`, `.git-hooks/`, `language/pasm2/add-missing-oneliners.py`, move
the encoding reference (D-D), drop README's *Release record* section.
**Verify:** `find deliverables/ai/P2 -type f ! -name '*.yaml'` returns only `README.md`; the
generator writes to its new path.

## §8 Registers and registries

Register entries annotated/closed as their rows land (F-xxx in study scope; F-352; F-336 closed with
no content; PENDING-VALIDATION entries close when the release serves them); `KNOWLEDGE-GAPS.md` rows
answered by EF-093..EF-101 moved; `SOURCE-ERRATA.md` E-020..E-023. Doc-audit instrument findings
(below) fixed.
**Verify:** register hygiene check clean; `audit-guide-conformance.py --inventory` 0 findings.

## §9 Release (release-yamls, incl. §1.5)

Index regenerated after the commit; root `CHANGELOG.md` entry written from the diff; §1.5
change-set audit by fresh adversarial agents, recorded in `correction-sweeps/`; Stephen's review;
tag and push with him; then «#398» (server release, live probes, F-439).

---

## Documentation Blast Radius

`DOC_AUDIT_COMMAND` (`audit-guide-conformance.py --inventory`), run 2026-10-09 — reported:

```
FAIL  2 finding(s) across 2 file(s)
D1 — RESTATED VOICE RULE — engineering/document-production/app-notes/APP-NOTE-VOICE-GUIDE.md:185
D4 — CODENAME "Silicon Doc" — engineering/document-production/manuals/p2-errata/creation-guide.md:28
```

Both are sprint scope (§8). Other artifacts this sprint's changes describe:
- **Root `CHANGELOG.md`** — the close-out entry (always in scope).
- **`deliverables/ai/P2/README.md`** — loses its *Release record* section (Q8); its claims ("Entries
  cite the Parallax document…") checked against the result.
- **Skills** `release-yamls` / `yaml-knowledge-base-maintenance` — gate names and counts for §1's new
  gates.
- **Counts**: the DoD runner's gate list; `audit-kb-code-compiles.py` totals; the study's row count.
- **Duplicated material:** the encoding reference (generated) moves to one home (D-D).

## Named unknowns

- **VO-J-035's result** («#409»): the USB page's on-the-fly sentence waits on it.
- **S-390**: what the parallax.com article lists as code author.
- **E-023 (C_Z in PASM)**: whether the document or the compiler is the party in error — filed as a
  disagreement either way; Parallax decides.
- **§2's unsourced examples**: how many blocks have no source for their behaviour (removed per D-B);
  known only as each row is worked.

## Revision log

*(none yet)*
