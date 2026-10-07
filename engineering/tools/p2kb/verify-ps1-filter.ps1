# Verify the PowerShell delivery filter -- run once on Windows after any .ps1 change.
#
# Requested by Stephen (2026-10-07): the .ps1 scripts run only under his Windows
# emulator, "let's do as little of this as possible". The filter's rule comes from the
# index, so a RULE change never needs this run -- only an edit to fetch-kb-file.ps1 or
# refresh-kb.ps1 does, and validate-dod-release.py fails the release until the hashes
# printed below are recorded in PS1-VERIFIED.md.
#
# No network. Loads fetch-kb-file.ps1's functions without running the script, then checks:
#   1. golden vectors (engineering/tools/p2kb-mcp/filter-test-vectors) and the empty pair
#   2. the rule reader on four index fixtures: rule present / absent / format 2 / changed
#   3. rule_id values, computed independently by the bash script
#   4. the cache stamp: unstamped and changed-rule caches are cleared, a matching one kept
#   5. both .ps1 scripts parse without errors
#   6. a negative control: a deliberately wrong expectation must be reported as a failure
#
# Usage: copy the folder engineering/tools/p2kb/ps1-check/ (built by
# build-ps1-check-folder.sh: this script, both .ps1 scripts and the four vector files,
# side by side) to Windows, then inside it:
#   powershell -ExecutionPolicy Bypass -File .\verify-ps1-filter.ps1
# It also runs in place in a repository checkout (engineering\tools\p2kb\).

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$fetch = Join-Path $here "fetch-kb-file.ps1"
$refresh = Join-Path $here "refresh-kb.ps1"
# Flat copy: everything beside this script. Repository checkout: the vectors folder.
$vectors = if (Test-Path (Join-Path $here "input.yaml")) { $here } else { Join-Path $here "..\p2kb-mcp\filter-test-vectors" }
foreach ($need in @($fetch, $refresh, (Join-Path $vectors "input.yaml"), (Join-Path $vectors "expected.yaml"),
                    (Join-Path $vectors "empty-input.yaml"), (Join-Path $vectors "empty-expected.yaml"))) {
    if (-not (Test-Path $need)) {
        Write-Host "FAIL -- missing $need (copy the whole ps1-check folder and run inside it)"
        exit 1
    }
}
$failures = New-Object System.Collections.Generic.List[string]

function Check {
    param([string]$Name, [bool]$Ok)
    if (-not $Ok) { $script:failures.Add($Name) }
}

# Bytes as text, line endings normalized to LF: a Windows checkout may have converted them.
function Read-Lf { param([string]$Path) ([System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)) -replace "`r`n", "`n" }

# Hash of a file's LF-normalized UTF-8 bytes -- the same value the validator computes on Linux.
function Get-LfHash {
    param([string]$Path)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes((Read-Lf $Path))
    return -join ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") })
}

# 5. Both scripts parse.
foreach ($p in @($fetch, $refresh)) {
    $tokens = $null; $errors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile($p, [ref]$tokens, [ref]$errors)
    Check "parse $(Split-Path -Leaf $p) ($($errors.Count) errors)" ($errors.Count -eq 0)
}

# Load the fetch script's functions (not its main body) into this scope.
$tokens = $null; $errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($fetch, [ref]$tokens, [ref]$errors)
foreach ($fn in $ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] }, $false)) {
    Invoke-Expression $fn.Extent.Text
}
$FilterEngineVersion = ($ast.Extent.Text -split "`n" | Where-Object { $_ -match '^\$FilterEngineVersion\s*=\s*"([^"]+)"' } | Select-Object -First 1) -replace '^\$FilterEngineVersion\s*=\s*"([^"]+)".*$', '$1'
$ShowDetails = $false

# 1. Golden vectors, with the built-in rule.
Check "vectors: input.yaml -> expected.yaml" ((Filter-Metadata -Content (Read-Lf "$vectors\input.yaml")) -ceq (Read-Lf "$vectors\expected.yaml"))
Check "vectors: empty input -> empty output" ((Filter-Metadata -Content (Read-Lf "$vectors\empty-input.yaml")) -ceq (Read-Lf "$vectors\empty-expected.yaml"))

