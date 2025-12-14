# OBEX Download Helper Script v2.1 (Windows PowerShell)
# Automatically retrieves YAML metadata and downloads OBEX object
# Usage: powershell -File download-helper.ps1 -ObjectId [id]

param(
    [Parameter(Mandatory=$true)]
    [string]$ObjectId
)

# Enable strict error handling
$ErrorActionPreference = "Stop"

Write-Host "[INFO] OBEX Download Helper v2.1 (Windows)" -ForegroundColor Cyan
Write-Host "[INFO] Object ID: $ObjectId" -ForegroundColor Gray

# GitHub API base for fetching OBEX metadata (OBEX not in p2kb index)
$ApiBase = "https://api.github.com/repos/ironsheep/P2-Knowledge-Base/contents"
$ApiHeaders = @{Accept="application/vnd.github.raw"}

# Step 1: Fetch the object's YAML directly from GitHub
Write-Host "[INFO] Fetching object metadata..." -ForegroundColor Yellow
$yamlPath = "deliverables/ai/P2/community/obex/objects/$ObjectId.yaml"

try {
    $yamlContent = (Invoke-WebRequest -Uri "$ApiBase/$yamlPath" -Headers $ApiHeaders -UseBasicParsing).Content

    if ([string]::IsNullOrWhiteSpace($yamlContent)) {
        throw "Empty YAML content"
    }
} catch {
    Write-Host "[ERR] Could not fetch YAML for object $ObjectId" -ForegroundColor Red
    Write-Host "Please verify the object ID is correct." -ForegroundColor Yellow
    Write-Host "Valid IDs are numeric (e.g., 2811, 4047)" -ForegroundColor Gray
    exit 1
}

# Step 2: Parse title from the captured YAML content
$titleLine = $yamlContent -split "`n" | Where-Object { $_ -match '^\s+title:' } | Select-Object -First 1
if ($titleLine) {
    $title = ($titleLine -replace '^\s+title:\s*', '').Trim()
    # Remove surrounding quotes if present
    $title = $title -replace '^["'']|["'']$', ''
} else {
    Write-Host "[ERR] Could not parse title from YAML" -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] Title: $title" -ForegroundColor Gray

# Step 3: Generate slug from title
$titleSlug = $title.ToLower() -replace '[^a-z0-9]', '-' -replace '-+', '-' -replace '^-|-$', ''
Write-Host "[INFO] Directory slug: $titleSlug" -ForegroundColor Gray

# Step 4: Get download URL from YAML (or construct it)
$urlLine = $yamlContent -split "`n" | Where-Object { $_ -match 'download_direct:' } | Select-Object -First 1
if ($urlLine -and $urlLine -match 'https://') {
    # Extract URL from the line
    $downloadUrl = $urlLine -replace '.*download_direct:\s*', ''
    $downloadUrl = $downloadUrl.Trim()
} else {
    # Fallback: construct URL from object ID
    $downloadUrl = "https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB$ObjectId"
}

Write-Host "[INFO] Download URL: $downloadUrl" -ForegroundColor Gray

# Step 5: Create directory and download
$obexPath = "OBEX\$titleSlug"
Write-Host "[OK] Creating directory: $obexPath" -ForegroundColor Green
New-Item -ItemType Directory -Force -Path $obexPath | Out-Null
Set-Location $obexPath

# Download the ZIP file
$zipFile = "OB$ObjectId.zip"
Write-Host "[INFO] Downloading from OBEX..." -ForegroundColor Yellow

try {
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipFile
} catch {
    Write-Host "[ERR] Download failed" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}

# Check if download was successful
if (-not (Test-Path $zipFile) -or (Get-Item $zipFile).Length -eq 0) {
    Write-Host "[ERR] Download failed or file is empty" -ForegroundColor Red
    exit 1
}

$fileSize = (Get-Item $zipFile).Length / 1KB
Write-Host "[OK] Downloaded: $zipFile ($([math]::Round($fileSize, 2)) KB)" -ForegroundColor Green

# Step 6: Extract the ZIP file
Write-Host "[INFO] Extracting $zipFile..." -ForegroundColor Yellow
Expand-Archive -Path $zipFile -DestinationPath . -Force

# Step 7: Check for nested ZIPs (common in OBEX)
$nestedZips = Get-ChildItem -Path . -Filter "*.zip" -Recurse | Where-Object { $_.Name -ne $zipFile }
if ($nestedZips) {
    Write-Host "[INFO] Found nested ZIP files, extracting..." -ForegroundColor Yellow
    foreach ($nested in $nestedZips) {
        $destName = [System.IO.Path]::GetFileNameWithoutExtension($nested.Name)
        Write-Host "   Extracting: $($nested.Name)" -ForegroundColor Gray
        Expand-Archive -Path $nested.FullName -DestinationPath $destName -Force
    }
}

# Step 8: List extracted contents
Write-Host ""
Write-Host "[INFO] Extracted contents:" -ForegroundColor Cyan
Get-ChildItem -Recurse | Format-Table Mode, LastWriteTime, Length, Name -AutoSize

# Step 9: Report completion
Write-Host ""
Write-Host "[OK] OBEX object $ObjectId successfully downloaded and extracted" -ForegroundColor Green
Write-Host "[INFO] Location: $(Get-Location)" -ForegroundColor Cyan
Write-Host "[INFO] Object: $title" -ForegroundColor Gray
Write-Host ""
Write-Host "[STOP] Ready for user inspection" -ForegroundColor Yellow

# Output the final path to stdout for programmatic capture
Write-Output "$(Get-Location)"
