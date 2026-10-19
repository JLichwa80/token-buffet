# Back-compat shim: use `tbuffet dashboard` directly.
Set-Location (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..")
$env:PYTHONIOENCODING = "utf-8"
python -m tokenbuffet.cli dashboard @args
