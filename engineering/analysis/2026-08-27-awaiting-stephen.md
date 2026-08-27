# Awaiting Stephen — 2026-08-27

**What this is.** Everything from this sprint that genuinely needs *you*, and nothing that does not.
Each item says what was already done toward it, the options **with the cost of each**, and my
recommendation. Recommendations are mine; **nothing here records a decision, an acceptance or an
approval in your name.**

**Tree state.** Clean, committed, and **at release position** — all eight gates green
(`verify-yaml-format` · `validate-crossref-keys` · `audit-yaml-claim-sourcing` ·
`audit-constant-fidelity` · `audit-extraction-digit-density --all` · `audit-yaml-duplicate-keys` ·
`audit-register-hygiene` on all three registers · `validate-dod-release`, 11 checks). It is
**unreleased by design**: no version bump, no tag, no push.

**The full picture is in** `engineering/analysis/2026-08-27-yaml-release-change-ledger.md` — 89 YAML
files, 24 commits, §0.5 lists everything still open. This file is the subset that is yours.

**Six items. Only #1 blocks anything.**

---

## 1 — The release act itself

**Needs you because** your standing instruction is *do not release automatically*. The version
number, `git tag`, `push` and `release-yamls` are yours, and nothing in this sprint touched any of
them.

**Already done.** The tree is at release position and green (above). A `## [1.18.0] - 2026-08-25`
entry already sits in `CHANGELOG.md`, written on 2026-08-25 by `fc45912d`; the tag `v1.18.0` does
**not** exist. `deliverables/ai/P2/CHANGELOG.md` is a deliberate pointer at the repo changelog and
holds no entries of its own.

⚠️ **The staged entry covers only the first half of the sprint.** It was written at `0a5323ab`;
**13 commits and 28 more YAML files landed after it**, and none of what they carry appears in it —
the six fabricated-provenance files re-derived (including an **inverted interrupt vector map**), the
new package record, the streamer pin-capture page, the Click adapter ingestion, the duplicate-key
sweep, the restored clock-setup declarations, and the `ADDSX`/`SUBSX` flag correction. `release-yamls`
owns writing that entry, so this resolves itself if the release runs through the skill — flagged so
the gap is not discovered at tag time.

**Options.**

| | Cost |
|---|---|
| **Release now as `1.18.0`** | The entry must be refreshed first or it understates the release by half. Minor semver is right for the content shape (additions + corrections, no removals a consumer depends on). |
| **Release as `1.19.0`** and leave `1.18.0` as a never-tagged entry | A changelog with a version nobody can `git checkout` is a small, permanent lie. Only worth it if you consider 1.18.0 to have been "announced". |
| **Hold the release** until items 2-4 below are decided | Those decisions change file *content*, so releasing first means releasing twice. But none of them is a correctness risk to a consumer today, and the release fixes an inverted interrupt vector map that ships wrong right now. |

**My recommendation: release as `1.18.0` after `release-yamls` refreshes the entry, and do not wait
on items 2-6.** The tree fixes real, currently-shipping harm — the IJMP3/IJMP1 inversion, a pin
current figure five times the absolute maximum, and a C-flag semantic wrong exactly on overflow. The
open items are either "delete something we already flagged" or "decide a policy", and none of them
gets safer by shipping the current set for longer.

---

## 2 — F-359: eight claims that could not be re-derived, still standing in the shipped files

**Needs you because deletion is yours.** «#323» re-derived six `architecture/` files whose provenance
headers cited silicon-doc files that have never existed. Eight further claims survived the
re-derivation: **no source states them, and in two cases a source contradicts them.** They were
**collected rather than deleted**, deliberately.

**Already done.** All six files re-derived against the live silicon doc and datasheet — 41 wrong
encodings → 0, four non-existent mnemonics deleted, six semantic inversions corrected, every
`<file>:<line>` re-read at the line it names. The eight are enumerated in **F-359** in
`engineering/operations/P2KB-CORRECTION-FINDINGS.md`, each with what was searched for and where.

**The eight** — `locks.yaml` `state_bits: 4` · `lookup_ram.yaml` power consumption · `lookup_ram.yaml`
streaming bandwidth (that figure is the **hub RAM** rate) · `lookup_ram.yaml` internal bandwidth (a
restatement of RDLUT/WRLUT timings as a bandwidth) · `debug_interrupt.yaml` trace-buffer size ·
`debug_interrupt.yaml` debug-state size · `debug_interrupt.yaml` "debug can disrupt streamer
operations" (**the source makes the opposite kind of claim**) · `cog_attention.yaml` WAITATN latency
`0 clocks` (**the datasheet gives `2+`**).

