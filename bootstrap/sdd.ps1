# Wrapper CLI SDD
$ErrorActionPreference = "Stop"
$KitDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "Python no encontrado. Instala Python 3.10+." }
& $py.Source (Join-Path $KitDir "cli\sdd.py") @args
exit $LASTEXITCODE
