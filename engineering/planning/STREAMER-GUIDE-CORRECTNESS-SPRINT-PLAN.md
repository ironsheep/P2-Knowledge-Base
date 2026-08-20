# Streamer Guide Correctness — Sprint Plan

**Document:** P2 Streamer Programming Guide (`manual:p2-streamer-programming-guide`)
**Created:** 2026-08-19
**Status:** 🟢 **RESEARCH COMPLETE — §0 IS EMPTY (2026-08-20).** Q1–Q4 all closed. Two sweeps
have run (the original class audit and a four-angle second sweep on orthogonal axes), plus a
cross-artifact sweep. **17 findings** across §1–§16. Ready for `plan-to-tasks`.

**Version: v1.1.0.**

**Scope (Stephen, 2026-08-20):** *this manual only* — correct its content and land every pending
update it owes. Errors found in **other** artifacts are registered as **F-302…F-305** and
deliberately excluded here; the co-release judgement is taken at the release gate (§13 and
release-verification step 6).
**Entry state:** v1.0.9 released 2026-08-19 07:29, 76pp (`PUBLICATION-ROSTER.md:46,95`).
Roster: Draft ✅ Assets ✅ Platform ✅ **Chip ⏳** Comm ✅ Released ✅.

**Origin:** the 2026-08-19 class audit in
`manuals/p2-streamer-programming-guide/audit/halfbaked-class-audit-2026-08-19.md`
(git-ignored workspace history), triggered by Christof Eb.'s forum review of §17.2.
Every finding below was hand-verified against the Silicon Doc by the plan author;
line numbers are `opus-master/streamer-body.md` at HEAD unless stated.

**Scope as instructed:** *"fixing all issues in this manual."* Withdrawal is
therefore off the table — this sprint corrects and re-releases.

## Working rules (apply to every item)

- Edit **`manuals/p2-streamer-programming-guide/opus-master/`**, never the workspace render.
- Code fences ` ```pasm2 ` / ` ```spin2 `; prose callouts as `:::`. Code ≤ **K = 76**
  (`creation-guide.md:696`); code lines do not wrap.
- Show the compiler's symbolic constants, not raw arithmetic.
- Voice: `documentation-voices-catalog.md` (house canon R1–R4) → this manual's
  `voice-guide.md` (`CONFORMANCE_GUIDES`, strength: reference).
- **Authority is the ingestion tree**, in the `DOMAIN_AUTHORITY` precedence order.
  `p2kb-mcp` is *not* authority inside this project (circular). Every corrected
  fact carries its `p2-documentation.txt:<line>` citation in the commit.
- Batch-and-verify: apply everything, then **one** re-prepare → Forge round-trip →
  read the returned PDF.
- **Bench policy (Stephen, 2026-08-19).** A bench run is allowed for any code needing
  **no hardware external to the P2** — jumper-to-itself rigs qualify, anything wanting a
  scope, generator, or breakout does not. But a run must **prove useful before it is
  proposed**: it costs far more than compile-and-verify, so it has to answer a question
  the compiler cannot. `pnut-ts` proves legality, never semantics — that gap is the only
  thing a bench run is for. This sprint proposes exactly one (§1b).

---

## §0 Open Questions — must reach empty before `sprint-start`

### Q1 — **CLOSED 2026-08-20. F-272 is resolved from documentary sources; nothing is gated.**

The research pass falsified F-272's own premise. It had recorded that the `%TT` setting for a
streamer-driven DAC *"is not stated by any source we hold."* It is — in three separate Silicon Doc
statements that together determine the whole arrangement. See the register entry; not restated
here.

**Consequences for this plan:**

- **§1b and §7 are NO LONGER GATED.** The streamer-fed DAC setup can be authored from documentary
  authority now.
- **The bench run becomes optional confirmation**, not a decision. It still qualifies under
  Stephen's policy and is still *recommended* — **F-264** proved this exact axis inverts (a
  constant mandatory in one DAC arrangement kills the output in the other), so a jumper-rig check
  is cheap insurance. But the sprint no longer waits on it.
- **§17.1's original form was right.** It shipped `P_DAC_124R_3V | P_CHANNEL` alongside
  `X_DACS_0N0_0N0`; «#221» doubted it only because the documentary basis had not been found.

*(Superseded text kept below for the reasoning that led here — the bench-policy criteria still
govern any future run.)*

### Q1 (superseded) — The F-272 bench run — approved in principle 2026-08-19.

Stephen's standing policy, stated this session: *bench runs are allowed for any code
that needs no special hardware external to the P2, but the run has to prove useful,
because it costs far more than compile-and-verify.*

**F-272 qualifies on both tests.**

*No external hardware.* The rig is **one jumper wire, P2 pin to P2 pin** — a DAC-mode
output pin strapped to an ADC-mode input pin on the same chip. No scope, no signal
generator, no breakout. This is the jumper case, not the external case.

*Provably useful, and not answerable any cheaper.* `pnut-ts` proves legality only, and
**both candidate forms compile clean** — which is exactly why the question is still
open. Only silicon separates them. The run:

- unblocks **§1b** and **§7** (rebuild §17.2), the sprint's headline deliverables;
- closes a register finding that already blocks the **P2AN001 / P2AN003 / P2AN004**
  cog-DAC re-audit, so the cost is amortised across four documents, not one section;
- returns a **binary, unambiguous** answer — one arrangement produces a varying
  voltage and the other does not.

`F-272` is `OPEN` in `P2KB-CORRECTION-FINDINGS.md` — consult the register for its
current state and reasoning; this plan does not restate it. Rig spec: **§1b** below.

**Still open:** whether the run happens *before* the authoring pass (recommended — §7
cannot be written without it) or the sprint proceeds with §7 held back as a labelled
fragment. **Recommendation: bench first.**

### Q2 — **CLOSED 2026-08-20: v1.1.0.**

Four wrong facts corrected in a released document, plus genuinely new material — the
`S[11:0]` field with its bounded-region and phase-offset bits, the DAC-pin requirement, and a
declared example contract. More than a patch.

**Bump in one place only** once §11 lands: `request.json` `metadata.version` → `1.1.0`
(bare, no `v`). The cover reads it from `\DocVersion` after conversion, so there is no second
location and no mismatch is possible.

### Q3 — **CLOSED 2026-08-20: included.** Metadata single-source rides along.

Stephen's instruction — *"get all pending updates for manuals that this needs, done"* — settles
it. `PLATFORM-FEATURE-ADOPTION.md` has this document **⏳ on metadata single-source** (cross-ref
already ✅); that is a pending update this manual owes, so it is in scope as **§11**.

Current state, researched rather than assumed:

| Where | Now | After |
|---|---|---|
| `request.json` `metadata.version` | `"v1.0.9"` — **carries a `v` prefix** | the **bare** number (the cover supplies the word "Version") |
| `front-matter.md:24` | hardcoded `{\large August 2026\par}` | `\DocDate` |
| `front-matter.md:26` | hardcoded `{\large\color{blue}Version 1.0.9\par}` | `\DocVersion` |

