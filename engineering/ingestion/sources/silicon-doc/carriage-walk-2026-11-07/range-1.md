# Silicon Doc carriage walk — range 1 (SD:1-504)

Source: `engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt`, lines 1-504, read whole.
KB: `deliverables/ai/P2/` (paths below are relative to it). Plan: `engineering/planning/P2KB-CONTRACT-GAPS-SPRINT-PLAN.md`.

## Sections

| SD line | Heading | Disposition |
|---|---|---|
| 1-11 | Title block (v35, Rev B/C, part numbers) | Metadata; not a contract. |
| 12-119 | Design Status (history table) | Mostly history/mechanism. The Rev B feature list (SD:55-70) is contract: it is carried, or IN-PLAN (§3, §4). Rev C ADC-float change is carried. |
| 121-133 | KNOWN SILICON BUGS | Both bugs carried as errata E1, E2 (MATCH). |
| 135-222 | OVERVIEW (cog, hub, smart pin, clock feature lists) | Mostly carried. Gaps: hub bandwidth stated wrongly in `hub.yaml`; smart-pin serial rate limits and DAC impedances not carried; little-endian only on a Spin2 method page. |
| 227-243 | PIN DESCRIPTIONS | Hardware facts; partly carried. TEST pin and "no external R/C on XI/XO" not carried; RESn hold behaviour partial. P58-P63 deferred to the BOOT PROCESS range. |
| 245-281 | MEMORIES (memory table) | Carried (MATCH). |
| 282-331 | COGS (pipeline; encoding key table) | Pipeline facts MATCH. Encoding key: SD's R-bit row is inverted against CSV/compiler (source erratum; KB right). The cccc/zzzz modifier rule and MODCZ symbols not carried; the encoding glossary the pages point to does not exist. |
| 333-341 | INSTRUCTION MODES | MATCH. |
| 343-344 | REGISTER EXECUTION | MATCH. |
| 345-346 | LOOKUP EXECUTION | MATCH. |
| 347-360 | HUB EXECUTION | MATCH except the forbidden list: KB drops the "when the streamer mode engages the FIFO" qualifier from XINIT and XZERO (MISMATCH, 7 sites). SD:350 is a reviewer comment, not a fact. |
| 362-433 | STARTING AND STOPPING COGS | COGINIT/COGSTOP/COGID carried. `spin2/methods/coginit.yaml:134` says "All cog registers cleared except PTRA" (MISMATCH). `pasm2/coginit.yaml` omits PTRA=0 with no SETQ, the pair-returns-even-ID rule, and the $000..$1F7 load range (PARTIAL; carried elsewhere). `cog.yaml` D layout IN-PLAN §1. SD:370-373, 401-402 are reviewer comments. |
| 436-468 | COG RAM (GENERAL / DUAL / SPECIAL-PURPOSE REGISTERS) | Carried correctly in `complete-system-registers-index.yaml`. `pasm2/concepts/special_registers.yaml` contradicts it three ways (MISMATCH). |
| 471-480 | LOOKUP RAM | MATCH. |
| 481-486 | LOAD/STORE ACCESS | MATCH. SD:484-485 is a reviewer comment. |
| 487-488 | STREAMER ACCESS | "(to be completed.)" in source; nothing to carry. |
| 489-490 | BYTECODE EXECUTION LOOKUP TABLE | "(to be completed.)" in source; nothing to carry. |
| 491-504 | RAM SHARING BETWEEN PAIRED COGS | MATCH. |

## Ledger

