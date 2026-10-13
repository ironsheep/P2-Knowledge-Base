# P2 Diagnostics Handbook — Planning (shape prototype)

**Status:** SHAPE PROTOTYPE, built 2026-10-12 for task «#428». Not a release.
**Working title / slug:** *P2 Diagnostics Handbook* / `p2-diagnostics-handbook` — both
are Stephen's call, confirmed or changed at the prototype review.
**What the review decides:** A1 (this one handbook, front door = Symptom Map) or A2
(separate notes + a map).

This file is planning, not reader text. It may name ledger ids and our own files;
the opus-master may not.

## 1. Decisions of record (Stephen, 2026-10-12, todo-mcp `debug_techniques_decisions`)

- Goal: stop agents and humans repeating weeks of debug traps.
- Q2 = A1: ONE diagnostics handbook, guide class. The **Symptom Map** is the front door
  and routes to **sections**, not chapters. Debug limits (HB-output) and rig supervision
  (HB-rig, Stephen's label "C4 rig supervision") are **parts**.
- Pin and streamer material goes to the *P2 I/O & Smart Pins User Guide* and the
  *P2 Streamer Programming Guide*; the handbook points there and does not duplicate.
- P2AN006 (*Sizing Cog & Task Stacks*) is kept as is (v1.0.2).
- Q4 = A: Part III "Trusting what you measure" carries the **P2-applied** method only;
  generic engineering method only where a P2 example needs it. `GENERIC-method`-only
  ledger rows are therefore NOT in this skeleton (Stephen: consider separately).
- The agent symptom-hub YAML is «#431», not this task.

## 2. Sources for the feed-mapping

- Claim ledger: `engineering/ingestion/sources/p2-debug-techniques/CLAIM-LEDGER.md`
  (DT-001..DT-411). Each row's **destination** column names HB-output / HB-rig /
  HB-trust (= this handbook's Parts I / II / III) or another home.
- Status letters below are the ledger's KB status: **C** COVERED · **P** PARTIAL ·
  **A** ABSENT · **X** CONTRADICTS · **AV** arbiter container-verified (arbiter column).
  The route after the comma is the ledger's verify route (container / source / XF /
  bench / n/a).
- **Verified** (usable in reader text) = C by a sourced KB page, or AV, or stated by an
  ingested Parallax source (Spin2 v55 text). XF-ungraded and bench-route claims stay out
  of reader text until «#429» grades them or a bench run settles them.

## 3. Falsification counts (the skeleton accounts for every HB row)

| Count | Value | How it is produced |
|---|---|---|
| Ledger rows (all) | 411 | `grep -o -E "^\| DT-[0-9]+ \|" CLAIM-LEDGER.md -c` |
| Ledger rows naming an HB part | **208** | `grep -c -E "^\| DT-[0-9]+ \|.*HB-(output\|rig\|trust)" CLAIM-LEDGER.md` |
| … of which ledger Part A / B / C / D / E | 43 / 57 / 34 / 35 / 39 | same grep restricted to each id range |
| Mapped to a handbook section below | **207** | hand count of §4 (Part I 43 + Part II 59 + Part III 105) |
| Deliberately routed elsewhere | **1** | DT-308 (below) |
| Mapped + routed elsewhere | **208** | equals the HB-tagged count |

**Routed elsewhere (with reason):**

- **DT-308** (`sed -i -E` differs between Linux and macOS). The ledger's own destination is
  "drop (host-tooling note, not P2); at most a one-line aside under HB-trust". It is a
  host-tool fact, not a P2 one, and Q4 = A keeps Part III P2-applied. If kept at all it
  is a one-line aside in Section 18.2 (its parent method, DT-307, is mapped there).

**Rows whose tag is HB but which sit in another part's section** (one primary home each,
to avoid saying the same thing twice): DT-372 and DT-373 (tagged HB-trust) sit in
Section 10.1 with their duplicates DT-256/DT-257 (tagged HB-trust + HB-rig). Rows tagged
with two HB parts are mapped once, to the section listed.

## 4. Skeleton — parts, chapters, sections, and what feeds each

Each section lists the ledger rows that feed it, as `id (status, route)`.
"Sample" marks Chapter 2, the one written chapter.

### Front door — Symptom Map

Three tables (*Nothing prints* · *The run looks stuck* · *The numbers look wrong*), 38
symptom rows, each routed to one or more **sections** by "Section N.M" (the platform
crossref filter links them, cell by cell, because crossref runs before tables in
`request.json`). The map is fed by the sections it routes to; it carries no claims of
its own (each row is a reader observation, not a cause).

