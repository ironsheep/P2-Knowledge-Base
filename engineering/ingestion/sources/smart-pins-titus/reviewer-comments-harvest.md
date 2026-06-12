# Smart Pins (Titus) rev 5 — Reviewer-Comment Harvest

**Source:** `Smart Pins rev 5.docx` (2026-03-31) · **Harvested:** 2026-06-12 (ingest-source pass 6, §5.3)
**Mechanism:** `word/comments.xml` (27 embedded Google-Docs / Word review comments), each
anchored to its commented text range in `word/document.xml`.

> **Why harvest these:** embedded editorial notes are **credible feedback**, not noise — they are
> the document's own peer review. Per the project rule on ingesting reviewer notes, each is
> classified and routed. **Weight under the source's tier:** Titus is 🟡 *cross-check* — a
> reviewer's *assertion* is a lead to verify against an authority, not a fact to adopt.

## Authors (27 comments)
Jim Granville (20) · Deleted user (1) · Jonathan Shook (1) · Anonymous (1) ·
Miguel António Nunes (1) · Frank Freedman (1) · Carroll Moore (1) · Walter Mosscrop (1).
Jim Granville is the dominant technical reviewer; dates span 2020-08 → 2026-03.

## Classification & routing

Legend — **Route:** `KG`=KNOWLEDGE-GAPS Part A (gap) · `KG-B`=Part B (expert-only) ·
`ERRATA`=confirmed Titus-source defect (not our YAML) · `EDIT`=editorial/wording · `NOISE`=banter.
**No comment routed to the corrections register** — see "Conflict adjudication" below.

### High-value: factual assertions verified against an authority

| # | Author | Anchor (mode/topic) | The note | Adjudication | Route |
|---|--------|---------------------|----------|--------------|-------|
| **21** | Walter Mosscrop | WRPIN %AAAA/%BBBB input-selector table | "This value is incorrect. It should be x111, and the value of x111 below should be x101. True for both AAAA and BBBB selectors." | **CONFIRMED — Titus is wrong.** Silicon Doc (authority for this bit-field): `x101=Relative −3`, `x110=−2`, `x111=Relative −1`. Titus rev5 labels `x101=−1` / `x111=−3` — **x101 and x111 are swapped** (x110=−2 agrees). Reviewer is correct. | ERRATA + KG (our WRPIN YAML lacks this sub-field entirely) |
| **18** | Carroll Moore | %10000 Time-A-input example (`.test_loop_x`) | "Should `#A_in` be followed by `wc` in `.test_loop_x`? If not, why?" | **VALID catch.** The example polls carry via `if_nc` after `rqpin pin_data, #A_in` with **no `wc`** — carry isn't updated, so the branch tests a stale flag. The sibling loop `.test_loop_y` *does* use `wc`. Inconsistent; reviewer is right. | ERRATA (Titus example bug) |
| **5** | Deleted user | %11100/%11101 sync-serial framing | "This is wrong" (sync-serial "starts with a logic-0 start bit") — links a Parallax-forum thread. | **Plausible.** Synchronous serial has no async-style start bit; the description likely over-borrows async framing. Forum link no longer extractable. Needs forum/expert confirmation before acting. | KG-B (verify vs forum/Chip) |
| **25** | Jim Granville | %00010 DAC dither / IN flag | "Is that true? Usually DACs update at the DAC output rate, not sysclk? A DAC with 8-bit dither → output frame rate sysclk/256?" | Open technical question about DAC-dither update cadence vs the prose's sysclk claim. | KG (verify vs Silicon Doc DAC-dither) |

### Content gaps & technical questions (→ KNOWLEDGE-GAPS Part A)

