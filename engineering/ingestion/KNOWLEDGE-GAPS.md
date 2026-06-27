# Knowledge Gaps & Questions-for-Experts — Moving Ledger

> Backing doc #3 of the ingestion **quad** (README dashboard + `AUTHORITATIVE-SOURCES` +
> `DOCUMENT-LINEAGE` + this). Added per the breadth study (`INGESTION-PERSPECTIVES-STUDY.md`, perspectives
> **#8 gap-evolution ledger** + **#9 questions-for-experts**) — the single biggest gap the triad was missing.
> Unlike the other backing docs (static trust / lineage), this is a **moving worklist**: holes open as new
> sources arrive and close as later sources / the designer fill them. _2026-06-12._

## Why this is its own doc
The dashboard answers "how complete is each source." This answers the orthogonal question: **"what does the KB
still not know, and who can answer it?"** It's the boundary of what's verifiable from sources at all. The
dashboard rolls it up as a Tier-1 line (open-questions count + how many are routed to an expert).

---

## Part A — Gap-evolution ledger  ‹perspective #8›

Each row is a knowledge hole. Status **moves**: `OPEN` → `ANSWERED` (cite the source/edition that filled it) →
or `STILL-UNKNOWN` (no source covers it; escalate to Part B). Record the **edition** that closed it so a
later supersession can re-open it if it overturns the answer.

| # | Domain | The gap (question / missing fact) | Status | Filled by (source @ edition) | Opened | Closed |
|---|--------|-----------------------------------|--------|------------------------------|--------|--------|
| G-001 | Smart Pins / WRPIN | WRPIN **%AAAA/%BBBB input-selector** relative-pin sub-field is undocumented in our YAML. Add with **Silicon-Doc** values: bit3=invert; `x000`=this pin, `x001..x011`=+1..+3, `x100`=this pin's OUT, `x101`=−3, `x110`=−2, `x111`=−1. *(Titus rev5 had x101/x111 swapped — use Silicon-Doc, not Titus.)* | OPEN | _value known (silicon-doc); needs YAML add by yaml head_ | smart-pins-titus rev5 (#21) | |
| G-002 | Smart Pins / DAC dither | Dithered-DAC update cadence: sysclk or sysclk/256? Real effective resolution behind the "16-bit" claim (reviewer says ~10–12b realistic). | OPEN | _verify vs silicon-doc DAC section_ | smart-pins-titus rev5 (#0,#25,#26) | |
| G-003 | Smart Pins / counting modes | "time" vs "states" vs "periods" terminology (%10011–%10111); reciprocal/"whole-periods" behavior — X+ is a *minimum*, window snaps to next whole Fin cycle. | OPEN | _clarify vs silicon-doc_ | smart-pins-titus rev5 (#2,#14) | |
| G-004 | Smart Pins / %01010 SMPS | PWM switch-mode-power-supply mode has **no code example** anywhere; Y-register update timing unstated. | OPEN | | smart-pins-titus rev5 (#20,#22) | |
| G-005 | Smart Pins / %11011 USB | Scope of smart-pin USB support; documented sysclk floor (FS-USB > 80 MHz, LS-USB less). | OPEN | | smart-pins-titus rev5 (#24) | |
| G-006 | Smart Pins / NCO | Is `Y=0` valid for NCO (%00110/00111) — continuous output or none? NCO quantization jitter (fractional-add → rare long periods). | OPEN | | smart-pins-titus rev5 (#8,#17) | |
| G-007 | Smart Pins / ADC | %11000/11001 ADC modes: relationship to STREAMERS; "digital filters in digital mode"; external SDM-ADC use (TI AMC1035/1303). | OPEN | | smart-pins-titus rev5 (#7,#12,#23) | |
| G-008 | Smart Pins / WRPIN | Per-pin **Pin-Electrical** choices + full WRPIN mode-register bit-field map belong in the docs (reviewer cites evanh's bit-layout doc). | OPEN | | smart-pins-titus rev5 (#19) | |
| G-009 | Hardware / 64004-ES | HyperRAM/HyperFlash datasheet **part numbers + URLs are OCR-transcribed** (corrupt PDF text layer forced OCR) → transcription risk: HyperRAM `IS66WVH16M8BLL-100B1LI` / `issi.com/WW/pdf/66-67WVH16M8ALL-BLL.pdf`; HyperFlash `IS26KL256S-DABL100` / `issi.com/WW/pdf/26KS-KL128S-256S-512S.pdf`. Confirm exact strings vs ISSI datasheets / the 64004-ES product page before they reach published YAML. | OPEN | _verify vs ISSI datasheets / Parallax 64004-ES product page_ | hyperRam-n-hyperFlash ingestion (2026-06-22) | |
| G-010 | Hardware / WX Wi-Fi #32420 | The guide names a "Command serial communication mode" and "default serial settings" but never enumerates the **UART baud/format** or the **command set/protocol**. Firmware is "Remora" (Parallax build of open-source esp-link by Thorsten von Eicken). | OPEN | _verify vs esp-link project docs / Parallax WX firmware repo_ | parallax-wx-wifi re-extraction (2026-06-27) | |
| G-011 | Hardware / WX wireless-programming → P2 | #32420 DIP pins DTR (IO12 "toggles MCU reset") + PS (IO4) describe a **P1-era Activity-Board WX** wireless-programming flow (2016 doc); how/whether it maps to **P2** wireless programming/debug is unspecified. Same RES/PGM/CTS/DI/DO signals appear on the #64007 P2-WX-Adapter. | OPEN | _verify vs P2 board guides (Edge/eval WX) + hardware_ | parallax-wx-wifi + p2-wx-adapter re-extraction (2026-06-27) | |
| G-012 | Hardware / add-on `+N` offset | Add-on guides use **relative `+N` accessory-header offsets**; the **absolute P2 IO** each `+N` maps to is board/header-dependent and not given in the add-on guide (surfaced on #64009 microSD; systemic across the 12-pin add-on family). | OPEN | _resolve vs P2 Edge/eval-board accessory-header base-pin map_ | p2-microSD-addon ingestion (2026-06-27) | |
| G-013 | Hardware / RTC #64013 | Board guide defers RTC programming to the NXP **PCF8523** datasheet: the **I2C slave address** and the **register map** (time/date, alarm, timer, offset) are not in the guide. Cite the datasheet — do NOT infer the address. | OPEN | _resolve vs NXP PCF8523 datasheet_ | P2-RTC-Add-on ingestion (2026-06-27) | |
| G-014 | Hardware / HD-Audio #64014 (AK5704) | The #64014 ADC board's on-board **AK5704 I2C device address** (set by the CAD strap pin) is not stated — needed to write a P2 I2C codec driver. The guide also lists only **4 of 16** DAC drive-impedance steps (full table absent). | OPEN | _resolve vs AK5704 datasheet §9.16 + board schematic_ | P2-HD-Audio-Add-on ingestion (2026-06-27) | |
| G-015 | Hardware / add-on example code | Every add-on guide in this wave (microSD/RTC/HD-Audio/motor-driver/WX) **defers example & driver code to the product-page download** — no in-repo driver/init code for these boards (AK5704 register-init, PCF8523 I2C, SD-SPI boot, motor PWM). Candidate future ingestion of the product-page example archives. | OPEN | _candidate future ingestion: per-board product-page example ZIPs_ | addon-wave-2026-06 (2026-06-27) | |

> **Format heritage (from the study):** three prior representations worth carrying — resolution-status tags +
> per-question source-check list (`questions-remaining.md`), strikethrough before/after (`gaps-consolidated.md`),
> and dated "what changed since" batches (`chip-clarifications-update`). This table unifies them.

## Part B — Questions for experts (the answerable-only-by-designer residue)  ‹perspective #9›

The subset of Part A that **no source can close** — only Chip Gracey (or another named authority) can. Carries a
**who-to-ask** routing so the question can actually be sent.

| # | Question | Why no source settles it | Who to ask | State (open / asked / answered) | Links |
|---|----------|--------------------------|------------|---------------------------------|-------|
| Q-001 | Is the sync-serial (%11100/%11101) description's "starts with a logic-0 start bit" correct, or does it wrongly borrow async framing? | Reviewer (#5) flagged it wrong, cited a now-unextractable Parallax-forum thread; no in-corpus source settles sync-serial framing detail. | Chip Gracey / Parallax forum (orig. thread) | open | smart-pins-titus #5 |
| Q-002 | Is the DAC dither frame fixed at 8 bits, or could a (e.g.) 4-bit extension give 12-bit DAC at a faster period? | Design-intent question about silicon capability not stated in any doc. | Chip Gracey | open | smart-pins-titus #3 |
| Q-003 | What is the realistic scope of smart-pin USB (%11011) support, and the SW/opcode help + sysclk needed for FS/LS-USB? | Implementation knowledge lives with the community implementer, not in docs. | garryj (USB impl.) / Chip Gracey | open | smart-pins-titus #24 |
| Q-004 | Is the #32420 WX Wi-Fi Module officially supported for **Propeller 2** wireless programming/debug, or only the (P1-era) Propeller Activity Board WX the 2016 guide references? | The guide predates P2 boards; no in-corpus source settles P2 support. | Parallax | open | parallax-wx-wifi (2026-06-27) |
| Q-005 | On the #64013 RTC board, +0 is shared between **I2C SCL** and **INT/CLKOUT**: is there a recommended sequence to switch +0 between the two roles without glitching an in-progress PCF8523 I2C transaction? | Board-design/timing intent not stated in the guide. | Chip Gracey / Parallax board author | open | P2-RTC-Add-on (2026-06-27) |
| Q-006 | Confirm the on-board **AK5704 CAD-strap → 7-bit I2C address** on the #64014 ADC board, and whether **SDTO2/TDMIN** on the header is wired data-out (SDTO2E=1) by default. | Set by board CAD strapping; only the schematic / Parallax can confirm. | Parallax (schematic) | open | P2-HD-Audio-Add-on (2026-06-27) |

---

## Inputs that feed this ledger
- **`ingest-source` pass 6** (cross-source conflict audit) — unresolved conflicts and uncovered facts land here.
- **Reviewer notes harvested from source DOCX** — technical questions in embedded editorial notes / Google-Docs
  comments are routed here as credible feedback (e.g. Smart Pins (Titus) rev 5's 27 comments). See the project
  rule on ingesting reviewer notes.
- **The corrections register** — a finding that turns out to be unanswerable-from-sources is mirrored here as a
  Part-B question rather than left CONFIRMED-but-unfixable.

## Maintenance
Updated by `ingest-source` on every pass-6 and on each new edition (a supersession may ANSWER or RE-OPEN rows).
The dashboard's Tier-1 Q&A line reads its counts from here. Stale 2025 gap instances (`gaps-consolidated`,
`questions-remaining`, `AREAS-NOW-UNDERSTOOD`, …) fold into this ledger, then archive.
