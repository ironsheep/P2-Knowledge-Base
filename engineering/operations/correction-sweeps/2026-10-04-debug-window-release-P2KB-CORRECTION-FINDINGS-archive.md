# P2KB Correction Findings — ARCHIVE, swept 2026-10-04 (after the Debug Window v1.1.4 release)

> **This is an archive of CLOSED findings. It is never re-edited.** Ask "what is
> outstanding?" of `engineering/operations/P2KB-CORRECTION-FINDINGS.md` alone — never
> re-derive completion state from here. If an archived finding must be reopened, it
> returns as a **new** active finding that references this file.
>
> Contains 1 finding carrying a `DONE` status token: F-531 (released in the P2 Debug Window
> Manual v1.1.4, tag `p2-debug-window-manual-v1.1.4`, verified on the released PDF on 2026-10-04).
> The third sweep of the day, so it has its own file (the two earlier 2026-10-04 archives are never
> re-edited).
>
> Swept by rename-then-trim: the register was `git mv`'d here and copied back; this copy was cut to
> the 1 finding, and the live copy had the same text removed with the edit tools. Every line below is
> the pre-sweep text (commit 92916ddd), verbatim; `audit-register-hygiene.py --sweep-check 92916ddd`
> proves it.

---

### F-531 — DEBUG Window BITMAP: "a runtime RATE with any positive count resumes refreshing" — `DONE` (released in v1.1.4, 2026-10-04, verified on the PDF: page 39)
> **Applied and released.** The sentence now says a later `TRACE` or `CLEAR` (each re-derives the rate) or an
> explicit `UPDATE` brings it back, and that a runtime `RATE 0` freezes it as `RATE -1` does (`bitmap.yaml`
> RATE entry, from the PNut source). "(Hardware-verified.)" moved to follow the freeze sentence, the only part
> the bench measured.
D21. `ch04-bitmap.md:311` (marked "Hardware-verified"). `bitmap.yaml:47` (from the PNut source): a later
TRACE or CLEAR, or an explicit UPDATE, un-freezes it. **Fix:** replace the sentence; check what the
"(Hardware-verified.)" tag covers (the freeze, not the recovery).
