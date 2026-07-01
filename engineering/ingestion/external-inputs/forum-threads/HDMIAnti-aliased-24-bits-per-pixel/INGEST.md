# Forum Thread Ingestion — Anti-aliased 24-bits-per-pixel HDMI

- **Source URL:** https://forums.parallax.com/discussion/175725/anti-aliased-24-bits-per-pixel-hdmi
- **Thread ID:** 175725
- **Pages:** 3
- **Post count:** 85 (p1: 31, p2: 26, p3: 28)
- **OP author + date:** cgracey — 2024-02-14
- **cgracey post count:** 13
- **Fetched:** 2026-07-01
- **Topic class:** Graphics / video output — HDMI(DVI) streamer output, PSRAM framebuffer, anti-aliased pixel-blend drawing, TTF/Bezier font rendering. Application/demo thread with authoritative timing + pixel-op detail from the chip designer.

## Thread purpose

cgracey demonstrates a 960x540 24-bits-per-pixel ("qHD") anti-aliased graphics
system on the P2-EC32MB Edge module, driving HDMI through the Parallax DIGITAL
VIDEO OUT board (8 pins → HDMI). He ports his PC DEBUG-display anti-aliased
line-draw routine to the P2. The thread then explores minimum DVI/HDMI blanking
timings across many monitors, a Z-buffered/anti-aliased polygon renderer, and
community work on TTF/Bezier vector-font rendering and a 16bpp variant. Primary
doc value: HDMI/DVI blanking-timing limits and the P2 pixel-blend instruction
usage (SETPIV/BLNPIX, RGBSQZ/RGBEXP) for anti-aliasing.

## Participant trust classification

| User | Trust | Basis |
|------|-------|-------|
| cgracey | 🏆 | Chip Gracey — P2 chip designer; authoritative ground truth |
| rogloh | 🟢 | Roger Loh — author of the P2 PSRAM + video drivers used here; deep, correct hardware/bandwidth analysis, CORDIC/PASM detail |
| evanh | 🟢 | Long-standing P2 expert; systematic DVI/HDMI timing testing across many displays, understands TMDS/FRL/VRR |
| Wuerfel_21 | 🟢 | "Ada" — author of MegaYume/MegaVGA drivers; expert 3D-rasterization/blending/audio-packet knowledge; cgracey defers to her (34-pixel audio-packet figure) |
| pik33 | 🟢 | Ships P2 BASIC interpreter + media player with own video driver; concrete tested timing tables |
| Rayman | 🟡 | Active P2 community dev; practical experiments, later reverse-engineers the pixel-blend PASM (correctly) |
| SaucySoliton | 🟡 | Community; MPEG/font-storage dedup idea (tangential) |
| TonyB_ | 🟡 | Community; timing question |
| VonSzarvas | 🟡 | Parallax-affiliated; light comment |
| Tubular | 🟡 | Community; laser/gcode application idea |
| refaQtor | 🟡 | Community; bench-setup comment |

## Chip Gracey findings (trusted gold)

### CG-1 · qHD 960x540 24bpp over HDMI from PSRAM
> "The PSRAM buffers 960x540 screens at 24bpp for a really nice picture over HDMI... I took the anti-aliased line-draw routine I made for the PC that the DEBUG displays use and got it running on the P2... To try this code, you'll need a P2-EC32MB module and the DIGITAL VIDEO OUT board which connects 8 pins to an HDMI connector... With the 'qHD' mode, or quarter-HD, we'll be able to show really nice anti-aliased fonts and graphics at the same time."

**Means:** A 960x540 24bpp framebuffer = ~2 MB, held in the Edge module's PSRAM (hence external RAM is required; confirmed later "that's a 2 MB screen buffer!"). The P2 streamer drives HDMI/DVI via the 8-pin DIGITAL VIDEO OUT board. The DEBUG-window anti-aliased line renderer is the same algorithm now running on-chip.
**Affects:** Streamer Programming Guide (HDMI/DVI output example, framebuffer sizing, PSRAM-sourced scanout); I/O & Smart Pins guide (DVI/HDMI 8-pin output topology).

### CG-2 · Anti-aliased line-draw sub-pixel encoding
> "The anti-aliased line draw has 8 sub-bits for each X, Y, and diameter. So, lines can be placed in X and Y at offsets of 256ths of a pixel. Line diameter is similar, but gets halved to make a radius in 256ths of a pixel. The minimum diameter is $100, or 1 whole pixel."

**Means:** Coordinates and line diameter carry an 8-bit fractional part (1/256 pixel). Diameter is a Q?.8 value; `$100` = 1.0 pixel minimum. `smoothline(x0,y0,x1,y1,diameter,RGBA)` — the community demos confirm diameter `$100`=1px, `$480`=dots, and an RGBA color long. This is the sub-pixel model behind the DEBUG-display renderer.
**Affects:** Any documentation of the DEBUG display anti-aliasing model; not a silicon fact but designer-authoritative algorithm detail.

