#!/usr/bin/env python3
"""Build the delivery-filter certification bundle for the p2kb-mcp server.

Requested by Stephen, 2026-10-07: "you create test files - no commit - i copy to
other environment they test". The bundle is what the MCP agent runs agreement §9.2
against (engineering/tools/p2kb-mcp/MCP-DELIVERY-FILTER-HANDOFF.md); its layout is
§9.1. It is written to engineering/tools/p2kb-mcp/cert-bundle/ (git-ignored) and is
never committed.

Everything comes from the COMMITTED KB at HEAD: the script refuses a dirty
deliverables/ai/P2/ tree, so the index it generates (mtimes and sha256 included) is
exactly what a release would publish. The bundle's KB content is frozen at that
commit; a content finding during certification goes to the corrections register,
never into the bundle.

Expected outputs are produced by RUNNING the KB's reference engine (fetch-kb-file.sh
filter_metadata) with each rule, and cross-checked here against an independent
transcription of the agreement's §4.

Usage (repository root):  python3 engineering/tools/p2kb-mcp/build-filter-cert-bundle.py
"""

import copy
import gzip
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path.cwd()
OUT = REPO / "engineering/tools/p2kb-mcp/cert-bundle"
VECTORS = REPO / "engineering/tools/p2kb-mcp/filter-test-vectors"
FETCH_SH = REPO / "engineering/tools/p2kb/fetch-kb-file.sh"
BASE_URL = "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main"

# Variant B's rule: different on both axes, so the cache must be discarded and the
# output differs from the main rule across many files.
RULE_B = {"format": 1, "remove_fields": ["source", "sources"], "remove_column0_comments": False}


def die(msg):
    print(f"REFUSED: {msg}", file=sys.stderr)
    sys.exit(1)


def git(*args, binary=False):
    proc = subprocess.run(["git", *args], capture_output=True, cwd=REPO)
    if proc.returncode != 0:
        die(f"git {' '.join(args)} failed: {proc.stderr.decode()[:200]}")
    return proc.stdout if binary else proc.stdout.decode()


def rule_id(rule):
    text = (f"p2kb-delivery-filter\nformat={rule['format']}\n"
            f"remove_fields={','.join(rule['remove_fields'])}\n"
            f"remove_column0_comments={'true' if rule['remove_column0_comments'] else 'false'}\n")
    return hashlib.sha256(text.encode()).hexdigest()


def oracle(content, rule):
    """Independent transcription of agreement §4 (format 1)."""
    if content == "":
        return ""
    ws = " \t\n\v\f\r"
    fields = set(rule["remove_fields"])
    lines = content.split("\n")
    if content.endswith("\n"):
        lines = lines[:-1]
    out, dropping, drop_indent = [], False, 0
    for line in lines:
        if dropping:
            body = line.lstrip(ws)
            if body == "" or body.startswith("#"):
                continue
            if len(line) - len(body) > drop_indent:
                continue
            dropping = False
        if rule["remove_column0_comments"] and line.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(ws))
        rest = line[indent:]
        colon = rest.find(":")
        if colon > 0 and rest[:colon] in fields:
            drop_indent, dropping = indent, True
            continue
        out.append(line + "\n")
    return "".join(out)


def run_engine(raw_by_key, rule):
    """{key: filtered bytes} from fetch-kb-file.sh's own filter_metadata, one bash pass."""
    sh = FETCH_SH.read_text()
    start = sh.index("filter_metadata() {")
    fn = sh[start:sh.index("\n}\n", start) + 3]
    tmp = OUT / ".work"
    tmp.mkdir(parents=True, exist_ok=True)
    for key, raw in raw_by_key.items():
        (tmp / f"{key}.in").write_bytes(raw)
    driver = fn + '\nfor k in "$@"; do filter_metadata < "$W/$k.in" > "$W/$k.out"; done\n'
    env = dict(os.environ, W=str(tmp), RULE_FIELDS=",".join(rule["remove_fields"]),
               RULE_COL0="true" if rule["remove_column0_comments"] else "false")
    proc = subprocess.run(["bash", "-c", driver, "bash", *raw_by_key], env=env, capture_output=True)
    if proc.returncode != 0:
        die(f"reference engine failed: {proc.stderr.decode()[:200]}")
    out = {k: (tmp / f"{k}.out").read_bytes() for k in raw_by_key}
    shutil.rmtree(tmp)
    return out


