# How These Manuals Are Made, and How They Stack Up

The companion to this page, *"Why You Can Trust What's in These Manuals"*, is about
whether the **content** is right. This one is about the **craft**: how these manuals
are built, measured honestly against how the best technical reference manuals in the
world are actually made.

So we went and looked. We pulled the production practices the top publishing houses and
documentation standards actually use, and then asked the uncomfortable question: where
do we meet that bar, where do we get past it, and where do they still have us? Here's
the honest scorecard.

## The bar: how the best reference manuals get made

Strip it down and a world-class technical reference comes from a fairly consistent
pipeline. Some of it is genuinely codified. International standards exist for
indexing (ISO 999, ANSI/NISO Z39.4), for terminology (ISO 704), for accessibility
(the W3C's EPUB rules, WCAG, and now actual EU law). Most of it, though, is strong
professional *norm* rather than law:

- **Single-source, structured authoring.** Write once in a structured, version-
  controlled form, publish to many outputs (the formal version is DITA; the code-shop
  version is "docs-as-code").
- **The right document type for the job.** The profession draws a hard line between a
  *reference* (look-it-up, austere, complete) and a *tutorial* (learn-by-doing,
  narrative). The popular Diátaxis framework names them as different things with
  different rules; you don't write one like the other.
- **Code that actually runs.** The best programming publishers (Pragmatic Bookshelf is
  the clearest example) keep their code in real source files that are compiled and run,
  so the listing printed in the book is the listing that *worked*. Most houses don't go
  this far; they lean on expert review plus a published errata page.
- **Several editing passes by different people.** Developmental edit, technical review
  by subject experts, copyedit, proofread.
- **A house style guide and controlled terminology.** One approved term per concept,
  layered over a standard like the *Chicago Manual of Style*.
- **A real, human-built index.** For a reference, this is the big one. A machine
  produces a *concordance* (words → page numbers); a human produces an *index* (concepts
  → where to look), including the word a reader would search for even when the text
  never uses it.
- **Edition and errata discipline.** Clear version identity, public errata, fixes
  folded into reprints; for software-tied books, keeping current with the releases.
- **Accessible production.** Semantic structure, alt-text, accessible PDF/EPUB.

That's the bar. Now, honestly, against it:

## Where we meet that bar

- **Single-source, structured authoring: yes.** Our manuals aren't hand-typed
  one-offs. They're derived from one structured knowledge base, kept in version control,
  the same docs-as-code discipline the standard calls for. A fact lives in one place and
  flows out to wherever it's needed.
- **Code that actually runs: yes, and this is where we're strongest.** Every code
  example is compiled clean on `pnut_ts` before it ships. `pnut_ts` is a cross-platform
  port of Chip's own PNut compiler, developed jointly with the chip's designer, and
  anything PNut compiles it compiles to a byte-for-byte identical binary. That's checked
  continuously: the bulk of its regression suite is golden files produced by PNut itself,
  compared byte-for-byte on every platform. So a clean compile there is a clean compile
  against the real thing. And
  for the **Debug Window Manual** we go the whole way the best programming publishers do,
  and
  then some: the program is compiled clean, then *run on real hardware*, and the screen
  it produces is captured and dropped into the page. The thermal heatmap, the strip-
  chart, the glitch capture you see there are the actual output of the exact program
  on the page, not a mockup, not a redrawn figure. Code in, real picture out.
- **Edition and errata discipline: yes, and tightened.** Every manual carries a real
  version and changelog; corrections are tracked in a register from "found" to "fixed";
  and because the manuals derive from a knowledge base that's gated to specific compiler
  and silicon revisions, "keeping current with the releases" is built into how the
  content is sourced, not bolted on after.
- **Style and terminology governance: mostly.** Each manual has a written **voice
  guide** that defines its register, plus standing rules about terms (we say *cog*, not
  "CPU," because that's how the community thinks about the chip). It's real governance,
  even if it isn't a formal term base.
- **Expert technical review: in our own form.** The best houses put a manuscript in
  front of subject-matter experts before it's final. Ours are **review editions**, in
  front of the whole community of P2 practitioners right now, and we plan a further pass
  with the **chip's own designer**, to fold in what he thinks we should cover, what we've
  missed, and the specific insights that live nowhere in the documentation, as new source
  material. A different shape than a publishing house's review desk, but the same purpose,
  with arguably a rarer caliber of expert.

## Different manuals, different jobs

The profession's reference-vs-tutorial line is one we drew *on purpose*, and it's why
this set looks the way it does. These aren't four attempts at the same book. They're
four different document types, each built to its job:

- The **Assembly Language Reference** is a true **reference**: austere, complete, laid
  out for look-up.
- The **deSilva-Style Assembly** book is a **tutorial**: warm, narrative, learn-by-
  doing.
- The **Streamer Guide** is a **capability introduction**. It exists because the
  streamer was genuinely hard to get your arms around from the silicon docs alone, and
  its job is to make the *breadth and function* of the streamer make sense. It's
  deliberately an early, lightweight delivery, not a training manual, and if the
  community tells us per-mode examples would help, that's a fast follow-on, not a
  rebuild.
- The **Single-Step Debugger** guide is a **tool quick-reference**, a reminder of how
  and why to drive a debugger you already have. Its community review is itself a test:
  it gets validated by running the guide straight through against the live single-step
  support built into PNut-Term-TS, with a parity source to check against. The manual
  doubles as the tool's acceptance test.

Matching depth to purpose, and saying plainly what each one is *for*, is itself part
of the craft. We don't pad a quick-reference into a textbook to look thorough.

## A process built to repeat itself

Here's a practice the publishing-house list doesn't quite capture, because it comes
from software engineering rather than from books: we've turned our own production steps
into **codified, repeatable procedures**, the same way you'd write a script instead of
doing a fiddly job by hand every time.

The audit that checks a chapter for unsupported claims, the steps that stage a manual
for printing, the release checklist, the ingestion of a new source: these are written
down as repeatable procedures and run the same way every time. That matters for *you*
because it means the rigor doesn't depend on whether someone remembered to be careful on
chapter 9 at the end of a long day. The same checks run on every chapter, every manual.

Behind that sits a standing rule set, and every rule traces back to a real mistake we
made once and refuse to make twice, so the process doesn't just repeat, it *improves*.
And the auditing work that backs the trust page isn't a one-time event; it's part of the
machine.

## Where we go past what a printed book can do

Three things in this pipeline a traditional print house structurally *can't* offer, no
matter how good its editors are:

- **We check against the silicon, not just against experts.** A printed reference can be
  reviewed by the sharpest subject-matter experts alive and still be wrong, because
  expert review is still opinion about the chip. We can ask the chip directly: write
  the test, run it on a real P2, and take the result as ground truth. It has overruled
  our own knowledge base and one of our own released manuals. A book on paper has no way
  to do that after it's printed; our source does it continuously.
- **The same source serves a human *and* an AI.** These manuals are the human-readable
  face of a machine-readable knowledge base. The exact source that grounds the book also
  answers an AI coding assistant's questions directly, curated and version-tracked, far
  better than letting a model guess from scraps it found on the open web. One source,
  two audiences. A printed book serves one.
- **The review doesn't end when the book ships. It's when the biggest review starts.**
  A printed reference freezes the moment it goes to press. The best a paper book can do
  about a mistake a reader finds afterward is a separate errata sheet, which reaches only
  the people who go looking for it and corrects the error in exactly one spot. Ours work
  the other way around: a find after publication is folded straight back into the one live
  source, and because the same fact often appears across several manuals and in the
  machine-readable source too, correcting it once corrects it everywhere. So putting a
  manual in front of the whole community isn't the last tidy step after review. It's the
  point where the largest and most varied review pass we could ever run finally begins.

And because that source faces both ways, it gets better from both directions. When an AI
assistant can't find something in the knowledge base (sometimes a user reports it, and
sometimes the assistant itself tells us plainly *why* it couldn't find what it needed)
that isn't a dead end, it's a signal. It points at a real gap, or at material that's
there but not reachable from the angle someone actually searched. So we go back and fix
the knowledge base, adding what's missing, or adding the new wording, perspective, or
cross-reference that makes it surface, and because the manuals are drawn from that same
base, the fix doesn't stop at the database. We push it back into the manuals, so the book
and the machine-readable source stay in step. Every surface we expose becomes a way to
find out what's still missing, and every find flows back into the whole system. The
manual and the knowledge base sharpen each other.

None of that is hypothetical. It's how the last stretch of work actually went:

- **Writing the Debug Window manual** showed us the knowledge base didn't yet say enough
  about some of the windows. So we bolstered the knowledge base, which made the manual
  better and left the database stronger for the next person, human or AI, who comes
  asking.
- **The smart-pin work** is running the same loop right now. As we ratify Jon Titus's
  community study against the hard sources, and weigh its readers' comments the same
  way, the gaps and questions that surface get folded into the knowledge base, and from
  there back into the manuals. Because that new material lands
  *after* some manuals were already written, we then go back and re-audit the older ones
  against the improved base, and re-release the ones that need it rather than leave them
  behind.
- **The hardware add-on boards** were a pure findability miss: much of that material had
  already been ingested, but it wasn't in the search index, so AI assistants couldn't
  surface anything about the various evaluation and add-on boards even though it was
  sitting right there in the database. That's the "there, but not reachable" case exactly.
  We corrected the indexing, and now it shows up.
- **Functional decomposition** came from watching AI assistants handle it badly, because
  we'd given them no guidance on it at all. So we added a whole new section of the
  knowledge base so they could. That worked well enough that it's likely to grow into a
  short, plain-language guide for people who want to learn the same approach: a new
  introductory document, born from a gap an AI revealed.

## Where we don't match them yet

Being honest about this is the whole point, so here's where a traditional house still
has us:

- **No professional copyedit-and-proofread pass.** We don't have a dedicated copyeditor
  and proofreader running the classic line passes a publishing house would. That craft
  role isn't part of how we work, and we won't imply otherwise.
- **No formal accessibility conformance.** We produce clean PDFs, but they aren't
  certified against PDF/UA or WCAG AA, the accessibility standards the best houses now
  treat as table stakes, and which are becoming legally required to sell into some
  markets. A real gap.
- **The index isn't a professional concept index.** It isn't hand-authored by an indexer
  the way the gold standard is, and it isn't a raw machine word-dump either. We build it
  from a consistent *measure of importance*: every term that clears that bar gets
  included, and the presentation is human-shaped. Systematic and repeatable, but not the
  dense, cross-referenced, implied-vocabulary index a career indexer would produce to ISO
  999, the kind that lists the word you'd search for even when the text never uses it.

We'd rather you hear those from us than discover them.

## Why we built it this way

None of this is new in spirit. People who build reference works have always reached for
the best tools they had: typesetters, concordance programs, compilers that check the
examples on the page. The question that's always mattered isn't *which tools touched the
page*, it's *was the result checked against the truth*.

For a small team, the real ceiling on a job this size is plain human hours. AI doesn't
replace the judgment or the verification. It does the tireless part: drafting,
cross-referencing, reformatting. What that buys us isn't a shortcut; it's the
*opposite*. It lets us afford to check **everything**, compile every example, run the
ones that matter on silicon, audit every chapter the same way, instead of spot-checking
because a person ran out of day. We were never trying to go faster by cutting corners;
the tool just made it affordable to cut *none*.

So we keep two claims strictly apart, on purpose:

- **The AI is why a small team could write manuals this complete.**
- **The verification, the sources, the compiler, the silicon, the audits, is why you
  can trust what's in them.**

Those are different things. The first explains how these exist at all; only the second
asks for your trust, and it earns it the same way any reference does, by being checked.

## The short of it

Measured against how the best reference manuals in the world are made, we meet most of
the bar, we get past it on the two things a printed book can't do (checking against real
silicon, and serving an AI as well as a human) and we're honestly short on a few craft
passes a traditional publishing house runs. That's the real picture, no spin.

Tell us where it's wrong. That's what makes every edition that follows better. Please let
me know when you do.

-Stephen