### CG-3 · HDMI/DVI blanking can be pushed far below analog-era values
> "Yeah, I found that on my TV it could be set minimally, in order to get to 60Hz refresh. All this timing was carry-in from the analog era. It seems that most of it can be squeezed out in HDMI... I don't know what the minimum really is."

His demo used **16 horizontal blank pixels** and **8 total vertical blank lines** (see CG-4).
**Means:** Unlike VGA, DVI/HDMI (TMDS) tolerates minimal front/back porch; the traditional large blanking intervals are not electrically required — the practical floor is set by each display's tolerance, not the P2. (evanh's cross-testing: floor ranges from 16 up to 60–68 hblank depending on monitor age; older/VGA-mode displays are fussiest.)
**Affects:** Streamer Programming Guide HDMI timing section — document that blanking is display-limited, give the observed practical range rather than a single mandated porch.

### CG-4 · Vertical blanking = 1 vsync line + 7 blanks (8 total); audio needs ~34 hblank
> "Yeah, it's one vsync line and seven blanks. I need to know how tight this can be safely pushed. Ada said today that we need something like 34 total horizontal blank pixel periods to accommodate data packets for sound."

**Means:** Demo vertical blanking is 8 lines total (front porch 0, 1 sync line, 7 blank). Crucially: **HDMI audio (data-island packets) requires ~34 horizontal blank pixel periods** — so an HDMI-with-sound design cannot use the ultra-tight 16-pixel hblank; the horizontal blanking floor rises to ~34 to carry audio packets. (Figure sourced from Wuerfel_21/"Ada".)
**Affects:** Streamer Programming Guide — HDMI audio section: minimum horizontal blanking budget (~34 px) for data-island/audio packets. Distinguishes video-only vs audio-carrying HDMI timing.

### CG-5 · Z-buffer + edge-only anti-alias blending for polygons (design intent)
> "A section identical to the screen memory can be maintained in the PSRAM to act as a per-pixel Z buffer. Only nearer pixels get written to the screen memory..."
> "I meant to say that I would blend the edges, as in anti-alias them... All polygons would be considered opaque, but the edges might as well get blended to reduce jaggies."

**Means:** Planned per-pixel Z buffer co-resident in PSRAM; polygons treated opaque with edge-only alpha blend for AA. (Wuerfel_21 correctly cautions any read-underneath blend produces ordering artifacts.) Design discussion, not shipped feature.
**Affects:** None directly — future graphics-demo context only.

### CG-6 · Bitmap screen fonts via supersample-and-dither
> "render each character at high resolution in on/off pixels, and then reduce it to dithered pixels by gridding it and counting on/off pixels to get greyscale/blend pixels."

**Means:** Designer's recommended path to anti-aliased screen fonts: render glyph at high res 1bpp, box-downsample counting coverage → greyscale/alpha. Algorithm guidance.
**Affects:** None directly (technique note).

## Other credible technical contributions

