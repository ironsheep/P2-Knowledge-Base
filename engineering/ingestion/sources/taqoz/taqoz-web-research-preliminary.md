# TAQOZ — Preliminary Web Research

**Date captured:** 2026-05-23
**Authority level:** PRELIMINARY / LEADS-ONLY
**Source:** Web research conducted by an external agent against forums.parallax.com
**How to use:** Treat as direction-finding for deeper research, NOT as authoritative facts. Cite the primary sources named below (forum threads, Peter Jakacki's wiki, TAQOZ.spin2 source) before publishing specific claims in deliverable YAMLs.

This file preserves the raw research output verbatim so future agents can re-evaluate it. The companion `taqoz-narrative.txt` extracts the high-confidence facts and flags what still needs primary-source verification.

---

## Research Track 1 — What TAQOZ version is built into the P2 ASIC?

**Original question:** "If you were to look in https://forums.parallax.com/ what can you find about the actual TAQOZ version that was built into the P2 ASIC? I'm looking for the word set, source code, anything you can find."

### Summary

The ROM TAQOZ on shipping P2 silicon is the fixed "TAQOZ V1.0/V1.1" boot‑ROM variant (often referred to as TAQOZ in ROM or TAQOZ BOOT), with a limited, never‑changing word set that's distinct from the later "TAQOZ Reloaded" images you boot from SD/flash.

### Version actually in ROM

In the "Try these TAQOZ code snippets" thread, Peter shows the cold‑start banner from a P2 running the ROM TAQOZ:

```
Parallax P2 .:.:--TAQOZ--:.:. V1.1--v33h 190219-1900.
```

That same thread explicitly says "TAQOZ is an amazing 'tool' that anyone can access on their P2 because it is already built into the ROM," and all the examples there are designed to run on the ROM version, not the SD‑card "Reloaded" version.

So the ASIC mask ROM contains that V1.x build (v33h, 2019‑02‑19), which is finite and unchangeable on any produced P2 chip.

### Where it's documented

The long forum thread "TAQOZ – Tachyon Forth for the P2 BOOT ROM" is the central discussion and includes:
- Design notes about building a cut‑down Tachyon specifically for P2 boot ROM
- Links (now‑stale in places) to "TAQOZ.spin2" and documentation, which were the source bases used to generate the ROM image and the SD‑bootable TAQOZ Reloaded

In the "code snippets" thread Peter points to his SourceForge wiki for TAQOZ/Tachyon, which contains word glossaries and implementation notes, though that's primarily for his maintained builds, not a formal "ROM reference."

In short: the ROM TAQOZ wordset is mostly captured in those two forum threads plus the wiki material they reference.

### Word set in ROM

The ROM TAQOZ is described as having "a limited number of words in the dictionary – which is what you have in the ROM of course," with roughly "100–200 words in Taqoz ROM" compared to many more in the SD‑card versions.

Peter notes that the ROM dictionary has "over 500 active words" during development, but that "the dictionary has a lot of words that would be 'reclaimed' or stripped prior to the final image" to make it fit, so the ASIC version is a pruned subset of his full development environment.

The snippets thread shows concrete examples of ROM‑resident words, such as:
- General: `PIN`, `HZ`, `ms`, `MUTE`, `BACKUP`, `RESTORE`, `AUTO`, `DUMP`
- Memory ops: `@`, `!`, `C@`, `C!`, `W@`, `W!`, `CMOVE`, `FILL`
- Smartpin helpers: `WYPIN`, `WRPIN`, etc.

There is at least one community "Glossary of Words" for TAQOZ Reloaded 2.8 that explicitly covers autostart and SD usage, but you have to allow for differences from the smaller ROM set.

### Source code for the ROM build

In the boot‑ROM development thread, Peter states he is "attempting documentation and full conversion of the higher level Forth source that includes FAT32 so that it can all be integrated into the TAQOZ.spin2 file," and that this file can be loaded directly from PNut.

That same top post links to "Current file TAQOZ.spin2" and "LATEST BINARY and boot files for TAQOZ RELOADED on SD," which were the publicly distributed source and binaries for his maintained builds.

The ROM image itself is mask ROM in the ASIC, not distributed as a separate source tree, but its contents come from that TAQOZ.spin2 base plus the low‑level Tachyon kernel Peter developed; the public TAQOZ.spin2 and related sources on GitHub/SourceForge are the closest available representation of what went into the ROM.

So: you won't find a "this is exactly the ROM TAQOZ source" tag, but TAQOZ.spin2 and Peter's Tachyon/TAQOZ repositories are effectively the same code line with some conditional stripping and compression for mask ROM.

### How to tell you're in ROM TAQOZ

The snippets thread shows the typical entry sequence: connect any serial terminal, send `> ` (greater‑than, space) followed by ESC to enter TAQOZ in ROM after power‑up/reset, then you'll see the `TAQOZ V1.1--v33h 190219-1900` banner.

It also notes that TAQOZ in ROM does not auto‑boot by itself; instead you can `BACKUP` to store your current TAQOZ image into SPI flash at $F0000, and later `RESTORE` or `^R` to reload that image after re‑entering TAQOZ.

This is one of the easiest ways to distinguish the built‑in TAQOZ from any SD‑loaded TAQOZ Reloaded (which usually announces itself as such).

### Key differences vs TAQOZ Reloaded

Peter and others explicitly distinguish "TAQOZ in ROM" (small, fixed, ~100–200 core words) from "TAQOZ RELOADED," which is a larger, updatable system booted from SD that adds VGA, PS/2, extensive file handling, and many more words.

The ROM version is described as "a finite version, one that will never change and is available on any P2," whereas the SD version is meant to be expanded over time.

Functionally, the ROM TAQOZ is focused on hardware bring‑up, smartpin testing, and minimal file/flash tools; Reloaded is meant as a full environment.

---

## Research Track 2 — How to use ROM TAQOZ to boot external code

**Original question:** "How to use P2 ROM TAQOZ to boot external code"

### Summary

You can use the built‑in P2 ROM TAQOZ as a "soft bootloader" by entering TAQOZ from the ROM, then using its SD/flash words (`BOOT`, `BACKUP`, `RESTORE`, `LOAD`, etc.) to fetch and start external binaries or TAQOZ scripts.

### 1. How ROM TAQOZ fits into P2 boot

The P2 mask ROM first tries Chip's standard loaders (serial, QSPI flash, SD) and only drops into TAQOZ if those fail, or when you explicitly enter it via the serial‑escape sequence.

TAQOZ itself resides in mask ROM but is copied to hub RAM to run, and then gives you a Forth console with SD and flash utilities intended specifically for loading external code.

So you can deliberately "fall into" TAQOZ on a blank system and use it as a boot monitor.

### 2. Entering ROM TAQOZ from a terminal

Typical sequence from a USB‑serial terminal (115200 8N1 is common; check your board defaults):

1. Power up or reset the P2
2. Within the early boot window, send: `>` followed by a space, then ESC (0x1B) – this is the documented "enter TAQOZ" trick
3. TAQOZ will respond with a banner similar to: `Parallax P2 .:.:--TAQOZ--:.:. V1.1--v33h 190219-1900.`
4. At this point you're talking to ROM TAQOZ and can execute its boot‑helper words

### 3. Using TAQOZ to load and boot a binary

The ROM TAQOZ has file and raw‑sector support sufficient to:
- Read sectors from SD
- Access FAT32 files
- Copy images to/from SPI flash

The usual pattern to boot non‑TAQOZ code is:

**Prepare a binary**
- Build your PASM2/Spin2/C code as a normal P2 binary image targeting hub address 0 (what you'd normally load with PNut or loadp2)
- Place this binary on an SD card in a known location (often in the root directory, sometimes with a specific filename your TAQOZ script expects)

**Write a TAQOZ loader word (once, then reuse)**
Conceptually, your Forth definition will:
- Open the binary file (or point to raw sectors)
- Read its contents into hub RAM at address 0
- Start execution at 0 with a TAQOZ word that jumps to hub address 0

The forum thread emphasizes that TAQOZ "allows booting from raw SD sectors but also by FAT32 name," which is exactly the mechanism you're exploiting.

**Execute the loader from the TAQOZ prompt**
- Insert the SD card
- From the TAQOZ console, run your loader word, which loads the binary and jumps to it

Because the ROM word set includes memory, block‑move, and smartpin helpers, the missing piece is just a small loader definition tying SD file reads to hub RAM and then doing the jump.

### 4. Using BACKUP/RESTORE as a boot mechanism

TAQOZ also has built‑in flash‑helper words that you can co‑opt for booting:

Peter notes that TAQOZ will include "serial Flash utilities as well so that Flash can be saved or loaded from a file or serially etc." in the ROM‑based system.

The typical flow is:
1. Develop your TAQOZ‑based application or loader in RAM from the console
2. Use `BACKUP` to store the current TAQOZ image plus your definitions into SPI flash at a fixed offset (Parallax docs and forum posts commonly mention a dedicated TAQOZ region)
3. On power‑up, arrange (via your early boot conditions or a small script) to:
   - Enter TAQOZ from ROM
   - Use `RESTORE` (or a shorthand, often `^R` mentioned in TAQOZ examples) to pull that stored image back into RAM and run it

If the stored image consists primarily of "load binary from SD, then jump," your ROM TAQOZ is effectively a multi‑stage bootloader: ROM TAQOZ → flash TAQOZ image → your binary.

### 5. Booting TAQOZ scripts that then launch other code

Another approach is two‑step:
- Use ROM TAQOZ to boot a TAQOZ script or extended TAQOZ image from SD (TAQOZ Reloaded or a cut‑down variant). The boot‑ROM thread explicitly mentions using TAQOZ to "boot binaries from FAT32 files, load TAQOZ source code which could be the assembler/disassembler etc."
- Let that loaded TAQOZ system provide richer tools or a more convenient loader environment, then jump into your PASM2/Spin2 application from there

This is especially handy if you want to keep your low‑level boot very simple and then have a more full‑featured "OS‑ish" environment do the rest.

### 6. Practical tips and caveats

**ROM TAQOZ uses hub RAM**
Peter confirms TAQOZ in ROM is copied into hub RAM and uses buffers and dictionary space, so it doesn't leave hub 0..N completely untouched.

For a pure "load binary at 0 and jump" pattern, just be aware you're replacing TAQOZ; that's fine for a bootloader, but you don't get TAQOZ afterwards unless you architect coexistence yourself.

**SD constraints**
- The ROM TAQOZ SD/FAT32 layer targets standard SD cards with FAT32 (not exFAT)
- MBR/FAT32 access is designed as a robust, failsafe boot path from SD up to large card sizes

**Where to find concrete loader examples**
- The "TAQOZ – Tachyon Forth for the P2 BOOT ROM" thread explicitly mentions using TAQOZ to "boot binaries from FAT32 files" and to interact with files almost like DOS/BATCH; many of the code examples there can be adapted into a binary loader word
- Later TAQOZ Reloaded documentation and examples include file‑load words that are very similar to what the ROM version uses, so you can borrow structure from those when writing your own loader

---

## Primary sources named — chase order for verification

These are the authoritative sources this research pointed at. Anything we want to PUBLISH as fact in the YAML KB should be traced to one of these:

1. **Forum thread**: "TAQOZ – Tachyon Forth for the P2 BOOT ROM" (forums.parallax.com)
   - Central thread, design notes, links to TAQOZ.spin2 source
   - Has the BOOT/BACKUP/RESTORE word documentation
2. **Forum thread**: "Try these TAQOZ code snippets" (forums.parallax.com)
   - Where the V1.1 banner string is quoted
   - Concrete word examples
3. **TAQOZ.spin2** — Peter Jakacki's public source
   - Linked from the forum threads (URLs noted as "stale in places")
   - Closest available representation of what went into mask ROM
4. **Peter Jakacki's SourceForge wiki** for TAQOZ/Tachyon
   - Word glossaries and implementation notes for his maintained builds
5. **TAQOZ Reloaded 2.8 Glossary of Words** (community-maintained)
   - Comprehensive, BUT includes Reloaded-only words; needs filtering for ROM-only subset

## Items needing primary-source verification before publishing

| Claim | Confidence from this research | Verification needed |
|-------|------------------------------|---------------------|
| ROM banner: `Parallax P2 .:.:--TAQOZ--:.:. V1.1--v33h 190219-1900.` | HIGH (quoted from forum) | Direct forum citation; ideally also verify by booting a P2 |
| Build date: 2019-02-19 | HIGH (derived from banner) | Same as above |
| ~100-200 words in ROM | MEDIUM | Count from actual ROM dictionary extraction (could mine from ROM_Booter.lst) |
| BACKUP target address $F0000 | MEDIUM | Verify in TAQOZ.spin2 source or by experiment |
| Specific word list (PIN/HZ/ms/MUTE/etc.) | MEDIUM | Filter from TAQOZ.spin2; verify each is in ROM build |
| SD card layer = FAT32 only (no exFAT) | MEDIUM | Verify in forum thread |
| Entry sequence: `> ` + ESC | HIGH (matches Silicon Doc + Datasheet — primary source agreement) | Already cross-verified |
| ROM TAQOZ is copied to hub RAM to run | MEDIUM-HIGH (Peter's statement) | Confirm in TAQOZ.spin2 / ROM_Booter.lst |
| ROM TAQOZ does not auto-boot | MEDIUM | Verify in forum |
| Entry only after power-up / before autorun | HIGH (matches Silicon Doc) | Already cross-verified |

## Follow-up research suggestions (from agent)

1. Build a complete TAQOZ word-set reference guide for the P2 ROM version, extracted from forum glossaries and source discussions
2. Create a P2 TAQOZ vs. full SD-loaded version comparison report, detailing the ROM's fixed word-set limits and advanced driver support
3. How to use P2 ROM TAQOZ to boot external code
4. Difference between Tachyon Forth and TAQOZ on P2
5. Accessing P2 hardware registers via TAQOZ console
