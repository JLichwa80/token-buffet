<#
.SYNOPSIS
    Deploy token-buffet: commit, push and publish the GitHub Release for the version in pyproject.toml.

.DESCRIPTION
    Run .\scripts\release.ps1 X.Y.Z first to set the version. Publishing the GitHub Release starts
    .github/workflows/publish.yml, which builds and uploads via PyPI trusted publishing.

.EXAMPLE
    .\scripts\deploy.ps1
#>
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..")

$pyproject = Get-Content pyproject.toml -Raw
if ($pyproject -notmatch '(?m)^version = "(.*)"') { throw "No version found in pyproject.toml" }
$Version = $Matches[1]
Write-Host "Deploying v$Version" -ForegroundColor Cyan

git add -A;                          if ($LASTEXITCODE) { throw "git add failed" }
git commit -m "Release $Version";    if ($LASTEXITCODE) { throw "git commit failed" }
git push;                            if ($LASTEXITCODE) { throw "git push failed" }
gh release create "v$Version" --title "v$Version" --generate-notes
if ($LASTEXITCODE) { throw "gh release create failed" }
