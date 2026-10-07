#!/bin/bash
# Assemble engineering/tools/p2kb/ps1-check/ -- the one folder Stephen copies to Windows
# to run verify-ps1-filter.ps1 (Stephen, 2026-10-07: the .ps1 scripts run only under his
# Windows emulator, outside any repository checkout). Copies, side by side: the check, the
# two scripts it verifies, and the four golden vector files. Git-ignored; rebuilt on demand.
set -e
cd "$(dirname "${BASH_SOURCE[0]}")"
rm -rf ps1-check
mkdir ps1-check
cp verify-ps1-filter.ps1 fetch-kb-file.ps1 refresh-kb.ps1 ps1-check/
cp ../p2kb-mcp/filter-test-vectors/{input,expected,empty-input,empty-expected}.yaml ps1-check/
ls -1 ps1-check
