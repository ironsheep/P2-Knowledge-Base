# Fabrication-Audit Fan-Out Spec — finder + verifier packet

**Sprint:** Fabrication Audit & Correctness Sweep (Group 1), plan §3 (task #175).
**Used by:** the §5 fan-out Workflow — this doc is injected verbatim into every
**finder** agent and every **adversarial-verifier** agent. It operationalizes
`TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md` v2.0.0 (§5.4 exhaustive prose, §6.4 operator,
§8.6 fan-out) into an agent-executable procedure.

**Judgment standard (methodology Part IX): no severity.** Every claim is correct or
wrong. This spec produces *findings*, not rankings.

**Revision:** v1.1.0 (pilot-tuned 2026-07-09). The §4 pilot on PASM2 Part I caught 4/6
reported defects and surfaced ~40 new ones, but **missed two** (a glob-scope error and an
operator-notation error) and the finders **self-capped output at ~8/chapter**. It also
exposed that pointing finders at the *summary* silicon doc manufactures false
"unverifiable" findings. The ten changes tagged **[PILOT-FIX N]** below close those gaps.
Prior revision archived alongside as `.backup-*`.

---

## 0. Pipeline (how your output is used)

```
FINDER (you, stage 1)  →  ADVERSARIAL-VERIFIER (stage 2, a different agent)  →  human hand-check  →  fix
```

You are one stage. **Raise recall, flag uncertainty, never suppress.** A finding you
report will be independently *refuted* by a skeptic in stage 2 and hand-checked by a
human before it changes anything — so a false positive is cheap (it gets killed
downstream) but a **miss is expensive** (nobody else reads your region). When unsure
whether something is a claim, extract it. When unsure whether it's wrong, report it
with `confidence: low`.

**[PILOT-FIX 3] There is NO cap on the number of findings.** Every non-aligned claim is
its own finding object. If your region has 3 defects, return 3; if it has 30, return 30.
Do **not** summarize, consolidate, or report only "the top N." A tidy short list is the
failure mode that let two real defects ship in the pilot. Your `attestation.findings_count`
MUST equal the number of finding objects you return — a mismatch is a self-detected cap.

**[PILOT-FIX 6] Your region is bounded on purpose.** The orchestrator assigns you a
**report-range** (a line span) small enough that you can be exhaustive without
consolidating. Read the whole file for *context*, but report only findings whose primary
location falls inside your assigned report-range (this keeps regions disjoint — no
double-counting). If you find a defect just outside your range, note it in
`attestation.uncovered` rather than emitting a finding for it.

---

## 1. The trust hierarchy (verify in this order)

| Tier | What | Where / how to read it |
|------|------|------------------------|
| **1. PRIMARY (ground truth)** | Parallax P2 Instructions v35 CSV; **P2 Silicon Doc v35 (full)**; Spin2 Language Reference; **the pnut_ts compiler** | see the source map below |
| **2. YAML (derived, agent-facing)** | The P2KB YAML the doc is built from | `mcp__p2kb-mcp__p2kb_get` (natural-language or exact key) and, on disk, `deliverables/ai/P2/language/{pasm2,spin2}/*.yaml` + `deliverables/ai/P2/architecture/*.yaml` |
| **3. TARGET** | the manual/app-note under audit | the assigned `opus-master/` file(s) |

**Primary source map (read the SOURCE, not a summary):**
- **Encodings / flag effects / clocks** — `engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv`. Columns: `order, syntax, group, encoding-bits, alias/., description, [flags in description], hub-cols, cog-clocks…`. Flag semantics and clocks live in the **description** column (ABS row: `"D = ABS(D). C = D[31]."`; RDLONG: `9...16`, variable) — grep the mnemonic and read that cell.
- **[PILOT-FIX 4] Silicon behavior — read the FULL doc, not the facts-only summary.**
  Authoritative text is `engineering/ingestion/sources/silicon-doc/p2-documentation.txt`
  (~13k lines) **plus** the topical extracts in that dir:
  `part2-*.txt` (pixel-ops, video, interrupts, code-blocks), `part3-*.txt` (interrupts,
  end), `part4-smart-pins.txt`, `part4-locks.txt`, `hub-ram-section.txt`,
  `INSTRUCTION-TIMING-AND-ENCODING.md`, `KNOWN-BUGS-CRITICAL.md`,
  `COG-RAM-REGISTER-MAP.md`. `silicon-doc-v35-facts-only.md` is a **22 KB SUMMARY / index
  only** — use it to locate a topic, then confirm in the full doc. **Never conclude
  "unverifiable / fabricated" from the summary's silence — grep the full sources first.**
  (The pilot's false rejections all came from trusting the summary.)
- **Spin2 syntax/operators** — `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt`.
- **[PILOT-FIX 8] The compiler is a primary oracle for code examples.** `pnut_ts` is on
  PATH. For any fenced PASM2/Spin2 example that makes a compileable claim, compile it
  (`pnut_ts <file>`; add `-d` if it contains `debug()`). A compile error or a listing that
  contradicts the doc's stated encoding/cycle-count is a Tier-1 finding. **Known pnut_ts
  blind spots** (do NOT rely on the compiler alone for these — cross-check the CSV):
  operand-order legality, `DIRH/DIRL`-not-a-Spin2-method, and cycle timing (the compiler
  does not report clocks — get clocks from the CSV).

**The YAML (Tier 2) is NOT an authority until it is itself proven against Tier 1.** If
the doc matches the YAML but the YAML is unverified, that is **not** a pass — check the
YAML against the CSV/Silicon Doc. If the YAML is *wrong*, that is its own finding
(`verdict: yaml-wrong`) routed to the corrections register.

---

## 2. Your job: exhaustive claim extraction over ALL prose

Read **every sentence** of your assigned region and extract **every claim** — do not
scan for a feature checklist (that is the exact failure that let the fabrications ship).

A **claim** is any statement of fact about P2 behavior, including:
- capability / behavior statements ("RDLONG reads a long", "ABS sets C to …");
- **worked examples** — an example asserts "this code does X" and "takes N clocks";
  treat each as a claim and verify it end to end (compile it — see PILOT-FIX 8);
- **idiom explanations** — "this pattern gives edge-case-safe abs" is a claim;
- timing / cycle-count statements;
- flag-effect statements;
- cross-instruction or cross-component interaction statements;
- **[PILOT-FIX 1] scope / set-membership / quantifier claims** — any glob (`TEST*`,
  `ALT*`), any "all X do Y", "only X", "every", "none", "always", or a parenthetical
  instruction list. The claim is the **membership itself**: verify that the named set is
  *exactly* the set that has the stated property. The pilot missed `TEST*` because it
  checked "do the bit-test instructions reject WCZ?" (yes) but never checked "does the
  glob `TEST*` correctly delimit the set?" (no — it wrongly swept in TEST/TESTN, which
  carry full WCZ). For every glob/quantifier, enumerate the actual members from the CSV
  and compare.

Prose, tables, callouts, and code comments all contain claims. Extract from all of them.

**[PILOT-FIX 2] Operator-notation pass — run it explicitly over every flag/behavior
table.** For each cell of every flag/behavior/condition table, and every `c:`/`z:`-style
description, classify the `=`:
- `=` meaning **"receives / is"** (a flag or register takes this value: `C = D[31]`,
  `then D = D − S`) → **correct, do NOT flag.**
- `=` used as a **comparison predicate** (a true/false condition: `Result = 0`, `A = B`,
  `Source = 0`) → this must be `==`; emit an `operator` finding.
This is a mandatory sub-step, not an optional red-flag — the pilot content-checked the
§3.4 tables (aligned) and never noticed the comparison-`=` because nothing forced the pass.

**[PILOT-FIX 5] Internal-consistency pass — the doc against itself.** As you read, hold a
running note of every concrete assertion. Whenever two passages of the *same document*
disagree (e.g. §3.5.4 says ABS sets C for an edge case while §3.4.4 says C = "source was
negative"), emit a finding — **at least one side is wrong, and you need no external source
to know that.** This is the cheapest, highest-yield signal we have. Name the sibling
passage in `notes` and still resolve which side Tier 1 supports.

## 3. Per-claim procedure (the trust-chain proof)

For each extracted claim:
1. Classify it (behavior / timing / flag / capability / example / idiom / operator / scope).
2. Find it in **Tier 1** (cite the exact CSV row or Silicon-Doc/Spin2 location — from the
   **full** source, not the summary; compile the example if it is code).
3. Check **Tier 2** (the YAML) agrees with Tier 1 (cite the key/field). If YAML ≠ Tier 1,
   that is a `yaml-wrong` finding too. **[PILOT-FIX 7]** For any flag/operator/comparison
   claim, actively spot-check whether the *same* defect is live in the YAML (the operator
   `=`/`==` issue lives in ~61 YAMLs) — do not treat a matching YAML as automatic
   corroboration; the YAML can carry the identical error. Record `yaml_same_defect`.
4. Compare the **doc** statement to Tier 1.
5. Assign a **verdict** (§5) with a citation for every tier you touched.

## 4. Fabrication red-flags (high-yield; every hit gets verified)

Search your region for these and verify each instance against Tier 1:
- "in parallel" / "overlap*" / "while … proceeds" — claims concurrency the HW may not do (RDLONG blocks).
- "pipelined" applied to a single/blocking op — only the FIFO/streamer + SETQ-burst hide hub latency.
- "issue … and immediately begin" / "fire-and-continue" — asserts non-blocking issue.
- "sets C/Z to indicate <edge/special case>" — invents a flag semantic; the flag is usually just sign/zero/carry.
- "takes N clock cycles" for an M-instruction sequence — cycle-count vs instruction-count (each instr ≥ 2 clocks; sum per-instruction clocks from the CSV).
- "also / additionally / furthermore / side effect / automatically / eliminates" — classic capability-inflation (methodology §2.1).
- **[PILOT-FIX 1]** globs & quantifiers — `TEST*`, `ALT*`, "all", "only", "every", "none", "always", "automatic fallback" — verify the exact membership/universality.

### Timing arithmetic (apply consistently — the pilot got these right; codify so 13 finders do too)
- No P2 instruction executes in **fewer than 2 clocks**; a cancelled conditional still occupies its 2-clock slot.
- An M-instruction straight-line sequence costs **≥ 2·M clocks** — count clocks, never instructions.
- A **taken** branch adds a pipeline flush (≈ +2–3 clocks over not-taken); get the per-instruction figure from the CSV cog-clocks column.
- Hub ops are **variable** (RDLONG `9...16` cog / `9...26` hub) — a hub op can never demonstrate *constant* timing.
- `##`-immediate (AUGD/AUGS) adds an instruction (and 2 clocks) each — `wrlong ##d, ##a` = 6 clocks, not 2.

## 5. Verdict vocabulary (per finding)

| verdict | meaning |
|---------|---------|
| `aligned` | doc matches Tier 1 (and YAML matches Tier 1). Not reported individually — counted in the attestation. |
| `misaligned` | doc contradicts Tier 1 in a factual detail (wrong value/flag/timing/scope). |
| `fabricated` | doc asserts behavior with **no** Tier-1 basis / contradicted by Tier 1 (a hallucination). **[PILOT-FIX 4] Confirm the full silicon doc is silent — not just the summary — before using this verdict.** |
| `operator` | behavior-description comparison written `=` instead of `==`, or a fenced Spin2 code example using `=` where `:=`/`==` is required (methodology §6.4). NB: a "receives" `=` (`C = D[31]`) is **correct** — do NOT flag it. |
| `yaml-wrong` | Tier 2 YAML disagrees with Tier 1 (independent of the doc) — routes to `P2KB-CORRECTION-FINDINGS.md`. |
| `unverifiable` | **[PILOT-FIX 4/soft]** no Tier-1 source found *after grepping the full silicon doc + CSV + Spin2 ref* — flag for human. In `notes`, state which full sources you searched, so this is never a "I only read the summary" shrug. |

Internal contradictions (PILOT-FIX 5) are reported under `misaligned` or `fabricated`
(whichever Tier 1 supports for the wrong side), with the sibling-passage conflict named in `notes`.

## 6. Output schema (one object per finding)

```
{
  "doc": "<manual slug>",
  "location": "<file §/heading + line>",
  "anchor_snippet": "<8-20 words quoted VERBATIM from the doc at the defect — [PILOT-FIX 9] survives line-number drift; the fix step text-matches on this>",
  "claim": "<the exact doc claim, quoted>",
  "kind": "behavior|timing|flag|capability|example|idiom|operator|scope|internal-contradiction",
  "defect_class": "<[PILOT-FIX 10] short kebab slug grouping like defects across the fan-out, e.g. cycle-count-vs-instruction-count, glob-overgeneralization, operator-eq-vs-eqeq, hub-overlap-fabrication, cordic-result-path — the class-wide sweep groups by this>",
  "verdict": "misaligned|fabricated|operator|yaml-wrong|unverifiable",
  "tier1_cite": "<CSV row / FULL Silicon-Doc loc / Spin2 ref / pnut_ts result — the ground truth>",
  "tier1_says": "<what the primary source actually states>",
  "yaml_cite": "<p2kb key / deliverables path + field, or 'n/a'>",
  "yaml_agrees_tier1": true|false|null,
  "yaml_same_defect": true|false|null,
  "correct_statement": "<what the doc SHOULD say>",
  "confidence": "high|medium|low",
  "notes": "<why; any uncertainty for the verifier; full sources searched if unverifiable; sibling passage if internal-contradiction>"
}
```

Also emit, per assigned region, a **coverage attestation**:
`{ "region": "<file + report-range>", "claims_extracted": N, "findings_count": M, "coverage": "exhaustive|partial", "uncovered": "<none | what and why | defects seen just outside the report-range>" }`.
**No silent caps** — `findings_count` MUST equal the number of finding objects (PILOT-FIX 3);
if you could not fully cover the region, say so; silence ≠ audited.

## 7. Adversarial-verifier instructions (stage 2)

You receive ONE finding. **Default to refuting it.** Independently pull the Tier-1
source yourself (do not trust the finder's cite — re-fetch it), and **[PILOT-FIX 4] read
the FULL silicon doc (`p2-documentation.txt` + `part*-*.txt`), never the facts-only
summary** — a finding of `fabricated`/`unverifiable` is only sustainable if the full
sources are genuinely silent. For a code example, **recompile it with `pnut_ts` yourself**.
Then decide:
- `confirmed` — Tier 1 genuinely contradicts the doc as the finding claims (quote Tier 1).
- `rejected` — the doc is actually correct, or the finding misread Tier 1 / relied on the summary (explain, quote the full Tier 1). This is the expected outcome for inverted findings.
- `refine` — a real problem exists but the finder mis-stated it (give the corrected finding).
Output `{ "verdict": "confirmed|rejected|refine", "tier1_recheck": "<what you found in the FULL source>", "corrected": "<if refine>" }`.
Only `confirmed` (and `refine`d) findings reach the human hand-check.

---

## 8. Worked example — proves the spec (PASM2 §3.5.4 ABS)

**Doc claim** (`chapter-03-flags.md:431`): *"The ABS instruction … sets C to indicate the
exceptional case [$8000_0000]."* + `abs result,value wc` / `if_c neg result` billed
"edge-case safe."

1. kind = flag + idiom (worked example); also **internal-contradiction** (conflicts with §3.4.4).
2. Tier 1: CSV row 62 — `"D = ABS(D). C = D[31]."` → **C = the original sign bit**, always. Full Silicon Doc: $8000_0000 is unrepresentable; ABS leaves it unchanged, no dedicated edge flag.
3. Tier 2: `p2kb_get "p2kbPasm2Abs"` → `C: Set to original sign bit (S[31]/D[31])` — agrees with Tier 1 (`yaml_same_defect: false`). (So YAML is correct; only the doc is wrong.)
4. Compare: doc says "C indicates the edge case"; Tier 1 says "C = original sign." Contradiction. The code, read with C=sign, computes the **identity**, not abs. The doc's own §3.4.4 ("ABS | Source was negative") already agrees with Tier 1 — internal contradiction.
5. Verdict: **`fabricated`**. `defect_class: "abs-c-flag-edge-case-fabrication"`. `anchor_snippet`: "sets C to indicate the exceptional case". `tier1_cite`: "v35 CSV row 62 (ABS): C = D[31]". `correct_statement`: "ABS alone is the absolute value; with WC, C records that the source was negative (used to restore sign later)." `confidence: high`.

A finder handed only this spec and this section reproduces the finding with the correct
silicon citation — which is the acceptance test for this spec (plan §3 / task #175).
