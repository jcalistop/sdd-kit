# Valida coherencia documental de una instancia SDD.
# Uso: .\sdd-kit\bootstrap\validate-sdd.ps1 [-SddPath ".github/docs/sdd"]
# Codigos de salida: 0=OK, 1=fallo del script/entorno (FATAL), 2=incoherencias documentales (ERROR)
# Salida por componente (SDD-010): [backlog] [specs] [config] [agent] [kit-version] [docs]

param(
    [string]$SddPath = ".github/docs/sdd"
)

$ErrorActionPreference = "Continue"
$errors = 0
$warnings = 0
$componentStats = [ordered]@{}
$lastComponent = $null

function Ensure-Component([string]$Component) {
    if (-not $script:componentStats.Contains($Component)) {
        $script:componentStats[$Component] = @{ Errors = 0; Warnings = 0; Messages = 0 }
    }
    if ($script:lastComponent -ne $Component) {
        Write-Host ""
        Write-Host "--- [$Component] ---" -ForegroundColor DarkCyan
        $script:lastComponent = $Component
    }
}

function Write-Fatal($msg) {
    Write-Host "FATAL: $msg" -ForegroundColor Magenta
}

function Write-Err {
    param([string]$Component, [string]$Msg)
    Ensure-Component $Component
    Write-Host "[$Component] ERROR: $Msg" -ForegroundColor Red
    $script:errors++
    $script:componentStats[$Component].Errors++
    $script:componentStats[$Component].Messages++
}

function Write-Warn {
    param([string]$Component, [string]$Msg)
    Ensure-Component $Component
    Write-Host "[$Component] WARN:  $Msg" -ForegroundColor Yellow
    $script:warnings++
    $script:componentStats[$Component].Warnings++
    $script:componentStats[$Component].Messages++
}

function Write-Ok {
    param([string]$Component, [string]$Msg)
    Ensure-Component $Component
    Write-Host "[$Component] OK:    $Msg" -ForegroundColor Green
    $script:componentStats[$Component].Messages++
}

Write-Host ""
Write-Host "=== Validacion SDD ($SddPath) ===" -ForegroundColor Cyan

if (-not (Test-Path $SddPath)) {
    Write-Fatal "No existe el directorio SDD: $SddPath"
    Write-Host "La validacion no pudo ejecutarse (exit 1)." -ForegroundColor Magenta
    exit 1
}

$backlogPath = Join-Path $SddPath "BACKLOG.md"
if (-not (Test-Path $backlogPath)) {
    Write-Fatal "Falta BACKLOG.md en $SddPath"
    Write-Host "La validacion no pudo ejecutarse (exit 1)." -ForegroundColor Magenta
    exit 1
}

$backlogLines = Get-Content $backlogPath -Encoding UTF8
$backlogIds = @{}
$backlogSection = @{}
$currentSection = ""

foreach ($line in $backlogLines) {
    if ($line -match '^##\s+(Discovery|Draft|Ready|In Build|Validating|Released|Descartado)') {
        $currentSection = $Matches[1]
        continue
    }
    if ($line -notmatch '^\|') { continue }
    if ($line -match '^\|\s*[-:]') { continue }
    $cols = ($line.Trim('|').Split('|') | ForEach-Object { $_.Trim() })
    if ($cols.Count -lt 1) { continue }
    if ($cols[0] -notmatch '^(SDD-\d+[a-z]?)$') { continue }
    $id = $Matches[1]
    if ($backlogIds.ContainsKey($id) -and $backlogIds[$id] -ne $currentSection) {
        Write-Err -Component "backlog" -Msg "ID $id duplicado en BACKLOG (secciones: $($backlogIds[$id]) y $currentSection)"
    } else {
        $backlogIds[$id] = $currentSection
        $backlogSection[$id] = $currentSection
    }
}

$fileIds = @{}
$seenFiles = @{}

$specDirs = @(
    (Join-Path $SddPath "specs"),
    (Join-Path $SddPath "archive")
)

