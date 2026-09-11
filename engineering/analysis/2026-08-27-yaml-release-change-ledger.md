# YAML release change ledger — `v1.17.0..HEAD`

**Purpose.** Everything that differs in `deliverables/ai/P2/**/*.yaml` between the last release and
HEAD, with the reason it changed and **what was absent that let the defect exist**. Written for a
release review; the question it answers is *"is it safe to ship, and what did we lose that I cannot
see from a diffstat?"*

**This document shows CURRENT differences only.** An item that has been fixed is **gone from here**,
not annotated as fixed. If you want the history of what was once outstanding, read the archived
predecessor named below and the git log — not this file.

**Range.** `v1.17.0` (`7ff76b30`, 2026-08-21) `..` `b0057ec1` (2026-09-08).
**Re-derived on disk 2026-09-09.** Every count below was measured from git and from the parsed YAML
at HEAD. *(The 2026-08-27 revision measured the range ending at `b466a538`; the 2026-08-29
pre-release fix pass added three commits touching KB YAML — §1.18; the **2026-08-30 fix pass** added
three more — §1.19; and the **2026-09-05 / 2026-09-08 passes** added five more — §1.20 · §1.21 ·
§1.22. Every count in §0.1, §0.3, §0.4 and §0.5 was re-measured, not adjusted, on each occasion.)*
Where a project record, a commit message or a companion analysis disagrees with the artifact, the
artifact is reported and the disagreement is named (§0.2).

**The body was derived at `b0057ec1`; six 2026-09-09 commits have landed on top of it and are
carried in §1.23 · §1.24 · §1.25.** Re-deriving found three defects, Stephen's terminology review
found two more, and the reference sweep he then authorised closed a sixth — all fixed in the same
pass, per the no-deferring rule. Final: **118 files · +7528/−3684 · 41 commits touching KB YAML,
153 in the range.** Stated here and in §0.1 rather than folded silently into the body's numbers,
because a derived document that quietly absorbs its own edits is the drift this re-derivation exists
to remove.

⚠️ **This re-derivation found the tree RED and repaired it.** `validate-dod-release.py` exited **1**
at `b0057ec1`: *"Gzip Compression: FAIL — gzip content does not match JSON file."* The 2026-09-05
pass regenerated `p2kb-index.json` **twice** (`d55b6c7f`, `da896073`) and regenerated
`p2kb-index.json.gz` **neither time**, so the pair had been out of sync in committed history for
four days — **F-357's exact defect, recurred**. The index was separately stale by the two files the
2026-09-08 pass changed. Both are fixed in the commit that carries this document; the pair is back
in sync and the validator is green at 11 of 11. See §0.4. *The re-derivation is what found this: no
gate runs itself, and nothing had run the validator since 08-30.*

**Supersedes** `engineering/analysis/2026-08-25-yaml-release-change-ledger.md`, archived to
`engineering/analysis/archived/2026-08-25-yaml-release-change-ledger.md`, **byte-identical to its
last committed revision** (`git show HEAD:… | cmp -` returns clean). *Note the path is `archived/`,
not `archive/`: `.gitignore:179` carries a bare `archive/` rule that matches any directory of that
name anywhere in the tree — archiving into one would have silently dropped the document out of
version control, which is the opposite of what an archive is for.* That document measured
**61 files / 11 commits** and was correct when written; 28 more files and 13 more commits landed
after it. It was **re-derived, not patched** — hand-patching a derived document preserves exactly
the drift this re-derivation exists to remove.

**Two views of the same facts.** Part 1 groups by *reason* — a class usually crosses regions.
Part 2 goes region → file, **each carrying its differential-read verdict**. *(Part 2's tables were
written when the set was 92, and its **92 rows** are still the differential read's population. The
change set is now **112**, and the arithmetic is stated so nothing reads as an omission:
**92 rows + 4 (§1.19) + 15 (§1.21) + 1 (§1.22) = 112.** The four the 2026-08-30 pass brought in —
`architecture/hub.yaml`, `hardware/p2-hardware-selection-guide.yaml`,
`language/spin2/methods/coginit.yaml`, `language/spin2/methods/cogspin.yaml` — are in §1.19 with the
revised ± figures for the fourteen it re-touched; the fifteen the findability pass brought in are in
§1.21 and the one the boot-ROM pass brought in is in §1.22. Part 2's region headers carry the HEAD
file counts, so header total (112) and row count (92) differ by exactly those twenty.)*

---

# Why this release touched the KB — the drivers, and how far each one reached

**Read this first.** Part 1 groups the changes by *what kind of change* they are and Part 2 by
*where* they landed; both assume you already know **why anyone was in these files**. This section is
that missing layer. Every file count and region list below is measured from `git log`/`git diff`
over `v1.17.0..HEAD`, not asserted.

**The one-sentence version.** This release started from **one reported symptom** — the KB described
the P2 as having pull-up resistors it does not have — and the fix for it exposed that the mechanism
it should have named had *no definition anywhere in the set*, which in turn exposed how much of the
set's physical content *cited nothing at all*. Everything after that is the consequence: a policy sweep,
then a sequence of audits, each of which was designed to catch what the previous one structurally
could not, and each of which found a different class of defect. **No audit here found the class the
audit before it was looking for.** That is the shape of the release.

## The drivers, in the order they arose

| | Driver | What set it off | Reach | Scope | Detail |
|---|---|---|---|---|---|
| **A** | **The reported symptom** — drive strength mislabelled as bias resistors | **The P2 has no pull-up or pull-down resistors.** `P_HIGH_*`/`P_LOW_*` select drive strength; the shipped KB called them bias resistors, so an agent asking how to enable a pull-up was handed a mechanism the silicon does not have. This is the one defect that was *reported* rather than found — everything else below was found while fixing it or while checking the fix | 6 regions — `language/spin2` · `language/pasm2` · `hardware` · `guides` · `architecture/smart-pins` · `code-examples` | **12 files** | §1.4 |
| **B** | **Cite-or-omit, applied as policy** — the uncited-quantity purge and its source-first repopulation | Fixing A meant reading the sources, and the reading showed the mislabel was not isolated: the set was full of physical quantities that named no source at all. Removal first, deliberately, so nothing could be rationalised in place | 8 of the 11 regions — all but `architecture/streamer`, `architecture/system-registers` and `code-examples` | **42 files**; **119 blocks removed**, **80 returned cited**, **41 did not come back** | §1.1 · §1.2 · §1.3 |
| **C** | **The definition gap** — 55 constants the KB used and defined nowhere | A's replacement text had to name the real mechanism, and the real mechanism's constants had no home. You cannot cite a constant you never defined | 3 regions — `architecture` · `language/spin2` · `language/pasm2` | **5 files**; 55 constants defined, all **116** v55 constants covered in one home, and a **116-name `aliases:` block** added — without it the index harvests nothing and none of the definitions resolve through `p2kb_get` | §1.5 |
| **D** | **The actionability filter** — does this block change the code an agent emits? | Neither purge asked it. A block can be true, cited, and still be noise a code-generating agent must wade through | 3 regions — `hardware` · `language/spin2` · `language/pasm2` | **4 files**; **233 blocks** given a written disposition | §1.8 |
| **E** | **The fabricated-provenance audit** (F-359) | A provenance header naming source files that **have never existed** satisfies every citation gate ever written. Once one was found, the question became how far the same 2025-11-29 authoring run reached | 2 regions — `architecture` · `architecture/system-registers` | **7 files** touched, **6 re-derived from scratch** (a seventh carrying the same header had already been purged); across the six, **41 of 45** encodings were wrong, 4 mnemonics did not exist, 6 semantic inversions | §1.6 |
| **F** | **The ingestion sprint's findings, finally applied** | `ingest-source` forbids YAML edits by design, so everything the ingestion sprint found had been sitting in the register untouched. This release is where it reached the KB | 9 regions — the widest reach of any driver | **22 files** | §1.12 · §1.9 |
| **G** | **New ingestions** — Click Adapter, WX module, streamer pin capture | Coverage the KB did not have, ingested from schematics and guides rather than inferred | 5 regions — `hardware` · `architecture` · `architecture/streamer` · `language/spin2` · `language/pasm2` | **17 files**; **two of the four new files** this release (`streamer/pin-capture.yaml`, `addon-click-adapter.yaml`) | §1.11 · §1.12 |
| **H** | **The differential read** — what did we *lose*? | A diffstat cannot tell a repair from a deletion. The read asked, per file, whether HEAD still says everything `v1.17.0` said. It found one file **gutted**: `pasm2-getting-started.yaml` explained what happens when you declare a clock mode and no longer said how to declare one | 2 regions — `guides` · `architecture` | **3 files**; **34 top-level keys across 24 files** also changed YAML type, measured here | §1.14 · §1.13 · §1.16 |
| **I** | **Instruments armed, and the defects they immediately found** | Three gates went from advisory to blocking and one was built from nothing. Arming them was not the end of the work — it was the start of a new class: a duplicate YAML key silently discarded this sprint's own central corrective sentence | 4 regions — `architecture` · `hardware` · `language/spin2` · `language/pasm2` | **19 files**; duplicate keys to **0/1132** | §1.10 · §1.17 · §1.13 |
| **J** | **Citation routing** — the paths every new agent follows | Both getting-started guides told an agent to read `concepts/basic-io.yaml` first, and **two real files answer to that name** — the routing citation pointed at nothing deterministic, straight at the files carrying the mislabel from A | 3 regions — `guides` · `language/spin2` · `language/pasm2` | **4 files** | §1.9 |
| **K** | **Register drains — including two refusals** | The corrections register had accumulated findings older than this sprint. Two of them were **rejected**: applying them would have introduced defects into content that is currently correct | 2 regions — `architecture` · `architecture/smart-pins` | **2 files** | §1.15 |
| **L** | **2026-08-29 pre-release pass** | Re-reading before shipping, rather than re-checking a prior pass's conclusions. Recomputing the SETXFRQ NCO class instead of trusting two named values found **nine shipped values wrong** by one bit | 4 regions — `architecture` · `architecture/streamer` · `language/spin2` · `language/pasm2` | **6 files** | §1.18 |
| **M** | **2026-08-30 pre-release pass** | The defect census graded two items category 1 — 19 uncited hardware quantities and 721 unread citations. Reading the 19 found **three were wrong** and opened a family sweep; reading the 721 discharged F-377 | 6 regions — `hardware` · `architecture` · `architecture/streamer` · `application-notes` · `language/spin2` · `language/pasm2` | **18 files** | §1.19 |
| **N** | **The codegen-effect audit of the unpublished delta** (2026-09-05) | The only question this whole release exists to answer had never been asked directly: *of the content an agent actually receives, do these changes weaken its ability to generate code?* Answered by running today's instruments over a real `git worktree` of `v1.17.0` — the baselines are first-hand, not relayed from commit messages | 2 regions — `architecture` · `hardware` | **2 files** — the audit's own two introduced-locator repairs; the audit itself changed nothing else | §1.20 |
| **O** | **The findability audit** (F-401, F-402 — 2026-09-05) | **A question from outside the release**: an agent failed three or four times over two days to locate information the KB *has*. Reproduced and measured — the index harvested four name fields, and **0 of the 62 pure-symbol Spin2 names** (`:=` `+//` `<=>` `^@` `??` …) were in it in any form. Those are precisely the tokens an agent meets when reading Spin2 source | 3 regions — `language/spin2` · `architecture/system-registers` · `code-examples` | **16 files**; 12 name-bearing fields now harvested, 13 files given a hand-authored `aliases:` block, and the duplicate `+//` definition home merged | §1.21 |
| **P** | **The boot-ROM content list** (F-403 — 2026-09-08) | A survey of what the KB asserts about the 16 KB mask ROM. The shipped file named **six** residents; the one authoritative content list we hold names **three**, and two of the extras trace to *our own generated narrative* rather than to any Parallax document | 1 region — `architecture/boot-rom` | **2 files** | §1.22 |

Every one of the **112** changed files is attributable to at least one driver above; the union is
112, with no remainder. Files appear under more than one driver where more than one reason reached
them, and **how many drivers entered a region is the best single predictor of how large its per-file
diffs are in Part 2**:

| Region | Drivers that entered it | |
|---|---|---|
| `language/spin2` · `architecture` | **11 each** | the two most re-entered regions. `architecture/`'s re-derived files carry the largest *rewrites* — `interrupts.yaml` +221/−115, `debug_interrupt.yaml` +208/−92, `clock_system.yaml` +185/−136 — while `language/spin2/`'s largest change is the one-way constant expansion `spin2-builtin-symbols-complete.yaml` **+1052/−23**, still the biggest single diff in the release |
| `language/pasm2` | **10** | untouched by every pass after 08-30 |
| `hardware` | **8** | A · B · D · F · G · I · M · N — the widest region by file count (28) and by lines changed (+2233/−1752) |
| `architecture/smart-pins` · `guides` · `architecture/streamer` | 4 each | |
| `application-notes` · `architecture/boot-rom` · `architecture/system-registers` | 3 each | `boot-rom` and `system-registers` were each entered once more by the 2026-09 passes |
| `code-examples` | **2** | driver A (one word) and driver O (an `aliases:` block on the schema file) — and that is the whole of it |

The two new files not attributable to G are `architecture/pin-drive-configuration.yaml` (driver C —
it *is* the definition home) and `hardware/p2-package-mechanical.yaml` (driver F — written as the
package record for F-366).

## What each audit actually contributed — and what it could not have found

The audits are not redundant. Each was built to see something the last one was blind to, and the
record of *what it caught that nothing else would have* is the argument for having run it.

| Audit / pass | Found what nothing before it could | Was structurally blind to |
|---|---|---|
| **The purge** (B) | Every quantity with no source named | A wrong value that *is* cited; a fabricated citation |
| **Source-first repopulation** (B) | Wrong scalars and invented board sections in blocks that **survived** the purge — because rebuilding from the source rather than the removed block reads the source | Anything in a block it did not rebuild |
| **The promotion filter** (D) | Content that is true and cited and still cannot change emitted code | Correctness of any kind |
| **The fabricated-provenance audit** (E) | Citations naming files that never existed, and the 41 wrong encodings hiding behind them | The seven files' *siblings* — the audit was scoped to the authoring run |
| **The differential read** (H) | A file **gutted** by an otherwise-good rewrite; 34 silent schema-type changes | Anything present at both revisions and wrong at both |
| **Armed instruments** (I) | Duplicate keys — including one destroying this sprint's own corrective sentence | Any claim a regex cannot read; the gates say so themselves |
| **The defect census** (2026-08-30) | The *size* of what remained, class by class — which is what made M finishable rather than open-ended | A class it did not model; it says so, and M then found one |
| **The 08-29 pass** (L) | Nine NCO values wrong by one bit, in files that **quoted the very rule they violated** | Anything outside the classes it recomputed |
| **The 08-30 pass** (M) | 22 mis-pointing citation locators, and six facts simply wrong in files with no citation defect at all | The Tier-2 population; and it says so |
| **The codegen-effect audit** (N) | What the delta does to the *consumer* — the only direction no other instrument measures. It is also the only pass that measured `v1.17.0` with today's tools, which is what makes every "before" figure real rather than quoted | Anything wrong at **both** revisions; it compares two trees, so a defect that predates the tag is invisible to it |
| **The findability audit** (O) | Content that is present, correct, cited — and **unreachable by the name an agent types**. No gate in §0.4 asks whether a file can be *found*; every one of them asks whether it is *right* | Whether the content it made reachable is correct. It moved 0 → 62 symbol names and read none of the definitions behind them — except the one collision that forced a read, which is exactly how F-402 surfaced |
| **The boot-ROM survey** (P) | A claim with **no quantity and no constant in it**, sourced to a file we generated ourselves. The sourcing gate never scored it (no numbers) and the fidelity gate never saw it (no constant names), while the file's four real header citations made a Tier-2 sweep read it as a citing file | Everything outside the one file it surveyed; it names its own scope |

**The through-line, and the reason §0.5 still has a red block.** Every instrument in §0.4 is green and
was green before each of the fixes above. **No gate here can read a sentence, and none of them asks
whether a file can be found at all.** What found the wrong values was, in every case, a person or an
agent *reading the source at the line* — and in three cases (F-389/F-401, and the debug/stack
questions behind F-390/F-391) it was **a question from outside the release entirely**. That is why
the ledger reports gate results as *"not caught by these checks"* rather than *"correct"*, and why
the count of findings in a class is the size of the class we measured, never the size of the defect
population.

**And one gate result was not a green at all.** The eight instruments in §0.4 all passed at
`b0057ec1`, but `validate-dod-release.py` — which wraps them and adds four artifact-level checks —
**exited 1**. Nothing had run it since 2026-08-30, so a red release gate sat in committed history
for four days. **A gate that nothing runs is not a gate**, which is the same sentence §0.5 item 19
has been carrying about the duplicate-key checker, now demonstrated rather than predicted.

---

## Part 0 — Scope, reconciliation, gate state, and what is still open

### 0.1 Scope, measured at HEAD

| Quantity | Measured | Command |
|---|---|---|
| Commits touching KB YAML | **41** | `git log --oneline v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' \| wc -l` |
| Commits in the range, all paths | **153** | `git log --oneline v1.17.0..HEAD \| wc -l` |
| YAML files changed | **118** | `git diff --name-only v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' \| wc -l` |
| Lines | **+7528 / −3684** | `git diff --numstat … \| awk '{a+=$1;r+=$2} END{print a,r}'` |
| ↳ *composition of the 2026-09-09 work* | §1.23 F-404 · §1.24 F-406/F-407 · §1.25 the reference sweep | Eleven files touched across the day; **six of them entered the change set**, all in §1.25 — the first files to do so since `9ab0433b`. |
| New files | **4** | `git diff --diff-filter=A --name-only …` |
| Deleted / renamed files | **0 / 0** | `git diff --diff-filter=DR -M --name-status …` |
| Shipped set size | **1129 → 1133 files** (unchanged by every pass after 2026-08-26 — the 08-29, 08-30, 09-05 and 09-08 passes added no files and deleted none) | `git archive` both revisions, count `*.yaml` |
| Region spread | language/spin2 **33** · hardware 28 · architecture 15 · language/pasm2 **15** · architecture/streamer 8 · architecture/boot-rom 5 · architecture/smart-pins 4 · application-notes 4 · guides 2 · code-examples 2 · architecture/system-registers 2 | `… \| awk -F/ …` |
| Lines by region | hardware +2237/−1756 · language/spin2 +1987/−418 · architecture +1904/−968 · architecture/streamer +692/−94 · language/pasm2 +225/−179 · guides +180/−92 · architecture/boot-rom +93/−63 · architecture/smart-pins +72/−42 · application-notes +65/−54 · architecture/system-registers +62/−17 · code-examples +11/−1 | sums to +7528/−3684 exactly |

The four new files are unchanged from the 2026-08-30 derivation:
`architecture/pin-drive-configuration.yaml`, `architecture/streamer/pin-capture.yaml`,
`hardware/addon-click-adapter.yaml`, `hardware/p2-package-mechanical.yaml`. **The twenty-two files that
entered the change set after `9ab0433b` were all already in the shipped set** — the 2026-09 passes
added names, corrected content and repaired references; they did not add coverage:

| Region | Files new to the change set since `9ab0433b` | Pass |
|---|---|---|
| `language/spin2` (13) | `debug-commands/debug-formatters-{overview,complete,decimal,hexadecimal,binary,arrays}.yaml`, `debug-commands/debug-new-user-guide.yaml`, `integration/spin2-pasm2-integration.yaml`, `operators/modulo_add.yaml`, `operators/op_addmodulo.yaml`, `spin2-language-complete-map.yaml`, `spin2-language-schema.yaml`, `symbols/streamer-symbols.yaml` | §1.21 |
| `architecture/system-registers` (1) | `dira-dirb-registers.yaml` | §1.21 |
| `code-examples` (1) | `code-example-schema.yaml` | §1.21 |
| `architecture/boot-rom` (1) | `boot-rom-contents.yaml` | §1.22 |
| `language/pasm2` (3) | `concepts/labels.yaml`, `concepts/cog_hub_execution.yaml`, `xcont.yaml` | §1.25 |
| `language/spin2` (3 more) | `methods/pinstart.yaml`, `methods/wxpin.yaml`, `methods/wypin.yaml` | §1.25 |

**Out of scope, named once so their absence from Part 2 is not read as an omission.**
`deliverables/ai/P2/CHANGELOG.md`, `deliverables/ai/P2/README.md` and `deliverables/ai/README.md`
changed in this range and are not YAML. `deliverables/ai/p2kb-index.json` and its `.gz` are
regenerated artifacts, not content. And **one commit in the range is not this release's work**:
`7be432a6` ("pnut-ts 015504, and the Dockerfile no longer names the version") belongs to another
session and touches no KB YAML.

### 0.2 Reconciliation — every number that disagreed, and why

Nothing here is a defect in the artifact; each is a measurement taken at a different revision or by
a different method. Recorded because a stale count is what sent this document back for re-derivation.

| Source | Its number | Measured at HEAD | Why |
|---|---|---|---|
| The archived 2026-08-25 ledger | 61 files, 11 commits, 1 new file, +3770/−2751 | **89 · 24 · 4 · +6246/−3355** | It was right at `0a5323ab`. Thirteen commits landed after it. |
| `2026-08-26-yaml-differential-read.md` | 85 files, 81 modified / 4 added, +6137/−3341 | **89 · 85/4 · +6246/−3355** | It measured at `4caeb6cc`. The four files added since are `language/pasm2/{addsx,subsx,sumc,sumz}.yaml`, all from `b466a538`; `ca07aaf7` moved lines without adding files. **85 + 4 = 89, reconciled exactly.** |
| `2026-08-26-yaml-shape-change-consumer-audit.md` | 34 keys / 24 files / 23 `list→dict` / 11 `str→dict` | **34 · 24 · 23 · 11 — reproduced independently at HEAD** | No drift. Re-measured by parsing every top-level key of every changed file at both revisions and comparing `type()`. |
| `15c84de5`'s own subject line | "59 uncited quantitative blocks" | **60** | The commit's own body and `597d5eba`'s body both say 60; the subject is off by one. Measured as a key-set delta across the commit. |
| `491f2b55`'s own body | "Of the 59 blocks … 34 return … 24 stay" | 34 + 24 = **58** | One hardware block is unaccounted for in that commit's arithmetic. Not reconciled here; the HEAD-side key-set delta (§0.3, 41 keys) is the reliable instrument. |
| `11ebec54`'s commit message, and this task's own dispatch | "validate-dod-release: **12** checks" | **11** | The script's `validations` list holds eleven functions (`validate-dod-release.py:661-673`); its output prints eleven named checks plus a summary line. It held **nine** at `v1.17.0`; the two content gates armed by `43b0ede2` took it to eleven. It has never been twelve. The shape-change audit's own §6 also records eleven. |
| `2026-08-26-yaml-differential-read.md` §8.6 | `audit-register-hygiene.py … P1-CORRECTION-FINDINGS.md` remains exit 1 `no-counter` | **exit 0, CLEAN** | Repaired after that read, by `d62544ea`. Both P1 registers now name their allocators. |
| `2026-09-05-codegen-effect-of-the-unpublished-yaml-delta.md` | 96 files, +6,703/−3,480; 130 commits since the tag, 97 unpushed | **118 · +7528/−3684**; 153 commits | It measured at `a7fd84e3`, before its own repairs and before every 2026-09 pass. Its *findings* stand; its scope line is superseded by §0.1 here. The unpushed count is deliberately dropped — it moves with every commit and is not a property of the change set. |
| The same document's findability rows | files with top-level `aliases:` 71 (6.3%) → **84 (7.4%)**; alias keys 508 → **755** | **100 (8.8%) / 961 keys** at HEAD | Measured before F-401. The findability pass (§1.21) added sixteen more `aliases:`-bearing files. **The index's own alias table is a different instrument and a different number — 2,896 entries** — because it harvests twelve name-bearing fields, not just a top-level `aliases:` block. Do not compare the two. |
| The F-401 register entry's result table | dark files 452 → **206**; alias entries 2,082 → **2,660** | **173 dark (15.3%) · 2,896 alias entries** | The entry records the **first** of two passes (`ba24f0f9`/`d55b6c7f`) and was never updated after the second (`19385b66`/`da896073`). Corrected in the register in this pass. |
| `19385b66`'s claim *"zero dark files outside `community/`"* | — | **confirmed: all 173 dark files are under `community/`** | Re-derived from the emitted index at HEAD: 1,133 files, 955 reachable by an alias (84.3%), 557 in a category, 173 in neither — every one of them an OBEX object or a Quick Byte, which have their own `p2kb_obex_*` retrieval route. |
| F-403's evidence table | `Monitor`/`debugger` **40** hits in the ROM listing | **`Monitor` 32 + `debugger` 9 = 41** in `ROM_Booter.lst`; **33 + 10 = 43** in `rom_booter_v33_01j.lst` | Re-counted here. The finding's point is untouched — the residents it removed return **0** in both listings for `font`, `glyph`, `sine`, `sin_` and `log2`, verified at the line, while `TAQOZ` returns **48** in both. |

### 0.3 The block accounting — where the content went

The two purges removed **top-level YAML blocks**, and that is the unit everything else counts in.
Measured by parsing the top-level key set of every file at each commit's parent, at the commit, and
at HEAD.

