# IOSP suppressed-qualifier probe — «#230», 2026-08-16

**Question.** «#214» tested damage by *removal* — calibrated qualifiers stripped from released
text — and returned NIL. But removal is the half a diff can see. The likelier exposure is
qualifiers **never written**, which no diff-based method can detect. This probe tests that.

**What is deliberately NOT the question.** Hedge density per 1k body lines measures 1.31 in the
manuals whose guides carried a word blacklist versus 5.23 in those without. That is correlation
only, heavily confounded by genre, length and era. It is the reason to look, never the answer, and
it is not cited as evidence below.

---

## Method

Content-level, not counting. Of each claim: **is this stated more absolutely than its evidence
supports?** A suppressed hedge shows up as a *confident sentence whose authority is partial* — not
as a missing word — so it cannot be grepped for. Every judgement is made against the domain
authority (the ingestion tree, empirical findings first), never against how the sentence reads.

**Sampling was risk-weighted, not random.** A suppressed qualifier can only exist where the
evidence is partial, so the sample targets the chapters whose underlying sources are thinnest or
whose claims are most measurement-dependent, rather than sampling uniformly across 14,702 lines:

| Sampled | Lines | Why chosen |
|---|---|---|
| Ch.19 USB (`part-4-special-modes/chapter-19-usb.md`) | 410 | The mode our own source comparison rates **"severely lacking"**; `KNOWLEDGE-GAPS.md` G-005 is still **OPEN** against it |
| Ch.16 ADC (`part-3-input-modes/chapter-16-adc.md`) | 700 | The most measurement-dependent chapter in the guide — resolution, ENOB, accuracy |
| App. G FPGA differences | 19 | Whole-file; states hardware differences that cannot be verified on the ASIC |

Read in full or in claim-dense regions; no keyword pass was used to select claims.

---

## Result — NOT nil, and the pattern is coherent

**Two findings, both in Ch.19.** Both routed to `P2KB-CORRECTION-FINDINGS.md` as **F-274** and
**F-275**. Neither ships in the current wave: IOSP left it when F-261 reversed into F-269, so both
wait for IOSP's next release rather than being force-fitted into this one.

**Ch.16 and App. G came back clean, and emphatically so.** Ch.16 is the strongest counter-evidence
in the sample: it repeatedly refuses to overstate, in exactly the register the hypothesis predicted
would have been flattened —

- *"the bit figures above are **nominal resolution** … **not ENOB**"*
- *"treat them as optimistic upper bounds, not attainable resolution"*
- *"this is a **mechanism**, not a guaranteed specification"*
- *"any specific ENOB figure is a bench result for a *particular* rig, never a datasheet value"*

Ch.19 likewise carries two `::: caution` blocks that calibrate explicitly, one of them naming its
own limit: *"this is a community-observed behaviour; the exact mechanism is not described in the
current silicon documentation, so tune the per-clock delay against the actual clock rather than
treating any single value as a published figure."* An author working under a suppressing rule does
not write that sentence.

**So the shape of the result is not "the blacklist flattened the manual."** It is narrower and more
useful: **the guide is well calibrated where its evidence is rich and characterized, and goes quiet
about its own uncertainty exactly where the evidence is thinnest.** Ch.16's uncertainty is
*explicit* because it was measured; Ch.19's is *absent* because it was never established. The
defect is a silence, not a stripped word — which is why «#214»'s diff-based method could not have
found it, and why hedge-counting would have scored Ch.19 as the *better* chapter.

### F-274 — Ch.19 §19.4 teaches an FS-USB configuration at the exact clock its own source flags

The chapter's only worked baud-rate example computes full-speed (12 Mbps) USB at **80 MHz**
(`chapter-19-usb.md:122-128`). `KNOWLEDGE-GAPS.md` **G-005 is OPEN** and reads: *"Scope of
smart-pin USB support; documented sysclk floor (**FS-USB > 80 MHz**, LS-USB less)."*

The chapter states **no sysclk dependency for USB anywhere** — not in §19.4, not in §19.9
Limitations, not in the Quick Reference. A reader following the worked example lands exactly on the
boundary the open gap is about, with nothing to tell them a boundary exists.

**The correction is not to assert the floor.** Its only source is a reviewer comment on the Titus
document — an upstream lead, not a citation, and not something to carry into reader-facing prose as
fact. The honest repair is to (a) rework the example at a clock unambiguously clear of the question
(the chapter's own Spin2 example already runs at 200 MHz), and (b) state that USB signaling needs
sysclk headroom with the exact floor unsettled — the same shape §19.4's existing transmit-pacing
caution already uses successfully.

### F-275 — Ch.19 §19.5 says the P2 provides USB bus power; §19.8 says otherwise

`:210` — *"As a USB host, the P2: **Provides bus power (5V)**"*. The P2's I/O is 3.3 V and it
sources no 5 V rail; §19.8 `:329` correctly lists *"5V power supply for VBUS"* as an external
component the host design must provide. This is a plain factual error with an internal
contradiction two sections later — not a calibration defect, and it was surfaced by the same
read-the-claims pass rather than by any hedging detector.

---

## What this says about method, for the next probe

1. **Risk-weighted sampling found it; uniform sampling probably would not have.** Both findings sit
   in the one chapter our own gap register already flagged. Reading `KNOWLEDGE-GAPS.md` *first* and
   sampling where it is OPEN is the cheapest version of this probe.
2. **Hedge counting is worse than useless here — it inverts.** Ch.16, the chapter that hedges most,
   is the chapter that is right. Ch.19, the chapter that hedges least, is the one with the gap. Any
   future instrument built on density would have scored these backwards.
3. **The detectable signature is a missing *dependency*, not a missing *word*.** Both findings are
   cases where the manual does not mention that an answer depends on something (sysclk headroom; who
   supplies VBUS). That is the thing to look for next time.
4. **A confident chapter over a thin source is the risk profile.** Where the source is rich, authors
   calibrated well without being told to. Where the source is thin, the confident house voice filled
   the space. That is worth a targeted pass over every chapter whose mode carries an OPEN G-entry.

**Not claimed:** that this generalizes beyond the sample. Three artifacts of a 27-file guide were
read. The result is bounded to them, and the correlation figures from «#214» remain
uninterpreted — they motivated the look and did not survive as evidence.
