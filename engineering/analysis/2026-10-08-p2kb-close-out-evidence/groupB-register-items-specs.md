# Group B — the 13 register items: change specs (close-out study «#407», 2026-10-09)

Read-only reviewer; the arbiter re-read `p2-hardware-manual-text.txt:1488`, `:1611`, `:1634` and
`silicon-doc-text.txt:3946`, `:4579`. Abbreviations: SD = `sources/silicon-doc/silicon-doc-text.txt`,
HW = `sources/p2-hardware-manual/p2-hardware-manual-text.txt`, DS = `sources/p2-datasheet/p2-datasheet-text.txt`,
V55 = `sources/spin2-v55/spin2-v55-text.txt`, CSV = P2 Instructions v35 sheet, EF = the empirical ledger,
DP = `deliverables/ai/P2`. Nothing was compiled; replacement code needs pnut-ts in the sprint.

## F-550 — `DP/architecture/serial_loader.yaml` (change spec)
Authority `HW:1593-1725`, `SD:4859-4868`, `sources/rom-booter/rom_booter_v33_01j.lst:125-131`.
| Site | Current | Correct | Authority |
|---|---|---|---|
| `:54` | `Prop_Chk` | `> Prop_Chk 0 0 0 0` | `HW:1609`, `:1634` |
| `:55` | `'Prop_Ver Au'` (version A) | `CR+LF+"Prop_Ver G"+CR+LF` (Rev B/C; A–F were FPGA builds) | `HW:1631-1634`, `SD:4863-4868`, `.lst:125-131` |
| `:60` | `Prop_Clk P1 P2 P3` | `Prop_Clk <INAmask> <INAdata> <INBmask> <INBdata> <HUBSETclocksetting>` | `HW:1611` |
| `:61-66` | p1/p2/p3 and `Prop_Clk 2 8 1` | e.g. `> Prop_Clk 0 0 0 0 19D28F8`, reply `.`, wait ~10 ms, send `> `; `Prop_Clk 0 0 0 0 F0` returns to boot clock | `HW:1639-1661` |
| `:84` | `Prop_Txt ~` | `Prop_Txt 0 0 0 0 <base64chrs> ~` or `?` | `HW:1616-1617`, `:1716`, `:1722` |
| `:91` | `~75% vs 44% for hex` | remove; source says Base64 is "2.25x denser than hex" | `HW:1703` |
| `:99-102` | `'?'` error, `'> '` loader prompt | `.` = valid Prop_Clk / good checksum; `!` = bad checksum; `?`/`~` are sender terminators; `> ` is the sender's auto-baud | `HW:1593`, `:1640`, `:1666-1667` |
| `:36-50` | auto-baud "from CR" | re-adapts at every `>` ($3E); initial `> ` required; `>` not passed to the parser | `HW:1593` |
| `:141-143`, `:157`, `:161-164` | session examples, `Prop_Clk 2 16 1`, `?` on error | `HW:1634` form; remove; `!` on bad checksum, bad characters abort | `HW:1627`, `:1666` |
| `:123`, `:185-193` | `'Prop'` header with length | checksum-complement long (`$706F7250` minus the sum of all longs), long-aligned anywhere; reply `.`/`!` | `HW:1688-1699` |
| `:127-138` | multi-chip | add: INA[1:0] (P0/P1) cannot be matched | `HW:1623`, `SD:4859` |
| `:204`, `:206-210` | "don't pull up P61"; efficiency/speed figures | remove (unsourced) | — |
Class sweep: `Prop_Ver`, `Prop_Clk [0-9]`, `prop_chk` over DP — only this file.

## F-562 — `DP/hardware/hub75_adapter.yaml` (change spec)
`:156` → "ISP Hub75 Matrix Driver"; `:158` → `https://obex.parallax.com/obex/isp-hub75-matrix-driver/`.
Authority `external-inputs/source-code/obex-projects/2850-ISP_Hub75_Matrix_Driver/2850_metadata.yaml:51`, `:57`;
`DP/community/obex/objects/2850.yaml:50`, `:56`; the file's own `:62`. The old name is the GitHub repo name.
`:150` `source: P2 HUB75 LED Matrix Driver Study` is a label (F-560 class).