| Movement | Measured | Detail |
|---|---|---|
| Blocks removed by the purges | **119**, across **41 distinct files** | 60 (`15c84de5`, 25 files) + 59 (`c733a223`, 17 files); one file appears in both |
| Blocks returned carrying a citation | **80** | 46 (`597d5eba`, 24 files) + 34 (`491f2b55`, 15 files) |
| Blocks removed *by the repopulation* | **1** | `hardware/edge-32mb-module.yaml alternate_part` — the fabricated `64000-ES` part number, deleted with a note saying why |
| **Top-level keys present at `v1.17.0` and absent at HEAD** | **54, across 19 files** | the reliable instrument: a strict key-set delta at HEAD, immune to any intermediate churn |

**Disposition of the 54** — the first three groups are carried from the differential read §3 and
checked here; the fourth is new at HEAD and is **not a loss**. The four groups sum to 54 exactly.

| Disposition | Keys | Where |
|---|---|---|
| **Fabricated / disproven** — no source states it, and several are contradicted | **15** | `io_pin_timing` ×8 · `{pasm2,spin2}/concepts/basic-io` ×3 each · `p2-eval-board video_audio` |
| **True but not actionable** — cannot change emitted code; verified present in the ingestion tree | **24** | all in `hardware/`, across 13 files |
| **Authored here, no upstream** — correct, actionable, unsupportable by anything we hold | **2** | `io_pin_timing best_practices` · `click_module_integration best_practices` — **F-352, open** |
| **Moved to the definition home** — the `+//` merge (F-402, §1.21) | **13** | all `language/spin2/operators/modulo_add.yaml` |

⚠️ **The fourth group is an instrument artefact, and it is worth saying exactly how.** This
measurement is a **per-file** key-set delta, so it cannot see a key that moved to a different file.
`modulo_add.yaml` became a redirect and `op_addmodulo.yaml` became the definition home. Of the 13
keys the redirect shed, **8 are present in the home file at HEAD** — `best_practices`,
`common_patterns`, `comparison_with_alternatives`, `notes`, `operation`, `overview`,
`related_operators`, `syntax` — verified by parsing both files at both revisions. The home file
gained 13 keys in the same move and lost none.

