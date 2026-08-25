# P2-Knowledge-Base overlay — task-handoff

## Augments §1 — which gate closes a task, per head

`BUILD_COMMAND` / `TEST_COMMAND` are the **P2KB YAML** head's gates. A task that
touches no YAML is not closed by them and must not claim them; run the gate its
own head owns and say which one ran:

| Head / surface | The gate that closes the task |
|---|---|
| `yaml` (P2KB set) | `verify-yaml-format.py` + `validate-crossref-keys.py` |
| manual / app-note **prose** | `audit-code-line-length.py` (K from the descriptor) · `audit-inline-code-ascii.py` |
| the **guide layer** (creation-/voice-/style-guide, `MANUAL-DESCRIPTOR.md`) | `DOC_AUDIT_COMMAND` — must read PASS (`CONFORMANCE_GUIDES` strength: gate) |
| authored `.spin2` | `pnut-ts` (add `-d` for `debug()`) — legality only, never semantics |
| anything rendered | **provisional here** — the PDF gate is `EXEC_ENV_CANONICAL` |

## Augments §2 — the prose analogue of `simplify`

`simplify` reviews *code* for reuse and accidental complexity. Most tasks in this
project change **prose**, where that pass still has real content — it just asks
different questions. On a documentation task, run these four instead and record
the result the same way (a plain "nothing found" is a valid outcome):

1. **Duplication** — does the new text restate something that already lives
   elsewhere? A manual's rule belongs in one section; every other site points.
   (`documentation-voices-catalog.md`: never restate a shared rule; checklists
   point rather than re-encode.)
2. **Altitude** — is it in the chapter a reader would look in, rather than the
   chapter the defect happened to surface in?
3. **Dangling references** — does every `§N.N`, anchor, and cited path resolve?
4. **Perishability** — did a count, version, or vendor fact get written into
   reader prose where it will rot? State the mechanism, not the catalog.

*Certified 2026-08-20 («#267»).* Question 1 caught a word-for-word duplication of
the relocated §12.0 rule left behind in the §9.2 callout, in the same task that
relocated it.

## Augments §4 — the sprint resume key is `active_element`

Do **not** create a parallel `resume_<sprint-name>` key. This project's front
door (`whats-next`) reads the todo-mcp key **`active_element`**, so that key IS
the sprint's live narrative pointer; a second key nothing reads is the drift §4
exists to prevent. Update `active_element` at every task boundary, keeping its
`head:element` first line intact.

## Augments §6 — the hand-back is not finished until the NEXT task is dispatched

**Central §6 already says the hand-back is forward motion and that a failed clear
means "continue directly into the next task in this same turn." This overlay makes
it mechanical, because it was violated four times in one session by an agent that
had read §6 and agreed with it.**

> **The last tool call of a task-closing turn is the NEXT task's dispatch — not the
> summary, and not the commit.**

Under `arbiter-serial` a closing turn is a fixed sequence, and the summary comes
**after** the dispatch, never instead of it:

```
todo_complete + context_delete  →  boundary commit  →  active_element update
→  todo_start «#next»  →  breadcrumb  →  DISPATCH  →  then write the summary
```

**Why it kept failing, so the next agent recognises the shape in itself.** The
failure never looks like stopping. It looks like *finishing well*: the task really
is done, the verification really did pass, the summary really is worth writing —
and naming the next task at the end of it *feels* like forward motion because it
mentions the future. It is not. **A sentence that says "next is «#N»" and a turn
that opens «#N» are different acts, and only one of them is work.** {{USER_NAME}}
named it four times — *"you seem to have stopped"*, *"why stopped?!"* — each time
after a summary that ended by naming the next task.

**The test, applied before ending any task-closing turn:** *is my final tool call
the next task's dispatch?* If the answer is "no, my final call was the commit and
then I wrote prose", the turn is incomplete — go open the next task. Announcing an
intention is not a protection point and it is not a hand-off; it is a stop wearing
the vocabulary of progress.

**Where this genuinely ends.** Only two things end a closing turn without a
dispatch, and both are on the closed stop roster: the queue is empty (roster #8 —
nothing runnable remains), or the next task needs a decision {{USER_NAME}} owns
(roster #1). *"The next task looks big"*, *"this is a natural pause"*, and *"I
should report before continuing"* are none of those — he reads the report from
inside another agent's context, and a stopped agent does not have his attention.
