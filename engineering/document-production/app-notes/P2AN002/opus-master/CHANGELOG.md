# P2AN002 — CORDIC for Real Work — Changelog

## v1.0.2 (2026-08-08)

A licensing change. No technical content changed — not a page of it.

- **License restored to CC BY-SA 4.0.** This note is again licensed Creative Commons Attribution–ShareAlike 4.0 International, the license the community-review editions carried from 2025-12-09 through 2026-05-22. You may share and adapt it, including commercially, with attribution and under the same terms.
- **Why it changed back.** The CC BY-NC-ND terms it carried from 2026-06 went well beyond their intent. NonCommercial does not restrict resale — it restricts *all* commercial use, including a paid course referencing a chapter or a distributor bundling the PDF with a board. NoDerivatives blocked translations, excerpting, and community forks. The concern behind that change was only that someone might resell this as their own product.
- **Trademark, not copyright, addresses that concern.** The Trademarks note now states that the license grants permissions under copyright only: a reuser may copy, adapt, translate, and sell the text, but may not present the result as the official edition or imply endorsement.
- **Nothing was retroactively taken.** Creative Commons licenses are irrevocable, so every copy distributed under BY-SA stays BY-SA permanently.

## v1.0.1 (2026-07-11)

A derivation and attribution refinement. No recipes added.

- **Step-size derivation** — the circle-layout recipe explains why the direct `$1_0000_0000 / STEPS` form won't compile (a 33-bit dividend literal) and how the halved `$8000_0000 / (STEPS / 2)` form reaches the same quotient within 32 bits.
- **OBEX attributions** — the Resources list matches the catalog: #2812 Binary Floating-Point (ersmith) and #5361 FFT/IFFT (James Smith).

## v1.0.0 (2026-07-03)

Initial release for community review. An application note for putting the Propeller 2's shared
hardware CORDIC solver to real work — the engine that turns a rotation, a sine, a square root, or
a full 64-bit multiply into a single queued operation with a fixed 55-clock latency. Six runnable
recipes the reader selects among — distance and heading, point rotation, circle layout, sine/cosine
waves, 64-bit-safe fixed-point scaling, and pipelining to retire one result every eight clocks —
plus a field-oriented motor-control reference ceiling. Every recipe verifies against a closed-form
answer you can derive by hand, with no bench instruments. All worked programs compile clean
under `pnut_ts`. Ships with a downloadable example library of every recipe.
