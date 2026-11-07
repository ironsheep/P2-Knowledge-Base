# P2KB Correction Findings — Archive: closed 2026-11-07, KB findings served and owing only their register closure

**This is an archive, not the register.** It holds the findings closed on 2026-11-07, after the document pass: F-637, F-636, F-569, F-567, F-564, F-545, F-377, F-375, F-372, F-361, F-359, F-352, F-347, F-337, F-320. The live register is `engineering/operations/P2KB-CORRECTION-FINDINGS.md`, and it carries open work only. The text below is each entry as it stood at closure, with its status and the closing note updated. Earlier text is in git.

### F-637 — `qmul.yaml` says Spin2 operators are already protected by the interpreter — `RESOLVED` (found 2026-11-06, the document pass's class search; closed 2026-11-07)
> **Closed 2026-11-07:** Served in v1.25.4 and read live; the tree at v1.25.5 carries it.
`language/pasm2/qmul.yaml:142`, the last of the wording `cordic_solver.yaml` dropped in v1.25.2. Spin2 v55 says the interpreter "accommodates interrupts and only stalls them briefly" and does not speak of the CORDIC window.
> **Applied 2026-11-06, widened by the v1.25.4 audit:** v55's sentence sits in the list of what in-line and CALLed PASM may do, and says nothing of CORDIC or operators. Beside a CORDIC window it still read as "Spin2 CORDIC is safe", so it moves to its own home, `spin2/constructs/inline_pasm.yaml` `interrupts`, and goes from `qmul.yaml` and both `cordic_solver.yaml` pages; "Spin2 code" comes off `when_unnecessary`. `spin2/concepts/cordic_solver.yaml` drops the same claim in other words ("handle all timing and synchronization automatically", "No timing concerns", "interpreter handles everything", "Automatic timing management", "handled efficiently", the key `automatic_management`, now `calling_the_methods`), "All operations use dedicated CORDIC hardware", the two unsourced speed comparisons and "Full 32-bit precision", which becomes the Silicon Doc's "32-bit, pipelined CORDIC solver with scale-factor correction". Documents follow: Assembly §5.1.8, `REP`, `instructions-q.md`, `instruction-categories.md`, and P2AN002 `:326`, each stating the pattern for PASM2 with interrupts enabled.

### F-636 — two leftovers of F-632's class, seen reading the pages live on v1.25.1 — `RESOLVED` (found 2026-11-06, «#440», v1.25.1 content probe; closed 2026-11-07)
> **Closed 2026-11-07:** Served in v1.25.2 and read live; `until ret` and `Consider interrupt latency` occur nowhere in the tree at v1.25.5.
`cordic_solver.yaml` `extended_protection.description` said "until ret", where `rep_instruction.yaml` now says "a branch, such as _ret_". `setq_block_ops.yaml` `best_practices` said "Consider interrupt latency impact", the same unsourced advice as the removed "Keep transfers small".
> **Applied 2026-11-06, uncommitted:** both changed in the tree. They ship with the next KB release. The Assembly Reference's "first `ret`, `_ret_`, or branch" stands: it names a branch generally, and `ret.yaml` is category Branch.

### F-569 — the new provenance-key gate's census: three provenance keys still reach agents, and the OBEX tooling it touched has two defects — `RESOLVED` (found 2026-10-10, «#422»; closed 2026-11-07)
> **Closed 2026-11-07:** All parts done. The compile-record item closed with CP-029; `combinations_are_compiler_verified`, `base_pin_options_provenance` and `last_scraped` occur nowhere in the tree at v1.25.5.
> **Applied 2026-11-06:** the last served key is gone: CP-029 records the clock-setup forms, `clock_setup.source` cites it, `combinations_are_compiler_verified` and the gate's `open` line are deleted.
Found building F-545's gate (`audit-yaml-provenance-key-names.py`, kind `open`). Each is understood but
needs a call or a record that is not in hand:
- **`last_scraped`** in OBEX `version_tracking` (130 files): a scraper timestamp served to every OBEX
  lookup. By Stephen's rule (F-545) it is tracking data; moving it under `scrape_tracking` collides
  with the `last_scraped` 17 files already carry there, so it needs a new tracking name or a second
  filtered name — **Stephen's call.** The writer is `scrape-obex-repos.py`.
  **APPLIED 2026-10-10 (Stephen: "a"):** moved into `scrape_tracking` as `version_last_scraped` in all
  130 OBEX objects (the filter list does not grow); `scrape-obex-repos.py` writes it there; the gate's
  `open` line is deleted. Done by script under the new doctrine *A scripted change is done only when
  an audit proves it changed nothing else*: an independent audit against HEAD passed for all 130 —
  parsed data equal to before with exactly that key moved and its value unchanged, the diff exactly
  one line out and one line in, and no file outside the OBEX objects touched. The same parse audit was
  then run on the earlier 173-file `metadata:` → `scrape_tracking:` rename (`c5c5367f`): every file's
  data equal to before apart from the key name; the template's other difference is the deliberate
  removal of its empty `notes:` block.
- **`base_pin_options_provenance`** (`hardware/addon-click-adapter.yaml:42`): provenance prose served,
  and it says the value it annotates (`base_pin_options: [0, 16, 32, 48]`) is stated by no source — it
  is inferred from the other dual-header boards and a driver enum. The same `[0, 16, 32, 48]` is on
  `addon-motor-driver.yaml`, `addon-hyperram-hyperflash.yaml` and `hub75_adapter.yaml`; whether each is
  sourced (board guide, schematic, or the P2 Eval Board guide's header layout) is **not yet checked**.
  Fix: check the class against the guides; cite or mark unknown; drop the provenance key.
  **APPLIED 2026-10-10.** Stephen explained it: the Eval Board's headers are used alone, one per 8-pin
  group, or in pairs that form the 16-pin groups. The Eval Board Rev C guide shows it: the board
  photograph, p.1, silkscreens P0-P7 beside P8-P15, P16-P23 beside P24-P31, P32-P39 beside P40-P47 and
  P48-P55 beside P56-P63 (one pair per side), and 11. I/O Pin Breakout Edge Headers, p.9, says each
  header carries one group of eight. So `[0, 16, 32, 48]` is right for the four dual-header boards
  (click, motor driver, HyperRAM/HyperFlash, HUB75): each now says why in `base_pin_note` and cites the
  guide in `pin_group.source`; the click page's `base_pin_options_provenance` (inference from sibling
  boards and a driver enum) is removed. Class widened: the 11 single-header boards' `[0, 8, … 56]` had no
  citation either; `pin_group.source` added to each by script, audited against HEAD (parsed data
  equal plus that one key; diff exactly one added line; no other file touched).
  **Widened the same day (Stephen: P56-P63 "are dedicated and would interfere with the function of
  the eval board"):** all 15 pages offered base 48 (16-pin) or 56 (8-pin) with no warning. Each now
  carries `pin_group.p56_p63_caution` — P58-P61 boot flash / microSD SPI, P62/P63 PC-USB serial, every
  pin an on-board LED, P57 optionally the LDO enable; P0-P55 the fully free pins — and its source adds
  the guide's I/O Pin Assignments table, p.15 (script + audit as above: 15 files, data equal plus the
  two intended changes, diff exactly those 3 lines). `hardware-compatibility-matrix.yaml` said
  "64 (all accessible)" available for add-ons and "any of the 8 header positions"; it now gives 56
  fully free, a `dedicated_group` line, the header pairs, and a block `source:`.
- **`combinations_are_compiler_verified`** and `errfreq_is_optional`'s "confirmed to compile"
  (`guides/pasm2-getting-started.yaml:105-107`): compile results served as prose with no CP record.
  Fix: record them as CP-NNN in `COMPILE-PROOFS.md`, cite in `source:`, state the fact only.
- **OBEX tooling:** `engineering/tools/obex-integration/obex_discovery.py` does not compile at HEAD
  (`185ff1c58`): the file is cut mid-method at `:128` (an unterminated `re.compile(r'/obex/[^/]+/`) and a
  method body is lost. Not reconstructed (the lost text is unknown). `obex_discovery_fixed.py` sits beside
  it. **Also** `scrape_tracking.created_date` disagrees with `version_tracking.obex_upload_date` in
  OBEX 4800 and 4926 (`2024-07-09` / `2026-05-06`; `2025-04-07` / `2026-05-08`); only the latter is
  served. And `original_archiver_name` (now filtered) carried one credit that is nowhere else on its
  page: OBEX 2816, "based on BR's original in the Propeller 1 Object repo".
  **APPLIED 2026-10-12 (KB v1.24.4, Stephen: "pure mirror"):** all three parts are gone.
  - `obex_discovery.py` and the other 28 scripts from 2025 are retired to the local `archive/`.
    Discovery is now `obex-catalog-mirror.py discover`, proved live: 130 object pages listed, 0 new.
  - `scrape_tracking` is removed from every object. Each date is now the catalog's own, from the
    Object ID line: 4800 is `2026-05-06` and 4926 is `2026-05-08`.
  - The 2816 credit was in fact on its page: the catalog's Author line reads "Dennis Gately based on
    BR's original in the Propeller 1 Object repo", and the mirror serves it as `author`.

  Closes with the v1.24.4 release; the compile-record item above stays open.

### F-567 — `hardware/hub75_adapter.yaml` is an Iron Sheep board no Parallax document describes, so it fails the claim-sourcing gate (3 Tier 1) and the source-lock ratchet — `RESOLVED` (applied 2026-10-10, «#422»; Q-012 answered the same day; closed 2026-11-07)
> **Closed 2026-11-07:** Served; `audit-yaml-claim-sourcing.py` reads 0 Tier 1 across the tree on 2026-11-07, and Q-012's answers are applied.

