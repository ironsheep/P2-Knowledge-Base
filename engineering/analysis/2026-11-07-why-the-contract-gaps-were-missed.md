# Why our process missed the contract gaps

**Head:** `yaml:p2kb` · **Written:** 2026-11-07 · **Kind:** analysis (no ship commitment)

**Question (Stephen, 2026-11-07):** *"If you look at the things that are missing based on what this plan
is identifying, can you identify any crucial something in our process that caused us to miss all of
these things? Is there something we should have done differently to not have these gaps?"*

**Input:** `engineering/planning/P2KB-CONTRACT-GAPS-SPRINT-PLAN.md` (the gaps), measured against git
history and our own process records. Every number below has its command at the end.

---

## The short answer

There are two process faults, and the second makes the first invisible.

1. **We only ever check what moves.** Each check we run is triggered by an edit, a release delta, a
   reported finding, or a manual that happens to cover the page. None of them is triggered just because
   content exists. The text written in the founding weeks (August and September 2025) was never read
   whole against its source, and it is still 34% of what we serve.
2. **We measure what we wrote, never what a reader needs.** Ingestion counts how much of a source we
   extracted, not how much of it reached the KB. No list exists of the questions a programmer must be
   able to answer. When the KB says nothing on a point, that looks exactly like having nothing to say.

Chip found these gaps because a simulator is a consumer: to implement an instruction, you have to answer
every question about it. We had no consumer anywhere in our loop.

---

## The gaps, sorted by what would have caught them

| Class | Count in the plan | Examples | What would have caught it |
|---|---|---|---|
| A. Served wrong while a source says otherwise | 15 | COGINIT D layout, hub alignment, debug area, BRK bit order, RD/WR timing, XBYTE flags, GETRND "cryptographic" | Reading the page against its source |
| B. Served with no source behind it | 3, plus 1 source conflict | CORDIC "stall when full", COGINIT resets, REP and `_RET_`; TRGINT under STALLI | The same read, which finds the missing citation |
| C. A source says it but the KB doesn't | about 18 | ALTI codes, PTR encoding, Q's life, the pixel mixer table, event clearing, GETBRK codes, smart pin reset values | A map from each source section to where the KB carries it |
| D. The KB says it but readers can't reach it | 2 pages, 62 missing links | Interrupt and pin timing pages: no aliases, no inbound links | Asking the KB a reader's question |
| E. No source says it anywhere | 3 compile proofs, 15 bench arms | Branch offset units, CALLD far field, what COGINIT resets | A list of the questions a programmer must answer, so the silence shows |

Classes A and B come from fault 1. Classes C, D and E come from fault 2.

---

## Fault 1: we only check what moves

**Where the defects came from.** I blamed the served line for 12 of the class A and B defects:

| Defect line | Written | Since then |
|---|---|---|
| `cog.yaml:201` COGINIT layout, `hub.yaml:70,107,236`, `xbyte_engine.yaml:42`, `cordic.yaml:142` | 2025-09-06, commit `6d917664` (15 architecture files, 4,280 lines in one commit, *"comprehensive extraction from both Silicon Doc v35 and P2 Datasheet"*) | Never changed |
| `complete-system-registers-index.yaml:145` | 2025-09-06, `2164a9fe`, KB v1.0.0 | Never changed |
| `smart-pin-11110-…:20` async TX IN | 2025-11-10, a "rich, concise YAML content" rewrite | Never changed |
| `getrnd.yaml:12` "for security/crypto" | 2026-01-24, an enrichment pass. The source it names, the pnut_ts guide, says nothing like it | Never changed |
| `brk.yaml:12`, `rcr.yaml:28`, `cog_hub_execution.yaml:83` | Touched by later fixes, each to repair something else on the same page | The wrong text sat beside the repaired text |

Seven of the twelve date from the founding week, and four of those are in a single commit.

**These pages were edited many times without ever being read whole.** Those founding pages have had
10 to 17 commits each since, and most of their text is still the founding text: `hub.yaml` 208 of 281
lines, `cog.yaml` 221 of 284, `xbyte_engine.yaml` 216 of 339. Each later edit was checked as a hunk.
Across the tree, **391 of 921 pages** are still more than half founding text, and **27,227 of 79,865
served lines** (34%) date from August or September 2025.

**Why none of our checks reached them.** Each check has a trigger, and none of those triggers fires on
content that already exists:

| Check | Fires on | Why it missed these |
|---|---|---|
| Change-set audit (`release-yamls` §1.5, since 2026-10-08) | Lines changed in the release | The founding lines never changed |
| Claim-sourcing audit | Quantities with no citation in a file that cites elsewhere | Tier 2, "uncited file", is advisory because *"the population is large and mostly historical"*, so we knew about the unaudited base and chose not to gate it. And it checks that a citation exists, not that it supports the claim |
| Constant fidelity | Named constants | Most of these defects name none |
| Code compile gate | Code blocks | Legality only, so prose isn't touched |
| Manual audits | Pages a manual draws on | See the next paragraph |
| Correction sweeps (2026-06-10 onward) | Register findings | A finding has to be reported first |

