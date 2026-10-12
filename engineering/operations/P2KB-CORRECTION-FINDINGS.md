# P2KB Correction Findings — Consolidated Register

**Purpose:** the register of everything we find that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via `yaml-knowledge-base-maintenance`).

**This file carries OPEN work only.** Closed findings are archived, not kept here. Ask "what is
outstanding?" of this file alone — never re-derive completion state from an archive.

**How to use it:**
- When any work (manual production, audits, example compilation, ingestion, bench) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets an ID, a status, the exact location, what is wrong, the evidence, and the proposed correction.
- **Annotate as you fix, in the same pass** — flip the status, add an applied-note and source trace, and log newly-surfaced defects as new findings. A register whose statuses lag the YAML lies and invites re-chasing.
- **One finding lives in exactly one place.** When a finding is revised, **rewrite its entry in place**; never append a correction below the entry it corrects. The prior text is in git and in the archives.
- Consultation protocol (status-before-content, duplicate IDs are a STOP): the project's
  `REGISTER-CONSULTATION` protocol (agent-side; not shipped with this repo).

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `PARTIAL` (some of it applied; the rest still owed) · `PENDING-VALIDATION` (the fix is fully applied; only its validation — a render, a release, a re-test — is owed. Added 2026-08-21: the rule below already described this state and there was no token for it, so nine findings sat as `CONFIRMED` with "render owed" prose and tripped the hygiene gate on every run) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head) · **`RESOLVED`** (the defect is gone AND its validation has landed — the render/release/re-test was RUN and the artifact READ; a fix applied but unvalidated is `PENDING-VALIDATION`, never this. **Added to this legend 2026-08-25 («#302»): it was already the file's MOST-USED token — 31 of 82 entries — and the legend had never defined it, so a third of the register could not be classified by the very vocabulary this line exists to declare**) · `PARTIALLY CONFIRMED` (a ONE-OFF variant used only by F-202, where part of the claim is grounded in a source and part awaits silicon; it classifies as **`CONFIRMED` — open** — do not spread it).

⚠️ **`RESOLVED` entries are CLOSED and are awaiting the next archive sweep, not awaiting work.** Since 2026-10-05 the hygiene gate treats a live `RESOLVED` exactly like a live `DONE` — closed-but-live, a violation — so this file can only read CLEAN while it carries open work alone. Before that the gate let `RESOLVED` through, and closed findings piled up behind a CLEAN verdict: 119 of 179 live entries, with "what is outstanding?" overstated by two-thirds, until the «#386» reconciliation verified every entry against the tree and the release tags and swept the 130 closed ones (`correction-sweeps/2026-10-05-register-reconciliation-…`). **Close a finding by sweeping it, in the same pass that closes it.**

**A fix applied but not yet validated is NOT done** — it stays here until its validation lands (the `[~]` rule from `punch-list-maintenance`). That covers a YAML edit awaiting its EF entry, and a manual fix awaiting its re-test.

**Authority order for P2 facts:** empirical / hardware-verified results in `engineering/ingestion/external-sources/hardware-verification/` (strongest — they have overturned every other tier) → the `pnut-ts` compiler, for legality only → Parallax documentary sources under `engineering/ingestion/sources/` → the published P2KB YAML. Community/forum material is an upstream lead, never a citable authority.

**No inference or derivation.** Every correction must trace to an authoritative source. Aligning a file to an authority it contradicts is fine; **inventing a value or claim that no source states — by computation, reasoning, or "it must logically be" — is not.** If a change can only be justified by inference, log it as a finding that needs a source. Match the source's wording, not an interpretive paraphrase.

**Next finding ID: `F-576`** · gap IDs are **not allocated here** — `engineering/ingestion/KNOWLEDGE-GAPS.md` owns the `G-` allocator and declares its own counter. (This line previously carried `Next gap ID: G-008`, stale by fourteen against that register's actual G-022; two registers claiming one allocator is the collision `audit-register-hygiene.py` exists to catch. Retired 2026-08-26 — see F-352 for the earlier, smaller instance of the same drift.)

**Archives** — search them before re-filing; a finding that reappears is usually a regression:
- F-001…F-124 → `correction-sweeps/2026-06-13-P2KB-CORRECTION-FINDINGS-archive.md`
- F-125…F-266 (closed) → `correction-sweeps/2026-08-15-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-08-19 (18 findings: F-227, F-228, F-254, F-255, F-257, F-258, F-259, F-260, F-261, F-262, F-263, F-264, F-265, F-266, F-267, F-269, F-270, F-273) → `correction-sweeps/2026-08-19-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-09-10 (1 finding: F-415, `RESOLVED-INVALID`) → `correction-sweeps/2026-09-10-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-01 (24 findings: F-449, F-450, F-451, F-452, F-462, F-463, F-464, F-465, F-466, F-467, F-468, F-469, F-470, F-471, F-472, F-473, F-474, F-475, F-476, F-477, F-478, F-480, F-481, F-482) → `correction-sweeps/2026-10-01-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-03 (45 findings: F-440, F-445, F-446, F-447, F-448, F-483…F-505, F-506…F-520, F-522) → `correction-sweeps/2026-10-03-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 (4 findings: F-400, F-523, F-526, F-540) → `correction-sweeps/2026-10-04-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 after the manual releases (2 findings: F-521, F-524) → `correction-sweeps/2026-10-04-manual-releases-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 after the Debug Window v1.1.4 release (1 finding: F-531) → `correction-sweeps/2026-10-04-debug-window-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 after the Streamer Guide v1.1.3 release (2 findings: F-539, F-479) → `correction-sweeps/2026-10-04-streamer-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the XBYTE Guide v1.1.1 release (2 findings: F-537, F-538) → `correction-sweeps/2026-10-05-xbyte-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the I/O & Smart Pins v1.0.11 release (4 findings: F-533, F-534, F-535, F-536) → `correction-sweeps/2026-10-05-iosp-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the Assembly Reference v3.1.11 release (4 findings: F-527 `RESOLVED-INVALID`, F-528, F-530, F-541) → `correction-sweeps/2026-10-05-assembly-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the deSilva v3.0.9 release (3 findings: F-529, F-532, F-276) → `correction-sweeps/2026-10-05-desilva-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 by the register reconciliation «#386» (130 findings verified closed against the tree and the release tags; 63 emptied section headings moved with them) → `correction-sweeps/2026-10-05-register-reconciliation-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-10 by the close-out sprint «#423» (5 findings with nothing left to validate or ship: F-218, F-336, F-364, F-405, F-441) → `correction-sweeps/2026-10-10-close-out-sprint-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-11 by the close-out release MCP validation «#398» (34 findings: F-381, F-383, F-386, F-387, F-389, F-392, F-393, F-398, F-421, F-436, F-439, F-454, F-525, F-542, F-543, F-544, F-546, F-547, F-548, F-549, F-550, F-551, F-552, F-553, F-554, F-555, F-556, F-557, F-558, F-559, F-560, F-563, F-568, F-570) → `correction-sweeps/2026-10-11-mcp-validation-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-11 at the v1.24.1 release «#398» (1 finding: F-572) → `correction-sweeps/2026-10-11-v1.24.1-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-12 at the v1.24.3 release «#425» (1 finding: F-573) → `correction-sweeps/2026-10-12-v1.24.3-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-12 at the v1.24.5 release (1 finding: F-574) → `correction-sweeps/2026-10-12-v1.24.5-P2KB-CORRECTION-FINDINGS-archive.md`

> **Swept 2026-08-19** per `punch-list-maintenance`, as **rename-then-trim** (the archive is a
> git-tracked rename of the original; both files are subtractions from a preserved copy — see the
> skill's project overlay for why building the output loses content). 18 findings archived, 3,559 →
> 2,478 lines. **Classified by STATUS TOKEN only.** Sixteen findings whose headline reads "source
> fixed"/"tool fixed" **stayed open**, because their status is still `CONFIRMED` and most say
> "render owed" — this file's own rule is that a fix applied but not yet validated is NOT done. A
> first pass that trusted the prose would have archived all sixteen. Verified with
> `audit-register-hygiene.py --sweep-check`, which reads the pre-sweep revision out of git.
>
> **Swept 2026-08-15** per `punch-list-maintenance`: 129 closed findings archived, 3,161 lines → this
> file. The previous sweep was deferred on 2026-06-20 pending G-004 and G-005; G-005 closed
> 2026-07-04, and G-004's remainder was found to be out of KB scope entirely (see its entry), so the
> deferral's condition is discharged.

---




## Found during the 2026-10 manual releases, the register reconciliation and the pre-release audit (2026-10-04/07) — F-546 … F-562 (+ F-563, found 2026-10-09 by the VO-J-035 rework; + F-564, found 2026-10-09 by «#414»; + F-565, found 2026-10-09 by «#415»; + F-566, found 2026-10-10 by «#422»; + F-567, found 2026-10-10 by «#422»/«#423»; + F-568, F-569, found 2026-10-10 by «#422»; + F-570, reported 2026-10-10 by Stephen; + F-571, F-572, F-573, found 2026-10-11 by «#398» and the MCP agent's 1.5.1 review; + F-574, reported 2026-10-12 by Stephen; + F-575, found 2026-10-12 by the debug-techniques study)

### F-575 — P2AN006 ships a stack checker whose depth scan under-reports, and that is not safe for two cogs at once — `CONFIRMED` (found 2026-10-12 by the debug-techniques study; «#426»)

**Where.** P2AN006 *Sizing Cog & Task Stacks* v1.0.1: `app-notes/P2AN006/examples-library/isp_stack_check.spin2`,
the 2022 version (md5 `f75cbec4…`), shipped verbatim. The same copy sits in the Debug Window manual's
`REF/robot-dog/` (reference only, not shipped).

**What is wrong.**
1. `getStackDepth()` scans UPWARD from index 0 and stops at the first long still holding
   `NOT_WRITTEN_MARK`. That equals the high-water mark only if the used region has no gaps.
   **Scope, checked 2026-10-12:** the source says a frame that reserves longs it never writes stops
   the scan early. But Spin2 v55 (`spin2-v55-text.txt:286`) says "Results and local variables are
   initialized to zero on method entry", so a pure Spin2 frame writes every long it reserves and leaves
   no gap. The under-report is therefore NOT demonstrated for Spin2 code. A gap needs something that
   advances the stack without writing, such as PASM using `PTRA` as a stack, which is not measured. The
   downward scan is equal or better in every case, so it ships. The note describes the new scan and
   claims nothing about the old one. This goes to the debug-techniques claim ledger («#427»), source
   §7.3, as a contested claim.
2. The scratch values, including that scan's loop index `nStkChkIdx`, live in `DAT`. All declarations
   share one `DAT`, so two cogs scanning at once overwrite each other's index. The note presents
   "one checker at a time" as the utility's limitation.

**Evidence.** Stephen's current version of the object
(`appNote-fodder-NO-COMMIT/p2-debug techniques/isp_stack_check.spin2`, updated 2026-09-09) scans
DOWNWARD and records both defects and their history in its comments. It compiles under `pnut-ts -d`
1.55.8.

**Correction.**
- Stephen reviews a cleaned copy (header date updated, the SD project's file names reworded
  generically) and adopts it as the master.
- P2AN006 then ships it verbatim, with the note's text updated: the depth semantics, the
  saturated-reading case, concurrent checkers now safe, and the new `isStackGuardIntact()` and
  byte-guard methods.
- Release P2AN006 v1.0.2.

### F-571 — `p2kb_obex_get` shows a zero quality score and an empty created date for every OBEX object — `PARTIAL` (found 2026-10-11 by the close-out release MCP test, step 5, «#398»; the date moved KB-side 2026-10-11 for v1.24.1; the KB is a pure mirror from v1.24.4; the server half, including dead download links, is requested for p2kb-mcp 1.5.1)
**Updated 2026-10-12 (KB v1.24.4, "pure mirror"):**
- Every object is now the catalog's fields only. `version`, `file_size`, `author_username` and the
  other fields the server's struct reads are gone. The change request (§2, §3.2, §3.3) now asks the
  server to drop them too.
- All 130 objects carry a date: 2816's came back with the v1.24.2 mirror.
- **New for 1.5.1 (§3.6):** 5 objects (4442, 4571, 4581, 4616, 4617) have no download on OBEX, and
  their YAML now has no `download_direct`. A server that builds the URL from the id hands agents a
  link that answers `invalid!`. The request asks the server to take `download_url` from
  `urls.download_direct` and omit it when absent. Probe O3 now tests this (4581), replacing the
  2816 no-date probe.
- `scrape-obex-repos.py` is retired; `obex-catalog-mirror.py` writes the date.

**Applied 2026-10-11 (Stephen: "yes a now"):** the upload date moved from
`version_tracking.obex_upload_date` to `object_metadata.metadata.created_date` in all 129 objects that
had one then. Proved against HEAD: all 131 files (130 objects and the template) parse equal to before apart from that move (and 2842's
`known_issues` clearing). **Requested for p2kb-mcp 1.5.1** (Stephen, 2026-10-11):
`engineering/tools/p2kb-mcp/MCP-OBEX-SUMMARY-CHANGE-REQUEST.md` — remove `quality`, omit empty fields,
drop dead struct fields, add `full_metadata` (the whole filtered object, ending field-name coupling);
acceptance probes O1-O7 there. `OBEX-IMPLEMENTATION-SPEC.md` and `P2KB-MCP-SPECIFICATION.md` updated
to the same contract. **Date half validated live 2026-10-11** on p2kb-mcp 1.5.0 against v1.24.1:
`p2kb_obex_get 2842` → `metadata.created_date: "2022-01-04"`; 2816 → `""` (no date). `quality: 0`
remains until 1.5.1. **Release-day note:** the first refreshes after the push ran inside GitHub raw's
5-minute CDN window — a normal refresh reported 0 stale keys and kept pre-release bodies, and a flush
inside the window made every OBEX object fail verification (old bodies vs new index: "not found",
"verification failed"). A flush after the window cleared both. Probe a release only after ~5 minutes.
Probed on p2kb-mcp **1.5.0** against KB v1.24.0, after `p2kb_refresh include_obex` (0 stale entries).
`p2kb_obex_get 2842` returns a curated summary, not the object. **What the server reads** — the YAML
tags compiled into the v1.5.0 linux-amd64 binary: `object_metadata` → `title`, `author`,
`author_username`, `urls.*`, `technical_details.*`, `functionality.*`, and a block `metadata` →
`created_date`, `quality_score`, `discovery_date`, `last_verified`, `extraction_status`. It parses no
`compatibility` and no `version_tracking`. (`engineering/tools/p2kb-mcp/OBEX-IMPLEMENTATION-SPEC.md`
specifies a `full_metadata` field — the whole object — which the server does not return.)
- `metadata.quality: 0` — the KB removed `quality_score` («#422»; we do not rate OBEX objects), so the
  server shows Go's zero value, which reads as a rating of zero. **Server-side only:** no KB value can
  remove it short of inventing a score.
- `metadata.created_date: ""` — `object_metadata.metadata` was renamed `scrape_tracking` (filtered at
  delivery; F-545), so the server finds nothing. The real upload date is served as
  `version_tracking.obex_upload_date` (`'2022-01-04'` for 2842; 129 of the 130 objects carry one).
  **KB-side option:** move it to `object_metadata.metadata.created_date` (a fact about the object, not
  scraper bookkeeping) and have `scrape-obex-repos.py` write it there — the server then shows it with no
  change. Stephen's call, asked 2026-10-11.

**`known_issues` is withdrawn from this finding (Stephen, 2026-10-11):** "It's not up to us to be rating
OBEX content." The CP-010 compile verdict was removed from object 2842 and from the four pages that
repeated it (three JonnyMac convention pages, the Spin2 getting-started guide); the language fact it
rests on — `field` cannot name a method local — now lives on `language/spin2/operators/FIELD.yaml`, and
CP-010's KB home moved there. Doctrine overlay: *An OBEX entry carries what the catalog says, never our
verdict on it.*

**The KB body is correct:** `p2kb_get p2kbCommunity2842` serves the filtered object (no
`scrape_tracking`). v1.4.0 showed the same summary mapping (test record step 3,
`correction-sweeps/2026-10-11-close-out-release-mcp-test.md`, git-ignored).
**Owed:** the date per Stephen's call; in the MCP server, drop `quality` (or return the whole filtered
object as the OBEX spec says, which ends field-name coupling for good). Re-probe 2842 on the release
that carries each.

### F-569 — the new provenance-key gate's census: three provenance keys still reach agents, and the OBEX tooling it touched has two defects — `NEEDS-VERIFICATION` (found 2026-10-10, «#422»)
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

### F-567 — `hardware/hub75_adapter.yaml` is an Iron Sheep board no Parallax document describes, so it fails the claim-sourcing gate (3 Tier 1) and the source-lock ratchet — `PENDING-VALIDATION` (applied 2026-10-10, «#422»; Q-012 answered the same day; closes when the next KB release serves it)

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

### F-566 — Parallax moved www.parallax.com to Shopify; every Quick Bytes article now lives on the OBEX docs site, so all 42 catalog entries cited a dead root — `PENDING-VALIDATION` (applied 2026-10-10, «#422»; closes when the next KB release serves it)
Found 2026-10-10 by «#422» checking S-390: `community/quick-bytes/simple-analog-input.yaml` cited
`https://www.parallax.com/simple-analog-input/`, which returned HTTP 404. Stephen's reading: the site moved, so
"quick bytes urls may have changed ... all should be rerooted the same way". **Applied:** all 42 entries in
`community/quick-bytes/` now cite `https://obex.parallax.com/docs/quick-bytes/propeller-2/<slug>/` in `url:`,
`modalities.article` and `modalities.source_code.get_from` (the arbiter fetched each: HTTP 200). 30 slugs were
unchanged; 12 moved and `slug:` is updated (the filenames keep the old slugs — they are KB keys):
`breakout-board-options-for-p2`, `dht11-dht22-cm2302-object`, `floating-point-math`, `i2c-device-bus-scanner`,
`i-o-test-utility-with-led-matrix`, `multiple-serial-port-16-object`, `p2-simple-video-driver-using-images-intro-to-using-video-2-of-3`,
`rotary-encoder`, `smart-pins-tsl235r`, `video-hardware-character-map`, `visual-studio`, `wireless-programming`.
The six hardware pages that linked a Quick Bytes article (`addon-goertzel-touch`, `addon-control-board`,
`addon-av-breakout` x3, `addon-led-matrix`) were re-rooted the same way. **Downloads:** the old
`download_mechanism: parallax-download-manager` is gone; each article page now lists its code as plain
`/qbi/downloads/<file>` links on `obex.parallax.com` with no login wording on the page, so the field reads
`direct-link`. `download_count` / `has_code` were corrected to what each page lists (flash reader 4→6, neopixel
1→3, rotary 3→4, 32-channel ADC 1→2, DHT 2→1, DS3231 2→1, LED-matrix test 3→1; multi-servo, floating-point and
serial-16 `has_code` false→true; wireless programming true→false, its page offers only a Google Drive
firmware link, already in `reference_links`). `addon-av-breakout`'s character-map `source_package` now names
the file the page lists. **`code_author` of `simple-analog-input.yaml`:** the new page's Document Author and
Source Code Author blocks read "John Doe" and "Jane Doe" — template placeholders, not authors — so `code_author`
stays `''` and `author: Ken Gracey` stands (the page carries no published date). The claim-sourcing gate
(`audit-yaml-claim-sourcing.py` `CATALOG_URL_RE`) now accepts the `obex.parallax.com/docs/quick-bytes/` root
beside `parallax.com/`; a non-Parallax host is still refused. **Owed:** other `www.parallax.com` links in the
hardware pages that are not Quick Bytes articles (`/usbdrivers`, `/product/p2-to-mikrobus-click-adapter`, the
bare home page) were not probed under the request to keep traffic to Parallax light; and the download links
themselves were read from the pages, not fetched, so `auth_gated: false` rests on the page showing no gate.

### F-565 — `keywords/STRUCT.yaml` `gotchas.struct_pointer_obj_returns` said `pCfg := sensor.getConfig()` is a COMPILE ERROR for structures over 15 longs; no ingested source and no compile-proof record states it — `NEEDS-VERIFICATION` (compile probe)
Found 2026-10-09 by «#415» fixing `language/spin2/keywords/STRUCT.yaml`. The page carried a
`wrong:`/`correct:` pair (`pCfg := sensor.getConfig()  ' COMPILE ERROR for large structs` against
`[pCfg] := sensor.getConfig()`), the explanation that "the compiler may interpret the return as the full
structure", and the scope "only across OBJ boundaries". Both pair strings were manifest class `not-code`
(a one-line string cannot declare the `sensor` OBJ), so the gate never compiled them. The only origin is
the upstream lead `external-inputs/pnut_ts_facts/Pointer-Usage-Guide.md` (not an authority); Spin2 v55's
VAR Blocks section states only that a pointer variable named alone is the pointed-to variable and
`[ptrvar]` is the pointer itself (`spin2-v55-text.txt:249-261`); the interpreter has no typed-pointer
bytecode; no EF or CP record covers the call. **Applied now:** the pair, the compile-error claim and the
scope sentence are removed; the page states the v55 pointer semantics (a bare `pCfg :=` writes through
the pointer, `[pCfg] :=` stores the pointer) and keeps the compiled bracket-form example. **Question
(compile probe, no hardware):** with a child object returning a `^StructName` of 16 or more longs,
does `pCfg := child.getConfig()` fail to compile, and with what message? **Fix when answered:** record a
CP-NNN in `COMPILE-PROOFS.md`; if it fails, restore the "wrong" form as a `never` block citing it. The
same pair sat in `operators/typed-pointers.yaml` (`gotchas.struct_pointer_obj_returns`); **«#416»
applied the same treatment there on 2026-10-10** (the pair, the compile-error claim and the scope sentence
removed, the v55 pointer semantics stated, the bracket-form example kept). The CP-NNN question above
now covers both pages.

### F-564 — what a stopped cog leaves on the pins and in smart-pin modes is stated nowhere in the ingested sources; `cogstop.yaml` shipped three claims about it — `NEEDS-VERIFICATION` (bench question)
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

### F-562 — `hub75_adapter.yaml` names the OBEX driver and URL differently from OBEX 2850's own metadata — `NEEDS-VERIFICATION`
Found 2026-10-07 by the independent check of F-556. `hardware/hub75_adapter.yaml:156,158` gives
"P2-HUB75 LED Matrix Driver" and `https://obex.parallax.com/obex/p2-hub75-led-matrix-driver/`;
`engineering/ingestion/external-inputs/source-code/obex-projects/2850-ISP_Hub75_Matrix_Driver/2850_metadata.yaml:51,57`
gives "ISP Hub75 Matrix Driver" and `.../isp-hub75-matrix-driver/`. Which is current is unverified
(no network probe here). **Fix:** confirm against the OBEX listing the user can open; use that.

> **Applied 2026-10-10 («#420»); the entry stays NEEDS-VERIFICATION until Stephen opens the live
> listing.** `hub75_adapter.yaml` `resources.obex` now reads "ISP Hub75 Matrix Driver" and
> `https://obex.parallax.com/obex/isp-hub75-matrix-driver/` — the form in `2850_metadata.yaml:51,57`
> (downloaded 2025-09-13) and in the KB's own OBEX object page (`community/obex/objects/2850.yaml:50,56`),
> which already agreed with each other; the old name was the GitHub repository's. **Not verifiable
> here:** whether the live OBEX listing still carries that title and path (no network). Stephen:
> open `https://obex.parallax.com/obex/isp-hub75-matrix-driver/` and say if it resolves.

### F-561 — P2AN003 (app note + YAML companion) says reversing the DAC init order "leaves the first output cycle undefined"; the P2 Documentation says Y is captured in reset — `PARTIAL` (companion half applied 2026-10-10, «#420», and `PENDING-VALIDATION`; the app-note prose and the "undefined" clause change together at the app-note release)
Found 2026-10-07 by the independent check of F-554. `app-notes/P2AN003/opus-master/P2AN003.md:541`
and its companion `application-notes/p2an003-dac-analog-signal-generation.yaml:98` ("the universal
smart-pin init order. Reversing it leaves the first output cycle undefined"). For the DAC modes
the P2 Documentation says "During reset (DIR=0), IN is low and Y.[15..0] is captured"
(`silicon-doc-text.txt:3946`, `:3963`) — a WYPIN before DIR is raised is captured, not lost; no
source states the "undefined" outcome, and "universal" overclaims (EF-090 exception). **Fix:** the
app note and its companion together (the agreement gate), as an app-note correction release —
state the order as the general one and drop the unsourced consequence, or source it.

> **Half applied 2026-10-10 («#420»), by the agreement gate's own rule.** The companion
> `p2an003-dac-analog-signal-generation.yaml` `gotchas[0]` no longer says "the universal smart-pin init
> order" (the app note never said it). The clause "Reversing it leaves the first output cycle
> undefined" is **kept in both** — the published app-note text (`P2AN003.md:541`) states the same, so
> changing the companion alone would put them in disagreement. It changes in the app-note release
> together with the prose.

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

### F-545 — provenance ships under keys the delivery filter does not list (`last_verified`, `extraction_status`, `authority_tier`, `grounding`, …) — `PARTIAL` (census, folds, the `scrape_tracking` filter key and the new-key gate applied 2026-10-10, «#420»/«#422», `PENDING-VALIDATION`; three served provenance keys remain, F-569)
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

## Impact survey — v1.24.5 (`release-yamls` §8, run 2026-10-12)

v1.24.5 reverses v1.24.4's silicon sweep (F-574). The 12 YAMLs are back to their pre-sweep served
text. `basic-io`'s one addition is a `source:` line, which the delivery filter strips. So every
manual's declared sources match what the manual was written against. **The v1.24.4 survey's
Assembly-manual re-audit flag below is withdrawn**: the KB again states the "(Rev B/C silicon)" and
"Rev C" framing the manual uses. **No document is flagged.**

## Impact survey — v1.24.4 (`release-yamls` §8, run 2026-10-12)

**What v1.24.4 changed:**
- The 130 OBEX objects became a pure catalog mirror. No document quotes the removed fields.
- 12 content YAMLs dropped their silicon-revision framing: GETCT ×2, `special_registers`,
  `serial_loader`, the errata status on AUGS/AUGD/SETQ blocks, GETXACC, the Goertzel page,
  `P_ADC_FLOAT`, `silicon_errata` and `basic-io`. Stephen, 2026-10-12: Rev C is the only P2 silicon.

**By manual:**
- **Declared sources:** P2AN001 and P2AN003 declare the ADC smart-pin page. Its only change is the
  `P_ADC_FLOAT` parenthetical, which neither note uses, so neither is affected.
- **Flagged: re-audit against HEAD, the P2 Assembly Language Manual.** Its opus-master states the
  same framing the KB dropped:
  - `special-registers.md:534`, `instructions-g.md:94,106` and `chapter-04-timing.md:545`: "64-bit
    counter (Rev B/C silicon)";
  - `appendix-j-known-bugs.md:86`: "affect all P2X8C4M64P Rev B/C silicon";
  - its `[Rev C]{.silicon-note}` markers, e.g. `appendix-e-constants.md:687`, a deliberate device of
    the manual (its CHANGELOG: "Rev C silicon notes").

  Whether that device stays is decided at the manual's re-audit; the KB side is done.
- **Not affected:** the P2 Errata's "confirmed on Rev C silicon by a test program" is a true record
  of what was run. The other "Rev B/C" hits are citations of the P2 Documentation's own title.

## Impact survey — v1.24.2 and v1.24.3 (`release-yamls` §8, run 2026-10-12)

Both releases changed the 130 OBEX objects only (catalog re-mirror, one-liners, `file_size` emptied,
`languages_confirmed` and `obex_version` removed; F-573). The one live document that names OBEX
objects is P2AN002 (#2811, #2812, #5278, #5361 in its text and Resources): its credits and claims
still hold against the mirrored data — "ersmith" is Eric R. Smith's handle (OBEX now lists the name),
and its titles differ from OBEX's only in punctuation and case ("FFT/IFFT" vs "FFT IFFT"). No manual
quotes an OBEX description, category or size. **No document is flagged.** Published state verified
live on p2kb-mcp 1.5.0.

## Impact survey — v1.24.1 (`release-yamls` §8, run 2026-10-11)

v1.24.1 changed one fact: `field` cannot name a method local (FIELD.yaml, CP-010). Every other hunk
moves provenance into stripped fields, removes pointers to material the KB does not have, or relocates
the OBEX upload date — no served fact changes. No live manual declares a local named `field` (grep of
every `opus-master/` for a PUB/PRI local list containing it: none). The Getting Started guide names
`jm_fullduplexserial` (OBEX 2842) in three `OBJ` shape examples (getting-started-body.md:342, 470, 746)
that illustrate block structure; none is in its compiled examples library, and the guide makes no claim
about the object, so the KB's removal of the compile verdict leaves it unaffected. **No document is
flagged.** Published state verified live on p2kb-mcp 1.5.0 (F-572 probes).

## Impact survey — v1.23.2 (`release-yamls` §8, run 2026-10-04)

v1.23.2 changed two facts, both decided on the bench (EF-090, EF-091). Sync serial TX primes its first
word in reset: the I/O & Smart Pins guide already teaches this (ch11:292-296), and F-533's fix text
carries it; no other live document teaches `%11100` ordering (the «#378» audit's per-document reads).
A `##` operand's AUGS takes a skip-pattern bit: the XBYTE guide already teaches it (xbyte-body.md:321-328);
the Assembly Reference states no skip-pattern AUGS rule («#378» G1: NOT-TAUGHT). **No document is
flagged.** Published state verified from raw.githubusercontent.com (both new sentences served); the
running p2kb-mcp needs a restart before F-526/F-540 can flip to `DONE`.

## Impact survey — v1.23.1 (`release-yamls` §8, run 2026-10-03)

v1.23.1 changed no fact: every edit moved a citation or a provenance key out of the shipped text
(F-523, F-400). No live document teaches a fact this release changed, so **no document is flagged.**
Published state verified from outside (raw.githubusercontent.com): `guides/pasm2-getting-started.yaml`
served = HEAD blob, sha256 = the published index entry, `v55:` shorthand absent. The running p2kb-mcp
refused it ("verification failed") — its boot-time index snapshot predates the release; F-523 and F-400
flip to `DONE` on the first served probe after an MCP restart.

## Impact survey — v1.23.0 (`release-yamls` §8, run 2026-10-03)

v1.23.0 changed facts (not only wording) in areas these live documents teach. Each flag is a
**re-audit-against-HEAD** signal for that document's next pass; the grep that located each
concrete site is the evidence, and the audit decides the fix.

| Document | What changed in the KB | Located in the manual |
|---|---|---|
| Architect's Guide | latest-wins mailbox handshake is load-bearing (F-507) | `architect-guide-body.md:919` states the disproven claim — **F-524** |
| P2AN007 | the re-check-the-sequence option is unsafe (F-521) | `P2AN007.md:214` (and the Tip below it) — owed under F-521 |
| Streamer Guide | GETXACC clears only during a Goertzel burst (F-506); streamer-DAC pin needs `P_CHANNEL` (F-513) | GETXACC: already open as F-479 |
| DEBUG Window Manual | SCOPE_XY DOTSIZE / SCOPE LINESIZE half-pixels (F-508); PLOT/MIDI COLOR, BITMAP SET, RATE un-freeze (F-516, F-518); DEBUG_TIMESTAMP stale-window caveat (F-514) | 6 files mention DOTSIZE/LINESIZE units — check each |
| I/O & Smart Pins | PINSTART Yval lost in trigger/serial modes (F-509); NCO Y = 0 (F-510); %10010 restart (F-511); DAC TT bit 0 (F-512); WRPIN pin-first (F-522) | no PINSTART-with-trigger-Yval site found (grep); the rest to the audit |
| P2AN003 | DAC smart-pin modes: OUT runs the ADC only with TT bit 0 (F-512) | to the audit |
| Assembly Reference | DEBUG_TIMESTAMP stale-window caveat (F-514); GETCT pair overhead (F-515, already stated as 2 in ch. 4) | 4 DEBUG_TIMESTAMP sites — check against the caveat |

No other live document's subject intersects the v1.23.0 fact changes; the F-519 id strip changes
no fact.

F-524 (the Architect's Guide mailbox claim) is DONE and archived — `correction-sweeps/2026-10-04-manual-releases-P2KB-CORRECTION-FINDINGS-archive.md`.

## Impact survey — v1.22.0 (`release-yamls` §8, run 2026-10-01)

The v1.22.0 delta (21 YAMLs: the P2 Errata silicon findings — `rdfast` + hub read/write family,
`setq`/`wmlong`/`setq_block_ops`, `augs`, `getct` + Spin2 `getct`/`getms`/`getsec`, `getxacc`,
`brk`, `muldiv64`, `wrpin`, `architecture/hub` and `smart_pins`) was intersected against every live
manual's declared sources, then each intersecting master was grepped for the statements the delta
contradicts (capture-and-clear GETXACC, conditional BRK, signed MULDIV64, `address & 7` slicing,
no-wait RDFAST use, GETSEC "long-duration").

- **Streamer Guide — DEFECT FOUND → F-479** (GETXACC capture-and-clear, §10.6 and §17.1).
- **Assembly Reference and deSilva — carried by «#352»** (its body names every entry: GETCT, GETXACC,
  RDFAST and the hub read/write family, SETQ, AUGS, BRK, Appendix J).
- **Architect Guide, Getting Started, I/O & Smart Pins, Single-Step Debugger, XBYTE — intersect, no
  contradicted statement found** by the targeted grep; re-audit against HEAD at each one's next pass
  (IOSP: the DAC-mode `TT` rule and §16.3's MULDIV64 ratio; Single-Step: its BRK material). XBYTE checked: every `RDFAST` it
  shows is `rdfast #0, …` — the waiting form — so E7 does not reach it.
- **No impact:** Debug Window, PNut-TS Terminal Guide. P2 Errata grounds on the silicon itself.

## Impact survey — v1.21.0 (`release-yamls` §8, run 2026-09-22)

The v1.21.0 delta (38 files: `hardware/`, `architecture/smart-pins|streamer|locks`,
`language/pasm2`, `language/spin2`, one app note) was intersected against every live manual's
`MANUAL-DESCRIPTOR.md` declared sources. **Two manuals intersect; eight do not.**

- **Assembly Reference — intersects `language/pasm2/`, `language/spin2/`, and is ALREADY ALIGNED.**
  Every flag-field correction this release shipped (`SUMC`/`SUMNC`/`SUMZ`/`SUMNZ` true-sign,
  `INCMOD`'s wrap, `RCR`'s shifted-out bit, `GETCT`'s WC-as-selector) was applied to the manual in
  «#348» *before* the YAML caught up, so the two trees now agree — verified in `appendix-a`
  (4 / 1 / 8 occurrences). **One row lags and is already recorded:** `LOC` moved to `category: Branch`
  here, and the manual still groups it under Arithmetic. That is on
  `workspace/p2-assembly-language-manual/PUNCH-LIST.md` with an expiry of the next Assembly release,
  including the note that Appendix C's per-category counts must be recomputed when the row moves.
  **No new flag needed.**
- **deSilva Tutorial — intersects `language/pasm2/`, `language/spin2/`; flag recorded here** because
  that manual has no punch list of its own. **Re-audit against HEAD at its next pass**, specifically
  for: the `SUM*`/`INCMOD`/`RCR` flag effects, `GETCT`'s WC (a selector, not a flag write), `LOC`'s
  category, and — most likely to bite a tutorial — the Spin2 `||` operator, which on P1 meant
  absolute value and on P2 means logical OR. A tutorial aimed at P1 refugees is exactly where that
  one does damage.
- **No impact:** Architect Guide, Debug Window, Getting Started, I/O & Smart Pins, Single-Step
  Debugger, Streamer Guide, XBYTE Guide, PNut-TS Terminal Guide. Recorded so the survey is visibly
  done rather than skipped.

## ✅ YAML-HEAD DRAIN GATE — evaluated 2026-09-22 («#351»): **GREEN**

The gate (`document-audit` §2) asks one question: are there **actionable** pending YAML corrections —
information not reaching the agents that consume this KB live? It had never been evaluated. All 61
open findings were classified, each **verified against the tree rather than read off its status**,
because the register lags reality and a stale `CONFIRMED` is indistinguishable from a live defect.

**Result: no actionable YAML correction remains open. The gate is GREEN.**

| Classification | n | Meaning |
|---|--:|---|
| **Landed this pass** | 13 | F-449, F-450, F-451, F-452, F-453, F-387, F-392(part), F-393, F-394, plus F-454…F-459 from «#350» |
| **Already done, status was lagging** | 8 | F-382, F-383, F-386(part), F-388, F-329, F-348, F-374, F-352 |
| **Blocked on external — parked, does NOT gate** | 7 | F-372, F-354, F-400, F-336, F-337, F-202, F-208 |
| **Not YAML — outside this gate's scope** | 15+ | tooling (F-405, F-439, F-376, F-389, F-381), ingestion (F-421, F-367, F-332, F-344, F-341), manuals (F-356, F-274, F-276, F-278, F-280, F-424, F-207, F-203, F-218), platform/PDF (F-316, F-317, F-300, F-301, F-299, F-319) |

**Why the parked set does not gate, individually:**
- **F-372** (`%11011` says a new WRPIN needs no reset, against the same document's general rule) —
  settles only on a bench: configure a USB pair, WRPIN with DIR high, observe. Jumper-only, so it is
  a *runnable* test, not an out-of-scope one. Class B periphery.
- **F-354** — six of eight items need an acquisition this repo does not hold (a level-shifter
  datasheet, ISP HUB75 driver docs, the #64013 and #64006 schematics, OBEX `psram.spin2` docs). Two
  of the eight have since resolved themselves via the HUB75 official-specs ingestion.
- **F-400** — a definition call on citation shorthand, Stephen's ruling. Worth knowing: expanding
  every shorthand is now **15 sites in 2 files**, not the 55 the entry was written against.
- **F-336, F-337, F-202, F-208** — bench or Chip Gracey. These are the hardware periphery.

⚠️ **Three things this pass proved about the register itself, which matter more than any single row:**
1. **Eight findings were already fixed and still read `CONFIRMED`.** A register whose statuses lag
   the tree invites re-chasing work that is done. Every row touched here was re-verified and flipped
   in the same pass.
2. **One finding's sub-claim was REFUTED** (F-394's C/Z entry condition, which is absent from the
   source it cites). A register entry is a claim like any other.
3. **`p2an006` cited `cogspin.yaml` for figures `cogspin.yaml` had no source for** (F-392). Two
   files agreeing is not provenance; it is a loop.

## The manuals were audited against the v1.18.0 delta at the FACT level, not the path level, and eight corrections were located that the path intersection could not see (2026-09-09, post-release manual sweep, applied 2026-09-10) — F-408…F-419

**How this surfaced.** `release-yamls` Step 8 recorded a **path intersection** — each document's
`MANUAL-DESCRIPTOR.md` declared sources against the release's changed files — and returned
*"INTERSECTS"* for 17 of 20 documents. Stephen asked for the list we would actually work from. A
path intersection cannot produce one: it says a document touches changed ground, never that it
restates a changed fact. Re-run at the fact level — 31 probes over all **126 live master files**,
every hit read in context — the answer is **9 documents with work and 7 with none**.

**Range extended to F-416 on 2026-09-10** as the sweep was applied: F-416 is a KB defect
(`cordic.yaml`) that this sweep *surfaced* rather than a manual correction, and it is kept under this
header because that is where its provenance is legible. **F-415 was rejected on the evidence** — see
its entry — so the header's "eight corrections" is seven applied plus one that was not a defect.

**Full located list, with the negatives that keep the sweep from re-deriving them:**
`engineering/analysis/2026-09-09-v1.18.0-manual-update-list.md`.

**Verified clean, so nothing below is a sweep target:** the `150 mA` per-pin scalar never reached
any manual (every drive figure reads 30 mA); no document carries TTL `VIL`/`VIH`/`VOL`/`VOH`
figures; ALM's interrupt vector map is correct (`$1F0=IJMP3` … `$1F5=IRET1`); `WRLUT` operand order
and LUT-sharing direction are both correct in ALM; `LOCKTRY` acquires everywhere; no fabricated
mnemonics (`RDCOGID`, `RDLUTS`, `NIXINT0`, `TRGINT0`) appear anywhere; no boot-ROM font or math-table
claim survives; no document states a `WAITMS` ceiling; and **of 95 shipped `examples-library/*.spin2`
files, none carries a pull idiom or a `-1` cog launch.**

### F-418 — the layout torture test is built on 44 constant names that exist in no Parallax source — `CONFIRMED` (scope decision owed)

`p2-layout-torture-test/opus-master/P2-Layout-Torture-Test.md`. Measured 2026-09-10 against **every**
ingested source under `engineering/ingestion/sources/` plus the published KB: of **63** `P_*`/`X_*`/
`EVENT_*` symbols the document uses, **19 are real and 44 appear nowhere**.

**Fixed in this pass (6 sites), because these claimed to be a symbol reference:**
- §6.2 *"Long Unbreakable Tokens"* — all three rows were invented at 30-32 characters. **The longest
  constant that actually exists in the P2 symbol set is 24 characters** (`X_2ADC8_16P_4DAC8_WFLONG`),
  so the section was calibrating the width allocator against an input no real document can produce,
  leaving the true worst case untested. That is a **validity** defect in the instrument, not a
  cosmetic one. Now the three longest real symbols (24 / 23 / 23), and `X_2ADC8_16P_4DAC8_WFLONG` is
  the right target for a second reason: it is the symbol that printed ON TOP of its own value in the
  released Assembly manual, the defect behind the tables filter's token-fit branch.
- §6.1 and two mode-table rows — `X_RFBYTE_1P_1ADC` / `X_RFBYTE_1P_1ADCb` → real analogues.
- Two **PASM2 code** sites — `xinit ##X_RFLONG_32P` → `X_RFLONG_32P_4DAC8`. A constant that does not
  exist inside a code listing is the least defensible instance of the class.

**Still open — 44 names, and it is a scope decision, not a defect to fix silently.** The rest sit in
the instrument's wide synthetic mode tables, whose cells are layout fodder ("HDMI and VGA framebuffer
scan-out"). The document is an **instrument**, never published to readers, and it is *"engineered to
reproduce every known layout defect"*. Against that, changing 44 symbols shifts column widths and
would invalidate the `VerifiedBox` claims throughout — each of which was verified against a specific
numbered render. **The question for the register's owner:** does the no-fabricated-names rule reach
an instrument's test fixtures, or stop at documents a reader can obtain? Answer that once and it
settles the whole table set; do not re-derive it per row.

**And F-356's own repair changed shape.** §1.24 settled that calling `P_HIGH_15K` a "15 kΩ pull-up"
is *acceptable vocabulary*; the KB stopped policing a word its own authority uses. What F-356 owes
is **the `DIR` caveat plus a source for the `P_HIGH_15K | P_LOW_FLOAT` composition**, not deletion of
the word. Anyone scoping F-356 off its original wording will do the wrong repair.

---


## Two residues the gates cannot see: a citation re-anchor that translated line numbers, and an eighth fabricated-provenance file (2026-08-27, «#325» verification) — F-377

### F-377 — F-365's re-anchor left locators that are in range and point at nothing; `io_pin_timing.yaml` cites a silicon-doc part file that does not exist — `PENDING-VALIDATION` (the last residue applied 2026-10-07, «#387»; closes when the next KB release serves it)
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

### F-375 — a remote agent receives 383 of our files with their source line deleted, and the gate that checks the filter cannot see it — `PENDING-VALIDATION` (gate half resolved 2026-09-11; the rename overtaken by Stephen's 2026-10-08 ruling; the sourcing gate teaching and the bookkeeping-word cleanup applied 2026-10-10, «#412»/«#422»; closes when the next KB release serves it)

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

---


**GATE HALF RESOLVED 2026-09-11 (block I «#340»).** The structural complaint — *every gate reads the tree, the consumer reads the stream, nothing compares them* — is answered where it mattered: `validate_metadata_filter` now `yaml.safe_load`s the DELIVERED payload and fails on any key that collapsed to `None`, proven with an independently-built negative control (block H, `75911edb`).

**Delivery-strip numbers re-derived and recorded** in the change ledger (now `2026-09-11-yaml-release-change-ledger.md` §1.5 — see the note below) so they reach Stephen's visual read: `filter_metadata` strips five fields; `documentation_source` is **396 values across 395 files**, of which **363 (91%) are real provenance** and only 33 are bookkeeping tokens (`enhanced` 16, `original` 15, `code_analysis` 1, `redirect_stub` 1). So the set satisfies cite-or-omit ON DISK and is delivered NOT satisfying it, and nine tenths of what the filter removes is the provenance the project's own rule requires. Filing drift noted rather than smoothed: the entry said 397/396, today measures 396/395.

**The 383-file rename was a scope call Stephen owned; he ruled 2026-10-08 that there is no rename** (the delivery filter strips `source:` too, so a rename would deliver nothing; provenance is for us). What was left — the gate learning `documentation_source:` and the bookkeeping words — is applied (the blocks above).

⚠ **Ledger correction 2026-09-11.** These numbers were first appended as §1.26 to `2026-08-27-yaml-release-change-ledger.md`. That ledger was **spent** — its declared range `v1.17.0..b0057ec1` shipped on 2026-09-10 as v1.18.0/v1.18.1 — so it could not gate an unshipped release. Stephen caught it. The append was reverted, that ledger archived byte-identical to its last committed revision, and the content re-derived against the correct `v1.18.1..HEAD` range in `2026-09-11-yaml-release-change-ledger.md`. **A release ledger expires the moment its range ships, and nothing in the process was checking that.**
## Our USB smart-pin entry states as fact a sentence the DOCX edition dropped, and it contradicts the general WRPIN rule (2026-08-26, «#320» citation re-anchor) — F-372

### F-372 — `%11011` says a new WRPIN needs no reset; the same document's general rule says the opposite — `PENDING-VALIDATION` (settled on silicon by EF-093, applied 2026-10-10, «#419»; closes when the next KB release serves it)

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

## Two same-named Silicon Doc DOCX copies disagree, and the KB garbled a flag semantic from that passage (2026-08-26, «#314» pre-flight) — F-367 · F-368 · F-369

### F-367 — `external-inputs/p2/` and `sources/silicon-doc/` hold DIFFERENT documents under the same filename — `CONFIRMED`

**How this surfaced.** «#314» went looking for a PASM2 DOCX and found `external-inputs/p2/` holds
DOCX originals for several sources — **including a second copy of the Silicon Doc**, same filename,
different size (4,919,444 vs 4,814,991 bytes).

**Measured, not assumed.** Both carry 48 tables and 34 media, so a structural check calls them
identical. Extracting text from each and diffing says otherwise: **972 characters differ across 4
sites.**

| Site | `sources/` (the copy used for the 2026-08-26 re-extraction) | `external-inputs/` |
|---|---|---|
| GETBRK WZ | `Z = 1 if no … pattern queued (D = 0) or **0** if pattern queued (D <> 0)` | `… or **1** if pattern queued (D <> 0)` |
| smart-pin reset | **carries a full paragraph**: *"Once a smart pin is configured via WRPIN and then started by making its DIR bit high, it can be reset at any time by making its DIR bit low. It does not lose its configuration…"* | **paragraph absent** |
| PWM dither rationale | *"a maximum of only two adjacent 8-bit DAC levels are set for every 2…"* | *"a maximum of only two transitions occur for every 256 clocks"* |
| typo | `cog regis+ters:` | `cog registers:` |

**Which is right, and why it is decidable without a third source.** The `external-inputs/` GETBRK
line sets **Z = 1 in both branches**, which makes `WZ` useless and cannot be what the silicon does;
`sources/` gives `Z = 1 / Z = 0`, which is also the conventional Z semantic (`D = 0 → Z = 1`).
**The copy used for the re-extraction is the correct one**, and it additionally carries a paragraph
the other lacks. No prior work is invalidated.

**Why it still matters.** Two files with one name, differing on a flag semantic, is a silent
corruption waiting for whoever opens the wrong one. `external-inputs/p2/` is not a source folder and
carries no dashboard row, no audit and no trust tier — it is a staging area that has quietly become
a second, unlabelled copy of the corpus. **Disposition is Stephen's:** label `external-inputs/p2/`
as staging-only with a pointer to the canonical `sources/` copies, or reconcile the copies. Recorded
as **needs Stephen's accept-or-fix**.

**Also found there and NOT blocked as previously reported:** `Propeller 2 Questions & Answers.xlsx`
— the `p2-qa-spreadsheet` row sits at 80% and was listed in this sprint's plan as having *no primary
document staged*. It has one. That plan line is wrong and is corrected in «#318».

## `pin-selection.yaml` printed the streamer's sub-pin table with the wrong bit weights, and shipped the EF-065 trap as its worked example (2026-08-26, found while composing the streamer pin-capture page) — F-361

- **F-361 — Two defects in `deliverables/ai/P2/architecture/streamer/pin-selection.yaml`: a
  `sub_pin_selection` table that contradicts both the Silicon Doc and the bench, and a
  `pin_base_encoding` example that is the EF-065 misalignment trap written out for a reader to
  copy.** — `PENDING-VALIDATION` (both fixed 2026-08-26; a direct bench check of the sub-pin
  weights is arm B of VO-J-005 and has not been run)

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
  the citation regex, so six of the seven still pass the gate today.** — `PENDING-VALIDATION` (six files re-derived and shipped by 2026-10-05, «#386»; the five remaining claims applied 2026-10-10, «#413»/«#418»/«#419»; closes when the next KB release serves them)

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

  Status: `PENDING-VALIDATION` — all six re-derived and cited against live sources; the eight
  non-derivable claims listed above are dispositioned (three removed by 2026-10-05, five decided and applied
  in the block at the top of this entry).

---
## Carry-forward guardrails — investigated and settled; do NOT re-file (full detail in the archive)

- **F-002 (`WONTFIX`):** `?` / `||` operator-form failures were an agent usage error — the KB is correct (`??var` = XORO32 random; `ABS()` not `||`; `?` is the ternary operator).
- **F-036 (`WONTFIX`):** `calld.yaml` — LOC loading a 20-bit address into PA/PB/PTRA/PTRB is not a defect.
- **F-093 (`WONTFIX`):** `lockrel.yaml` C-flag polarity — the appendix's "inverted" claim is the error; the YAML is correct (C = lock-was-held).
- **F-114b (`RESOLVED-INVALID`):** the MIDI display modes KEYBOARD / GRID / ROLL / MONITOR do **not** exist in PNut v55 — do **not** add them to `midi.yaml` (it carries an explicit `not_supported:` claim).
- **Verified-resolved (don't re-chase):** the Jan-2026 streamer KB audit's issues were all reconciled in the 2026-05/06 passes (DAC routing, 32-pin groups, mode encoding, xcont/xzero phase wording, setxfrq 2³¹ formula, streamer symbols). Only the XZERO concept text was open and is fixed (F-003).

---

## The "masters are clean of the drive-strength mislabel" measurement is wrong (2026-08-25, «#301») — F-356

### F-356 — the drive-strength mislabel is alive in the IOSP master at 23 sites, including the one composition this sprint forbids by name — `PARTIAL`

**How this surfaced.** «#301» was told, as a *measured result and not an assumption*, that a
class-wide sweep on 2026-08-24 found the manual and app-note masters **clean** of this sprint's
defect class (the drive-strength mislabel, the fabricated ladder, pin slew-rate claims) — which is
why Plan §3 excludes manual prose from that class. Working F-251 required reading the deSilva Ch.1
LED aside, whose closing sentence turned out to state the mislabel outright. One site is an
anomaly; the sweep it implied is what produced this finding.

**What was measured.** A sweep of every `opus-master/` body and CHANGELOG across all manuals and all
seven app notes (excluding `archived-2025/` scaffolding and the non-P2 `Donna-Manuscript`) for
pull-up / pull-down language, then each hit graded by hand as *external component* (correct) or
*`P_HIGH_*`/`P_LOW_*` glossed as a bias resistor* (wrong):

| Site class | Count | Where |
|---|---|---|
| A `P_HIGH_*`/`P_LOW_*` constant glossed as a **pull-up/pull-down resistor** | **23 lines** | IOSP `appendix-b-p-constants.md` ×7 · `chapter-12-digital-input.md` ×5 · `chapter-02-enhanced-direct-io.md` ×7 · `chapter-06-digital-output.md` ×2 · `appendix-a-intent-index.md:56` · `part-5-appendices/index.md:221` |
| **"internal pull-up/pull-down"** asserted as a P2 feature | **5 lines** | `chapter-06-digital-output.md:137`, `:144`, `:441` · `chapter-02-enhanced-direct-io.md:431`, `:479` |
| The composition this sprint says to **never** write | **4 sites** | `chapter-02-enhanced-direct-io.md:94`, `:399`, `:439`, `:480` — `P_HIGH_15K \| P_LOW_FLOAT` |

**Why each class is wrong.** A pull-up is active whenever the pin is *not* driven; a drive-strength
selector applies **only while the pin drives that direction** — DIR high, per the Pin Mode Legend
(`deliverables/ai/P2/architecture/pin-drive-configuration.yaml:41-43`, `:166-171`; P2 Datasheet
2022/11/01 p.24). This is F-321's reasoning exactly, and F-321 was applied to
`deliverables/ai/P2/` and **only** there. `chapter-02-enhanced-direct-io.md:53` is the cleanest
example: it prints `| P_HIGH_15K | %010 | Resistive | ~200µA / 15kΩ | **Pull-up resistor** |` — a
component the chip does not have, in a table of things it does. `:441`'s
*"Open-drain + internal pull-up"* is the F-322 inversion in a summary row. And
`P_HIGH_15K | P_LOW_FLOAT` is the composition whose "high side weak, low side floated" variant
`pin-drive-configuration.yaml:250-252` records as having **no Parallax documentary statement and no
empirical record** — the manual teaches it four times, once as a recipe headed **"Pull-Up
Resistor:"**.

**Scope note — this is filed, NOT fixed, and the distinction is deliberate.** Plan §3 puts this
defect class out of scope for manual prose in this sprint, and «#301» was told scope is Stephen's.
So the correct act is to **falsify the measurement the exclusion rests on** and hand it over, not to
widen a roster. The two sites «#301» *did* fix are the ones inside its own roster's findings:
deSilva `COMPLETE-OPUS-MASTER.md:294` (inside F-251's aside), and `:2881` was checked and left
because it is already **correct** (*"No pullup/pulldown by default — Use external resistors or
configure smart pin modes"*).

**PARTIAL 2026-09-10 — the MECHANISM half is applied across IOSP and deSilva; the SOURCING half is
not: no source or bench result exists for `P_HIGH_15K | P_LOW_FLOAT` (F-336, closed 2026-10-10 by
Stephen's ruling that the composition is dropped, not benched).** Worked as part of the v1.18.0 sweep, under §1.24's reframing.

⚠️ **§1.24 changed what the repair is, and this entry's own site counts must be read through it.**
Calling `P_HIGH_15K` a "15 kΩ pull-up" is now *acceptable vocabulary* — the Silicon Doc uses it for
these same rungs, and the KB deliberately carries `pull-up`/`pull-down` **aliases** so a coder
asking the real question lands on the real answer. So the "23 mislabel sites" are no longer 23
defects. **What was owed, and is now delivered, is the DIR caveat and the mechanism at every place
the constants are presented:**
- `chapter-02` — a passage before the drive tables stating the P2 has no separate pull resistors,
  that these are drive strengths, and that every rung needs `DIR = 1`; a second note governing the
  *Common Drive Configurations* block (those lines are mode words only); and `PINHIGH` added to the
  two bare-`WRPIN` pull-up recipes at `:94` and `:399`.
- `chapter-06` — `:144` now says this is an open-drain *substitute* whose high side drives rather
  than floats, and sends a genuine multi-master bus to `P_HIGH_FLOAT` + an external pull-up; `:441`'s
  summary row is retitled *"Weak-high / strong-low (open-drain substitute)"* (that row is **F-417(b)**).
- `appendix-b` — the *Drive Strength - High* table now opens with the DIR/OUT rule, and the button
  recipe carries its `PINHIGH` step.
- `deSilva :2881` — **re-adjudicated and rewritten.** This entry records it as "already correct",
  and against the framing of 2026-08-25 it was; under §1.24 *"no pullup/pulldown **by default**"*
  implies a non-default internal pull, and it sent the reader to smart-pin modes when the mechanism
  is drive strength. It now gives the answer first.
- `part-5-appendices/index.md:221` — the index sent a reader looking up "Pull-up" to Ch. 6, when the
  mechanism and the constant tables are in Ch. 2. Now "Ch. 2, 6", and it names them as drive-strength
  rungs. `appendix-a-intent-index.md:56` was read and **left**: an intent-index row using the
  vocabulary a reader actually types is the findability behaviour the KB's own aliases exist for.

**STILL OPEN — the sourcing half.** `P_HIGH_15K | P_LOW_FLOAT` still has no Parallax documentary
statement and no bench result; the manual now explains the mechanism correctly but cannot *cite* the
composition. **F-336 closed 2026-10-10 without content** (Stephen's Q6, study decisions: the line
exists only in our own catalog extract, no Parallax document states it, no bench run is owed, the KB
dropped it). So the manual cannot cite the composition either: its four `P_HIGH_15K | P_LOW_FLOAT`
sites must come out or be re-expressed with a documented form. That, with the rest of the chapter-scale
pass below, is what keeps this entry `PARTIAL`.

**What would settle it.** Nothing further to establish — the mechanism is closed (F-321 applied, the
Pin Mode Legend cited, the idioms hardware-verified in
`pin-drive-configuration.yaml:203-239`). What is needed is a decision on **when** the IOSP master
takes the correction, because it is not a token substitution: two constant tables, a chapter section
heading (*"### Button Input with Internal Pull-Up"*), four worked recipes and an intent-index row all
have to be restated in drive-strength terms, and the four `P_LOW_FLOAT` recipes need a form that has
a source behind it. That is a chapter-scale pass on Chapters 2, 6 and 12 plus two appendices, not a
sweep.

**Related:** F-321 (same mislabel, KB side, applied) · F-322 (the disable-the-drive inversion) ·
F-325 (the ladder absent from the shipped KB) · F-336 (closed: `P_HIGH_15K | P_LOW_FLOAT` has neither a
Parallax statement nor a bench result, and the KB no longer carries it) · F-341 (the same mislabel in our own derived analysis docs) ·
`SOURCE-ERRATA.md` E-004 and **E-010** (Parallax's own guides state it).

> 🔴 **F-341 IS SHARPER THAN "LATENT" — THOSE FILES INVENT PARALLAX PART NUMBERS. Confirmed by
> Stephen 2026-08-26.**
>
> Asked whether our board coverage was complete, the inventory turned up three part numbers with
> **zero occurrences in any ingested source directory** — i.e. in any actual captured Parallax
> document. They exist only in the loose analysis files at `engineering/ingestion/sources/`:
>
> | Invented | Where it appears | What it actually is |
> |---|---|---|
> | **#64025 "LED Board"** | `p2-hardware-validation-checklist.md:102`, `p2-board-power-analysis-matrix.md` | **does not exist** — the real board is **#64006C LED Matrix** |
> | **#64026 "7-Segment Display"** | `p2-hardware-validation-checklist.md:150` | **does not exist** |
> | **#64027 "Switches Board"** | `p2-hardware-validation-checklist.md:191` | **does not exist** — switches are on the **#64006A Control** add-on |
>
> **Stephen, asked directly: "LED board, no. 7-segment, no. Switches, no."**
>
> **Why this is worse than a wrong name.** The inventions are *plausible* — they describe real
> capabilities (LEDs, a display, switches) that map onto real boards, at part numbers adjacent to
> the real #64019/#64020/#64029 range. And `#64027`'s validation section is headed **"Test 1:
> Pull-up Test"**, so the fabricated board carries the fabricated mechanism. A reader has nothing to
> catch it with.
>
> **None of the four files names a Parallax document anywhere.** Their headers are
> *"Comprehensive testing procedures…"*, *"Complete power budget calculations…"*, *"Complete
> cross-reference for automatic code generation"* — authored analysis, with no provenance, sitting
> in the directory reserved for captured sources. **Location is doing the work of attribution.**
>
> 🟢 **CONTAINMENT VERIFIED: zero leakage.** `grep -rl` for all three across `deliverables/ai/P2/`
> returns **0 files**. The shipped KB never carried them, and «#305» had already excluded loose
> root files from the fidelity tool's truth side. The damage is confined to the ingestion tree.
>
> **Still open, and it is a scope call:** the four files remain where sources live, they still assert
> the pull-up mislabel, and the compatibility/power matrices cross-reference boards that do not
> exist — so anything derived from them is derived from fiction. Options: correct them in place and
> relabel as analysis, relocate them out of `sources/`, or retire them. **Not actioned pending
> Stephen's decision.**
>
> 🟢 **THE INVENTED-PART-NUMBER HALF IS CLOSED 2026-08-26 («#323»).** Stephen's standing rule —
> *"no fabricated names in the KB tree, delete invalid names outright"* — settled the disposition
> without needing a further decision, so it was executed. **Every `#64025` / `#64026` / `#64027`
> site in the repository was worked**, which was more than the three the finding names:
>
> | File | What was there | What was done |
> |---|---|---|
> | `sources/p2-hardware-validation-checklist.md` | three validation sections (`:102`, `:150`, `:191`), incl. the `#64027` "Pull-up Test" that carries the F-321 mislabel | sections deleted, dated removal note left in place |
> | `sources/p2-board-power-analysis-matrix.md` | three power-analysis sections, two `case` arms in worked code, five Quick-Reference rows | all deleted, removal note left |
> | `sources/p2-complete-signal-flow-matrix.md` | three signal-path sections, a VIO-load `case`, three `ADDON_*` constants, an impedance-detect routine returning two of the invented boards | all deleted, removal note left |
> | `sources/p2-board-addon-compatibility-matrix.md` | three grid rows, five detailed configurations across two boards, three power rows, three `case` arms | all deleted, removal notes left |
> | `plans/quick-bytes-ingestion-plan.md` | `parallax_id: "64025"` against **"P2 RTC Add-on Board"** | **corrected to `64013`** — the real part number, from `sources/edge-breakout-board/edge-breakout-board-narrative.txt:137` |
> | `knowledge-base/P2-support/extractors/hardware-specs-extractor.py` | a YAML **generator** with all three baked in, emitting them under `source: P2 Documentation Collection` | the three entries deleted, note left |
>
> **Deleted rather than relabelled, deliberately.** The nearest real boards are the **#64006C LED
> Matrix** (an 8×7 Charlieplexed grid driven on 8 pins) and the **#64006A Control** add-on (four
> buttons and four LEDs); there is no 7-segment board in the #64006 series at all. The removed pin
> maps, currents and test procedures described none of those, so relabelling would have attached
> fabricated numbers to real boards — a worse defect than the one being fixed.
>
> After: `grep -rn '64025\|64026\|64027'` across the repository returns **no hit that presents a
> board**. Every surviving occurrence is one of four kinds: a dated removal note at the site the
> content was cut from, the `#64013` correction comment, the sprint plan's task row, or this
> register's own documentation above. Deliberately stated as classes rather than a count — the
> count changes every time this register is edited, and a self-referential tally is stale the
> moment it is written. (Arbiter check, «#323»: the figure first written here was 11; the live
> number was already 15, because writing the table above added hits to the thing being counted.)
>
> **Two halves remain open**, both unchanged by this pass: the four files still sit at
> `sources/` top level asserting the pull-up mislabel (the relocate-or-repair-or-retire call), and
> the *same class* of unverified part numbers survives in them — `#64028` "Buttons Board",
> `#64029` relabelled "Switches and LEDs Combo", `#40003` "Protoboard", `#40007` "Digital I/O
> Board". Those four were left strictly alone because Stephen confirmed three numbers, not seven,
> and «#323» would have been widening its own scope to act on them.

Status: `PARTIAL` — the mechanism/DIR-caveat half is applied across IOSP and deSilva (2026-09-10, in the v1.18.0 sweep, shipping in IOSP v1.0.10); the `P_HIGH_15K | P_LOW_FLOAT` composition has no source and no bench result (F-336, closed 2026-10-10: dropped from the KB), so the four manual sites that teach it are still owed.

---

## Five defects surfaced while ending the drive-strength mislabel class (2026-08-25, «#296» §5) — F-342…F-346

> **Origin.** All five were found while correcting F-321…F-324 — three of them only because
> R8 forces a **semantic read** of every example after it compiles. Three are fixed in that same
> pass and marked so; two are not this task's repair and are filed for the head that owns them.
> Every line number below was read off disk on 2026-08-25.

### F-344 — the derived board extract contradicts itself in one sentence about switch polarity — `CONFIRMED`

> **Where:** `engineering/ingestion/sources/p2-eval-add-on-boards/boards/addon-control-64006a.md:9-11`
> — *"each **active-high** push-button has a **470 Ω series resistor** so the I/O pin is **driven
> low** while the button is asserted."*
>
> **Active-high and driven-low-when-asserted cannot both be true of the same switch.** The rest of
> that same file says active high in the pin map (`:20-23`), and the shipped
> `hardware/addon-control-board.yaml:16-20` says *"the I/O pin reads high while the button is
> pressed"* — so the KB already resolved it the other way. The extract's own summary sentence is
> the outlier.
>
> **Ingestion-tree defect, not a YAML edit** — this file is derived source-research and is frozen
> to KB maintenance. Same class as **F-341** (our own derived documents inside the truth root).
> **What is owed:** re-read the #64006A Product Guide v2.0 page and correct the extract's summary
> sentence, or record why the guide itself says both.

## Provenance holes the repopulation could not fill (2026-08-25, «#299» Plan §8 part 2) — F-352

> **Origin.** «#299» rebuilt `architecture/`, `language/`, `guides/` and `application-notes/` from
> the repaired sources, source-first. Forty-five of F-347's sixty blocks came back cited. Two did
> not, for the same reason — the KB was their only home — and the rule set had no branch for that
> once the purge had already removed them. Line numbers below were read off disk 2026-08-25.

### F-352 — two shipped KB areas are authored-here content with NO upstream anywhere in the ingestion tree, and once their blocks were purged the promotion filter's sub-rule P had no branch left for them — `PENDING-VALIDATION` (click half closed and its citations rewritten 2026-10-10, «#420»/«#422»; the `io_pin_timing` half closes by staying closed; closes when the next KB release serves it)

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

---

## `hardware/` repopulated from the board guides — the return record, and the wrong scalars the source-first read exposed (2026-08-25, «#307» Plan §8 part 2) — F-353 · F-354

> **Origin.** «#294» removed 59 quantitative blocks from `deliverables/ai/P2/hardware/` (F-334, two
> records: 48/16 files and 11/6 files). «#298» dispositioned every one. «#307» worked the **board
> guides**, not the removal list, and wrote back what each guide states. One of the 11 —
> `language/spin2/methods/getct.yaml description` — is outside this tree and belongs to «#299», so
> **58** were in scope here. Every line number below was read off disk 2026-08-25.

### F-354 — eight content-level holes in the repopulated `hardware/` blocks: seven are closed or applied (the five driver-shaped ones by removal 2026-10-07; the PCB dimensions and the `addon-serial-device` supply 2026-10-10, «#420»), and one is BLOCKED on a document this repo does not hold (the #64013 schematic) — `PARTIAL`

> **Why these are not "gaps" in the three-number sense.** Every ACTIONABLE block returned. What did
> not return is *material inside* those blocks — figures the KB shipped that no ingested source
> states. Each open one is recorded in the YAML itself, at the point of use, with what would settle
> it, so a reader meets the hole where the fact would have been.
>
> **Re-scoped 2026-10-07 by Stephen's ruling** (he designed the HUB75 adapter): *"it is best that
> we do not get too specific about the driver so we don't have to update every thing the driver
> changes.. the api matters to code, the pinout matters to code."* A hardware entry carries the board
> — pinout, pin budget, voltages, level shifting, the board's published ceiling — and names its
> driver; the driver's timings, chain counts, cog use and chipset table are the driver's, and the
> v4 HUB75 driver is coming. So a driver-shaped hole is closed by **removing the hole**, not by
> sourcing the number (`.claude/doctrine-overlay.md`, *A hardware entry carries the board, not the
> driver that runs it*). The entry previously said six of the eight needed documents this repo does
> not hold; that was also wrong for the HUB75 rows — Stephen's driver repository is in
> `engineering/ingestion/external-inputs/source-code/external-projects/p2-HUB75-LED-Matrix-Driver/`
> (`THEOPS.md:149` states 1–3 adapters; nothing under `driver/` uses the streamer).
>
> | Hole | Disposition |
> |---|---|
> | HUB75 max clock **40/35 MHz**, **13 ns** | **CLOSED 2026-10-07.** Board fact, already sourced: the designer's spec says 70 MHz, limited by the 2x 74HCT244 (`p2-hub75-adapter-official-specs.md:22`). `gap_max_clock` deleted; `specifications.electrical.panel_clock_note` added from the designer's own note (HUB75Adapter.md "Specifications" note: the panel's chipset sets the clock, far below the adapter's ceiling). No datasheet needed. |
> | HUB75 **pulse-width minimums**, 3/8-bit refresh table | **CLOSED 2026-10-07 — driver facts, out of scope.** `gap_pulse_widths` deleted with the rest of the driver restatement in `software_features` (feature list incl. a wrong "automatic panel detection" — the driver is configured per panel chipset — refresh rates, bandwidth model); replaced by a pointer to OBEX 2850. |
> | HUB75 **"maximum 3 chains"**, **"no streamer"** | **CLOSED 2026-10-07 — driver facts, out of scope.** `notes.gap_chain_limit` deleted. The `led_driver_chips` table (the driver's per-chipset configuration) removed for the same reason. |
> | HUB75 **board current 35 mA**, per-panel currents | **CLOSED (verified 2026-10-07).** The board's own draw ships sourced (`specifications.electrical.board_consumption`, "under 50 mA", `official-specs.md:126`); the held `power_requirements` block is gone from the tree; panel currents are the panel's. |
> | **"One cog consumed by the PSRAM driver"** (32 MB module) | **CLOSED 2026-10-07 — driver fact, out of scope.** The `(uses 1 cog)` comment removed from `code_patterns.spin2.obex_driver_usage`. The rest of that file's driver restatement (`code_patterns`, `protocol_constraints` driver settings) is the class sweep **F-548**. |
> | Whether the **#64013 RTC board carries its own SDA/SCL pull-ups** | **OPEN** — `addon-rtc.yaml` `pin_mode_tip.scl_pull_up_caveat`. A board fact that changes how it is connected. Needs the #64013 schematic (referenced by the guide, not ingested). **BLOCKED — missing document, re-checked 2026-10-10 («#420»):** `sources/P2-RTC-Add-on/` holds the guide, the PCF8523 datasheet and the example archive, no schematic. The page asserts nothing about pull-ups (it says in so many words that neither the guide nor any ingested source states it), so there is no claim to remove. **Stephen / ingestion:** obtain and ingest the #64013 schematic from the 64013 product page (www.parallax.com, search 64013). |
> | Numeric **PCB dimensions for the #64006 add-on boards** | **CLOSED 2026-10-10 («#420»).** Read off the guide's PCB Dimensions drawings (pp.11-12, rendered): A/V 3.2 x 1.3 in, Goertzel 3.2 x 1.2 in, small modules 1.6 x 0.8 in (drawn for the LED Matrix). `addon-goertzel-touch.yaml` `specifications.pcb_size_class` replaced by `pcb_size` (3.2 x 1.2 in, 81.3 x 30.5 mm) and the contradicting `size_class: small_addon` → `medium_addon`. The other small boards inherit the guide's "small modules" grouping; no per-board dimensions are stated for them and none were set. |
> | `addon-serial-device.yaml` **"3.3 V supply"** | **APPLIED 2026-10-09/10 («#413», «#420»)** — the unsourced voltage and `power_sharing` lines are removed and the page states no supply, per Stephen's Q7 (study decisions, 2026-10-09): the Rev B ACC HDR/5V shunt jumper is an Eval-board fact that matters for any add-on using header 5 V, already modelled on `p2-hardware-feature-comparison.yaml` and `addon-serial-host.yaml`; no erratum. (A `power_note` added in «#420» restating the guide's Serial Host vs Revision History wording was removed by the arbiter as contrary to Q7.) |
>
> Status: `PARTIAL` — seven closed or applied (they ship in the next KB release, `PENDING-VALIDATION`);
> one blocked: the #64013 schematic is not ingested (Stephen / ingestion: obtain it from the 64013 product page).

---

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
>

- **F-347 — «#293»'s removal record was never written, so 60 removed blocks existed only in a git
  diff and in a transcript that does not survive.** — `PARTIAL`

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

  `PENDING-VALIDATION` — the record is written and executed against; only the YAML release is owed.

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

> **Disposition.** `PARTIAL` — the record exists now and is usable; it closes when «#299» has
> executed against it and every row carries a returned/not-returned outcome.

---

## WRPIN D-operand field map: three field descriptions wrong in the YAML, ten mode numbers footnote-fused in an ingestion artifact (2026-08-24, `KNOWLEDGE-GAPS` pass-6 catch-up) — F-331, F-332

> **Origin.** The pass-6 gap-ledger catch-up read the WRPIN bit-field map in both 2026-08-24
> repaired captures (P2 Datasheet pp.23-25, P2 Hardware Manual Tables 16-25) to close
> `KNOWLEDGE-GAPS.md` **G-001** and **G-008**. Both defects below were found while doing that
> reading. **Nothing is fixed in this filing.**

### F-332 — the P2 Hardware Manual's table artifact carries ten six-digit `%SSSSS` values for a five-bit field, with no reconciliation note — `CONFIRMED`

**Location:** `engineering/ingestion/sources/p2-hardware-manual/complete-tables-reference.md:287-314`
(Table 25) and the same table in
`engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:1030-1036, 1053, 1054, 1056`.

**Ten values, each a 5-bit mode with its superscript footnote `¹` fused on:** `001001` `001011`
`001101` `001111` `010001` `010011` `010101` `110111` `111001` `111101` — correctly
`%00100¹` `%00101¹` `%00110¹` `%00111¹` `%01000¹` `%01001¹` `%01010¹` `%11011¹` `%11100¹`
`%11110¹`, footnote 1 being *"OUT signal overridden"* (the artifact carries that footnote
immediately below the table).

**This is a known, already-adjudicated class — and the adjudication is in the wrong file.** The
`p2-datasheet` artifact names the identical defect as reconciliations **R1** and **R2**
(`sources/p2-datasheet/complete-tables-reference.md:49-50`), decided by three of four extraction
paths plus a visual read of the rendered pp.34-35, and its **R8** even records that "The Hardware
Manual's DOCX (Table 9) carries the identical fusion, so this reconciliation applies to both
sources" — for Table 9's `INA`/`INB` only. **No such note exists anywhere in the Hardware
Manual's own artifact** (a case-insensitive search of that file for *footnote*, *superscript*,
*reconcil*, and *OUT signal overridden* returns nothing).

**KB impact: NONE today — recorded so it stays that way.** No fused value reached
`deliverables/ai/P2/` (grepped for all ten; the only near-hits are COGINIT mode bits in
`spin2/patterns/implementation/spin2_cog_management.yaml`, unrelated). The exposure is forward:
an agent deriving smart-pin YAML from the Hardware Manual artifact alone gets `%001001` for
pulse/cycle output.

**Proposed correction (ingestion head, not a YAML edit):** add the R1/R2 reconciliation note to
`sources/p2-hardware-manual/complete-tables-reference.md` beside Table 25, in the form the
datasheet artifact already uses. **Wider question worth one pass:** the DOCX walk drops
superscript markers into the adjacent numeral generally — Table 9's `INA1`/`INB2` is the same
mechanism, so Table 25 is unlikely to be the only other instance.

---


## Six defects surfaced while building the single constant-definition home (2026-08-25, «#295» phase 2) — F-336…F-341

> **Origin.** All six were found while implementing «#295» — promoting the drive ladder into the
> KB and collapsing two `P_*` definition homes into one. Two are fixed in that same pass and are
> marked so; four are not this task's repair and are filed for the task that owns them. Every
> number below was measured against disk on 2026-08-25, not carried from the design.

### F-337 — the P2 Datasheet and the P2 Hardware Manual agree with each other and contradict the Silicon Doc on `%TT` in DAC_MODE, and the shipped YAML follows the minority source — `PENDING-VALIDATION` (smart-mode row settled by EF-071; smart-pin-off row applied 2026-10-10, «#419», with no bench needed; closes when the next KB release serves it)

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

### F-341 — six of our own derived analysis documents sit at the root of `engineering/ingestion/sources/`, repeat the pull-up mislabel F-321 exists to kill, and are inside the fidelity gate's declared *Parallax documentary* truth root — `PARTIAL`

> 🔴 **THE LATENT DISARM WENT ACTIVE, EXACTLY AS THIS FINDING PREDICTED — and is now closed
> at the instrument (2026-08-25, «#305»).** This entry says the disarm is "a shape away, not a
> policy away". «#305» changed the shape (the harvest had to read the current-edition v55
> table, whose rows put the name in column 2), and with the repaired parser and no guard,
> `p2-complete-signal-flow-matrix.md:100` — a **signal-flow** table whose last cell happens to
> hold a constant name — defined `P_PWM_SAWTOOTH` as **"P38"**, the pin number in the
> neighbouring cell. One of our own derived documents teaching the instrument our own
> inference, in the first run after the shape changed.
>
> **Closed structurally, not by a list of six names.** An ingested source **is a directory**:
> every real source under `sources/` lives in its own folder because that is what the ingestion
> process creates, so a loose file at the root of a truth root was put there by something else
> and is not an ingested source document (`MIN_DEPTH_BELOW_ROOT`). That rule excludes all
> **twelve** loose files at `sources/` top level, not just these six, and it catches the next
> stray file without an edit. A second, independent guard bounds the name cell to the first two
> columns — a constant in the last column is a *use*, not a definition. Both carry negative
> controls, including the exact `P_PWM_SAWTOOTH | P38` row.
>
> **`TRUTH_ROOTS` was NOT widened or narrowed** — the roots are unchanged; only what counts as
> a file inside them is now defined.
>
> **Still open, and it is the half this finding actually asked for:** the six documents remain
> at `sources/` top level, still asserting a 15 kΩ internal pull-up the P2 does not have. The
> instrument can no longer be misled by them; a reader still can. Relocating them to a derived/
> analysis area, or repairing them against the Datasheet legend, is unchanged and unowned.
>
> Status: `PARTIAL` — instrument disarm closed and controlled; the invented-part-number half
> is closed at every site in the repository (2026-08-26, «#323» — see the boxed note under
> F-356); the content relocation, and the four further unverified part numbers those files
> carry (#64028, #64029-as-combo, #40003, #40007), are owed.

> **The six**, all at `engineering/ingestion/sources/` top level, all self-describing as
> generated cross-references rather than Parallax publications:
> `p2-board-addon-compatibility-matrix.md` · `p2-complete-signal-flow-matrix.md` ·
> `p2-hardware-validation-checklist.md` · `p2-board-power-analysis-matrix.md` ·
> `p2-board-pin-mapping-knowledge.md` · `p2-addon-board-circuit-knowledge.md`.
> Their own subtitles give them away — *"Complete cross-reference for automatic code generation"*,
> *"Comprehensive testing procedures"*, *"Knowledge Base"*. No Parallax document is named on any
> of them.
>
> **What they assert.** The F-321 mislabel, verbatim and repeatedly:
> `p2-complete-signal-flow-matrix.md:127` *"WRPIN(pin, P_HIGH_15K) ' 15kΩ pull-up"*, `:62`
> *"Input Type: Digital with internal pull-up"*, `:65` *"220µA through pull-up when pressed"*;
> `p2-board-power-analysis-matrix.md:79` *"Internal pull-up: 15kΩ to 3.3V"*;
> `p2-board-addon-compatibility-matrix.md:84` *"8 × 220µA pull-up current = 1.76mA"*;
> `p2-hardware-validation-checklist.md:198` *"Enable internal pull-ups"*. The P2 has no such
> component — `P_HIGH_15K` selects **drive strength**, per the Datasheet p.24 Pin Mode Legend
> (`p2-datasheet-text.txt:1139-1147`). The 220 µA and 1.76 mA figures are stated by no Parallax
> source.
>
> **Why it is more than stale prose.** `audit-constant-fidelity.py` scopes its truth side to
> `TRUTH_ROOTS = [ingestion/sources, ingestion/smart-pins-catalog]` with a comment explaining that
> an unauthoritative source does not add a wrong answer, it **DISARMS the check** — that is why
> `external-inputs/` was excluded. These six are unauthoritative and are *inside* the root.
> **Measured today: they contribute 0 entries to the truth table**, because their pull-up lines do
> not happen to match `ROW_RE` or `BULLET_RE`. The disarm is latent, not active — a shape away, not
> a policy away.
>
> **What is owed.** Decide what these files are and put them where that is true: relocate to a
> derived/analysis area outside `sources/`, or repair them against the Datasheet legend and label
> their provenance. Either way they must stop reading as Parallax documentary sources.
> **Same class as the arbiter's F-322 correction** — a derived extract inside the ingestion tree
> mistaken for the source it was derived from. Two instances in two days makes it a class, not an
> accident: an audit of what actually lives under `ingestion/sources/` is owed.

---

## `object-image-dedup.yaml`'s map_caveat goes stale when pnut-ts 1.55.4 ships (2026-08-22) — F-320

### F-320 — `p2kbSpin2ObjectImageDedup`'s `map_caveat` warns readers off .map labels that 1.55.4 makes correct, while the limitation that SURVIVES the fix is documented nowhere. `PENDING-VALIDATION` (closed by measurement 2026-10-07, «#387»; the one-clause addition ships with the next KB release)
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

## An ADC comparator example still states the input threshold in fixed volts, in the manual F-412 just repaired (2026-09-11) — F-424

### F-424 — IOSP §2.5's ADC comparator example quotes `~1.65V` as an input threshold without the supply-fraction caveat the same manual now carries everywhere else — `CONFIRMED`

Found 2026-09-11 while **validating F-412 on the released PDF** — which is the point worth
recording: the validation pass for one finding is where the residual sites of its class surface,
because it is the only pass that reads the whole artifact looking for that exact shape.

`P2-IO-and-Smart-Pins-User-Guide.pdf` **page 59** (§2.5 ADC modes), in the worked example:

```
' Detect when analog input exceeds ~1.65V (mid-scale)
WRPIN(adc_pin, P_ADC_1X)
PINFLOAT(adc_pin)
```

**Why this is the F-412 class and not a duplicate of it.** F-412 named
`chapter-12-digital-input.md:25` and `:95` and was repaired there — p184 now states the threshold
as a fraction of `Vxxyy` (0.3 / 0.5 / 0.7), calls it a band rather than a point, and ends
*"Quote 1.65 V as the typical value at 3.3 V, never as the switching point."* This site is a
**different chapter** and states a comparator trip point as a fixed voltage with no supply
reference at all. `(mid-scale)` carries the fraction implicitly for a reader who already knows
the rule; the reader who meets this page first does not.

**It is genuinely wrong off-nominal, which is what makes it a finding rather than a style note.**
`Vxxyy` is specified 3.15 V - 3.45 V, so mid-scale spans roughly 1.58 V - 1.73 V, and pin groups
on different supplies do not share a threshold. The manual states this itself at p184 and again at
p187 (*"the fraction is what the level fixes"*) and p195 (*"Levels below assume Vxxyy = 3.3V;
scale them to your I/O supply"*) — three sites carry the caveat and this one does not.

**Fix.** One line, in
`engineering/document-production/workspace/p2-io-and-smart-pins-user-guide/opus-master/` §2.5:
state the trip point as mid-supply and give 1.65 V as the value at a nominal 3.3 V, matching the
vocabulary p184 already established. Do not delete the number — the reader needs a figure to
aim at; it needs the supply attached to it.

**Class sweep owed with the fix** (`feedback_classwide_sweep_on_every_finding`): re-read every
site in the IOSP that names an input threshold or comparator trip point in volts and confirm each
carries the supply. This entry records only the site the F-412 validation pass happened to cross.

---

## YAML→Manual impact survey — KB v1.16.3 (2026-08-16, `release-yamls` §8)

Delta: `spin2/methods/wrpin.yaml` · `architecture/smart_pins.yaml` ·
`architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` · `architecture/cordic.yaml` ·
`architecture/streamer/overview.yaml` · `architecture/streamer/dds-goertzel.yaml` ·
`pasm2/getxacc.yaml` · `spin2/integration/spin2-pasm2-integration.yaml` ·
`spin2/special-symbols/at.yaml`.

Intersected against every live manual's `MANUAL-DESCRIPTOR.md` declared sources. **Survey done, not
skipped.** Most intersections are already owned by an in-flight Sprint 2 task, so no duplicate flag
is raised for them; the ones that are **not** covered are flagged below.

| Element | Intersects on | Disposition |
|---|---|---|
| Streamer Guide | streamer, dds-goertzel, getxacc, DEBUG_COGS | **covered** — «#220» «#221» |
| IOSP | `architecture/smart-pins/`, smart_pins | **covered** — «#219» (and the F-264 %TT material rides its v1.0.9 pass) |
| Assembly Reference | cordic, streamer | **covered** — «#228» |
| P2AN002 | cordic | **covered** — «#236» |
| XBYTE Guide | streamer | **covered** — «#227» (§15.3 restructure); see the F-268 flag below |
| **P2AN001 / P2AN003** | wrpin | **⚑ FLAG — re-audit against v1.16.3.** These two were read site-by-site and taken OUT of the release wave, but that read answered **F-259's** question (does every executable example carry `\| P_OE`?). **F-264 is a different fact** — that `%TT` is context-dependent and that adding `P_OE`/`P_CHANNEL` to a **non-smart-pin cog DAC** kills it. Any cog-DAC or `P_DAC_*` configuration in these app notes was never checked against that. Do not treat the wave exclusion as covering it. |
| **P2AN004** | wrpin | **⚑ FLAG — same class as above**, and it was never in the wave at all. |
| **Architect's Guide** | CORDIC, streamer | **⚑ FLAG — re-audit against v1.16.3.** Not in the release wave. Declares both sources; the CORDIC hub-in-loop rule (F-263) and the `DEBUG_COGS` streamer caveat (F-266) are new since its last pass. |
| **DeSilva Tutorial** | CORDIC | **⚑ FLAG — re-audit against v1.16.3.** It *is* in the wave, but for §1/§2 (Acknowledgments, Appendix A) only — its CORDIC material is untouched by «#222»/«#223» and unexamined against F-263. |
| All elements showing PASM fragments | `spin2-pasm2-integration.yaml` | **⚑ FLAG — F-268 class sweep**, filed below and deliberately not folded into a correction task. |

These flags are the drift signal `document-audit` drains on each element's next pass. They are
**not** Sprint 2 scope and must not be pulled into it silently — surface them to Stephen as a scope
decision.

---

## Spin2/PASM2 boundary defect promoted from the empirical ledger (2026-08-16) — F-268

### F-268 — inside a Spin2 object, `##hubsymbol` in a `DAT` block resolves against `$400`, not the object's load address. `PARTIAL — KB DONE 2026-08-16; guide-side sweep owed`

**Origin:** EF-060, which had no F-number and no KB entry. Surfaced while getting the F-256/EF-058
rig working, so it is a by-product rather than a target — and it is the broadest-reach item the
2026-08 campaign produced.

**The fact.** A PASM fragment that is correct in a **standalone** PASM file reads **interpreter
memory** when pasted into a Spin2 object's `DAT` block: `##hubsym` resolves against `$400` rather
than the object's load address. Measured on real P2 silicon: `@disp` = `$1AF9` from Spin2 versus
`##disp` = `$0651` from PASM in the same object — **5,288 bytes apart**, and the `##` form returned
garbage.

**Why it matters more than its size suggests.** It bites anyone who copies a PASM fragment out of a
guide or reference into a Spin2 object — which is how most P2 code is written. It assembles, it
runs, and it reads the wrong memory. **Workaround:** pass hub addresses in from Spin2 with `@`, or
address through PTRA/PTRB.

> **KB APPLIED 2026-08-16 («#218»).**
> `language/spin2/integration/spin2-pasm2-integration.yaml` →
> `integration_rules.hub_address_resolution`: the rule, where it is instead correct (standalone
> PASM), why it bites, the workaround, and the measurement. Findability: a matching one-line pointer
> added to `language/spin2/special-symbols/at.yaml` `notes:`, since `@`'s
> object-relative-vs-absolute entry is exactly where a reader chasing this lands — that file already
> documented the Spin2 side of the same boundary and had no route to the PASM side.
> Source trace: EF-060.

**Still owed (manual head, NOT tasked in Sprint 2):** our guides present standalone-PASM fragments
without saying so. A class-wide sweep of `##hubsym`-style fragments across the live manual set is
the durable fix; scope it as its own item rather than folding it into a correction task.

> **KB + KB-GUIDE HALVES RE-VERIFIED ON DISK 2026-08-25 («#300») — both clean; only the MANUAL sweep remains.**
>
> - **KB half — DONE, confirmed at the file.**
>   `deliverables/ai/P2/language/spin2/integration/spin2-pasm2-integration.yaml:427-436` carries
>   `integration_rules.hub_address_resolution` complete: the rule, `correct_in` (standalone PASM),
>   `why_it_bites`, the `workaround` (pass `@` in from Spin2, or address through PTRA/PTRB), the
>   `measured` figures (`@disp` `$1AF9` vs `##disp` `$0651`, 5,288 bytes apart) and
>   `source: … P2-EMPIRICAL-FINDINGS.md EF-060 (2026-08-14)`. The findability pointer is live at
>   `language/spin2/special-symbols/at.yaml:219`.
> - **KB-guide half — NOTHING OWED, and this was measured rather than assumed.** Swept
>   `deliverables/ai/P2/guides/` for `##`-prefixed hub-symbol fragments: **zero hits**. The KB's guide layer
>   does not present any standalone-PASM fragment that would carry this defect, so there is no guide-side
>   sweep to run.
> - **What is left is the MANUAL set only** — the class-wide sweep named above, which is «#301»'s scope,
>   not a KB item. Status stays `PARTIAL` for that reason alone.

---

## Stephen's review of the Sprint 2 gate release (2026-08-16, «#234») — F-276…F-283

> **Full dispositions and reasoning:** `engineering/planning/SPRINT2-VISUAL-REVIEW-NOTES-2026-08-16.md`.
> Eight observations (V-1…V-8) worked one at a time against the gate commit `fea28f1c`. Four became
> findings; the rest were scope and structure decisions recorded in that file.
>
> **All four are tasked into the voice-conformance family «#240»–«#248» and are absorbed into the
> per-manual pass rather than applied as point fixes** — applying them first and conformance-checking
> after would write the same prose twice and have the second pass judge what the first just wrote.
>
> **Two of these were found by the review, not by the sprint's own sweeps**, and that is the useful
> part: F-277's site sits in body text no Sprint 2 task touched. A findings-driven sweep sees the
> diff; it does not see the document.

### F-280 — `pnut_ts` survives in 16 masters as a command that does not run. `PARTIAL — the whole declared sweep APPLIED in opus-master 2026-08-25 («#301»); publication owed, per document`

**Found:** 2026-08-17 during the P2AN001/P2AN002 voice pass («#247»), by checking the compiler name
the two notes hand the reader against the name of the binary that exists.

**This was already adjudicated and only half-swept.** Commit `c203fa52` (2026-08-11) established the
finding on its merits: `command -v pnut_ts` finds nothing, the installed binary is `pnut-ts`, and the
tool's own usage banner reads *"PNut-TS: Usage: pnut-ts [optons] filename"*. SSDB and the PNut-Term-TS
guide were corrected then — 21 sites — and both voice guides were amended so it could not come back.
**The rest of the set was never swept.** Thirty-three occurrences remain across eighteen files, against
thirty-nine correct ones — a near-even split, so the set currently teaches both.

**Fixed in this pass (2 sites, the two notes being touched):** `P2AN001/opus-master/CHANGELOG.md:37`
and `P2AN002/opus-master/CHANGELOG.md:35`. Both are reader-facing — an app-note CHANGELOG is promoted
to the published `p2anNNN-changelog.md` beside its PDF.

**Remaining (31 sites, 16 files) — the class-wide sweep this finding owns:**

| Element | Sites |
|---|---|
| Getting Started Guide | `getting-started-body.md` ×1 — **highest reader risk**: a beginner's first compile |
| Architect's Guide | `architect-guide-body.md` ×1, `CHANGELOG.md` ×2 |
| ~~Assembly Language Manual~~ | ~~`CHANGELOG.md` ×1~~ — **CLEAR, verified 2026-08-22**: `pnut_ts` appears nowhere in `opus-master/`. (Its three *process* docs carried 10 tool-invocation uses; corrected the same day. The remaining hits in `audit/`, `archive/` and `code-validation/` are frozen records, and `external-inputs/pnut_ts_facts/` is a real path — all correctly left alone.) |
| PNut-Term-TS Guide | `CHANGELOG.md` ×1 (the body was swept at `c203fa52`; its CHANGELOG was missed) |
| deSilva | `archived-2025/README-COMBINED-MASTER.md` ×3 — **archived scaffolding, not shipped; excluded** |
| P2AN003 – P2AN007 | body ×17, `CHANGELOG.md` ×5 |

**Not swept here on purpose.** Conform-on-touch: these elements are not being touched by Sprint 2, and
pulling sixteen masters into a voice pass is the big-bang sweep the rule exists to avoid. Each takes it
at its next visit — this row is what makes sure the visit knows.

**The correction is one substitution** — `pnut_ts` → `pnut-ts` — with no prose consequence. Check each
site is the *command*; the project name in running text is properly **PNut-TS**.

> **SWEEP APPLIED 2026-08-25 («#301»). The conform-on-touch deferral above is discharged: the visit
> came.** All 27 reader-facing occurrences substituted across **14 files**, line counts unchanged
> (4,907 before and after), diff is exactly 27 insertions / 27 deletions.
>
> **⚠️ The row header's own arithmetic was wrong, and re-measuring it is how the extra defect turned
> up.** It reads *"Remaining (31 sites, 16 files)"*; the table under it sums to **30 sites / 15
> files**, because the `~~Assembly Language Manual~~ CHANGELOG ×1` row was struck through as CLEAR on
> 2026-08-22 and the header was never re-totalled. Measured on disk today: **30** occurrences across
> **15** files under `opus-master/`, of which **3** in **1** file are the excluded deSilva
> `archived-2025/README-COMBINED-MASTER.md` — leaving **27 in 14**, which is what was fixed. The
> table's per-element counts were all correct: Getting Started ×1, Architect body ×1 + CHANGELOG ×2,
> PNut-Term-TS CHANGELOG ×1, P2AN003–007 body ×17 + CHANGELOG ×5.
>
> **A second wrong name rode along on one of the lines, and is fixed with it.**
> `pnut-term-ts-user-guide/opus-master/CHANGELOG.md:106` carried *"`pnut_ts` + `pnut_term_ts`"* —
> **both** underscore forms, in the guide whose own `MANUAL-DESCRIPTOR.md:28` and `voice-guide.md:83`
> declare *"the underscore forms `pnut_ts` / `pnut_term_ts` are wrong and no such executable is
> installed."* `command -v pnut-term-ts` finds nothing under that spelling either; the installed
> binary is `/usr/local/bin/pnut-ts`. Corrected to `pnut-term-ts` in the same pass — leaving it would
> have fixed half a sentence.
>
> **Every site was checked for sense, not just substituted** — this finding requires it ("check each
> site is the *command*"). Counted off the pre-edit backups: **23 of the 27 are inside backticks**
> (13 as `` `pnut_ts -d` ``, 10 as bare `` `pnut_ts` ``), unambiguously the command. The **other 4**
> are the compound adjective *"pnut_ts-verified"* — `architect-guide/CHANGELOG.md:102` and `:114`,
> `architect-guide-body.md:19`, `getting-started-body.md:17`. Those are the one shape where this
> finding says **PNut-TS** might be proper instead; they were still taken to `pnut-ts` because
> "verified by running it" names the *binary*, and that is the form already shipping in running text
> at `p2-assembly-language-manual/opus-master/CHANGELOG.md:196` ("348 code examples audited with
> pnut-ts v1.51.7"). Two of the four (`architect-guide-body.md:19`,
> `getting-started-body.md:17`) sit inside the masters' `<!-- CONVENTIONS -->` authoring comments and
> reach no reader — corrected anyway, because a convention block that names a non-existent binary is
> how the next author reintroduces it. The result matches the form P2AN001/P2AN002 already ship
> (`P2AN001/opus-master/P2AN001.md:622`, `P2AN002/opus-master/P2AN002.md:357`), so the set no longer
> teaches both spellings. `grep -c pnut_ts` over `manuals/*/opus-master/` + `app-notes/*/opus-master/`
> is now **0** outside `archived-2025/`.
>
> **Deliberately NOT swept, and why:** the 3 sites in
> `p2-pasm-desilva-style/opus-master/archived-2025/README-COMBINED-MASTER.md` — archived scaffolding
> that ships to nobody, excluded by this finding's own table. Frozen records under `audit/`,
> `archive/` and `code-validation/`, and the real path `external-inputs/pnut_ts_facts/`, are likewise
> untouched.
>
> **Gates:** `audit-code-line-length.py --budget 76` and `audit-inline-code-ascii.py` exit 0 on all
> 14 files. **No occurrence was inside a code fence** — verified by mapping every changed line number
> against the files' fence ranges — so no example file changed, byte-identity is untouched, and
> `pnut-ts` compilation does not apply to this finding.
>
> **What remains is publication, not authorship.** Nine reader-facing documents now carry the
> correction in source and none of them has been re-released: Getting Started, Architect's Guide,
> PNut-Term-TS Guide, and P2AN003–P2AN007. Each ships it at its next release. **This is not a render
> gate** — a token substitution has no layout consequence — so «#302» need not look at it; it is a
> release-wave item.

## Published PDFs carry no machine-readable rights (2026-08-21) — F-316

### F-316 — every published PDF states CC BY-SA 4.0 and a joint copyright on its own page, and carries neither in its metadata. `PARTIAL — mechanism DONE and PROVEN 2026-08-22; adoption is per document`

**How it surfaced.** Stephen, reading the Streamer v1.1.0 metadata at the «#287» gate, asked whether
the PDF's rights should name both companies. The `Author` field is correct as written — Iron Sheep
Productions is the author, and authorship is not copyright — but the question exposed that the
copyright and licence are **absent from the metadata entirely**.

**Measured on the returned v1.1.0 PDF:**

```
Title:            P2 Streamer Programming Guide
Subject:          Comprehensive Reference for Propeller 2 Streamer Hardware
Author:           Iron Sheep Productions, LLC
Custom Metadata:  no
Metadata Stream:  no          <- no XMP at all
```

while `front-matter.md:112` reads *"Copyright © 2026 Iron Sheep Productions, LLC and Parallax Inc."*
and the page below it grants **CC BY-SA 4.0**. Nothing in
`platform/templates/p2kb-platform-foundation.sty` sets `pdfkeywords`, and `hyperxmp` is not loaded,
so no `dc:rights` is emitted.

**Why it matters more than its size suggests.** CC BY-SA exists to be machine-readable. An
aggregator, a search index or a model crawler reading these files sees a document with no licence —
so a deliberately-open set reads as unlicensed, which is the opposite of the intent.

**The split is real, and the fix must respect it.** Surveyed 2026-08-21 across every manuscript:

| Population | Count | Copyright line |
|---|---|---|
| Manuals, guides and all 7 app notes | 17 | Iron Sheep Productions, LLC **and Parallax Inc.** |
| `pnut-term-ts-user-guide` | 1 | Iron Sheep Productions, LLC **only** |
| `Donna-Manuscript` | 1 | private, separate author — out of scope |
| `p2-layout-torture-test` | 1 | instrument, no copyright page — out of scope |

So the string **must be single-sourced per document from `request.json`**, never hardcoded in the
platform. A platform constant would silently attribute Parallax to the one document they have no
part in — precisely the class of defect the metadata single-sourcing work («#283») was built to end.

**Proposed correction.** Two new `request.json` metadata keys (`copyright`, `license`), consumed the
way `\DocTitle` / `\DocAuthor` already are. Emit through `\hypersetup{pdfkeywords=…}`, which needs no
new package; add XMP `dc:rights` via `hyperxmp` **only if** the Forge's TeX Live carries it — that is
unverifiable from the container and must be probed on the interactive daemon rather than discovered
in a production build.

**Sequencing — IN THIS WAVE. Stephen's call, 2026-08-21, overriding a first recommendation to
defer it.** The initial reasoning was that a platform change invalidates the built Streamer PDF and
everything queued behind it. That is true and it is the wrong trade: **this wave is the metadata wave
by design** — «#283» converted identity strings to platform single-sourcing and this release is the
first time the full metadata set reaches the documents. Deferring rights to a later adoption round
means a SECOND metadata round-trip for every document, and an interval in which every published PDF
carries half its metadata. One round-trip, complete, is cheaper and correct. Get it right the first
time it ships.

**Not a manuscript defect.** Every copyright page is already correct and states both parties where
both apply. Nothing in any master needs editing.

**Status:** `PARTIAL — the mechanism is DONE and PROVEN on a returned PDF; the other 17 documents adopt at their next render.`

> **PROVEN 2026-08-22 on the returned Streamer v1.1.0 PDF — read from the artifact, not the log.**
> `Keywords` now reads *"Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed
> under CC BY-SA 4.0"*. `\DocCopyright`/`\DocLicense` join the `\Doc*` family, fed per document
> from its own `request.json`.
>
> **The build is byte-stable**: 91 pages, 24,737 words, and **ZERO pages whose text differs**
> from the pre-rights build — which is what a guarded metadata-only platform change should
> produce, and is now measured rather than assumed.
>
> **Two defects were caught by arming the gate against the returned build**, both mine, and both
> would have shipped: the first emitted string read *"Parallax Inc.. Licensed under"* because the
> template appended a full stop to a value that already ended in one (now a semicolon, fixed in
> the platform so none of the 17 documents still to adopt inherits it); and the gate itself was
> checking only that SOMETHING rights-shaped was present, never that the declared values actually
> arrived. It now verifies each one round-tripped. That is the second time in one day this gate
> passed on intent rather than artifact — worth remembering as a shape, not an incident.
>
> **Owed:** the other 17 documents, tracked in `PLATFORM-FEATURE-ADOPTION.md`'s new Rights column;
> and XMP `dc:rights`, which needs `hyperxmp` and stays gated on confirming that package exists in
> the Forge's TeX Live rather than assuming it. `Keywords` is the carrier today.

> **ADOPTION MEASURED ON THE ARTIFACTS, 2026-08-25 («#302»).** `pdfinfo` over all 15 files in
> `deliverables/documents/DOCs/`: **2 carry a rights `Keywords` string, 13 carry none.**
>
> - **Assembly Reference** — *"Copyright 2025-2026 Iron Sheep Productions, LLC and Parallax Inc.;
>   licensed under CC BY-SA 4.0"*
> - **Streamer Guide** — *"Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed
>   under CC BY-SA 4.0"*
> - **EMPTY:** Getting Started · I/O & Smart Pins · DeSilva · Debug Window · Architect's Guide ·
>   XBYTE · P2AN001…P2AN007
>
> Both adopted strings use the **semicolon** form, so the *"Parallax Inc.. Licensed under"*
> double-stop defect is confirmed absent from everything that has shipped — the platform fix held,
> and none of the 13 still to adopt can inherit it.
>
> **The `pnut-term-ts-user-guide` split is intact and is the reason this must never become a
> platform constant:** its row is ✅ in the adoption table with the ISP-only string, distinct from
> the 17 joint-copyright documents.
>
> **Two things remain owed, and NEITHER can be discharged in this container:**
> 1. **13 published documents adopt at their next render** on `EXEC_ENV_CANONICAL`.
> 2. **XMP `dc:rights` stays gated on whether `hyperxmp` exists in the Forge's TeX Live** — a probe
>    on the interactive daemon, Stephen's side. Until then `Keywords` is the carrier and
>    `Metadata Stream: no` is expected, not a defect. **Do not "fix" this by loading `hyperxmp`
>    speculatively in a production build.**

---

## Nine documents carry a request.json subtitle their own cover contradicts (2026-08-22) — F-317

### F-317 — the subtitle in `request.json` disagrees with the printed cover in 9 of 15 published documents, and adopting metadata single-sourcing is what makes that visible. `PARTIAL` (re-verified 2026-10-05 «#386»: deSilva and Debug Window now agree; seven app-note subtitles still contradict their covers) — **all 9 re-measured 2026-08-25 («#302»): unchanged, still drifting, none adopted**

**How it surfaced.** Stephen: *"fix README if needed, always."* Sweeping the public index's
subtitle lines against the PDFs found 10 apparent mismatches — but checking them against
`request.json` was the wrong comparison, because **`request.json` only reaches the PDF for a
document that has ADOPTED metadata single-sourcing**, and only three have. Re-run against the
**printed cover**, the picture inverted: the README was right in almost every case, and it is
`request.json` that is out of step.

**The real defect, and it is latent rather than shipped.** For an unadopted document
`request.json`'s subtitle reaches nothing, so the disagreement is invisible. The moment that
document adopts — `\DocSubtitle` → `pdfsubject` — that string **becomes the PDF's Subject** and
contradicts the subtitle printed on its own cover. **This already happened once**: «#283» hit it
on the Streamer Guide, and the rule recorded then is **the cover wins**.

| Document | `request.json` subtitle | printed cover says |
|---|---|---|
| `p2-pasm-desilva-style` | Build, Experiment, and Master the Propeller 2 | A Human-Centered Approach to Parallel Processing |
| `p2-debug-window-manual` | See What Your Program Is Doing — Nine Display Windows for the Propeller 2 | See What Your Program Is Doing |
| P2AN001 | Application Note P2AN001 — No External ADC | Measure an Absolute Voltage in Microvolts on a P2 Pin |
| P2AN002 | Application Note P2AN002 — Hardware Math on the P2 | CORDIC for Real Work |
| P2AN003 | Application Note P2AN003 — No External DAC | Generate Analog Waveforms and Audio on a P2 Pin |
| P2AN004 | Application Note P2AN004 — No External Counter or ADC | Read Real-World Sensors by Frequency, Rotation, and RC Timing on a P2 Pin |
| P2AN005 | Application Note P2AN005 — Run Several Jobs in One Cog | Cooperative Multitasking with Spin2 TASK Methods |
| P2AN006 | Application Note P2AN006 — Size Every Stack, Catch Every Overflow | Sizing Cog & Task Stacks |
| P2AN007 | Application Note P2AN007 — STRUCT Records, Shared Safely Across Cogs | Data Structures with the New Language Facilities |

**Correction.** Before each document adopts metadata single-sourcing, bring its `request.json`
subtitle to the string its cover prints — **the cover wins**, per «#283». Doing it at adoption
time is the natural moment: that is the render where the value first matters, and
`audit-pdf-metadata.py` will compare the Subject against `request.json` on the returned PDF, so a
wrong value fails the gate rather than shipping. For the seven app notes, note their cover puts a
*descriptive line* under the title — decide per document whether that line or the catalog tagline
is the subtitle, rather than sweeping one reading across all seven.

**Also fixed here (2026-08-22):** the public index's bold line for the Streamer Guide read *"A
Guide to the Propeller 2 Streamer, Its Modes and Function"* while the document it links to prints
*"Comprehensive Reference for Propeller 2 Streamer Hardware"*. That one WAS shipped drift — the
catalog misdescribing the download — and is corrected. Every other index line was verified against
its cover and is correct; the app notes deliberately use `Application Note P2ANxxx · <topic>` as an
index label while their **heading** carries the cover's title, which is a consistent scheme, not
drift.

> **RE-MEASURED 2026-08-25 («#302») — all nine `request.json` subtitles read off disk: every one is
> UNCHANGED from the table above. The drift is intact, and none of the nine has adopted.** So the
> defect is still latent rather than shipped, exactly as recorded — but see the sharpening below,
> which changes when it stops being latent.
>
> ⚠️ **`pdfsubject` IS wired, so "latent until adoption" now means "fires at the very next
> adoption".** This entry was written while F-300 step 4 said *"Do NOT wire `pdfsubject`"*. The two
> adopted PDFs measured today both carry a populated `Subject` (Assembly: *"Complete PASM2
> Instruction Set Documentation"*; Streamer: *"Comprehensive Reference for Propeller 2 Streamer
> Hardware"* — the **cover** string, i.e. «#283»'s cover-wins rule already applied). Neither is in
> the drift table, which is why nothing has shipped wrong yet. **That is luck of ordering, not a
> guard.** The next of the nine to render will publish its `request.json` subtitle as the PDF
> Subject and contradict its own cover.
>
> **So the correction is now a PRE-RENDER step, not a same-render one:** bring the `request.json`
> subtitle to the cover string **before** staging that document, and let `audit-pdf-metadata.py`
> confirm it on the returned PDF. The seven app-note rows still need the per-document decision this
> entry calls for (cover descriptive line vs catalog tagline) — **do not sweep one reading across
> all seven.**

**Status:** `PARTIAL — resolve each document's subtitle to its printed cover BEFORE the render that adopts metadata single-sourcing; 2 of 9 resolved (deSilva, Debug Window), the seven app notes still drifting (re-verified 2026-10-05 «#386»).`

## Open — enhancement proposals (new content, not corrections)

- **ENH-03 — a gating compile step for every code block in `deliverables/ai/P2/`.**
  > **DECIDED by Stephen 2026-10-08: build it now, as the first item of the close-out. From here
  > on it is a permanent part of the release gate** ("let's get this built and from here forward be
  > part of our actual gate!"). It is a hard gate in `release-yamls` and an edit-time check in
  > `yaml-knowledge-base-maintenance` on the files touched. Order: (1) the per-block markers
  > (`compile: program` / `fragment` / `never` + reason, with `never` asserted to fail); (2) fix
  > the prototype's auto-declare collision ("Symbol is already defined") before trusting any pass
  > rate; (3) wire the gate into both skills; (4) all close-out corrections are made under it.
  > F-381's "the example is correct" depends on it.

  > **PROGRESS 2026-10-08 — B1+B2 built («#400»); B3 classification «#403» and B4 wiring «#404»
  > open.** Design: `engineering/analysis/2026-10-08-enh-03-compile-gate-design.md` (approved).
  > Gate: `engineering/tools/validation/audit-kb-code-compiles.py`; manifest root
  > `engineering/tools/validation/kb-compile-manifest/` (sidecars, never shipped). Points (1) and (2)
  > above are delivered: classes live in the sidecar manifest, not in the YAML, and the proposer
  > attributes each collision to the one name that caused it. `--negative-control`: 17 controls
  > (the 11 designed plus 6 opposite-case companions) all hold, and each fires when its guard is
  > removed (arbiter re-run: PASS, 2.1 s). **Re-measured census** (supersedes the 1913/438 figure
  > above): 1130 files, 0 parse errors; **2963 candidates in 581 files** (2476 under a code-named
  > key, 897 of those single-line; 487 found by compiler-recognised shape only); 2066 multi-line
  > in 498 files, 155 with `debug(`. Proposer over all 2963: 438 program, 1687 fragment,
  > **836 FAIL (B3's triage input)**, 2 HARNESS. Speed (24 cores): a populated full sweep 26 s; the
  > proposer 2 m 13 s — the "~25 min" estimate above does not hold. PNut-TS hang on a file with no
  > final newline is worked around (the gate adds one) and filed as punch-list item 5.

  > **PROGRESS 2026-10-09 — B4 done («#404»): the gate is a permanent release gate.**
  > `validate-dod-release.py` runs `validate_kb_code_compiles()` (negative control, then the full
  > sweep with its own 900 s timeout — measured 27 s wall / ~520 s CPU on 24 cores; the inherited
  > 300 s would not cover a single-core machine). `audit-gate-arming.py --show-tiers` lists it
  > ARMED by the runner. `release-yamls` names it as a BLOCKING §1 precondition, a §1.5 standing
  > check (`--since "$PREV"` plus an audit of the manifest diff — moves into `never`/`not-code`,
  > new `assumes` names and deleted entries are the hunks auditors read), in §5.5's command list
  > and in *What a green gate does NOT certify*. `yaml-knowledge-base-maintenance` gained §2.6
  > *Compile the code you touched* and a hand-back line. A DoD run now includes it and is RED on
  > the 352 registered blocks: no release until the close-out fixes them, as decided. Full sweep
  > time on Stephen's machine is not yet measured. The ENH-03 build is complete; this entry closes
  > when the close-out release ships green.

  > **PROGRESS 2026-10-09 — B3 done («#403»).** Every candidate is
  > classified: **3077 blocks — 501 program, 1932 fragment, 17 never (asserted to fail), 627
  > not-code (each with its reason)**, in sidecars under `kb-compile-manifest/`. A full sweep takes
  > 27 s and fails on **352 blocks, every one REGISTERED** against a close-out study row (105
  > distinct rows) — none unclassified, none unregistered, no tooling gap left. Ten review groups,
  > each a fresh reviewer, verified by the arbiter in a fresh scratch root before writing the real
  > manifest; evidence in `engineering/analysis/2026-10-08-p2kb-close-out-evidence/`. The review
  > also produced **266 study rows** (S-001..S-266) — compile defects and the prose defects the
  > reviewers read on the way — in `engineering/analysis/2026-10-08-p2kb-close-out-study.md` §3.
  > Five tooling passes widened the harness honestly (version-gated built-ins, flow statements in
  > the net, result/VAR wraps, valued constants, STRUCT types, PASM labels, end-of-file `never`);
  > 37 negative controls, each shown to fire when its guard is removed. The census grew 2963 →
  > 3077 when the net learned flow statements (S-109). Two compiler questions went to the PNut-TS
  > punch list (items 6, 7), each to be checked against PNut first. Still outside the net by design:
  > single-line strings (S-256 asks whether tutorial one-liners should come in) and text YAML has
  > already cut (S-183/S-200: 47 served strings truncated at ` #`; needs its own gate).

  > **Drained for `language/pasm2` 2026-10-10 («#418»).** Every pasm2 finding in the manifest is
  > gone (86 entries in 29 files → 0 `finding:` under `kb-compile-manifest/language/pasm2`; the
  > 18 `S-137` quick_example entries were already compiling). The ` #` plain-scalar gate
  > (`audit-yaml-plain-scalar-comment.py`) reads 47 flagged in 15 files → 0; the D3 bare-constant
  > sites (`false`/`true`/`negx`/`posx`/`multi_cog_synchronization`) → 0. Stack: EF-094 — a 9th
  > push discards the oldest entry and entries are 32 bits (the "22 bits" claim is gone from
  > `stack_operations.yaml` and `architecture/cog.yaml`, whose push/pop lists also named CALLA/CALLB/
  > CALLD/RETA/RETB, which use no hardware stack); EF-101 — a zero XORO32 state is absorbing.
  > Wider findings fixed in the same pass: the ALTS+`JMP #0-0` computed-jump idiom (the immediate
  > branch assembles as a relative offset, so the substituted S field gives a wrong target) is now a
  > table of `JMP #case` entries entered with `JMP reg`; `architecture/cordic.yaml` `pollqmt` was
  > "check if CORDIC pipeline empty" (the QMT flag is set by a GETQX/GETQY with nothing queued);
  > the WAIT-family `timing.cycles: 2` is now `2+` as each page's encoding says (15 pages); the
  > Spin2 `spin2-pasm2-integration` `JMP @slowCode` register-indirect form is `JMP #\@slowCode`.

  *Filed 2026-08-21;
  Stephen's call, and he asked for it in these words: "we must, for all code in YAML files, compile
  that code and assure ourselves that it compiles correctly. We do not publish a release unless all
  the code publishes correctly."* Nothing in this project compiles KB code examples, which is how
  F-311…F-313 and F-315 shipped. **Census: 1913 code-shaped blocks across 438 files; only 118 are
  complete programs, so 1795 need a synthesized context.** Design points already settled:
  - **The blocker is not the compiler, it is that the KB never declares which strings are code.** A
    heuristic sweep pulled 166 of 541 PASM2-shaped blocks out of *prose* fields. So the first
    deliverable is a per-block marker — `compile: program` / `compile: fragment` /
    `compile: never` + reason — not a runner. A guessing gate cries wolf, and a gate that cries wolf
    gets ignored.
  - **`compile: never` must be ASSERTED TO FAIL**, not skipped. The KB teaches anti-patterns; a
    wrong-code example that quietly starts compiling means the wrongness was edited away.
  - **It proves LEGALITY, not correctness**, and must never be cited otherwise. F-312 is the proof:
    fixing `qvector y_val` so it assembles would have left X and Y still swapped.
  - **No build stamps** (PL-004). The gate runs against whatever compiler is installed; a bump that
    breaks something turns the release red, which is the gate working. That is also what makes the
    surviving `re-verify on a compiler version bump` notes deletable.
  - Prototype validated 2026-08-21: it asks the compiler which identifiers are declarable rather than
    carrying a keyword list that would rot. 4/4 known-bad caught, 4/4 known-good passed. Its known
    weakness is auto-declaration colliding with symbols a block defines itself, which produced
    `Symbol is already defined` on blocks that compile correctly by hand — fix that before trusting
    any pass-rate number from it.
  - Hooks: `release-yamls` as a hard gate (~0.8 s/block, ~25 min full sweep), and
    `yaml-knowledge-base-maintenance` on touched files so it fails at edit time, not release time.

- **ENH-02 — make the platform fail loudly on a code line that cannot fit.** *Filed 2026-08-21 when F-281 closed.* F-281's three over-wide lines were fixed and v1.1.3 shipped margin-clean, but **nothing stops the class recurring**: `p2kb-platform-code-coloring.lua` emits `\begin{Verbatim}[xleftmargin=-10pt]` with no break options at all ten sites, and the `breaklines=true` at `p2kb-platform-foundation.sty:317` is a pre-existing `\lstset` that the Verbatim path never consults. So an over-long line silently runs off the page and the compile log stays clean — the exact shape of every render defect this project has shipped. The source-side `audit-code-line-length.py` gate catches most of it, and `audit-pdf-margin-overflow.py` catches it after the fact; what is missing is the platform refusing to typeset it. Not a defect in any document — an absent guard.

- **ENH-01 — Harvest the Architect's Guide *project front-end* into a new KB node set.** *Scheduled
  2026-07-08 (deferred from the Architect's Guide v1.0.0 release); Stephen go/no-go before authoring.*
  Source: *The P2 Architect's Guide* v1.0.0, **Part I (Act I)**. The decomposition-reasoning layer
  (`architecture/decomposition/`) begins *at* "which cog owns what"; nothing in the KB captures the
  **pre-decomposition** front-of-project work Part I lays out. Candidate new node set — reusable P2
  **design-process** patterns that sit *above* the decomposition layer: feasibility-before-design ·
  **narrow-vs-broad comms selection** (I²C/SPI vs host-style ribbon) · **offload-vs-port /
  companion-device partitioning** · pin-budget → adapter-board · "characterization becomes the spec" ·
  firmware-loaded-device → loader. Also a small KB touch worth doing: **performance → P2-resource
  mapping** (which performance need → LUT RAM / PSRAM / CORDIC / streamer — Architect's Guide Act III
  P-7). **Do NOT harvest the Act III agentic principles** (about *using agents*, not the P2 — low KB
  value). Fuller rationale table lives in the manual's `PLANNING.md` (KB-harvest proposals).

---

## Open — TRACKED in the ingestion head (resolution lives there, not in a YAML edit)

- **F-123 — TAQOZ-Forth / ROM-Monitor capability detail rests partly on preliminary web research.** `TRACKED → ingestion` Grounding plan in `engineering/ingestion/sources/taqoz/taqoz-content-gaps-and-grounding-plan.md` (mine `ROM_Booter.lst`; verify vs Peter Jakacki's `TAQOZ.spin2`).
  > **Routing re-verified 2026-08-25 («#300») — still live, and one of its two inputs is missing.** The
  > routing target resolves: the grounding plan exists at the path above, and the first input is in hand —
  > `engineering/ingestion/sources/rom-booter/ROM_Booter.lst` **and** `rom_booter_v33_01j.lst` are both
  > present (the `v33_01j` copy is the one E-005 cites, so it is the mined edition). **The second input is
  > NOT in hand:** no `TAQOZ*.spin2` exists anywhere in the repo, so the *"verify vs Peter Jakacki's
  > `TAQOZ.spin2`"* half cannot run today. **What would settle it:** obtain Jakacki's `TAQOZ.spin2` source;
  > until then the ROM-monitor half is groundable from `ROM_Booter.lst` alone and the Forth-vocabulary half
  > is not. Stays `TRACKED → ingestion` — the preliminary web-research material
  > (`taqoz-web-research-preliminary.md`) remains community-tier and is still not citable.
  >
  > 🔴 **CORRECTED 2026-09-10 by F-421 — this plan names the WRONG listing.** *"mine
  > `ROM_Booter.lst`"* points at the **FPGA** build (`ver = "A"`, Prop123-A9/BeMicro-A9).
  > The chip's ROM is `rom_booter_v33_01j.lst` (`ver = "G"`, Prop2 Silicon v2) — same source
  > version v141, different build target. Mine THAT one; the FPGA listing carries FPGA clock
  > constants, a different SD call structure, and a reserved long that silicon uses for MBR
  > validation. Keep `ROM_Booter.lst` only as the labelled FPGA comparison point.

---

## ADC gain-mode input ranges framed ground-referenced, not centered on VIO/2 (2026-07-07) — F-202

### F-202 — IOSP §16.2 ADC input-mode table (and 5 propagated sites) frame the gain ranges as ground-referenced `0V–ceiling` — `PARTIAL — the KB and the IOSP ch16/appendix-c windows ship as measured; two stale phrases still say the windows are "being characterized on hardware" (IOSP ch16 :532, appendix-d :192) (re-verified 2026-10-05 «#386»)`
> **Source of report:** community reviewer (2026-07-07, relayed by Stephen): *"the ranges are totally
> wrong… they are centred around 1.65V."* Community-tier input (Titus-tier): challenges our work, is not
> itself a citable source.
> **TRUST-CHAIN DISCIPLINE (Stephen, 2026-07-07):** the **P2AN\*** app notes are derived from the SAME
> ingested sources as the manuals — a **peer derivation, NOT an authority**. Do not justify manual content
> against P2AN001/§16.3; ground only against trusted **ingested** sources (Silicon Doc) or **empirical**
> hardware (EF ledger). This finding was re-grounded on that basis.
> **What the Silicon Doc (trusted ingested) DOES ground:**
> - **GIO/VIO are calibration sources, not input-range modes** — *"Delta-sigma ADC with 5 ranges, 2
>   **sources**, and **VIO/GIO calibration**."* The §16.2 table mislabels them as ranges (`GIO = 0V–3.3V`,
>   `VIO = VIO-relative`). WRONG per a trusted source.
> - **The ADC has a ~mid-supply bias point** — Rev C note: FLOAT mode "useful for determining the
>   **floating bias point of the ADC**." So the gain window sits around mid-supply, **not up from 0 V** —
>   the table's ground-referenced framing is wrong.
> - Tell-tale of how it happened: the table's ceilings (`1.04V / 330mV / 104mV / 33mV`) equal `3.3V ÷ gain`
>   — correct range **widths** placed at `[0, width]` (generic unipolar-PGA assumption) instead of around
>   the mid-supply bias. (§16.7 L469 and §16.3 already describe the bias/references correctly — but those
>   are peer manual sections, cited here only as internal-inconsistency evidence, not as authority.)
> **RESOLUTION — nominal transfer characteristic (releasable-correct without hardware):**
> The exact endpoints are a **nominal / definitional** quantity, not a measured one: the mid-supply
> reference is grounded (Silicon Doc float-bias-point) and the gain factors are grounded (Silicon Doc
> "5 ranges" + image catalog), so the window `= 1.65 V ± (1.65 V / gain)` about mid-supply is **DERIVED**
> (like the Ohm's-law drive currents and `clkfreq/2³²` NCO resolution we already print), NOT AT_RISK —
> **provided it is labelled *nominal* and carries the calibration caveat** (exact endpoints vary with device
> tolerance + VIO; for absolute work calibrate against GIO/VIO, §16.3). This mirrors the manual's already-correct
> nominal-vs-measured handling of resolution ([[F-201]]). This is the distinction I initially over-collapsed:
> a *measured precision spec* needs silicon; the *nominal transfer characteristic* does not. So §16.2 prints the
> nominal windows (labelled) — correct, complete, hardware-independent.
> **Verification split (per VERIFICATION-OPPORTUNITIES.md):**
> - **VO-J-001 (jumper-only — we do it):** on-chip DAC → jumper → ADC pin sweep confirms the centering + √10
>   window scaling on silicon (upgrades nominal → silicon-confirmed). Task #172. NOT a release blocker.
> - **VO-X-001 (external-hardware — cataloged, not committed):** calibrated external reference + precision meter
>   for tolerance-bounded absolute endpoints. Benefit: nominal → datasheet-grade. Deferred.
> **Propagated sites (all same root), IOSP opus-master `part-3-input-modes/chapter-16-adc.md` unless noted:**
> §16.2 table (L39–46) · §16.2 prose (L50–60) · §16.2 example "0-100mV sensor → 30x" (L64–66) ·
> §16.7 Example 4 thermocouple "0-50mV → 100x" (L505–517) · §16.7 quick-ref table (L636–640) ·
> `part-5-appendices/appendix-d-mode-comparison-charts.md` (L195–198). The **examples are the worst**:
> they feed a ground-referenced small-signal sensor (0-100 mV, 0-50 mV thermocouple, mic, strain gauge)
> into a 1.65 V-centered gain mode with **no mid-rail bias network** — they would not work as written.
> **NOT affected (checked, don't over-correct):** §16.3 ratiometric (correct) · §16.7 float note L469
> (correct) · **DAC ranges ch10** `0–3.3V`/`0–2.0V` (correct — DAC is genuinely unipolar 0-to-Vfs,
> matches Silicon Doc drive-level table). Defect is **specific to ADC gain modes**.
> **Secondary check:** `architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml` L144–145 calls
> GIO/VIO "Ground-referenced input / VIO-referenced input" — loose (they're calibration references);
> tighten wording, and confirm no range claim depends on the ground-referenced framing.
> **SILICON-CONFIRMED 2026-07-07 (EF-024) — supersedes the nominal formula.** VO-J-001 ran on real P2:
> gain modes ARE centered on mid-supply (~1.64 V measured) [structural, definitive], but the **derived
> `1.65 ± 1.65/gain` (3.3 V/gain width) was WRONG** — measured widths are ~1.4× wider (≈4.55 V/gain), √10-laddered.
> Measured representative windows (N=1): 3.16× 0.93–2.36 V · 10× 1.41–1.87 V · 31.6× 1.57–1.71 V · 100× 1.61–1.66 V.
> **Fold into IOSP v1.0.4** (staged): (a) GIO/VIO reclassified [APPLIED]; (b) mid-supply framing + examples
> fixed [APPLIED]; (c) **print the MEASURED windows** (table above) across §16.2 + Appendix B + Appendix C,
> labelled *measured on real P2 silicon, representative single-sample* (per the citation convention), NOT the
> derived formula; rebuild the two examples on the measured centering [PENDING apply]. With (c), F-202 is
> **CLOSED for release** and now hardware-grounded (not merely derived). VO-X-001 (absolute tolerance across
> parts) remains the optional datasheet-grade upgrade.

> ### KB-SIDE SECONDARY CHECK DISCHARGED 2026-08-25 («#300») — and this entry's HEADLINE is stale
>
> 🔴 **Read the headline against this block.** The heading still says *"exact centered endpoints UNVERIFIED
> (no trusted numeric source) → **hardware campaign required**"*. **That campaign already ran.** The
> `SILICON-CONFIRMED 2026-07-07 (EF-024)` note immediately above is the result, and
> `VERIFICATION-OPPORTUNITIES.md:38` records **VO-J-001 → DONE → EF-024**. A top-down reader stops at the
> heading and concludes this is blocked on silicon we cannot reach; it is not. **This is exactly the failure
> mode REGISTER-CONSULTATION §1 exists for** — the status sits at the end, and here the end supersedes the
> front. The heading is left in place rather than rewritten because the entry is mid-flight on the manual
> side, but nothing downstream should quote it.
>
> **KB FIX APPLIED — the "Secondary check" line above, now discharged.**
> `deliverables/ai/P2/architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml`:
> - `:143-151` — `adc_input_modes` no longer calls GIO/VIO input ranges. `P_ADC_GIO` / `P_ADC_VIO` now read
>   *"…calibration reference to the ADC (a calibration **SOURCE**, not an input range)"*, and `P_ADC_FLOAT`
>   states its actual purpose. Grounded in-file on **Silicon Doc `p2-documentation.txt:452`** — *"Delta-sigma
>   ADC with 5 ranges, 2 **sources**, and **VIO/GIO calibration**"* — with the mode-name glosses cited to
>   **`spin2-v55-text.txt:1466-1473`** (*"ADC GIO → IN"* / *"ADC VIO → IN"* / *"ADC FLOAT → IN"*), and
>   `P_ADC_FLOAT`'s bias-point role to **`p2-documentation.txt:188-190`** (Rev C: *"…but floats the ADC input.
>   This mode is now useful for determining the floating bias point of the ADC."*).
> - `:168-169` — **the range claim that depended on the ground-referenced framing is gone.** The old note
>   *"ADC input modes (GIO/VIO/gain) affect voltage range and sensitivity"* lumped the calibration sources in
>   with the gain ladder as if all of them set a range. It now separates them, and a second note carries the
>   structural EF-024 result: *"The gain-mode window is **CENTERED ON MID-SUPPLY (~VIO/2)**, not referenced up
>   from 0V … centered at ~1.64V for every gain (EF-024). A ground-referenced small-signal source needs a
>   mid-rail bias network before it can be read through a gain mode"* — which is the trap that made this
>   finding's worked examples unrunnable.
> - **Only the structural half of EF-024 was carried into the KB, deliberately.** EF-024 grades the centering
>   as *[structural, definitive]* but its window endpoints as a **representative single sample (N=1)**. The
>   centering is stated; **the N=1 endpoint numbers are NOT printed in the KB**, because a bare table there
>   would read as a specification. Printing them, labelled, is step (c) above — **manual-side, «#301»**.
> - Verified after the edit: `validate-crossref-keys.py` 3161 refs / 0 unresolved ·
>   `audit-yaml-claim-sourcing.py` 0 Tier-1, Tier-2 unchanged at 78 · `verify-yaml-format.py` clean.
>
> **THE GAP THAT ACTUALLY REMAINS — and it is NOT the centering.** It is **VO-X-001**, cataloged at
> `VERIFICATION-OPPORTUNITIES.md:51`: *tolerance-bounded **absolute** endpoints across parts and
> temperatures.* **What would settle it:** a calibrated, traceable external voltage reference plus a
> precision meter, exercised across several parts — **external hardware, which this container cannot reach**
> and which is `CATALOGED`, not committed. Its own entry says it is *"not needed for correctness."*
> **No endpoint number was supplied here, and none should be** — the measured N=1 windows in EF-024 are the
> only figures with evidence behind them, and they are labelled as such at their source.

---

## Render-verification wave — defects found by READING the generated PDFs (2026-08-17/19) — F-284…F-294, F-299…F-301

**Origin.** Verifying the six generated wave PDFs page by page rather than reading their compile
logs. Every finding below was invisible to a clean log: LaTeX ate an operator, a filter split a
line, a glyph printed nothing, a gate skipped the blocks it was built to check. F-295…F-298 closed
at the XBYTE sprint closeout and are archived.

> **These sat under the wrong header until 2026-08-21.** The 2026-08-19 sweep archived
> F-259…F-263 but left their `## Community bench review — refaQtor` header in place, so all
> fourteen read as part of a third party's bench review. That header is now in the archive with
> the findings it introduced. Detected by `audit-register-hygiene.py` check 9.

### F-301 — the cross-ref filter's adopt-at-next-release rule was passed over about a dozen times, because nothing read the tracker. `PARTIAL` (re-verified 2026-10-05 «#386»: the structural fix landed; only P2AN003, P2AN005 and P2AN006 still lack the cross-ref filter) — **detected 2026-08-19 by comparing the tracker against every `request.json`**

**The rule, written into `CROSSREF-FILTER-ADOPTION.md` when the filter shipped 2026-06-26:**
*"The next time each manual is released (for any reason), its release MUST add
`p2kb-platform-crossref` to that manual's `request.json` `lua_filters` and visually audit the
rendered PDF."* The tracker even names its own consumer — *"`release-manual` Phase 1/Phase 4
**should** consult this tracker."*

**Measured, not assumed.** Every workspace `request.json` read directly against the tracker's rows:

| Document | Tracker | In `request.json`? | Releases since the rule |
|---|---|---|---|
| Assembly | ⏳ pending, at v3.1.0 | **no** | v3.1.1 → v3.1.6 |
| DeSilva | ⏳ pending, at v3.0.1 | **no** | v3.0.2 → v3.0.6 |
| Debug Window | ⏳ pending, at v1.0.1 | **no** | v1.0.2 → v1.1.3 |
| Getting Started | ⏳ pending, at v1.0.0 | **no** | v1.0.1 → v1.0.3 |
| Architect | ⏳ "in development" | **no** | released v1.0.3 |
| XBYTE | **absent from the table** | **no** | v1.0.0, v1.1.0 |
| 7 app notes | **absent from the table** | **no** | 20+ |
| IOSP | 🔧 adopting (pilot) | yes, ordering correct | audit never recorded |
| Streamer | ✅ adopted + audited | yes, ordering correct | — |

**Only two of fifteen ever adopted.** IOSP's row still reads "awaiting Stephen's regen + visual
audit" although it has released three times since, so its filter has certainly rendered — the
**audit** is what is unrecorded, and that half is the half that matters (a mis-fired auto-link is
exactly what the audit exists to catch).

**The statuses are not wrong. Nothing read them.** Every row above is an accurate record of a
decision that was then never consulted at the moment a release happened. This is the same failure
as [[F-281]]'s «#250» in a different costume — a correct record that is not where the decision gets
made — and it is why adoption state moved into `PLATFORM-FEATURE-ADOPTION.md`, which
`prepare-manual` consults on every prepare rather than "should" consult on release.

**FIX — structural, landed 2026-08-19:** one per-document × per-feature matrix
(`PLATFORM-FEATURE-ADOPTION.md`), seeded from **detected** state rather than from what each tracker
claimed, plus a `prepare-manual` check that surfaces a document's outstanding ⏳ features as work
owed **this** release. `CROSSREF-FILTER-ADOPTION.md` keeps the mechanism (including the mandatory
crossref-before-tables ordering) and its status table is frozen as history.

**Still owed per document:** the adopt + visual audit itself, at each document's next release —
that has not been shortcut, only made visible. **ssdb and pnut-term-ts release next and both sit at
⏳**, so they are the first two chances to stop the count growing.

> **RE-MEASURED 2026-08-25 («#302») — read out of every workspace `request.json`, not off the
> tracker, and the two agree row for row.** `p2kb-platform-crossref` present in the `lua_filters`
> list:
>
> | | Documents |
> |---|---|
> | **ADOPTED (4)** | Assembly Reference · I/O & Smart Pins · Streamer Guide · **PNut-Term-TS User Guide** |
> | **⏳ still owed (11 P2 documents)** | Architect's Guide · Debug Window · Getting Started · DeSilva · XBYTE · Single-Step Debugger · P2AN001…P2AN007 |
> | out of scope | `ai-privacy-guide`, `Donna-Manuscript` (private, non-P2), `p2-layout-torture-test` (instrument) |
>
> **The count stopped growing, which is the first evidence the structural fix works.**
> `pnut-term-ts-user-guide` was one of the two "first chances" this entry named, and it **took**
> the feature — adopted **and audited 27 of 27 on the returned PDF** (2026-08-23), the audit half
> that IOSP's pilot row never recorded. The other named chance, **Single-Step Debugger, is still
> ⏳** and is the next test of it.
>
> **This stays `CONFIRMED` because the per-document work is genuinely outstanding, not because
> anything is unknown.** Two things ride every future adoption and must not be dropped:
> **`p2kb-platform-crossref` MUST sit between `figures` and `tables`** (`tables` flattens each cell
> to a string and would leave table-borne refs dead — verified ordering in all four adopted
> `request.json`s), and **the visual audit on the returned PDF is the half that matters**, because
> a mis-fired auto-link is exactly what it exists to catch.

### F-300 — every published PDF in the set ships with empty Title and Author properties. `PARTIAL` — **MECHANISM LANDED + PROVEN 2026-08-19; 10 of the 17 published PDFs have adopted, 7 owed at their next render (re-measured 2026-09-21, «#344»)**

> **RE-MEASURED ON THE RELEASED ARTIFACTS 2026-09-21** («#344») — `pdfinfo` over every PDF in
> `deliverables/documents/DOCs/`, read from the shipped files themselves, not from a render log and
> not from this register. **10 of 17 now carry both Title and Author** (all `Iron Sheep Productions,
> LLC`), against 2 of 15 at the 2026-08-25 measurement. The set grew by two documents in the
> interval, so the denominator moved as well as the numerator.
>
> **Still empty, and each resolves at that document's next render — this is the expected shape of
> this finding, not debt:** `P2AN003` · `P2AN005` · `P2AN006` · `P2AN007` ·
> `P2-Architect-Guide` · `P2-Debug-Window-Manual` · `P2-XBYTE-Programming-Guide`.
>
> Status stays open deliberately: it is manual-head and per-document, so it cannot close until the
> last of those seven re-renders. It is `PARTIAL` rather than `PENDING-VALIDATION` because the
> mechanism is proven and adopting is now routine — what remains is render scheduling, not
> validation.

> **ADOPTION MEASURED ON THE ARTIFACTS, 2026-08-25 («#302») — `pdfinfo` over every file in
> `deliverables/documents/DOCs/`, not read off the tracker.**
>
> | State | Count | Which |
> |---|---|---|
> | **Title + Author + Subject + Keywords populated** | **2** | Assembly Reference (`P2 Assembly Language Reference Manual` / `Iron Sheep Productions, LLC`), Streamer Guide (`P2 Streamer Programming Guide` / same) |
> | **all four fields still EMPTY** | **13** | Getting Started · I/O & Smart Pins · DeSilva · Debug Window · Architect's Guide · XBYTE · P2AN001…P2AN007 |
>
> The mechanism is also proven on two documents that are **not yet published to `DOCs/`**
> (Single-Step Debugger, PNut-Term-TS User Guide), so four conversions exist in total.
>
> **This stays `PENDING-VALIDATION`, and it closes per document, on a render — never on an edit
> here.** Each of the 13 adopts by rendering on `EXEC_ENV_CANONICAL`; there is no container-side
> action that can advance it. Per-document state is `PLATFORM-FEATURE-ADOPTION.md`, which
> `prepare-manual` consults, and the measurement above agrees with it row for row.
>
> ⚠️ **`pdfsubject` IS being populated**, contrary to this entry's step 4 (*"Do NOT wire
> `pdfsubject`"*): both adopted PDFs carry a `Subject`. That does not misreport either of them —
> neither appears in **F-317**'s drift table — but it means F-317 is **live at every adoption**, not
> deferred, and each of the 13 must have its `request.json` subtitle reconciled to its printed cover
> **before** it renders.

> **RESOLUTION (2026-08-19).** The fix is **not** the one-line `pdfusetitle` this entry proposed —
> that would have populated the info dictionary and left the cover as a second hand-maintained copy
> of the same five strings, and would have shipped *wrong* titles on 9 of 15 (see the template table
> below). What landed instead: **every identity string lives once, in the document's `request.json`
> metadata, and reaches both the PDF info dictionary and the cover page from there**, via
> `\DocTitle`/`\DocSubtitle`/`\DocVersion`/`\DocDate`/`\DocAuthor` defined in
> `p2kb-platform-foundation.sty` (§ DOCUMENT METADATA). The macros carry the *value*; the cover keeps
> its *presentation*.
>
> **Proven on the interactive daemon, four round-trips, by reading the rendered PDF** — not the
> success flag. Both first converts (Single-Step Debugger, PNut-Term-TS User Guide) came back with
> compile logs clean on every serious signature and Title/Author/Subject populated for the first
> time, covers rendered and looked at. Commit `09958b0a`.
>
> **Unconverted documents are safe:** the foundation `\providecommand`s all five macros empty, so a
> template that has not opted in writes exactly what it wrote before. **Per-document adoption state
> is `PLATFORM-FEATURE-ADOPTION.md`**, and `prepare-manual` now reads it. The analysis below stands
> as the record of how the fix was found; only the proposed one-liner is superseded.

**Surfaced by** the Streamer v1.0.9 release verification — reading the delivered PDF's metadata
dictionary, then checking whether it was a Streamer regression. It is not: **all 15 PDFs in
`deliverables/documents/DOCs/` report `(empty)` for both `title` and `author`** — eight manuals and
seven app notes. Only `creator` (`LaTeX with hyperref`) and `producer` (`xdvipdfmx`) are set.

**What a reader sees.** A PDF viewer's title bar and Document Properties fall back to the *filename*
instead of the document's name, and anything indexing the file — a search tool, a library, a
citation manager — finds no title or author to key on.

**The mechanism, traced end to end.** The `.latex` template sets `\title{P2 Streamer Programming
Guide}` (generated `.tex` line 31), and `p2kb-platform-foundation.sty:259` sets a `\hypersetup`
block — but that block configures **only** link colors and bookmarks. It never sets `pdftitle` or
`pdfauthor`, and **hyperref does not derive them from `\title{}` on its own**; that requires either
`pdfusetitle` or explicit keys. So the title exists in the document body and never reaches the PDF
info dictionary.

**FIX (one line, in the shared platform):** add `pdfusetitle` — or explicit
`pdftitle={...}, pdfauthor={...}` — to the `\hypersetup` block at
`p2kb-platform-foundation.sty:259`. **Zero layout risk**: it writes the PDF info dictionary only and
cannot reflow a page. This is what distinguishes it from [[F-299]], which is parked because it
*does* move type.

**Corrects a claim in our own process doc.** The `prepare-manual` skill states that a `request.json`
metadata change "feeds PDF properties, not just the build." For this manual-production path that is
**not true** — the template hardcodes `\title{}`, and nothing carries `request.json`'s
`metadata.{title,author,version}` into the PDF info dictionary. Re-staging `request.json` on a
document switch is still mandatory for a different and real reason (input/template/filters), so the
rule stands; only its stated justification about PDF properties is wrong. Fix that sentence when the
platform fix lands.

**Sequencing.** No manual should re-render just for this. Let it ride with the next render each
document takes anyway, and take it in the same set-wide sweep as [[F-299]] — one `forge-test` pass,
two set-wide render changes.

> **Stale reference removed 2026-08-19.** This sentence named the fancyvrb `breaklines` work «#250»
> as a third member of the sweep. That work was **REJECTED 2026-08-17** on the round-trip evidence
> (see [[F-281]]); the reference was written after the rejection and never checked against it. The
> sweep is F-300 + F-299, and F-299 is polish. There is no breaklines work to schedule.

⚠️ **TRAP FOR WHOEVER TAKES THIS FIX — the two title sources already disagree.** Because nothing
consumes `request.json`'s metadata today, nobody has had to keep it in step with the cover, and it
has drifted. On the Streamer: the **cover** reads *"Comprehensive Reference for Propeller 2 Streamer
Hardware"* while `request.json` reads *"Comprehensive Reference for the Propeller 2 Streamer"*. The
moment `pdftitle`/`pdfsubject` start being populated, whichever source the fix wires up becomes
reader-visible, and a stale one ships silently. **Before adopting: audit cover-vs-`request.json`
across all 15 documents and reconcile, then decide which source is authoritative** (the cover is
what a reader actually sees, so it should win). Do not wire the metadata through without that pass.

**THAT AUDIT IS NOW MEASURED (2026-08-19), and the drift is systemic, not a Streamer typo.** Comparing
each master's cover block (`\fontsize{36}…\bfseries` title + `{\Large\itshape …}` subtitle) against
its `request.json` `metadata.subtitle`, over the 15 published documents:

| Verdict | Count | Which |
|---|---|---|
| **SAME** | 3 | Architect, Assembly, Getting Started |
| **DRIFT** | 8 | Debug Window, Streamer, P2AN001, P2AN002, P2AN003, P2AN004, P2AN005, P2AN007 |
| **cover block not matched by this scan** | 4 | IOSP, deSilva, XBYTE, P2AN006 — a different cover shape, **unresolved, not clean** |

**Two of the drifts are kinds of drift, not typos, and they change what the fix has to decide:**
1. **The app notes disagree structurally.** `request.json` carries a *catalog label* — "Application
   Note P2AN001 — No External ADC" — while the cover carries a *reader subtitle*: "No external ADC —
   a single-pin instrumentation ADC…". Neither is a stale copy of the other. Wiring the cover through
   verbatim drops the P2AN00N designator from the PDF's Title; wiring `request.json` through gives
   every app note a title that is not what its cover says. **Decide this before touching the
   platform** — likely `pdftitle` = title + designator, `pdfsubject` = the reader subtitle.
2. **Cover strings contain LaTeX.** PNut-Term-TS's cover subtitle carries a literal `\\` line break.
   PDF info-dictionary fields are plain text, so any such markup must be stripped, not passed through
   — one more reason `pdfusetitle` (which takes `\title{}` as-is) is not automatically the right
   mechanism for the subtitle half.

Truncation was not checked: two of these subtitles run past 50 characters and the register scan
compared full strings, so the counts above are exact for equality but say nothing about length limits.

---

**⚠️ THE SUBTITLE DRIFT IS NOT THE GATE. The gate is the templates, and nobody had looked at them
(traced 2026-08-19).** `pdfusetitle` populates `pdftitle` from `\title{}` and `pdfauthor` from
`\author{}` — it never touches the subtitle. So the drift table above gates only a `pdfsubject` we do
not have to wire. What actually decides whether this fix can be turned on and left to ride is what
each template declares, and **9 of the 15 declare something wrong:**

| Template `\title{}` | Documents | Verdict |
|---|---|---|
| `P2 Application Note` (hardcoded, SHARED) | **all 7 app notes** | **BROKEN** — `pdfusetitle` gives seven distinct documents one identical title. Worse than empty in a library or index. |
| `P2 XBYTE Programming Guide` | XBYTE | **STALE** — the released v1.1.0 cover reads *"P2 Interpreters & Emulators Guide"*. The template kept the pre-retitle name. |
| *(no `\title` and no `\author` at all)* | deSilva | **EMPTY** — would stay broken after the fix. |
| correct, matches cover | Architect, Assembly, Debug Window, Getting Started, IOSP, Streamer | ready |

`\author{Iron Sheep Productions, LLC}` is correct in every live template **except deSilva's**, which
has none.

**The one fact that makes all of this safe: `\title{}` is never rendered.** Every cover in the set is
hand-built in the master's `front-matter.md` (`\fontsize{36}{42}\selectfont\bfseries …`). There is no
`\maketitle` anywhere in the published set — the only one in the tree is in `ai-privacy-guide`, which
is not a published document. **So `\title{}` is metadata-only, and changing it cannot move a single
point of type on any page.** That is what turns this from a render-risk change into a ride-along.

**REVISED PLAN — prep in one commit, no renders, then ride:**
1. **Switch every live template from a hardcoded `\title{…}` to `\title{$title$}` / `\author{$author$}`.**
   `request.json` becomes the single source and a template can never go stale against its document
   again — this is what fixes the seven app notes and XBYTE at once, and it is durable rather than a
   catalog of literals to maintain. Verified safe: **`request.json` `metadata.title` equals the cover
   title for 14 of 15**, including all seven app notes (the cover carries the designator on its own
   eyebrow line — *"Propeller 2 • Application Note P2AN006"* — above the title, so nothing is lost).
2. **deSilva is the one real conflict, and it is BOTH fields.** Released cover: *"P2 Assembly
   Programming"* / *"A Human-Centered Approach to Parallel Processing"*. `request.json`:
   *"Discovering P2 Assembly"* / *"Build, Experiment, and Master the Propeller 2"*. The cover wins →
   update `request.json`, then give `p2kb-desilva.latex` the same `$title$`/`$author$` pair.
3. **Add `pdfusetitle`** to the `\hypersetup` at `p2kb-platform-foundation.sty:259`.
4. **Do NOT wire `pdfsubject`.** Leaving it out defers the whole subtitle question above at zero cost;
   revisit it as its own item whenever someone wants Subject populated.
5. **Add a `PLATFORM` ledger line and let each document absorb it at its next natural render.**
   Precedent for the standing: the 2026-07-13 mnemonic-bold line — *live-but-benign, not outstanding
   debt*. No manual re-renders for this.

**One `forge-test` still confirms three things before adoption**, none of them layout: that `$title$`
substitution actually reaches `\title{}` on this path, that `&` survives into the info dictionary
(IOSP *"P2 I/O & Smart Pins User Guide"*, P2AN006 *"Sizing Cog & Task Stacks"*), and that `pdfauthor`
lands. Read the output PDF's metadata dictionary, not the compile log.

### F-299 — wide `tblr` tables overhang the right text edge by ~5–6pt, in the platform, not the manual. `CONFIRMED` — **POLISH, NOT A GATE FAILURE: it is inside the project's own 20pt tolerance (re-graded 2026-08-19, same day, see the correction at the end)**

**Surfaced by** the Streamer v1.0.9 daemon pre-verify — a whole-document margin measurement of the
rendered PDF (every text span's `x1` against the 540pt text edge), not by the compile log, which was
clean on every serious signature in both the v1 and v2 renders.

**The defect.** Two of the Streamer's wide mode-reference tables push their rightmost column past
the text block: §6.2 *RDFAST → Pins/DACs* by **6.1pt** (`DAC Bits` header) and §8.x *Pins/DACs →
Hub* by **5.3pt** (`Hub Write` header). Visible as the table's horizontal rules extending past the
running-header rule directly above them. The compile log reports these as `Overfull \hbox
(26.6406pt too wide)` — the larger number is the whole `tblr` box including padding; the visible
overhang is the 5–6pt the measurement above reports.

**Why it is the platform's, not the manual's.** The column widths are computed by
`p2kb-platform-tables.lua`, which every manual in the set loads. Nothing in the Streamer's markdown
sets a width. A manual-side "fix" would mean hand-tuning a table the filter is supposed to own.

**NOT the two tables an earlier note predicted.** The Streamer release note expected the
`p2kb-platform-tables.lua` column fix to absorb "2 over-wide `Constant | Value | Description`
tables". These two are **6-column** `Mode | Symbol | Type | Pins | DAC Channels | DAC Bits` tables —
a different shape the fix does not reach. The prediction was not wrong about its own targets; it
was applied to the wrong pair. **A status note naming a fix is not evidence the fix covers what you
are looking at** — measure the artifact ([[feedback_status_line_is_not_evidence]]).

**Deliberately not fixed in this release.** A column-width change in
`p2kb-platform-tables.lua` reflows tables in **every** manual, so adopting it while Streamer is
mid-render means re-verifying the whole set against a changed table model for 6pt of rule overhang.
Schedule it when no manual is mid-render, and expect the absorbing manual's next render to shift
table layout. **Pair it with [[F-300]]** — both are set-wide render changes whose failure mode is a
page that looks fine in the log, and both want one `forge-test` sweep across the set rather than two.

> **Stale reference removed 2026-08-19.** This paragraph cited the fancyvrb `breaklines` work «#250»
> as the precedent it followed and the partner to pair with. That work was **REJECTED 2026-08-17**
> ([[F-281]]) — before this entry was written. The scheduling rule it borrowed is sound and stands on
> its own; the partner is F-300.

**Scope when taken:** measure every manual, not just the Streamer — the filter is shared, so any
manual with a 6-column table is a candidate.

---

⚠️ **CORRECTION, same day, before this entry could mislead anyone — I RE-GRADED MY OWN FINDING.**

I measured this with a hand-rolled PyMuPDF scan at a **4pt** threshold. **The project already has a
sanctioned instrument for exactly this** — `engineering/tools/validation/audit-pdf-margin-overflow.py`
— and I did not use it. Run against the shipped v1.0.9 PDF it reports:

```
text-block right edge: prose 540.0pt, code 540.0pt   (tolerance 20pt)
CLEAN  nothing crosses the margin (76 pages measured)
```

**The gate's tolerance is 20pt by design. These tables are 6.1pt and 5.3pt — comfortably inside it.**
So both statements are true and the second is the one that sets priority: the overhang is real and
visible if you look for it (the table rule extends a hair past the running-header rule), and it is
**not** something the project's own margin gate would ever block on.

There is direct precedent for accepting far more: the IOSP v1.0.9 PUBLISH line accepts a chart
bleeding **~24pt** past the text block on evidence — zero overlapping spans measured, every cell
readable — with the explicit note that *magnitude is never the verdict*. A 6pt rule overhang with no
overlap is a smaller version of the same accepted case.

**Re-grade: this is POLISH, not a defect owed.** Still worth taking in the set-wide sweep with
[[F-300]] because the fix is cheap once the platform is open anyway — but it must not be
described as a defect blocking anything, and no manual should re-render for it.

**The transferable lesson — the one worth more than the finding.** Reach for the project's own
instrument before hand-rolling a measurement. Mine was not wrong, but it carried **no calibrated
threshold**, so it reported a number without the judgement that makes the number mean something, and
I very nearly filed a tolerance-conformant table as a defect owed. A raw measurement is not a
verdict; the tolerance IS the verdict ([[feedback_validation_tool_verdict_is_a_claim]] — the inverse
case, where the tool PASSES and the hand-rolled scan is the one overstating).

> ### DISPOSITION CONFIRMED 2026-08-25 («#300») — the re-grade stands; nothing re-measured, nothing re-argued
>
> Carried on «#300»'s roster and **closed here as POLISH, per the same-day correction above.** The 6.1pt and
> 5.3pt overhangs sit inside this project's **20pt** margin tolerance, so
> `audit-pdf-margin-overflow.py` — the sanctioned instrument — reports the shipped v1.0.9 PDF **CLEAN across
> all 76 pages**. **The tolerance IS the verdict.**
>
> **Deliberately NOT re-measured.** A disposition already made on evidence does not get re-litigated by a
> later agent hoping for a different number; re-running the hand-rolled 4pt scan would only reproduce the
> mistake the correction above documents. **No PDF was re-graded and no manual re-rendered for this.**
>
> **Not a gap and not a defect owed** — it is scheduled work with no blocker: take it in the set-wide
> `p2kb-platform-tables.lua` sweep, paired with **F-300**, when no manual is mid-render. Nothing in this
> sprint is waiting on it, and **no document may cite it as blocking**.