### Part I — Getting Output Out (HB-output) — 43 rows

**Chapter 1: When Nothing Prints**

| Section | Feeds |
|---|---|
| 1.1 Two gates on every channelled statement | DT-027 (P, n/a) · DT-366 (C, n/a) · DT-105 (A, container) |
| 1.2 An object that was meant to be quiet | DT-006 (P, container) · DT-007 (P, container) · DT-361 (C, source v55) · DT-362 (P, n/a) · DT-363 (P, n/a) |
| 1.3 An object that cannot report | DT-068 (P, container) · DT-069 (A, n/a) · DT-062 (A, n/a) |

**Chapter 2: Staying Inside the Debug Limits** (Sample — written)

| Section | Feeds | In the sample text? |
|---|---|---|
| 2.1 Three limits, one listing | DT-044 (A, container) · DT-345 (P, source + bench) | held — see §5 |
| 2.2 When a limit is crossed | DT-039 (X→AV, container) · DT-347 (X→AV, container + bench) | loud-at-the-limit part USED; sub-limit soft zone HELD |
| 2.3 What counts as DEBUG data | DT-346 (C, container) · DT-348 (P, n/a) | 346 USED; 348 held |
| 2.4 Moving text out of debug() | DT-349 (C, container) · DT-350 (P, n/a) · DT-063 (P, n/a) | 349 USED; 350/063 held |
| 2.5 Fewer records | (no HB row; fed by drop-routed C rows DT-040, 052, 053, 054 — see §6) | USED |
| 2.6 Compiling less | DT-064 (A, container) · DT-011 (A, container) · DT-013 (A, container) · DT-364 (X→AV, container) | 364 USED as its verified inverse; 064/011/013 held |
| 2.7 Keeping a margin | DT-050 (P, n/a) · DT-051 (P, n/a) · DT-046 (A, XF) | 050/051 covered portion USED; 046 held |

**Chapter 3: Debug Output in a Large Program**

| Section | Feeds |
|---|---|
| 3.1 A formatter that writes into your buffer | DT-058 (A, n/a) · DT-059 (A, n/a) |
| 3.2 Shared scratch space | DT-060 (A, n/a) · DT-061 (A, container) |
| 3.3 One line, one statement | DT-057 (P, bench) · DT-351 (P, bench) |
| 3.4 A channel plan for a whole program | DT-103 (A, n/a) · DT-104 (A, n/a) · DT-109 (A, n/a) |
| 3.5 Checking a channel conversion | DT-108 (A, container) |

**Chapter 4: When the Printout Looks Wrong**

| Section | Feeds |
|---|---|
| 4.1 A printed value that does not match the program | DT-112 (A, XF) · DT-113 (A, XF) |
| 4.2 Two prints of one variable | DT-114 (A, XF) |
| 4.3 The last line of a run | DT-116 (A, XF) · DT-117 (A, XF) |
| 4.4 Output after a cog is stopped | DT-367 (A, bench) |

Part I count: 3+5+3 + 2+2+2+3+0+4+3 + 2+2+2+3+1 + 2+1+2+1 = **43**.

### Part II — Supervising a Run (HB-rig, "C4 rig supervision") — 59 rows

**Chapter 5: When the Output Stops**

| Section | Feeds |
|---|---|
| 5.1 Reading silence | DT-127 (A, XF) · DT-128 (A, n/a) · DT-129 (A, n/a) |
| 5.2 Where the last record ended | DT-130 (A, n/a) · DT-131 (P, bench) |
| 5.3 A heartbeat another cog can watch | DT-132 (A, n/a) · DT-133 (A, n/a) · DT-134 (A, n/a) |
| 5.4 Measuring below the debug path | DT-135 (A, bench) · DT-136 (A, bench) |

**Chapter 6: Making Every Exit Report**

| Section | Feeds |
|---|---|
| 6.1 End markers on every path | DT-137 (A, n/a) |
| 6.2 A cog whose top method returns | DT-139 (P, source v55) · DT-140 (A, n/a) |
| 6.3 Observers that time out on their own terms | DT-141 (A, n/a) |
| 6.4 Readings before stops | DT-090 (A, n/a) · DT-169 (A, n/a) |
| 6.5 Parking a cog for inspection | DT-091 (A, bench) · DT-092 (P, bench) |
| 6.6 Stopping a cog cleanly | DT-093 (A, bench) |
| 6.7 Lock allocation in a rig | DT-078 (A, n/a) |
| 6.8 Power cycles and independent runs | DT-142 (A, n/a) |