| SD lines | Fact (one line) | C/M | YAML home (file:line) or NOT-CARRIED | Disposition | Note (quotes, searches) |
|---|---|---|---|---|---|
| 19-41 | Rev A defects (IQ, +1/+3 counting, ALTx sign-extension, DIR/OUT glitch); fixed in Rev B | M | NOT-CARRIED | NOT-CARRIED | Historical, fixed in the silicon the KB covers. Correct to leave out. |
| 53-54, 81-84 | Clock-gating, PLL filter, jitter <2ns, 390 MHz at room temp | M | NOT-CARRIED | NOT-CARRIED | Characterisation, not a spec. Correct to leave out. |
| 55 | System counter is 64 bits; GETCT WC returns upper 32 | C | `language/pasm2/concepts/special_registers.yaml:61` | MATCH | "64-bit free-running (Rev B/C silicon); GETCT returns lower 32 bits by default, upper 32 bits with WC" |
| 56-59 | Streamer SINC/Goertzel/HDMI modes; smart-pin SINC2/SINC3; four 8-bit SCOPE ADC channels per cog | C | `architecture/smart-pins/smart-pin-11010-adc-scope-trigger.yaml:20`; `architecture/smart_pins.yaml:52` | PARTIAL | Summary only. Detail belongs to the streamer and smart-pin ranges. The "four channels per cog" count was not found (grep `four.{0,25}(DAC\|ADC) (output \|input )?channels`). |
| 60 | BITx work on a span: +S[9:5] bits; a prior SETQ overrides S[9:5] | C | `language/pasm2/bitrnd.yaml:15` | IN-PLAN §4 | Plan §4 "the span uses (SD:60-62)". |
| 61 | DIRx/OUTx/FLTx/DRVx span +D[10:6] pins; SETQ overrides | C | — | IN-PLAN §4 | Same. |
| 62 | WRPIN/WXPIN/WYPIN/AKPIN span +S[10:6] pins; SETQ overrides | C | — | IN-PLAN §4 | Same. |
| 63 | BIT_DAC has two 4-bit levels (low and high) | C | `architecture/smart_pins.yaml:365` | MATCH | "BIT_DAC outputs {2{M[7:4]}} for high or {2{M[3:0]}} for low" |
| 64 | PTRx index -16..+16 with update, -32..+31 without | C | — | IN-PLAN §3 | `ptr_expression_encoding`. |
| 65 | SETQ(2) block plus PTRx update moves the pointer by the block | C | — | IN-PLAN §3 | `ptrx_with_block_transfers`. |
| 66 | RDLUT/WRLUT accept PTRx expressions | C | `architecture/lookup_ram.yaml:46-50` | MATCH | "RDLUT/WRLUT accept a PTRx pointer expression in place of S". The unit is IN-PLAN §9 arm N. |
| 67 | LUT sharing is glitch-free | M | NOT-CARRIED | NOT-CARRIED | Mechanism. |
| 68 | POP returns Z=1 if result=0 | C | `language/pasm2/pop.yaml:7,16` | MATCH | "z: Result == 0"; "Set if result equals zero" |
| 69-70 | XORO32 improved; main PRNG is Xoroshiro128** | C | `language/pasm2/concepts/special_registers.yaml:54` | MATCH | "xoroshiro128** PRNG, seeded at boot, iterating every clock" |
| 97-105 | VIO latch-up seen from ~4.3 V | M (electrical) | `architecture/io_pin_timing.yaml:236-238` | MATCH | "latch-up onset was reported as early as ~4.3 V on VIO" |
| 115 | Rev C: %100010_OHHHLLL floats the ADC input (bias-point measurement); Rev B used the adjacent pin | C | `architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml:148` | MATCH | "P_ADC_FLOAT - ADC input floated (Rev C silicon); used to determine the ADC's floating bias point" |
| 123-127 | Erratum: ALTx/AUGS/AUGD between SETQ and a block PTRx op cancels the block-size PTRx delta | C | `architecture/silicon_errata.yaml:33-45` (E1) | MATCH | "PTRx steps by the plain expression's own step ... Write the SETQ/SETQ2 directly before the block transfer" |
| 129-133 | Erratum: an immediate-#S ALTx between AUGS and its target also takes the AUGS | C | `architecture/silicon_errata.yaml:47-57` (E2) | MATCH | "Give any ALTx placed between an AUGS and its target a register S, not an immediate #S." |
| 137 | Architecture family: 1/2/4/8/16 cogs, up to 1 MB hub, up to 64 pins | M | `architecture/hub.yaml:16,77-78` | PARTIAL | "1MB maximum"; the slice text says "(depending on number of cogs)". The family is never stated as a list. Low value for P2X8C4M64P code. |
| 139, 146-147 | P2X8C4M64P = 8 cogs, 512 KB, 64 smart pins, TQFP-100; part-number decode | C | `hardware/edge-standard-module.yaml:47`; `hardware/p2-package-mechanical.yaml:28` | MATCH | "P2X8C4M64P (8 cogs, 512 KB shared hub RAM, 64 smart pins)"; "TQFP-100". The decode (4M = 4 Mb, ES) is informational. |
| 152 | Each cog has four fast DAC output channels and four fast ADC input channels | C | `architecture/streamer/overview.yaml:41` | PARTIAL | "Four 8-bit channels (X0, X1, X2, X3)" for the DACs. The ADC channel count is not found (see SD:59 row). |
| 153-154 | 512 longs of dual-port register RAM; 512 longs of dual-port lookup RAM | C | `architecture/cog.yaml:23-34`; `architecture/lookup_ram.yaml:33` | MATCH | "512 longs (2KB)"; "512 × 32 bits, dual-port" |
| 155 | Code runs from register RAM, lookup RAM and hub RAM | C | `language/pasm2/concepts/execution_modes.yaml:11-91` | MATCH | |
| 157 | 2-clock execution for all math/logic, including 16x16 multiply | C | `architecture/cog.yaml:16`; `language/pasm2/mul.yaml:27` | MATCH | "cycles: 2" |
| 158 | 6-clock custom-bytecode executor | C | `architecture/xbyte_engine.yaml:12` | MATCH | "6 clocks per bytecode + routine execution time" |
| 161 | Colorspace converter: 3x3 matrix with 8-bit signed/unsigned coefficients | C | `language/pasm2/setcy.yaml:12` | PARTIAL | The converter exists in the KB. The 3x3 / 8-bit detail is left to the streamer/colorspace range (grep `3 ?x ?3` found nothing in `architecture/`). |
| 164-167 | 16 event trackers; 3 prioritized interrupts; hidden debug interrupt; 8-level hardware stack; C and Z | C | `architecture/event_system.yaml:24`; `architecture/cog.yaml:100,133-138` | MATCH | "event_sources: 16"; "8 levels; a 9th push discards the oldest entry" |
| 171 | Hub: up to 1 MB in a 20-bit space; P2X8C4M64P has 512 KB | C | `architecture/hub.yaml:15-19` | MATCH | "$00000-$7FFFF (512KB) or $00000-$FFFFF (1MB)" |
| 172 | Hub gives 32 bits per clock sequential read/write to all cogs at once | C | `architecture/hub.yaml:121,189` | MATCH | "1 long per clock after initial sync"; "burst: 4 bytes per clock during block transfer" |
| 172 | (same fact) against hub.yaml's bandwidth block | C | `architecture/hub.yaml:186-188` | MISMATCH | "theoretical: Clock_freq / 2 bytes/second per COG"; sustained "Clock_freq / 8". Unsourced, and contradicts SD:172 and the same file's :189. |
| 173 | Hub is byte/word/long accessible, little-endian | C | `language/spin2/methods/endianl.yaml:66` | PARTIAL | "P2 is little-endian" is only on a Spin2 method page. `hub.yaml`, `rdword.yaml` and `rdlong.yaml` do not say it (grep `little.endian`, `byte order`, `lowest address`). SD:2868 says it again (a later range). |
| 174 | The last 16 KB also appears at the end of the 1 MB map and can be write-protected | C | `architecture/hub.yaml:40-44` | MATCH | "read and written at both its normal range and at $FC000..$FFFFF ... write-protected" |
| 175-183 | CORDIC: 32x32 multiply, 64/32 divide with remainder, sqrt, rotate, polar/cartesian, log/exp 5.27 | C | `architecture/cordic.yaml:63-66,188-189` | MATCH | "64÷32 → 32-bit quotient, 32-bit remainder"; "32-bit unsigned -> 5.27 fixed-point logarithm" |
| 184 | A CORDIC op can start every #cogs clocks; results arrive 55 clocks later | C | `architecture/cordic.yaml:17`; `language/spin2/concepts/cordic_solver.yaml:113` | MATCH | "Every 8 clocks per COG ... 'every 1/2/4/8/16 (#cogs) clocks'" |
| 185 | 16 semaphore bits (locks) with atomic RMW | C | `architecture/hub.yaml:147,154` | MATCH | "count: 16"; "Test-and-set in single operation" |
| 186 | 64-bit free-running counter, +1 every clock, cleared on reset | C | `language/pasm2/getct.yaml:14` | MATCH | "increments every clock, cleared on reset" |
| 187 | PRNG: Xoroshiro128**, true-random seeded at start-up, updates every clock, unique data per cog and pin | C | `language/pasm2/getrnd.yaml:17` | IN-PLAN §1, §6 | GETRND claims and `prng_seeding` are in plan. "unique per cog" is carried; "per pin" is not stated. |
| 189-190 | 16 KB boot ROM is loaded into the last 16 KB of hub RAM at boot | C | `architecture/hub.yaml:23,229` | PARTIAL | "Mapped at $FC000-$FFFFF on boot"; "$FC000_$FFFFF: Boot ROM (16KB)". Reads as ROM mapped there, not ROM copied into hub RAM (which is RAM afterwards). Owned by the BOOT PROCESS range; plan §1 "Empty hub" touches $FC000. |
| 191-195 | SPI/serial loaders, Hex/Base64, Monitor via "> " + Ctrl-D, TAQOZ via "> " + ESC | C | `architecture/boot-rom/boot-rom-contents.yaml:53`; `architecture/boot-rom/p2-monitor.yaml:26,33`; `architecture/boot-rom/taqoz-forth.yaml:25`; `architecture/serial_loader.yaml:92` | MATCH | "'> ' (greater-than + space) then Ctrl+D"; "a received ESC ($1B) starts TAQOZ" |
| 199 | Pin DACs: 8-bit, 120-ohm (3 ns) and 1 k-ohm, 16-bit oversampling, noise, high/low digital modes | C | `architecture/smart_pins.yaml:53` | PARTIAL | "8-bit DAC (16-bit with dithering)". The two output impedances (120 ohm / 1 k) are NOT-CARRIED: grep `120.?(ohm\|Ω)`, `(990\|1k\|1 ?k\|123\.75).{0,10}(ohm\|Ω)`, `ohm` over `smart_pins.yaml`, `pin-drive-configuration.yaml`. Detail belongs to the smart-pin range. |
| 200 | ADC: delta-sigma, 5 ranges, 2 sources, VIO/GIO calibration | C | `architecture/smart_pins.yaml:52` | MATCH | "Delta-sigma ADC with 5 ranges, 2 sources and VIO/GIO calibration" |
| 204 | Inputs can come from relative pins -3..+3 | C | `architecture/smart_pins.yaml:50` | MATCH | "±3 pins from any pin" |
| 206 | Drive modes: logic / 1.5k / 15k / 150k / 1 mA / 100 µA / 10 µA / float | C | `architecture/pin-drive-configuration.yaml:175-180` | MATCH | table rows %001..%110 |
| 212-213 | Sync serial up to clock/2; async serial up to clock/3 | C | NOT-CARRIED | NOT-CARRIED | grep `clock ?/ ?[23]`, `sysclk ?/ ?[23]`, `max.{0,30}(baud\|bit rate)`, `fastest`, `minimum` over `architecture/smart-pins/smart-pin-111*.yaml`, `smart_pins.yaml`. The likely home is `smart-pin-11100/11101/11110/11111-*.yaml`, which give "programmable baud rate" with no ceiling. |
| 217 | RCFAST 20+ MHz, nominally 24 MHz, the clock at boot | C | `architecture/clock_system.yaml:168,200-203` | MATCH | "20+ MHz (nominally ~24 MHz) ... used on boot up." |
| 218 | Crystal oscillator with internal loading caps for 7.5 pF / 15 pF crystals | C | `architecture/clock_system.yaml:160-161` | MATCH | "15pF per pin" / "30pF per pin" (= 7.5 / 15 pF crystal load) |
| 220 | PLL: 1..64 crystal divider, 1..1024 VCO multiplier, optional (1..15)*2 post-divider | C | `architecture/clock_system.yaml:94-125` | MATCH | "1..64 division of XI"; "1..1024"; PPPP table VCO/2..VCO/30, VCO/1 |
| 221 | RCSLOW ~20 kHz, 130 µA | C | `architecture/clock_system.yaml:190-193` | MATCH | "Low-power operation (130 µA)" |
| 222 | Clock can be stopped until reset (100 µA) | C | `language/pasm2/idioms/halt-and-fault-response.yaml:10` | PARTIAL | "Stop the system clock until the next reset". The current figure is not carried. |
| 215 | Glitch-free switching between clock sources | C | `architecture/clock_system.yaml:177,209` | MATCH | deglitching text; "glitch_free: true" |
| 232 | TEST pin is tied to ground | C (board) | NOT-CARRIED | NOT-CARRIED | grep `TEST.{0,30}(ground\|GND\|tied)` found nothing. `architecture/pin-power-domains.yaml:52` only counts the pin. Board-design fact. Likely home is `hardware/p2-package-mechanical.yaml`. |
| 233-236 | VDD 1.8 V; VIO 3.3 V per pin group; GIO ground | C (board) | `hardware/p2-package-mechanical.yaml:82`; `architecture/pin-power-domains.yaml:36` | MATCH | "All VDD pins must be connected to a single 1.8 V supply. All Vxxyy pins must be connected to 3.3 V" |
| 238-239 | XI/XO: crystal or clock input; no external resistors or capacitors needed | C (board) | `architecture/clock_system.yaml` (crystal block, "loading_capacitors: Internal, programmable") | PARTIAL | "No external R/C required" is not stated. grep `no external (resistors\|R)` found nothing. |
| 240 | RESn low: all cogs disabled, pins float; restarts 3 ms after RESn rises | C | `architecture/boot-rom/_index.yaml:27` | PARTIAL | "delays for 3 ms". "All cogs disabled, I/O pins floating while low" is not found (grep `reset.{0,60}(float\|all cogs)`). |
| 243 | P58-P63 are boot sources | C | `architecture/boot-rom/_index.yaml:160-171` | MATCH | Detail belongs to the BOOT PROCESS range. |
| 247-281 | Memory table: COG/LUT 32-bit x 512 (D/S $000-$1FF; PC $000-$1FF / $200-$3FF); HUB 8-bit, D/S $00000-$FFFFF, PC $00400-$FFFFF | C | `architecture/cog.yaml:21-34,111-131`; `architecture/lookup_ram.yaml:34`; `architecture/hub.yaml:17-19` | MATCH | "$200-$3FF in the cog's address space; $000-$1FF as seen by RDLUT/WRLUT" |
| 286 | 5-stage pipeline; 2 clocks when full; a stall stalls followers; a cancelled instruction takes 2 clocks; first instruction after a branch takes at least 4 | C | `architecture/cog.yaml:13-19` | MATCH | quotes SD verbatim at :18-19. Stall propagation is not stated (mechanism-adjacent). |
| 286 | (pipeline detail) stage names and hazard claims | M | `architecture/cog.yaml:179-195` | PARTIAL | "Instruction Fetch (IF) ... Memory Access (MA) ... Write Back (WB)", "Hardware forwarding handles most cases", "Branch prediction not implemented", "cordic_wait: 0-54 clocks": unsourced. SD gives only "five-stage". For `audit-yaml-claim-sourcing.py`. |
| 294-295 | EEEE = condition field | C | `language/pasm2/concepts/conditional_execution.yaml:247` | MATCH | "_RET_ is the EEEE=%0000 condition prefix" |
| 296-311 | C/Z = write flag (WC/WZ/WCZ); I = #S literal; L = #D literal | C | per-instruction `bits:` fields only | PARTIAL | No page explains the C/Z/I/L key letters. The 140 pages that carry `# See encoding-table-reference.yaml` point to a file that does not exist (find over the repo: none). |
| 313-315 | R bit: SD says 0 = relative, 1 = absolute | C | `language/pasm2/call.yaml:63`; `language/pasm2/loc.yaml:13`; `guides/pasm2-getting-started.yaml:298` | MISMATCH (source erratum; KB right) | KB: "relative (R=1) or absolute (R=0)"; "If R = 1 then PC += A". SD Table 6 has it inverted. The KB agrees with the CSV and with pnut-ts (plan §9 prototype `FE1FFC12`, R=1, relative). Not in `engineering/ingestion/SOURCE-ERRATA.md` (grep `R bit\|relative\|Table 6`). |
| 316-317 | WW = index of PA/PB/PTRA/PTRB to write | C | `language/pasm2/calld.yaml:73` | MATCH | "WW selects PA/PB/PTRA/PTRB" |
| 322-325 | 20-bit A field; 23-bit augment field | C | `language/pasm2/augs.yaml:11,13` | MATCH | "prepends AUGS's 23 bits" |
| 326-327 | N/NN/NNN = word/byte/nibble index | C | `language/pasm2/getnib.yaml:31` (bits only) | PARTIAL | Same missing glossary as above. |
| 328-331 | cccc/zzzz: %0000 = clear, %1111 = set, others as EEEE | C | `language/pasm2/modcz.yaml:9-10`; `modc.yaml:20-22`; `modz.yaml` | PARTIAL | "the 4-bit modifier values select which combinations of current C and Z states produce 1 results". The %0000/%1111 rule, the EEEE equivalence and the modifier symbols (`_CLR`, `_SET`, `_NC_AND_Z`, ...) are not carried. grep `_CLR\|_SET\b`, `\b_(c\|z\|nc\|nz\|clr\|set)\b`, `modifier`. pnut-ts compile (scratch) of `modcz _set,_clr wcz` gives D field `0_1111_0000`; `modc _nc_and_z wc` gives cccc `%0010` = EEEE `if_nc_and_z`. |
| 334-341 | 20-bit PC; source by PC range; PC increment 1 / 1 / 4 | C | `architecture/cog.yaml:111-131` | MATCH | "pc_increment: 4" for hub |
| 344-346 | No special consideration branching to cog or LUT addresses | C | `language/pasm2/concepts/execution_modes.yaml:33,57,110-115` | MATCH | |
| 348 | Hub exec uses the FIFO to spool instructions | C | `language/pasm2/concepts/execution_modes.yaml:153-162` | MATCH | |
| 351 | Hub branch: at least 13 clocks, +1 if the target is not long-aligned | C | `architecture/cog.yaml:130`; `execution_modes.yaml:66` | MATCH | "Minimum 13 clocks (+1 if not long-aligned)" |
| 351 | Rolling from $3FF to $400 does not start hub exec; it takes a branch | C | `language/pasm2/concepts/branch_addressing.yaml:97` | MATCH | "JMP to $400 and above enters hub execution (the PC rolling from $3FF to $400 does not)" |
| 353-357 | No RDFAST/WRFAST/FBLOCK/RFx/WFx in hub exec | C | `execution_modes.yaml:80`; `cog_hub_execution.yaml:99-115` | MATCH | |
| 358 | XINIT / XZERO / XCONT are barred in hub exec only "when the streamer mode engages the FIFO" | C | `language/pasm2/concepts/execution_modes.yaml:80`; `cog_hub_execution.yaml:166,342`; `language/pasm2/hubexec.yaml:30`; `architecture/fifo.yaml:241`; `language/spin2/constructs/inline_pasm.yaml:85,114` | MISMATCH | KB: `"XINIT", "XZERO", "XCONT (when streamer engages FIFO)"` puts the qualifier on XCONT only. `cog_hub_execution.yaml:166` and `inline_pasm.yaml:114` bar all three outright. SD puts the qualifier on the whole line. The KB forbids a legal hub-exec XINIT/XZERO in non-FIFO streamer modes (DDS/LUT, pins->LUT). |
| 360 | Hub $00000-$003FF normally cannot be executed (cog/LUT take those PCs) | C | `execution_modes.yaml:62`; `cog_hub_execution.yaml:75` | MATCH | "cannot host hubexec at $00000-$003FF" |
| 364 | Any cog can start/stop any cog or itself; free-cog start without knowing IDs | C | `language/pasm2/coginit.yaml:5` | MATCH | |
| 376-377 | D=%0_x_xxxx: target loads its registers $000..$1F7 from hub at S, then runs from $000 | C | `language/pasm2/concepts/cog_hub_execution.yaml:59`; `architecture/hub.yaml:170`; `language/pasm2/cogexec.yaml:25` | MATCH | "COGINIT loads $000-$1F7 = 504 longs". `pasm2/coginit.yaml:5` says only "load code from Hub RAM to be executed within Reg/LUT RAM" (PARTIAL there: no range, and LUT is not loaded). |
| 379 | D=%1_x_xxxx: target starts at register/LUT/hub address S, with no load | C | `language/pasm2/coginit.yaml:5`; `language/spin2/methods/coginit.yaml:27` | PARTIAL | "or to be executed right from Hub RAM"; "Bit 5 set: Execute from hub RAM". Neither says S may be a register or LUT address. |
| 381 | D=%x_0_CCCC: the target cog's ID is %CCCC | C | `language/pasm2/coginit.yaml:5` | IN-PLAN §1 | `cog.yaml:201-204` wrong layout is plan §1. The pasm2 page "%E_N_xVVV" is right. |
| 383-386 | Free-cog start: D must be a register with WC; success C=0, D=ID; failure C=1, D=$F | C | `language/pasm2/coginit.yaml:5,13-16,25` | MATCH | "C is set on failure or cleared on success, and if Dest is a register, it receives the launched cog's ID (or $F on failure)" |
| 388-392 | Pair start: D gets the even/lower cog's ID | C | `language/spin2/methods/coginit.yaml:36` | PARTIAL | "returns the even/lower cog's ID" is only in the Spin2 page's `not_an_input` note. `pasm2/coginit.yaml` does not say it. |
| 395-398 | S (32-bit) is written to the target's PTRB; it is the load or start address, per D[5] | C | `language/pasm2/coginit.yaml:5` | MATCH | "the entire 32-bit Src is written to the target cog's PTRB" |
| 404 | A preceding SETQ value goes to the target's PTRA; with no SETQ, PTRA is cleared to 0 | C | `architecture/system-registers/ptra-register.yaml:25-26`; `complete-system-registers-index.yaml` (coginit_initialization) | MATCH | "Cleared to 0 if no SETQ". `pasm2/coginit.yaml:5` gives only the SETQ half (PARTIAL there). |
| 376-404 | (same facts) against the Spin2 COGINIT page notes | C | `language/spin2/methods/coginit.yaml:134-135` | MISMATCH | "All cog registers cleared except PTRA"; "Cog starts at address 0". SD: $000..$1F7 are loaded from hub (SD:376-377), PTRB gets S (SD:397-398), and hub-exec starts at S (SD:379). It also contradicts its own :140. Not in plan §1 (which lists only :45 of this file). |
| 406-418 | Worked COGINIT examples | C | `language/pasm2/coginit.yaml:49-71` | MATCH | All six SD examples present, plus named-constant forms. |
| 421 | COGSTOP: the 4 LSBs of D/# give the target cog | C | `language/pasm2/cogstop.yaml:5,18` | MATCH | "Dest[3:0] (the 4 LSBs of the D/# operand supply the target cog ID)" |
| 429 | COGID returns its ID in D[3:0], upper bits cleared | C | `language/pasm2/cogid.yaml:5` | MATCH | "returned in D[3:0] with upper bits cleared" |
| 431 | COGID WC: D not written; C = status of cog D/# (1 busy, 0 free) | C | `language/pasm2/cogid.yaml:5,16,25` | MATCH | "write: D if reg and !WC" |
| 437-441 | Cog RAM: 512x32 dual-port; $000-$1EF general purpose | C | `architecture/cog.yaml:37`; `complete-system-registers-index.yaml:31-35` | MATCH | "$000-$1EF (496 registers)" |
| 441 | (same fact) on the concept page | C | `language/pasm2/concepts/special_registers.yaml:8` | MISMATCH | "Unlike general-purpose registers (cog RAM $000-$1FF)". SD: $000-$1EF. |
| 444-453 | $1F0-$1F7 dual-purpose: IJMP3/IRET3/IJMP2/IRET2/IJMP1/IRET1/PA/PB, RAM unless the function is in use | C | `complete-system-registers-index.yaml:49-104`; `cog_hub_execution.yaml:56` | MATCH | Cell-identical, including PA/PB roles. `cog.yaml:27` "$1F0-$1F7 can be RAM or interrupt vectors" leaves out PA/PB (PARTIAL there). |
| 446-451 | (same fact) IJMPx/IRETx are cog RAM registers holding the ISR call/return addresses | C | `language/pasm2/concepts/special_registers.yaml:29-33` | MISMATCH | "name: IJMP0/IJMP1/IJMP2/IJMP3 ... access: Via SETINT1/SETINT2/SETINT3". SD: they are registers $1F0-$1F5 (code writes them with MOV, e.g. `mov ijmp1,#isr`). SETINTx picks the event, not the vector. IRETx are left out. |
| 456 | $1F8-$1FF are 8 special-purpose registers in the register address space; addressing them reaches the special register "not just the underlying RAM" | C | `complete-system-registers-index.yaml` access_patterns ("MOV $1F8, ##$3000 ' Same as MOV PTRA") | MATCH | |
| 456 | (same fact) on the concept page | C | `language/pasm2/concepts/special_registers.yaml:7-9` | MISMATCH | "special registers have fixed hardware functions and require specific instructions to access. They cannot be used as regular memory operands." SD:456 says they are addressed as ordinary register operands. The same page's :22 says "MOV x, PTRA". |
| 456 | (detail) an underlying RAM exists beneath $1F8-$1FF | M | `architecture/cog.yaml:39`; `complete-system-registers-index.yaml:46` | PARTIAL | "$1F8-$1FF (not RAM)"; "not standard RAM". SD implies RAM sits beneath. Mechanism; harmless for code. |
| 458-465 | PTRA $1F8, PTRB $1F9, DIRA $1FA, DIRB $1FB, OUTA $1FC, OUTB $1FD, INA $1FE, INB $1FF | C | `architecture/cog.yaml:43-57`; `complete-system-registers-index.yaml:107-201` | MATCH | |
| 467-468 | INA is also the debug interrupt call address; INB the debug return address | C | `complete-system-registers-index.yaml:183,193`; `architecture/cog.yaml:56-57` | MATCH | "Becomes IJMP0 (R/W) during debug ISR"; "Becomes IRET0" |
| 472-480 | LUT: 512x32 dual-port; uses: load/store, streamer, bytecode table, smart-pin data, pair sharing, code | C | `architecture/lookup_ram.yaml:24-29,228-240` | MATCH | |
| 482-486 | Most instructions cannot address LUT; use RDLUT/WRLUT, which address it as $000-$1FF | C | `architecture/lookup_ram.yaml:34,39-42` | MATCH | "$000-$1FF as seen by RDLUT/WRLUT" |
| 493 | Even/odd pair cogs can each let the other write their LUT through its local writes | C | `architecture/lookup_ram.yaml:52-56,73-80` | MATCH | "Sharing is a write path, not a read path" |
| 495-498 | SETLUTS #0 disallows (default); #1 allows writes from the other cog | C | `architecture/lookup_ram.yaml:157-159`; `language/pasm2/setluts.yaml:12` | MATCH | |
| 500 | Pair writes use the LUT's 2nd port, shared with the streamer in DDS/LUT modes; the external write wins a same-clock clash; not meant to be used together | C | `architecture/lookup_ram.yaml:76-79` | MATCH | "an external write wins a same-clock collision, and the two are not intended to be used together" |
| 502 | COGINIT %x_1_xxx1 finds and starts a free even/odd pair with the same parameters; the program must tell them apart | C | `architecture/lookup_ram.yaml:102-108` | MATCH | |
| 504 | SETSE1..4 can set LUT read/write events for handshaking | C | `architecture/lookup_ram.yaml:95-100` | MATCH | "%1111111AA" |

