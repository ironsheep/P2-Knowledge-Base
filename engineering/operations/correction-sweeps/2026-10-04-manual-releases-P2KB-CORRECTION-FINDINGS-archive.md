# P2KB Correction Findings — ARCHIVE, swept 2026-10-04 (after the two manual releases)

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 2 findings carrying a `DONE` status token: F-524 (released in the Architect's Guide
> v1.1.1) and F-521 (its YAML half served in KB v1.23.0, its document half released in P2AN007
> v1.0.2), both verified on the released PDFs on 2026-10-04. The second sweep of the day, so it has
> its own file (`2026-10-04-P2KB-CORRECTION-FINDINGS-archive.md` holds the first and is never re-edited).
>
> Swept by rename-then-trim: the register was `git mv`'d here and copied back; this copy was cut to
> the 2 findings plus one live line they made stale (kept here verbatim; rewritten in the live file),
> and the live copy had the same text removed with the edit tools. Every line below is the pre-sweep
> text (commit d722a093), verbatim; `audit-register-hygiene.py --sweep-check d722a093` proves it.

---

### F-524 — the Architect's Guide says a latest-wins mailbox makes a torn read impossible without a lock — `DONE` (released in v1.1.1, 2026-10-04, verified on the PDF: pages 21, 22, 33, 59)
> **Applied 2026-10-03 («#377»).** Step 6 (:918-927) now states the handshake: the orchestrator posts again only after motion has copied and acknowledged; bump-last alone does not prevent a torn read. **Widened in the same file:** the contract list (:427-429) described the latest-wins mailbox as "a single slot where the producer never waits … (decoupled completely)" — the same disproven claim one level up; now the producer waits only for the consumer's copy, and a one-long command needs no wait (EF-038, EF-037). Step 6's "Nothing blocks anywhere" became "Nothing waits on a slow partner". Swept the rest of the guide for mailbox/never-blocks wording: the sensor "last posted value … never blocks" (:442) is the reader side and stays. **Widened again 2026-10-04 («#378» impact audit), after the first build:** the Force 2 "publish-last" passage (:486-492, "a reader that watches that counter can never catch a torn, half-written value") and the glossary's Publish-last entry made the same claim for any multi-field update — now both require the reader's hand-back (acknowledgement or ring tail) before the next write; :731 and :955 name the discipline and read correctly with it. The first sweep grepped "torn read" and missed "torn, half-written value". Re-staged; the built PDF predates this.
`manuals/p2-architect-guide/opus-master/architect-guide-body.md:919`: "sequence counter bumped
last, so a torn read is impossible without a lock." The bench disproved it (EF-038): bump-last
guards only the first publish; with a reader that does any work between reading the command and its
arguments, a writer that does not wait for the ack tore 20,000 of 20,000 commands. The KB carried
the same sentence and was corrected in v1.23.0 (F-507). **Fix:** state the handshake — the writer
posts only when ack == seq, the reader copies every argument before acknowledging — at the
Architect's Guide's next release.

F-506…F-520 and F-522 shipped in v1.23.0 and are archived; F-521 (its P2AN007 half) and F-523 stay open.

### F-521 — p2an007 offers "re-check the sequence after copying" as a safe non-blocking mailbox; with a bump-last writer it is not — `DONE` (YAML half served in v1.23.0; P2AN007 document half released in v1.0.2, 2026-10-04, verified on the PDF: pages 7-8 and 14)
> **Applied to the document 2026-10-03 («#377»).** R3 Pitfall: the re-check option replaced by why it is unsafe with this writer (KB YAML :131 wording); the Tip's "extends naturally to the non-blocking re-check above" removed. **Widened:** "How this works" said the worker would run the newest "if the writer overwrote `cmd` twice before the worker looked" — the R3 code waits for the ack and cannot do that; now "each post replaces the last … the writer posts only after the ack". Example code unchanged. **Widened 2026-10-04 («#378»):** R3's "Use it when" said "Old unread commands should be overwritten, not queued" (the handshake forbids exactly that) → "Commands are replaced, not queued … with the worker's acknowledgement handing the slot back"; the publish-last pitfall now adds that the writer must not rewrite the fields until the reader has copied them (R2's tail, R3's ack). Re-staged; the built PDF predates this.
Found 2026-10-03 while fixing F-507. `application-notes/p2an007-data-structures-new-facilities.yaml:131`
and the P2AN007 document (`app-notes/P2AN007/opus-master/P2AN007.md:214`, R3 pitfall; the Tip below it
repeats it) give two "honest options" for a writer that never waits: pack the payload into one long
(R5, measured, EF-037), or have the reader read seq, copy the record, re-read seq and retry if it moved.
**The second does not work with this recipe's writer.** The writer bumps seq only AFTER writing the
fields, so while it is mid-write the reader reads the old seq, copies half-new fields, and re-reads the
same old seq — the torn copy passes the check. (A seqlock needs the writer to mark a write in progress
before touching the fields, e.g. an odd seq first; the recipe does not do that, and no bench run has
tested any variant.) Never run on silicon; refuted by this counterexample. **Applied 2026-10-03 to the
YAML («#375»):** the option is replaced by a sentence saying why it is not safe; R5 remains the
non-blocking route. **Owed:** the same correction in the P2AN007 document — its next release (manual
head; app notes ship through their own release).