**Chapter 7: Instrumenting a Worker Cog**

| Section | Feeds |
|---|---|
| 7.1 A stack you own and can measure | DT-143 (C, source) · DT-165 (A, n/a) · DT-166 (A, n/a) · DT-167 (A, n/a) |
| 7.2 Asking a worker for its own diagnostics | DT-168 (A, n/a) |
| 7.3 Mailbox drivers and the stranded caller | DT-176 (A, n/a) |
| 7.4 Handshake sequence numbers | DT-177 (A, n/a) |
| 7.5 Publishing what is in flight | DT-178 (A, n/a) · DT-179 (A, n/a) |
| 7.6 Reading the phase word | DT-180 (A, n/a) |
| 7.7 An observer that needs no driver declaration | DT-181 (A, container) · DT-182 (A, n/a) · DT-183 (A, n/a) |
| 7.8 Watching mailbox invariants | DT-184 (A, n/a) · DT-185 (A, n/a) |

**Chapter 8: What an Instrument Costs**

| Section | Feeds |
|---|---|
| 8.1 Instruments in a timed path | DT-186 (A, XF) · DT-187 (A, n/a) |
| 8.2 Tiers of diagnostics | DT-188 (A, n/a) · DT-189 (A, n/a) |

**Chapter 9: Observing Without Driving** (points to the I/O & Smart Pins, Streamer and
PNut-Term-TS guides for the techniques; carries the supervision rules)

| Section | Feeds |
|---|---|
| 9.1 Pins every cog can drive | DT-193 (P, source silicon doc; XF) · DT-195 (A, n/a) |
| 9.2 Observers and pin ownership | DT-196 (A, n/a) |
| 9.3 The debug pins | DT-197 (C, container) · DT-207 (C, container) |
| 9.4 Landing pads and neighbouring pins | DT-201 (A, bench) · DT-206 (P, source hardware manual) |
| 9.5 Streamer capture in a debug build | DT-359 (C, n/a) · DT-382 (A, source + bench) |
| 9.6 A byte-level view of the link | DT-402 (A, source/bench) |

**Chapter 10: Injecting Faults and Sweeping Conditions**

| Section | Feeds |
|---|---|
| 10.1 Faults fed by a build flag | DT-256 (A, n/a) · DT-257 (A, n/a) · DT-372 (A, n/a) · DT-373 (A, n/a) |
| 10.2 The build-arm check in a rig | DT-241 (A, n/a) |
| 10.3 Sweeping phase and frequency | DT-235 (C, source silicon doc) · DT-324 (C, XF) · DT-325 (A, container) |
| 10.4 Test helpers safe to declare anywhere | DT-262 (A, container) |

Part II count: 10 + 11 + 15 + 4 + 10 + 9 = **59**.

### Part III — Trusting What You Measure (HB-trust, P2-applied) — 105 rows

**Chapter 11: The Debugger Is Part of the System**

| Section | Feeds |
|---|---|
| 11.1 What a debug build takes from your program | DT-001 (P, n/a) · DT-072 (P, n/a) |
| 11.2 Debug interrupts and timing | DT-024 (C, n/a) · DT-083 (P, bench) · DT-087 (A, bench) · DT-088 (A, bench) |
| 11.3 A pin the debugger reconfigures | DT-076 (P, XF) |
| 11.4 Timestamps across cogs | DT-033 (P, bench) · DT-034 (A, n/a) |
| 11.5 Stopping a cog in a debug build | DT-089 (A, XF; an open observation, no mechanism) |

**Chapter 12: Reading the Whole Transcript**

| Section | Feeds |
|---|---|
| 12.1 Printing a verdict twice | DT-115 (A, n/a) |
| 12.2 End markers and passing runs | DT-118 (A, n/a) · DT-119 (A, XF) · DT-138 (A, n/a) |
| 12.3 Reading the whole artifact | DT-120 (A, n/a) |
| 12.4 The chain between the chip and the log | DT-121 (A, n/a) · DT-122 (A, n/a) · DT-123 (A, XF) |
| 12.5 A transcript that looks empty | DT-124 (A, container) · DT-125 (A, n/a) |
| 12.6 Reconciling a byte dump | DT-126 (A, n/a) |

**Chapter 13: Proving a Build Arm**

