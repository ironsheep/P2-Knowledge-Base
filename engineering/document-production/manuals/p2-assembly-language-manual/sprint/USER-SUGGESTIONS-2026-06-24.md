# P2 Assembly Language Reference — User Suggestions Collection

**Manual:** p2-assembly-language-manual (currently released v3.0.0, 2026-06-10, 492pp)
**Collected:** 2026-06-24
**Source:** Stephen M Moraco — live observations, various forms
**Status:** 🟡 COLLECTING — Stephen is feeding observations; evaluation begins when he says "done."

---

## How to read this document

This is a **faithful capture** of Stephen's observations during the collection
phase. Observations are recorded as given — NOT yet evaluated, judged, or acted
on. Light categorization (Layout / Content / Voicing) is applied only to keep
related items findable; the real disposition happens in the evaluation phase.

**Categories:**
- **Layout** — render / template / page-layout (PDF appearance)
- **Content** — the reference material itself (opus-master text, facts, examples)
- **Voicing** — narrative tone/wording; may also require a fix to `voice-guide.md`
  so the habit stops being reproduced
- **Uncategorized** — captured first, classified during evaluation

---

## Observations

<!-- Each observation captured as a numbered entry. Verbatim where given;
     lightly structured where Stephen describes something. No evaluation here. -->

### Batch 1 — 2026-06-24

> Several of these are relayed from a **community reviewer** ("the user");
> Stephen adds his own framing/context in places. Captured faithfully.

---

#### OBS-01 — Min/Max pattern should show FLE/FGE alternative
**Category:** Content + Layout (side-by-side presentation)
**Location:** Chapter 2 (Instruction Format), §2.2.4 Conditional Execution Patterns

The min/max pattern is shown using **Compare Unsigned** (CMP-style + conditional
move). Reviewer is reminded that someone would actually use the **FLE**
instruction instead. Request: **compare the two approaches**, and possibly
**put the two side by side** as alternate ways to do min/max.

*(Research note for eval: P2 has FGE/FLE/FGES/FLES "force greater/less or equal"
clamp instructions — verify which gives min vs max.)*

---

#### OBS-02 — Overarching: the manual text is too lengthy
**Category:** Voicing (thesis — drives several items below)

Reviewer's stance (NOT verbatim, just where he's coming from): *"the text of
the assembler manual is too lengthy."* This is the umbrella concern that the
specific examples below illustrate.

**Stephen's framing/context:** This was our **first manual generated**, our
**first attempt at a voicing guide**, and our **most lengthy manual**. He
suspects that against our intent for this manual we could **tighten the voicing**
to remove marketing / superfluous narrative and reduce presentation to the
essential (non-repetitive). That should **whittle down the preface material**.
*"It's better and more difficult to write a short text than an epic one."*

---

#### OBS-03 — §1.1 is superfluous, dated-marketing, and partly wrong
**Category:** Content + Voicing
**Location:** Chapter 1, the text immediately under **Figure 1.1** (summarizing
that the P2 contains eight identical processors), leading into **§1.1.1 COG
Independence**.

Reviewer's observations:
1. **§1.1 is completely superfluous** — everything is already said in the words
   before it.
2. It **reads like outdated marketing text** — in 2026, having more than one
   core is state of the art / unremarkable.
3. The text is **factually wrong**: the shared hub slows random hub access very
   much, so you are always struggling to **avoid** hub memory access. (The prose
   implies the opposite / glosses this.)

---

#### OBS-04 — Add short-form operation summary to long instruction explanations
**Category:** Content (class request) + Voicing
**Location example:** MULS instruction

