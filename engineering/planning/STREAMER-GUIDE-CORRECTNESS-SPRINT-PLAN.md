# Streamer Guide Correctness — Sprint Plan

**Document:** P2 Streamer Programming Guide (`manual:p2-streamer-programming-guide`)
**Created:** 2026-08-19
**Status:** 🟡 PLAN — open questions in §0 must close before `sprint-start`.
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

### Q1 — The F-272 bench run — **ANSWERED 2026-08-19: approved in principle.**

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

### Q2 — Release number: **v1.1.0** or v1.0.10? *(Recommendation: v1.1.0.)*

Four wrong facts corrected in a released document, plus genuinely new material (the
`S[11:0]` field, the DAC-pin requirement, a declared example contract). That is more
than a patch. **Recommendation: v1.1.0.**

### Q3 — Does the metadata single-source conversion ride along? *(Recommendation: yes.)*

`PLATFORM-FEATURE-ADOPTION.md` shows this document **⏳ on metadata single-source**
(cross-ref already ✅). Every ⏳ is work owed at *this* release, and `prepare-manual`
Step 4 will surface it anyway. F-301's lesson is that deferring it is precisely how it
gets passed over. **Recommendation: include as §11.** Mechanical; no render risk.

### Q4 — Is a second sweep wanted beyond the audit? *(Recommendation: no.)*

The audit swept all 37 code blocks and every factual claim across six regions, with an
adversarial refutation pass. §10's labelling work forces a fresh per-block decision on
every block anyway, which is a better second look than repeating the same sweep.

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

**§1b — the bench run that settles the streamer-fed DAC mode constant (F-272).**

The open half is the `%TT` field for a DAC pin the **streamer** writes. Both candidate
forms compile, so only silicon decides.

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
| — | `S[11:0]` appears nowhere; only an unexplained code comment at `:1424` hints it exists |

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

## §7 — Rebuild §17.2 DDS Waveform Generation *(gated on Q1/F-272)*

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

**Verification.** *Normal:* every symbol defined or cross-referenced; `pnut-ts -q`
compiles the assembled example clean. *Edge:* the §17.1 forward promise is now kept —
read both sections in sequence. *Error:* if F-272 is unresolved, this section ships as an
explicitly **labelled fragment** under §10's contract, not as a worked example wearing
worked-example furniture. That is the whole lesson of this sprint.

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

## §11 — Platform: metadata single-source adoption *(pending Q3)*

`PLATFORM-FEATURE-ADOPTION.md` carries this document **⏳** on metadata single-source
(cross-ref ✅). Convert per the mechanism recorded there: identity strings live once in
`request.json` metadata and reach both the PDF info dictionary and the cover.
`metadata.version` becomes the **bare** number for a converted document.

**Verification.** *Normal:* rendered PDF has populated Title/Author/Subject. *Edge:*
cover text unchanged in presentation. *Error:* flip the tracker row to ✅ **only after
the rendered PDF is inspected**, never on staging.

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
6. `release-manual` for promotion, roster, and the ledger line.

**Known non-goals.** Chip review (roster `⏳`) is not gated on this sprint. F-299 is
polish. The 11 pre-existing `audit-register-hygiene.py` violations in
`P2KB-CORRECTION-FINDINGS.md` are unrelated to this manual and are carved out — each
needs its own per-finding evidence.
