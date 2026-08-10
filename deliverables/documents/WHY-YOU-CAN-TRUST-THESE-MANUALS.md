# Why You Can Trust What's in These Manuals

We're handing the community a stack of P2 manuals and asking you to lean on them
while you work. That's a real ask, and we don't take it lightly. These manuals are
built with AI assistance under human direction, and the P2 community runs the full
range on that, from "show me" to "no thanks, not for me," and every bit of that
skepticism is fair. AI is very good at writing something that *reads* correct and is
quietly wrong, and a reference manual is exactly the place where that would hurt you.

Here's the honest division of labor. The AI work is structural: drafting, organizing,
and carrying facts across from the documentation we've ingested into the text you read.
What goes into a manual, how it's organized, what's worth saying, and where the line
falls between explaining and drilling are human calls. The verification described
below is the part that decides whether any of it ships.

So this page doesn't ask you to take our word for anything. It lays out how a fact
gets *into* one of these manuals, how we check it, and, just as important, what
happens when we get one wrong. The short version: every claim traces back to a
trusted source or to **real silicon**, we audit our own drafts the way we'd audit a
stranger's, and we say plainly what we don't yet know. Here's the whole chain.

## The trust chain

Everything we publish rides one chain, and the rule is that each link must preserve
the truth of the one before it:

> **Trusted Sources → Trusted Knowledge Base → Trusted Manuals → You**

The sources are of two kinds. There's the **documentary** record: the Parallax
Silicon Doc, the datasheets, and Chip's own PNut compiler source. And there's the
**empirical** record, code we write, compile, and *run on a real P2*, where the chip
itself tells us what's true. When those two ever disagree,
the silicon wins. It sits at the top of the chain on purpose, and further down you'll
see what happened the times it spoke up.

From the sources we build a structured knowledge base, and from that knowledge base
we derive the manuals. The manuals are never the first place a fact is written down;
they're the *last*, downstream of a source we can point to.

## Where the facts come from

Before a source is allowed to ground anything, it's catalogued and rated. We keep an
authoritative-sources list that tags every source with a trust tier and a reason for
that tier, and a documented order of precedence for when sources conflict (hardware
first, then the compiler, then the Spin2 language documentation, then the Silicon Doc
and datasheets, then community lore). A claim inherits the trust of wherever it came
from, and we keep the lineage so we can always walk it back.

We also keep an honest ledger of **what's missing**: the questions the documentation
doesn't answer, the corners nobody has nailed down yet. That ledger ships as part of
the work rather than being quietly papered over, because "we don't know this yet" is
itself a fact you can use, and pretending otherwise is how a manual loses your trust
for good.

## Checked against the silicon

This is the part we're proudest of, and it's the part most documentation can't offer.

Every code example we ship is run through `pnut_ts` and has to compile clean before it
goes in the book. And `pnut_ts` isn't a third-party tool we're taking on faith. It's a
cross-platform port of Chip's own PNut compiler, developed jointly by Parallax and Iron
Sheep Productions by studying PNut's original source and re-implementing it line by
line. Anything PNut compiles, `pnut_ts` compiles to a **byte-for-byte identical
binary**, and that isn't an aspiration: the bulk of its regression suite is golden
files produced by PNut itself, compared byte-for-byte on every platform, every build.
(`pnut_ts` also accepts a superset, a handful of directives PNut doesn't provide. Our
examples deliberately stay inside what PNut accepts, so the code in these manuals
builds under either compiler.) So checking a program against `pnut_ts` really is
checking it against Chip's compiler. For the debug-window code, that compile is run
with the flag that actually evaluates the `DEBUG()` directives, so the compiler is
checking the part that matters instead of skipping past it.

