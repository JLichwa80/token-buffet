# Run `tbuffet start-router` in this workspace.
Set-Location (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..")
$env:PYTHONIOENCODING = "utf-8"
python -m tokenbuffet.cli start-router @args
