# P2 Errata — Voice Guide

**This manual speaks in the Assembly Reference's voice.** That guide is adopted by reference,
not copied: `../p2-assembly-language-manual/voice-guide.md`. Read its §4 (Voice Rules,
including §4.2a *calibrated confidence* and §4.4 *cadence budget*) and §7 (Quality Checklist)
before writing. Where the two guides differ, this one wins, and only in the places below.

The classification terms are adopted from `CLASSIFICATION-GUIDANCE.md`. They are defined once,
in the front matter, and used exactly as defined everywhere else.

---

## 1. What carries over unchanged

- Reference register: third person, definitive, specific. No "we", no "let's". "You" only
  where §2a allows it.
- No vague hedging; **calibrated qualifiers are required** where the evidence is partial.
- No marketing, no reassurance that the hardware is correct, no reader-as-foil, no
  self-admiration, no staged reveal.
- State each fact once.
- "cog" lowercase in prose (capital only at the start of a sentence).

## 2. What is particular to an errata manual

**Report the defect; never dramatize it.** An erratum is a fact about a part, not a scandal.
Not "a dangerous bug", "silently corrupts", "a nasty surprise". Instead: what happens, when,
and to what. Severity is shown by the symptom, not asserted by adjectives.

**Keep proof separate from prediction.** Say *confirmed on silicon* only for what a bench run
decided. What the bench did not test stays qualified: *"only `ALTD` was tested as the
intervening instruction; Parallax names `AUGS` and `AUGD` as well."* The evidence sets the
strength of the sentence.

**"Found so far", never "all".** The list is open-ended. No "the complete list of P2 errata",
no "every silicon bug".

**Credit without blame.** Parallax published E1 and E2 and is credited for it. E3 to E6 were
predicted by the clean-room design study and confirmed here; the study is credited by name.
E7 was found on the bench here, by a test built to measure something else; it was not
predicted.
No sentence implies the vendor hid anything or that documentation was careless.

**The mechanism in our own words.** *Why it happens* describes behaviour at the programmer's
model: registers, clocks, instructions, what is held and when it is applied. No HDL, no
signal or module names from the design material, no line references.

**Lead with what the reader must do.** The reader opened this manual to find out whether an
erratum touches their program and what to change. The CAUTION box at the top of every erratum
answers that in three lines; everything after it is the evidence for those lines. An opening
paragraph follows the box, it does not restate it. Name whose statement the part contradicts
(*the P2 Documentation states*), never an unowned "the design".

**A workaround, not a fix; one, not the only one.** The part keeps its defect; the reader's
code steps around it. A *fix* is what a new silicon revision does, so this manual never calls
the reader's change a fix (Stephen, 2026-09-26: "We can't possibly be offering the only fix").
Section *A proven workaround* is **rule-first**: it opens with the condition any workaround
must meet (*What any workaround must do: …*), then *One way, proven on P2 hardware:* and the
code block a reader pastes, byte-identical to a block a test program ran on silicon, then one
sentence saying what it guarantees and its kind — a *one-time startup workaround*, a *rule at
each use*, or a *helper routine*. Where other ways meet the same condition, say so (E3: any cog
the program already keeps running in 4-7 does what the keeper does). A block that has not run
on a part is not printed as the proven workaround.

## 2a. The voice boundary: where "you" is allowed

The reader-facing parts of an erratum speak to the reader; the evidence speaks in the reference
voice. The line is fixed by section:

| Section | Voice |
|---|---|
| CAUTION box | "you" allowed |
| Section headings (*What your program sees*, *A proven workaround*) | "you" / "your" allowed |
| Opening paragraph | reference voice |
| *What the P2 is documented to do* · *What the P2 does* | reference voice |
| *What your program sees* | "you" allowed |
| *A proven workaround* | "you" allowed |
| *Why it happens* · *How it was proven on P2 hardware* · *The test program* · *Status* | reference voice, no "you" |

"You" is the programmer at their bench, never a foil: no "you might think", no "as you can
see", no "you'll be surprised". "We" is never used; the test was run *here*, or *on the bench*.

**Numbers are the evidence.** Give the measured values exactly as the log prints them,
with their units and conditions. Do not round a measured value, and do not state a measured
result as a general law beyond the conditions it was measured under.

**No qualifier that carries no weight** (Stephen, 2026-09-26: *"Qualifying words that carry
no weight are of no benefit to us."*). Test each qualifier by deleting it: if the sentence's
truth does not change, it goes. *On a real P2* implies an unreal one — it is *on P2 hardware*;
*what the P2 actually does* is *what the P2 does*; *the very next instruction* is *the next
instruction*. Kept, because they change the claim: *exactly* (a measured exact equality),
*directly / immediately before* (instruction position), *just after* (timing), *explicitly*
(written by the programmer, not generated by the assembler), *correctly* (a right read versus a
wrong one).

## 3. Terms

| Use | Not |
|---|---|
| erratum / errata (only for class 1) | bug (in headings), glitch, quirk, gotcha |
| silicon erratum | hardware bug |
| the part, the chip, the P2; *P2 hardware* for where a test ran | the silicon (acceptable in *confirmed on silicon*); *real P2*, *real part*, *real chip*, *real silicon* |
| workaround (the reader's code change; heading *A proven workaround*; *proven* only when it ran on a part) | fix (a fix is a silicon revision), patch, hack; *the* workaround (there may be others) |
| test program (reader text) · rig (internal) | harness (reader text) |
| confirmed on silicon | verified, validated (for a bench result) |
| the clean-room design study (until its formal name is settled) | the HDL agent, the study agent |

## 4. Headings

Chapter headings carry the erratum number and a plain reader title that names the behaviour,
not the internal id: `# Erratum E3: GETCT Returns a Stale Upper Long`. Section headings inside a chapter are the
fixed set in `creation-guide.md` §4, in that order, every time. A reader who has read one
erratum knows where everything is in the next.