Request: **add the short form to the long versions explaining instructions.**
Example (reviewer's image was partly cut off, reconstructed):
`D = signed(D[15:0]) × signed(S[15:0])`, where `Z = (S==0 OR D==0)`.
Add that operation-summary form **into the long text** explaining MULS so that
people who just want the information fast can retrieve it quickly **in the same
place**. Treat as a **class** (applies across instruction entries).

---

#### OBS-05 — Superfluous reassurance wording
**Category:** Voicing
**Location:** MULS explanation (and likely a class)

Wording like *"the result is correctly signed"* / *"the result is properly
extended"* — reviewer (tongue-in-cheek: *"I'm really glad that…"*) flags this as
**superfluous text that doesn't add anything.**

---

#### OBS-06 — Scaled multiply mentioned without SCA / SCAS (cross-ref completeness)
**Category:** Content (class) + Layout (decoration/cross-refs)
**Location:** the multiply model section that mentions **scaled multiply**

Reviewer: it's strange that this section mentions **scaled multiply** without
mentioning **SCA** and **SCAS** — you'd have to look them up to see how they
apply. If they should be mentioned, **decorate this section and bring SCA/SCAS
forward**. Likewise there may be similar cases throughout the manual where we
should refer to other related techniques.
**Treat this as a CLASS** — study the whole manual for missing
related-technique cross-references.

---

#### OBS-07 — "commonly used for signed arithmetic and physics calculations"
**Category:** Voicing
**Location:** MULS (example of filler prose)

Reviewer (tongue-in-cheek): is there really someone who needs a sentence like
*"MULS is commonly used for signed arithmetic and physics calculations"*? Cited
as another instance of **too many words**. We should **ratify it or argue
against it with an explanation.**

---

#### OBS-08 — LUT chapter should state its primary purpose & memory-layout tradeoff
**Category:** Content
**Location:** the LUT chapter

It should be mentioned that the **primary purpose of LUT memory is faster
assembler code** (execute from LUT), because **COG RAM is more valuable** — it
can be used as registers. This matters at **project start for memory layout
planning**, so the reader should have it in mind early.

---

#### OBS-09 — LUT immediate addressing limited to first 256 (verify + document)
**Category:** Content (verify against source)
**Location:** LUT chapter / RDLUT-WRLUT

Reviewer recalls (source not at hand) that **RDLUT destination #500 will not
work** because **only the first 256 LUT locations can be addressed directly via
immediate**. Forum response to verify:
> "Yes, immediate addressing only available for first half of LUT. This was done
> to allow PTRx + optional index to address entire LUT."
Forum link: https://forums.parallax.com/discussion/comment/1453739/#Comment_1453739

**Action:** verify against authoritative source (Silicon Doc / compiler /
hardware) and document the limitation + the PTRx rationale if confirmed.

---

### Cross-cutting CLASSES identified in Batch 1

- **CLASS-A — Voicing trim / de-marketing.** Sweep the manual (esp. preface &
  Ch.1) for superfluous narrative, marketing tone, and reassurance filler
  (OBS-02, -03, -05, -07). Likely also needs a **`voice-guide.md` fix** so the
  habit stops being reproduced.
- **CLASS-B — Short-form operation summary in instruction entries** (OBS-04).
  Possibly a structural/authoring-convention addition.
- **CLASS-C — Related-technique cross-reference completeness** (OBS-06) — surface
  related instructions/techniques where a concept is mentioned.

---

## Evaluation

_Batch 1 closed by Stephen ("this concludes the entire batch — dissect, research,
come back with proposals"). Research complete 2026-06-24. Each item below carries
a disposition + grounded proposal. Nothing edited yet — awaiting Stephen's
go-ahead on the flagged design decisions._

**Manual is RELEASED v3.0.0 → full release path (version bump) once changes land.**

### Sources consulted during evaluation
- Opus-master: `part-i/chapter-01-execution-model.md` (§1.1, §1.3),
  `part-i/chapter-02-instruction-format.md` (§2.2.4, §2.9), `part-ii/instructions-m.md`
  (MUL, MULS), `part-ii/instructions-s.md` (SCA, SCAS).
- P2KB (authoritative): `FLE`/`FGE`/`FLES`/`FGES`, `RDLUT`/`WRLUT`, addressing-modes.
- Silicon Doc / datasheet instruction tables (RDLUT/WRLUT `{#}S/P` shared field).

---

#### OBS-01 — ACCEPT (Content add + side-by-side layout)
**Verified (P2KB):** `FLE D,S` = "force less-or-equal" = **limit maximum** →
`D = min(D,S)` (unsigned, 2 clk). `FGE D,S` = "force greater-or-equal" =
**limit minimum** → `D = max(D,S)` (unsigned, 2 clk). Signed variants `FLES`/`FGES`.
**Current text (§2.2.4) min/max idiom:** `cmp a,b wc` + `if_c mov min,a` +
`if_nc mov min,b` = 3 instruction slots, **6 cycles always** (cancelled
conditional instructions still cost 2 clk), plus it needs `a`/`b` live.
**FLE idiom:** `mov min,a` + `fle min,b` = 2 instr, **4 cycles**; or in-place
`fle x,limit` = 1 instr/2 cycles when the value is already in `x`.
**Proposal:** §2.2.4's job is teaching *conditional execution*, so KEEP the
conditional-execution min/max as the worked example, but ADD a short
side-by-side "In real code, use FLE/FGE" callout showing the 1–2-instruction
clamp, with a cross-ref to the FLE/FGE/FLES/FGES entries. Note the distinction
from §2.9's compile-time `#>` / `<#` limit operators (those are assembler-time;
FLE/FGE are runtime).
*Design decision D1:* side-by-side two-column vs stacked code blocks (layout).

#### OBS-02 — ACCEPT as guiding principle → drives CLASS-A
Thesis is sound and matches our own read (first manual, first voice guide, longest
doc). Execute via the CLASS-A voicing sweep + a `voice-guide.md` rule update so
the habit stops recurring. Expect meaningful shrink concentrated in front-matter
/ preface and Chapter 1.

#### OBS-03 — ACCEPT (trim + de-market) / PARTIALLY REJECT the "factually wrong" framing
**Read of the actual text:** the chapter intro, the §1.1 bullet list under
Fig 1.1, and §1.1.1 *do* overlap ("unique multi-processor architecture" /
"eight identical processors" / "true parallel execution"). Trimming the
redundancy is warranted (CLASS-A).
- *Superfluous:* agree there is redundancy; tighten — don't delete the figure
  orientation, but collapse the duplicated claims.
- *Dated-marketing tone:* agree — lines like "ideal for real-time applications
  such as video generation, motor control…" read as marketing; de-market.
- *"Factually wrong about hub":* **honest pushback — the manual is NOT wrong.**
  §1.4.2 already documents hub timing accurately (up to 7-clock align wait,
  deterministic, FIFO/egg-beater for sustained streaming). The reviewer's own
  framing ("you always struggle to avoid hub access") is itself an overstatement
  — *random* access is costly; *sequential/streamed* access is high-bandwidth.
  The legitimate fix is that Chapter 1's first impression oversells parallelism
  **without surfacing the hub-access cost early**. **Proposal:** add a brief,
  accurate note in §1.1/§1.4 that random hub access carries latency and that
  time-critical code runs from cog/LUT — cross-ref §1.4.2. Do NOT adopt the
  "you always struggle" overstatement (no unsourced/overstated claims).

#### OBS-04 — ACCEPT → CLASS-B (structural authoring-convention add)
The operation pseudocode already EXISTS but is buried (MULS para 2: "The
operation is: D = signed(D[15:0] * S[15:0])"; Z-effect is in the encoding table;
Appendix C has compact forms). The ask is to **surface a scannable one-line
operation summary** at the top of each entry. Source material exists
(P2KB `oneliner`/`result`/`description`, Appendix C categorical forms) — this is
surfacing, not inventing.
*Design decision D2 (big-scope):* add a consistent **Operation:** line (compact
pseudocode incl. flag conditions) to the identity/result block of instruction
entries. Decide: (a) format (e.g. `Operation: D = signed(D[15:0] × S[15:0]); Z = (S==0 ∨ D==0)`),
(b) scope — all ~350 entries vs math/logic first, (c) source of truth
(P2KB-derived; update `AUTHORING-CONVENTIONS.md` + `creation-guide.md`).

#### OBS-05 — ACCEPT → CLASS-A (specific instance + voice rule)
MULS prose: "The 32-bit result is properly sign-extended…" / "…the result is
correctly signed." Trim reassurance that the hardware does its job. Add a
voice-guide rule: don't editorialize hardware correctness.

#### OBS-06 — ACCEPT → CLASS-C (concrete + class sweep)
**Concrete instance:** MUL's fixed-point example teaches manual scaling
(`mul` then `shr #16`) — exactly what **SCA** does in one instruction
(`>>16`, unsigned). MULS's example (`muls` then `sar #16`) is what **SCAS**
does (`>>14`, signed). SCA/SCAS are already in the `Related:` line but not
surfaced in the teaching prose where the manual idiom appears. **Proposal:**
add an inline "→ see SCA/SCAS for single-instruction scaled multiply" at those
teaching points. **Class:** sweep the manual for "here's a multi-instruction
idiom that a single instruction does natively" and cross-ref.

#### OBS-07 — PARTIALLY ACCEPT (trim vague application name-drops) → CLASS-A
MULS: "MULS is commonly used for signed arithmetic and physics calculations:".
The vague domain name-drop ("physics calculations") adds nothing; the *example*
carries the meaning. **Proposal:** replace with a concrete lead-in
(e.g. "Signed scaling example:") rather than naming application domains.
Voice rule: lead examples with what the code does, not hand-wavy use-cases.
*(Ratified: the reviewer is right; keep examples, drop the domain editorializing.)*

#### OBS-08 — ACCEPT with honest reframe (Content add)
§1.3.1 already notes LUT as "valuable overflow code space." The new value is the
**memory-layout-planning** guidance. **Honest reframe:** don't claim a single
"primary purpose" (LUT also serves lookup tables, streamer palettes, CORDIC,
cog-pair sharing). **Proposal:** add a short note in §1.3 — "cog RAM doubles as
your register file and is your most precious resource; the LUT is a second
512-long fast space for data tables and overflow code, so plan the split at
project start." Captures the reviewer's intent without overstatement.

#### OBS-09 — ACCEPT — ✅ CONFIRMED 2026-06-24 (Content add)
**Status: VERIFIED against primary sources + the compiler (R2 thread).** No longer
NEEDS-VERIFICATION. Bit-level mechanism (ground-sourced):
- S field bit 8 is the discriminator: `0AAAAAAAA` = 8-bit literal LUT address
  $000–$0FF (first 256 only); `1SUPNNNNN` = PTR expression (bit 7 = PTRA/PTRB),
  which reaches the full $000–$1FF.
- **Silicon Doc primary table:** `engineering/ingestion/sources/silicon-doc/part3-end.txt:172-218`
  (`#%0AAAAAAAA` 8-bit immediate vs `#%1SUPNNNNN` PTR expr; PTRA=100000000,
  PTRB=110000000). RDLUT/WRLUT reach full $000–$1FF (`.../p2-documentation.txt:983`)
  — so the cap is the literal restriction, not LUT size.
- **Compiler empirical (PNut-TS 1.55.0):** `#255` compiles; `#256`/`#500` → error
  "Constant must be from 0 to 255" (boundary exactly $0FF→$100). `ptra` emits
  S=$100, `ptrb` S=$180 — bit-for-bit match to the Silicon Doc table.
- Chip Gracie's forum rationale is thus corroborated by primary + empirical;
  no external compiler-source study needed (residual is belt-and-suspenders).
**Document (Phase 2):** ✅ now backed by an AUTHORITATIVE pnut-ts-source briefing
supplied by Stephen: `engineering/ingestion/external-inputs/pnut_ts_facts/LUT-Immediate-Addressing-Briefing-for-Doc-Agents.md`.
Use its **§6 copy-paste callout** in §1.3.2 (LUT Instructions) + the RDLUT/WRLUT
entries. Facts to land: literal address `#0`–`#255` only; `#256`+ is a **hard
compile error** (`Constant must be from 0 to 255`) — not a wrap/silent trap;
**full LUT via a register operand OR PTRA/PTRB(+index)**; the *why* (S-field bit 8
is the pointer-expression selector). Honor briefing **§7 guardrails** (don't say
"wraps"/"256 longs inaccessible"; don't push `##`; no numeric opcode constants).
MAYBE (Stephen): a one-line note that the same plain-immediate 0–255 cap is shared
by the hub RD/WR family (RDLONG/WRLONG/RD-WR BYTE/WORD/WMLONG) but rarely bites
there. KB side tracked as **F-161** (enriched with this briefing).
**Cross-head spillover (→ corrections register):** the published KB page
`p2kbPasm2Rdlut` shows `{#}S/P` but omits the 0–255 literal limit in prose —
logged to `P2KB-CORRECTION-FINDINGS.md` for the yaml head.

_(original assessment retained below for history)_
**Status:** highly plausible, partially corroborated, not yet ground-sourced.
Silicon Doc/datasheet confirm `RDLUT D,{#}S/P` and `WRLUT {#}D,{#}S/P` — the
same 9-bit field encodes **either** an immediate **or** a PTRx expression. The
specific claim "immediate reaches only the first 256" follows if bit 8 of that
field is the PTR-mode selector (leaving an 8-bit literal → 0–255), with the
full 512-long LUT reachable via PTRA/PTRB(+index). **Forum post is community-tier
— corroboration only, not citable.** **Action before documenting:** confirm the
bit-8/PTR-mode encoding from the Silicon Doc pointer-operand section (and/or the
compiler's operand encoder). If confirmed, add a pitfall note to §1.3.2 (LUT
Instructions) + the RDLUT/WRLUT entries: literal LUT addresses are limited to
$000–$0FF; use PTRA/PTRB for the upper half. Per the "NEEDS-VERIFICATION is not
a ship license" rule, this gets verified in-repo during execution — not shipped
on the forum's say-so.

---

### Cross-cutting CLASSES — dispositions

- **CLASS-A (voicing trim / de-marketing + voice-guide fix).** ACCEPT. Sweep
  front-matter, Ch.1, and instruction prose for: redundant restatement,
  marketing tone, hardware-correctness reassurance (OBS-05), vague
  application-domain name-drops (OBS-07). Update `voice-guide.md` with explicit
  rules so regeneration/future edits don't reintroduce them. This is the
  single biggest lever on OBS-02's "too lengthy."
- **CLASS-B (Operation: pseudocode line).** ACCEPT pending D2 decisions — biggest
  mechanical scope (per-entry). Authoring-convention change + sweep.
- **CLASS-C (related-technique cross-ref completeness).** ACCEPT. Sweep for
  manual idioms that a single instruction performs (SCA/SCAS being the seed),
  and surface the cross-ref inline at the teaching point.

### Flagged design decisions — STEPHEN'S DECISIONS (2026-06-24)

- **D1 — DECIDED: STACK (not side-by-side).** No existing precedent for
  side-by-side in our manuals. Stack the alternatives (CMP-based vs FLE/FGE) and
  **show the performance difference** (cycle counts) between them.
- **D2 — DECIDED: DO IT, but CAREFULLY PLACED (not 100% of instructions).**
  *(Refined by Stephen 2026-06-24.)* Surfacing the buried pseudocode early is the
  right move — **but only where it's actually useful**: where the operation is
  non-obvious / something a reader wouldn't already understand from the name +
  syntax + one-line description. **Do NOT** add pseudocode to instructions whose
  behavior is self-evident (e.g. trivial MOV/ADD-style ops). Curated placement,
  not blanket coverage. Requirements:
  - Must be **grounded and correctly sourced** wherever it IS added (no
    inference). Richest grounded source — the Parallax instruction **CSV**
    (`P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv`); the **ingested
    instruction DB(s)** are an alternate/cross-check.
  - **Fixed location** within the narrative entry (consistent slot, surfaced
    **early**) for the entries that get one.
  - The research (R1) must therefore ALSO produce a **usefulness/selection
    criterion** — classify which instructions genuinely benefit (e.g. signed/
    scaled multiplies, bit-field shuffles like MERGEB/MOVBYTS/MUXNIBS, flag-
    derived results) vs which are self-evident — and recommend the cut line.
- **D3 — DECIDED: VOICING FIRST.** Do the voicing + `voice-guide.md` rewrite
  first and **agree the new voicing**, THEN rework the document under the new
  voice, THEN go through and clean up the other items (CLASS-B/C, OBS-01, etc.).
- **D4 —** (carried) voice-guide fixes land in this manual's `voice-guide.md`;
  watch for any rule general enough to promote to a shared voice standard.

### OBS-09 — source clarification (Stephen)
The forum responder is believed to be **Chip Gracie (username "C. Gracie")** —
the P2 designer / PNut compiler author — describing **what the compiler does and
why**. That makes it effectively a primary/authoritative rationale, **confirmable
in the compiler**. ACTION: an **agent studying the compiler** locates the LUT
immediate/PTR (`S/P`) operand handling and confirms the 0–255 immediate limit +
PTRx-for-full-LUT rationale.
NOTE (environment): the **PNut-TS compiler source is NOT in this workspace**
(only the compiled `pnut-ts` binary + ingested compiler-ref material). So this
splits: (a) exhaust the in-repo ingested operand-encoding material
(`pnut-ts-pasm-ref/OPERAND-FORMAT-*`, instruction DB JSON, Silicon Doc), then
(b) formulate the precise residual question for a study against the external
PNut-TS source tree.

### NEW scope added by Stephen (2026-06-24) — two full-instruction-set SCANS
Now that we have the **complete instruction set** in hand, two opportunities are
worth a comprehensive scan (not just the seed instances found in Batch 1):
- **SCAN-1 (extends CLASS-C):** related-technique cross-references — find every
  place a concept/idiom is taught where a related instruction should be surfaced
  inline (SCA/SCAS was the seed).
- **SCAN-2 (extends OBS-01):** "alternative-technique / better-performing single
  instruction" — find every multi-instruction idiom in the manual that a single
  (or fewer) instruction(s) accomplishes, and present the alternative + its
  performance delta (FLE/FGE-for-min/max was the seed).

### Agreed execution sequence (per D3)
1. **Phase 1 — Voicing.**
   - **Step 1 — ✅ DONE 2026-06-24.** `voice-guide.md` updated to **v1.1**
     (Stephen agreed the rules): §1.3 Narrative Brevity + surface-honest-tradeoffs;
     §4.2 four new "Never Do" rows (no marketing, no hardware-correctness
     reassurance, no vague-domain example justification, say-each-fact-once);
     §7 checklist items. Timestamped backup made first.
     **Bonus defect fixed same pass:** §5.1 terminology table wrongly mandated
     "COG — all caps"; corrected to lowercase-cog-in-prose (matches the applied
     E2 cog-casing sweep + Parallax corpus; also folded in cog-not-CPU). A second
     residual "COG" in the register-row note fixed too.
   - **Step 2 — ✅ DONE 2026-06-24.** Doc-wide CLASS-A rework applied. Discovery
     sweep (`scratchpad/classA-voicing-sweep.md`, ~65 located findings) → edit
     pass: front-matter + chapters 01/03/04/05/06 done by me (incl. the approved
     CAT5 tradeoff lines in front-matter + §1.1.1, the structural §2.8 cross-ref,
     CAT4 sentence-merges); part-ii/part-iii (51 edits) by a sub-agent; then a
     verification grep caught + fixed ~14 stragglers (more seamless/sophisticated/
     powerful, 4× CPU→cog, directives "ORGF ensures"). Structure verified clean
     (all code-fence counts even). Covers OBS-02, -03 (trim/de-market), -05, -07.
   - **Hub-casing finding:** prose is ALREADY predominantly lowercase (Part I:
     247 lowercase vs 78 capital; the capitals are sentence-initial, code
     comments, or the named "Hub Execution" mode). A blanket lowercase would be
     artificial — so no sweep applied; hub-casing is effectively consistent.
     Voice-guide §5.1 updated to the consistent rule.
   - **OPEN observation (flag to Stephen) — all-caps `COG`:** remains in
     chapter-end **keyconcepts `\item` blocks** (ch01:225-229, ch03:701,
     ch04:678, ch05:825/830, ch06:598) and **code comments** (directives, ch05
     lockrel comments, appendix-e). The E2 cog-casing sweep evidently scoped to
     prose only. NOT swept here (prior, reviewed element). Decision needed:
     extend lowercase-cog to keyconcepts/code-comments, or leave as-is.
   - **Hub casing — DECIDED (Stephen 2026-06-24):** treat "hub" like "cog" —
     **lowercase in plain reference prose; capitalize only in titles/headings/
     special-meaning/proper-noun uses.** Be consistent, not artificial/too
     literal. Fold into the voicing edit pass (and update voice-guide §5.1 "Hub
     — Title case" to match this consistent rule).
2. **Phase 2 — Content adds.** (IN PROGRESS)
   - **COG translations — ✅ DONE 2026-06-24.** 22 all-caps `COG` → cog/Cog
     across keyconcepts + code comments (8 files); verified zero remain;
     protected mnemonics/`DEBUG_COGS` untouched.
   - **OBS-08 — ✅ DONE.** §1.3 LUT memory-layout note (reframed — cog RAM is the
     constrained resource; plan the split early).
   - **OBS-09 — ✅ DONE.** §1.3.2 pitfall + RDLUT + WRLUT entry notes, grounded in
     the briefing, honoring its §7 guardrails ("does not assemble," full LUT
     reachable, no `##` push, no numeric opcodes).
   - **CLASS-B Operation line [D2] — ✅ DONE + VERIFIED 2026-06-24. 206 lines.**
     Verification: per-file counts match the mapping exactly; all 12 NF-special
     lines present; backticks clean (the one `\\\`` hit is legit glossary content
     for the `\` prefix); all fences even; every Operation line sits above its
     Result. CAUGHT a sub-agent over-report (a–l agent claimed ADDCT1/2/3 + ADDPIX
     inserted; they were NOT — verified by grep, fixed by hand). Apply split:
     a–l (85 incl. 2 hand-fixes) + m–z (121).
     - Conventions ✅: voice-guide §6.3 redefined (compact pseudocode, supersedes
       the unused procedural-list def); AUTHORING-CONVENTIONS §1.1 + template slot.
     - Mapping built (`scratchpad/operation-line-mapping.md`): 279 entries —
       145 INC / 46 SKIP / 49 BORD / 39 NF.
     - **Adjudication (Stephen approved):** apply a line to all INC + all 49 BORD
       (each has a non-default flag / non-obvious operand-order / side effect) +
       12 sourced NF lines (ADDCT, ADDPIX, AUGD, AUGS, COGATN, GETXACC, MULPIX,
       MUXNIBS, MUXNITS, QEXP, QLOG, REP). **Demoted to SKIP** (no clean faithful
       one-line): ALTI, RESI0-3/RETI0-3, + the config/command/PRNG NF set. Net
       ~206 entries get a line, ~73 skipped.
     - **Apply:** two parallel agents (files a–l, m–z) inserting each line after the
       entry's syntax-block `---`, before **Result:**. Verify on completion
       (backtick-unescaping, fence balance, count). Grouped headers = one shared
       line. Source = Parallax CSV col-5 (no inference).
3. **Phase 3 — Cross-ref + alternatives. ✅ DONE 2026-06-24.**
   - **Discovery:** two read-only full-instruction-set scans. SCAN-1 (CLASS-C
     cross-refs) = 20 grounded findings (CR-01..CR-20) + 4 held UNVERIFIED (incl.
     MULPIX→SETPIX, which was *incorrect* — MULPIX has no SETPIX dependency).
     SCAN-2 (OBS-01 alternatives) = 3 grounded (ALT-01/02/03) + 5 logged
     non-findings (TJ/DJNZ/GETBYTE/MOVBYTS/SCA-as-idiom all ruled out).
   - **SCAN-2 applied (all stacked per D1, with cycle deltas):** ALT-01 §2.2.4
     min/max cmp+mov (6 clk) → FLE/FGE (4→2 clk); ALT-02 §3.5.3 conditional
     assignment → FLE/FGE; ALT-03 §3.5.4 ABS fast-path (4→2 clk) promoted to a
     stacked comparison.
   - **🔴 BONUS DEFECT fixed (in ALT-02):** §3.5.3 line 400 claimed the min/max
     idiom "takes exactly three clock cycles" — corrected to 6 clk (3 slots ×
     2 clk; a cancelled conditional still costs its slot, per §4.4.3).
   - **SCAN-1 applied — 19 of 20** in house style (prose-integrated, plain-uppercase
     mnemonics, NOT arrow/bold callouts).
     Part II (2 agents, every insertion grep-verified): CR-01 MUL→SCA, CR-02
     MULS→SCAS, CR-06 MUXQ→SETQ, CR-03 ENCOD→DECOD, CR-04 BLNPIX→SETPIV, CR-05
     INCMOD→DECMOD, CR-07 QMUL→MUL/GETQX/GETQY, CR-08 QDIV→SETQ/GETQX/GETQY, CR-09
     NEGC→ABS, CR-10 RDLONG→SETQ2, CR-11 WRLONG→SETQ/SETQ2, CR-12 SUB→SUBX/SUBSX.
     Part I (by hand): CR-15 §4.5.2→POLLCT/JCT, CR-16 §5.4.4→JSE/JNSE, CR-17
     §6.4→ALTD/ALTS, CR-18 §3.6.2→MUXNIBS/MUXNITS, CR-19 §3.5.1→TESTB, CR-20
     §5.2.3→BIT* family.
   - **CR-13 NOT applied — verified already satisfied.** §5.1.1 line 25 (right after
     the CORDIC table, same section) already names GETQX/GETQY with links; the
     finding's premise ("not named until §5.1.7") inverted on close reading.
   - **Verification:** all 12 Part II insertions grep-confirmed; no HTML-entity
     leaks (files hold literal `>>`); all code-fence counts even in all 14 touched
     files; all newly-added PASM2 code lines ≤ K=76 (trimmed one 85-char comment
     in §2.2.4). CR-08's "after 55 clocks" confirmed grounded (§5.1.2 documents the
     55-clock CORDIC period).
   - **Files touched:** part-i ch02/03/04/05/06; part-ii instructions-b/e/i/m/n/q/r/s/w.
4. **Phase 4 — Release.** One render + verify + release with version bump
   (released v3.0.0 → bump).

### Research / sweep threads (2026-06-24)
- **CLASS-A discovery sweep:** read-only, doc-wide voicing-violation enumeration
  (4 banned patterns + oversell-without-cost). Feeds Phase 1 step 2 edit pass.
- **R1 (D2 sourcing + selection): ✅ COMPLETE 2026-06-24.** Report:
  `scratchpad/R1-operation-line-sourcing.md`. Findings:
  - **Source of truth = Parallax CSV column 5** (`P2 Instructions v35 - Rev B_C
    Silicon - Sheet1.csv`): 491 rows / 440 unique mnemonics, 0 empty; 326 carry a
    formal `=` expression with bit-slice + flag notation, 165 are prose. Same
    source appendix-c was derived from. Cross-check against P2KB YAML + appendix-c.
  - **pnut-ts JSON is UNUSABLE** for this (generic template descriptions, zero
    operation semantics) — never source the line from it.
  - **Format:** `**Operation:** \`D = signed(D[15:0] × S[15:0])\`; \`Z = (S==0) OR (D==0)\``
    — placed after the syntax line / before **Result:**; monospace; result, then
    C, then Z; keep CSV bit-slice/brace notation; strip the CSV `*` footnote.
  - **Selection:** add the line when the result/flag formula is NOT reconstructable
    from mnemonic+syntax+one-liner (bit-field shuffles, slice-indexed, signed/
    scaled math, non-obvious flag derivations, pixel ops, ALT side effects,
    CRC/encode). Skip plain whole-register ops (MOV/ADD/SUB/AND/OR/CMP/NOP) with
    default value+flags. Est. ~180–210 get one, ~140–170 skipped.
  - **Nuance to decide:** cleanest policy may be "Operation line whenever the
    *flags* aren't default, even if the result is obvious" (covers AND/OR/XOR
    `C=parity`, shift/rotate carry edge-cases). → D2 format/selection refinement.
  - **Reconcile with voice-guide §6.3** (existing "Operation" = procedural list):
    decide whether the compact pseudocode replaces/augments it. (Open for Phase 2.)
- **R2 (OBS-09): ✅ COMPLETE 2026-06-24 — VERDICT CONFIRMED.** Report:
  `scratchpad/R2-lut-immediate-limit.md`. Primary (Silicon Doc bit-table) +
  empirical (compiler rejects bit-8 literals) both confirm. See OBS-09 above.
  Spillover: KB `p2kbPasm2Rdlut` prose gap → corrections register.
