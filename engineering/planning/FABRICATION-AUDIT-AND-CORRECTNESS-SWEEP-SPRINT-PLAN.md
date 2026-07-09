# Fabrication Audit & Correctness Sweep — Sprint Plan

**Head:** manual (+ yaml) — cross-head correctness program
**Trigger:** PASM2 Assembly Language Reference forum-defect report (M1k3yM1k3y / Rayman, 2026-07-09)
**Findings anchor:** `manuals/p2-assembly-language-manual/audit/forum-feedback-2026-07-09-instruction-reference-errors.md`
**Authored:** 2026-07-09

---

## Program context (this plan is Group 1 of ≥3)

User feedback arrives in **groups** (≥3 planned); this plan is **Group 1**. The
governing discipline (see [[feedback_classwide_sweep_on_every_finding]]):

- **Every finding → class-wide sweep** across all documents + all YAMLs. No
  lightweight/triage version.
- **Full audit gates re-release.** A region we cannot show was fully audited gets
  fully audited before its manual re-releases.
- **No release until all sweeps land.** Groups 1–3 + the DEBUG-window ZIP pass all
  modify content first; then **one coordinated release sweep** bumps/re-releases
  each modified manual **once**, version set at release time per our release skills
  by the nature of that manual's changes (avoids double-bumps).
- **Separate tracks:** YAML releases on its own process; documentation on its own.

**Explicitly downstream of this plan (not deliverables here):** feedback Groups 2–3;
the DEBUG-window manual ZIP-rebuild pass; the coordinated release sweep.

**Sequencing (locked with Stephen):** root-cause → methodology upgrade → author the
audit spec → **pilot on PASM2 Part I (checkpoint: Stephen reviews the spec)** →
fan-out audit across all released docs (+ mandatory adversarial verify + my
hand-check) → class-wide correction sweeps → re-render (no release).

---

## § Sprint-start record (2026-07-09)

- **Build number — DEFERRED.** No release this sprint; per Stephen's directive,
  every adjusted manual's version is set at the **coordinated release sweep** by the
  nature of its changes (fabrication corrections ⇒ content bump, not patch). The
  YAML operator corrections release on the KB track (its own version). Nothing is
  pinned now.
- **Working-tree audit — clean in the blast radius.** All files this sprint edits
  (assembly `opus-master/`, `TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md`, the YAML tree)
  are committed. Only untracked in-scope item: this plan doc (to commit as the sprint
  foundation). Out-of-scope untracked (architect `presentation/`, two debug-window
  `.backup` files) left for Stephen — not touched.
- **Tracking-readiness — READY.** No completed tasks lingering; context pruned
  50→38 keys (12 superseded `resume_*` snapshots removed, snapshot
  `tasks/backups/project_dump_20260709_213838.json`); MEMORY.md 119 lines. The 4
  leftover board tasks (#110 doc-style-change, #54/#46 IOSP-paused, #160 diagram
  propagation) are **unrelated to this sprint → handled separately, not folded.**
- **Baseline-health (yaml:p2kb entry baseline) — GREEN.** `verify-yaml-format.py`
  1129/1129 parsed clean; `validate-crossref-keys.py` all resolved. No failure
  groups, no skips. This is the entry baseline the closeout asserts no-regression
  against (manual head has no local build gate — its baseline is the Part I audit
  state established in Deliverable 1).

## § Resolved scope decisions (both closed 2026-07-09)

