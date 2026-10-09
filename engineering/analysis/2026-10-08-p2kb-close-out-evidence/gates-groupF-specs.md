# Close-out study, group F: gate build specs (F-364, F-405, F-441, F-454, F-389, S-200, S-256, S-308, D3)

Task «#407», group F. Study freeze: nothing in the KB, the register, the study or any gate script was edited;
no gate was run. Written 2026-10-09. Paths are repo-relative. Populations below were measured with read-only
scratch scripts (reproducers in the "Reproduce" line of each section; they live in the session scratchpad
`/tmp/claude-1000/-workspaces-P2-Knowledge-Base/fd20d1c1-e1ec-45fc-a5bc-7f395c46f9e1/scratchpad/gatesF/` and are
not part of the repo).

Conventions every new script follows (read from `audit-yaml-duplicate-keys.py`, `audit-kb-code-compiles.py`,
`audit-gate-arming.py`, `validate-dod-release.py::_run_gate`):

- Lives in `engineering/tools/validation/audit-<name>.py`, `#!/usr/bin/env python3`, a module docstring that opens
  with the one-line question, then **WHY THIS EXISTS** (the finding id), **Usage**, **Exit** and what a green does
  NOT certify. Repo root: a script run from the repo root uses cwd-relative defaults (`deliverables/ai/P2`) like
  `audit-yaml-duplicate-keys.py`; a script that needs the root explicitly uses `audit-gate-arming.py::repo_root()`
  (walk parents for `.git` + `engineering/`; fail loudly — a `.backups` copy is never a valid control).
- Exit **0** clean · **1** defects found (release blocks) · **2** the tool could not audit (no files, tool missing,
  unreadable manifest) — and `_run_gate` treats 2+ as a FAILURE: *nothing audited is never a pass*. A scan that
  finds zero candidates exits 2, not 0.
- `--negative-control` plants every defect class it claims to catch plus the cases that must stay clean, prints one
  `[PASS]/[**FAIL**]` line per case and ends with a line starting `Negative control PASSED`/`FAILED` (that is the
  prefix `_run_gate` quotes as the verdict); exit 0 only if every case behaves.
- Wiring = three things, all required for `audit-gate-arming.py` to see ARMED and for the gate to be a gate:
  (1) a `validate_<name>()` in `engineering/tools/validate-dod-release.py` that calls `_run_gate(result, script,
  ['--negative-control'], "negative control", verbose)` then `_run_gate(result, script, [], "audit", verbose[, timeout=N])`,
  with a `Scope:` info line saying what a pass is not, **and its name added to the `validations` list** in
  `run_all_validations`; (2) the script's file name added to `HEADS["yaml"]` in `audit-gate-arming.py` (else it is
  reported UNASSIGNED); (3) a line in the skills that make an agent run it — `release-yamls` §5.5 (pre-release
  command list) and, for edit-time gates, `yaml-knowledge-base-maintenance` §2.5/§2.6. The meta-gate counts a runner
  mention only in code (docstrings and comments are stripped) and a skill mention anywhere in the SKILL.md.

---

## Summary table

