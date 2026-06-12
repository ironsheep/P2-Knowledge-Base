# Smart Pins (Titus) rev 5 — Image Catalog

**Source:** `Smart Pins rev 5.docx` (2026-03-31) · **Extracted:** 2026-06-12
**Method:** DOCX-media (lossless `word/media/*`) + `image-tools-mcp` quality gate + OCR
**Count:** 21 figures (18 .jpg + 3 .png)

## Quality gate (all 21 PASS)
Bulk check: every figure is a discrete white-background diagram/schematic
(mean brightness 238–250), dimensions 524×250 → 2500×1556, RGB. **Zero** black
captures, zero full-page mis-captures, zero tiny artifacts — the DOCX-media path
eliminated the v3.0 black-image/false-success failure class at the source.

## Figures (document order, mapped to mode/section)

| File | WxH | Mode / Section | Type | OCR'd content (key labels) |
|------|-----|----------------|------|----------------------------|
| image12.jpg | 1758×379 | Input-Output-Bit Timing | I/O timing diagram | System Clock; DIRA/OUTA P0; instruction `DRVH #0`; "Internal register transfers" |
| image10.jpg | 1421×268 | Input-Output-Bit Timing | I/O timing diagram | (timing waveform — enhancement debt) |
| image14.jpg | 1244×290 | Input-Output-Bit Timing | I/O timing diagram | (timing waveform — enhancement debt) |
| image2.jpg | 1758×379 | %00011 DAC + PWM dither | timing diagram | (waveform — debt) |
| image3.jpg | 2183×765 | %00100 Pulse/cycle output | timing diagram | (waveform — debt) |
| image15.jpg | 1823×797 | %00100 Pulse/cycle output | timing diagram | (waveform — debt) |
| image16.jpg | 2500×903 | %00110 NCO | NCO timing + register values | IN Flag; "Z Overflow"; Base Period; **X[31:16] = $0000 $5010 $A020 $F030 $4040 $9050 $E060**; System Clock |
| image13.jpg | 2500×815 | %00110 NCO | timing diagram | (waveform — debt) |
| image1.png | 663×423 | %00111 NCO Duty Cycle | timing diagram | (waveform — debt) |
| image4.jpg | 2500×1556 | %01000 Triangle PWM | PWM timing + parameters | P20 Output; **X[31:16]=$200**, **Y[15:0]=$0082**; PWM Period 41.0 µs; Frame Period 20.5 µs; **Base period = 40 ns (25 MHz); $200 base periods = 20.5 µs** |
| image6.jpg | 2500×1529 | %01001 PWM sawtooth | PWM timing | (waveform — debt) |
| image18.jpg | 2500×868 | %01011 A/B quadrature encoder | encoder timing | Encoder P33/P32; CW; **4 edges = 4 counts** |
| image17.jpg | 1576×570 | %10000 Time A-input states | timing diagram | (waveform — debt) |
| image8.jpg | 1711×559 | %10010 Time A-input highs | timing diagram | (waveform — debt) |
| image19.jpg | 1644×597 | %10010 Time A-input highs | timing diagram | (waveform — debt) |
| image11.jpg | 1549×633 | %10010 Detect missing A-input | timing diagram | (waveform — debt) |
| image5.jpg | 1161×687 | %10011 Measure time X events | timing diagram | (waveform — debt) |
| image7.jpg | 1677×666 | %11100 Synchronous serial TX (SST) | timing diagram | (waveform — debt) |
| image20.jpg | 1571×656 | %11100 Synchronous serial TX (SST) | timing diagram | (waveform — debt) |
| image21.png | 524×250 | %11110 Async serial TX (AST) | timing diagram | (waveform — debt) |
| image9.png | 555×253 | %11110 Async serial TX (AST) | timing diagram | (waveform — debt) |

## OCR coverage & enhancement debt
- **Detailed OCR done (4):** image12, image16, image18, image4 — one per major diagram
  family (I/O timing, NCO register-value, encoder, PWM-parameter). These carry the
  **checkable register/timing values** used in pass-6 cross-validation.
- **OCR enhancement debt (17):** remaining timing waveforms. OCR is noisy on dense
  waveform glyphs (raster `0`→`@`, tick marks → `|`); low value-per-effort for pure
  waveforms with few register labels. Queued as image-enhancement debt; not blocking
  (Titus is a 🟡 cross-check source — its figures corroborate, they are not the primary
  authority for any published fact).

## Pass-6 cross-validation hooks (figure content → evidence)
- **image16 (NCO):** X[31:16] step sequence $0000→$E060 (increment $5010) — corroborate
  against the NCO base-frequency math in the prose and Silicon Doc NCO mode.
- **image4 (Triangle PWM):** Base period 40 ns ⇔ 25 MHz; $200 (512) base periods = 20.5 µs
  frame; Y[15:0]=$0082 — arithmetic self-consistent (512 × 40 ns = 20.48 µs ✓).
- **image18 (encoder):** "4 edges = 4 counts" (1× decode shown) — note Titus prose elsewhere
  divides count by 4 (`sar …,#2`); reconcile the encoder edge-count convention in pass 6.