| # | Author | Topic | Note (essence) | Route |
|---|--------|-------|----------------|-------|
| 0 | Granville | %00010 pseudo-random dither | "A formula is needed — exactly how does the random use the extended data." | KG |
| 3 | Granville | DAC dither frame | 8-bit dither frame fixed? A 4-bit extension → 12b DAC at faster period? | KG-B (Chip) |
| 26 | Granville | %00010 "16-bit" DAC claim | "16-bit claim is nominal" — real precision set by 8b-DAC LSB; ~10–12 bits realistic. | KG (caveat the claim) |
| 8 | Granville | NCO (%00110/00111) Y=0 | "DOCs should state if Y=0 is valid. Continuous output, or no output?" | KG |
| 17 | Granville | NCO jitter | Example adds 238609294 but ideal is 238609294.222 → rare 19µs periods every ~1073 s. | KG (note quantization jitter) |
| 9 | Granville | %00100 pulse/cycle naming | Other vendors call this "Pin Toggle" / "Burst Toggle" — rename? | EDIT |
| 16 | Granville | %01000 triangle PWM | Triangle PWM gives dead-band control; expand waveform with a P21 $0088 pin example. | KG (example request) |
| 22 | Granville | %01010 PWM SMPS | "DOCs should state when Y updates (I think when IN ↗)"; multi-phase PWM dead-band; add a 3-pin example. | KG |
| 20 | Granville | %01010 PWM SMPS | "Chip needs to give a working schematic and code example here." | KG (confirmed: %01010 has **no** code example in rev5) |
| 2 | Granville | %10101–10111 reciprocal-counter | Should say "for whole periods"; X+ is a *minimum*, window snaps to next whole Fin cycle; freq = whole-periods / time. | KG (wording + technique) |
| 14 | Granville | %10011–10111 "time/states/periods" | Chip's terminology is uncommon & confusing; "states"=gated counter (enables when Fin=H), "periods"=whole Fin cycles. | KG (clarify terminology) |
| 1 | Granville | counting modes | Dual-capture (time + states) on one pin removes remote-MCU sysclk error; resolves to remote jitter. | KG (technique) |
| 13 | Granville | %10011 A→B event timing | Chip's code uses 3 pins; concurrent start via single `dirh #msr_pins` enables all on same sysclk. | KG (technique) |
| 7 | Granville | %11000/11001 ADC streamers | Read the STREAMERS datasheet section; Chip's debug display/capture could help docs. | KG |
| 12 | Granville | %11001 external-clock ADC | External 16-bit SDM ADCs (TI AMC1035 non-isolated, AMC1303 isolated) common for motor control. | KG (reference) |
| 23 | Granville | %11000/11001 ADC | "Digital pin modes are digital, and the ADC filters here are digital mode." | KG (clarify) |
| 24 | Granville | %11011 USB | Smart-pin USB support is minimal, needs extensive SW/opcode help; garryj has it working; FS-USB needs sysclk > 80 MHz, LS-USB less. | KG-B (garryj / Chip) |
| 19 | Granville | WRPIN / pin-electrical | Section should include per-pin Pin-Electrical choices + the WRPIN mode-register bit-field map (cites evanh's doc). | KG (content gap: WRPIN bit-field doc) |

### Editorial / low-priority

| # | Author | Note | Route |
|---|--------|------|-------|
| 4 | Granville | Opcode 9 bits vs legal pin 6 bits — say "lower 6 bits". | EDIT (pin-address width clarification) |
| 6 | Jonathan Shook | Float instructions — give an intuitive example of why you'd do this. | EDIT (example request) |
| 10 | Anonymous | Explain D/# and S/# = Source/Destination, `#`=immediate. | EDIT |
| 15 | Frank Freedman | Typo: "Drop space ⇒ Depending". | EDIT (typo) |
| 11 | Miguel A. Nunes | "Maybe Chip is thinking about a 128-bit P3 with 16 COGs :)" | NOISE (banter) |

## Conflict adjudication — corrections-register decision
**Zero entries routed to `P2KB-CORRECTION-FINDINGS.md` this run.** The one *confirmed* factual
error (#21) and the example bug (#18) are defects in the **Titus source**, which is being corrected
through its own editorial review — they are not errors in our published `deliverables/ai/P2/` YAML.
I verified the most concrete claim (#21) against the WRPIN YAML entry: **our YAML does not carry the
%AAAA/%BBBB input-selector relative-pin sub-field at all**, so there is nothing to correct — only a
*completeness gap* to fill (with the **correct Silicon-Doc** values, never Titus's swapped ones).
That gap is logged in KNOWLEDGE-GAPS, the proper home. This is the expected outcome for a cross-check
source whose disagreements are with primary prose, not with our derived data.

## Additional source defects found during code validation (pass 2)
Not reviewer comments, but same class (Titus authorship errata, → ERRATA):
- **`COM` used as a section header** (should be `CON`) in 4 mode examples (%01000, %01001, ×2 %01011).
- **BBBB selector typo:** `x011 = …+3 = P39` (should be **P40**; the AAAA row above has it right).
- Lowercase `dat`/`con` section keywords throughout (~20 examples) — compiles (case-insensitive), style only.
