# Capitalization & Terminology Standard (P2 Manuals)

*The authoritative capitalization rule table for recurring P2/Propeller terms in our
reader-facing manuals. **Derived empirically from the formal Parallax corpus** — this is
Parallax's own discipline observed across their P1+P2 documents, not a house style we
invented. Adopt their **discipline**, not their one-off lapses.*

**Status:** Research deliverable for the doc-style-change sprint, Element 2 (Capitalization
discipline). This table is the authority the cross-manual sweep applies.
**Date:** 2026-06-23
**Trust chain:** Formal Parallax docs (documentary) → this rule table → manual sweep.

---

## Sources surveyed (faithful raw-text extractions, author casing preserved)

| Authority | File | Role |
|---|---|---|
| **Parallax Propeller 2 Documentation v35 (Rev B/C "Silicon Doc")** — Chip Gracey | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (13,016 lines) | P2 architecture — primary |
| **Parallax Spin2 Documentation v55** — Chip Gracey | `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` (1,740 lines) | Spin2 language — primary |
| **Parallax Propeller 1 Manual v1.2** | `engineering/ingestion/sources/p1-propeller-manual-v1.2/p1-propeller-manual-v1.2-layout-text.txt` (14,574 lines) | P1 precedent for shared terms |

Method: for each recurring term, every occurrence was classified as **prose mid-sentence**
(the only decision-relevant class), start-of-sentence (forced cap — ignored), heading/label
(excluded), or code/mnemonic (excluded). Capitalized-vs-lowercase tallies are over prose
mid-sentence occurrences only.

---

## The headline rule

> **Generic P2/Propeller component nouns are written LOWERCASE in prose.** Chip Gracey does
> **not** title-case component names mid-sentence — "Smart Pin", "Cog", "Hub", "Streamer"
> appear capitalized **only** in section headings, table/label cells, numbered instances
> ("Cog 0"), and at the start of a sentence. Capitalize a term in prose only when it is a
> **true acronym**, a **proper noun**, a **product/language name**, or part of a **named
> proper compound** (a named register/region/block).

This is the same discipline that already gave us "cog, not CPU" (lowercase, P1-precedented).

---

## Rule table

### A. Lowercase in prose — generic component / language nouns

| Term | Prose form | Evidence (prose cap : lower) | Notes |
|---|---|---|---|
| cog / cogs | **cog** | Silicon ~0:302 · Spin2 ~0:50+ · P1 ~0:463 | Cap only in headings, "Cog 0..7", "cog RAM" region label. Decisive across all three. |
| hub | **hub** | Silicon ~0:190 · Spin2 ~0:40+ · P1 **53:74 (split)** | **DECISION below** — P2 corpus is uniformly lowercase; follow it. |
| smart pin / smart pins | **smart pin** (two lowercase words) | Silicon ~0:70 · Spin2 0:12 | NOT "Smart Pin" (headings/symbol-tables only), NOT "smartpin". Hyphenated "smart-pin" only adjectivally. |
| pin / pins | **pin** | Silicon ~3:403 · Spin2 — · P1 41:64 | Cap "Pin" = syntax-field name / table header only. |
| streamer | **streamer** | Silicon 0:70 · Spin2 0:10 | Cap = headings / "Event N = Streamer…" labels / sentence-start. |
| hub exec / cog exec | **hub-exec**, **cog-exec** (lowercase) | Silicon 0:1 (space) · Spin2 0:9 (hyphen) | **DECISION below** — prefer Spin2's hyphenated form when adjectival. |
| lock / locks | **lock** | Silicon ~0:49 · P1 20:130 | Common-noun = lowercase. **`LOCK[n]` uppercase only as the register/resource notation or Spin2 mnemonic** (Spin2 v55 writes `LOCK[15]`). |
| event / events | **event** | Silicon 0:144 · Spin2 0:6 | Cap = headings / "Event N =" labels. |
| interrupt / interrupts | **interrupt** | Silicon 0:116 · Spin2 0:20 | Uniform. |
| flag / flags | **flag** | Silicon ~0:102 · Spin2 0:6 · P1 7:20 | "C flag", "C and Z flags". |
| register / registers | **register** | Silicon ~0:229 · Spin2 ~0:35+ · P1 91:351 | Cap only for **named** registers ("Direction Register", "DIRA"). |
| bytecode / bytecodes | **bytecode** | Silicon 0:52 · Spin2 0:12 | Cap = ALL-CAPS headings / code comments only. |
| method / methods | **method** | Spin2 0:30+ · P1 11:217 | Cap = "Public/Private Method Block" named-block only. |
| object / objects | **object** | Spin2 0:30+ · P1 24:161 | Cap = "Object Block" / "Object Exchange" proper names only. |
| operator / operators | **operator** | Spin2 0:12 | Uniform. |
| egg beater | **egg beater** (lowercase) | heading-only in all sources | **EDITORIAL — see decisions.** Silicon shows only `THE "EGG BEATER" INTERFACE` (quoted heading). No prose precedent; lowercase chosen for consistency. |