The `v` prefix is the trap: converted documents take the bare number, so the conversion is a
two-part edit, not a one-part one.

### Q4 — **CLOSED 2026-08-20: the second sweep RAN, and it was right to.** Recommendation reversed.

I had recommended **no**, arguing §10's labelling pass was a better second look. **That was
wrong, and the reasoning was weak in three ways:**

1. **The substitution didn't hold.** §10 is a *code-block* pass. The highest-severity findings —
   RGBI8, the `SETSCP` literal, Appendix A, the 512 claim — are prose-and-table facts. §10 does
   not cover that ground.
2. **The evidence was already in front of me.** Everything found *after* the first sweep, the
   first sweep had missed: both wrong diagrams (its agents were scoped to `streamer-body.md`;
   the `.sty` was never in scope), the fourth 512 site at `:1424`, Appendix C's arithmetic,
   Appendix B's consistency. Its region 6 covered Appendices B and C and reported on neither.
3. **It reproduced the pathology.** "We already looked" is exactly what was true, and wrong,
   nine times over in this document's history.

There is also a gap no re-run of the first sweep could close: it checked claims the manual
**makes**. It structurally cannot find what the manual **never says** — which is how `S[11:0]`
stayed missing for nine releases. We found that because Christof asked, not because we swept.

**So a second sweep ran on four orthogonal angles** — omissions against the Silicon Doc,
self-consistency with no external authority, numeric/bit-pattern recomputation, and the non-body
artifacts. **8 raw findings → 8 CONFIRMED, 0 refuted** by the adversarial pass (two were the same
contradiction found independently by two angles, so **7 distinct**). Results: **§16**.

---

## §1 — The DAC pin requirement: state it, then use it everywhere

**Finding S-1 (critical, book-wide).** This is the root of the reviewer's *"to which
pin(s) will there be output?"*, and it is not confined to §17.2.

**Authority — `sources/silicon-doc/p2-documentation.txt:3521-3523`, verbatim:**

> "The streamer has four DAC output channels, X0, X1, X2 and X3, which can selectively
> override the four SETDACS values on a per-DAC basis. To bring out the data as a
> voltage on a pin, that pin must be set to DAC mode with the COGID embedded, via
> WRPIN, and DIR must be set high."

**Current state — measured over `streamer-body.md`, not recalled:**

| Search | Occurrences |
|---|---|
| `P_DAC` (any DAC pin-mode constant) | **0** |
| `COGID` | **0** |
| `SETDACS` | 1 — an unexplained legend entry, `:764` |
| `"DAC mode"` | **1** — `:1710`, a three-word Appendix D checklist item |
| `wrpin` configuring a **DAC** pin | **0** (all four `wrpin` uses are ADC ×2, HDMI, SPI clock) |

Chapter 11 is titled *"DAC Channel Configuration"* and teaches the `%dddd` routing field
(`:743`) and the channel→pin-LSB mapping (`:772`) — but never the step that makes a DAC
pin emit a voltage.

**This is an omission, not a scope boundary.** The front-matter scope statement
(`front-matter.md:153`) assumes only cog/hub architecture, basic PASM2, and RDFAST/WRFAST;
and the manual configures **ADC** pins twice in detail (`:606`, `:1380`). Pin
configuration is plainly in scope; only the DAC half is missing.

**§1a — citable now.** Add a new §11.0 *"Getting a DAC channel onto a pin"* before the
routing table, stating the WRPIN-DAC-mode + `DIRH` requirement with the citation above.
Cross-reference it from every DAC-routing example: §5.1, §5.2, §6.1, §6.2, §7.3, §11.3
(all four), §15.1, §17.2.

**§1b — the streamer-fed DAC setup — NOW CITABLE (F-272 resolved 2026-08-20).**

What §11.0 must teach, all of it from the Silicon Doc (see the F-272 register entry for the
verbatim quotes and line numbers — this plan points, it does not restate):

- **`%TT = %01`** (`P_CHANNEL`) is the cog-DAC-channel arrangement — required whenever the
  streamer supplies the value.
- **`M[3:0]` carries the COGID** — the cog whose DAC channels drive this pin.
- **`DIRH`** the pin.
- **The channel is chosen by the pin's two low bits**, not by the mode word — which is why
  §11.2's existing channel↔pin-LSB table is correct and becomes load-bearing here.
- **The contrast that makes it stick:** the *level-driven* DAC is `%TT = %00` with `M[7:0]` as
  the level and **no `P_CHANNEL`** — and per **F-264**, adding `P_CHANNEL` there **kills** the
  output. Same constant, opposite effect, decided by who supplies the value. Teach both, adjacent.

Pick the impedance constant from the four the KB carries: `P_DAC_124R_3V`, `P_DAC_990R_3V`,
`P_DAC_600R_2V`, `P_DAC_75R_2V`.

**§1b-bench — optional confirmation (recommended, not gating).**

Given F-264's demonstrated inversion on this exact axis, confirm on silicon before release.
It is one jumper and no external hardware, so it clears Stephen's policy.