| Section | Feeds |
|---|---|
| 13.1 What "compilation successful" tells you | DT-237 (A, container) · DT-352 (A, container) |
| 13.2 Comparing binaries between arms | DT-022 (A, container) · DT-025 (P, container) · DT-238 (A, container) · DT-239 (A, container) · DT-240 (A, container) · DT-353 (A, container) · DT-354 (A, n/a) · DT-357 (A, container) |
| 13.3 Flag implications | DT-242 (A, container) · DT-243 (A, n/a) · DT-369 (A, container) |
| 13.4 Code inside a closed conditional | DT-244 (A, container) · DT-368 (A, container) |
| 13.5 Flags and the declaring file | DT-246 (C, container) · DT-248 (A→AV, container) · DT-371 (A, n/a) |
| 13.6 An object that reports what it compiled | DT-250 (A, container) · DT-251 (A, container) · DT-252 (A, n/a) |
| 13.7 Guards that must stop the build | DT-255 (A, container) |

**Chapter 14: An Instrument You Can Believe**

| Section | Feeds |
|---|---|
| 14.1 Self-tests against published vectors | DT-279 (A, n/a) · DT-387 (A, n/a) · DT-388 (A, n/a) |
| 14.2 An instrument that has never reported a failure | DT-296 (A, n/a) · DT-298 (A, n/a) · DT-299 (A, n/a) · DT-399 (A, n/a) |
| 14.3 Positive controls for a capture path | DT-205 (A, XF) · DT-227 (A, n/a) · DT-232 (A, XF) |
| 14.4 Measuring the wrong thing | DT-210 (A, n/a) · DT-338 (A, n/a) |
| 14.5 Getters and plausible zeros | DT-190 (A, container) · DT-191 (A, n/a) · DT-192 (A, n/a) |

**Chapter 15: Records That Check Each Other**

| Section | Feeds |
|---|---|
| 15.1 What each integrity field can and cannot see | DT-280 · DT-281 · DT-282 · DT-283 · DT-284 · DT-389 · DT-390 · DT-391 · DT-392 (all A, n/a) |
| 15.2 Binding the sequence number into the check | DT-285 (A, n/a) · DT-393 (A, n/a) |
| 15.3 Payloads derived from the sequence | DT-286 (A, n/a) · DT-287 (A, n/a) · DT-394 (A, n/a) |
| 15.4 One record, two encodings | DT-288 (A, bench) · DT-289 (A, bench) · DT-395 (A, n/a) |

**Chapter 16: Finding the Real Writer**

| Section | Feeds |
|---|---|
| 16.1 Physical addresses and stray writes | DT-374 (P, source) |
| 16.2 Damage in a constant table | DT-291 (A, bench) · DT-292 (A, source silicon doc; negative claim, verify first) · DT-293 (A, bench) |
| 16.3 Instruments at the fault site | DT-294 (A, n/a) |
| 16.4 Stack readings you can trust | DT-147 (A, n/a) · DT-157 (P, n/a) · DT-171 (A, XF) — points to P2AN006 for the method |
| 16.5 Pin variables and sentinel values | DT-200 (P, n/a) — points to the I/O & Smart Pins guide |
| 16.6 Causes that come before main() | DT-213 (A, XF/bench) · DT-222 (A, n/a) |

**Chapter 17: Time, Clocks and Code Layout**

| Section | Feeds |
|---|---|
| 17.1 Waits longer than the timer reaches | DT-315 (C, n/a) |
| 17.2 Delays at a different clock | DT-316 (A, bench) · DT-318 (A, n/a) |
| 17.3 Effects at the top clock rate | DT-319 (A, bench) |
| 17.4 Code layout and results | DT-320 (A, bench) · DT-322 (A, n/a) |

**Chapter 18: Tests That Can Fail**

| Section | Feeds |
|---|---|
| 18.1 Asserting the number | DT-305 (A, n/a) · DT-306 (A, n/a) |
| 18.2 Asserting the effect | DT-307 (A, n/a) |
| 18.3 Timeouts from measured durations | DT-309 (A, n/a) |
| 18.4 Reference patterns | DT-310 (A, n/a) |
| 18.5 A pass in isolation | DT-311 (A, bench) |
| 18.6 Checking a compiler fix | DT-265 (A, container) |
| 18.7 Tools that refuse rather than report clean | DT-266 (A, n/a) · DT-397 (A, n/a) · DT-398 (A, n/a) · DT-401 (A, n/a) |
| 18.8 Code correct under both readings | DT-333 (A, n/a) |
| 18.9 Estimating a budget by hand | DT-049 (A, n/a) |

Part III count: 10 + 11 + 22 + 15 + 17 + 11 + 6 + 13 = **105**.