## F-561 (YAML half) — `DP/application-notes/p2an003-dac-analog-signal-generation.yaml:98` (change spec)
Keep "mode (WRPIN/WXPIN) before raising DIR"; drop "universal" and "reversing it leaves the first output
cycle undefined". For the DAC modes a WYPIN written while DIR is low is captured (`SD:3946`, `:3963`
"During reset (DIR=0), IN is low and Y.[15..0] is captured"); sync-TX `%11100` is the exception (EF-090,
`EF:1618`); general order EF-011 (`EF:240`). Sweep: only `:98`. The prose twin
`app-notes/P2AN003/opus-master/P2AN003.md:541` changes in the same release (agreement gate).

## F-392 — the top-level cog stack (change spec; carve-out expiry met by «#401»)
From the v55 interpreter (`external-inputs/source-code/spin-interpreter/v55/Spin2_interpreter.spin2`):
VAR cleared `:34-35`; stack set up `:37-38` with `pbase`/`vbase` at `dbase_init`, launched `:40-41`;
`dbase_init long @test_dbase`, `var_longs` `:46-47`; V55:1036 DEBUG INIT "stack space starting at $010BC".
Grows upward (`wrlong v,ptra++` `:686`). Call frame = 6 longs (v/pbase/vbase/dbase/mrecv/msend,
`setq #6-1` `:665-693`; `launch_spin` `:2028-2036`) plus locals (≤64 KB, V55:279). No limit check (PTRA
compared nowhere: `:823`, `:1439`, `:1926`, `:2185` are other uses). `_STACK`/`_FREE` inert in Spin2 (the
register's compile proof). Spec: a new documented "top-level cog stack" entry — home not decided (a new
`language/spin2/concepts/` entry, or a block in `methods/cogspin.yaml` linked from
`application-notes/p2an006-sizing-cog-task-stacks.yaml`). The "free hub RAM to $7FFFF / $7BFFF with
DEBUG" point depends on F-393.

## F-548 — driver restatement in hardware pages (change spec + sweep)
`DP/hardware/edge-32mb-module.yaml`: rename `:274` header; in `:277-296` keep `:279-280` (133/84 MHz,
`sources/edge-32mb-module/edge-32mb-module-narrative.txt:392`, `:395`) and `:295-296` (8 µs CE# low —
driver comment `obex-projects/4162-…/psram16drv.spin2:185`; the APS6404L datasheet is not held), remove
`:282-292`, `:298-301` (S-259), `:303-320`; `:322-325` flash 133 MHz — no source, remove or mark unknown;
remove `:335-390` (driver API), `:404-409`, `:420`, `:486-488`; `:268-271` point to OBEX 4162 only.
Siblings: `addon-control-board.yaml:78`, `:115-135` (with S-258); `addon-led-matrix.yaml:106-107`,
`:112-121`, `:148-152`, `:171`, `:175`; `addon-goertzel-touch.yaml:115`; `edge-standard-module.yaml:253`;
`addon-hd-audio.yaml:149`, `:157` (verify against the guide). Unsourced `power_sharing` to remove:
`addon-digital-video-out.yaml:184`, `addon-goertzel-touch.yaml:121`, `addon-control-board.yaml:202`,
`addon-serial-device.yaml:104`, `addon-led-matrix.yaml:182`; and `addon-serial-device.yaml:89`.
Not defects: `addon-rtc.yaml:123-131`, `hub75_adapter.yaml:160`. The register's 18-file count was not
re-derived (grep-level sweep).