## Findings

MISMATCH and NOT-CARRIED contract rows, most consequential first.

### 1. Hub-exec forbidden list over-restricts XINIT and XZERO (MISMATCH, 7 sites)
- SD:353-358: "during hub execution these instructions cannot be used: ... XINIT / XZERO / XCONT - when the streamer mode engages the FIFO".
- KB: `language/pasm2/concepts/execution_modes.yaml:80` `"XINIT", "XZERO", "XCONT (when streamer engages FIFO)"`. The same form is at `cog_hub_execution.yaml:342`, `language/pasm2/hubexec.yaml:30` and `architecture/fifo.yaml:241`. `cog_hub_execution.yaml:166` and `language/spin2/constructs/inline_pasm.yaml:114` say "FIFO/streamer ops (RDFAST/.../XINIT/XZERO/XCONT) ... FORBIDDEN". `inline_pasm.yaml:85` says "they would be forbidden in hub-exec".
- Effect: an agent will refuse, or rework, legal hub-exec code that uses the streamer in modes that do not use the FIFO (DDS/LUT, pins->LUT, immediate modes). Fix: put the qualifier on all three. Searches: `XINIT.{0,80}(FIFO|forbidden|hubexec|hub exec)`.

### 2. Spin2 COGINIT notes misstate what COGINIT does to the cog (MISMATCH)
- SD:376-377 "loads its own registers $000..$1F7 from the hub, starting at address S/#, then begins execution at register address $000". SD:379 "%1_x_xxxx The target cog begins execution at register/LUT/hub address S/#". SD:397-398 "This 32-bit value will be written into the target cog's PTRB register".
- KB: `language/spin2/methods/coginit.yaml:134` "All cog registers cleared except PTRA"; `:135` "Cog starts at address 0". The same file's `:140` says COGINIT loads $000-$1F7.
- Not in plan §1, which lists only `:45` of this file. It belongs with the plan's COGINIT-reset row (§1/§11) because it claims a reset.

