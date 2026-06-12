# Smart Pins (Titus) rev 5 — Cross-Source Q&A Audit (pass 6)

**2026-06-12** · companion to `reviewer-comments-harvest.md` (the conflict/reviewer leg).
Three legs per `ingest-source` §5: answer prior, raise new, score trust.

## Leg 1 — Prior open questions answered
The `KNOWLEDGE-GAPS.md` Part-A ledger was **empty** (seeded today, Titus is its first populating run),
so there were no prior cross-source questions for Titus to *close*. Against the broader corpus, Titus
**corroborates** (does not originate) the Smart Pins mode taxonomy already held from `src:silicon-doc`
and `src:smart-pins`: the 32-mode list, mode bit-numbers, and X/Y/Z register roles all agree.

## Leg 2 — New questions raised (→ KNOWLEDGE-GAPS Part A / B)
Titus's prose + its 27 reviewer comments surface a substantial first batch of gaps. The headline items
(full list with anchors in `reviewer-comments-harvest.md`):

- **WRPIN %AAAA/%BBBB input-selector relative-pin sub-field** is undocumented in our YAML (and is the
  field Titus got wrong). Add it with the **Silicon-Doc** values (`x101=−3, x110=−2, x111=−1`,
  `x001..x011=+1..+3`, `x100=this pin's OUT`, bit3=invert). *High-value findability gap.*
- **DAC-dither cadence** (#25/#0/#26): does the dithered DAC update at sysclk or sysclk/256? what's the
  real effective resolution behind the "16-bit" claim? → verify vs Silicon Doc DAC section.
- **Counting-mode terminology** (#14/#2): "time" vs "states" vs "periods" and the reciprocal
  ("for whole periods / X+ is a minimum") behavior of %10101–%10111 — clarify against Silicon Doc.
- **%01010 PWM-SMPS** (#20/#22): no code example anywhere; Y-update timing unstated.
- **%11011 USB** (#24): scope of smart-pin USB support, sysclk floor (FS-USB > 80 MHz).
- **NCO Y=0 validity** (#8) and **NCO quantization jitter** (#17).

Expert-only residue (Part B): #5 (sync-serial framing — forum/Chip), #3 (dither-frame extensibility — Chip),
#24 (USB — garryj/Chip).

## Leg 6 — Trust scoring
| Source | Fact-type touched | Outcome |
|--------|-------------------|---------|
| `src:silicon-doc` 🏆 | WRPIN A/B input selector encoding | **authority** — resolved #21 (Titus wrong) |
| `src:smart-pins-titus` 🟡 | mode taxonomy, register roles | corroborates silicon-doc (HIGH agreement) |
| `src:smart-pins-titus` 🟡 | WRPIN selector bit-table | **single-source error**, peer-review-caught → MEDIUM trust |
| `pnut-ts v1.55.0` 🏆 | code-example syntax/semantics | validated 28/30 examples |

**Net:** Titus rev5 is a strong *corroborating + color* source (techniques, app notes, external-part
references) at 🟡. It is **not** an encoding/bit-field authority — one such table here was demonstrably
wrong. Conflict precedence stands: `pnut_ts` → Silicon Doc → … → Titus.

## Corroboration matrix touchpoints (figure content → evidence)
- NCO X[31:16] step values from `image16` consistent with NCO base-frequency prose.
- Triangle-PWM `image4`: 512 base periods × 40 ns = 20.48 µs frame — arithmetically self-consistent.