**Total mapped: 43 + 59 + 105 = 207.** With DT-308 routed elsewhere: **208 = the
HB-tagged count.**

### Where to Next

Pointers only, by official title: *P2 I/O & Smart Pins User Guide*, *P2 Streamer
Programming Guide*, *PNut-Term-TS User Guide*, *P2 Debug Window Manual*, *P2 Single-Step
Debugger Manual*, and the application note P2AN006 *Sizing Cog & Task Stacks*.

## 5. Chapter 2 — held out of the sample text (needs «#429» grading, a bench run, or a container check)

| Row(s) | What is held | Why | Route |
|---|---|---|---|
| DT-039, DT-347, DT-046, DT-345 | A sub-limit "soft zone": a `-d` build under the listing's maximum that downloads and prints nothing | Arbiter: "Loud at the cap, a silent soft zone below it; the threshold is unknown". The soft-zone evidence is bench/XF, not container; KB does not state it (struck as soft, compiler-version-specific) | «#429» (XF grading) + bench |
| DT-044 | A fixed DEBUG-data baseline spent before the first statement | ABSENT; container route not yet run; must never be stated as a figure | container (arbiter) |
| DT-064 | An arm that returns before a reporter still pays for the reporter's text | ABSENT; container route not run | container |
| DT-011, DT-013 | Forwarded-constant mask workaround; `-D` + `#ifdef` lighting a child's channels | 011 likely unnecessary (DT-010 AV shows the direct override works); 013 not run | container |
| DT-348, DT-350, DT-063 | "The cost is the repeated label text"; "gate, never delete the diagnostic" | PARTIAL: the KB states the DAT move, not these framings | n/a (judgement); may enter as method once Stephen accepts |
| DT-042 (support) | Splitting an over-size single record | PARTIAL: the m150 failure is covered; "split the line" is not | container |

Also held: the KB's `which_you_reach_first` note (records run out first for many short
statements, DEBUG data first for a few long lines). It is in the debug strategy guide but
has no ledger row, so the sample states the two underlying facts (each distinct statement
is a record; literal text is DEBUG data) and lets the reader draw it. Arbiter's call
whether a KB statement without a ledger row is "verified".

## 6. Chapter 2 — sentence trace (every sentence of fact → its source)

Sources: **DS** = `deliverables/ai/P2/language/spin2/debug-commands/debug-strategy-guide.yaml`
(sourced to Spin2 v55 + pnut-ts 1.55.8 listing/compile behaviour, observed 2026-10-07).
**v55** = `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` (Parallax Propeller 2
Spin2 Language Documentation v55), by line. Ledger rows marked **drop** are routed "drop
(already in DS)" in the ledger — not new KB content — and are cited here only as the
verified status of the fact. "Corroborated" = my own `pnut-ts 1.55.8 -d -l` compile of the
chapter's example files (scratch copies), never the authority.

