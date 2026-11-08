# YAML Certification Record

One row per YAML file under `deliverables/ai/P2/` that has been read whole against its sources.
The release gate `engineering/tools/validation/audit-yaml-certification-record.py` reads this table
and fails when a YAML file that differs from the latest KB tag has no row.

## What certified means

A file is certified when:

- every claim in the file is checked against a source line, a compile proof, or an EF/XF result;
- a claim with no support is corrected, or stated as not documented, in the same pass;
- the file gets one row in the table below.

The whole file is read, not only its changed lines. A file touched only for a `related:` link is
certified whole like any other.

## How to write a row

The table has four columns, in this order:

- **file**: the path relative to `deliverables/ai/P2/`, in backticks.
- **date**: the ISO date of the certification, `YYYY-MM-DD`.
- **sources read**: the source lines, compile proofs and EF/XF results the claims were checked against.
- **result**: `certified`, or `certified with fixes` plus a count in parentheses, e.g. `certified with fixes (3)`.

A re-certification updates the file's row. It never adds a second row for the same file. A file the
release deletes needs no row. A renamed file is a new path and needs its own row.

## Scope

This record covers the files the current sprint touches. The process plan that follows this sprint
extends the record to the founding files.

## Record

| file | date | sources read | result |
|---|---|---|---|
