# P1 Propeller Manual v1.2 — Structure Map (Pass 1 backbone)

> **Re-extraction (current tooling), 2026-06-22.** This is the section→page spine for the
> full re-extraction of the P1 Propeller Manual. It replaces the old-tooling "strategic
> sampling" capture (archived per ingest-source §0.6 once this extraction validates).
> Page numbers below are **printed page numbers, which equal the physical PDF page index
> (offset 0)** — verified against rendered pages, so figure targeting maps directly.

## Document identity (lineage)

| Field | Value |
|-------|-------|
| Title | Propeller Manual — Version 1.2 |
| Version string | 1.2.0-11.06.14-CWR (2011-06-14) |
| Author | Jeff Martin (Parallax Inc.) |
| Copyright | © 2006–2011 Parallax Inc. · ISBN 9781928982593 |
| Subject | Propeller P8X32A (P1) — architecture + Spin + Propeller Assembly (PASM1) |
| Pages | 399 (PDF), printed 1–399 |
| Producer | Acrobat Distiller 9.4.2 (Windows) — digital text layer, NOT scanned |
| Trust tier | 🏆 AUTHORITATIVE (official Parallax) — P1 corpus **primary / backbone** |
| Source PDF | `engineering/ingestion/external-inputs/P1/P1 P8X32A-Web-PropellerManual-v1.2.pdf` |

## Three-chapter architecture

| Part | Pages | Content |
|------|-------|---------|
| Preface | 11–12 | orientation |
| **Ch 1 — Introducing the Propeller Chip** | 13–34 | hardware/architecture: packages, pins, specs, boot/run/shutdown, block diagram, cogs, hub, I/O, system counter, CLK register, locks, memory map, ROM contents (character defs, log/antilog, sine table, boot loader/Spin interpreter) |
| **Ch 2 — Spin Language Reference** | 35–237 | full Spin command reference + categorical listing + operators |
| **Ch 3 — Assembly Language Reference** | 238–378 | full Propeller Assembly (PASM1) reference + master table + categorical listing |
| Appendix A | 379 | Reserved Word List |
| Appendix B | 380–385 | Math samples + function tables (log/antilog, sine) |
| Index | 386–399 | alphabetical index |

## Chapter 1 — Hardware sections (pages)

CONCEPT 13 · PACKAGE TYPES 14 · PIN DESCRIPTIONS 15 · SPECIFICATIONS 16 ·
HARDWARE CONNECTIONS 17 · BOOT UP PROCEDURE 18 · RUN-TIME PROCEDURE 18 ·
SHUTDOWN PROCEDURE 19 · BLOCK DIAGRAM 20 · SHARED RESOURCES 22 · SYSTEM CLOCK 22 ·
COGS (PROCESSORS) 22 · HUB 24 · I/O PINS 26 · SYSTEM COUNTER 27 · CLK REGISTER 28 ·
LOCKS 30 · MAIN MEMORY 30 · MAIN RAM 31 · MAIN ROM 32 · CHARACTER DEFINITIONS 32 ·
LOG AND ANTI-LOG TABLES 34 · SINE TABLE 34 · BOOT LOADER AND SPIN INTERPRETER 34

## Chapter 2 — Spin language command inventory (the Spin1 tree)

Front matter: STRUCTURE OF PROPELLER OBJECTS/SPIN 36 · CATEGORICAL LISTING 38
(Block Designators 38 · Configuration 38 · Cog Control 39 · Process Control 39 ·
Flow Control 39 · Memory 40 · Directives 41 · Registers 41 · Constants 42 ·
Variable 42 · Unary Operators 42 · Binary Operators 43 · Syntax Symbols 44) ·
SPIN LANGUAGE ELEMENTS 45 (Symbol Rules · Value Representations · Syntax Definitions 46)

Commands (headword → page):

ABORT 47 · BYTE 51 · BYTEFILL 57 · BYTEMOVE 58 · CASE 59 · CHIPVER 62 · CLKFREQ 63 ·
_CLKFREQ 65 · CLKMODE 67 · _CLKMODE 68 · CLKSET 71 · CNT 73 · COGID 75 · COGINIT 76 ·
COGNEW 78 · COGSTOP 83 · CON 84 · CONSTANT 91 · CONSTANTS (PRE-DEFINED) 93 ·
CTRA,CTRB 95 · DAT 99 · DIRA,DIRB 104 · FILE 107 · FLOAT 108 · _FREE 110 ·
FRQA,FRQB 111 · IF 112 · IFNOT 117 · INA,INB 118 · LOCKCLR 120 · LOCKNEW 122 ·
LOCKRET 125 · LOCKSET 126 · LONG 128 · LONGFILL 134 · LONGMOVE 135 ·
LOOKDOWN,LOOKDOWNZ 136 · LOOKUP,LOOKUPZ 138 · NEXT 140 · OBJ 141 · OPERATORS 143 ·
OUTA,OUTB 175 · PAR 178 · PHSA,PHSB 180 · PRI 181 · PUB 182 · QUIT 186 · REBOOT 187 ·
REPEAT 188 · RESULT 194 · RETURN 196 · ROUND 198 · SPR 200 · _STACK 202 ·
STRCOMP 203 · STRING 205 · STRSIZE 206 · SYMBOLS 207 · TRUNC 209 · VAR 210 ·
VCFG 213 · VSCL 216 · WAITCNT 218 · WAITPEQ 222 · WAITPNE 224 · WAITVID 225 ·
WORD 227 · WORDFILL 234 · WORDMOVE 235 · _XINFREQ 236

