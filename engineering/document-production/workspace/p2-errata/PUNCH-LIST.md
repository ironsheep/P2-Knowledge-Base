# P2 Errata — Punch List

Active-work register. Completed items are swept into the dated archive at the bottom at
each closeout; the list above carries only **outstanding** work.

---

## Outstanding

### Chip Gracey's "why it exists" paragraph for each erratum — PARKED (may never happen)

Parked 2026-10-11 from task «#373» (Stephen: "may or may not happen... remember its intent so
if it does finally happen, we'll know what to do").

**Intent.** Each erratum entry says *what* the part does and the rule code must follow. Chip
said on 2026-10-02 that he would amend the P2 Documentation (the Silicon Doc) with the errata;
Stephen asked him to use our E1-E7 numbers. If that amendment also states *why* each erratum
exists, the reader gets the design reason, in Chip's words, beside each entry.

**Trigger.** Parallax publishes the amended Propeller 2 Documentation. Nothing before that:
manuals cite only official, published Parallax documentation, and our own P2 Errata may never
ship either (see the Silicon Doc publication path).

**Until then, by design (RESHAPE-SPEC.md D4).** No placeholder and no forward reference. Each
entry reads complete without the paragraph. Stephen, 2026-10-03: "draft this in a way such that
it's easy for us to add the Y later, but we don't indicate that the Y is going to appear for now."

**What to do when it publishes:**

1. Ingest the amended P2 Documentation first (`ingest-source`), so every quote can be checked
   against the ingested text.
2. For each erratum whose design reason the amendment states, add ONE short paragraph at the
   fixed insertion point: directly after the summary box (`<!-- include: shared-eN.md -->`),
   before `## What happens` (RESHAPE-SPEC.md §4; creation-guide §4 item 2). Edit the
   opus-master only.
3. Quote or paraphrase the amendment and name its section. Never use the clean-room study's
   account of the cause. An erratum the amendment gives no reason for gets no paragraph.
4. The same publication is when the KB and the other manuals can start citing the errata: the
   follow-up sweep adds the citation where a manual states an erratum's rule (and the KB's
   `architecture/silicon_errata.yaml` gains the amended document as a source for each entry).
5. Then `prepare-manual` → Stephen builds → verify the PDF → CHANGELOG.

---

## Archive

- _(none yet)_
