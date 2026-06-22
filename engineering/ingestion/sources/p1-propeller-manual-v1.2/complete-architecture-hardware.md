# P1 Propeller (P8X32A) — Architecture & Hardware Facts (Pass 1 curated)

> Faithful extraction from **P1 Propeller Manual v1.2, Chapter 1** (pp. 13–34). Page citations are
> printed = PDF pages. No inference — every fact traces to the cited page. Trust tier 🏆 (Parallax primary).
> This is the **seeding source** for `deliverables/ai/P1/architecture/` and `…/hardware/` (YAML head builds those).

## Identity & packages (p13–14)
- 8 processors ("cogs"), simultaneous independent/cooperative tasks; flat memory map; **no interrupts** (assign cogs to tasks instead); PASM has per-instruction conditional execution + optional result write (deterministic timing). (p13)
- Packages: **P8X32A-D40** 40-pin DIP · **P8X32A-Q44** 44-pin LQFP · **P8X32A-M44** 44-pin QFN. (p14)

## Specifications (Table 1-2, p16)
| Spec | Value |
|------|-------|
| Model | P8X32A |
| Power | 3.3 V DC (max total current draw ≤ 300 mA) |
| External clock | DC–80 MHz (4–8 MHz with Clock PLL) |
| System clock | DC–80 MHz |
| Internal RC oscillator | ~12 MHz or ~20 kHz (range 8–20 MHz / 13–33 kHz resp.) |
| Main RAM/ROM | 64 KB total = 32 KB RAM + 32 KB ROM |
| Cog RAM | 512 × 32 bits each |
| Addressing | Main RAM: long/word/byte; Cog RAM: long only |
| I/O pins | 32 CMOS, VDD/2 input threshold |
| Source/sink per I/O | 40 mA |
| Current draw | 500 µA per MIPS (MIPS = MHz/4 × active cogs) |

## Pins (Table 1-1, p15)
- **P0–P31**: 32 GP I/O (Port A), 40 mA source/sink @3.3 V, logic threshold ≈½ VDD (1.65 V). P28–P31 special at power-up/reset, GP afterward: **P28** I²C SCL (EEPROM), **P29** I²C SDA (EEPROM), **P30** serial Tx to host, **P31** serial Rx from host.
- **VDD** 3.3 V (2.7–3.3 V) · **VSS** ground · **BOEn** brown-out enable (active low) · **RESn** reset (active low; restart 50 ms after low→high) · **XI** crystal in · **XO** crystal out (no external R/C needed).
- External EEPROM = 32 KB 24LC256. (p15)

## Boot / run / shutdown (p18–19)
- **Boot** (power-up +100 ms, RESn low→high, or soft reset): start clock slow (~20 kHz), 50 ms reset delay, switch to fast (~12 MHz), load **Boot Loader** into Cog 0. Boot Loader: (a) detect host on P30/P31 → converse, optionally download to RAM and EEPROM; (b) else look for 24LC256 EEPROM on P28/P29 → load 32 KB image to RAM; (c) else stop, terminate Cog 0, shutdown, pins → inputs. If (a)/(b) loaded and no suspend → Cog 0 reloaded with **Spin Interpreter**, user code runs.
- **Run-time**: app = compiled Spin (+ optional PASM) in RAM/EEPROM; Spin interpreted by a cog running the Spin Interpreter, PASM run directly; every app has ≥ a little Spin. App controls clock speed, pins, config, cog count — all variable at run time. (p18)
- **Shutdown**: clock stopped, all cogs halt, pins → input (hi-Z). Triggered by: (1) VDD < brown-out threshold (~2.7 V) when brown-out enabled; (2) RESn low; (3) app REBOOT (p187). Ends when V rises above threshold and RESn high. (p19)

