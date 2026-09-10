# P2 Boot ROM — Facility Map

**What is actually in the 16 KB boot ROM, by address, read from the ROM's own assembly listing.**

**Extracted:** 2026-09-10
**Source:** `rom_booter_v33_01j.lst` — the **silicon** build (`ver = "G"`, *Prop2 Silicon v2*,
listing line 131). Source version v141, 2018-05-27.

> 🔴 **Not `ROM_Booter.lst`.** That sibling is the **FPGA** build (`ver = "A"`,
> *Prop123-A9 / BeMicro-A9, 8 cogs, 64 smart pins*). Same source, different target — see
> **F-421**. Mining the FPGA listing would describe a ROM that is not in the chip.

## Why this document exists

Two questions had no answer anywhere in the corpus:

1. *What facilities are in the ROM that we should be documenting?* The one authoritative
   content list — the P2 Hardware Manual, `p2-hardware-manual-text.txt:210` — says only:
   `ROM | 16 KB (Bootloader, P2 Monitor debug interface, and TAQOZ (Forth) command interface)`.
   Three names, no addresses, no inventory. The Datasheet (`:99`) and Silicon Doc (`:189`)
   say *"16KB boot ROM"* and inventory nothing at all.
2. **F-403** removed two fabricated ROM residents that had reached the shipped KB from our own
   generated narrative. It established what the ROM is **not**. This establishes what it **is**,
   from the strongest evidence available — the listing *is* the ROM.

## The map

ROM occupies `$FC000..$FFFFF`. Every address below is read from the listing's own address
column; the section titles are the listing's own banners.

| Address | Facility | Listing evidence |
|---|---|---|
| `$FC000` | **Booter** — cog init. The listing's own banner: *"Cog init - overwritten by SPI program"* | `orgh $FC000`, line 163 |
| `$FC560` | **SD card** — initialise, locate, load and run a file. HUBEXEC. Entry points `_Start_SDcard`, `_Run_SDfile`, `_Load_SDfile`, `_SDcard_Init0/1` | banner *"SD Card - HUBEXEC code..."*, line 996 |
| `$FCA78` | **LMM Monitor** — HUBEXEC. Serial setup (`_SerialInit`, `_SerialBaud`), hub I/O (`_HubTx`, `_HubRxString`, `_HubList`, `_HubHex`), and the command loop `_HubMonitor` at `$FCD78` | banner *"LMM Monitor - HUBEXEC code..."*, line 1706 |
| `$FD028` | **TAQOZ entry** (`_Enter_TAQOZ` at `$FD02C`) | `orgh`, line 2491 |
| `$FD04C` | **TAQOZ version data** — `taqoz_version long 1_1`, `taqoz_name byte "v33h"` | lines 2527, 2532 |
| `$FD058` | **TAQOZ Forth kernel** — output operations onward | `orgh`, line 2532 |
| `$FE9C6` | `_hubexec` — **HUBEXEC code** region | banner *"HUBEXEC CODE"*, line 4531 |
| — | **Hub registers** | banner, line 5132 |
| — | **Tachyon cog kernel** | banner, line 5228 |
| — | **Serial I/O** | banner, line 6043 |
| — | **SPI read/write** | banner, line 6058 |
| `$FF466` | **`romdict` — the TAQOZ word dictionary**, 432 words, ending `$FFFA6` (`END`) | banner *"DICTIONARY"*, line 6171 |

The three facilities the Hardware Manual names are all present and now have addresses. The
listing additionally shows **SD-card boot with FAT32** as a first-class ROM facility — the
changelog's final entry is `PBJ20180527  Added SD and FAT32 routines` — which the Hardware
Manual's one-line inventory does not mention.

## The TAQOZ version in ROM

`taqoz_version = 1_1` and `taqoz_name = "v33h"` (`$FD04C`, `$FD054`; the listing notes the name
must be *"exactly 4 characters = 1 long"*). This is the fact the grounding plan wanted for the
ROM-versus-*TAQOZ Reloaded* question: the ROM carries **v33h**, and any capability described
against Reloaded 2.8 is a superset claim until checked against the dictionary in this folder.

## What this does NOT establish

- **Nothing about unlabelled data.** A 16 KB mask ROM can hold data blocks that no symbol name
  reveals. F-403 made the same reservation about character-font and math-table claims and it
  still stands: what is established is what the listing *names*, never that nothing else exists.
- **No byte-level accounting.** This maps facilities to their entry addresses; it does not
  measure how many of the 16,384 bytes each occupies, and no total is claimed.
- **The Forth-vocabulary half of F-123 remains ungrounded** in the way that finding requires:
  Peter Jakacki's `TAQOZ.spin2` is still not in the repo, so *"verify vs Jakacki's source"*
  cannot run. What the listing settles is what is in **this ROM build**, which is the stronger
  question for documenting the chip.

## Companions

- `taqoz-rom-dictionary.md` — all 432 ROM words, with the 17 that are commented out.
- `rom-monitor-command-grammar.md` — the Monitor's full command set.
