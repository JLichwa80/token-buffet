$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Initializing Basisconf Router Environment  " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path $ScriptDir

# Create necessary directories
$dirs = @(
    "src",
    "src/extractors",
    "config/registered_providers",
    "data/providers_status",
    "logs/router",
    "logs/proxy",
    "logs/sessions",
    "data/temp",
    "scripts"
)

foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        Write-Host "Creating directory: $d" -ForegroundColor Gray
        New-Item -ItemType Directory -Path $d | Out-Null
    }
}

Write-Host "`nAll directories are set up!" -ForegroundColor Green
Write-Host "Zero external dependencies detected (Pure Python Standard Library)." -ForegroundColor Green

Write-Host "`nTo start the proxies and router, run:" -ForegroundColor Yellow
Write-Host ".\scripts\fleet\start_all_proxies.ps1" -ForegroundColor White