foreach ($dir in $specDirs) {
    if (-not (Test-Path $dir)) { continue }
    Get-ChildItem -Path $dir -Recurse -Filter "SDD-*.md" -File | ForEach-Object {
        if ($_.Name -match '^(SDD-\d+[a-z]?)') {
            $id = $Matches[1]
            $loc = if ($_.FullName -match [regex]::Escape("\specs\")) { "specs" } else { "archive" }
            if ($seenFiles.ContainsKey($id)) {
                Write-Err -Component "specs" -Msg "ID $id aparece en mas de un archivo"
            }
            $seenFiles[$id] = $_.FullName
            $fileIds[$id] = $loc
        }
    }
}

foreach ($id in $fileIds.Keys) {
    $loc = $fileIds[$id]
    $filePath = $seenFiles[$id]
    $headerEstado = $null
    if ($filePath -and (Test-Path $filePath)) {
        $headLines = Get-Content $filePath -Encoding UTF8 -TotalCount 40
        foreach ($hl in $headLines) {
            if ($hl -match '\|\s*\*\*Estado\*\*\s*\|\s*`?([^`|]+)`?\s*\|') {
                $headerEstado = $Matches[1].Trim()
                break
            }
        }
    }
    if ($loc -eq "specs") {
        if (-not $backlogIds.ContainsKey($id)) {
            Write-Err -Component "specs" -Msg "Spec $id en specs/ sin entrada en BACKLOG.md"
        } elseif ($backlogSection[$id] -eq "Released") {
            Write-Err -Component "specs" -Msg "Spec $id en specs/ pero BACKLOG dice Released (debe estar en archive/)"
        } elseif ($backlogSection[$id] -eq "Descartado") {
            Write-Err -Component "specs" -Msg "Spec $id en specs/ pero BACKLOG dice Descartado (debe estar en archive/)"
        } elseif ($headerEstado -match '^(Released|Descartado)\b') {
            Write-Err -Component "specs" -Msg "Spec $id en specs/ con cabecera Estado=$headerEstado (terminales solo en archive/)"
        } elseif ($backlogSection[$id] -eq "Discovery") {
            Write-Warn -Component "specs" -Msg "Spec $id en specs/ pero BACKLOG aun en Discovery (esperado Draft+)"
        } else {
            Write-Ok -Component "specs" -Msg "Spec activo $id coherente con BACKLOG ($($backlogSection[$id]))"
        }
    }
    if ($loc -eq "archive") {
        if (-not $backlogIds.ContainsKey($id)) {
            Write-Err -Component "specs" -Msg "Spec archivado $id sin entrada en BACKLOG.md"
        } elseif ($backlogSection[$id] -eq "Released" -or $backlogSection[$id] -eq "Descartado") {
            Write-Ok -Component "specs" -Msg "Spec archivado $id coherente con BACKLOG ($($backlogSection[$id]))"
        } else {
            Write-Err -Component "specs" -Msg "Spec $id en archive/ pero BACKLOG no esta en Released ni Descartado (esta en $($backlogSection[$id]))"
        }
    }
}

$activeSections = @("Draft", "Ready", "In Build", "Validating")
foreach ($id in $backlogIds.Keys) {
    $sec = $backlogSection[$id]
    if ($activeSections -contains $sec) {
        if ($fileIds[$id] -ne "specs") {
            Write-Err -Component "specs" -Msg "BACKLOG: $id en $sec pero no hay archivo en specs/"
        }
    }
}

$nextLine = $backlogLines | Where-Object { $_ -match 'ximo ID disponible' } | Select-Object -First 1
if ($nextLine -match 'SDD-(\d+)') {
    $nextNum = [int]$Matches[1]
    $maxNum = 0
    $allIds = @($backlogIds.Keys) + @($fileIds.Keys) | Select-Object -Unique
    foreach ($id in $allIds) {
        if ($id -match 'SDD-(\d+)') {
            $n = [int]$Matches[1]
            if ($n -gt $maxNum) { $maxNum = $n }
        }
    }
    $expected = $maxNum + 1
    if ($nextNum -lt $expected) {
        Write-Warn -Component "backlog" -Msg "Proximo ID SDD-$($nextNum.ToString('000')) parece bajo (max usado: SDD-$($maxNum.ToString('000')))"
    } else {
        Write-Ok -Component "backlog" -Msg "Proximo ID disponible coherente (max usado: SDD-$($maxNum.ToString('000')))"
    }
}

if (-not (Test-Path (Join-Path $SddPath "sdd.config.yaml"))) {
    Write-Warn -Component "config" -Msg "Falta sdd.config.yaml"
} else {
    Write-Ok -Component "config" -Msg "sdd.config.yaml presente"
    $configText = Get-Content (Join-Path $SddPath "sdd.config.yaml") -Raw -Encoding UTF8
    if ($configText -match 'targets:\s*\[([^\]]*)\]' -and $Matches[1] -match 'cursor') {
        $projectRoot = (Resolve-Path (Join-Path $SddPath "../../..")).Path
        $manifestPath = Join-Path $projectRoot ".cursor/skills/.sdd-kit-manifest.json"
        if (-not (Test-Path $manifestPath)) {
            Write-Warn -Component "agent" -Msg "agent.targets incluye cursor pero falta .cursor/skills/.sdd-kit-manifest.json (reinstalar con install-agents.py)"
        } else {
            Write-Ok -Component "agent" -Msg "Manifest de skills SDD presente (.sdd-kit-manifest.json)"
        }
    }
}

$kitVersionScript = Join-Path $PSScriptRoot "kit-version.py"
if (Test-Path $kitVersionScript) {
    $py = Get-Command python -ErrorAction SilentlyContinue
    if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
    if ($py) {
        $projectRoot = (Resolve-Path (Join-Path $SddPath "../../..")).Path
        $checkOut = & $py.Source $kitVersionScript check $SddPath $projectRoot 2>&1
        foreach ($line in @($checkOut)) {
            if ($line -match '^WARN:') { Write-Warn -Component "kit-version" -Msg ($line -replace '^WARN:\s*', '') }
            elseif ($line -match '^OK:') { Write-Ok -Component "kit-version" -Msg ($line -replace '^OK:\s*', '') }
        }
    }
}

# Dual-release (producto kit): acta campaña => nota SemVer en docs/releases/
$projectRootForDocs = (Resolve-Path (Join-Path $SddPath "../../..")).Path
$productReleasesPath = Join-Path $projectRootForDocs "docs/releases"
$campaignReleasesPath = Join-Path $SddPath "releases"
if ((Test-Path $productReleasesPath) -and (Test-Path $campaignReleasesPath)) {
    $campaignDirs = Get-ChildItem -Path $campaignReleasesPath -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '^v\d+\.\d+\.\d+' }
    $dualWarns = 0
    foreach ($dir in $campaignDirs) {
        $ver = $dir.Name
        $productNote = Join-Path $productReleasesPath "$ver.md"
        $hasActa = Get-ChildItem -Path $dir.FullName -Filter "release_*.md" -File -ErrorAction SilentlyContinue
        if ($hasActa -and -not (Test-Path $productNote)) {
            Write-Warn -Component "docs" -Msg "dual-release: existe acta $ver/ pero falta docs/releases/$ver.md"
            $dualWarns++
        }
    }
    if ($campaignDirs.Count -gt 0 -and $dualWarns -eq 0) {
        Write-Ok -Component "docs" -Msg "dual-release: actas de campana con nota producto en docs/releases/"
    }
}

Write-Host ""
Write-Host "--- Resumen ---" -ForegroundColor Cyan
foreach ($name in $componentStats.Keys) {
    $s = $componentStats[$name]
    if ($s.Messages -eq 0) { continue }
    $status = if ($s.Errors -gt 0) { "FAIL" } elseif ($s.Warnings -gt 0) { "WARN" } else { "OK  " }
    $color = if ($s.Errors -gt 0) { "Red" } elseif ($s.Warnings -gt 0) { "Yellow" } else { "Green" }
    Write-Host ("[{0,-12}] {1} ({2} errores, {3} warnings)" -f $name, $status, $s.Errors, $s.Warnings) -ForegroundColor $color
}

Write-Host ""
Write-Host "Total: $errors error(es), $warnings advertencia(s)"

if ($errors -gt 0) {
    Write-Host ""
    Write-Host "Validacion documental SDD FALLIDA. Corrige los ERROR listados arriba (exit 2)." -ForegroundColor Red
    exit 2
}

Write-Host ""
Write-Host "Validacion documental SDD OK." -ForegroundColor Green
exit 0