The **five that did not move** are all deliberate: `examples` (the home carries its own, and the
redirect's worked ring-buffer material was folded into `common_patterns` — `(index + 1) +//
BUFFER_SIZE`, the head/tail distance idiom and the power-of-2 `&`-mask comparison are all present in
the home file), and four bookkeeping keys — `created: 2025-09-09`, `documentation_level`,
`documentation_source: code_analysis` (the very token F-402's class sweep flagged) and `references`.
That last one is the only judgement call in the group and it is an improvement: it held
*"P2-OctoSerial: Extensive use in circular buffers"*, *"Spin2 documentation: Arithmetic operators"*
and *"Production code patterns from Iron Sheep Productions"* — three pointers, none of them a
locatable citation. The home file carries a real one in its place
(`complete-spin2-operators.md:715`, `:62`, `:103`).

**So the honest reading of 54 is: 41 keys gone, 13 relocated.** The earlier 41 is not superseded —
it is still the loss figure, and this pass did not add to it.

The differential read separately estimates **1930 leaf facts across 73 files** whose value string
appears nowhere in the shipped KB at HEAD, and states plainly that this over-reports: a reworded
fact counts as absent. It is quoted here as a *candidate* population, not a loss figure. Not
re-derived in this document.

### 0.4 Gate state at HEAD — all eight run, none quoted

| Gate | Result | Exit |
|---|---|---|
| `verify-yaml-format.py` | 1133 scanned, 1133 parsed clean, 0 failures | 0 |
| `validate-crossref-keys.py` | ALL TOP-LEVEL CROSS-REFERENCES RESOLVE — **698 nested sites NOT checked (F-340)** | 0 |
| `validation/audit-yaml-claim-sourcing.py` | Tier 1 **none** across 1133 files; **27 Tier-2 advisory** blocks in wholly-uncited files (48 on 2026-08-27 → 32 after §1.18 → **27** after §1.19 cited the two hardware files the census had called category 1). Tier 1 stayed at none through both moves, so neither exposed an uncited sibling block — the **F-381** trap was checked for, not assumed | 0 |
| `validation/audit-constant-fidelity.py` | Tier 1 none, Tier 2 none, across 120 source-defined constants; truth side 35 files, editions `spin2-v51` + `spin2-v55` | 0 |
| `validation/audit-extraction-digit-density.py --all` | CLEAN, 65 artifacts at or above the 20% floor, 4 declared exempt | 0 |
| `validation/audit-yaml-duplicate-keys.py` | 1132 scanned, **0 files with duplicate keys** | 0 |
| `validation/audit-register-hygiene.py` ×3 | corrections **127 live / 294 archived / 0 unaccounted**, next `F-404` · gaps **37 live**, next `G-29`/`Q-10` · errata **17 live**, next `E-18` | 0, 0, 0 |
| `validate-dod-release.py` | **11 checks, all PASS** — READY FOR RELEASE ⚠️ **only after the repair below; it exited 1 at `b0057ec1`** | 0 |

**⚠️ The index pair had drifted again, and the release validator was red because of it.**

Run at `b0057ec1`, before any repair, `validate-dod-release.py` reported
**`❌ Gzip Compression: FAIL — Gzip content does not match JSON file`** and exited **1**
(*VALIDATION FAILURES - DO NOT RELEASE*). The other ten checks passed. Diagnosis, from `git log` on
the two paths rather than from recollection:

| | `p2kb-index.json` | `p2kb-index.json.gz` |
|---|---|---|
| last regenerated | `da896073` (2026-09-05) | **`b753a29d` (2026-08-30)** |
| commits touching it since `9ab0433b` | `d55b6c7f`, `da896073` | **none** |

The 2026-09-05 pass regenerated the JSON **twice** and the gzip **neither time**, so the pair sat
out of sync in committed history for four days. **This is F-357's exact defect, recurred** — and
F-357 is `RESOLVED` in the register, which is what makes it a regression rather than an open item.

The index was **separately stale**, for a second and unrelated reason: it was generated on 09-05 and
the 09-08 boot-ROM pass committed content after it. Regenerating updated exactly **two** entries —
`p2kbArchBootRomContents` and `p2kbArchIndex` (`architecture/boot-rom/_index.yaml`), both mtime and
sha256, the two files §1.22 changed. No entry was added or removed; the count stayed at 1,133.

**Both are repaired in the commit that carries this document**, regenerated together and in the
required order (the index stores the **git blob** sha256, so it must be rebuilt *after* the content
commit). `gzip -cd … | cmp -` is clean, and the validator is green at 11 of 11.

**What this says about the release, and it is the more important half.** Nothing had run
`validate-dod-release.py` since 2026-08-30. A **red release gate lived in committed history for four
days** and was found only because this document was re-derived. The gate itself works — it caught
the drift on the first run — so the defect is not in the instrument, it is that **nothing makes the
instrument run**. That is the same sentence §0.5 items 12a and 19 have been carrying about the
duplicate-key checker, now with a demonstration attached instead of a prediction. Two checks belong
in the same wiring work: **the duplicate-key gate**, and an **index-freshness check**
(`generate-p2kb-index.py` then `git diff --quiet` on the pair) — the pair-*consistency* check
already exists and just proved itself; what is missing is *freshness*, which would have caught the
two stale boot-ROM entries as well.

⚠️ **What these greens do not certify, and each instrument says so itself.** The sourcing gate
checks that a citation is *present*, never that it is *right* — nothing here opens the cited
document. F-359 established that a **fabricated** provenance header satisfies that same regex, and
F-377 that a locator can be in range and still point at the wrong line. The constant gate checks
*named constants*; name coverage is not semantic coverage. `b466a538` is the current proof: four
files that parsed, resolved, carried citations and assembled under `pnut-ts` while each contradicted
itself about a flag's meaning. **No instrument in this project can read a sentence.**

**2026-08-29 adds a second, sharper proof, and it is the reason to distrust a green here.** §1.18
recomputed the SETXFRQ NCO class instead of re-reading the two values a prior pass had named. Nine
shipped values were wrong — an off-by-one in bit 0 of a 31-bit phase word — in files that parsed,
resolved, carried correct citations, and **quoted the very rule they were violating**. Every gate in
this table was green before that fix and is green after it. The same pass found the KB describing the
64-bit system counter as 32-bit, and a `~1-2 ns` smart-pin figure that exists in no Parallax source.
None of it was detectable by any instrument listed above. **Read this table as "not caught by these
checks", never as "correct" — the gates themselves say so in their own closing banners.**

**2026-09 adds two more blind spots, and one of them is a different axis entirely.**

- **F-403 (§1.22) is the *quantity-free* claim.** `boot-rom-contents.yaml` asserted character font
  data and sin/cos/log tables as ROM residents with `verification_status: "Existence confirmed"`.
  The sourcing gate never scored those blocks because **they carry no quantities**; the fidelity
  gate never saw them because **they name no constants**; and the file's header cites four real
  sources, which is exactly what makes a Tier-2 sweep read it as a citing file. It was found by
  reading the ROM's own assembly listing. **A claim with no number and no constant in it is
  invisible to every content gate this project has.**
- **F-401 (§1.21) is not a correctness blind spot at all — it is a *findability* one.** Every gate
  in this table asks whether a file is *right*. Not one asks whether an agent can *find* it. The
  measurement: **0 of 62** pure-symbol Spin2 names were in the index in any form, while **560 of
  560** word-named mnemonics and methods resolved cleanly. Content that cannot be retrieved is
  functionally absent, and eleven green gates said nothing about it for the life of the index.

### 0.5 What is still open — the pre-ship list, as it actually stands at HEAD

This replaces the twelve-item checklist the archived ledger carried. Nine of those twelve are gone
because they were fixed (`getct` description, the E-010 pull-up, `digital_io_board`, the
EF-063/EF-064 attribution, the shape-change question, `edge-breadboard-carrier`'s missing supply
figure, `addon-serial-host`'s identity string, both duplicate keys, and the `1224` symbol count).
What follows is what a release reviewer would still hit.

**🔴 Needs Stephen — the release cannot decide these itself**

1. **Eight claims that could not be re-derived are still standing in the shipped files.** «#323»
   re-derived six fabricated-provenance `architecture/` files against the live silicon doc and
   found the header was the signature, not the extent — 41 of 45 encodings wrong, four mnemonics
   that do not exist, six semantic inversions. Eight further claims survived: LUT power figures,
   LUT bandwidth restated from instruction timings, a lock "state bits: 4" width no source gives, a
   trace-buffer size, a debug-state size the source contradicts, a streamer-disruption claim the
   source rebuts, and a `0 clocks` WAITATN latency the datasheet gives as `2+`. They were
   **collected rather than deleted, because deletion is his.** Enumerated in **F-359**.
2. **F-367 — two different documents under one filename.** `external-inputs/p2/` and
   `sources/silicon-doc/` hold Silicon Doc DOCX copies that differ in 972 characters across four
   sites, including a GETBRK `WZ` semantic where one copy sets `Z = 1` in both branches. The
   `sources/` copy is demonstrably the right one and is what every extraction used, so nothing
   downstream is wrong. `b466a538` labelled `external-inputs/p2/` a staging area and wrote the
   mapping README; **reconcile-or-delete is his.** `CONFIRMED`.
3. **F-375 — both delivery paths strip `documentation_source:`, and 706 of those values are real
   citations, across 383 files.** The shipped set satisfies *cite-or-omit* on disk and is delivered
   not satisfying it. Every gate reads the tree; the consumer reads the filtered stream; nothing
   compares them. The remedy is a 383-file rename, which is a scope call, not a repair to start
   unasked. `CONFIRMED`.
4. **`ENH-NN` is an ungoverned allocator that has already collided.** The corrections register
   carries a third ID series with no declared counter, and live `ENH-02`/`ENH-03` name different
   proposals than the archived `ENH-02`/`ENH-03`. `d62544ea` made the hygiene gate print
   `unmodelled series : ENH-NNN` on every run without failing on it. Renumbering the live entries
   and inventing a proposal-status vocabulary are his calls.

4b. **F-398 — the hardware selection guide ships 2025 US retail prices as data.** ~15 USD sites
   (`cost_estimate` ×6, `total_cost` ×3, `cost` ×4, `total_investment` ×2, `additional_cost` ×2,
   `cost_difference`, a `+$30` PropPlug note) under `last_updated: "2025-09-06"`. Nothing sources
   them and nothing could: a Parallax guide does not carry retail price. It is F-374's shape in a
   different key — an unsourced claim wearing a data key — and the same kind of call.
   **Recommendation: delete every absolute figure and keep the relative tiering**, which is what
   the guide's decision tree actually turns on. `CONFIRMED`, not fixed.

4c. **F-400 — the `v55:NNNN` citation shorthand resolves to no file.** Several files cite the Spin2
   v55 documentation in a shorthand established at the top of the same block. Every instance
   checked in the F-399 sweep resolved to the right line *for a human*; no tool can bind it, and a
   tool that guesses binds it to the nearest full path, which is a different document. It was left
   alone rather than half-swept (55 spin2-v55 citations, plus `v51:` and `v35:` variants).
   **Recommendation: declare the shorthand and give the resolvers a prefix table**, rather than
   expanding 55 citations. `CONFIRMED`, not fixed.

**🟠 Real defects in the shipped set, scoped and unstarted**

5. ~~**F-377 part 1 — translated locators.**~~ **CLOSED 2026-08-30 (§1.19, F-399).** It was the
   largest unstarted item and it is done, the only way it could be done: **all 721 citation
   locators in the shipped set were opened at their cited lines and read** — 83 files, 40 source
   documents, nothing sampled. **22 were repaired**: 18 pointing at content that does not support
   the claim, 1 on a blank line, 2 naming a file that resolves to nothing, 1 ambiguous between two
   same-named source files. Ten of the 18 were exactly this carry-over shape, in
   `streamer/pin-capture.yaml` and `streamer/pin-selection.yaml`; the `dds-goertzel.yaml` pair
   named above is among them. A corpus-wide carry-over detector now returns **zero** across all
   **222** `silicon-doc-text.txt` citations. **The instrument had to be repaired first** — see
   §1.19 for the form-feed defect that made eight of the fourteen "blank line" hits the tool's own,
   and for the locator-binding ambiguity that is now registered as **F-400**.
6. ~~**F-377 part 2 — an eighth fabricated-provenance file.**~~ **CLOSED 2026-08-29 («#333»,
   §1.18).** `architecture/io_pin_timing.yaml`'s `part3-pins.txt` citation is gone. The content was
   checked and proved genuine, so it was re-anchored rather than removed: the four timing claims now
   cite `silicon-doc-text.txt:1987`, `:1997`, `:2005` and `:3847`, each re-read at the line, and the
   latch-up figure cites `:101` with the note that it comes from ON Semi failure analysis of one
   wafer lot quoted in the revision history, not a characterised limit. Reading the file also killed
   an unsourced `~1-2 ns` smart-pin timing claim and labelled a `5 clocks` total the source never
   states as the sum it is.
7. ~~**F-378 — the KB ships the compiler's acceptance range as a frequency ceiling.**~~ **CLOSED
   2026-08-29 («#334», §1.18)** — and it was five sites, not one. The sweep F-378's own text called
   for found `_CLKFREQ` (500 MHz vs the datasheet's 320), `_XINFREQ` (500 vs 200 for direct drive),
   `_XTLFREQ` (60 vs 50 for a crystal), `clkmode.yaml`'s "up to 500 MHz", and a 500 MHz row in
   `timing_operations.yaml`'s rollover table. All five now state the compiler range labelled as the
   compiler range, the datasheet rating beside it, and the Silicon Doc's 350 MHz `VCO / 1` overclock
   ceiling — three different numbers a reader was previously handed as one. **Superseded text
   follows for the record only:**
   `language/spin2/constants/special-configuration-symbols.yaml:59` gives `_CLKFREQ` a range of
   3,333,333 Hz to **500,000,000 Hz**, unlabelled. That is pnut-ts's acceptance range; the
   datasheet's PLL absolute maximum is **320 MHz**. An agent reading only that entry emits a
   `_clkfreq` up to 500 MHz, compiles clean, and ships silicon 180 MHz past the datasheet maximum.
   **The file is not in this release's change set** — it is a standing defect this sprint found, not
   one it introduced. E-007's label-which-framing rule applies and was never applied here.
   `CONFIRMED`.
8. **F-373 — three top-level fields are typed `text`, so a file path in any of them is never
   resolved.** `see_also`, `references` and `related_concepts`; 14 shipped file paths sitting in them
   point at nothing, and `validate-crossref-keys.py` stays green. Companion to F-340's 698
   unchecked nested sites. `CONFIRMED`.
9. **F-374 — 40 quality-score sites across 18 shipped files state a judgement, not a fact.**
   Star ratings and scores that the KB entry rule (existence · access · utility) excludes and no
   source authorises. `CONFIRMED`.
10. **F-372 / G-027 — the USB smart-pin entry states as fact a sentence the DOCX edition dropped.**
    *"A new WRPIN can be done to effect such a change without resetting the smart pin"* exists in
    the PDF-era capture of v35 and is absent from the DOCX capture of the same document, which
    states the opposite general rule. The KB now carries the conflict rather than deleting the
    claim, since it may well be right. **Bench-testable and jumper-only.** `CONFIRMED`.
11. **F-352 — two shipped areas are authored-here with no upstream anywhere.**
    `io_pin_timing best_practices` and `click_module_integration best_practices` were removed as
    uncited and cannot be restored without manufacturing provenance inside the fidelity gate's
    truth root (the defect F-341 files). The removal rule has no branch for *correct, actionable,
    unsupportable*. `CONFIRMED`.
12. **F-354 — seven content-level holes inside blocks that DID come back**, recorded at the point of
    use rather than in a separate document, plus one held block only three-quarters present in the
    ingestion tree. `CONFIRMED`.

12b. **F-381 — the Tier-2 advisory class is "no control available", not "reviewed and accepted",
    and it hides uncited quantity blocks from the blocking gate.** Proved by accident on 2026-08-29:
    adding silicon-limit citations to three clock files took `audit-yaml-claim-sourcing.py` from
    **0 Tier-1 violations to 12**. Nothing broke. Those files had cited *nothing anywhere*, which
    parks every quantity block in Tier 2; the gate judges a block against **its own file's other
    sections as the control**, and a wholly-uncited file supplies none. One real citation turns the
    rest of the file red. The 12 were always uncited — they were merely invisible. **32 advisory
    blocks across 24 files remain in that state** — **measured, not inferred**: a simulation
    inserting one recognised citation into each of the 24 files returns exactly 32, matching the
    advisory count. *(Corrects the 2026-08-29 wording, which called 32 a floor. Census §2.)* The 24 split
    into ordinary citation debt (8 smart-pin mode pages, 6 clock/timing language files) and content
    that may need a *declared exemption* rather than a citation (3 OBEX object-metadata files,
    5 `architecture/decomposition/` reasoning-layer files, 2 hardware guides — one of which is
    already item 17 below). **Deciding which is a scope call, not a repair to start unasked.**
    `CONFIRMED`.

**🟡 Residues named by the differential read and still open at HEAD** — each re-checked in the tree
today; the two that `ca07aaf7` closed have been dropped from this list.

13. ~~`language/pasm2/setxfrq.yaml common_values` — two of four values…~~ **CLOSED 2026-08-29
    («#332», §1.18), and the class was eight times the size recorded here.** This entry named 2
    values in 2 files. Recomputing the whole class instead of re-reading the named values found
    **9 wrong in the shipped KB** (setxfrq 2 of 4, `nco-timing.yaml video_rates` **7 of 12**) and
    **8 more in the published Streamer Guide v1.1.0**, which also taught the rule as `round()` in
    three places. Filed **F-380**. ⚠️ **A Streamer Guide re-release is owed** — the master is fixed,
    the shipped PDF is not. *This is the clearest instance of the counting lesson in §0.6.*
14. `application-notes/p2an004-…yaml` contradicts itself: `:111` says the sensor's electrical
    figures are "deliberately not restated here", `:87` restates them, `:127` cites the datasheet by
    document number.
15. Inconsistent treatment of derived arithmetic inside one region: `p2an003` deleted
    `200 MHz / 256 = 781_250 sps` as a derivation, while `p2an001:80` keeps
    `raw_sample_rate_sps: 1_562_500  # 200_000_000 / 128`, the identical construction, uncited.
16. `p2an001…:93` cites `p2-datasheet-text.txt:2199`; the PLL row is `:2200` (`:2199` is the Crystal
    row). Same shape as F-377, different pass.
17. `hardware/p2-hardware-selection-guide.yaml` (all three blocks) and
    `p2-hardware-feature-comparison.yaml selection_criteria` are authored buying-guide content,
    correctly retained under the promotion filter's sub-rule P and **never given a disposition** —
    the same missing branch as F-352.
18. **Tooling silent-failures (F-376) — one of the two is now CLOSED.** ~~`generate-p2kb-index.py`'s
    alias harvest ends in `except Exception: pass`~~ **CLOSED 2026-09-05 (`ba24f0f9`, §1.21):** the
    harvest now returns its failure reason and the generator **refuses to emit** rather than
    reporting success over a file that is present-but-unfindable. Proven with a negative control — a
    planted malformed YAML gives exit 1, names the file and the parser error, and leaves the
    existing index byte-identical. *That failure shape mattered because it removed **findability**,
    not the entry: the file still got a path and a sha256 and looked present.* **Still open:**
    `fetch-kb-file.sh -v <KEY>` fetches nothing and exits 0. **A green index generation is still not
    evidence that the corpus parses** — `verify-yaml-format.py` is the tool that answers that.
    `CONFIRMED`, half-discharged.
19. **The duplicate-key gate exists, passes, and nothing makes it run.**
    `validation/audit-yaml-duplicate-keys.py` was armed by `02ff61b7` and returns 0 across 1132
    files — but it is **not wired into `validate-dod-release.py`**, which calls
    `audit-constant-fidelity.py` and `audit-yaml-claim-sourcing.py` as blocking gates and not this
    one. A duplicate key reintroduced tomorrow turns nothing red at release. Named in **F-360**'s
    own closing line as the one thing that entry leaves open.

19b. **Nothing makes the *release validator itself* run, and that is no longer hypothetical.**
    The index/gzip pair drifted on 2026-09-05 and `validate-dod-release.py` sat **red in committed
    history for four days** until this re-derivation ran it (§0.4). The gate worked; nothing invoked
    it. Two checks belong in the same wiring work as item 19: the duplicate-key gate, and an
    **index-freshness** check — regenerate, then `git diff --quiet` on the pair. The pair-consistency
    check already exists and just proved itself; freshness is the one that is missing, and it would
    also have caught the two boot-ROM entries the index was stale by. **F-357 recurring while marked
    `RESOLVED` is the argument**: a defect closed by a one-time repair, with no gate wired to the
    release path, is a defect scheduled to come back.

19c. **F-401's fix is applied and unvalidated — the validation is a *post-publish* probe.**
    The index served to agents is the **published** one, so none of §1.21 reaches an agent until the
    set is pushed. What is owed after publish is one query: `p2kb_find("+//")` must return the
    operator file instead of dumping 59 categories. `PENDING-VALIDATION`, and it cannot move to
    `RESOLVED` before a release. Same shape for **F-402**.
20. **`validate_metadata_filter` reads the pattern list, not the artifact.** It classifies which
    lines the filter removed and never re-parses the filtered payload, so a block delivered as
    `null` passes it clean. The corpus is clean today (0 of 1133); the gate is measuring the wrong
    thing. Half of F-375. `CONFIRMED`.

**⚪ Known, measured, and NOT blocking**

21. **The shape mixture is deliberate and rule-determined.** 34 top-level keys across 24 files
    changed YAML type (23 `list→dict`, 11 `str→dict`) — re-derived here at HEAD, matching the
    consumer audit exactly. All five consumers were **executed** against the new shapes and each was
    **made to fail** on a shape it cannot handle, so the greens discriminate. The decisive
    experiment: moving the citations to the uniform-shape alternative drives
    `audit-yaml-claim-sourcing.py` to **exit 1 with 22 Tier 1 violations** — the reshape was forced
    by the armed gate, not chosen. And **0 of the 28** blocks still carrying the old shape is one the
    gate would demand a reshape for. Verdict: **MEASURED-SAFE.** What it does not settle is that
    nothing enforces or records the rule; if a schema is ever wanted, that is the rule to write down.
22. **27 Tier-2 advisory blocks** remain in wholly-uncited files (48 on 2026-08-27 → 32 after
    §1.18 cited three of those files → **27** after §1.19 cited the two hardware files the census
    had graded category 1). Advisory by design, non-blocking, and its population is not zero.
    ⚠️ **Re-graded 2026-08-29 — this is no longer "known, measured and NOT blocking".** See
    **F-381** / item 12b: the advisory class is not an accepted exemption, and citing any one of
    those 24 files turns its remaining blocks Tier-1 RED. It is listed here because it does not
    block *today*, not because it has been adjudicated.
23. **698 nested cross-reference sites are never checked** (F-340) and three top-level fields are
    exempt (F-373). `validate-crossref-keys.py`'s exit 0 covers less than it reads as covering.
24. **173 files are still dark — and all 173 are under `community/`.** Re-derived from the emitted
    index at HEAD: 1,133 files · 955 reachable by an alias (84.3%) · 557 in a category · **173 in
    neither, every one of them an OBEX object or a Quick Byte.** Those name themselves one level
    down (`object_metadata.title`, `quick_byte.*`) and have their own `p2kb_obex_*` retrieval route,
    so they are very likely not dark *in practice*. Reading a nested name is a different change from
    reading a scalar field that was already there, and it wants its own decision — **not blocking,
    and not to be started unasked.** Outside `community/` the count is **zero**.
25. **F-403 leaves one question no document can answer.** The correction establishes that *no source
    we hold supports* character font data or math tables in the boot ROM, and that the one
    authoritative content list omits them — so the KB must not state them. It does **not** assert
    they are absent: a 16 KB mask ROM can hold unlabelled data blocks that an assembly listing's
    symbol names would never reveal. If their presence ever matters, that is a question for Chip
    Gracey, **not a gap to research and not a release blocker**. Recorded so the silence reads as a
    decision rather than an oversight.

---

## 0.6 The 2026-08-29 pre-release fix pass — and the counting lesson it kept teaching

**Why there is a second pass at all.** The 2026-08-27 review left this document at release position
with §0.5 as the pre-ship list. Reading that list rather than trusting it turned up defects the list
had *named* but under-counted, every single time. In three consecutive cases the real class was
larger than the entry recorded:

| §0.5 entry | recorded | actually found | ratio |
|---|---|---|---|
| item 13 — SETXFRQ rounding | 2 values, 2 files | **17 values, 3 files** (incl. a published manual) | 8.5× |
| item 7 — F-378 compiler range | 1 site | **5 sites** | 5× |
| item 6 — F-377 pt2 fabricated header | header only | header **+ 2 further defects in the file** | — |

**The lesson, stated so the next pass does not relearn it: §0.5's counts are what the differential
read NAMED, not the size of the class.** The differential read examined the files that changed; a
defect class does not respect that boundary. Every entry here should be treated as *"at least this
many"* and the class recomputed from the rule, not from the list. Three of the four biggest finds in
this pass were invisible to every gate and would have shipped.

**A second-order lesson, from F-381.** Fixing a file can *reveal* defects rather than introduce
them. Citing three previously-uncited files moved them out of the sourcing gate's advisory class and
turned 12 always-uncited blocks into blocking violations. A gate going red after a repair is not
necessarily a regression — check whether the repair changed what the gate can *see* before treating
it as one.


---

# PART 1 — By change class

A class is one *reason*. Each carries: **what** it is · **the lack** — what was absent that let it
exist or persist · the files it touched · the net effect. A class usually crosses regions; Part 2
is the same facts arranged the other way.

---

## 1.1 The uncited-quantity purge — 119 blocks, 41 files

**What.** Every top-level block that stated a physical quantity without naming a source was deleted:
**60** from `architecture/`, `language/`, `guides/`, `application-notes/` (`15c84de5`, 25 files) and
**59** from `hardware/` (`c733a223`, 17 files). Removal moved first, on purpose — the damaged set was
being served while the repair ran, and there was to be nothing to grandfather when the gate was armed.

**The lack.** Nothing had ever asked whether a stated quantity named its source. `io_pin_timing.yaml`
went 433 lines to 175 in one commit, and that included both blocks F-327 proved fabricated **and**
four further ranges F-327's line numbers did not cover — a fix applied literally to those lines would
have left the same ladder standing in two more blocks.

**Two gate defects surfaced *by* the purge, and the first zero was false.** `c733a223` records that
`INLINE_CITE_RE` read `rev B` / `rev C` as a citation — on a board file that is a board revision, and
worst precisely in the tree where every file legitimately names one — and that `CITE_RE` tested the
key name rather than the value, so `source: External 5V power supply` counted as a citation of a power
supply. Both silence rather than over-fire, which is how a purge could report success over eleven
blocks it never looked at. `1f37ae58` then found a third member of the same family: the deferral
*"Check datasheet for package limits"* matching on the token `datasheet`. The generalisation is in
**F-335**: the citation side matched on the presence of a token, not on whether the sentence
attributes the block to a document.

**Two consequences the executing agent could not see**, measured at the boundary: deleting the uncited
`pull_up_modes`/`pull_down_modes` blocks resolved 18 of the 23 drive-strength CONTRADICT rows as a
side effect, and orphaned five constants whose only definition lived inside those blocks — which is
why §1.5 defines 55 rather than 50.

---

## 1.2 Source-first repopulation — 80 blocks returned, cited

**What.** The removed blocks were rebuilt **by reading the source, not the removed block**: 46 return
in `597d5eba` (24 files) and 34 in `491f2b55` (15 files), each carrying the document and a
`file:line` into it.

**The lack.** Nothing had ever required a block to be written *from* a source rather than checked
*against* one. Reading the sources first is what paid beyond the brief, and it paid every time:

* **WAITMS / WAITUS shipped a ceiling wrong by a factor of four hundred.** The files claimed
  1–4,294,967 **milliseconds**; v55 bounds them in **clocks**, at `$8000_0000`, which at 200 MHz is
  under eleven seconds. That is the kind of wrong a long delay discovers at runtime.
* **A restored guide block claimed ORG's cog limit as `$1F0`.** v55 says `$1F8`.
* **A boot block claimed the ROM issues no `HUBSET` before jumping.** Its own listing contradicts it;
  the `Prop_Clk` and shutdown paths both do.
* **The PLL lock conflict settled at 10 ms, not ~10 µs** — three Parallax documents state it on two
  extraction paths each, all three emit `WAITX ##20_000_000/100`, and v55 states it twice more. The
  microsecond figure has no source at all. Settling it turned up a **fifth** site the finding never
  named: two `clock_system` examples waiting 100 µs, invisible to the gate because it strips code
  regions before scanning.
* **The `alternate_part: 64000-ES`** on `edge-32mb-module.yaml` was deleted *by the repopulation*,
  with a note saying why — it is the only block the repopulation removed.

---

## 1.3 The 41 blocks that did not come back — three different outcomes, kept apart

Collapsing these into one number would say we could not verify content we know is fabricated.
The strict key-set delta at HEAD is **41 keys across 18 files** (§0.3).

**(a) Fabricated or disproven — 15 keys.** `architecture/io_pin_timing.yaml` ×8
(`timing_specifications`, `clock_relationships`, `drive_strength_configurations`, `slew_rate_control`,
`input_characteristics`, `special_timing_modes`, `protocol_timing_examples`,
`compensation_techniques`); `language/pasm2/concepts/basic-io.yaml` and
`language/spin2/concepts/basic-io.yaml` ×3 each (`drive_strength_configuration`,
`timing_considerations`, `hardware_specifications`); `hardware/p2-eval-board.yaml video_audio`.

The falsification was run against the **completed** Silicon Doc extraction, not the earlier partial
one: `slew` returns **0** hits across `silicon-doc/`, `p2-datasheet/`, `p2-hardware-manual/`,
`smart-pins/` and `spin2-v55/`; so do `fall time` and `FR4`; `VIL`/`VIH` return **0** in the datasheet,
the Silicon Doc and the Hardware Manual. `Schmitt` appears 103 times — always as an input **mode**
(`Pin Schmitt`, `P_SCHMITT_A`), never as a threshold. **The mode is documented and is in the KB; its
electrical characterisation is documented nowhere and is correctly absent.**

**(b) True, and still out — 24 keys, all in `hardware/`.** Ruled correct but *not actionable*: they
cannot change the code an agent emits. Each is verified present in the ingestion tree, so nothing is
lost — it is not shipped. Across `addon-hd-audio` (2), `addon-hyperram-hyperflash` (1),
`addon-motor-driver` (2), `addon-rtc` (2), `addon-serial-device` (2), `addon-serial-host` (3),
`addon-wx-wifi` (2), `edge-32mb-module` (1), `edge-breadboard-carrier` (3), `edge-mini-breakout` (2),
`edge-standard-breakout` (2), `edge-standard-module` (1), `hub75_adapter` (1).

One of them came **back** later by a different route: `addon-wx-wifi part_variants` carried the
DIP-to-Activity-Board mapping, and `599d3660` recovered that content from the ingestion tree into a
cited `form_factors` block. The key name did not return; the fact did.

**(c) Authored here, no upstream — 2 keys. This is the open gap.** `io_pin_timing best_practices` and
`click_module_integration best_practices` are correct and actionable, and **nothing we hold supports
them**. Writing them into the ingestion tree to cite them would manufacture provenance inside the
fidelity gate's documentary truth root — the exact defect F-341 files. **F-352** records that the
removal rule needs a fourth branch for authored-here content with no upstream. Still open.

---

## 1.4 The drive-strength mislabel — the class this sprint started from

**What.** The P2 has **no pull-up or pull-down resistors.** `P_HIGH_*` / `P_LOW_*` select **drive
strength**, and the shipped KB described them as bias resistors — so an agent asking how to enable a
pull-up was handed a mechanism the silicon does not have. That was the reported symptom.

**The lack.** One fact written in many places, with no single home, and no instrument that reads a
sentence. The purge had already resolved 18 of the 23 CONTRADICT rows by deleting their blocks; the
remaining five were reworded from the v55 table, and the structural half is **deletion and
repointing**, not rewording in place: no file restates the mechanism, and each carries a full-path
reference to the single definition home.

**Files.** `language/spin2/methods/{pinfloat,cogstop,wrpin}.yaml` ·
`language/spin2/conventions/{johnny-mac-documentation-style,spin2-docs-jonnymac}.yaml` ·
`language/{pasm2,spin2}/concepts/basic-io.yaml` · `guides/{pasm2,spin2}-getting-started.yaml` ·
`code-examples/smart-pins-002-button-reading.yaml` ·
`architecture/smart-pins/smart-pin-00000-normal-mode.yaml` · `hardware/addon-control-board.yaml` ·
`hardware/addon-rtc.yaml` · `hardware/edge-{32mb,standard}-module.yaml` ·
`architecture/pin-drive-configuration.yaml` (new).

**What reading the examples found, beyond the mislabel.** Nine examples were extracted from the
shipped YAML **bytes** rather than retyped, compiled, and then read for semantics — which is the whole
point, because F-322's examples all compiled and were all wrong. The reading found a `TESTP` whose
comment inverted the flag polarity so the handler ran on the wrong half; a `JMP #$` self-jump that
blinked once and hung; an `ORG` followed by data so execution began on a LONG; a setup routine
nothing called; and a glitch rule that contradicted both of its own examples. Filed as F-345/F-346.

**Two residues this sprint killed after the fact.** `75971308` removed E-010 from the shipped set —
both Edge Module files said the LEDs could be held by *"enabling a pin pull-up"*, and **both lines
had been rewritten in this release with the phrase intact**, which is how it survived. And
`ca07aaf7` dropped "pull resistors" from a routing blurb in `spin2-getting-started.yaml`, honest now
that `basic-io.yaml` states the P2 has no internal pull network.

**Two findings went to Parallax rather than into the KB** (F-342, F-344): the RTC add-on guide itself
teaches the mislabel and prescribes it in input mode, where a drive selection cannot do anything; and
an eval add-on guide calls a switch active-high and says the pin is driven low when asserted, in one
sentence.

---

## 1.5 One definition home, and the aliases that made it reachable

**What.** The KB referenced **55 constants it defined nowhere.** All 55 are now defined, worded from
the Spin2 v55 table rather than the v51 extracts (superseded for eight of them), in one file that
covers all 116 v55 constants, each defined exactly once. Seventeen duplicate definitions in
`language/spin2/methods/wrpin.yaml` and `architecture/smart_pins.yaml` were replaced with **pointers
rather than corrected**, because F-321 and F-323 exist precisely because one fact was written twice
and the copies drifted. Six one-line restatements in `language/pasm2/wrpin.yaml` went the same way.

**The lack — and it is the mechanism behind the whole sprint.** `generate-p2kb-index.py` harvests
top-level `aliases:` **only**, and the symbol file had none. Not one of its 48 existing constants
resolved through `p2kb_get`, and 55 more would have satisfied the gate while leaving the reporting
agent exactly where it started. A top-level `aliases:` block of 116 names fixes that at the mechanism.
`ad4f974f` then found seven `streamer/` files with no aliases at all — unreachable by name — and gave
them some.

**The new `architecture/pin-drive-configuration.yaml` states its facts by ENCODING, never as
name-to-description**, and that shape is deliberate: the fidelity tool reads a constant name used as a
YAML key as a *definition*, so the natural spelling would have created a second definition home for
sixteen constants inside the task chartered to end that defect. Verified against the tool's own
regexes, not by eye.

**Two fabricated names deleted with nothing substituted.** `P_LEVEL_B` and `P_SCHMITT_B` are rejected
by `pnut-ts` while seven real siblings compile, and v55 carries only their `_FB`/`_FBP`/`_FBN` forms.
**F-340** records how they survived: the crossref validator reads top-level keys only, so nested
`related_symbols:` lists have never been checked — they were not missed by bad luck, they sat in a
field the instrument does not read.

---

## 1.6 The fabricated-provenance class — six files re-derived from scratch

**What.** **F-359** established that seven `architecture/` files carry a provenance header citing
silicon-doc files that have **never existed** (`part3-pins.txt`, `part1-cog.txt`) and datasheet page
ranges beyond the end of a 50-page datasheet — all written in one 2025-11-29 commit that touched
1,323 files and 973 YAMLs. One was purged this sprint; `9a1f14a3` **re-derived the other six** against
the now-complete silicon doc.

**The header was the signature, not the extent.** Across the six files:

| | Before | After |
|---|---|---|
| `- instruction:` entries carrying an `encoding:` | 47 | 45 |
| encoding **verbatim-identical** to the silicon doc's PASM2 encoding table | **2** | **45** |
| encoding **wrong** | **41** | **0** |
| mnemonic **not in the encoding table at all** | **4** | **0** |

**The semantic inversions, each of which a code-generating agent would have acted on:**
`interrupts.yaml` had the **IJMPx/IRETx address map inverted** — `$1F0` called IJMP1 where three
authorities say IJMP3; it also claimed per-level **shadow registers**, of which there are none.
`lookup_ram.yaml` had **LUT sharing backwards** (it is a WRITE path into the paired cog's LUT) and
**WRLUT's operands reversed** (D carries data, S carries address). `locks.yaml` carried a `LOCKTRY`
"query" form that actually **acquires**. `cog_attention.yaml` had **ATN as event 15**; it is 14, and
both SETINTx examples used the wrong number. `debug_interrupt.yaml` invented three "configuration
registers". `event_system.yaml` carried an invented event taxonomy in place of the sixteen the source
enumerates, and its pattern-match example selected **mismatch** mode while its comment said match.

**Four fabricated mnemonics deleted** — `RDCOGID`, `RDLUTS`, `NIXINT0`, `TRGINT0` — each checked three
ways first: absent from the silicon doc, absent from every other file under `deliverables/ai/P2/`, and
not accepted by `pnut-ts` v1.55.3, with `cogid` compiling clean as the control. Each site keeps a note
saying what was removed and why, so nothing restores them.

**The lack.** Nothing checked generated content against a source at creation time, and **the citation
header was generated along with the content it claims to source**. A fabricated citation is not an
error in sourcing; it is the signature of never having sourced. 973 YAMLs in one commit is the scale
at which that becomes invisible. 🔴 **And the gate is not the evidence:** `audit-yaml-claim-sourcing`
read `0 Tier 1` before this work and reads `0 Tier 1` after it, because none of the six carries a
unit-bearing quantity block. The evidence is that every `<file>:<line>` written into them was re-read
at the line it names. The instrument was separately shown live on these files — a planted two-quantity
block in `locks.yaml` produced `TIER 1 … 1 violation` and exit 1; removing it returned exit 0.

**Still open from this class:** the **eight non-derivable claims** (§0.5 item 1, F-359) and the
**eighth file** the list never contained (§0.5 item 6, F-377).

---

## 1.7 Wrong scalars and invented board identities — what a source-first read exposed

**What.** Reading the guides instead of the removed blocks found defects in blocks that had **survived
both purges**, because a purge keyed on missing citations does not find a wrong scalar or an invented
section.

* 🔴 **`max_current_per_pin: "150mA"` in both `basic-io.yaml` files.** The datasheet's absolute
  maximum is **±30 mA**. That is five times the limit, in the exact number a reader uses to size an
  LED series resistor, and following it damages hardware. The same block carried `VOL 0.4 V` /
  `VOH 2.4 V`, which are 5V-TTL figures. Both copies deleted; the correct facts already ship, cited,
  in `io_pin_timing.yaml`.
* 🔴 **`#64006G` was described as a Combined Digital I/O board** with four LEDs and four switches.
  `#64006G` is the **Goertzel** board; the LEDs and switches belong to `#64006A`. An agent generating
  code against that entry gets pin assumptions for a different board entirely. The corrected file
  still named the invented `digital_io_board` slug in two guidance lists afterwards; `75971308`
  removed it, and sweeping that class found two more slugs naming no board at all (`eval_board`,
  where the key is `p2_eval_board`, and `breakouts`). **Nothing validates these lists**, which is why
  a fabricated name lived there.
* **Invented carrier part numbers** where real ones exist · a carrier dimension off by a factor · a
  mini breakout credited with all 64 pins on castellations · an eval board given a barrel jack it
  does not have · a fabricated "USB connector onboard" on two breakouts · a false "all add-ons use
  P0-P7" in the compatibility matrix · a fabricated `alternate_part: 64000-ES`.
* **`p2-eval-board.yaml`**: Rev D → Rev C, 320 MHz → 180 MHz recommended, the real flash part,
  3.55 in, and roughly ten `TBD` placeholders replaced with sourced values.
* **`hub75_adapter.yaml`**: the manufacturer's **70 MHz** replaces the unsourced 40/35 MHz.

**The lack.** No instrument reads a scalar for plausibility, and none reads a board name for
existence. Both classes are caught only by reading the guide.

---

## 1.8 Not-actionable content removed — the promotion filter

**What.** `1f37ae58` asked a question neither purge asked: not whether a block is true, nor whether it
is cited, but **whether it can change the code an agent emits.** 233 blocks across both populations
were given a written disposition — 114 that survived the purge, and 119 the purge removed that the
repopulation would otherwise have had to re-decide.

**The lack.** The KB had no stated rule for *correct but useless*. Quality commentary is the clearest
case: `waitus.yaml`'s removed content was "excellent / good / marginal resolution" — a judgement, and
the KB entry rule states existence, access and utility, never quality.

**Still un-dispositioned** (§0.5 item 17): `hardware/p2-hardware-selection-guide.yaml` and
`p2-hardware-feature-comparison.yaml selection_criteria` were correctly *retained* under sub-rule P
and never given a disposition — the same missing branch as F-352.

---

## 1.9 Citation paths — the ones that route every new agent, and 23 that pointed at a dead artifact

**What, part one (`69af3733`).** Both getting-started guides tell an agent that
`concepts/basic-io.yaml` is required reading before any I/O work — **and two real files answer to that
name**, so the citation pointed at nothing deterministic, straight at the files carrying the broken
pull-up examples. Each guide declared a `content_base` that would disambiguate and then refuted it
three lines earlier, with one path base-relative and its neighbour P2-root relative **in one block**.
The citations were right by the luck of the reader's guess. Fourteen bare paths across the two guides
are now repo-absolute, six more inside the `basic-io` files with them, and each `content_base` carries
a comment saying it is not a resolution base.

**The lack, measured.** `validate-crossref-keys.py` iterates a fixed fifteen-name field list against
the **top level** of each document. A reference nested below that is invisible; a field not on the
list is invisible even at the top. It sees 742 reference sites and cannot see 230 — it reports on
**76%**. The guide citations sat in `knowledge_progression` and `next_steps`, on neither list, so
exit 0 was never evidence about them. 136 of the invisible sites are `related_symbols` — precisely
where the two fabricated constant names lived. **F-340** and **F-373** carry the remainder.

**What, part two (`491d033b`).** All **23** shipped citations into `p2-documentation.txt` — the PDF-era
capture now known to be lossy — were re-anchored to `silicon-doc-text.txt`. Each was resolved **by
reading what the old locator pointed at and finding that content in the new artifact**, never by
translating line numbers, which do not correspond. The shipped KB no longer references
`p2-documentation.txt` at all. **One did not resolve, and that is the find**: F-372 + G-027.

**And the rule was not fully kept — §0.5 item 5.** F-377 found locators that *were* translated. A
range check over all 113 `silicon-doc-text.txt` citations returns 0 out of range, because a
translated locator lands inside the file. Only opening the line catches it.

---

## 1.10 Duplicate keys, and the gate that now exists

**What.** A duplicate YAML key does not error: `yaml.safe_load` keeps the **last** and discards the
first, silently. On 2026-08-25 that destroyed the central corrective sentence of this entire sprint —
`pin-drive-configuration.yaml` had `note:` twice inside `idioms:`, the second won, and every consumer
read the bench-gap paragraph where the corrective statement should be. `43061dad` restored it.

**The sweep found four more sites, all pre-existing**, and `d756b44c`+`e9dc9507` adjudicated every one:

* **`architecture/lookup_ram.yaml`** — an orphaned block (the body of a removed pseudo-instruction
  whose header had become a comment) was being absorbed into the **SETLUTS** entry above it and
  overwriting SETLUTS's `operation` and `usage_example`. **Anyone reading SETLUTS was reading streamer
  setup.**
* **`language/pasm2/drvl.yaml`** — the discarded `timing:` block was a strict subset of the kept one,
  and byte-identical to the live one in its twin `drvh.yaml`. So **DRVL and DRVH were disagreeing
  about pin timing in what consumers read**, and the three-clock DIRx/OUTx delay was uncited in both.
  Now cited in both, from the Silicon Doc and the Hardware Manual. *(The first source found for it was
  Titus material — an upstream lead, never citable. The Parallax primaries say the same thing.)*
* **`hardware/edge-breadboard-carrier.yaml`** — a structured `educational_value` mapping shadowed by
  the scalar `"excellent"`.
* Fixed with them: `edge-breadboard-carrier` has a power figure again (**5 VDC, 5.5 V absolute
  maximum**, cited) where a wrong 6–9 V had been removed with its whole block and nothing put back;
  `addon-serial-host` has an identity string again, with **500 mA continuous per socket** rather than
  the summed "up to 1A" nobody sourced; and the symbol file's claimed `1224` records over 136 actual
  ones is corrected — 1224 is the source document's whole universe, 1024 of the clock category being
  `XMUL1..XMUL1024` — with the provenance recorded so nobody restores it.

**The lack, and it is closed.** `verify-yaml-format.py` stays at exit 0 on a planted duplicate,
because duplicate keys are **legal YAML**. It asks whether a document parses, which they do; nobody
asked whether it says what it appears to say. `02ff61b7` armed
`validation/audit-yaml-duplicate-keys.py`, which walks the **composed node tree** rather than the
loaded object — by the time you have a dict the evidence is gone — and reports which line wins and
which is discarded. Its negative control fires on a duplicate at the root, nested in a mapping, and
inside a list item, and stays clean on good input and on the same key legitimately reused at a
different depth. It exits **2** on "nothing measured" rather than reporting an empty scan as a pass.
**Current state: 1132 files, 0 duplicates.**

---

## 1.11 New coverage written this release — four files

| File | Why it exists |
|---|---|
| `architecture/pin-drive-configuration.yaml` | The replacement for the fabricated drive ladder: the 13-bit field's sub-fields, eight real rungs, and the DIR/OUT rule, expressed by encoding and cited. §1.5. |
| `architecture/streamer/pin-capture.yaml` | Stephen asked whether four smart pins running SPI can be traced through their nearest neighbours at Nyquist rates. **They can, and the neighbour routing is required, not a convenience**: on a pin running a smart-pin mode, `IN` is the smart pin's **event flag**, not the pin's logic level, so pointing the capture path at the bus records ready pulses instead of traffic. The KB held the harmless half of that fact and not the operative half. The page refuses to state a sample-rate ceiling no source gives. |
| `hardware/addon-click-adapter.yaml` | `#64008` had no hardware record. Written from the schematic — the first source in this corpus where **no text-extraction path can work at all**: the sheet is vector art with its text converted to curves, proven by a negative control returning 0 occurrences of every net, signal and refdes token. Read from the page rendered at 200 and 600 dpi, with all four renders committed so the netlist is checkable without re-rendering. |
| `hardware/p2-package-mechanical.yaml` | `deliverables/ai/P2/` had **no package or mechanical record of any kind**. Full CASE 932BR dimension table (15 rows), recommended mounting footprint, pin-corner numbering, 12 aliases. Read from the transcription verified in «#312», **not** re-OCR'd — tesseract misreads digits on these sheets and these are precision values. Closes **G-021**. It also says what the drawing does **not** give: no thermal resistance, derating curve or thermal-via guidance exists anywhere in the corpus, so the record says so rather than letting a reader infer a thermal solution from pad size (**G-020 stays open**). |

**A self-audit followed the Click record** (`601e65ce`): three places where inference had been written
as reading are now labelled with what actually establishes them — "the 4 spare I/Os are free for other
use" (the sheet draws no pass-through), `base_pin_options [0,16,32,48]` (the sheet is base-relative
throughout), and the `signal_map` direction column (the sheet's arrows are net-label pointers and
carry no direction information).

---

## 1.12 Ingestion findings applied to the shipped YAML

The ingestion sprint routed its findings to the register by design — `ingest-source` forbids YAML
edits — so nothing it found had reached the KB until this release.

* **F-363** — `$1F6`/`$1F7` now read *"CALLD-imm return, CALLPA parameter"* / *"…CALLPB…"*. The two
  rows had been byte-identical where all three authorities draw a CALLPA/CALLPB distinction, and
  "parameter" named **neither** role.
* **F-364** — 13 dangling `yaml_file:` pointers removed from the register index (it advertised 16
  register files and 13 of the pointers did not exist); content kept inline.
* **F-368** — `getbrk.yaml`'s WZ sentence had lost the Z value for the queued branch, and the file
  declared `Z: No effect` three lines after stating that GETBRK **requires** a flag effect.
* **F-369** — the smart-pin DIR-reset mechanism, in the Silicon Doc and carried nowhere in the KB:
  each smart pin holds 126 bits of state separate from its WRPIN configuration.
* **F-370** — `taqoz-forth.yaml` called ROM TAQOZ "the finite, fixed version"; its author says it is
  also an **early** version. Sourced to the author's own reviewer comment.
* **`599d3660`** — the WX module's two form factors: `#32420S` (SIP) → the P2 WX Adapter `#64007`,
  which carries the 2×6 accessory-header footprint; `#32420D` (DIP) → the Propeller Activity Board
  socket, a **P1** board. Both records now say plainly that `#64007` is the only P2 WX adapter.

🔴 **Citation drift caught while applying, twice.** F-363 cited `silicon-doc-text.txt:313-314` — the
numbering from *before* the artifact was re-emitted; live location is `:452-453`. And F-369's own
register entry cited `:3360`, which today reads `(X,Y) ROTATION`, while the shipped YAML always cited
`:3856` correctly. Both found by **reading the cited lines rather than trusting them**, and corrected
in the register. Nothing downstream inherited either.

---

## 1.13 Files that disagreed with themselves — the class no instrument can see

**What.** Three separate repairs this release, all the same shape: one field in a file contradicting
another field in the same file, with every gate green throughout.

* **`language/pasm2/{addsx,subsx}.yaml` (`b466a538`, F-379).** Both carried the PASM2 Manual's prose
  verbatim — *"the C flag is set (1) if the result is negative (Result[31] = 1)"* — while
  `flags_affected` and the encoding row in the **same file** gave the true-sign form. `Result[31]` and
  the true sign differ **only on overflow**, which is exactly the condition `TJV` exists to detect,
  and the manual's own TJV description requires C to hold the correct sign. Refuted three times inside
  the manual itself (Tables 9 and 169; the TJV description; the summary tables). **Root cause:**
  commit `87511c99` (v1.11.1) repaired this class across `adds · cmps · cmpsx · subs` and three `SUM`
  files and **skipped these two** — a class sweep that misses two members leaves a defect that now
  looks deliberate, because every neighbour is correct. Two more in the same family, both CSV
  column-split artifacts in fields no gate reads: `sumz.yaml encoding[0].z` held the **C column's**
  condition text where the manual gives `Result = 0`; `sumc.yaml encoding[0].c` had the same prose
  welded in front of a correct semantic.
* **`architecture/interrupts.yaml` (`4caeb6cc`).** The top-level `description` at `:26` said *"Each
  interrupt level has its own set of shadow registers"* — forty lines above the file's own sourced
  statement at `:38-46` that **there are no shadow register banks**. §1.6 corrected the detailed block
  and left the summary contradicting it. The `description` is the first thing a retrieving agent
  reads.
* **`language/spin2/methods/pinfloat.yaml` (`4cecb02c`).** Right where it was explicit and wrong one
  line above: *"External pull-up/pull-down resistors will determine the level"* is the anti-mislabel
  statement, while the line before it omitted "external" and so read as a chip feature — in the P2
  method file a reader looking for a pull-up actually lands on.

**The lack, stated exactly.** Every instrument here passed all of these throughout: the files parse,
their keys resolve, their citations are present, and `pnut-ts` assembles the instructions regardless.
**A compiler proves legality, never a flag's meaning.** The encoding check that verified all 45
encodings in §1.6 cannot read sentences. Only reading a `description` against the same file's
`flags_affected` catches a file disagreeing with itself, and no gate does that.

---

## 1.14 The one gutted file — found by the differential read, restored source-first

**What.** `guides/pasm2-getting-started.yaml` lost its `file_structure.clock_setup` block: the file
explained what happens when you declare a non-RCFAST clock mode and **never said how to declare one**,
while citing the very source table that would. That is the differential read's `gutted` test — content
the KB **needs** *and* that a source we hold **can support**, both halves required. It was the only
one of 85 files to meet it.

**Restored (`ca07aaf7`), and not verbatim.** All nine legal CON declaration combinations are back with
their `%CC_SS` values, the `_errfreq` default of `1_000_000` and the 15/30 pF crystal-loading rule,
each carrying the v55 line it came from. The deleted text had called `_clkfreq` **"Required"**; v55's
own table row — *no symbol and not DEBUG mode selects RCFAST* — says nothing is required. That claim
was a **two-file class**: `spin2-getting-started.yaml` kept its block *and* the claim, in the key name,
the description and the example. Both corrected; a widened grep finds no others.

**The clock-ceiling block was replaced, not restored.** Its three figures were uncited, its "default"
contradicted the same file's own `clock_setup`, and *"340+ MHz"* traces only to a TAQOZ overclocking
anecdote — community material, an upstream lead, never citable — against a datasheet maximum of 320.
It now carries the datasheet's AC Characteristics min/typ/max, labelled as **absolute limits** rather
than recommended-use range, which is what **E-007** requires.

**One deliberate divergence from our own extraction**, recorded so nobody "reconciles" it back: the KB
ships `%01_11` where `spin2-v55-text.txt` reads `01_1 1`. The DOCX confirms that cell is split across
two Word runs, is the only one of the nine so split, and the spaced form appears **nowhere** in the
source. Our extractor inserted the space. A future pass that aligns the KB to the extraction would
introduce a bit pattern that does not exist.

---

## 1.15 Two register corrections REJECTED — and that is the valuable half

**What.** `9370c580` and `e92aa02f` refused corrections that would have introduced defects into
content that is currently correct.

* **The PLOT `TEXTSTYLE` vertical-align "swap" is not a swap.** The Pascal-derived directive matrix
  carries a warning that anchor-edge and ink-side vocabularies describe the same pixels, and that this
  exact ambiguity caused the row to be documented backwards once already. The v55 text mixes both
  vocabularies in one sentence; `plot.yaml` uses ink-side consistently and says so. What was actually
  missing is the **disambiguation the authority itself carries** — which is why this got filed as a
  defect twice.
* **The weight correction wanted "thin" changed to "light" for value 100.** The Pascal source declares
  `weight[0..3] = (100,400,700,900)`, and 100 is OpenType **Thin**. Light is 300.
* **Deleting F-251's pull-up sentence would have left a hole exactly where the reader is standing in
  front of a floating pin**, so it was raised instead of cut: no bias resistors, a choice of how hard
  to drive, and a weak drive is still a drive.

**And a measurement this sprint's own scope rested on was falsified rather than quietly widened.**
Plan §3 excluded manual prose because a sweep found the masters clean. Searching the IOSP master
**recursively** — it is split per chapter under `part-*` directories, which is how a flat glob misses
it — finds 23 mislabel lines, 5 internal-pull-up assertions, and four sites teaching the
`P_HIGH_15K | P_LOW_FLOAT` composition that has **no Parallax source at all**. Filed as **F-356**,
still `CONFIRMED`, because scope is Stephen's and the honest move is to falsify the measurement.

**An attribution error was corrected in five files.** `EF-063` and `EF-064` had been cited as the
empirical basis for "the P2 has no pull-ups". They are not pull-up findings: EF-063 certifies jumper
continuity, EF-064 establishes streamer pin placement. The weak drive is their **rig apparatus**, not
their subject, and the ledger holds no dedicated drive-strength finding. `e92aa02f` fixed
`pin-drive-configuration.yaml`; `75971308` swept the other four. Three of the ten citations were left
alone because they describe what the rigs actually did.

---

## 1.16 Schema reshaping — measured, and forced by the instrument

**What.** **34 top-level keys across 24 files changed YAML type** (23 `list→dict`, 11 `str→dict`),
re-derived here at HEAD. The typical case: a `signal_map` that was a list of rows becomes a mapping
whose sibling key is the citation for the rows.

**It is not a judgement call, and that was established by experiment.** With the citations moved to
the uniform-shape alternative — a sibling `signal_map_source:` key — `audit-yaml-claim-sourcing.py`
returns **exit 1 with 22 Tier 1 violations**, including all 19 of the blocks the in-block form
silences. The uniform alternative does not satisfy the armed gate. And for every block still carrying
the **old** shape (`signal_map` list ×10, app-note `gotchas` list ×4, hardware `description` str ×14),
the question *"would the gate demand a reshape here?"* was evaluated with the auditor's own helpers:
**0 of 28**. Not one is a block that got away. The rule is exact: **reshaped ⟺ the block stated an
uncited quantity inside a file that demonstrably cites.**

**All five consumers were executed against the new shapes and each was made to fail** on a shape it
cannot handle — `generate-p2kb-index.py`, `fetch-kb-file.sh`, `validate-crossref-keys.py`,
`audit-yaml-claim-sourcing.py`, and the p2kb-mcp fetch contract. Nothing breaks. **Verdict:
MEASURED-SAFE.**

**One of the 34 is not a reshape at all.** `hardware/edge-breadboard-carrier.yaml educational_value`
was a **duplicate top-level key** at `v1.17.0` — a mapping shadowed by the scalar `"excellent"`, which
YAML's last-wins rule made parse as `str`. HEAD removed the shadowing scalar, so the mapping that was
always in the file now parses. The type changed; nobody reshaped anything.

**What it does not settle.** Nothing enforces the rule and nothing records it in the tree. The next
block that acquires a quantity will drift the shape further, and the only thing that would catch it is
the citation gate firing — which fixes citation, not uniformity. Not blocking; no consumer is affected
today.

---

## 1.17 Instruments armed as blocking release gates

**What.** Three gates went from advisory to blocking in this range, and one was built from nothing.

| Gate | Armed by | Proven able to fail |
|---|---|---|
| `audit-yaml-claim-sourcing.py` | `43b0ede2` | A planted uncited quantitative block turns the release path red and names the file, line, block and units; removing it returns green with the file byte-identical. |
| `audit-constant-fidelity.py` | `43b0ede2` | A fabricated constant fires it; so does an instrument that cannot reach its inputs — **exit 2 on "nothing audited", with a message saying why, because nothing audited is never a pass.** |
| `audit-yaml-duplicate-keys.py` | `02ff61b7` | 5 negative-control cases; fires at the root, nested in a mapping, and inside a list item; clean on good input and on legitimate reuse at a different depth. §1.10. |
| `audit-register-hygiene.py` | `d62544ea` | The planted-duplicate `G-019` fixture passes **CLEAN at exit 0** through the pre-fix tool and **fails at exit 1** through the fixed one. |

**No baseline, no tolerance, no ratchet** — the purge removed the population first precisely so there
is nothing to grandfather.

**Arming meant fixing the harvest first, because a gate is only as true as what it reads.** The
fidelity truth side now globs `.txt` as well as `.md` and parses pipe rows by cell, so the current
Spin2 v55 symbol table — tab-indented, value in column one — is finally on it: **116 constants where
there were none**, with edition precedence so a superseded extract cannot outrank the current one.
`TRUTH_ROOTS` was deliberately **not** widened; widening it is what let a derived fact sheet shadow a
real source during planning (**F-341**).

**And `d62544ea` fixed a gate that was reporting CLEAN while reading nothing.** `audit-register-hygiene`
printed `0 entries` against a register full of table rows. Three changes: the table-row dialect is a
recognised entry form; the status vocabulary is **per-register**, selected off the counter label the
file declares (so `OPEN` stays excluded for the corrections register, where it is ordinary prose, pinned
by a control case); and the status is read from the row's own Status **cell** rather than anywhere in
the row, because the ledgers use lowercase lifecycle words that appear in prose too. A fifth register
nobody had looked at had the same defect. The ID family is a prefix **string** now, so the P1
namespaced allocators are governed rather than renamed. **All five registers now exit 0 with the gate
actually reading them.**

## 1.18 The 2026-08-29 pre-release fix pass — 6 files, 3 commits, all source-first

Every change below was made against a source read **at the line**, and the source is quoted in the
file. Nothing was inferred, and no value was changed to make a gate pass.

**`856ef2f2` — the SETXFRQ increment rule (F-380).** The *Parallax Propeller 2 Documentation* v35
states one rule for the streamer NCO word (`part2-pixel-ops.txt:117`, continuing at `:121` — one
sentence split by a page break): *"For fractions with remainders, the computed D/# value should be
incremented, in order to produce proper initial rollover behavior."* Its own table applies it —
`1/3` is `$2AAA_AAAA+1`, `1/5` is `$1999_9999+1`, while `1/2`, `1/4`, `1/8` carry nothing. So the
rule is **truncate, then increment on a remainder**; it is **not** round-to-nearest, which agrees
with the source only when the remainder happens to exceed half.

| file | wrong / total | what it also got wrong |
|---|---|---|
| `language/pasm2/setxfrq.yaml` | 2 of 4 | stated the rule **twice, differently** — `source:` quoted the footnote, `computation:` said `round()`; and cited `nco-timing.yaml` as a cross-check that "the two agree" while that file carried the same wrong value |
| `architecture/streamer/nco-timing.yaml` | **7 of 12** | its own ratio table is correct at **all 8** entries — the file applied the rule in one block and not the next |
| *(not KB)* Streamer Guide v1.1.0 master | **8 of 18** | taught `round()` in three places, incl. a worked example printing the wrong result |

*The lack:* nothing in this project can detect an off-by-one in bit 0 of a 31-bit phase word. The
values are well-formed hex of the right magnitude, they carry citations, and they compile. Only
recomputing from the quoted rule finds it. **⚠️ A Streamer Guide re-release is owed.**

**`9723e482` — `architecture/io_pin_timing.yaml`, the eighth fabricated-provenance file (F-377 pt2).**
Header cited `part3-pins.txt, pages 5-8`; no such file exists under `sources/silicon-doc/` and none
ever did. F-359 named seven such files. **The content proved genuine** — all four timing claims are
really in the Silicon Doc — so it was re-anchored, not removed: `:1987` (DIRx/OUTx three-clock
latency), `:1997` (INx read), `:2005` (TESTP read), `:3847` (smart-pin IN-flag reset), `:101`
(latch-up onset, now labelled as ON Semi wafer-lot failure analysis quoted in the revision history
rather than a characterised limit). Reading it found two more: **`"Smart pins add ~1-2ns to base
timing"` has no source** — zero nanosecond figures for this exist in any ingested Parallax source,
removed under cite-or-omit (F-327/F-333 class) — and `total_latency: 5 clocks` is a sum of a 2-clock
`DRVH` and the source's THREE, which the source never states as a total. The abs-max table was
re-read against `p2-datasheet-text.txt:2126-2149` and matches verbatim; the four package-and-supply
limits stated beside it are now named as deliberately out of scope, so their absence reads as a
choice rather than a gap.

*The lack:* a fabricated citation satisfies the sourcing gate exactly as well as a real one. The
gate checks that a citation is present; it never opens the file named.

**`efc683a8` — whose limit is it, the compiler's or the silicon's (F-378, and F-381 as a by-product).**

| symbol | shipped range (= pnut-ts acceptance) | P2 Datasheet rating | over by |
|---|---|---|---|
| `_CLKFREQ` | 3,333,333 Hz – **500,000,000 Hz** | PLL max **320 MHz** (`p2-datasheet-text.txt:2200`) | 180 MHz |
| `_XINFREQ` | 250 kHz – **500 MHz** | direct drive into XI max **200 MHz** (`:2198`) | 300 MHz |
| `_XTLFREQ` | 1 – **60 MHz** "typical" | crystal max **50 MHz** (`:2199`) | 10 MHz |

Plus `clkmode.yaml`'s PLL `use_case: "High-speed operation (up to 500 MHz)"` and a **500 MHz row**
in `timing_operations.yaml`'s rollover table — a speed no P2 clock source is rated to reach (now
320 MHz: 13.4 s rollover, 3.125 ns cycle, recomputed). All five now carry the compiler range
*labelled as the compiler range*, the datasheet rating beside it, and the *Parallax Propeller 2
Documentation*'s 350 MHz `VCO / 1` overclock ceiling (`part3-interrupts.txt:545`) — three distinct
numbers the reader was previously handed as one. This is **E-007's label-which-framing rule**, which
had been settled for the Hardware Manual's clock limits and never applied here.