**Manual audits are not a backstop for YAML errors, by design.** The trust chain runs from sources to
YAML to documents: the YAML is the bible, and manuals are made from it. So a manual audit's job is to
confirm the manual says what the YAML says, and a YAML error correctly passes into a manual and through
its audit. The plan's §13 shows three cases: BRK's bit order in the Assembly manual, the TRGINT wording,
and the XBYTE flags in the XBYTE guide. When manual audits did find YAML defects (most of F-026 to F-097
came from the Assembly manual audit), that was a by-product: the manual's writer had gone to the Silicon
Doc. The design puts the whole burden of truth on the step that makes the YAML, which is ingestion and
its audit, and that step never read the founding YAML against its sources. *(Corrected 2026-11-07 after
Stephen's review: an earlier draft proposed that manual audits stop treating the YAML as a source. That
would break the design; the fix belongs upstream.)*

**What we should have done.** When we adopted write-time verification (2026-01-23) and later the
change-set audit (2026-10-08), we should have run one baseline pass. That means reading every inherited
page whole against its sources, or at least marking the inherited set as *unaudited* and working it down
as a tracked backlog. Auditing only the delta is sound only if the base was audited once, and ours never
was.

---

## Fault 2: we measure what we wrote, not what a reader needs

**Ingestion stops at extraction.** The ingestion work mode's completeness assessment asks whether the
document's text was extracted, and its catalogue step raises a *"knowledge coverage percentage"*.
Nothing in either step records where each source section ended up in the KB. The Silicon Doc's
extraction audit never mentions the YAML at all. So the ALTI control codes, the PTR expression layout,
Table 13 and the event-clearing rules were all extracted correctly and are all sitting in our sources,
but no ledger shows that no page carries them. That is class C.

**The KB's shape had no place for these facts.** `language/pasm2/` holds 382 instruction pages and 18
concept pages. An instruction page is a natural home for a fact about that instruction. Most of the
plan's additions are not about one instruction:

- state that spans instructions: Q, pending AUGS and ALTx, the skip pattern, REP;
- tables that several instructions share: the pixel mixer, event clearing, PTR encoding;
- rules that depend on the form: branch units.

The Silicon Doc states these in prose sections, not in the instruction CSV that seeded the pages, so they
had nowhere to land. This is why the plan has to add `cog_state.yaml`, `pixel_mixer.yaml` and new blocks,
and why only 4 of 47 S-branch pages carry the units line. This part is an inference from the structure
and the counts: I found no record of a decision to leave these facts out.

**Our probes check what we changed.** Even the MCP before-and-after test of 2026-10-11 was a set of
probes predicted from that release's changes (P1 to P7). None of our tests asks the KB a question a
programmer would ask and checks whether it can be answered. That is how class D survived: 0 of 22
interrupt-control pages link the interrupt page, and `p2kb_find latency` returns nothing, yet every
cross-reference gate reads 100%. Our gates check that the links we have resolve, not that the links
readers need exist.

**Silence and coverage look the same.** The KB has no habit of saying "not documented". Where no source
speaks (class E), the KB said nothing, and an absent sentence raises no flag in any gate. Chip's document
is mostly a list of such silences, which his simulator forced him to name.

**What we should have done.**

- Make carriage part of ingestion's definition of done: a per-section ledger for each primary source,
  recording each section's KB home or *"not carried, because…"*.
- Keep a contract question list per area, the questions a programmer must answer to write correct code.
  Run a periodic "answer from the KB only" probe against it. Every question that can't be answered
  becomes a gap, a "not documented" statement, or a bench candidate.
- Design the cross-cutting pages (cog state, shared tables, units by form) from the start, so the
  instruction page isn't the only container.

---

## What this means for the sprint

The sprint plan fixes the instances. Without changes to the process, the same classes will regrow: the
other 391 founding pages haven't been read either, and the same fault would hide the next source's
uncarried sections. In rough order of value, the process changes are:

1. **A baseline read of the founding pages,** worked down from the most-served architecture pages,
   using the same four questions as the change-set audit applied to whole pages. The plan's §12 held item
   (making the whole-page read a gate on changed pages) is the forward half of this; the baseline is the
   backward half.
2. **A carriage ledger for the Silicon Doc,** since it is the source behind most of class C, then for
   the datasheet and the CSV.
3. **The contract question list and the KB-only probe,** seeded from Chip's document, which is already
   such a list for the architecture.

Manual audits stay as they are: they check a manual against the YAML, which is their job. Changes 1 and
2 make the YAML worth checking against.

Which of these join this sprint, and which become their own sprint, is a scope decision for Stephen.
Each is a process change, so none is offered as optional.

---

## Commands behind the numbers

- Origins: `git blame -L <line>,<line> --porcelain <file>` then `git log -1 <sha>`, for the 12 lines in
  the table; `git show --stat 6d917664`.
- Founding share per page: `git blame --date=short <file> | grep -c ' 2025-09-0'`, against `wc -l`.
- Tree-wide: over `find architecture language -name '*.yaml'` under `deliverables/ai/P2/`, counting blame
  lines dated `2025-0[89]-`: 921 files, 391 with more than half, 27,227 of 79,865 lines (2026-11-07).
- Page shape: `ls language/pasm2/*.yaml | wc -l` gives 382; `ls language/pasm2/concepts/*.yaml | wc -l`
  gives 18.
- Claim-sourcing scope: `audit-yaml-claim-sourcing.py` header (Tier 2 rationale) and run tail ("A clean
  run means NOT CAUGHT BY THESE CHECKS").
- Ingestion: `engineering/ingestion/work-modes/document-ingestion-focused.md:290-325`; no YAML mention in
  `silicon-doc-complete-extraction-audit.md` (`grep -i yaml`).
- Sweep triggers: `ls engineering/operations/correction-sweeps/`, where every entry is a register archive,
  a change-set audit, or a finding-driven sweep.