But compiling clean is only the floor. For the **Debug Window Manual** we go all the
way: a program is compiled clean, then it's taken to real hardware through PNut-Term-TS
and *actually run*, and the screen it produces is captured and brought back into the
manual. So the thermal heatmap, the PID strip-chart, the glitch capture, and the motor
run-up you see in those chapters are **not mockups or hand-drawn diagrams. They are
the actual output of the exact program printed on the page.** Code in, real picture
out, both in front of you. That's about as close to "see it for yourself" as a book
gets.

And it isn't only the examples that are grounded that deeply. The window *descriptions*
are too. For the Debug Window Manual we went through Chip's PNut compiler itself and
documented every facet of all nine windows straight from it, every directive, parameter,
range, and default, verifying each against the compiler as we went. That verified study
became part of the knowledge base, and from there it strengthened the manual. So what the
book tells you about a window doesn't come from a second-hand account or someone's memory
of how it works; it traces straight back to the code that actually implements it.

And when we say silicon outranks the page, we mean it has *changed* the page. Running
tests on a real P2 has corrected our own knowledge base and even corrected one of our
own already-released manuals. We hold our own published work to the same chip-level
check as everything else. We keep the accepted tests and their results as a permanent,
versioned record of empirical findings, so those corrections are evidence you can
check, not claims you have to believe.

A fair note while we're being straight with you: not every manual is example-driven,
and that's by design (more on that in the companion "how these are made" page). Where
a manual carries code, that code is compiled; where a manual's whole job is to
*explain a capability* rather than drill it, it leans on description. We try to always
be clear about which is which.

## We audit our own work

We assume our own drafts contain mistakes, and we go looking for them with a real
methodology, not a quick reread. We learned that the hard way.

When we first put our earliest manuals, the Assembly Reference and the deSilva
tutorial, into the community's hands, we were too eager. A few sharp-eyed readers came
back almost immediately with things that were flat-out wrong: errors that should never
have shipped. We turned the fixes around fast, but the fixes weren't the real win. The
real win was that those early eyes forced us to build the auditing discipline we use
today, so that whole *class* of mistake can't reach you the way it did again, not in a
new manual, and not in an update to an old one. It was painful at the time, and it was
probably the best thing that could have happened to this project. If you were one of
those readers: thank you. This is partly your doing.

The cheapest mistake to fix is the one you never write, so the first pass is at
*writing* time: a fact gets verified against its source before it goes on the page,
not after. Then, after the fact, every claim is extracted and cross-checked against
the primary sources and sorted into verified, modified, unverified, or, the one that
matters most, **fabricated**. We've caught our own fabrications and our own confident
little errors this way, on manuals we'd otherwise have been happy with. Those finds
don't get buried; they go into a corrections register that tracks each one from
"found" to "fixed."

Some of the most valuable material in our smart-pin manuals came in from outside,
through **Jon Titus**, a well-respected name in embedded computing, who wrote a
generous, tutorial-grade study of the P2's smart pins and shared it openly with the
community, readers' inline comments and all. It's a genuinely good piece of work: it
walks all thirty-two smart-pin modes with the *how and why*, worked calculations,
complete runnable examples, and timing diagrams. We didn't hold it at arm's length, and
we didn't merely audit our own draft against it. We accepted his document *into* our
process as a first-class source, to be ratified, broadened, and carried forward into
formal manuals.

Ratifying it meant running every code example through `pnut_ts`, Chip's own compiler,
and holding every claim against the Silicon Doc and, where it mattered, against real
silicon. Most of it held up beautifully. A few things didn't, including one bit-field
table Jon's own readers had already questioned and the chip confirmed wrong, and a
handful of reader observations that simply didn't survive silicon. Those we
corrected and marked rather than passed along. Broadening it meant re-casting the
material for the people who'll actually use it: where a mode was written as a raw
bit-pattern we rewrote it with the compiler's named constants (`P_DAC_NOISE`, `P_PULSE`,
and the rest) so the code shows what it's doing; where he taught in assembly we
re-expressed the same capability in Spin2, the language most P2 users reach for first,
with the PASM2 kept alongside; and where his study left a corner thin, we filled it from
the primary sources.

