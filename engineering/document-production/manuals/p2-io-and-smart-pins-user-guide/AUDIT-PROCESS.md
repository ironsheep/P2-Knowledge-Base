# Manual Periodic Audit Process

**Purpose:** A reusable, periodic-audit process document. Drop this file at the root of any manual folder under `engineering/document-production/manuals/<manual-name>/` and it works against that manual — all paths in this document are **relative to the manual folder root** unless otherwise noted.

**Reusability rule:** This document references files inside its own manual folder (e.g. `./opus-master/`, `./audit/`, `./creation-guide.md`, `./voice-guide.md`, `./style-guide.md`) and never hard-codes a particular manual's name. Each manual provides its own creation-guide / voice-guide / style-guide — the audit reads those *for that manual*.

**Companion methodology:** This document is the operational, recurring-audit checklist. For deeper background on hallucination detection, truth-matrix construction, and audit theory, see `engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md`.

---

## 1. When to Run

Run a periodic audit when **any** of these are true:

- A meaningful set of YAML changes has landed since the last audit (the *primary* trigger)
- The manual has had non-trivial content changes since the last audit
- A user reports an inaccuracy (audit at least the surrounding domain)
- Before a release / version bump
- On a calendar cadence (recommended: once per quarter, or before each Parallax silicon/compiler release)

**Quality philosophy reminder (from CLAUDE.md):** We are never in a rush. Complete over partial. The audit gets done *thoroughly* or it gets postponed — never half-finished.

---

## 2. Authoritative Sources

This audit verifies the manual against its sources. **Each manual's `./creation-guide.md` is the source-of-truth list for that manual.** Do not duplicate that list here — read it.

For reference, P2 manuals typically cite:

| Source tier | Typical location | Notes |
|-------------|------------------|-------|
| Primary (silicon truth) | `engineering/ingestion/sources/silicon/` | Hardware behavior is ground truth |
| Primary (encoding) | P2 spreadsheet (ingested) | Encoding authority |
| Primary (compiler) | `pnut_ts` behavior | Implementation validation |
| Derived (KB YAML) | `deliverables/ai/P2/language/` (`pasm2/`, `spin2/`, `fundamentals/`) | Structured truth used by KB consumers |
| Target | `./opus-master/` | The manual being audited |

**Important:** `p2kb-mcp` returns the *published* index, which can lag local YAML edits until commit + push + republish. When auditing, **always read YAML directly from disk** under `deliverables/ai/P2/language/` — do not trust `p2kb_get` mid-audit.

---

## 3. Pre-Audit Setup

Before starting, gather these inputs:

1. **Last audit date** — check `./audit/` for the most recent `periodic-audit-*.md` file; record its date as the audit baseline.
2. **YAML change-set** — `git log --since=<last-audit-date> -- deliverables/ai/P2/language/` to list YAML touched since last audit. This drives dimensions #1 and C below.
3. **Manual change-set** — `git log --since=<last-audit-date> -- ./opus-master/` to list manual files touched since last audit.
4. **Prior findings** — read every audit file in `./audit/` newer than the previous baseline. Items still open feed dimension #12.
5. **This manual's guides** — read `./creation-guide.md`, `./voice-guide.md`, `./style-guide.md` to load the conformance rules for this audit pass.

Stage today's report file: `./audit/periodic-audit-YYYY-MM-DD.md` — populated as the audit progresses.

---

## 4. Audit Dimensions

Seventeen dimensions, grouped into six themes. Every dimension produces findings into the consolidated report (§6).

### Theme A — Factual Grounding (the heart of the audit)

#### Dimension A: Manual content vs current YAML

For every factual claim in `./opus-master/`, confirm the same fact in the relevant YAML.

- **Method:** Section by section, list extracted claims and trace each to a YAML field (e.g. `add.yaml` → `flags:` / `clocks:` / `encoding:`).
- **Classification:** `VERIFIED` / `MODIFIED` / `UNVERIFIED` / `FABRICATED` (per `TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md` §5).
- **Fix rule:** When a fact is wrong, sweep for *every* occurrence of that fact across the manual and fix all of them — do not pause to ask about scope. See memory rule: bad info is outlawed; fix data-set-wide.

#### Dimension B: Voicing factually anchored to YAML

