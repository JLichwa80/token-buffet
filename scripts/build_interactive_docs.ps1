<#
.SYNOPSIS
    Regenerate the interactive documentation site (site/) from docs/interactive-documentation/.

.DESCRIPTION
    Needs: pip install concept-mapmaker. Everything in the output folder is replaced.
    Arguments pass through to build_interactive_docs.py: [SRC] [--out OUT].

.EXAMPLE
    .\scripts\build_interactive_docs.ps1
    .\scripts\build_interactive_docs.ps1 C:\my\docs --out C:\my\site
#>
$ErrorActionPreference = 'Stop'

python (Join-Path $PSScriptRoot "build_interactive_docs.py") @args
if ($LASTEXITCODE) { throw "build_interactive_docs.py failed" }