# 2-4. Rule reader, rule_id and cache stamp on fixtures in a temp directory.
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("p2kb-ps1-verify-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $tmp | Out-Null
$IndexFile = Join-Path $tmp "p2kb-index.json"
$CacheDir = Join-Path $tmp "cache"
New-Item -ItemType Directory -Path $CacheDir | Out-Null
$builtinId = "b431af2a9f515c11fe5fd982642c636c6f8843bf89ed2c3003ee0e28c04877ee"   # agreement §3.1
$changedId = "1c59f31106a7096918596addaf9d7a6dff5ab770e73fdf828d698f3b90761219"   # ["source"], false -- from fetch-kb-file.sh
$present = '{"delivery_filter": {"format": 1, "remove_fields": ["documentation_level", "documentation_source", "enhancement_source", "last_updated", "manual_extraction_date", "source", "source_reference", "sources", "verified_against"], "remove_column0_comments": true}, "files": {}}'
$changed = '{"delivery_filter": {"format": 1, "remove_fields": ["source"], "remove_column0_comments": false}, "files": {}}'
try {
    [System.IO.File]::WriteAllText($IndexFile, $present)
    $r = Get-FilterRule
    Check "rule present: read from index" ($r.Source -eq "index")
    Check "rule present: rule_id = built-in value" ((Get-FilterRuleId $r) -ceq $builtinId)

    [System.IO.File]::WriteAllText($IndexFile, '{"files": {}}')
    $r = Get-FilterRule
    Check "rule absent: built-in rule" ($r.Source -eq "built-in" -and (Get-FilterRuleId $r) -ceq $builtinId)

    [System.IO.File]::WriteAllText($IndexFile, ($present -replace '"format": 1', '"format": 2'))
    Check "format 2: refused, built-in rule" ((Get-FilterRule).Source -eq "built-in")

    [System.IO.File]::WriteAllText($IndexFile, ($present -replace '"remove_column0_comments": true', '"remove_column0_comments": "yes"'))
    Check "string flag: refused, built-in rule" ((Get-FilterRule).Source -eq "built-in")

    [System.IO.File]::WriteAllText($IndexFile, $changed)
    $r = Get-FilterRule
    Check "changed rule: read from index" ($r.Source -eq "index" -and $r.Column0 -eq $false)
    Check "changed rule: rule_id matches the bash script" ((Get-FilterRuleId $r) -ceq $changedId)
    Check "changed rule: column-0 comment kept, source removed" ((Filter-Metadata -Content "# c`nsource: x`nkeep: 1`n" -Rule $r) -ceq "# c`nkeep: 1`n")

    # Cache stamp.
    $body = Join-Path $CacheDir "k.yaml"
    [System.IO.File]::WriteAllText($body, "x")
    Sync-CacheStamp $r
    Check "unstamped cache cleared" (-not (Test-Path $body))
    Check "stamp written" ((Get-Content (Join-Path $CacheDir ".filter-stamp") -Raw).Trim() -ceq "$changedId/$FilterEngineVersion")
    [System.IO.File]::WriteAllText($body, "x")
    Sync-CacheStamp $r
    Check "matching stamp keeps the cache" (Test-Path $body)
    [System.IO.File]::WriteAllText($IndexFile, $present)
    Sync-CacheStamp (Get-FilterRule)
    Check "changed rule clears the cache" (-not (Test-Path $body))
} finally {
    Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}

# 6. Negative control: the comparison above must be able to fail.
$wrong = (Read-Lf "$vectors\expected.yaml") + "extra: line`n"
$controlCaught = -not ((Filter-Metadata -Content (Read-Lf "$vectors\input.yaml")) -ceq $wrong)
Check "negative control: a wrong expectation is detected" $controlCaught

Write-Host "fetch-kb-file.ps1 sha256 (LF): $(Get-LfHash $fetch)"
Write-Host "refresh-kb.ps1    sha256 (LF): $(Get-LfHash $refresh)"
if ($failures.Count -eq 0) {
    Write-Host "PASS -- PowerShell delivery filter verified (engine $FilterEngineVersion)"
    exit 0
} else {
    Write-Host ("FAIL -- " + ($failures -join "; "))
    exit 1
}