The *prose voice* — not just literal claims, but the descriptive framing — must remain grounded in YAML. If the YAML says "stores the sum of Dest and Src in Dest" and the manual says "performs addition with optional overflow handling that may signal carry", that's voicing drift even if technically not contradictory.

- **Method:** For each instruction/method, place the YAML `description:` next to the manual prose and check for: capability inflation, vague verbs replacing precise ones, or invented secondary behaviors.
- **Fix rule:** Propose specific rewording that brings the prose back into alignment with the YAML's literal claims. Submit as a finding with proposed text.

#### Dimension #1: KB delta since last audit

What changed in YAML since the last audit baseline (gathered in §3 step 2)?

- **Method:** For each touched YAML file, diff against its state at the baseline. Categorize changes as: new field, value change, removal, new YAML file (new instruction / method / construct), removed YAML file.
- **Output:** A delta inventory. Each delta then becomes a verification question for the manual: does the manual reflect this?

#### Dimension #5: Quantitative claim verification

Every number is a high-bug-density target. Audit:

- Clock counts (per-instruction timing, hub-window cycles, latencies)
- Bit positions / field widths (encoding fields, flag bits, immediate ranges)
- Addresses (register addresses, special-register `$1F0-$1FF`, hub regions)
- Counts asserted in prose / front matter ("359 instructions", "8 COGs", "64 Smart Pins", "512KB hub")

- **Method:** grep the manual for digits and ranges; cross-check each against YAML / silicon doc.
- **Forbidden under existing rules (from auto-memory):**
  - Do **not** publish bytecode-interpreter clock timings for Spin2 methods — cite the underlying PASM or remove the field. Never use "varies with release" framing.
  - Do **not** publish compiler bytecode values or `bc_`-prefixed symbol names — they change with compiler revs. Describe behavior, not the symbol.

### Theme B — Coverage

#### Dimension C: Missing content

Anything in YAML that the manual *should* cover but doesn't.

- **Method:** Enumerate YAML elements expected to appear in this manual (per `./creation-guide.md` scope). Walk the manual to confirm presence of each. List gaps with proposed placement (which chapter / appendix / section it belongs in).
- **Output for each gap:** `[element name] — proposed location: [chapter X.Y or appendix Z] — rationale: [why it belongs here]`.

#### Dimension #12: Prior audit-findings closure

For every audit report in `./audit/` since this manual's first audit, list findings still marked open. Verify whether each has actually been applied in current `./opus-master/` content.

- **Output:** Per-finding status — `Closed (applied)` / `Closed (no longer applicable)` / `Still open — escalate` / `Re-opened (regression)`.
- **A reopened finding is more serious than a new one** — flag it at higher severity.

### Theme C — Hallucination & Drift

#### Dimension #4: Hallucination red-flag sweep

Linguistic patterns that historically precede fabricated content. From `./creation-guide.md` §4A.2 and `TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md` §2.1:

| Pattern | Risk |
|---------|------|
| "also provides" | HIGH — fabricated secondary capability |
| "side effect" | HIGH — invented behavior |
| "eliminates" | HIGH — unverified optimization claim |
| "synchronizes" / "synchronization mechanism" | CRITICAL — past fabrications used this exact framing (HUBSET) |
| "automatically" | MEDIUM — automatic behavior must be documented |
| "mechanism for" | MEDIUM — hand-waving |
| "additionally" / "furthermore" | MEDIUM — often precedes invented extras |
| "can be used to" (vague) | MEDIUM |
| "enables" / "allows" (vague capability) | MEDIUM |

- **Method:** grep each pattern across `./opus-master/`. For each hit, locate the source backing the claim. If no source can be cited, the claim is `FABRICATED` until proven otherwise — **never escalate severity downward without a citation**.
- **Sweep rule:** "We always do complete work" — sweep every occurrence; don't stop at the first one.

### Theme D — Linkage & Examples

#### Dimension #2: Cross-reference integrity

Every internal link must resolve.

- **In-manual:** Every "See Chapter X" / "see Appendix Y" / "Related: FOO" points to something that still exists at that location with that name.
- **YAML cross-refs (if manual cites them):** Use full paths per CLAUDE.md rule #7 (e.g. `language/spin2/methods/exp.yaml`, not bare `EXP`).
- **Never-delete rule:** If a referenced target has moved, find where the concept is *now* documented and redirect — do not delete the reference. See CLAUDE.md sacred rule #7.

