# Run the learner app locally against the CLOUD database (docs/05-operations.md).
#
# Lives in the repo on purpose: the launch.json entry used to point at a script
# in a session scratchpad, which died with that session and left `preview_start`
# broken. Secrets are read from Railway at runtime and never written to disk.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File studio/dashboard/run_local.ps1
#
# CAUTION: this points at the PRODUCTION database. Test rows are real rows —
# create them under obviously-fake emails and delete them when you are done.

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $repo

Write-Output "reading Railway env..."
$pg = railway variables --service Postgres --kv
$svc = railway variables --kv

function Get-Var($lines, $name) {
    foreach ($l in $lines) {
        if ($l -match "^$name=(.*)$") { return $Matches[1] }
    }
    return ""
}

$env:DATABASE_URL      = Get-Var $pg  "DATABASE_PUBLIC_URL"
$env:OPENROUTER_API_KEY = Get-Var $svc "OPENROUTER_API_KEY"
$env:LLM_MODEL          = Get-Var $svc "LLM_MODEL"
$env:PYTHONIOENCODING   = "utf-8"

if (-not $env:DATABASE_URL) { throw "DATABASE_PUBLIC_URL not found - is the Railway CLI linked?" }
if (-not $env:OPENROUTER_API_KEY) { Write-Output "WARNING: no OPENROUTER_API_KEY - AI evaluations and job analysis will fail" }

# Honour an assigned PORT so two sessions can run previews side by side; a stale
# server from another session serving old code is a documented time sink
# (docs/07: uvicorn has no --reload here, preview_start reuses what is running).
$port = $env:PORT
if (-not $port) { $port = "8799" }

# DASHBOARD_TOKEN is deliberately left unset: the admin gate is off locally.
Write-Output "db ok - starting uvicorn on :$port (model $($env:LLM_MODEL))"
& "$repo\MoneyPrinterTurbo\.venv\Scripts\python.exe" -m uvicorn app:app --port $port --app-dir studio/dashboard