| # | Sentence (opening words) | Trace |
|---|---|---|
| I-1 | "Every debug build has limits, and a program that keeps adding debug output eventually meets them." | DS `the_compilers_limits`; DT-038 (C, drop) |
| I-2 | "They belong to the compiler, they can change from one release to the next, and the compiler reports them every time you ask." | DS `description`, `how_you_find_out`; DT-037 (P — covered portion: "read the current figures from the compiler's own listing"); DT-048 (AV) |
| 2.1-1 | "The compiler limits three things about a debug build:" (records / one record / total) | DS `what_is_limited`; DT-037 (P — the three limits are named; figures deliberately absent); DT-038 (C, drop); DT-042 (P — the one-record limit, m150, covered) |
| 2.1-2 | "A record is what one `debug()` statement compiles to." | v55:909 ("the BRK instruction is used to interrupt and select the particular DEBUG() statement definition"); v55:1067 |
| 2.1-3 | "When a cog reaches the statement, a `BRK` instruction selects that statement's record, and the debugger looks the record up and sends the message it describes." | v55:909; v55:1067 ("unique BRK code ... used as an index to look up the specific record in the DEBUG() database ... from which the debugging program reads its commands"); v55:897 ("outputs the message for that statement") |
| 2.1-4 | "The records are stored with the debugger, at the top of hub RAM, rather than in your program's code." | v55:901 ("stored within the debugger image in the top 16 KB of RAM, minimizing impact on your application code") — the figure is not carried |
| 2.1-5 | "The listing reports both totals, on the lines `DEBUG records:` and `DEBUG data:`, each with the current usage and the current maximum." | DS `how_you_find_out`; DT-048 (AV: "read 'DEBUG data:' from the -d -l listing"). Corroborated: both lines present in all seven listings |
| 2.1-6 | "Read the maximums there, from the compiler you are using, and never from a document, this one included." | DS `how_you_find_out` ("read them from your compiler, never from a document"); DT-037 (P — covered portion) |
| 2.1-7 | "Do not estimate DEBUG data from the size of the binary. The difference ... includes the debugger itself, which is present even when the program has no debug statements at all." | DT-048 (X→AV: "KB right. The -d/non-d delta includes the debugger image"); DS `binary_size_is_not_the_measure` |
| 2.1-8 | "Without `-d`, the compiler ignores every debug statement and includes no debugger, so a release build needs no statements commented out." | DT-003 (C, drop); v55:904 ("ignored by the compiler when not compiling for DEBUG mode, so you don't need to comment them out") |
| 2.2-1 | "Past a limit, the build fails at compile time." | DT-038 (C, drop); DT-039 (AV: "Past the compiler's maximum the build fails LOUDLY (m151)"); DS `how_it_fails` |
| 2.2-2 | "The compiler stops with "DEBUG data is too long" and gives the reason: too many records, one record that exceeds its size, or a total that exceeds the maximum." | DS `how_it_fails` (m153 / m150 / m151); DT-038 (C); DT-042 (P — m150 covered); DT-039 (AV) |
| 2.2-3 | "Whichever it is, take the maximum from the listing." | Arbiter probe P12 (§6a). The earlier sentence on the m151 message's figure was removed: a one-version tool quirk, not intent — filed as PNut-TS punch-list item 13 |
| 2.3-1 | "DEBUG data is the literal text inside `debug()` statements, the labels that the labelled output commands print, and an overhead for each statement." | DT-043 (C, drop: "literal format strings inside debug() plus per-statement overhead"); DS `what_debug_data_counts` (labels) |
| 2.3-2 | "The labelled commands print the source of what they show as well as its value: `debug(uhex(x))` prints something like `x = $ABC`." | v55:915 |
| 2.3-3 | "To print that label, the record stores the name `x`." | DT-053 (C, drop: DS dedup rule "the labelled UDEC stores the expression's name") |
| 2.3-4 | "Every output command also has a value-only form, whose name ends in an underscore ..., which prints only the value and stores no name." | v55:918, v55:1001; "stores no name": DT-053 (C — same DS rule: "The value-only UDEC_(x) and UDEC_(y) store no name") |
| 2.3-5 | "Strings kept in a `DAT` block are not DEBUG data. Printing one with `zstr_()` leaves only the command bytes in the record." | DT-043 (C, drop); DT-346 (C); DS `what_debug_data_counts` |
| 2.4-1 | "Move the text into `DAT` and print it with `zstr_()`, and the text leaves DEBUG data entirely" | DT-041 (C, drop); DT-055 (C, drop); DS `over_on_bytes.fix`. Corroborated: 76 → 4 bytes |
| 2.4-2 | "The value-only commands store no name, and `zstr_()` does not store the pointer it is given, so the two statements ... are identical and the compiler keeps one record for both." | DT-055 (C — DS `helps_both`); DT-056 (C — DS `over_on_records`: "the zstr_ pointer is not stored"); DT-053 (C). Corroborated: 2 → 1 records |
| 2.4-3 | "Build the line in a hub byte buffer, from labels kept in `DAT` and digits your own code writes, and print it with a single statement" | DT-055 (C: "labels live in DAT, not charged"); DT-349 (C) |
| 2.4-4 | "`lineChar()` stops at `LINE_MAX` ... and `lineDec()` handles only values that are not negative." | describes the example's own code (read it) |
| 2.4-5 | "However many places in a program call `lineEmit()`, its one `debug()` statement is one record." | DT-056 (C — DS: "one record no matter how many call sites emit it"). Corroborated: 1 record |
| 2.5-1 | "Each distinct `debug()` statement is a record, and the compiler merges statements that are byte-for-byte identical, wherever in the program they appear" | DT-052 (C, drop — DS `deduplication.rules`: "Identical debug() calls in different locations share ONE record") |
| 2.5-2 | "The two `debug("tick")` statements share one record." | DT-052 (C) |
| 2.5-3 | "Printing `x` and `y` from one statement takes one record, where printing them from two statements takes two." | DT-040 (C, drop — DS `over_on_records.also_helps`) |
| 2.5-4 | "The last two statements look alike but are different records, because each labelled `udec()` stores the name of what it prints." | DT-053 (C) |
| 2.5-5 | "Five statements, four records" | derived from 2.5-2..4. Corroborated: 4 records |
| 2.5-6 | "two ways to spend fewer records: make statements identical ..., and merge statements that report together." | DS `over_on_records` (fix + also_helps); DT-040, DT-052, DT-053 (C) |
| 2.5-7 | "`DEBUG_COGS` and an `IF()` inside `debug()` decide at run time whether a message goes out, but the record is compiled either way." | DT-054 (C, drop); v55:931 (IF gates output) |
| 2.6-1 | "The compile-time switches remove statements from the build altogether." | DT-054 (C — "only -d, DEBUG_DISABLE or masked debug[N]() help"); DS `mechanisms_overview` |
| 2.6-2 | "Setting `DEBUG_DISABLE` to any non-zero value removes every debug statement in the file that defines it." | DT-004 (C, drop); v55:1028 |
| 2.6-3 | "give each subsystem a channel" | DT-102 (C, drop); DT-066 (C, drop) |
| 2.6-4 | "a statement on channel `N` is compiled only if bit `N` of the mask is set." | DT-100 (C, drop); v55:1027 |
| 2.6-5 | "Channels run from 0 to 31, and naming them with constants keeps the mask readable" | DT-016 (C, drop); v55:1027 ("(0..31)"); DT-097 (C, drop) |
| 2.6-6 | "A plain `debug()` statement ... is compiled in every `-d` build that `DEBUG_DISABLE` has not switched off, even when `DEBUG_MASK` is 0." | DT-005 (C, drop); DT-361 (C); DS `critical_note` ("compile whenever -d is used and DEBUG_DISABLE is not set") and `common_mistakes` |
| 2.6-7 | "`debug[N]()` needs `DEBUG_MASK` to be defined; without it, the build fails." | DT-014 (C, drop) |
| 2.6-8 | "Keep plain `debug()` for the few lines that must always print ... put everything else on a channel." | DT-067 (C, drop); DT-008 (C, drop) |
| 2.6-9 | "Channels need no version directive." | DT-015 (C, DM); DT-094 (X→AV: "KB right"). Corroborated: every example compiles with no `{Spin2_vNN}` |
| 2.6-10 | "The mask belongs to the file that defines it, so a parent's mask does not reach a child object, and a child that defines `DEBUG_MASK = 0` adds no records and no DEBUG data." | DT-009 (C, drop); DT-045 (C, drop). Corroborated: no-override control = parent's 1 record / 11 bytes only |
| 2.6-11 | "A parent can still turn a child's channels on, by setting the child's mask where it declares the object" | DT-010 (X→AV: "`OBJ c : "child" \| DEBUG_MASK = %1` compiles and enables the child's channel 0"); DT-364 (X→AV, same). Corroborated: 1 → 2 records |
| 2.6-12 | "Records belong to the whole program. Once the child's channel is on, its statement counts against the same totals as the parent's" | DT-106 (X→AV: "records are program-wide"). Corroborated: 1 → 2 records, 11 → 28 bytes |
| 2.6-13 | "A reusable object should not spend its user's limits by default. Set `DEBUG_DISABLE = 1` in it, or put its statements on channels and document which channel is which." | DT-065 (C, drop — DS `decision_guide`: reusable object) |
| 2.7-1 | "Treat the listing's maximums as ceilings, not targets." | DS `stay_well_inside`; DT-050 (P — covered portion only: "keep a margin below the maximum") |
| 2.7-2 | "A program that compiles right at a maximum has no room for its next statement, and a newer compiler may draw the limits differently." | DS `stay_well_inside`, `common_mistakes` ("Treating the listing's maximum as a target"); DT-050 (P — covered portion) |
| 2.7-3 | "Watch both listing lines as the program grows, and apply the techniques in this chapter before you need them." | DS `which_you_reach_first` ("Watch both lines of the listing"), `stay_well_inside` ("use the techniques below before you need them"); DT-051 (P — covered portion: "read the listing") |
| 2.7-4 | "Chapter 11 covers what else a debug build takes from the program it is built into." | DS `what_a_debug_build_takes_from_your_program`; DT-001 (P — the costs are listed) |