**Options.**

| | Cost |
|---|---|
| **Delete all eight** | Two blocks lose their only content and go silent on a question a reader may ask. Consistent with cite-or-omit and with every other unsourced claim this sprint removed. |
| **Delete the two the sources contradict, keep six labelled** | Needs a label vocabulary the KB does not have — "no source, retained" is a hedge, and a remote agent cannot weigh a hedge. That is the failure mode cite-or-omit exists to prevent. |
| **Keep all eight as they are** | The release ships eight claims we have *established* have no source, in files this sprint touched specifically to end that condition. |

**My recommendation: delete all eight.** They are the same class the sprint spent itself removing,
and the two contradicted ones are actively wrong. If you want any of them back, they need a bench
result — which is a different thing from a citation, and a better one.

---

## 3 — `ENH-NN` is an ungoverned allocator, and it has already collided

**Needs you because** renumbering live register entries and inventing a status vocabulary for
proposals are register-owner calls.

**Already done.** «#327» made `audit-register-hygiene.py` print
`unmodelled series : ENH-NNN — ID-shaped entries this gate does NOT check` on every run, **without
failing on it**, so the question surfaces instead of staying silent. The gate deliberately does not
model the family, because modelling it turns the register red over a defect whose remedy is
renumbering.

**The collision.** `P2KB-CORRECTION-FINDINGS.md` carries `ENH-01`, `ENH-02`, `ENH-03` with no
declared counter, and live `ENH-02`/`ENH-03` name **different proposals** than the archived
`ENH-02`/`ENH-03` in `correction-sweeps/2026-08-15-…-archive.md`. Two entries share an ID across the
archive boundary, which is exactly the condition the hygiene gate exists to catch for `F-`, `G-`,
`Q-` and `E-`.

**Measured high-water mark:** the archive carries `ENH-02`…`ENH-05`; live carries `ENH-01`…`ENH-03`.
So the true next free ID is **`ENH-06`**, and a renumbering of the two colliding live entries lands
them at `ENH-06`/`ENH-07` with the counter declared at `ENH-08`.

**Options.**

| | Cost |
|---|---|
| **Renumber the live three, declare `Next enhancement ID`, and let the gate model the family** | One editing pass, then the family is governed like every other. The archived IDs stay as they are, since archives are read-only history. |
| **Move enhancements out to their own register** | Cleaner separation (an enhancement is not a correction), but a new file to maintain and a new place to forget to look. |
| **Leave it** | The next `ENH-` allocated has better-than-even odds of colliding again, and the gate will keep printing the line without stopping it. |

**My recommendation: renumber the live three and declare the counter in the corrections register.**
Three entries is the cheapest this will ever be, and a fourth register is a real cost for a
three-item family.

---

## 4 — F-367: two different Silicon Doc DOCX copies under one filename

**Needs you because** deleting or reconciling a source file is yours.

**Already done — the labelling half.** «#328» wrote `engineering/ingestion/external-inputs/p2/README.md`:
the folder is labelled a **staging area**, every file is mapped to its canonical `sources/` folder,
and the second Silicon Doc copy is marked **NOT authoritative** with both GETBRK readings quoted.
Nothing downstream is wrong — the `sources/` copy is demonstrably correct (the `external-inputs/`
copy sets `Z = 1` in *both* WZ branches, which would make `WZ` useless) and it is what every
extraction used.

**Also established, and it is *not* a second F-367:** the Hardware Manual exists in both places at
different sizes but **identical text** — the pair differs only in two images being PNG in one and GIF
in the other.

**Options.**

