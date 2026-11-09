# Silicon Doc walk, range 8: SD:4819-5625

Serial loading protocol, the DAT ORG blink example, and the `instructions.txt` dump (timing diagram,
encoding list, aliases, MODCZ constants, notes, directives).

Method for the encoding list: a script parsed every `EEEE ...` line in the range (359 lines) and looked
each mnemonic up in `deliverables/ai/P2/language/pasm2/<mnemonic>.yaml`. It checked that the SD bit
pattern is one of the page's `encoding[].bits` strings (whitespace-normalised), then grouped the SD operand
form against the page's `syntax:`. Script and output:
`/tmp/claude-1000/-workspaces-P2-Knowledge-Base/365eedcb-d473-4cf3-9fad-05b0d2d16bc1/scratchpad/sdwalk/r8/cmp.py`,
`.../r8/out.tsv`, `.../r8/ops.py`. Result: **353 of 359 bit-identical**, 4 differ in form only (below), 2
are the `<empty>` slots. Every mnemonic in the list has its own page.

The blink example was compiled with `pnut-ts` (`.../r8/blink.spin2`). The output is byte-identical to
SD:4921. The checksum ($E6CE9A2C sum, $89A0D824 complement) and both Base64 strings were recomputed and
agree with SD:4930-4960.

## Sections

| SD line | Heading | Disposition |
|---|---|---|
| 4819 | SERIAL LOADING PROTOCOL | Carried in `architecture/serial_loader.yaml`. One mismatch on the line format (inverted data); small gaps |
| 4862 | Prop_Chk | MATCH |
| 4869 | Prop_Clk | MATCH; the FPGA note and "F0 not required" note are not carried |
| 4882 | PLL Example | MATCH |
| 4894 | Reset to Boot Clock Configuration | MATCH |
| 4901 | Prop_Hex (incl. DAT ORG example, tables 42-45) | MATCH; the example's source program is not carried (bytes are) |
| 4936 | Prop_Txt | MATCH; alphabet values implicit; one internal inconsistency in the YAML |
| 4964 | SUMMARY | PARTIAL (P61..P58 condition missing); "CR line endings" requirement contradicts SD |
| 4969 | Assembly Language | Pointer to the Google doc / instructions.txt; nothing to carry |
| 4981 | instruction timing (diagram) | Mechanism; not carried |
| 5001 | instructions (encoding list) | 353/359 bit-identical; LOCKREL is an SD typo; `<empty>` slots and the TESTP/DIRx shared opcode not carried |
| 5432 | instruction aliases | All alias encodings MATCH (each short form has its own encoding row) |
| 5500 | MODCZ constants (+ Examples 5537) | **NOT-CARRIED**: the `_CLR` .. `_SET` operand symbols appear nowhere in the KB |
| 5548 | notes (ORG/ORGH symbols, abs/rel, `##`) | MATCH; operand-class line IN-PLAN §3 |
| 5578 | assembler directives | ORG default limit contradicts the KB (KB is right per pnut-ts); `[count]` repeat missing from PASM2 data pages |
| 5623 | Boot ROM / Debug ROM | Heading only; next range |

## Ledger

