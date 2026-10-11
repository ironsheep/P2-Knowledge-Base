# PowerShell delivery-filter verification record

The `.ps1` scripts cannot run in the development container, so they are verified by one
run of `verify-ps1-filter.ps1` on Windows whenever either script changes (Stephen,
2026-10-07: "let's do as little of this as possible"). A change to the filter's **rule**
needs no run — the rule comes from the index.

`validate-dod-release.py` ("PowerShell Filter Verified") fails the release unless the
SHA-256 of each script's LF-normalized content equals the value recorded below with
`result: PASS`. Edit a `.ps1`, and the gate stays red until the check is run again and
its printed hashes are recorded here.

**To run:** build the folder with `engineering/tools/p2kb/build-ps1-check-folder.sh`, copy
`engineering/tools/p2kb/ps1-check/` (seven files) to Windows, and inside it run:

```
powershell -ExecutionPolicy Bypass -File .\verify-ps1-filter.ps1
```

## Latest run

```
date: 2026-10-11 (Stephen, Windows PowerShell under his Windows emulator; folder copy)
engine: 3.5
fetch-kb-file.ps1: 12ff79da70780dd6438a6cf541cbf9751676de84fc1c87a71c8a22db98abf1e9
refresh-kb.ps1: 7ba88c3aeafdcdead5fb53920d335966becb170d32b1a792acf2ace09b90a0f9
result: PASS
```
