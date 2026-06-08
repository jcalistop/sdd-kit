# Inicializa SDD en un proyecto.
# Uso: .\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App"

param(
    [string]$Profile = "laravel-filament",
    [string]$Project = "Mi Proyecto",
    [string]$SddPath = ".github/docs/sdd",
    [switch]$Cursor
)

$ErrorActionPreference = "Stop"
$KitDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not (Test-Path (Join-Path $KitDir "core"))) {
    Write-Error "No se encontró sdd-kit/core en $KitDir"
}
$TargetRoot = Get-Location
$ProfileDir = Join-Path $KitDir "profiles\$Profile"

if (-not (Test-Path $ProfileDir)) {
    Write-Error "Perfil no encontrado: $Profile"
}

$FullSdd = Join-Path $TargetRoot $SddPath
$BusinessPath = Join-Path $TargetRoot ".github/docs/business"

@("specs", "archive", "adr", "releases", "templates", "profiles") | ForEach-Object {
    New-Item -ItemType Directory -Force -Path (Join-Path $FullSdd $_) | Out-Null
}
New-Item -ItemType Directory -Force -Path $BusinessPath | Out-Null

@("workflow.md", "operations.md", "branching.md", "checklist-pr.md", "README.md") | ForEach-Object {
    Copy-Item (Join-Path $KitDir "core\$_") (Join-Path $FullSdd $_) -Force
}

Copy-Item (Join-Path $KitDir "core\releases\*") (Join-Path $FullSdd "releases\") -Recurse -Force
Copy-Item (Join-Path $KitDir "core\adr\README.md") (Join-Path $FullSdd "adr\README.md") -Force
Copy-Item (Join-Path $KitDir "core\templates\*") (Join-Path $FullSdd "templates\") -Force
Copy-Item $ProfileDir (Join-Path $FullSdd "profiles\$Profile") -Recurse -Force

$config = Get-Content (Join-Path $KitDir "sdd.config.example.yaml") -Raw
$config = $config -replace "Mi Proyecto", $Project
$config = $config -replace "profile: laravel-filament", "profile: $Profile"
Set-Content (Join-Path $FullSdd "sdd.config.yaml") $config -Encoding UTF8

$backlog = Get-Content (Join-Path $KitDir "core\templates\BACKLOG-template.md") -Raw
$backlog = $backlog -replace "\{\{PROJECT_NAME\}\}", $Project
Set-Content (Join-Path $FullSdd "BACKLOG.md") $backlog -Encoding UTF8

@"
# SDD — $Project

Instancia SDD generada con **sdd-kit** (perfil ``$Profile``).

| Capa | Ubicación |
|------|-----------|
| Kit | ``sdd-kit/`` |
| Instancia | Este directorio |

**Config:** [sdd.config.yaml](sdd.config.yaml)
"@ | Set-Content (Join-Path $FullSdd "PROJECT.md") -Encoding UTF8

if (-not (Test-Path (Join-Path $BusinessPath "README.md"))) {
    @"
# Negocio — $Project

Contexto de producto. Separado de SDD en ``$SddPath``.
"@ | Set-Content (Join-Path $BusinessPath "README.md") -Encoding UTF8
}

$prTemplate = Join-Path $TargetRoot ".github\PULL_REQUEST_TEMPLATE.md"
if (-not (Test-Path $prTemplate)) {
    New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot ".github") | Out-Null
    Copy-Item (Join-Path $KitDir "core\templates\pr-template.md") $prTemplate -Force
}

if ($Cursor) {
    $rulesDir = Join-Path $TargetRoot ".cursor\rules"
    New-Item -ItemType Directory -Force -Path $rulesDir | Out-Null
    Copy-Item (Join-Path $KitDir "bootstrap\cursor-rules\sdd-core.mdc") (Join-Path $rulesDir "sdd-core.mdc") -Force
    $stackRule = Join-Path $KitDir "bootstrap\cursor-rules\sdd-stack-$Profile.mdc"
    if (Test-Path $stackRule) {
        Copy-Item $stackRule $rulesDir -Force
    }
}

Write-Host "SDD inicializado en $FullSdd (perfil: $Profile)"