#### Dimension #3: Code example currency

Every code example in `./opus-master/` must compile against current `pnut_ts` and use non-deprecated syntax.

- **Method:** Extract every fenced code block tagged as PASM2 / Spin2, write to a temp file, attempt compile with `pnut_ts`. Record pass/fail per example.
- **Failure handling:** A failed example is a finding — propose a corrected version, not just a removal. If the example demonstrates a concept the user needs, fix it; if obsolete, replace with a current example illustrating the same point.

### Theme E — Consistency

#### Dimension #6: Internal consistency

The manual must not contradict itself.

- **Method:** For each fact that appears in more than one place (tables vs prose, narrative vs example, summary vs detail), confirm all instances agree word-for-word on the facts and as closely as practical on wording.
- **Common failure modes (from prior audits):** Table column shifted from header; instruction described one way in Chapter 3, another way in its A–Z entry; example uses a syntax variant the prose says is invalid.

#### Dimension #7: Structural tables column-alignment

Every domain-specific structural table is high-risk. **35% of bugs in the PASM2 100% audit were column-transposition errors.** Targets vary by manual:

| Manual type | High-risk table |
|-------------|-----------------|
| Assembly language | Encoding tables (COND / INSTR / FX / DEST / SRC / Write / C / Z / Clocks) |
| Smart Pins | Mode-config tables (WRPIN value → behavior) |
| Streamer / CORDIC | Operation / queue tables |
| Debug | DEBUG window / command tables |

- **Method:** For each such table, verify every row against the originating YAML field. Confirm header order matches data order on every row. **Spot-check the first cell of every row** — this is where transposition surfaces.

#### Dimension #8: Terminology conformance

Canonical terms per this manual's `./voice-guide.md` and `./style-guide.md` used consistently. Common targets: "C flag" vs "carry", "COG" vs "cog", "register" vs "location".

- **Method:** Build a canonical-term list from the manual's voice guide; grep for non-canonical variants; flag each occurrence.

#### Dimension #13: Front matter / changelog accuracy

Front matter, README, and changelog often go stale.

- Version number matches latest tag / release
- Claimed counts ("359 instructions", "X methods", "Y appendices") match reality
- Date stamps match last substantive change
- Changelog entries reflect actual changes (not aspirational ones)

### Theme F — Conformance

#### Dimension #9: Voice / tone conformance

Per `./voice-guide.md`. Distinct from Dimension B — B is *factual anchoring of the prose*, this is *tone*:

- No hedging: "probably", "typically", "usually", "may", "might" (unless intentional and source-backed)
- No tutorial voice: "Let's explore…", "You might wonder…" (unless this manual is explicitly tutorial-style — check `./voice-guide.md`)
- No informal language: "basically", "just", "simply"
- No vague: "works like X", "similar to Y" without specifics

- **Method:** grep for the patterns above. Each hit is a finding; propose a specific rewording.

#### Dimension #10: Structural conformance

Every required section per `./creation-guide.md` is present and in the prescribed order. For an instruction/method reference, that typically means: header → short description → category line → syntax → result → parameters → encoding/table → related → explanation. Missing sections, out-of-order sections, and silently-renamed sections are all findings.

#### Dimension #11: Authoring scaffolding leftovers

Anything that shouldn't ship:

- `TODO`, `FIXME`, `XXX`, `HACK`
- `PLACEHOLDER`, `TBD`
- `<!-- NEEDS_VERIFICATION: ... -->`, `<!-- DRAFT: ... -->`
- Commented-out paragraphs older than the last commit
- Backup-file siblings (`*.backup-*`) referenced inadvertently

- **Method:** grep these patterns across `./opus-master/`. Each instance is a finding.

#### Dimension #14: Non-native comment-style leakage

A PASM2 / Spin2 manual must use **only PASM2/Spin2 native comment syntax** — even inside pseudocode, antipattern blocks, or "what-other-platforms-do" contrast examples. Comment markers from other languages (`//`, `/* */`, `;`, `#` as a comment prefix) are an anti-pattern in a manual whose entire mission is teaching the PASM2/Spin2 idiom — they teach the eye to accept foreign syntax in the wrong context.

**Valid PASM2 / Spin2 comments:**

