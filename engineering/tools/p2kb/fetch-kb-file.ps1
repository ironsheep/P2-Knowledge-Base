# P2 Knowledge Base Fetch Script v3.0
# Key-based access to YAML content
# Usage: .\fetch-kb-file.ps1 <key> [-Verbose]

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Key,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

$BaseUrl = "https://raw.githubusercontent.com/IronSheepProductionsLLC/P2-Knowledge-Base/main"
$CacheDir = if ($env:P2KB_CACHE) { $env:P2KB_CACHE } else { "$env:USERPROFILE\.p2kb-cache" }
$IndexFile = "$CacheDir\p2kb-index.json"
$IndexMaxAge = 86400  # 24 hours in seconds

function Write-Log($Message) {
    if ($Verbose) { Write-Host "[INFO] $Message" -ForegroundColor Cyan }
}

# Ensure cache directory exists
if (-not (Test-Path $CacheDir)) {
    New-Item -ItemType Directory -Path $CacheDir -Force | Out-Null
}

# Check if index needs refresh
function Update-Index {
    $needRefresh = $false
    
    if (-not (Test-Path $IndexFile)) {
        Write-Log "Index not found, downloading..."
        $needRefresh = $true
    } else {
        $age = (Get-Date) - (Get-Item $IndexFile).LastWriteTime
        if ($age.TotalSeconds -gt $IndexMaxAge) {
            Write-Log "Index is $([int]$age.TotalSeconds)s old (max ${IndexMaxAge}s), refreshing..."
            $needRefresh = $true
        }
    }
    
    if ($needRefresh) {
        Write-Log "Downloading index from $BaseUrl/deliverables/ai/p2kb-index.json.gz"
        $tempFile = "$IndexFile.tmp.gz"
        
        # Download compressed index
        Invoke-WebRequest -Uri "$BaseUrl/deliverables/ai/p2kb-index.json.gz" -OutFile $tempFile
        
        # Decompress
        $input = New-Object System.IO.FileStream $tempFile, ([IO.FileMode]::Open)
        $output = New-Object System.IO.FileStream "$IndexFile.tmp", ([IO.FileMode]::Create)
        $gzip = New-Object System.IO.Compression.GZipStream $input, ([IO.Compression.CompressionMode]::Decompress)
        $gzip.CopyTo($output)
        $gzip.Close(); $output.Close(); $input.Close()
        
        Move-Item "$IndexFile.tmp" $IndexFile -Force
        Remove-Item $tempFile -ErrorAction SilentlyContinue
        
        $idx = Get-Content $IndexFile | ConvertFrom-Json
        Write-Log "Index updated: $($idx.system.total_entries) entries"
    }
}

# Look up key in index
function Get-PathForKey($key) {
    $idx = Get-Content $IndexFile -Raw | ConvertFrom-Json
    $entry = $idx.files.$key
    if ($entry) { return $entry.path }
    return $null
}

# Filter metadata from YAML content
# These fields are process/lineage metadata, not content
function Remove-Metadata($content) {
    $content -split "`n" | Where-Object {
        $_ -notmatch '^\s*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):'
    } | Out-String
}

# Main execution
Update-Index

$PathInRepo = Get-PathForKey $Key

if (-not $PathInRepo) {
    Write-Error "Key '$Key' not found in index"
    Write-Host "Hint: Keys start with 'p2kb' followed by category and name" -ForegroundColor Yellow
    Write-Host "Example keys: p2kbPasm2Mov, p2kbArchCog, p2kbSpin2Pinwrite" -ForegroundColor Yellow
    exit 1
}

Write-Log "Key: $Key -> $PathInRepo"

# Check cache
$ContentDir = "$CacheDir\content"
if (-not (Test-Path $ContentDir)) {
    New-Item -ItemType Directory -Path $ContentDir -Force | Out-Null
}
$CacheFile = "$ContentDir\$($Key -replace '/', '_').yaml"

# Fetch if not cached
if (-not (Test-Path $CacheFile)) {
    Write-Log "Fetching: $BaseUrl/$PathInRepo"
    $content = (Invoke-WebRequest -Uri "$BaseUrl/$PathInRepo").Content
    $filtered = Remove-Metadata $content
    $filtered | Out-File -FilePath $CacheFile -Encoding UTF8 -NoNewline
    Write-Log "Cached to: $CacheFile"
}

# Output content
Get-Content $CacheFile -Raw
