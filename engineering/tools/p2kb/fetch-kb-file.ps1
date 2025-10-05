# P2 Knowledge Base Fetcher v2.1 - Pre-approvable with progress
# Usage: fetch-kb-file.ps1 <path> [-Verbose]

param(
  [Parameter(Mandatory=$true)]
  [string]$path,
  
  [switch]$Verbose
)

$cache = ".p2kb-cache\$($path -replace '/','\\')"
$url = "https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main/$path"

# Progress reporting function
function Report {
  param($Message)
  Write-Host "P2KB: $Message" -ForegroundColor Cyan
}

if ($Verbose) {
  Report "Fetching: $path"
}

try {
  if (Test-Path $cache) {
    if ($Verbose) {
      Report "Using cached: $cache"
    }
    Get-Content $cache -Raw
    if ($Verbose) {
      Report "Complete: $path (cached)"
    }
  } else {
    if ($Verbose) {
      Report "Downloading: $url"
    }
    
    $dir = Split-Path $cache -Parent
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    
    Invoke-WebRequest -Uri $url -OutFile $cache -ErrorAction Stop
    
    if ($Verbose) {
      Report "Downloaded successfully: $path"
    }
    
    Get-Content $cache -Raw
    
    if ($Verbose) {
      Report "Complete: $path (downloaded)"
    }
  }
} catch {
  Report "ERROR: Failed to fetch $path"
  if (Test-Path $cache) {
    Remove-Item $cache -Force  # Remove partial download
  }
  throw $_
}
