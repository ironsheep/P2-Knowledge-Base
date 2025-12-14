# P2 Knowledge Base Fetch Script v3.2
# Key-based access to YAML content with navigation support
# Usage: ./fetch-kb-file.ps1 <key> | -Help | -Cached | -Browse <category> | -Search <term>

param(
    [Parameter(Position=0)]
    [string]$Key,

    [switch]$Help,
    [switch]$Cached,
    [string]$Browse,
    [string]$Search,
    [switch]$Categories,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

$BaseUrl = "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main"

# Determine script's directory (where this script lives)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Index and cache location (relative to script directory)
$IndexDir = if ($env:P2KB_INDEX) { $env:P2KB_INDEX } else { "$ScriptDir\.p2kb" }
$IndexFile = "$IndexDir\p2kb-index.json"
$CacheDir = "$IndexDir\cache"

$IndexMaxAge = 86400  # 24 hours in seconds

# =============================================================================
# Helper Functions
# =============================================================================

function Show-Help {
    @"
P2 Knowledge Base Fetch Script v3.2

USAGE:
    fetch-kb-file.ps1 <key>              Fetch content by key
    fetch-kb-file.ps1 -Cached            List downloaded keys
    fetch-kb-file.ps1 -Browse <cat>      Browse keys in category
    fetch-kb-file.ps1 -Search <term>     Search for keys (case-insensitive)
    fetch-kb-file.ps1 -Categories        List all available categories
    fetch-kb-file.ps1 -Help              Show this help

CATEGORIES (for -Browse):
    PASM2 Instructions:
      pasm2_directives, pasm2_branch, pasm2_cordic, pasm2_math, pasm2_pin,
      pasm2_event, pasm2_hub_control, pasm2_hub_fifo, pasm2_hub_ram,
      pasm2_interrupt, pasm2_lookup_table, pasm2_misc, pasm2_pixel,
      pasm2_register_indirection, pasm2_smart_pin, pasm2_streamer

    Architecture:
      architecture_core, architecture_math, architecture_timing,
      architecture_interrupts, architecture_sync, architecture_io

    Smart Pins:
      smart_pins_digital, smart_pins_serial, smart_pins_pwm,
      smart_pins_counting, smart_pins_timing, smart_pins_frequency,
      smart_pins_analog, smart_pins_special, smart_pins_beginner

    Spin2:
      spin2_control_flow, spin2_pin_control, spin2_timing, spin2_cog_control,
      spin2_memory, spin2_math, spin2_strings, spin2_smart_pins, spin2_locks

    Guides:
      guides_getting_started

EXAMPLES:
    fetch-kb-file.ps1 p2kbPasm2Mov           # Get MOV instruction
    fetch-kb-file.ps1 -Browse pasm2_branch   # List all branch instructions
    fetch-kb-file.ps1 -Search uart           # Find UART-related keys
    fetch-kb-file.ps1 -Cached                # Show what's already downloaded

KEY PREFIXES:
    p2kbPasm2*    - PASM2 assembly instructions
    p2kbSpin2*    - Spin2 methods and language elements
    p2kbArch*     - P2 architecture documentation
    p2kbGuide*    - Guides and quick references
    p2kbHw*       - Hardware specifications

IMPORTANT:
    Always use this script for P2KB access. Never access index or cache directly.
    Use -Browse or -Search to find valid keys. Never guess at key names.

"@
    exit 0
}

function Write-Log {
    param([string]$Message)
    if ($Verbose) {
        Write-Host "[INFO] $Message" -ForegroundColor Gray
    }
}

function Write-Error-Message {
    param([string]$Message)
    Write-Host "ERROR: $Message" -ForegroundColor Red
}

function Ensure-Directories {
    if (-not (Test-Path $IndexDir)) {
        New-Item -ItemType Directory -Path $IndexDir -Force | Out-Null
    }
    if (-not (Test-Path $CacheDir)) {
        New-Item -ItemType Directory -Path $CacheDir -Force | Out-Null
    }
}

function Refresh-Index {
    $needRefresh = $false

    if (-not (Test-Path $IndexFile)) {
        Write-Log "Index not found, downloading..."
        $needRefresh = $true
    } else {
        $fileInfo = Get-Item $IndexFile
        $age = (Get-Date) - $fileInfo.LastWriteTime
        if ($age.TotalSeconds -gt $IndexMaxAge) {
            Write-Log "Index is $([int]$age.TotalSeconds)s old (max ${IndexMaxAge}s), refreshing..."
            $needRefresh = $true
        }
    }

    if ($needRefresh) {
        Write-Log "Downloading index from $BaseUrl/deliverables/ai/p2kb-index.json.gz"
        $tempGz = "$IndexFile.tmp.gz"
        $tempJson = "$IndexFile.tmp"

        try {
            Invoke-WebRequest -Uri "$BaseUrl/deliverables/ai/p2kb-index.json.gz" -OutFile $tempGz

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

            $index = Get-Content $IndexFile | ConvertFrom-Json
            Write-Log "Index updated: $($index.system.total_entries) entries"
        } catch {
            Write-Error-Message "Failed to download index: $_"
            exit 1
        }
    }
}

function Get-Index {
    if (-not (Test-Path $IndexFile)) {
        Refresh-Index
    }
    return Get-Content $IndexFile -Raw | ConvertFrom-Json
}

function Lookup-Key {
    param([string]$KeyName)
    $index = Get-Index
    if ($index.files.PSObject.Properties.Name -contains $KeyName) {
        return $index.files.$KeyName.path
    }
    return $null
}

function Find-SimilarKeys {
    param([string]$KeyName)
    $index = Get-Index

    # Extract portion of key to search for
    $searchTerm = if ($KeyName.Length -gt 8) { $KeyName.Substring(4, 8) } else { $KeyName.Substring(4) }

    $similar = $index.files.PSObject.Properties.Name |
        Where-Object { $_ -match $searchTerm } |
        Select-Object -First 5

    return $similar
}

function Filter-Metadata {
    param([string]$Content)
    $lines = $Content -split "`n"
    $filtered = $lines | Where-Object {
        $_ -notmatch '^\s*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):'
    }
    return $filtered -join "`n"
}

# =============================================================================
# Command: -Cached - List downloaded keys
# =============================================================================
function Invoke-Cached {
    if (Test-Path $CacheDir) {
        $files = Get-ChildItem -Path $CacheDir -Filter "*.yaml" -ErrorAction SilentlyContinue
        if ($files) {
            $files | ForEach-Object { $_.BaseName }
            Write-Host ""
            Write-Host "Total: $($files.Count) cached files" -ForegroundColor Gray
        } else {
            Write-Host "No cached files found." -ForegroundColor Yellow
        }
    } else {
        Write-Host "Cache directory not found. No files cached yet." -ForegroundColor Yellow
    }
    exit 0
}

# =============================================================================
# Command: -Browse <category> - Show keys in category
# =============================================================================
function Invoke-Browse {
    param([string]$Category)

    if ([string]::IsNullOrEmpty($Category)) {
        Write-Error-Message "Usage: fetch-kb-file.ps1 -Browse `<category`>"
        Write-Host "Use -Categories to see available categories" -ForegroundColor Yellow
        exit 1
    }

    Ensure-Directories
    Refresh-Index

    $index = Get-Index

    if ($index.categories.PSObject.Properties.Name -contains $Category) {
        $keys = $index.categories.$Category
        $keys | ForEach-Object { $_ }
        Write-Host ""
        Write-Host "Total: $($keys.Count) keys in '$Category'" -ForegroundColor Gray
    } else {
        Write-Error-Message "Category '$Category' not found or empty"
        Write-Host ""
        Write-Host "Available categories:" -ForegroundColor Yellow
        $index.categories.PSObject.Properties.Name | ForEach-Object { Write-Host "  $_" }
        exit 1
    }
    exit 0
}

# =============================================================================
# Command: -Categories - List all categories
# =============================================================================
function Invoke-Categories {
    Ensure-Directories
    Refresh-Index

    $index = Get-Index

    Write-Host "Available categories:"
    $index.categories.PSObject.Properties | ForEach-Object {
        Write-Host "  $($_.Name): $($_.Value.Count) keys"
    }
    exit 0
}

# =============================================================================
# Command: -Search <term> - Search for keys
# =============================================================================
function Invoke-Search {
    param([string]$Term)

    if ([string]::IsNullOrEmpty($Term)) {
        Write-Error-Message "Usage: fetch-kb-file.ps1 -Search `<term`>"
        exit 1
    }

    Ensure-Directories
    Refresh-Index

    $index = Get-Index

    $matches = $index.files.PSObject.Properties.Name | Where-Object { $_ -match $Term }

    if ($matches) {
        $matches | ForEach-Object { $_ }
        Write-Host ""
        Write-Host "Found: $(@($matches).Count) keys matching '$Term'" -ForegroundColor Gray
    } else {
        Write-Host "No keys found matching '$Term'" -ForegroundColor Yellow
    }
    exit 0
}

# =============================================================================
# Command: Fetch key
# =============================================================================
function Invoke-Fetch {
    param([string]$KeyName)

    Ensure-Directories
    Refresh-Index

    $path = Lookup-Key -KeyName $KeyName

    if (-not $path) {
        Write-Error-Message "Key '$KeyName' not found in index"
        Write-Host ""

        # Find and show similar keys
        $similar = Find-SimilarKeys -KeyName $KeyName
        if ($similar) {
            Write-Host "Similar keys:" -ForegroundColor Yellow
            $similar | ForEach-Object { Write-Host "  $_" }
        }

        Write-Host ""
        Write-Host "Tips:" -ForegroundColor Yellow
        Write-Host "  - Use -Search <term> to find keys"
        Write-Host "  - Use -Browse <category> to explore by category"
        Write-Host "  - Use -Categories to see all categories"
        exit 1
    }

    Write-Log "Key: $KeyName -> $path"

    # Check cache
    $cacheFile = "$CacheDir\$KeyName.yaml"

    # Fetch if not cached
    if (-not (Test-Path $cacheFile)) {
        Write-Log "Fetching: $BaseUrl/$path"
        try {
            $content = Invoke-WebRequest -Uri "$BaseUrl/$path" -UseBasicParsing | Select-Object -ExpandProperty Content
            $filtered = Filter-Metadata -Content $content
            $filtered | Out-File -FilePath $cacheFile -Encoding UTF8 -NoNewline
            Write-Log "Cached to: $cacheFile"
        } catch {
            Write-Error-Message "Failed to fetch content: $_"
            exit 1
        }
    } else {
        Write-Log "Using cached: $cacheFile"
    }

    # Output content
    Get-Content $cacheFile -Raw
}

# =============================================================================
# Main - Dispatch based on parameters
# =============================================================================

if ($Help) {
    Show-Help
}

if ($Cached) {
    Invoke-Cached
}

if ($Categories) {
    Invoke-Categories
}

if (-not [string]::IsNullOrEmpty($Browse)) {
    Invoke-Browse -Category $Browse
}

if (-not [string]::IsNullOrEmpty($Search)) {
    Invoke-Search -Term $Search
}

if (-not [string]::IsNullOrEmpty($Key)) {
    Invoke-Fetch -KeyName $Key
    exit 0
}

# No valid command - show help
Show-Help
