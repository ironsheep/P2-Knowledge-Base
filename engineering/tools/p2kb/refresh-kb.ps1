# P2 Knowledge Base Refresh Script v1.0
# Refreshes all cached scripts, index, and common files
# Usage: .\refresh-kb.ps1 [-Verbose]

param(
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

$BaseUrl = "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main"
$CacheDir = if ($env:P2KB_CACHE) { $env:P2KB_CACHE } else { "$env:USERPROFILE\.p2kb-cache" }

function Write-Log($Message) {
    if ($Verbose) { Write-Host "[INFO] $Message" -ForegroundColor Cyan }
}

function Write-Status($Message) {
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Err($Message) {
    Write-Host "✗ $Message" -ForegroundColor Red
}

# Ensure cache directory structure exists
New-Item -ItemType Directory -Path "$CacheDir\content" -Force | Out-Null
New-Item -ItemType Directory -Path "$CacheDir\obex" -Force | Out-Null

Write-Host "P2 Knowledge Base Refresh"
Write-Host "========================="

# =============================================================================
# Step 1: Update all scripts (including this one)
# =============================================================================
Write-Host ""
Write-Host "Updating scripts..."

# Fetch script
Write-Log "Downloading fetch-kb-file.ps1"
Invoke-WebRequest -Uri "$BaseUrl/engineering/tools/p2kb/fetch-kb-file.ps1" -OutFile "$CacheDir\fetch-kb-file.ps1"
Write-Status "fetch-kb-file.ps1"

# Refresh script (self-update)
Write-Log "Downloading refresh-kb.ps1"
Invoke-WebRequest -Uri "$BaseUrl/engineering/tools/p2kb/refresh-kb.ps1" -OutFile "$CacheDir\refresh-kb.ps1"
Write-Status "refresh-kb.ps1"

# OBEX helper
Write-Log "Downloading obex\download-helper.ps1"
Invoke-WebRequest -Uri "$BaseUrl/engineering/tools/p2kb/obex/download-helper.ps1" -OutFile "$CacheDir\obex\download-helper.ps1"
Write-Status "obex\download-helper.ps1"

# =============================================================================
# Step 2: Refresh index
# =============================================================================
Write-Host ""
Write-Host "Updating index..."

Write-Log "Downloading p2kb-index.json.gz"
$tempGz = "$CacheDir\p2kb-index.json.tmp.gz"
Invoke-WebRequest -Uri "$BaseUrl/deliverables/ai/p2kb-index.json.gz" -OutFile $tempGz

# Decompress
$input = New-Object System.IO.FileStream $tempGz, ([IO.FileMode]::Open)
$output = New-Object System.IO.FileStream "$CacheDir\p2kb-index.json", ([IO.FileMode]::Create)
$gzip = New-Object System.IO.Compression.GZipStream $input, ([IO.Compression.CompressionMode]::Decompress)
$gzip.CopyTo($output)
$gzip.Close(); $output.Close(); $input.Close()
Remove-Item $tempGz -ErrorAction SilentlyContinue

# Get entry count
$idx = Get-Content "$CacheDir\p2kb-index.json" -Raw | ConvertFrom-Json
Write-Status "p2kb-index.json ($($idx.system.total_entries) entries)"

# =============================================================================
# Step 3: Refresh common getting_started files
# =============================================================================
Write-Host ""
Write-Host "Updating common files..."

$CommonKeys = @(
    "p2kbGuideQuickQueries"
    "p2kbSpin2Spin2GettingStarted"
    "p2kbPasm2Pasm2GettingStarted"
    "p2kbToolsPnutTsCompiler"
)

function Get-PathForKey($key) {
    $entry = $idx.files.$key
    if ($entry) { return $entry.path }
    return $null
}

function Remove-Metadata($content) {
    $content -split "`n" | Where-Object {
        $_ -notmatch '^\s*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):'
    } | Out-String
}

foreach ($key in $CommonKeys) {
    $path = Get-PathForKey $key
    if ($path) {
        Write-Log "Fetching $key -> $path"
        $cacheFile = "$CacheDir\content\$key.yaml"
        $content = (Invoke-WebRequest -Uri "$BaseUrl/$path").Content
        $filtered = Remove-Metadata $content
        $filtered | Out-File -FilePath $cacheFile -Encoding UTF8 -NoNewline
        Write-Status $key
    } else {
        Write-Err "$key (not found in index)"
    }
}

# =============================================================================
# Step 4: Fetch root manifest and ai-instructions for reference
# =============================================================================
Write-Host ""
Write-Host "Updating manifests..."

Write-Log "Downloading propeller-knowledge-root.yaml"
Invoke-WebRequest -Uri "$BaseUrl/manifests/propeller-knowledge-root.yaml" -OutFile "$CacheDir\propeller-knowledge-root.yaml"
Write-Status "propeller-knowledge-root.yaml"

Write-Log "Downloading ai-instructions.yaml"
Invoke-WebRequest -Uri "$BaseUrl/manifests/ai-instructions.yaml" -OutFile "$CacheDir\ai-instructions.yaml"
Write-Status "ai-instructions.yaml"

# =============================================================================
# Done
# =============================================================================
Write-Host ""
Write-Host "Refresh complete!"
Write-Host ""
Write-Host "Cache location: $CacheDir"
Write-Host "To fetch content: $CacheDir\fetch-kb-file.ps1 <key>"
Write-Host "To download OBEX: $CacheDir\obex\download-helper.ps1 <package>"