## F-551 — `DP/guides/pasm2-getting-started.yaml` (block-by-block)
| Lines | Disposition |
|---|---|
| 173-213 | `:183` "or LUT register" wrong (LUT only via RDLUT/WRLUT); `:203` C is carry (CSV) — S-266; `:213` re-derive; add a source |
| 365-392 | cite `SD:3189-3193`; add the pointer step size |
| 394-429 | compile + source |
| 431-454 | cite `V55:802-803`, `:813` (S-091-adjacent); compile |
| 456-493 | `:473` `:labelname` unsourced (V55:813 has "regular and local symbols"); `:491` `$` = current origin (`V55:312`, `:321`); sibling `language/pasm2/concepts/labels.yaml:51-54`, `:118-128` |
| 513-549 | `:536` data after cog code with `@message` — compile and execute-check |
| 551-561 | `:554` Spin2 DEBUG syntax in a PASM2 guide — verify the PASM2 form; compile `-d` |
| 574-594 | `:578` C is carry/borrow, not "overflow" (CSV) |
| 599, 603-604 | "+1 if not long-aligned" unsourced; hub-exec branch 13…20 / 13…28 is CSV `:193`, `:343`, `:426-427`; QMUL "55-clock latency, 8-clock issue" → CSV 2…9 / 2…17, `SD:3413` 54-clock pipeline; "Silicon Doc v35" (S-265) |
| 626-636, 45-48 | name real keys for "Full PASM2 instruction reference", "Multi-COG programming", "CORDIC", "Streamer" |
| 71, 112, 169, 615 | remove dated history notes from reader text |

## F-354 — three board facts
1. #64013 RTC pull-ups: **blocked — missing document** (the #64013 schematic; the guide defers to the
   product page). `addon-rtc.yaml:104-111` already states the gap. A test needs the physical board (external).
2. #64006 PCB sizes: **closable** from the guide's drawings, pp.11-12 of
   `sources/p2-eval-add-on-boards/64006-P2-Eval-Add-on-Boards-Product-Guide.pdf` (read as images):
   A/V 3.2 × 1.3 in; Goertzel 3.2 × 1.2 in; small modules 1.6 × 0.8 in (drawn: LED matrix).
   `addon-goertzel-touch.yaml:32-35` → "3.2 × 1.2 in (81.3 × 30.5 mm)"; contradiction `:34` "medium" vs
   `:150` `size_class: small_addon`. Verify the other small boards before setting numbers.
3. `addon-serial-device.yaml` "3.3 V": **blocked** — the guide gives no supply for Serial Device
   (`p2-eval-add-on-boards-text.txt:253-284`); the Serial Host needs 5 V (`:113-115`); the Rev B note
   (`:405-407`) says the 5 V shunt supplies "the Serial Device board" — conflict. Remove the unsourced
   `:89`, `:104` meanwhile. Question: which board does the 5 V note mean?

## F-386 — bench question VO-J-028 (retained)
Eight pages, not ten (`VERIFICATION-OPPORTUNITIES.md:73`): `%01111`, `%10010`–`%10111`, `%11001`; order
sites (WYPIN before DIRH) `smart-pin-01111-…:62-63`, `10010-…:65-66`, `10011-…:61-62`, `10100-…:69-70`,
`10101-…:78-79`, `10110-…:79-80`, `10111-…:74-75`, `11001-…:93-94`; non-zero Y in `pinstart`
`10010-…:47`, `10100-…:89`. Sources silent on Y at reset for these modes: term `During reset` in SD, HW,
`smart-pins-titus-text.txt`, `smartpins-narrative-from-docx.txt` — Z only (`SD:4116-4254`, HW
`:1174-1266`); control hits for pulse/transition ("Y is set to zero", `HW:1107`, `:1114`) and PWM ("Y[15:0]
is captured", `HW:1087`, `:1097`). No EF covers it. Jumper-testable (source pin → measuring pin, free
pins; control = the after-DIRH arm). `%11001` needs an arm with an observable Y override.

## F-372 — bench question (G-027) + small edit
`smart-pin-11011-usb-host-device.yaml:16` keeps "A new WRPIN can be done … without resetting the smart
pin": present in `HW:1488`, `silicon-doc/p2-documentation.txt:8885`, the narrative `:2475`, Titus `:1381`;
absent from `SD:4579`. Sources disagree (not silent). Question: with a USB pair running, does a new WRPIN
with DIR high switch `%1_11011_0` ↔ `%0_11011_0` without a DIR cycle? Jumper-only. Edit regardless:
`:9` cite all four; `:10` `pin_pairing` add "and %HHH_LLL drive modes" (`SD:4579`).

