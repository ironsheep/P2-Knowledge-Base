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