| Marker | Meaning |
|--------|---------|
| `'` | Single-line comment (rest of line) |
| `{ ... }` | Block comment |
| `{{ ... }}` | Documentation comment |

**Forbidden in any code block (including pseudocode):**

| Marker | Why forbidden |
|--------|---------------|
| `//` | C/C++/Java/Rust line comment — not PASM2/Spin2 |
| `/* ... */` | C-style block — not PASM2/Spin2 |
| `;` | Older-tradition assembly line comment — not used in P2 |
| `#` at start of a line followed by space + word | Python / shell — and `#` is PASM2's immediate-prefix; collision is confusing |

**Sweep method:**

1. `grep -nE "//" opus-master/**/*.md | grep -v "https*://"` — line `//` outside URLs
2. `grep -nE "/\*" opus-master/**/*.md` — block-comment opener (filter false-positives from `**X**/**Y**` markdown bold)
3. `grep -nE "^\s*;" opus-master/**/*.md` — semicolon-comment lines (filter Spin2 statement terminators, which are rare)
4. Inspect each hit: is it inside a fenced code block / `:::` div? If yes → finding. If it's narrative prose or a URL → ignore.

**Resolution:**

- Inside `pasm2` / `spin2` code blocks → the example won't compile; **fix the syntax**.
- Inside `::: antipattern` / pseudocode / "C++ does it this way" blocks → still convert to `'` comments. Pseudocode in a PASM2 book uses PASM2 comment syntax. The contrast comes from the *structure* (e.g. an `ISR(...)` shape vs. a dedicated-COG loop), not from foreign comment markers.

**Why this is a real finding (not an aesthetic preference):** A reader sees `// foo` and `' foo` interchangeably and learns that either is "comment-shaped." When they later write PASM2 code, they may try `// my note` and get a syntax error they can't explain. The manual that taught them mixed comment styles is the cause.

---

## 5. Finding Classification

Every finding gets two attributes: **status** (against source) and **severity** (impact on reader).

### Status

| Status | Meaning |
|--------|---------|
| `VERIFIED` | Source confirms exactly — no action |
| `MODIFIED` | Source partially supports — adjust wording |
| `UNVERIFIED` | Cannot locate in any source — investigate or remove |
| `FABRICATED` | Source contradicts — must correct or remove |

### Severity

| Level | Definition | Examples |
|-------|------------|----------|
| `CRITICAL` | Fundamentally wrong; would cause user failure | Opposite flag behavior, wrong opcode, fabricated capability claim |
| `HIGH` | Significant error affecting correct usage | Wrong cycle count, wrong bit width, missing required parameter |
| `MEDIUM` | Misleading but with workaround | Terminology drift, unclear wording, voice drift |
| `LOW` | Cosmetic | Formatting, style preference |
| `INFO` | Improvement opportunity | Missing cross-reference, missing example |

