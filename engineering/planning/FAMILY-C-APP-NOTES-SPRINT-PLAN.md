# Family C App Notes — Sprint Plan

> **Status:** Planning (2026-07-06). Head: **document-production / app-notes**
> (`active_element = manual:app-notes-family-c`). Produces **three** new P2
> application notes end-to-end (author → PDF), each on the four-artifact model.
> Governing specs: `engineering/document-production/app-notes/APP-NOTE-CREATION-GUIDE.md`
> (structure/pedagogy/sourcing), `APP-NOTE-VOICE-GUIDE.md` (voice),
> `APP-NOTE-DESIGN-DECISIONS.md` (four-artifact + YAML-companion principle),
> roster `engineering/analysis/p2-app-note-roster.md §Family C`.
> Exemplars (all released): P2AN001–P2AN004.

## Scope (confirmed with Stephen 2026-07-06)

Author the three **Family C — Concurrency & New Language Features** app notes,
full four-artifact each (human doc + first-party YAML companion + runnable
example(s) + example-library ZIP), take **all three to PDF** (staged in
`outbound/` for Forge generation), then **untrack** the two mistakenly-committed
`appNote-fodder-NO-COMMIT/stack/` files.

| Roster | Note | Number | Successor to | Build pairing |
|---|---|---|---|---|
| **C1** | Cooperative Multitasking with Spin2 TASK Methods | **P2AN005** | P1 AN014 (Coroutines) | authored **with** C3 |
| **C3** | Sizing Cog & Task Stacks | **P2AN006** | P1 AN019 (Stack Space) | authored **with** C1 |
| **C2** | Data Structures with the New Language Facilities | **P2AN007** | P1 AN003 (Abstract Data Structures) | authored after the pair |

Numbering: `P2AN001–004` are taken (004 = Frequency/Period/Pulse, released);
005/006/007 are the next free sequential ids, assigned at commit-to-production in
build order (C1, C3, then C2). No collision (research-confirmed).

**Common ground (all three):** the owning manual is the **Spin2 Reference, which
is PARKED** — so each note is the *guided home* for its topic (advanced-fork-only,
like P2AN002/P2AN004's empty foundational forks). There is **no manual-enrichment
fork** for any of the three; nothing here belongs in a currently-shipping manual.
Archetype: **techniques-catalog** (shared conceptual base + a small set of runnable
recipes chosen among by need), matching P2AN001/P2AN004. Doc class: app-note over
the shared `p2kb-platform-*` + `p2kb-appnote-*` stack, K=76, **no ToC**, cover
"What You'll Build" box, joint Iron Sheep + Parallax copyright.

---

## §0 — Sequencing & boundaries (settled 2026-07-06)

Settled with Stephen — recorded for the record, not gates:

**Numbering & build order.** C1→P2AN005, C3→P2AN006, C2→P2AN007 (pair first, then C2) —
matches roster §5 and the "number = build-order provenance" rule.

**KB corrections are DEFERRED until after the drafts are up for PDF review.** Findings
are **logged** to `P2KB-CORRECTION-FINDINGS.md` as they surface (always — never gated).
**No `.yaml` edits happen during authoring.** The notes are authored *correctly against
P2* regardless of the register state: C2 uses the real P2 `LOCKTRY`/`LOCKREL` (never P1
`lockset/lockclr`), and any suspect token (e.g. `TASKWAIT`) is **compile-probed with
`pnut_ts`** and excluded if it doesn't compile — a compiler probe, not a YAML change.
Once all three drafts are staged for PDF review, the logged findings are handed to a
yaml-head pass (`yaml-knowledge-base-maintenance`). See §4/§5.

**C2 boundary.** C2 teaches the *implementation* (worked mailbox/ring/queue/deque code)
and **cites, does not teach**, the *which-structure-and-why* decision — that reasoning
stays with the Architect's Guide + `data-flow-contracts.yaml` (esp. refcount-vs-copy
fan-out, flagged irreversible). Established convention, not a choice.

