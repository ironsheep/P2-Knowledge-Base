# P2KB close-out sprint — plan

**Head / element:** `yaml:p2kb`. **Seeded by** the close-out study
`engineering/analysis/2026-10-08-p2kb-close-out-study.md` (steps 0–10 done) and its evidence folder
`engineering/analysis/2026-10-08-p2kb-close-out-evidence/`. **This plan points at the study and the
registers; it does not restate them.** A row's defect, evidence and change spec live on its `S-NNN`
row (and the evidence file it names); a register entry's state lives in
`engineering/operations/P2KB-CORRECTION-FINDINGS.md`; a bench fact lives in
`engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md`.

**Status:** STARTED 2026-10-09 (Stephen's go: "if we can start the sprint without having to wait
let's do so"). Sprint-start record below; next: `plan-to-tasks`.

---

## §0 Open questions (each with a recommendation; asked one at a time)

1. ~~What does a KB entry cite for a fact our own compile proved?~~ **RESOLVED 2026-10-09 (study
   Q12):** a separate compile-proof register, `CP-NNN` — "to keep our registers pure". Legality facts
   stay CP; behaviour facts move to EF when a P2 run proves them. Citations are internal provenance.
   Built in §6.
2. ~~Citation format for the S-392 rewrite~~ — **settled by standing ruling** (doctrine, Q3,
   2026-10-09: "A claim learned from our capture of a Parallax document cites that document (title,
   edition, section or page), not our file"). Applied: `"<Parallax title> <edition>, <section
   heading>"`, plus `p.N` for paginated PDFs; no line numbers or repo paths. Citations are internal
   provenance (Q12), so the format serves the auditor and the gate.
   **Canonical citation titles** («#412», read off each document's own cover/footer; the gate's
   `CANONICAL_TITLES` in `audit-yaml-claim-sourcing.py` carries the printed alternates and the
   file:line provenance; codenames such as "Silicon Doc" are refused). `p.N` is required where
   marked **P**. Document → citation title · edition form:
   - Silicon doc → `Parallax Propeller 2 Documentation` · `v35 (Rev B/C silicon)`, section
   - Spin2 → `Parallax Propeller 2 Spin2 Language Documentation` · `v55`, section
   - PASM2 manual → `Propeller 2 Assembly Language (PASM2) Manual` · `Nov 1, 2022 Release` **P**
   - Datasheet → `Parallax Propeller 2 (P2X8C4M64P) Datasheet` · `2022/11/01` **P**
   - Hardware manual → `Propeller 2 P2X8C4M64P Hardware Manual` · `Nov 1, 2022 Release` **P**
   - P2 Instructions sheet → `P2 Instructions` · `v35 - Rev B/C Silicon`, row/section
   - Spec sheet → `Propeller P2X8C4M64P (P2) Multicore Microcontroller Spec Sheet`, section
   - Eval Board → `Propeller 2 Eval Board Rev C (64000)` · `v2.0 29/6/2020` **P**
   - Edge Module → `P2 Edge Module Rev D (#P2-EC)` · `v3.0 6/3/2022` **P**
   - Edge 32MB → `P2 Edge Module with 32MB RAM (#P2-EC32MB)` · `v2.0 5/23/2022` **P**
   - Edge Breakout → `P2 Edge Breakout Board (#64029)` · `v1.0 03/01/2023` **P**
   - Edge Mini Breakout → `P2 Edge Mini Breakout Board (#64019)` · `v1.1 11/30/2020` **P**
   - Edge Breadboard → `P2 Edge Module Breadboard (#64020)` · `v1.2 01/07/2021` **P**
   - Add-on Boards → `P2 Eval Add-on Boards (#64006 Series)` · `v2.0 1/12/2021` **P**
   - Motor Driver → `Universal Motor Driver P2 Add-on Board (#64010)` · `v2.0 5/5/2022` **P**
   - microSD → `P2 microSD Add-on Board (#64009)` · `v1.0 22/02/2021` **P**
   - RTC → `P2 RTC Add-on (#64013)` · `v1.0 11/29/2022` **P**
   - HD Audio → `P2 HD Audio Add-on Set (#64014)` · `v1.0 10/16/2022` **P**
   - HyperRAM/Flash → `P2-ES Eval HyperRAM/Flash Add-on (#64004-ES)` · `1.0 11/5/2019` **P**
   - WX Adapter → `P2 WX Adapter Add-on Board (#64007)` · `v1.0 11/12/2020` **P**
   - WX Wi-Fi → `Parallax WX ESP8266 Wi-Fi Modules` · `v1.0 05/12/2016` **P**
   - Prop Plug → `Prop Plug (#32201) Rev E` · `v3.0 2/03/2021` **P**
   - Click Adapter → `P2 mikroBUS Adapter` · `Part Number 64008, Revision A` (one-page schematic)
   Not citable by title (source listings with no printed title): the ROM booter and the flash
   loader. Not Parallax-authored, so never cited: Smart Pins (Titus), TAQOZ guide, HUB75 notes.
3. ~~`pnut_ts` → `pnut-ts`~~ — **not a question**: the only installed executable is `pnut-ts`
   (`which`, 2026-10-09), so the KB's `pnut_ts` is a defect seen, fixed under *fix everything seen*.

### §0.2 Design decisions to flag (overlay: confirm each before edits start)

- **D-A** Gates land before content (§1 before §2–§7) — sequencing; follows *Gates must run when the
  fix is cheap*.
- **D-B** The compile-gate drain (§2) edits each failing block to compile *and* agree with its
  source (F-381); where no source states the example's behaviour, the block is removed, not invented
  — follows *no unsourced claims* and *our reasoning is not a source* (Sacred Rule #7 for any
  `related:` it held).
- **D-C** Rows whose fix is "remove" remove the claim; nothing is rewritten from memory — same rulings.
- **D-D** **Decided 2026-10-09 (A):** the generated PASM2 encoding reference is deleted, not moved —
  "not versioning a generated file is the right fix here"; `gen-pasm2-encoding-reference.py` (default
  output `/tmp`) is its only source.
- **D-E** Proven compiler-vs-document disagreements filed as `SOURCE-ERRATA` E-020..E-023, each
  pointing at its CP record — follows Q9 and Q12.

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

**Tree state at planning (sprint-start check, 2026-10-09):** on `main`; uncommitted
`deliverables/ai/p2kb-index.json(.gz)` = the 2026-10-07 local regeneration carrying the delivery
filter (schema 3.6.0, «#398»; its `remove_fields` already strips `documentation_source`,
`enhancement_source`, `source`, `sources` … from served content). Left as is; §9 regenerates the
index after the release commit. The VO-J-035 test («#409») was then committed (439771aa).

## Sprint start (2026-10-09)

- **Outgoing build: KB v1.24.0** — the planned v1.24.0 is this release (standing ruling, 2026-10-08:
  "v1.24.0 folds into the single close-out release"; last release v1.23.3).
- **Working tree** (`git status --short`, live): the index pair above (left as is; §9 regenerates)
  and «#409»'s files — VO-J-035 run 1 recorded in the campaign README and the VO row, and the test
  under rework (its run 1 was NO VERDICT from a rig defect). «#409» runs alongside the sprint and
  commits its own change set; nothing in §1–§4 or §6–§8 waits on it. §5's USB-page sentence waits on
  its EF (Named unknowns).
- **Tracking readiness:** 162 completed tasks archived (`tasks/archives/archive_20261009_201229.md`);
  42 obsolete context keys deleted (superseded resume snapshots, breadcrumbs of finished tasks) after a
  dump (`tasks/backups/project_dump_20261009_201229.json`) — 82 keys remain. Leftover tasks: «#387»
  (register open set) is subsumed by this sprint's tasks and closes when they are generated; «#398»
  is §9's server half and follows the sprint; «#373» (P2 Errata) waits on Chip's amendment, outside
  this sprint. `MEMORY.md` is at 150 lines (the audit threshold): a feedback-to-doctrine routing pass
  is owed, not a readiness blocker. **Verdict: ready.**
- **Entry baseline** (`python3 engineering/tools/validate-dod-release.py`, re-run live): unchanged
  from the measurement above — every gate PASS except KB Code Compiles, 352 FAIL in 176 files, all
  352 REGISTERED, 0 unregistered. These are §2's scope, not a deferral. The exit check compares
  against this run.

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

**Built «#410» (2026-10-09) — red by design; §2–§8 drive each count to 0.** Each count names the
script that produced it, run from the repo root on the working tree (HEAD `EF-102`, the two index
files uncommitted as of the sprint start):

| Gate (row) | Script | Today's count |
|---|---|---|
| S-382 / S-200 plain scalar cut by ` #` | `audit-yaml-plain-scalar-comment.py` | **52** flagged in **15** files (168 comment-after-plain scalars seen; 1,129 files) |
| S-383 / F-364 `yaml_file:` pointer | `validate-crossref-keys.py --negative-control` | gate already existed; owed control added (dangling, bare, good); no population count (0 dangling) |
| S-384 / F-441 index sha256 vs HEAD blob | `audit-index-integrity.py --limb sha256` | working-tree index: **21** stale of 1,130; `--committed-index`: **38** stale + **1** path absent at HEAD of 1,131 |
| S-385 / F-405 index freshness | `audit-index-integrity.py --limb fresh` | working-tree index differs from a fresh regeneration at HEAD (**21** entries, **24** alias keys, `total_aliases`); gz pair consistent (`--limb gz` clean) |
| S-386 / F-454 revision scope | `audit-hardware-revision-scope.py` | **12** findings in **7** of 29 files: R-A **7** (of 8 revision-declaring), R-B **5** |
| S-387 / F-389 directory-term findability | `audit-index-findability.py` | **8** partial-reach directories (**135** files unreachable); advisory **14** reached-by-none (**423** files); 31 qualifying |
| S-388 / S-256 one-line code keys | `audit-kb-code-compiles.py` | net 3 = **204** candidates in **86** files under 13 keys (136 of them compiler-code-bearing); all decided in the manifest: **113** fragment, **5** program, **3** never, **83** not-code; **23** FAIL (**18** `S-137` `;` comments, **5** `S-256`) |
| S-389 / D3 bare constant | `audit-kb-code-compiles.py` | **7** `BARE-CONST` blocks, **10** sites, in 5 files (`false`, `true`, `negx`, `posx`, `multi_cog_synchronization`); all registered `S-162` |

Compile gate totals (`audit-kb-code-compiles.py`, full sweep): **375** FAIL + **7** BARE-CONST =
**382** problems on **379** blocks in **197** files, all REGISTERED (was 352 FAIL in 176 files).
Manifest reconciliation: before, 354 `finding:` entries in 176 files against 352 FAIL — two entries
(`language/pasm2/orgf.yaml examples[2].code` `S-168`, `language/pasm2/xoro32.yaml critical_warning.solution`
`S-023`) named a finding on a block that compiles; those two `finding:` lines were removed (the S-rows
stay open in the study). After: 379 entries with `finding:` = the 379 failing blocks.

**Built «#412» (2026-10-09) — the sourcing gate accepts only Parallax documents, EF, CP; red by
design, driven to 0 by the citations task.** `audit-yaml-claim-sourcing.py` (script that produced every
number; run from the repo root on the working tree, 999 files scanned). Before: PASS, 0 Tier 1, 27
Tier 2 advisory. After (titles read off the documents' own covers — see §0 Q2): **FAIL — 33 Tier 1 +
1,438 BAD_CITATION**, Tier 2 **123** (advisory). BAD_CITATION by class, counted per citation value:
extraction path **523** · register path **30** · KB-file pointer **21** · line locator **133** · batch
label (`parallax-quick-bytes`) **42** · bookkeeping word (`documentation_source:
enhanced/original/p2_datasheet/…`) **49** · title without edition **1** · paginated PDF without
`p.N` **42** · other (no printed Parallax title, EF or CP) **597**. (First cut, titles taken from the
dashboard's row names: NO_EDITION 9, NO_PAGE 76, other 214, total 1,097, Tier 1 37, Tier 2 121 —
superseded; it accepted informal names the documents never print.) The large "other" class is mostly
informal names the KB uses today — `PASM2 Manual 2022/11/01 Pages 31-147`, `64013 P2 RTC Add-on
Guide`, `P2 Datasheet` — which «#422» rewrites to the canonical titles. Tier 1/Tier 2 grew because a
block's citation no longer counts unless it passes the same rule. The `enhancement_source:`
lines (356) are not flagged — they simply stop counting; their deletion is «#422». **Owed to the
citations task:** the Tier-2 switch-on (`TIER2_BLOCKING` in the script, or `--tier2-blocking`) after
S-295..S-307; the OBEX-metadata-vs-index check (S-308c) is not built. The compile-proof register's
`*KB:*` home check lives in `validate-dod-release.py::validate_ledger_kb_home` (CP entries added to
`LEDGERS`).

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
`deliverables/ai/P2/CHANGELOG.md`, `.git-hooks/`, `language/pasm2/add-missing-oneliners.py` and
`language/PASM2-ENCODING-REFERENCE.md` (D-D: not versioned; the generator is its source — its
docstring gains a line saying the output is never committed), drop README's *Release record* section.
**Verify:** `find deliverables/ai/P2 -type f ! -name '*.yaml'` returns only `README.md`; the
generator still runs to `/tmp`; no live doc links the deleted files (`git grep` — the dated audit
report and the study keep their historical mentions).

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
- **Duplicated material:** the generated encoding reference is removed (D-D); the YAMLs are the one
  home for encodings.
- **New register:** `compiler-verification/COMPILE-PROOFS.md` + README (§6); the ingestion dashboard
  and the `ingest-source` / verification skill text that name the proof registers gain it.

## Named unknowns

- ~~**VO-J-035's result** («#409»)~~ — **decided 2026-10-09: EF-102, SURVIVES.** The USB page states the
  P2 Documentation's on-the-fly sentence for the baud, cited to EF-102, in «#419».
- **S-390**: what the parallax.com article lists as code author.
- **E-023 (C_Z in PASM)**: whether the document or the compiler is the party in error — filed as a
  disagreement either way; Parallax decides.
- **§2's unsourced examples**: how many blocks have no source for their behaviour (removed per D-B);
  known only as each row is worked.

## Tasks (plan-to-tasks, 2026-10-09)

**Shape.** Rows were mapped to sections and KB areas by a read-only survey (396 study rows: §1 13, §2
106, §3 235, §4 7, §5 8, §6 7, §7 5, §8 2, closed/no-op 13). §2 and §3 rows share files heavily (e.g.
`constructs/repeat.yaml` carries §2, §3, §4 and §6 rows), so **§2 and §3 are worked together per KB
area**, each file opened once; §5's EF results land in the area task that owns the page. The
tree-wide sweeps (§4 citations, S-396) run after the content tasks so no citation is rewritten on a
block about to be removed. The compile manifest counts 353 entries in 175 files against the gate's
352 FAIL in 176 — reconciled in «#410».

| Plan § | Deliverable | Task | seq |
|---|---|---|---|
| §1 | Gates: plain-scalar, pointer control, index integrity, revision scope, findability, one-line code, D3; manifest reconcile | «#410» | 1 |
| §6 (1–2) | Compile-proof register, CP-001..004, E-020..E-023 (two-phase) | «#411» | 2 |
| §1 (S-308, S-393) | Sourcing gate: Parallax docs, EF, CP only | «#412» | 3 |
| §7 | Stephen's Q2/Q6/Q7/Q8 decisions + D-D tree hygiene | «#413» | 4 |
| §2+§3 | language/spin2 methods | «#414» | 5 |
| §2+§3+§5 | spin2 concepts/constructs/symbols (+EF-101) | «#415» | 6 |
| §2+§3 | spin2 operators — F-547 cascade, S-310..S-315 | «#416» | 7 |
| §2+§3 | spin2 preprocessor/conventions/patterns (S-153 class) | «#417» | 8 |
| §2+§3+§5 | language/pasm2 (+EF-094, EF-101) | «#418» | 9 |
| §2+§3+§5 | architecture + smart-pins (+EF-093, 095–100; F-563) | «#419» | 10 |
| §2+§3 | hardware, guides, fundamentals, app notes, tools, code-examples | «#420» | 11 |
| §6 (3–5) | Teach what compiles (CP); S-396 `pnut_ts` sweep | «#421» | 12 |
| §4 | Citations and provenance (S-292, 293, 327, 328, 390, 391, 392) | «#422» | 13 |
| §8 + Blast Radius | Registers, gaps ledger, guide-conformance, docs | «#423» | 14 |
| §9 | Release KB v1.24.0 (§1.5 audit, Stephen's review), then server, F-439 | «#398» | 15 |
| §5 (VO-J-035) | Bench round 2 — done, EF-102 (SURVIVES); the USB sentence lands in «#419» | «#409» | — |

«#387» (the register's open set) superseded by «#410»–«#423». «#373» (P2 Errata, waiting on Chip) is
outside this sprint, seq 16.

**Dispatch.** `arbiter-serial` (the project default for the YAML head): every area task edits shared
KB files and the compile manifest, so no two run at once. **Two-phase:** «#411» (the CP register's
shape is consumed by «#412», «#421» and every CP citation). **Atomic green-units:** «#410» and «#412»
leave new gates red on today's population by design. Each body says so, and the area tasks and
«#422» drive them to 0. **Gate over the sprint's output:** «#423» runs the exit baseline after every
content task; the §1.5 change-set audit in «#398» follows it.

**Undetermined rows carried into their tasks** (resolved from the source in the pass, or the claim
removed and a blocker registered): S-333, S-349, S-361, S-319, S-379, S-315 (page list), S-327 (census),
S-370, S-374, S-390, S-391, S-322 item 1 (#64013 schematic), F-352, F-562.

## Revision log

- 2026-10-09 — sprint started; tasks «#410»–«#423» generated; «#387» superseded; F-563 (USB status
  bits, found by «#409») added to «#419»'s scope.
- 2026-10-09 — «#414» boundary: the DoD's *Internal IDs in Shipped Content* check caught an `EF-099`
  written into served prose; its pattern now also covers `CP-NNN` and `E-NNN` (both internal registers)
  and found two errata ids in served text, fixed. Every area-task brief («#415»–«#422») names this check
  among the agent's narrow checks: an id belongs in a stripped field (`source:`/`sources:`), never in
  served prose.
- 2026-10-09 — VO-J-035 rerun SURVIVES → EF-102; «#419» now writes the on-the-fly WXPIN sentence (baud
  only) on the USB page, cited to the P2 Documentation and EF-102.
