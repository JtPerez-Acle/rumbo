# Run the course factory against the CLOUD database, with the right interpreter.
#
# Lives in the repo for the same reason run_local.ps1 does: the documented
# command was `python studio/cloud/course_factory.py <slug> all`, and typing
# that gets you `ModuleNotFoundError: No module named 'loguru'` — the system
# Python is not the one with the dependencies, and even past that the factory
# needs DATABASE_URL, OPENROUTER_API_KEY and PEXELS_API_KEY, none of which are
# on a fresh shell. A command in the docs that cannot be typed is a bug.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File studio/cloud/run_factory.ps1 curso-sql all
#   powershell -NoProfile -ExecutionPolicy Bypass -File studio/cloud/run_factory.ps1 curso-sql preflight
#
# CAUTION: this points at the PRODUCTION database. `all` runs for 2-3 hours and
# writes real rows. Everything is idempotent — re-running is the recovery model.

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $repo

if ($args.Count -lt 1) {
    Write-Output "uso: run_factory.ps1 <slug> <comando> [extra]"
    Write-Output "  ej: run_factory.ps1 curso-sql preflight"
    Write-Output "      run_factory.ps1 curso-sql all"
    exit 2
}

$python = Join-Path $repo "MoneyPrinterTurbo\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) { throw "no existe el intérprete del repo: $python" }

Write-Output "leyendo variables de Railway..."
$pg  = railway variables --service Postgres --kv
$svc = railway variables --kv

function Get-Var($lines, $name) {
    foreach ($l in $lines) { if ($l -match "^$name=(.*)$") { return $Matches[1] } }
    return ""
}

# DATABASE_PUBLIC_URL is how a script on this machine reaches the cloud DB; the
# private one only resolves inside Railway's network.
$env:DATABASE_URL       = Get-Var $pg  "DATABASE_PUBLIC_URL"
$env:OPENROUTER_API_KEY = Get-Var $svc "OPENROUTER_API_KEY"
$env:LLM_MODEL          = Get-Var $svc "LLM_MODEL"
$env:PEXELS_API_KEY     = Get-Var $svc "PEXELS_API_KEY"
# Spanish output through a Windows console otherwise arrives as mojibake.
$env:PYTHONIOENCODING   = "utf-8"

if (-not $env:DATABASE_URL)       { throw "DATABASE_PUBLIC_URL no encontrada - ¿está enlazado el CLI de Railway?" }
if (-not $env:OPENROUTER_API_KEY) { throw "OPENROUTER_API_KEY no encontrada - la generación de lecciones fallaría en la primera llamada" }
if (-not $env:PEXELS_API_KEY)     { Write-Output "AVISO: sin PEXELS_API_KEY - el render fallará (el resto de las fases funcionan)" }

Write-Output "db ok - modelo $($env:LLM_MODEL) - ejecutando: $($args -join ' ')"
Write-Output ""
& $python (Join-Path $repo "studio\cloud\course_factory.py") @args
exit $LASTEXITCODE