**Companion schema.** Reuse the established P2ANxxx companion schema (piloted P2AN001,
carried to P2AN004) — digest + `cross_references.composes` links, agreement-gated
against the doc. No schema invention.

**No P1 content in these notes (lineage is metadata, not a source).**
The "successor to AN014 / AN003 / AN019" labels are **roster lineage** (recorded in
`p2-app-note-roster.md` + `P1-DOCUMENT-LINEAGE.md`), not sources the notes read or cite.
These are **P2-native** notes: every technical fact traces to a P2 source (the TASK\*/
STRUCT/lock/stack YAMLs, Spin2 v55, `isp_stack_check`). **No P1 ingestion, and no P1
document read or cited** — References carry only the P2 primary sources the facts trace
to. (The one P1-flavored gotcha worth keeping — C1's "finish the transaction before you
yield" — is already captured in the **P2** pattern `spin2_cooperative_tasking.yaml`;
sourced from there, not from AN014.)

**File table — new/changed files (excludes the generated workspace render):**

| File | Action | Scope |
|---|---|---|
| `app-notes/P2AN005/` (opus-master/, examples-library/, NOTES, MANUAL-DESCRIPTOR, audit/) | create | C1 note tree |
| `app-notes/P2AN006/` (same shape) | create | C3 note tree |
| `app-notes/P2AN007/` (same shape) | create | C2 note tree |
| `deliverables/ai/P2/application-notes/p2an005-cooperative-multitasking-tasks.yaml` | create | C1 companion (digest+links) |
| `deliverables/ai/P2/application-notes/p2an006-sizing-cog-task-stacks.yaml` | create | C3 companion |
| `deliverables/ai/P2/application-notes/p2an007-data-structures-new-facilities.yaml` | create | C2 companion |
| `deliverables/ai/P2/.../spin2_shared_memory.yaml` | **DEFERRED** (after PDF review) | P1 `lockset/lockclr` → P2 `LOCKTRY/LOCKREL`; logged as F-199 now |
| `deliverables/ai/P2/language/spin2/methods/taskwait.yaml` | **DEFERRED** (after PDF review) | stub-invalid iff `pnut_ts` probe fails; logged as F-196 now |
| `engineering/operations/P2KB-CORRECTION-FINDINGS.md` | append | F-196.. (all §4 findings) |
| `engineering/document-production/PUBLICATION-ROSTER.md` | edit | move C1/C3/C2 Upcoming→In progress |
| `engineering/analysis/p2-app-note-roster.md` | edit | Family C status `candidate → …` |
| workspace `P2AN005/006/007/` + `outbound/` | create | Three-Folder wiring for PDF |
| `.gitignore` or `git rm --cached` | edit | untrack the two `stack/` fodder files |

---

## §1 — P2AN005 · Cooperative Multitasking with Spin2 TASK Methods (C1)

**Why.** The `{Spin2_v47}` TASK\* family (cooperative, non-preemptive multitasking of
up to 32 tasks in one cog) is documented in the KB only as atomic method/constant/
register YAMLs + one implementation pattern; there is no end-to-end guided home. This
note is the P2 successor to AN014's hand-coded PASM coroutines — the "what got better"
is that a fragile `JMPRET`/`swap` idiom becomes first-class language methods.

**Starting point (source-confirmed).** Method set from the v55 keyword table
(`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:39,149`) and the YAMLs
`deliverables/ai/P2/language/spin2/methods/task{spin,next,stop,halt,cont,chk,id}.yaml`,
`constants/{newtask,thistask}.yaml`, `registers/taskhlt.yaml`, and the vetted pattern
`patterns/implementation/spin2_cooperative_tasking.yaml`. The "finish the
transaction before you yield / no flag reliance across a switch" gotcha is sourced from
the **P2** pattern `spin2_cooperative_tasking.yaml` (not from P1 AN014).

