# Fan-Out Fabrication-Audit Findings — App Note P2AN005

**Slug:** P2AN005 · **Spec:** fan-out v1.1.0 · **Generated:** 2026-07-10 (plan §5 / task #177)  
**Claims extracted:** 69 · **Survivors:** 1 · **Rejected by verify:** 0

> Candidate findings — each survived an independent adversarial refute pass. **Pending human hand-check + class-wide sweep.** Not yet applied to the document.

## Survivors (confirmed/refine)

| Location | Kind | Verdict | Conf | Class | Claim | Tier-1 says | Correct statement |
|----------|------|---------|------|-------|-------|-------------|-------------------|
| P2AN005.md §Adapt It / Going Further | capability | misaligned | high | false-negative-capabilit | which would need a hardware mutex the P2 doesn't have | The P2 has a hub lock pool of hardware locks (semaphores) that grant o | The P2 DOES provide hardware mutual-exclusion primitives — 16 hub lock |

### Full detail per survivor

**S1. P2AN005.md §Adapt It / Going Further, line 301** — `misaligned`/high · class `false-negative-capability-denial`  
- Claim: which would need a hardware mutex the P2 doesn't have  
- Anchor: "without splitting the bus across cogs (which would need a hardware mutex the P2 doesn't have)"  
- Tier-1 (Silicon Doc v35 p2-documentation.txt LOCKS section (~lines 7455-7490): 'locks are just a means of allowing one cog at a ): The P2 has a hub lock pool of hardware locks (semaphores) that grant one cog at a time exclusive 'owner' status across cogs — i.e. hardware mutexes. LOCKTRY takes a lock, LOCKREL releases it, and while held no other cog can take it.  
- Correct: The P2 DOES provide hardware mutual-exclusion primitives — 16 hub locks (LOCKNEW/LOCKTRY/LOCKREL/LOCKRET). The valid point is that keeping the bus inside one cog with cooperative tasks lets you SKIP cross-cog lock coordination, not that the hardware lacks a mutex. Reword e.g. 'which would need cross-cog lock coordination you avoid entirely by keeping the bus in one cog.'  
- Verify: I re-fetched the FULL silicon doc LOCKS section (engineering/ingestion/sources/silicon-doc/p2-documentation.txt, section 'LOCKS', following its TOC entry at line 310). Verbatim: "The hub contains a pool of 16 semaphore bits, called locks. Locks can be used by cogs to coordinate e  
