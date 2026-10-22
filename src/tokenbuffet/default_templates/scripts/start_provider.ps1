# Run `tbuffet start-provider` in this workspace [name] (omit for all providers).
Set-Location (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..")
$env:PYTHONIOENCODING = "utf-8"
python -m tokenbuffet.cli start-provider @args