Method inventory: `TASKSPIN(id, Method(params), @stack)` (expression-returns the task
# or −1), `TASKNEXT()`, `TASKSTOP(id)`, `TASKHALT(id)`, `TASKCONT(id)`, `TASKCHK(id)`
(0/1/2 = free/running/halted), `TASKID()`; constants `NEWTASK`/`THISTASK` (both −1,
different context); register `TASKHLT` @ $200 (32 halt bits, **reversed**: bit0=task31).
Version gate `{Spin2_v47}` must be the **first source line**.

**Target — techniques-catalog, shared base + 4 recipes:**
- Shared base (The Idea / How It Works): the cooperative model, TASKSPIN-is-to-a-task-
  as-COGSPIN-is-to-a-cog, the yield contract (`TASKNEXT`), and the **register-space
  collision** ($100–$11F task-pointer table overlaps inline-PASM ORG..END) as a design
  note.
- **R1 — Two-task round-robin blinker** (the AN014 port): `TASKSPIN`+`NEWTASK`,
  `TASKNEXT`; author aside contrasting the old `swap`/`JMPRET` idiom.
- **R2 — Cooperative yield in a long compute loop**: `TASKNEXT` cadence, `TASKID` tag.
- **R3 — Halt/resume flow control** (producer/consumer + synchronized start):
  `TASKHALT`, `TASKCONT`, `THISTASK`, `TASKCHK`.
- **R4 — Task-ID coordination + status dashboard**: scan 32 slots via `TASKCHK`, read
  `TASKHLT` bitmap (with the reversed-bit gotcha), `TASKSTOP(THISTASK)` shutdown.
- Optional capstone (cite the pattern): multi-cadence-on-one-bus (50/100/1 Hz sharing
  one I²C bus) from `spin2_cooperative_tasking.yaml` — ties to C3 (stack per task).

**Gotchas to carry (sourced from `spin2_cooperative_tasking.yaml`):** complete a
bus/resource transaction *before* yielding; a shared VAR is safe only if its value need
not span a yield (no flag reliance across a switch); a task halting itself
auto-`TASKNEXT`s; all-halted → waits for an interrupt; last task's return frees the cog.

**Integration points.** Forward cross-ref to **P2AN006** (how big must each task's
stack be?). Companion `p2an005-…yaml` composes: the 7 TASK method YAMLs + 2 constants
+ TASKHLT register (all as `cross_references.composes` links).

**Verification.** Every recipe compiles `pnut_ts -d` (probe each token's legality
individually first). **Exclude `TASKWAIT` pending its compile-probe (§4 F-196).**
Runtime scheduling/halt/free-on-return semantics are hardware-observed (Stephen runs
silicon externally) — cite v55 as documentary authority; do not invent per-method clock
timings. Normal: two tasks alternate. Edge: only-remaining-task `TASKNEXT` is a no-op;
`NEWTASK` returns −1 when 32 slots full. Error: a task that never yields starves siblings
(shown as the honest failure branch).

---

## §2 — P2AN006 · Sizing Cog & Task Stacks (C3, companion to C1)

**Why.** Both `cogspin()` (new-cog method) and `TASKSPIN()` (intra-cog task) require the
caller to hand over a hub-memory stack buffer, and the interpreter gives **zero overflow
protection** — an undersized buffer silently overwrites following hub memory, producing
"impossible" bugs. This note is the worked recipe that answers the question C1 raises,
and the P2 successor to AN019.

**Starting point (source-confirmed).** `deliverables/ai/P2/language/spin2/methods/
taskspin.yaml` (per-task stack) + `cogspin.yaml:47-55,231-236` ("Stack overflow is not
detected"); stack-packing rule `spin2-v55-text.txt:284` (params→results→locals in
declaration order); hub-vs-hardware-stack distinction `stack_operations.yaml:51-79`
(that YAML is PASM PTRA/PTRB + 8-level HW stack — a **different** resource; do not
conflate). **Centerpiece instrument** = Stephen's `isp_stack_check` (MIT), read-only
from the NO-COMMIT fodder `external-inputs/appNote-fodder-NO-COMMIT/stack/
isp_stack_check.spin2` + `…_UserGuide.md`. (No P1 AN019 content — P2-native; see D-3.)

`isp_stack_check` mechanism: fill every stack long with `NOT_WRITTEN_MARK $a5a50df0`,
place sentinel `DO_NOT_WRITE_MARK $addee5e5` in the long immediately after the buffer;
`checkStack` re-reads the sentinel (overwritten ⇒ overflow, halts the cog);
`getStackDepth` counts longs bottom-up to the first still-`$a5a50df0` long = high-water.
API: `prepStackForCheck` / `checkStack` / `getStackDepth` / `reportStackUse` (all take
`pStack`, `nStackLongCt` in **longs**).

**Target — shared base + 3–4 recipes:**
- Shared base: two stack contexts (new-cog stack vs intra-cog task stack), what consumes
  stack, why overflow is silent, the sentinel-fill measurement idea, the sizing method
  (start 128 → exercise fully → read high-water → cut to ~1.5× → keep `checkStack` in loop).
- **R1 — Instrument a new-cog stack** (three-phase: DAT stack+sentinel abutted →
  `prepStackForCheck` → `cogspin` → `checkStack` at loop top).
- **R2 — Find the high-water mark, then right-size** (`reportStackUse`/`getStackDepth`;
  the Init→exercise→read-high-water→cut flow, from the `isp_stack_check` UserGuide).
- **R3 — Pinpoint the overflowing routine** (granular `checkStack` after each init call).
- **R4 (task variant) — Size a TASKSPIN task stack** (same instrument on an intra-cog
  buffer; capstone showing the technique is stack-context-agnostic — it just watches a
  hub buffer; ties back to C1's per-task stacks).

**Honest framings (sourced).** `checkStack` detects "boundary crossed," not arbitrary
corruption (contiguous growth clobbers the sentinel first — detection is sound); the
instrument's shared DAT scratch is a **reentrancy hazard** if `checkStack` is called
from multiple cogs concurrently (note it / recommend locals) — cite as a caveat.

**Integration points.** Bidirectional cross-ref with **P2AN005** (C1's `cogspin`/
`TASKSPIN` sections point here for sizing; C3 assumes C1's launch mechanics + the
two-context model). Companion `p2an006-…yaml` composes: `taskspin.yaml`, `cogspin.yaml`,
relevant stack YAMLs. **Ship the `isp_stack_check` object** into `examples-library/`
(it's MIT, Stephen's — the note's own runnable artifact; note: this is a *deliberate*
inclusion of the object into the note's example library, distinct from the NO-COMMIT
raw fodder which stays untracked).

**Verification.** `isp_stack_check` and every recipe compile `pnut_ts -d` (it uses
`debug()` throughout — a plain compile is a false pass). Actual overflow detection +
the halt + the "48 and 32 crash!" discovery are hardware-observed; compile-cert is the
floor. Normal: `reportStackUse` prints "used N of M." Edge: sentinel exactly at boundary.
Error: undersized stack → sentinel overwritten → halt (the honest failure branch).

---

## §3 — P2AN007 · Data Structures with the New Language Facilities (C2)

**Why.** The Spin2 `STRUCT` facility ({Spin2_v45}) plus the worked *implementation* of
hub-shared cross-cog structures (FIFOs/queues/deques with indexing + locking) has
reference-only coverage and no guided home. P2 successor to AN003. **Implementation-layer
only** (D-4): the note codes the mechanisms; the *contract decision* stays with the
Architect's Guide.

**Starting point (source-confirmed).** `deliverables/ai/P2/language/spin2/keywords/
STRUCT.yaml`, `concepts/struct-bitfields.yaml`, grammar `spin2-v55-text.txt:36-37,202-256`;
comm-style mechanisms `architecture/decomposition/data-flow-contracts.yaml` +
`patterns/implementation/spin2_{latest_wins_mailbox,buffer_management,event_dispatcher}.yaml`;
locks `architecture/locks.yaml` + `methods/{locknew,locktry,lockrel,lockret,lockchk}.yaml`.
(No P1 AN003 content — P2-native; see D-3.)

STRUCT essentials: declared in CON, packed (no padding), members default LONG, typed
members (`WORD`/`BYTE`), arrays, nesting (unlimited), pointers `^struct` with auto-step
`ptr[++]`, `SIZEOF` {v45} / `OFFSETOF` {v53}, whole-struct ops (`:=` copy, `:=:` swap,
`~`/`~~` zero/set, `==`/`<>` compare), cross-object export {v49}, member bitfields {v54}.
Pass-by-value ≤15 longs. **Cross-cog gotcha:** a child method returning `^struct` needs
bracket-notation receipt `[pCfg] := obj.getConfig()` or >15-long structs throw a compile
error.

**Target — shared base + 4 recipes:**
- Shared base: STRUCT as an in-cog aggregate; the same type in hub RAM shared across
  cogs; the atomicity concern (single-long hub access is atomic → lock-free single-writer;
  multi-long updates need a lock + sequence-bumped-last).
- **R1 — In-cog STRUCT record + array** (`reading_t(LONG timestamp, LONG value, BYTE
  status)`, indexed access, `SIZEOF`, whole-struct copy).
- **R2 — Lock-free SPSC hub ring buffer, STRUCT elements** (power-of-2 `& MASK` indexing,
  producer owns head / consumer owns tail; basis `spin2_buffer_management.yaml`).
- **R3 — Latest-wins command mailbox with a STRUCT arg block** (`cmd_t` written first,
  `seq++` last, seq/ack handshake, **no lock**; basis `spin2_latest_wins_mailbox.yaml`;
  note this supersedes the blocking `spin2_mailbox_communication.yaml` toy).
- **R4 — Locked multi-writer queue** (STRUCT-element FIFO, `LOCKNEW`/`REPEAT UNTIL
  LOCKTRY`/`LOCKREL`, release-on-all-paths, ascending-lock-order; basis `locks.yaml`).
- Deque: shown as the ring/queue mechanism with push/pop at both ends (no new primitive).

**Cite-not-teach.** Which contract per seam, the three-planes framing, and
**refcount-vs-copy fan-out** (flagged irreversible in the YAML) → point to the Architect's
Guide + `data-flow-contracts.yaml`. Implement the mechanism; never code the design choice.

**Integration points.** Companion `p2an007-…yaml` composes: `STRUCT.yaml`, the lock
method YAMLs, the pattern YAMLs. Cross-ref to the Architect's Guide (contract decisions)
and — where a structure feeds a task — to C1/C3.

**Verification.** All four recipes are pure Spin2 → fully `pnut_ts -d` compile-certifiable
(verify STRUCT syntax, `SIZEOF`/`OFFSETOF`, pointer stepping, and the `[ptr] := obj.method()`
bracket form). **Do not** reference `spin2_shared_memory.yaml`'s P1 `lockset/lockclr`
(§4). Cross-cog atomicity/race-freedom is a runtime multi-cog property (compile proves
legality only) — assert only what's sourced; no invented `LOCKTRY` clock counts. Normal:
producer/consumer exchange records. Edge: ring full `((head+1)&MASK)==tail`. Error: torn
read without the lock (the honest failure branch, framed as *why* R4 needs the lock).

---

## §4 — P2KB correctness findings (log now; all YAML fixes DEFERRED to after PDF review)

Append to `engineering/operations/P2KB-CORRECTION-FINDINGS.md` from `F-196` as they
surface (logging is automatic — never gated). **No `.yaml` edits this sprint** — the
fixes are handed to a yaml-head pass once the three drafts are staged for PDF review.
The notes author *correctly against P2* independent of the register state.

| Proposed ID | Location | Defect | Status | Fix disposition |
|---|---|---|---|---|
| F-196 | `methods/taskwait.yaml` | `TASKWAIT` absent from v55 keyword table; YAML gives a 3rd signature matching neither v51 source; no `{Spin2_v47}` gate; carries forbidden interpreter `cycles:` | NEEDS-VERIFICATION | DEFERRED. Authoring: **compile-probe** `TASKWAIT` with `pnut_ts`; exclude from C1 if it fails. Register fix (stub invalid, like `taskresume.yaml`) → after PDF review |
| F-197 | `methods/taskspin.yaml` | `returns: void` omits the expression-return (task # or −1) form v55 documents | CONFIRMED | DEFERRED → after PDF review (note authors the correct form regardless) |
| F-198 | `methods/taskid.yaml`, `registers/taskhlt.yaml` | "main task is typically ID 0" is unsourced inference (v55 doesn't state it) | NEEDS-VERIFICATION | DEFERRED → after PDF review (soften/remove or HW-probe) |
| F-199 | `patterns/implementation/spin2_shared_memory.yaml` | uses P1 `lockset()`/`lockclr()` — **do not exist in P2**, would not compile | CONFIRMED | DEFERRED → after PDF review. Authoring: C2 uses the real P2 `LOCKTRY`/`LOCKREL`, never cites the P1 form |
| F-200 | `patterns/implementation/spin2_event_dispatcher.yaml` | correct only SPSC; races if used multi-producer — scope not stated | CONFIRMED | DEFERRED → after PDF review (yaml-head scope note) |

(`spin2_mailbox_communication.yaml` is already correctly marked `status: superseded` — no
finding; the notes just prefer latest-wins. The `isp_stack_check` UserGuide's
`getStackDepth`-omission is a defect in *Stephen's object doc*, not the P2KB — carry it as
an authoring note for C3, not a register finding.)

---

## §5 — Cross-cutting close: rosters, PDF, untrack fodder

**5a — Roster moves.** As each note's folder is stood up, move it Upcoming→In progress in
`PUBLICATION-ROSTER.md` (Type = app-note) and advance its Family C status in
`p2-app-note-roster.md` (`candidate → …authored`).

**5b — PDF production (all three).** Per `prepare-manual` + the Three-Folder Rule: refresh
each workspace from opus-master, clone the `p2kb-appnote-*` templates (incl. the shared
`p2kb-appnote-diagrams.sty` — task #160 propagation applies), escape LaTeX, stage **only
changed files** to `outbound/P2AN005|006|007/`, no ToC / no `--toc`. Leave all three staged
for Stephen to run on the Forge. (First render is a v0.1.0 draft-review PDF per note — the
XBYTE "stood up" bar.) Publish each `examples-library/` as `P2ANxxx-src.zip` at
release (release is a later step, not this stand-up sprint).

**5c — Untrack the mistakenly-committed fodder (final step).** Two tracked files under the
NO-COMMIT tree: `engineering/ingestion/external-inputs/appNote-fodder-NO-COMMIT/stack/
isp_stack_check.spin2` + `isp_stack_check_UserGuide.md`. `git rm --cached` both (keep on
disk), confirm `.gitignore` covers `appNote-fodder-NO-COMMIT/` so they stay untracked. Do
this **after** C3 authoring (the object ships as C3's own `examples-library/` copy — a
separate, deliberately-tracked artifact). Verify no other tracked file references the
fodder path.

---

## Verification model (whole sprint)

- **Code floor:** every embedded block + every `examples-library/*.spin2` compiles clean
  under `pnut_ts -d` (all three notes use `debug()`); K=76, no wrapped lines, inline code
  ASCII-only. Idioms validated against P2KB YAML before the compiler.
- **Empirical honesty:** runtime/multi-cog/overflow behaviors are hardware-observed
  (Stephen runs silicon externally). Notes show correct *behavior* and cite v55/KB as
  documentary authority; no invented timings, no imagined DEBUG captures. Anything
  requiring silicon to confirm is framed as such (→ EF ledger when a HW run is accepted).
- **Doc↔companion agreement gate:** each note's YAML companion must AGREE with its doc
  (composition, key params, gotchas) — digest+links, never a prose clone.
- **Audit:** each note is `document-audit`-ready via its MANUAL-DESCRIPTOR overlay before
  the draft PDF; the corrections drain gate applies at *release* (a later step).

## Exit state

Three notes stood up (folders + triad + roster moves), authored to v0.1.0 first-draft
(bodies + companions + examples, all `pnut_ts -d`-clean), **staged in `outbound/` for
Forge PDF generation**; all §4 findings logged (blocking ones resolved); the two stray
fodder files untracked. Green = all three prepared + staged; register current; fodder clean.