Two further defects, found by reading the files while citing them: `timing_operations.yaml`
described the system counter as **32-bit** where the Silicon Doc says it was *"extended to 64 bits.
GETCT WC retrieves upper 32-bits"* (`silicon-doc-text.txt:55`) — the file now says the counter is
64-bit and that the rollover discussion concerns the 32-bit value `GETCT` returns alone; and its
`minimum_resolution` block carried a `min_practical` column (~1 us / ~100 ns / ~50 ns / ~30 ns) plus
*"Spin2 interpreter overhead adds several microseconds to any operation"*, **neither of which any
source states nor any bench result here measures**. Removed, with a note that the overhead is real
and wants a silicon measurement before the KB prints a figure for it.

*The lack:* nothing compares a `range:` against the silicon rating for the same quantity, and
nothing flags that a range's source is a **compiler guide**. Both numbers are true; the entry never
said which question it was answering.

**Per-file, this pass:**

| file | +/− | new to the change set? | verdict |
|---|---|---|---|
| `language/pasm2/setxfrq.yaml` | +18/−15 | no (already in the 89) | **stronger** — 2 wrong values, rule restated, self-corroborating cross-check removed |
| `architecture/streamer/nco-timing.yaml` | +28/−10 | no | **stronger** — 7 wrong values, `source:` added to `video_rates` |
| `architecture/io_pin_timing.yaml` | +29/−14 | no | **stronger** — provenance re-anchored, 1 unsourced claim removed |
| `language/spin2/constants/special-configuration-symbols.yaml` | +17/−3 | **yes** | **stronger** — 3 ranges labelled, 4 blocks cited |
| `language/spin2/concepts/timing_operations.yaml` | +31/−12 | **yes** | **stronger** — counter width corrected, unsourced estimates removed, 6 blocks cited |
| `language/spin2/system-variables/clkmode.yaml` | +3/−2 | **yes** | **stronger** — PLL ceiling corrected, 2 blocks cited |

**Registers moved:** `F-380` filed (SETXFRQ class) · `F-381` filed (Tier-2 structural) · `F-378`
rewritten in place and **RESOLVED** · next finding ID now `F-382`.


---

## 1.19 The 2026-08-30 pre-release fix pass — 18 files, 3 commits, and the two instruments that had to be fixed first

Three commits: `ca684aac` (steps 1-2), `912100db` (step 3, mechanical half), `9ab0433b` (step 3,
semantic half). Four files entered the change set — `architecture/hub.yaml`,
`hardware/p2-hardware-selection-guide.yaml`, `language/spin2/methods/coginit.yaml`,
`language/spin2/methods/cogspin.yaml` — and fourteen already in it were re-touched. **No file was
added to or removed from the shipped set.**

### The four files new to the change set

| File | ± (v1.17.0..HEAD) | Verdict | What changed |
|---|---|---|---|
| `architecture/hub.yaml` | +42/−2 | stronger | **F-391.** `protection_bit: "Set via HUBSET D[2]"` — W is **D[16]**; D[2] is inside the per-cog debug-enable field, so a HUBSET assembled from the old sentence carries the `%0000` clock-configuration opcode, not `%0010`. Replaced with the full operand map (`%0010_xxxx_xxxx_xxLW_DDDD…`, L=D[17], D[15:0]) and the three worked examples, cited to `silicon-doc-text.txt:2743-2762` and `:2765-2772`. Separately, `state_preservation: "All COG states saved on debug entry"` — the silicon saves `$000..$00F` only, via the `$1F8` ROM routine, **and `debug_interrupt.yaml` already said so**, so this page was contradicting a sibling. The two pages are now linked. |
| `hardware/p2-hardware-selection-guide.yaml` | +52/−22 | **corrected** | **F-396** — see below. Fabricated part numbers, USB-C on a micro-USB board, three wrong board dimensions, castellations that appear nowhere in the guide, an unsourced VGA resolution ceiling, and **F-397**'s `"5V @ 1A minimum (USB-C or barrel jack)"` / `"50-500mA each"` power block. |
| `language/spin2/methods/cogspin.yaml` | +28/−2 | **corrected** | **F-390.** `-1` is gone as an input. It is not a synonym for `NEWCOG`. |
| `language/spin2/methods/coginit.yaml` | +25/−3 | **corrected** | **F-390**, plus the two `_PAIR` symbols the file had never listed. |

### The fourteen re-touched, with their revised totals

`hardware-compatibility-matrix.yaml` **+174/−47** (was +27/−2 — this pass is +147/−45 of it) ·
`streamer/pin-capture.yaml` **+324/−0** · `streamer/pin-selection.yaml` **+193/−57** ·
`architecture/clock_system.yaml` **+185/−136** · `architecture/lookup_ram.yaml` **+156/−99** ·
`architecture/pin-drive-configuration.yaml` **+277/−0** ·
`hardware/edge-32mb-module.yaml` **+225/−419** · `hardware/edge-standard-module.yaml` **+173/−336** ·
`language/pasm2/concepts/basic-io.yaml` **+96/−121** ·
`language/spin2/concepts/basic-io.yaml` **+89/−121** · `architecture/locks.yaml` **+91/−53** ·
`streamer/modes-reference.yaml` **+49/−9** · `streamer/dds-goertzel.yaml` **+31/−10** ·
`application-notes/p2an002-cordic-for-real-work.yaml` **+19/−12**.

---

### Change class 1 — the census's 19 uncited electrical quantities, sourced or removed (F-397)

All 19 now carry a block-level `source:`. **Tier-2 advisory 32 → 27; Tier 1 stayed at none**, so
citing two wholly-uncited files exposed no uncited sibling block in either — the F-381 trap was
checked for, not assumed.

Reading them found **three of the nineteen were wrong**:

- **`"64006A (Control) - ~16mA max (4 LEDs)"`** — **no source anywhere states 16 mA.** The #64006
  guide gives the Control board four blue LEDs and four push-buttons, each on a **470 Ω series
  resistor** (`p2-eval-add-on-boards-text.txt:62`, `:74-80`), and no current at all. 16 mA reads as
  4 × the LED Matrix's 4 mA — a figure borrowed from a different board with different circuitry and
  presented as this board's maximum. **A derived electrical quantity wearing a data key is the
  150 mA defect in miniature.**
- **`"64006H (A/V Breakout) - 80mW audio amplifier"`** filed under `addon_power_requirements.high_power`.
  80 mW is real (`:328`, *"Amplified Audio Out (80mW)"*) but it is the amplifier's **output** rating.
  Filed as a power *requirement* it invites a supply budget built from the wrong number.
  **A correct citation attached to a miscategorised quantity still ships a wrong claim.**
- **`"5V @ 1A minimum (USB-C or barrel jack)"`** — 1 A appears in no guide, and see class 2 for the
  connector.

### Change class 2 — three inverted or damaging facts, found by reading (F-395, F-396)

- **`external_power: "5V or 6-9V depending on carrier"`.** **No P2 carrier accepts a wide input.**
  All three guides state the same requirement verbatim — *"Voltage input requirements: 5 VDC,
  absolute maximum 5.5 VDC"* — each followed by a boxed *"CAUTION! … do not exceed 5.5 VDC"*. A
  reader taking the KB at its word applies 9 V to a 5.5 V absolute maximum. This is the
  `max_current_per_pin: 150mA` shape exactly, and `edge-breadboard-carrier.yaml` had *the same*
  wide-input claim removed on 2026-08-25 (item 7 of the archived ledger) — **the sweep stopped at
  that file.**
- **`addon_support: "none"` / `"No 2x6 expansion headers"`** for the #64029 and #64019, and
  *"Cannot use 64006-series add-on boards"* under `incompatibilities`. **Every carrier has 2x6
  accessory headers and takes the #64006 boards** (`edge-breakout-board-narrative.txt:39`,
  `edge-mini-breakout-narrative.txt:45`, `edge-module-breadboard-narrative.txt:56`), and our own
  `edge-mini-breakout.yaml:56-58` already said so — **the file contradicted a sibling page**, the
  F-391 shape. **Nine sites** across five blocks carried the inversion. An agent asked "which board
  for add-ons?" was told to buy the Eval Board and that two of the three carriers are disqualified:
  the recommendation wrong and the reason for it fabricated.
- **`pin_access: "P0-P31, P58-P63 accessible (40 pins)"`** in `edge-standard-module.yaml` and
  `edge-32mb-module.yaml`. **The range and the count disagree with each other** — P0-P31 + P58-P63
  is 38. The guide says P56-P63, which is what makes 40. *The file's own arithmetic was the tell,
  and nothing checks arithmetic.*

Also corrected: the `combinations` table's `pin_access:` was a single bare integer that meant the
carrier's header count on some rows and the module's free-pin count on others, so P2-EC32MB on a
full 64-pin carrier read `40`. A pin budget is the product of **two** independently sourced facts —
what the module frees and what the carrier brings to a header — and both are now stated per row,
with no derived total. **The unsourced `rating:` values were deliberately left in place**: they
belong to F-374, whose class boundary is still Stephen's call, and removing six of the thirteen
would have silently moved that finding's count.