| Gate | Catches | Today's population | Home | Invoked by |
|---|---|---|---|---|
| **S-200** `audit-yaml-plain-scalar-comment.py` (new) | a YAML plain scalar silently cut by a same-line ` #` comment | **52 flagged** scalars in 15 files (of 168 comment-after-plain; 47 R1 + 5 R2, 26 R3, 4 R3-only); 0 after the S-183 edit | new, beside `audit-yaml-duplicate-keys.py` | `validate_plain_scalar_comment` in `validate-dod-release.py` (60 s); `yaml-knowledge-base-maintenance` §2.5; `release-yamls` §5.5 |
| **F-364** pointer fields | a `yaml_file:`-style pointer to a file that does not exist | **0** dangling (3 `yaml_file:` pointers, all resolve; 0 unresolved bare-path pointer values in any non-`related` field) | **already built**: `validate-crossref-keys.py` path-token pass (F-340/F-373, 2026-09-13) — only a negative-control case is owed | `validate_cross_references` (60 s / 120 s nc); `release-yamls` §5.5, §6c |
| **F-441** index sha256 vs committed blob | an index entry whose `sha256` is not the SHA-256 of `git show HEAD:<path>` | committed index: **38 of 1131** entries stale vs HEAD; working-tree (throwaway) index: **21 of 1130**; +1 indexed path absent from HEAD. Expected after step 6b: 0 | new `audit-index-integrity.py`, limb `sha256` | `validate_index_integrity` in `validate-dod-release.py` (300 s); `release-yamls` §6c |
| **F-405** index freshness | a committed index that a fresh regeneration at HEAD would change (and the dup-key / gzip limbs already wired) | committed index is stale today (same 38 entries); gzip pair **consistent** at HEAD and in the working tree | same script, limb `fresh` (post-commit only) | same runner function; `validate-dod-release.py --post-commit` in `release-yamls` §6c (600 s, unmeasured) |
| **F-454** `audit-hardware-revision-scope.py` (new) | an absolute maximum / rating stated without the board revision it holds for | **8** hardware files declare a revision, **1** carries a revision-scope block; **5** rating scalars in **3** files lack a revision qualifier | new, yaml head | `validate_hardware_revision_scope` (60 s); `yaml-knowledge-base-maintenance` §2.5; `release-yamls` §5.5 |
| **F-389** `audit-index-findability.py` (new) | a directory term that reaches only some (or none) of the directory's files through key + alias + category | **8** directories (135 files) reached partially, incl. `debug-commands` (4 files: `c-z`, `dly`, `pc_key`, `pc_mouse`); 14 directories (423 files) reached by none — structural, needs a reviewed allow-list | new, reads the index; baseline file for the reviewed exceptions | `validate_index_findability` (60 s); `release-yamls` §6c |
| **S-256** one-line code net (extension) | one-line real programs under non-code keys outside the ENH-03 net | **123** candidates under 13 seed keys in 51 files; the whole one-line population the compiler classes as code is 1,703 (mostly `syntax:` notation, not proposed) | extend `audit-kb-code-compiles.py` + new data `kb-compile-manifest/_oneline-code-keys.yaml` | already: `validate_kb_code_compiles` (900 s) |
| **D3** bare constant as PASM operand (extension) | `mov flag, TRUE` — a constant used as a bare D/S operand | **8** sites in **6** blocks in 4 files (`false`, `true`, `negx`, `posx`.yaml), all built-in constants; **0** user lower-case CON constants in the gated blocks | extend `audit-kb-code-compiles.py` (new problem kind `BARE-CONST`) | already: `validate_kb_code_compiles` (900 s) |
| **S-308** claim-sourcing change | wholly-uncited files advisory; example blocks and `part\d+-….txt` cites mis-tiered | study row S-308 (27 Tier-2 blocks per the F-381 paragraph) | existing `audit-yaml-claim-sourcing.py` | already: `validate_claim_sourcing`; `release-yamls` §1 |

---

## S-200 — `audit-yaml-plain-scalar-comment.py` (build spec; rule from `rows-S162-S219-specs.md` §"S-200 gate")

**Catches.** S-183: `- MOV reg, #42` is parsed as the scalar `MOV reg,` with the comment `#42`. Every other gate reads the
parsed value, which looks fine; the compile gate sees the cut text only where the cut leaves illegal code.

**Rule (exact).** `yaml.compose_all(text, SafeLoader)` per file under `deliverables/ai/P2`; for every `ScalarNode` with
`style is None` (plain), take the source line at `end_mark.line`; if `line[end_mark.column:]` matches `^\s*#`, record
(file, line, served value, lost text). **Flag** when any of:
- **R1** the character after `#` is not a space (`#42`, `##addr`, `#@label`);
- **R2** the scalar is empty (a key or `- ` item with nothing before the comment);
- **R3** the scalar contains whitespace (a multi-word value followed by a comment).
**Allow** a comment after a single-token plain scalar with a space after the `#` (`- language/pasm2/rep.yaml  # note`,
`133  # Per datasheet`). Block scalars (`|`, `>`) and quoted scalars are never plain, so they are not touched.

**Population today (measured, `deliverables/ai/P2`, 1,130 files, 2.5 s wall).** 168 comment-after-plain occurrences;
**52 flagged** in 15 files (R1 47, R2 5, R3 26 — overlapping; 4 are R3-only: `calld.yaml:51`, `branch_addressing.yaml:40,41,80`).
This reproduces the reviewer's 52. The 5 R2 sites are all `addressing_modes.yaml:16,17,88,130,131`. After the S-183 edit the
rule must give 0 (the gate and the edit ship in one release). No allow-list entry for the `encoding:  # [bits|write|…]` header
is needed on today's tree: that comment follows a mapping key whose value is a nested mapping, so `end_mark` is the key and the
remainder starts with `:`.
Reproduce: `python3 …/scratchpad/gatesF/pop1.py`.

