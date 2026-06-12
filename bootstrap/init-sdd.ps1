# Inicializa SDD en un proyecto.
# Uso: .\sdd-kit\bootstrap\init-sdd.ps1 -Profile laravel-filament -Project "Mi App"

param(
    [string]$Profile = "laravel-filament",
    [string]$Project = "Mi Proyecto",
    [string]$SddPath = ".github/docs/sdd",
    [string]$Agent = "auto",
    [switch]$NoPrompt,
    [switch]$Cursor  # retrocompat: equivale a -Agent cursor
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

@("workflow.md", "operations.md", "branching.md", "checklist-pr.md", "adoption-guide.md", "agent-setup.md", "healthy-development.md", "README.md", "prompt-catalog.md") | ForEach-Object {
    Copy-Item (Join-Path $KitDir "core\$_") (Join-Path $FullSdd $_) -Force
}

Copy-Item (Join-Path $KitDir "core\prompts") (Join-Path $FullSdd "prompts") -Recurse -Force
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

$domainRules = Join-Path $BusinessPath "domain-rules.md"
if (-not (Test-Path $domainRules)) {
    $tpl = Get-Content (Join-Path $KitDir "core\templates\business-domain-template.md") -Raw
    $tpl = $tpl -replace "\{\{PROJECT_NAME\}\}", $Project
    Set-Content $domainRules $tpl -Encoding UTF8
}

$prTemplate = Join-Path $TargetRoot ".github\PULL_REQUEST_TEMPLATE.md"
if (-not (Test-Path $prTemplate)) {
    New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot ".github") | Out-Null
    Copy-Item (Join-Path $KitDir "core\templates\pr-template.md") $prTemplate -Force
}

$agentArg = if ($Cursor) { "cursor" } else { $Agent }
$installAgents = Join-Path $KitDir "bootstrap\install-agents.py"
if (Test-Path $installAgents) {
    $py = Get-Command python -ErrorAction SilentlyContinue
    if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
    if ($py) {
        $agentCmd = @(
            $py.Source,
            $installAgents,
            "install",
            "--target", $TargetRoot,
            "--kit", $KitDir,
            "--profile", $Profile,
            "--agent", $agentArg,
            "--sdd-path", $SddPath
        )
        if ($NoPrompt) { $agentCmd += "--no-prompt" }
        if ($Cursor) { $agentCmd += "--cursor" }
        & $agentCmd[0] $agentCmd[1..($agentCmd.Length - 1)]
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "install-agents.py terminó con código $LASTEXITCODE"
        }
    } else {
        Write-Warning "Python no encontrado; omitiendo instalación de adaptadores de agente. Requiere Python 3.10+."
    }
} else {
    Write-Warning "No se encontró bootstrap/install-agents.py; omitiendo adaptadores de agente."
}

Write-Host "SDD inicializado en $FullSdd (perfil: $Profile)"
Write-Host "Siguiente: revisar sdd.config.yaml, completar business/ y leer adoption-guide.md"
Write-Host "Validar: .\sdd-kit\bootstrap\validate-sdd.ps1 -SddPath `"$SddPath`""
