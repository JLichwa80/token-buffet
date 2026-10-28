<#
.SYNOPSIS
    Regenerate the documentation site (site/) from docs/interactive-documentation/ and docs/static-pages/.

.DESCRIPTION
    Needs: pip install "concept-mapmaker>=0.2.0". Everything in the output folder is replaced.
    Arguments pass through to build_interactive_docs.py: [SRC] [--out OUT].

.EXAMPLE
    .\scripts\build_interactive_docs.ps1
    .\scripts\build_interactive_docs.ps1 C:\my\docs --out C:\my\site
#>
$ErrorActionPreference = 'Stop'

python (Join-Path $PSScriptRoot "build_interactive_docs.py") @args
if ($LASTEXITCODE) { throw "build_interactive_docs.py failed" }