**Negative controls (scratch YAML per case).** Must FIRE: `- MOV reg, #42  ' x` (R1+R3); `- CALL #target` (R1); `key:  # note`
(R2); `- JMP vector  # Jump to address` (R3); `syntax: CALLD PA|PB,  #label` (R1). Must NOT fire: `- language/pasm2/rep.yaml  # note`;
`133  # Per datasheet`; `- "MOV reg, #42"` and `- 'MOV r, #1'` (quoted); a `|` block holding `mov a, #1`; `key: a#b` (no whitespace
before `#`, so not a comment); a file with no comments (positive control). A case file that fails to parse is a gate failure, not a skip.

**Home / wiring.** New file beside `audit-yaml-duplicate-keys.py`; `validate_plain_scalar_comment()` in `validate-dod-release.py`
(`_run_gate` nc + audit, default 300 s is ample, measured 2.5 s; use 120 s), added to `validations`; `HEADS["yaml"]`; edit-time: replace the
prose paragraph at `yaml-knowledge-base-maintenance` §2.5 ("Also check what YAML did to any line holding a `#`") with the command;
`release-yamls` §5.5 list.

**A green does NOT certify.** That every `#` in a served string survived: a *quoted* scalar that itself lost text, a flow
`[a, b #c]` collection, and a plain scalar whose `#` is preceded by non-whitespace are outside the rule. Nor that the quoting is
semantically right — only that nothing is cut by a comment.

---

## F-364 — pointer fields (`yaml_file:`): the gate already exists; one control is owed

**Defect class.** An index/entry names a file by a pointer field that nothing resolves (F-364: 13 of 16 `yaml_file:` pointers dangled while
`validate-crossref-keys.py` stayed green because it then validated `related:` only).

**Finding (read from the code, not run).** The register says "the gate reading `yaml_file:` is not built" (re-verified 2026-10-05). The
validator's own header (`validate-crossref-keys.py:5-9`) and `check_document` (`:603-610`) show otherwise since F-340/F-373 (2026-09-13):
`iter_strings` feeds **every string value at every depth** to `PATH_TOKEN` (`:440`, matches a bare `name.yaml` too), and `check_path_token`
(`:547-567`) fails a token that is not a KB-root-relative existing file (`missing` / `not_full_path`; `_index.yaml` alone may list siblings
by bare name). A `yaml_file: dual-pa-register.yaml` pointer would therefore be reported today. What is genuinely missing is **proof**: the
negative control (`:655-671`) plants no `yaml_file:` case, so nothing shows the gate sees *that* field. (The register entry is not mine to edit;
the arbiter should reconcile it.)

**Spec = one change to an existing gate.** Add two cases to `run_negative_control`:
`('nc/yaml_file_dangling.yaml', {'registers': [{'yaml_file': 'architecture/system-registers/no-such-register.yaml'}]}, 'missing')` and
`('nc/yaml_file_bare.yaml', {'registers': [{'yaml_file': 'dual-pa-register.yaml'}]}, 'missing')`; keep a `yaml_file:` pointing at the real
`architecture/system-registers/ptra-register.yaml` as a must-stay-clean case. No new script, no new wiring (already `validate_cross_references`,
60 s + 120 s nc, and `release-yamls` §5.5/§6c).

**Population today.** 3 `yaml_file:` pointers (`complete-system-registers-index.yaml:126,149,161`), all resolve; across every
scalar whose whole value is a bare `*.yaml` path under a key other than `related` (`group_file` 31, `path` 28, `canonical` 16, `file` 16 …) and every
such list item under `see_also` 160, `composes` 89, `patterns` 34 …, **0 unresolved** (anchor tried: own directory, KB root, repo root — a gate must use the KB-root form the validator already enforces).
Reproduce: `python3 …/scratchpad/gatesF/pop3.py`.

**A green does NOT certify.** That the pointer names the *right* file, only that a file exists. A pointer without a `.yaml` suffix, or one split across prose, is not seen.

