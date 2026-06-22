# P2 Eval Add-on Boards (#64006) × Smart Pin Modes — Initial Mapping (DRAFT)

> **Status: DRAFT cross-reference for possible future document use** (e.g. a "learn Smart Pins by board"
> tutorial / exercise set). **Board functions are sourced** from the per-board docs (`boards/addon-*.md`,
> from the Product Guide). **The Smart-Pin-mode bindings are a proposed teaching mapping** — which modes a
> board is naturally suited to *exercise* — not a manufacturer claim. **Validate each binding against
> `deliverables/ai/P2/architecture/smart-pins/smart-pin-*.yaml` before using as a document source.**
> Mode names/numbers below are taken from those KB YAML filenames.

## Matrix
| Board | Sourced function | Primary Smart Pin modes to exercise | Secondary / optional | Confidence |
|-------|------------------|-------------------------------------|----------------------|------------|
| **A — Control** | 4 LEDs (PWM brightness) + 4 push-buttons | **%01001 PWM sawtooth**, **%01000 PWM triangle** (LED dimming) | %00000 normal (button read); %10101/%10110 count-in-X-clocks (debounce); %10000 time-A-states (press duration) | High (PWM stated in guide) |
| **B — Serial Host** | Twin USB-A host + activity LEDs | **%11011 USB host/device** (host role) | %11110/%11111 async serial TX/RX (UART use); %01001 PWM (LEDs) | Med — USB-vs-bitbang depends on driver |
| **C — LED Matrix** | 8×7 Charlieplexed LEDs (tri-state direct drive) | *(mostly direct tri-state I/O — %00000 normal)* | %01001/%01000 PWM (brightness); %00100 pulse/cycle output (refresh timing) | Med — board is direct-drive; SP optional |
| **D — Digital Video Out** | HDMI-type TMDS (clock + 3 data pairs) | *(exercises the **Streamer + DVI/HDMI**, not Smart Pins)* | — | High that it's **not** a Smart-Pin board |
| **E — Mini Prototyping** | 8×12 plated thru-hole grid | *(user-wired — any mode, depends on the circuit built)* | all modes | n/a — open-ended |
| **F — Serial Device** | Twin microUSB (P2 as USB device) + LEDs | **%11011 USB host/device** (device role) | %11110/%11111 async serial; %01001 PWM (LEDs) | Med — same USB-vs-bitbang caveat |
| **G — Goertzel** | Touch / non-contact position-sense pads (Rev B) | **%11000 ADC internal clock** (pad sensing) + SW Goertzel | %10101 count-ticks / %10110 count-highs-in-X-clocks (RC/charge-time sensing); %00000 (switch pads 4–6) | Low/Med — sensing method needs confirming vs smart-pins KB |
| **H — A/V Breakout** | Audio out (amp L/R, headphone), mic in, VGA/composite/component video | **%00011 DAC 16-bit PWM dither** / **%00010 DAC pseudo-random dither** (audio out); **%11000 ADC internal clock** (mic in) | video paths exercise the **Streamer + DAC**, not Smart Pins | Med — audio High; video is streamer |

## Caveats for later doc use
- **Video boards (D, and H's VGA/composite) primarily exercise the Streamer/DAC, not Smart Pins** — they
  belong in a streamer tutorial, not a smart-pins one. Flagged so a "Smart Pins by board" doc doesn't miscast them.
- **USB boards (B, F)** depend on whether the driver uses smart-pin USB mode %11011 or bit-banged serial —
  confirm against the actual OBEX/driver before asserting.
- **Goertzel (G)** sensing method (ADC vs charge-time measurement) is the least certain row — verify against
  the smart-pins KB + any Goertzel object before doc use.
- This maps boards→modes; the inverse (which board best demonstrates a given mode) can be derived from it when
  scoping a tutorial.
