# Forum-Thread Ingestion — Policy & Convention

**Status:** Working policy (established 2026-07-01, first batch of 4 threads).
**Scope:** Ingesting Parallax P2 forum discussion threads into the KB as a
distinct, lighter-weight ingestion sub-class alongside document ingestion.

Forum threads are **community sources with one authoritative exception** — when
the P2 chip designer posts, that is ground truth. This policy says how we capture
a thread, how we tier its participants, where the result files go, and how their
findings flow into our manuals and YAML.

---

## 1. Trust model (the reason this sub-class is special)

| Poster | Tier | Handling |
|--------|------|----------|
| **`cgracey` (Chip Gracey)** — the P2 silicon designer | 🏆 **AUTHORITATIVE / TRUSTED** | His reasoning and solutions are trustable ground truth, comparable to the Silicon Doc. Capture **verbatim**. Findings flow into docs/YAML directly (still empirically overridable — silicon behavior on real hardware wins if it ever contradicts an informal forum post). |
| Any other poster | 🟢 domain-expert **or** 🟡 general community | **Individually qualified** per thread from the technical quality/correctness of *their* posts. Claims are **cross-check tier** — never authoritative; **verify against the KB / compiler / hardware before use.** A 🟢 rating means "worth taking seriously and testing," not "trusted." |

This mirrors the repo trust chain: empirical/hardware 🏆 ≥ Parallax documentary 🏆
> community/derived 🟡. The designer's own forum posts sit at the documentary-🏆
tier (he *is* the source of the silicon); everything else in a thread is community.

**Primary goal of every forum ingestion:** glean everything from Chip Gracey's
posts that could affect our documentation. Other posters matter mainly for (a)
context that makes his statements interpretable and (b) occasional 🟢 techniques
worth verifying.

---

## 2. Where the result files go (placement convention)

**Co-locate derived artifacts with the source** — each thread keeps its
`.webloc` bookmark, its raw capture, and its digest together in one folder:

```
engineering/ingestion/external-inputs/forum-threads/
├── README.md                          # glanceable index of all ingested threads
├── FORUM-THREAD-INGESTION-POLICY.md   # this file
└── <ThreadSlug>/
    ├── <title> — Parallax Forums.webloc   # the source bookmark (given)
    ├── raw-capture.md                     # verbatim posts, all pages, in order (the EVIDENCE)
    └── INGEST.md                          # the structured digest (the UNDERSTANDING)
```

Rationale: this matches the document-ingestion pattern (`sources/<src>/` holds the
source + its extraction-audit). Verbatim capture and the digest travel together so
a later reconciliation pass can re-read the evidence behind any claim.

`raw-capture.md` is git-committed (forum posts are small text; re-fetching later is
unreliable as threads/accounts change). No binaries.

---

## 3. Process (per thread)

1. **Resolve the URL** from the `.webloc` (`grep -o 'https://[^<]*'`).
2. **Chase pagination.** Parallax threads paginate as `…/discussion/<id>/<slug>/pN`.
   Fetch `/p1`; it reports the total page count; fetch `/p2 … /pN` until done.
3. **Capture verbatim** into `raw-capture.md` — every post, in order, with author +
   date + full text + fenced code. **Never paraphrase Chip Gracey's posts or any
   code** (paraphrase loses the evidence). Other posters may be captured tightly but
   completely enough to qualify them.
4. **Digest** into `INGEST.md` with the fixed section set (below).
5. **Route doc-impact findings** to the reconciliation queue (§5).

### `INGEST.md` fixed section set
- **Header** — Source URL, thread ID, pages, post count, OP author+date, fetch date, topic class.
- **Thread purpose** — one paragraph.
- **Participant trust classification** — table (User | Trust | Basis); `cgracey` = 🏆.
- **Chip Gracey findings (trusted gold)** — `### CG-N · <title>` each with the
  **verbatim** quote (+ code), a `**Means:**` interpretation, and `**Affects:**`
  (target doc/section/YAML/app-note, or "reference only").
- **Other credible technical contributions** — qualified posters' notable, verifiable
  claims, flagged community/cross-check.
- **Doc-impact targets (reconciliation queue)** — table (# | Finding | Target
  doc/section | Suggested action | Trust).
- **Open questions / unresolved.**

---

## 4. Fan-out (how a batch is run)

A batch of threads is embarrassingly parallel: one subagent per thread, each
fetching all pages, capturing verbatim, qualifying posters, and writing its two
files. The parent then synthesizes the top-level `README.md` index and the merged
reconciliation queue. (First batch: 4 threads, 2026-07-01.)

---

## 5. Reconciliation flow (what happens to the findings)

Forum ingestion **finds and understands**; it does not itself edit manuals or YAML.
Each `INGEST.md` doc-impact target is dispositioned downstream:

- **Chip Gracey 🏆 findings that contradict or extend a manual/YAML** → route to the
  **corrections register** (`engineering/operations/P2KB-CORRECTION-FINDINGS.md`) and
  fix through the owning skill (`document-audit` / `document-finalize` for manuals,
  `yaml-knowledge-base-maintenance` for YAML). A confirmed **silicon problem/erratum**
  is high-value — flag it explicitly.
- **🟢/🟡 community techniques** → verify first (KB / `pnut_ts` / hardware). Only
  promote what survives verification; log the rest as a gap or discard.
- **App-note fodder** → hand to the relevant `P2ANxxx` region (mine-and-delineate)
  rather than forcing it into a manual.

The reconciliation pass (audit each affected manual/app-note against the queue) is a
**separate step** run after the batch is captured and understood.

---

## 6. Skill candidacy

This policy is deliberately runnable-by-hand for a small batch. If forum ingestion
recurs, promote it to a `forum-thread-ingest` skill (front-to-back: resolve webloc →
chase pagination → verbatim capture → tiered digest → reconciliation-queue emit),
reusing the `ingest-source` conventions and this trust model. Tracked as a candidate;
not built for a one-off batch.
