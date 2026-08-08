# P2AN004 — Frequency / Rotation / RC-Timing Measurement — Changelog

## v1.0.2 (2026-08-08)

A licensing change. No technical content changed — not a page of it.

- **License restored to CC BY-SA 4.0.** This note is again licensed Creative Commons Attribution–ShareAlike 4.0 International, the license the community-review editions carried from 2025-12-09 through 2026-05-22. You may share and adapt it, including commercially, with attribution and under the same terms.
- **Why it changed back.** The CC BY-NC-ND terms it carried from 2026-06 went well beyond their intent. NonCommercial does not restrict resale — it restricts *all* commercial use, including a paid course referencing a chapter or a distributor bundling the PDF with a board. NoDerivatives blocked translations, excerpting, and community forks. The concern behind that change was only that someone might resell this as their own product.
- **Trademark, not copyright, addresses that concern.** The Trademarks note now states that the license grants permissions under copyright only: a reuser may copy, adapt, translate, and sell the text, but may not present the result as the official edition or imply endorsement.
- **Nothing was retroactively taken.** Creative Commons licenses are irrevocable, so every copy distributed under BY-SA stays BY-SA permanently.

## v1.0.1 (2026-07-11)

A specification-accuracy and titling refinement. No instruments added.

- **Clock headroom** — the programs run at 200 MHz, the top of the P2 PLL VCO's designed 100–200 MHz range.
- **Encoder input filtering** — `P_FILT1_AB` routes the A/B inputs through the global FILT1 digital filter (reset default ≈600 ns low-pass).
- **Title** — the note is *Frequency / Rotation / RC-Timing Measurement*, naming its three instruments (light-to-frequency, quadrature-rotation, RC-decay); the cover reads "Frequency, Rotation, and RC Timing."

## v1.0.0 (2026-07-03)

Initial release for community review. A techniques-catalog application note for reading real-world
sensors by timing, counting, and decoding directly on a single P2 pin — no external counter or ADC.
One shared idea (let a smart pin time or count the signal so the cog never watches an edge) applied
through three runnable instruments the reader selects among by transducer: an RC-decay reader that
times a capacitor's discharge for any resistive or capacitive sensor, a light-to-frequency reader
that turns a TSL235R's output frequency into an irradiance with a reciprocal frequency counter, and
a drop-in quadrature-knob instrument with detent normalization, preset, range clamp, and a debounced
button. Every worked program compiles clean under `pnut_ts`; the encoder recipe self-verifies on a
bare board with two jumper wires and a known-answer detent count, while the analog recipes' absolute
calibration defers to a hardware pass and carries no invented readings. Circuit schematics (RC-decay
network, TSL235R hookup) and a quadrature timing diagram are rendered inline. Ships with a
downloadable example library of every worked program.
