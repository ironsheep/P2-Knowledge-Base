# GOLDEN — Cross-cog data structures (P2AN007 rig suite)

**Date:** 2026-07-13 · **Silicon:** P2 Edge, RAM download · **Toolchain:** `pnut_ts` v1.55.0 `-d`
· **Clock:** `_clkfreq = 200_000_000` · **Feeds:** EF-036 … EF-040
**Origin:** built to verify P2AN007 v1.0.0 ("Data Structures with the New Language Facilities")
before its first render. Compilation proves the STRUCT and lock code is *legal*; only two cogs
actually contending prove it *correct*.

## Method — dual-tail, and why the negative control is the point

Every race rig runs the correct discipline **and** a control that is deliberately broken in exactly
one way, with any injected delay applied **identically to both arms** — so the arms differ only in
the protocol under test. Each rig refuses to report PASS unless its broken arm actually fails:
zero-in-both-arms means the detector never fired, which is `INCONCLUSIVE`, never success.

That guard earned its keep twice (see *Rig defects found*, below). Both failures were in the
**rigs**, not the recipes, and both were caught rather than banked as false greens.

## Results (final runs, all PASS)

| Rig | Claim | Control arm | Broken arm |
|---|---|---|---|
| VT1 | ring buffer: publish the index **last** | 0 tears | **200,000 / 200,000** tears |
| VT2 exp-1 | mailbox: publish the sequence **last** | 0 bad | **20,000 / 20,000** bad |
| VT2 exp-2 | mailbox: the seq/ack handshake is load-bearing | 0 bad | **20,000 / 20,000** bad |
| VT3 | one hardware lock serializes two enqueuing writers | 0 anomalies | **3,331** anomalies |
| VT4 | a one-long packed record still needs a **one-store** publish | 0 tears | **116,452 / 200,000** tears |
| VT5 | `OFFSETOF`/`SIZEOF` match the published layout numbers | 11 / 11 checks | — (deterministic) |

VT1 and VT4 reproduced across two independent runs (VT1: 200,000 twice; VT4: 109,642 then 116,452).

## The headline — VT4

Packing a record's named fields into one long does **not** make it atomic. Each bitfield write is a
read-modify-write of the backing long, so filling the *shared* record field-by-field is several
separate stores and a reader lands between them: **116,452 torn snapshots in 200,000**. Staging the
record in a private local and publishing it with **one** whole-struct store tore **zero**. The
atomicity is bought by the one-store publish, not by the record fitting in 32 bits. This is the
counter-intuitive fact P2AN007 R5 is built around, and it was measured, not reasoned.

## VT2 exp-2 — the ack is load-bearing (grounds F-213)

With the seq/ack handshake removed and a worker that spends 25µs between reading the opcode and
reading its arguments — i.e. any worker that dispatches on the opcode before using the args, which
is nearly all of them — **every single command tore: 20,000 / 20,000**. The matched control (A2:
same 25µs worker, ack present) tore **zero**, which is what isolates the ack as the cause rather
than the injected delay.

The danger is precisely that it *looks* fine: a worker that only polls, with no work between its
reads, wins the race against the writer and reports zero (measured — see below). Safety without the
ack is contingent on worker timing, which is not a property any reader should have to reason about.

## Rig defects found (both caught by the INCONCLUSIVE guard)

1. **Phase lock.** VT3's unlocked arm reported 14,976 anomalies on run 1 and **0** on run 2 from a
   binary whose only change was debug text. Two cogs running deterministic loops of equal length
   hold a near-fixed relative phase: whether the writers ever collide was decided at `cogspin` time
   and never re-sampled. **Fix:** hold the contended window (10µs) open longer than the other cog's
   entire loop, making the overlap structural. → `lessons-learned/two-cog-race-rigs-must-be-structural.md`
2. **One worker cannot serve two claims.** A slow worker exposes the missing-ack bug but *hides* the
   bad-publish-order bug (whose window is the ~2µs between the seq bump and the fields landing); a
   fast worker does the reverse. **Fix:** two experiments, each with its own worker **and its own
   matched control**.

## Reproducing

Each rig is standalone: `pnut-ts -d vt<N>-*.spin2`, download to RAM, capture DEBUG. Every rig
announces its arm count up front, prints one `VT# RESULT:` line, and ends with `VT# DONE`. Raw logs
are not versioned (regenerable from these `.spin2` files); the numbers above are the receipt.
