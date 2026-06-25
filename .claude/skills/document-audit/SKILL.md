---
name: document-audit
description: >-
  Audit a P2 manual against the current YAML/KB HEAD and itself, at a chosen
  depth, producing a consolidated findings report — and, at release depth, ENFORCE
  the publish gate. Use when the user says "audit the <manual>", "re-audit <manual>
  against the KB", "is <manual> ready to release", runs a periodic/quarterly audit,
  re-audits after a YAML change-set lands, or invokes /document-audit. This is the
  central, manual-agnostic audit body; per-manual specifics (sources, code-line
  budget K, doc-class, fragile areas) come from that manual's MANUAL-DESCRIPTOR.md
  overlay, resolved from the active_element pointer. Owns the YAML-HEAD drain gate
  (no publish while actionable YAML corrections are pending) and the changeset-
  integrity (delta-since-last-published) audit. Finds and reports; resolving findings
  is document-finalize, releasing is release-manual.
---

# Document Audit — the manual release-gate audit body

This is the **central, manual-agnostic** audit procedure. It supersedes the per-manual
`AUDIT-PROCESS.md` copies (which were ~98% identical — see the consolidation note in §11).
The procedure lives here once; everything that varies per manual lives in that manual's
**`MANUAL-DESCRIPTOR.md`** overlay (§0, §10). Improve the method here and every manual
inherits it — no copy drifts.

**Companion methodology:** for deeper theory (truth-matrix construction, hallucination
taxonomy, lessons learned), see `engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md`.
This skill is the *operational* checklist; the methodology doc is the *why*. It is linked,
not inlined.

**What this skill does NOT do:** it FINDS and REPORTS. Resolving findings as a batch +
re-rendering is `document-finalize`; promoting to deliverables is `release-manual`. At
**release-gate depth** this skill produces the GO/NO-GO the release skill blocks on.

---

## 0. Resolve the target and load its overlay

1. Determine the manual. From `active_element` (`mcp__todo-mcp__context_get key:"active_element"`,
   form `manual:<slug>`) or from what the user names. The manual folder is
   `engineering/document-production/manuals/<slug>/`.