> **Q-012 answered and applied 2026-10-10 («#422»).** Stephen confirmed (a) the host boards, (b) the
> address lines per panel height, (c) female pass-through headers and (d) retiring / limited stock, and
> chose to remove (e). Recorded in the designer's statement (*Product facts confirmed*). In
> `hub75_adapter.yaml`: `description`, `specifications` and `sources` cite the statement for (a)–(d);
> the derived "8/16/32 row scan" figures are removed (he confirmed panel heights, not scan ratios),
> as are `supported_panels` (scan rates incl. "1:4", resolutions, pixel pitches), `compatibility`
> (a second, unconfirmed host list incl. "any P2 board with 16 consecutive pins", and a toolchain
> list), the scan / daisy-chain / 18 AWG notes, "0.1 inch spacing" and "P16-P31 is the most common"
> (in no source), and `references:` (two generic pointers, no document). Class search: no other KB
> file carries the removed HUB75 claims (`grep -i hub75|64032` over `deliverables/ai/P2`: the
> compatibility matrix, `p2-eval-board.yaml`, `addon-click-adapter.yaml`, `muxq.yaml`, OBEX 2850 and
> 4616 — none states them).

> **DECIDED by Stephen 2026-10-10.** His own hardware documents and hand measurements are golden
> sources ("cite me as the source"); an ingestion run may rewrite the data it produces. **Applied
> 2026-10-10 («#422»):** the schematic *HUB75E Adapter for P2 Eval* H/W Rev 1.4 (2020-11-25) was
> ingested (`sources/p2-hub75-adapter/`, audit of record `p2-hub75-adapter-complete-extraction-audit.md`)
> with a dated designer's statement for size / current / clock; the three 2025 captures are retired
> to `archived/` (6 of their claims proven wrong). Both gates accept the two documents as a new
> acceptance class (`audit-yaml-claim-sourcing.py` CANONICAL_TITLES rows `p2-hub75-adapter`,
> `p2-hub75-adapter-designer`, with pass and refuse controls; `AUTHORITATIVE-SOURCES.md` admission
> route 2). **YAML corrected from the schematic:** 5 V does NOT reach the HUB75 connector (the file
> said it did); offsets 14/15 are spares brought out on J4 (direct) and J5 (5 V-buffered), not
> "not connected"; added the two 74HCT244 buffers with output enables tied low, the J3 probe header,
> J6 (HUB75 pin 4), the HUB75E pin-8 = E pinout and the lower-header-only 5 V input. **Class search:**
> `hardware/hardware-compatibility-matrix.yaml` repeated "offsets 14-15 unused" and is fixed;
> `p2-eval-board.yaml` and `language/pasm2/muxq.yaml` mention the board without a wrong claim.
> **Gates:** claim sourcing PASS (0 Tier 1); source lock exit 0, hub75 RESOLVABLE→NAMED replaced
> by CANONICAL (673 CANONICAL / 7 NAMED). **Still open:** host-board list, address-line → panel-row
> mapping, "female pass-through" headers, retiring status, and the generic panel lists
> (`supported_panels`, `compatibility.operating_systems`, panel-wiring note) are not in the schematic.
> Asked of the designer as Q-012 (`KNOWLEDGE-GAPS.md`).
Found 2026-10-10 by «#422» and carried through «#423»'s exit baseline. `audit-yaml-claim-sourcing.py` (Tier 2
blocking since 89eb8c02) reports 3 Tier-1 blocks in this file — `description` (`:19`, 2 quantities in V),
`specifications` (`:29`, 5 quantities in MHz, V, mA), `notes` (`:61`, 3 quantities in MHz, V) — "this file DOES
cite elsewhere, its own other sections are the control". `audit-yaml-source-lock.py` reports `WEAKENED:
hardware/hub75_adapter.yaml  RESOLVABLE -> NAMED` against `baselines/yaml-source-lock.json`, because the
citation rule (a canonical Parallax title with its edition, an EF/CP/XF id, a pinned listing, an OBEX id)
cannot be met by a document the board's designer wrote: the file itself says "Every figure in this file is
the board designer's own; no Parallax-published document describes this board" (`:15-16`). These two
failures are the **only red in the close-out exit baseline** (`validate-dod-release.py`). The file is left
exactly as it is and the ratchet baseline is not re-recorded. **The call is Stephen's:** teach both gates
a way to cite a designer-authored specification of a non-Parallax board (a new acceptance class, which
changes what "cited" means), or remove the quantities the gate names, or move the board out of the served
tree. Until he decides, the release cannot go green.

### F-564 — what a stopped cog leaves on the pins and in smart-pin modes is stated nowhere in the ingested sources; `cogstop.yaml` shipped three claims about it — `RESOLVED` (bench question; closed 2026-11-07)
> **Closed 2026-11-07:** Answered by EF-105 and served in v1.25.5; `cogstop.yaml`'s `pin_state_after_stop` read live 2026-11-07.
> **Answered 2026-11-06, EF-105:** a stopped cog no longer drives a pin. A smart pin it configured keeps its configuration, and goes quiet only when no cog holds its DIR high. `cogstop.yaml` says so.
Found 2026-10-09 by «#414» fixing `language/spin2/methods/cogstop.yaml`. The page shipped "All pins
controlled by the cog are released to float state", `pin_control: All DIR bits cleared (pins become
inputs) / Smart pin modes disabled / Pin states float`, "Cog RAM contents preserved but inaccessible",
"Power saving (stopped cogs use less power)" and the warning "Pins float - may need external
pull-up/down resistors". Checked 2026-10-09: the P2 Documentation v35 says only that a stopped cog
returns to the pool of free cogs (`silicon-doc-text.txt:364`, `:421-431`) and that a held lock is
released (`:3688`, `:3698`); the Datasheet's COGSTOP row says "Stop cog D[3:0]"
(`p2-datasheet-text.txt:1790`); the v55 interpreter's `cogstop` is the instruction itself; no EF
entry observes pins after a COGSTOP (the only COGSTOP in the ledger, EF-087, is a rig step). A smart
pin keeps its own mode register, so "Smart pin modes disabled" is doubtful. **Applied now:** the
claims are removed; the page says the pin and smart-pin state after a stop "is not established by an
ingested source; do not rely on it", and keeps the sourced `WAITX #20` before a self-stop after
`WRFAST` (`silicon-doc-text.txt:3120`). **Bench question (no external pins needed beyond a
jumper-free read-back):** start a cog that drives P0 high, sets a smart-pin mode on P1 (e.g. NCO) and
enables it, COGSTOP it from another cog, read P0's DIR/OUT/IN and P1's mode behaviour from the
surviving cog. **Fix when answered:** state the measured result on `cogstop.yaml`, cite the EF.

## Full impact audit: every fact KB v1.23.0 and v1.23.1 changed, against every live document (2026-10-04, «#378») — F-526 … F-541, plus F-542 … F-545 (seen verifying v1.23.1 and writing the MCP filter handoff)

**Method.** The fact inventory was built from the diffs (`v1.22.0..v1.23.1`, `deliverables/ai/P2/`), not
from this register: **69 net fact changes** (843d6fac: 43 — C6 net-reversed by a0ebdd21; a0ebdd21 +
522bc105: 26). v1.23.1 changed no fact (structurally verified in «#376»). Every fact × every live
document — the 18 published plus P2 Errata — was read by five read-only agents, each with a 69-row
denominator per document (all 18 sum to 69). **Every non-CONSISTENT verdict was re-read by the arbiter
against the manual file and against the YAML AND the Silicon Doc on disk.** Rejected after reading:
D16 Single-Step (a Spin2 `GETCT()` example; the 2-clock figure is PASM2-only by design), D10 I/O &
Smart Pins (the guide is right — see F-526), C10 I/O & Smart Pins and P2AN001 (rule + taught `WRPIN #0`
exception = the KB's; P2AN001 changes input select, not mode), C32 Assembly (a valid PLL bring-up), C13
XBYTE (echoes the Silicon Doc's own "cog/LUT only!"), C21 XBYTE (see F-540). Excluded: AI Privacy Guide
(no P2 facts), Donna-Manuscript (private), the layout torture test (instrument). Already in flight, not
re-filed: Streamer GETXACC (F-479); Architect's Guide and P2AN007 mailbox (F-524/F-521 — widened by this
audit, see their notes).

| Document | Update needed | Findings |
|---|---|---|
| Assembly Reference | **yes** | F-527, F-528, F-529, F-530, F-541 |
| DeSilva Tutorial | **yes** | F-529, F-532 |
| I/O & Smart Pins | **yes** | F-533, F-534, F-535, F-536 |
| DEBUG Window | **yes** | F-530, F-531 |
| XBYTE Guide | **yes** | F-537, F-538 |
| Streamer Guide | **yes** | F-539 (+ F-479 open) |
| Architect's Guide · P2AN007 | in «#377» | F-524, F-521 (widened, re-staged) |
| Getting Started · Single-Step · PNut-Term-TS · P2 Errata · P2AN001-P2AN006 | no | — |
| *the KB itself* | **yes** | F-526, F-540 |

F-526 (sync TX primes in reset, EF-090) and F-540 (`##` takes a skip-pattern bit, EF-091) are DONE and archived — `correction-sweeps/2026-10-04-P2KB-CORRECTION-FINDINGS-archive.md`.

### F-545 — provenance ships under keys the delivery filter does not list (`last_verified`, `extraction_status`, `authority_tier`, `grounding`, …) — `RESOLVED` (census, folds, the `scrape_tracking` filter key and the new-key gate applied 2026-10-10, «#420»/«#422»; three served provenance keys remain, F-569; closed 2026-11-07)
> **Closed 2026-11-07:** Served in v1.25.2; the last open key is F-569's, closed with it. `validate-dod-release.py`'s PowerShell filter check passed at the v1.25.5 release (`PS1-VERIFIED.md`, 2026-10-11).
Measured 2026-10-04 on the shipped payload (keys surviving the filter): `extraction_status` 131 files,
`last_verified` 131, `last_author_extraction` 113, `last_complete_extraction` 73,
`last_author_re_extraction` 29, `authority_tier` 92 lines / 15 files, `grounding` 28 / 10,
`extraction_metadata` 13, `provenance` 10, `extraction_date` 9, `primary_sources` 7, `authority` 7,
`derived_from` 7 / 4, `cite` 18 / 2, `cross_check_sources` 4, `source_document` 3 (outside the
code-example schema), `range_source` 12, `rescrape_source` 17, `import_source` 12,
`original_archiver_name` 6, and others. These reach every consumer (scripts and MCP alike). **Rule
(Stephen, 2026-10-04): the filter's key list does not grow** — "let's make sure we're using existing
keys the way we should and not inventing new keys." So the fix is on the KB side, key by key:
provenance moves into `source:` / `sources:` (or the existing metadata keys), content stays. **To do:**
classify each key (provenance vs content — e.g. `resources`, `reference_links`, `source_code`,
`event_sources` are content; `original_archiver_name` may be attribution a consumer should see), then a
sweep with the «#376» verification method (structural checker, word diffs, gates). Also add a gate that
fails on a NEW key name containing source/extract/verified/provenance/authority that is not in the
list, so the drift cannot recur.

> **`source_document` of the two code examples dispositioned 2026-10-10 («#420»).** The retired
> "Green Book" tutorial citation was replaced, not deleted: `audit-yaml-source-lock.py` counts the
> key as a citation (removing it was a NAMED → ABSENT regression). `smart-pins-001-basic-io.yaml` now
> cites "P2 Instructions v35 - Rev B/C Silicon, rows DIRL, DIRH, OUTL, OUTH" and
> `smart-pins-002-button-reading.yaml` the same sheet's DIRL row plus the Spin2 v55 Cog Registers table,
> each saying the example itself is illustrative, not a published listing. The key stays (the schema
> now lists it as optional); it still reaches consumers.

> **Key census and first removal, 2026-10-10 («#422», dispatch A).** Outside the OBEX catalog:
> `authority_tier` is content (the decomposition pages, 92 lines in 15 files, and the sourcing gate
> reads `authority_tier: EXAMPLE`) and stays; `grounding` (decomposition pages: pointers to the KB
> keys a principle rests on) is content and stays; `extraction_status` and `last_verified` occur only
> in the OBEX objects. Those two keys are **removed** from all 130 OBEX objects and from
> `_template.yaml` (262 lines; no gate and no KB reader consumes them, and the OBEX-metadata parent
> keeps its other children, so no null parent). `provenance:` / `primary_sources:` /
> `cross_check_sources:` / `range_source` were assigned to S-392 (folded; next note).
> **Decided by the arbiter 2026-10-10:** `extraction_metadata` / `extraction_date` (process dates) are
> removed; `cite:` (decomposition method, KB-key pointers) is content and stays.
> **Left, by the arbiter's call:** the OBEX objects' `metadata:` scrape bookkeeping — measured
> 2026-10-10: `last_author_extraction` 113 files, `last_complete_extraction` 73,
> `last_author_re_extraction` 29, `discovery_date` and `kb_integration` 131, `import_source` 12,
> `rescrape_source` 17, `original_archiver_name` 6 — because the p2kb-mcp OBEX tools may read them
> (outside this register's reach; a question for the MCP head, not a KB defect found here).

> **Folds and removals applied 2026-10-10 («#422», dispatch B).** `provenance:` / `primary_sources:`
> (`p2an001`–`p2an007`, `click_module_integration.yaml`, `addon-hyperram-hyperflash.yaml`) are folded into
> `sources:`, each entry rewritten to the Parallax title, edition and page it was read from.
> `cross_check_sources:` in `p2an005`–`p2an007` points at P2KB pages, which are not sources and which a
> `sources:` line would have rejected as a KB path, so the key is renamed `related_pages:` (the paths
> still resolve). `range_source` is folded into `source:` in all 12 `language/pasm2/` pages (the PASM2
> Manual "in Brief" page; `wmlong.yaml` cites the P2 Instructions sheet). `derived_from` in
> `timing_operations.yaml` is now a `computation_note:` and `provenance: "heuristic, unsourced"` in
> `cogspin.yaml` is a `caveat:` — reader caveats stay as content. `extraction_metadata` /
> `extraction_date` are removed from `spin2-builtin-symbols-complete.yaml`,
> `spin2-pasm2-integration.yaml`, `io_pin_timing.yaml`, the system-register pages and the two code
> examples (process dates; each page keeps a real citation).
> **Owed (not built):** the gate this entry named — fail on a NEW key whose name contains
> source/extract/verified/provenance/authority and is not in the reviewed list — does not exist
> (checked 2026-10-10: nothing in `validate-dod-release.py` or `engineering/tools/validation/` reads key
> names); until it is built the drift can recur.

> **Scrape bookkeeping moved under a filtered key, and the owed gate built, 2026-10-10 («#422»).**
> **DECIDED by Stephen:** tracking data stays in the YAML and the delivery filter keeps it out of the
> agent's context; only what helps an agent build code or understand the P2 and its drivers is served
> (doctrine *Provenance is for us*). `metadata:` holds real content in 16 language/architecture pages
> (query tags, common mistakes), so it cannot be filtered; the OBEX / Quick Bytes scraper block is
> renamed `scrape_tracking:` in 173 files (131 OBEX objects incl. `_template.yaml`, 42 Quick Bytes
> pages; one line each, `git diff --numstat` 1/1 on every file) and `scrape_tracking` is the one name
> added to `remove_fields` — his exception to the 2026-10-04 no-growth rule ("yes A"). `rule_id`
> `b431af2a…77ee` → `7dc618e4…4870` (`DELIVERY_FILTER`, `generate-p2kb-index.py`); the MCP handoff
> (amendment note), the `.sh` / `.ps1` built-ins, `verify-ps1-filter.ps1`, the OBEX spec, 25 OBEX
> scripts and the Quick Bytes scraper write and read the new key. The cert bundle is a frozen fixture
> and is untouched. **The gate:** `audit-yaml-provenance-key-names.py`, in `validate-dod-release.py`:
> every provenance-shaped key name (source / extract / scrape / verif / authorit / provenance /
> tracking, by word) must be on a reviewed list with its reason; scrape bookkeeping must sit under
> `scrape_tracking`; self-test with a synthetic `last_verified_by` and in-list cases. **Fixed in the
> same pass from its census:** `wrlut` / `rdlut` `authority:` → `source:`; `fifo.yaml`
> `verification_notes:` split into `hubexec_fifo_facts:` (the four verbatim Silicon Doc facts, content)
> and `sources:`; `_template.yaml`'s empty `notes:` placeholder removed; `pin-capture.yaml`
> `verification_status:` reviewed as content (measured facts, each sub-block with its EF `source:`).
> **Still open (served today, recorded as `open` in the gate):** `last_scraped` in OBEX
> `version_tracking` (130 files) — Stephen's call, see F-569; `base_pin_options_provenance`
> (`addon-click-adapter.yaml`) and `combinations_are_compiler_verified` (`pasm2-getting-started.yaml`)
> — F-569. **Needs Stephen on Windows:** `fetch-kb-file.ps1` changed, so *PowerShell Filter Verified*
> stays red until `verify-ps1-filter.ps1` is re-run and `PS1-VERIFIED.md` updated. *Fetch Script Parity*
> reads the published index rule and turns green when the index is regenerated after the commit.

## Two residues the gates cannot see: a citation re-anchor that translated line numbers, and an eighth fabricated-provenance file (2026-08-27, «#325» verification) — F-377

### F-377 — F-365's re-anchor left locators that are in range and point at nothing; `io_pin_timing.yaml` cites a silicon-doc part file that does not exist — `RESOLVED` (the last residue applied 2026-10-07, «#387»; closed 2026-11-07)
> **Closed 2026-11-07:** Served; no silicon-doc part-file citation remains in `io_pin_timing.yaml` at v1.25.5.
> **Applied 2026-10-07.** `architecture/clock_system.yaml` had **four** off locators into v55
> "Clock Setup", not two: `configuration_constants` :1715-1725 → **:1708-1726, :1736** (section
> head, the CON table and its footnotes, the compiler-defined `clkmode_`/`clkfreq_` at :1724-1726,
> `_AUTOCLK` at :1736); `configuration_rules` :1716-1725 → **:1709-1722** (closed-set sentence,
> the rows :1711-1719, footnotes :1721-1722); `anti_patterns.conflicting_definitions` :1716-1725 →
> **:1709-1719**; `missing_crystal_frequency` :1718 → **:1711** (the `_clkfreq`-alone row,
> "assumes 20 MHz crystal"; :1718 is the no-symbol default row). Each target line read off disk.
> Swept the class: every other KB citation into v55 :1700-1749 (`guides/pasm2-getting-started.yaml`,
> `guides/spin2-getting-started.yaml`) lands on the text it names — untouched.

**DISCHARGED 2026-08-30 by F-399.** Part 1 (the translated-locator class) is closed the only way it can be: all **721** citation locators in the shipped set were opened at their cited lines and read. 22 were repaired — 18 pointing at content that does not support the claim, of which **10 were exactly this carry-over shape** in `pin-capture.yaml` and `pin-selection.yaml`; the two named in this entry (`dds-goertzel.yaml`) are among them. A corpus-wide carry-over detector now returns **zero** across all 222 `silicon-doc-text.txt` citations. Part 2 (`io_pin_timing.yaml`'s fabricated `part3-pins.txt`) was repaired earlier and its replacement locators were re-read in the F-399 sweep. **See F-399 for the method, the totals, and the two instrument defects that had to be fixed before any of it could be trusted.**

**Part 1 — the re-anchor residue.** F-365 moved 23 shipped citations from the superseded
`p2-documentation.txt` to `silicon-doc-text.txt`, and its own instruction was explicit: *verify each
against the new artifact; never translate line numbers.* Some were translated anyway.

`architecture/streamer/dds-goertzel.yaml:74` cites `silicon-doc-text.txt:1565 and :4062-4095`.
**`:1565` is correct** — it carries *"S[19:0] supplies a 20-bit value which is used to configure the
DDS/Goertzel mode"*. **`:4062` is a blank line.** The same file's `:303` cites `:1636` (`' Setup`,
plausible) and `:4289-4305`, where `:4289` reads `[t34 r3c1] %0000` — a table-cell marker, not the
mode/data longs claimed. `application-notes/p2an002…:103` carries two more of the same shape.

**No instrument can catch this, and that is the point.** A class-wide range check over every
`silicon-doc-text.txt:NNN` citation in the shipped set — **113 citations, file is 5626 lines** —
returns **0 out of range**. A translated locator lands inside the file and reads as valid to
anything that checks bounds. Only opening the line catches it. The suspect set is bounded and
small: the 23 citations F-365 moved.

**Fix.** Re-verify those 23 by *reading* each cited line and confirming it carries the content the
citing block claims — the discipline F-365 stated and did not fully execute. Where it does not,
locate the content in the artifact; do not adjust the number.

**Two more of the same shape, found by «#326» and confirmed by the arbiter — and note they are NOT
F-365 residue, which widens the class.** `architecture/clock_system.yaml`
`anti_patterns.conflicting_definitions.source` cites `spin2-v55-text.txt:1716-1725` for the
sentence *"These symbols must be defined in one of the following combinations"* — that sentence is
at **`:1709`**; `:1716` is the `_rcslow` table row. And `anti_patterns.missing_crystal_frequency.source`
cites `:1718` for the verbatim *"Selects XI/XO-crystal-plus-PLL mode, assumes 20 MHz crystal"* —
that is the `_clkfreq`-alone row at **`:1711`**; `:1718` reads *"No symbol and not DEBUG mode"*.
Both quotes are accurate, both locators point at a different row. `«#326»` also found the same
shape in the differential-read artifact it was handed (a datasheet footnote given as `:2205`, the
`Cin` Mode 3 row, where footnote 2 is at `:2209`).

**So the class is wider than F-365's 23.** Any citation written by translating a number rather than
locating content has this shape, whatever pass wrote it. The sweep should cover every
`spin2-v55-text.txt:` and `p2-datasheet-text.txt:` locator in the shipped set, not only the
re-anchored ones.

**Part 2 — an eighth fabricated-provenance file.** F-359 named seven `architecture/` files carrying
headers that cite silicon-doc part files which have never existed; one was purged and «#323»
re-derived the other six. **`architecture/io_pin_timing.yaml` is an eighth and was never in the
list.** It carries `# Silicon Doc Reference: part3-pins.txt, pages 5-8` at `:2` and
`"part3-pins.txt, Pin Timing Specifications"` at `:193`. The silicon-doc folder contains
`part3-end.txt`, `part3-interrupts.txt`, `part3-pages-37-38.txt`, `part4-locks.txt` and
`part4-smart-pins.txt` — **there is no `part3-pins.txt`**. Same defect, same mechanism: the header
satisfies the citation regex, so the sourcing gate reads the file as cited.

**Fix.** Re-derive it against `silicon-doc-text.txt` exactly as «#323» did the six, and collect
anything that cannot be re-derived rather than deleting it.

**Also repaired on the spot during this verification** (not deferred, one line):
`architecture/interrupts.yaml:27` asserted *"Each interrupt level has its own set of shadow
registers"* while `:43` of the same file, rewritten by «#323» from the source, states *"There are
no shadow register banks."* «#323» corrected the detailed block and left the summary paragraph
contradicting it. The summary now points at `automatic_state_save` instead of restating it.
A prose self-contradiction is invisible to every gate here — the encoding check that verified this
file cannot read sentences.

## The delivery filter strips `documentation_source:` from every file it serves, and 706 of those values are real citations (2026-08-26, «#324» verification) — F-375

### F-375 — a remote agent receives 383 of our files with their source line deleted, and the gate that checks the filter cannot see it — `RESOLVED` (gate half resolved 2026-09-11; the rename overtaken by Stephen's 2026-10-08 ruling; the sourcing gate teaching and the bookkeeping-word cleanup applied 2026-10-10, «#412»/«#422»; closed 2026-11-07)
> **Closed 2026-11-07:** Served; the filter gate, the sourcing gate teaching and the bookkeeping-word cleanup are all in the tree at v1.25.5, and the rename was overtaken by Stephen's ruling of 2026-10-08.

> **DECIDED by Stephen 2026-10-08 (no rename): ready to fix.** The delivery half was overtaken
> by the 2026-09-19 ruling that *provenance is for us*: the certified delivery filter strips
> `source:` as well, so a rename would deliver nothing. What is left:
> - Teach `audit-yaml-claim-sourcing.py` `CITE_KEY_RE` to read `documentation_source:` (Stephen's Q3,
>   2026-10-09: `enhancement_source:` is not read and its 356 lines are deleted). Done in «#412».
> - Delete the ~40 bookkeeping words: `enhanced` (16), `original` (15), `p2_datasheet` (8),
>   `code_analysis` (1). Done in «#422».
>
> F-375 then closes (when a release serves it).

> **Applied 2026-10-10 («#422», dispatch A).** All 356 `enhancement_source:` lines are deleted (the
> sourcing gate already ignores the key; `enhancement_source` is in the delivery filter's stripped set,
> so no served text changed). Of the 40 bookkeeping `documentation_source:` words, 19 are deleted and 21
> are **replaced with the real citation**, because deleting them would have dropped the page from a
> poor tier to none: the 8 CORDIC pages cite the Datasheet's CORDIC Solver section (p.20 / p.21) and
> its instruction table (p.44 / p.45) — each page's facts checked there; `qvector` / `qrotate` also cite
> the Silicon Doc's CORDIC Solver section for the angle units, which the Datasheet does not state — and
> 12 PASM2 pages plus `event_interrupt_config.yaml` cite the PASM2 Manual "in Brief" table page
> (p.148–159), the P2 Instructions sheet, or the Silicon Doc Events / Interrupts sections. `crcnib.yaml`'s
> description was a truncated fragment ("Q = Q << 4.") and is now the table's full text. A final grep of the
> four words over the tree found none left. Closes with the next release that serves it.

> **Continued 2026-10-10 («#422», dispatch B).** The remaining `documentation_source:` values that were not
> a document are rewritten to the real citation: `production_code_analysis`, `PNUT_TS_compiler_analysis`,
> `redirect_stub`, `enhanced_from_code_study` and `Spin2_v51_documentation` (each page now cites the
> Silicon Doc, Spin2 v55 or PASM2 Manual section the page's facts come from), and about 230
> `language/pasm2/` `documentation_source:` one-liners now read "Propeller 2 Assembly Language (PASM2)
> Manual Nov 1, 2022 Release, <instruction>, p.N" (the page read from the manual's own table of contents or
> its "in Brief" table). The sourcing gate reads every one of them.

**The mechanism.** Both delivery paths run the same five-pattern line filter:
`engineering/tools/p2kb/fetch-kb-file.sh:189` and the `FilterMetadata` contract recorded in
`engineering/tools/p2kb-mcp/P2KB-MCP-SPECIFICATION.md`, designed in
`engineering/tools/p2kb/METADATA-FILTER-DESIGN.md`, which describes `documentation_source` as
*"Original doc reference"* — internal bookkeeping not worth shipping.

**That premise is false for the overwhelming majority of them.** Measured 2026-08-26 across all
1133 shipped files:

> **706 `documentation_source:` / `enhancement_source:` values are citation-shaped** — they name a
> document, an edition, a page or a line. **47 are the bare internal tokens the filter was designed
> for** (`enhanced` 16, `original` 15, `p2_datasheet` 8, `code_analysis` 2, and three singletons).
> The citation-shaped values sit in **383 distinct files**.

Examples of what is deleted on the way out:

| File | Value stripped in delivery |
|---|---|
| `language/spin2/assembly-directives/alignl.yaml` | `PASM2 Manual 2022/11/01 Pages 31-147` |
| `language/spin2/registers/pr-registers.yaml` | `PASM2 Manual 2022/11/01 Page 118` |
| `language/spin2/debug-commands/pc_key.yaml` | `Spin2 v51 (debug-section.txt) + PNut v55 directive matrix` |
| `language/spin2/statements/debug.yaml` | `PNut v55 compiler source (p2com.asm: check_word_chr_initial/check_word_chr @8888, debug_symbols table @19335, parse_debug_string, symbol_size_limit=30); hardware-isolated on real silicon 2026-07-27` |

**Why this is the sharpest form of a defect this project already knows.** The shipped set carries
the **agent-consumer** bar — *cite or omit*, because a remote agent cannot weigh a hedge and a
wrong fact becomes silently authoritative in generated code. The filter takes files that satisfy
that bar on disk and delivers them **not satisfying it**. Every gate we run reads the tree; the
consumer reads the filtered stream; nothing compares the two. The KB is cited. What we *serve* is
not.

**Second half, and it is why this was never caught.** `validate-dod-release.py`'s
`validate_metadata_filter` (lines 352-396) checks *which line-patterns the filter removes* and
never re-parses the filtered payload — there is no `yaml.safe_load` and no type comparison anywhere
in the function. «#324» proved the consequence: a block whose only child is `documentation_source:`
is delivered as `null`, and the check passes clean. **The filter is indentation-blind, so it can
destroy a block outright**, and the gate that exists to watch it is measuring the wrong thing.
*A gate must read the artifact* — this one reads the pattern list.

**Fix (two parts).**
1. **Filter:** stop deleting `documentation_source:` / `enhancement_source:` wholesale. Either
   deliver them, or delete only the 47 bare-token values and keep every citation-shaped one. The
   cleanest form is the one the project already uses everywhere else — rename the real ones to
   `source:` and let the filter keep its narrow meaning. That is 383 files, so it is a task.
2. **Gate:** `validate_metadata_filter` must re-parse the filtered payload and compare top-level
   types against the on-disk file, with a negative control that proves it fires. The `shape_probe`
   case from «#324» is a ready-made control.

**How this surfaced.** «#324» was measuring whether 34 YAML shape changes break any consumer. They
do not. But running the real fetch script against the real tree — rather than reading it — showed
what the delivery path does to files that were never part of the shape question at all.

**GATE HALF RESOLVED 2026-09-11 (block I «#340»).** The structural complaint — *every gate reads the tree, the consumer reads the stream, nothing compares them* — is answered where it mattered: `validate_metadata_filter` now `yaml.safe_load`s the DELIVERED payload and fails on any key that collapsed to `None`, proven with an independently-built negative control (block H, `75911edb`).

**Delivery-strip numbers re-derived and recorded** in the change ledger (now `2026-09-11-yaml-release-change-ledger.md` §1.5 — see the note below) so they reach Stephen's visual read: `filter_metadata` strips five fields; `documentation_source` is **396 values across 395 files**, of which **363 (91%) are real provenance** and only 33 are bookkeeping tokens (`enhanced` 16, `original` 15, `code_analysis` 1, `redirect_stub` 1). So the set satisfies cite-or-omit ON DISK and is delivered NOT satisfying it, and nine tenths of what the filter removes is the provenance the project's own rule requires. Filing drift noted rather than smoothed: the entry said 397/396, today measures 396/395.

**The 383-file rename was a scope call Stephen owned; he ruled 2026-10-08 that there is no rename** (the delivery filter strips `source:` too, so a rename would deliver nothing; provenance is for us). What was left — the gate learning `documentation_source:` and the bookkeeping words — is applied (the blocks above).

⚠ **Ledger correction 2026-09-11.** These numbers were first appended as §1.26 to `2026-08-27-yaml-release-change-ledger.md`. That ledger was **spent** — its declared range `v1.17.0..b0057ec1` shipped on 2026-09-10 as v1.18.0/v1.18.1 — so it could not gate an unshipped release. Stephen caught it. The append was reverted, that ledger archived byte-identical to its last committed revision, and the content re-derived against the correct `v1.18.1..HEAD` range in `2026-09-11-yaml-release-change-ledger.md`. **A release ledger expires the moment its range ships, and nothing in the process was checking that.**

## Our USB smart-pin entry states as fact a sentence the DOCX edition dropped, and it contradicts the general WRPIN rule (2026-08-26, «#320» citation re-anchor) — F-372

### F-372 — `%11011` says a new WRPIN needs no reset; the same document's general rule says the opposite — `RESOLVED` (settled on silicon by EF-093, applied 2026-10-10, «#419»; closed 2026-11-07)
> **Closed 2026-11-07:** Served; `smart-pin-11011-usb-host-device.yaml` cites EF-093 at v1.25.5.

**How this surfaced.** F-365's re-anchoring reads each stale citation's old target and finds that
content in the new artifact. Twenty-two of twenty-three matched. **One did not exist in the new
artifact at all**, which looked like an extraction defect and is not one.

**What the two editions actually say.** Both are labelled *Propeller 2 Documentation v35 (Rev B/C)*.

| | |
|---|---|
| **PDF-derived capture** `p2-documentation.txt:8886` | *"…will disable output drive and effectively create a USB 'sniffer'. **A new WRPIN can be done to effect such a change without resetting the smart pin.** NOTE: In Propeller 2 emulation on an FPGA…"* |
| **DOCX capture** `silicon-doc-text.txt:4579` | *"…will disable the output drive and effectively create a USB 'sniffer'. NOTE: In Propeller 2 emulation on an FPGA…"* — **the sentence is absent** |

The DOCX paragraph is not merely shorter; it is **differently written**, and it *adds* material:
`%HHH_LLL` drive modes are overridden alongside OUT, and *"The lower pin in the pair is DM, while
the upper pin is DP, per USB naming convention"* — neither of which the PDF version carries. The
heading differs too (`%11011 = USB host/device` vs `%11011 = USB host or device, full-speed
(12Mbps) or low-speed (1.5Mbps)`). **These are two revisions of one document, both claiming v35.**

**Why it matters beyond bookkeeping.** The dropped sentence **contradicts the general rule** this
same document states at `silicon-doc-text.txt:3856` and that «#319» just applied to
`architecture/smart_pins.yaml` as F-369: a WRPIN issued while DIR is high remaps 126 bits of state
underneath a running mode, producing *"unpredictable and quite certainly useless behavior"*, which
is why modes are configured only while DIR is low.

Two readings, and **documents cannot separate them**:

1. **USB is a genuine exception** — the sniffer change is a drive-enable flip rather than a mode
   change, so the multiplexing hazard does not apply, and the DOCX simply lost the sentence.
2. **The sentence was removed because it was wrong**, and the general rule governs `%11011` like
   everything else.

**Reached our KB?** **Yes — as settled fact.**
`architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` `configuration.wrpin_data` ends with
the sentence verbatim, with no caveat, cited to the PDF-derived capture that is now superseded.

**Applied 2026-08-26:** the claim kept its place — it may well be right, and deleting a plausible
documented behaviour is its own kind of damage — and carried the conflict, citing both editions.
**Routed to `KNOWLEDGE-GAPS` as G-027, bench-testable and jumper-only; the bench settled it
(EF-093, below), and G-027 is ANSWERED.**

> **Settled 2026-10-10 («#419»): EF-093 (WRPIN, drive ↔ sniffer) and EF-102 (WXPIN, baud).**
> EF-093: a live WRPIN that switches a running USB pair between the drive word `$76` and the sniffer word
> `$36` took effect without a reset or a DIR cycle, 5 of 5 (one pair, full speed, host mode, nothing
> attached). The Hardware Manual's sentence stands. `smart-pin-11011-usb-host-device.yaml`
> `configuration.wrpin_data_conflict` ("NOT SETTLED … the same document") is replaced by
> `wrpin_data_on_a_running_pair` (`:21-31`); `detailed_description.source` cites the P2 Documentation, the Hardware
> Manual, EF-093 and EF-102; `pin_pairing` names the overridden `%HHH_LLL` drive modes (`silicon-doc-text.txt:4579`).
> EF-102 supplies the P2 Documentation's on-the-fly WXPIN sentence (`:4581`) for the **baud only**
> (`configuration.wxpin_on_the_fly`); the FS/LS bit D[14] is not claimed.

## `pin-selection.yaml` printed the streamer's sub-pin table with the wrong bit weights, and shipped the EF-065 trap as its worked example (2026-08-26, found while composing the streamer pin-capture page) — F-361

- **F-361 — Two defects in `deliverables/ai/P2/architecture/streamer/pin-selection.yaml`: a
  `sub_pin_selection` table that contradicts both the Silicon Doc and the bench, and a
  `pin_base_encoding` example that is the EF-065 misalignment trap written out for a reader to
  copy.** — `RESOLVED` (both fixed 2026-08-26; a direct bench check of the sub-pin weights is arm B of VO-J-005 and has not been run; closed 2026-11-07)
> **Closed 2026-11-07:** Bench confirmed by EF-105 (2026-11-06), which closes the owed arm B of VO-J-005; the page is correct and served.

  **Defect 1 — the sub-pin table.** The block stated `field: "D[19:17] within mode config"` and then
  gave a **dense slot** mapping: for 2-pin modes `%001 = Pins 3..2`, `%010 = Pins 5..4` … `%111 =
  Pins 15..14`; for 4-pin modes `%001 = Pins 7..4` … `%111 = Pins 31..28`. Both columns are wrong,
  and wrong in a way that matters: they imply a 4-pin capture can be based anywhere in a 32-pin
  window, which is exactly the belief that produces a misaligned base.

  **What the sources say.** Propeller 2 Documentation v35: *"In every mode, the three %ppp bits in
  D[22:20] select the pin group, in 8-pin increments"*
  (`engineering/ingestion/sources/silicon-doc/p2-documentation.txt:3606`) and *"For modes which
  involve less than 8 pins, lower-order %p bit(s) in D[19:19..17] are used to further resolve the
  pin number(s)"* (`:3653`). So the pin number is ONE six-bit field at D[22:17] — `pin << 17` —
  and D[19:17] is `pin & 7`, not a slot index. The Spin2 v55 streamer symbol table states the same
  thing per mode, as the bit templates themselves:
  `X_1P_1DAC1_WFBYTE %1100_DDDD_WPPP_PPPA`, `X_2P_2DAC1_WFBYTE %1101_DDDD_WPPP_PP0A`,
  `X_4P_4DAC1_WFBYTE %1110_DDDD_WPPP_P00A`, `X_8P_4DAC2_WFBYTE %1110_DDDD_WPPP_0110`
  (`engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:1608-1613`). The fixed zeros at
  D[17] and D[18:17] ARE the alignment rule, stated by encoding.

  **The bench already agreed with the sources, in two mode families.** EF-064: a 1-pin mode with
  `20<<17` drove **P20 exactly**. EF-065: an 8-pin mode with `+ 20<<17` drove **P24..P31** — the
  carry model, not the slot model. Under the table's dense reading neither result follows.

  **Defect 2 — the worked example.** `pin_base_encoding.example` read
  `mode := X_RFBYTE_8P_1DAC8 | X_PINS_ON + 20<<17 + count`: an **8-pin** mode at a base that is not
  a multiple of 8, composed with `+`. That is EF-065 verbatim, in a third mode family, printed as
  the line a reader copies. Assembled with `pnut-ts` v1.55.3 to check rather than assert:

  ```
  X_RFBYTE_8P_1DAC8 | X_PINS_ON + 20<<17 + $FFFF   ->  $A0B6_FFFF
  X_RFBYTE_8P_1DAC8 | X_PINS_ON | (16<<17) | $FFFF ->  $A0AE_FFFF
  X_RFBYTE_8P_1DAC8 | X_PINS_ON | (20<<17) | $FFFF ->  $A0AE_FFFF
  ```

  `$A0B6_FFFF` is D[19:16] = `%0110` (**X_RFBYTE_8P_4DAC2**, a different mode) at D[22:20] = `%011`
  (**P24..P31**, a different group). And the third line is the other half of EF-065: with `|` the
  misaligned base is **byte-identical** to base 16 — it does not carry, it silently vanishes. Both
  compile clean.

  **Applied 2026-08-26.** `sub_pin_selection` rewritten to state the rule and the per-width free
  bits by encoding, with a worked mapping only for the 1-pin case (the one width where all three
  bits are free and no mode caveat applies), plus a `what_a_misaligned_base_does` pointer.
  `pin_base_encoding` now carries the alignment rule, the composition rule, an **aligned** example,
  and both failure modes with their assembled words. `common_configs` re-composed with `|` and each
  base annotated with the rule it satisfies. The file also gained a `source:` (it had none) and the
  capture-path facts this sprint's Section B added.

  **What is still owed.** A bench confirmation of the 2-pin/4-pin sub-field weights specifically.
  EF-064/EF-065 cover the 1-pin and 8-pin families; the 4-pin family is **arm B of VO-J-005**
  (`engineering/ingestion/external-sources/hardware-verification/VERIFICATION-OPPORTUNITIES.md`),
  which captures at base 12 against two distinct static pin patterns and names the reversing
  outcome: if the buffer returns the P8..P11 pattern rather than the P12..P15 pattern, this finding
  is backwards and must be reverted before anything built on it ships.

## The bulk-generation commit wrote FABRICATED PROVENANCE HEADERS, and those headers are what make seven `architecture/` files look cited (2026-08-25, Stephen's question at the release review) — F-359

- **F-359 — Seven `architecture/` files carry a provenance header citing source files that have
  never existed and datasheet pages beyond the end of the datasheet; the header itself satisfies
  the citation regex, so six of the seven still pass the gate today.** — `RESOLVED` (six files re-derived and shipped by 2026-10-05, «#386»; the five remaining claims applied 2026-10-10, «#413»/«#418»/«#419»; closed 2026-11-07)
> **Closed 2026-11-07:** Served; `state_bits` is gone from `locks.yaml`, and the five remaining claims are applied in the tree at v1.25.5.

  > **DECIDED by Stephen 2026-10-08 for the five remaining claims, and APPLIED.**
  > - `locks.yaml` `state_bits: 4`: **deleted** (no `state_bits` key remains).
  > - `cog_attention.yaml` `waiting: "0 clocks"`: **fixed from the Datasheet** — now
  >   `latency: "2+ clocks (2 minimum, plus the wait for the event)"` (`cog_attention.yaml:57-59`).
  > - `debug_interrupt.yaml` `trace_buffer` and `debug_state`: the whole `memory_usage` block is
  >   **deleted** (Stephen's Q2, 2026-10-09: keep it only if it guides code; the one such fact, writes to
  >   the top 16 KB dropped in a debug build, is at `debug-strategy-guide.yaml:93`, `hub.yaml:36-57` and
  >   `debug_interrupt.yaml:80-83`). `streamer_interaction` now states the measured behaviour
  >   (`debug_interrupt.yaml:381-385`: streamer Goertzel results corrupted with every cog
  >   debug-enabled; pin and DAC output unchanged; no source states the mechanism), cited to EF-057,
  >   EF-062 and EF-063.
  >
  > The v55 interpreter and debugger that the first decision wanted ingested are ingested (2026-10-09,
  > «#401»; the debugger source is identical to v51).

  **How it surfaced.** Stephen asked whether `io_pin_timing.yaml`'s content might have come from
  our own I/O & Smart Pins manual rather than a Parallax source — i.e. whether the provenance was
  circular. **The answer is no, and the truth is worse.**

  **The timeline rules the manual out.** `io_pin_timing.yaml` was created **2025-11-29** in
  `e271cab0`; the IOSP manual's first commit is **2026-01-25**, nearly two months later. Causality
  therefore runs **KB → manual**, not manual → KB. Where that manual repeats the drive-strength
  mislabel (F-356), it most likely **inherited it from this file**, which inverts the assumption
  behind the post-release manual review.

  **Nor did it come from what it cites. Every citation in the header is false:**

  | Header line | Reality |
  |---|---|
  | `Silicon Doc Reference: part3-pins.txt` | **no such file has ever existed** (nor `part1-cog.txt`, nor `part3-smartpins.txt`, nor `part2-cog.txt`) |
  | `Datasheet Reference: pages 42-45` | those pages are the **PASM2 instruction listing** |
  | `Datasheet Reference: … 76-78` | **the datasheet is 50 pages** |
  | `Layer 1: Direct extraction from Silicon Doc v35 and P2 Datasheet` | the values (`2.5/3.5/5.0 ns`, the mA ladder, "slew") appear **zero times** in any ingested source |

  **It is a class of seven, and we purged one.** All seven were written in the same commit —
  `e271cab0`, 2025-11-29, *"Implement DOD v3.0"*, which touched **1,323 files and 973 YAMLs in a
  single commit**. Each carries the same header shape, each names a non-existent silicon-doc file,
  and **each cites a second datasheet range beyond page 50**:

  | File | Cites | Impossible page range | Quantities today |
  |---|---|---|---|
  | `architecture/io_pin_timing.yaml` | `part3-pins.txt` | 76-78 | purged this sprint |
  | `architecture/cog_attention.yaml` | `part1-cog.txt` | 73 | 0 |
  | `architecture/debug_interrupt.yaml` | `part1-cog.txt` | — | 0 |
  | `architecture/event_system.yaml` | `part1-cog.txt` | 74-75 | **6** |
  | `architecture/interrupts.yaml` | `part1-cog.txt` | 71-72 | **2** |
  | `architecture/locks.yaml` | `part1-cog.txt` | 82 | 0 |
  | `architecture/lookup_ram.yaml` | `part1-cog.txt` | 67-68 | **1** |

  🔴 **THE MECHANISM — the fabricated header IS the citation that silences the gate.** Measured
  against `audit-yaml-claim-sourcing.py`'s own regex: all three header forms return
  `INLINE_CITE = True`, because the matcher fires on the tokens *"Silicon Doc"* and *"Datasheet"*
  wherever they appear. **A header that invents its sources reads to the instrument exactly like a
  header that names real ones.** This is F-335's pattern — the citation side matching on the
  presence of a token rather than on whether the sentence attributes the block to a document —
  applied to the KB's original sin rather than to a later edit.

  **Consequence for the release, stated plainly:** at least **9 quantities** across three of these
  files stand under a header citing a file that does not exist, and the current `0 Tier 1` does not
  contradict that — the gate is satisfied by the fabrication. `io_pin_timing.yaml` was caught only
  because it *also* had blocks with no header coverage at all.

  **The "lack" this traces to.** Nothing checked generated content against a source at creation
  time, and **the citation header was generated along with the content it claims to source**. A
  fabricated citation is not an error in sourcing; it is the signature of never having sourced.
  973 YAMLs in one commit is the scale at which that becomes invisible.

  **NOT FIXED — this is a scope decision Stephen owns**, raised at the release review he called
  for. Purging six more files is a widening at the gate, and the release is his call. Options are
  his: purge the class now, ship and schedule it, or re-derive those six from the real sources.
  What must NOT happen is shipping while believing the `0 Tier 1` covers them.

  🟢 **RESOLVED 2026-08-26 («#323») — the third option was taken: all six re-derived from the
  real sources.** The silicon doc is now fully extracted, which is what made this tractable;
  every claim below was read off `sources/silicon-doc/silicon-doc-text.txt` or
  `sources/p2-datasheet/p2-datasheet-text.txt` live, and every citation written into the six
  files was then re-read at the line it names.

  **What the re-derivation actually found is worse than the header.** The fabricated citation was
  the signature, not the extent. Across the six files:

  | | Before | After |
  |---|---|---|
  | `- instruction:` entries carrying an `encoding:` | 47 | 45 |
  | encoding **verbatim-identical** to the silicon doc's PASM2 encoding table | **2** (`RDLUT`, `SETSE1`) | **45** |
  | encoding **wrong** | **41** | **0** |
  | mnemonic **not in the encoding table at all** | **4** | **0** |

  The four absent mnemonics are `RDCOGID`, `RDLUTS`, `NIXINT0` and `TRGINT0`. Each was checked
  three ways: absent from `silicon-doc-text.txt`, absent from every other file under
  `deliverables/ai/P2/`, and not accepted as an instruction by pnut-ts v1.55.3 (`nixint0` and
  `trgint0` assemble to a zero-byte binary because the compiler reads them as labels; `rdcogid`
  and `rdluts` are hard errors). The four RETIx encodings come from this knowledge base's own
  `language/pasm2/reti0..3.yaml`, since RETIx are CALLD aliases and appear in the silicon doc as
  alias definitions (`:5483-5486`) rather than as encoding-table rows.

  Plus these semantic inversions, each of which a code-generating agent would have acted on:
  * `interrupts.yaml` had the **IJMPx/IRETx address map inverted** — it called `$1F0` IJMP1 where
    three authorities (silicon-doc `:2296-2301`, datasheet `:558-563`, and the RETIx alias
    definitions at silicon-doc `:5483-5485`) all say `$1F0` is IJMP3.
  * `interrupts.yaml` claimed **per-level shadow registers** for PA/PB/PTRA/PTRB/Q. There are
    none; the CALLD dispatch saves the return address and C/Z into IRETx and nothing else
    (silicon-doc `:2294`, `:2359`).
  * `lookup_ram.yaml` had **LUT sharing backwards** — it described reading the neighbour's LUT.
    Sharing is a WRITE path into the paired cog's LUT (silicon-doc `:491-500`). It also had
    **WRLUT's operands reversed** (D is the data, S is the address).
  * `locks.yaml` carried a `LOCKTRY (WC mode)` entry meaning "check the owner without acquiring".
    LOCKTRY always attempts to take, and C=1 means *taken* (silicon-doc `:3688`); the query form
    is LOCKREL with WC and a register D (`:3700`).
  * `cog_attention.yaml` had **ATN as event 15**; it is event 14 (`:2053`, `:2290`), and both
    SETINTx examples used the wrong number. Its `setup_for_event` configured SETSE1 for
    attention, which SETSEn cannot select at all (`:2246-2260`).
  * `debug_interrupt.yaml` invented three **"configuration registers"** (BRK as a register with a
    `[31:20]` flags field, plus SKIP and SKIPF as debug registers). BRK is an instruction whose D
    operand is `%aaaaaaaaaaaaaaaaeeee_LKJIHGFEDCBA` (`:2498-2517`), and GETBRK reads cog status
    in three forms rather than reading back a break configuration (`:2527-2593`).
  * `event_system.yaml` carried an invented event taxonomy ("Edge-detect", "IN-rise",
    "CORDIC-done") in place of the sixteen the source enumerates (`:2037-2054`), and its
    pattern-match example selected **mismatch** mode while its comment said match — SETPAT reads
    C and Z as inputs, and takes no WC/WZ effect (confirmed against pnut-ts).

  **The header was replaced in both places it lived** — the leading comment block AND
  `extraction_metadata.source_documents`, which carried the same `part1-cog.txt` and the same
  impossible page ranges. Each file now names the real document, the real section, and a live
  line range, and carries a `re_derivation_note` stating what was corrected.

  ⚠️ **THE GATE IS STILL NOT THE EVIDENCE.** `audit-yaml-claim-sourcing.py` read `0 Tier 1`
  before this work and reads `0 Tier 1` after it, because none of the six carries a
  unit-bearing quantity block. That green says nothing about whether these files are cited; the
  evidence is that every `<file>:<line>` written into them was re-read at the line it names. The
  instrument was separately shown to be live on these files: a planted two-quantity block in
  `locks.yaml` produced `TIER 1 ... 1 violation` and exit 1, and removing it returned exit 0.

  **Eight claims could NOT be re-derived and were NOT deleted — deletion is Stephen's.** Each was
  searched for in the silicon doc, the datasheet and this KB's own per-instruction YAMLs before
  being listed:
  1. `locks.yaml` `architecture.state_bits: 4` with the comment "3 bits COG ID + 1 bit owned
     flag". No source gives a lock any internal bit-width; both authorities say only "16
     semaphore bits" (silicon-doc `:3674`, datasheet `:878`).
  2. `lookup_ram.yaml` `performance_characteristics.power_consumption` (active "similar to COG
     RAM access", idle "static power only"). Zero hits for LUT power in either document.
  3. `lookup_ram.yaml` `bandwidth.streaming: "32 bits per clock (via streamer)"`. That figure is
     the **hub RAM** rate (silicon-doc `:2999`, `:3003`); nothing states it for a LUT-sourced
     streamer.
  4. `lookup_ram.yaml` `bandwidth.internal: "32 bits per 2-3 clocks"` — a restatement of the
     RDLUT/WRLUT timings as a bandwidth, which no source makes.
  5. `debug_interrupt.yaml` `memory_usage.trace_buffer: "Typically 4KB-16KB in hub"`.
  6. `debug_interrupt.yaml` `memory_usage.debug_state: "~100 longs for full state capture"` —
     the source describes 16 longs saved by the ROM routine and 64 bytes per cog per area.
  7. `debug_interrupt.yaml` `limitations.streamer_interaction: "Debug can disrupt streamer
     operations"`. The source makes the opposite kind of claim about the hub FIFO — the scheme
     runs in cog register space precisely so it does *not* disturb it (`:2484`) — and says
     nothing about the streamer.
  8. `cog_attention.yaml` `performance_characteristics.response_latency.waiting: "0 clocks after
     signal arrives"`. The datasheet gives WAITATN as `2+` (`:1914`).

  Not listed above, and deliberately: the `programming_patterns`, `common_applications`,
  `best_practices` and `debugging_tips` sections of all six files are authored guidance rather
  than source claims. They were corrected wherever they encoded one of the defects above (wrong
  event number, fabricated mnemonic, inverted sharing direction, mismatch-mode SETPAT), and
  otherwise left alone.

  **Fabricated NAMES were deleted rather than escalated**, under Stephen's standing rule *"no
  fabricated names in the KB tree -- delete invalid names outright"* — the same rule this
  sprint's C3 applies to the invented part numbers. The four mnemonics were checked three ways
  first: absent from the silicon doc, absent from every other file in `deliverables/ai/P2/`, and
  not accepted as instructions by pnut-ts v1.55.3.

  Status: `RESOLVED` — all six re-derived and cited against live sources; the eight
  non-derivable claims listed above are dispositioned (three removed by 2026-10-05, five decided and applied
  in the block at the top of this entry).

## Provenance holes the repopulation could not fill (2026-08-25, «#299» Plan §8 part 2) — F-352

> **Origin.** «#299» rebuilt `architecture/`, `language/`, `guides/` and `application-notes/` from
> the repaired sources, source-first. Forty-five of F-347's sixty blocks came back cited. Two did
> not, for the same reason — the KB was their only home — and the rule set had no branch for that
> once the purge had already removed them. Line numbers below were read off disk 2026-08-25.

### F-352 — two shipped KB areas are authored-here content with NO upstream anywhere in the ingestion tree, and once their blocks were purged the promotion filter's sub-rule P had no branch left for them — `RESOLVED` (click half closed and its citations rewritten 2026-10-10, «#420»/«#422»; the `io_pin_timing` half closed by staying closed; closed 2026-11-07)
> **Closed 2026-11-07:** Served; the click half is in the tree at v1.25.5, and the `io_pin_timing` half closes by staying closed, as the entry says.

> **Found:** 2026-08-25 by «#299», working the sources tree-by-tree rather than the removal list.
> Two of F-347's 60 rows could not be returned source-first, for the same underlying reason, and
> «#298»'s sub-rule P (*presence before removal*) does not cover the case because the removal has
> **already happened**.
>
> | Where | «#298» disposition | What «#299» found |
> |---|---|---|
> | `architecture/click_module_integration.yaml` `best_practices` | **ACTIONABLE** | **No ingested source states any of it.** The file's own `documentation_source: code_analysis` points at `engineering/ingestion/sources/code-analysis/`, which holds exactly three files — `bldc-motor-control-analysis.md`, `debugger-analysis.md`, `flash-loader-analysis.md` — and `grep -rln -i "click\|mikrobus"` over that directory returns **nothing**. The MikroBUS pinout, the P2 Eval Click Adapter offsets and the "three adapter positions" claim the block depends on have no upstream at all. **Recorded as a GAP, not restored.** |
> | `architecture/io_pin_timing.yaml` `best_practices` | **CORRECT BUT NOT ACTIONABLE** | Generic PCB-layout lore — match trace lengths, 22-33 Ω source termination, ~1 ns rise per 10 pF. `grep -rn "22-33\|150 ps\|150ps\|source termination\|match_trace"` over `engineering/ingestion/sources/` returns **zero**. **Held out, and deliberately NOT written to the ingestion tree.** |
>
> 🔴 **Why the io_pin_timing block was not "written to the ingestion tree first".** The C6 instruction
> offers that as the fix for a not-actionable block with no ingestion home. It is the wrong move here,
> and the reason generalises: **`engineering/ingestion/sources/` mirrors INGESTED SOURCE DOCUMENTS.**
> Writing authored-here electronics lore into it would manufacture a Parallax-tier authority out of
> nothing — and that tree is inside `audit-constant-fidelity.py`'s declared *Parallax documentary*
> truth root, which is precisely the defect F-341 already files against six of our own derived
> analysis documents sitting at that tree's root. Curing a provenance hole by inventing provenance is
> worse than the hole. The block stays out; git holds it at `15c84de5^` for anyone who wants it.
>
> **The generalizable half — sub-rule P needs a fourth branch, not a third.** «#298»'s *Sharpening*
> §3 already added *"authored-here content with no upstream at all — stays, and say why"*. That
> branch assumes the block is still **in** the KB, where "stays" is an available answer. Once a purge
> has removed it, "stays" is gone and the only choices are *invent an upstream* or *record the
> absence*. The rule wants: **authored-here, no upstream, ALREADY REMOVED → record it as a gap with
> the acquisition that would close it; never manufacture the source.**
>
> **What would settle each:**
> - *Click*: ingest the Parallax **P2 Eval Click Adapter** product documentation (the MikroBUS
>   offset map and the adapter's base-pin positions). That single ingestion would ground both this
>   block and the `p2_adapter_mapping` offsets the file already ships uncited.
> - *io_pin_timing*: nothing Parallax can settle — it is not a P2 fact. It closes by staying closed.
>
> ⚠️ **Also found while filing:** this register's header reads **`Next gap ID: G-007`**, but
> `engineering/ingestion/KNOWLEDGE-GAPS.md` already allocates **G-007** (Smart Pins / ADC, ANSWERED
> 2026-08-24). The counter is stale by one and the next free gap ID is **G-008**. «#299» allocated no
> G-number rather than collide; the header is left for whoever owns that ledger to correct
> deliberately.

> **Click half CLOSED 2026-10-10 («#420»); the `io_pin_timing` half has nothing to ship (it is not a P2 fact and closes by staying closed).** The P2 Eval Click
> Adapter's documentation *is* ingested now: `sources/p2-click-adapter/p2-click-adapter-netlist.md`
> ("Consolidated offset map", `:122-144`, from the 64008 Rev A schematic) states all twelve offsets
> (+0 SDA … +11 MOSI, +12..+15 no-connect, SPI four on header B), and
> `architecture/click_module_integration.yaml` `p2_adapter_mapping` already matches it value for value
> (re-read against the netlist, no difference). What the schematic does **not** state, and the page
> already labels as the driver's idiom (`source: P2-Click-eInk`, `provenance.code_patterns`): the three
> base-pin positions (`PINS_P0_P15` / `P16_P31` / `P32_P47`) and the mikroBUS signal meanings (the
> mikroBUS standard is not held).

> **Click citations rewritten 2026-10-10 («#422», dispatch B).** `addon-click-adapter.yaml` and
> `click_module_integration.yaml` now cite the schematic by the title block it prints, "P2 mikroBUS
> Adapter Part Number 64008, Revision A, schematic", instead of the netlist capture and the catalog
> page. The product-page statements stay as prose that names the Parallax product page; the three
> base-pin positions and the mikroBUS signal meanings are still labelled as the driver's idiom and the
> mikroBUS standard.

## The `architecture/`/`language/`/`guides/`/`application-notes/` uncited-block purge — the removal record «#293» owed and did not write (2026-08-25, arbiter) — F-347

> **Why this exists.** «#293»'s own PROTECTION POINT required *"every removal recorded with its
> origin so «#299» can work from a list rather than from git archaeology."* It was not written —
> its executor mirrored only the `io_pin_timing.yaml` portion into the register and left the rest
> in its transcript, which does not survive. **The arbiter verified that task green without
> checking that specific deliverable; that is the miss, and it is the arbiter's, not the
> executor's.** Caught at «#298»'s entry, because «#298» population 2 and «#299» both consume this
> list.
>
> **Reconstructed mechanically** from `git show --unified=0 15c84de5 -- deliverables/ai/P2/`,
> taking every removed line that begins a top-level YAML key. Nothing is lost — the purge is fully
> recoverable from git — but recoverable is not the same as recorded, and a list nobody can find
> is a list that gets re-derived under time pressure.
>
> ⚠️ **COUNT DISCREPANCY, STATED RATHER THAN SMOOTHED: this reconstruction yields 60 top-level key
> deletions; the executor reported 59 blocks.** The likely cause is one key counted differently
> (a `description:` removed as part of a larger block, or a nested key at column 0). «#298» and
> «#299» should work the 60 and treat any that resolves to "was never a block" as a no-op rather
> than assume the reconstruction is wrong. Do not reconcile to 59 by deleting a row.
>
> **Sibling records:** «#294»'s two are in F-334 above (48 blocks / 16 files, and 11 / 6).

- **F-347 — «#293»'s removal record was never written, so 60 removed blocks existed only in a git
  diff and in a transcript that does not survive.** — `RESOLVED`; closed 2026-11-07
> **Closed 2026-11-07:** Every one of the 60 rows carries an outcome (45, 1, 1, 13), and the 13 `never returns` strings read 0 in the tree at v1.25.5.

  > **Headline corrected `PENDING-VALIDATION` → `PARTIAL` 2026-08-25 («#302»), to agree with this
  > entry's own Disposition line.** `PENDING-VALIDATION` asserts the fix is fully applied and only
  > its validation is owed; that is not this entry's state. The Disposition sets the closing
  > condition as *"every row carries a returned/not-returned outcome"*, and **the reconstructed
  > table below still has four columns — File · block · pre-removal line · span — and no outcome
  > column at all.** «#299» did execute against it (F-352: *"Forty-five of F-347's sixty blocks came
  > back cited. Two did not"*), so **47 of the 60 rows are accounted for in narrative** — but the
  > record itself carries no outcome column, and the remaining **13 rows are not accounted for by
  > that sentence** (whether each is held in the ingestion tree or simply unstated was NOT
  > determined here — that determination is part of the work this entry still owes). Writing the
  > outcomes onto the rows is **work**, not validation. This disagreement was invisible to check 10 for the same
  > reason as F-355's: the entry declares its status as an indented `Disposition.`/`Status:` line
  > rather than a column-0 `**Status:**`.

  «#293» removed 59-60 uncited quantitative blocks from `architecture/`, `language/`, `guides/`
  and `application-notes/`, and its PROTECTION POINT required that every removal be recorded with
  its origin *"so «#299» can work from a list rather than from git archaeology."* The executor
  mirrored only the `io_pin_timing.yaml` portion into the register. The remainder was left in its
  transcript.

  **The arbiter passed that task green without checking that deliverable.** The other protection
  criteria — the four entry gates, the zero Tier-1 count, the crossref clean — were all verified
  and all held; the *record* was the one criterion nobody re-ran, because it is the only one with
  no instrument behind it. That is the generalizable lesson: **a protection-point criterion that
  no tool can check is the criterion that silently does not happen**, and it needs a named,
  eyes-on verification step rather than inheriting the confidence of the gates around it.

  Reconstructed mechanically at «#298»'s entry (the first task to consume it) from
  `git show --unified=0 15c84de5 -- deliverables/ai/P2/`. The table above is that reconstruction.
  Nothing was lost — a purge is fully recoverable from git — but *recoverable* is not *recorded*,
  and a list nobody can find is a list that gets re-derived under time pressure by whoever needs
  it next.

  **EXECUTED 2026-08-25 by «#299». Every one of the 60 rows now carries an outcome, and the
  count is stated in four numbers rather than one total:**

  | Outcome | Count | What it means |
  |---|---|---|
  | **restored with a trace** | **45** | The repaired source states it and it is ACTIONABLE. Every returned block carries a `source:` naming the document and a `file:line`. |
  | **held out — no ingestion home** | **1** | `architecture/io_pin_timing.yaml best_practices` (generic PCB-layout advice). CORRECT-BUT-NOT-ACTIONABLE per «#298»; see F-352 for why it was not written to the ingestion tree either. |
  | **gap** | **1** | `architecture/click_module_integration.yaml best_practices` — ACTIONABLE per «#298», but no ingested source states any of it. See F-352 for what would settle it. |
  | **never returns (UNSOURCED)** | **13** | The F-327 fabrication family, ruled by «#298». Re-verified absent at HEAD: all nine `io_pin_timing.yaml` keys and all four `basic-io.yaml` twins return `grep -c` = 0, and `grep -rn "150mA\|75mA\|~2000Ω\|3-7ns\|pull_up_modes\|pull_down_modes"` over `deliverables/ai/P2/` returns **0**. |

  45 + 1 + 1 + 13 = 60. **The dispatch's own numbers were checked against disk:** the body's "65
  blocks" is wrong (it is 60, as this entry already recorded), and the register header's
  **`Next gap ID: G-007` is stale** — `engineering/ingestion/KNOWLEDGE-GAPS.md` already allocates
  G-007 (Smart Pins / ADC, ANSWERED 2026-08-24). No G-number was allocated by «#299» for that
  reason; its gap is filed as F-352 instead.

  Two blocks were returned **corrected rather than verbatim**, as C4 required: both
  `internal_pull_resistors` blocks now teach the hardware-verified `P_HIGH_15K` + DIR-high /
  `P_LOW_15K` + DIR-low form from `architecture/pin-drive-configuration.yaml idioms` (EF-063,
  EF-064), and neither reintroduces a `pull_up_modes:` / `pull_down_modes:` key. Both
  `pin_architecture` blocks returned without the `drive_strength: 1.5mA to 150mA` line.

  `RESOLVED` — the record is written and executed against; only the YAML release is owed.

### Removal record — «#293», reconstructed by the arbiter 2026-08-25

| File | Top-level block removed | pre-removal line | span |
|---|---|---|---|
| `application-notes/p2an001-single-pin-instrumentation-adc.yaml` | `gotchas` | 92 | 16 |
| `application-notes/p2an002-cordic-for-real-work.yaml` | `gotchas` | 102 | 14 |
| `application-notes/p2an003-dac-analog-signal-generation.yaml` | `key_parameters` | 91 | 13 |
| `application-notes/p2an004-frequency-rotation-rc-timing-measurement.yaml` | `gotchas` | 97 | 16 |
| `architecture/boot-rom/_index.yaml` | `boot_timing` | 25 | 6 |
| `architecture/boot-rom/_index.yaml` | `boot_paths_summary` | 155 | 18 |
| `architecture/boot-rom/boot-pattern-selection.yaml` | `boot_time_clock_state` | 64 | 27 |
| `architecture/boot-rom/boot-pattern-selection.yaml` | `pin_triple_duty` | 64 | 27 |
| `architecture/boot-rom/spi-flash-boot.yaml` | `boot_pattern_trigger` | 29 | 7 |
| `architecture/click_module_integration.yaml` | `best_practices` | 185 | 25 |
| `architecture/clock_system.yaml` | `configuration_constants` | 22 | 34 |
| `architecture/clock_system.yaml` | `configuration_rules` | 22 | 34 |
| `architecture/clock_system.yaml` | `pll_system` | 98 | 65 |
| `architecture/clock_system.yaml` | `hubset_configuration` | 98 | 65 |
| `architecture/clock_system.yaml` | `clock_modes` | 98 | 65 |
| `architecture/clock_system.yaml` | `stabilization_timing` | 175 | 6 |
| `architecture/clock_system.yaml` | `clock_specifications` | 253 | 15 |
| `architecture/clock_system.yaml` | `anti_patterns` | 279 | 21 |
| `architecture/io_pin_timing.yaml` | `description` | 10 | 6 |
| `architecture/io_pin_timing.yaml` | `timing_specifications` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `clock_relationships` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `drive_strength_configurations` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `slew_rate_control` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `input_characteristics` | 90 | 173 |
| `architecture/io_pin_timing.yaml` | `special_timing_modes` | 298 | 40 |
| `architecture/io_pin_timing.yaml` | `protocol_timing_examples` | 298 | 40 |
| `architecture/io_pin_timing.yaml` | `compensation_techniques` | 359 | 33 |
| `architecture/io_pin_timing.yaml` | `best_practices` | 359 | 33 |
| `architecture/pin-power-domains.yaml` | `description` | 16 | 15 |
| `architecture/pin-power-domains.yaml` | `board_power_grouping` | 43 | 9 |
| `architecture/serial_loader.yaml` | `boot_sequence` | 11 | 26 |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `operation` | 21 | 6 |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `pin_behavior` | 55 | 7 |
| `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `pwm_characteristics` | 189 | 5 |
| `architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` | `detailed_description` | 8 | 13 |
| `architecture/smart_pin_patterns.yaml` | `notes` | 251 | 9 |
| `architecture/smart_pins.yaml` | `input_routing` | 148 | 19 |
| `architecture/smart_pins.yaml` | `related_components` | 405 | 7 |
| `architecture/smart_pins.yaml` | `electrical_limits` | 504 | 4 |
| `guides/pasm2-getting-started.yaml` | `file_structure` | 48 | 66 |
| `language/pasm2/concepts/basic-io.yaml` | `pin_architecture` | 40 | 49 |
| `language/pasm2/concepts/basic-io.yaml` | `control_registers` | 40 | 49 |
| `language/pasm2/concepts/basic-io.yaml` | `drive_strength_configuration` | 241 | 58 |
| `language/pasm2/concepts/basic-io.yaml` | `internal_pull_resistors` | 241 | 58 |
| `language/pasm2/concepts/basic-io.yaml` | `timing_considerations` | 371 | 6 |
| `language/pasm2/concepts/streamer_smartpin_control.yaml` | `protocol_client_code_note` | 480 | 8 |
| `language/pasm2/setxfrq.yaml` | `common_values` | 53 | 13 |
| `language/spin2/concepts/basic-io.yaml` | `pin_architecture` | 40 | 43 |
| `language/spin2/concepts/basic-io.yaml` | `control_registers` | 40 | 43 |
| `language/spin2/concepts/basic-io.yaml` | `drive_strength_configuration` | 173 | 66 |
| `language/spin2/concepts/basic-io.yaml` | `internal_pull_resistors` | 173 | 66 |
| `language/spin2/concepts/basic-io.yaml` | `timing_considerations` | 339 | 8 |
| `language/spin2/debug-commands/pc_key.yaml` | `description` | 4 | 5 |
| `language/spin2/debug-commands/pc_key.yaml` | `usage_rules` | 15 | 8 |
| `language/spin2/methods/getct.yaml` | `pitfalls` | 120 | 19 |
| `language/spin2/methods/waitms.yaml` | `notes` | 84 | 13 |
| `language/spin2/methods/waitms.yaml` | `limitations` | 84 | 13 |
| `language/spin2/methods/waitus.yaml` | `notes` | 92 | 20 |
| `language/spin2/methods/waitus.yaml` | `limitations` | 92 | 20 |
| `language/spin2/methods/waitus.yaml` | `clock_frequency_impact` | 92 | 20 |

**60 top-level blocks across 25 files.**

> **Disposition.** `RESOLVED` — the record exists now and is usable; it closes when «#299» has
> executed against it and every row carries a returned/not-returned outcome.

## WRPIN D-operand field map: three field descriptions wrong in the YAML, ten mode numbers footnote-fused in an ingestion artifact (2026-08-24, `KNOWLEDGE-GAPS` pass-6 catch-up) — F-331, F-332

### F-337 — the P2 Datasheet and the P2 Hardware Manual agree with each other and contradict the Silicon Doc on `%TT` in DAC_MODE, and the shipped YAML follows the minority source — `RESOLVED` (smart-mode row settled by EF-071; smart-pin-off row applied 2026-10-10, «#419», with no bench needed; closed 2026-11-07)
> **Closed 2026-11-07:** Served; the `%TT` rows are in the tree at v1.25.5.

> **Applied 2026-10-10 («#419»); closes when a release serves it.** The
> smart-pin-off row needs no bench (`bench-groupD-recheck.md` §3.2): the texts do not conflict there — the
> Datasheet names the DAC enable (DIR), the Silicon Doc the ADC enable (OUT), and Datasheet p.31 shows both;
> EF-055 measured the DAC driving at `TT=%00` with no OUT write. `smart_pins.yaml`
> `…behavior_by_context.smart_pin_off.dac_mode."%00"` now reads "DIR enables the DAC output; OUT enables the
> ADC; M[7:0] sets DAC level" with its `source`. The DAC smart-mode rows keep the Silicon Doc wording and
> the existing EF-071 TT-bit-0 condition.

> **Two disagreements, both in the `(T) Pin DIR/OUT Control` table, both about whether it is the
> DAC or the ADC that gets enabled.**
>
> | Context | Datasheet 2022/11/01 + Hardware Manual 2022/11/01 | Silicon Doc v35 |
> |---|---|---|
> | smart pin off, DAC_MODE, `%TT = 00` | **`DIR enables DAC`**, M[7:0] sets DAC level | **`OUT enables ADC`**, M[7:0] sets DAC level |
> | DAC smart-pin modes (`%SSSSS = %00001..%00011`), `0x` | `OUT enables **DAC** in DAC_MODE`, M[7:0] overridden | `OUT enables **ADC** in DAC_MODE`, M[7:0] overridden |
>
> **Verbatim locations, all four read this session:**
> `engineering/ingestion/sources/p2-datasheet/p2-datasheet-text.txt:1175` and `:1183` ·
> `engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:897` and `:905` ·
> `engineering/ingestion/sources/silicon-doc/part4-smart-pins.txt:83` and `:98`.
>
> **Where the KB stands.** `deliverables/ai/P2/architecture/smart_pins.yaml`
> `configuration_format.fields.tt.behavior_by_context` carries the **Silicon Doc** wording in both
> places (`dac_mode."%00": "OUT enables ADC, M[7:0] sets DAC level"` and
> `dac_smart_pin_modes.adc_control: "0x=OUT enables ADC..."`). Two agreeing 2022/11/01 sources say
> otherwise, and this is the field an agent reads to work out why a DAC will not drive.
>
> **Not resolved here, and not guessable.** EF-054/EF-055 already probed this bit family
> empirically (they established that `%01` switches the DAC's *source*), so the ledger may already
> settle it or be one short rig away from settling it. Empirical outranks both documentary
> sources; that is the route, not picking the majority.

## `object-image-dedup.yaml`'s map_caveat goes stale when pnut-ts 1.55.4 ships (2026-08-22) — F-320

### F-320 — `p2kbSpin2ObjectImageDedup`'s `map_caveat` warns readers off .map labels that 1.55.4 makes correct, while the limitation that SURVIVES the fix is documented nowhere. `RESOLVED` (closed by measurement 2026-10-07, «#387»; the one-clause addition is served; closed 2026-11-07)
> **Closed 2026-11-07:** Served; `map_caveat` read live 2026-11-07.
> **Measured 2026-10-07 on pnut-ts 1.55.8 — the limitation no longer survives.** The mirror-trap
> fixture (F-436; `drv` forked into images #2 and #3) maps its DAT symbol `BUF` as **two** SYMBOL
> INDEX rows — `BUF DAT #2 $00034` and `BUF DAT #3 $00068` — with an `Owner` column, and every
> method likewise once per image. The per-source-file SYMBOL INDEX this entry recorded on 1.55.3
> is gone, so there is nothing to document as a limitation (the KB carries the current edition
> only). `map_caveat` now says SYMBOL INDEX lists a forked symbol once per image, beside the
> ADDRESS INDEX clause it already had.

**Origin.** `engineering/ingestion/external-inputs/p2kb-update-requests/P2KB-map-caveat-retraction-1.55.4.md`
— an upstream request from the pnut-ts side proposing an amendment. Treated as **input, not
authority** ([[feedback_upstream_input_docs_not_authority]]): its finding was checked here, its
proposed text was not adopted.

**The site.** `deliverables/ai/P2/language/spin2/concepts/object-image-dedup.yaml:123-126` — the only
copy. Four other files reference the entry (`method-pointers`, `object_archetypes`, `OBJ`,
`shared-bus-replication`) but none duplicate the caveat.

### Measured HERE on pnut-ts 1.55.3, 2026-08-22 — the "before" baseline

Rebuilt the entry's own `cascade_through_tiers` fixture and read it as `verification.method` says
to. **The label defect reproduces, and is worse than the request describes:**

```
  case4  (1 methods)
      +-- A : casc_mid
      |   \-- LEAF : object_3          <- placeholder name
      |       \-- child_0 : object_4   <- a tier that DOES NOT EXIST
      \-- B : casc_leaf                <- wrong SOURCE FILE (B is casc_mid)
```

B's real child is absent and an extra tier is invented. **Send upstream as a 1.55.4 regression
check** if their fixtures do not already cover the invented-tier and wrong-source-file shapes.

Two things confirmed independently of the fix, and they are why the entry is otherwise sound:

- **`Objects: 5`** — exactly the entry's measured value. The count IS reliable, as the caveat says.
- **`SYMBOL INDEX` carries ONE `MTAG` ($00034) and ONE `LTAG` ($00048)** while `MEMORY LAYOUT`
  shows two images of each source. The second image's DAT addresses appear nowhere in that section.
  This is **structural — symbols are stored per source file — so it is NOT version-coupled and
  survives the 1.55.4 fix.** It is documented in no punch list here despite the request saying it is
  tracked, so this entry is also that gap's only record.

### The proposed text is REJECTED — it reinstates the shape PL-004 just stripped from this file

The request asks for prose reading *"Fixed in pnut-ts 1.55.4. Through 1.55.3 the multi-instance .map
could show… As of 1.55.4…"*, and offers a `verification.method` line *"confirmed correct at pnut-ts
1.55.4"* as an alternative anchor. **Both are build stamps.**

`[[reference_kb_is_always_latest_no_version_citations]]` — *cite the EDITION, never the BUILD* — uses
**this exact file** as its worked example: it said *"re-verify on a compiler version bump"* pinned at
v1.55.0 while v1.55.3 was installed; the bump had happened and the re-verify had not. PL-004 removed
the `toolchain:` field for that reason, and `verification.method` now carries the durable
replacement: *"Compiler-coupled behaviour: re-measure rather than assume if a result surprises you."*

The request understood half of it — it dropped its own `toolchain:` proposal as moot — then moved the
build numbers into prose. Same rot, different field.

### Amendment to apply (current-state only, nothing to maintain at the next bump)

```yaml
  map_caveat: |
    SYMBOL INDEX reports one row per SOURCE FILE, so when an override forks a file into
    several images only the first image's DAT address appears there. For per-instance DAT
    addresses read MEMORY LAYOUT or ADDRESS INDEX, which list every image. The Objects:
    count is reliable.
```

Nothing else in the entry needs changing: `description`, THE RULE, `singleton_rule`,
`forking_a_dat_region`, `the_silent_trap`, `the_other_silent_trap`, `cascade_through_tiers`,
`completeness_rule` and `verification.measured` all re-read clean against the request's own
re-measurement.

### Why it is HELD, and what releases it

**Sequencing is the whole reason.** On 1.55.3 the labels genuinely ARE wrong — measured above — so
dropping the warning while readers are still on 1.55.3 publishes guidance that is wrong for them.
The amendment is only correct once 1.55.4 is what people have.

Release conditions, both required:

1. **pnut-ts 1.55.4 is in this devcontainer**, so the fix can be verified here rather than taken on
   the request's word. The container is on 1.55.3 (`Build date: 8/9/2026`) as of filing.
2. **The compiler side's test source set is in hand** — offered 2026-08-22 and expected to evidence
   the new map details directly, so the fixtures do not have to be reconstructed from the entry's
   prose. Re-run the "before" shapes above against it; every one should invert.

Then: apply the amendment, and record the result in `verification.measured` **without a build
number**.

> ### GAP RECORDED 2026-08-25 («#300») — the HELD decision stands, and both release conditions were MEASURED
>
> This finding was on «#300»'s roster and **closes this sprint as a recorded gap, not as work**. Stephen's
> 2026-08-22 decision to hold it was **not re-opened, not re-argued, and the amendment was not applied.**
> The only thing done here was to check — rather than assume — whether the two release conditions this entry
> names have since been met. **Both are still unmet:**
>
> 1. **pnut-ts 1.55.4 is NOT in this devcontainer.** `pnut-ts --version` → **`PNut-TS: v1.55.3`**. The
>    compiler that makes the amended text true is still not the one installed, so publishing the amendment
>    now would hand 1.55.3 readers guidance that is wrong *for them* — the exact sequencing risk this entry
>    was held on.
> 2. **The compiler side's test source set is NOT in hand.**
>    `engineering/ingestion/external-inputs/p2kb-update-requests/` contains only the originating request,
>    `P2KB-map-caveat-retraction-1.55.4.md`. No fixture set accompanied it.
>
> **What would settle it:** both conditions together — 1.55.4 installed here, plus the fixtures — after which
> the entry's own "before" shapes (placeholder name, invented tier, wrong source file) are re-run and every
> one should invert. **Until then this is a gap, and the KB text stays as it is.**
>
> **The half that is NOT version-coupled remains this entry's only record**, and is unaffected by the hold:
> `SYMBOL INDEX` stores symbols **per source file**, so a forked file's second image has no row there. That
> survives 1.55.4 and is documented nowhere else.