## Cogs (p22–23)
- 8 cogs (0–7), identical. Each = Processor, 2 KB RAM = **512 × 32 (longs)**, two Counter modules with PLLs, Video Generator, I/O Output Register, I/O Direction Register, + special registers (Table 1-3).
- All driven from System Clock → same time reference, execute simultaneously. Shared access to I/O pins, Main RAM, System Counter. Start/stop at run time; coordination via Main RAM; **no compiler/OS task-splitting** — designer controls all → deterministic timing/power/response. (p22)
- Cog RAM: 512 regs × 32 bit; locations $000–$1EF general purpose (496×32), $1F0–$1FF (16) special purpose. On boot, $000–$1EF (0–495) loaded sequentially from Main RAM/ROM; $1F0–$1FF (496–511) cleared to 0; execution begins at Cog RAM location 0. (p23)

### Cog special-purpose registers (Table 1-3, p23)
| Addr | Name | Type | Purpose |
|------|------|------|---------|
| $1F0 | PAR | RO¹ | Boot Parameter |
| $1F1 | CNT | RO¹ | System Counter |
| $1F2 | INA | RO¹ | Input states P31–P0 |
| $1F3 | INB³ | RO¹ | Input states P63–P32 (reserved future) |
| $1F4 | OUTA | R/W | Output states P31–P0 |
| $1F5 | OUTB³ | R/W | Output states P63–P32 (reserved) |
| $1F6 | DIRA | R/W | Direction P31–P0 |
| $1F7 | DIRB³ | R/W | Direction P63–P32 (reserved) |
| $1F8 | CTRA | R/W | Counter A control |
| $1F9 | CTRB | R/W | Counter B control |
| $1FA | FRQA | R/W | Counter A frequency |
| $1FB | FRQB | R/W | Counter B frequency |
| $1FC | PHSA | R/W² | Counter A phase |
| $1FD | PHSB | R/W² | Counter B phase |
| $1FE | VCFG | R/W | Video configuration |
| $1FF | VSCL | R/W | Video scale |

¹ In PASM, source-register only (`mov dest, source`). ² In PASM, source-readable only; no read-modify-write as destination. ³ Reserved for future use (P1 has no Port B). Access via physical address (PASM), predefined name (Spin/PASM), or `SPR[0..15]` array (Spin). (p23)

## Hub (p24)
- Maintains integrity of mutually-exclusive resources via **round-robin** access Cog 0→7→0. Hub + bus run at **½ System Clock** → a cog gets access **once every 16 System Clock cycles**.
- **Hub instructions** require **8 cycles** to execute but must first sync to the hub window: up to **15 cycles** (16−1) to sync + 8 to execute ⇒ **8 to 23 cycles** total (Fig 1-3 best case = 8; Fig 1-4 worst = 23). Interleave non-hub instructions (most PASM = 4 cycles, so 2 fit between hub windows). (p24–25)
- Hub instructions: CLKSET, COGID, COGINIT, COGSTOP, HUBOP, LOCKCLR, LOCKNEW, LOCKRET, LOCKSET, RDBYTE, RDLONG, RDWORD, WRBYTE, WRLONG, WRWORD. (p24)

