# OBEX tools

One tool: **`obex-catalog-mirror.py`**. It is the only writer of the OBEX object YAMLs in
`deliverables/ai/P2/community/obex/objects/`. Each object mirrors its Parallax OBEX catalog page and
carries nothing of ours (KB v1.24.4). The full field list, and where each field comes from, is in
the tool's docstring. The shape is also shown in the objects folder's `_template.yaml`.

The 2025 discovery, repair and manifest scripts are retired to `archive/`, which is local and
git-ignored. `archive/README.md` says why each one was retired.

## Modes

```bash
T=engineering/tools/obex-integration/obex-catalog-mirror.py
P=<scratch dir>              # saved pages; a saved page is reused, never fetched twice

python3 $T discover --pages $P           # object pages on the P2 listing that have no YAML yet
python3 $T add --url <page URL> --pages $P   # start a YAML for one new object (id + page URL)
python3 $T fetch    --pages $P           # save every object's catalog page
python3 $T report   --pages $P --json $P/report.json   # what apply would change; writes nothing
python3 $T apply    --pages $P           # write every object, whole
```

- **Requests are polite:** one every 2.5 s, with a neutral User-Agent and no personal address.
- **On a problem, the YAML is left untouched:** a page that is missing, or whose field list or
  download section has a shape the tool doesn't know, is reported, never filled with a fallback.
- **`description_short`** is the one hand-authored field. `apply` keeps it as it is. A new object
  starts with it empty, and the release gate "OBEX One-Line Descriptions" fails until someone
  writes one.

## Runbook

The runbook (re-scan, new objects, close-out checklist) lives on the OBEX head dashboard:
`engineering/obex-integration/README.md`.