1. **AI Privacy Guide — EXCLUDED** from the fabrication-audit fan-out (Stephen: "the
   privacy guide can be ignored"). It makes no P2 capability claims, so the class has
   no surface there. **Fan-out scope = 13 P2 documents** (Getting Started, IOSP,
   Assembly, DeSilva, Debug, Streamer, Architect, P2AN001–006).
2. **Fan-out granularity — my call** (Stephen: "under your control … most efficient
   /most reliable"). Decision: **one finder per Part/chapter-range** for the large
   manuals (Assembly 505pp → per Part I/II/III + appendices; IOSP 396pp → per
   chapter-cluster), **one finder per document** for the smaller manuals and each
   app-note. Rationale: bounded per-agent context maximizes claim-extraction recall,
   which is the reliability driver for a fabrication hunt; the adversarial-verify
   stage (§5) absorbs the cost of more, smaller finders.

*No open questions remain — planning gate met.*

---

## 1. Root-cause analysis — why the fabrications slipped the prior audits

**Why:** we cannot prevent a class we have not diagnosed. This is the study that
justifies the methodology upgrade (§2).

**Current-code starting point:**
- `manuals/p2-assembly-language-manual/audit/PART-I-ARCHITECTURAL-AUDIT-PROPOSAL.md:25` — the Part I audit **scope list** is 8 hand-picked architectural features (condition prefixes, WC/WZ/WCZ, address modes, AUGS/AUGD, REP, SKIP/SKIPF, MODCZ, special registers).
- `…/audit/PART-I-AUDIT-CONSOLIDATED-FINDINGS.md:43` — findings organized by those same 8 categories.
- `…/audit/100-percent-audit-A-B.md` … `T-Z.md` — the only *exhaustive* coverage is Part II A–Z instruction entries.
- The six reported defects live in `part-i/chapter-03-flags.md` (§3.2.6:180, §3.3.1:207, §3.3.2:223, §3.5.4:420) and `part-i/chapter-04-timing.md` (§4.6.2:469) — **none of which are in the Part I audit's 8-feature scope.**

**Target (finding to write):** a short root-cause memo in the manual's `audit/`:
*the Part I audit verified a curated feature list, never performed exhaustive
claim-level extraction of narrative/example prose; flag-behavior idioms and
timing narrative were unverified; the trust-chain proof (silicon→YAML→doc) was
applied to instruction entries, not to conceptual prose.* Name the process
invariant this violates and that §2 must add.

**Verification:** normal — the memo names every reported defect's section and shows
it was outside prior scope; edge — a reported defect that *was* nominally in scope
(none, but check) is called out separately; error — if any defect was in scope and
still missed, that is a *different* root cause (verification depth, not coverage) and
must be recorded as such.

## 2. Audit-methodology upgrade (project-owned) + skill proposals

**Why:** the audit that missed this becomes the audit spec that cannot. Encode the
Group-1 finding taxonomy into our process so it is caught everywhere, forever.

**Current-code starting point:** `engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md`
- Part II (`:77`) Hallucination Detection — has linguistic/content red flags; **extend** with the exact capability-fabrication phrasings from this report ("allowing … in parallel", "setting C to indicate", "issue … and immediately begin").
- Part V (`:202`) Claim Verification — **strengthen**: exhaustive claim extraction must cover **all narrative + example + idiom prose**, not a curated feature list (the §1 root cause); every capability/behavior claim carries a trust-chain proof **silicon → YAML → doc**, and **the YAML is not an authority until itself proven against silicon.**
- Part VI (`:240`) Semantic vs Formatting — **add** the operator-notation rule ([[feedback_behavior_notation_vs_code_operators]]): `=` receives / `==` compares in behavior descriptions; `:=`/`==` strict in Spin2 code; a comparison written `=` is a correctness defect.
- Part IX (`:349`) Issue Severity — **remove/replace.** No severity. Judgment is binary right/wrong; wrong ⇒ repair ([[feedback_classwide_sweep_on_every_finding]]). Every finding triggers a class-wide sweep.
- Part VIII (`:297`) Multi-Phase — **add** the fan-out execution mode (§3/§5) with its mandatory adversarial-verify + hand-check stage.

**Also update (project-owned):** this manual's `creation-guide.md` and
`MANUAL-DESCRIPTOR.md` — record the flag-behavior/timing-narrative fragile areas and
the operator-notation rule as write-time verification requirements.

**Central skill (propose only — never edit central):** write a proposal to extend
`document-audit` with the exhaustive-prose-claim rule + operator check + fan-out
mode; add a `feedback_skill_evolution_candidates.md` entry.

**Verification:** normal — re-running the upgraded checklist against the six known
defects flags all six; edge — the checklist flags a *correct* "receives" `=` as
NOT a defect (no false positive on the operator rule); error — a curated-feature
audit that skips example prose fails the new coverage gate.

## 3. Author the fan-out audit spec (the finder + verifier packet)

**Why:** every fan-out agent must run the *same* verification or findings are uneven.
This is the operationalization of §2 into an agent-executable spec.

**Target:** a self-contained audit-spec doc the Workflow injects into every finder:
(a) trusted-source paths — `ingestion/sources/p2-instructions-csv/P2 Instructions v35 …csv`, `ingestion/sources/silicon-doc/`, Spin2 v55 ref; (b) `p2kb-mcp` for the YAML tier; (c) the claim-extraction rule (all prose, exhaustive); (d) the trust-chain-proof output schema (claim → silicon cite → YAML cite → doc loc → verdict aligned/misaligned/**fabricated**/operator); (e) the fabrication red-flags; (f) explicit instruction that findings will be adversarially re-verified (raise recall, flag uncertainty, do not suppress).

**Verification:** the spec, handed to a fresh agent against PASM2 §3.5.4, independently
re-derives the ABS fabrication with the correct silicon cite (row 62, C = D[31]).

## 4. Pilot — run the upgraded audit on PASM2 Part I (CHECKPOINT)

**Why:** validate the spec + finder prompt on the known-bad region before spending
the fan-out. **Stephen reviews the audit spec at this checkpoint** before it drives
the full fan-out.

**Target:** run the §3 spec over `part-i/chapter-01…06` → a Part I findings register.
Success = it catches all six reported defects **and** surfaces the rest of Ch.1–6's
unverified claims. Tune the spec on any miss/false-positive.

**Verification:** normal — six known defects present in the register with correct
silicon cites; edge — at least one *new* previously-unreported claim is surfaced and
verified (confirms exhaustiveness beats the old curated scope); error — a false
fabrication call is caught at Stephen's checkpoint and the spec tightened.

## 5. Fan-out fabrication audit — all released P2 documents

**Why:** "these are the worst" — a full trust-chain fabrication audit across every
released P2 doc, done in parallel, not six sequential sprints.

**Mechanism:** a **Workflow** — finders (per §Open-Q-2 granularity) over the 13 P2
docs (Getting Started, IOSP, Assembly, DeSilva, Debug, Streamer, Architect, P2AN001–006)
→ **adversarial-verify stage** (independent refute pass per finding — *fan-out audit
findings invert*, [[feedback_handverify_audit_findings_and_compile_blindspots]]) →
**my hand-check** of the confirmed set → per-document findings registers +
master register.

**Integration points:** each register lands in that manual's `audit/`; the master
register drives §6. Any P2KB (YAML) conflict a finder surfaces routes to
`P2KB-CORRECTION-FINDINGS.md` per [[project_p2kb_corrections_register]].

**Verification:** normal — every in-scope doc has a register (findings or a clean
attestation); edge — a doc with zero findings still emits an explicit "audited, clean"
record (silence ≠ audited); error — an inverted finding (correct→flagged-wrong) is
killed by the adversarial pass + hand-check before it can drive a fix; **no silent
caps** — if any doc/region is not fully covered, it is logged, not omitted.

## 6. Class-wide correctness sweep A — fabrications & factual errors

**Why:** fix all occurrences in all documents (not just the reported spots).

**Current-code starting point (the PASM2 seed):** `chapter-03-flags.md:180` (TEST\*),
`:207`+`:223` (cycle-vs-count + RDLONG example), `:420` (ABS fabrication);
`chapter-04-timing.md:469` (hub-pipelining fabrication) — plus every finding §5
confirms across all docs.

**Target:** for each confirmed finding, repair every occurrence, each carrying its
silicon→YAML→doc proof. Rewrite the two fabrication sections (§3.5.4 ABS around
"C = original sign / restore-sign idiom"; §4.6.2 hub around FIFO/SETQ reality, pointing
to the already-correct CORDIC §4.6.3). Fix cycle counts (→6), replace the RDLONG
constant-timing example with a constant-cost op, reword the TEST\* glob.

**Verification:** normal — each corrected claim re-verifies against the trusted source;
edge — the manual's *own* §3.4.4 ABS row (already correct) is left intact and now
agrees with the rewritten §3.5.4; error — no fix introduces a new unsourced claim
([[feedback_no_unsourced_claims]]).

## 7. Class-wide correctness sweep B — operator notation (document + YAML) — PLAN-GATED

**Why:** the agent-facing half — a stray `=` for a comparison can steer agent
code-gen to the wrong operator.

> **This work package edits many YAML files — the plan-before-YAML gate applies
> ([[feedback_plan_before_yaml_changes]]). The file table + per-decision flags below
> must be confirmed before any YAML edit begins.**

**File table (initial — finalized after the §5 grep across all docs):**

| Surface | Scope | Change |
|---------|-------|--------|
| `deliverables/ai/P2/**/*.yaml` — flag-condition fields | ~61 files w/ `z:/c: … = 0` comparisons | comparison `=` → `==` |
| same YAMLs — "receives" fields (`c: C = D[31]`, `…then D = D - S`) | subset | **LEAVE `=`** (behavior assignment) |
| Manual §3.4 flag tables + all docs' behavior tables | per §5 | comparison cells → `==`, add behavior-notation legend |
| Spin2 *code examples* across docs | per §5 | bare `=` → `:=`/`==` (real source) |

**Design decisions to flag (await per-decision confirm):**
- Predicate-vs-receives is a **per-occurrence** judgment, never a blind replace.
- Whether the behavior-notation legend is added once per manual (recommend: yes, short).
- Confirm PASM2 CON-block `=` stays (legit assembler syntax).

**Integration points:** after YAML edits — `validate-yaml-syntax.py` +
`validate-crossref-keys.py` + index regen (Path-B two-commit,
[[reference_index_generator_post_commit]]).

**Verification:** normal — post-sweep, every YAML `=` is either "receives" or CON,
and every comparison is `==`; edge — a "receives" `=` is unchanged; error — no
cross-reference broken, index regenerates clean, `p2kb_refresh` serves the corrected
fields.

## 8. Re-render affected manuals (no release)

**Why:** prove each modified manual regenerates clean; leave it prepared. **Release
is deferred to the coordinated program sweep.**

**Target:** for each manual touched by §6/§7, run `prepare-manual` (refresh workspace
from opus-master, escape LaTeX, stage changed files) and regenerate on the Forge;
**verify each render** (page count, outline, key sections, compile log — guard silent
content-drop). Do **not** bump versions or promote to deliverables.

**Verification:** normal — every modified manual renders compile-clean with corrected
sections text-present; edge — a manual only touched by the operator legend still
renders + verifies; error — silent content-drop caught by page-count/outline check
([[reference_forge_silent_content_drop]]).

## 9. YAML correctness release-prep (separate track)

**Why:** the operator YAML corrections ship on the KB track, not the manual track.

**Target:** stage the KB release for the §7 YAML changes (validate + index regen +
`p2kb_refresh` + MCP restart + content-probe). Release-number and timing per
`release-yamls`.

**Verification:** normal — validators green, index clean, MCP serves corrected fields;
edge — an app-note companion field touched by the sweep re-serves correctly; error —
DoD validation (`validate-dod-release.py`) blocks on any unsourced/broken ref.

---

## Exit note

Deliverables 1–9 constitute Group 1. Groups 2–3, the DEBUG-window ZIP pass, and the
coordinated release sweep are tracked as program context above and are **not** closed
by this plan. The re-rendered-but-unreleased manuals wait for that coordinated sweep.