**Rig — one jumper, no external hardware.** Strap a DAC-capable pin to an ADC-capable
pin on the same P2 (`dac_pin` → `adc_pin`, respecting §11.2's channel/pin-LSB rule).
Read the voltage back through the ADC pin. Report via `debug()`; compile with
`pnut-ts -d`.

**Run the control first, and stop if it fails.** The rig must be proven able to see a
DAC voltage *at all* before any test reading means anything.

| Stage | Arrangement | Purpose | Expected |
|---|---|---|---|
| **C — control** | Level-driven DAC exactly as the Silicon Doc's own worked program does it (`p2-documentation.txt:4225-4305`): streamer DAC routing **off**, `TT = %00`, level written by re-issuing `WRPIN` with the power byte inserted | Prove the jumper, the ADC pin, and the reader work | ADC tracks the written level across a ramp |
| **T0 — test** | Streamer-fed DAC (`X_DACS_*` routing on, streamer supplying values), `TT = %00` | Does the streamer reach the pin without `P_CHANNEL`? | unknown — this is the question |
| **T1 — test** | Same, with `P_CHANNEL` (`TT = %01`) | Does selecting the cog DAC channel enable it? | unknown — this is the question |

**Reading the result.** Exactly one of T0/T1 should produce a varying voltage tracking
the streamed values; the other should sit flat. That identifies the required `%TT`.

**Failure handling — doubt the instrument first.** If **C** does not track, the rig is
wrong, not the silicon: **stop and confirm the measurement** (jumper seated, pin LSB
matches the DAC channel per §11.2, ADC gain matched to a directly-wired signal — a
high-gain constant saturates on a wired signal and reads constant). Do **not**
interpret T0/T1 against a control that never responded. If **both** T0 and T1 track, or
**neither** does, that is a real finding and F-272's premise needs revisiting — record
it and do not force a conclusion.

**Where the result goes.** Accepted result → `P2-EMPIRICAL-FINDINGS.md` (EF entry) and
the test replicated to `external-sources/hardware-verification/`, per the trust chain.
Then F-272's status flips in the register, and §1b + §7 unblock.

**Verification.**
- *Normal:* `grep -c "P_DAC" streamer-body.md` > 0; §11.0 exists and is referenced from
  every DAC example listed above.
- *Edge:* §15.1 VGA — the manual's best program — now either configures its DAC pins or
  states explicitly which setup it assumes. It cannot silently keep the gap.
- *Error:* no example asserts a `%TT` value unless F-272 closed. A `grep` for
  `P_CHANNEL` returning a hit while F-272 is still `OPEN` is a fail.

---

## §2 — §9.2: the `SETSCP` literal is numerically wrong

**Finding S-2 (critical).** `:603`, inside the titled *"ADC Configuration Example"*:

```pasm2
        setscp  #%1_0000        ' enable, D[5:2]=%0000 -> pin base 0
```

**Authority — `p2-documentation.txt:8828`:** *"`SETSCP {#}D` — D[6] enables the SCOPE
data pipe, D[5:2] selects the 4-pin block."*

`%1_0000` = 16. Underscores are digit grouping, not field delimiters.

| Field | Comment claims | Literal gives |
|---|---|---|
| `D[6]` enable | enabled | **0 — pipe DISABLED** |
| `D[5:2]` block | `%0000` → pins 0–3 | **4 → pins 16–19** |

**Fix:** `#%100_0000` (64). The prose at `:597` already states the layout correctly — only
the literal is wrong.

**Note for the retrospective:** this shipped in v1.0.9, the release that rewrote §9.2 end
to end to fix the `adc_pin<<17` bug. The pass that corrected the mechanism got the
constant wrong. `setscp` appears exactly once, so there was no second usage to disagree
with it.

**Verification.** *Normal:* recompute both fields from the new literal in the commit
message. *Edge:* confirm `setscp` still appears exactly once (no second, divergent usage
introduced). *Error:* the inline comment must match the literal field-by-field — the
defect was comment-vs-value drift, so the check is agreement, not plausibility.

---

## §3 — RGBI8 is not a 2:2:2:2 format. Three locations

**Finding S-3 (critical).**

**Authority — `p2-documentation.txt:3800`:** *"RGBI8 mode uses the top three bits of the
8-bit pixel values as colors and the bottom 5 bits as luminance values"* — followed
(`:3801-3907`) by a `P[7:5]`→Color table carrying **the same eight named colours as
LUMA8**, with X3..X0 driven by the luminance field bit-replicated as `P[4,3,2,1,0,4,3,2]`.

RGBI8 is structurally **identical to LUMA8** — a 3-bit colour select plus an intensity
value. It has no per-channel R/G/B fields.

| Line | Current text | Action |
|---|---|---|
| 519 | *"**RGBI8 (2:2:2:2):** Two bits each for red, green, and blue, plus a 2-bit intensity field."* | Rewrite to colour-select + 5-bit luminance; state the LUMA8 kinship explicitly |
| 497 | Mode table Format column: `RGBI 2:2:2:2` | Correct the label |
| 945 | §13.1 symbol table Description: `RGBI 2:2:2:2` | Correct the label |
| **diagram** | `\DiagRgbFormats` in `workspace/p2-streamer-programming-guide/templates/p2kb-streamer-diagrams.sty` draws RGBI8 as `R 2 \| G 2 \| B 2 \| I 2` | **Redraw** as colour-select + luminance. Added 2026-08-20 — a fourth in-manual site, and a *template* edit (see the staging note below) |

**A ready-made model exists.** The **P2 Debug Window Manual** (released v1.1.3)
`ch04-bitmap.md:100` states it correctly — *"Upper 3 bits select a color, lower 5 bits
are intensity"* — and contrasts it against LUMA8 immediately above. Copy that framing
rather than re-deriving it.

**Staging consequence.** The diagram lives in the **workspace template**, not in
`opus-master` (this manual has no `opus-master/templates/`). Fixing it means
`p2kb-streamer-diagrams.sty` must be **staged to outbound** alongside the markdown — the
release verification in this plan originally assumed a markdown-only bundle. Same applies
to §4's diagram fix.

**The tell to keep in the fix:** §7.2 describes LUMA8 **correctly** four lines above
(`:510`). Say plainly that RGBI8 is that same mechanism with the colour select moved into
the pixel — the near-miss is what made the error survive nine releases.

**Verification.** *Normal:* all three locations agree with `:3800`. *Edge:* `:502`
(memory-budget prose) lists RGBI8 as a 1-byte format — still true, must not be broken.
*Error:* `grep -n "2:2:2:2" streamer-body.md` returns **zero** hits.

---

## §4 — The DDS LUT is not fixed at 512 entries; `S[11:0]` is undocumented

**Finding S-4 (critical). Registered as `F-302`** in `P2KB-CORRECTION-FINDINGS.md` —
consult the register for the authority table and the KB-side correction; this plan does
not restate it.

**Manual-side locations:**

| Line | Defect |
|---|---|
| 648 | `LUT[NCO[30:22]]` given as *the* indexing rule — true only at loop size 512 |
| 674 | *"The LUT **must** contain 512 entries"* — **false** |
| 1458 | §17.2 tip: *"The NCO steps through **the 512 entries**"* |
| **1424** | *"…invert none, **512-entry LUT window**"* — **a defect line, not just a hint.** Corrected classification 2026-08-20: the earlier draft of this plan called it "an unexplained code comment," but it asserts 512 as fact. Fix it, and let it be the place that points at the new section |
| **diagram** | `\DiagDdsGoertzel` renders `entry = LUT[NCO[30:22]]` — same 512-only claim in the picture. Template edit; see §3's staging note |

**Deliverable is larger than the correction.** Add the `S[11:0]` field to Chapter 10 as
its own section: the eight loop sizes with their NCO index bits, the `%A` bounded-region
bits, and the `%T` phase-offset bits. §17.2's headline applications include **RF
modulation**, and `%T` is the field that performs it — today we document the application
and not the mechanism it needs.

**Verification.** *Normal:* the eight-row table matches the register's authority table
exactly. *Edge:* `:1424`'s code comment (`512-entry LUT window`) now resolves to the new
section instead of dangling. *Error:* `grep -n "must contain 512" streamer-body.md`
returns zero.

---

## §5 — Appendix A's `D[19:16]` column is wrong in 15 rows

**Finding S-5 (critical).** Appendix A is titled *"Complete Mode Encoding Table."*

**This is a recurrence in a declared-fragile area.** `MANUAL-DESCRIPTOR.md:23` already
lists *"Mode reference pin/DAC-channel columns — origin of F-154 (streamer-symbols
transposition) + manual H-4/M-1."* The area was flagged; the appendix was not re-checked
against it.

