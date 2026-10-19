# Stop Token Buffet service trees in the current user's session, across workspaces.
# Does not rely on saved status files. Supports -WhatIf to preview targets.
[CmdletBinding(SupportsShouldProcess)]
param()

$ErrorActionPreference = 'Stop'
$taskkillPath = Join-Path $env:SystemRoot 'System32\taskkill.exe'
$snapshot = @(Get-CimInstance Win32_Process)
$sessionId = (Get-Process -Id $PID).SessionId
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
# Match the executable and module invocation, never arbitrary mentions in prompts.
$services = @($snapshot | Where-Object {
    $_.SessionId -eq $sessionId -and (
        ($_.Name -match '^(python(?:w|\d+(?:\.\d+)?)?|py)\.exe$' -and
         $_.CommandLine -match '(?:^|\s)-m\s+tokenbuffet\.(?:logged_run|cli_proxy_server|local_router|dashboard|extractors)(?:\s|$)') -or
        ($_.Name -match '^(?:tbuffet|tokenbuffet)\.exe$' -and
         $_.CommandLine -match '\sstart(?:\s|$)') -or
        ($_.Name -match '^python(?:w|\d+(?:\.\d+)?)?\.exe$' -and
         $_.CommandLine -match '(?:^|\s)-m\s+tokenbuffet\.cli\s+start(?:\s|$)')
    )
})
$ownedServices = @()
foreach ($service in $services) {
    $owner = Invoke-CimMethod -InputObject $service -MethodName GetOwner
    if ($owner.ReturnValue -eq 0 -and "$($owner.Domain)\$($owner.User)" -eq $currentUser) {
        $ownedServices += $service
    }
}
if (-not $ownedServices) {
    Write-Output 'No Token Buffet services found in this user session.'
    return
}

# Remember descendants before terminating parents, including any that outlive them.
$targets = @{}
foreach ($service in $ownedServices) { $targets[[int]$service.ProcessId] = $service }
do {
    $added = $false
    foreach ($item in $snapshot) {
        $parentId = [int]$item.ParentProcessId
        if (-not $targets.ContainsKey([int]$item.ProcessId) -and $targets.ContainsKey($parentId) -and
            $item.CreationDate -ge $targets[$parentId].CreationDate) {
            $targets[[int]$item.ProcessId] = $item
            $added = $true
        }
    }
} while ($added)

$failures = @()
foreach ($target in ($targets.Values | Sort-Object CreationDate)) {
    $live = Get-CimInstance Win32_Process -Filter "ProcessId = $($target.ProcessId)"
    if (-not $live -or $live.CreationDate -ne $target.CreationDate) { continue }
    if ($PSCmdlet.ShouldProcess("$($target.Name) (PID $($target.ProcessId)) and its children", 'Force stop')) {
        $savedErrorAction = $ErrorActionPreference
        try {
            $ErrorActionPreference = 'Continue'
            $output = & $taskkillPath /PID $target.ProcessId /T /F 2>&1
            $stopExitCode = $LASTEXITCODE
        } finally {
            $ErrorActionPreference = $savedErrorAction
        }
        if ($stopExitCode -ne 0) {
            $remaining = Get-CimInstance Win32_Process -Filter "ProcessId = $($target.ProcessId)"
            if ($remaining -and $remaining.CreationDate -eq $target.CreationDate) {
                $failures += "PID $($target.ProcessId): $($output -join ' ')"
            }
        }
    }
}
if ($WhatIfPreference) { return }
if ($failures) { throw ($failures -join [Environment]::NewLine) }
Write-Output 'Token Buffet service trees stopped.'