### 3. `special_registers.yaml` contradicts the register map (MISMATCH, three statements)
- SD:456 "when specifying an address between $1F8 and $1FF, the instruction is accessing a special-purpose register". KB `language/pasm2/concepts/special_registers.yaml:7-9`: "require specific instructions to access. They cannot be used as regular memory operands." Its own `:22` says "MOV x, PTRA".
- SD:446-451 "$1F0 RAM / IJMP3 interrupt call address for INT3 ..." (registers). KB `:29-33`: "IJMP0/IJMP1/IJMP2/IJMP3 ... access: Via SETINT1/SETINT2/SETINT3". The vectors are written with MOV; SETINTx selects the event source. IRETx are left out.
- SD:441 "$000 through $1EF are general-purpose". KB `:8`: "general-purpose registers (cog RAM $000-$1FF)".
- `complete-system-registers-index.yaml` is right on all three, so fix the concept page to match it and link it there.

### 4. MODC/MODZ/MODCZ modifier rule and symbols not carried (NOT-CARRIED)
- SD:328-331: "cccc conditional test used to update C (%0000=clear, %1111=set, all others per EEEE)", the same for zzzz.
- KB `language/pasm2/modcz.yaml:9-10`, `modc.yaml:20-22`: "the 4-bit modifier values select which combinations of current C and Z states produce 1 results". The page says neither that the code matches EEEE nor what the assembler symbols are; the parameters say only "a Modifier symbol".
- Searches: `_CLR|_SET\b`, `\b_(c|z|nc|nz|e|ne|lt|ge|clr|set)\b`, `modifier`, all with no symbol list anywhere in the KB. Compiled in scratch with pnut-ts: `modcz _set,_clr wcz` gives D field `0_1111_0000` and `modc _nc_and_z wc` gives cccc `%0010` (= EEEE `if_nc_and_z`), so the symbols exist and follow the EEEE table. Home: `modcz.yaml` (with modc/modz linking), citing the EEEE table in `conditional_execution.yaml`.