**Authority.** `p2-documentation.txt:2995-3020` (Immediate) and `:3125-3145`
(RDFAST/WFBYTE) print the identical 12-row field sequence:
`pppa · pp0a · pp1a · p00a · p01a · p10a · 0110 · 0111 · 1110 · 1111 · 0000 · 0001`.
The `%a` bit is real — `:3653-3654`: *"Some of these modes have the %a bit in D[16] to
reorder the data sequence within the individual bytes to top-first when %a = 1."*

| Rows | Manual shows | Silicon Doc | Defect |
|---|---|---|---|
| 1544–1549 (IMM 1/2/4-pin) | `%0000` `%0000` `%0010` `%0000` `%0010` `%0100` | `pppa` `pp0a` `pp1a` `p00a` `p01a` `p10a` | pin-select and `a` bits hardcoded to 0 — forces every IMM mode onto pin 0 |
| 1561–1565 (RFBYTE 2/4-pin) | `%ppp0`, `%pp00` | `pp0a`, `p00a` | wrong p-field width; `a` bit dropped |
| 1566–1568 (RFBYTE 8-pin) | `%p000`+6/+7/+$E | `0110` `0111` `1110` | invents a free `D[19]` bit that does not exist |
| 1578–1585 (WFBYTE mirror) | same shapes | same as RFBYTE | identical defects |
| 1594–1595 (DDS/Goertzel) | `%0111` | `p111` (from `1111 dddd 0ppp p111`, `:3484`) | hardcodes the low bit of the four-pin-block selector |

**The DDS row contradicts the manual itself:** `:1004` correctly states `adc_base<<17`
addresses the block field `D[22:19]`, which requires `D[19]` live.

**Verification.** *Normal:* every row matches the Silicon Doc sequence. *Edge:*
`X_ALT_ON` is used at §13.4 and §16.1 — the `a` bit must now be visible in the appendix
that documents it. *Error:* cross-check Appendix A against §13.1's symbol values and
§12.2's sub-pin tables; all three must agree. Disagreement between the manual's own
tables is the failure mode that produced this.

---

## §6 — Appendix D's Goertzel checklist contradicts §17.1

**Finding S-6 (major).** `:1712-1721`, *"Symptom: Goertzel Results Invalid."*

The checklist omits the two causes §17.1 identifies as dominant:

1. **`S[15:12] = 0` sums nothing** — §17.1: *"zero sums nothing, and every magnitude
   reads as noise."*
2. **The ADC pin must be RAW** — mode field `%00000`, DIR **not** set.

Worse, item 2 reads *"ADC pin configured for ADC mode"* — which is §9.2's requirement,
where `DIRH` **is** required. §17.1 spends a paragraph establishing that Goertzel is the
opposite case. A reader following Appendix D configures the pin the §9.2 way and gets the
silent zero the chapter warns about.

**Fix:** add both causes as items 1 and 2, and disambiguate the existing item so it names
the Goertzel requirement (raw bitstream, no smart-pin mode, DIR low) and points at the
§9.2 contrast rather than echoing it.

**Verification.** *Normal:* both causes present. *Edge:* the ADC-mode item distinguishes
§9.2 from §17.1 explicitly. *Error:* the checklist and §17.1 must not disagree — read
them side by side; a troubleshooting appendix that contradicts its chapter is worse than
none.

---

## §7 — Rebuild §17.2 DDS Waveform Generation *(UNGATED — F-272 resolved 2026-08-20)*

**Finding S-7 (major).** `git log -S` on its opening sentence returns exactly one commit:
`10bb35d5 "Add P2 Streamer Programming Guide (WIP)"`. **Never edited since.**

| Test | Defect |
|---|---|
| Undefined symbol | `dds_mode` appears **once in the whole manual** — the section's central symbol does not exist (§17.1 defines `dds_cmd`) |
| Phantom data | `waveform_table` appears **once**. No format, size, amplitude, or build code |
| No output path | No DAC routing symbol, no pin, no `wrpin`/`dirh` — see §1 |
| False constraint | The "512 entries" tip — see §4 |
| Broken promise | `:1383` states *"that side is §17.2, and **the DAC routing field is what turns it on**."* §17.2 never mentions DAC routing |

**Target:** a worked example to the §15.1 standard — a defined mode long, an
`X_DACS_*` routing symbol, DAC pin configuration per §1, a shown `waveform_table` with
its amplitude rule (SINC1 ±127 / SINC2 ±10, currently only in §17.1's `::: hardware`
block), and declared `res` storage. Cross-reference §10.3's build loop rather than
duplicating it.

**The DAC setup this example needs is now citable** — `%TT = %01` (`P_CHANNEL`), COGID in
`M[3:0]`, `DIRH`, channel by pin LSBs (§1b). §17.1's original `P_DAC_124R_3V | P_CHANNEL`
form was correct; reuse it here rather than re-deriving.

**Verification.** *Normal:* every symbol defined or cross-referenced; `pnut-ts -q`
compiles the assembled example clean. *Edge:* the §17.1 forward promise is now kept —
read both sections in sequence. *Error:* if the optional §1b-bench run contradicts the
documentary reading, **stop and confirm the measurement** before changing the text —
empirical outranks documentary here, but a rig that never produced a control reading is
not empirical. Should it survive confirmation and still disagree, that is a new register
finding, not a quiet edit.

---

## §8 — §15.2 HDMI and §15.3 Composite: the same furniture, the same problem

**Finding S-8 (major).** Both use §17.2's exact shape (prose → **Configuration:** → fence).

- **§15.2 HDMI** (`:1242`) — `hdmi_base` appears twice, both uses, never assigned; the
  block sets mode, pins and NCO but **issues no streamer command**. Its three `:::`
  blocks are excellent: the prose got attention, the code did not.
- **§15.3 Composite** (`:1272`) — `cy_ntsc`, `ci_ntsc`, `cq_ntsc` appear **once each**.
  The colour-matrix coefficients — the entire difficulty of composite video — are three
  undefined symbols. No streamer command, and no `:::` note of any kind. **This is the
  closest twin to §17.2 in the book.**

**Decision required per section:** complete it to the §15.1 standard, or label it a
fragment under §10 and say what it omits. Either is honest; the current state is not.
Supply the coefficients only if they can be cited — otherwise say where they come from.

**Verification.** *Normal:* each section is either runnable or labelled. *Edge:* §15.2's
three `:::` blocks (observed display limits) must survive the rework intact — they are
good and hard-won. *Error:* no undefined symbol remains inside a block presented as a
recipe.

---

## §9 — §10.1's mode pattern silently omits the `%dddd` nibble

**Finding S-9 (minor).** `:639` prints `%1111_0ppp_p111`. The Silicon Doc (`:3484`)
writes the same encoding as `1111 dddd 0ppp p111`. The manual's form is `D[31:28]` +
`D[23:16]` with `D[27:24]` skipped, so it reads as a contiguous 12-bit pattern and is not
one. Correct as a lookup, misleading as a bit pattern — and it is the same 4-bit
misalignment §5 gets wrong outright.

**Fix:** show the full 16-bit form, or mark the elision explicitly.