2. Read that manual's **`MANUAL-DESCRIPTOR.md`** (the overlay). It binds:
   - `doc_class` — `reference` (YAML-backed) | `behavior` (source-extraction-backed) | `tutorial`
   - `code_line_budget_K` — the per-manual code-line width budget (Dimension #3b)
   - `last_published_tag` — baseline for the changeset-integrity audit (Dimension #15)
   - `authoritative_sources` — or a pointer to `./creation-guide.md`'s source list
   - `guide_paths` — `./creation-guide.md`, `./voice-guide.md`, `./style-guide.md`
   - `high_risk_tables` — this manual's transposition-prone tables (Dimension #7)
   - `fragile_areas` — known-thin / historically-buggy sections to weight heavily
3. If the manual has **no `MANUAL-DESCRIPTOR.md`**, run the **onboarding** in §10 first (build it),
   then proceed. Never guess these bindings — they are data, sourced from the manual's own guides.

> The descriptor is **thin and non-duplicating**: it names what isn't already captured and
> *points at* `creation-guide`/`voice-guide`/`style-guide` for the rest. It is a per-manual
> **descriptor** the whole manual-skill family (`prepare-manual`, `release-manual`,
> `document-finalize`) may read — audit is its first consumer.

---

## 1. Depth modes

Pass `--depth` (default `systematic`). Same dimensions, different reach (maps to
`TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md` Part VIII):

| Depth | Use | Reach |
|-------|-----|-------|
| `smoke` | quick sanity after a small edit | Themes C, D, F greps + Dimension #13; no full claim trace |
| `systematic` | default periodic / post-YAML re-audit | all dimensions; sample-then-expand on Theme A |
| `deep` | exhaustive ("full audit = exhaustive") | every claim, every chapter; fan out per theme/letter-range |
| `release-gate` | before publish | `deep` **plus** the §2 YAML-HEAD drain gate (blocking) **plus** Dimension #15 changeset integrity |

**"Full audit" means exhaustive, not a sample** (memory rule): at `deep`/`release-gate`,
every claim in every chapter is traced — re-audit when KB sources OR the model improve.

---

## 2. The YAML-HEAD drain gate  (release-gate depth — BLOCKING)

**A manual does not publish while there are *actionable* pending YAML-HEAD changes.**
A release is a rare, high-energy event (7 manuals, infrequent updates); we use that motivation
as **pressure to flush the KB current for the dynamic agents who consume the YAMLs live**.
Pending YAML = information not reaching those agents. So draining the register is a release
precondition — not domain-scoped, but **global**, because stale YAML is harm regardless of
which manual triggered the flush. Because releases are rare, this is a healthy sawtooth
(backlog accumulates, each release drains it to zero), not a deadlock.

**Predicate (must be GREEN to publish):** no *actionable* open items in the corrections
register `engineering/operations/P2KB-CORRECTION-FINDINGS.md`.

- **Actionable** = resolvable from in-repo golden sources (compiler / hardware-verified ledger /
  Silicon Doc / authoritative-derived YAML). These MUST land (fix YAML → release-yamls / commit)
  before this manual publishes. `NEEDS-VERIFICATION` whose sources are in-repo is **actionable**
  — "NEEDS-VERIFICATION is not a ship license."
- **Blocked-on-external** = genuinely cannot be resolved here (awaiting Chip Gracie / a hardware
  test / an expert answer — e.g. an IOSP expert-queue item). These are **explicitly parked with a
  reason**, stay visible in the register, and do **NOT** gate.

**Procedure:**
1. Read the register. Classify every open item: `actionable` vs `parked-on-external (reason)`.
2. If any `actionable` remain → gate is **RED**. Report them; the manual cannot publish until
   they are landed (hand off to `yaml-knowledge-base-maintenance` + `release-yamls`), then
   **re-audit against the new HEAD**.
3. If only `parked-on-external` remain → gate is **GREEN**; list the parked items in the report
   so the reader sees what's deliberately deferred and why.

> The audit and the register form a loop: this audit (Theme A / Dimension C) *creates* register
> entries when it finds a KB defect. Those new in-domain entries are `actionable` and join the
> drain. That is intended — the audit feeds the register; the register state gates the publish.

### Two directions (this gate is only one of them)

The manual↔YAML relationship runs both ways, off the **same join index** — each manual's
`MANUAL-DESCRIPTOR` source list:

- **Manual → YAML (this §2 gate):** a manual release drains *all* actionable pending YAML.
  Manual-triggered. Lives here.
- **YAML → Manual (impact survey):** YAML changes arrive independently (consumers report issues →
  research → apply head change → publish — no manual in view). When that lands, survey *which*
  manuals derive from the changed YAML paths and flag them for re-audit. YAML-triggered, and
  **cross-manual** — so it does NOT live in this single-manual skill. Its home is **`release-yamls`**
  §8 (the YAML head's publish moment), computed by intersecting the YAML delta against every
  `MANUAL-DESCRIPTOR`'s declared sources — the descriptors seeded by this skill are the data it
  needs.

---

## 3. Authoritative sources — and the two grounding models

This audit verifies the manual against its sources. **The manual's `./creation-guide.md` is the
source-of-truth list** (the descriptor points at it). Determine the grounding model from
`doc_class` before starting:

- **`reference` (YAML-backed)** — instruction / method references (PASM2, Spin2, Smart Pins).
  Source of truth is KB YAML under `deliverables/ai/P2/language/`, plus the Silicon Doc and the
  encoding spreadsheet. Dimensions A, B, #1, #5, C verify against that YAML.
- **`behavior` (source-extraction-backed)** — how a subsystem *operates* (Single-Step Debugger,
  Debug Windows). Little/no instruction YAML; the truth is the reverse-engineered / extracted
  reference — a Theory-of-Operations doc, Pascal/PNut source extractions, per-feature study docs
  — **as enumerated in `./creation-guide.md`**. Here "the YAML" in the dimensions below means
  "the manual's cited extraction/source documents," and the `p2kb-mcp` caveat does not apply.
- **`tutorial`** — teaching docs (deSilva-style). Factual dimensions still apply against the
  reference KB, but Dimension #9 permits tutorial voice (the `voice-guide` says so).

For YAML-backed manuals, the source tiers:

| Source tier | Typical location | Notes |
|-------------|------------------|-------|
| Primary (silicon truth) | `engineering/ingestion/sources/silicon/` | Hardware behavior is ground truth |
| Primary (empirical) | `engineering/ingestion/external-sources/hardware-verification/` | 🏆 top of trust chain |
| Primary (encoding) | P2 instruction spreadsheet (ingested) | Encoding authority |
| Primary (compiler) | `pnut_ts` behavior | Implementation validation |
| Derived (KB YAML) | `deliverables/ai/P2/language/` (`pasm2/`, `spin2/`, `fundamentals/`) | Structured truth KB consumers read |
| Target | `./opus-master/` | The manual being audited |

**Important:** `p2kb-mcp` returns the *published* index, which lags local edits until commit +
push + republish. **Always read YAML directly from disk** under `deliverables/ai/P2/language/`
mid-audit — do not trust `p2kb_get` for currency.

---

## 4. Pre-audit setup

1. **Baseline** — most recent `./audit/periodic-audit-*.md` date (or `last_published_tag` for a
   release-gate run).
2. **YAML change-set** — `git log --since=<baseline> -- deliverables/ai/P2/language/` (drives #1, C).
3. **Manual change-set** — `git log --since=<baseline> -- ./opus-master/` (and, for #15, the diff
   from `last_published_tag`).
4. **Prior findings** — read every `./audit/` file newer than baseline; open items feed #12.
5. **Guides** — read `./creation-guide.md`, `./voice-guide.md`, `./style-guide.md` per the descriptor.

Stage today's report: `./audit/periodic-audit-YYYY-MM-DD.md` (release-gate runs may name it
`./audit/release-gate-YYYY-MM-DD.md`).

---

## 5. Audit dimensions

Seventeen dimensions in seven themes. Every dimension produces findings into §7.

### Theme A — Factual Grounding (the heart of the audit)

**Dimension A — Manual content vs current YAML.** For every factual claim in `./opus-master/`,
confirm it in the relevant YAML. Section by section, trace each claim to a YAML field. Classify
`VERIFIED`/`MODIFIED`/`UNVERIFIED`/`FABRICATED`. **Fix rule:** when a fact is wrong, sweep for
*every* occurrence and fix all of them — don't pause to ask scope (bad info is outlawed,
fix data-set-wide).

**Dimension B — Voicing factually anchored to YAML.** The descriptive *framing*, not just literal
claims, must stay grounded. Place the YAML `description:` next to the manual prose; check for
capability inflation, vague verbs replacing precise ones, invented secondary behaviors. Propose
specific rewording.

**Dimension #1 — KB delta since baseline.** For each touched YAML, diff against baseline;
categorize (new field / value change / removal / new or removed YAML file). Each delta becomes a
verification question: does the manual reflect it?

**Dimension #5 — Quantitative claim verification.** Every number is high-bug-density: clock counts,
bit positions / field widths, addresses, asserted counts ("491 instructions", "8 cogs", "64 Smart
Pins", "512KB hub"). grep digits/ranges; cross-check each. **Forbidden (memory):** no
bytecode-interpreter clock timings for Spin2 methods (cite underlying PASM or remove; never "varies
with release"); no compiler bytecode values / `bc_`-prefixed symbols (describe behavior, not symbol).

### Theme B — Coverage

**Dimension C — Missing content.** Anything in YAML the manual *should* cover (per `creation-guide`
scope) but doesn't. List gaps with proposed placement and rationale.

**Dimension #12 — Prior audit-findings closure.** For every prior `./audit/` report, list findings
still open; verify each was actually applied in current `./opus-master/`. Status: `Closed (applied)`
/ `Closed (n/a)` / `Still open — escalate` / `Re-opened (regression)`. **A reopened finding
escalates one severity level.**

### Theme C — Hallucination & Drift

**Dimension #4 — Hallucination red-flag sweep.** grep the patterns below across `./opus-master/`;
each hit must cite a backing source or it is `FABRICATED` until proven otherwise. Sweep every
occurrence.

| Pattern | Risk |
|---------|------|
| "also provides" / "side effect" | HIGH — fabricated secondary capability |
| "eliminates" | HIGH — unverified optimization claim |
| "synchronizes" / "synchronization mechanism" | CRITICAL — past fabrications used this exact framing |
| "automatically" / "mechanism for" | MEDIUM — hand-waving |
| "additionally" / "furthermore" | MEDIUM — often precedes invented extras |
| "enables" / "allows" / "can be used to" (vague) | MEDIUM |

### Theme D — Linkage & Examples

**Dimension #2 — Cross-reference integrity.** Every "see Chapter X" / "see Appendix Y" /
"Related: FOO" / "§N.N" resolves to something that still exists with that name. YAML cross-refs use
full paths (CLAUDE.md rule #7). **Never delete a reference** — redirect to where the concept now
lives.

**Dimension #3 — Code example currency.** Extract every PASM2/Spin2 fenced block, compile against
`pnut_ts`. **Compile DEBUG-window code with `pnut-ts -d`** (without `-d` the compiler ignores
`debug()` contents — a no-`d` pass is a false pass). A failed example is a finding — propose a
corrected version, not a removal.

**Dimension #3b — Code-line-length budget.** Every PASM2/Spin2 code line ≤ the descriptor's
`code_line_budget_K`. Run `audit-code-line-length.py` against K (LaTeX `\item`/keyconcepts lines
are prose, not code — exclude). Over-budget lines are an authorship defect; never reintroduce
breaklines — shorten the content.

### Theme E — Consistency

**Dimension #6 — Internal consistency.** No fact stated two ways (tables vs prose, narrative vs
example, summary vs detail). Common failures: shifted table column; instruction described one way
in a chapter, another in its A–Z entry; example using a syntax the prose calls invalid.

**Dimension #7 — Structural table column-alignment.** **35% of bugs in the PASM2 100% audit were
column-transposition errors.** For each table named in the descriptor's `high_risk_tables`, verify
every row against its originating YAML field; confirm header order matches data order on every row;
**spot-check the first cell of every row** (where transposition surfaces).

**Dimension #8 — Terminology conformance.** Canonical terms per `./voice-guide.md` / `./style-guide.md`
used consistently (e.g. "cog" lowercase in prose, not "CPU"/"COG"; "C flag" vs "carry"). Build the
canonical list from the guides; grep non-canonical variants.

**Dimension #13 — Front matter / changelog accuracy.** Version matches latest tag; asserted counts
match reality; dates match last substantive change; **changelog entries reflect actual changes and
cover every unreleased effort since `last_published_tag`** (not aspirational). (See `audit-changelog`
for the deep changelog cross-reference.)

### Theme F — Conformance

**Dimension #9 — Voice / tone conformance.** Per `./voice-guide.md`. **Derive the grep pattern set
from the voice-guide's "Never Do" table (its §4.2) — do NOT hardcode a sample list here, so this
dimension can never drift from the guide.** The voice-guide is the single source of banned patterns;
read it and grep each. (Patterns the guide typically bans: hedging; tutorial voice unless
`doc_class: tutorial`; informal "basically/just/simply"; vague "works like X"; marketing /
superlatives; hardware-correctness reassurance; vague application-domain justification; restating a
fact already stated.) Each hit → finding + proposed rewording.

**Dimension #10 — Structural conformance.** Every required section per `./creation-guide.md` present
and in prescribed order. Missing / out-of-order / silently-renamed sections are findings.

**Dimension #11 — Authoring scaffolding leftovers.** grep `TODO`/`FIXME`/`XXX`/`HACK`/`PLACEHOLDER`/
`TBD`/`<!-- NEEDS_VERIFICATION -->`/`<!-- DRAFT -->`, stale commented-out paragraphs, inadvertent
`*.backup-*` references. Each is a finding.

**Dimension #14 — Non-native comment-style leakage.** A PASM2/Spin2 manual uses only PASM2/Spin2
comment syntax (`'`, `{ }`, `{{ }}`) — even in pseudocode/antipattern blocks. Forbidden in any code
block: `//`, `/* */`, `;`, line-leading `#`+word. Sweep: `grep -nE "//" ... | grep -v "https*://"`;
`grep -nE "/\*"`; `grep -nE "^\s*;"`. Inside a code/`:::` block → finding; prose/URL → ignore. Fix
the syntax (won't compile) or convert to `'` (pseudocode). Reason: mixed comment styles teach the
eye to accept foreign syntax, then the reader writes `// note` and gets an unexplained error.

### Theme G — Changeset Integrity (release-gate; NEW)

**Dimension #15 — Delta since last published.** Baseline = the descriptor's `last_published_tag`.
Diff `git diff <tag>..HEAD -- <manual folder>`. The diff is the *complete* record of what will be
new in the next published artifact. Two checks:

- **Scope completeness** — every file in the diff is one we intended to touch. The "expected set"
  is the **union of all unreleased efforts** (sprint docs + changelog lines + commit messages) since
  the tag — not just the latest sprint. Any file tracing to **no** documented effort is a finding
  ("worry and review").
- **Per-hunk traceability + correctness** — every hunk maps to a documented intended change AND is
  itself correct. Unmappable or incorrect hunks are findings.

**Output:** a classification of every changed file → `intended (cite the effort)` / `errant
(finding)`. This dimension is the mechanical guarantee that the release contains exactly what we
believe it contains and nothing errant.

**EXHAUSTIVE — never sampled.** Itemize **every hunk** in the diff; spot-checking a subset of
files/hunks is NOT acceptable here. A change that "got away from us" hides precisely in the hunk
you didn't read, so file-level attribution ("this file is the lowercase sweep") is insufficient —
a stray non-lowercase edit could ride inside a file you attributed to the sweep. Read every hunk,
attribute every hunk. For a large diff, fan out by file-range to parallel agents, then verify each
agent covered its full range (count hunks claimed vs `git diff` hunk count). If the changeset is
still growing (e.g. a drain is in progress), run #15 against the FINAL pre-publish state — but when
run, it is 100%.

---

## 6. Finding classification

Two attributes per finding. **Status** (against source): `VERIFIED` / `MODIFIED` / `UNVERIFIED` /
`FABRICATED`. **Severity** (reader impact): `CRITICAL` (fundamentally wrong; user failure) /
`HIGH` (affects correct usage) / `MEDIUM` (misleading but workaround) / `LOW` (cosmetic) / `INFO`
(improvement). Reopened findings (#12) escalate one level. A CRITICAL Theme-A finding pauses the
audit and triggers an immediate fix discussion — never buried in a long report.

---

## 7. Report template

Single consolidated file `./audit/periodic-audit-YYYY-MM-DD.md` (or `release-gate-YYYY-MM-DD.md`):

```markdown
# <Periodic|Release-Gate> Audit — <manual> — YYYY-MM-DD
**Auditor:** <name/agent>   **Depth:** <smoke|systematic|deep|release-gate>
**Baseline:** <prior audit date | last_published_tag>
**YAML range:** <rev range>   **Manual range:** <rev range>

## Gate status (release-gate only)
- YAML-HEAD drain gate: GREEN / RED  — actionable pending: <n> ; parked-on-external: <n>
- Changeset integrity (#15): clean / <n> errant files

## Summary
| Theme | Findings | Crit | High | Med | Low | Info |
|-------|----------|------|------|-----|-----|------|
| A Factual Grounding | | | | | | |
| B Coverage | | | | | | |
| C Hallucination & Drift | | | | | | |
| D Linkage & Examples | | | | | | |
| E Consistency | | | | | | |
| F Conformance | | | | | | |
| G Changeset Integrity | | | | | | |
| **Totals** | | | | | | |

## Findings   (one subsection per dimension, with located rows + proposed fixes)
## Recommended Actions (ranked by severity)
## Sign-off
- [ ] All CRITICAL have a tracked fix
- [ ] YAML-HEAD drain gate GREEN (release-gate)
- [ ] Changeset integrity clean (release-gate)
- [ ] Prior-audit follow-up complete (#12)
- [ ] Report committed to ./audit/
- [ ] If fixes touch YAML, downstream consumers identified (Trust Chain)
```

---

## 8. Workflow

```
0. Resolve target + load MANUAL-DESCRIPTOR.md (§0); run §10 onboarding if absent
1. Pre-audit setup (§4) — baseline + change sets + guides
2. release-gate ONLY: evaluate the YAML-HEAD drain gate (§2). RED → stop, report, drain first.
3. Theme A (factual grounding) — priority block
4. Themes B → C → D → E → F
5. release-gate ONLY: Theme G changeset integrity (#15)
6. Triage by severity → ranked action list
7. Commit report to ./audit/
8. Open follow-up items for every CRITICAL/HIGH (hand to document-finalize to resolve)
```

**Parallelization:** themes are largely independent — dispatch one Explore/agent per theme (or per
instruction-letter-range) for large manuals at `deep`/`release-gate`. **Verify a delegated agent's
COMPLETION, not just its findings** — grep-count inserted/changed markers per file vs expected
before trusting "done" (insert-agents over-report). **Hand-verify audit findings** — fan-out
findings can invert (doc-right/YAML-wrong), cite community-tier sources as primary, or name
non-existent constants; `pnut_ts` has blind spots (operand-order, DIRH/DIRL-not-Spin2).

---

## 9. Fix-side rules

> **This skill does not execute these.** It FINDS and REPORTS (see the boundary at the top);
> `document-finalize` resolves the findings and applies the rules below. They live here so the
> audit report can name the standard each finding will be held to when it is fixed.

- **Edit the opus-master, never the workspace render** — the render is generated and overwrites edits.
- **Edit in place** — no `-fixed`/`-v2`/`-new` suffixes (sacred rule #5).
- **Sweep wide** — fix every occurrence of a bad fact in one pass.
- **Protocol layer first** — a driver-domain fix (SD/SPI/I²C/UART) often cascades from the protocol page.
- **Fix at the layer where truth lives** — if the manual is right and the YAML wrong, fix the YAML
  (route via `yaml-knowledge-base-maintenance`; that is also what feeds the §2 drain gate).
- **No YAML generators** — per-content YAML edits are safe and won't be overwritten.

---

## 10. Onboarding a new manual — build its MANUAL-DESCRIPTOR.md

When a manual has no descriptor, create `engineering/document-production/manuals/<slug>/MANUAL-DESCRIPTOR.md`.
This is **form-filling against a fixed schema**, not discovery — keep it thin and point at the
existing guides rather than duplicating them. Populate from the manual's own `creation-guide.md`
(sources, scope, K) and folder:

```markdown
---
manual_slug: <slug>
doc_class: reference | behavior | tutorial      # selects the §3 grounding model + #9 tutorial-voice
code_line_budget_K: <int>                        # from creation-guide; Dimension #3b
last_published_tag: <git tag or "unreleased">    # baseline for Dimension #15
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md
  style_guide: ./style-guide.md
authoritative_sources: see ./creation-guide.md   # or an explicit tier list if it diverges
high_risk_tables:                                 # transposition-prone tables, Dimension #7
  - <table name + where>
fragile_areas:                                    # known-thin / historically-buggy sections
  - <section + why>
---

# <Manual> — Descriptor

Thin per-manual overlay read by document-audit (and prepare-/release-/finalize-manual).
Everything not listed above is inherited from the central skill body + the guides above.
```

If a field is genuinely unknowable from in-repo sources, that absence is itself a finding — record
it; do not invent a value.

**Flag (do NOT remove) a superseded `AUDIT-PROCESS.md`.** If the manual folder still carries an
`AUDIT-PROCESS.md` (the old per-manual process doc this skill replaces), note it in the onboarding
output as "superseded by document-audit — queue for the consolidation pass." Do **not** delete it
here: onboarding (like an audit run) is side-effect-free on repo structure. Retirement happens only
in the consolidation pass (§11). And never confuse `AUDIT-PROCESS.md` (the process doc — retire it)
with the `./audit/` folder (findings/run history — KEEP; Dimension #12 reads it).

---

## 11. Companion documents & consolidation note

- `engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md` — deeper methodology
  (truth-matrix, hallucination taxonomy, lessons). Linked, not inlined.
- `./creation-guide.md` — source authority + write-time verification for *this* manual.
- `./voice-guide.md`, `./style-guide.md` — conformance rules for #8, #9, #10.
- `./audit/` — prior findings; check before re-finding.
- `audit-changelog` skill — deep changelog readiness cross-reference (feeds #13).

**Consolidation note (in progress):** **three** manuals still carry a near-identical
`AUDIT-PROCESS.md` (debug-window, IOSP, deSilva — debug-window's is the only one with
the two-grounding-models improvement, which MUST be carried across before it is retired; the
rest are stale). Those copies are **superseded by this skill**. (Assembly retired 2026-06-25:
carry-across verified — all 16 dimensions present here — archived to its git-ignored `./archive/`;
done as we release each manual that still has one.) Retiring the rest is a separate, deliberate
consolidation pass — **never a side effect of an
audit or onboarding run** — and per manual it goes: (1) **carry-across check** — confirm this skill
+ the manual's descriptor capture everything in that copy (don't delete what wasn't migrated;
surface any gap); (2) **archive, don't hard-delete** — move the file to a git-ignored `./archive/`
(git history is the real record; the archive-locally rule); (3) one manual at a time, reviewed.
This is the `overlay-reconcile` motion (retire local docs as central catches up). Scope: only
`AUDIT-PROCESS.md` — the `./audit/` findings/run history is untouched.