### 5. `hub.yaml` bandwidth block contradicts the hub's 32-bits-per-clock rate (MISMATCH)
- SD:172 "32-bits-per-clock sequential read/write for all cogs, simultaneously".
- KB `architecture/hub.yaml:186` "theoretical: Clock_freq / 2 bytes/second per COG"; `:187-188` sustained "Clock_freq / 8 bytes/second per COG". No source. Contradicted by the same file's `:189` "4 bytes per clock during block transfer" and `:121`. Fix: theoretical = 4 bytes/clock per cog; the "sustained" figures must be sourced or removed.

### 6. SD encoding key states the R bit backwards (source erratum; KB correct)
- SD:313-315 "R 0: 20-bit Address field is relative to current PC. 1: 20-bit Address field is absolute."
- KB `language/pasm2/call.yaml:63` "relative (R=1) or absolute (R=0)"; `loc.yaml:13`; `guides/pasm2-getting-started.yaml:298` "If R = 1 then PC += A". The KB agrees with the CSV and pnut-ts output (plan §9 prototype `FE1FFC12`, R=1, relative).
- Action: record in `engineering/ingestion/SOURCE-ERRATA.md` (not there now: grep `R bit|relative|Table 6`), so that no later pass "corrects" the KB from the SD.

### 7. Smart-pin serial rate ceilings not carried (NOT-CARRIED)
- SD:212-213 "Synchronous serial ... up to clock/2 baud rate"; "Asynchronous serial ... up to clock/3 baud rate".
- Searches: `clock ?/ ?[23]`, `sysclk ?/ ?[23]`, `max.{0,30}(baud|bit rate)`, `fastest`, `minimum` over `architecture/smart-pins/smart-pin-111*.yaml` and `smart_pins.yaml`. None. Home: `smart-pin-11100/11101-sync-serial-*.yaml` and `smart-pin-11110/11111-async-serial-*.yaml` (the X-register bit-period minimum). The smart-pin range may have the per-mode statement.

