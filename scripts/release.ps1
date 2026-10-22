<#
.SYNOPSIS
    Release token-buffet: set the version, commit, push, and create a GitHub Release. GitHub Actions publishes to PyPI.

.DESCRIPTION
    Sets the version in pyproject.toml and src/tokenbuffet/__init__.py, commits everything
    (git add -A), pushes, and creates the GitHub Release v<version> with the gh CLI. Publishing
    the release starts .github/workflows/publish.yml, which builds and uploads via PyPI
    trusted publishing. Safe to re-run with the same version: nothing to commit is skipped and
    an existing release is left alone.

.EXAMPLE
    .\scripts\release.ps1 0.2.0
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Version                          # X.Y.Z, always explicit
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

function Invoke-Git { git @args; if ($LASTEXITCODE) { throw "git $args failed" } }
Invoke-Git add -A
git diff --cached --quiet
if ($LASTEXITCODE) { Invoke-Git commit -m "Release $Version" }
Invoke-Git push
gh release view "v$Version" *> $null
if ($LASTEXITCODE) { gh release create "v$Version" --title "v$Version" --generate-notes; if ($LASTEXITCODE) { throw "gh release create failed" } } else { Write-Host "Release v$Version already exists." }
Write-Host "Released v$Version. Watch the publish run under the repo's Actions tab." -ForegroundColor Green
