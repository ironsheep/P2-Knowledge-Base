# Fabrication-Audit Fan-Out Spec — finder + verifier packet

**Sprint:** Fabrication Audit & Correctness Sweep (Group 1), plan §3 (task #175).
**Used by:** the §5 fan-out Workflow — this doc is injected verbatim into every
**finder** agent and every **adversarial-verifier** agent. It operationalizes
`TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md` v2.0.0 (§5.4 exhaustive prose, §6.4 operator,
§8.6 fan-out) into an agent-executable procedure.

**Judgment standard (methodology Part IX): no severity.** Every claim is correct or
wrong. This spec produces *findings*, not rankings.

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

---

## 1. The trust hierarchy (verify in this order)

| Tier | What | Where / how to read it |
|------|------|------------------------|
| **1. PRIMARY (ground truth)** | Parallax P2 Instructions v35 CSV; P2 Silicon Doc v35; Spin2 Language Reference | `engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv` (encodings, flag effects, clocks); `engineering/ingestion/sources/silicon-doc/silicon-doc-v35-facts-only.md` (+ siblings in that dir); `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` (Spin2 syntax/operators) |
| **2. YAML (derived, agent-facing)** | The P2KB YAML the doc is built from | `mcp__p2kb-mcp__p2kb_get` (natural-language or exact key) and, on disk, `deliverables/ai/P2/language/{pasm2,spin2}/*.yaml` + `deliverables/ai/P2/architecture/*.yaml` |
| **3. TARGET** | the manual/app-note under audit | the assigned `opus-master/` file(s) |

**The YAML (Tier 2) is NOT an authority until it is itself proven against Tier 1.** If
the doc matches the YAML but the YAML is unverified, that is **not** a pass — check the
YAML against the CSV/Silicon Doc. If the YAML is *wrong*, that is its own finding
(`verdict: yaml-wrong`) routed to the corrections register.

CSV reading note: columns are `order, syntax, group, encoding-bits, alias/., description, [flags in description], hub-cols, cog-clocks…`. The flag semantics and clocks live in the **description** column (e.g. ABS row: `"D = ABS(D). C = D[31]."`; RDLONG: `9...16`, variable) — grep the mnemonic and read that cell.

---

## 2. Your job: exhaustive claim extraction over ALL prose

Read **every sentence** of your assigned region and extract **every claim** — do not
scan for a feature checklist (that is the exact failure that let the fabrications ship).

A **claim** is any statement of fact about P2 behavior, including:
- capability / behavior statements ("RDLONG reads a long", "ABS sets C to …");
- **worked examples** — an example asserts "this code does X" and "takes N clocks";
  treat each as a claim and verify it end to end;
- **idiom explanations** — "this pattern gives edge-case-safe abs" is a claim;
- timing / cycle-count statements;
- flag-effect statements;
- cross-instruction or cross-component interaction statements.

Prose, tables, callouts, and code comments all contain claims. Extract from all of them.

## 3. Per-claim procedure (the trust-chain proof)

For each extracted claim:
1. Classify it (behavior / timing / flag / capability / example / idiom / operator-notation).
2. Find it in **Tier 1** (cite the exact CSV row or Silicon-Doc/Spin2 location).
3. Check **Tier 2** (the YAML) agrees with Tier 1 (cite the key/field). If YAML ≠ Tier 1, that is a `yaml-wrong` finding too.
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

## 5. Verdict vocabulary (per finding)

| verdict | meaning |
|---------|---------|
| `aligned` | doc matches Tier 1 (and YAML matches Tier 1). Not reported unless attesting coverage. |
| `misaligned` | doc contradicts Tier 1 in a factual detail (wrong value/flag/timing). |
| `fabricated` | doc asserts behavior with **no** Tier-1 basis / contradicted by Tier 1 (a hallucination). |
| `operator` | behavior-description comparison written `=` instead of `==`, or a fenced Spin2 code example using `=` where `:=`/`==` is required (methodology §6.4). NB: a "receives" `=` (`C = D[31]`) is **correct** — do NOT flag it. |
| `yaml-wrong` | Tier 2 YAML disagrees with Tier 1 (independent of the doc) — routes to `P2KB-CORRECTION-FINDINGS.md`. |
| `unverifiable` | no Tier-1 source found; flag for human (do not assume wrong or right). |

## 6. Output schema (one object per finding)

```
{
  "doc": "<manual slug>",
  "location": "<file §/heading + line>",
  "claim": "<the exact doc claim, quoted>",
  "kind": "behavior|timing|flag|capability|example|idiom|operator",
  "verdict": "misaligned|fabricated|operator|yaml-wrong|unverifiable",
  "tier1_cite": "<CSV row / Silicon-Doc loc / Spin2 ref — the ground truth>",
  "tier1_says": "<what the primary source actually states>",
  "yaml_cite": "<p2kb key / deliverables path + field, or 'n/a'>",
  "yaml_agrees_tier1": true|false|null,
  "correct_statement": "<what the doc SHOULD say>",
  "confidence": "high|medium|low",
  "notes": "<why; any uncertainty for the verifier>"
}
```

Also emit, per assigned region, a **coverage attestation**:
`{ "region": "...", "claims_extracted": N, "findings": M, "coverage": "exhaustive|partial", "uncovered": "<none | what and why>" }`.
**No silent caps** — if you could not fully cover the region, say so; silence ≠ audited.

## 7. Adversarial-verifier instructions (stage 2)

You receive ONE finding. **Default to refuting it.** Independently pull the Tier-1
source yourself (do not trust the finder's cite — re-fetch it). Then decide:
- `confirmed` — Tier 1 genuinely contradicts the doc as the finding claims (quote Tier 1).
- `rejected` — the doc is actually correct, or the finding misread Tier 1 (explain, quote Tier 1). This is the expected outcome for inverted findings.
- `refine` — a real problem exists but the finder mis-stated it (give the corrected finding).
Output `{ "verdict": "confirmed|rejected|refine", "tier1_recheck": "<what you found>", "corrected": "<if refine>" }`.
Only `confirmed` (and `refine`d) findings reach the human hand-check.

---

## 8. Worked example — proves the spec (PASM2 §3.5.4 ABS)

**Doc claim** (`chapter-03-flags.md:431`): *"The ABS instruction … sets C to indicate the
exceptional case [$8000_0000]."* + `abs result,value wc` / `if_c neg result` billed
"edge-case safe."

1. kind = flag + idiom (worked example).
2. Tier 1: CSV row 62 — `"D = ABS(D). C = D[31]."` → **C = the original sign bit**, always. Silicon Doc: $8000_0000 is unrepresentable; ABS leaves it unchanged, no dedicated edge flag.
3. Tier 2: `p2kb_get "p2kbPasm2Abs"` → `C: Set to original sign bit (S[31]/D[31])` — agrees with Tier 1. (So YAML is correct; only the doc is wrong.)
4. Compare: doc says "C indicates the edge case"; Tier 1 says "C = original sign." Contradiction. The code, read with C=sign, computes the **identity**, not abs.
5. Verdict: **`fabricated`**. `tier1_cite`: "v35 CSV row 62 (ABS): C = D[31]". `correct_statement`: "ABS alone is the absolute value; with WC, C records that the source was negative (used to restore sign later)." `confidence: high`.

A finder handed only this spec and this section reproduces the finding with the correct
silicon citation — which is the acceptance test for this spec (plan §3 / task #175).