---

## F-441 and F-405 — `audit-index-integrity.py` (new): the index agrees with what is committed

**Defects.** F-441: v1.19.1 shipped an index carrying the pre-change SHA-256 of two edited files; the MCP refused to serve them. F-405: the
index and `.gz` drifted (F-357 recurred), the index was also stale against later content commits, and nothing ran the validator.

**State of F-405's two owed halves (read).** (1) `audit-yaml-duplicate-keys.py` **is** wired (`validate_duplicate_keys`, `validate-dod-release.py:977`);
and `validate-dod-release.py` **is** now invoked by a skill (`release-yamls/SKILL.md` lines 301 and 450, and `baseline-health/project-overlay.md`).
(2) The freshness check is **not built** (`grep -i fresh` in the runner: nothing; the runner's `validate_gzip_compression` checks pair parity only).
F-441's owed sha256-vs-blob check is likewise not built (the skill says so at `release-yamls` lines 416-421: "no gate does").

**Rule — three limbs, one script, `--limb sha256|fresh|all`, default all.**
- **sha256 limb.** For each entry in `deliverables/ai/p2kb-index.json` `files`, `sha256` must equal SHA-256 of `git show HEAD:<path>` (the exact
  bytes `generate-p2kb-index.py::get_git_blob_sha256` hashes). One `git cat-file --batch` for all paths. FAIL on mismatch, on a path missing
  at HEAD, and on a HEAD-tracked YAML under `deliverables/ai/P2` that has no entry. Valid at **both** moments `validate-dod-release.py` runs:
  at §5.5 the throwaway index was generated at the same HEAD, so every sha equals the HEAD blob; after a collapsed 6a/6b (F-441) HEAD has moved and it fails.
- **fresh limb (post-commit only).** Clone the repo locally into a temp dir (`git clone --local`), `import` `generate-p2kb-index.py` and call
  `generate_index(clone_root)` there (the module writes only in `main()`, so nothing in the working tree is touched), then compare to the working-tree
  index **ignoring `system.generated`**. FAIL if anything differs. It is valid only when `git status --porcelain -- deliverables/ai/P2` is empty
  (aliases and categories come from working-tree YAML, so a dirty tree would false-red at §5.5). Dirty tree without `--post-commit` → limb prints
  `SKIPPED (uncommitted YAML — expected before step 6a)` and the exit is decided by the sha256 limb; with `--post-commit` a dirty tree is **exit 2**.
- **pair limb is not duplicated** — `validate_gzip_compression` already compares the gzip to the JSON byte for byte.

**Population today.** Committed index vs HEAD blobs: **38 of 1,131** entries stale (+1 indexed path absent from HEAD) — the index was last regenerated
before later content commits. Working-tree (throwaway) index vs HEAD: **21 of 1,130** (it was generated at an older HEAD, git status ` M`). Pair parity:
identical in both HEAD and working tree. Red today by design; the expected state after §6b is 0.
Reproduce: `python3 …/scratchpad/gatesF/pop2.py` (second half).

**Negative controls (scratch git repo, 3 YAMLs).** Must FIRE: an index regenerated, then one file edited and committed (F-441 shape) → sha256 limb;
an index entry whose `sha256` is flipped one hex digit; an index entry for a path deleted at HEAD; a committed YAML with no entry; an index missing one
alias that regeneration would add (fresh limb, clean tree). Must NOT fire: an index regenerated after the commit (positive control); `system.generated`
alone differing; the fresh limb on a dirty tree without `--post-commit` (prints SKIPPED, does not fail); with `--post-commit` that same dirty tree must
exit **2**, not 0.

**Wiring / timeout.** `validate_index_integrity(verbose)` in `validate-dod-release.py`, nc + audit; sha256 limb alone is seconds (300 s default fine);
the fresh limb runs the generator (≈1,130 `git log`/`git show` calls) — **not measured here**, so give it `timeout=600` and record the measured wall time
in the docstring on first run (as «#404» did for the compile gate). `run_all_validations` gains a `--post-commit` flag that passes `--post-commit` through;
`release-yamls` §6c changes to `validate-dod-release.py --post-commit`, §5.5 stays as is. `HEADS["yaml"]`.

**A green does NOT certify.** That the *content* of any entry is right, that the published tree (raw.githubusercontent.com) serves the same bytes — the skill's
"probe the published tree" step is still a separate act — or that the aliases are findable (see F-389).

---

## F-454 — `audit-hardware-revision-scope.py` (new): a rating stated without its board revision

**Defect class.** A *correct* current-revision number stripped of the scope that made it correct (Rev A/B VIN max 5.5 V; Rev C+ 16 V).
No content check can know that a rating differs across revisions — that is in the source's Revision History — so the gate cannot judge the number. What it **can**
enforce is that the author has *made and recorded the decision*, and that a rating in a revision-declaring file carries its scope.

**Rule (exact; key lists are proposals for review).** Scope `deliverables/ai/P2/hardware/*.yaml`.
- **R-A (declared decision).** A file declaring a board revision (top-level `module_revision:` / `board_revision:` / `board_revision_note:`, or a `# Revision:` header line)
  must contain either a `board_revisions:` mapping or a `revision_scope_reviewed:` mapping with non-empty `source:` and `finding:` (e.g. `finding: "Revision History
  lists no rating change"`). Else FAIL: *revision declared, scope never reviewed*.
- **R-B (rating scoped).** In such a file, every string under a rating key (`^(vin|input_voltage|absolute_maximum|supply_voltage|vin_maximum|max_[a-z_]+|[a-z_]+_max(imum)?)$`)
  that holds a number with a V/A/W/Hz unit must name a revision (`\bRev(ision)?[ .]?[A-F]\b`) in the same string, or sit inside the `board_revisions:` mapping. Else FAIL.

**Population today (measured).** 29 hardware YAMLs; **8** declare a revision (`addon-motor-driver`, `edge-standard-module`, `p2-eval-board`, `edge-breadboard-carrier`, `edge-mini-breakout`,
`edge-standard-breakout`, `edge-32mb-module`, `addon-goertzel-touch`), **1** (`edge-standard-module`, the F-454 repair) carries `board_revisions:` → R-A would require a reviewed decision
for **7**. R-B: **5** scalars in **3** files — `edge-32mb-module.yaml:84` (`input_voltage: "5-16 VDC …"`) and `:99` (`vin: "5 V recommended, 16 V maximum"`; module is declared Rev B), `edge-breadboard-carrier.yaml:78-79`
(`input_voltage`, `absolute_maximum: "5.5 VDC"`; Rev B), `p2-eval-board.yaml:63` (`supply_voltage: "USB 5 VDC, absolute maximum 5.5 VDC"`; Rev C). Whether any of those ratings actually differs by revision
is **not established here** (the sources have Revision History sections — `edge-32mb-module-narrative.txt:618`, `edge-module-breadboard-narrative.txt` — I did not read them); the 32 MB module's body says 16 V outright
(narrative lines 93, 113, 537). They are the gate's first review queue, not three known defects.
Reproduce: `python3 …/scratchpad/gatesF/pop6.py` (loose heuristic, 52 scalars/6 files — too noisy to ship) and the strict key grep in the transcript.

**Negative controls.** Must FIRE: a file with `module_revision: "Rev B"` and `vin: "16 V maximum"`, no `board_revisions` (R-A and R-B); `absolute_maximum: "5.5 VDC"` in a revision-declaring file; a file with
`revision_scope_reviewed:` whose `finding:` is empty. Must NOT fire: the real `edge-standard-module.yaml` shape (scalar names Rev, `board_revisions:` present); `vin: "5 V"` in a file declaring no revision;
`vin_maximum: "5.5 V"` inside a `board_revisions:` entry; a file with `revision_scope_reviewed:` + a rating with no Rev token only if the mapping is present and non-empty (R-B waived by the recorded review).

**Wiring.** `validate_hardware_revision_scope()` in the runner (60 s); `yaml-knowledge-base-maintenance` §2.5 (add: "hardware file edited → run it"); `release-yamls` §5.5; `HEADS["yaml"]`.

**A green does NOT certify.** That a rating is right for the revision named, or that the revision history was read correctly — only that the file records a scope decision and that a rating in a revision-declaring file is qualified.
A deleted revision history that leaves no `module_revision` marker (the F-454 mechanism exactly, if the marker went with it) is **invisible** to this gate; the ingestion-side check (source has a Revision History → YAML must carry a decision) would
fire on about 17 board guides, most with no rating change, and is not recommended.

---

## F-389 — `audit-index-findability.py` (new): key generation that makes a subtree unreachable

**Defect class.** The generator abbreviates or drops path components in the key (`debug-commands/c-z.yaml` → `p2kbSpin2DbgCZ`), so the term that names the subtree reaches only some files of it.

**What is decidable.** Reachability of a path term through the three things the index offers a searcher: the key, the aliases that point at it, and its category. (Whether `p2kb_find` searches categories is **not checked** — if it
does not, drop the category from the haystack and re-measure.) What is **not** decidable by a gate: which directory names are *topic* words (`debug-commands`) and which are *structural* (`methods`, `obex`, `keywords`). That needs a reviewed list.

**Rule.** For each directory D (≥3 files, at least two levels below `deliverables/ai/P2`): term = the normalised tokens (split on `-`/`_`, length ≥3) of D's leaf name. `reach(file)` = any token occurs (normalised, substring)
in `key + aliases-of-key + category-names-of-key`. FAIL when **0 < reached < all** (the "partial results" failure mode: some files return, some do not) for a directory not in a reviewed baseline
`engineering/tools/validation/baselines/index-findability.json` (`{directory: reviewed reason}`). Directories reached by **none** are listed (advisory) — they are structural by design today.

**Population today (measured against the committed index).** 31 qualifying directories; **8 partial** (135 files unreachable): `architecture/boot-rom` 5/7, `architecture/system-registers` 2/3, `language/spin2/conventions` 1/6,
`language/spin2/debug-commands` 9/13, `language/spin2/operators` 1/77, `language/spin2/patterns/implementation` 1/19, `language/spin2/preprocessor` 2/14, `language/spin2/registers` 1/18. **`debug-commands` (4 files: `p2kbSpin2DbgCZ`, `…DbgDly`,
`…DbgPcKey`, `…DbgPcMouse`) is exactly the F-389 shape; `boot-rom` looks the same by key name (`p2kbArchP2Monitor`, `p2kbArchTaqozForth` carry neither "boot" nor "rom").** The other six partials have generic leaf names (`operators`, `registers`, `conventions` …) reached by one or two keys; I did not inspect them individually — each is a review decision (fix the alias, or baseline it with a reason). **14 reached-by-none** (423 files),
all structural (`community/obex/objects` 131, `methods` 101, `keywords` 37 …). The F-389 headline term "debug": 30 files have `debug` in their path, 4 are unreachable by key/alias/category (it was 33 of 60 on 2026-08-30; the alias vocabulary has since closed most of it).
Reproduce: `python3 …/scratchpad/gatesF/pop5.py`.

**Negative controls (synthetic index JSON).** Must FIRE: directory `x/debug-commands/` with 4 files whose keys are `…Dbg…` and no alias containing `debug`, one file with an alias `debug` → partial. Must NOT fire: all files reachable; zero files reachable (advisory only); a partial directory present
in the baseline with a reason; fewer than 3 files. A baseline entry with an empty reason is a failure.

**Wiring.** `validate_index_findability()` in the runner (60 s); `release-yamls` §6c (it reads the *regenerated* index, so it belongs after 6b); `HEADS["yaml"]`.

**A green does NOT certify.** That a searcher finds the right file for a real query (`p2kb_find "debug data too long"` returning 0 is a vocabulary gap, invisible to a path-term test); that the baseline's reasons are right; or that `p2kb_find` ranks the file. It certifies only that no
directory's own name reaches some of its files and not others without a recorded reason.

---

## S-256 — one-line code outside the ENH-03 net (extension of `audit-kb-code-compiles.py`)

**Defect class.** Real one-line programs in non-code keys (design §3.1/§11 Q3 accepted the limit for *notation*): e.g. `guides/pasm2-getting-started.yaml` `con_symbols: CON _clkfreq = 250_000_000, _errfreq = 0`, `quick_example: JCT1 #handler …`,
`wrong:`/`correct:` one-liners, `create:`/`update:` DEBUG lines.

**Decision to make (the study row asks it): yes, admit them — by a reviewed key list, not by shape.** Admitting every single-line string the compiler classes as code is not viable: that is **1,703** of the 42,980 single-line scalars outside the code keys, and most are `syntax:` (354),
`syntax_variants` (159), `description` (141) — notation or prose the elementizer misclassifies. (Prefilter then `code_bearing(elementize(...))`, 16,360 strings elementized, 0 aborted.)

**Rule.** New data file `engineering/tools/validation/kb-compile-manifest/_oneline-code-keys.yaml` (`oneline_code_keys: [...]`, "to be reviewed", same header discipline as `_code-keys.yaml`). The finder gains **net 3**: every single-line string scalar under one of these keys is a
candidate and must carry a manifest decision (program | fragment | never | not-code), exactly like net 1/2. Seed list from the measurement: `wrong, correct, quick_example, spin2_examples, create, update, setup, con_symbols, basic, comment, expands_to, sequence, formula`.

**Population today.** **123** candidates under those 13 keys in **51** files (`wrong` 26, `correct` 16, `quick_example` 14, `spin2_examples` 9, `create` 9, `update` 9, `setup` 7, `con_symbols` 7, `comment` 6, `basic` 6, `expands_to` 5, `sequence` 5, `formula` 4). Each needs a
sidecar entry once; many will be `not-code` (`basic: ':='`) or `fragment`. `guides/` alone holds 85 of the net-2 hits. Reproduce: `python3 …/scratchpad/gatesF/s256.py` then `s256c.py`.

**Negative controls.** Add to the harness's NC list: a one-line `correct: result := value * 2` under a seed key with no manifest entry → UNCLASSIFIED (must fire); the same line with `compile: fragment` + assumes → clean; the same string under `syntax:` → not a candidate (must stay outside); a seed key holding prose → needs a `not-code` entry
with a reason (UNCLASSIFIED until added). Adding a key can only widen the net; removing one is a reviewed hunk (existing rule).

**Wiring / timeout.** None new — `validate_kb_code_compiles` (900 s; +123 small compiles, negligible against the 2,450 present).

**A green does NOT certify.** Anything the harness already does not (legality only), and not the 1,580 one-line code-shaped strings under other keys (`syntax:` notation etc.), which stay outside the net by decision.

---

## D3 — bare constant used as a PASM D/S operand (`mov flag, TRUE`)

**Can a gate catch it? Partly. Yes where the symbol table is visible; no where it is not — review must carry the rest.**

**Why the obvious design does not work.** The elementize pass does not resolve user symbols: in `CON myc = 5` / `mov flag, myc` every user name — the constant, the register label `flag`, the label `buf` — is `type_undefined` (probed on a scratch file with
`pnut-ts --pass elementize --log elementizer`). So "a `type_con` token in a register-operand position" is detectable **only for built-in constants** (`TRUE`, `FALSE`, `NEGX`, `POSX`, `PI`, `P_*`…), which the elementizer does type as `type_con_int`/`type_con_float`
(the payload is the value, so the *name* is recovered from the source column, as `parse_elementizer_log` already does for `type_undefined`).

**Rule (in the existing harness, after the block is built and elementized).** For every `type_asm_inst` line (skip leading `type_asm_cond`), split the remaining tokens on top-level `type_comma`; for operand 0 (D) and 1 (S) — a single-token operand with **no `type_pound`** — FAIL (`BARE-CONST`) when:
(a) the token type starts `type_con` **and** the source text at its column is an identifier (so `mov x, 5` is not flagged, `mov x, TRUE` is); or
(b) the token is `type_undefined` whose lower-cased name is in the **constant set** = the manifest entry's `assumes: NAME=con[:V]` names ∪ names declared in the block's own `CON` section (`type_undefined` followed by `type_equal`).
Directives (`long TRUE`, `res`, `orgh`) are `type_asm_dir`, not `type_asm_inst`, so they are not touched. Escape: a manifest entry may list `bare_const_ok: [NAME]` with a mandatory `reason:` (an intentional read of the register at address NAME).

**What it is blind to (stated, not hidden).** A constant the author declared as a plain operand (`assumes: [limit]` without `=con`) — the manifest *says* it is a register; only review can know otherwise. A constant defined in an `#include`d file or another object (no visible declaration). Constants in blocks classed `not-code`, in
the 503 non-PASM Spin2 blocks, or in one-liners outside the net (S-256). Spin2-side misuse is a different class.

**Population today (measured).** Using the harness's own `find_candidates`/`load_manifest`/`build`/`elementize` over every `program|fragment|never` block (2,450; 1,946 PASM blocks scanned, 503 non-PASM skipped, 1 elementize abort): **8 operand sites in 6 blocks in 4 files** — `false.yaml` examples[0] (`mov flag, FALSE`, `if_e mov flag, TRUE`), `true.yaml` examples[0] (`mov result, TRUE`, `if_z mov result, FALSE`),
`negx.yaml` examples[0],[1] (`cmps value, NEGX`, `mov limit, NEGX`), `posx.yaml` examples[0],[1] (`cmp value, POSX`, `mov limit, POSX`); all built-in constants, all currently `fragment`/green in the compile gate. **0** user lower-case CON constants in the gated blocks (so the lower-case class the study worries about has no gated instance today).
Reproduce: `python3 …/scratchpad/gatesF/d3/scan.py` (≈ minutes: one elementize per block).

**Negative controls.** Verified on scratch text with the rule above (`…/gatesF/d3/ctl.py`): `mov flag, myc` with `CON myc = 5` → fires (a CON in the block); `mov flag, TRUE` → fires (built-in); with `assumes: limit=con` and no CON in the block, `mov flag, limit` → fires. Must NOT fire: `mov flag, #myc`, `mov flag, #TRUE`, `mov flag, ##myc`,
`mov flag, buf` (a label), `mov flag, 5` (a numeral), `flag long TRUE` (a directive), and `mov flag, limit` when `limit` is a plain-operand assume.

**Home / wiring.** Extend `audit-kb-code-compiles.py` (reuses its elementizer parse and manifest; the token walk costs no extra compile, one elementize per PASM block that the harness mostly already makes). New problem kind `BARE-CONST` in `print_report`; negative-control cases NC-D3a..d. Wiring unchanged: `validate_kb_code_compiles` (900 s;
the added cost is **not measured** — report it with the first run). The 8 sites then become findings to fix with the S-162 edits (the gate lands with them).

**A green does NOT certify.** That no constant is misused: only constants whose declaration the harness can see. It does not check that a `#` operand is the *right* constant, or that the value fits 9 bits (the compiler does that).

---

## S-308 — claim-sourcing change (already specified; pointer)

The build spec is the study row **S-308** (`2026-10-08-p2kb-close-out-study.md`, Group A table, line 674) and decision D4; it changes `audit-yaml-claim-sourcing.py` in place: (a) exempt example blocks by location (`^(\w+_)?examples?$`, `quick_example`, `complete_example`, `usage_example`,
`authority_tier: EXAMPLE`, `worked_escape`, one-line `wrong:`/`correct:`; **not** `anti_patterns`/`common_patterns`), (b) switch Tier 2 on after S-295..S-307 (`main()` ~`:820-824`; 27 Tier-2 blocks per the F-381 paragraph at study line 653), (c) skip `community/obex/objects/` and check OBEX
metadata against the index, (d) recognise `part\d+-…\.txt` silicon-doc cites in `INLINE_CITE_RE` (`:277-280`). Controls: four must-not-fire (example blocks) and four must-still-fire (uncited prose, `notes` beside exempt examples, PRINCIPLE-tier figures, `common_patterns`).
Home and wiring are unchanged and already armed: `validate_claim_sourcing()` (nc + audit), `release-yamls` §1/§5.5. Interaction with this file: S-256's `wrong`/`correct` keys and S-308's exemption of one-line `wrong:`/`correct:` must agree — S-256 sends them to the compile gate (legality), S-308 exempts them from the sourcing gate (no quantity claim).

---

## Not checked

- No gate, runner, or skill command was run. The scratch scripts import the compile gate's functions (`find_candidates`, `load_manifest`, `build`, `elementize`, `code_bearing`) to *read* the corpus; that is not a gate run, but it does run `pnut-ts --pass elementize` on temp files.
- The F-454 sources' Revision History sections (whether the 5 unqualified ratings differ by revision), and whether `p2kb_find` searches categories (F-389 haystack).
- The wall time of the F-405 freshness limb and of the D3 token walk inside the 900 s compile gate.
- Any `.yml` / non-`.yaml` pointer, and the 4 S-200 R3-only sites' intent (are `JMP vector  # Jump to …` meant as comments? — the rule flags them, the S-183 edit decides).
- The register entries were not edited: F-364's "gate not built" line and F-405's "nothing invokes `validate-dod-release.py`" are both stale against the code (see their sections); the arbiter reconciles.
