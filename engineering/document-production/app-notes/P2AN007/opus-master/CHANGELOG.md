# P2AN007 — Data Structures with the New Language Facilities — Changelog

## v1.0.1 (2026-08-08)

A licensing change. No technical content changed — not a page of it.

- **License restored to CC BY-SA 4.0.** This note is again licensed Creative Commons Attribution–ShareAlike 4.0 International, the license the community-review editions carried from 2025-12-09 through 2026-05-22. You may share and adapt it, including commercially, with attribution and under the same terms.
- **Why it changed back.** The CC BY-NC-ND terms it carried from 2026-06 went well beyond their intent. NonCommercial does not restrict resale — it restricts *all* commercial use, including a paid course referencing a chapter or a distributor bundling the PDF with a board. NoDerivatives blocked translations, excerpting, and community forks. The concern behind that change was only that someone might resell this as their own product.
- **Trademark, not copyright, addresses that concern.** The Trademarks note now states that the license grants permissions under copyright only: a reuser may copy, adapt, translate, and sell the text, but may not present the result as the official edition or imply endorsement.
- **Nothing was retroactively taken.** Creative Commons licenses are irrevocable, so every copy distributed under BY-SA stays BY-SA permanently.

## v1.0.0 (2026-07-13)

Initial release for community review. A techniques-catalog application note for the Spin2 `STRUCT`
facility — packed, named, typed records — and the worked code for sharing them safely across cogs.
One shared idea (a single hub long is atomic but a multi-field record is not, so a record is
published by writing its fields first and flipping one long last) applied through six runnable
recipes: an in-cog record and array, a lock-free single-producer/single-consumer ring buffer, a
latest-wins command mailbox published with a sequence counter, a lock-guarded multi-writer queue on
the real P2 hardware locks (`LOCKNEW`/`LOCKTRY`/`LOCKREL`), a whole command record packed into a
single atomically-published long with `{Spin2_v54}` member bitfields, and compiler-computed member
offsets with `{Spin2_v53}` `OFFSETOF` for the places raw addressing is unavoidable. Recipes R1–R4
need only `{Spin2_v45}`, so a compiler predating the newer facilities still builds them.

The note carries the counter-intuitive fact at the heart of packed records: fitting a record into
one long does not make it atomic, because each bitfield write is a read-modify-write of the backing
long — atomicity comes from staging the record privately and publishing it in a single store. Every
cross-cog claim here is confirmed on real P2 silicon with two cogs actually contending: each
discipline was measured against a deliberately-broken version of itself, and the broken version was
required to fail before the result was accepted.

Implementation-only by design: the note teaches the worked code and defers the *contract decision*
(which structure to use and why, copy vs. reference) to the P2 Architect's Guide. Every recipe
compiles clean under `pnut_ts -d`. Ships with a downloadable example library of all six programs.