## F-337 remainder — bench question + interim edit
Smart pin OFF, `DAC_MODE` `%TT=00`: DS `:1175` and `HW:897` "DIR enables DAC"; `sources/silicon-doc/part4-smart-pins.txt:83`
"OUT enables ADC"; DS legend `:1138-1146` "DAC modes use DIR". EF-071 settles only the smart-mode row;
EF-055/EF-063 rigs drive DIR and OUT together. Question: four arms DIR×OUT at `M[12:10]=%101`,
`%TT=%00` — does the DAC drive on DIR alone, does OUT alone run the ADC? Reuse the EF-071 rig (P4→P5)
with SSSSS=0. Interim: `DP/architecture/smart_pins.yaml:407-411` add the DS/HW wording as a conflict note.

## F-336 — documentary half + Stephen's call
`P_HIGH_15K | P_LOW_FLOAT` follows from the field definitions (`SD:206`, `DS:117` separate high/low drive;
`DS:1136-1147` 3-bit HHH/LLL, `111` = float). `DP/architecture/pin-drive-configuration.yaml:297-299` can
move from the gap list to an idiom entry "documentary composition, not bench-verified". Stephen's call:
ship as documentary composition (recommended, with a bench follow-up), bench first (P4→P5, EF-063/064
`weak_read` routine), or keep as a gap. The 8-rung sweep half is optional characterisation, not a defect.

## F-545 — key census (partial)
Filter `remove_fields` (`engineering/tools/generate-p2kb-index.py:44-48`) does not grow. Classified:
`extraction_status`, `last_verified` (OBEX objects only) — remove; `provenance:`, `primary_sources:`,
`cross_check_sources:` (app notes `p2an001`–`p2an007`, `architecture/click_module_integration.yaml:20`,
`hardware/addon-hyperram-hyperflash.yaml:156`) — fold into `sources:`; `range_source` (~12
`language/pasm2/*.yaml`, e.g. `rdlong.yaml:19`) — fold into `source:`; `source_document`
(`code-examples/smart-pins-00{1,2}-*.yaml:9`, an archived tutorial) — remove with S-001/S-002;
`authority_tier` (decomposition) — **content, keep**; `original_archiver_name` — attribution content;
`derived_from` (`timing_operations.yaml:98`, `:148`), `provenance: "heuristic, unsourced"` (`cogspin.yaml:81`)
— reader caveats, reword as content. Not done: per-key counts; `import_source`, `rescrape_source`,
`authority`, `cite`, `grounding`; the new-name gate.

## F-560 — label-valued `source:` lines (per-site list)
`grep -rn -E "^\s+source: *['\"]?[A-Za-z0-9_-]+['\"]?\s*$" DP` → 78: 42 `community/quick-bytes/*.yaml`
(`parallax-quick-bytes`, in `metadata:` beside `scraped:` and `url:` — a catalogue tag; **Stephen's call**:
relabel as `Parallax Quick Bytes, <url>, scraped <date>` (recommended), leave, or remove); 10 `P2-OctoSerial`
(`operators/op_addmodulo.yaml:100`; `pasm2/alts.yaml:74,85,107`; `pasm2/incmod.yaml:54,62,71`;
`architecture/multi_resource_management.yaml:57,80,96`) — re-source from
`external-inputs/source-code/external-projects/P2-OctoSerial` (file:line) or remove; 2 `P2-Click-eInk`
(`architecture/click_module_integration.yaml:124,202`) — re-source from `…/P2-Click-eInk`; 24 category
labels (`pasm2/rdfast.yaml:35,47`; `lockrel.yaml:43,58,69,79`; `brk.yaml:28,35`; `waitx.yaml:33,42,50,58`;
`altgb.yaml:72`; `muxq.yaml:77,87`; `locktry.yaml:53,63`; `testp.yaml:88`;
`pasm2/concepts/cog_hub_execution.yaml:303`; `pasm2/concepts/streamer_smartpin_control.yaml:261`;
`architecture/smart_pin_patterns.yaml:100,141,156,172`) — invented examples: remove unless a real source
is found. Defects seen: `lockrel.yaml:61-68`, `waitx.yaml:30-32`, `locktry.yaml:47-52`, `altgb.yaml:60-64`
(S-171), `testp.yaml:76-80` (S-175).