**OPERATORS** (143–174) is a large multi-page section covering all unary/binary/assignment
operators — extract as its own sub-catalog.

## Chapter 3 — Propeller Assembly (PASM1) instruction inventory (the PASM1 tree)

Front matter: THE STRUCTURE OF PROPELLER ASSEMBLY 238 (Cog Memory 240 · Where Does an
Instruction Get Its Data? 240 · Don't Forget the Literal Indicator '#' 241 · Literals Must
Fit in 9 Bits 241 · Global and Local Labels 242) · CATEGORICAL LISTING 243 ·
ASSEMBLY LANGUAGE ELEMENTS 250 (Syntax Definitions 250 · Opcodes and Opcode Tables 251 ·
Concise Truth Tables 252 · **Propeller Assembly Instruction Master Table 253**)

Instructions / directives / pseudo-entries (headword → page):

ABS 257 · ABSNEG 258 · ADD 259 · ADDABS 260 · ADDS 261 · ADDSX 262 · ADDX 264 · AND 266 ·
ANDN 267 · CALL 268 · CLKSET 271 · CMP 272 · CMPS 274 · CMPSUB 276 · CMPSX 277 · CMPX 280 ·
CNT 282 · COGID 283 · COGINIT 284 · COGSTOP 286 · CONDITIONS (IF_X) 287 · CTRA,CTRB 288 ·
DIRA,DIRB 289 · DJNZ 290 · EFFECTS (WC,WZ,WR,NR) 291 · FIT 292 · FRQA,FRQB 293 · HUBOP 294 ·
IF_X (CONDITIONS) 295 · INA,INB 297 · JMP 298 · JMPRET 300 · LOCKCLR 303 · LOCKNEW 304 ·
LOCKRET 305 · LOCKSET 306 · MAX 307 · MAXS 308 · MIN 309 · MINS 310 · MOV 311 · MOVD 312 ·
MOVI 313 · MOVS 314 · MUXC 315 · MUXNC 316 · MUXNZ 317 · MUXZ 318 · NEG 319 · NEGC 320 ·
NEGNC 321 · NEGNZ 322 · NEGZ 323 · NOP 324 · NR 325 · OPERATORS 326 · OR 327 · ORG 328 ·
OUTA,OUTB 330 · PAR 331 · PHSA,PHSB 332 · RCL 333 · RCR 334 · RDBYTE 335 · RDLONG 336 ·
RDWORD 337 · REGISTERS 338 · RES 339 · RET 342 · REV 343 · ROL 344 · ROR 345 · SAR 346 ·
SHL 347 · SHR 348 · SUB 349 · SUBABS 350 · SUBS 351 · SUBSX 352 · SUBX 354 · SUMC 356 ·
SUMNC 357 · SUMNZ 358 · SUMZ 359 · SYMBOLS 360 · TEST 362 · TESTN 363 · TJNZ 364 · TJZ 365 ·
VCFG 366 · VSCL 367 · WAITCNT 368 · WAITPEQ 369 · WAITPNE 370 · WAITVID 371 · WC 372 ·
WR 373 · WRBYTE 374 · WRLONG 375 · WRWORD 376 · WZ 377 · XOR 378

> Note: several Ch3 "headwords" are NOT opcodes — directives (ORG, RES, FIT, FILE),
> condition/effect reference pages (CONDITIONS, IF_X, EFFECTS, WC, WR, WZ, NR), register
> reference pages (CNT, CTRA/CTRB, DIRA/DIRB, INA/INB, OUTA/OUTB, PAR, PHSA/PHSB, VCFG,
> VSCL), and OPERATORS/SYMBOLS reference pages. Classify each at the code/pass-4 stage.

## Extraction inputs staged (working, /tmp/p1-ingest)

- `pdf2md/` — docling markdown (table + structure recovery) — **Pass 1 fidelity**
- `p1-layout.txt` — `pdf-layout` (pdftotext -layout, 14,574 lines) — **Pass 2 code listings**
- `images-raw/` — `pdfimages` rasters: **only 7 unique** (mostly decorative) → confirms most
  figures are **vector** → Pass 3 uses **page-render + crop**, not raster XObject extraction
- `pages/` — `pdftoppm` 150 dpi page renders (figure crop source)
