<#
.SYNOPSIS
Read a provider's usage/quota or model list out of its CLI (Windows entry point).

.DESCRIPTION
These numbers only exist on the vendor CLI's interactive /usage and /model
screens -- there is no API for them. This drives the real CLI through a
pseudo-console, reads what it prints, and turns it into JSON:

  usage   -> remaining quota per period (how much is left before you hit a limit)
  models  -> the models that provider currently offers

Two steps run under the hood: capture (drive the TUI, clean the screen into
tests/<provider>_<op>_raw.txt) then parse (run the config's regexes over that
text into tests/<provider>_<op>.json). This script owns provider naming, output
filenames, flags, and sequencing; Python only provides the two primitives
(python -m tokenbuffet.logged_run --log extractors/console.log --module tokenbuffet.extractors capture|parse).

.EXAMPLE
  .\scripts\providers\read_provider_status.ps1 usage grok     # how much quota grok has left -> JSON
  .\scripts\providers\read_provider_status.ps1 models grok    # grok's model list -> JSON
  .\scripts\providers\read_provider_status.ps1 usage grok -RawOnly                       # capture only, skip parse
  .\scripts\providers\read_provider_status.ps1 usage grok -Extract tests\grok_usage_raw.txt  # re-parse saved raw
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('models', 'usage')]
    [string]$Op,

    [Parameter(Mandatory = $true, Position = 1)]
    [string]$Config,

    [switch]$RawOnly,
    [string]$Extract
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)   # repo root (parent of scripts/providers/)
$StatusDir = Join-Path $Root 'data/providers_status'  # structured JSON the router/proxy read
$RawDir = Join-Path $StatusDir 'raw'                 # captured screen text (for regex iteration)
New-Item -ItemType Directory -Force -Path $RawDir, $StatusDir | Out-Null
# Make `python -m tokenbuffet.extractors` importable regardless of the caller's cwd.
$env:PYTHONPATH = (Join-Path $Root 'src') + [IO.Path]::PathSeparator + $Root + [IO.Path]::PathSeparator + $env:PYTHONPATH
$Python = if ($env:PYTHON) { $env:PYTHON } else { 'python' }

function Get-ProviderName([string]$inp) {
    $base = Split-Path -Leaf ($inp.TrimEnd('/', '\'))
    if ($base -eq 'config.json' -or $base -eq 'config') {
        $parent = Split-Path -Leaf (Split-Path -Parent $inp)
        if ($parent) { return $parent } else { return 'provider' }
    }
    $n = $base -replace '\.json$', ''
    if ($n) { return $n } else { return 'provider' }
}

$name = Get-ProviderName $Config
$rawPath = Join-Path $RawDir "$($name)_$($Op)_raw.txt"
$jsonPath = Join-Path $StatusDir "$($name)_$($Op).json"

# Resolve a bare provider name to its repo-root config.json, leaving explicit paths untouched.
$ConfigPath = $Config
if ($Config -notmatch '[\\/]' -and $Config -notlike '*.json') {
    $ConfigPath = Join-Path $Root "registered_providers/$Config/config.json"
}

if ($Extract) {
    # Extraction only, from the given capture file.
    & $Python -m tokenbuffet.logged_run --log extractors/console.log --module tokenbuffet.extractors parse $Op $ConfigPath $Extract $jsonPath --provider $name
    exit $LASTEXITCODE
}

& $Python -m tokenbuffet.logged_run --log extractors/console.log --module tokenbuffet.extractors capture $Op $ConfigPath $rawPath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if ($RawOnly) {
    Write-Host "raw-only: saved $rawPath"
    exit 0
}

& $Python -m tokenbuffet.logged_run --log extractors/console.log --module tokenbuffet.extractors parse $Op $ConfigPath $rawPath $jsonPath --provider $name
exit $LASTEXITCODE