def write_index(path_json, index):
    path_json.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(index, indent=2)
    path_json.write_text(text)
    with gzip.open(str(path_json) + ".gz", "wb") as gz:
        gz.write(text.encode())


def main():
    if git("status", "--porcelain", "--", "deliverables/ai/P2/").strip():
        die("deliverables/ai/P2/ has uncommitted changes -- the bundle certifies committed content only")
    head = git("rev-parse", "HEAD").strip()

    spec = importlib.util.spec_from_file_location("gen", REPO / "engineering/tools/generate-p2kb-index.py")
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    gen.assert_git_usable(REPO)
    index = gen.generate_index(REPO)
    rule = index["delivery_filter"]

    if OUT.exists():
        shutil.rmtree(OUT)
    serve = OUT / "serve"

    # serve/: the index and every indexed file, raw, exactly as committed at HEAD.
    write_index(serve / "deliverables/ai/p2kb-index.json", index)
    raw_by_key = {}
    for key, entry in index["files"].items():
        raw = git("show", f"HEAD:{entry['path']}", binary=True)
        if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            die(f"{key}: committed bytes do not match the index sha256")
        (serve / entry["path"]).parent.mkdir(parents=True, exist_ok=True)
        (serve / entry["path"]).write_bytes(raw)
        raw_by_key[key] = raw

    # expected/: main rule. variants/B: changed rule. Both by running the engine.
    expected = run_engine(raw_by_key, rule)
    expected_b = run_engine(raw_by_key, RULE_B)
    for key, raw in raw_by_key.items():
        text = raw.decode("utf-8")
        if expected[key].decode("utf-8") != oracle(text, rule):
            die(f"{key}: reference engine and the agreement transcription disagree (main rule)")
        if expected_b[key].decode("utf-8") != oracle(text, RULE_B):
            die(f"{key}: reference engine and the agreement transcription disagree (rule B)")
    (OUT / "expected").mkdir(parents=True)
    (OUT / "variants/B-changed-fields/expected").mkdir(parents=True)
    for key in raw_by_key:
        (OUT / "expected" / f"{key}.yaml").write_bytes(expected[key])
        (OUT / "variants/B-changed-fields/expected" / f"{key}.yaml").write_bytes(expected_b[key])
    differ = sum(1 for k in raw_by_key if expected[k] != expected_b[k])

    # Variant indexes: identical files/sha256, only the rule differs.
    a = copy.deepcopy(index)
    a["delivery_filter"]["format"] = 2
    write_index(OUT / "variants/A-unknown-format/p2kb-index.json", a)
    b = copy.deepcopy(index)
    b["delivery_filter"] = copy.deepcopy(RULE_B)
    write_index(OUT / "variants/B-changed-fields/p2kb-index.json", b)
    c = copy.deepcopy(index)
    del c["delivery_filter"]
    write_index(OUT / "variants/C-no-rule-block/p2kb-index.json", c)

    # vectors/
    (OUT / "vectors").mkdir()
    for name in ("input.yaml", "expected.yaml", "empty-input.yaml", "empty-expected.yaml"):
        shutil.copyfile(VECTORS / name, OUT / "vectors" / name)

    (OUT / "README.md").write_text(readme(head, index, rule, len(raw_by_key), differ))

    # MANIFEST.sha256 over every file in the bundle (written last, excludes itself).
    lines = []
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.sha256":
            lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(OUT).as_posix()}")
    (OUT / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")

    print(f"Bundle: {OUT}")
    print(f"  KB commit {head}; {len(raw_by_key)} files; expected/ {len(expected)}; "
          f"rule B differs from main on {differ} files; manifest {len(lines)} entries")
    print(f"  rule_id main {rule_id(rule)}  B {rule_id(RULE_B)}")


def readme(head, index, rule, nfiles, differ):
    return f"""# p2kb-mcp delivery-filter certification bundle

Built from P2-Knowledge-Base commit `{head}` (committed content only), index schema
{index['system']['version']}. The contract is `MCP-DELIVERY-FILTER-HANDOFF.md` (AGREED
2026-10-07); this bundle is its §9.1, and the steps below are its §9.2.

## What you need

This folder is self-contained: no network, no KB repository checkout, nothing outside it.
You need only your server build with `P2KB_BASE_URL` implemented, `sha256sum` (or
`Get-FileHash`) to check the copy, and any static HTTP server for `serve/` — the command
below uses `python3`; any other static server works the same. Copy the **whole** folder.

## Check the copy first

From this directory: `sha256sum -c MANIFEST.sha256` (every line must read OK). On Windows,
compare `Get-FileHash -Algorithm SHA256` against the same file.

## What is here

| Path | What |
|---|---|
| `serve/` | the `P2KB_BASE_URL` root: `deliverables/ai/p2kb-index.json(.gz)` and all {nfiles} indexed KB files, raw |
| `expected/<key>.yaml` | the KB reference engine's output under the main rule, one per index key ({nfiles}) |
| `variants/A-unknown-format/` | index with `delivery_filter.format = 2` |
| `variants/B-changed-fields/` | index with rule B, and `expected/` under rule B (differs from main on {differ} files) |
| `variants/C-no-rule-block/` | index with `delivery_filter` removed (§9.2 step 5) |
| `vectors/` | golden vectors: `input.yaml` → `expected.yaml`; `empty-input.yaml` → `empty-expected.yaml` (both zero bytes) |

Every variant's `files` entries and `sha256` values equal the main index's; only the rule differs.

## Rules and their `rule_id`

| Rule | Block | rule_id |
|---|---|---|
| main (= the agreement's built-in rule) | `{json.dumps(rule)}` | `{rule_id(rule)}` |
| B | `{json.dumps(RULE_B)}` | `{rule_id(RULE_B)}` |
| A | format 2 — must be **refused** | — |

## Serving

```
python3 -m http.server 8080 -d serve
P2KB_BASE_URL=http://localhost:8080
```

The server fetches `<base>/deliverables/ai/p2kb-index.json.gz` and `<base>/<files[key].path>`.
To switch variants, copy the variant's `p2kb-index.json.gz` (and `.json`) over the ones in
`serve/deliverables/ai/`. "Fresh cache" means: stop the server, delete its whole cache
directory (stamp and last-good rule included), start again.

## Steps (agreement §9.2), in order

Compare the **`content` field** of each `p2kb_get` result with the expected file, byte for byte.

1. **Golden vectors** (unit test, no server): with `BuiltinRule`, `Apply(vectors/input.yaml)`
   equals `vectors/expected.yaml`; `Apply(vectors/empty-input.yaml)` is empty;
   `BuiltinRule.RuleID()` = `{rule_id(rule)}`.
2. **Whole KB:** main index served, empty cache. For every key in the index, `content` equals
   `expected/<key>.yaml`. `p2kb_version`: `filter_rule_source` = `index`, `filter_rule_id` = main.
3. **Variant A:** serve A's index; `p2kb_refresh`. `p2kb_version`: source `last-good`, main
   `rule_id`, `filter_rule_refused.format` = 2. Outputs still equal `expected/`.
4. **Variant B:** serve B's index; `p2kb_refresh`. `p2kb_version`: source `index`, B's
   `rule_id`. Outputs equal `variants/B-changed-fields/expected/`.
5. **No rule block:** serve C's index; **fresh cache**. `p2kb_version`: source `built-in`,
   main `rule_id`. Outputs equal `expected/`.
6. **Unstamped cache:** main index; populate a cache; stop; delete only the cache stamp; start.
   Every body re-fetched; outputs equal `expected/`.
7. **Restart keeps a valid cache:** stop and start with the stamp intact; nothing re-fetched;
   outputs equal `expected/`.

Also unit-test `ParseRule` refusing: a missing `remove_column0_comments`, a string `format`, an
extra key, a duplicate name, an empty list, a name containing `-`.

## Reporting back (agreement §9.3)

To Stephen: the server version tested, pass/fail for each step, and for every mismatching key
the key name and a diff against the expected file. Nothing is released by either side until
every step passes.
"""


if __name__ == "__main__":
    main()
