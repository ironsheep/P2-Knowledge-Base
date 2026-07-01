# P2AN004 — Example Library

The complete, runnable source for the worked recipes in **Application Note
P2AN004, "Read Real-World Sensors by Frequency, Period, and RC Timing on a P2
Pin."** Each file is extracted verbatim from the opus-master so the download and
the document never drift.

| File | Recipe | Demonstrates |
|---|---|---|
| `rc-decay-reader.spin2` | R1 (RC-decay reader) | charge-float-time RC sensor read, polled, via %10001 P_HIGH_TICKS |
| `light-to-freq-reader.spin2` | R2 (light-to-frequency) | TSL235R Hz reading (reciprocal counter) + Hz->irradiance |
| `quadrature-knob.spin2` | R3 (encoder instrument) | production encoder knob (clamp + preset + det4x + button) with a Tier-0 self-test |

**Verification.** Every file compiles clean under `pnut-ts -d` (v1.55, `_clkfreq =
200_000_000`). Build with DEBUG enabled (`-d`) so the `debug()` output stream
appears.

- **R3 is Tier-0 self-stimulable** — jumper pin 40->32 and 41->33 and the program
  drives its own A/B quadrature pattern, so it reads a *known-answer* detent count
  with no encoder attached. This is the recipe you can fully confirm on an Edge
  board with two jumper wires.
- **R1 and R2 are hardware-pending for *accuracy*** — R1 needs a real R-C sensor
  network on the pin; R2 needs a TSL235R (and a reference light source to certify
  the irradiance curve). The code paths compile and run; the absolute readings are
  confirmed against hardware in a later pass (see the note's Verify sections).

**Packaging.** At release these files are published as `P2AN004-src-<YYMMDD>.zip`
beside the PDF in `deliverables/documents/DOCs/`, with a download link in the
publication roster (per the app-note production convention — see
`../../APP-NOTE-CREATION-GUIDE.md` §6).