- **evanh 🟢 — DVI/HDMI minimum-blanking survey.** Tested many displays: minimum hblank varies 16 (Chip's TV) → 60 → 68 (old Dell U2412M DVI); fully-flexible resolution acceptance is a "last ~10 years" capability that arrived with HDMI firmware; older/VGA-mode displays only accept standard modes. Rule: horizontal must be a multiple of 8. Below-250 MHz TMDS link speeds worked on newer displays despite the nominal minimum. TMDS vs HDMI 2.1 FRL; VRR likely needs FRL (packetized), so classic blanking/sync concepts don't apply there. **Cross-check tier — corroborates CG-3, extends with per-display floors.**
- **evanh 🟢 — worked timing examples** (sysclk/dotclock/hfp/hsync/hbp/vfp/vsync/vbp) for 1280x640, 640x320, etc., all with hfp/hbp≈4, vsync=2. Useful concrete DVI timing sets.
- **pik33 🟢 — tested timing table** 1024x600@50Hz: 76 px hblank, 12 lines vblank, stable across several Philips/AOC monitors + Waveshare 1024x600 HDMI touch panel; notes CVT-RBv2 standard is 80 px hblank / 18 vblank lines, too wide to fit under the 340 MHz EC32 stability ceiling; prefers trimming hblank but monitors resist. Gives a full `timings` LONG structure incl. HUBSET PLL value `%1_100111__10_1010_1000__1111_1011` for 340.5 MHz.
- **rogloh 🟢 — driver/bandwidth authority.** 960x540 32bpp@60Hz scanout ≈ needs the whole PSRAM bus; text-over-background compositing ≈379 MB/s (infeasible >30Hz) unless composited on-the-fly during scanout like sprites (~10 P2 clocks/pixel at 320 MHz). Pixel-doubling from PSRAM can't always meet scan timing; line-doubling can. CORDIC-based Bezier (up to 1024 segments) fits the 8-bit sub-pixel coordinate scale. TTF contour format is compact (per-point flag byte, on/off-curve bit, repeat flag, 8/16-bit signed deltas, omitted zero deltas).
- **rogloh 🟢 / Rayman 🟡 — pixel-blend PASM (P2 silicon instructions).** The anti-alias inner loop is:
  ```
  setpiv  plot_color        'set blend factor from low 8 bits (alpha) of plot_color
  blnpix  pa,plot_color      'blend background pixel pa with plot_color using that factor
  ```
  Rayman deduces (rogloh confirms): SETPIV takes the alpha from the **low 8 bits** of the operand as the blend factor; BLNPIX then blends the two RGB colors, result in `pa`. These pixel-mixer ops work naturally only in 32bpp/LUMA modes; for 16bpp you must RGBEXP→blend→RGBSQZ (adds ~8 instructions/pixel). rogloh notes BLNPIX/SETPIV use one M factor for all bytes (no per-byte alpha without a prior SETQ trick); MUXQ is the alternative for 8bpp sprite work. **Cross-check tier — but this is directly verifiable against the SETPIV/BLNPIX/RGBSQZ/RGBEXP instruction YAML.**
- **Rayman 🟡 — 16bpp port gotcha:** anti-alias pixel routine must clear C/Z afterward: `modcz _clr,_clr wcz`. Anti-aliased circle code ported from Versa-Design/Antialiased_Circle. VGA + Edge/Platform variants; ~5–10 fps with PSRAM double-buffering.

## Doc-impact targets (reconciliation queue)

| # | Finding | Target doc/section | Suggested action | Trust |
|---|---------|--------------------|------------------|-------|
| 1 | 960x540 24bpp (~2MB) framebuffer in PSRAM, streamer→HDMI via 8-pin DIGITAL VIDEO OUT board | Streamer Programming Guide — HDMI/DVI output example | Add qHD PSRAM-sourced HDMI example / sizing note | 🏆 CG-1 |
| 2 | DVI/HDMI blanking is display-limited, not analog-era-mandated; practical hblank floor 16→~68 px, multiple-of-8 rule | Streamer Programming Guide — HDMI timing / blanking | Document that porches can be minimized; give observed range + per-display caveat | 🏆 CG-3 / 🟢 evanh |
| 3 | HDMI audio (data-island packets) needs ~34 horizontal blank pixel periods; video-only can go to ~16 | Streamer Programming Guide — HDMI audio section | State minimum hblank budget for audio-carrying HDMI vs video-only | 🏆 CG-4 |
| 4 | Vertical blanking floor observed = 8 lines (fp=0, 1 sync, 7 blank) | Streamer Programming Guide — vertical timing | Note minimal-vblank feasibility + display variance | 🏆 CG-4 / 🟢 evanh/pik33 |
| 5 | SETPIV (alpha from low 8 bits) + BLNPIX blend usage for per-pixel alpha; 32bpp/LUMA only; RGBEXP/RGBSQZ for 16bpp | I/O & Smart Pins guide? No — PASM2 instruction YAML: setpiv/blnpix/rgbsqz/rgbexp | Verify/enrich instruction docs with this canonical anti-alias usage pattern + mode restriction | 🟢/🟡 (verify vs YAML) |
| 6 | Concrete tested DVI timing sets (1024x600@50 76x12; assorted evanh examples; HUBSET PLL constants) | Streamer Programming Guide — timing examples appendix | Optionally cite as community-tested example modes (cross-check) | 🟢 pik33/evanh |
| 7 | 8-bit sub-pixel (1/256 px) coordinate + diameter model of DEBUG anti-aliased line draw | DEBUG display docs (line/plot rendering model) | Note sub-pixel precision model if documented | 🏆 CG-2 |

## Open questions / unresolved

- **Exact safe minimum blanking** the P2 HDMI output can drive is never pinned down — cgracey explicitly asks for exact numbers ("I need to know how tight this can be safely pushed... It would be good to know exact numbers"). Answer is display-dependent, not a P2 limit; no authoritative floor established in-thread.
- **Audio packet hblank figure (~34 px)** is attributed to Wuerfel_21/"Ada," relayed by cgracey — credible but not independently spec-cited here; verify against HDMI data-island spec before publishing as a hard number.
- **SETPIV/BLNPIX exact semantics** (which operand supplies alpha, effect on C/Z, per-byte M behavior) are community-reverse-engineered (Rayman/rogloh) — must be reconciled against the authoritative PASM2 instruction YAML before use; Rayman's 16bpp `modcz _clr,_clr wcz` requirement suggests flag side-effects worth documenting.
- No cgracey source-code listings were posted inline in this thread (code is in linked Google Drive / attached .spin2 files); the SETPIV/BLNPIX snippet comes from community readers of the attachment, not a cgracey post.