Code comments inside the examples restate 2.5-2..4 (`ch02-share-records`), 2.6-4/2.6-6
(`ch02-channels`) and 2.6-10/2.6-11 (`ch02-sensor-driver`, `ch02-light-a-child`).

**Judgement calls flagged for the arbiter:** rows used through their **covered portion
only** while the row as a whole is PARTIAL — DT-037, DT-042, DT-050, DT-051, DT-001. Strike
any the arbiter does not accept as "verified"; each is one sentence.

## 6a. Independent verification of Chapter 2 (arbiter, 2026-10-13; cover build date moved to 2026-10-13 with the render)

A fresh read-only checker, given the text and the sources and not this trace, re-verified every
fact sentence under the clean-room rule: **no KB (DS) and no p2kb-mcp as evidence** — v55 text,
`pnut-ts 1.55.8 -d -l` listings and the bench ledgers only. Where it could not build a probe, the
arbiter compiled one (scratch, `pnut-ts -d -l <probe>.spin2`, counts from the `.lst`):

| Probe | Claim (trace row) | Result |
|---|---|---|
| P1 `debug[0]` with no `DEBUG_MASK` | 2.6-7 | `error:DEBUG_MASK symbol must be defined for DEBUG[0..31] usage` |
| P2 `DEBUG_MASK = 0`, one plain + one `debug[0]` | 2.6-6 | 1 record: the plain statement compiles, the channelled one does not |
| P3 no debug statements, `-d` vs plain | 2.1-7 | 9226 vs 6292 bytes, 0 records / 0 data: the debugger is present |
| P5 parent + child with `DEBUG_MASK = 0`, no override | 2.6-10, 2.6-12 | parent's 1 record only (override: 2) |
| P6 `debug(if(x), udec(x))` + `debug(udec(x))` | 2.5-7 | 2 records: the `IF()` statement is compiled |
| P8 `debug("tick")` in two methods and a child object | 2.5-1 | 1 record (control, one statement: 1) |
| P9 `DEBUG_DISABLE = 1` | 2.6-2 | 0 records / 0 data |
| P10 one statement with 300 literal chars | 2.1-1, 2.2-2 | `DEBUG data is too long: record exceeds 255 bytes (m150)` |
| P11 256 distinct statements | 2.1-1, 2.2-2 | `DEBUG data is too long: too many records: max 255 (m153)` |
| P12 200 statements of 90 chars | 2.1-1, 2.2-2 | `DEBUG data is too long: total exceeds 16384 bytes (m151)` |