## I/O pins — wired-OR collective (p26)
- Each cog has 32-bit Direction Register + 32-bit Output Register. Final pin state = **wired-OR of the whole cog collective**:
  - Pin Directions = OR of all cogs' Direction Registers.
  - Pin Outputs = OR of all cogs' output states; a cog's output state = (its I/O-module bits — Counters, Video Gen, Output Register — OR'd) AND its Direction Register.
- Rules: (A) input only if no active cog sets it output; (B) outputs low only if all active cogs driving it set low; (C) outputs high if any active cog drives it high. Shut-down cog's Dir/Output cleared → no influence. Input Register is a pseudo-register: reads actual pin states regardless of direction. (p26, Table 1-4 p26)

## System Counter (p27)
- Global, **read-only, 32-bit**, increments every System Clock cycle. Read via CNT; used with WAITCNT for delays. Common resource (all cogs read simultaneously). Not cleared at startup (used for differential timing). (p27)

## Clock / CLK register (p28–29)
- CLK register configures RC Oscillator, Clock PLL, Crystal Oscillator, Clock Selector. Set at compile time by `_CLKMODE` (p68); writable at run time via Spin `CLKSET` (p71) or PASM `CLKSET` (p271). Writing CLK → global **~75 µs** delay during source transition. System Clock from one of: Internal RC, Clock PLL, or Crystal Oscillator. Hub/Bus divide System Clock by 2. (p22, p28)
- **CLK register bits (Table 1-5)**: 7=RESET, 6=PLLENA, 5=OSCENA, 4=OSCM1, 3=OSCM0, 2:0=CLKSEL2:0.
  - RESET=1 → reboot (REBOOT writes it). (T1-6)
  - PLLENA=1 → enable PLL (×16 of XIN internally; PLL internal must stay 64–128 MHz ⇒ XIN 4–8 MHz; allow 100 µs to stabilize; OSCENA must be 1). (T1-7)
  - OSCENA=1 → enable Crystal Oscillator; OSCMx selects mode; allow crystal 10 ms to stabilize. (T1-8)
  - **OSCMx (Table 1-9)**: 00 XINPUT (∞ R, 6 pF, DC–80 MHz input) · 01 XTAL1 (2000 Ω, 36 pF, 4–16 MHz) · 10 XTAL2 (1000 Ω, 26 pF, 8–32 MHz) · 11 XTAL3 (500 Ω, 16 pF, 20–60 MHz).
  - **CLKSELx (Table 1-10)**: 000 RCFAST ~12 MHz internal · 001 RCSLOW ~20 kHz internal · 010 XINPUT (XIN; OSCENA=1) · 011 PLL1X (XIN×1) · 100 PLL2X (×2) · 101 PLL4X (×4) · 110 PLL8X (×8) · 111 PLL16X (×16) — all PLLnX require OSCENA=1 and PLLENA=1.
- Clock Mode value mirrored to BYTE[4] in Main RAM, master frequency to LONG[0] (so objects read current timing); CLKSET updates these automatically. (p28)

## Locks (p30)
- **8 lock bits** (semaphores) for exclusive access to user-defined resources. Live inside the Hub (outside Main/Cog RAM), globally accessible via hub instructions LOCKNEW/LOCKRET/LOCKSET/LOCKCLR. Only one cog executes them at a time; LOCKSET/LOCKCLR are atomic read+write. (p30)

## Main Memory map (p30–34, Fig 1-5)
- 64 KB (16 K longs), Hub-arbitrated mutually-exclusive. **RAM $0000–$7FFF** (32 KB): $0000–$000F init data, code/data from $0010, then variables/stack to $7FFF. LONG[$0]=initial master clock freq (Hz); BYTE[$4]=initial CLK value (names CLKFREQ/CLKMODE).
- **ROM $8000–$FFFF** (32 KB): **Character Set $8000–$BFFF** (256 chars 16w×32h; even/odd pairs merged into 32 longs; first pair $8000–$807F … last $BF80–$BFFF; even char = bits 0,2,…30, odd = 1,3,…31) · **Log/Anti-Log table** · **Sine table** (2,049 unsigned 16-bit samples 0°–90° inclusive, 0.0439° resolution; other quadrants by transformation) · **Boot Loader + Spin Interpreter** (last section). (p32–34)
- Four-color run-time character pairs (3-D beveled box edges) occupy pairs 0-1, 8-9, 10-11, 12-13 as 16×16 cells (codes 9/10/13 = Tab/LF/CR). Parallax True Type font mirrors the embedded Propeller Font. (p33)

---
*Ch2 (Spin) and Ch3 (PASM1) per-symbol reference content is captured in the layout text + code corpus +
structure map; structured per-command extraction is the YAML-head build step. See the extraction audit.*
