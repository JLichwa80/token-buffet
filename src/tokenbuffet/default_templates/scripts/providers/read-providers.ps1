<#
.SYNOPSIS
    Refresh ALL registered providers: export usage + models JSON for each.

.DESCRIPTION
    Loops over registered_providers/* and runs read-provider.ps1 for
    each provider, writing the structured JSON to data/providers_status/ (which
    the router and proxies read). This is the external refresher: the router
    never scrapes -- run this (on a schedule, or by hand) to refresh the files.

.EXAMPLE
    .\scripts\providers\read-providers.ps1               # every provider, usage + models
    .\scripts\providers\read-providers.ps1 -Op usage     # every provider, usage only
    .\scripts\providers\read-providers.ps1 -Provider grok  # just grok, usage + models
#>
param(
    [string]$Provider = "",                       # limit to one provider; default = all
    [ValidateSet('all', 'usage', 'models')]
    [string]$Op = 'all'
)

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = Join-Path $ScriptDir "../.."
Set-Location -Path $RepoRoot
$LogDir = Join-Path $RepoRoot 'logs/extractors'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
Start-Transcript -Path (Join-Path $LogDir ("refresh-{0}-{1}.log" -f (Get-Date -Format 'yyyyMMdd-HHmmss'), $PID)) | Out-Null
try {

$ops = if ($Op -eq 'all') { @('usage', 'models') } else { @($Op) }
$failed = $false

$providerDirs = Get-ChildItem -Path "registered_providers" -Directory
foreach ($dir in $providerDirs) {
    $prov = $dir.Name
    if ($Provider -and $prov -ne $Provider) { continue }
    foreach ($o in $ops) {
        Write-Host "[read-providers] $prov $o ..." -ForegroundColor Cyan
        try {
            & (Join-Path $ScriptDir "read-provider.ps1") $o $prov
            if ($LASTEXITCODE -ne 0) {
                Write-Host "[read-providers] $prov $o FAILED (exit $LASTEXITCODE)" -ForegroundColor Red
                $failed = $true
            }
        } catch {
            Write-Host "[read-providers] $prov $o FAILED: $_" -ForegroundColor Red
            $failed = $true
        }
    }
}
if ($failed) { throw "One or more provider refreshes failed; see logs/extractors/." }
Write-Host "[read-providers] done -> data/providers_status/" -ForegroundColor Green

} finally { Stop-Transcript | Out-Null }