| SD lines | Fact (one line) | Contract/Mechanism | YAML home (file:line) or NOT-CARRIED | Disposition | Note (quotes, searches) |
|---|---|---|---|---|---|
| 4821 | Loader takes 8-N-1 into P63, START=low, STOP=high, 9,600-2,000,000 baud | Contract | `architecture/serial_loader.yaml:27` | MISMATCH, FIXED (task 459): `serial_loader.yaml:27` now reads "...asynchronous serial into P63. The start bit is low and the stop bit is high." The Hardware Manual's inversion sentence is out of served text; its divergence is for the SOURCE-ERRATA entry in task 460 (loader inversion) | YAML (before the fix): "The signal should be inverted; start bit is low, stop bit is high, and data bits are high for 0 and low for 1." (verbatim from HW Manual `p2-hardware-manual-text.txt:1592`). SD: "8-N-1 asynchronous serial into P63, where START=low and STOP=high". SD:4968 says any PC terminal works, which sends true (non-inverted) data. Start-low/stop-high with inverted data is not a valid UART frame. See Findings 2 |
| 4823 | Baud adapts on every `>`; send `> ` first; `>` not passed to parser | Contract | `serial_loader.yaml:39-40` | MATCH | "adapts to the sender's baud rate from every greater-than '>' character" |
| 4825 | Responses on P62 at sender's baud; P62 open-drain when either mask non-0 | Contract | `serial_loader.yaml:25` | MATCH | "will go into open-drain mode when either the INA or INB mask of a command is non-0" |
| 4827 | Active within 15 ms unless preempted by SPI program with pull-up on P60 | Contract | `serial_loader.yaml:30` | PARTIAL, FIXED (task 459): `serial_loader.yaml:30` now says "...in an SPI memory chip with a pull-up resistor on P60 (SPI_CK)..." | YAML (before the fix): "preempted by a program in an SPI memory chip". The P60 pull-up condition is not on this page (it is on boot-pattern-selection.yaml per :15) |
| 4829-4835 | Whitespace = any contiguous run of TAB, LF, CR, SP, `=` | Contract | `serial_loader.yaml:49` | MATCH | "TAB ($09), LF ($0A), CR ($0D), SPACE ($20) and '=' ($3D...)" |
| 4838-4855 | Four commands and their syntax | Contract | `serial_loader.yaml:52-97` | MATCH | syntax strings identical |
| 4859 | Mask/data select chips; a non-matching chip waits for another command; INA[1:0] unusable; underscore keeps keywords unambiguous | Contract | `serial_loader.yaml:50,128-136,96` | PARTIAL, FIXED (task 459): `serial_loader.yaml:49` (chip_identifier) and `:145` (non_matching_chip) state that a chip whose INA/INB ports do not match waits for another command; the "P31-P0 state must match" wording at `:137-143` is replaced by "the INA mask and data values select a chip by its P31-P0 states" | Missing (before the fix): the non-matching chip "waits for another command"; the compare is masked (YAML: "P31-P0 state must match"). INA[1:0] at :136 MATCH |
| 4861 | Unexpected character aborts the command | Contract | `serial_loader.yaml:162` | MATCH | "aborts the current command; the loader waits for a new command" |
| 4862-4867 | Prop_Chk reply CR LF "Prop_Ver G" CR LF | Contract | `serial_loader.yaml:54-56` | MATCH | exchange quoted identically |
| 4869-4875 | Prop_Clk: echo `.`, switch to RCFAST, set config except mode, wait ~5 ms, enable mode | Contract | `serial_loader.yaml:62-63` | MATCH | "switches to the internal 20 MHz clock, sets the desired configuration (except mode), waits about 5 ms" |
| 4877 | Sender waits ~10 ms then sends `> ` | Contract | `serial_loader.yaml:63` | MATCH | "wait an additional 10 ms, then send '> '" |
| 4879 | Image may need HUBSET #$F0 before its own PLL mode | Contract | `serial_loader.yaml:65` | MATCH | |
| 4881 | FPGA: only $00 / $FF clock values | Mechanism (FPGA) | NOT-CARRIED | NOT-CARRIED (FPGA-only; recorded, not carried) | grep `FPGA` in serial_loader.yaml: only ":54 (A-F were FPGA builds)". FPGA-only; low. Task 459 first removed that parenthetical, then (fix round 1) restored a sourced statement at `serial_loader.yaml:53-54`: the ROM booter listing (`rom_booter_v33_01j.lst` lines 125-131, `text_ver` at :448) gives `ver` "A" to "F" as FPGA images (Prop123-A9, DE2-115, DE0-Nano, BeMicro-A2, Prop123-A7, Prop123-A9 16 cogs) and "G" as Prop2 Silicon v2. The first removal's "no source states it" was wrong: the Silicon Doc and Hardware Manual do not, the listing does |
| 4882-4892 | PLL example 19D28F8 then 19D28FB | Contract | `serial_loader.yaml:64,154-159` | MATCH | |
| 4893 | An initial `Prop_Clk ... F0` is not needed: the clock starts in that mode | Contract | `serial_loader.yaml:64` | FIXED (task 459): `serial_loader.yaml:65` (initial_clock_command) | before the fix, grep `not required`, `starts up`, `F0` in serial_loader.yaml: F0 appears only as "Return to the boot clock". Low |
| 4894-4900 | Return to boot clock with F0 | Contract | `serial_loader.yaml:64` | MATCH | |
| 4901-4903 | Prop_Hex loads bytes at $00000; whitespace-separated; low 8 bits used | Contract | `serial_loader.yaml:69-75` | MATCH | "Only the bottom 8 bits of each hex value are used as data." |
| 4905 | `~` does COGINIT #0,#0 from $00000 | Contract | `serial_loader.yaml:35,125` | MATCH | |
| 4907 | `?` replies `.` and runs, or `!` and waits | Contract | `serial_loader.yaml:80-81,100-101` | MATCH | |
| 4910-4928 | Blink example source and its 20 bytes | Contract (example) | `serial_loader.yaml:82-90,145` | PARTIAL, FIXED (task 459): `serial_loader.yaml:83-89` (example_source) and `:90` (example_source_bytes); pnut-ts assembles the source to the same 20 bytes | Before the fix: bytes carried. The source (`not dirb` / `.lp not outb` / `waitx ##20_000_000/4` / `jmp #.lp`) is not. pnut-ts output is byte-identical to SD:4921 |
| 4930-4934 | Checksum long = $706F7250 - sum of longs, anywhere long-aligned | Contract | `serial_loader.yaml:76-79,177-179` | MATCH | "$706F7250 - $E6CE9A2C = $89A0D824, sent as the bytes 24 D8 A0 89". Arithmetic re-verified |
| 4934, 4962 | Start each data line with `>` | Contract | `serial_loader.yaml:40` | MATCH | "use '>' characters periodically throughout the data" |
| 4936-4938 | Prop_Txt: Base64, 6 bits/char, 2.25x denser | Contract | `serial_loader.yaml:86-87` | MATCH | |
| 4939-4947 | Base64 alphabet values (A-Z=$00-$19 ... `/`=$3F) | Contract | `serial_loader.yaml:86` | PARTIAL, FIXED (task 459): `serial_loader.yaml:95` (alphabet) | Before the fix, YAML lists "A-Z, a-z, 0-9, +, /" without values. Standard Base64, so low |
| 4949 | Whitespace ignored among Base64 chars | Contract | `serial_loader.yaml:95` | MATCH | |
| 4952-4960 | Prop_Txt examples with and without checksum | Contract | `serial_loader.yaml:97,149` | MATCH | strings re-derived from the compiled bytes; identical |
| 4936, 4957 | Prop_Txt accepts `~` or `?` | Contract | `serial_loader.yaml:88` vs `:117-120` | PARTIAL, FIXED (task 459): `serial_loader.yaml:129` base64_mode now stops on '~' or '?' | Before the fix, `:88` correct ("~ ... ? verifies"). `base64_mode` at `:120` says only "Stop on '~' character". The YAML disagrees with itself |
| 4966 | Many chips from one line: distinct INA/INB signatures and no SPI/SD on P61..P58 | Contract | `serial_loader.yaml:127-139` | PARTIAL, FIXED (task 459): `serial_loader.yaml:147` (loading_many_chips) | Before the fix, the P61..P58 condition was missing. grep `P61..P58`, `P58`, `uniquely` in serial_loader.yaml: no hits |
| 4968 | A terminal works with no new-line conventions to worry about | Contract | `serial_loader.yaml:169` | MISMATCH, FIXED (task 459): `serial_loader.yaml:182` says no line-ending convention is required (all of TAB, LF, CR, SPACE, '=' are whitespace) | Before the fix, YAML requirement: "CR line endings". SD: "needn't worry about PC/Mac/Unix new-line differences" (CR and LF are both whitespace, SD:4831-4832). Low |
| 4969-4976 | Pointer to the Google instruction doc / instructions.txt | n/a | - | - | nothing to carry |
| 4981-4999 | Pipeline diagram: rdRAM I/D/S, latch, ALU, wrRAM, stall `gox`/`go`/`get` | Mechanism | NOT-CARRIED | NOT-CARRIED (mechanism; recorded, not carried) | grep `rdRAM`, `wrRAM`, `'gox'`, `stall/done` across the KB: 0 hits. Mechanism only |
| 5004-5041 | ROR..SAL, ADD..SUBSX, CMP..CMPSUB, FGE..FLES, SUMC..SUMNZ (40 rows): `CZI`, `D,S/# {WC/WZ/WCZ}` | Contract | e.g. `ror.yaml:29`, `add.yaml:22`, `cmpsub.yaml:29`, `sumnz.yaml:27` | MATCH | bits identical; syntax `D,{#}S {WC|WZ|WCZ}` on all |
| 5043-5050 | TESTB/TESTBN: four opcodes each, WC/WZ, ANDC/ANDZ, ORC/ORZ, XORC/XORZ | Contract | `testb.yaml:2-23`, `testbn.yaml:5-20,31-32` | CLOSED against task 449: `testb.yaml:2` (syntax lists WC\|WZ\|ANDC\|ANDZ\|ORC\|ORZ\|XORC\|XORZ), `:39-40` (parameter), `:42-43` (flags_affected), `:59-62` (syntax_variants) name all eight effect keywords; no edit in task 459 | All 8 encodings MATCH. (Before task 449:) `testb.yaml` syntax is "TESTB D,{#}S WC/WZ" and nowhere names the ANDC/ANDZ/ORC/ORZ/XORC/XORZ keywords. Its flags say only "or AND/OR/XOR with C". `testbn.yaml:31` does name them |
| 5052-5059 | BITL..BITNOT share TESTB's opcodes, `{WCZ}` | Contract | `bitl.yaml:4` .. `bitnot.yaml:20` | CLOSED against task 449 (CP-033): `testb.yaml:44-45` (encoding_notes) and `:48` (CP-033 source) state the shared opcode fields and the effect split; no edit in task 459 | bits MATCH. The shared-opcode / effect split is CP-033 |
| 5061-5089 | AND..XOR, MUXC..MUXNZ, MOV..NEGNZ, INCMOD..SIGNX, ENCOD..TESTN (28 rows) | Contract | e.g. `and.yaml:4`, `testn.yaml:32` | MATCH | |
| 5091-5121 | SETNIB..ROLWORD (`NNN`/`NN`/`N` fields), ALTSN..ALTI, SETR/D/S, DECOD..MOVBYTS (31 rows) | Contract | e.g. `setnib.yaml:29`, `movbyts.yaml:4` | MATCH | N-field split and `0NI`/`1NI`/`10I` sub-codes identical |
| 5123-5136 | MUL/MULS/SCA/SCAS `{WZ}`, ADDPIX..MIXPIX, ADDCT1-3, WMLONG (13 rows) | Contract | e.g. `mul.yaml:30`, `wmlong.yaml:4` | MATCH | |
| 5138-5144 | RQPIN `C0I`/RDPIN `C1I` `{WC}`, RDLUT/RDBYTE/RDWORD/RDLONG `CZI` with PTRx | Contract | `rqpin.yaml:4`, `rdpin.yaml`, `rdlong.yaml:5` | MATCH | YAML writes PTRx as `/P` in the compiler pattern; same meaning |
| 5146 | CALLD D,S/#rel9 `{WC/WZ/WCZ}` | Contract | `calld.yaml:74` | MATCH | |
| 5148-5199 | CALLPA/CALLPB `0LI`/`1LI`, DJZ..TJV, JINT..JNQMT event jumps (D = event code) (47 rows) | Contract | e.g. `djz.yaml:4`, `jint.yaml:4`, `jnqmt.yaml:20` | MATCH (bits) / IN-PLAN §3 (operand) | bits identical. `S/#rel9` meaning and the units are §3 (43 S-branch pages) |
| 5201-5202 | Two unassigned slots `1011110 1LI` and `1011111 0LI`, form D/#,S/# | Contract (low: decoders, hand-encoders) | `language/pasm2/concepts/instruction_encoding_key.yaml:117-123` (unnamed_encodings) | FIXED (task 459): both slots recorded there; what the words do when executed is not documented (instruction CSV rows 213 and 214 give no description either) | Before the fix, grep `<empty>`, `1011110 1LI`, `1011111 0LI`, `unused opcode`, `reserved opcode`, `unassigned`, `undefined opcode`: 0 hits. Likely home: an opcode-map page (none exists; see Notes) |
| 5204-5231 | SETPAT, WRPIN/WXPIN/WYPIN/WRLUT, WRBYTE..WRLONG, RDFAST/WRFAST/FBLOCK, XINIT/XZERO/XCONT, REP, COGINIT `CLI`, QMUL..QVECTOR (22 rows) | Contract | e.g. `wrpin.yaml:4`, `coginit.yaml:24`, `qvector.yaml:4` | MATCH | |
| 5233-5241 | HUBSET, COGID `C0L`, COGSTOP, LOCKNEW `C00`, LOCKRET, LOCKTRY, QLOG, QEXP (8 rows) | Contract | e.g. `hubset.yaml:4`, `qexp.yaml:4` | MATCH | |
| 5239 | LOCKREL `EEEE 1101011 00L DDDDDDDDD 000000111` with `D/# {WC}` | Contract | `lockrel.yaml:4` | MISMATCH (SD error; KB right): no KB change; closed against task 460, which writes it to SOURCE-ERRATA | YAML: `C0L`. SD shows C=0 but allows `{WC}`, so the SD line contradicts itself. CSV:247 has `C0L` with WC. No KB change; a SOURCE-ERRATA candidate |
| 5243-5262 | RFBYTE..RFVARS, WFBYTE..WFLONG, GETQX/GETQY, GETCT `C00`, SETDACS, SETXFRQ, GETXACC, WAITX `CZL` (16 rows) | Contract | e.g. `rfbyte.yaml:4`, `waitx.yaml:4` | MATCH | |
| 5257 | GETRND `CZL` with `{D} {WC/WZ/WCZ}` | Contract | `getrnd.yaml:3-12,40-41` | PARTIAL, FIXED (task 459): `pasm2/getrnd.yaml:17-21` (description) states the D form writes RND[31:0] to D and the no-D form produces only C and Z; `:34-36` syntax_variants lists both forms. The file was unchanged when read (task 445's rewrite is of `spin2/methods/getrnd.yaml`, a different file) | Before the fix, encoding: YAML splits it into `CZ0 DDDDDDDDD` and `CZ1 000000000`, which is the same thing (CSV:261-262). The description at :13 says only "Get RND into C/Z". It does not say the D form writes RND[31:0] to D (CSV:261 "D = RND[31:0]"), though `write: D` implies it |
| 5264-5311 | SETSE1-4, POLLINT..POLLQMT (D=event, S=000100100), WAITINT..WAITATN, ALLOWI/STALLI, TRGINT1-3, NIXINT1-3 (43 rows) | Contract | e.g. `pollint.yaml:26`, `waitatn.yaml:36`, `nixint3.yaml:4` | MATCH | |
| 5313-5351 | SETINT1-3, SETQ/SETQ2, PUSH/POP, JMP/CALL/CALLA/CALLB D, RET/RETA/RETB `CZ1`, JMPREL..EXECF, GETPTR, GETBRK/COGBRK, BRK, SETLUTS, SETCY..SETCMOD, SETPIV/SETPIX, COGATN (31 rows) | Contract | e.g. `setq.yaml:4`, `jmp.yaml:5`, `retb.yaml:4`, `cogatn.yaml:31` | MATCH | GETBRK syntax "D WC/WZ/WCZ" (effect required) matches |
| 5353-5360 | TESTP/TESTPN with WC/WZ, ANDC/ANDZ, ORC/ORZ, XORC/XORZ | Contract | `testp.yaml:4-19,30,99`, `testpn.yaml:8,27-42` | MATCH | both pages name all eight effect keywords |
| 5362-5396 | DIRx/OUTx/FLTx/DRVx (32 rows) `CZL ... {WCZ}` | Contract | e.g. `dirl.yaml:16`, `drvnot.yaml:47` | MATCH | |
| 5353 vs 5362 (also 5337-5338) | DIRL..DIRNOT reuse TESTP/TESTPN's S codes 001000000-001000111, told apart only by the effect (WCZ vs WC/WZ/ANDx/ORx/XORx). GETBRK/COGBRK share 000110101, told apart by CZ0 vs 00L | Contract (hand-encoding, disassembly) | FIXED (task 459): `encoding_notes` in `testp.yaml:81-82`, `testpn.yaml:66-67`, `dirl.yaml:21-22`, `dirh.yaml:22-23`, `dirc.yaml:22-23`, `dirnc.yaml:46-47`, `dirz.yaml:41-42`, `dirnz.yaml:46-48`, `dirrnd.yaml:52-53`, `dirnot.yaml:48-49`, `getbrk.yaml:9-10`, `cogbrk.yaml:25-26` (all under deliverables/ai/P2/language/pasm2/). All eight pairs compared with SD:5353-5360 and 5362-5369 (code to pair: 000 TESTP/DIRL, 001 TESTPN/DIRH, 010 TESTP ANDx/DIRC, 011 TESTPN ANDx/DIRNC, 100 TESTP ORx/DIRZ, 101 TESTPN ORx/DIRNZ, 110 TESTP XORx/DIRRND, 111 TESTPN XORx/DIRNOT) | FIXED | Before the fix, grep `same opcode`, `same encoding`, `share`, `distinguish` in testp/testpn/dirl/getbrk/cogbrk: 0 hits. The TESTB/BITx case of the same rule is IN-PLAN §2 (CP-033); this one is not |
| 5398-5414 | SPLITB..REV, RCZR/RCZL, WRC..WRNZ, MODCZ `CZ1 0cccczzzz` (17 rows) | Contract | e.g. `splitb.yaml:4`, `modcz.yaml:22` | MATCH | |
| 5416-5417 | SETSCP / GETSCP | Contract | `setscp.yaml:4`, `getscp.yaml:4` | MATCH | |
| 5419-5425 | JMP/CALL/CALLA/CALLB `#{\}A` (`RAA` 20-bit), CALLD `11100WW`, LOC `11101WW` | Contract | `jmp.yaml:10,39`, `call.yaml:58`, `calld.yaml:68`, `loc.yaml:4` | MATCH | |
| 5427-5428 | AUGS `11110NN ...`, AUGD `11111NN ...` #N | Contract | `augs.yaml`, `augd.yaml` (encoding row) | MATCH | Only the letters differ: YAML uses `SS..`/`DD..`, SD uses `NN..`, CSV:408 uses `nn..`. Same 23-bit field |
| 5435 | NOP = $00000000 | Contract | `nop.yaml:16` | MATCH | |
| 5437-5446 | NOT/ABS/NEG/NEGC/NEGNC/NEGZ/NEGNZ/ENCOD/ONES/TEST reg = op reg,reg | Contract | second encoding `CZ0 DDDDDDDDD DDDDDDDDD` on each page, e.g. `not.yaml:34` | MATCH | |
| 5448-5470 | SETxxx reg/# = op 0,reg/#,#0; GETxxx/ROLxxx reg = op reg,0,#0; ALTx reg = ALTx reg,#0; ALTI reg = ALTI reg,#%101_100_100 | Contract | second encodings, e.g. `setnib.yaml` (`1000000 00I 000000000 S`), `getnib.yaml` (`1000010 000 D 000000000`), `alti.yaml` (`001 D 101100100`) | MATCH | all 22 checked |
| 5472-5473 | DECOD/BMASK reg = op reg,reg | Contract | `decod.yaml`, `bmask.yaml` (`000`/`010 D D`) | MATCH | |
| 5475-5476, 5490-5491 | POPA/POPB = RDLONG reg,--PTRx; PUSHA/PUSHB = WRLONG reg/#,PTRx++ | Contract | `popa.yaml:4` (`CZ1 D 101011111`), `pusha.yaml:4` (`0L1 D 101100001`), popb/pushb | MATCH | S fields decode to --PTRA ($15F) / PTRA++ ($161), the same values as CP-032 |
| 5478-5486 | RESI3..0 / RETI3..0 as CALLD pairs | Contract | `resi0.yaml:4,13` ("CALLD $1FE,$1FF WCZ"), `reti0.yaml:4,13`, resi1-3, reti1-3 | MATCH | INA=$1FE, INB=$1FF |
| 5488 | AKPIN reg/# = WRPIN #1,reg/# | Contract | `akpin.yaml:23` (`1100000 01I 000000001 S`) | MATCH | |
| 5493 | XSTOP = XINIT #0,#0 | Contract | `xstop.yaml:4` (`1100101 011 0 0`) | MATCH | |
| 5495-5496 | MODC c = MODCZ c,0 {WC}; MODZ z = MODCZ 0,z {WZ} | Contract | `modc.yaml:4` (`C01 0cccc0000`), `modz.yaml:4` (`0Z1 00000zzzz`) | MATCH | |
| 5500-5534 | MODCZ operand symbols: `_CLR`=%0000 .. `_SET`=%1111, with aliases `_GT`,`_GE`,`_NE`,`_E`,`_LT`,`_LE`, `_NC_AND_NZ` etc. | Contract | `pasm2/modcz.yaml:27-59` (modifier_symbols) | CLOSED against task 446 (written there; verified in task 459 name by name): 32 names and 16 values equal SD:5503-5534 line for line (grep count of `_NAME: '%bbbb'` lines in modcz.yaml = 32, of `_NAME = %bbbb` lines in SD = 32); pnut-ts assembled every one of the 32 names in the cccc position and again in the zzzz position, and the decoded field equals the SD value for all 64 (recorded in Findings 1) | See Findings 1 |
| 5537-5545 | MODCZ/MODC/MODZ examples using the symbols | Contract | `pasm2/modcz.yaml:65-70` (effect_cases); `modc.yaml:34-35`; `modz.yaml:34-35` | CLOSED against task 446: all five examples present and assembled by pnut-ts | the IF_ versus MODCZ name sets are told apart in `modcz.yaml:11-25` and `concepts/conditional_execution.yaml:129-131` (task 459) |
| 5551-5556 | ORGH symbol = hub address; ORG symbol = cog address, `@` gives hub address (`COGINIT #0,#@newcode`) | Contract | `concepts/labels.yaml:106-107,119`; `concepts/branch_addressing.yaml:32` | MATCH | "@label is the hub address of a label defined under ORG" |
| 5559-5564 | `#` before branch/LOC address; assembler picks absolute across cog/hub, relative within; `#\` forces absolute | Contract | `concepts/branch_addressing.yaml:21,24-32,98`; `labels.yaml:100-101` | MATCH | "Crossing between cog and hub is always absolute; the assembler forces it" |
| 5566-5568 | Operand classes: rel_imm9/ind_reg20; abs_imm20/rel_imm20/ind_reg20; LOC abs/rel_imm20 | Contract | `concepts/branch_addressing.yaml` | IN-PLAN §3, closes against task 448 (not edited in task 459) | `offset_units` table and the 43 S-branch pages |
| 5571-5575 | `##` invokes AUGS/AUGD (`AND address,##$FFFFF`, `DJNZ register,##far_away`) | Contract | `augs.yaml:31,104-106` | MATCH | `##` S-branch width is IN-PLAN §3 / §10 (arm B) |
| 5580-5583 | ORGH {addr}: hub mode, fill to addr with $00 | Contract | `orgh.yaml:10,27-29` | PARTIAL, FIXED (task 459): `orgh.yaml:30` states ORGH {hub_address} sets hub mode and an optional address to fill to with $00 bytes; `:36` cites it | Before the fix, the fill was stated only for PASM-only programs (:29). The page leads with Spin2+PASM default $400 and a limit parameter SD lacks; it is newer and compiler-checked, so it does not contradict SD |
| 5585-5589 | ORG {addr{,limit}} defaults $000,$200; $200-$3FF selects LUT; no data | Contract | `org.yaml:17,42-43` | MISMATCH (SD stale; KB right): no KB change; closed against task 460, which writes it to SOURCE-ERRATA | YAML: "bare ORG defaults to address 0 with limit $1F8 ... compiler-verified". SD: "Defaults to $000,$200." Checked here with pnut-ts: bare ORG + 504 longs ok, + 505 longs gives "Cog address exceeds limit (m113)", so the limit is $1F8. LUT range MATCH (:17). Spin2 v55 (`spin2-v55-text.txt:313`) also says $1F8. No KB change |
| 5592-5595 | ORGF fills to cog address with $00; cog mode only | Contract | `orgf.yaml:13-18,49` | MATCH | "ORGF is only valid in COG mode" |
| 5597-5600 | RES reserves cog registers, no data, cog mode only | Contract | `res.yaml:5,22` | PARTIAL, FIXED (task 459): `res.yaml:21-22` state RES generates no data and must be in cog mode (SD:5599); the source is `res.yaml:28`. The assembler's refusal of RES in ORGH mode (pnut-ts: "RES is not allowed in ORGH mode") is not in served text: no CP record exists for it (QUESTION returned) | Before the fix, YAML: "RES only reserves space in cog RAM". It said nothing on whether RES is legal or refused in ORGH mode |
| 5602-5605 | FIT cog_or_hub_address | Contract | `fit.yaml:3-10,33-35` | MATCH | |
| 5607-5610 | ALIGNW/ALIGNL align to word/long in hub | Contract | `alignw.yaml:3-10`, `alignl.yaml` | MATCH | |
| 5612-5617 | BYTE/WORD/LONG data with optional `[count]` repeat | Contract | `pasm2/byte.yaml:10`, `word.yaml:10`, `long.yaml:10`; carried on `spin2/keywords/DAT.yaml:14,59` | PARTIAL, FIXED (task 459): syntax `byte.yaml:10`, `word.yaml:10`, `long.yaml:10` now `data{[count]}{, data{[count]}...}`; examples `byte.yaml:12-17`, `word.yaml:12-15`, `long.yaml:12-15`; notes `byte.yaml:28`, `word.yaml:22`, `long.yaml:26`; sources `byte.yaml:38`, `word.yaml:32`, `long.yaml:36` (lines re-found after fix round 2); a scratch program of the repeat forms (`0[100]`, `$FF[4], 0`, `$AAAA[50]`, `0[16]`, `5[2], 6`) assembled with pnut-ts to 281 bytes (100+5+100+64+12); the YAML examples are the first four forms. Fix round 1: the same syntax in `spin2/assembly-directives/{byte,word,long}.yaml:5` and `spin2/keywords/{BYTE,WORD,LONG}.yaml` (DAT data context) | Before the fix, PASM2 data pages give "[label] BYTE value[, value...]" without `[count]`. grep `\[count\]` in language/pasm2: 0 hits. The Spin2 DAT page carries it |

**Counts (ledger rows):** MATCH 51 · PARTIAL 11 · MISMATCH 4 (2 are SD errors where the KB is right) ·
NOT-CARRIED 7 (2 mechanism/FPGA) · IN-PLAN 3. The S-branch row counts as MATCH for its bits and IN-PLAN
for its operand. Encoding lines: 359 = 353 bit-identical + 4 form-only
differences (LOCKREL SD typo, GETRND split form, AUGS/AUGD letters) + 2 `<empty>`.

## Findings

1. **MODCZ operand symbols are not in the KB at all (SD:5500-5545). Contract, high.** Correct code
   writes `MODCZ _CLR, _Z_OR_C WCZ`, `MODC _NZ_AND_C WC`, `MODZ _Z_NE_C WZ`. The 32 names and their
   values (`_CLR`=%0000, `_NC_AND_NZ`/`_NZ_AND_NC`/`_GT`=%0001, ... `_C_OR_Z`/`_Z_OR_C`/`_LE`=%1110,
   `_SET`=%1111) are the only legal way to write the operand symbolically. `modcz.yaml:12-13` (and
   `modc.yaml:36-37`, `modz.yaml:36-37`) say only "CModifer is a Modifier symbol for the designated mode"
   and list none. `concepts/conditional_execution.yaml:48-180` carries the `IF_` names, which differ
   (%0000 is `_RET_` there and `_CLR` here; %1111 is `IF_ALWAYS` there and `_SET` here). Searches:
   `_CLR`, `_SET`, `_GT`, `_GE`, `_LT`, `_LE`, `_NE`, `_E`, `_Z_OR_C`, `_NZ_AND_C`, `_C_NE_Z`,
   `_NC_AND_NZ` not preceded by `IF`, `modifier symbol`, `modcz constant` over all of
   `deliverables/ai/P2/`: no hits outside the `IF_` names. Home: `language/pasm2/modcz.yaml`, linked
   from modc/modz.
   **Task 459 result.** The table and the five examples were already in `modcz.yaml` (task 446); verified
   name by name against SD:5503-5534 (32 names, 16 values). pnut-ts 1.55.10 assembled `MODCZ <name>,_CLR WCZ`
   and `MODCZ _CLR,<name> WCZ` for all 32 names (scratch listing of 69 words, 276 bytes); the cccc field
   (bits 16:13) and the zzzz field (bits 12:9) decoded from the listing equal the SD value for every name,
   and the five SD examples assemble. A wrong name (`MODCZ _FOO,_CLR WCZ`) is refused ("Undefined symbol"),
   and an IF_ name in the operand (`MODCZ IF_Z,_CLR WCZ`) is refused ("Expected a constant, unary operator,
   or "(""). `concepts/conditional_execution.yaml:129-131` and `modcz.yaml:11-25` now state which name set
   is which.
2. **Serial-loader line format states inverted data (SD:4821 vs `architecture/serial_loader.yaml:27`).
   Contract, medium.** YAML: "The signal should be inverted; start bit is low, stop bit is high, and
   data bits are high for 0 and low for 1." SD: "8-N-1 asynchronous serial into P63, where START=low and
   STOP=high", plus "just open a terminal program on your PC ... and type" (SD:4968). A host following
   the YAML would invert its data bits and fail. Start-low/stop-high with inverted data is not a
   consistent UART frame. The YAML sentence copies the Hardware Manual
   (`p2-hardware-manual-text.txt:1592`), so this is a source conflict with the Silicon Doc. It needs a
   SOURCE-ERRATA entry and a fix to the YAML line, not a bench run: the SD's terminal instruction and the
   Prop_Hex/Prop_Txt examples, sent by ordinary UARTs, settle it.
3. **The TESTP/TESTPN vs DIRx shared opcode is not stated (SD:5353-5360 vs 5362-5369; also GETBRK/COGBRK
   SD:5337-5338). Contract, low-medium.** DIRL..DIRNOT use the same `1101011 CZL ... 0010000xx` words as
   TESTP/TESTPN and are told apart only by the effect field. GETBRK (`CZ0`) and COGBRK (`00L`) share
   `000110101`. Searched `same opcode`, `same encoding`, `share`, `distinguish` in `testp.yaml`,
   `testpn.yaml`, `dirl.yaml`, `getbrk.yaml`, `cogbrk.yaml`: none. IN-PLAN §2 CP-033 proves this only
   for TESTB/BITx; the plan could extend CP-033 to these two pairs. Home: `testp.yaml`, `dirl.yaml`,
   `getbrk.yaml`.
4. **`testb.yaml` never names its ANDC/ANDZ/ORC/ORZ/XORC/XORZ effects (SD:5043-5050). Contract, low
   (PARTIAL).** `testb.yaml:2` "TESTB D,{#}S WC/WZ"; `:29` "or AND/OR/XOR with C". The encodings are
   all present, but an agent on this page cannot learn the keyword spelling. `testbn.yaml:31` and
   `testp.yaml:30,99` do name them.
5. **The two `<empty>` opcode slots are not recorded (SD:5201-5202). Contract, low.** `EEEE 1011110 1LI`
   and `EEEE 1011111 0LI` (D/#,S/#) are unassigned. Searches: `<empty>`, the two bit prefixes, `unused
   opcode`, `reserved opcode`, `unassigned`, `undefined opcode`: none. No opcode-map page exists to hold
   them (see Notes).
6. **The `[count]` repeat is missing from the PASM2 data directives (SD:5612-5617). Contract, low
   (PARTIAL).** `pasm2/byte.yaml:10`, `word.yaml:10`, `long.yaml:10`: "[label] BYTE value[, value...]".
   It is carried on `spin2/keywords/DAT.yaml:59` ("Array repetition using [count] syntax").
7. **Smaller serial-loader items.** `serial_loader.yaml:169` requires "CR line endings", against SD:4968
   (MISMATCH, low). `:120` `base64_mode` "Stop on '~' character" omits `?`, contradicting `:88`. Not
   carried: SD:4893 ("initial Prop_Clk F0 not required"), SD:4966 (no SPI/SD on P61..P58 for
   multi-chip), and SD:4859 (a non-matching chip waits for another command).

Not actioned (SD errors, KB correct): LOCKREL `00L` (SD:5239; CSV:247 and `lockrel.yaml:4` say `C0L`).
ORG default `$000,$200` (SD:5589; pnut-ts and Spin2 v55 say limit $1F8, as `org.yaml:17,42` does). Both
are SOURCE-ERRATA candidates.

## Notes (observed, outside the carriage question)

- **Dangling reference.** 140 YAML pages under `deliverables/ai/P2/` carry the comment
  `# [bits|write|c|z|clocks] See encoding-table-reference.yaml`, and no such file exists anywhere in the
  repo. The nearest thing is the manual's
  `engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-iii/appendix-a-encoding-table.md`.
  It is only a comment, so it is probably not served, but it points at nothing.
- **Unexplained source conflict.** `org.yaml:43` says `ORG $100` gets limit $200, and pnut-ts agrees
  (`ORG $100` + $F9 longs assembles cleanly). `spin2-v55-text.txt:313` says
  "ORG $100 ... cog limit = $1F8 (reg, default limit)". Recorded, not chased.
