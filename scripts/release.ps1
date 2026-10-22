<#
.SYNOPSIS
    Release token-buffet: set the version, commit, tag, and push. GitHub Actions publishes to PyPI.

.DESCRIPTION
    Sets the version in pyproject.toml and src/tokenbuffet/__init__.py, commits everything
    (git add -A), tags v<version>, and pushes the commit and tag. The tag push starts
    .github/workflows/publish.yml, which builds and uploads via PyPI trusted publishing.
    Safe to re-run with the same version: nothing to commit is skipped and an existing tag is reused.

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
if (-not (git tag -l "v$Version")) { Invoke-Git tag "v$Version" }
Invoke-Git push --follow-tags
Write-Host "Pushed v$Version. Watch the publish run under the repo's Actions tab." -ForegroundColor Green
