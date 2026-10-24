<#
.SYNOPSIS
    Release token-buffet: set the version. Git is left to you.

.DESCRIPTION
    Sets the version in pyproject.toml and src/tokenbuffet/__init__.py and prints the git and gh
    commands to run next. Publishing the GitHub Release starts .github/workflows/publish.yml,
    which builds and uploads via PyPI trusted publishing. Safe to re-run with the same version.

.EXAMPLE
    .\scripts\release.ps1 0.2.0
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Version                          # X.Y.Z, always expliciti
)

$ErrorActionPreference = 'Stop'
Set-Location (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..")

if ($Version -notmatch '^\d+\.\d+\.\d+$') { throw "Version must be X.Y.Z" }
$pyproject = Get-Content pyproject.toml -Raw
if ($pyproject -notmatch '(?m)^version = "(.*)"') { throw "No version found in pyproject.toml" }
Write-Host "Version $($Matches[1]) -> $Version" -ForegroundColor Cyan

$utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText("$PWD\pyproject.toml", [regex]::Replace($pyproject, '(?m)^version = ".*"', "version = `"$Version`""), $utf8)
$init = Get-Content src\tokenbuffet\__init__.py -Raw
[IO.File]::WriteAllText("$PWD\src\tokenbuffet\__init__.py", [regex]::Replace($init, "(?m)^__version__ = .*", "__version__ = '$Version'"), $utf8)

Write-Host "Version set. Now commit, push and publish:" -ForegroundColor Green
Write-Host "  git add -A; git commit -m `"Release $Version`"; git push"
Write-Host "  gh release create v$Version --title v$Version --generate-notes"