### 8. Encoding-key glossary missing; 140 pages point at a file that does not exist (NOT-CARRIED)
- SD:292-327 defines C, Z, I, L, R, WW, N/NN/NNN, A and n fields.
- KB: 140 instruction pages carry `# [bits|write|c|z|clocks] See encoding-table-reference.yaml`. No file of that name exists in the repo (find). Only WW (`calld.yaml:73`), R (`call.yaml:63`) and n (`augs.yaml:11`) are explained, piecemeal. Home: a real `encoding-table-reference.yaml` (or a block in `pasm2/concepts/`), or the comment repointed to wherever the key lives.

### 9. Pin DAC output impedances not carried (NOT-CARRIED)
- SD:199 "8-bit, 120-ohm (3ns) and 1k-ohm DACs".
- Searches: `120.?(ohm|Ω)`, `(990|1k|1 ?k|123\.75).{0,10}(ohm|Ω)`, `ohm` over `smart_pins.yaml` and `pin-drive-configuration.yaml`. None. Home: `architecture/smart_pins.yaml` (`dac_per_pin`, :53). The smart-pin range may carry the exact figures.

### 10. Board-level pin facts (NOT-CARRIED, low)
- SD:232 "TEST | I | 0 | Tied to ground". grep `TEST.{0,30}(ground|GND|tied)`: none. Home: `hardware/p2-package-mechanical.yaml`.
- Also partial: SD:238-239 XI/XO "No external resistors or capacitors are required" (not found), and SD:240 RESn low "all cogs disabled and I/O pins floating" (not found; only the 3 ms is carried, at `boot-rom/_index.yaml:27`).

### Partial rows worth adding while those pages are open (not findings, but cheap)
- `language/pasm2/coginit.yaml:5`: add PTRA = 0 when there is no SETQ (SD:404), the pair start returning the even/lower ID (SD:390-392), the $000..$1F7 load then start at $000 (SD:376-377; drop "Reg/LUT"), and that the %1 start may target a register or LUT address (SD:379).
- Little-endian hub (SD:173) is only on `spin2/methods/endianl.yaml:66`; it belongs on `architecture/hub.yaml`.
- `architecture/cog.yaml:179-195`: the pipeline stage names, forwarding and branch-prediction lines are unsourced (SD:286 gives only "five-stage").
- `architecture/hub.yaml:23,229`: "Boot ROM mapped at $FC000" should say the ROM is loaded into the last 16 KB of hub RAM (SD:190). Owned by the boot range.
