# Operations — cross-cutting infrastructure

> The **Operations head**: the process, registers and lessons that every content head runs on.
> It is *not* a content head — it ships no document and no YAML, and it has **no
> `active_element` form**, so `whats-next` never resumes "into" it. Work here is always in
> service of a content head (Ingestion · YAML · Manual · OBEX · Quick Bytes), which is why the
> Heads Board lists its Next actionable as *"(infrastructure)"*.
>
> Front door → [`../README.md`](../README.md) · _Last refreshed: 2026-09-10._

## Registers — the standing to-do lists this head owns

| Register | State | What it is |
|---|---|---|
| [`P2KB-CORRECTION-FINDINGS.md`](P2KB-CORRECTION-FINDINGS.md) | **142 live** · 295 archived · 0 unaccounted · hygiene **CLEAN** · next ID **F-420** | Every *"this is wrong"* about the KB or a manual. **The only sanctioned route** — hand-carrying a correction drops half of it. |
| [`YAML-HEAD-DASHBOARD.md`](YAML-HEAD-DASHBOARD.md) | ledger current at **v1.18.0** (2026-09-09) | The YAML head's release ledger + served-hardware inventory. |
| [`P1-CORRECTION-FINDINGS.md`](P1-CORRECTION-FINDINGS.md) | P1 register (parked with the P1 effort) | The P2KB register's P1 twin. |
| [`lessons-learned/INDEX.md`](lessons-learned/INDEX.md) | 18 indexed | Rule → the incident that caused it. Read this before questioning a Sacred Rule. |
| [`../document-production/PUNCH-LIST.md`](../document-production/PUNCH-LIST.md) | **14 OPEN · 1 HALF · 3 RESOLVED** | Manual-head punch list (owned there, listed here because closeout sweeps it). |

**Register hygiene is gated, not asserted:**
`python3 engineering/tools/validation/audit-register-hygiene.py engineering/operations/P2KB-CORRECTION-FINDINGS.md`

## Process — where the rules live

| Document | Answers |
|---|---|
| [`PROCESS-GUIDANCE-ARCHITECTURE.md`](PROCESS-GUIDANCE-ARCHITECTURE.md) | Which guide governs which work type — the routing map CLAUDE.md points at. |
| [`PROCESS-DOC-CATALOG.md`](PROCESS-DOC-CATALOG.md) | The full inventory of process documents. |
| [`../standards/`](../standards/) | Conventions that gate work — backups, dashboard design, ingestion roles. |
| [`../procedures/`](../procedures/) | Step-by-step workflows (YAML, validation, release). |
| [`claude-guidance/`](claude-guidance/) | How an agent should enter and run each work type. |
| [`correction-sweeps/`](correction-sweeps/) | Dated archives of closed register findings. Never re-edited. |

## What "operations work" looks like

Process defects surface **inside** content work — a skill step in the wrong order, a gate that
reads a declaration instead of an artifact, a dashboard nothing writes. The rule is that the fix
ships **with the release that revealed it** (CLAUDE.md → *"Discipline updates ship with the work
that revealed them"*), so operations work is rarely a standalone sprint and almost always a
rider on a content head's release.

---

*Historical: this file was the **V1.0–V1.3 milestone board** until 2026-09-10 (last true
2025-09-13), and `INDEX.md` beside it was a master index whose 53 links had all gone dead.
Both were snapshots of a finished era. They are kept for retrospectives in the **gitignored**
`operations/archive/` — deliberately not tracked, per the project's archive convention — so the
durable record is git itself:*

```bash
git show 6766f4b7:engineering/operations/README.md    # the milestone board
git show 6766f4b7:engineering/operations/INDEX.md     # the master index
```
