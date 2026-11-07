# Silicon Doc carriage walk: agent brief

You are walking one line range of the P2 Silicon Doc from the source side, to find what the P2
Knowledge Base (the YAML files) carries, carries wrongly, or does not carry at all.

## Inputs
- Source: `/workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/silicon-doc-text.txt`
  (cite as `SD:<line>`). Read your WHOLE range, every line.
- KB: `/workspaces/P2-Knowledge-Base/deliverables/ai/P2/` (YAML). Search it with grep -rn (try several
  phrasings, mnemonics, numbers, bit patterns), and read the candidate file at the lines found.
- Already known: `/workspaces/P2-Knowledge-Base/engineering/planning/P2KB-CONTRACT-GAPS-SPRINT-PLAN.md`
  §1-§11. A fact the plan already lists is marked IN-PLAN (with the § number), not re-reported.

## Rules
- Read-only everywhere except your one output file. Do not edit any repository file.
- Never open `engineering/ingestion/external-inputs/p2-hdl-study/`.
- A fact is CONTRACT if correct code could depend on it (encodings, operand meanings, flag effects,
  timing a program can observe, addresses, modes, ordering rules, reset values, limits). It is
  MECHANISM if only someone building the chip or a simulator needs it. Record mechanism rows briefly.
- MATCH means the YAML says the same thing in meaning, not just that a related page exists. Quote the
  YAML text you compared (short). If the YAML is vaguer but not wrong, use PARTIAL and say what is
  missing.
- MISMATCH means the YAML states something the source contradicts. Quote both.
- NOT-CARRIED means you searched and no YAML states it. Name the searches you ran (terms) and the page
  where an agent would most likely look for it.
- Do not judge from memory: every row cites SD lines you read and YAML lines you read.

## Output
Write ONE file, the path given in your task, as markdown:

1. `## Sections` - each SD heading in your range with its line, and a one-line disposition.
2. `## Ledger` - a table: `SD lines | Fact (one line) | Contract/Mechanism | YAML home (file:line) or NOT-CARRIED | MATCH / PARTIAL / MISMATCH / NOT-CARRIED / IN-PLAN | Note (quotes, searches)`.
3. `## Findings` - only the MISMATCH and NOT-CARRIED contract rows, most consequential first, each with
   both quotes and the searches.

Then reply with a SHORT summary only (under 150 words): counts per disposition, and the five most
consequential findings in one line each. The file holds the detail.
