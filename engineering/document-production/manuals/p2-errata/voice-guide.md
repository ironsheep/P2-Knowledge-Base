# P2 Errata — Voice Guide

**This manual speaks in the Assembly Reference's voice.** That guide is adopted by reference,
not copied: `../p2-assembly-language-manual/voice-guide.md`. Read its §4 (Voice Rules,
including §4.2a *calibrated confidence* and §4.4 *cadence budget*) and §7 (Quality Checklist)
before writing. Where the two guides differ, this one wins, and only in the places below.

The classification terms are adopted from `CLASSIFICATION-GUIDANCE.md`. They are defined once,
in the front matter, and used exactly as defined everywhere else.

---

## 1. What carries over unchanged

- Reference register: third person, definitive, specific. No "you", no "we", no "let's".
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

**Credit without blame.** Parallax published E1 and E2 and is credited for it. E3 to E5 were
predicted by the clean-room design study and confirmed here; the study is credited by name.
No sentence implies the vendor hid anything or that documentation was careless.

**The mechanism in our own words.** *Why it happens* describes behaviour at the programmer's
model: registers, clocks, instructions, what is held and when it is applied. No HDL, no
signal or module names from the design material, no line references.

**Numbers are the evidence.** Give the measured values exactly as the log prints them,
with their units and conditions. Do not round a measured value, and do not state a measured
result as a general law beyond the conditions it was measured under.

## 3. Terms

| Use | Not |
|---|---|
| erratum / errata (only for class 1) | bug (in headings), glitch, quirk, gotcha |
| silicon erratum | hardware bug |
| the part, the chip, the P2 | the silicon (acceptable in *confirmed on silicon*) |
| workaround | fix, patch, hack |
| test program (reader text) · rig (internal) | harness (reader text) |
| confirmed on silicon | verified, validated (for a bench result) |
| the clean-room design study (until its formal name is settled) | the HDL agent, the study agent |

## 4. Headings

Chapter headings are plain reader titles that name the behaviour, not the internal id:
`# Chapter 3: GETCT Returns a Stale Upper Long`. Section headings inside a chapter are the
fixed set in `creation-guide.md` §4, in that order, every time. A reader who has read one
erratum knows where everything is in the next.