We also made one deliberate departure. His study follows the natural reference order,
mode %00000 straight through %11111, exactly right for a document you look things up
in. Our manuals have a different job, bringing a reader along, so we organized the same
ground as a learning progression: fundamentals first, then output modes, then input
modes, then the special cases. Same material, ordered to teach rather than to index.
Through all of it, Jon's name stays on what he contributed. Accepting a serious
author's work, verifying it, and presenting it clearly is how we honor it here, not the
opposite of it.

That's the honest shape of this work: the audits aren't proof we're never wrong,
they're proof that being wrong gets *caught and recorded* here instead of shipping
silently.

## What we refuse to claim

Part of trust is discipline about what you *won't* say. A few standing rules:

- **No unsourced claims.** If we can't point to where it came from, it doesn't go in.
- **No numbers that quietly drift.** We don't publish compiler bytecode values or
  interpreter clock-timings that change from one tool release to the next and would
  silently rot into wrong. We describe the behavior instead.
- **We keep provenance.** Authorship, copyright, and who-figured-this-out stay
  attached; that chain of credit is part of how you judge a source, so we don't strip
  it.

Small thing you'll notice: we say **cog**, not "CPU." The community treats the cog as
the computer, and matching how *you* think about the chip is part of getting it right.

## When you report a problem, it ships

Here's the question every reviewer is really asking: *if I find something wrong, will
it actually get fixed, or rot in a backlog?*

Because the manuals derive from one shared knowledge base, a correction usually lands
in **one** place and propagates out from there, and the corrections register tracks it
the whole way. That means turnaround is fast, and it means we can deliver in *phases*.
The Streamer guide is a good example: it exists to introduce a part of the P2 that was
genuinely hard to get your arms around, and it's deliberately an early, lightweight
delivery. If the community tells us per-mode examples would help, we can add them and
push the guide back out again without rebuilding anything. Your feedback isn't a
suggestion box; it's the next edition.

And "one place" undersells what that propagation does for you. The same knowledge
base feeds every manual and the machine-readable source our AI coding assistants read
from, so a single thing you flag against one page can correct that fact everywhere it
lived, all at once, in books you weren't even reading, and in the source an assistant
answers from. That is not hypothetical. On a recent read, a reviewer went through one
of our references casually and turned up a handful of errors in an afternoon, including
two spots where the prose described behavior the chip simply doesn't have. One of the
notes was a small notation fix, and it turned out to be live in more than sixty of the
underlying data files, not the single table it pointed at, so it was corrected across
the whole set in one pass. The findings did more than get fixed, too: they showed us the
narrative chapters hadn't been held to the same silicon-backed proof as the look-up
entries, so we extended that proof to the narrative as well. One reader, one afternoon,
and the whole system came out sharper.

There's a second kind of leverage that only shows up when many people read at once. A
few reviewers, each arriving from their own angle (the assembly programmer reading for
timing, the driver author reading for edge cases, the newcomer reading for what went
unexplained) will between them catch what no single exhaustive pass can, because each
one sees what their own vantage makes visible. We can't staff all of those perspectives
ourselves. You are them, and a handful of sharp, honest reads does more for a manual
than one more careful pass on our end ever could.

## The short of it

These are **review editions** on purpose. They're grounded deeply and checked hard,
and they'll still miss in their own particular ways, the kind of thing automated
checks can't catch but a practitioner spots in a heartbeat. Everything above is what
lets us hand them to you with a straight face: a traceable source or real silicon
behind every claim, our own work audited the way we'd audit anyone's, plain talk about
what we don't know, and a fast path from your report to a fixed page.

That last link in the chain is you. Read hard, push back, and tell us what you find.
Every report you send makes the next release of these manuals better. I look forward to
seeing what you turn up.

-Stephen