**Reopened findings (Dimension #12)** escalate one severity level — a previously-fixed MEDIUM that has regressed becomes HIGH on this audit.

---

## 6. Report Template

The audit produces a single consolidated file: `./audit/periodic-audit-YYYY-MM-DD.md`.

```markdown
# Periodic Audit — <manual name> — YYYY-MM-DD

**Auditor:** <name or agent>
**Baseline:** Previous audit YYYY-MM-DD (or "first audit")
**YAML range audited:** <git revision range>
**Manual range audited:** <git revision range>

## Summary

| Theme | Findings | Critical | High | Medium | Low | Info |
|-------|----------|----------|------|--------|-----|------|
| A. Factual Grounding | | | | | | |
| B. Coverage | | | | | | |
| C. Hallucination & Drift | | | | | | |
| D. Linkage & Examples | | | | | | |
| E. Consistency | | | | | | |
| F. Conformance | | | | | | |
| **Totals** | | | | | | |

## Findings

### Theme A — Factual Grounding

#### A.1 Manual vs YAML (Dimension A)

| # | Location | Claim in manual | YAML source | Status | Severity | Proposed fix |
|---|----------|-----------------|-------------|--------|----------|--------------|

#### A.2 Voicing alignment (Dimension B)

| # | Location | Manual prose | YAML reference text | Drift type | Severity | Proposed rewording |
|---|----------|--------------|---------------------|------------|----------|--------------------|

#### A.3 KB delta (Dimension 1)

[Inventory of YAML changes since baseline; each entry: changed item / nature of change / does manual reflect it / action needed.]

#### A.4 Quantitative claims (Dimension 5)

| # | Location | Number stated | Source value | Match? | Action |
|---|----------|---------------|--------------|--------|--------|

### Theme B — Coverage

#### B.1 Missing content (Dimension C)

| # | YAML element | Proposed manual location | Rationale | Priority |
|---|--------------|--------------------------|-----------|----------|

#### B.2 Prior-finding closure (Dimension 12)

| Prior audit | Finding ID | Status today | Notes |
|-------------|------------|--------------|-------|

### Theme C — Hallucination & Drift

#### C.1 Red-flag sweep (Dimension 4)

| Pattern | # of hits | Hits with source backing | Hits without (findings) |
|---------|-----------|--------------------------|-------------------------|

[Per-hit table for unsourced hits, with proposed action.]

### Theme D — Linkage & Examples

#### D.1 Cross-references (Dimension 2)
#### D.2 Code examples (Dimension 3)

### Theme E — Consistency

#### E.1 Internal consistency (Dimension 6)
#### E.2 Structural tables (Dimension 7)
#### E.3 Terminology (Dimension 8)
#### E.4 Front matter / changelog (Dimension 13)

### Theme F — Conformance

#### F.1 Voice / tone (Dimension 9)
#### F.2 Structural (Dimension 10)
#### F.3 Authoring scaffolding (Dimension 11)
#### F.4 Non-native comment-style leakage (Dimension 14)

## Recommended Actions (Ranked)

1. **CRITICAL** — must fix before any release
2. **HIGH** — fix in current sprint
3. **MEDIUM** — backlog with target date
4. **LOW / INFO** — backlog without target date

## Sign-off

- [ ] All CRITICAL findings have a tracked fix
- [ ] All HIGH findings have an owner
- [ ] Prior-audit follow-up complete (Dimension 12)
- [ ] Report committed to `./audit/`
- [ ] If fixes touch YAML, downstream consumers identified (see CLAUDE.md "Trust Chain")
```

---

## 7. Workflow

```
1. Pre-audit setup (§3) ─ gather baseline + change sets
2. Run Theme A (factual grounding) ─ this is the priority block
3. Run Theme B (coverage)
4. Run Theme C (hallucination sweep)
5. Run Theme D (linkage + examples)
6. Run Theme E (consistency)
7. Run Theme F (conformance)
8. Triage by severity ─ produce ranked action list
9. Commit report to ./audit/
10. Open follow-up work items for every CRITICAL/HIGH finding
```

**Parallelization:** Themes are largely independent — they can be dispatched to parallel agents (e.g. one Explore agent per theme) for large manuals. Themes D and E benefit most from automation; Themes A and B require domain judgment.

**Stop-and-fix rule:** A CRITICAL finding in Theme A (factually wrong information) should pause the audit and trigger an immediate fix discussion with the user — do not bury CRITICAL findings inside a long report.

---

## 8. Fix-Side Rules

When findings are applied:

- **Edit in place** — no `-fixed`, `-v2`, `-new` suffixes (CLAUDE.md sacred rule #5).
- **Sweep wide, not narrow** — when fixing a fact, find every occurrence and fix all of them in one pass. Memory rule: bad info is outlawed.
- **Protocol layer first** — if the issue is in a driver-domain manual (SD / SPI / I²C / UART), check whether fixing the protocol-layer documentation cascades and covers multiple driver pages at once.
- **Update YAML if the manual is right and the YAML is wrong** — this happens. The trust chain points both ways; fix at the layer where the truth lives.
- **No yaml-generator concerns** — this KB does not use YAML generators; edits to per-instruction/content YAMLs are safe and will not be overwritten.

---

## 9. Companion Documents

- `engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md` — deeper methodology (truth-matrix construction, hallucination taxonomy, lessons learned).
- `./creation-guide.md` — source-authority list and write-time verification protocol for *this* manual.
- `./voice-guide.md`, `./style-guide.md` — conformance rules for Dimensions #8, #9, #10.
- `./audit/` — prior findings; check before re-finding.

---

*This is a process document. The audit reports it produces live in `./audit/periodic-audit-YYYY-MM-DD.md`. Update this process document only when the *process* changes — not when findings change.*