### Change class 3 — F-350's sweep never ran, and the whole fabrication set was still live (F-396)

`p2-hardware-feature-comparison.yaml:159-167` carries a `corrections_applied_2026_08_25` block
naming exactly what F-350 removed. **Every item on that list was still present in the sibling
`p2-hardware-selection-guide.yaml` five days later**, because F-350 was applied to the file where it
was noticed and the family was never swept: `64000-ES` ×3 (the Rev C guide documents **#64000**),
fabricated `P2-EVAL-STD-BREAKOUT` ×2 and `P2-EVAL-MINI-BREAKOUT` ×3 (the parts are **#64029** and
**#64019**), *"USB-C programming"* ×3 on a board with two **micro-USB** sockets, `127x89mm` /
`76×51mm` / `38×25mm` against the guides' 3.55×3.55 in / 4×1.4 in / 3.15×1.4 in, and
*"castellation mounting"* ×2 where the string *castell* appears **nowhere** in the #64019 guide.

**The lesson, and it is the point of the class.** F-350's disposition read as complete because the
file it was found in was fully repaired **and carries a correction record saying so**. What made it
incomplete is invisible from that file. **A fabrication that reaches a family of sibling documents
is one finding with N locations, and a repair record written inside one of them looks identical to a
finished sweep.** Two consequences worth carrying: a correction record belongs with the **finding**,
not only in the repaired file; and a finding that names a fabricated value cannot close until the
sweep has run corpus-wide **and been reported with its total**.

### Change class 4 — the citation read, and the instrument that had to be repaired first (F-399)

This discharges **F-377** and the census's category-1 "409". **721 locators, 83 files, 40 source
documents, every one opened at its cited line and read.** The census's 424/409 is the same
population at coarser granularity: this extractor enumerates bare continuation locators separately,
expands multi-locator tokens, and includes the ~30 citations this release added.

**Two instrument defects, either of which alone would have produced a confidently wrong measurement:**

1. **`str.splitlines()` breaks on FORM FEED.** **117 ingested sources disagree with `grep -n` about
   their own line count** — `p1-propeller-manual-v1.2-layout-text.txt` by **+398**,
   `122-32305-PE-Labs-Fundamentals-text.txt` by +232, `pasm2-manual-narrative.txt` by +161,
   `p2-documentation.txt` by +122. They are PDF captures; the form feeds are page breaks. The
   citations were written against `grep`/`sed` numbering and a human verifies with `sed -n 'Np'`, so
   **newline-only is the truth side**. Under `splitlines()` the extractor called **14** citations
   blank; the true figure is **6**. Eight "defects" were the instrument's own. *Any future tool that
   resolves a `path:line` citation against these sources must split on `\n` only.*
2. **A bare continuation locator has no unambiguous owner.** This corpus writes locators on **both**
   sides of the path they belong to. Nearest-token and preceding-token binding each mis-bind a
   different set. Where a locator could not be bound without guessing the **citation** was
   rewritten, not the tool — ambiguity that misleads a tool misleads an agent chasing it. Fixed in
   both `basic-io.yaml` files and `streamer/pin-capture.yaml`; the surviving `v55:NNNN` shorthand is
   registered as **F-400** and deliberately not half-swept.

**22 locators repaired across 12 files.** Ten were the F-365 carry-over shape —
`p2-documentation.txt` numbers attributed to `silicon-doc-text.txt`, in `streamer/pin-capture.yaml`
and `streamer/pin-selection.yaml` — some landing in range on unrelated content (line 3604 is CORDIC
example code), some past the end of the file. **The claims were right in every case; only the
locators were wrong**, which is precisely why the range check reported zero. The other eight were
found by reading and by nothing else:

| File | cited | actually there | should be |
|---|---|---|---|
| `p2an002-cordic-for-real-work.yaml` | `:434`, `:5145`, `:5401` | COGID / COG RAM; the RDLUT and MERGEW encoding tables | `:3304`, `:3315`, `:2054`, `:2291`, `:3413` |
| `architecture/locks.yaml` | `:1794` for **LOCKRET** | **`into C.`** — a wrapped continuation of the LOCKREL row above it | `:1795` |
| `architecture/lookup_ram.yaml` | `:1831` as a LUT instruction row | **RDLONG** | `:2061`/`:2063`/`:2065`, with `:1830-1832` correctly labelled as RDLONG's cog/LUT block-transfer note |
| `streamer/modes-reference.yaml` | `:3653-3654` for the D[16] bit-order flag | `jmp #loop 'loop for another sample set` | `:1456` |
| `streamer/dds-goertzel.yaml` | `:4062-4095` for S[11:0]/%T; `:4289-4305` for the worked program's longs | the PWM/SMPS smart-pin mode text; Table 34's clocks/bits rows | `:1586-1600`; `:1686-1687` |
| `architecture/clock_system.yaml` | `:520` | a blank line | `:521` |
| `edge-standard-module.yaml`, `edge-32mb-module.yaml` | a bare `narrative.txt` | resolves to nothing | the full path; both line numbers were already right |
| `pin-drive-configuration.yaml` | `complete-tables-reference.md:326-338` | that basename exists under **both** `p2-datasheet/` and `p2-hardware-manual/`, and F-367 established two same-named documents can differ | the full `p2-datasheet/` path |

**A new defect class this pass names: the wrapped table row.** The PASM2 tables in
`p2-datasheet-text.txt` wrap a long description onto the line **above** its mnemonic, so an
off-by-one lands on a neighbouring instruction's prose **and still reads like a table row**. That is
what `:1794` was.

**Two mechanical class-checks now run corpus-wide, both clean after repair.** The carry-over
detector — compare each `silicon-doc-text.txt` citation's claim against the same line number in the
superseded capture — returns **zero** across all **222**. The no-shared-anchor detector flagged
**175 of 721**; all 175 were read individually and all are sound (prose claims citing prose
legitimately share no mnemonic).

⚠️ **What this does not certify.** It closes *"is the claim supported by the line it cites?"* It says
nothing about a claim that cites nothing (the Tier-2 population, F-381), and nothing about a claim
that is simply wrong in a file with no citation defect at all — the **F-390 / F-391 / F-395** class,
which has no instrument and which this same pass found three more members of. **The delta is not the
defect boundary, and neither is the citation set.**

---

## 1.20 The 2026-09-05 codegen-effect audit — the question the whole release exists to answer

One commit, `395d6362`, and **two files changed** — because this pass was an *audit*, not a fix pass.
Its output is `engineering/analysis/2026-09-05-codegen-effect-of-the-unpublished-yaml-delta.md`; the
two file changes are the two defects the audit found **in its own delta** and repaired rather than
carried.

**The question.** Every other pass asked *is this content correct?* This one asked the only question
the release is actually for: **of the content an agent receives, do these changes weaken its ability
to generate code?** Nothing else here measures that direction.

**The method matters more than the answer, and it is the reusable part.** Today's instruments were
run over **a real `git worktree` checkout of `v1.17.0`** with the tools copied in — *not* a flat copy
of the old tree. Three of the gates did not exist at that tag, and all three derive the repo root
from their own path: a flat copy silently breaks that derivation and returns **a false green**. So
every "before" figure below is first-hand, and none of it is relayed from a commit message.

| Instrument (today's, run over both trees) | `v1.17.0` | HEAD | direction |
|---|---|---|---|
| Uncited quantitative blocks, Tier 1 (blocking) | **128** | **0** | ▲ |
| Tier 2 advisory (wholly-uncited files) | 66 | 27 | ▲ |
| Constant-fidelity Tier 1 (mechanical) | **50** | **0** | ▲ |
| Constant-fidelity Tier 2 `CONTRADICT` | 23 | 0 | ▲ |
| Files with duplicate YAML keys | 3 | 0 | ▲ |
| PASM2 encodings present but **fabricated** | 41 | 0 | ▲ |
| Cross-reference sites | 1,319 | 1,423 | ▲ |
| …of which unresolved | 21 | 19 → **18** after this pass | ▲ |
| PASM2 mnemonic lines in examples | 62 | 227 | ▲ |
| Spin2 method-call lines in examples | 27 | 48 | ▲ |

*(Its findability rows — files with a top-level `aliases:` block 71 → 84, alias keys 508 → 755 — were
measured at `a7fd84e3`, **before** F-401. At HEAD they read **100 files (8.8%) / 961 keys**; see §0.2,
and do not confuse either with the index's 2,896-entry alias table, which is a different instrument.)*

**Four things the *published* set was telling agents**, each of which an agent would have acted on:

1. **The interrupt vector map was inverted.** `IJMP1`/`IRET1` given `$1F0`/`$1F1` where the Silicon
   Doc says `IJMP3`/`IRET3` — stated twice, at `:446-451` and `:2296-2301`. **An INT1 handler
   installed itself into INT3's register and still compiled.**
2. **Forty-one fabricated instruction encodings.** Of the 44 removed from the `architecture/` concept
   files, 41 appear nowhere in the Silicon Doc's PASM2 table; all three that do are still carried,
   and `RDLUT` differed from the real encoding by **one bit**.
3. **A duplicate key was silently deleting content the file appeared to carry.** `drvl.yaml`'s
   duplicate `timing:` meant the parser handed an agent `{cycles: 2, type: fixed}` and **dropped the
   pin-latency block its sibling `drvh.yaml` delivered** — two instructions of one pair answering
   differently, with nothing in the file to show it.
4. **Code the published set taught that does not work** — the pull-up idiom that floats the pin, the
   streamer `+` composition that silently selects a different mode, and a `WAITMS` ceiling wrong by
   **400×**.

**And it checked its own repair for fresh fabrication**, which is the half that is easy to skip: of
the **42** encodings the repopulation *added*, **38 are verbatim in the source** and the remaining 4
are the `RETIx` aliases, expanded from the alias definitions at `:5483-5486` and **byte-identical to
the per-instruction files**.

**The two defects this delta introduced — both repaired here, not carried** (CLAUDE.md's no-deferring
rule, and the reason this pass touched any YAML at all):

| file | ± at HEAD | what was wrong |
|---|---|---|
| `architecture/interrupts.yaml` | +221/−115 (was +219/−115) | cited `language/pasm2/reti0..3.yaml` — **not a resolvable path**; the four filenames are now written out |
| `hardware/edge-breadboard-carrier.yaml` | +69/−69 (was +66/−69) | cited the 2026-08-25 ledger **at its pre-move path** — the same stale-locator class F-365/F-377 were closing; re-pointed at `archived/`, where item 7 still reads as cited |

*The lack:* **neither was visible to `validate-crossref-keys.py`** — both sit in comment text, which
is F-373's blind spot exactly. Broken reference sites 19 → 18; unresolved ingestion-source citations
**1 → 0 of 368**. The 17 that remain are pre-existing block-D work (task «#335») and the report names
them as out of scope rather than leaving them implied.

**Verdict, quoted because it is the answer to the release question:** *"Strengthened. Not by adding
more, but by removing content that produced plausible, compilable, wrong code… The residual risk
moved from 'the agent is confidently told something false' to 'the agent is told less, and told where
the rest lives.'"*

**Appendix A of that report is written for you.** It reproduces **verbatim** the two `best_practices`
blocks the purge deleted (`io_pin_timing`, `click_module_integration` — F-352's two authored-here
areas, §0.5 item 11) so the deletion can be eyeballed rather than taken on trust.

---

## 1.21 The 2026-09-05 findability pass — the first defect class that is not about correctness

Four commits: `ba24f0f9` (harvester), `d55b6c7f` (index), `19385b66` (the residue + the `+//` merge),
`da896073` (index). **16 files entered the change set, all of them already in the shipped set** — this
pass added *names*, not coverage.

**It started outside the release.** Stephen reported that an agent had failed three or four times
over two days to locate information the KB **has**. Reproduced and measured here, and the measurement
is the finding: **the index harvested four name fields** — `aliases`, `pattern_id`, `instruction`,
`method` — and the operator and special-symbol files name themselves in `operator:` and `symbol:`,
neither of which it read. Nor could the path-derived key carry them: `op_addlteqgt.yaml` becomes
`p2kbSpin2OpOpAddlteqgt`, and the token `+<=>` survives nowhere.

> **0 of 62** pure-symbol Spin2 names were in the index in any form — `:=` `==` `+/` `+//` `<=>`
> `+<=>` `#>` `<#` `@` `@@` `^@` `~` `~~` `??` `..` `? :` and 46 more.
> Against **560 of 560** word-named mnemonics and methods resolving cleanly.

**The defect is confined to symbolic tokens, and those are precisely the tokens an agent meets when
reading or generating Spin2 source.** Evidence was taken live against the published index, not
reasoned: `p2kb_find("+//")` matched nothing and fell back to dumping all 59 categories / 1,129
entries — the undifferentiated-directory response.

**The mechanism was verified *before* the fix was written**, which is why no matcher change was owed:
the alias table already held **161 punctuated keys** and the resolver returned `"resolved_from":
"#32201"` for a bare-symbol query, so punctuation already survived both the index and the query path.

**Pass 2 answered *why* the residue was dark, and the answer is a convention fact, not a data gap.**
The files were not missing names — **the field a file uses follows its subtree's convention rather
than one house style**: `variable:` (CLKFREQ/CLKMODE/VARBASE), `topic:` (Operator Precedence),
`construct:` (Inline PASM2 and ten siblings), `statement:` (DEBUG), `register_name:` (PTRA),
`fundamental:` (three language fundamentals). Nine more fields harvested, **every value read first**.
`fundamental_concept:` was deliberately excluded — it holds multi-paragraph prose, and harvesting it
would put whole essays in the alias table. Thirteen files carried no name anywhere and were given a
hand-authored `aliases:` block.

| | `v1.17.0` | after pass 1 | **HEAD** |
|---|---|---|---|
| pure-symbol names in the index | **0 of 62** | 62 of 62 | **62 of 62** |
| files reachable by an alias | 591 (52.2%) | 916 (80.8%) | **955 (84.3%)** |
| files reachable by neither alias nor category | 452 (39.9%) | 206 (18.2%) | **173 (15.3%)** |
| alias entries | 2,082 | 2,660 | **2,896** |
| aliases lost | — | 0 | **0** |

**All 173 that remain are under `community/`** — 131 OBEX objects and 42 Quick Bytes, which name
themselves one level down and have their own `p2kb_obex_*` route. **Outside `community/`, zero.**

**Two seams worth naming.** The **DEBUG formatters** were the largest single gap: `UDEC`, `SDEC`,
`UHEX`, `SHEX`, `UBIN`, `SBIN`, `FDEC` and their sized variants resolved to nothing, and they are
among the most-typed names in Spin2 work. And `symbols/streamer-symbols.yaml` got the treatment
`spin2-builtin-symbols-complete.yaml` had already had: its **78** `X_*` constants are defined one
level down under `symbol:` keys, so `X_RFBYTE_1P_1DAC1`, `X_IMM_32X1_LUT` and `X_ALT_ON` all resolved
to nothing — while `X_PINS_ON` and `X_WRITE_ON` resolved *only* because `pin-selection.yaml` happens
to list those two by hand. **These constants are what a streamer command word is composed from, and
composing one wrong is silent.** Its `total_symbols` also read **82 against 78 actual records**;
corrected, the same class as the `1224`-vs-136 the symbols file carried.

**F-376's third silent exit-0, closed in the same function.** The harvest ended in
`except Exception: pass`, so a file that could not be parsed **still received a path and a sha256** —
it looked present and was reachable by no name. *The failure removed findability, not the entry*,
which is why swallowing it was the wrong shape. The harvest now returns its reason and the generator
**refuses to emit**. Proven with a negative control: a planted malformed YAML gives exit 1, names the
file and the parser error, and leaves the existing index **byte-identical**.

**F-402 — arming the alias found a conflict, and that is the only content defect this pass produced.**
`+//` suddenly resolved to **two** targets. Reading them found they disagreed: `modulo_add.yaml`
called `+//` an *"Unsigned Modulo Add"* that *"performs addition with unsigned modulo"* — **it
performs no addition**; a leading `+` on a division-family operator selects the UNSIGNED form
(`/` signed divide vs `+/` unsigned; `//` signed remainder vs `+//` unsigned). Its
`related_operators` also **inverted the one distinction the file exists to draw** (giving `//` as
unsigned) and invented `%%`, which is not a Spin2 operator. Corrected against
`complete-spin2-operators.md:62`, `:103`, `:715`.

> **Why it survived every gate, and this is the general lesson.** Every wrap-around idiom in the file
> **adds explicitly and then takes the remainder** — `(tail + 1) +// 32`, `(index + 1) +//
> BUFFER_SIZE`. **The code was right while the prose describing it was wrong.** Nothing an agent
> copied would fail; only what it *believed the operator was* would be wrong. The sourcing gate reads
> quantities, the constant gate reads names, **and neither reads a semantic claim.**

**The merge, decided by Stephen and applied the same day.** `op_addmodulo.yaml` is the definition
home (+156/−3, 13 keys gained, none lost, the ring-buffer patterns and the power-of-2 `&`-mask
comparison folded in). `modulo_add.yaml` is a **32-line redirect rather than a deletion**, because its
key `p2kbSpin2OpModuloAdd` **is in the published `v1.17.0` set** and removing a published key breaks
any consumer that cached it. One definition, two resolvable keys, no conflict — verified in the
emitted index.

**Per-file, this pass:**

| file | ± | new to the change set? | what changed |
|---|---|---|---|
| `language/spin2/operators/op_addmodulo.yaml` | +156/−3 | **yes** | the definition home; folded-in patterns; a real `source:` replacing three unlocatable `references` |
| `language/spin2/symbols/streamer-symbols.yaml` | +104/−1 | **yes** | 78 `X_*` names harvestable; `total_symbols` 82 → 78 |
| `language/spin2/debug-commands/debug-formatters-complete.yaml` | +46/−0 | **yes** | formatter names reachable |
| `language/spin2/operators/modulo_add.yaml` | +32/−129 | **yes** | conflicting definition → redirect |
| `language/spin2/debug-commands/debug-formatters-overview.yaml` | +21/−0 | **yes** | |
| `language/spin2/debug-commands/debug-formatters-hexadecimal.yaml` | +20/−0 | **yes** | |
| `…-binary.yaml` · `…-decimal.yaml` | +19/−0 each | **yes** | |
| `language/spin2/debug-commands/debug-formatters-arrays.yaml` | +18/−0 | **yes** | ⚠️ **incomplete — see §1.23** |
| `architecture/system-registers/complete-system-registers-index.yaml` | +49/−17 | no | |
| `architecture/system-registers/dira-dirb-registers.yaml` | +13/−0 | **yes** | |
| `language/spin2/debug-commands/debug-new-user-guide.yaml` | +13/−0 | **yes** | |
| `language/spin2/integration/spin2-pasm2-integration.yaml` | +12/−0 | **yes** | |
| `language/spin2/spin2-language-complete-map.yaml` | +11/−0 | **yes** | |
| `language/spin2/spin2-language-schema.yaml` | +10/−0 | **yes** | |
| `code-examples/code-example-schema.yaml` | +10/−0 | **yes** | |

**Registers moved:** `F-401` filed (`PENDING-VALIDATION` — the served index is the published one, so
none of this reaches an agent until the set is pushed) · `F-402` filed and now
`PENDING-VALIDATION` · `F-376` half-discharged.

---

## 1.22 The 2026-09-08 boot-ROM pass — a claim with no quantity and no constant in it

Two commits, `2a6df5ef` and `b0057ec1`; **two files**, one of them new to the change set.

**What the shipped file said.** `architecture/boot-rom/boot-rom-contents.yaml` listed **six** ROM
residents — Bootloader, P2 Monitor, TAQOZ, plus `utility_routines`, `character_font_data` (*"Bitmap
font data for terminal output / debug displays"*) and `math_tables` (*"Sin/cos/log tables"*). The last
two carried `verification_status: "Existence confirmed; specifics not yet documented"`.

**What the authority says — one line, and it names three things:**

> `ROM | 16 KB (Bootloader, P2 Monitor debug interface, and TAQOZ (Forth) command interface)`
> — P2 Hardware Manual 2022-11-01, `p2-hardware-manual-text.txt:210`

The same three-item list is what our own extraction matrix recorded from that manual. The P2
Datasheet (`:99`) and the Silicon Doc (`:189`) say only *"16KB boot ROM"* and inventory nothing.

**Existence was not confirmed.** Measured against the ROM assembly listing — the strongest evidence
available, because it **is** the ROM. Re-counted for this ledger:

| term | `ROM_Booter.lst` | `rom_booter_v33_01j.lst` |
|---|---|---|
| `font` · `glyph` · `sine` · `sin_` · `log2` | **0** each | **0** each |
| `TAQOZ` | 48 | 48 |
| `Monitor` + `debugger` | 32 + 9 | 33 + 10 |

The real residents are plainly present, so **the search is not blind** — which is the only thing that
makes the zeros mean anything.

**Where the claim came from, and it is the F-341 shape.**
`sources/rom-booter/rom-booter-narrative.txt:51-56` — *"Beyond the bootloader, the ROM also contains:
Monitor/debugger code, TAQOZ Forth interpreter, Utility routines, Character font data, Math tables
(sin/cos/log)"*. That file was created by commit `9fcf7d84`, **"Complete narrative text generation for
all P2 sources"** — it is **our own generated summary, not a Parallax document**, sitting inside the
documentary truth root and read as an authority.

**Why no instrument could catch it.** The claims **carry no quantities**, so the sourcing gate never
scored them; they **name no constants**, so the fidelity gate never saw them; and the file cites four
real sources in its header, which is exactly what makes a Tier-2 sweep read it as a citing file. This
is the F-402 blind spot again, one step further out: **no gate reads a semantic claim, and a claim
with no number and no constant in it has nothing for any gate to grip.**

**Applied.** The two unsupported residents are removed with the removal recorded in place, so the
narrative cannot quietly reintroduce them, and the authoritative content line is now carried in the
file. `utility_routines` is **retained but reclassified**: the listing does contain called
subroutines, which is an observation about the code, not a documented ROM component, and it now says
so instead of standing as a fifth resident with a source line.

**Deliberately NOT asserted:** that font data and math tables are *absent*. A 16 KB mask ROM can hold
unlabelled blocks no symbol name would reveal. What is established is that **no source we hold
supports them and the one authoritative content list omits them**, so the KB must not state them. If
it ever matters, that is a question for Chip Gracey, **not a gap to research** (§0.5 item 25).

**The sweep half, and the ordering lesson.** `2a6df5ef`'s commit body ends *"Class sweep run: no other
shipped file makes a font-data or math-table ROM claim."* **It was written before the sweep's output
was read, and it was wrong.** `b0057ec1` found two more instances of the same fabricated list **in the
same directory** — `boot-rom/_index.yaml` stated six residents in its `description:` sentence *and
again* in the `contains:` line under `boot-rom-contents`. Both corrected. The sweep's other two hits
were read and correctly left alone: `hardware/p1_rom_font_character_set.yaml` documents the **P1's**
ROM font (real, different chip) and `assembly-directives/file.yaml` shows a `FILE` directive
including a font file from *user* code.

> **Two consequences.** *A class-sweep claim written before its output is read is an assertion, not a
> measurement* — the F-396 shape in a different key. And **the second site was the sibling
> `_index.yaml` of the very directory being corrected**: an index file restates its members' claims,
> so a finding that removes a claim must sweep that file's index in the same pass.

| file | ± | new to the change set? | verdict |
|---|---|---|---|
| `architecture/boot-rom/boot-rom-contents.yaml` | +33/−26 | **yes** | **corrected** — six residents → three, plus the authoritative content line |
| `architecture/boot-rom/_index.yaml` | +23/−18 (was +18/−15) | no | **corrected** — the same claim, twice, in the directory index |

**Registers moved:** `F-403` filed, both halves applied, now `PENDING-VALIDATION`.

---

## 1.23 The 2026-09-09 re-derivation — what re-deriving the ledger itself found

**Re-deriving a document is an instrument**, and this run of it returned three defects. None was
found by reading the tree looking for defects; each fell out of checking a number this document
asserts.

**1. The release validator was RED, and had been for four days (F-405).** `validate-dod-release.py`
exited **1** at `b0057ec1` — *Gzip Compression: FAIL*. The 2026-09-05 pass regenerated
`p2kb-index.json` twice and `p2kb-index.json.gz` neither time. **This is F-357's exact defect,
recurring while F-357 reads `RESOLVED`.** The index was *separately* stale by the two files §1.22
changed. Both repaired here; §0.4 carries the diagnosis. **The generalisable form:** *a defect closed
by a one-time repair, with no gate wired to the release path, is a defect scheduled to come back.*

**2. Three register entries were lagging the artifact.** Each is the "annotate as you fix, in the same
pass" rule failing in the same session that made the fix:

| entry | what it said | what the tree said |
|---|---|---|
| **F-402** | `PARTIAL` — *"two files still define one operator … the call is Stephen's"* | He made the call and **the merge landed the same day** (`19385b66`). `op_addmodulo.yaml` is the home; `modulo_add.yaml` is a redirect. Re-graded `PENDING-VALIDATION`. |
| **F-401** | a one-column result table: dark **206**, aliases **2,660** | Those are **pass 1**. Pass 2 (`19385b66`/`da896073`) took it to **173 / 2,896** and was never written back. Table re-derived and both passes recorded. |
| *(and)* **F-403** | `CONFIRMED`, with its own body reading *"Correction applied 2026-09-08"* | Fully applied, unpublished → `PENDING-VALIDATION`. The `_index.yaml` half was not recorded at all. |

**A status line is not evidence, and it lies in both directions** — F-402 under-reported progress,
F-403 over-reported openness. The artifact settles it.

**3. A new finding, filed and fixed: F-404 — 24 of 54 DEBUG formatter names resolve to nothing.**
Found by *verifying* §1.21's own claim rather than restating it. `debug-formatters-arrays.yaml`
defines the array formatters **by composition** — `formatters` × `array_types` — and **a composition
rule is not a string**, so no field holds the literal token and the harvester has nothing to read.

> Measured against the emitted index at HEAD — the *published* index is `v1.17.0`'s and cannot answer
> this: of the **54** formatter names the Spin2 v55 reference lists in its formatter tables,
> **30 resolved and 24 did not** — every one of them a `<fmt>_{REG,BYTE,WORD,LONG}_ARRAY` form.
> **`UHEX_LONG_ARRAY` is among them** — and it is the *only* trusted packed-data feed shape for a
> scrolling LOGIC or SCOPE window (F-207). The one name an agent most needs when a scrolling window
> renders empty resolved to nothing.

All 24 were transcribed from the v55 formatter tables and **read at their lines** (`:943`,
`:951-954`, `:960-963`, `:969-972`, `:978-981`, `:987-990`, `:996-999`) and added to the file's
`aliases:` block. **`FDEC` has `_REG_ARRAY` and `_ARRAY` forms only** — no `FDEC_BYTE_ARRAY` appears
in the reference, and none was invented to make the cross-product tidy. They are **lookup keys for a
rule the file already documents**; nothing new is claimed, and an alias is never a definition.

*The lack, and it is F-401's lack one level in:* **no gate in this project asks whether a file can be
found.** Every one asks whether it is right. A name that exists in no field is invisible to all of
them, because there is nothing to read.

| file | ± | verdict |
|---|---|---|
| `language/spin2/debug-commands/debug-formatters-arrays.yaml` | +18/−0 → **+61/−0** | **stronger** — 24 sourced formatter names now resolve |

**Measured in the emitted index after the repair, not asserted:**

| | at `b0057ec1` | **after** |
|---|---|---|
| v55 formatter names resolving | **30 of 54** | **54 of 54** |
| `UHEX_LONG_ARRAY` in the index alias table | absent | `["p2kbSpin2DbgDebugFormattersArrays"]` |
| alias entries | 2,896 | **2,920** |
| files reachable by an alias · dark | 955 · 173 | 955 · 173 *(unchanged — the file was already reachable; this repair adds names, not files)* |
| `validate-dod-release.py` | **exit 1** | **exit 0, 11 of 11 PASS** |

*(Every other findability figure in this document — §0.4, §0.5 item 24, §1.21 — is stated at
`b0057ec1`, which is the derivation baseline. Only the alias-entry count moves, 2,896 → 2,920, and it
moves here rather than being back-filled silently into the tables above.)*

---

## 1.24 The 2026-09-09 terminology review — the class where the KB is right and the reader is worse off

Four content commits, five files, **all five already in the change set**. This pass produced no new
coverage and corrected no fact. It fixed something none of the other passes were looking for: places
where the KB is **correct, cited, gate-green — and the reader who asks the question is worse off than
before.**

**How it started.** Reading this ledger, Stephen asked: *"our spin2 language has pull up and pull down
named constants… how are these handled in our .yaml files?"* — and then, when the first answer was a
lecture about naming rather than an answer: *"Are those constants defined in the YAML? Are they
described in how they can be used, and do we have examples showing which instructions they get used
in? Yes or no? They need to be. If we took them out of the YAML, we broke the YAML."*

**The answer was yes, yes, yes — and coverage had grown, not shrunk.**

| | `v1.17.0` | HEAD |
|---|---|---|
| distinct `P_HIGH_*`/`P_LOW_*` names | 16 | 16 |
| occurrences in the shipped set | 73 | **153** |
| files carrying them | 11 | **13** |

All 16 encodings re-checked against the v55 table and correct; each record carries `value`,
`bit_pattern`, `description`, `usage_context`, `hardware_relationship`, `related_symbols`; 16 files
show them in working `WRPIN`/`PINSTART`/`DRVH`/`DRVL` examples. The only `P_*` names this release
deleted are `P_LEVEL_B` and `P_SCHMITT_B`, and `pnut-ts` rejects both as undefined while accepting
`P_LEVEL_A`/`P_SCHMITT_A`.

**But two things were wrong, and neither is a fact (F-406).**

1. **Retrieval.** Of **17** phrasings a coder types for this concept, **2 resolved** — `pull-up` and
   `pull-down`, hyphenated singular. `pullup`, `pull up`, `weak pull-up`, `pull-up resistor`,
   `bias resistor`, `P_PULLUP` and eleven more returned the category dump. **Now 17 of 17.**
2. **Framing.** Both `basic-io.yaml` files opened with *"The P2 has no internal pull-up/pull-down
   resistor network"* and delivered the answer **fourth**, under `substitute_for_a_pull_up`.

**And the substantive point was Stephen's, not the KB's.** `P_HIGH_15K` with `DIR=1, OUT=1` is a
15 kΩ resistive path to VIO — **in the reader's circuit that is a pull-up.** The **Silicon Doc uses
that vocabulary for these same rungs**: `:4599`, USB mode, *"two 15k pull-downs for 'host' or a 1.5k
pull-up and a float for 'device'"*. The KB had been policing a word its own authority uses. The one
real difference — the pull is a property of **driving**, so DIR must stay high — is unchanged and now
stated first, because it is the part that breaks code.

Reframed accordingly: `yes_you_can_pull_a_line_high_or_low` leads, the DIR caveat follows, and
`how_the_p2_does_it` carries the no-dedicated-bias-network fact as the *reason* for the caveat rather
than as a refusal. `substitute_for_a_pull_up`/`_down` → `pull_a_line_high`/`_low`. **None of the
renamed keys is in the published `v1.17.0` set**, so the rename cost no consumer anything — and this
was the last moment it was free. The published parent `internal_pull_resistors` is unchanged.

**Then the audit he actually asked for: does anything else in the change set have this shape?**
All 112 files as the set then stood, all 41 removed top-level keys, a denial-shaped-key sweep, and
retrieval probes per removed topic. **One instance (F-407), and three findings of "this is the pattern, keep it":**

| | verdict |
|---|---|
| `io_pin_timing.yaml`'s *"What it deliberately does NOT carry, and where those live instead"* | **the model.** Drive strength → forwarded; slew rate → *"There is none to document"* with zero-hit evidence; propagation/rise/fall → *"No Parallax source states them"* |
| F-390's `-1` correction | **exemplary.** A coder with `-1` learns it arrives as `$FFFF_FFFF`, decodes `D[5:0]=%111111` and **launches an even/odd cog pair** — cited, and confirmed against emitted bytecode |
| the `no_*` / `not_*` keys (11 of them) | **scoping, not denial.** Each says where the answer lives or that no source states it |
| `hardware/` `specifications`/`power_*` removals (24 keys) | forward only via each file's source citation — recoverable, weaker than the `io_pin_timing` pattern. **Noted, not a defect** |

**The one instance — F-407, and it is the same shape one level worse.** The purge removed
`io_pin_timing.yaml`'s `input_characteristics` block and was **right** to: `VIL_max 0.8 V`,
`VIH_min 2.0 V`, a `~1.5 V` threshold, Schmitt thresholds `1.65 V`/`1.35 V`, `~300 mV` hysteresis —
no Parallax source states any of it. **But nothing replaced it**, and the real table was in a source
the same file already cites. The P2 Datasheet's **DC Characteristics**, p.47-48:

| Symbol | Parameter | Value | Line |
|---|---|---|---|
| `Vih` | Input Logic Threshold | min `Vxxyy*0.3` · typ `*0.5` · max `*0.7` | `:2163` |
| `Iil` | Input Leakage Current | ±0.1 µA typ · ±10 µA max | `:2165` |
| `Vol` | Output Low (vs GND) | 15 / 160 / 510 mV at 1 / 10 / 30 mA | `:2172-2174` |
| `Voh` | Output High (vs Vxxyy) | −6 / −170 / −580 mV at 1 / 10 / 30 mA | `:2176-2178` |
| `Vdd` · `Vxxyy` | Supply ranges | 1.7/1.8/1.9 V · 3.15/3.3/3.45 V | `:2159`, `:2161` |

**The threshold row's *shape* is what the fabrication got wrong.** The datasheet states **one**
threshold as a **fraction of the I/O supply**, not a VIL/VIH pair in fixed volts — 0.99 / 1.65 /
2.31 V at 3.3 V, and it **moves with `Vxxyy`**, so two pin groups on different supplies do not share
thresholds. The removed `0.8 V / 2.0 V` pair reads as generic 5 V TTL numbers; it cannot be derived
from this table.

**`Vol`/`Voh` stop at 30 mA**, agreeing with the `±30 mA` absolute maximum already in the file.
**That is the table that made the shipped `150 mA` claim impossible** — it was in the datasheet all
along, on the page after the one we were already citing.

**One claim verified rather than asserted while writing it:** the file says no source states
propagation, rise or fall figures. The **AC Characteristics** table on the facing page
(`:2188-2210`) is oscillator frequency and XI/XO capacitance **only**. The claim stands. Its PLL row
(3.33 / 180 / 320 MHz) is the same ceiling **F-378** corrected the clock files to.

**Why no instrument could catch F-407, and this is the lesson of the pass.** Every gate scores what is
**present** — quantities, constants, references. **A question the KB does not answer at all is
invisible to all of them.** This file passed all eight gates cleanly while carrying no answer where a
fabricated one had been removed. *Removal under cite-or-omit is only half a repair; the other half is
a forwarding address or the real figure, and nothing measures whether it was written.*

| file | ± | verdict |
|---|---|---|
| `architecture/io_pin_timing.yaml` | +29/−14 → **+162/−270** | **stronger** — the DC Characteristics table, transcribed and line-verified |
| `architecture/pin-drive-configuration.yaml` | +277/−0 → **+305/−0** | **stronger** — 18 pull-vocabulary aliases; 2 of 17 → 17 of 17 |
| `language/spin2/concepts/basic-io.yaml` | +89/−121 → **+104/−121** | **stronger** — answer-first reframe |
| `language/pasm2/concepts/basic-io.yaml` | +96/−121 → **+111/−121** | **stronger** — same |
| `language/spin2/debug-commands/debug-formatters-arrays.yaml` | +18/−0 → **+61/−0** | **stronger** — F-404, §1.23 |

**Registers moved:** `F-406` and `F-407` filed, both `PENDING-VALIDATION`; next finding ID `F-408`.
Register at **131 live · 294 archived · 0 unaccounted**.

---

## 1.25 The 2026-09-09 reference sweep — 43 dangling links, none deleted

Two commits, `d757adde` and `0f8274f5`. **Six files entered the change set** — the first to do so
since `9ab0433b`, and all six were already in the shipped set.

**Why it happened now.** Stephen asked whether anything stood in the way of releasing. This did:
task «#335» had been carrying "35 broken `see_also` values" since 2026-08-29, and a re-measurement
found **43** — a number the task could not have had, because six of them were introduced or exposed
after it was written.

**The measurement, before and after, over `see_also` · `references` · `related_concepts`:**

| | before | after |
|---|---|---|
| file references that resolve | 123 | **159** |
| directory references that resolve | 0 counted | **7** |
| **broken** | **18** | **0** |
| **`deliverables/ai/P2/`-prefixed** (unresolvable as written) | **22** | **0** |
| **globs** | **3** | **0** |

**Sacred Rule 7 governed every one: not a single reference was deleted.** Each was redirected to
where the concept *is* documented, and where the old target was a *scheme* rather than a file, the
retirement is recorded in place so the next reader is not left guessing why a link moved.

| shape | n | what was done |
|---|---|---|
| **wrong base** | 8 | `cogspin` → `language/pasm2/concepts/multi_cog_synchronization.yaml`; `pinstart` → `language/spin2/constructs/inline_pasm.yaml`; `streamer-symbols` + `xcont` → four `architecture/streamer/` files whose `../../` form resolved to nothing; `labels.yaml` → `language/pasm2/{jmp,call,djnz,rep}.yaml` |
| **target never existed** | 4 | `language/spin2/methods/_index.yaml` → `language/spin2/methods/wrpin.yaml` |
| **retired scheme** | 2 | `manifests/P2/language/*-manifest.yaml` → the Spin2 language map · the PASM2 `groups/` tree |
| **prose-prefixed** | 2 | `pin-power-domains.yaml` — path becomes the value, prose becomes a comment |
| **glob** | 3 | `architecture/smart-pins/*.yaml` → `architecture/smart_pins.yaml` |
| **root-prefixed** | 22 | prefix stripped, 5 files |

**Three of these are worth carrying as shapes, not counts.**

- **`call.yaml` was ambiguous.** Two files answer to that basename — `language/pasm2/call.yaml` and
  `language/spin2/methods/call.yaml`. This is the **`complete-tables-reference.md` trap F-399
  closed**, in a second key: a bare basename that a human resolves from context and a tool resolves
  by guessing. `labels.yaml` is a PASM2 file, so PASM2 is right — but the fix is the **full path**,
  not the reasoning.
- **`pinstart` pointed at a redirect stub.** `concepts/inline_pasm2.yaml` exists, so the reference
  was not "broken" in the crude sense — it just resolved to a file whose entire content is *"Canonical
  entry redirected to `constructs/inline_pasm.yaml`."* Sacred Rule 7 says point at where the content
  **is**, so the hop is now gone.
- **The 22 root-prefixed were never dangling**, which is exactly why they survived. Every one
  resolves to a real file *after* stripping. They were unresolvable **as written**: a consumer that
  prepends the KB root gets `deliverables/ai/P2/deliverables/ai/P2/…`. A reference can be wrong
  without being missing, and only the consumer's resolution rule can tell you which.

**Also fixed, task «#338» item 1.** `p2an001`'s clock gotcha quotes the PLL system clock — 3.33 /
180 / 320 MHz with the *"180 MHz at up to 105 °C"* footnote — and cited
`p2-datasheet-text.txt:2199`. **That line is the crystal row** (1 / – / 50 MHz). The PLL row is
`:2200`, its footnote `:2209`; both read at the line. **F-377's shape, one table row over** — a
locator in range, landing on a neighbouring row that still reads like a plausible source, which is
the defect class §1.19's "wrapped table row" named.

⚠️ **What this does NOT close, and it is why F-373 moved to `PARTIAL` rather than `RESOLVED`.**
All three fields are still typed `'text'` in `validate-crossref-keys.py`, so **the gate could not see
any of this**: green before the sweep, green after it, and green again tomorrow if a broken path is
reintroduced. **The repair is content-only and nothing defends it.** That is F-360's unwired
duplicate-key gate and F-405's unrun validator in a third key — *a defect closed by a one-time
repair, with no gate wired to the release path, is a defect scheduled to come back.* The gate half
belongs with the wiring work in task «#339».

**Punch-listed, deliberately not done:** authoring `language/spin2/methods/_index.yaml`, the
101-method catalog the four board files were reaching for. Stephen: *"punch list B so we can come
back to it later. We may or may not do it."* Recorded in
`engineering/document-production/PUNCH-LIST.md` with what it would cost and why it might not be
worth it — including the warning that `spin2-language-complete-map.yaml` is a **coverage report**,
not an index, and must not be repurposed as one.

---

# PART 2 — By region → file

**92 files, each carrying its differential-read verdict.** Regions are ordered by their **rowed** file
count, so related corrections sit together; **each region header carries its HEAD file count**, which
is why the headers sum to 118 while the rows number 92 — and why `language/spin2` (33 at HEAD) sits
second behind `hardware` (28) rather than first. The other twenty are the
files that entered the change set after the differential read was written, and each is carried where
its pass is described: **4 in §1.19 · 15 in §1.21 · 1 in §1.22 · 6 in §1.25.** *(92 + 4 + 15 + 1 + 6 = 118.)* Nothing
is omitted; the split is by where the reader will find the reasoning, not by importance.

**The verdicts** (`2026-08-26-yaml-differential-read.md` §0.1): **stronger** — what was removed was
replaced by better-sourced content. **equal** — reworded or restructured, same substance.
**thinner-but-honest** — removed because unsourced, wrong, or deliberately out of scope; its absence
is *correct*. **gutted** — removed content the KB **needs** *and* that a source we hold **can
support**; both halves required. **new file** — nothing could have been removed from it.

**Tally over the 92 rows: 78 stronger · 6 equal · 1 gutted-then-restored · 4 new file · 3 corrected
(§1.19) = 92.** Zero files are `thinner-but-honest` at *file* level; that verdict lives at block level
(§1.3). The four `language/pasm2` files added after the differential read was written are verdicted
here, from `b466a538`'s diff.

**The twenty files carried in their pass sections do not have differential-read verdicts, and that is
correct rather than missing.** The read compared `v1.17.0` against `4caeb6cc`; a file that entered the
change set afterwards was never in its population. Their verdicts are stated where their changes are
described — **corrected** for the six that had content wrong (`hub.yaml`,
`p2-hardware-selection-guide.yaml`, `cogspin.yaml`, `coginit.yaml`, `boot-rom-contents.yaml`,
`modulo_add.yaml`) and **stronger** for the fourteen that gained names or a definition home.

`GONE` = top-level keys present at `v1.17.0` and absent at HEAD **plus** leaf-fact candidates whose
value string appears nowhere in the shipped KB, as measured by the differential read. It
over-reports — a reworded fact counts as gone — and is a *reading list*, not a loss figure.

---

## `hardware/` — 28 files · 25 stronger · 2 new · 1 corrected (`p2-hardware-selection-guide.yaml`, §1.19)

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `edge-32mb-module.yaml` | +223/−417 | 224 | stronger | Pin map, boot table, 8 µs CS limit, PSRAM banks all returned cited; P58-P61 anchored to the **boot-ROM listing** rather than the eval guide, which the errata register records as reversing the directions. Fabricated `alternate_part: 64000-ES` removed **with a note saying why**. E-010's "enable a pin pull-up" removed (`75971308`). |
| `edge-standard-module.yaml` | +172/−335 | 176 | stronger | `pin_mapping` returned cited with an explicit *"LEDs are P56/P57, NOT P38/P39"* warning; boot-mode table records that two rows are the same switch setting, disambiguated by card presence, stated as the source states it. E-010 removed. |
| `p2-hardware-feature-comparison.yaml` | +244/−121 | 104 | stronger | **`#64006G` re-identified as the Goertzel board**, not a Digital I/O board; invented carrier part numbers replaced with real ones; a carrier dimension off by a factor corrected. `75971308` then removed the `digital_io_board` slug from two guidance lists and found two more slugs naming no board. |
| `addon-motor-driver.yaml` | +116/−67 | 62 | stronger | All 16 pin offsets, the PWM interlock, 250 ns deadtime and 150 mV/A returned cited; a guide self-contradiction resolved and filed as errata — **our own extraction audit blamed docling and was wrong**: plain `pdftotext` carries the same duplication, so it is in the PDF and no re-extraction would fix it. |
| `hub75_adapter.yaml` | +100/−93 | 58 | stronger | Manufacturer's **70 MHz** replaces the unsourced 40/35 MHz; three explicit `gap_*` keys record what was removed and what would settle it. Its `source:` keys point at loose files at the ingestion root (F-341's shape) — defensible on authority, anomalous in location. |
| `p2-eval-board.yaml` | +95/−49 | 36 | stronger | Rev D→Rev C, 320→180 MHz recommended, real flash part, 3.55 in; ~10 `TBD` placeholders replaced with sourced values. F-328(b)'s fabrication class drained. |
| `addon-wx-wifi.yaml` | +61/−30 | 33 | stronger | `pin_descriptions` returned as a full table with SIP/DIP numbers; `part_variants` → cited `form_factors` with the `#32420S`/`#32420D` split (`599d3660`). |
| `addon-serial-host.yaml` | +61/−106 | 62 | stronger | Enables at offsets 1/5, D-/D+ pairs and the enable sequence returned cited; new Spin2 `code_patterns`. **Identity string restored** (`e9dc9507`) with 500 mA continuous per socket rather than the summed "up to 1A" nobody sourced. |
| `addon-hyperram-hyperflash.yaml` | +60/−23 | 10 | stronger | `configuration`/`specifications` returned cited; the RES shunt now stated as a **driver requirement**. |
| `addon-hd-audio.yaml` | +59/−49 | 22 | stronger | `dac_board` returned with the four `P_DAC_*` constants and the parallel-pin impedance rule. |
| `addon-rtc.yaml` | +58/−33 | 15 | stronger | **E-004 closed** — the guide's "150 kΩ pull-up" mislabel restated as a P2 drive-strength mechanism with DIR high, quoting the guide under a key that says not to copy it; PCF8523 map + `$68` added. Fixing it surfaced a second mismatch the finding never named: the guide also prescribes a 3.3 kΩ pull-up, and the P2 ladder has **no 3.3 k rung at all**. |
| `addon-control-board.yaml` | +55/−38 | 7 | stronger | Description/signal map returned cited; the `P_LOW_15K` read idiom **corrected** to require DIR high. Three inferences removed because the guide states 470 Ω and nothing else — no LED current, no forward drop, no debounce interval, so neither do we. |
| `programming-prop-plug.yaml` | +51/−28 | 12 | stronger | 3 Mbaud ceiling, DTR/RTS reset selection, ~20 µs pulse returned cited; new `header_pinout`. |
| `edge-mini-breakout.yaml` | +39/−48 | 30 | stronger | Fabricated "USB connector onboard" removed; cited `connectivity` gives the real P0-P31 + P56-P63. |
| `addon-mini-prototyping.yaml` | +32/−4 | 2 | stronger | Description, power rails and grid retained and cited. |
| `edge-standard-breakout.yaml` | +29/−45 | 27 | stronger | Same fabrication removed; cited `connectivity` adds the eight 2×6 headers. |
| `addon-serial-device.yaml` | +28/−63 | 26 | stronger | LEDs at 0/1/6/7 and D-/D+ at 2/3, 4/5 returned cited; new even/odd smart-pin pairing note. |
| `hardware-compatibility-matrix.yaml` | +27/−2 | 2 | stronger | False *"all add-ons use P0-P7"* replaced by the correct single/dual-header model (`ccddcbe6`). |
| `addon-goertzel-touch.yaml` | +25/−14 | 7 | stronger | `specifications` returned cited plus a board-revision note. |
| `addon-digital-video-out.yaml` | +21/−2 | 2 | stronger | Same facts, reworded with a citation; ACC-5V bridge retained. |
| `addon-wx-adapter.yaml` | +18/−0 | 0 | stronger | Insertions only — citation + `sole_p2_wx_adapter` disambiguation (`599d3660`). |
| `addon-led-matrix.yaml` | +14/−2 | 2 | stronger | Charlieplex rule and ~4 mA retained; description now cited. |
| `addon-microsd.yaml` | +7/−0 | 0 | stronger | Insertions only — `power_signals` gained a citation. |
| `edge-breadboard-carrier.yaml` | +66/−69 | 43 | stronger | Wrong "6-9 V" and a non-existent on-board USB-to-serial gone; **5 VDC / 5.5 V max restored cited** and the `educational_value` duplicate key resolved (`e9dc9507`). |
| `addon-av-breakout.yaml` | +70/−44 | 0 | stronger | `signal_map` restructured, guide citation + per-board capture added. |
| `addon-click-adapter.yaml` | **+195/−0** | — | *new file* | `#64008` from the schematic — the first source here where no text-extraction path works at all. §1.11. Three inference-as-reading claims self-audited and labelled (`601e65ce`). |
| `p2-package-mechanical.yaml` | **+102/−0** | — | *new file* | CASE 932BR, 15 rows, footprint, 12 aliases. **G-021 closes.** §1.11. |

## `architecture/` (top level) — 15 files · 13 stronger · 1 new · 1 corrected (`hub.yaml`, §1.19)

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `interrupts.yaml` | +219/−115 | 78 | stronger | 🔴 **The worst correction in the range**: IJMP3/IJMP1 were **inverted** — anyone generating interrupt code got the wrong vector addresses for levels 1 and 3. The `shadow_registers` model is disproven; there are no shadow banks, only `CALLD IRETx,IJMPx WCZ`. A summary paragraph still contradicting that was repaired by `4caeb6cc`. §1.6, §1.13. |
| `debug_interrupt.yaml` | +208/−92 | 64 | stronger | Three invented configuration registers and the fabricated `NIXINT0`/`TRGINT0` removed; real `BRK`/`COGBRK`/`GETBRK` encodings substituted. Two of the eight non-derivable claims live here (§0.5 item 1). |
| `smart_pins.yaml` | +173/−21 | 13 | stronger | `%AAAA`/`%BBBB`/`%FFF` selectors given full bit ranges and cited; the four global filter defaults now carry length, tap **and** the source's own arithmetic. Gained the **IN rule** with its consequence stated (`ad4f974f`) and F-369's 126-bit state mechanism (`36196329`). |
| `clock_system.yaml` | +185/−136 | 85 | stronger | Rebuilt from v55's own "Clock Setup" closed set with `%CC_SS` per row; PLL fields, `%CC`/`%SS` tables and the datasheet's worked 148.5 MHz sequence all cited. **`pll_lock: ~10 microseconds` was wrong — three Parallax sources say 10 ms.** Its `part3-interrupts.txt:520` locator landed on a blank line and is now `:521` (§1.19). |
| `lookup_ram.yaml` | +152/−99 | 47 | stronger | Fabricated `RDLUTS` deleted; **LUT sharing direction corrected** and `WRLUT`'s operand order fixed. The orphaned block that had been overwriting **SETLUTS** removed (`e9dc9507`). Three of the eight non-derivable claims live here. |
| `cog_attention.yaml` | +124/−49 | 36 | stronger | Fabricated `RDCOGID` deleted; **ATN corrected from event 15 to event 14**; encodings replaced with the real ones; `setup_for_event` no longer configures SETSE1 for attention, which SETSEn cannot select at all. |
| `event_system.yaml` | +109/−55 | 52 | stronger | The whole 16-event catalogue restored verbatim and cited; the `SETSE` restriction (pin/LUT/lock only) added. |
| `click_module_integration.yaml` | +70/−33 | 20 | stronger | `documentation_source` went `code_analysis` → `schematic_primary`; **all twelve CLICK_OFST values confirmed against the #64008 sheet with zero corrections** — they had been derived from the P2-Click-eInk driver and every one was exactly right. Gained `uart_direction_caveat` and `header_span`. Its removed `best_practices` is authored-here with no upstream — **F-352, open**. |
| `locks.yaml` | +89/−53 | 26 | stronger | The invented `LOCKTRY` "query" form — which actually **acquires** — removed; real encodings substituted. One non-derivable claim (`state_bits: 4`) stands here. |
| `pin-power-domains.yaml` | +35/−19 | 8 | stronger | The two-layer distinction rebuilt with sources — silicon 16 groups of 4, Edge board 8 LDOs of 8 — plus *why* a ratiometric measurement must stay within four. |
| `io_pin_timing.yaml` | +18/−256 | 146 | stronger | The F-327 fabrication family — a milliamp drive ladder, programmable slew, and a propagation/rise/fall model built on both — removed; cited absolute-maximum ratings, the protection-diode mechanism and the 5 V series-resistor technique added. The `part3-pins.txt` fabricated header and the residual `~1-2ns` were both removed by §1.18; its four replacement locators were re-read in the §1.19 sweep. |
| `serial_loader.yaml` | +14/−15 | 10 | stronger | All boot facts returned quoted from source, plus P62's open-drain behaviour under a non-zero INA/INB mask. |
| `smart_pin_patterns.yaml` | +5/−7 | 7 | stronger | Generic unsourced notes replaced by verbatim cited statements; the timing cross-reference kept **and** promoted into `related:`. |
| `pin-drive-configuration.yaml` | **+277/−0** | — | *new file* | Eight real rungs, cited, expressed by encoding. §1.5. Its duplicate `note:` — which silently discarded the sprint's own central corrective sentence — was found and fixed by `43061dad`. |

## `language/spin2/` — **33 files at HEAD**, 15 rowed here · 14 stronger · 1 equal · 2 corrected (`methods/cogspin.yaml`, `methods/coginit.yaml`, §1.19) · **13 more in §1.21** (the findability pass: the seven DEBUG-formatter pages, `spin2-pasm2-integration`, both `+//` operator files, both language-map/schema files, `streamer-symbols`) · **3 more in §1.25** (`methods/pinstart`, `methods/wxpin`, `methods/wypin`)

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `concepts/timing_operations.yaml` | +31/−12 | 2 | stronger | **§1.18.** System counter corrected from 32-bit to **64-bit** (`silicon-doc-text.txt:55`, "GETCT WC retrieves upper 32-bits"), with the rollover discussion scoped to the 32-bit value GETCT returns alone. The 500 MHz rollover row → 320 MHz, recomputed. The 2 GONE are the unsourced `min_practical` column and "Spin2 interpreter overhead adds several microseconds" — **no source states either**. Six blocks gained `derived_from:`/`source:`; those blocks were always uncited and were invisible until the file gained its first citation (F-381). |
| `constants/special-configuration-symbols.yaml` | +17/−3 | 0 | stronger | **§1.18.** `_CLKFREQ`, `_XINFREQ` and `_XTLFREQ` ranges labelled as **pnut-ts acceptance ranges**, each with the P2 Datasheet's rating beside it (320 / 200 / 50 MHz) — the compiler accepts 180, 300 and 10 MHz beyond them respectively. Four further blocks cited to the compiler guide's own rules 1-5 and to `spin2-v55-text.txt:1018`/`:1027`. |
| `system-variables/clkmode.yaml` | +3/−2 | 0 | stronger | **§1.18.** PLL `use_case` no longer says "up to 500 MHz"; states the datasheet's 320 MHz max and 180 MHz typical plus the 350 MHz `VCO / 1` overclock ceiling. `bit_fields` and the PLL-lock `~10 ms` note cited (`silicon-doc-text.txt:2621`, `:2687`, `:2635`). |
| `symbols/spin2-builtin-symbols-complete.yaml` | +1052/−23 | 20 | stronger | 874 → 1937 leaves carrying v55's own wording; **all 116 v55 constants defined exactly once**, plus a top-level `aliases:` block of 116 names that makes them reachable at all. The 20 GONE are 3 corrected counts, 13 rewordings and **4 fabricated symbol names** — zero real losses. The `1224` record count corrected to 136 with its provenance (`e9dc9507`). |
| `concepts/basic-io.yaml` | +89/−121 | 59 | stronger | Source-first rebuild; three disproven blocks deleted incl. `max_current_per_pin: 150mA` — **five times the datasheet's ±30 mA absolute maximum**, in the exact number used to size an LED resistor. |
| `methods/getct.yaml` | +45/−25 | 4 | stronger | Derived figures replaced by cited v55 + datasheet statements. Its `description` was purged and not returned for a while; **restored by `75971308`**, quoted rather than derived. |
| `debug-commands/pc_key.yaml` | +32/−11 | 5 | stronger | Every removed rule restated from v55; one new rule added (hub `@key` vs cog `#key`). |
| `methods/wrpin.yaml` | +22/−20 | 26 | stronger | All 26 are **de-duplication**; every one of the 13 mode constants and all four `P_TT_*` verified present exactly once in the definition home. |
| `debug-displays/logic.yaml` | +22/−0 | 0 | stronger | Pure addition — the capture-vs-display split, a `pin-capture.yaml` cross-reference and a cited worked example. |
| `methods/waitus.yaml` | +21/−16 | 15 | stronger | The wrong 1–4,294,967 ms ceiling replaced by v55's `$8000_0000`-clock bound plus a `ceiling_formula`. Removals are quality commentary — `thinner-but-honest` at block level under the KB entry rule. |
| `methods/waitms.yaml` | +17/−11 | 10 | stronger | Same correction. Its `notes:`/`limitations:` went list→dict where every sibling keeps them as lists (§1.16). |
| `conventions/johnny-mac-documentation-style.yaml` | +13/−10 | 1 | stronger | Inline example corrected: `P_HIGH_150K "150K pullup resistor"` → `P_HIGH_15K` + `drvh`. Compiles. |
| `conventions/spin2-docs-jonnymac.yaml` | +13/−10 | 1 | stronger | Same correction, uppercase variant. |
| `methods/pinfloat.yaml` | +3/−1 | 1 | stronger | "external" added one line above where it was already right, plus a note that a `P_HIGH_*` selection goes inactive when the pin floats. §1.13. |
| `methods/cogstop.yaml` | +1/−1 | 1 | equal | One word: "pull-up/down resistors" → "**external** pull-up/down resistors". |

## `language/pasm2/` — **15 files at HEAD**, 12 rowed here · 12 stronger · **3 more in §1.25** (`concepts/labels`, `concepts/cog_hub_execution`, `xcont`)

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `concepts/basic-io.yaml` | +96/−121 | 62 | stronger | Byte-twin of the Spin2 file; same disproven blocks removed, and the `Set DIR before OUT` glitch rule was **backwards** and is now corrected. |
| `setxfrq.yaml` | +22/−12 | 3 | stronger | All four SETXFRQ words retained; the block now carries the source rule and per-value arithmetic. ⚠️ **Two of the four values contradict the rounding rule the block itself cites** — §0.5 item 13. |
| `wrpin.yaml` | +22/−6 | 6 | stronger | Six drifted one-line restatements de-duplicated to `architecture/smart_pins.yaml`, verified to carry all six with bit ranges. |
| `getbrk.yaml` | +16/−4 | 3 | stronger | `flags_affected: C/Z: No effect` was **wrong** for an instruction that requires a flag effect; replaced with cited per-flag behaviour and the WZ polarity corrected (**F-368**). |
| `subsx.yaml` | +8/−2 | 0 | stronger | The manual's `Result[31]` prose replaced with the true-sign form its own Table 169 gives, naming E-016. §1.13. |
| `drvh.yaml` | +7/−0 | 0 | stronger | Citation added for the existing 3-clock pin latency. |
| `drvl.yaml` | +7/−3 | 0 | stronger | Same citation, **plus a duplicate `timing:` key removed** — DRVL and DRVH had been disagreeing about pin timing in what consumers read. §1.10. |
| `concepts/streamer_smartpin_control.yaml` | +6/−8 | 1 | stronger | The removed block returned structured and cited; a derived figure replaced by the source's own wording. |
| `addsx.yaml` | +1/−1 | 0 | stronger | The same `Result[31]` sentence replaced, naming Table 9 and the TJV requirement. §1.13. |
| `getxacc.yaml` | +1/−1 | 1 | stronger | A dead locator re-anchored to a live, verified one (**F-365**). |
| `sumc.yaml` | +1/−1 | 0 | stronger | `encoding[0].c` had the C column's condition prose welded in front of a correct semantic — a CSV column-split artifact in a field no gate reads. |
| `sumz.yaml` | +1/−1 | 0 | stronger | `encoding[0].z` held the **C column's** condition text where the manual gives `Result = 0`. Wrong, not merely malformed. |

## `architecture/streamer/` — 8 files · 4 stronger · 3 equal · 1 new

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `pin-capture.yaml` | **+312/−0** | — | *new file* | Why a smart-pin bus must be watched from next door. §1.11. |
| `pin-selection.yaml` | +188/−57 | 34 | stronger | **F-361**: the dense sub-pin slot table no source states and the bench contradicts is gone, replaced by the real rule (`pin << 17`, `D[19:17] = pin & 7`); the `pin_base_encoding` example was the EF-065 misalignment trap written out for a reader to copy. |
| `modes-reference.yaml` | +43/−8 | 4 | stronger | `field_notation_caveat` expanded with a second bench proof and a source. |
| `_index.yaml` | +25/−0 | 0 | stronger | Gained the whole `pin_capture` routing entry plus aliases. |
| `dds-goertzel.yaml` | +22/−10 | 10 | stronger | Citations re-anchored from the partial `p2-documentation.txt` extract to `silicon-doc-text.txt`; aliases added. ⚠️ **Two locators only half re-anchored** — `:4062` is a blank line (**F-377**, §0.5 item 5). |
| `overview.yaml` | +21/−4 | 0 | equal | Apparatus only — aliases, `related:`, full-path `see_also`. |
| `nco-timing.yaml` | +11/−2 | 2 | equal | Apparatus only. Its `video_rates:92` carries the same `$0CE3_BCD3` as `setxfrq` (§0.5 item 13). |
| `dac-routing.yaml` | +10/−2 | 2 | equal | Apparatus only — aliases added, `see_also` bare names → full paths. No content change. |

## `architecture/smart-pins/` — 4 files · 4 stronger

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `smart-pin-11011-usb-host-device.yaml` | +28/−12 | 2 | stronger | USB 12 Mbps / 1.5 Mbps returned with the `D_14` field, the DP/DM roles and the FPGA resistor note. Carries **F-372 / G-027** — the sentence one edition of v35 states and the other omits, now presented as a conflict rather than as fact. |
| `smart-pin-00000-normal-mode.yaml` | +18/−11 | 2 | stronger | Both worked examples **corrected**: they taught the disproven `WRPIN P_HIGH_15K` + `DIRL` pull-up idiom. |
| `smart-pin-00011-dac-16bit-pwm-dither.yaml` | +17/−15 | 6 | stronger | Dither facts returned verbatim from `part4-smart-pins.txt:284-308`, plus the `M[12:10]=%101` requirement. |
| `smart-pin-11000-adc-internal-clock.yaml` | +9/−4 | 4 | stronger | `P_ADC_GIO`/`P_ADC_VIO` **redefined correctly** — they are calibration *sources*, not input ranges. The old text was a legal name with a wrong definition, which is the shape no constant gate can catch. |

## `architecture/boot-rom/` — **5 files at HEAD**, 4 rowed here · 4 stronger · **`boot-rom-contents.yaml` in §1.22**

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `_index.yaml` | +18/−15 | 12 | stronger | Boot timing and all three path summaries returned cited, with pin directions named **from the flash chip's side**. |
| `taqoz-forth.yaml` | +17/−0 | 0 | stronger | Gained `useful_for`, sourced to the author's own reviewer comment (**F-370**): ROM TAQOZ is an *early* build, not merely a cut-down one. |
| `boot-pattern-selection.yaml` | +15/−17 | 7 | stronger | **Corrected**: the claim that the ROM issues no `HUBSET` is contradicted by its own listing — the `Prop_Clk` and shutdown paths both do, now cited to `ROM_Booter.lst`. |
| `spi-flash-boot.yaml` | +5/−2 | 2 | stronger | Patterns returned verbatim; DI/DO direction disambiguated. |

## `application-notes/` — 4 files · 4 stronger

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `p2an003-dac-analog-signal-generation.yaml` | +17/−13 | 9 | stronger | `key_parameters` returns with verbatim dither text plus a new sourced `M[12:10]=%101` requirement. Deleted `200 MHz / 256 = 781_250 sps` as a derivation — see the inconsistency at §0.5 item 15. |
| `p2an001-single-pin-instrumentation-adc.yaml` | +15/−15 | 7 | stronger | Two removals were **corrections**: the designer's 15 mV became the hardware-verified ≤9 mV with an explicit *"do not quote 15 mV"*, and *"P2 spec max is 300 MHz"* was simply wrong (datasheet PLL max 320 MHz). Keeps an uncited derived `raw_sample_rate_sps` and one off-by-one locator (§0.5 items 15-16). |
| `p2an002-cordic-for-real-work.yaml` | +14/−12 | 7 | stronger | Six gotchas return with Silicon Doc quotes + EF-053; two dropped claims are **refuted**, not lost. Two locators of the F-377 shape. |
| `p2an004-frequency-rotation-rc-timing-measurement.yaml` | +14/−14 | 9 | stronger | Gotchas re-anchored to the datasheet Pin Mode Legend and the `%AAAA`/`%BBBB` table; the EF-063/EF-064 mis-attribution removed (`75971308`). ⚠️ Carries a self-contradiction about sensor figures (§0.5 item 14). |

## `guides/` — 2 files · 1 gutted-then-restored · 1 equal

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `pasm2-getting-started.yaml` | +135/−70 | 24 | ✅ **gutted → RESTORED** | The CON clock-setup declarations went missing while the file kept explaining what happens once you declare one. Net a large improvement everywhere else, which is exactly why a gate would have passed it. Restored source-first by `ca07aaf7`, with the "Required" claim dropped and the clock-ceiling block **replaced** rather than restored. §1.14. |
| `spin2-getting-started.yaml` | +31/−13 | 7 | equal | Relative→absolute path re-anchors, all targets verified present, plus dropping "pull resistors" from a routing blurb — honest, since `basic-io.yaml` now states the P2 has no internal pull network. Carried the same "Required" claim and was corrected with its sibling. |

## `architecture/system-registers/` — **2 files at HEAD**, 1 rowed here · 1 stronger · **`dira-dirb-registers.yaml` in §1.21**

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `complete-system-registers-index.yaml` | +36/−17 | 15 | stronger | 13 dangling `yaml_file:` pointers removed (**F-364**), content kept inline; `$1F6`/`$1F7` descriptions **corrected** — PA/PB hold the CALLD-imm *return* address and the CALLPA/CALLPB parameter, which "CALLD-imm parameter" named neither (**F-363**). |

## `code-examples/` — **2 files at HEAD**, 1 rowed here · 1 equal · **`code-example-schema.yaml` in §1.21**

| File | ± | GONE | Verdict | What changed |
|---|---|---|---|---|
| `smart-pins-002-button-reading.yaml` | +1/−1 | 1 | equal | One word: "Pull-up or pull-down resistor" → "**External** …", so it cannot be read as an internal P2 pull. |

---

# Appendix A — Commit legend

The **41 commits that touched `deliverables/ai/P2/**/*.yaml`**, oldest first. (153 commits landed in
the range across all paths; the rest touched tooling, registers, ingestion sources, analysis
documents or manuals.) **Every hash below is read from
`git log --oneline --reverse v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml'`, not from
recollection** — see the correction note under the table for why that sentence is here.

| # | Commit | Date | What it did to the shipped YAML |
|---|---|---|---|
| 1 | `15c84de5` | 08-24 | Removed **60** uncited quantitative blocks from `architecture/`, `language/`, `guides/`, `application-notes/` (25 files). Fixed six detector defects in the same pass; the negative control grew 5 → 13 cases, three of them MUST-STILL-FIRE controls that caught a first attempt quietly switching the gate off. |
| 2 | `c733a223` | 08-25 | Removed **59** uncited blocks from `hardware/` (17 files) — and repaired the two citation-side false negatives (`Rev B` as a citation, a key-name test) that had made the previous zero false. Control set 12 → 25 cases. |
| 3 | `cd860ba7` | 08-25 | Defined all **55** undefined constants in one home; 116 `aliases:` made them reachable; created `pin-drive-configuration.yaml`; deleted `P_LEVEL_B` / `P_SCHMITT_B`. |
| 4 | `4cecb02c` | 08-25 | Corrected the drive-strength mislabel class; both fidelity tiers to zero; nine examples extracted from the shipped bytes, compiled, **and read**. |
| 5 | `1f37ae58` | 08-25 | Applied the promotion filter to 233 blocks; deleted the `150mA` pin-current figure and the TTL logic levels beside it. |
| 6 | `597d5eba` | 08-25 | **46** blocks return cited to `architecture/`/`language/`/`guides/`/`app-notes`; three shipped errors fell out of reading the sources first. |
| 7 | `491f2b55` | 08-25 | **34** blocks return cited to `hardware/`; the Goertzel/Digital-I/O misidentification corrected; E-004 closed. |
| 8 | `9370c580` | 08-25 | Drained the KB-side findings; **rejected** two register corrections that would have introduced defects. |
| 9 | `e92aa02f` | 08-25 | Drained the manual-prose findings; falsified this sprint's own "masters are clean" (F-356); corrected the EF-063/EF-064 attribution. |
| 10 | `69af3733` | 08-25 | Fixed the citations that route every new agent; measured what the crossref gate cannot see (76%). |
| 11 | `43b0ede2` | 08-25 | Armed both content instruments as blocking release gates, after repairing the harvest behind them (116 constants on the truth side where there were none). |
| 12 | `43061dad` | 08-25 | Restored the corrective sentence a duplicate `note:` had been silently discarding; swept 1130 files and filed F-360. |
| 13 | `ad4f974f` | 08-26 | Streamer pin capture: the `IN`-is-the-event-flag rule, a new `pin-capture.yaml`, and aliases for seven unreachable `streamer/` files. |
| 14 | `ccddcbe6` | 08-26 | Ingested the `#64008` Click Adapter from its schematic; **all 12 mikroBUS offsets confirmed, 0 corrections**; new `addon-click-adapter.yaml`. |
| 15 | `601e65ce` | 08-26 | Self-audit of that record: three inference-as-reading claims labelled with what actually establishes them. |
| 16 | `599d3660` | 08-26 | The WX module's two form factors; recovered content the purge had removed, from the ingestion tree. |
| 17 | `36196329` | 08-26 | Applied **F-363**, **F-368**, **F-369**, **F-370** — the first ingestion findings to reach the KB. |
| 18 | `491d033b` | 08-26 | Wrote the package record (**F-366** / G-021) and re-anchored **23** citations off the superseded capture (**F-365**); one did not resolve → **F-372** + **G-027**. |
| 19 | `75971308` | 08-26 | Repaired four red ledger items: GETCT's description, E-010's pull-up that survived a rewrite, the fabricated `digital_io_board` in two guidance lists, and the EF-063/EF-064 attribution in four more files. |
| 20 | `e9dc9507` | 08-26 | The content half of `d756b44c` (which staged only three ingestion-source renames): duplicate keys to zero, SETLUTS's own content back, DRVL/DRVH reconciled and cited, `edge-breadboard-carrier`'s supply figure and `addon-serial-host`'s identity restored, the `1224` symbol count corrected. **`d756b44c` + `e9dc9507` are one unit** — `git add` aborted atomically on the first; the pair was not amended. |
| 21 | `9a1f14a3` | 08-26 | Re-derived the six fabricated-provenance files; the interrupt vector map was inverted. §1.6. |
| 22 | `4caeb6cc` | 08-27 | Two residues the gates cannot see, found while verifying the differential read: `interrupts.yaml` contradicting its own corrected block, and **F-377**. |
| 23 | `ca07aaf7` | 08-27 | Restored the clock-setup declarations (the one gutted file) and stopped telling readers `_clkfreq` was required. §1.14. |
| 24 | `b466a538` | 08-27 | The E-016 sibling sweep found its case: `ADDSX`/`SUBSX` shipping the manual's wrong C-flag sentence while contradicting it in the same file, plus two `SUM*` encoding fields. **F-379**. |

| 25 | `856ef2f2` | 08-29 | The SETXFRQ increment rule (**F-380**) — nine shipped NCO values wrong by one in bit 0 of a 31-bit phase word. §1.18. |
| 26 | `9723e482` | 08-29 | `io_pin_timing.yaml` re-anchored to the lines it actually comes from — **F-377 part 2**, the eighth fabricated-provenance file. §1.18. |
| 27 | `efc683a8` | 08-29 | Compiler acceptance range vs silicon rating, said as two different numbers (**F-378**) — five sites, not one. §1.18. |
| 28 | `ca684aac` | 08-30 | Sourced the census's 19 hardware quantities and fixed the six wrong facts reading them exposed — **F-395**, **F-396**, **F-397** filed, **F-398** registered unfixed; **F-390** and **F-391** applied. §1.19. |
| 29 | `912100db` | 08-30 | Every mechanically-broken citation locator repaired, and the first four F-377 mis-points found by reading. Built the extractor the census described but did not ship, after fixing its two defects. §1.19. |
| 30 | `9ab0433b` | 08-30 | Finished the citation read — **721 of 721** opened at their cited lines. **F-399** filed, **F-400** registered unfixed, **F-377** discharged. §1.19. |
| 31 | `395d6362` | 09-05 | The codegen-effect audit of the unpublished delta, and the **two locators the delta itself introduced**, repaired rather than carried — `interrupts.yaml`'s unresolvable `reti0..3.yaml`, and `edge-breadboard-carrier.yaml`'s citation of the ledger at its pre-move path. Both invisible to the crossref gate (comment text — F-373). §1.20. |
| 32 | `ba24f0f9` | 09-05 | The harvester reads twelve name-bearing fields instead of four — **0 → 62 of 62** pure-symbol Spin2 names. **F-376**'s third silent exit-0 closed in the same function, with a negative control. **F-401** and **F-402** filed; `modulo_add.yaml`'s inverted definition corrected. §1.21. |
| 33 | `19385b66` | 09-05 | Nine more fields harvested (the subtree-convention finding), thirteen files given hand-authored `aliases:`, `streamer-symbols.yaml`'s 78 `X_*` constants made reachable and its `total_symbols` corrected 82 → 78, and **the `+//` definition home merged per Stephen's agreement**. §1.21. |
| 34 | `2a6df5ef` | 09-08 | **F-403** — six ROM residents where the Hardware Manual names three, two of them traced to our own generated narrative. §1.22. |
| 35 | `b0057ec1` | 09-08 | Finished the F-403 sweep the previous commit had claimed without reading its output: `boot-rom/_index.yaml` stated the six-resident list **twice**. §1.22. |
| 36 | `de9b693e` | 09-09 | **F-404** — the 24 `<fmt>_{REG,BYTE,WORD,LONG}_ARRAY` formatter names a composition rule cannot spell; plus three lagging register statuses corrected (F-401, F-402, F-403). §1.23. |
| 37 | `235e714e` | 09-09 | **F-406**, retrieval half — 18 pull-vocabulary aliases, so a coder finds the drive constants by the word they type. 2 of 17 phrasings → 17 of 17. §1.24. |
| 38 | `2b4d81fb` | 09-09 | **F-406**, framing half — both `basic-io.yaml` blocks answer the pull-up question before qualifying it; three unpublished keys renamed. §1.24. |
| 39 | `4ef81b58` | 09-09 | **F-407** — the datasheet's DC Characteristics table, carried at last, where a fabricated `input_characteristics` block had been removed with nothing put in its place. §1.24. |
| 40 | `d757adde` | 09-09 | Task «#338» item 1 — `p2an001` cited the datasheet's **crystal** row for a PLL figure. §1.25. |
| 41 | `0f8274f5` | 09-09 | Task «#335» — **43 dangling references redirected**, none deleted; **F-373** re-graded `PARTIAL` because the gate half is untouched. §1.25. |

*(Rows 25-27 are the 2026-08-29 pass; that revision described them in §1.18 but its Appendix A table
stopped at 24. Recorded here so the legend and the count agree. **Corrected 2026-08-31:** the
2026-08-30 revision of this table named `43e7f8b1` at row 26 — **no such object exists**, and row 27
named `79fbbe1e`, which touches no shipped YAML and belongs in the list below, not in the legend.
Both were written from recollection rather than derived from `git log`, which is the one thing this
document is not allowed to do. 24 + 3 + 3 + 5 + 4 + **2** = **41**, matching §0.1. Rows 31-35 were derived
the same way, and the **two 09-05 index regenerations are deliberately NOT in this table** — they
touch `deliverables/ai/p2kb-index.json` only, which is a regenerated artifact and not shipped YAML.
That is exactly how the gzip drift stayed invisible: see F-405 and the list below.)*

**In the range, touching no shipped YAML, and load-bearing for this release:**
`79fbbe1e` (brought this ledger up to the tree it describes, and was its derivation baseline until
2026-08-30) · `d756b44c` (the three `p2-hub75-adapter` source renames — half of #20) ·
`02ff61b7` (armed `audit-yaml-duplicate-keys.py`) ·
`d62544ea` (repaired `audit-register-hygiene.py` so it reads the registers it was reporting clean on)
· `11ebec54` (regenerated the index **and** its gzip together, the pair F-357 records as having
drifted for four days) · `fc45912d` (the `deliverables/ai/P2/CHANGELOG.md` release entry) ·
`b753a29d` (re-derived this ledger at `9ab0433b` and regenerated the index pair) ·
`a7fd84e3` (gave this ledger its "why" layer, and corrected the invented hash named above) ·
`068ccaa0` (filed **F-401**) · `2a869e64` (annotated F-401 with what pass 1 measured) ·
`6434fdc0` (added Appendix A to the codegen report — the two deleted blocks verbatim, for your visual
audit) · **`d55b6c7f` and `da896073`** (the two 09-05 index regenerations — ⚠️ **each rebuilt
`p2kb-index.json` and neither rebuilt `p2kb-index.json.gz`; this is F-405, and it left
`validate-dod-release.py` red for four days**).

**In the range and NOT this release's work:** `7be432a6` ("pnut-ts 015504, and the Dockerfile no
longer names the version") — another session, no KB YAML.

---

# Appendix B — Findings, errata and gaps referenced, with status at HEAD

Status read from the registers at HEAD, not carried from a task record. `RESOLVED` entries are
**closed and awaiting the next archive sweep**, not awaiting work.

## Corrections register — the entries this release moved or created

| ID | Status at HEAD | Subject |
|---|---|---|
| F-407 | `PENDING-VALIDATION` | The datasheet's DC Characteristics table was never carried, so the KB answered "what is the input threshold?" with silence after the fabricated answer was removed |
| F-406 | `PENDING-VALIDATION` | A coder asking for a pull-up got a denial first and the answer fourth, and 15 of 17 phrasings of the question resolved to nothing |
| **F-405** | **`PARTIAL`** | The index and its gzip drifted apart again and `validate-dod-release.py` sat **red in committed history for four days** — F-357's defect, recurred. Drift repaired; **the missing wiring that would prevent recurrence is not** |
| F-404 | `PENDING-VALIDATION` | 24 of the 54 Spin2 DEBUG formatter names the v55 reference lists resolve to nothing, because the file documents them as a composition rule rather than as strings. Includes `UHEX_LONG_ARRAY` |
| F-403 | `PENDING-VALIDATION` | Character font data and sin/cos/log tables asserted as boot-ROM residents on the strength of our own generated narrative; the authoritative content list names three things |
| F-402 | `PENDING-VALIDATION` | Two files defined `+//` and disagreed; `modulo_add.yaml` called it an addition. Corrected, and merged into one definition home per Stephen's call |
| F-401 | `PENDING-VALIDATION` | The index harvested four name fields, so **0 of 62** pure-symbol Spin2 names were reachable. Twelve fields now harvested; 62 of 62, and dark files 452 → 173 |
| F-379 | `RESOLVED` | `ADDSX`/`SUBSX` shipped the manual's wrong C-flag sentence; two `SUM*` encoding fields malformed |
| **F-378** | **`CONFIRMED`** | `_CLKFREQ range` ships the compiler's acceptance range, unlabelled, 180 MHz past the datasheet ceiling |
| F-377 | `RESOLVED` | Translated locators that are in range and point at nothing; an eighth fabricated-provenance file. **Discharged 2026-08-30 by F-399** — all 721 locators opened and read. |
| F-399 | `RESOLVED` | The citation read run to the end: 721 locators, 22 repaired, and the two instrument defects that had to be fixed first (form-feed line counting; locator binding) |
| **F-400** | **`CONFIRMED`** | The `v55:NNNN` citation shorthand resolves to no file — a locator a reader can follow and a tool cannot. Registered, not fixed. |
| F-395 | `RESOLVED` | `hardware-compatibility-matrix.yaml` told readers to feed a 5.5 V-maximum board 9 V, and that two carriers cannot take accessory boards at all |
| F-396 | `RESOLVED` | F-350 corrected one file of a four-file family and no sweep ever ran; the whole fabrication set was still live in the sibling selection guide |
| F-397 | `RESOLVED` | The census's 19 uncited electrical quantities, sourced or removed; three of them were wrong |
| **F-398** | **`CONFIRMED`** | The hardware selection guide ships 2025 US retail prices as data. Registered, not fixed — F-374's shape in a different key. |
| F-390 | `RESOLVED` | `cogspin`/`coginit` documented `-1` as a synonym for `NEWCOG`; the silicon reads it as *start a PAIR* |
| F-391 | `RESOLVED` | `hub.yaml` put the HUBSET write-protect bit at D[2] (it is D[16]) and claimed all cog state is saved on debug entry (it is `$000..$00F`) |
| **F-376** | **`CONFIRMED`** | Two silent-failure bugs in the KB tooling, both exit 0 |
| **F-375** | **`CONFIRMED`** | The delivery filter strips `documentation_source:` from 383 files; 706 values are real citations |
| **F-374** | **`CONFIRMED`** | 40 quality-score sites across 18 files state a judgement, not a fact |
| **F-373** | **`CONFIRMED`** | Three top-level fields typed `text`; 14 shipped paths in them resolve to nothing |
| **F-372** | **`CONFIRMED`** | `%11011` says a new WRPIN needs no reset; the same document's general rule says the opposite |
| F-371 | `RESOLVED` | The sprint plan's "8 blocked sources" was wrong on five |
| F-370 | `RESOLVED` | ROM TAQOZ is an EARLY build, not just a cut-down one |
| F-369 | `RESOLVED` | The smart-pin DIR-reset mechanism, in the Silicon Doc and carried nowhere |
| F-368 | `RESOLVED` | `getbrk.yaml` dropped a Z value and declared `Z: No effect` for an instruction requiring one |
| **F-367** | **`CONFIRMED`** | `external-inputs/p2/` and `sources/silicon-doc/` hold different documents under one filename |
| F-366 | `RESOLVED` | No package record existed; the source had been in the repo unextracted |
| F-365 | `RESOLVED` | 23 shipped citations pointed into the superseded lossy capture |
| F-364 | `RESOLVED` | The register index advertised 16 files; 13 pointers did not exist |
| F-363 | `RESOLVED` | PA/PB described as "CALLD-imm parameter"; all three authorities say **return** |
| F-362 | `RESOLVED` | The hygiene gate reported CLEAN while reading zero entries |
| F-361 | `PENDING-VALIDATION` | `pin-selection.yaml`'s wrong sub-pin bit weights; the EF-065 trap as its example |
| F-360 | `RESOLVED` | Duplicate keys destroy content silently — **gate armed; wiring it into the release validator is still open** |
| F-359 | `RESOLVED` | Fabricated provenance headers — **the eight non-derivable claims are left standing for Stephen** |
| F-358 | `RESOLVED` | Check 10 had never once been able to fire |
| F-357 | `RESOLVED` | The index and its gzip drifted in committed history for four days |
| **F-356** | **`CONFIRMED`** | The drive-strength mislabel is alive in the IOSP master at 23 sites |
| F-355 | `RESOLVED` | The hygiene gate could not see the new errata register |
| **F-354** | **`CONFIRMED`** | Seven content-level holes inside blocks that DID come back |
| F-353 | `PENDING-VALIDATION` | The 58 in-scope hardware blocks, plus six wrong scalars in surviving blocks |
| **F-352** | **`CONFIRMED`** | Two shipped areas are authored-here with no upstream; the removal rule has no branch for them |
| F-351 | `RESOLVED` | The sourcing gate read part numbers and code points as amperes |
| F-350 | `PENDING-VALIDATION` | The eval-board fabrication class is not confined to one file |
| F-349 | `PENDING-VALIDATION` | PLL lock stated as ~10 µs in one place and ~10 ms in four |
| F-348 | `PARTIAL` | A *cited* block shipped a pin-current limit five times the absolute maximum |
| F-347 | `PARTIAL` | The `architecture/`-side purge removal record |
| F-345 · F-346 | `PENDING-VALIDATION` | Inverted flag polarity in a worked example; three structurally unrunnable examples |
| F-344 | `CONFIRMED` | A derived board extract contradicts itself about switch polarity → Parallax |
| F-343 | `PENDING-VALIDATION` | The Control Board credited with pull-ups its guide does not give it |
| F-342 | `RESOLVED` | A Parallax guide states the mislabel itself, in the one configuration where it cannot work |
| F-341 | `PARTIAL` | Six derived analysis documents sit inside the fidelity gate's documentary truth root |
| F-340 | `PARTIAL` | The crossref validator reads top-level keys only |
| F-338 | `PARTIAL` | `P_LEVEL_B` / `P_SCHMITT_B` do not exist |
| **F-337** | **`CONFIRMED`** | Datasheet + Hardware Manual vs Silicon Doc on `%TT` in DAC_MODE; the YAML follows the minority |
| **F-336** | **`CONFIRMED`** | The weak-drive idiom set is one composition wide, and that composition has no source |
| F-335 | `RESOLVED` | A whole class of board file mis-tiered into the advisory lane by a citation spelling |
| F-334 | `PENDING-VALIDATION` | The `hardware/` purge removal record; a citation token that silences the gate |
| **F-332** | **`CONFIRMED`** | Ten six-digit `%SSSSS` values for a five-bit field, with no reconciliation note |
| F-331 | `PENDING-VALIDATION` | Three of the six WRPIN D-operand fields mislabelled |
| F-329 · F-333 | `PARTIAL` · `PENDING-VALIDATION` | The fabricated drive ladder in blocks F-327 does not name; the same claim in a `description:` |
| F-328 | `PENDING-VALIDATION` | `p2-eval-board.yaml` describes a board the `#64000` guide does not |
| F-321…F-327 | `PENDING-VALIDATION` | The drive-strength mislabel class this sprint started from |

**One status was corrected while building this table.** F-360's headline read `CONFIRMED` while its
own body's closing line read ``Status: `RESOLVED` ``. Flipped to `RESOLVED`, which is what the body
establishes (4/4 sites fixed, gate armed, 0 duplicates across 1132 files). **The hygiene gate reports
CLEAN both before and after the flip**, so it cannot see this class: F-358's headline-vs-body check
reads `**Status:**` at column 0, and this entry states its status indented inside a bullet. Not
filed as a new finding — the allocator is the arbiter's — but it is the same shape as F-358.

**Register state after this pass:** **131 live · 294 archived · 0 unaccounted · next `F-408`**
(`audit-register-hygiene.py`, exit 0). It read 124 live / next `F-401` on 2026-08-30; F-401…F-405
account for the difference.

**Findings filed during this sprint: F-373…F-407, thirty-five of them — and every single one was
filed by a verification step rather than by the work it was verifying.** That pattern has not broken
once. The last five are the sharpest instance of it: **F-401 came from a question outside the release
entirely**, F-402 from *arming* F-401's fix, F-403 from surveying what the KB claims rather than
fixing anything, and **F-404 and F-405 from re-deriving this very document** (§1.23). Nothing here
was found by the pass that created the defect.

**Three status corrections were made while building this table**, all of them the register lagging
the artifact rather than the artifact being wrong — F-402 (`PARTIAL` → `PENDING-VALIDATION`; the
merge it called Stephen's open call had landed four days earlier), F-403 (`CONFIRMED` →
`PENDING-VALIDATION`, and its `_index.yaml` half was unrecorded), and F-401's result table, which
recorded pass 1 of two. **A status line is not evidence, and it lies in both directions:** F-402
under-reported progress, F-403 over-reported openness.

## Source errata

**17 live, next `E-018`.** Referenced above: **E-004** (an RTC guide's "150 kΩ pull-up" mislabel —
closed in the KB by `491f2b55`), **E-007** (where two documents frame a limit differently, the KB
must label which framing it is quoting — applied by `ca07aaf7`, **not yet applied to F-378**),
**E-010** (the Edge guides' "enable a pin pull-up" — out of the shipped set as of `75971308`),
**E-012**…**E-016** (Propeller 2 Documentation v35 and the PASM2 Manual contradicting themselves),
and **E-017**, filed this sprint: `COGATN`'s operand width, where the Datasheet's prose says 8 bits,
its own instruction table says `D[15:0]`, and the Silicon Doc says 16.

**E-016 is the one that reached the shipped YAML.** Its sibling sweep is `b466a538` / F-379: the
manual is wrong **and our KB followed it**, in two of the eight files in the family.

## Knowledge gaps

**37 live, next `G-29` / `Q-10`** (`audit-register-hygiene.py` at HEAD, exit 0 — the earlier "36 live"
was measured before the counter advanced).

| ID | State | Note |
|---|---|---|
| **G-021** | **ANSWERED — APPLIED** | The TQFP-100 package drawing was in the Silicon Doc all along. Closed by `491d033b`. |
| **G-026** | **ANSWERED** | microSD boot selection is **P59**, not P60, and it is a DIP switch pair rather than a single pull-down — closed from the Edge Module Rev D guide. It corrects the Silicon Doc reviewer comment that raised the gap. The KB already carried the table; it was never connected to this gap. |
| **G-027** | **OPEN** | Can a new WRPIN reconfigure a *running* USB smart pin? Two editions of one document disagree. **Bench-testable and jumper-only.** Paired with F-372. |
| **G-020** | **OPEN — re-tested and CONFIRMED** | No thermal-design content exists anywhere in the corpus. The new package record says so explicitly rather than letting a reader infer a thermal solution from exposed-pad size. |
| **Q-009** | open | Under what conditions does RDFAST corrupt? Established as real by the designer in the Silicon Doc's own review thread, where both he and the reporter state they cannot explain it — so **no document can close it**. |

---

## How to re-derive every number in this document

```bash
G="git"   # the -c safe.directory workaround is retired: /etc/gitconfig carries
         # safe.directory=/workspaces/* at system scope (8778e6a2). Do not re-add it.

# Scope (§0.1)   — run against HEAD; the body's per-pass tables are stated at their own revisions
$G diff --name-only  v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' | wc -l     # 118
$G log  --oneline    v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' | wc -l     # 41
$G log  --oneline    v1.17.0..HEAD | wc -l                                       # 153
$G diff --numstat    v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' \
   | awk '{a+=$1;r+=$2} END{print a,r}'                                          # 7528 3684
$G diff --diff-filter=A  --name-only    v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml'   # 4
$G diff --diff-filter=DR -M --name-status v1.17.0..HEAD -- 'deliverables/ai/P2/**/*.yaml' # empty

# Blocks (§0.3) and shapes (§1.16): parse both revisions and compare top-level key sets / types
$G archive v1.17.0 deliverables/ai/P2 | tar -x -C /tmp/old
$G archive HEAD    deliverables/ai/P2 | tar -x -C /tmp/new

# Gates (§0.4) — run, never quoted
python3 engineering/tools/verify-yaml-format.py
python3 engineering/tools/validate-crossref-keys.py
python3 engineering/tools/validation/audit-yaml-claim-sourcing.py
python3 engineering/tools/validation/audit-constant-fidelity.py
python3 engineering/tools/validation/audit-extraction-digit-density.py --all
python3 engineering/tools/validation/audit-yaml-duplicate-keys.py
python3 engineering/tools/validation/audit-register-hygiene.py engineering/operations/P2KB-CORRECTION-FINDINGS.md
python3 engineering/tools/validation/audit-register-hygiene.py engineering/ingestion/KNOWLEDGE-GAPS.md
python3 engineering/tools/validation/audit-register-hygiene.py engineering/ingestion/SOURCE-ERRATA.md
python3 engineering/tools/validate-dod-release.py                                # 11 checks

# Citations (§1.19) — resolve every <path>:<line> in the shipped set and open each cited line.
#   SPLIT ON '\n' ONLY. str.splitlines() also breaks on form feed, and 117 of these
#   PDF-derived sources carry them (up to +398 lines). Newline-only is the truth side,
#   because the citations were written against grep/sed numbering.
#   Bind a bare continuation locator (", :1565") to its path; this corpus writes them on
#   BOTH sides of the path, so a locator that cannot be bound is a CITATION defect, not a
#   tool defect. Expect: 721 locators, 83 files, 40 source documents, 0 unresolved.

# The index pair — regenerate TOGETHER, and AFTER the content commit (the index stores git blob sha256)
#   ⚠️ BOTH LINES, ALWAYS. Regenerating the .json alone is F-357 / F-405, and it has now happened
#   TWICE: 11ebec54 records the first (four days adrift), d55b6c7f + da896073 the second (four more).
#   validate-dod-release.py catches it on the first run — so RUN IT, every time either file moves.
python3 engineering/tools/generate-p2kb-index.py
gzip -c deliverables/ai/p2kb-index.json > deliverables/ai/p2kb-index.json.gz
gzip -cd deliverables/ai/p2kb-index.json.gz | cmp - deliverables/ai/p2kb-index.json
$G diff --quiet deliverables/ai/p2kb-index.json deliverables/ai/p2kb-index.json.gz  # freshness: no gate does this yet

# Findability (§1.21, §1.23) — read the EMITTED index, never the generator's summary
python3 - <<'EOF'
import json
b=json.load(open('deliverables/ai/p2kb-index.json'))
files,al,cats=b['files'],b['aliases'],b['categories']
tgt={t for v in al.values() for t in (v if isinstance(v,list) else [v])}
mem={m for v in cats.values() for m in (v if isinstance(v,list) else v.keys())}
dark=set(files)-tgt-mem
print(len(files), len(set(files)&tgt), len(dark), len(al))   # 1133 955 173 2920
print({files[k]['path'].split('/')[3] for k in dark})        # {'community'}
EOF
#   2920 is post-F-404; the tables above read 2896, which is the count at b0057ec1.
```

**The tree is at release position and is deliberately unreleased.** No version bump, no tag, no push.
What still needs Stephen is in `engineering/analysis/2026-08-27-awaiting-stephen.md` — noting that
its item 1 predates the 2026-08-29 fix pass (§0.6), so read that item's *options* as still live but
its "already done" paragraph as superseded by §0.1 and §0.5 here.

**Reviewing this document is the release gate.** Stephen, 2026-08-29: *"we don't release until my
visual check of the all changes document confirms the content."* Nothing is tagged or pushed until
that read happens.

**Re-derived 2026-09-09 at `b0057ec1`**, on Stephen's instruction, because the document was derived at
`9ab0433b` and five commits had touched the shipped YAML since. **Six further commits landed the same
day**, from his review of this document; they are §1.23 · §1.24 · §1.25 and the numbers above include
them.

**What changed, in one paragraph.** The change set is **118 files / +7528 −3684 / 41 commits** (was
96 / +6703 −3480 / 30). Six new passes are described — **§1.20** the codegen-effect audit, **§1.21**
the findability pass, **§1.22** the boot-ROM content list, **§1.23** what re-deriving found on its own
account, **§1.24** the terminology review, **§1.25** the reference sweep. Every count in §0.1, §0.2,
§0.3, §0.4 and §0.5 was **re-measured, not adjusted**. **Nothing about the shipped set's coverage
changed** — no file was added or deleted; 22 files entered the *change set* after `9ab0433b` and every
one was already in the shipped set.

**Then his review of it found three more things, and they are the reason to read §1.24 and §1.25.**
He asked how the Spin2 pull-up/pull-down constants are handled, which surfaced **F-406** — every fact
correct, coverage *up*, and the reader answered with a denial they could reach by only 2 of 17
phrasings. He asked whether anything else in the change set had that shape, which surfaced **F-407** —
a fabricated block correctly removed and never replaced, while the real DC Characteristics table sat
one page over in a source the same file cites. And he asked whether anything blocked releasing, which
surfaced **43 dangling references** (task «#335», **F-373** → `PARTIAL`) and a citation pointing at
the datasheet's crystal row instead of its PLL row. **None of the three was found by a gate; all three
were found by him reading this document and asking a question.**

**And the re-derivation found the tree red.** `validate-dod-release.py` exited **1** at `b0057ec1` — the index and
its gzip had drifted apart on 09-05 and **nothing had run the validator since 08-30**. That is F-357
recurring while F-357 reads `RESOLVED` (**F-405**, `PARTIAL`). Repaired; the validator is green at
11 of 11. Two register entries were also lagging the artifact and one was over-reporting openness
(F-401, F-402, F-403 — all corrected), and three new findings were filed and fixed (**F-404**: 24 of 54
DEBUG formatter names resolved to nothing, now 54 of 54; **F-406** and **F-407**, §1.24), plus the
43-reference sweep that moved **F-373** to `PARTIAL` (§1.25). **Not one of them was found by a gate.**
Four came from checking numbers this document asserts; three came from Stephen reading it and asking
a question.

**What is left for Stephen is unchanged**, and no new decision was added to it: §0.5's red block —
**F-359** (the eight non-derivable claims — deletion is his), **F-367** (reconcile-or-delete the
duplicate Silicon Doc DOCX), **F-375** (the 383-file rename scope call), the **ENH-NN** allocator,
**F-398** (the price data), **F-400** (the `v55:` shorthand) — plus **F-374**, whose class boundary is
still undefined and is a definition call, not research. **F-402's merge left that list**: he decided
it on 09-05 and it shipped the same day.

---

## §1.26 — F-375's gate half, and what the delivery actually strips (2026-09-11, block I «#340»)

**The gate half is fixed.** F-375's complaint was structural: *every gate reads the tree, the
consumer reads the stream, and nothing compares them.* That is now false in the one place it
mattered most. `validate-dod-release.py`'s `validate_metadata_filter` used to classify which lines
the filter REMOVED and never re-parse what the filter DELIVERED, so a mapping key whose only
children were filtered fields arrived at the consumer as `null` and passed clean. It now
`yaml.safe_load`s the filtered payload and fails on any key that collapsed to `None`. Proven with a
negative control built independently of the fix: a block holding only `documentation_source` now
delivers `extraction: None` and the gate FAILS, while the same block with one surviving sibling
passes. (Landed with block H, `75911edb`.)

**The delivery-strip numbers, re-derived 2026-09-11 — not carried forward from the filing.**
`fetch-kb-file.sh:188 filter_metadata` strips five fields from every delivered file:

| field stripped | values on disk | files |
|---|---:|---:|
| `documentation_level` | 408 | 408 |
| `documentation_source` | **396** | 395 |
| `last_updated` | 389 | 389 |
| `enhancement_source` | 356 | 356 |
| `manual_extraction_date` | 147 | 147 |

**The `documentation_source` split is the finding, and it is worse than the ratio suggests.**

| | count | share |
|---|---:|---:|
| real provenance | **363** | **91%** |
| bookkeeping tokens | 33 | 9% |

The bookkeeping is only `enhanced` (16), `original` (15), `code_analysis` (1) and `redirect_stub`
(1). Everything else is a genuine citation — *PASM2 Manual 2022/11/01 Pages 31-147* (145),
*PASM2 Manual 2022-11-01* (116), *PASM2 Manual 2022/11/01* (60), *PNut v55 (DebugDisplayUnit.pas)*
(9), *p2_datasheet* (8), *Silicon Doc v35* (4), *P2 Instructions v35 CSV* (2), and per-page cites.

**So the set satisfies cite-or-omit ON DISK and is delivered NOT satisfying it.** 363 real citations
are stripped at the moment of delivery, and nine tenths of what the filter removes is the very
provenance the project's own rule requires. A remote agent fetching a key receives content with no
statement of where it came from — and every gate we run reads the tree, where the citation is still
present.

**Filing drift, recorded rather than smoothed over:** the finding states 397 values across 396
files; today's re-derivation gives **396 across 395**. One value moved in two weeks. Small, and the
point of re-deriving is that it moved at all.

**Still Stephen's call, unchanged by this entry:** the 383-file rename (F-375's other half) is a
scope decision, not research, and is not in block I.

**Also closed since the last entry:** F-374's class boundary is no longer undefined — it was
defined and worked (block F, `e80be72c`): 40 sites across 18 files removed. Three new findings were
filed today, all from reading artifacts rather than from a gate — **F-424** (an ADC comparator
example still quoting a fixed-volt threshold in the manual F-412 just repaired), **F-425**
(F-374's class surviving under `cost_efficiency` and `production_readiness: "excellent"`), and
**F-426** (F-413's 300 MHz maximum standing in a companion F-413 never looked at).