Also from the checker: v55:915 (`x = $ABC`), v55:920/931 (`IF()` gates output at run time), v55:1001
(value-only forms), v55:1027-1028 (mask, `DEBUG_DISABLE` per file/object), v55:1067 (records at the
top of memory); all seven examples compile; every fence is identical to its file. **Verdict: every
fact sentence in Chapter 2 is verified without the KB.** Its omission flag (the sub-cap "downloads
and prints nothing" zone, DT-039/347) is rejected for the reader text: struck by Stephen as soft and
compiler-version-specific (VO-J-027), so it stays held in §5.

## 7. Examples (Chapter 2)

All in `examples-library/`, byte-identical to their code blocks (headers generated by
`sync-manual-examples.py`), K = 76 (the
family's platform budget, as the XBYTE and Getting Started descriptors carry). Each
compiled with `pnut-ts -d -l` 1.55.8 (scratch copies; no `.bin` kept in the tree):

| File | Records / DEBUG data in its listing (pnut-ts 1.55.8) |
|---|---|
| `ch02-text-inline.spin2` | 2 / 76 bytes |
| `ch02-text-in-dat.spin2` | 1 / 4 bytes |
| `ch02-line-buffer.spin2` | 1 / 3 bytes |
| `ch02-share-records.spin2` | 4 / 26 bytes |
| `ch02-channels.spin2` | 3 / 22 bytes |
| `ch02-light-a-child.spin2` (+ `ch02-sensor-driver.spin2`) | 2 / 28 bytes; without the override (scratch control) 1 / 11 bytes |

These figures are planning evidence only and never enter the reader text.

## 8. Open for the review

1. **A1 or A2** — the purpose of this prototype.
2. **Title and slug** — *P2 Diagnostics Handbook* / `p2-diagnostics-handbook` is a working title.
3. **Part II name** — Stephen's label is "C4 rig supervision"; the reader title used is
   *Supervising a Run*. Confirm or rename.
4. **Unwritten chapters in the render** — they appear as headings plus a one-line purpose so
   the Symptom Map's section links resolve and the TOC shows the full shape. Keep that form
   for later drafts, or show only written chapters?
5. **Size** — 18 chapters, 97 sections, 207 rows. If that reads as overload, the cheapest
   cut is folding Chapter 8 into Chapter 7 and Chapter 15 into Chapter 14.