**Verification.** *Normal:* the pattern is unambiguous about which bits it covers.
*Error:* consistent with the Appendix A repair in §5 — the two must not disagree.

---

## §10 — The declared example contract *(the systemic fix)*

**Finding S-10, and the reason this sprint is not a point-fix.**

Every improvement pass this manual has had was **finding-driven**: it deepened the
sections it was pointed at and never swept the ones it was not. Untouched sections keep
first-draft depth beside excellent neighbours, and **because both wear identical section
furniture the variance is invisible from inside the document.** §17.1 (hardware-verified,
measured selectivity figures) and §17.2 (never edited) are adjacent, in one chapter.

The audit's nine **refuted** findings prove the manual *already has* a legitimate pattern
genre (§18.1, §18.3, §16.1, §14.4 — parameterised placeholders in blocks framed as
patterns). It simply never told the reader that genre exists.

**Deliverables:**

1. **Declare the contract** in `creation-guide.md`: every code block is either a
   **worked example** — runnable, every symbol defined or cross-referenced, output path
   shown — or is **visibly labelled** a fragment/pattern with what it omits.
2. **Add a `fragile_areas` gate** to `MANUAL-DESCRIPTOR.md` so `document-audit` enforces
   it, in the style of the existing rows. Include the diagnostic tests (undefined symbol,
   phantom data, no output path, false constraint, no storage) — the audit doc carries
   the wording.
3. **Apply the label to every one of the 37 code blocks.** This is the pass that finds the
   next §17.2.
4. **Relocate the two rules that prevent this class.** Both exist and are well written,
   both are in the wrong chapter: `:1004` states the `<<17` multiple-of-four rule for
   Goertzel only, and `:620` states the general *"streamer command fields are positional
   and mode-specific"* rule inside a §9.2 `::: hardware` block. `<<17` is used **21
   times**; **Chapter 12 — "Pin Selection and Control" — states neither.** Move the
   general rule to Chapter 12 and cross-reference it from §9.2 and §13.4.

**Verification.** *Normal:* all 37 blocks classified. *Edge:* the nine refuted findings
stay refuted — a pattern block correctly labelled is not a defect, and this pass must not
"fix" them into fake completeness. *Error:* Chapter 12 states the general rule; a reader
who never opens Chapter 9 can still learn it.

---

## §11 — Platform: metadata single-source adoption *(IN SCOPE — Q3 closed)*

Convert per the mechanism recorded in `PLATFORM-FEATURE-ADOPTION.md`: identity strings live
once in `request.json` metadata and reach both the PDF info dictionary and the cover via
`\DocTitle`/`\DocSubtitle`/`\DocVersion`/`\DocDate`/`\DocAuthor`. Three edits — the two
hardcoded cover lines at `front-matter.md:24,26`, and **stripping the `v` prefix** from
`request.json`'s `"version": "v1.0.9"` (converted documents carry the bare number; the cover
supplies the word "Version").

The macros carry the **value**; the cover keeps its **presentation** — do not move the
formatting into the metadata.

**Verification.** *Normal:* rendered PDF has populated Title/Author/Subject. *Edge:*
cover text unchanged in presentation. *Error:* flip the tracker row to ✅ **only after
the rendered PDF is inspected**, never on staging.

---

## §12 — Finish the voice audit *(2 of 4 mandatory findings never landed)*

`audit/voice-audit-2026-07-21.md` raised four **#9 register failures**. Verified against
the artifact 2026-08-20, not against the audit's summary:

| Finding | State |
|---|---|
| L48 §1.5 *"It is tempting to…"* (banned reader-as-foil) | ✅ fixed |
| Ch10 *"the streamer's **cleverest** mode"* | ✅ fixed |
| Ch7 *"Video is the streamer's **headline act**"* | ✅ fixed |
| **`:160` Ch3 opener — *"the single most important thing"*** | **❌ still present** |
| **`:44` §1.4 — *"you only ever care about one side at a time"*** | **❌ still present** (the audit's soft quantifier note) |

`:44` is worth more than its size: the audit flagged it as overstating *"against
DDS/Goertzel's simultaneity"* — and DDS/Goertzel is the exact mode this sprint is
correcting. Fixing §17.2 while §1.4 still tells the reader the two directions never
coincide leaves the book arguing with itself.

**Keep `:1364`** — *"the single most common way to build a Goertzel detector that appears
completely dead"* is technical severity, not self-admiration. The audit's tell was about
praising the *subject*, not about ranking failure modes.

**Cadence work is explicitly optional** — the audit recorded **PASS (at budget)**, longest
run 4, and offered margin-thinning as *"not required."* That includes the Ch17 opener
(`:1346`) and the Ch15→Ch18 four-beat run. **Stephen's call**; not scoped here by default.

**Verification.** *Normal:* both mandatory lines rewritten. *Edge:* `:1364` untouched.
*Error:* re-run the voice tells listed in the audit's method section — the fix must not
introduce a replacement tell.

---

## §13 — Errors found in OTHER artifacts: tracked, deliberately NOT in this sprint

Swept 2026-08-20 across all manuals, app notes, `deliverables/ai/P2/`,
`engineering/knowledge-base/`, and every workspace diagram template. **The same four errors
live outside this manual — in a second released manual and in the live KB.**

**Scope decision (Stephen, 2026-08-20): this sprint stays on this manual.** Those findings
are **registered, not scoped here**, so they cannot be lost:

| Finding | What it covers |
|---|---|
| **F-303** | RGBI8 `2:2:2:2` in the **released** Assembly Language Reference v3.1.6, in two live KB files, and in the cloned torture-test diagram |
| **F-304** | `modes-reference.yaml` hardcoding `D[19:16]` — plus its **mirror image**, inventing a free bit where the field is fixed |
| **F-305** | The Assembly Manual's streamer-DAC example with no `WRPIN`/`DIRH` |
| **F-302** | Widened the same day to carry the four extra `dds-goertzel.yaml` sites the sweep found |

Site-by-site detail, authorities, and the fix templates live in the register entries. **This
plan points at them and does not restate them** — the register is where their status stays
current.

### The release gate — a required step, not a reminder

**Before this manual releases, re-read F-302…F-305 and decide whether the affected artifacts
co-release.** That decision is Stephen's and is taken *at the gate*, when the corrected
Streamer Guide is in hand and the blast radius is visible — not now, and not by default.

Two facts to carry into that decision:

- The Assembly Language Reference (v3.1.6, 502pp) is **currently shipping with the RGBI8
  fabrication and a DAC example that cannot work**. It is the larger and more heavily used of
  the two manuals.
- The **live KB is served on push** — `deliverables/ai/P2/` is always "latest", so its errors
  reach agents the moment they are fixed, with no release cycle to wait for. KB work belongs
  to the `yaml` head (`yaml-knowledge-base-maintenance`); it touches 3+ files, so the
  sprint-plan overlay's **file table + design-decisions + wait-for-confirmation** rule applies
  before any YAML editing begins.

### A cloned diagram — the duplication trap

`\DiagRgbFormats` and `\DiagDdsGoertzel` were **copy-pasted** into
`workspace/p2-layout-torture-test/templates/p2kb-torture-diagrams.sty` (`:176`, `:207`),
carrying both bugs. `\DiagRgbFormats` **is invoked** there
(`P2-Layout-Torture-Test.md:836`), so the bad diagram renders into every torture-test
build; `\DiagDdsGoertzel` is currently dead code in that template but is a copy source for
whatever clones next. A staged mirror also exists at
`pdf-forge/interactive-testing/templates/p2kb-torture-diagrams.sty:207`.

**This is exactly the duplication the plan-authoring rule warns about:** fixing one copy
and shipping the other two is the normal outcome. Decide whether the two diagram macros
become **one shared platform diagram** rather than three copies.

### Verified correct — do not "fix" these

The sweep was careful to distinguish look-alikes, and these survived row-by-row decoding:

- **Assembly Manual Appendix G's "ADC Sampling Modes" (5 rows) and "DDS/Goertzel" tables**
  — checked explicitly. `D[19:16]` genuinely *is* a fixed sub-mode selector for the ADC
  family, and the DDS/Goertzel rows are a **named-constant value table**, not a field
  template, so `p = 0` is an accurate value for that symbol rather than a false claim
  about the encoding. *Completeness caveat only:* neither table discloses that setting
  `D[19]` selects the other four-pin block.
- **`dds-goertzel.yaml:11, :18`** — `%1111_0ppp_p111` / `%1111_1ppp_p111`, exact matches,
  with the correct `D[22:19]` multiple-of-four caveat. **Use this file as the fix template.**
- **This manual's own `§4.2` (`:305`), `§10.1` (`:638-639`), `§17.1` (`:1356`), and
  `§9.2` (`:618`)** all state the field correctly. Appendix A is the outlier — the fix
  source is already inside the same book.
- **`wrpin.yaml:54`** documents the DAC/COGID mechanism correctly. §1's answer was never
  missing from the repo; it was missing from the manual.
- ~~**`dds-goertzel.yaml:203`** carries a complete worked DAC-pin setup.~~ **WITHDRAWN
  2026-08-20 («#269») — this claim was wrong and is now `F-306`.** Read end to end, that
  example configures and enables a DAC pin that *nothing ever drives*: its own `dds_cmd`
  has the `%dddd` routing nibble at `%0000` (`X_DACS_OFF`), and `P_DAC_124R_3V` carries
  `TT = %00` with `M[7:0] = 0`, so the pin is level-driven at zero and the level is never
  rewritten — the Silicon Doc program's `setbyte`/`wrpin` level-update step was dropped
  while its setup was kept. **It is not the fix template for §1.** The fix template for the
  streamer-fed arrangement is F-272's resolution (`%TT = %01`, COGID in `M[3:0]`, `DIRH`,
  channel by the pin's low two bits), corroborated on silicon by **EF-054** (`%00` = 1,408
  no-drive vs `%01` = 6,737) and **EF-055**.

**Verification.** *Normal:* every SAME_ERROR site above is either fixed or explicitly
deferred with a reason. *Edge:* the CORRECT_HERE list is untouched — a sweep that
"corrects" a correct table is the worst outcome here. *Error:* re-run the four sweep
patterns after the fixes and confirm zero SAME_ERROR hits remain.

---

## §14 — Register and audit-record hygiene for this manual

Small, and it prevents the next audit from re-deriving what is already done.

- **`audit/fanout-findings-2026-07-10.md` header is stale.** It says *"Pending human
  hand-check + class-wide sweep. **Not yet applied to the document.**"* Verified against
  the artifact: **all 8 survivors were applied** (NCO 32-bit wording `:232`, Appendix D
  long-alignment `:1684`, VGA porch order, `m_visible` `$B085`→`$BF85`, SPI `wxpin ##1`,
  §7.3 `xcont`→`xinit`, Appendix A `%pppp`→`%pppa`, §10.4 SINC2 citation). Correct the
  header to record what landed.
- **`F-278`'s Streamer annotation is stale.** `:1017` now uses the ```` ```antipattern ````
  fence and it shipped in v1.0.9. Flip that site.

**The most useful thing in this section is why S-5 happened.** The fanout audit's survivor
list included *"Appendix A RFBYTE 1-pin `%pppp` should be `pppa`."* **That one row was
fixed. The other 15 rows of the same table, with the same defect class, were never
touched** — even though the audit's own header said the class-wide sweep was **owed**. The
finding named one row; the fix corrected one row; nobody swept the table. Record this in
the retrospective: it is the class mechanism caught in our own history, and §10's contract
plus this sprint's sweep are the corrective.

---

## §15 — Index entries for the new material

The Index (`:1731`, 56 hand-authored `- term: link` bullets) needs entries for everything
this sprint adds: DAC pin configuration / DAC mode, the LUT window and its loop sizes,
phase offset / modulation, and `S[11:0]`. Index entries are hand-authored, never generated.

**Verification.** *Normal:* every new section is reachable from the Index. *Edge:*
alphabetical placement and the `\indexletter` groupings stay correct. *Error:* every new
anchor resolves — a dead Index link is worse than a missing one.

---

## §16 — Second-sweep findings (2026-08-20): 7 distinct, all confirmed

Four orthogonal angles the first audit structurally could not cover. **8 raw → 8 CONFIRMED, 0
refuted**; two angles independently found the same VGA contradiction, so 7 distinct. The two
load-bearing ones were re-verified by hand.

### S-11 — CRITICAL — Chapter 15 is titled "Video Output" and never explains the colorspace converter

Its two code blocks call **`SETCMOD`, `SETCFRQ`, `SETCY`, `SETCI`, `SETCQ`** — and the manual
never says what any of them compute. Absent entirely, verified by grep across body, front matter
and diagrams:

| Missing | Silicon Doc |
|---|---|
| The signed Y/I/Q matrix formulas and the `CMOD[4]` sign/zero-extend switch | `:4760-4776` |
| The modulator (`PHS = PHS - CFRQ`) and the **1.646 CORDIC scaling factor** | `:4777-4791` |
| The `FY/FI/FQ/FS/FIQ/FYS/FYC` terms | `:4792-4852` |
| **The `CMOD[6:5]` table has FOUR modes** — `%00` off, `%01` VGA/HDTV, `%10` Composite **+ S-Video**, `%11` Composite. §15.3 shows only `%11`; **S-Video is never mentioned in the book** | `:4853-4930` |
| The `CMOD[8:7]` DVI forward/reverse table, its RED±/GRN±/BLU±/CLK± pin assignments, and the **`P[1]` literal-vs-TMDS bit — the mechanism by which sync rides inside an HDMI stream**. §15.2 reduces all of it to *"Eight pins in sequence for TMDS pairs"* | `:4342-4467` |

This is the same shape as `S[11:0]` and larger: an entire subsystem the chapter depends on,
invisible to any audit that only checks claims the book makes.

### S-12 — MAJOR — `SETDACS` is never introduced

The instruction that sets the background level on any DAC channel the streamer is not overriding.
Its **only** appearance in the whole manual is a legend bullet at `:764` — *"`--` = No override
(SETDACS value used)"*. No syntax, no example, no statement that it exists. Yet **every `--` in
§11.1's routing table depends on it**, and §11.3's own "Stereo Audio" recipe (`X_DACS_X_X_1_0`)
leaves DAC3/DAC2 undefined without it. Authority: `:2704-2721`.

### S-13 — MAJOR — the flagship VGA program contradicts the book's own timing advice

**Hand-verified.** §3.4 says three times to use 25.0 MHz for VGA on a 20 MHz crystal:

- `:239` table — *"use 25.0 MHz pixel → 10.000 cyc/px, no jitter"*
- `:245` VGA note — *"**Standard practice is a 25.0 MHz pixel clock at 250 MHz sysclk** — exactly
  10 cycles per pixel (jitter-free)"*
- `:259` worked remedy — *"25.0 MHz @ 250 = 10.000 cyc/px → no jitter"*

§15.1 — **the manual's one complete program, and the standard §10 measures every other block
against** — then ships `pixfreq long $0CE3_BCD3 ' 25.175 MHz @ 250 MHz`: the 9.93-cyc/px value
§3.4 computes as producing ±1-cycle jitter. Unacknowledged.

**Decide which is right and make them agree.** If §15.1 is deliberate (matching real driver
practice), it needs one sentence saying so and why. Silent disagreement is the defect.

### S-14 — MINOR (but wrong, and shipped in v1.0.9) — the "$7F/$80 rails" claim

**Hand-verified arithmetic.** `:1429` states *"The DAC bytes are emitted with their MSB inverted,
so the output rails sit at `$7F` and `$80`, not `$FF` and `$00`."* Applying the manual's own
formula (§10.2, `DACn := LUT.byte[n] XOR $80`) to the manual's own amplitudes (§10.4):

| Table | DAC codes produced |
|---|---|
| SINC1 ±127 | **`$01` … `$FF`** — so `$FF` *is* reached; "not `$FF`" is false |
| SINC2 ±10 | **`$76` … `$8A`** — neither `$7F` nor `$80` is a rail |
| input `0` / `-1` | `$80` / `$7F` — **these are the zero-crossing codes** |

The callout conflates the quiescent midpoint with the extremes.

### S-15 · S-16 · S-17 — MINOR omissions

- **S-15** — for the combined ADC+pin modes (`X_1ADC8_8P_2DAC8_WFWORD`,
  `X_2ADC8_16P_4DAC8_WFLONG`), the manual never says which half of the captured word holds pin
  data and which holds ADC data, so the buffer cannot be decoded (`:3977-3979`).
- **S-16** — never states that when the count exceeds the sub-values packed in the source, **the
  last value repeats** for the remainder — stated by the Silicon Doc for every immediate and
  RDFAST family (`:3664-3683`), and §5's "small, fixed pattern" framing invites reliance on it.
- **S-17** — after a **perpetual (`$FFFF`)** command, a buffered `XZERO`/`XCONT` waits only for
  the *next NCO rollover*, not for completion — the predecessor never reaches a final rollover
  (`:3505-3512`). §4.7's general rule is stated without this exception.

### The pattern worth carrying to the retrospective

**Two of the errors in this sprint were introduced by v1.0.9 itself** — the `SETSCP` literal
(§2) and this `$7F/$80` claim (S-14) — the release that rewrote §9.2 and §17.1 from
hardware-verified work. A pass can be right about the mechanism and wrong about the arithmetic
in the same paragraph. **Numbers need recomputing even when the physics was measured.**

**Verification (all of §16).** *Normal:* each finding fixed at every location. *Edge:* S-11 is
scope-sensitive — decide how deep Chapter 15 goes into the colorspace converter versus
cross-referencing it; "document everything in `:4726-4931`" is not automatically right for a
*streamer* guide, but "call five instructions and explain none" is not defensible either.
*Error:* S-13 must end with §3.4 and §15.1 **agreeing**, not with both edited into vagueness.

---

## Verified clean — checked this pass, no work owed

Recorded so the next audit does not re-derive it, and because it is the evidence behind
"correct and re-release" rather than "withdraw."

| Area | Result |
|---|---|
| **Appendix C** frequency tables | **All 23 values arithmetically correct** — 8 NCO ratios + 15 video pixel rates, recomputed from `round(2^31 × rate / clock)` |
| **Appendix B** symbol reference | **Consistent with Appendix A** — 56 modes, no gaps; its extra 22 entries are the control/DAC symbols A correctly omits |
| **Guide layer** | `audit-guide-conformance.py --inventory` → **PASS across 45 files**; every item `[D1]`–`[D6]` deliberate |
| **5 of 7 diagrams** | `\DiagStreamerArch`, `\DiagDataFlow`, `\DiagNcoRollover`, `\DiagCommandWord`, `\DiagVgaTiming` all correct. `\DiagVgaTiming` arithmetic checks (800 px @ 25.175 MHz ≈ 31.78 µs) |
| **Fanout audit (8 survivors)** | All applied — only the header lies |
| **F-278 wrong-code fencing** | The single wrong-code block correctly uses ```` ```antipattern ```` |
| **§15.1 VGA mode-long** | `$7F01_0000` intact, and the fanout DAC-routing fix (`$BF85_0000`) landed |

**Two ironies worth keeping in the retrospective.** `\DiagCommandWord` correctly labels
`D[19:16]` *"mode-specific"* while Appendix A hardcodes it, and `\DiagStreamerArch` labels
its output *"on DAC-mode pins"* while the prose never states the DAC-mode requirement.
**Both times the diagram knew and the text did not.**

---

## Documentation Blast Radius

`DOC_AUDIT_COMMAND` run at plan time —
`python3 engineering/tools/validation/audit-guide-conformance.py --inventory`:

```
PASS  guide layer conformant across 45 file(s)
```

All reported items are `[D1]`–`[D6]` deliberate-mention classifications (lineage
references, rules quoted in order to forbid them). **No guide-layer defect is owed.**

| Artifact | In scope? | Why |
|---|---|---|
| `opus-master/streamer-body.md` | **Yes** | §1–§10 |
| `opus-master/CHANGELOG.md` | **Yes** | Always in scope. Four corrected facts + new §11.0 / `S[11:0]` material |
| `creation-guide.md` | **Yes** | §10.1 example contract |
| `MANUAL-DESCRIPTOR.md` | **Yes** | §10.2 gate row |
| `PUBLICATION-ROSTER.md` | **Yes** | Version + release line + Platform Freshness Ledger PUBLISH (owned by `release-manual`, not `prepare-manual`) |
| `PLATFORM-FEATURE-ADOPTION.md` | **Yes** (Q3) | metadata row → ✅ after PDF inspection |
| `P2KB-CORRECTION-FINDINGS.md` | **Yes** | F-302 status on KB fix; F-272 status if benched |
| `voice-guide.md` | **No** | No voice convention changes |
| `workspace/.../templates/p2kb-streamer-diagrams.sty` | **Yes** | §3 + §4 diagram fixes. **Must be staged to outbound** — the bundle is no longer markdown-only |
| `audit/fanout-findings-2026-07-10.md` header | **Yes** | §14 — stale "not yet applied" |
| `workspace/p2-layout-torture-test/templates/p2kb-torture-diagrams.sty` | **§13 decision** | Cloned copies of both wrong diagrams |
| `p2-assembly-language-manual` Appendix G | **§13 decision** | Released manual, two of the same errors |
| `deliverables/ai/P2/architecture/streamer/*.yaml`, `language/spin2/symbols/streamer-symbols.yaml` | **§13 decision** | Live KB; `yaml` head owns it |
| `deliverables/.../DOCs/` PDF + changelog copy | **Yes** | Promoted by `release-manual` |
| P2KB YAML (`p2kbArchDdsGoertzel`) | **Separate head** | F-302's KB half is `yaml-knowledge-base-maintenance`, not this sprint. Pair the releases; do not merge the work |
| Counts / sample transcripts | **None** | The manual quotes no tool output and maintains no counts |

**Duplication watch.** The `S[11:0]` table will exist in the register (F-302), the manual
(§4), and eventually the KB YAML. The manual and the KB are separate audiences and both
must carry it; **the register is the working record and must not become a third
maintained copy** — it points at the authority, per `REGISTER-CONSULTATION.md`.

---

## Release verification (whole sprint)

One Forge round-trip after **all** items land.

1. **Stop and confirm the measurement** on any gate that fires — never abandon on a single
   instrument's word. Confirm by an independent path first.
2. Pre-stage gates: code-line (K=76) · inline-code ASCII · guide conformance ·
   `pnut-ts -q` on every block now claiming to be a worked example.
3. `prepare-manual` → outbound → Stephen deploys.
4. **Read the returned PDF**, not the log: page count against 76pp entry, outline
   complete, Appendix A renders (it is a wide table in a historically overflowing area),
   the new Chapter 10 and §11.0 sections present.
5. `audit-pdf-margin-overflow.py` — tolerance is the verdict. F-299's two 6-column mode
   tables (6.1/5.3pt) are **polish, inside tolerance**; do not re-render for them, but
   confirm the §5 Appendix A edits did not push them past 20pt.
6. **THE CO-RELEASE GATE — do not skip.** With the corrected PDF in hand, re-read
   **F-302 · F-303 · F-304 · F-305** and put the decision to Stephen: do the *Assembly Language
   Reference* and the live-KB fixes release alongside this manual, or separately? This is the
   step §13 exists to protect — the findings were kept out of this sprint's scope precisely so
   this judgement could be made once, here, with the blast radius visible.
7. `release-manual` for promotion, roster, and the ledger line.

**Known non-goals.** Chip review (roster `⏳`) is not gated on this sprint. F-299 is
polish. The 11 pre-existing `audit-register-hygiene.py` violations in
`P2KB-CORRECTION-FINDINGS.md` are unrelated to this manual and are carved out — each
needs its own per-finding evidence.

---

## Section ↔ task cross-reference

Generated by `plan-to-tasks` 2026-08-20. Sprint tag **`streamer-correctness`**; 22 tasks,
`«#267»`–`«#288»`, `seq` 17–38. `seq` is the only ordering signal — declared dependencies
(recorded on `«#273»`, `«#276»`, `«#277»`, `«#280»`, `«#285»`, `«#286»`) are documentary.

| Plan § | Deliverable | Task | seq |
| ------ | ----------- | ---- | --- |
| §10 (part 1) | Declare the example contract · `MANUAL-DESCRIPTOR` gate row · relocate the two rules to Ch12 | «#267» | 17 |
| §2 | `SETSCP` literal `#%1_0000` → `#%100_0000` | «#268» | 18 |
| §1 + §16/S-12 | Chapter 11 DAC foundations: new §11.0, the `%TT` contrast, `SETDACS` | «#269» | 19 |
| §4 | DDS LUT is not fixed at 512 · new Ch10 `S[11:0]` section · `\DiagDdsGoertzel` | «#270» | 20 |
| §3 | RGBI8 is not 2:2:2:2 — 3 body sites + `\DiagRgbFormats` | «#271» | 21 |
| §5 + §9 | Appendix A `D[19:16]` (15 rows) + §10.1 mode-pattern notation, made consistent | «#272» | 22 |
| §6 | Appendix D Goertzel checklist vs §17.1 | «#273» | 23 |
| §16/S-11 | Chapter 15 colorspace converter (CMOD modes, S-Video, DVI `P[1]`) | «#274» | 24 |
| §16/S-13…S-17 | VGA pixel-clock reconciliation · `$7F/$80` codes · three omissions | «#275» | 25 |
| §7 | Rebuild §17.2 DDS Waveform Generation | «#276» | 26 |
| §8 | §15.2 HDMI / §15.3 Composite — complete or label | «#277» | 27 |
| §1b-bench | Author + compile the jumper rig (optional run; canonical env) | «#278» | 28 |
| §12 | Voice audit: `:160` and `:44` | «#279» | 29 |
| §10 (part 2) | Apply the declared label to every code block | «#280» | 30 |
| §15 | Index entries for the new material | «#281» | 31 |
| §14 | Register + audit-record hygiene (incl. F-272 headline vs status) | «#282» | 32 |
| §11 | Metadata single-source (`front-matter.md:24,26` + bare `1.1.0`) | «#283» | 33 |
| Blast radius | `CHANGELOG.md` v1.1.0 entry | «#284» | 34 |
| Release step 2 | Pre-stage gate battery (K=76 · ASCII · guide conformance · `pnut-ts -q`) | «#285» | 35 |
| Release step 3 | `prepare-manual` → outbound (markdown **+ the `.sty`**) | «#286» | 36 |
| Release steps 4–5 | Verify the returned PDF · margin overflow vs 20pt tolerance | «#287» | 37 |
| §13 + steps 6–7 | Co-release gate (F-302…F-305, Stephen's call) → `release-manual` | «#288» | 38 |

**Ordering rationale.** §10 part 1 runs first (standard before application). §10 part 2 runs
last among content tasks so every block this sprint adds is labelled in the same sweep — its
37-block count is a **subset pending measurement**, to be re-counted and re-sized after the
new sections land. The gate battery runs after every edit including the changelog, because a
verification run certifies the tree it ran against. The bench rig («#278») is container-side
authoring only; the run itself is optional and Stephen's.

**Not tasked, deliberately.** F-302…F-305 (out of scope by the 2026-08-20 scope decision;
they surface at «#288»'s gate). The 10 pre-existing `audit-register-hygiene.py` violations
(F-203, F-281, F-284, F-285, F-286, F-287, F-289, F-292, F-294, F-300) — carved out, each
needs its own per-finding evidence. §12's optional cadence work — Stephen's call, not scoped.
