# P2 Knowledge Base Refresh Script v3.2
# Updates scripts, index, and common files with migration from v3.1 structure
# Usage: .\refresh-kb.ps1 [-Verbose] [-Force]

param(
    [switch]$Verbose,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$BaseUrl = "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main"

# Determine script's directory (where this script lives)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Index and cache location (relative to script directory)
$IndexDir = if ($env:P2KB_INDEX) { $env:P2KB_INDEX } else { "$ScriptDir\.p2kb" }
$IndexFile = "$IndexDir\p2kb-index.json"
$CacheDir = "$IndexDir\cache"

function Write-Log {
    param([string]$Message)
    if ($Verbose) { Write-Host "[INFO] $Message" -ForegroundColor Cyan }
}

function Write-Status {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Err {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Warn {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

# =============================================================================
# Migration: Detect and migrate from v3.1 structure
# =============================================================================
function Invoke-Migration {
    $oldIndex = "$ScriptDir\p2kb-index.json"
    $oldContent = "$ScriptDir\content"
    $migrated = $false

    # Check for old index in script directory (v3.1 layout)
    if (Test-Path $oldIndex) {
        Write-Warn "Detected v3.1 layout - migrating to v3.2..."

        # Ensure new directories exist
        if (-not (Test-Path $IndexDir)) {
            New-Item -ItemType Directory -Path $IndexDir -Force | Out-Null
        }
        if (-not (Test-Path $CacheDir)) {
            New-Item -ItemType Directory -Path $CacheDir -Force | Out-Null
        }

        # Move index file
        if ((-not (Test-Path $IndexFile)) -or $Force) {
            Write-Log "Moving index to $IndexFile"
            Move-Item -Path $oldIndex -Destination $IndexFile -Force
            Write-Status "Migrated index"
            $migrated = $true
        } else {
            Write-Log "Index already exists at new location, removing old"
            Remove-Item -Path $oldIndex -Force
        }
    }

    # Check for old content directory
    if (Test-Path $oldContent) {
        $files = Get-ChildItem -Path $oldContent -Filter "*.yaml" -ErrorAction SilentlyContinue
        if ($files) {
            Write-Log "Moving $($files.Count) cached files to $CacheDir"
            foreach ($f in $files) {
                $destPath = Join-Path $CacheDir $f.Name
                if ((-not (Test-Path $destPath)) -or $Force) {
                    Move-Item -Path $f.FullName -Destination $CacheDir -Force
                } else {
                    Remove-Item -Path $f.FullName -Force  # Already exists, remove old
                }
            }
            Write-Status "Migrated $($files.Count) cached files"
            $migrated = $true
        }

        # Remove old content directory if empty
        $remaining = Get-ChildItem -Path $oldContent -ErrorAction SilentlyContinue
        if (-not $remaining) {
            Remove-Item -Path $oldContent -Force -ErrorAction SilentlyContinue
        }
    }

    # Clean up any stray old files
    Remove-Item -Path "$ScriptDir\index.json" -Force -ErrorAction SilentlyContinue

    if ($migrated) {
        Write-Host ""
        Write-Host "Migration complete! Index and cache now stored in:"
        Write-Host "  $IndexDir (hidden)" -ForegroundColor Gray
        Write-Host ""
    }
}

# =============================================================================
# Directory Setup
# =============================================================================
function Ensure-Directories {
    if (-not (Test-Path $ScriptDir)) {
        New-Item -ItemType Directory -Path $ScriptDir -Force | Out-Null
    }
    if (-not (Test-Path "$ScriptDir\obex")) {
        New-Item -ItemType Directory -Path "$ScriptDir\obex" -Force | Out-Null
    }
    if (-not (Test-Path $IndexDir)) {
        New-Item -ItemType Directory -Path $IndexDir -Force | Out-Null
    }
    if (-not (Test-Path $CacheDir)) {
        New-Item -ItemType Directory -Path $CacheDir -Force | Out-Null
    }
}

# =============================================================================
# Main
# =============================================================================

Write-Host "P2 Knowledge Base Refresh v3.2"
Write-Host "=============================="

# Ensure all directories exist
Ensure-Directories

# Check for and migrate old structure
Invoke-Migration

# =============================================================================
# Step 1: Update all scripts (including this one)
# =============================================================================
Write-Host ""
Write-Host "Updating scripts..."

# Cache-control header to bypass GitHub CDN cache
$NoCacheHeaders = @{"Cache-Control"="no-cache"}

# Fetch script
Write-Log "Downloading fetch-kb-file.ps1"
Invoke-WebRequest -Uri "$BaseUrl/engineering/tools/p2kb/fetch-kb-file.ps1" -Headers $NoCacheHeaders -OutFile "$ScriptDir\fetch-kb-file.ps1"
Write-Status "fetch-kb-file.ps1"

# Refresh script (self-update)
Write-Log "Downloading refresh-kb.ps1"
Invoke-WebRequest -Uri "$BaseUrl/engineering/tools/p2kb/refresh-kb.ps1" -Headers $NoCacheHeaders -OutFile "$ScriptDir\refresh-kb.ps1"
Write-Status "refresh-kb.ps1"

# OBEX helper
Write-Log "Downloading obex\download-helper.ps1"
Invoke-WebRequest -Uri "$BaseUrl/engineering/tools/p2kb/obex/download-helper.ps1" -Headers $NoCacheHeaders -OutFile "$ScriptDir\obex\download-helper.ps1"
Write-Status "obex\download-helper.ps1"

# =============================================================================
# Step 2: Refresh index (to hidden location)
# =============================================================================
Write-Host ""
Write-Host "Updating index..."

Write-Log "Downloading p2kb-index.json.gz"
$tempGz = "$IndexFile.tmp.gz"
$tempJson = "$IndexFile.tmp"

Invoke-WebRequest -Uri "$BaseUrl/deliverables/ai/p2kb-index.json.gz" -Headers $NoCacheHeaders -OutFile $tempGz

# Decompress gzip
$input = [System.IO.File]::OpenRead($tempGz)
$output = [System.IO.File]::Create($tempJson)
$gzip = New-Object System.IO.Compression.GZipStream($input, [System.IO.Compression.CompressionMode]::Decompress)
$gzip.CopyTo($output)
$gzip.Close()
$output.Close()
$input.Close()

Move-Item -Path $tempJson -Destination $IndexFile -Force
Remove-Item -Path $tempGz -Force -ErrorAction SilentlyContinue

# Get entry count and category count
$idx = Get-Content $IndexFile -Raw | ConvertFrom-Json
$entries = $idx.system.total_entries
$categories = $idx.system.total_categories
if ($categories -and $categories -gt 0) {
    Write-Status "p2kb-index.json - $entries entries, $categories categories"
} else {
    Write-Status "p2kb-index.json - $entries entries"
}

# =============================================================================
# Step 3: Refresh common getting-started files
# =============================================================================
Write-Host ""
Write-Host "Updating common files..."

# List of commonly-needed files to pre-cache
$CommonKeys = @(
    "p2kbGuideQuickQueries"
    "p2kbGuideSpin2GettingStarted"
    "p2kbGuidePasm2GettingStarted"
)

function Get-PathForKey {
    param([string]$key)
    if ($idx.files.PSObject.Properties.Name -contains $key) {
        return $idx.files.$key.path
    }
    return $null
}

function Filter-Metadata {
    param([string]$Content)
    $lines = $Content -split "`n"
    $filtered = $lines | Where-Object {
        $_ -notmatch '^\s*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):'
    }
    return $filtered -join "`n"
}

foreach ($key in $CommonKeys) {
    $path = Get-PathForKey $key
    if ($path) {
        Write-Log "Fetching $key -> $path"
        $cacheFile = "$CacheDir\$key.yaml"
        $content = (Invoke-WebRequest -Uri "$BaseUrl/$path" -Headers $NoCacheHeaders -UseBasicParsing).Content
        $filtered = Filter-Metadata $content
        $filtered | Out-File -FilePath $cacheFile -Encoding UTF8 -NoNewline
        Write-Status $key
    } else {
        Write-Err "$key - not found in index"
    }
}

# =============================================================================
# Step 4: Fetch reference files
# =============================================================================
Write-Host ""
Write-Host "Updating reference files..."

Write-Log "Downloading propeller-knowledge-root.yaml"
Invoke-WebRequest -Uri "$BaseUrl/manifests/propeller-knowledge-root.yaml" -Headers $NoCacheHeaders -OutFile "$IndexDir\propeller-knowledge-root.yaml"
Write-Status "propeller-knowledge-root.yaml"

Write-Log "Downloading ai-instructions.yaml"
Invoke-WebRequest -Uri "$BaseUrl/manifests/ai-instructions.yaml" -Headers $NoCacheHeaders -OutFile "$IndexDir\ai-instructions.yaml"
Write-Status "ai-instructions.yaml"

# =============================================================================
# Done
# =============================================================================
Write-Host ""
Write-Host "Refresh complete!"
Write-Host ""
Write-Host "Scripts location: $ScriptDir"
Write-Host "Index/cache location: $IndexDir (hidden)" -ForegroundColor Gray
Write-Host ""
Write-Host "Usage:"
Write-Host "  $ScriptDir\fetch-kb-file.ps1 -Help      Show all commands"
Write-Host "  $ScriptDir\fetch-kb-file.ps1 -Browse    Browse by category"
Write-Host "  $ScriptDir\fetch-kb-file.ps1 -Search    Search for keys"
Write-Host "  $ScriptDir\fetch-kb-file.ps1 <key>      Fetch content"