### B. Always ALL-CAPS in prose — true acronyms

`LUT` `CORDIC` `FIFO` `DAC` `ADC` `PLL` `NCO` `RAM` `ROM` `PWM`

- Uniform across the corpus; the only lowercase hits are inside code comments (excluded).
- **Plural convention: caps acronym + lowercase `s`** → **DACs, ADCs, RAMs, LUTs, PLLs, NCOs, FIFOs** — never "DACS".
- **Compounds follow each word's own rule**: **hub RAM**, **cog RAM**, **LUT RAM** (lowercase
  descriptor + all-caps acronym). (P1 wrote "Cog RAM"/"Main RAM" as proper named regions; the
  P2 corpus uses the lowercase-descriptor form — follow P2.)

### C. Always capitalized in prose — proper nouns & product/language names

| Term | Form | Note |
|---|---|---|
| Goertzel | **Goertzel** | Proper noun (mathematician). Silicon 22:0. Its own category — not an acronym, not a common noun. |
| Spin2 | **Spin2** | Cap "S", lowercase "pin", digit "2". Silicon/Spin2 prose 125×. Lowercase "spin2" is only the `.spin2` file extension. |
| Propeller 2 / P2, Parallax | **Propeller 2 / P2, Parallax** | Product / company proper names. |

---

## Resolved decisions (confirmed by Stephen, 2026-06-23)

These were the points where the corpus is split or diverges from our house usage. Per the
Element 2 method: where the corpus is internally inconsistent, pick the **dominant + most
readable** form and **document the choice + its source** — do not follow a one-off lapse.
**All four below are CONFIRMED** and are now binding rules for the sweep.

1. **`hub` — lowercase, always (CONFIRMED).**
   The P2 authorities (Silicon Doc + Spin2 v55, *both Chip Gracey*) write **lowercase "hub"
   uniformly**, including the subsystem-as-entity sense. The P1 Manual is the lone outlier:
   it capitalizes **"Hub"** for the standalone subsystem ("the **Hub** controls…") while
   keeping lowercase **"hub"** as a modifier ("hub instruction"). Resolution: these are **P2
   manuals**, the P2 corpus is the governing authority, and its dominant form is lowercase —
   which is also more readable and consistent with our lowercase-"cog" rule. **→ lowercase
   "hub" everywhere in prose.** (P1's "Hub" entity-cap is a P1-era convention Chip did not
   carry into the P2 docs.) **Confirmed: hub is treated like cog.**

2. **`PASM2` vs `PASM` — divergence from source; KEEP "PASM2".**
   The formal Parallax docs write bare **"PASM"** (Spin2 v55: 82× "PASM", **0×** "PASM2";
   Silicon Doc likewise). But our house convention and our published manual title use
   **"PASM2"** — the community disambiguator (PASM = P1, PASM2 = P2). The source's bare "PASM"
   predates the need to distinguish from P1. **Confirmed: keep "PASM2"** as the P2-era
   term; it matches "P2 Assembly Language PASM2 Manual" and community usage. This is the one
   place we deliberately diverge from the source.

3. **`hub-exec` / `cog-exec` — hyphenation form (CONFIRMED).**
   Both are lowercase. Silicon writes "hub exec" (space, 1×); Spin2 v55 writes
   "hub-exec"/"cog-exec" (hyphen, 9×) adjectivally. **Confirmed: hyphenated when
   adjectival** ("hub-exec code"), the dominant Spin2 form.

4. **`egg beater` — editorial, no prose precedent (CONFIRMED).**
   Appears only as the quoted heading `THE "EGG BEATER" INTERFACE` in the Silicon Doc; no
   mid-sentence prose anywhere. **Confirmed: lowercase "egg beater"** in prose, for
   consistency with the lowercase-common-noun convention.

---

## The 3-bucket sweep (how the sweep applies this table)

1. **DE-CAP** habitual prose capitals on Section-A terms: cog, hub, smart pin, pin, streamer,
   lock, event, interrupt, flag, register, bytecode, method, object, operator, hub-exec, egg
   beater. (Leave headings, table/label cells, named registers, numbered instances, and
   sentence-initial caps alone.)
2. **KEEP** product/language/proper names: Spin2, PASM2, Propeller 2, P2, Parallax, Goertzel.
3. **KEEP** true acronyms & code mnemonics: LUT, CORDIC, FIFO, DAC, ADC, PLL, NCO, RAM, ROM,
   PWM, and all instruction mnemonics / register names verbatim.

**De-ritualization goal governs:** de-cap habitual prose caps; Spin2/PASM2 are
case-insensitive, so descriptive phrases like "hub exec" are not Capitalized as if proper nouns.

---

## No internal inconsistency hidden here

Across all three documents, every capitalized appearance of a Section-A term traced cleanly to
(a) sentence-initial position, (b) a section heading, (c) a table column-header / label cell,
(d) a numbered instance, or (e) a named proper compound — **never** a genuine mid-sentence
prose split. The lowercase-in-prose convention is the authors' consistent discipline, not an
average over noise.