| | Cost |
|---|---|
| **Delete the `external-inputs/p2/` Silicon Doc copy** | Removes the trap outright. Loses a second copy of a large source you may have kept deliberately. |
| **Keep it, labelled** (today's state) | Zero effort; the README now says which is which. Someone still has to read the README before opening the wrong file. |
| **Reconcile — determine why the two differ** | The most informative outcome (they are different *editions* of one document, and knowing which is which may matter later). Also the most work, for a question nothing currently depends on. |

**My recommendation: keep it labelled, and do nothing more.** The correctness question is settled and
recorded; deleting a source to prevent a misreading the README already prevents is a net loss of
material.

---

## 5 — F-375: the delivery filter strips real citations from 383 files

**Needs you because it is a scope call, not a repair.** Nobody should start a 383-file rename unasked.

**Already done.** «#324» measured it end-to-end by running the real fetch script against the real
tree: **706 `documentation_source:` / `enhancement_source:` values are citation-shaped** — they name a
document, an edition, a page or a line — against **47** that are the bare internal tokens the filter
was designed for. The citation-shaped values sit in **383 distinct files**. Both delivery paths run
the same five-pattern line filter, so **the shipped set satisfies cite-or-omit on disk and is
delivered not satisfying it.** Every gate reads the tree; the consumer reads the filtered stream;
nothing compares them.

**A second, smaller half is already actionable and needs no decision:** `validate_metadata_filter`
in `validate-dod-release.py` checks *which line patterns the filter removed* and never re-parses the
filtered payload, so a block delivered as `null` passes it clean. That is a tool fix with a
ready-made negative control, not a scope question.

**Options.**

| | Cost |
|---|---|
| **Rename the 706 citation-shaped values to `source:`** and leave the filter's narrow meaning intact | The cleanest form, and the spelling the project already uses everywhere else. 383 files — a task, not an edit. Mechanical, but 383 files is 383 chances to break a parse, so it needs the duplicate-key and format gates on every step. |
| **Stop filtering the two fields entirely** | One-line change. Ships 47 bare tokens (`enhanced`, `original`, `p2_datasheet`) to consumers as noise. |
| **Filter by value, not by key** — delete only the 47 bare tokens | One tool change, no YAML churn. Adds a value-classifier to the delivery path, which is a place we have twice been burned by regex classification (F-335, F-359). |
| **Ship as-is** | The KB is cited; what we *serve* is not. |

**My recommendation: fix the gate now (it needs no decision), and do the 706-value rename as its own
task after the release.** It is the option with no new classifier in the delivery path, and the
release does not need to wait for it — the condition is unchanged from `v1.17.0`.

---

## 6 — G-027 / F-372: a bench question only you can run

**Needs you because it needs hardware.** Jumper-only, no external instrument.

**Already done.** The conflict is fully characterised and the KB now carries it *as a conflict*
rather than as fact. Propeller 2 Documentation v35's PDF-derived capture says outright *"A new WRPIN
can be done to effect such a change without resetting the smart pin"*; the DOCX capture of **the same
document** omits the sentence entirely, while stating the opposite general rule — a WRPIN while DIR
is high remaps 126 bits of state under a running mode, *"unpredictable and quite certainly useless
behavior"*. No third document separates them.

**The test.** Configure a USB pair, issue a new `WRPIN` with `%0_11011_0` while `DIR` is high, and
observe whether the pin keeps working or breaks.

**Options.** Run it (the KB gets a hardware-verified answer and G-027 closes) · leave it open (the KB
already presents both readings honestly, so nothing is misleading today) · treat USB as a documented
exception without testing (**not recommended** — that is inference, and the whole class of defect this
sprint cleared began as inference).

**My recommendation: queue it for the next bench session; it does not block the release.**

---

## Considered and deliberately NOT put on this list

So you can see what was triaged out rather than wonder whether it was missed.

- **F-378** (`_CLKFREQ` ships the compiler's acceptance range as a ceiling, 180 MHz past the silicon
  limit) — a real defect with a stated fix and an existing rule to apply (E-007's *label which
  framing you are quoting*). It needs a task, not a decision.
- **The duplicate-key gate is not wired into `validate-dod-release.py`** — it returns 0 across 1132
  files today, so wiring it in turns nothing red. Ordinary work.
- **F-352** (two blocks that are correct, actionable, and unsupportable by anything we hold) — the
  KB currently ships *without* them, which is the safe state. The open question is whether the
  removal rule wants a fourth branch; that can be proposed with a worked example rather than asked
  cold.
- **F-356** (the drive-strength mislabel is alive in the IOSP master at 23 sites) — genuinely yours,
  and genuinely a scope call, but it is a **manual-side** decision with no bearing on this KB
  release. It belongs in the next manual sprint's planning, not on a release hand-back.
- **The 48 Tier-2 advisory blocks and the 698 unchecked nested cross-reference sites** — both are
  measured, both are recorded (F-340, F-373), and both are unchanged from `v1.17.0`. They are
  standing conditions, not decisions.
