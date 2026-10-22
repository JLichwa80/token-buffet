# Run `tbuffet stop-router` in this workspace.
Set-Location (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..")
$env:PYTHONIOENCODING = "utf-8"
python -m tokenbuffet.cli stop-router @args
